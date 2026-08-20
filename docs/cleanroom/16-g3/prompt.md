# Cleanroom round 16 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 15 found a byte-level ambiguity in round 14's repair, which had
itself been written to close round 14's finding in round 13's repair. Both
sat in the same sentence, §20.3 step 4, which is now on its fourth
revision.

Fifteen rounds support one durable claim about this process: **no two
consecutive rounds have ever come back clean**, and each of the three
rounds that found nothing (7, 9, 13) was followed by one that found a
defect in the repairs that round produced (8, 10, 14). This round tests
round 15's repairs, which were the largest single batch the project has
made — 23 defects fixed at once.

**The changed surface is 90 lines inserted and 35 deleted across 15 hunks,
touching 9 sections** — §4.2, §11.1, §20.3, §20.5, §21.1, §21.2, §21.3,
§21.7 and Appendix G, six of them with two hunks each.

Three properties of it are given to the walks, none of which says what any
answer is. A rule here is on its **fourth revision**. Several of these
repairs were written to fix a rule **cited for the opposite of what it
says**, or one that claimed to enumerate cases and did not — a class of
repair that tends to overcorrect. And one repair **moved a statement out of
a non-normative block into normative text**, the third round running in
which a rule was found to carry no force because §2.1 excluded where it
sat.

Both of ADR-0073's recorded blind spots remain live, as they are in every
repair round: the propagation check cannot see two passages that
contradict each other without shared vocabulary, and it cannot see two
passages written to disagree in the same commit.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes,
not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or
`README.md`. Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

No agent reads the round's own output directory. The three triage passes
are additionally barred from each other's transcripts by name.

A conclusion you reach because a test vector or an ADR told you is not
evidence that the specification says it, and this gate's whole claim is
that the document stands alone. A disclosed breach is a usable result; an
undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a
**reader** implementer, a **writer** implementer, a **verifier**
implementer, a **diagram auditor**, a **register hunter**, an
**adversary**, and a **quiz** authored, answered and keyed by three agents
blind to one another.

Standing charges: the register hunter checks **every cross-reference to a
register row against the row it lands on** and **recounts by hand every
total the document states about itself**; the diagram auditor treats the
conformance checklists and any table restating a rule as figures, and
checks every worked example byte by byte.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not
defects; unresolvable forward references into them are reportable and
expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Fifteen rounds: 33 flagged / 5 survived; 8/0; 5/2; 3/0; 7/1; 3/1; 6/1;
0/0; 1/1; 1/1. The record is given to both charters with the warning that
it is a fact about the process and not a quota — it neither promises a
defect nor licenses inventing one.

Three cautions carried into triage, each earned in the last two rounds.
Search for the deciding sentence as hard as you would search to refute:
one round's passes graded a finding on the absence of text §3 contained,
and last round's survivor was settled by grepping a single word and
noticing its one occurrence sat where §2.1 strips force. Make the
emittable-by-another-actor distinction explicitly rather than by feel. And
check a citation against the rule it names, not against the sentence around
it.

## Harness

Round 15's first pass had the worst failure the project has recorded:
three agents returned schema-valid placeholders at once, the emptiness
guard added after round 13 passed all three, and triage graded 23 findings
where 38 existed. The guard is now a general degeneracy check —
`assertNotDegenerate`, rejecting any return whose prose fields are too
short to be prose — applied to the slate, every walk, both quiz takers and
all three triage passes.

## Disposition

Three independent triage passes deduplicate and re-judge every finding,
blind to each other. The three-way reconciliation is done by the
maintainer's agent directly, not delegated, and mechanically: union-find
over the passes' groupings and a set difference on finding ids. **Each
walk's transcript is diffed against its own structured return, and the
workflow's own error report is read before any result.** The maintainer
additionally reads the same repairs independently, and reports what the
round missed as well as what it found.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction;
zero findings left without a disposition. This being an acceptance round,
G3 additionally requires **zero byte-level ambiguities outright**.
