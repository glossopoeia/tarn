# 0125. Round 32's repairs: a channel list changes one way per commit, and the binary64 test names its rounding

- Status: Accepted (resolves round 32's repairable findings; both decisions
  confirmed by the maintainer on 2026-09-08; the erratum's name-swap
  decision confirmed on 2026-09-09)
- Date: 2026-09-08
- Covers: §20.3 step 4's permitted list, its several-at-once sentence,
  its bounds paragraph and its witness parenthetical; §18.2 `[R-MTA-04]`;
  §11.1's Rationale; §13.3's sparse-writing Note; §20.3's three-shapes
  Example; §5.1's Example; §5.2 `[R-CNT-21]`; §2.3 `[R-CNF-03]`; §7.1
  `[R-CNT-25]`; §20.5's compaction Example; §21.2 F3; §21.3 L14; §21.6's
  closing paragraph; Appendix H's reader and updater entries; Appendix F's
  IEEE 754 entry
- Confirm: none. Two decisions were put to the maintainer and confirmed on
  2026-09-08, each with its alternative stated below so a superseding ADR
  can choose it. (1) That
  one commit MAY extend a planar layer's channel list at its end or
  shorten it from its end, and not both, so that a commit's net change to
  the list is one of the two and replacing the last channel is two commits
  or a rewrite. (2) That §18.2's finiteness test is taken under IEEE 754's
  default rounding-direction attribute, roundTiesToEven, which the text now
  names. On confirming, the maintainer directed that Appendix F's IEEE 754
  entry cite §18.2 beside §12.1, which the round-32 hand-check had left as
  the one ground the dissenting pass stood on; it now names the conversion
  and its default attribute.

## Context

Round 32 read ADR-0123's repairs, the audit of them, ADR-0124's closed
list and the audit of that, nineteen passages over five commits, with every
lane on Opus. It returned 29 findings from 7 reporters, 19 distinct defects
with all three passes agreeing on the partition, a 15/15 quiz, and four
self-flagged byte-level findings in three groups. One group was upheld
byte-level by all three passes, attacked by the uphold-refuter the harness
added for this round, which returned UPHOLD_STANDS on Sonnet after Opus
refused it twice at zero tokens, and confirmed by hand. One was split, two passes
downgrading it and one upholding, and the hand-check settles it below the
line. One was downgraded by all three passes on a governing clause above
the sentence quoted, and the hand-check agrees. The findings file records
every verdict and every refuter's quotation.

**The flag.** ADR-0124's list permits a planar layer's channel list to be
*"extended at its end, or shortened from its end"*, and its erratum added
*"A commit MAY make several of these changes at once"* and the tie-break
*"where a field is on both sides — a dimension extent, a planar layer's
channel list — the permitted side states the whole of what a commit MAY do
to it"*. Read together they let one commit shorten the list by one and
extend it by one, replacing the last channel with one of another type over
the disk ordinals it vacated, since a planar disk ordinal is c · N + s and
the appended channel takes index C − 1. The fixed side says *"every
channel's type and fill"* is fixed, and read over the net change the
commit is a re-type and a rewrite. Four reporters built it, one to bytes:
planar, rank 1, E = T = 1, two float32 channels both stored, the last
replaced by an int32 channel whose entry the commit points at the removed
channel's four stored bytes, so that `00 00 80 3F` denotes 1,065,353,216
where it denoted 1.0. Every check passes on the result, since P · B is 4
under either type, E = T leaves no padding position, and no bool is
involved. One updater emits that commit and keeps the file_id; another
refuses and rewrites the file under a fresh one. The disputed file is
conforming and only one reading lets a conforming updater produce it from
that input, which is the discriminating question's second limb, as in
round 31. No sentence decides it: the tense sentence closes only the
empty-then-redeclare route, `[R-GEO-01]`'s floor bites only at C = 0, the
re-emission clause decides the entries' disposition (an appended channel's
entries are new to the generation) but not whether the composition is
permitted, and the principle paragraph's own justification for an append,
*"an appended planar channel adds tiles at ordinals after every existing
one"*, is false of the composition rather than a bar on it. The flag is
new, and it is in the erratum's own sentence in the step this round was
chartered to read hardest.

**Why this is a repair here and not a ledger entry.** ADR-0124 drew the
line where a stored tile's meaning is fixed and stated the principle beside
the list so the list could be checked against it. The principle's account
of an append holds exactly when the appended channel's ordinals lie after
every ordinal the superseded generation addressed, which is true of a
commit whose net change to the list is an extension and false of one that
also shortens it. So the principle already decides which way the list
should read; what the document lacked was the sentence. ADR-0091's rule is
satisfied by this ADR, and the maintainer's veto is kept in the Confirm
line, with the alternative below.

## Decision

