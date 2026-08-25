# 0098. Round 25's four checkable repairs, and §21.2 goes to the ledger whole

- Status: Accepted (dispositions round 25's findings)
- Date: 2026-08-25
- Covers: §23.1's shape citation; §9.6's row list; §11.1's growth Rationale;
  L41's antecedent; the disposition of round 25's remaining findings
- Revises: a citation ADR-0097 wrote
- Confirm: none

## Context

Round 25 returned **zero byte-level over 26 findings** — 21 through its own
triage and five recovered from a walk whose structured return was lost. The
document was swept before any repair or menu, which is the step ADR-0094
recorded as missing and ADR-0096 first supplied.

**Four findings needed no action.** Three reporters independently re-found the
question already open as **Q-H4**; two re-found **Q-I4**, now reported in three
consecutive rounds; one re-found a round-24 deferral; and one was graded
not-a-defect by triage. That is four of eighteen decided by reading.

**One of the repairs corrects a defect written the previous day.** ADR-0097
added a sentence to §23.1 citing "§20.3's shape (c)" for a user-metadata edit.
§20.3 says, in terms: *"Editing user metadata **is not this shape**: its
document lives in an extent, so a new extent is appended and the old one becomes
slack, **as in (b)**."* The citation named the one shape the document explicitly
rules out — in the same sentence ADR-0097 added to close a different finding
about that same paragraph.

## Decision

**Four repairs, each checkable against a named rule or against arithmetic.**

§23.1 now says §20.3 places a metadata edit with shape **(b)**.

§9.6 cited §21.2 rows F8 and F17 for a failure of `[R-CNT-06]`'s gates and
omitted **F14**, the trailer CRC — one of the three ordered gates, and squarely a
way the final 64 bytes fail to be a valid trailer. The citation now names all
three and says what each is.

§11.1's Rationale asserted that growth raising a grid count changes
`entry_count`. That is false where another dimension's grid count is 0: (2,0)
grows to (3,0) and the product stays 0, so no entry is added and no index region
is re-emitted. The Rationale now carries the exception.

L41's condition read "the previous stored tile's offset plus **that tile's**
length", with two available antecedents — and on one of them the row is
unsatisfiable. It now says "the previous stored tile's length".

**§21.2's preamble goes to the ledger whole, as §21.7 did.** It has drawn
findings in **three consecutive rounds**: round 23's `verifier-01`, round 24's
`register-01` and `quiz-03`, round 25's `reader-01`/`diagrams-02`/`register-01`
— three walks at once — and `quiz-01`. Q-H4 and Q-H5 already carve pieces off it
without asking whether its design can work.

**Q-H6** asks that. The paragraph offers an *excusing* property ("rows whose
subject is that file's geometry do not reach it") and an *excepting* property
("their subject is a field fixed across every major"), and **they are not
complements**. `[R-CNT-27]`'s 128-byte floor satisfies neither — its subject is a
physical size — which is why ADR-0090 tried to place it, ADR-0091 reverted that
against five contradicting passages, and round 25 found it again independently
from three walks. A fourth patch would repeat what §21.7 taught: four repairs in
four days, clusters every round, until the section went to the ledger as Q-I5.

**Four further design questions become ledger entries**, per AGENTS.md rule 3:
**Q-C7** (what a partial slack total is when the rejection is at file scope — the
recovered `verifier-01`, with its three candidate values and its
exact-versus-partial label axis), **Q-B6** (whether step 4's bar reaches a
channel's sample type and the channel order), **Q-B7** (whether adding a record
is an independent change licensing a drop), and **Q-I6** (why Appendix G pins
codec, filter, alignment and slab but not tile extents or channel layout, on the
same argument).

**Eleven findings are deferred with named owning sections**, recorded in round
25's findings.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. None of
the four repairs changes a condition's extension — L41's disambiguation selects
the reading under which the row is satisfiable, which is the reading its
instances already exercise.

**What the sweep is worth, measured a second time.** Round 24's sweep resolved
two findings without a repair, prevented one wrong repair, and separated one
question from a ledger entry it would have been folded into. Round 25's resolved
four without a repair. Two rounds, six findings decided by reading, at the cost
of a few greps.

**And what it did not catch.** The sweep is run against the findings; it does not
re-read the previous day's repairs looking for what they broke. ADR-0097's
shape-(c) citation was found by a fresh-context round, not by the sweep and not
by the audit that read that very diff — the audit checked whether the sentence's
*claim* was true and not whether its *citation* landed. That is check 2's
territory and it was run; the citation was to a labelled sub-part of an Example,
which no `[R-CNF-01]` check flags because the Example is not where the defect is.

## Precedent

- ADR-0096's rule that a finding is dispositioned only after the document is
  swept for what already answers it — applied here for the second time, with the
  same yield.
- ADR-0096's decision to send §21.7 to the ledger whole rather than patch it a
  fifth time, which is the model for Q-H6.
- ADR-0091's rule that a repair which must invent a warrant is a decision, which
  is why four design questions became entries rather than edits.
