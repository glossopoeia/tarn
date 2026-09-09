# Cleanroom round 34 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 33's
charter: ADR-0126's fourteen repairs and their confirmation, and the
pre-round-34 audit's seventeen — sixteen passages, 19 hunks over 2 commits,
chartered over `42e60b8..bf617cb`. Charter: [prompt.md](prompt.md).

## Verdict

**Zero byte-level flags: none raised, none upheld, and the zero attacked
eight ways and standing — the second half of G3's criterion is met, at the
fifth attempt.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** by hand — twenty-eighth round running; the normaliser reported one divergence, two spellings of one answer |
| Findings | **26**, from 7 reporters |
| Distinct defects | **21** by union-find; all three passes partitioned identically |
| Self-flagged byte-level | **0** |
| Upheld by any triage pass | **0** |
| Refute phase | fired on the **zero**: no reporter flag, no pass uphold, no split; seven groups attacked by subject and one round-wide attacker |
| Targeted refuters | **7 × DOWNGRADE_STANDS**, every one hand-checked in the gate-clearing direction |
| Round-wide attacker | **DOWNGRADE_STANDS**, with an account of the search; refused at zero tokens twice on Opus, returned on Sonnet; hand-checked |
| Surviving the hand-check as a *new* byte-level ambiguity | **0** |
| Harness | 20 agent slots; 19 returned at the first launch on the models the brief names; every walk stalled once and was retried by the runtime; the zero-attacker was refused on Opus twice and returned on Sonnet |
| Coverage | **opus-grade** — see *Harness integrity* |

Byte-level history: … → 1 flagged, 1 new → 4 flagged in 3 groups, 1 new →
1 flagged, 1 new → **0 flagged, 0 new**.

**The criterion.** The round that reads the previous round's repairs must
return zero new byte-level ambiguities in the text it was chartered to read,
surviving the refute phase and the hand-check. Round 34 read ADR-0126's
repairs, the audit of them and its erratum: the fourth verb's four sites, the
bar's category sentence, the closing paragraph's slab sentence restated as an
obligation, `[R-CNF-02]`'s two lists, and twelve sentences elsewhere. Seven
reporters returned 26 findings in the range the last three rounds returned,
three passes graded every one, and not one was called byte-level by anyone.
The refute phase then did what a zero triggers: seven Sonnet refuters attacked
the seven groups likeliest to hide a fork and a round-wide attacker went
looking for the question nobody asked, and all eight returned STANDS with
their constructions stated. The driver hand-checked every one of those eight
verdicts and the fourteen groups the cap left unattacked, and found no
sentence in the chartered text that two competent implementations could read
to different bytes or a different verdict. **The zero stands.**

**What the round found instead** is twenty-one wording defects, seventeen of
them repaired under ADR-0127, two sent to ledger entries that already carry
the question, and two declined on sentences the passes quoted. Four sit in
sentences this surface wrote: the closed list's fifth member, which now
carries a verb with no counterpart in the clause it delegates to; the bar's
category sentence, whose classification two reporters disputed and the text
defends; the erratum's restatement of the slab obligation, stated over a kept
declaration with no trigger and inheriting the step's two senses of *keeps*;
and §4.7's Note, whose next sentence under-describes one table and
over-states another. None reaches a byte.

## The zero, and how it was attacked

A unanimous zero is the one verdict shape the protocol distrusts most: round
16's three passes downgraded a real fork the same way, and round 28's hand-run
refute pass found the round's only byte-level defect in a group four readers
had graded editorial. So the phase fired on this zero as it has since round
29. [round-refute-verdicts.md](round-refute-verdicts.md) carries every
verdict, every section each refuter opened, and the driver's hand-check of
each; the shape of the eight is this.

**The seven targeted attacks** went to the groups several reporters landed on
or a pass killed with the least argument: the fifth member's verb, the
tie-break sentence's *both sides*, §4.7's two actor sets, the bar's category,
the HTTP vocabulary, F5's pad, and the parenthetical that omits L44. Each
refuter was told the discriminating test — is the disputed file conforming,
and does only one reading let a conforming actor produce it — and each
returned the construction it tried and the sentence that killed it. The
hand-check opened the same sentences and their governing paragraphs and
reached the same end in every case; the closest the round came is the fifth
member, where the refuter built a slab-declared layer whose extent growth
renumbers ordinals and found `[R-SLB-04]`'s trigger list firing whatever the
member's verb says.

**The round-wide attacker** read the document end to end, re-derived five CRC
constants from its own table and reproduced every one, and carried one
candidate to bytes: a file whose front-block magic is corrupt, which a reader
holding bytes [0, 16) resident rejects and a reader that never fetches them
serves. It killed the candidate on `[R-CNT-04]`'s own words, restated in F1's
Condition cell, F6, Appendix A and Appendix H: a divergence the requirement
licenses in terms is a designed asymmetry, not a question left open. The
hand-check agrees, and adds that no ledger entry asks it because the document
answers it.

