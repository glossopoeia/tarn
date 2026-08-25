# Round 26 — Diagram auditor — working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,484 lines; the brief said 4,485 — off by one, immaterial). It was where the
brief said it would be. I read it end to end in six `Read` calls, and ran
`grep -n` against that same file three times (for `stored-tile set|index
content|re-emits…`, for `local reader|resident|front-block`, and once while
locating table rows). I ran two Python scripts I wrote myself in the scratchpad
(`crc.py`, `crc2.py`); neither reads any file — the first hard-codes the byte
strings I needed CRCs over, the second hard-codes Appendix A's hex dump as a
string literal transcribed from what I had already read. No ADRs, no
`conformance/`, no `registry.json`, no `PLAN.md`, no `AGENTS.md`, no git, no
web.

Context I did not ask for: my runtime placed a project-instruction pointer
(`CLAUDE.md` → `AGENTS.md`) and an *index* of the maintainer's auto-memory in
my context before I began — a list of memory-file titles with one-line
descriptions, several of which name TARN-specific working practice and one of
which names a spec-editing hazard. I did not open any of those files and I have
not used their contents to reach or to settle any conclusion here. I am naming
their appearance, not repeating them.

Everything below is derived from the specification text alone.

---

## 1. Enumeration of figures, diagrams, layout boxes, tables, examples, checklists

I enumerated before judging. Line numbers are from the file as read.

### Normative layout tables (fixed structures)
| # | Lines | What |
|---|---|---|
| N1 | 697–701 | §6.1 front signature block — Offset / Size / Value / Class |
| N2 | 740–752 | §6.2 trailer layout — Offset / Size / Type / Field / Class / Valid values |
| N3 | 904–910 | §7.2 record framing header — Offset / Size / Type / Field / Class |
| N4 | 977–981 | §7.3 record types of format major 1 |
| N5 | 1006–1023 | §7.4 layer record inline payload — Field / Type / Constraint |
| N6 | 1123–1131 | §8.1 checksum coverage map |
| N7 | 1398–1407 | §10.2 numeric identifier spaces |
| N8 | 1607–1621 | §12.1 core sample types |
| N9 | 1839–1842 | §14.2 decoded size / offset-of-value-k |
| N10 | 2002–2003 | §15.1 index-region layout box (blockquote) |
| N11 | 2007–2011 | §15.1 index entry layout |
| N12 | 2055–2067 | §15.3 entry-validity classification table |
| N13 | 2450–2452 | §18.2 user-metadata inline payload |
| N14 | 2640–2647 | §18.4 standardized keys |
| N15 | 235–241 | §2.4 outcome-class table |
| N16 | 3176–3180 | §20.4 updater preservation table |
| N17 | 3746–3755 | §21.9 minimum-guarantee limits table |

### Register tables (restate rules stated in prose)
| # | Lines | What |
|---|---|---|
| R-F | 3438–3475 | §21.2, F1–F36 |
| R-L | 3482–3532 | §21.3, L1–L49 |
| R-T | 3539–3566 | §21.4, T1–T26 |
| R-R | 3589–3600 | §21.5, R1–R10 |
| R-N | 3607–3622 | §21.6 conditions that are not violations |

### ASCII figures
| # | Lines | What |
|---|---|---|
| A1 | 587–592 | §5.1 file after three commits |
| A2 | 1202–1211 | §9.2 what a crash sees |
| A3 | 3107–3111 | §20.3 shape (a) new layer |
| A4 | 3123–3127 | §20.3 shape (b) tiles added |
| A5 | 3147–3150 | §20.3 shape (c) directory-only change |
| A6 | 3299–3305 | §20.5 what compaction reclaims |
| A7 | 4105–4114 | Appendix A hex dump |

### Worked examples / numeric boxes
| # | Lines | What |
|---|---|---|
| E1 | 442–446 | §4.5 CRC check vector |
| E2 | 513–517 | §4.6 `température` NFC/NFD |
| E3 | 577–582 | §5.1 smallest conforming file |
| E4 | 1060–1099 | §7.4 complete layer-record payload (hex box + arithmetic) |
| E5 | 1524–1528 | §11.2 grid arithmetic |
| E6 | 1578–1584 | §11.4 ordinals |
| E7 | 1641–1644 | §12.1 bfloat16 |
| E8 | 1690–1695 | §12.3 channel entry bytes |
| E9 | 1760–1765 | §13.3 rgb fill |
| E10 | 1881–1891 | §14.2 interleaved / planar offsets |
| E11 | 1915–1920 | §14.3 packed bool tile |
| E12 | 1971–1976 | §14.5 padding content |
| E13 | 2095–2108 | §15.4 entry_count = 1,000,000 |
| E14 | 2110–2114 | §15.4 planar disk ordinals |
| E15 | 2210–2217 | §16.2 slab runs |
| E16 | 2393–2396 | §17.3 byte-shuffle |
| E17 | 3093–3100 | §20.3 supersede cost |
| E18 | 4116–4132 | Appendix A annotation table |

