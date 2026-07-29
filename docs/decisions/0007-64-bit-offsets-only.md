# 0007. All offsets, lengths, and extents are fixed-width unsigned 64-bit

- Status: Accepted
- Date: 2026-07-29
- Covers: integer widths for file geometry
- Confirm: none

## Context

Formats that let writers choose integer widths tax every reader forever: each
choice point doubles the test matrix, and the narrow variant eventually
becomes a hard ceiling. TIFF is the canonical case — its 32-bit offsets could
not be widened compatibly, so the fix was BigTIFF, a fork with a different
magic number rather than a version. Width variance also invites silent
truncation bugs at the boundary, the worst possible failure mode for a
format that stores scientific data.

## Decision

Every file offset, byte length, dimension extent, and tile extent is an
unsigned 64-bit little-endian integer. Valid values are bounded to ≤ 2^63 − 1,
stated explicitly so implementations in signed-64-bit languages work without
gymnastics. There are no width variants and no writer choice, anywhere in the
format. Counts that are structurally small (e.g. rank, channel count) may use
narrower fixed widths, chosen once by the spec — never by the writer.

## Consequences

One test matrix, no truncation boundary, no future fork to widen anything.
The size cost is negligible at TARN's target tile granularity (megabyte-scale
tiles), and the index-size concern is addressed by index encoding choices
(OPEN-QUESTIONS Q-E3), not by narrowing field widths.

## Precedent

- BigTIFF: widening as a fork, not a version — the failure TARN pre-empts.
- PNG's explicit signed-domain concession (values bounded for two's-complement
  languages), applied here at 64-bit scale.
- TIFF's SHORT-or-LONG writer choice as permanent reader tax.
