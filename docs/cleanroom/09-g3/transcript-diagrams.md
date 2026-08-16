# Round 9 — Diagram auditor — working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,892 lines). I opened no other file, ran no `git` command, listed no
directory beyond `wc -l` and `grep` against that one path, and consulted no
network resource. I wrote two scratch things: this transcript, and two
throwaway `python3 - <<EOF` heredocs run inline (they read no files — the
byte strings were typed from the document's own hex dumps). Everything else
below is derived from the document text.

Tooling actually run:

- `wc -l spec/tarn.md`
- `grep -n '^#\{2,5\} ' spec/tarn.md` (heading inventory)
- `grep -n 'Example\|Figure\|Note\.\|Rationale' spec/tarn.md` (figure inventory)
- `grep -n "R-ENC-13\|R-ENC-12" spec/tarn.md`, `grep -n "pad bit" spec/tarn.md`
- a Python script that re-parses the four §21 register tables straight out of
  the file and counts rows and semicolon-separated instances
- a Python CRC-32C implementation (bit-reflected, poly 0x82F63B78) used to
  re-derive `0xE3069283`, `0x00000000`, Appendix A's trailer CRC, and
  §15.4's all-sentinel-segment constant

## 1. Figure and worked-example inventory

Enumerated before judging anything, so coverage is checkable. Line numbers
are the first line of the block.

### Byte-layout / offset tables (normative)

| Line | Structure |
|---|---|
| 656 | §6.1 front signature block (2 rows: offset/size/value/class) |
| 699 | §6.2 trailer (11 rows: offset/size/type/field/class/valid values) |
| 863 | §7.2 record header (5 rows, 24 bytes) |
| 934 | §7.3 record types of format major 1 (2 rows) |
| 963 | §7.4 layer record inline payload (16 rows, field/type/constraint — no offset or class column, by §4.7's Note) |
| 1037 | §8.1 checksum coverage map (7 rows) |
| 1299 | §10.2 numeric identifier spaces (8 rows) |
| 1494 | §12.1 core sample types (13 rows) |
| 1724 | §14.2 decoded size and offset-of-value-k (2 rows) |
| 1892 | §15.1 tile-index entry (3 rows, 20 bytes) |
| 1940 | §15.3 entry-validity classification (11 rows) |
| 2326 | §18.2 user-metadata inline payload (1 row) |
| 2450 | §18.4 standardized keys (6 rows) |
| 2883 | §20.4 updater preservation by stored flags (3 rows) |
| 3040 | §21.2 file-scope register (38 rows) |
| 3086 | §21.3 layer-scope register (50 rows) |
| 3144 | §21.4 tile-scope register (27 rows) |
| 3186 | §21.5 ignored-record register (10 rows) |
| 3204 | §21.6 conditions that are not violations (14 rows) |
| 3291 | §21.9 minimum guarantees (8 rows) |
| 227 | §2.4 outcome classes (5 rows) |

### ASCII region diagrams

| Line | Figure |
|---|---|
| 560 | §5.1 a file after three commits |
| 1116 | §9.2 what a crash sees (3 rows) |
| 1887 | §15.1 tile-index region layout (blockquote box) |
| 2821, 2837, 2857 | §20.3 the three shapes a commit takes (a), (b), (c) |
| 2942 | §20.5 what compaction reclaims |
| 3594 | Appendix A hex dump (8 lines, 128 bytes) |

### Worked numeric examples

§4.6 (499, `température`), §5.1 (550, smallest file), §11.2 (1411, grid),
§11.4 (1465, ordinals), §12.1 (1528, bfloat16), §12.3 (1577, channel entry
bytes), §13.3 (1645, fill tuples), §14.2 (1766, interleaved/planar offsets),
§14.3 (1800, packed bool `55 01` / `55 FD`), §14.5 (1856, padded edge tile),
§15.4 (1980 and 1995, segments and disk ordinals), §16.2 (2092, slab runs),
§17.2 note (2187, sub-1-KiB frames), §17.3 (2273, byte-shuffle),
§20.3 (2807, one superseded tile).

### Checklists / summaries treated as figures

Appendix B (3641, constants), Appendix C (3668, registry snapshot),
Appendix G (3770, nine numbered profile items + a four-item closing promise),
Appendix H (3837, five class checklists), §10.1 (1279, the four growth
vehicles), §19.1 (2511, four open steps), §19.4 (2635, eight tile-read
steps), §20.3 (2759, six append steps), §9.2 (1082, six commit steps).

## 2. Arithmetic I actually did

### 2.1 CRC constants

```
crc32c(b"123456789") = 0xe3069283   §4.5 says 0xE3069283, stored 83 92 06 E3  OK
crc32c(b"")          = 0x00000000   §4.5, §7.1, Appendix A                    OK
crc32c(65536 x (FF*16 + 00*4)) = 0xeecb3bb2   §15.4 says 0xEECB3BB2           OK
```

### 2.2 Appendix A, byte by byte

I rebuilt the trailer from the field table rather than from the dump, then
compared:

```
8a 4e 52 41 54 0d 0a 1a  magic
01 00                    version_major = 1
00 00                    version_minor = 0
00 00 00 00              flags = 0
01 00 00 00 00 00 00 00  generation = 1
10 00 00 00 00 00 00 00  dir_offset = 16
04 00 00 00 00 00 00 00  dir_length = 4
80 00 00 00 00 00 00 00  committed_file_length = 128
ef cd ab 89 67 45 23 01  file_id = 0x0123456789ABCDEF
00 00 00 00              reserved
-> crc32c over these 60 bytes = 0xe00938d2, stored little-endian D2 38 09 E0
```

The dump's lines 0040–0070 reproduce exactly this, and the annotation table's
21 byte-range rows partition [0,128) with no gap and no overlap:
[0,8) [8,16) [16,20) [20,64) [64,72) [72,74) [74,76) [76,80) [80,88) [88,96)
[96,104) [104,112) [112,120) [120,124) [124,128). Verified against
`[R-CNT-06]`'s gates: dir_offset 16 ≥ 16; dir_length 4 ≥ 4; 16 + 4 = 20 ≤
128 − 64 = 64; generation 1 in [1, 2⁶³−1]; file_id ≠ 0; reserved zero; F mod
64 = 0. The prose that follows ("112 bytes covering [16, 128)") is right:
128 − 16 = 112. **Appendix A is clean.**

Note for §4.7 below: this is the *only* annotated file in the document and it
carries zero layers, so no layer record, tile-index region, or stored tile is
ever shown as bytes.

### 2.3 §14.2 example

tile extents (2,3) → P = 6. Channels a:uint8 (B=1), b:uint16 (B=2) → Q = 3,
decoded size P·Q = 18 ✓. In-tile coords (1,2) → ordinal 1·3+2 = 5 ✓; sample at
5·3 = 15, so [15,18) ✓; a at 15, b at 16–17 ✓. Planar b-plane = 6·2 = 12 bytes
✓; ordinal 5 at 5·2 = 10, so bytes 10–11 ✓. t:float32 + m:bool interleaved →
Q = 4+1 = 5, size 30 ✓; ordinal 5 at 25, [25,30), t 25–28, m 29 ✓. The
closing identity "channel c's value at in-tile ordinal u sits at byte
u·Q + Fᶜ — the table's forms with k = u·C + c" checks out: the table gives
(k div C)·Q + F_{k mod C}, and with k = u·C + c that is u·Q + Fᶜ ✓.

### 2.4 §14.3 example

P = 10, values alternating true,false from ordinal 0. Bit k of byte k div 8:
byte 0 bits 0–7 = 1,0,1,0,1,0,1,0 = 0b01010101 = 0x55 ✓. Byte 1 bits 0–1 =
1,0 = 0x01 ✓, six pad bits (2–7). Fill false → `55 01` ✓; fill true → pad bits
2–7 set → 0b11111101 = 0xFD → `55 FD` ✓. Decoded size ⌈10/8⌉ = 2 ✓ (which is
also the "2" §17.2's note cites).

### 2.5 §14.5 example

extents (5,5), tile extents (4,4) → G = (2,2) ✓. Tile (1,1) covers 4–7 on both
axes; real positions are those with both coords < 5, i.e. only (4,4) → 1 real,
15 padding ✓. One uint16 channel → decoded size 16·2 = 32 ✓. Fill 0xABCD →
little-endian `CD AB` ✓ at values 1–15 ✓.

### 2.6 §15.4 first example

entry_count = 1,000,000. Segments ⌈10⁶/65536⌉ = 16 ✓; 15 full = 983,040; final
covers 1,000,000 − 983,040 = 16,960 ✓. CRC array 16·4 = 64 ✓. Region
10⁶·20 + 64 = 20,000,064 ✓. k = 999,999 → segment 15 ✓, segment-relative
16,959, byte 20·16,959 = 339,180 ✓. CRC array at [20,000,000, 20,000,064) ✓.
Segment 15 at [983,040·20, 20,000,000) = [19,660,800, 20,000,000) ✓, length
339,200 ≈ "339 KB" ✓. One full segment = 65,536·20 = 1,310,720 = 1.25 MiB ✓.

### 2.7 §15.4 second example, §11.4 example, §16.2 example

(300,700) with T = (256,256): t = (1,2) ✓, s = 1·8 + 2 = 10 ✓, u = (44,188) ✓,
in-tile ordinal 44·256 + 188 = 11,452 ✓. Planar C = 4, c = 2: 2·32 + 10 = 74 ✓.
Entry 74 at region bytes [1,480, 1,500) ✓. Channel 3's ordinals 96–127 ✓ = 32
entries ✓. Slab example: S = 8 over block [0,32) → runs at 0,8,16,24 ✓; under
row-major with G = (4,8) a run of 8 consecutive ordinals is exactly one tile
row ✓; tile rows 1–2 = ordinals 8–23 = runs 1 and 2 ✓.

### 2.8 §17.3 byte-shuffle example

float32 1.0/2.0/3.0 → `00 00 80 3F | 00 00 00 40 | 00 00 40 40` ✓ (0x3F800000,
0x40000000, 0x40400000 little-endian). s = 4, n = 3. Filtered byte at
i·n + j:

```
i=0: 00 00 00
i=1: 00 00 00
i=2: 80 00 40
i=3: 3F 40 40
```

concatenated `00 00 00 00 00 00 80 00 40 3F 40 40` — exactly the example's
string, and the prose gloss ("the three first bytes, the three second bytes,
then 80 00 40, then 3F 40 40") matches ✓. Divisibility claim checked in all
three cases: interleaved L = P·Q with s = Q; planar numeric L = P·Bᶜ with
s = Bᶜ; packed bool s = 1 ✓.

### 2.9 §12.3 and §4.6 examples

`temp`/float32/NaN 0x7FC00000 → 04 | 74 65 6D 70 | 0C 00 | 04 | 00 00 C0 7F =
5 + 2 + 5 = 12 bytes ✓, and the field order matches §7.4's channel-entry row
(name, type u16, fill u8-len+bytes) ✓. `température` NFC = 12 bytes, the hex
given is exactly those 12 ✓; NFD variant 13 ✓.

### 2.10 §20.3, §21.9, §24 numbers

32-tile index region = 32·20 + ⌈32/65536⌉·4 = 640 + 4 = 644 ✓.
10⁶-tile layer ≈ 20 MB of index ✓.
entry_count 2³² → 2¹⁶ segments → 2¹⁶·4 = 256 KiB ✓; 2³⁶ → 2²⁰·4 = 4 MiB ✓;
2³²·20 = 85.9 GB, matching §24's "tens of gigabytes" ✓.
0x7E000000 = 2,113,929,216 ≈ 1.97 GiB, comfortably above §21.9's 256 MiB tile
guarantee ✓. LZ4 frame magic 0x184D2204 → bytes `04 22 4D 18` ✓ (T23).
zstd magic 0xFD2FB528 → `28 B5 2F FD` ✓.

### 2.11 Register row and instance counts, recomputed from the file

I re-parsed the four register tables with a script rather than counting by
eye. Rows: F 38, L 50, T 27, R 10 — matching each subsection's stated
"38 conditions", "50 conditions", "27 conditions", "10 conditions", total 125,
matching §21.8's "125 conditions". Instances under §21.1's stated rule
(semicolon-separated; a cell reading "—" is one): F 60, L 103, T 46, R 44,
total **253**, matching §21.8's "253 instances". So the document is
*arithmetically* self-consistent. Whether the cells are *correctly written* is
a different question, and §21.1 gives the test — see finding diagrams-02.

## 3. Completeness sweep of the register

§21.1 makes completeness normative, so I walked every requirement identifier
in the document and asked whether a detectable file-level witness exists and,
if so, which row carries it. Summary of the sweep (all confirmed present):

- §6.2's eleven trailer gates → F10–F19, F20, F21; the width/endian causes →
  F1, F5; the front block → F2, F8; minimum file size → F7.
- §7.2's framing → F26, F31; extent slot → F32, F33, F34; flags → F27, F28,
  F30; overlap → F35; multiplicity → F36; unknown/reserved types → F37, F38.
  Layer-side mirrors → L14, L15, L16, L17, L18, L19, L20, L25, L26, L27,
  L47, L48, L50.
- §7.4's whole constraint set → L21–L37, L40, L44, L45, L46 (I checked each
  of the 16 payload rows against a register row; all covered).
- §15.3's eleven classification rows map one-to-one onto T6–T12, T1, L19/F35,
  L41–L43 — no row of §15.3 is unregistered, and no T-row lacks a §15.3 row.
- §17.2's six `[R-COD-06]` frame constraints → T17–T22; §18.2's four document
  restrictions → R5–R10; `[R-MTA-09]`'s frame constraints → R4.
- §8.1's map: every checksum has a failure row (F16, F22, L38, L39, T1, R2);
  the two entries the map covers with *no* checksum (front block, unassigned
  extent) are exactly the two §4.5 exempts, and §22.3 states the consequence.
- Deliberate non-rows are each accounted for in text: sub-record nesting
  (§7.4's Note at 1015), stale slab declaration (§16.2's Note at 2069),
  post-commit residue (§9.5's Note at 1186), and the classes in §21.7.

I found no missing row. The `[R-WRT-*]` preservation obligations are not in
§21.7's second-paragraph enumeration, but they fall in the same class
(properties of a file's history, which §9.7 does not reconstruct) and §21.7
presents its account "by class" rather than as an exhaustive list, so I did
not treat that as a defect.

## 4. Findings

### diagrams-01 — Appendix G promises to close gap *content* and no item does

Appendix G's closing paragraph, line 3824:

> "Four things are not, and the items above are where the profile adds them:
> gap *content*, which `[R-CNT-03]` only advises; gap *extent*, which
> placement freedom (`[R-SLB-05]`) leaves open; sub-record order within a
> layer record's inline payload, which `[R-CNT-14]` leaves free; and the fill
> a writer records when its caller chooses none, which `[R-TYP-10]` states as
> a SHOULD."

Three of the four are delivered. Gap extent and sub-record order are item 3
("A total emission order, contiguously… Each structure begins where the
previous one ended… a layer record's sub-records are ordered by type, and
within a type by their order of creation"). Default fill is item 7 ("The
all-zero fill default"). **Gap content is delivered by no item.** I read
items 1–9 twice looking for it: item 3 mentions gaps only to concede the
problem ("save where a declared alignment forces a gap: order alone does not
fix bytes while the space between structures is free"), item 5 fixes whether
alignment is declared but not what the resulting gaps hold, and item 8 pins
`version_minor` and `flags` but nothing about slack.

This is not hypothetical for a profile whose whole subject is byte-identity.
`[R-LIF-02]` step 5 forces a pre-trailer pad whenever the directory does not
end 64-aligned, and §5.2 is explicit that its content is unconstrained
("Slack has no internal structure this specification defines, its content is
unconstrained, and no conformance requirement applies to it"), with
`[R-CNT-03]` only a SHOULD and §14.5's Note repeating "no conformance
requirement constrains its content". Two writers that both satisfy items 1–9
can therefore emit files differing in the pre-trailer pad, which is exactly
what the profile exists to prevent.

Reading chosen: the closing paragraph's promise is the error, not a missing
item's *content* being inferable — because there is nothing in the list to
infer from. An implementer building the profile has to guess, and the obvious
guess (zero the gaps, i.e. take `[R-CNT-03]` as a requirement the way item 7
takes `[R-TYP-10]`) is the one the document never states.

Byte-level: no. Appendix G is non-normative and says outright "It adds no
requirement to any actor: a writer ignoring it is fully conforming." Both
files a divergent profile-writer pair emits are conforming files, and no
reader's accept/reject verdict changes.

### diagrams-02 — L47, L48 and L50 do not apply §21.1's own instance arithmetic; §21.8's 253 is short by 4

§21.1, line 3016:

> "An instance names a field the condition ranges over, a container it can
> occur in, one of several alternatives the condition text states, or any
> combination of the three — a condition applying to two alternatives in two
> containers has four."

Compare the file-scope and layer-scope rows of the same condition:

F30 (line 3071): "A non-layer top-level record of a type §7.3 registers
carries a stored MU or PE bit differing from the value the registry fixes" —
Instances **`flags bit 0; flags bit 1`** = 2. One container, two alternatives.

L50 (line 3137): "A layer record, or a sub-record of a type §7.3 registers,
carries a stored MU or PE bit differing from the value the registry fixes" —
Instances **`layer record flags; sub-record flags`** = 2. Two containers, and
the same two alternatives — so by §21.1's sentence it should be **four**.

The same slip appears twice more in the same block:

- L47 (3134): "A layer record's or sub-record's flags carry MUST_UNDERSTAND =
  1 with PRESERVE_ON_EDIT = 0" — cell `—` = 1. §21.1 rightly treats the
  two-bit combination as a single predicate ("a combination of two flag bits
  — the fields it reads are not instances"), so there is one alternative, but
  there are still two containers → 2, not 1. Its file-scope twin F27 (3068)
  has one container and correctly reads `—`.
- L48 (3135): "Any of a layer record's or sub-record's reserved flag bits
  2-15 is set" — cell `flags bits 2-15` = 1. One range-alternative (correct
  per §21.1's T24 precedent) but two containers → 2. Its twin F28 (3069) has
  one container and correctly reads 1.

That the document *does* treat "layer record" and "sub-record" as two
containers is settled by the neighbouring rows, which do the cross product
explicitly: L16 "A layer record's or sub-record's extent slot has exactly one
of extent_offset and extent_length zero" enumerates all four (`layer record
extent_offset; layer record extent_length; sub-record extent_offset;
sub-record extent_length`), and L17 and L18 each enumerate the two
containers. So L47/L48/L50 are the outliers, not the convention.

Consequence: §21.8's "125 conditions over 253 instances" — a figure I
re-derived mechanically from the tables — should be 257, and `[R-ERR-02]`'s
"one vector per instance" plus `[R-VEC-03]`'s "every register row has at
least one vector for each instance it names" understate the corpus build list
by four files: a layer record with the MU bit wrong, a layer record with the
PE bit wrong (L50), a layer record carrying MU = 1 / PE = 0 (L47), and a
layer record with a reserved flag bit set (L48). Each is a distinguishable
file that no sub-record instance can stand in for.

I picked the reading that §21.1's sentence is the rule and the three cells are
wrong, rather than the reverse, because §21.1 states the arithmetic as a fact
("has four"), because F27/F28/F30 apply it correctly for the single-container
case, and because L16–L18 apply it correctly for the two-container case.

Byte-level: no. It changes what a corpus builds, not what any implementation
emits or what verdict it must reach — the governing rules `[R-CNT-12]` and
`[R-CNT-22]` are unchanged, and §21.1 already says "where a row and the rule
it cites diverge, the rule governs".

### diagrams-03 — Appendix H's verifier checklist drops the pad-bit obligation its own writer checklist names

Appendix H, verifier entry (3885):

> "alignment and slab invariants (§16); decoded-content obligations —
> padding samples and interleaved boolean bytes (§14.5, §14.2);"

Two items. But the structurally-constrained content is three things, and the
document says so twice. §21.7 (3260): "The obligations of §14.5 and
`[R-SER-08]` narrow this only where content is structurally constrained:
**padding positions, pad bits, and boolean bytes**." And Appendix H's own
writer entry (3858) names all three sides of it: "fill-encodes edge padding
**and pad bits** (`[R-SER-05]`, §14.5)".

Pad bits are not a sub-case of padding positions — §14.3's Note (1793) is
emphatic about this: "Pad bits are not padding positions (§11.3). A padding
position is a whole sample position outside the layer's extents, arising in
any layout; pad bits are a packed plane's final-byte unused high bits,
arising only when P is not a multiple of 8. A plane can have many padding
positions and no pad bits." So "padding samples" cannot be read as covering
them, and T5 — "In a packed planar bool plane with P mod 8 ≠ 0, a final-byte
pad bit … is not the channel's fill bit", detector *verifier* — is the one
verifier-detected row of §21.2–§21.5 that the checklist's list omits.

The verifier entry reads as exhaustive ("every reader obligation, plus the
checks readers are exempt from:" followed by a colon list), and I checked the
rest of it against every verifier-detected row: F9, F27/F28/L47/L48,
F29/L49, F30/L50, F35/L19, F38/L26, L41/L42/L43, T2, T4 and T26 (which the
register says is detected by T2's or T4's check) are all represented. T5 is
the sole gap.

Byte-level: no. `[R-SER-05]` is unambiguous ("Every pad bit (§14.3) MUST
carry the plane's channel's fill bit… a verifier MUST check it"), and
Appendix H is non-normative with the standing caveat "each entry's authority
is the requirement or section cited, never this summary."

### diagrams-04 — Appendix H's reader checklist states the acceptance duty wider than §2.3 does

Appendix H, reader entry (3849):

> "accepts every conforming file within §21.9's minimum guarantees and
> reports any resource refusal as a limit rather than as corruption
> (`[R-ERR-04]`)"

§2.3's actual duty (137) carries two further qualifiers:

> "A reader MUST accept every conforming file **of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1** … and none of whose values exceeds the minimum
> guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on
> that last ground; §21.6's closing paragraph names the other two)"

and §21.6's closing paragraph (3232) exists precisely to name those two:
"Two structural cases are **conforming files a reader nevertheless refuses**.
The first is **version_major naming a major this reader does not
implement**… The second is an **experimental-range record type carrying
MU = 1**".

As written, the checklist says a conforming reader must accept a conforming
major-7 file and a conforming file carrying an experimental MU = 1 record —
both of which `[R-CNT-07]` and `[R-CNT-15]` oblige it to reject. This is a
summary of a rule taken further than the section licenses, which is the same
defect class as a stale restatement even though the appendix disclaims its
own authority. It is worth fixing because §2.3 goes out of its way to
cross-reference "§21.6's closing paragraph names the other two", and the
checklist is where an implementer auditing their own work would look last.

Byte-level: no — §2.3 governs and is unambiguous.

### diagrams-05 — §4.7's Note promises a worked example for every non-obvious encoding; the layer record's inline payload has none

§4.7's Note (514) is the document's own presentation contract:

> "A packed variable-length payload — the layer record's inline payload
> (§7.4) — has no fixed offsets to give; its table omits the offset and class
> columns, and each field's class follows from the definitions above. **Every
> non-obvious encoding is followed by a worked numeric example**, and every
> sentinel or overloaded encoding additionally has a paired conformance
> vector. All named constants appear once in Appendix B."

The same sentence singles out the layer record's inline payload as the one
structure whose layout table cannot state offsets — i.e. the least obvious
encoding in the document, sixteen packed fields including two
variable-length-entry arrays whose element layouts are themselves packed —
and that encoding is the one with no worked numeric example anywhere. I
checked: §12.3's example (1577) gives a single *channel entry*'s twelve bytes
and nothing more; Appendix A's annotated file (3588) contains zero layers, so
no layer record, no dimension entry, no tile-index region and no stored tile
is ever exhibited as bytes; §15.4's examples give region *offsets* but no
entry bytes beyond the sentinel's `FF ×16 00 ×4`.

I verified the encoding is nonetheless determinate — §7.4's "fields are
packed in table order with no alignment or padding between them" plus the
per-field widths plus §12.3's channel-entry example fix it — so this is a
promise defect and a usability defect rather than an ambiguity. But it is the
one place where I would have most wanted a byte string to check my parser
against, and building a layer record was the only part of this walk where I
had to assemble the layout from prose alone.

Byte-level: no. The packing is determinate from §7.4 and `[R-ENC-06]`.

### diagrams-06 — §19.1 step 4 attributes byte comparison to `[R-ENC-12]`; `[R-ENC-13]` is the rule

§19.1 step 4 (2549):

> "Uniqueness is decided first, and over the raw name bytes whether or not
> each name is itself well-formed — `[R-ENC-12]` makes name comparison a byte
> comparison, which needs no valid name — so two layers whose name fields are
> byte-identical are a duplicate even when neither name is valid."

`[R-ENC-12]` (474) is the name-constraint rule (non-empty, at most 255 bytes,
free of U+0000–U+001F). The rule that makes comparison a byte comparison is
`[R-ENC-13]` (481): "Name comparison is raw bytes: two names are the same
name if and only if their encoded byte sequences are identical. Readers MUST
NOT normalize, case-fold, or otherwise transform names for comparison."

The register gets it right — F6's Governing-rule cell reads "`[R-ENC-15]`
(R-ENC-13)" — and the same step's earlier citation of `[R-ENC-12]` for
"parsed and checked per §4.6" is correct, so this is one wrong identifier in
one clause. It matters because the clause's whole argument is that comparison
needs no *valid* name, and `[R-ENC-12]` is exactly the rule about validity —
so citing it makes the sentence read as self-defeating to anyone chasing the
reference.

Byte-level: no. The outcome (duplicate byte-identical name fields are a
file-scope error even when neither name is valid) is stated in the same
sentence and registered as F6.

### diagrams-07 — §20.4's preservation table carries no requirement identifier, and its two remote citations point at different rules

The three-row table at §20.4 (2883) states MUST-level updater obligations
("Retain byte-identical. The updater MUST NOT modify the scope the record
governs."). It sits between `[R-WRT-05]` (which ends the preceding paragraph)
and `[R-WRT-08]` (which ends the following one), and carries no identifier of
its own. Under this document's convention — the identifier closes the
requirement it labels — the table would belong to `[R-WRT-08]`, whose own
sentence is about something else entirely ("An updater MUST NOT re-encode a
record whose type it does not implement, and MUST NOT modify one except by
relocating its extent").

The two places that cite the table cite it two different ways:

- §2.4 (233), by prose position: "**preserve-verbatim** | Binds updaters: the
  bytes are carried forward unmodified (relocated only as Part I permits).
  **§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows.**"
- §21.6 (3210), by the neighbouring identifier: "Ignored, and **preserved or
  dropped per its PE bit**; … | `[R-CNT-15]`, **`[R-WRT-08]`**"

Permitted readings: (i) the table is part of `[R-WRT-08]` — supported by
§21.6's citation but contradicted by `[R-WRT-08]`'s own subject matter;
(ii) it is part of `[R-WRT-05]` — supported by §2.4's "preserve-verbatim"
framing but not by the paragraph boundary; (iii) it carries no identifier at
all, which is what the bytes of the document actually show. I picked (iii),
because the document's identifier convention is positional and no identifier
appears between the two paragraphs.

That matters against §1's rubric ("Normative requirements carry stable
identifiers like `[R-IDX-03]`; test vectors and conformance checklists cite
identifiers, never prose positions") and §2.2 ("Normative requirements carry
identifiers of the form `[R-<PREFIX>-<NN>]`"). A vector or checklist covering
"an MU = 0 / PE = 1 record's extent content is carried forward unmodified"
has no identifier to name, and Appendix H's updater entry falls back to a
bare section reference ("respects unknown records' MU and PE bits (§20.4)").

A second, smaller half of the same problem: §2.4's cell says "§20.4's table
states the cases", but that table's preamble scopes it explicitly — "**For a
type the updater does not implement**, the stored flags are authoritative
(§7.3, `[R-CNT-15]`…), and carry these obligations:". Preserve-verbatim also
binds the *registered* types, which the paragraph before the table handles
instead ("both registered types carry PE = 1, so neither can be dropped, and
implementing a record's type confers understanding of it, not permission to
drop it"). So §2.4's pointer is narrower than the obligation it summarises.

Byte-level: no. `[R-WRT-05]` and the table's own text between them determine
the bytes an updater must carry forward; what is undetermined is only which
identifier names the obligation.

### diagrams-08 — Appendix B claims to collect every named constant and omits one of `[R-ERR-05]`'s hard limits

§4.7's Note: "All named constants appear once in Appendix B." Appendix B's
own header (3638): "Every named constant this specification fixes,
collected."

`[R-ERR-05]` (3329) enumerates the hard limits "stated where the structures
forcing them are defined": name ≤ 255 bytes; rank ≤ 255 and channel count ≤
65,535; codec 4's 0x7E000000; every offset/length/extent/count ≤ 2⁶³ − 1; A a
power of two in [512, 2⁶²] and A_slab a power of two in [1, 2⁶²]; S in
[1, 2⁶³ − 1]; "**a directory of at least 4 bytes at an offset of at least
16** (§6.2, `[R-CNT-06]`)"; and no file shorter than 128 bytes. Appendix B
carries seven of those eight — the directory minimums are the one that is
missing, even though the neighbouring "Smallest conforming file | 128 bytes"
row is derived from them.

Also absent, and comparable in kind to Appendix B's existing "Record header
size | 24 bytes" and "Index entry size | 20 bytes" rows: the 5-byte minimum
`extent_length` of a user-metadata record, a number the document pins in five
separate places (§7.1's `[R-CNT-25]`, F24, L12, §19.1 step 4, §19.3); and the
LZ4 frame magic `04 22 4D 18` that T23 uses as a detection constant, where
Appendix B does carry the zstd frame magic.

Byte-level: no. Every one of these is normative where it is defined, and
Appendix B says so ("Each is normative where it is defined; this table is a
finding aid").

## 5. Things I checked and cleared

Recorded so the coverage claim is falsifiable, not just asserted.

- **Appendix A** — every byte, every annotation row, the CRC, the region
  partition, and the two-request narrative. Clean.
- **Every ASCII region diagram** (§5.1, §9.2, §20.3 a/b/c, §20.5, §15.1). The
  §9.2 crash figure's three rows are consistent with `[R-LIF-05]` and §9.6;
  §20.3's three shapes match `[R-WRT-04]`/`[R-WRT-05]`; §20.5's figure matches
  `[R-WRT-06]`/`[R-WRT-07]` including the fresh file_id and generation 1. The
  §5.1 three-commit figure reconstructs consistently as commit 1 = front +
  layer A + dir₁, commit 2 = layer B + dir₂, commit 3 = dir₃ alone, matching
  its own captions. (Its phrase "the commit that added layer B here did
  exactly that" uses "re-emits" for a first emission; I judged that a
  wording looseness rather than a defect, since the bytes it describes are
  exactly §20.3 shape (a).)
- **Every worked numeric example** — arithmetic reproduced above in §2.
- **§8.1's coverage map against §4.5's classification** of terminal versus
  interior checksum fields: the seven map rows and §4.5's three lists agree
  exactly, and §8.2's seven-link chain matches the map's nesting.
- **§10.2's identifier-space table against every owning section** (§7.3,
  §14.1, §11.4, §12.2, §17.2, §17.3, §15.1, §18.2) and against Appendix C's
  snapshot: all eight rows' assigned/reserved/experimental partitions agree,
  including the two spaces with no experimental range.
- **§12.1's thirteen sample types** against Appendix C, §21.9's "all thirteen"
  in Appendix H, and the reserved pinnings in §12.2's Note (14/15 OFP8,
  16/17/18 int128/uint128/float128, 19 raw bytes) versus Appendix C's
  "19 opaque".
- **§15.3's eleven-row classification table** against its own preamble's "Six
  rows are marked *structural*" (six exactly), against §9.7's and §16.2's
  treatment of structural-ground entries versus crc-failing entries, and
  against T1 and T6–T12.
- **§21.9's eight-row limits table** against Appendix B's one-line restatement
  (all eight, same values), against §2.3's acceptance duty, against
  `[R-ERR-05]`'s hard limits, and against the sizing note (256 KiB at 2³²,
  4 MiB at 2³⁶ — both reproduced).
- **§21.6's fourteen non-violation rows** against their cited rules; the
  closing two paragraphs about the two conditions moved out of the table and
  the two conforming-but-refused cases are consistent with §2.3 and
  `[R-CNF-02]`.
- **§21.2–§21.5 row-by-row against §21.1's column contract**: every Detected
  cell names one of §19.2's four tiers or *certification*; every Detector is
  reader or verifier; the specialization claims (F2 of F8 and F10, F37 of
  F38, L25 of L26) hold.
- **§19.1's four open steps, §19.4's eight tile-read steps, §20.3's six append
  steps, §9.2's six commit steps** — checked for order, duplication and
  omission against §6.2's validation order, §6.4's accounting, `[R-LIF-02]`
  and §20.2. §19.4 steps 3–6 are correctly scoped "once per needed entry" and
  step 8's layer-scope-versus-tile-scope bounding matches §2.4's reject-layer
  row. No numbered list in the document is out of order, duplicated, or
  missing an item.
- **§21.1's instance-arithmetic rule applied to all 125 cells** — only the
  three of finding diagrams-02 disagree with it.
