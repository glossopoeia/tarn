# Round 23 — Diagram auditor — working transcript

Charter: every figure, diagram, byte-layout box, ASCII table of offsets, worked
example, and checklist in `spec/tarn.md`, audited against the prose it
illustrates and the rules it cites.

## 0. Access and disclosure

I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four passes (lines 1–400, 400–850, 850–1300, 1300–1750, 1750–2200, 2200–2650,
2650–3100, 3100–3550, 3550–4000, 4000–4426). I read no ADR, no plan, no
conformance material, no registry, no git history, and I ran no search.

Two disclosures.

**(a) Contaminating context appeared before I began.** My runtime placed a
project instruction file and an index of the maintainer's private notes in my
context ahead of the task. I did not open any file it named and I have not used
anything in it. I note its appearance here as the brief requires, without
repeating its contents.

**(b) I read one file another agent wrote, in the shared scratchpad.** I wrote
a CRC-32C helper to `scratchpad/crc.py`, ran it (it printed my own strings), and
one minute later re-executed it from a second script — at which point it printed
*different* strings and a `crc32c` that omitted the final XOR. The path had been
overwritten by a concurrently running agent. To diagnose that I ran `ls -la` on
the scratchpad root and `cat` on `crc.py`. So:

- I saw the *filenames* in the shared scratchpad, including `round23/` (this
  round's output directory), `r23audit/`, `rows.txt`, `flat.txt`,
  `accumulated.diff`, `inst.txt`, `edits*.json`, `r89*.json`. I opened none of
  them and I did not list `round23/`.
- I read the *contents* of `scratchpad/crc.py` as another agent had left it. Its
  entire content is a table-driven CRC-32C implementation with a handful of
  print statements over the sentinel constants. It contains no prose, no
  conclusion about the specification, and nothing I did not independently
  compute myself. It is nonetheless a file I did not write, so it is disclosed.

I then moved all my work to `scratchpad/diagaudit-private/` and re-derived every
number from a self-tested CRC implementation of my own
(`crc32c("123456789") == 0xE3069283`, `crc32c(b"") == 0`).

The false alarm this caused is worth recording, because it briefly looked like a
finding: with the other agent's un-XORed `crc32c`, Appendix A's trailer CRC came
out `0x1FF6C72D` against a stored `0xE00938D2`. `0x1FF6C72D ^ 0xFFFFFFFF ==
0xE00938D2`. Appendix A is correct; my borrowed tool was not. This is the reason
the arithmetic below is all re-run under `diagaudit-private/c.py`.

---

## 1. Enumeration — every figure, box, table, example and checklist

Located mechanically before judging any of them, so coverage is checkable.

### 1.1 Fenced ASCII diagrams (8)

| Lines | Figure |
|---|---|
| 587–592 | §5.1 — a file after three commits (regions, ▓ = slack) |
| 1071–1090 | §7.4 — annotated layer-record inline payload, offset-annotated byte box |
| 1202–1211 | §9.2 — what a crash sees (three rows: committed / mid-commit / committed) |
| 3093–3097 | §20.3 shape (a) — a new layer |
| 3109–3113 | §20.3 shape (b) — tiles added to an existing layer |
| 3133–3136 | §20.3 shape (c) — a change confined to the directory |
| 3273–3279 | §20.5 — what compaction reclaims (input / output) |
| 4047–4056 | Appendix A — 128-byte hex dump of the minimal file |

Plus the un-fenced block-quoted region diagram at §15.1 lines 1996–1997
(`[ entry array ] [ segment CRC array ]`).

### 1.2 Tables (24)

| Line | Table | Kind |
|---|---|---|
| 235 | §2.4 outcome classes | rule restatement |
| 697 | §6.1 front signature block | byte layout |
| 740 | §6.2 trailer | byte layout |
| 904 | §7.2 record header | byte layout |
| 977 | §7.3 record types of major 1 | registry restatement |
| 1006 | §7.4 layer-record inline payload | packed layout |
| 1123 | §8.1 checksum coverage map | rule restatement |
| 1397 | §10.2 numeric identifier spaces | rule restatement |
| 1601 | §12.1 sample types | value set + element sizes |
| 1833 | §14.2 decoded size / offset of value k | arithmetic |
| 2001 | §15.1 tile-index entry | byte layout |
| 2049 | §15.3 entry validity | rule restatement |
| 2441 | §18.2 user-metadata inline payload | byte layout |
| 2631 | §18.4 standardized keys | registry |
| 3162 | §20.4 updater obligations by stored flags | rule restatement |
| 3410 | §21.2 file-scope register (F1–F36) | register |
| 3454 | §21.3 layer-scope register (L1–L49) | register |
| 3511 | §21.4 tile-scope register (T1–T26) | register |
| 3561 | §21.5 ignored records (R1–R10) | register |
| 3579 | §21.6 conditions that are not violations | rule restatement |
| 3703 | §21.9 minimum guarantees | limits |
| 4058 | Appendix A annotation table | byte-by-byte gloss |
| 4094 | Appendix B constants | finding aid |
| 4191 | Appendix E changelog | — |

### 1.3 Worked examples (block-quoted, labelled *Example*) — 22

513 (§4.6 `température`), 577 (§5.1 smallest file), 584 (§5.1 three commits),
1060 (§7.4 layer record payload), 1198 (§9.2 crash), 1518 (§11.2 grid),
1572 (§11.4 ordinals), 1635 (§12.1 bfloat16), 1684 (§12.3 channel entry),
1754 (§13.3 fill tuples), 1875 (§14.2 byte layout), 1909 (§14.3 packed bools),
1965 (§14.5 padding), 2089 (§15.4 million-entry index), 2104 (§15.4 planar
entries), 2203 (§16.2 slab runs), 2384 (§17.3 byte-shuffle), 3079 (§20.3
supersede cost), 3088 (§20.3 three shapes), 3270 (§20.5 compaction), plus
Appendix A (4041) and Appendix G's numbered profile (4215).

### 1.4 Checklists and numbered lists

- §9.2 `[R-LIF-02]` commit protocol, steps 1–6 (lines 1168–1180)
- §10.1 four extension vehicles, items 1–4 (1377–1381)
- §18.2 four decoded-document restrictions (2539–2566)
- §19.1 open algorithm, steps 1–4 (2693–2736)
- §19.4 tile-read algorithm, steps 1–8 (2822–2873)
- §20.3 append procedure, steps 1–6 (2946–3069)
- §21.9 hard-limits list `[R-ERR-05]` (3756–3777)
- Appendix G reproducible-writer profile, items 1–10 (4226–4353)
- Appendix H conformance checklists, five classes (4355–4426)

Numbering checked: every numbered list above is contiguous, in order, with no
duplicate or missing item. Register row ids checked mechanically: F1–F36,
L1–L49, T1–T26, R1–R10 — all contiguous from 1, none repeated, none skipped.

---

## 2. Arithmetic actually performed

Everything below was computed, not eyeballed.

### 2.1 CRC constants (§4.5, §7.4, §15.4, Appendix A, Appendix B)

Self-tested CRC-32C (reflected poly `0x82F63B78`, init/final `0xFFFFFFFF`):

```
crc32c("123456789")                     = 0xE3069283   (§4.5 check vector)     OK
crc32c(b"")                             = 0x00000000   (§4.5 check vector)     OK
crc32c(FF*16 00*4 repeated 4)  [80 B]   = 0x80A34955   (§7.4 example)          OK
   stored little-endian                 = 55 49 A3 80  (§7.4 example)          OK
crc32c(55 49 A3 80)                     = 0xC4EE982E   (§7.4 crc_of_crc_array) OK
   stored little-endian                 = 2E 98 EE C4  (§7.4 dump byte 77)     OK
crc32c(sentinel * 65536)                = 0xEECB3BB2   (§15.4, App. B)         OK
```

### 2.2 Appendix A, byte by byte

Parsed the hex dump and re-derived every annotation cell:

```
file length 128, F mod 64 = 0                                   OK (§6.2)
[0,8)   89 54 41 52 4E 0D 0A 1A  = front magic                  OK (§6.1)
[8,16)  zero                                                     OK (§6.1)
[16,20) 00 00 00 00 = crc32c(b"") over a zero-record sequence     OK (§7.1)
[20,64) zero, 44 bytes pre-trailer pad                           OK (§6.2, §5.1)
trailer magic 8A 4E 52 41 54 0D 0A 1A                            OK
version_major 1, version_minor 0, flags 0                        OK
generation 1, dir_offset 16, dir_length 4                        OK
committed_file_length 128 = physical size                        OK
file_id 0x0123456789ABCDEF (LE bytes EF CD AB 89 67 45 23 01)    OK
reserved [56,60) zero                                            OK
crc32c(trailer[0,60)) = 0xE00938D2 -> stored D2 38 09 E0         OK
dir_offset + dir_length = 20 <= F - 64 = 64                      OK
```

Trailer field offsets are contiguous and exhaust 64 bytes:
0+8=8, 8+2=10, 10+2=12, 12+4=16, 16+8=24, 24+8=32, 32+8=40, 40+8=48, 48+8=56,
56+4=60, 60+4=64 — confirming §6.3's "The format-major-1 trailer has zero slack:
every byte is assigned", and `[R-CNT-24]`'s 64 − 16 = **48** redefinable bytes.

`[R-CNT-27]`'s 128-byte floor re-derived independently: F ≡ 0 (mod 64),
dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64 ⇒ F ≥ 84 ⇒
F ≥ 128. Correct.

### 2.3 §7.4's layer-record payload, field by field

Field widths from the §7.4 table, summed:

```
name              1 + 3  =  4      dump offset  0   03 73 73 74   's','s','t'  OK
layout            1             4   01
linearization     2             5   01 00
codec             2             7   01 00
filter            2             9   01 00
alignment A       8            11   00*8
slab S            8            19   00*8
A_slab            8            27   00*8
rank d            1            35   01
channel count C   2            36   01 00
  -> "the nine scalars from layout through channel count" = 1+2+2+2+8+8+8+1+2 = 34   OK
dim entry     1+1+8+8 = 18     38   01 78 | 64 00.. (100) | 20 00.. (32)       OK
chan entry  1+4+2+1+4 = 12     56   04 74 65 6D 70 0C 00 04 00 00 C0 7F        OK
index_encoding    1            68   01
entry_count       8            69   04 00*7
crc_of_crc_array  4            77   2E 98 EE C4
  -> trailing fixed fields = 1+8+4 = 13                                        OK
TOTAL 4 + 34 + 18 + 12 + 13 = 81 = stated inline_length                        OK
```

Geometry: G = ⌈100/32⌉ = 4 ⇒ entry_count 4. `[R-CNT-17]`: 4×20 + ⌈4/2¹⁶⌉×4 =
80 + 4 = **84**, the stated extent length. Element size of float32 is 4 = the
fill length prefix (`[R-CNT-23]`). The 12 channel bytes are byte-for-byte
§12.3's `temp` entry, as claimed.

Also confirmed this example correctly exercises `[R-IDX-05]`'s *partial*-segment
rule: its one segment covers 4 entries, not 2¹⁶, so the all-sentinel constant
`0xEECB3BB2` must **not** substitute — and the example computes `0x80A34955`
instead. The example and the rule agree.

### 2.4 Every other numeric example

| Example | Check | Verdict |
|---|---|---|
| §4.6 `température` | NFC 12 bytes `74 65 6D 70 C3 A9 72 61 74 75 72 65` (11 chars); NFD `65 CC 81` for é ⇒ 13 | OK |
| §5.1 smallest file | 16 + 4 = 20, pad to 64 = 44 slack, trailer [64,128) | OK |
| §11.2 grid | ⌈1024/256⌉=4, ⌈2048/256⌉=8, N=32, P=65536; ⌈1000/256⌉=4 | OK |
| §11.4 ordinals | s = t_y·8+t_x: (0,0)→0, (0,1)→1, (1,0)→8; (300,700)→t(1,2), s=10; u=(44,188), 44·256+188=11,452; planar c=2: 2·32+10=74 | OK |
| §12.1 bfloat16 | 1.0f = 0x3F800000, high half 0x3F80, LE `80 3F`; 0x7FC0 ↔ 0x7FC00000 qNaN | OK |
| §12.3 channel entry | `04 't','e','m','p' 0C 00 04 00 00 C0 7F` = 12 bytes | OK |
| §13.3 fill tuples | interleaved (255,0,0); planar r,g decoded, b = fill 0x00 = 0 | OK |
| §14.2 | Q=1+2=3, size 6·3=18; ord (1,2)=1·3+2=5; bytes [15,18); planar b = 6·2=12, ord5 at 10–11; t/m: Q=4+1=5, size 30, [25,30) | OK |
| §14.2 closing identity | table offset (k div C)·Q + F_{k mod C} with k = u·C + c ⇒ u·Q + Fᶜ | OK |
| §14.3 packed bools | P=10, ⌈10/8⌉=2; alternating from true ⇒ bits 0,2,4,6 = 0x55; values 8,9 ⇒ 0x01; pad bits 2–7; fill true ⇒ 0x01\|0xFC = 0xFD ⇒ `55 FD` | OK |
| §14.5 padding | grid ⌈5/4⌉²=2×2; tile (1,1) spans 4–7 both axes ⇒ 1 real + 15 pad; 16·2 = 32 bytes; 0xABCD LE = `CD AB` | OK |
| §15.4 (a) | 1e6 entries ⇒ ⌈1e6/65536⌉ = 16 segments, last = 1e6−15·65536 = 16,960; array 64 B; region 20,000,064; k=999,999 in seg 15 at 20·16,959 = 339,180; seg 15 = [15·65536·20, …) = [19,660,800, 20,000,000); full segment 65536·20 = 1,310,720 = 1.25 MiB | OK |
| §15.4 (b) | disk ordinal 74 ⇒ region [1480,1500); channel-3 block [96,128) = 32 entries | OK |
| §16.2 | N=32, S=8 ⇒ runs [0,8),[8,16),[16,24),[24,32); rows 1–2 = ordinals 8–23 = runs 1,2 | OK |
| §17.3 shuffle | 1.0/2.0/3.0 f32 = `00 00 80 3F 00 00 00 40 00 00 40 40`, s=4, n=3; i·n+j ⇒ `00 00 00 00 00 00 80 00 40 3F 40 40` — re-derived position by position | OK |
| §20.3 cost | 32·20 + 4 = 644; 1 re-pointed, 31 identical; 10⁶·20 = 20 MB | OK |
| §21.9 note | 2³²/2¹⁶ · 4 = 2¹⁸ = 256 KiB; 2³⁶ ⇒ 2²² = 4 MiB; 65536 × 200 B = 12.5 MiB | OK |

**No numeric error found in any example in the document.**

### 2.5 §21.8's stated total — the flagged passage

> "Every row of §21.2 through §21.5 — 121 conditions over 277 instances — has at
> least one conformance vector (§24) whose expected outcome is that row's
> outcome, and one vector per instance."

Counted mechanically, applying §21.1's own arithmetic ("Instances within a cell
are separated by semicolons, and a cell reading — is one instance; the count is
therefore mechanical once the cell is written"):

```
§21.2  36 rows, ids F1..F36 contiguous,   58 instances
§21.3  49 rows, ids L1..L49 contiguous,  116 instances
§21.4  26 rows, ids T1..T26 contiguous,   55 instances
§21.5  10 rows, ids R1..R10 contiguous,   48 instances
TOTAL 121 rows                            277 instances
```

Both stated numbers are **exactly right**, and the per-section counts stated in
§21.2 ("36 conditions"), §21.3 ("49"), §21.4 ("26") and §21.5 ("10") each match
their delivered row count.

I then spot-audited the instance cells against §21.1's two stated axes (layout
formulas; magnitude direction on a *does not equal*, one direction on an
*exceeds*). Every one I checked is right, including the ones easiest to get
wrong:

