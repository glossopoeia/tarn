# Round 20 — Diagram auditor — verbatim working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,369 lines), in four `Read` calls covering lines 1–400, 400–849, 850–1299,
1300–1749, 1750–2199, 2200–2649, 2650–3099, 3100–3549, 3550–3999, 3999–4369 —
i.e. the whole document. I ran `wc -l` and three `grep` invocations against that
same file. I wrote and ran four Python scripts in my own scratchpad
(`crc.py`, `crc2.py`, `build.py`, plus inline heredocs) which read **no** project
files except that they re-parse hex dumps I transcribed by hand out of the
specification. I opened no ADR, no `docs/`, no `conformance/`, no
`spec/registry.json`, no git history, no web resource, and I listed no
directory.

**Context I did not ask for.** My runtime placed a `claudeMd` block and a
memory index in my context before I began, naming project working practice and
prior positions, and a task list naming this round's number. I did not read the
files it pointed at and I have not used any of its content as evidence. I state
that it appeared because the brief requires me to; I am not repeating what it
said. Everything below is derived from `spec/tarn.md` alone.

---

## 1. Method

The charter is: enumerate every figure, byte-layout box, table, worked example
and checklist first, *then* judge each. So the first section below is the
enumeration with line numbers, and the second is the walk.

I then built the format end to end — a minimal file and a one-layer file — from
the document alone, and recomputed every checksum the document quotes.

---

## 2. Enumeration

### 2.1 Tables (24)

| # | Line | Table |
|---|---|---|
| T-01 | 235–241 | §2.4 outcome classes (5 rows) |
| T-02 | 697–700 | §6.1 front signature block layout |
| T-03 | 740–752 | §6.2 trailer layout (11 rows) |
| T-04 | 904–910 | §7.2 record header layout (5 rows) |
| T-05 | 977–980 | §7.3 record types of format major 1 |
| T-06 | 1006–1023 | §7.4 layer record inline payload (16 rows) |
| T-07 | 1123–1131 | §8.1 checksum coverage map (7 rows) |
| T-08 | 1397–1406 | §10.2 numeric identifier spaces (8 rows) |
| T-09 | 1601–1615 | §12.1 sample types (13 rows) |
| T-10 | 1833–1836 | §14.2 byte layout / decoded size (2 rows) |
| T-11 | 2001–2005 | §15.1 tile-index entry layout (3 rows) |
| T-12 | 2049–2061 | §15.3 entry validity (11 rows) |
| T-13 | 2441–2443 | §18.2 user-metadata encoding field |
| T-14 | 2590–2597 | §18.4 standardized keys (6 rows) |
| T-15 | 3121–3125 | §20.4 updater obligations by stored flags (3 rows) |
| T-16 | 3369–3406 | §21.2 file-scope register (36 rows) |
| T-17 | 3413–3463 | §21.3 layer-scope register (49 rows) |
| T-18 | 3470–3497 | §21.4 tile-scope register (26 rows) |
| T-19 | 3519–3530 | §21.5 ignored-record register (10 rows) |
| T-20 | 3537–3552 | §21.6 conditions that are not violations (14 rows) |
| T-21 | 3659–3668 | §21.9 minimum guarantees (8 rows) |
| T-22 | 4001–4017 | Appendix A annotated byte table (13 rows) |
| T-23 | 4037–4065 | Appendix B constants (27 rows) |
| T-24 | 4134–4136 | Appendix E changelog (1 row) |

### 2.2 ASCII figures and byte-layout boxes (8)

| # | Line | Figure |
|---|---|---|
| F-01 | 587–592 | §5.1 a file after three commits |
| F-02 | 1071–1090 | §7.4 the 81-byte layer-record payload, annotated by offset |
| F-03 | 1202–1211 | §9.2 what a crash sees (three rows) |
| F-04 | 1996–1997 | §15.1 tile-index region blockquote box |
| F-05 | 3052–3056 | §20.3 shape (a): a new layer |
| F-06 | 3068–3072 | §20.3 shape (b): tiles added to an existing layer |
| F-07 | 3092–3095 | §20.3 shape (c): a change confined to the directory |
| F-08 | 3232–3238 | §20.5 what compaction reclaims |
| F-09 | 3990–3999 | Appendix A hex dump of the 128-byte minimal file |

(That is nine; I mis-stated the count as eight when I first wrote the heading
and am leaving the correction visible rather than renumbering.)

### 2.3 Worked examples (28)

Located by `grep -n '^\s*>\s*\*\*\(Example\|Note\|Rationale\)'`. The
Example-labelled ones, which are the arithmetic-bearing ones:

513 (§4.6 `température`), 577 (§5.1 smallest file), 584 (§5.1 three commits),
1060 (§7.4 complete layer record payload), 1198 (§9.2 crash), 1518 (§11.2 grid),
1572 (§11.4 ordinals), 1635 (§12.1 bfloat16), 1684 (§12.3 channel entry),
1754 (§13.3 rgb fill), 1875 (§14.2 interleaved offsets), 1909 (§14.3 packed
bool), 1965 (§14.5 padding content), 2089 (§15.4 million-entry index),
2104 (§15.4 planar disk ordinals), 2203 (§16.2 slab runs), 2384 (§17.3
byte-shuffle), 3038 (§20.3 supersede cost), 3047 (§20.3 three shapes),
3229 (§20.5 compaction).

