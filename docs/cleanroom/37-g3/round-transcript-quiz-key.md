# Quiz-keyer working transcript — Cleanroom round 37

Access: read only `spec/tarn.md` (4981 lines), read in full via six sequential
`Read` calls (offsets 1, 1000, 1700, 2400, 3100, 3800, 4500-end). No other
project file was opened. Local Python computation (no file reads) was used
for CRC-32C and arithmetic checks; scripts written to this scratch directory:
`crc_check.py`, `crc_check2.py` (independent table-based cross-check),
`arithmetic_checks.py`.

Both CRC-32C implementations were validated against the spec's own check
vector (§4.5: CRC-32C("123456789") = 0xE3069283, CRC-32C(zero bytes) =
0x00000000) and against the spec's stated full-all-sentinel-segment constant
(§15.4, `[R-IDX-05]`: 0xEECB3BB2 for 65536 sentinel entries) before being
trusted for the round's actual question. Both implementations agreed on
every result.

---

## Q01

index_encoding 1, entry_count = 70000. Segments per §15.4: segment s covers
entries [s·2^16, min((s+1)·2^16, entry_count)). Segment 0: [0,65536) = 65536
entries (full). Segment 1: [65536,70000) = 4464 entries — a **partial**
segment (it does not cover exactly 2^16 entries).

`[R-IDX-05]`: "writers of sparse layers MAY emit this constant
[0xEECB3BB2] for any **full** segment — one covering exactly 2^16 entries,
final or not — whose entries are all sentinels, without computing it — **a
partial segment's CRC MUST be computed**."

Segment 1 is partial (4464 < 65536), so the constant may NOT be used; the
writer MUST compute the CRC-32C over the 4464 sentinel entries' stored bytes
(89,280 bytes: 4464 × 20-byte sentinel entries, each `FF×16 00×4`, §15.2).

