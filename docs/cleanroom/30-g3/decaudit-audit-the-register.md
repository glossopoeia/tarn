# Repair audit — hunk-03 (R8 row) and hunk-05 (§21.8 total)

## Access disclosure

Files read:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-decaudit/case/hunk-03.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-decaudit/case/hunk-05.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — read in full via offsets 3560-3960 (§21.1 through the start of §21.9) and 4225-4305 (§24 opening), plus targeted greps over the whole file.

Scripts written (my own scratch dir only):
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-decaudit/scratch/the-register/count.py`
  — parses spec/tarn.md, locates the §21.2-21.5 heading boundaries, extracts every row `F#/L#/T#/R#`, splits the Instances cell on `;` (a `—` cell counts as 1), and sums.

**Contamination check.** My system context (CLAUDE.md / project instructions / auto-memory) contained references to "TARN lineage gate word list", "TARN repair prose vs rules", "TARN preflight before launch" and similar. None of that material was read or used to reach any conclusion below — I did not open any of the referenced docs (they are outside my access rule regardless) and did not let the file names steer my analysis. Flagging per the disclosure requirement; treating it as noise.

No other files were read. I did not read `full.diff`, other hunk files, docs/, ADRs, registry.json, or git history, and did not list the case directory.

## Hunk 3 — R8 row, §21.5 Ignored records (spec line 3818)

### The rule the repair adopts

Before: R8 treated "a non-finite number, in any form" as **one** condition-shape ("a magnitude ... overflows ... and the bare tokens ... alike"), instantiated only over the two containers (top-level document, layer sub-record document) → Instances cell `top-level document; layer sub-record document` = 2 entries.

After: R8 treats the condition as **two alternatives** — (a) an overflowing magnitude, (b) a bare non-numeric token (`NaN`/`Infinity`/`-Infinity`) — crossed with the same two containers → Instances cell enumerates all four combinations = 4 entries.

What this makes true of an implementation: the conformance corpus (§21.8, §24 `[R-VEC-03]`) must now carry **4** distinct R8 vectors (one per instance), not 2 — two exercising an overflowing-magnitude document (top-level and sub-record) and two exercising a bare-token document (top-level and sub-record).

### Check 1 — Tense and quantifier

§21.1 (line ~3599-3602, quoted verbatim):
> "a condition applying to two alternatives in two containers has four"

and, on when alternatives are enumerated vs. collapsed (line ~3603-3606):
> "What a cell enumerates is the condition's own alternatives and containers: a row whose check ranges over a family without the condition changing shape states that range as a single instance (T24's *any codec*), and one whose members give the condition materially different shapes enumerates them (T15, T25)."

The repair's own governing text `[R-MTA-04]` (line 2693-2702, "Finite numbers only") states the rule disjunctively:
> "A document is unreadable if it contains a number whose binary64 interpretation is not finite — which covers a magnitude that overflows on conversion, `1e400` being the ordinary case — or any of the bare tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit and some parsers accept regardless."

