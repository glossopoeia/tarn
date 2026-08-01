# 0028. Degenerate geometry: zero extents valid, everything else bounded

- Status: Accepted
- Date: 2026-07-30
- Covers: geometry validity floor (rank, extents, tile extents, channel
  count); adds requirement-ID prefixes MDL (§3) and GEO (§11)
- Confirm: none

## Context

The undefined-behavior worklist demands a defined answer for zero-size
dimensions, zero channels, and empty layers — the boundary cases where
implementations silently diverge. Two of the four calls are forced: a
zero tile extent is a division by zero, and a zero-channel layer has no
sample content. The genuine choices were zero extents and rank zero.
Zero-extent dimensions make empty layers valid, which is what
schema-first workflows need — declare layers up front, grow extents as
data arrives — and extent growth is already a blessed metadata-only
operation (ADR-0010) that composes naturally with the append model
(ADR-0017); NumPy and Zarr both treat zero-size arrays as valid. Rank
zero (scalar layers) degenerates cleanly in the math but adds a special
case to every worked formula for a shape expressible as a one-extent,
one-dimension layer.

## Decision

- **Extents:** Eᵢ ≥ 0. A dimension with extent 0 yields a grid count of
  0, zero addressed tiles, and an empty reference array — a valid,
  empty layer.
- **Tile extents:** Tᵢ ≥ 1, and a tile extent MAY exceed its dimension's
  extent (the grid is then a single padded tile; also required for
  growth from small extents without retiling).
- **Rank:** d ≥ 1. No zero-dimensional layers.
- **Channels:** C ≥ 1.

Violations (rank 0, any tile extent 0, channel count 0) are validity
errors at layer scope: writers MUST NOT emit them; readers MUST
reject-layer.

Housekeeping under spec §2.2: requirement-ID prefixes `MDL` (terminology
and data model, §3) and `GEO` (layers, dimensions, and tiling, §11) are
added to the registry of prefixes.

## Consequences

Empty layers are first-class, so declare-then-fill workflows need no
placeholder extents; the N = 0 case gets a conformance vector and one
sentence per formula rather than an error path. Foreclosed: scalar
(rank-0) layers — a future demand would arrive through a minor-version
record extension, not a reinterpretation.

## Precedent

- NumPy and Zarr zero-size arrays as ecosystem expectation.
- ADR-0010 (growth as metadata-only) and ADR-0017 (append model) as the
  workflows zero extents serve.
