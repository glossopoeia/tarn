# Cleanroom round 34 — Diagram auditor — working transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,838 lines), in six overlapping chunks with `sed`/`Read`. I opened no other file
in the repository — no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`, `AGENTS.md`, `README.md`. I ran no `git` command, no web search, no
web fetch, and I did not list any directory to see what else exists. The
specification was where the brief said it would be.

Context I did not ask for **did** appear before I began: the runtime placed a
project instruction file (`CLAUDE.md`, which forwards to `AGENTS.md`), an index
of the maintainer's auto-memory notes whose titles name this project's harness
and prior-round machinery, and a `git status` snapshot with recent commit
subject lines. I did not open any file they name, and I have not used any of
their content as evidence. I flag it here as a disclosed appearance, per the
brief; I am not repeating what they said. The commit subject lines in
particular describe prior rounds' outcomes, and I have deliberately not let them
steer where I looked: my walk is charter-driven (enumerate every figure, then
recompute everything in it).

Files I wrote, all inside my own scratch directory
`/private/tmp/claude-501/.../r34-round/scratch/diagrams/`:

- `crc_diag.py` — my own CRC-32C implementation (reflected table, poly 0x82F63B78)
- `appA.py` — Appendix A dump parser + field decoder + trailer CRC
- `layerrec.py` — §7.4 layer-record payload reconstruction + index CRCs
- `count_inst.py` — mechanical register row/instance counter
- `examples.py` — consolidated arithmetic check of every worked example

and this transcript, at the single output path the brief names.

## 1. Method

Charter: every figure, diagram, byte-layout box, ASCII offset table, worked
example, and checklist, against the prose it illustrates. So: enumerate first,
judge second.

The document is hard-wrapped and blockquotes wrap with `> ` inserted, so every
phrase sweep I ran was over a whitespace-normalised, `> `-stripped copy of the
file built in Python, with a character→line map so hits report real line
numbers. I ran four **positive controls** first — phrases I had already read and
knew spanned a wrap — before trusting any zero:

| control phrase | hits |
|---|---|
| `pre-trailer pad` | 11 |
| `a slab or alignment declaration MAY be declared` | 1 (L3216) |
| `Only the directory is re-emitted` | 1 (L3389) |
| `each table giving the columns its structure needs` | 1 (L613) |

All four hit. A line-oriented `grep` returns 0 for the second and fourth.

## 2. Inventory

### 2.1 Labelled blocks (Note / Example / Rationale) — 62 blockquote blocks

Enumerated programmatically. Of the 62, exactly **one is unlabelled**:

- **L2186–2187, §15.1** — the index-region schematic
  `> [ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`

Under `[R-CNF-01]` the exemption is by label, not by the `>` marker, so **this
figure is normative text**. I checked it against `[R-CNT-17]`'s
`extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4` and against §15.4's
segment definition: it agrees exactly, and the "with no padding anywhere inside
the region" sentence directly under it is what makes the concatenation
unambiguous. Clean.

All other blockquotes carry a Note/Example/Rationale label and are therefore
non-normative. That mattered twice below (§4.7's presentation Note; §11.1's
Rationale).

### 2.2 Tables — 25

| lines | table |
|---|---|
| 127–147 | §2.2 requirement prefixes (19) |
| 304–310 | §2.4 outcome classes (5) |
| 785–788 | §6.1 front signature block layout |
| 828–839 | §6.2 trailer layout (10 fields) |
| 1003–1009 | §7.2 record header layout (5 fields) |
| 1079–1082 | §7.3 record types (2) |
| 1108–1125 | §7.4 layer-record inline payload (16 rows) |
| 1226–1234 | §8.1 checksum coverage map (7) |
| 1570–1579 | §10.2 numeric identifier spaces (8) |
| 1784–1798 | §12.1 sample types (13) |
| 2018–2021 | §14.2 decoded size / offset of value k (2) |
| 2191–2195 | §15.1 index entry layout (3 fields) |
| 2239–2251 | §15.3 entry validity (11 rows) |
| 2638–2640 | §18.2 user-metadata encoding byte (1 field) |
| 2841–2848 | §18.4 standardized keys (6) |
| 3437–3441 | §20.4 updater obligations by governing flags (3) |
| 3729–3765 | §21.2 file-scope register (35 rows) |
| 3778–3828 | §21.3 layer-scope register (49 rows) |
| 3838–3865 | §21.4 tile-scope register (26 rows) |
| 3888–3899 | §21.5 ignored-record register (10 rows) |
| 3908–3924 | §21.6 non-violations (15 rows) |
| 4039–4048 | §21.9 minimum guarantees (8 rows) |
| 4426–4441 | Appendix A annotation table (14 rows) |
| 4461–4489 | Appendix B constants (27 rows) |
| 4559–4561 | Appendix E changelog (1 row) |

### 2.3 ASCII figures — 6

- L664–669 §5.1 a file after three commits
- L1328–1337 §9.2 what a crash sees
- L2186–2187 §15.1 index region (the normative one)
- L3359–3363 / L3375–3379 / L3402–3405 §20.3 the three shapes a commit takes
- L3576–3582 §20.5 what compaction reclaims
- L4415–4424 Appendix A hex dump

### 2.4 Worked numeric examples — 17

§4.6 name bytes · §5.1 smallest file · §7.4 complete layer-record payload ·
§11.2 grid · §11.4 ordinals · §12.1 bfloat16 · §12.3 channel entry ·
§13.3 fill tuples · §14.2 byte layout · §14.3 packed bool · §14.5 padding ·
§15.4 (two) · §16.2 slab runs · §17.3 byte-shuffle · §20.3 supersede cost ·
Appendix A.

### 2.5 Numbered lists / checklists — 6

§9.2 commit protocol (6 steps) · §10.1 four extension vehicles ·
§19.1 open (4 steps) · §20.3 append (6 steps) · Appendix G profile (10 items) ·
Appendix H conformance checklists (5 classes).

## 3. Checksums — recomputed, never read

I wrote CRC-32C myself (reflected polynomial 0x82F63B78 = reflection of the
0x1EDC6F41 §4.5 names, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and validated it
against §4.5's own check vector *before* using it anywhere:

```
CRC32C("123456789") = 0xE3069283, stored 83 92 06 E3   — §4.5 agrees
CRC32C(zero bytes)  = 0x00000000                        — §4.5 agrees
```

Then every stated checksum in the document:

| where | document states | I computed | verdict |
|---|---|---|---|
| §4.5 / App B check vector | 0xE3069283 | 0xE3069283 | match |
| §4.5 / App B zero bytes | 0x00000000 | 0x00000000 | match |
| §7.4 example, segment CRC over the 80-byte all-sentinel entry array | 0x80A34955 (`55 49 A3 80`) | 0x80A34955 | match |
| §7.4 example, crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E (`2E 98 EE C4`) | 0xC4EE982E | match |
| §15.4 / App B, CRC of 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 | match |
| Appendix A trailer CRC over trailer[0,60) | 0x402F157E (`7E 15 2F 40`) | 0x402F157E | match |
| Appendix A directory region [16,20) | 0x00000000 | 0x00000000 | match |

The §7.4 chain is worth naming because it is two-deep: the segment CRC is taken
over 80 bytes of `FF×16 00×4` repeated four times, and `crc_of_crc_array` is
then taken over the *little-endian stored form* of that CRC — I confirmed the
document means the stored bytes and not the integer, because computing over
`80 A3 49 55` (big-endian) gives a different value, and only the little-endian
input reproduces 0xC4EE982E. That is consistent with `[R-CNT-19]`'s "All
checksums are CRC-32C over bytes exactly as stored."

No checksum in this document is wrong.

## 4. Appendix A, byte by byte

I parsed the hex dump programmatically (asserting each row's stated offset
against the running length, so a dropped or added byte would have thrown), then
cut every trailer field out at the offset and width §6.2's *layout table* gives
— not at the offsets Appendix A's annotation table gives — and compared the
decode against both the annotation and every other place in the document that
states the same constant.

```
file length 128                                  — §5.1, [R-CNT-27], App B all say 128
[0,8)    89 54 41 52 4E 0D 0A 1A                 — §6.1 table row 0, App B
[8,16)   00 ×8                                   — §6.1 table row 8 ("zero")
[16,20)  00 00 00 00 = CRC-32C of zero bytes     — §7.1, §4.5
[20,64)  44 bytes zero                           — pad = 64 − 20, [R-LIF-02] step 5
trailer at 64 (F mod 64 = 0)                     — §6.2
 +0  (file 64..72)  8A 4E 52 41 54 0D 0A 1A      — §6.2 table, App B, [R-CNT-24]
 +8  (72..74)  01 00        version_major = 1
 +10 (74..76)  00 00        version_minor = 0    — the one descriptive field, §4.7
 +12 (76..80)  00 00 00 00  flags = 0            — [R-CNT-08] creator writes 0
 +16 (80..88)  dir_offset = 16                   — ≥ 16 ✓
 +24 (88..96)  dir_length = 4                    — ≥ 4 ✓; 16+4 = 20 ≤ F−64 = 64 ✓
 +32 (96..104) committed_file_length = 128       — = F, multiple of 64 ✓
 +40 (104..112) file_id = 0x0123456789ABCDEF     — ≠ 0 ✓; LE bytes EF CD AB 89 67 45 23 01 ✓
 +48 (112..124) 12 zero bytes                    — reserved ✓
 +60 (124..128) 7E 15 2F 40 = 0x402F157E         — recomputed: match
```

Every field offset in Appendix A's annotation table equals 64 + the §6.2 layout
table's offset. The 44-byte pad is exactly `64 − (dir_offset + dir_length)`, as
`[R-LIF-02]` step 5 forces. The prose "112 bytes covering [16, 128) contains the
directory" is `128 − 16 = 112`. Appendix A is clean, dump and annotation table
alike.

## 5. §7.4's layer-record example, byte by byte

I reconstructed the 81-byte payload from the field semantics (not by copying the
dump) and compared it against the dump's own offsets:

```
 0 03 73 73 74            name len 3 "sst"        4 bytes  → next 4
 4 01                     layout 1                1        → 5
 5 01 00                  linearization 1 (u16)   2        → 7
 7 01 00                  codec 1 (u16)           2        → 9
 9 01 00                  filter 1 (u16)          2        → 11
11 00×8                   A = 0 (u64)             8        → 19
19 00×8                   S = 0 (u64)             8        → 27
27 00×8                   A_slab = 0 (u64)        8        → 35
35 01                     rank 1 (u8)             1        → 36
36 01 00                  C = 1 (u16)             2        → 38
38 01 78                  dim name len 1 "x"      2        → 40
40 64 00 …                extent 100 (u64)        8        → 48
48 20 00 …                tile extent 32 (u64)    8        → 56
56 04 74 65 6D 70 0C 00   chan "temp", type 12    7        → 63
63 04 00 00 C0 7F         fill len 4, 0x7FC00000  5        → 68
68 01                     index_encoding 1        1        → 69
69 04 00 …                entry_count 4 (u64)     8        → 77
77 2E 98 EE C4            crc_of_crc_array        4        → 81
```

Every printed offset is the running sum of the widths §7.4's own table implies.
The prose accounting checks: name 4 + nine scalars 34 = 38; dimension entry
2+8+8 = 18; channel entry 5+2+5 = 12; trailing 1+8+4 = 13; 38+18+12+13 = **81**,
matching the stated inline_length and leaving an empty sub-record sequence.

Cross-checks against the rest of the document:
- The 12 channel bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F` are byte-for-byte
  §12.3's example — the §7.4 example claims "§12.3's `temp` entry, byte for
  byte", and it is.
- Grid count ⌈100/32⌉ = 4 (§11.2), entry_count = 4, interleaved so addressed-tile
  count = N = 4 (`[R-CNT-17]`, §11.2). ✓
- Extent length 4×20 + ⌈4/2¹⁶⌉×4 = 84, which the example states. ✓
- Entry array 4×20 = 80 bytes; one segment; 4-byte CRC array. ✓
- Fill length 4 = float32 element size (`[R-CNT-23]`, §12.1 table). ✓
- `0x7FC00000` is the same quiet NaN §12.3 and §12.1 use. ✓

Clean.

## 6. Every other worked example — recomputed

Consolidated in `examples.py`; **69 checks, 0 failures**. The ones worth naming:

- §11.2: G = (⌈1024/256⌉, ⌈2048/256⌉) = (4,8); N = 32; P = 65,536;
  ⌈1000/256⌉ = 4. ✓
- §11.4: s(1,2) = 1·8+2 = 10; in-tile (44,188); ordinal 44·256+188 = 11,452;
  planar disk ordinal 2·32+10 = 74. ✓ (I checked the ordinal formulas
  Σ tᵢ·∏_{j>i}Gⱼ and Σ uᵢ·∏_{j>i}Tⱼ reduce correctly at d = 2.)
- §12.1: `struct.pack` gives binary32 1.0 = 0x3F800000; high 16 bits = 0x3F80;
  stored `80 3F`. ✓
- §14.2: Q = 1+2 = 3, decoded 18, ordinal 5 at [15,18); planar b = 12 bytes,
  ordinal 5 at [10,12); Q = 4+1 = 5, decoded 30, ordinal 5 at [25,30) with `t`
  at 25–28 and `m` at 29. I also verified the closing identity — channel c at
  in-tile ordinal u sits at u·Q + Fᶜ, which is the table's
  (k div C)·Q + F_{k mod C} with k = u·C + c, since k div C = u and k mod C = c
  for 0 ≤ c < C. ✓
- §14.3: I bit-packed the alternating sequence myself. Byte 0 = 0x55, byte 1 =
  0x01, and with the pad bits (positions P mod 8 = 2 through 7) set to a true
  fill, byte 1 = 0x01 | 0xFC = 0xFD, giving `55 FD`. ✓
- §14.5: grid ⌈5/4⌉² = 2×2; tile (1,1) covers 4–7 on both axes; I counted the
  positions with both coordinates < 5 and got exactly 1 real and 15 padding;
  decoded 16·2 = 32; fill 0xABCD little-endian = `CD AB`. ✓
- §15.4 first: ⌈10⁶/2¹⁶⌉ = 16 segments, 15 full, last 16,960; CRC array 64
  bytes; region 20,000,064; k = 999,999 in segment 15 at relative byte
  20·16,959 = 339,180; array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000). Full segment = 2¹⁶·20 = 1,310,720 = exactly 1.25
  MiB. The "~339 KB" is (16,960·20 + 64) = 339,264. ✓
