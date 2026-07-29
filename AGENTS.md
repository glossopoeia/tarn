# Working instructions

Canonical instructions for anyone — human or AI agent — working in this
repository. Tool-specific pointer files in the repository root are one-line
pointers to this file; this is the only place working rules live. Nothing in
this repository may depend on or assume any particular AI vendor or product.

## What this repository is

The specification for TARN, a single-file tiled N-dimensional array format.
Spec-first: deliverables are the spec, the ADR decision trail, ID registries,
and conformance test vectors. **No implementation code** beyond eventual
test-vector tooling; any reference implementation will live in a separate
repository, and this repo never depends on one.

## Process rules

1. **Read before writing:** [PLAN.md](PLAN.md) (roadmap and drafting order),
   [OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) (what is undecided),
   [docs/decisions/](docs/decisions/) (what is decided and why).
2. **Decisions are ADRs.** Never encode a design decision in spec text,
   README prose, or a commit message alone — it exists when an ADR records
   it. Use [docs/decisions/0000-template.md](docs/decisions/0000-template.md);
   number in drafting order; supersede, never rewrite.
3. **Open questions gate new features.** Any format capability not already
   covered by an accepted ADR must first appear in OPEN-QUESTIONS.md as a
   proposal with options and tradeoffs.
4. **Spec text encodes Accepted decisions only.** Proposed ADRs and open
   ledger entries never leak into normative text.
5. **Normative register** (once spec drafting begins): BCP 14 keywords in
   ALL CAPS only; every requirement names its actor; every writer-MUST is
   paired with a reader clause; every non-obvious encoding gets a worked
   numeric example; requirements carry stable IDs. See
   [ADR-0003](docs/decisions/0003-spec-conventions-and-conformance.md).
6. **Cleanroom protocol** (Phase 2): after each drafted batch, a
   fresh-context agent receives only the spec text — no history, no ADRs —
   and must describe a conforming reader, answer byte-level questions, and
   list ambiguities. Ambiguities are spec bugs; fix them before drafting
   continues. Artifacts land in `docs/cleanroom/`.
7. **Conformance vectors ship with sections**, not after them; every error
   outcome and every sentinel gets a vector.

## Hygiene

- Commit messages reference the ADR or ledger entry they touch (`ADR-0009`,
  `Q-B2`); keep commits scoped to one reviewable unit.
- Respect the license split ([NOTICE](NOTICE)): prose is CC BY 4.0, code is
  Apache-2.0, vectors are CC0.
- No secrets, no generated artifacts, no vendor-specific configuration
  beyond tool-specific pointer files to this document.
- Do not add implementation code "temporarily." If tooling is needed for
  vectors, it lands under `conformance/` with an ADR noting its scope.

## Current phase

Phase 1 (planning) is complete when this scaffolding is reviewed. Phase 2
(spec drafting, per [PLAN.md §5](PLAN.md)) begins only on explicit maintainer
approval, and proceeds batch by batch — propose section content points,
agree, draft, refine, cleanroom-test.
