# Cleanroom round 15 — Diagram auditor transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,227 lines, read in five contiguous chunks covering lines 1–4227). I ran
`wc -l` on that file, and three Python scripts that I wrote myself and that read
no project file except `spec/tarn.md`:

- `scratchpad/crc.py` — a from-scratch CRC-32C (reflected Castagnoli 0x82F63B78,
  init/final 0xFFFFFFFF) used to check every checksum constant in the document.
- `scratchpad/count.py` — reads `spec/tarn.md`, regex-extracts every §21.2–§21.5
  register row, and counts rows and semicolon-separated Instances cells.
- `scratchpad/build.py` — builds a complete conforming TARN file byte by byte
  from the document's rules alone, reading no file.

Plus one inline `python3 -` for Unicode NFC/NFD byte lengths and a grep-like
scan of the same file for normative keywords inside blockquotes.

I opened no ADR, no `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`, no git history, no web page. I did not list the output
directory. The task list visible in my harness's system reminders named prior
work items; I did not use it as evidence about the document and none of my
findings rests on it.

---

## Part 1 — Inventory of figures, diagrams, tables, examples and checklists

Enumerated before judging any, so coverage is checkable. Line numbers are from
the file as read.

### Layout / normative tables

| # | Line | Item |
|---|---|---|
| 1 | 235–241 | §2.4 outcome-class table (5 rows) |
| 2 | 691–694 | §6.1 front signature block (2 rows) |
| 3 | 734–746 | §6.2 trailer layout (10 rows) |
| 4 | 898–904 | §7.2 record header (5 rows) |
| 5 | 971–974 | §7.3 record types of format major 1 (2 rows) |
| 6 | 1000–1017 | §7.4 layer-record inline payload (17 rows) |
| 7 | 1115–1123 | §8.1 checksum coverage map (7 rows) |
| 8 | 1389–1398 | §10.2 numeric identifier spaces (8 rows) |
| 9 | 1589–1603 | §12.1 sample types (13 rows) |
| 10 | 1821–1824 | §14.2 decoded size / offset table (2 rows) |
| 11 | 1984–1985 | §15.1 index-region diagram (blockquote, unlabelled ⇒ normative) |
| 12 | 1989–1993 | §15.1 index entry layout (3 rows) |
| 13 | 2037–2049 | §15.3 entry-validity table (11 rows) |
| 14 | 2429–2431 | §18.2 user-metadata encoding byte (1 row) |
| 15 | 2578–2585 | §18.4 standardized keys (6 rows) |
| 16 | 3072–3076 | §20.4 updater obligation table (3 rows) |
| 17 | 3276–3313 | §21.2 file-scope register (F1–F36) |
| 18 | 3320–3370 | §21.3 layer-scope register (L1–L49) |
| 19 | 3377–3404 | §21.4 tile-scope register (T1–T26) |
| 20 | 3424–3435 | §21.5 ignored-record register (R1–R10) |
| 21 | 3442–3457 | §21.6 conditions that are not violations (14 rows) |
| 22 | 3546–3555 | §21.9 minimum-guarantee limits (8 rows) |
| 23 | 3882–3898 | Appendix A byte-annotation table (13 rows) |
| 24 | 3918–3946 | Appendix B constants (27 rows) |
| 25 | 3955–3973 | Appendix C registry snapshot (prose lists) |
| 26 | 4015–4017 | Appendix E changelog (1 row) |

### ASCII figures

| # | Line | Item |
|---|---|---|
| 27 | 582–586 | §5.1 three-commit region box |
| 28 | 1194–1203 | §9.2 "what a crash sees" (3 rows) |
| 29 | 3004–3008 | §20.3 shape (a) — a new layer |
| 30 | 3020–3024 | §20.3 shape (b) — tiles added |
| 31 | 3043–3046 | §20.3 shape (c) — directory-only change |
| 32 | 3154–3160 | §20.5 compaction input/output |
| 33 | 3871–3880 | Appendix A hex dump (128 bytes) |
| 34 | 1063–1082 | §7.4 layer-record payload byte dump |

### Worked numeric examples

§4.6 `température` (507–511); §5.1 smallest file (571–576); §7.4 layer record
(1052–1091); §11.2 grid (1506–1510); §11.4 ordinals (1560–1566); §12.1 bfloat16
(1623–1626); §12.3 channel entry (1672–1677); §13.3 fill tuples (1742–1747);
§14.2 byte layout (1863–1873); §14.3 packed bool (1897–1902); §14.5 padding
(1953–1958); §15.4 million-entry index (2077–2090); §15.4 planar ordinal
(2092–2096); §16.2 slab runs (2191–2198); §17.3 byte-shuffle (2372–2375);
§20.3 supersede cost (2990–2997); §20.3 three shapes (2999–3050); §20.5
compaction (3151–3179); §21.9 where-the-numbers-come-from note (3567–3582).

### Checklists

Appendix G — reproducible-writer profile, 10 numbered items (4039–4155).
Appendix H — conformance checklists, 5 classes (4157–4227).

---

## Part 2 — Arithmetic and byte verification

### 2.1 Every checksum constant

