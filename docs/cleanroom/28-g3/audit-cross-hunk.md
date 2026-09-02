# Cross-hunk consistency audit — ADR-0113/0114 repair set (9 hunks)

## 0. Disclosure

Read: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (in
pieces, via sed on absolute line ranges), and hunk-01.diff … hunk-09.diff in
.../scratchpad/case-adr0113/. Did NOT read full.diff, did not list the case
directory beyond a glob of hunk-NN.diff, did not read docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, or
any git history.

Unrequested context appeared before I began: a project instruction file
pointer (CLAUDE.md -> AGENTS.md), a user auto-memory index naming two memory
notes, a git status block with five recent commit subject lines, and an MCP
server instruction block. The commit subjects in particular name this round's
subject matter. I did not open any of it and did not use it; every conclusion
below is anchored to a quotation from spec/tarn.md or from a hunk file, and I
re-derived the "one rule added then withdrawn" and "section converted to a
test" facts from the hunk texts themselves.

## 1. Grouping (by rule touched, not by section or commit)

- **G1 — the §14 bar: its name, its list, its tense, its reach.**
  hunks 2 (names it, adds sample type to its list), 4 (shrink: "the §14 bar is
  the whole of the test of what a shrink alters"), 5 (rescue question; sweeps
  "the bar above" -> "the §14 bar"), 1 (§11.1 restatement), 6 (§20.3 Example
  (c) restatement), 9 (§21.7 witnessing account).
- **G2 — the new planar disk-ordinal bar.** hunks 3 (states it), 5 (says it
  does not reach a shrink), 1 (says it reaches neither shrink nor growth),
  9 (its witnessing).
- **G3 — sample-type re-typing, folded INTO the §14 bar rather than standing
  as a third bar.** hunks 2 (list item), 3 (the elaborating paragraph),
  1 ("Re-typing a channel is the §14 bar's own subject"), 9 (re-typing's
  witnesses). This is the "added to a numbered step and then withdrawn again"
  rule: the residue is that every passage now says "two bars", and the
  re-typing rule survives only as a list item plus a gloss.
- **G4 — the empty-layer re-declaration permission and its tense.** hunks 3
  ("the tense is both bars'"), 1, 6.
- **G5 — §21.7 converted from an inventory into a test, illustration demoted
  to a Rationale block; §21.1 rewired to cite the test.** hunks 9, 7, 8, and
  hunk 5's "§21.7 records the consequence".

## 2. The three scoping mechanisms now coexisting

1. *A rule reaching only what it designates*: the §14 bar and the ordinal bar,
   each quantified over "any tile the layer stores **in the generation this
   commit supersedes**".