- §15.4 second: 20·74 = [1,480, 1,500); channel-3 block [96,128) = 32 entries. ✓
- §16.2: runs [0,8),[8,16),[16,24),[24,32) under S = 8, N = 32. Under row-major
  each is one tile row, and tile rows 1–2 are ordinals 8–23 = runs 1 and 2. ✓
- §17.3: I implemented the permutation "byte i of group j at offset i·n + j"
  and applied it to `00 00 80 3F 00 00 00 40 00 00 40 40` (s = 4, n = 3),
  getting `00 00 00 00 00 00 80 00 40 3F 40 40` — the printed value, and the
  prose gloss ("then `80 00 40`, then `3F 40 40`") is right too. ✓
- §20.3: 32·20 + 4 = 644. §20.3's Note: 10⁶·20 ≈ 20 MB. ✓
- §21.9's Note: segment-CRC array at 2³² entries = 2¹⁶·4 = 256 KiB; at 2³⁶ =
  2²⁰·4 = 4 MiB; 65,536 × 200 B = exactly 12.5 MiB. `[R-VEC-03]`'s "tens of
  gigabytes" for a 2³²-entry index = 2³²·20 ≈ 86 GB. ✓

Every printed constant: 0x1EDC6F41 (Castagnoli), 0xFD2FB528 / `28 B5 2F FD`
(zstd frame magic — correct little-endian), `04 22 4D 18` (LZ4 frame magic in
T23 — correct), `1F 8B` (gzip in T15 — correct), 0x7E000000 (the LZ4 block
format's practical input bound — correct), 0x7FC00000 / 0x7FC0, 0x3F800000 /
0x3F80, 0xABCD → `CD AB`, `FF×16 00×4`, 0x0123456789ABCDEF → `EF CD AB 89 67 45
23 01`. All correct.

## 7. The register as a set of tables

### 7.1 Row and instance counts, derived mechanically

§21.1 makes the instance count mechanical: semicolon-separated items in the
Instances cell, a cell reading `—` counting as one. I parsed all four register
tables and counted:

| section | rows found | header claims | instances |
|---|---|---|---|
| §21.2 | 35 (F1–F36, F11 struck) | 35 | 56 |
| §21.3 | 49 (L1–L49) | 49 | 116 |
| §21.4 | 26 (T1–T26) | 26 | 55 |
| §21.5 | 10 (R1–R10) | 10 | 50 |
| total | **120** | — | **277** |

§21.8 states "120 conditions over 277 instances". Both figures reproduce
exactly. F11's absence is deliberate and the Note at L3767 says so.

I spot-audited the instance arithmetic against §21.1's two stated axes (layout
formulas are materially different shapes; a magnitude comparison with no
direction bound enumerates both directions; an "exceeds" enumerates one):

