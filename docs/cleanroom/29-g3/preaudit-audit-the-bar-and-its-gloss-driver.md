# Repair audit — lane "the-bar-and-its-gloss-driver"
Charter hunks: hunk-02, hunk-03, hunk-04, hunk-05, hunk-06 (all land in §20.3 step 4,
current spec lines 3139–3328; nearest preceding heading line 3073 "#### 20.3 The append
procedure" — header line verified against the body, no mismatch).

## 0. Disclosure

Read, in full or in the ranges named:
- /private/tmp/.../case/hunk-02.diff, hunk-03.diff, hunk-04.diff, hunk-05.diff, hunk-06.diff
  (cat'ed together in one call). No other hunk file, no full.diff, no directory listing.
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md — ranges 96–116
  (§2.1/[R-CNF-01]), 341–430 (§3.1, §3.2, §3.3), 455–480 ([R-ENC-03]/[R-ENC-04]/[R-ENC-06]),
  1600–1730 (§11.1 rationale, §11.2, §11.3, §11.4/[R-GEO-06], §12 head), 1720–1830 (§12.1–12.3),
  1922–2120 (§14 entire), 2146–2200 (§15.2, §15.3), 2245–2348 (§16 entire),
  2371–2500 (§17.2 codecs, [R-COD-07] + its Note), 2556–2578 (§18.1),
  3073–3360 (§20.3 entire + head of §20.4), 3864–4000 (§21.7 entire),
  4199–4240 (§23.1), plus grep-returned single lines listed in §1 below.
- Wrote and ran one scratch script,
  /private/tmp/.../scratch/the-bar-and-its-gloss-driver/ordinals.py (output in §4).
- Wrote this transcript to /private/tmp/.../out/audit-the-bar-and-its-gloss-driver.md.

Nothing else. No docs/, no conformance/, no registry.json, no git, no web.

Unrequested context that appeared before I began: a project CLAUDE.md pointer to AGENTS.md,
and an index of the maintainer's auto-memory files (titles only, several naming this project's
process). I did not open any of them and drew no conclusion from their titles. Disclosed as
required; not used.

## 1. Sweeps run (verbatim, with hit counts)

All run with `grep -n` in spec/ against tarn.md. The document is hard-wrapped, so every
pattern below is a short fragment chosen not to wrap.

    grep -n "R-GEO-06" tarn.md                     6 hits (1626,1703,2971,3127,3181,3934)
    grep -n "R-COD-07" tarn.md                     6 hits (2462,2942,3207,3732,3771,4028)
    grep -n "bar" tarn.md | grep -v barrier        ~30 hits (listed in-line below)
    grep -n "re-declar" tarn.md                    6 hits (1615,3145,3201,3204,3326,3962)
    grep -n "supersedes" tarn.md                   14 hits
    grep -n "sample type" tarn.md                  7 hits (185,1521,1723,1728,3139,3154,4714)
    grep -n "disk ordinal" tarn.md                 13 hits
    grep -n "channel declarations" tarn.md         2 hits (1619, 3180)
    grep -n "re-typ" tarn.md                       3 hits (3164, 3945, 3961)
    grep -n "stores no tile" tarn.md               2 hits (3200, 4648)
    grep -n "empties" tarn.md                      2 hits (1615, 3328)
    grep -n "step 4" tarn.md                       6 hits (2930,3101,3324,3944,4208,4221)
    grep -n "declaration edit" tarn.md             1 hit  (3166)
    grep -n "the §14 bar" tarn.md                  8 hits (1606,1616,3176,3215,3232,3237,3241,3985)
    grep -n "companion" tarn.md                    1 hit  (3949)
    grep -n "two bars" tarn.md                     1 hit  (1606)
    grep -n "both bars" tarn.md                    1 hit  (3203)
    grep -n "R-CNF-01" tarn.md                     1 hit  (106)
    grep -n "R-CNT-17\]\`\|R-CNT-21\]\`" tarn.md   19 hits
    grep -n "R-CNT-25" tarn.md                     10 hits
    grep -n "R-ENC-04" tarn.md                     5+ hits (455–471 definition read in full)

## 2. What each hunk makes true (the rule it adopts)

**Hunk 02.** Gives the step-4 prohibition a name — "the **§14 bar**" — and adds one member to
its appositive list: "the sample type each value in the image is read under". The rule it
makes true: a commit may not re-declare a channel's sample type where the layer stored, in the
superseded generation, a tile carrying that channel — even when the new type has the same
element size and the stored bytes are untouched.

**Hunk 03.** (a) A classifying paragraph asserting that a sample type is "such a declaration"
and a re-type "such a change" wherever a stored tile carries the channel, decided from the
layer record and not from stored bytes, and free where the superseded generation stored no
such tile. (b) A second, new MUST NOT: for a planar layer, a commit may not change the channel
declarations in a way that alters the disk ordinal [R-GEO-06] assigns any tile the layer stored
in the superseded generation — with an account of which channel edits move an ordinal, a worked
example, and an interleaved exclusion. (c) "the tense is the bar's" → "both bars'". (d) The
growth warrant gains "for each channel the position carries" and a §14.5 citation.

**Hunk 04.** Replaces the anaphor "the bar above" with "the §14 bar", narrows the exclusivity
claim from "the whole of the test" to "the whole of the test of what a shrink **alters**", and
states that the step's later obligations (slack, entry_count, [R-SLB-04]/[R-SLB-01], the
new-file SHOULD) bind a shrink as they bind any commit. Rule made true: a shrink that alters
nothing §14 fixes is still bound by everything else a commit is bound by.

