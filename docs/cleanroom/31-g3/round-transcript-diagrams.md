# Cleanroom round 31 — Diagram auditor — working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,790 lines). I opened no ADR, no `docs/`, no `conformance/`, no `PLAN.md`, no
`registry.json`, no git history. I ran no web search or fetch. I did not list
the output directory.

The file was where the brief said it would be.

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file (`CLAUDE.md` pointing at `AGENTS.md`) and an
index of the maintainer's auto-memory naming several TARN-process notes by
title. I did not open any of the files it names, and I have disregarded its
contents; nothing in this transcript derives from it. Disclosing that it
appeared, per the brief.

**Files I wrote**, all in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/diagrams/`:

- `crc32c_diag.py` — my own CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF)
- `checks_diag.py` — the document's four stated CRC constants
- `appA_diag.py` — Appendix A's hex dump reconstructed and gate-checked
- `layerrec_diag.py` — §7.4's worked layer record reconstructed field by field
- `count_inst.py` — mechanical register row/instance count

and this transcript, at the single output path the brief names. I named my
files with a `_diag` suffix precisely because of the collision incident the
brief describes; nothing I ran read a file another agent could have written.

**Wrap discipline.** I did all phrase searching against a whitespace-normalised
copy of the document with `> ` blockquote markers stripped, and ran a
line-oriented grep beside each as a control. The hazard was real: a line-grep
for `fill bit in a packed plane` returns **0**, and for
`stored byte already holds the fill` returns **2**; the normalised search
returns **1** and **4**. One of my findings turns on exactly that pair, and a
line-grep would have hidden it.

---

## 1. Enumeration — every figure, table, dump, example and checklist

Before judging anything I enumerated the artefacts in my charter. Line numbers
are the first line of the artefact.

### Markdown tables (25 blocks, by line range)

| Lines | What it is |
|---|---|
| 127–147 | §2.2 requirement-prefix table (19 prefixes) |
| 301–307 | §2.4 outcome-class table (5 rows) |
| 769–772 | §6.1 front signature block layout (2 rows) |
| 812–823 | §6.2 **trailer byte-layout table** (10 field rows) |
| 980–986 | §7.2 record header layout (5 rows) |
| 1055–1058 | §7.3 record types of format major 1 (2 rows) |
| 1084–1101 | §7.4 layer-record inline payload layout (16 field rows) |
| 1202–1210 | §8.1 checksum coverage map (7 rows) |
| 1541–1550 | §10.2 numeric identifier spaces (8 rows) |
| 1762–1776 | §12.1 core sample types (13 rows) |
| 1994–1997 | §14.2 byte layout / decoded size (2 rows) |
| 2166–2170 | §15.1 tile-index entry layout (3 rows) |
| 2214–2226 | §15.3 entry-validity classification (11 rows) |
| 2613–2615 | §18.2 user-metadata inline payload (1 row) |
| 2810–2817 | §18.4 standardized keys (6 rows) |
| 3428–3432 | §20.4 updater preservation obligations (3 rows) |
| 3708–3744 | §21.2 file-scope register (35 rows) |
| 3757–3807 | §21.3 layer-scope register (49 rows) |
| 3817–3844 | §21.4 tile-scope register (26 rows) |
| 3867–3878 | §21.5 ignored-records register (10 rows) |
| 3887–3903 | §21.6 conditions that are not violations (15 rows) |
| 4013–4022 | §21.9 minimum-guarantee limits (8 rows) |
| 4396–4411 | Appendix A annotation table (14 rows) |
| 4431–4459 | Appendix B constants (28 rows) |
| 4529–4531 | Appendix E changelog (1 row) |

### ASCII / box figures and hex dumps

| Line | Figure |
|---|---|
| 656 | §5.1 Example — a file after three commits (box diagram) |
| 1150 | §7.4 Example — **annotated layer-record byte dump** (18 annotated rows) |
| 1304 | §9.2 Example — what a crash sees (three-row box diagram) |
| 2161 | §15.1 **unlabelled blockquote** — index-region layout box |
| 3357 | §20.3 Example (a) — a new layer |
| 3373 | §20.3 Example (b) — tiles added to an existing layer |
| 3399 | §20.3 Example (c) — a change confined to the directory |
| 3567 | §20.5 Example — what compaction reclaims |
| 4385 | Appendix A — **128-byte annotated hex dump** |

### Labelled Examples with arithmetic (checked byte by byte)

§4.6 (l.585 `température`), §5.1 (l.649 smallest file), §7.4 (l.1139 layer
record), §11.2 (l.1677 grid), §11.4 (l.1733 ordinals), §12.1 (l.1796 bfloat16),
§12.3 (l.1845 channel entry), §13.3 (l.1915 fill tuples), §14.2 (l.2038 byte
offsets), §14.3 (l.2072 packed bool), §14.5 (l.2130 padding), §15.4 (l.2254 and
l.2269 index regions), §16.2 (l.2371 slab runs), §17.3 (l.2556 shuffle), §20.3
(l.3343 supersede cost).

### Numbered lists

§9.2 commit steps 1–6; §10.1 four vehicles 1–4; §19.1 open steps 1–4; §19.4
tile-read steps 1–8; §20.3 appender steps 1–6; Appendix G items 1–10.
**All six are in order, none duplicated, none missing.**

### Checklists

Appendix H — five class checklists (file, reader, writer, updater, verifier),
lines 4718–4790. Appendix D — six design choices. Appendix F — nine normative
references plus one informative.

### The unlabelled blockquote

Exactly one blockquote in the document carries no *Note* / *Example* /
*Rationale* label, and is therefore **normative** under `[R-CNF-01]`: §15.1's
index-region box at lines 2161–2162:

> `[ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]`

I checked it against `[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`
and against §15.4's segment definition. It agrees exactly, including at
entry_count = 0 (0 + 0 = 0, matching the (0,0) extent slot `[R-CNT-23]` forces).
**No defect.** I record it because the brief warned that at least one such block
exists and that an earlier briefing in this project got the rule backwards.

---

## 2. Recomputed checksums — the standing charge

I wrote CRC-32C myself (table-driven, reflected polynomial 0x82F63B78 =
reflection of the document's 0x1EDC6F41, init 0xFFFFFFFF, final XOR
0xFFFFFFFF) and validated it against the document's own check vector before
using it for anything.

| Quantity | Document says | I computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | `0xE3069283` | `0xE3069283` | yes |
| CRC-32C(zero bytes) (§4.5) | `0x00000000` | `0x00000000` | yes |
| CRC of a full 2¹⁶-sentinel segment (§15.4, App. B) | `0xEECB3BB2` | `0xEECB3BB2` | yes |
| §7.4 example: CRC over 80 bytes of 4 sentinel entries | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, stored `55 49 a3 80` | yes |
| §7.4 example: crc_of_crc_array over that 4-byte array | `0xC4EE982E`, stored `2E 98 EE C4` | `0xC4EE982E` | yes |
| Appendix A trailer CRC over trailer[0,60) | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E` | yes |
| Appendix A directory CRC over 0 bytes | `0x00000000` | `0x00000000` | yes |

**Every stated checksum in this document reproduces.** I found no arithmetic,
offset, width or constant error anywhere in the document. That is a real
result, and I say below what I did that would have found one.

### Appendix A, byte by byte

I reconstructed the 128 bytes from the printed dump, cut each field out at the
offset and width §6.2's **layout table** gives (not at the offsets the
annotation table gives), decoded it, and compared against the annotation:

