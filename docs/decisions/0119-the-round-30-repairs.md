# 0119. Round 30's repairs, and the repair round 29 recorded and never made

- Status: Accepted (resolves round 30's repairable findings)
- Date: 2026-09-03
- Covers: §14.2 `[R-SER-02]` and §17.2's Note; §21.3 rows L2 and L23; §21.6's
  table; §14.2 `[R-SER-08]`; §18.2 `[R-MTA-05]` and Appendix G item 3; §9.2's
  conduct paragraph; §20.3 step 4's re-type consequence; §2.3 `[R-CNF-11]` and
  §17.4 `[R-COD-11]`; §18.2's Note beneath `[R-MTA-09]`; Appendix G's closing
  paragraph
- Confirm: none

## Context

Round 30 read round 29's repairs — the second half of G3's criterion — and
returned 19 findings from 7 reporters, 14 distinct defects, and **two reporter
flags byte-level, each upheld by at least one triage pass and attacked by the
refute phase as a split.**

**One is Q-B7**, open since round 25 and byte-level since round 27, found cold
for the sixth time: whether adding a non-layer top-level record is a change to
*"another non-layer top-level record"* that licenses a PE = 0 drop. The round
adds nothing to the ledger's standing and is recorded there.

**The other is round 29's own finding, unrepaired.** Round 29's one byte-level
flag asked whether a planar layer derives P · Q for `[R-ENC-04]`'s overflow
ceiling, since §14.2's summary sentence carries no layout qualifier; it was
settled not byte-level by two blind checkers and a hand-check, and the findings
recorded the reporter's one-clause repair as the right disposition. ADR-0118's
Context then states that §14.2's layout qualifier was "repaired with decision
2". **No commit made that repair**: `0790131` did not touch §14.2, and nothing
after it did. Round 30's reader found the same sentence cold, built the same
construction — planar, one extent 0, T = 2⁵², 4,096 uint8 channels, P · Bᶜ in
domain and P · Q at 2⁶⁴ — and this time two of three passes upheld it
byte-level, citing beside the sentence L2's untagged instance cell and §17.2's
Note, which says *"P·Q and P·Bᶜ are checked in an empty layer"* with no layout
either. The refute phase, attacking the split, let the downgrade stand, and the
hand-check agrees with the skeptic and with round 29: `[R-ENC-04]` makes a
designation *"express, made by the section that defines the quantity"*, §14.2's
table defines P · Q only as the interleaved decoded size, `[R-SER-07]` makes
every decoded size a function of layout, `[R-COD-07]` says outright that in a
planar layer each channel's plane carries its own decoded size, and every other
row that lists P · Q tags it *interleaved*. The wide reading needs the summary
sentence and the untagged cell read against all of that, and §21.1 makes the
rule govern the cell. **Not byte-level on the normative text — and repaired,
because a reporter in one round and two passes in the next read it wide, and
one clause ends the question.**

The instruments could not see the omission. `tarn_chain` sees whether a commit
was audited, not whether a recorded repair exists; `tarn_adr_quotes` sees a
quotation that drifted, and ADR-0118 paraphrased the qualifier rather than
quoting it. The check that would have seen it is the one this ADR now records
as owed after every repairs commit: **the round's repair list against the
diff**, item by item.

## Decision

**The unapplied repair is made, in the three places the round named.** §14.2's
designation sentence now reads *"each for the layout its row states — a planar
layer has no P · Q to form"*; L2's Instances cell tags its layout-varying
members as L44, T3, T14, T21 and T22 already do — *"planar C·N"*,
*"interleaved P·Q"*, *"planar numeric P·Bᶜ"* — with no change to its instance
count; and §17.2's Note names *"the decoded size the layout gives, P·Q or
P·Bᶜ"*. Every reading the round's passes offered arrives at the same set of
designated quantities under these words.

**L23's Detected cell** said *layer access* for every region of the layer
record, and §19.1 step 4 parses the name at open and makes a name overrunning
inline_length a layer-scope error there; two reporters found it. The cell now
reads *"open (the name, §19.1 step 4); layer access (every other region)"*, on
R1's model. The instance grouping is unchanged.

**§21.6 gains an entry** for the two ignore-record non-violations §21.5's
preamble promised the table lists and the table did not: a user-metadata
document's decoded size, or its frame's declared `Window_Size`, exceeding the
reader's own bound. The entry states what §18.2 and `[R-ERR-04]` already
provide — ignore-record on capability grounds, the narrowest-scope decline
`[R-ERR-04]` names for a document, reported as a resource limit, the whole-file
decline available instead. §21.6 is outside the register's arithmetic.

**`[R-SER-08]`'s antecedent** reached only *"a reader that neither detects the
violation nor rejects the tile"*, leaving a reader that detects the byte and
elects to serve it — a choice `[R-CNF-12]` permits — with no fixed return value,
which is the divergence the rule's own Rationale says it exists to prevent. It
now binds *"A reader that does not reject the tile and returns the value —
whether or not it detected the violation"*.

**`[R-MTA-05]`'s order** over keys' UTF-8 bytes never said how unequal lengths
compare. The universal reading — bytewise, a proper prefix first — is now
stated, and Appendix G item 3's layer-name order compares the same way. Not
byte-level on the reporter's own grading: the length-first reading is not one a
competent implementer takes from *"ascending order of their keys' UTF-8
bytes"*, and the round agreed.

**§9.2's conduct paragraph**, written by ADR-0117's decision 4 to place the
durability barriers in `[R-CNF-02]`'s conduct category, closed with the
express-declaration device of that rule's *other* category — *"the file it
produces is not nonconforming on that account"* — so three reporters read it as
a third member of a class `[R-CNF-02]` counts as two. It now says the file is
never nonconforming by virtue of a conduct rule, *"as `[R-CNF-02]` says of every
conduct rule"*. Decision 4 stands; its sentence now says which category it
chose.

**§20.3 step 4's re-type consequence** said a barred re-type *"makes each stored
tile it reaches nonconforming"*. It does not: conformance is a pure predicate on
bytes (`[R-CNF-02]`), the re-typed file is byte-identical to one a creator may
emit, and every bit pattern is a value under the new type. What it does is make
the stored bytes denote values the writer did not store — wrong content, of the
kind §21.7 leaves unwitnessed — and that is what the sentence now says.

**"An encoding this specification does not assign"** carries §21.5's sense —
encoding 0 and the reserved range included, both R1 violations — and the sense
§21.6 and Appendix H use, the experimental range alone. §2.3's cannot-establish
sentence and §17.4's closing clause used the words in the second sense and read
false in the first. Both now say *experimental-range*, and §2.3 names the
violations beside it.

**§18.2's Note** beneath `[R-MTA-09]` still said an `[R-ERR-04]` decline for a
document lands *"at the whole file"* after ADR-0118's erratum made `[R-ERR-04]`
name the record as a scope; two reporters found the residue. The Note now says
the record-scope ignore-record is that narrowest-scope decline and the
whole-file decline is available instead.

**Appendix G's closing paragraph** called the version_minor floor *"item 8's
creator's rule, not a compactor's"* after item 8 was rewritten to say the floor
binds a compactor too; two reporters found it. The gloss now matches the item.

**Deferred, to the ledger:** Q-B7 (adversary-02) and Q-C7 (verifier-03, with
quiz-01's observation on the same clause), each with a round-30 note.
**Declined:** adversary-03's observation that `[R-COD-11]`'s cannot-establish
ground is unreachable by a conforming verifier — true, and already explained by
§17.4's own last sentence and settled by `[R-CNF-11]`'s priority clause; a
redundancy, not a defect.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors,
Appendix A byte-identical. L2 and L23 are reworded within their instance
counts; §21.6's new entry sits outside the arithmetic.

**ADR-0118's Context is corrected by erratum**: the sentence attributing §14.2's
repair to decision 2 described a repair that was never made.

**A new obligation on the repair process**, recorded here because no instrument
carries it: after a repairs commit, the round's findings list is checked against
the commit's diff, item by item, and every item is either in the diff or named
as deferred. Round 29's list had twenty-one repairables; ADR-0117 and ADR-0118
between them account for twenty, and the twenty-first was this one.

## Precedent

- **ADR-0104**, requiring an ADR for a register change: two cells and a §21.6
  entry.
- **ADR-0117** decision 4, whose category choice §9.2 now states in that
  category's own terms.
- **ADR-0118**'s erratum, whose `[R-ERR-04]` edit §18.2's Note now follows.

## Erratum, 2026-09-03 — the pre-round-31 audit

Seven lanes read this ADR's fourteen edits with the three decisions taken after
them, and found nine of the fourteen needed a second repair, none byte-level.
Each is made in the commit carrying this erratum.

- **§17.2's Note** named the decoded size as *"P·Q or P·Bᶜ"* and omitted the
  planar bool plane's ⌈P/8⌉ and the per-channel plurality; it now reads *"P·Q
  for an interleaved layer and each channel's P·Bᶜ or ⌈P/8⌉ for a planar one"*.
- **L23's Detected cell** said *"every other region"* in a row whose regions
  are its four instances, leaving the leading fixed fields other than the name
  in neither part; now *"every other field and entry"*.
- **`[R-ERR-04]`'s "the two capability refusals §21.6 names"** became a
  miscount once §21.6's new row named a third; two lanes found it. It now says
  *"§21.6's closing paragraph names"*, as `[R-CNF-03]` already did, and the row
  says *"on resource grounds"*, the rule's own word, rather than *capability*.
- **§21.6's preamble** branded any reader treating an entry as a failure
  nonconforming, which the new row's licensed whole-file decline contradicted;
  it now says *"validity failure"* and that a recorded resource decline is
  licensed and reported as `[R-ERR-04]` requires.
- **§20.3's re-type consequence**, rewritten here as *"wrong content, of the
  kind §21.7 leaves unwitnessed"*, swapped one universal for its opposite: a
  size-changing re-type is witnessed by T3 and T14, and one to bool by T2. Two
  lanes found it. The sentence now states the disjunction.
- **Appendix G item 3** pinned the layer-name comparison and left the
  record-key comparison three sentences later unpinned; two lanes found it.
  Every byte order in the item now compares as `[R-MTA-05]` compares keys.
- **§9.7, §22.3 and `[R-MTA-10]`** still stated the certification consequence
  over *"an unassigned encoding"* after §2.3 and §17.4 were narrowed to the
  experimental range; two lanes found it. All three now say experimental-range,
  and `[R-MTA-10]` names R1's violations beside the claim.
- **§17.4's "the metadata-encoding space alone differs"** was false across
  every identifier space once narrowed; it now names its comparison class, the
  codec and filter spaces.
- **§18.2's Note** said *"a reader that proceeds"* where `[R-MTA-09]` has a
  reader whose own bound is larger decode the document; now *"A reader whose
  own bound it exceeds"*.
