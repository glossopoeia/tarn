# 0003. Normative conventions and conformance classes

- Status: Accepted
- Date: 2026-07-29
- Covers: spec register; conformance structure; violation-outcome classes
- Confirm: none

## Context

Underspecified reader behavior is the single most reliable way to fragment a
format's ecosystem. TIFF never defined what a reader does with a violating
file, so the most tolerant reader became the de facto standard and writers
targeted its quirks. QOI shows the small-scale version: lowercase "must,"
requirements with no named actor, and limits that live only in the reference
implementation all produced divergent decoders. PNG's conformance section —
per-role checklists, no subset profiles — is the proven fix.

## Decision

The spec adopts BCP 14 (RFC 2119 + RFC 8174) with the boilerplate verbatim:
keywords are normative only in ALL CAPS. One blanket sentence marks examples,
notes, rationale boxes, and non-normative appendices; all other text is
normative. Every requirement names its actor, and every writer-MUST is paired
with an explicit reader clause (what a reader does with a file that violates
it). Requirements carry stable IDs (e.g. `[R-IDX-03]`) so checklists, test
vectors, and reviews cite requirements rather than prose positions.

Conformance is defined for four classes:

- **file** — a pure predicate on bytes;
- **reader** — MUST accept every conforming file within spec-stated limits; no
  subset profiles (every reader handles all core codecs, both channel layouts,
  every core data type);
- **writer** — MUST emit only conforming files; conformance is semantic, with
  no canonical-bytes promise;
- **updater** — a tool that modifies files it may not fully understand, with
  explicit preservation obligations.

Every detectable violation the spec defines is assigned exactly one outcome
class: **reject-file**, **reject-layer**, **reject-tile**, **ignore-record**,
or **preserve-verbatim**. All limits (maximum rank, name lengths, structure
sizes) live in the spec, never only in an implementation.

## Consequences

The undefined-behavior worklist becomes a fill-in-the-table exercise instead of
ad hoc prose, and cleanroom implementer tests can be scored against outcome
classes. The cost is drafting discipline: a requirement without an actor or an
outcome is a defect by definition.

## Precedent

- RFC 2119 / RFC 8174 (BCP 14); RFC 8259's parser/generator asymmetry and
  minimum-guarantee limit pattern.
- PNG §15 (conformance structure); TIFF's tolerant-reader death spiral and
  QOI's implementation-defined limits, catalogued in
  `docs/research/reference-format-lessons.md`.