```
front magic [0,8)      89 54 41 52 4E 0D 0A 1A   matches §6.1 row 0
front reserved [8,16)  all zero                   matches §6.1 row 8
directory [16,20)      00 00 00 00                CRC-32C of 0 bytes
pre-trailer pad [20,64) 44 bytes, all zero
trailer+0  [64,72)     8A 4E 52 41 54 0D 0A 1A    magic
trailer+8  version_major = 1        trailer+10 version_minor = 0
trailer+12 flags = 0x00000000
trailer+16 dir_offset = 16          trailer+24 dir_length = 4
trailer+32 committed_file_length = 128
trailer+40 file_id = 0x0123456789ABCDEF
trailer+48 reserved 12 bytes, zero
trailer+60 CRC = 0x402F157E  (computed: 0x402F157E)
```

Every gate of `[R-CNT-06]` passes: F == physical length; F mod 64 == 0;
dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length (20) ≤ F − 64 (64);
file_id ≠ 0; reserved zero; incompat lane clear. The 128-byte floor of
`[R-CNT-27]` is met exactly. The annotation table's `[20,64) … 44 bytes` is
right (64 − 20 = 44), and the prose's "112 bytes covering [16, 128)" is right
(128 − 16 = 112). **The dump and its annotation table agree, and both agree
with §6.2's layout table.**

### §7.4's layer record, field by field

This is the document's only other annotated dump and the one with real
arithmetic in it. I asserted, for every printed offset, that it equals the
running length of everything printed before it — this catches a stale offset
column, which is the classic failure here. All eighteen matched. I then
re-parsed the 81 bytes independently, in the field order §7.4's **payload
layout table** gives:

```
name="sst"  layout=1  linearization=1  codec=1  filter=1
A=0  S=0  A_slab=0  d=1  C=1
dim  ("x", extent 100, tile extent 32)
chan ("temp", type 12, fill 00 00 C0 7F)
index_encoding=1  entry_count=4  crc_of_crc_array=0xC4EE982E
consumed 81 of 81 bytes, residue 0  -> sub-record sequence empty, as claimed
```

Derived and cross-checked:

- grid count ⌈100/32⌉ = **4** = declared entry_count (§11.2, `[R-CNT-17]`)
- entry array 4 × 20 = **80 bytes**; segment CRC array ⌈4/2¹⁶⌉ × 4 = **4 bytes**
- `[R-CNT-17]` extent_length = 4·20 + 1·4 = **84** — the document says 84
- fill length 4 == float32 element size 4 (`[R-CNT-23]`); fill decodes
  little-endian to **0x7FC00000**, the quiet NaN claimed
