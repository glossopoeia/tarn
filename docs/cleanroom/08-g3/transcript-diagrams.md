# Round 8 — Diagram auditor working transcript

Access discipline: I opened exactly one file, `spec/tarn.md`. I read it end to
end in five passes (lines 1–400, 400–850, 850–1300, 1300–1750, 1750–2200,
2200–2650, 2650–3100, 3100–3520, 3520–3843). I ran `grep`/`awk` against that
same file (three invocations, all shown below) and three Python snippets whose
input data was typed inline into the command — no Python call opened a file. I
read no ADR, no `docs/`, no `conformance/`, no `registry.json`, no git history,
no web. I did not list any directory. I wrote this one file.

---

## Part 1 — Inventory before judgment

I enumerated every figure, byte-layout box, ASCII diagram, offset table,
worked example and checklist before evaluating any of them, so coverage is
checkable. Line numbers are from `spec/tarn.md`.

### A. Byte-layout / offset tables (normative)

| # | Location | Lines | What it lays out |
|---|---|---|---|
| A1 | §2.4 | 220–226 | Outcome classes (restates rule vocabulary) |
| A2 | §6.1 | 644–647 | Front signature block, offset/size/value/class |
| A3 | §6.2 | 687–699 | Trailer, 10 rows, offset/size/type/field/class/valid |
| A4 | §7.2 | 851–857 | Record header, 5 rows, 24 bytes |
| A5 | §7.3 | 922–925 | Record types of major 1, with fixed MU/PE |
| A6 | §7.4 | 951–968 | Layer record inline payload, 16 rows |
| A7 | §8.1 | 1025–1033 | Checksum coverage map, 7 rows |
| A8 | §10.2 | 1286–1295 | Numeric identifier spaces, 8 rows |
| A9 | §12.1 | 1481–1495 | The 13 sample types and element sizes |
| A10 | §14.2 | 1711–1714 | Decoded size and offset of value k, 2 rows |
| A11 | §15.1 | 1874–1875 | Tile-index region layout (block quote figure) |
| A12 | §15.1 | 1879–1883 | Tile-index entry, 3 rows, 20 bytes |
| A13 | §15.3 | 1927–1939 | Entry-validity classification, 11 rows |
| A14 | §18.2 | 2313–2315 | User-metadata record inline payload, 1 row |
| A15 | §18.4 | 2437–2444 | Standardized keys, 6 rows |
| A16 | §20.4 | 2867–2871 | Updater obligations by stored flags, 3 rows |
| A17 | §21.9 | 3270–3279 | Implementation-limit minimum guarantees, 8 rows |

### B. Register tables (normative, restate rules stated in prose)

| # | Location | Lines | Rows |
|---|---|---|---|
| B1 | §21.2 file scope | 3024–3064 | F1–F39 |
| B2 | §21.3 layer scope | 3071–3122 | L1–L50 |
| B3 | §21.4 tile scope | 3129–3156 | T1–T26 |
| B4 | §21.5 ignored records | 3170–3181 | R1–R10 |
| B5 | §21.6 non-violations | 3188–3203 | 14 rows |

### C. ASCII diagrams

| # | Location | Lines | Subject |
|---|---|---|---|
| C1 | §5.1 | 548–553 | File after three commits, with slack |
| C2 | §9.2 | 1104–1113 | What a crash sees (3 rows) |
| C3 | §20.3 (a) | 2808–2812 | Commit adding a new layer |
| C4 | §20.3 (b) | 2824–2828 | Commit adding tiles to an existing layer |
| C5 | §20.3 (c) | 2841–2844 | Commit confined to the directory |
| C6 | §20.5 | 2926–2932 | What compaction reclaims |
| C7 | Appendix A | 3564–3573 | 128-byte hex dump (the only unquoted code block) |

### D. Worked numeric examples

| # | Location | Lines | Claim under test |
|---|---|---|---|
| D1 | §4.5 | 421–425 | CRC-32C check vector |
| D2 | §4.6 | 490–494 | `température` NFC/NFD byte counts |
| D3 | §5.1 | 538–543 | Smallest conforming file region map |
| D4 | §11.2 | 1398–1402 | Grid counts, N, P; ceiling division at 1000 |
| D5 | §11.4 | 1452–1458 | Spatial, in-tile and disk ordinals |
| D6 | §12.1 | 1515–1518 | bfloat16 1.0 and 0x7FC0 |
| D7 | §12.3 | 1564–1569 | 12-byte channel entry byte string |
| D8 | §13.3 | 1632–1637 | Interleaved and planar fill tuples |
| D9 | §14.2 | 1753–1763 | Q, decoded size, per-value byte offsets |
| D10 | §14.3 | 1787–1792 | Packed bool plane `55 01` / `55 FD` |
| D11 | §14.5 | 1843–1848 | 5×5 / 4×4 edge tile, 32 bytes, `CD AB` ×15 |
| D12 | §15.4 | 1967–1980 | entry_count = 1,000,000 segment arithmetic |
| D13 | §15.4 | 1982–1986 | Planar disk ordinal 74, entries 96–127 |
| D14 | §16.2 | 2079–2086 | Four slab runs over N = 32 |
| D15 | §17.2 note | 2174–2182 | zstd Window_Size derivations, cites 18/30/2 |
| D16 | §17.3 | 2260–2263 | Byte-shuffle of three float32 values |
| D17 | §19.4 note | 2675–2680 | Planar all-channel segment spacing |
| D18 | §20.3 | 2794–2801 | Supersede one tile: 644-byte index region |
| D19 | §21.8 | 3257–3260 | 125 conditions over 252 instances |
| D20 | §21.9 note | 3291–3306 | Where the guarantee numbers come from |
| D21 | Appendix A | 3575–3604 | Field-by-field annotation of C7 |

