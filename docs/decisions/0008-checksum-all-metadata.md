# 0008. Every metadata structure is checksummed, and verification is a reader obligation

- Status: Accepted
- Date: 2026-07-29
- Covers: metadata integrity; verifier contract; checksum algorithm
- Confirm: none — CRC-32C fixed by ADR-0023; the tile index's whole-
  structure CRC is amended to segment granularity by ADR-0024.

## Context

Integrity that covers only payload data leaves the most dangerous bytes
unprotected: a flipped bit in an offset table or a length field misdirects
readers into unrelated bytes, which is both a corruption hazard and an attack
surface. PNG documents its own version of this gap — the chunk length field
sits outside the CRC, and its errata note that readers can "get out of step."
The subtler lesson comes from Zarr's crc32c extension: it specifies how the
checksum is *encoded* but never obligates anyone to *verify* it. A checksum
whose verification is unspecified is documentation, not integrity.

## Decision

Every metadata structure — discovery structure (header/footer), directory,
every per-layer tile index, and the user-metadata document — carries its own
checksum, and no offset, length, or geometry field anywhere in the file sits
outside checksum coverage. One algorithm is used everywhere (recommended:
CRC-32C, stored as a fixed little-endian u32), for tiles and metadata alike.

The verifier contract is normative: a reader MUST verify a structure's
checksum before acting on any offset, length, or geometry it contains —
before allocation, before seeks. Mismatch outcomes are assigned per structure
using ADR-0003's outcome classes (e.g. directory → reject-file; per-layer
index → reject-layer; tile → reject-tile), with the full table drafted in the
spec's error register. The spec's threat-model paragraph states plainly that
checksums detect accidental corruption and do not authenticate; authenticity
requires detached hashing or signatures, out of scope for the container.

## Consequences

"Integrity by default" becomes testable — corrupt-file conformance vectors
carry expected verdicts — and misdirection-by-corrupted-offset is structurally
closed. Writers pay one checksum pass per structure per commit; readers pay
verification on the metadata path, with any fast-path opt-out made explicit
in the spec rather than left to silent implementation choice.

## Precedent

- PNG §5.3 chunk CRC and the documented length-outside-CRC gap.
- Zarr crc32c extension: encode-only specification as the anti-pattern.
- CRC-32C (RFC 3720): hardware support on SSE4.2/ARMv8, Zarr precedent.
