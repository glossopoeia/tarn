# Audit transcript — hunks 01, 02, 05, 06, 07 (case-adr0113)

## Disclosure

I read exactly the five hunk files named in my charter (hunk-01.diff,
hunk-02.diff, hunk-05.diff, hunk-06.diff, hunk-07.diff), via `cat` in one
Bash call, and the specification at
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, via
the Read tool (several offset/limit windows: 1560-1660, 1690-1730,
1900-1925, 660-680, 1440-1485, 3072-3391, 3422-3500, 3884-3969) and via
`grep -n` searches listed under Sweeps below. I did not read full.diff, any
other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, or git history, and did not list the
case-adr0113 directory.

**Contamination notice.** Before this task began, my context already
contained project instructions (a CLAUDE.md pointer to AGENTS.md), a user
memory file (MEMORY.md) with two unrelated notes about a "TARN harness spec
path" and a "TARN lineage gate word list", and an email/date system
reminder. None of this named a defect location, a prior round's finding, or
this round's expected outcome, and none of it is spec content or evidence
about the spec. I disregarded all of it and drew no conclusion from it; I
flag it here per the access rule's disclosure requirement.

## Hunks audited, and the rule each adopts

**Hunk-01** (lands §11.1 Rationale, spec lines ~1602-1627, a block headed
`> **Rationale.**`, hence non-normative per [R-CNF-01]): restates, as
commentary on the normatively-controlling §20.3, that step 4 contains
*three* declaration-change bars, that only the §14 bar's test reaches a
shrink or a growth, that the other two (the sample-type bar and the planar
disk-ordinal-move bar) reach neither, and tightens "a layer that stored
nothing may be re-declared freely" to "a layer that stored no tile in the
generation the commit supersedes may be re-declared freely; a layer the
commit itself empties does not qualify" — matching the tense of the actual
normative rule it is glossing.

**Hunk-02** (lands §20.3 step 4, normative numbered-list text, spec line
~3139): inserts a naming sentence, "Call this the **§14 bar**," directly
after the paragraph that states the rule, giving it a label for every later
back-reference to resolve to.

**Hunk-05** (lands §20.3 step 4's shrink paragraph, normative text, spec
lines ~3252-3264): replaces the dangling anaphor "the bar above" with the
explicit label "the §14 bar," and adds "Neither of the two bars beside the
§14 bar reaches a shrink: one bars a change to a channel's declared sample
type, the other a change to a planar layer's channel declarations that
moves a stored tile's disk ordinal, and a shrink is neither" — the mirror
image of hunk-01's growth-side claim.

