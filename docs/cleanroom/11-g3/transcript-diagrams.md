# Round 11 — Diagram auditor — working transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,953 lines), in five `Read` chunks covering lines 1–3953 with no gaps. I ran
`wc -l` and two `grep`/`grep -o` passes against that same file (a requirement-ID
census, and a scan for normative keywords inside table rows). I wrote and ran one
Python script of my own creation, `scratchpad/round11/crc.py`, which reads no
files — it contains a CRC-32C implementation and three literal byte strings I
typed in from the document. I opened no ADR, no `docs/`, no `conformance/`, no
`spec/registry.json`, no `PLAN.md`, no `AGENTS.md`, no README. I ran no `git`
command, listed no directory, and issued no web request. I wrote this transcript
and the scratch script; I did not read the directory they live in.

Prior knowledge of DEFLATE/zstd/LZ4/JSON/CRC-32C was used only to generate
suspicions (e.g. "is the zlib wrapper really caught by T24 or T25?"). Every
conclusion below is settled against this document's own text, quoted.

---

## Part 0 — Inventory before judgement

The charter requires me to enumerate the figures before judging them. Here is the
census, by line number, from a `grep` for example/note headers plus a manual sweep
for fenced blocks, blockquoted layout sketches, and tables.

### Worked examples (19)

| line | what |
|---|---|
| 499 | §4.6 `température` NFC/NFD byte encoding |
| 561 | §5.1 the 128-byte minimal file, region by region |
| 568 | §5.1 a file after three commits (ASCII box) |
| 1125 | §9.2 what a crash sees (three-row ASCII figure) |
| 1424 | §11.2 grid arithmetic, (1024,2048)/(256,256) |
| 1478 | §11.4 spatial, in-tile and disk ordinals |
| 1541 | §12.1 bfloat16 1.0 and quiet NaN |
| 1590 | §12.3 a twelve-byte channel entry |
| 1658 | §13.3 interleaved and planar fill tuples |
| 1779 | §14.2 interleaved/planar byte offsets |
| 1813 | §14.3 packed bool plane `55 01` / `55 FD` |
| 1869 | §14.5 edge tile, 1 real + 15 padding positions |
| 1993 | §15.4 entry_count = 1,000,000 segmentation |
| 2008 | §15.4 planar disk ordinal 74, entries 96–127 |
| 2105 | §16.2 four slab runs over N = 32 |
| 2286 | §17.3 byte-shuffle of three float32 |
| 2831 | §20.3 cost of superseding one tile |
| 2840 | §20.3 the three shapes a commit takes (3 ASCII figures) |
| 2981 | §20.5 what compaction reclaims (ASCII figure) |

### Layout / rule-restating tables (23)

§2.4 outcome classes (227) · §6.1 front block (669) · §6.2 trailer (712) ·
§7.2 record header (876) · §7.3 record types (947) · §7.4 layer-record inline
payload (976) · §8.1 coverage map (1050) · §10.2 identifier spaces (1312) ·
§12.1 sample types (1507) · §14.2 decoded size / offset (1737) · §15.1 index
entry (1905) · §15.3 entry validity (1953) · §18.2 metadata encoding (2339) ·
§18.4 standardized keys (2463) · §20.4 updater obligations (2907) · §21.2 (3082)
· §21.3 (3126) · §21.4 (3183) · §21.5 (3224) · §21.6 non-violations (3242) ·
§21.9 limits (3337) · Appendix A annotation (3659) · Appendix B constants (3695).

### Other figures / checklists

§15.1's blockquoted region layout (1900) · Appendix A hexdump (3648) ·
Appendix C registry snapshot (3723) · Appendix D six choices (3750) ·
Appendix E changelog (3788) · Appendix F references (3799) ·
Appendix G reproducible-writer profile, 9 numbered items (3814) ·
Appendix H conformance checklists, 5 entries (3890).

---

## Part 1 — Arithmetic I actually did

### 1.1 CRC constants and the Appendix A trailer

I implemented CRC-32C from §4.5's parameters alone (Castagnoli, reflected in/out,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF), i.e. the reflected table constant
0x82F63B78, and checked it against §4.5's own check vector before using it:

```
CRC-32C("123456789") = 0xE3069283      §4.5 says 0xE3069283   OK
CRC-32C(zero bytes)  = 0x00000000      §4.5 says 0x00000000   OK
```

Then the two derived constants the document publishes:

```
CRC-32C(65536 x "FF x16 00 x4") = 0xEECB3BB2
    §15.4 / Appendix B say 0xEECB3BB2                          OK
```

Then Appendix A's trailer, transcribed from the hexdump at lines 3653–3656:

```
8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
01 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
04 00 00 00 00 00 00 00  80 00 00 00 00 00 00 00
EF CD AB 89 67 45 23 01  00 00 00 00 D2 38 09 E0

CRC-32C(trailer[0,60)) = 0xE00938D2
stored at [60,64) little-endian = D2 38 09 E0 = 0xE00938D2      OK
```

Appendix A is byte-correct. I then walked its annotation table against §6.2's
layout table, offset by offset, because a stale annotation is exactly the class of
defect this charter is for:

| §6.2 offset | +64 | Appendix A row | value | agrees |
|---|---|---|---|---|
| 0, 8, magic | 64 | [64,72) | `8A 4E 52 41 54 0D 0A 1A` | yes |
| 8, 2, version_major | 72 | [72,74) | `01 00` = 1 | yes |
| 10, 2, version_minor | 74 | [74,76) | `00 00` = 0 | yes |
| 12, 4, flags | 76 | [76,80) | zero | yes |
| 16, 8, generation | 80 | [80,88) | 1 | yes |
| 24, 8, dir_offset | 88 | [88,96) | 16 | yes |
| 32, 8, dir_length | 96 | [96,104) | 4 | yes |
| 40, 8, committed_file_length | 104 | [104,112) | 0x80 = 128 | yes |
| 48, 8, file_id | 112 | [112,120) | 0x0123456789ABCDEF | yes |
| 56, 4, reserved | 120 | [120,124) | zero | yes |
| 60, 4, CRC | 124 | [124,128) | 0xE00938D2 | yes |

The directory at [16,20) is `00 00 00 00`, which the annotation explains as "a
record sequence of zero bytes, followed by its CRC-32C — which for zero bytes is
0x00000000". Confirmed above. The pad [20,64) is 44 bytes, matching §5.1's example
("44 bytes of slack"). 16 + 4 + 44 + 64 = 128.