- T3 = 3 layouts × 2 directions = 6 ✓; T14 = 6 ✓; T22 = 6 ✓ (all "differs
  from"/"does not equal"); T21 = 3 ("larger than", one direction) ✓;
  L44 = 3 ("exceeds") ✓.
- L21 = 2 layouts × 2 directions = 4 ✓; L22 = 2 directions + 2 stated
  alternatives = 4 ✓; L30 = 2 directions ✓.
- L2's nine derived quantities: I checked the two dominance claims. `C·N`
  dominates the max disk ordinal `(C−1)N + (N−1) = CN − 1` ✓. `P·Q` dominates
  `V = P·C` because Q = ΣBᵢ ≥ C, every element size being ≥ 1 ✓. And I checked
  why packed-bool `⌈P/8⌉` needs no instance: it is ≤ P, which is already
  enumerated, so no file could differ.
- R4 = 8 frame constraints × 2 containers = 16 ✓, and the 8 are exactly what
  §18.2 carries over from `[R-COD-06]` (magic, skippable, second frame, nonzero
  dict ID, content-checksum flag) plus §18.2's own two (bytes after the frame;
  content-size larger / smaller) — with the two §18.2 says fall outside the
  register (undisclosed dictionary use, the buffer-sizing bar) correctly absent.

