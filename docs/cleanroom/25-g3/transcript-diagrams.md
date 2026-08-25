# Round 25 — Diagram auditor — working transcript

## 0. Access disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,477 lines, read in full in five chunks). I ran `wc -l` and one `grep` over
that same file, plus two local Python scripts that read no files (a CRC-32C
implementation and a mechanical instance-counter that re-reads the spec text
through `open()` — that is still the one permitted file). I opened no ADR, no
`docs/`, no `conformance/`, no `registry.json`, no git history, no web page,
and I listed no directory.

Context I did not ask for **did** appear before I began: a `claudeMd` block
naming `AGENTS.md`, and an index of the maintainer's auto-memory listing six
note titles (one of which names a specific register row identifier and an ADR
number). I did not open any of those files, and I have disregarded their
contents. One of those titles brushed against a row I was independently
examining (R8); I note below, at that finding, that I reached it from §21.1's
own instance-counting rule and from R-MTA-04's bullet text, and I have said so
explicitly so a reader can discount it if they prefer.

Paths: the spec was exactly where the brief said it would be.

---

## 1. Method

The charter is figures. I did three passes:

1. **Enumerate.** Grep out every table row, fenced block, Example, Note and
   Rationale with line numbers, so coverage is checkable.
2. **Arithmetic.** Recompute every number: CRCs, offsets, widths, grid counts,
   ordinals, decoded sizes, region lengths, instance counts.
3. **Scope.** For each figure, ask whether it illustrates the rule, a narrower
   rule, or a wider one; whether its label (normative / Note / Example /
   Rationale) matches how the surrounding text leans on it; and whether any
   promise of completeness it makes is kept.

Then I built a file end to end on paper (§4 below) to find the places where I
had to guess.

---

## 2. Inventory of figures, with line numbers

Layout / byte tables (normative):
- §2.4 outcome class table — L235–241
- §6.1 front signature block — L697–700
- §6.2 trailer — L740–752
- §7.2 record header — L904–910
- §7.3 record types — L977–980
- §7.4 layer-record inline payload — L1006–1023
- §8.1 checksum coverage map — L1123–1131
- §10.2 numeric identifier spaces — L1397–1406
- §12.1 sample types — L1604–1618
- §14.2 byte layout / decoded size — L1836–1839
- §15.1 index entry — L2004–2008
- §15.3 entry validity — L2052–2064
- §18.2 metadata encoding — L2444–2446
- §18.4 standardized keys — L2634–2641
- §20.4 preservation obligations — L3170–3174
- §21.2 file-scope register — L3432–3469 (F1–F36)
- §21.3 layer-scope register — L3476–3526 (L1–L49)
- §21.4 tile-scope register — L3533–3560 (T1–T26)
- §21.5 ignored-record register — L3583–3594 (R1–R10)
- §21.6 non-violations — L3601–3616
- §21.9 minimum guarantees — L3740–3749

ASCII region diagrams (all inside Examples, non-normative):
- §5.1 "a file after three commits" — L584–616
- §9.2 "what a crash sees" — L1198–1220
- §20.3 "the three shapes a commit takes" (a)(b)(c) — L3096–3148
- §20.5 "what compaction reclaims" — L3290–3321

Worked examples (non-normative unless noted):
- §4.6 `température` NFC/NFD — L513–517
- §5.1 smallest conforming file — L577–582
- §7.4 complete layer-record payload, annotated hex — L1060–1099
- §11.2 grid arithmetic — L1521–1525
- §11.4 ordinals — L1575–1581
- §12.1 bfloat16 — L1638–1641
- §12.3 channel entry hex — L1687–1692
- §13.3 fill tuple — L1757–1762
- §14.2 offsets/strides — L1878–1888
- §14.3 packed bool plane — L1912–1917
- §14.5 padding content — L1968–1973
- §15.4 entry_count = 1,000,000 — L2092–2105
- §15.4 planar disk ordinal 74 — L2107–2111
- §16.2 slab runs — L2206–2213
- §17.3 byte-shuffle — L2387–2390
- §20.3 superseding one tile — L3087–3094
- Appendix A annotated 128-byte file — L4098–4138
- Appendix B constants — L4145–4173
- Appendix C registry snapshot — L4182–4200
- Appendix G reproducible-writer profile, items 1–10 — L4277–4404
- Appendix H conformance checklists — L4406–4477

Numbered lists checked for order / duplication / gaps:
- §9.2 commit protocol steps 1–6 — in order, no gaps
- §10.1 four extension vehicles 1–4 — in order
- §19.1 open steps 1–4 — in order
- §19.4 tile-read steps 1–8 — in order
- §20.3 appender steps 1–6 — in order
- Appendix G items 1–10 — in order, no duplicates

---

## 3. Arithmetic actually performed

### 3.1 Checksums

I implemented CRC-32C from §4.5's parameters alone (polynomial 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and reproduced §4.5's
check vector before trusting it:

```
CRC-32C("123456789") = 0xE3069283      matches §4.5
CRC-32C(<zero bytes>) = 0x00000000     matches §4.5
```

