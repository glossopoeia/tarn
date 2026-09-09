# Cleanroom round 35 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 34's
charter: ADR-0127's seventeen repairs, their confirmation, and the
pre-round-35 audit's twelve — sixteen passages, 24 hunks over 2 commits,
chartered over `bf617cb..cdaf294`. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level flag, new, in §20.5's `[R-WRT-09]` — text this round was
not chartered to read. The chartered text returned zero, so the second half
of G3's criterion held across this repair cycle; the document has a fork
outside it, repaired under ADR-0128 as a decision the maintainer is asked to
confirm.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-ninth round running |
| Findings | **25**, from 6 reporters; the diagrams walk returned none with a full account |
| Distinct defects | **22** by union-find; the implementer pass partitioned into 22, the other two into 23 each, splitting one group apiece |
| Self-flagged byte-level | **0** |
| Upheld by any triage pass | **1** — by all three, unanimously, against both reporters' own grading |
| Refute phase | fired on **one unanimous uphold** and nothing else: no reporter flag was downgraded and no verdict split, and the uphold suppressed the zero-trigger |
| Uphold-refuter | **UPHOLD_STANDS** — the gate-failing verdict; refused at zero tokens twice on Opus, returned on Sonnet; hand-checked in both directions, and the driver's own search for the deciding sentence found none |
| Surviving the hand-check as a *new* byte-level ambiguity | **1** — whether a compactor's checksum duty reaches an extent it copies without relocating |
| In the chartered text | **0** |
| Harness | 13 agent slots; 12 returned at the first launch on the models the brief names; no walk stalled; the uphold-refuter was refused on Opus twice and returned on Sonnet |
| Coverage | **opus-grade** — see *Harness integrity* |

Byte-level history: … → 1 flagged, 1 new → 4 flagged in 3 groups, 1 new →
1 flagged, 1 new → 0 flagged, 0 new → **0 flagged, 1 upheld, 1 new**.

**The criterion, in both halves.** Round 34 met G3's second half by
returning zero over round 33's repairs. This round read round 34's repairs,
the audit of them and its erratum, and returned zero byte-level ambiguities
in those 24 hunks: every one of the twelve defects it found in chartered
passages is wording, and two of them sit in sentences this cycle wrote. So
the second half held. What the round found instead is a fork the passes
built where no reporter had claimed one, in a compaction rule no round had
touched, and the first half of the criterion, zero byte-level ambiguities
outright, is not met until that fork is repaired. ADR-0128 repairs it on the
rule's own stated principle and asks the maintainer to confirm; if the
repair stands, the document is at zero again, and the reading of that repair
is the next round's.

**The flag is a compactor's checksum duty over an extent it copies but does
not move.** `[R-WRT-09]` says a compactor *"relies structurally on every
structure it copies, so it MUST verify each link of the chain"*, and then
lists the links: the open, each retained layer's record and full index
chain, *"and each relocated extent's checksum, including every stored tile's
entry crc"*. The premise ranges over everything copied; the list ranges over
relocated extents. §20.5 makes the difference live twice: a compactor
*"preserves no placement"* and is *"free to place structures anywhere §5.2
admits"*, and its own figure commentary says *"In this placement A's stored
extents happen not to move"*. Take an input whose top-level user-metadata
extent fails its terminal CRC (R2) and is otherwise clean, and a compactor
that keeps every structure at its input offset. Under the list it never
reads that CRC, detects nothing, and emits the output under a fresh
file_id; under the premise it verifies, fails, and §20.5 obliges it to
refuse. Two reporters built it and both graded it below byte-level on
`[R-CNF-05]`'s ground, that the output is nonconforming under both readings;
all three passes upgraded it on `[R-WRT-01]`, which says of an appender and a
compactor that *"a violation latent in a structure they carry forward
unmodified travels with it, seen or unseen"*, and on §20.5's *"Given a
conforming input the output is a conforming file"*, a conditional with no
work to do unless a nonconforming input may yield a nonconforming output. So
the output is a file a conforming compactor may emit under one reading and
none may under the other. The uphold-refuter stood, and the hand-check
agrees.

It is new: no ledger entry asks it, though Q-C10 asks the neighbouring
question about an index entry's classification and names `[R-WRT-09]` only
as the depth bound. It is not in chartered text: §20.5 was last touched by
ADR-0126's slack Note and `[R-WRT-09]` itself by no recent cycle. The repair
is made under ADR-0128 on the rule's own principle, that verification depth
follows reliance over everything the compactor carries, and the alternative,
narrowing the premise to the list, is recorded so the maintainer can choose
it.

