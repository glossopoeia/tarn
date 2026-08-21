# 0080. The shrink permission takes the bar's tense

- Status: Accepted
- Date: 2026-08-20
- Covers: §20.3 step 4's shrink permission and the stores-no-tile permission;
  §20.5's compactor clauses; §20.4's drop trigger; `[R-CNF-12]` on SHOULD
  deviations; T18's placement axis
- Revises: ADR-0079's shrink paragraph, whose quantifier this corrects
- Confirm: none

## Context

Cleanroom round 16 read round 15's repairs. Its triage found 14 defects and
graded **zero** byte-level, downgrading the one flag its reporters raised.

The downgrade was tested rather than accepted, by an adversarial pass whose
only job was to refute it — and it did. That matters more than the count,
so it is recorded first.

**The downgrade's ground was sound and its scope was not.** All three passes
argued that the disputed shrink leaves a surviving stored tile with wrong
padding content, which is a T4 violation, so the output is nonconforming and
`[R-CNF-05]` bars every conforming writer from emitting it under both
readings — the emittable set does not move. That is true of the
counterexample the reporter chose. It is false of the class the defective
sentence governs.

The refuting construction takes the damaged tile out of the new state.
Shrink an extent so that one stored tile gains padding positions, **and in
the same commit write that tile's index entry as the sentinel.** §3.1: "A
tile is *stored in a generation* if and only if that generation's tile-index
entry for it is not the sentinel", and "Superseded payload bytes from earlier
generations do not make a tile stored." T4's subject is a padding position in
a decoded tile image; an unstored tile has none. Its old bytes become slack,
which `[R-CNT-21]` puts beyond every conformance requirement. **The output is
a conforming file** — so `[R-CNF-05]` bars nobody, only one reading permits an
appender to produce it, and the emittable set moves. Byte-level.

The specification had already conceded the class exists. §21.7, written two
rounds earlier, says "a commit that supersedes every tile it would have
damaged leaves the live state clean, so the bar is unwitnessed there". That
sentence names the sub-class in which a conforming writer is forbidden to
emit a file a verifier would certify.

**The repair written earlier the same day did not close it, and made it
sharper.** ADR-0079's shrink paragraph stated the permission over "any tile
the new state still stores", while the bar it claims to adopt is quantified
over the superseded generation. Those two domains come apart precisely when
the damaged tile is unstored or de-addressed — which is the construction
above.

## Decision

**The shrink permission takes the bar's tense.** A shrink is permitted
exactly where it alters nothing §14 fixes for any tile the layer stores **in
the generation this commit supersedes**. Dropping a tile out of the addressed
set is not such an alteration and never bars a commit on its own; neither
does it rescue one, and neither does unstoring the damaged tile in the same
commit — the quantifier is the prior generation's, which is the whole content
of ADR-0078's decision and is unchanged here. §21.7's acknowledgment that
this is where the bar has no witness is now cited from the rule, so the two
read as one statement.

The **stores-no-tile permission takes the same tense**: a layer that stores
no tile *in the superseded generation* may be re-declared freely. Without
that, a commit could earn the permission by emptying the layer as it
re-declares it — the shrink-to-zero route the adversarial pass found second.

Four further decisions, three of them the maintainer's:

- **§20.5's compactor clauses.** Two byte-level candidates were repairs
  written hours earlier in this same round. "Carried forward as it stands,
  its offset re-pointed like any other" told a compactor two contradictory
  things about one entry; a structurally invalid entry is now reproduced with
  offset and length exactly as they stand, there being no live extent for a
  re-pointing to target (`[R-IDX-03]`), and the violation travels with it
  (`[R-WRT-01]`). And "a record §20.4 does let it drop is no exception" read
  as both *refuse* and *drop*; dropping is now stated as the disposal that
  answers, the prohibition biting on what the output carries.
- **§20.4's drop trigger** (maintainer): "the file's layer set" changes by
  adding or removing a layer **and equally by modifying any layer's record**.
  The cost is recorded rather than argued away — a top-level MU = 0 / PE = 0
  record can now be dropped in a commit that edits a layer record the record
  had nothing to do with, and because PE = 0 that loss is silent.
- **SHOULD deviations** (maintainer): a verifier owes no search for them.
  §2.3's duty to check every file-level requirement runs to the MUST-level
  conditions §21 inventories; a SHOULD deviation is reported where observed
  and not hunted for. This keeps §21 the complete operational inventory the
  corpus and G5 are built on.
- **T18's placement axis** (maintainer): a skippable frame's position is not
  a materially different shape, so T18 collapses to two instances and the
  register returns to **121 conditions over 273 instances**. The three
  placement vectors are retained and re-annotated to the single instance
  rather than retired; extra coverage of real constructions costs nothing.

## Consequences

Round 16's own repairs introduced two of the four byte-level candidates this
ADR closes, both within an hour of being written. That is the sharpest
statement yet of the pattern the gate board records: **a repair is the
least-reviewed text in the document, and repairs to subtle rules are where
the next defect lives.**

The instrument that caught it is worth naming. Three independent triage
passes agreed on a downgrade, each quoting text, and all three were wrong in
scope — not in reasoning. What found the error was a pass whose only
instruction was to refute the downgrade, given the conforming-file
distinction as an explicit test rather than left to judgement. Unanimity
across passes graded the same way is not independent evidence when they share
a premise; the premise has to be attacked separately.

## Precedent

- ADR-0078's tense decision, which this extends to the permission that had
  been stated in the opposite tense.
- ADR-0079's cost argument, unchanged: de-addressing strands only what the
  caller chose to discard.
- §21.7's no-witness class, which turned out to be the load-bearing evidence
  that the byte-level sub-class exists — a passage written to record a
  limitation, doing the work of a proof.
