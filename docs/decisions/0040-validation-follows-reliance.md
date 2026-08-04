# 0040. Validation follows reliance

- Status: Accepted (discharges cleanroom round 1's validation-timing
  deferral and round 2's duplicate-name-timing deferral)
- Date: 2026-08-04
- Covers: when a reader detects violations, per owning scope; the
  duplicate-name detection point; the shape of §19's algorithms
- Confirm: none

## Context

The conformance machinery assigns every violation an outcome but not
a moment: both cleanroom rounds found implementers guessing whether a
reader serving one layer must validate the others. Timing left to
discretion is acceptance nondeterminism — two readers disagree on the
same file depending on what they happened to read — the divergence
class the outcome model exists to kill. Fully eager validation buys
nothing observable (only earlier failure on unused layers) at open
cost proportional to layer count; fully lazy validation makes the
layer-name namespace path-dependent, so lookup-by-name stops being a
function.

## Decision

A reader detects each violation readers are obliged to detect —
verifier-assigned checks impose no reader obligation — no later than
its **first reliance** on the structure carrying it:

- **at open:** the front signature block (local readers), the
  trailer, the directory region and its record walk — multiplicity
  and non-layer extent-slot rules included — and the layer-name
  namespace. Duplicate layer names are reject-file at open, before
  any data is served — one length-prefixed name parse per record,
  in a region already resident and CRC-verified.
- **at first layer access:** full validation of that layer's
  record — extent slot and payload: constraint set, exact parse,
  value sets, fill constraints, geometry floor and arithmetic,
  I/O-free index cross-checks — before any use of the layer's
  declarations; no fetch is involved.
- **at tile use:** the index-chain, payload-CRC, and decode checks
  before any sample of that tile is returned; index-chain failures
  take layer scope although detected here.

Earlier detection is always permitted (the nonconforming-file rule);
later is forbidden — a reader never returns data whose governing
structure has not passed its tier's validation. Structures a request
never relies on impose no obligation beyond the open steps: a
violating record in an unaccessed layer leaves every other layer's
reads conforming. The open consumes the trailer and directory only,
preserving the two-request accounting at any layer count.

## Consequences

The latest detection point is deterministic — divergence under the
earlier-detection license is only ever toward earlier rejection of
nonconforming files, never toward silent acceptance — and the
blast-radius model gains a time dimension at zero I/O cost. §19
encodes the open and tile-read algorithms as numbered steps and
layer access as a single validation obligation, each citing the
rule whose outcome governs its failure. The error register (§21)
inherits a defined detection point for every reader-detected row.
Foreclosed: reader-discretion timing, and any open procedure whose
cost grows with file size.

## Precedent

- The outcome-class blast-radius model (ADR-0003) extended to time.
- PMTiles' fixed open sequence as the deterministic-open precedent.
- The cleanroom lesson (ADR-0034, both rounds): fix the spec wherever
  a fresh implementer had to guess — both rounds guessed here.
