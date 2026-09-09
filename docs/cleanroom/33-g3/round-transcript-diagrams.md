# Round 33 — Diagram auditor — working transcript

## 0. Access disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,805 lines, as the brief states). I read it end to end in eight `sed -n` slices, then
re-read individual passages as questions arose. I opened no `docs/`, no `conformance/`,
no `PLAN.md`, no `AGENTS.md`, no `registry.json`, no git history. I ran no web tool.

I wrote three files, all inside my own scratch directory
`/private/tmp/.../r33-round/scratch/diagrams/`:

- `crc32c_diag.py` — a from-scratch CRC-32C (reflected poly 0x82F63B78, init/final
  0xFFFFFFFF), used to check §4.5's check vector, §15.4's all-sentinel constant, and
  the two CRCs in §7.4's worked example.
- `appA_diag.py` — parses Appendix A's hex dump back into 128 bytes, cuts each trailer
  field at the offset and width §6.2's layout table gives, decodes it, and recomputes
  the trailer CRC over bytes [0, 60).
- (no third file; the register arithmetic ran as heredoc `python3 -` with no file
  written)

Everything else was `grep`/`python3` heredocs reading only `spec/tarn.md`.

**Context I did not ask for.** My runtime placed a project instruction file
(`CLAUDE.md`, which redirects to `AGENTS.md`) and an index of the maintainer's memory
notes in my context before I began. The memory index named several TARN-process topics
by title. I did not open any of them, and I did not use any of it — none of it bears on
figures, arithmetic or checksums, which is my charter. I disclose that it appeared.

**Paths.** Everything was where the brief said it was. `spec/tarn.md` exists at the
stated path; my scratch directory did not exist and I created it; the output directory
I created with `mkdir -p` and did not list or read.

**Hard-wrap discipline.** I did every phrase search over a whitespace-normalised copy of
the document built in memory (`re.sub(r'\n>? ?', ' ', raw)` then collapse runs of
whitespace), so that a phrase crossing a hard wrap or a `> ` blockquote continuation is
still found. I ran positive controls before resting on any zero: searching
`"several of these in one commit"` and
`"A commit MAY make several of these changes at once"` — phrases I had already read and
which each span a wrap — each returned exactly 1 on the normalised text. Only then did I
credit the zeros (`"size column"` → 0, `"the size column"` → 0).

---

## 1. Inventory: every figure, dump, layout table and checklist, with line numbers

I enumerated before judging. Three mechanical sweeps.

**(a) Every markdown table** (`awk` over lines beginning `|`), 25 tables:

| lines | table |
|---|---|
| 127–147 | §2.2 requirement prefixes |
| 302–308 | §2.4 outcome classes |
| 779–782 | §6.1 front signature block — *layout table* |
| 822–833 | §6.2 trailer — *layout table* |
| 997–1003 | §7.2 record header — *layout table* |
| 1073–1076 | §7.3 record types of format major 1 |
| 1102–1119 | §7.4 layer record inline payload — *layout table* |
| 1220–1228 | §8.1 coverage map |
| 1563–1572 | §10.2 numeric identifier spaces |
| 1777–1791 | §12.1 core sample types |
| 2011–2014 | §14.2 decoded size / offset of value k |
| 2184–2188 | §15.1 tile-index entry — *layout table* |
| 2232–2244 | §15.3 entry-state classification |
| 2631–2633 | §18.2 user-metadata inline payload — *layout table* |
| 2830–2837 | §18.4 standardized keys |
| 3414–3418 | §20.4 updater obligation by governing flags |
| 3700–3736 | §21.2 file-scope register (35 rows) |
| 3749–3799 | §21.3 layer-scope register (49 rows) |
| 3809–3836 | §21.4 tile-scope register (26 rows) |
| 3859–3870 | §21.5 ignored-records register (10 rows) |
| 3879–3895 | §21.6 conditions that are not violations |
| 4008–4017 | §21.9 minimum guarantees |
| 4395–4410 | Appendix A byte annotation |
| 4430–4458 | Appendix B constants |
| 4528–4530 | Appendix E changelog |