I implemented CRC-32C from the parameters in §4.5 (`[R-ENC-09]`: Castagnoli
0x1EDC6F41, reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — i.e.
reflected polynomial 0x82F63B78 — and checked it against §4.5's own check
vector before using it on anything else.

```
CRC32C("123456789")            = 0xE3069283   §4.5 says 0xE3069283          OK
CRC32C(<zero bytes>)           = 0x00000000   §4.5 says 0x00000000          OK
CRC32C(4 sentinel entries, 80B)= 0x80A34955   §7.4 example says 0x80A34955  OK
   stored little-endian        = 55 49 A3 80  §7.4 example says 55 49 A3 80 OK
CRC32C(<55 49 A3 80>)          = 0xC4EE982E   §7.4 example says 0xC4EE982E  OK
   stored little-endian        = 2E 98 EE C4  §7.4 dump line 77 says same   OK
CRC32C(2^16 sentinel entries)  = 0xEECB3BB2   §15.4 / App B say 0xEECB3BB2  OK
CRC32C(App A trailer[0,60))    = 0xE00938D2   App A says 0xE00938D2         OK
   stored little-endian        = D2 38 09 E0  App A dump 0070 says same     OK
```

The sentinel used is §15.2's `FF ×16 00 ×4` (20 bytes). The Appendix A trailer
I fed the CRC was assembled independently from §6.2's layout table — magic,
version_major=1, version_minor=0, flags=0, generation=1, dir_offset=16,
dir_length=4, committed_file_length=128, file_id=0x0123456789ABCDEF, reserved
zero — and came to exactly 60 bytes, matching §6.2's field offsets. All eight
constants reproduce. **No byte-level defect in any published constant.**

### 2.2 Appendix A, byte by byte

The hex dump at 3871–3880 decodes exactly as the annotation table says:

- [0,8) `89 54 41 52 4E 0D 0A 1A` = §6.1's magic. OK
- [8,16) zero = §6.1's reserved 8 bytes. OK
- [16,20) `00 00 00 00` — an empty record sequence (0 bytes) followed by
  CRC-32C of zero bytes = 0x00000000. Matches §7.1 and §4.5. OK
- [20,64) 44 zero bytes. §6.2 + `[R-LIF-02]` step 5 pad the directory end (20)
  to the next 64-byte boundary (64): 64 − 20 = 44. OK, and §5.1's example
  independently says "44 bytes of slack".
- [64,72) trailer magic, first byte 0x8A ≠ front block's 0x89 — §6.2's Note. OK
- [72,74)=01 00; [74,76)=00 00; [76,80)=00 00 00 00; [80,88)=gen 1;
  [88,96)=dir_offset 0x10; [96,104)=dir_length 4; [104,112)=0x80=128;
  [112,120)=file_id LE; [120,124)=0; [124,128)=D2 38 09 E0. All at §6.2's
  stated offsets. OK
- F = 128, 128 mod 64 = 0 (§6.2). dir_offset+dir_length = 20 ≤ F−64 = 64. OK
- 128 ≥ `[R-CNT-27]`'s 128-byte floor, and the prose "The smallest conforming
  TARN file is 128 bytes" is exactly satisfied, not merely bounded.

Appendix A's closing prose also checks out arithmetically: a 112-byte suffix
window covers [16,128), which contains the directory [16,20) but not [0,16), so
§6.4's containment test spares request 2 while `[R-CNT-04]` leaves the front
block unchecked. Correct.

### 2.3 §7.4's layer-record dump

I re-derived every offset in the 81-byte dump from §7.4's field order:

```
 0 name        1+3 = 4      → 0..3    03 73 73 74   ("sst" = 73 73 74)  OK
 4 layout      1            → 4
 5 lineariz.   2            → 5..6
 7 codec       2            → 7..8
 9 filter      2            → 9..10
11 A           8            → 11..18
19 S           8            → 19..26
27 A_slab      8            → 27..34
35 rank d      1            → 35
36 C           2            → 36..37
38 dim entry   1+1+8+8 = 18 → 38..55
56 chan entry  1+4+2+1+4=12 → 56..67
68 index_enc   1            → 68
69 entry_count 8            → 69..76
77 crc_of_crc  4            → 77..80
                              total 81
```

Every offset in the dump matches. The prose reconciliation also holds:
4 + 34 + 18 + 12 + 13 = 81, and the "nine scalars from layout through channel
count" are exactly layout(1)+lin(2)+codec(2)+filter(2)+A(8)+S(8)+A_slab(8)+
d(1)+C(2) = 9 fields, 34 bytes. Grid count ⌈100/32⌉ = 4 = entry_count.
Extent length 4×20 + ⌈4/2^16⌉×4 = 84. All correct.

Cross-check: the channel bytes at offsets 56–67 are
`04 74 65 6D 70 0C 00 04 00 00 C0 7F`, byte for byte §12.3's twelve-byte
example, as §7.4 claims. float32 is type 12 per §12.1, `0C 00` LE. Fill
0x7FC00000 LE = `00 00 C0 7F`. Correct.

One thing I checked deliberately: the example's segment is *partial* (4 entries,
not 2^16), and it computes 0x80A34955 rather than reaching for `[R-IDX-05]`'s
all-sentinel constant 0xEECB3BB2 — which is what `[R-IDX-05]` requires ("a
partial segment's CRC MUST be computed"). The example demonstrates the rule
correctly rather than tripping over it.

### 2.4 The geometry and serialization examples

- §11.2: E=(1024,2048), T=(256,256) → G=(4,8), N=32, P=65,536. ⌈1000/256⌉=4. OK
- §11.4: s = t₀·G₁ + t₁; (0,0)→0, (0,1)→1, (1,0)→8. (300,700) → t=(1,2), s=10;
  u=(44,188), in-tile ordinal 44·256+188 = 11,452. Planar c=2: 2·32+10 = 74. OK
- §14.2: interleaved T=(2,3), P=6, Q=1+2=3, size 18; (1,2) → ordinal 1·3+2 = 5;
  bytes [15,18). Planar `b`: 6·2 = 12 bytes, ordinal 5 at [10,12). float32+bool:
  Q=5, size 30, ordinal 5 at [25,30), t at 25–28, m at 29. All OK.
  The closing generalisation "channel c's value at in-tile ordinal u sits at
  byte u·Q + Fᶜ — the table's forms with k = u·C + c" is right: k div C = u and
  k mod C = c for c < C.
- §14.3: P=10, alternating T,F from ordinal 0 → bits 0,2,4,6 of byte 0 = 0x55;
  values 8,9 = T,F → byte 1 bit0 = 0x01; pad bits 2–7. Fill false → `55 01`;
  fill true → 0xFC|0x01 = 0xFD → `55 FD`. OK
- §14.5: E=(5,5), T=(4,4) → G=(2,2); tile (1,1) covers 4–7 on both axes; the
  only real position is (4,4), so 1 real + 15 padding; P=16, uint16 → 32 bytes;
  values 1–15 each `CD AB` for fill 0xABCD. OK
- §15.4 (a): 1,000,000 entries → ⌈10⁶/65536⌉ = 16 segments, 15 full covering
  983,040, last covering 16,960. CRC array 64 bytes. Region 20,000,064 bytes.
  k=999,999 → segment 15, segment-relative 16,959, byte 339,180. CRC array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000) = 339,200
  bytes ≈ 339 KB. One full segment = 65,536×20 = 1,310,720 = 1.25 MiB. All OK.