## The byte-level flag, and how it was settled

### `compactor-copies-vs-relocated` — `verifier-02`, `adversary-04`; §20.5 `[R-WRT-09]`, `[R-WRT-07]`, `[R-WRT-01]`

The construction, checked by hand: input I of one generation, no interior
slack.

| structure | bytes | state |
|---|---|---|
| front block | [0, 16) | constant |
| user-metadata extent, top-level, PE = 1 | [16, 116) | terminal CRC does not match: R2 |
| layer A's one stored tile | [116, 216) | entry crc holds |
| A's tile-index region | [216, 300) | chain holds |
| directory, pad, trailer | [300, F) | hold |

**Two readings.** (E) The dash list is the obligation and the premise its
justification: the compactor verifies the open, A's record, A's index chain
and A's tile's entry crc, relocates nothing, reads no CRC over the metadata
extent, detects no violation, and emits O. (P) The premise is the
obligation and the list illustrates it: the compactor verifies the extent's
CRC, the check fails, and *"A compactor MUST refuse to compact when any check
`[R-WRT-09]` obliges fails"*. O exists under (E) and not under (P). No
creator may emit O (`[R-CNF-05]`) and no appender produces it (the file_id
is fresh), so O is a byte sequence exactly one class of conforming
implementation may emit, and only under one reading. That is the
discriminating question's second limb.

**What was opened in the direction that would have cleared the gate.**
`[R-CNF-05]`'s first sentence, which both reporters rested on: `[R-WRT-01]`
carves a compactor out of it in terms, and §20.5 restates the carve-out.
§8.2's chain of trust, which names no user-metadata extent's CRC among its
links: `[R-WRT-09]`'s list already reaches outside that chain, naming the
open and each retained layer's record, so *"each link of the chain"* is a
restatement whose completeness is the question. `[R-WRT-03]`, the appender's
rule, which gates reliance to what the commit modifies or reuses: `[R-WRT-09]`
opens by contrasting itself with it, *"over everything it carries"*, which
reads as a deliberate widening and not a loose one. `[R-WRT-07]`'s
restatement, *"reach the index chain and each stored tile's entry crc"*, which
drops the *relocated* qualifier for tiles and is silent on every other
extent. `[R-RDR-02]`'s extent tier, keyed to returning content, which
`[R-WRT-09]` does not invoke, stating an emission-timed trigger of its own.
`[R-MTA-02]`, which forbids structural reliance on a document's content and
says nothing of the extent `[R-CNT-02]` names a structure. Three formulations
of one duty exist, in the premise, the list and `[R-WRT-07]`, and no two
agree; nothing decides which.

**Byte-level, new, and outside the chartered text.** Both reporters said
their own grading was the contestable part; the passes contested it and the
refuter could not restore it.

**Attacked by the uphold-refuter.** On Opus the refuter was refused at zero
tokens with `[reasoning_extraction]` at launch and on the unchanged resume,
as in rounds 32 and 33; per the brief the one call was set to Sonnet and the
run resumed. It returned **UPHOLD_STANDS**, and did the work the verdict
needs: it opened §2.3, §8.1 and §8.2, §19.2 through §19.4, §20.1 through
§20.5 whole, the three §21.5 rows and the checklists, tested four closers and
said why each fell short, and tested the reporters' own downgrade ground
before setting it aside. [round-refute-verdicts.md](round-refute-verdicts.md)
carries its account. A STANDS from a Sonnet refuter is not provisional the
way its downgrades are, and the driver's own search, above, reached the same
sentences and one more, the placement freedom that makes *relocated* a
proper subset, and the same end.

**Repaired — ADR-0128, decision 1.** The duty reads over *"the checksum §8.1
states over each extent it copies, every stored tile's entry crc among
them"*, with the placement point stated: *"an extent the output leaves at its
input offset owes the same check as one it relocates"*. `[R-WRT-07]`'s
restatement says the same. The cost to a compactor is a CRC over bytes it
reads to copy in any case. The alternative, narrowing the premise to the
list and saying an unmoved extent owes no check, is recorded in the ADR so
the maintainer can choose it.

## Harness integrity

- **13 agent slots; 12 returned at the first launch, every one on the model
  the brief names** — the runtime's metadata says `opus` for the author, the
  six walks, the two takers and the three passes. The uphold-refuter, on
  Opus, **was refused at zero tokens with `[reasoning_extraction]` at launch
  and again on the unchanged resume**, which replayed every cached result in
  six seconds; the one call was set to `sonnet` without rewording, the run
  resumed a third time, and the refuter returned in six minutes with metadata
  saying `sonnet`. The first launch took 80 minutes, 327 tool calls and
  3.12 M subagent tokens. **No walk stalled**: the six ran 27 to 36 minutes
  each and completed at the first attempt, against round 34's six retries.
