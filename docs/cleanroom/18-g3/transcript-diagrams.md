# Round 18 — Diagram auditor — working transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,339 lines), in five `Read` calls covering lines 1–400, 400–849, 866–1425,
1425–2024, 2025–2644, 2644–3263, 3264–3713, 3714–4339 (overlapping). I ran
`grep`/`awk` and Python **against that one file only**, plus standalone Python
that reads no files (CRC-32C implementation, geometry arithmetic, a file
builder). I listed no directories, ran no git commands, read no ADR, no
`docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`, no
`AGENTS.md`. I wrote three scratch files of my own (`crc.py`, `crc2.py`,
`build.py`) and one output file, `mini.tarn`, in my scratchpad; I did not read
the round-18 output directory.

Prior knowledge of other array/image formats was used only to generate
suspicions (e.g. "does the BOM case belong under 'not well-formed JSON'?"),
never to settle anything. Every settled question below is settled by a
quotation from this document or by arithmetic I did myself.

---

## Part 1 — Enumeration (coverage is checkable from this list)

### 1a. Tables (25)

| Line | Table |
|---|---|
| 236 | §2.4 outcome classes (incl. preserve-verbatim row) |
| 698 | §6.1 front signature block layout |
| 741 | §6.2 trailer layout |
| 905 | §7.2 record framing layout |
| 978 | §7.3 record types of format major 1 |
| 1007 | §7.4 layer record inline payload |
| 1122 | §8.1 checksum coverage map |
| 1396 | §10.2 numeric identifier spaces |
| 1600 | §12.1 core sample types |
| 1832 | §14.2 decoded size / offset of value k |
| 2000 | §15.1 tile-index entry layout |
| 2048 | §15.3 entry-validity classification |
| 2440 | §18.2 user-metadata inline payload |
| 2589 | §18.4 standardized keys |
| 3120 | §20.4 updater obligations by stored flags |
| 3360 | §21.2 file-scope register (F1–F36) |
| 3404 | §21.3 layer-scope register (L1–L49) |
| 3461 | §21.4 tile-scope register (T1–T26) |
| 3510 | §21.5 ignored-record register (R1–R10) |
| 3528 | §21.6 conditions that are not violations |
| 3643 | §21.9 implementation-limit minimum guarantees |
| 3982 | Appendix A byte table for the annotated minimal file |
| 4018 | Appendix B constants |
| 4115 | Appendix E changelog |
| — | (Appendix C is prose-formatted registry snapshot, lines 4054–4072) |

### 1b. ASCII figures inside code fences (6)

| Lines | Figure |
|---|---|
| 587–592 | §5.1 a file after three commits |
| 1069–1088 | §7.4 the 81-byte layer-record inline payload, offset by offset |
| 1200–1209 | §9.2 what a crash sees (3 rows) |
| 3050–3054 | §20.3 shape (a), a new layer |
| 3066–3070 | §20.3 shape (b), tiles added to an existing layer |
| 3090–3093 | §20.3 shape (c), a change confined to the directory |
| 3222–3228 | §20.5 what compaction reclaims |
| 3970–3979 | Appendix A hex dump of the 128-byte minimal file |

### 1c. Worked numeric examples (blockquoted `**Example`) — 21

513 (§4.6 `température`), 577 (§5.1 smallest file), 584 (§5.1 three commits),
1058 (§7.4 layer record payload), 1196 (§9.2 crash), 1516 (§11.2 grid),
1570 (§11.4 ordinals), 1633 (§12.1 bfloat16), 1682 (§12.3 channel entry),
1752 (§13.3 rgb fill), 1873 (§14.2 interleaved/planar offsets), 1907 (§14.3
packed bool), 1963 (§14.5 padding), 2087 (§15.4 entry_count = 10^6), 2102
(§15.4 planar disk ordinal 74), 2201 (§16.2 slabs), 2382 (§17.3 shuffle),
3036 (§20.3 supersede one tile), 3045 (§20.3 three shapes), 3219 (§20.5
compaction), Appendix A (3966–4010).

### 1d. Numbered / checklist material (5)

- §9.2 commit protocol, steps 1–6 (1166–1178)
- §19.1 open algorithm, steps 1–4 (2652–2693)
- §19.4 tile-read algorithm, steps 1–8 (2779–2830)
- §20.3 append procedure, steps 1–6 (2905–3026)
- Appendix G reproducible-writer profile, items 1–10 (4149–4249)
- Appendix H conformance checklists, five classes (4268–4339)

---

## Part 2 — Arithmetic and CRC verification (done, not eyeballed)

I implemented CRC-32C from §4.5's parameters alone (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — reflected table
constant 0x82F63B78 — and checked it against §4.5's own check vector before
using it for anything.

