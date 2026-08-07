# 0046. The conformance corpus is derivative evidence

- Status: Accepted
- Date: 2026-08-06
- Covers: what §24 promises about the vector corpus; the manifest
  contract; precedence between a vector and the specification
- Confirm: none

## Context

A conformance corpus can play two roles, and the choice decides what
a bug in it costs. If passing the vectors defines conformance, then
correctness is mechanically testable — and a wrong expected verdict
in one vector makes every correct implementation nonconforming until
the corpus is fixed, so the corpus needs the same change control as
the specification. If the vectors are evidence, the specification
text stays the authority and a disagreeing vector is a corpus bug.
This project already faced the identical question for the error
register and answered it (ADR-0042): completeness is normative, each
row restates its rule, and the rule governs.

## Decision

- **The corpus is derivative.** A conforming implementation is one
  that satisfies this specification's requirements; where a vector's
  expected verdict and the specification disagree, the specification
  governs and the vector is corrected. Vectors are how conformance is
  *demonstrated*, never how it is *defined*.
- **Coverage is the normative claim** the corpus makes about itself,
  inherited from `[R-ERR-02]`: every error-register row has at least
  one vector per instance it names, and every sentinel and boundary
  has one. A missing vector is a gap in the corpus, never a licence
  to skip the check.
- **Every vector carries a machine-readable expectation**: for a
  valid file, the decoded content it must yield, with floating-point
  values written as hexadecimal bit patterns so no comparison depends
  on a formatter; for an invalid file, the outcome class, the scope,
  and the register row it exercises.
- **The corpus lives in `conformance/`** with a JSON manifest,
  versioned with the specification, and is licensed CC0 (ADR-0016) so
  that using it imposes nothing on an implementation.

## Consequences

Implementers get a runnable check that costs them no legal or
governance entanglement; the project gets G5 as a measurable gate
rather than an aspiration. Priced knowingly: a passing implementation
is evidenced, not certified — the corpus can only exercise what
someone thought to write, which is why §24 states plainly that
passing it is necessary evidence and not sufficient proof.

## Precedent

- ADR-0042's derivative register, for the identical precedence
  question one layer up.
- The QOI lesson this repository already carries: divergence between
  "valid per spec" and "valid per implementation" is a spec bug — a
  corpus makes the two comparable, which only works if the spec is
  the fixed point.
- Hex bit patterns for float expectations, the retrofit Zarr needed
  when JSON fill values could not express NaN payloads (ADR-0010).
