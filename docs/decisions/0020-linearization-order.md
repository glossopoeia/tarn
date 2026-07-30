# 0020. Linearization: row-major via a reserved enum

- Status: Accepted (resolves Q-B2)
- Date: 2026-07-29
- Covers: sample/tile/index linearization; future ordering extensions
- Confirm: none — planar composition formula finalized by ADR-0021

## Context

Linearization — the mapping from declared dimension order to byte order —
governs in-tile sample layout, tile-grid ordinals, and index entry order;
slab contiguity and range coalescing are defined against it, so it cannot
be implementation-defined. The ecosystem survey is lopsided: NumPy, CuPy,
PyTorch, TensorFlow, JAX, HDF5, netCDF, Zarr, GeoTIFF, WebGPU, and CUDA are
row-major (fixed or default); Julia, MATLAB, and Fortran are column-major.
Zarr ran the configurability experiment: v2 shipped a writable C/F order
field, third-party F-order support fractured, and v3 deleted the field.
Column-major ecosystems consume row-major formats today by declaring
dimensions reversed at the binding layer (HDF5, netCDF) — identical bytes,
relabeled axes, zero copies.

## Decision

Each layer carries a **u16 linearization field**: value 0 is invalid
(zeroed bytes can never masquerade as a defined order); value 1 =
**row-major** — the last-declared dimension varies fastest — and is the
only value writers may emit in v1; values 2 and 3 are reserved for Morton
and Hilbert tile orderings **without any normative semantics** (readers
reject-layer on them, per the scoped-criticality rule); values ≥ 0x8000
are the experimental lane (Q-G3). The field governs tile-grid ordinal
assignment and index entry order. **Decoded in-tile sample order is fixed
row-major unconditionally and permanently** — a future curve reorders
tiles, never bytes within a tile, so tile decodability from stored bytes +
layer metadata is untouched. For planar layers the index ordinal composes
as channel-block × spatial-ordinal, with the exact formula finalized by
Q-B3's planar-order decision. Non-normative notes carried into the spec:
linearization fixes the declared-order→byte mapping only — axis direction
and orientation are semantics for user metadata (Q-F3); column-major
writers achieve zero-copy storage by declaring dimensions reversed (worked
example included, alongside the coordinates→ordinal→byte-offset table).

## Consequences

Every v1 reader implements exactly one order plus one reject branch — two
bytes and one comparison. The Hilbert door stays open for the workload that
genuinely wants it (interactive 2D pan/zoom over range requests, where
compact windows coalesce into few runs and index deltas shrink — the
PMTiles result) as an additive registry entry rather than a fork. Sphere
pixelizations (HEALPix) need no enum value: they are a different grid, not
a different ordering — a HEALPix map is stored as a 1-D layer of
12·Nside² pixels (NESTED numbering gives sky-locality) with its parameters
under registered metadata keys; logged as a candidate standardized-key
registry entry.

## Precedent

- Zarr v2→v3: the configurable-order field's removal, and the transpose
  codec as its demoted replacement.
- HDF5 and netCDF: row-major-fixed formats serving column-major language
  communities via reversed declaration, for decades.
- PMTiles v3: Hilbert tile IDs as the proven locality/compression payoff
  that justifies reserving curve IDs; its in-tile raster order staying
  fixed inside curve-ordered tiles is the same tiles-not-bytes split.
