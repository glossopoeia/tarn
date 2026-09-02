# Audit transcript — downstream accounts of §20.3 step 4
# Lane: hunks 01, 03, 04, 05, 06. Auditor: repair auditor, fresh context.

## 0. Disclosure

Files opened:
- /private/tmp/.../case-adr0113/hunk-01.diff, hunk-03.diff, hunk-04.diff,
  hunk-05.diff, hunk-06.diff  (my charter's hunks, and only those)
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md

Not opened: full.diff, hunk-02, hunk-07, hunk-08, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json,
git history, the web. I did not list the case directory.

Commands run: `cat` on the five hunk files; `wc -l`, `sed -n`, `awk`, `grep -n`
and three inline python3 whitespace-normalising searches, all against
spec/tarn.md only. `mkdir -p` for the output directory (no read of it).

Unrequested context that appeared before I began: a CLAUDE.md/AGENTS.md pointer
block, a user auto-memory index naming two memory files about this project's
harness and a "lineage gate word list", a scratchpad-directory notice, an MCP
server instruction block, a deferred-tool list, and a skills list. None of it is
part of the specification. I read none of the memory files and used none of it.
It named things that look like answers about this project's rounds; I disregarded
all of it and drew every conclusion below from spec/tarn.md and my hunk files.

## 1. Reading the hunks — what rule each repair adopts

hunk-01 → §11.1, inside a block whose opening words are `> **Rationale.**`
  ([R-CNF-01] line 106: text labeled *Rationale* is non-normative. Test applied:
  the LABEL, not the ">" marker. Label = Rationale ⇒ non-normative.)
  Rule asserted: §20.3 step 4 holds exactly two bars; only one of them (the §14
  bar) can be reached by a shrink or a growth; re-typing a channel is the §14
  bar's subject; the other bar is about a planar layer's channel declarations
  moving a stored tile's disk ordinal; the free-re-declaration permission is
  quantified over the superseded generation, and a commit that empties a layer
  does not earn it.

hunk-03 → §20.3 step 4, no ">" marker, inside the numbered MUST list. Normative.
  Two insertions.
  (a) sample-type paragraph: a channel's declared sample type is a "declaration"
      within the §14 bar's meaning, and re-typing is a barred "change" where a
      tile carrying that channel is stored; the test is on declared types, not on
      stored byte values; where no such tile is stored it bars nothing.
  (b) planar disk-ordinal paragraph: a second MUST NOT — for a planar layer, a
      commit MUST NOT change the channel declarations so as to alter the disk
      ordinal [R-GEO-06] assigns any tile stored in the superseded generation.
      Reordering and mid-list insert/remove move ordinals; appending or removing
      the last does not; interleaved layers are said to be unaffected.
  (c) "the tense is the bar's" → "the tense is both bars'".
  (d) growth clause gains "for each channel the position carries" and "(§14.5)".

hunk-04 → §20.3 step 4, normative. Rule: the §14 bar is the whole of the test of
  what a shrink ALTERS (narrowed from "the whole of the test"), and the step's
  other obligations bind a shrink like any other commit.

hunk-05 → §20.3 step 4, normative. Rule: the second bar does not reach a shrink;
  and "the bar above" is re-pointed to "the §14 bar" twice.

hunk-06 → §20.3, inside `> **Example — the three shapes a commit takes.**`
  Label = Example ⇒ non-normative ([R-CNF-01]). Rule: shape (c)'s free
  re-declaration is quantified over the superseded generation; a layer the commit
  itself empties does not qualify.

## 2. Counting the bars myself

`awk 'NR>=3116 && NR<=3260' spec/tarn.md | grep -o "MUST NOT\|MUST\|SHOULD\|MAY" | sort | uniq -c`
  3 MAY
  2 MUST NOT
  1 SHOULD

The two MUST NOTs in step 4 are at:
  3133  "A commit MUST NOT change a layer's declarations in a way that alters,
         for any tile that layer stores **in the generation this commit
         supersedes**, what §14 fixes ... Call this the **§14 bar**."
  3179  "For a **planar** layer, a commit MUST NOT change the channel
         declarations in a way that alters the disk ordinal `[R-GEO-06]` assigns
         any tile the layer stores in the generation this commit supersedes."

DERIVED COUNT = 2.

The three MAYs are the permissions, not bars: 3200 re-declare freely, 3203 grow,
3214 shrink. The SHOULD at 3247 is the produce-a-new-file recommendation.
(Step 2's "MUST NOT repair the defect" / "MUST NOT drop the record" at 3103-3105
are step 2, not step 4, and are not bars on declaration changes.)

Every statement of the number, checked:
  1606 (hunk-01, Rationale)  "Of its two bars"                  -> 2. CORRECT.
  3202 (hunk-03, normative)  "the tense is both bars'"          -> 2. CORRECT.
  3236 (hunk-05, normative)  "The bar beside the §14 bar"       -> 1 other. CORRECT.
  3901 (§21.7, normative)    "Its companion bar on a planar
                              layer's disk ordinals"            -> 1 other. CORRECT.

Whitespace-normalised phrase counts over the whole file:
  'three bars': 0   'two bars': 1   'both bars': 1   'the bars': 0
  'each bar': 0     'third bar': 0  'companion bar': 1  'bar beside': 1
  '§14 bar': 11
No surviving "three" statement. The count sweep is CLEAN and I say so.

Naming, checked: 1606 names the §14 bar and "the other bar ... a change to a
planar layer's channel declarations that moves a stored tile's disk ordinal";
3236 and 3901 name the same pair. The names match the two MUST NOTs.

Also checked, hunk-01's stronger claim "Of its two bars the one reaching a shrink
or a growth is the §14 bar": the planar bar is scoped to "the channel
declarations". A shrink or growth changes dimension extents, not channel
declarations, so it cannot trip that bar directly. CORRECT. But see B-01 below
for the sentence two lines later.

Minor, recorded and not filed as a finding: "Of **its** two bars" — the nearest
antecedents for "its" are "a commit" and "a layer" in the preceding clause, and
the bars belong to §20.3 **step 4**, not to §20.3 at large (§21.7 gets this right:
"§20.3 step 4's **§14 bar**"). Dangling but recoverable.

## 3. Check 8 — every back-reference around the insertions

### hunk-03 insertion (a), between line 3151 and 3153

Text before the insertion read, continuously:

  "... a new padding position whose stored byte already holds the fill
  `[R-SER-05]` fixes — is not what this bars. Where a change does reach **them**
  it makes each stored tile it reaches nonconforming ..."

"them" BEFORE: the nearest plural antecedent was "those tiles" in "a change that
leaves every one of **those tiles'** stored bytes meaning exactly what they
meant" (3147), which in turn is "such a tile" (3145) = "any tile that layer
stores in the generation this commit supersedes" (3134-3135). Unambiguous.

"them" NOW: a paragraph break and 20 lines of new text intervene. Reading
backwards from "Where a change does reach them" (3165-3166) the candidates are,
nearest first: "stored bytes" ("rather than by inspecting stored bytes", 3161),
"a planar channel none of whose own tiles are stored" (3164-3165, and those
tiles are precisely NOT stored), "the values a tile happens to hold" (3157-3158),
"the declared types" (3157). The original antecedent is now four sentences and a
paragraph boundary away. → CHANGED. Filed as B-05.

Consequence, same sentence chain: "Such a change is a new layer, or a whole-file
rewrite under a fresh file_id" (3171-3172) was the general remedy for any change
the §14 bar reaches; it now sits at the end of a paragraph whose subject is
sample type, so "Such a change" reads as "such a re-typing".

### hunk-03 insertion (b), between 3172 and 3199

Opening: "One effect is barred beside **it**, on the same tense and on its own
ground: the §14 bar does not reach **it** ...".
  First "it" → the §14 bar, last named at 3140 ("Call this the **§14 bar**"),
  32 lines and one whole inserted paragraph earlier. The immediately preceding
  nouns are "a new layer", "a whole-file rewrite", "a fresh file_id".
  Second "it" (four words later) → "One effect", i.e. the ordinal move.
  Two different referents for the same pronoun in one sentence, the first with a
  distant antecedent. Recorded; folded into B-05's discussion, not filed
  separately (the sentence names "the §14 bar" explicitly, which repairs the
  first "it" retroactively for a careful reader).

Forward from the insertion:
  "Where **this** bars a change the operation is a new layer or a whole-file
  rewrite, exactly as **above**." (3197-3199)
    "this" → the planar bar, same paragraph. UNCHANGED/correct.
    "above" → 3171-3172. Resolves. CORRECT.
  "A layer that stores no tile **in the generation this commit supersedes** MAY
  be re-declared freely ... the tense is **both bars'**" (3199-3202)
    Before the insertion this read "the tense is **the bar's**", resolving to the
    §14 bar. After the insertion there are two bars and the repair updated it.
    This is the one re-pointing the repair CAUGHT. CORRECT.
  "an extent MAY **grow**, since a position that becomes real held, for each
  channel the position carries, **that channel's** fill (§14.5)"
    Before: "that channel's fill" with no channel anywhere in the sentence or the
    two before it — dangling. After: "each channel the position carries" supplies
    it. FIXED. See B-08 for the citation.

### hunk-04 insertion, at 3214-3220

  "An extent MAY also **shrink**, and the **§14 bar** is the whole of the test..."
    was "the **bar above** is the whole of the test". "the bar above" would now
    resolve to the nearest preceding bar, which after hunk-03 is the planar
    ordinal bar at 3179. The repair replaced it with an explicit name.
    FIXED — this is the second re-pointing the repair caught.
  "in **that bar's** own tense" → the §14 bar, named three words earlier. CORRECT.
  "the obligations this step states **below**" → all five referents are below:
    [R-CNT-21] 3244/3253, [R-CNT-17] 3245, SHOULD-new-file 3247-3250,
    [R-SLB-04] 3255, [R-SLB-01] 3258. CORRECT.
  "A shrink is permitted exactly where **it** alters nothing" → the shrink.
    CORRECT. But see B-06 for what the sentence now contradicts.

### hunk-05 insertion, at 3236-3239

  "What counts as such an alteration is **the §14 bar** and nothing else"
    was "**the bar above**". Same fix as hunk-04. FIXED.
  Inserted: "The bar beside the §14 bar does not reach a shrink either: it bars a
  change to a planar layer's channel declarations that moves a stored tile's disk
  ordinal, and a shrink is not one."
  Immediately after it, UNTOUCHED:
  "§21.7 records the consequence — that **this** is precisely where the §14 bar
  has no witness, the live state being clean — which is why **the rule** is
  stated here and not left to the rows."
    "this" BEFORE: the rescue case two sentences up — "Unstoring that tile in the
      same commit does not rescue it either" (3226-3227), i.e. a commit that
      supersedes the tile it would have damaged. §21.7 confirms that reading at
      3909-3911: "a commit that supersedes every tile it would have damaged
      ... leaves the live state clean, so the §14 bar is unwitnessed there".
    "this" NOW: the nearest antecedent is the inserted sentence, whose subject is
      a shrink and the OTHER bar — "and a shrink is not one." A reader takes
      "this is precisely where the §14 bar has no witness" to mean "a shrink is",
      which §21.7 does not say and which is false (a shrink that damages a still-
      stored tile is exactly where the rows DO bite). → CHANGED. Filed as B-04.
    "the rule" NOW: nearest "rule" is "the re-emission rule above" (3177),
      further back; intended referent is the shrink test. Degraded, not filed.

### hunk-01 insertion, at 1606

  "... a commit supersedes. Of its two bars the one reaching a shrink or a growth
  is the §14 bar: a shrink is barred wherever it alters what §14 fixes for **such
  a tile**"
    "such a tile" BEFORE: "a layer that already stored tiles in the generation a
      commit supersedes" (1605), reached across a colon.
    "such a tile" NOW: the same, reached across a full stop and one new sentence
      that mentions no tile. UNCHANGED. Correct.
  "**One shrink** can do several of **these** at once." → the three carve-outs
    listed just before. UNCHANGED by the insertion (insertion is before them).
  "**The other bar** reaches neither a shrink nor a growth" → the non-§14 bar.
    CORRECT.

### hunk-06 insertion, at 3324-3327

  "A fill change on a layer that **stores** a tile carrying **either**" →
    "either" = "no padding position and no pad bit" from (c)'s opening.
    UNCHANGED. But the tense of "stores" — see B-10.
  "which is the same step's permission" → step 4's 3199-3202 permission.
    Resolves. CORRECT.

## 4. Check 2 — every citation opened

[R-CNF-01] (line 104-106) — "All text in this document is normative except: §1
  (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
  appendices identified as non-normative." Used to classify hunk-01 (Rationale,
  non-normative) and hunk-06 (Example, non-normative). PASS.
[R-GEO-06] (1700-1703) — "The **disk tile ordinal**, which orders tile-index
  entries (§15), is s for an interleaved layer, and **c · N + s** for a planar
  layer (§14), where c is the channel's index (§3.1) — channel-major grouping."
  hunk-03 claims exactly this, including "a disk ordinal is c · N + s". PASS.
§11.2 (1631-1640) — "its **addressed-tile count** ... is N for an interleaved
  layer and C · N for a planar layer, where C is the channel count". hunk-03's
  "the channel count enters the addressed-tile count C · N (§11.2)". PASS.
§11.1 (1584-1600) — cited by 3201 as "what schema-first creation needs (§11.1)".
  §11.1 has [R-GEO-02] (extent 0 valid) and the Rationale about schema-first
  workflows. PASS.
§14.5 / [R-SER-05] (2087-2098) — "at every padding position, a writer MUST
  encode, for each channel the position carries, that channel's fill value".
  hunk-03 lifts the phrase verbatim. PASS as to wording; see B-08 as to range.
[R-COD-07] (2447-2463) + its Note (2465-2476) — "The cap is quantified over the
  layer's *addressed* tiles". Step 4's "which an empty layer escapes only because
  that cap is quantified over addressed tiles". PASS.
L44 (3730) — "Codec 4 (lz4) declared on a layer any of whose addressed tiles'
  decoded size exceeds 0x7E000000 bytes". PASS.
[R-SLB-04] (2306-2314) — "A writer or updater whose commit changes the
  stored-tile set, the run partition, or the byte placement of any run of a
  slab-declared layer MUST either re-establish the invariants for every such run
  — or clear the declaration". A shrink changes N and so the run partition
  (planar blocks [c·N,(c+1)·N)), so this genuinely binds a shrink. PASS.
[R-SLB-01] (2260-2268) — per-tile alignment; "every stored tile's offset
  satisfies offset mod A = 0". A pure shrink moves no tile, so it binds
  vacuously; step 4 at 3255-3258 already states the kept-tiles form. PASS
  (binds, as hunk-04 says; satisfied trivially).
[R-CNT-21], [R-CNT-17] (3244-3245) — pre-existing, unchanged by my hunks;
  L21 (3707) confirms [R-CNT-17] is the entry_count = addressed-tile-count rule.
  PASS.
[R-CNF-05] (200) — writer conformance is semantic; used in my byte-level
  reasoning. PASS.
§21.7 (3862-3950) — cited by 3239-3242 as recording the no-witness consequence.
  §21.7 does record it (3909-3911). PASS as to the pointer; FAIL as to what
  §21.7's own earlier sentence says about re-typing — see B-03.
§20.5 (3400-3470) — cited as the whole-file-rewrite home. Compaction "MUST
  preserve content", so it grants no licence that collides with either bar. PASS.
§13.3 / [R-TYP-08] (1875-1890) — NOT cited by the repair; relevant to B-08.
§14.1 / [R-SER-01] (1930-1946) and §14.2 / [R-SER-02] (1954-1978) — the value
  sequence and the offset table. Relevant to B-09.
L32 (3718) — "A layer **geometry** field whose floor is 1 is 0 | rank d;
  **channel count C**; tile extent Tᵢ". Relevant to B-07.
[R-EXT-04] (1556-1562) — "sample types, geometry, channel sets and layout,
  codecs, filters, linearization, fill ... are never ignorable" — lists geometry
  and channel sets SEPARATELY. Also relevant to B-07, and it is why B-07 is an
  ambiguity rather than a flat error.

## 5. Check 3 — where each repair sits, by LABEL

hunk-01: block opens `> **Rationale.**` at line 1602. Labeled Rationale ⇒
  non-normative. The rules it restates are stated normatively at 3133 and 3179,
  and the block itself says "§20.3 states normatively, and governs". So this is
  NOT the "only statement in a labeled block" signature. It IS a mis-restatement
  in a non-normative block: B-01.
hunk-03/04/05: lines 3153-3242, inside the numbered "An appender MUST, in order:"
  list. No ">" marker, no label. NORMATIVE. Both new MUST NOTs land with force.
hunk-06: block opens `> **Example — the three shapes a commit takes.**` at 3292.
  Labeled Example ⇒ non-normative. It restates step 4's permission; the normative
  statement at 3199-3202 already carries the superseded-generation quantifier, so
  the repair did not need to land here for force. B-10 is what it left behind.

Test applied in every case: the block's opening words, not the ">" marker.

## 6. Check 5 — completeness words, each falsified or cleared

"Of **its two** bars" (1606) — verified 2 by counting MUST NOTs. CLEAR.
"**both** bars'" (3202) — same. CLEAR.
"**the whole of** the test of what a shrink alters" (3214-3215) — hunk-04
  deliberately narrowed this from "the whole of the test". As narrowed it is
  right; but the untouched sentence beside it is not. B-06.
"the §14 bar and **nothing else**, its carve-out included" (3231) — about what
  counts as an ALTERATION. Consistent with the narrowing. CLEAR.
"**among them**" (3216) — explicitly open. CLEAR.
"the list is **not offered as exhaustive**" (3209-3210) — CLEAR.
"moves **no ordinal at all**" (3187) — arithmetic checked below. CLEAR.
"which **no** channel declaration enters" (3197) — true of s. CLEAR as to
  ordinals; the surrounding sentence is B-09.
"whose **only** stated occasion for a renumbering is a geometry change" (3177-78)
  — B-07.
"An interleaved layer is **unaffected**" (3196) — B-09.
"free where it does not" (1618) — B-01.
"**exactly** where it alters nothing §14 fixes" (3220-3222) — B-06.
"a re-typed channel among the cases it does **not** reach" (3897-98, §21.7) — B-03.

## 7. Check 6 — the structure, and what is still unconstrained

Structure the two bars govern: a layer record's **channel declaration list**.
Per §12 (1717-1719) each channel entry carries: a name (§4.6), a sample type
(u16, structural), a fill value (§13). Per §3.1 the list's ORDER is load-bearing
and fixes each channel's index. Per §11.1 the list's LENGTH is the channel count
C, which L32 calls a layer geometry field.

Member by member, is it fixed by a rule?
  sample type   — YES, newly and explicitly: 3153-3172 (the §14 bar's subject).
  fill value    — YES, but only via the §14 bar's general preamble, because
                  changing fill changes the content [R-SER-05] fixes at padding
                  positions and the pad bits of §14.3. Where a layer has neither
                  a padding position nor a pad bit the change is free, which the
                  (c) Example blesses at 3319-3321. Note it still changes what
                  every SENTINEL tile reads as ([R-TYP-08], §13.3) — nothing bars
                  that, and the document appears to intend it. Not a repair
                  defect; recorded.
  channel name  — governed by nothing. Correct: a name enters no ordinal, no
                  offset and no size. Recorded as intentionally free.
  order/index   — planar: YES, the new bar at 3179.
                  interleaved: only via the §14 bar's preamble, and the new
                  paragraph's only sentence about interleaved layers says
                  "unaffected". B-09.
  count C       — planar: partially. Appending, or removing the last, is
                  explicitly free (3186-3188) and the arithmetic is right.
                  Mid-list insert/remove is barred where a moved channel has a
                  stored tile. A removed channel's OWN stored tiles simply fall
                  out of the addressed set and become slack — the same disposal a
                  shrink gets. Consistent.
                  interleaved: changing C changes Q = ΣBᵢ and so the decoded size
                  ⇒ §14 bar. Covered.

Neighbouring quantity of the same structure that the disk-ordinal bar does NOT
name: the per-value in-sample offset F_c = Σ_{j<c} B_j of §14.2's table. For a
planar layer the ordinal is the whole story; for an interleaved layer the ordinal
never moves and F_c is the only thing that does. The repair pinned the ordinal
and said the sibling case is "unaffected". B-09.

Other quantity checked and found governed: N. A growth or shrink changes N, and
for a planar layer c·N + s therefore moves for every c ≥ 1. Neither bar reaches
it (both are scoped to declaration changes / channel declarations), and it does
not need to be barred: step 4's re-emission rule at 3126-3128 states the
renumbering as a fact — "(a geometry change renumbers ordinals wherever
[R-GEO-06] moves them)" — and §11.1's Rationale repeats it at 1625-1627.
Coherent. NOT a finding.

## 8. Check 7 — arguments by warrant, verb against verb

(i) 3153: "A channel's declared **sample type** is **such a declaration**, and
    changing it is **such a change**".
    Warrant verb (3133-3135): "A commit MUST NOT **change** a layer's
    declarations in a way that **alters**, for any tile that layer **stores in
    the generation this commit supersedes**, what §14 fixes ...".
    Repair's verb: "wherever the layer **stores** a tile that carries that
    channel" — bare present, no generation.
    Same set? NO. "stores" simpliciter ranges over the live/new state; the bar
    ranges over the superseded state. → B-02.

(ii) 3205: "held, for each channel the position carries, that channel's fill
    (§14.5)".
    Cited verb, [R-SER-05]: "at every padding position, a writer MUST **encode**,
    for each channel the position carries, that channel's fill value".
    Same set? §14.5 ranges over padding positions of a SERIALIZED tile. The
    repair's clause ranges over every position a growth makes real, which
    includes positions inside tiles the superseded generation did not store
    (sentinel entries) and positions inside grid cells the old geometry did not
    address at all. Those positions held no byte; they READ as fill under
    [R-TYP-08]/§13.3, which the repair does not cite, and "held" is false of them.
    → B-08. One sentence carrying the warrant for two different populations, and
    it is sound for one and unsound for the other.

(iii) 3177-3178: "what it disturbs is instead the re-emission rule above, whose
    only stated occasion for a renumbering is a geometry change."
    Cited text (3126-3128): "every other entry byte-identical at its disk-ordinal
    position (a geometry change renumbers ordinals wherever [R-GEO-06] moves
    them)." The characterisation of the cited rule is accurate as far as the
    words go. The problem is whether "geometry change" excludes a channel-
    declaration change, which is what the argument needs. → B-07.

(iv) 3234: "a shrink producing only those is permitted here **exactly as it is
    there**". "here" = the shrink paragraph, "there" = the §14 bar's carve-out at
    3149-3151. Both range over "a new padding position whose stored byte already
    holds the fill [R-SER-05] fixes". Verbs: "is not what this bars" / "is not
    one". Same set. PASS — reported because it passes.

(v) 3198-3199: "the operation is a new layer or a whole-file rewrite, **exactly
    as above**". "above" = 3171-3172, "Such a change is a new layer, or a
    whole-file rewrite under a fresh file_id ([R-LIF-01], §20.5)". Same remedy,
    same actor. PASS.

(vi) 3229-3231: "the quantifier is the superseded generation's ... What counts as
    such an alteration is the §14 bar and nothing else". Verb "alters what §14
    fixes for a tile stored there" vs the bar's "alters ... for any tile that
    layer stores in the generation this commit supersedes". Same set. PASS.

## 9. Derived numbers

- Bars in step 4: I counted MUST NOTs at 3133 and 3179 = **2**. Document figures
  compared: "two bars" (1606), "both bars" (3202), "The bar beside the §14 bar"
  (3236), "Its companion bar" (3901). All agree. Searches for "three bars",
  "third bar", "the bars", "each bar" returned 0 hits each.
- Normative keywords in step 4: 2 MUST NOT, 3 MAY, 1 SHOULD, 0 bare MUST.
- Ordinal example at 3193-3196, recomputed from [R-GEO-06] with N = 2:
    a (c=0): 0·2+0 = 0, 0·2+1 = 1  → {0,1}. Document says 0 and 1. MATCH.
    b (c=1): 1·2+0 = 2, 1·2+1 = 3  → {2,3}. Document says 2 and 3. MATCH.
    append c (c=2): 2·2+0 = 4, 2·2+1 = 5 → {4,5}; a and b unmoved.
      Document: "leaves those four where they are and adds 4 and 5". MATCH.
    exchange a and b: b→c=0→{0,1}, a→c=1→{2,3}; all four tiles change ordinal.
      Document: "moves all four". MATCH.
- Interleaved reorder arithmetic, from [R-SER-02]'s table, channels a(uint8),
  b(uint8): Q = ΣBᵢ = 2 before and after. Decoded size P·Q unchanged.
  Offset of value k = (k div C)·Q + F_{k mod C}; the sample term (k div C)·Q is
  unchanged; F_a goes 0→1 and F_b goes 1→0. So exactly one quantity moves and it
  is a VALUE's in-sample offset, not a SAMPLE's offset. The §14 bar's list at
  3138-3139 names "the byte offset of any **sample** within the decoded tile
  image". Basis for B-09.
- Element sizes for the §21.7 cross-check: int8 and uint8 both 1 byte, so an
  int8→uint8 re-type changes no decoded size, no padding-byte content and no
  offset — the basis for calling the disputed file in B-03 conforming.
- All five obligations hunk-04 says are stated "below" verified to be below
  line 3220: 3244, 3245, 3247, 3255, 3258.

## 10. Sweeps run, verbatim, with hit counts

grep -n "bar" spec/tarn.md                                   → 47 lines
grep -n "re-declar" spec/tarn.md                             → 6
grep -n "shrink" spec/tarn.md                                → 17
grep -n "grow" spec/tarn.md                                  → 22
grep -n "disk ordinal\|disk-ordinal\|disk tile ordinal"      → 24
grep -n "R-GEO-06" spec/tarn.md                              → 6
grep -n "geometr" spec/tarn.md                               → 16
grep -n "R-SLB-01" / "R-SLB-04" / "^| L44 "                  → 7 / 3 / 1
grep -n "R-CNF-01\|R-CNF-05"                                 → 12
awk step-4 range | grep -o "MUST NOT\|MUST\|SHOULD\|MAY"     → 2/0/1/3

Whitespace-normalised (python3, re.sub(r'\s+',' ') over the whole file, so hard
wraps cannot hide a phrase):
  'three bars' 0 | 'two bars' 1 | 'both bars' 1 | 'the bars' 0 | 'each bar' 0
  'all three bars' 0 | 'third bar' 0 | 'companion bar' 1 | 'bar beside' 1
  '§14 bar' 11 | 'step 4' 6 | 'sample type' 11 | 'declared type' 2 | 're-typ' 3
  'channel declarations' 3 | 'disk ordinal' 16 | 'geometry change' 2
  'permutation' 2 | 'reorder' 3 | 're-index' 2 | 'insert a channel' 0
  'appending a channel' 1 | 'channel count' 11 | 'channel set' 1
  'changing a channel' 1 | 'change a channel' 0 | 'declared order' 4
  'load-bearing' 5 | 'not reach' 6 | 'does not reach' 6 | 'unaffected' 10

Every hit for 'step 4', 'geometry change', 'channel declarations',
'declared type', 're-typ', 'permutation', 'reorder', 're-index',
'appending a channel', 'channel set', 'changing a channel' was printed with 260
characters of context on each side and read. That sweep is what surfaced B-03
(§21.7) and B-07 (L32 / [R-EXT-04]).

## 11. Findings

### B-01 — hunk-01. §11.1 Rationale contradicts the sentence before it, on tense.

  1614  "A layer that
  1615   stored no tile in the generation the commit supersedes may be
  1616   re-declared freely; a layer the commit itself empties does not
  1617   qualify. Re-typing a channel is the §14 bar's own subject, barred
  1618   wherever the layer stores a tile that carries that channel, and
  1619   free where it does not."

The first sentence was repaired precisely to carry the superseded-generation
quantifier and to close the empty-as-you-go loophole. The very next sentence,
written in the same repair, states the re-typing rule in the bare present and
adds "and free where it does not". Take a planar layer whose channel `c` has
stored tiles, and a commit that supersedes all of them (sentinel entries) and
re-types `c` in the same directory. After the commit the layer stores no tile
carrying `c`, so sentence 2 says "free". Sentence 1 and §20.3 at 3141-3145 say
barred: "so a commit does not escape this by unstoring in the same breath:
superseding every tile of a layer and re-declaring it are one operation, and this
bars it." The two sentences are adjacent and answer the same question opposite
ways. Repair: "...barred wherever the layer stored a tile carrying that channel
in the generation the commit supersedes, and free where it did not."

Byte-level: NO. Block label is **Rationale.** ⇒ non-normative under [R-CNF-01],
and the block itself defers ("§20.3 states normatively, and governs"). §20.3
decides the bytes either way. But it is the same fact pattern the repair fixed
one clause earlier, restated as permitted.

### B-02 — hunk-03. The normative sample-type rule restates the §14 bar without
### the §14 bar's generation quantifier.

  3153  "A channel's declared **sample type** is such a declaration, and
  3154   changing it is such a change wherever the layer stores a tile that
  3155   carries that channel"

The bar it elaborates (3133-3135) is quantified "for any tile that layer stores
**in the generation this commit supersedes**", bolded in the source, and 3141-45
spends four lines insisting on that tense. The elaboration drops it. Three lines
later the paragraph gets it right — "Where the superseded generation stored no
tile carrying that channel there is nothing to reinterpret" (3161-3163) — and
then drops it again in the same sentence's gloss: "re-typing a channel of a layer
that **stores nothing**, or a planar channel none of whose own tiles **are
stored**, is a declaration edit like any other" (3163-3165). Three statements of
the condition, one qualified and two not, and the unqualified ones are the
paragraph's opening claim and its worked gloss — the two a reader lifts.

I grant the defence: "such a declaration"/"such a change" is anaphoric to the bar
and arguably imports its quantifier. That is why I mark this PLAUSIBLE rather
than CONFIRMED. It is nonetheless the exact slip the same commit went to §11.1
and to the (c) Example to fix, and it left it standing in the paragraph it wrote
itself.

Byte-level: YES. The disputed commit is: supersede every stored tile carrying
channel `c`, and re-declare `c` from int8 to uint8, in one commit. Element size
is 1 both ways, so the decoded size, every sample offset, every padding byte and
the codec/filter are unchanged, and §21.7 says in terms that this leaves the live
state clean and unwitnessed (3909-3911). The resulting file is CONFORMING — no
register row fires. Writer A, reading 3153-3155 and 3163-3165, emits it; writer B,
reading 3141-3145, refuses and writes a new layer or a fresh file_id instead.
Different bytes on disk for the same caller request.

Repair: "...wherever the layer stored a tile carrying that channel in the
generation this commit supersedes", and likewise "a layer that stored no tile
there" / "a planar channel none of whose own tiles were stored there".

### B-03 — hunk-03. §21.7 still says the §14 bar does not reach a re-typed
### channel. Unswept restatement, and it now contradicts the new paragraph head-on.

  3896  "§20.3 step 4's **§14 bar** is witnessed only where the affected tiles
  3897   remain stored, and then only for part of what it bars — a re-typed
  3898   channel among the cases it does not reach, since the prior
  3899   generation's declarations are not part of the live state..."

"it" is bound two clauses earlier — "for part of what **it** bars" — to the §14
bar. So the sentence says the bar does not reach a re-typed channel. The repair's
whole purpose at 3153-3165 is that it does: "A channel's declared sample type is
such a declaration, and changing it is such a change". hunk-01 says it a third
time, in the same vocabulary: "Re-typing a channel is the §14 bar's own subject"
(1616-1617).

§21.7's own later text also contradicts it: "Where the change does touch something
§14 fixes, the rows below reach it" (3907-3908) and "A change reaching the decoded
size is witnessed by T3 or T14" (3917-3919), with the worked case "a planar
`uint8` channel re-declared `bool` ... its plane goes from P · Bᶜ bytes to ⌈P/8⌉"
(3912-3914) — a re-typing that IS reached. The author plainly meant "among the
cases the WITNESSING does not reach"; the pronoun says the bar.

This is the restatement the repair should have swept. §21.7 is the one other place
in the document that discusses re-typing, it uses the same verb ("reach"), and the
repair is the commit that made re-typing an explicitly named subject of the bar.
Repair: "— a re-typed channel among the cases no check reaches, since ...".

Byte-level: YES, though I mark it PLAUSIBLE because §21.7's heading is "What no
check detects" and a careful implementer reads it as detection scope. The disputed
file is the same one as B-02 and is conforming; §21.7 is unlabeled prose carrying
[R-ERR-01], hence normative under [R-CNF-01], so a writer that takes 3897-3898 as
a scope statement about the bar emits a re-typing commit that a writer reading
3153 refuses.

### B-04 — hunk-05. The insertion moved "this" onto itself. §21.7's consequence
### now attaches to a shrink instead of to the rescue case.

  3236  "The bar beside the §14 bar does not reach a
  3237   shrink either: it bars a change to a planar layer's channel
  3238   declarations that moves a stored tile's disk ordinal, and a shrink
  3239   is not one. §21.7 records the
  3240   consequence — that **this** is precisely where the §14 bar has no
  3241   witness, the live state being clean — which is why the rule is
  3242   stated here and not left to the rows."

Before the insertion, "this" resolved to the rescue case discussed at 3226-3231:
"Unstoring that tile in the same commit does not rescue it either ... the
quantifier is the superseded generation's". §21.7 confirms that is what it
records: "a commit that supersedes every tile it would have damaged leaves the
live state clean, so the §14 bar is unwitnessed there" (3909-3911).

After the insertion, the nearest antecedent is "a shrink" — the last noun of the
inserted sentence is literally "a shrink is not one." So the sentence now reads
"a shrink is precisely where the §14 bar has no witness", which §21.7 nowhere says
and which is false: a shrink that damages a still-stored tile is exactly where the
rows DO bite (§21.7's T2/T3/T4/T14/T26 discussion at 3914-3934). The clause
"the live state being clean" is the giveaway — a shrink does not leave the live
state clean; a supersede-everything commit does.

The repair touched this very sentence — it changed "the bar" to "the §14 bar" one
word away — and did not notice it had moved the antecedent of "this".
Repair: put the inserted sentence AFTER the §21.7 sentence, or make it explicit:
"§21.7 records the consequence — that a commit that unstores the tile it would
have damaged is precisely where the §14 bar has no witness...".

Byte-level: NO. Both readings describe detection, not emission; no file changes
hands. But it misstates what §21.7 holds, and §21.7 is normative.

### B-05 — hunk-03. The insertion re-pointed "them" and narrowed the remedy
### sentence from any barred change to a re-typing.

  3151  "...is not what this bars."   [paragraph break inserted here]
  ...
  3164  "...or a planar channel none of whose own tiles are stored, is a
  3165   declaration edit like any other. Where a change does reach **them**
  3166   it makes each stored tile it reaches nonconforming..."

Before the insertion these were one continuous passage and "them" was the nearest
plural, "those tiles" at 3147 = "any tile that layer stores in the generation this
commit supersedes". Now twenty lines and a paragraph boundary intervene, and the
nearest plurals are "stored bytes" (3161), and the tiles of "a planar channel none
of whose own tiles are stored" (3164-3165) — tiles that are by construction NOT
stored, which inverts the sentence. The consequence sentence that hangs off it —
"Such a change is a new layer, or a whole-file rewrite under a fresh file_id"
(3171-3172) — was the general remedy for anything the §14 bar reaches and now
reads as the remedy for a re-typing only, which matters because 3198-3199 points
back at it ("exactly as above") for the ordinal bar.

Repair: close the sample-type paragraph after 3165 and restore the general
sentence to its own paragraph with an explicit subject — "Where a change does
reach a tile the superseded generation stored, it makes each such tile
nonconforming...".

Byte-level: NO. The sentence states consequences and a remedy, not a permission
or a prohibition; the bar itself is unmoved.

### B-06 — hunk-04. The added caveat contradicts the untouched sentence four
### words later.

  3214  "An extent MAY also **shrink**, and the §14 bar is the whole of the
  3215   test of what a shrink **alters**, **in that bar's own tense**;
  3216   the obligations this step states below — among them slack,
  3217   entry_count, a slab or alignment declaration (`[R-SLB-04]`,
  3218   `[R-SLB-01]`), and the recommendation to produce a new file
  3219   instead where a commit would strand a large share of a layer's
  3220   stored bytes — bind a shrink as they bind any commit. A shrink is permitted
  3221   exactly where it alters nothing §14 fixes for any tile the layer
  3222   stores in the generation this commit supersedes."

The repair's point is that satisfying the §14 bar is NOT sufficient for a shrink
to be permitted — [R-SLB-04], [R-CNT-17] and the SHOULD bind too. The next
sentence, untouched, says a shrink "is permitted **exactly where**" it satisfies
the §14 bar, which is an iff and therefore asserts the sufficiency the previous
clause just withdrew. The old text was at least self-consistent (both halves
over-broad); the repair fixed one half and left the other. The growth paragraph
shows the document knows the right form: "a growth is permitted exactly where the
geometry it produces satisfies **every rule that geometry is subject to**"
(3211-3212).

Repair: "A shrink alters nothing the §14 bar reaches exactly where it alters
nothing §14 fixes for any tile the layer stores in the generation this commit
supersedes", or append "and satisfies every other obligation this step states".

Byte-level: NO, and I want to be explicit about why rather than claim it. Every
obligation the added clause names is either a MUST whose breach puts a register
row in the file — [R-SLB-04]'s breach is detected as [R-SLB-03]'s invariant
failures (2315-2321), [R-CNT-17]'s as L21 (3707) — so [R-CNF-05] bars both
readings' writers from emitting it, or a SHOULD (3247-3250), whose breach leaves
the file conforming under both readings. The emittable set does not move.

### B-07 — hunk-03. The second bar's whole warrant rests on "geometry change"
### excluding a channel-declaration change, and the document classes the channel
### count as a geometry field.

  3174  "One effect is barred beside it, on the same tense and on its own
  3175   ground: the §14 bar does not reach it, an ordinal move being no
  3176   effect on any stored tile's bytes, and what it disturbs is instead
  3177   the re-emission rule above, whose **only** stated occasion for a
  3178   renumbering is a geometry change."

The argument is: the re-emission rule licenses renumbering only for a geometry
change, a channel-declaration change is not one, therefore the renumbering it
causes is unlicensed and needs its own bar. The middle premise is what the
document contradicts:

  L32 (3718): "A layer **geometry** field whose floor is 1 is 0 | rank d;
  **channel count C**; tile extent Tᵢ | ... `[R-GEO-01]`"
  L21 (3707): "entry_count does not equal the **geometry-derived** addressed-tile
  count (N interleaved, **C·N** planar)"
  §11.1 (1591-1594), under the heading "Geometry and its validity floor":
  "...and the layer has at least one channel. ... Writers MUST NOT emit a layer
  with rank 0, any tile extent 0, or channel count 0."

By those, inserting or removing a channel IS a geometry change, the re-emission
rule's parenthetical at 3126-3128 already covers it, and the stated ground for the
new bar evaporates. Cutting the other way, [R-EXT-04] (1558-1560) lists "sample
types, geometry, channel sets and layout" as separate items, which is the reading
the repair needs. So the document uses "geometry" both ways and the repair's
warrant turns on the undetermined one.

Repair: state the ground without the term — "...whose stated occasion for a
renumbering is a change to a dimension's extent or tile extent" — or say plainly
that this bar and the re-emission rule's parenthetical partition the renumbering
cases between them.

Byte-level: NO. The MUST NOT at 3179 stands on its own words whatever the ground
clause says, and 3126-3128 states a fact about re-emission rather than granting a
permission, so no writer's output moves. But it is the entire justification the
repair offers for adding a second bar, and it is stated with "only".

### B-08 — hunk-03. The growth clause's new citation covers one of the two
### populations the clause ranges over.

  3203  "...and an extent MAY **grow**, since a position that
  3204   becomes real held, for each channel the position carries, that
  3205   channel's fill (§14.5), and fill is a legal sample value..."

[R-SER-05] (§14.5, 2090-2093): "at every padding position, a writer MUST encode,
for each channel the position carries, that channel's fill value". The phrase is
lifted verbatim and the citation is exact — for positions that were PADDING
POSITIONS OF A STORED TILE. But a growth makes real, in one operation, at least
three populations: (a) padding positions of stored tiles — §14.5, correct;
(b) padding positions of ADDRESSED BUT UNSTORED tiles, whose entry is the
sentinel; (c) positions in grid cells the old geometry did not address at all,
because a grid count rose. For (b) and (c) no byte ever existed, so "held ...
that channel's fill" is false of them and §14.5 says nothing about them; what
makes the growth safe there is [R-TYP-08] / §13.3 "Unstored tiles read as fill"
(1877-1884), which the repair does not cite. §11.1's own Rationale
(1621-1624) confirms case (c) is in scope: "a growth raising one grid count
⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0".

The pre-repair text had no citation at all and a dangling "that channel's"; the
repair fixed the dangling reference and, in doing so, attached a warrant that is
sound for one of the three populations.
Repair: "...held, for each channel the position carries, that channel's fill —
as encoded content where the tile was stored (§14.5), and as what an unstored
tile reads (§13.3) where it was not — and fill is a legal sample value".

Byte-level: NO. The clause is the "since" of a permission, not a condition on it;
the operative proviso is the "provided the grown geometry stays within every
bound..." that follows.

### B-09 — hunk-03. The one sentence about interleaved layers says "unaffected",
### and the quantity that actually moves for them is not in the §14 bar's list.

  3196  "An interleaved layer is unaffected, its disk ordinal being s,
  3197   which no channel declaration enters."

True of the disk ordinal. But the paragraph is the document's only sustained
treatment of what a commit may do to a channel declaration list, and this is its
only sentence about interleaved layers, so it reads as clearance. Reordering an
interleaved layer's channels is in fact barred — but only by the §14 bar's
PREAMBLE ("what §14 fixes for its stored bytes or **how they decode**"), not by
any item in the list a reader will check. From [R-SER-02]'s table (1966-1971),
for two uint8 channels a and b: Q = ΣBᵢ = 2 before and after, so the decoded size
P·Q is unchanged; the padding set (§11.3) is unchanged; the padding content is the
same fill bytes; the codec and filter are unchanged; and the offset of value k is
(k div C)·Q + F_{k mod C}, whose sample term (k div C)·Q is unchanged. The only
quantity that moves is F_c — the in-sample offset of a channel's VALUE — and the
bar's list names "the byte offset of any **sample** within the decoded tile image"
(3138-3139). The planar sibling of this exact question got a new MUST NOT and a
worked example; the interleaved sibling got "unaffected".

That §14 fixes it is not in doubt: §3.1's glossary says "a channel's **index** is
its 0-based position in that order, and the order is load-bearing (§11.4, §14)".
The gap is that step 4 never says so, and the sentence a reader lands on says the
opposite-sounding thing.

Repair: "An interleaved layer's disk ordinal is s, which no channel declaration
enters, so this bar does not reach it — but reordering its channels moves each
channel's value within every sample (§14.2), which the §14 bar does."

Byte-level: YES, and I will name the disagreement. Writer A reads 3196 plus the
bar's four-item list and emits a commit that exchanges two equal-element-size
interleaved channels on a layer with stored tiles, changing only the directory.
Writer B reads the bar's preamble and refuses. A's file is CONFORMING: §21.7 says
so in terms — "moving a sample's byte offset within the decoded image without
changing that image's length alters no declared quantity" and "where it breaks
neither there is no witness" (3929-3934). So the disputed file is emittable under
one reading and not the other, and every subsequent read of that file returns
channel `a`'s samples as `b`'s. Marked PLAUSIBLE only because the preamble plus
"the list names where that effect arises rather than standing on its own" (3145-46)
gives B the better argument.

### B-10 — hunk-06. The Example's tense was repaired on the permission and left
### on the bar, in the same paragraph.

  3321  "A fill change on a layer that **stores** a tile
  3322   carrying either is not an
  3323   appender's operation at all (step 4): it would invalidate every
  3324   stored tile it reaches. A layer that stored no tile in the
  3325   generation the commit supersedes is re-declared freely..."

The repair added "in the generation the commit supersedes" to the permission
sentence and to nothing else. The bar sentence beside it keeps the bare present,
and the bold on "**stores**" now sets up a contrast against the next sentence's
explicit past — inviting exactly the reading step 4 forbids, that the test is on
the new state. Same slip as B-01 and B-02, in the third of the three places the
repair visited.

Repair: "A fill change on a layer that **stored** a tile carrying either in the
generation the commit supersedes is not an appender's operation at all".

Byte-level: NO. Block label is **Example** ⇒ non-normative ([R-CNF-01]).

## 12. Candidates I opened and dropped

1. "The other bar reaches neither a shrink nor a growth" (1618-1620) has no
   normative counterpart for the growth half — step 4 says only that it does not
   reach a shrink (3236-3239). Dropped: the growth half is derivable from the
   bar's own words, which are scoped to "the channel declarations" while a growth
   changes dimension extents. A negative scope claim that follows from the rule's
   text is not a rule needing its own statement.
2. "the §14 bar does not reach it" (3175) looked over-broad, because a planar
   channel permutation between channels of DIFFERENT element sizes changes a
   stored tile's decoded size, which the §14 bar lists — §21.7 says as much at
   3903-3907. Dropped: "it" in that clause is "One effect", i.e. the ordinal move
   as such, not the whole edit, and an ordinal move as such is indeed no §14 item.
3. A planar or interleaved growth/shrink moves every stored tile's disk ordinal
   (N changes, and the planar ordinal is c·N + s), and neither bar reaches it.
   Dropped: it is licensed on purpose — 3126-3128 "(a geometry change renumbers
   ordinals wherever [R-GEO-06] moves them)" and 1624-1627 say so.
4. A fill change on a layer with no padding position and no pad bit is free, yet
   it changes what every sentinel tile reads ([R-TYP-08]). Dropped: pre-existing,
   blessed by (c) at 3319-3321, untouched by these hunks, and consistent with the
   §14 bar being about STORED bytes.
5. Step 4's free-re-declaration permission (3199-3201) carries no "subject to
   every rule its new geometry is subject to" proviso, unlike the growth clause
   and unlike the (c) Example. Dropped: [R-CNF-05] makes writer conformance
   semantic, so a MAY cannot license a nonconforming file; and the register would
   fire (e.g. L44) on the file such a writer produced.
6. "Of **its** two bars" — dangling "its", and the bars are step 4's rather than
   §20.3's. Dropped as too small to file; recorded in §2 above.
7. hunk-04's list of obligations partly duplicates what 3243-3258 already states
   about a shrink. Dropped: redundancy, not error, and the "among them" keeps it
   open.
8. Removing a non-last channel that has stored tiles while the channels after it
   have none is permitted by the new bar, and the removed channel's stored tiles
   become slack. Dropped: that is the same disposal a shrink gets ([R-CNT-21]),
   and §23.1 already treats it as removal-from-reachability.

## 13. Per-check verdict

1 TENSE/QUANTIFIER — FAILS at three sites: B-01, B-02, B-10.
2 CITATIONS — 16 opened, 15 pass, 1 partial: B-08.
3 NORMATIVE PLACEMENT — passes. Labels checked, not markers. hunk-01 = Rationale,
  hunk-06 = Example, both non-normative but both restating rules that are stated
  normatively at 3133/3179; hunks 03/04/05 land unlabeled inside the MUST list.
4 NO CONTRADICTION IN THE PASSAGE — FAILS: B-01, B-06 (and B-03 across sections).
5 EXHAUSTIVE CLAIMS — one fails: B-07's "only". The counts all check out.
6 WHAT IS LEFT UNCONSTRAINED — one gap: B-09 (interleaved channel order).
7 WARRANT-BY-ANALOGY — two of six comparisons fail: B-02 (i), B-08 (ii); (iii)
  is B-07; (iv), (v), (vi) pass and are reported passing.
8 WHAT THE INSERTION DID TO ITS NEIGHBOURS — FAILS twice: B-04, B-05. Two other
  back-references were re-pointed correctly by the repair and are reported so.
