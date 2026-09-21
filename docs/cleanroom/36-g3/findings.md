# Cleanroom round 36 — findings

Protocol: ADR-0034, four phases, over the surface changed since round 35's
charter: ADR-0128's repair of round 35's fork and its seventeen wording
repairs, ADR-0129's restated writer tiers, ADR-0130's layer record at
PE = 0, two audits of them and the maintainer's rulings between the two —
thirty-one passages, 55 hunks over 7 commits, chartered over
`cdaf294..96e4ad4`. Charter: [prompt.md](prompt.md), the cut of `965f209`.

## Verdict

**No byte-level flag: none self-flagged, none upheld by any pass, and the
refute phase, firing on the zero, stood on all eight of its attacks. The
round was read on Sonnet throughout, returned a third of the findings an
Opus round returns, and its zero is weaker evidence than any zero before it.
Whether it meets G3 is the maintainer's to say.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** by hand; the normaliser said 9 / 6, all six being one answer spelled two ways |
| Findings | **8**, from 5 reporters; the register walk and the quiz author returned none, each with a full account |
| Distinct defects | **8** by union-find; the three passes partitioned identically |
| Self-flagged byte-level | **0** |
| Upheld by any triage pass | **0** |
| Refute phase | fired on **the zero**: seven targeted refuters on seven of the eight groups, and a round-wide attacker |
| Refuter verdicts | **eight of eight stand**; the round-wide attacker returned the wrong enum label with an unambiguous account (see *Harness integrity*) |
| Surviving the hand-check as a *new* byte-level ambiguity | **0** |
| Harness | 20 agent slots, 20 returned at the first launch, every one on `claude-sonnet-5` by the runtime's metadata; no refusal, no stall; 54 minutes, 441 tool calls, 3.34 M subagent tokens |
| Coverage | **sonnet-grade** — see *Harness integrity* |

Byte-level history: … → 4 flagged in 3 groups, 1 new → 1 flagged, 1 new →
0 flagged, 0 new → 0 flagged, 1 upheld, 1 new → **0 flagged, 0 upheld, 0
new, on a weaker reader**.

**The criterion, in both halves, and what this round can and cannot say
about it.** By the protocol's letter a zero here meets G3's first half, no
byte-level ambiguity anywhere, and its second, the round that reads the
previous round's repairs returning zero too; the charter said so. The round
returned that zero. But the instrument changed under it. Rounds 31 through
35 ran on Opus and returned 24 to 29 findings and 19 to 22 distinct defects
each; this round ran on Sonnet, on the maintainer's instruction of
2026-09-21 after Opus refused the quiz author twice and the driver had
eleven of its twelve started lanes refused, and returned **8 findings and 8 defects
over a surface wider than any of theirs**. The one measurement on record
had Sonnet returning 2 findings where the driver returned 8 on identical
hunks, and this round's yield is in that proportion. The two audits before
it, also on Sonnet, found three byte-level defects in this same text, so
Sonnet can see a fork; and the text those three sat in has since been
decided by the maintainer and read a second time. A count says nothing about
what a lane missed, and no passage is read as clean on it. **The driver
records the zero and does not declare the criterion met**: that judgement
weighs an instrument, and it is the maintainer's.

## The hand-check

Every verdict of this round is in the direction that clears the gate, so
every one is provisional until checked by hand. All eight groups were read
against the specification; none is byte-level.

1. **`both-sides-sentence-imprecise`** (reader-01; §20.3 step 4's
   tie-break). The sentence says a planar and an interleaved channel list are
   each *"on both sides"*; the permitted list names the planar one alone and
   the fixed list the interleaved one alone, each reaching the other only
   through a general clause. Every commit on either kind of list is
   classified the same way under the face-value reading and the
   cross-checked one, because the two lists decide and the sentence
   summarizes. Wording, in a sentence ADR-0126 and ADR-0127 each rewrote.