### Appendix material and checklists
| # | Lines | What |
|---|---|---|
| X1 | 4147–4180 | Appendix B constants |
| X2 | 4182–4207 | Appendix C registry snapshot |
| X3 | 4209–4245 | Appendix D six design choices |
| X4 | 4247–4256 | Appendix E changelog |
| X5 | 4258–4271 | Appendix F references |
| X6 | 4273–4411 | Appendix G reproducible-writer profile, items 1–10 |
| X7 | 4413–4484 | Appendix H conformance checklists, five classes |

### Numbered lists checked for order / duplication / gaps
§9.2 commit protocol 1–6; §10.1 vehicles 1–4; §18.2 four document restrictions;
§19.1 open 1–4; §19.4 tile read 1–8; §20.3 append 1–6; Appendix G 1–10.
All present, in order, no duplicates, no gaps. Cross-references to step numbers
(§5.1 "steps 3 and 5"; §6.2 "step 5"; §20.2 "steps 4–6 — both barriers";
§20.3 steps citing "steps 1–2", "step 3", "steps 4–6") all resolve correctly.

---

## 2. Arithmetic and byte-level checks I actually performed

### 2.1 Checksum constants (computed, not eyeballed)

I implemented CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41, reflected
in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) as the reflected table
polynomial 0x82F63B78, and checked it against §4.5's own check vector before
trusting it:

```
CRC32C("123456789")            = 0xE3069283   stored 83 92 06 E3   § 4.5  ✓
CRC32C(zero bytes)             = 0x00000000                        § 4.5  ✓
CRC32C(4 sentinel entries, 80B)= 0x80A34955   stored 55 49 A3 80   § 7.4  ✓
CRC32C(55 49 A3 80)            = 0xC4EE982E   stored 2E 98 EE C4   § 7.4  ✓
CRC32C(2^16 sentinel entries)  = 0xEECB3BB2                        §15.4  ✓
```

Every constant in the document reproduces. The sentinel entry I used was
`FF ×16 00 ×4` per §15.2, which is also what Appendix B's constants table gives.

### 2.2 Appendix A, byte by byte (A7 + E18)

I transcribed the hex dump and decoded it as a structure:

```
len = 128                        multiple of 64                    ✓ §6.2
[0,8)   89 54 41 52 4E 0D 0A 1A  = \x89 "TARN" CR LF ctrl-Z        ✓ §6.1
[8,16)  zero                                                       ✓ §6.1
[16,20) 00 00 00 00              = CRC32C of zero bytes            ✓ §7.1
[20,64) zero                     44 bytes of pad  (64-20 = 44)     ✓ E3
[64,72) 8A 4E 52 41 54 0D 0A 1A  = \x8A "NRAT" CR LF ctrl-Z        ✓ §6.2
version_major = 1, version_minor = 0, flags = 0
generation = 1, dir_offset = 16, dir_length = 4
committed_file_length = 128 = physical size
file_id = 0x0123456789ABCDEF (stored EF CD AB 89 67 45 23 01)      ✓ LE
reserved [120,124) = 00 00 00 00
computed CRC32C(trailer[0,60)) = 0xE00938D2, stored D2 38 09 E0    ✓
```

Field offsets in the annotation table (E18) map onto the trailer table (N2)
exactly: 64+0, 64+8, 64+10, 64+12, 64+16, 64+24, 64+32, 64+40, 64+48, 64+56,
64+60 → [64,72) [72,74) [74,76) [76,80) [80,88) [88,96) [96,104) [104,112)
[112,120) [120,124) [124,128). All eleven rows correct.

Minimum-size derivation independently: dir_offset ≥ 16, dir_length ≥ 4 →
directory ends ≥ 20; dir_offset+dir_length ≤ F−64 → F ≥ 84; F ≡ 0 (mod 64)
→ F ≥ 128. §5.1's `[R-CNT-27]`, E3, Appendix B and F5 all agree.

The narrative that follows the dump: two requests, the second being [16,20) —
that is exactly [dir_offset, dir_offset+dir_length) per §6.4 ✓. "112 bytes
covering [16, 128)" = 128−16 ✓. See §4.1 below for the one problem I found in
this narrative.

### 2.3 §7.4's layer-record hex box (E4)

Re-derived the offsets from the field order in N5 rather than reading them off
the box:

```
 0 name          1 + 3          → 4      03 73 73 74   "sst"       ✓
 4 layout        1              → 5
 5 linearization 2              → 7
 7 codec         2              → 9
 9 filter        2              → 11
11 A             8              → 19
19 S             8              → 27
27 A_slab        8              → 35
35 rank d        1              → 36
36 C             2              → 38
38 dim name      1 + 1          → 40      01 78   "x"              ✓
40 extent        8              → 48      100 = 64 00 …            ✓
48 tile extent   8              → 56      32  = 20 00 …            ✓
56 chan name+typ 1 + 4 + 2      → 63      04 "temp" 0C 00          ✓
63 fill          1 + 4          → 68      04 00 00 C0 7F           ✓
68 index_enc     1              → 69
69 entry_count   8              → 77      4                        ✓
77 crc_of_crc    4              → 81
```
81 bytes, matching the stated `inline_length = 81`, and every offset label in
the box is right. The prose summary checks too: name 4 + "nine scalars from
layout through channel count" 1+2+2+2+8+8+8+1+2 = 34 (and there are exactly
nine of them), dimension entry 18, channel entry 12, trailing fixed fields
1+8+4 = 13 → 4+34+18+12+13 = 81.

