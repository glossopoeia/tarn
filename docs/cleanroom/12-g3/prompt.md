# Cleanroom round 12 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 11 found one byte-level ambiguity — a clause in §20.3 whose trigger
could never produce its outcome, and which collided with step 4 of its own
requirement — in text ADR-0071 had written one commit earlier. Its 36 defects
are dispositioned, and ADR-0072 settled both of its escalations.

Two things are different about this round.

**The changed surface is the smallest of any round: 59 lines inserted and 30
deleted across 9 hunks, touching only 6 sections.** Eleven rounds of repair
have left little new text to read, which changes where a walk's effort is best
spent — see the brief's weighting note.

**A mechanical propagation check now exists** (ADR-0073). Five rounds running,
the defect the next round found sat in the previous round's repair, always the
same shape: a rule fixed in one place, its restatements left at the old
meaning. That class is now checked by machine on every change, and validated
against the revisions where those defects lived. It was run on the commit this
round reads, which flagged eight restatement sites; all eight were verified in
sync by hand before this round was launched.

So the propagation class should be thinner here than in any previous round. If
this round still finds one, that is the most useful single result it can
produce, because it means the check has a blind spot worth knowing about — and
its known blind spot is already recorded: it is a term-overlap heuristic and
cannot see two passages that contradict each other while sharing no
vocabulary, which is exactly the shape of round 11's survivor.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes, not
this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or `README.md`.
Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

A conclusion you reach because a test vector or an ADR told you is not
evidence that the specification says it, and this gate's whole claim is that
the document stands alone. A disclosed breach is a usable result; an
undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a **diagram
auditor**, a **register hunter**, an **adversary**, and a **quiz** authored,
answered and keyed by three agents blind to one another.

Standing charges: the register hunter checks **every cross-reference to a
register row against the row it lands on** and **recounts by hand every total
the document states about itself**; the diagram auditor treats the conformance
checklists and any table restating a rule as figures.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Six rounds of calibration, pointing both ways: reporters flagged 33 byte-level
and 5 survived; then 8 and 0; then 5 and **2**; then 3 and 0; then 7 and
**1**; then 3 and **1**. The base rate is neither zero nor high, and a judge
who has decided in advance which way to lean has stopped testing anything.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind
to each other. The three-way reconciliation is done by the maintainer's agent
directly, not delegated, and mechanically: union-find over the passes'
groupings and a set difference on finding ids. **Each walk's transcript is
diffed against its own structured return, and the workflow's own error report
is read before any result** — in round 9 a walk returned one of the eight
findings it had written, and in round 11 a walk died after writing six, both
recovered only by going to disk.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**.
