# Cleanroom round 6 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round is not the previous one

Rounds 4 and 5 found only propagation failures — a rule changed in one
place and left standing in another — while both constructive
instruments (an adversary building a file two verifiers judge
differently, a differential writer emitting the same file twice) came
back empty three rounds running. PLAN §9 recorded the reading: the
format looks determinate and the residual risk is editorial
consistency, which two other instruments would close better than a
sixth round of the same shape.

Both have since been built and run. A mechanical consistency check
found ten register defects; the conformance corpus found eight more,
including two rows that could not be distinguished from their
neighbours and one that no file could exhibit. Between them they have
rewritten §21 three times and added text to §5, §6.4, §9, §12, §14,
§19, §20 and §24, plus six diagrams — **none of which any cleanroom
round has seen.**

So this round is weighted toward material that has never been read
cold, and adds two roles the earlier rounds did not have: an auditor
for the diagrams, which are new restatement sites, and a hunter aimed
at the register, which has changed most.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research
notes. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or `README.md`.
Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

The reason is not ceremony. A conclusion you reach because a test
vector or an ADR told you is not evidence that the specification says
it, and this gate's whole claim is that the document stands alone. If
you read something outside `spec/tarn.md`, say so plainly in your
report; a disclosed breach is a usable result, an undisclosed one
poisons the round.

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
4. **Quiz** — a fixed slate of byte-level questions, answered cold.
   The answer key is derived by a different agent, independently, from
   the same text. A divergence indicts the key's reading as readily as
   the answer's.
5. **Diagram auditor** — every figure in the document, checked against
   the prose it illustrates and the rules it cites. A figure that
   contradicts its section, or that a reader could take further than
   the section licenses, is a defect of the same class as a stale
   restatement.
6. **Register hunter** — §21 against the rules it restates. §21.1 makes
   the register's completeness normative and subordinates every row's
   wording to the rule it cites; both are checkable by reading.
7. **Adversary** — construct a file two conforming verifiers could
   judge differently, or show why the text forecloses it.

## Finding taxonomy

Required of every agent:

- **AMBIGUITY** — location, every permitted reading, which you picked
  and why.
- **CONTRADICTION** — both citations, quoted.
- **OBSERVATION** — decidable, but disproportionately expensive to
  decide.

Reserved values and sections are not defects. Unresolvable forward
references into them are reportable and expected.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz
fully graded with every divergence resolved by a spec fix or a key
correction; zero findings left without a disposition. This being an
acceptance round, G3 additionally requires **zero byte-level
ambiguities outright**.
