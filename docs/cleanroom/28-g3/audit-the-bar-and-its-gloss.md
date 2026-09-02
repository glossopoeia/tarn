# Audit transcript — hunk-02 and hunk-03, ADR-0113 repair set
# Lane: "the bar and its gloss"

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../case-adr0113/hunk-02.diff` (whole file)
- `/private/tmp/.../case-adr0113/hunk-03.diff` (whole file)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, ranges:
  3060–3260 (§20.2 tail + all of §20.3 step 4 and the shrink paragraph),
  1590–1720 (§11.1 incl. its Rationale, §11.2, §11.3, §11.4 incl. [R-GEO-06]),
  1720–1830 (§12 entire, incl. §12.3 [R-TYP-04]/[R-TYP-05], and §13 head),
  1922–2120 (§14 entire: §14.1–§14.5),
  2122–2166 (§15.1, §15.2),
  1067–1095 (§7.4 layer-record inline-payload table),
  341–402 (§3.1 Terms),
  1224–1240 (§9.1 [R-LIF-01], §9.2 head),
  3260–3345 (the "three shapes a commit takes" Example block, §20.4 head),
  3862–3960 (§21.7 entire, §21.8),
  plus the single-line grep hits reproduced verbatim in §2 below.

Did NOT read: full.diff, any other hunk file, the case directory listing,
docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/,
spec/registry.json, git history/log/diff, the web.

Commands run: `sed -n`, `awk`, `grep -n`, `grep -c`, `tr`. No writes to the
repo. Nothing executed against any file other than spec/tarn.md and the two
hunk files.

**Unrequested context.** Material appeared in my context before I began: a
project CLAUDE.md pointer, a user auto-memory index with two entries naming
this project's harness and a "lineage gate", and an MCP/tooling preamble.
None of it is part of the specification. I did not open any file it named and
no conclusion below rests on it. Naming that it appeared, not repeating it.

## 1. The hunks, and what rule each adopts

**hunk-02** (lands at 3140–3141). Inserts one sentence into the §14-bar
paragraph: `Call this the **§14 bar**.` It adopts no new obligation. What it
makes true of an implementation: nothing directly; it supplies a name that
three other passages (§11.1 Rationale, §21.7, §20.3's shrink paragraph) already
use, and it converts three later anaphors ("this", "the bar's") into
name-anchored references.

**hunk-03** (lands at 3151–3205). Inserts two paragraphs and edits two
sentences. The rules it adopts:

(a) *Sample-type classification.* A channel's declared sample type counts as a
"layer declaration" for the §14 bar, and re-typing it counts as a barred
"change", wherever the layer stores a tile carrying that channel. Effect on an
implementation: an appender must refuse a commit that re-declares a channel's
type on a layer with a stored tile carrying it, and may re-type freely
otherwise. It is stated classificatorily (no MUST of its own), hooking into
the §14 bar's MUST NOT.

(b) *Planar disk-ordinal bar.* A fresh `MUST NOT`: for a planar layer, a commit
may not change channel declarations in a way that alters the disk ordinal
[R-GEO-06] assigns any tile stored in the superseded generation. Effect: an
appender must refuse channel reorders/insertions/removals that re-index a
channel with stored tiles; appends and last-removals are free; interleaved
layers are wholly outside it.

(c) Two sweeps in untouched-adjacent text: "the tense is the bar's" →
"the tense is both bars'", and the growth clause's bare "held that channel's
fill" → "held, for each channel the position carries, that channel's fill
(§14.5)".

Header check: both hunk headers name "line 3073, 20.3 The append procedure" as
the nearest preceding heading. Verified — line 3073 is `#### 20.3 The append
procedure`, and both landings (3140, 3151–3205) fall inside it, in numbered
step 4 of "An appender MUST, in order:". No mismatch.

## 2. Sweeps run, verbatim, with hit counts

    grep -n "R-GEO-06" spec/tarn.md                      -> 6 hits (1626,1703,2971,3127,3180,3886)
    grep -n "14 bar" spec/tarn.md                        -> 11 hits (1606,1616,3140,3175,3214,3231,3236,3240,3896,3911,3935)
    grep -n "carries" spec/tarn.md                       -> 61 hits
    grep -n "carrying" spec/tarn.md                      -> 27 hits
    grep -n "R-CNT-17" spec/tarn.md                      -> 10 hits
    grep -n "R-CNT-21" spec/tarn.md                      -> 10 hits
    grep -n "R-COD-07" spec/tarn.md                      -> 5 hits
    grep -n "R-LIF-01" spec/tarn.md                      -> 11 hits
    grep -n "R-CNT-23" spec/tarn.md                      -> 16 hits
    grep -n "R-WRT-04" spec/tarn.md                      -> 4 hits
    grep -n "^| L44 " spec/tarn.md                       -> 1 hit  (3730)
    grep -ni "re-declar\|redeclar" spec/tarn.md          -> 6 hits (1615,3144,3200,3203,3325,3912)
    grep -ni "re-typ\|retyp" spec/tarn.md                -> 3 hits (1616,3163,3897)
    grep -n "sample type" spec/tarn.md                   -> 8 hits
    grep -n "disk ordinal\|disk-ordinal" spec/tarn.md    -> 20 hits
    grep -c "affected position" spec/tarn.md             -> 1
    grep -c "denote" spec/tarn.md                        -> 10   (locations: 404,1763,1765,1770,3156,3158,3495,3677,3678,4265)
    grep -c "layer record" spec/tarn.md                  -> 58
    grep -c "such a change" spec/tarn.md                 -> 3
    grep -c "stores a tile" spec/tarn.md                 -> 3    (1617, 3154, 3185)
    grep -c "stored a tile" spec/tarn.md                 -> 0
    grep -n "generation this commit supersedes" spec/tarn.md -> 4 hits (3135,3181,3200,3222)
    grep -n "the live generation" spec/tarn.md           -> 3 hits (374,1877,4199)
    grep -c "spatial-tile count" spec/tarn.md            -> 2
    tr '\n' ' ' < spec/tarn.md | grep -o "store[sd] no tile[^.]\{0,60\}"   -> 6 hits (wrap-safe)
    grep -n "^#\+ " spec/tarn.md                         -> full heading inventory (used to bound §§)

Hard-wrap discipline: every multi-word phrase above was chosen short enough
that it cannot straddle the document's wrap column, and the two phrases that
could ("stores no tile", "stored no tile") were re-run through a
whitespace-normalising `tr | grep -o` so a wrapped instance could not hide.
The 6 wrap-safe hits are reproduced in the tool log; they are lines 1615,
3162, 3164, 3191, 3199, 3325 plus one unrelated ("stores no tile whose samples
all equal fill", Appendix G).

## 3. Citations opened, one by one

| Citation in repaired text | Where | Verdict |
|---|---|---|
| `[R-GEO-06]` (3180, 3187 by implication) | §11.4, line ~1700 | **PASS.** "The **disk tile ordinal**, which orders tile-index entries (§15), is s for an interleaved layer, and **c · N + s** for a planar layer (§14), where c is the channel's index (§3.1)". Exactly the formula the repair uses. |
| `§11.2` (3189, for "the addressed-tile count C · N") | §11.2 [R-GEO-03] | **PASS.** "its **addressed-tile count** — the number of its tile-index entries (§15) — is N for an interleaved layer and C · N for a planar layer, where C is the channel count". Also confirms N = ∏ Gᵢ is the "spatial-tile count", as 3188 says. |
| `§14.5` (3205, for "that channel's fill") | §14.5 [R-SER-05] | **PASS, verbatim.** "at every padding position, a writer MUST encode, **for each channel the position carries, that channel's fill value**". The repaired clause reproduces the phrase word for word. This is a good repair. |
| `§11.1` (3201, "what schema-first creation needs") | §11.1 Rationale | **PASS as a pointer.** §11.1's Rationale block says "Empty layers serve schema-first workflows: declare layers at creation, grow extents as data arrives." Note the block is labeled **Rationale.** and is therefore non-normative under [R-CNF-01] — but the MAY it supports sits in §20.3 step 4 (normative), so the rule is not homeless. |
| `[R-COD-07]` + `(L44)` (3206–3208) | §17.2 / register row L44 (3730) | **PASS.** L44: "Codec 4 (lz4) declared on a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000 bytes — in a planar layer the largest channel plane governs". So the cap *is* quantified over addressed tiles and an extent-0 layer escapes it vacuously, exactly as 3208–3209 says. |
| `[R-ENC-04]` (3209) | §4.2 / [R-GEO-03] etc. | **PASS.** Its 2⁶³−1 ceiling on declaration-derived quantities is repeatedly invoked (1625, 2472, L2 at 3688). L2 even prints "C·N (which dominates the max disk ordinal (C−1)·N + (N−1))" — an independent confirmation of the c·N+s formula. |
| `[R-LIF-01]` (3169, 3172) | §9.1, line 1231 | **PASS.** "Bytes in [0, F) … are immutable: a writer MUST NOT modify them, and every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id (compaction, §20)." Supports both "freezes them where they lie" and "a whole-file rewrite under a fresh file_id". |
| `§20.5` (3172) | §20.5 Compaction | **PASS.** Compaction is the whole-file-rewrite operation. |
| `§3.1` (3142, context) | §3.1 Terms, line 372–376 | **PASS with a caveat that matters — see finding A-01.** "A tile is *stored in a generation* if and only if that generation's tile-index entry for it is not the sentinel (§15); **unqualified *stored* means stored in the live generation.**" |
| `§11.3`, `[R-SER-05]`, `[R-COD-10]` (context, 3137–3150) | §11.3, §14.5, §17.3 | **PASS** (untouched bar text; checked because the gloss leans on them). |

No citation in either hunk points at a rule that only *almost* says the claimed
thing, with the single exception recorded as A-05 ("the layer record alone",
which is not a citation but a structural claim, and which fails).

## 4. Check 3 — normative placement (label test, not marker test)

I applied the **label** test required by [R-CNF-01], not the ">" test.

- hunk-02's sentence lands at 3140, inside numbered item 4 of "An appender
  MUST, in order:". No ">" marker; no **Note.**/**Example.**/**Rationale.**
  label anywhere in the enclosing structure. **Normative.**
- hunk-03's two inserted paragraphs (3153–3172, 3174–3198) sit in the same
  numbered item 4. No ">" marker; no label. **Normative.** The ordinal bar
  carries its own `MUST NOT` (3179). The sample-type paragraph carries no
  modal at all — it is classificatory, borrowing the §14 bar's MUST NOT. That
  is not a placement failure, but it is the hinge of finding A-04.
- The rule's restatements elsewhere, and their labels:
  - **1604–1628, §11.1** — block opens `> **Rationale.**` → **non-normative**.
    It restates both bars ("Re-typing a channel is the §14 bar's own subject,
    barred wherever the layer stores a tile that carries that channel, and
    free where it does not"; "The other bar … bars a change to a planar
    layer's channel declarations that moves a stored tile's disk ordinal").
    Swept correctly and consistently. Because it is labeled, it carries no
    force; the normative home is §20.3 step 4, which exists. **No defect.**
  - **3286–3339, §20.3** — block opens `> **Example — the three shapes a
    commit takes.**` → labeled *Example* → **non-normative**. Its (c) says
    "A layer that stored no tile in the generation the commit supersedes is
    re-declared freely … a layer the commit itself empties does not qualify" —
    tense correctly stamped here, unlike in the repaired paragraph. Swept.
  - **3896–3903, §21.7** — plain prose under `[R-ERR-01]`, no label →
    **normative**. It already presupposes both bars: "§20.3 step 4's **§14
    bar** … a re-typed channel among the cases it does not reach [i.e. no
    witness]" and "Its companion bar on a planar layer's disk ordinals is
    witnessed indirectly and only sometimes". Consistent with both hunks.
    Swept.

So: the repaired rules have a normative home, and every restatement I could
find was swept. No NORMATIVE_PLACEMENT defect.

## 5. Check 1 — tense and quantifier

Reference quantifiers, quoted:

- §14 bar (3133–3135): "for any tile that layer stores **in the generation
  this commit supersedes**" — stamped, and bolded.
- Ordinal bar (3180–3181): "any tile the layer stores in the generation this
  commit supersedes" — stamped.
- The MAY (3199–3200): "A layer that stores no tile **in the generation this
  commit supersedes**" — stamped, and bolded.
- Shrink paragraph (3221–3222): "any tile the layer stores in the generation
  this commit supersedes" — stamped.

That is 4 of the 4 hits of the phrase in the whole document, all inside step 4.
The document stamps this quantifier every single time it states it — except in
the inserted sample-type paragraph, where it is stamped **once** (in the
negative governing clause at 3161–3162) and left **bare four times**:

1. 3154: "wherever the layer **stores** a tile that carries that channel"
   — the *positive* half of the rule, i.e. the half that bars anything.
2. 3163–3164: "re-typing a channel of a layer that **stores nothing**"
3. 3164–3165: "or a planar channel none of whose own tiles **are stored**"
4. 3190: "The test is the effect on **a stored tile**" (ordinal paragraph)

§3.1 supplies a default for the bare form: "unqualified *stored* means stored
in **the live generation**." For an appender the live generation is contested —
before the commit it is the superseded one, after the commit it is the new one
— and the passage's own next-but-one sentence exists precisely to kill that
reading: "a commit does not earn this permission by emptying the layer as it
re-declares it" (3202–3203), which mirrors the bar's own "a commit does not
escape this by unstoring in the same breath" (3142–3144).

Read post-commit, item 2 above ("re-typing a channel of a layer that stores
nothing") grants exactly the permission 3202–3203 denies. **Finding A-01.**

## 6. Check 7 — the analogies, verb against verb

| Repaired text's analogy | Repair's governing words | Cited rule's governing words | Same set? |
|---|---|---|---|
| 3174 "on the same tense" (ordinal bar ≡ §14 bar) | "any tile the layer **stores in the generation this commit supersedes**" | "any tile that layer **stores in the generation this commit supersedes**" | **Identical, word for word. PASSES.** |
| 3197–3199 "Where this bars a change the operation is a new layer or a whole-file rewrite, **exactly as above**" | "a new layer or a whole-file rewrite" | 3170–3172 "Such a change is a new layer, or a whole-file rewrite under a fresh file_id (`[R-LIF-01]`, §20.5)" | Same remedy. Tested separately for each bar: a re-typing can be re-homed to a new layer (new type, tiles re-stored) ✔; an ordinal move can be re-homed to a new layer (reordered channels, tiles re-stored) ✔. **PASSES.** The citations are dropped in the restatement; harmless. |
| 3153–3157 "is **such a** declaration, and changing it is **such a** change" (the sample-type gloss's warrant) | "changing it is such a change wherever the layer **stores** a tile that **carries** that channel" | §14 bar: "alters … what §14 fixes for its stored bytes **or how they decode**"; and its own gloss: "a change that leaves every one of those tiles' stored bytes **meaning exactly what they meant** … is not what this bars" | **Passes on the "meaning" clause; fails on the enumeration.** See §7 below and A-04. |
| 3189 "the addressed-tile count C · N (§11.2)" | "the channel count **enters** the addressed-tile count" | [R-GEO-03] "its addressed-tile count … **is** N for an interleaved layer and C · N for a planar layer" | **PASSES.** |

## 7. The central question: does the sample-type paragraph follow from the bar?

Put side by side.

Bar's test (3133–3136): "alters, for any tile that layer stores in the
generation this commit supersedes, **what §14 fixes for its stored bytes or
how they decode**", followed by the enumeration: "the set of padding positions
(§11.3) and the content [R-SER-05] fixes there, the decoded size, the byte
offset of any sample within the decoded tile image, or the codec and filter
that produced the stored bytes."

Bar's own gloss on that test (3145–3151): "The test is the effect on such a
tile, and **the list names where that effect arises** rather than standing on
its own: a change that leaves every one of those tiles' stored bytes **meaning
exactly what they meant** … is not what this bars."

Gloss's claim (3153–3157): re-typing "is such a change".

I derived the four enumerated quantities for a **same-element-size numeric
re-typing** (int8↔uint8; int16↔uint16↔float16↔bfloat16; int32↔uint32↔float32;
int64↔uint64↔float64 — all pairs share an element size per §12.1's table),
with the fill bytes left unchanged:

- Padding positions: §11.3, a function of Eᵢ mod Tᵢ only. **Unchanged.**
- Padding content: §14.5 fixes it to the channel's recorded fill bytes; the
  fill field is unchanged and its length equals the element size, which is
  unchanged. **Unchanged.**
- Decoded size: planar numeric P·Bᶜ (§14.2 table) — Bᶜ unchanged → **unchanged**;
  interleaved P·Q with Q = ΣBᵢ — every Bᵢ unchanged → **unchanged**.
- Byte offset of any sample: planar k·Bᶜ → **unchanged**; interleaved
  (k div C)·Q + F_{k mod C} with Fᶜ = Σ_{j<c} Bⱼ → **unchanged**.
- Codec and filter: separate record fields. **Unchanged.**

So a same-width re-typing's effect arises at **none** of the four places the
list "names where that effect arises". §21.7 confirms the drafters know this
class exists: "Which case a type change falls in is not decided by the element
sizes of §12.1: a planar `uint8` channel re-declared `bool` keeps its element
size of 1 while its plane goes from P · Bᶜ bytes to ⌈P/8⌉" — i.e. the
*element-size-preserving* cases are precisely the ones §21.7 leaves without a
witness ("a re-typed channel among the cases it does not reach").

Does the claim nonetheless follow? **Yes, from the "meaning" clause, not from
the list.** The bar's carve-out sentence tests whether the change "leaves every
one of those tiles' stored bytes meaning exactly what they meant". Re-typing
`int8`→`uint8` does not: 0x80's denotation changes. So the entailment holds on
the bar's *stated* test. I opened this as a candidate byte-level defect (the
gloss widening the bar) and **closed it** on that clause. What survives is
narrower and is recorded as A-04: the enumeration, which the bar says names
where the effect arises, was not swept to name the place this one arises.

And the warrant sentence collides with a defined term — A-03.

## 8. Check on the quantifier's reach — every layer shape I could build

Rule under test (3153–3155): barred "wherever the layer stores a tile that
carries that channel".

Relation check first. "a tile **carries** a channel" is the document's own
relation, and it agrees everywhere:
 - §3.1 (368): "in an interleaved layer, one cell of the tiling grid **carrying
   all channels**; in a planar layer, one cell of the grid **for one channel**".
 - §3.1 (378): "wherever the tile **carrying that channel** is not stored".
 - §13 (1828): "each channel it **carries** reads as fill".
 - §14.1 (1937, 1941): "the tile with disk ordinal c·N+s **carries** exactly the
   values of channel c"; "the tile at spatial ordinal s **carries** all C
   channels".
 - §11.4 Example (1710): "the tile **carrying channel 2**".
 - Register row T4 (3750) and §21.6 (3815) both use "for each channel it carries".
The repaired text's 3204 "for each channel the **position** carries" is the
other, also-attested relation, and it matches §14.5 (2091) verbatim. **No
disagreement anywhere.** Nowhere does the document say a channel carries a tile.

Shape-by-shape, with whether the answer follows from the words:

| Layer shape | Re-typing barred? | Follows from the words? |
|---|---|---|
| Interleaved, ≥1 stored tile | Yes, for every channel | Yes — §14.1: an interleaved tile carries all C channels, so any stored tile carries the channel. |
| Interleaved, stores nothing | No | Yes — explicit at 3163 ("a layer that stores nothing"), tense caveat A-01. |
| Planar, C=2, tiles stored for `a` only | `a` yes, `b` no | Yes — §14.1: a planar tile carries exactly one channel; 3164's "a planar channel none of whose own tiles are stored" names this case. |
| Planar, stores nothing | No | Yes. |
| C=1, N=1, extent 1, one stored tile | Yes | Yes — the single tile carries the single channel under either layout. |
| Extent 0 in any dimension | No | Yes — Gᵢ = ⌈0/Tᵢ⌉ = 0 ⇒ N = 0 ⇒ no addressed tile ⇒ none stored ([R-GEO-02], [R-GEO-03]). |
| Planar, C=1, tile stored | Yes | Yes. |

The quantifier's reach is correct in every shape I could construct. What is
*not* correct is its tense stamping (A-01), and the decision procedure it
claims (A-05): "an updater decides the question from the layer record alone".
The layer record (§7.4's table, lines 1075–1090) carries name, layout,
linearization, codec, filter, alignment, slab, slab alignment, rank, channel
count, dimension entries, channel entries, index_encoding, entry_count,
crc_of_crc_array, sub-records — and an extent slot addressing the tile-index
region. **Whether a tile is stored is nowhere in it.** §3.1: "A tile is stored
in a generation if and only if that generation's tile-index entry for it is not
the sentinel (§15)"; §15.2 defines the sentinel as 20 bytes in the *index
region*, not the record. §20.3's own opening even enumerates the three as
distinct: "every layer whose **record, index, or extents** the commit
modifies". `entry_count` decides it only in the degenerate case entry_count = 0.
So the test needs the index, which is neither the layer record nor "stored
bytes" — the sentence's two alternatives are not exhaustive of what must be
read. **Finding A-05.**

## 9. Derived disk-ordinal arithmetic — every claim, computed

From [R-GEO-06]: planar disk ordinal = **c · N + s**, c = channel index
(0-based, §3.1), s = spatial tile ordinal ∈ [0, N); interleaved = **s**.
From [R-GEO-03]: N = ∏ Gᵢ (spatial-tile count); addressed-tile count = C·N
planar, N interleaved. Cross-check from register row L2: "C·N (which dominates
the max disk ordinal **(C−1)·N + (N−1)**)" = C·N − 1 ✔ consistent with c·N+s.

Claim at 3187–3189: "a disk ordinal is c · N + s, and N is the spatial-tile
count, so the channel count enters the addressed-tile count C · N (§11.2) but
no individual ordinal." — **Computed and CORRECT.** C appears nowhere in
c·N+s.

Claim at 3196–3197: "An interleaved layer is unaffected, its disk ordinal being
s, which no channel declaration enters." — **CORRECT** per [R-GEO-06].

Claim at 3186–3187: "Appending a channel, or removing the last, re-indexes
nothing and moves no ordinal at all." — Appending at index C: existing
c ∈ [0, C) unchanged, N unchanged ⇒ every existing ordinal fixed; new ordinals
are C·N … (C+1)·N − 1, appended past the end. Removing index C−1: c ∈ [0, C−1)
unchanged, N unchanged. **CORRECT both ways.**

Worked example at 3192–3195, position by position, N = 2, channels (a, b):
  a: c=0 → 0·2+0 = 0, 0·2+1 = 1.  Document says "0 and 1" ✔
  b: c=1 → 1·2+0 = 2, 1·2+1 = 3.  Document says "2 and 3" ✔
  append c: c=2 → 2·2+0 = 4, 2·2+1 = 5; a and b untouched.
     Document says "leaves those four where they are and adds 4 and 5" ✔
  exchange a and b: a c=0→1 ⇒ 0,1 → 2,3; b c=1→0 ⇒ 2,3 → 0,1. All four tiles
     change ordinal. Document says "moves all four" ✔
**The worked example is arithmetically correct at every position.**

Claim at 3181–3182: "A channel's tiles move exactly when its index does."
Forward: c changes, N ≥ 1 ⇒ c·N changes ⇒ every one of its N ordinals moves ✔
(N = 0 is vacuous — no tiles exist). Backward: within channel-declaration edits
N and s are fixed, so an ordinal moves only if c does ✔. **Biconditional holds.**

Claim at 3183–3184: "inserting or removing one moves every channel **after the
affected position**." **This one does not compute.** Worked both ways:

  Removal, old-list indexing. Channels (a,b,c,d) at 0,1,2,3; remove b at
  position 1. New: a=0, c=1, d=2. Moved = {c, d} = old indices {2,3} = those
  strictly after position 1. **Correct under old-list indexing.**
  Removal, new-list indexing: channels after new position 1 = {d} only, but c
  moved too. **Wrong under new-list indexing.**

  Insertion, old-list indexing. Channels (a,b,c) at 0,1,2; insert x at
  position 1. New: a=0, x=1, b=2, c=3. Moved = {b, c} = old indices {1, 2} =
  those **at or after** position 1. The phrase "after the affected position"
  excludes b — which moved. **Wrong under old-list indexing.**
  Insertion, new-list indexing: channels after new position 1 = {b(2), c(3)} ✔.
  **Correct under new-list indexing.**

There is no single referent for "position" under which the clause is correct
for both operations. Under the natural old-list reading (the list you are
editing), the clause understates the moved set for an insertion by exactly one
channel — the one at the insertion point. And the worked example that follows
exercises only *append* and *exchange*: neither a middle insertion nor a middle
removal, so the example cannot correct the reader. **Finding A-02.**

(A charitable reader can rescue it by reading "position" as a *gap* for an
insertion and as an *index* for a removal, in one clause. That the rescue
requires two senses of one word in one clause is itself the defect.)

## 10. Check 4 — contradictions in the passage, including untouched text

Read: all of numbered step 4 (3111–3256), the paragraphs either side, the
Example block at 3286–3339, and §11.1's Rationale. Looked for a carve-out the
new breadth collides with, a MUST the new MAY lets an actor violate, and a
sentence true only under the old wording.

- Carve-out at 3161–3165 ("this bars nothing") vs the MAY at 3199–3203 ("a
  commit does not earn this permission by emptying the layer as it re-declares
  it"): they collide **only under the post-commit reading of the bare
  "stores"** at 3163. Recorded as A-01.
- Carve-out at 3146–3151 (the identity-filter / already-fill-padding
  exception) vs the new breadth at 3153: no collision — a re-typing is not one
  of those two cases, and 3231–3235 says so explicitly for the shrink ("its
  carve-out included").
- "The bar beside the §14 bar does not reach a shrink either: it bars a change
  to a planar layer's channel declarations that moves a stored tile's disk
  ordinal, and a shrink is not one" (3236–3239, untouched by my hunks):
  **consistent** with 3178–3181. A shrink is a geometry change, and a geometry
  change *does* move planar ordinals (N falls), but the ordinal bar is
  restricted to *channel-declaration* changes, so it does not bite; the
  re-emission rule's "(a geometry change renumbers ordinals wherever
  [R-GEO-06] moves them)" (3127–3128) licenses the renumbering. No collision.
- 3177–3178 "the re-emission rule above, whose only stated occasion for a
  renumbering is a geometry change": verified against 3126–3128 — the
  parenthetical there names a geometry change and nothing else. **Accurate.**
  I then asked whether anything *other* than geometry or channel index can
  move a planar ordinal, i.e. whether the new bar leaves a hole. Only the
  **layout** field remains (interleaved s ↔ planar c·N+s), and layout is
  neither geometry nor a channel declaration. Computed: a layout switch moves
  an ordinal only when C ≥ 2 (at C = 1, c·N+s = 0·N+s = s, no move); and at
  C ≥ 2 the decoded size necessarily changes (planar P·Bᶜ vs interleaved P·Q
  with Q = ΣBᵢ > Bᶜ), so the §14 bar already bars it wherever a tile is
  stored. **No hole.** Closed.
- "the same bytes denote different values" (3156–3157) vs §12.3 [R-TYP-04]:
  a genuine defined-term collision. **Finding A-03.**

## 11. Check 8 — what the insertion did to the sentences around it

**hunk-02.** Back-references forward of 3140, and their resolution before and
after:
 - 3142 "a commit does not escape **this**" — before: the MUST NOT sentence;
   after: "the §14 bar", same referent. Unchanged.
 - 3144 "and **this** bars it" — same. Unchanged.
 - 3145 "The test is the effect on **such a tile**" — "a tile that layer stores
   in the generation this commit supersedes". Unchanged.
 - 3145 "**the list**" — the four-item enumeration. Unchanged.
 - 3151 "is not what **this** bars" — the §14 bar. Unchanged.
 - Backwards: "Call **this** the §14 bar" — nearest noun phrase is "the codec
   and filter that produced the stored bytes"; intended referent is the whole
   MUST NOT. Disambiguated by every later use of the name (3175, 3214, 3231,
   3236, 3240, and §11.1/§21.7). Not a defect.
 **hunk-02 is anaphorically clean, and improves three later references.**

**hunk-03.** The insertion splits a sentence pair that was adjacent in the
prior text. The prior text read (from the hunk's `-` lines):

    …is not what this bars. Where a
    change does reach them it makes each stored tile it reaches
    nonconforming…

 - "**them**" resolved, before the insertion, to the tiles of 3147 —
   "every one of **those tiles'** stored bytes", i.e. the tiles the layer
   stores in the superseded generation. One sentence away.
 - After the insertion, "Where a change does reach them" (3165–3166) sits at
   the *end* of the new sample-type paragraph, 14 lines and one paragraph
   break from its antecedent, and the nearest preceding plural is
   "a planar channel none of whose **own tiles** are stored" (3164–3165) —
   tiles the immediately preceding clause has just declared **not** stored and
   the change **not** barred for. Substituting that candidate yields "Where a
   change does reach [tiles that are not stored] it makes each stored tile it
   reaches nonconforming", which is incoherent; the reader must jump back over
   the whole inserted paragraph. **Finding A-06, limb 1.**
 - Same sentence, second effect: the clause it heads ("…strand the originals
   as slack — the whole layer's worth … Such a change is a new layer, or a
   whole-file rewrite under a fresh file_id") was the general consequence of
   the §14 bar, covering every change the bar reaches — codec, filter, padding
   content, decoded size, sample offsets. It is now embedded as the tail of
   the sample-type paragraph and reads as the consequence of a *re-typing*.
   The ordinal paragraph then points back at it — "exactly as above"
   (3198–3199) — anchoring the general remedy to the sample-type paragraph.
   Neither sentence changed a word; no diff shows it. **Finding A-06, limb 2.**
 - Other back-references forward of the insertion, checked and **unaffected**:
   3197 "Where **this** bars a change" → the ordinal bar, same paragraph ✔;
   3202 "**this permission**" → the MAY in its own sentence ✔;
   3214 "the §14 bar" → named, not anaphoric ✔;
   3216 "**that bar's** own tense" → named ✔;
   3224 "**such an alteration**" → "alters nothing §14 fixes", same paragraph ✔;
   3226 "neither does **it** rescue" → dropping a tile out of the addressed
     set, same sentence ✔;
   3236 "**The bar beside the §14 bar**" → now resolves to the newly inserted
     ordinal bar, which is exactly what it should resolve to ✔ (this one
     *needed* the insertion to resolve at all);
   3240 "**this** is precisely where the §14 bar has no witness" → the shrink
     case ✔.
 - Backwards, inside the inserted text: 3174–3176 "One effect is barred beside
   **it** … the §14 bar does not reach **it**" — the same pronoun carries two
   different referents inside one sentence (first the §14 bar, then the
   ordinal move). Recorded below as a rejected candidate: it is loose prose,
   but both readings converge on the same rule and the sentence names the
   §14 bar explicitly two words later.

## 12. Check 5 — every completeness word, and the attempt to falsify it

| Word / claim | Location | Falsification attempt | Result |
|---|---|---|---|
| "wherever … stores a tile that carries that channel" | 3154 | tested against 7 layer shapes, §8 above | holds (tense aside) |
| "whether or not any tile stores that byte" | 3159 | the test is on declared types; no counterexample | holds |
| "**alone**" (from the layer record alone) | 3160 | §7.4 table + §15.2 sentinel + §3.1 | **FALSIFIED — A-05** |
| "none of whose own tiles are stored" | 3164 | planar ⇒ one channel per tile (§14.1) | holds |
| "each stored tile it reaches" | 3166 | — | holds |
| "the whole layer's worth" | 3168 | [R-LIF-01] freezes the committed prefix; index region is one extent | holds |
| "**exactly** when its index does" | 3181–3182 | computed both directions, §9 above | holds |
| "**every** channel after the affected position" | 3183–3184 | computed for insertion and removal, §9 above | **FALSIFIED under one reading — A-02** |
| "moves **no** ordinal **at all**" | 3186–3187 | computed for append and last-removal | holds |
| "**no** individual ordinal" (channel count) | 3189 | c·N+s contains no C | holds |
| "**no** channel declaration enters" (interleaved s) | 3196–3197 | [R-GEO-06]: interleaved ordinal is s | holds |
| "the list is **not** offered as exhaustive" | 3210 | explicitly disclaims — no overclaim | holds |

## 13. Check 6 — what the repair left unconstrained

**Structure governed:** a layer record's channel-declaration list (§7.4:
`channel count C` plus C channel entries of *name*, *type*, *fill*), together
with the layer-level declarations that interact with it (`layout`,
`linearization`, geometry, `codec`, `filter`, `alignment`, `slab`,
`entry_count`).

Every edit that structure admits, and what governs it after the repair:

| Edit | Governed by | Verdict |
|---|---|---|
| change a channel's **type** | new sample-type paragraph, via the §14 bar | constrained (A-01, A-03, A-04, A-05 attach) |
| change a channel's **fill** | §14 bar's enumeration, via §14.5's padding content | constrained; free where the layer has no padding position and no pad bit (Example (c), 3319–3321) |
| change a channel's **name** | nothing | genuinely free — a name enters no ordinal, no §14 arithmetic, no register row. Correct. |
| **reorder** channels | ordinal bar (planar); §14 bar via Fᶜ/byte offsets (interleaved) | constrained |
| **insert** a channel | ordinal bar (planar); §14 bar via Q and decoded size (interleaved) | constrained, with A-02's off-by-one |
| **remove** a channel | ordinal bar (planar); §14 bar (interleaved) | constrained |
| change **layout** | §14 bar via decoded size, whenever C ≥ 2; no ordinal move at C = 1 | constrained — computed in §10 above, no hole |
| change **linearization** | [R-GEO-05]: only value 1 may ever be emitted | cannot change |
| change **geometry** | growth / shrink paragraphs, §14 bar | constrained |
| change **codec / filter** | §14 bar's enumeration, last item | constrained |
| `entry_count` after a channel add/remove (planar) | [R-CNT-17] / row L21, generally | constrained (see rejected candidate 2) |
| slack from a removed channel's stored tiles | [R-CNT-21] / §21.6's slack row, generally | constrained (see rejected candidate 2) |

The one member of the *repair's own* structure left un-swept is the §14 bar's
four-item enumeration, which now fails to name where the sample-type effect
arises. **A-04.**

## 14. Rejected candidates — what I opened and what closed each

1. **"The gloss widens the §14 bar; a same-width re-typing alters nothing the
   bar names, so the entailment fails and the emittable set forks."** Opened as
   the lane's likely byte-level finding; I computed all four enumerated
   quantities for every same-element-size type pair (§7 above) and they are all
   invariant. **Closed** by the bar's own test sentence at 3146–3148: "a change
   that leaves every one of those tiles' stored bytes **meaning exactly what
   they meant** … is not what this bars" — a re-typing does not leave them
   meaning what they meant, so the bar reaches it on its stated test. What
   survives is only the un-swept enumeration (A-04).
2. **"A planar channel removal that de-addresses stored tiles has no stated
   disposition: slack, entry_count and index re-emission are stated only for an
   *extent* shrink (3243–3245), whose carve-out is keyed to '§11.2's grid count
   falls' (3222–3223) — and removing a channel lowers C, not a grid count."**
   **Closed:** [R-CNT-17] ("entry_count equals the addressed-tile count") and
   row L21 ("entry_count does not equal the geometry-derived addressed-tile
   count (N interleaved, C·N planar)") bind generally, not only under a shrink;
   [R-CNT-21] and §21.6's slack row cover the orphaned extents generally. The
   passage is silent, but nothing is unconstrained.
3. **"The re-typing carve-out says re-typing an unstored planar channel 'is a
   declaration edit like any other' with no proviso, while the growth
   permission two paragraphs down is fenced with 'provided the grown geometry
   stays within every bound the layer's own declarations impose, [R-COD-07]'s
   lz4 decoded-size cap among them (L44)'. A `uint8`→`uint64` re-type of an
   unstored plane under codec 4 can cross 0x7E000000."** Real asymmetry.
   **Closed as non-byte-level and non-reportable:** the disputed file carries an
   L44 violation, so [R-CNF-05] bars every conforming writer from emitting it
   under both readings; and "like any other" imports exactly the obligations
   any declaration edit carries. The growth proviso is belt-and-braces.
4. **"The ordinal bar overshoots: barring a channel reorder on a planar layer
   with stored tiles forbids something that would produce a perfectly valid
   file (the entries simply renumber)."** **Closed:** the stated ground at
   3176–3178 is that the re-emission rule's only stated occasion for a
   renumbering is a geometry change; permitting channel-driven renumbering
   would leave that rule without a licence. Conservative but coherent, and a
   maintainer's design call, not a defect.
5. **"'An interleaved layer is unaffected' (3196) could be read as licensing
   free channel edits on interleaved layers, which would be flatly wrong —
   Q = ΣBᵢ changes."** **Closed:** the clause supplies its own reason ("its
   disk ordinal being s, which no channel declaration enters"), which scopes it
   unambiguously to the ordinal bar, and the §14 bar catches the interleaved
   cases independently.
6. **"'One effect is barred beside it … the §14 bar does not reach it' uses one
   pronoun for two referents in one sentence."** **Closed as prose looseness,
   not a rule defect:** the §14 bar is named explicitly two words after the
   first "it", both readings converge on the same rule, and no obligation turns
   on the resolution.
7. **"§11.1's Rationale restates the re-typing rule with the same bare tense —
   an unswept restatement."** **Closed:** the block opens `> **Rationale.**`,
   so [R-CNF-01] makes it non-normative; it cannot carry or corrupt force. Its
   content otherwise matches the repair exactly, so the sweep succeeded.
8. **"The '§14 bar' name introduced by hunk-02 might be used somewhere before
   it is defined."** **Closed by grep:** 11 hits; the definition is at 3140 and
   the earliest *use* is 1606, inside §11.1's non-normative Rationale, which
   pins it ("Of its two bars the one reaching a shrink or a growth is the §14
   bar"). Forward reference in non-normative text to a name defined in §20.3 is
   the document's habit elsewhere; not worth a finding.

## 15. Findings

A-01  TENSE_QUANTIFIER — bare "stores" at four sites in the insertion (3154,
      3163, 3164, 3190) where all four occurrences of the stamped quantifier
      elsewhere in step 4 carry "in the generation this commit supersedes"
      (two in bold), and where §3.1 supplies a contested default. Byte-level.
A-02  NEW_AMBIGUITY — "moves every channel after the affected position"
      (3183–3184) is correct for a removal only under old-list indexing and
      for an insertion only under new-list/gap indexing; under the natural
      old-list reading it excludes the channel at the insertion point, which
      moves. The worked example exercises neither case. Byte-level.
A-06  NEW_AMBIGUITY — the insertion re-resolved "them" (3165) away from "those
      tiles" (3147) and re-homed the §14 bar's general consequence clause into
      the sample-type paragraph, which the ordinal bar then points back at
      ("exactly as above", 3198). Not byte-level.
A-05  OVERCLAIM — "an updater decides the question from the layer record alone
      rather than by inspecting stored bytes" (3160–3161): the storage half of
      the test lives in the tile index (§15.2 sentinel), which is neither.
      Not byte-level.
A-03  LOCAL_CONTRADICTION — "the same bytes denote different values"
      (3156–3157) against [R-TYP-04] §12.3, which stipulates that same bytes
      *are* the same value. Not byte-level.
A-04  UNDERSHOT — the §14 bar's enumeration, which the bar says "names where
      that effect arises", was not extended to name where a same-element-size
      re-typing's effect arises. Not byte-level.

## 16. Per-check verdict

1. Tense/quantifier — **FAILED** (A-01).
2. Citations resolve — **PASSED**, 10 of 10 opened and verified (§3).
3. Normative placement, by label — **PASSED** (§4).
4. No contradiction in the passage — **FAILED** (A-03); the four other
   collisions I looked for are recorded closed in §10 and §14.
5. No exhaustive claim it cannot carry — **FAILED** (A-02, A-05); 12 claims
   tested, 10 hold (§12).
6. What is still unconstrained — **FAILED** (A-04); the 12-row edit inventory
   is otherwise complete (§13).
7. Analogy quantifiers word for word — **PASSED**, all four compared (§6).
8. What the insertion did to its neighbours — **FAILED** (A-06); 12
   back-references resolved, 10 unaffected (§11).
