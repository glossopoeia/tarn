# Cleanroom round 27 — Diagram auditor — working transcript

## 0. Access, disclosure, method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines — the brief said 4,550; the file has 4,549 newline-terminated
lines, which is the same document, and I mention it only because I checked).
It was exactly where the brief said it would be.

I opened no other file. No `docs/`, no `conformance/`, no `PLAN.md`, no
`AGENTS.md`, no `spec/registry.json`, no git history, no directory listings,
no web.

I ran three Python scripts I wrote myself in the scratchpad:
`crc.py` (a CRC-32C implementation, reads no files), `appa.py` (Appendix A's
hexdump transcribed inline from what I had read, reads no files), and
`count.py` (reads `spec/tarn.md` only, to count register rows and instances
mechanically). I wrote this transcript. I did not read the output directory.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointer and an index of the maintainer's
persistent notes with descriptive titles, plus a working directory whose name
(`scratch/cleanroom`) is not one the brief named. I disregarded all of it —
I did not open any file it referenced and no finding below derives from it. I
name its appearance here as the brief requires and do not repeat its contents.

Method as the charter directs: **enumerate first, judge second.** Section 1
below is the full inventory with line numbers. Section 2 is the arithmetic I
actually performed. Section 3 is the per-figure walk. Section 4 is the
findings in full prose.

---

## 1. Inventory of figures, diagrams, byte-layout boxes, worked examples,
## tables that restate rules, and checklists

Line numbers are of the first line of each item.

### Blockquoted display material (I enumerated every blockquote in the file
### mechanically with an awk pass over lines beginning `>`)

Labelled *Note* / *Example* / *Rationale* blocks — non-normative by
`[R-CNF-01]` — at lines 12, 108, 271, 327, 423, 455, 495, 531, 576, 599, 640,
647, 729, 738, 748, 788, 792, 828, 844, 906, 1127, 1168, 1216, 1254, 1260,
1265, 1303, 1339, 1348, 1432, 1522, 1551, 1585, 1591, 1609, 1647, 1655, 1710,
1729, 1759, 1798, 1812, 1829, 1844, 1850, 1855, 1932, 1943, 1950, 1977, 1984,
2009, 2013, 2019, 2040, 2047, 2055, 2096, 2151, 2164, 2179, 2210, 2256, 2263,
2267, 2279, 2334, 2374, 2384, 2404, 2424, 2429, 2463, 2468, 2602, 2681, 2744,
2856, 2954, 2961, 3155, 3163, 3172, 3268, 3366, 3407, 3844, 3913, 4143.

**Exactly one blockquote carries no such label: line 2071–2072**, §15.1's
tile-index region layout box:

> [ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]

By `[R-CNF-01]` — "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative" — this box is **normative**. The
brief warned that at least one such block exists and that an earlier briefing
in this project got the rule backwards. I checked the label, not the marker.
The box is treated as normative by its surroundings (§15.1 says "the
tile-index region ... is, contiguously:" and then the box, then "with no
padding anywhere inside the region"), and its content agrees with
`[R-CNT-17]`'s length formula, §15.4's segmentation and §8.1's map. No
finding here; recorded because the label check is part of my charter.

### Byte-layout / offset tables

| Line | Table |
|---|---|
| 126 | §2.2 requirement-prefix table (the presentation change — list → table) |
| 294 | §2.4 outcome-class table (5 rows) |
| 760 | §6.1 front signature block, 16 bytes |
| 803 | §6.2 trailer, 64 bytes, 11 fields |
| 968 | §7.2 record header, 24 bytes, 5 fields |
| 1043 | §7.3 record types of format major 1 |
| 1072 | §7.4 layer-record inline payload (16 rows, packed variable-length) |
| 1190 | §8.1 checksum coverage map (7 rows) |
| 1465 | §10.2 numeric identifier spaces (8 rows) |
| 1676 | §12.1 sample types (13 rows) |
| 1908 | §14.2 decoded size / offset-of-value-k |
| 2071 | §15.1 index region layout box (unlabelled ⇒ normative) |
| 2076 | §15.1 index entry, 20 bytes, 3 fields |
| 2124 | §15.3 entry-validity classification (11 rows) |
| 2520 | §18.2 user-metadata record inline payload, 1 byte |
| 2710 | §18.4 standardized keys (6 rows) |
| 3246 | §20.4 stored-flags → updater-obligation (3 rows) |
| 3500 | §21.2 file-scope register (36 rows) |
| 3544 | §21.3 layer-scope register (49 rows) |
| 3601 | §21.4 tile-scope register (26 rows) |
| 3651 | §21.5 ignored-record register (10 rows) |
| 3669 | §21.6 conditions that are not violations (14 rows) |
| 3808 | §21.9 minimum-guarantee limits (8 rows) |
| 4178 | Appendix A annotation table (14 rows) |
| 4214 | Appendix B constants (26 rows) |
| 4311 | Appendix E changelog (1 row) |

### ASCII diagrams

| Line | Diagram |
|---|---|
| 650 | §5.1 — a file after three commits |
| 1269 | §9.2 — what a crash sees (3 rows) |
| 3177 | §20.3 shape (a) — a new layer |
| 3194 | §20.3 shape (b) — tiles added to an existing layer |
| 3217 | §20.3 shape (c) — a change confined to the directory |
| 3369 | §20.5 — what compaction reclaims |

### Worked numeric examples

| Line | Example |
|---|---|
| 576 | §4.6 `température` NFC/NFD byte counts |
| 640 | §5.1 smallest conforming file, 128 bytes |
| 1127 | §7.4 complete layer-record payload, 81 bytes, byte-by-byte |
| 1591 | §11.2 grid arithmetic |
| 1647 | §11.4 ordinals |
| 1710 | §12.1 bfloat16 |
| 1759 | §12.3 channel entry, 12 bytes |
| 1829 | §13.3 fill tuples |
| 1950 | §14.2 interleaved/planar byte offsets |
| 1984 | §14.3 packed boolean plane |
| 2040 | §14.5 padding content |
| 2164 | §15.4 entry_count = 1,000,000 |
| 2179 | §15.4 planar entry placement |
| 2279 | §16.2 slab runs |
| 2463 | §17.3 byte-shuffle |
| 3163 | §20.3 superseding one tile |
| 4167 | Appendix A annotated minimal file (128-byte hexdump) |

### Checklists and numbered lists (count as figures per the charter)

| Line | List |
|---|---|
| 1235 | §9.2 commit protocol, steps 1–6 |
| 1445 | §10.1 the four extension vehicles |
| 2772 | §19.1 open algorithm, steps 1–4 |
| 2901 | §19.4 tile-read algorithm, steps 1–8 |
| 3025 | §20.3 append procedure, steps 1–6 |
| 4346 | Appendix G reproducible-writer profile, items 1–10 |
| 4484 | Appendix H conformance checklists (5 classes) |
| 4251 | Appendix C registry snapshot |
| 4322 | Appendix F normative references |

---

## 2. Arithmetic and byte-level checks I actually performed

I implemented CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and validated it
against §4.5's own check vector before using it for anything else.

```
CRC-32C("123456789")            = 0xE3069283   §4.5 says 0xE3069283   ✓
CRC-32C(zero bytes)             = 0x00000000   §4.5 says 0x00000000   ✓
```

**§7.4's worked layer record.** entry_count = 4, so the entry array is
4 × 20 = 80 bytes, all sentinel (`FF ×16 00 ×4` each), and the segment CRC
array is ⌈4/2¹⁶⌉ × 4 = 4 bytes.

```
CRC-32C(4 sentinel entries, 80 bytes) = 0x80A34955   §7.4 says 0x80A34955, stored 55 49 A3 80  ✓
CRC-32C(those 4 bytes)                = 0xC4EE982E   §7.4 says 0xC4EE982E, stored 2E 98 EE C4  ✓
```

**§15.4 / Appendix B constant.**

```
CRC-32C(2¹⁶ sentinel entries) = 0xEECB3BB2   §15.4 and Appendix B say 0xEECB3BB2  ✓
```

**Appendix A, byte for byte.** I transcribed the 128-byte hexdump from lines
4168–4175 and recomputed everything:

```
file length                      128                              ✓ (§5.1, [R-CNT-27])
[0,8)   89 54 41 52 4E 0D 0A 1A  = front magic                    ✓ §6.1
[8,16)  zero                                                       ✓ §6.1
[16,20) 00 00 00 00              = CRC-32C(zero bytes)            ✓ §7.1
[20,64) zero, 44 bytes           = 64 − 20 = 44                   ✓ §6.2 pre-trailer pad
trailer offset 0..7   magic 8A 4E 52 41 54 0D 0A 1A               ✓
trailer offset 8..9   01 00 = version_major 1                     ✓
trailer offset 10..11 00 00 = version_minor 0                     ✓
trailer offset 12..15 flags 0                                     ✓
trailer offset 16..23 generation 1                                ✓
trailer offset 24..31 dir_offset 16                               ✓
trailer offset 32..39 dir_length 4                                ✓
trailer offset 40..47 committed_file_length 128                   ✓
trailer offset 48..55 file_id 0x0123456789ABCDEF (LE EF CD AB …)  ✓
trailer offset 56..59 reserved zero                               ✓
CRC-32C(trailer bytes [0,60)) = 0xE00938D2, stored D2 38 09 E0    ✓
```

Every field lands where §6.2's layout table puts it; the offsets in that table
sum to exactly 64 (8+2+2+4+8+8+8+8+8+4+4), which is what §6.3's "The
format-major-1 trailer has zero slack: every byte is assigned" asserts, and
`[R-CNT-24]`'s three fixed positions (magic at F−64, version at F−56, CRC at
F−4) plus its 48 redeemable bytes come to 16 + 48 = 64 ✓.