**Hunk 05.** Two more "bar above" → "§14 bar" swaps, plus a new sentence excluding the second
bar from the shrink test.

**Hunk 06.** Aligns Example (c)'s restatement of the free-re-declaration permission with step
4's tense: "A layer storing no tile" → "A layer that stored no tile in the generation the
commit supersedes … a layer the commit itself empties does not qualify."

## 3. Check 3 — normative force, by LABEL not by ">"

[R-CNF-01] (line 106, read in full): "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified
as non-normative."

- Hunks 02–05 land in the numbered prose of §20.3 step 4. No blockquote marker, no label.
  **Normative.** The two MUST NOTs are in force. PASS.
- Hunk 06 lands inside a block opening `> **Example — the three shapes a commit takes.**`.
  Label = *Example* ⇒ **non-normative**. I applied the label test, not the marker test.
  This is *not* a failure-to-land: the normative statement of the same rule is at 3200–3204
  ("A layer that stores no tile **in the generation this commit supersedes** MAY be re-declared
  freely … the tense is both bars', so a commit does not earn this permission by emptying the
  layer as it re-declares it"), and hunk 06 brings the Example into agreement with it rather
  than being the rule's only home. PASS — this is the sweep done right.
- §11.1's block at 1602–1628 is labelled `> **Rationale.**` ⇒ non-normative; §21.7's at
  3930–3995 likewise. Both restate the two bars and both already carry the new wording, so
  neither is an unswept restatement. (§21.7's normative body at 3864–3922 carries no statement
  of either bar.)

## 4. Check — the disk-ordinal arithmetic, derived independently

[R-GEO-06] (1703–1707, read in full): "The **disk tile ordinal**, which orders tile-index
entries (§15), is s for an interleaved layer, and **c · N + s** for a planar layer (§14), where
c is the channel's index (§3.1)". §11.2 [R-GEO-03]: N = ∏Gᵢ (spatial-tile count); addressed-tile
count = N interleaved, C·N planar. §3.1: "a channel's **index** is its 0-based position in that
order".

Script /private/tmp/.../scratch/the-bar-and-its-gloss-driver/ordinals.py, output verbatim:

    N=2, channels (a,b): {0: [0, 1], 1: [2, 3]}
    append c -> C=3: {0: [0, 1], 1: [2, 3], 2: [4, 5]}
    swap a,b (b idx0, a idx1): {0: [0, 1], 1: [2, 3]}
    insert at front, C=3: {0: [0, 1], 1: [2, 3], 2: [4, 5]}
    growth N=2->3, C=2: {0: [0, 1], 1: [2, 3]} -> {0: [0, 1, 2], 1: [3, 4, 5]}
    max ordinal C=4,N=32: 127 C*N-1 = 127

Claim-by-claim against the repaired passage (3179–3199):

1. "a disk ordinal is c · N + s, and N is the spatial-tile count, so the channel count enters
   the addressed-tile count C · N (§11.2) but no individual ordinal." — **TRUE.** C does not
   appear in c·N+s. Cross-checked against §21.3 row L2, which writes "C·N (which dominates the
   max disk ordinal (C−1)·N + (N−1))"; I computed (C−1)N+(N−1) = C·N−1, and for C=4,N=32 got
   127 = 4·32−1. Agrees.
2. Worked example, position by position. "A layer with N = 2 and channels (`a`, `b`) places `a`
   at ordinals 0 and 1 and `b` at 2 and 3" — a: 0·2+0=0, 0·2+1=1; b: 1·2+0=2, 1·2+1=3. **TRUE.**
   "appending `c` leaves those four where they are and adds 4 and 5" — c: 2·2+0=4, 2·2+1=5, and
   N is untouched by a channel append. **TRUE.** "exchanging `a` and `b` moves all four" — after
   the exchange b holds index 0 (ordinals 0,1) and a holds index 1 (ordinals 2,3), so each of
   the four tiles sits at a different ordinal than before. **TRUE.**
