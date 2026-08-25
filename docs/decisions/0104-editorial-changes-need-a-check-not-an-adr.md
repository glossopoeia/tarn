# 0104. Editorial and placement changes need a check, not an ADR

- Status: Accepted
- Date: 2026-08-25
- Covers: CONTRIBUTING's "spec changes cite their ADR" rule, as it applies to
  changes that alter no normative content; `conformance/tools/tarn_editorial.py`
- Confirm: none

## Context

CONTRIBUTING says: "every pull request that changes normative text links the ADR
that governs it." That is right for decisions. Applied to readability work —
rewording a normative sentence that means the same thing, moving a rule to the
section it belongs in, splitting a paragraph that has grown two subjects — it
forces a choice between ADRs that record no decision and an exception nobody
wrote down. Ninety-nine ADRs in, the trail's value comes from every entry
recording a real call; padding it with "moved a sentence" is a cost to every
future reader of it.

Note how much of the document is already outside the rule. `[R-CNF-01]` puts
Note, Rationale and Example blocks outside normative text, and those are **18.5%
of the specification's non-blank lines**; headings, section ordering and
hard-wrapping are not normative text either. Restyling any of that never needed
an ADR. What the rule actually bites on is normative sentences and where they
sit.

**The difficulty is that "this changes no meaning" is the claim this project has
got wrong more often than any other.** In one week: ADR-0097 found a gloss that
ADR-0096 had reworded from an accurate form into a false one; ADR-0098
disambiguated a pronoun in a register row and left the identical pronoun
standing in the rule the row restates; ADR-0099 restated a Rationale onto a
quantity that does not decide the question, and the audit called that half a
regression; and round 26 found the single word *last* ambiguous, from five
independent readers at once. Every one of those was offered as a clarification.

So the author's judgement about their own edit is the wrong instrument. It is
also the only instrument a per-change ADR actually supplies, since an ADR saying
"this is editorial" records the same unchecked claim at greater length.

## Decision

**Editorial and placement changes to `spec/tarn.md` may land without a per-change
ADR.** This ADR is the decision AGENTS.md rule 2 requires, made once for the
class rather than once per edit.

**The per-change ADR is replaced by `conformance/tools/tarn_editorial.py`**,
which proves the property instead of asserting it. It compares **each section's
normative prose, concatenated and whitespace-normalised** — blockquotes excluded
as non-normative under `[R-CNF-01]`, table rows excluded from the prose and
compared separately and exactly — and returns one of three verdicts.

Comparing a whole section as one string is what makes the check useful for
readability work: re-wrapping a paragraph, splitting one paragraph into two and
merging two into one are all invisible, while text that moves between sections is
caught.

- **EDITORIAL.** Every section's normative prose is unchanged and so is every
  table row. Commit with an `editorial:` subject and no ADR.
- **PLACEMENT.** The document's normative sentences are exactly the same
  multiset, but some sit in a different section. Allowed on the same terms, and
  reported separately because **placement is not content-neutral in this
  document**: `[R-ENC-04]` as ADR-0102 wrote it reaches quantities designated by
  "the section that defines" them, §2.4 assigns owning scope by structure, and
  §21.1 subordinates a register row to the rule it cites. The tool names every
  sentence that moved, the identifiers inside it, and marks those carrying
  location-sensitive wording, so the mover checks them.
- **CONTENT.** Normative prose or a table cell changed. This needs an ADR, and
  the tool prints the differing sentences and any BCP 14 keyword movement so the
  author can see whether it is substance or markup.

**The check is only worth its authority if the check itself is checked**, so
`--selftest` runs fifteen assertions: four historical commits whose answers are
known from their own ADRs, five sections of ADR-0102's commit that a rejected
earlier design missed, and six mutations of the current document exercising all
three verdicts. It is wired to run with the other gates.

The existing gates are unchanged and still run: `tarn_check`, `tarn_build
--selftest`, `tarn_vectors --verify`, `tarn_propagate`, and the lineage gate.
An editorial commit is subject to all of them, and to `tarn_chain` — an editorial
change still lands in the audit chain, because a claim that a change is editorial
is exactly the claim a fresh reading is good at falsifying.

**What this does not relax.** Register cells stay under the ADR rule: §21.1 makes
a row's wording answerable to the rule it cites, and ADR-0096 and ADR-0097 were
both cell edits that turned out to decide something. Nor does it relax AGENTS.md
rule 3: a change that requires deciding what a rule reaches is a decision however
small its diff, and ADR-0091 governs.

## Consequences

CONTRIBUTING gains the exception in its own words, pointing here, so a
contributor reading it is not left to infer the rule from commit history.

The burden moves from the author to the tool, which is this repository's
established answer to exactly this shape: `SPEC-03` for the normative register,
`tarn_propagate` for unswept restatements, `tarn_chain` for unaudited repairs.
Each replaced a judgement nobody was making reliably with a check that runs.

**A rejected design, recorded because it failed in the direction that matters.**
The first implementation keyed normative text by the `[R-XXX-NN]` identifier
ending each requirement, which looked natural and was wrong. Identifiers are not
only definitions: they appear as citations too — 265 parenthetical and 37
possessive occurrences against 152 that end a line — and because the document is
hard-wrapped, a requirement's closing identifier routinely shares a line with the
*next* requirement's opening words, so no punctuation rule separates the two
cases. Keying by identifier let the last citation in document order silently
overwrite the definition. Run against ADR-0102's commit it found **one of five**
changed passages, attributed it to two requirements defined in other sections,
and missed `[R-ENC-04]`'s own rewrite entirely; it returned CONTENT only because
a citing paragraph happened to change in the same commit. Had that commit touched
only §4.2, §11.2, §11.3 and §20.3 it would have returned **EDITORIAL on the
rewrite of a rule that had just forked the emittable set.**

Two things follow. The first is the design above: comparing whole sections needs
no attribution, so the failure has no way to occur. The second is the self-test,
and it is the more important. **A guard shipped without a test of the guard is
the assurance it exists to replace** — the first version was demonstrated on a
clean tree, where EDITORIAL was the only answer it could give and a tool
hardcoded to print EDITORIAL would have passed identically. The suite now
includes cases of every verdict, because a suite of CONTENT-only cases would pass
for a tool that always said CONTENT. This is ADR-0081's lesson about instruments,
applied to the instrument rather than to the document.

**The tool's limits, stated so they are not discovered later.** It compares text,
so it cannot see that a moved rule now reads differently in its new neighbourhood
— that is what the PLACEMENT verdict's checklist is for, and it is advisory. It
treats a table cell change as CONTENT even when it is only markup, which
over-flags rather than under-flags, deliberately. And it says nothing about
whether the new wording is *better*; it says only that the old meaning survived.

## Precedent

- `tarn_propagate.py` (ADR-0073) and `tarn_chain.py` (ADR-0100), both of which
  replaced a manual discipline with a mechanical one after the manual version was
  measured failing.
- `[R-CNF-01]`, which already places 18.5% of the document outside the rule this
  ADR relaxes, and so establishes that the rule was never meant to reach
  everything in the file.
- ADR-0091's rule that a repair which must decide a rule's reach is a decision —
  the boundary this ADR does not cross.
