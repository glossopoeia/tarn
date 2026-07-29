# 0014. Little-endian only

- Status: Accepted
- Date: 2026-07-29
- Covers: byte order
- Confirm: none

## Context

Dual endianness is a permanent tax that buys nothing on modern hardware.
TIFF's II/MM duality doubled its conformance surface for thirty years, seeded
an entire class of half-swapped-file corruption bugs, and forced the spec
itself to engineer around it (TIFF LZW is defined byte-oriented specifically
"so compressed data will be identical whether it is an II or MM file" — the
spec paying costs to neutralize its own option). A byte-order mark is also a
second source of truth: one more field whose corruption or mishandling
silently transposes every multi-byte value in the file. Every relevant
consumer platform today — x86-64, ARM64, WASM, GPUs — is little-endian.

## Decision

All multi-byte values in a TARN file are little-endian, stated once, globally.
There is no byte-order field and no byte-order variant. Anything resembling a
byte-swapped signature is treated as an invalid file (reject-file), not as a
foreign-endian file to be adapted.

## Consequences

Half the conformance matrix disappears; checksums of identical content are
identical bytes everywhere; 128-bit-style two-half encodings can never
disagree about half order. Big-endian hosts byte-swap on access — an accepted,
negligible cost on the platforms where TARN will actually run.

## Precedent

- TIFF II/MM as the documented permanent tax, including the LZW
  byte-orientation workaround.
- PMTiles v3: little-endian-only declared in one sentence — the register TARN
  matches.