Grid: ⌈100/32⌉ = 4 → entry_count 4 ✓ (interleaved, C = 1, so N).
Index region: 4·20 + ⌈4/2¹⁶⌉·4 = 84, matching the quoted extent length and
`[R-CNT-17]`'s formula ✓. Segment CRC and crc_of_crc_array computed above ✓.
Channel-entry bytes are byte-identical to §12.3's example (E8) as claimed ✓.

### 2.4 Geometry / ordinal examples

* E5: (1024,2048)/(256,256) → G = (4,8), N = 32, P = 65,536 ✓. (1000,2048):
  ⌈1000/256⌉ = 4 ✓.
* E6: s(0,0)=0, s(0,1)=1, s(1,0)=8 under s = Σ tᵢ·∏_{j>i}Gⱼ with G=(4,8) ✓.
  (300,700) → t = (1,2), s = 10; u = (44,188), in-tile ordinal 44·256+188 =
  11,452 ✓. Planar C=4, c=2: 2·32+10 = 74 ✓.
* E14: entry 74 at region bytes [1480,1500) = [20·74, 20·75) ✓; channel 3's
  block is [96,128) → 32 entries, ordinals 96–127 ✓.
* E13: ⌈1,000,000/65,536⌉ = 16 segments; 15 full = 983,040 entries; last
  covers 16,960 ✓. CRC array 64 bytes ✓. Region 20,000,064 ✓. k = 999,999 is
  segment 15 at segment-relative byte 20·16,959 = 339,180 ✓. CRC array at
  [20,000,000, 20,000,064) ✓, segment 15 at [19,660,800, 20,000,000) ✓,
  339,200 bytes ≈ 339 KB ✓. Full segment 65,536·20 = 1,310,720 = 1.25 MiB ✓.
  entry_count = 0 → zero segments, zero-byte array, slot (0,0),
  crc_of_crc_array = 0 ✓ against N5 and `[R-CNT-17]`.
* E10: (2,3) P=6, uint8+uint16 → Q=3, size 18; ordinal (1,2) = 1·3+2 = 5;
  bytes [15,18); planar b tile 12 bytes, ordinal 5 at 10–11 ✓. float32+bool
  → Q=5, size 30, sample at [25,30), t 25–28, m 29 ✓. Closing identity
  u·Q+Fᶜ = the table's form with k = u·C+c: k div C = u, k mod C = c ✓.
* E11: (2,5) P=10 alternating from true → bits 0,2,4,6 of byte 0 = 0x55 ✓;
  values 8,9 = true,false → byte 1 = 0x01 ✓; ⌈10/8⌉ = 2 bytes ✓; fill true →
  pad bits 2–7 set → 0x01|0xFC = 0xFD ✓.
* E12: (5,5)/(4,4) → grid 2×2; tile (1,1) covers 4–7 both axes; only (4,4) is
  inside extents → 1 real, 15 padding ✓; P·B = 16·2 = 32 bytes ✓; in-tile
  ordinal 0 is (0,0) → global (4,4), so "value 0 is the stored sample" ✓;
  0xABCD little-endian = `CD AB` ✓.
* E15: N=32, S=8 → ⌈32/8⌉ = 4 runs [0,8) [8,16) [16,24) [24,32) ✓; row-major
  with G_x = 8 makes each run one tile row ✓; tile rows 1–2 = ordinals 8–23 =
  runs 1 and 2 ✓; sentinel at ordinal 10 transparent ✓ against `[R-SLB-03]`.
* E16: 1.0,2.0,3.0 float32 = `00 00 80 3F | 00 00 00 40 | 00 00 40 40`, s=4,
  n=3, byte i of group j → offset i·n+j. I laid all twelve output positions
  out by hand: `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` — byte-identical to
  the example, and matching its prose gloss ✓.
* E17: 32·20 + ⌈32/2¹⁶⌉·4 = 644 ✓; "one entry re-pointed, 31 byte-identical" ✓.
* E2: "température" NFC = 11 code points, é 2 bytes → 12 bytes, matching the
  quoted `74 65 6D 70 C3 A9 72 61 74 75 72 65` ✓; NFD é = `65 CC 81` → 13 ✓.
* E7: binary32 1.0 = 0x3F800000, high half 0x3F80, stored `80 3F` ✓;
  0x7FC0 ↔ 0x7FC00000 quiet NaN ✓.
* E9: fills 0xFF/0x00/0x00 → (255,0,0) ✓; planar mixed case ✓ against
  `[R-TYP-08]` and §3.2.

### 2.5 Register instance arithmetic (§21.8's "121 conditions over 277 instances")

§21.1 makes this mechanical: semicolon-separated items per cell, a `—` cell is
one instance. I counted every cell.

* §21.2 F1–F36 = 36 rows. Instance counts:
  2,6,2,1,2,2,4,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,2,1,1,5,1,1,1
  → **58**
* §21.3 L1–L49 = 49 rows:
  8,9,1,2,1,1,2,2,2,1,1,2,1,3,4,2,2,3,1,1,4,4,4,1,1,1,1,1,3,2,3,3,4,4,1,2,
  1,1,3,1,3,1,3,3,3,2,2,1,4 → **116**
