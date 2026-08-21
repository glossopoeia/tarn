# Cleanroom round 16 — Reader implementer transcript

## Disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read in full in five `Read` calls (lines 1–400, 400–850, 850–1300, 1300–1750,
1750–2200, 2200–2650, 2650–3100, 3100–3548, 3548–3947, 3947–4282) plus targeted
`sed`/`grep` re-reads of §6.1, §11.1, §20.3, §20.5 and §21.7.

I opened no other file. No `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`,
`README.md`, no `conformance/`, no `spec/registry.json`, no prior-round findings,
no git history (`git log`/`git diff` never run), no web fetch, no web search. I
did not list the output directory and did not read any other agent's transcript.

I ran local Python that reads no project file, in my own scratchpad:
- a CRC-32C implementation (Castagnoli, reflected, init/final 0xFFFFFFFF) checked
  against §4.5's check vector;
- a builder that emits two complete TARN files from scratch;
- a conforming reader written only from §19, §7, §14, §15, §17;
- twelve degradation mutations of the first file;
- a two-generation witness for the §21.7 finding;
- a script that counts §21's register rows and instances by parsing the four
  tables out of the markdown (this reads `spec/tarn.md` only).

Prior knowledge of other array/image formats was used only to generate
suspicions; every conclusion below is settled against the document.

---

## Part 1 — Constants and arithmetic I could check

Before writing any code I checked every stated constant, offset and checksum I
could compute. All of them are correct.

