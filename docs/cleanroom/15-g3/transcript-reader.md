# Cleanroom round 15 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in five `Read` calls covering lines 1–4227. I ran `wc -l` and four `grep`
invocations against that same file (register row enumeration, and searches for
"structural ground / transparent"). I ran four Python scripts of my own authoring
in the scratchpad, which read no project file: a CRC-32C implementation, a decoder
of Appendix A's hex dump (typed in from the document text), a builder that
constructs a complete TARN file from scratch, and the arithmetic checks below.

I did **not** open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, or any ADR;
I ran no `git` command, no web search, no web fetch, and did not list any
directory. I did not read the round15 output directory.

One thing I must disclose because it was placed in front of me rather than sought:
my harness's system context included (a) an auto-memory index summarising prior
sessions on this project, and (b) a `gitStatus` block listing the subject lines of
the five most recent commits (`ADR-0076: the instance criterion applied in one
direction`, `ADR-0075: document rules attach only under assigned encodings`,
`§7.4: worked byte example for the layer record`, `Cleanroom round 12: 1
byte-level defect; quiz 15/15`, `ADR-0074: a stored tile freezes the declarations
it depends on`). I did not go looking for these and did not open any of the
referenced artifacts, but I saw the subject lines and I noticed, mid-walk, that
they name three of the ten changed sections. I deliberately did **not** use them
to settle anything: every finding below is argued from quoted specification text
alone, and I checked each candidate against the document after noticing the
overlap rather than before. Readers of this transcript should nonetheless discount
any impression that I "independently" homed in on §20.3, §21.1 or §18.2.

---

## 1. What I built

A conforming reader, on paper, in the order I would write the code:

```
open(transport)                 -> Session{F, trailer, directory, layer_table}
layer(session, name)            -> LayerHandle          (§19.3 full validation)
read_point(handle, coord, chans)-> samples | failure
read_region(handle, box, chans) -> samples | failure
```

Plus the degradation matrix and a worked end-to-end file I built and checksummed.

---

## 2. The open path, byte by byte

### 2.1 Step 1 — establish F

`[R-CNT-10]` forces the size to be transport-authoritative: "a full-response
content length, the complete length of a range response, or a size probe"; the
reader "MUST NOT substitute the trailer's committed_file_length for the transport
size". Locally this is a `stat`. Remotely, §19.1 step 1 says steps 1 and 2 cost
one request between them, because a `206` for a suffix range carries
`Content-Range: bytes X-Y/Z`.

Guess I had to make: what a reader does when the transport reports F < 64, so
that `[F − 64, F)` underflows. `[R-CNT-27]` gives the answer for the outcome
(reject-file below 128 bytes) but nothing places that check in §6.2's ordered
validation, whose enumerated list in `[R-CNT-06]` does not contain it. I resolved
it by checking `F ≥ 128` before issuing request 1 and reporting reject-file, and
then convinced myself no verdict turns on the ordering: §6.2's remaining gates
already reject every F < 128 that declares major 1 (dir_offset ≥ 16 ∧
dir_length ≥ 4 ∧ dir_offset + dir_length ≤ F − 64 forces F ≥ 84, and F mod 64 = 0
forces F ≥ 128), and for a file declaring a foreign major §2.3 settles it
independently of order — "a file declaring another major is neither conforming nor
nonconforming under it". So F5 is never the only row a sub-128-byte file
exhibits, but that is a corpus-construction problem for §24, not a reader fork. I
did not file it.

### 2.2 Step 2 — the trailer

One request, exactly 64 bytes, at `[F − 64, F)`. What bounds it before I have read
it: the constant 64 (§6.2, and permanently so under `[R-CNT-24]`) and F from the
transport. Nothing from the file.

Validation order, from `[R-CNT-06]`, is not negotiable and I implemented it as a
straight-line sequence:

1. magic `8A 4E 52 41 54 0D 0A 1A` at trailer +0 — byte equality, which
   `[R-ENC-10]` expressly says is not "acting on" the field, so it precedes the CRC.
2. trailer CRC at +60 over `[0, 60)`.
3. version gate (§6.3): `version_major == 0` → reject-file; a major I do not
   implement → refuse on capability grounds with a distinct diagnostic.
4. then, and only then, everything else: flag gates (incompat lane bits 0–15 set →
   reject-file; ignore lane 16–31 → ignore); committed_file_length == F and
   ≡ 0 (mod 64); dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
   1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved `[56, 60)` zero.

The reason the order is load-bearing is stated in §6.3/`[R-CNT-24]`: only the magic,
the major/minor at F − 56, and the CRC at F − 4 have positions fixed across all
majors. A reader that checked, say, `reserved == 0` first would be reading a byte a
future major may have redefined.

### 2.3 Step 3 — the directory

