# Cleanroom round 14 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,168 lines), in five `Read` calls covering lines 1–4168 with no gaps. I ran
`wc -l` on that file and three Python scripts of my own authorship in the
scratchpad directory (`crc.py`, `c2.py`, `build.py`, `reader.py`), plus two
`python3 - <<EOF` heredocs. Two of the heredocs read `spec/tarn.md` again, to
count register rows and instance cells mechanically and to audit the
Detector/Detected columns; nothing else on disk was read. I did not open
`docs/`, `PLAN.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, or any output directory; I ran no `git` command, no web
search, and no directory listing. I wrote `example.tarn` (a file I generated
myself) and this transcript. I used background knowledge of DEFLATE/zstd/LZ4/
CRC-32C/JSON only to sanity-check that the document's external references say
what it claims about them; every conclusion below is sourced to this document.

---

## 0. Method

I wrote a reader in the order I would actually write the code: open path,
validation tiers, layer access, tile read, extract. I then built a real
128-byte file (Appendix A's) and a real 448-byte one-layer file with a stored
tile, and ran the reader over it. Every constant, offset, CRC and count the
document states that I could compute, I computed. I record below each point
where the text failed to tell me what to do, whether or not the passage was in
the changed surface.

I read the seventeen changed sections cold first (§2.3, §4.7, §5.2, §11.1,
§16.2, §20.3, §21.1–§21.7, §21.9, §24, Appendices G and H), then implemented,
then went back over the changed sections with what implementation had taught
me. Findings 1 and 2 both come from that second pass.

---

## 1. Checksum primitive — the first thing to get right

§4.5 `[R-ENC-09]`: CRC-32C, Castagnoli 0x1EDC6F41, reflected in and out,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian. Reflected input
and output means I implement with the reflected polynomial 0x82F63B78 and a
right-shifting table. §4.5's check vector is the gate:

```
CRC-32C("123456789") = 0xE3069283   -> computed 0xe3069283   OK
CRC-32C(<zero bytes>) = 0x00000000  -> computed 0x0          OK
```

Both reproduce. Every later CRC in this transcript uses that function.

I then checked every CRC constant the document states:

| Where | Stated | Computed |
|---|---|---|
| Appendix A trailer CRC over `[0,60)` | `0xE00938D2` (`D2 38 09 E0`) | `0xe00938d2` |
| §7.4 example, CRC over 4 sentinel entries (80 bytes) | `0x80A34955` | `0x80a34955` |
| §7.4 example, `crc_of_crc_array` | `0xC4EE982E` | `0xc4ee982e` |
| §15.4 / Appendix B, full all-sentinel segment (2^16 entries) | `0xEECB3BB2` | `0xeecb3bb2` |
| §7.1 / Appendix A, empty directory record sequence | `0x00000000` | `0x0` |

All five correct. No constant defect found. (This matters: `0xEECB3BB2` is a
1.25 MiB computation nobody checks by hand, and `0xC4EE982E` is a CRC of a CRC,
which is exactly the shape of arithmetic that goes wrong silently.)

---

## 2. The open path, byte by byte

### 2.1 Steps and their bounds

§19.1 `[R-RDR-01]` gives four steps. What each one may act on, and what bounds
each range *before* the range has been read, is the part I had to assemble from
§4.2 `[R-ENC-05]`, §6.2 `[R-CNT-06]`, §6.4 `[R-CNT-10]` and §8.2 `[R-CNT-20]`:

**Step 1 — F.** The size must be transport-authoritative (`[R-CNT-10]`): a full
response's content length, a range response's complete length, or a size probe.
A reader that cannot obtain one probes or fails, and MUST NOT substitute the
trailer's own `committed_file_length`. This is the only quantity in the whole
open that does not come from the file, and it is what bounds everything else.
Before anything else I check F ≥ 128 (§5.1 `[R-CNT-27]`, register row F5).

**Step 2 — trailer.** Fetch `[F−64, F)`. §6.2 fixes the validation order and I
followed it literally, because getting it wrong changes diagnostics if not
verdicts:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` at trailer offset 0 (row F8);
2. trailer CRC at `[60,64)` over `[0,60)` (row F14);
3. version gate (§6.3): `version_major = 0` → reject-file (F18); an
   unimplemented major → reject-file on *capability* grounds with a distinct
   diagnostic (`[R-CNT-07]`, §21.6's closing paragraph — not a register row);
4. then, and only then, everything else: flag gates, `committed_file_length =
   F` and `≡ 0 (mod 64)`, `dir_offset ≥ 16`, `dir_length ≥ 4`,
   `dir_offset + dir_length ≤ F − 64`, `1 ≤ generation ≤ 2^63−1`, `file_id ≠ 0`,
   reserved `[56,60)` zero.

§6.2's reason for that ordering is stated and load-bearing: only the magic,
the version fields and the CRC "touch fields whose positions are fixed across
all majors (`[R-CNT-24]`)". So a major-7 file is rejected as a major, never as
corruption, and I do not read `dir_offset` out of a trailer whose layout I do
not know. §6.3's diagnostic SHOULD is the difference between a user deleting an
intact file and a user upgrading their reader.

**Step 3 — directory.** Fetch `[dir_offset, dir_offset + dir_length)`. What
bounds this range before I read it: the trailer CRC has verified
(`[R-ENC-05]` forbids acting on an unverified integer), and the four gates
above have confined the range inside `[16, F−64)` where F is the transport's
number. Verify the terminal 4 bytes against a CRC-32C over the preceding
`dir_length − 4` bytes (§7.1 `[R-CNT-11]`, row F20) *before any other use*.

**Step 4 — record walk.** Parse `[dir_offset, dir_offset + dir_length − 4)` as
zero or more 24-byte-header records with no residue (§7.2). Per record: type 0
is a validity error, never an unknown type (F24/L13); an unknown top-level type
with MU = 1 is reject-file and with MU = 0 is ignore-record (`[R-CNT-15]`);
extent-slot validity per `[R-CNT-13]` at the scope the record *governs* — file
for non-layer top-level records, layer for a layer record and for sub-records;
multiplicity per `[R-CNT-14]`; and for a top-level user-metadata record the
three framing rules §19.1 restates (no (0,0) slot, `extent_length ≥ 5`,
`inline_length = 1`). Then the layer-name namespace.

**Ordering question I had to settle.** For an *unknown* top-level record with
MU = 0 whose extent slot is malformed (say `extent_offset = 5`), two readings
compete: "ignore-record — the record is skipped as though absent" (§2.4), so I
never look at its slot; or `[R-CNT-13]`, whose text and whose register rows
F30/F31/F32 say "a non-layer top-level record's extent slot", with no
exemption for unknown types. The document decides this, and I record how,
because it took three passes: `[R-CNT-13]` itself says "For a record with
MU = 0, the extent slot is its only sanctioned reference to bytes outside the
record sequence … this is what lets a compactor relocate an unknown ancillary's
extent without parsing it" — the slot of an unknown record is explicitly a
thing tools read and act on. Combined with F31's detector (*reader*) and
detection point (*open*), and `[R-CNF-04]`'s bind to every reader-assigned row,
the answer is: validate the slot, reject the file. Not a finding.

### 2.2 The layer-name namespace

§19.1 step 4 puts three things at the open that I would otherwise have deferred:

- the name is parsed from the layer record's inline payload and checked against
  §4.6 — well-formed UTF-8 (L3), non-empty (L5), no U+0000–U+001F (L6), all
  three carrying *Detected: open* in §21.3;
- uniqueness is decided **first**, over raw name bytes, "whether or not each
  name is itself well-formed", because `[R-ENC-13]` makes comparison a byte
  comparison that needs no valid name. So two layers both named with the same
  ill-formed bytes are F4 (reject-file), not two L3s (reject-layer). That
  ordering is stated and I would have got it backwards without it;
- a layer record whose name field does not lie entirely within its
  `inline_length` "yields no name field to compare, so it contributes no name
  to the namespace and is instead a validity error at layer scope".

Note that the third item forces a containment decision at open even though the
row that governs it (L23) carries *Detected: layer access*. That is consistent
— §19.2 fixes the *latest* detection point and licenses earlier detection — but
it is worth writing down, because a reader that defers L23 wholesale cannot
build the namespace.

### 2.3 Byte-exact cold remote open

Against a server that honours ranged requests, with no speculation:

| # | Range | Bytes | What bounds it before it is read |
|---|---|---|---|
| 1 | suffix `bytes=-64` | 64 | nothing from the file; the response also carries F (`[R-CNT-10]`), so steps 1 and 2 of §19.1 cost one request between them |
| 2 | `[dir_offset, dir_offset+dir_length)` | `dir_length` | trailer CRC verified; `dir_offset ≥ 16`; `dir_length ≥ 4`; `dir_offset+dir_length ≤ F−64`; F transport-authoritative |

**Two requests, 64 + `dir_length` bytes, at any file size and layer count.**
Bytes `[0,16)` are *not* fetched: `[R-CNT-04]` makes the front-block check turn
on residency, not transport, and §6.4's accounting excludes it. For Appendix A's
file that is 64 + 4 = **68 bytes**. For the file I built in §5 below it is
64 + 109 = **173 bytes**, which my reader confirms:

```
requests(open): [(384, 448), (228, 337)]  bytes: 173
```

A reader that speculates a 64 KiB suffix instead issues **one** request; if the
window contains `[dir_offset, dir_offset+dir_length)` the second is
unnecessary (`[R-CNT-09]`), and if the window reaches offset 0 the front-block
equality check becomes mandatory. Appendix A works this through correctly for a
128-byte file, including the 112-byte window `[16,128)` that captures the
directory while leaving `[0,16)` non-resident. I checked that arithmetic: 128 −
16 = 112, and the window contains `[16,20)`. Correct.

A 200 response to a range request must be handled deliberately — abort, or
accept the full body — and never truncated to the requested length
(`[R-CNT-10]`). On a 128-byte file a 64 KiB suffix request will often come back
200, so this is not a hypothetical.

---

## 3. Validation timing by tier

§19.2 `[R-RDR-02]` gives four reader tiers plus *certification* for
verifier-detected rows. I mechanically audited every one of the 121 register
rows against them:

```
('reader',   'extent use')    9
('reader',   'layer access')  35
('reader',   'open')          32
('reader',   'open (top-level); layer access (sub-record)')  1
('reader',   'tile use')      24
('verifier', 'certification') 20
mismatches (verifier not at certification, or reader at certification): none
unexpected Detected values: none
```

Every verifier row is at certification and every certification row is a
verifier row. No row names a tier §19.2 does not define. I then checked the
coverage the other way:

- §19.1's four steps account for exactly the 32 reader/open rows (F1–F6, F8–F24
  minus the verifier ones, F29–F32, F34, F35, plus L3/L5/L6) and R1's
  top-level half.
