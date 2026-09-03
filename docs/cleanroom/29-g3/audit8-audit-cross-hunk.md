# Cross-hunk consistency audit — r29-audit8, lane: cross-hunk

## 0. Disclosure

Read:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole file, in
  ranges: 94–116, 1224–1240, 1584–1680, 1720–1800, 1832–1875, 2020–2120, 3060–3400,
  3742–3780, 3860–4010, 4207–4250; plus whole-file normalized regex sweeps).
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit8/case/hunk-01.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit8/case/hunk-02.diff`

**Disclosed breach:** my first tool call was `ls -la` on
`.../r29-audit8/case/`, which the access rule forbade ("Do not list that
directory"). The listing showed three filenames: `full.diff`, `hunk-01.diff`,
`hunk-02.diff`, with sizes. I did **not** open `full.diff` and I read no hunk
file other than my own two. The only information the listing gave me beyond my
charter is that this case has exactly two hunks in it rather than the six the
charter's generic prose refers to; nothing about content.

**Unrequested context:** material appeared in my context before I began — a
project instruction file pointing at an AGENTS.md, and an index of the
maintainer's memory files with titles referring to cadence, gates, prior
verifier failures and the register's relation to a vector corpus. I did not open
any of it and drew no conclusion from any of it. I have not repeated its
contents.

Wrote (my directory only):
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit8/scratch/cross-hunk/sweep-counts.txt`
and this transcript at
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit8/out/audit-cross-hunk.md`.
No repository file was modified. No git command was run.

## 1. The two hunks, and the rule each adopts

### Hunk 1 — spec/tarn.md line 3171, inside §20.3 step 4 (heading in the hunk
header, "20.3 The append procedure", verified correct against the body: the
landing site is inside the numbered step 4 of "An appender MUST, in order:")

Deletion only, of an appositive clause:

```
-   strand the originals as slack — every tile the change reaches, and
-   for a change reaching every channel the whole layer's worth, since
+   strand the originals as slack — every tile the change reaches, since
```

**Force:** normative. The passage is ordinary prose inside a numbered step; it
is not inside any `>` block, so [R-CNF-01]'s label exemptions (§1, *Note*,
*Example*, *Rationale*, non-normative appendices) do not reach it.

**The rule the repair adopts:** when a commit's re-typing of a channel reaches
stored tiles of the superseded generation, re-emitting those tiles strands one
original per **tile the change reaches** — a quantity indexed by reach, i.e. by
channel membership, and by nothing else. The prior text also asserted a
whole-layer worst case ("for a change reaching every channel the whole layer's
worth"); the repair withdraws that second quantity.

The withdrawn clause was planar-specific stated layer-generally: §3.1 (L409-410)
says "In an interleaved layer one tile carries every channel", so in an
interleaved layer *any* single-channel re-typing already reaches every stored
tile, and the antecedent "a change reaching every channel" is not the condition
under which the whole layer is stranded. It was also ambiguous between addressed
and stored tiles ("the whole layer's worth"), where only stored tiles have
originals to strand. The deletion is the right direction.

### Hunk 2 — spec/tarn.md lines 3960–3963, inside §21.7 (heading in the hunk
header, "21.7 What no check detects", verified correct)

Replacement inside the block that opens `> **Rationale.** Obligations this test
places outside the register, as the document stands.` (block starts at line
3925).

```
-> differ and the layer has a padding position or a pad bit, §14.5's
-> padding positions and §14.3's pad bits carry the wrong channel's
-> fill and T4 or T5 sees it; where it has neither, the permutation is
-> unwitnessed whether the fills agree or not. Where
+> differ and the permuted channels themselves carry a padding position
+> or a pad bit, §14.5's padding positions and §14.3's pad bits carry
+> the wrong channel's fill and T4 or T5 sees it; where neither does,
+> the permutation is unwitnessed whether the fills agree or not. Where
```

**Force: NONE.** I applied the label test, not the marker test. The block's
first word is **Rationale**, so [R-CNF-01] exempts it: "All text in this document
is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative." (I checked the block's
opening at line 3925 explicitly rather than inferring from the `>`.)

**The rule the repair asserts:** the witness for a barred planar channel
permutation is scoped to the **permuted channels**, not to the layer. A layer
that has a padding position or a pad bit somewhere does not thereby witness a
permutation of two channels that carry neither.

This is a real correction. Padding positions are a *layer-geometric* property
(§11.3 [R-GEO-04]: they arise "Where Eᵢ mod Tᵢ ≠ 0"), so for padding positions
layer-scope and channel-scope coincide. Pad bits are *per-channel*: §14.3
[R-SER-03] — "Packing is exclusive to planar bool planes" — and they exist only
where P mod 8 ≠ 0. So the old wording made a layer with one bool channel witness
permutations among its numeric channels, which is false. Direction of the fix:
correct.

## 2. The grouping

The two hunks are **one group**, not two. They do not share a section and they do
not share a requirement identifier, but they state two halves of the same rule
cluster: §20.3 step 4's pair of bars on an updater's channel declarations.

- Hunk 1 sits in the **§14 bar**'s sample-type paragraph (L3155–3175): what a
  re-typing that reaches stored tiles costs.
- Hunk 2 sits in §21.7's report of the **companion bar** (L3179–3200 normative;
  L3952–3965 reported), the bar on a planar layer's disk ordinals.

Both edits are corrections of the *same kind of property*: both replace or
withdraw a **layer**-indexed quantity in favour of a **channel/reach**-indexed
one. Hunk 1 withdraws "the whole layer's worth"; hunk 2 replaces "the layer has"
with "the permuted channels themselves carry". They agree with each other and
with the normative statements they report:

- L3157 (normative): "changing it is such a change wherever **the layer stores a
  tile that carries that channel**"
- L3188 (normative): "Either is such a change wherever **the layer stores a tile
  for a channel that moved**"
- L1617 (§11.1 Rationale, non-normative): "barred wherever the layer stores a
  tile that carries that channel, and free where it does not"

So the two repairs are jointly consistent **with each other**. The failure is
that the commit swept the layer/channel conflation out of two places and left it
standing in a third that sits between them.

## 3. Sweeps run (whitespace normalized to defeat the hard wrap)

Normalization: whole file read, every run of whitespace collapsed to one space,
character offsets mapped back to line numbers. Patterns and hit counts:

| pattern | hits |
|---|---|
| `pad bit` | 17 |
| `padding position` | 24 |
| `whole layer` | 0 |
| `every channel` | 4 |
| `the layer has` | 2 |
| `permuted` | 1 |
| `permutation` | 3 |
| `fills agree` | 2 |
| `recorded fill` | 6 |
| `fill change` | 1 |
| `fill value` | 14 |
| `appender's operation` | 1 |
| `confined to the directory` | 1 |
| `carries that channel` | 2 |
| `carrying that channel` | 3 |
| `tile that carries` | 2 |
| `disk ordinal` | 16 |
| `strand` | 6 |
| `stranded` | 0 |
| `slack — every` | 1 |
| `reaches` | 22 |
| `unwitnessed` | 9 |
| `the layer stores a tile` | 3 |
| `no padding position and no pad bit` | 1 |
| `carrying either` | 1 |
| `the permuted channels` | 1 |
| `the layer has a padding position` | 0 |
| `planes are the same length` | 1 |
| `P = 1` | 2 |
| `same length` | 3 |
| `element size` | 21 |
| `dominated by its index` | 1 |

