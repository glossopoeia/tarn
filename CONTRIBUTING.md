# Contributing to TARN

Thanks for your interest. TARN is a spec-first project: the deliverable is
the specification, its decision record, and conformance test vectors — not
implementation code. Contributions that sharpen ambiguity, find holes, or
add test vectors are the most valuable kind.

## Ground rules

- **Decisions live in ADRs.** Format-level proposals must land as (or amend)
  an ADR in [docs/decisions/](docs/decisions/), following
  [the template](docs/decisions/0000-template.md). Open design questions go
  through [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) first — a new format
  feature that hasn't appeared there as a proposal will be redirected there
  before it is discussed on the merits.
- **Design authority rests with the maintainer.** Discussion is open;
  final calls are recorded, with reasoning, in the ADR trail.
- **Spec changes cite their ADR.** After the first spec draft exists, every
  pull request that changes normative text links the ADR that governs it.
- **No implementation dependencies.** Nothing in this repository may depend
  on any particular implementation, vendor, or AI product. Agent-facing
  instructions live in [AGENTS.md](AGENTS.md) only.

## AI-assistance policy

This project is developed with substantial AI assistance under human
direction (see the note in [README.md](README.md)). The same standard
applies to contributions:

- AI-assisted contributions are welcome. You are responsible for everything
  you submit: review it, understand it, and be able to defend it in review
  as your own work.
- Disclosure is appreciated when AI played a substantial role in a
  contribution's design reasoning (not needed for routine wording or
  mechanical edits).
- Contributions that show signs of unreviewed generation — confident
  assertions nobody checked, citations that don't exist, prose that doesn't
  engage with the actual ADR trail — will be closed without detailed review.

## Licensing of contributions

Inbound = outbound, per path (see [NOTICE](NOTICE) and
[ADR-0016](docs/decisions/0016-licensing.md)):

- Specification text and docs: you license your contribution under
  **CC BY 4.0**.
- Schemas, tooling, harness code: **Apache-2.0**.
- Conformance vector files: **CC0 1.0**.

## Practical notes

- Keep ADRs to one page. Keep normative proposals in normative-ready
  language (BCP 14 keywords, named actors, paired reader/writer clauses —
  see [ADR-0003](docs/decisions/0003-spec-conventions-and-conformance.md)).
- Commit messages reference the ADR or open question they touch
  (e.g. `ADR-0009`, `Q-B2`).
- There is no CLA; the license grant above is the whole arrangement.