3. "reordering moves those channels the reorder re-indexes" — **TRUE** (ordinal is monotone in c
   with N fixed).
4. "inserting or removing one moves every channel after the affected position" — **TRUE for
   removal** (old indices > p fall by one); **off by one for insertion** under the natural
   reading in old indices: inserting at position p moves every channel with old index ≥ p, i.e.
   including the one that *was* at p. Insert at the front of (a,b): the script's "insert at
   front" line shows a's tiles going 0,1 → 2,3, and a was *at* position 0, not after it. The
   claim is only true if "the affected position" is read in the new indexing. → finding D-07.
5. "Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at all"
   — **TRUE holding geometry fixed** (append: no old index changes; remove-last: no surviving
   index changes; and the removed channel's own tiles leave the addressed set entirely, which
   the parallel shrink sentence at 3223–3226 classes as not an alteration). **FALSE without that
   proviso**, see 6.
6. "**A channel's tiles move exactly when its index does**" — **FALSE as an unqualified
   biconditional.** The ordinal is c·N+s and N is not a channel quantity. Script line
   "growth N=2->3, C=2": channel 1 keeps index 1 and its stored tile at s=0 moves from ordinal
   2 to ordinal 3. Any commit that changes a grid count Gᵢ = ⌈Eᵢ/Tᵢ⌉ moves every planar tile with
   c ≥ 1 while every index stands. → finding D-03, and it is the engine of D-04.
7. "An interleaved layer is unaffected, its disk ordinal being s, which no channel declaration
   enters." — **TRUE.** s = Σ tᵢ·∏_{j>i}Gⱼ contains no channel term.

Ordinal-move sources, enumerated exhaustively from c·N+s: (i) c changes — the new bar; (ii) N
changes — geometry; (iii) s changes — geometry. The re-emission rule at 3126–3128 covers (ii)
and (iii) with "(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)". So the
insertion does close the (i) hole its own rationale names. Byte-neutrality of the *permitted*
(i) cases checked separately: every tile the superseded generation did not store carries the
sentinel, which §15.2 [R-IDX-02] fixes at the constant 20 bytes `FF ×16 00 ×4`, so an ordinal
move confined to unstored tiles permutes identical entries and the re-emitted region is
byte-identical. No fork there.

## 5. Check 1 — tense and quantifier, per hunk

§3.1 supplies the definitions the whole passage rides on and I quote them because two findings
turn on them: "A tile is *stored in a generation* if and only if that generation's tile-index
entry for it is not the sentinel (§15); **unqualified *stored* means stored in the live
generation.**" And: "**sample** — the tuple of one value per channel at one coordinate."

- Hunk 02. The §14 bar's quantifier is untouched: "for any tile that layer stores **in the
  generation this commit supersedes**". The added list member introduces no quantifier of its
  own ("the sample type each value in the image is read under" ranges over values of one tile's
  image). Note the added member says "each **value**", which is the §14.2 usage (per channel per
  position), while its neighbour says "the byte offset of any **sample**", which by §3.1 is the
  whole tuple. The new member is the more precise of the two; the imprecision in the neighbour
  is pre-existing and I do not charge it to this repair. PASS.
- Hunk 03(a). "wherever the layer stores a tile that carries that channel" — generation left
  implicit in that clause, but supplied two sentences later and correctly: "Where the superseded
  generation stored no tile carrying that channel there is nothing to reinterpret". PASS.
- Hunk 03(b). "any tile the layer stores in the generation this commit supersedes" — matches the
  §14 bar verb for verb. PASS. Its restatement three sentences on, "a commit that moves only the
  ordinals of channels the superseded generation stored no tile for", also matches. PASS.
- Hunk 03(c). "the tense is both bars'" — both bars do carry the same tense. PASS.
- Hunk 04. "**in that bar's own tense**" and "any tile the layer stores in the generation this
  commit supersedes" — matches. PASS.
- Hunk 05. "it bars a change to a planar layer's channel declarations that moves **a stored
  tile's** disk ordinal" — FAIL. Unqualified *stored*, which §3.1 pins to the **live**
  generation, restating a bar quantified over the **superseded** one. → finding D-05.
- Hunk 06. "A layer that stored no tile **in the generation the commit supersedes**" replacing
  "A layer storing no tile", plus "a layer the commit itself empties does not qualify". This is
  exactly the normative sentence's tense at 3200–3204. PASS — and it is the repair that this
  round's tense discipline was aiming at.

## 6. Check 2 — every citation opened