* §21.4 T1–T26 = 26 rows:
  1,1,6,4,1,1,2,1,1,1,2,1,2,6,2,1,1,2,1,1,3,6,1,1,3,3 → **55**
* §21.5 R1–R10 = 10 rows: 4,2,2,16,8,4,6,2,2,2 → **48**

36+49+26+10 = **121** ✓ and 58+116+55+48 = **277** ✓. Both figures in §21.8
are exactly right. I spot-re-counted the long cells (R4's sixteen, L2's nine,
L1's eight, R5's eight, T3/T14/T22's six each) by counting semicolons.

I also checked the instance *rules* against the cells that apply them:
§21.1 says a comparison whose text bounds one direction gets one instance and a
*differs from / does not equal* gets two, and that layout-varying formulas are
enumerated. T21 ("larger than") = 3 layouts × 1 = 3 ✓; T22 ("does not equal")
= 3 × 2 = 6 ✓; T3, T14 = 6 ✓; L44 ("exceeds") = 3 ✓; L21, L22, L30 ✓. A
nonzero test gets no direction: L28's `A_slab ≠ 0` is one instance ✓.

### 2.6 Closed counts and lists promised complete

Each of these I derived independently from the rule the list is about, then
compared:

* §15.3 "Six rows are marked *structural*" — I count six `*structural*` cells ✓.
  Those six map onto register rows T6, T7, T8, T9, T10, T11, T12 (the sixth
  table row carries two alternatives, split into T9 and T12) ✓.
* §21.2 "36 conditions" ✓, §21.3 "49" ✓, §21.4 "26" ✓, §21.5 "10" ✓.
* §21.2 "Four rows are outside that reasoning" — F8, F1, F14, F6 = four ✓, and
  the only other row keyed to a field `[R-CNT-24]` fixes across majors is F18,
  which the paragraph explicitly excepts on a different ground ✓.
* §10.2's eight spaces, each cross-checked against its defining section
  (§7.3, §14.1, §11.4, §12.2, §17.2, §17.3, §15.1/§7.4, §18.2) — all eight
  assigned/reserved/experimental partitions agree ✓.
* §20.5's "one row for each of the other seven spaces §10.2 tabulates (L31,
  L33, L34, L36, L43, L45, R1)" — index encoding, linearization, sample type,
  channel layout, codec, filter, metadata encoding = seven, and the seven rows
  named are exactly the rows for those seven ✓.
* §12.1 "exactly thirteen sample types" ✓ (13 rows; 12 numeric + bool ✓).
* §10.1 four vehicles vs §4.3's four ✓ (same four, same order-independent set).
* §17.2 "Three frame features are excluded" — dictionary/dictionary ID,
  content-checksum flag, window size — three ✓.
* §18.2 "Four restrictions apply" — four bullets delivered ✓ (the fourth
  bundles UTF-8 well-formedness with the key name rules, which is why it maps
  to three register rows, R5/R6/R10; the count of *bullets* is still four).
* §22.2 "Three properties" ✓; §22.3 "Four residues" ✓; §21.7 "§20.5's four
  obligations" ✓ (fresh file_id draw, generation 1, ignore-lane carry-forward,
  version_minor floor — all four present in `[R-WRT-06]`).
* §21.9 `[R-ERR-05]` "Two do not [follow from a width, an external format, or
  the value domain]" — I worked each hard limit: 255-byte names (u8 prefix),
  rank 255 / C 65,535 (field widths), 0x7E000000 (external), 2⁶³−1 (domain),
  A ≤ 2⁶² and A_slab ≤ 2⁶² (largest power of two inside the domain), S range
  (domain), dir ≥ 4 at ≥ 16 and the 128-byte floor (arithmetic over the
  trailer/front block). The residue is exactly the 512 floor on A and the
  255-byte key cap — two ✓.
* §2.3's closed set of "writer obligation ... expressly declared not to be a
  file-conformance violation": §6.3's flags = 0 and §6.2's over-long
  pre-trailer gap. I looked for a third and found only §10.3 and §18.3, both
  of which §2.3 has already named in the preceding clause ✓.
* Appendix D "Six choices" ✓; §2.3 "five classes" ✓; §2.4 four reader
  outcomes ✓.
* Appendix H's verifier checklist against every register row whose Detector is
  *verifier* — F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46,
  L47, L48, L49, T2, T4, T5, T26. Every one of the twenty is reachable through
  a checklist line ✓ (T26 through the decoded-content line, as T26's own cell
  says its detecting check is T2's or T4's).

### 2.7 Register completeness sweep

Because §21.1 makes the register's completeness normative, I walked every
requirement identifier that names a detectable file-level condition and looked
for its row. §6.2's twelve gates → F8–F19 with F2 for the generation ceiling;
`[R-CNT-13]`'s five slot conditions → F30/F31/F32/F3/F33 and L15/L16/L17/L2/L18;
`[R-CNT-23]`'s whole table → L1, L3–L9, L21, L22, L27–L36, L39, L43, L45;
`[R-IDX-03]`'s eleven rows → T6–T12 plus L18/L40/L41/L42; §18.2's four document
restrictions → R5–R10; the frame constraints → R4; `[R-COD-03]`–`[R-COD-10]`
→ L43/L44/L45 and T13–T26. I found no detectable condition without a row.
Conditions the document says have no witness are all accounted for in §21.7,
and the two that carry no row of their own but are witnessed by others —
`[R-SLB-04]`'s stale declaration and `[R-CNT-18]`'s nesting prohibition — each
carry an explanatory Note saying so.

