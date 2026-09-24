# Fidelity calibration 2 — findings

Protocol: ADR-0133, decision 4, and the erratum of 2026-09-22, which owed a
second calibration "over a stretch of B the rewrite has reworded, with seeds
whose rule A states once". Edition A is `spec/tarn.md` at `81e2ad2` (tag
`edition-a`). Edition B for this run is a copy of the `readable` branch's
`spec/tarn.md` at `f1feb3f` (22 commits into the rewrite: §1 rewritten, §3
reordered and reworded, §2.3 and §2.4 cut to their rules with eight IDs in
`reworded-ids.txt`) carrying six planted changes
([seed-manifest.json](seed-manifest.json), [seeded-edition.diff](seeded-edition.diff)),
served under the neutral path `editions/c/tarn.md`. Every seed sits inside
text the rewrite had already reworded, so no diff against A isolates it. Run
`wf_c16a4649-e70`, 2026-09-24.

The question this run answers is the one calibration 0 could not: **do the
two-edition instruments read a reworded rule, or only diff it?**

## Verdict

**They read. Every one of the four seeds that was a content change was found
by at least two reading instruments, graded a byte-level LOSS by all three
triage passes, and upheld by its refuter; the two seeds that turned out to be
restatement removals were graded LOSS by triage and then correctly overturned
by their refuters, each with the surviving statement quoted. The inventory
tool saw none of the six, by construction. Calibration 0's caveat on the
reading instruments is discharged, with one measured weakness: a single-word
flip inside a long reworded sentence (C5) was found by two of the six
two-edition lanes.**

| | |
|---|---|
| Seeds | 6, all prose, all inside reworded text; 4 content changes (C1, C2, C4, C5) and, as the run showed, 2 restatement removals (C3, C6) |
| `tarn_inventory.py` A against C | PASS, the same 17 soft items as A against B: five seeds hidden behind `ID_REWORDED_LISTED`, one in an ID-less paragraph |
| Found by two-edition instruments | C1 by 6 of 6 lanes, C2 by 5, C4 by 5, C6 by 4, C3 by 2, C5 by 2 |
| Found by blind walks, quiz, probes | 0 of 6 |
| Triage (three passes) | unanimous byte-level LOSS on C1, C2, C4 (+C5 in its group); unanimous LOSS on C3 and C6 |
| Refute | C1, C2, C4 `LOSS_STANDS`; C3 and C6 `LOSS_REFUTED`, correctly, on §20.1 / §4.2 and on §9.7 |
| The rewrite's own edits | every one graded EQUIVALENT after refute, save the closed-list cut in `[R-CNF-02]` (one pass: LOSS, clarity) |
| Harness | 31 agent slots, 31 returned, 0 failed; 64 minutes, 779 tool calls, 4.77 M tokens; every call on Sonnet |
| Coverage | sonnet-grade |

## What each seed taught

1. **C1, `[R-CNF-02]`'s conduct rule flipped** ("never makes a file
   nonconforming" → "a file that breaks one is nonconforming"). Found by
   every two-edition lane: the three comparators, both sweeps and the
   adversary, most of them by checking it against C's own §6.3, §9.2 or
   §20.3 rather than against A. Byte-level LOSS, unanimous; the loss-refuter
   re-derived it from the raw files and stood.
2. **C2, the record-type duty dropped from `[R-CNF-03]`.** Found by five
   lanes, four of them by noticing that Appendix H's checklist still
   attributes the full list to `[R-CNF-03]`. Byte-level LOSS, unanimous,
   `LOSS_STANDS`. A reading instrument that cross-checks a reworded list
   against the document's own restatements is what caught it.
3. **C3, "Verifiers and updaters are readers" narrowed to verifiers.** Found
   by the reader and verifier comparators only; LOSS, unanimous; and then
   **`LOSS_REFUTED`, correctly**: §20.1 says an updater "is a reader of
   every structure it processes (`[R-CNF-11]`)" and §4.2 says "a reader —
   including any updater or verifier, which are readers of the files they
   process", both byte-identical in C. The seed was a restatement removal,
   mislabelled `statement_count` 1 because the planter's `terms` regex
   matched the phrase and not the rule. Same mistake as calibration 0's S1
   and S6; the pipeline showed the same restraint.
4. **C4, a reaching failure made a capability refusal** (`[R-CNF-13]`).
   Found by five lanes; the reader comparator and the adversary both noted
   that C's next sentence (the `[R-CNT-07]` diagnostic) only makes sense on
   A's assignment, so C contradicts itself. Byte-level LOSS, unanimous,
   `LOSS_STANDS` with a constructed file (version_major = 2, F14 failing).