- §15.4 (b): disk ordinal 74 → region bytes [1480,1500) (74×20). Channel-3 block
  = [96,128) = 32 entries. OK
- §16.2: N=32, S=8 → runs [0,8),[8,16),[16,24),[24,32); rows 1–2 = ordinals
  8–23 = runs 1 and 2. OK
- §17.3: 1.0f/2.0f/3.0f LE = `00 00 80 3F 00 00 00 40 00 00 40 40`; s=4, n=3;
  byte i of group j → offset i·n+j gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`, exactly the example. OK
- §20.3: 32·20 + 4 = 644; 10⁶·20 + 64 ≈ 20 MB. OK
- §21.9 note: 2³² entries → 2¹⁶ segments → 256 KiB CRC array; 2³⁶ → 4 MiB;
  12.5 MiB / 65,536 ≈ 200 bytes per layer record. OK
- §4.6 / App G item 10: `température` NFC = 12 bytes
  `74 65 6D 70 C3 A9 72 61 74 75 72 65`; NFD = 13. Verified with Python's
  `unicodedata`. Exact match, including the hex.

Also checked, because §21.4's T26 turns on it: under §17.3's shuffle, the byte
at input offset L−1 (group j=n−1, byte i=s−1) maps to output offset
(s−1)n + (n−1) = L−1 for *every* stride s dividing L. So the final byte of a
packed bool plane is a fixed point of the shuffle at any stride, and a
mis-strided filter can never disturb pad bits. That means T26's claim that "the
check that detects it is T2's or T4's" is right and T5 is correctly absent from
it. I set out to file this as a defect and the arithmetic refuted me.

### 2.5 Register arithmetic

Mechanical count over §21.2–§21.5 (script `count.py`, semicolon-separated cells,
`—` counted as one):

```
F rows 36  instances  57
L rows 49  instances 115
T rows 26  instances  57
R rows 10  instances  44
TOTAL  121 rows, 273 instances
```

§21.2 says "36 conditions", §21.3 "49 conditions", §21.4 "26 conditions",
§21.5 "10 conditions", §21.8 "121 conditions over 273 instances". **All five
counts are exactly right.**

I then applied §21.1's instance criterion row by row. The layout axis (three
decoded-size formulas) and the magnitude axis (two directions for a "differs
from", one for an "exceeds") are applied consistently across T3 (3×2=6),
T14 (6), T22 (6), T21 (3, "larger than"), L44 (3, "exceeds"), L21 (4), L22 (4),
L30 (2), F17 (2). Value tests and constant comparisons enumerate no direction
(F13, F14, F20, L37, L38, T1). Twin rows across scopes are symmetric — F29/L14
(3/3), F25/L46 (1/2 containers), F26/L47 (1/2), F28/L49 (2/4), F35/L24, F36/L25,
F21-23/L10-12, F34/L19, F24/L13, F27/L48. F33 (5 claimant kinds) versus L18 (3)
is right, since the directory region and non-layer extents cannot participate in
an intra-layer overlap. The one place I found the criterion applied unevenly is
R4 against T18 — finding `diagrams-07`.

### 2.6 The build

I built a complete conforming file from the document alone (`build.py`), to find
where an implementer has to guess. Layer `img`: rank 2, dims `y` (E=2, T=2) and
`x` (E=3, T=3), interleaved, channels `a` (uint8, fill 00) and `b` (uint16, fill
00 00), codec 1, filter 1, one stored tile.

```
G=(1,1)  N=1  P=6  C=2  Q=3  entry_count=1  decoded size = P·Q = 18
value k → channel (k mod 2) at ordinal k div 2; offset (k div 2)·3 + F_{k mod 2}
tile image:  00 E8 03 | 01 E9 03 | 02 EA 03 | 03 EB 03 | 04 EC 03 | 05 ED 03
inline_length = 4+34+36+13+13 = 100
index region  = 1·20 + ⌈1/2^16⌉·4 = 24
layout: front[0,16) tile[16,34) index[34,58) dir[58,186) pad[186,192) trailer[192,256)
F = 256, F mod 64 = 0, dir_offset+dir_length = 186 ≤ 192 = F−64
```

The whole 256-byte file came out without a single undetermined choice at the
container level. Every field width, every ordering constraint, every checksum
scope, and the pad arithmetic are fully determined by §5–§8 and §14–§15. The
document stands up well to a first-time implementer for the *create* path.

Where I had to guess was not in creating a file but in three later operations —
compacting one (`diagrams-01`), shrinking a layer's extents (`diagrams-05`), and
adopting Appendix G's reproducible-writer profile (`diagrams-04`).

### 2.7 Promise-versus-delivery checks

- **§4.7's Note on layout-table columns.** It promises: fixed-layout tables give
  offset, size, type, name, class, valid range; §7.4's packed payload omits
  offset and class; §6.1 replaces type and range with a Value column; §7.2 folds
  range into the Field cell. Checked all six layout tables (§6.1, §6.2, §7.2,
  §7.4, §15.1, §18.2). Every one matches its description exactly. Delivered.
- **§8.1's coverage map.** Walked every field of every structure against the map
  and §4.5's exception list. Trailer [0,60) ← trailer CRC; directory record
  sequence ← directory CRC; index entries ← segment CRCs ← crc_of_crc_array
  (which itself lives in the directory and is covered by the directory CRC);
  stored tile ← entry crc; user-metadata extent ← its terminal 4 bytes;
  unassigned record extent ← nothing. Terminal fields (trailer CRC, directory
  CRC, user-metadata CRC) are covered by nothing, exactly as §4.5 says; interior
  fields (segment CRC array, entry crc, crc_of_crc_array) are each covered once,
  exactly as §4.5 says. In format major 1 the only assigned record types are
  layer (extent = tile index) and user metadata (extent = document), so no
  assigned extent falls outside the map. Complete and consistent.
- **§21.1's completeness clause versus §21.7's account.** I walked every
  `[R-…]` identifier looking for a MUST-level, file-witnessed condition with
  neither a register row nor a §21.7 entry. Everything I could name is placed:
  writer-conduct rules by `[R-CNF-02]` and §21.6; history properties, ordinal
  mappings, opaque MU=0 payloads, sub-record nesting, §20.3 step 4's bar and
  `[R-ENC-06]`'s field widths by §21.7; `[R-SLB-04]`'s stale slab declaration by
  §16.2's Note routing it to L41/L42; `[R-LIF-04]`'s residue by §9.5's Note
  routing it to F8/F17; `[R-CNT-02]`'s "belongs to no class" half by §5.2's Note
  ("a register row for it would be a row no file could exhibit"). I found no
  omission.
- **Appendix H's verifier checklist versus the verifier-detected rows.** The
  verifier rows are F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42,
  L46, L47, L48, L49, T2, T4, T5, T26, plus F1/F6 (which §2.3 denies a verifier
  the residency exemption for). Appendix H names every one of them, T26 via the
  T2/T4 checks that actually detect it. Complete.
- **§2.1's Note on drafting discipline.** Extracted all 38 normative SHOULD
  occurrences. The claim "every writer-side prohibition is paired with an
  explicit reader-side clause" holds throughout, with the unwitnessable cases
  (`[R-LIF-01]`, `[R-CNT-13]`'s payload-offset ban, `[R-CNT-18]`'s nesting ban,
  `[R-COD-06]`'s undisclosed dictionary, `[R-COD-10]`'s stride) each explicitly
  addressed where they arise. The claim "every SHOULD states the consequence of
  deviation" holds for all but three (`[R-SLB-01]`'s and `[R-SLB-03]`'s
  zero-the-slack, which delegate to `[R-CNT-03]`, and `[R-MTA-09]`'s "the
  verifier SHOULD report the bound it applied", which states none). Since the
  claim sits in a Note and two of the three delegate, I am not filing it; I
  record it here so the check is on the record.
- **Appendix B against every section it cites.** All 27 rows re-derived. Every
  value matches its defining section, including the reader-minimum-guarantee row
  against §21.9's eight-row table (rank 32 · C 4096 · entry_count 2³² · 65,536
  layers · 16 MiB directory · 256 MiB tile · 16 MiB document · 8 MiB window).
- **Appendix C against §7.3, §10.2, §12.1/§12.2, §14.1, §15.1, §17.2, §17.3,
  §18.2, §18.4.** Every assignment and every pinned reservation matches,
  including "19 opaque" against §12.2's "a fixed-size raw-bytes type".
- **§10.2's eight identifier spaces** against the sections that own them. All
  eight partitions match, including §11.4's split of linearization's reserved
  range (2–3 without semantics, 4–0x7FFF for future assignment) and §12.2's
  (14–19, 20–0x7FFF), which L33 and L34 then enumerate as separate instances.
- **§5.1, §9.2, §20.3(a)(b)(c), §20.5 region figures.** Each re-derived against
  the commit protocol. §5.1's three-commit box is exactly what `[R-LIF-02]`
  produces for create-A / add-B / touch-nothing, with the two hatched runs being
  dir₁-pad-trail₁ and dir₂-pad-trail₂ in the right positions. §9.2's three rows
  match §9.4/§9.6. §20.3's three shapes match step 4 and `[R-WRT-05]`.

---

## Part 3 — Findings

### diagrams-01 — CONTRADICTION — §20.5 licenses a compactor to place structures where §16 forbids, and its twin §20.2 does not

**Location:** §20.5, `[R-WRT-07]` (line 3132); against §16.1 `[R-SLB-01]`,
§16.2 `[R-SLB-03]`, and §20.2 `[R-WRT-02]`.

**Quotation (§20.5):**
> "A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits"

**Quotation (§16.1):**
> "When declared: every stored tile's offset satisfies offset mod A = 0."

**Quotation (§20.2, the twin):**
> "each layer's stored tiles, tile-index region, and any record extents, in any
> order satisfying §5.2's coverage classes (`[R-CNT-02]`, `[R-CNT-03]`) and
> every declared layout invariant (`[R-SLB-01]`, `[R-SLB-03]`) — placement is
> otherwise free (`[R-SLB-05]`)"

§5.2 constrains placement in exactly one way: the live state must partition into
non-overlapping claimants. It says nothing about alignment or slab packing. So
"anywhere §5.2 admits" admits a placement in which an A=4096 layer's relocated
tiles sit at arbitrary offsets, and in which a slab-declared layer's runs are
neither packed nor A_slab-aligned. §16.1 and §16.2 forbid both, and §21.3
registers them as L40, L41, L42 — verifier-detected, reject-layer.

The creation path (§20.2) states the qualifier and names both rules. The
compaction path does not: the enumeration was extended in one place and not its
twin. This matters more for compaction than for creation, because compaction is
the one operation that *moves live bytes* (§20.5's own figure caption says so),
so it is the only place where an existing declared invariant has to be
re-established at a new address. Note also that a compactor cannot take the
escape `[R-SLB-04]` gives an appender — clearing the declaration — because §20.5
permits it to change only the extent slot and crc_of_crc_array of a re-emitted
layer record, and `[R-WRT-05]` requires byte-identical re-emission otherwise.
That obligation to *re-establish* the invariant is nowhere stated for a
compactor; the section instead states its negation.

An implementer building a compactor reads §20.5 as the section that governs
compaction, and its placement sentence is the operative permission there. I had
to go outside the section to settle it.

**Byte-level: no.** What already decides it: §20.5's own preceding paragraph
("Given a conforming input the output is a conforming file"), `[R-CNF-05]` ("A
writer MUST emit only conforming files"), and §20.1's `[R-WRT-01]` ("An appender
and a compactor satisfy every writer requirement for the bytes they produce").
Three independent normative statements force the aligned output, so two
competent implementations should not actually diverge on bytes. The sentence is
still wrong and should carry §20.2's qualifier.

---

### diagrams-02 — CONTRADICTION — §21.1 says `[R-SER-08]` obliges a reader to serve the structure unchanged; §14.2 obliges the opposite

**Location:** §21.1 closing paragraph (line 3259); against §14.2 `[R-SER-08]`
and Appendix H.

**Quotation (§21.1):**
> "For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader to
> serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`, and `[R-MTA-05]`,
> whose unsorted document readers process as they find it — F27 and L48)."