One request, exactly `dir_length` bytes at `dir_offset`. What bounds it before I
read it: two `u64`s that the trailer CRC has already covered — which is what
`[R-ENC-05]` demands ("MUST NOT allocate, seek, or issue I/O based on any integer
obtained from a file before the checksum covering it has been verified"). Verify
the final 4 bytes as CRC-32C over the preceding `dir_length − 4` (`[R-CNT-11]`);
mismatch is reject-file. §7.1 is explicit that the region is "always raw, with no
codec involvement on the open path", so there is nothing to decompress here.

### 2.4 Step 4 — record walk

Parse `⌈zero or more⌉` 24-byte headers + `inline_length` payloads to exactly
`dir_offset + dir_length − 4`, no residue (F29). At open I do, per §19.1 step 4:

* type 0 → reject-file (F24);
* unknown top-level type: MU = 1 → reject-file, MU = 0 → ignore-record;
* multiplicity: ≥ 2 top-level user-metadata records → reject-file (F34);
* extent-slot validity for **non-layer** top-level records only (F30/F31/F32) —
  a layer record's slot is deliberately *not* checked here, it is deferred to
  §19.3 and registered at layer access (L15–L17);
* top-level user-metadata framing: slot ≠ (0,0), extent_length ≥ 5,
  inline_length == 1 (F21/F22/F23);
* build the layer table by parsing each layer record's *name* and only its name.

The name handling is the subtlest part of the open and the document is unusually
careful here, so I recorded it verbatim as my implementation note: uniqueness is
"decided first, and over the raw name bytes whether or not each name is itself
well-formed", and "a layer record whose name field does not lie entirely within
that record's inline_length yields no name field to compare, so it contributes no
name to the namespace and is instead a validity error at layer scope". So my open
does: (i) slice each layer record's `[0, 1 + len)` from its inline payload, marking
records where that slice does not fit; (ii) compare the fitting slices bytewise for
duplicates → reject-file (F4); (iii) validate each fitting name under §4.6 →
reject-layer (L3/L5/L6) at open; (iv) the non-fitting records enter the table
nameless and unaddressable, their rejection due no later than layer access (L23).

### 2.5 Byte-exact cold remote open

Two requests. Request 1: 64 bytes, suffix. Request 2: `dir_length` bytes. Total
`64 + dir_length`. For Appendix A's file that is 64 + 4 = **68 bytes in 2
requests**; for the file I built in §5 below, 64 + 109 = **173 bytes in 2
requests**. Neither request touches `[0, 16)`: `[R-CNT-04]` makes the front-block
check turn on *residency*, not transport, and §6.4's accounting "does not include
the front block". A reader that instead speculates a suffix window and reaches
offset 0 owes the equality check and can skip request 2 by containment
(`[R-CNT-09]`). Appendix A works this through for the 128-byte case correctly,
including the 112-byte window that captures the directory while leaving `[0, 16)`
non-resident.

`[R-RDR-01]`'s invariant is the thing worth implementing to: the open's working set
is trailer + directory at any file size and layer count. My open therefore never
touches an extent slot's *contents*, never fetches an index region, and never
fetches a payload — which is also why §19.2's fourth tier ("at use of a record's
extent") can say "no earlier, since the open fetches no extent".

---

## 3. Validation timing by tier

I built this as a table driving the code, from §19.2 plus §21's *Detected* column
(which §19.1's preamble says is authoritative where the prose does not restate a
row):

| Tier | Checked | Rows |
|---|---|---|
| open | front block *if resident*; trailer; directory CRC; record framing; top-level MU gate; top-level multiplicity; non-layer extent slots; top-level user-metadata framing; layer-name namespace and each layer name's §4.6 validity | F1–F36 (reader rows), L3, L5, L6, R1 (top-level) |
| layer access | the whole layer record: slot, `[R-CNT-23]`'s constraint set, `[R-CNT-16]`, exact parse + sub-record walk + sub-record multiplicity, dimension/channel names, §4 widths and domains, the six value sets, bool fill, lz4 cap, geometry floor and its arithmetic, `[R-CNT-17]`'s index cross-checks | L1, L2, L4, L7–L36, L39, L43–L45, R1 (sub-record) |
| tile use | crc_of_crc_array, segment CRC, entry classification, payload CRC, decode exactness, decoded size | L37, L38, T1, T3, T6–T25 |
| extent use | the extent's terminal CRC and the document rules §18.2 attaches *at an assigned encoding* | R2–R10 |
| never (reader) | everything whose Detector is *verifier* | F7, F25–F28, F33, F36, L18, L25, L40–L42, L46–L49, T2, T4, T5, T26 |

Three things I made sure the code gets right:

* **Layer access performs no fetch.** `[R-RDR-03]` closes with "All are decidable
  from the resident directory and F". So `open()` can be cheap and `layer()` is
  pure computation. Good.
* **Index-chain failures take layer scope though detected at tile use.** §19.2 says
  so explicitly and L37/L38 carry *tile use* / reject-layer. My `read_point` therefore
  poisons the whole handle on a segment-CRC failure, not just the tile.
* **Rejection is prospective.** §2.4's reject-layer row and §19.4 step 8 both say a
  layer rejection "does not retroactively invalidate content already returned". So
  I do not have to buffer or retract.

What a reader is permitted never to check: every verifier row above; coverage and
slack (§5.2's Note: "Coverage is checked by verifiers, never by readers");
extent overlap (`[R-CNT-13]`: "readers are not obligated to detect overlap, which
requires whole-directory knowledge"); alignment and slab invariants (`[R-SLB-01]`,
`[R-SLB-03]`); padding-position content (`[R-SER-05]`); interleaved bool byte
values (`[R-SER-08]`); the sortedness of user-metadata members (`[R-MTA-05]`).

---

## 4. Layer access and the tile-read algorithm

### 4.1 Layer record parse

Fields are packed with no alignment, in §7.4's table order. My parser is a cursor
that must land exactly on `inline_length` after the trailing fixed fields, with the
remainder parsing as whole sub-records:

```
name          u8 len + bytes
layout        u8      1|2
linearization u16     ==1
codec         u16     1..4
filter        u16     1|2
A             u64     0 or pow2 in [512, 2^62]
S             u64     0 or 1..2^63-1
A_slab        u64     0 iff S==0, else pow2 in [1, 2^62]
d             u8      >=1
C             u16     >=1
d x { name, E:u64, T:u64 }        T>=1, E>=0
C x { name, type:u16, fill:u8 len + bytes }   len == elem_size(type)
index_encoding u8     ==1
entry_count    u64    == addressed-tile count
crc_of_crc_array u32  ==0 iff entry_count==0
sub-records    ...    to end of inline payload, no residue
```

Derived, all under `[R-ENC-04]`'s overflow rule at layer scope:
`Gᵢ = ⌈Eᵢ/Tᵢ⌉` computed as `Eᵢ/Tᵢ + (Eᵢ mod Tᵢ ≠ 0)` — the document explicitly
warns off `(E+T−1)/T` because the sum can leave the declared domain;
`N = ∏Gᵢ`, `P = ∏Tᵢ`, `addressed = N` (interleaved) or `C·N` (planar),
`Q = ΣBᵢ`, `Fᶜ = Σ_{j<c} Bⱼ`.

Cross-checks with no I/O: `entry_count == addressed`; and under index_encoding 1,
`extent_length == entry_count·20 + ⌈entry_count/2¹⁶⌉·4`, zero when
`entry_count == 0` (`[R-CNT-17]`).

`A ≠ 0 ∧ S ≠ 0` → reject-layer (`[R-CNT-16]`, L20). `S == 0 ∧ A_slab ≠ 0` →
reject-layer (L28).

### 4.2 Coordinate → tile

`tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`, in-tile ordinal `Σ uᵢ·∏_{j>i} Tⱼ`
(row-major, permanently, for *every* linearization value — §11.4 is emphatic that
in-tile order is not what the field selects), spatial ordinal
`s = Σ tᵢ·∏_{j>i} Gⱼ` under linearization 1, disk ordinal `s` interleaved or
`c·N + s` planar. Inverting: from a disk ordinal `k` in a planar layer,
`c = k div N`, `s = k mod N` — which is how the tile-read step knows which
channel's element size and fill to use.

I checked §11.4's worked example against my arithmetic: grid (4, 8), coordinate
(300, 700) → tile (1, 2) → s = 10, in-tile (44, 188) → 44·256 + 188 = 11,452;
planar C = 4 channel 2 → 2·32 + 10 = 74. All correct.

### 4.3 Index chain

Region bytes: entry array `[0, entry_count·20)`, then the segment CRC array
`[entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4)`. Entry `k` at region byte
`20k`. Segment `sg = k div 2¹⁶` covers entries `[sg·2¹⁶, min((sg+1)·2¹⁶, entry_count))`,
at region bytes `[sg·2¹⁶·20, min(...)·20)`.

To use entry `k` I must fetch and verify **the whole CRC array** (covered by
crc_of_crc_array) and **the whole containing segment** (covered by its u32). Both
ranges are computable from the layer record alone and may be fetched in parallel
(`[R-IDX-04]`). §15.4's example checks out arithmetically: entry_count 1,000,000 →
16 segments (15 full + 16,960), array at `[20,000,000, 20,000,064)`, entry 999,999
at segment-relative byte 339,180, segment 15 at `[19,660,800, 20,000,000)`; the
cap "one full segment (1.25 MiB) plus the CRC array" is 65,536·20 = 1,310,720. All
correct.

I cache verified ranges keyed `(file_id, range)` under `[R-LIF-03]`, which §15.4's
Note explicitly licenses ("To use" obliges verification, not re-verification).

The `[R-IDX-05]` constant is a writer convenience only: "Equality with the constant
licenses nothing for readers: verification is byte comparison of computed CRCs,
never constant matching." My reader computes.

### 4.4 Entry classification (§15.3)

```
if off==S and len==S and crc==0   -> sentinel  (fill)
if off==S and len==S and crc!=0   -> reject-tile [structural]
if (off==S) != (len==S)           -> reject-tile [structural]
if len==0                         -> reject-tile [structural]
if off<16                         -> reject-tile [structural]
if off>2^63-1 or len>2^63-1       -> reject-tile [structural]
if off+len overflows or > F-64    -> reject-tile [structural]
otherwise                         -> well-formed; fetch and check crc
```
Exactly six *structural* rows, matching §15.3's own count. The distinction matters
outside the reader: a structural entry contributes no extent to the coverage walk
or to the verifier rows (so its nominal bytes fall to slack, and it is transparent
to slab run continuity), whereas an entry that merely fails its payload CRC "is
well-formed: the defect lies in the bytes it addresses, not in the entry, so its
extent stands". I checked that this distinction is stated consistently in all four
places it is needed — §9.7, §15.3, §16.2 and L41 — and it is. §16.1 does not restate
it for the alignment invariant, but §15.3's clause is general ("the *verifier*
rows, which bind over well-formed entries' extents only"), so L40 is covered too.
I did not file that asymmetry.

Note the sentinel is *not* subject to the alignment invariant either, but for a
different reason: §3.1 makes a sentinel tile not *stored*, and `[R-SLB-01]`
quantifies over stored tiles.

### 4.5 Payload and decode

Fetch `[offset, offset + length)`; CRC over the stored bytes against the entry's
crc field, **before** decoding (`[R-CNT-20]`). Then codec, then filter inverse
(§17.1 — the writer order is filter-then-codec, so the reader order is
codec-then-filter-inverse; I got this backwards on my first pass and §17.1's second
sentence corrected me).

Decoded size, from declarations alone, never from payload content:

| case | size |
|---|---|
| interleaved | `P·Q` |
| planar, numeric channel c | `P·Bᶜ` |
| planar, bool channel | `⌈P/8⌉` |

`[R-SER-07]` makes any other decoded length a tile-scope error. Under codec 1
`[R-COD-04]` lets me reject before fetching at all. Under codec 3 I must reject a
`Frame_Content_Size` that disagrees, and must **not** allocate from it. Under all
codecs, trailing bytes after the stream/frame/block are a tile-scope error
(`[R-COD-08]`, T24).

The byte-shuffle inverse: `s = Bᶜ` planar-numeric, `s = Q` interleaved, `s = 1`
(identity) for a packed bool plane; `n = L/s`; inverse moves the byte at
`i·n + j` to `j·s + i`. I ran §17.3's example (`1.0, 2.0, 3.0` float32) through my
implementation and reproduced `00 00 00 00 00 00 80 00 40 3F 40 40` exactly.

### 4.6 Extract

Interleaved: channel `c` at in-tile ordinal `u` sits at `u·Q + Fᶜ`. Planar numeric:
`u·Bᶜ`. Planar bool: bit `u mod 8` of byte `u div 8`, LSB-first.

I re-derived §14.2's three worked examples and §14.3's packed example
(`55 01` with fill false, `55 FD` with fill true) and §14.5's edge tile (32 bytes,
value 0 real, values 1–15 each `CD AB`). All correct.

Padding positions are never returned (`[R-GEO-04]`); their content is the channel's
fill and I am not obliged to check it.

### 4.7 Sparse and fill

A valid sentinel short-circuits the payload fetch entirely: every requested
position of that tile reads as fill, bit-exactly as recorded, in declared channel
order for an interleaved layer or just the entry's own channel for a planar one.
`[R-TYP-09]` is the rule I put an assertion behind: fill is produced by *exactly*
one condition, a sentinel from a verified chain. A malformed entry, a failed index
CRC, or a failed payload CRC must never yield fill.

### 4.8 Region reads and partial failure

§19.4 step 8 gives me a genuine choice, stated as a choice: return the validating
entries' values with a per-entry report of the failed ones, *or* fail the request
whole — but never substitute fill. A layer-scope failure inside the same request
(step 3) bars the remaining entries and all further service, prospectively.

---

## 5. Worked example — a file I built and read back

Appendix A first. I typed its hex dump in and decoded it: F = 128, magic ok,
major 1, minor 0, flags 0, generation 1, dir_offset 16, dir_length 4,
committed_file_length 128, file_id `0x0123456789ABCDEF`, reserved zero, and the
trailer CRC over `[0, 60)` computes to **0xE00938D2**, matching the stored
`D2 38 09 E0` exactly. The directory region `00 00 00 00` is a zero-byte record
sequence plus the CRC of zero bytes, which is 0. Live claimants are 16 + 4 + 64 =
84 bytes, so slack is 44 — matching the annotation. Appendix A is correct in every
byte I can check.

Then I built my own, to exercise the parts Appendix A cannot: the §7.4 example
layer with one tile actually stored.

Layer `sst`: rank 1, dimension `x` with E = 100, T = 32; one interleaved float32
channel `temp`, fill `0x7FC00000`; codec 1, filter 1; no alignment, no slab.
G = 4, N = 4, P = 32, Q = 4, decoded size 128, entry_count 4, index region
4·20 + 1·4 = 84.

```
[0, 16)      front signature block
[16, 144)    stored tile, disk ordinal 0, 32 float32 values, 128 bytes
[144, 228)   tile-index region: 4 entries + 1 segment CRC
[228, 337)   directory: one layer record (24 header + 81 inline) + 4 CRC
[337, 384)   pre-trailer pad, 47 bytes of slack
[384, 448)   trailer;  F = 448, 448 mod 64 = 0
```
`dir_offset + dir_length = 337 ≤ F − 64 = 384` ✓.

Computed values: tile CRC `0xF8118D31`; segment CRC over the 80-byte entry array
`0xB76F7866`; crc_of_crc_array `0x9F491382`. My layer-record inline payload came
out to **81 bytes**, matching §7.4's stated `inline_length = 81` exactly, and every
field offset in §7.4's annotated dump (0, 4, 5, 7, 9, 11, 19, 27, 35, 36, 38, 40,
48, 56, 63, 68, 69, 77) matched my packer's cursor. The document's stated 4 + 34 /
18 / 12 / 13 = 81 decomposition is right.

