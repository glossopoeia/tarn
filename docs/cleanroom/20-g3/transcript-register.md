# Round 20 — Register hunter — verbatim working transcript

Charter: audit §21, the error-handling register, against the rules it restates
and against itself.

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full, in seven `sed` chunks. I ran `grep`/`python3` against that one file only,
and I ran a standalone CRC-32C implementation in Python that reads no files. I
opened no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no git
history, no network.

My runtime placed context in front of me before I began: a project instruction
file pointing at an agent guide, and an index of the maintainer's memory notes
naming this project's cadence and position. I disregarded it. Nothing in this
transcript derives from it; where it named a thing I could have used (a round
number, a prior finding class), I did not consult it and have not reproduced it.

Order of work: (1) full cold read; (2) mechanical recount of conditions and
instances; (3) requirement-ID coverage sweep in both directions; (4) row-by-row
comparison against each governing rule; (5) every cross-reference to a row;
(6) the limits material in both directions; (7) independent recomputation of
every CRC constant and worked layout the document states.

---

## 1. The counting — done by hand, then mechanised

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading — is one
> instance; the count is therefore mechanical once the cell is written.

I parsed each of the four register tables, took the third column, and counted
semicolon-separated items with `—` counting as one.

| Subsection | Rows counted | Rows claimed | Instances counted |
|---|---|---|---|
| §21.2 file scope | 36 | "36 conditions" | 58 |
| §21.3 layer scope | 49 | "49 conditions" | 116 |
| §21.4 tile scope | 26 | "26 conditions" | 55 |
| §21.5 ignored records | 10 | "10 conditions" | 44 |
| **total** | **121** | §21.8: "121 conditions over 273 instances" | **273** |

Every stated total reproduces exactly. Row labels are contiguous F1–F36,
L1–L49, T1–T26, R1–R10 with no gaps and no duplicates. §21.8's pair (121, 273)
is exact. This is the first thing I checked and it is clean; I record the
per-row counts below so the arithmetic can be re-run.

Per-row instance counts (F): 2,6,2,1,2,2,4,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,2,3,2,1,1,5,1,1,1 → 58.
Per-row (L): 8,9,1,2,1,1,2,2,2,1,1,2,1,3,4,2,2,3,1,1,4,4,4,1,1,1,1,1,3,2,3,3,4,4,1,2,1,1,3,1,3,1,3,3,3,2,2,1,4 → 116.
Per-row (T): 1,1,6,4,1,1,2,1,1,1,2,1,2,6,2,1,1,2,1,1,3,6,1,1,3,3 → 55.
Per-row (R): 4,2,2,12,8,4,6,2,2,2 → 44.

### 1.1 Testing each cell against §21.1's two stated axes

§21.1 states two axes rather than leaving them to judgement:

> Where the quantity a condition derives varies by layout, the layout formulas
> are materially different shapes and the cell enumerates them. Where the
> condition compares two **magnitudes** either of which can be the greater — a
> *differs from* or *does not equal* — the two directions are likewise
> enumerated; where its own text bounds the comparison in one direction — an
> *exceeds*, a *larger than* — there is one.

Layout axis. Every row deriving a layout-varying quantity enumerates the
formulas: L2 (nine derived quantities individually), L21 (interleaved N /
planar C·N), L44 (P·Q / P·Bᶜ / ⌈P/8⌉), T3, T14, T21, T22 (same three shapes),
T4 (four content shapes), T26 (three stride shapes). No row that should
enumerate by layout fails to.

Magnitude axis, checked one by one:
- one-direction (`below`, `less than`, `exceeds`, `larger than`, `above`):
  F5, F9, F10, F16, F22, F32, L1, L2, L11, L17, L44, T9, T11, T12, T21, T24,
  R10 — each gives one direction, multiplied only by field/container/layout.
- two-direction (`does not equal`, `differs from`, `is not`, `≠`):
  F17 (2), F23 (2), L12 (2), L21 (4 = 2×2), L22 (4 = 2 + 2 alternatives),
  L30 (2), T3 (6 = 2×3), T14 (6), T22 (6). All correct.
- no magnitude ordering (checksum vs computed, byte pattern vs constant):
  F6, F8, F14, F20, L37, L38, T1 — one each, as §21.1 requires ("*greater*
  names nothing").
- value tests (`nonzero`, `is 0`, `not a multiple of`): F11, F12, F13, F15,
  F18, F19, F24, L27, L28, L42 — one each.

Two cells I had to think about and then accepted:

L23's condition reads "does not lie entirely within inline_length (overrun or
truncation)" and enumerates four *regions*, not eight (four regions × two
directions). I accepted four: "overrun" and "truncation" are the same file
state described from either side — the region extends past the payload end iff
the payload is short of the region — so no two files could differ, and §21.1's
own rule ("One instance is one *distinguishable* file") gives one.

