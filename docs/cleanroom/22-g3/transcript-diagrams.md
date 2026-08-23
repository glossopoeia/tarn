# Round 22 — Diagram auditor, verbatim working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,394 lines), in five reads covering lines 1–4394 with no gaps. I ran
`wc -l` and `grep` against that file only, and two Python scripts I wrote
myself in the scratchpad (`crc.py`, `count.py`) that read no project files —
one implements CRC-32C from the parameters in §4.5 and hashes byte strings I
typed in from the document; the other parses the §21 register tables out of a
string I pass it and counts semicolon-separated instance cells. I opened no
ADR, no `PLAN.md`, no `AGENTS.md`, no `conformance/` file, no
`spec/registry.json`, and ran no git command and no web request. I did not
list or read the round22 output directory.

Context I did not ask for **did** appear before I began: the runtime placed a
project instruction file and an index of the maintainer's personal memory
notes into my context, the latter naming several project artifacts and
working practices. I disregarded all of it and did not open anything it
named. I am naming that it appeared, not repeating its contents.

## 1. Method

The charter is: find every figure, byte-layout box, ASCII table, worked
example and checklist first, with line numbers, then judge each one. So the
enumeration comes first and the judgements after it, and the enumeration is
meant to be checkable by someone re-running the same greps.

### 1.1 Enumeration — layout / structure tables (fixed-layout boxes)

Located by `grep -n '^\s*>\?\s*|' | grep '|---'`; 24 markdown tables total.
The ones that are byte-layout boxes or that restate rules:

| Lines | Table |
|---|---|
| 235–241 | §2.4 outcome classes (5 rows) |
| 697–700 | §6.1 front signature block (Offset·Size·Value·Class) |
| 740–752 | §6.2 trailer (Offset·Size·Type·Field·Class·Valid values) |
| 904–910 | §7.2 record header (Offset·Size·Type·Field·Class) |
| 977–980 | §7.3 record types of format major 1 |
| 1006–1023 | §7.4 layer record inline payload (Field·Type·Constraint) |
| 1123–1131 | §8.1 checksum coverage map (7 rows) |
| 1397–1406 | §10.2 numeric identifier spaces (8 rows) |
| 1601–1615 | §12.1 sample types (13 rows) |
| 1833–1836 | §14.2 decoded size / offset of value k |
| 2001–2005 | §15.1 tile-index entry |
| 2049–2061 | §15.3 entry validity (11 rows) |
| 2441–2443 | §18.2 user-metadata encoding byte |
| 2605–2612 | §18.4 standardized keys (6 rows) |
| 3136–3140 | §20.4 updater obligations by stored flags (3 rows) |
| 3384–3421 | §21.2 file-scope register, F1–F36 |
| 3428–3478 | §21.3 layer-scope register, L1–L49 |
| 3485–3512 | §21.4 tile-scope register, T1–T26 |
| 3535–3546 | §21.5 ignored-record register, R1–R10 |
| 3553–3568 | §21.6 conditions that are not violations (14 rows) |
| 3675–3684 | §21.9 minimum guarantees (8 rows) |
| 4026–4042 | Appendix A annotation of the minimal file (14 rows) |
| 4062–4090 | Appendix B constants (27 rows) |
| 4159–4161 | Appendix E changelog |

### 1.2 Enumeration — ASCII figures (fenced blocks)

- 587–592 §5.1, a file after three commits
- 1071–1090 §7.4, the 81-byte layer-record payload hex listing
- 1202–1211 §9.2, what a crash sees (three rows)
- 1996–1997 §15.1, the tile-index region block form
- 3067–3071 §20.3 (a), a new layer
- 3083–3087 §20.3 (b), tiles added to an existing layer
- 3107–3110 §20.3 (c), a change confined to the directory
- 3247–3253 §20.5, what compaction reclaims
- 4015–4024 Appendix A, the 128-byte hex dump

### 1.3 Enumeration — worked numeric examples

513 (`température` NFC/NFD), 577 (smallest file), 1060 (layer record payload),
1518 (grid arithmetic), 1572 (ordinals), 1635 (bfloat16), 1684 (channel entry
bytes), 1754 (fill tuples), 1875 (interleaved/planar byte offsets), 1909
(packed bool plane), 1965 (edge-tile padding), 2089 (segment arithmetic at
10^6 entries), 2104 (planar disk ordinal 74), 2203 (slab runs), 2384
(byte-shuffle), 3053 (supersede one tile), 3062 (three shapes a commit takes),
3244 (compaction). Plus §4.5's **Check vector** at 442.

### 1.4 Enumeration — checklists and appendix material

Appendix A (4009), B (4057), C (4092), D (4119), E (4157), F (4168),
G (4183, numbered items 1–10), H (4323, four class checklists).
Numbered lists elsewhere: §9.2 steps 1–6 (1168), §10.1 vehicles 1–4 (1377),
§19.1 steps 1–4 (2667), §19.4 steps 1–8 (2796), §20.3 steps 1–6 (2920).

## 2. Arithmetic I actually did

### 2.1 Every CRC constant in the document

I implemented CRC-32C from §4.5's parameters (poly 0x1EDC6F41 reflected =
0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against
§4.5's own check vector first, then used it on every stored constant:

