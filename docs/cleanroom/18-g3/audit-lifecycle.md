# Round 18 repair audit — lifecycle pair (hunk-01, hunk-02)

Auditor working transcript. Verbatim record of what was read, what was run,
and what was concluded. Written to be checked, not skimmed.

## 0. Access disclosure

Read, in full or in the ranges named below:

- `/private/tmp/.../round18-audit/hunk-01.diff` (whole file, 26 lines)
- `/private/tmp/.../round18-audit/hunk-02.diff` (whole file, 20 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  96–113, 172–193, 282–341, 1036–1046, 1430–1549, 1560–1572, 1787–1826,
  1950–1981, 2310–2349, 2857–2896, 2930–3014, 3010–3149, 3516–3567,
  3567–3616.

Nothing else was read. No `docs/`, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no
`AGENTS.md`, no `README.md`, no `conformance/`, no `spec/registry.json`, no
git history/log/diff, no web, no `full.diff`, no other hunk file, no listing
of the audit directory. Commands run were `grep`/`sed`/`tr` against
`spec/tarn.md` only; each is reproduced verbatim below with its output.

Wrote exactly one file: this transcript.

---

## 1. The two hunks

### Hunk 1 — §11.1 Rationale, spec/tarn.md line 1478ff

Round 16 (deleted):

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes
> for a tile the new state still stores, and permitted where it drops tiles
> out of the addressed set, whose extents then become slack. A layer that
> stores nothing may be re-declared freely.

Round 17 (current, lines 1482–1489):

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: a shrink is
> barred wherever it alters what §14 fixes for such a tile — whether or not
> the new state still stores it — and permitted where it only drops tiles out
> of the addressed set, whose extents then become slack. A layer that stored
> nothing may be re-declared freely.

**Rule the repair asserts, in my words.** For a layer that had at least one
stored tile in the generation the commit supersedes: an extent shrink is
forbidden if it changes anything §14 fixes about any such tile, and the
commit cannot escape that by also unstoring the tile. A shrink whose only
effect is to push tiles out of the addressed set is allowed, and those tiles'
stored bytes become slack. A layer that had no stored tile in the superseded
generation may be re-declared with no constraint stated here.

### Hunk 2 — §20.3 Example shape (c), spec/tarn.md line 3078ff

Round 16 (deleted): `A layer storing no tile is re-declared freely whatever
its geometry, which is the same step's permission.`

Round 17 (current, lines 3083–3085): `A layer storing no tile is re-declared
freely, subject to every rule its new geometry is subject to, which is the
same step's permission.`

**Rule the repair asserts, in my words.** A layer with no stored tile may have
its record re-declared — including its geometry — by an appender, and the
resulting geometry must still satisfy every rule that applies to a geometry;
the permission is step 4's, not a separate one. The repair withdraws the claim
that the new geometry is unconstrained.

---

## 2. The normative rules these two rationales are rationales FOR

Both live in §20.3 step 4 (`[R-WRT-04]`), spec/tarn.md lines 2934–3008. This
text is a numbered list item, **not** inside a `>` block — I checked every
line of 2934–3014 for a leading `>` and there is none. So it is normative
under `[R-CNF-01]` (line 104–106: "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative.").

### 2a. The bar (hunk 1's subject), lines 2951–2968, verbatim

> A commit MUST NOT change a
> layer's declarations in a way that alters, for any tile that layer
> stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode —
> the set of padding positions (§11.3) and the content
> `[R-SER-05]` fixes there, the decoded size, the byte offset of any
> sample within the decoded tile image, or the codec and filter that
> produced the stored bytes. The tense is the prior generation's
> (§3.1 defines *stored* against a generation), so a commit does not
> escape this by unstoring in the same breath: superseding every
> tile of a layer and re-declaring it are one operation, and this
> bars it. The test is the effect on such a tile, and the list names
> where that effect arises rather than standing on its own: a change
> that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — a filter whose mandated stride makes it
> the identity (`[R-COD-10]`), or a new padding position whose
> stored byte already holds the fill `[R-SER-05]` fixes — is not
> what this bars.

### 2b. The shrink clause (hunk 1's subject), lines 2990–3008, verbatim

> An extent MAY also **shrink**, and the bar above is the whole of
> the test, **in the bar's own tense**: a shrink is permitted
> exactly where it alters nothing §14 fixes for any tile the layer
> stores in the generation this commit supersedes. Dropping a tile
> out of the addressed set (§11.2's grid count falls) is not itself
> such an alteration — a tile the new state does not address carries
> no §14 obligation and its extent becomes slack — but neither does
> it rescue a commit that damages a prior-generation stored tile.
> Unstoring that tile in the same commit does not rescue it either,
> and for the same reason: the quantifier is the superseded
> generation's, so a shrink that turns real positions into padding
> of a tile stored there is barred whether or not the new state
> still stores it. §21.7 records the consequence [...]
> Where a shrink is permitted the de-addressed tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and
> so a re-emitted index region, and every surviving stored tile is
> untouched.

### 2c. The empty-layer permission (hunk 2's subject), lines 2975–2988, verbatim

> A layer that stores no tile **in the
> generation this commit supersedes** MAY be re-declared freely,
> which is what schema-first creation needs (§11.1) — the tense is
> the bar's, so a commit does not earn this permission by emptying
> the layer as it re-declares it; and an extent MAY **grow**, since a position that
> becomes real held that channel's fill and fill is a legal sample
> value — provided the grown geometry stays within every bound the
> layer's own declarations impose, `[R-COD-07]`'s lz4 decoded-size
> cap among them (L44), which an
> empty layer escapes only because that cap is quantified over
> addressed tiles. `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every derived
> product is another, and the list is not offered as exhaustive:
> a growth is permitted exactly where the geometry it produces
> satisfies every rule that geometry is subject to.

### 2d. The re-emission obligation (bears on hunk 2), lines 2936–2946, verbatim

> Every layer
> whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full — entry_count entries
> plus the segment CRC array — necessarily at a new placement
> (`[R-LIF-01]`), with entries [...] new to this
> generation (added tiles, grown extents) emitted per §15 [...]

---

## 3. CHECK 1 — tense and quantifier

### Hunk 1

| clause | rationale (repaired) | normative | verdict |
|---|---|---|---|
| whose layer | "already stored tiles in the generation a commit supersedes" | "for any tile that layer stores **in the generation this commit supersedes**" | MATCH (past tense now explicit; round 16's "already stores" was the untensed form) |
| bar's range | "for such a tile — whether or not the new state still stores it" | "barred whether or not the new state still stores it" (3001–3002) | MATCH — near-verbatim |
| escape | (implied by "whether or not") | "a commit does not escape this by unstoring in the same breath" | MATCH |
| permission | "permitted where it **only** drops tiles out of the addressed set" | "permitted **exactly where** it alters nothing §14 fixes for any tile the layer stores in the [superseded] generation"; de-addressing "is not itself such an alteration ... but neither does it rescue" | NOT the same quantifier — see finding A-03 |
| empty layer | "A layer that stored nothing may be re-declared freely." | "A layer that stores no tile **in the generation this commit supersedes** MAY be re-declared freely" | MATCH on tense and on the word "freely" |
| slack | "whose extents then become slack" | "the de-addressed tiles' extents become slack (`[R-CNT-21]`)" | MATCH |

Round 16 → 17 direction check: round 16 said the bar ranged over "a tile the
new state still stores". The normative rule ranges over tiles stored in the
**superseded** generation, and says so in bold, twice, and spends four
sentences insisting on it. So round 16's rationale was the stale one and
round 17 moved it the right way. The repair's direction is correct.

Also checked §3.1 (line 312–317) for the default tense of the bare word:

> **addressed tile / stored tile** — every tile of a layer is *addressed*. A
> tile is *stored in a generation* if and only if that generation's tile-index
> entry for it is not the sentinel (§15); unqualified *stored* means stored in
> the live generation.

So an unqualified "stores/storing/stored" resolves to the live generation. For
an appender mid-commit the live generation is the one being superseded, which
is why the untensed form is *defensible* — and also why §20.3 refuses to rely
on it and bolds the qualifier instead.

### Hunk 2

The repair changed the geometry clause and left `A layer **storing** no tile`
untensed. The normative rule it cites ("which is the same step's permission")
names the generation twice in bold and adds an explicit anti-escape clause.
The sister rationale (hunk 1) had exactly this word repaired in the same round
("stores nothing" → "stored nothing"). Finding A-02.

Quantifier of "subject to every rule its new geometry is subject to": the
normative closing generalization is "a growth is permitted exactly where the
geometry it produces satisfies every rule that geometry is subject to"
(line 2987–2988). The repair's phrase is a near-verbatim lift. Note the
normative sentence is grammatically attached to the **growth** permission,
while the repair attaches it to the **re-declaration** permission; the
transfer is sound because `[R-CNF-05]` (line 180: "A writer MUST emit only
conforming files") and `[R-WRT-05]` (line 3101–3105: "a record it modifies is
new output under its writer obligations (`[R-CNF-05]`)") bind any re-declared
record to every writer rule regardless. So the repair is true; it is not an
overclaim in either direction. Passes.

---

## 4. CHECK 2 — citations resolve

Every identifier and section number in the repaired text, and in the sentences
either side that the repair leans on. Each was opened.

| citation | where cited | what I read | verdict |
|---|---|---|---|
| §20.3 | hunk 1: "§20.3 states normatively, and governs" | line 2891 `#### 20.3 The append procedure`; step 4 at 2934–3020, no `>` prefix on any line, terminating `[R-WRT-04]` at 3026 | PASS — normative, and it does state both the bar and the empty-layer permission |
| §14 | hunk 1: "what §14 fixes for such a tile" | line 1787 `### 14. Tile Serialization` — "defines the **decoded tile image**"; §14.2 byte layout and decoded size; §14.5 padding content (`[R-SER-05]`) | PASS — §14 is where padding content, decoded size and in-image byte offsets are fixed |
| §11.2 | hunk 1 context: "every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2)" | line 1497 `#### 11.2 Grid arithmetic`, Gᵢ = ⌈Eᵢ / Tᵢ⌉ | PASS |
| `[R-CNT-17]` | hunk 1 context: "changes entry_count and with it extent_length" | line 1038–1042: "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0); a mismatch, or an entry_count that does not equal the geometry-derived addressed-tile count, is a validity error at layer scope" | PASS — and this is what makes finding A-01's mis-emitted file non-conforming (rows L21/L22) |
| `[R-GEO-06]` | hunk 1 context: "disk ordinals renumber wherever `[R-GEO-06]` moves them" | lines 1560–1568: disk tile ordinal is s interleaved, c·N + s planar | PASS — N changes with grid count, so planar ordinals do move |
| `[R-WRT-04]` | hunk 1 context: "(§20.3, `[R-WRT-04]`)" | line 3026, the id terminating §20.3's numbered procedure | PASS |
| `[R-GEO-02]` | the normative sentence hunk 1 attaches to (line 1479) | line 1476–1479, extent 0 valid, zero addressed tiles, empty index | PASS |
| step 4 | hunk 2: "(step 4)" and "the same step's permission" | §20.3's item 4 = "**Write payloads and indexes**", lines 2934–3020, which carries both the MUST NOT bar and the empty-layer MAY | PASS |
| `[R-CNT-25]` | hunk 2 context: "its document lives in an extent" | line 897 `[R-CNT-25]`; rows F21 (extent slot (0,0) placing the document inline is a violation), L10 | PASS — a user-metadata document may not be inline, so it does live in an extent |
| `[R-COD-07]` / L44 | normative text hunk 2 restates | line 2314–2324 and register row L44 (line 3442): "Codec 4 (lz4) declared on a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000" | PASS — the cap really is quantified over addressed tiles, so an empty layer really does escape it |
| §21.7 | normative text hunk 1 restates | lines 3597–3607: "§20.3 step 4's bar on a declaration change is witnessed only where the affected tiles remain stored *and* ... a commit that supersedes every tile it would have damaged leaves the live state clean, so the bar is unwitnessed there" | PASS — independently confirms the repair's "whether or not the new state still stores it" |

No citation in either repaired sentence points at a rule that only
almost says the claimed thing. Check 2 passes with zero findings.

---

## 5. CHECK 3 — does the repair sit in normative text?

Both hunks are inside `>` blocks, so neither carries force. The question is
whether the rule each states is stated normatively elsewhere, and whether the
normative statement now agrees.

Greps run (blockquote markers stripped first where needed, because the `>` and
the hard wrap both defeat naive line-oriented matching — noted because a grep
that could not have succeeded proves nothing):

```
$ grep -n "re-declar\|redeclar\|declared freely\|freely" spec/tarn.md
1488:> then become slack. A layer that stored nothing may be re-declared
1489:> freely. Growth
2961:   tile of a layer and re-declaring it are one operation, and this
2976:   generation this commit supersedes** MAY be re-declared freely,
2979:   the layer as it re-declares it; and an extent MAY **grow**, since a position that
3083:> stored tile is re-declared
3084:> freely, subject to every rule its new geometry is subject to, which
```

Exactly three statements of the empty-layer permission: line 2976 (normative,
§20.3 step 4), line 1488 (hunk 1, rationale), line 3083 (hunk 2, example).
The normative one at 2976 says the right thing, in the right tense, with the
geometry caveat supplied by the clause that follows it. So hunk 2's repair did
not have to land in normative text and the old rule is not left standing.

```
$ grep -n "shrink\|shrunk\|de-address\|deaddress" spec/tarn.md
1485:> shrink is barred wherever it alters what §14 fixes for such a
2990:   An extent MAY also **shrink**, and the bar above is the whole of
2991:   the test, **in the bar's own tense**: a shrink is permitted
3000:   generation's, so a shrink that turns real positions into padding
3005:   Where a shrink is permitted the de-addressed tiles' extents become slack
```

Two statements of the shrink rule: line 2990ff (normative) and line 1485
(hunk 1, rationale). The normative one already carries the superseded-
generation tense — this is the rule round 17 was reconciling the rationale
*to*, not a rule it was trying to change. So hunk 1 is not a
rationale-only rule either.

Unwrapped searches for further restatements:

```
$ tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o ".\{120\}empty layer.\{140\}"
[3 hits: §17's codec-4 Note (line 2326-2334); §20.3 step 4 line 2983; §21.6 row]

$ tr '\n' ' ' < spec/tarn.md | tr -s ' ' | grep -o "..\{160\}zero-extent.\{160\}"
[3 hits: §1 bullet; §11.1's own rationale line 1495; §19 read path]

$ sed 's/^> *//' spec/tarn.md | tr '\n' ' ' | tr -s ' ' | grep -o ".\{130\}directory alone.\{120\}"
 layer that stored nothing may be re-declared freely. Growth that leaves every
 grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the directory alone; growth
 that raises one changes entry_count and with it extent_length (`[R-CNT-17]`),
 so the layer's whole tile-index r...
```

The §17 Note at 2326–2334 is the third restatement of the empty-layer escape,
and it is the one that most directly explains hunk 2's reported defect:

> **Note.** The cap is quantified over the layer's *addressed* tiles, so a
> layer that addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) —
> satisfies it whatever its tile shape declares, and codec 4 is conforming
> there. The escape is not durable: a later commit that grows an extent
> addresses tiles, and the same declarations are then measured against the cap.

This one already carries the "not durable" caveat and is correctly scoped to
the lz4 cap alone, so it needed no sweeping and got none. It is consistent
with hunk 2's repair. **No unswept restatement here.**

Check 3 passes for both hunks: each repair restates a rule that is stated
normatively and correctly at §20.3 lines 2951–3008.

---

## 6. CHECK 4 — contradiction in the same passage, including untouched text

### 6a. Hunk 1's passage — §11.1, lines 1465–1495, read whole

`[R-GEO-01]` (1468–1474), `[R-GEO-02]` (1476–1479), then the rationale
(1481–1495). Untouched sentences in that rationale:

- "Empty layers serve schema-first workflows" — agrees with §20.3 line 2977
  ("which is what schema-first creation needs (§11.1)"). The two cross-cite
  each other; no conflict.
- "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the
  directory alone" — consistent with `[R-CNT-17]`: unchanged grid counts means
  unchanged entry_count means unchanged extent_length means the index region
  need not move. Consistent with §20.3 shape (c).
- "growth that raises one changes entry_count and with it extent_length
  (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted ... —
  **the first growth of a zero-extent layer included**." Consistent with
  `[R-CNT-17]` ("and 0 when entry_count is 0"): a zero-extent layer's slot is
  (0,0)/length 0, so growing it necessarily writes a new index region.

No sentence in §11.1 was written to be true only under round 16's wording. I
looked specifically for a "still stores"-shaped clause elsewhere in the
subsection and there is none. **No contradiction found inside hunk 1's own
passage.**

### 6b. Hunk 2's passage — §20.3 example (c), lines 3077–3093, read whole

Verbatim, whole shape (c):

> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, or changing a channel's fill value on
> a layer with no padding position and no pad bit. **Only the directory
> is re-emitted.** A fill change on a layer that **stores** a tile
> carrying either is not an appender's operation at all (step 4): it
> would invalidate every stored tile it reaches. A layer storing no tile
> is re-declared freely, subject to every rule its new geometry is
> subject to, which is the same step's permission. Editing user metadata
> is not this shape: its document lives in an extent (`[R-CNT-25]`), so a
> new extent is appended and the old one becomes slack, as in (b).

followed by the diagram, in which `after` contains only `│front│ A:
tiles+index │▓▓▓▓▓▓▓▓▓▓▓▓▓│ dir₂│pad│tr₂│` — no new index region.

**This is the contradiction.** The paragraph's frame is "Only the directory is
re-emitted", and the paragraph polices its own membership twice ("is not an
appender's operation at all", "is not this shape"). The repaired sentence is
unflagged and now expressly contemplates a **new geometry**. But a
re-declaration that changes a layer's addressed-tile count re-emits that
layer's whole tile-index region — §20.3 step 4 itself requires it
(lines 2936–2946, "entries new to this generation (added tiles, grown
extents) emitted per §15"), `[R-CNT-17]` forces it, and hunk 1's own passage
says so in as many words: "the first growth of a zero-extent layer included."

So the repair, which was written to *narrow* an overclaim, left the sentence
sitting under a frame that is false for exactly the case the new wording
invites. Finding A-01. Note the direction: the round-16 text ("whatever its
geometry") had the same collision, so the repair neither caused nor swept it —
it is an undershoot, and the two hunks now disagree about the same commit.

Other untouched text in (c) checked for collision with the repair:

- "A fill change on a layer that **stores** a tile carrying either is not an
  appender's operation at all" — no collision with the repair's breadth; it is
  the complementary case. It does share hunk 2's untensed "stores" (see A-02).
- "Editing user metadata is not this shape" — no collision.
- The closing paragraph at 3095–3097 ("In every shape the file grows and no
  committed byte changes") — consistent.
- Shapes (a) and (b) at 3048–3075 — (b) explicitly covers "That layer's index
  is re-emitted whole", which is where a geometry-changing re-declaration
  actually belongs. Read and cross-checked; it does not itself claim the
  empty-layer case.

### 6c. §20.4's table row and paragraph (lines 3119–3133)

Read in full because it is the next structure and it reasons about "modifying
any layer's record". The MU=0/PE=0 row says a commit changes the file's layer
set "by adding a layer and equally by modifying any layer's record". A
re-declaration of an empty layer modifies that layer's record, so this row is
consistent with both hunks. No collision.

---

## 7. CHECK 5 — exhaustive claims

Every completeness word in the two repaired sentences, and the attempt to
falsify each:

| word | in | falsification attempt | verdict |
|---|---|---|---|
| "wherever it alters" (hunk 1) | universal over shrinks | §20.3's carve-out: "a change that leaves every one of those tiles' stored bytes meaning exactly what they meant — ... or a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars." Concrete case: E 1024→1000, T 256, four stored tiles; positions 1000–1023 of tile 3 become padding; `[R-SER-05]` (line 1952–1961) requires fill there; if the stored bytes already hold fill, §20.3 permits the shrink. The rationale's list-form test ("alters what §14 fixes", and §20.3's list names "the set of padding positions" first) says it is barred. | FALSIFIED — finding A-03 |
| "whether or not the new state still stores it" (hunk 1) | closed binary | matches line 3001–3002 verbatim; §21.7 confirms the unstoring case | HOLDS |
| "only drops tiles out of the addressed set" (hunk 1) | presented as the permission half of a dichotomy | the normative permission is "exactly where it alters nothing §14 fixes", strictly broader — the shrink above is permitted and drops no tile | FALSIFIED as a partition — finding A-03 |
| "freely" (hunk 1) | uncaveated licence | matches the normative word at line 2976 exactly; bounded in force by `[R-CNF-05]`/`[R-WRT-05]` under both readings | HOLDS (but see the asymmetry note below) |
| "every rule its new geometry is subject to" (hunk 2) | universal | this is the *repair*; it can only be falsified by finding a rule the geometry is subject to that the sentence excludes, and by construction it excludes none | HOLDS |
| "freely" (hunk 2) | now caveated | — | HOLDS |
| "the same step's permission" (hunk 2) | identity claim about step 4 | step 4 does grant it (line 2975–2976) | HOLDS |

**Asymmetry noted and deliberately not filed as a separate finding.** Hunk 2
now reads "freely, subject to every rule its new geometry is subject to" while
hunk 1 still reads bare "freely". That is a three-way spread across §20.3 step
4 (normative, "freely"), §11.1 (rationale, "freely"), §20.3(c) (rationale,
"freely, subject to..."). I considered filing it as an unswept restatement and
decided against it: §11.1's wording is *verbatim the normative wording*, so it
is not stale relative to any rule; the word "freely" in a licence is bounded by
`[R-CNF-05]` under every reading; and the round-16 defect was specifically the
explicit exhaustive claim "whatever its geometry", which §11.1 never carried.
Filing it would be padding. Recorded here so the decision is visible.

---

## 8. Byte-level analysis

The controlling text for all three findings is §20.3 step 4, which is
normative and unambiguous, and `[R-CNF-01]` strips all three disputed
sentences of force. So for each I asked the discriminating question anyway.

**A-01.** The file a permissive reading of shape (c) produces — a layer record
declaring a new geometry whose addressed-tile count differs from the retained
index region's entry_count — violates `[R-CNT-17]`, register rows L21
("entry_count does not equal the geometry-derived addressed-tile count",
reject at layer access) and L22 (extent_length against the formula, "or a
nonzero slot with entry_count = 0"). `[R-CNF-05]` therefore bars every
conforming writer from emitting it under *both* readings. The emittable set
does not move. **Not byte-level.**

**A-02.** Here the disputed file *is* conforming, which I checked carefully.
Construct: layer L, E=(1024), T=(256), four stored tiles. One commit both
supersedes all four entries to the sentinel and changes T to 512. Result:
entry_count 2 (= addressed-tile count ✓ `[R-CNT-17]`), extent_length
2·20 + 1·4 = 44 ✓, both entries sentinel, prior payloads slack (unconstrained
content, §21.6 row for slack). Every register row is satisfied; §21.7 says so
directly — "a commit that supersedes every tile it would have damaged leaves
the live state clean, so the bar is unwitnessed there". §20.3 step 4 bars an
appender from producing it ("a commit does not earn this permission by
emptying the layer as it re-declares it"; T 256→512 changes P and hence the
decoded size, which §14 fixes for a tile stored in the superseded generation).
A permissive reading of hunk 2's untensed "storing no tile" permits it.

So the charter's literal discriminator is met — conforming file, one reading
permits it. I still answer **not byte-level**, and state the reason plainly
rather than suppressing it: the two texts are not two readings of one rule.
§20.3 step 4 is normative and says exactly one thing; hunk 2 is inside a `>`
block and under `[R-CNF-01]` carries no force. The set of files a *conforming*
implementation may emit is fixed by step 4 alone and does not move when hunk 2
is reworded. What does move is the set of files a *careless* implementation
emits — and because the violation is unwitnessed (§21.7), no verifier will
ever catch it. That is the real cost and it is why the finding is worth filing,
but it is not the byte-level test.

**A-03.** Same structure as A-02 and the same answer. The shrink at issue
(E 1024→1000 with fill already in place) produces a conforming file; §20.3
permits the commit; §11.1's gloss reads as barring it. §11.1 is a Rationale
and says in its own first clause that "§20.3 states normatively, and governs".
Conforming set unmoved. **Not byte-level.**

---

## 9. Findings

- **A-01** (hunk 2, LOCAL_CONTRADICTION, not byte-level) — the repaired
  sentence contemplates a new geometry while sitting under shape (c)'s "Only
  the directory is re-emitted"; a re-declaration that changes the
  addressed-tile count re-emits the index region, as hunk 1's own passage
  says ("the first growth of a zero-extent layer included") and as §20.3 step
  4 and `[R-CNT-17]` require.
- **A-02** (hunk 2, TENSE_QUANTIFIER, not byte-level) — "A layer **storing**
  no tile" names no generation, while the rule it cites bolds "in the
  generation this commit supersedes" and forecloses earning the permission by
  emptying the layer in the same commit. Round 17 repaired precisely this word
  in hunk 1 and did not sweep it here.
- **A-03** (hunk 1, OVERCLAIM, not byte-level) — the repaired dichotomy
  ("barred wherever it alters ... / permitted where it only drops tiles")
  over-bars and under-permits against §20.3's biconditional, because it drops
  the normative carve-out that a change leaving stored bytes meaning what they
  meant is not barred. The repair correctly widened the set of tiles the bar
  ranges over, which makes the omitted carve-out bite over a strictly larger
  set than it did in round 16.

## 10. What I looked for and did not find

- No citation defect in either hunk (11 citations opened, all pass).
- Neither repair is a rationale-only rule; both restate normative text at
  §20.3 lines 2951–3008 that already says the right thing (check 3 clean).
- No contradiction inside §11.1 (check 4 clean for hunk 1).
- No unswept restatement: `re-declar|freely` yields exactly three sites and
  `shrink` exactly two, all accounted for; §17's codec-4 Note is the only
  other place the empty-layer escape is discussed and it is already correct.
- No new ambiguity introduced by hunk 1's wording beyond A-03, and none by
  hunk 2's added clause itself.
- Hunk 1's tense repair moves in the correct direction — the normative rule
  was already the superseded-generation one, so round 16's rationale, not the
  rule, was the stale text.
