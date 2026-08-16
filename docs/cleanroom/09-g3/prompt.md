# Cleanroom round 9 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 7 met G3's byte-level criterion for the first time — 63 findings, 8
self-flagged byte-level, zero surviving. Round 8 then read the text that
had been written since, and found **two** byte-level ambiguities, both in
§20.4's `[R-WRT-08]` table, and the first of them a propagation failure of
a repair round 7 had itself made to that same table.

That is the standing lesson of this gate: **a clean round certifies a
revision, not a document.** Round 8's 22 defects are now all dispositioned
— 21 fixed, 1 judged to need no change, across ADR-0066 and ADR-0067 — and
every one of those fixes is again text no cleanroom round has read.

The measurement, taken before this round was written: **130 lines inserted
and 80 deleted across 37 hunks, touching 19 sections.** The heaviest are
Appendix G (40 changed lines), §21.2 (39), Appendix H (20), §21.9 (17),
§21.6 (16), §2.3 (13), §4.7 (9), §21.1 (8), §9.7 (7) and §20.3 (7). Then a
second tier that changed by less but changed: §2.4, §21.7, §4.6, §9.2,
§15.3, §20.4, §21.3, §21.4.

Do not read the ordering as importance. One of the smallest hunks in that
list is the one two independent triage passes and a hand-check spent the
most effort on last round. Cover the whole list.

That weighting is a hint about *where to look*, never about what the
answer is. No agent in this round is told what changed, why, or what any
fix was meant to accomplish. Several of those sections carry the first
statement of their rule anywhere in the document, and at least one carries
a rule stated differently from how it stood before — reading them cold,
with no memory of a previous revision, is exactly the instrument.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research
notes, not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
or `README.md`. Not `conformance/` — no tooling, no vectors, no
manifest. Not `spec/registry.json`. No git history, no web.

The reason is not ceremony. A conclusion you reach because a test vector
or an ADR told you is not evidence that the specification says it, and
this gate's whole claim is that the document stands alone. If you read
something outside `spec/tarn.md`, say so plainly in your report; a
disclosed breach is a usable result, an undisclosed one poisons the
round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other.

1. **Reader implementer** — the open path, validation timing by tier,
   layer access, the tile-read algorithm, degradation walks, and the
   byte-exact cost of a cold remote open.
2. **Writer implementer** — creation byte layout, the append procedure,
   what becomes slack on each shape of commit, torn-write recovery, and
   a catalogue of legitimate byte-divergence between two conforming
   writers given identical input.
3. **Verifier implementer** — the certification procedure, the coverage
   walk and slack total, extent overlap, alignment and slab invariants,
   and the decoded-content obligations.
4. **Diagram auditor** — every figure in the document, checked against
   the prose it illustrates and the rules it cites. A figure that
   contradicts its section, or that a reader could take further than the
   section licenses, is a defect of the same class as a stale
   restatement.
5. **Register hunter** — §21 against the rules it restates. §21.1 makes
   the register's completeness normative and subordinates every row's
   wording to the rule it cites; both are checkable by reading. Every
   cross-reference to a register row is checkable by reading too.
6. **Adversary** — construct a file two conforming verifiers could judge
   differently, or show why the text forecloses it.
7. **Quiz** — a fixed slate of byte-level questions, answered cold. The
   slate is authored by one agent, answered by a second, and keyed by a
   third, each blind to the others' output. A divergence indicts the
   key's reading as readily as the answer's.

## Finding taxonomy

Required of every agent:

- **AMBIGUITY** — location, every permitted reading, which you picked
  and why.
- **CONTRADICTION** — both citations, quoted.
- **OBSERVATION** — decidable, but disproportionately expensive to
  decide.

Reserved values and sections are not defects. Unresolvable forward
references into them are reportable and expected.

## The byte-level test

Every finding is judged against one question, and reporters are asked to
answer it for their own findings before triage does:

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Three rounds of calibration, and this time it does not point one way.
Round 6's reporters flagged 33 byte-level and 5 survived; round 7's
flagged 8 and 0 survived; round 8's flagged 5 and **2 survived**. A
finding is not byte-level because it is important, or because it is
embarrassing — but nor is the base rate zero. Both of round 8's survivors
were in a table a previous round had just repaired, and both were upheld
by three independent judges who were explicitly warned against
over-downgrading.

## Disposition

Three independent triage passes deduplicate the findings and re-judge
each against the byte-level test. No pass sees another's output. The
three-way reconciliation is done by the maintainer's agent directly,
not delegated, and mechanically: union-find over the passes' groupings
and a set difference on finding ids. In rounds 6 and 7 a triage-stage
agent's claim about its own coverage did not survive checking; in round 8
all three did, under a schema that required the complete input id list
back. That check is run again regardless of the result.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz
fully graded with every divergence resolved by a spec fix or a key
correction; zero findings left without a disposition. This being an
acceptance round, G3 additionally requires **zero byte-level ambiguities
outright**.
