# Round 19 — quiz key transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(via `sed -n`/`grep` through Bash, in sequential line ranges, plus `wc`).
I read no ADRs, no PLAN.md, no AGENTS.md, no conformance directory, no
registry.json, no git history, no web. I listed no directories other than
creating my own scratchpad. I ran one local Python script
(`scratchpad/calc.py`) that reads no files: a CRC-32C implementation
(reflected Castagnoli 0x82F63B78, init/final 0xFFFFFFFF) plus integer
arithmetic. I validated that implementation against the three CRC
constants the document itself publishes before using it:
CRC-32C("123456789") = 0xE3069283 (§4.5), CRC-32C over 80 sentinel bytes
= 0x80A34955 and crc_of_crc_array = 0xC4EE982E (§7.4's worked example),
CRC-32C of a full 2^16-entry all-sentinel segment = 0xEECB3BB2 (§15.4).
All four reproduced exactly.

---

## Q01 — compactor's output flags and minimum version_minor

Input X: version_major 1, version_minor 3, flags 0x00140000 = bits 18 and
20, both inside the **ignore lane** (§6.2's trailer table: "bits 0–15
incompat lane; bits 16–31 ignore lane"). The compactor implements no flag
bits, so both are unknown to it. X is conforming — §21.6: "An ignore-lane
flag bit (16–31) is set | Ignored; the file is conforming".

**(a)** `[R-WRT-06]` (§20.5): "The output trailer MUST copy the input's
unknown ignore-lane flag bits forward, in place of the flags = 0 §6.3
requires of a file created under this text (`[R-CNT-08]`)." §6.3 says the
same: "A compactor, though its output is a new file, carries the input's
unknown ignore-lane bits into its output trailer rather than writing
flags = 0."

So output flags = 0x00140000. u32, little-endian (`[R-ENC-01]`):
0x00140000 → `00 00 14 00`.

**(b)** `[R-WRT-06]`: "Where the output carries a feature a later minor
defines and this compactor does not — on a conforming input a carried
ignore-lane bit (§6.3) ... — the output's version_minor SHOULD be at
least the input's". That condition is met here (a carried ignore-lane
bit the compactor does not implement). "Otherwise version_minor follows
`[R-CNT-26]`'s floor" — but we are not in the otherwise branch.

The question asks for the smallest value deviating from no requirement
**or recommendation**, so the SHOULD binds: version_minor ≥ 3.
Smallest = **3**.

**Answer:** `00 00 14 00`, 3.

---

## Q02 — three inputs to a compactor implementing only 0x0001 and 0x0002

**(a)** Entry offset = 0xFFFF_FFFF_FFFF_FFFF (= S), length = 0x40 (≠ S),
crc = 0. §15.3's table: "offset = S ∧ length ≠ S, or offset ≠ S ∧
length = S | *structural*: reject-tile". Register row T7.

§20.5, `[R-WRT-07]`'s regeneration paragraph: "An entry §15.3 classifies
reject-tile on a structural ground is neither — `[R-IDX-03]` gives it no
stored extent for a re-pointing to target — so regenerating the region
cannot proceed without meeting it, and the violation is thereafter one
the compactor has detected. `[R-WRT-06]` then obliges refusal: the
compactor can neither reproduce the entry nor invent a replacement, and
no drop is available, a tile-index entry being no record §20.4's table
licenses dropping."

→ **refuse**.

(Premise noted: the refusal runs through regeneration of the region.
§20.5 states a compactor "preserves content but not placement — placement
is not among the things it carries forward", and `[R-WRT-09]` obliges it
to rely structurally on every structure it copies, so it reads the entry
to relocate the extent either way. Both routes land on refuse.)

**(b)** Type 0x8123 ≥ 0x8000 = experimental range (§10.2's table). MU = 0.
§21.6: "A record type this specification has not assigned, from the
experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and
preserved or dropped per its PE bit" — the file is conforming.
`[R-WRT-06]`'s refusal clause reaches only "any record whose type it does
not implement with MU = 1". §20.4's table, MU = 0 / PE = 0 row: "Retain
byte-identical, or drop it — its extent becoming slack. ... A compactor
MAY drop it whenever it rewrites the file." §7.2 makes the extent
relocatable without parsing ("neither its inline payload nor its extent
contents encode offsets or lengths of other file bytes — this is what
lets a compactor relocate an unknown ancillary's extent without parsing
it").

→ **compact**.

**(c)** Type 0x9000, experimental, MU = 1. `[R-WRT-06]`: "A compactor
MUST refuse to compact a file carrying any record whose type it does not
implement with MU = 1: such a type can define references this
specification does not (§7.2), so its bytes cannot be safely relocated."
§21.6 confirms the file is conforming all the same ("an
experimental-range record type carrying MU = 1 ... `[R-CNT-15]` obliges
the reader to reject, and `[R-CNF-02]` makes the file conforming").

→ **refuse**.

**Answer:** refuse, compact, refuse.

---

## Q03 — verdict and slack for the 192-byte empty file

Gates in §6.2's order (`[R-CNT-06]`): magic ✓; trailer CRC ✓; version
gate — major 1 ✓, minor never gates (`[R-CNT-07]`); flags 0 ✓;
committed_file_length 192 = file size ✓, 192 mod 64 = 0 ✓; dir_offset
16 ≥ 16 ✓; dir_length 4 ≥ 4 ✓; 16 + 4 = 20 ≤ F − 64 = 128 ✓;
generation 1 ✓; file_id ≠ 0 ✓; reserved zero ✓. Front block ✓
(`[R-CNT-04]`). Directory CRC: zero-byte record sequence, CRC-32C of
zero bytes = 0x00000000 (§4.5) = bytes [16,20) ✓. Zero records is
valid — §21.6: "The file contains zero layers | A conforming file with
an empty directory". File size 192 ≥ 128 (`[R-CNT-27]`) ✓.

The pre-trailer gap is [20, 128) = 108 bytes, far longer than
`[R-LIF-02]` step 5's pad (which would reach 64). §6.2 `[R-CNT-05]`:
"a longer gap is conforming, and no conforming commit produces one."
`[R-CNF-02]` names this case explicitly among the writer obligations
whose violation is *not* a file-conformance violation: "§6.3's flags = 0
against a set ignore-lane bit and §6.2's pre-trailer gap longer than
`[R-LIF-02]` step 5's pad are the cases this text states". No structure
lies in the gap, so F7 does not fire.

→ verdict **conforming**.

Slack (§5.2 `[R-CNT-21]`, §9.7 `[R-LIF-08]`): claimants are the front
block [0,16), the directory [16,20), and the live trailer [128,192).
The walk completes, so the total is exact, not partial.
192 − 16 − 4 − 64 = **108**.

**Answer:** conforming, 108.

---

## Q04 — crc_of_crc_array for an all-sentinel rank-1 layer

d = 1, E = 70, T = 32. G = ⌈70/32⌉ = 3 (§11.2). N = 3. Interleaved, so
addressed-tile count = N = 3 (`[R-GEO-03]`), entry_count = 3.

Index region (§15.1): entry array 3 × 20 = 60 bytes, all sentinel
`FF ×16 00 ×4` (`[R-IDX-02]`); segment CRC array ⌈3/2^16⌉ × 4 = 4 bytes.
The single segment is **partial** (3 < 2^16), so `[R-IDX-05]`'s
0xEECB3BB2 constant does not apply — "a partial segment's CRC MUST be
computed."

CRC-32C over the 60 sentinel bytes = 0xD171D122 (stored `22 d1 71 d1`).
crc_of_crc_array = CRC-32C over that 4-byte array = 0x34C74AFB.

u32 little-endian on disk: **`fb 4a c7 34`**.

(Method validated: the same code gives 0x80A34955 / 0xC4EE982E for
§7.4's 4-entry example, and 0xEECB3BB2 for a full segment.)

---

## Q05 — the 20-byte index entry for a planar bool edge tile

Geometry: E = (5,5), T = (3,3) → G = (2,2), N = 4, P = 9.
Planar, C = 1 → addressed tiles = C·N = 4.
Tile (1,1): s = 1·2 + 1 = 3 (`[R-GEO-06]`); disk ordinal = 0·4 + 3 = 3.

Decoded tile image: planar bool plane → §14.3 packed, ⌈P/8⌉ = ⌈9/8⌉ = 2
bytes.

Tile (1,1) covers y ∈ [3,6), x ∈ [3,6). Real positions need y < 5 and
x < 5, i.e. u_y ≤ 1 and u_x ≤ 1. In-tile ordinal k = u_y·3 + u_x
(§11.4, row-major in every linearization):

| k | (u_y,u_x) | (y,x) | real? | bit |
|---|---|---|---|---|
| 0 | (0,0) | (3,3) | real | 0 (false) |
| 1 | (0,1) | (3,4) | real | 0 |
| 2 | (0,2) | (3,5) | padding | 1 (fill) |
| 3 | (1,0) | (4,3) | real | 0 |
| 4 | (1,1) | (4,4) | real | 0 |
| 5 | (1,2) | (4,5) | padding | 1 |
| 6 | (2,0) | (5,3) | padding | 1 |
| 7 | (2,1) | (5,4) | padding | 1 |
| 8 | (2,2) | (5,5) | padding | 1 |

`[R-SER-05]`: "at every padding position, a writer MUST encode ... the
fill bit in a packed plane." Fill byte 0x01 = true, so fill bit = 1.

Byte 0 = bits 0..7 = 0,0,1,0,0,1,1,1 → 4+32+64+128 = 0xE4.
Byte 1 = bit 0 (value 8) = 1; P mod 8 = 1 so bits 1–7 are pad bits, each
carrying the fill bit (`[R-SER-03]`, `[R-SER-05]`) = 1 → 0xFF.

Decoded image = `E4 FF`. Filter 1 (identity) then codec 1 (none), so
stored bytes = `E4 FF`, length 2 — which `[R-COD-04]` requires to equal
the decoded size ✓.

CRC-32C(`E4 FF`) = 0x69C99AA0.

Entry (§15.1: offset u64, length u64, crc u32, all little-endian):
`00 02 00 00 00 00 00 00` `02 00 00 00 00 00 00 00` `a0 9a c9 69`.

---

## Q06 — inline_length and extent_length for layer `air`

Inline payload, §7.4's table order, packed with no padding:

- name `air`: 1 + 3 = 4
- layout u8 1, linearization u16 2, codec u16 2, filter u16 2,
  A u64 8, S u64 8, A_slab u64 8, rank u8 1, C u16 2 = 34
  (matches §7.4's example: "Name and the nine scalars from layout
  through channel count occupy 4 + 34 bytes")
- 3 dimension entries, names `t`,`y`,`x` (1 byte each):
  3 × (1+1 + 8 + 8) = 3 × 18 = 54
- 2 channel entries:
  `u` float64 → (1+1) + 2 + (1+8) = 13;
  `flag` bool → (1+4) + 2 + (1+1) = 9; total 22
- trailing: index_encoding 1 + entry_count 8 + crc_of_crc_array 4 = 13
- sub-records: one user-metadata sub-record = 24-byte header + 1 byte
  inline payload = 25

4 + 34 + 54 + 22 + 13 + 25 = **152**.

Geometry: T = (1,50,50), E = (10,100,100) → G = (10, 2, 2), N = 40.
Layout 1 = interleaved → addressed tiles = N = 40 = entry_count.

`[R-CNT-17]`: extent_length = 40 × 20 + ⌈40/2^16⌉ × 4 = 800 + 4 = **804**.

---

## Q07 — three verifier verdicts on user-metadata encodings

**(a) 0x91 (≥ 0x80, experimental).** §21.6: "A user-metadata record
declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming ... No document rule attaches at
such an encoding, so a verifier certifies, reporting the record it
ignored". `[R-MTA-10]`: "A verifier meeting such a record in an otherwise
conforming file has no requirement it is unable to check — the record is
not among `[R-CNF-11]`'s cannot-establish grounds, and certification is
unaffected." → **conforming**.

**(b) 0x05 (reserved range 3–0x7F).** Register row R1: "A user-metadata
record declares a document encoding of 0, or a reserved-range value
(3-0x7F)". §21.5: "Every row here is a violation all the same: the
outcome bounds a reader's blast radius and never makes the file
conforming (`[R-CNF-12]`)." §21.5 restates it: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as
violations: what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set". A verifier that established a
violation reports nonconforming (`[R-CNF-11]`). → **nonconforming**.

**(c) 0x02, decodes to 20 MiB, verifier declines at its 16 MiB bound.**
`[R-MTA-09]`: "A **verifier** that declines to decode a document on the
bound above cannot establish that document's conformance and MUST NOT
certify the file ... it fixes the file's verdict as *cannot establish*
only where the verifier established no violation elsewhere". Nothing else
is unchecked and nothing else is violated. → **cannot establish**.

**Answer:** conforming, nonconforming, cannot establish.

---

## Q08 — entry_count, extent_length, segment index

G_y = G_x = ⌈100000/256⌉ = 391 (390·256 = 99,840 < 100,000).
N = 391² = 152,881. Planar, C = 3 → entry_count = C·N = **458,643**.

`[R-CNT-17]`: 458,643 × 20 = 9,172,860; ⌈458,643/65,536⌉ = 7
(65,536 × 7 = 458,752 ≥ 458,643 > 65,536 × 6 = 393,216); 7 × 4 = 28.
extent_length = **9,172,888**.

Coordinate (50000, 60000): t_y = 50000 div 256 = 195,
t_x = 60000 div 256 = 234 (`[R-GEO-06]`).
s = t_y·G_x + t_x = 195·391 + 234 = 76,245 + 234 = 76,479.
Planar disk ordinal for channel 2 = c·N + s = 2·152,881 + 76,479
= 305,762 + 76,479 = 382,241.
§15.4: segment s covers entries [s·2^16, …) → 382,241 div 65,536 = **5**
(65,536·5 = 327,680 ≤ 382,241 < 393,216).

---

## Q09 — three planar channel reads

- **Channel 0**: well-formed entry, crc matches, decodes to exactly the
  decoded size → §19.4 steps 5–8 complete → **decoded**.
- **Channel 1**: `FF ×16 00 ×4` = offset S, length S, crc 0 = the
  sentinel (`[R-IDX-02]`). §15.3's first row: "valid sentinel — reads as
  fill"; `[R-TYP-08]`, and §19.4 step 4: "A valid sentinel short-circuits
  steps 5 and 6 for that entry ... the entry's channel's recorded fill in
  a planar layer" → **fill**.
- **Channel 2**: offset = S, length = 0x40 ≠ S → §15.3 "*structural*:
  reject-tile". `[R-CNF-09]`: "a read of a rejected tile MUST NOT
  silently return fill"; `[R-TYP-09]` likewise. §19.4 step 4: "a rejected
  tile's read reports failure, and fill is never a failure fallback"
  → **failure**.

**Answer:** decoded, fill, failure.

---

## Q10 — zstd smallest-window frame on a 30-byte tile

Interleaved, T = (2,3) → P = 6. Channels `t` float32 (4) + `m` bool (1)
→ Q = 5. Decoded size = P·Q = 30 (§14.2 — this is verbatim §14.2's own
worked example: "With channels `t` (float32) and `m` (bool) interleaved
instead: Q = 5, decoded size 30").

Single_Segment_Flag clear ⇒ a Window_Descriptor is present. §17.2's Note:
"without it, the Window_Descriptor cannot express less than 1 KiB. A tile
whose decoded size is below 1 KiB — §14.2's worked examples give 18 and
30 bytes ... — is therefore encodable under codec 3 only as a
single-segment frame". So the declared Window_Size is 1024 > 30.

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the
tile's decoded size; a reader MUST treat either as a validity error at
tile scope, both being header-checkable."

Every other listed feature is clean: magic present (not T17), one frame
(not T18), dictionary ID zero (not T19), content-checksum flag clear
(not T20), decodes to exactly the decoded size consuming the extent
exactly (not T3/T24/T25), crc matches (not T1).

Outcome class (§2.4's four): **reject-tile**.
Register row (§21.4): **T21** — "Codec 3 (zstd) and the frame declares a
window size larger than the tile's decoded size".

---

## Q11 — decoded size and bytes 5–9

Interleaved, T = (4,4) → P = 16. Q = B_a + B_b = 1 + 4 = 5.
Decoded size = P·Q = **80** (§14.2's table, interleaved row).

Offset of value k = (k div C)·Q + F_{k mod C}, with C = 2, F_0 = 0,
F_1 = 1. Bytes [5,10) are the sample at in-tile ordinal 1: `a` at byte 5,
`b` at bytes 6–9.

In-tile ordinal 1 = (u_y, u_x) = (0, 1) since ordinal = u_y·4 + u_x.
Tile (1,1) covers y ∈ [4,8), x ∈ [4,8) → the coordinate is (y,x) = (4,5).
E = (5,5), so x = 5 ≥ E_x: this is a **padding position** (§11.3).

`[R-SER-05]`: "at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value — the recorded
fill bytes for a numeric channel". `a` fill = 0x2A → `2a`.
`b` fill = the bit pattern 0xBF800000 (float32, −1.0), stored
little-endian (`[R-ENC-01]`, §12.3's worked channel entry) → `00 00 80 bf`.

Bytes 5–9: **`2a 00 00 80 bf`**.

---

## Q12 — dir_offset, dir_length, committed_file_length

The §7.4 layer: entry_count = 4, inline payload 81 bytes.
`[R-CNT-17]`: index extent_length = 4 × 20 + ⌈4/2^16⌉ × 4 = 84
(the example states this: "an extent slot of length 4 × 20 + ⌈4/2^16⌉ × 4
= 84").

Index region placed at [16, 100). Directory begins at the first byte
after → **dir_offset = 100**.

Directory region = record sequence + terminal CRC (§7.1). One layer
record = 24-byte header (§7.2) + 81 inline = 105 bytes.
**dir_length = 105 + 4 = 109**. Directory ends at 100 + 109 = 209.

`[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary".
Next 64-boundary above 209 is 256 → 47 pad bytes. Trailer [256, 320).
**committed_file_length = 320** — multiple of 64 ✓, and
dir_offset + dir_length = 209 ≤ F − 64 = 256 ✓ (`[R-CNT-06]`).

---

## Q13 — permitted shrink; erasure claim

Before: E = (64,64), T = (16,16) → G = (4,4), N = 16, every tile stored.
After: E = (64,32) → G = (4,2), N = 8.

**(a)** §20.3 step 4: "An extent MAY also **shrink**, and the bar above is
the whole of the test, **in the bar's own tense**: a shrink is permitted
exactly where it alters nothing §14 fixes for any tile the layer stores
in the generation this commit supersedes. Dropping a tile out of the
addressed set (§11.2's grid count falls) is not itself such an
alteration — a tile the new state does not address carries no §14
obligation and its extent becomes slack".

Test on each prior-generation stored tile that survives (t_x ∈ {0,1}):
G_x·T_x = 2·16 = 32 = E_x exactly, so no padding positions appear (there
were none before either, 4·16 = 64 = old E_x); decoded size P·Q is
unchanged (T and channel types unchanged); sample byte offsets unchanged;
codec and filter unchanged. Nothing §14 fixes is altered. The de-addressed
tiles (t_x ∈ {2,3}) simply leave the addressed set.

Ordinal renumbering is expressly contemplated: step 4, "every other entry
byte-identical at its disk-ordinal position (a geometry change renumbers
ordinals wherever `[R-GEO-06]` moves them)", and `[R-CNT-17]` forces the
smaller entry_count and hence the full index re-emission the question
describes. → **yes**.

**(b)** `[R-PRV-01]`: "A commit removes sample data two ways —
superseding it, and a shrink that de-addresses tiles (§20.3 step 4) ...
In each case the bytes remain in the file as slack (`[R-CNT-21]`) ...
Writers and the tools built on them MUST NOT represent any commit that
makes sample data unreachable as erasure of it — a shrink reported as
erasure misleads exactly as a supersede so reported does." → **no**.

**Answer:** yes, no.

---

## Q14 — Appendix G item 2 applied to Appendix A's file

Item 2: "its input the bytes [0, F − 64) followed by the trailer's first
60 bytes with the `file_id` field zeroed".

F = 128 (Appendix A). [0, F − 64) = [0, 64) = 64 bytes. Plus the trailer's
first 60 bytes = 60. Total hash input = **124 bytes**.

The eight bytes taken as zero are the `file_id` field, at trailer offset
48, size 8 (§6.2's layout table). Within the hash input the trailer's
bytes begin at input offset 64, so file_id occupies
[64 + 48, 64 + 56) = **[112, 120)**.

(On this particular file the in-file range coincides — the trailer starts
at 64 and Appendix A annotates file bytes [112,120) as file_id — so the
two readings of "measured within" agree and nothing is underdetermined.)

---

## Q15 — the row §21.7 names for a codec 3 → codec 1 redeclaration

§21.7: "§20.3 step 4's bar on a declaration change is witnessed only
where the affected tiles remain stored *and* the change reaches a byte
§14 structurally constrains ... a change that reaches the decoded size
instead is witnessed by T3 or T14 ... and a change that reaches the codec
is witnessed by the rows for the codec now declared, which test the
stored bytes as a stream of it (T15, T17, T23, T25), **or by T14 where
the new declaration is codec 1**".

The new declaration is codec 1. → **T14**.

(T14: "Codec 1 (none) declared and a non-sentinel index entry's length
differs from the tile's decoded size" — the carried-forward zstd-
compressed stored bytes will not have length equal to the decoded size,
`[R-COD-04]`.)
