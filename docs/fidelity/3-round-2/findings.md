# Fidelity round 2 — findings

Protocol: ADR-0133, decision 4, the second real round after the two
calibrations ([0-calibration](../0-calibration/findings.md),
[1-calibration-2](../1-calibration-2/findings.md)) and round 1
([2-round-1](../2-round-1/findings.md)). Edition A is `spec/tarn.md` at
`81e2ad2` (tag `edition-a`), exported at `scratch/cleanroom/editions/a/tarn.md`
and checked byte-identical to the tag before launch. Edition B is the
`readable` branch's `spec/tarn.md` at `7b5b9a7`, 81 commits into the rewrite:
§1 through §8 rewritten under the maintainer's direction (read by round 1 at
`5220d1a`), §9's five dense paragraphs re-cut, §10 through §24 and Appendices
A, D, G and H spruced up in twenty commits (2026-10-08 to 2026-10-12, 82 rule
paragraphs reworded and four long ones split, every keyword clause verbatim),
and one word restored by the word-diff preflight below; 121 IDs in
`reworded-ids.txt`, 4,755 lines and 48,337 words against A's 4,981 and 49,821.
No seeds: the question is whether B says what A says, and the result is
graded. Run `wf_ed2decfe-4e2`, 2026-10-12, every agent on `claude-sonnet-5`
by the harness constant; the launch turn was the single word "Go".

## Verdict

**No byte-level divergence and no addition, and nothing graded LOSS or
ADDITION by any lane anywhere from §5 to the end of the document. The
spruce-up series, which this round was run to grade before the maintainer's
read-through layers edits on it, drew no finding at all: every blind walk and
every quiz taker read the same rules from both editions, the three
comparators found every reworded rule in §9 through §24 and the appendices
deciding what A decides, the two sweeps and the adversary found nothing B
states that A does not, and the adversary's six constructions produced
identical bytes and verdicts under both editions. Eight groups were graded
LOSS by at least one triage pass, all eight in the front matter and §1
through §4, and every one is a cut of explanatory prose the edit log records
and the maintainer approved: five are round 1's items 3 through 6 (the §3.3
Note and §1's roadmap sentence, graded as two groups this time; §2.4's
preserve-verbatim bridge; §2.4's reject Note; §2.3's reach Note), ruled kept
cut on 2026-10-08; three are new grades on cuts from 2026-09-23 and
2026-09-25 (§4.4's bit-numbering Note, the tail of §4.7's layout-table Note,
the front-matter clause on vectors citing identifiers). Two groups were
unanimous LOSS and six were 2–1 splits with the skeptic pass grading
EQUIVALENT; all six split refuters stood on EQUIVALENT, the bridge's
loss-refuter stood on LOSS, and the reach Note's loss-refuter overturned
its LOSS on text byte-identical in both editions. The hand-check finds the
rule each cut explained standing in B for all eight and grades all eight
EQUIVALENT; under decision 4 all eight go to the maintainer with both texts.
The absence of a byte-level divergence is measured by calibration 2, subject
to its floor: a one-word inversion inside a long reworded sentence reached
triage there through two of six lanes, and a change of that size that both
lanes miss is not excluded here.**