- §19.3's enumeration accounts for exactly the 35 reader/layer-access rows.
  I walked its list against §21.3 row by row: slot validity → L15–L17; the §7.4
  constraint set → L20, L27–L31, L34–L36, L39, L43, L45; exact parse and
  sub-record walk → L13, L14, L19, L23, L24, L26; dimension/channel names →
  L4, L7–L9; user-metadata sub-record framing → L10–L12; field widths and u64
  domain → L1; the value sets → L31, L33, L34, L36, L43, L45; bool fill → L35;
  the lz4 declaration bound → L44; geometry floor and arithmetic → L32, L2; the
  no-I/O index cross-checks → L21, L22. Nothing left over in either direction.
- §19.4's steps account for the 24 reader/tile-use rows (T1, T3, T6–T12,
  T14–T25, and L37/L38 which take *layer* scope at a *tile-use* detection
  point — §19.2 states that inversion explicitly).

What a reader is permitted never to check: everything with detector *verifier*
— the coverage partition and slack total, extent overlap, record flag bits
(reserved bits, MU = 1 with PE = 0, a registered type's stored bits against
§7.3), the pre-trailer gap, reserved-range type values whatever their MU bit,
alignment and slab invariants, decoded padding content and pad bits,
interleaved boolean bytes, and user-metadata member ordering. §19.2 and
`[R-CNF-12]` between them say a reader that *does* detect one may reject.

