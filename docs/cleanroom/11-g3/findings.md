# Cleanroom round 11 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent that
returned disclosed its access; none reported a breach.

## Verdict

**One byte-level ambiguity, and it is in ADR-0071's text, one commit old.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings reaching triage | 41 — reader 7, verifier 6, diagrams 10, register 6, adversary 8, quiz 4 |
| **Findings recovered from a dead walk** | **6** (the writer; see below) |
| Distinct defects | **36** (30 triaged + 6 recovered) |
| **Byte-level, after triage and hand-check** | **1** |

## The walk that died

**The writer walk exceeded the structured-output retry cap and returned
nothing** — but it had already written a 57 KB transcript containing six
findings. A dead agent returns null, so all six were absent from the 41 that
reached triage, and no triage pass ever saw them.

They were recovered by reading the transcript from disk. **Two of the six are
the substance of this round.** The `transcript_finding_count` guard added in
round 10 cannot catch this failure: it compares a returned array against a
claimed count, and here nothing was returned at all. What catches it is
checking the workflow's error report and the transcript directory before
reading any conclusion.

## The survivor — `writer-02`, never triaged

ADR-0071 added to §20.3 step 2: *"reject-tile bars reuse of that entry."* It
is defective twice.

Its **trigger cannot produce its outcome**. The bar fires on *"a violation the
open establishes"*, and `[R-RDR-01]` fixes the open as consuming *"the trailer
and directory only — no extent slot's content, no tile index, no payload"*. No
tile-scope violation is establishable there.

And where an appender detects one anyway — which `[R-CNF-12]` licenses — the
bar **collides with step 4** of the same requirement, *"every other entry
byte-identical at its disk-ordinal position"*. No third value is permitted: the
sentinel would be a repair, which the same paragraph forbids. One
implementation emits nothing; another emits a complete generation. Both claim
conformance.

## Also ADR-0071's, also one commit old — `writer-01`

§4.7 claimed *"`fill` is the only semantic field"* while its own broadened
`structural` test reaches *"whether the file, layer or tile is accepted at
all"*. `[R-SER-05]` fixes every padding position's content to the channel's
fill and makes a verifier's acceptance of the tile turn on it — so `fill` is
structural by that criterion, and the semantic class was **empty**: the defect
ADR-0069 fixed for the third class, recreated in the second.

Not byte-level — no requirement branches on the class label — but the document
was asserting something false about itself, and the assertion is what made it
findable. That is the case for keeping self-counting claims.

## The other four recovered findings, adjudicated

No triage pass saw these; each was checked against the text directly.

- **`writer-03`** — Appendix G's *"Four things are not"* is wrong on its own
  criterion: items 2, 4, 5, 6, 8 and 9 each add something outside the four.
  **CONFIRMED, editorial.** Second independent confirmation of a defect round
  10 found and deferred.
- **`writer-04`** — the profile leaves the user-metadata storage encoding open
  (item 1 pins a *codec*, and §10.2 tabulates codec and metadata encoding as
  separate identifier spaces) and never mentions Unicode normalization, though
  `[R-ENC-14]` is a SHOULD and a decomposed name differs in length.
  **CONFIRMED, editorial**; the NFC half is new.
- **`writer-05`** — item 3 does not place record extents relative to the
  per-layer loop, and "ascending record order" is undefined over the union of
  top-level records and sub-records. **CONFIRMED, editorial.** Repeat of a
  round 10 defect, deferred.
- **`writer-06`** — §9.7 enumerates *"the live directory and its records and
  their sub-records, each record's extent, …"* and then checks that *"these
  occupy disjoint byte ranges"*. Read literally every record overlaps the
  directory containing it, so a verifier built from §9.7 rejects every
  conforming file with a record. **CONFIRMED, editorial**, and new: decided by
  `[R-CNT-02]`, whose class list names no "record" class — verified directly.

## The candidate that did not survive

`quiz-02` argued that §20.5's declarative *"carries the greater of
`[R-CNT-26]`'s floor and the input's version_minor"* forks between MUST and
SHOULD, since `[R-CNT-26]` binds "a writer" and "an appender" and §20.1 makes a
compactor a third tier. Downgraded on a link neither the reporter nor the
upholding pass cited: §20.1's *"An appender and a compactor satisfy every
writer requirement for the bytes they produce"* carries the writer SHOULD to
the compactor at SHOULD strength.

## Disposition

All 36 dispositioned. Both ADR-0071 defects and ten editorial repairs land in
[ADR-0072](../../decisions/0072-the-taxonomy-loses-its-middle-class.md): the
taxonomy drops to two classes, §20.3 loses the reject-tile limb, Appendix G's
closing paragraph stops counting and gains a tenth item, item 3 places record
extents and item 9 pins the storage encoding, and §9.7 distinguishes traversal
from claim.

Register and corpus unchanged: **121 conditions over 248 instances, 300
vectors**.