| Cited in repaired text | Claim made | Verdict |
|---|---|---|
| §3.1 (hunk 02, "defines *stored* against a generation") | defines stored per generation | PASS — quoted above |
| §14 (name "the §14 bar") | §14 fixes stored bytes / decode | PASS as a section handle; §14's opening: "This section defines the **decoded tile image**". See §8 note on the list's looseness |
| [R-GEO-06] (hunk 03) | assigns a tile its disk ordinal | PASS — "The **disk tile ordinal** … is s … and **c · N + s**" |
| §11.2 (hunk 03, "the addressed-tile count C · N") | C·N is the planar addressed-tile count | PASS — [R-GEO-03] verbatim |
| §11.1 (hunk 03, "what schema-first creation needs") | empty layers serve schema-first workflows | PASS — §11.1 Rationale, 1602–1604 |
| [R-COD-07] + (L44) (hunk 03 context) | lz4 decoded-size cap quantified over addressed tiles | PASS — "any of whose **addressed** tiles' decoded size exceeds 0x7E000000"; its Note: "The cap is quantified over the layer's *addressed* tiles" |
| [R-ENC-04] (hunk 03 context) | 2⁶³−1 ceiling "on every quantity it designates" | PASS — "any quantity this specification **designates** … whose mathematical value would exceed 2⁶³ − 1"; the repair's verb "designates" is the rule's own |
| §14.5 (hunk 03, new) | a becoming-real position held, for each channel the position carries, that channel's fill | PASS — [R-SER-05] verbatim: "at every padding position, a writer MUST encode, **for each channel the position carries**, that channel's fill value". The repair lifts the phrase exactly |
| [R-TYP-05] (implied by "fill is a legal sample value") | every bit pattern is a valid fill and sample value | PASS — §12.3 |
| [R-LIF-01], §20.5 (hunk 03 context) | freeze / whole-file rewrite | PASS |
| [R-SLB-04] (hunk 04) | slab declaration re-established or cleared | PASS — §16.2 [R-SLB-04] verbatim |
| [R-SLB-01] (hunk 04) | per-tile alignment invariant | PASS — §16.1 |
| [R-CNT-17] (hunk 04's "entry_count", context below) | entry_count equals the addressed-tile count | PASS — §7.4 / L21 |
| [R-CNT-21] (context) | slack | PASS |
| §21.7 (hunk 05) | records that the §14 bar has no witness where the live state is clean | PASS — §21.7 Rationale: "a commit that supersedes every tile it would have damaged leaves the live state clean, so the §14 bar is unwitnessed there" |
| [R-CNT-25] (hunk 06 context) | a user-metadata document lives in an extent | PASS |
| [R-CNF-01] (my instrument) | normativity by label | PASS |

No citation failed. Two are worth naming as *passing narrowly*: §14 as the bar's handle (see §8)
and [R-COD-07]'s "empty layer escape", where the passage's word "empty" means *addresses none*
(the [R-COD-07] Note: "a layer that addresses none — any dimension extent 0") and not *stores
none* — the two are different sets, which is the pivot of finding D-06.

## 7. Check 7 — the analogies, verb against verb

(a) Hunk 03(b): "One effect is barred beside it, **on the same tense** and on its own ground".
    repair's verb: "any tile the layer **stores in the generation this commit supersedes**"
    warrant's verb: "any tile that layer **stores in the generation this commit supersedes**"
    Same set, same generation, same individuation (a tile). **Analogy holds.**

(b) Hunk 03(b): "the §14 bar does not reach it, an ordinal move being no effect on any stored
    tile's bytes". §14 bar's own reach is "alters … what §14 fixes for its **stored bytes** or
    how they **decode**". An ordinal move changes the *entry's position in the index region*,
    not the payload and not the decode. **Analogy holds** — and note it is the one place the
    passage's unqualified "stored" is harmless, because the sentence is about bytes, not sets.

(c) Hunk 03(b): "Where this bars a change the operation is a new layer or a whole-file rewrite,
    **exactly as above**." The "above" remedy is "Such a change is a new layer, or a whole-file
    rewrite under a fresh file_id (`[R-LIF-01]`, §20.5)". Same remedy, same two options.
    **Analogy holds** on its own terms — but the sentence it points at has been re-scoped by
    this same insertion (finding D-01), so "exactly as above" now points into a paragraph about
    re-typings. Reported there, not here.

(d) Hunk 04: "the obligations this step states below … bind a shrink **as they bind any
    commit**." Each named obligation checked: [R-CNT-21] slack, [R-CNT-17] entry_count,
    [R-SLB-04] slab, [R-SLB-01] alignment, and "A writer SHOULD instead produce a new file
    wherever a commit would strand a large share of a layer's stored bytes" — all five are
    stated below, at 3244–3258, and all five are written over commits generally, not over
    shrinks. **Analogy holds for each member, tested separately.**

(e) Hunk 05: "The bar beside the §14 bar does not reach a shrink either: **it bars** a change to
    a planar layer's channel declarations that moves a stored tile's disk ordinal, and a shrink
    is not one."
    repair's verb: "moves **a stored tile's** disk ordinal"
    the bar's verb: "alters the disk ordinal … assigns **any tile the layer stores in the
    generation this commit supersedes**"
    Different quantifier (§3.1: unqualified *stored* = live generation). **Analogy fails on the
    generation** → D-05. The conclusion it supports ("a shrink is not one") survives, because a
    shrink is not a channel-declaration change under either generation.

(f) Hunk 03(a): "the type is what fixes the value a stored bit pattern denotes". Warrant is
    §12.1's Definition column ("signed two's-complement integer" / "unsigned integer"). Checked
    against §12.3 [R-TYP-04] — "A sample value **is** its bit pattern … Wherever this
    specification treats two sample or fill values as the same value, it means their encoded
    bytes are identical; this format defines no numeric equality" — under which `0x80`-as-int8
    and `0x80`-as-uint8 are the same *value*, and only its out-of-format interpretation differs.
    I opened this as a candidate contradiction and closed it: [R-TYP-04] disclaims *equality and
    ordering*, not *denotation*, and §12.1 does assign denotations. See rejected candidates.

## 8. Check 5 — every completeness word in the repaired text, falsified where possible

- "**exactly** when its index does" — FALSIFIED, §4 item 6. → D-03.
- "moves **no** ordinal **at all**" — falsified in the same way when the same commit changes a
  grid count. → D-03.
- "**every** channel after the affected position" — off by one for insertions read in old
  indices. → D-07.
- "**the whole** layer's worth" — FALSIFIED for the planar re-type the sentence now glosses:
  [R-LIF-01] strands only the payloads actually re-emitted, and a planar re-type of one channel
  reaches only that channel's own tiles. → D-02.
- "the §14 bar is **the whole of** the test **of what a shrink alters**" — the qualifier the
  repair adds is exactly what makes this survivable; tested against the five obligations in
  §7(d). HOLDS.
- "What counts as such an alteration is the §14 bar **and nothing else**, its carve-out
  included" — holds now that hunk 05 adds the companion-bar exclusion beside it.
- "**both** bars'" / "the bar **beside** the §14 bar" / "**Its companion** bar" (§21.7, 3949) /
  "Of its **two** bars" (§11.1, 1606) — I counted the MUST NOTs in step 4 myself:
  (i) 3131 "A commit MUST NOT change a layer's declarations in a way that alters …";
  (ii) 3179 "a commit MUST NOT change the channel declarations in a way that alters the disk
  ordinal …". Two. (Step 2 carries two further MUST NOTs, at 3103 and 3105, but they bind an
  appender's repair behaviour, not a commit's declarations, and no count claim reaches them.)
  Every count claim in the document — 1606 "two bars", 3203 "both bars'", 3237 "The bar beside
  the §14 bar", 3949 "Its companion bar" — agrees with the count of two. **The withdrawal was
  swept everywhere I can find.** PASS, and this was the check I most expected to fail.
