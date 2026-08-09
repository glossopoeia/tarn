# 0049. Repair the error register and fix what an instance is

- Status: Accepted
- Date: 2026-08-09
- Covers: §21's register — row set, row identity, the Instances column's
  meaning; the pre-trailer pad's bound; the scope-discrimination
  obligation on reject-layer and reject-tile vectors
- Confirm: none

## Context

Gate G5 binds one conformance vector to each *instance* named by
§21's register, so the register's row set and its instance counts
become the corpus's build list. Audited before generating anything,
the table did not support that weight. Its stated size was wrong; it
carried three rows byte-identical to the row above; it omitted
five conditions this specification states elsewhere; and its
Instances column had drifted to mean two different things in
different subsections. Building ~300 files against it would have
frozen every one of those defects into the corpus.

The damage is traceable. ADR-0048 retired declared padding and
authorised six row deletions. Five landed cleanly at `f738b29`, which
correctly updated §21.8 to 121 conditions over 213 instances. The
sixth was executed at `e417dcb` as a block rewrite that shifted
§21.2's tail up by one and filled the vacated slots with copies of
their neighbours: four rows were deleted where one was authorised,
and three duplicates were inserted. The two errors cancelled to zero
instances, which is why the count still looked plausible and why five
subsequent reviews — including a dedicated adversarial round that
touched one of the affected rows — did not catch it.

## Decision

- **Duplicate rows are deleted, not differentiated.** Three rows were
  byte-identical to the row above in all six columns. They are
  removed; nothing is invented to fill them.
- **Rows lost without authorisation are restored** from `f738b29`:
  the front-signature-block mismatch (`[R-CNT-04]`) and two or more
  top-level user-metadata records (`[R-CNT-14]`). Both cite live
  reader MUSTs, so §21.1's completeness clause makes their absence a
  defect in this document.
- **Conditions this specification names and the register never
  carried are added**: a user-metadata record whose `extent_length`
  is below 5 (`[R-CNT-25]`) and whose `inline_length` is not 1
  (`[R-MTA-03]`), each at file and layer scope. F7's citation moves
  to `[R-CNT-27]`, the rule that actually states the 128-byte floor.
- **An instance is one distinguishable file.** The Instances column
  enumerates what the corpus builds: a field the condition ranges
  over, a container it can occur in, or one of several alternatives
  the condition text states. Where a condition is a single predicate
  over several fields — a sum against a bound, a combination of two
  flag bits — the fields it reads are not instances, because no two
  files could differ.
- **A violation is a register row wherever it is named.** Two
  conditions that stated "the file is nonconforming" while sitting in
  §21.6's table of non-violations (`[R-MTA-05]`, `[R-CNT-22]`) move
  to §21.2 and §21.3 with detector *verifier*, on the precedent
  `[R-CNT-12]`'s reserved-flag rows already set. `[R-CNT-22]`'s
  verifier obligation strengthens from SHOULD-report to MUST-treat-
  as-a-validity-error to match.
- **Row identifiers are positional labels, renumbered contiguously.**
  They are not requirement identifiers and §2.2's stability
  discipline does not reach them. §21.3's L40 hole — present since
  the register was first drafted, never carrying a condition — closes
  by renumbering. Vector identity therefore never derives from a row
  id; the corpus keys on its own serials and carries the row as a
  field.
- **The pre-trailer pad has no bound.** `[R-CNT-05]`'s "fewer than 64
  bytes" was stale text ADR-0048 left standing: under live-state
  coverage those bytes are slack, whose extent and content this
  specification does not constrain. The clause is struck, and with it
  the row for a gap of 64 bytes or more. What survives is the rule
  that no *structure* may sit there, which a verifier MUST detect.
- **Reject-layer and reject-tile vectors carry an intact sibling**
  (`[R-VEC-04]`). `[R-CNF-12]` lets a reader reject any nonconforming
  file whole, and every register-derived vector is nonconforming, so
  a single-scope vector cannot distinguish a reader that scopes its
  refusal from one that rejects everything. The sibling — another
  layer, or another tile of the same layer, with its decoded content
  recorded — is what makes the distinction observable.

The register is now **127 conditions over 224 named instances**.

## Consequences

The corpus gets a build list that means what it says, and G5 becomes
countable rather than asserted. §21.8's figure is recomputed, not
adjusted; PLAN.md §9 follows it.

Priced knowingly. Renumbering every row of §21.2 and §21.3 is free
exactly once — now, before any vector cites one — and expensive
afterwards, which is why vector identity is decoupled from row
identity in the same decision. Filing `[R-MTA-05]` and `[R-CNT-22]`
as violations means a verifier can no longer certify files that
readers handle perfectly well; that is the correct reading of
`[R-CNF-12]`, and §21.6 keeps the reader's side of both so no reader
is misled into rejecting them. Striking the pre-trailer pad's bound
removes a writer MUST that no actor was assigned to detect — the same
defect shape as the pad-zeroing rule that survived at seven sites
after §5.2 made it advisory.

The intact-sibling rule is a construction obligation, not a schema
field: it binds roughly 150 vectors, and retrofitting it after they
exist means rebuilding them. It is recorded now for that reason.

This ADR does not supersede ADR-0042, whose "122 rows over 226
instances" describes the register as first drafted and stays as
written. That figure was itself wrong — the table held 122 rows over
129 instances at `72ae3fa` — which is part of why the counts are now
generated rather than hand-maintained.

## Precedent

- ADR-0042's derivative register and ADR-0046's derivative corpus:
  each row restates its rule, and the rule governs. A register that
  miscounts itself breaks the only claim it makes normatively, which
  is completeness.
- The QOI lesson this repository already carries: divergence between
  "valid per spec" and "valid per implementation" is a spec bug. A
  corpus makes the two comparable only if the spec is the fixed
  point, and only if the corpus's coverage claim is checkable.
- PNG's chunk-registry discipline, where a registered type's flag
  bits are fixed by the registry and a mismatch is a file defect
  rather than a reader's problem — the shape `[R-CNT-22]` now
  follows.