I also checked §5.1's floor argument independently: dir_offset ≥ 16 and
dir_length ≥ 4 force the directory to end at ≥ 20; `[R-CNT-06]` forces
dir_offset + dir_length ≤ F − 64, so F ≥ 84; F ≡ 0 (mod 64) gives F ≥ 128. The
prose ("cannot be satisfied in fewer") is correct.

### 1.2 Geometry, ordinals and byte layout

Every one of these I recomputed rather than eyeballed.

- §11.2: ⌈1024/256⌉ = 4, ⌈2048/256⌉ = 8, N = 32, P = 65,536. With E_y = 1000,
  ⌈1000/256⌉ = 4 (3.906…). Correct.
- §11.4: tile (1,0) → 1·8 + 0 = 8. (300,700) → t = (1,2), s = 1·8+2 = 10,
  u = (44,188), in-tile ordinal 44·256 + 188 = 11,452. Planar C = 4, c = 2:
  2·32 + 10 = 74. All correct.
- §12.3: `04` + `74 65 6D 70` + `0C 00` + `04` + `00 00 C0 7F` = 12 bytes, and
  0x7FC00000 little-endian is `00 00 C0 7F`. Correct, and the "twelve bytes"
  count is right (1+4+2+1+4).
- §12.1: binary32 1.0 = 0x3F800000, high 16 bits 0x3F80, stored `80 3F`. Correct.
- §14.2: Q = 1 + 2 = 3, decoded size 6·3 = 18; ordinal 5 at 5·3 = 15, `b` at
  16–17. Planar `b` = 6·2 = 12 bytes, ordinal 5 at byte 10. float32 + bool:
  Q = 5, size 30, ordinal 5 at [25,30), bool at 29. I also checked the table's
  general form: value k = u·C + c, offset = (k div C)·Q + F_{k mod C}; for
  k = 11, C = 2, Q = 3, F_1 = 1 that is 5·3 + 1 = 16. Consistent.
- §14.3: values alternating true,false from ordinal 0 give bits 0,2,4,6 set in
  byte 0 → 0b01010101 = 0x55; byte 1 holds values 8,9 = true,false → 0x01; fill
  true sets pad bits 2–7 → 0x01 | 0xFC = 0xFD. Both `55 01` and `55 FD` correct,
  ⌈10/8⌉ = 2.
