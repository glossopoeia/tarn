# 0127. Round 34's repairs: a verb that named the default, and the slab clause grounded as its alignment half is

- Status: Accepted (resolves round 34's repairable findings)
- Date: 2026-09-09
- Covers: §20.3 step 4's permitted list at its three sites (with §11.1's
  Rationale and Appendix H's updater entry), its tie-break sentence, its
  closing paragraph's slab clause, its principle paragraph and its
  three-shapes Example; §4.7 `[R-ENC-16]` and its Note; §15.3 `[R-IDX-03]`'s
  table; §18.2's layout table; §21.1's verifier-detected sentence and its
  Instances sentence; §21.2 F5; §21.6's trailer-mimic entry; §21.8
  `[R-ERR-02]`; Appendix F; Appendix G item 8
- Confirm: one repair the maintainer can reverse. Repair 15 lists RFC 9110
  in Appendix F for the transport vocabulary §6.4 and `[R-CNT-10]` are
  stated in; the alternative, stated below, is a transport-neutral
  restatement of `[R-CNT-10]`. Nothing here takes a decision about what a
  conforming actor may do: ADR-0126's decision 1 stands unchanged, *changed*
  staying at every site.

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