**1. A planar layer's channel list changes one way per commit.** The
permitted list now reads *"a planar layer's channel list MAY be extended at
its end or shortened from its end, but not both in one commit"*, and the
several-at-once sentence carries the one exception: *"A commit MAY make
several of these changes at once, an extension and a shortening of one
channel list excepted: a commit's net change to a planar layer's channel
list is an extension or a shortening, and replacing the last channel is
two commits or a rewrite"*. §11.1's Rationale says *"one or the other in a
commit"*, and Appendix H's updater entry *"a planar channel list extended
at its end or shortened from it (not both in one commit)"*. Nothing else
in the step moves: the principle paragraph's two justifications, the
appended channel's ordinals after every existing one and the removed
channel's tiles leaving the addressed set, are true of every commit the
list now permits, and the tie-break sentence stays true because the
permitted side now states the whole rule for the field.

**2. The finiteness test names its rounding.** `[R-MTA-04]`'s second
restriction reads *"A reader interprets every JSON number as the IEEE 754
binary64 value its decimal text converts to under IEEE 754's default
rounding-direction attribute, roundTiesToEven, and MAY use a wider
representation"*, and the overflow clause says *"overflows on that
conversion"*. Two passes held the attribute already imported by the
reference to IEEE 754-2019 and by `[R-CNF-02]`'s rule that file
conformance depends on no reader or environment; one pass held Appendix
F's pointer to §12.1 scoped the reference to the interchange formats and
graded the half-ULP window above `DBL_MAX` a fork. The hand-check agrees
with the two: a conversion stated as producing *"an IEEE 754 binary64
value"* with no attribute named is the standard's conversion under the
standard's default, and a parser that clamps on overflow is not performing
it. The clause is added because the document should say what it relies
on, and because `[R-VEC-03]` asks for a vector at R8's stated bound, which
has no stable expected outcome until the attribute is named. R8's
Condition cell already says *"overflows"* and is unchanged.

**The seventeen editorial repairs.** Fifteen were confirmed by every pass;
items 16 and 17 were held already decided by two passes each and are
repaired for their wording:

3. §13.3's sparse-writing Note no longer claims that among the permitted
   changes *"only a change to entry_count"* moves a layer's index content:
   a growth that holds entry_count while a shortening halves C moves every
   ordinal, and a slab or alignment declaration re-established over stored
   tiles moves their entries. The Note is keyed to §20.3's own test,
   *"each commit that changes a layer's stored-tile set or its index
   content re-emits that layer's whole tile-index region"*, which is
   Q-B8's option (b), and §11.1's Rationale is restated on the grid counts
   `[R-GEO-06]` reads: *"A growth that changes no grid count ⌈Eᵢ / Tᵢ⌉
   (§11.2) moves no entry and adds none, and taken alone touches the
   directory alone"*. Five reporters.
4. The bounds paragraph's closing criterion is scoped to the changes the
   list permits: *"a permitted change holds exactly where the declarations
   it produces satisfy every rule they are subject to, and which changes
   are permitted is what the list above states"*, and its antecedent is
   named, *"These bounds are not offered as exhaustive"*. Three passes read
   the unscoped sentence as bounded by the MUST NOT above it, and repaired
   the wording anyway. Two reporters.
5. *"`[R-CNT-17]` obliges the smaller entry_count"* is false of a
   shortening taken with a growth; the sentence now keys the re-emission
   to the clause that governs it and names both cases. Two reporters.
6. The witness parenthetical names the padding rows: *"a decoded size, a
   padding position or pad bit, or a boolean byte the register witnesses
   (T3, T14, T4, T5, T2)"*, as §21.7's three classes have it. Two
   reporters.
7. Appendix H's reader entry carries `[R-CNF-03]`'s three qualifiers, the
   major and the unimplemented top-level MU = 1 record beside the
   guarantees.
8. Appendix H's updater entry re-emits byte-identically *"every retained
   record it does not logically modify"*, a modified one being new output
   under its writer obligations, as `[R-WRT-05]` says.
9. §5.1's figure text says a commit *"that touches no layer and appends
   no record extent"* re-emits the directory, the pad and the trailer
   alone, a user-metadata document living in an extent.
10. Shape (c) and §11.1's Rationale re-declare an empty layer subject to
    every rule its new *declarations* are under, step 4's own word, where
    one said *geometry* and the other said nothing.
11. §20.5's compaction figure marks only B's index as regenerated, A's
    tiles not having moved, and its caption says so.
12. L14's Condition cell names the third alternative its Instances cell
    and `[R-CNT-18]` carry, *"or bytes remain after the last complete
    sub-record"*.
13. F3 carries the in-domain qualifier L2 and T12 carry, and loses *"so
    the sum wraps"*, which `[R-ENC-04]` does not require.
14. §21.6's closing paragraph says the two moved conditions oblige no
    reader to reject anything, `[R-CNF-12]`'s licence on the nonconforming
    file each makes being untouched, as `[R-CNT-18]` says of its own case.
