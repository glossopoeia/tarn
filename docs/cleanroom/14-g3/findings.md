# Cleanroom round 14 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**One byte-level ambiguity. G3 is not met on this round's evidence.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 23 — reader 2, writer 5, verifier 3, diagrams 4, register 4, adversary 2, quiz author 3 |
| Distinct defects | **15** (plus 3 the maintainer found independently) |
| Self-flagged byte-level by reporters | 1 |
| **Byte-level, after triage and hand-check** | **1** |

Round 13 met the criterion and then produced seventeen repairs. This round
read those repairs, and the defect it found is in one of them — the fifth
time in the project's history that the next round's defect sat in the
previous round's repair, and the second time in the repair that closed the
round before.

## The survivor: a declaration freeze with no tense

§20.3 step 4 bars a commit that alters, "for any tile that layer
**stores**, what §14 fixes for its stored bytes or how they decode". Which
generation *stores* refers to was never fixed. The separating operation is
ordinary: **recompressing a layer** — change the codec, re-emit every
stored tile under it. Against the prior generation's stored set the commit
is barred; against the set the commit publishes it is permitted.

Two of three passes upheld it byte-level. Both asserted that no text in the
document names a tense, and **both were wrong**: §3.1 says "unqualified
*stored* means stored in the live generation". The correctness pass found
it; the other two missed it and graded on its absence. The finding survives
the correction anyway, because §3.1's *live generation* during a commit in
flight is the pre-commit one while §20.3's own gloss is framed on the
committed outcome, and nothing arbitrates.

The byte-level claim was verified by hand rather than accepted. A creator
emits generation 1 (§20.1) and a compactor generation 1 under a fresh
`file_id`, so a generation-g+1 file is producible only by a commit, and the
two-commit workaround publishes at g+2. The disputed byte sequence is
emittable under one reading and by no conforming implementation under the
other — which is what distinguishes this from round 13's `writer-02`, where
a creator could emit the same file from scratch and the finding was
correctly downgraded.

Settled in [ADR-0078](../../decisions/0078-a-declaration-freeze-with-a-tense.md):
**the tense is the prior generation's**, on the ground ADR-0068 and
ADR-0074 already established — re-emitting a layer's tiles strands the
originals as slack, and the permissive reading is the one that hides that
cost. The ADR records two things the decision does not buy: the rule steers
rather than prevents, since two commits still reach the same end state with
the same stranded bytes; and the bar loses its witness precisely where a
commit supersedes every tile it would have damaged, so §21.7 now lists it
beside `[R-LIF-01]` as a property of a prior generation that no single file
exhibits.

## The recurrence

Seven of eight reporters independently found §21.1's direction axis applied
at T3/T14/T22 but not at F17, L21, L22 and L30. This is the **third**
consecutive round to find that one criterion incomplete, because each round
has fixed the rows it named rather than sweeping the rule across the
register.

This round swept it mechanically over all 121 rows. The sweep confirmed the
reporters' list exactly and, in doing so, falsified the criterion ADR-0077
had written: it wrongly caught F14's trailer CRC, where *greater* names
nothing, and L20, L29 and T5's `≠ 0` nonzero tests, which are value tests
rather than comparisons of two quantities. §21.1 now excludes both classes,
and the four cells gained the axis.

## The maintainer's own pass

Run against the same repairs while the round was in flight, and reported
here because a round is measured by what it finds and what it misses. It
found one defect the round did not: §20.3's "a change that reaches none of
**these**" binds either to the enumerated declarations or to the effect
clause they gloss, and the two readings disagree — the sentence written in
round 13 to remove exactly that confusion reproduced it one clause later. A
first assessment calling it self-contradictory was corrected to an
ambiguity with a signposted charitable reading before it was acted on.

It also found four prose lines from round 13's repairs exceeding the
document's hard wrap, since fixed. A third observation — that
`[R-SLB-04]`'s "run partition" is grounded only in `[R-SLB-02]`'s verb —
was considered and left: §16.2 says "Runs partition each contiguous block
of disk ordinals independently", which carries the term.

## Harness

**The first fully clean run**: twelve agents, no errors, no dead walks, no
dead triage, twelve journal rows, every transcript matching its structured
return, and all three passes covering all 23 ids with exact
`all_input_ids_seen`. The empty-slate guard added after round 13 was not
exercised, the quiz author having survived.

Six agents stalled and were retried. That is a new operational shape, and
the transcripts were diffed against the returns specifically because a
retry could leave a transcript from the stalled attempt beside a return
from the retry. They matched.

## Disposition

All 15 dispositioned: **15 fixed, 0 deferred, 0 escalated**, plus the
maintainer's three.

Beyond those named: `[R-CNT-21]`'s slack-total MUST no longer presupposes
an F the trailer gate may have denied, and now says what a
walk-established layer rejection does to claimants it had already
enumerated; `[R-WRT-07]`'s enumeration gained the MU = 1 type a compactor
*does* implement, which §7.2 expressly admits; §21.2 says outright that its
rows presuppose a file declaring format major 1; §21.1's outcome-follows-
from-scope clause gained the quarantine's exception; the Governing rule
column's parenthesised identifiers gained the convention they follow;
Appendix G's item 2 says which eight digest bytes, its item 3 fixes the
first structure's offset, and its recap stopped omitting item 10; §20.3's
"an extent MAY always grow" gained the one bound that contradicts it
(`[R-COD-07]`'s lz4 cap, L44); and §16.2 no longer claims the slab
invariant is decidable from index bytes alone when §15.3 needs F.

Register and corpus: **121 conditions over 273 instances, 325 vectors.**
