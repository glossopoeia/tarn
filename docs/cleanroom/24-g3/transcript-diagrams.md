# Round 24 — Diagram auditor — verbatim working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in four
`Read` calls covering lines 1–4446 (the whole file). I opened no other file. I ran no `git`
command, no web fetch, no directory listing of the project. The only other things I ran were
Python scripts I wrote myself into my own scratchpad (`work/crc.py`, `work/build.py`) plus
inline `python3 - <<EOF` heredocs; those scripts read `spec/tarn.md` and nothing else, and one
of them wrote a synthetic `.tarn` file into my scratchpad. I ran three `grep`-family commands,
all against `spec/tarn.md` only.

Context I did not ask for: my runtime placed a project-instruction block (`CLAUDE.md`
pointing at `AGENTS.md`) and an index of the maintainer's auto-memory files in my context
before I began. The memory index carried titles suggesting things about this project's
process and about §21's relationship to a conformance corpus. I did not open any of the files
it names, and I have not used any of it as evidence. I disclose that it appeared. Nothing in
this transcript derives from it; every claim below is anchored to a quotation from
`spec/tarn.md` or to arithmetic I did myself.

---

## 1. Method: enumerate before judging

My charter is every figure, byte-layout box, ASCII table of offsets, worked example, checklist,
and any table whose cells restate a rule stated in prose elsewhere. I enumerated them first so
the coverage is checkable.

### 1.1 Fixed-layout / byte-layout tables

| Lines | Structure | Columns delivered |
|---|---|---|
| 697–700 | §6.1 front signature block | Offset, Size, Value, Class |
| 740–752 | §6.2 trailer | Offset, Size, Type, Field, Class, Valid values |
| 904–910 | §7.2 record header | Offset, Size, Type, Field, Class |
| 1006–1023 | §7.4 layer-record inline payload | Field, Type, Constraint |
| 2001–2005 | §15.1 tile-index entry | Offset, Size, Type, Field, Class, Valid values |
| 2441–2443 | §18.2 user-metadata inline payload | Offset, Size, Type, Field, Class, Valid values |

### 1.2 Other normative or rule-restating tables

- 235–241 §2.4 outcome classes
- 977–980 §7.3 record types of format major 1
- 1123–1131 §8.1 checksum coverage map
- 1397–1406 §10.2 numeric identifier spaces
- 1601–1615 §12.1 core sample types
- 1833–1836 §14.2 decoded size / offset-of-value-k
- 2049–2061 §15.3 entry-validity classification
- 2631–2638 §18.4 standardized keys
- 3164–3166 §20.4 updater preservation obligations (3 rows)
- 3414–3452 §21.2 file-scope register (F1–F36)
- 3458–3508 §21.3 layer-scope register (L1–L49)
- 3515–3542 §21.4 tile-scope register (T1–T26)
- 3565–3576 §21.5 ignored-record register (R1–R10)
- 3583–3598 §21.6 conditions that are not violations
- 3722–3731 §21.9 minimum-guarantee limits
- 4077–4093 Appendix A annotated minimal file
- 4113–4141 Appendix B constants
- 4210–4212 Appendix E changelog

### 1.3 ASCII figures

- 587–592 §5.1 "a file after three commits"
- 1202–1211 §9.2 "what a crash sees"
- 1071–1090 §7.4 worked layer-record payload hex box
- 1996–1997 §15.1 tile-index region box
- 3093–3097, 3109–3113, 3133–3136 §20.3 "three shapes a commit takes" (a)(b)(c)
- 3275–3281 §20.5 "what compaction reclaims"
- 4066–4075 Appendix A hex dump

### 1.4 Worked numeric examples

513 (§4.6 `température`), 577 (§5.1 smallest file), 1060 (§7.4 layer record), 1518 (§11.2 grid),
1572 (§11.4 ordinals), 1635 (§12.1 bfloat16), 1684 (§12.3 channel entry), 1754 (§13.3 fill),
1875 (§14.2 offsets), 1909 (§14.3 packed bool), 1965 (§14.5 padding), 2089 and 2104 (§15.4
segments), 2203 (§16.2 slabs), 2384 (§17.3 byte-shuffle), 3079 (§20.3 supersede cost).

### 1.5 Checklists and enumerated lists

Appendix C (registry snapshot), Appendix D (six choices), Appendix F (normative references),
Appendix G (reproducible-writer profile, items 1–10), Appendix H (four conformance checklists);
plus the numbered procedures `[R-LIF-02]` steps 1–6, §10.1's four vehicles, §19.1's four open
steps, §19.4's eight tile-read steps, §20.3's six appender steps.

---

## 2. Arithmetic I did myself

I refused to eyeball anything. Every checksum in the document was recomputed from a CRC-32C
implementation I wrote from `[R-ENC-09]`'s parameters (Castagnoli 0x1EDC6F41, reflected in and
out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), which I first validated against §4.5's own check
vector before trusting it on anything else.