15. `[R-CNT-25]`'s *"never invalidates"* is scoped: application metadata
    never makes the structural data it annotates unusable, and where a rule
    outside the quarantine records a document's defect at the file or the
    layer (F27, L48) the verifier records it there and a reader owes
    nothing for it.
16. `[R-CNF-03]` names the registered record types among what a reader
    MUST handle and among the things a subset profile may not decline;
    §20.4 had assumed it.
17. The fixed list says *"an interleaved layer's channel list (its names
    aside)"*, the permitted side letting channel names change for either
    layout.
18. §5.2's grounds for an incomplete walk carry §9.7's carve-out: an
    entry `[R-IDX-03]` classifies reject-tile on a structural ground leaves
    the walk complete.
19. Appendix H's updater entry states decision 1's shape (with 1).

**Declined.** That a compactor's duty to refuse a structurally malformed
entry turns on a placement it is free to choose (adversary-05): §20.5
states that asymmetry in terms, *"bounds how far a compactor goes looking,
not what it owes on what regenerating the region has already put in front
of it"*, two passes graded it no defect, and a rule reaching every entry
would be a decision about `[R-WRT-09]`'s depth that no finding asked for.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331
vectors. Decision 1 binds a commit's conduct with no single-file witness,
as the list it qualifies has none; §21.7 is unchanged. Decision 2 fixes
which side of R8 a literal in the half-ULP window above `DBL_MAX` falls
on, which is what every IEEE-default parser already does; the corpus
still owes R8 a boundary vector under `[R-VEC-03]`, and that debt is
recorded with the others.

**What decision 1 costs a caller**: one directory and one trailer. A
writer replacing a planar layer's last channel shortens the list in one
commit and extends it in the next, two generations where one would have
done; nothing it could do in one commit is lost, and the ordinals an
appended channel takes are always fresh. **What it buys** is that every
sentence in the step is true of every commit the list permits, and that
no updater has to decide whether a net change is a re-type.

**Q-B8's remaining question is narrowed.** Its premise was settled by
ADR-0124 on the ground that entry_count was the only way a permitted
change moved index content; round 32 found two permitted changes that move
it with entry_count still, and the two blocks now restate §20.3's own key
and nothing else, which is the entry's option (b). Whether they should
restate the rule at all is where the entry was.

**G3's second half is not met by this round**: round 32 read round 31's
repairs and the decision that replaced them, and returned one byte-level
flag, new, in the erratum's own sentence. Round 33 reads this ADR's
repairs, and the criterion turns on it.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every numbered item above is in the diff, and none is
deferred.

## Alternatives rejected

- **Permit the composition and fence it**, by adding that an entry new to
  a generation MUST NOT address an extent a superseded generation's entry
  addressed, and by repairing the principle paragraph's two justifications
  for the composed case. Rejected: the fence is a rule over a file's
  history with no witness, it bars the two-commit path's deliberate
  re-addressing of slack as readily as the one-commit accident, and it
  keeps an operation the append model was not built for. Stated here so
  the maintainer can choose it.
- **Restate the finiteness test without an attribute**, as a magnitude of
  2¹⁰²⁴ or more. Rejected: under roundTiesToEven the half-ULP window below
  2¹⁰²⁴ converts to infinity, so every standard converter would then be
  wrong in that window, and the attribute-free form would need a clamp no
  parser ships.
- **Send the composition to the ledger.** Rejected on ADR-0123's ground:
  the principle decides it, the alternative has no defender in the trail,
  and a round-33 reading of an unrepaired fork is the shape that has
  produced the next finding every time.

## Precedent

- **ADR-0124**: the closed list and the principle stated beside it, which
  decision 1 reads the list against.
- **ADR-0081**: a declaration change that would reinterpret stored bytes
  is not an appender's operation.
- **ADR-0123**: a reach question decided on the trail's own ground with
  the maintainer's confirmation asked, and the repair list against the
  diff.
- **ADR-0091**: a rule's reach is settled by an ADR; this is the ADR.
- **ADR-0104**: editorial repairs ride with the decision.

## Erratum, 2026-09-08 — the pre-round-33 audit

Six lanes read the nineteen hunks of this decision's two commits the same
day, on the shape the ADR-0124 audit set: four subject lanes on Sonnet from
the start, and two cross-hunk passes on Opus, one grouped by rule and one by
operation. Opus refused the by-rule pass at zero tokens at launch and ran it on the
unchanged resume, which refused the by-operation pass in its turn while
re-running it rather than replaying its cache; the journal holds one
completed result from each Opus pass, and neither needed the fallback.
The four Sonnet lanes returned 8 findings between them, one lane empty
with a full account of its sweeps; the two Opus passes returned 10 each. Twenty-eight findings merge by hand into eighteen distinct defects, every one in this
decision's wording, and every one is repaired in the commit carrying this
erratum. The four subject lanes are fallback-grade; the Opus pass grouped by
operation did the substantive work, and the lanes converged on it in three
places and added five small ones.