Computed (two independent implementations, cross-validated against the
spec's own check vector and full-segment constant): **0xE6E3E4F3**.

**Answer: 0xE6E3E4F3**
Confidence: high.

---

## Q02

Interleaved layer, dims declared y(E=10,T=4) then x(E=10,T=4); channels a
(uint16, index 0) then b (uint8, index 1). Coordinate (y=7,x=7).

§11.4: tile coords tᵢ = xᵢ div Tᵢ; in-tile position uᵢ = xᵢ mod Tᵢ. In-tile
sample ordinal = Σᵢ uᵢ·∏_{j>i}Tⱼ (row-major, last-declared dim fastest).
u_y = 7 mod 4 = 3; u_x = 7 mod 4 = 3. Ordinal = u_y·T_x + u_x = 3·4+3 = 15.

§14.2 interleaved byte layout: offset of value k = (k div C)·Q + F_{k mod C},
Q = ΣBᵢ (sample stride), Fᶜ = ΣBⱼ for j<c. Q = 2(a,uint16)+1(b,uint8) = 3.
F_b = B_a = 2.

Offset of channel b at in-tile ordinal 15 = 15·3 + 2 = **47**.

**Answer: 47**
Confidence: high.

---

## Q03

Planar layer, channels p(float64,size8), q(uint8,size1); P = 300,000,000
per tile (every addressed tile); codec = 4 (lz4).

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes ... in a planar
layer each channel's plane carries its own decoded size (§14.2, §14.3), and
the largest governs ... a reader MUST treat such a declaration as a
validity error at layer scope, checkable from declarations alone."

Per §14.2, planar numeric decoded size = P·Bᶜ.
- channel p: 300,000,000 × 8 = 2,400,000,000 bytes
- channel q: 300,000,000 × 1 = 300,000,000 bytes
- cap 0x7E000000 = 2,113,929,216 bytes

Largest (p's plane, 2,400,000,000) exceeds the cap (2,113,929,216), so the
codec declaration is nonconforming (register row L44). Outcome per L44's
scope and §2.4's outcome-class table: reject-layer, an error "checkable from
declarations alone" i.e. detected at layer access (§19.3), not requiring
payload I/O. §2.4: "reject-layer ... all other layers are unaffected."

**Answer: reject-layer; no (other layers unaffected)**
Confidence: high.

---

## Q04

Trailer: version_major=1 (implemented), flags=0x00000004 (bit 2 set — bits
0-15 are the incompat lane per §6.2's layout table), everything else valid.

§6.3, `[R-CNT-08]`: "a reader MUST reject-file on any set bit it does not
implement in the incompat lane (bits 0–15) ... In this specification's text
no flag bits are defined." Register row F19: "Any bit of the flags incompat
lane (bits 0-15) is set; this text defines no flag bits, so every such bit
is unimplemented" — outcome reject-file, governing rule `[R-CNT-08]`.

This is a genuine file-scope violation (unlike the *ignore-lane* bit case,
which `[R-CNF-02]` expressly carves out as a writer-conduct-only rule, not a
file-conformance violation — that carve-out explicitly names the
ignore-lane, not the incompat lane). F19 is a listed register row (§21.2),
and §21.1 states the register enumerates file-conformance violations, so a
file exhibiting F19 is nonconforming.

**Answer: no (not conforming); reject-file**
Confidence: high.

---

## Q05

index_encoding 1, entry_count = 200,000.

`[R-CNT-17]`/§7.4: extent_length = entry_count × 20 + ⌈entry_count / 2^16⌉ × 4.

⌈200,000 / 65,536⌉ = ⌈3.0518⌉ = 4.
extent_length = 200,000×20 + 4×4 = 4,000,000 + 16 = 4,000,016.

**Answer: 4,000,016**
Confidence: high.

---

## Q06

Interleaved layer, N = 20 (block [0,20)); slab run length S = 6.

§16.2, `[R-SLB-02]`: "Run r of a block starts at ordinal block_start + r·S
... the final run of a block can cover fewer than S ordinals." Runs:
[0,6),[6,12),[12,18),[18,20). 20 mod 6 = 2 ≠ 0, so the final run [18,20)
covers 2 ordinals.

**Answer: 2**
Confidence: high.

---

## Q07

Layer record inline payload per §7.4's table, computed field by field
(name/type framing per §4.6/§7.4):

- name `z` (len 1): 1+1 = 2
- layout (u8): 1
- linearization (u16): 2
- codec (u16): 2
- filter (u16): 2
- alignment A (u64): 8
- slab S (u64): 8
- slab alignment A_slab (u64): 8
- rank d (u8): 1
- channel count C (u16): 2
- dimension entry `u` (extent5,tile5): name(1+1) + extent(8) + tileextent(8) = 18
- dimension entry `v` (extent7,tile3): 18
- channel entry `p` (uint8, elem size 1): name(1+1) + type(2) + fill(1+1) = 6
- channel entry `q` (uint16, elem size 2): name(1+1) + type(2) + fill(1+2) = 7
- index_encoding (u8): 1
- entry_count (u64): 8
- crc_of_crc_array (u32): 4
- sub-records: 0 (none)

Sum: 2+1+2+2+2+8+8+8+1+2+18+18+6+7+1+8+4 = 98.

Cross-checked against the worked example in §7.4 itself (a 3-byte name plus
the nine leading scalar fields = 4+34 bytes; here name is 1 byte so
2+34=36, plus dims 36 + channels 13 + trailing fixed 13 = 98). Verified by
local Python arithmetic as well.

**Answer: 98**
Confidence: high.

---

## Q08

Layer L stored ≥1 tile in the superseded generation. Commit changes only
one channel's recorded fill value (same element size, different bit
pattern); nothing else touched.

§20.3 step 4 lists the *only* declarations an appender may change on a
layer that stored a tile in the superseded generation: name, dimension/
channel names, extent growth, planar channel-list extend/shorten at the
end, slab/alignment declared/changed/cleared. Fill is explicitly *not* on
that list — the same step lists it, together with type and tile extent,
among what a commit MUST NOT change on such a layer: "Every other
declaration is fixed for as long as the layer stores a tile: ... every
channel's type and fill ...". The example under 20.3 shape (c) confirms
directly: "A change to any fixed declaration of a layer that **stored** a
tile in the generation the commit supersedes — a fill value, a type, a
tile extent — is not an appender's operation at all (step 4)."

`[R-WRT-01]`/§20.3: "A commit MUST NOT change one of these; the change is a
new layer, or a rewrite that re-declares it under a fresh file_id."

**Answer: No — not permitted as an ordinary appender's commit under the
existing name. The two named alternatives: (1) create it as a new layer
(under a different name), or (2) perform a whole-file rewrite that
re-declares the layer under a fresh file_id (§20.5).**
Confidence: high.

---

## Q09

Layer L's sub-records: (1) user-metadata sub-record (registered type
0x0002, registry-fixed MU=0, PE=1); (2) an unassigned-type sub-record,
MU=1, unimplemented by this updater. Appender wants to drop layer L
entirely.

§20.4: "A commit MAY therefore drop a layer record, and the drop takes the
layer whole: a sub-record's flags govern it within a layer the updater
keeps, so a dropped layer's sub-records and their extents go with it
whatever their PE bits. **One sub-record blocks the drop, a sub-record of a
type the updater does not implement with MU = 1**, the drop being a
modification of the scope it governs (the table's first row)."

The user-metadata sub-record's PE=1 status is irrelevant to a *layer drop*
(it "goes with" the layer regardless of PE bit) — PE=1 only blocks
*retaining the layer while modifying that record*, not dropping the whole
layer. Only the MU=1 unassigned-type sub-record — per §20.4's table row
"MU = 1 ... at layer scope an unknown critical record blocks modification
of that layer, its drop included" — blocks this drop.

**Answer: No, the drop is not permitted. It is blocked specifically by the
sub-record of the unassigned type carrying MUST_UNDERSTAND = 1 (not by the
user-metadata sub-record).**
Confidence: high.

---

## Q10

Non-layer, non-user-metadata top-level record, type ≥ 0x8000 (experimental,
unassigned), flags MU=1, PE=0. No reader implements the type.

Two independent things are true of this record:

1. Register row F25 (§21.2): "A non-layer top-level record's flags carry
   MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination no writer
   emits" — detector *verifier*, governing rule `[R-CNT-12]`: "Writers MUST
   NOT emit the combination MU = 1 with PE = 0 ... Both writer violations
   make the file nonconforming (`[R-CNF-05]`)." This applies regardless of
   whether the type value is assigned, reserved, or experimental — F25's
   condition is stated purely over the flag combination. So this file
   carries a genuine file-scope violation and is **not conforming**.

2. Independently, `[R-CNT-15]`: "An unknown record type at file scope:
   MU = 1 → reject-file". Since the type is experimental (by definition
   unregistered — no reader is expected to implement it) and MU=1 is set,
   an ordinary conforming reader that does not implement this type MUST
   reject-file at open (§19.1 step 4). This is the same mechanical gate
   §21.6 describes for "an experimental-range top-level record type
   carrying MU = 1" (there stated for the PE=1-conforming case; here the
   file already fails on F25, but the reader's own open-time action is
   unaffected by that — it is a pure MU-bit/unknown-type gate).