| Constant | Document | Computed |
|---|---|---|
| CRC-32C("123456789") (§4.5) | 0xE3069283 | 0xE3069283 ✓ |
| CRC-32C(zero bytes) (§4.5) | 0x00000000 | 0x00000000 ✓ |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 stored `D2 38 09 E0` | 0xE00938D2 ✓ |
| §7.4 segment CRC over 4 sentinel entries (80 B) | 0x80A34955 stored `55 49 A3 80` | 0x80A34955 ✓ |
| §7.4 crc_of_crc_array over those 4 bytes | 0xC4EE982E stored `2E 98 EE C4` | 0xC4EE982E ✓ |
| §15.4 / App. B full all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 ✓ |

All six reproduce. Note the §7.4 example's segment is a *partial* segment
(4 entries, not 2^16), so `[R-IDX-05]`'s "a partial segment's CRC MUST be
computed" applies and 0xEECB3BB2 must not appear there — it does not.

### 2.2 Appendix A, byte by byte

Hex dump at 4015–4024, annotation table at 4026–4042. I laid the trailer's
§6.2 field offsets over file offsets 64–127:

```
64..71   8A 4E 52 41 54 0D 0A 1A   trailer magic            (offset 0,  8B) ✓
72..73   01 00                     version_major = 1        (offset 8,  2B) ✓
74..75   00 00                     version_minor = 0        (offset 10, 2B) ✓
76..79   00 00 00 00               flags = 0                (offset 12, 4B) ✓
80..87   01 00 ×7                  generation = 1           (offset 16, 8B) ✓
88..95   10 00 ×7                  dir_offset = 16          (offset 24, 8B) ✓
96..103  04 00 ×7                  dir_length = 4           (offset 32, 8B) ✓
104..111 80 00 ×7                  committed_file_length=128(offset 40, 8B) ✓
112..119 EF CD AB 89 67 45 23 01   file_id = 0x0123456789ABCDEF LE ✓
120..123 00 00 00 00               reserved zero            (offset 56, 4B) ✓
124..127 D2 38 09 E0               CRC = 0xE00938D2         (offset 60, 4B) ✓
```

The annotation table's 14 rows name exactly these ranges plus [0,8), [8,16),
[16,20), [20,64), and every range is contiguous and non-overlapping and sums
to 128. Directory [16,20) = `00 00 00 00`: dir_length 4, so the covered
record sequence is 0 bytes and its CRC is 0 — consistent with §7.1 and with
§4.5's second check vector. Pre-trailer pad [20,64) = 44 bytes, and
`[R-LIF-02]` step 5 pads to the next 64-byte boundary from 20, which is 64,
so 44 is exactly what a conforming commit produces. Gate-by-gate against
`[R-CNT-06]`: magic ✓, CRC ✓, major 1 ✓, flags 0 ✓, F=128 and 128 mod 64 = 0 ✓,
dir_offset 16 ≥ 16 ✓, dir_length 4 ≥ 4 ✓, 16+4 = 20 ≤ 128−64 = 64 ✓,
1 ≤ generation ≤ 2^63−1 ✓, file_id ≠ 0 ✓, reserved zero ✓. The file is
conforming and is the 128-byte minimum §5.1 and `[R-CNT-27]` derive.

Appendix A's closing prose: "112 bytes covering [16, 128)" — 128−16 = 112 ✓,
and that window contains [16,20) so §6.4's containment test applies while
[0,16) stays non-resident, which is exactly the split `[R-CNT-04]` draws.

**Appendix A is clean.**

### 2.3 §7.4's 81-byte layer record payload

Field order in the listing must match the table at 1006–1023. It does. I
recomputed every offset from the widths:

```
 0 name        1 + 3   = 4     -> next 4
 4 layout      u8      = 1     -> 5
 5 lineariz.   u16     = 2     -> 7
 7 codec       u16     = 2     -> 9
 9 filter      u16     = 2     -> 11
11 A           u64     = 8     -> 19
19 S           u64     = 8     -> 27
27 A_slab      u64     = 8     -> 35
35 rank d      u8      = 1     -> 36
36 C           u16     = 2     -> 38
38 dim entry   2+8+8   = 18    -> 56
56 chan entry  5+2+5   = 12    -> 68
68 index_enc   u8      = 1     -> 69
69 entry_count u64     = 8     -> 77
77 crc_of_crc  u32     = 4     -> 81
```

