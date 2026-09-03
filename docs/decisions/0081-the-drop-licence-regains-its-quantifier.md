# 0081. The drop licence regains its quantifier, and ADR-0070 is superseded

- Status: Accepted; the §20.4 drop gate it made operative superseded by ADR-0120, its other decisions standing
- Date: 2026-08-21
- Covers: §20.4's MU = 0 / PE = 0 cell; §23.1's removal appositive; §21.7's
  codec witnesses; Appendix G item 3's first structure; `SPEC-03`'s scope
- Supersedes: ADR-0070, whose decision ADR-0080 reversed without recording it
- Confirm: §20.5's compactor disposal — confirmed by ADR-0082

## Context

This decision comes from a **repair audit**, not a cleanroom round: a
spec-only pass over the ten hunks of round 17's repairs, run before round 18
launched, one auditor per two or three hunks plus a cross-hunk pass, each
finding adversarially verified and every surviving byte-level downgrade
attacked by a refuter.

The lever was aimed at a pattern the gate board records: rounds 14–17 each
found their defect in the *immediately preceding* round's repair, three of
them in §20.3 step 4. Running another round of the same shape had not broken
that. Auditing the repairs before the round did.

**The audit found three things a cleanroom round structurally cannot.**

### 1. The ADR trail and the spec had come apart

ADR-0070, *A supersede-only commit drops nothing*, is `Status: Accepted` and
says "a commit whose only change is a supersede MUST retain the record."
ADR-0080 then widened §20.4's drop trigger so that a commit changes the file's
layer set "equally by modifying any layer's record" — which a supersede does,
since `[R-LIF-01]` forces the index region to a new placement. That reverses
ADR-0070. **ADR-0080 does not list ADR-0070 in its Revises field, and no ADR
supersedes it.**

Round 17 then found the resulting contradiction *inside the spec* — MAY drop
against MUST retain in one cell — and resolved it in ADR-0080's favour by
deleting the carve-out. Correctly. But `git log 08b9b9d..a42d0b6 --
docs/decisions/` is **empty**: round 17 changed 32 lines of normative text,
including deleting a MUST and widening a MAY, and recorded no ADR.

No cleanroom agent could have found this. Every one of them reads
`spec/tarn.md` and nothing else — that is the gate's whole design — and a
disagreement between the spec and the decision trail is invisible from inside
the spec.

### 2. The repair's conclusion outran its own premise

§20.4's cell states the drop rule as a **scope-matched, kind-split gate**: a
layer sub-record's qualifying change must be to *that* layer; a top-level
record's may be to the layer set or another non-layer top-level record. Round
17's repair then drew its conclusion with no such match — "an appender
superseding a tile MAY drop **the record**" — where "the record" is the row's
generic subject. Read as written it licenses dropping layer B's unknown
sub-record in a commit that touched only layer A, which the premise it is
derived from does not support. Round 16's deleted sentence had carried the
quantifier explicitly ("not such a change **for either kind**"); the
replacement dropped it.

Three verifiers judged this not byte-level. A refute-only pass overturned all
three downgrades, and the deciding fact is one none of them weighed: **the
gate is lowercase and the conclusion is ALL CAPS.** §2.1 binds BCP 14 keywords
"when, and only when, they appear in all capitals". So the operative
permission was an unbounded `MAY`, and the restriction meant to bound it was
not a BCP 14 keyword at all. The document states precedence wherever it wants
it — §21.1's "the rule governs", `[R-EXT-05]`'s "the section that defines the
space governs" — and states none here.

### 3. The gate that should have caught it was blind to the passage

`SPEC-03` enforces AGENTS.md rule 5, BCP 14 keywords in ALL CAPS. Its
normativity test exempted **every line beginning with `|`**, justified on the
ground that "tables carry restatements whose wording §21.1 subordinates to the
rule." That is true of §21's register tables and false of §20.4's obligations
table, which is the *only* statement of the updater's drop rule in the
document.

Measured: the entire specification contained exactly **two** lowercase BCP 14
verbs inside table rows, and **both were in §20.4 line 3123** — the cell that
has produced the byte-level defect in rounds 10, 14, 16 and 17. The blind spot
was one cell wide and pointed precisely at the document's most defect-prone
passage.