- "the list is not offered as exhaustive" (3209, context) — the growth-bound list. Honest.
- "**exactly** thirteen sample types" (§12.1) — unrelated but checked while there; the table has
  13 rows, IDs 1–13. Agrees.

## 9. Check 4 — contradiction in the passage, including untouched text

Read the whole of step 4 (3117–3258) and the whole Example block (3315–3340) sentence by
sentence, looking for the three shapes the charter names.

1. **A carve-out the new breadth collides with.** The §14 bar's list names "the set of padding
   positions (§11.3)", and a *growth* alters that set — yet "an extent MAY **grow**" sits three
   sentences later. This is pre-existing and is resolved, deliberately, by 3147–3148: "The test
   is the effect on such a tile, and the list names where that effect arises **rather than
   standing on its own**." No new collision from hunks 02–06. But that same sentence is what
   makes the added list member subordinate rather than self-executing — see D-08's neighbour
   discussion and the rejected candidate on the §14 handle.
2. **A MUST elsewhere the new MAY lets an actor violate.** The permissions the passage grants
   (re-type a stores-nothing channel; append or remove-last a channel; grow; shrink) were each
   run against L44 ([R-COD-07]), L21/L22 ([R-CNT-17]), L2 ([R-ENC-04]), [R-SLB-04], [R-SLB-03].
   Every one of those fires as a register row on the produced file, so [R-CNF-05] bars the
   emission under any reading — no permission here licenses a nonconforming file. What the
   passage *does* do is state the proviso for one permission and withhold it from its siblings
   → D-06.