**Answer: no (file is not conforming, due to F25's MU=1/PE=0 violation);
reader outcome: reject-file (an unimplemented MU=1 top-level type, per
`[R-CNT-15]`).**
Confidence: high.

---

## Q11

Interleaved tile, channels a(int8,size1), b(int16,size2); P=2. Decoded
values: pos0 a=0x01, b=0x0203; pos1 a=0x04, b=0x0506 (b little-endian per
`[R-ENC-01]`). Filter = byte-shuffle (2).

Decoded tile image (§14.2, sample-major, channel order a then b, b encoded
little-endian so low byte first):
`01 03 02 04 06 05` (pos0: a=01, b_lo=03, b_hi=02; pos1: a=04, b_lo=06, b_hi=05).

§17.3 byte-shuffle: stride s = sample stride Q = 1+2 = 3 (interleaved).
L=6, n=L/s=2. View as n=2 groups of s=3 bytes:
group0 = [01,03,02], group1 = [04,06,05].
Filtered image places byte i of group j at offset i·n+j:
- i=0: offset0=group0[0]=01; offset1=group1[0]=04
- i=1: offset2=group0[1]=03; offset3=group1[1]=06
- i=2: offset4=group0[2]=02; offset5=group1[2]=05

Filtered sequence: 01 04 03 06 02 05.

This matches the shape of the spec's own worked example in §17.3 (all first
bytes of each group, then all second bytes, then all third bytes).

**Answer: 01 04 03 06 02 05**
Confidence: high.

---

## Q12

Codec 3 (zstd), tile decoded size = 500,000 bytes. Frame: correct magic, no
dictionary ID, no content-checksum flag, exactly one frame, Window
Descriptor (not Single_Segment_Flag) declaring Window_Size = 8,388,608
bytes (8 MiB), no Frame_Content_Size field.

`[R-COD-06]`: "writers ... MUST NOT declare a window size exceeding the
tile's decoded size; a reader MUST treat ... a validity error at tile
scope, both being header-checkable." Declared Window_Size (8,388,608) vastly
exceeds this tile's decoded size (500,000). This is register row T21:
"Codec 3 (zstd) and the frame declares a window size larger than the tile's
decoded size" — outcome reject-tile.

(The separate §21.9 8 MiB *reader minimum guarantee* on Window_Size is not
what's at issue here — that guarantee only lets a writer declare up to 8
MiB and still be sure any conforming reader accepts it; it does not excuse
a window larger than the tile's own decoded size, which `[R-COD-06]` bars
outright regardless of the 8 MiB figure.)

**Answer: reject-tile**
Confidence: high.

---

## Q13

Rewriter compacting a file; re-creates one layer under new tiling/codec,
asserting the reference array is unchanged, but does not implement the
layer's declared sample type and cannot decode any of its existing tiles.