What becomes a verdict when: nothing at the reader tier is a verdict — a reader
produces outcomes (reject-file / reject-layer / reject-tile / ignore-record),
not verdicts. Verdicts are §2.3's *conforming* / *nonconforming* / *cannot
establish*, and §2.3's repaired text fixes their precedence cleanly: an
established violation beats any number of unchecked requirements, so *cannot
establish* is available only to a traversal that established no violation, and
*unexamined* constrains the report rather than the verdict. I found no gap here.

One asymmetry worth naming, because it caught me: §2.4's `reject-layer` is
**prospective** — "it bars further service from the layer, and does not
retroactively invalidate content already returned under §19.2's validation
timing". So a segment-CRC failure at tile use (L38) does not oblige me to
retract samples I already returned from an earlier tile of that layer. §19.4
step 8 restates it. Without that sentence I would have had to buffer.

---

## 4. Layer access and the tile-read algorithm

### 4.1 Layer access (§19.3)

`[R-RDR-03]`: first access is any operation using a declaration other than the
name, and it performs **no fetch** — every check is decidable from the resident
directory and F. I verified that claim against the checks it names: the only
ones that look like I/O are `[R-CNT-17]`'s cross-checks, and both of them
(`entry_count` against the geometry-derived addressed-tile count, and
`extent_length` against `entry_count × 20 + ⌈entry_count/2^16⌉ × 4`) read only
the layer record. True as stated.

The inline payload parses in strict table order with no padding (§7.4
`[R-CNT-18]`): name, layout, linearization, codec, filter, A, S, A_slab, rank
d, channel count C, d dimension entries, C channel entries, index_encoding,
entry_count, crc_of_crc_array, then sub-records to the end with no residue.
A variable-length field's value includes its length prefix (§4.7's Note), which
is what makes the parse single-pass.

### 4.2 Ordinals

From §11.2 and §11.4:

- `G_i = ⌈E_i / T_i⌉`, computed as `E_i/T_i + (1 if E_i mod T_i else 0)`. §11.2's
  Note is right that the `(E+T−1)/T` idiom overflows the declared domain, and I
  used the stated form.
- `N = ∏ G_i`, `P = ∏ T_i`; addressed-tile count `N` interleaved, `C·N` planar.
- tile coords `t_i = x_i div T_i`, in-tile `u_i = x_i mod T_i`.
- in-tile ordinal `Σ u_i · ∏_{j>i} T_j` — row-major, for every linearization
  value, permanently.
- spatial ordinal `s = Σ t_i · ∏_{j>i} G_j` under linearization 1.
- disk ordinal `s` interleaved, `c·N + s` planar.
- empty product is 1, so `d = 1` reduces to `u_0` and `t_0`.

I checked §11.4's worked example: layer (y,x) extents (1024,2048) tiles
(256,256) → G = (4,8), N = 32, P = 65,536; coordinate (300,700) → tile (1,2) →
s = 1·8 + 2 = 10; in-tile (44,188) → 44·256 + 188 = 11,452; planar C = 4 channel
2 → 2·32 + 10 = 74. All correct. §15.4's companion example puts entry 74 at
region bytes [1,480, 1,500) — 20·74 = 1,480, correct — and channel 3's 32
entries at ordinals 96–127, correct.

### 4.3 Index chain

Region layout under index_encoding 1 (§15.1): `entry_count × 20` bytes of
entries, then `⌈entry_count/2^16⌉ × 4` bytes of segment CRCs, contiguous, no
padding. Entry k at region byte `20k`, 20 bytes: u64 offset, u64 length, u32
crc.

To use entry k (`[R-IDX-04]`), in dependency order:

1. fetch the **whole** CRC array at region `[20·entry_count, extent_length)` and
   verify `crc_of_crc_array` over it (L37 → reject-layer). The array must be
   fetched whole, not just the relevant u32, because `crc_of_crc_array` covers
   the whole array — §21.9's Note confirms this reading ("the segment-CRC array
   a reader fetches whole before using any entry");
2. fetch segment `s = k div 2^16`, covering entries
   `[s·2^16, min((s+1)·2^16, entry_count))`, and verify its CRC (L38 →
   reject-layer). The final partial segment's CRC covers only its actual bytes.

