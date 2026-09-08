# Audit transcript — lane "the-renumbering" — hunks 09, 10, 13, 14

## 0. Disclosure

Files read, in order:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-09.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-10.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-13.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-14.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in ranges: 1090-1125, 1595-1670, 1700-1745, 2985-3025, 3075-3105, 3100-3320, 3319-3400, 3420-3450. Also targeted `grep -n` passes over the whole file (below).

Commands run (all via Bash `grep`/`sed`, read-only; no other files opened; nothing written outside the designated scratch dir except this transcript, which goes to the mandated `out/` path):
- `cat` on all four hunk files (full text reproduced below in each hunk's section).
- `grep -n '\[R-GEO-06\]' spec/tarn.md` → 6 hits (1662, 1739, 3019, 3178, 3194, 3238, 3255) [listed 7 lines above, includes the one from hunk 10's own inserted text].
- `sed -n '1700,1745p'` and `sed -n '1090,1125p'`, `sed -n '2990,3025p'`, `grep -n '\[R-CNT-17\]'` (11 hits), `grep -n '\[R-CNT-21\]'` (9 hits) — to pin `[R-CNT-17]` (entry_count = addressed-tile count) and `[R-CNT-21]` (slack).
- `sed -n '3075,3105p'` — to read §20.1 in full (the `[R-WRT-01]` rule hunk 9 cites).
- `sed -n '1595,1635p'` — to find the label on the block containing the pre-existing "renumber... wherever [R-GEO-06]" restatement at line 1662 (found: **Rationale.**, non-normative).
- `grep -n 'geometry change' spec/tarn.md` → exactly 3 hits, all inside the passage under audit (3177, 3246, 3252) — confirms "geometry change" is not a term defined/used anywhere else in the document.
- `grep -n 'denotes\|denote '` → 12 hits, used to disambiguate whether "the coordinate (R-GEO-06) ... denotes" in the §14 bar list is about spatial coordinate (tile/dimension mapping) or disk ordinal (channel/index mapping). Control: line 3238, in the (not-mine) tile-extents paragraph, ties "the coordinate each stored value denotes ([R-GEO-06])" explicitly to tile extents/dimension order, confirming the sense.
- `grep -n 'renumber' spec/tarn.md` → 5 hits; the three substantive ones (1662, 3178, 3252) checked against each other for restatement drift (see hunk 10/13 below); the two others (120, 122, 3782, 4350 area — requirement-identifier renumbering) are a different sense of the word, irrelevant.
- `grep -n '\[R-WRT-05\]'` (6 hits) and `sed -n '3420,3450p'` — to verify `[R-WRT-05]` in hunk 9's unchanged tail actually says what "a record re-emitted byte-identically" claims (§20.4's re-emission rule).
- `grep -n '^### 14\|^#### 14\.'` — confirms §14 = "Tile Serialization," the section the bar text keeps citing unbracketed.

No docs/, no ADRs, no PLAN.md, no OPEN-QUESTIONS.md, no AGENTS.md, no registry.json, no git log/diff, no web, no other lane's hunk files, no full.diff, no directory listing of case/. I did not write any scratch file — all computation was small enough to do inline in the transcript below; nothing needed a script.

**Context I did not ask for.** Before this task began, my context already contained a project CLAUDE.md pointer, a user-memory index (MEMORY.md) with bullet titles like "TARN harness spec path," "TARN lineage gate word list," "TARN preflight before launch," "TARN repair prose vs rules," "TARN harness vs charter," "TARN repair list vs diff," "Shell gates need explicit exit checks," "TARN subagents on Opus," plus later system-reminders about MCP server instructions, an "Auto Mode Active" notice steering me toward Bash over the Read/Edit tools, and a mid-task date change (2026-09-03 → 2026-09-08). None of this is part of the specification or evidence about it. I did not open any of the named memory files, did not act on the "Auto Mode" bias toward Bash-only tooling beyond what the charter itself already permits (grep via Bash), and did not let any of it inform which findings I looked for. Flagging per the access-rule's mandatory-disclosure clause.

---

## 1. Deriving the renumbering cases (planar layer, C=3 {a,b,c}, N=2, a stored, b&c sentinel)

Governing rules: `[R-GEO-06]` (disk ordinal = s interleaved, **c·N+s** planar, c = channel index, N = spatial-tile count = ∏Gᵢ, §11.4); `[R-CNT-17]` (entry_count MUST equal the addressed-tile count, N interleaved / C·N planar — confirmed against the L21 register row at line 3813 too: "N interleaved, C·N planar"); the ordinal bar (§20.3, my hunk 13's second sentence's subject): "a commit MUST NOT change the channel declarations in a way that alters the disk ordinal [R-GEO-06] assigns any tile the layer stores in the generation this commit supersedes."

Baseline: a=idx0→ordinals{0,1}; b=idx1→{2,3}; c=idx2→{4,5}. a's two tiles stored; b's and c's four tiles sentinel. entry_count = C·N = 6.

**(1) Remove b.** Remaining order (a,c), indices 0,1. a stays at {0,1} (unmoved). c moves idx2→idx1, ordinals {4,5}→{2,3}. b's two entries are dropped (de-addressed, not "unstored" — they cease to exist as index entries at all).
- Permitted? The ordinal bar only reaches a change that moves the disk ordinal of "any tile the layer stores in the generation this commit supersedes." Only a's tiles are stored; a's ordinals don't move. b and c store nothing. So the bar is not triggered — **permitted**.
- Entries that move: c's two (relocate 4,5→2,3). Entries byte-identical in place: a's two (stay at 0,1). Entries dropped: b's two.
- entry_count: 6 → 4 (changes; C·N: 3·2→2·2).
- What the re-emission clause (hunk 10) now obliges: full index re-emission for this layer (stored-tile set/index content changed — R-CNT-17's entry_count changed), with a's entries byte-identical at 0,1, c's entries re-emitted at their new ordinals 2,3 (licensed by the widened parenthetical: "a permitted change to a planar layer's channel declarations renumbers ordinals wherever `[R-GEO-06]` moves them"), and no entries at all for the removed positions 4,5.

**(2) Instead insert d before c** (from the same baseline, not compounding with (1)). New order (a,b,d,c), indices 0,1,2,3. a unchanged {0,1}; b unchanged {2,3} (still before the insertion point); d is new at idx2→{4,5}; c moves idx2→idx3, ordinals {4,5}→{6,7}.
- Permitted? a's and b's stored/sentinel tiles are unaffected in ordinal. c has no stored tiles, so even though c's ordinal moves, the bar (which is keyed to *stored* tiles of the superseded generation) is not triggered — **permitted**.
- Entries that move: c's two (4,5→6,7). Byte-identical in place: a's two, b's two. New entries: d's two, emitted per §15 (as "entries new to this generation").
- entry_count: 6 → 8 (C·N: 3·2→4·2).
- Re-emission clause obliges: full re-emit; a and b byte-identical at their old ordinals; c re-emitted at 6,7 under the widened parenthetical; d's two entries newly emitted per §15's rule for added tiles.

**(3) Instead swap b and c** (again from the baseline). New order (a,c,b), indices 0,1,2. a unchanged {0,1}. c moves idx2→idx1, {4,5}→{2,3}. b moves idx1→idx2, {2,3}→{4,5}.
- Permitted? Neither b nor c stores any tile in the superseded generation, so the ordinal bar (keyed to stored tiles) doesn't reach either move — **permitted**.
- Entries that move: both b's and c's (they trade ordinal ranges). a's stay put.
- entry_count: unchanged (C is still 3; C·N stays 6).
- Re-emission clause obliges: full re-emit (index *content* — the ordinal-to-channel mapping — changed even though entry_count didn't); a byte-identical at 0,1; b and c re-emitted at their new (swapped) ordinals under the widened parenthetical.

**Does "a permitted change to a planar layer's channel declarations" name exactly the set of commits that renumber?** No. It is a strict superset. Case (2)'s own passage states this explicitly two paragraphs later (unchanged text, at line 3261): "Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at all." Appending a channel *is* "a permitted change to a planar layer's channel declarations" (it is not barred — a's, b's, c's ordinals are all untouched by an append), yet it renumbers nothing. Likewise a permitted sample-type re-typing of an unstored channel, a permitted rename, or a permitted fill change are all "permitted changes to a planar layer's channel declarations" that touch no ordinal at all. So the phrase, read as a class, is broader than "the commits that renumber" — only the reordering / non-final-insert / non-final-remove subset of "permitted changes to channel declarations" actually renumbers anything. See §3 below (hunk 13) for how this bears on the actual repaired sentence.

**Does "permitted" have a referent a reader can find?** Yes, but only forward: the word appears in hunk 10's parenthetical at line 3177 (inside step 4's entry-emission description) and again in hunk 13's gloss at line 3252, and the rule that actually defines the boundary of "permitted" (the ordinal-bar MUST NOT sentence) does not appear until line 3253-3256 — immediately after the hunk-13 gloss, but a full ~75 lines after hunk 10's first use of the word. A linear reader hits "permitted" at line 3177 with nothing yet said about what licenses a channel-declaration change; the referent exists and is locatable, but only by reading forward through the entire §14-bar / sample-type / tile-extent discussion first. I flag this as a live forward-reference gap but, per my assessment below, do not think it clears the bar for a filed finding on its own (see rejected candidates).

---

## 2. Hunk 09 — the shelter for a carried-forward violation

### The hunk

```
-   neither modifies nor relies on travels with that structure
-   (§20.1, `[R-WRT-01]`) — which is as true of an index entry copied
-   to its disk-ordinal position as of a record re-emitted byte-identically
-   (`[R-WRT-05]`). Certifying the whole file is a
+   carries forward unmodified travels with that structure (§20.1,
+   `[R-WRT-01]`) — which is as true of an index entry copied to its
+   disk-ordinal position as of a record re-emitted byte-identically
+   (`[R-WRT-05]`), and validating either to `[R-WRT-03]`'s depth is
+   not authoring it. Certifying the whole file is a
    verifier's office.
```

Lands at spec/tarn.md:3154-3164, inside §20.3 step 2 ("Open"), in the "An appender MUST, in order:" list — normative body text, not inside any blockquote. Checked: the paragraph opens "Reproducing a structure's bytes unchanged is not authoring them" — plain prose, no **Note.**/**Example.**/**Rationale.** label anywhere near it. Normative placement is fine (check 3 passes).

### The rule the repair adopts

Old: a violation latent in a structure the appender *neither modifies nor relies on* travels forward with that structure, uncorrected, and this is as true of a carried index entry as of a re-emitted record.

New: a violation latent in a structure the appender *carries forward unmodified* travels forward with that structure — a broader class, dropping the "nor relies on" restriction — **and** validating such a structure (index entry or record) to `[R-WRT-03]`'s depth does not make the appender its author.

### Check 1 — tense/quantifier, against the rule it restates

§20.1's actual text (read in full, lines 3096-3104):

> "An appender and a compactor satisfy every writer requirement for the bytes they produce and the preservation obligations of §20.4 for what they carry forward (`[R-CNF-06]`), and are readers of every structure they process (`[R-CNF-11]`) — a violation latent in a structure they **neither modify nor rely on** travels with it, and certifying the whole file is a verifier's office (§9.7). `[R-WRT-01]`"

The class §20.1/`[R-WRT-01]` actually names is "neither modify nor rely on" (a conjunction: *not modified AND not relied on*). Hunk 9's repaired sentence names a broader class — "carries forward unmodified" (silent on reliance) — while still citing `(§20.1, [R-WRT-01])` immediately after. §20.1 also uses the phrase "carry forward," but that occurrence is tied to a *different* citation, `[R-CNF-06]` (preservation obligations), not `[R-WRT-01]`. So the repair borrows §20.1's "carry forward" wording from the R-CNF-06 clause and grafts it onto the R-WRT-01 citation, producing a claim R-WRT-01's own words do not state.

### Check 2 — citations resolve

- `(§20.1, [R-WRT-01])` — opened and read in full above. States the narrower "neither modify nor rely on" class. The repaired sentence's "carries forward unmodified" class is a **superset** of that (it drops the reliance condition) — so this citation is attached to a claim broader than what it establishes. This is exactly the "citation points at a rule which almost says the claimed thing" shape the charter calls out as the most expensive kind, because R-WRT-01 genuinely is the right rule in spirit and does license *part* of the sentence.
- `[R-WRT-05]` — opened at §20.4 (lines 3441-3447): "an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify... a record it modifies is new output under its writer obligations. `[R-WRT-05]`" — matches "a record re-emitted byte-identically ([R-WRT-05])" precisely. Citation checks out (this portion is unchanged by the hunk — carried over from the original text — but I verified it since it sits in the repaired sentence).
- `[R-WRT-03]` (new in this hunk, "validating either to `[R-WRT-03]`'s depth") — opened §20.3's opening paragraph (lines 3122-3131): "An updater's verification depth follows reliance... the trailer and the full directory always... plus §19.3's layer validation for every layer whose record, index, or extents the commit modifies, and the §19.4 index chain for every segment whose entries the commit reuses... Structures the commit neither modifies nor relies on impose no further obligation. `[R-WRT-03]`" — this is indeed the rule defining validation *depth*, so "`[R-WRT-03]`'s depth" is an accurate label. Citation checks out.

### Check 4 — contradiction with untouched text in the same passage

§20.3's own opening paragraph (R-WRT-03, quoted above) states that re-emission "relies on every directory byte" *always*, and that §19.3/§19.4-depth validation applies to *every* layer the commit touches and *every* segment whose entries it reuses — i.e., plenty of "carried forward unmodified" material (untouched directory bytes for other layers, reused index-chain segments) **is** relied upon under R-WRT-03. So "carries forward unmodified" genuinely does include material R-WRT-01's own narrower "neither modify nor rely on" wording excludes. This is not a hypothetical: the very next numbered item (step 2, lines 3146-3153, unmodified by any of my hunks) already describes exactly this case — "a malformed index entry an appender meets **while re-emitting a region**... is carried forward byte-identically... not repaired" — an entry that is read/relied-on (to be copied) but not modified. The newly added clause ("validating either... is not authoring it") is doing real, needed work to cover this pre-existing scenario, which the *unmodified* R-WRT-01 text alone does not license. So the content of the repair is defensible and consistent with the rest of the passage; the defect is narrower than a full contradiction — it's that the citation `(§20.1, [R-WRT-01])` is asked to carry more than it states, and no other citation is offered for the added, load-bearing "validating... is not authoring it" clause.

### Check 8 — back-references (this hunk both inserts and deletes)

- "which is as true of an index entry copied to its disk-ordinal position as of a record re-emitted byte-identically" — unchanged, still resolves to the two items just introduced.
- "and validating **either** to `[R-WRT-03]`'s depth is not authoring it" (new) — "either" resolves to the two items in the immediately preceding "as true of X as of Y" clause (index entry / record). Clear antecedent, correctly placed right after its referents; not stranded.
- Forward, unaffected by the insertion: "Certifying the whole file is a verifier's office." (no back-reference). "An appender that carries a violation forward SHOULD report it, and a caller that is not told cannot know the file it extended was already damaged." — "it" (report it) = "a violation," self-contained in its own sentence; "it extended" = "the appender," self-contained. Neither back-reference's resolution changed by the insertion.

### Byte-level test

Does resolving the citation mismatch change what bytes a conforming appender may emit, or must accept/reject? No. The actual obligations governing a carried-forward defective structure are stated elsewhere in the same numbered step, untouched by this hunk: MUST NOT repair it, MUST NOT drop it save where §20.4 licenses the drop, SHOULD report it. This hunk's sentence is explanatory/justificatory — it tells the reader *why* the appender isn't on the hook for authorship of a pre-existing defect, but the concrete emit/accept/reject behavior is fixed by the surrounding MUST/SHOULD sentences, which this hunk does not touch. **Not byte-level.**

### Verdict: D-01, CITATION, not byte-level (see structured findings).

---

## 3 & 4. Hunks 10 and 13 — the two occasions for a renumbering

### Hunk 10 (the operative rule, step 4)

```
-   (a geometry change renumbers ordinals wherever `[R-GEO-06]`
+   (a geometry change, or a permitted change to a planar layer's
+   channel declarations, renumbers ordinals wherever `[R-GEO-06]`
    moves them). A layer
```

Lands at spec/tarn.md:3176-3179, inside the same "Write payloads and indexes" step-4 sentence enumerating the four categories of re-emitted index entries (stores/supersedes → new state; become-unstored → sentinel; new-to-generation → §15; every other entry → byte-identical, with this parenthetical as the carve-out).

### Hunk 13's second edit (the gloss, "One effect is barred beside it...")

```
-   the re-emission rule above, whose only stated occasion for a
-   renumbering is a geometry change. For a **planar** layer, a
+   the re-emission rule above, whose stated occasions for a
+   renumbering are a geometry change and a permitted change to a
+   planar layer's channel declarations. For a **planar** layer, a
```

Lands at spec/tarn.md:3251-3253. (The other, larger insertion in this same hunk — the "tile extents/dimensions" paragraph at lines 3235-3246 — is out of my charter's scope; the maintainer's brief assigns it to a different lane. I read it for context only.)

### The rule each adopts

Hunk 10: widens step 4's stated trigger for ordinal renumbering from "a geometry change" alone to "a geometry change, **or** a permitted change to a planar layer's channel declarations," conditioned throughout by "wherever `[R-GEO-06]` moves them."

Hunk 13: restates hunk 10's rule, in the course of explaining why the §14 bar doesn't reach a pure ordinal move, as: the re-emission rule's "stated occasions for a renumbering **are**" the same two things — but without carrying forward the "wherever `[R-GEO-06]` moves them" qualifier.

### Check 2 — citation / cross-reference to `[R-GEO-06]`

Opened §11.4 in full (lines 1711-1739). `[R-GEO-06]` is the tag on the *last* of four bullets: "The disk tile ordinal, which orders tile-index entries (§15), is s for an interleaved layer, and **c · N + s** for a planar layer (§14), where c is the channel's index... — channel-major grouping." Confirms: (a) the ordinal formula is exactly `c·N+s`, so only `c` (channel index — moved by reordering/insert/remove) or `N`/`s` (moved by a geometry/grid-count change) can move an ordinal; (b) the formula is planar-specific for the `c·N` term, so "a permitted change to a planar layer's channel declarations" is correctly scoped to planar layers only (interleaved ordinal = s, no channel term at all) — checked against §11.4's own text, holds.

### Check 5/7 — the exhaustive claim, compared word for word against what it restates

This is the substantive finding. I derived in §1 above that "a permitted change to a planar layer's channel declarations" is **not** coextensive with "the occasions for a renumbering" — it is a strict superset. The passage's own later, unmodified text proves it: "Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at all" (line 3261, two paragraphs after hunk 13's gloss). Appending a channel is indisputably "a permitted change to a planar layer's channel declarations" (nothing bars it), yet it renumbers nothing.

Hunk 10's parenthetical survives this because of its trailing hedge: "...renumbers ordinals **wherever `[R-GEO-06]` moves them**." Read this way, the sentence names two *categories from which* a renumbering can arise, conditioned on `[R-GEO-06]`'s formula actually producing a different value — it is not asserting that every member of either category renumbers something. Appending a channel is a member of "a permitted change to a planar layer's channel declarations" for which `[R-GEO-06]` moves nothing, so nothing is renumbered; the sentence is vacuously, not falsely, satisfied for that case.

Hunk 13's gloss drops that hedge. "...whose stated occasions for a renumbering **are** a geometry change and a permitted change to a planar layer's channel declarations" is an unconditioned identity statement ("the occasions are X and Y"), not a conditioned one. Read on its own — which a reader arriving at this sentence, in the middle of the ordinal-bar discussion, is entitled to do — it says: X and Y *are* the occasions, full stop. But X's own paragraph (two below) shows X is not uniformly an occasion; only the reordering/non-final-insert/non-final-remove subset of X is.

Check 7 (analogy/pointer comparison), applied explicitly: hunk 13's governing verb is the bare copula **"are"** (occasions... are X and Y — unconditioned identity). The rule it points at (hunk 10, "the re-emission rule above") has governing verb **"renumbers... wherever `[R-GEO-06]` moves them"** (conditioned causation). These are not the same claim-strength, even though — checked against the task's specific instruction — the two named items themselves ("a geometry change" / "a permitted change to a planar layer's channel declarations") are worded identically in both places, with only the expected "or"→"and" swap for the "are X and Y" construction. So the *nouns* match exactly; the *quantificational force* around them does not.

### Check 4 — contradiction with the paragraph the sentence sits in

Read forward within the same structure (the whole planar-ordinal-bar paragraph, lines 3248-3283, in full): "A channel's tiles move exactly when its index does: reordering moves those channels the reorder re-indexes, and inserting or removing one moves every channel after the affected position... Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at all." This is the paragraph's own, explicit statement of exactly which channel-declaration changes renumber — and it's narrower than "a permitted change to a planar layer's channel declarations." The gloss two sentences earlier and this later, precise statement are in the same paragraph and are in tension (not a hard contradiction — the gloss can be read charitably as inheriting hunk 10's hedge by cross-reference to "the re-emission rule above" — but the sentence as written, taken at face value, overclaims).

### Check 6 — what a coordinate item added elsewhere does to this paragraph's ground

The charter directs me to check whether "the §14 bar does not reach it, an ordinal move being no effect on any stored tile's bytes" — the premise my sentence opens with — still holds now that the §14 bar (four paragraphs above, lines 3184-3196, unmodified by any of my hunks) contains "the coordinate (`[R-GEO-06]`) each value in the image denotes" as one of its listed items. Checked: I disambiguated "the coordinate ... denotes" using the parallel, unambiguous occurrence at line 3238 (in the other lane's paragraph): "[tile extents, and dimension order] are what fix the coordinate each stored value denotes (`[R-GEO-06]`)." This ties "coordinate ... denotes" to tile extents/dimension order — i.e., the *spatial* (x₀,…,x_{d−1}) position a decoded value represents — which is fixed by T_i and dimension order (the first bullets of §11.4), not by channel index `c` (the last bullet, disk ordinal). Channel reordering changes `c` and hence the disk ordinal (an index/lookup key), but does not touch T_i or dimension order, so it does not change which spatial coordinate any stored value denotes. The §14 bar's "coordinate" item and an ordinal move are about different outputs of the same `[R-GEO-06]` rule-block. **The ground still holds; no contradiction from the coordinate item's addition.**

### Byte-level test

The operative, byte-governing rule is hunk 10's parenthetical, unaffected by hunk 13's imprecision. Hunk 13's sentence is expository — it explains why the §14 bar doesn't reach an ordinal move and transitions into the actual MUST NOT sentence that follows, which states its own, precise, correctly-scoped condition ("alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation this commit supersedes"). No writer's actual obligation is derived from the gloss sentence itself; the ordinal a tile must occupy is fixed deterministically by `[R-GEO-06]`'s formula regardless of how a reader parses this sentence's rhetorical scope. **Not byte-level.**

### Verdict: D-02, ANALOGY (hunk 13's gloss vs. the rule it restates), not byte-level.

Hunk 10 itself: checked against checks 1-8, no defect found — the hedge keeps it accurate. Noted in `rejected_candidates`.

---

## 5. Hunk 14 — the antecedent for "such a tile"

### The hunk

```
-   nothing: a commit that also alters what §14 fixes for such a tile
-   is barred. **The
+   nothing: a commit that also alters what §14 fixes for a tile the
+   layer stores in the generation this commit supersedes is barred.
+   **The
    test is the effect on a stored tile, not the shape of the edit**: a
```

Lands at spec/tarn.md:3270-3273, in the paragraph on removing a planar channel (part of the same long planar-ordinal-bar paragraph as hunk 13's gloss).

### The rule the repair adopts

Spells out the demonstrative "such a tile" as "a tile the layer stores in the generation this commit supersedes."

### Check 1 — hold the three parallel statements side by side

1. The §14 bar itself (unmodified, lines 3184-3187): "A commit MUST NOT change a layer's declarations in a way that alters, **for any tile that layer stores in the generation this commit supersedes**, what §14 fixes for its stored bytes or how they decode..."
2. The shrink paragraph's parallel sentence (unmodified, line 3312-3314): "A shrink is permitted exactly where it alters nothing §14 fixes **for any tile the layer stores in the generation this commit supersedes**."
3. Hunk 14, now: "...a commit that also alters what §14 fixes **for a tile the layer stores in the generation this commit supersedes** is barred."

All three now use the identical phrase "[a/any] tile the layer stores in the generation this commit supersedes." The only variance is "any" (1, 2) vs. the bare indefinite "a" (3). Checked whether this is a quantifier drift: in a *prohibition* ("MUST NOT ... for any tile") the two are logically equivalent to a *barring-conditional* phrased with the indefinite ("a commit that alters ... for a tile ... is barred") — ∀t¬Alter(t) [permitted] is the exact complement of ∃t Alter(t) [barred]. "A tile" here is existential-under-a-conditional, not a narrowing to some contextually-singled-out tile. Read this way, hunk 14 doesn't just avoid the demonstrative's ambiguity, it brings the sentence into near-verbatim alignment with the §14 bar's own quantifier and the shrink paragraph's parallel sentence. **The three now state one rule**, consistently worded (check 1: pass — this is a genuine improvement, not a defect).

### Was "such a tile" actually ambiguous before the fix, and did the fix pick the right resolution?

Traced the antecedent chain leading into the demonstrative (lines 3265-3272, unmodified apart from this hunk): "Removing a planar channel de-addresses its N tiles: those the superseded generation stored carry no §14 obligation afterwards and their extents become slack... As there, de-addressing rescues nothing: a commit that also alters what §14 fixes for such a tile is barred." Two readings were available for "such a tile": (a) narrowly, one of the just-mentioned, now-de-addressed tiles of the *removed* channel; (b) broadly, any tile the layer stores in the superseded generation, full stop (the same class the §14 bar already ranges over). Reading (a) turns out to be near-vacuous: those tiles "carry no §14 obligation afterwards," so "altering what §14 fixes" for one of them, post-de-addressing, is closer to an empty condition. The passage's exact structural twin, in the shrink paragraph (lines 3322-3325, unmodified): "Unstoring that tile in the same commit does not rescue it either, and for the same reason: the quantifier is the superseded generation's, so a shrink that alters what §14 fixes for a tile stored there is barred **whether or not the new state still stores it**." That "whether or not" is exactly reading (b) — the bar is judged against what the tile was in the *prior* generation, regardless of what the current commit does to it (unstores it, or here, de-addresses it via channel removal). Hunk 14's spelled-out antecedent adopts reading (b), and it is the reading that makes "de-addressing rescues nothing" a non-vacuous, working parallel to the shrink case's "unstoring... does not rescue it either." **The fix resolved the demonstrative correctly.**

### Check 8, on "As there"

"As there" (line ~3270, unmodified by this hunk — it sits immediately before the edited clause but is not itself part of the diff) is a *forward* reference, not backward: the sentence immediately preceding it ends "...as a shrink's de-addressed tiles do **below**, and the recommendation **below**..." (unmodified). "As there" = "as [is the case] there [below, in the shrink discussion]" — explicitly primed by the two "below"s in the immediately preceding sentence. Confirmed the target: the shrink paragraph's own "de-addressing rescues nothing" twin is "Unstoring that tile in the same commit does not rescue it either" (line 3322) — matching vocabulary ("rescues/rescue... nothing/it either"), confirming the forward link is to that specific sentence.

Checked whether any of my four hunks insert material between "As there" (~3270) and the shrink paragraph (~3306) that could pull this forward reference to a different target: none do. Hunk 13's tile-extents paragraph (not mine, but read for context) sits *before* "As there," not between it and its target. No hunk in my set touches anything in the 3283-3306 range. **"As there"'s resolution is unaffected, before and after hunk 14, and resolves correctly.**

### Check 3 — normative placement

This sentence sits inside the same step-4 "MUST, in order" list as hunks 9/10/13, no blockquote, no Note/Example/Rationale label nearby. Normative. Pass.

### Byte-level test

The spelled-out antecedent doesn't change which tiles the bar covers (I showed above it's the same class §14's bar and the shrink sentence already use) — it only removes an ambiguity a careful-but-uninformed reader might have resolved the *narrower*, near-vacuous way. Two implementers who both read "such a tile" correctly (as the class §14 already uses) and two who both read the spelled-out version would reach the same accept/reject verdicts. A reader who mis-resolved "such a tile" narrowly, before the fix, might have concluded the "rescues nothing" sentence adds no real constraint beyond what's already stated — but the *actual* constraint (the §14 bar itself, unmodified, at lines 3184-3187) still independently bars the same commits regardless of how this one restatement is read; this sentence is a restatement/reminder ("as there... rescues nothing"), not the sole source of the obligation. **Not byte-level** — this is a clarity improvement over a genuine-but-recoverable ambiguity, not a fork in emittable bytes.

### Verdict: no defect. Checked and passed all eight checks; noted as a rejected candidate (the pre-fix ambiguity was real but the fix picked the correct resolution and the underlying obligation was never solely carried by this sentence).

---

## 6. Sweep for restatements elsewhere that these repairs should have caught

- `grep -n 'renumber'` (5 hits, listed above) — the only substantive prior restatement of "occasion(s) for renumbering" is the **Rationale** block at line 1662 ("...disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`)..."), non-normative (block opens "> **Rationale.**", checked at lines 1595-1635) and, in any case, only discusses the *growth* case — it doesn't make an "only occasion" claim that the widened text would contradict. Checked and cleared.
- `grep -n 'geometry change'` (3 hits, all inside the audited passage, lines 3177/3246/3252) — "geometry change" is not used or defined anywhere else in the document. Line 3246 (the other lane's paragraph) glosses it as "an extent's growth and shrink... are the geometry changes this step permits" — consistent with, not contradicting, hunk 10/13's usage.
- `grep -n '\[R-CNT-17\]'` / `\[R-CNT-21\]'` — all other hits (§7, the L21/L22 register rows at 3813-3814, §9's slack discussion) are consistent with the entry_count/slack mechanics I derived in §1; none restate an "occasions for renumbering" claim that would need sweeping.

No unswept restatement found for these four hunks specifically.

## 7. NESTED_DASH sweep

Read the exact repaired text of all four hunks for an em-dash pair nested inside a clause already set off by em-dashes. Hunk 9's sentence has exactly one em-dash pair ("... (§20.1, `[R-WRT-01]`) — which is as true of ... `[R-WRT-05]`) ..." — only one "—", not a pair nested inside another). Hunk 10's parenthetical uses commas, no dashes. Hunk 13's sentence uses a colon and commas, no dashes. Hunk 14's sentence has none in the repaired span. **No NESTED_DASH instances in any of the four hunks.**

## 8. Rejected candidates (opened and closed)

1. Hunk 9, "either" in "validating either to `[R-WRT-03]`'s depth" — checked for a missing antecedent; resolves cleanly to "an index entry" / "a record" from the immediately preceding clause. Closed, not a defect.
2. Hunk 9, does the widened shelter conflict with the next sentence's SHOULD-report duty for a violation the appender "found... defective"? Checked; "not authoring it" is about attribution of writer-conformance fault, not about the separate, advisory SHOULD-report duty — the two coexist without contradiction, and the document already treats this exact scenario (a malformed entry an appender "meets" while re-emitting) two sentences earlier. Closed.
3. Hunk 13, does the §14 bar's "coordinate (`[R-GEO-06]`) ... denotes" item (four paragraphs above, added by another lane's hunk) undercut "the §14 bar does not reach [an ordinal move]"? Checked via the parallel, unambiguous phrase at line 3238; the coordinate item concerns tile-extent/dimension-order-derived spatial coordinate, not channel-index-derived disk ordinal. Closed, no contradiction.
4. Hunk 14, "a tile" vs. "any tile" — checked as a possible quantifier narrowing; shown logically equivalent in a barring-conditional. Closed, not a defect — in fact an improvement (see §5).
5. Hunk 14, "As there" — checked as a possible back-reference casualty of insertion; it's a forward reference, explicitly primed two sentences earlier by "below," unaffected by any of my four hunks. Closed.
6. Hunk 10, "permitted" used before its defining rule appears (~75 lines later) — considered as NEW_AMBIGUITY. The referent exists and is locatable on a forward read; the document uses forward reference conventionally elsewhere (e.g. "the recommendation below," "as a shrink's de-addressed tiles do below," both in this same passage). Did not clear the bar for a filed finding; noted here rather than reported as D-03.
7. Whether hunk 10's own parenthetical (not just hunk 13's gloss) overclaims in the same way — checked; its trailing "wherever `[R-GEO-06]` moves them" hedge is doing exactly the conditioning work that would be needed, and does distinguish it from hunk 13's unhedged restatement. Closed, hunk 10 is clean.

## 9. Confidence / what an empty result would have meant

Not applicable in full — two findings were filed (D-01, D-02) — but for the two hunks with no filed finding (10, 14) I record what I did that would have caught something: for hunk 10, I ran the same three-case derivation (§1) that surfaced hunk 13's defect, checked it against hunk 10's own wording, and confirmed the hedge saves it; for hunk 14 I traced the full antecedent chain back through the shrink paragraph and forward through "As there" to its target sentence, rather than accepting the diff's plausibility at face value.