### 2.8 ASCII figures, region by region

* A1: front | A | ▓ | B | ▓ | dir₃ | pad | trail₃. Commit 1 wrote A then
  dir₁/pad/tr₁; commit 2 appended B then dir₂/pad/tr₂; commit 3 touched no
  layer. The two ▓ runs are therefore exactly the two superseded
  directory/pad/trailer triples, in the positions drawn ✓. The caption's
  "a commit that touches no layer re-emits the directory, the pad and the
  trailer alone" is consistent with §9.2 (steps 2's payload set may be empty)
  and with `[R-LIF-03]`'s "increasing by exactly 1 per commit" ✓.
* A2: row 2's ▓ is the interrupted tail, trailₙ intact but no longer terminal —
  which is precisely the state `[R-LIF-05]` forbids scanning backward from ✓.
  Row 3's ▓ is dirₙ/pad/trailₙ ✓.
* A3/A4/A5: each shows only appends past F and no rewritten committed byte ✓,
  and the ▓ runs are what the accompanying prose says they are ✓.
* A6: input's five ▓ runs, output with none but its own pad; the pad is drawn
  and named, so the figure does not claim a slack-free output ✓. Placement
  differs from Appendix G item 3's total order, which is fine — item 3 is an
  opt-in profile and §20.5 leaves a compactor's placement free
  (`[R-SLB-05]`, "preserves no placement").

### 2.9 Degenerate files I built on paper and asked the tables about

* **Zero-addressed-tile layer** (some Eᵢ = 0, planar, C = 3): entry_count =
  C·N = 0; N5's crc_of_crc_array must be 0; `[R-CNT-17]` forces extent
  (0,0)/length 0; §21.9's "decoded size of one tile" row bounds nothing
  (§21.9 says so explicitly); `[R-COD-07]`'s lz4 cap is escaped (§17.2's Note
  says so, and I verified N = ∏Gᵢ = 0 ⟺ some Eᵢ = 0, so "takes every
  dimension's extent nonzero" is exactly right); `[R-SLB-02]`'s blocks are
  [0,0) so a declared S is vacuous but conforming. Every table answers.
* **Zero-layer file carrying one top-level user-metadata record**: I worked the
  placement — the extent cannot sit between the directory's end and the
  trailer (`[R-CNT-05]`/F7), so it must precede the directory; dir_offset then
  exceeds 16 and F = 128 still works. Conforming. §21.6's row for this
  condition is the one place a table describes it, and see §4.5 below.
* **Layer with padding positions in tiles it does not store**: relevant to
  §20.3's shape (c); I record the reasoning in §4.6 below and concluded it is
  not a defect.

---

## 3. Things I checked that turned out clean (recorded so coverage is checkable)

* §8.1's map against §4.5's prose: the three terminal checksum fields named in
  §4.5 (trailer, directory-region, user-metadata) are exactly the three rows of
  the map whose checksum covers bytes short of itself; the three interior
  fields §4.5 names (segment CRC array, entry crc, crc_of_crc_array) are each
  both compared and covered once — segment array by crc_of_crc_array, entry crc
  by its segment CRC, crc_of_crc_array by the directory CRC. Every byte of a
  tile-index region is covered by exactly one checksum. No gap, no double
  cover.
* §8.2's chain of trust against §15.4's two-verification rule and against the
  outcome each link takes (F14/F20, L37/L38, T1, R2).
* §6.3's `[R-CNT-24]` arithmetic: 64 − 8 magic − 4 major/minor − 4 CRC = 48
  redefinable bytes, and N2 assigns all 64, so "zero slack" holds.
* Appendix B against every constant I could find defined in the body. Every
  entry resolves to its cited section and carries the right value. I looked for
  named constants missing from it and found only range boundaries (0x8000,
  0x7F, …), which Appendix C and §10.2 carry instead.
* Appendix C against §7.3, §12.1, §12.2's pinned reservations, §17.2, §17.3,
  §14.1, §11.4, §15.1, §18.2, §6.3, §18.4. All agree.
* Appendix F against every external format cited normatively. RFC 1950 and
  1952 appear in §17.2 and in T15's instances but only to name what is
  excluded, and detection of T15 is routed to T24/T25, so their absence from
  Appendix F costs an implementer nothing.
* External-format details in the register: gzip `1F 8B` + trailing CRC32/ISIZE;
  zlib CMF/FLG + Adler-32; zstd magic `28 B5 2F FD` (0xFD2FB528 LE); LZ4 frame
  magic `04 22 4D 18` (0x184D2204 LE); LZ4 match offset 0 invalid; DEFLATE
  BTYPE 3 invalid. All correct.
* §21.9's Note arithmetic: 2³² entries → 2¹⁶ segments → 256 KiB array; 2³⁶ →
  4 MiB ✓. 65,536 layers × ~200 B ≈ 12.5 MiB ✓.
* §21.6's thirteen rows against their governing rules; §21.6's two "conforming
  files a reader nevertheless refuses" against `[R-CNT-07]`, `[R-CNT-15]`,
  `[R-CNF-02]` and `[R-CNT-18]`.