### E. Checklists and summary tables (non-normative, in charter)

| # | Location | Lines | Subject |
|---|---|---|---|
| E1 | Appendix B | 3611–3636 | Constants |
| E2 | Appendix C | 3645–3663 | Registry snapshot |
| E3 | Appendix E | 3705–3707 | Changelog |
| E4 | Appendix G | 3740–3785 | Reproducible-writer profile, 8 items |
| E5 | Appendix H | 3793–3842 | Five conformance checklists |

That is 17 + 5 + 7 + 21 + 5 = 55 artifacts. Everything below is the audit.

---

## Part 2 — Arithmetic actually performed

I did the arithmetic rather than eyeballing it. Three Python runs, all with
inline literal data.

### 2.1 The checksum constants (D1, E1, A11/§15.4)

```
CRC32C('123456789') = 0xE3069283   spec §4.5 says 0xE3069283   MATCH
CRC32C(b'')         = 0x00000000   spec §4.5 says 0x00000000   MATCH
CRC32C(65536 sentinel entries, 1,310,720 bytes) = 0xEECB3BB2
                     spec §15.4 / Appendix B say 0xEECB3BB2    MATCH
```

The sentinel bytes I fed in were `(b"\xff"*16 + b"\x00"*4) * 65536`, i.e.
exactly §15.2's "`FF ×16 00 ×4`". Length came out 1,310,720 = 65,536 × 20,
which is also the "1.25 MiB" figure §15.4's example quotes for one full
segment. Both check.

### 2.2 Appendix A, byte by byte (C7 + D21)

I typed the 128 bytes of the hex dump in verbatim and decoded them against
§6.2's layout table.

```
file length: 128                       §5.1 / Appendix B: 128        MATCH
trailer at [64,128), 64 bytes          §6.2                          MATCH
magic            8A 4E 52 41 54 0D 0A 1A                             MATCH
version_major    1        (u16 @ trailer 8,  file 72)                MATCH
version_minor    0        (u16 @ trailer 10, file 74)                MATCH
flags            0        (u32 @ trailer 12, file 76)                MATCH
generation       1        (u64 @ trailer 16, file 80)                MATCH
dir_offset       16       (u64 @ trailer 24, file 88)                MATCH
dir_length       4        (u64 @ trailer 32, file 96)                MATCH
cfl              128      (u64 @ trailer 40, file 104)               MATCH
file_id          0x0123456789ABCDEF (u64 @ trailer 48, file 112)     MATCH
reserved         00 00 00 00        (@ trailer 56, file 120)         MATCH
computed CRC-32C over trailer[0,60) = 0xE00938D2
  stored little-endian at [124,128) = D2 38 09 E0 = 0xE00938D2       MATCH
dir region [16,20) = 00 00 00 00 = CRC-32C of zero bytes             MATCH
```

Every offset in the annotation table (D21) also matches the physical dump:
[72,74), [74,76), [76,80), [80,88), [88,96), [96,104), [104,112), [112,120),
[120,124), [124,128) are exactly trailer offsets 8, 10, 12, 16, 24, 32, 40,
48, 56, 60 shifted by 64. The pad is [20,64) = 44 bytes, and 16 + 4 + 44 + 64
= 128. The file also satisfies every §6.2 gate: F mod 64 = 0, dir_offset ≥ 16,
dir_length ≥ 4, dir_offset + dir_length = 20 ≤ F − 64 = 64, 1 ≤ generation,
file_id ≠ 0, reserved zero. And §9.7's walk: the single claimant (the
directory) lies inside [16, 64) as required.

Appendix A is exact. I could not fault a single byte of it. The closing prose
is right too: 128 − 16 = 112, so a 112-byte suffix window covering [16,128)
does contain the directory and leaves [0,16) non-resident, which is exactly
the case §6.1's residency test lets a reader skip.

### 2.3 §5.1's 128-byte floor (D3)

dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64 gives
F ≥ 84; F ≡ 0 (mod 64) gives F ≥ 128. The example's region map
(front [0,16), dir [16,20), 44 slack, trailer [64,128)) is the unique minimum.
Checks.

### 2.4 The geometry chain (D4, D5, D9, D10, D11, D13, D14)

- D4: ⌈1024/256⌉ = 4, ⌈2048/256⌉ = 8, N = 32, P = 65,536. ⌈1000/256⌉ = 4
  (1000/256 = 3.90625). All correct.
- D5: s = Σ tᵢ ∏_{j>i} Gⱼ → tile (1,0) = 1·8 + 0 = 8. (300,700) → t = (1,2),
  s = 1·8+2 = 10; u = (44,188); in-tile ordinal = 44·256 + 188 = 11,452.
  Planar channel 2: 2·32 + 10 = 74. All correct.
- D9: Q = 1 + 2 = 3, P·Q = 18. Ordinal of (1,2) = 1·3 + 2 = 5. 5·3 = 15, so
  bytes [15,18) with `a` at 15 and `b` at 16–17. Planar `b`: P·B = 6·2 = 12,
  ordinal 5 at 10–11. With float32 + bool: Q = 5, P·Q = 30, sample at
  [25,30), `t` at 25–28 (F₀ = 0), `m` at 29 (F₁ = 4). The generalization
  "channel c's value at in-tile ordinal u sits at byte u·Q + Fᶜ — the table's
  forms with k = u·C + c" is algebraically exact: k div C = u and k mod C = c.
  All correct.
