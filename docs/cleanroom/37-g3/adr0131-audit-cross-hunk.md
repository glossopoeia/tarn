# Cross-hunk consistency audit — round 37

## Disclosure

Files read:
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (via Read, in chunks: lines 95-434, 414-458 [3.2/3.3], 1007-1101 [7.2/7.3], 1276-1370 [9.1-9.3], 1507-1566 [9.7], 3126-3480 [20.1-20.3], 3475-3674 [20.4-20.5], 4016-4080 [21.6], 4354-4392 [23.1], 4708-4960 [Appendix G/H], plus targeted `sed`/`grep`/`python3` reads of lines 633-697 [5.1 figure] and 3407-3474 [20.3 figure example]).
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/case/hunk-01.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/case/hunk-02.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/case/hunk-03.diff

I did **not** read full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git history/log/diff, or the web. I did not list the case/ directory beyond the one `ls` needed to confirm the path the brief gave was correct (it was — case/ contains hunk-01..03.diff and full.diff as stated).

Commands run: `ls` on the case/, r37-audit/, and scratch/ directories to verify paths matched the brief (they did — no path substitution to report); `grep -n "^#\{1,4\} "` to build a section/line map; several `grep -n` searches for phrases and citation numbers; three `python3` scripts (no data files, only tarn.md) to (a) print exact character columns of the two figure rows in the §20.3 Example so bracket alignment could be computed rather than eyeballed, (b) run whitespace-normalized phrase searches to defeat the hard-wrap, with control searches proving each zero. No file was written to any directory other than this one and the scratch dir noted below (I did not end up needing a scratch script beyond the two inline python3 calls, which read only tarn.md and wrote no files).

**Contamination disclosure.** Before this task began, my context already contained: a CLAUDE.md pointer to AGENTS.md (not read, per the access rule), a user MEMORY.md index with ~18 one-line entries with titles like "TARN lineage gate word list — the canonical file is missing", "TARN repair prose vs rules — where this project's repair defects actually live", "TARN closed-list exceptions compose", etc., and a git-status block naming five recent commit subjects including "ADR-0131: round 36's repairs — three clauses, after a zero read on a weaker instrument" and "Cleanroom round 36: ... eight findings, eight defects, the refute phase stood on the zero; whether a zero from this instrument meets G3 is the maintainer's". This is exactly the kind of pre-loaded index-of-notes/commit-subject material the brief warns about. I did not open any of the linked memory files, did not read AGENTS.md, and did not let the commit subjects or memory titles steer which passages I searched or which verdict I reached — my findings below are derived from the hunk diffs and the spec text search-and-compute record shown here, not from any of that material. Flagging its presence per the mandatory-disclosure instruction.

No path substitution: the case/ directory was exactly where the brief said, containing exactly hunk-01.diff, hunk-02.diff, hunk-03.diff, full.diff (untouched).

## The three hunks, restated

- **Hunk 1** — §3.3's Note. Strikes "verifiers," from the subject list "verifiers, appenders, and rewriters carrying a layer forward operate on files whose layers they cannot decode," and moves a comma: "appenders, and rewriters carrying a layer forward, operate on files whose layers they cannot decode."
- **Hunk 2** — §20.3's "three shapes" Example, figure (b). Closes an annotation bracket: `└ every entry, re-emitted` (opened, never closed, running to end of line) becomes `└────────┘ every entry, re-emitted` (closed, then the caption follows outside the bracket).
- **Hunk 3** — §20.4's preservation table, MU=0/PE=0 row. "so an updater MAY drop the record in any commit..." becomes "so an appender MAY drop the record in any commit...", leaving "...and a rewriter MAY drop it in any rewrite" (already present, untouched) as the rewriter's own licence.

## Grouping (by rule, not by section)

**Group A — who operates without decoding (hunk 1).** §3.3's Note; §2.3's verifier verdicts (`[R-CNF-11]`); §9.7; §19.3 (`[R-RDR-03]`); §20.1; `[R-WRT-03]`.