I then independently checked §7.4's own two CRC constants for the all-sentinel
variant of that layer: CRC-32C over 80 bytes of `FF×16 00×4` repeated four times is
**0x80A34955** (stored `55 49 A3 80`) and the CRC of that 4-byte array is
**0xC4EE982E** (stored `2E 98 EE C4`). Both match the document. I also confirmed
`[R-IDX-05]`'s constant: CRC-32C of 2¹⁶ sentinel entries is **0xEECB3BB2**, and
§4.5's check vector CRC-32C("123456789") = **0xE3069283**.

**No stated constant, offset or checksum in this document is wrong that I could
check.** That is five independent constants and two worked byte layouts.

Reading my file back through the reader: open = 2 requests, 64 + 109 = 173 bytes;
`layer("sst")` = 0 requests; `read_point(x=5)` = fetch the 4-byte CRC array at
`[228−84+80 …]` (region-relative `[80, 84)`) and the single segment at
`[0, 80)`, verify both, classify entry 0 as well-formed, fetch `[16, 144)`,
verify `0xF8118D31`, identity codec, identity filter, extract bytes `[20, 24)`.
`read_point(x=40)` lands in tile 1, whose entry is the sentinel, and returns
`0x7FC00000` with no payload I/O at all.

Also checked: §21.8's arithmetic. I summed every Instances cell in §21.2–§21.5 by
hand: 57 + 115 + 57 + 44 = **273**, over 36 + 49 + 26 + 10 = **121** conditions —
matching "121 conditions over 273 instances" precisely. And the row numbering is
gapless (F1–F36, L1–L49, T1–T26, R1–R10). I then re-derived every instance cell
against §21.1's criterion (layout formulas enumerated; *differs from* enumerates
two directions, *exceeds* one; checksum-vs-computed and pattern-vs-constant
enumerate none; a nonzero test enumerates none; a single predicate over several
fields is one instance) and found no cell that disobeys it. Whatever was uneven
about that rule before, the version I read is internally consistent. I want that on
the record, since this is the passage the brief flagged as thrice-rewritten.