Both ranges are computable from the layer record alone and MAY be fetched in
parallel; §15.4's Note licenses caching the verification result under
committed-prefix immutability.

`[R-IDX-05]`'s `0xEECB3BB2` constant is a *writer* shortcut only: "Equality with
the constant licenses nothing for readers: verification is byte comparison of
computed CRCs, never constant matching." I record that because the obvious
optimisation — recognising an all-sentinel segment and skipping the CRC — is
explicitly forbidden, and L38 restates the prohibition in the register.

### 4.4 Entry classification (§15.3)

The table is total and unambiguous. Six rows are marked *structural* (I counted:
rows 2–7 — the sentinel-with-nonzero-crc row, the half-sentinel row, the
zero-length row, the offset-below-16 row, the bit-63 row, and the
overflow/past-F−64 row), which matches the text's "Six rows are marked
*structural*". The seventh reject-tile row — stored bytes failing the entry's
crc — is explicitly *not* structural: the entry is well-formed, its extent
stands, and it keeps its place in the verifier rows, in slab run continuity, and
in `[R-LIF-08]`'s coverage walk. `[R-IDX-02]` keeps `[R-ENC-03]`/`[R-ENC-04]`
off sentinel fields, so an all-ones sentinel is not itself a domain violation.

Overlap in classification is benign: an entry with `offset = 5, length = 0` hits
two rows, both structural reject-tile. No fork.

### 4.5 Payload, decode, extract

Fetch `[offset, offset+length)`, verify the entry's crc over the **stored** bytes
before decoding (§8.2 `[R-CNT-20]`, T1). Then §17.1: **codec first, then the
filter's inverse**. I note the asymmetry with the writer, which filters then
codes; §19.4 step 6 restates the reader direction, so there is no chance of
getting it backwards.

Decoded size is a function of declarations alone (`[R-SER-07]`), never of
payload content:

| Case | Decoded size | Offset of value k |
|---|---|---|
| interleaved | `P · Q`, `Q = Σ B_i` | `(k div C)·Q + F_{k mod C}`, `F_c = Σ_{j<c} B_j` |
| planar, numeric channel c | `P · B_c` | `k · B_c` |
| planar, bool channel | `⌈P/8⌉` | bit `k mod 8` of byte `k div 8`, LSB-first |

I verified §14.2's examples: tile extents (2,3), P = 6, channels a:uint8 +
b:uint16 → Q = 3, decoded size 18, ordinal 5 at bytes [15,18); planar b's tile
12 bytes with ordinal 5 at bytes 10–11; channels t:float32 + m:bool → Q = 5,
decoded size 30, ordinal 5 at [25,30) with the bool as the single byte 29. All
correct. §14.3's example: P = 10 alternating → byte 0 = `0x55`, byte 1 = `0x01`
with fill false, `0xFD` with fill true (pad bits 2–7 set). Correct.

§17.3's byte-shuffle: filtered places byte i of group j at `i·n + j`; the
inverse restores `i·n + j` to `j·s + i`. Stride is the channel element size for
a planar tile, Q for an interleaved tile, and **1 (identity) for a packed
boolean plane**. I checked `L` is divisible by `s` in all three cases: `P·Q / Q`,
`P·B_c / B_c`, `⌈P/8⌉ / 1`. §17.3's worked example — three float32 1.0/2.0/3.0
shuffling to `00 00 00 00 00 00 80 00 40 3F 40 40` — reproduces byte for byte
under my implementation.

Sentinel short-circuit (§19.4 step 4): a valid sentinel skips steps 5 and 6
entirely — no payload I/O — and every requested position of that tile reads as
fill: the entry's channel's fill in a planar layer, every carried channel's
fill in declared order in an interleaved layer. `[R-TYP-09]` is the rule I most
had to keep in front of me: fill is produced by **exactly one** condition, a
sentinel entry read from a *verified* chain. A malformed entry, a failed CRC
array or segment, or failed stored bytes never yield fill — they reject, and
`[R-CNF-09]` says a rejection is never satisfied by returning fill.

Padding positions are never returned (`[R-GEO-04]`), and their stored content is
fill by `[R-SER-05]` — which means a reader that forgets to clip observes fill
rather than garbage, but is still nonconforming.

---

## 5. Worked example — a real file, built and read

Appendix A's 128-byte file parsed cleanly and every annotation in its table
checks out (I re-derived the trailer CRC over `[0,60)` from the hex dump: 
`0xE00938D2`, matching `D2 38 09 E0` at [124,128)).

To exercise more of the reader I built a second file from §7.4's example layer,
with tile 0 actually stored. Layer `sst`, rank 1, dimension `x` E = 100 T = 32,
one interleaved float32 channel `temp` with fill `0x7FC00000`, codec 1, filter 1.

Derived: `G = [4]`, `N = 4`, `P = 32`, `Q = 4`, `entry_count = 4`,
`decoded size = P·Q = 128`, index region `4·20 + ⌈4/2^16⌉·4 = 84` bytes.
Inline payload came out **81 bytes** — exactly what §7.4's example states, with
the same field offsets (name [0,4), layout 4, linearization 5, codec 7, filter 9,
A 11, S 19, A_slab 27, rank 35, C 36, dimension entry [38,56), channel entry
[56,68), index_encoding 68, entry_count 69, crc_of_crc_array 77). §7.4's own
accounting — "4 + 34 bytes, the dimension entry 18, the channel entry 12, and
the trailing fixed fields 13 — 81 exactly" — adds up: 38 + 18 + 12 + 13 = 81.
The nine scalars from layout through channel count are 1+2+2+2+8+8+8+1+2 = 34.
The channel entry reproduces §12.3's twelve bytes
`04 74 65 6D 70 0C 00 04 00 00 C0 7F` byte for byte.

