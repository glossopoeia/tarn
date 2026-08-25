# Audit — downstream accounts (charter: look OUTSIDE the three hunks)

> *Editorial substitution for the repository's vocabulary gate: an ordinary-English
> use of a gate word has been replaced with an exact synonym. The substitution is
> recorded here and changes no finding, quotation or verdict.*

Role: repair auditor, "what elsewhere depended on what those passages used to say".
Hunks: hunk-01 (§11.1 Rationale), hunk-02 (§13.3 Note), hunk-03 (§16.2 [R-SLB-03] prose).

## 0. Disclosure

Read, in full or in the passages named:
- `/private/tmp/.../case-adr0099/hunk-01.diff`, `hunk-02.diff`, `hunk-03.diff` (my charter's three).
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — sections read in full:
  §7.4 (995–1110), §9.7 (1322–1372), §11.1–§11.4 (1460–1600), §13.3 (1748–1800),
  §15 (1991–2116), §16 (2116–2225), §17.2 codec 3/4 (2290–2365), §19.3–§19.4 head
  (2794–2840), §20.1–§20.3 (2899–3155), §21.1 (3341–3420), §21.6–§21.9 (3600–3820),
  §24 (4010–4095), Appendix A (4097–4145), Appendix B (4145–4180), Appendix G
  (4271–4410), Appendix H (4411–4482), §5.2 preamble block (585–618), §3.1 glossary
  fragments (312–325).
- Register rows read individually: L21, L22, L23, L24, L27, L28, L29, L39, L40, L41,
  L42, L44, T3, T5, T14, and §21.2/§21.3/§21.4 header lines around them (3475–3565).

Ran: `wc -l`, `sed -n` on spec/tarn.md, `grep -n "R-SLB"` on spec/tarn.md, and a local
python3 script of my own (`/private/tmp/.../scratchpad/work/s.py`) that flattens
spec/tarn.md to a single whitespace-normalised string with a char→line map, so that
hard-wrapped phrases match. Every "grep" below is that script. No other file was read.
I did NOT read full.diff, other hunk files, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, registry.json, git history, or the web. I did not
list the case directory.

**Unrequested context appeared before I began**: a project instruction file pointer
(CLAUDE.md → AGENTS.md) and an index of the maintainer's memory notes, including
entries whose titles referred to spec-edit propagation and to the §21 register.
I did not open any of them and I did not read past the titles that were placed in
context. I disclose that they appeared. Nothing below rests on them; every conclusion
below is anchored to a quotation from spec/tarn.md that I print.

## 1. The rule each repair adopts, in my own words

**Hunk 1 (§11.1 Rationale, lines 1493–1503).** Adopts: for a commit that only grows a
layer's extents, the *named header quantity* `entry_count` is the sole discriminator of
cost. If the growth leaves `entry_count` at its prior value, nothing but the layer
record (hence the directory) is re-emitted. If it changes `entry_count`, then
`extent_length` changes too, so the whole tile-index region is re-emitted at a new
placement and disk ordinals renumber. It further asserts that a growth CAN raise one
grid count and still leave `entry_count` alone — when another grid count is 0, holding
the product at 0 — and that the growth which ends that state is the one raising the
*last* remaining zero grid count.

Old formulation (superseded): keyed on "every grid count ⌈Eᵢ/Tᵢ⌉ unchanged", with an
**exception** clause "save where another dimension's grid count is 0, which holds the
product at 0 and adds no entry", and a tail "the first growth of a zero-extent layer
included."

**Hunk 2 (§13.3 Note, lines 1788–1794).** Adopts: the re-emission trigger for a
declare-then-fill workflow is (a) a change to the layer's stored-tile set, or (b) a
growth of extents that changes `entry_count`. Replaces (b)'s old form, "grows its
extents across a grid boundary".

**Hunk 3 (§16.2, [R-SLB-03], line 2158).** Adopts: inside a slab run the packing
relation is `offset(k) = offset(k−1) + length(k−1)` — the *previous* stored tile's
length, not the current one's. It makes true of an implementation: a verifier computes
each stored tile's expected offset by accumulating the lengths of the stored tiles
before it in the run.

## 2. The seven checks

### Check 1 — tense and quantifier

**Hunk 1.** Generation: the block is about what a commit does, and it speaks of the
*new* state's `entry_count` against the *superseded* state's ("Growth that leaves
entry_count unchanged", "Growth that changes entry_count"). That is the correct pairing
for a cost claim. The surrounding shrink half of the same Rationale is explicitly in the
superseded generation's tense ("a tile the superseded generation did not store"), and
§20.3 fixes that tense normatively ("any tile the layer stores **in the generation this
commit supersedes**"). No tense collision.
Set: `entry_count` is a single per-layer scalar, so there is no set to range over — this
is exactly why re-keying onto a named header quantity is the right move. §7.4 makes it
a `u64` field: "| entry_count | u64 | equals the addressed-tile count (§11.2,
`[R-CNT-17]`) |".
The normative rule this restates is §20.3 step 4 ([R-WRT-04]):
"Every layer whose stored-tile set or index content this commit changes has its
tile-index region re-emitted in full — entry_count entries plus the segment CRC array —
necessarily at a new placement (`[R-LIF-01]`)". Quantifier "every layer whose … this
commit changes" vs the repair's "Growth that changes entry_count" — the repair's
antecedent is a proper subset of the normative one (index content also changes without
`entry_count` changing, e.g. superseding a stored tile). A Rationale narrower than its
rule is sound; it does not license anything the rule forbids. PASS.

I verified the arithmetic behind the repair's central claim myself. Under growth,
every Eᵢ is non-decreasing, so every Gᵢ = ⌈Eᵢ/Tᵢ⌉ is non-decreasing, so N = ∏Gᵢ is
non-decreasing. `entry_count` = N (interleaved) or C·N (planar) — §11.2 — and C is not
a geometry field, so growth cannot change it. Therefore, under growth:
`entry_count` unchanged ⟺ (every Gᵢ unchanged) OR (N = 0 before and after, i.e. some
Gᵢ = 0 in both states). The repair's two clauses cover exactly that disjunction; the
old text covered the same set through its exception clause. The **covered set did not
move**; what moved is the tail ("first growth" → "last zero grid count").

**Hunk 2.** "each commit that changes a layer's stored-tile set, or that grows its
extents so that entry_count changes, re-emits that layer's whole tile-index region".
Subject is the commit, object "that layer's" — so the per-layer quantifier is carried
implicitly and correctly. Against §20.3's "stored-tile set or index content this commit
changes": the first disjunct matches word for word; the second is a proper subset of
"index content … changes". Narrower, not wrong. PASS.
Noted but not reported: the Note still omits a **shrink** that changes `entry_count`
without changing the stored-tile set (§20.3: "`[R-CNT-17]` obliges the smaller
entry_count and so a re-emitted index region"). That omission predates the repair and
the Note's declared subject is declare-then-fill growth ("Declare-then-fill workflows
append tiles as data arrives"), so I do not count it a defect.

**Hunk 3.** Ranges over "every run" and, inside a run, over each stored tile with an
ordinally-preceding one. Tense is atemporal (a state invariant on the live generation). The
disambiguation removes a quantifier ambiguity rather than creating one. PASS.

### Check 2 — citations resolve

| Cited in repair | Opened at | Verdict |
|---|---|---|
| §11.2 (hunk 1, "grid count ⌈Eᵢ/Tᵢ⌉") | 1505–1518 | PASS. "the **grid count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉". |
| `[R-CNT-17]` (hunk 1, "changes extent_length with it") | 1039–1044 | PASS with a noted qualifier. Text: "Under index_encoding 1, extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0)". The map is strictly increasing in entry_count, so a change in one forces a change in the other. The repair drops the "Under index_encoding 1" qualifier; harmless, because §7.4's table makes every other index_encoding value "a validity error at layer scope", so index_encoding is 1 in every conforming layer. |
| `[R-GEO-06]` (hunk 1, "disk ordinals renumber wherever [R-GEO-06] moves them") | 1563–1577 | PASS. "the **spatial tile ordinal** … is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" and "**disk tile ordinal** … s for an interleaved layer, and **c · N + s** for a planar layer". Both are functions of the Gⱼ and N, so a grid-count change does renumber. |
| §20.3 (hunks 1 and 2) | 2941–3084 | PASS. Step 4 states the re-emission obligation. |
| `[R-WRT-04]` (hunks 1 and 2) | 3084 | PASS. That identifier closes §20.3's numbered procedure, so it is the rule that carries step 4. |
| §11.1 (hunk 2) | 1466–1503 | PASS — §11.1 is where the growth/entry_count account now lives. |
| `[R-IDX-05]` (hunk 2, context, untouched) | 2100–2107 | PASS. "The CRC-32C of a segment consisting of 2¹⁶ sentinel entries is `0xEECB3BB2`". |
| `[R-SLB-02]`, `[R-SLB-05]`, §5.2, §15.3 (hunk 3 surrounds) | 2146–2155, 2116–2127, 618ff, 2036–2068 | PASS, all unchanged by the repair and all consistent with the disambiguated packing relation. |

No citation in any of the three repairs points at a rule that merely almost says the
claimed thing.

### Check 3 — does the repair sit in normative text?

Hunks 1 and 2 are both inside ">" blocks and therefore carry no force ([R-CNF-01]).
That is correct here, because neither is the statement of a rule: the rule is §20.3
step 4 / [R-WRT-04], which is plain prose and was not touched. I checked that the
normative statement does not still say the old thing: grep for the old key phrase
`grid boundary` over the whole flattened document returns **zero hits**, and grep for
`grid count` returns hits only at lines 403, 1064, 1475, 1479, 1497 (the repair), 1507,
1563, 3044 — none of which is a normative re-emission trigger. §20.3 step 4 keys on
"stored-tile set or index content", never on grid counts, so there was no old normative
statement to leave standing. PASS for both.

Hunk 3 IS normative — it is the body of [R-SLB-03], plain prose, not a ">" block. PASS.

### Check 4 — no contradiction in the same passage, including untouched text

**§11.1's Rationale, read whole (1483–1503).** Its shrink half ends "A layer that stored
nothing may be re-declared freely." — which mirrors §20.3's "A layer that stores no tile
**in the generation this commit supersedes** MAY be re-declared freely". No collision
with the growth half. No MUST anywhere in the block (it is a Rationale). No carve-out in
the block that the repair's new breadth collides with — the repair's breadth is
identical to the old text's, as shown in check 1.

**§13.3, read whole (1748–1794).** [R-TYP-08] and [R-TYP-09] are read-path rules; the
repaired Note is about writer/commit cost. No collision. The two intervening Notes
(fill vs padding, the Rationale about corruption) are untouched and unaffected.

**§16.2, read whole (2146–2218).** The repaired sentence is followed by, and must live
with: "Sentinel tiles are transparent to run continuity: they occupy no bytes and do not
break packing", "So are the entries §15.3 classifies reject-tile on a *structural*
ground", and the carve-out "An entry whose only defect is that its stored bytes fail its
crc is not transparent — its offset and length stand, and the packing relation reads
them as it does any other stored tile's". Under the disambiguated reading
(offset(k) = offset(k−1) + length(k−1)) every one of these reads correctly: a
transparent entry drops out of the sequence of "stored tiles", and a crc-failing entry
stays in it with its own length feeding the next tile's offset. Under the OLD ambiguous
reading ("plus its length", the current tile's) the crc carve-out would have been
incoherent, because the relation would not have read the *previous* tile's length at
all. So the repair removes a latent contradiction rather than creating one. PASS.

### Check 5 — exhaustive claims

Hunk 1: "touches the directory alone" (a completeness claim). I tried to falsify it.
Growth leaving `entry_count` unchanged: no index entry is added or removed; no stored
tile's bytes change (§20.3 expressly permits growth: "an extent MAY **grow**, since a
position that becomes real held that channel's fill"); [R-SLB-04] is not triggered
(no change to "the stored-tile set, the run partition, or the byte placement of any
run" — N and S are unchanged, so the partition is unchanged); crc_of_crc_array is
unchanged because the segment CRC array is unchanged. The extent slot is unchanged
because extent_length is a function of `entry_count` ([R-CNT-17]). I could not falsify
it. PASS.
"the growth that raises a zero-extent layer's **last** zero grid count" — a definite
description presented as unique. It is unique *for a given commit sequence*, but a
single commit may raise several zero grid counts at once; such a commit does raise the
last one, so the description still covers it. Strained but not false. The word "last"
carries a separate problem — see finding B-02.

Hunk 2: no "every/only/always/never"; the two-item list is introduced by "each commit
that … or that …", which reads as a closed disjunction. It is not exhaustive against
§20.3 (see check 1), but a Note's narrower list is not a false exhaustive claim.

Hunk 3: "for every run", "each stored tile's offset" — both are genuine universals and
both are what [R-SLB-03] means; register row L41 states the same universal. PASS.

### Check 6 — what else in this structure is still unconstrained?

**Hunk 1/2 structure: the layer record's geometry and index-locating fields.**
Members a growth commit can move: E₀…E_{d−1}; T₀…T_{d−1}; d; C; the derived Gᵢ, N, P;
`entry_count`; the extent slot's `extent_offset` and `extent_length`;
`crc_of_crc_array`; the entry array; the segment CRC array; disk ordinals.
- Eᵢ, Tᵢ, d, C: §7.4 table + [R-GEO-01].
- Gᵢ, N, P: [R-GEO-03] + [R-ENC-04].
- `entry_count`: [R-CNT-17] pins it to the geometry-derived addressed-tile count; row L21.
- `extent_length`: [R-CNT-17] formula; row L22.
- `extent_offset`: [R-CNT-13]/[R-LIF-01] — a new placement.
- `crc_of_crc_array`: [R-CNT-23] ("0 when entry_count = 0"), §15.4, row L27.
- entry array / segment CRC array: §15.1, §15.4, [R-IDX-04].
- disk ordinals: [R-GEO-06].
The repair names `entry_count` and `extent_length` and leaves `crc_of_crc_array` and
`extent_offset` unmentioned — but both are governed by rules of their own, and the
repair is a Rationale, not the rule. No sibling is left ungoverned. PASS.

**Hunk 3 structure: a slab run.** Every quantity a run carries:
run partition (S, block_start, final short run) — [R-SLB-02]; the ordinal→run map —
[R-SLB-02]; ordering of stored tiles within a run ("packed in ordinal order") —
[R-SLB-03], row L41's "out-of-ordinal placement"; the packing relation itself —
[R-SLB-03], row L41; the first stored tile's offset mod A_slab — [R-SLB-03], row L42;
A_slab's own domain — §7.4 + [R-CNT-23], rows L28/L29; S's domain — §7.4, [R-ERR-05];
mutual exclusion with A — [R-CNT-16], row L23; relative placement of runs — [R-SLB-05]
(deliberately free); bytes between runs — §5.2 slack; a run with no stored tiles —
"imposes nothing"; sentinel and structurally-rejected entries — transparent; a
crc-failing entry — not transparent; overlap of a run's bytes with anything else —
§15.3's two verifier rows; re-establishment after a commit — [R-SLB-04].
Every member of the structure is governed. Notably the *last* stored tile of a run has
no end constraint, and that is correct and deliberate ([R-SLB-05] governs between runs).
PASS — I could not find an unpinned neighbouring quantity.

### Check 7 — analogy: repair's governing verb vs cited rule's governing verb

Hunk 1, the one place it argues by warrant: "Growth that changes entry_count **changes**
extent_length with it (`[R-CNT-17]`)". Cited rule's governing verb: "extent_length
**MUST equal** entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4". "changes … with it" against
"MUST equal": the analogy is an inference from a functional equality, and it is valid
only because the function is injective — which it is, being strictly increasing on
non-negative integers. Both range over the same object (one layer's index region under
index_encoding 1). SOUND.

Second warrant, same sentence: "so the layer's whole tile-index region is **re-emitted**
… (§20.3, `[R-WRT-04]`)". §20.3's verb: "**has** its tile-index region **re-emitted in
full**", quantified over "Every layer whose stored-tile set or **index content** this
commit **changes**". Repair's antecedent verb-phrase: "Growth that **changes**
entry_count". Compare the ranges: "index content changes" ⊇ "entry_count changes",
because an entry_count change necessarily changes how many 20-byte entries the region
holds. The analogy runs in the safe direction (repair narrower than warrant). SOUND.
This sentence carries the warrant for exactly one consequence, so there is no
several-rows problem of the kind check 7 was written for.

Hunk 2's warrant is the same §20.3 clause; same verbs, same verdict. SOUND.

Hunk 3 uses no analogy language ("exactly as", "the same way", "as X is", "following X",
"the model is", "transposed from", "for the same reason", "likewise") — I grepped the
repaired sentence's neighbourhood and there is none. N/A.

## 3. The charter's own sweep: what elsewhere depended on the old text

### 3.1 Re-keying onto `entry_count` — every other passage stating the same claim

grep `entry_count` (35 hits) and `grid count` (8 hits) over the flattened document.
Passages that state, in any terms, when a commit re-emits an index region or when a
layer starts addressing tiles:

1. **§5.2's figure block, line 605–610 (">" block).** "A commit that changes a layer's
   stored-tile set or index content re-emits that layer's whole tile-index region as
   well, at a new placement (§20.3, `[R-WRT-04]`)." — states the normative trigger word
   for word. **Still correct**, unaffected by the re-keying.
2. **§20.3 step 4 (normative).** Quoted above. **Still correct.**
3. **§20.3's cost Note (">" block, 3084–3090).** "any change to a layer's stored-tile
   set re-emits that layer's whole tile-index region". **Still correct** (a subset
   claim, and it says nothing about growth).
4. **§20.3 shape (c) (">" block, 3134–3145).** "A change confined to the directory —
   clearing a slab declaration, renaming a layer, or changing a channel's fill value on
   a layer with no padding position and no pad bit." A growth leaving `entry_count`
   unchanged is also such a change and is not in that list — but the list reads as
   illustrative, and it was equally incomplete under the old wording (which likewise
   called such a growth directory-only). **Still correct as written**; not a
   consequence of the repair. Not reported.
5. **§20.3's growth permission (normative, 3029–3038).** "an extent MAY **grow** …
   provided the grown geometry stays within every bound the layer's own declarations
   impose, `[R-COD-07]`'s lz4 decoded-size cap among them (L44), which an empty layer
   escapes only because that cap is quantified over addressed tiles." **Still correct** —
   it says the escape exists and why, and does not say when it ends.
6. **§21.6's row.** "A dimension has extent 0 | A valid, empty layer: zero addressed
   tiles, an empty index, reads returning no samples | `[R-GEO-02]`". **Still correct.**
7. **§21.9's per-instance paragraph (3753–3766).** "A layer addressing no tile (§11.2)
   therefore has no tile whose decoded size the table bounds." **Still correct.**
8. **§17.2's Note under [R-COD-07] (">" block, 2336–2343).** "The escape is not
   durable: **a later commit that grows an extent addresses tiles**, and the same
   declarations are then measured against the cap." — **NOW FALSE, and it is the
   passage the repair should have swept.** See finding B-01.
9. **§7.4 (normative).** "a layer with zero addressed tiles has extent (0, 0)".
   **Still correct.**
10. **§15.4's Example (">" block).** "At entry_count = 0 there is no region at all".
    **Still correct.**
11. **§21.9's limits table.** "addressed tiles per layer (entry_count) | 2³²" — equates
    the two, consistent with §11.2 and [R-CNT-17]. **Still correct.**
12. **§3.1 glossary, "addressed tile / stored tile".** **Still correct.**

### 3.2 The exception the old wording carried, and what mirrored it

Old exception: "save where another dimension's grid count is 0, which holds the product
at 0 and adds no entry". The new wording folds it into the `entry_count` criterion, so
nothing normative depended on it. Passages written to mirror it:
- §20.3's "which an empty layer escapes only because that cap is quantified over
  addressed tiles" — mirrors it correctly and is **still needed**, because it is now the
  only *normative* statement of why an empty layer escapes [R-COD-07].
- §17.2's Note — mirrors the exception's *negation*. Under the old text this Note agreed
  with §11.1's tail ("the first growth of a zero-extent layer included") and disagreed
  with §11.1's exception clause; the repair resolved §11.1 in the exception's favour and
  left the Note behind. **Finding B-01.**
- §20.3's shrink parenthetical, "Dropping a tile out of the addressed set (§11.2's grid
  count falls)" (normative prose, line 3044). Read as a biconditional this would be
  wrong in the zero-product case (a grid count can fall from 4 to 2 while another stays
  0 and no tile is dropped). Read as what it is — a gloss naming the mechanism by which
  a tile leaves the addressed set — it is fine, and the operative claim ("is not itself
  such an alteration") is unaffected either way. It predates the repair and is not a
  restatement of the repaired claim. **Examined, not reported.**

### 3.3 The pronoun disambiguation — every restatement of [R-SLB-03]'s packing relation

grep `previous stored tile`, `pack(ed|ing)`, `contigu` across the document:
- **Row L41 (§21.3, line 3522).** "Inside a slab run, a stored tile's offset ≠ **the
  previous stored tile's offset plus the previous stored tile's length** (gap, overlap,
  or out-of-ordinal placement; sentinels and entries §15.3 classifies reject-tile on a
  structural ground are transparent, an entry failing only its stored bytes' crc is
  not)". The row **already carried the disambiguated reading**. Before the repair,
  §21.1's precedence clause — "where a row and the rule it cites diverge, **the rule
  governs**" — meant the ambiguous prose governed over the explicit row. The repair
  brings the rule into agreement with the row. **Now consistent; this is the repair
  landing correctly.**
- **Row L42.** "A slab run's first stored tile's offset is not a multiple of A_slab" —
  matches the untouched second half of the sentence. **Still correct.**
- **§16.2's own crc carve-out.** "its offset and length stand, and the packing relation
  reads them as it does any other stored tile's" — **still correct**, and only coherent
  under the disambiguated reading.
- **§16.2's Example (">" block, 2213–2218).** "If ordinal 10 is a sentinel, run 1's
  stored tiles are 8, 9, 11…15, packed with no gap where 10 would have been." No byte
  arithmetic to check; the ordinal arithmetic ([0,8),[8,16),[16,24),[24,32) for S=8,
  N=32) matches [R-SLB-02]'s "Run r of a block starts at ordinal block_start + r·S".
  **Still correct.**
- **§16.2's "what slabs are" Note.** "A slab guarantees *contiguity*: consecutive disk
  ordinals occupy consecutive bytes." A loose gloss — sentinel ordinals occupy no bytes —
  but the body sentence three paragraphs above states the transparency rule expressly,
  and this wording predates the repair. **Examined, not reported.**
- **§19.4's region-read Note.** "a slab declaration guarantees contiguity only for
  stored tiles within one run (§16.2)". **Still correct.**
- **§3.1 glossary, "slab".** "a declared run of consecutive stored tiles kept physically
  contiguous as one I/O unit". **Still correct.**
- **§20.5 (line 3259).** compactor "free to place structures anywhere §5.2 admits and
  every declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)". **Still
  correct.**
- **Appendix G item 3.** "each later structure begins where the previous one ended, save
  where alignment forces a gap" — an independent restatement of the same arithmetic, in
  the disambiguated direction. **Still correct, and now in agreement with §16.2.**
- Appendix A carries no layer and no slab; Appendix B carries only S and A_slab domains.
  **Unaffected.**

### 3.4 The reverse direction — do the repairs duplicate or contradict anything?

- Hunk 3 vs row L41: same claim, two places. That is this document's declared practice
  (§21.1: "each row *restates* its governing rule"), so it is duplication by design, not
  a defect. They now agree byte for byte in substance.
- Hunk 1 vs §20.3 step 4: subset, not contradiction.
- Hunk 1 vs hunk 2: they now agree — both key on `entry_count`.
- Hunk 1 vs §17.2's Note: **contradiction. Finding B-01.**

## 4. Findings

### B-01 — §17.2's [R-COD-07] Note still says any extent growth starts addressing tiles

Location: spec/tarn.md §17.2, lines 2336–2343, the Note under [R-COD-07].
Verbatim: "The escape is not durable: a later commit that grows an extent addresses
tiles, and the same declarations are then measured against the cap."
Contradicted by the repaired §11.1, verbatim: "a growth raising one grid count
⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among them, the product holding at 0" … "the
growth that raises a zero-extent layer's **last** zero grid count included."

Two ways the Note is false, both derivable from §11.2's N = ∏ Gᵢ:
(a) A layer with two zero-extent dimensions — E = (0, 0) — that grows one of them to a
    nonzero value has G = (1, 0), N = 0, and still addresses no tile. The cap is still
    not measured.
(b) Even with a single zero-extent dimension — E = (0, 100), T = (256, 256), G = (0, 1) —
    growing the *other* extent from 100 to 300 gives G = (0, 2), N = 0. Still no
    addressed tile.
The Note's claim is true only of the growth that raises the last remaining zero grid
count, which is precisely the formulation hunk 1 has just adopted next door.

Under the old §11.1 wording, this Note agreed with §11.1's tail ("the first growth of a
zero-extent layer included"). The repair changed that tail and left the Note standing.
This is the unswept restatement.

Repair: replace "a later commit that grows an extent addresses tiles" with "a later
commit that raises the layer's last zero grid count (§11.1, §11.2) addresses tiles", or
"a later commit that gives every dimension a nonzero extent addresses tiles".

Byte-level: **No**, and I want to be explicit about why, because the case for "yes" is
tempting. The normative rule [R-COD-07] reads "Writers MUST NOT declare this codec for
a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000 bytes", and
row L44 reads "Codec 4 (lz4) declared on a layer any of whose **addressed** tiles'
decoded size exceeds 0x7E000000 bytes". Both quantify over addressed tiles and neither
moves. §20.3's normative growth permission also states the escape correctly. [R-CNF-01]
denies the Note any force, so it cannot bar a writer from emitting, nor oblige a reader
to reject. The emittable set and the accept/reject set are therefore identical under
both readings.
What the fork would look like if one *did* grant the Note weight, named concretely so
the judgement can be checked: a rank-2 interleaved uint8 layer, T = (65536, 65536), so
P = 2³² and decoded size P·Q = 4,294,967,296 > 0x7E000000 = 2,113,929,216, declared with
codec 4 and E = (0, 0); generation 2 grows E₀ to 65536 leaving E₁ = 0. N = 0,
entry_count = 0, extent slot (0, 0). Reader X (following [R-COD-07] and L44) accepts;
reader Y (following the Note) reports a validity error at layer scope. The file is
conforming — I checked it against L21, L22, L27, [R-ENC-04] (P·Q = 2³² ≤ 2⁶³−1) and
[R-GEO-01]. So the defect is a live implementer trap; it is just not a fork between two
competent readings of the *normative* text.

### B-02 — "last" in the repaired §11.1 tail has a positional reading that is false

Location: spec/tarn.md §11.1, lines 1502–1503.
Verbatim: "— the growth that raises a zero-extent layer's **last** zero grid count
included."
Intended reading: the growth that raises the final grid count still standing at zero
(after which N > 0). Under this reading the sentence is true.
Available second reading: "last" as *last-declared*, which is the sense this very
section fixes — §11.4: "**1 = row-major** — the **last-declared** dimension varies
fastest" — and §11.2's example uses "the last row of tiles". Under that reading the
sentence says: the growth that raises the zero grid count belonging to the
last-declared among the zero-extent dimensions changes entry_count. That is false
whenever an earlier-declared dimension is also zero: E = (0, 0) → (0, 65536) leaves
G = (0, 1), N = 0, entry_count unchanged, so no re-emission — the exact case the
preceding sentence of the same repair says leaves the directory alone. The repair thus
contains a reading under which its two halves contradict each other.
Repair: "— the growth that leaves no dimension with extent 0 included", or "— the growth
that raises the layer's *only remaining* zero grid count included".
Byte-level: No. The block is a Rationale ([R-CNF-01]); the obligation is [R-CNT-17]'s
`entry_count` cross-check plus §20.3, both of which are stated over the actual value of
entry_count and admit no such ambiguity. Row L21 likewise. Nothing a writer may emit and
nothing a reader must reject turns on it.

## 5. Things I looked for and did NOT find (so the clean parts are on the record)

- No occurrence of the removed phrase "grid boundary" survives anywhere (0 hits).
- No occurrence of "first growth" survives anywhere (0 hits).
- No normative rule anywhere keys re-emission on grid counts; §20.3 keys it on
  "stored-tile set or index content", which the re-keying did not disturb.
- No worked example anywhere computes a slab byte offset, so the pronoun fix invalidated
  no arithmetic. The two examples that touch slabs (§16.2's, §19.4's Note) are ordinal-
  level and remain correct.
- No register row disagrees with any of the three repairs. L41 and L42 agree with hunk 3;
  L21, L22 and L44 agree with hunks 1 and 2.
- §21.6, §21.7, §21.9, Appendix G and Appendix H were each read for a dependent
  statement of the old formulations; none carries one.
- Neither hunk 1 nor hunk 2 widened a licence, so there is no carve-out for a widened
  licence to collide with.