Then, byte for byte:

**Appendix A (L4099–4106).** I rebuilt the 128-byte file from the hex dump and
recomputed the trailer CRC over bytes [64,124) — i.e. trailer-relative [0,60):

```
8a4e5241540d0a1a 0100 0000 00000000
0100000000000000 1000000000000000
0400000000000000 8000000000000000
efcdab8967452301 00000000
CRC-32C = 0xE00938D2 -> stored little-endian D2 38 09 E0
```

The dump's bytes [124,128) are `D2 38 09 E0`. **Correct.** The annotation
table's field ranges all line up: [64,72) magic, [72,74) major, [74,76) minor,
[76,80) flags, [80,88) generation, [88,96) dir_offset, [96,104) dir_length,
[104,112) F, [112,120) file_id, [120,124) reserved, [124,128) CRC. The dump's
row `0070` is `EF CD AB 89 67 45 23 01 00 00 00 00 D2 38 09 E0`, which is
file_id 0x0123456789ABCDEF little-endian, four zero reserved bytes, and the
CRC. **Correct.** Directory at [16,20) is `00 00 00 00` = CRC-32C of zero
bytes. **Correct.** Pad [20,64) = 44 bytes. **Correct.**

**§7.4's layer-record example (L1060–1099).** entry_count = 4, all sentinel.
The 80-byte entry array is `FF×16 00×4` repeated four times:

```
CRC-32C(80 sentinel bytes) = 0x80A34955 -> stored 55 49 A3 80   matches
CRC-32C(55 49 A3 80)       = 0xC4EE982E -> payload 2E 98 EE C4  matches
```

**Correct.**

**§15.4's all-sentinel constant.** CRC-32C of 65,536 sentinel entries
(1,310,720 bytes) = `0xEECB3BB2`. **Correct**, and Appendix B repeats it
correctly.

Every checksum constant in the document reproduces.

### 3.2 §7.4's worked layer record, field by field

Table order (L1006–1023) vs example order (L1071–1090): name, layout,
linearization, codec, filter, A, S, A_slab, rank d, C, dimension entries,
channel entries, index_encoding, entry_count, crc_of_crc_array. The example
follows the table order exactly.

```
 0  03 73 73 74               name len 3, "sst"                        4
 4  01                        layout 1                                 1
 5  01 00                     linearization 1                          2
 7  01 00                     codec 1                                  2
 9  01 00                     filter 1                                 2
11  00 x8                     A = 0                                    8
19  00 x8                     S = 0                                    8
27  00 x8                     A_slab = 0                               8
35  01                        d = 1                                    1
36  01 00                     C = 1                                    2
38  01 78                     dim name len 1, "x"                      2
40  64 00 ... (=100)          E0                                       8
48  20 00 ... (=32)           T0                                       8
56  04 74 65 6D 70 0C 00      chan "temp", type 12                     7
63  04 00 00 C0 7F            fill len 4, 0x7FC00000                   5
68  01                        index_encoding 1                         1
69  04 00 ... (=4)            entry_count                              8
77  2E 98 EE C4               crc_of_crc_array                         4
                                                                  ----
                                                                    81
```

The example's own accounting — "4 + 34 bytes, the dimension entry 18, the
channel entry 12, and the trailing fixed fields 13 — 81 exactly" — checks:
1+2+2+2+8+8+8+1+2 = 34 (nine scalars, as claimed); 2+8+8 = 18; 7+5 = 12;
1+8+4 = 13; 4+34+18+12+13 = 81. **Correct.**

Grid: G = ceil(100/32) = 4, so entry_count = 4. Extent slot length by
R-CNT-17: 4x20 + ceil(4/65536)x4 = 80 + 4 = 84. **Correct.**

§12.3's twelve-byte channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` is
byte-identical to bytes 56..67 of the payload, as §7.4's example claims.
**Correct.**

### 3.3 Geometry, ordinals, sizes

- §11.2: (1024,2048)/(256,256) -> G=(4,8), N=32, P=65,536. Correct.
  (1000,2048) -> G_y = ceil(1000/256) = 4. Correct.
- §11.4: (0,0)->0; (0,1)->1; (1,0)->8. Coordinate (300,700): t=(1,2),
  s = 1*8+2 = 10; u = (44,188), in-tile ordinal 44*256+188 = 11,452;
  planar C=4 channel 2 -> 2*32+10 = 74. All correct.
- §14.2: P=6, uint8+uint16 -> Q=3, size 18; ordinal 5 at [15,18). Planar `b`
  plane 12 bytes, ordinal 5 at [10,12). float32+bool -> Q=5, size 30, ordinal
  5 at [25,30), `m` at byte 29. All correct.
- §14.3: P=10, alternating from true -> byte0 = 0x55 (bits 0,2,4,6), byte1
  bits 0..1 = 0b01. Fill false -> `55 01`; fill true -> 0x01|0xFC = `55 FD`.
  Correct.