Every offset in the listing matches. The prose's decomposition —
"4 + 34 bytes, the dimension entry 18, the channel entry 12, and the
trailing fixed fields 13 — 81 exactly" — checks: the nine scalars from
layout through channel count are 1+2+2+2+8+8+8+1+2 = 34 (and they are nine),
4+34+18+12+13 = 81. Byte values: `sst` = 73 73 74 ✓; `x` = 78 ✓; 100 = 0x64 ✓;
32 = 0x20 ✓; `temp` = 74 65 6D 70 ✓; type 12 = `0C 00` ✓; fill
`00 00 C0 7F` = 0x7FC00000 ✓. The channel entry is byte-identical to §12.3's
twelve-byte example `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, as claimed.
Geometry: ceil(100/32) = 4, interleaved so addressed-tile count = N = 4 =
entry_count ✓. `[R-CNT-17]`: 4×20 + ceil(4/65536)×4 = 80+4 = 84, and the
prose says 84 ✓. The index region is the 80-byte entry array plus one
4-byte segment CRC ✓ per §15.1's block form. Both CRCs reproduce (§2.1).

**§7.4's example is clean.**

### 2.4 The remaining worked examples

- §4.6, `température`: NFC `74 65 6D 70 C3 A9 72 61 74 75 72 65` is t·e·m·p·é·r·a·t·u·r·e = 12 bytes with é two bytes ✓; NFD 13 ✓.
- §11.2: (1024,2048)/(256,256) -> G=(4,8), N=32, P=65536 ✓. (1000,2048): ceil(1000/256)=4 ✓.
- §11.4: (300,700) -> tile (1,2), s = 1·8+2 = 10 ✓; in-tile (44,188) -> 44·256+188 = 11,452 ✓; planar c=2 -> 2·32+10 = 74 ✓.
- §12.1 bfloat16: 1.0 binary32 0x3F800000 -> high 16 = 0x3F80, stored `80 3F` ✓; 0x7FC0 quiet NaN ✓.
- §13.3: r,g,b uint8 fills FF,00,00 -> (255,0,0) ✓.
- §14.2: Q = 1+2 = 3, decoded 6·3 = 18 ✓; ordinal 1·3+2 = 5, bytes [15,18) ✓; planar b = 6·2 = 12 B, ordinal 5 at [10,12) ✓; float32+bool: Q = 5, 6·5 = 30, ordinal 5 at [25,30), t at 25–28, m at 29 ✓. Closing identity "u·Q + F^c — the table's forms with k = u·C + c": k div C = u, k mod C = c ✓.
- §14.3: P = 10, alternating from true: bits 0,2,4,6 set -> 0x55 ✓; values 8,9 = true,false -> 0x01 ✓; P mod 8 = 2 so pad bits 2–7 ✓; fill true -> 0x01|0xFC = 0xFD ✓.
- §14.5: extents (5,5)/tiles (4,4) -> grid 2×2 ✓; tile (1,1) covers 4–7 both axes, one real position (4,4) at in-tile ordinal 0, 15 padding ✓; P=16, uint16 -> 32 bytes ✓; fill 0xABCD LE = `CD AB` ✓.
- §15.4 first example: ceil(10^6/2^16) = 16 segments, 15 full = 983,040, last = 16,960 ✓; array 64 B ✓; region 20,000,064 ✓; k = 999,999 in segment 15 at relative byte 20·16,959 = 339,180 ✓; array at [20,000,000, 20,000,064) ✓; segment 15 at [19,660,800, 20,000,000) = 339,200 B ≈ 339 KB ✓; one full segment = 65,536·20 = 1,310,720 = 1.25 MiB ✓.
- §15.4 second example: ordinal 74 -> region bytes [1480,1500) ✓; channel 3's block is [96,128), i.e. entries 96–127, 32 copies ✓.
- §16.2: N=32, S=8 -> runs [0,8),[8,16),[16,24),[24,32) ✓, each one tile-row under row-major with G_x = 8 ✓; rows 1–2 = ordinals 8–23 = runs 1 and 2 ✓; sentinel at 10 -> stored 8,9,11..15 ✓.
- §17.3: 1.0/2.0/3.0 -> `00 00 80 3F 00 00 00 40 00 00 40 40`; s=4, n=3; byte i of group j to i·n+j gives `00 00 00 00 00 00 80 00 40 3F 40 40` ✓ exactly as printed, and the prose's grouping "then `80 00 40`, then `3F 40 40`" ✓.
- §20.3: 32·20 + 4 = 644 ✓, "one entry re-pointed, 31 byte-identical" ✓.

**No numeric error found in any worked example in the document.**

### 2.5 The §21 register, counted mechanically

§21.1 fixes the instance count as mechanical: "Instances within a cell are
separated by semicolons, and a cell reading — is one instance". I parsed all
121 rows and applied exactly that rule:

- §21.2: 36 rows, 58 instances (header claims 36 conditions ✓)
- §21.3: 49 rows, 116 instances (header claims 49 ✓)
- §21.4: 26 rows, 55 instances (header claims 26 ✓)
- §21.5: 10 rows, 44 instances (header claims 10 ✓)
- Totals: **121 rows, 273 instances**, against §21.8's "121 conditions over
  273 instances" ✓.

I then spot-checked the enumeration axes §21.1 declares. Layout-varying
quantities enumerate three layouts (interleaved P·Q, planar numeric P·B^c,
packed planar bool ceil(P/8)): T3 3×2 directions = 6 ✓, T14 3×2 = 6 ✓,
T22 3×2 = 6 ✓, T21 3×1 (an "exceeds", one direction) = 3 ✓, L44 3×1 = 3 ✓,
T26 3 ✓. Magnitude pairs: L21 2 layouts × 2 directions = 4 ✓, L22 2+2 = 4 ✓,
L30 2 ✓, F17 2 ✓. Family-as-one-instance: T24 "any codec" = 1 ✓.
L2's nine derived quantities include the two dominance claims — C·N dominates
the max disk ordinal (C−1)·N + (N−1) = C·N − 1 ✓, and P·Q dominates V = P·C
because Q = ΣB_i ≥ C when every B_i ≥ 1 ✓. L23's four regions match
`[R-CNT-18]`'s four ("the fixed fields, the d dimension entries, the C
channel entries, and the trailing fixed fields") ✓.

§15.3's prose says "Six rows are marked *structural*"; the table has 11 rows
of which exactly 6 carry *structural* ✓.

§21.2's preamble claims "Four rows are outside that reasoning and do reach"
a foreign-major file: F8, F14, F6, and F1 (both instances) — four rows ✓, and
each subject is fixed across majors by `[R-CNT-24]` (magic, the CRC at F−4,
the front block) ✓. F15's subject, trailer [56,60), is inside the 48 bytes
`[R-CNT-24]` lets a future major redefine, so its exclusion is right ✓.

`[R-CNT-24]`'s own arithmetic: fixed across majors are [0,8) magic,
[8,12) versions, [60,64) CRC = 16 bytes, leaving 48 ✓ "MAY redefine only the
remaining 48 trailer bytes". "The format-major-1 trailer has zero slack":
8+2+2+4+8+8+8+8+8+4+4 = 64 ✓ and §6.2's offsets 0,8,10,12,16,24,32,40,48,56,60
are contiguous ✓. §7.2's header: 0,2,4,8,16 with widths 2,2,4,8,8 = 24 ✓.
§15.1's entry: 0,8,16 with widths 8,8,4 = 20 ✓.

**The register's arithmetic is fully self-consistent.** This is worth saying
plainly because it is the single largest checkable surface in the document.

### 2.6 §8.1's coverage map against §4.5

§4.5 names three terminal checksum fields (trailer, directory-region,
user-metadata) and three interior ones (each segment CRC array, each
tile-index entry's crc, each layer record's crc_of_crc_array), and claims
each interior one is covered by "exactly one further checksum". Walking the
map: entry crc fields sit inside index entries -> segment CRC ✓; the segment
CRC array -> crc_of_crc_array ✓; crc_of_crc_array is a layer-record field, so
it sits in the directory region -> directory CRC ✓. Exactly one each. Every
structure §5.2 names has a row: front block (equality), trailer, directory,
tile-index region, stored tile, user-metadata extent, unassigned-type extent
(none). Seven rows, no structure unmapped. ✓

### 2.7 §10.2's identifier-space table against the owning sections

record type 0x0001–2 / 0x0003–0x7FFF / ≥0x8000 vs §7.3 and F35/F36 ✓;
channel layout 1,2 / 3–255 / none vs `[R-SER-06]` ✓; linearization 1 /
2–0x7FFF / ≥0x8000 vs `[R-GEO-05]` (which sub-splits 2–3 and 4–0x7FFF) ✓;
sample type 1–13 / 14–0x7FFF / ≥0x8000 vs `[R-TYP-03]` ✓; codec 1–4 /
5–0x7FFF / ≥0x8000 vs `[R-COD-03]` ✓; filter 1,2 / 3–0x7FFF / ≥0x8000 vs
`[R-COD-09]` ✓; index encoding 1 / 2–0x7F / ≥0x80 vs §7.4 ✓; metadata
encoding 1,2 / 3–0x7F / ≥0x80 vs `[R-MTA-03]` ✓. Appendix C's snapshot
agrees with all eight. Appendix B's 27 constants each reproduce their
defining section, including the two I recomputed.

### 2.8 Appendix H's checklists against the rules they summarise

Reader: "implements all four codecs, both filters, both layouts, all thirteen
sample types, and both user-metadata encodings" — §17.2 makes codecs 1–4
core (four), §17.3 both filters core, §14.1 two layouts, §12.1 "exactly
thirteen sample types, all core", §18.2 "Both assigned encodings are core".
All five counts match `[R-CNF-03]` ✓. Writer, updater and verifier lists each
trace to a stated rule; the verifier list covers every *verifier*-detector row
family in §21 (F7, F25/F26/L46/L47, F27/L48, F28/L49, F33, F36/L25, L18,
L40/L41/L42, T2/T4/T5/T26) plus §9.7's coverage walk and `[R-MTA-10]`'s
report ✓.

Appendix G's numbered list runs 1–10 with no gap, no duplicate, no
transposition; its closing paragraph does not enumerate every item, but it
disclaims that explicitly — "Read the numbered items as the list; this
paragraph names what they are for, not how many there are" — so the promise
it makes is the one it keeps.

### 2.9 Step cross-references

Every `[R-LIF-02]` step citation resolves correctly: §5.1 "steps 3 and 5"
(directory; pad+trailer) ✓, §6.2 "step 5" (the pad) ✓, §2.3 "step 5's pad" ✓,
§9.4 "before step 1"/"no later than step 6" ✓, §20.2 "steps 4–6 — both
barriers, not one" (4 and 6 are the two barriers) ✓, §20.3 "steps 1–2",
"step 3", "steps 4–6" ✓, Appendix G "step 2" (placement) ✓. §19.1's four
steps, §19.4's eight steps (with "steps 3 through 6 run once per needed
entry" and the sentinel short-circuiting 5 and 6) and §20.3's six steps are
internally ordered and consistently referenced.

## 3. The two changed passages

### 3.1 §21.9 — which instances the guarantee table ranges over

> "The last three rows are **per-instance**: they range over the tiles,
> user-metadata documents and compressed frames a file actually contains,
> and a file containing none of a kind does not exceed that row, whatever
> its declarations would derive — a layer addressing no tile (§11.2) has no
> tile whose decoded size the table can bound, exactly as `[R-COD-07]`'s cap
> is quantified over a layer's *addressed* tiles. The first five range over
> declarations, which every file and every layer carries."

Mechanical check first: the table has 8 rows; the last three are decoded tile
size, user-metadata document size, zstd `Window_Size`, and those are exactly
the three the sentence names (tiles, documents, frames) ✓. The first five are
rank, C, entry_count, layers per file, dir_length — all declarations, and
every file carries a layer count and a dir_length while every layer carries a
rank, a C and an entry_count ✓. 5 + 3 = 8 ✓.

I then pressed the quantifier, since that is the shape the charter flags.
The live question is a layer that *addresses* tiles but *stores* none — every
entry the sentinel — while declaring a decoded tile size above 256 MiB. Does
the file "contain" a tile whose decoded size exceeds the guarantee? Under a
stored reading it does not, and `[R-CNF-03]` obliges every conforming reader
to accept it; under an addressed reading it does, and `[R-ERR-04]` licenses a
decline. That would be a genuine accept/refuse fork.

The text decides it, and I want to record why I concluded that rather than
report it. The gloss's analogy is not loose: "exactly as `[R-COD-07]`'s cap is
quantified over a layer's *addressed* tiles" states the quantifier by name,
and §17.2's Note it points at says the same thing twice ("The cap is
quantified over the layer's *addressed* tiles, so a layer that addresses none
… satisfies it whatever its tile shape declares"). §20.3 step 4 uses the same
phrase a third time ("`[R-COD-07]`'s lz4 decoded-size cap … which an empty
layer escapes only because that cap is quantified over addressed tiles").
Three occurrences, all *addressed*, and `[R-ERR-04]`'s own decline clause is
worded over declarations ("at the narrowest scope whose declarations exceed
what it can serve"). An all-sentinel layer's declarations do derive the
oversized decoded size, so the decline is licensed and the reader that
accepts is also conforming — the row is a floor, not a duty to refuse. I
found no reading on which two conforming implementations must disagree.
**No finding.**

I also checked the per-instance rows against the rules that reference them:
`[R-COD-06]`'s "Writers SHOULD keep the declared window within §21.9's 8 MiB
`Window_Size` guarantee" ✓, §18.2's "no smaller than §21.9's user-metadata
guarantee" and its Note's "The 16 MiB figure is a §21.9 minimum guarantee" ✓,
Appendix B's "8 MiB zstd window" and "16 MiB metadata document" ✓, and
`[R-VEC-03]`'s carve-out that the tile-count guarantee is exercised by a
scaled vector rather than one at the bound — that is the entry_count row,
which is one of the *first five* and so always has an instance ✓ consistent.

### 3.2 §18.2 — the metadata frame's content-size field

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is a failure to decode
> within the meaning of R3, so that R3's condition stays checkable from the
> bytes alone rather than turning on a decoder's tolerance (`[R-CNF-02]`)"

This pins a header field that §18.2 previously left open, and it does so by
routing the breach into an existing register row rather than adding one. The
routing is what I went after, because §21.5 already has a row whose condition
text claims the neighbouring territory. That is finding **diagrams-02** below.

Everything else in the passage traces cleanly. The four constraints §18.2
carries over from `[R-COD-06]` — magic, no skippable/second frame, no nonzero
dictionary ID, no content-checksum flag — are the four `[R-COD-06]` states
that do not reference a tile, and R4 enumerates exactly those four plus the
single-frame-occupancy rule ✓. The decline machinery routes to `[R-CNF-11]`'s
*cannot establish* and to `[R-ERR-04]`'s resource-limit reporting, both of
which say what §18.2 says they say ✓.

## 4. The degenerate-file walk

Rounds that found survivors did it by building a file nobody would write on
purpose. Mine:

**File Z.** 128-byte skeleton as Appendix A, but with one layer record: rank 1,
dimension `x` with E = 0, T = 1; one interleaved float32 channel `t`, fill
all-zero; codec 1, filter 1; A = 0, S = 0, A_slab = 0; index_encoding 1;
entry_count 0; crc_of_crc_array 0; extent slot (0,0); no sub-records.

Walked against every table that has to say something about it:
- §11.2: G = ceil(0/1) = 0, N = ∏G = 0, addressed-tile count = N = 0 ✓;
  P = ∏T = 1, N·P = 0.
- §7.4: "a layer with zero addressed tiles has extent (0, 0)" ✓; `[R-CNT-17]`
  "and 0 when entry_count is 0" ✓; `[R-CNT-23]` forces crc_of_crc_array 0 ✓.
- L22's instances name both traps at this boundary — "slot (0,0) with
  entry_count > 0" and "a nonzero slot with entry_count = 0" — and file Z
  trips neither ✓. L27 likewise ✓.
- §15.4's example closes the same case explicitly: "At entry_count = 0 there
  is no region at all — zero segments, a zero-byte CRC array, extent slot
  (0, 0) and crc_of_crc_array = 0 … so nothing is fetched and nothing is
  verified" ✓.
- §21.6's row "A dimension has extent 0" -> "zero addressed tiles, an empty
  index, reads returning no samples" ✓.
- §21.9: the layer addresses no tile, so the decoded-tile row has no instance
  ✓ — and P·Q = 4 is still checked under `[R-ENC-04]` because §17.2's Note
  says the overflow rule "carries no such quantifier" ✓.
- §19.4 step 1: "any region of a zero-extent layer, succeeds and returns no
  samples" ✓.
- L44: codec 4 on this layer would be conforming, per §17.2's Note ✓.

Then a second degenerate: **file Z′**, same but with codec 3 and a stored
tile whose decoded size is 2 bytes (§14.3's packed-plane example size). §17.2's
Note answers it before I could ask: below 1 KiB the Window_Descriptor cannot
express the window, so the tile is encodable only as a single-segment frame,
and "no conforming file turns on which derivation a reader implements" ✓.

Third: **file Z″**, a commit that touches no layer. This is where §5.1's
figure prose overreaches — finding **diagrams-03**.

No further defect surfaced from the degenerate walk. The zero-extent and
zero-entry boundaries are covered in five places and they agree in all five.

## 5. Findings

### diagrams-01 — OBSERVATION

**Location.** §21.6's non-violation table, row 5 (line 3559); §20.4's updater
obligation table (lines 3136–3140); §2.2.

**Quotation.** §21.6's row cell and its Rule cell, verbatim:

> "| A record type this specification has not assigned, from the experimental
> range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
> per its PE bit; a *reserved*-range type is read the same way, but emitting
> one is a violation (F36, L25) | `[R-CNT-15]`, `[R-WRT-08]` |"

and `[R-WRT-08]` in full (lines 3152–3156):

> "An updater MUST NOT re-encode a record whose type it does not implement,
> and MUST NOT modify one except by relocating its extent and re-pointing its
> slot under §20.5 — the operation the no-embedded-offsets rule (§7.2) makes
> safe for MU = 0 records. `[R-WRT-08]`"

**Detail.** §21.6's cell attributes "preserved or dropped per its PE bit" to
`[R-CNT-15]` and `[R-WRT-08]`. `[R-CNT-15]` supplies "Ignored" and nothing
about preservation. `[R-WRT-08]` supplies a re-encoding prohibition and a
relocation permission and says nothing about PE, preservation, or dropping.
The rule that actually states "preserved or dropped per its PE bit" is
§20.4's three-row table, whose MU = 0 / PE = 1 row reads "Retain
byte-identical, extent content unmodified" and whose MU = 0 / PE = 0 row reads
"Retain byte-identical, or drop it — its extent becoming slack."

The reason the citation goes astray is structural, and it is the part worth
reporting: **§20.4's table carries normative requirements and no requirement
identifier.** Its cells contain "The updater MUST NOT modify the scope the
record governs", "An appender MUST NOT drop it except in a commit that
*independently* changes the scope the record attaches to", "A compactor MAY
drop it whenever it rewrites the file", and "An updater that drops such a
record SHOULD report the loss". §2.2 says "Normative requirements carry
identifiers of the form `[R-<PREFIX>-<NN>]`", and every other normative
paragraph in this document does. The table sits between `[R-WRT-05]` (line
3122, which covers only byte-identical re-emission of retained records) and
`[R-WRT-08]` (line 3156), and neither identifier's sentence states the
table's content. So a citer has no correct identifier to reach for, and
§21.6 reached for the nearest one.

I considered and rejected two innocent readings. First, that `[R-WRT-05]`
covers it: `[R-WRT-05]` requires re-emission of "every record it retains and
does not logically modify" — it says nothing about which records may be
retained versus dropped, which is exactly what the PE bit decides. Second,
that the table is a restatement of §2.4's preserve-verbatim row and inherits
`[R-CNF-08]`: §2.4 points the other way ("§20.4's table states the cases"),
so the table is the source, not the restatement.

Downstream, `[R-VEC-02]` requires a vector entry to record "the §21 register
row it exercises together with that row's governing requirement identifier",
and reasons that identifiers are what survive renumbering while row labels do
not. §21.6 is not a register row, so no vector is blocked today; but the same
argument says a rule with no identifier is a rule nothing can cite stably,
and the drop permission in §20.4's PE = 0 row is the most intricate
conditional in Part III — it turns on whether a commit "*independently*
changes the scope the record attaches to" — which is precisely the kind of
rule an implementer will want to cite.

**What an implementer does wrong without it.** Nothing to the bytes: an
implementer who follows the `[R-WRT-08]` pointer lands in §20.4 anyway and
reads the table two lines above. The cost is to citation and to review — a
reviewer checking §21.6's entry against its stated rule finds the rule does
not contain the claim, and (per §21.1's closing, "where such an entry and the
rule it cites diverge, the rule governs there too") would be entitled to
conclude that the preserve-or-drop behavior is unstated at that entry, which
it is not.

**Byte-level: no.** Both the correct rule (§20.4's table) and the incorrect
citation point at the same behavior; §20.4's table is unambiguous on its own
terms, and no reader obligation and no emittable byte turns on which
identifier §21.6 names. The obligations are updater-side and §21.7 already
records that they have no single-file witness.

### diagrams-02 — AMBIGUITY

**Location.** §18.2, `[R-MTA-09]`; §21.5 rows R3 and R4 (lines 3539–3540);
§21.8, `[R-ERR-02]`; §21.4 row T22 (line 3508).

**Quotation.** §18.2:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is a failure to decode
> within the meaning of R3"

and R4's condition cell:

> "A user-metadata document stored under encoding 2 breaks one of the frame
> constraints §18.2 states or carries over from `[R-COD-06]` — the single
> frame occupying the extent's bytes before its terminal CRC included; unlike
> R3, the constraint is broken whether or not the bytes decode"

**Detail.** Two readings are available for a file whose metadata frame
declares a `Frame_Content_Size` that differs from the decoded document's byte
length, and both are defensible from the text.

*Reading A — R4.* R4's condition ranges over "one of the frame constraints
§18.2 states", and the content-size requirement is a frame constraint §18.2
states, in the same paragraph as the four carried over from `[R-COD-06]`.
R4's distinguishing clause fits it exactly: a declared content size can
disagree with the decoded length while the frame decodes perfectly, so "the
constraint is broken whether or not the bytes decode" is true of it and true
of nothing else in §18.2 that R4 does not already list.

*Reading B — R3.* §18.2 says in terms that the mismatch "is a failure to
decode within the meaning of R3", and gives the reason: it keeps R3's
condition "checkable from the bytes alone rather than turning on a decoder's
tolerance". R3's condition cell reads "A user-metadata document's stored bytes
fail to decode under its declared assigned encoding".

**I pick reading B**, because §18.2 states it directly and §21.1 makes the
rule govern over the row where they diverge; R4's clause is then a
description of R4's own six listed constraints rather than a test that
recruits new ones.

**What an implementer does wrong without it.** Two things, neither of which
changes a verdict.

First, corpus construction. `[R-ERR-02]` requires "at least one conformance
vector … and one vector per instance", and `[R-VEC-03]` repeats it. R3's
Instances cell is "top-level extent; layer sub-record extent" — two
instances, no alternative and no direction pair. R4's is twelve: six
constraint kinds each in two containers, and content-size is not among the
six. So on either reading **no instance in the register names a content-size
mismatch, and the corpus therefore builds no vector for it.** The contrast
with the tile side is stark and is what convinced me this is worth reporting:
the identical constraint on a *tile* frame is row T22, whose cell enumerates
six instances (three layout formulas × two directions, since §21.1 makes a
"does not equal" over two magnitudes enumerate both). The document's newest
MUST is the only frame-header constraint in it with no vector behind it.

Second, verifier reporting and vector attribution. `[R-VEC-02]` requires each
vector to name the row it exercises and provides for the un-isolatable case
by recording "every row the file exercises and says which it was built for" —
but that provision is for conditions §6.2 validates together, not for a
condition two rows both claim. §21.1's list of rows that are strict
specializations of others ("F1 of F6 and of F8, F35 of F36, L24 of L25") does
not include an R3/R4 pair, so the register offers no tiebreak of its own.

**Byte-level: no.** R3 and R4 carry identical Outcome (ignore-record),
Detector (reader) and Detected (extent use) cells, and both route through
`[R-CNT-25]`'s quarantine. Whichever row a file is recorded against, every
conforming reader ignores the record and reports the loss, and the file is
nonconforming either way. Two implementations reading this text agree on
every byte and on every accept/reject verdict; they disagree only about which
label a manifest entry carries. That is a corpus-coverage and taxonomy defect,
not a fork.

### diagrams-03 — OBSERVATION

**Location.** §5.1, the "file after three commits" Example, lines 604–607.

**Quotation.**

> "Layer A's tiles and index have never moved: a layer the commit does not
> touch keeps its extent slot pointing where it always pointed (§20.3,
> `[R-WRT-05]`), so a commit that touches no layer re-emits the directory,
> the pad and the trailer alone."

**Detail.** The inference in the "so" clause is false for one commit shape the
document names elsewhere. §7.2 admits exactly two top-level record types in
format major 1, layer and user-metadata, so a commit that touches no layer can
still change the file-scope user-metadata record — and §20.3's shape (c)
figure says what that costs, in terms:

> "Editing user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack,
> as in (b)."

Such a commit touches no layer and appends a record extent *in addition to*
the directory, the pad and the trailer. The §5.1 sentence says "alone",
which is right for the figure's commit 3 (a no-op or checkpoint commit under
`[R-LIF-07]`) and wrong as the general claim the "so" makes it.

The figure itself is correct. I checked the three-commit reconstruction:
commit 1 emits front + A + dir₁/pad/trail₁; commit 2 appends B +
dir₂/pad/trail₂; commit 3 appends dir₃/pad/trail₃. That yields
front | A | ▓ | B | ▓ | dir₃ | pad | trail₃, and the caption's identification
of the two ▓ runs as "the directories, pads and trailers of commits 1 and 2"
matches ✓. The live-state statement ("front, both layers' structures, dir₃ and
trail₃") matches `[R-CNT-02]` ✓, and the pad's classification as slack matches
§5.2 ✓. Only the generalising clause overreaches.

**What an implementer does wrong without it.** A writer implementer reading
§5.1 first could budget a metadata-only commit as directory-plus-trailer and
discover at §20.3 that it needs an appended extent. There is no way to act on
the §5.1 sentence and emit a nonconforming file — the old extent is frozen by
`[R-LIF-01]`, so a writer that tries to edit metadata without appending
simply cannot change the document — so the cost is a wrong cost model, not a
wrong file.

**Byte-level: no.** §20.3 shape (c) and `[R-CNT-25]` decide the behavior, and
this sentence is Example text, non-normative under `[R-CNF-01]`. No byte and
no verdict turns on it.

### diagrams-04 — OBSERVATION

**Location.** §4.7's Note, lines 536–546; §7.4's inline-payload table, lines
1006–1023.

**Quotation.**

> "Layout tables for fixed-layout structures give, per field: byte offset
> within the structure, size, type, name, taxonomy class, and valid range,
> each table giving the columns its structure needs. A packed variable-length
> payload — the layer record's inline payload (§7.4) — has no fixed offsets to
> give; its table omits the offset and class columns, and each field's class
> follows from the definitions above."

**Detail.** The Note enumerates six columns and then says §7.4's table omits
two of them, naming offset and class. §7.4's table has three columns —
**Field | Type | Constraint** — so it omits three: offset, class, **and
size**. I checked the claim against every other structure table to be sure
the six-column baseline is the right one to measure against, and it is:
§6.2's trailer and §15.1's entry and §18.2's encoding byte all carry the full
six (Offset·Size·Type·Field·Class·Valid values); §6.1's front block carries
Offset·Size·Value·Class, which the Note accounts for ("a Value column
replaces type and range"); §7.2's header carries five and folds the range into
the Field cell, which the Note also accounts for. §7.4 is the one table whose
omissions the Note states explicitly and states incompletely.

The escape clause "each table giving the columns its structure needs" softens
this, and the omitted size is recoverable — the Type cells give `u8`, `u16`,
`u64`, and "u8 len + bytes" for the variable-length fields — which is why I
grade this an OBSERVATION rather than an ambiguity. But the Note is the
document's own account of its presentation discipline, it is the only place
that account is given, and it is the natural thing for a reader to check a
table against.

**What an implementer does wrong without it.** Nothing. The widths are in
§7.4's Type column and in §4.2's type definitions, and §7.4's worked example
lays out all fifteen fields at explicit offsets. This is a defect in the
document's description of itself.

**Byte-level: no.** A Note is non-normative under `[R-CNF-01]`, and the field
widths it fails to mention are fixed by `[R-ENC-06]` and given in the table
it describes.

## 6. What I checked and found sound

Recorded so the coverage is auditable and so the finding list is not read as
the whole result:

- All six CRC constants recompute (§2.1).
- Appendix A verifies byte for byte, gate for gate, against §6.2 and §7.1 (§2.2).
- §7.4's 81-byte payload verifies field for field and offset for offset (§2.3).
- All eighteen worked examples verify numerically (§2.4).
- The register's counts — 36/49/26/10 rows, 273 instances, §21.8's totals — are exact, and the instance axes follow §21.1's stated rules in every row I sampled (§2.5).
- §8.1's coverage map is complete and its "exactly one further checksum" claim holds for all three interior checksum fields (§2.6).
- §10.2's eight spaces agree with their owning sections and with Appendix C; Appendix B's 27 constants agree with their defining sections (§2.7).
- Appendix H's four checklists agree with the rules they summarise, including all five counts in the reader entry (§2.8).
- Appendix G's items run 1–10 with no gap or duplicate, and its non-exhaustive closing paragraph disclaims exhaustiveness explicitly (§2.8).
- Every `[R-LIF-02]` step citation in six sections resolves to the right step; §19.1, §19.4 and §20.3's numbered procedures are ordered and correctly cross-referenced (§2.9).
- The zero-extent / zero-entry_count boundary is stated in five places (§7.4, `[R-CNT-17]`, `[R-CNT-23]`, §15.4's example, §21.6) and they agree (§4).
- §15.3's "Six rows are marked *structural*" is exactly six; §21.2's "Four rows" is exactly four (§2.5).
- §21.5's ten rows deliver every unreadability path `[R-CNT-25]` enumerates and every restriction `[R-MTA-04]` states, including the U+FEFF and 255-byte-key sub-rules (checked row by row).

Two near-misses I chased and dismissed, recorded so the next round need not
repeat them:

- **§19.1 step 4 and §19.3 do not name the metadata encoding byte's value check, but R1's Detected cell says open / layer access.** §19's preamble forecloses the complaint in terms: "Those enumerations are not the complete inventory of what a reader detects at that tier: §21's register is … A row this section does not restate is due at its own tier all the same." Not a defect.
- **§20.5's compaction figure carries the legend "▓ marks slack" and shows an output with no ▓ but with a `pad`, which §5.2 classifies as slack.** The convention is consistent across all four region figures (pad is always drawn as a labelled region, never hatched) and §5.1's caption states the key explicitly ("the pad and the ▓ runs are slack"). Not a defect.

## 7. Confidence

**Medium-high** on the charter's surface, which is the part I can speak to.
Every number, offset, width, constant, count and cross-reference in every
figure, layout box, worked example, register table, constants table and
checklist reproduces from the normative text, and the one large mechanical
surface — the 121-row, 273-instance register — is internally exact. An
implementer building from the diagrams alone would get the bytes right.

I return **no byte-level finding**. That is an honest result rather than a
concession to the acceptance gate: I looked hardest at the two changed
passages and at the quantifier shape the charter named, and in the one place
that shape could have forked a verdict — §21.9's tile row over an
all-sentinel layer — the document pins the quantifier three separate times,
in §17.2's Note, §20.3 step 4, and the changed sentence itself. The four
findings I do return are a mis-citation with an unidentified rule behind it,
a register-attribution gap that leaves the document's newest MUST with no
conformance vector, an Example clause that overreaches by one commit shape,
and a Note that miscounts its own omitted columns. None of them changes a
byte or a verdict, and I have said so in each.