§20.5: "A layer the rewrite re-creates is new output: its record, its
tile-index region and its stored tiles are written under §20.2's rules
**from content the rewriter decoded** (§19.3, §19.4) ... What it re-creates
it decodes as a reader (`[R-CNF-11]`) and writes as a creator (§20.2)."
`[R-WRT-07]` states this as the governing rule for re-creation.

Since the rewriter cannot decode the layer's sample type at all, it cannot
satisfy this decode-then-write requirement, and (per `[R-CNF-03]`) software
that does not implement a core sample type is not even a conforming reader
of that content in the first place. It cannot "assert" the reference array
is unchanged without having decoded it — there is no other route to
re-creating a layer under this specification.

**Answer: No. Governing rule: `[R-WRT-07]` (§20.5) — "what it re-creates it
decodes as a reader ... and writes as a creator" — read together with
`[R-CNF-11]` (an updater is a reader of what it processes) and `[R-CNF-03]`
(a conforming reader/updater must implement every core sample type to
decode it at all).**
Confidence: high.

---

## Q14

Future minor registers type Z, MU=1, whose registration defines that its
inline payload references another region by offset+length — one of the
specification-or-registry-defined exceptions §7.2 allows to the "MU=0
records carry no embedded file offsets" rule. Rewriter fully implements Z
and is compacting, relocating other structures.

§20.5 (immediately following `[R-WRT-06]`'s discussion of unimplemented
MU=1 types): "No other record payload carries a file offset: MU = 0
records by rule (§7.2), and an MU = 1 type the rewriter does not implement
never reaches this step (`[R-WRT-06]`). **An MU = 1 type it *does*
implement is the remaining case, and §7.2 admits it — such a type carries
further references where this specification or registry review defines
them — so a rewriter implementing one relocates whatever that registration
defines, on the same terms as the tile index.**"

This is explicit: a rewriter that implements an MU=1 type carrying its own
internal file references (like the tile index does) is permitted — indeed
expected, "on the same terms as the tile index" — to relocate the
referenced region and re-point type Z's own reference, exactly as it
regenerates a tile-index region whose stored extents move (`[R-WRT-07]`).

**Answer: may relocate and re-point the reference**
Confidence: high.

---

## Q15

Tool opens an existing conforming file, fully decodes every layer, and
produces a wholly new file: fresh file_id; flags=0 (does NOT carry forward
the input's unknown ignore-lane bits); every tile re-encoded under
different tiling/codec; omits the input's file-scope user-metadata record
entirely (neither retained byte-identically nor re-emitted as a modified
version). Every layer's reference array is bit-for-bit identical to the
input's corresponding layer.

§20.1, `[R-WRT-01]`: "A writer of a new file from an existing one takes one
of two positions, and the choice is its own. As a **rewriter** it
undertakes to preserve its input: §20.4's table for every record, the
unknown ignore-lane bits (`[R-CNT-08]`), and §20.5 whole ... As a
**creator** it undertakes nothing toward its input, whatever it read: §20.2
binds it, **it writes flags = 0**, and it answers for every byte of its
output (`[R-CNF-05]`), bytes it copied from another file included."

This tool's actual behavior matches the creator description exactly, not
the rewriter's: it writes flags=0 rather than carrying forward the input's
unknown ignore-lane bits (which `[R-WRT-06]` would require of a rewriter —
"The output trailer MUST copy the input's unknown ignore-lane flag bits
forward and set no other"), and it drops the file-scope user-metadata
record outright, which §20.4 never licenses for any updater ("A commit
never removes a user-metadata record from a scope it keeps: a top-level one
from the file"). A tool behaving this way is not undertaking §20.4's/§20.5's
preservation obligations at all — it is exercising the creator's
"undertakes nothing toward its input" position. The fact that the output's
reference arrays happen to be bit-identical to the input's is consistent
with either tier and does not itself make the tool a rewriter (a creator
may of course also compute the very same values from what it decoded).

**Answer: creator; no, it owes no preservation obligations (a creator's
§20.2 obligations run only to its own output, per `[R-CNF-05]`/`[R-WRT-01]`;
the §20.4/§20.5 preservation duties bind only an updater — appender or
rewriter — and this tool's flags=0 and dropped file-scope metadata are
exactly the creator's signature, not an updater's).**
Confidence: high.

---

## Disclosure note

No context outside the one permitted file was used to derive any answer.
The runtime placed a CLAUDE.md pointer, a user MEMORY.md index (entries
about "TARN" topics), git status/log, and an attribution reminder into this
session's context before the task began; none of that material was read
further, consulted, or relied on for any answer above — every citation
above is to `spec/tarn.md` itself, verified by direct quotation and (where
applicable) independent local arithmetic/CRC computation. No other
project file was opened. The two output-directory instructions (do not
read/list `out/` or the scratch root) were followed; only this session's
own scratch subdirectory was written to.