* §19.1/§19.2/§19.3/§19.4's step lists against the register's Detector and
  Detected columns. §19's preamble explicitly disclaims exhaustiveness for
  these lists ("Those enumerations are not the complete inventory … §21's
  register is"), so their being partial is licensed rather than defective.
* §20.4's table's three flag rows against §2.4's preserve-verbatim row (which
  names exactly the MU = 1 and MU = 0 / PE = 1 rows) ✓, and against
  `[R-WRT-06]`'s compaction refusal ✓.
* §14.2's table's scope: it deliberately omits packed planar bool, which §14.3
  governs, and §14.3 supplies both the size and the bit position. Not a gap.
* §16.2's transparency carve-out against §15.3's "contributes no stored extent
  to the *verifier* rows" and against L40/L41/L42. L41 restates the carve-out,
  L40 does not, but L40's governing-rule cell cites `[R-IDX-03]`, where the
  carve-out lives, and §21.1 makes the rule govern. Not a defect.
* §21.1's specialization triage rule. I found further strict specializations
  it does not name (T12 ⊂ T9, since offset+length > 2⁶³−1 ≥ F implies
  > F−64; T14 ⊂ T3 under codec 1; F3 ⊂ F10/F32). I decided **not** to report
  this: the sentence's own word is "Some", the triage rule it states is
  general, and §24 `[R-VEC-02]` already tells a corpus builder what to do when
  a condition cannot be isolated. Listing it would be padding.
* §4.7's Note on presentation columns against N1/N2/N3/N5/N11/N13. §7.4's
  table (N5) omits a Size column as well as the offset and class columns the
  Note names, but the Note's own hedge — "each table giving the columns its
  structure needs" — licenses that, and the Type cell carries the width for
  every fixed field while the two variable-length fields have no fixed size to
  give. Not reported.
* Appendix G item 2's file_id derivation for circularity: the hash input is
  [0, F−64) followed by trailer[0,60) with file_id zeroed, and every other
  trailer field is fixed before file_id, so there is none.
* Appendix G item 3's ordering key for totality and self-reference: masking
  extent_offset is what breaks the self-reference, and the remaining key
  components are content ✓.

---

## 4. Findings

### 4.1 diagrams-01 — Appendix A keys `[R-CNT-04]`'s front-block obligation to *locality*, where §6.1 keys it to *residency* and says so on purpose

**Location.** Appendix A (line 4136), against §6.1 `[R-CNT-04]`, §19.1 step 1,
§19.2, §21.2 rows F1 and F6, and Appendix H's verifier checklist.

**Quotation (Appendix A).**

> "A remote reader opens this file in §6.4's two requests: the final 64
> bytes, validated per §6.2; then [16, 20), whose CRC it verifies. A
> local reader additionally verifies bytes [0, 16) by equality first,
> which `[R-CNT-04]` requires of any reader holding them"

**The rule it illustrates (§6.1).**

> "A **local reader** is one whose transport serves any byte range at no
> per-range round trip … That distinction governs the request accounting of
> §6.4 and nothing else; the obligation over the front block turns on
> residency instead, because a transport can be classified either way at the
> margin while residency is decidable at any reader's own open path.
>
> A reader whose open leaves bytes [0, 16) **resident** … MUST verify the
> full block by byte equality before other processing … A reader that would
> have to issue a further range request to obtain those bytes MAY defer or
> omit the check … The test is residency, not transport".