5. **C5, the `[R-CNT-04]` exemption made to lapse** (one word, in the same
   sentence as C4). Found by two lanes, the adversary and the B→A sweep,
   each reporting it beside C4 as "two clauses flipped"; every triage pass
   folded it into C4's group, so it never had a grade of its own. The
   equivalence-refuter attacking a different group in the same paragraph
   (the Note cut) re-read the paragraph in full and found both flips. **This
   is the measured floor**: a one-word inversion inside a long reworded
   sentence reaches triage only through a lane that reads the sentence
   clause by clause.
6. **C6, the resource-decline ground cut from the paragraph moved to
   §21.6.** Found by four lanes (the writer comparator through §9.7, which
   "independently states the missing ground's consequence"); LOSS,
   unanimous; and then **`LOSS_REFUTED`, correctly**: §9.7 says a verifier
   "that declines a tile's decode on resource grounds reports that check
   unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)", byte-identical
   in both editions, and §21.6's own table row states the `[R-MTA-10]`
   carve-out's consequence. A second mislabelled seed; and a correction to
   the rewrite's record: the edit-log entry for `2c00338` says three of the
   five grounds are tied to the verdict "nowhere else", which is wrong for
   this one.

**Two of six seeds were restatement removals for the second calibration
running.** Both times the planter checked "stated once" by grepping the
rule's phrase. The check has to be for the rule: every phrasing, and the
consequence words (*cannot certify* for *cannot establish*, *is a reader of*
for *inherit every reader obligation*). The refuters found what the planter
did not, which is the finding about the refuters worth having.

## The instruments, one by one

- **`tarn_inventory.py`**: PASS on A against C with exactly the soft items A
  against B carries. A seed inside a listed ID paragraph is invisible to it
  by design; this run confirms that a listed rewording is where a silent
  rule change would hide, and that the reading instruments are the only
  guard there.
- **The quiz, cross-answered**: 30 questions, none on a seeded sentence;
  quiza-15 came nearest (verifier verdict priority, two sentences from C3)
  and both takers answered it identically from unchanged text. The two quiz
  comparators (new since calibration 0) graded all eleven divergences
  EQUIVALENT, every one taker phrasing, so no quiz item reached triage and
  no refuter was spent on one. The quiz remains a broad net that cannot be
  aimed; it detected nothing here and cost nothing downstream.
- **The six blind walks**: no seed. The probes concern file operations, none
  of which passes through §2.3's reworded sentences, and no seed made C
  inconsistent with itself in a way a probe exercised. Their own findings
  (a missing outcome class for a reader lacking a core codec; F5's instance
  naming; the pad's non-unique slack total; `[R-COD-11]`'s unreachable
  branch; a §20.3-step-4 citation question) are shared indeterminacies of
  A, each confirmed byte-identical by a comparator, and belong to the
  ledger.
- **The three comparators**: reader 4 seeds (C1, C2, C3, C4), writer 3 (C1,
  C2, C6), verifier 4 (C1, C3, C4, C6). Each read the reworded hunks and
  checked them against the rest of the document (Appendix H, §9.7, §20.3,
  §6.3); each also graded the rewrite's permitted cuts EQUIVALENT with the
  surviving location named. The verifier comparator alone graded the
  reach Note's removal and the closed-list cut LOSS.
- **The two sweeps**: A→B found C1, C2, C4, C6; B→A found C1, C2, C4 + C5,
  C6, and graded the §1 condensation, the folded Note, the §3.1 trims and
  the §3.3 removal as restated or non-normative. Both raised the same
  AMBIGUITY on the *addressed tile* rewording, below.
- **The diff-adversary**: C1, C2, C4 + C5, carrying C4 to a constructed
  file. It missed C3 and C6.
- **Triage**: 53 findings (six comparators 43, six walks 8, one author 1,
  one relayed) into 19, 23 and 26 groups; coverage CLEAN on all three, 53 of
  53 ids each; unanimous on every seed group. The three passes disagreed
  only on clarity grades of the rewrite's own edits.
- **Refute**: eight refuters under the cap of ten: five loss-refuters on the
  unanimous losses (C1, C2, C4 stood; C3 and C6 fell, rightly) and three
  equivalence-refuters on the split or clarity-graded groups (the folded
  front-matter Note and the §3.3 removal stood; the reach-Note group was
  "refuted" by a refuter that re-read the whole paragraph and found the C4
  and C5 flips, which belong to another group). No refuter returned
  off-schema; none was recovered from disk.

## The rewrite's own edits, as this run graded them

These are not seeds; they are the edits committed to B between `c486508` and
`f1feb3f`, read by the same instruments.