```
CRC32C("123456789")            = 0xE3069283   spec §4.5 says 0xE3069283      OK
CRC32C(zero bytes)             = 0x00000000   spec §4.5 says 0x00000000      OK
CRC32C(4 sentinel entries, 80B)= 0x80A34955   spec §7.4 says 0x80A34955,
                                              stored `55 49 A3 80`           OK
CRC32C(`55 49 A3 80`)          = 0xC4EE982E   spec §7.4 crc_of_crc_array     OK
CRC32C(2^16 sentinel entries)  = 0xEECB3BB2   spec §15.4 / App. B constant   OK
CRC32C(App. A trailer[0,60))   = 0xE00938D2   App. A says `D2 38 09 E0`      OK
```

All six reproduce exactly. That is the strongest single piece of evidence that these figures
have been maintained rather than copied.

**Appendix A hex dump, byte by byte.** I decoded the dump at lines 4067–4074 against §6.1,
§6.2 and §7.1 without consulting the annotation table, then compared:

- `[0,8)` = `89 54 41 52 4E 0D 0A 1A` = 0x89, "TARN", CR, LF, ctrl-Z — matches §6.1 exactly.
- `[8,16)` = zero — §6.1's second row.
- `[16,20)` = `00 00 00 00` — dir_offset 16, dir_length 4; the region is a zero-byte record
  sequence plus CRC-32C of zero bytes = 0x00000000. Consistent with §7.1's "Its final 4 bytes
  are a CRC-32C over the preceding dir_length − 4 bytes".
- `[20,64)` = 44 zero bytes. 64 − 20 = 44 — the annotation says 44. Correct.
- Trailer field map, computed from §6.2's offsets added to 64:
  magic [64,72); version_major [72,74)=1; version_minor [74,76)=0; flags [76,80)=0;
  generation [80,88)=1; dir_offset [88,96)=16; dir_length [96,104)=4;
  committed_file_length [104,112)=128; file_id [112,120)=0x0123456789ABCDEF;
  reserved [120,124)=0; CRC [124,128)=0xE00938D2. Every row of the annotation table at
  lines 4079–4093 matches, including the little-endian reading of file_id.
- §6.2's field offsets sum: 8+2+2+4+8+8+8+8+8+4+4 = 64, contiguous from 0 with no gap and no
  overlap. `[R-CNT-24]`'s claim "The format-major-1 trailer has zero slack: every byte is
  assigned" holds. Its other claim — that a future major may redefine "only the remaining 48
  trailer bytes" — also checks: the permanently fixed bytes are [0,8) magic, [8,12) the two
  version fields, [60,64) CRC = 16 bytes, leaving 48.
- The minimum-size argument of `[R-CNT-27]`: minimise F subject to dir_offset ≥ 16,
  dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, F mod 64 = 0. F = 64 fails (20 ≤ 0);
  F = 128 works (20 ≤ 64). 128 is correct.
- §6.1 vs §6.2 magic first bytes: 0x89 vs 0x8A. §6.2's Note ("The trailer magic's first byte
  differs from the front signature's, so a recovery scan (§9.6) never matches the front block")
  is correct.

**§7.4's worked layer-record payload.** I laid out the fields from the table at lines 1006–1023
independently and got the same offsets as the hex box:

```
 0  name (u8 len 3 + "sst")            -> 4    (4 bytes)
 4  layout u8                          -> 5
 5  linearization u16                  -> 7
 7  codec u16                          -> 9
 9  filter u16                         -> 11
11  alignment A u64                    -> 19
19  slab S u64                         -> 27
27  A_slab u64                         -> 35
35  rank d u8                          -> 36
36  channel count C u16                -> 38
38  dim entry: 1+1 name, 8 extent, 8 T -> 56   (18 bytes)
56  chan entry: 1+4 name, 2 type, 1+4 fill -> 68 (12 bytes)
68  index_encoding u8                  -> 69
69  entry_count u64                    -> 77
77  crc_of_crc_array u32               -> 81
```
Total 81. The prose's accounting — "Name and the nine scalars from layout through channel count
occupy 4 + 34 bytes, the dimension entry 18, the channel entry 12, and the trailing fixed
fields 13 — 81 exactly" — checks: the nine scalars are layout(1)+linearization(2)+codec(2)+
filter(2)+A(8)+S(8)+A_slab(8)+d(1)+C(2) = 34, and there are exactly nine of them; trailing
fixed = 1+8+4 = 13; 4+34+18+12+13 = 81.

`[R-CNT-17]`'s extent length: 4 × 20 + ⌈4/2^16⌉ × 4 = 80 + 4 = 84 — the example says 84.

I then **built the file**, not just the record: a complete 448-byte one-layer TARN file with
tile 0 actually stored under codec 1 / filter 1, an index region of 84 bytes, a directory of
109 bytes, a 47-byte pre-trailer pad and a valid trailer. The inline payload came out at 81
bytes, `[R-CNT-17]`'s formula reproduced 84, F mod 64 = 0, dir_offset + dir_length ≤ F − 64,
and a hand-written `[R-LIF-08]` coverage walk over the five claimants (front block, tile
extent, index region, directory, trailer) found them pairwise disjoint with a slack total of
exactly 47 — the pad. Nothing in Part I forced me to guess.

**Every other worked example, recomputed:**

