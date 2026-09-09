# 0127. Round 34's repairs: a verb that named the default, and the slab clause grounded as its alignment half is

- Status: Accepted (resolves round 34's repairable findings; repairs 1 and
  15 confirmed by the maintainer on 2026-09-09)
- Date: 2026-09-09
- Covers: §20.3 step 4's permitted list at its three sites (with §11.1's
  Rationale and Appendix H's updater entry), its tie-break sentence, its
  closing paragraph's slab clause, its principle paragraph and its
  three-shapes Example; §4.7 `[R-ENC-16]` and its Note; §15.3 `[R-IDX-03]`'s
  table; §18.2's layout table; §21.1's verifier-detected sentence and its
  Instances sentence; §21.2 F5; §21.6's trailer-mimic entry; §21.8
  `[R-ERR-02]`; Appendix F; Appendix G item 8
- Confirm: none. Two repairs were put to the maintainer and confirmed on
  2026-09-09: repair 15, that Appendix F lists RFC 9110 for the transport
  vocabulary §6.4 and `[R-CNT-10]` are stated in, its alternative stated below
  so a superseding ADR can choose it; and repair 1, which drops a verb from
  the member whose wording ADR-0126's decision 1 carried, that decision's
  substance standing and *changed* staying at every site. Nothing here takes
  a decision about what a conforming actor may do.

## Context

Round 34 read ADR-0126's fourteen repairs, the pre-round-34 audit of them
and its erratum, sixteen passages over two commits, with every lane on the
model the brief names. It returned 26 findings from 7 reporters, 21 distinct
defects with the three passes partitioning identically, a 15/15 quiz, and
**no byte-level finding: none self-flagged, none upheld by any pass.** The
refute phase fired on the zero, as it has since round 29. Seven Sonnet
refuters attacked the groups likeliest to hide a fork and a round-wide
attacker, on Sonnet after Opus refused it twice at zero tokens, went looking
for the question the round had not asked; all eight returned
DOWNGRADE_STANDS with their constructions stated, and the hand-check of every
verdict and of the fourteen groups the cap left unattacked found no sentence
two implementations read to different bytes. **G3's second half is met at
the fifth attempt.** The findings file records every verdict and the
refute-verdicts file every quotation.

**What the round found instead** is wording, four sentences of it in this
cycle's own text. The closed list's fifth member, which ADR-0126 extended to
*"declared, changed, re-established or cleared"*, carries a verb with no
counterpart in the clause it delegates to: that clause, the erratum's
restatement of the slab obligation, names a declaration *"declared, changed
or kept"* and attaches *re-established* to its invariants. Three reporters
enumerated the transitions a declaration can make in one commit, none to
some, some to another, some to none, some to the same, and the switch between
the two exclusive declarations, and found every one named or defaulted
without the verb: some to the same is the default the list is carved out of,
*"keeps its declarations, with these exceptions and no other"*. The same
erratum's restatement of the slab obligation states it over a kept
declaration with no trigger where `[R-SLB-04]` names five, and its *"every
run the new state keeps"* inherits the two senses *keeps* carries in the step;
its alignment half, grounded in `[R-SLB-01]` and `[R-CNF-05]` and quantified
*"every one the new state keeps, not only those this commit adds"*, is stated
at the right breadth. And §4.7's Note, rewritten by the erratum for its
column list, is wrong in its next sentence about two tables. None reaches a
byte: `[R-SLB-03]`'s invariants are unconditional over the live state,
`[R-CNF-05]` bars every conforming writer from a file that fails them, and
the member's verbs are read by no rule.

## Decision

The seventeen repairs, each confirmed by at least two passes or, where two
passes held the text already decided it, repaired for its wording on
ADR-0125's precedent:

