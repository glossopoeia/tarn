# 0021. Planar tile ordering: channel-major

- Status: Accepted (resolves Q-B3; finalizes ADR-0012's planar-order Confirm
  and ADR-0020's composition formula)
- Date: 2026-07-30
- Covers: planar disk-tile ordinal assignment; index entry order
- Confirm: none

## Context

Planar layout exists to serve channel-wise access (ADR-0012); the open
question was whether its tile ordinals group by channel or by spatial tile.
The worked read patterns are decisive. Channel-major makes a whole channel
one contiguous ordinal run — a single range request or direct read for a
full-channel scan — and serves channel *subsets* exactly (three bands from
a twelve-band layer fetch precisely those bytes). Spatial-major turns the
same scan into one strided read per spatial tile (65,536 reads at 4 MiB
stride in the worked example) or a factor-C byte amplification, and its one
winning pattern — every channel of a window — is precisely the workload
interleaved layout already serves. Channel-major also keeps index-segment
fetch amplification at 1× rather than C× for single-channel readers, and it
is the conceptually consistent end of the axis interleaved starts:
interleaved is channel-fastest at sample granularity; planar is
channel-slowest at tile granularity.

## Decision

For a planar layer with N spatial tiles (per ADR-0020's row-major spatial
ordinal s) and C channels, the disk-tile ordinal is:

> **ord(c, s) = c · N + s**

— equivalently, the channel behaves as an implicit outermost (slowest)
dimension. This governs index entry order; physical byte contiguity is
promised only where a slab declaration (ADR-0022) is made, so streaming
writers with interleaved sources may place tiles physically in acquisition
order at the cost of the slab flag, never of conformance. Interleaved
layers use the spatial ordinal alone.

Extent-growth honesty (applies to either ordering, recorded here): growing
a layer's extents renumbers ordinals and requires re-emitting that layer's
entire index region in the new commit (≈ 20 B × C × N′ plus segment CRCs);
ADR-0010's "growth is metadata-only" remains true — no payload bytes are
rewritten — but carries this index cost, and growth clears the layer's slab
declaration unless the writer re-establishes it (ADR-0022).

## Consequences

Single-channel scans, GPU plane uploads, and band-subset reads are
contiguous or exact; all-channel window readers should choose interleaved
layout, which exists for them. The spec's worked-example table gains one
planar row. Writers streaming interleaved sources buffer index entries
(not payloads) until commit — entries are emitted in ordinal order at
commit time per ADR-0017's write ordering.

## Precedent

- ADR-0012's own logic: the two layouts as the two ends of one
  channel-position axis.
- The band-interleaved-by-sequence vs band-sequential distinction long
  established in raster formats, resolved here toward band-sequential for
  the planar mode.
