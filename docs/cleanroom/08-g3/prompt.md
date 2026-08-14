# Cleanroom round 8 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 7 met G3's byte-level criterion for the first time: 63 findings, 8
self-flagged byte-level, **0 surviving** by unanimous triage, and a quiz
that came back 15 agree / 0 diverge / 0 underdetermined. All 44 of its
distinct defects are now dispositioned.

The gate is still open for one reason only: **every fix since is text no
cleanroom round has read.**

The measurement, taken before this round was written: **371 lines
inserted and 169 deleted across 72 hunks, touching 43 sections.** The
heaviest are §2.3 (28 changed lines), §9.7 (22), §18.2 (22), §17.2 (21),
§19.1 (19), §15.3 (18), §20.3 (17), §5.1 (15), §5.2 (15), §21.1 (15),
§22.3 (13), Appendix H (13), §18.4 (10) and §6.3 (8). A second tier —
§15.4, §21.3, §21.9, §20.4, §8.1, §9.3, §9.6, §19.3, §19.4, §11.1,
§13.3, §16.2 — changed by less but changed.

Round 6's lesson, which round 7 confirmed, is that findings concentrate
in the newest text, because it is the text no one has yet had to
implement from. So this round is weighted the same way round 7 was, and
the sections above are where to spend attention first.

That weighting is a hint about *where to look*, never about what the
answer is. No agent in this round is told what changed, why, or what any
fix was meant to accomplish. Several of those sections carry the first
statement of their rule anywhere in the document; reading them cold is
the point of the exercise.

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
   wording to the rule it cites; both are checkable by reading.
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

Two rounds of calibration. Round 6's reporters flagged 33 findings
byte-level and 5 survived; round 7's flagged 8 and 0 survived. The
dominant cause of over-claiming was a reporter finding a register row
that contradicts a rule and concluding a verifier's verdict was open —
when §21.1's *"where a row and the rule it cites diverge, the rule
governs"* has already decided it, and only the table is wrong. A finding
is not byte-level because it is important, or because it is
embarrassing; it is byte-level only if two implementations reading the
text could disagree about actual bytes.

The calibration cuts both ways, and triage is told so explicitly: two
rounds of *"almost nothing survives"* anchors a judge toward
downgrading. A finding that genuinely forks the bytes must survive that
prior. The reconciliation re-reads the strongest survivors against the
text by hand rather than accepting any pass's verdict.

## Disposition

Three independent triage passes deduplicate the findings and re-judge
each against the byte-level test. No pass sees another's output. The
three-way reconciliation is done by the maintainer's agent directly,
not delegated, and mechanically: union-find over the passes' groupings
and a set difference on finding ids, because in each of the last two
rounds a triage-stage agent's claim about its own coverage did not
survive checking.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz
fully graded with every divergence resolved by a spec fix or a key
correction; zero findings left without a disposition. This being an
acceptance round, G3 additionally requires **zero byte-level ambiguities
outright**.
