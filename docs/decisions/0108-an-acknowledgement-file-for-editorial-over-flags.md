# 0108. An acknowledgement file for editorial over-flags

- Status: Accepted
- Date: 2026-08-25
- Covers: `conformance/tools/editorial-acks.txt`; `tarn_editorial.py`'s verdict path
- Confirm: none

## Context

ADR-0104 replaced the per-change ADR for editorial work with a check that proves
a change altered no normative content. Its first real use found the gap: §2.2's
list of requirement-identifier prefixes was turned into a table, and the check
graded it CONTENT.

It was right to, on its own terms. The check compares each section's normative
prose and every table row; content that moves **between** prose and a table looks
like prose removed and rows added, and proving the two are the same content is a
semantic question, not a textual one. Teaching it that equivalence would mean
teaching it that `` `CNF` (conformance) `` and `` | `CNF` | conformance | `` say
the same thing, across every formatting convention the document uses. That is a
much larger tool than the one the check needs to be, and the two changes made to
this tool earlier the same day both shipped with defects.

But ADR-0104 left no path for the case. Its own text says "record the judgement
in the ADR" — and for an editorial commit there **is** no ADR. So a faithful
conversion had a choice between a noise ADR and an unrecorded override, which is
exactly the choice ADR-0104 existed to remove, reappearing one level down.

## Decision

**`tarn_editorial.py` gains an acknowledgement file**,
`conformance/tools/editorial-acks.txt`, on the discipline `propagation-acks.txt`
already uses: an exception is a judgement on the record, not silence. Where the
check flags a difference the author judges to alter no normative content, the
judgement is written down with its reason and the commit proceeds as `editorial:`
with no ADR.

**An acknowledgement is keyed to one exact difference and is single-use.** The key
is a digest over the changed sections' before-and-after prose together with the
table rows added and removed, printed by the check itself when it flags. Any
further edit to the same passages produces a different key and is flagged again.
**A key that could stand for a section would be a licence**, and a licence over a
passage is the opposite of what this file is for — §21.7 and §11.1 are what
standing permission to edit a passage looks like.

Two further constraints, both tested: a key written with no reason is not an
acknowledgement, and a missing file acknowledges nothing.

**What this does not relax.** The check still reports the difference in full
before consulting the file, so an acknowledgement is written by an author who has
read the diff. Register cells remain under the ADR rule (ADR-0104), AGENTS.md
rule 3 is untouched, and every existing gate still runs.

## Consequences

The first entry records §2.2's conversion. Its reason is the form these should
take: the nineteen glosses were transcribed mechanically out of the existing
sentence rather than retyped, so none can have drifted; the whole word-level
difference over the document is one word removed and four added, the four being
`The`, `prefixes` and the two column headers; and the nineteen prefixes in the
table were afterwards cross-checked against the nineteen appearing in requirement
identifiers, with none unused and none missing. **An acknowledgement that cannot
say what makes the change content-free is not one.**

**On the check's own record.** This is the third change to `tarn_editorial.py` in
a day. The first design was wrong in the dangerous direction and was replaced; the
second excluded every blockquote when `[R-CNF-01]` exempts only *labelled* ones,
which an auditor found by reading its briefing against the document. This one
adds four assertions to the self-test — the key is deterministic, a different edit
yields a different and unacked key, a missing file acknowledges nothing, and a
reasonless line is not an acknowledgement — bringing it to twenty. **The pattern
worth naming is that every defect in this tool has been found by something other
than the tool**, which is why the suite grows with each change rather than after.

## Precedent

- `propagation-acks.txt` (ADR-0073), whose discipline this copies exactly: a
  mechanical check whose exceptions are recorded judgements rather than silence.
- ADR-0104, which authorised the class and left this gap; this closes it without
  reopening the per-change ADR it removed.
- ADR-0095's rule about closed claims, applied to the key: an acknowledgement
  scoped to a section would be a standing claim about every future edit to it.