2. **`appender-rewriter-mu1-asymmetry-unexplained`** (reader-02; §20.4's
   MU = 1 row, decision E2's text). An appender is blocked from one layer and
   a rewriter from the whole file on the same trigger, and no one sentence
   says why. Each rule is plain, *"its drop included"* decides the drop, and
   the reasons are `[R-LIF-01]`'s and `[R-WRT-06]`'s. An observation; no actor
   is left undecided.
3. **`verifier-decode-note-overstated`** (writer-01; §3.3's Note). The Note
   lists verifiers among the actors that *"operate on files whose layers they
   cannot decode"*, and §9.7 has a certifying verifier decode every stored
   tile. A labelled Note, no normative sentence defers to it, and the claim
   about verifiers predates this cycle; the cycle's rename touched the
   sentence and left it. Repairable.
4. **`conformance-vector-total-unverified`** (verifier-01; §21.8's 277).
   Not a defect: the register walk of this same round recounted the register
   by hand and by script to 56 + 116 + 55 + 50 = 277 instances over 120
   conditions, and `tarn_check` establishes 277 of 277 mechanically.
5. **`crc-fail-transparency-already-stated`** (verifier-02; §15.3, §16.2).
   The reporter found the text correct and hard to hold in mind; the
   correctness pass refuted it as a finding, the other two kept it as
   editorial, and its refuter found the rule stated in terms three times,
   row L41 included. Not a defect. This is the round's one pass
   disagreement, and it is about whether a correct passage is a finding.
6. **`figure-b-unclosed-bracket`** (diagrams-01; §20.3's Example, figure
   (b)). The second annotation bracket has no closing `┘`, the only one in
   the document without it. A labelled Example. Repairable.
7. **`unlabeled-normative-blockquote-15-1`** (adversary-01; §15.1). The
   index-region layout is an unlabelled blockquote and therefore normative
   under `[R-CNF-01]`. Known, and the charter names it: *"A blockquote
   carrying no such label is normative. At least one exists."* Everything in
   it is pinned again by `[R-IDX-01]` and `[R-CNT-17]`.
8. **`pe0-updater-commit-clause-loose`** (adversary-02; §20.4's last row),
   **the group the cap left unattacked, checked by hand alone.** *"an updater
   MAY drop the record in any commit"* gives a commit-shaped licence to a
   class one of whose tiers never commits. The same sentence licenses the
   rewriter's drop in its next clause, so each real operation is licensed
   once and no actor gains or loses a drop under either reading of
   *updater*. The pre-round audit's tiers lane raised the same clause as
   D-07 and the driver declined it; a second independent reader has now
   found it, and it is repairable in one word.

**The round-wide attacker's strongest construction is a decided question.**
It set §19.1 step 1, F below 128 as a validity error *"decided from F alone
and needing no other byte of the file"*, against `[R-CNF-13]`'s *"F5 does
not reach"* a file declaring another major, and closed it on the accepted
set not moving. The hand-check agrees about the accepted set and adds what
the attacker could not know: this is Q-H4, resolved by ADR-0105 on the
ground that reach is decided by the invariant a condition asserts and not by
detection order, `[R-RDR-02]` licensing earlier detection anyway. Step 1's
wording carries no exception for such a file, and a verifier's verdict on a
file of 80 to 127 bytes declaring another major is *nonconforming* by step
1's words and *cannot establish* by `[R-CNF-13]`'s; the rule governs, the
file is refused either way, and the residue is recorded here against Q-H4's
resolution and is not new.

## Harness integrity

- **20 agent slots, 20 returned at the first launch, every one on Sonnet.**
  The runtime's metadata says `claude-sonnet-5` for all twenty: the quiz
  author, six walks, two takers, three passes, seven targeted refuters and
  the round-wide attacker. `preflight.py`'s model check passed before launch
  (8 model sites, 13 rendered calls, all `sonnet`). **No refusal and no
  stall**: every walk returned within 25 minutes of starting. This is the
  first round on Sonnet. Two attempts preceded it under the same charter and produced
  nothing of record: Opus refused the quiz author twice with
  `[reasoning_extraction]`, and a run on the driver had every lane but the
  quiz author refused by the driver's safeguards.
- **Coverage is sonnet-grade, and the counts are recorded beside the
  measurements on record.** Sonnet returned 2 findings where the driver
  returned 8 on identical hunks (2026-09-03). Opus's calibration lines are
  rounds 31 through 35: 24/20/1, 29/19/1, 25/22/1, 26/21/0, 25/22/1
  (findings, defects, byte-level). This round: **8/8/0**. The two Sonnet
  audits of this cycle returned 44 findings over 49 hunks and 18 over 26,
  with three byte-level defects in the first. No passage is read as clean on
  this round's count.
- **Every walk's structured return matches its transcript by count**: reader
  2, writer 1, verifier 2, diagrams 1, register 0, adversary 2, each equal to
  its own `transcript_finding_count`; the quiz author 0.
- **The register walk returned no finding, with the account an empty return
  owes**: row against rule across the extent-slot disjunction, §15.3's entry
  table against T1 and T6 through T12, the reserved-range pairs, §10.2's
  spaces against their rows and R4's sixteen instances; all 28 citations of a
  row outside §21 resolved; 120 conditions and 277 instances recounted by
  hand and by script; every §21.9 limit checked both ways. The quiz author's
  empty return reproduced the document's two CRC-32C check vectors, Appendix
  A's trailer CRC and §15.4's all-sentinel constant before authoring.
- **All three triage passes CLEAN on mechanical coverage**: 8 of 8 ids each
  by set difference, every `all_input_ids_seen` exact, three identical
  partitions, union-find 8.
- **The result was rebuilt from the journal**: 20 of 20 results substituted
  from the launch's wrapper, none unused; the two ellipsis characters left
  are literal. The journal holds 20 starts, 20 results and no failure.
- **The round-wide attacker returned the wrong verdict label.** Told to
  return `DOWNGRADE_STANDS` or `DOWNGRADE_REFUTED`, it returned
  `UPHOLD_STANDS`, a label of the uphold-refuter's. Its account states its
  verdict in terms, no fork found after four constructions, and
  [round-refute-verdicts.md](round-refute-verdicts.md) quotes it. The schema
  should restrict that call's enum to its own two labels.
- **The quiz's six "divergences" are the normaliser's.** Q03, Q04, Q07, Q08,
  Q10 and Q11 each differ between the takers only in labelling, *"(a) … (b)
  …"* against prose; the bytes, integers and row labels are identical.
  15 of 15 by hand.

### Disclosures

Every spec-reading agent disclosed injected context — the project
instruction pointer, an index of memory-note titles, and a git-status block
carrying recent commit subjects — and used none of it. **Three agents
disclosed a breach of their own: the quiz author, the writer and the
verifier each ran `ls -la` on the shared output directory**, which the brief
says not to list. The quiz author saw it empty; the writer and the verifier
saw the file names of lanes that had finished and opened none. A lane's file
name says which lanes exist, which every brief already says. Three in one
round is a pattern, and the ACCESS block should say *do not list it* where
it names the directory, not only where it lists what may be read.

## Disposition

### Repairable — proposed for ADR-0131, not yet made

Three, all one clause each: §3.3's Note, which should not list verifiers
among the actors that cannot decode; figure (b)'s unclosed bracket; and
§20.4's last row, *an appender* for *an updater* before *in any commit*.
**They are held until the maintainer rules on the verdict**: a spec commit
stales the charter, and a second reading of this same charter on another
instrument, if the maintainer wants one, needs the text the charter names.

### For the maintainer, not a fourth rewording

Step 4's tie-break sentence (reader-01). ADR-0126 and ADR-0127 each rewrote
it. It admits a face-value reading that is literally false of both examples
and a cross-checked reading that is true, and the two decide every commit
alike. The standing direction is to say so and leave it.

### Declined

`verifier-01`, recounted this round and checked by `tarn_check`.
`verifier-02`, stated three times in terms. `adversary-01`, known and named
by the charter. `reader-02`, an explanation the document does not owe in one
place, each rule being plain where it stands.

## What the round says about the surface it read

**Decisions E1, E2 and E3 drew nothing.** The reader walked §20.4's MU = 1
row and found it decided, *"its drop included"* and all; the adversary
walked the last row and found a loose actor noun; no reporter touched the
two positions of §20.1, the sub-records of a dropped layer, or §7.2's Note.
After two audits and the maintainer's rulings that is what a settled text
looks like, and it is also what a reader that finds a third as much looks
like. The record cannot tell the two apart, and says so.

**Three of the eight findings sit in sentences this cycle touched**, and
none in what it decided: the MU = 1 row, §3.3's renamed Note and the last
row's actor. **Two sit in chartered passages in sentences the surface did
not touch**: step 4's tie-break and figure (b), each a few lines from text
the cycle rewrote. **Three are in text the charter did not name**: §21.8's
total, the slab-run carve-out of §15.3 and §16.2, and §15.1's blockquote.

**The instrument is now the open question.** Sonnet ran every brief, refused
none and stalled on none, in 54 minutes and 3.34 M tokens against round 35's
80 minutes and 3.12 M on Opus. It returned a third of the findings. A zero
from it is a necessary condition for G3 and was not, before this round,
anyone's idea of a sufficient one.
