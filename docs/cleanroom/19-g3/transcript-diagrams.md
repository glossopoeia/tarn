# Round 19 — Diagram auditor transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,364 lines, read in full across five `Read` calls plus targeted `grep`/`awk`
over the same path). I did not open `docs/`, `PLAN.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, or any git history, and I ran
no web tool. I ran local Python that reads no project file except through
scripts I wrote myself into the scratchpad
(`crc.py`, `appA.py`, `build.py`, `inst.py` — the last two of which parse
`spec/tarn.md`, the one permitted file). I wrote `demo.tarn` (a file I
constructed) into the scratchpad. I did not read the round19 output directory.

I did not consult any prior round's findings, any ADR, or any test vector. Where
I use knowledge of RFC 1951 / RFC 8878 / LZ4 below it is only to generate a
suspicion; every conclusion I state is settled from this document's text.

---

## 1. Method

Charter: every figure, byte-layout box, offset table, worked example and
checklist, checked against the prose it illustrates.

Step 1 — enumerate before judging. Step 2 — recompute every number. Step 3 —
build a conforming file end to end from the document alone and record where I
had to decide something the text did not decide for me. Step 4 — go back over
the four sections the brief flagged (§20.5, §21.7, §23.1, Appendix G) plus the
places nobody has had to implement from recently.

### 1.1 Inventory of figures, boxes, tables, examples and checklists

Line numbers are the first line of the item.

**ASCII region diagrams (5)**

| # | line | what |
|---|---|---|
| D1 | 587 | §5.1 — a file after three commits |
| D2 | 1069 | §7.4 — annotated layer-record inline payload (81 bytes) |
| D3 | 1200 | §9.2 — what a crash sees (3 rows) |
| D4 | 3050 / 3066 / 3090 | §20.3 — the three shapes a commit takes, (a)(b)(c) |
| D5 | 3230 | §20.5 — what compaction reclaims (input/output) |

**Byte-layout / offset boxes (6)**

| # | line | what | columns |
|---|---|---|---|
| B1 | 697 | §6.1 front signature block | Offset, Size, Value, Class |
| B2 | 740 | §6.2 trailer | Offset, Size, Type, Field, Class, Valid values |
| B3 | 904 | §7.2 record header | Offset, Size, Type, Field, Class |
| B4 | 1006 | §7.4 layer-record inline payload | Field, Type, Constraint |
| B5 | 1999 | §15.1 tile-index entry | Offset, Size, Type, Field, Class, Valid values |
| B6 | 2439 | §18.2 user-metadata inline payload | Offset, Size, Type, Field, Class, Valid values |
| B7 | 1994 | §15.1 region composition (blockquoted bracket figure) | — |

**Normative tables whose cells restate rules (11)**

235 (§2.4 outcome classes) · 977 (§7.3 record types) · 1121 (§8.1 coverage map)
· 1395 (§10.2 identifier spaces) · 1599 (§12.1 sample types) · 1831 (§14.2
decoded size / offset) · 2047 (§15.3 entry validity) · 2588 (§18.4 standardized
keys) · 3119 (§20.4 preservation obligations) · 3535 (§21.6 non-violations) ·
3654 (§21.9 minimum guarantees)

**Register tables (4)** — 3367 (§21.2, F1–F36) · 3411 (§21.3, L1–L49) · 3468
(§21.4, T1–T26) · 3517 (§21.5, R1–R10)

**Worked examples (21)** — 513 (§4.6 `température`) · 577 (§5.1 smallest file) ·
584 (D1) · 1058 (D2) · 1196 (D3) · 1516 (§11.2 grid) · 1570 (§11.4 ordinals) ·
1633 (§12.1 bfloat16) · 1682 (§12.3 channel entry) · 1752 (§13.3 fill) · 1873
(§14.2 offsets) · 1907 (§14.3 packed bool) · 1963 (§14.5 padding) · 2087 (§15.4
1e6 entries) · 2102 (§15.4 planar ordinals) · 2201 (§16.2 slab runs) · 2382
(§17.3 byte-shuffle) · 3036 (§20.3 supersede cost) · 3045 (D4) · 3227 (D5) ·
3985 (Appendix A hex dump + annotation table)

**Appendix material (7)** — A (3979, annotated minimal file) · B (4027,
constants) · C (4062, registry snapshot) · D (4089, design rationale) · E (4127,
changelog) · F (4138, references) · G (4153, reproducible-writer profile,
items 1–10) · H (4293, five conformance checklists)

**Numbered lists (7)** — §6.4 (1)(2) · §9.2 (1)–(6) · §10.1 1–4 · §18.2 four
restrictions · §19.1 1–4 · §19.4 1–8 · §20.3 1–6 · Appendix G 1–10.
All are contiguous, none duplicated, none out of order. `[R-SER-04]` is the one
withdrawn identifier and §14.4's Note says so; a numbering sweep over all
`[R-<PREFIX>-<NN>]` shows no gaps in any prefix (CNF 1–12, CNT 1–27, COD 1–11,
ENC 1–16 plus the illustrative `[R-ENC-100]` in §2.2, ERR 1–5, EXT 1–5, GEO 1–6,
IDX 1–5, LIF 1–8, MDL 1–2, MTA 1–10, PRV 1–5, RDR 1–4, SEC 1–7, SER 1–9, SLB
1–5, TYP 1–10, VEC 1–4, WRT 1–9). `[R-VEC-04]` is defined before `[R-VEC-03]`;
§2.2 says identifier order carries no meaning, so that is not a defect.

---

## 2. Arithmetic and checksums — everything I recomputed

### 2.1 CRC-32C constants

I implemented CRC-32C from §4.5's parameters alone (reflected polynomial
0x82F63B78 from the stated 0x1EDC6F41, init 0xFFFFFFFF, final XOR 0xFFFFFFFF)
and reproduced §4.5's check vector before using it for anything:

```
CRC32C("123456789") = 0xE3069283      §4.5 says 0xE3069283, bytes 83 92 06 E3  OK
CRC32C(<zero bytes>) = 0x00000000     §4.5 says 0x00000000                     OK
```

Then every CRC constant the document states:

```
80 bytes = 4 sentinel entries (FF x16 00 x4)      -> 0x80A34955   §7.4 example: 0x80A34955  OK
  stored little-endian                            -> 55 49 A3 80  §7.4 example: 55 49 A3 80  OK