### 7.2 Cross-reference integrity

- Every one of the 19 prefixes §2.2 tabulates is used; every prefix used is
  tabulated; neither set has a member the other lacks.
- Requirement numbering has no gaps in any prefix (CNF 1–13, CNT 1–27, COD 1–11,
  ENC 1–16 plus the illustrative `[R-ENC-100]` in §2.2 itself, ERR 1–5, EXT 1–5,
  GEO 1–6, IDX 1–5, LIF 1–8, MDL 1–2, MTA 1–10, PRV 1–5, RDR 1–4, SEC 1–7,
  SER 1–9 including the withdrawn SER-4 which §14.4's Note retires by name,
  SLB 1–5, TYP 1–10, VEC 1–4, WRT 1–9).
- 67 distinct requirement identifiers appear in Governing rule cells; every one
  is defined somewhere in the document with its bracketed marker.
- §21.1 says a Governing rule cell cites a bare section only "where no
  requirement identifier does, a value set (L31) or a registered type's scope
  (L26)". I swept all 120 cells for `§`: **exactly two hits, L26 and L31**. The
  claim is precisely true.
- §21.1's specialization list — F1's front-block instance of F6, F1's
  trailer-magic instance of F8, F35 of F36, L24 of L25, F21 of F22, L10 of L11 —
  I checked each: every file exhibiting the narrower row's condition necessarily
  exhibits the wider one. F21 ⊂ F22 works because slot (0,0) means
  extent_length = 0 < 5.
- F33's cross-reference net — "caught by the bounds rows F9/F10, F30/F31/F32,
  L15/L16/L17 and T8/T9 … the half-zero rows F30 and L15 among them" — I
  checked all ten labels against their rows. Every one denotes what F33 says,
  and between them they cover the directory, top-level record extents, layer and
  sub-record extents, and stored-tile extents at both ends of the file.
- §20.5's claim "one row for each of the other seven spaces §10.2 tabulates
  (L31, L33, L34, L36, L43, L45, R1)": §10.2 tabulates 8 spaces, so "the other
  seven" excludes record type (F36, L25). Mapping: layout→L36, linearization→L33,
  sample type→L34, codec→L43, filter→L45, index encoding→L31, metadata
  encoding→R1. Seven, all present, none duplicated.
- §21.2's reach derivation — "F8, F14, F6 and both of F1's instances … and no
  other row" — is exactly the set of rows asserting an invariant `[R-CNT-24]`
  fixes (trailer magic, trailer CRC, front block, and F1's two byte-reversal
  instances of those). §2.3's Note's three worked cases (F14 reaches, F5 does
  not, F15 does not) are consistent with it; F15's Governing cell does cite
  `R-CNT-24` parenthetically, as the Note says.
- `[R-CNF-13]`'s "`[R-CNT-06]` states nine". I counted `[R-CNT-06]`'s own
  conditions: magic, trailer CRC, CFL = file size, CFL multiple of 64,
  dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length ≤ F−64, file_id ≠ 0,
  reserved zero = **nine**, with the version and flag gates belonging to §6.3.
  And exactly nine register rows carry `[R-CNT-06]` as their governing rule:
  F8, F14, F17, F13, F9, F16, F10, F12, F15. Two of the nine (magic, CRC) reach
  a foreign major and seven do not — the split `[R-CNF-13]` states.

### 7.3 §15.3's entry-validity table against `[R-IDX-03]`

`[R-IDX-03]` says "Six rows are marked *structural*". I counted the table's
`*structural*` markers: sentinel-with-crc≠0; exactly-one-half-sentinel;
length = 0; offset < 16; offset or length > 2⁶³−1; overflow-or-past-F−64.
**Six.** The remaining five rows are the valid sentinel, the crc failure (whose
extent the prose expressly keeps standing), and three *verifier* rows.

Every structural row has its §21.4 row: T6, T7, T10, T8, T11, and T12+T9 (the
table's sixth row splits into two register conditions, which §21.1's
individuation licenses). The crc row is T1. The verifier rows are L18, F33, and
L40/L41/L42. Nothing in the table lacks a row and no row lacks a table line.

I also checked the §15.2 Rationale's two failure-mode claims against the table:
a zeroed region parses as offset 0 / length 0 and is caught (by both the
length = 0 and the offset < 16 rows), and an all-0xFF region is caught because a
sentinel's crc must be 0 while 0xFFFFFFFF is not. Both correct.

