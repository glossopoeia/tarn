# Cleanroom round 22 — quiz keyer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,394 lines, in four `Read` calls). No other file in the repository was
read or listed; no git history; no web access; no ADRs, vectors, tooling,
registry, PLAN, AGENTS, README.

Ran two local Python scripts I wrote myself, in the scratchpad, reading no
project files: `calc.py` (arithmetic + CRC-32C) and `verify.py` (validating my
CRC-32C against four constants the specification itself publishes).

**Contamination note.** My runtime placed a `claudeMd` block and an index of the
maintainer's auto-memory files in my context before I began — memory-file titles
referencing TARN working cadence, a naming constraint, workflow verifier
failures, spec-edit propagation, and a register/corpus relationship. I did not
open any of those files and did not use any of it. It named nothing I used to
answer a question.

## CRC-32C implementation validation

My table-driven CRC-32C (reflected poly 0x82F63B78, init 0xFFFFFFFF, xorout
0xFFFFFFFF) reproduces every constant the document publishes:

| Input | Computed | Spec |
|---|---|---|
| `"123456789"` | 0xE3069283 | §4.5 check vector |
| zero bytes | 0x00000000 | §4.5 |
| Appendix A trailer [0,60) | 0xE00938D2 | Appendix A |
| 4 sentinel entries (80 bytes) | 0x80A34955 | §7.4 example |
| CRC of that 4-byte array | 0xC4EE982E | §7.4 example |
| 2¹⁶ sentinel entries | 0xEECB3BB2 | §15.4, Appendix B |

---

## Q01 — channel entries and inline_length

§7.4's field table gives the inline payload order. Field widths from the same
table; §12.1 gives element sizes; §13.2 constrains a bool fill byte.

**(a) The two channel entries.** Channel entry = `name (u8 len + bytes) · type
u16 (0 invalid) · fill (u8 len + bytes)`, and `[R-CNT-23]`: "fill length equals
the type's element size".

- `a`, bool: type ID 1 (§12.1), element size 1, fill true = `0x01` (§13.2:
  "`0x00` (false) or `0x01` (true)"). → `01 61 01 00 01 01`
- `b`, uint16: type ID 7 (§12.1), element size 2, fill 0x1234 little-endian
  (`[R-ENC-01]`) = `34 12`. → `01 62 07 00 02 34 12`

Concatenated: `01 61 01 00 01 01 01 62 07 00 02 34 12` (13 bytes).