CRC32C(55 49 A3 80)                               -> 0xC4EE982E   §7.4 example: 0xC4EE982E  OK
65,536 sentinel entries (one full segment)        -> 0xEECB3BB2   §15.4 / App B: 0xEECB3BB2 OK
```

Appendix A's 128-byte hex dump, reassembled from the dump text and checked
field by field against §6.2's trailer table:

```
trailer bytes [0,60) -> CRC32C = 0xE00938D2      dump stores D2 38 09 E0 at [124,128)  OK
directory region [16,20) = 00 00 00 00           = CRC32C of zero bytes                 OK
```

Appendix A's annotation table maps every one of the 128 bytes and the map is
correct against B2: magic [64,72) at trailer offset 0; version_major [72,74) at
offset 8; version_minor [74,76) at 10; flags [76,80) at 12; generation [80,88)
at 16; dir_offset [88,96) at 24; dir_length [96,104) at 32;
committed_file_length [104,112) at 40; file_id [112,120) at 48; reserved
[120,124) at 56; CRC [124,128) at 60. `file_id` bytes `EF CD AB 89 67 45 23 01`
read little-endian as 0x0123456789ABCDEF, as the table says. Pad [20,64) is 44
bytes, which is exactly `[R-LIF-02]` step 5's pad-to-next-64 from a directory
ending at 20. Appendix A is clean byte for byte.

### 2.2 §7.4's annotated layer-record payload (D2)

Offsets recomputed from the field widths in B4, not read off the figure:

```
name           1+3  =  4   -> 0    fig: 0    OK
layout         1        1   -> 4    fig: 4    OK
linearization  2            -> 5    fig: 5    OK
codec          2            -> 7    fig: 7    OK
filter         2            -> 9    fig: 9    OK
A              8            -> 11   fig: 11   OK
S              8            -> 19   fig: 19   OK
A_slab         8            -> 27   fig: 27   OK
rank d         1            -> 35   fig: 35   OK
C              2            -> 36   fig: 36   OK
dim entry      (1+1)+8+8=18 -> 38   fig: 38 / 40 / 48   OK
chan entry     (1+4)+2+(1+4)=12 -> 56  fig: 56 / 63     OK
index_encoding 1            -> 68   fig: 68   OK
entry_count    8            -> 69   fig: 69   OK
crc_of_crc     4            -> 77   fig: 77   OK
total                        = 81   fig: "The inline payload is 81 bytes"  OK
```

The prose gloss checks too: "Name and the nine scalars from layout through
channel count occupy 4 + 34 bytes" — layout 1 + lin 2 + codec 2 + filter 2 + A 8
+ S 8 + A_slab 8 + d 1 + C 2 = 34, and that is nine scalars. "the dimension
entry 18, the channel entry 12, and the trailing fixed fields 13 — 81 exactly."
4+34+18+12+13 = 81. Grid count ⌈100/32⌉ = 4, entry_count 4, extent length
4×20 + ⌈4/2¹⁶⌉×4 = 84. Fill `04 00 00 C0 7F` is length 4 plus 0x7FC00000
little-endian. The channel entry bytes `04 74 65 6D 70 0C 00` + `04 00 00 C0 7F`
concatenate to exactly §12.3's twelve bytes
`04 74 65 6D 70 0C 00 04 00 00 C0 7F`, so "§12.3's `temp` entry, byte for byte"
holds. Sample type 12 = float32 per §12.1's table. All correct.

### 2.3 Every other worked example

- §4.6 `température`: NFC `74 65 6D 70 C3 A9 72 61 74 75 72 65` is 11 characters
  in 12 bytes; NFD substitutes `65 CC 81` for `C3 A9`, giving 13. Correct.
- §5.1 smallest file: 16 + 4 + 44 = 64, trailer at 64, F = 128, F mod 64 = 0.
- §11.2: ⌈1024/256⌉=4, ⌈2048/256⌉=8, N=32, P=65,536; ⌈1000/256⌉=4. Correct.
- §11.4: (0,0)→0, (0,1)→1, (1,0)→8; (300,700)→tile (1,2), s=1·8+2=10; in-tile
  (44,188)→44·256+188=11,452; planar c=2 → 2·32+10=74. Correct.
- §12.1 bfloat16: 0x3F800000 high half = 0x3F80, stored `80 3F`; 0x7FC0 ↔
  binary32 0x7FC00000. Correct.
- §14.2: (2,3), P=6, uint8+uint16 → Q=3, 18 bytes; ordinal 5 at [15,18) with
  `b` at 16–17. Planar `b` = 6·2 = 12 bytes, ordinal 5 at 10–11. float32+bool →
  Q=5, 30 bytes, ordinal 5 at [25,30), `t` 25–28, `m` at 29. All correct; and
  the generalisation "channel c's value at in-tile ordinal u sits at byte
  u·Q + Fᶜ — the table's forms with k = u·C + c" is algebraically exact
  (k div C = u, k mod C = c).
- §14.3: P=10, alternating from true → bits 0–7 = 10101010₂ read LSB-first =
  0x55; values 8,9 = 1,0 → 0x01; pad bits 2–7 set gives 0x01|0xFC = 0xFD.
  Correct, and ⌈10/8⌉ = 2.
- §14.5: extents (5,5) tile (4,4) → grid 2×2; edge tile (1,1) covers 4–7 on
  both axes = 16 positions, 1 real + 15 padding; uint16 → 32 bytes; fill 0xABCD
  little-endian is `CD AB`. Correct, and in-tile ordinal 0 is indeed the real
  position (4,4).
- §15.4 (1,000,000 entries): ⌈10⁶/65536⌉ = 16 segments, 15 full + 16,960;
  array 64 bytes; region 20,000,064; k=999,999 → segment 15, segment-relative
  entry 16,959, byte 339,180; array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) = 339,200 bytes ≈ 339 KB; one full segment =
  65,536·20 = 1,310,720 = 1.25 MiB. All correct.
- §15.4 (planar): ordinal 74 → region bytes [1,480, 1,500); channel 3 →
  ordinals 96–127 = 32 entries. Correct.
- §16.2: N=32, S=8 → runs [0,8) [8,16) [16,24) [24,32); under row-major with
  G=(4,8) a run of 8 is one tile-row; viewport rows 1–2 = ordinals 8–23 = runs
  1 and 2. Correct.
- §17.3 byte-shuffle: 1.0/2.0/3.0 float32 little-endian are
  `00 00 80 3F | 00 00 00 40 | 00 00 40 40`; applying "byte i of group j to
  offset i·n + j" with s=4, n=3 gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`, exactly the figure. Correct.