R8 collapses `1e400` and the bare token `NaN` into "in any form" (one
instance per container). Defensible under §21.1's "a row whose check ranges over
a family without the condition changing shape states that range as a single
instance", though a strict JSON parser meets the bare token as R7's
malformed-JSON case first. Not reported: the cell says "in any form" and the
count is therefore stated rather than judged.

Detector/detection-point consistency, mechanised: 101 rows carry Detector
*reader*, 20 carry *verifier*; every one of the 20 verifier rows carries
Detected *certification* and no reader row does. Detection points are drawn
only from {open, layer access, tile use, extent use, certification} plus R1's
compound cell, which is exactly §21.1's stated vocabulary.

Governing-rule cell shape: every cell is one bracketed identifier optionally
followed by a parenthesis of further identifiers, per §21.1's convention, with
two cells (L26, L31) putting a *section* reference in the parenthesis where
§21.1 says identifiers go. That is a convention slip with no consequence for
any reading, and I do not report it.

---

## 2. Independent recomputation of every stated constant

I implemented CRC-32C (reflected, poly 0x82F63B78, init/final 0xFFFFFFFF) from
§4.5's parameters and reproduced:

- `CRC-32C("123456789")` = 0xE3069283 ✓ (§4.5 check vector)
- `CRC-32C(<empty>)` = 0x00000000 ✓
- CRC over four sentinel entries (80 bytes `FF×16 00×4` ×4) = 0x80A34955, stored
  `55 49 A3 80` ✓ (§7.4 worked example)
- CRC over that 4-byte array = 0xC4EE982E ✓ (crc_of_crc_array in the same example)
- CRC over 2¹⁶ sentinel entries = 0xEECB3BB2 ✓ (`[R-IDX-05]`, Appendix B)
- Appendix A's trailer: CRC over the 60 bytes I assembled from the annotation
  table = 0xE00938D2, stored `D2 38 09 E0` ✓

I also rebuilt §7.4's layer-record inline payload byte for byte from the field
table and got 81 bytes matching the hex dump exactly, and confirmed
`[R-CNT-17]`'s arithmetic 4×20 + ⌈4/2¹⁶⌉×4 = 84.

§21.9's Note arithmetic: 2³² entries ⇒ 2¹⁶ segments × 4 bytes = 256 KiB ✓;
2³⁶ ⇒ 2²⁰ × 4 = 4 MiB ✓; 65,536 layers × ~200 B ≈ 12.5 MiB ✓; 2³² × 20 B ≈
86 GB, which is §24's "tens of gigabytes" ✓. §21.9's table matches Appendix B's
"Reader minimum guarantees" row term for term.

Nothing in the numeric surface is wrong.

---

## 3. Completeness, register → rules

I extracted all 161 requirement identifiers and marked which appear as a
Governing rule. Every unmarked identifier I then walked by hand to ask whether
it names a detectable file-conformance violation. Findings of that sweep:

- Conformance-framework, reader-behaviour, writer-conduct and corpus rules
  (`R-CNF-*`, `R-RDR-*`, `R-VEC-*`, `R-SEC-*`, `R-PRV-*`, `R-MDL-*`) impose no
  file condition. Correctly unregistered.