- D10: values 1,0,1,0,1,0,1,0 LSB-first = 0b01010101 = 0x55; values 8–9 =
  1,0 → 0x01; pad bits 2–7. Fill false → `55 01`; fill true → 0x01 | 0xFC =
  0xFD → `55 FD`. Decoded size ⌈10/8⌉ = 2. All correct.
- D11: ⌈5/4⌉ = 2 per axis; tile (1,1) covers 4–7 on both axes, so 16 positions
  of which only (4,4) is inside extents → 15 padding positions. P·B = 16·2 =
  32 bytes. Fill 0xABCD little-endian = `CD AB`. The real sample is at in-tile
  ordinal 0. All correct.
- D13: 74 × 20 = 1,480, entry at [1,480, 1,500). Channel 3's block is
  [3·32, 4·32) = entries 96–127, 32 entries. All correct.
- D14: G = (4,8) row-major, so ordinals 0–7 are tile row 0; S = 8 gives runs
  [0,8), [8,16), [16,24), [24,32); rows 1–2 = ordinals 8–23 = runs 1 and 2.
  All correct, and the sentinel remark matches `[R-SLB-03]`'s "Sentinel tiles
  are transparent to run continuity".

### 2.5 Index segmentation (D12)

entry_count = 1,000,000.
- ⌈1,000,000 / 65,536⌉ = 16 segments; 15 × 65,536 = 983,040; last covers
  1,000,000 − 983,040 = 16,960. Matches "15 full, the last covering 16,960".
- CRC array = 16 × 4 = 64 bytes. Matches.
- Region = 1,000,000 × 20 + 64 = 20,000,064. Matches, and matches
  `[R-CNT-17]`'s formula entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4.
- k = 999,999 → segment 15; 999,999 − 983,040 = 16,959; 20 × 16,959 = 339,180
  segment-relative. Matches.
- CRC array at [20,000,000, 20,000,064); segment 15 at [19,660,800,
  20,000,000) because 983,040 × 20 = 19,660,800. Both match, and the span is
  339,200 bytes ≈ "~339 KB". Matches.
- "never more than one full segment (1.25 MiB)": 65,536 × 20 = 1,310,720 =
  1.25 MiB. Matches.
- entry_count = 0 → 0 × 20 + 0 × 4 = 0, extent (0,0), crc_of_crc_array = 0.
  Matches `[R-CNT-17]` and `[R-CNT-23]`.

### 2.6 Byte-shuffle (D16)

1.0f = 0x3F800000 → `00 00 80 3F`; 2.0f = 0x40000000 → `00 00 00 40`;
3.0f = 0x40400000 → `00 00 40 40`. s = 4, n = 3, output[i·n + j] = group j
byte i. I enumerated all twelve positions by hand:

```
i=0: 00 00 00   i=1: 00 00 00   i=2: 80 00 40   i=3: 3F 40 40
→ 00 00 00 00 00 00 80 00 40 3F 40 40
```

