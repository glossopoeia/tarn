# Cleanroom round 10 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 9 found zero byte-level ambiguities and a quiz of 15 agree / 0 diverge
/ 0 underdetermined. Its 35 defects are now dispositioned, and five
maintainer decisions landed as ADR-0068 and ADR-0069.

One of those decisions reversed the reasoning of two earlier ADRs. Working up
round 9's endianness question, the maintainer asked why byte order should
count as *history* when the format is little-endian only — and the answer was
that it does not: `[R-ENC-01]` defines the encoding rather than constraining
it, so "stored big-endian" is not a state a file can be in, and the same
holds for field width. Four register rows that recorded a writer's mistake as
a file condition were retired, the remaining rows renumbered, and a rule that
had stood unapplied since ADR-0057 was finally applied uniformly.

That is a large, mostly mechanical change to the register, sitting on top of
round 9's own repairs — and **every line of it is text no cleanroom round has
read.** Three rounds running, the defect the next round found was in the
previous round's repair.

The measurement, taken before this round was written: **157 lines inserted
and 130 deleted across 28 hunks, touching 20 sections.**

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes,
not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or
`README.md`. Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

The reason is not ceremony. A conclusion you reach because a test vector or
an ADR told you is not evidence that the specification says it, and this
gate's whole claim is that the document stands alone. A disclosed breach is
a usable result; an undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a
**diagram auditor**, a **register hunter**, an **adversary**, and a **quiz**
authored, answered and keyed by three agents blind to one another.

The register hunter carries an extra charge this round: **every
cross-reference to a register row, from any section, appendix, checklist or
worked example, checked against the row it actually lands on.** Rows were
removed and the remainder renumbered, so a citation that survived the shift
pointing at its old neighbour is indistinguishable, to a reader, from a rule
that means something else.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Four rounds of calibration, pointing both ways. Round 6's reporters flagged
33 byte-level and 5 survived; round 7's flagged 8 and 0; round 8's flagged 5
and **2 survived**; round 9's flagged 3 and 0. The base rate is neither zero
nor high, and a judge who has decided in advance which way to lean has
stopped testing anything.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind
to each other. The three-way reconciliation is done by the maintainer's agent
directly, not delegated, and mechanically: union-find over the passes'
groupings and a set difference on finding ids.

**And each walk's transcript is diffed against its own structured return.**
In round 9 a walk wrote eight findings and returned one, with its disclosure
field reading `test`; no agent errored, the schema was satisfied, and seven
findings — six of them new — were recovered only by that diff.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**.
