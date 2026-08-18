# 0072. The taxonomy loses its middle class, and the appender its dead limb

- Status: Accepted
- Date: 2026-08-18
- Covers: §4.7's field classes; §20.3's reject-tile limb; Appendix G's
  closing paragraph, emission order, encoding and normalization; §9.7's
  claimant enumeration
- Confirm: amends ADR-0071 in both of the places round 11 found

## Context

Cleanroom round 11 read the 85 lines inserted and 51 deleted since round 10.
Its quiz came back 15 agree / 0 diverge / 0 underdetermined for the fifth
round running, and its 41 triaged findings reduced to 30 defects with none
byte-level.

**The writer walk died** — its structured return exceeded the retry cap — and
it had already written a 57 KB transcript carrying six findings, none of which
reached triage. They were recovered by hand from disk. Two of the six are the
substance of this ADR, and both are defects in ADR-0071, one commit old. That
is the fifth round running in which the defect found sat in the previous
round's repair, and ADR-0071 was written in explicit awareness of the pattern.

## Decision

**The field taxonomy drops to two classes.** ADR-0071 broadened `structural`
to "determines anything a conforming reader or verifier does with the file's
bytes — where a byte lies, how it decodes, or whether the file, layer or tile
is accepted at all", and then claimed `fill` was the only semantic field. The
two cannot stand together: `[R-SER-05]` fixes every padding position's content
to the channel's fill and makes a verifier's acceptance of the *tile* turn on
it, so `fill` meets the acceptance leg and is structural. The semantic class
was therefore empty — the defect ADR-0069 had just fixed for the third class,
recreated in the second within one commit.

§4.7 now classifies by what a field's value determines, in two cases:
**structural** if it determines where a byte lies, how it decodes, what a
decoded value is, or whether the file, layer or tile is accepted; and
**descriptive** if none of those. `version_minor` remains the only descriptive
field. §13.1's gloss is corrected to say `fill` is structural and why.

The alternative — sharpening the acceptance leg so it reaches only fields
whose *values* this specification constrains, keeping `fill` semantic — was
considered and rejected. It would have preserved three classes at the cost of
a line drawn nowhere else in the document, and the taxonomy's operative
content is one bit: is this field inert? Two classes carry that bit exactly.

**§20.3 loses its reject-tile limb.** ADR-0071 wrote that "a violation the
open establishes bars the commits its outcome bars and no others: reject-file
bars every commit, reject-layer bars a commit that modifies that layer,
reject-tile bars reuse of that entry." The third limb is defective twice over.
Its trigger cannot produce its outcome: `[R-RDR-01]` fixes the open as
consuming *"the trailer and directory only — no extent slot's content, no tile
index, no payload"*, so no tile-scope violation is establishable there. And
where an appender detects one anyway — which `[R-CNF-12]` licenses — the bar
collides with step 4's *"every other entry byte-identical at its disk-ordinal
position"*, leaving no permitted value: the sentinel would be a repair, which
the same paragraph forbids.

The limb is struck, and §20.3 now says positively what happens: the open
establishes no tile-scope violation, and a malformed entry met while
re-emitting a region is carried forward byte-identically under step 4, not
repaired. That is the line ADR-0068 and ADR-0071 already take everywhere else —
an appender carries defects forward rather than repairing or dropping them.

**Appendix G's closing paragraph stops counting.** It claimed "Four things are
not [already mandatory]" while items 2, 4, 5, 6, 8 and 9 each add something
outside that four — item 6's sentinel-for-every-all-fill-tile most of all,
since no rule requires an all-fill tile to be unstored and it changes which
tiles exist. Round 10 found this and it was deferred; round 11's writer found
it independently. The paragraph now names what the items are for rather than
how many there are, and lists them without a count.

Three further profile gaps close with it, all found twice or new this round:
item 3 places record extents after every layer's tiles and index region rather
than interleaved, and states the order over top-level records then
sub-records; item 9 pins the user-metadata storage encoding and, at encoding 2,
the zstd producer, which item 1 reaches only for tile codecs since §10.2
tabulates the two identifier spaces separately; and a new item 10 requires
Unicode NFC, which `[R-ENC-14]` states as a SHOULD and which changes a name's
byte length — §4.6's `température` is 12 bytes in NFC and 13 in NFD.

**§9.7 stops reading as though records were claimants.** Its enumeration ran
"the live directory and its records and their sub-records, each record's
extent, …" and then checked that *"these occupy disjoint byte ranges"*. Read
literally, every record overlaps the directory that contains it, and a
verifier built from §9.7 — the section that operationalises the check —
rejects every conforming file that has a record. `[R-CNT-02]` decides it, its
class list naming the front block, stored-tile extents, record extents, the
directory and the trailer, with no "record" class. §9.7 now distinguishes
traversal from claim, and says so in terms.

## Consequences

Register and corpus unchanged: **121 conditions over 248 instances, 300
vectors**, 100% coverage. Twelve spec edits.

Priced knowingly. Retiring the semantic class leaves a two-way split whose
second class holds one field, which reads thin — but it is true, checkable,
and it was a self-counting claim of exactly this kind that surfaced the defect
within one round of ADR-0071 writing it. Striking the reject-tile limb means
an appender extends a file carrying a malformed index entry and reports it
rather than refusing; the entry stays malformed and the tile stays
unreadable, which is the append-only model's standing bargain. And Appendix G
gains a tenth item and loses its count, which makes the profile longer and the
paragraph that summarises it weaker as an audit aid.

## Precedent

- ADR-0069, whose repair of an empty residual class this repeats for the class
  next door — evidence that a taxonomy asserting its own membership is worth
  having precisely because it can be falsified.
- ADR-0071's own line that an appender carries defects forward, here completed
  for the case its new text had contradicted.
- ADR-0057's rule that a register row describes an observable state, applied
  by analogy: a clause whose trigger cannot produce its outcome is not a rule.
