# 0006. Consolidated metadata directory, reachable in O(1) round trips

- Status: Accepted (the requirement); Proposed (placement — footer vs
  headers-first), resolved via OPEN-QUESTIONS Q-A1/Q-A2
- Date: 2026-07-29
- Covers: metadata layout; remote-read cost model
- Confirm: placement (see Q-A1), discovery byte budget (Q-A3), and
  indirection depth (Q-A4).

## Context

For a format whose stated use includes plain HTTP range requests, the number
of round trips to open a file is a first-class design property, not an
implementation detail. Metadata scattered through the file behind chained
pointers costs one serial request per hop, and each hop's latency is the
dominant cost of remote open. PMTiles proves the alternative and makes it
*testable*: a fixed-size structure at a spec-constant location, a normative
size budget for the root directory, and a hard bound on directory depth turn
"efficient remote open" into a conformance property. Cloud-optimized GeoTIFF
spent years as the counterexample — locality by convention, with no
normative requirement tools could rely on, until later OGC standardization
addressed it — proving that the guarantee belongs in the spec from day one.

## Decision

All metadata for all layers — names, dimensions, channels, codec and layout
declarations, fill values, and the locations of per-layer tile indexes — lives
in one consolidated, checksummed directory. The spec states cold-read
accounting normatively: a conforming file's complete metadata is reachable in
O(1) round trips, with the exact request sequence (discovery fetch →
directory → at most one spill hop for an oversized per-layer tile index →
payload) written into the spec as a guarantee, PMTiles-style. All layers are
equally first-class: there is no "readers need only process the first entry"
escape hatch. Whether the directory anchors at a footer, a front header, or a
hybrid (tiny front magic + authoritative trailer) is an open question gated
on the mutability contract (Q-A2), because a front directory forces in-place
rewrites on every append.

## Consequences

Remote open becomes a constant-request operation independent of layer and
tile count, and the claim is testable against a dumb HTTP server. Writers
accept either a suffix/prefix byte budget achievable in one pass or a
specified spill mechanism — the spec must choose one and say so.

## Precedent

- PMTiles v3: fixed 127-byte header, 16 KiB root-directory budget, bounded
  leaf depth, "at most N requests of overhead" phrasing.
- Cloud-optimized GeoTIFF's convention-first years as the
  locality-by-convention cautionary tale.
