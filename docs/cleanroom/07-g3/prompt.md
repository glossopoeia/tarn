# Cleanroom round 7 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 6 found 85 findings, which triage reduced to 67 distinct defects
and 5 byte-level ones. All five were fixed, three more were taken at the
same time, 49 of 56 editorial defects were cleared, and the four that
turned out to be design decisions took ADRs 0059–0062.

Every one of those fixes is text no cleanroom round has read.

The measurement, taken before this round was written: **310 lines
inserted and 145 deleted across 72 hunks, touching 35 sections.** The
heaviest are §21.1 (27 changed lines), §2.3 (29), §6.1 (22), §17.2 (19),
§20.5 (18), §18.2 (15), §19.4 (14), §7.1 (13), §5.1 (12), §21.7 (11) and
§19.1 (11). Round 6's own lesson was that findings concentrate in the
newest text, because it is the text no one has yet had to implement
from. So this round is weighted the same way round 6 was — toward what
has never been read cold — and the sections above are where to spend
attention first.

That weighting is a hint about *where to look*, never about what the
answer is. No agent in this round is told what changed, why, or what any
fix was meant to accomplish.

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

Round 6 is the calibration. Reporters flagged 33 findings byte-level and
5 survived. The dominant cause of over-claiming was a reporter finding a
register row that contradicts a rule and concluding a verifier's verdict
was open — when §21.1's *"where a row and the rule it cites diverge, the
rule governs"* has already decided it, and only the table is wrong. A
finding is not byte-level because it is important, or because it is
embarrassing; it is byte-level only if two implementations reading the
text could disagree about actual bytes.

## Disposition

Three independent triage passes deduplicate the findings and re-judge
each against the byte-level test. No pass sees another's output. The
three-way reconciliation is done by the maintainer's agent directly,
not delegated — in round 6 a delegated reconciler received one of three
passes, truncated, and disclosed it rather than manufacturing agreement.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz
fully graded with every divergence resolved by a spec fix or a key
correction; zero findings left without a disposition. This being an
acceptance round, G3 additionally requires **zero byte-level ambiguities
outright**.
