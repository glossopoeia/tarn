# 0038. Interleaved boolean values are single bytes

- Status: Accepted (supersedes ADR-0037's interleaved boolean cells;
  amends ADR-0012's uniformity clause)
- Date: 2026-08-04
- Covers: boolean representation in interleaved layers; scope of
  bit-packing; decoded-content strictness
- Confirm: none

## Context

ADR-0037 forbade bool channels in mixed interleaved layers to avoid
per-sample packed sub-fields. The maintainer challenged the
prohibition on adoption grounds, and the challenge is upheld:
co-located mask + value tuples are interleaved's core workload (point
clouds, pixel + QA records), so writers denied a bool type will
declare int8 — byte-identical storage with the type label erased —
and every downstream consumer inherits untyped 0/1 conversions the
format can never repair. The prohibition protected an aesthetic
invariant (no invalid decoded states) already qualified by the
padding-content rule, and a uniformity clause whose practical force
is small: decode paths branch entirely on layout, and the TIFF lesson
behind ADR-0012 concerns *unspecified* interactions — every cell here
is specified.

## Decision

- In an interleaved layer a bool channel is valid alongside any
  channels; each bool value occupies one byte of the sample tuple —
  0x00 = false, 0x01 = true — with element size 1 in the stride
  arithmetic. Representation keys on layout alone: bit-packing is
  planar-only, so an all-bool interleaved layer also uses bytes.
- Strictness mirrors the padding rule: writers MUST NOT emit any
  other byte; any other byte makes the file nonconforming, with the
  verifier as assigned detector (reject-tile); readers are not
  obligated to screen decoded content, and the general
  nonconforming-file license governs those that detect it.
- Packed planar planes are unchanged (⌈P/8⌉ bytes, LSB-first). A
  packed tile now has exactly one channel by construction, so pad
  bits carry the plane's channel's fill bit; ADR-0037's
  index-to-channel extension rule is withdrawn as moot.

## Consequences

Mixed tuples keep their schema types; libraries own the bool
conversion once instead of every application owning an int8 kludge;
the mask-compression story is untouched (planar). Priced consciously:
an all-bool interleaved layer is 8× packed size raw (multi-mask
compactness is the canonical planar case); a single-channel bool
layer is no longer byte-identical across layouts (the identity note
becomes numeric-only); and conforming-file content constraints now
exist in two places — padding and interleaved bool bytes — both
verifier-assigned. Spec requirement R-SER-04 is withdrawn and its
identifier permanently retired; the revised cells carry new
identifiers.

## Precedent

- Zarr's bool dtype (one byte per value) as ecosystem precedent for
  byte booleans in array interchange.
- ADR-0012's validity-table mechanism — this ADR moves one cell from
  writer-MUST-NOT to defined.
- TIFF SampleFormat's dangerous default — unsigned integer assumed
  wherever the tag is absent or ignored — as the guessed-type
  cautionary tale; and the bool-less raster stacks that store masks
  as 8-bit integer bands as the type-erasure outcome this decision
  prevents: a format that makes the honest type inexpressible gets
  the dishonest one.
- ADR-0037's padding-content enforcement pattern, reused verbatim.