3. **A sentence written to be true only under the old wording.** Found one, and it is the
   insertion's own doing: "Where a change does reach them it makes each stored tile it reaches
   nonconforming, and re-emitting those tiles would strand the originals as slack — the whole
   layer's worth …". Under the old text this sentence stood one sentence after "is not what this
   bars" and spoke for the §14 bar entire. The hunk-03 insertion spliced two paragraphs in front
   of it, and it now closes the sample-type paragraph. → D-01 and D-02.
4. **Internal pull inside the new paragraph.** "Appending a channel … moves no ordinal at all"
   versus "**The test is the effect on a stored tile, not the shape of the edit**". For a commit
   that both appends a channel and changes a grid count, the first says the append is inert and
   the second says the effect is what counts — and the effect is that stored tiles moved. → D-04.
5. Checked and clean: the shrink paragraph's rescue sentences (3220–3231) against the new
   classifying paragraph; Example (b)'s "a commit that supersedes stored tiles takes the same
   shape" against the §14 bar's "superseding every tile of a layer and re-declaring it are one
   operation, and this bars it" — (b) is about superseding *without* re-declaring, no collision;
   §23.1's "§20.3 step 4 permits that shrink only where those bytes already hold the channel's
   recorded fill" against the shrink carve-out — agrees.

## 10. Check 6 — the structure, and what is still unconstrained

**Structure A — the channel declaration.** §12 head: "A channel is declared by its layer
record's channel entry (§7.4): a **name** (§4.6), a **sample type** (`u16`, structural), and a
**fill value** (§13)." Plus two layer-level facts derived from the set: **channel order/index**
(§3.1: "the order is load-bearing") and **channel count C**.

| member | governed after the repair? |
|---|---|
| sample type | YES — new list member (hunk 02) + classifying paragraph (hunk 03) |
| fill value | YES — via the list's "the content `[R-SER-05]` fixes there", and Example (c) |
| name | Not governed, and correctly so: a rename alters no byte and no decode |
| index / order | YES for planar (new bar); for interleaved, only through the §14 bar's list — and I could not construct a harmful uncovered case: a reorder changing element sizes moves value offsets, one changing types trips the *new* list member, one changing fills breaks §14.5 padding content, and the residue (same type, same size, same fill) is byte-inert and semantically identical to two renames, which are free. **Coverage is complete.** |
| count C | Reaches entry_count (L21), extent_length (L22), C·N (L2), the slab run partition ([R-SLB-04]), the lz4 cap ([R-COD-07]) — all register-rowed, none named in the new permission → D-06 |

**Structure B — the §14 bar's list of loci.** Members after the repair: padding-position set;
the content [R-SER-05] fixes there; decoded size; a sample's byte offset in the image; the
sample type each value is read under; the codec and filter. **Pad bits are absent.** §14.3's
Note is explicit that "Pad bits are **not** padding positions (§11.3)", yet [R-SER-05] fixes
them ("Every pad bit (§14.3) MUST carry the plane's channel's fill bit") and Example (c), whose
neighbouring sentence hunk 06 edited, relies on step 4 reaching them: "changing a channel's fill
value on a layer with **no padding position and no pad bit** … A fill change on a layer that
**stores** a tile carrying **either** is not an appender's operation at all (step 4)". The list
was reopened by hunk 02 and this sibling was not added. → D-08.

**Structure C — the disk ordinal.** Enumerated in §4: c, N, s. All three now accounted for
between the new bar and the geometry parenthetical, with the seam at D-04.

## 11. Check 8 — every back-reference from each insertion to the end of the subsection

Insertions: hunk 02 (one clause + "Call this the §14 bar."), hunk 03 (two paragraphs), hunk 04
(one clause), hunk 05 (one sentence), hunk 06 (one clause).