| Claim | Location | Result |
|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5 | ✅ reproduced |
| CRC-32C(zero bytes) = `0x00000000` | §4.5 | ✅ |
| CRC-32C of a full 2¹⁶-sentinel segment = `0xEECB3BB2` | §15.4, App. B | ✅ (1,310,720 bytes of `FF×16 00×4`) |
| CRC-32C over four sentinel entries (80 bytes) = `0x80A34955`, stored `55 49 A3 80` | §7.4 example | ✅ |
| crc_of_crc_array of that 4-byte array = `0xC4EE982E` | §7.4 example | ✅ |
| Appendix A trailer CRC = `0xE00938D2` over trailer bytes [0,60) | App. A | ✅ reproduced from the hexdump |
| Appendix A field decode: vmaj 1, vmin 0, flags 0, gen 1, dir_offset 16, dir_length 4, cfl 128, file_id 0x0123456789ABCDEF, reserved zero | App. A | ✅ all match the annotation table |
| §7.4 layer-record inline payload = 81 bytes; field offsets 0,4,5,7,9,11,19,27,35,36,38,40,48,56,63,68,69,77 | §7.4 | ✅ my independent pack lands byte-for-byte identical through offset 77 |
| 4 + 34 + 18 + 12 + 13 = 81 | §7.4 | ✅ |
| extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84 | §7.4, `[R-CNT-17]` | ✅ |
| §11.2: G=(4,8), N=32, P=65,536; ⌈1000/256⌉=4 | §11.2 | ✅ |
| §11.4: tile(1,0)→8; (300,700)→tile(1,2), s=10, in-tile (44,188), ordinal 11,452; planar c=2 → 74 | §11.4 | ✅ |
| §14.2: Q=3, size 18, ordinal 5 at [15,18); planar `b` 12 bytes, ordinal 5 at 10–11; float32+bool Q=5, size 30, [25,30) | §14.2 | ✅ |
| §14.3: P=10 alternating → `55 01`; fill true → `55 FD` | §14.3 | ✅ |
| §14.5: extents (5,5)/tiles (4,4) → edge tile (1,1) has 1 real + 15 padding, 32 bytes | §14.5 | ✅ |
| §17.3: shuffle of `00 00 80 3F 00 00 00 40 00 00 40 40` (s=4,n=3) = `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | ✅ |
| §15.4: ec=1,000,000 → 16 segments (last 16,960), array 64 B, region 20,000,064 B; k=999,999 at segment-relative 339,180; array [20,000,000, 20,000,064); segment 15 [19,660,800, 20,000,000) | §15.4 | ✅ every figure |
| §15.4: planar C=4,N=32, disk ordinal 74 → entry [1,480, 1,500); channel-3 entries 96–127 | §15.4 | ✅ |
| §12.3: `04 74 65 6D 70 0C 00 04 00 00 C0 7F` (12 bytes) | §12.3 | ✅ |
| §12.1: bfloat16 1.0 = `0x3F80`, stored `80 3F` | §12.1 | ✅ |
| §4.6: `température` NFC 12 bytes, NFD 13 | §4.6 | ✅ |
| §20.3: 32·20 + 4 = 644; 10⁶ tiles ≈ 20 MB index | §20.3 | ✅ |
| §21.9 note: 2³²/2¹⁶ × 4 = 256 KiB; 2³⁶ → 4 MiB | §21.9 | ✅ |
| §21.8: "121 conditions over 275 instances" | §21.8 | ✅ — mechanical count of the four tables gives F=36, L=49, T=26, R=10 (=121) and, under §21.1's counting rule (a `—` cell is one instance; otherwise semicolon-separated), exactly 275 |

The §21.8 count is worth calling out: it is the kind of number that rots
silently, and it is exactly right, as are §21.2's "36", §21.3's "49", §21.4's
"26" and §21.5's "10".

I also machine-checked every `§N.M` cross-reference against the heading set:
**no dangling section references**. And every `[R-XXX-NN]` identifier: 161
distinct, with `[R-ENC-100]` (the §2.2 illustration) and `[R-SER-04]` (the
withdrawn one) as the only two never used as governing rules — both correct.

---

## Part 2 — The open path, built and costed

I wrote an actual reader (`reader.py`) whose transport logs every range it
issues, then built a file from scratch to open with it.

### File `one.tarn` — the layer of §7.4's example, with one tile stored

Geometry: rank 1, dim `x`, E=100, T=32 → G=(4), N=4, P=32. One interleaved
float32 channel `temp`, fill `0x7FC00000`. Codec 1, filter 1, no alignment, no
slab. entry_count = 4 (§11.2's addressed-tile count for an interleaved layer).
Decoded size = P·Q = 32·4 = **128** bytes (§14.2). Tile 0 stores the float32
values 0.0 … 31.0; tiles 1–3 are sentinels.

Placement (chosen freely under `[R-SLB-05]`):

```
[0,16)      front signature block          89 54 41 52 4E 0D 0A 1A + 8 zero
[16,144)    tile 0 stored extent           128 bytes, crc 0xF8118D31
[144,224)   index entry array              4 × 20 bytes
[224,228)   segment CRC array (1 segment)  0xB76F7866
[228,337)   directory region               1 layer record (24+81) + 4-byte CRC
[337,384)   pre-trailer pad                47 bytes of slack
[384,448)   trailer                        F = 448, 448 mod 64 = 0
```

crc_of_crc_array = CRC-32C(`66 78 6F B7`) = `0x9F491382`. Coverage (§5.2)
partitions: front block, four structures, one 47-byte slack run, no overlaps,
every claimant inside [16, F−64) = [16, 384). `dir_offset + dir_length = 337 ≤
384` ✔ (`[R-CNT-06]`).

### The cold remote open, byte-exact

Against a ranged-request server, **two requests, 173 bytes**:

| # | Range | Bytes | What bounds it before it is read |
|---|---|---|---|
| 1 | suffix `bytes=-64` → [384,448) | 64 | Nothing in the file. The suffix form needs no prior knowledge, and its response carries the transport-authoritative F (`[R-CNT-10]`, §6.4). §19.1 folds steps 1 and 2 into this one request. |
| 2 | [228, 337) | 109 | `dir_offset` and `dir_length` from the trailer, both covered by the trailer CRC verified in request 1 — which is what `[R-ENC-05]` demands before any seek or fetch. |

That is `64 + dir_length`, at any file size and any layer count
(`[R-RDR-01]`). The 128-byte Appendix A file costs `64 + 4 = 68`.

Order inside request 1, per `[R-CNT-06]`, and I checked I could not reorder it:
magic → CRC → version gate → **then** everything else. The gate ordering is why
§21.2 can say a foreign-major file never reaches the geometry rows. I verified
the front-block rule is about *residency* and not transport: on this file a
64-byte suffix window leaves [0,16) non-resident, so §6.1 lets me skip the
equality check; a whole-file read or an mmap makes it mandatory and *first*.

### The tile read, byte-exact

`read(x=5)` — coordinate 5 → tile coordinate 0, in-tile ordinal 5, spatial
ordinal 0, disk ordinal 0 (interleaved). **Three requests, 212 bytes**:

| # | Range | Bytes | Bounded by |
|---|---|---|---|
| 3 | [224, 228) | 4 | `extent_offset + entry_count×20` and `⌈entry_count/2¹⁶⌉×4`, both from the directory-CRC-covered layer record (§15.1) |
| 4 | [144, 224) | 80 | segment 0 = entries [0, min(2¹⁶, 4)) (§15.4); may run in parallel with #3 |
| 5 | [16, 144) | 128 | the entry's own offset/length, covered by the segment CRC, itself covered by crc_of_crc_array, itself covered by the directory CRC |

The chain of trust in §8.2 is exactly the order I had to write:
trailer → directory → crc_of_crc_array → segment CRC array → segment → entry →
stored tile. Nothing in it required an integer whose covering checksum I had not
already verified, which is `[R-ENC-05]` holding in practice rather than in
principle. `read(x=40)` (tile 1, sentinel) costs **zero payload I/O** and returns
`00 00 C0 7F` — the recorded fill, bit-exact (`[R-TYP-06]`, `[R-TYP-08]`).
`read(x=150)` fails as a request with no verdict on the file (§19.4 step 1).

### File `two.tarn` — planar, mixed types, byte-shuffle

To exercise the paths `one.tarn` does not, I built a second file: **planar**,
rank 2, dims (y:5, x:5) tile extents (4,4) → G=(2,2), N=4, P=16; channels `t`
(float32, fill +0.0) and `m` (bool, fill true); **filter 2** (byte-shuffle);
codec 1. Addressed-tile count = C·N = **8** (§11.2). Decoded sizes: `t`'s plane
P·Bᶜ = 64 bytes (§14.2), `m`'s plane ⌈P/8⌉ = **2** bytes (§14.3). Disk ordinals
0–3 are `t`'s tiles, 4–7 are `m`'s (channel-major, `[R-GEO-06]`). Stored: 0, 3,
4, 7; the rest sentinel. Shuffle strides: 4 for `t`'s planes, **1 (identity)**
for `m`'s packed planes (`[R-COD-10]`).

Edge tile 3 (tile coordinates (1,1)) covers y,x ∈ 4..7 — one real position
(4,4), fifteen padding positions, which I fill-encoded per `[R-SER-05]`; its
bool counterpart (ordinal 7) is `FF FF`, the real value true plus fifteen
fill-true padding bits.

Read-back through the reader:

| coordinate | tile / disk ordinal | result |
|---|---|---|
| (0,0) | spatial 0 → disk 0 and 4 | t = 0.0 stored, m = true stored |
| (1,2) | in-tile ordinal 1·4+2 = 6 | t = 6.0, m = true (bit 6 of `0x55…`) |
| (4,4) | spatial 3 → disk 3 and 7 | t = 99.5 (the one real position of the edge tile), m = true |
| (0,4) | spatial 1 → disk 1 and 5, both sentinel | t = fill, m = fill — a whole sample filled |
| (4,0) | spatial 2 → disk 2 and 6, both sentinel | fill |
| (5,0) | — | request fails, no verdict on the file |

Everything resolved from the document. §14.4's Note ("a single-channel bool layer
does not [produce byte-identical images under either layout]") is the passage
that settles what a reader returns for a bool sample read out of a packed plane:
the reference array is layout-independent, so the value returned is the logical
false/true whose canonical encoding §13.2 and §14.2 fix as the byte `0x00`/`0x01`
— not a bit. I had to triangulate that from §12.1 (element size 1), §13.2 (fill
byte), §14.2 (interleaved byte) and §14.4's Note rather than read it in one
place, but it resolves uniquely and I do not file it.

---

## Part 3 — Validation timing by tier

Building the reader forced me to place every check at a tier. §19.2's four tiers
and §19's preamble ("A row this section does not restate is due at its own tier
all the same") between them decided every one; I never had to invent a tier.

**At open** — front block *if resident* (`[R-CNT-04]`); trailer in §6.2's fixed
order; directory CRC; the whole record walk, including the extent-slot rules for
non-layer top-level records, the user-metadata framing trio (no (0,0), extent
≥ 5, inline_length = 1), the multiplicity rules, the MU gate for unknown types,
and the layer-name namespace. Two things I had to look up and found stated:

1. **An ignored record's extent slot is still checked.** `[R-CNT-15]` says an
   unknown MU = 0 top-level record is "skipped as though absent", which reads
   like "do not look at it". §19.1 step 4 settles it the other way — the slot
   rules apply to non-layer top-level records — and F30/F31/F32's condition text
   ("A *non-layer top-level record's* extent slot…") confirms. So a malformed
   slot on an ignored record is reject-file. Determined, not a guess.
2. **A layer record whose name field does not fit contributes no name.**
   §19.1 step 4 states it explicitly, and states that uniqueness is decided
   *first*, over raw bytes, "whether or not each name is itself well-formed".
   That is exactly the ordering question I would otherwise have had to guess:
   two byte-identical malformed names are a duplicate (reject-**file**) rather
   than two independent reject-**layer**s.

**At first access to a layer** — §19.3's list. I implemented all of it and
found no check I needed that was not there: value sets for layout,
linearization, codec, filter, index_encoding, channel type; A/S exclusivity and
their power-of-two ranges; the A_slab-with-S=0 rule; fill length against element
size; the bool fill byte; name rules and per-namespace uniqueness for dimensions
and channels; the geometry floor; every derived product against 2⁶³ − 1;
`[R-COD-07]`'s lz4 cap; and the two index cross-checks (`[R-CNT-17]`).
Crucially, "layer access performs no fetch" — every one of those is decidable
from the resident directory and F, and I confirmed it by construction: my
`access()` issues zero transport calls.

**At use of a tile** — the index chain (`[R-IDX-04]`), the §15.3 classification,
`[R-COD-04]`'s pre-fetch length equality, the entry CRC, and the decode checks.
`[R-COD-04]`'s check is not restated in §19.4's eight steps; §19's preamble
covers that, and T14's *Detected* cell says "tile use". No ambiguity.

**At use of a record's extent** — the extent CRC and the document content rules,
"no earlier, since the open fetches no extent".

**What a reader is permitted never to check.** The verifier-detected rows:
coverage/overlap (F7, F33, L18), record flag bits (F25/F26/F28, L46/L47/L49),
member ordering (F27, L48), alignment and slab invariants (L40–L42), decoded
content (T2, T4, T5, T26), reserved-range type values (F36, L25). §21.1's
paragraph on verifier rows is what makes this safe to implement: for those rows
"the outcome names the scope at which the damage is recorded, not an obligation
on any reader", and for `[R-CNT-22]` and `[R-MTA-05]` the reader is positively
obliged to serve the structure unchanged. A reader that "helpfully" rejected an
unsorted metadata document would be the nonconforming party.

**What becomes a verdict when.** `[R-CNF-12]` lets a reader reject a
nonconforming file on detecting any violation, including a verifier's; §19.2
fixes only the *latest* detection point. So divergence between two conforming
readers is always toward earlier rejection, never toward silent acceptance —
which is the property that let me stop worrying about check ordering inside a
tier.

---

## Part 4 — Degradation walks

Twelve mutations of `one.tarn`, each run through the reader. Every one resolved
to a single outcome from the document.

1. **Unknown top-level record type 0x8123, MU = 0, extent (0,0).** Appended to
   the directory, directory CRC and trailer rebuilt. → Opens; the record is
   ignored; the layer still reads. Still served: everything. (`[R-CNT-15]`,
   §21.6's experimental-MU=0 row — the file is *conforming*, and §10.3's
   prohibition on publishing experimental values binds conduct, not bytes.)
2. **Same record with MU = 1.** → reject-file at open (`[R-CNT-15]`). Nothing
   served. Note this is one of §21.6's two "conforming files a reader
   nevertheless refuses": the diagnostic must say *capability*, not *corrupt*.
3. **codec = 5 (reserved).** → reject-layer at layer access (`[R-COD-03]`,
   L43). Still served: the file's layer list including this layer's name (§2.4),
   and any other layer.
4. **Truncated by 48 bytes.** → The final 64 bytes are not a trailer; magic
   fails; reject-file, reported as torn (`[R-LIF-05]`), and the reader MUST NOT
   scan backward. Still served: nothing. Recovery is §9.6's separate operation.
5. **One byte of the stored tile flipped.** → Open and layer access succeed;
   `read(x=5)` is reject-tile at the entry CRC (T1, `[R-CNT-20]`). Still
   served: every other tile — `read(x=40)` still returns fill. Fill is *not*
   substituted for the damaged tile (`[R-TYP-09]`, `[R-CNF-09]`).
6. **Sentinel entry with crc ≠ 0** (segment CRC and crc_of_crc_array
   recomputed so the index chain still verifies). → `read(x=5)` succeeds
   (0x40A00000 = 5.0); `read(x=40)` is reject-tile (T6). Exactly the blast
   radius §2.4 promises, and a good demonstration that `[R-IDX-02]`'s "all-ones
   is a reserved pattern" carve-out does not extend to the crc field.
7. **version_major = 7.** → Refused on capability grounds, before every gate but
   magic and CRC (§6.2's order, §21.2's opening paragraph). Not a finding about
   the bytes (`[R-CNF-02]`).
8. **Ignore-lane flag bit 20 set.** → Ignored; the file opens and reads
   normally; the file is conforming (§21.6).
9. **Incompat-lane bit 3 set.** → reject-file (`[R-CNT-08]`, F19).
10. **entry_count = 5 against a geometry-derived 4.** → reject-layer at layer
    access (L21, `[R-CNT-17]`). Detected without any I/O.
11. **Codec 1 with entry length 120 ≠ decoded size 128.** → reject-tile,
    *before the payload fetch* (T14, `[R-COD-04]`). The saving is real: the
    reader never issues request #5.
12. **Layer name bytes `FF FE FD`.** → reject-layer at open (L3, `[R-ENC-11]`).
    Other layers unaffected; §2.4 still permits listing the rejected layer.
    (My first implementation aborted the whole open here; §2.4 plus §19.1 make
    clear it must not — that is my bug, not the document's.)

Two more I traced on paper rather than in code, because they need a codec I did
not implement: a zstd payload whose first four bytes are not `28 B5 2F FD`
(T17, reject-tile, header-checkable) and a zstd frame declaring a window above
§21.9's 8 MiB guarantee on a small tile — which is *two different things* and
the document keeps them apart cleanly: a window above the *decoded size* is
T21, reject-tile; a window above 8 MiB with a large tile is conforming and
grounds for a **resource** refusal that `[R-ERR-04]` requires be reported as a
limit, not as corruption.

---

## Part 5 — Register cross-checks

I re-derived the file-scope row set independently from §6.2's field list, §7.1,
§7.2, §7.3 and §5.1 and got exactly §21.2's 36 rows with nothing left over and
nothing missing. Same exercise on §15.3 → §21.4: six *structural* rows in
§15.3's table, six structurally-marked outcomes, mapping onto T6–T12 with T1 as
the well-formed-entry/bad-bytes case, exactly as §15.3's paragraph says.

I also checked §21.1's instance criterion against every row that could exercise
it, since it is the kind of rule that decays asymmetrically:

- *differs from / does not equal* → two directions: T3 (6 = 3 layouts × 2),
  T14 (6), T22 (6), L21 (4 = 2 layouts × 2), L22 (2 directions + 2 named
  alternatives), L30 (2), F17 (2). ✔ uniform.
- *exceeds / larger than* → one direction: T21 (3 layouts), L44 (3 layouts),
  L2 (9 quantities, one direction each). ✔ uniform.
- checksum or constant comparison → no direction: F14, F20, T1, L37, L38 all
  one instance. ✔
- nonzero value tests → no direction: L27, L28 one instance each. ✔
- L39 and L29 both enumerate the ends of a range that the condition's own text
  states as a range, and they differ in exactly the way the ranges differ
  (A's floor is 512 so "A below 512" is a distinct alternative; A_slab's floor
  is 1 so only "A_slab = 0" is). ✔

I could not find an asymmetry. §21.1's two "axes stated rather than judged" do
what they claim.

One near-miss I decided **not** to file: under codec 1 the decoded payload is
the stored bytes (the filter preserves length), so every T14 witness is also a
T3 witness, and §21.1's specialization list ("F1 of F6 and of F8, F35 of F36,
L24 of L25") does not name T14 of T3. But the specialization rule exists to fix
*which detector and detection point apply*, and T3 and T14 share both
(reader / tile use), so the rule has nothing to settle there; §24's fallback
("the entry records every row the file exercises and says which it was built
for") covers the corpus question. Not a defect.

A second thing I checked and did **not** file: `[R-MTA-06]`'s "writers MUST NOT
emit a `tarn.`-prefixed key this specification's registry does not define"
against §21.6's "A user-metadata document carries an unrecognized `tarn.`-prefixed
key → **Conforming**". These look contradictory and are not: §2.3 declares
"which registry version a writer targets (§10.3, §18.3)" a conduct rule that
never makes a file nonconforming, and §18.3 is exactly that rule. Cleanly
handled.

---

## Findings

### reader-01 — CONTRADICTION — §21.7's "and nowhere else" is false: a decoded-size or codec change to a still-stored tile is witnessed by §21.4 rows that have nothing to do with structurally constrained bytes

**Location:** §21.7 (`[R-ERR-01]`); against §20.3 step 4 (`[R-WRT-04]`) and
§21.4 rows T14 (`[R-COD-04]`), T3 (`[R-SER-07]`), T17 (`[R-COD-06]`).

**Quotation** (§21.7):

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

**Against** (§20.3 step 4, the bar whose witnesses this describes):

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes.

**and** (§21.4, T14):

> Codec 1 (none) declared and a non-sentinel index entry's length differs from
> the tile's decoded size

**The witness, built and run.** Layer `L`: interleaved, rank 1, dim `x`
E = 100 T = 32 (G = 4, N = 4, P = 32), one channel `c`, codec 1, filter 1,
entry_count 4. Generation 1 declares `c` as **uint8**: decoded size = P·Q = 32,
and tile 0 is stored with a 32-byte extent. Tile 0 covers coordinates 0…31 of an
extent of 100, so it has **no padding position**; the layer is interleaved, so
there is **no pad bit**; the channel is not bool, so there is **no boolean
byte**. Generation 2 changes `c` to **uint16** and carries tile 0's index entry
forward byte-identically at ordinal 0 (which `[R-WRT-04]` step 4 requires of
every entry the commit does not change). §20.3 step 4 bars this commit: tile 0 is
stored in the superseded generation, and the change alters its decoded size,
which is the third item in the bar's own list.

Per §21.7 there is no witness — the change reaches none of the three byte kinds
it enumerates. But the resulting file is loudly nonconforming: decoded size is
now 64, the entry's length is 32, and `[R-COD-04]` makes that a validity error
at tile scope *checkable before any payload fetch*. My reader rejects the tile
at exactly that point:

```
  gen1: decoded_size=[32], entry0 length=32   read x=5 -> ('stored', b'\x11')
  gen2: decoded_size=[64], entry0 length=32   read x=5 -> REJECT tile:
        T14: codec1 length != decoded size [R-COD-04]
