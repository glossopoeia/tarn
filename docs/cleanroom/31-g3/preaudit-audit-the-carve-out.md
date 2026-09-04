# Audit transcript — lane "the-carve-out" (hunks 04, 13, 14)

## 0. Disclosure

Read:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-04.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-13.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-14.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md, by line ranges via `sed -n` (heading list; 95-152; 345-436; 689-762; 1076-1188; 1600-1680; 1679-1697; 1697-1744; 1899-1946; 1978-2046; 2113-2146; 2146-2271; 2284-2300; 2330-2376; 3104-3330; 3320-3393; 3405-3430; 3597-3683; 3737-3794; 3794-3831 (grep-filtered); 3865-3980; 4186-4224; 1233-1243) and by grep.

Did not read: full.diff, any other hunk file, docs/, conformance/, PLAN/OPEN-QUESTIONS/AGENTS/README, registry.json, git history, the web. Did not list the case directory.

Wrote: this file only.

Context I did not ask for: my runtime placed a project-instruction pointer (CLAUDE.md -> AGENTS.md), a memory index naming four note files about this project's harness and repair history, a git status block with five recent commit subjects, and an environment block in my context before I began. I did not open any of the files they name and did not use their contents; the commit subjects mention round numbers and counts that I have not relied on. Findings below rest on the specification text and the three hunk files only.

Hunk headers vs bodies: hunk 04 header says lines 1632-1637 under "11.1 Geometry and its validity floor"; the body's changed lines are at 1632-1637 in the current file inside §11.1's Rationale block — consistent. Hunk 13 header says 3226-3232 under "20.3 The append procedure"; body lands at 3227-3232 (the "+" lines) — consistent. Hunk 14 header says 3271-3276; body lands at 3271-3276 — consistent. No discrepancy.

## 1. The text as it now stands

### Hunk 04 — §11.1, Rationale block (lines 1620-1652)

