# Cleanroom round 13 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 12 found one byte-level ambiguity — a commit that shrinks a dimension
extent leaves its own file nonconforming, because nothing forces the affected
tiles to be re-emitted while `[R-SER-05]` starts demanding fill in the columns
the shrink turned into padding. Its 24 defects are dispositioned: 21 fixed,
2 deferred, 1 escalated. All three of those tails are now closed, and they are
what this round reads.

**The changed surface is the largest in several rounds: 200 lines inserted and
54 deleted across 36 hunks, touching 29 sections.** That reverses the trend —
round 12 read the smallest surface of any round — and it changes what the
round is testing.

Two things make this surface different in kind, not only in size.

**It is not only repairs.** Every previous round changed text that already
existed. This one includes material written from scratch, which no round has
read cold and no one has implemented from, and a requirement identifier that
did not exist before. Newly authored normative text has had the least review
of anything in the document.

**Round 12's survivor was a blind-spot result, and the blind spot is still
there.** The mechanical propagation check of ADR-0073 runs on every change and
ran on the commits this round reads. It is a term-overlap heuristic: it cannot
see two passages that contradict each other while sharing no vocabulary, and
it cannot see a rule that was never written down twice. Round 12's defect was
the second shape. So the propagation class should again be thin — and a
propagation defect found here would be the most useful single result the round
can produce, because it would mean the check has a second blind spot worth
knowing about.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes, not
this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or `README.md`.
Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

No agent reads the round's own output directory, either: transcripts are
written there while other agents are still working, and reading one would
destroy the independence the round is built on.

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
checklists and any table restating a rule as figures, and checks every worked
example byte by byte.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Seven rounds of calibration, pointing both ways: reporters flagged 33
byte-level and 5 survived; then 8 and 0; then 5 and **2**; then 3 and 0; then
7 and **1**; then 3 and **1**; then 6 and **1**. The base rate is neither zero
nor high, and a judge who has decided in advance which way to lean has stopped
testing anything.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind
to each other — and, new this round, expressly barred from reading each
other's transcripts, which the access rule had not previously named. The
three-way reconciliation is done by the maintainer's agent directly, not
delegated, and mechanically: union-find over the passes' groupings and a set
difference on finding ids. **Each walk's transcript is diffed against its own
structured return, and the workflow's own error report is read before any
result** — in round 9 a walk returned one of the eight findings it had
written, in round 11 a walk died after writing six, and in round 12 a walk
died while the harness's own detector reported none.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**.
