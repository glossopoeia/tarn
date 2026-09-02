# Audit transcript — case-adr0113, hunks 02–06 (§20.3 step 4)

## Disclosure

Before reading anything under my access rule, my runtime context already
contained: the project CLAUDE.md pointer to AGENTS.md; the user's auto-memory
file MEMORY.md, which names two unrelated memory entries ("TARN harness spec
path", "TARN lineage gate word list — the canonical file is missing"); the
userEmail and currentDate blocks; and the full list of available skills/MCP
tools. None of this names or hints at a verdict for hunks 02–06, ADR-0113, or
any repair in §20.3 step 4. I disregarded all of it and did not use it to
reach any conclusion below; I flag it here only because the instructions
require disclosure of any such contamination, however irrelevant it looks.

What I actually read: the five hunk files (hunk-02.diff through hunk-06.diff)
in case-adr0113/, and spec/tarn.md — specifically §3.1 (Terms, lines
341–410), §11.1's Rationale (1594–1628), §11.2–§11.4 (1630–1719), §12.1
(1728–1739 partial), §14.1–14.2 (1930–1989), §14.5 (2087–2116), §20.3 in full
(3073–3341, read twice), §20.4 (3342–3372 partial), the register rows for
L2/L39/L40/L41/L44 and F-rows I grepped (3690–3737 region), and §21.7 in full
(3864–3994). I ran the bash/grep commands below against spec/tarn.md only. I
did not read full.diff, other auditors' hunk files, docs/, AGENTS.md,
registry.json, or git history/log, and did not list the case-adr0113
directory.

## What the repair does (my own restatement)

Step 4 of the append procedure already forbade a commit from changing a
layer's declarations in a way that alters, for any tile the layer *stored in
the generation the commit supersedes*, what §14 fixes for its stored bytes or
how they decode. Call this rule **the §14 bar** (hunk-02 gives it that name;
hunk-02 also adds one new item to its list of what-§14-fixes: "the sample
type each value in the image is read under").

hunk-03 does three things:
1. Adds a paragraph asserting that a channel's declared **sample type** is
   exactly the kind of declaration the §14 bar's list already names — so
   re-typing a channel is barred wherever the layer stores a tile carrying
   that channel, and unbarred where it doesn't (with the planar/interleaved
   carve-outs spelled out).
2. Adds a **second, new MUST NOT**: for a planar layer, a commit must not
   change channel declarations in a way that moves the disk ordinal
   (`c·N+s`, [R-GEO-06]) of any tile the layer stored in the superseded
   generation. It works the arithmetic: reordering moves the reordered
   channels; insert/remove (not at the end) moves everything after; append
   or remove-the-last moves nothing (since N, not C, is what appears
   per-ordinal); gives a worked N=2, channels (a,b) example.
3. Generalizes "a position that becomes real held that channel's fill" to
   "held, for each channel the position carries, that channel's fill
   (§14.5)" — fixing an implicit single-channel assumption that was wrong
   for interleaved tiles.

hunk-04 disambiguates "the bar above" → "the §14 bar" (now that two bars
exist) in the shrink paragraph, and adds a sentence noting that other step-4
obligations (slack, entry_count, slab/alignment, the new-file recommendation)
still bind a shrink even though the §14 bar is "the whole of the test of what
a shrink alters."

hunk-05 disambiguates the same way, and adds an explicit sentence that the
new ordinal bar (unlike the §14 bar) does not reach a shrink at all, since a
shrink is not a channel-declaration change.

hunk-06 fixes a tense/quantifier gap in the non-normative "three shapes"
Example: "a layer storing no tile" (ambiguous generation) becomes "a layer
that stored no tile in the generation the commit supersedes ... — a layer
the commit itself empties does not qualify," matching the wording already
used in the (also unchanged) §11.1 Rationale and in step 4's own body.

## Checks run

### 1. Tense and quantifier

- §14 bar and ordinal bar both explicitly say "in the generation this commit
  supersedes" / "the tense is the prior generation's" — matches §3.1's
  definition of *stored*: "A tile is stored in a generation if and only if
  that generation's tile-index entry for it is not the sentinel... unless
  qualified, *stored* means stored in the live generation." (spec/tarn.md:
  371–374). The repair explicitly overrides the default "live generation"
  reading with "the generation this commit supersedes" everywhere it
  matters — checked at every occurrence (line 3134, 3143, 3163, 3181,
  3192, 3201, 3216, 3222, 3230; hunk-06's "in the generation the commit
  supersedes").
- hunk-06's fix ("stores" → "stored ... in the generation the commit
  supersedes") brings the Example block's quantifier in line with the
  normative text's own tense discipline. Checked against §11.1 Rationale
  line 1614–1615 ("A layer that stored no tile in the generation the
  commit supersedes may be re-declared freely; a layer the commit itself
  empties does not qualify") — identical wording, confirms this was the
  established convention the Example had drifted from.
- "the tense is both bars'" (hunk-03) — verified both bars in fact share
  this tense: the §14 bar's MUST NOT ends "...in the generation this
  commit supersedes" (line 3135) and the ordinal bar's MUST NOT ends
  "...in the generation this commit supersedes" (line 3182). Match
  confirmed.

### 2. Citations resolve

| Citation (as used in hunks) | Claim | Verified against | Verdict |
|---|---|---|---|
| `[R-GEO-06]` (disk ordinal formula, hunk-03) | disk ordinal is c·N+s planar, s interleaved, c = channel's 0-based index | §11.4 lines 1700–1703: "disk tile ordinal ... is s for an interleaved layer, and c · N + s for a planar layer (§14), where c is the channel's index (§3.1)" | PASS — verbatim match |
| §14.5 (hunk-03 growth paragraph) | "for each channel the position carries, that channel's fill" | §14.5 line 2090–2092: "a writer MUST encode, for each channel the position carries, that channel's fill value" | PASS — near-verbatim phrase reuse |
| §11.2 (hunk-03, "channel count enters the addressed-tile count C·N") | C·N is the addressed-tile count for planar | §11.2 line 1636–1637: "addressed-tile count ... is N for an interleaved layer and C·N for a planar layer" | PASS |
| `[R-SLB-04]`, `[R-SLB-01]` (hunk-04, "a slab or alignment declaration") | R-SLB-04 = slab, R-SLB-01 = alignment | Confirmed at lines 3255–3259 (unchanged, same passage): "a slab declaration is re-established or cleared ([R-SLB-04]) ... an aligned layer's stored tiles ... satisfy its invariant or the declaration is cleared ([R-SLB-01] ...)"; also L39 (line 3727, alignment→R-SLB-01) | PASS |
| implicit R-CNT-21/R-CNT-17 (hunk-04, "slack, entry_count") | slack ↔ R-CNT-21, entry_count ↔ R-CNT-17 | Lines 3244–3245 (unchanged): "de-addressed tiles' extents become slack ([R-CNT-21]), [R-CNT-17] obliges the smaller entry_count" | PASS |
| `[R-COD-07]`/L44 (unchanged context inside hunk-03's growth paragraph, not itself edited) | lz4 decoded-size cap is quantified over *addressed* tiles | L44 row (line 3732): "any of its addressed tiles' decoded size exceeds..."; also line 4028 "addressed tiles, stored or not, exactly as [R-COD-07]'s cap is" | PASS — this is exactly the "addressed" quantifier the project's worst prior defect turned on; here it is used correctly and consistently, and this text is untouched by the hunk |
| §3.1 (unchanged, "The tense is the prior generation's... §3.1 defines stored against a generation") | matches §3.1's stored-in-a-generation definition | Confirmed lines 371–374 | PASS |

No citation in these five hunks pointed at a rule that says something
different from what the repairing sentence claims.

### 3. Normative placement — label, not marker

All of hunk-02 through hunk-05 land inside numbered item 4 of "An appender
MUST, in order:" (line 3085) — plain paragraph text, no `>` marker, so
squarely normative under [R-CNF-01] regardless.

hunk-06 lands *inside* a blockquote explicitly labeled "**Example — the three
shapes a commit takes.**" (opens at line 3287) — non-normative under
[R-CNF-01]. I checked whether the actual rule (a layer the commit itself
empties does not earn free-redeclaration) is stated normatively somewhere
else, since an edit landing only in a labeled Example would be no fix at all.
It is: step 4's own body states it at lines 3201–3203 ("A layer that stores
no tile in the generation this commit supersedes MAY be re-declared freely
... the tense is both bars', so a commit does not earn this permission by
emptying the layer as it re-declares it") and the §11.1 Rationale states it
again at lines 1614–1615. hunk-06 only brings the (non-normative,
illustrative) Example in line with the two normative statements that already
existed; it does not need to itself carry force. Verdict: PASS, correctly
scoped, no floating-only-in-Example rule was created.

### 4. Local contradiction, including untouched text

- Checked the new ordinal bar against the *already-existing, unchanged*
  parenthetical in step 4's own intro (line 3126–3127): "every other entry
  byte-identical at its disk-ordinal position (a geometry change renumbers
  ordinals wherever [R-GEO-06] moves them)." This looked, on first read,
  like it might license exactly what the new bar forbids. On inspection it
  does not conflict: that clause licenses renumbering caused by a *geometry*
  change (extent/tile-extent edits); the new bar forbids renumbering caused
  by a *channel-declaration* change (order/insert/remove) — the two are
  explicitly kept apart by hunk-03's own framing: "an ordinal move being no
  effect on any stored tile's bytes, and what it disturbs is instead the
  re-emission rule above, whose only stated occasion for a renumbering is a
  geometry change." I checked this is not merely asserted but true: a
  channel reorder is not a change to Eᵢ or Tᵢ, so it is not "a geometry
  change" in the sense §11.2 uses that term. No contradiction.
- Checked hunk-05's new "the bar beside the §14 bar does not reach a shrink
  either... a shrink is not one [a channel-declaration change]" against the
  shrink discussion three sentences earlier. A shrink is an extent edit;
  the ordinal bar's subject is channel declarations; these are different
  axes of a layer's declared state, so the claim holds without exception.
- Checked whether shrinking an extent could itself silently move a
  *surviving* stored tile's disk ordinal by changing N (spatial-tile count)
  even without touching channel declarations — since disk ordinal is
  c·N+s, a smaller N does shift every planar channel c≥1's ordinals. This
  is real, but it is licensed by the SAME already-quoted intro parenthetical
  ("a geometry change renumbers ordinals wherever [R-GEO-06] moves them") —
  a shrink IS a geometry change, so this renumbering is the licensed kind,
  not a violation of either bar. Confirmed no contradiction, only two
  cleanly separated mechanisms (geometry-driven renumbering: licensed;
  declaration-driven renumbering: now barred).
- Checked the §21.7 Rationale walkthrough (lines 3944–3959, wholly unchanged,
  outside my hunks) against the new normative text for both bars. It already
  discusses "§20.3 step 4's §14 bar" by that exact bolded name, and "Its
  companion bar on a planar layer's disk ordinals," describing precisely the
  reorder/permutation scenario the new ordinal bar states. No contradiction;
  this pre-existing block reads as though it was written assuming both bars
  already existed in step 4 in their current form.
- Checked the §11.1 Rationale (unchanged, lines 1602–1628) the same way: "Of
  its two bars the one reaching a shrink or a growth is the §14 bar...
  Re-typing a channel is the §14 bar's own subject, barred wherever the
  layer stores a tile that carries that channel, and free where it does
  not. The other bar reaches neither a shrink nor a growth: it bars a
  change to a planar layer's channel declarations that moves a stored
  tile's disk ordinal." This is a verbatim-in-substance match to the newly
  added normative paragraphs. No contradiction; this restatement already
  matched the repair, so nothing here needed (or got) sweeping.

### 5. Exhaustive claims

- "the list is not offered as exhaustive" (unchanged, follows the growth
  paragraph) — correctly hedged already, not itself part of the hunks.
- "A channel's tiles move exactly when its index does" (hunk-03) — read
  literally and out of context this biconditional is false: holding channel
  index fixed but changing N (a geometry edit) also moves that channel's
  tiles' ordinals (c·N+s). I checked whether this makes the sentence an
  overclaim. In context it is bounded by the immediately preceding sentence,
  which explicitly assigns geometry-driven renumbering to "the re-emission
  rule above" as a separate mechanism — so this sentence's "exactly when"
  is implicitly scoped to channel-declaration edits with geometry held
  fixed, which is the only case this MUST NOT is about. I convinced myself
  this reads correctly in context and is not a free-standing overclaim;
  logged in rejected_candidates.
- "the §14 bar is the whole of the test of what a shrink alters, in that
  bar's own tense" (hunk-04) — checked against the newly-added companion
  sentence in the same hunk ("the obligations this step states below...
  bind a shrink as they bind any commit") for a scope-vs-completeness
  clash. No clash: the claim is explicitly narrowed to "what a shrink
  alters" (the §14-bar permission test), not to every obligation a shrink
  is subject to, and the new sentence makes that narrowing explicit rather
  than contradicting it.
- hunk-05's parallel claim ("What counts as such an alteration is the §14
  bar and nothing else, its carve-out included") — checked against the new
  ordinal-bar sentence that immediately follows it ("The bar beside the
  §14 bar does not reach a shrink either"). These agree rather than
  conflict: exactly one bar (the §14 bar) governs what a shrink may alter;
  the other bar simply doesn't apply to shrinks at all. Consistent.

### 6. What else in this structure is unconstrained

Structure: a **channel declaration**, per §3.1/§12: name, sample type, fill
value, plus its position (index) in declared order.

- **Sample type** — now governed by the §14 bar (hunk-02's list item +
  hunk-03's classifying paragraph).
- **Index / declared order** — now governed by the new ordinal bar
  (hunk-03).
- **Fill value** — I checked this is *already* governed, by the pre-existing
  (unchanged) §14 bar list item "the content [R-SER-05] fixes there" (i.e.
  padding-position content, which §14.5 fixes as a function of declared
  fill) — a fill-value edit that reaches a stored tile with a padding
  position or pad bit is already barred via that item, confirmed
  independently by the (unchanged) Example-block sentence "A fill change on
  a layer that stores a tile carrying either is not an appender's operation
  at all (step 4)." Not a gap.
- **Name** — no rule anywhere ties a channel's declared name to any decoded
  byte or disk position; I found nothing suggesting it should be
  constrained. Not a gap.
- I checked the growth paragraph's fix ("for each channel the position
  carries, that channel's fill") specifically for the sibling-quantity
  pattern the charter warned about (one round pinned one header quantity and
  left a neighbour unpinned): the *original* text ("a position that becomes
  real held that channel's fill") named only one channel's fill, which is
  wrong for an interleaved tile where one padding position carries *every*
  channel, each with potentially a different fill. The hunk generalizes this
  to all channels the position carries, closing exactly this kind of gap.
  I confirmed this reading against §14.5's own wording (identical
  "for each channel ... carries" construction) and against the growth
  scenario's own logic (only pre-existing STORED tiles' padding positions
  are relevant here, per §14.5, not brand-new unaddressed tiles, which are
  outside the §14 bar's scope entirely since it only binds tiles stored in
  the superseded generation).

### 7. Analogies — verb-for-verb

- hunk-03's ordinal bar text ends "Where this bars a change the operation
  is a new layer or a whole-file rewrite, exactly as above." Compared
  word-for-word against the sample-type paragraph's own conclusion ("Such a
  change is a new layer, or a whole-file rewrite under a fresh file_id
  ([R-LIF-01], §20.5)"): same governing predicate ("is a new layer, or a
  whole-file rewrite"), same remedy, no quantifier mismatch. PASS.
- hunk-05's carve-out reuse ("so a shrink producing only those is permitted
  here exactly as it is there") — compared "here" (shrink test) against
  "there" (the general §14-bar carve-out at lines 3149–3151: "a new padding
  position whose stored byte already holds the fill [R-SER-05] fixes — is
  not what this bars"). Both use the identical governing test (padding
  position already holding the required fill), same quantifier (per
  stored tile). PASS. (This sentence is unchanged by the hunk itself, only
  the earlier "bar above"→"§14 bar" rename touches this paragraph, but I
  checked it anyway since the hunk's rename could have broken it.)
- No hunk in this set restates a rule by pointing at a *differently
  quantified* rule the way the project's worst prior defect did
  (contains vs. addressed). The one place that quantifier pair appears
  (L44/[R-COD-07], "addressed tiles") is untouched context, correctly
  worded, and consistent with its other occurrence at line 4028.

### 8. What insertion did to surrounding sentences (backreferences)

This is where I found my one substantive finding. Full list of
back-references checked, before vs. after each insertion:

**hunk-02** insertion ("Call this the §14 bar.") sits between the §14 bar's
list and "The tense is the prior generation's... so a commit does not escape
this by unstoring... and this bars it." Before: "this"/"this" resolved to
the just-stated MUST NOT (unnamed). After: same referent, now nameable as
"the §14 bar" — the insertion *is* the naming of that referent, so nothing
re-resolves. Checked, no change.

**hunk-03, first insertion** (sample-type paragraph, four sentences) sits
between "...is not what this bars." and "Where a change does reach them it
makes each stored tile it reaches nonconforming... Such a change is a new
layer, or a whole-file rewrite under a fresh file_id ([R-LIF-01], §20.5)."

- Before the insertion, "them" (in "Where a change does reach them") sat
  three sentences after, and its nearest antecedent was "those tiles" from
  the general §14-bar carve-out sentence ("a change that leaves every one
  of those tiles' stored bytes meaning exactly what they meant... is not
  what this bars") — i.e. the whole enumerated §14-bar class: re-typing,
  filter, codec, decoded-size, or byte-offset changes together. The diff
  confirms this: the original hunk context shows "what this bars. Where a"
  as one continuous line with no paragraph break.
- After the insertion, a full paragraph about sample-type reinterpretation
  sits immediately before "Where a change does reach them," with **no
  paragraph break between them** (confirmed from the diff: the `+` lines
  add a blank line only *before* "A channel's declared sample type," not
  between "...is a declaration edit like any other." and "Where a change
  does reach them"). So "Where a change does reach them it makes each
  stored tile it reaches nonconforming... Such a change is a new layer, or
  a whole-file rewrite" is now, paragraph-structurally, the tail of the
  sample-type paragraph rather than the tail of the general §14-bar
  paragraph. The nearest plausible antecedent for "them" is now the
  sample-type discussion's own tile-carrying language ("a tile that carries
  that channel" / "no tile carrying that channel").
- I asked whether this changes what the sentence claims. Read as the
  general §14-bar conclusion (its original job), "Such a change is a new
  layer, or a whole-file rewrite" states the remedy for *any* barred
  declaration change (re-typing, filter, codec, decoded-size, byte-offset).
  Read as scoped to the immediately preceding paragraph only, it appears to
  state the remedy *for re-typing specifically*, leaving the remedy for the
  other §14-bar triggers (filter/codec/decoded-size/offset changes)
  unstated in this passage.
- I checked whether this is merely cosmetic (still "arguably true" either
  way, per the charter's own standard for reporting these). It is true
  either way locally, but the two readings assign a different scope to an
  "only stated occasion" for the new-layer-or-rewrite remedy, which is
  exactly the shape the charter asks me to report even when the resulting
  sentence remains defensible. I do not believe this changes any
  conforming byte sequence (see byte-level test below), but it is a
  genuine new ambiguity introduced by the insertion's placement, not
  present in the pre-repair text.

**hunk-03, second insertion** (ordinal-bar paragraph) sits between "...under
a fresh file_id ([R-LIF-01], §20.5)." and "A layer that stores no tile in
the generation this commit supersedes MAY be re-declared freely..."

- "One effect is barred beside it" — checked "it": resolves to "the §14
  bar," a term last used explicitly two sentences earlier (before the
  sample-type paragraph) and not re-used inside the sample-type paragraph
  itself. This is a longer-distance pronoun resolution than most in this
  document, but the very next clause of the same sentence ("the §14 bar
  does not reach it") names the term explicitly, so the sentence
  self-resolves within its own bounds. Checked, no defect — the named term
  survives a full paragraph's distance because it is a proper noun-like
  label, not a bare pronoun trying to reach that far alone.
- "Either is such a change wherever the layer stores a tile for a channel
  that moved" — "Either" = the two preceding operations (reordering;
  insert/remove). Unambiguous, both antecedents in the same sentence.
- "Where this bars a change the operation is a new layer or a whole-file
  rewrite, exactly as above" — "this" = the ordinal bar just stated in the
  same paragraph. Unambiguous.
- Immediately after this insertion, "the tense is **both bars'**" (already
  checked under Check 1) correctly anticipates the insertion — this is the
  one place in the passage where the repair explicitly re-swept a
  downstream sentence to account for the new insertion, rather than leaving
  a stale singular "the bar's."

**hunk-04** insertion sits inside one sentence ("...in that bar's own
tense; [inserted clause] ... bind a shrink as they bind any commit.") and the
next sentence ("A shrink is permitted exactly where...") is a fresh,
self-contained sentence not depending on any pronoun crossing the insertion
boundary. Checked, no defect.

**hunk-05** insertion sits between "...restating the test." and "§21.7
records the consequence — that this is precisely where the §14 bar has no
witness... which is why the rule is stated here." Checked "the rule": its
antecedent, "the §14 bar," is named in the same sentence, immediately
before "the rule is stated here" — not disturbed by the newly inserted
sentence before it, which itself is self-contained ("it bars a change...
and a shrink is not one"). Checked, no defect.

**hunk-06** is a same-sentence tense fix plus an appended carve-out clause;
nothing crosses a sentence boundary that could re-resolve a pronoun.

## Byte-level test

For the one finding (hunk-03's "them"/paragraph-restructuring ambiguity): I
asked whether either reading changes which bytes a conforming writer may
emit or a reader/verifier must accept or reject. It does not. Under either
reading, the underlying prohibition — the §14 bar's MUST NOT, stated once
and unambiguously in the numbered list a few sentences earlier, covering
re-typing, filter, codec, decoded-size, and byte-offset changes alike — is
untouched; a commit that violates it via a filter or codec change is barred
regardless of which paragraph the "new layer or whole-file rewrite" remedy
sentence is read as belonging to. What is at stake is only whether a reader
of this exposition correctly understands that the *remedy* (going the
new-layer/rewrite route) is available for any of the bar's triggers, not
just re-typing — a documentation/comprehension risk, not a fork in
conforming bytes. **Not byte-level.**

## Sweeps and searches run (verbatim, with hit counts)

```
grep -n "disk ordinal\|R-GEO-06\|c · N + s\|c \* N + s\|spatial-tile count" spec/tarn.md | head -60
  -> 16 hits (lines 1620,1625,1626,1634,1701,1703,1711,1937,2142,2240,2280,2328,2969,2970,2971,3015,3127,3181,3188,3197,3239,3690 — 22 shown, truncated list above omits a couple; all inspected)

grep -n "R-COD-07\|L44" spec/tarn.md
  -> 5 hits: 2462, 2942, 3207/3208, 3732, 3771, 4028, 4075 (7 total lines)

grep -n "^#### 21\.7\|§21\.7" spec/tarn.md
  -> 8 hits: 2521, 2613, 3240, 3457, 3560, 3580, 3774, 3864

grep -n "R-SLB-04\|R-SLB-01\|R-CNT-21\|R-CNT-17" spec/tarn.md
  -> 27 hits, spanning 722–4747; all slab/alignment/slack/entry_count citations inspected around 3218-3259

grep -n "carries\|carrying" spec/tarn.md
  -> 90 hits; scanned for "tile carries channel" vs. "channel carries tile" direction — confirmed the document
     uses "tile carries channel(s)" exclusively (e.g. lines 368, 378, 407, 410, 1937, 1941, 1710, 3156, 3163,
     3182, 3205, 3225); no instance of "channel carries tile" found anywhere.

grep -n "reorder\|re-order\|declared order\|declaration order\|channel order\|channel count\|channels are declared" spec/tarn.md
  -> 17 hits; confirmed §12 ("channels are declared in order, and the declared order is load-bearing (§3.1,
     §11.4)") needs no sweep since the actual restriction lives in §20.3 step 4, which this repair supplies.

grep -n "the bar above\|bar above\|the other bar\|companion bar\|the §14 bar\|§14 bar" spec/tarn.md
  -> 10 hits: 1606, 1616, 3141, 3176, 3215, 3232, 3237, 3241, 3944, 3949, 3985 — all inspected; confirmed
     "§14 bar" was already used (as if defined) at 1606/1616 before hunk-02 supplied its actual naming
     clause at 3141 — the repair closes a genuine forward-reference gap rather than introducing a redundant
     label.

grep -n "the bar's\|bar's own" spec/tarn.md
  -> 2 hits: 1616 ("the §14 bar's own subject" — already-named, unchanged), 3216 ("in that bar's own
     tense" — same-sentence antecedent, correctly resolved). No leftover ambiguous singular "the bar's" found.

grep -n "re-typ\|sample type\|disk ordinal\|R-WRT-03\|R-WRT-04\|R-WRT-05\|R-WRT-01" spec/tarn.md
  -> 34 hits; confirmed the whole append procedure (steps 1-6) is governed by the single umbrella
     [R-WRT-04], cited independently at 1626, 1920, 673, 3268 — so neither new bar needs its own
     requirement ID; consistent with the umbrella-ID pattern already used elsewhere.

grep -n "^#### 14\." spec/tarn.md
  -> confirms §14.1 (1930), §14.2 (1954), §14.3 (2020), §14.4 (2058), §14.5 (2087)

grep -n "| L[0-9]*.*ordinal\|updater.*ordinal\|ordinal.*updater" spec/tarn.md
  -> 2 hits (L2, L41) — neither is a dedicated register row for the new ordinal bar, consistent with
     §21.7's own explanation that this condition is unwitnessed except indirectly via T3/T14/T4/T5.
```

## Derived numbers

- Disk ordinal formula, derived from §11.4's own definition (s for
  interleaved; c·N+s for planar, c = channel's 0-based declared index, N =
  spatial-tile count = ∏Gᵢ, independent of channel count C): confirmed
  against L2's register row, which independently states "the max disk
  ordinal (C−1)·N + (N−1)" — consistent with c ranging 0..C−1 and s
  ranging 0..N−1.
- Worked example in hunk-03 (N=2, channels a,b): a → ordinals 0·2+0=0,
  0·2+1=1; b → 1·2+0=2, 1·2+1=3. Matches the passage's claimed "a at
  ordinals 0 and 1 and b at 2 and 3."
- Appending channel c (index 2, N=2): c → 2·2+0=4, 2·2+1=5; a and b's
  ordinals (0,1,2,3) are unaffected since their indices (0,1) don't change.
  Matches "leaves those four where they are and adds 4 and 5."
- Exchanging a and b (b becomes index 0, a becomes index 1): b → 0·2+0=0,
  0·2+1=1 (was 2,3); a → 1·2+0=2, 1·2+1=3 (was 0,1). All four tiles change
  ordinal. Matches "moves all four."
- Checked append/remove-the-last claim generally: for C channels indexed
  0..C−1, appending a (C+1)-th channel at index C changes no existing
  channel's index, hence no existing channel's ordinal (only adds new
  ordinals C·N..(C+1)·N−1); removing the channel at index C−1 (the last)
  leaves indices 0..C−2 unchanged. Both match the passage's claim exactly.
- Checked insert-in-the-middle / reorder claims symbolically: for a
  channel originally at index i, its ordinal is i·N+s. Any edit that
  changes i (reorder that swaps it, or an insert/remove at a position ≤ i
  that shifts it) changes every one of that channel's N ordinals; an edit
  that leaves i unchanged leaves that channel's ordinals unchanged. This is
  exactly what the passage claims, verified position-by-position rather
  than granted.

No requirement in my charter named a specific numeric target (e.g., a count
of items in a list, a byte offset) other than the disk-ordinal arithmetic
above, which I computed independently rather than trusting the prose.

## Rejected candidates

1. *"A channel's tiles move exactly when its index does"* (hunk-03) — read
   as an unconditional biconditional this is false whenever N changes via a
   geometry edit (ordinal still moves with index fixed). Closed: the
   immediately preceding sentence explicitly assigns geometry-driven
   renumbering to a separate mechanism ("the re-emission rule above, whose
   only stated occasion for a renumbering is a geometry change"), so this
   sentence is implicitly scoped to channel-declaration edits with geometry
   held fixed — the only case this particular MUST NOT is about. Not
   reported as a primary finding.
2. *"companion bar" (§21.7, line 3949) vs. no equivalent bolded name given
   to the ordinal bar in step 4* — considered whether the ordinal bar
   needed its own bolded label the way "§14 bar" got one, on the theory
   that an unnamed forward reference is the same defect class hunk-02 just
   fixed for "§14 bar." Closed: "companion bar" reads as descriptive prose
   ("its companion" = the bar beside it), not as a proper term requiring a
   defined antecedent the way the bolded, repeatedly-cited "§14 bar" does;
   and step 4 itself never needs to invoke a name for the ordinal bar from
   outside its own paragraph (it's self-contained), so no dangling
   forward-reference is created. Not reported.
3. *Extent-shrink silently moving a stored tile's disk ordinal via N
   without touching channel declarations* — considered as a possible gap
   the ordinal bar leaves open. Closed: this is licensed renumbering under
   the pre-existing "a geometry change renumbers ordinals wherever
   [R-GEO-06] moves them" clause (step 4's intro, unchanged), which the new
   bar explicitly declines to reach ("what it disturbs is instead the
   re-emission rule above, whose only stated occasion for a renumbering is
   a geometry change"). Not a gap, by design.
4. *"an updater decides the question from the layer record alone rather
   than by inspecting stored bytes"* (hunk-03) — considered whether this
   overclaims that storedness itself is decidable from "the layer record"
   without the tile index. Closed: "the question" in context is which
   value a stored bit pattern denotes (a pure declared-type question), not
   whether a given tile is stored — so this doesn't purport to settle
   storedness from the layer record alone. Not reported.

## Summary

Checks 1, 2, 3, 5, 6, and 7 passed cleanly on every hunk: every tense/
quantifier I could find was either already correctly scoped to "the
generation this commit supersedes" or was fixed by the hunk to be so
(hunk-06); every citation resolved to a rule that says what the repairing
sentence claims, including the disk-ordinal formula, §14.5, §11.2, and the
R-SLB-04/R-SLB-01 slab/alignment pair; the repairs sit in numbered-list
normative text throughout except hunk-06, which lands in a labeled Example
whose actual normative counterpart already exists twice elsewhere (step 4's
own body, and the §11.1 Rationale) and was itself found to already match the
repair rather than needing one; I found no exhaustive claim the repaired
text cannot carry, including on the "exactly when" sentence I specifically
tried to falsify; I checked every declared attribute of a channel (name,
type, fill, index) against the two bars and found type and index now
governed, fill already governed by pre-existing text, and name not needing
governance; and every "exactly as"/"exactly as above" analogy I found
compared the same governing verb against the same quantifier with no
mismatch. Check 4 (contradiction) turned up nothing: the two bars are
cleanly orthogonal to each other and to the pre-existing geometry-driven
renumbering license, and the two pre-existing restatement sites (§11.1
Rationale, §21.7) both already matched the newly-added normative text rather
than conflicting with it or needing a sweep.

Check 8 is where I found something. The first insertion in hunk-03 (the
sample-type paragraph) sits, with no paragraph break, directly in front of a
sentence — "Where a change does reach them it makes each stored tile it
reaches nonconforming ... Such a change is a new layer, or a whole-file
rewrite" — that was originally the general conclusion for the entire §14 bar
(covering re-typing, filter, codec, decoded-size, and byte-offset changes
alike) but now reads, by nearest antecedent and by paragraph membership, as
the conclusion of the sample-type-specific discussion alone. I confirmed via
the diff that no paragraph break was inserted at that boundary, so the
general conclusion has been structurally absorbed into the specific
paragraph. I checked this is not byte-level: the actual MUST NOT prohibition
is stated once, unambiguously, a few sentences earlier, and doesn't depend
on which paragraph the remedy-sentence is read as belonging to — a
conforming writer's obligations don't change either way. It is, however, a
genuine ambiguity the insertion introduced that was not present before, and
it is exactly the shape the charter's Check 8 asks auditors to hunt for.