Block opens `> **Rationale.**` (line 1620). Under [R-CNF-01] (line 105-107: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative") this block is NON-normative. Test applied: the label, not the ">" marker.

Repaired sentence (1629-1637):
"a shrink is barred wherever it alters what §14 fixes for such a tile — whether or not the new state still stores it — and permitted wherever it does not: a tile dropped out of the addressed set carries no §14 obligation and its extent becomes slack — by a grid count falling or, in a planar layer, by its channel being removed (§20.3) — a tile the superseded generation did not store carries none either, and a new padding position whose stored byte already holds the fill alters nothing. One shrink can do several of these at once."

Followed (1640-1643) by: "The other bar reaches neither a shrink nor a growth: it bars a change to a planar layer's channel declarations that moves a stored tile's disk ordinal."

### Hunk 13 — §20.3 step 4, the ordinal-bar paragraph (lines 3210-3244)

Inserted (3227-3232): "Removing a channel de-addresses its N tiles: those the superseded generation stored carry no §14 obligation afterwards and their extents become slack (§5.2), as a shrink's de-addressed tiles do below, and the recommendation below to produce a new file instead reaches a commit that would strand a large share of a layer's stored bytes this way too."

Paragraph opens (3210-3218): "One effect is barred beside it, on the same tense and on its own ground: the §14 bar does not reach it, an ordinal move being no effect on any stored tile's bytes ... For a **planar** layer, a commit MUST NOT change the channel declarations in a way that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation this commit supersedes. A channel's tiles move exactly when its index does: reordering moves those channels the reorder re-indexes, and inserting or removing one moves every channel after the affected position. Either is such a change wherever the layer stores a tile for a channel that moved. Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at all — a disk ordinal is c · N + s ..."

After the insertion (3232-3244): "**The test is the effect on a stored tile, not the shape of the edit**: a commit that moves only the ordinals of channels the superseded generation stored no tile for alters nothing this bars. A layer with N = 2 and channels (`a`, `b`) places `a` at ordinals 0 and 1 and `b` at 2 and 3; appending `c` leaves those four where they are and adds 4 and 5, while exchanging `a` and `b` moves all four. An interleaved layer is unaffected, its disk ordinal being s, which no channel declaration enters. Where this bars a change the operation is a new layer or a whole-file rewrite, exactly as above."

### Hunk 14 — §20.3 step 4, the shrink paragraph (lines 3262-3309)

Repaired (3270-3276): "Dropping a tile out of the addressed set — §11.2's grid count falling, or a channel removed from a planar layer taking its N tiles with it — is not itself such an alteration, a tile the new state does not address carrying no §14 obligation and its extent becoming slack however it was de-addressed; but neither does it rescue a commit that damages a prior-generation stored tile."

Governing sentences above it (3262-3270): "An extent MAY also **shrink**, and the §14 bar is the whole of the test of what a shrink **alters**, **in that bar's own tense**; the obligations this step states below — among them slack, entry_count, a slab or alignment declaration (`[R-SLB-04]`, `[R-SLB-01]`), and the recommendation to produce a new file instead where a commit would strand a large share of a layer's stored bytes — bind a shrink as they bind any commit. A shrink is permitted exactly where it alters nothing §14 fixes for any tile the layer stores in the generation this commit supersedes."

Following sentences (3277-3300), verbatim where load-bearing: "Unstoring that tile in the same commit does not rescue it either, and for the same reason: the quantifier is the superseded generation's ... What counts as such an alteration is the §14 bar and nothing else, its carve-out included ... **The bar beside the §14 bar does not reach a shrink either: it bars a change to a planar layer's channel declarations that moves a stored tile's disk ordinal, and a shrink is not one.** A shrink whose damage falls only on tiles the new state no longer stores leaves the live state clean ... Where a shrink is permitted the de-addressed tiles' extents become slack (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region, and every surviving stored tile is untouched. ... A writer SHOULD instead produce a new file wherever a commit would strand a large share of a layer's stored bytes — and always where it would re-emit every one of them ..."

## 2. The rule each repair adopts (in my words)

- Hunk 04: (non-normative gloss) de-addressing a tile — by a grid count falling, or by removing a planar channel — is not a §14 alteration for that tile; its extent becomes slack; see §20.3.
- Hunk 13: (normative) removing a planar channel de-addresses its N tiles; for those of them the superseded generation stored, the commit owes nothing under the §14 bar and their extents become slack; the SHOULD-produce-a-new-file recommendation applies to such a removal when it strands a large share of the layer's bytes.
- Hunk 14: (normative) the "de-addressing is not itself a §14 alteration" carve-out covers BOTH de-addressing mechanisms — grid count falling and planar channel removal — and the freedom holds whatever the mechanism; de-addressing never rescues damage to a surviving prior-generation stored tile.

## 3. Derived effects of the operation (charter item 1)

Setup: planar layer, channels (a, b), C = 2, N = 2 (say d = 1, E = 2, T = 1 so G = 2), all four tiles stored. Disk ordinal = c·N + s ([R-GEO-06], line 1724-1727): a -> 0, 1; b -> 2, 3. Matches the step's own example (line 3235-3236) "places `a` at ordinals 0 and 1 and `b` at 2 and 3". entry_count = C·N = 4 ([R-CNT-17]); extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84 (matches §7.4 example, line 1175: "4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84").

Remove b (the last channel):
- addressed-tile count: C·N = 2·2 = 4 -> 1·2 = 2.
- entry_count 4 -> 2 (L21/[R-CNT-17]); extent_length 84 -> 2×20 + 1×4 = 44; one segment either way; crc_of_crc_array recomputed. Index region re-emitted at a new placement (step 4: "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full"; [R-LIF-01] freezes the old).
- surviving tiles' ordinals: a -> 0·2+0 = 0, 0·2+1 = 1 — unchanged. The two surviving entries are byte-identical at their disk-ordinal positions.
- removed tiles: b's two extents are reachable from no live entry -> slack under [R-CNT-21] (line 700-701 "everything an earlier commit superseded"; also §5.2's definition "Every byte the live state does not claim is slack").
- §14 bar on survivors: a planar tile's decoded size is P·Bᵃ, offsets k·Bᵃ (§14.2 table) — no channel-count term, so nothing §14 fixes for a's tiles changes. Consistent with hunk 13.

