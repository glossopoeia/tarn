# Cleanroom round 16 — Register hunter transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4282 (the whole document). I ran `wc -l`
on it and three Python scripts I wrote myself in the scratchpad
(`count.py`, `crc.py`, and one inline heredoc) — all of which read only
`spec/tarn.md` or nothing at all. I ran two `grep` invocations against that
same file. I opened no ADR, no `docs/` file, no `conformance/` file, no
`registry.json`, no `PLAN.md`, no `AGENTS.md`, no README. I ran no git
command, no web search, no web fetch. I did not list the output directory.

I did read the task-list system reminder that the harness injected
unprompted (it names round 13–16 and a task titled "Fix §21.1
instance-criterion asymmetry (T3/T14, F33/F7)"). I did not seek it and it
is not a file I opened, but I disclose it because it told me which §21.1
rule had recently been reworked, which shaped where I looked. It told me
nothing about what any answer is, and I verified T3/T14 and F33/F7
independently from the document text before I saw it in that light.

---

## 0. Method

My charter is §21, the error-handling register. I ran it as four passes:

1. **Mechanical arithmetic.** Reproduce §21.1's counting rules over the
   literal cells and compare against every total the document states.
2. **Row-versus-rule.** For every one of the 121 rows, find the governing
   requirement, read it, and compare condition text, outcome, scope,
   detector, detection tier.
3. **Completeness both ways.** Sweep every MUST/MUST NOT in §§1–20 and 22–24
   for a file-conformance condition, and check each has a row; then check
   no row registers something the rules do not make a violation.
4. **Cross-references and limits.** Every citation of a row label anywhere
   in the document; §21.9's limits against every other statement of a
   limit.

Then I built things: the minimal file's trailer bytes, §7.4's layer-record
payload, the sentinel CRCs, and a concrete two-generation commit to test
§21.7's witness claim.

---

## 1. The arithmetic

### 1.1 Condition counts

Rows counted straight off the tables:

| Subsection | rows | stated |
|---|---|---|
| §21.2 | F1…F36 = **36** | "36 conditions" ✓ |
| §21.3 | L1…L49 = **49** | "49 conditions" ✓ |
| §21.4 | T1…T26 = **26** | "26 conditions" ✓ |
| §21.5 | R1…R10 = **10** | "10 conditions" ✓ |
| total | **121** | §21.8 "121 conditions" ✓ |

### 1.2 Instance counts

§21.1 fixes the arithmetic:

> Instances within a cell are separated by semicolons, and a cell reading —
> is one instance; the count is therefore mechanical once the cell is
> written.

I applied exactly that (semicolons + 1; `—` = 1) with a script over the
markdown table rows, and by hand as a cross-check. Per-row:

```
21.2 F1:2 F2:6 F3:2 F4:1 F5:2 F6:2 F7:4 F8:1 F9:1 F10:1 F11:1 F12:1 F13:1
     F14:1 F15:1 F16:1 F17:2 F18:1 F19:1 F20:1 F21:1 F22:1 F23:2 F24:1
     F25:1 F26:1 F27:1 F28:2 F29:3 F30:2 F31:1 F32:1 F33:5 F34:1 F35:1 F36:1
21.3 L1:8 L2:9 L3:1 L4:2 L5:1 L6:1 L7:2 L8:2 L9:2 L10:1 L11:1 L12:2 L13:1
     L14:3 L15:4 L16:2 L17:2 L18:3 L19:1 L20:1 L21:4 L22:4 L23:4 L24:1
     L25:1 L26:1 L27:1 L28:1 L29:3 L30:2 L31:3 L32:3 L33:4 L34:4 L35:1
     L36:2 L37:1 L38:1 L39:3 L40:1 L41:3 L42:1 L43:3 L44:3 L45:3 L46:2
     L47:2 L48:1 L49:4
21.4 T1:1 T2:1 T3:6 T4:4 T5:1 T6:1 T7:2 T8:1 T9:1 T10:1 T11:2 T12:1 T13:2
     T14:6 T15:2 T16:1 T17:1 T18:4 T19:1 T20:1 T21:3 T22:6 T23:1 T24:1
     T25:3 T26:3
21.5 R1:4 R2:2 R3:2 R4:12 R5:8 R6:4 R7:6 R8:2 R9:2 R10:2
```

Subtotals **58 + 116 + 57 + 44 = 275**. §21.8 states "121 conditions over
275 instances". **Both totals reproduce exactly.** I checked the hand count
against the script and they agree row for row.

### 1.3 The instance criterion, applied

The mechanical count is only half the question; §21.1 also states *what* a
cell should say. I audited the two axes it names.

**Layout axis** — "Where the quantity a condition derives varies by layout,
the layout formulas are materially different shapes and the cell enumerates
them." Rows where a layout-varying quantity is compared: T3 (3 layouts × 2
directions = 6 ✓), T14 (6 ✓), T21 (3, one direction ✓), T22 (6 ✓), L44 (3,
one direction ✓), L21 (2 layouts × 2 directions = 4 ✓), T4 (4 layout-derived
shapes ✓), T26 (3 ✓). L2 lists `P·Q` and `P·Bᶜ` separately ✓ and correctly
omits `⌈P/8⌉`, which `P` dominates. **Consistent throughout.**

