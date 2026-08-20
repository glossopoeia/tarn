# Cleanroom round 13 — Diagram auditor transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,128 lines), in five `Read` calls covering lines 1–4128 with no gaps. I ran
`wc -l` and three `grep` invocations against that same file, and four local
Python programs that read no files (a CRC-32C implementation, a
byte-shuffle/bit-packing simulator, and a table-parsing instance counter that
read the spec file — that counter is the one program that opened the spec, and
it opened only the spec).

I opened no ADR, no `PLAN.md`, no `AGENTS.md`, no `README.md`, no
`conformance/` anything, no `spec/registry.json`, no git history. I ran no
`git` command, no web search, no web fetch, and I did not list any directory.
I did not read the round-13 output directory.

Two pieces of context reached me without my opening a file: the harness's
environment block lists the five most recent commit subjects, and the task-list
system reminder lists four task titles. I used those only to guess *where* the
newly authored material probably sits (the §7.4 byte example, §18.2's
metadata-encoding rules, §21.1's instance criterion, §20.3's new prohibition) —
i.e. as a search heuristic. Every conclusion below is grounded in quoted spec
text, and I settled nothing by reference to those subjects. I state this because
"disclosed breach is usable, undisclosed poisons the round" — I do not think
this is a breach, but it is the closest thing to one in my run.

