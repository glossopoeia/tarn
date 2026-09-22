# Fidelity calibration 0 — findings

Protocol: ADR-0133, decision 4. Edition A is `spec/tarn.md` at `81e2ad2`
(tag `edition-a`); edition B for this run is a copy of A with six known
changes planted by `fidelity-seed.py` ([seed-manifest.json](seed-manifest.json),
[seeded-edition.diff](seeded-edition.diff)), served to the agents under the
neutral path `editions/b/tarn.md`. The question this run answers is not
whether B says what A says (it does not, by construction) but **which
instrument catches which kind of change**, so that a zero from a later round
can be read against a measured sensitivity. Run `wf_aa9d31d7-f63`,
2026-09-22.

## Verdict

**Every seed was found and graded correctly, and the hand-check agrees with
every grade. The instruments that read both editions found the six loci by
diffing the two files, which a near-copy invites and a rewritten edition will
not allow; so this run measures the mechanical floor, the grading, and the
blind instruments, and leaves the two-edition instruments' *reading* to a
second calibration over rewritten text.**

| | |
|---|---|
| Seeds | 6: three the inventory tool catches (S4 register, S5 Example figure, S6 ID paragraph), three meant for readers only (S1, S2, S3) |
| Caught by `tarn_inventory.py` | S4 hard, S5 soft, S6 hard; S1–S3 invisible, as designed |
| Found by every two-edition agent | all six loci, by `diff` |
| Graded a content difference (triage, unanimous) | **S2, S3, S4, S5**; S2 and S3 byte-level |
| Graded equivalent (triage, unanimous) | **S1, S6**: each a restatement whose rule survives elsewhere in B |
| Refute phase | four loss-refuters stood on S2–S5; two equivalence-refuters stood on S1 and S6, each naming the surviving statement |
| Blind single-edition walks | caught **S4** (reader from B: F19's instances cell narrower than its own condition) and **S5** (writer from B: 664 against its own arithmetic); nothing else |
| Probes and quiz | **0 of 6**: no probe or question forced a taker into the seeded sentences |
| Quiz | slate A 15/15 and slate B 14/15 on substance by hand; the matcher reported 12/3 and 4/11; all fourteen divergences graded REPORTER_ERROR or EQUIVALENT by every pass, one of them a real taker error (quizb-08) |
| Harness | 35 agent slots, 34 returned, one schema failure recovered from disk; every one on `claude-sonnet-5`; 59 minutes, 720 tool calls, 4.96 M tokens |
| Coverage | sonnet-grade |

## What each seed taught

1. **S1, the blocking-sentence cut** (§20.4's paragraph below the table).
   Graded EQUIVALENT by all three passes; the refuter found the rule stated
   in the table's first row (*"blocks modification of that layer, its drop
   included"*) and, independently, in §7.2's Note (*"never drops the record,
   alone or with the scope it governs"*), and stood. The three comparators
   had graded it a byte-level loss; the passes and the refuter overruled
   them with the surviving text quoted. **The seed was ill-chosen**: ADR-0133
   decision 3 permits removing a restatement where the rule remains, so the
   correct grade was the one returned. That the pipeline returned it is a
   true negative worth having: the passes did not over-report.
2. **S2, step 2's carve-out cut** (*save where §20.4 licenses the drop*).
   Graded LOSS, byte-level, unanimously; the loss-refuter searched B for a
   reconciling sentence and stood. Correct: B's step 2 bars a drop that B's
   own §20.4 licenses, and an appender built from step 2 alone leaves a
   larger file. **Neither blind writer reported it**, and probe W4, which
   asks exactly this drop, was answered from §20.4 by both writers without
   either opening step 2. The probe needs to demand every sentence that
   bears on the act.
3. **S3, the MU = 1 row's reach flipped** (§20.4's lead-in). Graded LOSS,
   byte-level, unanimously: B's sentence contradicts its own next clause.
   Neither blind writer reported the contradiction; probe W3 asks about an
   unimplemented type, where both editions agree.
4. **S4, F19's instances narrowed.** Hard item for the tool; graded LOSS
   unanimously; and **the reader from B found it alone**, as the row's
   instances cell disagreeing with its condition cell. A blind instrument can
   see a mechanical seed when the seed leaves the document inconsistent with
   itself.
5. **S5, 644 to 664.** Soft item for the tool; graded LOSS unanimously (the
   passes disagreed only on byte-level, an Example being non-normative); and
   **the writer from B found it alone**, against `[R-CNT-17]`'s formula.
6. **S6, "MUST NOT clear them" cut from `[R-CNT-08]`.** Hard item for the
   tool (the ID paragraph changed); graded EQUIVALENT by all three passes;
   the refuter tried the narrow reading of *copy forward* and closed it on
   §6.2's cell, *"carried forward unchanged by every updater (appender and
   rewriter alike)"*, and Appendix H's *"clears none"*. Correct, and a second
   ill-chosen seed: the rule is stated three times, so cutting one is a
   permitted restatement removal. The reader comparator alone called it a
   loss.

**Two of the three "agent-only" seeds were restatement removals**, which the
process allows. Only S2 and S3 were content changes a reader had to catch,
and every two-edition instrument caught both, by diff. The next seed set
must plant changes whose rule is stated once (a grep for the rule's terms
returning one hit), and must plant them in rewritten text.

## The instruments, one by one

- **`tarn_inventory.py`**: exactly as its selftest promises. S4 and S6 hard,
  S5 soft, S1–S3 invisible. It also reported the keyword-count drop (one
  MUST NOT) that S6 caused.