**Magnitude axis** — "differs from"/"does not equal" → two directions;
"exceeds"/"larger than" → one; checksum-vs-computed or pattern-vs-constant →
none; nonzero test → none. Checked: T3 "is not exactly" = 2 ✓; T14 "differs
from" = 2 ✓; T22 "does not equal" = 2 ✓; T21 "larger than" = 1 ✓; L44
"exceeds" = 1 ✓; L21 "does not equal" = 2 ✓; L30 "differs from" = 2 ✓; F17
"does not equal" = 2 ✓; L37/L38/T1/F14/F20 checksum comparisons = 1 each ✓;
L20 (`A ≠ 0` and `S ≠ 0`), L27, L28 nonzero tests = 1 each ✓; F9 "less than
16", F16 "less than 4" one-directional = 1 each ✓.

**Value-space enumerations** are internally consistent too: L31 (3: 0 /
reserved 2–0x7F / experimental) ✓, L33 (4: 0 / reserved 2–3 / reserved
4–0x7FFF / experimental — §11.4 does state two reserved subranges) ✓, L34 (4,
§12.2 states 14–19 and 20–0x7FFF separately) ✓, L36 (2 — channel layout has
**no** experimental range per §10.2, and the cell correctly omits one) ✓,
L43 (3) ✓, L45 (3) ✓.

The one place the criterion does not reproduce the cells is the
skippable-frame enumeration — see **register-03** below.

### 1.4 Detector / detection-point consistency

Script check over all 121 rows: every row's Detector is `reader` or
`verifier`; every row's Detected is one of §19.2's four reader tiers or
`certification`; and `Detector = verifier` **iff** `Detected =
certification`, with no exceptions. Tallies: reader 101 / verifier 20;
layer access 35, open 32, tile use 24, certification 20, extent use 9, and
R1's split cell `open (top-level); layer access (sub-record)`.

That last is right: a top-level record's inline payload is resident and
walked at open (§19.1 step 4), a sub-record's is parsed at layer access
(§19.3).

### 1.5 Outcome vocabulary

§2.4 `[R-CNF-07]` defines exactly four reader outcomes plus the orthogonal
updater obligation:

- **reject-file** → §21.2's 36 rows ✓ reachable
- **reject-layer** → §21.3's 49 rows ✓ reachable
- **reject-tile** → §21.4's 26 rows ✓ reachable
- **ignore-record** → §21.5's 10 rows ✓ reachable, plus §21.6's
  non-violation entries (experimental metadata encoding)
- **preserve-verbatim** → not a register outcome by construction; §2.4 says
  "§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows",
  and §20.4's table does state both ✓ reachable

Every row's outcome is one the document defines, and every defined value is
reachable. **No defect on this axis.**

---

## 2. Row versus rule, all 121 rows

I read each governing requirement and compared. Rather than narrate all 121
(a walk that narrates and finds nothing is worth less than one that builds),
I record the mapping and then only the rows where I found something.

### 2.1 §21.2 — file scope

F1←`[R-ENC-02]`; F2←`[R-ENC-03]`; F3←`[R-ENC-04]`; F4←`[R-ENC-15]`;
F5←`[R-CNT-27]`; F6←`[R-CNT-04]`; F7←`[R-CNT-05]`; F8–F17←`[R-CNT-06]`;
F18←`[R-CNT-07]`; F19←`[R-CNT-08]`; F20←`[R-CNT-11]`; F21/F22←`[R-CNT-25]`;
F23←`[R-MTA-03]`; F24/F25/F26/F29←`[R-CNT-12]`; F27←`[R-MTA-05]`;
F28←`[R-CNT-22]`; F30–F33←`[R-CNT-13]`; F34←`[R-CNT-14]`;
F35/F36←`[R-CNT-15]`. All agree in wording, scope and outcome.

Field-completeness of F2: the trailer's u64 fields are generation,
dir_offset, dir_length, committed_file_length, file_id. F2 lists the first
four and correctly omits `file_id`, which is an identifier and not "an
offset, length, extent, or count" under `[R-ENC-03]` (its own constraint,
`≠ 0`, is F12). The record header contributes extent_offset/extent_length
(both listed) and inline_length (a `u32`, max 2³²−1, so out of reach). **F2
is complete.**

The §21.2 preamble's foreign-major carve-out checks out. `[R-CNT-24]` fixes
across every major: the trailer magic at F−64, version_major/minor at F−56,
the CRC at F−4 over [F−64, F−4), and the front block. The rows whose subject
is one of those are F8, F1's trailer-magic instance, F14, F6, F1's
front-block instance — **four distinct rows** (F1, F6, F8, F14), exactly as
the preamble says. F5 (128-byte floor) and F13 (multiple of 64) correctly do
*not* reach a foreign major, since a future major may redefine trailer bytes
[8, 56) and a two-structure minimum of 80 bytes is all `[R-CNT-24]` forces.
F18 is handled as "outside the premise" ✓ and §21.6's closing paragraph
agrees.

F19: I checked whether a set incompat-lane bit is really a *file*
violation rather than a capability refusal. `[R-CNT-08]` says "a writer
creating a file under this text MUST write flags = 0, but a set ignore-lane
bit is not a file-conformance violation" — the contrast is decisive, and
§10.1 vehicle 3 admits only *ignore*-lane bits as a growth vehicle, so no
minor version can ever make an incompat bit legal. F19 is correctly a
violation, and correctly absent from §21.6's two "conforming files a reader
nevertheless refuses" cases.

### 2.2 §21.3 — layer scope