I hold general knowledge of DEFLATE, zstd, LZ4, CRC-32C and IEEE 754. I used it
to generate suspicions and to run arithmetic (e.g. computing CRC-32C myself
rather than trusting the document's constants). I did not use it to settle any
question about what *this* document says.

---

## Part 1 — Inventory

Charter says: find them all first, with line numbers, so coverage is checkable.
Here is every figure, byte-layout box, offset table, worked example, checklist,
and rule-restating table I found, with the line range it occupies.

### 1a. On-disk layout tables (byte-layout boxes)

| # | Location | Lines | Columns delivered |
|---|---|---|---|
| A1 | §6.1 front signature block | 676–679 | Offset, Size, Value, Class |
| A2 | §6.2 trailer | 719–731 | Offset, Size, Type, Field, Class, Valid values |
| A3 | §7.2 record header | 883–889 | Offset, Size, Type, Field, Class |
| A4 | §7.4 layer-record inline payload | 985–1002 | Field, Type, Constraint |
| A5 | §15.1 tile-index entry | 1972–1976 | Offset, Size, Type, Field, Class, Valid values |
| A6 | §18.2 user-metadata inline payload | 2409–2411 | Offset, Size, Type, Field, Class, Valid values |

### 1b. Rule-restating tables (cells that restate prose stated elsewhere)

| # | Location | Lines | Rows |
|---|---|---|---|
| B1 | §2.4 outcome classes | 232–238 | 5 |
| B2 | §7.3 record types of format major 1 | 956–959 | 2 |
| B3 | §8.1 checksum coverage map | 1100–1108 | 7 |
| B4 | §10.2 numeric identifier spaces | 1374–1383 | 8 |
| B5 | §12.1 sample types | 1572–1586 | 13 |
| B6 | §14.2 decoded size / offset of value k | 1804–1807 | 2 |
| B7 | §15.3 entry validity | 2020–2032 | 11 |
| B8 | §18.4 standardized keys | 2558–2565 | 6 |
| B9 | §20.4 preservation obligations by stored flags | 3032–3036 | 3 |
| B10 | §21.2 file-scope register | 3207–3244 | 36 |
| B11 | §21.3 layer-scope register | 3251–3301 | 49 |
| B12 | §21.4 tile-scope register | 3308–3335 | 26 |
| B13 | §21.5 ignored-record register | 3352–3363 | 10 |
| B14 | §21.6 conditions that are not violations | 3370–3385 | 14 |
| B15 | §21.9 minimum-guarantee limits | 3465–3474 | 8 |
| B16 | Appendix A annotation table | 3801–3817 | 13 |
| B17 | Appendix B constants | 3837–3865 | 26 |
| B18 | Appendix E changelog | 3934–3936 | 1 |

### 1c. ASCII / region figures

| # | Location | Lines |
|---|---|---|
| C1 | §5.1 file after three commits | 575–580 |
| C2 | §7.4 layer-record payload byte listing | 1048–1067 |
| C3 | §9.2 what a crash sees | 1179–1188 |
| C4 | §15.1 index-region schematic | 1967–1968 |
| C5 | §20.3 shape (a) — a new layer | 2967–2971 |
| C6 | §20.3 shape (b) — tiles added | 2983–2987 |
| C7 | §20.3 shape (c) — directory-only | 3003–3006 |
| C8 | §20.5 what compaction reclaims | 3109–3115 |
| C9 | Appendix A hex dump | 3790–3799 |

### 1d. Worked examples (numeric)

| # | Location | Lines | Checked |
|---|---|---|---|
| D1 | §4.5 CRC check vector | 433–437 | computed |
| D2 | §4.6 `température` NFC/NFD | 504–508 | by hand |
| D3 | §5.1 smallest conforming file | 565–570 | by hand |
| D4 | §7.4 complete layer-record payload | 1037–1076 | computed |
| D5 | §11.2 grid arithmetic | 1489–1493 | by hand |
| D6 | §11.4 ordinals | 1543–1549 | by hand |
| D7 | §12.1 bfloat16 | 1606–1609 | by hand |
| D8 | §12.3 channel entry bytes | 1655–1660 | by hand |
| D9 | §13.3 fill tuples | 1725–1730 | by hand |
| D10 | §14.2 interleaved/planar offsets | 1846–1856 | by hand |
| D11 | §14.3 packed bool plane | 1880–1885 | computed |
| D12 | §14.5 edge-tile padding | 1936–1941 | by hand |
| D13 | §15.4 million-entry index | 2060–2073 | by hand |
| D14 | §15.4 planar entry positions | 2075–2079 | by hand |
| D15 | §16.2 slab runs | 2171–2178 | by hand |
| D16 | §17.3 byte-shuffle | 2352–2355 | computed |
| D17 | §20.3 supersede cost | 2953–2960 | by hand |
| D18 | §21.9 note — where the numbers come from | 3486–3501 | by hand |
| D19 | Appendix A annotated minimal file | 3786–3830 | computed |

### 1e. Checklists and numbered lists

| # | Location | Lines | Items |
|---|---|---|---|
| E1 | §9.2 commit protocol | 1145–1157 | 6 |
| E2 | §10.1 the four extension vehicles | 1354–1358 | 4 |
| E3 | §18.2 four document restrictions | 2466–2495 | 4 |
| E4 | §19.1 open algorithm | 2620–2663 | 4 |
| E5 | §19.4 tile-read algorithm | 2746–2797 | 8 |
| E6 | §20.3 append procedure | 2870–2943 | 6 |
| E7 | §21.9 hard limits (`[R-ERR-05]`) | 3503–3524 | 9 clauses |
| E8 | §22.3 "four residues" | 3580–3603 | 4 |
| E9 | Appendix G reproducible-writer profile | 3969–4044 | 10 |
| E10 | Appendix H conformance checklists | 4062–4128 | 5 classes |

---

## Part 2 — The arithmetic, done rather than eyeballed

### 2.1 Every CRC constant in the document

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and computed:

| Constant | Where | Document | Computed |
|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5, App. B | `0xE3069283` | `0xe3069283` ✓ |
| CRC-32C(zero bytes) | §4.5, App. A/B | `0x00000000` | `0x0` ✓ |
| 80 bytes = 4 sentinel entries | §7.4 example | `0x80A34955`, stored `55 49 A3 80` | `0x80a34955`, `55 49 a3 80` ✓ |
| CRC-32C of that 4-byte array | §7.4 example | `0xC4EE982E` | `0xc4ee982e` ✓ |
| 2¹⁶ sentinel entries | §15.4, App. B | `0xEECB3BB2` | `0xeecb3bb2` ✓ |
| Appendix A trailer bytes [0,60) | App. A | `0xE00938D2`, stored `D2 38 09 E0` | `0xe00938d2`, `d2 38 09 e0` ✓ |

All six reproduce. This is a stronger result than it sounds: §7.4's example is
newly authored material and its two CRCs are over byte strings the example
itself constructs, so an error anywhere in the sentinel definition, the entry
width, the segment-CRC-array width, or the grid count would have shown up here.
It did not.

### 2.2 §7.4's layer-record payload, field by field

The example claims 81 bytes. I re-derived every offset from §7.4's table order
(name, layout, linearization, codec, filter, A, S, A_slab, d, C, d dimension
entries, C channel entries, index_encoding, entry_count, crc_of_crc_array,
sub-records) and against §7.4's own type column:

```
 0  03 73 73 74              name  u8=3 + "sst"                  4  → next 4
 4  01                       layout u8                           1  → 5
 5  01 00                    linearization u16                   2  → 7
 7  01 00                    codec u16                           2  → 9
 9  01 00                    filter u16                          2  → 11
11  00 ×8                    A u64                               8  → 19
19  00 ×8                    S u64                               8  → 27
27  00 ×8                    A_slab u64                          8  → 35
35  01                       d u8                                1  → 36
36  01 00                    C u16                               2  → 38
38  01 78                    dim name u8=1 + "x"                 2  → 40
40  64 …                     extent u64 = 100 (0x64)             8  → 48
48  20 …                     tile extent u64 = 32 (0x20)         8  → 56
56  04 74 65 6D 70 0C 00     chan name u8=4 + "temp" + type u16  7  → 63
63  04 00 00 C0 7F           fill u8=4 + 00 00 C0 7F             5  → 68
68  01                       index_encoding u8                   1  → 69
69  04 …                     entry_count u64 = 4                 8  → 77
77  2E 98 EE C4              crc_of_crc_array u32                4  → 81
```

Every listed offset matches. The prose recap — "Name and the nine scalars from
layout through channel count occupy 4 + 34 bytes, the dimension entry 18, the
channel entry 12, and the trailing fixed fields 13 — 81 exactly" — checks:
1+2+2+2+8+8+8+1+2 = 34 and those are exactly nine scalars; 2+8+8 = 18;
1+4+2+1+4 = 12; 1+8+4 = 13; 4+34+18+12+13 = 81. The channel entry is
byte-for-byte §12.3's twelve bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, split
across two listing lines but identical when concatenated — the example's claim
"§12.3's `temp` entry, byte for byte" holds.

Grid count ⌈100/32⌉ = 4, interleaved ⇒ addressed tiles = N = 4 ⇒ entry_count 4
(§11.2, §15). Extent length by `[R-CNT-17]`: 4×20 + ⌈4/2¹⁶⌉×4 = 84, which is
what the example states. The segment here covers 4 entries, i.e. a *partial*
segment, so `[R-IDX-05]`'s "a partial segment's CRC MUST be computed" applies
and the example correctly gives a computed value rather than `0xEECB3BB2`. I
looked specifically for the mistake of reusing the full-segment constant; it is
not there.

I also checked the example does not show a case the prose forbids: codec 1 with
zero stored tiles never engages `[R-COD-04]`'s length equality; a nonzero extent
slot with entry_count = 4 is required (L22 registers the converse); every entry
being the sentinel is `[R-IDX-02]`'s defined case, not `[R-TYP-09]`'s forbidden
one.

### 2.3 Appendix A, byte by byte

I decoded the hex dump independently of its annotation table.

```
0000  89 54 41 52 4E 0D 0A 1A   = §6.1 magic                       ✓
0008  00 ×8                     = §6.1 reserved zero                ✓
0010  00 00 00 00               = directory region, dir_length 4    ✓ CRC-32C(∅)=0
0014..003F  00 ×44              = pre-trailer pad, 44 bytes         ✓ 64−20
0040  8A 4E 52 41 54 0D 0A 1A   = trailer magic (offset 0)          ✓
0048  01 00                     = version_major 1 (offset 8)        ✓
004A  00 00                     = version_minor 0 (offset 10)       ✓
004C  00 00 00 00               = flags (offset 12)                 ✓
0050  01 ×1 00 ×7               = generation 1 (offset 16)          ✓
0058  10 00 …                   = dir_offset 16 (offset 24)         ✓
0060  04 00 …                   = dir_length 4 (offset 32)          ✓
0068  80 00 …                   = committed_file_length 128 (40)    ✓
0070  EF CD AB 89 67 45 23 01   = file_id 0x0123456789ABCDEF (48)   ✓
0078  00 00 00 00               = reserved (offset 56)              ✓
007C  D2 38 09 E0               = CRC (offset 60)                   computed ✓
```

Every field lands at the offset §6.2's table assigns, the 64 bytes sum to the
trailer exactly (8+2+2+4+8+8+8+8+8+4+4 = 64, no slack, matching `[R-CNT-24]`'s
"The format-major-1 trailer has zero slack"), and the gates of `[R-CNT-06]` all
pass: dir_offset 16 ≥ 16; dir_length 4 ≥ 4; 16+4 = 20 ≤ 128−64 = 64;
1 ≤ generation ≤ 2⁶³−1; file_id ≠ 0; reserved zero; F mod 64 = 0. The 128-byte
figure is genuinely minimal — F = 64 is impossible because the front block
occupies [0,16) and dir_offset+dir_length ≤ F−64 = 0 cannot be satisfied.

`[R-CNT-24]`'s permanent-positions claim also checks against this file:
magic at F−64 = 64, version pair at F−56 = 72, CRC at F−4 = 124 covering
[F−64, F−4) = [64,124) = trailer bytes [0,60). And "A future major MAY redefine
only the remaining 48 trailer bytes": 64 − 8 − 4 − 4 = 48 ✓.

Appendix A's closing narrative on the open path: "112 bytes covering [16, 128)
contains the directory, so §6.4's containment test applies, while bytes [0, 16)
stay non-resident" — 128−112 = 16 ✓, [16,20) ⊂ [16,128) ✓, and `[R-CNT-04]`'s
"A reader that would have to issue a further range request to obtain those bytes
MAY defer or omit the check" is correctly applied.

I flagged one soft spot here and then talked myself out of it: the sentence "A
local reader additionally verifies bytes [0, 16) by equality first, which
`[R-CNT-04]` requires of any reader holding them" leads with the transport
category (§6.1's "local reader") for a rule §6.1 explicitly says turns on
residency — "The test is residency, not transport". A local reader that does a
64-byte pread of the trailer does not hold [0,16). But the same sentence's own
relative clause states the actual rule, and the next two sentences work the
residency test correctly for a remote reader. Non-normative appendix, corrected
in place. Not reported.

### 2.4 Every other numeric example

- §11.2: extents (1024,2048), tiles (256,256) ⇒ G=(4,8), N=32, P=65,536 ✓.
  Extents (1000,2048) ⇒ G_y = ⌈1000/256⌉ = 4 ✓.
- §11.4: coordinate (300,700) ⇒ tile (1,2), s = 1·8+2 = 10 ✓; in-tile (44,188),
  ordinal 44·256+188 = 11,452 ✓; planar C=4 channel 2 ⇒ 2·32+10 = 74 ✓.
- §12.1: bfloat16 1.0 = high 16 bits of binary32 0x3F800000 = 0x3F80, stored
  `80 3F` ✓; 0x7FC0 ↔ 0x7FC00000 quiet NaN ✓.
- §12.3: `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — name len 4 + "temp", type
  0x000C = 12 = float32, fill len 4 = float32 element size (`[R-CNT-23]`), fill
  `00 00 C0 7F` = 0x7FC00000 ✓ 12 bytes.
- §13.3: uint8 r/g/b fills FF/00/00 ⇒ unstored tile reads (255,0,0) ✓; planar
  mixed case reads b = 0 ✓.
- §14.2: (2,3) tile, a=uint8, b=uint16 ⇒ Q=3, decoded 18; ordinal of (1,2) is
  1·3+2 = 5; bytes [15,18) ✓. Planar b: 12 bytes, ordinal 5 at [10,12) ✓.
  t=float32 + m=bool ⇒ Q=5, decoded 30, ordinal 5 at [25,30), t at 25–28, m at
  29 ✓. Generalization "u·Q + Fᶜ, the table's forms with k = u·C + c" is exactly
  the table row (k div C = u, k mod C = c) ✓.
- §14.3: P=10 alternating true/false ⇒ byte 0 = 0x55, byte 1 = 0x01 with six pad
  bits; fill false ⇒ `55 01`, fill true ⇒ `55 FD`. I simulated this; both match.
- §14.5: extents (5,5) tiles (4,4) ⇒ grid 2×2, corner tile covers 4–7 on both
  axes, 1 real + 15 padding, P=16, uint16 ⇒ 32 bytes, values 1–15 = `CD AB`
  (little-endian 0xABCD) ✓.
- §15.4 #1: entry_count 10⁶ ⇒ 16 segments (15 full = 983,040, last 16,960),
  64-byte CRC array, region 20,000,064 ✓. Tile 999,999 is segment-relative
  16,959 ⇒ byte 339,180 ✓; CRC array at [20,000,000, 20,000,064) ✓; segment 15
  at [19,660,800, 20,000,000) ✓; full segment 65,536×20 = 1,310,720 = 1.25 MiB ✓.
- §15.4 #2: planar C=4 N=32 ⇒ entry 74 at [1480,1500) ✓; channel 3 = ordinals
  96–127, 32 sentinels ✓.
- §16.2: N=32, S=8 ⇒ runs [0,8) [8,16) [16,24) [24,32) ✓; row-major with
  G=(4,8) makes each run one tile-row ✓; tile rows 1–2 = ordinals 8–23 = runs 1
  and 2 ✓; sentinel at ordinal 10 leaves 8,9,11…15 packed ✓.
- §17.3: 1.0/2.0/3.0 float32 ⇒ `00 00 80 3F 00 00 00 40 00 00 40 40`; s=4, n=3;
  shuffled `00 00 00 00 00 00 80 00 40 3F 40 40`. I ran the transform and its
  inverse; both match the document exactly.
- §20.3: 32-tile layer index = 32·20 + 4 = 644 ✓. Note's "10⁶-tile layer …
  about 20 MB of index" = 20,000,064 ✓.
- §21.9 note: entry_count 2³² ⇒ 2¹⁶ segments ⇒ 2¹⁶·4 = 256 KiB ✓; 2³⁶ ⇒ 2²⁰·4 =
  4 MiB ✓; 65,536 layers × 200 B = 13,107,200 = 12.5 MiB ✓.

Nothing in this set is off by a byte.

### 2.5 The register's own arithmetic

§21.8 asserts "121 conditions over 264 instances", and §21.1 makes the count
mechanical: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance". I wrote a parser that pulls every six-column row
whose first cell matches `^[FLTR]\d+$` and counts semicolon-separated instance
cells (with `—` counted as 1):

```
F: 36 rows, 56 instances
L: 49 rows, 110 instances
T: 26 rows, 54 instances
R: 10 rows, 44 instances
total 121 rows, 264 instances
```

That is exactly what §21.8 claims, and the per-subsection headers (36 / 49 / 26
/ 10) match their row counts. The mechanical claim in §21.1 is true.

### 2.6 §10.2 identifier spaces against the sections that own them

| Space | §10.2 says | Owning section says | ✓ |
|---|---|---|---|
| record type | 1,2 / 3–0x7FFF / ≥0x8000 | §7.3 "All other type values are unassigned" | ✓ |
| channel layout | 1,2 / 3–255 / none | §14.1 "values 3 through 255 are reserved" | ✓ |
| linearization | 1 / 2–0x7FFF / ≥0x8000 | §11.4 "2 and 3 … 4 through 0x7FFF" | ✓ |
| sample type | 1–13 / 14–0x7FFF / ≥0x8000 | §12.2 "14 through 19 … 20 through 0x7FFF" | ✓ |
| codec | 1–4 / 5–0x7FFF / ≥0x8000 | §17.2 | ✓ |
| filter | 1,2 / 3–0x7FFF / ≥0x8000 | §17.3 | ✓ |
| index encoding | 1 / 2–0x7F / ≥0x80 | §7.4, §15.1 | ✓ |
| metadata encoding | 1,2 / 3–0x7F / ≥0x80 | §18.2 | ✓ |

Appendix C's snapshot agrees with all eight and with §12.1's thirteen types and
§18.4's six keys. Appendix B's "Reader minimum guarantees" row lists the same
eight quantities and values as §21.9's table.

### 2.7 §8.1's coverage map against §4.5's claim

`[R-CNT-19]` says every field of every structure is covered by exactly one
checksum, with three carve-outs. I traced each field class to a checksum:

- front block → equality, no checksum (carve-out 1)
- trailer bytes [0,60) → trailer CRC; trailer CRC field itself → terminal (carve-out 2)
- directory record sequence (all record headers, all inline payloads, including
  every layer record's `crc_of_crc_array`) → directory CRC; directory CRC field
  → terminal
- index entries → their segment CRC; segment CRC array → `crc_of_crc_array`
- stored tile bytes → its entry's `crc`
- user-metadata extent bytes → the extent's terminal 4 bytes; those → terminal
- unassigned-type record extent → none, stated (carve-out 3)

No field is left uncovered and none is doubly covered. §4.5's "Interior checksum
fields — each segment CRC array, each tile-index entry's crc field, and each
layer record's crc_of_crc_array — are both comparison-verified and covered by
exactly one further checksum" is exactly what the map delivers.

### 2.8 §15.3's entry-validity table against its own prose

`[R-IDX-03]` says "Six rows are marked *structural*". I counted the table:
rows 2–7 carry *structural* — six. Rows 9–11 carry *verifier* — three, matching
"rows marked *verifier* require whole-index or whole-file knowledge". Row 8
("stored bytes fail the entry's crc") is deliberately not structural, which the
prose spells out and which §16.2's `[R-SLB-03]` and §9.7's `[R-LIF-08]` both
rely on ("An entry whose only defect is that its stored bytes fail its crc is
not transparent"). All three passages agree. This is a place where a
propagation miss would have been easy and there is none.

### 2.9 F33's bounds cross-reference

F33 says a claimant reaching the front block or the trailer "is instead caught
by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier". I
enumerated the claimant classes §9.7 walks (directory, top-level record extents,
layer/sub-record extents including the tile-index region, stored-tile extents)
and each has exactly one low-bound row and one high-bound row in that list.
Complete.

### 2.10 Appendix H's verifier checklist against the register's verifier rows

Verifier-detected rows are F7, F25, F26, F27, F28, F33, F36, L18, L25, L40,
L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. Mapping them onto the checklist:
coverage/slack (§9.7), extent overlap (F33, L18), record flag bits (F25, F26,
L46, L47), registered-type stored bits (F28, L49), pre-trailer gap (F7),
reserved-range types (F36, L25), alignment and slab (L40–L42), decoded content
(T2, T4, T5, and T26 which detects through T2's or T4's check), member ordering
(F27, L48). Every verifier row is reachable from the checklist. No gap.

---

## Part 3 — Findings

Six. None is byte-level; I say why for each, and I looked hard for a fork
before concluding that.

---

### diagrams-01 — AMBIGUITY

**§21.1 (instance criterion) against §21.4 rows T14 and T22, and §21.3 row L21**

§21.1 tells a corpus builder how to read an Instances cell:

> What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25).

and

> An instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any combination
> of the three

Now put two rows side by side. Both are "a declared length ≠ the tile's decoded
size, checkable before decode":

> | T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs
> from the tile's decoded size | interleaved P·Q, length longer; interleaved
> P·Q, length shorter; planar numeric P·Bᶜ, length longer; planar numeric P·Bᶜ,
> length shorter; packed planar bool ⌈P/8⌉, length longer; packed planar bool
> ⌈P/8⌉, length shorter | reader | tile use | `[R-COD-04]` |

> | T22 | Codec 3 (zstd) and the frame's Frame_Content_Size field is present but
> does not equal the tile's decoded size | interleaved P·Q; planar numeric
> P·Bᶜ; packed planar bool ⌈P/8⌉ | reader | tile use | `[R-COD-06]` |

T14 splits its `≠` into longer/shorter and gets 6; T22 does not and gets 3. The
predicate is the same shape, the check is the same single comparison, and both
directions give distinguishable files in both rows. Nothing in §21.1
distinguishes them.

The same criterion is applied a third way one subsection up:

> | L21 | entry_count does not equal the geometry-derived addressed-tile count
> (N interleaved, C·N planar) | — | reader | layer access | `[R-CNT-17]`
> (R-CNT-20) |

L21 splits neither the direction *nor* the interleaved/planar shapes — although
its own condition text names those two alternatives, which §21.1 says is
precisely what an instance is ("one of several alternatives the condition text
states"), and although L22, L44, T3, T14, T21 and T22 all do enumerate layout
shapes. L22's first instance ("extent_length against the formula") and L30 ("A
channel entry's fill length prefix differs from the element size of the
channel's declared type") are further unsplit `≠`s.

**Permitted readings.** (a) A `≠` predicate contributes two instances (longer,
shorter) wherever the compared quantity is a length — T14 and T3's reading;
under it T22 owes 6, L21 owes 4, L22's first cell owes 2, L30 owes 2, and the
corpus is larger than 264. (b) A `≠` predicate is one instance because the check
does not change shape with the direction — T22, L21, L22 and L30's reading;
under it T14 and T3 owe 3 each and the corpus is smaller than 264. (c) The
splitting is per-row editorial judgment and 264 is simply what the cells say —
which is what §21.1's "the count is therefore mechanical once the cell is
written" actually licenses, but which makes the criterion decorative rather than
decidable.

**What I picked.** (c), because §21.1's own wording concedes that the *cell* is
written by judgment and only the *count* is mechanical, and because §21.8's 264
is stated as fact rather than derived. But a corpus builder asked to justify why
T22 has three vectors and T14 six cannot do it from this text, and the two
neighbouring rows in the same subsection are the worst possible place for the
criterion to be applied two ways.

**What an implementer does wrong without it.** Builds 264 vectors and cannot say
whether the corpus is complete under `[R-ERR-02]`'s "one vector per instance",
because "instance" is not pinned. Or, reading the criterion as decidable, builds
a different number and reports the register as defective.

**Byte-level: no.** This governs how many test files exist, not what any file
means. No conforming implementation's accept/reject behavior turns on it — every
one of these conditions is already unambiguously a violation with a stated
outcome, whichever way the vectors are counted.

---

### diagrams-02 — CONTRADICTION

**§20.3 step 4 (inside `[R-WRT-04]`, normative) against `[R-GEO-06]`; restated
in §11.1's Rationale**

§20.3, step 4 of the append procedure:

> and every other entry byte-identical at its disk-ordinal position (a geometry
> change renumbers ordinals, `[R-GEO-06]`)

§11.1's Rationale says the same thing:

> growth that raises one changes entry_count and with it extent_length
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and disk
> ordinals renumber (§20.3, `[R-WRT-04]`, `[R-GEO-06]`) — the first growth of a
> zero-extent layer included.

The rule both cite says:

> Under linearization 1, the **spatial tile ordinal** of (t₀, …, t_{d−1}) is
> s = Σᵢ tᵢ · ∏_{j>i} Gⱼ.
> The **disk tile ordinal**, which orders tile-index entries (§15), is s for an
> interleaved layer, and **c · N + s** for a planar layer

s depends on G₁ … G_{d−1} and *not* on G₀ — the empty product for i = 0 is over
j > 0. So for an interleaved layer, a geometry change that raises only the
first-declared dimension's grid count leaves every existing tile's disk ordinal
unchanged.

Worked counter-example. Interleaved, d = 2, extents (100, 100), tile extents
(32, 32) ⇒ G = (4, 4), N = 16, s = 4·t₀ + t₁. Grow E₀ to 200 ⇒ G = (7, 4),
N = 28, s = 4·t₀ + t₁ — identical. Entries 0–15 keep their positions; entries
16–27 are new. Nothing renumbered. At d = 1 it is even starker: s = t₀ always,
so no growth of a rank-1 layer ever renumbers anything — and §7.4's own worked
example is a rank-1 layer whose §11.1 rationale would, read literally, promise
renumbering on its first growth.

The claim is true for planar layers whenever N changes (channel blocks shift, so
c·N + s moves for c ≥ 1) and true for interleaved layers when a non-first
dimension's grid count changes. It is false in the canonical append case —
growing the outermost, slowest-varying axis, which is exactly the growth pattern
§11.1's "declare layers at creation, grow extents as data arrives" describes.

**Byte-level: no.** `[R-GEO-06]` is the only ordinal formula in the document,
and §20.3's parenthetical cites it rather than offering an alternative, so a
writer computing entry positions has exactly one procedure available and two
writers produce identical index regions either way. The damage is to a reader's
model, and to any writer that tries to short-circuit the formula on the strength
of the parenthetical.

---

### diagrams-03 — AMBIGUITY

**§21.5's preamble against row R1 and §21.6's table row**

§21.5's preamble:

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation
> in the rows below, except at an unassigned encoding, where no document rule
> attaches and §21.6 records the defined non-violation (`[R-MTA-10]`).

But the first row underneath it registers a violation at unassigned encodings:

> | R1 | A user-metadata record declares a document encoding of 0, or a
> reserved-range value (3-0x7F) | … | reader | open (top-level); layer access
> (sub-record) | `[R-CNT-25]` (R-MTA-03, R-EXT-03) |

and §21.6's row covers only the experimental part of the unassigned space:

> | A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming …

The reserved range 3–0x7F is unassigned (§10.2, §18.2: "3 through 0x7F are
reserved"), so the preamble's exception, read on its own terms, sweeps R1's
reserved-value instances into the non-violation column that §21.6 declares — and
§21.6 does not contain them.

**Permitted readings.** (a) "Unassigned" means what §10.2 means by it —
everything outside {1, 2} — so a reserved-range metadata encoding is not a
violation, contradicting R1 and §10.3's "a value from a reserved range MUST NOT
be emitted at all". (b) The exception is scoped to the *document content* rules
only: under any unassigned encoding no content rule attaches (which is
`[R-MTA-10]`'s actual claim), while the encoding byte's own value is a separate,
still-registered check.

**What I picked.** (b), because `[R-MTA-10]` spells it out — "file conformance …
is decided by the structural checks that precede the document alone: the
record's framing and extent slot (`[R-CNT-13]`), the encoding byte's own value
set (`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)" — and because
§21.6's row names the experimental range explicitly rather than the unassigned
space. The word the preamble wants is "experimental", not "unassigned".

**What an implementer does wrong without it.** A verifier that takes reading (a)
certifies a file carrying metadata encoding 5. A verifier taking (b) reports it
nonconforming under R1. That is a verdict split on identical bytes — which is
why I looked at this one hardest.

**Byte-level: no.** It is decided three ways over: R1's row text names
"reserved-range value (3-0x7F)" as a registered violation, §21.6's row is
restricted to "≥ 0x80", and §10.3 makes reserved-range emission a violation
outright. §21.1's "where a row and the rule it cites diverge, the rule governs"
does not even need to be invoked; the row and the rule agree, and only the
preamble's one word is loose. Two competent implementations reading the whole
of §18.2, §10.3 and §21.5–§21.6 cannot end up on opposite sides.

---

### diagrams-04 — AMBIGUITY

**Appendix G item 3 — the total emission order is not well founded**

> Records and a layer record's sub-records alike are ordered by type, and within
> a type by their encoded bytes compared lexicographically, save that type
> 0x0001 ties by layer name — an order a reader can derive, which a creation
> order is not.

and, immediately before it:

> then any record extents in ascending record order — all of them after every
> layer's tiles and index region, not interleaved with them

A record's "encoded bytes" are its 24-byte header followed by its inline payload
(§7.2). The header's bytes 8–15 are `extent_offset`. So the ordering key begins
with a field whose value is fixed by *where the record's extent was placed*, and
the placement of record extents is fixed by "ascending record order". The order
determines the offsets and the offsets determine the order.

For two records of the same type this is a genuine fixed-point problem rather
than a mere circular definition: place A before B and A gets the smaller
`extent_offset`, so A sorts first, which is consistent; place B first and that
is consistent too. Both emissions satisfy the stated rule, so the profile fails
to pin the bytes in exactly the case it exists to pin.

The document already noticed this once. "save that type 0x0001 ties by layer
name" replaces the encoded-bytes key with a placement-independent key for layer
records — the only reason to do that is that the encoded-bytes key does not work
for them. Type 0x0002 is protected by multiplicity (`[R-CNT-14]`: at most one
top-level, at most one per layer record), so it can never have two members to
order. That leaves unassigned types, for which `[R-CNT-14]` imposes no
multiplicity limit at all, with the broken key and no tie-break — and
unassigned-type records with extents are precisely what a compactor carries
forward, the actor item 2 explicitly contemplates adopting the profile.

**Permitted readings.** (a) "Encoded bytes" = header + inline payload, as §7.2
defines a record. Circular for two same-type unassigned records; two profile
implementations emit different byte sequences from the same input. (b) "Encoded
bytes" = the inline payload only. Well founded, but then the 0x0001 tie-break
clause is pointless (layer names are unique per `[R-ENC-15]`, so layer records'
payloads always differ), and two same-type records with identical payloads and
different extents still tie with nothing to break it.

**What I picked.** (a), because §7.2 defines a record as header plus payload and
nothing here narrows it, and because the 0x0001 clause only earns its place
under (a).

**What an implementer does wrong without it.** Two writers claiming profile
conformance produce different files for the same content whenever the input
carries two records of one unassigned type at the same level. Since "conformance
to the profile can be refuted cheaply but confirmed only by reproducing the
file", the failure surfaces as an unreproducible build with no diagnosis.

**Byte-level: no.** Appendix G is explicitly non-normative and "adds no
requirement to any actor: a writer ignoring it is fully conforming". Both
emission orders yield conforming TARN files, so no conforming implementation's
accept/reject behavior differs. It forks the *profile*, not the format.

---

### diagrams-05 — OBSERVATION

**§4.7's Note describes a column set three of the six layout tables do not have**

> **Note.** Layout tables for fixed-layout structures give, per field: byte
> offset within the structure, size, type, name, taxonomy class, and valid
> range. A packed variable-length payload — the layer record's inline payload
> (§7.4) — has no fixed offsets to give; its table omits the offset and class
> columns, and each field's class follows from the definitions above.

One carve-out is stated, for §7.4. Against the six actual layout tables:

| Table | Delivered | Against the claim |
|---|---|---|
| §6.2 trailer | Offset, Size, Type, Field, Class, Valid values | all six ✓ |
| §15.1 index entry | Offset, Size, Type, Field, Class, Valid values | all six ✓ |
| §18.2 metadata payload | Offset, Size, Type, Field, Class, Valid values | all six ✓ |
| §6.1 front block | `\| Offset \| Size \| Value \| Class \|` | four: no type, no name; "Value" in place of valid range |
| §7.2 record header | `\| Offset \| Size \| Type \| Field \| Class \|` | five: no valid-range column (ranges folded into the Field cells, e.g. "type (0 invalid)") |
| §7.4 inline payload | `\| Field \| Type \| Constraint \|` | three; the carve-out removes offset and class, which would leave four — size is also absent, subsumed into the Type column |

The front matter hedges where §4.7 does not — "On-disk structures are presented
as layout tables whose columns suit the structure — §4.7 states what they carry"
— so the two descriptions of the same convention disagree about how firm it is.

Nothing normative rides on this: §6.1's structure is a 16-byte constant, for
which "Value" is strictly more informative than "valid range", and §7.2's ranges
are carried in the Field cells and in `[R-CNT-12]`. But the claim as written is
a promise about a set of columns, and three of six tables do not deliver it. The
cheapest repair is to soften §4.7 the way the front matter already does, or to
name §6.1 and §7.2 as further carve-outs beside §7.4's.

**Byte-level: no.** Presentation only; every field's offset, width, type and
valid range is recoverable from the tables and prose as they stand, and I
recovered all of them in Part 2 without difficulty.

---

### diagrams-06 — OBSERVATION

**§24 attributes a row-label policy to §21.1 that §21.1 does not state**

`[R-VEC-02]`:

> and, for each structure the file damages, the outcome class (§2.4), the scope,
> and the §21 register row it exercises together with that row's governing
> requirement identifier — row labels are positional and renumber when a row is
> struck (§21.1), while §2.2 makes the identifier permanent, so the pair is what
> survives a renumbering.

I grepped the whole document for "renumber" and "positional". The only
occurrences are §2.2's rule about *requirement identifiers* ("they are never
renumbered or reused"), the two ordinal-renumbering claims of finding
diagrams-02, and this sentence. §21.1 says nothing about row labels being
positional, nothing about striking a row, and nothing about renumbering. The
citation is dangling: the policy exists only in §24 and is presented as §21.1's.

This is not idle. If row labels do renumber on a strike, the following in-document
references go stale silently, and none of them is a manifest entry a corpus
build would catch: §9.6's "§21.2 rows F8 and F17"; §17.2's "(§21.4, T24)";
§21.1's own "F1 of F6 and of F8, F35 of F36, L24 of L25"; F33's "F9/F10,
F31/F32, L16/L17 and T8/T9"; T2's "the same byte at a padding position is
T4's"; T13's, T15's, T16's, T23's and T26's "the check that detects it is
T24's / T25's / T2's or T4's"; §21.6's "(F18, `[R-CNT-07]`)" and "(F35, F36,
L24, L25)"; Appendix H's "(`[R-CNT-05]`, F7)" and "(`[R-CNT-15]`, F36, L25)".
So the document as it stands depends on row-label stability in about fifteen
places while §24 declares row labels unstable — and points at a section that
declares nothing.

**Byte-level: no.** `[R-VEC-02]` requires the manifest to record the row *and*
the permanent requirement identifier regardless of which policy holds, so a
corpus built to this rule interoperates either way. The cost is maintenance, not
interoperation.

---

## Part 4 — Things I checked and found clean

Recording these so the coverage claim is checkable, and because "found nothing"
is only worth reading if you can see what was looked at.

- **Every numbered list, for order, duplication and gaps.** §9.2 (1–6), §10.1
  (1–4), §18.2's four document restrictions, §19.1 (1–4), §19.4 (1–8), §20.3
  (1–6), Appendix G (1–10). All sequential, none duplicated, none skipped.
  §4.3's "four vehicles" matches §10.1's four items one for one. §22.3's "Four
  residues are stated rather than defended" is followed by exactly four.
  §21.9's `[R-ERR-05]` says "Two do not [follow from a field's width, an
  external format, or the value domain]" and names the 512 floor on A and the
  255-byte key cap; I checked the other seven hard limits and each does follow —
  in particular the 2⁶² ceiling on A and A_slab, which is the largest power of
  two inside §4.2's 0…2⁶³−1 domain, so it is derived rather than chosen.
