# Cleanroom round 32 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 31's
charter: ADR-0123's twenty repairs, the pre-round-32 audit's thirty-one, the
decision of ADR-0124 and the eighteen repairs of its audit — nineteen
passages, 25 hunks over 5 commits, chartered over `72c41e1..85abcf3`.
Charter: [prompt.md](prompt.md). The refute phase fires on a unanimous
byte-level uphold for the first time this round.

## Verdict

**One byte-level flag, new, in §20.3 step 4 — and the second half of G3's
criterion is not met, for the third time.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-sixth round running; two of the fifteen aim straight at the closed list (Q12's six operations, Q13's grow-plus-shorten commit) and both takers agree with the author on every one |
| Findings | **29**, from 7 reporters |
| Distinct defects | **19** by union-find, and the three passes agreed on the partition as well as the count — the third round running |
| Self-flagged byte-level | **4**, in three groups |
| Upheld by any triage pass | **2 groups** — one by all three passes, one by one of three |
| Refute phase | fired on **one unanimous downgrade, one split and one unanimous uphold**; the downgrade stands, the split's refuter sided with the reporter, the uphold's refuter returned UPHOLD_STANDS |
| Uphold-refuter | **UPHOLD_STANDS** — the gate-failing verdict; refused at zero tokens twice on Opus, returned on Sonnet; hand-checked in both directions, and the driver's own search for the deciding sentence found none |
| Surviving the hand-check as a *new* byte-level ambiguity | **1** — the composition of two permitted channel-list changes |
| Harness | 15 agent slots; 14 returned at the first launch, every one on Opus but the two refuters configured on Sonnet; the uphold-refuter was refused at zero tokens on Opus twice and returned on Sonnet |
| Coverage | **opus-grade** — see *Harness integrity* |

Byte-level history: … → 2 flagged, 0 new → 1 flagged, 1 new → **4 flagged in
3 groups, 1 new**.

**The flag is one commit that shortens a planar layer's channel list from its
end and extends it at its end.** ADR-0124's list permits either; its erratum
says *"A commit MAY make several of these changes at once"* and hands a
field on both sides wholly to the permitted side. Read together they let one
commit replace the last channel with one of another type over the disk
ordinals it vacated, since a planar ordinal is c · N + s and the appended
channel takes index C − 1; read over the net change the commit re-types a
channel the fixed side freezes. Four reporters built it, one to bytes, and
every check passes on the result. One updater emits the commit and keeps the
file_id; another refuses and rewrites the file under a fresh one. All three
passes upheld it, the uphold-refuter returned UPHOLD_STANDS, and the hand-check
found no sentence that decides it.

It is new — no ledger entry, no ADR, and no round has asked it; Q-B6 and
Q-B10 asked other questions of the step and are superseded — and it is in
the erratum's own sentence in §20.3 step 4, the passage this round was
chartered to read hardest. The criterion is stated outright: zero byte-level
ambiguities, surviving the refute phase and the hand-check. So the round that
read round 31's repairs and the decision that replaced them did not return
zero. The repair is made under ADR-0125 on the principle ADR-0124 states
beside its list, and the maintainer is asked to confirm it, the alternative
being stated so it can be chosen instead. Round 33 reads it.

**The other two groups a reporter called byte-level did not survive.** The
closing criterion of the bounds paragraph dies on the MUST NOT one paragraph
above it, by three passes, a refuter and the hand-check. The rounding
direction of §18.2's finiteness test split the passes two to one and its
refuter sided with the reporter; the hand-check holds that a conversion
stated as producing an IEEE 754 binary64 value with no attribute named is
the standard's conversion under the standard's default, and so does not
bank it, while recording the contrary verdict in full and repairing the
text so the question cannot recur. The round's verdict does not turn on it.

## The byte-level flag, and how it was settled

### `planar-tail-replacement` — `writer-02`, `verifier-03`, `adversary-01`, `quiz-03`; §20.3 step 4 `[R-WRT-04]`

The construction, recomputed by hand from the document rather than taken
from the reporters or the passes: a planar layer, rank 1, extent 1, tile
extent 1, so G = N = P = 1; codec 1, filter 1, no alignment or slab; two
float32 channels `a` and `b`, both stored, `b`'s four stored bytes
`00 00 80 3F`. One commit shortens the list from its end and extends it at
its end with `q`, an int32 channel with fill 0.

