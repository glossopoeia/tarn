# 0012. Interleaved and planar layouts as one enumerated mode with a full validity table

- Status: Accepted
- Date: 2026-07-29
- Covers: channel layout; cross-field validity; boolean representation
- Confirm: (a) planar disk-tile ordering — channel-major (recommended: a
  whole channel's tiles form one contiguous, slab-friendly run) vs
  spatial-major; (b) boolean representation — bit-packed LSB-first uniformly
  in both layouts (recommended) vs one byte per boolean (see OPEN-QUESTIONS
  Q-B3, Q-D6).

## Context

Both layouts earn their place: interleaved serves full-sample window reads;
planar serves single-channel scans and shuffle-style compression. The danger
is not the pair — it is specifying each field independently and leaving the
cross-product to inference. TIFF's PlanarConfiguration is the canonical case:
its interaction with photometric interpretation and sample counts was left
underspecified ("this field is irrelevant if SamplesPerPixel is 1, and it is
not required"), and readers diverged for decades. Any representation that
differs between layouts (packed booleans being the classic) multiplies that
risk.

## Decision

Per-layer layout is a two-value enum: **interleaved** (channel values adjacent
within each sample) or **planar** (each channel tiled separately). The spec
contains a normative validity table over layout × channel count × codec ×
filter × boolean representation × fill: every cell is either defined, or
writer-MUST-NOT paired with reader-MUST-reject. No cell is left to
inference, and the single-channel case is degenerate-but-defined in both
modes rather than "irrelevant." Planar disk-tile ordering is fixed normatively (one order, no
writer choice). Boolean representation is uniform across both layouts —
recommended: bit-packed, LSB-first (bit position = in-tile sample index
mod 8), final-byte pad bits defined, with the exact choice under Confirm.
In-tile sample ordering follows the linearization order decided in
OPEN-QUESTIONS Q-B2 and is stated with a worked byte-offset example for each
layout.

## Consequences

Implementers get an exhaustive table instead of a folklore matrix; the
test-vector surface doubles for layout-sensitive cases, priced deliberately.
Fixing planar ordering normatively is what makes "slab = a contiguous run in
a known order" meaningful for planar layers at all.

## Precedent

- TIFF PlanarConfiguration × PhotometricInterpretation × SamplesPerPixel —
  the underspecified-interaction disaster this ADR exists to prevent.
- QOI's rule that every non-obvious encoding carries a worked numeric
  example.
