# Round 14 — Diagram auditor — working transcript

## Access disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,168 lines, read in full in four `Read` calls plus targeted `grep`/`python3`
passes against that same file). I read no ADR, no `PLAN.md`, no `AGENTS.md`, no
`conformance/` material, no `spec/registry.json`, no git history, and did no web
access. I did not list or read the round-14 output directory. I created and read
three scratch files of my own (`crc.py`, `chk.py`, `build.py`) plus a synthetic
`t.tarn` I generated; all computation was local arithmetic over data I typed in
from the specification.

---

## Step 0 — Enumerating the figures before judging any of them

My charter is every figure, layout box, offset table, worked example and
checklist. So the first thing is an inventory with line numbers, so coverage is
checkable.

### Worked examples / Example blocks (21)

| Line | What |
|---|---|
| 507 | §4.6 — `température` NFC/NFD byte counts |
| 571 | §5.1 — the smallest conforming file, region by region |
| 578 | §5.1 — ASCII box: a file after three commits |
| 1043 | §7.4 — **a complete layer record payload**, annotated hexdump |
| 1181 | §9.2 — ASCII box: what a crash sees |
| 1496 | §11.2 — grid arithmetic, extents (1024,2048)/(1000,2048) |
| 1550 | §11.4 — spatial and disk ordinals |
| 1613 | §12.1 — bfloat16 1.0 and quiet NaN |
| 1662 | §12.3 — a `temp` float32 channel entry, twelve bytes |
| 1732 | §13.3 — r/g/b fill tuples, interleaved and planar |
| 1853 | §14.2 — interleaved/planar byte offsets, three channel sets |
| 1887 | §14.3 — packed bool plane, `55 01` / `55 FD` |
| 1943 | §14.5 — padding content, extents (5,5)/tiles (4,4) |
| 2067 | §15.4 — entry_count 1,000,000, segments and fetch ranges |
| 2082 | §15.4 — planar C=4 N=32, entry byte ranges |
| 2179 | §16.2 — slab runs over the §11.2 grid |
| 2360 | §17.3 — byte-shuffle of three float32 values |
| 2969 | §20.3 — supersede one tile: what a commit appends |
| 2978 | §20.3 — ASCII boxes: **the three shapes a commit takes** (a)(b)(c) |
| 3122 | §20.5 — ASCII box: what compaction reclaims |
| (3847) | Appendix A closing prose — the two-request open of the 128-byte file |

### Layout / offset tables (6 fixed-layout, 1 packed)

| Line | Structure | Columns |
|---|---|---|
| 682 | §6.1 front signature block | Offset, Size, Value, Class |
| 725 | §6.2 trailer | Offset, Size, Type, Field, Class, Valid values |
| 889 | §7.2 record header | Offset, Size, Type, Field, Class |
| 991 | §7.4 layer-record inline payload (packed) | Field, Type, Constraint |
| 1979 | §15.1 tile-index entry | Offset, Size, Type, Field, Class, Valid values |
| 2417 | §18.2 user-metadata inline payload | Offset, Size, Type, Field, Class, Valid values |
| 1974 | §15.1 region diagram (blockquote, not a table) | — |

### Tables that restate rules stated in prose elsewhere

| Line | Table |
|---|---|
| 235 | §2.4 outcome classes |
| 962 | §7.3 record types of format major 1 |
| 1106 | §8.1 checksum coverage map |
| 1380 | §10.2 numeric identifier spaces |
| 1579 | §12.1 core sample types |
| 1811 | §14.2 decoded size / offset of value k |
| 2027 | §15.3 entry validity |
| 2566 | §18.4 standardized keys |
| 3048 | §20.4 stored flags → updater obligation |
| 3230/3274/3331/3378 | §21.2–§21.5 the register (36/49/26/10 rows) |
| 3396 | §21.6 conditions that are not violations |
| 3493 | §21.9 minimum guarantees |
| 3829 | Appendix A annotated byte map |
| 3865 | Appendix B constants |
| 3963 | Appendix E changelog |

### Checklists and appendix material

- Appendix A (3812) — annotated minimal file, hexdump + table + prose
- Appendix B (3860) — constants
- Appendix C (3895) — registry snapshot
- Appendix F (3971) — normative references
- Appendix G (3986) — reproducible-writer profile, numbered items 1–10
- Appendix H (4098) — conformance checklists, five classes

### Numbered lists

§9.2 commit protocol steps 1–6; §10.1 four vehicles 1–4; §19.1 open steps 1–4;
§19.4 tile-read steps 1–8; §20.3 appender steps 1–6; Appendix G items 1–10;
§18.2's four document restrictions.

---

## Step 1 — The checksum arithmetic, done rather than eyeballed

I implemented CRC-32C from §4.5's parameters alone (Castagnoli reflected,
init/final `0xFFFFFFFF`, reflected polynomial `0x82F63B78`) and checked it
against §4.5's own check vector before using it for anything.

```
crc32c("123456789") = 0xe3069283   §4.5 says 0xE3069283, stored 83 92 06 E3  ✓
crc32c("")          = 0x00000000   §4.5 says 0x00000000                       ✓
```

Then every checksum constant the document states:

```
Appendix A trailer, bytes [0,60) assembled from the table's field values:
  8A4E52415 40D0A1A | 0100 | 0000 | 00000000 | gen=1 | dir_off=16 |
  dir_len=4 | cfl=128 | file_id=0x0123456789ABCDEF | reserved=0
  → CRC-32C = 0xe00938d2, stored little-endian D2 38 09 E0
  Appendix A row [124,128) says `D2 38 09 E0` = 0xE00938D2               ✓

§7.4 example, 4 sentinel entries (80 bytes of FF×16 00×4):
  → 0x80a34955, stored 55 49 A3 80    §7.4 says exactly that            ✓
  crc32c(55 49 A3 80) = 0xc4ee982e    §7.4 says 0xC4EE982E, stored
                                       `2E 98 EE C4` at payload byte 77  ✓

§15.4 / Appendix B, 2^16 sentinel entries:
  → 0xeecb3bb2                        §15.4 says 0xEECB3BB2              ✓
```

