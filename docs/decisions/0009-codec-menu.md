# 0009. Closed codec menu plus an orthogonal byte-shuffle filter

- Status: Accepted
- Date: 2026-07-29
- Covers: compression codecs; filters; codec boundary contract
- Confirm: none — the internal metadata codec is fixed by ADR-0032
  (none or zstd for directory and user metadata; the tile index is never
  compressed).

## Context

Codec history in container formats is a history of two failure modes. The
first is optionality: when codecs are optional, readers support different
subsets and files stop interchanging. The second is boundary violation: TIFF's
old-style JPEG wove codec state into the container (pointers from tags into
compressed stream interiors, shared tables outside the strips) and had to be
abandoned by technical note; PNG's single deflate stream across the whole
image forecloses random access to regions. TIFF's LZW shipped with two
incompatible bit-order interpretations. The rule that survives: a codec
consumes exactly the tile payload and nothing else, and every codec is pinned
to one exact external definition.

## Decision

A closed list, all reader-MUST: **none**, **deflate** (RFC 1951), **zstd**
(RFC 8878), **LZ4**. Each compressor earns its slot: deflate is the
one codec browsers decode natively (DecompressionStream); zstd is the
modern ratio/speed default; LZ4's near-memcpy decode throughput serves the
GPU-streaming and direct-I/O read paths, with wide precedent in
array-storage ecosystems (HDF5/Blosc, Zarr). Wrapper-level framing for each
(raw DEFLATE vs zlib; zstd dictionary policy; LZ4 frame vs block) is pinned
during drafting under OPEN-QUESTIONS Q-E1 — one exact external definition
per codec, chosen by the test "does the container already provide what the
wrapper adds?" One orthogonal filter slot: **byte-shuffle** (element-size
stride), with composition fixed as shuffle-then-compress. LZW is excluded.
Compression levels and encoder strategies are writer-side runtime knobs and
are never persisted.

The boundary contract is normative: every stored tile is independently
decodable from its stored bytes plus layer metadata alone — no cross-tile
state, no pointers from metadata into payload interiors, no side tables.
Slabs are an I/O grouping and never a compression context. Decoded size is
fully determined by declared geometry, so readers allocate from geometry and
treat codec output exceeding it as an error (structural decompression-bomb
defense). Unknown codec ID: reject exactly the layers that use it, never the
file. Codec IDs live in the registry with a reserved private/experimental
range (ID-space design under OPEN-QUESTIONS Q-G3).

## Consequences

No optional codecs means no reader dialects, and a four-entry
all-reader-MUST list is a deliberate forever obligation — the price of the
no-dialects guarantee, paid once here rather than re-litigated per codec.
Each codec ships with a normative external reference and byte-exact test
vectors. Adding a codec later is a registry + minor-version event with a
defined degradation story, not a fork.

## Precedent

- TIFF old-style JPEG (TTN2) — the codec-boundary autopsy; TIFF LZW's dual
  bit-order incompatibility.
- PNG's single-IDAT-stream random-access loss; PNG §4.11-style closed
  extension surface.
- Zarr's codec-chain model (consciously simplified here to one filter + one
  codec) and its write-strategy rule: writer knobs are not file format.
