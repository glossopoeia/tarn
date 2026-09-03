# 0116. §21.7's walk-through is cut, exercising the option ADR-0115 retained for exactly this

- Status: Accepted (exercises ADR-0115's retained option (d))
- Date: 2026-09-02
- Covers: §21.7's `> **Rationale.**` block
- Supersedes: nothing. ADR-0115's decision stands; this exercises a fallback it
  reserved and states the condition that triggered it.
- Confirm: none

## Context

ADR-0115 demoted §21.7's 926-word inventory to a block labelled *Rationale*,
which `[R-CNF-01]` strips of force, and retained cutting it as a further step —
in its own words, **"Retained as a further step if the walk-through keeps drawing
findings even without force: it could be cut rather than demoted."**

That condition is now met, and the evidence is four consecutive audit passes over
three revisions of the text.

| Pass | Reported inside the block |
|---|---|
| Round-29 pre-audit | the fills item (two lanes, **confirmed**); the lead-in's completeness claim (**confirmed**) |
| Repair audit | the fills item again — **the repair of it** (**confirmed**) |
| Second repair audit | the anaphor in that second repair; a neighbouring sentence false at P = 1; the walk-through omitting insertion and non-final removal |
| Driver-grade full-surface audit | the same-plane-length restriction dropped; the block counting three trailer obligations where §20.5 counts two |

**Three defects confirmed by adversarial verification, five further reports, and
one sentence defective in three successive versions.** The fills item was wrong as
ADR-0115 left it, wrong again after the repair that closed that finding, and
reported wrong a third time after the repair that closed *that* one. Each repair
was written by someone holding the previous finding in mind, and each introduced
a narrower error than the one it fixed: first an unconditional claim, then a
layer-scoped condition where the property is per-channel, then a two-element
anaphor over a set the bar lets exceed two.

**None of it was ever byte-level, and after ADR-0115 none of it could be.** The
block binds nothing. Every pass spent agents on text whose defects cost the
document nothing, while the block's own terms already conceded the position: *"an
item found stale — or an obligation the list omits — is a defect in this block and
not in the register."*

## Decision

**The block is cut.** §21.7 ends at `[R-ERR-01]`, with the test, its two
definitions, the subject rule and the unwitnessed/unviolatable distinction — 525
normative words — and no illustration.

**The split**: 830 illustrative words removed, 525 normative words unchanged.
Before ADR-0115 the section was 926 normative words and no illustration; it is now
525 normative words and no illustration, and everything the register turns on is
in the 525.

**Nothing is orphaned, and this was checked mechanically rather than asserted.**
Every rule identifier the block named — eight of them — and every register row
label it named — T2, T3, T4, T5, T14, T15, T17, T23, T25, T26 — occurs elsewhere
in the document. No requirement, row or section loses its only mention.

**No normative text depended on it.** The two normative passages that cite §21.7
for a conclusion — §20.3 step 4's shrink paragraph and §20.5's `[R-WRT-06]` — were
put to an adversarial verifier on exactly this question. Each states its
conclusion itself, in unlabelled normative prose, together with its ground, and
cites §21.7 as *recording* it rather than as its authority; and the test that
yields the conclusion is in §21.7's normative body, not the block. The finding
that argued otherwise was refuted on the text.

## Consequences

**The section keeps the property ADR-0115 bought and stops paying for it.** That
decision's argument was that a test decides membership without appeal to a list.
The list survived it as illustration, and the illustration is what four passes
found defective. A test that decides any condition put to it does not need a
worked list to be usable, and the list has now demonstrated that it cannot be kept
correct across revisions of the rules it illustrates.

**What a reader loses is a worked example, and what they gain is not being misled
by a stale one.** Three of the reports above are cases where the block said a
condition *was* witnessed and it was not, or gave a condition narrower than the
rule. A reader reasoning from those reaches the wrong answer; a reader applying
the test does not.

**The register does not move**: 120 conditions, 275 instances, 329 vectors. The
block carried no rows and sits outside §21.1's instance arithmetic, as §21.7 has
throughout.

**A defect class disappears rather than being repaired.** Five of the eight
reports across those four passes are now moot, not fixed — they were defects in
text that no longer exists. This is recorded plainly because a future reader
counting repairs will otherwise find them unaccounted for.

## Alternatives rejected

- **Repair the outstanding findings and audit again.** Rejected on the record
  above: three passes have each closed the previous pass's findings in this block
  and produced new ones, and two of those new ones were introduced by the repairs
  themselves. ADR-0106 states the governing rule — when a passage has been false
  twice, stop repairing the sentence and ask what it is for.
- **Leave the findings standing as known-stale illustration.** Defensible, since
  the block binds nothing and says of itself that a stale item is its own defect.
  Rejected because a walk-through that is known to be wrong in five places is
  worse than none: it reads as authority to anyone who has not read this ADR, and
  the section's whole difficulty has been readers taking the account for the rule.

## Precedent

- **ADR-0115** reserved this option, named the trigger, and the trigger is what
  fired. This is the reserved step being taken, not a reversal.
- **ADR-0106**, on a passage that had been false twice: delete rather than repair
  a fifth time. ADR-0113's motivating paragraph went the same way in this cycle.
- **ADR-0095**'s property-over-list rule, of which this is the completion: ADR-0115
  made the property govern and kept the list; this removes the list.