All three stated constants reproduce. This matters more than it looks: it means
the sentinel byte pattern, the entry width, the segment size and the CRC
parameters are all mutually consistent, because getting any one of them wrong
would have moved the constant.

## Step 2 — Appendix A, byte by byte

I read the hexdump off the page and checked every row of the annotation table
against it independently of the table.

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 ...
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  01 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
0060  04 00 00 00 00 00 00 00  80 00 00 00 00 00 00 00
0070  EF CD AB 89 67 45 23 01  00 00 00 00 D2 38 09 E0
```

- [0,8) front magic — matches §6.1's constant byte for byte ✓
- [8,16) zero — §6.1's second row ✓
- [16,20) `00 00 00 00` — directory region: zero record bytes plus CRC-32C of
  zero bytes, which §4.5 fixes at `0x00000000` ✓. dir_length = 4, the §6.2
  floor ✓
- [20,64) zero, **44 bytes** — 64 − 20 = 44 ✓, and 64 is where the trailer must
  begin because F = 128 and F − 64 = 64 ✓
- trailer field offsets: magic at 64 (= trailer 0), version_major at 72 (= 8),
  version_minor at 74 (= 10), flags at 76 (= 12), generation at 80 (= 16),
  dir_offset at 88 (= 24), dir_length at 96 (= 32), cfl at 104 (= 40), file_id
  at 112 (= 48), reserved at 120 (= 56), CRC at 124 (= 60). Every one matches
  §6.2's layout table ✓
- file_id `EF CD AB 89 67 45 23 01` little-endian = 0x0123456789ABCDEF ✓, ≠ 0 ✓
- trailer CRC computed above ✓

Then the closing prose. "112 bytes covering [16, 128) contains the directory":
128 − 16 = 112 ✓, and [16,20) ⊂ [16,128) so §6.4's containment test does apply,
while [0,16) stays non-resident so `[R-CNT-04]`'s deferral is available ✓. "That
is §19.1's four-step open" — §19.1 does have exactly four steps ✓.

Appendix A is correct in every value I can check.

## Step 3 — §6.2's trailer layout closes

Offsets 0,8,10,12,16,24,32,40,48,56,60 with sizes 8,2,2,4,8,8,8,8,8,4,4. Each
offset equals the previous offset plus the previous size, and 60 + 4 = 64 ✓ —
no gap, no overlap, no slack. §6.3's claim "The format-major-1 trailer has zero
slack: every byte is assigned" holds ✓. §6.3's "A future major MAY redefine only
the remaining 48 trailer bytes": 64 − 8 (magic) − 4 (the two version fields) − 4
(CRC) = 48 ✓.

§7.2's record header: 0(2),2(2),4(4),8(8),16(8) = 24 ✓. §15.1's entry:
0(8),8(8),16(4) = 20 ✓. §6.1: 0(8),8(8) = 16 ✓. §18.2: 0(1) = 1 ✓.

Every fixed-layout table's offsets close exactly on its stated structure size.

## Step 4 — §4.7's promise about which columns each table carries

§4.7's Note is the document's own statement of what a layout table delivers:

> Layout tables for fixed-layout structures give, per field: byte offset within
> the structure, size, type, name, taxonomy class, and valid range, each table
> giving the columns its structure needs. A packed variable-length payload — the
> layer record's inline payload (§7.4) — has no fixed offsets to give; its table
> omits the offset and class columns … §6.1's block is a 16-byte constant, where
> a Value column replaces type and range, and §7.2 folds each field's range into
> its Field cell.

Checked against all six tables: §6.2, §15.1 and §18.2 carry the full six columns;
§7.2 carries five and folds ranges into Field cells (`type (0 invalid)`,
`flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved`) ✓;
§6.1 carries Offset/Size/Value/Class ✓; §7.4 carries Field/Type/Constraint ✓.
Three carve-outs named, three carve-outs used, no fourth table left unexplained.

§4.7 also claims "`version_minor` is the only descriptive field". I checked every
Class cell in every table: §6.2's version_minor is the sole `descriptive` cell;
every other cell in §6.1, §6.2, §7.2, §15.1 and §18.2 reads `structural` ✓.

## Step 5 — Building the thing: the §7.4 layer record, assembled from the table

The §7.4 example is the newest large figure in the document, so I built it from
the *table* (line 991) rather than from the hexdump, and then compared.

Field order taken from the table: name; layout; linearization; codec; filter;
alignment A; slab S; slab alignment A_slab; rank d; channel count C; d dimension
entries; C channel entries; index_encoding; entry_count; crc_of_crc_array;
sub-records. Packed, no alignment (`[R-CNT-18]`).

My assembly produced:

```
03 73 73 74 01 01 00 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 01 01 00 01 78 64 00 00 00 00 00 00 00
20 00 00 00 00 00 00 00 04 74 65 6d 70 0c 00 04 00 00 c0 7f 01 04 00 00
00 00 00 00 00 2e 98 ee c4
inline_length = 81
```

Byte for byte identical to the document's annotated dump, including every offset
label (0, 4, 5, 7, 9, 11, 19, 27, 35, 36, 38, 40, 48, 56, 63, 68, 69, 77). The
arithmetic in the closing paragraph also checks: name 4; the nine scalars from
layout through channel count 1+2+2+2+8+8+8+1+2 = 34 (and that is nine scalars);
dimension entry 1+1+8+8 = 18; channel entry 1+4+2+1+4 = 12; trailing fixed fields
1+8+4 = 13; 4+34+18+12+13 = **81** ✓, so the sub-record sequence is empty with no
residue ✓.

Cross-check against §12.3's example at line 1662: it gives the same channel entry
as "the twelve bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F`". §7.4 splits the same
twelve bytes across payload offsets 56 and 63. Identical ✓ — the two figures
agree, which is exactly the sort of thing that goes stale.

