# Cleanroom round 37 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 36's
charter: ADR-0131's three clauses and the two of its erratum, three hunks over
two commits, chartered over `96e4ad4..6c9470e`, with the attention block
weighting this cycle's decisions above the five clauses on the maintainer's
direction. Charter: [prompt.md](prompt.md), the cut of `cadb44b`. The audit
that preceded it is recorded in ADR-0131's erratum; its diff and transcripts
are the `audit-*` and `adr0131-*` files here.

## Verdict

**No byte-level flag: none self-flagged, none upheld by any pass, and the
refute phase, firing on the zero, stood on all seven of its attacks. This is
the second zero from the same instrument over the same decisions, read with
the decisions weighted first. The round returned six findings, six distinct
defects, none of them in what the decisions decide. Whether a second Sonnet
zero meets G3 is the maintainer's to say; the findings record it and do not
declare it.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** on verdicts by hand; the normaliser said 9 / 6, five being one answer spelled two ways and one a right verdict with the wrong rule cited (see *The quiz*) |
| Findings | **6**, from 2 reporters; the reader, writer, verifier and register walks and the quiz author returned none, each with a full account |
| Distinct defects | **6** by union-find; the three passes partitioned identically, six singletons |
| Self-flagged byte-level | **0** |
| Upheld by any triage pass | **0** |
| Refute phase | fired on **the zero**: six targeted refuters, one per group, and a round-wide attacker; the cap of ten left nothing unattacked |
| Refuter verdicts | **seven of seven stand**, each in its own vocabulary |
| Surviving the hand-check as a *new* byte-level ambiguity | **0** |
| Harness | 19 agent slots, 19 returned at the first launch, every one on `claude-sonnet-5` by the runtime's metadata; no refusal, no stall; 58 minutes, 453 tool calls, 3.31 M subagent tokens |
| Coverage | **sonnet-grade** — see *Harness integrity* |

Byte-level history: … → 0 flagged, 0 new → 0 flagged, 1 upheld, 1 new →
0 flagged, 0 upheld, 0 new, on a weaker reader → **0 flagged, 0 upheld, 0
new, the second on that reader**.

**The criterion, and what a second zero adds.** Round 36 returned zero over
this cycle's decisions and the record could not tell a settled text from a
weaker reader. This round read the same decisions again, told to read them
hardest, with the round-36 repairs and their audit's repairs in front of it,
and returned zero again: two of its six findings sit in the decisions' text
and both were found decided, one of them by five restatements. That is more
than one zero said. It is still a zero from an instrument that returns a
third of what the rounds before it returned (six and eight findings against
twenty-four to twenty-nine), and a count says nothing about what a lane
missed. **The driver records the second zero and does not declare the
criterion met**: the weighing of the instrument is the maintainer's, and the
two Sonnet rounds are now the evidence to weigh.

**The maintainer's verdict, 2026-09-22: G3 is declared met**, on this round
and round 36 together. ADR-0132 records the declaration with the record it
rests on and makes this round's one repair.

## The hand-check

Every verdict of this round is in the direction that clears the gate, so
every one is provisional until checked by hand. All six groups were read
against the specification; none is byte-level.