- §14.5: ⌈5/4⌉ = 2 on both axes; edge tile (1,1) spans coordinates 4–7 on both
  axes = 16 positions, of which only (4,4) is inside E = (5,5) → 1 real, 15
  padding. P·B = 16·2 = 32 bytes. Ordinal 0 is in-tile (0,0) = coordinate (4,4),
  so "value 0 is the stored sample" is right and 0xABCD little-endian is `CD AB`.
  Correct. (The example does not name a layout; I checked both — single numeric
  channel gives 32 bytes either way, which §14.4's note asserts. Consistent.)
- §15.4 #1: ⌈10^6/65536⌉ = 16 segments; 10^6 − 15·65536 = 16,960 in the last;
  array = 64 bytes; region = 20,000,000 + 64. k = 999,999 → segment 15, index
  999,999 − 983,040 = 16,959, byte 339,180. Segment 15 spans
  [15·65536·20, 20,000,000) = [19,660,800, 20,000,000) = 339,200 bytes; plus the
  64-byte array ≈ 339 KB. Full segment = 65,536·20 = 1,310,720 = 1.25 MiB.
  Every figure in that example is right.
- §15.4 #2: 20·74 = 1,480; channel 3's block is [96,128) = 32 entries. Correct.
- §16.2: N = 32, S = 8 → runs [0,8),[8,16),[16,24),[24,32); tile rows 1–2 are
  ordinals 8–23 = runs 1 and 2 exactly. Correct.
- §17.3: 1.0/2.0/3.0 float32 LE = `00 00 80 3F | 00 00 00 40 | 00 00 40 40`;
  s = 4, n = 3; output[i·3 + j] = group j byte i gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40`. Matches the example byte for byte.
- §19.4's note: entries for one spatial ordinal are N apart; N ≥ 2^16 means the
  ordinal gap is at least one whole segment, so different segments. Correct, and
  correctly *not* claimed for N < 2^16.
- §20.3: 32·20 + 4 = 644. Correct (one segment CRC, since 32 ≤ 65,536).
- §20.3 note: 10^6 · 20 = 20 MB. Correct.
- §21.9 note: 2^32 / 2^16 = 2^16 segments · 4 B = 256 KiB; at 2^36 it is 2^20 · 4
  = 4 MiB. Correct. 12.5 MiB / 65,536 = 200 B per layer record, which is what
  "the small layer records that figure assumed" must mean; the note is honest
  that the 16 MiB directory row restates the same budget over the region.
- §24's claim that the tile-count guarantee is not constructible: 2^32 · 20 +
  2^16 · 4 ≈ 85.9 GB, "tens of gigabytes". Correct.

### 1.3 The register's own counts

§21.8 asserts "121 conditions over 248 instances". I counted both mechanically,
using §21.1's stated rule ("Instances within a cell are separated by semicolons,
and a cell reading — is one instance").

Conditions: §21.2 F1–F36 = 36 (header says 36); §21.3 L1–L49 = 49 (header says
49); §21.4 T1–T26 = 26 (header says 26); §21.5 R1–R10 = 10 (header says 10).
36+49+26+10 = **121**. Matches.

Instances, cell by cell:

- §21.2: F1 2, F2 6, F3 2, F4 1, F5 2, F6 2, F7 1, F8 1, F9 1, F10 1, F11 1,
  F12 1, F13 1, F14 1, F15 1, F16 1, F17 1, F18 1, F19 1, F20 1, F21 1, F22 1,
  F23 1, F24 1, F25 1, F26 1, F27 1, F28 2, F29 3, F30 2, F31 1, F32 1, F33 5,
  F34 1, F35 1, F36 1 → **53**
- §21.3: L1 8, L2 9, L3 1, L4 2, L5 1, L6 1, L7 2, L8 2, L9 2, L10 1, L11 1,
  L12 1, L13 1, L14 3, L15 4, L16 2, L17 2, L18 3, L19 1, L20 1, L21 1, L22 3,
  L23 4, L24 1, L25 1, L26 1, L27 1, L28 1, L29 3, L30 1, L31 3, L32 3, L33 4,
  L34 4, L35 1, L36 2, L37 1, L38 1, L39 3, L40 1, L41 1, L42 1, L43 3, L44 1,
  L45 3, L46 2, L47 2, L48 1, L49 4 → **106**
- §21.4: T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1, T11 2,
  T12 1, T13 2, T14 1, T15 2, T16 1, T17 1, T18 4, T19 1, T20 1, T21 1, T22 1,
  T23 1, T24 1, T25 3, T26 3 → **45**
- §21.5: R1 4, R2 2, R3 2, R4 12, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2 → **44**

53 + 106 + 45 + 44 = **248**. Matches §21.8 exactly. This is the single most
falsifiable claim in §21 and it holds.

I also verified two arithmetic side-claims inside L2's instance cell:
C·N does dominate (C−1)·N + (N−1) = C·N − 1; and P·Q dominates V = P·C because
Q = Σ B_i ≥ C (each B_i ≥ 1). Both correct.

### 1.4 Value-space cross-checks

§10.2's table against the eight owning sections, and against Appendix C:

| space | §10.2 | owning section | Appendix C | agree |
|---|---|---|---|---|
| record type | 1,2 / 3–0x7FFF / ≥0x8000 | §7.3 + `[R-CNT-15]` | 0x0001, 0x0002 | yes |
| channel layout | 1,2 / 3–255 / none | §14.1 `[R-SER-06]` | 1,2 | yes |
| linearization | 1 / 2–0x7FFF / ≥0x8000 | §11.4 (2–3, then 4–0x7FFF) | 1 | yes |
| sample type | 1–13 / 14–0x7FFF / ≥0x8000 | §12.2 (14–19, then 20–0x7FFF) | 1–13 + pins | yes |
| codec | 1–4 / 5–0x7FFF / ≥0x8000 | §17.2 | 1–4 | yes |
| filter | 1,2 / 3–0x7FFF / ≥0x8000 | §17.3 | 1,2 | yes |
| index encoding | 1 / 2–0x7F / ≥0x80 | §7.4 table row | 1 | yes |
| metadata encoding | 1,2 / 3–0x7F / ≥0x80 | §18.2 | 1,2 | yes |

The register's four-way and three-way instance splits track the *sections'*
sub-divisions, not §10.2's coarser ones: L33 has four (0 / 2–3 / 4–0x7FFF /
≥0x8000), L34 has four (0 / 14–19 / 20–0x7FFF / ≥0x8000), L31/L43/L45 have three,
L36 has two (no experimental range for a u8 layout). Every one matches the owning
section. §12.1's thirteen element sizes all check against §14.2's arithmetic and
against Appendix H's "all thirteen sample types". Appendix C's pins (14/15 OFP8
E4M3/E5M2, 16/17/18 int128/uint128/float128, 19 opaque) match §12.2's note.

One reference does not check out — see finding **diagrams-08**.

### 1.5 §15.3's table against §21.4

§15.3 says "Six rows are marked *structural*". I counted the table: sentinel with
crc ≠ 0; exactly one half sentinel; length 0; offset < 16; offset or length above
2^63 − 1; sum overflow or sum > F − 64. Six. The non-structural rows are the crc
failure and three *verifier* rows. Mapping to §21.4: T6, T7, T10, T8, T11,
T9/T12 (the sixth row splits into two register rows, which §21.1's instance rule
permits); T1 is the crc row; L18 / F33 / L40–L42 are the verifier rows. The
partition is complete in both directions.

### 1.6 §8.1's coverage map against §4.5

§4.5 names three terminal checksum fields (trailer, directory-region,
user-metadata) and three interior ones (segment CRC array, entry crc,
crc_of_crc_array). §8.1's map delivers exactly those: the segment CRC array is
covered by crc_of_crc_array (row 4), the entry crc is inside "index entries, per
segment" (row 4), and crc_of_crc_array is a layer-record field inside the
directory region (row 3). The seventh row is the unassigned-type extent, covered
by nothing, which §4.5 also names. The map is closed.

§8.2's chain has seven links; §15.4 and §19.4 step 3 restate the same two-link
prefix. Outcomes match F14/F20 (file), L21/L22/L37/L38 (layer), T1 (tile),
R2 (ignore-record).

### 1.7 Register completeness, spot-audited

§21.1 makes completeness normative. I walked every MUST-level file-conformance
condition I could find and looked for its row. Everything I traced landed:
`[R-CNT-05]`→F7, `[R-CNT-27]`→F5, `[R-ENC-02]`→F1, `[R-ENC-15]`→F4/L9,
`[R-CNT-14]`→F34/L19, `[R-CNT-16]`→L20, `[R-CNT-17]`→L21/L22, `[R-COD-07]`→L44,
all six `[R-COD-06]` frame constraints→T17–T22 (and §17.2's "Three frame features
are excluded" does name exactly three: dictionary, content-checksum, oversized
window), `[R-COD-05]`→T15/T16, `[R-SER-05]`→T4/T5, `[R-SER-08]`→T2,
`[R-COD-10]`→T26, `[R-MTA-04]`'s four restrictions→R5–R10, `[R-MTA-05]`→F27/L48,
`[R-CNT-22]`→F28/L49. The three conditions the document deliberately leaves
unregistered are each excused in place: nesting depth (§7.4's note), stale slab
declaration (§16.2's note), "belongs to no class" (§5.2's note). I found no
missing row.

I did find one class of obligation that fails detectability and is not accounted
for where §21.1 promises the account lives — finding **diagrams-09**.

---

## Part 2 — Findings

### diagrams-01 — CONTRADICTION — the promised layout-table columns are not the columns two layout tables deliver

**Location.** Front matter (the "How to read this document" note, lines 12–20);
§4.7's note (lines 523–533); §6.1's table (lines 669–672); §7.2's table (lines
876–882).

Two places promise what a layout table contains, and they promise different
things:

> On-disk structures are presented as offset/size/type/name/valid-range tables.
> — front matter

> **Note.** Layout tables for fixed-layout structures give, per field: byte
> offset within the structure, size, type, name, taxonomy class, and valid
> range. A packed variable-length payload — the layer record's inline payload
> (§7.4) — has no fixed offsets to give; its table omits the offset and class
> columns, and each field's class follows from the definitions above.
> — §4.7

The §4.7 note carves out exactly one exception (§7.4's packed payload, which
omits offset and class) and by doing so asserts that every *other* layout table
delivers all six. Checked against what the document contains:

| table | Offset | Size | Type | Name/Field | Class | Valid range |
|---|---|---|---|---|---|---|
| §6.2 trailer | yes | yes | yes | yes | yes | yes |
| §15.1 index entry | yes | yes | yes | yes | yes | yes |
| §18.2 metadata encoding | yes | yes | yes | yes | yes | yes |
| **§6.1 front block** | yes | yes | **no** | **no** | yes | as "Value" |
| **§7.2 record header** | yes | yes | yes | yes | yes | **no** |
| §7.4 inline payload | (excepted) | | yes | yes | (excepted) | as "Constraint" |

§6.1's table is `| Offset | Size | Value | Class |` — four columns, no type and no
field-name column at all. §7.2's is `| Offset | Size | Type | Field | Class |` —
five columns with no valid-range column; the constraints that would live there
are smuggled into the Field cells ("type (0 invalid)", "flags: bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved"). The front block is
unmistakably a fixed-layout structure ("Bytes [0, 16) of every file, constant in
every format major version"), and so is the 24-byte record header ("Each record
is a 24-byte header followed by inline_length bytes of inline payload").

And the two promises disagree with each other: the front matter lists five
columns and omits the taxonomy class, which §4.7 was evidently rewritten to make
central ("Every field is classified as **structural** … **semantic** … or
**descriptive** (neither — §4.7)" appears in the same front-matter note, so the
note both asserts universal classification and omits the class column from its
own table description).

**Permitted readings.** (a) The note describes an ideal the tables should meet and
two tables fall short — a documentation defect. (b) The note's list is a menu, not
a promise, and a table gives whichever of the six apply — but then the explicit
carve-out for §7.4 ("its table omits the offset and class columns") is pointless,
since under (b) no carve-out is needed. I take (a): the singling-out of §7.4 is
only meaningful if the list is otherwise exhaustive.

**What an implementer does wrong without it.** Nothing to the bytes. But a tool
that generates parsers or a reviewer auditing table completeness — which is what
§4.7's note invites — will look for a valid-range column on the record header and
a type/name column on the front block, find neither, and cannot tell whether the
omission is deliberate or an editing slip. It also leaves the record header the
only fixed structure whose field constraints are stated in prose inside a Field
cell rather than in the column the document says holds them.

**Byte-level?** No. Neither table's *content* is wrong; §7.2's constraints are all
present, merely in the wrong cell, and §6.1's two rows are unambiguous. No
implementation could emit or accept a different byte because of this.

---

### diagrams-02 — CONTRADICTION — Appendix G's closing "Four things are not [already mandatory]" undercounts the freedoms the profile's own nine items close

**Location.** Appendix G, closing paragraph (lines 3881–3888), against Appendix
G items 1, 2, 4, 5, 6, 8, 9.

> Everything else the profile needs is already mandatory — fill-encoded edge
> padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among them.
> Four things are not, and the items above are where the profile adds them: gap
> *content*, which `[R-CNT-03]` only advises; gap *extent*, which placement
> freedom (`[R-SLB-05]`) leaves open; sub-record order within a layer record's
> inline payload, which `[R-CNT-14]` leaves free; and the fill a writer records
> when its caller chooses none, which `[R-TYP-10]` states as a SHOULD.

The claim is a claim about this document's own contents: everything the profile
needs is already mandatory except four named things. It is false on the
profile's own face. At least these further freedoms are closed by the numbered
items and are not among the four:

- **Item 6.** "**The sentinel for every all-fill tile**, so that a tile whose
  samples all equal fill is never stored". Nothing in the normative text
  requires this. §13's whole architecture is that an unstored tile *reads as*
  fill (`[R-TYP-08]`); it nowhere forbids storing a tile whose decoded values
  all happen to equal fill. This is a fifth freedom, and the profile itself
  knows it: item 7 says "item 6 stores no tile whose samples all equal fill, so
  two writers that default fill differently disagree about which tiles exist".
- **Item 2.** Deriving `file_id` from a hash. §9.3 requires only nonzero and
  *advises* a cryptographically random source; any nonzero value is conforming.
- **Item 8.** "`version_minor` at the floor `[R-CNT-26]` states". `[R-CNT-26]`
  is a SHOULD ("A writer SHOULD emit the lowest version_minor that defines every
  feature present in the file"), so the profile promotes a second SHOULD to a
  requirement exactly as item 7 does with `[R-TYP-10]` — and item 7's promotion
  *is* one of the four while item 8's is not.
- **Item 5.** "**No declared alignment and no slab**, or fixed declared values".
  A writer is free to declare or not (`[R-SLB-01]`, §16.2).
- **Item 4.** "**One generation**". A conforming file may stand at any
  generation.

**Permitted readings.** (a) "Four things" counts *format* degrees of freedom, so
items 1 and 9 (encoder/serializer pinning, which are properties of software, not
of the format) are excluded — plausible, but that defence does not reach items
2, 4, 5, 6 or 8, all of which are format freedoms. (b) "Four things" was written
against an earlier, shorter item list and was not re-counted. I take (b).

**What an implementer does wrong without it.** A reader auditing the gap between
core conformance and the profile — which is the paragraph's entire purpose — will
conclude that item 6 restates a mandatory rule, i.e. that a conforming writer may
not store an all-fill tile. That is wrong, and it is wrong in a direction that
changes which files a writer produces. The normative text decides the question
(nothing forbids storing such a tile), so the error is recoverable; but the
paragraph is the one place a reader is told which items are additions and which
are restatements, and it misfiles at least five of nine.

**Byte-level?** No. Appendix G is labelled non-normative and states outright that
"It adds no requirement to any actor: a writer ignoring it is fully conforming."
A writer that stores an all-fill tile emits a conforming file under §13 and §15
regardless of how this paragraph is read; no verifier verdict turns on it.

---

### diagrams-03 — AMBIGUITY — Appendix G item 2's `file_id` hash input is not well defined, and one reading is circular

**Location.** Appendix G, item 2 (lines 3834–3842).

> 2. **`file_id` from a cryptographic hash of the file's own emitted
>    bytes**, computed over [0, F − 64) together with the trailer's
>    other fields with the `file_id` field taken as zero, then written
>    in. Deterministic, and high-entropy …

The trailer occupies [F − 64, F), so [0, F − 64) is everything before it. The
hash input is then "the trailer's other fields", i.e. the trailer minus
`file_id`. But by §6.2 the trailer's last field is the trailer CRC at trailer
offset 60, and by §6.2's table that CRC is taken "over trailer bytes [0, 60)" —
which *includes* `file_id` at trailer offset 48. So on the literal reading:

- file_id = H( [0, F−64) ‖ trailer fields other than file_id ), and
- trailer CRC ∈ "trailer fields other than file_id", and
- trailer CRC = CRC-32C(trailer[0,60)) which contains file_id.

That is circular and cannot be executed.

**Permitted readings.** (a) *Exclude the CRC entirely*: hash [0, F−64) plus the
eight content fields (magic, version_major, version_minor, flags, generation,
dir_offset, dir_length, committed_file_length, reserved), then write file_id,
then compute the CRC last. Executable. (b) *Zero the file_id in place and hash
the whole 64-byte trailer*, having first computed the CRC over the
file_id-zeroed trailer — the phrase "with the `file_id` field taken as zero"
reads naturally as zeroing a field in situ, and this is executable too, but
yields a different hash from (a). (c) *Zero both file_id and the CRC field* and
hash the 64 bytes — a third distinct value. (d) The literal reading — circular,
so not permitted.

I pick (a): "the trailer's *other fields*" is field vocabulary, not byte
vocabulary, and §6.2's CRC is a derived field rather than emitted content, so a
recipe that says "then written in" is describing a two-pass write in which the
CRC is necessarily last. But (b) is defensible on the plain sense of "with the
file_id field taken as zero", and I cannot rule it out from the text.

**What an implementer does wrong without it.** Two implementations adopting the
profile with codec 1 — the one case where Appendix G item 1 says byte-identity
across implementations *is* attainable ("codec 1 is reproducible by anyone") —
emit different `file_id` bytes at [F−56, F−48) for the same logical content, and
therefore different trailer CRCs, and therefore two different 128+-byte files.
Each would judge the other to have failed the profile. The profile's stated test
("conformance to the profile can be refuted cheaply but confirmed only by
reproducing the file") turns on precisely this.

**Byte-level?** No, though it is the closest call in this walk. The fork is real
and it is a fork in emitted bytes, but it is a fork in *profile* output, not in
what a conforming writer may emit: §6.2 admits any nonzero `file_id`, so every
one of readings (a), (b) and (c) produces a fully conforming file that every
conforming reader must accept, and no verifier verdict differs. Profile
conformance is not one of §2.3's five classes.

---

### diagrams-04 — CONTRADICTION — `[R-VEC-04]` relies on a manifest "detector field" that `[R-VEC-02]`'s minimum field list does not include

**Location.** §24, `[R-VEC-02]` (lines 3573–3579) against `[R-VEC-04]` (lines
3598–3604).

`[R-VEC-02]` states the manifest's promised field set:

> Each vector is one file plus a manifest entry recording, at minimum:
> its identifier; whether the file is **conforming**; the decoded
> content a reader is to return from every scope it can read, with each
> floating-point value written as a hexadecimal bit pattern so that no
> comparison depends on a number formatter; and, for each structure the
> file damages, the outcome class (§2.4), the scope, and the §21
> register row it exercises.

Four kinds of entry, and for each damaged structure exactly three: outcome class,
scope, register row. No detector.

`[R-VEC-04]` then reads a fourth off the entry, and cites `[R-VEC-02]` for it:

> Where it is the verifier, no reader is obliged to refuse anything
> (§21.1), so the pair is the scope at which a verifier confines its
> finding — carried by the entry's own scope and detector fields
> (`[R-VEC-02]`) — and the content a reader owes from every scope, the
> damaged one included.

"the entry's own scope and **detector** fields (`[R-VEC-02]`)" names a field the
cited requirement does not require.

**Permitted readings.** (a) The detector is recoverable from the recorded register
row, since every row of §21.2–§21.5 carries a Detector cell — so `[R-VEC-04]`
is loosely calling the row's Detector cell "the entry's own field". (b)
`[R-VEC-02]`'s list is a minimum ("at minimum"), so a corpus is free to add a
detector field, and `[R-VEC-04]` silently requires it. I take (b) as the
operative reading, because `[R-VEC-04]` says "the entry's own … fields", which
distinguishes them from the register's; but under (b) `[R-VEC-02]`'s enumeration
is incomplete and its citation misleading, and under (a) the phrase "the entry's
own" is simply wrong.

**What an implementer does wrong without it.** A corpus builder implementing
`[R-VEC-02]` literally emits manifests with identifier / conforming / decoded
content / (outcome, scope, row) and no detector column. `[R-VEC-04]`'s two-branch
rule — verifier-detected rows expect the damaged scope's content to be *served*,
reader-detected rows expect it to be *refused* — then has no field to switch on
inside the entry, and a harness must join back to §21's tables to know which
expectation applies. That is a real interoperability gap between two tools
reading the same manifest.

**Byte-level?** No. It governs manifest schema, not file bytes; nothing here
changes what a conforming file may contain or what a reader must accept.

---

### diagrams-05 — CONTRADICTION — Appendix H's updater checklist forbids removing a user-metadata record "at either scope"; §20.4's own consequence sentence covers only file scope

**Location.** §20.4 (lines 2913–2914) against Appendix H's updater entry (lines
3931–3932).

§20.4:

> No commit therefore removes a layer record or a file-scope
> user-metadata record.

Appendix H:

> never removes a layer record, or a
> user-metadata record at either scope (§20.4);

Appendix H cites §20.4 for a proposition §20.4's own summarising sentence does
not state. The two are not both restatements of the same rule: one says
file-scope user metadata is unremovable, the other says user metadata at file
*and* layer scope is unremovable.

Working out which is right from the governing text: §20.4's table preamble says

> Persistence governs every record type; only the authoritative source
> of the flags differs. For a type §7.3 registers, the registry's fixed
> flags govern rather than the stored ones (`[R-CNT-22]`) — both
> registered types carry PE = 1, so neither can be dropped …

§7.3's table fixes type 0x0002 at MU = 0, PE = 1 with Scope "file when
top-level; layer as sub-record" — one registration covering both placements. And
a conforming updater necessarily implements type 0x0002, since §2.3 makes both
assigned user-metadata encodings core, so the "type the updater does not
implement" branch (where stored flags govern and MU = 0 / PE = 0 licenses a
drop) can never reach it. Therefore PE = 1 governs at both scopes and Appendix H
is substantively correct; §20.4's sentence is under-inclusive.

**Permitted readings.** (a) §20.4's sentence is an incomplete consequence of a
complete rule, and the rule governs — the reading I take. (b) *Expressio unius*:
§20.4 names file scope deliberately, so a layer's user-metadata sub-record is
droppable. (b) is defeated by "both registered types carry PE = 1, so neither can
be dropped", which is unqualified by scope, but a reader who stops at the
summary sentence will not see that.

**What an implementer does wrong without it.** An updater on reading (b) drops a
layer's user-metadata sub-record during a commit that independently modifies that
layer, and silently loses application state — the loss §20.4's own last table row
calls for a report about ("An updater that drops such a record SHOULD report the
loss; unreported, application state disappears with no diagnostic"), except here
no diagnostic is even contemplated because the updater believes the drop is
licensed.

**Byte-level?** No. The general rule already decides it — "both registered types
carry PE = 1, so neither can be dropped" is unconditional, and Appendix H states
the same. The narrower sentence is a stale restatement, not a competing rule.
This is also not a rule about file conformance: both an updater that drops and
one that retains emit a *conforming file*; what differs is whether the updater is
a conforming updater, and §20.4's table plus `[R-CNT-22]` settle that without
recourse to the summary sentence.

---

### diagrams-06 — CONTRADICTION — Appendix A ties the front-block check to a *local reader*; §6.1 was written to tie it to residency and to disclaim exactly that

**Location.** Appendix A's closing prose (lines 3677–3688) against §6.1 (lines
676–695) and §19.1 step 1 (lines 2527–2537).

§6.1 defines the local/remote distinction and then explicitly bounds it:

> That distinction governs the request accounting of §6.4 and nothing
> else; the obligation over the front block turns on residency instead,
> because a transport can be classified either way at the margin while
> residency is decidable at any reader's own open path.

and the obligation itself is stated on residency:

> A reader whose open leaves bytes
> [0, 16) **resident** — a local file read whole, a memory mapping, a
> speculative suffix window that reached offset 0, or any transport
> already holding them — and a content sniffer MUST verify the full block by byte
> equality before other processing … The test is residency, not transport,
> so an implementation decides it at its own open path without having to
> classify the network underneath it. `[R-CNT-04]`

§19.1 step 1 and §19.2's "at open" bullet both use residency, and F6's Condition
cell restates it correctly ("the obligation binds a reader holding those bytes
resident"). Appendix A does not:

> A local reader additionally verifies bytes [0, 16) by equality first,
> which `[R-CNT-04]` requires of any reader holding them — as a remote
> reader does too whenever its speculative suffix window reaches offset
> 0 …

The sentence's main clause predicates the obligation on being a *local reader*,
which is precisely the transport classification §6.1 says governs "the request
accounting of §6.4 and nothing else". Its own subordinate clause then restates
the residency rule correctly, and the following sentence handles the remote case
by residency ("bytes [0, 16) stay non-resident, so §6.1 leaves the front-block
check to the reader"). So the appendix carries both the current rule and a
residue of a transport-scoped one, in adjacent clauses.

The gap is not empty. §6.1's definition of a local reader is "one whose transport
serves any byte range at no per-range round trip — a local file or a memory
mapping being the ordinary cases". A local reader that `pread`s only the final 64
bytes and then only [dir_offset, dir_offset+dir_length) is a local reader that
never holds [0, 16). Appendix A says such a reader verifies the front block; §6.1
says it need not.

**Permitted readings.** (a) Appendix A is loosely equating "local" with "reads the
whole 128-byte file", true of the ordinary case for a file this small — the
reading I take, since the appendix is non-normative and its subordinate clause
gives the right test. (b) Local readers really do owe the check regardless of
residency, which would contradict §6.1's "nothing else" sentence outright.

**What an implementer does wrong without it.** Under (b) an implementation that
opens local files by seeking to the tail believes it must additionally fetch and
compare [0, 16), and reject a file whose front block is damaged — where §6.1 and
F6 licence it to skip. That is a divergence in accept/reject on a corrupted front
block. But §6.1 and F6 both settle it: non-resident readers MAY defer or omit.

**Byte-level?** No. §6.1's "MAY defer or omit" and F6's Condition cell make both
behaviours conforming by construction, so the two implementations do not
*disagree* about a verdict this document fixes — the document deliberately leaves
that verdict to the reader. Resolving Appendix A's wording changes no obligation.

---

### diagrams-07 — OBSERVATION — §21.5's R7 enumerates an instance ("leading U+FEFF") that its own Condition cell does not state, contrary to §21.1's definition of an instance

**Location.** §21.5, row R7 (line 3232), against §21.1 (lines 3052–3065) and
§18.2's first restriction (lines 2393–2395).

R7 in full:

> | R7 | A decoded user-metadata document is not well-formed JSON, or
> its top-level value is not an object | not well-formed JSON,
> top-level document; not well-formed JSON, layer sub-record document;
> top-level value not an object, top-level document; top-level value
> not an object, layer sub-record document; leading U+FEFF, top-level
> document; leading U+FEFF, layer sub-record document | reader | extent
> use | `[R-MTA-04]` (R-CNT-25) |

§21.1 fixes what an instance may name:

> An instance names a field the condition ranges over, a
> container it can occur in, one of several alternatives the condition
> text states, or any combination of the three …

R7's Condition text states two alternatives (not well-formed JSON; top-level
value not an object) over two containers = four. The cell delivers six, adding a
third alternative — the byte-order mark — that the Condition text does not state.
It is a genuinely distinct alternative, not a specialization of the other two:
§18.2 makes the BOM independently fatal —

> **A JSON object, unmarked.** The top-level value is an object,
> and the encoding carries no byte-order mark: a leading U+FEFF
> makes the document unreadable.

— precisely because a leading U+FEFF is *not* by itself a JSON well-formedness
failure that every parser reports (RFC 8259 leaves BOM tolerance to
implementations, which is why §18.2 spells it out).

**Permitted readings.** (a) The Condition cell should read "…, its top-level value
is not an object, or it carries a leading U+FEFF" and the instance count of six
is right — the reading I take, since §18.2's restriction is titled "A JSON
object, unmarked" and plainly carries three obligations. (b) The Condition text
is right and the two BOM instances are spurious, which would make §21.8's
248-instance total wrong by two.

**Cost of deciding.** Cheap in itself; I record it as an OBSERVATION rather than an
AMBIGUITY because reading (b) is refuted by §21.8's arithmetic, which I recounted
above and which comes out at exactly 248 *with* the two BOM instances included.
So the document has already voted for (a) mechanically, and only the Condition
cell's prose lags.

**What an implementer does wrong without it.** A corpus builder generating vectors
from Condition cells rather than Instances cells builds four R7 vectors instead of
six and never exercises the BOM rule, which is a gap in exactly the place §18.2
went out of its way to close by hand.

**Byte-level?** No. `[R-MTA-04]` states the BOM rule in normative prose and
`[R-CNT-25]` fixes its outcome (ignore-record); no reader's behaviour depends on
R7's phrasing.

---

### diagrams-08 — OBSERVATION — the index-encoding value set is attributed to §15.1 in three normative places, and §15.1 states no value set

**Location.** §10.2's table row (line 1320), §10.3 (lines 1340–1341), §19.3 (line
1631), §21.3 row L31's Governing rule cell (line 3158), against §15.1 (lines
1891–1913) and §7.4's table row (line 990).

`[R-EXT-03]` sends a reader to §15.1 for this space:

> A reader
> encountering either treats it as its space's rules require: a
> validity error at the owning scope for the value sets of §11.4,
> §12.2, §14.1, §15.1, §17.2, and §17.3;

and `[R-RDR-03]` repeats the same six-section list ("the value sets of §11.4,
§12.2, §14.1, §15.1, §17.2, and §17.3"). §10.2's table cites "index encoding
(§7.4, §15.1)". L31 cites "`[R-CNT-23]` (§15.1)".

For five of those six sections the cited section does state the set: §11.4 states
linearization's four-way split, §12.2 the sample type's, §14.1 the layout's,
§17.2 the codec's, §17.3 the filter's. §15.1 states none. The whole of what §15.1
says about the field is parenthetical:

> Under
> index_encoding 1 (the only encoding this format major version defines,
> §7.4), the tile-index region addressed by the layer record's extent
> slot is, contiguously:

The set is stated only in §7.4's table:

> | index_encoding | u8 | 1 = raw-segmented; any other value —
> including 0, reserved 2–0x7F, and the experimental range ≥ 0x80
> (§10) — is a validity error at layer scope (§15) |

This matters because `[R-EXT-05]` makes section-of-definition the tiebreaker:
"Where the registry, §10.2's table, and Appendix C diverge, the section that
defines the space governs". For seven of the eight spaces that section is
unambiguous. For index encoding, the document's own cross-references name §15.1,
which defines nothing, while §7.4 — cited only first in §10.2's cell and not at
all by `[R-EXT-03]` or `[R-RDR-03]` — is where the definition lives. §7.4's cell
even points onward to "(§15)", completing a loop.

**Permitted readings.** (a) "§15.1" is shorthand for "the index encoding space,
whose semantics §15.1 gives for value 1" and §7.4 remains the defining section —
what I take. (b) §15.1 is meant to be the defining section and the value set was
never moved there, in which case a future divergence between §7.4 and the
registry has no arbiter.

**Cost of deciding.** Low to decide, but it requires reading §15.1 in full to
discover the absence, which is why I file it as an OBSERVATION.

**What an implementer does wrong without it.** Nothing to the bytes: §7.4 and
§10.2 agree exactly (1 assigned, 2–0x7F reserved, ≥0x80 experimental) and L31's
three instances match. The cost is to a maintainer applying `[R-EXT-05]`.

**Byte-level?** No. Every statement of the set in the document agrees.

---

### diagrams-09 — OBSERVATION — §21.7 is nominated as "the account, by class, of what fails" detectability, and omits the updater-preservation class

**Location.** §21.1 (lines 3032–3036) against §21.7's second paragraph (lines
3304–3316) and §20.4 / `[R-WRT-05]` / `[R-CNF-06]`.

§21.1 pins the division of labour:

> Its **completeness is normative** — a
> *detectable* file-conformance violation this specification names and
> the register omits is a defect in this document, detectability being the gate
> `[R-CNF-07]` already applies and §21.7 the account, by class, of
> what fails
> it …

§21.7's second paragraph then gives that account:

> A second set of obligations is omitted from the register because a
> single file exhibits no witness of their violation. Committed-prefix
> immutability and the generation sequence (`[R-LIF-01]`,
> `[R-LIF-03]`) are properties of a file's history, which §9.7 does
> not reconstruct; the ordinal mappings of `[R-GEO-06]` and
> `[R-SER-01]` are satisfied by a structurally valid tile whatever
> values it carries; `[R-CNT-13]`'s prohibition on an MU = 0
> record encoding file offsets in its own payload is opaque by
> construction; and `[R-ENC-06]`'s fixed field widths are not a state a
> file can be in …

Five obligations, in four classes. The updater preservation obligations are not
among them, and they belong to exactly this set. `[R-WRT-05]` — "an updater MUST
re-emit byte-identically — header, inline payload, and extent slot — every record
it retains and does not logically modify" — and §20.4's table rows ("Retain
byte-identical", "The updater MUST NOT modify the scope the record governs"), and
`[R-CNF-06]`'s "MUST honor the preservation obligations of §20.4", are MUST-level
obligations whose violation leaves no witness in the resulting file: a directory
missing a record it should have carried forward is, on its own bytes,
indistinguishable from a directory that never had it. §9.7 does not reconstruct
prior generations ("Nothing here enumerates prior commits"), which is precisely
the ground §21.7 gives for `[R-LIF-01]` and `[R-LIF-03]`.

Correspondingly they carry no register row, which is right — and §21.7 is where
the document promises to say why, and does not.

**Permitted readings.** (a) They fall under the history class §21.7 already opens
("properties of a file's history"), which names only `[R-LIF-01]` and
`[R-LIF-03]` but might be read as exemplary rather than exhaustive — the reading
I take. (b) The paragraph's list is closed and the preservation obligations are
an unaccounted-for gap in a completeness account §21.1 makes normative.

**Cost of deciding.** This is the expensive kind: settling it means walking every
MUST in §20 and asking of each whether a single file witnesses its violation. I
did that walk for §20.4 and §20.5 and found `[R-WRT-05]`, `[R-CNF-06]` and
§20.4's MU = 1 row all witness-free, plus `[R-WRT-06]`'s and `[R-WRT-09]`'s
refuse-to-compact duties, plus `[R-WRT-08]`'s bar on re-encoding — none of which
appear in §21.7. Hence OBSERVATION.

**What an implementer does wrong without it.** Nothing directly. The exposure is
to a future editor: §21.1 makes the register's completeness normative and points
at §21.7 as the exhaustive residue, so an obligation in neither place looks like
an oversight rather than a decision, and the next revision may "fix" it by adding
a row no file can exhibit — the very error §5.2's note warns against for
`[R-CNT-02]`.

**Byte-level?** No. It is an accounting question about which obligations are
unregisterable; no file's acceptance turns on it.

---

### diagrams-10 — OBSERVATION — the front matter says test vectors cite requirement identifiers; §24 requires them to cite register rows, and never requires the identifier

**Location.** Front matter, "How to read this document" note (lines 18–20),
against §24's `[R-VEC-02]` (lines 3573–3579) and §21.8's `[R-ERR-02]` (lines
3320–3323).

Front matter:

> Normative requirements carry
> stable identifiers like `[R-IDX-03]`, and test vectors cite those
> identifiers rather than prose positions.

`[R-VEC-02]`'s minimum manifest entry records, for each damaged structure, "the
outcome class (§2.4), the scope, and the §21 register row it exercises" — a row
label such as F7 or L24 or T26, not a requirement identifier. `[R-ERR-02]` ties
vectors to rows as well: "Every row of §21.2 through §21.5 … has at least one
conformance vector (§24) whose expected outcome is that row's outcome, and one
vector per instance." Nowhere does §24 oblige a manifest entry to carry an
`[R-...]` identifier.

**Permitted readings.** (a) A register row is itself a stable identifier and each
row's Governing rule cell names the requirement, so citing a row cites the
identifier transitively — the reading I take, and the one under which the front
matter's contrast ("rather than prose positions") is satisfied, since row labels
are certainly not prose positions. (b) The front matter describes an apparatus
the document did not build: `[R-VEC-02]`'s field list is the promise, and it does
not include the identifier.

**Cost of deciding.** Cheap to check, but arguing it requires deciding whether
"those identifiers" is meant strictly (the `[R-<PREFIX>-<NN>]` form §2.2 defines,
which is the antecedent in the very same sentence) or loosely (any stable label).
The strict reading is the natural one given the antecedent, and under it the
claim is not delivered.

**What an implementer does wrong without it.** A corpus consumer looking for the
requirement identifier in a manifest entry, on the front matter's assurance, will
not find one and must join through §21's Governing rule column. Minor, but it is
a claim about the document's own machinery in the paragraph that teaches a reader
how to use it.

**Byte-level?** No. Manifest schema again; nothing about a file's bytes or a
reader's verdict.

---

## Part 3 — Things I checked and found sound, recorded so the coverage is auditable

- Appendix A: hexdump, annotation table, CRC, offsets, and the four-step open
  narrative — all correct (§1.1 above), except the local-reader clause
  (diagrams-06).
- Appendix B against its sources: front block, trailer magic and size, 128-byte
  minimum, directory minimums, media type, 24-byte record header, 20-byte entry,
  2^16-entry segment, sentinel `FF ×16 00 ×4`, 0xEECB3BB2, CRC-32C parameters
  and check vector, value domain, 255-byte names, rank ≤ 255 and C ≤ 65,535,
  S range, A range and the 4096 recommendation, A_slab range, 65,536-byte
  discovery window, 1–16 MiB tile guidance, zstd magic, 0x7E000000, `tarn.`
  prefix, and all eight minimum guarantees. Every one matches its defining
  section.
- Appendix C against §7.3, §12.1/§12.2, §17.2, §17.3, §14.1, §11.4, §15.1/§7.4,
  §18.2, §6.3, §18.4. All match, including the six standardized keys.
- §21.9's eight-row table against Appendix B's one-line restatement and against
  §24's constructibility carve-out. Consistent.
- §21.6's fourteen non-violation rows against their cited rules; the two
  ex-rows now registered (`[R-MTA-05]` → F27/L48, `[R-CNT-22]` → F28/L49) and
  the two refused-but-conforming structural cases. Consistent, and §2.3's
  "§21.6's closing paragraph names the other two" resolves correctly.
- §15.3's ten rows against §21.4's T1/T6–T12 and §21.3's L18/L40–L42 and
  §21.2's F33; the "six rows … marked *structural*" count; the crc-failure row's
  special standing in `[R-LIF-08]`'s walk and `[R-SLB-03]`'s run continuity,
  which §9.7 and §16.2 restate identically in three places.
- §8.1's map against §4.5's exception list; §8.2's seven-link chain against
  §15.4 and §19.4.
- §20.3's three commit-shape figures and §5.1's three-commit box against
  `[R-WRT-04]`, `[R-WRT-05]`, `[R-WRT-07]` and §9.2's crash figure. Shape (c)'s
  careful carve-out ("changing a channel's fill value on a layer with no padding
  position and no pad bit") is exactly right against `[R-SER-05]`, and the
  §5.1 box's two hatched runs correspond correctly to commits 1 and 2.
- §20.5's compaction figure: fresh file_id, generation 1, index′ marks,
  reference-array equality. Consistent with `[R-WRT-06]`/`[R-WRT-07]`.
- §21.1's specialization list (F1 of F6 and F8, F35 of F36, L24 of L25) — I
  found further overlaps it does not name (T14 within T3 under codec 1; T11/T12
  within T9 whenever F ≤ 2^63 − 1), but §21.1 says "Some rows", and §24's
  "where a condition cannot be isolated … the entry records every row the file
  exercises and says which it was built for" disposes of the unlisted ones. Not
  a finding.
- Appendix H's verifier checklist against every verifier-detected row: F7, F25,
  F26, F27, F28, F33, F36, L18, L25, L40–L42, L46–L49, T2, T4, T5, T26. All
  present or covered by a cited section. (Its "padding samples" phrase does not
  name pad bits explicitly, but cites §14.5 which does; I judged that not a
  defect.)
- §10.1's four growth vehicles against `[R-ENC-07]`'s four — same four, same
  order.
- Appendix D's "Six choices" — six bolded items.
- §18.2's "Four restrictions" — four bullets, and bullet 4 restates §4.6's three
  name constraints correctly.
- §14.1's two-mode value sequence against §14.2's offset table and §17.3's
  stride rule (L divisible by s in all three cases: P·B/B, P·Q/Q, ⌈P/8⌉/1).
- The requirement-ID census: no gaps and no duplicates in any prefix's
  numbering, `R-SER-04` withdrawn as §14.4's note declares, `R-ENC-100`
  appearing only as §2.2's illustration.

## Part 4 — Where I had to guess

Three places, all recorded above as permitted readings: Appendix G item 2's hash
input (I chose "exclude the CRC field"); whether §20.4's file-scope sentence
narrows the table or merely summarises it (I chose summarises); and whether a
standardized user-metadata *key* counts as a "field this specification defines"
for §4.7's "In format major 1 `fill` is the only semantic field and
`version_minor` the only descriptive one". On that last one I concluded keys are
not fields — §4.7's note ties "field" to layout-table rows, and §18.2 contrasts
metadata content with "a structural field (§13.1)" — so I did not file it. Had I
concluded otherwise, `tarn.stats` would be a second descriptive field (it "MAY be
stale after any commit that changes the layer, and a reader MUST NOT use it to
skip reading data", which is exactly §4.7's descriptive-field contradiction
clause), and §4.7's uniqueness claim would fail. I flag the reasoning here so a
triager can overrule me cheaply.

I also checked §4.7's claim positively against every field that carries a class:
§6.1's two, §6.2's eleven, §7.2's five, §15.1's three, §18.2's one — all
structural but `version_minor`; and §7.4's classless payload fields, where the
declared alignment A survives as structural only because §4.7's structural test
says "a conforming reader **or verifier**" and §16.1 makes A verifier-checkable
("A verifier MUST check the invariant … readers are not obligated to — offsets
are always explicit, so alignment is reader-invisible"). That "or verifier" is
load-bearing and it holds.

**Total findings in this transcript: 10.**
