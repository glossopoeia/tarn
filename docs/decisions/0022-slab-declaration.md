# 0022. Slab: a declared layout guarantee, uniform every S tiles

- Status: Accepted (resolves Q-B1)
- Date: 2026-07-30
- Covers: slab semantics; contiguity declaration; slab alignment
- Confirm: none

## Context

Two designs were on the table: the slab as a *declared layout invariant*
over an unchanged per-tile index, or the slab as an *index granularity*
(per-slab offsets with per-tile lengths). The size motivation for the
latter died with the segmented index (ADR-0024): 20 B/tile is 0.002%
overhead on megabyte tiles and no reader fetches an index whole anymore —
while index-granularity would cost a second index format, a second sentinel
encoding, and O(S) intra-slab arithmetic in a weekend-implementable spec.
A reader holding index entries can always *detect* contiguity
arithmetically; what detection cannot give is a layer-wide promise known
before any index bytes are fetched — the fact a GPU planner needs to commit
pinned plane-sized buffers and one direct read per channel. Declared,
verifier-checkable layout invariants are the established pattern
(ADR-0005; PMTiles `clustered`).

## Decision

A layer MAY carry a **slab declaration `(S, A_slab)`** in its core layer
record (never an ancillary record): every run of S consecutive
linearization-order tiles (ADR-0020/0021 ordinals) has its stored tiles
physically contiguous and packed in ordinal order, and each run's first
stored byte satisfies `offset mod A_slab == 0` (A_slab a power of two).
Sentinel tiles are transparent to run continuity: a run's *stored* tiles
are contiguous; its *addressed* tiles need not all be stored. Runs MUST
NOT span planar channel blocks; the final run per channel may be short.

**Slab and per-tile alignment are mutually exclusive per layer.** The slab
invariant packs interiors (no inter-tile gaps), which is incompatible with
ADR-0005's every-tile alignment except in degenerate cases; a layer
declares one or the other, and the layouts × alignment × slab validity
cell in ADR-0012's table records the combination rules explicitly.

Honesty under mutation (ADR-0017): a writer that supersedes a tile in, or
grows the extents of, a slab-declared layer MUST either re-establish the
invariant for the affected runs or clear the declaration in the new
generation. Tools that modify a layer MUST fully parse its layer record
(ADR-0026's updater obligations), so the declaration cannot go silently
stale. Verifiers check the invariant; readers may ignore the declaration
entirely — offsets remain explicit in the index (reader-invisible option).

## Consequences

Direct-I/O and GPUDirect consumers get a plannable, checkable guarantee at
the cost of one declaration and ~six invariant sentences; the index format
stays single. Arithmetic contiguity detection remains available to readers
of undeclared layers. Foreclosed: per-slab index granularity — revisitable
only through the reserved index-encoding enum (ADR-0024) if evidence
demands it.

## Precedent

- ADR-0005: declared invariants over writer folklore; reader-invisible
  options as the cheapest option class.
- PMTiles `clustered` — a layout promise as a checkable flag.
- Zarr sharding-indexed as the index-granularity road considered and not
  taken (its guarantees arrive here via contiguity + the segmented index
  instead).