- **§15.3's "Six rows are marked *structural*"** — six, counted.
- **§21.2/3/4/5's row counts** — 36 / 49 / 26 / 10, counted, matching their
  headers and §21.8's 121.
- **§21.8's 264 instances** — parsed and counted mechanically; exact.
- **§2.4's five outcome rows** against the outcomes actually used in §21 —
  reject-file, reject-layer, reject-tile, ignore-record all appear as subsection
  outcomes; preserve-verbatim correctly appears only as an updater obligation,
  and §2.4's pointer "§20.4's table states the cases: its MU = 1 and MU = 0 /
  PE = 1 rows" matches §20.4's table, whose three rows exhaust the four flag
  combinations because `[R-CNT-12]` folds MU = 1 / PE = 0 into MU = 1.
- **§7.3's registry table** against Appendix C's snapshot: 0x0001 layer
  MU=1/PE=1, 0x0002 user metadata MU=0/PE=1 — identical.
- **§12.1's thirteen types** against §12.2's value set, Appendix C, §21.9's
  reader guarantee and Appendix H's "all thirteen sample types" — consistent;
  element sizes 1/1/2/4/8/1/2/4/8/2/2/4/8 are each used correctly by §14.2's
  arithmetic and §13.1's fill-length rule.
- **Appendix B's 26 constants**, each against its cited section — all agree,
  including the two I recomputed (0xE3069283, 0xEECB3BB2) and the derived ones
  (record header 24, entry 20, segment 2¹⁶, sentinel `FF ×16 00 ×4`).