Remove a (the first channel):
- b's tiles move 2,3 -> 0,1. Barred by the ordinal bar (3214-3222) since b's tiles are stored in the superseded generation: "inserting or removing one moves every channel after the affected position. Either is such a change wherever the layer stores a tile for a channel that moved." If b stored no tile: permitted ("a commit that moves only the ordinals of channels the superseded generation stored no tile for alters nothing this bars").

Remove a channel from an INTERLEAVED layer (§14.2 example, line 2035-2040: a uint8, b uint16, P = 6, Q = 3, decoded size 18): removing b gives Q = 1, decoded size 6, every value's offset changes from (k div 2)·3 + F to k·1. That is "the decoded size, the byte offset ... of any value within the decoded tile image" — named in the §14 bar's list (3167-3172). Barred wherever the layer stores any tile. No tile is de-addressed (interleaved addressed count is N). The file such a commit would leave is detectably nonconforming: T14 (codec 1, entry length ≠ decoded size) or T3 (decoded payload length ≠ P·Q) at tile use.

Consequences the step states for a shrink, checked against channel removal:
| stated for shrink | stated for channel removal? |
|---|---|
| §14 bar is the whole test of what it alters | implicit: the bar is unconditional over "a commit" (3162-3165); hunk 13 says the de-addressed tiles carry no §14 obligation |
| de-addressed tiles: no §14 obligation, extents slack | YES (hunk 13, hunk 14) |
| does not rescue damage to a surviving stored tile | for removal, the damage in play is an ordinal move, and the ordinal paragraph states that bar directly ("removing one moves every channel after the affected position") — YES on its own ground |
| the ordinal bar does not reach a shrink | the counterpart for removal is stated: last-channel removal moves nothing, non-last removal is barred where later channels store tiles — YES |
| [R-CNT-17] obliges the smaller entry_count and a re-emitted index region; every surviving stored tile untouched | NOT restated for removal. Covered generically by step 4's re-emission rule (3149-3160, "Every layer whose stored-tile set or index content this commit changes...") and by "the obligations this step states below ... bind a shrink as they bind any commit" (3264-3268). Observation only; not a defect. |
| recommendation to produce a new file | YES (hunk 13) |
| slab/alignment obligations ([R-SLB-04], [R-SLB-01]) | not restated; [R-SLB-04] (line 2333-2342) is quantified over "A writer or updater whose commit changes the stored-tile set ... the disk ordinal of any tile the new state stores, or the slab declaration itself" — channel removal changes the stored-tile set, so it binds on its own words. Not a defect. |

## 4. The eight checks

### Check 1 — tense and quantifier
- Hunk 13: "those the superseded generation stored" — superseded tense, matching the bar's "any tile that layer stores **in the generation this commit supersedes**" (3162-3164). Actor: the appender. Set: the removed channel's N tiles. Passes. The word "afterwards" places the absence of obligation in the new state; see rejected candidate R-1.
- Hunk 14: "a tile the new state does not address" — new-state tense for the de-addressed set, superseded tense implicit for "carrying no §14 obligation". Unchanged from the pre-repair wording ("a tile the new state does not address carries no §14 obligation"). "however it was de-addressed" is a new universal — see check 5.
- Hunk 04: restates hunk 14; "a tile dropped out of the addressed set" — same set. Passes as a restatement.