---

## 6. Degradation walks

**(1) Unknown record type, top level, MU = 0.** `[R-CNT-15]`: ignore-record. Its
extent is still a claimant for a verifier's walk ("a record extent (the bytes any
record's extent slot references, **whatever the record's type**, §7.2)"), and it is
covered by no checksum (§8.1's last row), so corruption in it is invisible —
§22.3 says so. I still serve every layer and every tile. An updater must carry it
forward or, at PE = 0, may drop it under §20.4's conditions.

**(2) Unknown record type, top level, MU = 1.** reject-file. Nothing is served.
If the type is from the experimental range the *file* is still conforming
(§21.6's second structural case) and my diagnostic must say so rather than
"corrupt". If it is from the reserved range, the file is nonconforming (F36) — but
that is a verifier's finding, not mine; my behavior is identical either way.
As a layer sub-record, the same MU = 1 gives reject-**layer**, never reject-file
(`[R-CNT-18]`), and every other layer stays readable.

**(3) Unknown codec value.** A conforming reader implements all four assigned
codecs and both filters (`[R-CNF-03]`), so this can only be a reserved or
experimental value → reject-layer at layer access (L43), before any I/O. Every
other layer is unaffected; I can still list the rejected layer's name (§2.4). A
verifier that cannot *execute* an assigned codec is in a different position: it
"cannot establish" and MUST NOT certify (`[R-COD-11]`).

**(4) Unrecognized flag/enum.** Trailer incompat bit → reject-file; ignore-lane bit
→ ignored and the file is conforming; record reserved flag bits 2–15 → readers MUST
ignore, verifier records F26/L47; layout/linearization/type/index_encoding/filter
outside their assigned values → reject-layer; metadata encoding 0 or 3–0x7F →
ignore-record *and* a violation (R1); metadata encoding ≥ 0x80 → ignore-record and
**not** a violation, with the verifier still certifying and naming the record
(`[R-MTA-10]`, §21.6). I traced `[R-EXT-03]`'s enumeration against §10.2's eight
identifier spaces and all eight are accounted for.

**(5) Truncated tail / torn commit.** The physical tail is not a trailer, so the
magic (F8) or the CRC (F14) or `committed_file_length` against the transport size
(F17) fails. reject-file, report *torn*, and `[R-LIF-05]` forbids scanning
backward. The state is recoverable, not readable — §9.6's probe is a deliberate
tool operation whose output must be re-verified whole. §9.5's Note is right that
residue past a completed commit needs no register row of its own: I meet it as one
of those three already-registered gate failures and cannot tell it from corruption.

**(6) Checksum mismatch, by scope.** trailer → reject-file; directory → reject-file;
crc_of_crc_array or a segment CRC → reject-**layer** (though detected at tile use);
a stored tile's crc → reject-**tile**, and never fill in its place; a user-metadata
extent's CRC → ignore-record with a SHOULD-report. That last one is the quarantine:
"Application metadata never invalidates the structural data it annotates."

**(7) Limit exceeded.** `[R-ERR-04]`: the file stays conforming, I may decline at
the whole file or at the narrowest scope whose *declarations* exceed what I can
serve, and I MUST report it as a resource limit, not as corruption — "a reader that
reports 'too large' as 'corrupt' invites the deletion of intact data". A
user-metadata document is the one case with no narrower scope, because it has no
declared size; §18.2's Note says such a decline is at the whole file, and
ignore-record remains available.

**(8) Format major I do not implement.** reject-file on capability grounds with a
diagnostic distinct from both "not a TARN file" and "corrupt". No row of §21
reaches such a file; a verifier reports *cannot establish*, never *nonconforming*.

**(9) A nonconforming interleaved bool byte.** This one I had to read three times;
see finding reader-02. §14.2's `[R-SER-08]` is clear on its own terms: I am not
obliged to screen decoded content; if I detect the violation `[R-CNF-12]` lets me
reject the tile; if I neither detect nor reject, I MUST report `0x00` as false and
every other byte as true. My implementation does not screen, so it reports
`0x02` as true. §12.3 flags this as the single place a reader resolves a byte
rather than passing it through.

---

## 7. Where I had to guess, and what I filed

Six findings. Full prose below; the structured return carries the same six.

---

### reader-01 — CONTRADICTION — §20.5, `[R-WRT-06]` vs §20.4, `[R-WRT-08]`

§20.5 says, of a compactor that has detected a violation:

> "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
> (`[R-WRT-05]`)."

§20.4's table says of an MU = 0, PE = 0 record:

> "Retain byte-identical, or drop it — its extent becoming slack. … A compactor
> may drop it whenever it rewrites the file."

And §20.5's own opening sentence, four sentences earlier, says:

> "A compactor's output contains only the structures reachable from the input's
> live trailer — the live committed state (§7.2), **less any record §20.4 lets it
> drop** — so slack is never carried."

So `[R-WRT-06]` cites §20.4 as authority for a proposition §20.4 denies, and
contradicts its own paragraph's opening clause.

The case is reachable and not exotic. Take a top-level record with MU = 0, PE = 0
whose type value is in the reserved range 0x0003–0x7FFF. That is a violation (F36),
whose assigned detector is the verifier — so a compactor built into a verifying
tool detects it, while a bare compactor need not. `[R-WRT-06]`'s *first* MUST does
not fire: `[R-WRT-09]`'s obliged checks are the open, each retained layer's record
and index chain, and each relocated extent's checksum, and none of them fails —
§19.1's open applies `[R-CNT-15]`'s MU rule and MU = 0 means ignore-record, so the
open succeeds. Only the second MUST is in play, and dropping the record would
discharge it completely: the output would carry no violation at all. The same holds
for a droppable record with a reserved flag bit set (F26).

Two readings, both defensible:

* **(A)** The parenthetical is a rule: a compactor that detects a violation cannot
  drop, so it must refuse. It emits nothing.
* **(B)** §20.4's explicit compactor permission governs — reinforced by §20.5's own
  "less any record §20.4 lets it drop" — so the compactor drops the offending
  record and emits a compacted, conforming file.

I picked (B) when writing my own compactor, because §20.4 is the section §20.5
defers to by name, because §20.5's opening sentence says the same thing, and
because (A) makes a reserved-range flag bit on an ancillary record permanently bar
compaction of an otherwise healthy file — precisely the outcome §20.4's
"a compactor may drop it whenever it rewrites the file" exists to avoid.

Without this resolved, an implementer who picks (A) ships a compactor that refuses
files another compactor happily rewrites.

**Byte-level: yes.** Implementation A emits nothing for an input that
implementation B compacts into a conforming output file. Under (A) that output is a
byte sequence no conforming compactor may emit; under (B) it is. The honest
counter-argument, which I record: one can read the parenthetical as mere
justification for the two MUSTs rather than as an independent rule, in which case
only §20.4 binds and there is no fork. I do not think that reading survives the
words "it can **neither** drop the structure … **nor** re-emit it corrected", which
is an exhaustive claim about the compactor's options, offered as the reason the
MUST NOT forces refusal.

---

### reader-02 — CONTRADICTION — §21.1 vs §14.2 (`[R-SER-08]`) and §2.4 (`[R-CNF-12]`)

§21.1's closing paragraph, describing verifier-detector rows:

> "For a row whose Detector is *verifier*, the outcome names the scope at which the
> damage is recorded, not an obligation on any reader: the governing rule states
> what a reader does, and for several such rows it obliges the reader to serve the
> structure unchanged (`[R-SER-08]`, `[R-CNT-22]`, and `[R-MTA-05]`, whose unsorted
> document readers process as they find it — F27 and L48)."

For `[R-CNT-22]` and `[R-MTA-05]` this is accurate — both carry a genuine MUST that
the reader process the structure. For `[R-SER-08]` it is wrong twice over. §14.2:

> "A reader is not obligated to screen decoded content, and a reader that does not
> detect the violation is not thereby nonconforming; `[R-CNF-12]` governs a reader
> that does detect it. A reader that neither detects the violation nor rejects the
> tile, and returns the value, MUST report 0x00 as false and every other byte as
> true."

First, the reader is not *obliged to serve*: `[R-CNF-12]` says "a reader MAY reject
it upon detecting any violation, including violations whose assigned detector is
the verifier", and §14.2 invokes that by name. Second, when it does serve, it does
not serve the structure *unchanged*: it must resolve every non-`0x00` byte to true,
which §12.3 singles out as "the one case where a reader resolves a byte to a value
rather than passing it through", and Appendix H calls "the sole resolved byte".

Permitted readings of the T2 case: (a) a reader that detects the bad byte MUST
still return the tile, resolving the byte; (b) a reader that detects it MAY reject
the tile, and only a reader that serves must resolve. I picked (b): §14.2 and
`[R-CNF-12]` are direct and unambiguous, and §21.1's clause is offered as a
*report* of what the governing rules oblige, not as a rule of its own. An
implementer who trusts §21.1's summary instead builds a reader that returns samples
from a tile it has diagnosed as malformed, believing it has no choice.

Note that §21.1's own tie-break — "where a row and the rule it cites diverge, the
rule governs" — is scoped to *rows*, and this sentence is not a row, so the
document does not literally supply the resolution; it has to be assembled from
§14.2 plus `[R-CNF-12]`.

**Byte-level: no.** Both readings agree on what a reader that serves must return
(`0x00` false, everything else true); they disagree only about whether rejecting is
also permitted, and §14.2's "`[R-CNF-12]` governs a reader that does detect it"
plus §2.4's blanket MAY settle that in the text as it stands. Two competent
implementations should not diverge on bytes here, only on how confidently they read
§21.1.

---

### reader-03 — OBSERVATION — §21.7 (`[R-ERR-01]`)

> "§20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored — the §21.4 rows then fire — and a commit that supersedes
> every tile it would have damaged leaves the live state clean, so the bar is
> unwitnessed there for the same reason `[R-LIF-01]` is"

The clause "the §21.4 rows then fire" asserts that whenever a barred declaration
change reaches a tile that remains stored, some tile-scope row detects it. That is
not so. §20.3 step 4's test is general — "alters … what §14 fixes for its stored
bytes **or how they decode**" — and the enumerated list "names where that effect
arises rather than standing on its own". Consider an interleaved layer with two
channels `a` and `b`, both `uint8`, with byte-identical fill values, and a commit
that swaps their declared order. The decoded size is unchanged (`P·Q`), the set of
padding positions is unchanged, the padding content is unchanged (the fills are
equal), the codec and filter are unchanged — so T3, T4, T5, T14 and T21–T26 all
stay silent, and every stored tile still passes its crc. Yet `Fᵃ` and `Fᵇ` have
swapped, so every sample the layer returns is now wrong: the commit altered how the
stored bytes decode, which the bar prohibits, with no §21.4 witness.

This does not change the register's contents — such a change is detectable only
against the prior generation, which §9.7 does not reconstruct, so §20.3 step 4 is
correctly omitted from §21.2–§21.5 either way. What is wrong is the *reason*
§21.7 gives. The entry ends up asserting both that the bar is witnessed (where
tiles remain stored) and that it is unwitnessed (where they are superseded), when
the truth is that it is unwitnessed in both cases and the §21.4 rows merely happen
to fire in the sub-case where the change also breaks a structural constraint.

**Byte-level: no.** No implementation's accept/reject verdict turns on it: the
register is unchanged, and a verifier cannot check §20.3 step 4 in any case. What
this costs is a writer implementer who reads §21.7 as licence to treat the §21.4
rows as a self-test for step 4 compliance.

---

### reader-04 — OBSERVATION — §11.1, Rationale

> "growth that raises one changes entry_count and with it extent_length
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and disk
> ordinals renumber (§20.3, `[R-WRT-04]`, `[R-GEO-06]`) — the first growth of a
> zero-extent layer included."

Disk ordinals do not renumber when the raised grid count is `G₀`. `[R-GEO-06]`
gives `s = Σᵢ tᵢ·∏_{j>i} Gⱼ`; the `i = 0` term is `t₀·∏_{j>0} Gⱼ`, so `G₀` appears
in no product and cannot affect any spatial ordinal. Growing an interleaved layer
along its first-declared dimension therefore leaves every existing tile's disk
ordinal fixed and appends new ordinals at the end — the cheap, common case
(appending time steps or scan lines along the slowest axis). For a rank-1 layer
that is the *only* case, so the sentence is false for every rank-1 growth,
including "the first growth of a zero-extent layer" it names, whenever d = 1.
(It is correct for planar layers, where the disk ordinal is `c·N + s` and `N = ∏Gᵢ`
does move with `G₀`, and for interleaved growth along any dimension but the first.)

§20.3 step 4 states this correctly and normatively — "(a geometry change renumbers
ordinals **wherever** `[R-GEO-06]` moves them)" — and §2.1 gives a *Rationale* no
force, so the governing text is right. I still had to stop and re-derive
`[R-GEO-06]` to be sure my index re-emission was not silently wrong.

**Byte-level: no.** §20.3's normative text already decides it, and the whole index
region is re-emitted regardless, so the entries land in the same places either way.
The risk is confusion, not divergence.

---

### reader-05 — OBSERVATION — §20.3 step 4 (`[R-WRT-04]`)

> "an extent MAY **grow**, since a position that becomes real held that channel's
> fill and fill is a legal sample value — provided the grown geometry stays within
> every bound the layer's own declarations impose, `[R-COD-07]`'s lz4 decoded-size
> cap being **the one such bound in format major 1** (L44), which an empty layer
> escapes only because that cap is quantified over addressed tiles."

The exhaustiveness claim is at least arguably wrong, and I could not settle it from
the text. Extent growth also moves quantities that `[R-ENC-04]` bounds and
`[R-ENC-03]` domains: `N = ∏Gᵢ`, `N·P`, `C·N`, `entry_count`, and
`entry_count·20 + ⌈entry_count/2¹⁶⌉·4` all rise with `Eᵢ` and can cross 2⁶³ − 1,
which is registered as L2 and L1, not L44. Those are bounds a grown geometry can
breach and the lz4 cap is not the only one.

Two readings: (i) "bounds the layer's own declarations impose" means
declaration-*conditional* bounds — ones that exist only because of what this layer
declared, of which the lz4 cap is indeed the only one in major 1 — in which case
the sentence is right; (ii) it means any bound that the layer's declared values are
measured against, in which case `[R-ENC-04]`'s overflow bounds qualify and the
sentence is incomplete. I implemented (ii) — i.e. I check the overflow bounds on
growth as well — because getting it wrong the other way emits a nonconforming file.

Nothing breaks either way: `[R-ENC-04]` binds independently of this sentence,
§20.3 step 3 routes the appender through §19.3's layer validation which includes
`[R-GEO-01]`–`[R-GEO-03]`, and `[R-CNF-05]` requires a conforming file regardless.
So the cost of the ambiguity is an implementer who reads the sentence as a
checklist and omits the overflow checks on the growth path.

**Byte-level: no.** The overflow rules bind on their own and a reader/verifier
detects the result as L1/L2 at layer access whichever way a writer read this
sentence; no reader's accept/reject verdict changes.

---

### reader-06 — OBSERVATION — §20.5 (`[R-WRT-07]`) vs §20.3 step 2 and §15.3

`[R-WRT-07]` gives compaction's index-regeneration recipe as a closed enumeration:

> "regenerates each relocated tile-index region (entry offsets new; entry lengths,
> entry crcs, and sentinel entries unchanged; segment CRCs recomputed over the
> entries as re-emitted)"