Plus the Notes carrying arithmetic: 2298 (§17.2 zstd window derivations),
2834 (§19.4 planar all-channel spacing), 3030 (§20.3 index cost),
3682 (§21.9 where the numbers come from).

### 2.4 Checklists and numbered lists

- §9.2 commit protocol, steps 1–6 (lines 1168–1180)
- §10.1 four extension vehicles, items 1–4 (1377–1381)
- §19.1 open algorithm, steps 1–4 (2652–2695)
- §19.4 tile-read algorithm, steps 1–8 (2781–2832)
- §20.3 append procedure, steps 1–6 (2905–3028)
- Appendix G reproducible-writer profile, items 1–10 (4169–4279)
- Appendix H five conformance checklists (4304–4369)

Numbering check on all of the above: each list runs 1..n with no duplicate, no
gap and no out-of-order item. Appendix G's items are 1,2,3,4,5,6,7,8,9,10 at
lines 4169, 4178, 4200, 4235, 4238, 4244, 4247, 4253, 4265, 4274.

---

## 3. The walk

### 3.1 Checksums the document quotes — all four recomputed

I implemented CRC-32C from §4.5's parameters alone (reflected Castagnoli
0x1EDC6F41 → reflected constant 0x82F63B78, init 0xFFFFFFFF, final XOR
0xFFFFFFFF) and checked it against §4.5's own check vector before trusting it.

```
check vector "123456789":      0xe3069283   (§4.5 says 0xE3069283)      OK
CRC-32C of zero bytes:         0x00000000   (§4.5 says 0x00000000)      OK
CRC of 4 sentinel entries:     0x80a34955   (§7.4 says 0x80A34955)      OK
  stored little-endian:        55 49 a3 80  (§7.4 says `55 49 A3 80`)   OK
crc_of_crc_array over those 4: 0xc4ee982e   (§7.4 says 0xC4EE982E)      OK
CRC of 2^16 sentinel entries:  0xeecb3bb2   (§15.4 says 0xEECB3BB2)     OK
```

The sentinel I fed in is §15.2's literal `FF ×16 00 ×4`. All four constants
reproduce. That also cross-validates Appendix B's rows "CRC of a full
all-sentinel segment" and "CRC check vector".

### 3.2 Appendix A, byte by byte

I transcribed the hex dump at lines 3990–3999 verbatim into a buffer and
checked the annotation table at 4001–4017 against it field by field, using
§6.2's trailer offsets with the trailer based at 64.

```
file length                    128                                     OK
[0,8)   89 54 41 52 4E 0D 0A 1A  = §6.1 magic                          OK
[8,16)  zero                                                            OK
[16,20) 00 00 00 00 = CRC-32C of zero bytes, dir_length 4               OK
[20,64) zero, 44 bytes of pad — 64-20 = 44                              OK
[64,72) 8A 4E 52 41 54 0D 0A 1A  = §6.2 trailer magic                   OK
[72,74) 01 00  version_major 1        (trailer offset 8)                OK
[74,76) 00 00  version_minor 0        (trailer offset 10)               OK
[76,80) 00 00 00 00 flags             (trailer offset 12)               OK
[80,88) generation 1                  (trailer offset 16)               OK
[88,96) dir_offset 16 = 0x10          (trailer offset 24)               OK
[96,104) dir_length 4                 (trailer offset 32)               OK
[104,112) committed_file_length 128 = 0x80  (trailer offset 40)         OK
[112,120) EF CD AB 89 67 45 23 01 = LE 0x0123456789ABCDEF (offset 48)   OK
[120,124) reserved zero              (trailer offset 56)                OK
[124,128) D2 38 09 E0 = LE 0xE00938D2                                   OK
computed CRC-32C over trailer[0,60):  0xe00938d2                        OK
```

Every trailer gate of `[R-CNT-06]` passes on this file: magic OK, CRC OK,
version_major 1, no incompat bit, committed_file_length = physical size = 128
and 128 mod 64 = 0, dir_offset 16 ≥ 16, dir_length 4 ≥ 4,
16 + 4 = 20 ≤ 128 − 64 = 64, generation 1 in [1, 2⁶³−1], file_id ≠ 0, reserved
zero. `[R-CNT-27]`'s floor argument also checks: with the front block ending at
16, a directory of ≥ 4 bytes at ≥ 16, and a 64-aligned trailer, the smallest
admissible trailer offset is 64 and so F = 128. The §5.1 Example at line 577
gives the identical layout and the identical 44-byte pad.

Appendix A's prose arithmetic also holds: "112 bytes covering [16, 128)" is
128 − 16 = 112, and that window contains the directory region [16, 20) while
leaving [0, 16) non-resident.

**One thing in Appendix A's prose I stopped on** — see Finding diagrams-02.

### 3.3 §7.4's layer-record figure (F-02), recomputed from scratch

I built the payload from the §7.4 *table* (not from the figure), then diffed
against the figure. Field walk:

```
name        u8 len + 3 bytes           4  -> offset 0
layout      u8                         1  -> 4
lineariz.   u16                        2  -> 5
codec       u16                        2  -> 7
filter      u16                        2  -> 9
A           u64                        8  -> 11
S           u64                        8  -> 19
A_slab      u64                        8  -> 27
rank d      u8                         1  -> 35
C           u16                        2  -> 36
dim entry   1+1 + 8 + 8 = 18           -> 38
chan entry  1+4 + 2 + 1+4 = 12         -> 56
index_enc   u8                         1  -> 68
entry_count u64                        8  -> 69
crc_of_crc  u32                        4  -> 77 .. 81
```

