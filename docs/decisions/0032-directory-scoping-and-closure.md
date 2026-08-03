# 0032. Directory scoping by containment; zero-layer files; internal metadata codec

- Status: Accepted (resolves Q-A5; discharges ADR-0026's scope-binding
  Confirm and ADR-0009's internal-codec Confirm)
- Date: 2026-07-30
- Covers: record scope mechanism; empty directories; metadata_codec
  values
- Confirm: none

## Context

ADR-0026 required record scope to be determinable from framing alone
and deferred the mechanism. Positional binding (records bind to the
preceding layer record) would contradict the directory's
order-independence; a layer-id field needs header space the 24-byte
header does not have, or a payload convention that weakens
scope-from-framing. Containment has neither defect, and it makes
ADR-0026's "fully parse every layer record of a layer you modify"
mechanical. Separately: the data model deliberately left the minimum
layer count unstated (Q-A5), and the trailer's metadata_codec byte
needed its value set fixed.

## Decision

- **Scope by containment, depth exactly two.** The directory is a flat
  sequence of file-scope records. A layer record is a critical (MU=1)
  container: its inline payload carries the layer's core structural
  fields followed by that layer's sub-records, which are layer-scope by
  containment. Sub-records MUST NOT contain records (nesting deeper
  than two is a validity error at layer scope). No layer-id fields; no
  positional binding.
- **Zero-layer files are valid** (Q-A5): a directory containing no
  layer records is a conforming generation — the same
  empty-things-are-valid principle as ADR-0028, serving
  create-then-append workflows. Readers open such a file and list
  nothing.
- **Internal metadata codec** (ADR-0009 Confirm): the trailer's
  `metadata_codec` (u8: 0 invalid, 1 none, 2 zstd — both emittable in
  format major 1) applies to the directory and to user-metadata
  documents. It never applies to the tile index, whose raw-segmented
  encoding exists for ranged access. New values are major-only
  (ADR-0025).
- **User-metadata granularity** (discharges the granularity half of
  ADR-0015's Confirm): one user-metadata document per file and at most
  one per layer, as a file-scope record and a per-layer sub-record of
  one registered type. The document's encoding (JSON vs CBOR) remains
  open under Q-F1.
- **Commit-protocol details recorded** (drafting refinements of
  ADR-0017, none contradicting it): record extents — including
  user-metadata extents — are appended before the directory that
  references them, with no further intra-generation ordering; the
  generation counter increases by exactly 1 per commit (making
  gap-free chains a verifiable property the coverage walk relies on);
  and file_id SHOULD be cryptographically random, since cache
  correctness keys on its distinctness.

## Consequences

Scope needs zero bytes of header; updaters editing a layer parse
exactly one record subtree; empty files cost one row in the vector
corpus; metadata compression arrives at zero marginal reader cost
(zstd is already a mandatory core codec).

## Precedent

- The order-independence rule (PNG §14.3.2's lesson) that positional
  binding would have violated; PMTiles' internal-vs-tile compression
  split for the codec scoping.