### 7.4 §8.1's coverage map against §4.5

§4.5 names three *terminal* checksum fields covered by nothing further (trailer,
directory-region, user-metadata) and three *interior* ones both
comparison-verified and covered once more (segment CRC array, entry crc,
crc_of_crc_array). The map's seven rows deliver exactly that: the trailer,
directory and user-metadata rows put the checksum at the tail of their own
structure; the tile-index row names the segment CRC array *and* says it is
itself covered by crc_of_crc_array; the stored-tile row names the entry crc;
and crc_of_crc_array, being a field of the layer record, falls under the
directory row's "the preceding dir_length − 4 bytes". The two "none" rows are
the equality-checked front block and the unassigned-type extent, both of which
§4.5 excepts by name. Consistent.

### 7.5 §10.2 and Appendix C against the defining sections

I read every space's defining rule and compared:

| space | defining rule says | §10.2 says |
|---|---|---|
| record type | 0x0001, 0x0002 assigned; rest unassigned | 0x0003–0x7FFF res, ≥0x8000 exp ✓ |
| channel layout | 1,2; 3–255 reserved without semantics | 3–255 res, no exp ✓ |
| linearization | 1; 2–3 reserved w/o semantics; 4–0x7FFF future | 2–0x7FFF res ✓ |
| sample type | 1–13; 14–19 w/o semantics; 20–0x7FFF future | 14–0x7FFF res ✓ |
| codec | 1–4; 5–0x7FFF future | 5–0x7FFF res ✓ |
| filter | 1,2; 3–0x7FFF future | 3–0x7FFF res ✓ |
| index encoding | 1; 2–0x7F res; ≥0x80 exp | same ✓ |
| metadata encoding | 1,2; 3–0x7F res; ≥0x80 exp | same ✓ |

Appendix C's snapshot restates all eight plus the record types, the standardized
keys and the flag lanes; every entry matches, including §12.2's pinned
reservations (14/15 OCP OFP8 E4M3/E5M2, 16/17/18 int128/uint128/float128, 19 a
fixed-size raw-bytes type, which C calls "opaque").

### 7.6 Appendix B against the sections it cites

All 27 rows checked against the defining section. Every constant, every bound,
every recommended value agrees. The three checksum constants I recomputed. The
"Reader minimum guarantees" row lists eight quantities and §21.9's table has
eight rows, in the same order.

### 7.7 §21.6 against its rules

All 15 rows read against their governing requirements. Each is faithful. Two
worth naming because they are easy to get wrong and are not:

- The slack row correctly carries `[R-CNT-21]`'s partial-total qualifier
  ("an upper bound naming what stopped the walk").
- The trailer-mimic row's "§9.6's second caution covers the rest" is right:
  `[R-LIF-06]` states two cautions, the first being the mimic and re-verification,
  the second being rollback — and a mimic that survives whole-file
  re-verification is exactly a rollback.

The closing paragraphs' two "conforming files a reader nevertheless refuses"
and their registered neighbours (F18; F35/F36/L24/L25) are correctly paired.

## 8. Appendix H — the five checklists

Every line audited against the requirement or section it cites.

- **File**: four claims, all correct. Its illustration ("an experimental-range
  MU = 0 record being conforming") is one instance of §21.6's defined
  conditions, offered as an instance and not as the class.
- **Reader**: the enumeration "all four codecs, both filters, both layouts, all
  thirteen sample types, both user-metadata encodings, and both registered
  record types" — I checked each count against its section: codecs 1–4 all core
  (§17.2), filters 1–2 both core (§17.3), layouts 1–2 (§14.1), thirteen sample
  types all core (§12.1), metadata encodings 1–2 both core (§18.2), record
  types 2 (§7.3). Every count is right. The acceptance clause reproduces
  `[R-CNF-03]`'s three qualifiers (major implemented; no top-level MU = 1 of an
  unimplemented type; within §21.9) correctly.
- **Writer**: eight obligations plus the `[R-CNT-03]` advisory correctly marked
  "Advisory, and not a conformance condition". The compactor carve-out on
  flags = 0 is present.