**Why this is a defect.** §6.1 goes out of its way to say that locality is *not*
the test, and every other restatement in the document obeys that: §19.1 step 1
("A reader whose open leaves bytes [0, 16) resident"), §19.2 ("for a reader whose
open leaves it resident"), F1 ("binds only a reader holding bytes [0, 16)
resident"), F6 ("the obligation binds a reader holding those bytes resident"),
Appendix H ("lets a reader not holding it resident defer or omit"). I grepped the
document for every occurrence of "local reader" and "resident"; line 4136 is the
single place where the obligation is stated over the local/remote axis.

A local reader is not necessarily a resident-holding one. Nothing obliges a local
reader to read the whole file: it may `pread` the final 64 bytes and then
[16, 20), exactly as the remote reader in the same paragraph does, and never hold
[0, 16). Such a reader is inside `[R-CNT-04]`'s exemption — it "would have to
issue a further range request", which for a local transport merely costs no round
trip — yet Appendix A's main clause says a local reader verifies the block first.
The illustration is therefore **wider than the rule**: it obliges a class §6.1
does not.

**Which reading I picked, and why.** The subordinate clause ("which `[R-CNT-04]`
requires of any reader holding them") states the correct test, so a careful
reader recovers it; and the sentence that follows in Appendix A gets residency
exactly right for the remote case ("bytes [0, 16) stay non-resident, so §6.1
leaves the front-block check to the reader"). I read the passage as intending the
resident case and reaching for "local" as shorthand — which is the shorthand §6.1
explicitly disclaims. The repair is to say "a reader that holds bytes [0, 16)"
rather than "a local reader".

**Byte-level: no.** Appendix A is labelled non-normative, and the over-stated
obligation is a *verification* duty, not an emission rule. Two readers built from
the two readings disagree only about whether a local tail-reading reader must
also fetch and compare [0, 16); and a file that fails that comparison is
nonconforming anyway (F6), so `[R-CNF-12]` already licenses either verdict on it.
No conforming file's accept/reject verdict changes, and no emittable byte does.
What it costs an implementer is a false conformance claim in either direction: a
local reader that omits the check may be told it is nonconforming when it is not.

---

### 4.2 diagrams-02 — §20.3's cost Note states the re-emission rule by the stored-tile set, then instances it with an operation that leaves the stored-tile set unchanged

**Location.** §20.3, the Note at line 3085–3091, against §20.3 step 4
(`[R-WRT-04]`), §5.1's Example, and §3.1's definition of *stored*.

**Quotation (§20.3 Note).**

> "**Note.** A commit's cost is dominated by its index, not its data:
> any change to a layer's stored-tile set re-emits that layer's whole
> tile-index region, so editing one sample of a 10⁶-tile layer appends
> about 20 MB of index and leaves as much slack."

**The rule (§20.3 step 4, `[R-WRT-04]`).**

> "Every layer whose stored-tile set or index content this commit changes
> has its tile-index region re-emitted in full"

**And §5.1's Example, which states it in full:**

> "A commit that changes a layer's stored-tile set or index content
> re-emits that layer's whole tile-index region as well, at a new
> placement (§20.3, `[R-WRT-04]`)."

**Why this is a defect.** §3.1 fixes *stored* precisely: "A tile is *stored in a
generation* if and only if that generation's tile-index entry for it is not the
sentinel". The stored-tile set is therefore the set of addressed tiles with
non-sentinel entries. Editing one sample of a tile that is *already stored* — the
ordinary meaning of the Note's example, and the case that produces the 20 MB it
quantifies — supersedes that tile's payload: the entry's offset, length and crc
all change, but the entry stays non-sentinel and every other entry stays as it
was, so the stored-tile **set** is unchanged. The trigger the Note names does not
reach the example the Note draws from it, and the "so" is a non-sequitur. The
half of the rule that does reach it — "or index content" — is the half the Note
drops.

That the document knows the difference is visible two subsections later: §20.4's
MU = 0 / PE = 0 row has to say, separately and explicitly, "Superseding a stored
tile's bytes re-places that layer's index region (§20.3, `[R-WRT-04]`), moving
its extent slot (§7.4) and so modifying that layer's record", precisely because
superseding is *not* a change to the entry set or to which tiles are stored.

**Which reading I picked.** Two readings are available: (a) "stored-tile set"
means the set of stored tiles, per §3.1, in which case the Note's inference
fails; (b) "stored-tile set" is loose for "the stored tiles' bytes", in which case
it holds. I picked (a): §3.1 defines the term, §20.4 uses the strict sense when
it matters, and §5.1 and `[R-WRT-04]` both feel the need to add "or index
content" — which would be redundant under (b). Under (b) the phrase would also
make §5.1's and `[R-WRT-04]`'s second disjunct unreachable.

**Byte-level: no.** The Note is non-normative (`[R-CNF-01]`) and `[R-WRT-04]` is
unambiguous. A writer that acted on the Note's narrower trigger could not
supersede a tile at all — `[R-LIF-01]` freezes the old payload where it lies, so
the new bytes need a new offset and the entry must change — so the mis-keying
cannot survive into an emitted file. What it costs is a reader of this document
who takes the Note as the rule and mis-plans the commit, and a triager who reads
the Note as the authority for §20.4's supersede case.

---

### 4.3 diagrams-03 — §13.3's sparse-writing Note enumerates two re-emission triggers where the rule has three, omitting supersede and shrink

**Location.** §13.3, the Note at lines 1786–1793, against §20.3 step 4
(`[R-WRT-04]`), §20.3's shrink paragraph, and §5.1's Example.

**Quotation (§13.3 Note).**

> "**Note — sparse writing.** A writer creates a sparse layer by emitting
> sentinel entries: no payload bytes, and for a full segment of sentinels
> even the segment CRC is a known constant (`[R-IDX-05]`). Declare-then-fill
> workflows append tiles as data arrives, generation by generation (§9);
> each commit that changes a layer's stored-tile set, or that grows its
> extents so that entry_count changes, re-emits that layer's whole
> tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

**Why this is a defect.** The rule's trigger is "stored-tile set **or index
content**". The Note substitutes "stored-tile set, or … grows its extents so that
entry_count changes". Two commits `[R-WRT-04]` obliges to re-emit fall outside
both of the Note's clauses:

1. **Superseding a stored tile's bytes.** Index content changes; the stored-tile
   set does not (§3.1); no extent grows. This is the same case as
   diagrams-02, met here through a different phrasing.
2. **A shrink that de-addresses only unstored tiles.** entry_count falls, so
   index content changes and §20.3 says so in terms — "`[R-CNT-17]` obliges the
   smaller entry_count and so a re-emitted index region" — but nothing is
   dropped from the stored-tile set and no extent *grows*.

The Note's statement is a true implication over a proper subset, so it is not
false in the way diagrams-02 is; its defect is that a reader taking it as the
account of when a layer's index is re-emitted gets a narrower rule than the one
that governs, and the narrowing is in the direction of under-writing. The
document's own full form is available twice (§5.1 and `[R-WRT-04]`), which is
what makes the divergence checkable rather than a matter of taste.

**Which reading I picked.** I read "grows its extents so that entry_count
changes" at its face: growth only, since §11.1 and §20.3 treat growth and shrink
as separate operations with separate permissions, and §20.3 states the shrink
consequence separately. Reading "grows" loosely as "changes" would repair one of
the two omissions and leave supersede untouched.

**Byte-level: no.** Non-normative Note; the governing rule is unambiguous and
`[R-LIF-01]` makes the omitted cases physically unavoidable in any case.

---

### 4.4 diagrams-04 — Appendix G's profile pins the filter value by an argument that applies verbatim to the layout field, which it does not pin, while claiming everything unpinned is already mandatory

**Location.** Appendix G item 5 and Appendix G's closing paragraph, against
Appendix G's opening, item 2's parenthetical, §14.1 `[R-SER-06]`, and §17.3
`[R-COD-09]`.

**Quotation (Appendix G, item 5).**

> "**No declared alignment and no slab**, or fixed declared values — both
> change placement and neither is implied by content. **A fixed filter
> value** likewise: §17.3 leaves the choice to the writer, it changes the
> stored bytes of every tile it touches, and no content implies it, so two
> writers agreeing on everything else still disagree on bytes without it
> pinned."

**And the closing paragraph:**

> "Everything else the profile needs is already mandatory — fill-encoded
> edge padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`)
> among them."

**Why this is a defect.** The three-part test item 5 applies to the filter field
— the specification leaves the choice to the writer; the choice changes the
stored bytes of every tile; no content implies it — is satisfied word for word
by the **layout** field. §14.1 `[R-SER-06]` leaves interleaved and planar both
open to a writer; the choice changes not only every tile's byte image but the
layer's entry_count (N versus C·N) and hence its whole index region; and §3.2's
reference array is indifferent to it, so no content implies it. The same is true
of the **tile extents**, which §11.3's Note expressly leaves to the writer
("Tile extents are a writer's choice, and this specification imposes none").
Neither is a numbered item, and neither is already mandatory — so the closing
paragraph's "Everything else the profile needs is already mandatory" is false
under the reading of "input" that makes item 5 necessary.

The document supplies the makings of the other reading in item 2:

> "this format fixes no canonical serialization of logical content, and two
> files carrying the same arrays can legitimately differ in tiling, layout,
> and codec."

Under that reading, tiling and layout are part of "the same input" a writer is
given, not degrees of freedom the profile owes anyone — and the profile is
complete as written. But then item 5's filter clause is unexplained on its own
terms, since the filter is a layer-record declaration exactly as layout is; and
item 1 pins the codec, which item 2's sentence has just named alongside tiling
and layout as a legitimate difference.

**The ambiguity, stated.** Appendix G never says what "the same input" is. Two
readings are defensible:

* **(i) Input = the logical arrays.** Then the profile must pin every
  byte-affecting declaration the reference array does not fix — tile extents,
  layout, codec, filter, alignment, slab. It pins four of the six; layout and
  tile extents are unpinned, and the closing paragraph's completeness claim
  fails.
* **(ii) Input = the arrays plus the full declared schema, layout and tiling
  included.** Then the profile is complete, and item 5's filter clause and item
  1's codec clause are pinning things that are already "input" — which the
  reasoning item 5 gives does not distinguish from layout.

I picked (ii) as the intended reading, on the strength of item 2's explicit
sentence about tiling and layout, and because reading (i) would make the closing
paragraph false rather than merely incomplete. But the document does not decide
it, and an adopter under reading (i) will believe the profile buys byte-identity
it does not buy.

**What an implementer does wrong without this.** Two teams adopting the profile
to get content-addressed storage, each handed the same arrays and the same
declared channels and extents, can still choose interleaved and planar and
produce completely different files — and both will believe they conform to the
profile, because the profile's own closing paragraph told them nothing else was
open. The repair is either to add layout (and tiling) to item 5, or to say in
the opening what "the same input" fixes.

**Byte-level: no.** Appendix G is labelled non-normative and states outright that
"It adds no requirement to any actor: a writer ignoring it is fully conforming",
so no conformance verdict and no emittable byte turns on it. Every file either
reading produces is a conforming file. `[R-CNF-05]` already licenses two
conforming writers to differ.

---

## 5. What I could not determine

Nothing material within my charter. Two judgement calls I made against
reporting, recorded so they can be overridden: §21.1's three-item list of
strict specializations is incomplete (at least T12 ⊂ T9 and T14 ⊂ T3), and
§21.6's "The file contains zero layers → A conforming file with an empty
directory" describes only one of the conforming files that satisfy its
condition (a zero-layer file may carry a top-level user-metadata record, whose
directory is not empty). I judged both to be below the reporting bar — the
first because the sentence says "Some" and states a general triage rule, the
second because the outcome cell's operative word, *conforming*, is correct and
no actor's behavior turns on the gloss.

Confidence that an implementation built from this document alone would
interoperate: high. Every figure, layout table, register cell, checksum
constant, hex dump and instance count I checked reproduces, and the four
findings above are all confined to non-normative material whose governing rules
the document states unambiguously elsewhere.