**The fourteen groups the cap left unattacked** were read by the driver
against the same test. Every one is a wording defect whose two readings reach
the same bytes and the same verdict, most of them decided by a sentence in
the same paragraph — §21.1's tie-break, `[R-CNF-01]`'s label rule, `[R-SLB-03]`'s
unconditional invariants, §20.3 step 4's re-emission clause — and the
disposition table below says which.

## Harness integrity

- **20 agent slots; 19 returned at the first launch, every one on the model
  the brief names** — the runtime's metadata says `opus` for the author, the
  six walks, the two takers and the three passes, and `sonnet` for the seven
  targeted refuters. The round-wide attacker, on Opus, **was refused at zero
  tokens with `[reasoning_extraction]` at launch and again on the unchanged
  resume**, the first refusal of that call in three rounds of running it; the
  one call was set to `sonnet` without rewording, the run resumed a third time,
  and the attacker returned in nine minutes with metadata saying `sonnet`. The
  unchanged resume replayed every cached result in sixteen seconds and
  re-ran nothing.
- **Every walk stalled once and was retried by the runtime.** Each of the six
  walks' first attempts was killed for making no progress after 24 to 32
  minutes, and each second attempt completed in 60 to 75 minutes, so the first
  launch took 111 minutes against round 33's 71, with 544 tool calls and
  4.93 M subagent tokens. The retries are the runtime's, not the harness's,
  and every returned walk is a second attempt run from its brief. One
  consequence surfaced through a disclosure: the writer's second attempt found
  its scratch directory already holding eight files timestamped before its own
  start, treated them as another agent's, read none, and worked in a private
  subdirectory. They were its own first attempt's, which it could not know;
  the behaviour is the one the access rule asks for.
- **Coverage is opus-grade, by the maintainer's model policy, and the counts
  are recorded beside the one measurement on record.** That measurement: on
  identical hunks, the Sonnet fallback returned 2 findings where the driver
  returned 8. Opus has not been measured against the driver; rounds 31, 32
  and 33 are its calibration lines, 24 findings and 20 defects, 29 and 19,
  25 and 22, one byte-level each. This round returned 26 findings and 21
  distinct defects, none byte-level. The count sits inside the three lines
  above it, so the zero is not a thin read; it says nothing about what an Opus
  lane missed, and no passage is read as clean on it. The refuters' eight
  verdicts are fallback-grade and were hand-checked before they were banked.
- **Every walk's transcript matches its structured return**, by independent
  id-scrape: reader 2, writer 4, verifier 2, diagrams 4, register 5, adversary
  6, each equal to its own `transcript_finding_count`; the quiz author's 3
  make 26.
- **All three triage passes CLEAN on mechanical coverage** — 26 of 26 ids
  each, by set difference, and every `all_input_ids_seen` complete and exact.
  All three partitioned into 21 groups, and union-find gives 21.
- **The result was rebuilt from the journal**: 20 of 20 results substituted
  from the final launch's wrapper, none unused, and the 36 ellipsis characters
  left are literal, checked by a walk for strings ending in one, which found
  none. The journal holds 28 starts, 20 results and 2 failures: the six
  stalled first attempts and the two refused attacker calls.
- **The quiz slate is Opus-grade and graded 15/15 by hand**; its author
  reproduced every CRC constant the document states and re-derived §21.8's
  120 / 277 by table before authoring a numeric question. The normaliser's
  one divergence, Q07, is *X: conforming; Y: nonconforming* against
  *X = conforming; Y = nonconforming*, and both are right: an experimental
  encoding byte is ignore-record on a conforming file and a reserved one is
  R1.
- **No pass ran a directory listing**, and no pass opened a walk transcript.
- **The refuter briefs carried every pass's verdict beside its rationale**,
  and the seven targeted refuters used them.

### Disclosures

Every spec-reading agent disclosed injected context — the project
instruction pointer, an index of memory-note titles, and a git-status block
carrying recent commit subjects that describe the changes under review — and
used none of it; several named the round number the subjects carry and said
they did not act on it. No persisted-output form appeared this round. Every
walk, both takers, the quiz author and the round-wide attacker wrote a
CRC-32C script of its own before trusting a printed constant, and each that
says so validated it against §4.5's check vector. The writer's
scratch-directory disclosure is recorded above.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0127