Placement:

```
front   [0,   16)   89 54 41 52 4E 0D 0A 1A + 8 zero bytes
tile 0  [16,  144)  128 bytes, 32 float32 values, codec 1 / filter 1
index   [144, 228)  4 entries (entry 0 stored, entries 1-3 sentinel) + 1 seg CRC
dir     [228, 337)  one layer record (24 + 81) + 4-byte CRC = 109 bytes
pad     [337, 384)  47 bytes of slack
trailer [384, 448)  F = 448, 448 mod 64 = 0
```

Checks: `dir_offset + dir_length = 337 ≤ F − 64 = 384`; `F` a multiple of 64;
`extent_length = 84` matches `[R-CNT-17]`'s formula. Computed CRCs: tile
`0xF8118D31`, segment `0xB76F7866`, `crc_of_crc_array 0x9F491382`, directory
`0x03AAC8CA`, trailer `0xC987F435`.

My reader's run:

```
requests(open):  [(384,448), (228,337)]        173 bytes, 2 requests
layers:          [b'sst']
layer decls:     layout 1, codec 1, G [4], N 4, P 32, Q 4, ec 4, nseg 1,
                 extent (144, 84)
tile0 requests:  [(224,228), (144,224), (16,144)]  212 bytes, 3 requests
x=0   stored 00000000 -> 0.0
x=5   stored 0000a040 -> 5.0
x=31  stored 0000f841 -> 31.0
x=40  fill   0000c07f
x=99  fill   0000c07f
```

Cold single-tile read cost, as §1 and §19.4 predict: the CRC array (4 bytes),
the segment covering the entry (80 bytes), and the tile (128 bytes) — three
requests, 212 bytes. Coordinates 40 and 99 fall in tiles 1 and 3, both
sentinel, and read as the recorded quiet NaN bit-exactly, with no payload I/O.
Coordinate 99 is the last real position; positions 100–127 of tile 3 are
padding positions that would carry the same fill bytes if the tile were stored,
and are never returned.

Slack total for this file: F − (16 + 128 + 84 + 109 + 64) = 448 − 401 = **47**,
which is the pad. §5.2's partial-total definition ("F less the bytes claimed by
the claimants the walk did enumerate") reduces to the exact total here because
the walk completes.

Other stated arithmetic I checked and found correct: §15.4's
entry_count = 1,000,000 example (16 segments, 15 full and one of 16,960; array
64 bytes; region 20,000,064 bytes; tile 999,999 at segment-relative byte
339,180; CRC array at [20,000,000, 20,000,064); segment 15 at [19,660,800,
20,000,000); a full segment 1.25 MiB); §20.3's `32·20 + 4 = 644`; §20.3's
"about 20 MB of index" for 10^6 tiles; §21.9's Note (2^32 entries → 2^16
segments → 256 KiB array; 2^36 → 4 MiB; 65,536 layers × ~200 bytes = 12.5 MiB);
§16.2's slab example (four runs, viewport rows 1–2 = ordinals 8–23 = runs 1 and
2); §14.5's edge tile (grid 2×2, 1 real position and 15 padding, 32 bytes at
uint16); §12.1's bfloat16 `0x3F80`; §4.6's `température` at 12 bytes NFC and 13
NFD; §17.2's Note that §14.2's examples give 18 and 30 bytes and §14.3's gives
2. Every one correct.

---

## 6. Degradation walks

**(1) Unknown record type, file scope, MU = 0, PE = 0.** The type is in neither
assigned value (§7.3). `[R-CNT-15]`: ignore-record. I still validate its extent
slot (F30/F31/F32 — see §2.1 above) and I still count its extent as a claimant
of the live state (§5.2: "a record extent … whatever the record's type"), but
§8.1 covers those bytes by **no checksum at all**, and I never read them. If
the type is from the experimental range the file is conforming (§21.6); if from
the reserved range the file is nonconforming but my behaviour is identical, the
detection being the verifier's (F36). Served: everything. This is the one
degradation where the *file's* status and *my* behaviour come apart, and the
document is explicit about it in three places.

**(2) Unknown codec.** `codec = 0x8000`. Detected at layer access (`[R-COD-03]`,
L43) → reject-layer. Every other layer serves normally; I may still list the
rejected layer's name (§2.4). I do **not** get to fall back to "treat as codec
1" — `[R-CNF-04]` forbids inferring values the specification does not define.
Note the contrast §17.4 draws: a *verifier* that cannot execute an assigned
codec reports *cannot establish*; a *reader* that cannot is simply not a
conforming reader, because all four codecs are core.

**(3) Unrecognized flag / enum value.** Three different answers, and I had to
keep them apart. An ignore-lane trailer bit (16–31): ignored, file conforming
(§6.3, §21.6). An incompat-lane bit (0–15): reject-file (F19). A reserved
`layout = 3`: reject-layer (L36) — §10.2 gives channel layout *no* experimental
range, so 3–255 are all reserved and all rejected. A reserved metadata
`encoding = 5`: **ignore-record**, and a violation (R1); an experimental
`encoding = 0x81`: ignore-record and **not** a violation (§21.6, `[R-MTA-10]`).
That last split is the only place in the document where the experimental range
of a space is conforming, and §21.5's header states the reason: `[R-MTA-10]`
withdraws the document's *content* rules, never the encoding byte's own value
set.

