# Audit transcript — hunk-03 and hunk-04 of case-adr0113
# Auditor lane: "the two bars"

## 0. Disclosure

Files read:
- /private/tmp/.../case-adr0113/hunk-03.diff  (my charter)
- /private/tmp/.../case-adr0113/hunk-04.diff  (my charter)
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md  (the spec; read in
  passages, listed below)

I did NOT read full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, git history, or the web. I did
not list the case directory. Everything I ran was grep/sed/tr/wc against spec/tarn.md.

Unrequested context that appeared before I began: a project-instruction preamble
(CLAUDE.md pointing at AGENTS.md), a user auto-memory index naming two prior-round
notes, an MCP server-instructions block, and a git-status/recent-commit snapshot whose
commit subjects name a prior round's disposition. I read none of the files they point
at and I have drawn no conclusion from any of it; naming it here per the charter.
The only effect it had on my behaviour: I used Bash (`sed`, `grep`, `tr`) instead of
the Read tool, per the MCP block.

Spec passages read in full:
- §2.1 lines 94-106 ([R-CNF-01])
- §3.1 / §3.2 lines 339-425
- §11.1 lines 1596-1626 (the Rationale block), §11.2 lines 1627-1653,
  §11.3 lines 1655-1672, §11.4 lines 1674-1716 ([R-GEO-05], [R-GEO-06] + Example/Note)
- §12 lines 1717-1800 ([R-TYP-01] type table, [R-TYP-02], [R-TYP-03])
- §14 lines 1919-2100 (§14.1-§14.5, [R-SER-01] [R-SER-06] [R-SER-02] [R-SER-08]
  [R-SER-03] [R-SER-07] [R-SER-09] [R-SER-05] and their Notes/Examples)
- §20.3 lines 3070-3340 — the whole subsection including all of step 4 and the three
  trailing blockquotes
- §20.4 opening lines 3340-3345
- §21.7 lines 3861-3946
- §23.1 lines 3145-3185 (partial, for the restatement sweep)
- register rows L2 (3687), L44 (3729), T4 (3749), T23 (3768), and line 3978

## 1. The two hunks, and the rule each adopts

### hunk 3 (lands at spec/tarn.md 3137-3138)

Diff body: replaces
    `produced the stored bytes. The tense is the prior generation's`
with
    `produced the stored bytes. Call this the **§14 bar**, the name the`
    `rest of this step and §21.7 use for it. The tense is the prior generation's`

Header claim "nearest preceding heading ... line 3070, '20.3 The append procedure'":
verified. `sed -n '3070p'` gives `#### 20.3 The append procedure`, and there is no
heading between 3070 and 3137 (`grep -n '^#' | awk` over the range returns nothing).
No mismatch to report.

**Rule the repair adopts:** none, normatively. It is a naming/definition move: it binds
the label "§14 bar" to the MUST NOT that begins at line 3128 (`A commit MUST NOT change
a layer's declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how they
decode`). What it makes true of an implementation: nothing new; it makes true of a
*reader of the document* that the term "§14 bar" appearing later resolves to that
requirement. It also makes a factual claim about where the name is used.

### hunk 4 (lands at spec/tarn.md 3155-3206)

Inserts three new paragraphs between the §14-bar paragraph and the pre-existing
"A layer that stores no tile ... MAY be re-declared freely" permission, and changes
`the tense is the bar's` to `the tense is these bars'`.

**Rules the repair adopts:**

(a) *Sample-type bar* (3170-3172): an appender's commit is nonconforming if it changes
the `sample type` field of ANY channel entry of ANY layer for which at least one tile
was stored in the generation the commit supersedes — irrespective of layout, of whether
the element size changes, and of whether that particular channel had any stored tile.

(b) *Ordinal bar* (3182-3186): for a layer whose layout is planar, an appender's commit
is nonconforming if the new channel declarations give some tile that was stored in the
superseded generation a different `c · N + s` than the old ones did. Operationally:
reorder, insert, or remove-not-last is barred if any channel at or after the moved
position had a stored tile; append and remove-last are free.

(c) A carve-out (3193-3196): moving the ordinals of channels that stored nothing in the
superseded generation is not such a change.

(d) A sweep: the pre-existing empty-layer permission's tense anaphor becomes plural.

## 2. Check 3 — normative placement (LABEL, not marker)