- §11.2: (1024,2048)/(256,256) -> G=(4,8), N=32, P=65,536. With E_y=1000, ⌈1000/256⌉ = 4. OK.
- §11.4: tile (1,0) -> 1·8+0 = 8. (300,700) -> tile (1,2), s = 1·8+2 = 10, in-tile (44,188),
  ordinal 44·256+188 = 11,452. Planar C=4, channel 2 -> 2·32+10 = 74. All OK.
- §12.1: bfloat16 1.0 = high 16 bits of 0x3F800000 = 0x3F80, stored `80 3F`. OK.
- §12.3: `04 74 65 6D 70 0C 00 04 00 00 C0 7F` = len 4, "temp", type 12 LE, fill len 4,
  0x7FC00000 LE. Twelve bytes. OK.
- §4.6: "température" NFC = 12 bytes (é = C3 A9); NFD = 13 (65 CC 81). OK.
- §14.2: (2,3) P=6, uint8+uint16 -> Q=3, size 18; ordinal 5 at 15, `a`@15, `b`@16–17.
  Planar `b` = 12 bytes, ordinal 5 at 10–11. float32+bool -> Q=5, size 30, ordinal 5 at
  [25,30), `t`@25–28, `m`@29. Checked against the table's `(k div C)·Q + F_{k mod C}` with
  k = u·C + c: for u=5,c=1 -> k=11, (11 div 2)·5 + 4 = 29. OK.
- §14.3: P=10 alternating from true -> byte 0 bits 0,2,4,6 set = 0x55; byte 1 value 8 true,
  value 9 false -> 0x01; pad bits 2–7 set -> 0xFD. `55 01` / `55 FD`. ⌈10/8⌉ = 2. OK.
- §14.5: (5,5)/(4,4) -> grid 2×2; edge tile (1,1) covers 4–7 on both axes; exactly one real
  position (4,4) and 15 padding; one uint16 channel -> 16·2 = 32 bytes; values 1–15 each
  `CD AB`. OK.
- §15.4 first example: 1,000,000 entries -> ⌈1e6/65536⌉ = 16 segments, last covers
  1,000,000 − 15·65,536 = 16,960; CRC array 64 bytes; region 20,000,064 bytes; k=999,999 in
  segment 15 at relative byte 20·16,959 = 339,180; array at [20,000,000, 20,000,064);
  segment 15 at [19,660,800, 20,000,000) = 339,200 bytes ≈ 339 KB; a full segment is
  65,536·20 = 1,310,720 = 1.25 MiB. Every figure OK.
- §15.4 second example: disk ordinal 74 -> region bytes [1480,1500) = 74·20. Channel 3's block
  is [96,128) = 32 entries. OK.
- §16.2: N=32, S=8 -> runs [0,8),[8,16),[16,24),[24,32); under row-major with G=(4,8) tile
  rows 1–2 are ordinals 8–23 = runs 1 and 2 exactly. OK.