**Quotation (§14.2, `[R-SER-08]`):**
> "A reader that neither detects the violation nor rejects the tile, and returns
> the value, MUST report 0x00 as false and every other byte as true."

**Quotation (Appendix H, conforming reader):**
> "returns sample bit patterns unaltered (§3.2), the sole resolved byte being a
> nonconforming interleaved boolean it chooses to return rather than reject
> (`[R-SER-08]`, §14.2)"

Two defects in one clause. First, `[R-SER-08]` is precisely the document's one
case where a reader may *not* serve the byte unchanged: §3.2's `[R-MDL-02]` and
§12.3's `[R-TYP-04]` require bit patterns to pass through untouched everywhere
except here, and Appendix H names this as "the sole resolved byte". A reader
that took §21.1 at its word and returned 0x7F for a malformed interleaved
boolean would violate `[R-SER-08]`. Second, `[R-SER-08]` does not *oblige*
serving at all: it is conditional ("A reader that neither detects the violation
nor rejects the tile, and returns the value"), and `[R-CNF-12]` expressly lets
the reader reject instead. `[R-CNT-22]` and `[R-MTA-05]` really do state reader
obligations of the shape §21.1 describes; `[R-SER-08]` does not, and grouping it
with them mis-states what T2's governing rule says.

The permitted readings of "serve the structure unchanged" are (i) "return the
stored byte as-is", which §14.2 forbids, and (ii) "do not reject the tile",
which is not an obligation `[R-SER-08]` imposes. I picked neither for
implementation: I implemented §14.2, because it is the rule and §21.1 is a
summary of detectors.

**Byte-level: no.** What already decides it: §14.2's `[R-SER-08]` states the
reader's obligation directly and unconditionally in its own terms, Appendix H
restates it correctly, and §21.1 itself says "each row *restates* its governing
rule, and where a row and the rule it cites diverge, **the rule governs**". The
divergence is also about a returned *value*, not about bytes on disk or an
accept/reject verdict, so it falls outside the byte-level test even where a
reader got it wrong.

---

### diagrams-03 — CONTRADICTION — §11.1's parenthetical asserts a grid count of 1 where §11.1's own next paragraph and §11.2 give 0

**Location:** §11.1, `[R-GEO-01]` (line 1464); against §11.1 `[R-GEO-02]` and
§11.2 `[R-GEO-03]`.

**Quotation (§11.1):**
> "A tile extent MAY exceed its dimension's extent (the grid is then a single
> padded tile along that axis)."