| | generation 1 | generation 2 |
|---|---|---|
| channel list | `a` float32, `b` float32 | `a` float32, `q` int32 |
| C, N, entry_count | 2, 1, 2 | 2, 1, 2 |
| `[R-CNT-17]` extent_length | 44 | 44 |
| decoded plane size P · B | 4 | 4 |
| padding positions, bool channels | none, none | none, none |
| entry 0 | (16, 4, `0x48674BC7`) | byte-identical |
| entry 1 | (20, 4, `0xDD54C4AB`) | (20, 4, `0xDD54C4AB`), the appended channel's entry pointing at the same four bytes |
| bytes `00 00 80 3F` denote | float32 1.0 | int32 1,065,353,216 |

Every quantity a register row could witness is unchanged: T3 and T14 see
equal decoded sizes, T4 and T5 have no padding position to check, T2 has no
bool byte, L21 and L22 hold, `[R-CNT-02]` partitions with generation 1's
index region fallen to slack. Both CRCs reproduce under the driver's own
CRC-32C, checked first against §4.5's vector. The output is an ordinary
conforming appended file, and §21.7 leaves the wrong content unwitnessed.

**Two readings.** (A) The two alternatives compose: *"A commit MAY make
several of these changes at once"* reaches inside an item, as it must for a
slab cleared and an alignment declared in one commit under `[R-CNT-16]`; the
tie-break hands the channel list wholly to the permitted side; and the fixed
side frees *"the position of every planar channel but the last"*. (B) The
net change is what a commit is judged by: channel index 1 has a different
type and fill in the two generations, *"every channel's type and fill"* is
fixed, and the commit is a rewrite. Under (B) the same final content is two
commits, each unambiguous. The disputed file is conforming and only one
reading lets a conforming updater produce it from that input in one commit,
which is the discriminating question's second limb and the shape round 31's
flag took; the counterweight two reporters recorded, that a creator could
emit the same bytes, was weighed by the passes and by hand and not treated
as decisive, since an updater is a conforming implementation and the rule
binds it.

**What was opened in the direction that would have cleared the gate.** The
tense sentence closes only the empty-then-redeclare route, on a ground
specific to *stores a tile*. `[R-GEO-01]`'s floor bites only at C = 0. The
re-emission clause's parenthetical decides the entries' disposition, an
appended channel's entries being *"new to this generation … emitted per
§15"*, and so kills `writer-02`'s carry-forward limb, as `quiz-03` said; it
does not decide whether the composition is permitted, and §15 then lets a
new entry address any well-formed extent no other claimant claims. The
give-up sentence names *"a re-type"* as a rewrite and does not say whether a
channel removed and one appended at the same index is one. §3.1 makes a
channel's index an attribute, not its identity. The principle paragraph's
two justifications, *"an appended planar channel adds tiles at ordinals
after every existing one"* and *"a channel removed from the end takes only
its own tiles out of the addressed set"*, are false of the composition
rather than a bar on it. §11.1's Rationale, Appendix H's updater entry and
§23.1 restate the list without deciding it. §20.1 `[R-WRT-01]` and §20.4
`[R-WRT-05]` bind what a commit carries forward, not what it may declare.
Nothing decides it.

**Byte-level, new, and in chartered text.** The several-at-once sentence
and the tie-break are the erratum's own text (`85abcf3`); the alternatives
they compose are ADR-0124's (`ebebcf0`); §20.3 step 4 is the passage the
charter named first.

**Attacked by the uphold-refuter.** The fourth trigger fired for the first time. On Opus the refuter was refused at zero tokens with `[reasoning_extraction]` at launch and again on the unchanged resume, the first refusal the round harness has met in two rounds; per the brief the one call was set to Sonnet and the run resumed. It returned **UPHOLD_STANDS**, and its account of the search is what makes the verdict usable: it opened §20.3 whole, §11.1's Rationale, §11.2, `[R-GEO-06]`, §16.1 and §16.2 with `[R-CNT-16]`, §23.1 and Appendix H, ran a control search before trusting any zero, and tried the one closer the passes had not: that *"several of these changes"* reaches only across the four items and not within one. It found that reading available and unforced, since §11.1 restates the rule with the same shape and no exclusivity marker, and since the slab-and-alignment switch needs the sentence to reach within an item. It quoted the closure clause, the tie-break, the ordinal formula and the principle paragraph's two justifications as the sentences that bear on the question, and named none as deciding it. A STANDS from a Sonnet refuter is not provisional the way its downgrades are, and the driver's own search, above, reached the same sentences and the same end.