- channel entry bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F` are byte-identical
  to §12.3's example, as the text claims ("byte for byte")
- the summary "4 + 34 bytes, the dimension entry 18, the channel entry 12, and
  the trailing fixed fields 13 — 81 exactly": 1+2+2+2+8+8+8+1+2 = **34**;
  1+1+8+8 = **18**; 1+4+2+1+4 = **12**; 1+8+4 = **13**; 4+34+18+12+13 = **81**
- the segment is *partial* (4 entries, not 2¹⁶), so `[R-IDX-05]` requires its
  CRC to be computed rather than taken from the all-sentinel constant — and the
  document computes it correctly (0x80A34955 ≠ 0xEECB3BB2)
- decoded tile size P·Q = 32·4 = 128 bytes, well inside every §21.9 row

**No defect.** This example is exact in every particular.

### Every other worked example, recomputed

- §4.6 `température`: NFC 12 bytes (`74 65 6D 70 C3 A9 72 61 74 75 72 65` — I
  counted 12), NFD 13. Correct.
- §11.2: G=(4,8), N=32, P=65,536; ⌈1000/256⌉=4. Correct.
- §11.4: s(1,0)=8; (300,700) → tile (1,2), s=10; in-tile (44,188) → 44·256+188
  = **11,452**; planar c=2 → 2·32+10 = **74**. Correct.
- §12.1 bfloat16: 1.0 = 0x3F80 stored `80 3F`; 0x7FC0 quiet NaN. Correct.
- §14.2: Q=3, size 18, ordinal 5 at [15,18) with `a` at 15 and `b` at 16–17;
  planar `b` 12 bytes, ordinal 5 at 10–11; t/m Q=5, size 30, ordinal 5 at
  [25,30) with t at 25–28 and m at 29. All recomputed from the table's own
  formulas `(k div C)·Q + F_{k mod C}` and `k·Bᶜ`. Correct. I also verified the
  closing identity `u·Q + Fᶜ` = the table's form at `k = u·C + c`. Correct.
- §14.3: P=10, byte 0 = **0x55**, byte 1 = **0x01**, six pad bits; with fill
  true `55 FD`. I built the packing LSB-first and got exactly `55 01` and
  `55 FD`. Correct.
- §14.4 Note: at P=1 the planar and interleaved images coincide **exactly when
  the fill is false** — I checked all four combinations; correct, and the
  general claim that ⌈P/8⌉ = P only at P = 1 holds for P ≥ 1.
- §14.5: grid 2×2, tile (1,1) covers 4–7 on both axes, exactly one real
  position (4,4) at in-tile ordinal 0 and **15** padding positions; P=16, B=2,
  decoded size **32**; fill 0xABCD stored `CD AB`. Correct.
- §15.4 first example: 1,000,000 entries → ⌈10⁶/65536⌉ = **16** segments, 15
  full, last covering 1,000,000 − 15·65,536 = **16,960**; CRC array 64 bytes;
  region 20,000,064; k=999,999 is entry 16,959 of segment 15 at relative byte
  **339,180**; array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000) = **339,200 bytes ≈ 339 KB**; one full segment =
  65,536·20 = 1,310,720 = **1.25 MiB**. Every figure correct.
- §15.4 second example: disk ordinal 74 → region bytes [1,480, 1,500)
  (74·20 = 1480); channel 3's block is [96,128), i.e. entries 96–127, **32**
  copies of the sentinel. Correct.
- §16.2 example: S=8 over [0,32) gives runs [0,8),[8,16),[16,24),[24,32).
  Correct.
- §17.3 shuffle: I applied `byte i of group j → offset i·n + j` with s=4, n=3 to
  `00 00 80 3F 00 00 00 40 00 00 40 40` and got exactly
  `00 00 00 00 00 00 80 00 40 3F 40 40`, the document's value; the stated
  inverse restores the original. Correct.
- §20.3 example: 32·20 + 4 = **644**. Correct. §20.3 Note: 10⁶ · 20 = 20 MB.
  Correct.
- §21.9 Note: at entry_count = 2³² the segment-CRC array is 2¹⁶ · 4 = 2¹⁸ =
  **256 KiB**, and at 2³⁶ it is 2²⁰ · 4 = 2²² = **4 MiB**. Both correct.
  65,536 layers × 200-byte records = 13,107,200 = **12.5 MiB** exactly, which
  is the "small layer records that figure assumed". Correct.
- §24 `[R-VEC-03]`'s "tens of gigabytes" for the entry_count guarantee's index
  region: 2³² · 20 = 85,899,345,920 bytes = **80 GiB**. Correct.

---

## 3. Mechanical checks over the register (§21)

### Row and instance counts

§21.8 claims "120 conditions over 277 instances". I extracted every register row
mechanically and applied §21.1's own counting rule ("Instances within a cell are
separated by semicolons, and a cell reading — is one instance"):

```
rows: 120   total instances: 277
```

Exactly the stated figures. Per subsection: §21.2 = 35 (F1–F36 with F11 struck,
and the struck label is documented in the Note at l.3746), §21.3 = 49 (L1–L49),
§21.4 = 26 (T1–T26), §21.5 = 10 (R1–R10). 35+49+26+10 = 120. Every subsection
header's count is right.

I then spot-checked the instance cells against §21.1's three enumeration axes:

- *layout formulas are materially different shapes*: L44, T21 (3 each — no
  direction split, since "exceeds"/"larger than" bounds one way); T3, T14, T22
  (6 each — three layouts × two directions, since "not exactly"/"differs
  from"/"does not equal" are two-way). All consistent.
- *magnitude direction*: L21 (2 layouts × 2 directions = 4), L30 (2), F17 (2),
  L22 (2 directions + 2 stated alternatives = 4). All consistent.
- *no direction for a checksum or a constant comparison*: F14, F20, L37, L38,
  T1 all read `—` = 1. Consistent.
- *no direction for a nonzero test*: L20 (`A ≠ 0` and `S ≠ 0`) reads `—` = 1;
  L27, L28 likewise. Consistent with the rule's own worked examples.
- R4's 16: six alternatives × two containers, plus the content-size field's two
  directions × two containers = 12 + 4 = 16. Consistent, and it correctly omits
  the `Window_Size` constraint, which §18.2 expressly does *not* carry over.

### Detector / detection-point consistency

I checked every row's Detector against its Detected cell: every `verifier` row
is at `certification` and no `reader` row is; every reader tier is one of
§19.2's four (`open`, `layer access`, `tile use`, `extent use`). **0
mismatches** across 120 rows.

### Governing-rule attribution

Grouping rows by the first identifier in the Governing rule cell:

`[R-CNT-06]` governs exactly **nine** rows — F8, F9, F10, F12, F13, F14, F15,
F16, F17. §2.3 asserts "`[R-CNT-06]` states nine". I also derived the nine
conditions from `[R-CNT-06]`'s own text (magic; CRC; length == size; length
multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; sum ≤ F−64; file_id ≠ 0;
reserved zero — the version gate and flag gates belonging to `[R-CNT-07]` and
`[R-CNT-08]`, which carry F18 and F19). **Nine both ways.** And §2.3's split
"the trailer magic and the trailer CRC assert invariants `[R-CNT-24]` fixes and
the other seven do not" — 2 + 7 = 9 — is right.

### §21.2's reach derivation

§21.2 claims that deriving `[R-CNF-13]` row by row "yields F8, F14, F6 and both
of F1's instances … and no other row". I derived it independently from
`[R-CNT-24]`'s four permanent invariants (magic at F−64; version fields at
F−56; CRC at F−4 over [F−64, F−4); constant front block): F8 asserts the first,
F14 the third, F6 the fourth, F1's two instances the fourth and the first. F5
does not reach (its floor derives from major 1's dir minimums); F15 does not
(its bytes sit inside the redefinable 48); F13, F17, F19 read fields inside the
redefinable 48. F18 is outside the premise. **The derivation matches exactly.**

### §15.3's "Six rows are marked *structural*"

I counted §15.3's table: 11 data rows, of which rows 2–7 carry *structural* —
**six**, as claimed. Those six map onto seven register rows (T6, T7, T10, T8,
T11, and T9+T12 from the single "overflows, or > F − 64" row), and
`[R-IDX-03]` governs exactly those seven. Consistent.

### §20.5's row inventory

"F36 and L25 for a record type, and one row for each of the other seven spaces
§10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates 8 spaces;
8 − 1 = 7; the seven cited rows map one-to-one onto index encoding,
linearization, sample type, channel layout, codec, filter and metadata
encoding. **Correct and complete.**

### Prefix table

Every prefix in §2.2's table is used in the document and every prefix used is in
the table (19 both ways). Within each prefix the identifier numbers are gapless
(`ENC` reaching 100 only because §2.2 uses `[R-ENC-100]` as its own worked
example of extension; `SER` gapless because the withdrawn `[R-SER-04]` is still
present in §14.4's Note as a withdrawal record, exactly as §2.2 requires).

---

## 4. Table-against-prose checks

### §8.1's coverage map vs §4.5's prose

§4.5 asserts every field of every structure is covered by exactly one checksum,
with four named exemptions and three named interior checksum fields. I walked
the map: front block (exempt, equality); trailer[0,60) by trailer CRC, [60,64)
terminal; directory's record sequence by the directory CRC — which is what
covers each layer record's `crc_of_crc_array`, the first interior field; index
entries by their segment CRC — which covers each entry's `crc` field, the
second; the segment CRC array by `crc_of_crc_array` — the third; stored tiles by
their entry crc; user-metadata extents by their terminal CRC; unassigned-type
extents by nothing. Every assigned record type's extent is covered (0x0001's
extent is the index region, 0x0002's is the metadata extent). **Complete and
consistent; no gap and no double coverage.**

§8.2's chain — trailer → directory → crc_of_crc_array → segment CRC array →
index segment → index entry → stored tile — and its outcome list (reject-file /
reject-layer / reject-tile / ignore-record) agree with L37, L38, T1 and R2.

### §10.2's identifier spaces vs the defining sections

All eight rows check out against §7.3, §14.1, §11.4, §12.2, §17.2, §17.3,
§7.4/§15.1 and §18.2 — including the two-part reserved range for linearization
(§11.4 says "2 and 3 … without semantics" plus "4 through 0x7FFF", which the
table correctly folds to 2–0x7FFF) and sample type (14–19 plus 20–0x7FFF folded
to 14–0x7FFF). "Value 0 is invalid in every space above" holds for all eight.

### Appendix B (constants) and Appendix C (registry snapshot)

I checked all 28 Appendix B rows against their defining sections. Every value
matches, including the two I recomputed (the all-sentinel segment CRC and the
CRC check vector). Appendix C matches §7.3, §12.1, §12.2's Note, §17.2, §17.3,
§14.1, §11.4, §15.1, §18.2, §6.3 and §18.4 exactly — 6 standardized keys, 13
sample types, 6 pinned reservations, 4 codecs, 2 filters, 2 layouts, 1
linearization, 1 index encoding, 2 metadata encodings.

### Appendix D, E, F

Appendix D says "Six choices" and gives six. Appendix E has one row. Appendix
F's nine normative references each cite a section that does use them; RFC 1950
and RFC 1952 are cited only negatively in §17.2 and T15, and §21.4 states that
T15's detection is T24's or T25's, so no reader needs them — correctly omitted.

### Appendix G

Items numbered 1–10, in order, none missing. I verified item 5's claim that the
byte-shuffle filter is the identity "exactly where the stride is 1 … and equally
where … n = L/s being 1": solving `i·n + j = j·s + i` for all i, j gives
`i(n−1) = j(s−1)`, which holds universally iff n = 1 or s = 1. **The claim is
exactly right and exactly exhaustive.** Item 2's hash input (bytes [0, F−64)
followed by trailer[0,60) with file_id zeroed) is well formed: file_id is at
trailer offset 40 with width 8, inside [0,60). Item 3's "the first structure
begins at 16 … or, where a declared alignment admits no structure at 16, at the
least position above it the declaration admits" is right, since A ≥ 512 > 16.
The closing paragraph disclaims exhaustiveness in terms ("Read the numbered
items as the list; this paragraph names what they are for, not how many there
are"), so I did not treat its omissions as defects.

### Appendix H checklists

I checked each of the five against the requirements cited. The reader checklist's
"all four codecs, both filters, both layouts, all thirteen sample types, and
both user-metadata encodings" is right on every count (§17.2 makes 1–4 core;
§17.3 makes 1–2 core; §14.1 assigns 2; §12.1 defines 13, all core; §18.2 makes
both assigned encodings core). The verifier checklist's ten items each trace to
a stated verifier obligation, and its "F1, F6", "F7", "F36, L25" and "R1"
citations are right. Findings against the writer and updater entries are below.

---

## 5. Findings

I open with the one that took real work to reach, and grade each honestly.

---

### diagrams-01 — AMBIGUITY

**The §14 bar's carve-out is stated in *bytes* in three normative places and
restated the same way twice more, but a padding position in a packed planar bool
plane occupies a *bit*, and `[R-SER-05]` fixes "the fill bit in a packed plane"
there.**

Location: §20.3 step 4 (`[R-WRT-04]`), three sentences; §11.1's Rationale;
§23.1 (`[R-PRV-01]`). The governing content rule is §14.5 (`[R-SER-05]`) and
§14.3 (`[R-SER-03]`).

The §14 bar's own list is explicitly bit-aware:

> "the set of padding positions (§11.3), the pad bits `[R-SER-03]` gives a
> packed planar bool plane, and the content `[R-SER-05]` fixes at both"

and `[R-SER-05]` spells the packed case out:

> "at every padding position, a writer MUST encode, for each channel the
> position carries, that channel's fill value — the recorded fill bytes for a
> numeric channel, the recorded fill byte for an interleaved bool channel, the
> fill bit in a packed plane."

The carve-out that decides whether a commit is barred, however, is stated only
over bytes. §20.3, the §14 bar itself:

> "a change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`), or a new padding position whose stored byte already holds the
> fill `[R-SER-05]` fixes — is not what this bars."