- **Coverage is opus-grade, by the maintainer's model policy, and the counts
  are recorded beside the one measurement on record.** That measurement: on
  identical hunks, the Sonnet fallback returned 2 findings where the driver
  returned 8. Opus has not been measured against the driver; rounds 31
  through 34 are its calibration lines, 24 findings and 20 defects, 29 and
  19, 25 and 22, 26 and 21, one byte-level each but the last. This round
  returned 25 findings and 22 distinct defects, one byte-level, in a rule no
  reporter graded byte-level. The refuter's verdict is fallback-grade and is
  hand-checked in both directions; a count says nothing about what an Opus
  lane missed, and no passage is read as clean on it.
- **Every walk's structured return matches its transcript by count**: reader
  2, writer 4, verifier 3, diagrams 0, register 6, adversary 6, each equal to
  its own `transcript_finding_count`; the quiz author's 4 make 25. The
  id-scrape flagged the writer, whose transcript labels its four findings
  W-01 through W-04 where its return says writer-01 through writer-04; the
  four titles match one to one, and nothing was dropped.
- **The diagrams walk returned no finding, with the account an empty return
  owes**: it inventoried every figure, table, example and list, recomputed
  every printed checksum from its own CRC-32C, decoded both hex dumps field
  by field, recounted the register to 120 rows and 277 instances, validated
  every Governing-rule cell against §21.1's grammar, and found the one
  unlabelled blockquote, §15.1's index-region figure, arithmetically
  consistent with `[R-CNT-17]`. An empty lane with that record is a clean
  reading of the figures, not an unestablished one.
- **All three triage passes CLEAN on mechanical coverage** — 25 of 25 ids
  each, by set difference, and every `all_input_ids_seen` complete and exact.
  The implementer pass partitioned into 22 groups and the other two into 23,
  each splitting a different pair; union-find gives 22.
- **The result was rebuilt from the journal**: 13 of 13 results substituted
  from the final launch's wrapper, none unused, and the 30 ellipsis
  characters left are literal, checked by a walk for strings ending in one,
  which found none. The journal holds 15 starts, 13 results and 2 failures,
  the two refused refuter calls.
- **The quiz slate is Opus-grade and graded 15/15**; its author reproduced
  every CRC constant the document states and re-derived §21.8's 120 / 277 by
  table before authoring a numeric question, and the normaliser found no
  divergence.
- **No pass ran a directory listing**, and no pass opened a walk transcript.
- **The stall-retry sentence held**: the quiz author and the refuter each
  said their scratch directory was empty when they began, the first agents
  told what to make of one that is not.

### Disclosures

Every spec-reading agent disclosed injected context — the project
instruction pointer, an index of memory-note titles, and a git-status block
carrying recent commit subjects — and used none of it. No persisted-output
form appeared this round. Every walk, both takers and the quiz author wrote
a CRC-32C script of its own before trusting a printed constant, and each
that says so validated it against §4.5's check vector.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0128

