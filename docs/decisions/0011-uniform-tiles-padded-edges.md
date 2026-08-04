# 0011. Uniform tile sizes with padded edge tiles

- Status: Accepted
- Date: 2026-07-29
- Covers: tiling geometry; edge-tile handling; padding content
- Confirm: padding content fixed by ADR-0037 (fill-encoded padding
  samples and pad bits; Q-C4).

## Context

When a dimension's extent is not a multiple of its tile size, a format must
choose: truncated edge tiles (every tile a different byte size; GPU upload
paths and stride arithmetic get per-tile special cases) or uniform tiles with
padded edges (every tile identical in shape and stored size; edge handling
becomes a read-side clip). Uniform tiles are the GPU-friendly choice and the
one Zarr's regular chunk grid settled on. The trap is leaving padding
*content* unspecified: don't-care bytes participate in compression and
checksums, so unspecified padding makes byte-identical logical data produce
different physical files — breaking reproducibility, deduplication, and
content-addressing. Boundary conditions left implicit are exactly where
implementations diverge.

## Decision

All tiles in a layer have identical logical shape; edge tiles are stored
full-size. Tile counts per dimension use ceiling division, stated with a
normative formula and a worked example. Padding samples have normatively
defined content (recommended: the channel's fill-value encoding, so every
sample in a decoded tile is meaningful; alternative under Confirm: all-zero
bytes). Padding is covered by compression and checksums like any other tile
content, and reads clip to the logical extent — padding is never returned as
data. Tile-size guidance (~1–16 MiB for GPU streaming and remote reads) is a
non-normative sidebar, not a requirement.

## Consequences

Every tile shares one decode path and one stored size (before compression);
slab and alignment arithmetic stay trivial; deterministic padding makes
writer output reproducible. Writers must materialize defined padding into
edge tiles — a small, bounded cost.

## Precedent

- Zarr v3 regular chunk grid (uniform chunks, edge semantics defined at the
  array boundary).
- The determinism lesson: unspecified don't-care bytes break checksum and
  content-addressing determinism (QOI boundary-case analysis,
  `docs/research/reference-format-lessons.md`).
- TIFF's normative-text hygiene counterexample ("about 8K seems to work
  well") for keeping sizing advice out of requirements.
