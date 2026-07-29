# Architecture Decision Records

This directory is the reasoning trail for the TARN format. Every format-level
decision is recorded here as a numbered ADR (see
[0000-template.md](0000-template.md) for the template and conventions).
Decisions marked **Proposed** or carrying a **Confirm** line have open
sub-questions, tracked either in the ADR's own Confirm line or — when they
need real analysis — as entries in
[OPEN-QUESTIONS.md](../../OPEN-QUESTIONS.md); a ledger entry is resolved
exactly when an ADR records its answer.

ADRs are numbered in drafting order and never reused. A superseded ADR is
never rewritten — a new ADR supersedes it and both link to each other.

## Index

| ADR | Title | Status |
|-----|-------|--------|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions as in-repo ADRs | Accepted |
| [0002](0002-vocabulary-and-identification.md) | Core vocabulary and file identification | Accepted (Confirm: signature form — Q-G4) |
| [0003](0003-spec-conventions-and-conformance.md) | Normative conventions and conformance classes | Accepted |
| [0004](0004-tile-checksums-in-index.md) | Per-tile checksums live in the tile index and cover stored bytes | Accepted (Confirm: coverage domain — Q-C2) |
| [0005](0005-optional-tile-alignment.md) | Optional per-layer tile alignment as a checkable invariant | Accepted (Confirm: values) |
| [0006](0006-consolidated-metadata-directory.md) | Consolidated metadata directory, O(1) round trips | Accepted (requirement); Proposed (placement) |
| [0007](0007-64-bit-offsets-only.md) | All offsets, lengths, and extents are u64 | Accepted |
| [0008](0008-checksum-all-metadata.md) | Every metadata structure checksummed; verification is a reader obligation | Accepted (Confirm: algorithm) |
| [0009](0009-codec-menu.md) | Closed codec menu plus byte-shuffle filter | Accepted (Confirm: internal metadata codec) |
| [0010](0010-fill-values-and-sparse-tiles.md) | Mandatory per-channel fill; unstored tiles read as fill | Accepted (Confirm: sentinel encoding, boolean fill) |
| [0011](0011-uniform-tiles-padded-edges.md) | Uniform tile sizes with padded edge tiles | Accepted (Confirm: padding content) |
| [0012](0012-channel-layouts.md) | Interleaved and planar layouts with a full validity table | Accepted (Confirm: planar order, bool packing) |
| [0013](0013-sample-type-list.md) | Closed sample-type list with zero optional members | Accepted (Confirm: fp8/opaque reservations) |
| [0014](0014-little-endian-only.md) | Little-endian only | Accepted |
| [0015](0015-structured-user-metadata.md) | Structured, quarantined user metadata | Proposed |
| [0016](0016-licensing.md) | Licensing: CC BY 4.0 / Apache-2.0 / CC0 split | Accepted (Confirm: CC0 vectors) |

Supporting evidence for many Precedent sections lives in
[docs/research/reference-format-lessons.md](../research/reference-format-lessons.md).