| back-reference | resolved BEFORE | resolves NOW | changed? |
|---|---|---|---|
| 3146 "and this bars it" | the §14 bar | unchanged (hunk 02 inserted only before it, inside the same sentence-run) | no |
| 3147 "The test is the effect on such a tile" | a tile stored in the superseded generation | same | no |
| 3152 "is not what this bars" | the §14 bar | same | no |
| 3164 "**this** bars nothing" (new) | — | the §14 bar, named 12 lines up | new text, resolves correctly |
| **3166 "Where a change does reach *them*"** | **the §14 bar's "any tile that layer stores in the generation this commit supersedes", one sentence back** | **the nearest plural antecedents are now "a layer that stores nothing" / "a planar channel none of whose own tiles are stored", i.e. the re-typed channel's tiles** | **YES → D-01** |
| 3170 "re-emitting **those** tiles" | the same set | rides on "them" | YES, same defect |
| 3173 "**Such a change** is a new layer" | any §14-bar-reaching change | a re-typing | YES, same defect |
| 3175 "barred beside **it**" (new) | — | the §14 bar | new text, correct |
| 3177 "the re-emission rule **above**" (new) | — | 3117–3129, the entry-placement rule. Correct, though "above" now has to reach past two intervening paragraphs | no defect, noted |
| 3193 "alters nothing **this** bars" (new) | — | the ordinal bar | correct |
| 3198 "exactly as **above**" (new) | — | 3173's remedy sentence — which D-01 has re-scoped | inherits D-01 |
| 3203 "the tense is **both bars'**" | was "the bar's" = the §14 bar | both, explicitly | repaired, correct |
| 3215 "**the §14 bar** is the whole of the test" | was "the bar above" — nearest antecedent would now be the *ordinal* bar | named | **repaired before it could break — this is the insertion's own anaphor hazard, correctly anticipated** |
| 3232 "is **the §14 bar** and nothing else" | was "the bar above" — same hazard | named | repaired |
| 3237 "The bar beside the §14 bar" (new) | — | the ordinal bar | correct, but mis-quantified → D-05 |
| 3241 "**this** is precisely where the §14 bar has no witness" | was "the bar" | named | repaired |
| 3328 "a layer the commit itself empties does not qualify" (new) | — | the permission in the same sentence | correct |
| 3329 "Editing user metadata is not **this shape**" | shape (c), fixed by the block's own heading | unchanged | no |
| 3339 "as in (b)" | shape (b) | unchanged | no |

Backwards run: does the inserted text itself lean on a distant antecedent? "the re-emission rule
above" (3177) reaches ~60 lines back, and "exactly as above" (3198) reaches past the paragraph
break. Both resolve, but the second lands on the sentence D-01 concerns.

**The two "bar above" anaphors that the naming repair fixed (3215, 3232) are precisely the ones
the insertion would otherwise have broken.** That is the repair working. The one it did not
protect is the "them"/"those"/"such a change" chain at 3166–3173, which no naming could fix
because the antecedent there is a *set of tiles*, not a bar.

## 12. Byte-level determination, finding by finding

Discriminator applied: is the file a permissive reading lets a writer produce itself conforming?
If it carries a register-row violation, [R-CNF-05] bars it under both readings and the
emittable set does not move.

- D-01, D-02, D-03, D-07: no. These misstate scope or a quantity in prose whose operative
  MUST NOTs still read correctly; no file becomes emittable or unemittable.
- D-04: **yes.** Writer W1 (effect reading) refuses a single commit that grows a planar layer's
  extent past a grid-count boundary while appending a channel, and emits either two commits or a
  new layer; writer W2 (causal reading) emits one commit. The one-commit file is conforming —
  its live layer satisfies §11.2, §15, §14; §21.7 states the companion bar is witnessed "only
  sometimes" and never for what the prior generation held. The two files differ by a whole
  directory, pad and trailer, and by every subsequent offset.
- D-05: no, on an honest reading. The fork it would open (reorder-plus-unstore in one commit) is
  real only for an implementer who takes a gloss over the rule it glosses, when the rule's own
  words sit 55 lines up in the same numbered step and use the explicit phrase. Two *competent*
  implementations converge. I record it as the highest-priority wording fix all the same,
  because in a document whose last four rounds each failed on a tense this is the exact shape.
- D-06: no. Every bound it fails to name (L44, L21, L22, L2, [R-SLB-03]) is a register row.
- D-08: no. A stale pad bit is [R-SER-05]'s violation, a tile-scope validity error with rows in
  §21.4; [R-CNF-05] bars the emission under either reading of the list.

## 13. Candidates opened and closed

- *The §14 bar's handle.* "the sample type each value in the image is read under" sits in a list
  appositive to "what **§14** fixes", but the sample type is declared in §12 and §14 only
  consumes it. Closed: the list already contains two members §14 does not itself fix — "the set
  of padding positions (**§11.3**)" and "the codec and filter" (§17) — so the handle was never a
  claim about section ownership; and §14.1's "value k of the sequence is channel c's value" plus
  [R-SER-07]'s "decoded size is a function of the layer's declarations alone — geometry, layout,
  and **channel types**" put the type inside §14's own machinery.
- *[R-TYP-04] against the classifying paragraph's warrant.* "A sample value **is** its bit
  pattern … this format defines no numeric equality" versus "the same bytes denote different
  values". Closed: [R-TYP-04] disclaims equality, ordering and comparison, not denotation, and
  §12.1's Definition column supplies the denotations the example uses. The bolded rescue —
  "**The test is on the declared types and not on the values a tile happens to hold**" — keeps
  the rule decidable from the record, which is what [R-MDL-02] and [R-TYP-04] actually care
  about.
