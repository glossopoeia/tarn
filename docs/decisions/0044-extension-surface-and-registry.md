# 0044. The enumerated extension surface and its registry

- Status: Accepted (resolves Q-G3)
- Date: 2026-08-05
- Covers: the extension surface §10 enumerates; numeric ID-space
  partitioning; the experimental lane; registration requirements and
  where the registry lives
- Confirm: none

## Context

Extension governance fails in two directions, and both are on the
record. TIFF's registration mailbox was decommissioned while its
"reusable" private tag range guaranteed collisions; formats with so
much process that nobody registers get the same outcome by the other
road. PNG's balance — a registry-governed public space, a
syntactically distinct private lane, and the rule that unregistered
public identifiers never ship — is the one that held for thirty
years. This specification has already been drafting toward it: every
enum it defines carries reserved and experimental ranges pointing at
§10, so what remained was to state the rules those pointers assume.

## Decision

- **The surface is closed and enumerated.** Growth happens through
  exactly four vehicles (`[R-ENC-07]`): new record types, new values
  in ranges this specification reserves, new ignore-lane flag bits,
  and new standardized user-metadata keys. Anything else — a new
  fixed field, a widened structure, a reinterpreted value — is a new
  format major version.
- **Every numeric ID space is partitioned the same way:** assigned
  values; a reserved range this specification alone assigns from;
  and a high experimental range (≥ 0x8000 for `u16` spaces, ≥ 0x80
  for `u8` spaces). §10 tabulates all of them in one place, since
  they were defined section by section.
- **The experimental lane is for private use and carries no
  collision protection** — two experiments MAY choose the same
  value. Writers MUST NOT ship files carrying experimental values in
  released software or published data, and an unregistered value
  from a reserved range MUST NOT ship at all: that is the failure
  the lane exists to absorb.
- **Registration requires** an unambiguous specification of the
  value's semantics, a security review, and — for record types — the
  MU/PE assignment justified against ADR-0026's banned-ancillary
  criterion: a type registers MU = 0 only if ignoring it leaves every
  stored sample bit-exact and every geometry identical.
- **The registry is a machine-readable file in this repository**,
  versioned with the specification (`spec/registry.json`), with
  Appendix C carrying a snapshot; where it and the spec's own tables
  diverge, the defining section governs — the registry is
  convenience, never a second authority. A registry living anywhere
  else is one that can be decommissioned out from under its format.

## Consequences

An implementer learns every extension point from one section instead
of inferring it from eight enums. Experiments are expressible without
touching the public space, and the format has a stated answer to
"what if two extensions collide" — for the reserved ranges, the
registry prevents it; for the experimental lane, nothing does, which
is why those files stay private. Foreclosed: silent semantic drift in
assigned values, and any extension mechanism that grows fixed
structures.

## Precedent

- PNG's registration discipline as this repository already sources
  it (docs/research/reference-format-lessons.md): §5.4's
  case-distinguished private lane and reserved-bit tolerance,
  §12.10.1 and §14.1 for private-chunk use and the prohibition on
  unregistered public types in released software — the mechanism,
  without the case-encoding trick ADR-0026 already rejected.
- TIFF's decommissioned registry and colliding private range as the
  failure mode this design is shaped against.
- Zarr's `must_understand` and IANA-style registry practice for the
  review requirements.