1. **The fifth member drops the verb that named the default.** It reads
   *"a slab or alignment declaration MAY be declared, changed or cleared as
   this step provides below"*; §11.1's Rationale and Appendix H's updater
   entry say the same. The closing clause below keeps *"declared, changed or
   kept"*, so the member's three verbs and the default it is carved out of
   are the clause's four. Three reporters. ADR-0126's decision 1, that a
   declared alignment or slab may change, is untouched.
2. **The tie-break names the fields that are on both lists.** *"where a
   field is on both sides — a planar layer's channel list, an interleaved
   layer's channel list — the permitted side states the whole of what a
   commit MAY do to it"*: a dimension extent is on the permitted side alone,
   the fixed list opening *"Every other declaration is fixed"* and naming
   *"every tile extent"*, a different field. Two reporters.
3. **§4.7's descriptive test names both actors**: *"its value determines
   nothing a conforming reader or verifier does"*, as the structural test
   does, so the two classes partition as `[R-ENC-16]` says they do. Two
   reporters.
4. **Appendix G item 8 names the drop licence.** A compactor's output is
   *"reproducible only modulo its trailer and the records §20.4 lets it
   drop"*, a record whose governing flags are MU = 0 and PE = 0 being
   retained or dropped at the compactor's choice, which no item pins.
   Whether the profile should pin retention is Q-I6's question and is
   recorded there.
5. **The closing slab clause is grounded as its alignment half is.** *"a
   slab declaration declared, changed or kept has its invariants satisfied
   over every run of the new state, the runs this commit adds included, or
   is cleared"*, citing `[R-SLB-03]`, `[R-SLB-04]` and `[R-CNF-05]`: a result
   over the new state, as the alignment sentence beside it is, with the
   appositive that sentence already carried. Two reporters, on the trigger
   and on the quantifier.
6. **Shape (c) says which re-declarations it covers.** *"A re-declaration
   that changes the layer's index content re-emits the region (step 4,
   `[R-CNT-17]`) and is shape (b); one that leaves it unchanged is this
   shape."* A layer that stores no tile can address several, and a
   re-tiling changes its entry_count.
7. **§4.7's Note describes the two tables it names.** §6.1's *"Value column
   replaces type, name and range"*, and §7.2 *"folds a field's range into
   its Field cell where it states one, its length and extent fields' bounds
   being stated in the rules below the table"*.
8. **§18.2's Valid-values cell states the value set**, as §7.4's
   index_encoding cell does: *"1 or 2 assigned; 0 invalid, 3–0x7F reserved,
   ≥ 0x80 experimental (§10); see below"*. Round 33 declined the same
   finding on the cell's deferral; a second reporter read it the same way.
9. **F5's Condition cell lists the floor's three components**: *"so the
   front block, directory and trailer cannot all fit"*, as `[R-CNT-27]`
   derives it; a zero-length pad is legal (`[R-CNT-05]`).
10. **§21.1 names both rules' rows**: *"fixed semantics, F28 and L49; and
    `[R-MTA-05]`, whose unsorted document readers process as they find it,
    F27 and L48"*.
11. **§21.6's trailer-mimic entry gives the reason that covers its
    condition**: *"no reader scans backward (`[R-LIF-05]`), the coverage
    walk claims a live payload's bytes as its tile's extent and enumerates
    nothing in slack"*, `[R-LIF-05]` cited beside `[R-LIF-06]`.
12. **§21.1's Instances sentence says what it means**: *"the row is the
    unit, and each instance is one file"*, twenty lines below the
    subsection's own tie-break that the rule governs.
13. **§21.8 carries `[R-VEC-03]`'s quantifier**: *"and at least one vector
    per instance"*.
14. **The principle paragraph's parenthetical names its subject**: *"but for
    a stored tile's decoded size"*, so that L44, which reads declarations
    alone, is not read into a list of rows that witness a stored tile's
    reinterpretation. Two passes held the text decided it.
15. **Appendix F lists RFC 9110** for §6.4's request accounting and
    `[R-CNT-10]`, which are stated in range requests, status codes and
    content length and pinned nothing. Confirm.