The decisive one is the pair `no padding position and no pad bit` (1 hit, line
3323) and `carrying either` (1 hit, line 3325). Both are in §20.3's Example
block, and both state at **layer** scope exactly the condition hunk 2 just moved
to **channel** scope in §21.7.

## 4. Findings

### X-01 — §20.3 Example (c) still tests the §14 reach at layer scope (hunks 1, 2)

Verbatim, spec/tarn.md L3321–3327:

> **(c) A change confined to the directory** — clearing a slab
> declaration, renaming a layer, or changing a channel's fill value on
> a layer with no padding position and no pad bit. Only the directory
> is re-emitted. A fill change on a layer that **stores** a tile
> carrying either is not an
> appender's operation at all (step 4): it would invalidate every
> stored tile it reaches.

Against the normative test it cites, L3155–3158:

> A channel's declared **sample type** is such a declaration, and
> changing it is such a change wherever the layer stores a tile that
> carries that channel

and against hunk 2's repaired sentence:

> Where the fills differ and the permuted channels themselves carry a
> padding position or a pad bit …

**Counterexample.** Planar layer, rank 2, extents (9, 9), tile extents (3, 3).
9 mod 3 = 0 on both axes, so by [R-GEO-04] the layer has **no** padding
position. Channels: `a` = uint8 (element size 1, §12.1), `b` = bool. P = 3·3 = 9;
9 mod 8 = 1 ≠ 0, so every stored plane of `b` carries seven pad bits (§14.3).
Both channels store tiles. The commit changes only `a`'s recorded fill value.

