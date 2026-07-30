# 0019. Remote-open model: two-request baseline, suffix-fetch optimization

- Status: Accepted (resolves Q-A3 and Q-A4)
- Date: 2026-07-29
- Covers: cold-read accounting; discovery byte budget; indirection depth
- Confirm: none

## Context

The O(1)-reachability requirement (ADR-0006) needs a concrete, testable
shape. Two candidate shapes were analyzed: a normative suffix *window* (one
speculative fetch of the last W bytes retrieves trailer + directory when the
directory fits) and a plain two-step sequence (fetch the 64-byte trailer,
then fetch the directory at the exact offset/length the trailer states).
The maintainer chose to center the two-step sequence: it is the simplest
correct remote reader — two straight-line requests, no window-containment
arithmetic, no clamping edge cases — which serves the weekend-implementable
gate directly. The window survives as an optimization, which composes
cleanly because the trailer always carries exact directory coordinates.

## Decision

- **Normative baseline:** a reader opens a file by (1) reading the final
  64 bytes and verifying the trailer, then (2) reading the directory as one
  exact-range request using the trailer's offset and length. Every
  subsequent hop is likewise exact: directory entries state each tile
  index's offset/length; index entries state each tile's. No step ever
  scans or guesses.
- **Accounting, stated normatively as serial depth:** complete metadata at
  serial depth ≤ 3 (trailer → directory → tile index); first tile at
  serial depth ≤ 4. Per-layer index fetches beyond the first are parallel,
  one per layer touched. Backends without suffix-range support (or servers
  answering 200 to Range requests, which readers MUST detect) add one
  request.
- **Sanctioned optimization:** a reader MAY fetch the final 64 KiB in one
  speculative request; whether the directory (and any tile index) lies
  inside the returned buffer is decided by arithmetic on the trailer's
  fields — no flags. Writers SHOULD keep padding + directory + trailer
  within 64 KiB (≈290 typical layer entries) so the speculative open
  succeeds; small files then yield **all** metadata, indexes included, in
  a single request, and the first tile at serial depth 2.
- Files whose directories exceed the window are fully conforming; they
  cost the baseline sequence, never more.

## Consequences

The G2 reader is two requests of plain code; sophisticated readers get
single-request opens on typical files without any new format surface. The
64 KiB figure binds writers (SHOULD) rather than defining validity, so
layer count is never capped. Conformance vectors can pin both paths: a
baseline open transcript and a speculative open against the same file.

## Precedent

- PMTiles v3's normative prefetch budget and bounded directory depth — the
  testable-guarantee register, with the budget relaxed from validity-
  defining MUST to interoperability SHOULD.
- Cloud-optimized GeoTIFF's convention-first years as the cautionary tale
  for leaving the accounting unstated.
- RFC 7233 Range semantics (suffix clamping, 200-vs-206) as the transport
  facts the reader rules encode.