**Repaired — ADR-0125, decision 1.** A planar layer's channel list *"MAY be
extended at its end or shortened from its end, but not both in one
commit"*, and the several-at-once sentence carries the exception: a
commit's net change to the list is an extension or a shortening, and
replacing the last channel is two commits or a rewrite. The principle
paragraph's two justifications are then true of every commit the list
permits, and the tie-break stays true. The alternative, permitting the
composition and fencing a new entry from any extent a superseded
generation's entry addressed, is recorded in the ADR so the maintainer can
choose it.

## The two flags that did not survive

### `json-number-rounding-direction` — `adversary-04`; §18.2 `[R-MTA-04]`, §21.5 R8

The reporter's construction: a document carrying the 309-digit literal
2¹⁰²⁴ − 2⁹⁷⁰, the midpoint between `DBL_MAX` and 2¹⁰²⁴. Under
roundTiesToEven it converts to infinity and the file exhibits R8; under
roundTowardZero it converts to `DBL_MAX` and the file is conforming. The
arithmetic is right, and every agent that touched it recomputed it.

**The passes split.** Two downgraded it on `[R-CNF-02]`'s *"file conformance
is a pure predicate on bytes: it does not depend on any reader, writer, or
environment"* and on the reference to IEEE 754-2019, whose default
rounding-direction attribute for binary formats is roundTiesToEven, so a
conversion stated as producing *"an IEEE 754 binary64 value"* with no
attribute named is the standard's conversion under the standard's default,
and a parser that clamps on overflow is not performing it. One of the two
also showed the document's own example decides the reporter's literal:
*"overflows on conversion, `1e400` being the ordinary case"* presupposes
that overflow yields a non-finite value, which is false of roundTowardZero,
and every direction consistent with that gloss sends the midpoint to
infinity, so the residue is a literal strictly between `DBL_MAX` and the
midpoint under roundTowardPositive. The third pass upheld it: Appendix F's
entry reads *"IEEE 754-2019 — binary16, binary32, and binary64 (§12.1)"*,
which it read as scoping the reference to the sample-type table, leaving
§18.2's conversion with no attribute. **The split fired a Sonnet refuter,
which returned DOWNGRADE_REFUTED** on the same ground, quoting §18.2's
rule, Appendix F's line, §21.5's *"every row here is a violation all the
same"* and `[R-CNF-05]`.