**Quotation (§11.1, the next paragraph):**
> "A dimension with extent 0 is valid: its grid count is 0, the layer has zero
> addressed tiles, its tile index has zero entries, and its reference array is
> empty."

**Quotation (§11.2):**
> "For each dimension, the **grid count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉"

Take Eᵢ = 0 and Tᵢ = 10. The tile extent exceeds the dimension's extent, so the
parenthetical's antecedent is satisfied and it asserts a grid of one padded
tile. `[R-GEO-03]` gives ⌈0/10⌉ = 0 and `[R-GEO-02]` says so in words. The
parenthetical is not labelled Note, Example or Rationale, so §2.1 makes it
normative text; it is a normative sentence that is false on the boundary case
the very next paragraph is about.

This is not academic: it is the difference between entry_count = ∏Gᵢ being 0 or
nonzero for a zero-extent layer, and with it between an extent slot of (0,0)
with crc_of_crc_array = 0 and a real index region — a difference L21, L22 and
L27 all register. The zero-extent layer is the document's declared
schema-first-workflow case (§11.1's Rationale, §21.6), so it is the case a
reader most needs the parenthetical not to mislead on.

**Byte-level: no.** What already decides it: `[R-GEO-03]` states the grid count
as a formula and is the section titled "Grid arithmetic"; `[R-GEO-02]` states
grid count 0 for Eᵢ = 0 explicitly, in the same subsection, one paragraph later.
No implementation derives grid counts from an aside in the geometry-floor
paragraph rather than from the arithmetic rule.

---

### diagrams-04 — AMBIGUITY — Appendix G item 3 pins the placement order of record *extents* but never the directory's record-sequence order, which the appendix's own summary claims it adds

**Location:** Appendix G, item 3 (lines 4080–4107) and the closing paragraph
(lines 4140–4155).

**Quotation (item 3):**
> "then any record extents in ascending record order — all of them after every
> layer's tiles and index region, not interleaved with them; then the directory.
> That order runs over top-level records first, then, within each layer record,
> its sub-records."

**Quotation (item 3, later):**
> "Record order carries no meaning (`[R-CNT-14]`), so it is otherwise free to
> vary, as is structure placement (`[R-LIF-02]` step 2)."

**Quotation (the closing paragraph):**
> "The items above add what is not, and the list is not short: gap *content*,
> which `[R-CNT-03]` only advises; gap *extent*, which placement freedom
> (`[R-SLB-05]`) leaves open; record and sub-record order, which `[R-CNT-14]`
> leaves free"

The profile's purpose is byte-identical output. The directory is a byte range
whose content depends on the order in which its records are concatenated
(`[R-CNT-14]`: "Record semantics MUST NOT depend on record order"), so byte
identity requires that order to be pinned. Item 3 defines a total order over
records — by type, type 0x0001 tying by layer name, everything else by header
with extent_offset masked, then inline payload, then extent contents — but it
applies that order to exactly one thing: *"any record extents in ascending
record order"*. It never says the directory's record sequence is emitted in that
order.

Two readings are defensible. (A) "ascending record order" is a total order over
records and the directory emits records in it; the closing paragraph's claim
that the items add "record and sub-record order" is then true. (B) Item 3 pins
only extent placement; directory record order stays free, and the closing
paragraph misstates the list. Reading B is not idle: item 3's own last sentence
says record order "is otherwise free to vary", and "otherwise" has no clear
antecedent if the directory order was never fixed.

The tie-break key itself is evidence for (A): it includes "type 0x0001 ties by
layer name", but type 0x0001's extent is the tile-index region, which item 3
places in the *earlier*, per-layer stage. So the 0x0001 clause of the key is
dead unless the key also orders the directory. I implemented (A). An implementer
who implements (B) emits a different directory, a different `dir_length`
position, and a different file for the same content — which is the one thing the
profile exists to prevent.

**Byte-level: no.** What already decides it: Appendix G is labelled
non-normative and states outright that it "adds no requirement to any actor: a
writer ignoring it is fully conforming". Both readings produce conforming files,
and neither changes any reader's accept/reject verdict. The divergence is in
profile conformance only, which the appendix says is "refuted cheaply but
confirmed only by reproducing the file".

---

### diagrams-05 — AMBIGUITY — whether a layer's extents may shrink is settled only in §11.1's *Rationale*, which §2.1 denies normative force, and §20.3's normative text grants growth alone

**Location:** §20.3 step 4, `[R-WRT-04]` (lines 2938–2970); §11.1's Rationale
(lines 1474–1485); §2.1 `[R-CNF-01]`.

**Quotation (§20.3 step 4):**
> "and an extent MAY **grow**, since a position that becomes real held that
> channel's fill and fill is a legal sample value — provided the grown geometry
> stays within every bound the layer's own declarations impose"

**Quotation (§11.1, labelled Rationale):**
> "Extents grow; a shrink is barred wherever it alters what §14 fixes for a tile
> the layer already stores (§20.3, which states the tense normatively and
> governs), which is the ordinary case — a layer that stores nothing may still
> be re-declared freely."

**Quotation (§2.1):**
> "All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative."

The word "shrink" appears nowhere in §20.3. §20.3 states a general bar — "A
commit MUST NOT change a layer's declarations in a way that alters, for any tile
that layer stores **in the generation this commit supersedes**, what §14 fixes
for its stored bytes or how they decode" — and then a single explicit
permission, for growth. The Rationale in §11.1 asserts that §20.3 "states the
tense normatively and governs" the shrink question, but §20.3 does not address
shrinking at all; the only sentence that tells an implementer a shrink is ever
allowed sits inside a Rationale that §2.1 excludes from the normative text.

Two things are undetermined as a result.

1. **Whether "MAY grow" is exclusive.** Reading (i): the bar is the only
   prohibition, so anything it does not reach is permitted, and the growth
   clause is illustration. Reading (ii): the section grants growth and grants
   nothing else, so a shrink is never an appender's operation. Only the
   Rationale picks (i).

2. **If shrinks are permitted, whether abolishing a stored tile is "altering
   what §14 fixes for its stored bytes".** Take E=100, T=32 (G=4, entry_count=4)
   with all four tiles stored, shrinking to E=64 (G=2, entry_count=2). Tiles 0
   and 1 keep their padding sets, decoded size, offsets, codec and filter, so
   the enumerated loci are untouched. Tiles 2 and 3 cease to be tiles of the
   layer and their payloads fall to slack. Reading (a): nothing about tile 2's
   *stored bytes* was altered — they were not rewritten — so the commit is
   allowed in one step. Reading (b): §20.3's own gloss says the bar spares only
   "a change that leaves every one of those tiles' stored bytes meaning exactly
   what they meant", and bytes that become unreachable slack no longer mean what
   they meant, so it is barred and the writer must unstore tiles 2 and 3 in an
   earlier commit — which §20.3 forces, since "a commit does not escape this by
   unstoring in the same breath".

I implemented (i) and (b): shrinks permitted, but a shrink that drops a stored
tile requires a prior commit that unstores it. That is the reading that makes
§20.3's "in the generation this commit supersedes" tense do work, and it matches
the Rationale's "which is the ordinary case".

**Byte-level: no.** What already decides it: §21.7 states that "§20.3 step 4's
bar on a declaration change is witnessed only where the affected tiles remain
stored", so a file produced under either reading has a clean live state and is
conforming; no reader or verifier verdict turns on which reading a writer used.
The fork is in writer conduct, which `[R-CNF-02]` separates from the byte
predicate.

---

### diagrams-06 — OBSERVATION — L40 and L42 omit the structural-entry transparency that L41 states, so read alone they classify entries §15.3 excludes

**Location:** §21.3, rows L40, L41, L42 (lines 3361–3363); against §15.3
`[R-IDX-03]` and §16.2 `[R-SLB-03]`.

**Quotation (L41, which carries the qualifier):**
> "Inside a slab run, a stored tile's offset ≠ the previous stored tile's offset
> plus that tile's length (gap, overlap, or out-of-ordinal placement; sentinels
> and entries §15.3 classifies reject-tile on a structural ground are
> transparent, an entry failing only its stored bytes' crc is not)"

**Quotation (L40, which does not):**
> "Alignment A declared and a stored tile's index-entry offset is not a multiple
> of A"

**Quotation (§15.3):**
> "Such an entry contributes no stored extent to the *verifier* rows, which bind
> over well-formed entries' extents only"

§3.1 makes every non-sentinel entry a "stored tile". §15.3 then carves six
structurally malformed states out of the verifier rows — one of which is its own
"alignment or slab invariant violated (§16)" row. L41 restates that carve-out;
L40 and L42 use the bare phrase "a stored tile" and do not. A verifier built from
L40's cell alone would raise reject-layer for a layer whose A=4096 declaration is
otherwise honoured but which carries one entry with, say, offset 1000 and
offset+length past F−64 — an entry §15.3 has already excluded from the alignment
check and classified reject-tile.

The same asymmetry appears in the smaller pair F31 ("extent_offset in 1-15",
which cedes offset 0 to F30) against L16 ("extent_offset < 16", which does not
cede it to L15). I mention it here rather than filing it, since it has no
consequence for any verdict.

I am filing this as an OBSERVATION rather than a contradiction precisely because
§21.1 has already decided it, and I want the record to say so rather than to
imply an open verdict. It is nonetheless the "enumeration extended in one place
and not its twin" pattern, in a changed section, and the fix is one clause.

**Byte-level: no.** What already decides it: §21.1's "each row *restates* its
governing rule, and where a row and the rule it cites diverge, **the rule
governs**", plus §15.3's explicit statement that structural entries contribute
no extent to the verifier rows — of which §15.3's alignment/slab row is one.
Only the table is wrong.

---

### diagrams-07 — AMBIGUITY — §21.1's instance criterion does not determine whether R4 enumerates skippable-frame positions as T18 does, leaving §21.8's 273 under-determined

**Location:** §21.5 row R4 (line 3429); §21.4 row T18 (line 3396); §21.1's
instance criterion (lines 3227–3255); §21.8 `[R-ERR-02]`.

**Quotation (T18's Instances cell):**
> "a second concatenated compressed frame; a skippable frame before the frame; a
> skippable frame after the frame; a skippable frame between two frames"

**Quotation (R4's Instances cell, the corresponding alternatives):**
> "a skippable frame, top-level extent; a skippable frame, layer sub-record
> extent; a second frame, top-level extent; a second frame, layer sub-record
> extent"

**Quotation (§21.1):**
> "What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25)."

T18 and R4 police the same `[R-COD-06]` frame constraints — R4's condition cell
says so: "breaks one of the frame constraints §18.2 states or carries over from
`[R-COD-06]`". T18 treats the three placements of a skippable frame (before,
after, between two frames) as materially different shapes and enumerates them;
R4 folds all three into a single "a skippable frame" per container. If the tile
side is right, the metadata side is short by two alternatives in each of two
containers, R4 is 16 instances rather than 12, and §21.8's total is 277 rather
than 273. If the metadata side is right, T18 is 2 rather than 4 and the total is
271.

The criterion does not settle it, because "the condition's own alternatives" is
itself ambiguous here: §17.2's text says a reader must reject a payload "that
contains a skippable frame **anywhere** or more than one frame", which reads as
licensing the positional enumeration, while §18.2's carry-over says only "no
skippable frame and no second frame". R4's governing rule is `[R-MTA-09]` citing
`[R-COD-06]` — so the row inherits the "anywhere" text while its cell is written
against §18.2's wording.

I picked T18's reading as the correct one (the constraint is `[R-COD-06]`'s in
both places), which makes R4 the row to repair and 273 the number to restate. I
flag it because §21.8's completeness is a normative promise consumed by
`[R-VEC-03]` — "every register row has at least one vector for each instance it
names" — so an unresolved instance count is four missing corpus files.

**Byte-level: no.** What already decides it: nothing in the file conformance
predicate turns on it. R4 and T18 both already register every listed
constraint-break as a violation with a fixed outcome (ignore-record and
reject-tile respectively), and a file carrying a skippable frame in any position
is caught either way. The disagreement is over how many vectors the corpus owes,
not over any byte or verdict.

---

## Part 4 — What I checked and did not file

For the record, so that the absence of a finding is legible as a check rather
than an omission:

- Every CRC constant, every hex dump, and every arithmetic claim in every worked
  example (Part 2). All correct, including the two constants that are the most
  expensive to get right by hand (0xEECB3BB2 over 1.25 MiB of sentinels, and
  0xC4EE982E's double-CRC chain).
- §21.4's T26 claim that a mis-strided filter is detected by T2 or T4 and never
  by T5 — proved correct by the fixed-point argument in §2.4.
- §14.2/§14.3/§17.3's divisibility claim ("The decoded image's length L is
  divisible by s in every case") — holds for all three layout/type combinations.
- §21.1's specialization list (F1 of F6 and F8, F35 of F36, L24 of L25) — each
  containment holds, and in the F35/F36 and L24/L25 pairs the narrower row
  really does carry the different detector and detection point, which is the
  point of the rule.
- §21.2's five row-count claims and §21.8's 121/273 — exact.
- The §20.5 compaction figure's output showing a `pad` box that is slack but not
  hatched — the ▓/pad distinction is established by §5.1's figure, whose caption
  says "the pad and the ▓ runs are slack", so the convention is consistent
  across figures and I am not filing it.
- §10.2's "Two spaces carry no experimental range", one of which (the trailer's
  flag lanes) is not a row of §10.2's table — self-explaining, not filed.
- §5.2, §9.7 and §15.3's three statements of structural-entry transparency
  against one another — mutually consistent, which surprised me; this is the
  triple I expected to find broken.
- §5.2's partial-slack-total arithmetic — "F less the bytes claimed by the
  claimants the walk did enumerate" is an upper bound on the true slack for
  every subset of claimants, so "never an under-count" is right.
- The normative citation of positional register labels (L18, L40–L42 in §5.2;
  L44 in §20.3; F1/F6/F7/F36/L25/R1 in Appendix H) against §24's own warning
  that "row labels are positional and renumber when a row is struck" — a
  maintenance hazard rather than a defect in the text as it stands.