- **§14.4's note** that a single-channel numeric layer is byte-identical under
  either layout, and a single-channel bool layer is not (⌈P/8⌉ vs P) — both
  follow from §14.2 and §14.3's formulas.
- **§17.2's zstd window note** — a sub-1-KiB tile is encodable only as a
  single-segment frame, because the Window_Descriptor's floor is 1 KiB while
  single-segment derives Window_Size from the frame content size, which
  `[R-COD-06]` already pins to the decoded size. §14.2's examples give 18 and 30
  bytes and §14.3's gives 2, all sub-1-KiB, so the note's cross-reference lands.
- **§20.3's shapes (a)/(b)/(c)** against `[R-WRT-04]`, `[R-WRT-05]` and the new
  declaration-freeze rule. (c)'s "changing a channel's fill value on a layer with
  no padding position and no pad bit" is exactly the residue the freeze leaves
  open, and (c) correctly excludes the case the freeze bars. I specifically
  checked whether "an extent MAY always **grow**" contradicts the freeze, since
  growing an extent does shrink a stored edge tile's padding set: it is an
  express carve-out with its justification attached ("a position that becomes
  real held that channel's fill and fill is a legal sample value"), and the
  stored bytes stay conforming under `[R-SER-05]` because the surviving padding
  positions still hold fill. Not a defect.
- **Whether the new §20.3 freeze needs a §21.7 entry** — no: a file produced in
  violation of it carries the witness in its own bytes (T3/T14 for a decoded-size
  change, T17 for a codec change, T4 for a padding-set change), which is what
  §20.3's "Every such change makes each stored tile it reaches nonconforming"
  asserts. The undetectable residue (channel reordering at equal element sizes,
  filter changes with no padding) is already §21.7's ¶1 subject.
- **§5.1's three-commit figure** — two ▓ runs for two superseded
  directory/pad/trailer triples from commits 1 and 2, layer A never moving, dir₃
  re-emitted alone. Consistent with `[R-WRT-05]` and with §20.3 shape (c).
- **§9.2's crash figure** — row 2's ▓ is the interrupted write, row 3's is what
  commit n+1 superseded; both match the legend and `[R-LIF-05]`'s
  no-backward-scan rule.
- **§20.5's compaction figure** — no ▓ in the output, `′` on both regenerated
  index regions, file_id X→Y and generation 7→1. The `pad` shown in the output
  is required by `[R-LIF-02]` step 5 and is newly created slack, not carried
  slack, so it does not contradict "slack is never carried".
- **§9.7's walk against §5.2's claimant classes** — the tile-index region enters
  once as the layer record's extent and is not double-counted, which §9.7 says
  in as many words; the [16, F−64) bound plus explicit claiming of [0,16) and
  [F−64, F) covers the file.
- **§19.1's four open steps and §19.3's layer-access list** against the
  register's Detected column — the layer *name* rows L3/L5/L6 are correctly at
  "open" while the dimension/channel name rows L4/L7/L8 are at "layer access",
  matching step 4's "each layer record's name, parsed and checked per §4.6". The
  §19 preamble ("Those enumerations are not the complete inventory … §21's
  register is") pre-empts any incompleteness claim against these lists, and I
  found nothing in them that is affirmatively wrong.
- **Appendix H's four class checklists** against §2.3, §14, §16, §18, §20 and
  §21 — the reader list's codec/filter/layout/type/encoding counts are right,
  the verifier list reaches every verifier-detected row, the updater list's
  MU/PE handling matches §20.4. The writer and updater lists are summaries and
  omit some obligations (writers' flags = 0, the §20.3 declaration freeze), but
  Appendix H says "A summary of each class's obligations" and "each entry's
  authority is the requirement or section cited, never this summary", so I do
  not treat the omissions as promise-breaking.
- **Appendix G's closing recap** enumerates nine of the profile's ten additions
  and omits item 10 (NFC normalization) — but the paragraph closes with "Read
  the numbered items as the list; this paragraph names what they are for, not
  how many there are", which disclaims exactly that. Not reported.
- **§21.6's "The file contains zero layers → A conforming file with an empty
  directory"** is narrower than the condition (a zero-layer file may still carry
  a top-level user-metadata record), but it restates `[R-CNT-14]`'s own
  parenthetical faithfully and no implementation goes wrong. Not reported.
- **R5–R10, F27 and L48 are not re-qualified for unassigned encodings** the way
  R3 is ("under an unassigned one this specification defines no decoding"). I
  chased this as a candidate propagation miss from `[R-MTA-10]` and concluded it
  is not one: R5, R6 and R7 say "a *decoded* user-metadata document", which
  cannot exist under an encoding this specification defines no decoding for, and
  `[R-MTA-10]` plus §21.6's row govern the rest.