Grid: ⌈100/32⌉ = 4 (3.125 → 4) ✓, interleaved so addressed-tile count = N = 4 =
entry_count ✓. Index extent length by `[R-CNT-17]`: 4×20 + ⌈4/65536⌉×4 = 84, and
§7.4 says 84 ✓. Region = 80-byte entry array + one segment CRC = 84 ✓, matching
§15.1's region diagram ✓. `[R-IDX-05]` requires a *partial* segment's CRC to be
computed rather than taken from the all-sentinel constant — this segment holds 4
entries, and the example does compute it ✓.

I then assembled a whole file around it to see whether anything forced me to
guess:

```
[0,16)     front block
[16,100)   tile-index region, 84 bytes
[100,209)  directory: 24-byte header + 81 inline + 4 CRC = 109 bytes
[209,256)  pre-trailer pad, 47 bytes (LIF-02 step 5: to the next 64 boundary)
[256,320)  trailer;  F = 320, 320 mod 64 = 0 ✓
dir_offset + dir_length = 209 ≤ F − 64 = 256 ✓
```

Record flags MU=1, PE=1 → bit0|bit1 = 0x0003 under §4.4's bit numbering ✓. No
guesswork was needed anywhere in this file.

## Step 6 — Every remaining worked example's arithmetic

I did each of these by hand rather than trusting the page.

- **§11.2.** (1024,2048)/(256,256) → G = (4,8) ✓, N = 32 ✓, P = 65,536 ✓.
  (1000,2048) → G_y = ⌈1000/256⌉ = ⌈3.906⌉ = 4 ✓.
- **§11.4.** s = Σ tᵢ·∏_{j>i} Gⱼ at d = 2 is t_y·8 + t_x. (0,0)→0, (0,1)→1,
  (1,0)→8 ✓. Coordinate (300,700): t = (1,2) → s = 10 ✓; u = (44,188) ✓;
  in-tile ordinal 44·256 + 188 = 11,452 ✓. Planar c = 2: 2·32 + 10 = 74 ✓.
- **§14.2.** a(uint8)/b(uint16): Q = 3, decoded size 6·3 = 18 ✓; ordinal
  1·3+2 = 5 ✓; offsets 5·3 + F_a=0 → 15, 5·3 + F_b=1 → 16 ✓. Planar b: 6·2 = 12
  bytes, value 5 at 5·2 = 10 ✓. t(float32)/m(bool): Q = 5, size 30 ✓, ordinal 5
  at 25, m at 25+4 = 29 ✓. The closing identity "k = u·C + c" gives k div C = u
  and k mod C = c ✓, so u·Q + Fᶜ ✓.
- **§14.3.** P = 10, values alternating true/false from ordinal 0: byte 0 bits
  0–7 = T,F,T,F,T,F,T,F → 0x55 ✓; byte 1 bits 0–1 = T,F → 0x01 ✓; pad bits are
  bits 2–7 (P mod 8 = 2) ✓; fill true sets bits 2–7 → 0xFD ✓. ⌈10/8⌉ = 2 ✓.
- **§14.5.** (5,5)/(4,4) → grid 2×2 ✓; edge tile (1,1) spans 4–7 on both axes,
  and only (4,4) is < 5 on both, so 1 real + 15 padding ✓; 16·2 = 32 bytes ✓;
  0xABCD little-endian = `CD AB` ✓.
- **§15.4 (a).** ⌈1,000,000/65,536⌉ = 16 ✓; 1,000,000 − 15·65,536 = 16,960 ✓;
  CRC array 64 bytes ✓; region 20,000,064 ✓; k = 999,999 is in segment 15 ✓ at
  segment-relative byte 20·(999,999 − 983,040) = 20·16,959 = 339,180 ✓; array at
  [20,000,000, 20,000,064) ✓; segment 15 at [19,660,800, 20,000,000) ✓; that
  segment is 16,960·20 = 339,200 bytes ≈ "~339 KB" ✓; a full segment is
  65,536·20 = 1,310,720 = 1.25 MiB ✓.
- **§15.4 (b).** disk ordinal 74 → region bytes [1,480, 1,500) ✓; channel 3's
  block is [96,128) = 32 entries ✓.
- **§16.2.** N = 32, S = 8 → runs [0,8),[8,16),[16,24),[24,32) ✓; rows 1–2 are
  ordinals 8–23 = runs 1 and 2 exactly ✓; sentinel at 10 leaves 8,9,11–15 packed ✓.