§20.3 again, in the shrink paragraph, which is the operative one:

> "What counts as such an alteration is the §14 bar and nothing else, its
> carve-out included — a new padding position whose stored byte already holds
> the fill `[R-SER-05]` fixes is not one, so a shrink producing only those is
> permitted here exactly as it is there"

§20.3 a third time, denying the carve-out to a growth:

> "The bar's carve-out does not reach a growth: it covers a position whose
> stored byte already holds the fill it keeps"

§11.1's Rationale: "a new padding position whose stored byte already holds the
fill alters nothing." §23.1: "§20.3 step 4 permits that shrink only where those
bytes already hold the channel's recorded fill, which the layer record
publishes."

**The degenerate witness.** Take a planar layer, one bool channel, d = 1,
T₀ = 16, E₀ = 16. Then P = 16, G₀ = ⌈16/16⌉ = 1, N = 1, entry_count = C·N = 1,
decoded size = ⌈16/8⌉ = 2 bytes, P mod 8 = 0 so there are no pad bits, and
E mod T = 0 so there are no padding positions. The single tile is stored, and
its bit 15 (byte 1, bit 7) happens to hold the channel's fill bit.

A commit shrinks E₀ to 15. Grid count still ⌈15/16⌉ = 1, so N = 1 and
entry_count = 1 — unchanged, so `[R-CNT-17]`'s extent_length is unchanged and
the index region need not be re-emitted at all. Decoded size still 2 bytes.
Still no pad bits. What changes is that in-tile ordinal 15 is now a *padding*
position, so `[R-SER-05]` now requires its bit to be the fill bit — and it
already is. **No stored byte in the file needs to change**, and the resulting
file is conforming.

