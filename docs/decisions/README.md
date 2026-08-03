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
| [0002](0002-vocabulary-and-identification.md) | Core vocabulary and file identification | Accepted (signature fixed by ADR-0029) |
| [0003](0003-spec-conventions-and-conformance.md) | Normative conventions and conformance classes | Accepted |
| [0004](0004-tile-checksums-in-index.md) | Per-tile checksums live in the tile index and cover stored bytes | Accepted (coverage ratified by ADR-0023) |
| [0005](0005-optional-tile-alignment.md) | Optional per-layer tile alignment as a checkable invariant | Accepted (Confirm: values) |
| [0006](0006-consolidated-metadata-directory.md) | Consolidated metadata directory, O(1) round trips | Accepted (placement resolved by ADR-0018) |
| [0007](0007-64-bit-offsets-only.md) | All offsets, lengths, and extents are u64 | Accepted |
| [0008](0008-checksum-all-metadata.md) | Every metadata structure checksummed; verification is a reader obligation | Accepted (algorithm fixed by ADR-0023; index granularity amended by ADR-0024) |
| [0009](0009-codec-menu.md) | Closed codec menu plus byte-shuffle filter | Accepted (internal codec fixed by ADR-0032) |
| [0010](0010-fill-values-and-sparse-tiles.md) | Mandatory per-channel fill; unstored tiles read as fill | Accepted (sentinel fixed by ADR-0024; Confirm: boolean fill — Q-D3) |
| [0011](0011-uniform-tiles-padded-edges.md) | Uniform tile sizes with padded edge tiles | Accepted (Confirm: padding content) |
| [0012](0012-channel-layouts.md) | Interleaved and planar layouts with a full validity table | Accepted (planar order fixed by ADR-0021; Confirm: bool packing — Q-D6) |
| [0013](0013-sample-type-list.md) | Closed sample-type list with zero optional members | Accepted (Confirm: fp8/opaque reservations) |
| [0014](0014-little-endian-only.md) | Little-endian only | Accepted |
| [0015](0015-structured-user-metadata.md) | Structured, quarantined user metadata | Proposed (granularity fixed by ADR-0032; Confirm: encoding — Q-F1) |
| [0016](0016-licensing.md) | Licensing: CC BY 4.0 / Apache-2.0 / CC0 split | Accepted (Confirm: CC0 vectors) |
| [0017](0017-append-only-mutability.md) | Mutability: append-only with atomic trailer swap | Accepted (resolves Q-A2) |
| [0018](0018-hybrid-discovery-anchoring.md) | Discovery anchoring: constant front block + 64-B trailer | Accepted (resolves Q-A1) |
| [0019](0019-remote-open-model.md) | Remote open: two-request baseline, suffix optimization | Accepted (resolves Q-A3/Q-A4) |
| [0020](0020-linearization-order.md) | Linearization: row-major via reserved enum | Accepted (resolves Q-B2) |
| [0021](0021-planar-channel-major.md) | Planar tile ordering: channel-major | Accepted (resolves Q-B3) |
| [0022](0022-slab-declaration.md) | Slab: declared layout guarantee, uniform S | Accepted (resolves Q-B1) |
| [0023](0023-checksum-algorithm-and-domain.md) | CRC-32C everywhere; stored-bytes domain ratified | Accepted (resolves Q-C1/Q-C2) |
| [0024](0024-segmented-index-and-sentinel.md) | Segmented raw index, all-ones sentinel, exactly-once extents | Accepted (resolves Q-E3/Q-D4/Q-B4) |
| [0025](0025-format-versioning.md) | Format versioning: trailer major/minor, forever clause | Accepted (resolves Q-G1) |
| [0026](0026-record-framing-and-flags.md) | Record framing: 24-B header, MU/PE flags | Accepted (resolves Q-G2; scoping fixed by ADR-0032) |
| [0027](0027-name-and-string-rules.md) | Name and string rules | Accepted (resolves Q-F2) |
| [0028](0028-degenerate-geometry.md) | Degenerate geometry: zero extents valid, everything else bounded | Accepted |
| [0029](0029-identification-constants.md) | File identification constants | Accepted (resolves Q-G4) |
| [0030](0030-byte-coverage-as-validity.md) | Byte coverage is file validity | Accepted (resolves Q-B5) |
| [0031](0031-checksum-mismatch-outcomes.md) | Checksum-mismatch outcomes per structure | Accepted (resolves Q-C3) |
| [0032](0032-directory-scoping-and-closure.md) | Directory scoping by containment; zero-layer files; metadata codec | Accepted (resolves Q-A5; discharges ADR-0009/0015/0026 Confirms; codec scoping amended by ADR-0033) |
| [0033](0033-raw-directory-per-record-codec.md) | Raw directory; user-metadata records declare their own codec | Accepted (amends ADR-0032/0025) |

Supporting evidence for many Precedent sections lives in
[docs/research/reference-format-lessons.md](../research/reference-format-lessons.md).
