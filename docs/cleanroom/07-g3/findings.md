# Cleanroom round 7 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**G3's byte-level criterion is met — zero byte-level ambiguities, for
the first time in seven rounds.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 63 — reader 8, writer 11, verifier 11, diagrams 9, register 12, adversary 12 |
| Flagged byte-level by their reporter | 8 |
| Distinct defects after three-way dedup | **44** (all three passes independently reached 44) |
| **Byte-level, after triage** | **0 — unanimous across all three passes** |
| Consensus status | 25 CONFIRMED · 17 PARTIAL · 2 REFUTED |
| Severity | 32 editorial · 8 register bookkeeping · 2 figure · 2 none |

The gate is not yet *closed*: ADR-0034 also requires zero findings left
without a disposition, and the 44 are undispositioned. What is settled
is the criterion that has failed six times running.

## The trend, stated plainly

| Round | Byte-level defects | Quiz |
|---|---|---|
| 3 | 4 | — |
| 4 | 4 | — |
| 5 | 3 | — |
| 6 | 5 | 14 / 1 diverge |
| **7** | **0** | **15 / 0 / 0** |

Two numbers moved together, and the second is the one worth trusting.
Reporters self-flagged 33 findings byte-level in round 6 and 5 survived;
this round they flagged 8 and none survived. Fifteen pointed byte-level
questions, authored by one agent, answered cold by a second and keyed
independently by a third, produced no divergence and — the stronger
signal — **no question either agent judged underdetermined.** Round 6
scored 14/1. The pilot round scored 15/15 on a document a tenth this
size.

## What the round caught that mattered

**§20.4's table now forbids every append — and I introduced it one commit
before the round ran.** ADR-0061's propagation replaced the table's
header. The old header scoped the whole table to *"record types the
updater does not implement"*; the replacement opens *"Persistence governs
every record type"*, and §7.3 fixes the layer record at MU = 1. The MU = 1
row reads *"Retain byte-identical. The updater MUST NOT modify the scope
the record governs"* — which, applied to a layer record, forbids every
append §20.3 defines. The writer walk hit it while tracing an append and
two triage passes confirmed it independently.

It is not byte-level: the cell's own gloss (*"an unknown critical record
at layer scope"*), `[R-CNF-06]`'s scoping to records an updater does not
understand, and Appendix H all recover the intended reading, and the
restrictive reading yields an updater that refuses to act rather than one
that emits different bytes. But it is a self-inflicted contradiction in
text that had existed for exactly one commit, and it is the clearest
argument this round could have made for running a cleanroom pass after
every substantive edit rather than every several.

**A violation the register does not carry.** `[R-MTA-07]` states that a
file carrying a standardized key outside its listed scope *"is
nonconforming, and a verifier detects it"* — and no row of §21.2–§21.5
registers the condition. Verified directly: the phrase *"standardized
key"* occurs in §18.4 and nowhere in §21. §21.1 makes register
completeness normative, so the omission is a defect by the document's own
terms.

This one is not bookkeeping, despite where triage filed it. The register
is partitioned by *reader* outcome, and this condition has none — a
reader ignores the key either way, so `[R-CNF-07]`'s four-value
vocabulary has no value that fits. §21.7 does not fit either, since that
is the inventory of what *no check* detects and a verifier detects this.
The condition is real, detectable, and unfileable under the present
taxonomy. It also moves G5's denominator: the register is 125 conditions
and should be 126, with a vector owed.

**A live structure no checksum covers.** §5.2 defines a structure to
include *"a record extent … whatever the record's type"*, §21.6 registers
an experimental-range MU = 0 record as conforming, and §7.2 lets it carry
an extent — but §8.1's checksum map has rows for only two record extents.
So a conforming file can carry a live-state structure covered by no
checksum, and §9.7's *"each verifies against the checksum covering it"*
is vacuous for it. §22.3 says two residues are stated rather than
defended; this is a third it does not name.