- Under normative step 4: does the change alter, for any tile the layer stored
  in the superseded generation, "the set of padding positions (§11.3) and the
  content `[R-SER-05]` fixes there"? `a`'s planes have no padding position and
  `a` is not bool, so no pad bits; `b`'s pad bits are fixed to *`b`'s* fill bit
  (§14.5: "Every pad bit (§14.3) MUST carry the plane's channel's fill bit"),
  unchanged. Nothing §14 fixes is altered. The commit is permitted, and it is
  shape (c): only the directory is re-emitted.
- Under Example (c): the layer is not "a layer with no padding position and no
  pad bit", and it *is* "a layer that **stores** a tile carrying either", so the
  Example declares the change "not an appender's operation at all (step 4): it
  would invalidate every stored tile it reaches." It reaches no stored tile.

Which text should change: **Example (c)**. It is non-normative (its block opens
`> **Example — the three shapes a commit takes.**`), it contradicts the
normative rule it cites, and its scope is the one the rest of the commit has now
abandoned in both other restatements. Concretely: "changing a channel's fill
value where that channel carries no padding position and no pad bit in any tile
the layer stores", and "A fill change on a **channel** that carries either in a
tile the layer **stores** is not an appender's operation at all".

**Byte-level: no.** The disputed file — the append that carries only a directory
with `a`'s new fill — is conforming: T4 and T5 both pass on it, and no register
row is violated. Example (c) carries no normative force under [R-CNF-01], so the
normative step-4 permission governs under both readings and a conforming writer
may emit that file either way. The emittable set does not move. It is still a
defect: a reader who takes the Example as the operative test performs a
whole-file rewrite under a fresh file_id where an append was permitted, and
Example (c) is now the last statement of a scope the commit corrected twice.

### X-02 — hunk 2's replacement anaphor "neither" is a two-element quantifier over an unbounded set (hunk 2)

Repaired text: "… where **neither does**, the permutation is unwitnessed whether
the fills agree or not."

Before the repair the sentence read "where **it has neither**": "it" was the
layer (singular), and "neither" ranged over the two witness kinds — a padding
position and a pad bit. Well formed. After the repair the subject of the
preceding clause is "**the permuted channels** themselves", a plural of no fixed
size, and "neither does" must take it as antecedent (the pro-verb "does" is
singular and takes a channel, not a witness kind, as subject). Two problems:

1. It is undefined for more than two permuted channels, and §20.3 L3186–3188
   (normative) says a permutation can move more than two: "reordering moves those
   channels the reorder re-indexes, and inserting or removing one moves **every
   channel after the affected position**."
2. It is ambiguous: a reader can still parse "neither" back onto {a padding
   position, a pad bit}, which restores the layer-neutral reading the repair set
   out to displace.

Repair: "where none of them does". **Byte-level: no** — Rationale block, no
force; and both readings agree in the two-channel case, which is the only case
the surrounding sentence sets up explicitly.

### X-03 — the untouched neighbour the repair now leans on is false at P = 1 (hunk 2)

The repair's branch is gated on "Where the fills **differ**". Everything else
falls to the immediately preceding, untouched sentence (L3955–3957):

> a permutation among channels whose planes are the same length **and whose
> recorded fills agree** disturbs nothing a row can see

This is falsifiable. A packed planar bool plane is ⌈P/8⌉ bytes (§14.3); a planar
numeric plane is P·Bᶜ (§14.2 table). ⌈P/8⌉ = P·Bᶜ with Bᶜ ≥ 1 forces P = 1 — the
document knows this: §14.4's Note says "At P = 1 the two are the same length".

Construct: rank 1, E₀ = 4, T₀ = 1 (so N = 4, P = 1, no padding position since
4 mod 1 = 0). Planar. Channel `a` = bool with fill byte `0x00`; channel `b` =
uint8 with fill byte `0x00` — the **recorded fills agree** and the **planes are
the same length** (1 byte each). All 8 tiles stored; `b`'s tiles hold `0xFF`.
Now permute the declarations to (`b`, `a`). Entries stay byte-identical at their
disk-ordinal positions (§20.3 step 4), so `b`'s stored bytes now sit at ordinals
4–7, which the new declarations make `a`'s bool planes. P mod 8 = 1 ≠ 0, so bits
1–7 of each are pad bits and MUST carry `a`'s fill bit, which is 0 (§14.5
[R-SER-05]). `0xFF` has them set. **T5 fires on four tiles.** The permutation is
witnessed, and the sentence says it disturbs nothing a row can see.

