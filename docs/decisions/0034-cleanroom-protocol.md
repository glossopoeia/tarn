# 0034. The cleanroom protocol, as piloted

- Status: Accepted (resolves Q-I2)
- Date: 2026-07-30
- Covers: cleanroom-round mechanics, pass criteria, artifacts
- Confirm: none

## Context

The drafting process gates each part of the spec on fresh-context
implementability, and the protocol's details — roles, batch size, pass
criteria, artifact layout — were deliberately left to be pinned by a
pilot. Round 1 (the container spine) ran the pilot: four independent
fresh-context implementers with a hard spec-text-only access rule, in
parallel, against §2–§9 plus §11.

## Decision

The protocol, as validated by the pilot:

- **Access rule:** each agent reads `spec/tarn.md` and nothing else —
  no ADRs, ledger, plan, history, or web. Every conclusion cites
  section numbers and requirement IDs.
- **Four roles, run independently in parallel:** a *reader*
  implementer (open paths, degradation walks, byte-exact request
  accounting), a *verifier* implementer (certification procedure,
  coverage walk, a worked multi-generation trace), a *writer*
  implementer (creation byte layout, append, torn-recovery, legitimate
  byte-divergence catalog), and a *quiz* (12–15 pointed byte-level
  questions authored per round, graded against an answer key derived
  independently from the spec — mis-keyed answers indict the key
  author's reading as readily as the agent's).
- **Finding taxonomy**, required of every agent: AMBIGUITY (location,
  permitted readings, pick and rationale), CONTRADICTION (both
  citations), OBSERVATION (decidable but disproportionately
  expensive). Reserved sections are not defects; unresolvable forward
  references into them are reportable and expected.
- **Disposition:** every AMBIGUITY and CONTRADICTION is a spec bug —
  fixed before the next batch, or explicitly deferred with a named
  owning section and a PLAN batch-row note. OBSERVATIONS may prompt
  non-normative clarifications and vector candidates.
- **Pass criteria for a gate:** all implementer walks correct against
  the drafter's intent; quiz fully graded with every divergence
  resolved (spec fix or key correction); zero findings left without a
  disposition. The final acceptance round additionally requires zero
  byte-level ambiguities outright (PLAN gate G3).
- **Artifacts** land in `docs/cleanroom/NN-name/`: `prompt.md` (the
  charters and access rule), verbatim `transcript-*.md` per role, and
  `findings.md` (verdict, quiz score, fixed/deferred disposition
  table).
- **Timing:** a round may run mid-scope when a coherent subsystem
  stabilizes (the pilot ran on the container before the tile index
  existed); deferred half-scopes fold into the next round.

## Consequences

Pilot results validate the design: 15/15 on the quiz, two genuine
contradictions found that three review passes had missed, and ~20
fixes landed. The cost per round (~4 agent-runs) is the price of the
weekend-implementable claim being tested rather than asserted.

## Precedent

- The reference-implementation-divergence lesson (QOI): fix the spec
  wherever an implementer had to peek — here, wherever a fresh
  implementer had to guess.