- **The quiz, cross-answered**: 30 questions, none on a seeded sentence.
  The one question near a seed (quiza-03, an appender and an ignore-lane
  bit) was answered identically from both editions, because B's remaining
  clause still yields the answer. The matcher's loose form produced fourteen
  divergences of which thirteen were the B-taker's terser phrasing of the
  same answer and one (quizb-08, slack total *partial* against *complete*)
  was taker A misreading a tile decline as a layer decline, on text
  identical in both editions. Every one was graded REPORTER_ERROR or
  EQUIVALENT by every pass; the skeptic named quizb-08's cause. **The quiz
  is a fine detector of taker error and, at this slate, no detector of a
  seeded prose change**; a slate written to the seeds' passages would be,
  and a real round cannot know where to aim. Its value is as a broad net,
  and its matcher needs a comparator or a stricter normaliser before its
  divergences reach triage.
- **The six blind walks**: every probe answered the same from both editions
  on substance (reader R1–R8, writer W1–W8, verifier V1–V6, with R3, V2, V4
  and W8 underdetermined from both alike). Two seeds caught, both by a B
  walker noticing its own edition disagreeing with itself. Their own
  findings about their editions (reader: no outcome class for a reader
  lacking a core codec; writer: the zero-copy drop-and-recreate and the
  cross-layer slab recheck; verifier: an uncertifiable conforming file, the
  open subsumption list, `[R-COD-11]` absent from the partial-total
  triggers) are shared indeterminacies of A, every one confirmed present
  verbatim in both editions by the comparators. They are observations for
  the ledger, not fidelity findings.
- **The three comparators**: each ran `diff` over the two editions (their
  access rule allows both, and both exceed the read tool's cap), found the
  six hunks, and graded them; the writer comparator also closed both
  A-walker findings correctly as shared. They graded S1 a byte-level loss
  and were overruled with quotation.
- **The two sweeps**: both diffed. A into B graded all six (S1 and S6
  equivalent, the rest losses or contradictions); B into A filed three and
  deferred S4 and S6 to the checker, judging S1 redundant. Both did what
  they were told, on a corpus where a diff answers the question.
- **The diff-adversary**: diffed, graded S2–S5 byte-level losses and S1, S6
  equivalent, and carried S2 and S3 to bytes.
- **Triage**: 67 findings (six comparators 43, six walks 10, the quiz matrix
  14, two authors 0); coverage CLEAN on all three passes, 67 of 67 ids each;
  partitions 31/13/31 (the implementer merged the quiz items into one
  group). Unanimous on every seed and on every quiz item.
- **Refute**: sixteen unanimous downgrades of a reported difference (two
  seeds and fourteen quiz items), four unanimous content differences, no
  split, no zero. The cap of ten attacked both seed groups and eight quiz
  groups and dropped six quiz groups, every one graded REPORTER_ERROR or
  EQUIVALENT by every pass and read by hand here (quizb-07, -08, -09, -10,
  -12, -15: five spellings and the one taker error). Every verdict in its
  own vocabulary. One refuter, quizb-03's, returned its result five times
  without the required `decisive_quotes` field and was failed by the
  runtime; its transcript carries `EQUIVALENCE_STANDS` with a full account,
  recovered here as the protocol directs.

## Harness integrity

- 35 agent slots, 34 returned, 1 failed on return shape and recovered; every
  one `claude-sonnet-5` by the runtime's metadata; no refusal, no stall.
  Walks 10–12 minutes, comparators and sweeps 8–12, passes 9–13, refuters
  1–5. 59 minutes end to end.
- The rebuilt result substituted 34 of 34 journal results, none unused, no
  truncation marker left.
- **Disclosures.** Every blind agent read exactly one edition in full and
  opened no other copy; every two-edition agent read the files its rule
  named. Listings were of the agent's own scratch directory only. Every
  agent disclosed injected context, this run's own commit subjects among it
  (*"ADR-0133 accepted …"*), and used none of it.
- Preflight with the launch args rendered 22 prompts, every B-agent naming
  `editions/b`, every A-agent `editions/a`, none the repository's spec.

## What the calibration mandates (ADR-0133 decision 4's rule)

The instruments that missed a seed are the blind walks and the quiz on S1,
S2, S3 and S6, and the probes on S2 and S3. Under the ADR a zero from them is
not trusted until their briefs change and the seeds are caught. The changes,
recorded as ADR-0133's erratum and owed before the first real round:

1. **Calibrate again over rewritten text.** Plant the next seeds inside a
   stretch of B that the maintainer's rewrite has already reworded, so that
   no diff finds them and the sweeps, comparators and adversary must read.
   This is the calibration the two-edition instruments still owe.
2. **Seeds are content changes stated once.** `fidelity-seed.py` records,
   per seed, the grep that shows the rule's terms occur once in A; a seed
   whose rule survives elsewhere tests the passes' restraint, not the
   instruments' reach, and is labelled so.
3. **Probes demand every bearing sentence.** Each probe asks the walker to
   cite every sentence that bears on the act, in every section, and to
   report any two that disagree; and two probes are added on the acts S1 and
   S2 sit on (dropping a layer that carries an MU = 1 sub-record; an
   appender's drop of a carried-forward PE = 0 record, read from step 2 and
   §20.4 both).
4. **Quiz divergences get their own kind** (`QUIZ_DIVERGENCE`), are graded
   by a quiz comparator before triage, and do not draw refuters unless a
   pass grades one LOSS or ADDITION; the refute cap then reaches the
   groups that matter first.
5. **The refute schema's `decisive_quotes`** is kept, with the brief saying
   the field is required and what goes in it; a return failed on shape is
   recovered from the transcript, as here.

Until item 1 has run, the fidelity round's sensitivity to a semantic change
in rewritten prose is unmeasured, and a zero from it is recorded as such.