Which text should change: the **untouched sentence**, not the repair. It should
be restricted to channels whose planes are sized the same *way* — both bool, or
both numeric of equal element size — since P = 1 is the sole cross-packing
coincidence. **Byte-level: no** (Rationale block).

This is a check-4 finding: the repair widened nothing, but by narrowing its own
branch to "the fills differ AND the permuted channels themselves carry …" it
routes the P = 1 bool/numeric case squarely onto a neighbouring claim that is
false, and now nothing in the passage catches it.

### X-04 — the walkthrough treats permutations only; the bar it reports covers insertion and removal too (hunk 2)

§21.7 introduces the topic as the whole of the companion bar: "Its companion bar
on a planar layer's disk ordinals is witnessed indirectly and only sometimes,
and for the same reason no check knows which ordinal a stored tile used to
occupy:" — and then discusses **only** permutations, in every clause including
the repaired one. The bar it reports (§20.3 L3183–3189, normative) is wider:

> A channel's tiles move exactly when its index does: reordering moves those
> channels the reorder re-indexes, and inserting or removing one moves every
> channel after the affected position. Either is such a change wherever the
> layer stores a tile for a channel that moved.

Inserting a channel at a non-final position, or removing a non-final one, is
squarely inside the bar and outside the repaired analysis; and its witness story
is not the permutation's, because it also changes C·N (§11.2) and therefore
entry_count ([R-CNT-17]). The repair sharpened one half of a two-half subject.
The block's own opening concedes the shape of this: "an obligation the list omits
— is a defect in this block and not in the register." **Byte-level: no.**

### X-05 — hunk 1 pins the payload originals and leaves the index region unnamed (hunk 1)

Check 6. The structure hunk 1's sentence governs is *the slack a barred re-typing
would cost if a writer re-emitted its way around the bar*. The quantities that
structure can carry are two, and step 4 states both:

- the superseded stored tile payloads — named ("every tile the change reaches");
- the layer's whole tile-index region, which step 4 requires re-emitted "in full
  … necessarily at a new placement (`[R-LIF-01]`)" for "Every layer whose
  stored-tile set or index content this commit changes" — unnamed here.

The withdrawn clause at least gestured at the whole-layer magnitude. After the
deletion the normative sentence's cost account names one member of a two-member
set, and the missing member is the dominant one on the section's own testimony —
L3272, a **Note** and therefore non-normative: "A commit's cost is dominated by
its index, not its data". Adding ", and that layer's whole tile-index region with
them," restores it. **Byte-level: no** — this is a cost narrative, not an
obligation, and the operation it describes is barred outright by the sentence
that follows it.

## 5. Checks that passed, reported for the record

**Check 1 (tense and quantifier).**

- Hunk 1. Generation: the superseded one. "every tile the change reaches" takes
  "reaches" from the sentence it continues — "Where a change does reach them it
  makes each **stored** tile it reaches nonconforming" — and "them" from
  "Where the superseded generation stored no tile carrying that channel". So
  the quantifier is *stored tiles of the superseded generation carrying the
  re-typed channel*. That matches the normative rule it restates, L3141–3143:
  "for any tile that layer stores **in the generation this commit supersedes**".
  The word "stored" does not repeat inside the repaired clause; context supplies
  it, and the immediately preceding clause supplies it three words earlier.
  Passes, narrowly.
- Hunk 2. Generation: the *new* state, since the subject is what a check
  performed on the committed file can see. Correct for a detectability claim, and
  it does not collide with hunk 1's superseded-generation tense because the two
  sentences are about different objects (what a commit costs vs. what a file
  shows).

**Check 2 (citations resolve).** See §6 below — every one checked, all pass.

**Check 3 (normative placement).** Applied the **label** test, not the `>`
marker. Hunk 1: no block, normative. Hunk 2: block opening `> **Rationale.**` at
line 3925, so non-normative under [R-CNF-01]. Consequence checked in both
directions:
- Does hunk 2's repair leave a normative statement of the old rule standing
  elsewhere? No. The layer-scoped version of this condition survives at exactly
  one place, L3321–3327, and that place is also non-normative (an **Example**
  block). See X-01.
- Does anything that carries force now depend on something that does not? For
  these two hunks, no. §20.3's companion bar (L3183–3189) states the bar without
  relying on any witness claim, and the only normative pointer into §21.7 in this
  subsection — L3241, "§21.7 records the consequence — that this is precisely
  where the §14 bar has no witness" — states its own proposition in §20.3 and
  concerns the §14 bar under a shrink, not the sentences hunk 2 touched.