### Check 2 — citations
- Hunk 04 "(§20.3)": §20.3 step 4 now carries the channel-removal account (hunk 13) — PASS.
- Hunk 13 "§14": the §14 bar is defined at 3162-3172 and named "Call this the **§14 bar**" — PASS. "(§5.2)": §5.2 defines slack as every byte the live state does not claim, [R-CNT-21] — PASS. "(§11.2)" (context line, unchanged): C·N addressed-tile count at 1656-1662 — PASS.
- Hunk 14 "§11.2's grid count": Gᵢ = ⌈Eᵢ/Tᵢ⌉ at 1656-1657 — PASS. "§14": as above — PASS.
- Context citations in the same sentences: [R-GEO-06] (1724-1727, c·N+s) — PASS; [R-CNT-21] (728) — PASS; [R-CNT-17] (1113-1119) — PASS.

### Check 3 — normative placement
Grep `de-address` -> 4 hits (3227, 3229, 3275, 3293), all inside §20.3 step 4's numbered item, not in any labelled block: normative. Grep `channel being removed|removed from a planar|Removing a channel|removing the last` -> 1633 (Rationale block, §11.1), 3223, 3227, 3272 (step 4). The normative statement of the widened carve-out is in step 4 (hunks 13 and 14); the §11.1 block is labelled **Rationale.** and carries no force, which is correct for a gloss. Control: `grep -n 'whole of the'` -> 3262, 3953 (present, as expected). PASS for all three.

### Check 4 — contradiction in the same passage
Found one (C-01, hunk 14): the widened sentence enumerates "a channel removed from a planar layer" as a species of its subject; four sentences on, the same paragraph says "The bar beside the §14 bar does not reach a shrink either: it bars a change to a planar layer's channel declarations that moves a stored tile's disk ordinal, and a shrink is not one." A non-last channel removal from a planar layer with stored later tiles IS "a change to a planar layer's channel declarations that moves a stored tile's disk ordinal" and IS barred (3214-3222). Before the repair the subject of the paragraph was extent-shrink only and the sentence was simply true; the repair folded a channel-declaration change into the paragraph's subject without touching the sentence that says the subject is not a channel-declaration change. The same shape recurs in hunk 04 (C-02): "One shrink can do several of these at once" and "The other bar reaches neither a shrink nor a growth" now follow a list that includes a channel removal.
Hunk 13's paragraph: no contradiction found between the insertion and the ordinal bar; the insertion speaks of the §14 obligation and slack, the bar of ordinals.

### Check 5 — exhaustive claims
- Hunk 13 "its N tiles": a planar channel c owns exactly the tiles at ordinals c·N .. c·N+N−1 — N of them. Verified against [R-GEO-06] and §11.2. Holds.
- Hunk 14 "however it was de-addressed": ways to de-address a tile from the layer record: extent falling (grid count falls), tile extent rising (grid count falls), planar channel removal, rank reduction, layout planar->interleaved (C·N -> N). Grid-count falling by either cause is inside "§11.2's grid count falling". Rank reduction, layout change, and tile-extent change each alter what §14 fixes for every SURVIVING stored tile (P, decoded size, padding set), so the sentence's own tail "neither does it rescue a commit that damages a prior-generation stored tile" bars them wherever a tile survives; where nothing survives (E -> 0), the de-addressed tiles do carry no obligation under the document's own shrink treatment. The universal is not falsified from the document. Holds.
- Hunk 14 "taking its N tiles with it": holds (as above).
- Hunk 04 "One shrink can do several of these at once": now falsifiable — a shrink cannot remove a channel; see C-02.

### Check 6 — what else in the structure is unconstrained
Structure: the de-addressing event, i.e., a change to a layer record's declaration fields that lowers the addressed-tile count (Eᵢ, Tᵢ, C in planar, d, layout). Each sibling: Eᵢ falling — governed (shrink paragraph). Tᵢ rising — inside "grid count falling"; survivors damaged -> barred by the §14 bar's decoded-size/padding items. C falling in planar — now governed (hunks 13/14). d falling — survivors' P and padding change -> §14 bar. layout planar->interleaved — survivors' decoded layout changes -> §14 bar. I found no sibling left ungoverned. Note that the C-falling case in an INTERLEAVED layer de-addresses nothing but is §14-barred via Q; hunk 13's sentence does not carry the "planar" qualifier (C-03).