2. *A section preamble bounding every rule in its section*: §20.3's opening
   reliance rule ("Structures the commit neither modifies nor relies on impose
   no further obligation", [R-WRT-03]) and §21.1's completeness clause
   bounding what the register must carry.
3. *A requirement deciding which requirements apply to a class of file*:
   [R-CNF-13] (which conditions reach a foreign-major file) and, newly,
   §21.7's unwitnessed/detectable test deciding which obligations the register
   may omit.

Passage falling under two with different answers: §20.3 step 4's declaration
bars fall under (1) and under §21.7's (3). §21.7 says an unwitnessed
obligation is "absent from [the register] by the clause's own terms"; §21.1's
completeness clause, as hunk 7 now states it, says a *detectable* violation the
register omits is a defect. Because the two tests are not complements (§4
below), the §14 bar and [R-COD-10] fall under both with opposite answers.

## 3. Definitions I had to pin down (all quotations verbatim from spec)

§3.1, line ~372:
  "A tile is *stored in a generation* if and only if that generation's
   tile-index entry for it is not the sentinel (§15); unqualified *stored*
   means stored in the live generation."
  -> This is decisive. Bare "the layer stores" = the NEW state. The bars'
  tense is the superseded state. Every unqualified use in these hunks
  therefore states a different rule.

[R-GEO-06], line 1701-1703:
  "The **disk tile ordinal**, which orders tile-index entries (§15), is
   s for an interleaved layer, and **c · N + s** for a planar layer"
  -> hunk 3's arithmetic ("a disk ordinal is c · N + s, and N is the
  spatial-tile count") is correct; appending / removing the last channel
  moves no ordinal. PASSES.

[R-CNF-01], line 104-106: text labeled *Note*, *Example*, or *Rationale* is
non-normative. Applied by LABEL:
  - §11.1 block (hunk 1) opens "> **Rationale.**" -> NON-normative.
  - §20.3 three-shapes block (hunk 6) opens
    "> **Example — the three shapes a commit takes.**" -> NON-normative.
  - §21.7 walk-through (hunk 9) opens "> **Rationale.**" -> NON-normative.
  - hunks 2, 3, 4, 5, 7, 8 and §21.7's first three paragraphs (hunk 9) are
    unmarked running text -> NORMATIVE. Marker test not used anywhere.

[R-CNF-07], line 286-288: "Every **detectable** file-conformance violation
named by this specification is assigned exactly one **reader outcome**" ->
hunk 7's and hunk 9's "the gate [R-CNF-07] applies" PASSES.

L32, line 3720: "A layer **geometry** field whose floor is 1 is 0 | rank d;
**channel count C**; tile extent Tᵢ | ... `[R-GEO-01]`"
  -> the register itself calls the channel count a layer geometry field.

T26, line 3774: the row's condition is narrowed to the detectable slice
("where the resulting image breaks §14.5's padding content or [R-SER-08]'s
bool bytes (a wrong stride with no such structural constraint is undetectable,
§21.7)"). Register practice: register the detectable slice; do not omit the
obligation.

L40/L41/L42 (3728-3730), L21 (3709): the obligations hunk 4 lists as still
binding a shrink are all register-backed.

## 4. The quantifier arithmetic on §21.7 (hunks 7 + 9)

unwitnessed(R)  ≡ ∃f violating R, ∃g satisfying R : live(f) = live(g)
                  ("a file that violates it and a file that satisfies it
                   **can** present identical live states"; and "ask whether
                   the breach **can be made** to leave the live state")
¬unwitnessed(R) ≡ ∀f violating, ∀g satisfying : live(f) ≠ live(g)     [∀∀]
detectable(V)   ≡ ∃f exhibiting V : ∀g not exhibiting V, live(f) ≠ live(g)
                  ("**some** file exhibiting it differs ... from every file
                   that does not")                                     [∃∀]

∃∀ ≠ ∀∀. So "**Detectability is its negation**" is false. The document
falsifies it itself, twice:
  - §21.7's own Rationale on a codec re-declaration: "*sometimes* witnessed
    ... but neither is assured: a writer can choose stored bytes that satisfy
    the old declaration and the new one alike, and the change is unwitnessed
    there." Same condition, detectable(∃∀)=true and unwitnessed(∃∃)=true.
  - T26 registers the detectable slice of [R-COD-10] while §21.7 calls the
    rest undetectable.
Repair direction: the *unwitnessed* definition is the wrong side. It needs
∀f∃g ("no file exhibiting the breach can be separated"), not ∃f∃g.

## 5. Searches run (whitespace-normalised over the whole file; the doc is
hard-wrapped so line-oriented grep would have missed most of these)

Python normaliser collapsing all runs of whitespace to one space, with a
character->line map, then substring search:

  'the bar above'          -> []            (hunks 4,5 swept it completely)
  'that requirement'       -> [3554]        (§21.1, unrelated)
  'the test above'         -> [3913]        (§21.7 Rationale preamble, correct)
  'such a change'          -> [3155, 3185, 3366, 3366]
  'the same ground'        -> []
  '§14 bar'                -> [1606,1616,3141,3176,3215,3232,3237,3241,3933,3974]
  'step 4'                 -> [2930,3101,3324,3933,4197,4210]
  '20.3 step'              -> [3933,4197,4210]
  'declaration change'     -> []
  're-declared freely'     -> [1615,3201,3326]
  'stores no tile'         -> [3200,4637]
  'stored no tile'         -> [1614,3163,3193,3325]
  'sample type'            -> [185,188,1521,1559,1723,1728,1730,3139,3154,4703]
  're-typing'              -> [3164,3934,3950]
  'disk ordinal'           -> [1620,1625,1711,1937,2142,2240,2280,2328,2969,
                               3015,3181,3188,3197,3239,3690,3938]
  'channel declarations'   -> [1619,3180,3238]
  'two bars'               -> [1606]
  "the bar's"              -> []
  "bar's own tense"        -> [3216]
  'layer stores'           -> [1617,3134,3155,3181,3186,3222]
  'layer that stores'      -> [3165,3200]
  'stores a tile'          -> [1617,3155,3186]
  'stores nothing'         -> [3165]
  'layer that stored'      -> [3325]
  'stores in the generation'-> [3182,3223]
  'it stores'              -> [3122]

  grep -n "R-GEO-06"       -> 1626,1703,2971,3127,3181,3923
  grep -n "21\.7"          -> 2521,2613,3240,3457,3560,3580,3774,3864
  grep -n "geometry"       -> 91,1109,1559,1586,2943,3127,3179,3206,3212,3213,
                              3327,3709,3720,4095,4231,4511
  grep -n "slab"           -> (many; L41/L42 at 3729/3730, [R-SLB-04] at 2314)
  grep -n "^| T26 |^| T3 |^| T14 |^| T4 |^| T5 |^| T2 " -> 3750-3774
  grep -n "live state"     -> 692,695,700,703,713,736,737,747,752,1442,3242,
                              3393,3562,3824,3884,3888,3894,3937,3974,4204,
                              4213,4488

## 6. The tense census — the core cross-hunk result

Qualified ("in the generation this commit supersedes"):
  3134 §14 bar MUST NOT           (hunk 2's paragraph)
  3181 ordinal bar MUST NOT       (hunk 3)
  3193 ordinal-bar carve-out      (hunk 3)
  3200 re-declaration permission  (pre-existing, hunk 3 amended its gloss)
  3222 shrink restatement         (hunk 4/5)
  3163 sample-type carve-out      (hunk 3)
  1614 §11.1 re-declaration       (hunk 1)
  3325 §20.3(c) re-declaration    (hunk 6)

Unqualified (= live generation, per §3.1):
  3155 sample-type operative test (hunk 3)  "wherever the layer stores a tile
                                             that carries that channel"
  3165 sample-type carve-out gloss (hunk 3) "a layer that stores nothing"
  3186 ORDINAL BAR OPERATIVE TEST (hunk 3)  "Either is such a change wherever
                                             the layer stores a tile for a
                                             channel that moved."
  1617 §11.1 re-typing restatement (hunk 1)
  3325 §20.3(c) fill prohibition   (hunk 6)  "A fill change on a layer that
                                             **stores** a tile carrying either"

3155 and 3165 are rescued by the qualified sentence they gloss. 3186, 1617 and
3325 are not — and 1617 and 3325 each sit immediately beside a sentence the
same hunk repaired TO the qualified form, which makes the contrast read as
deliberate.

## 7. Analogy comparisons (check 7), verbs side by side

- hunk 3: "the tense is **both bars'**" vs §14 bar "The tense is the prior
  generation's". Governing verbs: "stores ... in the generation this commit
  supersedes" (permission) / "stores **in the generation this commit
  supersedes**" (§14 bar) / "stores in the generation this commit supersedes"
  (ordinal bar MUST NOT). All three agree. PASSES.
- hunk 5: "a shrink producing only those is permitted here **exactly as it is
  there**". "there" = the §14 bar's carve-out, "a new padding position whose
  stored byte already holds the fill [R-SER-05] fixes ... is not what this
  bars". Verbs: "alters nothing §14 fixes for any tile the layer stores in the
  generation this commit supersedes" vs "leaves every one of those tiles'
  stored bytes meaning exactly what they meant". Same set, same tense. PASSES.
- hunk 3: "Where this bars a change the operation is a new layer or a
  whole-file rewrite, **exactly as above**". Above: "Such a change is a new
  layer, or a whole-file rewrite under a fresh file_id ([R-LIF-01], §20.5)."
  PASSES.
- hunk 3: "**for the same reason** ... what it disturbs is instead the
  re-emission rule above, whose only stated occasion for a renumbering is a
  geometry change." Cited text (3127): "(a geometry change renumbers ordinals
  wherever [R-GEO-06] moves them)". The analogy carries TWO cases —
  reordering, and insertion/removal. It holds for reordering (no geometry
  field changes) and fails for insertion/removal, because L32 and [R-GEO-01]
  make the channel count C a layer geometry field. One sentence, several
  cases, sound for one and not the next -> X-08.
- hunk 9: "unwitnessed there **for the same reason** [R-LIF-01] is: it is a
  property of the prior generation". Verbs: "supersedes every tile it would
  have damaged leaves the live state clean" vs "properties of a file's
  history, which §9.7 does not reconstruct". Both range over what §9.7's walk
  cannot reach. PASSES.
- hunk 9: "witnessed on the same terms T26 states for a wrong stride" — T26
  verbatim at 3774 states exactly those terms. PASSES.

## 8. Back-reference resolution (check 8), for every insertion

hunk 3, insertion A (sample-type paragraph) at 3154:
  - "A channel's declared sample type is **such a declaration**, and changing
    it is **such a change**". BEFORE: nothing (paragraph is new). Nearest
    preceding antecedent NOW is the carve-out sentence ending "is not what
    this bars" — whose subject is "a change that leaves every one of those
    tiles' stored bytes meaning exactly what they meant", i.e. an UNBARRED
    change. Intended antecedent is four sentences back ("A commit MUST NOT
    change a layer's declarations in a way that alters..."). -> X-06.
  - "Where a change does reach **them**" (3166, untouched). BEFORE the
    insertion: "them" = the §14 bar's "any tile that layer stores in the
    generation this commit supersedes". NOW: the nearest antecedent is the
    sample-type paragraph's tiles carrying one channel. The untouched
    continuation "strand the originals as slack — **the whole layer's
    worth**" was true of the old antecedent and false of the new one for a
    planar per-channel re-typing. -> X-07.
hunk 3, insertion B (ordinal bar) at 3175:
  - "One effect is barred **beside it**" — intended "it" = the §14 bar;
    nearest antecedent is "a whole-file rewrite under a fresh file_id".
    Then "the §14 bar does not reach **it**" ("it" = the effect) and "what
    **it** disturbs" ("it" = the effect). Three "it"s, two referents, in one
    sentence. -> folded into X-06's repair note.
  - "the tense is **the bar's**" -> hunk 3 changed to "both bars'". The
    insertion would have re-resolved "the bar's" to the ordinal bar; the
    repair landed. PASSES.
  - "exactly as above" (3199) -> resolves to the §14 bar's new-layer sentence,
    unchanged by the insertion. PASSES.
hunk 4:
  - "An extent MAY also shrink, and **the bar above** is the whole of the
    test" -> hunk 3's insertion had re-resolved "the bar above" to the ORDINAL
    bar; hunk 4 replaced it with "the §14 bar". Repair landed. PASSES.
  - "**in that bar's own tense**" -> now unambiguous. PASSES.
hunk 5:
  - "What counts as such an alteration is **the bar above**" -> replaced with
    "the §14 bar". Repair landed. PASSES.
  - "§21.7 records **the consequence** — that **this** is precisely where..."
    "this" = the rescue case just discussed. PASSES.
hunk 9:
  - "where an item here and **the test above** disagree, the test governs" ->
    resolves to the unwitnessed/detectable paragraphs immediately above the
    block. PASSES.
  - "**Its** companion bar" -> "§20.3 step 4's §14 bar". PASSES.
  - "for the same reason no check knows which ordinal a stored tile used to
    occupy" -> the immediately preceding "the prior generation's declarations
    are not part of the live state". PASSES.

## 9. Exhaustive-claim census (check 5)

  hunk 1  "Of its **two bars**"           — true of §20.3 step 4's two
          declaration bars; §20.3 states other MUST NOTs (step 2's two), so
          true only under the narrow reading the sentence's lead-in supplies.
          Survives.
  hunk 1  "permitted **wherever** it does not" — FAILS against hunk 4. -> X-04
  hunk 1  "The other bar reaches **neither** a shrink nor a growth" — true:
          the ordinal bar's subject is a channel-declaration change, and
          shrink/growth are extent changes. (A growth/shrink DOES move planar
          ordinals via N; that is covered by the re-emission rule's geometry
          parenthetical, not by the bar.) Survives.
  hunk 3  "moves **no ordinal at all**" (append / remove last) — true from
          c·N+s. Survives.
  hunk 3  "An interleaved layer is unaffected, its disk ordinal being s,
          **which no channel declaration enters**" — true. Survives.
  hunk 3  "a growth is permitted **exactly where** the geometry it produces
          satisfies every rule that geometry is subject to" — survives.
  hunk 5  "the §14 bar and **nothing else**, its carve-out included" —
          survives, given hunk 4's narrowing to "what a shrink alters".
  hunk 7  "**exactly where** some file exhibiting it differs" — the ∃∀ form.
          -> X-05
  hunk 9  "**That is the whole of the test**" — survives on its own terms.
  hunk 9  "Detectability is **its negation**" — FAILS. -> X-05
  hunk 9  "**Where the fills differ**, §14.5's padding positions and §14.3's
          pad bits carry the wrong channel's fill and T4 or T5 sees it" —
          FAILS where the layer has no padding position (Eᵢ mod Tᵢ = 0 for
          every i) and no pad bit (no packed planar bool plane with
          P mod 8 ≠ 0). -> X-09
  hunk 9  "unwitnessed for a reason **all three** share" — the three §20.5
          trailer obligations; survives (untouched text).

## 10. Structure census (check 6)

Structure the §14 bar governs: everything §14 fixes for a stored tile's bytes.
Members the list now names: padding-position set; padding content [R-SER-05];
decoded size; in-image sample byte offset; sample type; codec; filter.
Members it does NOT name: §14.3 **pad bits** of a packed planar bool plane,
and [R-SER-08]'s interleaved **boolean byte** values. Both are things §14
fixes for a stored tile, and both are separately registered (T5, T2). The bar
survives because its preamble is open ("the list names where that effect
arises rather than standing on its own") and because hunk 6's Example (c)
names "a padding position and ... a pad bit" as the pair. Recorded, not filed
as a finding.

Structure the ordinal bar governs: the layer's channel declaration list —
count C, order, and per-channel name / sample type / fill. Governed: type
(§14 bar), order and count where a planar stored tile moves (ordinal bar),
fill (§14 bar via padding content and pad bits). Ungoverned sibling: nothing
in the ordinal-bar paragraph, or anywhere else, addresses that **removing a
channel discards its stored tiles into slack** — the exact consequence the
§14 bar's paragraph uses as its ground for sending declaration changes to a
new layer. hunk 3 blesses "removing the last" as an ordinal non-event without
saying so. -> X-10

## 11. Findings (ranked)

X-01 hunk 3   ordinal bar's operative test is in the wrong tense (byte-level)
X-05 hunks 7,9 "Detectability is its negation" — ∃∀ vs ∀∀
X-04 hunks 1,4 §11.1's shrink biconditional vs hunk 4's narrowing
X-02 hunk 1   §11.1 re-typing restatement in the live-generation tense
X-03 hunk 6   §20.3(c) fill prohibition in the live-generation tense
X-06 hunk 3   "such a declaration / such a change" resolve to the carve-out
X-08 hunk 3   "only stated occasion for a renumbering is a geometry change"
X-07 hunk 3   "the whole layer's worth" over-claims after the insertion
X-09 hunk 9   the "fills differ" witness claim is unconditional
X-11 hunks 5,9 hunk 5 cites a §21.7 statement hunk 9 demoted to Rationale
X-10 hunk 3   channel removal blessed without its stranding consequence

## 12. Rejected candidates

- "the layer stores a tile that carries that channel" at 3155 as a standalone
  byte-level defect: dropped, because the very next sentence ("Where the
  superseded generation stored no tile carrying that channel...") supplies the
  quantifier and the colon makes 3165 a gloss on it. Kept only inside X-06.
- hunk 3's claim that a shrink/growth is outside the ordinal bar: dropped.
  A growth does move planar ordinals (N rises), but the bar's subject is a
  *channel-declaration* change, and the re-emission rule's geometry
  parenthetical already covers extent-driven renumbering. Both §11.1 and §20.3
  say the same thing.
- A layout flip (interleaved <-> planar) escaping both bars: dropped. For
  C > 1 the decoded size changes and the §14 bar bites; for C = 1 the layout
  flip changes neither decoded size nor disk ordinal (c = 0 gives s), except
  for bool where P·Q vs ⌈P/8⌉ differ and the §14 bar bites again.
- §11.1's "Of its two bars" as a miscount: dropped. §20.3 step 4 states
  exactly two declaration bars, and the lead-in ("what a commit may do to a
  layer that already stored tiles") bounds "its" to those.
- hunk 4's list of surviving obligations as incomplete (it names only "the
  obligations this step states below", omitting the re-emission rule stated
  above): dropped — hunk 5's tail restates the re-emitted index region
  explicitly two sentences later.
- §23.1's [R-PRV-01] operation list not swept for channel removal: dropped —
  the list is expressly "not offered as closed", and the removal falls in its
  first exhaustive case (bytes travel out of the live state).