**§7.4's payload offsets** (I walked the packed field list independently and
then compared with the example's own offset column):

```
 0 name 1+3 = 4        →  4
 4 layout u8           →  5
 5 linearization u16   →  7
 7 codec u16           →  9
 9 filter u16          → 11
11 A u64               → 19
19 S u64               → 27
27 A_slab u64          → 35
35 rank u8             → 36
36 C u16               → 38
38 dim entry 1+1+8+8=18→ 56
56 chan entry 1+4+2+1+4=12 → 68
68 index_encoding u8   → 69
69 entry_count u64     → 77
77 crc_of_crc_array u32→ 81
```

Total 81 = the example's stated `inline_length`. The example's own summation
("Name and the nine scalars from layout through channel count occupy 4 + 34
bytes, the dimension entry 18, the channel entry 12, and the trailing fixed
fields 13 — 81 exactly") checks: the nine scalars are 1+2+2+2+8+8+8+1+2 = 34,
and 4+34+18+12+13 = 81 ✓. The extent-slot length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 ✓
matches `[R-CNT-17]`. The channel entry bytes `04 74 65 6D 70 0C 00 04 00 00
C0 7F` are byte-identical to §12.3's twelve-byte example ✓ (the example says
"byte for byte", and it is).

**§11.2's example.** (1024,2048)/(256,256) ⇒ G=(4,8), N=32, P=65,536 ✓.
(1000,2048) ⇒ G_y = ⌈1000/256⌉ = 4 ✓.

**§11.4's example.** (300,700) ⇒ tile (1,2), s = 1·8+2 = 10 ✓; in-tile
(44,188) ⇒ 44·256+188 = 11,452 ✓; planar C=4, channel 2 ⇒ 2·32+10 = 74 ✓.

**§14.2's example.** Q = 1+2 = 3, decoded size 6·3 = 18 ✓; ordinal 5 ⇒
5·3 = 15, sample [15,18) ✓; planar b: 6·2 = 12 bytes, ordinal 5 at 10–11 ✓;
float32+bool: Q = 5, size 30, ordinal 5 at [25,30), `t` 25–28, `m` 29 ✓.
The general form u·Q + Fᶜ with k = u·C + c reduces correctly: k div C = u,
k mod C = c ✓.

**§14.3's example.** P = 10, alternating from true: byte 0 bits 0,2,4,6 set =
0x55 ✓; byte 1 holds values 8 (true) and 9 (false) ⇒ 0x01 ✓; with fill true
the six pad bits 2–7 set ⇒ 0x01 | 0xFC = 0xFD ✓.

**§14.5's example.** (5,5)/(4,4) ⇒ grid 2×2; tile (1,1) covers 4–7 on both
axes ⇒ 16 positions, one real ((4,4)), 15 padding ✓; one uint16 channel ⇒
32 bytes ✓; fill 0xABCD little-endian ⇒ `CD AB` ✓; value 0 is (4,4) because
its in-tile ordinal is 0 ✓.

