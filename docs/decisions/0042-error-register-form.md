# 0042. The error register is derivative, complete, and per-violation

- Status: Accepted
- Date: 2026-08-05
- Covers: normative status of §21's register; row granularity; the
  conformance-vector coverage claim (gate G5)
- Confirm: none

## Context

A consolidated violation × outcome table is the one place an
implementer checks "what happens when this is wrong," and every
specification that ships one faces the same trap: the table restates
rules that also live in the body, so the moment a cell drifts, two
normative statements contradict each other with no tiebreak. The
second question is granularity, which sets what the conformance
corpus can promise: a row reading "any constraint of the layer record
violated → reject-layer" is discharged by one test file while nine
sibling violations go unexercised.

## Decision

- **Derivative, with normative completeness.** The register's
  completeness is normative and testable: every violation this
  specification names appears in it. Each row's substance restates
  the rule it cites, and **the cited rule governs** on any
  discrepancy — so the register is a checklist and an index, never a
  second authority. This keeps conditional rules (scope exceptions,
  notwithstanding clauses) whole in the body where they can be
  stated properly.
- **One row per distinct condition, one vector per instance.** A row
  is a malformed condition, not a requirement: each forbidden field
  value, each invalid index-entry state, each trailer field gate is
  its own row. Where one condition ranges over a list of fields — a
  u64 field outside its domain, a sum that overflows — the row names
  the fields inline rather than fragmenting, and the vector corpus
  enumerates the instances. Coverage is therefore finer than the
  table: as drafted, **122 rows over 226 instances**. A full
  enumeration preceding this decision produced 272 raw items before
  consolidation — near-duplicates and cross-products included — which
  is what made the row/instance split necessary rather than tidy.
- **Every row carries its detector and detection point** — reader or
  verifier, and open / layer access / tile use / extent use per the
  validation-timing rule (spec §19.2), or *certification* for rows the
  verifier detects, which that rule places outside the reader tiers —
  because the verifier-only rows are precisely the ones implementers
  overlook.
- **Non-violations are tabulated separately**: defined conditions
  that are not errors (an unknown ancillary record ignored, a
  sentinel entry read as fill, a coordinate outside the extents)
  get their own short table, both cleanroom rounds having shown
  fresh implementers conflating them with failures.
- **Gate G5 binds to instances:** every register row gets a
  conformance vector with an expected verdict for each field
  instance it names — a singular row, one vector; a row over twelve
  fields, twelve.

## Consequences

The register is the corpus's generation checklist, and its instance
count is the vector floor — 226, most of them one-byte variants of a
known-good file, which is the deliberate price of "every error has a
vector." Assembling it was the document's first whole-spec integrity
sweep, and it paid: eight defects surfaced in already-committed
sections, among them a user-metadata document whose ill-formed UTF-8
would have destroyed the whole file against ADR-0015's quarantine
principle, a detection tier that existed for no record extent, and
three requirements that assigned no detector at all. Foreclosed: a
register that quietly becomes the real specification, and rows so
coarse that conformance testing cannot distinguish the violations
inside them.

## Precedent

- HTTP's status-code registry as the derivative-index pattern:
  central lookup, defining sections authoritative.
- The QOI lesson this repository already applies (docs/research):
  divergence between "valid per spec" and "valid per implementation"
  is a spec bug — a per-violation corpus is what makes the two
  comparable.
- Both cleanroom rounds' finding that outcome and detector
  assignments are what fresh implementers most often guess at.
