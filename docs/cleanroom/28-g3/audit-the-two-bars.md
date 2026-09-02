# Repair audit — hunks 3 and 4 of case-adr0113 ("the two bars")

Auditor lane: the two new requirements in §20.3 step 4 (the sample-type bar and
the planar disk-ordinal bar), and the shrink sentence they landed beside.

---

## 0. Disclosure — exactly what I read and ran

Files opened with a read tool:

- `/private/tmp/.../scratchpad/case-adr0113/hunk-03.diff`
- `/private/tmp/.../scratchpad/case-adr0113/hunk-04.diff`

Files read via `sed`/`grep`/`awk` through Bash:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only.

Ranges of `spec/tarn.md` I read in full:

- 3060–3300 (§20.2 tail, all of §20.3 including the whole of step 4 and the
  trailing Note/Example blocks)
- 3282–3362 (rest of §20.3's blocks, into §20.4)
- 1584–1730 (§11.1, §11.2, §11.3, §11.4 — `[R-GEO-01]`…`[R-GEO-06]`)
- 1727–1830 (§12.1, §12.2, §12.3)
- 1823–1925 (§13.1, §13.2, §13.3)
- 1921–2120 (all of §14: `[R-SER-01]`, `[R-SER-06]`, `[R-SER-02]`,
  `[R-SER-08]`, `[R-SER-03]`, `[R-SER-07]`, `[R-SER-09]`, `[R-SER-05]`)
- 1067–1180 (§7.4 the layer record)
- 2244–2346 (§16 — `[R-SLB-05]`, `[R-SLB-01]`, `[R-SLB-02]`, `[R-SLB-03]`,
  `[R-SLB-04]`)
- 2440–2540 (`[R-COD-07]`, `[R-COD-08]`, `[R-COD-09]`, `[R-COD-10]`)
- 3422–3500 (§20.5 compaction, `[R-WRT-06]`)
- 3884–3968 (all of §21.7)
- 4174–4212 (§23.1)
- 3113–3136, 3155–3245 re-read line-numbered for exact quotation.

I did **not** open `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, or the web. I did not list the case
directory.

**Context I did not ask for.** Material was placed in my context before I
began: a project instruction file (CLAUDE.md pointing at AGENTS.md), a
user-level auto-memory index naming two memory notes, and an MCP server
instruction block. None of it is part of the specification. I did not open any
of the files it names and I drew no conclusion from it; I record its appearance
here as the disclosure rule requires, without repeating its contents. One
practical effect: the MCP instruction block told me to prefer Bash over the
Read tool, which is why most of my reading is `sed`/`grep` output rather than
Read calls. That changes nothing about what I read.

---

## 1. The hunks, and the rule each repair adopts

### Hunk 3 (lands 3157–3228)

Inserts two whole paragraphs between the §14 bar's closing sentence and the
"layer that stores no tile … MAY be re-declared freely" permission, and edits
two clauses in that permission sentence.

**Rule the sample-type paragraph makes true of an implementation.** If a layer
stored at least one tile in the generation a commit supersedes, that commit may
not change the declared sample type of *any* of that layer's channels —
including, on a planar layer, a channel that stored nothing — whatever the
layout, and whether or not the element size changes. The only route to a type
change on such a layer is a new layer or a whole-file rewrite. This is strictly
wider than the §14 bar, which reaches a type change only where the change
disturbs the padding set, padding content, decoded size, a sample's byte
offset, or the codec/filter.

**Rule the ordinal paragraph makes true.** On a planar layer, a commit may not
edit the channel declarations in a way that changes the `[R-GEO-06]` disk
ordinal of any tile the layer stored in the superseded generation. Reorders and
mid-list insert/remove are such edits *when a moved channel had a stored tile*;
appending a channel and removing the last one never are; interleaved layers are
outside the rule entirely.

**Rule the two clause edits make true.** (a) The re-declare-freely permission
now takes its tense from all three bars, not just the §14 bar. (b) The growth
justification now says a newly-real position held, *for each channel the
position carries*, that channel's fill (§14.5) — supplying the antecedent the
dangling "that channel's" lacked.

### Hunk 4 (lands 3237–3241)

**Rule it makes true.** For an extent shrink, the §14 bar is the exhaustive
test of *what a shrink alters*, in the superseded generation's tense — but a
shrink is still bound by step 4's other obligations (slack, entry_count, slab
and alignment declarations) exactly as any other commit is. It also replaces
the anaphor "the bar above" with the explicit name "the §14 bar".

---

## 2. Check 3 first — is the repair in normative text?

I applied the **label** test, not the ">" test.

```
awk 'NR>=3150 && NR<=3282 && /^[[:space:]]*>/ {print NR": "$0}' tarn.md
→ 0 hits
```

There is not a single blockquote line anywhere in 3150–3282. Both hunks land in
the body of numbered step 4 of §20.3, which carries no *Note*, *Example* or
*Rationale* label. Under `[R-CNF-01]` that is normative text. **Check 3 passes
for both hunks.** Note the consequence for the rest of this audit: every
explanatory sentence in the inserted paragraphs — the glosses, the worked
example, the characterisation of the neighbouring rule — is normative too, and
I have judged them on that footing.

The two nearby restatements *are* labelled and therefore non-normative, which I
verified by reading their opening words:

- line 1604 `> **Rationale.** Empty layers serve schema-first workflows…` —
  contains "Of its three bars…" and both new bars. Non-normative; already
  swept; consistent.
- line 3345-ish `> **Example — the three shapes a commit takes.**` — shape (c).
  Non-normative; discusses fill changes, not the new bars.

---

## 3. Ordinal arithmetic, derived from `[R-GEO-06]` rather than granted

`[R-GEO-06]` (line 1699): "The **disk tile ordinal**, which orders tile-index
entries (§15), is s for an interleaved layer, and **c · N + s** for a planar
layer (§14), where c is the channel's index (§3.1) — channel-major grouping."

`[R-GEO-06]` also fixes s = Σᵢ tᵢ · ∏_{j>i} Gⱼ; `[R-GEO-03]` (§11.2) fixes
Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏ Gᵢ, and addressed-tile count = N interleaved, C·N planar.

Position by position against the passage's worked example ("A layer with N = 2
and channels (`a`, `b`)"):

| edit | channel | c | ordinals c·N+s, N=2, s∈{0,1} | document says |
|---|---|---|---|---|
| before | a | 0 | 0·2+0=0, 0·2+1=1 → {0,1} | "`a` at ordinals 0 and 1" ✓ |
| before | b | 1 | 1·2+0=2, 1·2+1=3 → {2,3} | "`b` at 2 and 3" ✓ |
| append `c` | a,b | 0,1 | {0,1},{2,3} unchanged | "leaves those four where they are" ✓ |
| append `c` | c | 2 | 2·2+0=4, 2·2+1=5 → {4,5} | "adds 4 and 5" ✓ |
| exchange a,b | a | 1 | {2,3} (was {0,1}) | |
| exchange a,b | b | 0 | {0,1} (was {2,3}) | "moves all four" ✓ (4 of 4 tiles change ordinal) |

The general claims also reproduce:

- "reordering moves those channels the reorder re-indexes" ✓ — the ordinal is
  affine in c alone, so a channel moves iff its index moves.
- "inserting or removing one moves every channel after the affected position" ✓
  — insertion at k shifts c→c+1 for all c ≥ k; removal at k shifts c→c−1 for
  all c > k.
- "Appending a channel, or removing the last, re-indexes nothing and moves no
  ordinal at all" ✓ — position C (append) and position C−1 (remove last) have
  nothing after them; N is unchanged by either.
- "a disk ordinal is c · N + s, and N is the spatial-tile count, so the channel
  count enters the addressed-tile count C · N (§11.2) but no individual
  ordinal" ✓ — C appears in `[R-GEO-03]`'s C·N and nowhere in `[R-GEO-06]`'s
  c·N+s.
- "An interleaved layer is unaffected, its disk ordinal being s, which no
  channel declaration enters" ✓ — s = Σ tᵢ ∏_{j>i} Gⱼ, and Gᵢ = ⌈Eᵢ/Tᵢ⌉ is
  built from dimension entries only. Verified against §11.2's own example at
  line 1710: planar C=4, N=32, channel 2, s=10 → 2·32+10 = 74, which is the
  figure the document prints.

Two stylistic notes, neither a finding: the sentence "a disk ordinal is
c · N + s" is stated bare although it holds only for planar layers (the
qualifier arrives two sentences later); and the worked example never repeats
that the layer is planar, though its paragraph is headed "For a **planar**
layer". Both are recoverable from the immediate context.

**Element-size arithmetic** (§12.1 table, read in full): int8 = 1, uint8 = 1;
float32 = 4, int32 = 4. So for both examples the planar decoded size P·Bᶜ, the
interleaved P·Q, every offset k·Bᶜ and (k div C)·Q + F_{k mod C}, and
`[R-COD-10]`'s shuffle stride (= the channel's element size planar, Q
interleaved) are all invariant. The claim "moves no stored byte, no decoded
size and no sample offset" reproduces exactly. And under `[R-TYP-04]`/
`[R-TYP-05]` a sample value *is* its bit pattern, so "simply has the same bytes
read under a different type" is literally the document's own model.

**The bool/uint8 figure.** §14.2 gives planar numeric decoded size P·Bᶜ; §14.3
gives planar bool ⌈P/8⌉; §12.1 gives bool element size 1. With Bᶜ = 1 the two
are P and ⌈P/8⌉. P = ⌈P/8⌉ ⟺ P ≤ 1, and P = ∏Tᵢ with every Tᵢ ≥ 1
(`[R-GEO-01]`) so P ≥ 1. **P = 1 is the unique coincidence**, exactly as the
passage says. Checked P = 2 (2 vs 1), P = 8 (8 vs 1), P = 9 (9 vs 2) — all
differ.

---

## 4. The scoping to one layout, at ordinary and degenerate geometries

Bar 2 is written for planar layers. I tried to find a layout at which a channel
declaration moves an ordinal outside that scope, and a layout flip that escapes
every bar.

- **Interleaved, ordinary.** Ordinal = s. No channel declaration enters s.
  Correct to exclude. But note the *other* side: on an interleaved layer a
  channel edit changes Q = ΣBᵢ and every Fᶜ, so `[R-SER-02]`'s decoded size and
  offsets move and the **§14 bar** catches it whenever a tile is stored. The
  division of labour is sound.
- **Interleaved, C = 1.** Addressed count N; ordinal s. A channel edit is
  either a type change (bar 1) or an append/remove (append is harmless; remove
  is barred by `[R-CNT-23]`, C ≥ 1). Nothing escapes.
- **Layout flip, C = 1 numeric.** §14.4's Note: "A single-channel numeric layer
  produces byte-identical tile images under either layout." Ordinals: planar
  0·N+s = s; interleaved s. Addressed count: C·N = N either way. So the flip is
  a total no-op — nothing to bar, and nothing barred. Fine.
- **Layout flip, C = 1 bool.** §14.4's Note again: images differ wherever
  ⌈P/8⌉ ≠ P, i.e. wherever P > 1, and the §14 bar catches that as a decoded-size
  change. At P = 1 with fill false the images coincide and the flip is again a
  no-op. Fine.
- **Layout flip, C ≥ 2.** Q > Bᶜ for every c, so the tile at ordinal 0 changes
  decoded size; §14 bar catches. Fine.
- **Extent 1 / one tile / N = 1.** Planar ordinals c·1+0 = c; a reorder still
  permutes them; bar 2 bites normally.
- **A layer that addresses tiles but stores none.** Neither bar's antecedent is
  satisfied (both quantify over storing a tile); the explicit permission at
  3222–3223 covers it. Consistent.
- **A layer that addresses no tile (some Eᵢ = 0).** N = 0, addressed count 0,
  every product 0; stores nothing; permission applies. Consistent, and
  consistent with `[R-COD-07]`'s Note about the escape ending when the
  addressed count rises above 0.

**Verdict: the planar scoping is right, and I could not construct a case where
an interleaved layer needs bar 2.**

---

## 5. The shared quantifier — the three wordings side by side

- §14 bar, line 3131–3134: "A commit MUST NOT change a layer's declarations in
  a way that alters, **for any tile that layer stores in the generation this
  commit supersedes**, what §14 fixes for its stored bytes or how they decode".
- Bar 1, line 3172–3174: "a commit MUST NOT change the declared sample type of
  any channel of **a layer that stores a tile in the generation this commit
  supersedes**".
- Bar 2, line 3202–3204: "a commit MUST NOT change the channel declarations in
  a way that alters the disk ordinal `[R-GEO-06]` assigns **any tile the layer
  stores in the generation this commit supersedes**".
- Permission, line 3222–3223: "A layer that stores **no tile in the generation
  this commit supersedes** MAY be re-declared freely".

**They agree on tense.** All four are the superseded generation's; none is
stated over the new state. The permission is the exact complement of bar 1's
layer-level antecedent ("stores a tile" / "stores no tile"), so there is no gap
and no overlap between them.

They differ in *what they range over*, and correctly so: bar 1 ranges over
layers (one stored tile anywhere in the layer arms it for every channel), the
§14 bar and bar 2 range over tiles. Bar 1's layer-level scope is deliberate and
the passage says so and defends it at 3175–3190. That is not a defect; it is a
documented widening, and the passage even concedes its cost ("costs a rewrite
the format did not strictly need").

The repair also swept the permission's anaphor from "the bar's" to "these
bars'", which is the correct sweep — the permission is the complement of all
three antecedents, not just the §14 bar's. "these bars" is never enumerated in
§20.3 itself (only §11.1's Rationale says "its three bars"), which is slightly
loose, but the three MUST NOTs are the only candidates in the preceding text.
Not reported.

**However**, two *glosses* inside the inserted text drop the tense. See
findings A-02 and its second instance.

---

## 6. Check 2 — every citation opened

| citation | where | claim made | verdict |
|---|---|---|---|
| §14 (as "the §14 bar") | 3159, 3198, 3237, 3242 | names the bar defined at 3139 | **pass** — "Call this the **§14 bar**." is at 3139 |
| §12.1 | 3168 | "the element sizes of §12.1 do not settle it" | **pass** — the table gives bool = 1 and uint8 = 1, so element size is blind to the change |
| §14.3 | 3170 | planar bool plane is ⌈P/8⌉ | **pass** — `[R-SER-03]`: "the decoded size is ⌈P/8⌉ bytes" |
| §14.2 | 3179 | "the sample stride Q and each in-sample offset Fᶜ are sums over all of them" | **FAIL** — `[R-SER-02]`: "Q = Σ Bᵢ over all channels … and Fᶜ = Σ Bⱼ over **channels j < c**". Q is over all; Fᶜ is not, and F₀ is the empty sum 0. → finding **A-04** |
| `[R-GEO-06]` | 3203 | assigns a tile its disk ordinal | **pass** — line 1699 |
| §11.2 | 3212 | addressed-tile count is C · N | **pass** — `[R-GEO-03]`, line 1638: "is N for an interleaved layer and C · N for a planar layer" |
| §11.1 | 3224 | "which is what schema-first creation needs" | **pass** — `[R-GEO-02]` and its Rationale, "Empty layers serve schema-first workflows" |
| §14.5 | 3228 | a newly-real position held, for each channel it carries, that channel's fill | **pass** — `[R-SER-05]`: "at every padding position, a writer MUST encode, **for each channel the position carries**, that channel's fill value". The repair's added clause is `[R-SER-05]`'s own words |
| `[R-COD-07]` / L44 | 3229–3231 | lz4 cap; empty layer escapes it because quantified over addressed tiles | **pass** — `[R-COD-07]`'s Note: "The cap is quantified over the layer's *addressed* tiles"; row L44 reads "any of whose **addressed** tiles' decoded size exceeds 0x7E000000" |
| `[R-ENC-04]` | 3232 | 2⁶³−1 ceiling on every quantity it designates, carrying no such quantifier | **pass** — `[R-COD-07]`'s Note says exactly that |
| `[R-SLB-04]` | 3240 | mapped to "a slab … declaration" | **pass** — §16.2's closing rule: "A writer or updater whose commit changes the stored-tile set, the run partition, or the byte placement of any run of a slab-declared layer MUST either re-establish … or clear the declaration" |
| `[R-SLB-01]` | 3241 | mapped to "… or alignment declaration" | **pass** — §16.1: "A layer MAY declare alignment A … every stored tile's offset satisfies offset mod A = 0". The parenthetical's order matches the phrase's order (slab→SLB-04, alignment→SLB-01) |
| "the re-emission rule above" | 3199–3200 | "licenses a renumbering only for a geometry change" | **FAIL** — see A-01 |

The last row is not a bracketed identifier, but it is a citation in every sense
that matters, and it is the load-bearing one for bar 2's stated ground.

---

## 7. Check 4 — contradiction inside the passage, including untouched text

I read the whole of step 4 (3115–3281), both flanking steps, and the trailing
Note/Example blocks.

### 7.1 The one that bites — the "only for a geometry change" gloss

Inserted, 3197–3201:

> "A further effect is barred on the same tense, though on its own ground: the
> §14 bar does not reach it, an ordinal move being no effect on any stored
> tile's bytes, and what it disturbs is instead **the re-emission rule above,
> which licenses a renumbering only for a geometry change**."

The re-emission rule, untouched, 3117–3127, quoted exactly:

> "Every layer whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full — entry_count entries plus the
> segment CRC array — necessarily at a new placement (`[R-LIF-01]`), with
> entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel,
> entries new to this generation (added tiles, grown extents) emitted per §15,
> and every other entry byte-identical at its disk-ordinal position **(a
> geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)**."

The word "only" appears nowhere in it. The parenthetical states that a geometry
change renumbers; it does not state that nothing else may.

Now put the gloss against the repair's own carve-out, 3212–3215:

> "**The test is the effect on a stored tile, not the shape of the edit**: a
> commit that moves only the ordinals of channels the superseded generation
> stored no tile for alters nothing this bars."

Instantiate it. Planar layer, N = 2, channels (`a`, `b`), entry_count = 4.
Superseded generation stores tiles for `a` (ordinals 0, 1); `b`'s entries at
2, 3 are sentinels. The commit inserts channel `x` before `b`, giving
(`a`, `x`, `b`), entry_count 6. `a` keeps 0, 1. `x` takes 2, 3. **`b`'s two
entries move from ordinals {2, 3} to {4, 5}** — a renumbering caused by a
channel-declaration edit, not by a geometry change. Bar 2 expressly permits
this commit. The gloss, taken as written, says the re-emission rule does not
license the renumbering it requires.

So one of two things is wrong, and both are defects:

- if the gloss is right, step 4 forbids at 3117–3127 the very commit it permits
  at 3212–3215; or
- if the gloss is wrong — and the neighbour's words do not contain "only" —
  then bar 2's stated ground is a misreading of the rule it names, and the
  ground on which the whole second bar is justified does not exist.

The re-emission rule's own phrase "every other entry byte-identical at its
disk-ordinal position" is silent about *whose* ordinal — the superseded
generation's or the new one's — and the parenthetical was the only thing
resolving it. The repair added a renumbering cause the parenthetical does not
name and did not extend it.

The same unswept restatement appears non-normatively at §11.1's Rationale,
line 1622–1625: "Growth that changes entry_count changes extent_length with it
(`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and disk
ordinals renumber wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`)" —
again geometry only. That block is labelled **Rationale** so it carries no
force, but it confirms that geometry was the document's only contemplated
renumbering cause before this repair, and that the repair introduced a second
without touching either statement.

→ **A-01**.

### 7.2 The second one — a gloss in the wrong tense that over-bars

Inserted, 3204–3208:

> "A channel's tiles move exactly when its index does: reordering moves those
> channels the reorder re-indexes, and inserting or removing one moves every
> channel after the affected position. **Either is such a change wherever the
> layer stores a tile for a channel that moved.**"

"stores" — bare present. Every other statement of this rule in the passage
carries "in the generation this commit supersedes". Read in the new state's
tense, this sentence declares an edit barred whenever the *new* state stores a
tile for a moved channel.

Instantiate against the carve-out four lines later. Same planar layer,
(`a`, `b`), N = 2; superseded generation stores tiles for `a` only. The commit
inserts `x` before `b` **and stores a new tile for `b`** at its new ordinal 4.

- By the bar (3202–3204) and the carve-out (3212–3215): permitted. `b` is a
  channel "the superseded generation stored no tile for", so moving its
  ordinals "alters nothing this bars".
- By the gloss at 3208: the layer now *stores* a tile for `b`, and `b` moved,
  so "Either is such a change" — barred.

Two normative sentences, twelve lines apart, give opposite verdicts on the same
commit. Note the direction: this gloss **over**-bars. It is not the classic
"escape by unstoring" — it is its mirror, barring a commit for a tile the
commit itself creates.

A second, milder instance of the same slip sits at 3159–3161:

> "The §14 bar already reaches many changes to a channel's declared **sample
> type**: any that alters, **for a tile the layer stores**, what §14 fixes for
> its bytes or how they decode."

against the §14 bar's own "for any tile that layer stores **in the generation
this commit supersedes**", and against the bar's emphatic tense sentence at
3140–3144: "The tense is the prior generation's (§3.1 defines *stored* against
a generation), so a commit does not escape this by unstoring in the same
breath". Here the loose gloss reads as licensing exactly the escape the bar
forecloses. It has no operative consequence for sample types (bar 1 bars them
all outright), which is why I treat 3208 as the finding and 3160 as its second
location rather than filing two.

→ **A-02**.

### 7.3 Contradictions I looked for and did **not** find

- The permission at 3222–3225 ("MAY be re-declared freely") against the three
  MUST NOTs: no collision — the permission's antecedent is the exact complement
  of bar 1's, and the "these bars'" edit is the right sweep.
- The growth clause at 3226–3235 against `[R-SER-05]`: the added "for each
  channel the position carries" is `[R-SER-05]`'s own wording. No collision.
- The shrink paragraph's untouched "Neither of the two bars beside the §14 bar
  reaches a shrink: one bars a change to a channel's declared sample type, the
  other a change to a planar layer's channel declarations that moves a stored
  tile's disk ordinal, and a shrink is neither" (3257–3260): correct. A shrink
  changes Eᵢ, hence Gᵢ, N and s — so a shrink *does* move disk ordinals — but
  it is not a *channel-declaration* change, which is what bar 2 quantifies
  over. The sentence survives.
- §21.7 (3918–3925): already swept — "its two companion bars are witnessed not
  at all where the change leaves untouched everything §14 fixes for a tile the
  layer stores in the generation the commit supersedes … no check can know
  which ordinal a stored tile used to occupy, or which type its channel carried
  before". Correct tense, correct pair, and it independently confirms that
  neither new bar gets a register row. Consistent.
- §11.1's Rationale (1604–1626): already swept to three bars, tense correct,
  and non-normative anyway.
- §23.1's list of operations that make data unreachable (4176–4197): does not
  name a channel removal, but explicitly says "the list of operations above is
  not offered as closed". No sweep failure.
- §20.5 compaction (3422–3500): governs a compactor, which is not an appender
  and makes no declaration changes ("A compactor MUST preserve content"). Not
  affected.
- §20.3's Example (c) at 3341–3349: lists a fill change on a padding-free layer
  as directory-confined, and says a fill change on a layer storing a tile
  carrying a padding position "is not an appender's operation at all (step 4)".
  Consistent with the bars; a **sample type** change is not in that Example's
  list, but the Example enumerates directory-confined shapes rather than
  restating a bar, and it is labelled *Example* so it carries no force. Not
  reported.

---

## 8. Check 5 — every exhaustive word, tried against the document

| word/claim | location | falsification attempt | verdict |
|---|---|---|---|
| "already reaches **many** … does not reach **all** of them" | 3159–3162 | needs one type change §14 misses: int8→uint8 and float32→int32 both keep element size, decoded size, every offset, the shuffle stride, and the fill bytes | **holds** |
| "leaves **every** content rule §14 states over those bytes satisfied exactly as before" | 3163–3165 | content rules in §14 are `[R-SER-05]` (padding = fill), `[R-SER-03]` (pad bits = fill bit), `[R-SER-08]` (interleaved bool = 0x00/0x01). For int8↔uint8 and float32↔int32 fill bytes are unchanged and neither type is bool | **holds** |
| "the two coincide at P = 1" | 3170–3171 | P vs ⌈P/8⌉; P ≥ 1 since every Tᵢ ≥ 1 | **holds, and P = 1 is the only coincidence** |
| "**whatever** the layer's layout" | 3174–3175 | `[R-SER-06]` defines exactly two emittable layouts, 1 and 2 | **holds** |
| "every stored tile depends on **every** channel's type" (interleaved) | 3176–3179 | decoded size P·Q with Q = ΣBᵢ over all channels | **holds** — though the stated reason is partly wrong, see A-04 |
| "re-indexes nothing and moves **no** ordinal at all" (append / remove-last) | 3209–3210 | c and N both unchanged for every surviving channel | **holds** |
| "the channel count enters the addressed-tile count C · N … but **no** individual ordinal" | 3211–3212 | C is absent from c·N+s and from s | **holds** |
| "An interleaved layer is unaffected … **which no channel declaration enters**" | 3219–3220 | s = Σ tᵢ ∏_{j>i} Gⱼ, Gᵢ = ⌈Eᵢ/Tᵢ⌉ — dimension entries only | **holds** |
| "licenses a renumbering **only** for a geometry change" | 3200–3201 | the cited rule contains no "only" | **FAILS** → A-01 |
| "the §14 bar is **the whole of** the test of what a shrink **alters**" | 3237–3238 | this is the repair narrowing an earlier unrestricted "the whole of the test"; scoped to "alters", it is the §14 bar by construction | **holds** |
| "**the obligations this step states below** — on slack, on entry_count, and on a slab or alignment declaration" | 3239–3241 | step 4 below also states, at 3269–3273, "A writer SHOULD instead produce a new file wherever a commit would strand a large share of a layer's stored bytes — and always where it would re-emit every one of them" | **incomplete** → A-05 |
| "bind it **as they bind any commit**" | 3241 | `[R-SLB-04]` binds a commit that changes the stored-tile set / run partition / byte placement — a shrink does all three; `[R-SLB-01]` binds any layer with A declared | **holds** |

---

## 9. Check 6 — what the repair left unconstrained

**The structure bar 1 and bar 2 govern** is a planar or interleaved layer's
*ordered channel-declaration list*. §12's opening and §7.4's table fix exactly
what it carries:

per channel: **name** (u8 len + bytes), **sample type** (u16), **fill** (u8 len
+ bytes); at list level: **channel count C** (u16) and **declared order**.

Walking each member:

1. **sample type** — pinned outright by bar 1, for every channel of a layer
   that stored a tile. ✔
2. **declared order** — pinned by bar 2 on planar layers (via the ordinal), and
   by the §14 bar on interleaved layers (a reorder permutes every Fᶜ, so every
   sample's byte offset moves). ✔
3. **fill** — governed by the §14 bar only where the layer's stored tiles carry
   a padding position or a pad bit (`[R-SER-05]` fixes their content to fill).
   On a layer with no padding position it is freely changeable, and this is
   **deliberate**: §20.3's Example (c) names "changing a channel's fill value on
   a layer with no padding position and no pad bit" as a directory-confined
   commit. Not a gap. ✔
4. **name** — unpinned entirely; a channel rename disturbs no byte and no
   ordinal. Nothing in §14 or §11.4 reads a channel name. Benign. ✔
5. **channel count C, rising** — an append moves no ordinal (verified above),
   changes no interleaved Q only because an interleaved append *does* change Q
   and is therefore caught by the §14 bar. Planar append is permitted and
   harmless: entry_count rises to (C+1)·N, the new entries are new to the
   generation, existing entries keep their ordinals. ✔
6. **channel count C, falling** — **this is the gap.** Bar 2 asks only whether a
   *surviving* stored tile's ordinal moves, and answers "no" for removal of the
   last channel. Bar 1 asks only about type changes. But a removal also drops
   `N` addressed tiles out of the addressed set, and if the superseded
   generation stored tiles for the removed channel, **nothing in the passage
   says whether the §14 bar reaches that**. The only de-addressing carve-out in
   §20.3 is at 3243–3247, inside the shrink paragraph:

   > "Dropping a tile out of the addressed set (**§11.2's grid count falls**) is
   > not itself such an alteration — a tile the new state does not address
   > carries no §14 obligation and its extent becomes slack"

   Its parenthetical scopes the mechanism to a falling **grid count**, i.e. an
   extent shrink; a falling **channel count** drops tiles by a different
   mechanism (C·N falls with N fixed), and hunk 4's own edit tightened the
   paragraph's framing further to "the test of what a **shrink** alters". So the
   passage now discusses channel removal (3206, 3209) without ever saying
   whether removing a channel that stored tiles is permitted at all.

   This is precisely the shape the charter names: the repair pinned one quantity
   of the structure — the ordinal — and left the sibling quantity the same edit
   moves — the addressed-tile set — ungoverned. → **A-03**.

Adjacent layer-record fields I checked and found governed elsewhere, so not
gaps: **layout** (§14 bar catches every flip except the C = 1 no-ops analysed in
§4 above), **linearization** (`[R-GEO-05]` admits only value 1, so it cannot
change), **codec** and **filter** (named explicitly in the §14 bar's list),
**alignment A** and **slab S/A_slab** (`[R-SLB-01]`, `[R-SLB-04]`, both named
by hunk 4), **entry_count** and **crc_of_crc_array** (`[R-CNT-17]`,
`[R-CNT-23]`), **extents** (grow/shrink paragraphs), **tile extents**
(§14 bar via P).

---

## 10. Check 7 — analogies, verb against verb

Three places in the two hunks argue by pointing at another rule.

**(a)** 3220–3222: "Where this bars a change the operation is a new layer or a
whole-file rewrite, **exactly as above**."

- repair's verb: "bars a change" → "the operation **is** a new layer or a
  whole-file rewrite"
- cited text's verb (3155–3157): "Such a change **is** a new layer, or a
  whole-file rewrite under a fresh file_id (`[R-LIF-01]`, §20.5)"

Same verb, same consequent, and the antecedents range over the same kind of
thing (a commit the passage bars). **Analogy sound.**

**(b)** 3241: "the obligations this step states below … **bind it as they bind
any commit**."

- repair's verb: "bind it" (it = a shrink)
- `[R-SLB-04]`'s verb: "A writer or updater **whose commit changes** the
  stored-tile set, the run partition, or the byte placement of any run … MUST
  either re-establish … or clear"
- `[R-SLB-01]`'s verb: "When declared: **every stored tile's offset satisfies**
  offset mod A = 0"

Tested separately against each of the two cited rules, as the charter requires,
because one sentence carries the analogy for both:

- against `[R-SLB-04]`: a shrink de-addresses tiles, so the stored-tile set
  changes and the run partition changes (blocks are [c·N, (c+1)·N) and N falls);
  the rule binds on its own terms. **Sound.**
- against `[R-SLB-01]`: the surviving stored tiles keep their offsets, so the
  invariant is preserved rather than re-established; but the rule still "binds"
  in the sense that the new state must satisfy it, and step 4's own later
  sentence spells this out ("an aligned layer's stored tiles — every one the new
  state keeps, not only those this commit adds — satisfy its invariant or the
  declaration is cleared"). **Sound.**

Also tested "on slack" against `[R-CNT-21]` and "on entry_count" against
`[R-CNT-17]`: both bind any commit; `[R-CNT-17]` is a per-file cross-check, so
"as they bind any commit" is accurate. **Sound.**

**(c)** 3197–3201: "A further effect is barred **on the same tense**, though on
its own ground: … what it disturbs is instead the re-emission rule above, which
licenses a renumbering only for a geometry change."

- "on the same tense": repair's verb "**stores** … in the generation this commit
  supersedes" vs the §14 bar's "**stores in the generation this commit
  supersedes**". Identical. **Sound** — this half of the analogy passes.
- "on its own ground": repair's verb "**licenses** a renumbering only for a
  geometry change" vs the cited rule's verb "a geometry change **renumbers**
  ordinals wherever `[R-GEO-06]` moves them". "renumbers" is descriptive and
  existential; "licenses … only" is normative and exclusive. **Different
  quantifiers, different modality.** This is the failure. → A-01.

---

## 11. Check 8 — what the insertion did to the sentences around it

**Forward from hunk 3's insertion point (3157) to the end of the subsection.**
Every back-reference, with its pre- and post-insertion resolution:

| back-reference | line | resolved before | resolves now | changed? |
|---|---|---|---|---|
| "the tense is the bar's" → "the tense is **these bars'**" | 3224–3225 | the §14 bar | all three bars | **changed, and the repair changed it deliberately and correctly** |
| "**this permission**" | 3225 | "MAY be re-declared freely" | same | no |
| "**that cap**" | 3231 | `[R-COD-07]`'s lz4 cap | same | no |
| "**the bar above**" → "**the §14 bar**" | 3237 | the §14 bar (nearest preceding "bar") | the §14 bar, now named | **would have re-resolved to the ordinal bar; the repair pre-empted it by naming the bar. This is the single most valuable thing hunk 4 does.** |
| "in **the bar's own tense**" → "in **that bar's own tense**" | 3238 | the §14 bar | the §14 bar | no (same sweep) |
| "**this step**" | 3239 | step 4 | same | no |
| "bind **it**" | 3241 | — (new text) | a shrink | new; see note below |
| "such an alteration" | 3244 | "alters nothing §14 fixes" | same | no |
| "neither does **it** rescue" | 3247 | dropping a tile out of the addressed set | same | no |
| "**its** carve-out included" | 3252 | the §14 bar's | same | no |
| "the **two bars beside** the §14 bar" | 3257 | — | bars 1 and 2 | new text elsewhere; consistent |
| "**this** is precisely where the §14 bar has no witness" | 3262 | the permitted-shrink case | same | no |
| "exactly as **it** escapes the §14 bar" (§21.7, 3929) | | a commit that supersedes every tile | same | no |

**Nothing forward of the insertion silently re-resolved.** Hunk 4 is exactly the
sweep hunk 3's insertion required, and it made it. That is the check this
project has lost a round to, and this repair passes it.

One small note, not filed: within hunk 4's own new clause, "bind **it**" has
"a shrink" as its antecedent — the subject of the sentence's first clause,
separated from the pronoun by "the obligations this step states below", "slack",
"entry_count" and "a slab or alignment declaration (`[R-SLB-04]`,
`[R-SLB-01]`)". The nearest noun phrase is "a slab or alignment declaration",
which "as they bind any commit" immediately rules out. Recoverable; not a
defect.

**Backwards — does the inserted text lean on a distant antecedent?**

- "the re-emission rule above" (3199) reaches back roughly 75 lines to
  3117–3127, past the whole of the §14 bar, and competes for the reader's eye
  with §20.4, whose heading is literally "Re-emission and preservation". §20.4
  is *below*, so "above" disambiguates, but only just. This is soft; the hard
  defect in that clause is A-01, not the anaphor.
- "exactly as above" (3221–3222) reaches back to 3155–3157. Its own paragraph
  ends "which is a new layer or a whole-file rewrite" (3194–3195) with the same
  content, so both candidate antecedents say the same thing. Harmless.

---

## 12. Findings

### A-01 — bar 2's stated ground reads an "only" into the re-emission rule that is not there, and that "only" forbids what bar 2 permits

**Hunk 3. §20.3 step 4, lines 3199–3201, against 3117–3127 and 3212–3215.
Check: LOCAL_CONTRADICTION (with an OVERCLAIM face). Byte-level: yes.**

Detailed in §7.1 above. The repair says the re-emission rule "licenses a
renumbering only for a geometry change"; the rule contains no "only" and names
geometry only in a parenthetical aside. Bar 2 then expressly permits a
channel-declaration edit that renumbers the entries of channels the superseded
generation stored nothing for — a renumbering with a non-geometry cause. Under
the gloss that renumbering is unlicensed, so step 4 forbids at 3117 the commit
it permits at 3214.

**Byte-level.** Two writers, same input file: a planar layer, N = 2, channels
(`a`, `b`), `a` stored, `b` all-sentinel. Both are asked to insert channel `x`
before `b`. Writer A follows 3199–3201, finds no licence to renumber `b`'s
entries from ordinals {2,3} to {4,5}, and refuses the append — the caller must
take a whole-file rewrite under a fresh file_id. Writer B follows 3202–3215,
appends: new payloads (none), a six-entry index region, a re-emitted directory,
pad, trailer with the **same** file_id and a larger committed_file_length. The
file Writer B emits is conforming — entry_count = 6 = C·N satisfies
`[R-CNT-17]`, every entry is well-formed, the old regions are slack which
`[R-CNT-21]` leaves unconstrained — and Writer A cannot emit it, because
Writer A's only route produces a file with a *different* file_id and no
committed prefix from the input. The emittable set moves, and it moves on
bytes a reader can see (the trailer's file_id, the retained prefix).

**Repair.** Either extend the re-emission rule's parenthetical at 3126–3127 to
name the second cause — "(a geometry change, or a channel-declaration change on
a planar layer, renumbers ordinals wherever `[R-GEO-06]` moves them)" — and
then restate 3199–3201 as "which requires every carried-forward entry at its
new disk ordinal and names only a geometry change as a cause of one"; or drop
the "only" and rest bar 2 on its own MUST NOT without claiming a warrant the
neighbour does not give. The first is better: it also settles whether "its
disk-ordinal position" at 3125 means the superseded generation's ordinal or the
new one's, which the passage currently leaves open. §11.1's Rationale at
1622–1625 should be swept with it.

### A-02 — the ordinal bar's own gloss is stated in the wrong generation's tense, and over-bars a commit the carve-out permits

**Hunk 3. §20.3 step 4, line 3208 (and, as a second instance, 3160). Check:
TENSE_QUANTIFIER. Byte-level: yes.**

Detailed in §7.2 above. "Either is such a change wherever the layer **stores** a
tile for a channel that moved" carries no tense; every other statement of the
rule in the passage carries "in the generation this commit supersedes". Read in
the live state's tense it declares barred a commit that moves a channel's
ordinals *and* stores the first tile for that channel in the same breath —
which the carve-out at 3212–3215 expressly permits ("a commit that moves only
the ordinals of channels the superseded generation stored no tile for alters
nothing this bars").

**Byte-level.** Same planar layer as A-01, but the commit additionally stores a
tile for `b` at its new ordinal 4. Writer A reads 3208, sees the new state
storing a tile for a moved channel, and refuses. Writer B reads 3202–3204 and
3212–3215, sees that the superseded generation stored nothing for `b`, and
appends — one new payload, a six-entry index region, directory, pad, trailer
with the same file_id. The file is conforming; Writer A cannot emit it.

The second instance at 3159–3161 leans the other way — "any that alters, for a
tile the layer stores, what §14 fixes" describes the §14 bar's reach without its
tense, which reads as reopening the "unstore in the same breath" escape the bar
forecloses at 3140–3144. It has no operative consequence, because bar 1 bars
every sample-type change on such a layer outright; it is the same slip and
should be fixed in the same pass.

**Repair.** At 3208: "Either is such a change wherever the layer stored a tile
for a moved channel **in the generation this commit supersedes**." At 3160:
"for a tile the layer stores **in the generation this commit supersedes**".

### A-03 — the repair pins the ordinal a channel edit moves and leaves the addressed tiles the same edit drops ungoverned

**Hunk 3. §20.3 step 4, lines 3206–3210 and 3202–3204, against 3243–3247.
Check: UNDERSHOT (check 6). Byte-level: yes (plausible).**

Detailed in §9 above. Bar 2 tests only whether a surviving stored tile's ordinal
moves. A channel *removal* also drops N tiles out of the addressed set, and if
the superseded generation stored tiles for the removed channel the passage never
says whether that is barred. The §14 bar's only de-addressing carve-out —
"Dropping a tile out of the addressed set (**§11.2's grid count falls**) is not
itself such an alteration" — scopes its mechanism to a falling grid count, i.e.
an extent shrink, and hunk 4 tightened that paragraph's framing to "the test of
what a **shrink** alters". A falling channel count is a different mechanism with
no counterpart sentence.

The repair raises the case itself — "inserting or **removing** one moves every
channel after the affected position", "**removing the last**, re-indexes nothing
and moves no ordinal at all" — so a reader arrives at the question and finds no
answer.

**Byte-level.** Planar layer, channels (`a`, `b`), N = 2, both storing tiles.
The commit removes `b`. Bar 2: no ordinal moves. Bar 1: no type change.
Writer A applies the §14 bar to `b`'s two superseded-generation stored tiles —
after the commit they have no decoded size, no padding-position set, no
`[R-SER-05]` obligation, because they are not addressed — reads that as altering
what §14 fixed for them, and refuses. Writer B reads across the shrink
paragraph's general principle ("a tile the new state does not address carries no
§14 obligation and its extent becomes slack") and appends: entry_count falls
from 4 to 2, `b`'s payloads become slack, same file_id. Writer B's file is
conforming. Writer A cannot emit it.

Note the asymmetry that makes this reachable only on planar layers: an
interleaved channel removal changes Q and is caught by the §14 bar outright.

**Repair.** Add one sentence to the ordinal paragraph, on the model of 3243–3247:
"A channel removal drops the removed channel's addressed tiles out of the
addressed set; a tile the new state does not address carries no §14 obligation
and its extent becomes slack, exactly as on a shrink, and this bar reaches only
the ordinals of tiles the new state still addresses." Alternatively, widen
3243–3247's parenthetical from "(§11.2's grid count falls)" to "(the addressed
count C · N falls, by a grid count or by the channel count)".

### A-04 — "each in-sample offset Fᶜ" is not a sum over all channels

**Hunk 3. §20.3 step 4, lines 3176–3179. Check: CITATION. Byte-level: no.**

The passage: "In an interleaved layer every stored tile depends on **every**
channel's type, since the sample stride Q and each in-sample offset Fᶜ are sums
over all of them (§14.2)".

`[R-SER-02]`, §14.2: "Q = Σ Bᵢ over all channels (the **sample stride**), and
Fᶜ = Σ Bⱼ over **channels j < c** (channel c's in-sample offset)."

Q is a sum over all channels. Fᶜ is a sum over the channels *preceding* c: F₀ is
the empty sum, 0, and depends on no channel's type at all; F_c for c < C−1
depends on a proper subset. The conclusion the sentence draws survives anyway,
because Q alone makes P·Q — the interleaved decoded size — depend on every
channel's element size, and that is enough to justify the layer-level scope. But
the stated reason misdescribes the rule it cites, in normative text, and the
misdescription reads as verified because it carries a section reference.

**Not byte-level.** No verdict or emitted byte turns on it: bar 1 bars every
sample-type change on such a layer outright under both readings.

**Repair.** "since the sample stride Q is a sum over all of them and each
in-sample offset Fᶜ a sum over those before it (§14.2)".

### A-05 — hunk 4's list of "the obligations this step states below" omits the one that bears most directly on a shrink

**Hunk 4. §20.3 step 4, lines 3239–3241, against 3269–3273. Check: OVERCLAIM.
Byte-level: no.**

The repair: "the obligations this step states below — on slack, on entry_count,
and on a slab or alignment declaration (`[R-SLB-04]`, `[R-SLB-01]`) — bind it as
they bind any commit."

Step 4 also states, below, at 3269–3273: "A writer SHOULD instead produce a new
file wherever a commit would strand a large share of a layer's stored bytes —
and always where it would re-emit every one of them, which duplicates the layer
rather than dropping part of it."

That is a BCP 14 SHOULD, stated below, and a shrink is the paradigm operation it
addresses: a shrink strands the de-addressed tiles' payloads as slack, and a
large shrink strands a large share of them. The em-dash appositive reads as
naming all of the obligations in play, and a reader who takes it that way
concludes the SHOULD does not reach a shrink. Contrast the growth paragraph
three lines above, which explicitly disclaims closure: "the list is not offered
as exhaustive".

**Not byte-level.** A SHOULD does not move the emittable set; a writer that
ignores it is still conforming.

**Repair.** Either add "and the advice below on producing a new file instead",
or borrow the growth paragraph's disclaimer verbatim: "and the list is not
offered as exhaustive."

---

## 13. Candidates I opened and closed

- **"An interleaved layer is unaffected" might be wrong at some geometry.**
  Closed by deriving s from `[R-GEO-06]`: s = Σ tᵢ ∏_{j>i} Gⱼ with
  Gᵢ = ⌈Eᵢ/Tᵢ⌉ contains no channel-derived term at any geometry, degenerate or
  not.
- **A layout flip might escape all three bars and move an ordinal.** Closed:
  the flip changes the decoded size for every C ≥ 2 (P·Bᶜ vs P·Q with Q > Bᶜ),
  so the §14 bar catches it; at C = 1 the ordinals coincide (0·N+s = s) and, by
  §14.4's Note, so do the images for a numeric channel and for a bool channel at
  P = 1 with fill false — the flip is a no-op with nothing to bar.
- **A fill change on a layer that stores tiles might be an unpinned sibling of
  the sample type in the same channel entry.** Closed by §20.3's Example (c),
  which names "changing a channel's fill value on a layer with no padding
  position and no pad bit" as an intended directory-confined commit, and adds
  that a fill change on a layer storing a tile carrying either "is not an
  appender's operation at all (step 4)". Deliberate, and covered by the §14 bar
  through `[R-SER-05]`.
- **A channel rename might need pinning.** Closed: nothing in §11.4, §14 or §15
  reads a channel name; a rename moves no byte of any stored tile and no
  ordinal.
- **A rank change might slip past all three bars.** Closed as out of lane: it is
  not a channel-declaration change, so neither new bar was ever the place for
  it, and the §14 bar's treatment of it is not this repair's work. (I record
  that I looked: a rank change can hold P, the decoded size and every offset
  fixed while reassigning every coordinate to a different tile. If that is a
  gap, it is a gap in the §14 bar, and it predates these hunks.)
- **"a channel storing nothing still governs the tiles that do" is vacuous for
  an interleaved layer.** Genuinely odd — in an interleaved layer a channel
  never stores separately, so while the layer stores any tile no channel of it
  "stores nothing". But the sentence is a step in an argument whose conclusion
  ("the scope is the layer") is correct and is separately established by Q, and
  the following sentences make the planar case explicit. Not filed.
- **"these bars'" has no enumerated antecedent in §20.3.** Closed: the three
  MUST NOTs immediately above are the only candidates, and §11.1's Rationale
  independently says "its three bars". Loose, recoverable.
- **The permission and growth material now sit inside the ordinal paragraph
  rather than standing on their own.** Structural, not normative; the "these
  bars'" edit fixes the only thing that turned on the placement.
- **Hunk 4's "bind it" has three intervening noun phrases before its
  antecedent.** Closed: "as they bind any commit" rules out every nearer
  candidate.
- **The shrink paragraph might now need a geometry-validity clause to match the
  growth paragraph's.** Closed: a shrink cannot break `[R-GEO-01]` (Tᵢ and d
  unchanged, Eᵢ ≥ 0 is satisfied at 0 per `[R-GEO-02]`), cannot break
  `[R-COD-07]`'s cap (decoded sizes depend on Tᵢ and Bᶜ, not Eᵢ), and cannot
  break `[R-ENC-04]` (every product falls). The asymmetry with the growth
  paragraph is safe.

---

## 14. Where I would have found something and did not

- I derived every number in both hunks from `[R-GEO-06]`, `[R-GEO-03]`,
  `[R-SER-02]`, `[R-SER-03]` and §12.1's element-size table rather than reading
  them off the page, and cross-checked the ordinal formula against §11.4's own
  worked example (2·32 + 10 = 74). Every printed figure reproduced. If a stated
  number had been wrong I would have caught it.
- I ran the layout scoping at four degenerate geometries (C = 1, one tile,
  extent 1, addresses-but-stores-none) and at the two layout flips, in both
  directions. If bar 2's planar scoping had left an interleaved case exposed I
  would have found it there.
- I checked every one of the twelve identifier and section citations in the two
  hunks by opening the target and reading its text; one failed (A-04) and one
  informal citation failed (A-01).
- I enumerated the governed structure field by field from §7.4's table and §12's
  opening sentence, which is how A-03 surfaced.
- I listed every back-reference from the insertion point to the end of §20.3 and
  resolved each before and after. Hunk 4 is a correct sweep; nothing else
  re-resolved.

The one thing I could not settle from the specification alone is whether A-03's
ambiguity was intended to be resolved by the shrink paragraph's general
principle applying beyond shrinks. That is a maintainer's call, which is why I
marked it PLAUSIBLE rather than CONFIRMED.
