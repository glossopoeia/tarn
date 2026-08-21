# Round 18 — the repair audit of round 17

A new instrument, run **before** the round rather than after it. Protocol:
ADR-0034 extended; decision: [ADR-0081](../../decisions/0081-the-drop-licence-regains-its-quantifier.md).

## Why it exists

Rounds 14–17 each found their defect in the *immediately preceding* round's
repair, three of them in §20.3 step 4. Four rounds of the same shape did not
break that pattern, so the check moved earlier: a spec-only audit over the
repair diff, before the next charter is committed.

## Shape

Round 17's repairs — commit `08b9b9d..a42d0b6`, 32 insertions, 22 deletions,
**10 hunks**. One auditor per two or three hunks (six), plus a **cross-hunk**
auditor holding all ten — the only agent able to see two repairs made in the
same commit that are each locally sound and jointly inconsistent, which is
`tarn_propagate`'s second blind spot.

Each auditor ran five checks against every hunk: tense and quantifier;
citations resolve; the repair sits in normative text; no contradiction in the
same passage **including text the repair did not touch**; no exhaustive claim
it cannot carry.

Every finding was then adversarially verified, and every surviving byte-level
downgrade attacked by a refute-only pass.

| | |
|---|---|
| Auditors | 7 (6 hunk-group + 1 cross-hunk) |
| Findings | 31 |
| After adversarial verification | 3 CONFIRMED, 6 PARTIAL, 22 REFUTED |
| Byte-level per the verifiers | **0** |
| Byte-level after the refute phase | **1** (and 3 further downgrades overturned) |
| Harness | 38 agents, 0 errors, 0 empty returns |

## The zero that was not a zero

Thirty-one findings were verified by agents each instructed to **default to
REFUTED**. That produced zero byte-level. Four auditors had independently
flagged byte-level; all four flags were downgraded.

A refute-only pass overturned **all four**. This is round 16's shape exactly:
a shared *framing* — here supplied by the instruction itself — makes verifiers
agree without making them independent. The deciding fact in the surviving
case was one no verifier had weighed: §20.4's gate is lowercase `may … only`
and its conclusion is ALL-CAPS `MAY`, and §2.1 binds BCP 14 keywords "when,
and only when, they appear in all capitals".

**A verdict of zero is the trigger for the refute phase, not a result.**

## What it found that a cleanroom round could not

Two of the three most consequential findings are invisible to any agent
reading `spec/tarn.md` and nothing else — which is every cleanroom agent, by
design:

1. **The ADR trail and the spec disagreed.** ADR-0070 (`Accepted`) said a
   supersede-only commit MUST retain the record; ADR-0080 reversed that
   without recording it; round 17 changed 32 lines of normative text and added
   **no ADR at all**. Found by reading the commit, not the document.
2. **`SPEC-03` was blind to the passage.** Its normativity test exempted every
   line beginning with `|`. The whole document held exactly **two** lowercase
   BCP 14 verbs inside table rows, and **both sat in §20.4 line 3123** — the
   cell that produced the byte-level defect in rounds 10, 14, 16 and 17. The
   check is now section-aware; run against the pre-repair document it reports
   those two hits and nothing else.

## Disposition

Repaired this session: the §20.4 cell (operative `MUST NOT` gate,
scope-matched `MAY`, real citation for "an appender never removes one", the
stranded "either", the em-dash nesting, the "layer set" stretch); §23.1's
"only removal" appositive; §21.7's codec witnesses; Appendix G item 3's first
structure under a declared alignment. `SPEC-03` widened. ADR-0070 marked
superseded.

**Left for the maintainer:** §20.5's compactor disposal, where ADR-0080 says
*reproduce* and round 17 says *MUST refuse*, neither recorded. The audit
faults the reversal's argument on three grounds and does not settle its
conclusion. See ADR-0081, "Left open".

Round 18 itself has not run. The charter is written against the repaired
surface once that decision is taken.