### Check 7 — analogies, verb against verb
- Hunk 13: "their extents become slack (§5.2), as a shrink's de-addressed tiles do below" — cited: "Where a shrink is permitted the de-addressed tiles' extents become slack (`[R-CNT-21]`)" (3293-3294) and hunk 14's "its extent becoming slack". Verbs: "become slack" / "become slack"; sets: tiles the new state does not address that the superseded generation stored / same. PASS.
- Hunk 13: "those the superseded generation stored carry no §14 obligation afterwards" vs hunk 14 "a tile the new state does not address carrying no §14 obligation". Verbs "carry no §14 obligation" / "carrying no §14 obligation"; same set. PASS (with the "afterwards" caveat in R-1).
- Hunk 13: "the recommendation below to produce a new file instead reaches a commit that would strand a large share of a layer's stored bytes this way too" vs "A writer SHOULD instead produce a new file wherever a commit would strand a large share of a layer's stored bytes" (3297-3300). "a commit that would strand a large share" / "a commit would strand a large share". Same quantifier. PASS.
- Hunk 04: points at §20.3 rather than arguing by analogy. Nothing to compare.

### Check 8 — anaphors
Hunk 13's own back-references: "below" (×2) — resolve to the shrink paragraph (3262-3300) in the same step, 30 lines down; "the recommendation below" — resolves to the SHOULD at 3297-3300 and is also named at 3266-3268 in the shrink paragraph's opening. Both are where a reader of step 4 will look (the same numbered step; the word "shrink" is bolded at 3262). PASS. "this way" — de-addressing by channel removal, in-sentence. PASS.

