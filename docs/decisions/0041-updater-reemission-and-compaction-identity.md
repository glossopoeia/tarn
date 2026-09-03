# 0041. Updater re-emission, verification depth, and compaction identity

- Status: Accepted (discharges cleanroom round 1's three §20
  deferrals); its MU = 0 / PE = 0 drop gate superseded by ADR-0120
- Date: 2026-08-04
- Covers: byte-identical re-emission of retained records; PE
  semantics operationalized; appender verification depth; compaction
  file_id and generation numbering
- Confirm: none

## Context

Every commit appends a complete directory, so re-emission is the
preservation mechanism, and cleanroom round 1 deferred three calls to
§20: what re-emission preserves, how much of the existing file an
appender must verify, and what identity a compacted file carries.
Record identity is byte equality throughout this specification —
"semantic re-emission" would lean on a record-equality notion the
spec never defines — and the lifecycle rules promise that any
(file_id, range) pair is byte-stable forever, which decides the
compaction question outright.

## Decision

- **Byte-identical re-emission of every retained, logically
  unmodified record** — known or unknown type: header, inline
  payload, and extent slot copied verbatim; a record the updater
  modifies is new output under its writer obligations. For types the
  updater does not implement, stored flags govern, restating
  ADR-0026's obligations in spec form: MU = 1 → retain
  byte-identical and do not modify the scope it governs (file-scope
  unknown criticals block file-scope edits entirely); MU = 0, PE = 1
  → retain byte-identical; MU = 0, PE = 0 → retain, or drop only
  when the commit modifies the record's scope, reporting the loss.
  Never re-encode; never modify except by compaction's slot
  re-pointing.
- **Verification depth follows reliance** (ADR-0040 extended to the
  updater class): the trailer and full directory always — forced,
  since re-emission relies on every directory byte — plus
  reader-depth validation of exactly the layers the commit modifies,
  including the index chains of any segments whose entries are
  reused. Untouched structures impose nothing. Append cost is
  O(directory + modified layers' indexes), independent of payload
  volume.
- **Compaction is a new identity:** a compactor emits a new file
  carrying only the structures reachable from the input's live
  trailer, under a fresh file_id — a whole-file rewrite under a new
  file_id by ADR-0017's own terms, and reuse would make a
  (file_id, range) cache serve wrong bytes — and generation 1, with
  ignore-lane flags copied forward. Stored-tile bytes and record
  payloads are preserved verbatim (entry crcs unchanged); extent
  slots re-point; relocated tile-index regions are regenerated with
  unchanged entry lengths and entry crcs, segment CRCs recomputed;
  the output's reference arrays equal the input's bit for bit. A
  compactor refuses any file carrying an unknown MU = 1 record,
  whose references it cannot know. Its verification depth is
  everything it carries.

## Consequences

The records of adjacent generations differ exactly by those
modified, added, or dropped, as a multiset (record order carries no
meaning) — a testable preservation property — and
re-encode drift (a re-serializer renormalizing a name and thereby
changing its identity) is impossible. Appends never scale with
payload volume. Caches keyed (file_id, range) survive compaction by
construction. Foreclosed: silent record normalization, and any
certify-before-append obligation.

## Precedent

- PNG §14's editor rules and safe-to-copy bit — the PE bit's
  ancestor (ADR-0026). PNG permits rather than compels carrying
  unrecognized ancillary chunks, and forbids carrying unsafe ones
  across critical edits; what it fixes is that a chunk carried is
  carried verbatim, which is the property restated here.
- ADR-0040's validation-follows-reliance principle, extended to the
  updater class the spec already binds to reader obligations
  (§2.3's verifier/updater inheritance, `[R-CNF-11]`).
- Content-addressed stores (Git's object database, Plan 9's Venti):
  identical bytes under a stable key are what make dedup and
  immutable caching sound — the property byte-stable retention
  preserves across generations.
