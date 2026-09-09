# Cleanroom round 33 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 32's
charter: ADR-0125's nineteen repairs and their confirmation, and the
pre-round-33 audit's eighteen — fifteen passages, 22 hunks over 3 commits,
chartered over `85abcf3..42e60b8`. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level flag, new, in §20.3 step 4's permitted list — and the second
half of G3's criterion is not met, for the fourth time.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-seventh round running |
| Findings | **25**, from 7 reporters |
| Distinct defects | **22** by union-find; two passes partitioned identically and the third split two of their groups |
| Self-flagged byte-level | **1** |
| Upheld by any triage pass | **1** — by all three, unanimously |
| Refute phase | fired on **one unanimous uphold** and nothing else: no reporter flag was downgraded and no verdict split |
| Uphold-refuter | **UPHOLD_STANDS** — the gate-failing verdict; refused at zero tokens twice on Opus, returned on Sonnet; hand-checked in both directions, and the driver's own search for the deciding sentence found none |
| Surviving the hand-check as a *new* byte-level ambiguity | **1** — whether a declared alignment or slab may change to another value |
| Harness | 13 agent slots; 12 returned at the first launch, every one on Opus; the uphold-refuter was refused at zero tokens on Opus twice and returned on Sonnet |
| Coverage | **opus-grade** — see *Harness integrity* |

Byte-level history: … → 1 flagged, 1 new → 4 flagged in 3 groups, 1 new →
**1 flagged, 1 new**.

**The flag is a commit that changes a layer's declared alignment or slab to
another value.** The permitted list's fifth member says a slab or alignment
declaration *"MAY be declared, re-established or cleared"*, and *"and no
other"* closes the list. A commit that sets A from 4096 to 512 on a layer
whose every stored tile lies at a multiple of both is, on one reading, a
declaration, and on the other none of the three verbs. The disputed file is
conforming under both: `[R-SLB-01]`'s invariant holds over every kept tile,
`[R-CNT-16]` and `[R-CNT-23]` hold, and no row witnesses the prior value. One
updater appends a directory-only commit under the same file_id; another
rewrites the file. All three passes upheld it after searching the fixed list
(which names neither A, S nor A_slab), the give-up list (which names no change
of either) and the tie-break sentence (which does not reach the field). The
uphold-refuter returned UPHOLD_STANDS. The hand-check found two sentences that
presuppose the answer and none that states it.

It is new — no ledger entry, no ADR, and no round has asked it — and it sits
in the permitted list of §20.3 step 4, text ADR-0124's erratum wrote, two
audits and round 32 read, and this round was chartered to read first. The
criterion is stated outright, so the round that read round 32's repairs did
not return zero. The repair is made under ADR-0126 on ADR-0124's own ground,
that a slab or alignment declaration governs placement and nothing a stored
tile's meaning turns on, and on `[R-SLB-04]`'s standing treatment of a changed
slab declaration; the maintainer is asked to confirm it. Round 34 reads it.

## The byte-level flag, and how it was settled

### `alignment-slab-value-change` — `writer-01`; §20.3 step 4 `[R-WRT-04]`, §16.1 `[R-SLB-01]`, §16.2 `[R-SLB-04]`

The construction, checked by hand: a layer that stores tiles under A = 4096,
every tile at a 4096-aligned offset; one commit sets A = 512 and changes
nothing else.

| | generation 1 | generation 2 |
|---|---|---|
| alignment field | `00 10 00 00 00 00 00 00` | `00 02 00 00 00 00 00 00` |
| S, A_slab | 0, 0 | 0, 0 |
| every stored tile at a multiple of A | yes | yes, 4096 being a multiple of 512 |
| index region, extent slot | unchanged | unchanged, the commit re-emitting the directory alone |
| `[R-CNT-16]`, `[R-CNT-23]`, L40 | hold | hold |

**Two readings.** (R-a) *"declared"* is any act of writing a nonzero
declaration, the prior value being irrelevant; the commit is permitted, and
the closing paragraph's invariant clause binds it. (R-b) The three verbs
partition the transitions, none to some, some to the same some, some to
none; a value change is none of them and *"and no other"* makes it a rewrite.
Under (R-b) the same end state is two commits, a clearing and a declaration,
each unambiguous. Only one reading lets a conforming updater emit the
one-commit file, which is conforming; the shape is round 31's and round
32's.

