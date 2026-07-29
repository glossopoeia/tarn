# 0016. Licensing: CC BY 4.0 spec text, Apache-2.0 tooling, CC0 test vectors

- Status: Accepted
- Date: 2026-07-29
- Covers: repository licensing; IPR posture
- Confirm: CC0 for the binary conformance-vector corpus (recommended
  refinement over a single-license repo — confirm before the corpus ships).

## Context

A specification's license governs its *text*; implementations of the format
it describes are not derivative works of that text, so the goal is a license
that keeps the prose freely reusable while preserving attribution — the hook
through which the project's design-authority policy stays visible.
Format-adoption history rewards low legal friction: QOI's public-domain-style
corpus is copied wholesale into test suites in every language, while
proprietary frozen stewardship (TIFF's) is the documented dead end. Patent
posture matters more for format tooling than for prose, which argues for
Apache-2.0's explicit grant over MIT where code is involved.

## Decision

- **Specification text and documentation** (`docs/`, `PLAN.md`,
  `OPEN-QUESTIONS.md`, `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, other
  repository documentation files, and `spec/` when it exists):
  **CC BY 4.0** (`LICENSE-SPEC`).
- **Schemas, tooling, and conformance-harness code**: **Apache License 2.0**
  (`LICENSE`; also the GitHub-detected repo license).
- **Binary conformance vectors** (`conformance/vectors/`, Phase 2): intended
  **CC0 1.0**, so third-party test suites embed them without attribution or
  NOTICE propagation.
- The spec itself will carry a short plain-language IPR paragraph: the format
  is published to be freely implementable, the maintainer asserts no patents
  over it, and all normative codec references target unencumbered
  specifications (RFC 1951 DEFLATE, RFC 8878 zstd, LZ4). New codec
  registrations receive an IPR check as part of registry review.
- Mechanics: `NOTICE` and the README license table map paths to licenses;
  `CONTRIBUTING.md` states inbound-equals-outbound per path.

Alternatives considered: CC0 for the spec text (rejected: surrenders
attribution, and CC0 §4(a) affirmatively reserves patent rights — worse than
CC BY on the one axis specs care about); MIT for prose (a software license
applied to text, no patent language, no benefit over CC BY); OWFa 1.0
(strongest patent posture but obscure enough to *add* review burden for
adopters — its benefit is captured by the IPR paragraph instead).

## Consequences

Anyone can quote, translate, or fork the spec with attribution; tooling
composes with the wider ecosystem under a familiar code license; vectors are
frictionless everywhere. The cost is a three-license repository, mitigated by
the NOTICE/README path map.

## Precedent

- QOI's freely-copied corpus as the adoption engine for test fixtures.
- W3C royalty-free regime (PNG) as the model whose *intent* the IPR paragraph
  reproduces at single-maintainer scale.
- TIFF's proprietary stewardship as the cautionary tale.