- *Interleaved channel reorder as an uncovered sibling of re-typing.* Enumerated in §10;
  every harmful case is caught, and the residue is equivalent to two renames, which are free.
- *"the obligations this step states **below**" (hunk 04) excluding the re-emission rule stated
  above.* Closed: the sentence includes, it does not exclude, and "as they bind any commit"
  generalises correctly.
- *"a planar channel" as a novel construction* (§3.1 makes planar a property of the layer's
  channel layout, not of a channel). Closed as a wording nit with no reading consequence; the
  phrase "none of whose own tiles are stored" pins the referent.
- *The "carries" direction.* Checked every occurrence: §14.1 "the tile … **carries** exactly the
  values of channel c" and "the tile at spatial ordinal s **carries all C channels**"; §3.1
  "one cell of the tiling grid **carrying all channels**"; §13 "each channel it **carries**
  reads as fill"; §14.5 "for each channel the **position carries**". The document's rule is:
  a tile (or a position) carries a channel, never the reverse. Hunk 03's "a tile that carries
  that channel" and "for each channel the position carries" both go the document's way. Closed
  clean — this was the charter item I most expected to catch something.
- *Whether the withdrawn rule left a stale count.* §8 above; every count says two and there are
  two. Closed.

## 14. Findings

D-01  hunk 03  the insertion re-scopes the untouched consequence sentence at 3166–3174
D-02  hunk 03  "the whole layer's worth" is false in the paragraph it now closes
D-03  hunk 03  "A channel's tiles move exactly when its index does" is a false biconditional
D-04  hunk 03  the ordinal bar's reach on a combined channel-edit + geometry commit (byte-level)
D-05  hunk 05  the companion bar restated with §3.1's live-generation "stored"
D-06  hunk 03  the re-type / channel-count permissions carry no proviso where their sibling does
D-07  hunk 03  "every channel after the affected position" is off by one for an insertion
D-08  hunk 02  the reopened §14-bar list still omits pad bits, which Example (c) relies on

## 15. Correction to §5 and §12, made on a re-read of lines 3175–3199

On re-reading the ordinal paragraph line by line with the line numbers in front of me I found a
second, worse instance of D-05's defect, inside hunk 03 rather than hunk 05, and it changes the
byte-level verdict.

Line 3191–3193, the paragraph's own statement of its test:

    **The test is the effect on a stored tile, not the shape of the edit**: a
    commit that moves only the ordinals of channels the superseded
    generation stored no tile for alters nothing this bars.

The two halves of that one sentence are quantified over different generations. The bolded half
says "**a stored tile**", which §3.1 fixes: "unqualified *stored* means stored in the **live**
generation." The half after the colon says "the **superseded** generation stored no tile for".
The bar the sentence is testing (3181–3182) says "any tile the layer **stores in the generation
this commit supersedes**".

Consequence, concretely. Planar layer, N = 2, channels (`a`, `b`), the superseded generation
stores both of `a`'s tiles at ordinals 0 and 1. One commit exchanges `a` and `b` **and**
supersedes both of `a`'s tiles to unstored (their entries become the sentinel). Under the bar's
own words: `a` moved, the superseded generation stored tiles for it, barred — the operation is a
new layer or a whole-file rewrite. Under the bolded test read with §3.1's definition: after the
commit no tile is stored at a moved ordinal, so there is no "effect on a stored tile", permitted.
The resulting file's live state is a valid planar layer with a full sentinel index for `a`;
§21.7 says of this same bar that it is "witnessed indirectly and only sometimes" and that "no
check knows which ordinal a stored tile used to occupy". So the file is conforming and only one
reading permits a writer to produce it. **Byte-level: yes.**

The passage does contain its own antidote — 3202–3204, "the tense is **both bars'**, so a commit
does not earn this permission by emptying the layer as it re-declares it" — but that sentence is
attached to the *free-re-declaration permission*, not to the bolded test, and the §14 bar's
equivalent warning ("a commit does not escape this by unstoring in the same breath", 3143–3146)
was written out longhand for the §14 bar and not for its companion. The companion bar got the
name, the tense in its operative sentence, and then a test sentence in the other tense.

D-05 is therefore restated as spanning hunk 03 (line 3191, the bolded test — the serious one)
and hunk 05 (line 3239, "moves a stored tile's disk ordinal" — the same slip in a gloss), with
byte_level = true. §11.1's Rationale at 1619–1620 carries the third instance ("that moves a
stored tile's disk ordinal"); being *Rationale*-labelled it has no force, but it should be swept
with the other two so the three agree.

The rest of §5's per-hunk verdicts stand. Line 3177's "no effect on any stored tile's bytes" is
the same bare word but is harmless: it is a claim about bytes, true in either generation.