**What was opened in the direction that would have cleared the gate.** The
fixed list: *"the layout, the linearization and the index encoding, the codec
and the filter, the rank and the dimension order, every tile extent, every
channel's type and fill, an interleaved layer's channel list (its names
aside), and the position of every planar channel but the last"*, with no
alignment or slab in it, so the MUST NOT does not bite. The give-up list,
offered as complete, names no change of alignment or slab. The tie-break
names three both-sides fields and not this one. The principle paragraph's
account of the member, *"a slab or alignment declaration governs placement
(§16), not a value, its coordinate or its padding"*, is true of a change as of
a first declaration and decides nothing. *"A commit MAY make several of these
changes at once"* would let a clearing and a declaration compose into a
change, a route the passes did not rest on and a reader of (R-b) can refuse
on the ground that a change with no cleared state between is not two of the
listed changes. `[R-SLB-04]` names *"the slab declaration itself"* changing
among the events that oblige a commit to re-establish its runs or clear the
declaration, on a layer slab-declared in either generation: the rule
presupposes the change is a commit's event, for a slab, and says nothing of an
alignment. Step 4's closing sentence makes *"every one the new state keeps,
not only those this commit adds"* satisfy the alignment invariant, a clause
with no work to do unless the declaration can be new or different. Both
presuppose; neither states. Appendix G item 5 is non-normative. §11.1's
Rationale and Appendix H restate the three verbs. Nothing decides it.

**Byte-level, new, and in chartered text.** The member's words are the
ADR-0124 erratum's, in §20.3 step 4, the passage named first in the charter;
the composition question of round 32 and its audit sat one item away.

**Attacked by the uphold-refuter.** On Opus the refuter was refused at zero tokens with `[reasoning_extraction]` at launch and again on the unchanged resume, as in round 32; per the brief the one call was set to Sonnet and the run resumed. It returned **UPHOLD_STANDS**, and it did the work the verdict needs: it opened §20.3 step 4 whole, §16.1, §16.2, §11.1's Rationale, Appendix H and §7.4's field table, ran a normalised search for every site of *re-establish*, and pushed the one closer the passes had weighed further than they did. That closer is `[R-SLB-04]`'s trigger, *"or the slab declaration itself"*, which the list's fifth member delegates to; the refuter argued that a rule regulating a change implies the change can occur, and then found the trigger fully explained by three uncontested cases, a first declaration, a whole-file rewrite, and an empty layer re-declared, so that its presence does not reach the disputed one. It quoted the closure clause, the fifth member, `[R-SLB-04]`, step 4's closing sentence and §7.4's alignment row, and named none as deciding. A STANDS from a Sonnet refuter is not provisional the way its downgrades are, and the driver's own search, above, reached the same sentences and one more, the several-at-once licence, and the same end.

**Repaired — ADR-0126, decision 1.** The member reads *"MAY be declared,
changed, re-established or cleared"*, the closing paragraph says the same of a
slab declaration with `[R-SLB-04]` cited, and §11.1's Rationale and Appendix
H carry the verb. The alternative, barring a value change as a rewrite, is
recorded in the ADR so the maintainer can choose it.

## Harness integrity

- **13 agent slots; 12 returned at the first launch, every one on Opus** —
  the runtime's metadata says `opus` for the author, the six walks, the two
  takers and the three passes. The uphold-refuter, on Opus, **was refused at
  zero tokens with `[reasoning_extraction]` at launch and again on the
  unchanged resume**, as in round 32; the one call was set to `sonnet` without rewording, the run resumed a second time, and the refuter returned in four minutes with metadata saying `sonnet`; nothing else re-ran. The first launch took
  71 minutes, 336 tool calls and 3.05 M subagent tokens; the unchanged resume
  replayed every cached result in five seconds.
- **Coverage is opus-grade, by the maintainer's model policy, and the counts
  are recorded beside the one measurement on record.** That measurement: on
  identical hunks, the Sonnet fallback returned 2 findings where the driver
  returned 8. Opus has not been measured against the driver; rounds 31 and 32
  are its calibration lines, 24 findings and 20 defects, then 29 and 19, one
  byte-level each. This round returned 25 findings and 22 distinct defects,
  one byte-level, in a member of the list two audits and a round had read.
  The uphold-refuter's verdict is fallback-grade and is hand-checked in both
  directions; a count says nothing about what an Opus lane missed, and no
  passage is read as clean on it.
- **Every walk's transcript matches its structured return**, by independent
  id-scrape: reader 3, writer 2, verifier 3, diagrams 4, register 6,
  adversary 4, each equal to its own `transcript_finding_count`; the quiz
  author's 3 make 25.
- **All three triage passes CLEAN on mechanical coverage** — 25 of 25 ids
  each, by set difference. The implementer and skeptic partitioned into 22
  groups each and the correctness pass into 24, splitting `writer-02` from
  `adversary-03` and `diagrams-04` from `register-04`; union-find gives 22.
- **The result was rebuilt from the journal**: 13 of 13 results substituted, none unused, and the 29
  ellipsis characters left are literal, checked by a walk for strings ending
  in one, which found none.
- **The quiz slate is Opus-grade and graded 15/15**; its author reproduced
  every CRC constant the document states and re-derived §21.8's 120 / 277 by
  table before authoring a numeric question.