- **§17.3.** 1.0f/2.0f/3.0f → `00 00 80 3F | 00 00 00 40 | 00 00 40 40`, s = 4,
  n = 3. Placing byte i of group j at i·n + j gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` — byte for byte the document's
  result ✓, and the prose gloss matches ✓.
- **§20.3.** 32·20 + ⌈32/65536⌉·4 = 644 ✓; "editing one sample of a 10⁶-tile
  layer appends about 20 MB of index" = 10⁶·20 ✓.
- **§21.9 note.** ⌈2³²/2¹⁶⌉·4 = 2¹⁶·4 = 262,144 = 256 KiB ✓; at 2³⁶ it is
  2²⁰·4 = 4 MiB ✓; 65,536 × 200 bytes = 13,107,200 = exactly 12.5 MiB ✓, and
  16 MiB > 12.5 MiB so the two rows compose ✓.
- **§19.4 note.** entries at c·N+s are N·20 region bytes apart ✓, and for
  N ≥ 2¹⁶ consecutive ones differ by ≥ 2¹⁶ ordinals so their segment indices
  differ ✓ — "guaranteed to fall in different segments" is correct.
- **§4.6.** `température` NFC: t e m p é r a t u r e = 11 characters, é being
  `C3 A9`, so 12 bytes ✓ matching the listed bytes; NFD `65 CC 81` → 13 ✓.
- **§12.1.** binary32 1.0 = 0x3F800000, high 16 bits 0x3F80, stored `80 3F` ✓;
  0x7FC0 ↔ 0x7FC00000 quiet NaN ✓.

Not one arithmetic error in twenty-one examples. The numeric layer of this
document is in good shape.

## Step 7 — Counting the register mechanically

§21.1 fixes the counting rule: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written." So I parsed the four register tables and
counted.

```
F: rows=36  instances=56     §21.2 header says 36 conditions  ✓
L: rows=49  instances=111    §21.3 header says 49 conditions  ✓
T: rows=26  instances=57     §21.4 header says 26 conditions  ✓
R: rows=10  instances=44     §21.5 header says 10 conditions  ✓
   total rows 121, total instances 268
