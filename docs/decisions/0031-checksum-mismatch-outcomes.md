# 0031. Checksum-mismatch outcomes per structure

- Status: Accepted (resolves Q-C3)
- Date: 2026-07-30
- Covers: the severity mapping from failed verification to outcome class
- Confirm: none

## Context

A checksum whose failure consequence is unspecified is documentation,
not integrity (the Zarr crc32c lesson). The outcome must be scoped per
structure — partial-read workflows should survive one bad tile — and
each row must be a testable verdict a corrupt-file conformance vector
can pin.

## Decision

| Failed verification | Outcome |
|---|---|
| Trailer at EOF−64 (magic, CRC, or self-checks) | reject-file — the default read path has no fallback; backward scan is recovery tooling (ADR-0017), not reader behavior |
| Directory CRC | reject-file |
| A layer's index cross-checks, CRC array, or any index segment | reject-layer (that layer only) |
| A stored tile's CRC against its index entry | reject-tile |
| User-metadata document CRC | ignore-record; readers SHOULD report the loss |

Verification is not optional for conforming readers, and no in-file
flag disables it; implementations offering non-verifying fast modes do
so outside this specification's conformance classes.

## Consequences

Every row gets at least one deliberately corrupted conformance vector
with a required verdict. One bad tile never poisons a layer; one bad
layer never poisons a file; and metadata loss is loud but non-fatal.

## Precedent

- PNG's precondition subtlety (ignoring a bad ancillary chunk is safe
  only because its CRC verified the chunk is what it claims); Zarr's
  unspecified-verifier gap as the anti-pattern.