- SHOULD-only rules (`R-ENC-14`, `R-CNT-03`, `R-CNT-09`, `R-CNT-26`,
  `R-TYP-10`, `R-LIF-07`, `R-MTA-06`'s conduct half) are outside the register by
  `[R-CNF-12]`. Correct.
- Keyword-free declarative rules whose violation has no procedure of its own —
  `R-COD-02`, `R-COD-05`, `R-COD-07`'s frame half, `R-IDX-01`, `R-IDX-02`,
  `R-SER-01`, `R-SER-02`, `R-SER-03`, `R-TYP-02`, `R-ENC-09`, `R-EXT-02` — are
  each either handled by an explicit "cause" row that names the detecting row
  (T13, T15, T16, T23, T26) or witnessed by a row for a derived quantity
  (L22 for `R-IDX-01`'s region layout; T6/T7 for `R-IDX-02`; T3 for
  `R-SER-02`; T5 for `R-SER-03`'s pad bits). I looked hard here because a
  clause with no BCP 14 keyword has no force of its own; the document has in
  fact anticipated exactly this and the cause-row device covers it.
- History-only obligations (`R-LIF-01`, `R-LIF-02`, `R-LIF-03`, `R-LIF-04`,
  `R-WRT-05`–`R-WRT-09`, §20.3 step 4's bar) are accounted for in §21.7 or, for
  `R-LIF-04`, in §9.5's Note ("Residue past a completed commit carries no
  register row of its own"). One omission from §21.7's account is reported
  below (register-03).

Rule-by-rule forward check, i.e. every clause that assigns a validity error or
an outcome, mapped to its row(s):

- §4.1 `R-ENC-02` → F1. §4.2 `R-ENC-03` → F2, L1, T11. `R-ENC-04` → F3, L2, T12.
- §4.3 `R-ENC-07` (a known structure at another size) → F16, F22, F23, F29,
  L11, L12, L14, L22, L23, L30, F6. Every fixed-size structure the document
  defines has a witness row; I enumerated them individually.
- §4.6 `R-ENC-11` → L3, L4, R5. `R-ENC-12` → L5–L8, R6, R10. `R-ENC-15` → F4, L9.
- §5.1 `R-CNT-27` → F5. §5.2 `R-CNT-02` → F33, L18; §5.2's Note disposes of the
  "belongs to no class" half ("a register row for it would be a row no file
  could exhibit").
- §6.1 `R-CNT-04` → F6, F1. §6.2 `R-CNT-05` → F7. `R-CNT-06`: all eleven gates
  in §6.2's ordered list map to F8, F14, F18, F19, F17, F13, F9, F16, F10, F11,
  F2, F12, F15 — I walked the list item by item and none is unregistered.
- §6.3 `R-CNT-07` → F18 (and the foreign-major refusal is §21.6's, not a row).
  `R-CNT-08` → F19 (incompat lane), §21.6 (ignore lane).
- §7.1 `R-CNT-11` → F20. `R-CNT-25` → F21, F22, L10, L11, R1–R10.
- §7.2 `R-CNT-12` → F24/L13, F25/L46, F26/L47, F29/L14. `R-CNT-13` → F30–F33,
  L15–L18, F3, L2. `R-CNT-14` → F34, L19, §21.6 (zero layers).
  `R-CNT-15` → F35, F36, L24, L25.
- §7.3 `R-CNT-22` → F28, L49.
- §7.4 `R-CNT-16` → L20; `R-CNT-17` → L21, L22; `R-CNT-18` → L14, L23, L24, L26;
  `R-CNT-23` → L27–L36 plus the value-set rows.
- §8.1/§8.2: every checksum in the coverage map has a mismatch row — trailer
  F14, directory F20, segment CRC array L37/L38, stored tile T1, user-metadata
  extent R2, front block by equality F6. The unassigned-type extent has no
  checksum and correctly no row.
- §11 `R-GEO-01` → L32; `R-GEO-03` → L2; `R-GEO-05` → L33; `R-GEO-02`,
  `R-GEO-04`, `R-GEO-06` are non-violations or §21.7's.
- §12 `R-TYP-03` → L34. §13 `R-TYP-07` → L35.
- §14 `R-SER-05` → T4, T5; `R-SER-06` → L36; `R-SER-07` → T3; `R-SER-08` → T2
  (+ T4 for the padding-position byte); `R-SER-09` → §21.6.
- §15.3: all eleven rows of `[R-IDX-03]`'s table map to T6, T7, T10, T8, T11,
  T9+T12, T1, L18, F33, L40/L41/L42, with the sentinel row being §21.6's
  non-violation. I checked this table row for row; the split of §15.3's
  "offset + length overflows, or > F − 64" into T12 and T9 with different
  parenthetical rules is correct.
- §15.4 `R-IDX-04` → L37, L38; `R-IDX-05`'s "a partial segment's CRC MUST be
  computed" is inside L38's condition text explicitly.
- §16 `R-SLB-01` → L39, L40; `R-SLB-03` → L41, L42; `R-SLB-04` correctly has no
  row of its own and §16.2's Note says so.
- §17 `R-COD-03` → L43; `R-COD-04` → T14; `R-COD-05` → T15, T16; `R-COD-06` →
  T17–T22; `R-COD-07` → L44, T23; `R-COD-08` → T24, T25; `R-COD-09` → L45;
  `R-COD-10` → T26.
- §18 `R-MTA-03` → F23, L12, R1; `R-MTA-04` → R5–R10; `R-MTA-05` → F27, L48;
  `R-MTA-09` → R4; `R-MTA-10`, `R-MTA-06`, `R-MTA-07` → §21.6.

I found no MUST-level condition without a row.

## 3.1 Completeness, rules → register: does any row register a non-violation?

I took each row and asked whether the rule it cites actually makes the
condition a violation.

- F19: `R-CNT-08` makes flags = 0 a writer MUST and `R-CNF-02` excepts only the
  *ignore* lane from file conformance, so every set incompat bit is a violation.
  §10.1's four vehicles include only ignore-lane bits, so no minor version can
  ever define one. Correct.
- F35/F36, L24/L25, R1: reserved-range values are violations under `R-EXT-03`
  ("a value from a reserved range MUST NOT be emitted at all"). Correct, and
  the experimental range is correctly kept out (§21.6).
- F27/L48: `R-MTA-05` says in terms "the file is nonconforming, a verifier MUST
  report it". Correct, and §21.1 explicitly reconciles the verifier outcome
  with the reader's duty to process the document unchanged.
- T13, T15, T16, T23, T26: each is a genuine writer-side violation whose
  detection borrows another row's procedure; each says so.
- F2 correctly omits `file_id`. I checked this deliberately: `R-ENC-03`'s
  domain is "every offset, length, extent, and count", `file_id`'s only stated
  constraint is "≠ 0", and Appendix G item 2 derives a `file_id` from a hash's
  last eight bytes read little-endian, which routinely exceeds 2⁶³ − 1. The
  omission is right and the three places agree.

No row registers a non-violation.

## 3.2 The overlap question

Three row pairs overlap without being named in §21.1's specialization list
("F1 of F6 and of F8, F35 of F36, L24 of L25"): T14 ⊂ T3 (a codec-1 length
mismatch is also a decoded-length mismatch), L46's layer-record instance ⊂ L49
(the layer record's registered flags are MU=1/PE=1, so MU=1/PE=0 is also a
stored-flag mismatch), and F25's type-0x0002 case ⊂ F28. In each of the three
the detector, the detection point and the outcome are identical, so nothing
turns on which row a file is recorded against; the pairs §21.1 *does* name are
exactly the ones where the detector or the field differs. I read the list as
purposive rather than exhaustive and do not report this.

---

## 4. Row versus rule, one row at a time

I compared all 121 rows against the requirement each cites, on wording, outcome
class, scope and detector. The scope placements I checked hardest, because
`[R-CNT-12]`, `[R-CNT-13]`, `[R-CNT-15]` and `[R-CNT-22]` all assign "the
record's governing scope" and that scope differs between a layer record, a
sub-record and a non-layer top-level record. The split is right throughout:
F25/F26/F28 cover only "a non-layer top-level record" and L46/L47/L49 pick up
the layer record and its sub-records, which is what `[R-CNT-13]`'s "the layer
for a layer record and for sub-records, the file for other top-level records"
requires.

Detection-point placements I checked against §19.1–§19.3 line by line:

- L3, L5, L6 (layer-record name) are Detected *open*, and §19.1 step 4 does
  put the name parse and its §4.6 check at open. L4, L7, L8, L9
  (dimension/channel names) are Detected *layer access*, matching §19.3. The
  asymmetry is deliberate and correct.
- L23's Detected is *layer access*, while §19.1 step 4 obliges a reader to
  decide at open whether each layer record's name field "lie[s] entirely within
  that record's inline_length". These are consistent: §19.2 fixes the *latest*
  detection point, the namespace decision at open is about membership rather
  than about reporting, and §19 opens by saying its enumerations are not the
  complete inventory and "§21's register is".
- L37, L38 are Detected *tile use* with outcome reject-layer, which §19.2
  itself calls out: "index-chain failures take layer scope (`[R-IDX-04]`)
  although their detection point is tile use".
- R1's compound cell (open for the top-level record, layer access for the
  sub-record) is the only compound one and is right — the encoding byte lives
  in the inline payload, resident at its record's own tier, while R2–R10 are
  all *extent use*.
- The 20 verifier rows are all *certification*, which §21.1 places outside the
  reader tiers.

Row texts against constants: F8's magic, F14's offset 60 and range [0,60),
F15's [56,60), F26/L47's bits 2–15, F29's `dir_offset + dir_length − 4`,
F31's 1–15, F35/F36/L24/L25's 0x0003–0x7FFF, L22's formula, L29's 1…2⁶²,
L31's 2–0x7F / ≥0x80, L33's 2–3 / 4–0x7FFF / ≥0x8000, L34's 14–19 / 20–0x7FFF,
L36's 3–255, L38's segment range and 0xEECB3BB2, L39's 512…2⁶², L43's
5–0x7FFF, L45's 3–0x7FFF, T6's all-ones, T11's "bit 63 set", T17's
`28 B5 2F FD`, T23's `04 22 4D 18` (LZ4 frame magic 0x184D2204 little-endian),
L44/T-rows' 0x7E000000, R1's 3–0x7F, R10's 255 — every one matches its
defining section. No numeric error in the register.

One row's condition text does not restate the whole of its rule; that is
finding **register-01** below.

---

## 5. Every cross-reference to a row

I grepped the whole document for row labels outside §21.2–§21.5 and resolved
each.

| Site | Cites | Resolves? |
|---|---|---|
| §5.2 `[R-CNT-21]` | L18, L40–L42 | ✓ all four are verifier rows the coverage walk itself establishes at layer scope |
| §9.6 `[R-LIF-06]` | F8, F17 | ✓ both say what is claimed |
| §17.2 deflate Note | T24 | ✓ trailing byte past the final bit |
| §20.3 step 4 | L44 | ✓ the lz4 decoded-size cap |
| §20.5 `[R-WRT-06]` | F36, L25, R1 | ✓ — see below |
| §21.1 | F1/F6/F8, F35/F36, L24/L25, T24, T15, T25, F27, L48 | ✓ |
| §21.7 | T2, T4, T5, T3, T14, T15, T17, T23, T25 | ✓ |
| Appendix H verifier list | F1, F6, F7, F36, L25, R1 | ✓ |

§20.5's `(F36, L25, R1)` I checked closely because it looks like an
under-enumeration: the reserved-range rows also include L31, L33, L34, L36,
L43 and L45. It is not an error. The sentence is about a *compactor* carrying
forward a feature it does not implement, and `[R-WRT-09]` makes a compactor
perform §19.3's layer validation on every retained layer record — so every
reserved-range value in a layer-record field forces refusal and can never reach
a compactor's output. What survives is exactly the reserved-range record type
(verifier-detected: F36, L25) and the reserved metadata encoding (ignore-record:
R1). The three named rows are precisely the reachable set. I record this because
it took work to satisfy myself and a later reader may make the same false start.

§9.6's `(§21.2 rows F8 and F17)` names two of the three grounds §9.5's parallel
Note names ("the magic, the CRC, or committed_file_length against the transport
size" — F8, F14, F17). Both cited rows resolve and say what is claimed, so
this is not a mis-citation; I considered and rejected it as a finding.

---

## 6. Outcome vocabulary

`[R-CNF-07]` defines exactly four reader outcomes and §2.4 adds
preserve-verbatim as an orthogonal updater obligation. Every register row's
outcome is fixed by its subsection: reject-file (§21.2), reject-layer (§21.3),
reject-tile (§21.4), ignore-record (§21.5). All four defined values are
reachable, and no row carries a value outside the vocabulary.
preserve-verbatim correctly has no register subsection — §2.4 says it "names an
updater obligation, orthogonal to reader outcomes" — and §20.4's table states
its cases.

I also checked that §21.5's preamble does not silently make a reader outcome do
double duty: it says "the outcome bounds a reader's blast radius and never
makes the file conforming (`[R-CNF-12]`)", and for the one row family whose
reader outcome (ignore-record) differs from the scope at which the damage is
recorded — a reserved-range MU = 0 top-level record, ignored by a reader but
registered at file scope as F36 — §21.1's "For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not an
obligation on any reader" already reconciles it.

---

## 7. Limits, in both directions

**§21.9's minimum-guarantee table against the rest of the document.** Every row
of the table is consistent with its defining section, and no defining section
states a different figure. Cross-checks: §2.3 and §2.5 (`[R-CNF-10]`) both point
at "§21's limits table" and agree that the guarantees are a floor a reader MUST
meet; §18.2's Note calls the 16 MiB metadata figure "a §21.9 minimum
guarantee"; `[R-MTA-09]` requires a decode bound "no smaller than §21.9's
user-metadata guarantee"; `[R-COD-06]` names "§21.9's 8 MiB `Window_Size`
guarantee"; §1 names "§21.9's tile-count guarantee"; §24 `[R-VEC-03]` explains
why the tile-count guarantee has no constructible vector, and 2³² × 20 B does
indeed run to tens of gigabytes. Appendix B's summary row reproduces all eight
figures verbatim.

No guarantee conflicts with a hard limit: C 4096 < 65,535; rank 32 < 255;
tile 256 MiB < codec 4's 0x7E000000; window 8 MiB is a SHOULD-target inside
`[R-COD-06]`'s "a wider window is conforming".

**Hard limits.** `[R-ERR-05]`'s list — name 255 B, key 255 B, rank 255,
C 65,535, 0x7E000000, 2⁶³ − 1, A ∈ [512, 2⁶²], A_slab ∈ [1, 2⁶²],
S ∈ [1, 2⁶³ − 1], dir_offset ≥ 16 / dir_length ≥ 4, file ≥ 128 B — each matches
its defining section exactly. Its closing claim, that all but two follow from a
field width, an external format, the value domain, or unavoidable arithmetic,
holds: A ≤ 2⁶² and A_slab ≤ 2⁶² follow from the value domain plus
power-of-two, so the only two chosen numbers really are the 512 floor and the
255-byte key cap.

Limits stated elsewhere and absent from §21.9 — the ≥ 5 user-metadata extent
(§7.1), 1 ≤ generation ≤ 2⁶³ − 1 (§6.2), F mod 64 = 0, the 65,536-byte
discovery window (§6.4, a SHOULD), the 2¹⁶-entry segment (§15.4), the two-deep
nesting bound (§7.4) — are all licensed by §21.9's own "The hard limits it
restates are a finding aid rather than an inventory". I record the sweep so the
next reader does not have to repeat it; there is no finding here.

---

## 8. Where I had to guess

### register-01 — R7's Instances cell prices an alternative its Condition cell does not state

§21.5, row R7. The Condition cell reads:

> A decoded user-metadata document is not well-formed JSON, or its top-level
> value is not an object

Its Instances cell reads:

> not well-formed JSON, top-level document; not well-formed JSON, layer
> sub-record document; top-level value not an object, top-level document; top-level
> value not an object, layer sub-record document; leading U+FEFF, top-level
> document; leading U+FEFF, layer sub-record document

Six instances = three alternatives × two containers. But the Condition cell
states only two alternatives. §21.1 is explicit about what an instance may be:

> An instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any combination
> of the three

so a cell enumerating an alternative the condition text does not state is
inconsistent with the register's own arithmetic rule. The governing rule
`[R-MTA-04]` does state it, as a separate limb of its first restriction:

> **A JSON object, unmarked.** The top-level value is an object, and the
> encoding carries no byte-order mark: a leading U+FEFF makes the document
> unreadable.

Permitted readings. (a) A leading U+FEFF is a species of "not well-formed
JSON", so the Condition cell already covers it and the third pair of instances
is a sub-enumeration of the first. (b) It is a distinct restriction the Condition
cell omits, and the row understates its rule. I pick (b): RFC 8259 forbids a
producer from emitting a BOM but permits an implementation to ignore one, so a
document that is a valid JSON object behind a BOM is not naturally "not
well-formed JSON" — it is unreadable here only because `[R-MTA-04]` says so
separately. §21.1's "where a row and the rule it cites diverge, **the rule
governs**" settles the reading: the BOM makes the document unreadable and R7's
instance count of six is right. Only the Condition cell is wrong.

What an implementer gets wrong without it: nothing at read time — the rule is
plain. What a *corpus* builder gets wrong is real: reading R7's Condition alone,
a builder writing vectors from the register (§21.8 requires "one vector per
instance") has no condition text telling it what the two U+FEFF vectors are
supposed to exercise, and `[R-VEC-02]` requires each entry to name "the §21
register row it exercises together with that row's governing requirement
identifier".

Not byte-level. Both readings reject the document identically (ignore-record);
`[R-MTA-04]` decides the byte question on its own.

### register-02 — §21.6 attributes §20.4's preserve/drop obligations to `[R-WRT-08]`, whose own sentence states a different rule

§21.6's fifth table entry:

> | A record type this specification has not assigned, from the experimental
> range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
> per its PE bit; a *reserved*-range type is read the same way, but emitting one
> is a violation (F36, L25) | `[R-CNT-15]`, `[R-WRT-08]` |

§21.1 puts these entries under the register's discipline:

> §21.6's entries restate their governing rules on the same terms a row does,
> and where such an entry and the rule it cites diverge, the rule governs there
> too.

Three things had to be guessed here.

First, *which requirement identifier owns §20.4's flags table*. §20.4 runs:
paragraph 1, ending `[R-WRT-05]`; then "Persistence governs every record type;
only the authoritative source of the flags differs. … and carry these
obligations:", the two-column table, and "No commit therefore removes a layer
record…", none of which carries an identifier; then a final paragraph ending
`[R-WRT-08]`, whose own sentence is

> An updater MUST NOT re-encode a record whose type it does not implement, and
> MUST NOT modify one except by relocating its extent and re-pointing its slot
> under §20.5

which says nothing about preserving or dropping. The table nonetheless carries
real BCP 14 obligations ("The updater MUST NOT modify the scope the record
governs", "An appender MUST NOT drop it except in a commit that *independently*
changes the scope the record attaches to", "a commit whose only effect would be
the drop MUST retain it", "A compactor MAY drop it"), and §2.2 says normative
requirements carry identifiers. Permitted readings: (a) the unlabelled
paragraphs are part of `[R-WRT-08]`'s block, the identifier following the whole
run of text as it does for `[R-CNF-11]`, `[R-WRT-04]` and `[R-WRT-06]`; (b) the
table is normative text with no identifier at all. I pick (a), because §21.6's
citation asserts it and because (b) would make the table an unidentified
requirement, which §2.2 forbids. Everywhere else the document cites the table by
section — §2.4 ("§20.4's table states the cases"), `[R-CNF-06]` ("the
preservation obligations of §20.4"), Appendix H — so §21.6 is the only place
that pins an identifier to it, and it pins one whose own sentence is about
something else.

Second, the entry says "preserved or dropped **per its PE bit**" without
§20.4's qualifier. §20.4 is explicit that the stored bit is authoritative only
for a type the updater does not implement:

> For a type the updater implements that this specification does not register,
> the definition it implements the type from supplies the flags, and the stored
> bits never do (`[R-CNT-22]`, §10.3). For a type the updater does not
> implement, the stored flags are authoritative

An updater that *does* implement an experimental type takes that type's flags
from its own definition, not from the record's PE bit. The §21.6 entry drops
that scope qualifier; the rule governs.

Third, the entry's behaviour claim reaches sub-records — it names L25, the
sub-record row — but cites `[R-CNT-15]`, which is scoped "at file scope". The
sub-record rule is `[R-CNT-18]`, uncited.

What an implementer gets wrong without it: an updater that implements an
experimental record type and reads §21.6's entry alone will let the stored PE
bit decide whether it may drop the record, where §20.4 gives that decision to
the definition the type is implemented from. That is a real divergence in what
a re-emitted directory contains.

Not byte-level, on the discriminator's own terms: `[R-CNF-05]` gates emission on
file conformance, and both dispositions produce a conforming file — a record
retained byte-identically and a record dropped are each conforming outputs of a
conforming updater. What differs is whether the record survives a commit, which
is a preservation question rather than an accept/reject one, and §20.4's text
decides it either way.

### register-03 — §21.7 counts "two" obligations on a compacted file's trailer where there are more that are equally unwitnessed

§21.7's second set opens "A second set of obligations is omitted from the
register because a single file exhibits no witness of their violation" and later
says:

> §20.5's two obligations on a compacted file's trailer (`[R-WRT-06]`) — the
> unknown ignore-lane bits it MUST carry forward, and the floor its
> version_minor SHOULD take — are unwitnessed for that same reason, the output
> carrying no record of its input's flags or its input's minor

§20.5 places four things on the output trailer, not two:

> It MUST mint a fresh file_id for the output — a new draw under §9.3's
> randomness advice, not merely a value compared against the input's — and
> generation 1 … The output trailer MUST copy the input's unknown ignore-lane
> flag bits forward … the output's version_minor SHOULD be at least the input's

The fresh-`file_id` obligation is omitted from the register and is unwitnessed
in exactly the sense §21.7 is accounting for: a single file cannot show that its
`file_id` equals its input's, and "a new draw" has no witness even with both
files in hand. The generation-1 obligation is likewise unwitnessed *as a
compaction obligation* — a generation-5 output is visibly generation 5, but
nothing in the output says it was a compaction — though `[R-LIF-03]`'s
generation sequence, which §21.7 does name, covers it.

The definite description "§20.5's two obligations on a compacted file's
trailer" therefore mis-counts §20.5. §20.5's own answering sentence, "Neither
obligation has a witness in the output alone (§21.7)", is consistent with the
pair §21.7 names, so the two sections agree with each other and disagree with
§20.5's list of trailer obligations.

I note against myself that §21.1 removes §21.7 from the register's normative
completeness clause — "neither this completeness clause nor the instance
arithmetic below reaches … §21.7's account of what no check detects" — so an
omission from §21.7 is not by itself a register defect. What is a defect is the
numeral: a reader counting §20.5's trailer obligations gets four, and a reader
counting the unwitnessed ones gets at least three.

What an implementer gets wrong without it: a verifier author reading §21.7 as an
inventory may look for, and fail to find, a check on `file_id` freshness, or
conversely may believe one exists because §21.7 accounted for only two of
§20.5's trailer obligations. Neither is registered and neither is checkable; the
text should say so.

Not byte-level. No byte sequence's emittability turns on it and no accept/reject
verdict moves; the obligations in question have no witness under either reading.

### register-04 — §21.2's preamble enumerates the rows that reach a foreign-major file by a rule that does not reach F5, and nothing places `[R-CNT-27]`'s 128-byte check relative to the version gate

§21.2's preamble:

> A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below whose
> subject is that file's *geometry* do not reach it: §6.2 puts the version gate
> ahead of every check but the trailer magic and the trailer CRC, so such a file
> is refused on capability grounds first. Four rows are outside that reasoning
> and do reach it, because their subject is a field fixed across every major
> (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC — the
> two checks §6.2 places before the gate — and F6 with F1's front-block
> instance, which `[R-CNT-04]` places before other processing.

The justification is that §6.2 orders the version gate ahead of everything else.
But two of this document's file-scope checks are stated *outside* §6.2's ordered
list. One is the front-block equality check, and the preamble names it as an
exception precisely because `[R-CNT-04]` gives it its own placement ("before
other processing"). The other is F5's, and it has no placement anywhere:

> No conforming file is shorter than 128 bytes … A reader MUST treat a shorter
> file as a validity error at file scope. `[R-CNT-27]`

`[R-CNT-06]`'s ordered list does not contain it, and §19.1's open algorithm does
not mention it at any step — even though step 1 already puts F, the
transport-authoritative file size, in the reader's hand before the trailer is
fetched, which is the natural place to test it.

Permitted readings, for a file of 64 to 127 bytes whose final 64 bytes carry a
valid trailer magic and CRC and a `version_major` the reader does not implement:

(a) `[R-CNT-27]`'s check runs where the size becomes available — §19.1 step 1,
ahead of the version gate — so the file is a validity error at file scope, F5
fires, and a verifier reports *nonconforming*. This reading is natural for an
implementer, since F5's Detected cell is *open* and step 1 of the open is where
F is obtained.

(b) The preamble's enumeration is exhaustive: only four rows reach such a file,
so `[R-CNT-27]`'s check runs after the version gate, the reader refuses on
capability grounds, and a verifier reports *cannot establish*.

I pick (b). §2.3 forecloses (a)'s verdict outright — "a file declaring another
major is neither conforming nor nonconforming under it … and that refusal is not
a finding about its bytes" — so a verifier may not report *nonconforming* for
such a file whatever else it observes, and the preamble's "Four rows" is
therefore the correct list. But the preamble reaches that result by a
justification that does not cover F5, and it does not name F5 as it names F6.

What an implementer gets wrong without it: a verifier reports *nonconforming*
for a file this specification declines to judge, and its diagnostic sends an
operator to "corrupt" rather than to "wrong format major" — the same
mis-routing `[R-ERR-04]` legislates against for resource refusals ("a reader
that reports 'too large' as 'corrupt' invites the deletion of intact data"). It
also matters to the corpus: a vector built at this boundary would record the
wrong expected outcome.

Not byte-level. Under both readings a reader refuses the file and a verifier
declines to certify it, so no byte sequence changes its emittability and no
accept/reject verdict flips; what forks is the verdict *label* a verifier prints
(*nonconforming* versus *cannot establish*) and the diagnostic class. I grade it
honestly rather than reaching for byte-level, while noting that §2.3 does make
the three verifier verdicts normative reportable values.

---

## 9. What I checked and found clean, recorded so it is not re-walked

- All four stated condition counts and the 273-instance total (§1).
- Every CRC constant, the §7.4 worked payload, and §21.9's Note arithmetic (§2).
- Requirement-ID coverage in both directions, including every keyword-free
  declarative rule (§3, §3.1).
- Every row against its governing rule on wording, outcome, scope and detector
  (§4), and the detection-point placement of every row against §19.1–§19.3.
- All eight cross-reference sites naming register rows (§5), including §20.5's
  `(F36, L25, R1)`, which is precise rather than under-enumerated.
- The outcome vocabulary: four defined values, all reachable, none exceeded (§6).
- §21.9 in both directions against every other statement of a limit (§7).
- §15.3's eleven-row entry-validity table, mapped row for row onto T1, T6–T12,
  L18, L40–L42 and F33.
- §8.1's coverage map: every checksum has a mismatch row.
- §21.6's fourteen non-violation entries against their cited rules; thirteen are
  exact, the fourteenth is register-02.
- §21.5's ten rows against `[R-MTA-04]`'s four restrictions and `[R-MTA-09]`'s
  frame constraints; R4's twelve instances are six constraints × two containers,
  matching `[R-MTA-09]`'s list plus the extent-occupancy clause.

Four findings, all reported above, none byte-level.