```

§21.8 says "121 conditions over 268 instances". Both numbers reproduce exactly
from the cells. That is a good sign about the bookkeeping — and it is what makes
the next check meaningful, because it means the 268 is a faithful sum of the
cells and any error must be in a cell.

## Step 8 — Auditing the cells against §21.1's stated instance criterion

§21.1 states two axes so that instance enumeration need not be judged case by
case:

> Two axes recur often enough to be stated rather than judged each time. Where
> the quantity a condition derives varies by layout, the layout formulas are
> materially different shapes and the cell enumerates them. Where the condition
> compares two quantities and either can be the greater — a *differs from* or
> *does not equal* — the two directions are likewise enumerated; where its own
> text bounds the comparison in one direction — an *exceeds*, a *larger than* —
> there is one.

The **layout axis** is applied consistently: T3, T14, T21, T22, T26 and L44 all
enumerate the three decoded-size formulas (interleaved P·Q, planar numeric P·Bᶜ,
packed planar bool ⌈P/8⌉), and T4 splits numeric fill by layout as well.

The **direction axis** is not. I grepped every register row for a two-way
comparison and sorted them:

Direction applied (all in §21.4):
- T3 "is not exactly" → 6 = 3 layouts × 2 directions
- T14 "differs from" → 6
- T22 "does not equal" → 6

Direction correctly *not* applied — one-directional text, or an unordered
comparison where "greater" is meaningless:
- T21 "larger than", L44 "exceeds", T24 "does not consume … exactly" (only one
  direction exists)
- F14, F20, L37, L38, T1, R2 — CRC equality, which has no direction

Direction *omitted* although the comparison is ordered and both directions are
constructible as distinguishable files:
- **F17**: "Trailer committed_file_length does not equal the
  transport-authoritative file size (physical file not truncated or extended to
  it)" — instance cell `committed_file_length`, 1 instance. The row's own
  parenthetical names both directions.
- **L21**: "entry_count does not equal the geometry-derived addressed-tile count
  (N interleaved, C·N planar)" — cell `interleaved N; planar C·N`, 2 instances.
  The layout axis is applied here and the direction axis is not, in the same cell.
- **L30**: "A channel entry's fill length prefix differs from the element size of
  the channel's declared type" — cell `—`, 1 instance. This row uses the exact
  trigger phrase §21.1 names.
- L22 is arguable: its "≠ the formula" instance is undirected, but its other two
  instances ("slot (0,0) with entry_count > 0", "a nonzero slot with
  entry_count = 0") happen to *be* the two directions at the boundary, so I do
  not count it.

I convinced myself the criterion really does reach these rows. It is stated as a
general axis, not scoped to layout-derived quantities — the layout sentence and
the direction sentence are separate, and only the first mentions layout. And each
of the three is constructible in both directions: fill prefix 3 or 5 against a
float32 element size; entry_count above or below N; a valid trailer whose
committed_file_length is 256 in a 320-byte file (extended) or 384 in a 320-byte
file (truncated).

Consequence: applying §21.1's own criterion yields 268 + 1 (L30) + 2 (L21) +
1 (F17) = **272** instances, while §21.8 and `[R-ERR-02]` state 268 and
`[R-VEC-03]` requires "one vector per instance". A corpus builder who applies
the criterion and a corpus builder who copies the cells build different corpora
and disagree about whether the corpus is complete. → **diagrams-02**.

This is the shape the brief warned about: an enumeration a repair extended in one
place (§21.4's decoded-size rows) and not its twins in §21.2 and §21.3.

## Step 9 — Reading §20.3's three-shapes figure as an implementer

This is a changed section and the figure is the kind that gets taken as a rule.

(a) and (b) check out against `[R-WRT-05]` and `[R-WRT-04]` step 4: a new layer
leaves A's record and extent slot byte-identical so it still addresses A's
original index ✓; adding tiles re-emits the whole index region at a new placement
because one extent slot addresses it ✓; the superseded region and payloads become
slack ✓. The §20.3 numeric example above it (644-byte index region) agrees ✓.

(c) is where I had to stop. The figure says:

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no padding
> position and no pad bit. Only the directory is re-emitted. **A fill change on a
> layer carrying either is not an appender's operation at all (step 4): it would
> invalidate every stored tile it reaches.**

Step 4, three paragraphs earlier, says the opposite about two whole classes of
layer:

> The test is the effect on a stored tile, and the list names where that effect
> arises rather than standing on its own: a change that reaches none of these for
> any tile the layer stores … leaves every stored tile conforming and is not what
> this bars.

and

> A layer that stores no tile MAY be re-declared freely, which is what
> schema-first creation needs (§11.1)

Two concrete files the figure forbids and the rule permits:

1. A layer with extents (5,5), tile extents (4,4) — so it *carries* padding
   positions, the figure's trigger — but with **no tile stored at all**. Step 4's
   last clause licenses re-declaring it freely; the figure says a fill change on
   it "is not an appender's operation at all".
2. The same geometry with **only the interior tile (0,0) stored**. Padding
   positions exist only in the edge tiles at (0,1), (1,0), (1,1); none of them is
   stored, so the fill change reaches no stored tile's padding. Step 4's test is
   "the effect on a stored tile", and here the effect is nil.

The figure's own justification undercuts it: "it would invalidate every stored
tile it *reaches*" — in both files it reaches none. I read "a layer carrying
either" as the geometric property, because the sentence it modifies says "a layer
with no padding position and no pad bit", which can only be geometry (a layer
does not stop having padding positions by not storing the tile that holds them).

→ **diagrams-01**.

## Step 10 — Appendix G, the reproducible-writer profile

Item 3's total emission order I traced end to end and could not break: front
block; per layer in ascending name-byte order, its stored tiles in disk-ordinal
order then its index region; then record extents in the type/masked-header/inline/
extent-content order, top-level before sub-records; then the directory; then the
64-aligned pad and trailer. The extent_offset masking is correctly justified
(a key containing it would depend on its own result) and the tie-breaking
argument is sound: two records the key does not separate differ only in
extent_offset, and swapping them yields identical file bytes because the records
are otherwise byte-identical and their extents are equal-length and equal-content.
No circularity: every offset the directory records is fixed before the directory
is emitted, and item 2's hash input is fixed before the trailer's CRC.

Item 2 is where I had to guess. The identifier is:

> the identifier its low eight digest bytes read little-endian

A digest is a byte string, not a number, and "low eight bytes" admits two
defensible readings — `digest[0:8]`, or `digest[len-8:]` if the digest is viewed
as a big-endian numeral, which is the ordinary way "low-order bytes" is used of a
hash. The trailing "read little-endian" pulls the other way (it does real work
only under the first reading, and is redundant-to-contradictory under the
second). Two producers naming the same hash function and version therefore emit
different `file_id` values, which is precisely the degree of freedom item 2
exists to close. I picked `digest[0:8]` because it is the reading under which
both halves of the phrase do work. → **diagrams-03**.

Item numbering 1–10 is consecutive with no duplicates. But the closing paragraph
that recapitulates what the items add enumerates ten things covering items
1,2,3,4,5,6,7,8,9 and never mentions item 10 (names normalized to NFC), which by
the paragraph's own criterion belongs there — `[R-ENC-14]` is a SHOULD, so NFC
normalization is exactly "what is not [already mandatory]". The paragraph guards
itself with "Read the numbered items as the list; this paragraph names what they
are for, not how many there are" — a guard about *count*, not about which items
exist. Low stakes and non-normative, but it is a list-completeness gap in a list
that reads as an enumeration. → **diagrams-04**.

## Step 11 — Appendices B, C, F and the checklists in H

**Appendix B** (26 rows): every constant traced to its defining section and
matched — front block, trailer magic, trailer size, 128-byte minimum, dir
minimums, extent_length ≥ 5, boolean byte encoding, media type, 24-byte header,
20-byte entry, 2¹⁶-entry segments with a 4-byte CRC each, the sentinel pattern,
0xEECB3BB2, the CRC parameters and check vector, the 2⁶³−1 value domain, 255-byte
names, rank ≤ 255 / C ≤ 65,535 (u8 and u16 widths ✓), S, A, A_slab, the 65,536
discovery window (§6.4's "dir_length plus the pre-trailer pad plus 64" ✓), the
1–16 MiB tile guidance, the zstd magic, 0x7E000000, `tarn.`, and the eight
minimum guarantees which match §21.9's eight-row table item for item ✓.

**Appendix C**: record types, thirteen sample types with the same names and
numbers as §12.1's table, the six pinned reservations 14–19 matching §12.2's
note, codecs 1–4, filters 1–2, layouts 1–2, linearization 1, index encoding 1,
metadata encodings 1–2, no assigned flags, six standardized keys matching
§18.4's six-row table ✓.

**§10.2's identifier-space table** against each defining section: record type
0x0003–0x7FFF reserved / ≥0x8000 experimental ✓; layout 3–255 reserved with no
experimental range ✓ (§14.1 agrees, and the "u8 too narrow" justification is
consistent); linearization 2–0x7FFF reserved (§11.4 splits it into 2–3 and
4–0x7FFF, whose union is the table's range ✓); sample type 14–0x7FFF ✓ (§12.2
splits 14–19 and 20–0x7FFF ✓); codec 5–0x7FFF ✓; filter 3–0x7FFF ✓; index
encoding 2–0x7F ✓; metadata encoding 3–0x7F ✓. Value 0 invalid everywhere ✓.

**§8.1's coverage map** against §4.5's prose: three terminal checksum fields
(trailer, directory region, user-metadata extent) ✓; three interior ones (segment
CRC array, entry crc, crc_of_crc_array) each comparison-verified and covered by
exactly one further checksum — entry crc by its segment CRC, the array by
crc_of_crc_array, crc_of_crc_array by the directory CRC ✓; front block by
equality ✓; unassigned-type extent by nothing ✓. §8.2's chain
trailer→directory→crc_of_crc_array→array→segment→entry→tile is the same order ✓.
No structure named in §5.2's coverage classes is missing a map row.

**Appendix H**, five checklists, each cross-checked against the class definition
in §2.3:

- *file*: matches §2.4/§5.2/§8.1/§21 ✓
- *reader*: "all four codecs, both filters, both layouts, all thirteen sample
  types, and both user-metadata encodings" — §17.2 makes 1–4 core ✓, §17.3 makes
  1–2 core ✓, §14.1 has two layouts ✓, §12.1 says "exactly thirteen … all core" ✓,
  §18.2 says both assigned encodings are core ✓. Five items, matching §2.3's
  five-item "no subset profiles" sentence ✓
- *writer*: fill recorded, padding and pad bits fill-encoded, interleaved bool
  only 0x00/0x01, sorted metadata members, both barriers, alignment/slab honored
  — each traced to its requirement ✓
- *updater*: matches §20.3/§20.4 including "never removes a layer record, or a
  user-metadata record at either scope", which follows from §7.3's table giving
  both registered types PE = 1 ✓
- *verifier*: the exempt-check list is complete against the register's
  verifier-detector rows — coverage/slack (F— , §9.7), overlap (F33/L18), flag
  bits (F25/F26/F28/L46/L47/L49), front block by equality (F1/F6), gap structures
  (F7), reserved-range types (F36/L25), alignment and slab (L40/L41/L42),
  decoded content (T2/T4/T5/T26), member ordering (F27/L48), plus the
  `[R-MTA-10]` reporting duty with its three named fields ✓

I found nothing in Appendix H that overstates or understates its cited authority.

## Step 12 — The ASCII region figures

§5.1's three-commit box: three commits, two ▓ runs (commits 1 and 2's
dir/pad/trailer), commit 3 touching no layer so re-emitting dir/pad/trailer alone
— internally consistent, and it carries its own narrowness guard ("The grouping
under the box is illustrative: a layer's structures need not be contiguous or
ordered (`[R-SLB-05]`), and §20.5's figure shows the general case"), which is
exactly the disclaimer this class of figure needs ✓.

§9.2's crash box: row 1's arrow lands after trailₙ at F ✓; row 2's ▓ is the
partial write with trailₙ no longer terminal, which is what `[R-LIF-05]` turns
into "torn" ✓; row 3's ▓ occupies exactly where dirₙ|pad|trailₙ stood ✓. Caption
distinguishes the two ▓ meanings ✓.

§20.5's compaction box: input carries five ▓ runs and the output none; file_id
X→Y and generation 7→1 ✓ matching `[R-WRT-06]`; the ′ marks on the regenerated
index regions ✓ matching `[R-WRT-07]`'s "entry offsets new; entry lengths, entry
crcs, and sentinel entries unchanged; segment CRCs recomputed". The output still
shows a `pad`, which is right — the compactor creates a pre-trailer pad of its
own, and "slack is never carried" refers to the input's ✓.

## Step 13 — Numbered lists, ordering and duplication

§9.2 steps 1–6 consecutive ✓, and every cross-reference to them lands correctly:
§20.2 "steps 4–6 — both barriers, not one" (steps 4 and 6 are the barriers ✓),
§20.3 step 4 cites "steps 1–2" for payloads ✓, step 5 cites "step 3" ✓, step 6
cites "steps 4–6" ✓, §6.2 and §2.3 cite "step 5" for the pad ✓.
§10.1's four vehicles match §4.3's four ✓. §19.1's four steps ✓ and Appendix A
calls it a four-step open ✓. §19.4's eight steps ✓ with step 3's "Steps 3 through
6 run once per needed entry" consistent with steps 3–6 being the per-entry ones ✓.
§20.3's six appender steps ✓. §18.2's four document restrictions map onto R5–R10
with none unregistered and none doubled ✓. Appendix G's items 1–10 ✓.

## Step 14 — Detection tiers in the register against §19

Spot-checked every Detected cell against §19.2's four tiers. L3/L5/L6 at *open*
is right because §19.1 step 4 parses and checks each layer record's name per §4.6
at open ✓. L4/L7/L8/L9 at *layer access* ✓ per §19.3. L37/L38 at *tile use* ✓
because they need I/O, while L21/L22 stay at *layer access* because §19.3 lists
"the index cross-checks computable without I/O" ✓. R2–R10 at *extent use* ✓.
R1 at open/layer access ✓ since the encoding byte is inline and resident.
F21–F23 at open, L10–L12 at layer access ✓ — the top-level/sub-record twins agree.
§19's preamble explicitly disclaims that its step lists are exhaustive, which
covers the rows §19 does not restate ✓.

I also checked §21.1's specialization list — F1 of F6 and of F8, F35 of F36,
L24 of L25 — and each holds as a strict containment with the narrower row's
detector and tier being the operative ones ✓.

---

## Findings

### diagrams-01 — CONTRADICTION — §20.3 example (c) forbids a commit `[R-WRT-04]` step 4 permits

**Location:** §20.3, example "the three shapes a commit takes", shape (c);
against `[R-WRT-04]` step 4 in the same section.

**Quotation (the figure):**

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no padding
> position and no pad bit. Only the directory is re-emitted. A fill change on a
> layer carrying either is not an appender's operation at all (step 4): it would
> invalidate every stored tile it reaches.

**Quotation (the rule it cites):**

> The test is the effect on a stored tile, and the list names where that effect
> arises rather than standing on its own: a change that reaches none of these for
> any tile the layer stores — a filter whose mandated stride makes it the
> identity (`[R-COD-10]`), or a new padding position whose stored byte already
> holds the fill `[R-SER-05]` fixes — leaves every stored tile conforming and is
> not what this bars.

and, in the same step:

> A layer that stores no tile MAY be re-declared freely, which is what
> schema-first creation needs (§11.1)

**Detail.** Step 4's bar is quantified over *stored tiles*: a declaration change
is barred only where it alters, for some tile the layer actually stores, the
padding-position set and its `[R-SER-05]` content, the decoded size, a sample's
byte offset, or the codec/filter. The figure re-states that bar quantified over
the *layer's geometry* instead — "a layer carrying either", i.e. a layer whose
extents and tile extents produce edge padding, or whose P is not a multiple of 8.
Those are not the same set. Two files show the gap:

1. Extents (5,5), tile extents (4,4), **no tile stored**. The layer carries
   padding positions, so the figure says a fill change on it "is not an
   appender's operation at all"; step 4's closing clause says it MAY be
   re-declared freely.
2. Same geometry, **only tile (0,0) stored**. Padding positions occur only in the
   edge tiles (0,1), (1,0), (1,1), none of them stored. The fill change reaches
   no stored tile, so by step 4's own test the layer's stored tile stays
   conforming.

The figure's justification refutes the figure: "it would invalidate every stored
tile it *reaches*" — in both files it reaches none. Two readings of "carrying
either" exist ("the geometry produces one" vs "a stored tile holds one"), but the
first is forced by the parallel clause one sentence earlier, "a layer with no
padding position and no pad bit", which can only be a geometric property.

An implementer who takes the figure as the rule builds an appender that refuses a
directory-only fill change on any layer with edge padding — including the
schema-first declare-then-fill workflow §11.1's Rationale and §13.3's
sparse-writing Note both build on, where the layer stores nothing yet.

**Byte-level: no.** The commit the figure over-forbids produces a file whose every
stored tile still satisfies `[R-SER-05]`, so no verifier verdict and no reader
outcome changes; §21.7 already places commit-history properties outside what a
single file witnesses. What forks is whether a given appender is willing to
perform the commit, not what bytes a conforming file may contain.

### diagrams-02 — CONTRADICTION — §21.1's direction axis is applied in §21.4 and not in its §21.2/§21.3 twins, so §21.8's 268 disagrees with §21.1's own criterion

**Location:** §21.1 (instance criterion) against §21.2 [F17], §21.3 [L21, L30],
and §21.8 / `[R-ERR-02]` / `[R-VEC-03]`.

**Quotation (the criterion):**

> Two axes recur often enough to be stated rather than judged each time. Where the
> quantity a condition derives varies by layout, the layout formulas are
> materially different shapes and the cell enumerates them. Where the condition
> compares two quantities and either can be the greater — a *differs from* or a
> *does not equal* — the two directions are likewise enumerated; where its own
> text bounds the comparison in one direction — an *exceeds*, a *larger than* —
> there is one.

**Quotation (three cells that do not obey it):**

> | L30 | A channel entry's fill length prefix differs from the element size of
> the channel's declared type | — | reader | layer access | `[R-CNT-23]`
> (R-TYP-06) |

> | L21 | entry_count does not equal the geometry-derived addressed-tile count (N
> interleaved, C·N planar) | interleaved N; planar C·N | reader | layer access |
> `[R-CNT-17]` (R-CNT-20) |

> | F17 | Trailer committed_file_length does not equal the
> transport-authoritative file size (physical file not truncated or extended to
> it) | committed_file_length | reader | open | `[R-CNT-06]` (R-LIF-04,
> R-CNT-10) |

**Quotation (the count that depends on them):**

> Every row of §21.2 through §21.5 — 121 conditions over 268 instances — has at
> least one conformance vector (§24) whose expected outcome is that row's
> outcome, and one vector per instance.

**Detail.** I parsed all four register tables and counted instances by §21.1's
mechanical rule (semicolons; `—` counts one). The totals are F 56, L 111, T 57,
R 44 = **268**, matching §21.8 exactly — so the sum is faithful and any error must
be in a cell.

The layout axis is applied uniformly: T3, T14, T21, T22, T26 and L44 all
enumerate interleaved P·Q / planar numeric P·Bᶜ / packed planar bool ⌈P/8⌉. The
direction axis is applied only in §21.4 — T3 (6 = 3×2), T14 (6), T22 (6) — and
nowhere else, although three rows outside §21.4 are ordered two-way comparisons
whose both directions are constructible as distinguishable files:

- L30 uses the criterion's own trigger phrase, "differs from". A float32 channel
  with a fill length prefix of 3 and one with a prefix of 5 are two files.
- L21 applies the layout axis and omits the direction axis *in the same cell*:
  entry_count above and entry_count below the derived count are two files, in
  each of two layouts, so four rather than two.
- F17's own parenthetical names both directions ("not truncated **or extended**
  to it"). A valid trailer whose committed_file_length is 256 in a 320-byte file
  and one whose value is 384 in a 320-byte file are two files.

(I do not count L22: its "≠ the formula" instance is undirected, but its other
two instances happen to be the two directions at the boundary.)

Two readings of the criterion are possible: that the direction sentence is
independent of the layout sentence, or that it only refines rows the layout
sentence already split. I take the first, because the two are given as separate
"axes" and only the first mentions layout; the second reading would also leave
L30, which mentions no layout at all, with no axis to be judged under, which is
what the passage says it exists to prevent ("stated rather than judged each
time").

Under that reading the register's instance total is 272, not 268. `[R-ERR-02]`
and `[R-VEC-03]` both make the per-instance count a corpus obligation, so an
implementer who applies §21.1's criterion and one who copies the cells build
corpora of different sizes and disagree about whether coverage is complete —
with §21.8 stating the smaller number as fact.

**Byte-level: no.** No row's condition, outcome, detector or tier changes; only
how many vectors the corpus owes for three rows. Two implementations still emit
and accept exactly the same byte sequences. §24 already makes the corpus
derivative of this document rather than constitutive of it.

### diagrams-03 — AMBIGUITY — Appendix G item 2's `file_id` derivation does not fix which eight digest bytes are taken

**Location:** Appendix G (non-normative), item 2.

**Quotation:**

> the hash a named function at a named version, its input the bytes [0, F − 64)
> followed by the trailer's first 60 bytes with the `file_id` field zeroed, and
> the identifier its low eight digest bytes read little-endian, with any other
> fixed nonzero value substituted in the measure-zero case that they are all zero

**Detail.** Everything else in item 2 is pinned: the input byte range, the field
zeroing, the exclusion of the trailer CRC (necessary, since it depends on
`file_id`), the hash function and version, and the degenerate all-zero case. The
extraction step is not. "Its low eight digest bytes" admits two readings:

1. `digest[0:8]` — the eight lowest-indexed bytes, assembled into a u64 by the
   trailing "read little-endian".
2. `digest[len−8:]` — the low-order eight bytes of the digest regarded as a
   big-endian numeral, which is how "low-order bytes of a hash" is ordinarily
   used.

I picked (1), because it is the reading under which both halves of the phrase do
work: under (2), "low" has already fixed the byte order and "read little-endian"
is either redundant or contradicts it.

An implementer who picks (2) produces a different `file_id` from one who picks
(1) for the same input and the same named hash — and item 2 exists precisely to
remove that degree of freedom, since §9.3 leaves `file_id` to a SHOULD. Since
Appendix G's own preamble says profile conformance "can be refuted cheaply but
confirmed only by reproducing the file", the failure mode is that two profile
adopters cannot reproduce each other's files and cannot tell whether the
difference is a bug or a reading.

**Byte-level: no.** Any nonzero `file_id` is conforming (§6.2), so both readings
yield conforming files and no reader or verifier changes its verdict. The
divergence is confined to reproducibility between two adopters of a
non-normative profile.

### diagrams-04 — OBSERVATION — Appendix G's closing recap of what the items add omits item 10

**Location:** Appendix G, closing paragraph, against Appendix G item 10.

**Quotation (the recap):**

> The items above add what is not, and the list is not short: gap *content*, which
> `[R-CNT-03]` only advises; gap *extent*, which placement freedom (`[R-SLB-05]`)
> leaves open; record and sub-record order, which `[R-CNT-14]` leaves free; the
> fill a writer records when its caller chooses none (`[R-TYP-10]`, a SHOULD);
> the sentinel for every all-fill tile, which no rule requires; a single
> generation, which §9 nowhere constrains; the absence or fixing of a declared
> alignment and slab, which §16 leaves to the writer; `version_minor` at its
> floor, which `[R-CNT-26]` states as a SHOULD; a derived `file_id`, where §9.3
> states only advice; and the producer pinning of items 1 and 9.

**Quotation (the omitted item):**

> 10. **Names normalized to Unicode Normalization Form C**, which `[R-ENC-14]`
> states as a SHOULD.

**Detail.** The recap's ten entries map onto items 1, 2, 3, 4, 5, 6, 7, 8 and 9
(gap content and gap extent are both item 3's, as is record order; producer
pinning covers 1 and 9). Item 10 appears nowhere in it, although it satisfies the
paragraph's own membership test exactly — `[R-ENC-14]` is a SHOULD, so NFC
normalization is squarely "what is not [already mandatory]", and item 10's own
text says so.

The paragraph carries a guard — "Read the numbered items as the list; this
paragraph names what they are for, not how many there are" — which disclaims the
count but not the membership, and the sentence it guards reads as an enumeration
("the list is not short: A; B; …; and J"). Nothing normative rides on it: the
appendix is non-normative, item 10 states its own justification, and the guard
tells a reader to use the numbered items. I report it because it is a
list-completeness gap of the kind my charter asks me to check, and because the
recap is the passage a reader consults to see whether the profile has closed
everything §9/§16/§18 leaves open.

**Byte-level: no.** Item 10 itself is intact and states its own requirement; only
the recapitulation is short. Nothing about which bytes a writer emits changes.

---

## What I could not determine

Nothing in my charter was left undecidable by the document. Every figure's
arithmetic is checkable from the sections it cites and every one of them checked
out; the three findings above are the only places where a figure, cell or list
says something its governing text does not, and diagrams-03 is the only place I
had to pick a reading to proceed.

Two things I looked at hard and decided were **not** defects, recorded so the
next round need not redo them:

- §21.6's "The file contains zero layers → A conforming file with an empty
  directory" is narrower than `[R-CNT-14]` (a file with zero layers may still
  carry a top-level user-metadata record), but §21.1 already fixes that the rule
  governs where a §21.6 entry diverges, and the cell describes rather than
  prescribes.
- F31 scopes its front-block-overlap instance as "extent_offset in 1-15" while
  its layer twin L16 says "extent_offset < 16", so L16 overlaps L15 where F31
  does not overlap F30. Both are faithful to `[R-CNT-13]`, which lists "either
  half zero" and "extent_offset < 16" as independent disjuncts, and `[R-VEC-02]`
  already prescribes what a vector records when a condition cannot be isolated.
  A cosmetic twin asymmetry with no consequence.