16. **§15.3's table carries the exclusion T11 restates**: *"the value being
    distinct from S (non-sentinel)"*, so the rule and not only the row
    separates a half-sentinel entry from a value-domain one.

**Deferred.** The coverage walk's incompleteness test, stipulated at layer
scope and factual at file scope and silent at tile scope beyond two named
cases: Q-C7, which already asks the file-scope question, carries a round-34
note. §21.1's rules carrying no requirement identifier: Q-I7's first
question, found again, carries one.

**Declined.** The bar's category sentence, which two reporters read as
*unwitnessed* where it says *"no condition a file can exhibit"*: two passes
refuted it and the targeted refuter stood, on `[R-CNF-02]` naming the bar
outright, on both of §21.7's classes requiring no row, and on `[R-CNT-21]`
leaving slack content unconstrained, so that a superseded generation in
slack is not a state the live file is in; the bar's subject is a commit's
event. §21.9's *"which every file and every layer carries"*: the sentence
before it, *"a file containing no instance of a kind does not exceed that
row"*, decides the zero-layer file, and the distributive reading is the plain
one.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors;
F5's cell and §15.3's row restate their rules with the rule's own words. No
reader behaviour changes and no writer permission moves: repair 1 removes a
verb that named the default, repair 5 restates an obligation `[R-SLB-03]`
already imposes, and repair 15 cites the vocabulary a rule already used.

**G3's second half is met.** Round 34 read round 33's repairs and their
audit and returned zero byte-level ambiguities, the refute phase and the
hand-check standing. The next job is the maintainer's: G1's verdict. The
round that reads this ADR's repairs, if one is run, reads seventeen wording
repairs and one new reference.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every numbered item above is in the diff, eighteen edits
over sixteen items, and none is deferred.

## Alternatives rejected

- **Rename the clause's *kept* to *re-established*** so the member's four
  verbs have four counterparts. Rejected: the clause restates `[R-SLB-04]`,
  whose *re-establish* takes the invariants as its object, and a declaration
  kept at its value is the default the list is carved out of, not an
  exception to it.
- **Pin retention in Appendix G**, a new profile item making an adopting
  compactor drop nothing. Rejected here: it is a profile decision of the
  kind Q-I6 asks be taken on a criterion rather than one item at a time, and
  item 8's claim is made true without it.
- **Restate `[R-CNT-10]` transport-neutrally** instead of citing RFC 9110, a
  response returning more than the requested range. Rejected: the rule's
  fallback clause names suffix ranges and a size probe, which are HTTP's, and
  a normative-references appendix that pins a codec's release tag can pin the
  transport a MUST is written in. Stated here so the maintainer can choose it.

## Precedent

- **ADR-0126**: decision 1, which stands; the erratum's restatement of the
  slab obligation, which this ADR grounds.
- **ADR-0125**: repairs made for wording where two passes held the text
  decided it.
- **ADR-0124**: the closed list and the principle beside it.
- **ADR-0119**: the repair list against the diff.
- **ADR-0104**: editorial repairs ride with the decision.

## Erratum, 2026-09-09 — the pre-round-35 audit

Six lanes read the eighteen hunks of this decision's commit the same
afternoon, on the shape the three previous audits set: four subject lanes on
Sonnet from the start, and two cross-hunk passes on Opus, one grouped by rule
and one by operation. For the first time no lane was refused: every one
completed at launch, in forty minutes. The four lanes returned 5 findings
between them, one lane empty with a full account of its sweeps; the two Opus
passes returned 9 and 11. Twenty-five findings merge by hand into twelve
distinct defects, every one in this decision's wording, and every one is
repaired in the commit carrying this erratum. The lanes are fallback-grade;
the Opus passes did the substantive work, and the lanes converged on it in
four places and added one.