| Defect | Reporters | Repair |
|---|---|---|
| `[R-WRT-09]`'s checksum duty is quantified over relocated extents against a premise over every structure copied — **byte-level** | verifier-02, adversary-04 | decision 1: the duty reaches every extent the compactor copies, placement aside; `[R-WRT-07]`'s restatement agrees |
| The principle paragraph's second parenthetical, *(T24, T25)*, omits T17, which witnesses a codec re-declared to zstd | reader-01, verifier-01 | *a decode that fails outright, or a codec's framing check that precedes it (T17, T24, T25)* |
| §6.1 says the local/remote distinction governs §6.4's accounting *and nothing else*, while `[R-CNT-06]` and `[R-CNT-10]` turn on it | reader-02 | the sentence names the three things the distinction governs |
| Appendix G item 3 says *a declared alignment* where it means A or A_slab, and constrains no non-tile structure | writer-01 | *a declared A or A_slab* admitting no stored tile at 16; a structure no declaration constrains begins at 16 |
| Appendix G item 5's reason for pinning the layout fails for a single-channel numeric layer | writer-02 | the layout byte itself is the residual reason |
| *added tiles* names tiles that produce no new entry | writer-03 | *tiles a grown extent or an appended channel adds to the addressed set* |
| §22.3's *every byte a reader can reach belongs to one named structure* is false of the front block by `[R-CNT-02]`'s own terms | writer-04 | *is the front signature block or belongs to exactly one named structure* |
| *The fixed declarations are* the ones §14, §11.4 and §15 read, omitting §17's codec and filter | verifier-03 | the fourth limb added |
| §21.1's *quarantine does for every §21.5 row* over-reaches `[R-CNT-25]`'s four-way trigger | register-01 | *for every way a §21.5 row makes the document unreadable* |
| §21.6's Rule column mixes two citation forms and §21.1's governance clause is singular over cells listing several | register-02 | the one parenthetical cell normalised; §21.1 says each listed rule governs the part it states |
| §21.1's *the further rules the condition reads* is not exhaustive across the rows | register-03 | *further rules the condition reads, a finding aid and not the whole of them* |
| §21.1's `[R-SER-08]` sentence explains its claim by restating it | register-05 | *which `[R-TYP-04]` (§12.3) records as the one such case* |
| `[R-EXT-03]` and `[R-RDR-03]` send a reader to §15.1 for the index-encoding value set, which §7.4 states | register-06 | §7.4 in both lists and in §10.2's row |
| Appendix G's closing inventory omits item 5's filter, tile-extent and layout pins | adversary-01 | the three kinds added in the paragraph's own form |
| `[R-EXT-02]` calls the trailer's flag lanes a numeric identifier space its own universal does not partition | adversary-02 | the lanes are not a space of this kind and are not tabulated |
| `[R-CNT-09]` and §19.1 step 1 assert a suffix-range response carries F, which `[R-CNT-10]` provides against | adversary-05 | both hedged to a transport that discloses the complete length |
| §4.7's Note puts a length prefix inside a field's value where §13.1 puts it in §7.4's framing | adversary-06 | the Note rests a name's structurality on `[R-ENC-15]` and calls the prefix framing |
| `[R-ENC-16]`'s *each class being what the one before it is not* names an order two classes do not have | quiz-03 | the clause is cut; the descriptive test's *none of those* carries it |

### Deferred

| Defect | Reporters | Where |
|---|---|---|
| A condition's individuation chains through `[R-CNF-13]` and §21.1 back to the register's rows, the vacuity §21.7 closes for detectability and not for this | register-04 | Q-I7, round-35 note: a third question beside the identifiers and the pair individuation |
| L23's Detected cell splits the name field out of an instance its Instances cell does not split | adversary-03 | Q-I7, round-35 note: an instance by §21.1's own test, split when its vector ships, since the gate fails on an instance with none |

### Declined

Two findings, on sentences the passes quoted, and the hand-check agrees.
`quiz-01` and `quiz-02`: the member's three verbs against the closing
clause's four, and §11.1's Rationale without the default clause; the head of
the same sentence decides it, *"keeps its declarations, with these exceptions
and no other"*, so keeping is the baseline and not a member, and the
Rationale defers to §20.3 in terms. `quiz-04`: `[R-ERR-04]`'s narrowest scope
for a tile's decoded size; §21.9's per-instance paragraph makes the quantity
a tile's, and the containing-scope licence makes the choice inconsequential
for conformance.

## What the round says about the surface it read

Of the twenty-two distinct defects, **two sit in sentences this surface
wrote or rewrote**: the principle parenthetical, whose first half the cycle
scoped to a stored tile and whose second half omits T17; and §21.1's
`[R-SER-08]` sentence, which the erratum restated into a tautology. **Twelve
sit in chartered passages in sentences the surface did not touch**: *added
tiles* and the fixed declarations' characterisation in §20.3; §21.1's
quarantine clause, its parenthetical convention and its §21.6 clause; the
individuation chain; §22.3's partition sentence; `[R-CNT-09]`'s suffix
claim; Appendix G's items 3 and 5 and its inventory; §4.7's prefix sentence
and its ordering clause; and the member's verbs, declined. **Eight are in
text the charter did not name**: `[R-WRT-09]`, the one fork; §6.1's *and
nothing else*; the two value-set lists and §10.2's row; `[R-EXT-02]`'s flag
lanes; L23; §19.1's half of the suffix claim; and `[R-ERR-04]`'s scope,
declined.

The chartered text held. The fork the round found is in a rule written
under ADR-0094's compactor decision and read past by every round since,
and it was found by the passes and not the reporters: both reporters
built the construction and then talked themselves out of it on a sentence
that does not apply to a compactor, and three passes reading blind each
found the sentence that does.