```

The same holds under codecs 2–4 with T3 (`[R-SER-07]`, decoded payload length ≠
decoded size), and for the bar's fourth item — "the codec and filter that
produced the stored bytes" — a change from codec 1 to codec 3 leaves raw bytes
where a zstd frame must be, witnessed by T17 on the frame magic. Three of the
bar's four listed effects are witnessed outside the three byte kinds §21.7
names; only the second (sample byte offset within a fixed decoded size, e.g. a
channel reorder) is genuinely unwitnessed.

**Permitted readings.** (a) "a byte §14 structurally constrains" is a closed
enumeration, glossed by the three items after the dash — the natural reading,
and the reading the "and nowhere else" clause requires to be doing work. Under
it the sentence is simply false. (b) "byte" is read loosely as "anything §14
fixes about the tile's bytes, including how many there are" — under which the
sentence is true but its gloss is wrong, since a decoded size is not one of "a
padding position, a pad bit, or a boolean byte". I picked (a).

**What an implementer does wrong without it.** §21.1 makes §21.7 normatively
"the account, by class, of what fails [detectability]", and a verifier author
reading it concludes that a declaration change reaching a still-stored tile is
undetectable unless it touches padding, pad bits or booleans — and so does not
look. That does not in fact loosen the verifier, because T3, T14 and T17 are
reader-detected rows it must check anyway. So the damage is to the document's
account of itself rather than to any verdict — but the account is the thing
§21.1 points at when it explains why the bar carries no register row of its own,
and the explanation given is not the true one.

**Adjacent, and not filed separately:** §21.7's second paragraph enumerates the
obligations omitted from the register for want of a single-file witness and
names `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`/`[R-SER-01]`, `[R-CNT-13]`,
`[R-CNT-18]`, §20.3 step 4 and `[R-ENC-06]`. It does not name §20.4's updater
family — `[R-WRT-05]`'s byte-identical re-emission and `[R-WRT-08]`'s
no-re-encode rule are equally properties of a file's history that §9.7 does not
reconstruct. That list carries no exclusivity marker, so I treat it as
incomplete rather than false and do not file it.

**Byte-level: no.** T3, T14 and T17 are reader-detected rows with their own
governing rules; every implementation must apply them regardless of what §21.7
says about them, so no accept/reject verdict and no emitted byte turns on
resolving this.

---

### reader-02 — CONTRADICTION — §20.3 step 4 states the declaration-change bar in the prior generation's tense and then, three paragraphs later, permits the same escape in the new state's tense

**Location:** §20.3 step 4 (`[R-WRT-04]`), both the bar and the shrink
paragraph; corroborated by §11.1's Rationale.

**Quotation** (§20.3 step 4, the bar's tense clause):

> The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so a commit does not escape this by unstoring in the same breath:
> superseding every tile of a layer and re-declaring it are one operation, and
> this bars it.

**Against** (§20.3 step 4, the shrink paragraph):

> but where it drops a tile out of the addressed set entirely (§11.2's grid
> count falls), nothing is altered for a tile the new state stores, and the
> commit is permitted

**And** (§11.1's Rationale, restating the same rule):

> a shrink is barred wherever it alters what §14 fixes for a tile the new state
> still stores, and permitted where it drops tiles out of the addressed set,
> whose extents then become slack

**The fork.** Take the same layer as reader-01: four tiles, all stored, channel
`c` uint8. One commit does two things: shrinks dim `x`'s extent from 100 to **0**
— which `[R-GEO-02]` expressly permits ("A dimension with extent 0 is valid") and
which drops the grid count to 0, de-addressing all four tiles — and re-declares
`c` as uint16.

Under the tense clause, all four tiles are stored in the generation this commit
supersedes; the change alters their decoded size; and de-addressing them is
precisely "unstoring in the same breath" — §3.1 makes a tile with no index entry
not stored, exactly as a sentinel does. So the commit is **barred**.

Under the shrink paragraph, every tile is dropped out of the addressed set, the
new state stores no tile, "nothing is altered for a tile the new state stores",
and the commit is **permitted** — after which "A layer that stores no tile MAY be
re-declared freely" and a second commit grows the extent back to 100.

The two routes leave *the same* live state and *the same* slack: a layer whose
declarations changed, storing none of the prior generation's tiles, with those
tiles' payload bytes left behind as slack. The bar names one of them and the
shrink paragraph names the other, and the underlying situation is
indistinguishable.

**Permitted readings.** (a) The tense clause governs throughout; the shrink
paragraph's "a tile the new state stores" is a slip, and a shrink that
de-addresses stored tiles while changing declarations is barred (a
shrink that changes *nothing else* stays permitted, since de-addressing alone
alters nothing §14 fixes for bytes that remain stored-tile bytes). (b) The shrink
paragraph is a deliberate exception carved out of the bar, in which case the
tense clause's flat "this bars it" is over-broad and the difference between
sentinel-unstoring and shrink-unstoring is load-bearing but nowhere argued.
I picked (a), because the tense clause is the one that says what it is doing and
why, and §11.1's Rationale is non-normative under §2.1 and so cannot decide it.

**What an implementer does wrong without it.** An appender author implementing
(b) will accept "shrink to zero, re-declare, grow back" as a supported way to
change a layer's channel types in place. An author implementing (a) will refuse
it and direct the caller to a new layer or a whole-file rewrite. Callers of the
two see different capabilities from the same specification.

**Byte-level: no.** Both routes produce *conforming* output files: the live
state each leaves violates no §21 row, and §21.7 already concedes that "a commit
that supersedes every tile it would have damaged leaves the live state clean, so
the bar is unwitnessed there". No reader or verifier can distinguish the two
outputs, and the set of conforming byte sequences a writer may reach is
unchanged — reading (a) only forces a second commit to reach the same bytes. The
divergence is in which single operations a writer will perform.

---

### reader-03 — OBSERVATION — `[R-CNT-04]` places a normative MUST on a "content sniffer", an actor §2.3 does not define and §2.1's phrasing discipline does not admit

**Location:** §6.1, `[R-CNT-04]`; against §2.3 and §2.1's Note.

**Quotation** (§6.1):

> A reader whose open leaves bytes [0, 16) **resident** — a local file read
> whole, a memory mapping, a speculative suffix window that reached offset 0, or
> any transport already holding them — and a content sniffer MUST verify the
> full block by byte equality before other processing, and MUST treat any
> mismatch as reject-file.

**Against** (§2.1's Note, which fixes the requirement grammar):

> every requirement names the actor it binds (writer, reader, updater, verifier,
> or file)

§2.3 defines exactly five conformance classes — conforming TARN file, reader,
writer, updater, verifier. "Content sniffer" is not one of them, is not defined
anywhere in the document, and the phrase occurs exactly twice: here, and in the
Note eighteen lines later ("Content sniffers match the 16-byte front block by
equality — no other prefix of a conforming file is constant"), which is
non-normative under §2.1.

**Permitted readings.** (a) A content sniffer is a kind of reader, in which case
the clause is inert: a sniffer necessarily holds [0,16) resident, so the
residency clause already binds it and the conjunct adds nothing. (b) It is a
distinct actor, in which case the MUST binds a class this document neither
defines nor tests, no conformance verdict attaches to it, and the outcome it
assigns — **reject-file**, which §2.4 defines as "The file is not usable" — is
in any case the wrong vocabulary for the sniffer's actual question, which §6.3
distinguishes as "not a TARN file" rather than a file that is invalid. I picked
(a), because (b) makes the sentence unenforceable and because the Note treats
sniffing as a use of the constant rather than a conformance class.

**What an implementer does wrong without it.** Nothing about bytes. But an
implementer auditing against Appendix H's checklists cannot place this
obligation: no checklist has a row for it, and a reader author reasonably
concludes the conjunct is about someone else. The cost is that a normative MUST
in a §21.2-registered condition's governing rule (F1, F6 both cite
`[R-CNT-04]`) has a subject the conformance model cannot name.

**Byte-level: no.** Under either reading a *reader* holding [0,16) resident must
check by equality and reject on mismatch, and one that does not hold them may
defer or omit — which is what decides every actual accept/reject. Nothing about
the sniffer clause changes a verdict on any byte sequence.

---

### reader-04 — OBSERVATION — §20.5 negates the same option twice in one sentence, with the same citation, leaving the sentence's list of what a compactor cannot do internally redundant

**Location:** §20.5, `[R-WRT-06]`.

**Quotation** (§20.5, verbatim, one sentence):

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the
> output clean — and a record §20.4 does let it drop is no exception, dropping
> being available only where that table licenses it — nor re-emit it corrected
> (`[R-WRT-05]`).

The first and third members of the `neither … nor … nor` list are the same
prohibition ("re-emit the structure corrected" / "re-emit it corrected") with
the same governing citation. A `neither/nor` list is read as an exhaustive
enumeration of the closed options, so a reader must decide whether the third
member is a distinct case they have failed to distinguish. It is not: under
`[R-WRT-05]` a retained record is re-emitted byte-identically, so "corrected"
re-emission is one prohibition however the object is named.

**Permitted readings.** (a) An editing artifact — the third member is a
duplicate of the first and should be struck. (b) The third member's "it" refers
to the droppable record introduced by the intervening dash clause, making it a
narrowing of the first rather than a repeat. Either way the option set is:
refuse, or drop where §20.4's table licenses dropping. I picked (a); (b) makes
the member a strict special case of the first, which is still redundant.

**What an implementer does wrong without it.** Nothing, on the merits — the
compactor's options are recoverable from the sentence. But the same sentence is
the only place that resolves what a compactor does when it detects a violation
in a record §20.4 would let it drop, and a duplicated clause in exactly that
sentence is a signal that the intended enumeration was not finished. A compactor
author needs to read the dash clause as licensing "drop it, then the output
carries no violation" rather than as barring the drop; the sentence's rhetorical
frame ("is no exception") pushes the other way while its own justification
("dropping being available only where that table licenses it" — and for a
compactor the table licenses it unconditionally, "whenever it rewrites the file")
pushes back.

**Byte-level: no.** Both readings leave the compactor with the same two lawful
outcomes and the same set of emittable outputs.

---

## What I could not determine, and did not have to guess

Nothing in the open path, the tile-read algorithm, the validation tiers or the
degradation walks left me guessing. The places where I expected to guess and did
not:

- the width in which a bool sample read from a packed planar plane is returned
  (§12.1 + §13.2 + §14.2 + §14.4's Note settle it as the byte 0x00/0x01);
- whether a duplicate-name check precedes name validation (§19.1 step 4 states
  it, and states which way);
- whether an ignored record's extent slot is validated (§19.1 step 4);
- where `[R-COD-04]`'s pre-fetch length check belongs (§19's preamble plus
  T14's *Detected* cell);
- the shuffle stride for every layout/type combination, including the packed
  bool identity case (`[R-COD-10]`);
- what a reader may still serve after each of the six outcome classes (§2.4
  plus §19.4 step 8's bounding paragraph, which is unusually complete about the
  region-read case).

## Confidence

**High** that an implementation built from this text alone would interoperate on
the read path. I built one, opened two files I constructed from the document
alone, read stored, sentinel, edge-padded, interleaved, planar, packed-bool and
byte-shuffled tiles, and ran twelve degradation cases, without once needing an
outside source. Every constant, offset, byte example and register count I could
check is correct, including three CRC constants, a 128-byte annotated file and a
275-instance count. The four findings above are a false exclusivity claim in
§21.7, a tense contradiction inside §20.3 step 4, an undefined actor in
`[R-CNT-04]`, and a duplicated clause in §20.5 — none of which forks the bytes.