**§15.4's example.** entry_count 1,000,000 ⇒ ⌈10⁶/65,536⌉ = 16 segments,
15 full (983,040 entries) and a last of 16,960 ✓; CRC array 64 bytes ✓;
region 20,000,064 bytes ✓; k = 999,999 is in segment 15 at segment-relative
byte 20 × (999,999 − 983,040) = 20 × 16,959 = 339,180 ✓; array at
[20,000,000, 20,000,064) ✓; segment 15 at [19,660,800, 20,000,000), which is
339,200 bytes ≈ "~339 KB" ✓; one full segment = 65,536 × 20 = 1,310,720 =
1.25 MiB ✓. Second example: disk ordinal 74 ⇒ region bytes [1,480, 1,500) ✓;
channel 3's tiles are ordinals 96–127, 32 entries ✓.

**§16.2's example.** N = 32, S = 8 ⇒ runs [0,8), [8,16), [16,24), [24,32) ✓;
under row-major, ordinals 0–7 are one tile row ✓; tile rows 1–2 are ordinals
8–23 = runs 1 and 2 ✓.

**§17.3's example.** 1.0f/2.0f/3.0f little-endian = `00 00 80 3F 00 00 00 40
00 00 40 40` ✓. s = 4, n = 3, offset i·n + j:
i=0 → 00 00 00; i=1 → 00 00 00; i=2 → 80 00 40; i=3 → 3F 40 40, giving
`00 00 00 00 00 00 80 00 40 3F 40 40` ✓ exactly as printed.

**§20.3's example.** 32-tile index region = 32·20 + ⌈32/2¹⁶⌉·4 = 644 ✓.

**§21.9's Note.** At entry_count = 2³², the segment-CRC array is
(2³²/2¹⁶) × 4 = 2¹⁶ × 4 = 262,144 bytes = 256 KiB ✓; at 2³⁶ it is 2²⁰ × 4 =
4 MiB ✓. 65,536 layers at ~200 bytes/record ≈ 12.5 MiB ✓.

**Register counts, computed mechanically** (`count.py`, applying §21.1's own
rule: instances are semicolon-separated, a cell reading `—` is one instance):

```
§21.2  F1..F36   36 rows   58 instances   (preamble says "36 conditions")  ✓
§21.3  L1..L49   49 rows  116 instances   (preamble says "49 conditions")  ✓
§21.4  T1..T26   26 rows   55 instances   (preamble says "26 conditions")  ✓
§21.5  R1..R10   10 rows   48 instances   (preamble says "10 conditions")  ✓
TOTAL            121 rows 277 instances
§21.8 says "121 conditions over 277 instances"                             ✓
```

I nearly filed a finding here: reading §21.3 I counted only 48 rows against a
stated 49, before finding L49 on line 3594, past the point where my first read
window ended. It is there. Noted so a checker can see the near-miss.

**Requirement identifier hygiene** (numbered-list check, applied to the
identifier space): every prefix used in the document appears in §2.2's table,
and every prefix's numbering is gapless from 1 to its maximum — CNF 1–13,
CNT 1–27, COD 1–11, ENC 1–16, ERR 1–5, EXT 1–5, GEO 1–6, IDX 1–5, LIF 1–8,
MDL 1–2, MTA 1–10, PRV 1–5, RDR 1–4, SEC 1–7, SER 1–9, SLB 1–5, TYP 1–10,
VEC 1–4, WRT 1–9. `[R-SER-04]` is present only in §14.4's withdrawal Note,
which §2.2 licenses ("a withdrawn requirement leaves its identifier
permanently retired"). `[R-ENC-100]` appears only as §2.2's own illustration
of numbering above 99. No duplicates, no gaps, nothing missing. The §2.2
table's 19 rows map one-to-one onto the 19 prefixes actually used.

---

## 3. The per-figure walk

### §2.2's prefix table (the flagged presentation change)

The brief told me one of the thirteen changed passages is a list restated as a
table with the assertion that nothing changed, and told me to check the
assertion rather than grant it. I cannot see the old list, so I checked the
table against the document instead. Every prefix in use is in the table; no
prefix in the table is unused; each expansion matches the section that owns
the prefix (CNF→§2, MDL→§3, ENC→§4, CNT→§5–§8, LIF→§9, EXT→§10, GEO→§11,
IDX→§15, SLB→§16, TYP→§12–§13, SER→§14, COD→§17, MTA→§18, RDR→§19, WRT→§20,
ERR→§21, SEC→§22, PRV→§23, VEC→§24). The row order is not document order
(IDX and SLB precede TYP and SER), but the section makes no ordering claim and
explicitly says "Identifier order carries no meaning," so I do not report it.
The one expansion I hesitated over is `ERR | error register`: §21 is
"Error-Handling Register **and Limits**", and `[R-ERR-03]`/`[R-ERR-04]`/
`[R-ERR-05]` are limits rules, not register rules. That is a mnemonic, not a
requirement, and I judged it an over-flag.

### §6.1's and §6.2's tables against §4.7's Note

§4.7's Note promises that layout tables give "byte offset within the
structure, size, type, name, taxonomy class, and valid range, each table
giving the columns its structure needs", then states two exceptions: §6.1's
block "is a 16-byte constant, where a Value column replaces type and range",
and §7.2 "folds each field's range into its Field cell". Checked:

- §6.2 trailer: Offset | Size | Type | Field | Class | Valid values — all six ✓
- §15.1 entry: all six ✓
- §18.2: all six ✓
- §7.2: Offset | Size | Type | Field | Class, ranges folded into Field ✓
- §7.4: Field | Type | Constraint, no offset/class column — exactly what the
  Note licenses for a packed variable-length payload ✓
- §6.1: Offset | Size | Value | Class — Value replaces type *and range*
  **and the name column**, which the Note does not mention.

I considered filing the §6.1 column as a finding and decided against it. The
first row's Value cell (`89 54 41 52 4E 0D 0A 1A` (`\x89`, "TARN", CR, LF,
ctrl-Z)) names the field as effectively as a Name column would, no
implementer is misled, and the Note's hedge "each table giving the columns its
structure needs" arguably covers it. This is exactly the kind of editorial
over-flag I was warned not to pad the list with.

### §8.1's coverage map

Seven rows. I checked it is a partition of the structure classes §5.2 names:
front block (equality), trailer, directory, tile-index region, stored tile,
user-metadata extent, unassigned-type record extent. §5.2's claimant classes
are front block, stored-tile extent, record extent (any type), directory,
trailer — and the three record-extent kinds in format major 1 (layer record's
index region, user-metadata extent, unassigned-type extent) each get a row ✓.

§4.5's split into terminal and interior checksum fields checks against the
map: terminal = trailer CRC, directory CRC, user-metadata extent CRC (three,
as §4.5 says); interior = segment CRC array (covered by crc_of_crc_array),
each entry's crc field (covered per segment), crc_of_crc_array (covered by the
directory CRC, since it sits in a layer record's inline payload). Each
interior field is "both comparison-verified and covered by exactly one further
checksum" ✓.

§8.2's chain — trailer → directory → crc_of_crc_array → segment CRC array →
index segment → index entry → stored tile — has seven nodes and matches ✓.
It mixes checksum links with containment links (segment → entry is
containment, not a checksum), which is harmless: §8.1's map is the authority
and says so.

### §10.2's identifier-space table

Eight rows, checked each against the section that defines the space:
record type (§7.3, assigned 0x0001–0x0002, reserved 0x0003–0x7FFF, exp
≥0x8000) ✓; channel layout (§14.1 `[R-SER-06]`: "values 3 through 255 are
reserved", no experimental) ✓; linearization (§11.4: 2–3 reserved without
semantics, 4–0x7FFF reserved for assignment, so 2–0x7FFF reserved) ✓;
sample type (§12.2: 14–19 and 20–0x7FFF, so 14–0x7FFF) ✓; codec (§17.2) ✓;
filter (§17.3) ✓; index encoding (§7.4/§15.1) ✓; metadata encoding (§18.2) ✓.
"Value 0 is invalid in every space above" ✓ each section says so.

"Two spaces carry no experimental range: channel layout ... and the trailer's
flag lanes" — only one of the *tabulated* spaces (channel layout) shows
"none", the flag lanes not being in the table at all. The sentence names them
explicitly and says §6.3 partitions them instead, so this is a deliberate
carve-out rather than a miscount. Not reported.

I cross-checked §20.5's closed count against this table: "the two of §10.1's
four vehicles §21.6 makes conforming" = ignore-lane bits and unrecognized
`tarn.` keys (both in §21.6) ✓; "F36 and L25 for a record type, and one row
for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43,
L45, R1)" — eight spaces minus record type = seven, and the seven cited rows
are index encoding (L31), linearization (L33), sample type (L34), layout
(L36), codec (L43), filter (L45), metadata encoding (R1), each of which does
register the reserved range ✓. Seven spaces, seven rows, no gap.

### §12.1's sample-type table

Thirteen rows, IDs 1–13, element sizes 1/1/2/4/8/1/2/4/8/2/2/4/8 ✓. "exactly
thirteen" ✓; "the twelve types other than bool are this specification's
numeric types" ✓. Appendix C's compressed restatement (1 bool · 2–5 · 6–9 ·
10 · 11 · 12 · 13) reproduces it ✓, and its "Pinned reservations" reproduce
§12.2's Note (14/15 OCP OFP8 E4M3/E5M2, 16 int128, 17 uint128, 18 float128,
19 raw-bytes/"opaque") ✓.

### §14.2's byte-layout table

Two rows: planar-numeric (P·Bᶜ, k·Bᶜ) and interleaved (P·Q,
(k div C)·Q + F_{k mod C}). Verified against `[R-SER-01]`'s value sequence:
interleaved value k is channel (k mod C) at ordinal k div C, so its byte
offset is (k div C)·Q + F_{k mod C} ✓. The table correctly omits planar bool,
which §14.3 governs, and the preamble scopes itself to "a planar tile of a
numeric channel ... and ... every interleaved tile" ✓ — narrower than a
careless reader might take it, and correctly so.

### §15.3's entry-validity table

Eleven rows. The preamble says "Six rows are marked *structural*"; I counted
the *structural* markers: sentinel-with-crc≠0, half-sentinel, length 0,
offset < 16, offset/length > 2⁶³−1, overflow-or-past-F−64 = **six** ✓. The
non-structural reader row is "stored bytes fail the entry's crc"; the three
*verifier* rows are intra-layer overlap, cross-layer overlap, alignment/slab.

Cross-checked against §21.4: T6 = sentinel-with-crc≠0; T7 = half-sentinel;
T10 = length 0; T8 = offset < 16; T11 = field above 2⁶³−1; T12 = overflowing
sum; T9 = past F−64; T1 = failed crc; and the verifier rows map to L18, F33,
L40/L41/L42 ✓. Nothing in the table lacks a row and no row lacks a table line.

The boundary is consistent everywhere I checked it: `[R-CNT-13]` and L17/F32
make `offset + length > F − 64` the violation, §15.3 and T9 agree, and §9.7's
"each lies within [16, F − 64)" is the same bound stated as a half-open
interval ✓.

### §21's register — completeness sweep

§21.1 makes the register's completeness normative. I walked the requirement
inventory looking for a detectable file-conformance violation with no row.

*File scope.* `[R-ENC-02]`→F1; `[R-ENC-03]`→F2; `[R-ENC-04]`→F3;
`[R-ENC-15]`→F4; `[R-CNT-27]`→F5; `[R-CNT-04]`→F6; `[R-CNT-05]`→F7;
`[R-CNT-06]`→F8–F17 (ten rows — which is exactly the "ten" §2.3's
`[R-CNF-13]` attributes to that rule, of which the magic and the CRC reach a
foreign major and "the other eight do not": 10 − 2 = 8 ✓); `[R-CNT-07]`→F18;
`[R-CNT-08]`→F19; `[R-CNT-11]`→F20; `[R-CNT-25]`→F21/F22; `[R-MTA-03]`→F23;
`[R-CNT-12]`→F24/F25/F26/F29; `[R-MTA-05]`→F27; `[R-CNT-22]`→F28;
`[R-CNT-13]`→F30/F31/F32/F33; `[R-CNT-14]`→F34; `[R-CNT-15]`→F35/F36.
`[R-CNT-02]`'s untestable half is accounted for by §5.2's Note ("a register
row for it would be a row no file could exhibit"), its testable half by F33
and L18 ✓.

*Layer scope.* I walked §7.4's constraint table row by row and found a
register row for each constraint: name (L3/L5/L6 at open, F4 for uniqueness),
layout (L36), linearization (L33), codec (L43), filter (L45), A (L39),
S (L1's upper bound), A_slab (L28/L29), rank & C (L32), dimension names
(L4/L7/L8/L9), extents & tile extents (L1, L32), channel type (L34), fill
length (L30), bool fill (L35), index_encoding (L31), entry_count (L21, L1),
crc_of_crc_array (L27, L37), sub-records (L10–L19, L24–L26, L46–L49), plus
L20, L22, L23, L2, L18, L38, L40–L42, L44. All 49 accounted for; no §7.4
constraint left unregistered.

*Tile scope.* §14's and §17's obligations: T1–T12 (index/crc), T13 (§17.1's
independence), T14 (codec 1 equality), T15/T16 (deflate), T17–T22 (zstd's six
frame constraints, which are exactly the six `[R-COD-06]` states), T23 (lz4
frame), T24/T25 (`[R-COD-08]`'s two halves — "consume exactly" is T24, "decode
to exactly the decoded size" is T3), T2/T4/T5 (content), T26 (stride). No gap.

*Ignored records.* §18.2's four decoded-document restrictions map to R7
(object/BOM/well-formedness), R8 (finite numbers), R9 (duplicate keys),
R5/R6/R10 (UTF-8 and the folded name rules), with R1 (encoding value),
R2 (extent CRC), R3 (decode failure) and R4 (encoding-2 frame constraints)
covering the framing. R4's sixteen instances are eight alternatives × two
containers, and the eight are exactly what §18.2 carries over minus the two it
says carry no witness (undisclosed dictionary use; the buffer-sizing bar) ✓.

*Instance-counting rules.* §21.1's stated axes reproduce mechanically:
"differs from"/"does not equal" rows enumerate both directions (L21, L22, L30,
T3, T14, T22), "exceeds"/"larger than" rows enumerate one (L44, T21), rows
with no magnitude ordering enumerate none (F14, F20, L37, L38, T1), and
nonzero-value tests are not comparisons (L28, L20). Layout-varying quantities
enumerate the three layout shapes (L44, T3, T14, T21, T22, T26). Single
predicates over several fields are one instance (F25, F3's per-sum entries,
L20). Every cell I spot-checked follows its own stated rule.

*L2's designated quantities.* I derived them independently:
`[R-CNT-13]`'s extent sums (×2 containers), `[R-GEO-03]`'s N, P,
addressed-tile count and N·P, `[R-SER-02]`'s P·Q and P·Bᶜ, `[R-SER-07]`'s V,
and `[R-CNT-17]`'s index-length formula. The cell's nine entries name exactly
these, with V folded under P·Q ("which dominates V = P·C" — correct, since
Q = ΣBᵢ ≥ C) and the maximum disk ordinal folded under C·N ("which dominates
(C−1)·N + (N−1)" — correct, that being C·N − 1) ✓. Q and Fᶜ are designated
but bounded by 65,535 × 8, so they exhibit no instance ✓.

### §21.2's reach derivation

The preamble says deriving `[R-CNF-13]` yields "F8, F14, F6 and both of F1's
instances ... and no other row". I derived it myself. `[R-CNT-24]` fixes four
invariants: trailer magic at F−64, version fields at F−56, a CRC-32C at F−4
over [F−64, F−4), and the front block's constancy. F8 asserts the first, F14
the third, F6 and F1's front-block instance the fourth, F1's trailer-magic
instance the first. Every other file-scope row asserts something about a
format-major-1 structure or about one of the 48 redefinable trailer bytes:
F13 (64-alignment of F) and F17 (committed_file_length against the transport
size) and F19 (flags) and F2/F3/F9/F10/F11/F12/F16 all read redefinable
fields, F15 is expressly the 48-byte case, F20 onward are directory and record
structures, and F18 is version_major = 0, which the preamble correctly places
outside the premise rather than inside the test. I could not find a
seventeenth reaching condition. The §2.3 Note's three worked cases (F14
reaches, F5 does not, F15 does not) each check out.

### §20.3's three diagrams

Shape (a): before `front | A: tiles+index | dir₁ pad tr₁`, after
`front | A | ▓(was dir₁…tr₁) | B: tiles+index | dir₂ pad tr₂`. Consistent
with `[R-LIF-01]` (nothing rewritten) and `[R-WRT-05]` (A's record carried
byte-identically, extent slot and all) ✓.

Shape (b): the whole index region moves because one extent slot addresses it ✓
— which is the same fact §20.3's Note quantifies ("editing one sample of a
10⁶-tile layer appends about 20 MB of index": 10⁶ × 20 + 16 × 4 = 20,000,064
bytes ✓).

Shape (c): "clearing a slab declaration, renaming a layer, or changing a
channel's fill value on a layer with no padding position and no pad bit."
I checked the fill case against step 4's bar. Fill enters §14 only through
`[R-SER-05]` (padding positions and pad bits). A layer with no padding
position and no pad bit has no stored byte whose content fill fixes, so
changing fill alters nothing §14 fixes for a stored tile ✓, and the diagram's
"Only the directory is re-emitted" holds ✓. The complementary claim — "A fill
change on a layer that **stores** a tile carrying either is not an appender's
operation at all" — is likewise right ✓.

I also checked §11.1's Rationale claim that "Growth that leaves entry_count
unchanged touches the directory alone". Under growth, every Gᵢ is
non-decreasing, so an unchanged product either leaves every Gᵢ unchanged (the
extents grew inside their existing grid — e.g. E from 100 to 128 with T = 32,
G staying 4) or holds the product at 0 through a dimension that stays at
extent 0 — which is the case the Rationale explicitly names. Both leave the
index region untouched ✓. The phrase "a zero-extent layer's **last** zero grid
count" I read as *the one whose raising leaves none remaining*, which is the
only reading that makes the sentence true; the preceding clause ("while
another stays 0 among them") fixes it. Not a finding.

### §5.1, §9.2, §20.5 diagrams

§5.1's three-commit figure: I reconstructed the commit sequence and the
layout falls out exactly — `front | A | (dir₁ pad tr₁) | B | (dir₂ pad tr₂) |
dir₃ pad tr₃`, two ▓ runs for two superseded commits, and commit 3 touching no
layer re-emits directory, pad and trailer alone ✓. The figure is explicitly
self-limiting about the `tiles+index` grouping ("illustrative: a layer's
structures need not be contiguous or ordered (`[R-SLB-05]`)") ✓.

§9.2's crash figure: three rows, ▓ correctly annotated per row ✓; the
mid-commit row shows trailₙ intact but not at the end, which is exactly what
`[R-LIF-05]`'s trailer-at-end-or-fail path sees ✓.

§20.5's compaction figure: output carries no ▓ except the pre-trailer pad
(shown as `pad`), which is what "slack is never carried" means ✓; file_id X→Y
and generation 7→1 ✓ per `[R-WRT-06]`. The claim that the tile-index region is
"the one kind this operation regenerates rather than copies" is true for
format major 1 (the only MU=1 registered type is the layer record) and
`[R-WRT-07]` itself allows a wider case for an implemented MU=1 registered
type — but the figure is an Example and format-major-1-scoped, so I let it
stand.

### Appendix H's five checklists

*File*: matches §2.4/§5.2/§8.1/§21 ✓.

*Reader*: "implements all four codecs, both filters, both layouts, all
thirteen sample types, and both user-metadata encodings" — I checked each
count against its defining section: §17.2 makes 1–4 core (four) ✓, §17.3 makes
1–2 core (two) ✓, §14.1 defines two layouts ✓, §12.1 defines thirteen core
types ✓, §18.2 makes both assigned encodings core ✓. Every number is right.

*Writer* and *Updater*: summaries, and the appendix says so ("each entry's
authority is the requirement or section cited, never this summary"). I checked
that nothing stated is wrong rather than that everything is stated.

*Verifier*: I enumerated the verifier-detected rows from the register — F7,
F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2,
T4, T5, T26 — and confirmed each is reachable from a checklist line: F7 →
"no structure between the live directory's end and the live trailer";
F25/F26/L46/L47 → "record flag bits — reserved bits, MU = 1 with PE = 0";
F28/L49 → "a registered type's stored bits against §7.3's registry";
F27/L48 → "user-metadata member ordering"; F33/L18 → "extent overlap";
F36/L25 → "a reserved-range record or sub-record type value, whatever its MU
bit"; L40/L41/L42 → "alignment and slab invariants"; T2/T4/T5/T26 →
"decoded-content obligations". Plus the coverage partition, the slack total
and its partial form, the front block by equality (F1, F6), and `[R-CNF-11]`'s
reporting duties. Nothing verifier-detected is missing. This is the most
complete checklist in the document and it survives the sweep.

### Appendix B's constants table

Appendix B claims completeness ("Every named constant this specification
fixes, collected"), and §4.7's Note repeats it ("All named constants appear
once in Appendix B"). I went hunting for a missing one: the front block, the
trailer magic, the trailer size and alignment, the 128-byte minimum, the
directory minimums, extent_length ≥ 5, the bool byte encoding, the media type,
the 24-byte header, the 20-byte entry, the 2¹⁶ segment, the sentinel, the
all-sentinel segment CRC, the CRC parameters and check vector, the value
domain, the 255-byte name cap, rank/channel widths, S, A, A_slab, the
discovery window, the tile working range, the zstd frame magic, the lz4 cap,
the `tarn.` prefix, and the reader minimum guarantees — all present, and the
guarantee row reproduces all eight of §21.9's rows exactly. The only named
byte-constant in the document that Appendix B lacks is the **LZ4 frame magic
`04 22 4D 18`** (§21.4's T23), which is LZ4's constant and not one this
specification fixes. I judged that outside the claim.

### Appendix G's numbered profile — where I did find things

Item 2's `file_id` derivation is well founded: its hash input is
[0, F − 64) followed by trailer bytes [0,60) with the `file_id` field
(trailer offsets 48–55, inside the first 60) zeroed, so the trailer CRC at
[60,64) — the only field that depends on `file_id` — is excluded, and the
derivation is not circular ✓.

Item 3's total emission order is deterministic: layers in name order, tiles in
disk-ordinal order, index region, then remaining record extents in record
order, then the directory, with the first structure at 16 ("which §5.2 counts
as no structure" — correct, `[R-CNT-02]` lists the front block *beside* the
structure classes, not among them ✓). The ordering key masks `extent_offset`
precisely because the order fixes it ✓ and every other component is a function
of content ✓.

Item 5's identity claim I checked algebraically. The byte-shuffle maps byte
*i* of group *j* to offset i·n + j, i.e. offset j·s + i ↦ i·n + j. Setting
i·n + j = j·s + i for all i < s, j < n: at s = 1 only i = 0 exists and both
sides are j; at n = 1 only j = 0 exists and both sides are i; and for s > 1,
n > 1 the pair (i,j) = (1,0) sends offset 1 to offset n ≠ 1. So "the identity
exactly where the stride is 1 ... and equally where the decoded image is a
single group, n = L/s being 1" is **correct**. The trailing clause is not —
see finding 02.

Item 10's NFC claim I checked against Unicode's own normalization mechanics —
see finding 03.

The closing paragraph disclaims its own count ("Read the numbered items as the
list; this paragraph names what they are for, not how many there are"), which
is why I did not file its omission of item 5's fixed-filter-value pinning.

---

## 4. Findings

### diagrams-01 — §20.4's MU = 1 row bars compaction "on the same ground", whose nearest antecedent is the file-scope ground alone, while `[R-WRT-06]` bars it for *any* unimplemented MU = 1 record

**Location.** §20.4, the stored-flags/updater-obligation table,
`MU = 1` row (line 3248), governed by `[R-WRT-08]`; against §20.5,
`[R-WRT-06]` (lines 3326–3329).

**Quoted, §20.4:**

> | MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the
> record governs. At layer scope an unknown critical record blocks
> modification of that layer, leaving other layers editable (`[R-CNT-18]`).
> At file scope no commit is available at all: the updater is a reader of the
> file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1
> record reject-file — the same treatment §6.3 gives an unknown incompat-lane
> bit. Compaction is barred on the same ground (`[R-WRT-06]`). |

**Quoted, §20.5:**

> A compactor MUST refuse to compact a file carrying any record
> whose type it does not implement with MU = 1: such a type can
> define references this specification does not (§7.2), so its
> bytes cannot be safely relocated.

**The readings.** The cell's final sentence turns on "the same ground". Two
readings are available:

(i) *the ground just stated* — the file-scope reject-file ground of the
immediately preceding sentence, whose own "the same treatment" a clause
earlier already anaphorises the file-scope case. On this reading the cell says
compaction is barred when the unimplemented MU = 1 record is **top-level**,
and says nothing about the layer-scope case it had just finished describing as
"leaving other layers editable".

(ii) *the ground of the whole row* — that the record's type is unimplemented
and MU = 1, regardless of scope.

**Which I picked, and why.** (ii), because `[R-WRT-06]` says "any record" and
the cell cites it. But (i) is the more natural reading of the English: the
sentence sits inside the file-scope sub-paragraph, immediately after two
consecutive anaphors ("the same treatment") that both point at the file-scope
case, and the layer-scope sentence three sentences earlier ends with an
explicit permission ("leaving other layers editable") that reading (i) leaves
undisturbed.

**What an implementer does wrong without it.** A conforming file may carry an
experimental-range MU = 1 record as a *layer sub-record*: §21.6 says so
expressly — "the same type as a layer sub-record is reject-layer and never a
ground to refuse the file (`[R-CNT-18]`)" — so only the top-level case is a
file a reader refuses. An updater reading §20.4's table alone, on reading (i),
concludes that such a file is compactable: no file-scope MU = 1 record is
present, so the bar it read does not apply, and the row's layer-scope sentence
told it that other layers stay editable. It compacts, relocating an extent
whose unimplemented type may carry references this specification does not
define — precisely what `[R-WRT-06]`'s stated ground says cannot be done
safely. A second implementer reading §20.5 refuses. Note also that the cell's
"the same ground" is factually wrong about `[R-WRT-06]`'s ground under either
reading: `[R-WRT-06]`'s ground is unsafe relocation of undeclared references,
not reject-file.

**Byte-level: no.** `[R-WRT-06]`'s "any record whose type it does not
implement with MU = 1" is unambiguous and the cell cites it, so a competent
implementation that follows the citation lands on the same answer; the
document does decide the question, in the section that owns the operation, and
§20.5 reinforces it elsewhere ("an MU = 1 type the compactor does not
implement never reaches this step (`[R-WRT-06]`)"). I record honestly that if
a reader stopped at the table the emittable set would move — a conforming
input, a compacted output only one reading permits an actor to produce — but
the discriminating question is whether the document leaves it open, and it
does not. What it costs is a table cell that points an updater author at a
narrower bar than the rule states, in the one table the updater class is most
likely to implement from.

---

### diagrams-02 — Appendix G item 5's "elsewhere it changes the stored bytes of every tile it touches" is false: a non-identity byte-shuffle is a permutation, and a legal decoded image can be its fixed point

**Location.** Appendix G, item 5 (lines 4415–4423), against §17.3,
`[R-COD-10]` (lines 2448–2461).

**Quoted, Appendix G item 5:**

> The filter is the identity
> exactly where its permutation is — where the stride is 1, as for a
> packed boolean plane, and equally where the decoded image is a
> single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes
> the stored bytes of every tile it touches.

**Quoted, `[R-COD-10]`:**

> Viewing the image as n = L/s consecutive groups
> of s bytes, the filtered image places byte i of group j at offset
> i · n + j — all first bytes in image order, then all second bytes,
> and so on; the inverse restores byte i · n + j to offset j · s + i.
> Length is unchanged.

**The readings.** "Changes the stored bytes of *every* tile it touches" is a
universal over the layer's stored tiles. `[R-COD-10]` defines the filter as a
permutation of byte *positions*; a permutation of positions changes the byte
string only when the string is not constant on some orbit it moves. The only
defensible reading of the sentence is the literal one — for every tile of a
filter-2 layer whose stride and group count both exceed 1, the stored bytes
differ from the decoded image — and that reading is false.

**The smallest legal counterexample I could build**, exactly as the brief's
degenerate-case shape asks. Interleaved layer (`[R-SER-06]` layout 1), rank 1,
dimension extent E₀ = 2, tile extent T₀ = 2 (so G₀ = 1, N = 1, P = 2 and there
are no padding positions, `[R-GEO-04]`); two `uint8` channels `a` and `b`
(§12.1, element size 1 each), fills `0x00`; codec 1; filter 2. Then
Q = ΣBᵢ = 2 and the decoded size is P·Q = 4 (§14.2). Take the tile whose two
samples are (a,b) = (0xAA, 0xBB) and (0xBB, 0xCC), so the decoded tile image
is `AA BB BB CC`. For an interleaved tile §17.3 fixes s = Q = 2, and
n = L/s = 4/2 = 2 — neither is 1, so by the sentence's own preceding clause
the filter is *not* the identity here. Applying `[R-COD-10]`: group 0 is
(AA, BB), group 1 is (BB, CC); byte i of group j goes to offset i·n + j =
2i + j, giving offset 0 ← AA, offset 1 ← BB, offset 2 ← BB, offset 3 ← CC.
The filtered image is `AA BB BB CC` — **byte-identical to the decoded image**.
The permutation at s = n = 2 transposes offsets 1 and 2 and fixes 0 and 3, so
every image whose bytes 1 and 2 agree is a fixed point. This tile is not
all-fill (its samples are not all `0x00`), so item 6's sentinel rule does not
remove it from the file, and nothing else in the profile or the specification
forbids it.

**What an implementer does wrong without it.** Nothing operational: item 5's
requirement — pin the filter value — is right, and the false clause is only
its justification. But the clause is the kind a reader relies on when
reasoning about whether a filter change is detectable, and §21.7 does reason
in exactly that register ("A change reaching the filter ... is witnessed on the
same terms T26 states for a wrong stride"). A reader who imports item 5's
universal into that reasoning will conclude that changing a filter declaration
always perturbs stored bytes, which it does not.

**Byte-level: no.** Appendix G is identified as non-normative ("Reproducible-
writer profile (non-normative)") and the sentence is a justification, not a
constraint; nothing an actor may emit turns on it. `[R-COD-10]`'s own
definition already decides what the filter does to any given image, and the
two never disagree about a byte — the appendix's claim is simply an
overstatement about how often that permutation is visible.

---

### diagrams-03 — Appendix G item 10's "a different length ... a different `inline_length`, and a different `dir_length`" is falsified by a name whose NFC form differs from it only by canonical reordering

**Location.** Appendix G, item 10 (lines 4454–4459), against §4.6's
`[R-ENC-13]` / `[R-ENC-14]` and its `température` Example (lines 560–580).

**Quoted, Appendix G item 10:**

> **Names normalized to Unicode Normalization Form C**, which
> `[R-ENC-14]` states as a SHOULD. A caller-supplied decomposed name
> is a different name under `[R-ENC-13]` and a different length —
> §4.6's `température` is 12 bytes in NFC and 13 in NFD — so a writer
> that does not normalize emits a different layer record, a different
> `inline_length`, and a different `dir_length`.

**Quoted, §4.6:**

> Name comparison is raw bytes: two names are the same name if and only if
> their encoded byte sequences are identical.

**The readings.** The item states three consequences of not normalizing a
"caller-supplied decomposed name": a different layer record, a different
`inline_length`, a different `dir_length`. The last two follow only from *a
different length*, which the item asserts as general and supports with one
example. Two readings of the length claim: (a) it is general over non-NFC
names; (b) it is scoped to the exhibited case. I picked (a) — the sentence's
grammar is "A caller-supplied decomposed name is ... a different length", with
the `température` clause offered as illustration ("— §4.6's `température`
is 12 bytes in NFC and 13 in NFD —"), and the conclusion "so a writer that
does not normalize emits ... a different `inline_length`" is drawn from the
general claim, not from the example.

Reading (a) is false. Normalization to NFC is *canonical reordering followed
by canonical composition*, and canonical reordering never changes byte length:
it permutes combining marks by combining class. Take the caller-supplied name
`a` + U+0301 COMBINING ACUTE ACCENT (ccc 230) + U+0327 COMBINING CEDILLA
(ccc 202), encoded `61 CC 81 CC A7` — five bytes, and not in NFC because the
marks are out of canonical order. Its NFC form reorders to `a` + U+0327 +
U+0301 = `61 CC A7 CC 81`, and no composition applies (Unicode has no
precomposed "a with cedilla"). Five bytes again, different bytes. A
normalizing writer and a non-normalizing writer therefore emit **different
layer records** — the item's first consequence, which is true and which
`[R-ENC-13]` makes decisive, since name identity is raw bytes — but the
**same `inline_length`** and the **same `dir_length`**. The same shape recurs
wherever reordering alone separates an input from its NFC form.

**What an implementer does wrong without it.** An adopter of the profile who
takes the length claim as general will build the wrong test for it: checking
that a non-normalizing writer's `inline_length` differs, and concluding from
an equal `inline_length` that normalization was performed. The item's actual
requirement — normalize — is unaffected; what fails is the account of why
byte-identity is at stake, and that account is what tells an adopter what to
verify.

**Byte-level: no.** Appendix G is non-normative and this item adds a
requirement to the profile only, not to any conformance class; §4.6's
`[R-ENC-13]` already decides name identity by raw bytes, under which both the
reordered form and its NFC form are conforming names and the file carrying
either is conforming. Nothing about what a conforming writer may emit turns on
the length claim.

---

### diagrams-04 — §21.6's sentinel row restates `[R-TYP-08]` without either of its two qualifications, and as written it would have a reader return padding positions that `[R-GEO-04]` forbids returning

**Location.** §21.6, first row of the "Conditions that are not violations"
table (line 3671), against `[R-TYP-08]` (§13.3, lines 1819–1827) and
`[R-GEO-04]` (§11.3, lines 1599–1607).

**Quoted, §21.6:**

> | An index entry is the sentinel | The tile is addressed but not stored;
> every sample position it carries reads as the channel's fill |
> `[R-IDX-02]`, `[R-TYP-08]` |

**Quoted, `[R-TYP-08]`:**

> For every addressed tile that is not stored in the live generation —
> its index entry is the sentinel (§15.2) — a reader that returns any
> of the tile's sample positions inside the layer's extents MUST
> return, for each channel the tile carries, that channel's fill value
> at every such position.

**Quoted, `[R-GEO-04]`:**

> Padding
> positions are serialized like any other
> position (byte-level rules and padding content: §14) but are not part
> of the reference array (§3.2); a reader MUST NOT return padding
> positions as samples.

**The readings.** `[R-TYP-08]` is qualified twice: the obligation runs over
"sample positions **inside the layer's extents**", and it delivers "for **each
channel** the tile carries" that channel's fill. The §21.6 cell drops both:
"every sample position it carries" and "the channel's fill", singular.

Reading (a): the cell means what `[R-TYP-08]` means and its brevity is
harmless. Reading (b): the cell means what it says — an unstored *edge* tile's
padding positions also read as fill and are returned, and an interleaved
unstored tile delivers one channel's fill.

I picked (a), because §21.1 states the precedence: "each row *restates* its
governing rule, and where a row and the rule it cites diverge, **the rule
governs**", and closes the same paragraph by extending that to §21.6's
entries — "§21.6's entries restate their governing rules on the same terms a
row does, and where such an entry and the rule it cites diverge, the rule
governs there too". But reading (b) is what the cell says, and it is
inconsistent with two separate MUSTs. On the extents half it contradicts
`[R-GEO-04]`'s "a reader MUST NOT return padding positions as samples" and
§3.2's `[R-MDL-01]` ("Sample positions that exist only as edge-tile padding
(§11.3) have coordinates outside the layer's extents and are not part of the
reference array"). On the channels half it contradicts `[R-TYP-08]`'s own next
sentence — "In an interleaved layer an unstored tile yields the full fill
sample — each channel's fill, in declared channel order — at every position."

**Smallest case that separates them.** A layer with extents (5,5) and tile
extents (4,4) — the very geometry §14.5's Example uses — has an edge tile at
tile coordinates (1,1) carrying one real position and fifteen padding
positions. If that tile's index entry is the sentinel, the §21.6 cell says all
sixteen "read as fill"; `[R-TYP-08]` says only the one inside the extents does,
and `[R-GEO-04]` forbids returning the other fifteen at all. Make the layer
interleaved with §13.3's `r`,`g`,`b` and the cell's singular "the channel's
fill" also fails, the tile carrying three.

**What an implementer does wrong without it.** A reader built from §21.6 —
which is the table an implementer consults for "what do I do when I meet a
sentinel" — returns padding positions as fill samples, so a region read that
covers an edge tile returns more samples than the reference array contains.
That is precisely the failure §11.3 and §3.2 were written to close, and it is
a defect of the class my charter names: a table cell a reader could take
further than the section licenses.

**Byte-level: no.** §21.1 states the precedence explicitly and in advance —
where a §21.6 entry and the rule it cites diverge, the rule governs — so both
the extents qualification and the per-channel qualification are already
decided against the cell, and no verifier verdict or emittable byte sequence
is open. This is the pattern the brief names as the dominant cause of
over-claiming, and I grade it accordingly: only the table is wrong.

---

## 5. What I could not determine

- Whether §2.2's prefix table preserves the content of the list it replaced.
  I can only check it against the rest of the document, which it survives; the
  prior text is outside my access.
- Whether §4.7's Note's promise that "every sentinel or overloaded encoding
  additionally has a paired conformance vector" holds, since the corpus is
  outside my access. `[R-VEC-03]` promises vectors for "every sentinel, every
  boundary value, and every hard limit of `[R-ERR-05]`", which does not name
  overloaded encodings such as the extent slot (0,0) or A = 0 in as many
  words; whether "boundary value" covers them is a judgement I did not have
  enough to settle, and it is a corpus obligation rather than a figure defect.
- Whether the register's completeness clause is discharged for a small set of
  writer obligations that §21.7's second paragraph does not name individually
  — `[R-LIF-02]`'s step ordering and barriers, `[R-LIF-04]`'s truncate-or-
  overwrite, `[R-WRT-05]`'s byte-identical re-emission. Each is a property of
  a file's history, and §21.7 does give "properties of a file's history, which
  §9.7 does not reconstruct" as the class, attaching it to `[R-LIF-01]` and
  `[R-LIF-03]` by name; §9.5's Note separately accounts for `[R-LIF-04]`'s
  observable residue. I concluded the class covers them and did not file it,
  but I record the reasoning because the paragraph reads as an enumeration
  rather than a class, and a stricter reader could take it the other way.

## 6. Finding count

This transcript contains **4** findings: diagrams-01 through diagrams-04.