- **`[R-CNF-02]`'s closed enumeration of expressly-declared cases, cut**:
  the implementer pass graded it LOSS (clarity) as a group of its own; the
  other two passes merged the reporter into C1's group, so it was not
  refuted separately. The edit log already records what was lost (the
  enumeration's closure, a fact about the text). Standing question for the
  maintainer, who approved the cut with that caveat.
- ***addressed tile* redefined "in a generation"** (`6e735a1`): AMBIGUITY
  from both sweeps; EQUIVALENT (clarity) from all three passes, the
  skeptic noting "A's own unchanged §20.3 text already implies this"; not
  attacked. Hand-check agrees: §20.3 step 4, §21.9 and ADR-0079/0122 treat
  the addressed set as per-commit.
- **The reach paragraph's version_major = 0 sentence and its Note, cut**
  (`155e97d`): one pass LOSS (content), two EQUIVALENT; the refuter's
  `EQUIVALENCE_REFUTED` rests on the seeds, not on these cuts. Hand-check:
  EQUIVALENT, §21.2's lead-in stating both.
- **The front-matter Note folded into §1** (`c486508`): two passes LOSS
  (clarity), one EQUIVALENT; `EQUIVALENCE_STANDS`, the two dropped clauses
  found at §4.7's Note and §24.
- **§3.3 removed** (`c58c243`): one pass LOSS (clarity), two EQUIVALENT;
  `EQUIVALENCE_STANDS`.
- **§1 condensed, the `[R-CNF-06]` gloss, the *generation* and *directory*
  trims**: EQUIVALENT, unanimous, each with the surviving location.

## Harness integrity

- 31 agent slots, 31 returned, none failed, none empty; every one on
  `claude-sonnet-5`; no refusal, no stall. Authors 8–9 minutes, takers
  13–15, walks 18–26, comparators and sweeps 9–13, passes 23–25, refuters
  2–3; 64 minutes end to end, 779 tool calls, 4.77 M tokens.
- `rebuild.py` substituted 31 of 31 journal results; `collect-fidelity.py
  --seeds` printed the matrix, grades and verdicts.
- **Disclosures.** Every blind agent read exactly one edition and opened no
  other copy; every two-edition agent read the files its rule named; no
  agent opened the repository's `spec/tarn.md`. Four minor breaches, each
  disclosed: `ls` of the shared output directory by the A quiz author
  (empty), the B reader walk and the B verifier walk (two filenames), and a
  `find` over `editions/` by the B writer walk that printed the three
  editions' filenames; none opened a second file. Every agent disclosed the
  injected context, and the reader comparator noted that the git-status
  block's commit subjects name the reworded stretch (`Readable: §2.3 — …`),
  a channel that names where the rewrite worked and not what was seeded;
  its findings were made by diff and reading and did not depend on it.
- Preflight ran on `/usr/local/bin/node` v22.19.0, Homebrew's node being
  unable to load `libsimdutf.34`; 22 calls rendered under the stub, 24
  briefs under `render-prompts.js`, every A-agent naming `editions/a`,
  every B-agent `editions/c`, none the repository's spec.

## What this calibration settles, and what it mandates

**Settled.** A rule silently flipped or dropped inside a paragraph the
rewrite has reworded is caught by the reading instruments: four content
changes, each by two to six of the six two-edition lanes, each a unanimous
byte-level LOSS upheld on refute. The refute phase's restraint is confirmed
a second time: two apparent losses fell to the surviving statement, quoted.
A fidelity zero over reworded text from this harness is therefore a
measured zero, subject to the floor below.

**The floor.** A one-word inversion inside a long reworded sentence (C5)
reached triage through two lanes and had no group of its own. A zero does
not exclude a change of that size that both of those lanes miss.

**Mandated:**

1. **Seeds are checked for the rule, not the phrase.** `fidelity-seed.py`'s
   `terms` is written as an alternation over every phrasing of the rule and
   its consequence words, and the planter records the search. Two of six seeds
   were restatement removals again; the pipeline's correct grading of them
   is a result, but it was not the result the seeds were planted for.
2. **A refuter that finds a different change reports it as a finding.** The
   reach-Note group's refuter returned `EQUIVALENCE_REFUTED` on evidence
   that belonged to the C4/C5 group. The refute brief needs to say: a change
   outside the group's claim is a new finding with its own location, not a
   refutation.
3. **The rewrite's own "stated once" claims are checked the same way.** The
   edit log's entry for `2c00338` says the resource-decline ground is tied
   to the verdict nowhere else; §9.7 states it. The proposal for C3's
   sentence said the same of updaters inheriting reader obligations; §4.2
   and §20.1 state it. Before a restatement is called unique, search for
   the rule's other words.
4. **ADR-0133's erratum** is owed a record of this run beside calibration 0.
   That is an ADR edit and lands on `main`, not on `readable`.