1. **`diagrams-bracket-overrun`** (diagrams-01; figures (a) and (b) of
   §20.3's three-shapes Example). The walk computed every bracket in the
   document by column and found the four in this Example open one column
   inside their cell and close on the cell's right divider, where §5.1's
   three open and close on the dividers themselves; it read the first
   convention as a one-column overrun. The audit before this round computed
   the same columns and read the opposite way, moving figure (b)'s new
   bracket to match its siblings. The hand-check settles which convention
   the Example can follow: figure (a)'s two brackets abut and share the
   divider at column 32, so divider-to-divider brackets would have to put
   two corners on one column; the Example's convention is forced by its own
   layout, and it is uniform across all four brackets, as the walk itself
   observed. Two conventions, each internally consistent, each in a labelled
   Example, neither a rule. **Declined**; this annotation row has been
   edited three times in this cycle and a fourth edit to the other
   convention would be churn.
2. **`trailer-flags-cell-actor-list`** (diagrams-02; §6.2's flags cell).
   *"carried forward unchanged by an updater, appender or rewriter alike"*
   lists the class beside its own two tiers as three coordinate actors,
   where §6.3's own statement of the same rule reads *"by every updater
   under this text, appender and rewriter alike"*. A normative table cell,
   but the rule is `[R-CNT-08]`'s and binds every updater whatever the
   cell's grammar; `[R-CNF-06]` leaves no third actor for a coordinate
   reading to reach. **Repairable in one clause**, to §6.3's idiom: *by
   every updater, appender and rewriter alike*.
3. **`r-wrt-06-missing-conduct-only-disclaimer`** (adversary-01; §20.5's
   `[R-WRT-06]` against §2.3's `[R-CNF-02]`). `[R-CNF-02]`'s second sentence
   names *"the cases this text states"* of writer obligations expressly
   declared not to be file-conformance violations, three of them, each
   declared where it arises. The rewriter's duty to refuse a file carrying
   an unimplemented MU = 1 record has the same shape: its refuter showed
   that a creator may emit, byte for byte, the file a rule-breaking rewriter
   would, so no verifier can see the violation and the emittable set does
   not move. It is not among the three, and its site does not say so; the
   general sentence (*conduct rules bind the actor, the predicate binds the
   bytes*) covers it without naming it. Not byte-level. **For the
   maintainer, not repaired here**: whether `[R-CNF-02]`'s stated cases gain
   a fourth member and `[R-WRT-06]`'s site the declaration, or the general
   sentence is left to carry it. It is a closed list in §2.3, and this
   cycle's rule is that a closed list is not edited in passing. The premise
   the finding starts from, that the same operation is refused as a
   rewriter and legal as a creator, is decision E3's shape: each position
   has its price, and the maintainer chose to bar neither.
4. **`layer-drop-mu1-row-label-scoping`** (adversary-02; §20.4's blocking
   sentence, decision E2's text). The one group the passes split on,
   PARTIAL against two REFUTED, and the split is over whether the row label
   *MU = 1* should carry the qualifier its lead-in states. The refuter built
   the fork and killed it on five restatements of *a type the updater does
   not implement*, in three sections; the hand-check finds the same five
   and nothing against them. **Declined**: the reading the finding needs
   is not available from the document. A one-phrase qualifier on the row
   label would restate the lead-in one sentence away and is not proposed.
5. **`appender-rewriter-narrowing-confirmed`** (adversary-03; §20.4's last
   row). A confirmation, returned as an observation: the narrowing to *an
   appender* and *a rewriter* reconstitutes the updater class exactly, and
   the asymmetry between the two clauses is §20.5's, which already says a
   rewrite does several things at once. The audit's hunk 3, read a third
   time. Not a defect.
6. **`single-channel-layout-confirmed-unwitnessed`** (adversary-04; step 4's
   bar at one numeric channel). A worked confirmation of what §14.4's Note
   states and `[R-CNF-02]` declares: the layout byte of a single-channel
   layer can change with no witness, and the bar binds the commit as an
   actor. Not a defect.

**The round-wide attacker's account is what the hand-check reads.** Three
constructions carried to numbers (the segment seam at 65,536 entries, the
sentinel and crc partition, `[R-ENC-04]`'s designation carve-out against
§14.2's stride at its ceiling) and six areas walked, none forking;
[round-refute-verdicts.md](round-refute-verdicts.md) quotes it. Nothing in
it is new to the record.

## The quiz

Fifteen questions, all answered by both takers with high confidence; 15 of
15 agree on verdicts by hand. The normaliser reported 9 agree and 6
diverge. Five of the six are one answer spelled two ways, beyond what its
loose form strips: Q03 (*reject-layer; no (other layers unaffected)* against
*reject-layer; no*), Q04, Q08, Q09 and Q10. **Q13 is a real divergence with
an agreed verdict**: a rewriter that cannot decode a layer's sample type may
not re-create that layer, both takers say *no*, and the answerer names
`[R-WRT-06]` where the keyer names `[R-WRT-07]`. The key is right: the
sentence that decides it, *"A layer the rewrite re-creates is new output:
its record, its tile-index region and its stored tiles are written under
§20.2's rules from content the rewriter decoded"*, sits in the paragraph
`[R-WRT-07]` closes; `[R-WRT-06]`'s paragraph is the trailer's flags,
version_minor and the refusal on an unimplemented MU = 1 record, and a
sample type is not a record type. The answerer's own reasoning states the
rule correctly and mis-cites it. No spec defect and no key correction.

## Harness integrity

- **19 agent slots, 19 returned at the first launch, every one on Sonnet.**
  The runtime's metadata says `claude-sonnet-5` for all nineteen: the quiz
  author, two takers, six walks, three passes, six targeted refuters and
  the round-wide attacker. No refusal and no stall; the walks took 14 to 19
  minutes each, the passes 6 to 10, the refuters 3 to 6. 58 minutes end to
  end against round 36's 54, 3.31 M tokens against 3.34 M.
- **Coverage is sonnet-grade, and the counts sit beside the measurements on
  record.** Opus's calibration lines are rounds 31 through 35: 24/20/1,
  29/19/1, 25/22/1, 26/21/0, 25/22/1 (findings, defects, byte-level).
  Sonnet's are round 36, 8/8/0, and this round, **6/6/0**. The one
  side-by-side measurement has Sonnet returning 2 findings where the driver
  returned 8 on identical hunks. No passage is read as clean on this round's
  count.
- **Both harness debts held.** Every refute call answered in its own
  vocabulary, the round-wide attacker included. No agent listed the shared
  output directory; nine briefs now say *do not list that directory* beside
  the path, and the disclosures say none did.
- **Every walk's structured return matches its transcript by count**: the
  diagrams walk 2 and the adversary 4, each equal to its own
  `transcript_finding_count`; the other four walks and the quiz author 0.
  `integrity.py` flags the diagrams walk because its transcript carries the
  two findings as *Finding 1* and *Finding 2* without the `diagrams-NN`
  ids; both are there in full.
- **All three triage passes CLEAN on mechanical coverage**: 6 of 6 ids each
  by set difference, every `all_input_ids_seen` exact, three identical
  partitions, union-find 6.
- **The result was rebuilt from the journal**: 19 of 19 results substituted
  from the launch's wrapper, none unused, no truncation marker left. The
  journal holds 19 starts, 19 results and no failure.
- **The empty walks gave the account an empty return owes.** The reader
  walked the two-request cold open, the four validation tiers and the
  eight-step tile read, and traced five degradation paths; the writer
  re-read the four decisions as if unread and the three changed passages
  with a column check of both figures; the verifier built a four-generation
  file by hand and closed the coverage partition at each generation,
  catching one addition error of its own; the register walk recounted 120
  conditions and 277 instances by script and checked every §21.9 limit; the
  quiz author reproduced the document's check vectors before authoring.

### Disclosures

Every spec-reading agent disclosed injected context and used none of it:
the project instruction pointer, an index of memory-note titles, and a
git-status block carrying recent commit subjects, this round's charter
subject and the audit's *"two defects in three clauses, none byte-level"*
among them. That channel is the one round 19 found; it names the round's
position and it is disclosed every round. **No agent listed the shared
output directory.** One disclosed breach of the same family: the verifier
ran `ls -la` on the run directory's parent to confirm its scratch path,
which printed the names `out`, `scratch` and the three `triage-*`
directories, every one of which its brief already names. The adversary
listed its own scratch directory once, which is allowed.

## Disposition

### Repairable — proposed for ADR-0132, not yet made

One, one clause: §6.2's flags cell, *by every updater, appender and
rewriter alike*. **Held until the maintainer has the verdict**, as round
36's were.

### For the maintainer

Whether `[R-CNF-02]`'s three stated conduct-only cases should become four,
`[R-WRT-06]`'s refusal declared conduct-only at its site (adversary-01).
The finding is sound about the rule's shape and the document is not wrong
as it stands; the choice is about a closed list in §2.3.

### Declined

`diagrams-01`, a figure convention forced by figure (a)'s abutting cells.
`adversary-02`, decided five times over. `adversary-03` and `adversary-04`,
confirmations the reporter itself graded as no defect.

### Standing

Step 4's tie-break sentence (round 36's reader-01) drew nothing this round
and stays with the maintainer, as directed before the audit.

## What the round says about the surface it read

**Decisions E1, E2 and E3 drew two findings and both were found decided.**
The adversary took E2's blocking sentence against an implemented MU = 1
sub-record and the document answered five times; it took E3's two positions
to the one place they diverge, a rewriter's refusal against a creator's
freedom, and found the divergence one the conformance predicate cannot see,
which is what E3 decided. §7.2's two passages and step 4's scope sentence
drew nothing. **The five clauses drew one finding**, figure (b)'s bracket
again, from the other convention's side, and one confirmation of the row
the audit had read twice. **Three of the six sit in text the charter did not
name**: §6.2's flags cell, `[R-WRT-06]` against `[R-CNF-02]`, and step 4's
unwitnessed-declaration sentence.

**What two zeros say.** Round 36 read this text once and found nothing to
decide; this round was told to read the decisions hardest, read them again,
and found the same. The instrument is the same in both and its yield is a
third of the rounds before it, so the second zero is a second reading, not a
stronger one. Whether two readings on this instrument meet a criterion set
under another is the maintainer's judgement, and the record is now shaped
to make it: two rounds, six and eight findings, none in what was decided.