**Group B — who may drop what, in what operation, and who reports (hunk 3, plus hunk 2's figure sits downstream of the same re-emission machinery).** §7.2's Note; §9.1/§9.2 (`[R-LIF-01]`, `[R-LIF-02]`); §20.1; §20.3 steps 2 and 4, shape (c); §20.4 whole; §20.5; §21.6; §23.1; Appendix G item 8; Appendix H's updater/rewriter entries.

**Group C — the re-emission figure (hunk 2) against its own conventions and against step 4's prose.** §5.1's figure; §20.3's figure (a) and the "old" bracket in figure (b); §20.3 step 4.

## Group A: hunk 1

**Rule the repair adopts:** the container/array independence Note should name exactly the actors for whom that independence lets them complete their function without decoding — and a certifying verifier is not one of them.

**Check 2 (citations).** No requirement ID or section number is introduced by this hunk; the unchanged trailing clause cites "§7 and §20" (context line, not part of the diff) — accurate: §7 is the directory/records section, §20 is writing/updating, both of which the Note's independence claim is said to be "load-bearing for."

**Check 3 (label, not marker).** The hunk lands inside a blockquote headed `> **Note.**` — labeled, hence non-normative under `[R-CNF-01]`. Verified by reading the block's own opening words, not by the ">" alone. The actual normative support for "appenders/rewriters need not decode" lives elsewhere and does not depend on this Note:
- §19.3 (`[R-RDR-03]`): layer access validation is "decidable from the resident directory and F: layer access performs no fetch" — no decode, ever, for the structural checks an appender owes.
- `[R-WRT-03]`: an appender's verification depth is the trailer, the full directory, §19.3's layer validation for touched layers, and the §19.4 index chain — never decoded sample content.
- §9.7: **"A verifier that certifies decodes every stored tile"** — the passage that grounds the whole repair. Confirmed present (not a mis-scan): `grep -n "certifies decodes every stored tile"` → line 1533, one hit.
So the Note's rule was always secondary/explanatory; removing "verifiers" does not strand a normative claim that depended solely on the Note.

**Check 4 (contradiction in the passage).** The Note's own trailing clause — unchanged by the hunk — says the independence "is load-bearing for the **updater** rules of §7 and §20." Before the repair, the subject list named three actors (verifiers, appenders, rewriters) but the conclusion named only "updater rules." Verifiers are not updaters (`[R-CNF-06]`: "Its tiers, the appender and the rewriter, are §20.1's"). So the pre-repair Note was already internally mismatched: three subjects, but a conclusion scoped to only two of them (the updater tiers). The repair fixes this: now exactly two actors (appenders, rewriters), both updater tiers, matching "updater rules" precisely. This is evidence *for* the repair, not against it.

**Check 4, continued — a live risk.** §2.3 itself states a verifier can reach *cannot establish* "when it cannot execute a codec or filter (`[R-COD-11]`)" — i.e. a verifier *can* be handed, and can partially process, a file whose layer it cannot decode; it just cannot *certify* it. The Note's repaired text doesn't contradict this (it's about which actors' designated function *completes* without decode, and a verifier's — certification — does not), but a careless reading could think the repair claims verifiers can never touch such a file at all. Re-reading the sentence, it doesn't claim that; it says which actors "operate on" (successfully carry out their operation on) such files. No contradiction found, but flagging the boundary since it's the nearest miss.

**Check 8 / list-of-two hazard (the main finding).** Comparing the two texts letter for letter:

- Before: `so verifiers, appenders, and rewriters carrying a layer forward operate on files...`
- After: `so appenders, and rewriters carrying a layer forward, operate on files...`

Before the repair, "carrying a layer forward" sits immediately before "operate" with **no comma**, reading as a restrictive participial phrase on the nearest noun, "rewriters" only — correctly excluding a rewriter that *re-creates* a layer (which does decode, per §20.1: "carrying structures forward, re-creating some, or dropping some").

After the repair, a comma was inserted after "forward" (and the pre-existing comma after "appenders" — originally an Oxford-comma artifact of the three-item list — was kept), giving `appenders, and rewriters carrying a layer forward, operate...`. The phrase "carrying a layer forward" is now boxed by commas on both sides, which is the shape a non-restrictive modifier over the *whole* preceding subject takes in English, not only over "rewriters." A reader can now parse this as "appenders [that are] carrying a layer forward, and rewriters [that are] carrying a layer forward, operate..." — i.e. that the "carrying forward" qualifier applies to *both* appenders and rewriters, not just to rewriters.

Does that misreading matter substantively? I checked: an appender that is *not* simply "carrying a layer forward" (e.g. one adding new tiles to a layer, superseding tiles, or growing an extent) still never needs to decode anything to do it (§19.3, `[R-WRT-03]`) — so the *joint* reading would be true but narrower than intended, silently converting an unconditional claim about appenders into one that reads as conditional on the appender leaving the layer untouched. That is a real narrowing of what the sentence appears to assert, introduced by the punctuation move, even though every actual conforming appender still satisfies it. This is a **repair-introduced ambiguity**, not present in the same shape before (the pre-repair three-item list had the identical no-comma-before-"carrying" construction that cleanly attached the modifier to "rewriters" alone).

**Verdict:** NEW_AMBIGUITY. Not byte-level — the passage is inside a `> **Note.**` block, carries no normative force under `[R-CNF-01]`, and no conforming byte sequence turns on how a reader parses this sentence.

**Repair:** either drop the now-orphaned Oxford comma and restore the original attachment — "so appenders and rewriters carrying a layer forward operate on files..." — or, if the parenthetical is wanted, unambiguously scope it: "so appenders, and rewriters that carry a layer forward, operate on files..." (adds "that... carry" to signal restriction) — either removes the two-comma sandwich that currently invites the joint reading.

**Unswept restatement check.** `grep -n "verifiers, appenders\|appenders, and rewriters\|appenders and rewriters"` → only line 439 (the hunk itself). Whitespace-normalized search for "cannot decode" / "decoding sample" / "operate on files whose layers they cannot decode" → exactly one occurrence in the whole document (the Note itself). No other restatement of this list exists to be left stale. Control search proving the normalization catches wraps: "no Part I structure requires decoding sample payloads" (spans lines 437-438) — line-oriented `grep` finds 0, but the whitespace-normalized python3 search finds 1. Technique validated.

## Group C: hunk 2 (figure (b))

**Rule the repair adopts:** the annotation bracket under the new index region (`index′`) should be closed at the region's own width, so the caption "every entry, re-emitted" reads as being about that region and not about everything to its right (the appended tiles, the new directory, etc.).

**Computing bracket columns (not judging by eye), per the brief's explicit instruction.** Using 0-indexed character columns (box-drawing and subscript/prime characters counted as single monospace columns, consistent with how the document already aligns them):

- Line "after" (`> after  │front│ tiles │▓index▓│▓▓▓▓▓▓▓▓▓▓▓▓▓│ +tiles │ index′ │ dir₂│pad│tr₂│`): the `▓index▓` cell's pipes are at columns 23 and 31; the `index′` cell's pipes are at columns 54 and 63.
- The **old** bracket, `└ old ─┘`, spans columns 24-31: `└` at 24 (one past the left pipe, i.e. the cell's first interior column) and `┘` at 31 (exactly the right pipe's column).
- Figure (a)'s two brackets confirm the same rule independently: `└── untouched ──┘` spans 16-32 (left pipe at 15, right pipe at 32); `└was dir₁…tr₁┘` spans 33-46 (left pipe at 32, right pipe at 46). In both, `└` sits one column right of the left pipe and `┘` sits exactly on the right pipe.
- §5.1's own figure uses the identical convention: `└──── re-emitted ────┘` under the `dir₃`/`pad`/`trail₃` span, again `┘` landing on the closing pipe.
- Applying that rule to the `index′` cell (pipes at 54 and 63) predicts a bracket spanning **55 to 63**.
- The repaired bracket, `└────────┘`, actually spans **54 to 63** — its `└` sits directly *on* the left pipe (column 54), one column left of where the document's own convention (verified against three independent sibling brackets, including the one immediately to its left on the very same line) puts it.

This is a small, mechanical off-by-one against the figure's own established alignment rule — not something eyeballing would catch, which is why the brief asked for it to be computed.

**Second, more consequential defect: label placement.** Every other bracket in this document's figures carries its caption *inside* the brackets, flanked by dashes on both sides of the text: `└ old ─┘`, `└── untouched ──┘`, `└was dir₁…tr₁┘`, `└──── re-emitted ────┘`. The repaired bracket instead is entirely dashes with no text (`└────────┘`) and the caption "every entry, re-emitted" trails **outside**, to the right of the closing `┘`. This is the only bracket in the document that puts its label outside the brackets rather than inside them. The repair fixed the reported defect (the bracket no longer runs unclosed to end of line, so it no longer visually claims everything to its right, including the appended tiles) but did so in a form inconsistent with every sibling mark in the same and other figures — the caption reads correctly in isolation, but a reader scanning the figure's convention (label-inside-bracket) could still misjudge what region "every entry, re-emitted" is attached to, since this is the one place the convention breaks.

**Verdict:** NEW_AMBIGUITY (two components: a one-column misalignment against the figure's own bracket-placement rule, computed and verified against three sibling brackets in two different figures; and a label-outside-bracket convention break unique to this mark). Not byte-level: the whole figure sits inside a `> **Example.**`-labeled block, non-normative under `[R-CNF-01]`; the caption's job is illustrative and the correct normative rule lives in step 4's prose, which I checked separately.

**Checking "every entry, re-emitted" against step 4.** Step 4 (§20.3, plain unlabeled prose, normative): "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array — necessarily at a new placement... with entries for tiles this commit stores or supersedes written to their new state, entries for tiles that become unstored written as the sentinel, entries new to this generation... emitted per §15, and every other entry byte-identical at its disk-ordinal position." The caption's "every entry, re-emitted" is consistent with this: the whole region is physically re-emitted (every entry's bytes appear again in the new region), even though most individual entries retain byte-identical values — "re-emitted" describes the region-wide physical act, not a claim that every entry's value changed. No contradiction between the caption and step 4.

**Repair for the placement issue:** put the caption inside the bracket on the model of the other three, e.g. `└─ every entry, re-emitted ─┘`, sized and left-aligned to start at column 55 (one past the left pipe of the `index′` cell) and closed at column 63 (the right pipe), matching the verified convention.

## Group B: hunk 3

**Rule the repair adopts:** the PE=0 drop-in-a-commit licence belongs to the appender specifically (not to "an updater" generically), because only appenders commit; the rewriter's parallel licence is the sentence's own next clause ("a rewriter MAY drop it in any rewrite"), already present and untouched.

**Check 3 (label, not marker).** This table (§20.4, "Governing flags | Updater obligation") carries **no** `>` prefix on any of its lines (verified directly against the raw source, lines 3495-3510) — it is plain, unlabeled, normative text under `[R-CNF-01]`. The repair lands in force-carrying text, as intended.

**Check 1 (tense/quantifier/actor) and the repair's own claim ("no actor gains or loses a drop by it").** I verified the premises independently:
- §9.1 (`[R-LIF-01]`): "every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite ... (a rewrite, §20.5)" — commit and rewrite are the only two mutation shapes, and mutually exclusive as named operations.
- §20.5: "That a rewrite is not a commit (`[R-LIF-01]`) fixes what the output *is*" — explicit, direct confirmation a rewrite is never a commit.
- §20.1 (`[R-CNF-06]`): "Its tiers, the appender and the rewriter, are §20.1's" — an updater is exhaustively and exclusively one of exactly these two tiers; no third tier exists.
- §20.1: "creator — emits a complete file in one commit, its first generation" — a creator *also* commits, but a creator is explicitly "a writer and nothing more," not an updater (`[R-CNF-06]`), and has no prior generation's record to "drop" (dropping presupposes a superseded state). So the set of actors that can meaningfully invoke "MAY drop the record in any commit" was, both before and after the repair, exactly the appenders — the pre-repair "an updater... in any commit" was already vacuous for rewriters (who never commit) and inapplicable to creators (nothing to drop), so it never actually reached anyone but appenders. Narrowing "updater" to "appender" here removes no reachable case and adds none.
- §20.3 step 2 already presupposes this: "An appender MUST... MUST NOT drop the record save where §20.4 licenses the drop" — the appender's own procedure already treated the §20.4 licence as its own to invoke; the repair now makes the antecedent match the actor exactly.

Grep control: `an updater MAY drop` → 0 hits (confirms the sweep is complete, no stale restatement of the old wording survives); `an appender MAY drop` → 1 (the repaired row); `a rewriter MAY drop` → 1 (the untouched clause in the same sentence).

**Check 4 (contradiction with untouched text in the same structure).** Read the whole cell and the paragraph below it (both untouched by the hunk):
- The SHOULD-report sentence in the same cell — "An updater that drops such a record SHOULD report the loss" — was **not** narrowed to "appender," and correctly so: both tiers can drop (appender by commit, rewriter by rewrite per the next clause), and both owe the same reporting duty. Confirmed by Appendix H's own summary (untouched, non-normative but a useful cross-check): "Advisory, and not a conformance condition, of an appender and a rewriter alike: an updater that drops a record SHOULD report the loss (§20.4)." No mismatch.
- The paragraph immediately below the table ("A commit MAY therefore drop a layer record...", "...an updater that drops a layer SHOULD report the loss, as the table says of any record dropped") uses "a commit" (= an appender's operation, per the definitions above) for the drop-by-commit case and separately treats drop-by-rewrite in §20.5 — consistent with, not contradicted by, the row's new appender/rewriter split.
- Appendix H's fuller checklist (lines 4924-4954, untouched) already itemizes the appender's and the rewriter's drop entitlements **separately** — "as an appender... drops a layer record only under §20.4's PE = 0 licence" in the appender paragraph, and "A rewriter, in addition... drops a layer or a PE = 0 record by omitting it, reclaiming what it addressed" in the rewriter paragraph — i.e. this non-normative summary already matches the *post-repair* shape of the row, not the pre-repair one. That means the row's old "an updater... in any commit" wording was already the odd one out relative to Appendix H, and the repair brings the row into line with a restatement that didn't need to change.
- Appendix G item 8 (untouched): "a record whose governing flags are MU = 0 and PE = 0 is retained or dropped at **the rewriter's choice** (§20.4)" — again already actor-specific (rewriter), consistent with the repaired row's split rather than with the old generic "updater" wording.

No contradiction found; if anything the repair resolves a mismatch between the row and two restatements (Appendix H, Appendix G item 8) that were already actor-specific.

**Check 5 (exhaustive claims).** No new "every/only/the two/whatever" language introduced by this hunk; the surrounding "one whose only effect is the drop included" is unchanged text.

**Check 6 (unconstrained siblings).** The structure is the three-row table. Sibling rows (MU=1; MU=0/PE=1) are untouched and were not implicated by this finding — MU=1 already has its own rewriter-specific carve-out sentence ("At either scope a rewriter MUST refuse to rewrite the file..."), so the table's established pattern is exactly "generic updater framing, with appender/rewriter specifics called out inline where they diverge," which is what row 3 now also does. No sibling left unconstrained by this change.

**Check 7 (analogy).** No "exactly as / on the model of / the same way" language appears in the edited text.

**Check 8 (anaphor).** This hunk is a substitution, not an insertion between sentences; the two nearby anaphors — "MAY drop **it**" (→ "the record") and "An updater that drops **such a record**" (→ the same PE=0 record) — resolve identically before and after, since only the subject noun of the first clause changed, not the object.

**NESTED_DASH check.** The cell contains one em-dash pair, "— one whose only effect is the drop included —", and it is not nested inside another dash-delimited clause in this cell (the earlier "— its extent becoming slack." is a single trailing dash, not a pair). No NESTED_DASH finding here.

**Verdict:** no defect found in hunk 3's repair. It is normative (unlabeled table), its premises check out against `[R-LIF-01]`, `[R-CNF-06]`, §20.1 and §20.5 directly, its "no actor gains or loses" claim holds, and two independent non-normative restatements (Appendix H, Appendix G item 8) already matched the post-repair shape rather than the pre-repair one — meaning this repair, if anything, resolves a latent normative/non-normative mismatch rather than creating one.

## Operations read through (brief's final exercise)

- **Appender, commit does nothing but drop an unimplemented-type PE=0 record:** licensed — "implementing a record's type confers understanding of it, and the permission to drop it is the bit's alone" (§20.4, untouched) — unaffected by any of the three repairs.
- **Rewriter dropping the same record:** licensed by the row's untouched second clause; unaffected.
- **Rewriter dropping a layer:** governed by §20.4's table + §20.5's "Dropping is the one disposal that answers, and only where §20.4's table licenses it"; unaffected.
- **Updater deciding whether the SHOULD-report binds it, as appender and as rewriter:** binds both, per the cell's untouched SHOULD sentence and Appendix H's "of an appender and a rewriter alike"; unaffected.
- **Verifier handed a file with an inexecutable codec:** reports *cannot establish* per `[R-CNF-11]`/§9.7; hunk 1 (a non-normative Note edit) changes nothing here.
- **Appender adding a layer to such a file:** licensed — §19.3/`[R-WRT-03]` never require decode for an appender's obligations regardless of what hunk 1's Note says; unaffected.

None of the three repairs changes the answer to any of these six scenarios.

## Summary of findings

1. **Hunk 1** — NEW_AMBIGUITY. The comma moved when "verifiers," was struck now lets "carrying a layer forward" be read as modifying both "appenders" and "rewriters" rather than "rewriters" alone, silently narrowing what looks like an unconditional claim about appenders. Not byte-level (non-normative Note).
2. **Hunk 2** — NEW_AMBIGUITY. The closed bracket is one column off the document's own verified alignment convention, and — more substantively — is the only bracket in the document whose label sits outside rather than inside the bracket, against three independently-checked sibling marks. Not byte-level (non-normative Example).
3. **Hunk 3** — no defect found; independently confirmed sound against `[R-LIF-01]`, `[R-CNF-06]`, §20.1, §20.5, and two untouched non-normative restatements (Appendix H, Appendix G item 8) that already anticipated the post-repair actor split.