- §14.5: extents (5,5), tiles (4,4) -> grid 2x2; edge tile (1,1) covers 4..7
  on both axes; exactly one real position (4,4) and 15 padding; P=16, uint16
  -> 32 bytes, values 1..15 = `CD AB`. Correct.
- §15.4 first example: entry_count 1,000,000 -> 16 segments (15 full +
  16,960); array 64 bytes; region 20,000,064 bytes; k=999,999 is
  segment-relative index 16,959, at segment byte 339,180; array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000) =
  339,200 bytes ~ 339 KB; one full segment = 65,536*20 = 1,310,720 = 1.25 MiB.
  All correct.
- §15.4 second example: disk ordinal 74 at region bytes [1,480, 1,500);
  channel 3 occupies ordinals 96..127 = 32 entries. Correct.
- §16.2 example: N=32, S=8 -> runs [0,8),[8,16),[16,24),[24,32); under
  row-major each is one tile-row; rows 1-2 = ordinals 8..23 = runs 1 and 2.
  Correct.
- §17.3 example: 1.0f/2.0f/3.0f -> `00 00 80 3F 00 00 00 40 00 00 40 40`;
  s=4, n=3; filtered offset i*n+j gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Correct.
- §20.3 example: 32-tile layer index region = 32*20 + 4 = 644. Correct.
- §21.9 note: array at entry_count 2^32 is (2^32/2^16)*4 = 2^18 = 256 KiB, and
  at 2^36 is 2^22 = 4 MiB. Correct. Index region at 2^32 entries is 85.9 GB,
  consistent with §24's "tens of gigabytes".

Fixed-structure widths: trailer 8+2+2+4+8+8+8+8+8+4+4 = 64 with every offset
consistent; record header 2+2+4+8+8 = 24; index entry 8+8+4 = 20; front block
8+8 = 16. All correct.

### 3.4 The register's own counts

I counted mechanically, using §21.1's stated rule ("Instances within a cell are
separated by semicolons, and a cell reading — is one instance"):

