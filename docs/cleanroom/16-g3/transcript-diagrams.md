# Cleanroom round 16 — Diagram auditor transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,282 lines, read in five passes covering every line). I ran `wc -l`, `grep`/`sed`
against that file only, and three Python scripts I wrote myself into my scratchpad:
a CRC-32C implementation used to check every checksum constant in the document, a
mechanical instance-counter over the §21 register tables, and a builder that
assembles a complete conforming TARN file from the document alone.

I did **not** open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`CLAUDE.md`, `README.md`, `conformance/`, or `spec/registry.json`. I ran no git
command, no web search, no web fetch, and did not list the output directory. I did
not consult any other array or image format as evidence; where prior-format
knowledge generated a suspicion (RFC 8878 window derivation, RFC 1951 bit-boundary
tails, LZ4 block bounds) I settled it against this document's own text and against
arithmetic I performed here.

Scratch files I created and read back: `crc.py`, `build.py`, `min.tarn`, in
`/private/tmp/.../scratchpad/round16/`.

---

## Part 0 — Method

My charter is every figure, byte-layout box, offset table, worked example, and
checklist. Per the brief I enumerated them all with line numbers *before* judging
any, so my coverage is checkable. Then I did the arithmetic myself — no eyeballing —
and finally built a real file end to end to find out where the document made me
guess.

### 0.1 Inventory — layout/data tables (24)

| # | Line | Table |
|---|---|---|
| 1 | 235 | §2.4 outcome classes (5 rows) |
| 2 | 694 | §6.1 front signature block layout |
| 3 | 737 | §6.2 trailer layout (11 rows) |
| 4 | 901 | §7.2 record header layout (5 rows) |
| 5 | 974 | §7.3 record types of format major 1 |
| 6 | 1003 | §7.4 layer-record inline payload (16 rows) |
| 7 | 1118 | §8.1 checksum coverage map (7 rows) |
| 8 | 1392 | §10.2 numeric identifier spaces (8 rows) |
| 9 | 1595 | §12.1 sample types (13 rows) |
| 10 | 1827 | §14.2 decoded size / offset of value k |
| 11 | 1995 | §15.1 index entry layout (3 rows) |
| 12 | 2043 | §15.3 entry validity (11 rows) |
| 13 | 2435 | §18.2 user-metadata encoding byte |
| 14 | 2584 | §18.4 standardized keys (6 rows) |
| 15 | 3099 | §20.4 updater obligations by stored flags (3 rows) |
| 16 | 3320 | §21.2 file-scope register (F1–F36) |
| 17 | 3364 | §21.3 layer-scope register (L1–L49) |
| 18 | 3421 | §21.4 tile-scope register (T1–T26) |
| 19 | 3468 | §21.5 ignored-record register (R1–R10) |
| 20 | 3486 | §21.6 conditions that are not violations (13 rows) |
| 21 | 3595 | §21.9 minimum-guarantee limits (8 rows) |
| 22 | 3931 | Appendix A annotated byte table (13 rows) |
| 23 | 3967 | Appendix B constants (26 rows) |
| 24 | 4064 | Appendix E changelog |

### 0.2 Inventory — ASCII figures (8)

| Line | Figure |
|---|---|
| 585 | §5.1 a file after three commits |
| 1066 | §7.4 layer-record payload byte listing (81 bytes) |
| 1197 | §9.2 what a crash sees (3 rows) |
| 1990 | §15.1 tile-index region layout box |
| 3031 | §20.3 shape (a) — a new layer |
| 3047 | §20.3 shape (b) — tiles added |
| 3070 | §20.3 shape (c) — directory-only change |
| 3186 | §20.5 what compaction reclaims |
| 3920 | Appendix A hex dump (128 bytes) |

### 0.3 Inventory — worked examples (19)

Lines 510, 574, 581, 1055, 1193, 1512, 1566, 1629, 1678, 1748, 1869, 1903, 1959,
2083, 2098, 2197, 2378, 3017, 3026, 3183. (§4.6 name bytes; §5.1 smallest file;
§5.1 three commits; §7.4 layer record; §9.2 crash; §11.2 grid; §11.4 ordinals;
§12.1 bfloat16; §12.3 channel entry; §13.3 fill tuples; §14.2 byte layout;
§14.3 packed bool; §14.5 padding; §15.4 million-entry index; §15.4 planar entries;
§16.2 slab runs; §17.3 byte-shuffle; §20.3 supersede cost; §20.3 three shapes;
§20.5 compaction.)

### 0.4 Inventory — checklists and numbered lists (11)

§4.6 three name constraints; §10.1 four extension vehicles; §17.2 "three frame
features"; §18.2 four document restrictions; §19.1 four open steps; §19.4 eight
tile-read steps; §9.2 six commit steps; §20.3 six appender steps; §22.2 three
properties; §22.3 four residues; Appendix D six choices; Appendix G ten profile
items; Appendix H five class checklists.

---

## Part 1 — Every checksum constant, recomputed

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — i.e. reflected table
constant 0x82F63B78 — and validated it against §4.5's own check vector before using
it on anything else.