- **Updater**: the §20.3 step-4 restatement carries all four permitted changes,
  including the slab/alignment declaration's four verbs "declared, changed,
  re-established or cleared" and the channel-list "not both in one commit"
  exception, and defers with "only as §20.3 step 4 permits". Faithful. It omits
  `[R-WRT-03]`'s index-chain-for-reused-segments clause, but the checklist's own
  preamble ("each entry's authority is the requirement or section cited, never
  this summary") licenses a summary.
- **Verifier**: eleven obligations, all traceable. The `[R-CNT-04]` residency
  asymmetry is correctly stated ("which `[R-CNT-04]` lets a reader not holding
  it resident defer or omit and §2.3 does not").

I also checked §11.1's Rationale, which restates the same closed list from the
other end, and Appendix H against it: both carry all four verbs, both carry the
"one or the other in a commit" channel-list exception, both carry the
"a layer the commit itself empties does not qualify" tense clause. The three
restatements (§11.1 Rationale, §20.3 step 4, Appendix H) agree with one another.

## 9. Appendix G — the profile's ten items

Item-by-item against the rules each closes:

- Item 2's `file_id` derivation is self-consistent: it hashes [0, F−64) plus the
  trailer's first 60 bytes with the file_id field zeroed. file_id sits at trailer
  offset 40..48, inside [0,60), and the trailer CRC at [60,64) is excluded — which
  it must be, since the CRC depends on file_id. The 0x…01 substitution matches
  §6.2's `file_id ≠ 0`.
- Item 3's "The first structure begins at 16 … which §5.2 counts as no structure"
  is correct: `[R-CNT-02]` makes the front signature block its own coverage
  class, distinct from "a structure".
- Item 5's identity claim I verified against `[R-COD-10]`'s permutation
  "byte i of group j at offset i·n + j": at s = 1 each group is one byte and
  the map is j ↦ j; at n = 1 it is i ↦ i. Both are the identity, and those are
  the only two cases. Correct.
- The closing paragraph names a purpose for each of the ten numbered items
  (item 1 and 9 by number, item 8 by number, the rest by content). I traced all
  ten and each is named. It under-names item 5, which closes four degrees of
  freedom (alignment/slab, filter, tile extents, layout) and is summarised by
  one; but the paragraph explicitly disclaims being the list ("Read the numbered
  items as the list; this paragraph names what they are for, not how many there
  are"), so I did not treat it as a defect. Recorded as a rejected candidate.

## 10. Appendix F — normative references

Appendix F carries no "non-normative" marker (every other appendix that is
non-normative says so in its heading: A, B, C, D, E, G, H). Under `[R-CNF-01]`
it is therefore **normative**, which matters because `[R-COD-07]` delegates to
it ("Appendix F pins the exact revision") for the LZ4 block format.

I swept the body for RFC citations: RFC 1950 ×3, 1951 ×5, 1952 ×3, 2119 ×2,
3339 ×2, 3720 ×2, 8174 ×2, 8259 ×3, 8878 ×7. Every one appears in Appendix F,
with the §-references matching where it is used. IEEE 754-2019 is cited for both
uses the body makes of it (§12.1's interchange formats and §18.2's
decimal→binary64 conversion under roundTiesToEven). The OCP OFP8 reference is
correctly marked informative, matching §12.2's Note. Nothing cited normatively
in the body is missing, and nothing listed is unused.

## 11. Findings

### diagrams-01 — §20.3's "three shapes" figure puts free re-declaration of an empty layer under "Only the directory is re-emitted" (AMBIGUITY)

§20.3, the Example beginning "**Example — the three shapes a commit takes.**",
shape (c) at lines 3386–3400:

> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, or dropping a PE = 0 record where
> §20.4 licenses the drop, any extent it owned becoming slack, a run
> the figure below does not draw. Only the directory is re-emitted. A
> change to any fixed declaration of a layer that **stored** a tile in
> the generation the commit supersedes — a fill value, a type, a tile
> extent — is not an appender's operation at all (step 4): it would
> reinterpret or invalidate every stored tile it reaches. A layer that
> stored no tile in the
> generation the commit supersedes is re-declared freely, subject to
> every rule its new declarations are subject to, which is the same step's
> permission — a layer the commit itself empties does not qualify. Editing
> user metadata is not this shape:
> its document lives in an extent (`[R-CNT-25]`), so a new extent is
> appended and the old one becomes slack, as in (b).

The block is a taxonomy — "the three shapes a commit takes" — and (c)'s heading
plus "Only the directory is re-emitted" state its shape. Three sentences follow.
Two of them are explicitly marked as *not* this shape ("is not an appender's
operation at all"; "is not this shape"). The third — free re-declaration of a
layer that stored no tile — carries no such marking and sits between them.

**Reading A**: the re-declaration sentence is a permission note, saying nothing
about which shape such a commit takes.
**Reading B**: it is inside (c), so a free re-declaration is a change confined to
the directory and only the directory is re-emitted.

Reading B is wrong, and the surrounding normative text says so. "Stores no tile"
is not "addresses no tile": a layer with extents (100,) and tile extent 32
addresses four tiles, has entry_count = 4, an 84-byte index region and four
sentinel entries, and stores nothing. A commit may re-declare it freely — change
its tile extent to 16, say — and then ⌈100/16⌉ = 7, entry_count and
extent_length change with it, and §20.3 step 4's own clause bites: "Every layer
whose stored-tile set or **index content** this commit changes has its
tile-index region re-emitted in full … necessarily at a new placement". That is
shape (b)'s cost, not (c)'s. §11.1's Rationale is careful about exactly this
distinction for the adjacent case of growth ("A growth that changes no grid
count ⌈Eᵢ / Tᵢ⌉ … taken alone touches the directory alone … Any other growth
changes the index content — entry_count and extent_length with it — so the
layer's whole tile-index region is re-emitted"); shape (c) is not.

I pick Reading A, because §20.3 step 4's re-emission clause is unconditional and
`[R-CNT-17]` ties extent_length to entry_count, so the figure cannot license
what the step forbids. An implementer who builds an appender from the figure
rather than the step, though, would fail to re-emit an index region it owes —
and the figure is where a reader goes for "what does a commit look like".

Related and smaller: "the three shapes a commit takes" is a completeness claim,
and this commit — a re-declared empty layer, index re-emitted, no tile added —
fits (b)'s picture (which draws "+tiles") no better than (c)'s.

**Not byte-level.** Step 4's re-emission clause is unconditional and states the
obligation; the figure is a labelled Example and therefore non-normative under
`[R-CNF-01]`. Two implementations reading the whole of step 4 cannot disagree
about the bytes a re-declaring commit must append.

### diagrams-02 — §4.7's presentation Note does not describe the tables it governs (OBSERVATION)

§4.7, the Note at lines 611–616:

> **Note.** Layout tables for fixed-layout structures give, per field:
> byte offset within the structure, size, type, name, taxonomy class,
> and valid range, each table giving the columns its structure needs.
> A packed variable-length payload — the layer
> record's inline payload (§7.4) — has no fixed offsets to give; its
> table omits the offset, size and class columns … §6.1's block is a 16-byte
> constant, where a Value column replaces type and range, and §7.2
> folds each field's range into its Field cell.

Six per-field columns are named and three tables get explicit carve-outs. Held
against the tables:

- **§6.1** (line 785) delivers `| Offset | Size | Value | Class |`. The carve-out
  says the Value column "replaces type and range" — which leaves offset, size,
  **name** and class standing. There is no name/Field column. No carve-out
  licenses that omission, and the document does name these fields elsewhere:
  F6's Instances cell calls them "magic bytes [0,8); reserved bytes [8,16)" and
  Appendix A's annotation table calls them "front signature magic" and "front
  signature reserved".
- **§7.2** (line 1003) is said to fold "each field's range into its Field cell".
  Of five fields, two do (`type (0 invalid)`; `flags: bit 0 …, bits 2–15
  reserved`) and three do not (`inline_length`, `extent_offset`,
  `extent_length`). The constraints on those three live in the prose below
  (`[R-CNT-12]`, `[R-CNT-13]`) — which is fine as engineering, but is not what
  the Note says, and §6.2's table shows the document is willing to put
  cross-field constraints in a range column ("dir_offset + dir_length ≤ F − 64").

The escape hatch is "each table giving the columns its structure needs", which
can be read as licensing any omission from the six. But then the two
omission-describing carve-outs (§7.4's "omits the offset, size and class
columns", §6.1's "replaces type and range") would be unnecessary, and the Note's
practice is to say when a listed column is dropped. Under that reading §6.1's
missing name column and §7.2's two-of-five folding are both unaccounted for.

**Not byte-level.** The Note is labelled and therefore non-normative
(`[R-CNF-01]`); which columns a table prints changes no byte and no verdict, and
the field names and ranges are all stated normatively elsewhere.

### diagrams-03 — §18.2's layout table gives a Valid-values cell narrower than the field's conforming value set (OBSERVATION)

§18.2, lines 2638–2640:

> | Offset | Size | Type | Field | Class | Valid values |
> |---|---|---|---|---|---|
> | 0 | 1 | u8 | encoding | structural | 1 or 2; see below |

The Valid-values column elsewhere carries conformance constraints — §6.2's
trailer gives "≥ 16", "≥ 4; dir_offset + dir_length ≤ F − 64", "≠ 0", "zero" —
so read as "the values a conforming file may carry", "1 or 2" excludes the
experimental range. It should not. §21.6 records:

> | A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's conduct, not the bytes …

and `[R-EXT-03]` is explicit that for this space the outcome is "ignore-record
under the quarantine (`[R-CNT-25]`), **never a scope-level rejection**". A
validator built from the cell alone would reject at the record's containing
scope a file this specification calls conforming.

The mitigation is real and in the cell: "; see below", and the paragraph
immediately below gives the whole value set. Compare the sibling cells that do
not defer — §7.4's index_encoding row spells out that "the experimental range
≥ 0x80 (§10) — is a validity error at layer scope", which for *that* space is
correct. The two u8 spaces with an experimental range are handled by opposite
conventions, and only one of them says which convention applies.

The near-parallel I considered and rejected as an excuse: §6.2's version_major
cell reads "1 (0 invalid; others: §6.3)" while a file declaring major 2 is not
nonconforming either. But there every reader under this text does reject that
file (`[R-CNT-07]`), so "1" describes what this text's reader accepts; here the
reader accepts the file and ignores one record.

**Not byte-level.** The cell defers explicitly to prose immediately below it,
and that prose plus `[R-EXT-03]` plus §21.6 decide the question with one voice;
no register row makes an experimental encoding a violation. An implementation
that read the paragraph under the table cannot diverge.

### diagrams-04 — F5's Condition cell puts the pre-trailer pad in a floor derivation that excludes it (OBSERVATION)

§21.2, row F5 (line 3735):

> | F5 | File size is below the 128-byte minimum, so the front block, directory, pre-trailer pad and trailer cannot all fit | F (physical file size); committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06) |

Its governing rule derives the floor from three components, not four
(§5.1, `[R-CNT-27]`):

> No conforming file is shorter than 128 bytes: the front signature
> block, a directory of at least 4 bytes at an offset of at least 16,
> and the 64-byte trailer at a 64-aligned offset cannot be satisfied in
> fewer.

The pad is not among them, and it is not a component a conforming minimal file
must contain. `[R-CNT-05]` says so directly — "a writer that ends its directory
on a 64-byte boundary leaves none" — and I constructed the witness: F = 128,
dir_offset = 16, dir_length = 48, so the directory occupies [16, 64) and the
trailer [64, 128) with **zero** pre-trailer pad. The 48-byte region holds a
44-byte record sequence plus its 4-byte CRC, and 44 = one 24-byte record header
plus a 20-byte inline payload — an experimental-range MU = 0 record with extent
slot (0,0), which §21.6 records as conforming. `dir_offset + dir_length = 64 =
F − 64` satisfies `[R-CNT-06]`. So a conforming 128-byte file with no pad
exists, and the pad cannot be part of what "cannot all fit".

§21.1 governs this exactly: "each row *restates* its governing rule, and where a
row and the rule it cites diverge, **the rule governs**." The divergence here is
confined to the row's reason clause; the condition, outcome, detector, tier and
instances are all right. It is a stale-restatement defect of the class the
completeness clause exists to catch, at the smallest scale.

The counter-reading I weighed and am reporting alongside it: a pre-trailer pad
of length zero is trivially "present", so naming it among the components costs
nothing arithmetically. I still report the row because a floor derivation is
read as a list of minimum sizes, and the only other place this document lists
the floor's components — `[R-CNT-27]` itself — names three, while §5.1's Example
and Appendix A name a pad only because their particular empty-directory file has
a 44-byte one.

**Not byte-level.** The condition F5 tests (file size < 128) is identical to
`[R-CNT-27]`'s, the outcome (reject-file) and detector (reader, at open) are
identical, and §21.1 makes the rule govern the reason clause. No file changes
sides.

## 12. Suspicions opened and closed

- **Appendix A's dump vs its annotation table.** Cut every field at the §6.2
  layout table's offsets, decoded, compared. All fourteen annotation rows agree
  with the dump and with §6.1/§6.2/App B/`[R-CNT-24]`. Closed by computation.
- **The three printed CRCs and two check-vector values.** All recomputed from
  bytes I built myself. Closed by computation.
- **§7.4's 81-byte payload.** Rebuilt from the field semantics, not copied.
  Offsets, widths, prose accounting, entry_count, extent_length, and the
  byte-for-byte identity with §12.3's channel entry all hold. Closed.
- **§21.8's "120 conditions over 277 instances."** Parsed and counted
  mechanically under §21.1's own rule. Exactly 120 and 277. Closed.
- **Register rows citing a bare § where §21.1 says only two do.** Swept all 120
  Governing-rule cells; exactly L26 and L31. Closed.
- **`[R-CNF-13]`'s "`[R-CNT-06]` states nine".** Counted the rule's own
  conditions (nine) and the register rows governed by it (nine). Closed.
- **§20.5's "one row for each of the other seven spaces".** §10.2 tabulates
  eight; the seven non-record-type spaces map one-to-one onto L36, L33, L34,
  L43, L45, L31, R1. Closed.
- **§15.3's "Six rows are marked *structural*".** Counted six. Closed.
- **§14.4's Note "at P = 1 … the images coincide exactly when that fill is
  false".** Worked the four cases (value × fill) for a single-position packed
  plane against a single interleaved byte: they coincide iff fill is false, and
  P = 1 is the only P with ⌈P/8⌉ = P. Closed as correct.
- **§17.2's Note "§14.2's worked examples give 18 and 30 bytes".** §14.2's
  Example in fact prints three decoded sizes — 18, 12 and 30. The Note names two
  and its point (all below 1 KiB, so single-segment-only under codec 3) holds for
  all three. Incomplete enumeration in a Note whose argument is unaffected; not
  filed.
- **Appendix G's closing paragraph vs item 5.** Item 5 closes four degrees of
  freedom and the paragraph summarises one. The paragraph disclaims being the
  list ("Read the numbered items as the list"). Not filed.
- **Appendix B's "Every named constant this specification fixes, collected."**
  Checked all 27 rows against their defining sections and looked for omissions:
  the 255-byte user-metadata key cap is covered by the "Name length" row because
  §4.6 defines *names* to include user-metadata keys. Found no constant the
  document fixes and the table omits. Closed.
- **§5.1's "tile-index regions" and "record extents" listed side by side**, when
  §5.2/§9.7 make an index region *a* record extent. §5.1 is describing what a
  file's commits appended, not stating the partition — `[R-CNT-02]` states the
  partition and lists four structure kinds. F7's and F33's Instances cells split
  them the same way, which §21.1 licenses as different containers. Closed.
- **§20.3 shape (c) listing only "clearing" a slab declaration** when step 4 also
  permits declaring, changing and re-establishing. Shape (c)'s list is a
  three-item illustration joined by "or", not a closed enumeration, and
  declaring an alignment on a layer whose stored tiles happen already to satisfy
  it is likewise directory-confined. Not filed.
- **§20.5's compaction figure.** Traced the placement claim: A sits at 16 in both
  input and output, so its stored extents do not move and its index is copied
  with only its slot re-pointed; B moves, so B's index is regenerated and marked
  ′. Consistent with `[R-WRT-07]`'s "regenerates each tile-index region any of
  whose stored extents the output relocates". Closed.
- **§5.1's three-commit figure.** Reconstructed the history it implies —
  commit 1 creates A, commit 2 appends B, commit 3 touches no layer — and the
  two ▓ runs land exactly where commits 1 and 2 left their directory/pad/trailer.
  The caption's caveat ("The grouping under the box is illustrative") covers the
  contiguity the box suggests. Closed.
- **§9.2's crash figure.** Row 3's ▓ spans what row 1 shows as dirₙ/pad/trailₙ,
  which is what the caption says it marks. Closed.
- **The one unlabelled blockquote (§15.1).** Confirmed normative under
  `[R-CNF-01]` and confirmed it agrees with `[R-CNT-17]`. Closed.
- **Appendix F's normativity.** No "non-normative" marker, unlike A, B, C, D, E,
  G, H; so normative, which is what `[R-COD-07]`'s delegation needs. Every RFC
  cited in the body is listed. Closed.
- **Requirement-identifier numbering.** No gaps in any prefix; `[R-ENC-100]` is
  §2.2's own illustration; `[R-SER-04]` is withdrawn by an explicit Note.
  Closed.
- **T15/T17/T23's external magic bytes.** gzip `1F 8B`, zstd `28 B5 2F FD`,
  LZ4 frame `04 22 4D 18`, zlib's CMF/FLG + trailing Adler-32 — all correct.
  Closed.

## 13. Where I found little, and what would have found something

The worked examples and byte layouts are the part of this document I can check
hardest, and they are clean: 69 independent arithmetic checks and six checksum
recomputations, zero failures. That is a strong negative result rather than an
absence of looking — a single transposed digit in `0x80A34955`, a wrong
`entry_count`, a mis-summed 81, or a segment boundary off by one would have
surfaced immediately, and I built every value from primitives rather than
reading it back.

The register's *arithmetic* is likewise clean and I can say precisely what would
have shown otherwise: my instance counter is the mechanical rule §21.1 states,
so a cell with one semicolon too many or too few would have moved the 277.

Where my instrument is weakest is judging whether a figure's *framing* misleads,
which is a reading question rather than a computation. diagrams-01 is exactly
that kind of finding and I have graded it accordingly.