```
CRC-32C("123456789")                     = 0xE3069283   § 4.5 says 0xE3069283  OK
CRC-32C(<zero bytes>)                    = 0x00000000   § 4.5 says 0x00000000  OK
CRC-32C(4 sentinel entries, 80 bytes)    = 0x80A34955   § 7.4 says 0x80A34955  OK
CRC-32C(`55 49 A3 80`)                   = 0xC4EE982E   § 7.4 says 0xC4EE982E  OK
CRC-32C(2^16 sentinel entries, 1310720 B)= 0xEECB3BB2   §15.4 says 0xEECB3BB2  OK
```

**Appendix A, byte for byte.** I parsed the hex dump at 3970–3979, sliced the
trailer at [64,128), and recomputed:

```
file length                       = 128            (§5.1 minimum: 128)        OK
trailer[0:8]  8A 4E 52 41 54 0D 0A 1A                                          OK
version_major = 1, version_minor = 0, flags = 0                                OK
generation = 1, dir_offset = 16, dir_length = 4                                OK
committed_file_length = 128 = file length, 128 mod 64 = 0                      OK
file_id  EF CD AB 89 67 45 23 01 -> 0x0123456789ABCDEF (table says exactly)    OK
reserved [120,124) = 00 00 00 00                                               OK
CRC-32C(trailer[0:60])            = 0xE00938D2   table says 0xE00938D2         OK
directory [16,20) = 00 00 00 00 = CRC-32C of zero record bytes                 OK
dir_offset + dir_length = 20 <= F - 64 = 64                                    OK
```
The 15 rows of Appendix A's byte table tile [0,128) with no gap and no
overlap. Verified.

**§7.4's layer-record example.** Walked every offset in the fence at 1069–1088:

```
 0 name 03 "sst"        4 bytes -> 4     4 layout  u8      -> 5
 5 linearization u16    -> 7             7 codec   u16     -> 9
 9 filter u16           -> 11           11 A  u64          -> 19
19 S u64                -> 27           27 A_slab u64      -> 35
35 rank d u8            -> 36           36 C u16           -> 38
38 dim name 01 "x"      -> 40           40 extent 0x64=100 -> 48
48 tile extent 0x20=32  -> 56           56 chan "temp"+type 12 -> 63
63 fill len 4 + 00 00 C0 7F -> 68       68 index_encoding  -> 69
69 entry_count = 4      -> 77           77 crc_of_crc_array-> 81
```
Recap arithmetic: 4 (name) + 34 (the nine scalars: 1+2+2+2+8+8+8+1+2)
+ 18 (dimension entry 1+1+8+8) + 12 (channel entry 1+4+2+1+4)
+ 13 (1+8+4) = **81**, matching the stated inline_length. Grid
count ⌈100/32⌉ = 4 = entry_count. Extent length 4·20 + ⌈4/2^16⌉·4 = **84**,
matching. The 12-byte channel entry is byte-identical to §12.3's example.

**§14.2's example.** Interleaved a(uint8)+b(uint16): Q = 3, decoded size
P·Q = 18. In-tile ordinal of (1,2) with T = (2,3) is 1·3+2 = 5; sample at
5·3 = 15, so [15,18), `a` at 15, `b` at 16–17. Planar `b`: 6·2 = 12 bytes,
ordinal 5 at 5·2 = 10, bytes 10–11. Interleaved t(float32)+m(bool): Q = 5,
size 30, ordinal 5 at 25, `t` 25–28, `m` at 25+4 = 29. All match.
General form u·Q + F_c reduces from the table with k = u·C + c
(k div C = u, k mod C = c). Correct.

**§14.3's example.** P = 10 alternating from true: byte 0 bits 0,2,4,6 set
= 0x55; byte 1 = values 8,9 = 1,0 = 0x01; P mod 8 = 2, so pad bits are
positions 2..7 = six bits. Fill false -> `55 01`; fill true -> 0x01|0xFC
= 0xFD -> `55 FD`. Matches.

**§14.5's example.** E = (5,5), T = (4,4): G = (2,2); edge tile (1,1) covers
4..7 on both axes = 16 positions, of which (4,4) is the only real one, so 15
padding positions. One uint16 channel: 16·2 = 32 bytes; value 0 real, values
1–15 = `CD AB` for fill 0xABCD. Matches.

**§11.2 / §11.4 / §15.4 examples.** G = (4,8) from (1024,2048)/(256,256);
N = 32; P = 65,536; ⌈1000/256⌉ = 4. Coordinate (300,700): tile (1,2),
s = 1·8+2 = 10; in-tile (44,188), ordinal 44·256+188 = 11,452; planar C = 4,
channel 2 -> 2·32+10 = 74; entry at 74·20 = [1480,1500); channel 3's
entries are 96..127 = 32 entries. entry_count = 10^6: ⌈10^6/2^16⌉ = 16
segments, 15 full (983,040 entries) and a last of 16,960; array 64 bytes;
region 20,000,064 bytes; k = 999,999 in segment 15 at 20·16,959 = 339,180;
array [20,000,000, 20,000,064); segment 15 [19,660,800, 20,000,000) —
339,200 bytes ("~339 KB"); one full segment = 65,536·20 = 1,310,720 = 1.25
MiB. All match.