| Where | Claimed | Computed | Verdict |
|---|---|---|---|
| §4.5 check vector, `"123456789"` | `0xE3069283` | `0xE3069283` | ✅ |
| §4.5, zero bytes | `0x00000000` | `0x00000000` | ✅ |
| §7.4 example, CRC over 4 sentinel entries (80 bytes) | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955` | ✅ |
| §7.4 example, `crc_of_crc_array` over `55 49 A3 80` | `0xC4EE982E`, stored `2E 98 EE C4` | `0xC4EE982E` | ✅ |
| §15.4 / Appendix B, full all-sentinel segment (2¹⁶ entries) | `0xEECB3BB2` | `0xEECB3BB2` | ✅ |
| Appendix A trailer CRC over trailer `[0,60)` | `0xE00938D2`, stored `D2 38 09 E0` | `0xE00938D2` | ✅ |

All six agree. Notably the §7.4 pair is not trivially reproducible by mistake: it
requires the sentinel to be exactly `FF ×16 00 ×4` (§15.2), the entry array to be
exactly `entry_count × 20`, and the segment for `entry_count = 4` to be *partial*
(so `[R-IDX-05]`'s all-sentinel constant is forbidden and the CRC must be computed).
The example gets all three right.

---

## Part 2 — Every figure and worked example, arithmetic redone

### §4.6, line 510 — `température`
NFC `74 65 6D 70 C3 A9 72 61 74 75 72 65` decodes t-e-m-p-é-r-a-t-u-r-e, 11 code
points, **12 bytes** ✅. NFD substitutes `65 CC 81` for `C3 A9`: 12 − 2 + 3 = **13**
✅. Appendix G item 10 repeats "12 bytes in NFC and 13 in NFD" ✅ consistent.

### §5.1, line 574 — smallest conforming file
Front `[0,16)`; directory `[16,20)`; 44 slack; trailer `[64,128)`. 16+4=20; 64−20=44
✅; F=128, 128 mod 64 = 0 ✅; dir_offset+dir_length = 20 ≤ F−64 = 64 ✅.
I re-derived `[R-CNT-27]`'s 128 independently: minimise F subject to F ≡ 0 (mod 64),
dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length ≤ F−64 ⇒ F ≥ 84 ⇒ F ≥ 128 ✅.

### §5.1, line 585 — a file after three commits
Eight cells: front, layer A, ▓, layer B, ▓, dir₃, pad, trail₃. I reconstructed the
history the caption asserts: commit 1 = front + A + dir₁/pad/trail₁; commit 2 = B +
dir₂/pad/trail₂; commit 3 touches no layer, so dir₃/pad/trail₃ only. That places
dir₁/pad/trail₁ in the first ▓ run and dir₂/pad/trail₂ in the second — exactly what
"The ▓ runs are the directories, pads and trailers of commits 1 and 2" says, and in
the right order ✅. Live state = front + both layers' structures + dir₃ + trail₃,
matching `[R-CNT-02]` ✅. The caption pre-empts over-reading ("The grouping under the
box is illustrative: a layer's structures need not be contiguous or ordered
(`[R-SLB-05]`)") — that is a figure correctly labelled *narrower than the rule* ✅.

### §7.4, line 1055 — a complete layer record payload
This is the newest byte figure in the document; I checked it byte by byte.

Field walk against §7.4's table order:

```
 0  03 73 73 74   name              4 bytes  (u8 len 3 + "sst")
 4  01            layout            1
 5  01 00         linearization     2
 7  01 00         codec             2
 9  01 00         filter            2
11  00×8          alignment A       8
19  00×8          slab S            8
27  00×8          A_slab            8
35  01            rank d            1
36  01 00         channel count C   2
38  01 78         dim name          2  ┐
40  64 00…        extent 100        8  ├ 18
48  20 00…        tile extent 32    8  ┘
56  04 74 65 6D 70 channel name     5  ┐
61  0C 00          type 12          2  ├ 12
63  04 00 00 C0 7F fill             5  ┘
68  01            index_encoding    1  ┐
69  04 00…        entry_count 4     8  ├ 13
77  2E 98 EE C4   crc_of_crc_array  4  ┘
                                   ---
                                    81