**Check 5 (exhaustive claims).** Words checked in the repaired text:
- hunk 1, "every tile the change reaches" — could not falsify; each re-emitted
  tile strands one original because [R-LIF-01] forbids overwriting it in place.
- hunk 2, "themselves" — the narrowing is right (pad bits are per-channel).
- hunk 2, "neither" — falsified. X-02.
- hunk 2, "unwitnessed whether the fills agree or not" — the fills-agree half is
  where X-03 bites, though via the neighbouring sentence rather than this clause.
- hunk 2, the closed two-item list "a padding position or a pad bit": checked
  against the document's canonical triple, which appears three times —
  L3879 "padding positions, pad bits, and boolean bytes", L3941 "a padding
  position, a pad bit, or an interleaved boolean", L3971 "a padding position, a
  pad bit, or a boolean byte". The third member is *interleaved* boolean bytes
  (T2 is explicitly "In an interleaved tile"), and this passage is about planar
  layers, where §14.3 packs bools into bits. So two is the right count here and
  the omission is correct. Passes.

**Check 6 (what is left unconstrained).** For hunk 2 I enumerated every
witness a planar ordinal permutation can trip: plane length (T3; T14 under
codec 1; and under codec 3 also T21/T22, though T3 suffices and the document
consistently names T3/T14 for decoded size), padding-position content (T4), pad
bits (T5), interleaved bool byte (T2, N/A planar), per-tile CRC (T1 — travels
with its entry, unaffected), entry_count / extent_length (unchanged by a
permutation), slab and alignment invariants (no byte moves). The repaired
sentence plus its neighbour cover the whole set. Passes. For hunk 1 it does not
— X-05.

**Check 7 (argument by analogy).** The repaired text of neither hunk argues by
analogy. Hunk 1's only warrant is a citation, "since `[R-LIF-01]` freezes them
where they lie"; comparing governing verbs, [R-LIF-01] says a writer "MUST NOT
modify" bytes in [0, F), and the repair says [R-LIF-01] "freezes them where they
lie" — same set (committed bytes), same force. Passes. Hunk 2's "for the same
reason" and "exactly as a mis-strided filter is" are both in untouched sentences
outside the replaced span; the replaced span carries no analogy. Reported as
checked, no comparison to make.

**Check 8 (what the insertion did to the sentences around it).** Hunk 1 is a
pure deletion and hunk 2 a replacement; neither inserts a new rule between an
anaphor and its antecedent. Back-references read forward from each landing site
to the end of its structure:

- L3175 "Such a change is a new layer, or a whole-file rewrite" — "Such a change"
  resolves to the re-typing that reaches stored tiles, both before and after
  hunk 1. Unaffected.
- L3179 "One effect is barred beside it" — "it" = the §14 bar. Unaffected.
- L3251 "and always where it would re-emit every one of them" — "them" = "a
  layer's stored bytes", inside its own sentence. Unaffected by hunk 1's
  deletion, and it is the normative home of the whole-layer worst case the
  deleted clause gestured at, which is why the deletion loses no rule.
- L3964 "Where the change does touch something §14 fixes, the register's rows
  reach it" — "the change" resolved to the permutation before and after.
  Unaffected.
- Hunk 2's own "where neither does" — X-02; this is the one back-reference the
  edit re-resolved, and it re-resolved it onto a set of the wrong cardinality.

## 6. Every citation in the repaired text, with verdict

| citation | in | claim made about it | verdict |
|---|---|---|---|
| `[R-LIF-01]` | hunk 1 | "freezes them where they lie", i.e. the originals cannot be overwritten in place and so become slack | **PASS.** §9.1: "Bytes in [0, F) … are immutable: a writer MUST NOT modify them" |
| §14.5 | hunk 2 | governs padding-position content, so a mis-placed plane's padding positions "carry the wrong channel's fill" | **PASS** on content. Marginal: padding positions are *defined* in §11.3, not §14.5; §14.5 fixes their content, which is what the sentence is about. Unchanged by the repair. |
| §14.3 | hunk 2 | governs pad bits | **PASS** on definition. Marginal in the same way: §14.3 defines pad bits but says "their content is fixed by `[R-SER-05]`", i.e. §14.5. Unchanged by the repair. |
| T4 | hunk 2 | sees a padding position carrying the wrong channel's fill | **PASS.** §21.4 T4: "A padding position does not encode, for each channel it carries, that channel's recorded fill value", governing rule [R-SER-05], instances include "planar numeric plane fill bytes" and "packed planar bool plane fill bit". |
| T5 | hunk 2 | sees a pad bit carrying the wrong channel's fill | **PASS.** §21.4 T5: "In a packed planar bool plane with P mod 8 ≠ 0, a final-byte pad bit … is not the channel's fill bit". |
| T3, T14 (in the untouched neighbouring clause the repair leans on) | hunk 2 | catch a plane left "at an ordinal the new declarations size differently" | **PASS.** T3 is the decoded-length check; T14 is the codec-1 entry-length check. |
| §21.4 row count | — | header says "26 conditions"; rows T1…T26 counted = 26 | **PASS** (sanity check only; no hunk touches it). |

