# Cleanroom round 30 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 29's
charter: ADR-0117's five decisions, the two audits' repairs, ADR-0118's nineteen
repairs and the pre-round-30 audit's eighteen edits. Charter:
[prompt.md](prompt.md).

## Verdict

**Two byte-level flags, neither new, and the second half of G3's criterion is not
claimed — for a process reason rather than a textual one.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-fourth round running (five answers differed only in how the key annotated the same value; hand-graded) |
| Findings | **19**, from 7 reporters |
| Distinct defects | **14** by union-find, and the three passes agreed on the partition as well as the count |
| Self-flagged byte-level | **2** |
| Upheld by any triage pass | **2** — both splits, both attacked by the refute phase |
| Surviving the refute phase and a hand-check as *new* byte-level ambiguities | **0** |
| Harness | 14 agents returned of 14 that ran; the quiz author was refused twice by the driver at zero tokens and ran on the fallback model |

Byte-level history: … → 1 → 0 → **2 flagged, 0 new**.

**One flag is Q-B7**, open since round 25 and byte-level since round 27, found
cold for the sixth time by the adversary with the ledger's own construction.
The refuter let the downgrade stand and the hand-check agrees with the ledger:
nothing the round produced moves that question's standing, which is the
maintainer's to settle.

**The other flag is round 29's own finding, unrepaired.** Round 29's single
byte-level flag asked whether a planar layer derives P · Q for `[R-ENC-04]`'s
overflow ceiling; it was settled not byte-level by two blind checkers and a
hand-check, and its findings recorded the reporter's one-clause repair as the
disposition. ADR-0118 then recorded that repair as made. **No commit made it.**
Round 30's reader found the same summary sentence cold, built the same
construction, and this time two of three passes upheld it byte-level, on the
untagged L2 cell and a §17.2 Note that names both products without a layout.

So the round read a surface that was not the surface round 29's findings called
for, and the criterion's second half — a round reading the previous round's
repairs returns zero — is not met by this round, because one of those repairs
was missing. On the normative text the question is decided, as round 29 found
and as the refuter and the skeptic found again; the repair is now made
(ADR-0119) and the next round reads it.

## The two byte-level flags, and how each was settled

### `planar-pq-designation` — `reader-01`, §14.2 `[R-SER-02]`, row L2, §17.2's Note

The construction: a planar layer, rank 1, one extent 0, tile extent 2⁵², 4,096
uint8 channels. P · Bᶜ = 2⁵² is in domain; P · Q = 2⁶⁴ is not; no tile is
addressed, so no §21.9 row is exceeded. A reader forming P · Q for a planar layer
rejects the layer under L2 and a verifier reports nonconforming; a reader forming
only the layout's own decoded size accepts, and under that reading `[R-CNF-03]`
obliges acceptance. The arithmetic is sound and was verified by all three passes.

**What decides it is the designation clause, and every layout-tagged row.**
`[R-ENC-04]`: *"A designation is express, made by the section that defines the
quantity."* §14.2's table defines P · Q in the row headed *interleaved* and P · Bᶜ
in the row headed *planar*; `[R-SER-07]` makes every decoded size a function of
layout; `[R-COD-07]` says outright that in a planar layer each channel's plane
carries its own decoded size; L44, T3, T14, T21 and T22 each tag P · Q
*interleaved*; §21.1 makes the rule govern the cell. The wide reading takes the
summary sentence and the untagged cell against all of that. The refuter, opening
§11, §14.1 through §14.4, §17.2, §19.3, §21.1 and the rows, returned
DOWNGRADE_STANDS on exactly those grounds — the weak direction for a weaker
model, so it was hand-checked, and the hand-check agrees.

**What the two upholding passes had that round 29 did not** is §17.2's Note:
*"P·Q and P·Bᶜ are checked in an empty layer"*, with no layout. It is a Note, and
under the layout reading it says only that whichever product the layout gives is
checked; but it is one more sentence a reader can take wide. The repair round 29
recommended is now made in three places: §14.2's sentence reads *"each for the
layout its row states — a planar layer has no P · Q to form"*, L2's cell tags
*planar C·N*, *interleaved P·Q* and *planar numeric P·Bᶜ* as its sibling rows
do, and the Note names *"the decoded size the layout gives"*.

### `pe0-drop-on-added-record` — `adversary-02`, §20.4 `[R-WRT-08]`

Q-B7's construction exactly: a PE = 0 experimental top-level record, a commit
that adds the file's first user-metadata record, one appender that drops the
record and one that retains it, both outputs conforming. The correctness and
implementer passes downgraded on the letter — *"another non-layer top-level
record"* presupposes a record existing before the commit — and the skeptic
upheld on the stated principle, calling it the group it tried hardest to kill.
The refuter let the downgrade stand, arguing from the Rationale's own
*"modified, added, or dropped"* trichotomy and from the row's set-language for
the one limb where addition counts.

