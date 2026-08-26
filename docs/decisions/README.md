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
| [0064](0064-instance-identity-in-the-manifest.md) | A vector names the instance it exercises, by the register's own words | Accepted (makes [R-ERR-02] measurable; corrects two mis-filed vectors) |
| [0065](0065-seven-escalations-round-seven-raised.md) | Seven decisions round seven escalated | Accepted (clears round 7; five more items were already decided) |
| [0066](0066-round-eight-reopens-the-updater-table.md) | Round eight reopens the updater table | Accepted (§20.4's MU = 1 grant at file scope and the MU = 0 / PE = 0 drop licence; scopes *cannot establish*) |
| [0067](0067-conformance-is-per-major-and-four-register-repairs.md) | Conformance is per-major, and four register repairs | Accepted (scopes *conforming*; removes F21 and renumbers the F rows) |
| [0068](0068-no-commit-removes-a-layer.md) | No commit removes a layer | Accepted (settles layer deletion; corrects [R-CNF-06]'s citation and §23.1's account) |
| [0069](0069-byte-order-is-not-a-file-state.md) | Byte order is not a file state | Accepted (retires the cause-row family; resolves ADR-0057 against ADR-0065/ADR-0067) |
| [0070](0070-a-supersede-only-commit-drops-nothing.md) | A supersede-only commit drops nothing | **Superseded by ADR-0081** (ADR-0080 reversed this decision without recording it) |
| [0071](0071-six-decisions-round-ten-raised.md) | Six decisions round ten raised | Accepted (amends ADR-0065's slack clause; trims ADR-0069's §20.5 sentence) |
| [0072](0072-the-taxonomy-loses-its-middle-class.md) | The taxonomy loses its middle class, and the appender its dead limb | Accepted (amends ADR-0071 in both of the places round 11 found) |
| [0073](0073-a-mechanical-propagation-check.md) | A mechanical propagation check | Accepted (adds `tarn_propagate.py`, SPEC-07 and SPEC-08; extends ADR-0050's tooling scope) |
| [0074](0074-a-stored-tile-freezes-its-declarations.md) | A stored tile freezes the declarations it depends on | Accepted (reverses the fill obligation landed hours earlier in the same round) |
| [0075](0075-document-rules-attach-only-under-assigned-encodings.md) | Document rules attach only under assigned encodings | Accepted (fixes the verifier verdict at an experimental user-metadata encoding) |
| [0076](0076-the-instance-criterion-applied-in-one-direction.md) | The instance criterion applied in one direction | Accepted (enumerates six cells; sixteen vectors added in the same commit) |
| [0077](0077-the-instance-criterion-stated-and-the-ordering-key-decircularized.md) | The instance criterion stated, and the ordering key de-circularized | Accepted (supersedes ADR-0076's direction rule; its cells stand) |
| [0078](0078-a-declaration-freeze-with-a-tense.md) | A declaration freeze with a tense | Accepted (supersedes ADR-0077's direction criterion, narrowing it; four more cells) |
| [0079](0079-a-shrink-that-de-addresses-is-permitted.md) | A shrink that de-addresses is permitted | Accepted (revises ADR-0074 and ADR-0078, narrowing their stranding argument) |
| [0080](0080-the-shrink-permission-takes-the-bar-s-tense.md) | The shrink permission takes the bar's tense | Accepted (revises ADR-0079's shrink paragraph, whose quantifier this corrects) |
| [0081](0081-the-drop-licence-regains-its-quantifier.md) | The drop licence regains its quantifier, and ADR-0070 is superseded | Accepted (supersedes ADR-0070; widens `SPEC-03`'s scope; from the round-18 repair audit) |
| [0082](0082-a-compactor-answers-for-the-region-it-regenerates.md) | A compactor answers for the region it regenerates, on detection | Accepted (confirms ADR-0081's open item; supersedes ADR-0080's compactor clause) |
| [0083](0083-version-minor-is-advisory-and-erasure-is-not-only-superseding.md) | `version_minor` is advisory for a compactor, and erasure is not only superseding | Accepted (resolves round 18's byte-level finding; widens `[R-PRV-01]` to any commit making data unreachable) |
| [0084](0084-the-experimental-mu1-refusal-is-top-level-only.md) | The experimental MU = 1 refusal is top-level only, and two clauses get keywords | Accepted (resolves round 19's byte-level finding; adds a context-injection clause to ADR-0034's access rule) |
| [0085](0085-a-metadata-frames-window-is-the-readers-capability.md) | A metadata frame's window is the reader's capability, not the file's defect | Accepted (resolves round 20's byte-level finding; follows `[R-MTA-09]`'s model for the neighbouring quantity) |
| [0086](0086-the-limits-tables-per-instance-rows.md) | §21.9's per-instance rows range over instances, not declarations | Accepted (resolves round 21's unanimous byte-level finding; aligns the table with `[R-COD-07]`'s existing quantifier) |
| [0087](0087-the-content-size-mismatch-is-an-r4-constraint.md) | A metadata frame's content-size mismatch is an R4 constraint, with four instances | Accepted (closes round 22's register debt; revises ADR-0085's R3 routing; 273 → 277 instances, four vectors) |
| [0088](0088-the-pinned-frame-fields-stay-and-the-carry-over-becomes-exhaustive.md) | The pinned frame fields stay enforced, and §18.2's carry-over becomes exhaustive | Accepted (resolves Q-E4; re-closes Q-E1's zstd half) |
| [0089](0089-the-round-23-audit-repairs.md) | §18.2's carry-over gets its four missing sentences, and R4's clause stops overclaiming | Accepted (resolves the round-23 repair audit's five confirmed findings; revises the trailing clause ADR-0087 gave R4, and three sentences ADR-0088) |
| [0090](0090-round-23s-repairs.md) | §21.7's enumerations stop overclaiming, and three register cells name what defines them | Accepted (dispositions cleanroom round 23) |
| [0091](0091-the-round-24-audit-repairs.md) | ADR-0090's F5 addition is reverted, and three of its claims are corrected | Accepted (resolves the round-24 repair audit's confirmed findings; revises four claims ADR-0090 wrote, one of which is reverted outright) |
| [0092](0092-the-r24b-audit-repairs.md) | R8's warrant is removed rather than replaced, and three clauses are corrected | Accepted (resolves the ADR-0091 re-audit's confirmed findings; revises three claims ADR-0091 wrote; corrects one pre-existing overclaim) |
| [0093](0093-round-24s-two-byte-level-defects.md) | A compactor is outside the commit protocol, and the shrink bar has one test | Accepted (resolves round 24's two byte-level ambiguities) |
| [0094](0094-the-compactor-binding-reversed.md) | ADR-0093's compactor half is reversed: `[R-LIF-02]` binds | Accepted (resolves the round-25 repair audit's confirmed findings; revises ADR-0093's compactor half, reverted outright. ADR-0093's shrink half) |
| [0095](0095-the-closed-counts-become-exhaustive.md) | Two closed counts are replaced by statements exhaustive by construction | Accepted (resolves the round-25 re-audit's confirmed findings; revises the counts ADR-0094 wrote in both places) |
| [0096](0096-round-24s-disposition.md) | Round 24's register cells are corrected, and §21.7 goes to the ledger whole | Accepted (dispositions round 24's non-byte-level findings) |
| [0097](0097-two-audits-and-a-contaminated-refute-pass.md) | Two glosses, F33's row list, and §23.1's superseded extent | Accepted (resolves the ADR-0096 and ADR-0095 audits) |
| [0098](0098-round-25s-disposition.md) | Round 25's four checkable repairs, and §21.2 goes to the ledger whole | Accepted (dispositions round 25's findings; revises a citation ADR-0097 wrote) |
| [0099](0099-the-entry-count-restatement.md) | §11.1 states its rule by `entry_count`, and `[R-SLB-03]` loses the pronoun | Accepted (resolves the ADR-0098 audit; revises two repairs ADR-0098 wrote) |
| [0100](0100-the-audit-chain-becomes-checkable.md) | The audit-chain invariant becomes mechanically checkable, and is corrected | Accepted (revises ADR-0097's statement of the invariant, which is too strong as written) |
| [0101](0101-the-lz4-escape-and-11-1-to-the-ledger.md) | §17.2's lz4 escape is stated by the addressed-tile count, and §11.1's growth Rationale goes to the ledger whole | Accepted (resolves the ADR-0099 audit; opens Q-B8) |
| [0102](0102-the-overflow-ceiling-reaches-designated-quantities.md) | The overflow ceiling reaches designated quantities, and §11.3 stops forming a product | Accepted (resolves round 26's byte-level ambiguity) |
| [0103](0103-round-26s-disposition.md) | Round 26's remaining findings: `[R-COD-04]`'s subject, and Appendix G's filter argument | Accepted (dispositions round 26's non-byte-level findings) |
| [0104](0104-editorial-changes-need-a-check-not-an-adr.md) | Editorial and placement changes need a check, not an ADR | Accepted (adds `tarn_editorial.py`; relaxes CONTRIBUTING's cite-your-ADR rule for changes that alter no normative content) |
| [0105](0105-reach-is-an-invariant-test-stated-in-2-3.md) | Reach is a test on the invariant violated, stated in §2.3 | Accepted (resolves Q-H4, Q-H5, Q-H6; adds `[R-CNF-13]`) |
| [0106](0106-the-r27-audit-repairs.md) | Six defects from the round-27 audit, five of them this week's own repairs | Accepted (revises ADR-0102, ADR-0103 and ADR-0105) |
| [0107](0107-the-r28-audit-repairs.md) | `[R-CNF-02]`'s stale quantifier, `[R-CNF-13]`'s swallowed exemption, and a tooling defect an auditor found | Accepted (revises ADR-0106; corrects `tarn_editorial.py`; amends Q-I6) |

Supporting evidence for many Precedent sections lives in
[docs/research/reference-format-lessons.md](../research/reference-format-lessons.md).