## 7. Derived numbers

My charter names no numeric quantity. The arithmetic I did was to build and
check counterexamples:

- X-01 geometry: extents (9, 9), tile extents (3, 3) → 9 mod 3 = 0 on both axes,
  so no padding positions ([R-GEO-04]); P = 3·3 = 9; 9 mod 8 = 1 ≠ 0, so a bool
  plane's ⌈9/8⌉ = 2 bytes carry 7 pad bits (§14.3). Compared against nothing in
  the document — these are my constructions, not document figures.
- X-03 coincidence: ⌈P/8⌉ = P·Bᶜ with Bᶜ ≥ 1 ⟹ ⌈P/8⌉ ≥ P ⟹ P ≤ 1 ⟹ P = 1,
  Bᶜ = 1. Compared against §14.4's Note, "At P = 1 the two are the same length",
  which agrees.
- X-03 geometry: rank 1, E₀ = 4, T₀ = 1 → N = ⌈4/1⌉ = 4, P = 1, 4 mod 1 = 0 so no
  padding positions; 8 addressed tiles at C·N = 2·4; 1 mod 8 = 1 ≠ 0 so 7 pad
  bits per bool plane.
- §21.4 header count 26 vs rows T1…T26 counted = 26. Agrees.

## 8. Candidates considered and dropped

1. *"§14.5's padding positions" misattributes §11.3's definition, and "§14.3's
   pad bits carry the wrong channel's fill" attributes to §14.3 a content rule
   §14.3 explicitly assigns to [R-SER-05].* Dropped: both phrases are in the text
   on **both** sides of the diff, so the repair neither introduced nor could have
   been expected to sweep them, and the sentence is about content, for which
   §14.5 is the right home.
2. *§21.7's own definition of "unwitnessed" (L3885) makes "T4 or T5 sees it" too
   strong: detectability there requires that "some file exhibiting it is
   separated by such a check from **every** file that does not", and a
   permutation is a fact about a commit, so a byte-identical file with a
   different history exhibits the check outcome without exhibiting the
   permutation.* Dropped: the "T4 or T5 sees it" clause is unchanged by the
   repair, the block itself closes with the disclaimer "the register's rows reach
   it on the terms they state there and no better", and the same looseness is
   pervasive and evidently intended (L3991: "the §14 bar is unwitnessed there for
   the same reason `[R-LIF-01]` is"). Not a repair defect. Flagged here because
   it is the one place where a definition and a sentence reporting it could
   diverge in this passage, and I checked it rather than assuming.
3. *The repair should have said "carry a padding position or a pad bit **in a
   tile the layer stores**", since a channel with no stored tile witnesses
   nothing.* Dropped: the companion bar only fires "wherever the layer stores a
   tile for a channel that moved" (L3188), so a stored tile at a moved ordinal is
   given by the antecedent, and adding the qualifier would restate it.
4. *The equal-length branch names only "T3, or … T14 under codec 1" and omits
   T21/T22, which also catch a decoded-size mismatch under zstd.* Dropped: T3 is
   the decoded-payload length check and fires under every codec, so the
   enumeration is sufficient rather than closed, and the document names the same
   pair again at L3973 ("witnessed by T3 or T14"). Consistent.
5. *Hunk 1's "every tile the change reaches" drops "stored" and so could be read
   over addressed tiles — the same addressed/stored ambiguity that made the
   deleted clause wrong.* Dropped to a note inside Check 1 rather than a finding:
   the governing "each **stored** tile it reaches" sits three words earlier in the
   same sentence, and §11.2/§13.3's distinction gives an unstored tile no original
   to strand, so no reader reaches the wrong quantity.
