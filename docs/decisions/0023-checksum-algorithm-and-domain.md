# 0023. CRC-32C everywhere; tile checksums cover stored bytes (ratified)

- Status: Accepted (resolves Q-C1 and Q-C2; discharges ADR-0008's algorithm
  Confirm and ADR-0004's coverage-domain Confirm)
- Date: 2026-07-30
- Covers: checksum algorithm, parameters, and coverage domain
- Confirm: none

## Context

One algorithm serves every checksummed structure (ADR-0008). CRC-32C
(Castagnoli) wins on every axis that matters. Hardware: the x86 `crc32`
instruction computes Castagnoli *only* (SSE4.2, 2008+), and ARMv8.1+ makes
its CRC32C instructions mandatory — choosing CRC-32 (IEEE) forfeits the
cheapest hardware path on the dominant ISAs. Error detection (published
Koopman bounds): CRC-32C holds Hamming distance 4 — every 1-, 2-, and
3-bit error detected — up to 268 MB, covering every TARN structure size;
IEEE falls to HD=3 above ~11 KiB. Fast hashes (xxh3, truncated BLAKE3)
carry *no* HD guarantee at all against the dominant physical corruption
modes (bit flips, short bursts), have stdlib support nowhere, and their
speed advantage buys nothing — checksumming already outruns every
decompressor and NVMe stream in the pipeline. A 4-byte code preserves the
20-byte index entry and the zero-slack trailer; at 2⁻³² random-miss
probability, a fleet verifying a billion corrupted 16 MiB tiles expects
~0.23 silent misses — corruption detection, which is this mechanism's whole
scope (ADR-0008: not authentication).

## Decision

**CRC-32C for every checksummed structure** — trailer, directory, index
segment array, tile payloads, user metadata: polynomial 0x1EDC6F41
(RFC 3720), reflected input/output, initial value and final XOR
0xFFFFFFFF, stored as little-endian u32. The spec pins the check vector
`crc32c("123456789") = 0xE3069283`.

**Coverage domain ratified: tile checksums cover the stored (wire) bytes,
verified before decompression** (ADR-0004 confirmed). Deliberately given
up: attestation of decoded output — a defective codec implementation, or
cross-file comparison of differently-compressed content, are outside the
checksum's scope. Compensating controls: decoded size is fully determined
by declared geometry (ADR-0009), closing the allocation/bomb class before
decode; codecs are pinned to exact external definitions with byte-exact
vectors, so verified stored bytes plus a conforming decoder determine the
decoded array; and a **decoded-hash ancillary record type is reserved** for
consumers needing output attestation — its flag semantics are decided at
registration (deliberately not pre-committed here: a content-derived
attestation must not survive edits to the content it attests).

## Consequences

One ~30-line software implementation with a hardware fast path everywhere;
Go has it in the standard library, Rust/C in tiny deps, browser JS in a
table implementation. The one honest wart: Python's stdlib CRC is IEEE, so
Python readers take a small wheel or a slow pure-Python path for bulk
verification. CRC combine (GF(2) composition) lets writers assemble
segment CRCs incrementally.

## Precedent

- RFC 3720 (iSCSI) as CRC-32C's normative home; Zarr's crc32c extension as
  ecosystem alignment.
- Koopman's published CRC Hamming-distance tables as the error-detection
  evidence.
