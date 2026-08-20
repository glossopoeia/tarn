# Cleanroom round 14 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 13 met G3's criterion: zero byte-level defects, over the largest
changed surface any round had read, with reporters self-flagging none for
the first time in thirteen rounds and all three triage passes agreeing.

That result is a property of the commit round 13 read, not of this
document. Round 13 then produced **seventeen repairs**, and this round
exists to read them.

The reason is the project's own record. For five rounds running the defect
the next round found sat in the previous round's repair. Twice a repair
introduced something worse than what it fixed. Once — round 9's fix to
§20.3's example — a repair was placed inside a non-normative block and sat
inert for three rounds. Two of round 13's own seventeen findings were
defects introduced by the commits of the day before, one of them in the
repair ADR-0074 had written to close round 12.

So the claim under test here is narrow and precise: **do round 13's repairs
hold, read cold by someone who has never seen them?**

**The changed surface is 79 lines inserted and 39 deleted across 21 hunks,
touching 17 sections** — §2.3, §4.7, §5.2, §11.1, §16.2, §20.3, §21.1
through §21.7, §21.9, §24, and Appendices G and H. Nearly every hunk is a
repair.

Two things are known going in. The mechanical propagation check (ADR-0073)
ran on those repairs and is clean, but it has two recorded blind spots: it
is a term-overlap heuristic and cannot see two passages that contradict
each other while sharing no vocabulary, and — found in round 13 — it cannot
see two passages **written to disagree in the same commit**, because it
only reports sites a change did not sweep. Both blind spots are live here,
since this round reads one commit's worth of repairs.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes,
not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or
`README.md`. Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

No agent reads the round's own output directory: transcripts are written
there while other agents are still working. The three triage passes are
additionally barred from each other's transcripts by name.

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

Eight rounds of calibration: reporters flagged 33 byte-level and 5
survived; then 8 and 0; then 5 and **2**; then 3 and 0; then 7 and **1**;
then 3 and **1**; then 6 and **1**; then **0 and 0**.

That last figure is the one this round has to be careful with. A round that
finds nothing because the text is clean and a round that finds nothing
because its readers expected to find nothing produce identical reports, and
only one is worth having. Both charters name the risk explicitly.

## Harness changes this round

Round 13's quiz author died mid-response. Its consumers received an empty
slate and each invented fifteen questions of their own, returning
schema-valid answers to *different* questions — a quiz indistinguishable,
in the structured result, from a graded one. **The workflow now refuses to
launch the answerer and keyer against an empty slate**, rather than
interpolating one silently. That is the fourth distinct shape of harness
failure this project has hit, and the first for which a guard now exists.

## Disposition

Three independent triage passes deduplicate and re-judge every finding,
blind to each other. The three-way reconciliation is done by the
maintainer's agent directly, not delegated, and mechanically: union-find
over the passes' groupings and a set difference on finding ids. **Each
walk's transcript is diffed against its own structured return, and the
workflow's own error report is read before any result.**

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction;
zero findings left without a disposition. This being an acceptance round,
G3 additionally requires **zero byte-level ambiguities outright**.
