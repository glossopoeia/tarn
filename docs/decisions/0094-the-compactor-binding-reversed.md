# 0094. ADR-0093's compactor half is reversed: `[R-LIF-02]` binds

- Status: Accepted (resolves the round-25 repair audit's confirmed findings)
- Date: 2026-08-25
- Covers: §20.5's compactor obligations; §23.1's removal enumeration; §11.1's
  shrink Rationale
- Revises: ADR-0093's compactor half, reverted outright. ADR-0093's shrink half
  stands.
- Confirm: none

## Context

The audit before round 25 read ADR-0093's two hunks — the only two repairs
written to close findings a fresh-context round graded **byte-level**. Three
auditors returned **25 findings**, five self-flagged byte-level. The
per-auditor cap left 13 unverified, so the list below is a floor.

The audit carried a role no previous one had: an auditor given the same hunks
as another but charged **not** to judge the repaired sentences — only to find
what elsewhere in the document was true solely under the old wording. That role
exists because `tarn_propagate` cannot see a passage that is unchanged, absent
from every hunk, and quietly invalidated, and neither can a diff-scoped auditor.
It found §23.1, §11.1 and Appendix H. Two of the three repairs below come from
it.

**ADR-0093's compactor paragraph is contradicted by five existing passages**,
each verified against primary text rather than taken from an agent:

| Site | Text |
|---|---|
| §20.1 `[R-WRT-01]` | "An appender and **a compactor satisfy every writer requirement** for the bytes they produce" |
| §20.5, its own earlier sentence | "A compactor satisfies every writer requirement for the bytes it produces" |
| `[R-LIF-02]` ¶2 | "**On creation** there is no prior trailer … then performs steps 2–6 … with generation 1" |
| §6.3 `[R-CNT-08]` | "A compactor, **though its output is a new file**, carries the input's unknown ignore-lane bits … rather than writing flags = 0" |
| Appendix H | writer checklist: "follows the commit protocol **including both barriers** (§9.2)" |

ADR-0093's warrant was that the protocol "is stated for a commit". That is true
of `[R-LIF-02]`'s first paragraph and **false of its second**, which is stated
for creation — and a compactor's output is generation 1 with no prior trailer,
which is exactly the case that paragraph states. Its second claim, that the
output's pre-trailer gap is "fixed by nothing", is separately false:
`[R-CNT-09]` SHOULD-bounds the pad.

The reading ADR-0093 took required amending five passages. The reading it
declined required one sentence.

## Decision

**A compactor MUST follow `[R-LIF-02]`'s creation path, as §20.2 obliges a
creator.** The output has no prior trailer and stands at generation 1, which is
the case that path states, and `[R-WRT-01]` already has a compactor satisfying
every writer requirement for the bytes it produces. The pad of step 5 and the
barriers of steps 4 and 6 — both, not one — are owed here as they are of a
creator. That a compaction is a whole-file rewrite rather than a commit
(`[R-LIF-01]`) fixes what the output *is*, not which rules govern writing it.

Round 24's byte-level fork closes on this reading rather than by declaring the
divergence intended: the pad is exactly (−dir_end) mod 64, so two conforming
compactors given one input emit outputs of the same length.

**§23.1 counts three ways, not two.** ADR-0093's shrink half made a third way to
remove sample data reachable — a shrink that turns a stored tile's real
positions into padding without de-addressing it. §23.1's enumeration is
normative and was closed at two. It now names the third, and distinguishes its
consequence: the first two leave the bytes as slack, while the third leaves them
inside a live stored tile as its padding content. That third discloses nothing a
reader could not already derive, because §20.3 step 4 permits the shrink only
where those bytes already hold the channel's recorded fill, which the layer
record publishes.

**§11.1's shrink Rationale names both permitted cases.** It said a shrink is
permitted "where it **only** drops tiles out of the addressed set", which
ADR-0093 made too narrow. It carries no force (`[R-CNF-01]`) but it is the
passage a reader meets first, and all three auditors flagged it.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. Three
propagation acknowledgements, all recording that §20.5 now *relies on* rules it
previously contradicted.

**What two decisions on one question cost.** Round 23 reported this defect and
graded it design-decision; it was deferred to the ledger. Round 24 graded the
identical finding byte-level. The first repair then chose the reading that
required amending five passages, and only the audit caught it. Q-A6 records both
resolutions, the superseded one included.

**The lesson is about the menu, not the choice.** The options put to the
maintainer did not include the five passages that decide the question, because
nobody had looked for them — the search that found them is the downstream
auditor's, and it ran only after the decision was taken. **A decision offered
before the document has been swept for what already answers it is a decision
taken blind.** The sweep is cheap and belongs before the question, not after
the repair.

## Precedent

- §20.2's creation-path sentence, which this now mirrors for the compactor tier
  and which had always been the model available.
- `[R-WRT-01]`'s "satisfy every writer requirement", stated in §20.1 and again in
  §20.5, which is what makes the binding a restatement rather than a new rule.
- ADR-0089's finding that a repair can be correct while the document cannot show
  why — here the inverse, a repair that was wrong while the document had said so
  in five places.