**§17.3's shuffle example.** 1.0/2.0/3.0 float32 LE = `00 00 80 3F 00 00 00
40 00 00 40 40`; s = 4, n = 3; output offset i·n+j gives
`00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Matches the stated result.

**§21.9's note.** entry_count 2^32 -> 2^16 segments -> 2^16·4 = 262,144 B =
256 KiB; 2^36 -> 2^20·4 = 4 MiB. Both match.

**§19.4's planar note.** Entries c·N+s are N·20 bytes apart; if N ≥ 2^16 the
ordinal gap is ≥ 2^16 so segment indices must differ. Correct.

**§21.8's promise, checked mechanically.** I parsed every 6-column register
row and counted semicolon-separated instances per §21.1's own rule ("a cell
reading — is one instance; the count is therefore mechanical once the cell is
written"):

```
F: 36 rows / 58 instances      L: 49 rows / 116 instances
T: 26 rows / 55 instances      R: 10 rows / 44 instances
total 121 rows / 273 instances   -- §21.8 says "121 conditions over 273 instances"
```
Row labels are contiguous 1..36 / 1..49 / 1..26 / 1..10 with no duplicate and
no gap. Every Detector=verifier row has Detected=certification and no
Detector=reader row has Detected=certification; every Detected value is one of
§19.2's four tiers or `certification` (R1 carries the split form "open
(top-level); layer access (sub-record)"). No anomalies.