- §17.3: 1.0f/2.0f/3.0f = `00 00 80 3F 00 00 00 40 00 00 40 40`; s=4, n=3; byte i of group j
  to offset i·n+j gives `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Matches the document
  character for character. I also verified the stated inverse "restores byte i·n+j to offset
  j·s+i" is the true inverse: with k = i·n+j, i = k div n and j = k mod n, so the target is
  (k mod n)·s + (k div n). Correct. And "L is divisible by s in every case" holds for all
  three cases (P·B^c / B^c, P·Q / Q, ⌈P/8⌉ / 1).
- §20.3: 32·20 + 4 = 644. OK.
- §21.9's Note: 2^32 entries / 2^16 per segment × 4 bytes = 2^18 = 256 KiB; at 2^36 it is
  2^22 = 4 MiB; 65,536 layers × 200 bytes = 12.5 MiB exactly. All OK.
- §19.4's planar Note: entries for one spatial ordinal are N apart; two ordinals share a
  segment only if they differ by < 2^16, so N ≥ 2^16 does guarantee different segments. OK.
- §17.2's zstd Note: §14.2's examples give 18 and 30 bytes, §14.3's gives 2 — all below 1 KiB,
  so the Window_Descriptor floor argument applies to exactly the tiles it names. OK.

**Register arithmetic.** §21.8 asserts "121 conditions over 277 instances". I parsed the four
register tables mechanically, took §21.1's own counting rule ("Instances within a cell are
separated by semicolons, and a cell reading — is one instance"), and got:

```
21.2: 36 rows,  58 instances
21.3: 49 rows, 116 instances
21.4: 26 rows,  55 instances
21.5: 10 rows,  48 instances
TOTAL 121 rows, 277 instances
```

Exactly the claimed numbers. I also checked every row has six cells, every Detector is
`reader` or `verifier`, and every Detected cell uses only §21.1's five-term vocabulary
(open / layer access / tile use / extent use / certification). All clean.

**Cross-reference integrity.** Every `§N` and `§N.M` reference in the document resolves to a
heading that exists (102 distinct references, zero dangling). Every `Appendix X` reference has
a heading. Every register row label cited in prose (F1, F6, F7, F8, F14, F18, F35, F36, L18,
L24, L25, L31, L33, L34, L36, L40–L45, L48, R1, T2–T5, T14, T15, T17, T23–T26, ...) exists as
a row. Requirement identifiers: 19 prefixes declared in §2.2, 19 used, none undeclared and
none unused; every prefix's numbering is gapless (`ENC` "gaps" 17–99 are an artifact of §2.2's
own illustrative `[R-ENC-100]`, and `SER-04`'s withdrawal is why `SER` shows no gap — §14.4's
Note keeps the identifier visible).

I found no arithmetic error anywhere in the document.

---

## 3. Row-by-row completeness audits I ran

### 3.1 §7.4's field constraints against §21.3

I walked every field of §7.4's inline-payload table and asked which register row witnesses its
violation. name -> L3/L5/L6/F4; layout -> L36; linearization -> L33; codec -> L43; filter ->
L45; A -> L39; S -> L1; A_slab -> L28/L29; d, C -> L32; dimension entries -> L4/L7/L8/L9/L1/
L32; channel entries -> L4/L7/L8/L9/L34/L30/L35; index_encoding -> L31; entry_count -> L21/L1;
crc_of_crc_array -> L27/L37; sub-records -> L10–L14/L19/L24/L25/L26/L46/L47/L49. Plus L20
(`[R-CNT-16]`), L22 (`[R-CNT-17]`), L23 (`[R-CNT-18]`), L15–L17 (`[R-CNT-13]`), L18, L2, L40–L42,
L44, L48. That accounts for L1 through L49 with no field left unwitnessed and no row left
unattached.

### 3.2 §15.3 against §21.4

§15.3 says "Six rows are marked *structural*". I counted the table: crc≠0 sentinel; exactly one
half sentinel; length 0; offset < 16; offset or length > 2^63−1; offset+length overflow or
> F−64. Six. They map onto T6, T7, T10, T8, T11, T12/T9 with no residue, and §15.3's three
verifier rows map onto L18, F33 and L40/L41/L42. `[R-COD-02]`–`[R-COD-10]` map onto
T13–T26. Complete in both directions.

### 3.3 F33's "caught instead by" list

F33 disclaims the front-block and trailer cases, redirecting to "F9/F10, F31/F32, L16/L17 and
T8/T9, each at its own tier". I enumerated the claimant kinds §9.7 names — the directory, each
record's extent, each non-sentinel entry's stored extent, plus front block and trailer — and
each has exactly one bounds pair: directory -> F9/F10; non-layer top-level record extent ->
F31/F32; layer record and sub-record extents -> L16/L17; stored-tile extents -> T8/T9. The
redirect is complete and non-overlapping.

### 3.4 §21.6's twenty verifier rows against Appendix H

The register has exactly 20 verifier-detected rows: F7, F25–F28, F33, F36, L18, L25, L40–L42,
L46–L49, T2, T4, T5, T26. Appendix H's verifier checklist covers all twenty: coverage/slack
(F33, L18 via "extent overlap"), flag bits (F25, F26, F28, L46, L47, L49), front block (F1,
F6), F7, F36/L25, alignment and slab (L40–L42), decoded content (T2, T4, T5, and T26 which
"the check that detects it is T2's or T4's"), member ordering (F27, L48). No verifier row is
missing from the checklist.

### 3.5 Every "N things" claim in the document

§2.3 five conformance classes -> 5 bullets. §4.6 three name constraints -> 3. §10.1 four
vehicles -> 4. §12.1 thirteen sample types -> 13 table rows, IDs 1–13. §15.3 six structural
rows -> 6. §17.2 "Three frame features are excluded" -> dictionary, content-checksum flag,
over-large window = 3. §18.2 "Four restrictions apply" -> 4 bullets. §20.5 "four obligations
on a compacted file's trailer" -> file_id, generation, ignore-lane bits, version_minor = 4.
§21.2 "36 conditions" / §21.3 "49" / §21.4 "26" / §21.5 "10" -> all exact. §22.2 "Three
properties" -> 3. §22.3 "Four residues" -> 4. Appendix D "Six choices" -> 6. Every count is
right.

### 3.6 §20.5's row list

The changed §20.5 passage claims: "F36 and L25 for a record type, and one row for each of the
other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates eight
spaces. Excluding record type leaves seven: channel layout (L36), linearization (L33), sample
type (L34), codec (L43), filter (L45), index encoding (L31), metadata encoding (R1). Seven
rows, one per space, each correctly matched. The word "tabulates" is doing real work here —
it excludes the trailer flag lanes, which §10.2's prose calls a space but does not put in the
table. The list is correct.

### 3.7 §10.2's table against the owning sections

Every row's Assigned/Reserved/Experimental partition matches the section that owns the space:
record type (§7.3, `[R-CNT-15]`), channel layout (`[R-SER-06]`: 3–255 reserved, no
experimental), linearization (`[R-GEO-05]`: 2–3 and 4–0x7FFF reserved -> 2–0x7FFF),
sample type (`[R-TYP-03]`: 14–19 and 20–0x7FFF -> 14–0x7FFF), codec (`[R-COD-03]`),
filter (`[R-COD-09]`), index encoding (§7.4), metadata encoding (`[R-MTA-03]`). Appendix C
restates all of them consistently. "Value 0 is invalid in every space above" holds in every
owning section.

### 3.8 The ASCII figures against their prose

- §5.1 "three commits": commit 1 writes front + A + dir1/pad/tr1; commit 2 writes B +
  dir2/pad/tr2; commit 3 writes dir3/pad/tr3. That places the two hatched runs exactly where
  the figure draws them and matches the caption "The ▓ runs are the directories, pads and
  trailers of commits 1 and 2". Consistent. The figure's own disclaimer ("The grouping under
  the box is illustrative: a layer's structures need not be contiguous or ordered
  (`[R-SLB-05]`)") correctly stops a reader from over-reading it, and it points at §20.5's
  figure for the general case — which does indeed draw A's tiles and A's index separated.
- §9.2 "what a crash sees": row 2's hatch is the partial write past trail_n; row 3's hatch
  replaces dir_n/pad/trail_n. Both match the legend and `[R-LIF-05]`.
- §20.3 (a)(b)(c): (a) hatches exactly dir1/pad/tr1 and leaves A untouched, matching "A's
  record is carried into dir2 byte-identically, extent slot and all"; (b) hatches the old
  index and the old dir/pad/tr and shows index′ at the same width, which is right because
  adding tiles inside an existing grid leaves entry_count and therefore extent_length
  unchanged; (c) hatches only dir1/pad/tr1. All three are consistent with `[R-WRT-04]` and
  `[R-WRT-05]`.
- §20.5 "what compaction reclaims": input has file_id X / generation 7, output file_id Y /
  generation 1, matching `[R-WRT-06]`'s "fresh file_id ... and generation 1". The ′ marks are
  explained. Consistent.

I checked the drawing convention across all of them: `pad` is drawn as its own box and is
never hatched, yet §5.1 states in terms that "the pad and the ▓ runs are slack". So the
convention is stated once and used consistently — a reader who takes §20.5's unhatched output
`pad` for a non-slack region has read past §5.1, not past a defect. I considered filing this
and decided against it.

---

## 4. Where I had to guess, and where I did not

Building the file end to end, the only places I had to supply reasoning the document does not
state outright:

1. **Inverting the planar disk ordinal.** §11.4 gives the forward map `c·N + s`; a verifier
   walking every entry of a planar layer needs `c = k div N` to know which channel's element
   size fixes that plane's decoded size (for `[R-COD-04]` and `[R-COD-07]`). The document never
   writes the inverse. It is forced — §11.4 constrains `0 ≤ s < N` and §15.1 says "entry order
   is disk-ordinal order, so a planar layer's entries group channel-major" — so I did not
   count this as a guess. A reader never needs the inverse at all, because §19.4 step 2 goes
   forward from the requested channel.
2. **The identifier that owns §20.4's preservation table.** The table at lines 3164–3166 sits
   between `[R-WRT-05]` and `[R-WRT-08]` with no identifier of its own. §2.4's
   preserve-verbatim row cites it as "§20.4's table" (a prose position), and §21.6 cites it as
   `[R-WRT-08]`. Since no register row and no vector turns on it, I did not report this; it
   costs nothing to an implementer and nothing to a corpus.

Everything else in Part I and Part II I could build from the document alone. That is a real
result and I want to state it plainly: the container, the geometry, the tile serialisation,
the index, the codec pipeline and the register are all implementable from this file without
recourse to anything outside it.

---

## 5. Findings

### diagrams-01 — AMBIGUITY — `[R-LIF-02]`'s commit protocol is in none of the three places this document puts a writer obligation

**Location:** §21.7 `[R-ERR-01]`; §2.3 `[R-CNF-02]`; §9.2 `[R-LIF-02]`.

**Quotation (§21.7, the passage that enumerates the class):**

> A second set of obligations is omitted from the register because a
> single file exhibits no witness of their violation. Committed-prefix
> immutability and the generation sequence (`[R-LIF-01]`,
> `[R-LIF-03]`) are properties of a file's history, which §9.7 does
> not reconstruct;

**Quotation (§9.2, the obligation itself and the document's own statement that it can be violated):**

> A writer performing a commit MUST, in order: (1) begin writing at
> exactly F (§9.4); ... (3) append the new complete directory —
> re-emitting every retained record per §20's preservation rules —
> followed by its CRC; (4) make steps 1–3 durable ...

> **Note.** Step 3 is not discharged by a directory an earlier
> generation appended: each commit appends its own complete
> directory, and the trailer of step 5 addresses that one. A writer
> that re-points a new trailer at a prior generation's directory
> region has left step 3 unperformed.

**Quotation (§2.3, the only mechanism by which a writer MUST escapes file conformance):**

> A few obligations this specification places on writers govern their
> *conduct* rather than their output — where a value is published, or
> which registry version a writer targets (§10.3, §18.3) — and a file
> is never nonconforming by virtue of one ... A writer obligation whose
> violation this specification expressly declares not to be a
> file-conformance violation binds the actor in the same way; §6.3's
> flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap
> longer than `[R-LIF-02]` step 5's pad are the cases this text
> states, and each is declared where it arises rather than
> enumerated here.

**The problem.** A file whose live trailer names generation *n+1* while its `dir_offset` points
at the directory region appended by commit *n* violates `[R-LIF-02]` step 3 — the document says
so itself, in the Note quoted above. That file has no witness: slack content is unconstrained
(`[R-CNT-21]`), so nothing distinguishes a re-pointed prior directory from a freshly appended
one, and §9.7 "does not reconstruct" history. So the violation is undetectable and rightly
absent from §21.2–§21.5.

But it is then absent from everywhere it could live:

- It is not in §21.7's second-set enumeration. That list names `[R-LIF-01]`, `[R-LIF-03]`,
  `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`, `[R-CNT-18]`, §20.3 step 4, §20.5's four trailer
  obligations, and `[R-ENC-06]`. `[R-LIF-02]` appears nowhere in §21.7.
- It is not a conduct rule under §2.3's first mechanism: step 3 is not about publication or
  about which registry version a writer targets.
- It is not covered by §2.3's second mechanism either: that mechanism requires the
  specification to "expressly declare" the violation not to be a file-conformance violation,
  and §2.3 names the only two such cases this text states — neither is `[R-LIF-02]` step 3.
  (§2.3 does mention `[R-LIF-02]` step 5, but only to define the *pad* against which §6.2's
  over-long gap is measured, not to exempt step 3.)

**Permitted readings.** (a) `[R-LIF-02]` step 3 states a file-level requirement. Then §21.7's
account — which §21.1 calls "the account, by class, of what fails" the detectability gate —
is incomplete, and an implementer who trusts it will conclude that a witness for step 3 must
exist somewhere in §21.2's file-scope rows. It does not. (b) `[R-LIF-02]` step 3 binds only
the writer's conduct. Then §2.3's machinery — which is explicit that conduct cases are
"declared where [they arise]" — should say so at §9.2, and does not; and §5.1's `[R-CNT-01]`
("a commit appends its own directory, pre-trailer pad, and trailer last, in that order (§6.2,
`[R-LIF-02]` steps 3 and 5)") reads it back into the file's anatomy, pulling against reading (b).

**Which I picked and why.** (a). §21.7 names `[R-LIF-01]` — a rule of exactly the same shape
(a per-commit obligation about bytes, unwitnessed in one file) — as belonging in its second
set, so the document itself classifies this family as file-level-but-unwitnessed rather than
as conduct. `[R-LIF-02]` belongs beside it. The same reasoning covers step 1 ("begin writing
at exactly F") only insofar as `[R-LIF-01]` already witnesses it; step 3 and the two barriers
of steps 4 and 6 are not covered by any named rule.

**What an implementer does wrong without this.** A verifier author reading §21.1's
"completeness is normative" together with §21.7's list concludes that everything not in §21.7
is either in the register or not a requirement, and therefore that a trailer pointing at an
older generation's directory must be caught by some F-row. They will go looking for the check
and find none, and either invent one (rejecting conforming files whose slack happens to
contain a directory-shaped region) or conclude the register is broken. A writer author reading
§2.3's conduct machinery concludes the opposite — that step 3 is optional in the way
`[R-EXT-03]`'s publication ban is — and re-points trailers at old directories to save a write.

**Byte-level:** No. Whichever way it resolves, `[R-LIF-02]` still binds writers, no register
row is added or removed, and no reader or verifier check changes: the condition has no
file-level witness by construction, so no two implementations can disagree about a byte or a
verdict on any file handed to them. It costs an implementer a wrong model of what the register
promises, not a divergent output.

---

### diagrams-02 — CONTRADICTION — Appendix H's verifier checklist demands a partial slack total in the one case `[R-CNT-21]` expressly says no total is owed

**Location:** Appendix H, "Conforming verifier" entry; §5.2 `[R-CNT-21]`.

**Quotation (Appendix H):**

> **Conforming verifier** — every reader obligation, plus the checks
> readers are exempt from: the live-state coverage partition and the
> slack total (§9.7) — reported as partial — an upper bound,
> naming the scope or violation that stopped the walk — where its walk
> did not complete (`[R-CNT-21]`);

**Quotation (§5.2 `[R-CNT-21]`):**

> Where §6.2's ordered validation rejects the file before a live trailer
> is established there is no F and no live state to walk, so the total is
> not owed at all: the verifier reports the trailer failure and
> nothing about slack, which is not a partial total but the absence of
> one.

**The problem.** `[R-CNT-21]` distinguishes three states, and spends four lines insisting on
the third: a complete total; a partial total ("F less the bytes claimed by the claimants the
walk did enumerate"); and *no total at all*, where the trailer gates fail and there is no F.
Appendix H's entry collapses this to two. Its condition is "where its walk did not complete",
and a walk that never began because the trailer failed its magic, its CRC or its field gates
(F8, F14, F9–F17) is on its face a walk that did not complete. So the checklist as written
directs a verifier to report a partial total in exactly the case the rule says none is owed —
and a partial total is not computable there, since it is defined as *F less the claimed bytes*
and there is no F.

§21.6's slack row has the same two-way shape ("counted and reported by a verifier — as a
partial total — an upper bound naming what stopped the walk — where its walk did not
complete"), but that row is a *condition* row predicated on slack existing, which presupposes
a live state; it is defensible. Appendix H's entry is not predicated on anything.

**Which reading I picked.** The rule governs. Appendix H says so itself — "each entry's
authority is the requirement or section cited, never this summary" — and its citation is
`[R-CNT-21]`, which decides it. So only the checklist is wrong. I record it because the
checklist is what an implementer audits against, and because the distinction it drops is one
the rule went out of its way to make.

**What an implementer does wrong without this.** A verifier that follows the checklist emits,
for a torn file, a diagnostic pairing "trailer magic mismatch" with a slack figure it computed
from the physical file length rather than from F — a number `[R-CNT-21]` says is "not a partial
total but the absence of one". §22.3 makes that number load-bearing ("the slack total ... is
the number that distinguishes a working file from a padded one"), so a fabricated one is worse
than none.

**Byte-level:** No. Appendix H is labelled non-normative and disclaims its own authority in its
first sentence, and `[R-CNT-21]` decides the case. No file's conformance and no verdict on any
file changes; what changes is one line of a verifier's report.

---

### diagrams-03 — OBSERVATION — §21.6's trailer-mimic row justifies its verdict with a clause that does not apply to the condition it states

**Location:** §21.6, the "payload contains a byte string that mimics a trailer" row.

**Quotation (§21.6):**

> | A payload contains a byte string that mimics a trailer | Inert:
> nothing enumerates slack, and a recovery tool re-verifies its output
> whole (§9.6) — which catches any mimic that is not itself a
> consistent generation; §9.6's second caution covers the rest |
> `[R-LIF-06]` |

**Quotation (§22.3 `[R-SEC-04]`, where the two cases are kept apart):**

> And a payload can contain a byte string that mimics
> a trailer; recovery tooling that scans backward can land on one, which
> is why recovery output is re-verified as a whole file before being
> trusted (`[R-LIF-06]`) before any use. Under live-state coverage a
> mimic in slack is inert — nothing enumerates it — but a recovery
> tool that truncates to one produces a different file, which is why
> its output is re-verified whole.

**The problem.** §22.3 keeps two cases distinct: a mimic *in slack*, which is inert because
"nothing enumerates it", and a mimic *in a payload*, which is a live-state structure that the
coverage walk very much does enumerate (as that entry's stored extent, §9.7) and which is inert
for a different reason — `[R-LIF-05]` forbids a reader to scan backward, and `[R-LIF-06]`
obliges a recovery tool to re-verify whole. §21.6's row states the *payload* condition and then
offers the *slack* justification. Its second clause is the right one and its cited rule is the
right one — `[R-LIF-06]` says in terms "a tile payload can deliberately contain a byte string
that mimics a valid trailer" — but its first clause belongs to the other case.

I decided it this way: the verdict "Inert" is correct for both cases, and the row's cited rule
is correct, so nothing turns on it beyond the reasoning a reader will carry away. The cost of
deciding it is having to reconcile §21.6, §22.3, §6.2's Note and §9.6 to see that "nothing
enumerates slack" was never an argument about payloads — which is why I file it as an
OBSERVATION rather than as a contradiction.

**What an implementer does wrong without this.** A verifier author takes the row to mean that
trailer mimics are a slack phenomenon and skips §6.2's Note, which describes the case that
actually bites: "A payload byte-string that mimics a trailer and happens to sit at exact
physical end of file can pass every check above; it is caught at the directory CRC (§7.1)". A
recovery tool author takes it to mean that a backward scan only ever lands on mimics in slack,
which is precisely the assumption `[R-LIF-06]`'s first caution exists to break.

**Byte-level:** No. The row's outcome (inert, no violation) matches `[R-LIF-06]`, and §21.1
already fixes that "where such an entry and the rule it cites diverge, the rule governs". No
byte a writer may emit and no verdict a reader must reach depends on the justification clause.

---

### diagrams-04 — OBSERVATION — §4.7's presentation contract mis-states which columns §7.4's layout table omits

**Location:** §4.7's Note (the document's contract for how layout tables are presented); §7.4's
inline-payload table.

**Quotation (§4.7):**

> **Note.** Layout tables for fixed-layout structures give, per field:
> byte offset within the structure, size, type, name, taxonomy class,
> and valid range, each table giving the columns its structure needs.
> A packed variable-length payload — the layer
> record's inline payload (§7.4) — has no fixed offsets to give; its
> table omits the offset and class columns, and each field's class
> follows from the definitions above.

**What §7.4 actually delivers (lines 1006–1007):**

> | Field | Type | Constraint |
> |---|---|---|

**The problem.** The contract names six columns: offset, size, type, name, class, valid range.
§7.4's table delivers three — Field (= name), Type, Constraint (= valid range). It therefore
omits offset, class **and size**. The Note names two of the three omissions. I checked the other
five layout tables against the same contract: §6.2, §15.1 and §18.2 deliver all six; §6.1
delivers offset/size/value/class, which the Note covers explicitly ("§6.1's block is a 16-byte
constant, where a Value column replaces type and range"); §7.2 delivers five, which the Note
also covers ("§7.2 folds each field's range into its Field cell"). §7.4 is the only table whose
omissions the contract states incompletely.

The best defence I can construct for the text is that the reason given — "has no fixed offsets
to give" — extends to size for the same reason, since `name (u8 len + bytes)` and the dimension
and channel entries have no fixed size either. That defence is sound but it is reasoning the
Note does not supply, and the Note supplies the analogous reasoning for §6.1 and §7.2
explicitly rather than leaving it to the reader.

**What an implementer does wrong without this.** Nothing to the bytes: the Type column carries
each fixed field's width (`u8`, `u16`, `u64`) and §4.2 fixes those widths normatively. What it
costs is a reader auditing the document's own presentation discipline — the discipline the
opening "How to read this document" block advertises — who finds a table that departs from the
contract in a way the contract does not acknowledge, and has to work out whether the departure
or the contract is the error.

**Byte-level:** No. Field widths are fixed by §4.2 and `[R-ENC-06]` regardless of which columns
a table prints; §7.4's Type column gives every width unambiguously. No two implementations can
read a different width out of this.

---

## 6. Things I checked and did not report

For the record, and so a reader can see where I decided against filing:

- **§21.2's preamble, "the rows below whose subject is that file's *geometry* do not reach it".**
  The restrictive clause narrows the claim to a subset, while the justification given (§6.2 puts
  the version gate ahead of everything but magic and CRC) supports all 32 non-excepted rows,
  including ones whose subject is plainly not geometry (F27's JSON member ordering, F24's type
  0). But the following sentence — "Four rows are outside that reasoning and do reach it" —
  makes the intended dichotomy (major-1-specific structure vs. fields fixed across every major)
  recoverable, and I verified the four named rows are exactly the ones `[R-CNT-24]` fixes across
  majors. Editorial, not reportable.
- **R8's Instances cell** enumerates two containers where R5, R6 and R7 enumerate alternatives ×
  containers, so a corpus builds 2 vectors for "non-finite number" rather than 8. But R8's
  condition text says "in any form ... alike", which is exactly §21.1's licensed device for a
  family that does not change the condition's shape ("T24's *any codec*"), and §21.1 makes the
  cell's judgement final ("the count is therefore mechanical once the cell is written"). Not a
  defect.
- **§20.5's "so slack is never carried"** together with an output figure whose legend says
  "▓ marks slack" and which draws an unhatched `pad`. A compacted file does contain slack — the
  pre-trailer pad, and alignment gaps under a declared A or A_slab. But "carried" reads as
  carried *forward from the input*, which is true, and §5.1 states the drawing convention for
  all these figures in terms ("the pad and the ▓ runs are slack"). Not a defect.
- **Appendix H's reader checklist never mentions the front signature block**, while the verifier
  entry files that check under "the checks readers are exempt from" — yet `[R-CNT-04]` makes it
  a reader MUST whenever [0,16) is resident, and F1/F6 carry Detector *reader*. I was ready to
  file this until I noticed the reader checklist's catch-all, "detects every reader-assigned
  violation no later than its tier (§19.2)", which reaches F1 and F6 generically, and that the
  verifier entry's own parenthetical is precise ("which `[R-CNT-04]` lets a reader **not holding
  it resident** defer or omit and §2.3 does not"). Not a defect.
- **§21.6's "The file contains zero layers | A conforming file with an empty directory"** — a
  file with zero layer records and one top-level user-metadata record has zero layers and a
  non-empty directory. But `[R-CNT-14]`, the rule the row cites, uses the same shorthand ("zero
  is valid: an empty directory is a conforming generation"), so the row does not diverge from
  its rule. Not reportable under §21.1's own standard.
- **§17.2's Note, "Resource limits are §21's subject", for the unbounded ratio between a stored
  tile's length and its decoded size.** §21.9 has no row bounding a stored extent's length, so
  `[R-ERR-04]`'s "Software that declines **on that ground** a file whose every quantity lies
  within the table is not a conforming reader" appears to oblige a reader to fetch an
  arbitrarily large stored extent for a small tile. I worked through it: the amplification
  factor is at most 1, because `[R-CNT-13]` and T9 bound every extent by F − 64, so the attacker
  pays for every byte the reader reads, and §22.2's three properties hold as stated. It is a
  design choice, not an ambiguity — the text decides it — so it is not a finding.
- **§20.4's table carries no requirement identifier of its own**, while the "How to read this
  document" block says "test vectors cite those identifiers rather than prose positions". No
  register row and no vector turns on an updater preservation obligation (they are
  history-dependent and unwitnessed), so nothing is left uncitable. Not reportable.

## 7. Bottom line

Four findings, none byte-level. I could not construct two conforming implementations that
disagree about any byte on disk or any accept/reject verdict on the strength of anything in a
figure, layout table, worked example, register cell or checklist in this document. Every
checksum, every offset, every width, every derived product and every "N things" count in the
document reproduces under independent computation. The defects I do report are all of one
shape: an enumeration or a summary that is narrower or wider than the rule it stands for, in a
document that has made those enumerations load-bearing.