Forward from hunk 13's insertion to the end of the paragraph:
- "**The test** is the effect on a stored tile ... alters nothing **this** bars" (3232-3234): before, nearest antecedents were the ordinal bar and "removing the last ... moves no ordinal at all"; now the nearest preceding sentence is the de-addressing/recommendation sentence. "this bars" still resolves to the ordinal bar because a recommendation does not bar and the colon-gloss says "moves only the ordinals". Unchanged in effect; noted as R-3.
- "those four" (3236): the example's own ordinals. Unchanged.
- "An interleaved layer is unaffected" (3239): before, "unaffected" by the ordinal bar (the paragraph's only subject); now the paragraph also states a de-addressing/slack/recommendation account, and "unaffected" reads as reaching it — see C-03.
- "Where **this** bars a change ... exactly as **above**" (3240-3242): "this" = ordinal bar, "above" = the §14 bar's "Such a change is a new layer, or a whole-file rewrite" (3207-3209). Unchanged.
- "the tense is both bars'" (3245): both bars, unchanged.

Forward from hunk 14's widened sentence to the end of the paragraph:
- "Unstoring **that tile** ... does not rescue **it** either" (3277): "that tile" = "a prior-generation stored tile" in the preceding clause; "it" = the commit. Unchanged.
- "**such an alteration**" (3282): an alteration of what §14 fixes. Unchanged.
- "**a shrink is not one**" (3289): "one" = "a change to a planar layer's channel declarations that moves a stored tile's disk ordinal". Referent unchanged; truth-condition now collides with the widened subject — C-01.
- "**the de-addressed tiles'** extents" (3293): before, tiles de-addressed by the grid count falling; now, under the widened sentence, tiles de-addressed by either mechanism — but the clause is governed by "Where a shrink is permitted", so it ranges over the shrink's own tiles. Unchanged in effect.
- "**this way**" does not occur here.

Hunk 04 backwards/forwards: "**these**" in "One shrink can do several of these at once" (1636-1637): before, {tile dropped by grid count falling, tile the superseded generation did not store, padding position already at fill}; now the first member is split into {by grid count falling, by planar channel removal}. A shrink cannot do the second — C-02. "The other bar" (1642): the ordinal bar, unchanged. "such a tile" (1629-1630): a tile the layer already stored — unchanged.

## 5. Sweeps (verbatim, with counts)

- `grep -n -i 'de-address' spec/tarn.md` -> 4 (3227, 3229, 3275, 3293).
- `grep -n -i 'removing a channel\|channel removed\|removing the last\|removes a channel\|channel being removed\|removed from a planar' spec/tarn.md` -> 4 (1633, 3223, 3227, 3272).
- `grep -n -i 'strand' spec/tarn.md` -> 7 (3205, 3231, 3267, 3298, 3421, 4196, 4198).
- `grep -n 'large share' spec/tarn.md` -> 3 (3231, 3267, 3298).
- `grep -n -i 'become[s]* slack\|becoming slack' spec/tarn.md` -> 9 (1632, 3229, 3274, 3293, 3303, 3334, 3366, 3382, 3417).
- `grep -n 'channel declaration' spec/tarn.md` -> 4 (1643, 1748, 3216, 3240).
- `sed -n '3452,3595p' spec/tarn.md | grep -n -i 'channel\|shrink\|re-declar'` (§20.5) -> 0. Control: `grep -n -c 'channel count' spec/tarn.md` -> 11, and `grep -n -i 'planar' spec/tarn.md | wc -l` -> 55, both nonzero on the same file.
- `sed -n '4698,4770p' spec/tarn.md | grep -n -i 'shrink\|channel\|slack'` (Appendix H) -> 2 (fill per channel; slack total), neither a restatement of the carve-out.
- `grep -n 'afterwards' spec/tarn.md` -> 1 (3228, the hunk itself).
- `grep -n 'the recommendation' spec/tarn.md` -> 2 (3230, 3266).
- `grep -n 'several of these' spec/tarn.md` -> 1 (1636).
- `grep -n 'a shrink is not one\|is not one\.' spec/tarn.md` -> 1 (3289).
- `grep -n -i 're-til\|retil' spec/tarn.md` -> 0. Control for the zero: `grep -n -i 'tile extent' spec/tarn.md` returned many hits (the filtered pipe returned 0 for change-words, but the unfiltered phrase is present at 1614 etc.), and `grep -n 'whole of the'` -> 2 hits on the same file.
- `grep -n 'unaffected' spec/tarn.md` -> 10 (227, 303, 304, 305, 2580, 2766, 3239, 3740, 3834, 3936); only 3239 is in the audited passage.
- `sed -n '3794,3831p' spec/tarn.md | grep -n -i 'decoded size\|decoded'` -> T3, T14, T21, T22 (decoded-size mismatch rows, used for byte-level grading of C-03).
- Wrap hazard: every phrase searched was a short fragment that does not span the hard wrap ("de-address", "strand", "large share", "channel declaration"); "become slack" was searched with the optional -s and the participle separately.

## 6. Restatements swept
- §23.1 (4190-4192): "a shrink that either drops tiles out of the addressed set or turns real positions into padding (§20.3 step 4)" — lists shrink but not channel removal as a way sample data becomes unreachable; the paragraph says "the list of operations above is not offered as closed" (4207-4208). Not a defect.
- §20.4 (3419-3425): "No commit therefore removes a layer record ... an in-place removal would strand that layer's stored tiles and index region as slack" — about layer records, not channels; consistent with hunk 13's recommendation reasoning.
- §20.3 Example (c) (3374-3382): "A layer that stored no tile in the generation the commit supersedes is re-declared freely ... a layer the commit itself empties does not qualify" — unchanged and consistent.
- §11.1 Rationale (hunk 04) is the only restatement of the carve-out outside step 4, and it was swept (with C-02's residue).
- §13.3 sparse-writing note (1940-1945) speaks of entry_count changes re-emitting the index; unchanged, consistent.

## 7. Findings

### C-01 — hunk 14 — LOCAL_CONTRADICTION (not byte-level)
Location: §20.3 step 4, shrink paragraph, lines 3270-3276 against 3287-3289.
Quotation (repaired): "Dropping a tile out of the addressed set — §11.2's grid count falling, or a channel removed from a planar layer taking its N tiles with it — is not itself such an alteration, a tile the new state does not address carrying no §14 obligation and its extent becoming slack however it was de-addressed; but neither does it rescue a commit that damages a prior-generation stored tile."
Contradicting (untouched, four sentences later): "The bar beside the §14 bar does not reach a shrink either: it bars a change to a planar layer's channel declarations that moves a stored tile's disk ordinal, and a shrink is not one."
Detail: the paragraph's subject is "a shrink" ("An extent MAY also **shrink**"). The repair enumerates a planar channel removal as one of the two things "Dropping a tile out of the addressed set" means, so the paragraph now discusses a channel-declaration change under the heading of a shrink, and then asserts that its subject "is not" a channel-declaration change. Two readings: (i) "shrink" still means extent-shrink and channel removal is mentioned only as a parallel mechanism — then the sentence at 3289 is true but the enumeration at 3271-3272 has smuggled a non-shrink into the shrink's carve-out; (ii) the paragraph's "shrink" now covers the enumerated de-addressings — then 3289 says the ordinal bar does not reach a channel removal, which is false for a non-last removal with stored later tiles (3214-3222). An implementer under (ii) removes channel a from (a, b) with b stored and believes only the §14 test applies. Not byte-level: the ordinal bar is stated unconditionally above in the same step and names removal ("inserting or removing one moves every channel after the affected position"), so a competent reading reaches the MUST NOT; and the shrink paragraph's own opening confines its "whole of the test" claim to what a shrink "alters". Interleaved removal is unaffected by this finding (no de-addressing occurs).
Repair: cut "or a channel removed from a planar layer taking its N tiles with it" and "however it was de-addressed" from this paragraph, leaving the channel-removal account where hunk 13 put it (the ordinal paragraph already says its de-addressed tiles behave "as a shrink's de-addressed tiles do below"); or, if the maintainer wants both mechanisms named here, append to 3289: "and a shrink is not one — a channel removal is, and the bar above judges it on its own ground."

### C-02 — hunk 04 — ANAPHOR (not byte-level; the block is labelled Rationale and carries no force)
Location: §11.1 Rationale block, lines 1629-1643.
Quotation: "a tile dropped out of the addressed set carries no §14 obligation and its extent becomes slack — by a grid count falling or, in a planar layer, by its channel being removed (§20.3) — a tile the superseded generation did not store carries none either, and a new padding position whose stored byte already holds the fill alters nothing. One shrink can do several of these at once."
Contradicting: "The other bar reaches neither a shrink nor a growth: it bars a change to a planar layer's channel declarations that moves a stored tile's disk ordinal." (1640-1643, untouched).
Detail: "these" (1636) ranged, before the repair, over three things a shrink does; the repair added a planar channel removal to the first of them, and a shrink cannot remove a channel, so "One shrink can do several of these" is now false for one member. The same enumeration sits under "a shrink is ... permitted wherever it does not", and is followed by "The other bar reaches neither a shrink nor a growth" — so the §11.1 reader is told a channel removal is among the shrink's permitted cases and that the other bar reaches no shrink, and is not told that the other bar reaches a non-last removal; the normative text (3214-3224) restricts the ordinal-free case to "removing the last". The block therefore says slightly more than the normative text. Also grammatical: the inserted dash-parenthetical replaced the comma that separated the first and second list items ("becomes slack, a tile the superseded generation..."), so the three-item list now reads as a run-on, and the parenthetical attaches to "becomes slack" rather than to "dropped out of the addressed set".
Repair: "a tile dropped out of the addressed set — by a grid count falling, or in a planar layer by the removal of its channel, which §20.3 judges under the other bar as well — carries no §14 obligation and its extent becomes slack; a tile the superseded generation did not store carries none either; and a new padding position ... alters nothing. One commit can do several of these at once."

### C-03 — hunk 13 — NEW_AMBIGUITY (not byte-level)
Location: §20.3 step 4, ordinal-bar paragraph, lines 3227-3232 and 3239-3240.
Quotation: "Removing a channel de-addresses its N tiles: those the superseded generation stored carry no §14 obligation afterwards and their extents become slack (§5.2), as a shrink's de-addressed tiles do below, ..." and, after the insertion, "An interleaved layer is unaffected, its disk ordinal being s, which no channel declaration enters."
Detail: of the three hunks, this is the only one whose channel-removal sentence lacks the qualifier "planar" (hunk 04: "in a planar layer"; hunk 14: "a channel removed from a planar layer"). The paragraph opens "For a **planar** layer", which scopes the sentence for a careful reader, but the paragraph closes with "An interleaved layer is unaffected", and that sentence's referent — the ordinal bar, the paragraph's only subject before this repair — is now one of several things the paragraph states. Read as "unaffected by channel removal", it is false: removing a channel from an interleaved layer de-addresses no tile (addressed count is N) and changes Q, so every stored tile's decoded size P·Q and every value's offset change — items the §14 bar names (3167-3172) — and it is barred wherever the layer stores any tile. Under a literal reading of "its N tiles" for an interleaved channel (the N tiles that carry it), an implementer concludes those tiles "carry no §14 obligation afterwards" and removes the channel from a stored layer. Not byte-level: the §14 bar's list is stated unconditionally above, and the resulting file is detectably nonconforming (T14 under codec 1, T3 otherwise: decoded size ≠ P·Q_new), so [R-CNF-05] bars every conforming writer from emitting it under both readings.
Repair: "Removing a planar channel de-addresses its N tiles: ..." and "An interleaved layer is unaffected by this bar, its disk ordinal being s, which no channel declaration enters — removing one of its channels is the §14 bar's subject instead, since Q enters every stored tile's decoded size."

## 8. Rejected candidates
- R-1 (hunk 13, "afterwards"): the word places the absence of §14 obligation in the new generation, while the bar insists its tense is the superseded generation's ("whether or not the new state still stores it"). Dropped because the document distinguishes unstoring (sentinel, no escape) from de-addressing (not an alteration), the sentence's own "as a shrink's de-addressed tiles do below" ties it to the normative shrink sentence, and hunk 14 states the same rule without the word. A one-word tidy, not a defect.
- R-2 (hunk 13, consequences unstated): [R-CNT-17]'s smaller entry_count and the re-emitted region are stated for a shrink (3293-3295) and not for a removal. Dropped: the re-emission rule at 3149-3160 is quantified over "Every layer whose stored-tile set or index content this commit changes", and 3264-3268 says the obligations "bind a shrink as they bind any commit".
- R-3 (hunk 13, "**The test** ... **this** bars"): nearest preceding sentence is now the inserted one. Dropped: the colon-gloss "moves only the ordinals" fixes the test, and a recommendation does not "bar".
- R-4 (hunk 14, "however it was de-addressed"): universal over mechanisms. Dropped after enumerating the siblings (check 6): every unnamed mechanism damages a surviving stored tile and the sentence's own tail bars it.
- R-5 (§23.1 restatement not swept): its list "is not offered as closed" (4207-4208).
- R-6 (hunk 13's "its N tiles" count): verified N from [R-GEO-06]; holds for planar.
- R-7 (hunk 04's force): block is labelled **Rationale.**; checked the label at 1620. A non-normative gloss of a normative sentence is the correct placement; no force defect.

## 9. Byte-level verdicts
C-01: not byte-level (ordinal bar stated unconditionally above; the shrink paragraph's carve-out addresses the §14 bar only).
C-02: not byte-level (Rationale, no force).
C-03: not byte-level (the §14 bar's list is unconditional; the disputed file is T3/T14-nonconforming under both readings, so the emittable set does not move).

No finding forks the bytes. The three are prose defects of the shape this project has been finding: a widened enumeration landing in a paragraph whose later sentences were written for the narrower subject.