L1←`[R-ENC-03]`; L2←`[R-ENC-04]`; L3/L4←`[R-ENC-11]`; L5–L8←`[R-ENC-12]`;
L9←`[R-ENC-15]`; L10/L11←`[R-CNT-25]`; L12←`[R-MTA-03]`;
L13/L14/L46/L47←`[R-CNT-12]`; L15–L18←`[R-CNT-13]`; L19←`[R-CNT-14]`;
L20←`[R-CNT-16]`; L21/L22←`[R-CNT-17]`; L23/L24/L26←`[R-CNT-18]`;
L25←`[R-CNT-15]`; L27–L31←`[R-CNT-23]`; L32←`[R-GEO-01]`; L33←`[R-GEO-05]`;
L34←`[R-TYP-03]`; L35←`[R-TYP-07]`; L36←`[R-SER-06]`; L37/L38←`[R-IDX-04]`;
L39/L40←`[R-SLB-01]`; L41/L42←`[R-SLB-03]`; L43←`[R-COD-03]`;
L44←`[R-COD-07]`; L45←`[R-COD-09]`; L48←`[R-MTA-05]`; L49←`[R-CNT-22]`.

Two things I checked hard and found sound:

**L3/L5/L6 at *open* with a *layer* outcome.** This looked wrong at first —
a layer-scope row detected at the file-open tier. It is right. §19.1 step 4
builds the layer table from "each layer record's name, parsed and checked
per §4.6", and §19.2's open bullet names "the layer-name namespace". The
name's owning scope is the layer (§7.4), so the outcome is reject-layer and
the tier is open. I then checked the neighbouring case: a layer record whose
*name field does not fit* inline_length. §19.1 says such a record
"contributes no name to the namespace and is instead a validity error at
layer scope (`[R-CNT-18]`)", and the register puts that in L23 at **layer
access**, not open. I spent a while on whether that is a tier divergence and
concluded it is not: the open needs an *obtainable* name; where none is
obtainable the open contributes nothing and the framing error is left to
layer access, which is exactly what keeps `[R-RDR-01]`'s two-request open
from becoming layer-by-layer validation. The two rows partition cleanly —
obtainable name → content checks at open (L3/L5/L6); unobtainable name field
→ framing check at layer access (L23). **Not a finding.**

**The (S, A_slab) space.** L28 = S=0 with A_slab≠0; L29 = S≠0 with A_slab not
a power of two in 1…2⁶² (A_slab = 0 included); the fourth quadrant is valid.
Complete, no overlap. L39 correctly has no "A = 0" instance because A = 0
means *none declared*, whereas L29 correctly does have "A_slab = 0" because
under S≠0 that value is forced invalid by §7.4. This asymmetry is deliberate
and right.

**L2's derived-quantity list.** Nine instances. I checked the domination
claims: `C·N` does dominate the max disk ordinal `(C−1)·N + (N−1) = C·N − 1`;
`P·Q` does dominate `V = P·C`, since `Q = Σ Bᵢ ≥ C` (every `Bᵢ ≥ 1`,
bool included at 1). `Q` itself cannot overflow (C ≤ 65535, max Bᵢ = 8, so
Q ≤ 524,280). `⌈P/8⌉` is dominated by `P`. **The list is complete and the
parentheticals are true.**

### 2.3 §21.4 — tile scope

I rebuilt §15.3's classification table from scratch and mapped every row:

| §15.3 entry state | register row |
|---|---|
| offset=S ∧ length=S ∧ crc=0 | not a violation → §21.6 row 1 |
| offset=S ∧ length=S ∧ crc≠0 | T6 |
| exactly one of offset/length = S | T7 |
| length = 0 (non-sentinel) | T10 |
| offset < 16 (non-sentinel) | T8 |
| offset or length > 2⁶³−1 | T11 |
| offset+length overflows | T12 |
| offset+length > F−64 | T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 |
| overlap outside its layer | F33 |
| alignment or slab invariant | L40 / L41 / L42 |

**Every row of §15.3 has a register row, and every §21.4 index row traces
back to a §15.3 row. No gap in either direction.**

T2/T4 partition `[R-SER-08]`'s bool byte by position (real vs padding), and
T4 does cover the padding case correctly: `[R-SER-05]` fixes a padding
position's interleaved bool byte to the *recorded fill byte*, which
`[R-TYP-07]` constrains to 0x00 or 0x01 (L35 enforces), so any byte outside
{0x00, 0x01} at a padding position differs from the recorded fill and fires
T4. The claim "the two rows together covering `[R-SER-08]`" holds.