**Identifier hygiene.** 161 distinct bracketed `[R-…-NN]`; every identifier
cited inside parentheses in a register cell exists in bracketed form somewhere;
per-prefix numbering has no gaps except R-ENC (17–99 unused, R-ENC-100 being
§2.2's illustrative example) and R-SER-04, which §14.4 records as withdrawn
and permanently retired. That matches §2.2.

---

## Part 3 — I built a file from the document alone

To test whether the byte-layout tables actually close, I built a complete
two-tile file from the tables and prose only (no vectors, no tooling):

rank 1, dimension `x` extent 3, tile extent 2 -> G = ⌈3/2⌉ = 2 = N; P = 2;
interleaved, C = 1, channel `v` uint8 (type 6) fill 0x00; codec 1, filter 1,
A = S = A_slab = 0; linearization 1; index_encoding 1; entry_count = 2.
Tile 0 = `11 22`; tile 1 = `33 00` — x = 3 is a padding position, so §14.5
forces the fill byte 0x00 there.

Placement chosen freely under `[R-SLB-05]`: tile0 [16,18), tile1 [18,20),
index region [20,64) (2·20 + ⌈2/2^16⌉·4 = 44 = `[R-CNT-17]`'s formula),
directory [64,165) (24-byte header + 73-byte inline + 4-byte CRC = 101),
pad [165,192) = 27 bytes, trailer [192,256). F = 256, F mod 64 = 0,
dir_offset + dir_length = 165 ≤ F − 64 = 192.

Coverage check per §5.2/§9.7: claimants total 16+2+2+44+101+64 = 229;
slack = 256 − 229 = 27 = exactly the pad. Disjoint, all inside [16, F−64)
except the front block and trailer, which §9.7 claims separately.

**Nothing in this build required a guess.** Every field width, order, and
derived quantity came from §6.1/§6.2/§7.2/§7.4/§15.1 and §11.2's arithmetic.
I then repeated the exercise on paper for a planar layer with C = 2
(`m` bool, `v` float32), extents (5,5), tile extents (4,4), filter 2,
S = 2, A_slab = 1: disk ordinals 0–3 for `m` and 4–7 for `v`; decoded sizes
⌈16/8⌉ = 2 and 16·4 = 64; runs partition each channel block independently
([0,2),[2,4) and [4,6),[6,8)); shuffle stride 1 (identity) for the packed
plane and 4 for the float plane; the edge tile's 15 padding positions carry
the fill bit / fill bytes; P mod 8 = 0 so there are no pad bits. Again no
guess was needed. The byte-layout tables close.

---

## Part 4 — Figure-by-figure judgements

**§5.1's three-commit figure (587–592).** Column alignment checked
programmatically: the four box rows are each 72 characters and the underline
brackets land exactly on the `┬`/`┴` columns of the `layer A`, `layer B`, and
`dir₃…trail₃` cells. The two ▓ runs are consistent with the narrative: commit
1 left dir₁/pad/trail₁ between layer A and layer B, commit 2 left
dir₂/pad/trail₂ between layer B and dir₃, and commit 3 touched no layer, which
is why it re-emitted "the directory, the pad and the trailer alone". The
figure carries its own scope disclaimer ("Regions, not offsets") and an
explicit warning that the grouping under the box is illustrative and that a
layer's structures need not be contiguous (`[R-SLB-05]`). No defect.

**§9.2's crash figure (1200–1209).** Row 2's ▓ is the interrupted commit's
partial write past trail_n; row 3's ▓ is dir_n/pad/trail_n, which commit n+1
superseded. Both match §5.2's definition of slack and `[R-LIF-05]`'s
no-backward-scan rule. No defect.

**§20.3's three shapes (3050–3093).** (a) A's record carried into dir₂
byte-identically, extent slot and all — matches `[R-WRT-05]` and §20.3 step 4's
"A layer whose record alone changes keeps its extent slot". (b) the whole
index region moves because one extent slot addresses it — matches
`[R-CNT-17]`/§7.4. (c) the three named directory-only changes each check out:
clearing a slab declaration is licensed by `[R-SLB-04]`; renaming a layer
touches nothing §14 fixes; changing fill on a layer with no padding position
and no pad bit reaches no byte `[R-SER-05]` constrains. The caveat that a fill
change on a layer that *stores* such a tile "is not an appender's operation at
all" matches step 4's bar. The `└ old ─┘` bracket in (b) starts one column
inside its cell and ends on the delimiter, where (a)'s brackets start on the
delimiter — a cosmetic asymmetry in ASCII art that points at the right cell;
not reported.

**§20.5's compaction figure (3222–3228).** file_id X/generation 7 in,
file_id Y/generation 1 out — matches `[R-WRT-06]`'s "fresh file_id … and
generation 1". Both index regions carry the ′ regeneration mark; since the
figure declares "Regions, not offsets", it makes no claim that A's tiles sat
still, and regenerating an index whose entries did not move reproduces the
same bytes anyway. The caption's "the one kind this operation regenerates
rather than copies" is true of format major 1, where no registered MU = 1 type
other than the layer record carries offsets; §20.5's prose already reserves
the case of a future registered type that does. No defect.

**Appendix A (3966–4010).** Verified byte-exact above. The closing paragraph's
request accounting also checks: the whole file is 128 bytes so a suffix window
reaching offset 0 makes the front block resident and `[R-CNT-04]` bites; a
112-byte window covering [16,128) contains the directory (containment test of
§6.4) while leaving [0,16) non-resident. 128 − 16 = 112. Correct.

**Appendix B (4018–4045).** Every row cross-checked against its defining
section: front block, trailer magic, 64-byte trailer at 64-aligned offset,
128-byte minimum, dir_offset ≥ 16 / dir_length ≥ 4, extent_length ≥ 5,
boolean 0x00/0x01, 24-byte record header, 20-byte index entry, 2^16-entry
segment with a 4-byte CRC each, `FF ×16 00 ×4` sentinel, 0xEECB3BB2,
CRC-32C parameters and check vector, 0..2^63−1 value domain, 255-byte names,
rank ≤ 255 and C ≤ 65,535 (the u8/u16 widths), 1 ≤ S ≤ 2^63−1, A a power of
two in [512, 2^62], A_slab a power of two in [1, 2^62], 65,536-byte discovery
window, 1–16 MiB tile guidance, zstd magic, 0x7E000000, `tarn.` prefix, and
the eight minimum guarantees, which reproduce §21.9's table exactly. No
mismatch found.

**Appendix C (4054–4072).** Matches §7.3, §12.1/§12.2 (including the pinned
reservations 14–19), §17.2, §17.3, §14.1, §11.4, §15.1, §18.2, §6.3 and
§18.4 row for row.

**§10.2's table.** All eight spaces agree with the sections that own them:
record type 0x0001–0x0002 / 0x0003–0x7FFF / ≥ 0x8000; layout 1,2 / 3–255 /
none; linearization 1 / 2–0x7FFF / ≥ 0x8000 (§11.4's "2 and 3 reserved
without semantics" and "4 through 0x7FFF reserved for future assignment" both
sit inside the table's reserved range); sample type 1–13 / 14–0x7FFF /
≥ 0x8000; codec 1–4; filter 1,2; index encoding 1 / 2–0x7F / ≥ 0x80; metadata
encoding 1,2 / 3–0x7F / ≥ 0x80.

**§8.1's coverage map.** Cross-checked against §4.5's prose: the three
terminal checksum fields named there (trailer, directory region,
user-metadata extent) are exactly the three "final bytes" rows; the three
interior checksum fields named there (each segment CRC array, each entry's
crc, each layer record's crc_of_crc_array) each have exactly one further
cover — array under crc_of_crc_array, entry crc under its segment CRC,
crc_of_crc_array under the directory CRC by containment. The seventh row
(unassigned record type's extent) matches both §4.5's carve-out and §22.3's
residue list. §8.2's chain trailer → directory → crc_of_crc_array → segment
CRC array → segment → entry → tile is the same ordering. No defect.

**§15.3's entry table.** Eleven rows; exactly six are marked *structural*, as
the lead paragraph claims. Every structural row has a §21.4 counterpart
(T6, T7, T10, T8, T11, T12/T9) and the crc row is T1; the three *verifier*
rows are L18/F33 and L40–L42. T11 explicitly excludes the all-ones value, so
it does not silently overlap T6 or T7. Clean.

**§12.1's type table.** Thirteen rows, IDs 1–13, sizes 1,1,2,4,8,1,2,4,8,
2,2,4,8; "the twelve types other than bool" is arithmetically right; the
element-size column is the quantity §7.4 cross-checks the fill prefix against
and the quantity §14.2's table consumes, with §14.3 correctly carved out.

**§14.2's table.** The planar row is scoped "planar, numeric channel c", so it
does not stray onto packed bool planes, which §14.3 sizes at ⌈P/8⌉. The
interleaved offset `(k div C)·Q + F_{k mod C}` is exactly §14.1's definition
of value k. No defect.

**Appendix G (4149–4266).** I tested the profile for closure by asking, field
by field, whether a second writer given the same content could differ. Item 3
pins placement (first structure at 16 or the least position a declared
alignment admits, contiguity thereafter, alignment gaps zeroed) and record
order (by type; type 0x0001 ties by layer name; otherwise header with
extent_offset masked, then inline payload, then extent contents). The masking
is what breaks the circularity, correctly noted. Item 2's hash input —
[0, F−64) followed by the trailer's first 60 bytes with file_id zeroed — is
well founded: the trailer's other 52 bytes are all determined before file_id
is chosen, and [60,64) is excluded because the CRC depends on file_id. Item 6
(sentinel for every all-fill tile) plus §14.5's mandated fill padding makes
storedness a function of content. Item 8 pins version_minor and flags; items 1
and 9 pin the producers; item 10 pins NFC (and its 12-vs-13-byte
`température` figure matches §4.6's example). The closing paragraph explicitly
disclaims being a count ("Read the numbered items as the list; this paragraph
names what they are for, not how many there are"), and correctly omits
`flags = 0` from the list of things the profile *adds*, since §6.3 already
makes it a MUST for a creator. Items 1–10 are in order, none duplicated. I
found no gap in the profile's closure.

**Appendix H (4268–4339).** Reader checklist: "all four codecs, both filters,
both layouts, all thirteen sample types, and both user-metadata encodings"
matches §2.3 against §17.2 ("all four are core"), §17.3 ("both are core"),
§14.1, §12.1 ("exactly thirteen sample types, all core") and §18.2 ("Both
assigned encodings are core"). Verifier checklist: the coverage partition and
slack total, extent overlap, the three flag-bit checks, the front block by
equality (with the residency caveat spelled out), F7's pre-trailer gap, the
reserved-range type value, alignment and slab invariants, the three
decoded-content obligations, member ordering, the `[R-MTA-10]` report, and
`[R-CNF-11]`'s two reporting duties — each traceable to a register row or
requirement. Updater checklist matches §20.3/§20.4. Writer checklist matches
§13.1/§14.5/§14.2/§18.2/§9.2/§16 and correctly labels `[R-CNT-03]` as
advisory. No mismatch found.

---

## Part 5 — Findings

### diagrams-01 — CONTRADICTION — §21.7, `[R-ERR-01]`

One sentence asserts an "only" and then names two further witnessing routes
that falsify it.

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — where §21.4's content rows fire; a change that reaches the
> decoded size instead is witnessed by T3 or T14, which
> test a length rather than the decoded image's content — T14 the
> entry's declared length, T3 the decoded payload's own; a change that
> reaches the codec is witnessed by the rows for the codec now declared,
> which test the stored bytes as a stream of it (T15, T17, T23, T25),
> or by T14 where the new declaration is codec 1

The second conjunct of the "only" is "the change reaches a byte §14
structurally constrains", and the reader is told what that means: "a padding
position, a pad bit, or a boolean byte". A decoded-size change reaches none of
those, and neither does a codec change; yet both are then said to be
witnessed. The two halves of the sentence cannot both be true.

The bar in §20.3 step 4 quantifies over four things — "the set of padding
positions (§11.3) and the content `[R-SER-05]` fixes there, the decoded size,
the byte offset of any sample within the decoded tile image, or the codec and
filter that produced the stored bytes" — and only two of those four (a
sample's byte offset with the decoded size unchanged, and a filter change)
are genuinely unwitnessed unless they happen to reach a constrained byte. The
sentence's list of witnesses is right; its "only" is stale.

Readings I can defend: (a) "only" governs the whole conjunction, in which case
the clauses after the first semicolon contradict it; (b) "only" governs the
first conjunct alone ("the affected tiles remain stored"), and the material
after it is a three-way branch on what the change reaches. I pick (b), because
(b) is the only reading under which the paragraph's own witnesses survive and
under which its closing clause ("a commit that supersedes every tile it would
have damaged leaves the live state clean, so the bar is unwitnessed there")
does the work it is plainly meant to do — it explains the failure of the
*first* conjunct.

Not byte-level. T3, T14, T15, T17, T23 and T25 exist in the register with
their own governing rules, and §21.1 makes the rule govern where a row and its
restatement diverge, so no verifier's verdict and no reader's outcome turns on
which reading a reader picks. The cost is to a maintainer of §21's
completeness claim, who is told by "the account, by class, of what fails" the
detectability gate (§21.1) that a class is unwitnessed when in fact it is.

### diagrams-02 — AMBIGUITY — §20.4's obligation table and §21.6's Rule cell

§21.6's non-violation table attributes a behaviour to `[R-WRT-08]`:

> | A record type this specification has not assigned, from the
> experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and
> preserved or dropped per its PE bit; a *reserved*-range type is read
> the same way, but emitting one is a violation (F36, L25) |
> `[R-CNT-15]`, `[R-WRT-08]` |

`[R-WRT-08]`'s own sentence is:

> An updater MUST NOT re-encode a record whose type it does not
> implement, and MUST NOT modify one except by relocating its
> extent and re-pointing its slot under §20.5 — the operation the
> no-embedded-offsets rule (§7.2) makes safe for MU = 0 records.
> `[R-WRT-08]`

Nothing there is about dropping, or about the PE bit. The rule that *is*
about dropping is §20.4's table (its MU = 0, PE = 0 row: "Retain
byte-identical, or drop it — its extent becoming slack. An appender MUST NOT
drop it except in a commit that *independently* changes the scope the record
attaches to…"), together with the paragraph introducing it. That block —
lines 3107 through 3133, containing MUST NOT, MAY and SHOULD obligations for
appenders, compactors and updaters — carries **no requirement identifier at
all**. Every identifier appearing inside it (`[R-CNT-22]`, `[R-CNT-15]`,
`[R-CNT-12]`, `[R-CNT-18]`, `[R-WRT-06]`, `[R-WRT-04]`, `[R-LIF-01]`) is a
citation of another rule, in parentheses. `[R-WRT-05]` terminates the
paragraph above it; `[R-WRT-08]` terminates a separate paragraph two
paragraphs below.

Two readings: (a) `[R-WRT-08]` labels only its own sentence, in which case
§21.6's Rule cell cites a requirement for a behaviour that requirement does
not state, and §20.4's drop rule has no citable identifier at all — awkward
given §2.2 ("Normative requirements carry identifiers"), the front matter
("test vectors cite those identifiers rather than prose positions"), and
§24's `[R-VEC-02]` ("row labels are positional and renumber when a row is
struck, while §2.2 makes the identifier permanent, so the pair is what
survives a renumbering"); (b) `[R-WRT-08]` labels the whole run from
"Persistence governs every record type" through its own sentence, in which
case §21.6 is right. §22.3 uses the identifier the narrow way — "`[R-WRT-08]`
bars re-encoding it" — which is evidence for (a); §21.6 uses it the wide way,
which is evidence for (b). Elsewhere the document is consistent about placing
an identifier immediately after the structure it labels (§19.1's steps then
`[R-RDR-01]`; §19.2's lead-in, list, then `[R-RDR-02]`; §20.3's steps then
`[R-WRT-04]`; §15.3's `[R-IDX-03]` immediately before its table), which
§20.4 does not do.

I pick (a): the identifier labels its own sentence, and §20.4's persistence
obligations are unlabelled. Under that reading an implementer who follows
§21.6's citation to `[R-WRT-08]` to learn when a PE = 0 record may be dropped
finds a rule that does not answer, and must find §20.4's table by section
number instead. Not byte-level: under either reading the obligations
themselves are the same words, and no file's acceptance turns on which
identifier labels them.

### diagrams-03 — OBSERVATION — §21.5, R5/R6 versus R7–R10

Six rows of §21.5 register violations of §18.2's four decoded-document
restrictions. They split the Governing rule cell two ways with no stated
principle:

- R5 (ill-formed UTF-8 / unpaired-surrogate escape): `` `[R-CNT-25]` (R-MTA-04, R-ENC-11) ``
- R6 (empty key or a key with U+0000–U+001F): `` `[R-CNT-25]` (R-ENC-12) ``
- R7 (not well-formed JSON / top-level not an object): `` `[R-MTA-04]` (R-CNT-25) ``
- R8 (non-finite number): `` `[R-MTA-04]` (R-CNT-25) ``
- R9 (duplicate key): `` `[R-MTA-04]` (R-CNT-25) ``
- R10 (key longer than 255 bytes): `` `[R-MTA-04]` (R-ENC-12) ``

R6 and R10 are the sharpest pair. Both register a user-metadata key that
breaks §4.6's name rules, both cite `R-ENC-12` as the secondary rule, and both
are stated by one bullet of `[R-MTA-04]`:

> - **Well-formed UTF-8 throughout** (`[R-ENC-11]`) … and every key
>   satisfying §4.6's name rules — non-empty, at most 255 bytes, free
>   of U+0000 through U+001F.

Yet R6 names `[R-CNT-25]` as governing and R10 names `[R-MTA-04]`. §21.1 says
"A Governing rule cell names that requirement first" — the requirement "that
defines it" — and for both rows the defining requirement is `[R-MTA-04]`;
`[R-CNT-25]` is what assigns the ignore-record outcome, which is the same for
all ten rows and is already stated in §21.5's heading. By that test R5 and R6
are misattributed and R7–R10 are right. R3 is a genuine `[R-CNT-25]` row,
since a decode failure is named there and not in `[R-MTA-04]`.

Not byte-level: the outcome is ignore-record either way and both cited rules
agree. It bites on `[R-VEC-02]`, which makes a vector's manifest record "that
row's governing requirement identifier" — two vectors testing one bullet of
one rule would record two different permanent identifiers.

### diagrams-04 — OBSERVATION — §21.5 row R7, Condition versus Instances

§21.1 fixes what an instance may be:

> An instance names a field the condition ranges over, a
> container it can occur in, one of several alternatives the condition
> text states, or any combination of the three.

R7's Condition cell states two alternatives:

> A decoded user-metadata document is not well-formed JSON, or its
> top-level value is not an object

Its Instances cell enumerates three, across two containers:

> not well-formed JSON, top-level document; not well-formed JSON, layer
> sub-record document; top-level value not an object, top-level document;
> top-level value not an object, layer sub-record document; leading
> U+FEFF, top-level document; leading U+FEFF, layer sub-record document

"Leading U+FEFF" is an alternative the condition text does not state. It is
stated by the governing rule — §18.2's first restriction is titled "**A JSON
object, unmarked**" and reads "the encoding carries no byte-order mark: a
leading U+FEFF makes the document unreadable" — so the instance is right and
the Condition cell is the incomplete half. I checked every other multi-
instance row for the same pattern (F23, F17, L21, L22, L30, T3, T14, T15,
T18, T21, T22, T25, R1, R4, R5, R6): in all of them the instances are either
fields, containers, magnitude directions licensed by §21.1's direction rule,
or alternatives the condition text does state. R7 is the only row where the
instance list exceeds the condition's stated alternatives.

Not byte-level; §21.1 already says the rule governs where a row and its rule
diverge, and the instance count (and hence §21.8's 273) is unaffected.

### diagrams-05 — OBSERVATION — §20.3's cost Note restates its rule too narrowly

The rule, in §20.3 step 4:

> Every layer
> whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full

The Note that quantifies its cost:

> **Note.** A commit's cost is dominated by its index, not its data:
> any change to a layer's stored-tile set re-emits that layer's whole
> tile-index region, so editing one sample of a 10⁶-tile layer
> appends about 20 MB of index and leaves as much slack.

The Note drops "or index content", and then reasons from the narrowed premise
to a case the premise does not cover: editing one sample supersedes a stored
tile, which under `[R-LIF-01]` must be written at a new offset, so the entry's
offset, length and crc change — index *content* — while the set of stored
tiles is exactly what it was. The conclusion (20 MB re-emitted) is correct
under the real rule and does not follow from the Note's own. §5.1's figure
caption states the rule in full ("A commit that changes a layer's stored-tile
set or index content re-emits that layer's whole tile-index region as well"),
so the narrow form here is an isolated stale restatement rather than a
convention.

Not byte-level. A writer that acted on the Note alone would decline to
re-emit an index it needs to re-emit, and would thereby simply fail to perform
the edit — the file it produced would still be conforming, so no byte
sequence's acceptance changes.

### diagrams-06 — OBSERVATION — §2.4's preserve-verbatim row points at a table scoped away from it

§2.4's outcome table:

> | **preserve-verbatim** | Binds updaters: the bytes are carried forward
> unmodified (relocated only as Part I permits). §20.4's table states the
> cases: its MU = 1 and MU = 0 / PE = 1 rows. |

§20.4 introduces that table with an explicit scope:

> For a type
> the updater does not implement, the
> stored flags are authoritative (§7.3, `[R-CNT-15]`; MU = 1 with
> PE = 0 is read as PE = 1, `[R-CNT-12]`), and carry these obligations:

and the table's own column is headed "Stored flags". In format major 1 the
only assigned record types are 0x0001 (layer) and 0x0002 (user metadata), and
for both of them the stored flags are precisely *not* authoritative —
`[R-CNT-22]` puts the registry's fixed values in charge, as §20.4's preceding
sentence says. So a reader following §2.4's pointer arrives at a table that,
by its own lead-in, governs neither of the two record types a conforming
format-major-1 file carries from the assigned range; the preserve-verbatim
obligation for those two is stated in prose instead ("both registered types
carry PE = 1, so neither can be dropped", and "No commit therefore removes a
layer record, or a user-metadata record at either scope").

The hazard is concrete if the pointer is taken at face value for the layer
type, whose registry-fixed flags are MU = 1, PE = 1. The MU = 1 row reads
"Retain byte-identical. The updater MUST NOT modify the scope the record
governs" — and the scope a layer record governs is the layer, so applied to a
layer record the row would bar every append §20.3 exists to describe. What
blocks that misreading is the row's own wording further in — "an *unknown*
critical record blocks modification of that layer" and "`[R-CNT-15]` makes an
*unimplemented* top-level MU = 1 record reject-file" — which shows the row is
written for types the updater does not implement, exactly as the lead-in says.

I pick the reading in which the table governs only unimplemented types and the
registered types take their persistence from §20.4's prose. Not byte-level:
two sentences in §20.4 and one in §7.3 decide it, and no updater following the
section as a whole could emit a directory the other reading forbids.

---

## Part 6 — Things I checked and found sound (recorded so coverage is auditable)

- §21.2's opening reasoning about which rows reach a foreign-major file names
  four rows (F8, F1, F14, F6) and the count is right; F18's treatment as
  "outside the premise" agrees with §21.6's closing paragraph.
- §21.1's specialization list (F1 of F6 and of F8, F35 of F36, L24 of L25) is
  correct; I looked for unlisted strict specializations and found none — in
  particular T6 is not a specialization of T11, because T11's condition
  excludes the all-ones value by name.
- §21.9's hard-limit paragraph claims exactly two limits do not follow from a
  field width, an external format, or the value domain. I derived all of them
  and confirmed exactly two are chosen: the 512 floor on A, and the 255-byte
  cap on a user-metadata key.
- §19.1/§19.3's enumerations are non-exhaustive but say so, in §19's preamble
  ("Those enumerations are not the complete inventory … §21's register is").
  I checked the F-rows and L-rows against them and every omission is covered
  by that disclaimer.
- §7.4's field list versus §21.3: every field in the layer-record table has at
  least one register row (name L3/L5/L6/F4, layout L36, linearization L33,
  codec L43, filter L45, A L39, S L1, A_slab L28/L29, d and C L32, dimension
  and channel names L4/L7/L8/L9, extents L1, types L34, fill L30/L35,
  index_encoding L31, entry_count L1/L21/L22, crc_of_crc_array L27/L37,
  sub-records L13/L14/L19/L24/L25/L26, A-with-S L20).
- L2's nine derived quantities dominate every other product the document
  derives: C·N dominates the maximum disk ordinal, P·Q dominates V = P·C
  (since Q = Σ Bᵢ ≥ C), N·P dominates ⌈P/8⌉ and each F_c ≤ Q.
- F33's cross-reference to the bounds rows (F9/F10, F31/F32, L16/L17, T8/T9)
  is complete: it covers the directory, non-layer top-level records, layer
  records and sub-records, and tile-index entries.
- §15.2's rationale about failure modes: a zeroed region parses as offset 0 /
  length 0 and trips both the length = 0 and the offset < 16 rows; an all-0xFF
  region trips the "crc ≠ 0 with sentinel offset and length" row. Both hold.
- §14.4's claim that a single-channel numeric layer produces byte-identical
  images under either layout: interleaved gives offset (k div 1)·Q + F₀ = k·B
  and size P·B; planar gives k·B and P·B. Identical.
- §17.2's Window_Size note: the two RFC 8878 derivations agree for a tile
  because Single_Segment_Flag ties Window_Size to the frame content size,
  which `[R-COD-06]` already ties to the decoded size, and the
  Window_Descriptor cannot express less than 1 KiB. The three small decoded
  sizes it points at (18, 30, 2) are all present in §14.2 and §14.3.
- §16.2's slab example: runs [0,8),[8,16),[16,24),[24,32) partition N = 32 at
  S = 8; a viewport over tile rows 1–2 is ordinals 8–23, exactly two runs.
- Appendix E's changelog has one row and a covenant for future revisions;
  Appendix F's normative references cover every external format the document
  cites (BCP 14, RFC 3720, IEEE 754, RFC 1951, RFC 8878, LZ4 Block, RFC 8259,
  RFC 3339, Unicode) and correctly marks OCP OFP8 informative.

## Confidence

An implementation built from this document alone would interoperate. I built
one file end to end and traced a second on paper without needing to guess a
single field width, offset, order or derived quantity; every constant the
document publishes reproduces from its own stated parameters; and every
byte-layout table, worked example and register count I checked is arithmetically
right. The six findings above are all defects of citation, restatement or
scoping in figures and register cells, none of which changes which byte
sequences may be emitted or must be accepted or rejected.
