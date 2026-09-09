# Cleanroom round 35 — Diagram auditor — working transcript

## 0. Access, disclosure, and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,864 lines). It was where the brief said it would be. I opened no ADR, no
`docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`, no charter, no
git history. I ran no web search and no web fetch. I did not list any directory
other than my own scratch directory.

**Context I did not ask for.** Before I began, my runtime placed material in my
context: a project instruction file (`CLAUDE.md`, which forwards to `AGENTS.md`),
an auto-memory index of the maintainer's notes with a dozen or so entry titles
naming things about this project's process, and a git-status block naming
several recent commit subjects. None of that is the specification and none of it
is evidence about the specification. I have disregarded all of it. I name that
it appeared without repeating its contents; the one place it is visible in my
work is that I did not need to guess where the spec file was.

**Scratch directory.** `/private/tmp/.../r35-round/scratch/diagrams/` — I created
it; it was **empty** when I began (no previous attempt's files). I wrote five
files there, all mine, all named with a `_dg` suffix precisely so that no other
lane's identically-named script could be substituted for one of mine between
calls:

- `crc32c_dg.py` — a from-scratch CRC-32C (Castagnoli, reflected, init/final
  0xFFFFFFFF), self-tested against the document's own check vector.
- `appA_dg.py` — parses Appendix A's hex dump and decodes every trailer field.
- `sec74_dg.py` — rebuilds §7.4's 81-byte layer-record payload from its
  annotated dump and recomputes both CRCs.
- `examples_dg.py` — recomputes every worked numeric example in the document.
- `count_dg.py`, `sweeps_dg.py` — register row/instance counting and
  whitespace-normalised phrase sweeps.

I wrote nothing to the parent, to a shared temp directory, or to the repository.
I did not read or list the output directory.

**Method.** Enumerate every figure, dump, layout table, worked example, checklist
and numbered list *first*, with line numbers, so coverage is checkable. Then
recompute rather than eyeball: every checksum from the printed bytes, every
offset from the structure's own layout table, every count from the rows
themselves.

---

## 1. Inventory (enumerated before judging any of it)

### 1.1 Fenced figures and dumps — 8, all of them

| Lines | What |
|---|---|
| 665–670 | §5.1 Example — a file after three commits (box diagram) |
| 1176–1195 | §7.4 Example — annotated 81-byte layer-record payload dump |
| 1330–1339 | §9.2 Example — what a crash sees (three rows) |
| 3364–3368 | §20.3 Example shape (a) — a new layer |
| 3382–3386 | §20.3 Example shape (b) — tiles added |
| 3416–3419 | §20.3 Example shape (c) — change confined to the directory |
| 3590–3596 | §20.5 Example — what compaction reclaims |
| 4436–4445 | Appendix A — 128-byte annotated hex dump |

### 1.2 Tables — 25, located by scanning for `|---` separator rows

Line of header row: 127 (§2.2 prefixes), 304 (§2.4 outcomes), 786 (§6.1 front
block), 829 (§6.2 trailer), 1005 (§7.2 record header), 1081 (§7.3 record types),
1110 (§7.4 layer-record payload), 1228 (§8.1 coverage map), 1572 (§10.2 identifier
spaces), 1786 (§12.1 sample types), 2020 (§14.2 decoded size / offsets),
2193 (§15.1 index entry), 2242 (§15.3 entry validity), 2641 (§18.2 encoding),
2844 (§18.4 standardized keys), 3451 (§20.4 updater obligations), 3748 (§21.2),
3797 (§21.3), 3857 (§21.4), 3907 (§21.5), 3927 (§21.6 non-violations),
4058 (§21.9 limits), 4447 (Appendix A annotations), 4482 (Appendix B constants),
4580 (Appendix E changelog).

### 1.3 Labelled blocks

20 `**Example`, 60 `**Note`, 13 `**Rationale`. These are non-normative by
[R-CNF-01]; I checked which side of the line each finding candidate sat on before
grading it.

### 1.4 The unlabelled blockquote

I ran an explicit scan for blockquote runs carrying no *Note* / *Example* /
*Rationale* label. **Exactly one exists**, at lines 2188–2189 (§15.1):

> `[ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`

It is therefore **normative** text, and it is a figure in my charter. Its content
is arithmetically identical to [R-CNT-17]'s
`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`. No divergence.

### 1.5 Numbered lists — 5 block lists + 2 inline sequences, all checked

Mechanically extracted and checked for order, gaps and duplication:

- §10.1 extension vehicles, lines 1552–1556, `[1,2,3,4]` — OK
- §19.1 open algorithm, lines 2908–2930, `[1,2,3,4]` — OK
- §19.4 tile-read algorithm, lines 3037–3071, `[1..8]` — OK
- §20.3 append procedure, lines 3163–3333, `[1..6]` — OK
- Appendix G profile, lines 4620–4750, `[1..10]` — OK
- §9.2 commit protocol inline `(1)…(6)` — OK, in order
- §6.4 remote open inline `(1)…(2)` — OK

No item out of order, duplicated, or missing anywhere.

---

## 2. Checksums recomputed from the printed bytes

I wrote CRC-32C from the parameters §4.5 states (polynomial 0x1EDC6F41 →
reflected 0x82F63B78, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF)
and validated the implementation against the document's own check vector
**before** using it on anything:

```
CRC-32C("123456789") = 0xE3069283   — document states 0xE3069283  ✓
CRC-32C(zero bytes)  = 0x00000000   — document states 0x00000000  ✓
```

Then, on printed bytes only:

| Where | Stated | Computed | |
|---|---|---|---|
| Appendix A trailer CRC over trailer[0,60) | `0x402F157E` (`7E 15 2F 40`) | `0x402F157E` | ✓ |
| Appendix A directory region [16,20) | `0x00000000` (CRC of zero bytes) | `0x00000000` | ✓ |
| §7.4 segment-0 CRC over 4 sentinel entries (80 bytes) | `0x80A34955` stored `55 49 A3 80` | `0x80A34955`, LE `55 49 a3 80` | ✓ |
| §7.4 `crc_of_crc_array` over that 4-byte array | `0xC4EE982E` stored `2E 98 EE C4` | `0xC4EE982E`, LE `2e 98 ee c4` | ✓ |
| §15.4 / Appendix B CRC of a full all-sentinel segment (65,536 × 20 = 1,310,720 bytes) | `0xEECB3BB2` | `0xEECB3BB2` | ✓ |

Every checksum the document prints is correct. The `55 49 A3 80` / `2E 98 EE C4`
little-endian byte orders in the §7.4 dump are also correct, and `7E 15 2F 40`
in Appendix A likewise.

---

## 3. Appendix A, byte by byte

I parsed the 8-line dump (128 bytes, confirmed length) and decoded the trailer
from §6.2's own layout table — reading each field's offset and width out of the
table, cutting those bytes out of the dump, and decoding them:

```
file length        128            (§5.1 "exactly 128 bytes")            ✓
[64,72) magic      8a 4e 52 41 54 0d 0a 1a   = §6.2's constant          ✓
[72,74) version_major  1          (§6.2: 1; 0 invalid)                  ✓
[74,76) version_minor  0          (descriptive)                         ✓
[76,80) flags          0          (§6.3: creator writes flags = 0)      ✓
[80,88) dir_offset     16         (≥ 16)                                ✓
[88,96) dir_length     4          (≥ 4)                                 ✓
[96,104) cfl           128        (= F; multiple of 64: 128 = 2·64)     ✓
[104,112) file_id      0x0123456789ABCDEF  (≠ 0), LE bytes EF CD AB 89 67 45 23 01 ✓
[112,124) reserved     12 bytes, all zero                               ✓
[124,128) trailer CRC  0x402F157E = recomputed                          ✓
[20,64) pre-trailer pad 44 bytes, all zero                              ✓
```

Every one of the annotation table's 13 rows matches the dump. The byte ranges in
the annotation table partition [0,128) exactly with no gap and no overlap:
[0,8) [8,16) [16,20) [20,64) [64,72) [72,74) [74,76) [76,80) [80,88) [88,96)
[96,104) [104,112) [112,124) [124,128).

The prose after the dump: "112 bytes covering [16, 128) contains the directory,
so §6.4's containment test applies, while bytes [0, 16) stay non-resident". A
128-byte file's 112-byte suffix is exactly [16,128) — the directory [16,20) is
inside and [0,16) is outside. Correct. And dir_length + pad + 64 = 4 + 44 + 64 =
112 ≤ 65,536, so [R-CNT-09]'s discovery-window advice is satisfied. Correct.

Appendix A is labelled non-normative and the surrounding text treats it as such
("this table is a finding aid", "each entry's authority is the requirement or
section cited").

---

## 4. §7.4's layer-record dump, byte by byte

I rebuilt the payload from the annotated dump, asserting at each line that the
printed offset equals the number of bytes accumulated so far. **Every printed
offset is right**; the payload is 81 bytes as stated. Decoding each field from
§7.4's own field table, in table order:

```
[0,4)   03 73 73 74               name len 3, "sst"                    ✓
[4,5)   01                        layout 1 = interleaved               ✓ (§14.1: 1=interleaved)
[5,7)   01 00                     linearization 1 = row-major          ✓ (§11.4)
[7,9)   01 00                     codec 1 = none                       ✓ (§17.2)
[9,11)  01 00                     filter 1 = none                      ✓ (§17.3)
[11,19) 00×8                      A = 0 (none declared)                ✓
[19,27) 00×8                      S = 0                                ✓
[27,35) 00×8                      A_slab = 0, forced by S=0            ✓ ([R-CNT-23])
[35,36) 01                        rank d = 1                           ✓ (≥1)
[36,38) 01 00                     C = 1                                ✓ (≥1)
[38,40) 01 78                     dim name len 1, "x"                  ✓
[40,48) 64 00…                    extent 100                           ✓
[48,56) 20 00…                    tile extent 32                       ✓
[56,63) 04 74 65 6D 70 0C 00      channel "temp", type 12 = float32    ✓
[63,68) 04 00 00 C0 7F            fill len 4, bits 0x7FC00000 (qNaN)   ✓
[68,69) 01                        index_encoding 1                     ✓
[69,77) 04 00…                    entry_count = 4                      ✓
[77,81) 2E 98 EE C4               crc_of_crc_array = 0xC4EE982E        ✓
```

The order matches §7.4's table row-for-row with nothing packed out of order and
no padding between fields, as [R-CNT-18] requires.

Cross-checks the Example itself asserts, all recomputed:

- grid count ⌈100/32⌉ = 4 → `entry_count = 4` = N (interleaved) — [R-CNT-17] ✓
- entry array = 4 × 20 = 80 bytes; segment CRC array = ⌈4/2¹⁶⌉ × 4 = 4 bytes ✓
- extent slot length = 4×20 + ⌈4/2¹⁶⌉×4 = **84** — document says 84 ✓
- "Name and the nine scalars from layout through channel count occupy 4 + 34
  bytes": the nine scalars are layout(1) + linearization(2) + codec(2) +
  filter(2) + A(8) + S(8) + A_slab(8) + d(1) + C(2) = **34**, and there are
  exactly nine of them. Name is 4. 4+34 = 38 = the offset of the dimension entry ✓
- "the dimension entry 18": 56 − 38 = 18 ✓
- "the channel entry 12": 68 − 56 = 12 ✓ — and this is byte-for-byte §12.3's
  `temp` entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, as the Example claims ✓
- "the trailing fixed fields 13": 81 − 68 = 13 ✓
- 4 + 34 + 18 + 12 + 13 = 81 exactly, so the sub-record sequence is empty ✓

Consistency of the *rules the Example cites*: [R-IDX-05] licenses the constant
`0xEECB3BB2` only for a **full** segment and requires a partial segment's CRC to
be computed. This segment covers 4 entries — partial — so a computed value is
required, and 0x80A34955 is what I compute. The Example is on the right side of
that rule.

---

## 5. Every other worked example, recomputed

All of these were recomputed in `examples_dg.py`; all pass.

**§11.2** extents (1024,2048), tiles (256,256): G = (4,8) ✓, N = 32 ✓,
P = 65,536 ✓. With extents (1000,2048): G_y = ⌈1000/256⌉ = 4 ✓.

**§11.4** grid (4,8): (0,0)→0 ✓, (0,1)→1 ✓, (1,0)→1·8+0 = 8 ✓. Coordinate
(300,700) → tile (1,2) ✓, s = 10 ✓, in-tile (44,188) ✓, in-tile ordinal
44·256+188 = 11,452 ✓. Planar C=4: disk ordinal 2·32+10 = 74 ✓.
The d = 1 degenerate case: with the empty-product convention the ordinals reduce
to u₀ and t₀ as §11.4 states ✓.

**§14.2** interleaved, T=(2,3), P=6, channels uint8+uint16: Q = 3 ✓, decoded size
18 ✓; in-tile (1,2) → ordinal 1·3+2 = 5 ✓; sample at [15,18), `a` at 15, `b` at
16–17 ✓. Planar `b`: 12 bytes, ordinal 5 at bytes 10–11 ✓. float32+bool
interleaved: Q = 5 ✓, size 30 ✓, ordinal 5 at [25,30), `t` 25–28, `m` at 29 ✓.
The closing generalisation "channel c's value at in-tile ordinal u sits at byte
u·Q + Fᶜ — the table's forms with k = u·C + c" is algebraically exactly the
table's `(k div C)·Q + F_{k mod C}` ✓.

**§14.3** planar bool, T=(2,5), P=10, alternating true/false from ordinal 0. I
built the packed plane both ways:
fill false → `55 01`; fill true → `55 fd`. The document states `55 01` and
`55 FD`. ✓ Decoded size ⌈10/8⌉ = 2 ✓; six pad bits (bits 2–7 of byte 1) ✓.

**§14.5** extents (5,5), tiles (4,4): grid 2×2 ✓; the edge tile at (1,1) covers
coordinates 4–7 on both axes, and enumerating them gives exactly **one** real
position, (4,4), and **15** padding positions ✓; one uint16 channel → decoded
tile 16·2 = 32 bytes ✓; fill 0xABCD little-endian is `CD AB` ✓; value 0 is the
stored sample and values 1–15 are the fill ✓.

**§17.3** byte-shuffle of 1.0f, 2.0f, 3.0f. `struct.pack('<fff',...)` gives
`00 00 80 3f 00 00 00 40 00 00 40 40` — exactly the document's bytes ✓. Applying
"byte i of group j goes to offset i·n + j" with s=4, n=3 gives
`00 00 00 00 00 00 80 00 40 3f 40 40` — exactly the document's shuffled bytes ✓,
and the prose gloss "the three first bytes, the three second bytes, then
`80 00 40`, then `3F 40 40`" reads off that result correctly ✓. I also applied
the stated inverse ("restores byte i·n+j to offset j·s+i") and it reproduces the
original image exactly ✓.

**§15.4 first Example**, entry_count = 1,000,000: segments ⌈10⁶/2¹⁶⌉ = **16** ✓;
15 full, the last covering 10⁶ − 983,040 = **16,960** ✓; CRC array 16×4 = **64**
bytes ✓; index region 10⁶·20 + 64 = **20,000,064** ✓; k = 999,999 lies in
segment 999999 div 65536 = **15** ✓ at segment-relative byte 20·16,959 =
**339,180** ✓; CRC array at [20,000,000, 20,000,064) ✓; segment 15 at
[19,660,800, 20,000,000) ✓ — 339,200 bytes, "~339 KB" ✓; "never more than one
full segment (1.25 MiB)": 65,536·20 = 1,310,720 = exactly 1.25 MiB ✓;
1 ≤ entry_count ≤ 65,536 → one segment, 4-byte array ✓; entry_count = 0 → zero
segments, zero-byte array, slot (0,0), crc_of_crc_array = 0 ✓ (and that agrees
with [R-CNT-17]'s "and 0 when entry_count is 0" and [R-CNT-23]).

**§15.4 second Example**, planar C=4, N=32: disk ordinal 2·32+10 = 74 ✓; entry at
region bytes [74·20, 75·20) = **[1,480, 1,500)** ✓; channel 3's block is
[3·32, 4·32) = entries **96–127**, thirty-two of them ✓.

**§16.2 Example**, N=32, S=8: runs [0,8),[8,16),[16,24),[24,32) — exactly four,
none partial ✓; tile rows 1–2 = ordinals 8–23 = runs 1 and 2 ✓ (row-major makes
G_x = 8 the fast axis, so a run of 8 is one tile-row ✓); the sentinel-at-10 case
is [R-SLB-03]'s "Sentinel tiles are transparent to run continuity" applied
correctly ✓.

**§20.3 Example**, 32-tile interleaved layer: index region 32·20 + ⌈32/2¹⁶⌉·4 =
**644** ✓, "one entry re-pointed, 31 byte-identical" — 32 entries ✓. §20.3's Note:
10⁶ tiles → 10⁶·20 = 20,000,000 ≈ "about 20 MB" ✓.

**§21.9 Note**: 2³² tiles → 2³²/2¹⁶ · 4 = 262,144 = **256 KiB** ✓; at 2³⁶ →
2²⁰·4 = **4 MiB** ✓; 65,536 layers at 200-byte records = 13,107,200 = exactly
**12.5 MiB** ✓. §24's "tens of gigabytes": 2³²·20 = 85.9 GB ✓.

**§19.4 Note**: entries for one spatial ordinal are spaced N·20 region bytes
apart; for N ≥ 2¹⁶ two such entries differ by ≥ 2¹⁶ in ordinal, so they cannot
share a 2¹⁶-entry segment ✓ — the "guaranteed to fall in different segments"
claim is exactly right at the boundary N = 2¹⁶, which is where I checked it.

**§14.4 Note** (a degenerate-case claim, so I built the degenerate case): at
P = 1 a single-channel bool layer's planar image is one byte carrying value 0 in
bit 0 and the fill bit in bits 1–7, while the interleaved image is 0x00 or 0x01.
Enumerating all four (value, fill) combinations: they coincide for both values
when fill is false and for neither when fill is true — so "the images coincide
exactly when that fill is false" is correct, in both directions ✓. And
"a single-channel numeric layer produces byte-identical tile images under either
layout" checks out: with C = 1, F₀ = 0 (empty sum) and Q = B, so the interleaved
offset k·Q equals the planar k·B ✓.

**§12.1/§12.3** bfloat16 1.0 = high 16 bits of binary32 0x3F800000 = 0x3F80,
stored `80 3F` ✓; 0x7FC0 ↔ binary32 0x7FC00000 quiet NaN ✓. §12.3's channel entry
is 1+4+2+1+4 = 12 bytes and its bytes match the §7.4 dump exactly ✓.

**§4.6** `température` in NFC: t e m p é r a t u r e = 11 characters, and
`74 65 6D 70 C3 A9 72 61 74 75 72 65` is 12 bytes with `é` = `C3 A9` ✓; NFD `é` =
`65 CC 81` gives 13 ✓.

**§13.3** fills 0xFF/0x00/0x00 → tuple (255, 0, 0) ✓; planar mixed case ✓.

**§17.2's Note on Window_Size** cites "§14.2's worked examples give 18 and 30
bytes, §14.3's gives 2" — 18 ✓, 30 ✓, 2 ✓ (see §5 above).

**§17.2's zstd/lz4 magics**: `28 B5 2F FD` is 0xFD2FB528 little-endian ✓;
T23's LZ4 frame magic `04 22 4D 18` is 0x184D2204 ✓; T15's gzip `1F 8B` ✓.
`0x7E000000` = 2,113,929,216 — the LZ4 block-format input bound ✓.

---

## 6. Diagram-by-diagram reading (the non-arithmetic half)

**§5.1, a file after three commits.** Two ▓ runs; the caption says they are
"the directories, pads and trailers of commits 1 and 2". I reconstructed the
history: commit 1 lays down front + A + dir₁/pad/tr₁; commit 2 appends B +
dir₂/pad/tr₂; commit 3 touches no layer and re-emits directory, pad, trailer
alone. That places commit 1's superseded tail between A and B and commit 2's
between B and dir₃ — which is exactly where the figure draws them. The figure's
own third commit is drawn as `dir₃│pad│trail₃` with no new payload, which is the
"touches no layer and appends no record extent" case the accompanying text names.
Consistent. The figure explicitly disclaims the one thing it could be
over-read for: "The grouping under the box is illustrative: a layer's structures
need not be contiguous or ordered ([R-SLB-05]), and §20.5's figure shows the
general case" — and §20.5's figure does show A's tiles disjoint from A's index.

**§9.2, what a crash sees.** Row 1's arrow marks F at the end of trailₙ ✓.
Row 2 hatches only the partial write past trailₙ, leaving trailₙ intact but no
longer terminal — which is what makes the reader's default path ([R-LIF-05])
report torn rather than scan back ✓. Row 3 hatches exactly `dirₙ│pad│trailₙ`,
the structures commit n+1 superseded, and leaves the earlier `…` (payloads) live
✓. The legend ("in row 2 the partial write of an interrupted commit, in row 3 the
structures commit n + 1 superseded") matches the drawing in both rows.

**§20.3's three shapes.** (a) draws A untouched and the old dir/pad/tr hatched,
with A's record carried into dir₂ byte-identically — that is [R-WRT-05] plus
§20.3 step 4's "A layer whose record alone changes keeps its extent slot" ✓.
(b) hatches the old index region and the old dir/pad/tr and draws `index′` as
"every entry, re-emitted" — matching step 4's "re-emitted in full — entry_count
entries plus the segment CRC array — necessarily at a new placement" ✓.
(c) draws only the directory changing ✓.

I checked (c) against the changed permitted-change list: of the permitted
changes to a layer that stores a tile, the ones that are genuinely confined to
the directory are a rename, an alignment or slab **clearing**, and a grid-count-
preserving extent growth (§11.1's Rationale: "taken alone touches the directory
alone"). (c)'s gloss names "clearing a slab declaration, renaming a layer, or
dropping a PE = 0 record". See §7 below for why I did not file this.

**§20.5, what compaction reclaims.** This is the figure I checked hardest,
because it makes a discriminating claim. Input: `front│A│▓▓▓▓│B│▓▓│A:index│▓▓│B:index│▓▓▓│dir│pad│tr`,
file_id = X. Output: `front│A│B│A:index│B:index′│dir│pad│tr`, file_id = Y.
A starts at 16 in both, so A's stored extents do not move; B moves left. The
caption says exactly that: "In this placement A's stored extents happen not to
move, so A's index is copied and only its slot re-pointed", and only B's index
carries the ′. That is [R-WRT-07]'s rule applied correctly — a region is
regenerated when *its own stored extents* relocate, not when the region itself
relocates. A's index region does relocate in the figure and is nevertheless
copied, which is the subtle case, and the figure gets it right. The fresh
file_id Y ✓ ([R-WRT-06]).

**§15.1's unlabelled (normative) region figure.** Arithmetically identical to
[R-CNT-17]. No divergence.

---

## 7. Cross-table restatement checks

### 7.1 §4.7's Note on presentation, against all six layout tables

The Note claims: fixed-layout tables give offset, size, type, name, class, valid
range; the packed variable-length payload's table (§7.4) "omits the offset, size
and class columns"; §6.1's table replaces type, name and range with a Value
column; §7.2 "folds a field's range into its Field cell where it states one".
Checked against every layout table in the document:

| Table | Columns delivered | Note's account |
|---|---|---|
| §6.2 trailer | Offset, Size, Type, Field, Class, Valid values | full six ✓ |
| §15.1 index entry | Offset, Size, Type, Field, Class, Valid values | full six ✓ |
| §18.2 encoding | Offset, Size, Type, Field, Class, Valid values | full six ✓ |
| §6.1 front block | Offset, Size, **Value**, Class | Value replaces type+name+range ✓ |
| §7.2 record header | Offset, Size, Type, Field, Class (no range column) | range folded into Field ✓ |
| §7.4 inline payload | Field, Type, Constraint | offset, size, class omitted ✓ |

And §7.2's Field cells do state ranges where they have one ("type (0 invalid)";
"flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved") and
not where they don't (inline_length, extent_offset, extent_length — whose bounds
are in [R-CNT-12] and [R-CNT-13] "below the table") ✓. The Note accounts for all
six tables and no seventh exists: I confirmed the layer record's inline payload
is the only packed variable-length payload with a table (the user-metadata inline
payload is one fixed byte and has offsets; the index entry is fixed).

### 7.2 §8.1's coverage map against §4.5

§4.5 names three terminal checksum fields (trailer, directory-region,
user-metadata) and three interior ones (segment CRC array, entry crc,
crc_of_crc_array). Reading §8.1's map: the trailer CRC at [60,64) covers [0,60)
and nothing covers it → terminal ✓; the directory's final 4 bytes → terminal ✓;
the user-metadata extent's final 4 bytes → terminal ✓; the segment CRC array is
"itself covered by the layer record's crc_of_crc_array" → interior ✓; the entry's
crc field lies inside the entry, covered by the segment CRC → interior ✓;
crc_of_crc_array lies in the layer record inside the directory → interior ✓.
Exactly three and three. The map's seven rows also cover all five [R-CNT-02]
classes with record extents split three ways (index region / user-metadata
extent / unassigned type), which is exhaustive over the record types that can
carry an extent.

### 7.3 §10.2, Appendix B, Appendix C against their defining sections

- §10.2's eight rows each match the defining section's value set. Where a
  defining section subdivides its reserved range (§11.4 splits 2–3 from
  4–0x7FFF; §12.2 splits 14–19 from 20–0x7FFF), §10.2 collects them as one
  reserved range and the corresponding register rows (L33, L34) enumerate the
  split — which is consistent, not divergent.
- Appendix B's 25 rows: I checked every value against its defining section.
  All match. The two CRC constants and the sentinel pattern are byte-identical
  to their definitions and to the recomputed values.
- Appendix C's snapshot: record types, 13 sample types, pinned reservations
  14–19, 4 codecs, 2 filters, 2 layouts, 1 linearization, 1 index encoding,
  2 metadata encodings, the flag lanes, and 6 standardized keys — every one
  agrees with the defining section, and the key list has exactly the 6 rows
  §18.4's table has.
- All 4 occurrences of `0x7E000000`, 3 of `0xEECB3BB2`, 5 of the trailer magic,
  4 of the front magic, 3 of the zstd magic and 3 of `FF ×16 00 ×4` are
  byte-identical across their occurrences.

### 7.4 §21.6's non-violation table, entry by entry against its Rule cells

All 15 entries check out against the rules they cite; I read each governing rule
and compared. The two that most needed checking:
- "The file contains zero layers → A conforming file … an empty directory
  included" against [R-CNT-14]'s "zero is valid: a directory carrying no layer
  record is a conforming generation, an empty directory included" ✓ verbatim.
- "A payload contains a byte string that mimics a trailer → … a recovery tool
  re-verifies its output whole (§9.6) — which catches any mimic that is not
  itself a consistent generation; §9.6's second caution covers the rest". §9.6
  does state two cautions, and its *second* is the rollback-indistinguishability
  one, which is precisely "the rest" ✓.

### 7.5 §20.4's updater table against §2.4

§2.4's preserve-verbatim row says "§20.4's table states the cases: its MU = 1 and
MU = 0 / PE = 1 rows". §20.4's table has three rows and exactly those two require
retention ✓. There is no MU = 1 / PE = 0 row, correctly, because [R-CNT-12] reads
that combination as PE = 1 — which the prose above the table states.

---

## 8. Register counting — done mechanically, not by eye

I parsed all 120 register rows out of the four tables and counted instances by
splitting each Instances cell on semicolons, treating an em-dash cell as one:

| Subsection | Rows found | Rows stated | Instances |
|---|---|---|---|
| §21.2 | 35 (F1–F36 less the struck F11) | "35 conditions" ✓ | 56 |
| §21.3 | 49 (L1–L49) | "49 conditions" ✓ | 116 |
| §21.4 | 26 (T1–T26) | "26 conditions" ✓ | 55 |
| §21.5 | 10 (R1–R10) | "10 conditions" ✓ | 50 |
| **Total** | **120** | §21.8: "120 conditions" ✓ | **277** — §21.8: "277 instances" ✓ |

Both figures §21.8 states are exactly right, and F11's retirement leaves the
gap the Note at line 3786 says it leaves.

I then checked whether each cell *correctly applies* §21.1's two stated axes
(the count matching does not by itself prove that):

- **Layout axis** ("where the quantity a condition derives varies by layout, the
  cell enumerates them"): T3 (6 = 3 layouts × 2 directions), T14 (6), T21 (3),
  T22 (6), L44 (3), L21 (4 = 2 layouts × 2 directions), T4 (4), T26 (3) — all
  enumerate. T2 and T5 are single-layout conditions and enumerate one, correctly.
- **Magnitude axis**: every *differs from / does not equal / is not exactly / is
  not 1* row enumerates two directions (T3, T14, T22, L21, L22, L30, F17, F23,
  L12); every *exceeds / larger than / below / less than / past* row enumerates
  one (L44, T21, F2, F3, F5, F9, F10, F16, F32, L1, L2, L17, R10, T9, T11, T12);
  every checksum comparison enumerates one (F14, F20, L37, L38, T1, R2); every
  byte-pattern-against-a-constant enumerates one per container (F1, F6, F8, T17,
  T23); every nonzero-value test enumerates one (L20, L27, L28, T19, F12).
- **Single predicate over several fields**: T12 (a sum against a bound) = 1 ✓,
  F25 (two flag bits) = 1 ✓, L20 = 1 ✓ — exactly as §21.1 prescribes.

I found no cell that misapplies either axis.

I also checked L2's omission of the packed-bool decoded size ⌈P/8⌉ from its
overflow instances, since every other derived-size row lists three layouts. It is
correct to omit: ⌈P/8⌉ < P ≤ 2⁶³−1 whenever P is in domain, so no distinguishable
file exists where ⌈P/8⌉ overflows and P does not.

**Governing-rule cell format.** §21.1 claims a cell "names that requirement
first; any identifiers following it in parentheses are … cited without brackets",
and that a section may appear there "a value set (L31) or a registered type's
scope (L26)". I validated all 120 cells against that grammar mechanically:
0 malformed, and the only two rows citing a `§` in the parenthetical are exactly
**L26** and **L31** — the two §21.1 names. The convention is stated and kept.

**§21.2's reach derivation.** "Deriving it there yields F8, F14, F6 and both of
F1's instances … and no other row." I derived it independently from [R-CNT-24]
(trailer magic at F−64, version fields at F−56, CRC-32C at F−4 over [F−64, F−4),
the front block constant) and got the same set: F8 (magic), F14 (trailer CRC),
F6 (front block, both instances), F1 (both instances). Everything else asserts
either a field inside the 48 bytes a future major may redefine (F13, F15, F17,
F19 and the dir/extent rows) or a format-major-1 derivation (F5) — and §2.3's
Note independently confirms F5 and F15 do not reach and F14 does. Consistent.

**§21.1's specialization list.** F1's front-block instance ⊂ F6 ✓; F1's
trailer-magic instance ⊂ F8 ✓; F35 ⊂ F36 ✓; L24 ⊂ L25 ✓; F21 ⊂ F22 (slot (0,0)
forces extent_length = 0 < 5) ✓; L10 ⊂ L11 ✓. All six pairs hold in the direction
claimed.

**§21.7's witness list.** §20.3 cites "(T3, T14, T21, T22, T4, T5, T2)" for
decoded size / padding / pad bits / boolean bytes and "(T24, T25)" for a decode
that fails outright. Mapping each label to its row: T3, T14, T21, T22 are the
four decoded-size witnesses; T4, T5 the padding and pad-bit witnesses; T2 the
boolean byte; T24, T25 the decode failures. Nine labels, nine correct rows,
grouped in the same order as the prose enumerates the categories.

**§20.5's space list.** "one row for each of the other seven spaces §10.2
tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates 8 spaces; less
record type leaves 7. The seven labels map one-to-one onto index encoding,
linearization, sample type, layout, codec, filter, metadata encoding — each
distinct, none repeated, none missing, and each row does register the
reserved-range value as a violation. Correct.

---

## 9. Checklists (Appendix H) and the profile (Appendix G)

**Appendix H, five checklists for §2.3's five classes.** I read each entry against
the rule it cites.

- *Conforming reader*: "all four codecs, both filters, both layouts, all thirteen
  sample types, both user-metadata encodings, and both registered record types".
  Counted against the defining sections: 4 core codecs (§17.2), 2 core filters
  (§17.3), 2 layouts (§14.1), 13 core sample types (§12.1 — "exactly thirteen …
  all core"), 2 assigned metadata encodings (§18.2, both core), 2 registered
  record types (§7.3). Every number right, and each matches [R-CNF-03]'s own
  enumeration clause for clause.
- *Conforming verifier*: I enumerated every verifier-detected register row
  (F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48,
  L49, T2, T4, T5, T26) and checked the checklist reaches all of them —
  coverage/slack and overlap (F33, L18), flag bits (F25, F26, F28, L46, L47,
  L49), F7, F36/L25, alignment and slab (L40, L41, L42), decoded content
  (T2, T4, T5, and T26 whose check "is T2's or T4's"), member ordering
  (F27, L48). Complete. It also correctly lists F1/F6 as checks *readers* are
  exempt from and verifiers are not.
- *Conforming updater*: its restatement of §20.3 step 4's permitted changes —
  "its names, a grown dimension extent, a planar channel list extended at its end
  or shortened from it (not both in one commit), a slab or alignment declaration
  declared, changed or cleared" — is a member-for-member match with step 4's own
  list, in the same order, with the same verbs, and with the same channel-list
  exception. I compared this three-way against §11.1's Rationale restatement
  (line 1660 ff.) as well; all three agree. A whitespace-normalised sweep
  confirms "declared, changed or cleared" occurs at exactly **three** sites, and
  "declared, changed or kept" at exactly **one** — §20.3's downstream clause at
  line 3326, where *kept* is the default the exception list correctly does not
  restate as an exception.
- The checklists disclaim being authorities ("each entry's authority is the
  requirement or section cited, never this summary"), so partial enumeration
  within an entry is not a broken promise.

**Appendix G, the reproducible-writer profile (10 items).** Numbering 1–10, in
order, no duplicates. I checked the load-bearing claims:

- Item 2's file_id derivation hashes [0, F−64) plus trailer[0,60) with file_id
  zeroed. file_id lies at trailer offset 40 with size 8, so it is inside [0,60) —
  the derivation is well-defined ✓. "Re-deriving it on an already-compact input
  would reproduce the input's own file_id" is correct: an idempotent compaction
  reproduces the same bytes and hence the same digest ✓. The 0x…0001 substitution
  is required because §6.2 forbids file_id = 0 ✓.
- Item 3's tie-break key is (type; then, for 0x0001, layer name; else header with
  extent_offset masked, inline payload, extent contents). Layer names are unique
  ([R-ENC-15]) so the 0x0001 tie always resolves ✓. The masked key covers type,
  flags, inline_length, extent_length, inline payload and extent contents — so
  "Two records this key does not separate are byte-identical in type, flags,
  lengths, payload and extent content" is exactly right, and swapping them
  therefore yields the same file ✓. The masking rationale (a key containing
  extent_offset would depend on its own result) is sound ✓.
- Item 3's "first structure begins at 16" is consistent with [R-CNT-13]'s
  extent_offset ≥ 16, [R-CNT-06]'s dir_offset ≥ 16, and §15.3's tile offset ≥ 16;
  and Appendix A's minimal file, whose only structure is the directory at 16,
  is the degenerate instance ✓.
- Item 5's identity claim: the shuffle is the identity exactly when s = 1 or
  n = L/s = 1. I verified it from the permutation itself: when s = 1 each group
  is one byte, so i = 0 always and the map i·n + j is j ↦ j; when n = 1 there is
  one group, so j = 0 always and the map is i ↦ i. Both are the identity, and
  neither holds otherwise ✓.
- The closing paragraph does not enumerate everything the items add (item 5's
  filter, tile extents and layout are missing from it), but it explicitly
  disclaims that role: "Read the numbered items as the list; this paragraph names
  what they are for, not how many there are." That disclaimer makes it not a
  broken promise.

**Appendix F, normative references.** I extracted every external reference cited
anywhere in the document — RFC 8878 (7), 1951 (5), 8259 (3), 1952 (3), 1950 (3),
9110 (2), 8174 (2), 3720 (2), 3339 (2), 2119 (2), plus BCP 14, IEEE 754, LZ4
Block, OCP OFP8, Unicode — and checked each against Appendix F. Every one is
listed, and every Appendix F entry cites a section that actually uses it. RFC
1950 and 1952 are correctly marked as wrappers codec 2 *excludes*, and T15's
instances name both with correct identifying bytes.

---

## 10. Suspicions I opened and closed

I record these because a clean lane has to show it looked.

1. **"All named constants appear once in Appendix B" (§4.7 Note).** I walked
   Appendix B's 25 rows against the constants defined across the document. Every
   constant I could name has a row. Candidates I thought might be missing —
   the record flag bit positions, the trailer flag lane boundaries, the
   user-metadata key length cap — are either in Appendix C (flag lanes) or
   covered by an existing row ("Name length … §4.6", which §18.2 folds onto keys).
   Closed: no omission I can defend.
2. **§10.2's "Two spaces carry no experimental range"** counts one space in the
   table (channel layout) and one not in it (the trailer's flag lanes). Closed by
   the sentence's own second half: "and the trailer's flag lanes, which §6.3
   partitions instead" — the exception is named where it arises.
3. **§17.2's Note citing "§14.2's worked examples give 18 and 30 bytes"** omits
   the planar 12 in the same Example block. Closed: it cites examples, not a
   complete set of §14.2's numbers, and 12 is likewise below 1 KiB so the Note's
   conclusion is unaffected either way.
4. **§22.3's "every byte a reader can reach belongs to one named structure"**
   against [R-CNT-02]'s "belongs to exactly one of: the front signature block;
   or a **structure**", where **structure** is a bolded defined term that
   excludes the front block (as Appendix G item 3 says outright: "the front
   signature block, which §5.2 counts as no structure"). Closed: "one named
   structure" admits a reading on which "named" does the work — a thing this
   specification names — under which the sentence is true, and no
   implementation behaviour turns on which reading is taken, since §9.7 has the
   walk claim the front block regardless.
5. **§20.3's shape (c) gloss** ("clearing a slab declaration, renaming a layer,
   or dropping a PE = 0 record") omits two operations that are equally confined
   to the directory: clearing an *alignment* declaration, and a grid-count-
   preserving extent growth, which §11.1's Rationale says "taken alone touches
   the directory alone". Closed: the Example's closed claim is that a commit
   takes one of **three** shapes, and it does — the growth case is shape (c).
   The per-shape glosses are appositions offering instances, not partitions, and
   (c) itself goes on to add further cases ("A re-declaration that leaves the
   index content unchanged is shape (c) too"). Nothing in the Example asserts
   its glosses are complete, so I have no sentence to quote as false.
6. **§21.6's Rule column uses co-equal comma-separated bracketed identifiers**,
   whereas one entry (zero layers) uses the register's "governing rule, then
   unbracketed parenthetical" form. Closed: §21.6's column is headed "Rule", not
   "Governing rule", and §21.1 extends only the *restatement* convention to
   §21.6's entries ("restate their governing rules on the same terms a row
   does"), not the citation typography.
7. **Whether a record header has the worked numeric example §4.7's Note
   promises** for "every non-obvious encoding". Closed: §7.4's Example gives the
   framing's field values numerically (type 0x0001, MU = 1, PE = 1,
   inline_length = 81, extent length 84), and a 24-byte fixed struct with a
   full layout table is not a non-obvious encoding.
8. **Whether §14.2's two-row table is complete.** Closed: §14.2 scopes itself to
   "a planar tile of a numeric channel … and … every interleaved tile", and
   [R-SER-07] routes the third case through §14.3 ("Whichever of §14.2 or §14.3
   defines a tile's decoded size").
9. **Whether the §15.3 table's six *structural* rows match the register's
   seven structural T-rows.** Closed and correct: table row 6 states two
   conditions (an overflowing sum, and a sum past F − 64), which the register
   individuates as T12 and T9 — exactly the per-condition individuation §21.1
   and [R-CNF-13] describe. The "Six rows are marked *structural*" count is
   right on the table's own terms.
10. **§15.2's Rationale's failure-mode claims.** I traced a zeroed region and an
    all-0xFF region through §15.3's table: zeroed → non-sentinel with length 0
    and offset < 16 (two structural rows), all-0xFF → sentinel offsets with
    crc ≠ 0 (T6). Both "loudly invalid" as claimed ✓.
11. **§23.1's "no commit turns a real position of a stored tile into padding".**
    I checked each permitted change: a growth only shrinks the padding set;
    a channel shortening removes whole tiles; names and slab/alignment
    declarations touch no position; a shrink is a rewrite. The claim holds ✓.

---

## 11. Result

**No findings.**

Every checksum the document prints, I recomputed from the printed bytes and it
matched. Every offset and width in every dump, I read out of the structure's own
layout table and cut out of the dump, and every field decoded to the value its
annotation claims. Every count the document states about itself — 35/49/26/10
register rows, 120 conditions, 277 instances, six structural rows, four residues,
five conformance classes, four extension vehicles, six design choices, thirteen
sample types, twelve numeric types, nine scalars, nine conditions in [R-CNT-06] —
I derived independently and it matched. Every numbered list is in order and
complete. Every constant is byte-identical across all of its restatements. Every
table that restates a rule stated in prose elsewhere agrees with that rule, and
the two tables whose citation grammar §21.1 specifies conform to it in all 120
rows. The one unlabelled — and therefore normative — blockquote agrees with the
requirement it renders.

I did not find a figure that illustrates a rule narrower or wider than the rule
is, a worked example that shows a case the prose forbids, or a checklist that
promises a set it does not deliver. The three multiply-restated closed lists in
the changed surface (§11.1's Rationale, §20.3 step 4, Appendix H) agree with each
other member for member and verb for verb.

I would not read this as evidence that nothing is wrong in the sixteen changed
passages — my instrument is arithmetic, byte layout and cross-table agreement,
and the defects this project's recent rounds have found are quantifier and scope
questions in prose, which that instrument is blind to. What I can say is that the
document's numbers are right.