- T3 and T14 each 6 = three layout formulas × two magnitude directions; T21 = 3
  (one direction, "larger than"); T22 = 6 (two directions, "does not equal").
- L21 = 4 (interleaved N / planar C·N × two directions). L22 = 4 (two directions
  plus the two alternatives the condition text states).
- L29 lists `A_slab = 0` as an instance and L39 does **not** list `A = 0` —
  correct asymmetry: A = 0 means "none declared" and is valid, while A_slab = 0
  with S ≠ 0 is not.
- L2's nine derived quantities, with domination arguments checked:
  (C−1)·N + (N−1) = C·N − 1 < C·N; and Q = ΣBᵢ ≥ C so P·Q ≥ P·C = V. Both hold.
- F2's six instances correctly omit `file_id`, which is a u64 but is not an
  "offset, length, extent, or count" and so is not bounded by `[R-ENC-03]`
  (§6.2's table gives it "≠ 0" with no ceiling). That omission is right.
- T13's two instances are deflate and lz4 with no zstd entry — correct, since
  zstd can only reach outside its extent through a dictionary, which is either
  T19 (disclosed) or undetectable (§21.7).
- R4's 16 = 8 alternatives × 2 containers, and the 8 map one-for-one onto
  §18.2's carried-over frame constraints minus the two §18.2 says R4 registers
  neither of. Checked below in §4.

---

## 3. Building a file from the layout tables alone

The charter says to build the thing end to end and report where I had to guess.
I built a second, non-trivial file using **only** the layout tables and the
arithmetic sections, and then validated it back against the rules.

Layer `grid`: rank 2, interleaved, extents (3,3), tile extents (2,2), channels
`a` (uint8, fill 0x07) and `b` (bool, fill 0x01), codec 1, filter 1, no
alignment or slab. Two of four tiles stored, two sentinel.

Derived: G = (2,2), N = 4, P = 4, C = 2, Q = 1 + 1 = 2, decoded size P·Q = 8,
entry_count = N = 4, index region = 4·20 + ⌈4/2¹⁶⌉·4 = 84.

Decoded tile images, built from §14.1's interleaved value sequence, §14.2's
offsets and §14.5's fill-encoded padding:

```
tile 0  tc (0,0)  00 00 01 01 0a 01 0b 00      (no padding: all 4 positions real)
tile 1  tc (0,1)  02 00 07 01 0c 01 07 01      (x=3 padding -> a=0x07, b=0x01)
tile 2  tc (1,0)  14 00 15 01 07 01 07 01      (y=3 padding)
tile 3  tc (1,1)  16 00 07 01 07 01 07 01      (one real position, three padding)
```

Hand-check of tile 1: it spans x ∈ [2,4), y ∈ [0,2). E₁ = 3, so x = 2 is real and
x = 3 is padding. In-tile ordinals 0..3 are (y,x) = (0,2),(0,3),(1,2),(1,3).
Ordinal 0 → a = 2, b = 0 → `02 00`; ordinal 1 → padding → fill pair `07 01`;
ordinal 2 → a = 12 = 0x0C, b = 1 → `0c 01`; ordinal 3 → padding → `07 01`.
Matches.

Resulting file (320 bytes, F mod 64 = 0, dir_offset 116, dir_length 128,
index region at 32, inline_length 100, pre-trailer pad 12):

```
0000  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00
0010  00 00 01 01 0a 01 0b 00 16 00 07 01 07 01 07 01
0020  10 00 00 00 00 00 00 00 08 00 00 00 00 00 00 00
0030  07 0f 98 1e ff ff ff ff ff ff ff ff ff ff ff ff
0040  ff ff ff ff 00 00 00 00 ff ff ff ff ff ff ff ff
0050  ff ff ff ff ff ff ff ff 00 00 00 00 18 00 00 00
0060  00 00 00 00 08 00 00 00 00 00 00 00 ee 30 24 31
0070  3e 08 7e fc 01 00 03 00 64 00 00 00 20 00 00 00
0080  00 00 00 00 54 00 00 00 00 00 00 00 04 67 72 69
0090  64 01 01 00 01 00 01 00 00 00 00 00 00 00 00 00
00a0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00b0  02 02 00 01 79 03 00 00 00 00 00 00 00 02 00 00
00c0  00 00 00 00 00 01 78 03 00 00 00 00 00 00 00 02
00d0  00 00 00 00 00 00 00 01 61 06 00 01 07 01 62 01
00e0  00 01 01 01 04 00 00 00 00 00 00 00 88 47 d9 89
00f0  fc 74 3f a4 00 00 00 00 00 00 00 00 00 00 00 00
0100  8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
0110  01 00 00 00 00 00 00 00 74 00 00 00 00 00 00 00
0120  80 00 00 00 00 00 00 00 40 01 00 00 00 00 00 00
0130  ef cd ab 89 67 45 23 01 00 00 00 00 bb b8 3b a7
```

**Where I had to guess: nowhere.** §7.4's table gave the packed field order
unambiguously; §15.1 gave the entry layout and the "no padding anywhere inside
the region" adjacency of the entry array and the segment-CRC array; §15.2 gave
the sentinel's 20 bytes; §14.1/§14.2 gave the value sequence and every offset;
§14.5 gave every padding byte; §7.2 gave the record header; §6.2 gave the
trailer; `[R-LIF-02]` step 5 gave the 12-byte pad (directory ends at 244, next
64-boundary is 256). Every cross-check the document names — `[R-CNT-17]`'s
extent-length formula, `[R-CNT-23]`'s fill-length equality, the 64-alignment of
F, `dir_offset + dir_length ≤ F − 64` — passed by construction.

That is a strong positive result and it is worth recording as such: the
byte-layout boxes in this document are sufficient to write a conforming file
with no interpretation.

---

## 4. Passage-by-passage audit of the tables that restate rules

### 4.1 §8.1's coverage map against §4.5's prose

§4.5 makes three claims the map must deliver. All three hold:

1. *Terminal checksum fields, covered by no further checksum*: trailer CRC
   (covers [0,60), so is outside its own coverage), directory-region CRC
   (covers the preceding dir_length − 4), user-metadata terminal CRC. All three
   are map rows and none is covered elsewhere. OK.
2. *Interior checksum fields, comparison-verified **and** covered by exactly one
   further checksum*: each segment CRC array → crc_of_crc_array (named in the
   Tile-index row's Checksum-location cell); each entry's crc field → its
   segment CRC (Tile-index row's Covers cell, "index entries, per segment");
   each layer record's crc_of_crc_array → the directory CRC (it lives in the
   record sequence). All three covered exactly once. OK.
3. *The extent of a record of an unassigned type is covered by no checksum.*
   Its own row. OK.

I then checked the map is exhaustive over §5.2's coverage classes. Every byte of
a live state falls in: front block (equality), stored-tile extent (entry crc),
record extent (index region → segment CRCs + crc_of_crc_array; user-metadata →
terminal CRC; unassigned type → none), directory (directory CRC), trailer
(trailer CRC). Complete, no gap, no double coverage.

### 4.2 §10.2's identifier-space table against each defining section

Every row re-read against the section that owns the space:

- record type: §7.3 + `[R-CNT-15]` — assigned 0x0001/0x0002, reserved
  0x0003–0x7FFF, experimental ≥ 0x8000. OK.
- channel layout: `[R-SER-06]` — 1, 2 assigned; 3–255 reserved; no experimental,
  matching §10.2's own closing note. OK.
- linearization: `[R-GEO-05]` splits reserved into 2–3 and 4–0x7FFF; §10.2's
  union 2–0x7FFF is right. OK.
- sample type: `[R-TYP-03]` splits 14–19 and 20–0x7FFF; union 14–0x7FFF. OK.
- codec `[R-COD-03]`, filter `[R-COD-09]`, index encoding §7.4, metadata
  encoding `[R-MTA-03]` — all match. OK.
- "Value 0 is invalid in every space above" — each defining section says so. OK.
- Trailer flag lanes are explicitly excluded and pointed at §6.3. OK.

Appendix C's snapshot restates all eight spaces and the six standardized keys
consistently with §10.2, §12.1, §7.3, §17.2, §17.3, §14.1, §11.4, §15.1, §18.2
and §18.4. §12.2's pinned reservations (14/15 OFP8 E4M3/E5M2, 16 int128, 17
uint128, 18 float128, 19 raw bytes) match Appendix C's line item for item.

### 4.3 §12.1's sample-type table

Thirteen rows, ids 1–13, no gap. Element sizes checked against the type
definitions: bool 1, int8 1, int16 2, int32 4, int64 8, uint8 1, uint16 2,
uint32 4, uint64 8, float16 2, bfloat16 2, float32 4, float64 8. All correct.
"exactly thirteen sample types" and "The twelve types other than bool" are
consistent (13 − 1 = 12).

### 4.4 §14.2's byte-layout table

`planar, numeric channel c` → size P·Bᶜ, offset k·Bᶜ; `interleaved` → size P·Q,
offset (k div C)·Q + F_{k mod C}. Derived independently from §14.1's value
sequence: for planar, value k is channel c at in-tile ordinal k, so offset =
k·Bᶜ; for interleaved, value k is channel (k mod C) at ordinal k div C, so
offset = (k div C)·Q + F_{k mod C}. Both correct.

The table correctly omits planar bool, which §14.3 governs, and `[R-SER-07]`
closes the case split ("Whichever of §14.2 or §14.3 defines a tile's decoded
size"). The three decoded-size formulas — P·Q, P·Bᶜ, ⌈P/8⌉ — are exactly the
three that L44, T3, T14, T21, T22 and §21.9's tile row all range over, and each
of those cells enumerates all three. Consistent.

### 4.5 §15.3's entry-validity table

Eleven rows. Prose says "Six rows are marked *structural*" — counted: rows 2–7
are marked structural, six exactly. Rows 1 (valid sentinel) and 8 (crc failure,
"the entry itself is well-formed") are not, matching the prose's careful
distinction. Rows 9–11 are verifier rows.

Cross-mapped to §21.4/§21.3/§21.2: row 2→T6, row 3→T7, row 4→T10, row 5→T8,
row 6→T11, row 7→T12 + T9, row 8→T1, row 9→L18, row 10→F33, row 11→L40/L41/L42.
No row of the table is unregistered and no register row is orphaned.

### 4.6 §21.6's non-violation table and its closing prose

Fourteen rows, each re-checked against the rule cited. Two I looked at hard:

- The experimental-range record type row correctly qualifies "a *reserved*-range
  type is read the same way, but emitting one is a violation (F36, L25)" — this
  matches `[R-CNT-15]`'s distinction between experimental (conduct, `[R-CNF-02]`)
  and reserved (bytes, a violation) exactly.
- The closing prose's "Two structural cases are **conforming files a reader
  nevertheless refuses**" correctly narrows the second case to a **top-level**
  MU = 1 experimental type, and expressly says the sub-record case is
  reject-layer under `[R-CNT-18]`. That qualifier is present and load-bearing.

I checked whether `[R-CNF-03]`'s acceptance carve-out ("carrying no record of a
type it does not implement with MUST_UNDERSTAND = 1") is stated wider than
§21.6, since it carries no *top-level* qualifier and so appears to excuse a
reader from accepting a conforming file whose only such record is a layer
sub-record. It does read wider — but `[R-CNT-18]` independently says "where the
file is otherwise conforming a reader MUST NOT reject the file for it", and
`[R-CNF-12]`'s licence to reject reaches nonconforming files only. So the
behaviour is fully determined and there is no fork. **Not reported.**

### 4.7 §20.4's updater table

Three rows, MU = 1 / MU = 0 PE = 1 / MU = 0 PE = 0. §2.4's preserve-verbatim row
points at "its MU = 1 and MU = 0 / PE = 1 rows" — correct, those are the two
retain-byte-identical rows. The table's governing scope (types the updater does
**not** implement) is set by the paragraph above it, and the two preceding
paragraphs route registered types to §7.3's registry and other implemented types
to their own definitions, so "Persistence governs every record type" is
delivered. The MU = 0 / PE = 0 cell's list of qualifying independent changes is
internally consistent, including the non-obvious closure that superseding a tile
re-places the index region and so modifies the layer record.

### 4.8 §21.9's limits table and its per-instance paragraph — flagged passage

Eight rows. The paragraph partitions them as "the last three" (tile decoded
size, metadata document decoded size, zstd Window_Size) and "the first five"
(rank, C, entry_count, layers per file, dir_length). 3 + 5 = 8: the partition is
exhaustive and non-overlapping, which is the first thing to check and it holds.

The individuation claims:

- *Decoded size of one tile* "ranges over a layer's **addressed** tiles, stored
  or not, exactly as `[R-COD-07]`'s cap is". Checked against §17.2's note on
  `[R-COD-07]`, which says the same thing in the same words, and against
  `[R-SER-07]` ("decoded size is a function of the layer's declarations alone").
  Consistent. The corollary "A layer addressing no tile therefore has no tile
  whose decoded size the table bounds" follows and matches §17.2's note.
- "The other two range over the user-metadata documents and compressed frames a
  file actually contains." Compressed frames occur in two places — codec-3 tile
  payloads and encoding-2 metadata extents — and "a file actually contains"
  reaches both. Consistent with `[R-COD-06]`'s SHOULD and §18.2's SHOULD, which
  both point at the same 8 MiB row.
- "The first five rows range over declarations, which every file and every layer
  carries." A zero-layer file carries no rank/C/entry_count instance and
  trivially satisfies those rows; the "every file **and** every layer" phrasing
  handles that. OK.

`[R-ERR-04]`'s "at the narrowest scope whose **declarations** exceed what it can
serve, a layer or a tile" would leave a user-metadata document with no narrower
scope, since a document has no declared size — and §18.2's Note says exactly
that, routing such a refusal to the whole file. The gap is anticipated and
closed. Appendix B's "Reader minimum guarantees" row restates all eight values
correctly.

`[R-ERR-05]`'s hard-limits list checked item by item against §4.6, §7.4, §16.1,
§16.2, §17.2, §6.2, §5.1 — all nine correct, and Appendix B carries each.

### 4.9 §18.2's compressed-document passage — flagged passage, read whole

I read this as one passage rather than a sequence, as the brief asks, and tried
to break it on the "one quantity named where two are in play" shape.

The structure it sets up: §18.2 adopts *every* frame constraint `[R-COD-06]`
places on a frame, "named here or not, **save two**" — (a) what `[R-COD-06]`
states against a tile's declared decoded size, and (b) what it states about the
frame's declared `Window_Size` — and replaces both.

I enumerated `[R-COD-06]`'s constraints exhaustively and matched them:

| `[R-COD-06]` constraint | §18.2 disposition | R4 |
|---|---|---|
| exactly one RFC 8878 frame | carried (plus "occupying the extent's bytes before its terminal CRC") | second frame; bytes remaining |
| frame magic 0xFD2FB528 | carried | missing frame magic |
| no skippable frame anywhere | carried | a skippable frame |
| no dictionary use, disclosed or not | carried | *not registered* — no witness, §18.2 says so |
| no nonzero Dictionary_ID | carried | a nonzero dictionary ID |
| no content-checksum flag | carried | the content-checksum flag set |
| window ≤ tile decoded size | **exception (b)** — replaced by the reader's own bound | — |
| content size == tile decoded size | **exception (a)** — replaced by the decoded document's byte length | two magnitude directions |
| no buffer sized from a frame-declared length | carried | *not registered* — binds a reader, §18.2 says so |
| SHOULD keep window ≤ 8 MiB | replaced by §18.2's own SHOULD | — |

Nothing in `[R-COD-06]` is unaccounted for, and R4's sixteen instances are
exactly (8 alternatives × 2 containers) with the two witnessless ones correctly
absent — which is what §18.2's own sentence "Two of those carry no witness a
file exhibits, and R4 registers neither" predicts. The two lists agree
mechanically.

The Single_Segment_Flag argument also holds: RFC 8878 makes Window_Size the
content-size field when SSF is set, §18.2 pins that field to the decoded
document's length, so an SSF-framed document above 8 MiB exceeds the
`Window_Size` row while staying inside the 16 MiB document row — which is
precisely what the passage says, and why it tells a writer to use a
Window_Descriptor instead. §21.9's two rows are independent here and the passage
says so ("§21.9's user-metadata row bounds a document's decoded size; it does not
relieve the frame carrying it of the `Window_Size` row").

One wording point I chased and dropped. The verifier sentence says "A
**verifier** that declines to decode a document on **the bound above**", singular,
while §21.5's preamble says a reader or verifier may decline "on the size bound
**or on the frame's declared window**". The window paragraph is written in
reader terms only ("a reader's window bound is its own"). So "the bound above"
is readable as the size bound alone, leaving a verifier's *window* decline
unaddressed by §18.2 — except that the window paragraph says the window "takes
the same treatment", §2.3 makes a verifier a reader and so binds its window
bound to the same ≥ 8 MiB floor, and `[R-CNF-11]` independently lists "when it
declines to decode a user-metadata document (`[R-MTA-09]`)" among the
cannot-establish grounds without restricting which bound caused the decline.
Both readings therefore produce the same verdict, the same report and the same
certification outcome. No fork; **not reported.**

### 4.10 §21.7 — flagged passage

Paragraph 1 (wrong content is undetectable, narrowed only where §14.5 and
`[R-SER-08]` structurally constrain content) is sound, and its closing claim
that none of these is a `[R-CNF-11]` *unable to check* ground is right: those
grounds are capability and resource, and a missing witness is neither.

Paragraph 2 enumerates, by class, the obligations omitted from the register for
want of a witness. I walked each:

- `[R-LIF-01]`, `[R-LIF-03]` — history, §9.7 does not reconstruct it. OK.
- `[R-GEO-06]`, `[R-SER-01]` ordinal mappings — witnessed only at T2/T4/T5. OK.
- `[R-CNT-13]`'s no-embedded-offsets rule — opaque. OK.
- `[R-CNT-18]`'s nesting bar — checked against §7.4's closing Note; the only
  detectable sub-case (a layer record as a sub-record) is L26. OK.
- `[R-WRT-06]`'s two compacted-trailer obligations — output carries no record of
  its input. OK.
- `[R-ENC-06]`'s field widths — "not a state a file can be in". OK.
- §20.3 step 4's bar on a declaration change — **this is where the account is
  short**, see finding diagrams-01 below.

### 4.11 Appendix H's five checklists

Each entry traced to the rule it cites.

- *Conforming reader*: "all four codecs, both filters, both layouts, all thirteen
  sample types, and both user-metadata encodings" — matches `[R-CNF-03]`'s
  reference to §17's core set (4 codecs, 2 filters), §14's two layouts, §12.1's
  thirteen, §18.2's two assigned encodings. Correct counts.
- *Conforming verifier*: I checked this one for completeness against the
  register, since it is the checklist most likely to drift. Every
  verifier-detected row is covered: F7 (named), F25/F26/L46/L47 (record flag
  bits), F27/L48 (member ordering), F28/L49 (registry flags), F33/L18 (extent
  overlap), F36/L25 (reserved-range types), L40/L41/L42 (alignment and slab),
  T2/T4/T5/T26 (decoded-content obligations), F1/F6 (front block, with the
  correct note that `[R-CNT-04]` exempts a non-resident reader and §2.3 does not
  exempt a verifier). No verifier row is missing.
- *Conforming writer* and *updater*: both are summaries and both are headed by
  "A summary of each class's obligations … each entry's authority is the
  requirement or section cited, never this summary", so their omissions
  (`[R-ENC-02]`, `[R-ENC-11]`, `[R-CNT-08]`'s flags = 0, `[R-WRT-03]`'s
  index-chain depth for reused segments) are licensed by the header. Not
  reported.

### 4.12 Appendix G's numbered profile

Item 2's `file_id` derivation is well-founded and non-circular: the hash input is
[0, F − 64) plus the trailer's first 60 bytes with `file_id` zeroed, which
excludes the trailer CRC at [60,64) — the one field that depends on `file_id`.
Had the CRC been in the input the definition would be circular; it is not.

Item 3's ordering key is likewise non-circular: the key masks `extent_offset` to
zero and reads only type, flags, lengths, inline payload and extent content — all
known before placement — and the appendix says why in one sentence. The claim
that two records the key does not separate produce the same file either way is
correct: their headers differ only in `extent_offset`, and swapping which extent
each takes leaves the byte sequence identical.

Item 3's "The first structure begins at 16 … which §5.2 counts as no structure"
is right — `[R-CNT-02]` lists the front block as a class *beside* "a structure" —
and its alignment escape ("or, where a declared alignment admits no structure at
16, at the least position above it the declaration admits") is needed, since
A ≥ 512 makes 16 unusable for the first stored tile.

The closing paragraph pre-empts an item/freedom count mismatch explicitly: "Read
the numbered items as the list; this paragraph names what they are for, not how
many there are." Item 5's fixed filter value and item 8's `flags` = 0 are absent
from that paragraph's list, which the disclaimer licenses.

---

## 5. Findings

### diagrams-01 — CONTRADICTION

**§21.7 `[R-ERR-01]`; §20.3 step 4 `[R-WRT-04]`; §21.1 `[R-ERR-02]`**

§20.3 step 4's bar names four things a commit may not alter for a tile stored in
the superseded generation:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes."

§21.7 undertakes to account for that bar's undetectable residue. Its account
covers the first item, the second, and **half** of the fourth:

> "§20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size instead is witnessed
> by T3 or T14, which test a length rather than the decoded image's content —
> T14 the entry's declared length, T3 the decoded payload's own; a change that
> reaches the codec is witnessed by the rows for the codec now declared, which
> test the stored bytes as a stream of it (T15, T17, T23, T25), or by T14 where
> the new declaration is codec 1"

The **filter** is missing, and the third bar item — "the byte offset of any
sample within the decoded tile image" — is missing too.

This is the analogy shape exactly. §20.3 names "the codec **and filter**" in one
breath, and §21.7 carries only the codec across. The witness argument it gives
for the codec is codec-specific and does not transfer: there are no "rows for
the filter now declared" that test stored bytes, because both filter values are
length-preserving and neither can fail. Filter 1 is the identity; filter 2 is a
permutation defined for every input whose length is divisible by the mandated
stride, which §17.3 proves is always the case. A filter change therefore has no
decode-time witness of any kind.

Worked witness. Layer: interleaved, two `uint16` channels, extents exactly
divisible by tile extents so there is no padding position, no bool channel so no
pad bit and no `[R-SER-08]` byte, codec 1, filter 1, one stored tile. Generation
n+1 changes the filter field from 1 to 2 and nothing else. Then Q = 4, so
`[R-COD-10]`'s mandated stride is 4 and the filter is **not** the identity — so
§20.3's own escape clause ("a filter whose mandated stride makes it the
identity") does not apply and the commit is barred. But: the decoded size is
unchanged, so T3 does not fire; the entry length still equals the decoded size,
so T14 does not fire; there is no padding position, so T4 does not fire; no pad
bit, so T5 does not fire; no interleaved bool byte, so T2 does not fire; and T26
requires "the resulting image breaks §14.5's padding content or `[R-SER-08]`'s
bool bytes", which nothing here does. The stored tile now decodes to a
byte-permutation of its true values and **no row of §21 fires**. The same
construction works for the third bar item: swapping two equal-width channels
changes every Fᶜ and therefore the byte offset of every sample, without changing
the decoded size or any structurally constrained byte.

§21.1 makes §21.7 load-bearing rather than decorative:

> "Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, by class, of what fails it"

So §21.7 is the document's own account of what fails detectability, and it is
short by one and a half of §20.3's four classes.

Two smaller points ride on the same sentence. First, its opening "witnessed
**only where** … the change reaches a byte §14 structurally constrains" is
contradicted by its own two following clauses, which name two further witnessed
classes; the "only" has to be read as scoping the first class alone. Second,
paragraph 1's general classes ("a mis-strided filter", "or simply wrong data")
do absorb the residue by class — but a mis-strided filter is a *writer* applying
the wrong stride at write time, a different violation from a *commit changing
the declaration under bytes already written*, and paragraph 2 is the paragraph
that enumerates §20.3's classes. The permitted reading in which paragraph 1's
"simply wrong data" silently swallows the filter case is available, but it makes
paragraph 2's careful three-way enumeration pointless.

**Byte-level: no.** A writer that follows §20.3's bar emits the same bytes
whether or not §21.7 lists the filter, and no reader or verifier changes a
verdict, precisely because the condition has no witness either way. §21.7 is
descriptive, not permissive, and §21.1 says the rule governs where a restatement
diverges. The cost is to a reader of the document, not to a file: an implementer
who trusts §21.7's enumeration will conclude that a filter-only re-declaration
is either witnessed or permitted, and it is neither.

### diagrams-02 — CONTRADICTION

**§24 `[R-VEC-04]`; §21.5; `[R-CNF-12]`**

`[R-VEC-04]` requires an intact sibling of two of the four outcome classes:

> "Every vector whose recorded outcome is reject-layer or reject-tile is built
> inside a file that also carries an **intact sibling** — another layer, or
> another tile of the same layer where that layer is one a reader is still
> permitted to serve — whose decoded content the manifest records, and a
> vector's expectation is therefore a pair."

Its own stated rationale, two sentences later, reaches every register row:

> "Without the sibling a vector cannot distinguish a reader that scopes its
> refusal from one that rejects the file entire, because `[R-CNF-12]` permits
> the latter for any nonconforming file and every vector built from §21's
> register is nonconforming."

"every vector built from §21's register" includes §21.5's ten ignore-record rows,
which §21.5 is explicit are violations and therefore nonconforming files:

> "Every row here is a violation all the same: the outcome bounds a reader's
> blast radius and never makes the file conforming (`[R-CNF-12]`)"

So the premise covers R1–R10 while the requirement's scope stops at reject-layer
and reject-tile. The gap is reachable, not hypothetical: R1 fires on a
**top-level** user-metadata record declaring encoding 0, and a file carrying one
such record and **zero layers** is a legal vector under `[R-VEC-04]` as written
(zero layers being conforming, §21.6). Against that file a reader that ignores
the record and a reader that rejects the whole file are observationally
identical — both return no samples — which is the exact failure `[R-VEC-04]`
exists to prevent. The reject-tile analogue is forbidden and the ignore-record
one is not, though the argument is word for word the same.

The permitted readings are (i) `[R-VEC-04]`'s enumeration is the operative scope
and R-row vectors need no sibling, and (ii) the rationale states the real scope
and the enumeration is an incomplete restatement of it. I pick (i), because the
requirement sentence is the normative one and the rationale sentence is
explanatory — which is what makes this a defect rather than an ambiguity a
corpus builder can reason past.

**Byte-level: no.** Vectors are derivative (`[R-VEC-01]`: "where a vector's
recorded expectation and this specification disagree, this specification
governs"), so widening `[R-VEC-04]` changes which files the corpus contains and
not which files an implementation may emit or must accept. The cost is that the
corpus can be built such that ten register rows are exercised by vectors no
implementation can fail for the right reason.

### diagrams-03 — OBSERVATION

**§4.7's presentation Note; §7.2's record-header table**

§4.7's Note tells a reader how to read each layout table, and makes a specific
promise about §7.2:

> "§6.1's block is a 16-byte constant, where a Value column replaces type and
> range, and §7.2 folds each field's range into its Field cell."

§7.2's table has five fields and folds a range into two of them:

> "| 0 | 2 | u16 | type (0 invalid) | structural |
> | 2 | 2 | u16 | flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved | structural |
> | 4 | 4 | u32 | inline_length | structural |
> | 8 | 8 | u64 | extent_offset | structural |
> | 16 | 8 | u64 | extent_length | structural |"

`inline_length`, `extent_offset` and `extent_length` carry no range in their
Field cells. Their ranges are stated normatively — `[R-CNT-12]`'s prose for
`inline_length` ("A record whose header or inline payload would extend past the
end of its containing record sequence…"), `[R-CNT-13]`'s paragraph for the
extent slot, `[R-ENC-03]` for the u64 domain — but not where §4.7 says to look
for them. The general hedge in the same Note, "each table giving the columns its
structure needs", does not reach this, because the §7.2 clause is a specific
claim about a specific table and the word is "each field".

I checked the parallel claims and they hold: §6.1's table does replace type and
range with a Value column, §7.4's table does omit the offset and class columns,
and §6.2's, §15.1's and §18.2's tables do deliver all six columns.

**Byte-level: no.** Every range the Field cells omit is stated normatively
within two paragraphs of the table, so no reading of the record header is left
open. This is a finding about a non-normative Note (labelled *Note*, and so
non-normative under `[R-CNF-01]`) misdescribing a normative table, which is the
"stale restatement" class my charter names, at its cheapest end. I report it
because "check the promise against what is actually delivered" is an explicit
charter instruction and this is the one promise in the document's presentation
apparatus that is not delivered.

---

## 6. What I checked and did not find fault with

Recorded so the coverage is legible, and because an empty result on a passage is
information.

- **Every numeric value in every worked example.** Twenty-two examples, all
  arithmetic re-derived. Zero errors. The CRC constants (`0x80A34955`,
  `0xC4EE982E`, `0xEECB3BB2`, `0xE00938D2`, the check vector) all reproduce.
- **Appendix A byte by byte**, including the trailer CRC over [0,60) and the
  empty-directory CRC, against the annotation table's fourteen rows. Exact.
- **§21.8's 121/277.** Both exact, mechanically, under §21.1's own counting rule.
  Row ids contiguous in all four register sections.
- **§21.9's table/paragraph partition.** 3 + 5 = 8, exhaustive, non-overlapping,
  and each individuation claim traced to the rule it invokes.
- **§18.2's frame-constraint inheritance** against `[R-COD-06]`, constraint by
  constraint, and against R4's sixteen instances. Complete on both sides.
- **§8.1's coverage map** against §4.5's three claims and §5.2's coverage
  classes. Complete, exactly-once, no orphan.
- **§10.2, §12.1, §7.3, §18.4 and Appendix C** against their defining sections.
  No divergence.
- **§15.3's eleven rows** against `[R-IDX-03]`'s prose ("Six rows are marked
  *structural*" — six exactly) and against every §21 row that registers them.
- **Appendix B's twenty-four constants** against their defining sections.
- **Appendix H's verifier checklist** against the full set of verifier-detected
  register rows. No row missing.
- **Appendix G items 2 and 3** for circularity in the `file_id` derivation and
  the record-ordering key. Neither is circular; both say why.
- **Every numbered list** in the document for order, duplication and omission.
  All contiguous.
- **All eight ASCII region diagrams** against the commit protocol. §5.1's
  three-commit figure in particular reconstructs exactly from `[R-LIF-02]`:
  front, A, [dir₁ pad trail₁], B, [dir₂ pad trail₂], dir₃, pad, trail₃, with the
  two ▓ runs falling precisely where the two superseded commits left them. The
  figure also disclaims its own grouping ("The grouping under the box is
  illustrative: a layer's structures need not be contiguous or ordered"), which
  is the right guard against a reader taking it further than `[R-SLB-05]` allows.
- **§20.3's shape (c)** against step 4's bar: "changing a channel's fill value on
  a layer with no padding position and no pad bit" is correct, since fill governs
  only unstored tiles and padding content, and both qualifiers are layer-level
  properties. The figure's companion sentence correctly excludes the case where
  the layer stores a tile carrying either.
- **§19.4's planar note**: entries spaced N·20 bytes apart fall in different
  2¹⁶-entry segments whenever N ≥ 2¹⁶ — true, since two ordinals differing by at
  least 2¹⁶ cannot share a bucket of size 2¹⁶.
- **§17.3's divisibility claim** across all three tile kinds: P·Bᶜ / Bᶜ,
  P·Q / Q, ⌈P/8⌉ / 1. All integral. The case split is exhaustive.
- **`[R-IDX-05]`'s full-versus-partial segment rule** against §7.4's example,
  which correctly computes rather than substitutes because its segment is partial.
- **The §17.2 Single_Segment_Flag note** against RFC 8878's two Window_Size
  derivations and against §14.2/§14.3's sub-1-KiB worked sizes (18, 30, 2).

## 7. Candidates I raised and dropped

- §18.2's "the bound above" (singular) versus §21.5's "the size bound or on the
  frame's declared window". Both readings give the same verdict, report and
  certification outcome, via §2.3 (a verifier is a reader) and `[R-CNF-11]`'s
  unrestricted user-metadata decline ground. Dropped.
- `[R-CNF-03]`'s MU = 1 carve-out reading wider than §21.6's top-level qualifier.
  `[R-CNT-18]` forbids the file-scope rejection outright and `[R-CNF-12]` reaches
  nonconforming files only, so the behaviour is determined. Dropped.
- §2.4's preserve-verbatim row pointing only at §20.4's stored-flags table. The
  table's rows are flag combinations and §20.4's three preceding paragraphs route
  every type to a flag source, so the pointer is not narrowing. Dropped.
- §21.6's "The file contains zero layers → A conforming file with an empty
  directory": a zero-layer file may still carry a top-level user-metadata record,
  so the cell's gloss is narrower than its condition. The cell's operative
  content is the verdict *conforming*, which is right in both cases. Dropped as
  too slight.
- §5.1's figure captioning the pre-trailer pad inside a "re-emitted" bracket. The
  pad is fresh slack, not a re-emission. Cosmetic. Dropped.
- Appendix G item 7's "not merely about eight bytes of the layer record" — the
  fill field is 1–8 bytes by element size. Illustrative prose in a non-normative
  appendix. Dropped.
- §21.7's claim that a codec re-declaration is "witnessed by the rows for the
  codec now declared" is probabilistic rather than certain — a raw image could in
  principle also be a valid frame of the new codec decoding to the right size.
  Measure-zero and already absorbed by paragraph 1. Dropped.