```
rows: 121   instances: 277
F: 36 rows,  58 instances
L: 49 rows, 116 instances
T: 26 rows,  55 instances
R: 10 rows,  48 instances
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10, §21.8 says "121
conditions over 277 instances". **All four subsection counts and both totals
match the cells as written.** Whether every cell should say what it says is a
separate question — see finding diagrams-03.

I also derived the register's row set from the rules rather than reading it
off: for §21.4 I walked R-COD-02 through R-COD-10, R-SER-05, R-SER-07,
R-SER-08, R-CNT-20 and R-IDX-03 and found every constraint has a row (T13/T15/
T16/T23 are "cause" rows that route to T24/T25, correctly labelled as such);
for §21.3 I walked every constraint of §7.4's table plus R-ENC-03/04/11/12/15,
R-GEO-01/05, R-TYP-03/07, R-SER-06, R-IDX-04, R-SLB-01/03, R-COD-03/07/09,
R-CNT-12/13/14/15/16/17/18/22/23/25, R-MTA-03/05 and found no gap; for §21.5
I derived the ten from R-CNT-25's enumeration plus R-MTA-04's four bullets and
§18.2's carried-over frame constraints. I found no missing row.

Cross-references I checked and found sound: §20.5's closed count of
"one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)" — §10.2 tabulates eight spaces, record type plus seven,
and each of the seven maps to exactly the row named; §21.7's "§20.5's four
obligations on a compacted file's trailer" — R-WRT-06 states exactly four
(fresh file_id draw, generation 1, ignore-lane carry-forward, version_minor
floor); §15.3's "Six rows are marked *structural*" — exactly six are;
§21.2's "36 conditions"; F33's list of bounds rows that pre-empt it
(F9/F10, F30/F31/F32, L15/L16/L17, T8/T9) — complete for the five claimant
kinds F33 enumerates, and its note that an offset-zero half-zero slot belongs
to F30/L15 rather than F31/L16 is right, since F31/L16 range over 1..15.

### 3.5 One arithmetic result I needed and had to derive myself

T26's cell says a wrong byte-shuffle stride is detected by "T2's or T4's"
check and does not name T5 (pad bits), while §21.7 says a mis-*ordered* image
is witnessed by "T2, T4 or T5". I wanted to know whether T26 was short a row.

Under R-COD-10 the filtered image places byte i of group j at offset
i*n + j, with i in [0,s) and j in [0,n), L = s*n. The maximum offset is
(s-1)*n + (n-1) = sn - 1 = L-1, and it is reached by i = s-1, j = n-1, whose
source offset is (n-1)*s + (s-1) = L-1. **The last byte of the image is a
fixed point of the shuffle at every stride.** Pad bits live in the last byte
of a packed plane (§14.3), so no wrong stride can ever disturb them. T26 is
right to omit T5, and §21.7 is right to include it for mis-ordering, which is
a different mechanism. No finding here — I record the computation because the
two passages read as though they disagree and they do not.

---

## 4. Building a file end to end, and where I had to guess

I built, on paper, a two-layer file: layer `m`, planar, rank 2, dims
y(E=5,T=4) and x(E=5,T=4), channels `f` (float32) and `b` (bool); plus a
top-level user-metadata record. G=(2,2), N=4, P=16, C=2, addressed-tile count
C*N = 8, entry_count 8, index region 8*20 + 4 = 164 bytes. Decoded sizes:
`f` planes P*B = 64 bytes each (§14.2); `b` planes ceil(16/8) = 2 bytes each
(§14.3). Disk ordinals 0..3 are `f`'s tiles, 4..7 are `b`'s (§11.4). Every
figure I needed was there and every number I needed was derivable. Filter 2
would use stride 4 on the `f` planes and be the identity on the `b` planes
(§17.3) — the one place where "the layer's filter" is not one transform, and
§17.3 says so explicitly.

The guesses I actually had to make, in order of how much they cost:

**(a) Changing one channel's fill on a planar layer.** My file has padding
positions in the edge tiles. Suppose I have committed `f`'s four planes and
left `b`'s four as sentinels, and I now want to change `b`'s fill. §20.3
step 4's bar is quantified over "any tile that layer **stores** in the
generation this commit supersedes", and the tiles that store `b` are none, so
the change alters nothing §14 fixes for a stored tile and step 4 permits it.
But §20.3's own Example, shape (c), told me flatly that "A fill change on a
layer that **stores** a tile carrying either [a padding position or a pad bit]
is not an appender's operation at all (step 4)". My layer does store such a
tile — `f`'s edge plane — so the Example forbids what the rule permits. I
followed the rule, because §2.1 makes the Example non-normative, but I had to
notice that to get there. This is finding **diagrams-01**.

**(b) A shrink that de-addresses nothing.** Shrinking E_x from 5 to 4 leaves
G_x = 1... no: ceil(4/4) = 1, down from 2, so that one does de-address. Try
E_y 5 -> 5 and E_x 5 -> 5 with T=4 shrunk in a different layer: take
E=(9), T=(4), G=2, and shrink E to 8. G stays 2, entry_count stays 2, no tile
is de-addressed, and the last tile's positions 8 becomes padding. §20.3 says
"Where a shrink is permitted the de-addressed tiles' extents become slack,
`[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region,
and every surviving stored tile is untouched." None of the first two clauses
holds for my shrink: nothing is de-addressed and entry_count does not change.
I re-emitted nothing and treated the commit as directory-only. This is finding
**diagrams-05**.

**(c) A 100-byte file declaring format major 7.** Not a file I would write,
but a file I have to classify. §21.2's preamble told me exactly four rows
reach a foreign-major file and named them; F5 is not among them, so I
concluded the file is refused on capability grounds and a verifier reports
*cannot establish*. But nothing in the document sequences R-CNT-27's 128-byte
minimum behind the version gate — §6.2's ordered list starts at the trailer
and does not contain it, and R-RDR-02 explicitly licenses earlier detection —
so a verifier that checks the file's length first establishes F5 and, under
§2.3's priority rule, must report *nonconforming*. Finding **diagrams-02**.

**(d) The domain of `extent_offset`.** §4.7's Note told me §7.2's table "folds
each field's range into its Field cell". Three of §7.2's five Field cells
carry no range, so I had to go to R-CNT-13 and R-ENC-03 for them. Cheap, but
the Note said I would not have to. Finding **diagrams-04**.

**(e) Whether a corpus needs a `NaN` vector.** R8's condition covers both a
number whose binary64 value overflows and the bare tokens `NaN` / `Infinity` /
`-Infinity`, and its Instances cell enumerates two containers and no
alternatives — so R-VEC-03's "one vector per instance" buys two files and
neither need exercise a bare token. Finding **diagrams-03**.

Everything else I needed to write the file was determined. In particular the
annotated Appendix A file is byte-exact, §7.4's example is byte-exact, and
every layout table's offsets sum to its declared fixed size.

---

## 5. Figures checked and found sound (recorded so coverage is checkable)

- **§5.1's three-commit diagram (L588–616).** I replayed the commits: c1
  writes A + dir1/pad/tr1; c2 appends B + dir2/pad/tr2, stranding dir1..tr1;
  c3 touches no layer and appends dir3/pad/tr3, stranding dir2..tr2. That is
  exactly `front | A | slack | B | slack | dir3 | pad | trail3`. The figure's
  own caveat that the grouping is illustrative and that layer structures need
  not be contiguous (R-SLB-05) is present and correct.
- **§9.2's crash diagram (L1202–1211).** Row 2's arrow sits at the same column
  as row 1's F, correctly making the point that trail_n is intact but no
  longer terminal; row 3's hatched run covers exactly dir_n/pad/trail_n.
- **§20.3's shapes (a) and (b).** (a): only the old directory/pad/trailer
  become slack, sized by layer count, not by data — correct, since A's record
  is re-emitted byte-identically with its extent slot intact (R-WRT-05). (b):
  the whole index region moves because one extent slot addresses it — correct
  and consistent with R-CNT-17 and the 644-byte worked figure.
- **§20.5's compaction diagram.** Placement changes, content does not; the
  primed index regions are the one record-extent kind regenerated rather than
  copied. Consistent with R-WRT-07. (The caption's "every record extent [but a
  relocated index region] survives" elides the MU=0/PE=0 records a compactor
  may drop, which the preceding normative text does state; I judged this
  inside the licence an Example has and did not raise it.)
