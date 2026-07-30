# 0017. Mutability contract: append-only with atomic trailer swap

- Status: Accepted (resolves Q-A2)
- Date: 2026-07-29
- Covers: mutability, consistency, crash recovery, concurrency
- Confirm: none

## Context

A single-file format has no store layer to delegate consistency to, so the
mutability contract is format design. The worked failure analysis was
decisive on two of the three candidates. In-place metadata patching: a crash
during a ~2.6 KiB directory rewrite leaves the old directory destroyed and
the new one torn — a 14 GB file lost to a 2.6 KiB write, unrecoverably.
Read-only: every mutation is a whole-file rewrite, so appending a 4.3 GB
layer to a 10 GB file writes ~15 GB, and a 2.7 KiB metadata amendment costs
exactly the same 15 GB. Appending new payloads, a new complete directory,
and a new trailer writes only the new bytes, rewrites nothing, and leaves
every crash state readable at the prior generation.

## Decision

TARN's contract is **committed-prefix immutability**: bytes, once committed,
never change meaning; commits only extend the file. Specifically:

- An update appends, in order: payloads → tile indexes → new complete
  directory → durability barrier → new fixed-size trailer → barrier. The
  last valid (checksum-verified) trailer at EOF is authoritative; prior
  bytes are never modified.
- A torn append leaves the previous trailer intact; the file remains
  readable at its prior generation. The default read path is
  trailer-at-EOF-or-fail; backward **scan-back is a recovery affordance**
  (repair tools, explicit flags), not reader behavior — a hostile payload
  can embed a valid-looking trailer, and the spec names that attack.
- An append transaction MUST begin at the committed file length; writers
  MUST truncate or overwrite any bytes beyond it first (torn garbage is
  unrepresentable in a valid file).
- Concurrency is single-writer / multiple-reader, stated normatively. The
  trailer carries a generation counter and a creation-time file identifier:
  committed bytes never change, so caches keyed (file-id, range) never
  invalidate; revalidation is one 64-byte read.
- Writers performing very large single transactions SHOULD emit periodic
  checkpoint commits (~2.7 KiB each) to bound recovery scan distance, or
  create under a temporary name and swap.
- Superseded directories/trailers are dead space under the byte-coverage
  rule (Q-B5); logical deletion is not erasure; compaction (full rewrite)
  is the only true removal — restated in the privacy section.
- A read-only artifact is the degenerate single-generation case: writers
  may simply never append, at no reader cost.

## Consequences

Crash consistency comes from write ordering, not journaling — implementable
in a weekend. The contract maps onto non-POSIX backends: S3/GCS server-side
compose uploads only the new suffix; Azure append blobs map directly; CDN
range caches stay valid across generations. Honest costs: each commit
re-emits the whole directory, so one-layer-at-a-time appends accumulate
superseded directories quadratically (~111 MB after 1,000 single-layer
appends) — batch appends and compact periodically; a file being appended to
is not guaranteed remotely openable until commit (loud, never silent);
truncation to a *prior commit boundary* is indistinguishable from that
prior version by design — rollback detection needs out-of-band state; on
shared filesystems readers MAY retry a failed trailer verification before
declaring the file torn.

## Precedent

- PMTiles v3's blunt read-only contract as the honesty register; TARN
  extends it because appendability was a design goal, and pays for it in
  spec text rather than reader code.
- Zarr's store-interface delegation (no consistency, atomicity, or listing
  guarantees) as the gap a single-file format must fill itself.
- PNG's privacy lesson (logical deletion leaves recoverable data) applied
  to superseded generations.
