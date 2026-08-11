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
| [0005](0005-optional-tile-alignment.md) | Optional per-layer tile alignment as a checkable invariant | Accepted (values fixed by ADR-0035) |
| [0006](0006-consolidated-metadata-directory.md) | Consolidated metadata directory, O(1) round trips | Accepted (placement resolved by ADR-0018) |
| [0007](0007-64-bit-offsets-only.md) | All offsets, lengths, and extents are u64 | Accepted |
| [0008](0008-checksum-all-metadata.md) | Every metadata structure checksummed; verification is a reader obligation | Accepted (algorithm fixed by ADR-0023; index granularity amended by ADR-0024) |
| [0009](0009-codec-menu.md) | Closed codec menu plus byte-shuffle filter | Accepted (internal codec fixed by ADR-0032; wrappers and shuffle scope fixed by ADR-0039) |
| [0010](0010-fill-values-and-sparse-tiles.md) | Mandatory per-channel fill; unstored tiles read as fill | Accepted (sentinel fixed by ADR-0024; boolean fill fixed by ADR-0036) |
| [0011](0011-uniform-tiles-padded-edges.md) | Uniform tile sizes with padded edge tiles | Accepted (padding content fixed by ADR-0037) |
| [0012](0012-channel-layouts.md) | Interleaved and planar layouts with a full validity table | Accepted (planar order fixed by ADR-0021; boolean representation fixed by ADR-0037 as amended by ADR-0038) |
| [0013](0013-sample-type-list.md) | Closed sample-type list with zero optional members | Accepted (reservations fixed by ADR-0036) |
| [0014](0014-little-endian-only.md) | Little-endian only | Accepted |
| [0015](0015-structured-user-metadata.md) | Structured, quarantined user metadata | Accepted (granularity fixed by ADR-0032; encoding fixed by ADR-0045) |
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
| [0030](0030-byte-coverage-as-validity.md) | Byte coverage is file validity | Accepted (resolves Q-B5; history-wide scope superseded by ADR-0048) |
| [0031](0031-checksum-mismatch-outcomes.md) | Checksum-mismatch outcomes per structure | Accepted (resolves Q-C3) |
| [0032](0032-directory-scoping-and-closure.md) | Directory scoping by containment; zero-layer files; metadata codec | Accepted (resolves Q-A5; discharges ADR-0009/0015/0026 Confirms; codec scoping amended by ADR-0033) |
| [0033](0033-raw-directory-per-record-codec.md) | Raw directory; user-metadata records declare their own codec | Accepted (amends ADR-0032/0025) |
| [0034](0034-cleanroom-protocol.md) | The cleanroom protocol, as piloted | Accepted (resolves Q-I2) |
| [0035](0035-alignment-values.md) | Alignment value sets | Accepted (discharges ADR-0005 Confirm) |
| [0036](0036-sample-type-ids-and-fill-mechanics.md) | Sample-type identifiers and fill mechanics | Accepted (resolves Q-D1/Q-D2/Q-D3; discharges ADR-0010/0013 Confirms) |
| [0037](0037-boolean-packing-and-padding-content.md) | Packed booleans over the value sequence; fill-encoded edge padding | Accepted (resolves Q-D6, completes Q-C4; interleaved boolean cells superseded by ADR-0038) |
| [0038](0038-interleaved-boolean-bytes.md) | Interleaved boolean values are single bytes | Accepted (amends ADR-0012/0037 after maintainer challenge) |
| [0039](0039-codec-wrappers-and-shuffle-scope.md) | Codec wrapper pinning and the shuffle stride rule | Accepted (resolves Q-E1/Q-E2; fixes ADR-0009 framing; discharges round-2 §17 deferrals) |
| [0040](0040-validation-follows-reliance.md) | Validation follows reliance | Accepted (discharges cleanroom timing deferrals from rounds 1 and 2) |
| [0041](0041-updater-reemission-and-compaction-identity.md) | Updater re-emission, verification depth, and compaction identity | Accepted (discharges round 1's three §20 deferrals) |
| [0042](0042-error-register-form.md) | The error register is derivative, complete, and per-violation | Accepted (fixes gate G5's coverage unit) |
| [0043](0043-limits-as-minimum-guarantees.md) | Limits are minimum guarantees, sized by cost budgets | Accepted (resolves Q-H1) |
| [0044](0044-extension-surface-and-registry.md) | The enumerated extension surface and its registry | Accepted (resolves Q-G3) |
| [0045](0045-user-metadata-json-and-standardized-keys.md) | User metadata is restricted JSON; conventions live as keys | Accepted (resolves Q-F1/Q-F3/Q-D5; discharges ADR-0015 Confirm) |
| [0046](0046-corpus-is-derivative.md) | The conformance corpus is derivative evidence | Accepted |
| [0047](0047-reproducible-writer-profile.md) | A non-normative reproducible-writer profile | Accepted (resolves Q-I1) |
| [0048](0048-live-state-coverage.md) | Coverage certifies the live state; slack is counted, not modelled | Accepted (supersedes ADR-0030's history-wide coverage) |
| [0049](0049-register-repair-and-instance-identity.md) | Repair the error register and fix what an instance is | Accepted (§21.8's count disagreed with its own table) |
| [0050](0050-specification-checking-tooling.md) | Tooling that checks the specification against itself | Accepted (scopes the only code AGENTS.md permits) |
| [0051](0051-interleaved-boolean-byte-interpretation.md) | Define what a reader returns for a nonconforming boolean byte | Accepted (addresses the UB, not the constraint; amends ADR-0038) |
| [0052](0052-remote-open-probe-scope.md) | The remote-open prober, and where tooling stops being a reader | Accepted (instrument for gate G4) |
| [0053](0053-corpus-layout-identity-and-isolation.md) | Corpus layout, vector identity, and one defect per vector | Accepted (gate G5 structure) |
| [0054](0054-vector-manifest-and-expectation-model.md) | The manifest schema and what a vector expects of a reader | Accepted (gate G5 schema) |
| [0055](0055-coverage-as-a-measured-gate.md) | Coverage is measured against the register, and reported | Accepted (binds G5 to instances, not rows) |
| [0056](0056-register-repair-from-the-corpus.md) | Five register defects the corpus found | Accepted (resolves the R11 range contradiction) |
| [0057](0057-rows-without-a-witness.md) | Three rows that name a cause rather than a state | Accepted (deletes F40, L45, L25) |
| [0058](0058-eight-silences-round-six-found.md) | Eight places the rules were silent | Accepted (closes round 6's five byte-level defects) |
| [0059](0059-metadata-encoding-2-is-core.md) | Metadata encoding 2 is core | Accepted (reconciles §1's promise with §18.2) |
| [0060](0060-a-layer-rejection-is-prospective.md) | A layer rejection is prospective | Accepted (ratifies §2.4; reads out ADR-0040) |
| [0061](0061-persistence-governs-every-record-type.md) | Persistence governs every record type, implemented or not | Accepted (closes a §20.4 seam left by ADR-0041) |
| [0062](0062-a-verifier-may-stop-but-unexamined-is-not-clean.md) | A verifier may stop, but unexamined is not clean | Accepted (adds a verifier reporting obligation) |
| [0063](0063-standardized-key-placement-is-advisory.md) | Standardized key placement and value shape are advisory | Accepted (resolves round 7's register gap by deletion; refines ADR-0045) |

Supporting evidence for many Precedent sections lives in
[docs/research/reference-format-lessons.md](../research/reference-format-lessons.md).
