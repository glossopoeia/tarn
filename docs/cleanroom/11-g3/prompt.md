# Cleanroom round 11 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 10 found one byte-level ambiguity — an em-dash clause in §20.4 whose
attachment decided whether the format's most routine commit may destroy an
unknown record — in text ADR-0066 had written. All 27 of its defects are now
dispositioned, and its six escalations landed as ADR-0070 and ADR-0071.

Four rounds running, the defect the next round found sat in the previous
round's repair. ADR-0071 was written in full knowledge of that, and it still
had to trim a sentence ADR-0069 had written one commit earlier.

Two things make this round's text unusually worth reading cold. Several rules
were **rewritten on a different principle** rather than adjusted — a field
taxonomy restated around what a value determines, an obligation moved from one
actor to another, a partial-total definition whose error direction was
deliberately inverted, a claim about the document's own completeness narrowed
to a finding aid. And working up round 10's decisions turned up **seven
conformance vectors that would have failed a correct implementation** — two
asserting a reader must refuse where no reader is obliged to, five recording
expected content the file does not carry. Those were tooling defects, not
document defects, but they are the sharpest evidence yet that a rule can read
cleanly and still be applied wrongly by the people closest to it.

The measurement, taken before this round was written: **85 lines inserted and
51 deleted across 25 hunks, touching 20 sections.**

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

Two standing charges carried from earlier rounds. The register hunter checks
**every cross-reference to a register row against the row it actually lands
on**, and **recounts by hand every total the document states about itself**.
The diagram auditor treats the conformance checklists and any table restating
a rule stated in prose as figures.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Five rounds of calibration, pointing both ways: reporters flagged 33
byte-level and 5 survived; then 8 and 0; then 5 and **2**; then 3 and 0; then
7 and **1**. The base rate is neither zero nor high. A judge who has decided
in advance which way to lean has stopped testing anything.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind
to each other. The three-way reconciliation is done by the maintainer's agent
directly, not delegated, and mechanically: union-find over the passes'
groupings and a set difference on finding ids. Each walk's transcript is
diffed against its own structured return — in round 9 a walk wrote eight
findings and returned one, and only that diff recovered them; in round 10 the
guard held for all six.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**.