My generated bytes:

```
  0  03 73 73 74 01 01 00 01 00 01 00 00 00 00 00 00
 16  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
 32  00 00 00 01 01 00 01 78 64 00 00 00 00 00 00 00
 48  20 00 00 00 00 00 00 00 04 74 65 6d 70 0c 00 04
 64  00 00 c0 7f 01 04 00 00 00 00 00 00 00 2e 98 ee
 80  c4
```

Byte-for-byte identical to the figure's annotated listing at lines 1072–1089.
`73 73 74` = "sst"; `78` = "x"; `74 65 6D 70` = "temp"; type `0C 00` = 12 =
float32; fill `00 00 C0 7F` = LE 0x7FC00000. The twelve-byte channel entry is
exactly §12.3's example at line 1684, split across the figure's rows 56 and 63
— the figure's claim "§12.3's `temp` entry, byte for byte" is true.

The figure's summing sentence checks: "Name and the nine scalars from layout
through channel count occupy 4 + 34 bytes" — layout 1 + linearization 2 +
codec 2 + filter 2 + A 8 + S 8 + A_slab 8 + rank 1 + C 2 = 34, and that is
nine scalars. "the dimension entry 18, the channel entry 12, and the trailing
fixed fields 13" — index_encoding 1 + entry_count 8 + crc 4 = 13.
4 + 34 + 18 + 12 + 13 = 81, so the sub-record sequence is empty and
`[R-CNT-18]`'s "no residue" holds.

Geometry: ⌈100/32⌉ = 4 (100/32 = 3 remainder 4, so 3+1), interleaved so the
addressed-tile count is N = 4 = entry_count. `[R-CNT-17]`:
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = 84, which is the figure's stated extent length.
The index region is 80 bytes of entry array plus one 4-byte segment CRC — which
is what §15.1's box (F-04) prescribes.

### 3.4 The two files I built end to end

I wanted to know whether the document alone gets a writer to a byte stream, so
I placed the §7.4 layer into a whole file, choosing placement myself under
`[R-SLB-05]`:

```
front           [0, 16)
index region    [16, 100)     84 bytes = 4x20 + 4
directory       [100, 209)    24 header + 81 payload + 4 CRC = 109
pre-trailer pad [209, 256)    47 bytes, to the next 64 boundary
trailer         [256, 320)    F = 320, 320 mod 64 = 0
```

Checks I then ran against my own output: trailer magic at F−64; trailer CRC
verifies; dir_offset 100 ≥ 16; dir_length 109 ≥ 4; 100 + 109 = 209 ≤ 320−64 =
256; directory CRC verifies over the preceding 105 bytes; the extent slot
(16, 84) is ≥ 16 and ends at 100 ≤ 256; no structure lies in [209, 256) so
`[R-CNT-05]` holds; the coverage partition is
16 + 84 + 109 + 64 = 273 claimed and 320 − 273 = 47 slack, which is exactly the
pad. Every step of §19.1 and §19.3 succeeds against it.

I did not have to guess anything to produce those bytes. The record header's
flags value (MU = 1, PE = 1 → 0x0003) comes from §7.3's fixed-flags table; the
placement is free; the pad length falls out of `[R-LIF-02]` step 5.

### 3.5 Every other example's arithmetic, done by hand

- **§4.6 (513)** `température` in NFC: t e m p é r a t u r e = 11 code points,
  `74 65 6D 70 C3 A9 72 61 74 75 72 65` = 12 bytes, prefix 12. NFD swaps the
  2-byte `C3 A9` for the 3-byte `65 CC 81` → 13. Correct.
- **§11.2 (1518)** extents (1024, 2048), tiles (256, 256): G = (4, 8), N = 32,
  P = 65,536. With E_y = 1000: ⌈1000/256⌉ = 4. Correct.
- **§11.4 (1572)** grid (4, 8): tile (1,0) → 1·8+0 = 8. Coordinate (300, 700):
  t = (300 div 256, 700 div 256) = (1, 2) → s = 1·8+2 = 10; u = (44, 188) →
  44·256 + 188 = 11,452. Planar C = 4, channel 2 → 2·32 + 10 = 74. All correct.
- **§12.1 (1635)** binary32 1.0 = 0x3F800000, high half 0x3F80, stored `80 3F`;
  0x7FC0 ↔ 0x7FC00000. The bit-field split (sign 15, exponent 14–7,
  significand 6–0) is exactly binary32's top 16 bits. Correct.
- **§13.3 (1754)** rgb fills FF/00/00 → (255, 0, 0); planar with `b` sentinel
  gives a mixed sample. Matches `[R-TYP-08]` and §3.2.
- **§14.2 (1875)** interleaved (2,3), P = 6, uint8+uint16: Q = 3, size 18;
  ordinal 1·3+2 = 5; bytes [15, 18); planar `b` = 12 bytes with ordinal 5 at
  10–11. Then float32+bool: Q = 5, size 30, ordinal 5 at [25, 30) with the bool
  byte at 29. The closing identity u·Q + Fᶜ is the table's
  (k div C)·Q + F_{k mod C} at k = u·C + c. All correct.
- **§14.3 (1909)** planar bool, P = 10, alternating true first: byte 0 gets
  bits 0,2,4,6 set = 0x55; byte 1 gets bit 0 = 0x01 with six pad bits; with
  fill true the pad bits set gives 0xFD. Correct, and consistent with
  `[R-SER-05]`'s "every pad bit MUST carry the plane's channel's fill bit".