- **No pass ran a directory listing**, and no pass opened a walk transcript.
- **The refuter briefs carried every pass's verdict beside its rationale**,
  round 32's harness defect being fixed, and the uphold-refuter's brief was
  the one call refused.

### Disclosures

Every spec-reading agent disclosed injected context — the project
instruction pointer and an index of memory-note titles — and used none of
it; several also named a git-status block carrying recent commit subjects
that describe the changes under review, and said what they did about it. No
persisted-output form appeared this round. Every walk and the quiz author
wrote and validated a CRC-32C script against §4.5's check vector before
trusting a printed constant.

## Disposition

**Zero findings are left without a disposition.**

### Repaired — ADR-0126

| Defect | Reporters | Repair |
|---|---|---|
| The closed list's fifth member does not say whether an already-declared alignment or slab may change to another value — **byte-level** | writer-01 | decision 1: *declared, changed, re-established or cleared*, at four sites |
| Step 4's MUST NOT binds an actor while leaving a conforming file, and no sentence says which of `[R-CNF-02]`'s categories that is; §2.1's Note claims every writer prohibition is paired with a reader clause | writer-02, adversary-03 | decision 2: the bar names its category; `[R-MTA-09]`'s SHOULD states its consequence |
| §5.2 and §9.7 dispose of a structurally rejected entry's bytes without §15.3's *no other claimant* qualifier | verifier-01, quiz-02 | the qualifier at both |
| §21.1's convention for the Governing-rule parenthetical admits no section reference; R10 alone omits `[R-CNT-25]` | diagrams-04, register-04 | the convention names the case; R10 cites the quarantine |
| §19.1's open path computes F − 64 before the 128-byte floor | reader-01 | step 1 states the floor |
| `[R-CNF-02]`'s enumeration omits `[R-LIF-02]`'s barriers, which §9.2 declares conduct rules | reader-02 | listed |
| §4.7's Note says §7.4's table omits two columns; it omits three | diagrams-01 | *offset, size and class* |
| §20.5's slack Note omits superseded payloads and record extents | diagrams-02 | named as the largest term |
| Appendix F omits RFC 1950 and RFC 1952 | diagrams-03 | both listed |
| §21.6's one reason for excluding two capability refusals is true of one | register-01 | each case its own reason |
| §21.1 attributes every §21.5 row to `[R-CNT-25]`'s quarantine alone | register-02 | `[R-MTA-09]` named beside it |
| §5.1 calls superseded directories and trailers *structures* | adversary-01 | *regions*, the superseded ones slack |
| *the position of every planar channel but the last* reads as barring a run removal | quiz-01 | *the position of every planar channel the new state keeps* |

### Deferred

| Defect | Reporters | Where |
|---|---|---|
| The naming duty on an uninspected extent reaches the checksummed one and not the unchecksummed one | verifier-02 | Q-C8, round-33 note: a known question, found from the other side |
| A compactor's duty to refuse a malformed entry turns on its placement choice | quiz-03 | Q-C10, new; round 32 declined the same finding and three passes now call it a decision |
| §21.1's own rules carry no requirement identifier; F33 and L18 individuate a pair by single claimant kinds | register-05, register-03 | Q-I7, new, beside the register debts |

### Declined

Three findings the passes refuted on sentences they quoted, and the
hand-check agrees: `adversary-02`, §21.5's experimental-encoding exception
leaves R2 in force by `[R-MTA-10]`'s closed three-item list; `adversary-04`,
the *"replacing the last channel"* gloss cannot reach a rename the same step
permits twice; `reader-03`, §18.2's *"1 or 2; see below"* is the document's
deferral practice, §15.1's cells doing the same. Two more the text decides:
`register-06`, F5's second instance reaches committed_file_length through
`[R-CNT-01]`, which its cell reads; `verifier-03`, `[R-CNF-13]`'s *"applies
unchanged"* preserves an exemption and creates none, and §2.3, F6 and
Appendix H each say a verifier holds none.

## What the round says about the surface it read

Of the twenty-two distinct defects, **six sit in sentences this surface wrote
or rewrote**: the fifth member's verbs, unchanged by this cycle but in the
list it qualified; the bar's missing category, beside the exception this
cycle added; the *"but the last"* clause the cycle's audit rewrote around;
§5.2's and §9.7's slack sentences the erratum touched; §20.5's slack Note the
erratum re-keyed; and §21.6's closing paragraph the erratum rewrote twice.
**Two sit in text a decision left leaning on an older rule**: `[R-CNF-02]`'s
enumeration and §5.1's *structures*. The remaining fourteen are in text no
recent round had touched: the register's conventions and four of its cells,
Appendix F, §4.7's Note, §19.1's open path, the naming duty, the compactor's
placement.

The list ADR-0124 wrote has now produced a byte-level finding in each of the
three readings since: a member composed with another, an exception glossed by
the wrong quantity, and a member whose verbs do not reach a change. Each was
in the permitted side's own words.