| Defect | Reporters | Repair |
|---|---|---|
| The closed list's fifth member says *re-established* of a declaration while the clause it delegates to says *kept* of one and *re-established* of its invariants; the verb names the default the list is carved out of | reader-01, adversary-01, quiz-01 | the member reads *declared, changed or cleared* at its three sites; the closing clause keeps *kept* |
| The tie-break's *both sides* names a dimension extent, which the fixed list does not contain | writer-04, adversary-02 | the example is dropped; the two channel lists remain |
| §4.7's structural test ranges over a reader or verifier and its descriptive restatement over a reader alone | verifier-01, adversary-04 | the descriptive clause names both actors |
| Appendix G item 8 says a compactor's output varies only modulo its trailer while §20.4 lets it drop a PE = 0 record | writer-01 | item 8 names the drop licence as a third source of variation; whether the profile should pin retention goes to Q-I6 |
| §20.3's closing slab clause states the obligation over a kept declaration with no trigger, grounded in a writer rule with five | writer-03 | stated as a result over every run of the new state, grounded as the alignment half is (`[R-SLB-03]`, `[R-SLB-04]`, `[R-CNF-05]`) |
| *keeps* carries two senses in one step and the slab clause inherits the narrower | adversary-03 | the same clause says *the runs this commit adds included* |
| Example shape (c) encloses an empty layer's free re-declaration under *Only the directory is re-emitted* | diagrams-01 | the Example says which re-declarations are shape (b) |
| §4.7's Note under-describes §6.1's table and over-states §7.2's range folding | diagrams-02 | both carve-outs corrected |
| §18.2's Valid-values cell reads *1 or 2* | diagrams-03 | the cell states the value set as §7.4's index_encoding cell does; round 33 declined the same finding and it came back |
| F5's Condition cell names the pre-trailer pad as a floor component | diagrams-04 | struck; the cell lists the rule's three |
| §21.1's *— F27 and L48* names one rule's rows | register-01 | both rules' rows are named |
| §21.6's trailer-mimic entry justifies a payload condition with a fact about slack | register-02 | the reason covers a live payload and slack; `[R-LIF-05]` cited |
| §21.1's *the row is the rule* against its own tie-break | register-04 | *the row is the unit* |
| §21.8's *one vector per instance* drops `[R-VEC-03]`'s *at least* | register-05 | restored |
| The principle paragraph's *a decoded size … the register witnesses* invites reading L44 into it | adversary-05 | *a stored tile's decoded size*; two passes held the text decided it, repaired for its wording |
| Appendix F pins no reference for the HTTP vocabulary `[R-CNT-10]` is stated in | adversary-06 | RFC 9110 listed for §6.4, a decision the maintainer can reverse |
| §15.3's table reaches a half-sentinel entry by two rows and only T11's cell excludes it | quiz-02 | the rule's row carries the exclusion T11 restates |

### Deferred

| Defect | Reporters | Where |
|---|---|---|
| The coverage walk's incompleteness test is stipulated at layer scope, factual at file scope, and silent at tile scope beyond two named cases | verifier-02 | Q-C7, round-34 note: a known question, found from the tile side |
| §21.1's rules carry no requirement identifier | quiz-03 | Q-I7, round-34 note: its first question, found again |

### Declined

Two findings, on sentences the passes quoted, and the hand-check agrees.
`reader-02` and `writer-02`: the bar's category sentence puts it in §21.7's
*no condition a file can exhibit* class where the reporters read
*unwitnessed*; two passes refuted it and the targeted refuter stood, on
`[R-CNF-02]` naming the bar outright, on both classes requiring no row, and on
`[R-CNT-21]` leaving slack content unconstrained, so that a prior generation
in slack is not a state the live file is in. `register-03`: §21.9's *which
every file and every layer carries* is a distributive clause, and the
sentence before it, *a file containing no instance of a kind does not exceed
that row*, already decides the zero-layer file; one pass confirmed, one held
it minor, one refuted.

## What the round says about the surface it read

Of the twenty-one distinct defects, **four sit in sentences this surface
wrote or rewrote**: the fifth member's verbs, which the cycle extended and the
audit left with a verb the delegated clause does not use; the bar's category
sentence, disputed and defended; the erratum's slab restatement, which drew
two findings on its trigger and its quantifier; and §4.7's Note, whose
neighbouring sentence was wrong about two tables. **Eleven sit in chartered
passages in sentences the surface did not touch**: the tie-break's examples,
`[R-ENC-16]`'s two actor sets, the incompleteness test beside the slack
qualifier, the three-shapes Example, §18.2's cell, §21.1's citation and its
aphorism and its identifiers, §21.6's trailer-mimic row, the principle
paragraph's parenthetical, and Appendix F's vocabulary. **Five are in text
the charter did not name**: Appendix G item 8, F5, §21.9's universal, §21.8's
quantifier and §15.3's table.

The list ADR-0124 wrote has now been read five times since, and for the first
time the reading returned no fork in it: a member composed with another
(round 32), an exception glossed by the wrong quantity (that audit), a member
whose verbs did not reach a change (round 33), a verb pasted where it turned
an obligation into a permission (that audit), and now a verb with no
counterpart below, which every reader and every pass read to the same bytes.
