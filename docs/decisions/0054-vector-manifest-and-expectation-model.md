# 0054. The manifest schema and what a vector expects of a reader

- Status: Accepted
- Date: 2026-08-10
- Covers: the fields of `conformance/vectors/manifest.json`; how decoded
  content is expressed; the pass/fail algorithm a harness implements
- Confirm: none

## Context

`[R-VEC-02]` fixes what a manifest entry records at minimum: an
identifier, whether the file is conforming, the decoded content a reader
returns from every scope it can read with floats as hexadecimal bit
patterns, and — for each structure the file damages — the outcome class,
the scope, and the register row exercised.

Turning that into a schema runs into `[R-CNF-12]`. Every vector built
from §21 is nonconforming, and for a nonconforming file no acceptance
obligation exists: a reader MAY reject it entirely upon detecting any
violation. So an entry recording only "reject-layer on layer `bad`"
describes an expectation that a reader rejecting the whole file also
satisfies. Without more, the corpus grades every reader on whether it
said no, not on what it refused.

## Decision

- **Expectation is a pair, not a verdict.** Each entry carries
  `must_not_serve` — the scopes no reader may serve data from — and
  `serves`, the content a reader that serves anything at all must
  return. `may_escalate_to` records the wider scope a reader is
  permitted to refuse instead, which is `"file"` for every register
  vector.
- **Decoded content is literal and formatter-independent.** Values are
  hexadecimal bit patterns of the sample's encoded bytes, per channel,
  per tile, in disk-ordinal order. A tile carries `stored: true|false`,
  so "returned fill" is distinguishable from "returned stored data that
  happens to equal fill" — a distinction `[R-TYP-08]` and `[R-TYP-09]`
  make load-bearing.
- **The pass/fail algorithm**, which a harness implements literally:
  1. Open the file. If the implementation reports failure for the whole
     file and the vector is nonconforming: **pass**, recorded as *scope
     untested*. Stop.
  2. For each `must_not_serve` scope, request data from it. Returning
     data is a **fail**; so is returning fill for a rejected tile
     (`[R-CNF-09]`). Reporting failure passes.
  3. For each `serves` entry, read it and compare bit patterns exactly.
     Any mismatch is a **fail**.
  4. For a conforming vector, step 1's whole-file rejection is itself a
     **fail** — no escalation licence exists for a conforming file.
- **Both axes are recorded independently**, as `[R-VEC-02]` requires:
  `conforming` is a property of the bytes, `violations` is a list, and a
  conforming file may still carry a record a reader ignores.
- **`derivation` records the recipe** — seed, patches, repairs — so the
  entry states not only what the file expects but how it came to be.

## Consequences

A harness can report two grades that the specification distinguishes and
a boolean cannot: *scope verified* for an implementation that read the
intact sibling and refused the damaged scope, and *scope untested* for
one that rejected the file. Both pass. Only the first is evidence about
scoping, and `[R-VEC-04]`'s intact-sibling rule is what makes the
distinction observable at all.

Priced knowingly. `serves` obliges the corpus to carry decoded content
for every readable scope of every vector, which is why vectors stay
small: the manifest is the only place that content exists, and a vector
with a million samples would have an unreviewable expectation. The two
guarantees §21.9 states at a scale no small file reaches — a 256 MiB
tile, 2³² addressed tiles — therefore record a digest of the canonical
decoded byte sequence rather than the samples themselves, and say so in
the entry.

The `serves` content is also the corpus's own weak point, since it is
authored rather than derived: a wrong expectation makes a correct reader
fail. ADR-0046 already fixes the remedy — the specification governs and
the vector is corrected — and this schema keeps the cost low by making
the expectation explicit enough to argue with.

Nothing here obliges an API shape. §2.4's note already says how failure
is reported is implementation technique; the algorithm above speaks of
*serving data from a scope*, which every reader can answer for itself.

## Precedent

- `[R-VEC-02]` and §24's Note, which state the narrowest-scope rule this
  schema mechanises.
- ADR-0010's retrofit of hexadecimal fill values, where JSON could not
  express a NaN payload — the same reason sample values are hex here.
- WebP's and PNG's conformance suites, which pair each file with expected
  decoded output rather than a bare accept/reject verdict.