**None is byte-level by the hand-check, and none was graded so by any
lane.** The nearest was the by-operation pass's reading of the closing slab
clause: grounded in `[R-SLB-03]` and `[R-CNF-05]` with no trigger, it reaches
on its face a slab-declared layer the commit does not touch, where a stale
declaration would oblige a clearing that `[R-WRT-05]`'s byte-identical
re-emission forbids. The pass graded it down itself, on the paragraph's
opening scope and on the input being nonconforming under both readings, and
the hand-check agrees; the clause now opens *"on a layer this commit
modifies"*, which is where `[R-WRT-05]`'s duty ends and where every trigger
of `[R-SLB-04]` lies.

**Two repairs undershot and one overshot.** F5's cell dropped the pad and
the 64-alignment with it, leaving a reason false over 84 ≤ F < 128; it names
*"a directory at an offset of at least 16 and the trailer at a 64-aligned
offset"*, as `[R-CNT-27]` does. The slab half of the closing sentence was
moved off *keeps* and the alignment half beside it was not; both halves now
range over the new state, *"every one the new state holds and those this
commit adds included"*. §4.7's gloss, *its value determines nothing a
conforming reader or verifier does*, outran the four-item test beside it,
since a verifier's SHOULD-deviation advisory (`[R-CNF-12]`) on version_minor
is a thing its value determines; the gloss is cut and the four-item test
stands alone.

**The sentinel carve-out reached one row and not its neighbours.** §15.3's
value-domain row gained a per-field rider while `[R-IDX-02]` still scoped the
two domain rules per entry and the sum row beside it carried no rider at all;
the three now say one thing: *"neither field being S"* on the value row and
*"neither field being the all-ones sentinel"* on T11, *"each field alone
being in domain"* on the sum row as T12 has it, and `[R-IDX-02]` saying that
*"an entry with exactly one field at the sentinel value is §15.3's own row
before either rule reads it"*.

**Below the line.** Shape (c)'s new sentence sent every index-changing
re-declaration to shape (b), which is false where the new declarations
address no tile: there is no region to emit, the slot becomes (0, 0), and the
commit is shape (c). The sentence says so, cites `[R-WRT-04]` for the
re-emission and `[R-CNT-17]` for the absent region, shape (b)'s heading
admits the no-tile-written case, step 4's re-emission clause states the
no-region case, and the old *this shape* reads *"shape (c)"* where a fresh *(b)* had
been planted before it. The trailer-mimic entry's live half named a tile's
extent where the walk's claimants are three; it names *"the extent or region
carrying them, a tile's, a record's or the directory's"*, cites `[R-LIF-08]`,
and §22.3's account carries the live half too. *"the row is the unit"* named
a unit of nothing, and *each instance is one file* read as exactly one
against §21.8's *at least*; the sentence says *"the unit a vector is
attributed to"* and *"one distinguishable file, covered by at least one
vector"*. Dropping *a dimension extent* from the tie-break left *an extent
MAY grow* with no site saying which extent; the permitted list and Appendix H
say *"a dimension extent"*. The RFC 9110 entry pluralised a status code,
named a content length `[R-CNT-10]` offers as one of three, called §6.4's
accounting stated in its terms when §6.4's Note removes the accounting from
conformance, and was cited by nothing; it names *"the 200 status code and the
range requests `[R-CNT-10]` names for an HTTP transport"*, and `[R-CNT-10]`
cites it. §4.7's Note named two of the four §7.2 fields whose bounds sit
below the table; it says *"a field's remaining bounds"*. §21.1's *the one
rule that goes the other way* was falsified by `[R-CNT-12]`'s reading of
MU = 1 with PE = 0 as PE = 1, and its restatement of `[R-TYP-04]` had dropped
*sample or fill*; both are restored, and the reserved-flag rows F26 and L47
join the inventory. And §11.1's Rationale had gained an Oxford comma the
member and Appendix H lack; it is gone.

**Register unchanged**: 120 conditions, 277 instances, 331 vectors;
`tarn_check` PASS; eight quotation and two propagation acknowledgements. The repair list of this erratum was ticked
against its diff: twenty edits, twelve defects, none deferred.