Cross-check against §12.3's worked example: `04 74 65 6D 70 0C 00 04 00 00 C0
7F` — name len, name, type LE u16, fill len, fill bytes. Same shape.

**(b) inline_length.**

Geometry first, for entry_count: G_y = ⌈4/2⌉ = 2, G_x = ⌈6/3⌉ = 2, N = 4
(§11.2). Planar ⇒ addressed-tile count = C·N = 2·4 = 8, and `[R-CNT-17]`
requires entry_count to equal it. entry_count = 8.

| Region | Bytes |
|---|---|
| name `m` (1 + 1) | 2 |
| layout(1) lin(2) codec(2) filter(2) A(8) S(8) A_slab(8) rank(1) C(2) | 34 |
| 2 dimension entries, (1+1)+8+8 = 18 each | 36 |
| 2 channel entries, 6 + 7 | 13 |
| index_encoding(1) entry_count(8) crc_of_crc_array(4) | 13 |
| sub-records | 0 |
| **total** | **98** |

The 34 and the 18 and the 13 are exactly the figures §7.4's worked example
states ("Name and the nine scalars from layout through channel count occupy
4 + 34 bytes, the dimension entry 18, … and the trailing fixed fields 13").

**inline_length = 98.** Confidence: high.

---

## Q02 — last four bytes of the file

§9.2's creation path: front block, then steps 2–6, generation 1.

Layout:
- front block [0, 16)
- user-metadata extent [16, 56) — 40 bytes at offset 16
- directory at dir_offset = 64: one record = 24-byte header (§7.2) + inline
  payload. `[R-MTA-03]`: "A user-metadata record's inline payload is exactly
  one byte", so inline_length = 1 ⇒ record is 25 bytes. Plus the region's
  terminal CRC-32C, 4 bytes (§7.1). **dir_length = 29**, region [64, 93).
- pad: `[R-LIF-02]` step 5, "append the pad to the next 64-byte boundary" ⇒
  [93, 128), 35 bytes.
- trailer [128, 192). **F = 192**, a multiple of 64 (§6.2). ✓
  dir_offset + dir_length = 93 ≤ F − 64 = 128 ✓.

The last four bytes are trailer [60, 64) = "CRC-32C over trailer bytes [0, 60)"
(§6.2 layout table).

Trailer [0,60):
```
8a 4e 52 41 54 0d 0a 1a  01 00 00 00 00 00 00 00
01 00 00 00 00 00 00 00  40 00 00 00 00 00 00 00
1d 00 00 00 00 00 00 00  c0 00 00 00 00 00 00 00
18 07 f6 e5 d4 c3 b2 a1  00 00 00 00
```
(magic; version_major 1; version_minor 0; flags 0; generation 1; dir_offset 64;
dir_length 29; committed_file_length 192; file_id 0xA1B2C3D4E5F60718 LE;
reserved 0.)

CRC-32C = 0xB17DAE50, stored little-endian (`[R-ENC-09]`).

**Answer: `50 ae 7d b1`.** Confidence: high.

---

## Q03 — zstd Frame_Content_Size mismatch on a metadata document

Frame declares FCS 4,096; the document decodes to 4,000 bytes. §18.2
`[R-MTA-09]`: "The frame's content-size field … MAY be present, and when
present it MUST equal the byte length of the decoded document. **A mismatch is
a failure to decode within the meaning of R3**".

So the row is **R3**, not R4: R4's own instance list is magic / skippable /
second frame / dictionary ID / content-checksum flag / trailing bytes, all of
which this file satisfies. The extent CRC verifies, so not R2. The document's
own content is clean, so not R5–R10.

§21.5 heading fixes the outcome for every row in it: **ignore-record**. R3's
row cells give Detector **reader** and Detected **extent use**.

(a) R3 (b) ignore-record (c) reader (d) extent use. Confidence: high.

---

## Q04 — 16 MiB window on a metadata frame, verifier bound 8 MiB

§21.9's guarantee row: zstd frame `Window_Size` — 8 MiB. §18.2 `[R-MTA-09]`:
"The frame's declared `Window_Size` is unconstrained here … a frame declaring
more than the reader admits is ignore-record on that ground — the reader's
capability, not a failure to decode within the meaning of R3, and **no
violation: the file exceeds a §21.9 guarantee and so remains conforming** while
the reader MAY decline it".

(a) **conforming**.

(b) Same rule: "A **verifier** that declines to decode a document on the bound
above cannot establish that document's conformance and MUST NOT certify the
file … it fixes the file's verdict as *cannot establish* only where the
verifier established no violation elsewhere". None established here ⇒
**cannot establish**. (§21.5's preamble confirms the window bound is one of
the two decline grounds: "except where a reader or verifier declines the decode
on the size bound or on the frame's declared window".)

(c) A conforming reader with the same bound: **ignore-record** (quoted above).

Confidence: high.

---

## Q05 — rank 40, one zero-extent dimension

Geometry: G₀ = ⌈0 / 67,108,864⌉ = 0, so N = ∏Gᵢ = 0; interleaved ⇒
addressed-tile count 0; entry_count = 0; extent slot (0,0) and
crc_of_crc_array 0 (§7.4, `[R-CNT-17]`, `[R-CNT-23]`).

**(a)** `[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is 0,
the layer has zero addressed tiles… Readers MUST accept such a layer." Rank
40 ≤ 255 (§7.4's u8), tile extents ≥ 1, C ≥ 1 — `[R-GEO-01]`'s floor holds.
Codec 1, so `[R-COD-07]`'s lz4 cap is not engaged at all. P = 2²⁶,
P·Q = 2²⁶·8 = 2²⁹, well under 2⁶³ − 1 (`[R-ENC-04]`). **conforming**.

**(b)** Walking §21.9's table:

- *rank d of a layer* — 32 guaranteed; declared 40. **Exceeds.**
- *channels per layer, C* — 4096; C = 1. No.
- *addressed tiles per layer (entry_count)* — 2³²; 0. No.
- *layers per file* — 65,536; one. No.
- *size of the directory region, dir_length* — 16 MiB; tiny. No.
- *decoded size of one tile* — 256 MiB. Declarations would derive
  P·Q = 2²⁹ = 512 MiB, but the row is per-instance: "they range over the
  tiles … a file actually contains, and a file containing none of a kind does
  not exceed that row, **whatever its declarations would derive** — a layer
  addressing no tile (§11.2) has no tile whose decoded size the table can
  bound". This layer addresses none. **Does not exceed.** (This is the trap in
  the question, and the spec closes it explicitly.)
- *decoded size of one user-metadata document* — none present. No.
- *zstd frame `Window_Size`* — none present. No.

**(a) conforming; (b) rank d of a layer.** Confidence: high.

---

## Q06 — planar geometry arithmetic

G = (⌈100/10⌉, ⌈200/64⌉, ⌈300/64⌉) = (10, 4, 5); N = 200 (§11.2).

(a) planar addressed-tile count = C·N = 3·200 = **600**.

(b) `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 600·20 + 1·4 = **12,004**.

(c) tᵢ = xᵢ div Tᵢ = (5, 2, 3). `[R-GEO-06]`: s = Σ tᵢ·∏_{j>i} Gⱼ
= 5·(4·5) + 2·5 + 3 = 100 + 10 + 3 = 113. Planar disk ordinal = c·N + s
= 2·200 + 113 = **513**.

(d) uᵢ = xᵢ mod Tᵢ = (5, 2, 8). In-tile ordinal = Σ uᵢ·∏_{j>i} Tⱼ
= 5·(64·64) + 2·64 + 8 = 20,480 + 128 + 8 = **20,616**.

Confidence: high.

---

## Q07 — packed planar bool tile with padding

G = (⌈3/3⌉, ⌈2/3⌉) = (1, 1); N = 1; one channel planar ⇒ one addressed tile.
P = ∏Tᵢ = 9. Planar bool ⇒ §14.3 packed plane, decoded size ⌈9/8⌉ = **2**.

In-tile ordinal (§11.4) = u₀·T₁ + u₁ = 3u₀ + u₁. Layer extent along x₁ is 2, so
every position with u₁ = 2 is a **padding position** (§11.3), and `[R-SER-05]`
fixes its content to the channel's fill — here the fill **bit**, true.

| ordinal | (u₀,u₁) | value | source |
|---|---|---|---|
| 0 | (0,0) | false | data |
| 1 | (0,1) | true | data |
| 2 | (0,2) | true | padding → fill |
| 3 | (1,0) | true | data |
| 4 | (1,1) | false | data |
| 5 | (1,2) | true | padding → fill |
| 6 | (2,0) | false | data |
| 7 | (2,1) | true | data |
| 8 | (2,2) | true | padding → fill |

§14.3: "value k occupies bit k mod 8 of byte k div 8". Byte 0 has bits
1,2,3,5,7 set = 0x02+0x04+0x08+0x20+0x80 = **0xAE**. Byte 1 carries value 8 in
bit 0; P mod 8 = 1, so bits 1–7 are pad bits, and `[R-SER-05]`: "Every pad bit
(§14.3) MUST carry the plane's channel's fill bit" = 1 ⇒ **0xFF**. (§14.3's own
example shows the same mechanic: fill true gives `55 FD`.)

(a) `ae ff`.
(b) Codec 1 and filter 1, so `[R-COD-04]`: "The index entry's length therefore
MUST equal the tile's decoded size". Length = **2**.

Confidence: high.

---

## Q08 — interleaved sample offset and bytes

Element sizes (§12.1): uint8 1, float32 4, int16 2. Q = ΣBᵢ = **7**
(§14.2's sample stride). Tile extents (2,4) ⇒ P = 8; decoded size P·Q = 56.

Tile extents equal the extents, so (1,2) is in the single tile at in-tile
position (1,2); in-tile ordinal u = 1·4 + 2 = 6.

§14.2's closing form: "channel c's value at in-tile ordinal u sits at byte
u·Q + Fᶜ", so the sample's first byte (c = 0, F⁰ = 0) is at u·Q = 6·7 = **42**.

Bytes, in declared channel order, each little-endian (`[R-ENC-01]`):
- `a` uint8 0x2A → `2a`
- `b` float32 1.5 = 0x3FC00000 → `00 00 c0 3f`
- `c` int16 −3 = 0xFFFD (two's complement) → `fd ff`

(a) **42**; (b) **`2a 00 00 c0 3f fd ff`**. Confidence: high.

---

## Q09 — all-ones offset/length with nonzero crc, in a slab layer

§15.3's second row: "offset = S ∧ length = S ∧ crc ≠ 0 | *structural*:
reject-tile". Register row: **T6** — "A tile-index entry has offset and length
both 0xFFFF_FFFF_FFFF_FFFF but crc ≠ 0".

(b) §9.7 `[R-LIF-08]`: "an entry `[R-IDX-03]` classifies reject-tile on a
*structural* ground contributes no stored extent to the walk". → **no**.

(c) §16.2 `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile on a
*structural* ground: they address no usable extent, and the run's stored tiles
close over them." → **no**.

(d) §20.5: "An entry §15.3 classifies reject-tile on a structural ground is
neither — `[R-IDX-03]` gives it no stored extent for a re-pointing to target —
so regenerating the region cannot proceed without meeting it… `[R-WRT-06]`
then obliges **refusal**: the compactor can neither reproduce the entry nor
invent a replacement, and no drop is available". One word: **refuse**.

Confidence: high.

---

## Q10 — reserved-range sub-record type 0x0500, MU = 0

0x0500 lies in §10.2's record-type **reserved** range 0x0003–0x7FFF.

(a) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer …
with MU = 0 it is **ignore-record**." `[R-EXT-03]` routes a reserved value to
that same treatment ("`[R-CNT-18]` for layer sub-records").

(b) `[R-CNT-15]`: "one from the reserved range is a value this specification
has not assigned — **emitting it is a violation**, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing
scope." → **nonconforming**. (Contrast §21.6, which makes only the
*experimental* range a non-violation.)