- **§14.5 (1965)** extents (5,5), tiles (4,4) → grid 2×2; the (1,1) tile covers
  4–7 on both axes, one real position and 15 padding; P = 16, one uint16
  channel → 32 bytes, values 1–15 each `CD AB` for fill 0xABCD. Correct.
- **§15.4 (2089)** entry_count 1,000,000: ⌈10⁶/65536⌉ = 16 segments, 15 full
  (983,040 entries) plus 16,960; CRC array 64 bytes; region 20,000,064 bytes.
  k = 999,999 → segment 15, segment-relative entry 16,959 → byte 339,180;
  CRC array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) — 339,200 bytes ≈ 339 KB. One full segment is
  65,536 × 20 = 1,310,720 = 1.25 MiB. Every figure in that example is right.
- **§15.4 (2104)** disk ordinal 74 → region bytes [1,480, 1,500); channel 3's
  block is [96, 128) so "entries 96–127" is 32 sentinels. Correct.
- **§16.2 (2203)** grid 4×8, N = 32, S = 8 → runs [0,8) [8,16) [16,24) [24,32);
  under row-major each run is one tile row; rows 1–2 are ordinals 8–23 = runs 1
  and 2. Correct.
- **§17.3 (2384)** float32 1.0/2.0/3.0 = `00 00 80 3F 00 00 00 40 00 00 40 40`,
  s = 4, n = 3. Placing byte i of group j at i·n + j gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`, which is the example's string.
  Correct.
- **§20.3 (3038)** 32 · 20 + 4 = 644, one entry re-pointed and 31 identical.
  Correct.
- **§21.9 note (3682)** segment CRC array at entry_count 2³² is
  2³²/2¹⁶ × 4 = 2¹⁸ = 256 KiB, and at 2³⁶ it is 2²⁰ × 4 = 4 MiB. 65,536 layers
  × 200 bytes = 13,107,200 = 12.5 MiB exactly. Correct.
- **§20.3 note (3030)** 10⁶ tiles × 20 = 20 MB. Correct.
- **§19.4 note (2834)** entries for one spatial ordinal are N apart in ordinal
  and N·20 apart in region bytes; if N ≥ 2¹⁶ consecutive channel entries differ
  by ≥ 2¹⁶ in ordinal and so cannot share a segment. Correct.
- **§17.2 note (2298)** the Single_Segment_Flag argument holds: with the flag
  set RFC 8878 requires Frame_Content_Size, which `[R-COD-06]` pins to the
  decoded size; without it the Window_Descriptor floor is 1 KiB, which would
  exceed a sub-1-KiB decoded size and trip `[R-COD-06]`'s window rule (T21).
  §14.3's example decoded size is ⌈10/8⌉ = 2, as the note says.
- **§24 / §21.9** 2³² entries × 20 bytes = 85.9 GB, so `[R-VEC-03]`'s "tens of
  gigabytes of incompressible entries" is right and the guarantee is indeed not
  directly constructible.

### 3.6 The register as a figure: counts and internal consistency

§21.8 states "121 conditions over 273 instances". I counted mechanically using
§21.1's own rule ("Instances within a cell are separated by semicolons, and a
cell reading — is one instance"):

```
§21.2  36 rows,  58 instances
§21.3  49 rows, 116 instances
§21.4  26 rows,  55 instances
§21.5  10 rows,  44 instances
       ---------------------
       121 rows, 273 instances