Identical to the document, and the prose gloss ("the three first bytes, the
three second bytes, then `80 00 40`, then `3F 40 40`") is right.

### 2.7 §21.8's instance arithmetic (D19)

§21.1 fixes the counting rule: "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written." I counted by hand first (61 / 102 / 45 /
44) and then mechanically:

```
awk -F'|' '{n=split($4,a,";"); tot+=n} END {print tot, NR}'   over each table
F TOTAL 61  rows 39
L TOTAL 102 rows 50
T TOTAL 45  rows 26
R TOTAL 44  rows 10
```

61 + 102 + 45 + 44 = 252; 39 + 50 + 26 + 10 = 125. §21.2's "39 conditions",
§21.3's "50", §21.4's "26", §21.5's "10", and §21.8's "125 conditions over 252
instances" are all exactly right. This was the number I most expected to have
drifted, and it has not.

### 2.8 §21.9's derivation note (D20)

- 2³² entries → ⌈2³²/2¹⁶⌉ = 2¹⁶ segments × 4 bytes = 262,144 = 256 KiB.
  Matches "still 256 KiB".
- 2³⁶ → 2²⁰ × 4 = 4 MiB. Matches "reaches 4 MiB at 2³⁶".
- 65,536 layers at ~200 bytes/record ≈ 12.5 MiB, below the 16 MiB directory
  row. Internally consistent.

### 2.9 §17.2's Window_Size note (D15)

It cites §14.2's worked examples as giving 18 and 30 bytes and §14.3's as
giving 2. D9 gives 18 and 30; D10 gives 2. The cross-references are accurate,
which is the sort of thing that rots first. The RFC 8878 reasoning is also
sound: with Single_Segment_Flag the Window_Size is the frame content size,
which `[R-COD-06]` already pins to the decoded size; without it the
Window_Descriptor's floor is 1 KiB, so a sub-1-KiB tile can only be a
single-segment frame, and `[R-COD-06]`'s "MUST NOT declare a window size
exceeding the tile's decoded size" is satisfiable. No fork.

### 2.10 §19.4's planar note (D17)

Entries for one spatial ordinal are N apart. If N ≥ 2¹⁶ then for any a,
(a + N) div 2¹⁶ ≥ a div 2¹⁶ + 1, so they land in different segments. The
"guaranteed" is genuinely guaranteed, not approximately.

### 2.11 §20.3's cost example (D18)

32 × 20 + ⌈32/65,536⌉ × 4 = 640 + 4 = 644. Matches, and "one entry re-pointed,
31 byte-identical" matches step 4's "every other entry byte-identical at its
disk-ordinal position".

### 2.12 Small ones

- D2: `température` in NFC = 11 characters with é as C3 A9 = 12 bytes; the
  quoted byte string `74 65 6D 70 C3 A9 72 61 74 75 72 65` decodes to exactly
  that. NFD é = `65 CC 81` gives 13. Correct.
- D6: binary32 1.0 = 0x3F800000, high 16 bits 0x3F80, stored `80 3F`; 0x7FC0 →
  0x7FC00000 = quiet NaN. Correct, and consistent with `[R-TYP-02]`'s
  "b × 2¹⁶" identification.
- D7: `04 | 74 65 6D 70 | 0C 00 | 04 | 00 00 C0 7F` = 12 bytes; type 12 =
  float32; fill length 4 = float32's element size, satisfying `[R-CNT-23]`'s
  "fill length equals the type's element size". 0x7FC00000 LE = `00 00 C0 7F`.
  Correct.
- D8: fills 0xFF, 0x00, 0x00 → (255, 0, 0); planar mixed case matches
  `[R-TYP-08]`'s "a single sample can mix decoded and fill channels".

---

## Part 3 — Table-against-prose cross-checks

These are the checks that found nothing, recorded so the coverage is
falsifiable.

**A3 trailer table vs §21.2.** Every valid-value cell has a register row:
version_major 0 → F20; unimplemented major → F21; flags incompat lane → F22;
generation domain → F13 and F3; dir_offset ≥ 16 → F11; dir_length ≥ 4 → F18;
dir_offset + dir_length ≤ F − 64 → F12; cfl = F → F19; cfl mod 64 → F15;
file_id ≠ 0 → F14; reserved zero → F17; trailer CRC → F16; magic → F10 (and
F2 byte-reversed). Nothing in the table lacks a row, and no row invents a
constraint the table lacks.

**A8 (§10.2 spaces) vs the defining sections.** record type 0x0003–0x7FFF
reserved / ≥0x8000 experimental = §7.3 + §10.3. channel layout 1,2 assigned /
3–255 reserved / no experimental = §14.1's `[R-SER-06]`. linearization 1 /
2–0x7FFF / ≥0x8000 = §11.4 (which further splits 2–3 and 4–0x7FFF, both
reserved — a refinement, not a conflict). sample type 1–13 / 14–0x7FFF /
≥0x8000 = §12.2 (again split 14–19 and 20–0x7FFF). codec 1–4 / 5–0x7FFF /
≥0x8000 = §17.2. filter 1,2 / 3–0x7FFF / ≥0x8000 = §17.3. index encoding 1 /
2–0x7F / ≥0x80 = §7.4 and §15.1. metadata encoding 1,2 / 3–0x7F / ≥0x80 =
§18.2. All eight agree. Appendix C (E2) restates all of them and agrees, with
one nomenclature drift: §12.2's note calls reserved 19 "a fixed-size raw-bytes
type" and Appendix C calls it "opaque". Same reservation, different word; I do
not consider that a defect since neither is a semantic assignment.

**A7 (§8.1 map) vs §4.5.** §4.5 names three exception classes: the front block
(equality), the terminal checksum fields (trailer CRC, directory CRC,
user-metadata extent CRC), and the extent of an unassigned record type. The map
has exactly one row for each of those plus rows for tile-index region and
stored tile. I checked the map is exhaustive over §5.2's coverage classes: a
record extent in major 1 is either a tile-index region (type 0x0001), a
user-metadata document (0x0002), or an unassigned type's extent — three rows,
three cases. §4.5's "interior checksum fields" list (segment CRC array, entry
crc, crc_of_crc_array) is likewise consistent: the array is covered by
crc_of_crc_array, the entry crc by its segment CRC, crc_of_crc_array by the
directory CRC. No gap and no double coverage.

**A13 (§15.3) vs §21.4.** §15.3's prose says "Six rows are marked *structural*"
and the table marks exactly rows 2–7. Mapping to the register: row 2 = T6,
row 3 = T7, row 4 = T10, row 5 = T8, row 6 = T11, row 7 = T12 (overflow half)
and T9 (F−64 half), row 8 = T1, rows 9/10 = L19/F36, row 11 = L41/L42/L43. The
register splits row 7 into two rows, which is finer, not different. T11's
qualifier "the value being distinct from the all-ones sentinel" correctly keeps
row 6 from swallowing the sentinel. I constructed the awkward case — offset =
S, length = 2⁶³ — and confirmed rows 3 and 6 both fire with the same outcome,
so no ambiguity in the verdict.

**A16 (§20.4 table) vs §7.2/§7.3.** Both registered types carry PE = 1, so the
MU = 0 / PE = 0 row is reachable only for unimplemented types — which is what
the surrounding prose says. The MU = 1 row's prohibition on "reordering
top-level records" sits oddly beside `[R-CNT-14]`'s "record semantics MUST NOT
depend on record order" and §20.4's own rationale ("as a multiset: record order
carries no meaning"), but it is a strictly-additional restriction that applies
only when an unknown critical record is present, so it is not a contradiction.
I looked hard at this one and let it go.

**A17 (§21.9) vs `[R-ERR-05]`.** See finding diagrams-05.

**A9 (§12.1) vs everything downstream.** 13 types, 12 numeric, element sizes
1/1/2/4/8/1/2/4/8/2/2/4/8. §12.1's "twelve types other than bool" = 13 − 1.
§13.2's "For the twelve numeric types" agrees. §14.2's "1 for bool" in the Q
sum agrees with element size 1. Appendix C's list agrees. §21.9's "all thirteen
sample types" in Appendix H agrees.

**A10 (§14.2 table) scope.** The table has no planar-bool row, and it should
not: the sentence introducing it reads "In a planar tile of a numeric channel
(§12.1), and in every interleaved tile", and §14.3 supplies the packed case.
§17.3's stride rule then covers all three (element size / Q / identity), and
its claim that L is divisible by s holds in each: P·Bᶜ by Bᶜ, P·Q by Q,
⌈P/8⌉ by 1. This is a place where a figure could easily have been wider than
its rule and is not.

