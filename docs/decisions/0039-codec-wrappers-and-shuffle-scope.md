# 0039. Codec wrapper pinning and the shuffle stride rule

- Status: Accepted (resolves Q-E1 and Q-E2; fixes ADR-0009's wrapper
  framing; discharges cleanroom round 2's §17 deferrals)
- Date: 2026-08-04
- Covers: exact external definition per codec; zstd frame policy;
  filter stride rule and layout scope; codec IDs; decode-failure and
  verifier obligations
- Confirm: none

## Context

ADR-0009 fixed the codec menu and left the framing layer to one test:
strike whatever the wrapper adds if the container already carries it.
The container carries a per-tile CRC-32C, the stored length (index),
and the decoded length (geometry) — so redundant wrapper checksums
and sizes fail the test, but framing that every library binding emits
by default passes on adoption grounds. Separately, Q-E2 asked whether
byte-shuffle earns interleaved scope; measurements on representative
interleaved data (float32 x/y/z + class records, four-channel uint16;
method and full numbers in docs/research/shuffle-measurements.md)
showed 28–33% compressed-size reduction with stride = sample stride —
comparable to the planar win — so the benefit materializes.

## Decision

- **Codec IDs sequential, house pattern:** 1 = none, 2 = deflate,
  3 = zstd, 4 = lz4; 0 invalid; 5–0x7FFF future assignment;
  ≥ 0x8000 experimental. All four core, reader-MUST.
- **none:** stored bytes are the filtered image verbatim; the index
  length MUST equal the decoded size — a pre-fetch cross-check.
- **deflate:** exactly one raw DEFLATE stream (RFC 1951) — no zlib
  (RFC 1950) or gzip wrapper; the checksums and headers they add
  (zlib's Adler-32, gzip's CRC-32 and size trailer) are redundant
  with the container, and browsers decode raw natively.
- **zstd:** exactly one RFC 8878 compressed frame — skippable or
  extra frames reject-tile, enforced by a frame-boundary check
  since whole-buffer decoders tolerate them — minimal-strict:
  dictionary use, the content-checksum flag, and a declared window
  exceeding the decoded size are writer-MUST-NOT and
  reader-reject-tile (all zero-friction against libzstd defaults);
  the frame content-size field MAY be present because libzstd emits
  it by default, MUST equal the decoded size when present, and is
  never an allocation source. The minimum window a reader must
  support is a limits-table row.
- **lz4:** exactly one raw LZ4 block (Block Format Description
  v1.0, revision pinned in Appendix F); the block contract (stored
  length in, decoded capacity out) is the container's own model, and
  the frame format's magic, sizes, and checksum are all redundant.
  Decoded tile size capped at 0x7E000000 bytes under this codec —
  the format's practical interoperability bound, reject-layer.
- **Filter stride rule, no special cases:** byte-shuffle transposes
  the image as n = L/s groups of s bytes; s is the channel's element
  size for a planar plane and the sample stride Q for an interleaved
  tile. A packed bool plane gets s = 1 — the identity — so the
  layout × filter validity table has no forbidden cell. Composition
  stays shuffle-then-compress (ADR-0009).
- **Failure and obligations:** a malformed stream, output not
  exactly the decoded size, trailing stored bytes past the stream,
  or a forbidden frame feature → reject-tile. No stored-vs-decoded
  expansion bound exists; allocation is geometry-only, resource caps
  are the limits table's business. A verifier that cannot decode a
  layer's codec cannot certify the file (the §9.7(d) pattern). Every
  codec's output for nonempty input is nonempty and no decoded size
  is zero, grounding the index rule that no stored tile is
  zero-length.

## Consequences

Weekend implementations use stock library APIs with documented
options — zlib's raw-windowBits mode or
DecompressionStream('deflate-raw'), libzstd defaults plus a
frame-boundary check on decode, the LZ4 block API — with no
nonstandard API use anywhere. Conforming tiles have one *framing*
per (codec, filter) choice — wrapper variance is gone, while
encoder output stays level- and library-dependent per ADR-0009 —
and the strict frame policy is testable with cheap header checks
plus one frame-boundary query. Interleaved
workloads keep the measured 28–33% shuffle gains. Foreclosed:
dictionaries (cross-tile state by another name), wrapper checksums,
and multi-frame or multi-stream payloads.

## Precedent

- TIFF old-style JPEG (codec state woven into the container) and
  PNG's single-IDAT random-access loss behind the per-tile boundary
  contract (ADR-0009).
- Browsers' `DecompressionStream('deflate-raw')` and the zlib-vs-raw
  redundancy audit for the deflate pinning.
- HDF5/Blosc and Zarr shuffle precedent, extended to interleaved
  stride by direct measurement.
- RFC 8878's own decoder-resource guidance, left governing (window
  handling is not re-specified).