```

Both numbers reproduce exactly, and the per-subsection counts (36 / 49 / 26 /
10) match the sentences at lines 3355, 3411, 3468 and 3517.

I also checked, mechanically:

- every row with Detector = *verifier* has Detected = *certification*, and no
  row with Detector = *reader* has Detected = *certification*: **no anomalies**;
- every Detected cell names one of §19.2's four reader tiers or *certification*
  (R1's split cell "open (top-level); layer access (sub-record)" being the one
  compound): **no anomalies**;
- every `R-xxx-nn` identifier cited in a Governing rule cell occurs elsewhere in
  the document: **none undefined**;
- identifier numbering per prefix has no gaps except `R-ENC-100`, which is §2.2's
  own illustration of numbers above 99, and `R-SER-04`, which §14.4's Note
  declares withdrawn and permanently retired.

§21.1's instance axioms then check out row by row. Two-direction enumeration for
*differs from* / *does not equal* (F17, F23, L12, L21, L22, L30, T3, T14, T22);
one direction for *exceeds* / *larger than* (T21, L44); no direction for a
checksum or a byte pattern against a constant (F14, F20, L37, L38, T1, R2, T17);
layout enumeration wherever a derived quantity varies by layout (T3, T14, T21,
T22, L44, T4, T26 — three or four shapes each). §21.1's named specialization
pairs also hold: F1's front-block instance specialises F6 and its trailer-magic
instance specialises F8; F35 specialises F36; L24 specialises L25. I looked for
unnamed strict specialisations and found none: T7 and T11 are kept disjoint by
T11's clause "the value being distinct from the all-ones sentinel", and L27
(entry_count 0 with nonzero crc_of_crc_array) cannot collide with L37 because
§15.4's example fixes that at entry_count 0 "nothing is fetched and nothing is
verified".

Where the check did find something is the alignment between a row's Condition
cell and its own Instances cell — **Finding diagrams-01**.

### 3.7 §15.3's table against `[R-IDX-03]`'s prose

`[R-IDX-03]` says "Six rows are marked *structural*". The table has exactly six:
sentinel-with-nonzero-crc; exactly-one-half-sentinel; length 0; offset < 16;
offset or length above 2⁶³−1; overflowing or past-F−64 sum. It has exactly three
*verifier* rows (intra-layer overlap; extra-layer overlap; alignment/slab), one
plain reject-tile row (stored bytes fail the crc, expressly "well-formed"), and
one valid-sentinel row. Eleven rows total, and each maps onto a register row:
T6, T7, T10, T8, T11, T9+T12, T1, L18, F33, L40/L41/L42. No orphan in either
direction.

### 3.8 §8.1's coverage map against §4.5

§4.5 names three excepted classes; §8.1's map has exactly the matching rows.
Terminal checksum fields (trailer CRC, directory CRC, user-metadata extent CRC)
are covered by nothing; interior ones (each segment CRC array, each entry's crc,
each layer record's crc_of_crc_array) are each covered by exactly one further
checksum — entry crc by its segment CRC, segment CRC array by crc_of_crc_array,
crc_of_crc_array by the directory CRC. The chain §8.2 states,
trailer → directory → crc_of_crc_array → segment CRC array → index segment →
index entry → stored tile, walks those edges in order. I built that chain in my
one-layer file and it closes.

The map's seven rows are exhaustive over §5.2's structure classes: front block,
trailer, directory, layer-record extent (= tile-index region), stored-tile
extent, user-metadata extent, unassigned-type extent. There are no other extent
kinds, because §7.3 assigns only two record types.

### 3.9 §10.2's spaces table against every owning section

Row by row against §7.3, §14.1, §11.4, §12.2, §17.2, §17.3, §15.1/§7.4 and
§18.2: assigned, reserved and experimental partitions all agree, including the
sub-partitions the owning sections state and §10.2 collapses (sample type 14–19
then 20–0x7FFF; linearization 2–3 then 4–0x7FFF). Appendix C's snapshot agrees
with both, including the six pinned sample-type reservations 14–19 and the six
standardized keys.

One loose seam I checked and decided against reporting: line 1408 says "Two
spaces carry no experimental range: channel layout ... and the trailer's flag
lanes", while the table above it has eight rows of which exactly one reads
"none" in the Experimental column — the flag lanes are not a row. The sentence
names the second explicitly and says §6.3 partitions it instead, so a reader is
not misled, and the preceding sentence's "Value 0 is invalid in every space
above" is scoped to the table and so does not collide with §6.3's mandatory
flags = 0. Not a defect.

### 3.10 §12.1's type table, §21.9's limits table, Appendix B

Thirteen types, twelve of them numeric — both counts used elsewhere
(§12.1 "exactly thirteen", §13.2 "the twelve numeric types") and both correct.
Element sizes 1,1,2,4,8,1,2,4,8,2,2,4,8 are each the natural width.

§21.9's eight guarantees appear identically in Appendix B's "Reader minimum
guarantees" row. §21.9's hard-limit paragraph and Appendix B agree on every
bound: names 255; rank 255; C 65,535; lz4 0x7E000000; value domain 2⁶³−1;
A power of two in [512, 2⁶²]; A_slab power of two in [1, 2⁶²]; S in
[1, 2⁶³−1]; dir_offset ≥ 16 and dir_length ≥ 4; file ≥ 128 bytes.

§21.9's claim that only two bounds are chosen rather than forced also holds
when checked: A ≤ 2⁶² is forced (2⁶² is the largest power of two inside the
2⁶³−1 domain), so the 512 floor and the 255-byte key cap really are the two
free choices.

Appendix B promises "Every named constant this specification fixes, collected".
I went looking for a missing one — the user-metadata key cap is covered by the
"Name length" row because §4.6 defines *names* to include user-metadata keys;
enum assignments live in Appendix C by design; the 64-byte pad boundary is
covered by "Trailer size ... at a 64-aligned offset". I found no omission.

### 3.11 The nine ASCII figures

- **F-01 (§5.1, three commits)** — the two ▓ runs are consistent with a real
  history: commit 1 wrote A then dir₁/pad/tr₁; commit 2 appended B then
  dir₂/pad/tr₂, superseding the first triple; commit 3 touched no layer and
  re-emitted dir₃/pad/tr₃, superseding the second. The caption's "the ▓ runs are
  the directories, pads and trailers of commits 1 and 2" is exactly that. The
  figure's own hedge — "The grouping under the box is illustrative: a layer's
  structures need not be contiguous or ordered (`[R-SLB-05]`), and §20.5's
  figure shows the general case" — is right, and §20.5's figure does show A's
  tiles and A's index non-adjacent.
- **F-03 (§9.2, crash)** — row 2's ▓ is a partial write past an intact trailₙ;
  row 3's ▓ is dirₙ/pad/trailₙ superseded. Both match the caption and
  `[R-LIF-05]`'s no-backward-scan rule.
- **F-05/F-06/F-07 (§20.3, three shapes)** — (a) nothing existing rewritten and
  the slack is exactly the old dir/pad/trailer, "sized by the file's layer
  count, never by any layer's data"; (b) the whole index region moves because
  one extent slot addresses it; (c) only the directory is re-emitted. Each is
  consistent with step 4's re-emission rule and with `[R-LIF-01]`. Shape (c)'s
  three permitted edits — clearing a slab declaration, renaming a layer,
  changing a fill on a layer with no padding position and no pad bit — are each
  outside step 4's bar, and the figure says so explicitly for the fill case.
- **F-08 (§20.5, compaction)** — the output keeps a `pad`, which is slack.
  I checked this against "so slack is never carried" in the same section and it
  is not a contradiction: the pad in the output is one `[R-LIF-02]` step 5
  obliges the compactor to write as a writer, not one carried from the input.
  The figure is right to show it and would be wrong to omit it.
- **F-04 (§15.1 region box)** and **F-02, F-09** are covered above.

### 3.12 Checklists

**Appendix H, conforming verifier.** I enumerated the register's verifier rows —
F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49,
T2, T4, T5, T26 — and checked each is reachable from a checklist line. Coverage
partition and slack total; extent overlap (F33, L18); reserved flag bits and
MU=1/PE=0 (F25, F26, L46, L47); registered types' stored bits (F28, L49); front
block (F1, F6); no structure in the pre-trailer gap (F7); reserved-range type
values (F36, L25); alignment and slab invariants (L40–L42); decoded-content
obligations (T2, T4, T5, and T26 whose detecting check the row itself says is
T2's or T4's); metadata member ordering (F27, L48). **All twenty are covered.**

**Appendix H, conforming reader.** "all four codecs, both filters, both layouts,
all thirteen sample types, and both user-metadata encodings" matches §2.3
resolved through §17.2, §17.3, §14.1, §12.1 and §18.2. The one thing the reader
entry does not restate is the front-block equality obligation for a reader
holding [0,16) resident; the appendix's preamble calls itself "A summary", not
an inventory, and the verifier entry does carry the front-block line together
with the reader's exemption, so I did not treat the omission as a promise
broken.

**Appendix G.** Items 1–10 in order. The closing paragraph names a purpose for
each of the ten and then disclaims being a count ("Read the numbered items as
the list; this paragraph names what they are for, not how many there are"), so
its silence on item 5's fixed-filter half is licensed. Item 2's `file_id`
derivation is well defined: the hash input is [0, F−64) followed by the
trailer's first 60 bytes with `file_id` zeroed, and F is known once [0, F−64) is
fixed, so there is no circularity. Item 3's ordering key masks `extent_offset`
for the same reason and says why. Item 3's tie-break argument ("Two records this
key does not separate are byte-identical in type, flags, lengths, payload and
extent content; emitting them in either order yields the same file") is sound —
identical extent lengths and contents make the swap invisible.

### 3.13 §21.6, read as a figure

Fourteen rows. Each Rule cell's identifiers resolve, and each Defined-behavior
cell restates its rule without widening it, with one wrinkle I checked and let
go: the sentinel row says "every sample position it carries reads as the
channel's fill", where `[R-TYP-08]` says only positions "inside the layer's
extents" are returned as fill and `[R-GEO-04]` forbids returning padding
positions at all. §21.1 already says the rule governs where an entry diverges,
and no reader could act on the wider reading without violating `[R-GEO-04]`.

I checked whether §21.6 owes completeness and it does not: §21.1 says "The
subsections after §21.5 are not part of the register and carry no rows: neither
this completeness clause nor the instance arithmetic below reaches §21.6's
defined non-violations". That disposes of the one gap I found — `[R-CNF-02]`
names two writer-conduct cases (a set ignore-lane bit, and a pre-trailer gap
longer than step 5's pad) and only the first has a §21.6 row of its own, the
second being covered generically by the slack row.

The closing paragraphs check out. "Four rows are outside that reasoning" (§21.2,
line 3360) is exactly F8, F14, F6 and F1 — I verified against §6.2's ordered
validation that every other file-scope row sits behind the version gate, and
against `[R-CNT-24]` that only the magic, the two version fields and the CRC
have positions fixed across majors. The two capability refusals named in the
closing paragraph are the same two §2.3 points back at, and §21.9 excludes them
from the resource-limit ground. The top-level qualifier on the MU = 1 case is
load-bearing and correct: `[R-CNT-18]` makes the sub-record case reject-layer
and forbids rejecting the file for it.

### 3.14 §20.5, read as a figure and as prose

Every normative verb in §20.5 is in capitals (MUST refuse ×3, MUST NOT emit,
MUST mint, MUST copy, MUST preserve, MUST equal, MUST verify, SHOULD be at
least). No lowercase near-keyword carrying weight. The unlabelled paragraph at
3203–3215 ("Regenerating a region means classifying every entry in it") invokes
`[R-WRT-06]` rather than stating a new obligation, so it needs no identifier of
its own.

I checked the parenthetical "(F36, L25, R1)" at line 3183. It claims the two
extension vehicles that are *not* §21.6-conforming reach a file only as
reserved-range violations. F36/L25 are the record-type rows and R1 the
metadata-encoding row; the other reserved-range rows (L31, L33, L34, L36, L43,
L45) are all layer-record enum fields that `[R-WRT-09]` obliges the compactor to
validate through §19.3, so they cannot survive into a compactor's output
unnoticed. The citation is the right three.

I also checked §20.4's table for an identifier, since it carries MUSTs. Under
the document's end-of-run convention the span from after `[R-WRT-05]` to
`[R-WRT-08]` — the persistence paragraph, the table, and the no-removal
paragraph — is `[R-WRT-08]`'s requirement text, which is why §21.6's
experimental-record row can cite `[R-CNT-15]`, `[R-WRT-08]` for "preserved or
dropped per its PE bit". §18.2's `[R-MTA-04]` sets the same multi-paragraph
precedent. Not a defect; I had it on my candidate list and struck it.

### 3.15 §7.4, read as a figure and as prose

Every normative verb is in capitals. The table's constraint cells agree with
their owning sections: layout with §14.1 and §10.2; linearization with §11.4;
codec with §17.2; filter with §17.3; index_encoding with §15.1 and §10.2; A with
§16.1; S with §16.2; entry_count with §11.2 and `[R-CNT-17]`; crc_of_crc_array
with §15.4; fill length with §12.1's element sizes.

One asymmetry I checked and struck: §16.2 gives A_slab as "a power of two ≥ 1"
with no ceiling, while §7.4's table, §21.9 and Appendix B all give
1 ≤ A_slab ≤ 2⁶², and L29 registers "A_slab above 2^62". §7.4's table is
normative through `[R-CNT-23]` and §16.2 cites it ("§7.4; mutually exclusive
with per-tile alignment"), so no implementation reading the document as a whole
can conclude 2⁶³ is admissible. Three statements of the ceiling against one
silence is not a fork.

Where §7.4's presentation *is* out of step with the document's own account of
it is the column set — **Finding diagrams-03**.

---

## 4. Findings

### diagrams-01 — CONTRADICTION — two register rows enumerate an instance their Condition cell does not state, contrary to §21.1's rule for instance cells

**Location:** §21.1 (instance rule), §21.3 row L14, §21.5 row R7.

§21.1 fixes what may appear in an Instances cell:

> "An instance names a field the condition ranges over, a container it can
> occur in, one of several alternatives the condition text states, or any
> combination of the three — a condition applying to two alternatives in two
> containers has four."

Two rows break that. **L14:**

> "| L14 | A sub-record does not fit in the layer record's inline payload: its
> 24-byte header is truncated at the payload end, or its inline_length runs
> past that end | sub-record header; sub-record inline_length; trailing
> residue | reader | layer access | `[R-CNT-12]` (R-CNT-18, R-ENC-07) |"

The Condition cell states two alternatives. The Instances cell names three, the
third being *trailing residue* — bytes remaining after the last complete
sub-record. Residue is not a case of "a sub-record does not fit"; it is a
distinct condition, and `[R-CNT-18]` states it separately: "the remaining bytes
MUST parse as zero or more complete sub-records under §7.2's framing with no
residue; any overrun, truncation, or residue is a validity error at layer
scope". The file-scope twin, F29, gets this right — its Condition cell reads
"...or bytes remain after the last complete record", and its three instances
follow from it.

**R7:**

> "| R7 | A decoded user-metadata document is not well-formed JSON, or its
> top-level value is not an object | not well-formed JSON, top-level document;
> not well-formed JSON, layer sub-record document; top-level value not an
> object, top-level document; top-level value not an object, layer sub-record
> document; leading U+FEFF, top-level document; leading U+FEFF, layer
> sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |"

The Condition cell states two alternatives; the Instances cell enumerates
three across two containers, the third being *leading U+FEFF*. §18.2 states the
BOM as its own rule — "The top-level value is an object, and the encoding
carries no byte-order mark: a leading U+FEFF makes the document unreadable" —
and states it separately precisely because a permissive parser will accept a
BOM and still call the text well-formed JSON, which is what keeps it from being
subsumed by the row's first alternative.

**What an implementer gets wrong without this.** The instance counts are what
§21.8 and `[R-ERR-02]` bind a corpus to — "121 conditions over 273 instances ...
one vector per instance" — and a corpus builder who works from the Condition
cells (as the row text invites, since §21.1 says every instance is an
alternative the condition states) builds two vectors for L14 instead of three
and four for R7 instead of six, and comes up four short of 273. A builder who
works from the Instances cells hits 273 but is building files against a
condition the row does not describe, so the manifest entry `[R-VEC-02]`
requires — "the §21 register row it exercises together with that row's
governing requirement identifier" — names a row whose text does not cover the
file. I recomputed the totals both ways: the Instances cells give exactly
121/273, so the published figure is only reachable by trusting the Instances
cells over the Condition cells.

**Byte-level: no.** Both omitted alternatives are stated normatively by the
governing rules — `[R-CNT-18]` for sub-record residue, `[R-MTA-04]` for the BOM
— and §21.1 says "each row *restates* its governing rule, and where a row and
the rule it cites diverge, **the rule governs**". Two implementations reading
this text both reject the layer on sub-record residue and both take
ignore-record on a leading BOM; the emittable set and every accept/reject
verdict are unmoved. The cost is corpus coverage, not interoperation.

### diagrams-02 — OBSERVATION — Appendix A ties the front-block check to a *local reader*, a test §6.1 expressly rejects in favour of residency

**Location:** Appendix A (lines 4019–4028); §6.1, `[R-CNT-04]`.

Appendix A's closing prose:

> "A local reader additionally verifies bytes [0, 16) by equality first, which
> `[R-CNT-04]` requires of any reader holding them"

§6.1 defines *local reader* and then rules that term out for this obligation:

> "A **local reader** is one whose transport serves any byte range at no
> per-range round trip ... That distinction governs the request accounting of
> §6.4 and nothing else; the obligation over the front block turns on residency
> instead, because a transport can be classified either way at the margin while
> residency is decidable at any reader's own open path."

and closes `[R-CNT-04]` with "The test is residency, not transport". The
document is otherwise uniform on this: §19.1 step 1 says "A reader whose open
leaves bytes [0, 16) resident"; F1 says "the front-block instance binds only a
reader holding bytes [0, 16) resident"; F6 says "the obligation binds a reader
holding those bytes resident"; Appendix H says "which `[R-CNT-04]` lets a reader
not holding it resident defer or omit". Appendix A is the only place in the
document that attaches the obligation to transport class.

**Permitted readings and the one I picked.** Reading (a): the main clause
asserts a fact about local readers and the relative clause supplies the real
trigger, so a local reader that pread s only the trailer and the directory —
holding no byte of [0,16) — is outside the obligation, and Appendix A is simply
describing the ordinary local reader of a 128-byte file, which does read it
whole. Reading (b): locality is itself the trigger, so any reader on a
zero-round-trip transport owes the check. I picked (a), because §6.1's "and
nothing else" and "The test is residency, not transport" are express, because
`[R-CNT-04]` enumerates residency cases and "a local file read whole" is one of
them rather than a synonym for local, and because Appendix A is labelled
non-normative. **What an implementer does wrong without this:** a memory-lean
local reader that fetches only the ranges it needs concludes, from Appendix A,
that it owes a read of [0,16) it does not owe — a wasted read, not a wrong
verdict — or, worse for a verifier author, reads Appendix A's local/remote split
as the operative distinction and grants a remote verifier the exemption §2.3
denies it ("including those ordinary readers are exempted from"; F6: "a verifier
holds no such exemption").

**Byte-level: no.** Appendix A is "An annotated minimal file (non-normative)"
and §2.1 excepts appendices identified as non-normative from the normative text.
`[R-CNT-04]`, §19.1 step 1, F1 and F6 all state the residency test, so no
conforming implementation can be led by this sentence into a different
accept/reject verdict on any byte sequence.

### diagrams-03 — OBSERVATION — §4.7's Note mis-states which columns §7.4's and §7.2's layout tables carry

**Location:** §4.7 Note (lines 536–549); §7.2's table (904–910); §7.4's table
(1006–1023).

§4.7's Note is the document's own account of how to read its layout tables:

> "Layout tables for fixed-layout structures give, per field: byte offset within
> the structure, size, type, name, taxonomy class, and valid range, each table
> giving the columns its structure needs. A packed variable-length payload — the
> layer record's inline payload (§7.4) — has no fixed offsets to give; its table
> omits the offset and class columns, and each field's class follows from the
> definitions above. §6.1's block is a 16-byte constant, where a Value column
> replaces type and range, and §7.2 folds each field's range into its Field
> cell."

Two of its three specific claims are not delivered.

*First*, §7.4's table's columns are `Field | Type | Constraint`. Measured against
the six-column list, it omits offset, **size**, and class — three, not the two
the Note accounts for. §6.2's, §15.1's and §18.2's tables all carry a Size
column beside Type, so the two are distinct columns in this document's own
practice, and §6.1's four-column exception is spelled out precisely ("a Value
column replaces type and range") where §7.4's is not.

*Second*, §7.2's table's Field cells are `type (0 invalid)`, `flags: bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved`, `inline_length`,
`extent_offset`, `extent_length`. Two of five carry a range; the extent slot's
range and `inline_length`'s bound live in `[R-CNT-13]` and `[R-CNT-12]`, in the
prose below the table, not in the Field cells. "each field's range" is
delivered for two fields.

**What an implementer does wrong without this:** nothing to the bytes. Every
size §7.4's table omits is recoverable from its Type cell (`u8`, `u16`, `u64`,
`u32`, or an explicit `u8 len + bytes` for the variable ones), and I built the
81-byte payload from the table alone without ambiguity. Every range §7.2's table
omits is stated in the immediately following requirement and registered
(F30–F32, L15–L17). The cost is to a reader auditing the document's
self-description — the Note is the map, and the map is wrong about two of the
territories it names.

**Byte-level: no.** The Note is labelled *Note* and §2.1 excepts "any text
labeled *Note*, *Example*, or *Rationale*" from the normative text. Neither
claim changes any field's width, offset or valid range.

---

## 5. What I could not determine, and where I did not have to guess

I built a 128-byte file and a 320-byte one-layer file from the document alone
and did not have to guess at any byte. The places I expected to guess and did
not:

- the segment CRC array at entry_count 0 — §15.4's example settles it
  ("zero segments, a zero-byte CRC array, extent slot (0, 0) and
  crc_of_crc_array = 0");
- the record header's flags for a layer record — §7.3's registry table fixes
  MU = 1, PE = 1, and `[R-CNT-22]` makes the fixed values govern;
- the pre-trailer pad's length — `[R-LIF-02]` step 5 pads to the next 64-byte
  boundary and `[R-CNT-05]` bounds the gap only through that step;
- whether an interleaved single-channel bool tile packs — §14.3 says packing is
  "exclusive to planar bool planes";
- the shuffle stride for a packed bool plane — §17.3 gives s = 1, identity;
- what a reader returns for a nonconforming interleaved bool byte —
  `[R-SER-08]` defines it, and §14.2's Rationale explains why.

Two things I could determine only by tracing the identifier convention rather
than by reading a label, and which cost me real time: that §20.4's table is
covered by `[R-WRT-08]` (the identifier sits at the end of the run, three
paragraphs below the table), and that the §21.6 row citing `[R-WRT-08]` for
"preserved or dropped per its PE bit" is therefore correct rather than
mis-cited. I record that as friction, not as a finding — §18.2's `[R-MTA-04]`
sets the same precedent, so the convention is consistent even where it is
slow to read.

**Finding count in this transcript: 3.**