**Three were graded byte-level by an Opus pass, and the hand-check
confirms two as forks in the text and settles the third as decided by the
list's own terms but stated loosely enough to be read against it.**

- **The exception's gloss tested the channel list by size.** Decision 1's
  sentence read *"a commit's net change to a planar layer's channel list is
  an extension or a shortening"*, and a commit that removes three trailing
  channels and appends five has a net change that is an extension by count
  while the bullet's *"not both in one commit"* forbids it; the lane and the
  Opus pass each built the file and found every row silent. The gloss now
  says what the bullet means: *"a commit that shortens a planar layer's
  channel list appends no channel to it and one that extends it removes
  none, whatever the counts, so replacing the last channel, or any run of
  channels at the end, is two commits or a rewrite"*.
- **The give-up list still called any change to an interleaved layer's
  channel list a rewrite**, three paragraphs after the fixed list excepted
  its names, so renaming an interleaved channel was a permitted change and a
  rewrite at once. It now reads *"any change to an interleaved layer's
  channel list but a channel's name"*, and it names the operation decision 1
  forbids, *"a planar channel list both extended and shortened in one
  commit"*, which it had omitted while claiming to state what the line gives
  up.
- **Two renames in one commit swap two dimensions' names**, and the give-up
  list named *"a transposition of the dimensions"* as a rewrite while the
  permitted list let every name change and the principle said a name enters
  no map. The fixed list fixes the dimension order, which is positional; a
  name is a label. The give-up list now says *"a change to the dimension
  order"*, and the principle says *"a name enters no map this specification
  defines, and a commit MAY change several names at once, two swapped
  included, the dimension order and the channel order being positional and
  fixed"*. That is a small decision taken on ADR-0124's ground, that a name
  enters no map, and the maintainer can reverse it by adding a composition
  rule for renames beside the channel-list one. The maintainer confirmed
  it on 2026-09-09.

**Below the line.** The channel-removal sentence's two-branch account of
why the index region is re-emitted was false of a shortening taken with a
growth that changes no grid count, and of one taken with a growth that
doubles N while C halves; it now rests on the index-content ground alone,
*"whether or not entry_count changes with it (`[R-CNT-17]`) and whether or
not a retained ordinal moves"*. The witness parenthetical omitted T21 and
T22 for a decoded size and said nothing of a codec or filter change a
decode does not survive; it names *"a decode that fails outright under a
changed codec or filter (T24, T25)"*. The partition claim's both-sides
examples gain the interleaved channel list the parenthetical split. §21.6's
closing paragraph said the reader's side was unchanged while adding the
licence that had changed it; it now says the obligation is unchanged and
the licence newly reaches, and drops the analogy to `[R-CNT-18]`, whose
otherwise-conforming branch these conditions never have. `[R-CNT-25]`'s
universal is scoped to a defect in application metadata, and the resource
decline `[R-MTA-09]` licenses at any containing scope is named as another
rule's subject. §5.2's carve-out for a structurally malformed entry is its
own sentence, the walk passing over it for the opposite reason from a
declined decode. Appendix F's *"its"* resolved to binary64; it says
*"IEEE 754's"*. L14's headline *"does not fit"* did not subsume its third
alternative; the cell coordinates the three on F29's model. Appendix H's
reader entry lists the registered record types among what a reader
implements, as `[R-CNF-03]` now does. §20.5's compaction caption taught a
placement as the rule; it says the placement is the compactor's to choose
and under another A's index would be regenerated too. §21.1's account of
verifier-detected rows said the rule *"obliges the reader to serve the
structure unchanged"*, unbounded, for the two rows §21.6's paragraph had
just bounded; it obliges the reader that serves the structure, the licence
untouched. §13.3's Note carried one of §11.1's two entry-free growths and
not the one a declare-then-fill writer meets; it carries both. §20.5's
slack Note still keyed the index cost to a layer a commit *"touched"*; it
keys to the stored-tile set or index content, as the rest of the account
now does. §18.2's *"MAY use a wider representation"* sat beside the
named conversion with nothing tying the two; it reads *"MAY hold the
value so obtained in a wider representation"*. And *"the list above"*
in the bounds paragraph resolved to the bounds it had just called
non-exhaustive; it names *"this step's list of exceptions above"*.

**Register unchanged**: 120 conditions, 277 instances, 331 vectors;
`tarn_check` PASS; eleven quotation and seven propagation acknowledgements,
each for a span this erratum supersedes or a restatement it cites. The
repair list of this erratum was ticked against its diff: eighteen edits,
eighteen hunks, none deferred.