**The two readings.**

*(R1, bit-wise.)* "Stored byte" is shorthand for the stored representation at
that position — the fill bytes for a numeric channel, the fill byte for an
interleaved bool, the fill bit in a packed plane, exactly as `[R-SER-05]`
enumerates. The carve-out reaches the packed plane, the shrink alters nothing,
and this is a directory-only commit.

*(R2, literally byte-wise.)* A padding position in a packed plane has no stored
byte of its own — its byte carries eight positions — so the carve-out states no
condition the packed case can satisfy (or satisfies it only if all eight bits
are the fill bit). The shrink alters "the set of padding positions", the first
item in the §14 bar's list, and is therefore **barred**: the operation is a new
layer or a whole-file rewrite under a fresh file_id.

**I pick R1**, and the reason is a governing clause two sentences above the
carve-out rather than the carve-out's own wording: "The test is the effect on
such a tile, and the list names where that effect arises rather than standing on
its own", followed by the general condition "a change that leaves every one of
those tiles' stored bytes meaning exactly what they meant". My witness satisfies
that general condition in the same sense the numeric carve-out does — the byte
is untouched and every bit still decodes the same way; only position 15's
sample/padding *status* changes, which is equally true of the numeric case the
document expressly permits. The two clauses after the em-dashes are
illustrations of the general test, and §20.3 says so in terms.

**What an implementer does wrong without it.** An updater built on R2 refuses a
commit that R1 lets it make, and tells its caller to rewrite the whole file
instead — for a change that touches one record in the directory and not one
stored byte. Conversely an updater built on R1 emits an append that an R2
verifier of the *writer's conduct* would call a violated obligation. The
disputed file is conforming under both readings, so nothing here changes what a
reader must accept or reject.

**Byte-level: no.** Not because the consequence is small — under R2 the byte
sequence "prior file + this commit" is one no conforming updater may emit, which
is the shape that *would* move the emittable set — but because the general
clause above the carve-out settles the reading, and R2 requires taking an
illustration as the rule against an express instruction not to. I flag it
anyway, at AMBIGUITY, because the byte-shaped wording is repeated five times
including in the sentence that is stated to be "the whole of the test" for a
shrink, because a packed planar bool plane is not an exotic case, and because a
triage judge who finds R2 defensible on the shrink paragraph alone should treat
this as byte-level. The cheapest repair is to say "stored representation" — or
to name the three cases as `[R-SER-05]` already does — in the three normative
occurrences.

---

### diagrams-02 — OBSERVATION

**§6.2's trailer layout table gives no value constraint for `flags`, alone among
its ten rows, although a conforming file under this text must carry bits 0–15
clear.**

Location: §6.2, the trailer byte-layout table (line 817).

> `| 12 | 4 | u32 | flags | structural | bits 0–15 incompat lane; bits 16–31 ignore lane (§6.3) |`

Every other row of that table states the field's admissible values in the *Valid
values* column: the magic gives its eight bytes; version_major "1 (0 invalid;
others: §6.3)"; version_minor "any (see §6.3)"; dir_offset "≥ 16"; dir_length
"≥ 4; dir_offset + dir_length ≤ F − 64"; committed_file_length "= F; multiple of
64"; file_id "≠ 0"; reserved "zero"; trailer CRC its covered range. The flags
cell alone gives a *structural decomposition* instead of a value set, and so
states neither of the two constraints that actually bind: §6.3's