**(4) Truncated tail / torn commit.** Physical length exceeds
`committed_file_length`, or the last 64 bytes are payload rather than a
trailer. Either way I fail at step 2: F8 (magic) or F17 (length mismatch), both
reject-file. `[R-LIF-05]` forbids scanning backward, so I report the file torn
or invalid and stop. §9.5's Note is what told me not to look for a register row
for "residue past a completed commit": there isn't one, because the observable
state is already F8/F17. Recovery is a separate, deliberate tool operation
(§9.6) whose output must be re-verified whole, and §9.5's other Note licenses a
retry against attribute-cache staleness before concluding "torn".

**(5) Checksum mismatch, at each scope.** Trailer → reject-file (F14).
Directory → reject-file (F20). `crc_of_crc_array` or a segment CRC →
reject-**layer** (L37/L38), detected at tile use but scoped to the layer, and
prospective. A stored tile's crc → reject-**tile** (T1), and the other tiles of
the layer are unaffected. A user-metadata extent's crc → **ignore-record**
(R2), whatever the containing scope, because the document is quarantined
(`[R-CNT-25]`), and readers SHOULD report the loss. Four scopes, four blast
radii, from one primitive.

**(6) Limit exceeded.** A layer declaring `entry_count = 2^40` is conforming
(§21.9 states minimum guarantees, not caps) and exceeds the 2^32 guarantee, so I
MAY decline — at the *narrowest* scope whose declarations exceed what I can
serve, here the layer. `[R-ERR-04]` makes the report obligation sharp: a
refusal on resource grounds MUST be reported as a resource limit and never as a
validity error. For a `dir_length` above the 16 MiB guarantee the narrowest
scope is the whole file; for an over-large user-metadata document §18.2's Note
says the same, "a document having no declared size and so no narrower scope
whose declarations that rule can measure". A reader that declines a file every
one of whose quantities is inside the table is not conforming.

**(7) Format major version I do not implement.** reject-file on capability
grounds, with a diagnostic distinct from "not a TARN file" and from "corrupt"
(`[R-CNT-07]`). §21.6's closing paragraph is explicit that this is *not* a
register row and the file may be perfectly conforming under that major — one of
exactly two "conforming files a reader nevertheless refuses", the other being an
experimental-range record type carrying MU = 1.