| | |
|---|---|
| Edition B | `readable` at `7b5b9a7`: §1–§8 rewritten, §9–§24 and Appendices A, D, G, H spruced up, 121 listed IDs, 4,755 lines against A's 4,981 |
| Byte-level LOSS surviving the hand-check | **0** |
| ADDITION | **0**: both sweeps, the three comparators and the adversary tried the §3.1 *addressed tile* candidate again and closed it on §11.1's Rationale, `[R-CNT-17]` and §20.3 step 4, byte-identical in both editions |
| LOSS graded by triage | **8 groups**, every one a logged cut of explanatory prose in the front matter and §1–§4; 2 unanimous, 6 split 2–1; EQUIVALENT by hand; to the maintainer with both texts, five of them ruled kept cut on 2026-10-08 |
| Findings in §5 through Appendix H | **0** graded LOSS or ADDITION by any lane; the comparators' relocation findings there (§6.3 → §20.5, §7.1 → §7.3) EQUIVALENT by every pass |
| Quiz | 30 questions; slate A 15 of 15 agree; slate B 14 of 15, the one loose divergence graded EQUIVALENT by its quiz comparator and by hand; 0 reached triage |
| Blind walks | 10 own-edition findings, every one shared text of A (ledger); no fidelity difference |
| Triage | 38 findings into 21, 21 and 21 groups; coverage CLEAN, 38 of 38 ids on each pass; byte-level groups 0, 0 and 0; LOSS groups 2, 8 and 8 |
| Refute | 6 equivalence-refuters on the splits, all `EQUIVALENCE_STANDS`; 2 loss-refuters on the unanimous groups, one `LOSS_STANDS` and one `LOSS_REFUTED`; no zero-attacker |
| Harness | 30 slots, 30 returned, 0 failed, 0 degenerate, no refusal, no stall; every agent `claude-sonnet-5`; the launch message "Go" disclosed by all 30 and acted on by none; 66 minutes, 869 tool calls, 4.78 M tokens |
| Word-diff preflight | 21 commits checked word by word before launch; one transcription loss ("above", §9.7) found and restored as `7b5b9a7`; [word-diff.md](word-diff.md) |
| Coverage | sonnet-grade |

## The LOSS grades, hand-checked

Eight groups were graded LOSS by at least one triage pass. Every one sits on
a cut the edit log records, with the surviving location named there, and
every one is hand-checked here against both editions. None is byte-level by
any pass's account; the B-into-A sweep self-flagged the first as byte-level
and all three passes set the flag aside. ADR-0133 decision 4 and the
maintainer's standing instruction send every LOSS on an approved cut to the
maintainer with both texts quoted, so all eight are listed in full, the five
already ruled with their ruling.

1. **§2.4's preserve-verbatim bridge** (`cmp-reader-04` EQUIVALENT,
   `swab-03` LOSS, `swba-01` LOSS byte-level, `adv-01` LOSS; unanimous LOSS
   at triage, `LOSS_STANDS` on refute). A, after `[R-CNF-07]`: *"The same
   vocabulary is used for defined conditions that are not violations (an
   unknown ancillary record is *ignored*, not rejected). **preserve-verbatim**
   names an updater obligation, orthogonal to reader outcomes: a record a
   reader ignores can still be one an updater preserves."* B ends the
   paragraph at the ID. Round 1's item 4, ruled kept cut. Hand-check: B's
   §20.4 obliges an updater to re-emit byte-identically *"every record it
   retains and does not logically modify, whether or not it implements the
   record's type"* (`[R-WRT-05]`), and its preservation table keys the duty
   to the stored MU and PE bits alone; B's §21.6 table writes *"Ignored
   (ignore-record); the file is conforming"* for a non-violation. The
   sweep's byte-level argument, that an updater built from B's §2.4 alone
   might drop a reader-ignored record, is answered by the table: the adversary
   carried exactly that record (MU = 0, PE = 1, unimplemented) to §20.4's
   row, *"Retain byte-identical, extent content unmodified"*, identical in
   both editions, and the refuter that stood on LOSS confirmed the table
   decides the duty without the bridge. **EQUIVALENT by hand; a restatement
   removal the log records and the maintainer kept cut.**

2. **§2.3's three-row reach Note** (`swab-01` LOSS; unanimous LOSS at
   triage, `LOSS_REFUTED`). A closes §2.3 with a Note working F14, F5 and
   F15 through `[R-CNF-13]`'s test (*"F14 reaches although the bytes it
   checksums include fields a future major may redefine … F5 does not reach
   although its subject is the physical file size … F15 does not reach
   although its Governing rule cell cites `[R-CNT-24]` …"*). Absent from B.
   Round 1's item 6, ruled kept cut. Hand-check: §21.2's lead-in, identical
   in both editions, says *"Deriving it there yields F8, F14, F6 and both of
   F1's instances … and no other row"*; the refuter added that B's §2.3 states
   the test's general form (*"a check can read bytes a future major is free
   to redefine and still assert only a property fixed for every major"*) and
   that `[R-CNT-24]`'s *"only the remaining 48 trailer bytes"* decides F15,
   both byte-identical in both editions. **EQUIVALENT by hand; a worked
   illustration cut under decision 3 and kept cut.**