**C1 (§5.1 three-commit figure).** Append order reconstructs exactly: commit 1
= layer A + dir₁/pad/tr₁ (the first ▓ run), commit 2 = layer B + dir₂/pad/tr₂
(the second ▓ run), commit 3 = dir₃/pad/tr₃. The figure explicitly disclaims
its own over-reach — "The grouping under the box is illustrative: a layer's
structures need not be contiguous or ordered (`[R-SLB-05]`)" — which is the
right move and which §20.5's figure then makes good on. Only quibble: the text
says the commit that *added* layer B "re-emit[ted] that layer's whole
tile-index region", where it in fact emitted it for the first time. Wording,
not substance.

**C2 (§9.2 crash figure).** Row 2 shows the interrupted commit's bytes
appended past trailₙ, which is exactly `[R-LIF-02]` step 1 ("begin writing at
exactly F"). Row 3 hatches precisely dirₙ/pad/trailₙ. The caption's claim that
a reader "MUST NOT scan backward (`[R-LIF-05]`)" matches §9.5. Consistent.

**C6 (§20.5 compaction figure).** Content survives, placement changes, index
regions get ′, file_id X→Y, generation 7→1 — all four match `[R-WRT-06]` and
`[R-WRT-07]`. The caption says "▓ marks slack" and then draws an unhatched
`pad` in both input and output, though §5.2 calls the pre-trailer pad slack;
§5.1's figure reconciles this explicitly ("the pad and the ▓ runs are slack")
and §20.5's does not, and the sentence "so slack is never carried" could be
misread as "the output has none". I judged this too thin to report: the output
figure itself draws the pad, so the misreading is self-refuting, and "carried"
plainly means "carried from the input".

**E1 (Appendix B).** I checked every one of the 24 rows against its cited
section. All correct, including the two derived ones (128-byte minimum, 1.25
MiB implicit in the segment size) and the three I recomputed (CRC parameters,
check vector, all-sentinel constant). Rank ≤ 255 and C ≤ 65,535 follow from
§7.4's u8/u16 as claimed.

**E4 (Appendix G).** Item 2's file_id construction — hash over [0, F − 64)
together with the trailer's other fields with file_id taken as zero — is
well-founded and does not collide with §9.3's nonzero requirement in any way
the text needs to state. Item 3's emission order is consistent with
`[R-CNT-14]`. Item 6 ("The sentinel for every all-fill tile") is a profile
addition, correctly not presented as a core rule. Item 1's claim that
byte-identity across implementations is unattainable for codecs 2–4 is
consistent with §17.2's note on DEFLATE's unused final-byte bits. Appendix G
is careful to say which of its items upgrade a SHOULD ("Everything else the
profile needs is already mandatory except gap content, which `[R-CNT-03]` only
advises and this profile requires"). That care is exactly what Appendix H
lacks — see diagrams-03.

---

## Part 4 — Findings

### diagrams-01 (CONTRADICTION) — §20.3's example (c) names a fill-value change as directory-only, which `[R-SER-05]` forbids for any layer with padding

Quoted, §20.3, lines 2835–2839:

> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, changing a channel's fill value. Only
> the directory is re-emitted.

and the figure that follows:

> ```
> before │front│ A: tiles+index │ dir₁│pad│tr₁│
> after  │front│ A: tiles+index │▓▓▓▓▓▓▓▓▓▓▓▓▓│ dir₂│pad│tr₂│
> ```

Against §14.5, `[R-SER-05]`, lines 1832–1841:

> Padding positions (§11.3) are serialized like any other position,
> and their content is fixed: at every padding position, a writer
> MUST encode, for each channel the position carries, that channel's
> fill value — the recorded fill bytes for a numeric channel, the
> recorded fill byte for an interleaved bool channel, the fill bit
> in a packed plane. Every pad bit (§14.3) MUST carry the plane's
> channel's fill bit. ... a verifier MUST
> check it, and a violation is a validity error at tile scope.

File conformance is a predicate on the live bytes (`[R-CNF-02]`: "File
conformance is a pure predicate on bytes"), and the fill a padding position
must encode is the one the *live* layer record records. So a commit that
changes a channel's fill value and re-emits nothing but the directory leaves
every carried-forward stored tile that has a padding position — or, for a
packed planar bool plane with P mod 8 ≠ 0, every carried-forward stored tile
full stop — encoding the *previous* fill, in violation of `[R-SER-05]`. The
register already carries the row: T4, "A padding position does not encode, for
each channel it carries, that channel's recorded fill value", verifier,
reject-tile; and T5 for the pad bits.

Worked instance, using §14.5's own example layer. Extents (5,5), tile extents
(4,4), one uint16 channel, fill 0xABCD, interleaved. Grid 2×2, four addressed
tiles:

| tile | covers | real positions | padding positions |
|---|---|---|---|
| (0,0) | x 0–3, y 0–3 | 16 | 0 |
| (0,1) | y 0–3, x 4–7 | 4 | 12 |
| (1,0) | y 4–7, x 0–3 | 4 | 12 |
| (1,1) | y 4–7, x 4–7 | 1 | 15 |

Suppose all four are stored, each 32 bytes, with the 39 padding positions
carrying `CD AB` as §14.5's example requires. Now perform example (c): commit a
new directory alone with the channel's fill changed to 0x0000. In generation
2, tiles (0,1), (1,0) and (1,1) are all T4 violations — 3 of 4 tiles
reject-tile, and the file is nonconforming. Example (c) says this is one of
"the three shapes a commit takes".

The bool case is worse because it does not need edge padding at all: a planar
bool plane with P = 10 (§14.3's example) has six pad bits in every tile, and
`[R-SER-05]`'s "Every pad bit MUST carry the plane's channel's fill bit" means
flipping that channel's fill invalidates *every stored tile of the plane*, edge
or interior. §14.3's example even gives both encodings: `55 01` for fill false
and `55 FD` for fill true.

What an implementer does wrong without this: an appender built to example (c)
offers "change fill value" as a cheap metadata edit, and silently produces
files that a verifier condemns tile by tile. The example needs the same
carve-out §16.2's `[R-SLB-04]` already spells out for slab declarations —
either re-emit the affected tiles or do not make the change — or it needs to
drop the fill case and keep only the two operations that really are
directory-confined.

Byte-level: no. `[R-SER-05]` is unambiguous and file conformance is defined
over live bytes, so both a compliant writer and a compliant verifier reach the
same answer; the example is simply wrong, and §2.1 makes it non-normative
("any text labeled *Note*, *Example*, or *Rationale*"). Two verifiers reading
this document both report the post-(c) file nonconforming at T4.

### diagrams-02 (CONTRADICTION) — §7.4's layer-record table carries no taxonomy class, and thirteen of its fields are classified nowhere in the document

Quoted, §4.7, `[R-ENC-16]`, lines 498–503:

> Every field this specification defines is classified **structural**,
> **semantic**, or **informative**.

and the note at lines 505–510:

> **Note.** Layout tables in this document give, per field: byte offset
> within the structure, size, type, name, taxonomy class, and valid
> range.

§7.4's table (lines 951–968) has the columns `| Field | Type | Constraint |`.
No class column. I grepped the whole document for the three class words:

```
grep -n "structural\b"  → §6.1 table, §6.2 table, §7.2 table, §15.1 table,
                          §18.2 table, §11.4 ("linearization field (`u16`,
                          structural)"), §12 ("a sample type (`u16`,
                          structural)")
grep -n "semantic\b"    → §6.2 table (generation, file_id), §13.1 ("The fill
                          value is semantic (§4.7)")
grep -n "informative"   → §4.7 only; no field anywhere carries the class
```

So of the layer record's fields, exactly three are classified: linearization
(§11.4), channel type (§12), and fill (§13.1). Unclassified: layer name,
layout, codec, filter, alignment A, slab S, slab alignment A_slab, rank d,
channel count C, dimension name, extent Eᵢ, tile extent Tᵢ, index_encoding,
entry_count, crc_of_crc_array. Every other layout table in the document —
§6.1, §6.2, §7.2, §15.1, §18.2 — carries the class column, so this is the one
table that drops it, and it is the table that defines the most fields.

`[R-ENC-16]` is a MUST-bearing requirement that also states the consequence of
the classification ("A field classified informative MUST NOT affect how any
byte is located or decoded, and a reader MUST NOT alter decoding based on
it"), so the classification is not decoration. For the layer record it is
simply absent.

Readings I can defend for what a reader should conclude about, say,
`crc_of_crc_array` or `entry_count`: (a) unstated because obviously structural,
so treat as structural; (b) unstated because the document's classification
obligation is discharged only where a table states it, so the field carries no
class. I picked (a) — every one of the fifteen is used to locate or decode
bytes by an explicit rule elsewhere (`[R-CNT-17]`, `[R-IDX-04]`, `[R-SER-02]`,
`[R-COD-03]`, `[R-SLB-01]`, …), so nothing turns on the missing label in
practice. What an implementer does wrong without it: nothing at decode time —
which is why I rate this a document defect rather than an interop hazard. But
`[R-ENC-16]` as written is not satisfied by the document, and the note at §4.7
promises a column that §7.4 does not deliver.

Byte-level: no. No layer-record field is a candidate for the *informative*
class (each has an explicit normative use), so no reader's decode path forks
on the missing label. Two implementations reading this text decode identically.

### diagrams-03 (CONTRADICTION) — Appendix H's conforming-writer checklist states `[R-CNT-03]`'s SHOULD as a writer obligation

Quoted, Appendix H, lines 3812–3819:

> **Conforming writer** — emits only conforming files (§2.3); records
> fill for every channel (`[R-TYP-06]`, §13.1); fill-encodes edge
> padding and pad bits (`[R-SER-05]`, §14.5); emits interleaved boolean
> values as only 0x00 or 0x01 (`[R-SER-08]`, §14.2); sorts
> user-metadata object members by their keys' UTF-8 bytes
> (`[R-MTA-05]`, §18.2); zeroes the gaps it creates (`[R-CNT-03]`, §5.2); follows the commit protocol
> including both barriers (§9.2); honors any alignment or slab it
> declares (§16).

Against §5.2, `[R-CNT-03]`, lines 607–611:

> Writers SHOULD zero the gaps they create — the run before an aligned
> tile or slab run, and the pre-trailer pad. A writer that does not
> leaves bytes indistinguishable from stale data and forfeits byte
> reproducibility (Appendix G); no conformance requirement rides on
> slack content either way.

Appendix H opens "A summary of each class's obligations", and every other item
in that writer list is a MUST-level rule. The eighth is not: §5.2 says in terms
that "no conformance requirement rides on slack content either way", and §5.2's
note repeats that slack "content is unconstrained, and no conformance
requirement applies to it". §21.6 registers unzeroed slack as a *non-violation*
("Bytes the live state does not claim … Slack: unconstrained content, no
conformance requirement"). So the checklist states a rule wider than the rule
is.

The document is elsewhere careful about exactly this distinction — Appendix G,
line 3782: "Everything else the profile needs is already mandatory except gap
content, which `[R-CNT-03]` only advises and this profile requires." Two
non-normative appendices, opposite treatments of the same SHOULD.

Readings: (a) Appendix H lists obligations of every strength and the reader is
expected to follow the citation to discover this one is advisory; (b) the list
is MUST-level, in which case it misstates `[R-CNT-03]`. I picked (a), because
Appendix H disclaims itself ("each entry's authority is the requirement or
section cited, never this summary") — but that disclaimer is doing a lot of
work for a list whose other seven items are all mandatory, and the fix is to
mark the item SHOULD.

Byte-level: no. A writer that zeroes and a writer that does not both emit
conforming files, and no verifier verdict differs — §21.6 forecloses it. The
defect is that the checklist would make a writer believe otherwise.

### diagrams-04 (CONTRADICTION) — F36's cell says four of the rows it cites catch the condition "at open"; the register's own Detected column says otherwise

Quoted, §21.2 row F36, line 3061:

> | F36 | A byte of the live committed state is claimed by two structures that do not belong to the same layer — across two layers, or a layer structure against another scope's structure; a claimant reaching the front signature block or the live trailer is instead caught at open by the bounds rows F11/F12, F34/F35, L17/L18 and T8/T9 | … | verifier | certification | `[R-CNT-13]` (R-CNT-02, R-IDX-03) |

Against the Detected cells of the rows it names:

> | L17 | A layer record's or sub-record's nonzero extent slot has extent_offset < 16, pointing into the front signature block | … | reader | **layer access** | `[R-CNT-13]` |
> | L18 | A layer record's or sub-record's extent reaches the live trailer or beyond: extent_offset + extent_length > F − 64 | … | reader | **layer access** | `[R-CNT-13]` |
> | T8 | A non-sentinel tile-index entry has offset < 16, addressing bytes of the front signature block | — | reader | **tile use** | `[R-IDX-03]` |
> | T9 | A non-sentinel tile-index entry's extent ends past F − 64, touching the live trailer or running beyond the committed file length | — | reader | **tile use** | `[R-IDX-03]` (R-CNT-13) |

§21.1 makes "open" a defined term, not a loose one: "Detection points name
§19.2's reader tiers — open, layer access, tile use, extent use — or
*certification*". Four of the eight rows F36 cites are due at layer access or
tile use, not at open. F11/F12/F34/F35 are indeed open.

Consequence for an implementer: a reader built from F36's cell would believe
that a tile-index entry pointing into the front block is caught during the open
walk, which §19.1's four steps cannot do — the open "consumes the trailer and
directory only — no extent slot's content, no tile index, no payload"
(`[R-RDR-01]`). Since §19.2's rule fixes the *latest* detection point and
permits earlier detection, a reader that tried would not be nonconforming, but
it would have to fetch every layer's whole index at open, which is the exact
cost `[R-RDR-01]` exists to bound.

Byte-level: no. Each cited row states its own detection point, and §21.1 says
"where a row and the rule it cites diverge, the rule governs"; the rules
(`[R-RDR-02]`, `[R-IDX-04]`, `[R-RDR-03]`) place these at layer access and tile
use unambiguously. No accept/reject verdict differs — only the tier at which a
conforming reader is *obliged* to have detected, and §19.2 licenses earlier
detection anyway.

### diagrams-05 (AMBIGUITY) — §21.9 claims to be the home of every validity-affecting limit, and its hard-limit list omits the alignment bounds and the minimum file size

Quoted, §21.9, `[R-ERR-03]`, lines 3264–3268:

> Every limit affecting which files are valid, or which files a
> conforming reader accepts, lives here (`[R-CNF-10]`). The table
> below states **minimum guarantees**, not caps

and `[R-ERR-05]`, lines 3308–3316:

> Some limits are instead **hard**: a file violating one is invalid,
> not merely large. They are stated where the structures forcing them
> are defined — a name at most 255 bytes (`[R-ENC-12]`, a `u8` length
> prefix); rank at most 255 and channel count at most 65,535 (§7.4's
> `u8` and `u16` fields); a layer declaring codec 4 at decoded tile
> size at most `0x7E000000` (`[R-COD-07]`); and every offset, length,
> extent, and count at most 2⁶³ − 1 (`[R-ENC-03]`). Each is a
> consequence of a field's width, an external format, or the value
> domain — never a number chosen here.

Limits that affect which files are valid and appear in neither §21.9 list:

- per-tile alignment A: "a power of two with 512 ≤ A ≤ 2⁶²" (§16.1,
  `[R-SLB-01]`; register row L40, reject-layer);
- slab alignment A_slab: "a power of two ≥ 1" bounded at 2⁶² (§7.4, §16.2;
  register row L30, reject-layer);
- minimum file size: "No conforming file is shorter than 128 bytes" (§5.1,
  `[R-CNT-27]`; register row F7, reject-file);
- dir_offset ≥ 16 and dir_length ≥ 4 (§6.2; rows F11, F18).

The first two are also counterexamples to `[R-ERR-05]`'s closing
generalization: 512 is not "a consequence of a field's width, an external
format, or the value domain" — §16.1's own note calls it "the legacy sector
floor", i.e. a number chosen here. Appendix B, which is only a finding aid,
does carry both alignment rows; §21.9, which claims to be the home, does not.

Permitted readings of "lives here": (a) §21.9 is the complete inventory of
validity-affecting limits, in which case it is incomplete by at least the four
above; (b) "here" means "in this specification", tracking `[R-CNF-10]`'s actual
words — "Every limit that affects which files are valid or which files a
conforming reader accepts lives in this specification, never only in an
implementation" — with §21.9 the collection point only for the reader-facing
minimum guarantees. I picked (b), because `[R-ERR-05]`'s very next clause says
hard limits "are stated where the structures forcing them are defined", which
concedes that they do not all live in §21.9. What an implementer does wrong
without this: builds its limits table from §21.9 alone and ships a writer that
emits A = 256 or a non-power-of-two A_slab, both of which are reject-layer to
every conforming reader.

Byte-level: no. §7.4's constraint column, §16.1 and §16.2 state the alignment
bounds directly and `[R-CNT-23]` assigns the outcome, so two implementations
that read those sections agree on every byte and every verdict; only an
implementer who treated §21.9 as exhaustive would diverge, and the document
elsewhere decides against him.

### diagrams-06 (OBSERVATION) — Appendix H's reader checklist drops one member of §2.3's five-item no-subset list

Quoted, Appendix H, lines 3800–3810:

> **Conforming reader** — … implements all four codecs, both filters,
> both layouts, and all thirteen sample types (`[R-CNF-03]`, §2.3); …

Against §2.3, `[R-CNF-03]`, lines 155–161:

> and MUST handle every codec and filter that §17 designates as core,
> both channel layouts (§14), every sample type that §12 designates
> as core, and every user-metadata encoding §18.2 assigns.
> There are no subset profiles: software that declines to support a core
> codec, a core filter, either channel layout, a core sample type, or an
> assigned user-metadata encoding is not a conforming
> reader, even if it reads all other conforming files correctly.

§2.3 gives five members; Appendix H repeats four and drops "every
user-metadata encoding §18.2 assigns". §18.2 makes the omission consequential
on paper — "Both assigned encodings are core: a conforming reader MUST be able
to decode encoding 2" — even though in practice it costs nothing, because
encoding 2 is zstd and the same decoder is already mandatory for codec 3
("whose decoder `[R-COD-11]` already requires of it for codec 3").

I have marked this OBSERVATION rather than CONTRADICTION because it is
decidable in one line and the practical consequence is nil; it is here because
the charter names checklists explicitly and because a checklist that
enumerates four of a five-item list is the class of drift worth catching
early. Byte-level: no — no implementation that satisfies the four can fail the
fifth.

---

## Part 5 — Things I checked and deliberately did not report

- **§21.3 L23's Instances cell** reads "extent_offset; extent_length;
  entry_count" for a condition that is a single equality predicate over
  extent_length and entry_count. §21.1 says "where a condition is a single
  predicate over several fields — a sum against a bound … — the fields it
  reads are not instances, because no two files could differ." Read strictly,
  L23 should be one instance, or three only if the field names are standing in
  for the three alternatives its condition text states (base mismatch; slot
  (0,0) with entry_count > 0; nonzero slot with entry_count = 0). F33 and L16
  use field names as proxies for alternatives in exactly that way, so I read
  L23 the same way. The count is self-consistent either way only under the
  three-instance reading, which is the one that makes §21.8's 252 come out —
  and it does come out, exactly. Not worth a finding.
- **§9.7's walk and sub-record extents.** §9.7 says the verifier "enumerates
  the live directory and its records, each record's extent"; it does not say
  "including sub-records". Read narrowly, a layer's user-metadata sub-record
  extent would fall to slack and its overlaps go unchecked, which would fork
  two verifiers' slack totals and one verdict. I did not report it because
  three other places decide it: §5.2's coverage class is "a record extent (the
  bytes any record's extent slot references, whatever the record's type)",
  `[R-CNT-13]` names "sub-record extents" explicitly, and L19's Instances cell
  lists "layer sub-record extents" as a claimant the verifier must check.
- **§20.5's figure drawing an unhatched `pad`** under a caption that says "▓
  marks slack". Reconciled by §5.1's figure and self-refuted by the output box
  itself.
- **§21.6's row "The file contains zero layers | A conforming file with an
  empty directory"** conflates zero layer records with an empty directory; a
  file with zero layers and one top-level user-metadata record has a non-empty
  directory. The same conflation is in the governing rule (`[R-CNT-14]`: "zero
  is valid: an empty directory is a conforming generation"), so the row does
  not diverge from the rule it restates, and nothing turns on it.
- **§5.1's "the commit that added layer B … re-emit[ted] that layer's whole
  tile-index region"** — it emitted it for the first time. Wording.
- **Appendix C's "19 opaque" vs §12.2's "a fixed-size raw-bytes type"** — the
  same reservation under two names, neither an assignment.
- **§7.1's extent_length ≥ 5 floor** is loose (the smallest JSON object is two
  bytes, so encoding 1 needs ≥ 6, and a zstd frame needs more). Loose floors
  are not defects; a 5-byte extent simply lands at R7.
- **Appendix E (changelog)** has one row and no content to be wrong about.

## Part 6 — Verdict on the charter

Every figure in the document that carries arithmetic reproduces under
independent computation: the three CRC constants, the entire 128-byte
annotated file, the 252-instance count, the segment arithmetic at
entry_count = 1,000,000, the shuffle permutation, the packed-bool bytes, the
edge-tile padding count, and every ordinal in §11.4 and §15.4. I found no
stale offset, no wrong width, and no mislabelled constant. The five real
defects are all of the "figure says more, or less, than its rule" kind:
§20.3(c) licenses a commit shape the padding rule forbids; §7.4's table drops
a column `[R-ENC-16]` needs; Appendix H's writer list promotes a SHOULD and
its reader list demotes a MUST; F36 misstates four detection tiers; §21.9
overstates its own completeness. None of them forks the bytes.