**§21.7 calls itself an inventory it is not.** It names five requirements
that fail the detectability gate and omits every §20 updater and
compactor obligation, `[R-CNT-08]`'s copy-forward, `[R-IDX-01]`'s
disk-ordinal entry order, and `[R-PRV-01]` — all MUST-level, all without
a single-file witness, all of exactly the kind already listed.

## The eight byte-level claims, and why none survived

Each was re-judged by three passes and the two strongest were then
checked by hand against the text.

- **The register-versus-§19 fork** (a top-level user-metadata record with
  extent slot (0, 0): reject-file under §21.2's F24, servable under
  §19.1's enumerated open). Refuted by `[R-CNF-04]`, quoted from the
  document: *"A reader MUST detect the violations enumerated in the error
  register (§21) and apply the outcome class this specification assigns
  to each."* One permitted reading, so no fork. §19's under-enumeration
  is a real defect for implementers and stays on the list as editorial.
- **The lz4 cap on a layer with zero addressed tiles.** Refuted by the
  rule's own quantifier — `[R-COD-07]` binds *"a layer any of whose
  addressed tiles' decoded size exceeds 0x7E000000"* — and by §21.6's row
  affirming a zero-extent dimension as *"A valid, empty layer: zero
  addressed tiles"*. The empty quantification is vacuously satisfied and
  the layer is conforming; a rejecting verifier is the nonconforming
  party. The reporter's offered second instance refutes itself, since
  `[R-ENC-04]` carries no addressed-tile quantifier at all.
- The remaining six reduced the same way: the rule states the verdict, so
  both implementations reach it.

The over-claim ratio fell from 33:5 to 8:0, which is the reporters
calibrating, not the document changing underneath them.

## Two honest caveats

**The triage passes were anchored.** All three were told round 6's
calibration — 33 flagged, 5 survived — which biases toward downgrading. I
mitigated it by verifying the strongest candidates against the text
myself rather than accepting the verdicts: `[R-CNF-04]`, `[R-COD-07]`
with §21.6's row, and `[R-MTA-07]`'s absence from §21 were each read
directly, and all three held. A reader who wants to discount this round
should discount it here first.

**One triage pass overstated its own coverage.** The skeptic pass wrote
*"All 63 input findings appear in exactly one judgement, and none was
dropped"* and then itemised a tally summing to 63 — while actually citing
62 unique ids. It dropped `register:RD-09`, which the other two passes
both graded CONFIRMED and not byte-level. The verdict does not move, but
the self-report was false, and it is the second round running in which a
triage-stage agent's coverage claim did not survive checking. The
mechanical union-find over all three passes' groupings is what caught it;
no agent did.

One disclosed deviation, recorded because it strengthens rather than
weakens the round: the verifier walk ran local CRC-32C computations in
Python, reading no files, and independently reproduced all four constants
the document states — `E3069283`, `00000000`, `EECB3BB2`, and Appendix
A's trailer CRC `E00938D2`. The reader walk separately recounted §21 by
hand and got 39 + 50 + 26 + 10 = 125 conditions over 242 named instances,
matching §21.8 exactly.

## Disposition

**One of the 44 is fixed: `wrt08-mu1-row-forbids-layer-edit`.** The
table's scope is restored to the types it was always about. Its header
now keeps ADR-0061's decision — persistence governs every record type,
the registry's flags are authoritative for a registered one, and
implementing a type confers understanding rather than permission to drop
it — and then hands the table itself to *"a type the updater does not
implement,"* for which §7.3 already says the stored flags are
authoritative. That restores agreement with the column header the table
carries (**Stored flags**) and with the MU = 1 cell's own gloss, *"an
unknown critical record at layer scope."* A layer record is implemented
and registered, so it never reaches the row that would have barred
modifying it, and §20.3's append is permitted again. ADR-0061 is
unchanged: the decision was right, only its propagation was not.

**A second is resolved by deletion: `mta07-standardized-key-no-register-row`**
(ADR-0063). The finding was right that §21 omits a violation the document
names, and the repair is not the one the finding implies. §18.4's own
Note explains that material lives in metadata *"rather than as a
structural record whose staleness would need rules, verifier
obligations, and an updater's attention"* — so attaching a verifier
obligation to a metadata key works against the reason the material is
there. §21.6 already blessed an unrecognized `tarn.`-prefixed key as
conforming, which made the specification's knowing *more* about a key
the thing that made a file worse. Placement and value shape are now
writer guidance; the register is unchanged at 125 conditions over 242
named instances, and no vector is owed. Registering it instead would
have cost 2 conditions, 4 instances and 4 vectors to detect a condition
no reader can observe.

**The tail: 37 edits landed, 14 were refused.** Six section owners drafted
51 exact anchor/replacement pairs across the remaining 39 defects; an
adversarial reviewer per group checked each anchor mechanically and each
replacement for normative drift. Thirty-seven applied with zero anchor
misses. **Fourteen were rejected, every one for normative drift** — a
verifier-decline-to-verdict mapping the document never makes, a flat
`MUST` converted into a default with an opt-out, a reader obligation
inserted into a declarative sentence that carries none, a Class column
added to a table §7.4 makes normative. That boundary is the round's
second useful result: the instruction was *if this would change what a
file may contain or what a reader must reject, stop*, and it held
fourteen times.

Counting by defect: **24 cleared outright**, 2 partly cleared with the
rest escalated, 4 judged to need no change with reasons recorded, 2
unanimously refuted at triage. **Thirteen now want a maintainer
decision** — 7 escalated by their drafter, 6 more where the reviewer
refused the only drafted repair as normative.

### The register grew, and the growth exposed a measurement gap

`instance-arithmetic-applied-inconsistently` was confirmed by all three
passes: §21.1 states the instance arithmetic multiplicatively — *"a
condition applying to two alternatives in two containers has four"* —
and five cells did not follow it. Repairing them moves the register from
**242 to 252 instances** (L1 +2, L16 +2, R4 +2, R5 +6, L2 −2). The
condition count is unchanged at 125; no row was added or removed. §21.8
now reads 252 and the mechanical recount agrees.

That exposed something larger. §21.8's `[R-ERR-02]` requires *"one vector
per instance"*, but `COV-03` computes **row** coverage — its docstring
claims instances while its code counts `covered_rows` — and the corpus
manifest has no instance field at all: a violation entry carries `row`,
`rule`, `outcome`, `scope`, `detector`, `detected`, and nothing naming
which instance the vector exercises. So G5's reported 125/125 at 100% is
a true statement about rows and was never a measurement of the criterion
`[R-ERR-02]` actually states.

Comparing vector counts to instance counts per row — a lower bound,
since several vectors on one row may all exercise the same instance —
gives a shortfall of **16 across 8 rows**: L1 −2, L2 −1, L16 −2, R4 −2,
R5 −6 from this repair, and F3 −1, F32 −1, L50 −1 that predate it and
were hidden by row-level counting. The four pre-existing ones are the
sharper finding: they were there before round 7 touched anything.

Closing this needs a manifest field and a real instance-coverage check,
which is an ADR-0054 revisit and a maintainer decision, so no vectors
were generated here. They are not the same shape as earlier
rounds' findings: rounds 4 and 5 found propagation failures, round 6
found silences, and this round found mostly **restatements that stop
short** — §19's tier lists, §21.7's inventory, §8.1's checksum map, each
accurate about what it names and incomplete about what it omits. Three
warrant more than an edit and are named above.

## Artifacts

- [prompt.md](prompt.md) — charters, access rule, taxonomy, pass criteria
- `transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`
  — the three implementer walks
- `transcript-diagrams.md` — the figure audit
- `transcript-register.md` — §21 against the rules it restates
- `transcript-adversary.md` — attacks tried, and which the text refutes
- `transcript-quiz.md` — the slate, both independent answer sets, and the
  adjudication
- `transcript-triage-correctness.md`, `transcript-triage-implementer.md`,
  `transcript-triage-skeptic.md` — the three blind triage passes