T13/T15/T16/T23 are *cause* rows that say so explicitly ("the check that
detects it is T25's, and this row records the cause rather than a procedure
of its own"). I checked each cause is genuinely detectable through the named
check. Deflate with a carried-over history window: back-references reach
before output position 0, which every RFC 1951 decoder rejects → T25 ✓. LZ4
match offset past produced output → T25 ✓. A second DEFLATE stream after
BFINAL → bytes remain → T24 ✓. LZ4 frame magic parsed as a block → T25 ✓.
And T13 correctly *omits* the undetectable member of `[R-COD-02]`'s
condition — a zstd frame using an undisclosed dictionary — which §21.7's
first paragraph accounts for instead. That is a careful piece of drafting.

### 2.4 §21.5 — ignored records

R1←`[R-CNT-25]`/`[R-MTA-03]`; R2←`[R-CNT-20]`; R3←`[R-CNT-25]`;
R4←`[R-MTA-09]`; R5/R6←`[R-CNT-25]` via `[R-MTA-04]`/`[R-ENC-11]`/
`[R-ENC-12]`; R7–R10←`[R-MTA-04]`.

The unassigned-encoding logic is the delicate part and the preamble handles
it well: `[R-MTA-10]` withdraws the *document's content rules* under any
unassigned encoding (0, reserved 3–0x7F, experimental ≥0x80), while
`[R-MTA-03]`'s value set still makes 0 and the reserved range invalid. The
preamble states exactly that:

> Encoding 0 and a reserved-range value are unassigned too, and R1 registers
> both as violations: what `[R-MTA-10]` withdraws is the document's content
> rules, never the encoding byte's own value set (`[R-MTA-03]`).

R2 correctly carries no encoding qualifier, because `[R-MTA-10]` lists "the
extent's terminal CRC (`[R-CNT-20]`)" among the structural checks that
survive at an unassigned encoding. R4 is correctly restricted to encoding 2.
R5–R10 presuppose a *decoded* document and so cannot reach an unassigned
encoding.

The one cell that does not survive this is R3's parenthetical — see
**register-02**.

---

## 3. Completeness, both directions

### 3.1 Register → rules (no row without a rule)

Every one of the 121 rows names a governing requirement that exists, and I
found no row whose condition the cited rule does not make a violation. The
closest calls, and why they stand:

- **F19** — verified above.
- **T13** — verified above.
- **T2/T4/T5/T26** — verifier rows whose governing rules
  (`[R-SER-08]`, `[R-SER-05]`, `[R-COD-10]`) each expressly assign
  "a validity error at tile scope" to a verifier. ✓
- **F27/L48** — `[R-MTA-05]` says "the file is nonconforming, a verifier
  MUST report it, and readers process the document unchanged". That is a
  violation with a verifier detector and no reader obligation, exactly as
  the rows say. §21.6's closing paragraph confirms the migration
  deliberately. ✓
- **F28/L49** — `[R-CNT-22]` likewise. ✓

### 3.2 Rules → register (no violation without a row)

I extracted every `Writer(s) MUST / MUST NOT` in §§1–20 (26 distinct
passages) and every `a reader MUST treat … as a validity error`, and walked
each to a row:

`[R-ENC-02]`→F1; `[R-ENC-03]`→F2/L1/T11; `[R-ENC-04]`→F3/L2/T12;
`[R-ENC-06]`→§21.7 (no row, accounted); `[R-ENC-11]`→L3/L4/R5;
`[R-ENC-12]`→L5–L8/R6/R10; `[R-ENC-15]`→F4/L9; `[R-CNT-04]`→F6;
`[R-CNT-05]`→F7; `[R-CNT-06]`→F8–F17; `[R-CNT-07]`→F18; `[R-CNT-08]`→F19;
`[R-CNT-11]`→F20; `[R-CNT-12]`→F24/F25/F26/F29/L13/L14/L46/L47;
`[R-CNT-13]`→F30–F33/L15–L18; `[R-CNT-14]`→F34/L19;
`[R-CNT-15]`→F35/F36/L24/L25; `[R-CNT-16]`→L20; `[R-CNT-17]`→L21/L22;
`[R-CNT-18]`→L14/L23/L24/L26 (+ nesting → §21.7); `[R-CNT-20]`→F14/F20/
L37/L38/T1/R2; `[R-CNT-22]`→F28/L49; `[R-CNT-23]`→L27–L31/L34–L36/L39/L43/
L45; `[R-CNT-25]`→F21/F22/R1–R7; `[R-CNT-27]`→F5; `[R-GEO-01]`→L32;
`[R-GEO-05]`→L33; `[R-GEO-06]`/`[R-SER-01]`→§21.7; `[R-IDX-01]`→L22 +
§21.7; `[R-IDX-02]`→T6/T7; `[R-IDX-03]`→T6–T12; `[R-IDX-04]`→L37/L38;
`[R-IDX-05]`→L38; `[R-SLB-01]`→L39/L40; `[R-SLB-03]`→L41/L42;
`[R-SLB-04]`→no row, §16.2's Note says so and the detection *is*
`[R-SLB-03]`'s ✓; `[R-TYP-03]`→L34; `[R-TYP-06]`→L30; `[R-TYP-07]`→L35;
`[R-SER-02]`→T3; `[R-SER-03]`→T5; `[R-SER-05]`→T4/T5; `[R-SER-06]`→L36;
`[R-SER-07]`→T3; `[R-SER-08]`→T2 (+T4); `[R-COD-02]`→T13; `[R-COD-03]`→L43;
`[R-COD-04]`→T14; `[R-COD-05]`→T15/T16; `[R-COD-06]`→T17–T22 (+§21.7 for
the undisclosed dictionary); `[R-COD-07]`→L44; `[R-COD-08]`→T24/T25;
`[R-COD-09]`→L45; `[R-COD-10]`→T26; `[R-MTA-03]`→F23/L12/R1;
`[R-MTA-04]`→R5–R10; `[R-MTA-05]`→F27/L48; `[R-MTA-09]`→R4;
`[R-MTA-06]`/`[R-MTA-07]`/`[R-MTA-10]`→§21.6 (non-violations).

SHOULDs correctly carry no rows (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`,
`[R-ENC-14]`, `[R-TYP-10]`, `[R-LIF-07]`, `[R-MTA-04]`'s
number-exactness advice) — §2.4 `[R-CNF-12]` says "§21's register
enumerates MUST-level conditions only".

I probed a dozen specific shapes for gaps and found none:

- directory region overlapping a tile extent → F33 (its "directory region"
  instance) ✓
- a layer's stored tile overlapping the *same* layer's sub-record extent →
  L18 ✓ (§7.2's "including a stored extent overlapping its own layer's
  index region or sub-record extents")
- two sub-record extents of *different* layers → F33 ✓
- a prior generation's trailer as a claimant → it is slack, not a claimant ✓
- a partial all-sentinel segment carrying the 0xEECB3BB2 constant instead of
  a computed CRC (`[R-IDX-05]`'s "a partial segment's CRC MUST be
  computed") → L38, whose cell says exactly that ✓
- a compressed directory (§7.1's "the directory is always raw") → F20 or
  F29 ✓, no separate row needed
- a bool fill byte in a *planar* layer → L35 ✓ (the rule is per channel, not
  per layout)
- extent_length ≥ 5 on user metadata → F22 / L11 ✓

**I found no detectable file-conformance violation the register omits, and
no row registering a non-violation.** That is a real result and I am
reasonably confident in it.

### 3.3 §21.6's own scope

§21.1 says the completeness clause does not reach §21.6, so I did not treat
§21.6 omissions as defects — which matters, because `[R-CNF-02]` names two
expressly-declared writer-conduct exemptions (a set ignore-lane bit; a
pre-trailer gap longer than `[R-LIF-02]` step 5's pad) and only the first
has a §21.6 entry. Under §21.1's exclusion that is not a defect. I checked
every §21.6 entry against its cited rules and all thirteen restate them
correctly, including the `[R-WRT-08]` citation for "preserved or dropped per
its PE bit" — §20.4's MU/PE table sits inside `[R-WRT-08]`'s requirement
text, not `[R-WRT-05]`'s.

---

## 4. Every cross-reference to a row

I grepped the whole document for the label patterns and audited all 22
occurrences outside the register tables, plus the intra-table citation in
F33. Every one resolves to a row that says what the citing text claims:

| Where | Cites | Verdict |
|---|---|---|
| §5.2 `[R-CNT-21]` | L18's overlap, L40–L42's placement | ✓ L18 is intra-layer overlap; L40/L41/L42 are alignment/slab placement, all verifier/reject-layer |
| §9.6 `[R-LIF-06]` | §21.2 rows F8 and F17 | ✓ both are trailer gates on the bytes handed over |
| §17.2 Note | §21.4, T24 | ✓ T24 is the trailing-bytes row |
| §20.3 step 4 | L44 | ✓ L44 is the lz4 decoded-size cap |
| §21.1 | F1 of F6 and of F8; F35 of F36; L24 of L25 | ✓ each is a strict specialization with the same detector/tier |
| §21.1 | T24's *any codec* | ✓ that is literally T24's cell |
| §21.1 | T15, T25 | ✓ both enumerate materially different shapes |
| §21.1 | F27 and L48 | ✓ the two `[R-MTA-05]` rows |
| §21.2 preamble | F8, F1, F14, F6 | ✓ four rows, verified above |
| §21.2 F33 | F9/F10, F31/F32, L16/L17, T8/T9 | ✓ the bounds rows at each tier, directory / non-layer record / layer record & sub-record / index entry |
| §21.6 | F36, L25 | ✓ reserved-range emission, verifier |
| §21.6 closing | F18; F35, F36, L24, L25 | ✓ |
| §21.7 | T2, T4, T5 | ✓ the three §14-content rows |
| App. H | F1, F6 | ✓ front block |
| App. H | F7 | ✓ structure in the pre-trailer gap |
| App. H | F36, L25 | ✓ |
| App. H | R1 | ✓ encoding 0 and reserved stay violations |

**No citation points at the wrong row.** The only near-miss is §9.6 naming
F8 and F17 where §9.5's parallel Note names three gates (magic, CRC,
committed_file_length = F8, F14, F17); the §9.6 parenthetical is a subset,
not a mis-citation, and I did not file it.

---

## 5. Limits, both directions

### 5.1 §21.9's minimum guarantees against the rest

| §21.9 | corroborating text |
|---|---|
| rank 32 | ≤ hard cap 255 (§7.4 `u8`) ✓ |
| C 4096 | ≤ hard cap 65,535 (§7.4 `u16`) ✓ |
| entry_count 2³² | ≤ 2⁶³−1 ✓; §1 calls it "§21.9's tile-count guarantee" ✓ |
| 65,536 layers | note's 12.5 MiB ≈ 65,536 × 200 B ✓, inside the 16 MiB directory row ✓ |
| dir_length 16 MiB | §19.1/`[R-CNT-11]` fetch-and-CRC-whole ✓ |
| decoded tile 256 MiB | ≤ lz4 cap 0x7E000000 ✓; §11.3's "1 to 16 MiB" ordinary range is an order of magnitude below ✓ |
| metadata document 16 MiB | `[R-MTA-09]` "no smaller than §21.9's user-metadata guarantee"; §18.2's Note names 16 MiB ✓ |
| zstd Window_Size 8 MiB | `[R-COD-06]` "Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size` guarantee" ✓ |

Appendix B's "Reader minimum guarantees" row restates all eight identically.

Arithmetic in §21.9's note checks out: at entry_count = 2³² the segment-CRC
array is ⌈2³²/2¹⁶⌉ × 4 = 2¹⁶ × 4 = 256 KiB ✓; at 2³⁶ it is 2²⁰ × 4 = 4 MiB ✓.

### 5.2 Hard limits

`[R-ERR-05]` names: name ≤255 B; metadata key ≤255 B; rank ≤255; C ≤65,535;
lz4 decoded ≤0x7E000000; every offset/length/extent/count ≤2⁶³−1; A a power
of two 512…2⁶²; A_slab a power of two 1…2⁶²; S in 1…2⁶³−1; dir_offset ≥16
and dir_length ≥4; file ≥128 bytes. **Each matches its defining section
exactly** (§4.6, §18.2, §7.4, §17.2, §4.2, §16.1, §16.2, §6.2, §5.1). I
checked the two the paragraph singles out as chosen rather than forced — the
512 floor on A (§16.1) and the 255-byte key cap (§18.2 folding §4.6 onto
keys, which carry no prefix) — and both are as described.

The one limit stated elsewhere and absent here is the user-metadata
`extent_length ≥ 5` (§7.1; Appendix B lists it). §21.9 disclaims inventory
explicitly — "The hard limits it restates are a finding aid rather than an
inventory" — so this is not a defect, and `[R-VEC-03]`'s "every hard limit
of `[R-ERR-05]`" reads over the named list.

**No limit is claimed here that its defining section states differently.**

---

## 6. Building things

### 6.1 Constants

I implemented CRC-32C from §4.5's parameters (Castagnoli 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and reproduced
every constant the document states:

```
CRC-32C("123456789")            = 0xE3069283   ✓ §4.5 check vector
CRC-32C(zero bytes)             = 0x00000000   ✓
CRC-32C(4 sentinel entries, 80B)= 0x80A34955   ✓ §7.4 example, LE 55 49 A3 80
CRC-32C(55 49 A3 80)            = 0xC4EE982E   ✓ §7.4 crc_of_crc_array
CRC-32C(2^16 sentinel entries)  = 0xEECB3BB2   ✓ §15.4 / Appendix B
```

### 6.2 Appendix A's minimal file

I assembled trailer bytes [0, 60) from §6.2's layout with the appendix's
values (major 1, minor 0, flags 0, generation 1, dir_offset 16, dir_length
4, committed_file_length 128, file_id 0x0123456789ABCDEF, reserved 0):

```
8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
ef cd ab 89 67 45 23 01 00 00 00 00
```

CRC-32C = **0xE00938D2**, stored LE `D2 38 09 E0` — byte for byte what the
hex dump at offset 0x7C shows. ✓

### 6.3 §7.4's layer-record payload

Laid the fields out by hand: name 4 (0–3), the nine scalars 34 (4–37),
dimension entry 18 (38–55), channel entry 12 (56–67), trailing fixed fields
13 (68–80) = **81 bytes**, matching every annotated offset in the example
and its "4 + 34 … 18 … 12 … 13 — 81 exactly". Extent length
4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84** ✓ matches `[R-CNT-17]`.

### 6.4 §15.4's segment example

entry_count 1,000,000 → 15 full segments + 16,960 ✓; array 64 B ✓; region
20,000,064 B ✓; tile 999,999 in segment 15 at segment-relative byte
20 × 16,959 = 339,180 ✓; array at [20,000,000, 20,000,064) ✓; segment 15 at
[19,660,800, 20,000,000) = 339,200 B ≈ "~339 KB" ✓; one full segment =
65,536 × 20 = 1,310,720 = "1.25 MiB" ✓.

Planar example: channel 2 at s = 10 → disk ordinal 2·32 + 10 = 74 ✓; entry
at [1,480, 1,500) ✓; channel 3's block = entries [96, 128) ✓.

### 6.5 §11.4, §14.2, §14.3, §14.5, §17.3 examples

All reproduce: (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal
11,452 ✓. Interleaved (2,3) with uint8+uint16: Q = 3, size 18, ordinal 5 at
[15,18) ✓; planar `b` 12 bytes, ordinal 5 at 10–11 ✓; float32+bool: Q = 5,
size 30, [25,30) ✓. Packed bool P = 10 alternating: `55 01`, fill-true
`55 FD` ✓. Padding example: 2×2 grid, edge tile 1 real + 15 padding, 32
bytes ✓. Byte-shuffle of 1.0/2.0/3.0: `00 00 00 00 00 00 80 00 40 3F 40 40`
✓.

**Everything the document computes, it computes correctly.** That is worth
saying plainly.

### 6.6 The commit I built to test §21.7

This is where I found something. I built a concrete two-generation file:

*Generation n.* One layer, name `a`, layout 1 (interleaved), linearization 1,
codec 1 (none), filter 1 (none), A = 0, S = 0, A_slab = 0, rank 1,
C = 1, dimension `x` with E = 8 and T = 4, channel `c` type 6 (uint8) with
fill `00`, index_encoding 1.

Grid count ⌈8/4⌉ = 2, so N = 2, entry_count = 2, P = ∏Tᵢ = 4, Q = ΣBᵢ = 1,
decoded size = P·Q = **4 bytes**. Both tiles stored, each a 4-byte extent
under codec 1 (`[R-COD-04]` forces length = decoded size = 4). G·T = 8 = E,
so there are **no padding positions**; the channel is numeric, so there are
**no pad bits and no boolean bytes**.

*Generation n+1.* The commit changes the tile extent T from 4 to 8 and
leaves E at 8. New grid ⌈8/8⌉ = 1, entry_count 1, P = 8, decoded size
P·Q = **8 bytes**. Tile 0 keeps disk ordinal 0, and §20.3 step 4 obliges
"every other entry byte-identical at its disk-ordinal position", so its
entry still declares length 4.

This commit is squarely barred by §20.3 step 4: it alters, for a tile the
layer stored in the generation this commit supersedes, "the decoded size".
And the resulting file **does** carry a witness — T14, "Codec 1 (none)
declared and a non-sentinel index entry's length differs from the tile's
decoded size" — with no §14-constrained content byte anywhere in the layer.
The same construction with codec 2→3 instead of a geometry change is
witnessed by T17 (missing zstd magic); with a compressing codec it is
witnessed by T3.

§21.7 says the opposite. That is **register-01**.

---

## 7. Findings

### register-01 — CONTRADICTION

**Location.** §21.7, `[R-ERR-01]`; against §21.4 rows T3 and T14 and §20.3
step 4's own list (`[R-WRT-04]`).

**Quotation** (§21.7):

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else;

**Against** (§20.3 step 4, `[R-WRT-04]`):

> A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores **in the generation this commit supersedes**,
> what §14 fixes for its stored bytes or how they decode — the set of
> padding positions (§11.3) and the content `[R-SER-05]` fixes there, the
> decoded size, the byte offset of any sample within the decoded tile image,
> or the codec and filter that produced the stored bytes.

**and** (§21.4, T14):

> Codec 1 (none) declared and a non-sentinel index entry's length differs
> from the tile's decoded size

**Detail.** §20.3 step 4 bars alteration of four things: the padding-position
set and its content, the decoded size, sample byte offsets, and the codec
and filter. Only the first is a "byte §14 structurally constrains". A change
to the **decoded size** is witnessed by T3 (or, under codec 1, by T14 before
any payload fetch), and a change to the **codec** is witnessed by T17, T24
or T25 — none of which constrains a §14 content byte, and all of which fire
in a layer with no padding position, no pad bit and no boolean channel. My
§6.6 construction is such a layer: one uint8 channel, E = 8, T changed 4→8,
tile 0 still stored, T14 fires. So "the §21.4 rows firing there and nowhere
else" is false: they fire elsewhere too.

I tested the charitable re-reading, that "witnessed" means "witnessed *as a
declaration change* rather than as a bad file". It does not rescue the
sentence: T4 does not witness a change either — a freshly created file can
carry a padding position with the wrong content just as easily as an edited
one — so under that reading the claim is wrong in the other direction and
nothing witnesses the bar at all.

**Which governs.** §21.1 says "where a row and the rule it cites diverge,
the rule governs", and separately that §21.7 is "the account, by class, of
what fails" the detectability gate. Here the rows are right and §21.7's
account of them is wrong: T3 and T14 stand, and a verifier checks them
whatever §21.7 says.

**What an implementer does wrong without it.** A verifier author reading
§21.7 as the inventory of what a declaration-change violation can look like
would conclude that only the §14-content rows are relevant and could
under-report the class in diagnostics. It does not change any accept/reject
verdict, because T3 and T14 are independently obligatory reader checks.

**Byte-level: no.** T3 and T14 are registered rows with detector *reader*
and detection point *tile use*; every conforming reader checks them
regardless of §21.7's prose. Two implementations built from this text emit
the same bytes and reach the same verdict on every file. The defect is in
the register's account of itself, not in the register.

---

### register-02 — AMBIGUITY

**Location.** §21.5, row R3's Condition cell.

**Quotation:**

> A user-metadata document's stored bytes fail to decode under its declared
> assigned encoding — under an unassigned one this specification defines no
> decoding, and §21.6 governs (`[R-MTA-10]`)

**Permitted readings.**

*(a)* "§21.6 governs" the conformance of any record under an unassigned
encoding. §21.6's only relevant entry is "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the
file is conforming". Read this way, a record declaring encoding 0 or a
reserved value 3–0x7F — also unassigned — would be a defined non-violation
and a verifier would certify past it.

*(b)* "§21.6 governs" only the *absence of a decode obligation*, and R3
simply does not reach unassigned encodings; what governs the record's
conformance there is R1.

**Which I picked and why.** (b). Reading (a) is refuted three ways within the
document. §21.5's own preamble, four lines above the table, says "Encoding 0
and a reserved-range value are unassigned too, and R1 registers both as
violations: what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set (`[R-MTA-03]`)". R1's cell registers
"a document encoding of 0, or a reserved-range value (3-0x7F)". And
Appendix H's verifier checklist says "encoding 0 and the reserved range stay
violations (R1)". §21.1's rule — "where a row and the rule it cites diverge,
the rule governs" — settles it: `[R-MTA-03]` makes 0 invalid and
`[R-MTA-10]` withdraws only content rules, so R1 stands.

**What an implementer does wrong without it.** A verifier author who reads
only R3's cell and follows the pointer to §21.6 finds an entry that says
"the file is conforming" and certifies a file carrying encoding 0. The
correct verdict is *nonconforming*.

**Byte-level: no.** This is exactly the pattern the brief names as the
dominant over-claim: a register cell that contradicts the rules it cites,
where §21.1 has already decided which governs. R1 is in the same table,
the preamble corrects the cell explicitly, and `[R-MTA-03]` says "0 is
invalid" flatly. Two competent implementations do not diverge; only the
parenthetical is wrong.

---

### register-03 — AMBIGUITY

**Location.** §21.1's instance criterion; §21.4 row T18 and §21.5 row R4.

**Quotation** (§21.1):

> What a cell enumerates is the condition's own alternatives and containers:
> a row whose check ranges over a family without the condition changing
> shape states that range as a single instance (T24's *any codec*), and one
> whose members give the condition materially different shapes enumerates
> them (T15, T25).

**Against** — T18's Instances cell:

> a second concatenated compressed frame; a skippable frame before the
> frame; a skippable frame after the frame; a skippable frame between two
> frames

**and** R4's, for the same RFC 8878 constraint:

> … a skippable frame, top-level extent; a skippable frame, layer sub-record
> extent; a second frame, top-level extent; a second frame, layer sub-record
> extent …

**Detail.** Both rows enumerate the same underlying prohibition. `[R-COD-06]`
states it for tiles as "contains a skippable frame **anywhere** or more than
one frame"; §18.2 carries it to documents as "no skippable frame and no
second frame". T18 splits the skippable case three ways by position; R4
states it once per container. The criterion cannot license both: the
position of a skippable frame does not change the shape of the check ("does
the extent hold more than the single compressed frame"), which by §21.1's
own T24 precedent — an *anywhere* being a family — makes it one instance;
and if position *does* give materially different shapes, then R4 is short
two per container. Either way the criterion yields 273 or 279, not 275.

**Permitted readings.** *(a)* Follow the criterion: T18 should read 2 and
the register holds 273 instances. *(b)* Follow the cells as literally
written, since §21.1 also says "the count is therefore mechanical once the
cell is written" — 275, and the criterion under-determines the cells.

**Which I picked and why.** (b), because that sentence is unconditional and
because §21.8's stated total (275) reproduces from the cells exactly. But
the criterion then does not do the work §21.1 assigns it: two cells applying
it to one rule disagree, so a corpus author who derives instances from the
criterion rather than transcribing the cells builds a different corpus.

**What an implementer does wrong without it.** A corpus author following
§21.1's stated criterion builds two fewer zstd-tile vectors than §21.8
promises, or four more metadata vectors — and `[R-ERR-02]` makes "a row
without a vector … a gap in the corpus".

**Byte-level: no.** This decides how many test files exist, not which byte
sequences a reader accepts. Every file either holds one compressed frame in
the extent or does not, and both readings reject exactly the same set.

---

### register-04 — AMBIGUITY

**Location.** §20.3 step 4, `[R-WRT-04]`.

**Quotation** (the general bar and its tense gloss):

> The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so a commit does not escape this by unstoring in the same
> breath: superseding every tile of a layer and re-declaring it are one
> operation, and this bars it.

**Against** (the shrink paragraph, two paragraphs later in the same step):

> but where it drops a tile out of the addressed set entirely (§11.2's grid
> count falls), nothing is altered for a tile the new state stores, and the
> commit is permitted

**Detail.** The general bar quantifies over tiles stored **in the superseded
generation**; the shrink paragraph justifies its permission with a
quantifier over tiles **the new state stores**. Take a layer with one
addressed tile, stored, codec 1. Two commits produce the same live bytes:

- (i) supersede the tile with a sentinel and re-declare the codec — the
  tense gloss bars this expressly;
- (ii) shrink the extent to 0 so the tile is de-addressed, and re-declare
  the codec — under the shrink paragraph's stated criterion "nothing is
  altered for a tile the new state stores", so permitted; under the general
  bar's prior-generation quantifier, the codec change alters "the codec and
  filter that produced the stored bytes" of a tile the superseded generation
  stored, so barred.

**Permitted readings.** *(a)* The shrink paragraph's criterion is general,
and the new-state tense governs shrinks; case (ii) is permitted, and the
tense gloss reaches only sentinel-superseding. *(b)* The tense gloss is
general and the shrink paragraph's permission is scoped to a commit whose
*only* change is the shrink; case (ii) is barred.

**Which I picked and why.** (b). The tense sentence is explicit and
emphatic ("The tense is the prior generation's"), and §20.3's neighbouring
permission — "A layer that stores no tile MAY be re-declared freely" — must
be read in the same tense or it swallows the bar entirely. §11.1's
Rationale, which I checked as a possible third voice, turns out to restate
the *shrink* paragraph faithfully and scoped ("a shrink is barred wherever
it alters what §14 fixes for a tile the new state still stores"), so it does
not settle the general question either way.

**What an implementer does wrong without it.** An appender author reading
(a) emits a commit that shrinks a layer to zero addressed tiles while
changing its codec, believing it conforming conduct. Under (b) that commit
is barred.

**Byte-level: no.** §21.7 already establishes that the bar is unwitnessed
wherever the affected tiles are not stored in the new state, so both files
are conforming byte sequences and every reader and verifier accepts both.
The divergence is in writer conduct only.

---

### register-05 — OBSERVATION

**Location.** §20.5, `[R-WRT-06]`.

**Quotation:**

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
> fails, and MUST NOT emit a file carrying a violation it has detected: it
> can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it
> and call the output clean — and a record §20.4 does let it drop is no
> exception, dropping being available only where that table licenses it —
> nor re-emit it corrected (`[R-WRT-05]`).

**Detail.** The trailing clause "nor re-emit it corrected (`[R-WRT-05]`)"
repeats the first clause "it can neither re-emit the structure corrected
(`[R-WRT-05]`)" verbatim, same requirement citation and all. A reader
meeting a three-branch "neither … nor … nor" reasonably assumes three
distinct prohibitions and spends effort looking for the difference between
"re-emit the structure corrected" and "re-emit it corrected" — there is
none; the antecedent of "it" in both is the structure carrying the detected
violation. The cost is a reader's time, not a wrong implementation, which is
why I file it as an observation rather than an ambiguity: the question is
decidable, and the answer is that the third branch adds nothing.

**Byte-level: no.** The prohibition is stated once or twice with identical
force; a compactor's behavior is the same either way.

---

## 8. What I could not determine

Nothing material. Two places I worked at and resolved rather than filed:

- **L23's tier.** Whether a layer record whose name field overruns
  inline_length is due at open (because §19.1 step 4 relies on the name
  there) or at layer access (as L23 says). Resolved in favour of the
  register: §19.1 says such a record "contributes no name to the namespace",
  so the open completes without the error and the framing check belongs to
  layer access. This also preserves `[R-RDR-01]`'s two-request open.
- **T14 as an unnamed specialization of T3.** Under codec 1 the stored bytes
  are the filtered image verbatim and the filter is length-preserving, so a
  stored length differing from the decoded size implies a decoded payload
  length differing from it: T14 ⊂ T3 strictly. §21.1's specialization list
  ("F1 of F6 and of F8, F35 of F36, L24 of L25") does not name it. I did not
  file this, because the list is hedged ("Some rows are strict
  specializations of others"), because both rows carry the same detector,
  tier and outcome so §21.1's consequence clause ("whose detector and
  detection point are the ones that apply") is vacuous here, and because
  `[R-VEC-02]` already handles a vector exercising two rows.

## 9. Transcript finding count

**5** findings: register-01 … register-05.
