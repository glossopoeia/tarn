# 0001. Record architecture decisions as in-repo ADRs

- Status: Accepted
- Date: 2026-07-29
- Covers: project process
- Confirm: none

## Context

TARN is a spec-first project with a stated AI-assistance policy: design
authority rests with the maintainer, and the reasoning trail must be public and
auditable. Format history shows what happens when rationale lives outside the
canonical repository with unclear authority — TIFF's technical notes circulated
for decades marked "draft" while functioning as the de facto standard, and its
extension registry died with a decommissioned mailbox. Reasoning that is not
recorded where the spec lives eventually stops binding anyone.

## Decision

Every format-level decision is recorded as a numbered ADR in `docs/decisions/`,
using the template in `0000-template.md`. ADRs are numbered in drafting order
and never renumbered or reused. A superseded ADR is never edited in substance:
a new ADR supersedes it, and both link to each other. Once spec drafting
begins, every spec section cites the ADRs that govern it, and spec changes
after the first draft require a pull request that links its ADR.

## Consequences

The process is cheap enough for a single maintainer to sustain, and it makes
the README's claim — "the reasoning trail lives in docs/decisions/" — true from
the first commit. Contributors can challenge a decision by targeting a specific
ADR rather than re-litigating folklore. The cost is discipline: decisions made
in discussion do not exist until they are written down here.

## Precedent

- Michael Nygard's "Documenting Architecture Decisions" (the original ADR
  pattern) and the MADR template family.
- TIFF's satellite-technote and dead-registry history, catalogued in
  `docs/research/reference-format-lessons.md`.
