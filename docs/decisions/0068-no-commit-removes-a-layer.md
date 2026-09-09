# 0068. No commit removes a layer

- Status: Superseded by ADR-0130, which gives the layer record PE = 0 and
  lets a commit drop a layer
- Date: 2026-08-16
- Covers: whether layer deletion is a defined operation; `[R-CNF-06]`'s
  citation and scope; §23.1's account of what a commit removes
- Confirm: none

## Context

Cleanroom round 9's writer walk asked a question the document had never
answered in terms: **can a conforming updater emit a generation whose
directory omits a layer record the prior generation carried?**

§20.4 says no — *"both registered types carry PE = 1, so neither can be
dropped, and implementing a record's type confers understanding of it, not
permission to drop it"* — and §20.5 closes the compactor route, letting it
drop only the MU = 0 / PE = 0 row. §2.3 read the other way, scoping an
updater's preservation duty to *"records it does not understand"*, and
Appendix H's updater checklist restated that narrower scope. All three
triage passes agreed §20.4 governs and that §2.3's *"additionally"* is
additive rather than exhaustive, so there was no contradiction — but also
that the *consequence* was stated nowhere, while two other passages read as
though deletion were available.

## Decision

**Layer deletion is not a defined operation, and §20.4 now says so.**

The reason is not the flag arithmetic; it is what an in-place deletion
would buy. Removing a layer record from the directory does not remove the
layer's stored tiles or its tile-index region: those bytes stay where they
are, unreferenced, and become **slack** (§5.2). The file does not shrink,
only compaction ever reclaims the space, and the operation therefore costs
exactly what it appears to save. A deletion that leaves the data on disk is
worse than no deletion at all, because it also destroys the record that
said what those bytes were.

The sanctioned path is the one that actually removes the data: **write a
new file containing the layers you want.** `[R-LIF-01]` already sanctions
it — *"every conforming mutation of a file is either a commit (§9.2) or a
whole-file rewrite under a new file_id"* — and it needs no new machinery,
no new record flag, and no verifier obligation. §20.4 now names it, and
distinguishes it from compaction, which carries every layer of its input
forward.

Three restatements are corrected with it. `[R-CNF-06]` cited *"the
preservation obligations of Part I"* while §20.4, which states them, is in
Part III; it now cites §20.4 and says the obligations govern every record
type rather than only unfamiliar ones. Appendix H's updater checklist said
*"respects unknown records' MU and PE bits"* — the scoping §20.4
forecloses — and now states the general rule plus the removal bar. §23.1's
*"a commit that removes data removes only its reachability"* now says which
removal it means, since a commit supersedes data and never removes a layer.

## Consequences

The format has no in-place delete, and that is now a stated property rather
than an inference from a flag table three sections away. An implementer who
wants one builds a rewriter, which is a writer and needs nothing this
specification does not already define.

Nothing moves in the register or the corpus: no row changes, no instance is
added or removed, and the corpus stays at 125 conditions over 254 instances
and 306 vectors. The change is four edits, all clarifying rules already in
force.

Priced knowingly. A caller that wants one layer gone from a 16 GB file
rewrites 16 GB, where an in-place directory edit would have written a few
kilobytes. That is the honest cost, and it is the same cost the append-only
model already imposes on every other kind of reclamation (§20.5); pretending
otherwise would have shipped an operation whose name promised space it never
returns.

## Precedent

- `[R-LIF-01]`'s two-way split — a commit, or a whole-file rewrite under a
  new file_id — which already contained the answer.
- ADR-0048's live-state coverage model, under which anything the live
  trailer does not reach is slack that is counted and reported rather than
  reused; an in-place layer removal is precisely a slack-manufacturing
  operation.
- §23.1's existing rule that deletion is not erasure, extended to say which
  removals a commit performs at all.