- **§8.1's coverage map** against §4.5's classification: the three terminal
  checksum fields (trailer, directory region, user-metadata extent) are
  exactly the map's comparison-verified-and-uncovered ones; the three interior
  ones (segment CRC array, entry crc, crc_of_crc_array) are each covered by
  exactly one further checksum in the map; the unassigned-type extent row is
  the one "no checksum" row §4.5 names. Consistent.
- **§10.2's table** against §7.3, §11.4, §12.2, §14.1, §15.1, §17.2, §17.3,
  §18.2: every assigned/reserved/experimental boundary matches its defining
  section, and the "channel layout has no experimental range" claim matches
  R-SER-06's "3 through 255 are reserved".
- **Appendix C** against §7.3, §12.1/§12.2's Note, §17.2, §17.3, §14.1, §11.4,
  §15.1, §18.2, §6.3, §18.4: every entry matches. The pinned reservations 14,
  15, 16, 17, 18, 19 match §12.2's Note ("opaque" for 19's "fixed-size
  raw-bytes type").
- **Appendix B** against its cited sections: all 26 rows correct, including
  both CRC constants I recomputed, the 0x7E000000 lz4 cap, the 65,536-byte
  discovery window (dir_length + pad + 64), and the eight-part minimum
  guarantee row that matches §21.9's eight table rows one for one.
- **§21.9's hard-limits paragraph.** Its "Two do not [follow from a width, an
  external format, or the value domain]" is exactly right: the 512 floor on A
  and the 255-byte user-metadata key cap are the only two chosen numbers; the
  2^62 ceilings on A and A_slab follow from the value domain, and the
  128-byte minimum from arithmetic.
- **Appendix G items 1–10.** Numbering intact. Item 3's total order is
  well-founded: the tie-break key masks extent_offset (which the order itself
  fixes), type 0x0001 ties by layer name (total, because F4 forbids duplicate
  layer names), and two records the key does not separate really do yield the
  same file under either order, because extents are owned exactly once
  (R-CNT-13) and every non-masked component is content. The closing paragraph
  correctly declines to give a count.
- **Appendix H's four checklists** against §2.3: the reader list's "all four
  codecs, both filters, both layouts, all thirteen sample types, both
  user-metadata encodings" matches R-CNF-03 read through §17.2, §17.3, §14.1,
  §12.1 and §18.2 exactly; the verifier list's items each map to a
  verifier-detected row or to §9.7; the updater list's items map to §20.3/§20.4.
  Each checklist's preamble disclaims exhaustiveness and none of them is
  relied on elsewhere as authority.
- **§15.3's entry-validity table** against §21.4: every one of its eleven rows
  has a register row (T6, T7, T10, T8, T11, T9+T12, T1, L18, F33, L40/L41/L42)
  and no register row lacks a table row.
