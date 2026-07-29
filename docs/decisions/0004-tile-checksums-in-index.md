# 0004. Per-tile checksums live in the tile index and cover stored bytes

- Status: Accepted
- Date: 2026-07-29
- Covers: tile integrity; payload framing
- Confirm: none for placement; the checksum algorithm itself is ADR-0008's
  Confirm item, and stored-vs-decoded coverage is deliberately restated in
  OPEN-QUESTIONS Q-C2 for maintainer ratification.

## Context

Where a tile checksum lives, and what it covers, determine the cost of
verified reads. A checksum stored adjacent to the payload costs a second range
request per verified tile over HTTP and breaks payload contiguity — tiles can
no longer be aligned or coalesced into single large reads. A checksum computed
over *decoded* (post-decompression) bytes is worse in a second way: corruption
is only detectable after untrusted bytes have already been run through a
decompressor, and a remote reader can never verify exactly the byte range it
fetched. Zarr's sharding format cannot decouple checksum from payload because
checksums there are a codec stage; a container-level index can.

## Decision

The per-layer tile index is an array of fixed-size entries — offset, length,
and checksum per stored tile (exact layout set during spec drafting). The
checksum covers the **stored tile bytes exactly as they appear in the file**
(post-codec), and readers verify it **before** decompression. Tile payloads
carry no framing of any kind: no length prefix, no trailing checksum — they
are pure contiguous byte runs located solely by the index. If a columnar
index encoding is adopted (OPEN-QUESTIONS Q-E3), the checksum column stays
separate from the offset/length columns, so incompressible checksum noise
never poisons delta-friendly offset encoding.

## Consequences

A verified remote tile read is one range request; corrupt tiles never reach
the decompressor; payloads are alignable and coalescible because nothing sits
between them. The accepted trade: comparing logical content across two
differently-compressed files requires decoding both — the checksum attests
stored bytes, not the reference array. Readers gain an obligation: fetch the
index entry, fetch exactly `length` bytes at `offset`, verify, then decode
into a geometry-bounded buffer.

## Precedent

- PMTiles' measured lesson that checksum-like incompressible columns must be
  kept out of delta-compressed directory streams (columnar struct-of-arrays
  layout).
- Zarr sharding-indexed codec (offset/length index; the design TARN's index
  generalizes) and its crc32c codec's placement constraint.
- PNG's chunk CRC precedent: verify before acting on contents.