- §20.3: 32·20 + 4 = 644; "one entry re-pointed, 31 byte-identical" is right for
  a single superseded tile; "about 20 MB of index" for 10⁶ tiles matches
  20,000,064. Correct.
- §21.9's Note: at 2³² entries the CRC array is 2³²/2¹⁶ × 4 = 2¹⁸ = 256 KiB and
  at 2³⁶ it is 2²² = 4 MiB; 65,536 layers × ~200 B ≈ 12.5 MiB. Correct.

### 2.4 Register census — the two counts §21 promises

I extracted the Instances column mechanically and applied §21.1's own counting
rule ("Instances within a cell are separated by semicolons, and a cell reading —
is one instance"):

```
rows        F 36   L 49   T 26   R 10   total 121
instances   F 58   L 116  T 55   R 44   total 273
```

§21.2 says "36 conditions", §21.3 "49", §21.4 "26", §21.5 "10", §21.8 "121
conditions over 273 instances". All five counts hold exactly. I also spot-checked
§21.1's stated instance discipline against thirty rows — the magnitude rule
(L21/L22/L30/T3/T14/T22 enumerate two directions; T21/L44/L2/F5 enumerate one),
the no-ordering rule (F14/F20/L37/L38/T1 are one), the nonzero-test rule
(L27/L28 are one), the single-predicate rule (F25/L20 are one), and the family
rule (T24 "any codec" one; T15 two; T25 three). Every one matches. This is the
tightest part of the document.

I also checked all 121 Governing-rule cells against the requirement each cites.
Every citation resolves and every one is apt, including the non-obvious ones —
L46/L47 cite `[R-CNT-12]` with `(R-CNT-13)`, and `[R-CNT-13]` is indeed where
"the record's governing scope" for a layer record and its sub-records is defined.

---

## 3. Building the thing

### 3.1 A complete file, written from the document alone

I built a real file rather than narrating. Layer `sst`, rank 1, dimension `x`
E=100 T=32, interleaved, one float32 channel `temp` with fill 0x7FC00000 — the
§7.4 example's layer, but with tiles 0 and 3 actually stored and tiles 1, 2
sentinel, so the index is not degenerate.

Derived: G = ⌈100/32⌉ = 4, N = 4, P = 32, Q = 4, decoded size P·Q = 128 (§14.2).
Codec 1, so `[R-COD-04]` forces each stored entry's length to 128. Tile 3 covers
x ∈ [96,128): 4 real positions and 28 padding positions, and `[R-SER-05]` fixes
each padding position's four bytes to the recorded fill.

Placement (free under `[R-SLB-05]`):

```
[0,16)      front signature block
[16,144)    tile 0 payload            128 bytes
[144,272)   tile 3 payload            128 bytes
[272,356)   tile-index region          84 bytes  = 4*20 + ceil(4/65536)*4
[356,465)   directory                 109 bytes  = 24 header + 81 inline + 4 CRC
[465,512)   pre-trailer pad            47 bytes  (pad to next 64 boundary)
[512,576)   trailer                    64 bytes
F = 576, F mod 64 = 0, dir_offset + dir_length = 465 <= F - 64 = 512
```

Index entries in disk-ordinal order: (16,128,crc0), sentinel, sentinel,
(144,128,crc3). One segment; segment CRC over the 80 entry bytes = 0xD8FC589C;
crc_of_crc_array = 0x38975D3F. Record header type 0x0001, flags 0b11 (MU=1,
PE=1 fixed by §7.3), inline_length 81, extent (272, 84).

Everything above is forced by the document. The only free choices were
placement, which `[R-SLB-05]` explicitly leaves free, and file_id, which §9.3
leaves to a random draw. **I had to guess nothing to write this file.** That is
a real result about the document: Part I plus §11–§17 is sufficient for a
writer.

### 3.2 A second build — planar bool + slab — to exercise the paths the first missed

Layer `mask`, rank 2, E = (5,5), T = (4,4) → G = (2,2), N = 4, P = 16. Planar,
C = 2: channel 0 `m` bool, channel 1 `v` uint16. Addressed tiles C·N = 8.

- channel 0 plane: packed, ⌈16/8⌉ = 2 bytes. P mod 8 = 0, so **no pad bits**,
  yet the edge tile at tile coords (1,1) has 15 padding *positions* out of 16 —
  exactly the case §14.3's Note calls out ("A plane can have many padding
  positions and no pad bits"). `[R-SER-05]` fixes those 15 bits to the fill bit.
  Determined.
- channel 1 plane: 16·2 = 32 bytes, value 0 real, values 1–15 the fill bytes.
- slab S=2, A_slab=512. `[R-SLB-02]` partitions per channel block: block [0,4)
  runs [0,2) and [2,4); block [4,8) runs [4,6) and [6,8). Placing at 512/514,
  1024/1026, 1536/1568, 2048/2080 satisfies `[R-SLB-03]` (each run's first
  stored tile A_slab-aligned, interiors packed). `[R-CNT-16]` forces A = 0.
- extent_length = 8·20 + 4 = 164; entry order groups channel-major per
  `[R-IDX-01]`.

Again nothing to guess.

### 3.3 Reader side — walking §19.1 → §19.3 → §19.4 over the built file

§19.1's four steps run without ambiguity. §19.3's layer-access list is
exhaustive enough that I could enumerate what to check without consulting §21,
and §19's preamble explicitly says the enumerations are not the inventory
(§21's register is), which is the right hedge and closes what would otherwise
be a completeness question about §19.1 step 4 (it cites `[R-ENC-12]` for the
layer name but not `[R-ENC-11]`, whose L3 row is also Detected=open).

§19.4's steps 1–8 are determinate. I checked the one asymmetry deliberately:
a point request at an out-of-extent coordinate **fails as a request**, while a
single-position *region* request at the same coordinate **succeeds and returns
nothing** — §19.4 step 1 plus the definition "a range whose every interval holds
a single position is a region request". That is stated, not an accident, and
§21.6's row restates it. Not a defect.

---

## 4. The four flagged sections, worked

### 4.1 §20.5 — compaction

**D5, the figure.** Input `front│A│▓│B│▓│A: index│▓│B: index│▓│dir│pad│tr`
with file_id X, generation 7; output `front│A│B│A: index′│B: index′│dir│pad│tr`
with file_id Y, generation 1. Consistent with `[R-WRT-06]` (fresh file_id,
generation 1) and with `[R-WRT-07]` (relocation re-points slots, regenerates
each relocated index region, ′ marks). The figure also does the job §5.1's
figure defers to it for — showing a layer whose tiles and index are *not*
contiguous (A's tiles and A's index are separated by B's tiles) — so §5.1's
"§20.5's figure shows the general case" is honest. The output still carries a
`pad`, which is slack; that does not contradict "slack is never carried", whose
subject is the *input's* slack.

**The two-modal sentence.** §21.7's new entry is the one that assigns two BCP 14
modals to two clauses of one rule: "the unknown ignore-lane bits it MUST carry
forward, and the floor its version_minor SHOULD take". I checked the casing
discipline §2.1 imposes on the corresponding §6.3 clause: §6.3's sentence about
compactors reads "A compactor … *carries* the input's unknown ignore-lane bits
into its output trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`)" —
lowercase, no keyword, so it has no force of its own and §20.5's MUST governs.
That is consistent, not a conflict.

**The closed two-item enumeration and its argument.** §20.5:

> Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's

I tested the closure claim vehicle by vehicle against §10.1's list.

- Vehicle 3 (new ignore-lane flag bits): §21.6 row "An ignore-lane flag bit
  (16–31) is set → Ignored; the file is conforming". Conforming. ✔
- Vehicle 4 (new standardized user-metadata keys): §18.3/§18.4 make these
  `tarn.`-prefixed, and §21.6's row "A user-metadata document carries an
  unrecognized `tarn.`-prefixed key → Conforming". ✔
- Vehicle 1 (new record types): under this text any such value lies in
  0x0003–0x7FFF, registered as a violation by F36 (top level) and L25
  (sub-record), so an input carrying one is **not conforming under this text**
  and the premise "on a conforming input" excludes it. ✔
- Vehicle 2 (new values in reserved ranges): every one of §10.2's eight spaces
  registers its reserved range as a violation — record type F36/L25, channel
  layout L36, linearization L33, sample type L34, codec L43, filter L45, index
  encoding L31, metadata encoding R1. Again excluded by the premise. ✔

So the enumeration is genuinely closed at two, and the argument is sound. I also
checked the near-miss: an **experimental-range** MU=0 record type is conforming
(§21.6) and is a feature the compactor does not implement — but it is not "a
feature a later minor defines", since experimental values are private use
(§10.3), so it falls outside the sentence's own scope. Correct.

The one thing I would fix: the parenthetical "(F36, L25, R1)" names three of the
nine rows that carry the claim, omitting L31, L33, L34, L36, L43, L45. The
sentence makes no exhaustiveness promise, so I am **not** filing this as a
finding; recording it here because I checked it and someone will check it again.

**"regenerates each relocated tile-index region".** I probed whether the trigger
is the right one. Two edge cases:

1. A region that *is* relocated but whose tiles are not — the parenthetical
   "entry offsets new" is then false for that region, but the next paragraph
   ("every other entry is re-pointed to where its stored extent **now** lies")
   resolves it to a no-op re-point. Determined.
2. A region that is *not* relocated (placed at its input offset) but whose tiles
   are — read narrowly, the "relocated region" clause would not fire and
   `[R-WRT-05]`'s byte-identical re-emission would copy stale offsets. But
   `[R-WRT-07]`'s closing sentence, "The output's reference arrays MUST equal
   the live generation's bit for bit", forbids the result outright, and the
   stale offsets would also trip `[R-CNT-13]`'s ownership rule or the entries'
   crcs. Determined by other rules; the phrasing is loose but nothing forks.

Not filing either.

**The refusal ladder.** "A compactor MUST refuse to compact when any check
`[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a violation it has
detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor
keep it and call the output clean." Then the structural-reject-tile entry case:
`[R-IDX-03]` gives such an entry no stored extent to re-point to, so regenerating
the region cannot proceed past it, and no drop is available because a tile-index
entry is no record §20.4's table licenses dropping. That chain closes. I also
checked that a compactor cannot escape `[R-SLB-04]` by clearing a slab
declaration: clearing would modify a retained layer record's inline payload,
which `[R-WRT-05]` forbids and §20.5's exception list (extent slots,
crc_of_crc_array) does not license. So a compactor must re-establish the slab
invariants. Determined.

### 4.2 §21.7 — what no check detects

Checked the new entry's claim of unwitnessedness: a compacted output's trailer
carries flags and version_minor but no record of the *input's* flags or minor,
so neither obligation has a witness in the output alone. Correct.

Checked the older clauses in the same paragraph that the new one hangs off:
"a change that reaches the decoded size instead is witnessed by T3 or T14 …
T14 the entry's declared length, T3 the decoded payload's own" — correct, those
are the two length tests and they are distinct. "a change that reaches the codec
is witnessed by the rows for the codec now declared, which test the stored bytes
as a stream of it (T15, T17, T23, T25), or by T14 where the new declaration is
codec 1" — correct; a filter change, not mentioned, falls under the paragraph's
leading clause (witnessed only where it reaches a byte §14 structurally
constrains), which is where it belongs.

One asymmetry I noted and decided is not a defect: the version_minor half of the
new entry is a **SHOULD**, and `[R-CNF-12]` already puts SHOULD deviation outside
the register entirely, so §21.7's stated reason ("a single file exhibits no
witness") is a second, redundant reason rather than the operative one. Both are
true, and stating the redundant one costs nothing.

### 4.3 §23.1 — deletion is not erasure

This is where I had to decide something. See **diagrams-01** below. Everything
else in §23.1 checks: the bytes do remain as slack (`[R-CNT-21]`); an earlier
trailer *is* recoverable by §9.6's backward probe for every case §23.1 names;
"no commit removes a layer at all" matches §20.4's closing paragraph; and
`[R-PRV-01]`'s widened scope ("any commit that makes sample data unreachable")
is what keeps the requirement safe regardless of how the preceding enumeration
is read.

### 4.4 Appendix G — the reproducible-writer profile

I treated this as a checklist and asked the only question that matters: **does
following items 1–10 actually pin every byte?** I walked the whole emitted file:

- trailer: magic fixed; version_major 1; version_minor by item 8; flags 0 by
  item 8; generation 1 by item 4; file_id by item 2; committed_file_length,
  dir_offset, dir_length derived; reserved 0; CRC derived. ✔
- directory: record order pinned by item 3; each record's flags fixed by §7.3;
  inline_length derived; layer-record fields derived from content except
  alignment/slab (item 5), fill (item 7) and names (item 10). ✔
- index regions: entry_count, entry order, segment CRCs, crc_of_crc_array all
  derived; which tiles are sentinel pinned by item 6. ✔
- tile payloads: decoded image derived from content; padding and pad bits fixed
  by `[R-SER-05]`; filter pinned by item 5; codec pinned by item 1. ✔
- placement: first structure at 16 (or the least position a declared alignment
  admits), each later one where the previous ended, gaps only where alignment or
  the 64-byte trailer alignment forces them, every gap byte zero. ✔

I looked hard for circularity in item 3's ordering key and found none: the key
is type, then layer name for 0x0001, then "the record's header with
**extent_offset masked to zero**, then its inline payload, then the contents of
its extent". extent_offset is the only placement-dependent component and it is
masked; extent_length, flags, inline payload and extent content are all
functions of content. The text says exactly this and says why. The tie case is
handled ("Two records this key does not separate are byte-identical … so the
writer chooses"). I could not find a residual degree of freedom.

**The carve-out.** Item 2's "This is a creator's rule: a compactor adopting the
profile takes `[R-WRT-06]`'s fresh draw instead, since a derived value is not a
draw and re-deriving it on an already-compact input would reproduce the input's
own `file_id`." I tested that reasoning: for a profile-conforming input that is
already compact and already in the profile's emission order, the compactor's
output bytes [0, F−64) and the trailer's other fields are identical to the
input's, so the item-2 hash would reproduce the input's file_id — which
`[R-WRT-06]` forbids ("a new draw … not merely a value compared against the
input's"). The carve-out is necessary and the argument for it is correct.

**The concession.** Item 8's "A compactor's output is therefore reproducible only
modulo its trailer". I checked the scope: file_id, version_minor and flags appear
nowhere but the trailer, and each feeds only the trailer CRC. So "modulo its
trailer" is exactly right, neither more nor less. Correct.

Item 8's citation of `[R-CNT-08]` for the compactor's carry-forward points at a
clause that is lowercase in §6.3 and whose MUST lives in `[R-WRT-06]`; §6.3 does
forward-cite `[R-WRT-06]`, so the trail closes. Noted, not filed.

---

## 5. The rest of the document — where the marginal value is

### 5.1 §8.1's coverage map against §4.5's exception list

§4.5 names three exception classes; §8.1's table has seven rows. I audited every
field of every structure for exactly-one-checksum coverage:

- trailer [0,60) ← trailer CRC; trailer CRC terminal, uncovered. ✔
- directory record sequence ← directory CRC; directory CRC terminal. ✔
- every layer-record field, including crc_of_crc_array, lies inside the
  directory ← directory CRC ("both comparison-verified and covered by exactly
  one further checksum"). ✔
- segment CRC array ← crc_of_crc_array. ✔
- index entries, including each entry's crc field ← segment CRC. ✔
- stored tile bytes ← entry crc. ✔
- user-metadata extent bytes ← extent terminal CRC; that CRC terminal. ✔
- unassigned-type record extent ← none, declared in both §4.5 and §8.1. ✔

No field escapes and no field is doubly covered. §8.2's chain of trust orders the
same links correctly. This map is sound.

### 5.2 §6.2's trailer box against `[R-CNT-24]`'s cross-major promise

Offsets 0,8,10,12,16,24,32,40,48,56,60 with sizes 8,2,2,4,8,8,8,8,8,4,4 tile
[0,64) exactly with no hole, so "The format-major-1 trailer has zero slack:
every byte is assigned" is literally true. `[R-CNT-24]` fixes magic at F−64,
version_major/minor at F−56 and the CRC at F−4 over [F−64, F−4): that is trailer
offsets 0, 8/10 and 60 over [0,60), matching B2 exactly. The residual a future
major may redefine is 64 − 8 − 4 − 4 = 48, which is the number `[R-CNT-24]`
states. Correct.

Front block: 0x89, "TARN" = `54 41 52 41`… checked byte by byte: `54 41 52 4E`
is T,A,R,N; trailer magic `4E 52 41 54` is N,R,A,T, i.e. "NRAT"; first bytes
0x89 vs 0x8A differ, so §6.2's Note ("a recovery scan never matches the front
block") holds. Appendix B restates both constants correctly.

### 5.3 §15.3's entry-validity table

Eleven rows. Six carry the *structural* marker — rows 2 through 7 — and
`[R-IDX-03]` says "Six rows are marked *structural*". Counted: correct. Each row
maps to exactly one §21.4 row (T6, T7, T10, T8, T11, T9+T12, T1) with the
verifier rows mapping to L18, F33, and L40/L41/L42. No row is unregistered and
no register row lacks a table row.

I checked the boundary the table leaves implicit: a non-sentinel offset of
exactly 2⁶³−1 passes row 6 and is then caught by row 7's overflow clause. The
table classifies error states only; a well-formed entry falls through, which is
the right shape.

### 5.4 §10.2's identifier-space table

Eight rows, each cross-checked against the section that owns the space:
record type (§7.2/§7.3), channel layout (§14.1: "values 3 through 255 are
reserved"), linearization (§11.4: 2–3 then 4–0x7FFF, i.e. 2–0x7FFF reserved),
sample type (§12.2), codec (§17.2), filter (§17.3), index encoding (§7.4),
metadata encoding (§18.2). All eight agree. "Value 0 is invalid in every space
above" — verified in all eight owning sections. Appendix C's snapshot agrees with
all of them and with §12.1's thirteen types and §18.4's six keys.

### 5.5 §21.9's guarantees against Appendix B's restatement

All eight rows restated in Appendix B's "Reader minimum guarantees" cell, in the
same order and with the same values. Appendix B's other 24 rows each check out
against the section they cite. §21.9's hard-limits paragraph explicitly
disclaims being an inventory ("a finding aid rather than an inventory"), which
is why the user-metadata `extent_length ≥ 5` hard limit appearing in Appendix B
but not in §21.9's list is not a defect.

### 5.6 §21.1's specialization claim

"F1 of F6 and of F8, F35 of F36, L24 of L25" — all three verified as strict
containments with consistent detector/detection-point. The sentence says "Some
rows", so I did not treat it as exhaustive; I did check the obvious unlisted
candidate, T14 ⊂ T3 under codec 1, and confirmed §24's multi-row provision
("the entry records every row the file exercises and says which it was built
for") already handles overlaps.

### 5.7 Appendix H's five checklists

Reader/writer/updater/verifier/file each walked against §2.3. The verifier
checklist is complete against §2.3 and against every verifier-detected register
row (F7, F25–F28, F33, F36, L18, L25, L40–L42, L46–L49, T2, T4, T5, T26). The
writer and updater checklists are faithful. The file checklist is faithful. The
reader checklist is the one that drifts — see **diagrams-04**.

### 5.8 §17.2's zstd Note

"with Single_Segment_Flag set there is no Window_Descriptor and Window_Size is
the frame content size, which this requirement already obliges to equal the
decoded size; without it, the Window_Descriptor cannot express less than 1 KiB.
A tile whose decoded size is below 1 KiB — §14.2's worked examples give 18 and
30 bytes, §14.3's gives 2 — is therefore encodable under codec 3 only as a
single-segment frame". Cross-checked the cited example sizes: §14.2 gives 18 and
30 (it also gives 12 for the planar case, which the Note does not need), §14.3
gives 2. The argument is internally valid given the RFC facts it asserts, and
`[R-COD-06]`'s "declare a window size" reads on the declared value, so the
document is determinate here. Not a defect.

### 5.9 Counts asserted in prose

- §22.2 "Three properties" — decoded size from declarations, overflow-checked
  sums, nothing acted on before its checksum. Three. ✔
- §22.3 "Four residues" — slack; unassigned-type extents; trailer mimics;
  user-metadata extents under an unassigned encoding. Four. ✔
- §18.2 "Four restrictions" — object/unmarked, finite numbers, no duplicate
  keys, well-formed UTF-8. Four. ✔
- §10.1 "exactly four vehicles" — four numbered items, and §4.3 names the same
  four. ✔
- §12.1 "exactly thirteen sample types … The twelve types other than bool are
  this specification's numeric types". 13 rows, 12 non-bool. ✔
- §17.2 "Three frame features are excluded" — dictionary, content-checksum flag,
  oversized window, which are the three constraints in the sentences that
  follow. Three, though the referents take a second reading to fix. Not filed.
- §21.2's preamble "Four rows are outside that reasoning" — F1, F6, F8, F14.
  Four. But see **diagrams-03**.

---

## 6. Findings

### diagrams-01 — AMBIGUITY — §23.1's "two ways" is a closed count over a word the document uses two ways

**Location.** §23.1, `[R-PRV-01]`; reads against §20.3 step 4 (`[R-WRT-04]`),
§3.1 and §23.2 (`[R-PRV-03]`).

**Quotation.** §23.1:

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

**The problem.** A commit has a third effect on stored sample data that is
neither of these under §20.3's own vocabulary: writing the **sentinel** for a
tile that was stored in the superseded generation, with the layer's extents
unchanged. §20.3 step 4 keeps the three apart in one clause:

> with entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel

"tiles this commit … supersedes" and "tiles that become unstored" are named as
different populations there. An unstored tile is not de-addressed either — the
grid count is unchanged, the entry is still in the index, and the tile still
reads (as fill). So on §20.3's reading of "supersede", §23.1's "two ways" is a
count of two over a set of three.

§23.2 relies on the missing case and points back here for it:

> a tile unstored by a later commit leaves its earlier payload in the file as
> slack (§23.1)

**Permitted readings.** (a) *Narrow* — "superseding it" means what §20.3 step 4
means: replacing a stored tile's payload. Then unstoring is a third way and the
"two ways" claim is false, and §23.2's cross-reference lands on an enumeration
that does not contain its case. (b) *Broad* — "superseding" means making
previously live bytes non-live, the sense §1 uses ("Superseded bytes remain as
slack until compaction reclaims them"), §5.2 uses ("everything an earlier commit
superseded"), and — decisively — §3.1 uses of exactly this case: "Superseded
payload bytes from earlier generations do not make a tile stored." Under (b) the
enumeration is complete.

**Which I picked and why.** (b). §3.1's sentence is about a tile whose live entry
is the sentinel and whose earlier payload is still in the file, and it calls
those bytes "superseded" — that is the unstoring case named in the document's
own terminology section, and terminology governs. But the choice is a guess I
had to make, and a reader who arrives from §20.3 step 4 will make the other one.

**What an implementer does wrong without it.** Nothing to the bytes.
`[R-PRV-01]`'s own scope is "any commit that makes sample data unreachable",
which covers unstoring however the preceding sentence is read, so a tool built
from the requirement rather than the enumeration behaves correctly. The cost is
to the enumeration's usefulness as a checklist: a privacy audit built from
§23.1's two ways would omit the case §23.2 says is the one that "publishes which
regions were written". The fix is one word — naming unstoring, or saying
"superseding it (its payload replaced, or the tile unstored)".

**Byte-level: no.** `[R-PRV-01]` binds how a writer *represents* a commit to its
caller, not what it emits; no byte and no accept/reject verdict turns on it.

---

### diagrams-02 — CONTRADICTION — §20.4's preservation table states MUST-level obligations with no requirement identifier, against §2.2's rule that requirements carry them

**Location.** §2.2; §20.4's table (between `[R-WRT-05]` and `[R-WRT-08]`); §6.1;
consequence visible in §21.6's row for an unassigned record type.

**Quotation.** §2.2:

> Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`.
> Identifiers are stable: they are never renumbered or reused …

§20.4's table, MU = 0 / PE = 0 row:

> Retain byte-identical, or drop it — its extent becoming slack. An appender
> MUST NOT drop it except in a commit that *independently* changes the scope the
> record attaches to … Dropping the record, or dropping another record in the
> same commit, is not itself such a change, so a commit whose only effect would
> be the drop MUST retain it.

and the MU = 1 row:

> Retain byte-identical. The updater MUST NOT modify the scope the record
> governs.

**The problem.** §2.2 is normative text (`[R-CNF-01]` exempts only §1, labelled
Notes/Examples/Rationale, and non-normative appendices), and it asserts that
normative requirements carry identifiers. §20.4's table carries at least three
MUST-level obligations and none of them does. I checked the whole subsection
mechanically: between `[R-WRT-05]` at the end of §20.4's first paragraph and
`[R-WRT-08]` at the end of its last, the paragraph introducing the table, the
table itself, and the paragraph "No commit therefore removes a layer record, or
a user-metadata record at either scope" carry no closing identifier. The same
holds for §6.1's

> Writers MUST emit exactly these 16 bytes.

which is the file-level source of the front-block constant that F6 registers —
F6 cites `[R-CNT-04]`, which binds only readers, and only readers holding the
bytes resident.

**That this is load-bearing, not cosmetic, shows in the citations it forces.**
Everything that needs to point at these obligations points at a section instead:
`[R-CNF-06]` ("MUST honor the preservation obligations of §20.4"), §2.4's
preserve-verbatim row ("§20.4's table states the cases"), §20.5 ("only where
§20.4's table licenses it"), Appendix H's updater checklist ("(§20.4,
`[R-CNT-22]`)"). And in one place the absence produces a wrong citation —
§21.6's table:

> | A record type this specification has not assigned, from the experimental
> range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
> per its PE bit; … | `[R-CNT-15]`, `[R-WRT-08]` |

`[R-WRT-08]` says only "An updater MUST NOT re-encode a record whose type it does
not implement, and MUST NOT modify one except by relocating its extent and
re-pointing its slot under §20.5". It does not state "preserved or dropped per
its PE bit"; §20.4's unidentified table does. The row cites the nearest
identifier because the right one does not exist.

**What an implementer does wrong without it.** Nothing to the bytes — the
obligations are findable by section. The cost falls on anyone doing requirement
coverage against this document, and on the corpus: `[R-VEC-02]` requires a vector
to name "that row's governing requirement identifier — row labels are positional
and renumber when a row is struck, while §2.2 makes the identifier permanent",
and these obligations have no permanent handle at all. §2.4 already treats
preserve-verbatim as a first-class outcome class alongside the four reader
outcomes, each of which is identified.

**Byte-level: no.** Assigning an identifier changes no byte and no verdict. The
obligations themselves are already stated; only their handle is missing.

---

### diagrams-03 — AMBIGUITY — §21.2's preamble excludes F5 from the rows that reach a foreign-major file, but its stated reason does not reach `[R-CNT-27]`

**Location.** §21.2's preamble; F5; `[R-CNT-27]` (§5.1); §19.1 step 1
(`[R-RDR-01]`); §2.3 (`[R-CNF-02]`).

**Quotation.** §21.2:

> A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below whose
> subject is that file's *geometry* do not reach it: §6.2 puts the version gate
> ahead of every check but the trailer magic and the trailer CRC, so such a file
> is refused on capability grounds first. Four rows are outside that reasoning
> and do reach it, because their subject is a field fixed across every major
> (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC — the
> two checks §6.2 places before the gate — and F6 with F1's front-block
> instance, which `[R-CNT-04]` places before other processing.

against `[R-CNT-27]` (§5.1):

> No conforming file is shorter than 128 bytes … A reader MUST treat a shorter
> file as a validity error at file scope.

and F5, whose Instances cell is "F (physical file size); committed_file_length"
with Detected = *open*.

**The problem.** The preamble's reason is an ordering argument about §6.2's gate
sequence. `[R-CNT-27]`'s check is not one of §6.2's gates; it is a check on the
physical file size, and §19.1 puts the physical size at **step 1**, before the
trailer is fetched at step 2:

> 1. **End of file.** Obtain the transport-authoritative file size F
>    (`[R-CNT-10]`).

So for F5's *physical file size* instance the version gate is not "ahead"; it is
strictly behind. The preamble's conclusion (only four rows reach) and its reason
disagree about F5.

**A witness.** F = 80. Bytes [0,16) are the front signature block exactly. Bytes
[16,80) hold the trailer magic at 16, a valid trailer CRC at 76,
committed_file_length = 80, and version_major = 7. A reader:

- §19.1 step 1 gives F = 80. `[R-CNT-27]` is satisfiable here and fails: 80 < 128
  → F5, reject-file, file-scope.
- `[R-CNT-04]` passes (the front block is correct), so F6/F1 do not fire.
- §6.2's order then gives magic ✓, CRC ✓, version gate → major 7 unimplemented →
  refusal on capability grounds, which §2.3 says "is not a finding about its
  bytes".

The later gates (dir_offset ≥ 16, dir_offset + dir_length ≤ F − 64, F mod 64 = 0)
are never reached because they sit behind the version gate, so the file cannot be
disqualified by them either.

**Permitted readings.** (a) F5 does not reach the file: §2.3 says a foreign-major
file is "neither conforming nor nonconforming", `[R-CNT-27]`'s own derivation is
major-1-specific (it is built from §6.2's dir_offset ≥ 16, dir_length ≥ 4 and the
64-alignment, none of which `[R-CNT-24]` fixes across majors), and §21.2's
preamble names four exceptions and F5 is not among them. A verifier reports
*cannot establish*. (b) F5 does reach it: `[R-CNT-27]`'s MUST is unqualified,
its subject is available at §19.1 step 1 before any version-dependent field is
read, and F5's Detected cell says *open*. A verifier reports *nonconforming*,
and §2.3's "An established violation takes priority" then forecloses *cannot
establish*.

**Which I picked and why.** (a). §2.3's "neither conforming nor nonconforming"
is the stronger, more general rule, and §21.2's preamble reaches the same
conclusion. But I picked it against the preamble's own stated reason, which is
false for this row, and against F5's Detected cell.

**What an implementer does wrong without it.** A verifier built from §19.1's
step order plus `[R-CNT-27]` returns *nonconforming* where one built from §2.3
returns *cannot establish*, on the same 80 bytes. §24 requires a vector to record
"whether the file is **conforming**", so a corpus entry for a short foreign-major
file cannot be written without choosing. The fix is one clause: either add F5's
physical-size instance to the four exceptions, or say in §5.1 that the 128-byte
floor is a format-major-1 minimum that a reader applies only after the version
gate.

**Byte-level: no**, and I want to be explicit about why rather than reach. Both
implementations refuse the file, and both are barred from certifying it, so no
byte is emitted differently and no accept/reject verdict differs. What differs is
the *label* on a verifier's refusal (*nonconforming* vs *cannot establish*) and
the diagnostic §6.3 asks to be distinct. That is a real interoperability
difference in a conformance report but it is not the emittable set and it is not
accept/reject.

---

### diagrams-04 — OBSERVATION — Appendix H's conforming-reader checklist states the acceptance duty wider than §2.3 and than the rule it cites

**Location.** Appendix H, "Conforming reader"; §2.3 (`[R-CNF-03]`); §21.9
(`[R-ERR-04]`); §21.6's closing paragraph.

**Quotation.** Appendix H:

> **Conforming reader** — … accepts every conforming file within §21.9's minimum
> guarantees and reports any resource refusal as a limit rather than as
> corruption (`[R-ERR-04]`); …

against §2.3:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 … and none of whose values exceeds the minimum guarantees
> of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on that last
> ground; §21.6's closing paragraph names the other two)

and against the rule the checklist actually cites, `[R-ERR-04]`:

> Software that declines **on that ground** a file whose every quantity lies
> within the table is not a conforming reader (`[R-CNF-03]`) — the two capability
> refusals §21.6 names, a foreign format major and an unimplemented MU = 1 type,
> are not this ground

**The problem.** §2.3's acceptance duty carries three qualifiers; the checklist
keeps one. The two it drops are exactly the two §21.6 devotes a closing paragraph
to and calls "conforming files a reader nevertheless refuses": a file declaring a
format major the reader does not implement, and a conforming file carrying an
experimental-range record type with MU = 1, which `[R-CNT-15]` *obliges* the
reader to reject. The checklist as written says a conforming reader accepts both.

This is the narrower/wider class rather than a stale restatement: the entry is
wider than the rule, and it is wider than the very requirement it cites, whose
sentence contains the carve-out verbatim. Appendix H does open with "each entry's
authority is the requirement or section cited, never this summary", which is the
disclaimer that keeps this from being decidable-in-two-ways; but the entry's
cited authority is `[R-ERR-04]`, and a reader who follows the citation finds the
carve-out and a reader who does not finds a duty their conforming reader fails.

**What an implementer does wrong without it.** An implementer auditing their own
reader against the checklist — which is precisely what Appendix H says it is
for, "for implementers auditing their own work" — concludes that refusing a
format-major-7 file makes them nonconforming, and that rejecting an
experimental-range MU = 1 record makes them nonconforming, when §21.6 says the
first is licensed and `[R-CNT-15]` says the second is required. The fix is a
clause: "accepts every conforming file of a major it implements, within §21.9's
minimum guarantees, save the two capability refusals §21.6 names".

**Byte-level: no.** §2.3 and `[R-ERR-04]` both state the carve-outs and Appendix
H is non-normative and says so; a reader built from the normative text behaves
correctly, and no byte or verdict is open.

---

### diagrams-05 — OBSERVATION — §18.2's byte-layout box gives "Valid values | 1 or 2" for the one enumerator space where an unassigned value leaves the file conforming

**Location.** §18.2's layout table (`[R-MTA-03]`); §10.3 (`[R-EXT-03]`); §21.6;
§18.2's `[R-MTA-10]`.

**Quotation.** §18.2:

> | Offset | Size | Type | Field | Class | Valid values |
> |---|---|---|---|---|---|
> | 0 | 1 | u8 | encoding | structural | 1 or 2; see below |

against §21.6:

> | A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming — §10.3's
> prohibition binds a writer's conduct, not the bytes. No document rule attaches
> at such an encoding, so a verifier certifies, reporting the record it ignored |

**The problem.** In every other layout box in this document, a "Valid values"
cell delimits validity, and a value outside it is a validity error at the owning
scope — §6.2's rows are all reject-file conditions, §15.1's cells defer to
§15.3's error classification, and §7.4's cells for codec/layout/filter/type all
mean "anything else is reject-layer". §18.2's encoding byte is the sole
enumerator in the document where a value outside the assigned set does **not**
make the file invalid: an experimental-range value is ignore-record and the file
stays conforming, and `[R-MTA-10]` goes further and requires the verifier to
certify while naming the record it ignored. The cell reads "1 or 2" in the same
column that means "or the file is invalid" everywhere else.

The cell does say "see below", and below is unambiguous ("values ≥ 0x80 are the
experimental range (§10)"), and §10.3, §21.6 and `[R-MTA-10]` each say the same
thing independently. Compare §6.2's version_major cell, which hedges inside the
cell — "1 (0 invalid; others: §6.3)" — precisely because the same trap exists
there. §18.2's cell does not.

**What an implementer does wrong without it.** A verifier written from the box
reports *nonconforming* for a record declaring encoding 0x85 and refuses to
certify, where §21.6 and `[R-MTA-10]` require it to certify and to report the
record instead. That would be a certification fork if the text were ambiguous —
it is not; four places outside the box decide it, so this is a table that
misleads rather than a rule that is open. The fix is the parenthesis §6.2
already uses: "1 or 2 (0 and 3–0x7F are violations, R1; ≥ 0x80 is conforming and
ignore-record, §21.6)".

**Byte-level: no.** The prose immediately below the table, §10.3, §21.6 and
`[R-MTA-10]` all decide the question in the same direction, so a competent
implementation reading past the box does not diverge.

---

## 7. Coverage statement, and what I could not determine

Every item in §1.1's inventory was examined. Every number in every worked
example was recomputed independently, not eyeballed; every CRC constant in the
document was reproduced from §4.5's parameters; Appendix A was verified byte for
byte including its trailer CRC; both register counts (121 rows, 273 instances)
were recomputed mechanically and hold; all 121 Governing-rule citations were
resolved and checked for aptness; §8.1's coverage map was audited field by field
for exactly-one-checksum coverage.

Two things I checked and could **not** settle from this document alone, recorded
so nobody has to repeat the work:

1. §17.2's Note asserts that RFC 8878 "derives a frame's Window_Size two ways"
   and that the Window_Descriptor "cannot express less than 1 KiB". Those are
   claims about a pinned external reference (Appendix F pins RFC 8878), so they
   are outside what this document can be checked against. `[R-COD-06]`'s
   "declare a window size" reads on the value the frame header declares, which is
   determinate; the Note's arithmetic about tiles below 1 KiB is then internally
   consistent with §14.2's and §14.3's example sizes, which I did verify.
2. §17.2's "Three frame features are excluded" — the three referents are
   recoverable from the sentences that follow (dictionary, content-checksum flag,
   oversized window) but the sentence immediately before it also excludes
   skippable frames and second frames, so the count takes a second reading to
   bind. Not filed: R4's twelve instances and T17–T22 pin the actual constraint
   set unambiguously.

Confidence that an implementation built from this text alone would interoperate:
**high**. I wrote two complete files and a reader walk from the document and had
to guess nothing about bytes. All five findings are documentation-integrity
defects — a closed count over an ambiguous word, three MUSTs without a handle, a
preamble whose reason does not reach one of its rows, a checklist wider than its
own citation, and a table cell narrower than its own rule. None of them opens the
emittable set or a reader's accept/reject verdict. Zero byte-level.