(c) **L25** — "A layer record's sub-record carries a type value from the
reserved range 0x0003-0x7FFF … emitting one is a violation whatever its MU
bit". L24 is its MU = 1 specialization (§21.1 names the pair) and does not
apply at MU = 0.

(d) L25's Detector cell: **verifier**.

Confidence: high.

---

## Q11 — flags = 0x00010000 from a creator implementing this text

Bit 16 ⇒ ignore lane (§6.2 layout: "bits 0–15 incompat lane; bits 16–31 ignore
lane").

`[R-CNT-08]`: "a writer creating a file under this text **MUST write flags =
0**, but a set ignore-lane bit is **not a file-conformance violation**".
`[R-CNF-02]` names this as one of the two stated conduct-not-bytes cases:
"§6.3's flags = 0 against a set ignore-lane bit … are the cases this text
states". §21.6 lists "An ignore-lane flag bit (16–31) is set | Ignored; the
file is conforming".

(a) The file has no violation and nothing is unable to be checked ⇒
**conforming**.
(b) No register row applies. F19 covers bits 0–15 only. → **no**.
(c) The writer disobeyed an all-capitals MUST (`[R-CNT-08]`, quoted). → **yes**.

This is the deliberately odd triple — a conforming file whose writer broke a
MUST — and §2.3 is explicit that the predicate binds the bytes while the
conduct rule binds the actor. Confidence: high.

---

## Q12 — slack total

Geometry: G = ⌈4/2⌉ = 2, N = 2, interleaved ⇒ entry_count = 2, and
`[R-CNT-17]` gives extent_length = 2·20 + ⌈2/2¹⁶⌉·4 = **44**, so the index
region is [3072, 3116).

§9.7 claimants (§5.2 `[R-CNT-02]`), the front block and live trailer included
("The front signature block at [0, 16) and the live trailer at [F − 64, F) are
claimed by the walk as well"). A record is not a claimant of its own — its
header and inline payload lie inside the directory region — and the layer
record's extent *is* the index region, "not a second claimant beside it":

| Claimant | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile, disk ordinal 0 | [1024, 1124) | 100 |
| stored tile, disk ordinal 1 | [2048, 2148) | 100 |
| tile-index region (layer record's extent) | [3072, 3116) | 44 |
| user-metadata record's extent | [3116, 3176) | 60 |
| directory region | [3200, 3400) | 200 |
| live trailer | [4032, 4096) | 64 |
| | | **584** |

Disjoint, and each non-terminal claimant lies in [16, F − 64) = [16, 4032). The
file is conforming and the walk completes, so the total is exact, not partial
(`[R-CNT-21]`).

Slack = F − 584 = 4096 − 584 = **3512**.
(Cross-check by gaps: 1008 + 924 + 924 + 24 + 632 = 3512.)

Confidence: high.

---

## Q13 — bad trailer CRC alongside a foreign major

§6.2 `[R-CNT-06]` fixes the order: "the trailer magic; the trailer CRC; the
version gate (§6.3) … and then, those gates passed, MUST validate all of the
following". Magic passes. The CRC fails next ⇒ that is the first violation
established, ahead of the version gate, ahead of dir_offset = 8 (F9), ahead of
generation = 0 (F11).

§21.2's preamble confirms the CRC row survives a foreign major: "Four rows are
outside that reasoning and do reach it… F8 and F1's trailer-magic instance,
**F14's trailer CRC** — the two checks §6.2 places before the gate".

(a) **F14**; (b) **reject-file** ("Any failure is reject-file", §6.2; §21.2
heading "Outcome: reject-file").

Note on the question's own wording: it calls the file "of format major version
1" and then says version_major holds 5. I answer on the stated field value.
The answer is insensitive to the tension either way, since the CRC check
precedes the version gate. Confidence: high.

---

## Q14 — dropping MU = 0 / PE = 0 records in a tile-supersede commit

Both types are ≥ 0x8000, the experimental range, and the appender implements
neither, so §20.4's stored-flags table governs, MU = 0 / PE = 0 row:

"An appender MUST NOT drop it except in a commit that *independently* changes
the scope the record attaches to: for a layer sub-record, **that layer's
record, the entry set of its index, or which of its tiles are stored**; for a
top-level record, the file's layer set, **any layer record's content**, or
another *non-layer* top-level record. … Superseding a stored tile's bytes
re-places that layer's index region…, moving its extent slot… and so modifying
that layer's record, which is such a change: **an appender superseding a tile
MAY drop a top-level such record, or such a sub-record of the layer whose tile
it superseded**."

(a) Top-level 0x9002: layer B's record content changes (its extent slot moves),
which is the "any layer record's content" trigger, and the rule names this case
outright. → **yes**.

(b) Layer A's 0x9001 sub-record: the trigger for a sub-record is scoped to
*that* layer — layer A. Layer A's record is unchanged, its index's entry set is
unchanged, and which of its tiles are stored is unchanged. The rule's explicit
permission is for "such a sub-record of the layer whose tile it superseded",
which is B, not A. → **no**.

Confidence: high.

---

## Q15 — planar slab runs and a packing gap

G = ⌈10/2⌉ = 5, N = 5, C = 2, planar ⇒ 10 addressed tiles, ordinals [0, 10).

§16.2 `[R-SLB-02]`: "for a planar layer each channel block [c·N, (c+1)·N) —
runs never span channel blocks, and the final run of a block can cover fewer
than S ordinals. Run r of a block starts at ordinal block_start + r·S."

Block 0 = [0, 5), S = 3 ⇒ runs [0, 3) and [3, 5).
Block 1 = [5, 10) ⇒ runs [5, 8) and [8, 10).

(a) **[0,3), [3,5), [5,8), [8,10)**.

(b) Run [0, 3) holds ordinals 0 (stored, 8192 + 100), 1 (sentinel —
"transparent to run continuity"), 2 (stored, 8300). `[R-SLB-03]`: "each stored
tile's offset equals the previous stored tile's offset plus its length". Needed
8192 + 100 = 8292; actual 8300 ⇒ an 8-byte **gap**. Row **L41** — "Inside a
slab run, a stored tile's offset ≠ the previous stored tile's offset plus that
tile's length (gap, overlap, or out-of-ordinal placement…)".

L42 is *not* exercised: the run's first stored tile is at 8192 = 2·4096, a
multiple of A_slab. The other runs have no stored tile and "impose nothing".

Confidence: high.

---

## Underdetermined questions

None. Every question resolved to a single reading with a decisive sentence.
The two places I looked hardest for a second reading and did not find one:

- **Q05(b)**, where the per-instance clause of §21.9 forecloses the tile-size
  row that the declarations would otherwise derive; and
- **Q03**, where §18.2 pre-empts the R3/R4 choice by naming R3 in its own text.

The nearest thing to a soft spot is **Q13**'s premise ("a file of format major
version 1" whose version_major holds 5), which is a defect in the question
rather than in the document, and which does not move the answer.