**(b) Every fenced block** (`grep -n '```'`), 8 of them:

- 660–665 §5.1 "a file after three commits" box figure
- 1168–1187 §7.4 annotated 81-byte layer-record payload dump
- 1322–1331 §9.2 "what a crash sees" figure
- 3336–3340 §20.3 shape (a) — a new layer
- 3352–3356 §20.3 shape (b) — tiles added
- 3379–3382 §20.3 shape (c) — directory-confined change
- 3553–3559 §20.5 "what compaction reclaims"
- 4384–4393 Appendix A 128-byte hex dump

**(c) Every box-drawing/hatch run** (`grep` for `│┌└┐┘├┤┬┴─▓↑`) — line runs 658–674,
1318–1330, 3332–3381, 3550–3557. No figure outside (b) exists; the extra hits are prose
that mentions `▓`.

**(d) Every labelled block** (`> **Note` / `> **Example` / `> **Rationale`) — 103 hits,
listed by line. Of these the *Examples* carrying arithmetic are at lines 586, 650, 657,
1157, 1318, 1692, 1748, 1811, 1860, 1930, 2056, 2090, 2148, 2272, 2287, 2389, 2574,
3322, 3331, 3550.

**(e) Unlabelled blockquotes.** I ran a scan for blockquote blocks whose first line does
not begin `**Note`/`**Example`/`**Rationale`. Exactly one exists:

- line 2179, §15.1: `> [ entry array: entry_count × 20 bytes ] [ segment CRC array: > ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`

Under `[R-CNF-01]` this block is **normative** — the exemption is by label, and it
carries none. I checked it against `[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`
and they agree exactly. No finding.

**(f) Appendix normativity.** `grep '^### Appendix'` gives eight headings. A, B, C, D, E,
G, H are marked `(non-normative)`. **Appendix F — Normative references is not**, so it is
normative text under `[R-CNF-01]`. I carried that fact into my grading of finding
diagrams-03.

---

## 2. Checksums recomputed rather than read

This is the standing charge, so I did it first and did it from scratch.

I wrote CRC-32C myself (bitwise, reflected polynomial 0x82F63B78 = reflect(0x1EDC6F41),
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and validated my implementation on §4.5's own
check vector before trusting it on anything else:

| what | document says | I computed | verdict |
|---|---|---|---|
| CRC-32C("123456789") | `0xE3069283` (§4.5, App. B) | `0xE3069283` | ✅ |
| CRC-32C(zero bytes) | `0x00000000` (§4.5, §5.1, App. A) | `0x00000000` | ✅ |
| CRC of one full all-sentinel segment (2¹⁶ × `FF ×16 00 ×4`) | `0xEECB3BB2` (`[R-IDX-05]`, L38, App. B) | `0xEECB3BB2` | ✅ |
| §7.4 example: CRC over the 80-byte 4-sentinel entry array | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, LE `55 49 a3 80` | ✅ |
| §7.4 example: crc_of_crc_array over those 4 bytes | `0xC4EE982E`, dump shows `2E 98 EE C4` | `0xC4EE982E`, LE `2e 98 ee c4` | ✅ |
| Appendix A: trailer CRC over trailer bytes [0, 60) | `0x402F157E`, dump `7E 15 2F 40` | `0x402F157E`, LE `7e 15 2f 40` | ✅ |

Every printed checksum in this document is correct. That is four independent CRCs plus
two check-vector values, all reproduced.

---

## 3. Appendix A, byte by byte against §6.2's layout table

I parsed the dump programmatically (asserting each line's stated offset equals the number
of bytes accumulated so far, so a dropped or duplicated byte would have thrown), got 128
bytes, cut the trailer at [64, 128), and decoded each field at the offset and width the
§6.2 table gives — not at the offsets the annotation table gives, so that the two could
disagree.

| §6.2 field | offset/size | bytes cut | decoded | Appendix A annotation | verdict |
|---|---|---|---|---|---|
| trailer magic | 0 / 8 | `8A 4E 52 41 54 0D 0A 1A` | — | "[64, 72) trailer magic" | ✅ |
| version_major | 8 / 2 | `01 00` | 1 | "[72, 74) version_major = 1" | ✅ |
| version_minor | 10 / 2 | `00 00` | 0 | "[74, 76) version_minor = 0" | ✅ |
| flags | 12 / 4 | `00 00 00 00` | 0 | "[76, 80) flags" | ✅ |
| dir_offset | 16 / 8 | `10 00 …` | 16 | "[80, 88) dir_offset = 16" | ✅ |
| dir_length | 24 / 8 | `04 00 …` | 4 | "[88, 96) dir_length = 4" | ✅ |
| committed_file_length | 32 / 8 | `80 00 …` | 128 | "[96, 104) = 128 = the file size" | ✅ |
| file_id | 40 / 8 | `EF CD AB 89 67 45 23 01` | 0x0123456789ABCDEF | "[104, 112) file_id = 0x0123456789ABCDEF, little-endian" | ✅ |
| reserved | 48 / 12 | twelve `00` | zero | "[112, 124) trailer reserved, 12 bytes, zero" | ✅ |
| trailer CRC | 60 / 4 | `7E 15 2F 40` | 0x402F157E | "[124, 128) = 0x402F157E, over trailer bytes [0, 60)" | ✅ |

Structural cross-checks the same dump has to satisfy:

- physical length 128 = committed_file_length ✅ (`[R-CNT-06]`, F17)
- 128 mod 64 = 0 ✅ (`[R-CNT-06]`, F13)
- dir_offset 16 ≥ 16 ✅ (F9); dir_length 4 ≥ 4 ✅ (F16)
- dir_offset + dir_length = 20 ≤ F − 64 = 64 ✅ (F10)
- file_id ≠ 0 ✅ (F12)
- front block [0, 8) = `89 54 41 52 4E 0D 0A 1A`, [8, 16) zero ✅ (§6.1, F6)
- directory region [16, 20) = `00 00 00 00` = CRC of zero bytes ✅ (§7.1, F20)
- 128 ≥ `[R-CNT-27]`'s floor; and 128 is the least F with F mod 64 = 0 and
  F ≥ 16 + 4 + 64 = 84 ✅ — so §5.1's "The smallest conforming file is exactly 128 bytes"
  and its region breakdown (front [0,16); directory [16,20); 44 bytes of pad; trailer
  [64,128)) is right: 64 − 20 = 44 ✅
- Appendix A's closing note: "112 bytes covering [16, 128) contains the directory" —
  128 − 16 = 112 ✅

Appendix A is byte-perfect. No finding.

---

## 4. §7.4's annotated layer-record payload, field by field

I laid the §7.4 constraint table's field order against the dump's stated offsets and
re-derived every one.

```
field                  width                     running offset
name (u8 len + "sst")  1 + 3 = 4                 0
layout u8              1                         4
linearization u16      2                         5
codec u16              2                         7
filter u16             2                         9
alignment A u64        8                        11
slab S u64             8                        19
slab alignment u64     8                        27
rank d u8              1                        35
channel count C u16    2                        36
dim entry: 1+1 name, 8 extent, 8 tile extent = 18  38
chan entry: 1+4 name, 2 type, 1+4 fill    = 12     56
index_encoding u8      1                        68
entry_count u64        8                        69
crc_of_crc_array u32   4                        77  → ends 81
```

Every running offset matches the dump's left column exactly (0, 4, 5, 7, 9, 11, 19, 27,
35, 36, 38, 40, 48, 56, 63, 68, 69, 77). The dump splits the channel entry at 56/63,
which is the name+type (7 bytes) and the fill (5 bytes) — consistent.

The example's own summing sentence: "Name and the nine scalars from layout through
channel count occupy 4 + 34 bytes, the dimension entry 18, the channel entry 12, and the
trailing fixed fields 13 — 81 exactly."
- nine scalars = layout, linearization, codec, filter, A, S, A_slab, rank, C — I counted
  nine ✅ — widths 1+2+2+2+8+8+8+1+2 = **34** ✅
- 4 + 34 + 18 + 12 + 13 = **81** ✅ and 13 = 1 + 8 + 4 ✅

Values:
- `03 73 73 74` → length 3, `sst` ✅
- extent `64 00…` = 100 ✅, tile extent `20 00…` = 32 ✅
- ⌈100 / 32⌉ = 4 ✅ (the example's grid count and entry_count)
- `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — I compared this byte for byte against §12.3's
  "twelve bytes" for the same `temp` channel entry. Identical ✅. The example's claim
  "§12.3's `temp` entry, byte for byte" holds.
- fill `00 00 C0 7F` little-endian = 0x7FC00000 ✅ quiet NaN, length 4 = float32's
  element size ✅ (`[R-CNT-23]`, L30)
- `[R-CNT-17]` arithmetic: 4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 80 + 4 = **84** ✅, and §15.1's
  region layout gives 80-byte entry array + one 4-byte segment CRC = 84 ✅
- both CRCs recomputed above ✅

Also checked against the rules the example must not violate: entry_count = 4 ≠ 0 so a
nonzero crc_of_crc_array is required, not forbidden (L27) ✅; a nonzero extent slot with
entry_count > 0 is required, not forbidden (L22) ✅; A = S = A_slab = 0 is the legal
"none declared" combination (L28, `[R-CNT-16]`) ✅.

No finding.

---

## 5. Every other worked example, re-derived

**§4.6 `température`.** NFC: `74 65 6D 70 C3 A9 72 61 74 75 72 65` — I decoded each byte:
t e m p (C3 A9 = é) r a t u r e = 11 characters, **12 bytes**, prefix 12 ✅. NFD with
`65 CC 81` for é: 12 − 2 + 3 = **13** ✅. Appendix G item 10 restates "12 bytes in NFC and
13 in NFD" ✅ consistent.

**§11.2.** extents (1024, 2048), tiles (256, 256) → G = (4, 8) ✅, N = 32 ✅,
P = 256·256 = 65,536 ✅. With extent 1000: ⌈1000/256⌉ = 3.906… → 4 ✅.

**§11.4.** Grid (4, 8), s = t₀·G₁ + t₁. (0,0) → 0 ✅; (0,1) → 1 ✅; (1,0) → 8 ✅.
Coordinate (300, 700): t = (300 div 256, 700 div 256) = (1, 2), s = 1·8 + 2 = **10** ✅;
u = (44, 188), in-tile ordinal 44·256 + 188 = 11,264 + 188 = **11,452** ✅. Planar C = 4,
channel 2: c·N + s = 2·32 + 10 = **74** ✅.

**§12.1 bfloat16.** binary32 1.0 = 0x3F800000, high 16 = 0x3F80, stored LE `80 3F` ✅.
0x7FC0 → 0x7FC00000 quiet NaN ✅. Bit layout: binary32 is 1 sign + 8 exponent + 23
significand, so the top 16 bits are sign at 15, exponent at 14–7, significand at 6–0 ✅
exactly as §12.1 states.

**§14.2.** Interleaved, T = (2, 3), P = 6, channels a(uint8, 1), b(uint16, 2): Q = 3,
decoded size 6·3 = **18** ✅. Coordinates (1, 2) → ordinal 1·3 + 2 = **5** ✅; bytes
[5·3, 5·3+3) = **[15, 18)**, a at 15, b at 16–17 ✅. Planar b: P·B = 6·2 = **12** bytes,
ordinal 5 at 5·2 = **10–11** ✅. Interleaved t(float32) + m(bool): Q = 4 + 1 = **5**,
size 30 ✅, ordinal 5 at [25, 30), t 25–28, m at 29 ✅. Closing identity
"channel c's value at in-tile ordinal u sits at byte u·Q + Fᶜ — the table's forms with
k = u·C + c": k div C = u ✅ and k mod C = c ✅ since c < C. Correct.

**§14.3.** Planar bool, T = (2, 5), P = 10, values alternating true/false from ordinal 0
(so value k true iff k even). Byte 0 = bits 0..7 from values 0..7 = 1,0,1,0,1,0,1,0 →
0b01010101 = **0x55** ✅. Byte 1 = values 8 (true → bit 0) and 9 (false → bit 1) = **0x01**
✅, six pad bits at 2–7. Fill false → `55 01` ✅; fill true → 0x01 | 0xFC = **0xFD**,
`55 FD` ✅.

**§14.4 Note.** Single-channel numeric: planar offset k·B vs interleaved
(k div 1)·B + F₀ = k·B ✅ byte-identical. At P = 1: ⌈1/8⌉ = 1 = P ✅ same length; planar
byte = v | (fill ? 0xFE : 0x00), interleaved byte = v; equal exactly when fill is false ✅
as stated.

**§14.5.** extents (5,5), tiles (4,4) → grid ⌈5/4⌉² = 2 × 2 ✅. Edge tile (1,1) covers 4–7
on both axes ✅ = 16 positions, of which only (4,4) is inside the extents → **1 real, 15
padding** ✅. One uint16 channel: decoded size 16·2 = **32 bytes** ✅. Ordinal 0 is
(u=0,0) = coordinate (4,4) = the real sample ✅; values 1–15 each `CD AB` (LE of 0xABCD) ✅.
(This example is layout-agnostic: interleaved P·Q = 32 and planar P·B = 32 agree — and
§14.4's Note is what licenses that, so the example does not silently assume a layout.)

**§15.4 (first).** entry_count = 1,000,000 → ⌈10⁶/65,536⌉ = **16 segments** ✅; 15 full
covering 983,040, last covering 10⁶ − 983,040 = **16,960** ✅; CRC array 16·4 = **64
bytes** ✅; region 10⁶·20 + 64 = **20,000,064** ✅. k = 999,999 → segment
999,999 div 65,536 = **15** ✅, segment-relative index 999,999 − 983,040 = **16,959** ✅,
byte 20 × 16,959 = **339,180** ✅. CRC array at [20,000,000, 20,000,064) ✅. Segment 15 at
[983,040·20, 20,000,000) = **[19,660,800, 20,000,000)** ✅, i.e. 339,200 bytes ≈ "339 KB" ✅.
One full segment = 65,536 · 20 = 1,310,720 = **1.25 MiB** ✅.

**§15.4 (second).** Planar C = 4, N = 32; channel 2 at s = 10 → disk ordinal **74** ✅;
entry at [20·74, 20·75) = **[1,480, 1,500)** ✅. Channel 3's ordinals 3·32 + s for
s = 0…31 = **96–127**, 32 entries ✅.

**§16.2.** N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32) ✅ four. Under row-major
with G = (4, 8) each run is one tile-row ✅. Tile rows 1–2 = ordinals 8–23 = runs 1 and 2
✅. Sentinel at ordinal 10 → run 1's stored tiles 8, 9, 11…15 packed ✅ (`[R-SLB-03]`
sentinel transparency).

**§17.3 byte-shuffle.** 1.0f/2.0f/3.0f = 0x3F800000/0x40000000/0x40400000 → LE
`00 00 80 3F | 00 00 00 40 | 00 00 40 40` ✅. s = 4, n = 3; byte i of group j → offset
i·n + j. I built the permutation by hand: i=0 → 00 00 00; i=1 → 00 00 00; i=2 →
80 00 40; i=3 → 3F 40 40, giving `00 00 00 00 00 00 80 00 40 3F 40 40` ✅ — identical to
the printed result and to the prose gloss.

**§19.4 Note (planar all-channel).** Entries spaced N·20 region bytes ✅; two ordinals
differing by N ≥ 2¹⁶ cannot share a 2¹⁶-ordinal segment ✅.

**§20.3 Example.** 32-tile interleaved layer: index region = 32·20 + ⌈32/2¹⁶⌉·4 =
640 + 4 = **644** ✅, "one entry re-pointed, 31 byte-identical" ✅ (32 entries).
§20.3's Note: 10⁶ tiles × 20 = 20,000,000 ≈ "about 20 MB" ✅.

**§21.9 Note.** 2³² entries → 2³²/2¹⁶ = 2¹⁶ segments × 4 = 2¹⁸ = **256 KiB** ✅; 2³⁶ →
2²⁰ × 4 = 2²² = **4 MiB** ✅. 65,536 layers ≈ 12.5 MiB ⇒ 200 bytes/record, which is
consistent with "small layer records" (I derived the true floor: 24-byte header + 73-byte
minimal payload = 97 bytes, so 65,536 minimal records fit in ~6.1 MiB, comfortably inside
the 16 MiB row) ✅.

**§6.4 / Appendix B.** "dir_length plus the pre-trailer pad plus 64 within 65,536" =
64 KiB ✅.

Every number in every worked example is right. I found no arithmetic error anywhere in
this document.

---

## 6. The register tables, counted mechanically

The register is the document's largest table, and §21.1 makes its counting rule
*mechanical* ("Instances within a cell are separated by semicolons, and a cell reading —
is one instance; the count is therefore mechanical once the cell is written"), so I
executed that rule rather than eyeballing it.

Parsed every row (`^\| ?([FLTR]\d+) \|`), split on `|`, asserted six cells per row (no
row failed — so no cell contains a stray pipe), and counted semicolon-separated items in
cell 3.

- **Rows:** F = 35 (F1–F36, F11 absent), L = 49 (L1–L49, no gaps, no duplicates, in
  ascending order), T = 26 (T1–T26, ditto), R = 10 (R1–R10, ditto). Total **120**.
  §21.2 says "35 conditions" ✅, §21.3 "49" ✅, §21.4 "26" ✅, §21.5 "10" ✅, §21.8
  "120 conditions" ✅. F11's gap is deliberate and explained by the Note at line 3738 ✅.
- **Instances:** the semicolon rule summed to **277** across the 120 rows. §21.8 says
  "over 277 instances" ✅ — exact.

I then spot-audited the cells against §21.1's two stated axes:

- *Layout formulas are materially different shapes.* T3 = 3 layouts × 2 directions = 6 ✅;
  T14 = 6 ✅; T22 = 6 ✅; T21 = 3 (one direction, "larger than") ✅; L44 = 3 (one
  direction, "exceeds") ✅; T4 = 4 ✅; T26 = 3 ✅.
- *Two magnitudes ⇒ two directions; a bounded comparison ⇒ one; no ordering ⇒ none.*
  L21 "does not equal" = 2 layouts × 2 directions = 4 ✅; L22 = 2 directions + 2 named
  special cases = 4 ✅; L30 "differs from" = 2 ✅; F17 "does not equal" = 2 ✅; L37 and
  L38 (a stored checksum against a computed one) = 1 each ✅ — exactly what §21.1 says
  a checksum comparison gets.
- *A single predicate over several fields is one instance.* T12 (a sum against a bound)
  = 1 ✅; F3 = 2 (two containers, each one sum) ✅; F25 (a combination of two flag bits)
  = 1 ✅.
- L2's nine designated quantities: I checked the two dominance parentheticals it asserts.
  "planar C·N (which dominates the max disk ordinal (C−1)·N + (N−1))": (C−1)N + N − 1 =
  CN − 1 < CN ✅. "interleaved P·Q (which dominates V = P·C)": Q = ΣBᵢ ≥ C since every
  Bᵢ ≥ 1 ✅. I also asked why the packed-bool decoded size ⌈P/8⌉ is absent from L2 while
  it is present in L44 and T3: ⌈P/8⌉ ≤ P and P is already an instance, so no file could
  overflow on ⌈P/8⌉ without overflowing on P — it is not a distinguishable file. The
  omission is correct, not a gap.

**Every register row citation in prose resolves.** I extracted every `F\d+`/`L\d+`/
`T\d+`/`R\d+` token outside the tables (44 distinct labels, 108 sites) and checked each
against the defined set. All resolve; the only "miss" is F11 at line 3738, which is the
Note that says F11 is struck. I then read each citation against the row it names:

- §9.6 "§21.2 rows F8, F14 and F17 — the magic, the trailer CRC and the length
  cross-check" ✅ exact.
- §5.2 "L18's overlap or L40 through L42's placement" ✅ (L18 overlap; L40 alignment,
  L41 slab packing, L42 slab first-tile alignment — all verifier, reject-layer).
- §20.3 "T3, T14, T21, T22, T4, T5, T2 … (T24, T25)" ✅ — I mapped each: four
  decoded-size rows, padding position, pad bit, boolean byte, then the two decode-failure
  rows. Exactly right, including the ordering of the three categories.
- §20.5 "F36 and L25 for a record type, and one row for each of the other seven spaces
  §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates eight spaces;
  minus record type leaves seven; I mapped them: index encoding→L31, linearization→L33,
  sample type→L34, channel layout→L36, codec→L43, filter→L45, metadata encoding→R1. All
  seven present, none duplicated, none missing ✅.
- §21.1's specialization list. I verified each pair actually stands in the "every file
  exhibiting one exhibits the other" relation: F21 (slot (0,0)) ⇒ F22 (extent_length < 5)
  ✅; L10 ⇒ L11 ✅; F35 (reserved type, MU=1) ⇒ F36 (reserved type, any MU) ✅; L24 ⇒ L25
  ✅; F1's front-block instance ⇒ F6 ✅ (the reversed constant differs from the constant);
  F1's trailer-magic instance ⇒ F8 ✅.
- §21.2's reach derivation: "F8, F14, F6 and both of F1's instances … and no other row."
  I derived it independently from `[R-CNT-24]`'s four fixed invariants (magic at F−64,
  version_major/minor at F−56, CRC at F−4 over [F−64, F−4), constant front block) and
  got the same four rows. I checked the near misses: F13 (F mod 64 = 0) — 64-alignment is
  *not* among `[R-CNT-24]`'s invariants, so it does not reach ✅; F17, F9, F10, F12, F16
  all read fields inside the 48 bytes a future major may redefine ✅; F5 and F15 are
  handled explicitly by §2.3's Note ✅; F18 is outside the premise ✅.
- §2.3's "`[R-CNT-06]` states nine". I enumerated `[R-CNT-06]`'s own conditions
  (excluding the version and flag gates, which are §6.3's): magic, CRC, cfl = size,
  cfl mod 64, dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64,
  file_id ≠ 0, reserved zero = **nine** ✅, and exactly nine register rows carry
  `[R-CNT-06]` as governing (F8, F9, F10, F12, F13, F14, F15, F16, F17) ✅. "the trailer
  magic and the trailer CRC … and the other seven do not" ✅ — 2 + 7 = 9.

**Register completeness sweep.** I walked every requirement identifier
(`R-<PREFIX>-<NN>`; 17 prefixes, no numbering gaps except ENC-17…99, which the ENC-100
example in §2.2 explains) and asked, for each, whether it states a detectable
file-conformance condition and whether a row carries it. Everything resolved: SHOULDs
(`[R-CNT-03]`, `[R-ENC-14]`, `[R-TYP-10]`, `[R-CNT-26]`, `[R-CNT-09]`, `[R-LIF-07]`) are
outside `[R-CNF-12]`'s register; conduct rules (`[R-LIF-02]` steps 4/6, §10.3, §18.3) are
declared as such; `[R-ENC-06]` and `[R-CNT-18]`'s nesting bar are each explicitly said to
state no witness; `[R-SLB-04]`'s Note says its detection *is* `[R-SLB-03]`'s. The
file/layer partitions are clean: F25/F26/F28/F30/F31/F32 say "non-layer top-level" and
L46/L47/L49/L15/L16/L17 say "layer record or sub-record", so between them every record is
covered exactly once. §15.3's eleven entry states map onto T1, T6–T12, L18, F33 and
L40–L42 with nothing left over. I found no missing row.

**§15.3's own closed count.** "Six rows are marked *structural*" — I counted the literal
`*structural*` occurrences inside lines 2232–2244: **6** ✅ (and 3 `*verifier*` rows,
uncounted by the prose, correctly so).

---

## 7. The box figures, checked including character alignment

**§5.1, a file after three commits.** I measured the cell widths off the top border
(7, 11, 7, 11, 7, 6, 4, 8) and confirmed each content cell fills its width exactly
(" front " = 7, "  layer A  " = 11, "▓▓▓▓▓▓▓" = 7, " dir₃ " = 6, "pad " = 4,
" trail₃ " = 8). The under-brace row places `└` at columns 8, 28, 48 and `┘` at 20, 40,
69 — exactly on the `┬` positions of the border. The figure is dimensionally exact.

Semantically: with commit 1 = front + A + dir₁/pad/tr₁, commit 2 = B + dir₂/pad/tr₂,
commit 3 = dir₃/pad/tr₃, the two ▓ runs land precisely where the caption says
("the directories, pads and trailers of commits 1 and 2") ✅, layer A's structures never
move ✅ (`[R-WRT-05]`), and commit 3 is the "touches no layer and appends no record
extent" case ✅. Consistent with `[R-CNT-02]`'s partition: live state = front + both
layers' structures + dir₃ + trail₃; pad and ▓ are slack ✅.

**§9.2, what a crash sees.** The ▓ run in row 3 is 19 characters; " dirₙ │pad│ trailₙ "
in row 1 is 6+1+3+1+8 = 19 ✅. The two `↑` markers both sit at column 38, one past the
final `│` at 37, which is where F is and where trailₙ ends ✅. Row 3's layout
(old dir/pad/trailer → ▓, then new payloads, then dirₙ₊₁/pad/trailₙ₊₁) is exactly what
`[R-LIF-02]` step 1 ("begin writing at exactly F") produces ✅.

**§20.3, the three shapes.** (a) the ▓ run is 13 characters and " dir₁│pad│tr₁" is
5+1+3+1+3 = 13 ✅. (b) "▓index▓" is 7 and " index " is 7 ✅. (c) matches (a)'s ▓ run ✅.
Semantically (a) matches `[R-WRT-05]` (A's record carried byte-identically, slot and all)
✅; (b) matches `[R-WRT-04]` (whole region re-emitted at a new placement, retained
payloads do not move) ✅; (c) matches §20.4's PE = 0 drop licence and §20.3 step 4's fixed
list ✅, and it explicitly routes the user-metadata edit to shape (b) rather than leaving
it ambiguous ✅.

**§20.5, what compaction reclaims.** I checked the claim that hangs off the drawing: "In
this placement A's stored extents happen not to move, so A's index is copied and only its
slot re-pointed". In the input A's tiles begin immediately after the 16-byte front block;
in the output they do too — so A's extents are at identical offsets ✅, A's entry offsets
are unchanged ✅, and only its slot moves ✅. B's tiles do move (an intervening ▓ run is
gone), so B's index carries the `′` ✅. The figure and `[R-WRT-07]` agree.

**§15.1's normative region blockquote** — checked against `[R-CNT-17]` ✅ (above).

---

## 8. Restating tables, checked against the prose they restate

**§8.1 coverage map vs §4.5.** §4.5 names three exception classes (front block; the three
terminal checksum fields; the unassigned-type record extent) and three interior checksum
fields (segment CRC array, entry crc, crc_of_crc_array). I traced each of §8.1's seven
rows: front block → equality; trailer CRC covers [0,60) and is itself uncovered; directory
CRC covers dir_length − 4 and is uncovered; segment CRC array covered by
crc_of_crc_array, which lives in the directory and is covered by the directory CRC; entry
crc covered by its segment CRC; user-metadata terminal CRC uncovered; unassigned extent
uncovered. Every field of every structure lands under exactly one checksum, and every
exception §4.5 names has a row ✅. §8.2's chain (trailer → directory → crc_of_crc_array →
CRC array → segment → entry → tile) is the same graph read in dependency order ✅.

**§10.2's identifier spaces vs the eight owning sections.** Row by row against §7.3,
§14.1/`[R-SER-06]`, §11.4/`[R-GEO-05]`, §12.2/`[R-TYP-03]`, §17.2/`[R-COD-03]`,
§17.3/`[R-COD-09]`, §7.4/§15.1, §18.2/`[R-MTA-03]`: assigned, reserved and experimental
bounds match in all eight ✅. The two spaces with no experimental range (channel layout
u8; trailer flag lanes) are exactly the two the prose names ✅.

**Appendix C registry snapshot** vs §7.3, §12.1, §12.2's Note, §17.2, §17.3, §14.1,
§11.4, §15.1, §18.2, §6.3, §18.4 — every assignment and every pinned reservation matches ✅
(including "19 opaque" against §12.2's "19 for a fixed-size raw-bytes type").

**Appendix B constants** — I checked all 28 rows against their cited sections. All 28
match, including the two CRCs I recomputed and the eight-item "Reader minimum guarantees"
row against §21.9's eight table rows ✅.

**§21.9 vs §2.3 and §21.6.** The limits table's eight rows, the per-instance
individuation of the last three, and the two capability refusals §21.9 excludes ("a
foreign format major and an unimplemented top-level MU = 1 type") match §21.6's closing
paragraph ✅ — and §2.3's parenthetical that in a conforming file such a type is
necessarily experimental-range squares with §21.6's wording ✅.

**§2.4's outcome table** vs §20.4's table (preserve-verbatim = the MU = 1 and
MU = 0 / PE = 1 rows) ✅.

**Appendix H checklists.** I read each of the five entries against the requirements it
cites.
- *Reader*: "all four codecs, both filters, both layouts, all thirteen sample types, both
  user-metadata encodings, and both registered record types" — I counted each against
  §17.2 (4 core), §17.3 (2 core), §14.1 (2), §12.1 ("exactly thirteen"), §18.2 (1 and 2
  assigned), §7.3 (2 registered). All six counts correct ✅.
- *Writer*: matches `[R-TYP-06]`, `[R-SER-05]`, `[R-SER-08]`, `[R-MTA-05]`, `[R-LIF-02]`
  ("both barriers"), `[R-CNT-08]` (creator flags = 0 vs compactor carry-forward) ✅.
- *Updater*: its restatement of §20.3 step 4's closed list carries all four permitted
  changes and the channel-list exception "(not both in one commit)" ✅. I considered
  whether dropping the "A commit MAY make several of these changes at once" clause
  narrows it, and concluded not: the checklist attaches the "not both" caveat to exactly
  one item and to no other, which if anything signals that the others compose, and it
  defers explicitly ("only as §20.3 step 4 permits"). Not a finding.
- *Verifier*: I listed the twenty verifier-detected rows (F7, F25, F26, F27, F28, F33,
  F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26) and matched each to a
  clause. Nineteen match directly. T26 is the only one with no clause of its own — and
  T26's own condition cell says "the check that detects it is T2's or T4's", both of which
  the checklist carries, so nothing is unchecked. Not a finding.
- *File*: matches §2.4, `[R-CNT-02]`, §8.1, §21.2–§21.5, §21.6 ✅.

**§11.1's Rationale and §13.3's sparse-writing Note vs §20.3 step 4.** These are the two
places outside §20.3 that restate the closed list, and they are in this round's changed
surface, so I read them word against word. §11.1 carries all four permitted changes, the
"one or the other in a commit" channel-list exception, the "several of these in one
commit" composition permission, the "every other declaration is fixed" closure, the
empty-layer freedom, and the "a layer the commit itself empties does not qualify"
qualifier — the full shape, with nothing dropped and nothing added. I then verified its
index-cost claims arithmetically: a growth changing no grid count leaves N, every ordinal
and entry_count fixed, so the region is untouched ✅; a growth raising one grid count
while another stays 0 leaves ∏Gᵢ = 0, so entry_count = 0, extent_length = 0, slot (0,0)
and crc_of_crc_array = 0 all hold ✅; raising the *only remaining* zero grid count moves
entry_count off 0 and so does change the region ✅. §13.3's Note restates the same two
cases and agrees ✅. No divergence.

---

## 9. Findings

### diagrams-01 — CONTRADICTION — §4.7's Note says the §7.4 layout table omits two columns; it omits three

§4.7's Note states the presentation convention every layout table in this document
follows, and then accounts, table by table, for each table's departure from it:

> **Note.** Layout tables for fixed-layout structures give, per field:
> byte offset within the structure, size, type, name, taxonomy class,
> and valid range, each table giving the columns its structure needs.
> A packed variable-length payload — the layer
> record's inline payload (§7.4) — has no fixed offsets to give; its
> table omits the offset and class columns, and each field's class
> follows from the definitions above. §6.1's block is a 16-byte
> constant, where a Value column replaces type and range, and §7.2
> folds each field's range into its Field cell.

The §7.4 table's header is:

> | Field | Type | Constraint |

Three of the six named columns are absent, not two: offset, class **and size**. The Note
names only offset and class, and gives a reason for each of those two (no fixed offsets
to give; class follows from the definitions). No reason is given for the missing size
column, because the sentence does not know it is missing.

The reading that the sentence is merely non-exhaustive ("it omits, among others, offset
and class") is available but is not the one the passage supports. The same Note accounts
*exactly* for the other two deviant tables — §6.1's `| Offset | Size | Value | Class |`
is precisely "a Value column replaces type and range", and §7.2's
`| Offset | Size | Type | Field | Class |` is precisely "folds each field's range into
its Field cell". I verified this against the other three layout tables, which carry all
six columns: §6.2 (`| Offset | Size | Type | Field | Class | Valid values |`), §15.1 and
§18.2 (same six). The Note is otherwise precise; here it is not.

A second, smaller drift sits in the same place: the Note calls the sixth column "valid
range", §6.2/§15.1/§18.2 head it "Valid values", and §7.4 heads it "Constraint". Three
names for the column the Note names once.

I picked the exhaustive reading, because that is how the Note treats §6.1 and §7.2, and
because a reader deriving a new structure's presentation from this Note — which is what
the Note exists for — would produce a §7.4 table with a Size column and find the document
disagreeing with itself.

**Not byte-level.** §4.7's Note is labelled *Note* and so is non-normative under
`[R-CNF-01]`; the §7.4 table is normative and governs field order and widths regardless.
No conforming file's bytes turn on which columns a table prints. The cost is to a reader
auditing the document's own presentation, and to any future section adding a layout table
by following this Note.

### diagrams-02 — OBSERVATION — §20.5's slack-accumulation inventory omits superseded payloads and superseded record extents

§20.5's Example — "what compaction reclaims" — closes with the sentence an operator is
meant to size a compaction trigger from:

> Slack
> accumulates a directory, a pad and a trailer per commit, plus a whole
> index region for each layer whose stored-tile set or index content a
> commit changed (§20.3); a verifier
> whose walk completes reports the total (§9.7), and that total is
> what tells an operator when to run this.

The inventory is shaped as a complete accounting ("X per commit, plus Y per layer") and it
omits the largest term. §20.3's own Example says so in as many words:

> The prior index
> region and the superseded payload become slack, reclaimable
> only by compaction.

and §20.3 step 4 adds two more sources the sentence does not reach — "Extents this commit
supersedes become slack (`[R-CNT-21]`)" (which covers a replaced user-metadata document's
extent, routed there explicitly by §20.3's shape (c): "a new extent is appended and the
old one becomes slack, as in (b)") and a shortened planar channel list, which "leaves its
stored tiles' extents as slack".

Concretely: on §20.3's own worked figures, superseding one 100,000-byte tile of a 32-tile
layer adds 644 bytes of superseded index and about 128–192 bytes of superseded
directory/pad/trailer — and 100,000 bytes of superseded payload, which is 99% of the slack
that commit creates and which this sentence does not name. An operator reading only this
sentence would model slack growth as bounded by the layer count and the index size, and be
wrong by orders of magnitude on exactly the workload — "a long series of small edits"
(§1) — that §20.5 exists to remedy.

Two readings are available: that the sentence enumerates all sources of slack (false), or
that it enumerates only the per-commit *fixed overhead* and leaves data-proportional slack
to §20.3 (true but not signalled — the sentence carries no "at least", no "besides the
bytes it supersedes", and its §20.3 citation points at the paragraph that does name
payloads). I picked the first reading, because the sentence's grammatical shape is an
inventory and because it is the last sentence of the section, positioned as the operator's
takeaway.

**Not byte-level.** This is a labelled *Example* and therefore non-normative under
`[R-CNF-01]`; `[R-CNT-21]` and §9.7 define the slack total normatively and are correct.
No file's bytes and no accept/reject verdict move. The cost is an operator's compaction
policy.

### diagrams-03 — OBSERVATION — Appendix F is normative and omits RFC 1950 and RFC 1952, which normative text and a register row both cite

Appendix F is the one appendix whose heading carries no `(non-normative)` marker:
`### Appendix F — Normative references` — so under `[R-CNF-01]` ("appendices identified as
non-normative") it is normative text. It lists nine references plus one informative one.

Two documents cited in normative text are absent from it. `[R-COD-05]`:

> **Codec 2 — deflate.** The stored bytes are exactly one DEFLATE
> compressed data stream as defined by RFC 1951 — raw, not a zlib
> (RFC 1950) or gzip (RFC 1952) wrapper. `[R-COD-08]`

and §21.4's T15, whose *Instances* cell obliges the corpus (`[R-ERR-02]`, `[R-VEC-03]`:
"one vector per instance") to contain one file per named wrapper:

> zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip RFC 1952 member (1F 8B, trailing CRC32+ISIZE)

I confirmed by normalised search that RFC 1950 and RFC 1952 each occur exactly twice in
the whole document — once in `[R-COD-05]`, once in T15 — and nowhere in Appendix F, under
that name or any other. Every other RFC the document cites (2119, 3339, 3720, 8174, 8259,
8878, 1951) does appear there, as do IEEE 754, the LZ4 Block Format Description and the
Unicode Standard; OCP OFP8 is listed under an explicit "Informative" heading. So the
appendix is otherwise complete, and its two omissions are the two references that appear
only inside a *prohibition*.

The permitted readings: either Appendix F is the document's list of external documents an
implementer must obtain (in which case it is missing two), or it lists only the documents
needed to *produce* conforming output, excluding those needed only to recognise what is
excluded (in which case it is complete but says so nowhere, and a corpus builder working
from `[R-VEC-03]` still needs both). I picked the first, because the appendix carries no
scoping sentence at all — no "the following are required to implement", no completeness
disclaimer, unlike Appendix B, which explicitly says "this table is a finding aid".

**Not byte-level.** A payload carrying a zlib or gzip wrapper fails `[R-COD-05]` and
`[R-COD-08]` on the RFC 1951 test alone, without any reader consulting RFC 1950 or
RFC 1952; T15's own cell supplies enough detail (CMF/FLG + Adler-32; `1F 8B` + CRC32/ISIZE)
to build the vectors. No conforming implementation's accept/reject set moves. The cost is
to a reader who takes a normative "Normative references" appendix as the closed list of
what it must obtain.

### diagrams-04 — OBSERVATION — §21.1 describes the Governing-rule parenthetical as holding requirement identifiers; two rows put section references there

§21.1 states, normatively, what the register's last column carries:

> A Governing rule cell names that requirement first; any
> identifiers following it in parentheses are the further rules the
> condition reads, cited without brackets to keep them distinct from
> the governing one.

I extracted all 120 Governing-rule cells. 118 follow the rule exactly: a bracketed
identifier, then zero or more bare identifiers of the form `R-XXX-NN`. Two do not:

> | L26 | … | `[R-CNT-18]` (§7.3 registry table) |

> | L31 | … | `[R-CNT-23]` (§15.1) |

A section reference is not "an identifier", and the stated purpose of the
without-brackets convention — "to keep them distinct from the governing one" — does not
reach a `§` citation, which was never at risk of being mistaken for the governing rule.
There is a further asymmetry of the same kind inside §21.5: R6 ("A key … is empty or
contains a code point in U+0000 through U+001F") cites `[R-MTA-04]` (R-CNT-25, R-ENC-12)
while R10 ("A user-metadata document key is longer than 255 bytes"), which comes from the
same bullet of §18.2, cites `[R-MTA-04]` (R-ENC-12) with R-CNT-25 dropped — every other
R-row carries it.

Readings: either the sentence describes the column exhaustively (in which case L26 and
L31 depart from it), or "identifiers" is loose for "cross-references" (in which case the
"cited without brackets" clause has no application to a `§` and the sentence under-states
what the column may hold). I picked the first, because the sentence is written as a
reading instruction for a table whose completeness §21.1 makes normative, and because 118
of 120 cells follow it.

**Not byte-level, and it does not even move a verdict.** §21.1 already settles what
happens when a row and its rule disagree — "the rule governs" — and neither L26 nor L31's
outcome depends on the parenthetical. This is a presentation defect in a normative
paragraph about a normative table. I file it at the bottom of the list and would not
defend it as anything more.

---

## 10. Suspicions I opened and closed

- **Appendix A's dump might disagree with its annotation table, or with §6.2's layout
  table.** Closed by cutting every field at §6.2's offsets independently of the annotation
  and finding all ten identical, plus the trailer CRC recomputed to `0x402F157E`.
- **§7.4's example might mis-state one of its two CRCs, or mis-sum its 81 bytes.** Closed
  by recomputing both CRCs from a from-scratch CRC-32C validated on the `"123456789"`
  check vector, and by re-deriving every running offset in the dump from the §7.4
  constraint table.
- **The `0xEECB3BB2` all-sentinel constant might be wrong** (it is asserted in three
  places and can only be checked by computing 2¹⁶ × 20 bytes). Closed by computing it.
- **§21.8's "120 conditions over 277 instances" might not survive §21.1's mechanical
  counting rule.** Closed by executing the rule: 120 rows, 277 semicolon-separated
  instances, both exact.
- **A register row might be missing (§21.1 makes completeness normative).** Closed by
  walking every requirement identifier in the document and asking whether it states a
  detectable condition and whether a row carries it; and by checking that F-rows and
  L-rows partition the record space ("non-layer top-level" vs "layer record or
  sub-record") with no record on both sides and none on neither.
- **§21.2's reach claim ("and no other row") might over- or under-reach.** Closed by
  deriving it independently from `[R-CNT-24]`'s four invariants and getting the same four
  rows, then checking the six near misses individually.
- **Appendix H's updater checklist might have dropped the composition permission the
  round-32 repair added to §20.3 step 4.** Closed: it defers to step 4 explicitly, and it
  carries the one exception ("not both in one commit") attached to the one item that bears
  it and to no other — which signals composition rather than forbidding it.
- **Appendix H's verifier checklist might omit a verifier-detected row.** Closed by
  listing all twenty and matching each; T26, the only one without its own clause, says in
  its own cell that its detecting check is T2's or T4's, both of which the checklist
  carries.
- **§20.5's compaction figure might contradict `[R-WRT-07]` about which index is
  regenerated.** Closed: A's tiles begin at 16 in both input and output, so A's extents
  genuinely do not move, and only B's index carries the `′`.
- **§17.2's Note "§14.2's worked examples give 18 and 30 bytes" omits that example's
  12-byte planar tile.** Closed: the Note claims no exhaustiveness, both figures it names
  are correct, and its point (below 1 KiB, so single-segment framing) holds of 12 as well.
- **§14.5's example does not say whether its layer is interleaved or planar.** Closed:
  with one uint16 channel both layouts give 32 bytes and identical offsets — which
  §14.4's Note states as a general fact and I verified — so the example is
  layout-agnostic by construction, not by oversight.
- **§20.3's "the three shapes a commit takes" might be a closed count with a fourth
  shape.** Closed: the two candidates I could build — editing user metadata, and removing
  a planar channel from the end — are both routed explicitly by the surrounding text
  ("Editing user metadata is not this shape … as in (b)"; §20.3 step 4's channel-removal
  clause re-emits the region, which is (b)).
- **§20.5's "truncation past F and recovery … neither reclaims any [slack]" might be
  false of recovery**, which does shorten the file past slack bytes. Closed: recovery
  produces a different artifact — the earlier generation, with that generation's own
  slack — so it does not reclaim slack while preserving the live state, which is what
  "reclaims" means throughout §20.5 and §9.7.
- **Appendix B might not be the complete constant list it claims ("Every named constant
  this specification fixes, collected").** Closed against 28 rows and their cited
  sections; the candidates I probed (the user-metadata key length cap; the extent_length ≥ 5
  minimum; record and entry sizes) are all present, the key cap under the "Name length"
  row, which §4.6 makes reach metadata keys.
- **§8.1's map might leave a field uncovered or double-covered.** Closed by tracing the
  full chain against §4.5's exception list; every field lands under exactly one checksum
  and every named exception has a row.
- **§16.2's slab example might mis-partition the runs.** Closed: [0,8), [8,16), [16,24),
  [24,32) is the partition `[R-SLB-02]`'s `block_start + r·S` gives, and under row-major
  each is one tile-row of the 4 × 8 grid.

## 11. Where I found little, and what I did that would have found something

My charter's central instruments — recomputing checksums, cutting fields at their layout
offsets, re-deriving every count — all fired and all came back clean. That is a real
result rather than an absence of effort: had any printed CRC, offset, width or count been
wrong, the six checksum recomputations, the ten-field Appendix A decode, the seventeen
re-derived worked examples and the mechanical 120/277 register count would each have
caught it, and any one of them would have been the byte-level finding this round most
wants. I found no arithmetic error of any kind in this document, and I am confident there
is none in the printed figures and examples, because I recomputed rather than read every
number they contain.

The four findings I do have are all in *prose about* figures — a Note describing a table's
columns, an Example's inventory of slack, a normative reference list, a reading
instruction for the register — which is where this document's figure surface is thinnest
and where the arithmetic instruments cannot reach.

**No byte-level finding.** I did not force one. None of the four changes which byte
sequences a conforming implementation may emit or must accept or reject: three sit in
non-normative labelled blocks or a reference list, the fourth sits in a normative
paragraph whose own text ("the rule governs") already resolves any divergence it could
produce.