There is no case in that enumeration for a non-sentinel entry that §15.3 classifies
reject-tile on a *structural* ground — one with `length = 0`, or `offset < 16`, or
exactly one half at the sentinel value, or an extent past `F − 64`. Such an entry
is not a sentinel, so "sentinel entries unchanged" does not reach it; and it
addresses no usable extent, so "entry offsets new" has no new offset to assign.

The state is not hypothetical: §20.3 step 2 provides for it explicitly on the
append path — "a malformed index entry an appender meets while re-emitting a region
is carried forward byte-identically at its disk-ordinal position under step 4, **not
repaired to a sentinel**" — and §15.3 and §9.7 both build machinery around it. So a
compacted file's input can certainly contain one.

Three candidate readings: (a) refuse to compact; (b) copy the 20 bytes verbatim;
(c) write a sentinel. (c) is foreclosed, but only by assembling `[R-CNF-04]` ("A
reader MUST NOT heuristically repair a violating structure") with §2.3's rule that
updaters are readers of what they process — and it matters to me as a *reader*,
because under (c) the tile would come back as fill where under (a)/(b) it comes
back as a failure, which is exactly the substitution `[R-TYP-09]` and `[R-CNF-09]`
exist to forbid. Between (a) and (b), §20.5's "MUST NOT emit a file carrying a
violation it has detected" points at (a) for any compactor that classifies its
entries — and a compactor must read every entry's offset and length to relocate
the tile bytes, which is classifying it. I implemented (a).

**Byte-level: no**, once `[R-CNF-04]` is brought to bear, which forecloses the only
reading that would change what a reader returns. (a) and (b) differ in whether an
output file exists at all, not in what any reader gets from the tile. I file it as
an OBSERVATION rather than an AMBIGUITY because the answer is derivable — it just
takes four sections and a class definition to derive, and `[R-WRT-07]`'s
enumeration reads as complete when it is not.

---

## 8. Things I checked and did not file

For the record, so this walk can be audited rather than repeated:

* Every stated constant and worked byte layout (§4.5's check vector, §7.4's two
  CRCs and its 81-byte payload, §15.4's `0xEECB3BB2`, Appendix A's trailer CRC and
  every field, §11.2/§11.4/§14.2/§14.3/§14.5/§15.4/§17.3's examples,
  §16.2's slab example, §21.9's Note arithmetic, `[R-CNT-27]`'s 128-byte floor).
  All correct.
* §21.8's "121 conditions over 273 instances", summed by hand from every cell.
  Correct, and every cell obeys §21.1's instance criterion as written.
* The six *structural* rows of §15.3 restated consistently in §9.7, §15.3, §16.2
  and L41. §16.1 does not restate the exclusion for the alignment invariant, but
  §15.3's clause is general ("bind over well-formed entries' extents only"), so
  L40 is covered. Not a defect.
* `[R-EXT-03]`'s value-set enumeration against §10.2's eight identifier spaces:
  complete.
* §2.3's five *cannot establish* grounds against `[R-COD-11]`, `[R-MTA-09]`,
  `[R-ERR-04]` and §21.6: consistent.
* Cross-references to register rows from outside §21 (F1, F6, F7, F8, F9/F10,
  F17, F31/F32, F33, F35, F36, L16/L17, L18, L24, L25, L40–L42, L44, R1, T8/T9,
  T24, F27/L48): all resolve to the row the citing text describes.
* The `[R-CNT-27]` / §6.2 ordering question (§2.1 above): decided by §2.3 plus
  §21.2's preamble, not a fork.
* Whether T14 is an unlisted strict specialization of T3 (it is — under codec 1 a
  wrong entry length always yields a wrong decoded length). Same outcome, same
  detector, same tier, and §24's "records every row the file exercises and says
  which it was built for" handles the corpus side. Not a defect.
* Whether an ignored record's extent is a coverage claimant (yes — §5.2's
  "whatever the record's type"), and whether a user-metadata extent under an
  unassigned encoding is CRC-verified (yes — §8.1's map, §22.3, `[R-MTA-10]`).
* Appendix G's ten items against the degrees of freedom I could enumerate
  (codec/encoder, placement, gap content and extent, record and sub-record order,
  file_id, generation, minor/flags, all-fill tiles, fill default, JSON writer, NFC).
  Item 2's `file_id` derivation is now pinned unambiguously — "the digest's **last
  eight bytes in output order** … read little-endian" over `[0, F − 64)` followed
  by trailer bytes `[0, 60)` with `file_id` zeroed — and I confirmed the round trip
  is the identity, so `trailer[48:56]` equals `digest[-8:]` byte for byte. Item 3's
  ordering key is derivable for every record type and its tie-break argument
  ("emitting them in either order yields the same file") holds. I found no residual
  freedom the profile leaves open.