**Hunk-06** (lands §20.3's Example (c), a block headed `> **Example — the
three shapes...`, hence non-normative): parallels hunk-01's tense fix inside
the example: "A layer storing no tile is re-declared freely" becomes "A
layer that stored no tile in the generation the commit supersedes is
re-declared freely, ... a layer the commit itself empties does not
qualify."

**Hunk-07** (lands §21.7 "What no check detects," plain prose, not a
blockquote, hence normative by [R-CNF-01]'s default): adds that the two
companion bars (sample-type, ordinal-move) are, unlike the §14 bar, *never*
witnessed for a tile that remains live and whose bytes the change leaves
untouched, because the prior generation's declarations are not part of the
live state §9.7 walks — and restates, for the setup of the following
paragraph, that element size alone does not decide which side of the §14
bar a type change falls on (uint8→bool keeps element size 1 but changes the
plane's byte length from P·Bᶜ to ⌈P/8⌉).

## Check 8 — back-references (primary instrument), run across §20.3 step 4

I read forward from each insertion point to the end of its subsection and
resolved every anaphor of the shape "the X above / that requirement / it /
such a change."

- **"the bar above"** (pre-repair, in the shrink paragraph, superseded by
  hunk-05): before this round's fix, its nearest preceding bar-shaped
  paragraph was the planar-ordinal-move bar (§20.3 step 4, lines
  ~3197-3235), which sits immediately above the shrink paragraph; but the
  content it must resolve to — "a new padding position whose stored byte
  already holds the fill … is not [an alteration]" — is the §14 bar's own
  carve-out (lines ~3132-3157), several paragraphs earlier, past two
  intervening bar-paragraphs (sample-type, ordinal-move). Nearest-antecedent
  resolution and correct-antecedent resolution diverged before this hunk.
  Hunk-05 removes the anaphor entirely, replacing it with "the §14 bar" —
  the correct referent, named explicitly. Verdict: **fixed by this hunk**,
  not introduced by it.
- **"Call this the §14 bar"** (hunk-02): the label attaches to the
  paragraph immediately preceding it (the paragraph that opens "A commit
  MUST NOT change a layer's declarations…", spec lines ~3132-3138). No
  ambiguity: label and labelled text are adjacent.
- **"the two bars beside the §14 bar"** (hunk-05, new): resolves to the
  sample-type bar (lines ~3159-3195) and the ordinal-move bar (lines
  ~3197-3235), both named explicitly in the same sentence ("one bars a
  change to a channel's declared sample type, the other a change to a
  planar layer's channel declarations that moves a stored tile's disk
  ordinal"). Self-resolving, no dangling reference.
- **"The other two bars"** (hunk-01, Rationale): same two bars, same
  explicit naming pattern. Self-resolving.
- **"this shape"** (§20.3 Example (c), immediately after hunk-06's
  insertion: "…which is the same step's permission — a layer the commit
  itself empties does not qualify. Editing user metadata is not this
  shape:"): before the insertion, "this shape" resolved to "shape (c),
  directory-confined change" (the subject of the whole example paragraph).
  The inserted clause ("a layer the commit itself empties does not
  qualify") is a qualifier on the sentence before it, introducing no
  competing noun a reader could mistake for a "shape." Resolution is
  unchanged by the insertion: still shape (c). Checked and unaffected.
- **"the same step's permission"** (hunk-06, unchanged wording, checked
  because it sits one clause before the insertion): resolves to step 4's
  growth paragraph permission ("A layer that stores no tile … MAY be
  re-declared freely," lines ~3222-3226), which the preceding parenthetical
  "(step 4)" in the same Example paragraph names explicitly two sentences
  earlier. Unaffected by the insertion.
- **"the rows below"** (hunk-07, new, forward reference): resolves to the
  enumeration that follows in the unchanged remainder of §21.7 — §21.4's
  content rows, T3/T14, the codec rows (T15/T17/T23/T25), T26 — all of
  which the text explicitly names over the next ~30 lines. Consistent
  forward reference, not a backward anaphor, so check 8's "nearest
  preceding antecedent" hazard does not apply to it, but I traced it
  forward to confirm it lands on real rows rather than nothing.
- **"escapes them exactly as it escapes the §14 bar"** (hunk-07, new): see
  finding B-01 below — this is the one place check 8's method (comparing
  what a phrase resolves to before/after, and what sense a term carries
  elsewhere in the document) surfaced a real problem, though the problem is
  a term-sense collision rather than a changed grammatical antecedent.

No back-reference in §20.3 step 4 or in the surrounding Rationale/Example
was left unedited that should have been — the sole one that needed fixing
("the bar above") *is* one of my hunks' fixes, and I found no residual
occurrence of "bar above" anywhere in the document (swept clean).

## Check 1 — tense and quantifier

- Hunk-01 and hunk-06 both replace an untensed "stored nothing" /"storing no
  tile" with "stored no tile in the generation the commit supersedes,"
  which is exactly the quantifier the actual normative rule uses (§20.3
  step 4's growth paragraph, line ~3222-3223: "A layer that stores no tile
  in the generation this commit supersedes MAY be re-declared freely").
  Both repairs align a Rationale/Example restatement to the normative
  rule's own tense. Correct, and in each case explicitly cross-verified
  against the "a commit does not earn this permission by emptying the layer
  as it re-declares it" sentence in step 4 (line ~3225-3226), which both
  repairs' added "does not qualify" clause paraphrases accurately.
- Hunk-05's "a shrink … barred whether or not the new state still stores
  it" quantifier (pre-existing, unchanged by this hunk but re-verified)
  matches the §14 bar's own stated quantifier: "for any tile that layer
  stores **in the generation this commit supersedes**" (line ~3133-3134).
  Consistent.
- Hunk-07's added "for a tile the layer stores in the generation the
  commit supersedes" matches the same quantifier. Consistent.

## Check 2 — citations resolve

| Citation (as it appears in a repaired hunk) | Where I opened it | Verdict |
|---|---|---|
| §14 bar (hunk-01, -05, -06, -07 all use the label hunk-02 coins) | §20.3 step 4, lines 3132-3157 | Resolves to the paragraph that states it; label and rule co-located, verified by hunk-02 itself |
| §12.1 (hunk-07: "the element sizes of §12.1 do not … decide it") | §12.1 "Core sample types," line 1717 heading; element-size definition at lines 1752-1834 | Confirmed: bool element size 1 stated at line 1757 and 1961 |
| formula P·Bᶜ → ⌈P/8⌉ (hunk-07, restating step 4's own line ~3168-3170) | §14 table, line 1967 ("planar, numeric channel c: P · Bᶜ"); line 2024 ("decoded size is ⌈P/8⌉ bytes … Packing is exclusive to planar bool") | Confirmed accurate |
| §9.7 (hunk-07: "the prior generation's channel declarations are not part of the live state, which is all §9.7 walks") | §9.7 "Coverage verification," line 1440; opening sentence line 1442: "A verifier checking [R-CNT-02]'s partition walks the live state only" | Confirmed accurate — direct match of wording |
| §21.4's content rows (hunk-07, restated from pre-existing text) | §21.4 "Tile-scope violations," line 3759; rows T2, T4, T5 at lines 3768-3771 concern bool-byte / padding-fill / pad-bit content | Confirmed: these are exactly the "content rows" the sentence means |
| T3, T14 (hunk-07, restated pre-existing text, unchanged by the hunk itself but re-verified in context) | Table rows at lines 3771 (T3) and 3782 (T14) | Confirmed: both test decoded/declared length, matching "test a length rather than the decoded image's content" |

No citation in these five hunks pointed at a rule that "almost" said the
claimed thing; every one I checked matched exactly.

## Check 3 — label vs marker

- Hunk-01 lands inside a block opening `> **Rationale.**` (spec line 1602)
  → non-normative per [R-CNF-01]. The block's own unchanged opening
  sentence ("§20.3 states normatively, and governs, what a commit may do…")
  already disclaims force correctly — the Rationale explicitly attributes
  the normative content to §20.3, so the repair landing here does not
  create an orphaned sole-source rule. I checked whether "a layer the
  commit itself empties does not qualify" is *also* stated in normative
  (non-blockquote) text elsewhere: yes — §20.3 step 4 itself, line
  ~3225-3226 ("the tense is these bars', so a commit does not earn this
  permission by emptying the layer as it re-declares it"), unlabeled and
  therefore normative. Test applied: opening-words-of-block, not the ">"
  marker alone. Passed — the normative statement exists outside the
  Rationale.
- Hunk-02 and hunk-05 land in §20.3 step 4's plain numbered-list prose —
  not a blockquote at all (no ">" prefix in the source at these lines) —
  so they are normative on the default rule, no label question arises.
- Hunk-06 lands inside a block opening `> **Example — the three shapes a
  commit takes.**` → non-normative. Same check as hunk-01: the "does not
  qualify" content is independently and normatively stated in step 4
  (line ~3225-3226, unlabeled prose). Passed.
- Hunk-07 lands in §21.7, which is plain prose — no ">" prefix, no Note/
  Example/Rationale label — so it is normative by [R-CNF-01]'s default (§21
  is not one of the exempted parts). I checked the actual block markers at
  the read offsets and confirmed no leading ">" on any of lines 3884-3968.
  Since this section is descriptive of detectability rather than a source
  of new MUST/MUST NOT text, its normative status matters less here than
  its consistency with the actual bars stated in §20.3 (checked below).

## Check 4 — contradiction within the passage

- Compared hunk-01's "the other two bars reach neither a shrink nor a
  growth" against step 4's own unchanged sentence permitting geometry
  changes to renumber disk ordinals as a side effect of re-emission ("a
  geometry change renumbers ordinals wherever [R-GEO-06] moves them," line
  ~3126-3127, and again in §11.1's own unchanged Rationale tail, lines
  1622-1627: "disk ordinals renumber wherever [R-GEO-06] moves them"). These
  do not contradict: the planar-ordinal-move bar (bar 3) is scoped
  specifically to a change to *channel declarations* (reordering,
  insertion, removal — line ~3202-3208) causing an ordinal move
  independent of geometry; growth- or shrink-driven renumbering is a
  different mechanism (N changing because the grid does), explicitly
  licensed by the general re-emission rule, and is never framed anywhere as
  triggering bar 3. Verified this distinction is stated explicitly in the
  bar's own text ("what it disturbs is instead the re-emission rule above,
  which licenses a renumbering only for a geometry change," line
  ~3199-3200). No contradiction.
- Checked whether hunk-05's "a shrink is neither [a sample-type change nor
  an ordinal-move change]" could be falsified by a compound commit that
  shrinks *and* changes channel order in the same commit — no: the claim is
  about what a shrink, as an extent operation, does by itself; a commit
  that also reorders channels would separately trigger bar 3 for that
  reason, which the text does not deny (it says "a shrink is neither,"
  about the shrink's own effect, not about everything a commit containing a
  shrink might additionally do). No contradiction found.
- Checked hunk-07's "no check can know which ordinal a stored tile used to
  occupy, or which type its channel carried before" against §9.7's
  statement that "A verifier decodes every stored tile" (line 1466): decoding
  under the *current* declaration does not require or provide access to the
  *prior* declaration, so a verifier that decodes every tile still cannot
  detect that a declaration differs from what it used to be. No
  contradiction.

## Check 5 — exhaustive claims

- "Of its three bars" (hunk-01) / "the two bars beside the §14 bar" (i.e.
  three total, hunk-05): I re-read the whole of §20.3 step 4 (lines
  3115-3280) looking for a fourth declaration-change prohibition — none
  found. The only other constraints in step 4 (the lz4 decoded-size cap,
  the 2⁶³−1 ceiling, slab/alignment obligations) are general validity
  bounds on *any* declaration, not additional bars on *changing* a
  declaration between generations, and the text itself frames them
  separately ("and the list is not offered as exhaustive" — but that
  disclaimer is about bounds on growth, not about the count of bars).
  Cross-checked: hunk-01 and hunk-05 state the "three" count independently,
  in two different subsections (§11.1 Rationale and §20.3 step 4 itself),
  and they agree. "Three" holds up.
- Considered whether "the other two bars reach neither a shrink nor a
  growth" (hunk-01) is falsified by linearization changes, dimension-name
  changes, or rank changes — checked: linearization has exactly one valid
  value (1) per [R-GEO-05]/L33 (line 3741), so there is no valid target
  value to change *to*; this is a separate validity rule, not a
  generation-to-generation change bar, and is out of scope for "three
  bars." Not falsified.
- "Which case a type change falls in is not decided by the element sizes of
  §12.1" (hunk-07, restated) — verified against the one worked
  counterexample the text gives (uint8→bool) and did not find a case where
  element size alone *would* decide it, so the negative claim holds for the
  example given (I did not exhaustively test all 13×13 type-pair
  combinations against this claim — see confidence_empty).

## Check 6 — what else in this structure is unconstrained

Named structure: a channel declaration, which §12 (line 1717-1723) defines
as exactly three fields — a name, a sample type, and a fill value — plus,
at the layer level, the *order* in which channels are declared.

- **Sample type**: barred by the sample-type bar (line ~3172-3175). Fixed.
- **Declared order** (reordering, insertion, removal — for a planar layer,
  via disk ordinal): barred by the ordinal-move bar (line ~3202-3208).
  Fixed. (Confirmed the text explicitly carves out the *interleaved* case
  as unaffected by ordinal changes because its ordinal is s alone — but
  reordering an interleaved layer's channels still changes each channel's
  in-tile byte *offset* Fᶜ and the sample stride Q, line ~3177-3178, and
  that is independently covered by the §14 bar's own list, "the byte offset
  of any sample within the decoded tile image," line ~3137. So interleaved
  reordering is not a gap — it is caught by the first bar, not the third.)
- **Fill value**: I checked whether a fill-value change on a channel is
  constrained by any of the three bars. It is — via the §14 bar's own list,
  "the content [R-SER-05] fixes there" (padding-position content is fixed
  to equal the channel's declared fill, line ~3136), and this is confirmed
  directly by the Example (c) text hunk-06 lands in: "A fill change on a
  layer that **stores** a tile carrying [a padding position or pad bit] is
  not an appender's operation at all (step 4): it would invalidate every
  stored tile it reaches" (line ~3343-3346). Fixed.
- **Channel name**: I found no rule, in §20.3 step 4 or elsewhere,
  constraining a channel-rename between generations the way layer renames
  are explicitly permitted as directory-only in Example (c) ("renaming a
  layer," line 3341). I looked for a parallel statement about channel
  renaming and found none (grep below). I do not think this is a gap
  *introduced or left open by these five hunks* — a name carries no byte-
  level consequence the §14 bar's list would need to reach (unlike type,
  order, or fill), so by the same logic that makes layer-renaming
  directory-only and unconstrained, channel-renaming should be as well; and
  none of my hunks touch, narrow, or claim anything about channel names.
  I report this as a considered-and-rejected candidate, not a finding
  against these hunks (see Rejected candidates).

## Check 7 — analogies, verb-for-verb

- Hunk-05: "and for the same reason" (pre-existing, re-verified in context)
  — the shrink paragraph's "the quantifier is the superseded generation's"
  is compared to the §14 bar's own stated quantifier ("for any tile that
  layer stores **in the generation this commit supersedes**," line
  3133-3134). Both range over the same set (tiles stored in the superseded
  generation). Matches.
- Hunk-07: "a commit that supersedes every tile it would have damaged
  escapes them exactly as it escapes the §14 bar." Governing verb pair:
  **"escapes [the rows]"** vs **"escapes [the §14 bar]"**. I checked every
  other use of "escape" in the document (grep below, 3 hits total): line
  3142 "a commit does **not** escape this [§14 bar] by unstoring… this
  bars it" and line 3231 "an empty layer escapes [a cap] only because that
  cap is quantified over addressed tiles" — both established uses mean
  "is exempted from / not subject to a normative requirement." Read against
  that established sense, "it escapes the §14 bar" in hunk-07 would assert
  the commit is *not barred* by §14 — which flatly contradicts line 3142's
  explicit statement that such a commit ("superseding every tile of a layer
  and re-declaring it") is *still barred*. The sentence is only correct
  under a third, unestablished sense — "escapes **witnessing of**" — which
  matches the section's own "unwitnessed" framing used two sentences later
  for the identical scenario (line 3952-3954: "the §14 bar is unwitnessed
  there"). The two governing verbs are not reliably the same sense, and
  this is check 7's exact shape: an analogy ("exactly as") whose two sides
  use the same word for two different established relations elsewhere in
  the document. See finding B-01.

## Check 8 — summary

Covered under its own section above (primary instrument). One term-sense
collision found (B-01); every grammatical back-reference resolution I
traced was correct or was itself the fix.

## Sweeps run (verbatim, with counts)

- `grep -n "bar above\|above bar\|the bar$\|this bar\b" tarn.md` → 0 hits (confirms the fixed anaphor left no stray twin)
- `grep -n "§14 bar\|the bar\b" tarn.md` → 10 hits (lines 1606, 2608, 3008, 3139, 3159, 3198, 3237, 3252, 3257, 3262) plus 3929, 3953 for "§14 bar" specifically when re-run — all traced and classified above; 2608 and 3008 are unrelated bars (a buffer-sizing bar, a prospective residency bar), not near this subject, no ambiguity
- `grep -n "escape" tarn.md` → 7 hits (1541, 2466, 2469, 2698, 2744, 3142, 3231, 3823, 3928, 3929, 4146) — filtered to the 3 substantive normative/near-subject uses (3142, 3231, and the new 3928-3929)
- `grep -n "companion bar" tarn.md` → 1 hit (3920, the new one)
- `grep -n "disk ordinal\|declared sample type\|channel declaration\|reorder\|re-declar" tarn.md` → 24 hits, read in full, reported under "look outward" below
- `grep -n "add a channel\|adding a channel\|insert.*channel\|remove.*channel\|appending a channel\|new channel" tarn.md` → 0 hits
- `grep -n "renam\|channel's name\|channel name" tarn.md` → 5 hits (568, 2776, 3341, 4043, 4215) — none states a channel-rename rule; only layer-rename (3341) is addressed
- `grep -n "R-WRT-04\]" tarn.md` → 5 hits, checked for consistent attachment to the whole numbered step-4-through-6 procedure
- `grep -n "empt" tarn.md` → 19 hits, scanned for any passage permitting a commit to both empty a layer and freely re-declare it in the same breath — none found; consistent with the new carve-out
- `grep -n "element size" tarn.md` → 12 hits, used to verify the uint8/bool element-size claim
- `grep -n "⌈P/8⌉\|P · Bᶜ\|P·Bᶜ" tarn.md` → 9 hits, used to verify the plane-size formula
- `grep -n "linearization" tarn.md` → 12 hits, used to rule out a fourth "bar" candidate
- `grep -n "^#### 21\.\|^### 21" tarn.md` and `sed -n '3759,3796p'` — used to verify §21.4's T2/T4/T5 rows and their governing rules
- `sed -n '3422,3500p' tarn.md` (§20.5 Compaction) — scanned for any statement permitting channel-declaration changes during compaction; none found (compaction preserves content, relocates only)

## Derived numbers

- "Three bars" (hunk-01, hunk-05): I counted the declaration-change
  prohibitions in §20.3 step 4 myself by reading lines 3115-3280 in full:
  (1) the §14 bar (3132-3157), (2) the sample-type bar (3159-3195), (3) the
  planar disk-ordinal-move bar (3197-3235). Count = 3, matching both
  hunks' claims.
- Disk-ordinal formula check (§11.4 worked example, unchanged, used only to
  sanity-check the shared vocabulary these hunks rely on): layer with
  N = 32, C = 4, channel 2, spatial ordinal 10 → disk ordinal
  c·N + s = 2·32 + 10 = 74, matching the document's own stated result at
  line 1710. Not a hunk-introduced number, but confirms I am reading the
  disk-ordinal formula the same way the repairs assume.
- uint8 vs bool plane size at P = 1: P·Bᶜ = 1·1 = 1 byte; ⌈P/8⌉ = ⌈1/8⌉ = 1
  byte. The two formulas coincide exactly at P = 1, matching the
  document's own (unchanged) statement "the two coincide at P = 1"
  (line 3171, not itself part of my hunks but the fact hunk-07 restates
  without that clause — checked it isn't needed for hunk-07's narrower
  point, which only asserts element size doesn't decide the case, not that
  the two formulas always differ).

## Rejected candidates

1. **"Of its three bars … the one reaching a shrink or a growth is the §14
   bar" vs. the general permission for geometry changes to renumber disk
   ordinals** — opened as a possible contradiction (does growth's
   renumbering trigger the ordinal-move bar the sentence says growth
   doesn't reach?). Closed by: the ordinal-move bar is textually scoped to
   *channel-declaration* changes (line 3202: "MUST NOT change the channel
   declarations"), not geometry changes; the general renumbering permission
   is keyed to [R-GEO-06] moving ordinals as a *side effect of a geometry
   change*, a mechanism the bar's own text distinguishes explicitly
   ("what it disturbs is instead the re-emission rule above, which licenses
   a renumbering only for a geometry change," line 3199-3200). Not a
   contradiction.
2. **Channel renaming left unconstrained** — opened as a possible check-6
   gap. Closed by: no bar reaches it because renaming has no byte-level
   consequence for the §14 bar's list to reach, matching the document's own
   treatment of layer renaming as directory-only and unconstrained
   (Example (c), "renaming a layer," line 3341); and none of my five hunks
   touch, narrow, or make any claim about channel names, so even if this
   were a gap it would not be one these hunks created or should have
   closed.
3. **"a layer the commit itself empties does not qualify" (hunk-01,
   hunk-06) vs. some other passage permitting empty-then-redeclare** —
   opened by searching every use of "empt*" in the document (19 hits).
   Closed: no other passage permits a commit to shrink a layer to zero
   tiles and then freely re-declare its channel types/order in the same
   commit; the growth paragraph in step 4 (line 3222-3226, unchanged, the
   rule these two hunks restate) already states the tense explicitly
   ("the tense is these bars', so a commit does not earn this permission by
   emptying the layer as it re-declares it").
4. **"escapes them exactly as it escapes the §14 bar" (hunk-07)** — opened
   and NOT closed; see finding B-01. This is the one candidate that
   survived scrutiny.

## Confidence / what would have found more

I did not exhaustively test the "element sizes of §12.1 do not decide
[which side of the §14 bar a type change falls on]" claim (check 5) against
every pair among the 13 core sample types × both layouts (interleaved/
planar) — I verified the one worked example the text supplies (uint8→bool)
and the general int8↔uint8 / float32↔int32 example stated earlier in step 4
(line 3162-3165), and did not construct or check additional pairs (e.g.
int16→uint16, float64→int64) for a case where the claim might fail. A
false claim there would show up as a body-of-text error, not as anything my
hunks specifically introduce (that sentence pre-dates this round except for
its relocation into §21.7 by hunk-07), so I judged the marginal return on
exhaustively re-deriving all pairs low against the five hunks' actual
scope, but flag it as unchecked.

I did not verify [R-LIF-01] and [R-CNT-02]'s own full text beyond the
sentences quoting them, since neither citation is newly introduced by any
of my five hunks (both are pre-existing cross-references I re-traced only
to confirm the surrounding-passage checks, not because a hunk asserts
something new about them).

## Summary

Five hunks, one real finding. Hunks 01, 02, 05, and 06 form a coherent,
mutually-consistent set: hunk-02 coins the "§14 bar" label at its point of
definition; hunk-05 uses that label to retire a genuinely dangling anaphor
("the bar above," which — before this round — resolved by nearest-antecedent
to the wrong bar) and adds a shrink-side exclusion claim; hunk-01 and
hunk-06 independently add the mirror-image growth-side and example-side
statements, both correctly matching the tense of the actual normative rule
in step 4 and both correctly attributing normative force to step 4 rather
than to the Rationale/Example blocks they sit in. I ran all eight checks
against each of these four hunks and found no contradiction, no bad
citation, no unswept restatement, and no quantifier mismatch; the "three
bars" count these hunks assert independently in two different subsections
is verifiably correct and self-consistent. Check 6 surfaced one candidate
(channel renaming unconstrained) that I traced to a non-issue by analogy
to the document's existing, explicit treatment of layer renaming, and
which in any case is not something these four hunks touch or claim
completeness about.

Hunk-07 is where check 7 (analogy, verb-for-verb) earned its keep: its new
sentence "a commit … escapes them exactly as it escapes the §14 bar" reuses
the word "escape" in a section that otherwise says "witnessed"/"unwitnessed"
throughout, and the word "escape" carries a *different, established*
meaning exactly twice elsewhere in the document — both times meaning
"is exempted from a normative requirement," which is the opposite of what
this sentence needs to mean here (the sentence needs "escapes detection,"
matching an unchanged sentence eight lines later that says the identical
thing correctly, "the §14 bar is unwitnessed there"). This is not
byte-level: it does not change any conforming implementation's obligations,
because the actual bar (a commit superseding a stored tile is *not*
exempted from the §14 bar — it is barred, per line 3142's own explicit
"this bars it") is stated unambiguously in normative text elsewhere and is
untouched by this hunk; §21.7's role is descriptive of detectability only.
But it is a real, locatable ambiguity a careful reader — one who has just
read line 3142's "a commit does not escape this… this bars it" — would
stumble on, which is exactly the class of defect this project's audits
exist to catch even when it does not fork bytes.