3. **§2.4's reject Note** (`swab-02` LOSS, `swba-02` OBSERVATION, `adv-02`
   LOSS; split at triage, `EQUIVALENCE_STANDS`). A: *"**Note.** "Reject"
   prescribes the scope of unusability, not user interface: how failure is
   reported is implementation technique."* Absent from B. Round 1's item 5,
   ruled kept cut. Hand-check: §2.1's Note, that requirements constrain
   *"bytes and observable behavior, never implementation technique"*, is
   byte-identical in both editions. **EQUIVALENT by hand.**

4. **§3.3's Note** (`swab-04` LOSS, `adv-03` LOSS; split, `EQUIVALENCE_STANDS`)
   and 5. **§1's roadmap sentence** (`swab-07` LOSS; split,
   `EQUIVALENCE_STANDS`). A's §3.3: *"Part I (container) is independent of
   Part II (array model) by construction: no Part I structure requires
   decoding sample payloads, so appenders, and rewriters that carry a layer
   forward, operate on files whose layers they cannot decode — that
   independence is load-bearing for the updater rules of §7 and §20."* A's
   §1: *"Part I alone yields a container reader — one that opens files, walks
   the directory, and lists layers without decoding a sample; returning
   sample values needs Part II as well …"*. B has neither. Round 1's item 3,
   ruled kept cut. Hand-check: the permission the claim explains is stated
   operatively at §20.1 and §20.4 (`[R-WRT-01]`, `[R-WRT-05]`), byte-identical
   in both editions; §1 is non-normative under `[R-CNF-01]` in both. The
   B-into-A sweep reached the same closure on §20.4 and §20.5 and did not
   report either as a loss. **EQUIVALENT by hand.**

6. **§4.4's bit-numbering Note** (`swab-05` LOSS; split, `EQUIVALENCE_STANDS`).
   A closes §4.4: *"**Note.** This rule fixes bit numbering in flags and
   packed fields generally; the mapping of boolean *samples* to bits is
   defined in §14."* B's §4.4 ends at `[R-ENC-08]`. Cut 2026-09-25 (the §4
   entry, item 3), the surviving location named as §14.3. Hand-check: §14.3,
   identical in both editions, says *"the tile's P values bit-packed
   LSB-first: value k occupies bit k mod 8 of byte ⌊k / 8⌋ (§4.4)"*, so the
   mapping the Note pointed at is stated where the Note said, with the same
   pointer back; `[R-ENC-08]` is cited nowhere else in either edition. The
   B-into-A sweep found the §14.3 citation and reported no loss. **EQUIVALENT
   by hand; a navigational Note cut under decision 3; new to the
   maintainer.**

7. **The tail of §4.7's layout-table Note** (`swab-06` LOSS; split,
   `EQUIVALENCE_STANDS`). A's Note ends: *"A name is structural: a duplicate
   is a validity error at file or layer scope (`[R-ENC-15]`, F4, L9), and its
   length prefix is §7.4's framing, not its value. Every non-obvious encoding
   is followed by a worked numeric example, and every sentinel or overloaded
   encoding additionally has a paired conformance vector. All named constants
   appear once in Appendix B."* B's Note ends two sentences earlier, at
   *"… the field's remaining bounds are stated in the rules below the
   table."* Cut 2026-09-25 (the §4 entry, item 6), then the Note re-cut in
   plain sentences on 2026-09-27. Hand-check: the duplicate-name rule stands
   at §4.6 `[R-ENC-15]` and in rows F4 and L9, byte-identical in both
   editions; *"every other field this specification defines is structural"*
   (`[R-ENC-16]`) stands in B's §4.7; the three remaining sentences describe
   the document's own conventions (ADR-0003's), not a rule. The refuter's
   `new_findings` names `[R-ENC-16]`'s cut citation clause, *"which is the
   sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use"*: the same
   2026-09-25 entry's item 5, `R-ENC-16` listed. **EQUIVALENT by hand; new to
   the maintainer.**