```

Every stated offset is the running sum of the widths before it ✅. The caption's
decomposition "4 + 34 … 18 … 12 … 13 — 81 exactly" checks: the nine scalars from
layout through channel count are 1+2+2+2+8+8+8+1+2 = **34**, and they are indeed
nine ✅. Dimension entry 2+8+8 = 18 ✅. Channel entry 5+2+5 = 12 ✅ and is
byte-identical to §12.3's `temp` entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` ✅.
Trailing 1+8+4 = 13 ✅. Total 81 ✅ with no residue, so the sub-record sequence is
empty ✅ (§7.4's "sub-records … to the end of the inline payload").

Grid: ⌈100/32⌉ = 4 ✅, interleaved so addressed-tile count = N = 4 = entry_count ✅.
`[R-CNT-17]`: 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = **84** ✅, matching the caption.
Index region = 80-byte entry array + one 4-byte segment CRC ✅ (§15.1's box).
Fill length 4 = float32 element size ✅ (`[R-CNT-23]`). Fill bytes `00 00 C0 7F` =
0x7FC00000 little-endian ✅. Both CRCs verified numerically above.

This example is clean. It is also the one place the document shows a *padded* layer
(4×32 = 128 > 100) without a stored tile, so `[R-SER-05]` never bites — correct, and
worth noting because a reader could otherwise think padding content was being
skipped.

### §9.2, line 1193 — what a crash sees
Row 2's ▓ tail is appended past trail_n, so the physical tail is not a trailer ✅
(`[R-LIF-05]`). Row 3's ▓ run spans exactly `dirₙ │pad│ trailₙ` — the structures
commit n+1 superseded ✅. The arrow in row 1 points at F ✅.

### §11.2, line 1512 — grid
(1024, 2048) / (256, 256) ⇒ G = (4, 8) ✅, N = 32 ✅, P = 65,536 ✅.
(1000, 2048): ⌈1000/256⌉ = ⌈3.906…⌉ = 4 ✅ — the example's point about the padded
last row.

### §11.4, line 1566 — ordinals
tile (1,0) → 1·8+0 = 8 ✅. (y,x) = (300,700) ⇒ t = (300 div 256, 700 div 256) =
(1, 2) ✅; s = 1·8+2 = 10 ✅; u = (44, 188) ✅; in-tile ordinal 44·256+188 = 11,452 ✅.
Planar C = 4: disk ordinal 2·32+10 = 74 ✅ (`[R-GEO-06]`'s c·N + s).

### §12.1, line 1629 — bfloat16
binary32 1.0 = 0x3F800000, high 16 bits 0x3F80 ✅, little-endian bytes `80 3F` ✅.
0x7FC0 ↔ binary32 0x7FC00000 quiet NaN ✅ — consistent with `[R-TYP-02]`'s
"b × 2¹⁶" identification.

### §12.3, line 1678 — channel entry
12 bytes as listed ✅ (see §7.4 walk above).

### §13.3, line 1748 — fill tuples
Interleaved r/g/b uint8 fills FF/00/00 ⇒ unstored tile reads (255, 0, 0) ✅
(`[R-TYP-08]`, declared channel order). Planar with `b` sentinel ⇒ decoded r, decoded
g, b = 0 ✅ — matches §3.2's "a single sample can mix decoded and fill values".

### §14.2, line 1869 — byte layout
(a) tile extents (2,3), P = 6, channels a(uint8, B=1), b(uint16, B=2): Q = 3 ✅,
decoded size P·Q = 18 ✅. In-tile coords (1,2) ⇒ ordinal 1·3+2 = 5 ✅ (row-major, last
dimension fastest). Byte range 5·3 = 15 → [15,18) ✅; F_a = 0 so a at 15, F_b = 1 so
b at 16–17 ✅.
(b) same layer planar: channel b's plane = P·B_b = 12 bytes ✅; ordinal 5 at 5·2 = 10,
bytes 10–11 ✅.
(c) t(float32) + m(bool) interleaved: Q = 4+1 = 5 ✅, decoded 30 ✅, ordinal 5 at
[25,30), t at 25–28, m at 29 ✅.
(d) The closing generalisation "channel c's value at in-tile ordinal u sits at byte
u·Q + Fᶜ — the table's forms with k = u·C + c": substituting k = uC + c into the
table's `(k div C)·Q + F_{k mod C}` gives `u·Q + Fᶜ` for 0 ≤ c < C ✅. The table and
the prose agree.

### §14.3, line 1903 — packed bool plane
Tile extents (2,5), P = 10, values alternating true,false,… from ordinal 0.
Byte 0 holds ordinals 0–7 in bits 0–7, LSB-first: bits 0,2,4,6 set = **0x55** ✅.
Byte 1 holds ordinals 8–9 in bits 0–1: 8 is true, 9 is false ⇒ 0x01 ✅, and
P mod 8 = 2 so bits 2–7 are pad ✅. Fill false ⇒ `55 01` ✅; fill true ⇒
0x01 | 0xFC = **0xFD** ✅ (`[R-SER-05]`'s "Every pad bit MUST carry the plane's
channel's fill bit"). Decoded size ⌈10/8⌉ = 2 ✅.

### §14.5, line 1959 — padding content
Extents (5,5), tile extents (4,4) ⇒ grid 2×2 ✅. Tile (1,1) covers y,x ∈ [4,8);
real positions need y<5 ∧ x<5 ⇒ exactly (4,4) ⇒ 1 real, **15 padding** ✅.
One uint16 channel ⇒ decoded 16·2 = **32 bytes** ✅. (4,4) has in-tile coords (0,0),
ordinal 0 ⇒ value 0 is the stored sample ✅; values 1–15 are `CD AB` = 0xABCD
little-endian ✅.
I checked the pigeonhole the example does *not* draw: tiles (0,1) and (1,0) are also
edge tiles with padding. The caption says "the edge tile at tile coordinates (1,1)",
which identifies the one it means rather than claiming it is the only one — correct
scoping.

### §15.4, line 2083 — million-entry index
entry_count = 1,000,000. ⌈10⁶/2¹⁶⌉ = **16** segments ✅; 15 × 65,536 = 983,040, so
the last covers 10⁶ − 983,040 = **16,960** ✅. CRC array 16 × 4 = **64 bytes** ✅.
Region = 20,000,000 + 64 = **20,000,064** ✅. Tile 999,999: segment 15 ✅,
segment-relative index 999,999 − 983,040 = 16,959, byte 20 × 16,959 = **339,180** ✅.
CRC array at [20,000,000, 20,000,064) ✅. Segment 15 at [983,040 × 20, 10⁶ × 20) =
**[19,660,800, 20,000,000)** ✅. "~339 KB" = 16,960 × 20 = 339,200 ✅.
"never more than one full segment (1.25 MiB)": 65,536 × 20 = 1,310,720 = 1.25 MiB ✅.
The "plus the CRC array" term is left unbounded, correctly — §1 calls it "the only
term that grows with the layer".
entry_count = 0 tail of the example: zero segments, zero-byte CRC array, slot (0,0),
crc_of_crc_array = 0 ✅ — and I note CRC-32C of zero bytes *is* 0x00000000, so the
mandated 0 and the computed value coincide rather than conflict.

### §15.4, line 2098 — planar entries
C = 4, N = 32 ⇒ entry_count = 128. Disk ordinal 74 ⇒ region bytes [1,480, 1,500) ✅.
Channel 3's block = [3·32, 4·32) = [96, 128) ⇒ entries 96–127, **32** copies of
`FF ×16 00 ×4` ✅.

### §16.2, line 2197 — slab runs
N = 32, S = 8 ⇒ runs [0,8), [8,16), [16,24), [24,32) ✅ (`[R-SLB-02]`: run r starts at
block_start + r·S, single block [0,N) for interleaved). Grid 4×8 row-major ⇒ ordinals
8–23 are tile rows 1–2 = runs 1 and 2 exactly ✅. Sentinel at ordinal 10 ⇒ run 1's
stored tiles 8,9,11…15 packed with no gap ✅ (`[R-SLB-03]`: "Sentinel tiles are
transparent to run continuity").

### §17.3, line 2378 — byte-shuffle
Decoded image for 1.0f, 2.0f, 3.0f: `00 00 80 3F | 00 00 00 40 | 00 00 40 40`,
s = 4, n = 3 ✅. I applied `[R-COD-10]`'s "byte i of group j at offset i·n + j"
position by position:

```
out[0..2] = g0[0],g1[0],g2[0] = 00 00 00
out[3..5] = g0[1],g1[1],g2[1] = 00 00 00
out[6..8] = g0[2],g1[2],g2[2] = 80 00 40
out[9..11]= g0[3],g1[3],g2[3] = 3F 40 40
```

= `00 00 00 00 00 00 80 00 40 3F 40 40` ✅ exactly as printed, and the prose gloss
("the three first bytes, the three second bytes, then `80 00 40`, then `3F 40 40`")
matches ✅. I also confirmed the divisibility premise: planar L = P·Bᶜ with s = Bᶜ;
interleaved L = P·Q with s = Q; packed bool s = 1 — divisible in all three ✅.

### §20.3, line 3017 — supersede cost
32-tile interleaved layer: new index region = 32·20 + ⌈32/2¹⁶⌉·4 = 640 + 4 = **644**
✅ ("one entry re-pointed, 31 byte-identical" ✅).
The preceding Note's "editing one sample of a 10⁶-tile layer appends about 20 MB of
index": 10⁶ × 20 = 20,000,000 ✅.

### §20.3, line 3026 — the three shapes
(a) new layer: A's structures untouched, old dir/pad/trailer hatched, B appended ✅.
(b) tiles added: old index hatched, index′ re-emitted whole, retained payloads do not
move ✅ — consistent with `[R-WRT-04]` step 4 ("necessarily at a new placement
(`[R-LIF-01]`)").
(c) directory-only: I checked the three instances the caption gives against §20.3
step 4's bar. Clearing a slab declaration ✅ (`[R-SLB-04]` expressly permits it).
Renaming a layer ✅ (touches no stored byte). Changing a channel's fill "on a layer
with no padding position and no pad bit" ✅ — the only thing §14 fixes from fill is
padding/pad-bit content, so with neither present no stored byte is reached; the
reference array changes only at *sentinel* tiles, which step 4 does not protect. The
caption's own carve-out ("A fill change on a layer that **stores** a tile carrying
either is not an appender's operation at all") is the right one ✅.

### §20.5, line 3183 — what compaction reclaims
Structure of the figure is right: slack runs vanish, extent slots re-point, indexes
carry ′, file_id X→Y, generation 7→1 ✅ (`[R-WRT-06]`, `[R-WRT-07]`).
**Its caption is not right** — see Finding diagrams-02.

### Appendix A, line 3920 — the annotated minimal file, byte by byte

```
0000  89 54 41 52 4E 0D 0A 1A   front magic  \x89 "TARN" CR LF ^Z   ✅ §6.1
0008  00×8                      front reserved                       ✅
0010  00 00 00 00               directory = CRC-32C(zero bytes) = 0  ✅ §7.1/§4.5
0014  00×44                     pre-trailer pad (slack)              ✅ §6.2
0040  8A 4E 52 41 54 0D 0A 1A   trailer magic \x8A "NRAT" CR LF ^Z   ✅
0048  01 00                     version_major = 1                    ✅
004A  00 00                     version_minor = 0                    ✅
004C  00 00 00 00               flags = 0                            ✅ §6.3
0050  01 00…                    generation = 1                       ✅
0058  10 00…                    dir_offset = 16                      ✅
0060  04 00…                    dir_length = 4                       ✅
0068  80 00…                    committed_file_length = 128          ✅
0070  EF CD AB 89 67 45 23 01   file_id = 0x0123456789ABCDEF LE      ✅
0078  00 00 00 00               trailer reserved                     ✅
007C  D2 38 09 E0               CRC = 0xE00938D2 over trailer[0,60)  ✅ recomputed
```

Every offset in the annotation table lands on the field the trailer layout table
puts there (0/8/10/12/16/24/32/40/48/56/60 + 64 ⇒ 64/72/74/76/80/88/96/104/112/
120/124) ✅. `8A 4E 52 41 54` is "NRAT", i.e. TARN reversed, and its first byte 0x8A
differs from the front block's 0x89 — which is exactly the property §6.2's Note
claims ("a recovery scan never matches the front block") ✅. I also checked F1's
premise: byte-reversing either constant yields neither constant ✅.

The prose after the dump: two-request remote open ✅; "112 bytes covering [16, 128)"
= 128 − 16 = 112 ✅; "§19.1's four-step open" — §19.1 has exactly four steps ✅.

### Appendix B — constants
I checked all 26 rows against their defining sections. Every value matches: front
block, trailer magic, 64-byte trailer, 128-byte minimum, dir_offset ≥ 16 /
dir_length ≥ 4, extent_length ≥ 5, 0x00/0x01 booleans, `application/vnd.tarn`,
24-byte record header, 20-byte index entry, 2¹⁶-entry segment with 4-byte CRC,
`FF ×16 00 ×4` sentinel, 0xEECB3BB2, CRC parameters and check vector, 0–2⁶³−1
domain, 255-byte names, rank ≤ 255 / C ≤ 65,535 (from §7.4's `u8` and `u16`),
1 ≤ S ≤ 2⁶³−1, A power-of-two 512…2⁶², A_slab power-of-two 1…2⁶², 65,536-byte
discovery window, 1–16 MiB tile guidance, `28 B5 2F FD`, `0x7E000000`, `tarn.`, and
the eight-item guarantee list. The guarantee row reproduces §21.9's eight rows
exactly and in order ✅.

### Appendix C — registry snapshot
13 sample types with the same names and numbering as §12.1 ✅; reservations 14–19
match §12.2's Note ✅; codecs 1–4 ✅; filters 1–2 ✅; layouts 1–2 ✅; linearization 1 ✅;
index encodings 1 ✅; metadata encodings 1–2 ✅; record types with §7.3's fixed flags
✅; six standardized keys matching §18.4 ✅.

---

## Part 3 — Register arithmetic, done mechanically

I parsed §21.2–§21.5's tables and counted instances by §21.1's own rule ("Instances
within a cell are separated by semicolons, and a cell reading — is one instance"):

```
rows: F=36  L=49  T=26  R=10   total 121
instances: F=58  L=116  T=57  R=44   total 275
```

§21.2 declares 36 ✅, §21.3 declares 49 ✅, §21.4 declares 26 ✅, §21.5 declares 10 ✅,
and §21.8 declares "121 conditions over 275 instances" ✅. That is an exact match on
both numbers — the strongest single piece of evidence that the register has not
drifted since its last edit.

### 3.1 The instance criterion, applied row by row

The brief warns that a rule in this repair set is on its fourth revision. §21.1's
Instances paragraph is the obvious candidate, so I applied its criterion to every row
rather than sampling.

Criterion as stated: (a) layout-varying derived quantities are enumerated per layout;
(b) a *differs from* / *does not equal* between two magnitudes enumerates two
directions, an *exceeds* / *larger than* enumerates one; (c) a checksum or a byte
pattern against a constant enumerates no direction; (d) a nonzero test is not a
comparison at all.

Layout axis (three shapes: interleaved P·Q, planar numeric P·Bᶜ, packed bool ⌈P/8⌉):
T3 = 3×2 = 6 ✅, T14 = 3×2 = 6 ✅, T21 = 3×1 = 3 ✅, T22 = 3×2 = 6 ✅, L44 = 3×1 = 3 ✅,
T26 = 3 ✅. Two-layout axis: L21 = 2×2 = 4 ✅. T4's four instances split by carried
channel kind rather than by layout formula, which its own condition text licenses ✅.

Magnitude axis: F17 = 2 ✅, L30 = 2 ✅, L22 = 2 + 2 alternatives = 4 ✅, F23/L12 = 2 ✅.
No-ordering: F8, F14, F20, L37, L38, T1 all = 1 ✅. Nonzero tests: L20, L27, L28 = 1
✅, and L29/L39 enumerate value-set alternatives without adding a direction for the
`S ≠ 0` / `A ≠ 0` guard ✅.
Value-set rows track their own sections' partitions exactly: L31 = 3 ✅, L33 = 4 ✅
(matching §11.4's 0 / 2–3 / 4–0x7FFF / ≥0x8000), L34 = 4 ✅ (§12.2's 0 / 14–19 /
20–0x7FFF / ≥0x8000), L36 = 2 ✅ (§14.1 has no experimental range), L43 = 3 ✅,
L45 = 3 ✅.
Family rows: T24 = "any codec" = 1 ✅ (the criterion's own example); T15 = 2 and
T25 = 3 ✅ (the criterion's other two examples).

The one place the criterion is applied unevenly is T18 against R4 — see Finding
diagrams-04.

### 3.2 F33 / F7 asymmetry
F33 lists five containers including "directory region"; F7 lists the same four minus
the directory. That is correct, not an omission: F7's condition is a structure lying
*after the directory's end*, which the directory cannot do to itself. F33's
"claimant reaching the front signature block or the live trailer is instead caught by
the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9" — I checked all eight and they
cover both bounds at all four tiers (trailer/dir, top-level record, layer record and
sub-record, index entry) with nothing left over ✅.

### 3.3 §21.2's preamble
"Four rows are outside that reasoning and do reach it … F8 and F1's trailer-magic
instance, F14's trailer CRC … and F6 with F1's front-block instance." Distinct rows:
F1, F6, F8, F14 = **four** ✅. And they are precisely the rows whose subject
`[R-CNT-24]` fixes across every major (trailer magic, trailer CRC, front block) ✅.
F15 (trailer reserved bytes at offset 56) is correctly *not* among them, since
`[R-CNT-24]` leaves the other 48 trailer bytes redefinable ✅. F18's carve-out
(version_major = 0 is outside the premise, not an exception) is right ✅.

### 3.4 Register completeness, sampled against the rules
I walked every requirement identifier that can produce a file-level witness and
looked for its row. File scope: `[R-CNT-06]`'s ten gates → F8–F18 with F2/F3 for the
domain ✅; `[R-CNT-04]` → F1/F6 ✅; `[R-CNT-05]` → F7 ✅; `[R-CNT-11]` → F20 ✅;
`[R-CNT-12]` → F24/F25/F26/F29 ✅; `[R-CNT-13]` → F30/F31/F32/F33 ✅; `[R-CNT-14]` →
F34 ✅; `[R-CNT-15]` → F35/F36 ✅; `[R-CNT-22]` → F28 ✅; `[R-CNT-25]` → F21/F22 ✅;
`[R-MTA-03]` → F23 ✅; `[R-MTA-05]` → F27 ✅; `[R-ENC-02]` → F1 ✅; `[R-ENC-15]` → F4 ✅;
`[R-CNT-27]` → F5 ✅.
Layer scope: `[R-CNT-23]`'s enumerated violations map to L27/L28/L30/L31/L34/L36/
L43/L45 ✅; geometry `[R-GEO-01]`→L32, `[R-GEO-05]`→L33 ✅; `[R-TYP-03]`→L34,
`[R-TYP-07]`→L35 ✅; `[R-IDX-04]`→L37/L38 ✅; `[R-SLB-01]`→L39/L40,
`[R-SLB-03]`→L41/L42 ✅; `[R-COD-03]`→L43, `[R-COD-07]`→L44, `[R-COD-09]`→L45 ✅.
Tile scope: §15.3's eleven rows map onto T6/T7/T10/T8/T11/T9+T12/T1 plus the three
verifier rows that surface as L18/F33/L40–L42 ✅; §17.2's codec constraints map onto
T14–T25 ✅.
`[R-SER-04]` is withdrawn and §14.4's Note says so; no prefix has a numbering gap
(I checked all 20 prefixes mechanically — CNF 1–12, CNT 1–27, COD 1–11, ENC 1–16 plus
the illustrative ENC-100, ERR 1–5, EXT 1–5, GEO 1–6, IDX 1–5, LIF 1–8, MDL 1–2,
MTA 1–10, PRV 1–5, RDR 1–4, SEC 1–7, SER 1–9, SLB 1–5, TYP 1–10, VEC 1–4, WRT 1–9,
none missing) ✅.

---

## Part 4 — Building the thing

I built a complete conforming file from the document alone: a rank-1 interleaved
layer `sst` (extent 4, tile extent 4), one uint8 channel `v` with fill `0x00`,
codec 1, filter 1, one stored tile carrying 1,2,3,4.

Derivations I had to make and where each came from:

- G = ⌈4/4⌉ = 1, N = 1, P = 4 (§11.2), interleaved ⇒ entry_count = N = 1 (§11.2).
- Q = ΣBᵢ = 1, decoded size = P·Q = 4 (§14.2's table).
- Index extent_length = 1×20 + ⌈1/2¹⁶⌉×4 = **24** (`[R-CNT-17]`).
- Layer record flags = MU 1 | PE 1 = bits 0 and 1 = **0x0003** (§7.2's header table +
  §7.3's registry row). §4.4 fixes bit 0 as least significant, so this is not a guess.
- Inline payload = 4 + 34 + 18 + 6 + 13 = **75** bytes (§7.4's table order; the
  channel entry is 6 here because name "v" is 1 byte and uint8 fill is 1 byte).
- Directory = 24-byte header + 75-byte payload + 4-byte CRC = **103** bytes (§7.1,
  §7.2).
- Pad: directory ends at 147, `[R-LIF-02]` step 5 pads to the next 64-byte boundary
  ⇒ 192, trailer [192, 256), F = 256, F mod 64 = 0 ✅.

Resulting file (256 bytes, verified against every gate in §6.2 and every coverage
rule in §5.2):

```
0000  89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00
0010  01 02 03 04 10 00 00 00 00 00 00 00 04 00 00 00
0020  00 00 00 00 F4 8C 30 29 AD 4E 85 8A 01 00 03 00
0030  4B 00 00 00 14 00 00 00 00 00 00 00 18 00 00 00
0040  00 00 00 00 03 73 73 74 01 01 00 01 00 01 00 00
...
00c0  8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
00d0  01 00 00 00 00 00 00 00 2C 00 00 00 00 00 00 00
00e0  67 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00
00f0  EF CD AB 89 67 45 23 01 00 00 00 00 FB 50 79 7B
```

Live-state partition: front [0,16), stored tile [16,20), index region [20,44),
directory [44,147), trailer [192,256); slack = 45 bytes, all of it the pre-trailer
pad; no two claimants overlap; every claimant lies in [16, F−64) except the front
block and trailer, which `[R-LIF-08]` claims separately ✅.

**Where I had to guess: nowhere in this build.** Every width, every order, every
derived quantity, and every checksum scope came out of a single named table or
requirement. The only free choices the document leaves — placement of the tile and
index, file_id value, and the *content* of the pad — it explicitly marks as free
(`[R-SLB-05]`, §9.3, `[R-CNT-03]`). That is a real result: the container half of this
document is implementable cold.

Extension probes I ran against the same build, all of which the document settles
without inference: entry_count = 0 ⇒ slot (0,0), zero-byte CRC array,
crc_of_crc_array = 0 (and CRC-32C of zero bytes *is* 0, so the mandated constant and
the computed one coincide); a planar bool plane ⇒ decoded size ⌈P/8⌉ with byte-shuffle
degenerating to identity (§17.3); a sub-1 KiB tile under codec 3 ⇒ single-segment
frame only, because a Window_Descriptor cannot express less than 1 KiB (§17.2's Note,
which I re-derived: windowLog = 10 + Exponent, minimum 2¹⁰).

---

## Part 5 — Findings

### diagrams-01 — §21.7 says §20.3 step 4's bar is witnessed only through structurally-constrained bytes; T14, T17, T3 and T25 witness it elsewhere

**Kind:** CONTRADICTION
**Location:** §21.7 `[R-ERR-01]`; §21.4 rows T3, T14, T17, T25; §20.3 step 4
`[R-WRT-04]`

§21.7 says:

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

§20.3 step 4 bars a change that alters, for a tile stored in the superseded
generation, any of five things:

> the set of padding positions (§11.3) and the content
> `[R-SER-05]` fixes there, the decoded size, the byte offset of any
> sample within the decoded tile image, or the codec and filter that
> produced the stored bytes.

Three of those five have live-state witnesses that have nothing to do with padding
positions, pad bits, or boolean bytes. I constructed two:

*Decoded size.* Interleaved layer, extents (4), tile extents (4) — so P = 4 and
there are no padding positions at all — one channel of type uint16, codec 1, one
stored tile of length 8. A commit changes the channel type to uint32. The decoded
size becomes P·Q = 16. `[R-COD-04]` requires a codec-1 entry's length to equal the
decoded size, so **T14** fires: "Codec 1 (none) declared and a non-sentinel index
entry's length differs from the tile's decoded size". Under any compressing codec the
same change is witnessed by **T3**: "The decoded payload's byte length is not exactly
the tile's decoded size derived from the layer's declarations". Neither row involves a
byte §14 structurally constrains, and the layer has no padding position, no pad bit
and no boolean channel.

*Codec.* Same layer, codec changed from 1 to 3. The stored bytes are raw, so **T17**
fires: "Codec 3 (zstd) and the stored bytes do not begin with the compressed-frame
magic 28 B5 2F FD", or **T25** if they happen to start with the magic and then fail.
Again no structurally-constrained byte is involved.

So the conjunct "*and* the change reaches a byte §14 structurally constrains" is
false, and "the §21.4 rows firing there and nowhere else" is false of §21.4 as a
whole. The only one of the five list items that genuinely produces no witness is the
byte-offset item — reordering channels of equal total stride leaves the tile the
right length under the right codec and simply mis-reads its contents — plus the
padding-set item where the layer has no padding.

**Reading I picked and why.** I read "the §21.4 rows firing there and nowhere else"
as a claim about which rows witness a step-4 violation, since that is what the
sentence is for: §21.1 makes §21.7 "the account, by class, of what fails" the
detectability gate, so an over-narrow account is a claim that a violation class is
undetectable when it is not. The alternative reading — that only T2/T4/T5 fire in the
padding/pad-bit/boolean case, which is true — leaves the leading "witnessed only
where … *and* …" still false, so it does not rescue the sentence.

**What an implementer does wrong without it.** A writer author reads §21.7 and
concludes that changing a channel's type or codec on a layer with no padding, no pad
bits and no booleans leaves no trace, and therefore treats §20.3 step 4 as a
formality there. It is not: the commit produces a file whose stored tiles every
conforming reader must reject at tile use. The remedy is to strike the conjunct and
name T3/T14/T17/T25 alongside T2/T4/T5, or to say the bar is witnessed wherever the
change reaches a byte §14 constrains *or* a quantity §14/§17 lets a reader
cross-check.

**Byte-level: no.** T3, T14, T17 and T25 are register rows with detector *reader* and
detection point *tile use* regardless of what §21.7 says about them, and §20.3 step 4
bars the change either way. Two conforming implementations cannot diverge on a byte
or a verdict over this; what diverges is what a writer author believes about
consequences.

---

### diagrams-02 — §20.5's compaction figure claims every record extent survives byte-for-byte, when both record extents in the figure are regenerated

**Kind:** CONTRADICTION
**Location:** §20.5, Example at line 3183; `[R-WRT-07]` at line 3162; §9.7
`[R-LIF-08]`; §5.2 `[R-CNT-02]`

The example's caption says:

> Every stored tile's bytes and every record extent survive
> byte-for-byte and the reference arrays are identical; extent slots
> are re-pointed and each relocated index region is regenerated — the
> ′ marks (`[R-WRT-07]`).

`[R-WRT-07]` says the opposite of the first clause for one class of extent:

> every retained record per §20.4, except that relocation re-points
> extent slots, regenerates each relocated tile-index region (entry
> offsets new; entry lengths, entry crcs, and sentinel entries
> unchanged; …; segment CRCs recomputed over the entries as
> re-emitted)

A tile-index region *is* a record extent on this document's own terms. §5.2 defines a
structure as "a stored-tile extent, a record extent (the bytes any record's extent
slot references, whatever the record's type, §7.2), the directory, or the trailer",
and §9.7 spells it out: "A layer record's extent slot addresses that layer's
tile-index region (§7.4), so the region enters the walk once, as that record's
extent."

The figure the caption annotates contains no user-metadata records and no unknown
records. Its only record extents are `A: index` and `B: index` — and both are marked
′ in the output, i.e. both are regenerated. So "every record extent survive[s]
byte-for-byte" is false of **every** record extent in the very figure it captions.

**Readings.** (i) "record extent" excludes index regions — unsupported; §5.2 and §9.7
both say it includes them, and no text carves them out. (ii) The trailing clause
"and each relocated index region is regenerated" is meant as the exception to the
leading clause — that is the charitable reading and the one I picked, but the leading
clause is stated unqualified and a reader who stops at the semicolon has been told
the wrong thing, which is precisely the "stale restatement" class.

**What an implementer does wrong without it.** A compactor author who takes the
caption at face value copies each layer record's extent verbatim to a new offset and
re-points the slot, leaving the old entry offsets inside. The output's index entries
then point at the *input's* tile placements. Nothing in the output's checksum chain
catches it if the author also copies the segment CRC array (the CRCs still match the
copied bytes), so the file verifies structurally and every tile read lands on the
wrong bytes or out of bounds. `[R-WRT-07]`'s normative text prevents this; the caption
undercuts it.

**Byte-level: no.** §2.1 makes the Example non-normative and §21.1's principle ("where
a row and the rule it cites diverge, the rule governs") has its analogue here:
`[R-WRT-07]` is unambiguous, so two implementations that read the normative rule
cannot disagree about output bytes. The exposure is to an implementer who reads the
figure instead of the rule.

---

### diagrams-03 — `[R-WRT-06]`'s "neither … nor … nor" list repeats its first alternative verbatim

**Kind:** OBSERVATION
**Location:** §20.5, `[R-WRT-06]`, lines 3139–3145

> A compactor MUST refuse to compact when any check `[R-WRT-09]`
> obliges fails, and MUST NOT emit a file carrying a violation it has
> detected: it can neither re-emit the structure corrected
> (`[R-WRT-05]`), nor keep it and call the output clean — and a record
> §20.4 does let it drop is no exception, dropping being available
> only where that table licenses it —
> nor re-emit it corrected (`[R-WRT-05]`).

The list has three branches and the third is the first restated: "re-emit the
structure corrected (`[R-WRT-05]`)" and "re-emit it corrected (`[R-WRT-05]`)" are the
same alternative with the same citation. A three-branch enumeration in normative text
that delivers two distinct branches is exactly what my charter asks me to check
("check every numbered list for items that are out of order, duplicated, or missing"),
and this one is not a numbered list only because it is written as a
neither/nor chain.

I looked for a reading under which the two differ — for instance "re-emit the
structure corrected" meaning the *whole structure* and "re-emit it corrected" meaning
the record §20.4 lets it drop, which the interposed em-dash clause introduces. That
reading is available but does not survive: the interposed clause says a droppable
record "is no exception", i.e. it is subject to the same three branches, not a fourth
option. Either way the sentence delivers two prohibitions dressed as three.

**What an implementer does wrong without it.** Nothing byte-visible. The union of the
branches is the same either way: refuse. I report it because the sentence is
normative, because a repair set that rewrote this section is where a duplicated
clause most plausibly came from, and because a reader who assumes the three branches
are distinct will spend time hunting for the distinction.

**Byte-level: no.** The requirement's effect — refuse to compact — is identical under
either reading, so no compactor's output bytes and no verifier's verdict turn on it.

---

### diagrams-04 — T18 and R4 enumerate the same skippable-frame condition at different granularity

**Kind:** OBSERVATION
**Location:** §21.4 row T18; §21.5 row R4; §21.1's Instances criterion; §21.8
`[R-ERR-02]`; §24 `[R-VEC-03]`

T18 splits "a skippable frame anywhere" into three placements:

> | T18 | Codec 3 (zstd) and the stored extent holds more than the single compressed frame | a second concatenated compressed frame; a skippable frame before the frame; a skippable frame after the frame; a skippable frame between two frames |

R4 — governing the identical constraint carried over to a user-metadata extent under
encoding 2 — collapses all three into one:

> …a skippable frame, top-level extent; a skippable frame, layer sub-record extent; a second frame, top-level extent; a second frame, layer sub-record extent…

§18.2 states R4's constraint set as "the frame magic; no skippable frame and no
second frame; no nonzero dictionary ID; no content-checksum flag", which carries the
"anywhere" from `[R-COD-06]`. So both rows range over the same three placements, and
one enumerates them while the other does not.

§21.1's criterion is what decides this: "a row whose check ranges over a family
without the condition changing shape states that range as a single instance (T24's
*any codec*), and one whose members give the condition materially different shapes
enumerates them (T15, T25)." T18's cell asserts that before / after / between are
materially different shapes. If they are, R4 owes six instances instead of two for
that alternative — eight more instances overall — and §21.8's 275 and
`[R-VEC-03]`'s "one vector for each instance it names" would both change. If they are
not, T18 owes two fewer.

**Reading I picked.** I take T18's cell as the document's own judgment that the three
placements are materially different shapes, because it is the more specific
statement and because the placements really do produce distinguishable files. On that
reading R4 under-enumerates. I did not adjust the totals: §21.1 says "the count is
therefore mechanical once the cell is written", so the cells as written are
self-consistent with 275 — this is a defect in the criterion's *application*, not an
arithmetic error, and I verified mechanically that the declared 121/275 match the
cells exactly.

**What an implementer does wrong without it.** Nothing at read time. A corpus builder
produces two vectors where six were intended, leaving a metadata extent with a
leading skippable frame untested against a rule that a whole-buffer zstd decoder is
most likely to tolerate — the same gap §17.2's Note flags for tiles ("Whole-buffer
zstd decoders that tolerate concatenated or skippable frames do not by themselves
enforce the exactly-one-frame rule").

**Byte-level: no.** The corpus is derivative (`[R-VEC-01]`), the rule is the same in
both places, and both readings oblige a reader to reject a skippable frame wherever it
sits. Only the vector count moves.

---

### diagrams-05 — `[R-CNT-04]` binds a "content sniffer", an actor no conformance class defines

**Kind:** OBSERVATION
**Location:** §6.1 `[R-CNT-04]` (line 713); §2.3; §2.1's phrasing-discipline Note;
§21.2 row F6

> A reader whose open leaves bytes
> [0, 16) **resident** — a local file read whole, a memory mapping, a
> speculative suffix window that reached offset 0, or any transport
> already holding them — and a content sniffer MUST verify the full block by byte
> equality before other processing, and MUST treat any mismatch as
> reject-file.

"Content sniffer" occurs exactly twice in the document: here, carrying two MUSTs and
a reader outcome, and once in the following non-normative Note ("Content sniffers
match the 16-byte front block by equality"). It is defined nowhere. §2.3 opens
"Conformance is defined for five classes" and names file, reader, writer, updater,
verifier — no sixth. §2.1's Note states the discipline the document says it follows:
"every requirement names the actor it binds (writer, reader, updater, verifier, or
file)".

So `[R-CNT-04]` places a MUST on a party outside every conformance class, and assigns
it an outcome — reject-file — drawn from §2.4's *reader* outcome vocabulary. A content
sniffer is not a conforming reader: §2.3's reader must accept every conforming file,
implement four codecs, two filters, thirteen sample types and two metadata encodings,
none of which a sniffer does. There is therefore no class under which violating this
MUST makes anything nonconforming, and no meaning for "reject-file" applied to a tool
that classifies rather than opens.

§21.2's row F6 restates the same rule and silently drops the sniffer: "the obligation
binds a reader holding those bytes resident, and a reader that would have to fetch
them MAY defer or omit the check (`[R-CNT-04]`); a verifier holds no such exemption".
That is the right thing for a register of file-conformance violations to say, but it
means the only enforceable half of `[R-CNT-04]` is the reader half, and the sniffer
clause carries no force anywhere.

**Readings.** (i) A content sniffer is a species of reader — but then the clause is
redundant, since a sniffer necessarily holds [0,16) resident and the first half
already binds it, and §2.3's reader obligations are ones no sniffer meets. (ii) It is
a sixth actor introduced ad hoc — which is what the text does, and what §2.1's
discipline forbids. I picked (ii) because the sentence lists the sniffer as a second
subject coordinate with the resident reader rather than as an instance of it.

**What an implementer does wrong without it.** A media-type sniffer author cannot tell
whether "MUST treat any mismatch as reject-file" obliges anything beyond "do not
report this as a TARN file", and a verifier author cannot tell whether checking
sniffer behavior is inside its remit. Deleting the clause (the first half already
covers any party holding the bytes) or defining the sniffer as a non-conformance-class
tool in §2.3 would settle both.

**Byte-level: no.** No byte sequence's status and no reader/verifier verdict turns on
it; the resident-reader half of `[R-CNT-04]` already fixes both, and F6 registers the
condition with detector *reader*.

---

## Part 6 — Things I checked and found clean, for the record

So that a later round need not redo them:

- All six checksum constants recomputed from §4.5's parameters (Part 1).
- Every offset and width in all four fixed-layout tables sums to the declared
  structure size: front block 8+8 = 16; trailer 8+2+2+4+8+8+8+8+8+4+4 = 64; record
  header 2+2+4+8+8 = 24; index entry 8+8+4 = 20.
- §6.3's permanent-across-majors claim: magic at F−64, version pair at F−56, CRC at
  F−4 over [F−64, F−4), 48 redefinable bytes, zero trailer slack — all consistent with
  the §6.2 table.
- §8.1's coverage map against §4.5's prose: every field of every structure is covered
  exactly once, with the three terminal fields, the front block and an unassigned
  record type's extent as the stated exceptions, and the three interior checksum
  fields each covered by exactly one further checksum (segment CRC array by
  crc_of_crc_array; entry crc by its segment CRC; crc_of_crc_array by the directory
  CRC). No gap.
- §10.2's eight identifier spaces against the eight defining sections; Appendix C's
  snapshot against both.
- §12.1's thirteen types, their element sizes, and "the twelve types other than bool"
  arithmetic.
- §14.2's offset formula reduced to the prose generalisation (k = uC + c).
- §15.3's eleven rows: six *structural*, three *verifier*, matching the prose's "Six
  rows are marked *structural*"; and the mapping of all eleven onto T1/T6–T12,
  L18/L40–L42 and F33.
- §21.9's derivation Note: 2³² entries ⇒ 2¹⁶ segments ⇒ 256 KiB CRC array, 2³⁶ ⇒
  4 MiB; 256 MiB is 16× §11.3's 16 MiB ceiling; 8 MiB is RFC 8878's recommended
  decoder window. (The Note explains seven of the table's eight rows; the 16 MiB
  user-metadata document row is the one it does not derive. I judged that too thin to
  file — the figure is cross-referenced from §18.2's Note and nothing turns on its
  provenance.)
- §24's "tens of gigabytes" for a 2³² -entry index: 2³² × 20 = 85.9 GB ✅.
- Every numbered and counted list: 4 vehicles, 3 name constraints, 3 frame features,
  4 document restrictions, 4 open steps, 8 tile-read steps, 6 commit steps, 6
  appender steps, 3 properties, 4 residues, 5 classes, 6 design choices, 10 profile
  items, 13 sample types, 5 outcome classes (4 reader + preserve-verbatim, correctly
  distinguished). None out of order, duplicated or missing.
- Appendix G's ten items against the rules each closes; item 2's hash input
  ([0, F−64) followed by trailer[0,60) with file_id zeroed) is well-defined and
  excludes both the file_id field and the trailer CRC that depends on it; item 3's
  sort key masks extent_offset for exactly the circularity reason it states; the
  closing paragraph's "Read the numbered items as the list" pre-empts a count
  mismatch.
- Appendix H's five checklists against §2.3, §2.4, §9.7, §19.2 and §20.4. The verifier
  checklist covers every verifier-detected register row (F7, F25–F28, F33, F36, L18,
  L25, L40–L42, L46–L49, T2, T4, T5, and T26 by way of "the check that detects it is
  T2's or T4's").
- A systematic scan for BCP-14 keywords sitting inside Note/Example/Rationale blocks
  (the class three rounds have already caught): five hits, at lines 112, 1209, 2071,
  2833 and 3013. Four are backed by normative text elsewhere — line 1209 restates
  `[R-LIF-05]`, line 2071's caching MAY is granted normatively in §19.4 step 3, line
  2833 is pure implementation technique, line 112 is descriptive. The fifth (§20.3's
  "Writers doing many small updates SHOULD batch them into one commit") has no
  normative counterpart, but nothing turns on it — §2.4 already says a SHOULD
  deviation is not a violation, and its sibling advice `[R-LIF-07]` *is* normative. I
  judged it a style nit rather than a defect and did not file it.
- A scan for singleton terms. The only load-bearing one is "content sniffer"
  (diagrams-05). "total sample-position count", "spatial-tile count" and "in-sample
  offset" are defined once and referred to thereafter by their symbols (N·P, N, Fᶜ),
  which is fine.
- §10.2's "Two spaces carry no experimental range" names the trailer's flag lanes,
  which is not a row in the table that promises to collect "The spaces". I considered
  filing this and did not: the sentence names §6.3 as the partitioner in the same
  breath, so no reader is left looking for a missing row, and flag lanes are not
  partitioned assigned/reserved/experimental at all.

## Finding count

This transcript contains **5** findings: diagrams-01 through diagrams-05.