> "a writer creating a file under this text MUST write flags = 0"

and F19's registration of a set incompat bit as a **reject-file** violation
("Any bit of the flags incompat lane (bits 0-15) is set; this text defines no
flag bits, so every such bit is unimplemented"). A reader consulting the layout
table for what values `flags` may hold learns only that there are two lanes.

Note that this is not a contradiction — the cell is silent, not wrong, and it
does point at §6.3 as version_major's cell does. But version_major's cell states
its value *and* points; this one only points, in a column whose other nine cells
are self-contained.

**Byte-level: no.** `[R-CNT-06]`'s ordered validation names "the flag gates
(§6.3)" explicitly, and §19.1 step 2 cites `[R-CNT-08]`, so a reader following
the reader algorithm reaches the right check. The omission costs a reader that
builds its trailer validator from the layout table alone, which is a real way to
build one.

---

### diagrams-03 — AMBIGUITY

**§21.6's zero-layers entry restates `[R-CNT-14]` narrower than the rule is: it
gives "an empty directory" as the defined behavior of a file with no layers,
although a conforming file with no layer records may carry other records and so
a non-empty directory.**

Location: §21.6's table, row 4.

> `| The file contains zero layers | A conforming file with an empty directory | [R-CNT-14] (R-CNT-02) |`

The governing rule is broader:

> "multiplicity rules are per type — in format major 1: any number of layer
> records (zero is valid: an empty directory is a conforming generation); at
> most one file-scope user-metadata record …"

The rule makes two separate statements — that zero layer records is valid, and
that an empty directory is a conforming generation — and the §21.6 cell fuses
them into one, so that the *behavior* attached to "zero layers" is "an empty
directory". A file carrying no layer record and one top-level user-metadata
record is conforming under `[R-CNT-14]` (nothing requires a layer record, and
one metadata record is permitted), and its directory is not empty. The same
goes for a file whose only record is an experimental-range MU = 0 ancillary,
which §21.6's own row 5 makes conforming.

Permitted readings: (a) the cell states the paradigm case and "conforming" is
the whole of the behavior — which is what §5.1's and Appendix A's examples
illustrate; (b) the cell states a conjunction, so zero layers is a defined
non-violation only where the directory is otherwise empty. **I pick (a)**,
because §21.1 says in terms that "§21.6's entries restate their governing rules
on the same terms a row does, and where such an entry and the rule it cites
diverge, the rule governs there too."

**Byte-level: no** — and this is precisely the pattern the brief names as the
dominant cause of over-claiming: §21.1 has already decided which of the two
governs, so only the table is loose. A verifier built from §21.6's cell would
wrongly report nonconforming on a conforming file, which is why it is worth
saying, but the document does not leave the verdict open.

---

### diagrams-04 — OBSERVATION

**§13's "Note — sparse writing" states the index re-emission trigger as
"changes a layer's stored-tile set, or … grows its extents so that entry_count
changes", omitting the shrink and the planar-channel-removal cases that
`[R-WRT-04]`'s "stored-tile set **or index content**" covers.**

Location: §13.3's closing Note (line 1941).

> "Declare-then-fill workflows append tiles as data arrives, generation by
> generation (§9); each commit that changes a layer's stored-tile set, or that
> grows its extents so that entry_count changes, re-emits that layer's whole
> tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

The normative rule, §20.3 step 4, is keyed differently:

> "Every layer whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full"

and §5.1's own figure text uses the same broader key ("A commit that changes a
layer's stored-tile set or index content re-emits that layer's whole tile-index
region as well"). Two commits fall inside the rule and outside the Note's
enumeration, and both are commits §20.3 expressly permits:

1. A shrink that drops only *sentinel* tiles out of the addressed set. The
   stored-tile set is unchanged; entry_count falls; `[R-CNT-17]` forces a new
   extent_length and so a re-emitted region. §20.3: "`[R-CNT-17]` obliges the
   smaller entry_count and so a re-emitted index region".
2. Removal of a planar channel none of whose tiles the superseded generation
   stored — which §20.3 expressly permits ("a commit that moves only the
   ordinals of channels the superseded generation stored no tile for alters
   nothing this bars") and which drops entry_count from C·N to (C−1)·N.

Case 2 is the mechanism §20.3 and §11.1 now name alongside a falling grid count
as the two ways a tile leaves the addressed set; the Note names neither.

**Byte-level: no.** The Note is labelled and therefore non-normative under
`[R-CNF-01]`, and `[R-WRT-04]` and `[R-CNT-17]` between them settle the
obligation without appeal to it. In fairness the Note's subject is
declare-then-fill, where growth is the natural direction; the fix is one word
("or that changes entry_count") rather than a rewrite.

---

### diagrams-05 — OBSERVATION

**§20.3's "the three shapes a commit takes" Example has no shape for a commit
whose only effect is dropping a PE = 0 record that owns an extent — a commit
§20.4 now licenses in terms.**

Location: §20.3's Example (line 3352), shapes (a), (b) and (c); §20.4's
preservation table, the MU = 0 / PE = 0 row.

§20.4:

> "Retain byte-identical, or drop it — its extent becoming slack. The licence is
> the bit's own: the writer that stored PE = 0 declined preservation across
> edits, so an updater MAY drop the record in any commit it is otherwise free to
> make — one whose only effect is the drop included"

The Example's taxonomy is closed by its own title and by shape (c)'s exclusion
test. Shape (c) is headed "A change confined to the directory" and enumerates
"clearing a slab declaration, renaming a layer, or changing a channel's fill
value where …", then rules a case out precisely because an extent is involved:

> "Editing user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack, as
> in (b)."

A drop-only commit of an extent-owning PE = 0 record re-emits only the directory,
the pad and the trailer — so it is not (b), which appends payloads — and it turns
an extent into slack, which is the very feature (c) uses to send user-metadata
editing away to (b). Its diagram would be (c)'s two boxes plus a hatched run
where the dropped extent was. Such a record is constructible in a conforming
file: §7.3 registers only PE = 1 types, so a PE = 0 record is of an unassigned
type, and §21.6's row 5 makes an experimental-range MU = 0 record conforming.

**Byte-level: no.** The Example is labelled and non-normative; §20.4 and
`[R-CNT-21]` state the outcome without it. It is reportable because a figure a
reader could take as the complete taxonomy of commit shapes no longer is one,
and because the gap sits exactly where the drop licence was widened.

---

### diagrams-06 — OBSERVATION

**Appendix H's conforming-writer and conforming-updater checklists carry no
trailer-flags obligation, although §6.3 places a MUST on a creator and three on
an updater — and the updater's three are precisely the obligations no verifier
can check from the bytes.**

Location: Appendix H, the "Conforming writer" and "Conforming updater" entries
(lines 4745 and 4755). The obligations are §6.3, `[R-CNT-08]`:

> "a writer creating a file under this text MUST write flags = 0 … An updater
> MUST copy forward unknown ignore-lane bits of the file it modifies, MUST NOT
> clear them, and MUST NOT set any other"

The writer entry lists seven writer MUSTs of comparable weight — records fill,
fill-encodes edge padding and pad bits, emits interleaved boolean values as only
0x00 or 0x01, sorts user-metadata members, follows the commit protocol including
both barriers, honors any alignment or slab it declares — and separates out the
one advisory it mentions ("Advisory, and not a conformance condition: a writer
SHOULD zero the gaps it creates"). It does not mention flags. The updater entry
lists five obligations and inherits "everything a writer does for the bytes it
produces"; it does not mention flags either, and the creator's flags = 0 rule
would be the wrong inheritance in any case, since §6.3 exempts an updater and a
compactor from it.

The gap matters more here than a missing checklist line usually would, for the
reason §2.3 gives: `[R-CNF-02]` declares this one expressly *not* to be a
file-conformance violation —

> "§6.3's flags rules against a set ignore-lane bit — a creator's flags = 0, and
> an updater's or compactor's copy-forward and set-no-other (§20.5) … are the
> cases this text states"

— so an updater that clears an inherited ignore-lane bit produces a **conforming
file** and no verifier will ever tell it otherwise. The checklist is the one
place an implementer auditing its own updater would expect to be told, and the
whole point of the rule is that nothing downstream will catch the mistake.

I checked the four normative statements of the prohibition against each other
word for word and found them consistent: §2.3 ("copy-forward and
set-no-other"), §6.3 ("MUST copy forward … MUST NOT clear them … MUST NOT set
any other"), §20.3 step 6 ("unknown ignore-lane flag bits copied forward and no
other set"), §20.5 ("MUST copy the input's unknown ignore-lane flag bits forward
and set no other"), plus Appendix G item 8 for the profile's compactor. Appendix
H is the one restatement site that carries nothing.

**Byte-level: no.** Appendix H is non-normative and says so ("each entry's
authority is the requirement or section cited, never this summary"), and §6.3
states the obligation plainly; a silence in a summary is not a competing
reading.

---

## 6. Suspicions I opened and closed

These are the things I chased that turned out to be clean. I record them because
a clean lane has to prove it looked.

- **§5.1's three-commit figure.** I reconstructed the commit history it implies
  (commit 1 = front + layer A + dir₁/pad/tr₁; commit 2 = layer B + dir₂/pad/tr₂;
  commit 3 = dir₃/pad/tr₃ alone) and checked it against the two ▓ runs drawn.
  It reconciles exactly. Its claims about which commits re-emit an index region
  agree with `[R-WRT-04]` and `[R-WRT-07]`, and it carries an explicit
  disclaimer that the grouping under the box is illustrative.
- **§20.5's compaction figure marks *both* index regions regenerated (`′`).** I
  suspected this was wrong, since `[R-WRT-07]` regenerates only "each
  tile-index region any of whose stored extents the output relocates", and the
  figure draws layer A first in both input and output. Closed: the figure says
  "Regions, not offsets", so it asserts no placement, and a compactor "preserves
  no placement" and may move A. Closed a second way: even if A's extents did not
  move, regenerating its region yields byte-identical output (entry offsets,
  lengths and crcs unchanged; segment CRCs recomputed over identical entries),
  so nothing turns on it.
- **§23.1's list of operations that make sample data unreachable names only "a
  shrink" as a de-addressing mechanism**, not the planar-channel removal §20.3
  now names beside it. Closed by the sentence at the end of the paragraph: "the
  list of operations above is not offered as closed." Its *two-case* claim, which
  *is* closed, survives: a planar channel removal puts the tile's extent out of
  the live state, which is case one. I verified §23.1's supporting claim that
  "§20.3 step 4 permits that shrink only where those bytes already hold the
  channel's recorded fill" against §20.3's carve-out — it is right, and it is
  what led me to finding diagrams-01.
- **§11.1's Rationale**, a labelled block restating §20.3's two bars, is the
  passage the brief's warning about "a labelled block restating a rule that was
  widened" most obviously fits. I checked all eight of its claims against §20.3
  clause by clause — which bar reaches a shrink, which a growth, the two
  de-addressing mechanisms, the carve-out, the re-declaration tense, re-typing a
  channel, the ordinal bar's subject, and the entry_count/extent_length
  implication — and every one matches. I separately verified its arithmetic
  claim that a change in entry_count always changes extent_length
  (`entry_count·20 + ⌈entry_count/2¹⁶⌉·4` is strictly increasing) and its claim
  that "growth that leaves entry_count unchanged touches the directory alone",
  which holds for both the within-grid case and the product-holding-at-0 case.
  Its only byte-shaped wording is the carve-out, which is diagrams-01.
- **§21.6's slack row** describes only two outcomes (a full total, or a partial
  total) where §5.2 has three (the third being a trailer failure before a live
  state exists, where no total is owed at all). Closed: in that third case the
  file is rejected outright, so this non-violation row cannot arise.
- **§2.3's closed list of writer obligations expressly declared not to be
  file-conformance violations** ("§6.3's flags rules … and §6.2's pre-trailer
  gap … are the cases this text states"). I derived the candidates myself and
  tested each: §10.3's experimental-value prohibition and §18.3's registry-version
  prohibition are in `[R-CNF-02]`'s *other* category (conduct rules), which the
  same paragraph names with both section numbers; §9.2's barriers are declared
  conduct rules in terms; `[R-COD-06]`'s undisclosed dictionary and
  `[R-COD-10]`'s mis-strided filter are *unwitnessed* violations, not
  non-violations, which §21.7 distinguishes explicitly; every other candidate is
  a SHOULD and so not a violation at all under `[R-CNF-12]`. **The list of two
  is right.**
- **Appendix B's "Every named constant this specification fixes, collected."**
  I hunted for omissions. The trailer's 12 reserved zero bytes and
  `[R-CNT-24]`'s 48 redefinable bytes are not tabulated; the user-metadata key
  cap is covered by the "Name length" row, since §4.6 defines names to include
  user-metadata keys. Not filed: the omissions are of field-fixed values rather
  than named constants, and Appendix B calls itself a finding aid.
- **§21.9's "hard limits" list.** Checked all nine against their defining
  sections; all correct. Not treated as a completeness claim, since the section
  says "a finding aid rather than an inventory".
- **§17.4's cannot-establish ground for a codec a verifier cannot execute**
  looks near-vacuous for a *conforming* verifier — an unexecutable assigned
  codec makes it a nonconforming reader, and a reserved or experimental value
  rejects the layer as a violation. Closed: §17.4 states that narrowing itself,
  in the sentence beginning "For a conforming reader that position arises only
  at a reserved or experimental value", so the document already knows.
- **§14.2's table has no row for a packed planar bool plane.** Closed:
  `[R-SER-07]` says "Whichever of §14.2 or §14.3 defines a tile's decoded size",
  §14.2's own prose scopes its planar row to numeric channels, and L2's instance
  list correctly omits ⌈P/8⌉ (bounded by P, which it does designate) while L44's
  correctly includes it (a different bound).
- **§17.2's Note citing "§14.2's worked examples give 18 and 30 bytes"** omits
  the 12-byte planar case from the same example. Not filed: all three are below
  the 1 KiB threshold the Note is about, so the omission changes nothing.
- **§19's step lists** looked like closed inventories of what a reader checks at
  each tier. Closed by §19's own opening: "Those enumerations are not the
  complete inventory of what a reader detects at that tier: §21's register is."
- **T2's claim that T2 and T4 "together cover `[R-SER-08]`".** I verified it: an
  interleaved bool byte at a padding position that is neither 0x00 nor 0x01
  necessarily differs from the channel's fill, which `[R-TYP-07]` constrains to
  0x00 or 0x01 — so every such byte falls to T4. The partition by position is
  exhaustive.
- **T7 versus T11 overlap.** T11 excludes the all-ones value in terms ("the
  value being distinct from the all-ones sentinel"), so a half-sentinel entry is
  T7's alone. Precise, not a defect; §21.1 and `[R-VEC-02]` handle rows that
  merely overlap.
- **§18.2's Window_Size gap** — a document between 8 MiB and 16 MiB framed with
  Single_Segment_Flag exceeds the Window_Size guarantee while sitting inside the
  document guarantee. Closed: §18.2 states this case in terms and tells a writer
  to use a Window_Descriptor instead.

---

## 7. What I would have found, and did not

The parts of my charter that came back clean, and what I did there:

**Every checksum, offset, width, and constant.** I wrote the CRC myself,
validated it against the document's published check vector *before* trusting it,
and ran it over the actual byte sequences the document prints — not over my idea
of what they should be. I reconstructed both hex dumps into byte buffers, cut
fields at the offsets and widths the *layout tables* give rather than the ones
the annotations give, and decoded each. A wrong constant, a stale offset column,
a mis-stated width, or a checksum computed over the wrong range would have
surfaced. None did. The §7.4 example in particular passes a test it did not have
to: every printed offset equals the running length of everything printed before
it, and the payload parses to exactly 81 bytes with zero residue.

**Instance and condition counts.** I extracted all 120 register rows
mechanically and applied §21.1's own semicolon rule rather than eyeballing. 120
and 277 both reconcile. A single added or dropped semicolon anywhere in those
tables would have shown as a mismatch against §21.8.

**Cross-table consistency.** I did the detector/detection-point check over all
120 rows programmatically (0 mismatches), grouped rows by governing rule to test
§2.3's "nine", derived §21.2's reach set independently, and counted §15.3's
"six structural" rows and §20.5's "seven spaces" by hand against §10.2.

**Where I am least sure.** Two places. First, whether diagrams-01 should be
graded byte-level: I decided it on the strength of one governing clause, and a
judge weighing the shrink paragraph's "the §14 bar is the whole of the test"
more heavily could reach the other verdict. Second, Appendix G's item 3
emission order — I checked its arithmetic and its alignment reasoning, but a
full check of whether the stated total order is in fact total (that no two
distinct records can tie under the masked-header key in a way the item's closing
sentence does not already excuse) would need a construction I did not build.
The item's own closing sentence — "Two records this key does not separate are
byte-identical in type, flags, lengths, payload and extent content; emitting
them in either order yields the same file" — appears to close it, but I did not
prove it.