- **§21.6's non-violations table**: every row's Defined-behavior cell matches
  its cited rule. §21.1 explicitly exempts this table from the completeness
  clause, so the layer-sub-record case of an experimental MU=1 type (handled
  in §21.6's prose but not in the table) is not a gap.

---

## 6. Findings

### diagrams-01 — CONTRADICTION

**§20.3, "Example — the three shapes a commit takes", shape (c) (L3128–3136),
against §20.3 step 4 (L2997–3013) and §14.5 `[R-SER-05]` (L1957–1966).**

The Example says:

> **(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no
> padding position and no pad bit. Only the directory is re-emitted. A fill
> change on a layer that **stores** a tile carrying either is not an
> appender's operation at all (step 4): it would invalidate every stored tile
> it reaches.

Step 4's actual bar is:

> A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores **in the generation this commit supersedes**,
> what §14 fixes for its stored bytes or how they decode — the set of padding
> positions (§11.3) and the content `[R-SER-05]` fixes there, ...

and §14.5 fixes padding content per channel:

> at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value

The quantifier that matters is "each channel the position carries". In an
**interleaved** layer one tile carries every channel (§3.1), so changing any
channel's fill reaches every padding position of every stored tile, and the
Example is right. In a **planar** layer a tile carries exactly one channel
(§3.1: "in a planar layer, one cell of the grid for one channel"), so
changing channel c's fill reaches only channel c's planes — and only their
padding positions and, for a bool channel, their pad bits (§14.5's "the
plane's channel's fill bit").

Concrete counter-case, from the file I built in §4: planar layer, dims
y(E=5,T=4), x(E=5,T=4), channels `f` (float32) and `b` (bool). Edge tiles
carry padding positions. Suppose the superseded generation stores `f`'s four
planes (disk ordinals 0..3) and leaves `b`'s four (ordinals 4..7) as
sentinels. The layer plainly "stores a tile carrying" a padding position —
`f`'s edge plane at ordinal 3. Now change `b`'s recorded fill. No tile the
layer stores in the superseded generation carries channel `b`, so nothing §14
fixes for any stored tile is altered; step 4 permits the commit, and only the
directory is re-emitted. The Example says this "is not an appender's operation
at all".

Its stated reason — "it would invalidate every stored tile it reaches" — is
sound; the defect is the quantifier in front of it. The Example's condition
ranges over the **layer** ("a layer that stores a tile carrying either")
where the rule ranges over the **channel-tile pairs the change reaches**.

**Which reading I take.** The rule's. §2.1 makes text labelled *Example*
non-normative, so step 4 governs and shape (c)'s qualifier is a sufficient
condition mis-stated as a necessary one.

**What an implementer does wrong without this.** An appender that trusts the
Example refuses a permitted commit and does the caller's fill change by
writing a whole new layer or a whole new file — for a planar layer of any
size that is an arbitrarily large amount of duplicated data, and it is exactly
the outcome §20.3's own SHOULD ("A writer SHOULD instead produce a new file
wherever a commit would strand a large share of a layer's stored bytes") is
trying to avoid, applied where nothing would be stranded at all. The
narrowing also propagates: §11.1's Rationale and §23.1 both lean on step 4's
tense and quantifier being exact.

**Byte-level?** No. Both behaviours emit conforming files, and no reader or
verifier verdict moves: the file the over-cautious appender writes is
conforming, and the file the correct appender writes is conforming. It costs
an implementer a whole-layer rewrite it does not owe.

---

### diagrams-02 — AMBIGUITY

**§21.2's preamble (L3416–3430), against `[R-CNT-27]` (§5.1, L571–575),
`[R-CNT-06]` (§6.2, L769–778) and `[R-RDR-02]` (§19.2, L2773).**

The preamble reads:

> A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below whose
> subject is that file's *geometry* do not reach it: §6.2 puts the version gate
> ahead of every check but the trailer magic and the trailer CRC, so such a
> file is refused on capability grounds first. Four rows are outside that
> reasoning and do reach it, because their subject is a field fixed across
> every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's
> trailer CRC — the two checks §6.2 places before the gate — and F6 with F1's
> front-block instance, which `[R-CNT-04]` places before other processing ...

This is a claim about *when* one check happens relative to another, and it is
asserted as a fact with a closed count of exceptions. The ordering it rests on
is §6.2's:

> A reader MUST validate, in order: the trailer magic; the trailer CRC; the
> version gate (§6.3) ... and then, those gates passed, MUST validate all of
> the following before acting on the fields involved: ...

That MUST orders the checks **inside its own list**. F5's governing rule is
not in that list:

> No conforming file is shorter than 128 bytes ... A reader MUST treat a
> shorter file as a validity error at file scope. `[R-CNT-27]`

`[R-CNT-27]` fixes no position relative to the version gate, and F5's first
Instance is "F (physical file size)" — a quantity §19.1 step 1 obtains
*before* step 2 fetches the trailer at all ("**End of file.** Obtain the
transport-authoritative file size F"). §19.2 then says in terms: "A reader MAY
detect any violation earlier (`[R-CNF-12]`)". So a reader or verifier that
compares F against 128 at step 1 establishes F5 before it ever reads
version_major.

**Permitted readings.**

*(i)* The preamble means what it says and F5 is among "the rows whose subject
is that file's geometry", so F5 must not be established on a foreign-major
file — in which case the document owes a rule sequencing `[R-CNT-27]` behind
the version gate, and it has none. A verifier that checks size first is then
violating an ordering nobody stated.

*(ii)* F5 is not "geometry" and therefore falls in neither the excluded set
nor the four exceptions — in which case the preamble simply does not dispose
of it, and its count of four is short by one instance.

*(iii)* F5 does reach such a file, the preamble's "four" is wrong, and a
64-to-127-byte file declaring major 7 is *nonconforming* under this text.

**Which I picked.** (iii), on the ground that `[R-CNT-27]`'s MUST is
unconditional and §19.2 licenses early detection, so nothing forbids
establishing it. But (i) is what the preamble asserts, and §2.3's
"a file declaring another major is neither conforming nor nonconforming under
it" argues for it.

**What an implementer does wrong without this.** Two conforming verifiers
handed a 100-byte file whose trailer magic and CRC are valid and whose
version_major is 7 report different verdicts. Verifier A obtains F, sees
100 < 128, establishes F5, and — §2.3: "An established violation takes
priority: a verifier that has established any violation reports
*nonconforming*" — certifies it *nonconforming*. Verifier B follows §6.2's
list, hits the version gate, establishes nothing, and reports *cannot
establish*. §2.3 makes those two verdicts semantically opposed
("*Cannot establish* is not a finding that the file is nonconforming"), and
§21.2's preamble exists precisely to settle which one is owed. Readers
diverge the same way in their diagnostic, which §6.3 makes a SHOULD-level
obligation to distinguish ("a reader that reports an unimplemented major as
corruption misleads users into discarding files that current software reads").

**Byte-level?** No, and I want to be explicit about why, because it is close.
Both actors refuse the file: neither certifies it and neither serves data from
it. The set of byte sequences a conforming writer may emit is untouched, and
no reader accepts a file another rejects. What forks is the *label* on the
refusal — a verifier's verdict among three, not accept-versus-reject. I grade
it below byte-level on that ground and note that it is nonetheless a
divergence in a normative output of a conformance class, and that it lands in
a closed count inside one of this round's edited passages.

---

### diagrams-03 — AMBIGUITY

**§21.5 row R8 (L3592), against `[R-MTA-04]`'s third bullet (§18.2,
L2546–2555) and §21.1's instance rule (L3371–3399).**

R8 reads:

> | R8 | A user-metadata document contains a non-finite number, in any form — a
> magnitude whose binary64 interpretation overflows (`1e400`) and the bare
> tokens `NaN`, `Infinity` and `-Infinity` alike | top-level document; layer
> sub-record document | reader | extent use | `[R-MTA-04]` (R-CNT-25) |

Two instances: one per container, none per form. §21.1 fixes how a cell is to
be filled:

> An instance names a field the condition ranges over, a container it can
> occur in, one of several alternatives the condition text states, or any
> combination of the three ... a row whose check ranges over a family without
> the condition changing shape states that range as a single instance (T24's
> *any codec*), and one whose members give the condition materially different
> shapes enumerates them (T15, T25).

R8's condition text states alternatives explicitly, and the rule it accounts
for distinguishes them by mechanism:

> A document is unreadable if it contains a number whose binary64
> interpretation is not finite — which covers a magnitude that overflows on
> conversion, `1e400` being the ordinary case — or any of the bare tokens
> `NaN`, `Infinity`, or `-Infinity`, **which RFC 8259 does not admit and some
> parsers accept regardless**.

Those are not one shape. `1e400` is well-formed JSON that a conforming parser
accepts and a conversion step must then reject; a bare `NaN` is not JSON at
all, and the bullet's own clause says the failure mode is a *lenient parser*.
A file exercising one exercises no part of the other's code path. The
document's practice elsewhere is to split exactly this way: R7 enumerates
"not well-formed JSON", "top-level value not an object" and "leading U+FEFF"
as three instances although R-MTA-04 states the last two in a single bullet;
T15 enumerates zlib and gzip wrappers as two.

**Permitted readings.** (a) The forms are one family and "in any form" makes
them T24's *any codec* case — two instances, as written. (b) The forms are
materially different shapes the condition text states as alternatives, and the
cell owes four (2 forms x 2 containers), or arguably eight if the three bare
tokens are themselves enumerated as R7 enumerates its three.

**Which I picked.** (b), for the two containers times two forms. The bullet's
"which RFC 8259 does not admit and some parsers accept regardless" is the
document telling me the second form is a different failure, and §21.1's tie-
breaker for "materially different shapes" is what to do about it. Reading (a)
is defensible and turns on a judgement §21.1 leaves to the cell's author,
which is why I file this as an ambiguity rather than as a flat error.

**What an implementer does wrong without this.** Two consequences, both in
promises the document makes normatively. First, §21.8 (`[R-ERR-02]`) states
"121 conditions over **277** instances"; under reading (b) the figure is 279,
and the mismatch would sit in a normative count. Second, §21.8 and
`[R-VEC-03]` require "one vector per instance", so under reading (a) a
complete corpus contains two R8 files and neither need contain a bare
`NaN` — the exact input the bullet says lenient parsers accept. An
implementation whose JSON reader accepts bare `NaN` passes a complete corpus.

**Byte-level?** No. `[R-VEC-01]` makes the corpus derivative — "where a
vector's recorded expectation and this specification disagree, this
specification governs" — so no reading changes which documents are unreadable;
a bare `NaN` is ignore-record under either, by R8 or by R7. What moves is what
a conforming corpus must contain, and the accuracy of a normative count.

*Provenance note.* The pre-loaded auto-memory index that appeared in my
context contained a title referencing this row identifier. I did not open the
file. I reached this row by counting §21.5's cells against §21.1's rule and
R-MTA-04's bullets, in the same sweep that produced §3.4's totals; a reader
who wants to discount it on contamination grounds should, and the counting
argument stands on its own.

---

### diagrams-04 — OBSERVATION

**§4.7's Note (L536–549), against §7.2's record-header table (L904–910).**

The Note states what layout tables deliver, and grants three named exceptions:

> Layout tables for fixed-layout structures give, per field: byte offset within
> the structure, size, type, name, taxonomy class, and valid range, each table
> giving the columns its structure needs. A packed variable-length payload —
> the layer record's inline payload (§7.4) — has no fixed offsets to give; its
> table omits the offset and class columns ... §6.1's block is a 16-byte
> constant, where a Value column replaces type and range, and **§7.2 folds each
> field's range into its Field cell.**

§7.2's table has five fields and columns Offset | Size | Type | Field | Class.
Two Field cells carry a range: `type (0 invalid)` and `flags: bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved`. Three do not:
`inline_length`, `extent_offset`, `extent_length`. Their ranges live in
`[R-ENC-03]` (0 to 2^63 - 1), `[R-CNT-13]` (the extent slot's (0,0) /
half-zero / <16 / past-F-64 rules) and `[R-CNT-12]` (the sequence-bounds rule
on inline_length) — none of them in the Field cell.

So "each field's range" is delivered for two of five. The blanket clause
"each table giving the columns its structure needs" would have covered a
missing column; what it does not cover is a specific claim about where the
missing column's content went.

**Which reading I take.** The Note is labelled *Note* and so non-normative
(§2.1); §7.2's table plus `[R-ENC-03]`, `[R-CNT-12]` and `[R-CNT-13]` are the
authority, and they are complete. The Note is simply inaccurate about §7.2.

**What an implementer does wrong without this.** Reads §7.2's table, takes the
Note at its word that the ranges are in the Field cells, finds none for
extent_offset, and concludes the field is unconstrained beyond u64 — shipping a
parser that does not enforce the (0,0)/half-zero/<16/past-F-64 rules, which
are F30, F31, F32, L15, L16 and L17. That is recoverable at §7.2's next
paragraph, which states the extent-slot rules two lines below the table, so the
cost is a re-read rather than a defect. I file it as an observation, not as an
ambiguity, because the text is decidable and the only expense is in checking
it.

**Byte-level?** No. The ranges are stated normatively elsewhere and the Note
carries no force.

---

### diagrams-05 — OBSERVATION

**§20.3 step 4, the shrink paragraph (L3056–3059), against `[R-CNT-17]`
(§7.4, L1038–1042) and §11.2's grid arithmetic (L1504–1513).**

> Where a shrink is permitted the de-addressed tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
> re-emitted index region, and every surviving stored tile is untouched.

The sentence's subject is "a shrink [that] is permitted" — every such shrink —
and it asserts three consequences of one. Two of the three hold only for the
subset of shrinks that lower a grid count.

`[R-CNT-17]` ties entry_count to the geometry-derived addressed-tile count,
which is N (or C*N) with N = product of ceil(E_i / T_i). A shrink of E_i that
stays inside the same ceiling changes no grid count, so entry_count is
unchanged, extent_length is unchanged, and `[R-CNT-17]` obliges no
re-emission at all. Worked case: rank 1, T = 4, E = 9 -> G = ceil(9/4) = 3;
shrink E to 8 -> G = ceil(8/4) = 2 (this one does de-address); shrink E from 9
to 7 instead -> G = ceil(7/4) = 2, also de-addresses; shrink E from 12 to 10
-> G = ceil(12/4) = 3 and ceil(10/4) = 3, unchanged. That last one is a
permitted shrink with no de-addressed tile, no smaller entry_count, and no
index re-emission — it turns positions 10 and 11 of the last tile into
padding, and step 4 permits it exactly where those bytes already hold the
channel's fill.

§11.1's Rationale states the growth side of the same arithmetic correctly —
"Growth that leaves every grid count ceil(E_i / T_i) (§11.2) unchanged touches
the directory alone" — so the document knows the distinction; the shrink
sentence does not carry it.

**Which reading I take.** The clauses are conditioned on de-addressing having
occurred: "the de-addressed tiles" is vacuous when there are none, and
"the smaller entry_count" with it. That reading makes the sentence true and
uninformative for the no-de-addressing case, and it is what I followed when I
built §4(b). The competing reading — that every permitted shrink re-emits the
index — is what the sentence's grammar offers.

**What an implementer does wrong without this.** Under the competing reading
an appender re-emits a whole tile-index region it did not need to (for a
10^6-tile layer, the 20 MB §20.3's own Note prices, plus 20 MB of new slack),
or, worse, concludes from "obliges the smaller entry_count" that a shrink
which cannot produce a smaller entry_count is not a permitted shrink and
refuses the commit. Both outputs are conforming files; the second refuses an
operation the rule allows.

**Byte-level?** No. Re-emitting an unchanged index region at a new placement
is conforming (`[R-SLB-05]` leaves placement free and the old region becomes
slack), and not re-emitting it is conforming. No reader or verifier verdict
turns on which the writer chose.

---

## 7. What I could not determine

Nothing in my charter was left undecidable. Two things I deliberately did not
raise, and say so here so the omissions are visible:

1. §20.5's compaction Example says "every record extent [survives] but a
   relocated tile-index region", which elides the MU=0/PE=0 records the
   preceding normative text lets a compactor drop. I judged that inside an
   Example's licence, since the drop is stated two paragraphs above it.
2. §23.1 cites "§20.3's shape (c)" for the fact that editing user metadata
   appends a new extent — and shape (c) says of that very fact "Editing user
   metadata is **not** this shape ... as in (b)". The citation points at where
   the sentence is written, which is literally correct, so I did not file it.

I found no arithmetic error anywhere in the document: every CRC constant
reproduces, every layout table's offsets sum to its declared size, every
worked ordinal and decoded size is right, and the register's four subsection
counts and its 121/277 total are exact against the cells as written.