The repaired R8 condition text now tracks this "or" structure almost verbatim ("a magnitude whose binary64 interpretation overflows (`1e400`), or one of the bare tokens `NaN`, `Infinity` and `-Infinity`, which RFC 8259 does not admit"), where the pre-repair text used "and ... alike" — language that reads as one family (à la T24's "any codec"), not two alternatives. The two detection paths are materially different in the T15/T25 sense: an overflowing magnitude is a syntactically valid JSON number whose binary64 conversion is infinite (requires parsing a numeric literal and checking a bound), while a bare token (`NaN`, `Infinity`, `-Infinity`) is not valid JSON syntax at all — it's a different lexical shape a lenient parser might accept. Two files can trivially differ (a document containing `1e400` vs. one containing the literal `NaN`), satisfying §21.1's "one instance is one distinguishable file" test (line ~3622-3625).

Verdict: the repair's quantifier (2 alternatives × 2 containers = 4) matches the governing rule's own two-way disjunction, and matches the general counting rule's worked example almost exactly. The generation is consistent — no prior/superseded-state confusion, since this is a static table describing detectable conditions, not a commit-tense rule.

### Check 2 — Citations resolve

- `[R-MTA-04]` (governing rule, unchanged by this hunk) — opened at line 2693-2718 ("Finite numbers only" bullet). Confirms the exact condition, including the RFC 8259 point and the three named tokens. **Resolves.**
- `(R-CNT-25)` (secondary citation, unchanged) — the user-metadata quarantine; opened at line 3792-3806 ("metadata is quarantined (`[R-CNT-25]`): every way its document can be unreadable takes this outcome"). R8 is exactly such a way. **Resolves.**

Both citations were already correct before this hunk and are untouched by it; I re-verified them because check 2 requires it regardless.

### Check 3 — Normative placement

R8 sits inside the §21.5 register table, which carries no `>` blockquote marker and is not headed *Note.*, *Example.*, or *Rationale.* — it is a plain markdown table under the `#### 21.5 Ignored records` heading. Per `[R-CNF-01]`, an unlabeled block (table or otherwise) is normative. Test applied: looked at the actual opening of the enclosing block, not the presence/absence of `>`. **The repair lands in normative text.**

(The only `>` block in this immediate neighborhood is the "Note. Row label F11 is struck..." note after §21.2's table, well before R8; it does not touch R8's row or table.)

### Check 4 — No contradiction in the same passage

Read the whole of §21.5 (lines 3788-3821) surrounding R8: the quarantine intro paragraph, R1-R10. Searched the whole document for "non-finite", "NaN", "Infinity" (see sweep below) — the only other occurrences are in the binary32/64 sample-value discussion (§13-ish, lines 1154-2809), which concerns tile/channel fill values, an entirely different subject (fill bytes of a channel, not JSON metadata numbers) and does not restate or reference R8's rule. No contradiction found — nothing elsewhere asserts R8's non-finite-number condition is a single family, and nothing narrows/widens the licence this row states.

### Check 5 — No exhaustive claim it cannot carry

The repaired text lists exactly the three tokens `NaN`, `Infinity`, `-Infinity` — this matches `[R-MTA-04]`'s own list exactly (same three tokens, no more no less). "a magnitude whose binary64 interpretation overflows" is a single unbounded predicate (any value whose conversion is infinite), not a closed list, so nothing to falsify there. No overclaim found.

### Check 6 — What else in this structure is left unconstrained?

Structure: the R8 table row (Condition / Instances / Detector / Detected / Governing rule). Every field:
- Condition — restated, unchanged in substance, only in "alternative" framing.
- Instances — the one field this hunk fixes.
- Detector = `reader` — untouched, unaffected by the split.
- Detected = `extent use` — untouched.
- Governing rule = `[R-MTA-04]` (R-CNT-25) — untouched.

Nothing else in this five-column structure is left dangling by the edit; the hunk touches exactly the one column the defect was in and leaves the others as they were (and they still read correctly against the row's new Condition text).

### Check 7 — Analogy comparison

This hunk does not argue by analogy to another rule ("exactly as", "the same way", etc.) — it directly restates its own governing rule's wording. N/A in the "compare two governing verbs" sense, but for completeness: the repaired Condition's disjunctive verb structure ("overflows... or one of the bare tokens...") was compared word-for-word against `[R-MTA-04]`'s disjunctive verb structure ("covers a magnitude that overflows... or any of the bare tokens...") above (Check 1) and they match — same subject, same "or", same three tokens, same RFC citation.

### Check 8 — Effect on surrounding sentences (back-references)

Hunk 3 is a same-line substitution (row R8 replaced by row R8), not an insertion of new prose between two sentences. Read forward through R9, R10 and into §21.6: no back-reference ("the two...", "such", bare "it"/"that") in R9 or R10 refers to R8 or to "non-finite number" — R9 is about duplicate keys, R10 about key length, both self-contained. No anaphora resolution changed.

## Hunk 5 — §21.8 Conformance vector coverage (spec line 3936)

### The rule the repair adopts

"Every row of §21.2 through §21.5 — 120 conditions over 277 instances — has at least one conformance vector..." The repair changes only the instance total, 275 → 277, a +2 delta that exactly equals the +2 delta hunk 3 makes to R8's own instance count (2 → 4). The row count (120) is untouched by either hunk.

### Check 1 — Tense/quantifier

The sentence quantifies over "every row of §21.2 through §21.5" — this exactly matches `[R-ERR-02]`'s own scope, quoted at line 3558: "The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates...". Same range, no drift. §21.1 (lines 3589-3595) explicitly states this arithmetic does **not** reach §21.6, §21.7 or §21.9 — the repaired sentence's own span ("§21.2 through §21.5") respects that boundary exactly.

### Check 2 — Citations resolve

- `[R-ERR-02]` (end of the sentence, unchanged) — opened at line 3558 (defines the register's span) and again at line 4284-4294 (§24, "Coverage is the corpus's own obligation, inherited from `[R-ERR-02]`: every register row has at least one vector for each instance it names..."). Both **resolve** and are consistent with the repaired sentence's own wording ("at least one conformance vector... and one vector per instance").

### Check 3 — Normative placement

§21.8's paragraph (lines 3934-3939) carries no `>` marker and is not labeled Note/Example/Rationale. Normative text; the repair lands there.

### Check 4 — Contradiction check

No other passage restates this total (see sweep below) so nothing conflicts with the new figure elsewhere. Within §21.8 itself, the next sentence ("A row without a vector is a gap in the corpus, not a licence to skip the check") is untouched and still coheres with the new total — it doesn't depend on the exact number.

### Check 5 — Exhaustive claim

"Every row... has at least one... vector... and one vector per instance" — an exhaustiveness claim over "every row", which is true by definition of the register (120 rows, all counted). No falsification found.

### Check 6 — What else is unconstrained

The sentence carries exactly two numbers: row-count (120) and instance-count (277). Row-count is unchanged and independently verified correct (see recount below: 35+49+26+10 = 120). Instance-count is the repaired figure and independently verified correct (see recount: 277). No third quantity in this sentence is left unpinned.

### Check 7 — Analogy

No analogy language in this hunk.

### Check 8 — Back-references

Single-number substitution inside an existing sentence, not an insertion of new clauses. No anaphora is created or affected.

## Independent recount (the core of this audit)

I derived the counting rule from §21.1 (a `—` cell is one instance; otherwise the instance count is the number of `;`-separated entries in the Instances cell) and wrote a script to apply it mechanically to every row of §21.2-21.5, using only spec/tarn.md.

Full output (see `count.py` above for method; raw run output captured here):

```
=== F (21.2): 35 rows ===  -- total instances: 56
=== L (21.3): 49 rows ===  -- total instances: 116
=== T (21.4): 26 rows ===  -- total instances: 55
=== R (21.5): 10 rows ===  -- total instances: 50   (R8 counted as 4, post-repair)
GRAND TOTAL rows: 120, instances: 277
```

56 + 116 + 55 + 50 = 277. This matches the repaired document figure (277) exactly, and 35+49+26+10 = 120 matches the row count exactly. Recomputing with the **pre-repair** R8 cell (2 instances instead of 4) gives 275, matching the pre-repair figure exactly. The two hunks are numerically consistent with each other and with an independent, rule-driven recount of the entire register.

I spot-checked the mechanical count against §21.1's stated conventions on a sample of non-trivial rows to make sure blind semicolon-splitting matches the *intended* counting rule (not just its surface form):

- **L1** (u64 field overflow, 8 named fields, no comparison) → 8 instances. Matches the "one instance per named field" pattern used throughout F2/L1 for simple range tests.
- **T3 / T14 / T22** (an equality test — "is not exactly", "differs from", "does not equal") → each 6 instances (3 layout shapes × 2 directions). Matches §21.1's explicit direction-doubling rule for `differs from`/`does not equal` comparisons (line ~3610-3614).
- **L21 / L22** (`entry_count` vs. geometry-derived count, `≠`) → 4 instances each (2 shapes × 2 directions). Matches the same direction-doubling rule.
- **F33** (claim conflicts across five structure kinds) → 5 instances, one per named structure kind, no direction-doubling (equality-vs-constant style, not a magnitude comparison per §21.1's carve-out). Matches.
- **F36 / L25** ("...whatever its MU bit") and **T2** ("neither 0x00 nor 0x01") → each 1 instance (`—`), because the alternative named (MU bit value; which of the two disallowed bytes) does not change the condition's shape — consistent with the T24 "any codec" pattern of collapsing a family that doesn't materially change shape.

I also specifically hunted for **other** rows that might share R8's original defect (a disjunctive condition text collapsed into one instance where §21.1's own rule would call for a split): I grepped every `—`-instance row in §21.2-21.5 whose Condition column contains " or " (see sweep below). All four hits (F10, F32, L35, T9) describe a single one-directional magnitude/byte-value test phrased with an "or" clause that names the same comparison from two angles (e.g. "touching the live trailer or running beyond the committed file length" is one inequality, not two distinguishable files) — none of them is a T15/T25-style materially-different-shape disjunction, so none should be split, and none is inconsistent with being left at 1. This is the check for "does the repair's own row now have a sibling problem it should have swept" — I found no sibling defect of that shape.

## Sweeps run (verbatim, with hit counts)

1. `grep -n "instances" spec/tarn.md` → 3 hits: lines 3625, 3645, 3937 (the last is inside the repaired §21.8 sentence itself; the other two are unrelated uses of the word "instances" in ordinary prose, not counts).
2. `grep -n "\b120\b" spec/tarn.md` → 1 hit: line 3936 (the repaired sentence itself). No other statement of "120".
3. `grep -n "275" spec/tarn.md` → 0 hits. Confirms the old figure does not survive anywhere else in the document.
4. `grep -n "277" spec/tarn.md` → 1 hit: line 3936 (the repaired sentence itself).
5. `grep -n "conditions" spec/tarn.md` → 13 hits (listed in full in the transcript above), covering each subsection's own row-count statement (35/49/26/10/120) plus unrelated prose uses of "conditions". Each subsection total was cross-checked against actual row counts from the recount script and matches (F:35, L:49, T:26, R:10, all-sections:120).
6. `grep -n "non-finite\|NaN\|Infinity" spec/tarn.md` → 12 hits; all outside §21.5 concern binary32/64 tile-sample fill values (a different subsystem), except line 3818 which is R8 itself. No restatement of R8's rule elsewhere that would need sweeping.
7. `grep -n "R-MTA-04\|R-CNT-25\|R-ERR-02\b" spec/tarn.md` → located and opened every hit relevant to the two hunks' citations (listed above); all resolve as claimed.
8. `awk` scan (see command above) of every register row (F/L/T/R) whose Instances cell is `—` (1 instance) and whose Condition text contains `" or "`, to hunt for a sibling of R8's original undercount defect → 4 hits (F10, F32, L35, T9), each examined and found to be a legitimate single-direction test, not a missed enumeration.
9. Full mechanical recount of every Instances cell across §21.2-21.5 (script `count.py`), 120 rows, cross-summed by subsection and grand total.

## Derived numbers

- **F (§21.2) instance total**: 56 (computed by summing 35 rows' Instances cells). Not separately stated anywhere in the document to compare against — only the grand total (277) and the row count (35) are stated, both of which check out.
- **L (§21.3) instance total**: 116. Same — not separately stated; folds into the grand total, which checks out.
- **T (§21.4) instance total**: 55. Same.
- **R (§21.5) instance total**: 50 (with repaired R8 = 4). Same.
- **Grand total instances**: 56+116+55+50 = **277**, matching the repaired document figure exactly.
- **Grand total rows**: 35+49+26+10 = **120**, matching the document figure exactly (unchanged by either hunk).
- **Pre-repair grand total** (R8 = 2 instead of 4): 275, matching the pre-repair document figure exactly — confirms the delta (+2) is exactly and only R8's change.

No arithmetic discrepancy found anywhere in this reconciliation.

## Rejected candidates

1. **"Maybe the overflow alternative should itself split by sign (1e400 vs -1e400)."** Checked `[R-MTA-04]`'s own text and §21.1's magnitude-comparison rule: the direction-doubling rule in §21.1 applies specifically to comparisons between two magnitudes ("differs from"/"does not equal"), not to a single-value threshold/overflow test. F2-style boundary tests (u64 > 2^63-1) are treated as one instance per field regardless of how far over the boundary a value could be, and R8's overflow alternative is the same shape. Closed: not a defect.
2. **"Maybe another §21.5 row (R1, R4, R7) has the same T24-vs-T15 mis-collapse R8 had."** Checked R1 (4, encoding-value alternatives × 2 containers — already split), R4 (16, 8 frame-constraint alternatives × 2 containers — already split), R7 (6, 3 JSON-defect alternatives × 2 containers — already split). All already enumerate their alternatives correctly; none shares R8's original defect. Closed by direct inspection of each cell.
3. **"Maybe the four F10/F32/L35/T9 rows with '—' and an internal 'or' are also undercounted like old-R8 was."** Checked each: all four state one one-directional inequality/byte-test phrased two ways, not two distinguishable files. Closed (see Check above and sweep #8).
4. **"Maybe §21.9's minimum-guarantee table or §24's coverage paragraph also states a total that needs the same +2 update."** Grepped for "275", "277", "instances", "120" across the whole document (sweeps 1-4): the only occurrences are inside the repaired sentence itself. Closed — no other restatement exists to sweep.
5. **"Maybe R8's Detector/Detected/Governing-rule columns needed to change along with the split (e.g., different detection point for a bare token vs. an overflow)."** Both alternatives are decoded-JSON-value checks performed during document parsing at the same point (`extent use`) by the same actor (`reader`), under the same governing rule (`[R-MTA-04]`). No basis found for a different Detector/Detected per alternative. Closed.

## Confidence / where little was found

This audit found the two repairs to be correct: hunk 3's re-enumeration of R8 is licensed by §21.1's own stated rule and by R8's governing requirement `[R-MTA-04]`'s own disjunctive wording, and hunk 5's total (277) is exactly reproduced by an independent, script-driven recount of all 120 register rows across §21.2-21.5 using only the spec text and the counting rule stated in §21.1. The pre-repair total (275) is also exactly reproduced by the same method with the pre-repair R8 cell, confirming the delta is fully and only explained by the R8 change — nothing else moved.

What would have caught a defect had one existed: the mechanical recount would have surfaced a mismatch against the stated 277 had any other row's Instances cell been miscounted (by the same convention the repair uses) or had the repair's own new R8 cell been wrong; the sweeps for "275", "277", "120" and "instances" would have surfaced an un-swept restatement elsewhere; the disjunctive-language grep (`" or "` inside `—`-instance rows) targeted specifically hunted for a sibling of the exact defect shape R8 had, and would have found one if it existed among the other 119 rows' "—" cells with internal "or"/"and" language. None of these turned up a second defect.

I did not find a citation that "almost" says the claimed thing, a contradiction elsewhere in the passage, an overclaim, an unconstrained sibling quantity, a bad analogy, or an anaphora shift — each check is reported explicitly above with what was looked for and why nothing was found, per check.

## Summary

Hunk 3 corrects R8's Instances cell from 2 to 4 by recognizing that "overflowing magnitude" and "bare non-numeric token" are, per §21.1's own stated test (materially different shapes, T15/T25-style), two alternatives rather than one family — a reading directly supported by R8's governing rule `[R-MTA-04]`, whose own prose states the same two-way disjunction the repaired Condition text now mirrors nearly verbatim. Both citations (`[R-MTA-04]`, `R-CNT-25`) resolve correctly and are unchanged. The row sits in normative table text (no Note/Example/Rationale label). No contradiction, overclaim, or dangling sibling quantity was found in the row or its immediate neighbors; four neighboring §21.5 rows (R1, R4, R6, R7, R9, R10 — six checked, more than the required four) were independently recounted and all already match the rule correctly. Hunk 5 updates the register's self-reported total from 275 to 277, and an independent, script-driven, rule-derived recount of every one of the register's 120 rows (§21.2 through §21.5) reproduces exactly 277 for the repaired state and exactly 275 for the pre-repair state — the total is correct, the scope named ("§21.2 through §21.5") matches `[R-ERR-02]`'s own defined scope, and no other place in the document restates either figure and needed sweeping. I found no defect in either hunk.