**Hand-check: not banked as byte-level.** The refuter's quotations establish
that no attribute is named and what follows if the fork is real; none of
them decides whether naming the standard imports its default, which is the
question. The driver holds that it does: a value *"as an IEEE 754 binary64
value"* is produced by the standard's operations, the standard fixes the
default attribute for every binary-format result absent a stated one, and
nothing in the document sets another; Appendix F's parenthetical indexes
where the reference is used and is not a limit on the standard's content,
and its omission of §18.2 is a small defect of its own. A fresh implementer
calling any shipped decimal converter gets the default. The fork requires
an implementer to choose a directed attribute the document nowhere
licenses, for a literal in a half-ULP window that §18.2 says a writer SHOULD
NOT emit. It is recorded here as a judgment the maintainer can reverse;
this round's verdict does not turn on it, and the text is repaired so
round 33 cannot meet the question. It is in a chartered passage, in a
sentence this surface did not touch (§18.2's bullet dates from batch 12).

**Repaired — ADR-0125, decision 2.** `[R-MTA-04]` names the attribute:
*"the IEEE 754 binary64 value its decimal text converts to under IEEE 754's
default rounding-direction attribute, roundTiesToEven"*. The attribute-free
alternative, a magnitude of 2¹⁰²⁴ or more, is recorded and rejected, since
it would make every standard converter wrong in the window.

### `permitted-change-biconditional` — `writer-01`, `reader-02`; §20.3 step 4's bounds paragraph

*"The list is not offered as exhaustive: a change is permitted exactly where
the declarations it produces satisfy every rule they are subject to"*, read
as a biconditional over any change, licenses a re-type in place, and
`writer-01` carried one to bytes with no witness. All three passes
downgraded it on the sentence one paragraph above, *"A commit MUST NOT
change one of these; the change is a new layer, or a whole-file rewrite"*,
on *"with these exceptions and no other"*, on §2.1's casing rule, and on
§11.1's Rationale stating the same clause as a necessary condition. The
Sonnet refuter returned DOWNGRADE_STANDS on the same four sentences, a
gate-clearing verdict and so provisional; the hand-check opened the same
four and agrees. The wording is repaired: *"a permitted change holds
exactly where…"*, and the antecedent is named.

## Harness integrity

- **15 agent slots; 14 returned at the first launch, every one on the
  model the harness names** — the runtime's metadata says `opus` for the
  author, the six walks, the two takers and the three passes, and `sonnet`
  for the two refuters of the downgrade and the split. The uphold-refuter,
  on Opus, **was refused at zero tokens with `[reasoning_extraction]`, at
  launch and again on the unchanged resume**, the first refusal the round
  harness has met; per the brief that one call was set to `sonnet` without
  rewording and the run resumed a second time. On Sonnet it returned in four minutes and its metadata says `sonnet`; nothing else re-ran.  The first
  launch took 82 minutes, 315 tool calls and 3.19 M subagent tokens; the
  unchanged resume replayed every cached result in three seconds and
  re-ran only the refused agent, which was refused again.
- **Coverage is opus-grade, by the maintainer's model policy, and the
  counts are recorded beside the one measurement on record.** That
  measurement: on identical hunks, the Sonnet fallback returned 2 findings
  where the driver returned 8. Opus has not been measured against the
  driver; round 31 is the calibration line, 24 findings, 20 defects, one
  real byte-level find in a passage seven driver audit lanes had read past.
  This round returned 29 findings and 19 distinct defects, one byte-level,
  in a passage two audits had read days before. The uphold-refuter's verdict
  is fallback-grade and is hand-checked in both directions below; a count
  says nothing about what an Opus lane missed, and no passage is read as
  clean on it.
- **Every walk's transcript matches its structured return**, by
  independent id-scrape: reader 3, writer 4, verifier 3, diagrams 7,
  register 3, adversary 5, each equal to its own
  `transcript_finding_count`; the quiz author's 4 make 29.
- **All three triage passes CLEAN on mechanical coverage** — 29 of 29 ids
  each, by set difference — and the three partitions agree exactly: 19
  groups each, union-find 19.
- **The result was rebuilt from the journal**: 14 of 14 results
  substituted, none unused, and the 52 ellipsis characters left are literal
  ellipses inside agent prose, checked by a walk for strings *ending* in one,
  which found none.
- **The quiz slate is Opus-grade and graded 15/15**; its author reproduced
  every CRC constant the document states and re-derived §21.8's 120 / 277
  by table before authoring a numeric question.
- **No pass ran a directory listing**, and no pass opened a walk transcript.
- **One harness defect, found by a refuter.** The split-refuter's brief
  pastes the first pass's rationale under *"The passes' stated reason for
  downgrading"*; on a split the first pass was the one that upheld, so the
  Sonnet refuter was handed an uphold labelled as a downgrade and said so.
  It reached its verdict from the document, not the label. Round 33's brief
  should carry every pass's rationale with its verdict.

### Disclosures

Every spec-reading agent disclosed injected context — the project
instruction pointer and an index of memory-note titles — and used none of
it. Both quiz takers also disclosed a git-status block naming the branch and
five recent commit subjects that describe the very changes under review,
one of them the audit's defect count; the answerer disclosed a list of
skills and servers as well; the quiz author disclosed a standing instruction
from a tool server preferring one file-access tool over another and said
which it used and why. One refuter disclosed a non-zero use of injected
material: it read the shape of one memory-note title to parse its own
brief's mislabelled field, the harness defect above, and rested no claim
about the document on it. No persisted-output form appeared this round; the
answerer's one over-long read was refused outright and re-issued narrower.
Nine agents wrote and validated a CRC-32C script against §4.5's check vector
before trusting a printed constant, which is the round-28 breach class
handled as the charter asks.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0125

| Defect | Reporters | Repair |
|---|---|---|
| One commit may both shorten and extend a planar channel list, replacing the last channel over the ordinals it vacated — **byte-level** | writer-02, verifier-03, adversary-01, quiz-03 | decision 1: extended or shortened, not both in one commit; the net change is one of the two; §11.1 and Appendix H restate it |
| §18.2's finiteness test names no rounding-direction attribute | adversary-04 | decision 2: roundTiesToEven named, as IEEE 754's default |
| §13.3's Note says only an entry_count change moves a populated layer's index content; a growth taken with a shortening, and a slab or alignment re-established over stored tiles, both move it with the count still | reader-01, writer-03, verifier-02, adversary-02, quiz-01 | the Note keyed to §20.3's own test; §11.1's Rationale restated on the grid counts (Q-B8 option (b)) |
| The bounds paragraph's closing criterion is stated over *a change* and as a biconditional | reader-02, writer-01 | *a permitted change holds exactly where*; *These bounds are not offered as exhaustive* |
| *`[R-CNT-17]` obliges the smaller entry_count* is false of a shortening taken with a growth | reader-03, writer-04 | the sentence keys the re-emission to the governing clause and names both cases |
| The witness parenthetical names T3, T14 and T2 and omits T4 and T5 | verifier-01, register-01 | *a padding position or pad bit* and both rows named |
| §5.1's figure text says a commit touching no layer appends the directory, pad and trailer alone | diagrams-01 | *and appends no record extent*, with the user-metadata case named |
| Appendix H's reader entry keeps one of `[R-CNF-03]`'s three qualifiers | diagrams-02 | all three |
| Appendix H's updater entry drops *and does not logically modify* | diagrams-03 | restored, with the modified record as new output |
| Shape (c) says *new geometry* where step 4 says *declarations*; §11.1's Rationale says nothing | diagrams-04 | *declarations* at both |
| The compaction figure's prime mark is unglossed and marks A's index, whose tiles did not move | diagrams-05 | only B's index marked; the caption says what the mark means |
| L14's Condition cell states two of its three alternatives | diagrams-06 | the residue alternative added |
| F3 lacks the in-domain qualifier L2 and T12 carry and adds *so the sum wraps* | diagrams-07 | the qualifier added, the clause cut |
| §21.6 says the two moved conditions are *not a reason for a reader to reject anything* | register-02 | *oblige no reader to reject anything*, `[R-CNF-12]`'s licence untouched |
| `[R-CNT-25]`'s *never invalidates* has no scope word | register-03 | scoped: never makes the structural data unusable; F27 and L48 recorded by the verifier, a reader owing nothing |
| Nothing requires a reader to implement the registered record types, which §20.4 assumes | adversary-03 | `[R-CNF-03]` names them among what a reader MUST handle and may not decline |
| *An interleaved layer's channel list* on the fixed side reaches channel names the permitted side frees | quiz-02 | *(its names aside)* |
| §5.2's incompleteness grounds lack §9.7's structural-entry carve-out | quiz-04 | the carve-out stated at §5.2 |

### Deferred

None. Two repairs ask for the maintainer's confirmation and ADR-0125's
*Confirm* line names them: the composition closed, and the rounding
attribute named. Q-B8 carries a round-32 note: its settled premise was
falsified and the two blocks now restate §20.3's key, the entry's own
question standing where it was. The corpus owes R8 a boundary vector under
`[R-VEC-03]`, recorded with the corpus debts.

### Declined

`adversary-05`: whether a compactor must refuse a structurally malformed
entry turns on a placement it is free to choose. §20.5 states that
asymmetry in terms, *"bounds how far a compactor goes looking, not what it
owes on what regenerating the region has already put in front of it"*; two
passes graded it no defect, and a rule reaching every entry would be a
decision about `[R-WRT-09]`'s depth that no finding asked for.

## What the round says about the surface it read

Of the nineteen distinct defects, **eleven sit in sentences this surface
wrote or rewrote**: the composition of two permitted changes, the
several-at-once sentence being the erratum's; §13.3's Note as the erratum
re-keyed it; the closing criterion as the erratum lifted it from a growth
to a change; the `[R-CNT-17]` sentence; the witness parenthetical; shape
(c)'s *geometry*; Appendix H's updater entry in two places; `[R-CNF-03]`'s
top-level qualifier, whose no-subset list the repair passed over; §5.2's
incompleteness grounds as ADR-0123 enumerated them; and the interleaved
channel list on ADR-0124's fixed side. **Three more sit in text a decision
left leaning on the rule it replaced**: §5.1's figure text, §21.6's closing
paragraph and `[R-CNT-25]`'s closing sentence. The remaining five are in
text no recent round had touched: the rounding attribute, the compaction
figure's mark, L14, F3 and the compactor's placement.

Two audits read the closed list before this round, and both found the next
defect in it; this round found one more, in the sentence the second audit
added. The shape the charter named fifth, a closed list whose members
compose, is what it was: check 5 asks for the member on neither side and the
member on both, and this round's flag is two members taken at once.