The ledger's standing — byte-level, gating G3, resting on round 27's hand-check
and a DOWNGRADE_REFUTED there — is unchanged by any of this, and the round's note
is added to the entry. Every pass recommended the one-clause closure in the "no"
direction, and none could show the document decides it. That is the maintainer's
call, and it has been since round 25.

## Harness integrity

- **14 agents returned of 14 that ran.** The quiz author was refused by the
  driver twice in a row, at zero tokens in under five seconds each — the
  recorded `[reasoning_extraction]` class — and ran on the fallback model
  without rewording, per the recorded remedy. **The slate is fallback-grade**;
  its fifteen questions nonetheless graded 15/15, and its author caught its own
  draft question drifting onto the layer-scope discard clause of `[R-CNT-21]`
  and rebuilt it, which it disclosed. Every walk, both takers, all three passes
  and both refuters ran on the driver.
- **Every walk's transcript matches its structured return**, by independent
  id-scrape: reader 4, writer 3, verifier 4, diagrams 1, register 3, adversary
  3, each equal to its own `transcript_finding_count`.
- **All three triage passes CLEAN on mechanical coverage** — 19 of 19 ids each,
  by set difference — and for the first time in this project's record the three
  partitions agree exactly: 14 groups each, and union-find gives 14.
- **The refute phase fired on two splits**, as designed, and did not need the
  zero-trigger.
- **No pass ran a directory listing.** Two passes and both refuters read walk
  transcripts by name, as the brief permits, and said which.

### Disclosures

Every spec-reading agent disclosed injected context — the project-instruction
pointer, an index of four memory-note titles, and an environment block naming
recent commit subjects — and used none of it. **Six agents disclosed a new form
of the channel**: a `sed` or `Read` call whose output exceeded the tool's cap was
persisted by the runtime to a file outside the specification, and each agent
said so and did not open it. That is the ninth distinct form in which this
channel has been disclosed, and the first that the harness itself creates.

The quiz author's disclosure that it wrote and ran a CRC script in its private
scratch directory, validated against §4.5's check vector before trusting it, is
the round-28 breach class handled as the charter asks.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0119

| Defect | Reporters | Repair |
|---|---|---|
| §14.2's designation sentence, L2's cell, §17.2's Note carry no layout (round 29's unapplied repair) | reader-01 | qualified in all three places |
| L23's Detected cell says *layer access* for the name `§19.1` step 4 decides at open | reader-04, register-02 | `open (the name, §19.1 step 4); layer access (every other region)` |
| §21.5 says §21.6 lists the ignore-record non-violations; the bound and window declines are not there | register-03 | a §21.6 entry, stating what §18.2 and `[R-ERR-04]` provide |
| `[R-SER-08]` fixes the return only for a reader that neither detects nor rejects | adversary-01 | the antecedent is a reader that does not reject and returns the value |
| `[R-MTA-05]`'s byte order undefined for unequal lengths | writer-01 | lexicographic, proper prefix first; Appendix G item 3 the same |
| §9.2's conduct paragraph closes with `[R-CNF-02]`'s other category's device | reader-02, writer-03, verifier-04 | now cites the conduct-rule principle |
| §20.3 says a re-type *makes each stored tile it reaches nonconforming* | reader-03 | the bytes denote values the writer did not store; unwitnessed |
| *an encoding this specification does not assign* in two senses | verifier-01 | §2.3 and §17.4 say *experimental-range* |
| §18.2's Note still places an `[R-ERR-04]` decline at the whole file after the pre-round audit named the record | verifier-02, register-01 | the Note follows the rule |
| Appendix G's closing gloss contradicts item 8 on the compactor floor | writer-02, diagrams-01 | the gloss matches the item |

### Deferred — to the ledger, with a round-30 note

| Defect | Entry |
|---|---|
| Adding a non-layer top-level record as a licensing change | **Q-B7** — the maintainer's, byte-level, gating G3 |
| The partial slack total after a walk-established file-scope rejection (verifier-03), and the discard clause's legibility (quiz-01) | **Q-C7** |

### Declined

`adversary-03`: `[R-COD-11]`'s cannot-establish ground is unreachable by a
conforming verifier. True, and §17.4's own last sentence says so; `[R-CNF-11]`'s
priority clause decides the verdict word. A redundancy, not a defect.

## What the round says about the surface it read

Of the fourteen distinct defects, **two sit in the repairs the round was
chartered to read**: §9.2's conduct paragraph, which three reporters read as a
third member of a two-member class because ADR-0117's decision 4 closed it with
the wrong category's words; and §18.2's Note, which two reporters found still
placing a document decline at the whole file after the pre-round audit's own
edit named the record in `[R-ERR-04]` — that audit's repair introducing, in the
Note beside it, the residue its next reader found. **A third was supposed to be
in that surface and was not**, which is the finding this round is most about.
The remaining eleven are in text no recent round had touched, the shape of
rounds 18 through 22.

None of the pre-round audit's eighteen edits drew a finding on its own text.
