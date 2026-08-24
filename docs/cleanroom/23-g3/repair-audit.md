# The repair audit of everything since round 22, before round 23

The first audit to run **check 7** — the "when a repair argues by analogy,
compare the two quantifiers word for word" check added after round 22's
survivor turned out to be the previous cycle's own repair sentence.

It is also the first audit run over an **accumulated** diff rather than one
cycle's repairs. Round 22 read the document at charter commit `7d151d6`;
everything after it was unaudited by a round — ADR-0086's quantifier fix,
ADR-0087's R4 routing and its four vectors, and ADR-0088's carry-over
inversion. Four hunks, 44 insertions over 34 deletions, written by more than
one pass at different times, which is `tarn_propagate`'s second blind spot and
the reason the cross-hunk auditor exists.

| | |
|---|---|
| Auditors | 2 hunk-pair + 1 cross-hunk |
| Findings | **18** (A-01..07, B-01..03, X-01..08) |
| Self-flagged byte-level by auditors | **0** |
| After adversarial verification | 16 REFUTED, 1 PARTIAL, 1 unverified |
| Byte-level after verification | **0** |
| Refute groups | 8, one per finding group |
| **Byte-level after the refute phase** | **0 — all eight returned DOWNGRADE_STANDS** |
| Real defects surviving | **5** |
| Harness | audit 21 agents (interrupted, recovered from `journal.jsonl`); refute 8 agents, 0 errors |

**A unanimous zero is the trigger for the refute phase, not a result.** Round
18's audit verified 31 findings with agents told to default to REFUTED,
returned zero byte-level, and a refute pass overturned all four downgrades.
Here the zero held under all eight attacks, so the accumulated diff is clean at
byte level. Five findings survive as real defects in the text, and are fixed by
ADR-0089.

## The harness failure, and the recovery

The audit run was interrupted at the end of its verify phase — 3 auditors and
17 of 18 verifiers had returned; one verifier (on X-04) was in flight, and the
refute phase had not started. **No work was lost.** All 18 findings and all 17
verdicts were recovered from `journal.jsonl` and re-used as-is; the refute pass
ran as a separate, smaller workflow seeded from them, and X-04 went to its
refuter unjudged and labelled as such.

Two process lessons recorded in the harness rather than here: the audit
workflow had folded audit, verify and refute into one long-lived run, which is
reverted; and `node --check` passing is **not** evidence a workflow's prompts
are intact, because a stray backtick can close a template early and let the
rest of the file re-pair by luck.

## The five that survived

**Two defects in R4's Condition cell** (A-01/X-02 and A-02/X-01 — four
findings, two defects, ADR-0087's text). The refuter flattened the document and
pulled every occurrence of "whether or not": in all seven undisputed ones the
consequent holds in **both** branches of the variable. So the appended clause
asserts the content-size constraint is broken where the field *matches*, which
`[R-MTA-09]` declares conforming. The blanket "broken whether or not the bytes
decode" separately came to range over a constraint whose comparand exists only
on a successful decode. Not byte-level — §21.1's tiebreak and the cell's own
anaphora both close it — but false, not merely loose.

**A-03 — "This section replaces both" is an overclaim** (ADR-0088's text).
`[R-COD-06]`'s writer-side 8 MiB window SHOULD is excepted by §18.2 and
replaced by nothing.

**X-05 leg 1 — two carried-over items R4 cannot register** (ADR-0088's text).
The widened carry-over includes dictionary use "disclosed or not" and the bar
on sizing a buffer from a frame-declared length. R4 registers breaches of that
list as reader-detected file violations, and neither is a state a file
exhibits. §21.1 routes R4's arbitration to `[R-MTA-09]`, so the widened text
governs and the carve-out has to be stated there.

**X-08 secondary — the reader's document bound under encoding 1** (ADR-0088's
text). §18.2 stated the bound only inside the encoding-2 paragraph, and the
repair tied it to "the first exception", an exception to `[R-COD-06]`, which
reaches encoding 2 alone. §21.9's row is encoding-agnostic.

**X-04 — the 16 MiB guarantee is unreachable above 8 MiB.** The one that
predates every recent repair. §21.9 guarantees 16 MiB of user-metadata document
and `[R-ERR-03]` says a writer MAY rely on it; §21.9 separately guarantees
8 MiB of `Window_Size`, over the frames a file contains. For a single-segment
frame RFC 8878 makes `Window_Size` the content-size field, which §18.2 pins to
the decoded document's length. So a 12 MiB document in ordinary framing exceeds
the 8 MiB row. And the single-segment derivation lives **only inside a Note**
whose opening clause reads "for a tile this rule they agree" — no force under
`[R-CNF-01]`, and by its own words not reaching §18.2.

## Three missing sentences

Three of the eight refute groups returned a `missing_sentence`: a place where
the reasoning that answers a finding exists, but only in a commit message or in
`propagation-acks.txt`, never in `spec/tarn.md`. A reader has neither. That is
the finding behind repairs 1, 2 and 3 of ADR-0089, and it is a new failure mode
worth naming — a repair can be *correct* and still leave the document unable to
show why.

## What did not survive

X-07 (hunk 1 declares the constraint set open while hunks 2 and 3 depend on its
closure), X-03 ("checkable from the bytes alone" moved onto a condition needing
a full decode), A-04, A-05, A-06, A-07, B-01, B-02, B-03, and X-06 were all
attacked and none moved the emittable set. B-01 through B-03 in particular were
answered from the document's own text (§5.2, §21.9's own lines, §17.2/T21), not
from reasoning outside it.

## Disclosures

Every agent in both runs — 20 of 20 in the audit, 8 of 8 in the refute pass —
disclosed that unrequested material appeared in its context before it began: a
project instruction pointer and an index of the maintainer's notes. Each named
that it appeared without repeating its contents and stated that no conclusion
rested on it, which is what ADR-0084's ACCESS paragraph asks for. The
repository-side and memory-side lineage gates both return clean.