**(8) Unimplemented MU = 1 record type, layer sub-record.** reject-**layer**,
never reject-file (`[R-CNT-18]`). Other layers stay readable. Contrast the
top-level case, which is reject-file — and note that for an *updater* the same
condition additionally bars every commit (§20.4's MU = 1 row).

---

## 7. Places I had to guess, and what settled them

Every one of these I did settle from the text; I list them because each cost me
a re-read and each is a place a less patient implementer diverges.

1. **Whether an ignored record's extent slot is still validated.** Settled by
   `[R-CNT-13]`'s "no embedded offsets" paragraph plus F30–F32's detector.
2. **Whether the whole segment-CRC array must be fetched.** Settled by
   `crc_of_crc_array`'s coverage and §21.9's Note.
3. **Codec-then-filter-inverse order on the read path.** Settled twice, §17.1
   and §19.4 step 6.
4. **Byte-shuffle stride for a packed bool plane.** Settled by `[R-COD-10]`'s
   explicit `s = 1, identity`; without it the "channel's element size" clause
   would have given `s = 1` anyway, but the plane's length is `⌈P/8⌉` rather
   than `P`, and I would have had to reason about divisibility myself.
5. **Which decoded size applies to a planar tile.** Settled by §14.1's "the tile
   with disk ordinal c·N + s carries exactly the values of channel c", so
   `c = k div N` selects the channel and its type selects §14.2 or §14.3.
6. **Whether `entry_count = 0` means fetching a zero-length CRC array.** Settled
   by §15.4's closing example: extent slot (0,0), nothing fetched, nothing
   verified.
7. **Whether a duplicate ill-formed layer name is F4 or L3.** Settled by
   §19.1's "Uniqueness is decided first … over the raw name bytes".
8. **What to return for an interleaved bool byte of `0x02`.** Settled by
   `[R-SER-08]`: if I neither detect nor reject, `0x00` is false and every other
   byte is true. This is the *only* byte in the format a reader resolves rather
   than passes through, and `[R-TYP-04]` and Appendix H both say so.
9. **Whether a segment-CRC failure retracts already-returned samples.** Settled
   by §2.4's prospective clause and §19.4 step 8.

Nothing in the reader path was left undetermined. That is the substantive
result of this walk: I could write the reader from this document alone, and the
two findings below are both about the register's corpus arithmetic and one
non-normative example, not about a byte a reader emits or accepts.

---

## 8. Register audit

Mechanical count over the four register tables:

```
rows: 121   instances: 268
F: 36 rows / 56 instances     L: 49 rows / 111 instances
T: 26 rows / 57 instances     R: 10 rows / 44 instances
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10, and §21.8 says
"121 conditions over 268 instances". All five numbers reproduce exactly under
§21.1's stated counting rule ("Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written"). The totals are internally consistent.

I then audited §21.1's *completeness* claim from the other direction — walking
the requirement identifiers and asking which have no row — and found the
account holds. `[R-CNT-23]`'s constraint table maps field by field onto
L1/L3/L5–L9/L20/L27–L36/L39/L43/L45. `[R-ERR-05]`'s hard limits each have a row
or are unrepresentable (a name longer than 255 bytes cannot be written through
a u8 prefix). §21.7's second paragraph correctly names the five obligations
with no single-file witness. §16.2's Note correctly explains why `[R-SLB-04]`
has no row of its own. I found nothing missing.

I also checked §10.2's value-space table against each defining section
(record type, channel layout, linearization, sample type, codec, filter, index
encoding, metadata encoding) and against Appendix C's snapshot: all eight rows
agree in all three places, including the two spaces with no experimental range.
L31/L33/L34/L36/L43/L45's instance cells reproduce each space's own
sub-partition (L33 splits reserved 2–3 from reserved 4–0x7FFF because §11.4
does; L34 splits 14–19 from 20–0x7FFF because §12.2 does; L36 has no
experimental instance because channel layout has no experimental range). That
discipline is carefully applied — which is what makes Finding 1 stand out.

---

## Findings

### reader-01 — AMBIGUITY — §21.1's second instance axis is applied to the tile-scope rows and not to F17, L21, L22 or L30

**Location:** §21.1 (the Instances criterion); §21.2 row F17; §21.3 rows L21,
L22, L30. Requirement IDs: `[R-ERR-02]`, `[R-ERR-01]`; the rows' governing
rules `[R-CNT-06]`, `[R-CNT-17]`, `[R-CNT-23]`.

**The text complained about.** §21.1:

> Two axes recur often enough to be stated rather than judged each time. Where
> the quantity a condition derives varies by layout, the layout formulas are
> materially different shapes and the cell enumerates them. Where the condition
> compares two quantities and either can be the greater — a *differs from* or
> *does not equal* — the two directions are likewise enumerated; where its own
> text bounds the comparison in one direction — an *exceeds*, a *larger than* —
> there is one.

Row F17, whose Instances cell reads `committed_file_length` (one instance):

> Trailer committed_file_length does not equal the transport-authoritative file
> size (physical file not truncated or extended to it)

Row L21, whose Instances cell reads `interleaved N; planar C·N` (two instances):

> entry_count does not equal the geometry-derived addressed-tile count (N
> interleaved, C·N planar)

Row L30, whose Instances cell reads `—` (one instance):

> A channel entry's fill length prefix differs from the element size of the
> channel's declared type

Row L22, whose Instances cell reads `extent_length against the formula; slot
(0,0) with entry_count > 0; a nonzero slot with entry_count = 0` (three
instances):

> Under index_encoding 1, extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉
> × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with
> entry_count = 0

**Detail.** §21.1 states two independent instance axes as mechanical rules
rather than judgement calls. The *layout* axis is applied consistently
everywhere I checked (T3, T14, T21, T22, T4, T26, L44, L21). The *direction*
axis is applied at T3 ("is not exactly" → six instances = three layouts × two
directions), T14 ("differs from" → six), and T22 ("does not equal" → six), and
at L39/L29 (which spell the directions as `A below 512` / `A above 2^62`) and
L41 (which spells them as `gap` / `overlap`). It is **not** applied at:

- **F17**, whose condition text names both directions in its own parenthetical
  — "not truncated or extended to it" — and whose cell gives one instance. A
  physical file longer than `committed_file_length` (residue from a torn or
  un-truncated append, the exact state §9.5's Note discusses) and one shorter
  (a truncated transfer) are two distinguishable files with materially
  different operator remedies.
- **L21**, which applies the layout axis (two instances) and not the direction
  axis. `entry_count` above the geometry-derived count and below it are two
  distinguishable files, and the over-declaring direction is the hostile one
  §22.2's Note is about ("The index is the cheapest hostile amplifier").
- **L22**, whose first alternative is a `≠` against a formula; `extent_length`
  longer and shorter than the formula are two distinguishable files.
- **L30**, which uses the criterion's own trigger phrase *differs from*,
  compares two magnitudes either of which can be the greater (a fill length
  prefix of 3 or of 5 against a float32's element size of 4), and gives one
  instance.

Permitted readings: (a) the direction axis is universal as §21.1 states it, in
which case these four cells under-enumerate and §21.8's "268 instances" is short
by five; (b) the direction axis applies only where the layout axis also applies,
which is what the four cells collectively behave as if it does — but that
reading is refuted by L21, which applies the layout axis and *not* the direction
axis in the same cell, and by L39/L29/L41, which apply the direction axis with
no layout involvement.

I picked (a): §21.1 states the axes as independent and unconditional, and its
whole purpose is that "the count is therefore mechanical once the cell is
written". Under (a) the four cells are the defect and the four rows should read
2, 4, 4 and 2 instances respectively, with §21.8's total becoming 273.

**What an implementer does wrong without it.** Nothing to a byte — but a corpus
builder does. `[R-ERR-02]` promises "one vector per instance" and `[R-VEC-03]`
inherits that as the corpus's own obligation. Under reading (b) a corpus ships
268 vectors and has no vector for a file whose physical length *exceeds*
`committed_file_length` — the residue case, which is a distinct real-world
failure with a distinct remedy — nor for an `entry_count` that under-declares,
nor for a fill prefix longer than its element size. A verifier author checking
their tool against the corpus would get a green light on a build that mishandles
whichever direction the corpus omitted.

**Byte-level: no.** §21.1 already decides which text governs where a row and its
rule diverge, and here the rows' *conditions* are correct in every case — only
the Instances cells and §21.8's total are at issue. Both directions of each
condition take the same detector, the same detection point and the same outcome,
so no two readers or writers can disagree about a byte or a verdict. What is
decided is the corpus build list, not the format.

---

### reader-02 — CONTRADICTION — §20.3's example (c) bars a fill change that §20.3's own step 4 permits

**Location:** §20.3, `[R-WRT-04]` step 4, against the Example "the three shapes
a commit takes", branch (c). Requirement IDs: `[R-WRT-04]`, `[R-SER-05]`,
`[R-GEO-04]`.

**The text complained about.** Step 4, normative:

> A commit MUST NOT change a layer's declarations in a way that alters, **for
> any tile that layer stores**, what §14 fixes for its stored bytes or how they
> decode — the set of padding positions (§11.3) and the content `[R-SER-05]`
> fixes there, the decoded size, the byte offset of any sample within the
> decoded tile image, or the codec and filter that produced the stored bytes.

and, four sentences later, still in step 4:

> A layer that stores no tile MAY be re-declared freely, which is what
> schema-first creation needs (§11.1)

against the Example, branch (c):

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no
> padding position and no pad bit. Only the directory is re-emitted. A fill
> change on a layer carrying either is not an appender's operation at all
> (step 4): it would invalidate every stored tile it reaches.

**Detail.** The normative test in step 4 is keyed to *tiles the layer stores*.
The Example's test is keyed to whether the layer *carries* a padding position or
a pad bit — and "carrying" a padding position is a property of geometry alone
(§11.3: padding positions exist wherever `G_i · T_i > E_i`), independent of
which tiles are stored. The two tests disagree on a whole class of layers.

Concretely: a layer with extents (5,5) and tile extents (4,4) has, by §14.5's
own worked example, 15 padding positions in its edge tile. Suppose the commit
finds that layer with only tile (0,0) stored — an interior tile with no padding
position — or with no tile stored at all. Step 4 permits the fill change: it
alters nothing §14 fixes for any tile the layer stores, and in the
stores-nothing case step 4 says outright that the layer "MAY be re-declared
freely". The Example says the change "is not an appender's operation at all".

The Example's own justification undercuts its assertion: "it would invalidate
every stored tile **it reaches**" is conditional, and when it reaches none, the
absolute clause before it does not follow.

Permitted readings of "a layer carrying either": (a) a layer whose geometry
yields padding positions or pad bits — the natural reading of "carrying", and
the one that makes the Example's first sentence ("on a layer with no padding
position and no pad bit") a meaningful qualifier — which contradicts step 4;
(b) a layer that *stores a tile which* carries a padding position or a pad bit,
which agrees with step 4 but is a strained reading of the words and makes the
Example's qualifier redundant with step 4's own test.

I picked (b) for my own implementation notes, because §2.1 makes the Example
non-normative and step 4 governs, but I would not have arrived there without
noticing the collision — and an appender author reading branch (c) as the
practical summary of step 4 (which is what the branch is for) lands on (a).

Note also that pad bits behave differently from padding positions under reading
(a): pad bits exist only in a packed planar bool plane with `P mod 8 ≠ 0`, and
every *stored* such plane carries them — so for pad bits the two readings
coincide whenever any bool plane is stored, and diverge only when none is. The
Example's "either" flattens two mechanisms §14.3's own Note is at pains to keep
apart ("Pad bits are not padding positions (§11.3)").

**What an implementer does wrong without it.** An appender refuses an operation
the format permits — the schema-first workflow §11.1's Rationale and §20.3's
own "re-declared freely" clause exist to enable. A tool that declares layers at
creation with an edge-padded geometry and then, before any data arrives, wants
to correct a fill value chosen by default (`[R-TYP-10]` records all-zero bytes
when the caller chooses none) is told by branch (c) that its only route is a
whole-file rewrite under a fresh `file_id`. That is the exact cost §20.3 says
the rule exists to avoid.

**Byte-level: no.** §2.1 settles it: the Example is labelled *Example* and
carries no normative force, and step 4 states the governing test twice in
compatible terms. Two appenders following the document as a whole emit the same
files; only an appender that reads branch (c) as the operative rule emits fewer.
Because the disagreement is about which conforming files a writer chooses to
produce — never about which byte sequences a reader must accept or reject, and
never about the content of any file either writer does produce — I do not claim
a byte-level fork.

---

## 9. Confidence

**Medium-high.** I could implement a conforming reader from this document
alone, end to end, and I did: open, tier the validation, walk the index chain,
decode, extract, and degrade in eight distinct ways, with no place where the
text left me to guess. Every constant, offset, CRC and count I could check
reproduced — twenty-plus of them, including the two CRC constants nobody
computes by hand. The register is complete and internally consistent at 121
rows and 268 instances, its Detector/Detected columns are clean, and §19.1's
and §19.3's enumerations account for exactly the rows their tiers own.

The two findings are both in the changed surface, both are hygiene rather than
mechanism, and neither forks a byte. I did not find a defect in the reader's
mechanism, and I want to be explicit that this is a claim about my walk rather
than about the document: the areas I probed hardest were the open path, the
index chain, the decoded-byte arithmetic, and the register's counting rules.
The areas I probed least were the compactor's obligations under `[R-WRT-07]`
(one question I noted and did not pursue: what a compactor writes for an index
entry §15.3 classifies reject-tile on a structural ground, since such an entry
is neither a sentinel to copy nor a stored extent to re-point — §20.5's "MUST
refuse to compact when any check `[R-WRT-09]` obliges fails" appears to answer
it, but by implication rather than directly), and the corpus construction rules
of §24 beyond checking that `[R-VEC-04]`'s intact-sibling requirement is
constructible for each outcome class.