Both hunks land inside the numbered list item "4. **Write payloads and indexes**" of
§20.3. These are 3-space-indented list-continuation paragraphs. They carry NO `>`
marker and NO **Note.** / **Example.** / **Rationale.** label. Test applied: I read the
opening words of the enclosing block, not the marker. Per [R-CNF-01] (line 104-106,
verbatim: "All text in this document is normative except: §1 (Introduction); any text
labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative.") both hunks are in normative text. The MUST NOTs land. PASS.

I then checked the converse — whether a statement the repair relies on lives only in a
labeled block. It does, once. See finding A-05.

Blockquote labels I checked in and around §20.3:
- 3268 `> **Note.** A commit's cost is dominated by its index` → labeled Note, inert.
- 3277 `> **Example.** Superseding one 100,000-byte stored tile` → labeled Example.
- 3291 `> **Example — the three shapes a commit takes.**` → labeled Example; this is the
  block containing shape (c) at 3317-3328. Non-normative.
- 1601 `> **Rationale.** Empty layers serve schema-first workflows` → labeled Rationale.
  This is the block that carries "The other two bars reach neither a shrink nor a
  growth". Non-normative. This matters — A-05.

## 3. The ordinal arithmetic, derived from first principles

Governing rule, [R-GEO-06] (lines 1712-1716, verbatim):
"The **disk tile ordinal**, which orders tile-index entries (§15), is s for an
interleaved layer, and **c · N + s** for a planar layer (§14), where c is the channel's
index (§3.1) — channel-major grouping."

Supporting: [R-GEO-03] (§11.2, 1629-1637): N = ∏ Gᵢ, Gᵢ = ⌈Eᵢ/Tᵢ⌉; addressed-tile count
is N interleaved, C·N planar. [R-GEO-05] (§11.4, 1706-1711): s = Σ tᵢ · ∏_{j>i} Gⱼ.
§3.1 (line 358-360): "a channel's **index** is its 0-based position in that order".

N depends only on extents and tile extents. C does not enter any individual ordinal.
Therefore, holding geometry fixed, the ordinal of tile (c, s) moves iff c moves.

Position-by-position check of the passage's claims:

| claim (line) | my derivation | verdict |
|---|---|---|
| "reordering moves those channels the reorder re-indexes" (3186-3187) | c changes ⇒ c·N+s changes for every s (N ≥ 1) | correct |
| "inserting or removing one moves every channel after the affected position" (3187-3188) | insert at p ⇒ c→c+1 for c ≥ p; remove at p ⇒ c→c−1 for c > p | correct |
| "Appending a channel ... re-indexes nothing and moves no ordinal at all" (3190-3191) | new channel takes index C; every c < C unchanged; N unchanged | correct |
| "removing the last ... moves no ordinal at all" (3190-3191) | remove index C−1; every c < C−1 unchanged; N unchanged | correct |
| "a disk ordinal is c · N + s, and N is the spatial-tile count" (3191-3192) | matches [R-GEO-06] and [R-GEO-03] verbatim | correct |
| "the channel count enters the addressed-tile count C · N (§11.2) but no individual ordinal" (3192-3193) | §11.2 line 1633-1635 says addressed-tile count "is N for an interleaved layer and C · N for a planar layer"; C appears nowhere in c·N+s | correct |
| worked example: "A layer with N = 2 and channels (`a`, `b`) places `a` at ordinals 0 and 1 and `b` at 2 and 3" (3196-3198) | a: c=0 → 0·2+{0,1} = {0,1}. b: c=1 → 1·2+{0,1} = {2,3} | correct |
| "appending `c` leaves those four where they are and adds 4 and 5" (3198-3199) | c: index 2 → 2·2+{0,1} = {4,5}; a,b unchanged | correct |
| "while exchanging `a` and `b` moves all four" (3199) | a→index 1 → {2,3}; b→index 0 → {0,1}; all four differ from before | correct |
| "An interleaved layer is unaffected, its disk ordinal being s, which no channel declaration enters" (3200-3201) | [R-GEO-06] gives s; s = Σ tᵢ·∏_{j>i}Gⱼ involves only grid counts | correct |
| §12.1 counter-example: "a planar `uint8` channel re-declared `bool` keeps its element size of 1 while its plane goes from P · Bᶜ bytes to ⌈P/8⌉ (§14.3), and the two coincide at P = 1" (3166-3169) | §12.1 table: bool size 1, uint8 size 1. §14.2 table: planar numeric = P·Bᶜ = P. §14.3: planar bool = ⌈P/8⌉. P = ⌈P/8⌉ ⟺ P=1 (P=2→2 vs 1; P=8→8 vs 1). Independently corroborated by §14.4's Note "At P = 1 the two are the same length" | correct |
| §12.1 sizes behind "`int8` to `uint8`, or `float32` to `int32`, moves no stored byte, no decoded size and no sample offset" (3160-3163) | §12.1 table: int8=1, uint8=1, int32=4, float32=4. §14.2: planar P·Bᶜ, offsets k·Bᶜ; interleaved P·Q, offset (k div C)·Q + F_{k mod C}, with Q=ΣBᵢ and Fᶜ=Σ_{j<c}Bⱼ. All are functions of element sizes only ⇒ unchanged | correct |
| register row L2 (3687) "C·N (which dominates the max disk ordinal (C−1)·N + (N−1))" | (C−1)·N + (N−1) = C·N − 1 < C·N | correct (checked in passing, not part of my hunks) |

**Every arithmetic claim in hunk 4 reproduces.** I could not falsify one.

But the arithmetic has a consequence the passage does not draw: N is a function of the
extents. Raising or lowering an extent so that some Gᵢ changes changes N, and then
c·N+s changes for every c ≥ 1 without any channel index moving. See A-03 and A-05.

## 4. Check 1 — tense and quantifier

Whitespace-normalised sweep (the file is hard-wrapped, so I flattened it):

    tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "..........................the layer stores................................"

output (5 hits):
    y that alters, for a tile the layer stores, what §14 fixes for its bytes o
    GEO-06]` assigns any tile the layer stores in the generation this commit s
    is such a change wherever the layer stores a tile for a channel that moved
    ng §14 fixes for any tile the layer stores in the generation this commit s
    hing §14 fixes for a tile the layer stores in the generation the commit su

    tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "generation this commit supersedes" | wc -l   → 5
    tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "stores in the generation this commit supersedes" | wc -l → 2

Governing definition, §3.1 line 372-376 (verbatim):
"A tile is *stored in a generation* if and only if that generation's tile-index entry
for it is not the sentinel (§15); unqualified *stored* means stored in the live
generation."

So an unqualified "the layer stores" is the LIVE generation — the opposite tense from
the one the §14 bar is at pains to fix.

Of the five hits, three carry the qualifier and two do not. Both unqualified ones are
inside hunk 4's inserted text:

  (i) line 3158: "any that alters, for a tile the layer stores, what §14 fixes for its
      bytes or how they decode" — a restatement of the §14 bar's test.
  (ii) line 3188-3189: "Either is such a change wherever the layer stores a tile for a
      channel that moved." — the operative gloss on when the ordinal bar bites.

A third, weaker instance is line 3193-3194: "**The test is the effect on a stored tile,
not the shape of the edit**" — "a stored tile", unqualified — in the very same sentence
as a correctly qualified clause, "channels the superseded generation stored no tile
for". One sentence, two tenses.

Compare with the neighbour I am asked to check against, the §14 bar itself
(lines 3128-3133, verbatim):
"A commit MUST NOT change a layer's declarations in a way that alters, for any tile
that layer stores **in the generation this commit supersedes**, what §14 fixes for its
stored bytes or how they decode"
and its own insistence, lines 3138-3142:
"The tense is the prior generation's (§3.1 defines *stored* against a generation), so a
commit does not escape this by unstoring in the same breath: superseding every tile of
a layer and re-declaring it are one operation, and this bars it."

And with §21.7's parallel gloss, which gets it right (line 3897-3900):
"its two companion bars are witnessed not at all where the change leaves untouched
everything §14 fixes for a tile the layer stores in the generation the commit
supersedes".

Findings A-01 and A-02.

### The charter's "shared quantifier" question — do the three agree?

- §14 bar: ranges over TILES. "for any tile that layer stores in the generation this
  commit supersedes".
- Sample-type bar (3170-3173): ranges over LAYERS. "the declared sample type of any
  channel of a layer that stores a tile in the generation this commit supersedes".
- Ordinal bar (3183-3186): ranges over TILES. "alters the disk ordinal `[R-GEO-06]`
  assigns any tile the layer stores in the generation this commit supersedes", with an
  explicit per-channel carve-out at 3193-3196.
- The permission (3203-3205): ranges over LAYERS. "A layer that stores no tile **in the
  generation this commit supersedes** MAY be re-declared freely".

**They do not agree.** The tense agrees in three of four (the two hunk-4 slips above
aside); the *scope* does not. The sample-type bar is layer-scoped where both its
neighbours are tile-scoped, and it therefore bars a change to the type of a channel
that had no stored tile at all, on a planar layer, where the very next paragraph
deliberately carves that case out for ordinals. Finding A-04.

## 5. Check 2 — citations

Every identifier and section number in the two hunks, opened and read:

| citation | where | claim made | verdict |
|---|---|---|---|
| §21.7 (hunk 3, 3137-3138) | "the name the rest of this step and §21.7 use for it" | §21.7 uses the term | PASS on §21.7 — `grep -n "§14 bar"` puts hits at 3906 ("escapes them here exactly as it does the §14 bar") and 3930 ("so the §14 bar is unwitnessed there"). FAIL on completeness — see A-08 |
| "the rest of this step" (hunk 3) | same | step 4 uses the term | PASS. Hits at 3157, 3181, 3218, 3230, 3235, 3239 — all inside step 4 (step 4 runs 3111-3253) |
| §14 (3158, 3159) | "what §14 fixes for its bytes or how they decode" | §14 fixes decode | PASS as to §14's content ([R-SER-01] value sequence, [R-SER-02] size/offsets, [R-SER-03] packing, [R-SER-07] decoded-size check, [R-SER-05] padding content). FAILS on tense — A-01 |
| §12.1 (3166) | "the element sizes of §12.1 do not settle it" | §12.1 gives element sizes | PASS — table at 1731-1746 |
| §14.3 (3168) | planar bool plane is ⌈P/8⌉ | PASS — [R-SER-03], line 2019-2022: "the decoded size is ⌈P/8⌉ bytes" |
| §11.2 (3192) | "the channel count enters the addressed-tile count C · N (§11.2)" | PASS — [R-GEO-03], 1633-1635 |
| `[R-GEO-06]` (3184) | "the disk ordinal `[R-GEO-06]` assigns" | PASS — 1712-1716, quoted above |
| §14 bar "does not reach it because it is not an effect on any stored tile's bytes" (3181-3182) | that an ordinal move touches no stored tile's bytes | PASS, but only because §3.1 individuates a tile by (grid cell, channel), not by ordinal. §3.1 line 369-372: "**tile** — the unit a tile-index entry addresses: ... in a planar layer, one cell of the grid for one channel." §14.1's phrasing "the tile with disk ordinal c · N + s ... carries exactly the values of channel c" is parameterised by c and s, so the tile keeps its identity and its bytes when its ordinal moves. See rejected candidate R-2 |
| `[R-COD-07]` / L44 (3210-3213, context the repair's tense-edit sits beside, not inserted) | "that cap is quantified over addressed tiles" | PASS — L44 (line 3729): "Codec 4 (lz4) declared on a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000 bytes" |
| `[R-LIF-01]`, §20.5 (3153, context) | not inserted by my hunks | not audited beyond noting it is unchanged |

## 6. Check 4 — contradiction in the same passage, including untouched text

I read the whole of step 4 (3111-3253) and both adjacent steps.

Collisions found:

(a) **3193-3194 vs 3236-3238.** The insertion says, in bold, "**The test is the effect
on a stored tile, not the shape of the edit**". Forty lines later, in the same step,
the untouched-by-me shrink paragraph reasons by exactly the shape of the edit:
"Neither of the two bars beside the §14 bar reaches a shrink: one bars a change to a
channel's declared sample type and the other a change to the channel declarations, and
a shrink is neither." A shrink that lowers a grid count lowers N and therefore moves
c·N+s for every c ≥ 1 — it has precisely the barred *effect* and is excused on the
*shape*. Reconcilable if the bold is read as scoped to channel-declaration edits, but
the bold is not so scoped, and it is bolded. Finding A-03.

(b) **3186 vs the growth permission at 3206-3210.** "A channel's tiles move exactly
when its index does" is false: they also move when N moves, and N moves on a growth
that changes a grid count. §11.1's Rationale states this outright (1621-1623:
"Growth that changes entry_count changes extent_length with it (`[R-CNT-17]`), so the
layer's whole tile-index region is re-emitted and disk ordinals renumber wherever
`[R-GEO-06]` moves them"). Under the bold "effect not shape" test, such a growth
alters stored tiles' disk ordinals and would be barred; under the requirement's own
subject ("change **the channel declarations**") it is not, and 3206 says "an extent MAY
**grow**". Finding A-03, and its placement half is A-05.

(c) **3173 vs the rest of the document.** "Reinterpreting a stored array is not an
appender's operation." — an unlabeled, hence normative, absolute. The document
permits several reinterpretations of a stored array: the Example at 3317-3320 blesses
"changing a channel's fill value on a layer with no padding position and no pad bit",
and nothing anywhere bars renaming a channel (`grep -i renam` returns exactly one hit
in the whole spec, line 3318, and it is about renaming a *layer*). Finding A-06.

Collisions I looked for and did NOT find:
- No MUST elsewhere in step 4 that the new MUST NOTs let anyone violate.
- No "is not such a case" carve-out that the sample-type bar's new breadth collides
  with. The §14 bar's own carve-out (3143-3149, the identity-filter / already-fill
  cases) is about the §14 bar and the sample-type bar sits beside it, not inside it.
- Step 4's earlier parenthetical at 3123-3124, "(a geometry change renumbers ordinals
  wherever `[R-GEO-06]` moves them)", is not falsified by the carve-out at 3193-3196:
  the only channel-declaration ordinal moves the new bar permits are moves of tiles the
  superseded generation stored nothing for, whose index entries are sentinels
  ([R-IDX-02], §15) and therefore byte-identical wherever they land. I constructed
  three candidate counterexamples (remove a middle channel with a later stored channel
  → barred; remove a middle channel with only unstored channels after it → sentinels
  only; append → nothing moves) and none produced a non-sentinel entry moving under a
  non-geometry change. Closed.

## 7. Check 5 — exhaustive claims

Every completeness word in the two hunks, and my attempt to falsify each:

| word / claim | line | falsification attempt | verdict |
|---|---|---|---|
| "the name the rest of this step and §21.7 use for it" (a closed two-item list of use sites) | 3137-3138 | `grep -n "§14 bar"` → 1606, 3137, 3157, 3181, 3218, 3230, 3235, 3239, 3906, 3930. Line 1606 is in §11.1, neither "this step" nor §21.7 | **FALSIFIED** — A-08 |
| "It does not reach all of them." | 3159-3160 | not a completeness claim; it is a negative existential and the two examples given are correct | passes |
| "leaves **every** content rule §14 states over those bytes satisfied exactly as before" | 3161-3163 | §14's content rules are §14.5/[R-SER-05] (padding positions carry the channel's recorded fill bytes), §14.3/[R-SER-05] (pad bits carry the fill bit), and [R-SER-08] (interleaved bool bytes are 0x00/0x01). For int8→uint8 and float32→int32 the fill field's length is the element size ([R-CNT-23] via §12.1) and is equal on both sides, so the recorded fill bytes need not change and the required padding content does not move; neither type is bool, so the pad-bit and bool-byte rules are not engaged | passes |
| "whatever the layer's layout" | 3172-3173 | [R-SER-06] (1948-1954): "1 = interleaved and 2 = planar are the only values this specification defines and the only values a writer MAY emit; values 3 through 255 are reserved without semantics. A reader MUST treat any value other than 1 or 2 as a validity error at layer scope". So the quantifier ranges over exactly two live cases and the claim is safe | passes |
| "whether or not the element size moves" | 3173 | exhaustive over a boolean | passes |
| "A channel's tiles move **exactly when** its index does" | 3186 | falsified by an extent change: N moves, index does not, tiles move | **FALSIFIED** — A-03 |
| "moves no ordinal **at all**" (append / remove-last) | 3190-3191 | derived above; correct | passes |
| "**The test is the effect on a stored tile, not the shape of the edit**" | 3193-3194 | falsified by 3236-3238, which decides a shrink on the shape | **FALSIFIED** — A-03 |
| "An interleaved layer is unaffected" | 3200 | true of this bar; the reason clause ("its disk ordinal being s, which no channel declaration enters") scopes it. Considered and rejected — see R-1 |
| "exactly as above" | 3202 | resolves to a new layer / whole-file rewrite either way | passes |
| "the two coincide at P = 1" | 3169 | derived above; correct, and P=1 is the unique solution | passes |

## 8. Check 6 — what the repair left unconstrained

**The structure the repair governs: the channel entry of a layer record (§7.4, §12).**
§12 line 1719-1721, verbatim: "A channel is declared by its layer record's channel
entry (§7.4): a **name** (§4.6), a **sample type** (`u16`, structural), and a **fill
value** (§13)." Plus two properties of the entry *sequence*: its length (C) and the
order of its members.

Member-by-member, for a layer that stored a tile in the superseded generation:

| member | what pins it | verdict |
|---|---|---|
| sample type | the new bar at 3170-3173, absolutely | pinned |
| position in the order | the new ordinal bar (planar) at 3182-3186; the §14 bar (interleaved, via decoded size / value-sequence attribution under [R-SER-01] and [R-SER-02]'s Q and Fᶜ) | pinned |
| count C (insert / remove) | same two, with the append and remove-last cases deliberately left free planar | pinned, but see the de-addressing gap below |
| **fill value** | the §14 bar, but only where §14 gives it a witness: [R-SER-05] padding-position content and pad bits. Where the layer's stored tiles have no padding position and no pad bit, nothing pins it, and the Example at 3317-3320 says so explicitly | **partly unpinned, deliberately** |
| **name** | **nothing.** `grep -i renam` over the whole spec returns one hit, 3318, about renaming a *layer*. `grep -n "channel name"` returns 568, 574 (uniqueness within a layer), 2774, 4020, 4192 — none of which is a change rule | **UNPINNED** |

So: the repair pinned one field of the three-field structure absolutely, one field
partially, and left the third unconstrained. A commit may, on a planar layer whose
stored tiles have no padding position and no pad bit, rename channel `a` to `b` and
rewrite its fill, keeping every stored byte — which is the reinterpretation of a stored
array that line 3173 declares "not an appender's operation". This is the same
"pinned one quantity, left the sibling free" shape the charter warns about. Finding
A-06.

A second gap in the same structure, on the count: the passage says "removing the last,
re-indexes nothing and moves no ordinal at all", which answers the *ordinal* question
and is silent on the *de-addressing* question — the removed channel's stored tiles
leave the addressed set entirely. The sentence that licenses that for the parallel case
is at 3222-3225 and is parenthetically tied to extents: "Dropping a tile out of the
addressed set (§11.2's grid count falls) is not itself such an alteration". A channel
removal drops tiles because C falls, not because a grid count falls. I considered
raising this and did not — see rejected candidate R-4.

## 9. Check 7 — arguments by analogy, verb against verb

Every self-justifying pointer in the two hunks:

(1) **3180-3182: "A further effect is barred on the same tense and for the same reason,
and the §14 bar does not reach it".**

- Repair's governing verb: "a commit MUST NOT **change** the channel declarations in a
  way that **alters the disk ordinal** `[R-GEO-06]` **assigns** any tile the layer
  stores".
- §14 bar's governing verb: "A commit MUST NOT **change** a layer's declarations in a
  way that **alters** ... what §14 **fixes** for its **stored bytes** or how they
  **decode**".
- Sample-type bar's stated reason (the nearer antecedent): "**Reinterpreting** a stored
  array is not an appender's operation."
- §14 bar's stated reason (the further antecedent): "Where a change does reach them it
  **makes** each stored tile it reaches **nonconforming**, and **re-emitting** those
  tiles would **strand** the originals as slack".

Same set? The **tense** transfers cleanly: both are "in the generation this commit
supersedes", and I verified both strings above. The **reason** does not transfer under
either antecedent. An ordinal move makes no stored tile nonconforming — the repair's
own next clause concedes this ("it is not an effect on any stored tile's bytes") —
requires no payload re-emission, and strands nothing; and it reinterprets no array,
since the payload keeps its channel and only its index-entry position moves. Step 4
four paragraphs above treats ordinal renumbering as a routine, permitted event
("a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them"). So the
sentence carries an anaphor, "the same reason", that has two candidate antecedents and
is false under both. Finding A-07.

There is a reason available that the text does not give: step 4's re-emission rule
("every other entry byte-identical at its **disk-ordinal position**") licenses
renumbering only in a parenthetical about *geometry* changes, so barring the
channel-declaration cause keeps that parenthetical exhaustive. That is not what
"for the same reason" points at.

(2) **3202: "the operation is a new layer or a whole-file rewrite, exactly as above."**
- Repair's verb: "**is** a new layer or a whole-file rewrite".
- Cited: 3151-3153, "Such a change **is** a new layer, or a whole-file rewrite under a
  fresh file_id".
Same verb, same set (a barred change ⇒ that operation). PASS. Reported per the charter
even though it passes.

(3) **3157-3159: "The §14 bar already reaches many changes ... : any that alters, for a
tile the layer stores, what §14 fixes for its bytes or how they decode."**
- Repair's verb: "the layer **stores**" (unqualified ⇒ live generation, §3.1).
- Cited rule's verb: "that layer **stores in the generation this commit supersedes**".
Different sets. Finding A-01.

(4) **3188-3189: "Either is such a change wherever the layer stores a tile for a
channel that moved."**
- Repair's verb here: "the layer **stores** a tile" (unqualified ⇒ live).
- Its own requirement three lines above: "any tile the layer **stores in the generation
  this commit supersedes**".
The gloss and the rule it glosses range over different generations. Finding A-02.

## 10. Check 8 — what the insertion did to the sentences around it

hunk 3 first. It inserts one sentence between "produced the stored bytes." and "The
tense is the prior generation's". Back-references immediately after:
- "**The tense**" (3138) — before: the tense of the MUST NOT just stated. After: the
  nearest antecedent is "the **§14 bar**", which IS that MUST NOT. Unchanged. PASS.
- "escape **this**" (3139) — same antecedent both ways. PASS.
- "**this** bars it" (3142) — same. PASS.

hunk 4. Reading forward from 3155 to the end of step 4 (3253), every back-reference:

| back-reference | line | resolved BEFORE the insertion | resolves NOW | changed? |
|---|---|---|---|---|
| "It does not reach all of them" — "them" | 3159-3160 | n/a (new text) | "changes to a channel's declared sample type" | n/a |
| "the same reason" | 3180 | n/a (new text) | ambiguous between the sample-type bar's reason and the §14 bar's; false under both | see A-07 |
| "does not reach **it**" | 3181-3182 | n/a | "a further effect", i.e. the ordinal move | fine |
| "Either **is such a change**" | 3188 | n/a | the ordinal-altering change just defined | fine, but mis-tensed (A-02) |
| "alters nothing **this** bars" | 3196 | n/a | the ordinal bar | fine |
| "Where **this** bars a change" | 3201-3202 | n/a | the ordinal bar | fine |
| "exactly **as above**" | 3202 | n/a | §14 bar's closing at 3151-3153; now the nearer candidate is the sample-type paragraph's closing at 3178-3179 — same content | changed antecedent, same meaning; no defect |
| "the tense is **these bars'**" | 3206 | "the bar's" → the §14 bar | all three bars | **swept deliberately by the repair.** Correct: all three carry the superseded tense in their headline statements. PASS |
| "**that channel's** fill" | 3208 | had NO local antecedent — the §14-bar paragraph (3128-3153) contains no occurrence of "channel", so the reader had to take it generically, as §14.5 does ("for each channel the position carries, that channel's fill value") | nearest preceding "channel" nouns are now the worked example's `a`, `b`, `c` at 3196-3199 and "no channel declaration" at 3201 | **CHANGED** — A-09 |
| "**that** cap" | 3213 | `[R-COD-07]`'s lz4 decoded-size cap, same sentence chain | unchanged | PASS |
| "**the §14 bar** is the whole of the test" | 3218-3219 | the §14 bar | unchanged (the name is now explicit, which is an improvement) | PASS |
| "**in that bar's** own tense" | 3219 | the §14 bar | unchanged | PASS |
| "not itself **such an alteration**" | 3223 | an alteration of what §14 fixes | unchanged | PASS |
| "**it** rescue a commit" / "does not rescue **it**" | 3224, 3226 | the commit / the shrink | unchanged | PASS |
| "its carve-out included" | 3231 | the §14 bar's | unchanged | PASS |
| "**Neither of the two bars beside** the §14 bar" | 3235-3236 | n/a — this sentence names the two new bars, so it postdates the change | resolves correctly | PASS (not my hunk) |
| "§21.7 records **the consequence**" | 3238-3239 | verified against §21.7, 3895-3901, which does record it | PASS |

Backwards run — does the inserted text itself lean on a distant antecedent? Yes, once:
"the same tense and for the same reason" (3180) reaches back over an intervening
paragraph. The tense is recoverable; the reason is not, and is wrong. A-07.

## 11. Sweep for unswept restatements

Searches run (all against spec/tarn.md; hard-wrap handled by keeping fragments short or
by flattening with tr):

    grep -n "R-GEO-06"                                → 6 hits (1623, 1700, 2968, 3124, 3184, 3885)
    grep -n "§14 bar"                                 → 10 hits (1606, 3137, 3157, 3181, 3218, 3230, 3235, 3239, 3906, 3930)
    grep -n -i "re-declar"                            → 7 hits (1613, 3141, 3167, 3204, 3207, 3324, 3907)
    grep -n -i "redeclar"                             → 0
    grep -n -i "sample type"                          → 12 hits
    grep -n -i "declared sample"                      → 3 hits (1615, 3171, 3236)
    grep -n -i "channel declaration"                  → 6 hits (1616, 1721, 3183, 3201, 3237, 3900)
    grep -n -i "disk ordinal"                         → 14 hits
    grep -n -i "declarations in a way"                → 2 hits (3131, 3183)
    grep -n -i "MUST NOT change"                      → 3 hits (3130, 3170, 3183)
    grep -n -i "20.3 step 4"                          → 3 hits (3895, 4158, 4171)
    grep -n -i "three bars"                           → 1 hit (1606)
    grep -n -i "two bars"                             → 2 hits (1614, 3235)
    grep -n -i "companion bar"                        → 1 hit (3897)
    grep -n -i "reinterpret"                          → 2 hits (1503, 3173)
    grep -n -i "renam"                                → 1 hit (3318)
    grep -n "channel name\|channel's name\|name (§4.6)" → 6 hits
    grep -n "fill value"                              → 14 hits
    grep -n "R-COD-07"                                → 6 hits
    grep -n -B14 "R-CNF-01"                           → 1 requirement, read in full
    grep -n "^#### 21\.|^#### 20\.|^### 21\.|^### 14\.|^#### 14\." → section map
    tr '\n' ' ' | tr -s ' ' | grep -o "for a tile the layer stores[^,]*,"  → 2 hits
    tr '\n' ' ' | tr -s ' ' | grep -o "generation this commit supersedes" | wc -l → 5
    tr '\n' ' ' | tr -s ' ' | grep -o "stores in the generation this commit supersedes" | wc -l → 2
    tr '\n' ' ' | tr -s ' ' | grep -o "..........................the layer stores................................" → 5 hits
    grep -n "for a tile the layer stores\|wherever the layer stores\|Either is such\|exactly when its index\|not the shape of the edit\|same tense and for the same\|that channel's fill\|Call this the" → 8 hits

Restatement sites found and each judged:

1. **§11.1 Rationale, 1601-1625.** Already swept — it says "Of its **three** bars" and
   names all three, including "a change to a planar layer's channel declarations that
   moves a stored tile's disk ordinal" (1615-1617). Content agrees with §20.3. BUT it
   is the *only* place that says the two new bars reach neither a shrink nor a
   **growth** (1614-1615), and it is labeled **Rationale.** → non-normative under
   [R-CNF-01]. §20.3's normative counterpart at 3235-3238 covers only the shrink.
   Finding A-05.
2. **§21.7, 3895-3901 and 3906-3908.** Swept — "its two companion bars", correct tense
   ("in the generation the commit supersedes"), and it repeats the uint8→bool element-
   size counterexample consistently with 3166-3169. No defect.
3. **§20.3's Example block, 3291-3336 (shape (c)).** Uses "a layer that **stores** a
   tile carrying either" unqualified at 3320-3321, then gets the tense right in the
   next sentence. Labeled **Example.** → non-normative. Not raised; recorded as R-3.
4. **§23.1, 4152-4158.** Lists what a commit makes unreachable, "(§20.3 step 4)", and
   explicitly says "the list of operations above is not offered as closed" (4173-4174).
   Needed no sweep.
5. **Register.** No row in §21.2-§21.6 restates any of the three bars — consistent with
   §21.7's statement that they are unwitnessed. Nothing to sweep.

## 12. Byte-level reasoning, per finding

The discriminating question each time: is the disputed file itself conforming?

- **A-01, A-02.** The disputed file is one produced by a commit that both re-declares
  and unstores. §21.7 line 3928-3932 states in terms that such a file's live state is
  clean and the §14 bar is unwitnessed there; no register row fires; [R-CNF-05] bars
  nothing. So the file is conforming, and only the superseded-tense reading forbids a
  writer from producing it. The set moves. Byte-level, both.
- **A-03.** Disputed file: a planar layer, C ≥ 2, stored tiles, one extent grown so a
  grid count rises. The grown file is conforming (§11.1's Rationale describes exactly
  this shape as ordinary). One reading permits it, one does not. Byte-level.
- **A-05.** Same file as A-03; the defect is that its permission's only statement is
  non-normative. Byte-level for the same reason.
- **A-06.** Disputed file: a directory in which a channel entry's name (and, where no
  padding position or pad bit exists, its fill) differs from the superseded
  generation's, over unchanged tile payloads. I could find no rule such a file
  violates. One reading of 3173 forbids a writer from producing it. Byte-level.
- **A-04.** Not byte-level. Both readings of "any channel of a layer that stores a
  tile" reject the same commit; there is no fork, only an obligation broader than its
  own justification.
- **A-07, A-08, A-09.** Not byte-level. None of the three changes any verdict about any
  file; they are a false warrant, a false inventory, and a degraded anaphor.

## 13. Rejected candidates

- **R-1. "An interleaved layer is unaffected" (3200) read as a general licence.** A
  reader could take it to mean interleaved layers may edit channel declarations freely,
  which the §14 bar forbids (inserting a channel changes Q and hence the decoded size
  P·Q, §14.2). Dropped because the sentence's own reason clause — "its disk ordinal
  being s, which no channel declaration enters" — confines "unaffected" to the ordinal
  bar, and the sentence sits in a paragraph about nothing else.
- **R-2. "the §14 bar does not reach it because it is not an effect on any stored tile's
  bytes" (3181-3182) as a mis-individuation.** §14.1 line 1934-1937 phrases the planar
  case as "the tile with disk ordinal c · N + s ... carries exactly the values of
  channel c", which invites individuating a tile by its ordinal; on that reading, a
  channel reorder DOES change what §14 fixes for "the tile at ordinal 0" (its channel,
  and if the two channels' element sizes differ, its decoded size P·Bᶜ). Dropped
  because §3.1's governing definition individuates a planar tile as "one cell of the
  grid for one channel" and §14.1's formula is itself parameterised by c and s, so the
  tile keeps its identity across the renumbering. The claim stands.
- **R-3. The Example at 3320-3321 using unqualified "stores".** Dropped: the block is
  labeled **Example.**, so [R-CNF-01] makes it non-normative, and its next sentence
  states the tense correctly.
- **R-4. Channel removal de-addressing a stored tile.** The licence for dropping a tile
  out of the addressed set (3222-3225) is parenthetically tied to a falling grid count,
  not a falling channel count, so whether removing the last channel of a planar layer
  that stored tiles for it is permitted is arguably not stated. Dropped — narrowly —
  because 3190-3191 blesses "removing the last" in the same breath as the ordinal test,
  3201-3202 makes "barred ⇒ new layer" the only exit, and §23.1 line 4152-4157 treats
  the family of unreachability-producing operations as open and permitted. I record it
  here because it is the closest call I made, and a maintainer may wish to add "or a
  channel is removed" to 3223's parenthesis.
- **R-5. The §14 bar's enumerated list omitting pad bits.** "the set of padding
  positions (§11.3) and the content `[R-SER-05]` fixes there" names padding positions;
  §14.3's Note is explicit that "Pad bits are not padding positions". Dropped: the list
  is expressly non-exhaustive at 3143-3145 ("the list names where that effect arises
  rather than standing on its own"), and this is pre-existing §14-bar text, not my
  hunks.
- **R-6. Layout change planar↔interleaved evading the ordinal bar.** Dropped: the bar's
  subject is channel declarations, and the §14 bar catches every layout flip except
  C=1 numeric, where I verified the decoded image is byte-identical (planar P·Bᶜ vs
  interleaved P·Q with Q=Bᶜ) and the ordinal is s either way, so nothing is evaded.

## 14. Confidence

I ran all eight checks against both hunks. Checks 2 (citations), 3 (placement) and the
whole of §3 above (ordinal arithmetic) came back clean, and I have shown the work for
each rather than asserting it: every stated number in hunk 4 reproduces from
[R-GEO-06], [R-GEO-03], §12.1's table and §14.2/§14.3's size formulas, including the
worked example position by position and the P=1 coincidence. Checks 1, 4, 5, 6, 7 and 8
each produced at least one finding. Nine findings from two hunks is more than I
expected; A-01 through A-03, A-05 and A-06 are the ones I would defend hardest, and
A-08 and A-09 are small and I say so.

What I could not check: anything outside spec/tarn.md — the register's tooling, the
conformance vectors, the other seven hunks. If another hunk adds the growth disclaimer
A-05 asks for, or the tense qualifiers A-01/A-02 ask for, my findings there are
already satisfied and should be dropped; I had no way to see that.