8. **The front-matter clause on vectors** (`swab-08` LOSS; split,
   `EQUIVALENCE_STANDS`). A's Note before §1: *"Normative requirements carry
   stable identifiers like `[R-IDX-03]`, and test vectors cite those
   identifiers rather than prose positions."* B folded the Note into §1 on
   2026-09-23, the entry naming §2.2 and §24 as the surviving statements for
   this clause. Hand-check: B's §2.2 says *"Identifiers are stable: they are
   never renumbered or reused"*, and B's §24 `[R-VEC-02]` requires a vector's
   manifest to record *"the §21 register row it exercises together with that
   row's governing requirement identifier. A row label is never renumbered and
   never reused … exactly as §2.2 makes the identifier permanent, and
   recording both ties the vector to the rule as well as to the row"*, A's
   words. Calibration 2 graded the fold and its refuter stood on the same
   closure. **EQUIVALENT by hand; new to the maintainer.**

No ADDITION was graded by any lane. The A-into-B sweep ran the harder
direction first, treating every B sentence without a verbatim match in A as
a candidate, and closed each on text A states elsewhere; the B-into-A sweep
reconciled its Note census (57 against 52) to zero unresolved; both sweeps,
the writer comparator and the adversary tried the generation-relative
*addressed tile* definition (§3.1) and closed it on §11.1's Rationale,
`[R-CNT-17]` and §20.3 step 4, byte-identical in both editions, as
calibration 2 and round 1 had.

**Round 1's items 1 and 2** (`[R-CNF-03]`'s experimental-range gloss and
`[R-CNF-02]`'s closed enumeration) were graded EQUIVALENT this time by the
reader and verifier comparators and by every pass, with the surviving
statements named (§21.6 and row F36; §6.3, §6.2 and §20.3 step 4).

## The spruce-up stretch, §9 through Appendix H

This round was run to grade the spruce-up alone. Over §9 through §24 and
Appendices A, D, G and H the instruments reported:

- the three comparators: two relocations the log records as restatement
  removals, EQUIVALENT by every pass (§6.3's rewriter sentence standing at
  §20.5 `[R-WRT-06]`; §7.1's quarantine paragraph standing at §7.3), and the
  writer comparator's diff of §20.3, §20.4, §20.5, §21.4's table, Appendix A
  and Appendix G finding them byte-identical or identical in substance;
- the A-into-B sweep: section diffs of 16 to 141 lines for §10 through §21,
  every hunk read, no finding; the B-into-A sweep: "almost every non-equal
  diff opcode across all 24 sections and 8 appendices is a punctuation-register
  change", no finding;
- the adversary: 40 section-level side-by-side passes over the charter's hot
  zones (§9.2, §9.3, §9.7, §12, §15, §18.2, §19, §20.3–§20.5, §21.1, §21.5,
  §21.6, §21.9, §22, §23, §24, Appendices A, B, G, H), *"most returning only
  em-dash/colon/comma rewording with zero semantic difference"*; keyword
  counts (*save where*, *unless*, *except*, *only*, *whatever*, *in any
  commit*, *any rewrite*) identical, *notwithstanding* 2 against 0 traced to
  the §15.3 swap the log records; modal-verb totals higher in B by the
  sentence splits, spot-checked to identical content;
- the quiz: eleven of thirty questions on this stretch (§9.2, §11.2, §14.2,
  §15.1, §15.4, §17.2, §19.2, §19.4, §20.3, §20.5, §21.3), every one answered
  the same from both editions;
- the walks: every probe answered the same on substance, the writer walks
  through §20.3's steps, §20.4's table and §20.5 in both editions.

Nothing was graded LOSS or ADDITION in this stretch by any lane. The word
restored before launch (§9.7's *"the [16, F − 64) bound above"*) was
mentioned by no lane.

## Shared indeterminacies of A, for the ledger

The six blind walks reported ten findings about their own editions. Every one
quotes text that stands identically in both editions, checked here and by
the comparators, and all three passes graded each EQUIVALENT with the
location in both editions named. They are observations about A, not fidelity
findings.

- **No outcome class for a reader or verifier lacking an assigned core codec
  or filter** (`readera-01`, `readerb-01`, `verifiera-01`, `verifierb-01`;
  `cmp-reader-01` AMBIGUITY, `cmp-verifier-04`; §2.3 `[R-CNF-03]`,
  `[R-CNF-11]`, §17.4 `[R-COD-11]`, §21.6, §21.9 `[R-ERR-04]`). The same
  finding as both calibrations' and round 1's reader walks, now from the
  verifier walks too: `[R-CNF-11]`'s unqualified "cannot execute a codec or
  filter" ground against `[R-CNF-03]`'s class-level bar.
- **A fixed-declaration change on a layer with no padding position is
  unwitnessed** (`writera-01`, `writerb-02`, `verifierb-02`; `cmp-writer-01`;
  §20.3 step 4, §21.4 T4, §11.3, §21.7). Round 1's T4 group again, this time
  derived the same way by both writers; identical text.
- **A creator that decodes an input file and re-emits it writes flags = 0**
  (`writerb-01`; `cmp-writer-02`; §20.1 *"As a creator it undertakes nothing
  toward its input, whatever it read"*). Identical text; the creator and
  updater tiers decide it.
- **§15.1's region-layout line is the document's one unlabelled blockquote**
  (`writerb-03`; `cmp-writer-03`). Byte-identical in both editions, the only
  such block in each; a note on presentation for the read-through.
- **Probe R4 names the tile-index entry's fields extent_offset and
  extent_length** where §15.1 names them *offset* and *length*
  (`readera-02`): a note for the probes, not for either edition.
- **Verifier A's V2 answer records a reserved-range MU = 1 record against
  F35 and F36 both** (`cmp-verifier-01` REPORTER_ERROR, unanimous); both
  editions' §21.1 record it against the narrower row F35 alone, in a
  sentence byte-identical in both. A walker error on shared text.

## The instruments, one by one

- **The word-diff preflight**, the check the spruce-up owed before a round:
  for each of the twenty-one commits from `95b5a30` to `7a2046e`, the diff's
  removed and added lines tokenised as `propose.py` does and the Counter
  difference read word by word ([word-diff.md](word-diff.md)). Every word
  lost or gained is a connective, an inflection, a capital at a sentence
  split, a recorded swap, the `[R-ERR-04]` pointer's words or the dropped
  duplicate "(§8.1)", save one: the §9 first pass, done before the passes
  carried a word-level diff, had lost "above" from §9.7's bound sentence.
  Restored as `7b5b9a7` with its log entry before the launch. Three wordings
  the entries had not named are in the approved proposals' after-texts
  ("Field values:" → "The field's values:" in §11.4 and §12.2; "all reserved
  values" → "every reserved value" in §11.4; "forms" → "form" in §14.2's
  Example) and were left.
- **`tarn_inventory.py`** was not part of the run; it passed before the
  launch with the 121 listed IDs and the carried soft items (the eight §3.1
  term rewordings, Appendix B's row, HEADINGS 130 against 129, SHOULD 46
  against 47).
- **The quiz, cross-answered**: 30 questions, two authors with no findings,
  eleven questions on the spruce-up stretch. Slate A agreed 15 of 15 after
  the loose match, so no quiz comparator ran for it; slate B agreed 14 of 15,
  the one divergence (quizb-q3: *"conforming; channel a; 16000000"* against
  *"conforming; a; 16000000"*) graded EQUIVALENT by the quiz comparator on
  §12.1's table, §14.2's formula, `[R-COD-07]` and row L44, byte-identical in
  both editions. Hand-check agrees. Nothing reached triage from the quiz.
- **The six blind walks**: 10 to 15 minutes each, every probe answered the
  same from both editions on substance; ten own-edition findings, all shared
  text (above). No walk found a fidelity difference, as in both calibrations
  and round 1.
- **The three comparators**: reader 4 findings (1 AMBIGUITY, 3 EQUIVALENT),
  writer 6 (all EQUIVALENT), verifier 4 (1 REPORTER_ERROR, 3 EQUIVALENT); no
  LOSS from any comparator this round. Each read every section either walk
  cited side by side in both editions and diffed the long ones whole; each
  closed the same candidates the edit log records (the §2.3 grounds list at
  §21.6; the §7.1 paragraph at §7.3; the §6.3 rewriter sentence at §20.5;
  `[R-CNF-02]`'s cases at §6.3, §6.2 and §20.3 step 4).
- **The two sweeps**: A into B, 8 findings, all LOSS, all Notes and
  orientation prose in the front matter and §1–§4 (items 2 through 8 above
  and the bridge), with a section-by-section diff of all 24 sections and the
  appendices and a labelled-block census by fingerprint (85 against 80 by
  its regex, every one-sided fingerprint re-checked); B into A, 3 findings
  (1 LOSS self-flagged byte-level, the bridge; 1 OBSERVATION; 1 AMBIGUITY),
  with a census of Notes 57 against 52, Examples 15 against 15 and
  Rationales 13 against 13, the Note gap reconciled to zero (two reworded
  fingerprints, three relocations found by reading). Both sweeps paired the
  blocks as round 1's debt asked.
- **The diff-adversary**: 3 findings (round 1's items 4, 5 and 3, all LOSS);
  six constructions carried to bytes or verdicts and every one closed on
  text byte-identical in both editions (§20.4's MU = 0 / PE = 1 row; the
  grown extent against `[R-CNT-17]` and §20.3 step 4; the 4-byte
  user-metadata extent; the 92-byte pre-trailer gap against §6.2; the
  experimental-range document encoding against §21.6's row; the
  experimental-range MU = 1 record against `[R-CNT-15]` and `[R-CNF-02]`); a
  heading diff isolating §3.3 as the one unmatched subsection; a reflowed
  paragraph match in both directions (29 and 39 unmatched, every one opened
  and classified).
- **Triage**: 38 findings (three comparators 14, two sweeps 11, the adversary
  3, six walks 10, two authors 0; no quiz item) into 21, 21 and 21 groups;
  coverage CLEAN on all three passes, 38 of 38 ids each; byte-level 0 on all
  three. Unanimous on every group but the six splits: the two unanimous LOSS
  groups are the bridge and the reach Note; the correctness and implementer
  passes graded the other six cuts LOSS where the skeptic graded them
  EQUIVALENT, each pass naming the surviving location; every walk group
  EQUIVALENT on identical text; `cmp-verifier-01` REPORTER_ERROR on all
  three, and `readera-02` REPORTER_ERROR on two as a note on the probe. The
  correctness and skeptic passes read the two editions only; the implementer
  also read the walk and comparator transcripts.
- **Refute**: six equivalence-refuters on the splits, 1 to 4 minutes each,
  every one `EQUIVALENCE_STANDS` in its own vocabulary with `decisive_quotes`
  filled and a control search behind every zero; two loss-refuters on the
  unanimous groups: the bridge's `LOSS_STANDS` (no sentence of B carries the
  bridge; §20.4's table decides the duty), the reach Note's `LOSS_REFUTED`
  (the general test in §2.3, `[R-CNT-24]`'s 48 bytes and §21.2's lead-in
  decide F14, F5 and F15 in B as in A). The §4.7 refuter reported
  `[R-ENC-16]`'s cut citation clause in `new_findings` as outside its group,
  as calibration 2's debt asked. No zero-attacker: the round was not a zero
  in the harness's terms. Every refuter read the two editions only.

## Harness integrity

- 30 agent slots, 30 returned, 0 failed, 0 degenerate, no refusal, no stall,
  every agent at its first attempt. Authors 7 minutes, takers 4–7, walks
  10–15, comparators 6–8 (the adversary 20, the sweeps 16, the quiz
  comparator 2), passes 10–12, refuters 1–4; 65.6 minutes end to end, 869
  tool calls, 4.78 M tokens.
- `rebuild.py` substituted 30 of 30 journal results, none unused, no
  ellipsis character left in the output. `collect-fidelity.py --full`
  printed the matrix, the findings by kind, the three passes' groups and
  the eight verdicts. `copy-fidelity.sh` copied 23 files, every triage
  transcript from the directory its brief named.
- **The degeneracy check**, paid after round 1, ran on every lane's prose
  fields and flagged none (`degenerateLanes` empty); no lane returned a
  placeholder, and no return was rejected by the validator more than the
  runtime's own retries show.
- **The model.** Every agent's meta file says `claude-sonnet-5` and all 1,574
  assistant messages across the 30 transcripts carry `claude-sonnet-5`. The
  pin is the harness constant, `SUBAGENT_MODEL = 'claude-sonnet-5'` (line
  47), with preflight under `--models claude-sonnet-5`; the pre-launch probe
  `wf_4cccf01e-aaa` (one agent, `model: 'claude-sonnet-5'`, no tools) ran on
  it.
- **The launch turn.** The Workflow runtime prepended the launching user turn
  to every agent's prompt as "the only user voice in this task"; this round's
  was the single word "Go", by the handoff's rule after round 1's agents
  received an action-naming message and three acted on it. All 30 agents
  disclosed it and none acted on it; the ACCESS blocks' relayed-request
  paragraph, the second guard, was cited by most as the reason to set it
  aside. The first transcript's user turn reads, after the harness's label,
  exactly "Go".
- **The mechanical boundary scan** (`scratch/cleanroom/pass/boundary-scan.py`,
  over every transcript's tool calls): the six blind-A agents named
  `editions/a/tarn.md` and never the repository's `spec/tarn.md`; the six
  blind-B agents the reverse; no agent named `editions/b`, `editions/c` or
  the stale sibling repository; no agent ran a git command; no agent read a
  file outside its rule but the runtime's own tool-result spill files (seven
  agents, the runtime's mechanism for a long tool result). Directory
  listings were of the agent's own scratch directory or a stat of its one
  file, save `sweep:a-to-b`'s `ls -la` of `out/`, which it disclosed.
- **Two undisclosed writes to `/tmp`**: `sweep:a-to-b` wrote four working
  files (`/tmp/a_216.txt`, `/tmp/b_216.txt`, `/tmp/diff21.txt`,
  `/tmp/diff24.txt`) and read one back; `compare:writer` wrote
  `/tmp/A_203.txt`. The ACCESS rule says a scratch directory is the agent's
  alone and names a shared temporary directory as out of bounds; both wrote
  section extracts of the two editions they were permitted to read, nothing
  else, and no other agent read them. Noted as round 1 noted the undisclosed
  `git log`.
- **Other disclosures.** Every agent disclosed the injected context (the
  project pointer file, the memory index, the git-status block naming the
  spruce-up's commit subjects, the channel the maintainer accepted for this
  round), used as disclosure only; the sweeps and the adversary noted the
  commit subjects name a "spruce-up pass" and said their findings were made
  by diff and reading.
- **Preflight** on `/usr/local/bin/node` v22.19.0: selftest PASS; PASS with
  the run's args under `--models claude-sonnet-5`, 22 calls rendered, 11
  model sites on `claude-sonnet-5`, run again after the word-diff repair;
  `render-prompts.js` 24 briefs, byte-identical before and after the repair;
  the path audit (`scratch/cleanroom/audit-briefs.py`) PASS: six A-agents
  `editions/a/tarn.md` only, six B-agents `tarn-first-draft/spec/tarn.md`
  only, twelve two-edition briefs both, no `editions/b`, no `editions/c`,
  all 24 naming `fidelity-4`, all 24 carrying the validator rule and the
  relayed-request paragraph.

## What this round mandates

1. **Nothing in the harness.** Every debt round 1 raised ran as paid: the
   degeneracy check on every lane, the validator rule, the relayed-request
   paragraph (which, with an inert launch turn, held all 30 agents to their
   role), the sweeps' pair-by-pair census, V2 asking both ranges.
2. **Probe R4 names the entry's fields as §15.1 does** (*offset*, *length*),
   so a walker is not left noting the probe's own words.
3. **The ACCESS rule's scratch-directory clause names `/tmp` as the shared
   directory it means**, two agents having written there undisclosed; a
   wording change, not a new rule.
4. **The grade a round gives a logged Note cut is now measured three times**:
   calibration 2, round 1 and this round each graded cuts of explanatory
   prose LOSS wherever no sentence of B carries them, and each time the
   hand-check and the refuters found the rule standing. The class is the
   round reading decision 3's permission as a finding for the maintainer,
   which is what decision 4 asks; expect it every round over §1–§4 until the
   maintainer's read-through settles that stretch.

## What this round says about B

For ADR-0133 decision 5's test, no LOSS survives the hand-check and no
ADDITION was found. The spruce-up series over §9 through the appendices,
82 reworded rule paragraphs and four splits under the mechanical contract
and the word-level diff, drew no finding from any instrument: on every rule
read there, B at `7b5b9a7` says what A says. The eight graded losses are the
maintainer's, listed above with both texts; five were ruled on 2026-10-08 and
three are new, all in the front matter and §1–§4, which is where the rewrite
has cut the most explanatory prose and where the read-through has not yet
passed.
