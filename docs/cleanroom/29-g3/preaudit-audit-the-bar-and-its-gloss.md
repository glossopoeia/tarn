# Audit transcript — hunks 02–06 (§20.3 step 4, the §14 bar and its companion ordinal bar)

## Disclosure

Per the access rule I read exactly:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-02.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-03.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-04.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-05.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-06.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (multiple ranges: 1-260 skim, 339-470, 1570-2350, 2495-2525, 3073-3412, 3543-3620 headings, 3864-3990, plus targeted greps below)

I did **not** read docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, full.diff, or any other
auditor's hunk file. I did not list the case/ directory. I ran no web
access. All commands run are Bash `grep`/`wc`/`mkdir`/`ls` against the spec
file only, plus Read calls against the spec and my own hunk files.

**Contamination notice (mandatory disclosure):** my runtime context, before I
began, contained a project `CLAUDE.md`/`AGENTS.md` pointer and a user memory
index (`MEMORY.md`) whose entry titles reference this same project ("TARN
lineage stays private", "TARN working cadence", "TARN register is the corpus
build list", "Spec edits need propagation checks", "Workflow verifier
failures", "Rob's decision style"). I did not open, follow, or act on any of
these — I never invoked a memory-reading tool and treated the presence of
these titles as inert background noise, not as evidence about the
specification. None of my findings below rely on anything from that material;
every claim below is anchored to a spec line number or a hunk file line I
quote. I flag the exposure here per the charter's mandatory-disclosure rule.

Working notes were not written to any file (all computation was done in-line
via grep and manual arithmetic in this transcript); nothing was written to
the scratch directory because no script or scratch artifact was needed.

## Hunks read (headers)

- hunk-02: lands 3139-3142, "sample within the decoded tile image, the sample
  type each value in the image is read under, or the codec and filter..."
  gains "Call this the **§14 bar**."
- hunk-03: lands 3152-3206, inserts (a) a classifying paragraph asserting a
  channel's declared sample type is "such a declaration" under the §14 bar,
  and (b) a new MUST NOT — "For a planar layer, a commit MUST NOT change the
  channel declarations in a way that alters the disk ordinal [R-GEO-06]
  assigns any tile the layer stores in the generation this commit
  supersedes" — plus a worked N=2 example, and reflows two anaphors
  ("the bar's" → "both bars'"; a dangling "that channel's fill" →
  "for each channel the position carries, that channel's fill (§14.5)").
- hunk-04: lands 3215-3221, disambiguates "the bar above" → "the §14 bar" in
  the shrink-opening sentence and adds a sentence that other step-4
  obligations (slack, entry_count, slab/alignment, the SHOULD-new-file
  recommendation) still bind a shrink.
- hunk-05: lands 3232-3243, disambiguates a second "the bar above" → "the §14
  bar", and adds "The bar beside the §14 bar does not reach a shrink either:
  it bars a change to a planar layer's channel declarations that moves a
  stored tile's disk ordinal, and a shrink is not one."
- hunk-06: lands 3325-3328, in the non-normative "Example — the three shapes
  a commit takes" block, tightens "A layer storing no tile is re-declared
  freely" to "A layer that stored no tile in the generation the commit
  supersedes is re-declared freely ... — a layer the commit itself empties
  does not qualify."

I verified each hunk's claimed landing-line range against the live file by
Read (offsets shown above) — all five ranges matched their diff context
exactly; no header/body mismatch to report.

I then read the whole of §20.3 step 4 in one pass: spec/tarn.md lines
3073-3412 (from the "20.3 The append procedure" heading through the start of
"20.5 Compaction"), as the charter requires, not just the hunk windows.

## Sweeps run (verbatim, with hit counts)

1. `grep -n "R-GEO-06" tarn.md` → 5 hits: 1626, 1703, 2971, 3127, 3181, 3934
   (6 actually — recount below in transcript body).
2. `grep -n "disk ordinal" tarn.md` → hits at 1620, 1625, 1711, 1937, 2142,
   2240, 2280, 2328, 2969, 3015, 3181, 3188, 3197, 3239, 3690, 3949.
3. `grep -n "geometry" tarn.md` → hits at 91, 1109, 1559, 1586, 1943(none —
   actual list): 91, 1109, 1559, 1586, 1626, 1703, 2052, 2461(approx),
   3127, 3179, 3206, 3212, 3213, 3327, 3709, 3720, 4106, 4242, 4522 (see
   raw tool output captured in this session; used to test whether "channel
   count" is ever classed as a "geometry field").
4. `grep -n "sample type" tarn.md` → 8 hits: 185, 188, 1521, 1559, 1723,
   1728, 3139, 3154, 4714 (9 actually, see raw output — one is header
   text "12.1 Core sample types").
5. `grep -n "carries that channel|carries a channel|channel it carries|carries channel"` →
   4 hits: 378, 407, 410(no—see raw), 1617.
6. `grep -n "position carries|positions carr|carries a channel|carries the channel|channel the position|carries that channel|carrying that channel|carries every channel"` →
   7 hits: 378, 407, 410, 1617, 2091, 3156, 3163, 3205 (8 — see raw output,
   reproduced in body below).
7. `grep -n "the bar\b|bar's|bars'|companion bar|other bar"` → 7 hits: 1616,
   1618, 2609, 3009, 3203, 3216, 3949.
8. `grep -n "two bars|three bars|one bar|both bars|second bar|third bar|a third|only bar"` →
   2 hits: 1606, 3203. No stale count claim found anywhere else in the
   document.
9. `grep -n "R-COD-07|R-COD-10|R-SER-05\b|R-SLB-04|R-SLB-01\b|R-ENC-04|§14.5|§21.7"` →
   see body; used to verify every citation in the five hunks resolves.
10. `grep -n "^#### 21\.|^### 21"` → located §21.7 "What no check detects" at
    3864-3996, confirming hunk-05's "§21.7 records the consequence" citation.
11. `grep -n "^### 3\.|^#### 3\.1"` → 339, 341 — located the terminology
    section defining "channel" and "channel's index" (§3.1) and "tile" and
    "fill value" (also §3.1) to check the tile/channel "carries" direction.
12. `wc -l tarn.md` → 4768 lines total.

(Raw tool outputs for greps 1-2, 6-8 are preserved in this session's tool
call log; counts above are transcribed from those outputs at time of
writing. Where my count paraphrase above disagrees with the literal grep
output, the literal grep output governs — I include it below verbatim for
the two searches central to my finding.)

Verbatim grep output for the central search (geometry-field classification):

```
$ grep -n "geometry" tarn.md | head -60
91:layer validation resolves into Part II's value sets and geometry
1109:geometry-derived addressed-tile count, is a validity error at layer
1559:bit-exact and every geometry identical; sample types, geometry,
1586:The owning scope (§2.4) of a layer's geometry and linearization fields
2052:function of the layer's declarations alone — geometry, layout, and
3127:   (a geometry change renumbers ordinals wherever `[R-GEO-06]`
3179:   renumbering is a geometry change. For a **planar** layer, a
3206:   channel's fill (§14.5), and fill is a legal sample value — provided the grown geometry stays within every bound the
3212:   a growth is permitted exactly where the geometry it produces
3213:   satisfies every rule that geometry is subject to.
3327:> every rule its new geometry is subject to, which is the same step's
3709:| L21 | entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | ...
3720:| L32 | A layer geometry field whose floor is 1 is 0 | rank d; channel count C; tile extent Tᵢ | reader | layer access | `[R-GEO-01]` (R-CNT-23) |
4106:(§14.2, §14.3), so a reader allocates from geometry and never from
4242:dimension, and channel names; declared geometry; the write footprint
4522:structural field, which is why fill values, geometry, and codecs are not keys.
```

L32 (line 3720) is the load-bearing hit: the register's own descriptive
column names **"rank d; channel count C; tile extent Tᵢ"** together as "A
layer geometry field." This is the document's own vocabulary explicitly
classing channel count as a geometry field, and it is what my central
finding (C-01) turns on.

## Derived numbers

1. **Bar count in step 4, current text.** I counted normative MUST-NOT
   statements introduced with a naming device in step 4: (i) the §14 bar
   (line ~3133-3141, now named at 3141), (ii) the new ordinal bar (line
   3179-3182, "a commit MUST NOT change the channel declarations in a way
   that alters the disk ordinal..."). Count: **2**. Cross-checked against
   every place in the document that states a count: line 1606 ("Of its two
   bars...") and line 3203 ("the tense is both bars'") — both say 2. No
   other numeric claim about bar count exists anywhere in the document (the
   full "two bars|three bars|one bar|both bars|second bar|third bar"
   sweep above returned only these two hits). Count is internally
   consistent: **2 = 2**.

2. **Disk-ordinal arithmetic, worked by hand against R-GEO-06 (line
   1700-1703): disk ordinal = s (interleaved), c·N + s (planar), c =
   channel's 0-based index (§3.1, line 357).**

   - Example in the hunk: N = 2, channels (a, b). a at index 0 → ordinals
     0·2+0=0, 0·2+1=1. b at index 1 → ordinals 1·2+0=2, 1·2+1=3.
     Matches the hunk's claim ("a at ordinals 0 and 1 and b at 2 and 3").
   - Append c (new index 2): ordinals 2·2+0=4, 2·2+1=5; a,b unchanged (their
     indices didn't change). Matches "appending c leaves those four where
     they are and adds 4 and 5."
   - Exchange a and b (a→index1, b→index0): a's ordinals become 1·2+s =
     2,3 (were 0,1); b's ordinals become 0·2+s = 0,1 (were 2,3). All four
     positions change value. Matches "exchanging a and b moves all four."
   - General claims tested by hand-construction (not just the N=2 example):
     - "Appending a channel ... re-indexes nothing and moves no ordinal at
       all": for channels 0..C-1 unchanged, a channel appended at index C
       does not alter any existing c. True by inspection of the formula.
     - "removing the last[, re-indexes nothing]": removing the channel at
       index C-1 leaves indices 0..C-2 unchanged. True.
     - "reordering moves those channels the reorder re-indexes": swapping
       channels at indices i≠j moves exactly those two channels' N-tile
       blocks (verified with a 4-channel, swap-of-2 hand construction: a=0,
       b=1, c=2, d=3, swap b,d → a=0, d=1, c=2, b=3; only b and d's blocks
       moved, a and c unchanged). True.
     - "inserting or removing one moves every channel after the affected
       position": 3-channel (a=0,b=1,c=2), insert d at position 1 → a=0,
       d=1, b=2, c=3 (b,c shifted up by one, matching "after the affected
       position"); remove b (position 1) from (a=0,b=1,c=2) → a=0, c=1
       (c shifted down by one). Both match.
     - "a disk ordinal is c · N + s, ... so the channel count enters the
       addressed-tile count C · N (§11.2) but no individual ordinal": true
       by inspection — C never appears as a factor in c·N+s for any single
       ordinal, only in the aggregate count C·N (confirmed against §11.2,
       line 1636-1638, "addressed-tile count ... is N for an interleaved
       layer and C · N for a planar layer").
   - **Conclusion: I could not falsify any specific arithmetic claim in the
     ordinal-bar paragraph or its worked example.** The arithmetic is
     correct throughout.

3. **0x80 sample-type example** (line 3159-3160): int8 two's-complement,
   byte 0x80 = -128 (10000000b, most negative 8-bit two's complement value);
   uint8, 0x80 = 128. Both correct.

## The eight checks, run against each hunk

### Hunk 02 (§14 bar's enumerated list gains "sample type"; the bar is named)

**Rule adopted:** the set of things a channel-declaration edit MUST NOT
alter, for a tile the layer stored in the superseded generation, now
explicitly includes "the sample type each value in the image is read
under" (previously implicit only in the stem "what §14 fixes ... or how
they decode"), and this whole rule acquires the handle "the §14 bar."

1. **Tense/quantifier.** The list item is quantified "each value in the
   image," parallel in form to the surrounding items ("the decoded size,"
   "the byte offset of any sample"). The governing stem's tense is
   unchanged and still explicitly "any tile that layer stores **in the
   generation this commit supersedes**" (line 3134-3136, untouched by this
   hunk). No tense/quantifier mismatch introduced.

2. **Citations.** No new requirement ID or section number is introduced by
   this hunk (it only adds the phrase and a bold naming device). Not
   applicable beyond what's already checked as part of hunk-03's
   citations below.

3. **Label check.** This text sits inside numbered step 4 of "An appender
   MUST, in order:" (line 3085), no leading ">" anywhere in this
   paragraph — confirmed normative, not Note/Example/Rationale.

4. **Contradiction check.** I searched for whether "sample type" was
   already excluded from §14's scope anywhere. It is not; §14.2's
   byte-layout arithmetic is explicitly a function of each channel's
   element size (`Bᶜ`), itself derived from the declared sample type
   (§12.1) — so "how they decode" already depended on sample type before
   this hunk; the hunk just names that dependency explicitly. No
   contradiction found.

5. **Exhaustive claims.** None introduced by this hunk specifically (the
   "list names where that effect arises rather than standing on its own"
   disclaimer, at line 3146-3147, already existed and already disclaims
   exhaustiveness for the whole list, sample type included).

6. **What's left unconstrained.** Checked whether "channel layout" (planar
   vs interleaved, §7.4/§14.1) is separately enumerated. It is not listed
   item-by-item, but the governing stem ("what §14 fixes for its stored
   bytes or how they decode") is pre-existing, general, and explicitly
   non-exhaustive (line 3146-3147); §14.1 makes layout fully determine
   "how bytes decode," so a layout change is caught by the stem regardless
   of the specific list. Not a gap this hunk introduces or needed to close.

7. **Analogy check.** No "exactly as / following / the same way" language
   in this hunk.

8. **Back-reference check.** This hunk only appends to a list and adds a
   naming sentence; it does not insert new material *between* two existing
   sentences that could re-resolve an anaphor. (The anaphor consequences of
   inserting material happen in hunk-03, checked there.)

**Verdict on hunk-02: no defect found.** The naming device is corroborated
by two pieces of text this hunk does *not* touch: §11.1's Rationale (line
1602-1628, pre-existing) already uses the term "§14 bar" as if it were
already defined ("Of its two bars the one reaching a shrink or a growth is
the §14 bar" — line 1606), and §21.7 (line 3944, pre-existing) already
refers to "§20.3 step 4's **§14 bar**." Both of these were, before this
round, forward/loose references to a term that was never actually minted at
its point of use. Hunk-02 supplies the missing definition. This is a
targeted, correct fix, not merely decorative.

### Hunk 03 (classifying paragraph for sample-type re-typing; new ordinal
bar; anaphor fixes)

**Rule adopted, part A (sample-type classification):** re-typing a channel
falls under the §14 bar wherever the layer stores a tile carrying that
channel; free wherever the superseded generation stored no such tile
(whole-layer-empty, or — for planar — that one channel's own tiles all
unstored).

**Rule adopted, part B (new ordinal bar):** for a **planar** layer, a
commit MUST NOT change the channel declarations in a way that alters the
disk ordinal [R-GEO-06] assigns to any tile the layer stores in the
superseded generation. Reordering moves the reordered channels;
insert/remove (not-at-the-end) moves every channel after the affected
position; append/remove-last moves nothing; interleaved layers are
categorically unaffected.

1. **Tense/quantifier — part A.** "wherever the layer stores a tile that
   carries that channel" and "Where the superseded generation stored no
   tile carrying that channel" are both explicitly anchored to the
   superseded generation, matching the §14 bar's own governing tense (line
   3134-3136). Quantifier matches verb-for-verb: the §14 bar is quantified
   "for any tile that layer stores in the generation this commit
   supersedes" and the classification is quantified identically. **This
   restates, rather than merely resembles, the governing rule** — check 1
   is satisfied because the words track exactly, not just in spirit.

   I also checked this classification against a **pre-existing,
   untouched-by-this-hunk** sentence at line 1616-1617 (§11.1 Rationale):
   "Re-typing a channel is the §14 bar's own subject, barred wherever the
   layer stores a tile that carries that channel, and free where it does
   not." This is word-for-word the same rule the hunk now states
   normatively in §20.3. The Rationale had evidently been written already
   anticipating a normative statement that, before this round, did not
   yet exist in step 4's actual prose — hunk-03 supplies it. No tension.

2. **Citations — part A.** `§14.5` is cited for "for each channel the
   position carries, that channel's fill" in the growth clause (reflowed
   by this hunk, not new prose but re-anchored). I opened §14.5 (line
   2087-2098): "at every padding position, a writer MUST encode, for each
   channel the position carries, that channel's fill value..." — **exact
   phrase match**, correctly cited. This is the single most load-bearing
   citation in this hunk and it resolves cleanly.

   `(§11.2)` for "the channel count enters the addressed-tile count C · N"
   — opened §11.2 (line 1636-1638): "addressed-tile count ... is N for an
   interleaved layer and C · N for a planar layer." Matches exactly.

   `[R-GEO-06]` for "a disk ordinal is c · N + s" — opened §11.4 (line
   1700-1703): "s for an interleaved layer, and c · N + s for a planar
   layer ... where c is the channel's index." Matches exactly, including
   which variable is which.

   `[R-LIF-01], §20.5` for the new-layer/whole-file-rewrite remedy — this
   is a restatement of the identical remedy already given for the §14 bar
   three sentences earlier in the same paragraph (line 3171-3173,
   untouched). Consistent, not new.

   `(§11.1)` for "which is what schema-first creation needs" — opened
   §11.1's Rationale (line 1602-1603): "Empty layers serve schema-first
   workflows: declare layers at creation, grow extents as data arrives."
   Matches.

3. **Label check.** Same numbered-step-4 location as hunk-02, no ">" — 
   confirmed normative for both the classification paragraph and the new
   MUST NOT.

4. **Contradiction check — this is where I found a defect (C-01, below).**
   The new ordinal bar's own justification reads: "what it disturbs is
   instead the re-emission rule above, whose only stated occasion for a
   renumbering is a geometry change" (line 3177-3179) — asserting that
   channel-declaration edits are *not* "geometry changes" and therefore
   fall outside the pre-existing renumbering permission at line 3127
   ("a geometry change renumbers ordinals wherever [R-GEO-06] moves
   them"), which is why a fresh, separate bar is needed. I checked this
   classification against the document's own use of "geometry": the
   register row **L32** (line 3720) explicitly calls channel count a
   "layer geometry field," bundling it with rank and tile extent, and
   §11.1 is titled "Geometry and its validity floor" and states the
   channel-count floor (≥1) as part of that same section/rule (R-GEO-01,
   line 1589-1595). Given that, and given R-GEO-06 (the very rule the
   pre-existing sentence cites) has the channel index *c* as a term in its
   formula, the pre-existing sentence's plain words — "a geometry change
   renumbers ordinals wherever R-GEO-06 moves them" — read most naturally
   as licensing *any* R-GEO-06-driven ordinal move, channel-index-driven
   included, not only extent/tile-shape-driven ones. See C-01 for the full
   writeup and byte-level analysis.

   I also checked the surrounding carve-outs for collisions and found
   none beyond C-01: the "layer that stores no tile... MAY be re-declared
   freely" carve-out (line 3200-3203) was updated to "both bars'" tense
   consistently, and does not conflict with the new bar (an empty layer
   trivially satisfies "the layer stores a tile for a channel that moved"
   as false for every channel, so the ordinal bar never fires on it — 
   consistent).

5. **Exhaustive claims.** "A channel's tiles move exactly when its index
   does" (line 3182-3183) reads, taken in complete isolation, as an
   "exactly when" (iff) claim that could be falsified by a commit that
   *also* changes extent/grid-count in the same commit (which can move a
   tile's spatial ordinal *s*, hence its disk ordinal, without any change
   to *c*). I checked this as a candidate finding and rejected it: the
   sentence sits inside a paragraph explicitly scoped to "changes to the
   channel declarations" (the MUST NOT's own subject, restated in the
   sentence immediately before), and geometry-driven *s*-changes are
   governed by an entirely separate mechanism (the pre-existing
   parenthesis at line 3127, and §11.1's growth/shrink Rationale) that
   this paragraph never purports to describe. Read in its paragraph's own
   scope (channel-declaration edits holding N and s fixed), the claim is
   correct. I list this in rejected_candidates below rather than as a
   finding, because context resolves it and a competent reader would not
   read "moves" here as "moves for any reason whatsoever."

   "which no channel declaration enters" (interleaved case, line 3197) — 
   checked against R-GEO-06 (line 1701): interleaved ordinal is *s* alone.
   True, not overclaiming.

6. **What's left unconstrained.** I asked what other channel-declaration
   fields exist besides sample type and index/order: name and fill value
   (§3.1 line 356-358; §7.4/§13.1). Fill-value changes are independently
   governed by the pre-existing §14 bar (padding-position content is fixed
   to the fill by R-SER-05, so a fill change that reaches a stored tile's
   padding position is already barred; a fill change on a layer with no
   padding positions and no pad bits is explicitly the "directory-only"
   shape (c) in the Example block). Name changes have no byte-level
   decode consequence anywhere in §14's arithmetic (checked: §14.2's
   offset/length formulas use element size and channel *count*/*index*,
   never name) and are correctly left unconstrained, matching how a
   layer-level rename is treated in the same Example. No genuinely
   unconstrained field found here beyond the ambiguity in C-01.

7. **Analogy check.** "the tense is both bars'" (line 3202-3203) — compares
   the growth/empty-layer carve-out's tense to *both* the §14 bar's tense
   ("in the generation this commit supersedes," line 3134-3136) and the
   new ordinal bar's tense ("...assigns any tile the layer stores in the
   generation this commit supersedes," line 3181-3182). Both bars are
   quantified identically over "any tile the layer stores in the
   generation this commit supersedes" — verified verb-for-verb, matches on
   both sides. No mismatch.

   "Where this bars a change the operation is a new layer or a whole-file
   rewrite, exactly as above" (line 3198-3199) — compared against the §14
   bar's own remedy sentence three sentences earlier: "Such a change is a
   new layer, or a whole-file rewrite under a fresh file_id ([R-LIF-01],
   §20.5)" (line 3171-3173). Same remedy, same citation, genuinely
   identical (not merely analogous) — no mismatch.

   The "whose only stated occasion for a renumbering is a geometry change"
   clause (line 3178-3179) is itself the analogy-by-classification that
   produced finding C-01 above; I treat it under check 4 rather than
   duplicating it here, since its defect is a contradiction with an
   untouched rule rather than a quantifier mismatch between two
   *consistent* rules.

8. **Back-reference check.** This hunk inserts roughly 35 new lines between
   the (pre-existing) §14 bar paragraph and the (pre-existing) growth
   paragraph, and again before the (pre-existing) shrink paragraph two
   hunks later. I read forward from the insertion point to the end of
   §20.3 step 4 and listed every bare back-reference:
   - "the tense is the bar's" (pre-existing, at what's now line 3202) — 
     hunk-03 itself updates this to "both bars'", correctly capturing that
     a *second* bar now sits between the referring sentence and its
     original antecedent. Correctly repaired *by this hunk*.
   - "a position that becomes real held that channel's fill" (pre-existing
     growth clause) — this anaphor's antecedent ("that channel") did not
     exist in the paragraph at all in the pre-hunk text (I checked: the
     preceding sentences discuss "a layer," never a specific "channel").
     This was already a dangling reference *before* hunk-03, independent
     of the insertion; hunk-03 repairs it by universally quantifying
     ("for each channel the position carries") rather than resolving to a
     specific antecedent, and cites §14.5 for the phrase, which I verified
     resolves correctly (check 2 above). This is a genuine, good fix, not
     a new defect.
   - "the bar above" appears twice more, in the shrink paragraph, but that
     paragraph is not part of hunk-03 — it is fixed by hunk-04 and
     hunk-05, checked below. I confirm here that hunk-03 leaves those two
     instances *un-fixed* (they are literally two hunks away in the diff
     set, not touched by hunk-03), and I verified by grep (search 7 above)
     that by the time all five hunks are applied, no unqualified "the bar
     above" remains anywhere in step 4 — every instance now reads "the
     §14 bar," "both bars'," or "the bar beside the §14 bar." This is a
     coordinated, cross-hunk repair that is internally consistent across
     all five hunks I was given.
   - "which no channel declaration enters" (new, hunk-03's own text,
     interleaved case) — "it" implicitly refers to "disk ordinal," the
     nearest antecedent two clauses earlier in the same sentence
     ("its disk ordinal being s"). Resolves correctly, no ambiguity.

**Verdict on hunk-03: one confirmed defect (C-01, contradiction with
untouched line-3127 text over the scope of "geometry change"); one
candidate considered and rejected (the "exactly when" overclaim, resolved
by paragraph scope); all citations resolve; all anaphors this hunk
touches are correctly repaired.**

### Hunk 04 (shrink-opening disambiguation)

**Rule adopted:** "the bar above" → "the §14 bar" (disambiguating an
anaphor whose nearest antecedent, after hunk-03's insertion, would
otherwise have silently become the ordinal bar instead of the §14 bar);
plus an added sentence that step 4's other obligations (slack, entry_count,
slab/alignment invariants, the SHOULD-new-file recommendation) still bind a
shrink even though only the §14 bar constrains what a shrink may *alter*.

1. **Tense/quantifier.** "in that bar's own tense" (line 3216) still
   correctly singular ("that bar" = the §14 bar just named), and the
   sentence goes on: "A shrink is permitted exactly where it alters
   nothing §14 fixes for any tile the layer stores in the generation this
   commit supersedes" (line 3221-3223, unchanged by this hunk) — same
   tense as the bar itself. Consistent.

2. **Citations.** `[R-SLB-04]` and `[R-SLB-01]` — opened §16.2 (line
   2308-2314) and §16.1 (line 2260-2268): R-SLB-04 is exactly "A writer or
   updater whose commit changes the stored-tile set... MUST either
   re-establish the invariants... or clear the declaration"; R-SLB-01 is
   the per-tile alignment invariant. Both citations are accurate for "a
   slab or alignment declaration."

3. **Label check.** Normative, step 4, no ">".

4. **Contradiction check.** I checked whether "the obligations this step
   states below... bind a shrink as they bind any commit" collides with
   anything narrower stated for shrink specifically. It does not — the
   text this sentence forward-references (line 3244-3259, unchanged,
   "Where a shrink is permitted the de-addressed tiles' extents become
   slack... a slab declaration is re-established or cleared...") states
   exactly these obligations for shrink already. The new sentence is a
   correct summary/preview of unchanged material, not a new claim in
   tension with it.

5. **Exhaustive claims.** "among them slack, entry_count, a slab or
   alignment declaration... and the recommendation" — "among them" is
   explicitly non-exhaustive language. No overclaim.

6. **Unconstrained neighbors.** N/A — this hunk doesn't introduce a new
   structure to check for unconstrained siblings.

7. **Analogy.** None in this hunk.

8. **Back-reference.** The fix itself *is* a back-reference repair (see
   hunk-03's check 8 above for the full before/after). I re-verified: at
   the point this sentence sits, the nearest preceding bar-statement in
   the fully-patched document is indeed the ordinal bar (line 3179-3182),
   so "the bar above," left unrepaired, would have silently resolved to
   the wrong bar. The repair correctly names "the §14 bar" explicitly.
   Confirmed correct.

**Verdict on hunk-04: no defect found; the anaphor repair is necessary and
correct.**

### Hunk 05 (second shrink disambiguation; explicit ordinal-bar carve-out
for shrink)

**Rule adopted:** "the bar above" (second occurrence) → "the §14 bar"; and
a new sentence: "The bar beside the §14 bar does not reach a shrink either:
it bars a change to a planar layer's channel declarations that moves a
stored tile's disk ordinal, and a shrink is not one."

1. **Tense/quantifier.** Consistent with the ordinal bar's own stated
   scope ("a change to a planar layer's channel declarations" — line
   3237-3239 restates the bar's subject exactly as stated at its point of
   definition, line 3179-3182). Verbatim match on subject.

2. **Citations.** `§21.7` — opened and confirmed (§21.7 spans 3864-3996,
   located by heading grep). The cited consequence — "this is precisely
   where the §14 bar has no witness, the live state being clean" — matches
   §21.7's own text at line 3982-3986 ("a commit that supersedes every
   tile it would have damaged leaves the live state clean, so the §14 bar
   is unwitnessed there for the same reason [R-LIF-01] is"). Confirmed.

3. **Label check.** Normative, step 4, no ">".

4. **Contradiction check.** "a shrink is not one [a change to a planar
   layer's channel declarations]" — checked by definition: a shrink is
   introduced at line 3215 as "An extent MAY also shrink," i.e., an
   *extent* edit. Channel declarations (name/type/fill/order) are a
   disjoint field set from extent/tile-extent fields (§12 vs §11). A pure
   shrink, by construction, does not touch channel declarations, so the
   claim is definitionally true **given the extent/channel-declaration
   split the rest of the document uses.** I note this claim rests on the
   same field-classification question as C-01 (is a channel-*count*
   change a "declaration" edit, an "extent" edit, or a "geometry" edit?);
   for a *shrink specifically*, this doesn't matter, because a shrink
   changes extents only, never channel count — so hunk-05's claim survives
   the C-01 ambiguity untouched.

5. **Exhaustive claims.** "What counts as such an alteration is the §14
   bar and nothing else, its carve-out included" (line 3232-3234,
   pre-existing, unchanged by this hunk but immediately preceding the new
   sentence) — I checked this "and nothing else" against the newly-added
   sentence for collision: does the new sentence *add* a second thing that
   "counts," contradicting "nothing else"? No — the new sentence's whole
   point is that the *second* bar does **not** reach shrink, i.e., it
   affirms rather than contradicts "the §14 bar and nothing else" as the
   full test for shrink. Consistent, and in fact the new sentence is
   necessary to make that pre-existing "and nothing else" claim actually
   true post-hunk-03 (since hunk-03 introduced a second bar that could,
   absent this sentence, have been read as also constraining shrink).

6. **Unconstrained neighbors.** N/A.

7. **Analogy.** "and a shrink is not one" is a direct definitional claim,
   not an analogy to another rule's quantifier — no mismatched verbs to
   compare.

8. **Back-reference.** Same repair pattern as hunk-04; verified no
   remaining ambiguous "bar above" after this hunk (grep search 7, above).

**Verdict on hunk-05: no defect found.** This hunk is a necessary and
correctly-targeted consequence of hunk-03's insertion — without it, "the
§14 bar and nothing else" (pre-existing) would have been left ambiguous
about whether the newly-introduced second bar also bound shrink.

### Hunk 06 (Example block: withdraw-the-permission-you-just-emptied)

**Rule restated (non-normative):** "A layer that stored no tile in the
generation the commit supersedes is re-declared freely... a layer the
commit itself empties does not qualify."

1. **Tense/quantifier.** Matches the normative rule's tense exactly (line
   3200-3202, "A layer that stores no tile **in the generation this commit
   supersedes** MAY be re-declared freely") and matches a pre-existing,
   untouched sentence in §11.1's Rationale almost word for word: "A layer
   that stored no tile in the generation the commit supersedes may be
   re-declared freely; a layer the commit itself empties does not qualify"
   (line 1613-1616). This Example update is a correct sweep of that
   already-established rule into the illustrative text — exactly the kind
   of restatement propagation the charter asks me to check for, done
   correctly here.

2. **Citations.** None introduced.

3. **Label check — the important one for this hunk.** I confirmed the
   whole "(a)/(b)/(c)" block is inside one continuous `>`-prefixed
   quotation opened at line 3287 with **"> Example — the three shapes a
   commit takes."** and closed before "#### 20.4" at line 3342. Per
   [R-CNF-01], a block headed **Example.** is non-normative. This hunk's
   text is illustrative only; the *normative* version of the same rule
   lives at line 3200-3203 (step 4 proper) and was not touched by this
   hunk. Since both say the same thing, there's no risk of the Example
   drifting from the normative rule it illustrates.

4. **Contradiction check.** Checked whether "does not qualify" collides
   with the immediately preceding sentence in the same block, "A fill
   change on a layer that stores a tile carrying either is not an
   appender's operation at all (step 4)." No collision — that sentence
   covers the *stores* case, the new sentence covers the *stored-nothing-
   but-the-commit-itself-emptied-it* case; they partition cleanly, no
   overlap.

   I also checked whether "a layer the commit itself empties" could ever
   legitimately need shape (c) (directory-only) for a different reason:
   emptying a layer necessarily requires writing sentinel entries into its
   tile index, which is a full index re-emission (shape (b)), never a
   directory-only edit (shape (c)) — so the exclusion is doubly justified
   (both by the supersedes-tense rule and by the fact that emptying can
   never actually take shape (c)'s form anyway). Not a contradiction, if
   anything an over-defended (safe) restatement.

5. **Exhaustive claims.** None of concern.

6. **Unconstrained neighbors.** N/A.

7. **Analogy.** None.

8. **Back-reference.** "as in (b)" at the very end of the Example
   (unchanged, line 3330-3331, "so a new extent is appended and the old
   one becomes slack, as in (b)") — checked this still resolves to
   shape (b) two paragraphs earlier in the same Example, unaffected by
   this hunk's insertion (the insertion sits entirely within shape (c)'s
   own paragraph, before the "Editing user metadata" sentence, not between
   "(b)" and its reference). Confirmed unaffected.

**Verdict on hunk-06: no defect found.** Correct, faithful propagation of
an already-established rule into the illustrative Example, properly kept
non-normative.

## Rejected candidates

1. *"A channel's tiles move exactly when its index does"* read as a
   universal iff regardless of what else a commit does (e.g., a
   simultaneous extent growth that also moves spatial ordinal *s*).
   Closed by: the paragraph's own topic sentence two sentences earlier
   ("For a **planar** layer, a commit MUST NOT change the channel
   declarations...") scopes "moves" to channel-declaration-driven moves;
   extent-driven ordinal moves are a different, separately-governed
   mechanism (line 3127, and §11.1's growth/shrink Rationale) that this
   paragraph never claims to describe. Not reported as a finding.

2. *§21.7's "companion bar" witness discussion (line 3944-3959,
   pre-existing, not part of any hunk I was given) only illustrates the
   ordinal bar via "a permutation among channels," never mentioning
   insert/remove even though the normative bar (as now worded) explicitly
   covers insert/remove too.* I considered reporting this as a full
   contradiction and instead down-graded it: the sentence at line 3896-3897
   ("That is the whole of the test, and it decides any condition put to it
   without appeal to a list") explicitly disclaims that the walkthrough's
   examples are an exhaustive enumeration, and I checked that insert/remove
   have the same "no check knows which ordinal a stored tile used to
   occupy" witness-blindness as permutation does (both are invisible from
   a single resulting file, for the identical reason: prior-generation
   declarations aren't part of live state, §9.7). Reported below as a
   lower-confidence, non-byte-level UNSWEPT_RESTATEMENT finding (C-02)
   rather than withdrawn entirely, because the *charter* explicitly asks
   me to search for exactly this shape of gap and I think it's real enough
   to flag even though I don't believe it changes any conformance verdict.

3. *"0x80 denotes -128 as int8 and 128 as uint8"* — checked the arithmetic
   by hand (two's complement of 10000000b = -128; unsigned = 128). Correct,
   not a finding.

4. *Whether "sample type" belongs in the §14 bar's list at all, given §14
   itself doesn't "declare" sample types (§12 does)* — considered
   reporting under check 3 (label/scope), rejected: the governing stem is
   "what §14 fixes for its stored bytes **or how they decode**," and sample
   type is inseparable from "how [bytes] decode" throughout §14.2's own
   arithmetic (element size Bᶜ derives from it). Not a finding.

5. *Whether hunk-03's per-channel storedness carve-out ("or a planar
   channel none of whose own tiles are stored") wrongly extends the same
   freedom to interleaved layers* — checked: the sentence explicitly
   restricts this specific carve-out to "planar," and does not claim it
   for interleaved. For interleaved, a single stored tile carries every
   channel (§14.1, §3.2), so per-channel retyping freedom while other
   tiles remain stored is correctly *not* extended there. Not a finding.

## Findings summary

- **C-01** (primary, byte-level): the new ordinal bar's own justification
  — that channel-declaration edits are not "geometry changes" and so fall
  outside the pre-existing renumbering permission at line 3127 — is
  contradicted by the document's own classification of channel count as a
  "layer geometry field" (L32, line 3720) and by §11.1's title/rule
  bundling channel-count's floor into "Geometry and its validity floor"
  (R-GEO-01). R-GEO-06, the rule the pre-existing permission cites by
  name, has the channel index *c* as a term in its own formula. This
  creates genuine textual support for reading the untouched line-3127
  parenthetical as already licensing exactly the channel-index-driven
  ordinal moves (specifically: insert-not-at-end, remove-not-last) that
  the new MUST NOT now forbids for a planar layer's previously-stored
  tiles — a live conflict between an unmodified permissive clause and a
  newly-added prohibition over the same act.

- **C-02** (secondary, not byte-level): §21.7's pre-existing "companion
  bar" witness discussion illustrates the ordinal bar using only
  channel-permutation language, and was not sweept to also mention
  insert/remove now that the bar's own wording explicitly covers those
  too. Lower confidence; likely harmless given §21.7's own
  non-exhaustiveness disclaimer, but worth a maintainer's look.

## Confidence / what an empty result would have meant

I did not return an empty list. Where I found nothing (hunks 04, 05, 06,
and part A of hunk 03), I ran all eight checks explicitly and recorded, for
each, what I checked and why it passed — see the per-hunk sections above,
each of which states a concrete result for checks 1-8 rather than a bare
"looks fine." For hunk-02 and part A of hunk-03, the strongest available
counter-evidence I could construct (overreach of "sample type" past what
§14 "fixes," a dangling anaphor in the growth clause, a false per-channel
carve-out) is recorded under "Rejected candidates" with the specific text
that closed each.
