# 0073. A mechanical propagation check

- Status: Accepted
- Date: 2026-08-18
- Covers: `tarn_propagate.py`; SPEC-07 and SPEC-08 in `tarn_check.py`
- Confirm: extends ADR-0050's tooling scope

## Context

Five cleanroom rounds running, the defect the next round found sat in the
previous round's repair. The shape never varies: a rule is fixed in one place
and the passages restating it are left at the old meaning.

- ADR-0067 made an unimplemented major unjudgeable in §2.3 and §21.6 and left
  §21.2's F1 registering it as a violation. Round 9 found it.
- ADR-0067 added the directory minimums to `[R-ERR-05]` and left Appendix B
  claiming to collect every named constant. Round 9 found it.
- ADR-0071 broadened §4.7's `structural` until it swallowed `fill`, and left
  §4.7 asserting `fill` was the only semantic field and §13.1 calling it
  semantic. Round 11 found it.
- ADR-0071 wrote a reject-tile bar into §20.3 step 2 that step 4 of the same
  requirement contradicts. Round 11 found it.

None of these needed twelve agents and an hour. Each is two passages sharing
the terms of one rule, changed in one and not the other. ADR-0071 was written
in explicit awareness of the pattern and produced two more.

## Decision

**`tarn_propagate.py` checks a change against the document**, where
`tarn_check.py` checks the document against itself at rest.

For each changed hunk in `spec/tarn.md` it extracts the rule's *anchors* — the
requirement identifiers and register rows it cites, the field and structure
names it uses, the terms it emboldens, and its distinctive three-word
phrasing — then reports every other passage carrying enough of the same
anchors, and whether that passage was changed too. A site that shares a
change's anchors and was not changed with it exits 1, unless the pair is
recorded in `propagation-acks.txt` with a reason.

Three design choices earn their keep:

**Markup is not part of the term.** A field written `` `fill` `` in one
passage and "the fill value" in another is one anchor. That exact pair is how
§4.7 and §13.1 drifted apart, and the first draft — which matched backticks —
did not see it.

**Anchors must discriminate.** A term appearing on 2–12 lines names something
in particular; `slack` appears on forty and links nothing. The same judgement
bands the phrase index at 2–6 occurrences.

**Two register rows restating each other are not a propagation failure.**
§21.1 licenses the register to restate its rules and REG-01..08 own that
relationship. Without the exclusion, one renumbering buries the real findings:
ADR-0067's sweep produced fourteen row-to-row pairs above the two defects the
next round actually found.

**SPEC-07 checks the document's claims about its own contents.** §4.7 states
its own membership — "`version_minor` is the only descriptive field" — which
is the strongest kind of sentence a specification can carry, because it can be
falsified. SPEC-07 falsifies it: it counts the class cells, checks the named
field carries the class it claims, and fails a class the taxonomy names that
no field carries — the defect ADR-0069 fixed for `informative` and ADR-0072
for `semantic`.

**SPEC-08 checks Appendix B against `[R-ERR-05]`.** An index that claims
completeness is checkable against what it indexes. It warns rather than fails,
being a heuristic over prose.

## Consequences

Validated against the revisions where the defects existed, which is the only
test that means anything for a check written after the fact:

| Revision | Check | Result |
|---|---|---|
| `033ef41` (ADR-0071) | SPEC-07 | **FAILS** — "§4.7 says `fill` is the only semantic field, but 0 table cell(s) carry that class" |
| `f051626` (ADR-0067) | SPEC-08 | **warns** — "`[R-ERR-05]` names 'dir_offset'; Appendix B does not carry it" |
| `033ef41` (ADR-0071) | propagate | flags §13.1 line 1616 on the shared term `semantic` |
| `f051626` (ADR-0067) | propagate | flags §21.2's F-row region from §21.6's changed paragraph |
| HEAD | all | clean |

The first draft of SPEC-07 passed the revision it was written to fail, because
the sentence it tests is hard-wrapped — at ADR-0071 it read "is the\nonly
semantic field" — and the pattern was line-oriented. That is hazard one of
this project's own list, committed by the check written to enforce it. Both
checks now normalise whitespace before matching, and the episode is recorded
here because the next person to write a pattern over this document will make
the same mistake.

Honest limits. The propagation check is a term-overlap heuristic: it will not
see a contradiction between two passages that share no vocabulary, which is
why §20.3's step 2 against step 4 does not surface — the two steps share
almost no distinctive terms, and the collision is semantic. It will also flag
sites that are fine, which is what `propagation-acks.txt` is for; an
acknowledgement is a judgement on the record and an unreasoned one silences
the instrument. And neither check replaces a cleanroom round: they catch the
propagation class, which is most of what the last five rounds found, and
nothing else.

## Precedent

- ADR-0050's scope for specification tooling: reads the spec, reports, never
  writes and implements no part of the format. `tarn_propagate.py` holds to it.
- ADR-0064's instance identity, which made a mis-annotated vector a hard
  failure rather than a silent one — the same move, applied to prose.