## Decision

**The gate becomes operative and the conclusion regains its quantifier.**
§20.4's MU = 0 / PE = 0 cell now reads "An appender **MUST NOT** drop it
except in a commit that *independently* changes the scope the record attaches
to", and the supersede conclusion is scope-matched: an appender superseding a
tile MAY drop **a top-level such record, or such a sub-record of the layer
whose tile it superseded**. The rule ADR-0080 decided is unchanged; what
changes is that it is now stated in BCP 14 and bounded where it was always
meant to be bounded.

Three further corrections in the same cell: the scope list names "any layer
record's content" directly rather than claiming the *layer set* changes when a
member's contents change; the self-citation "(§20.4)" from inside §20.4
becomes `[R-CNT-22]`, §7.3, which is the actual ground; and the stranded
"either" — left pointing at a clause whose polarity the repair inverted — is
gone, along with the three-deep em-dash nesting.

**ADR-0070 is superseded**, formally and late. Its decision has not been the
document's rule since ADR-0080.

**`SPEC-03` becomes section-aware.** A table row is exempt only inside §21,
where §21.1 subordinates a row's wording to the rule it cites. Elsewhere the
row is checked. Run against the pre-repair document the patched check reports
exactly the two hits above and nothing else.

Three sweeps the repair audit confirmed, unrelated to the drop rule:

- **§23.1** said superseding data is "the only removal a commit performs".
  The drop licence makes that false, and §23.1 is where this document reasons
  about what survives as slack — so it now names the record drop as the one
  other removal.
- **§21.7** said a declaration change reaching "the decoded size or the codec"
  is witnessed by T3 or T14. True of the size; wrong of the codec in most
  directions — T14 is gated on codec 1, and a re-declaration away from codec 1
  is witnessed by the rows for the codec now declared (T15, T17, T23, T25).
- **Appendix G item 3** pinned the first structure to offset 16 flatly, while
  item 5 permits a fixed declared alignment. `[R-SLB-01]` bounds A at
  512 ≤ A ≤ 2⁶², and 16 is a multiple of no such A, so the profile's own
  emission order made its first structure unplaceable. The alignment exception
  now reaches the first structure too.

## Left open

**§20.5's compactor disposal is not decided here.** ADR-0080 decided that a
structurally invalid index entry is *reproduced* and its violation travels;
round 17 reversed that to *MUST refuse*, again with no ADR. The audit found
the reversal's *argument* faulty in three ways — it glosses `[R-WRT-01]` at
region granularity where §20.3 step 2 glosses the same rule at entry
granularity, it reads "in full" into §20.1's sentence whose second clause is
the very carve-out it omits, and it states the obligation unconditionally
three clauses before conceding "a compactor need not have looked". Its
*conclusion* may still be right: §20.5's untouched text already compels
refusal for a violation the compactor has detected, and regenerating a region
arguably forces detection. Which of ADR-0080 and round 17 governs is the
maintainer's call, and the passage is left as round 17 wrote it until it is
made.

## Consequences

The pattern that has held for four rounds — the next defect lives in the last
repair — was met by moving the check earlier rather than by running the same
round again. It found a byte-level defect in round 17's repair before round 18
read a line, and two defects of a kind seventeen rounds could not reach.

**The instrument's own reading is the durable lesson.** Thirty-one audit
findings were adversarially verified by agents instructed to default to
REFUTED, and that instruction produced **zero** byte-level — the same shape as
round 16, and wrong the same way. Every one of the four byte-level downgrades
fell to a refute-only pass. A verifier told to default to a verdict shares a
premise with every other verifier told the same thing, and the refute phase is
not optional after a zero. It is what a zero means.

## Precedent

- ADR-0080's widened drop trigger, whose substance is unchanged here and whose
  unrecorded reversal of ADR-0070 this ADR closes.
- ADR-0034's cleanroom protocol, which this extends: the round tests the
  document, and a repair audit tests the repairs, because the two find
  different classes of defect.
- §2.1's casing rule, which turned out to be load-bearing: a restriction that
  is not in capitals does not bound a permission that is.
