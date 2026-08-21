# Round 18 repair audit — hunk 3 (§20.4 table, MU = 0 / PE = 0 cell)

Auditor scope: hunk-03.diff only. Working transcript, verbatim.

## 0. Disclosure — what I read and ran

Read:

- `/private/tmp/.../round18-audit/hunk-03.diff` (my charter's hunk; nothing else in that directory).
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these ranges:
  - lines 96–235 (§2.1 normative language, §2.2, §2.3 conformance classes, head of §2.4)
  - lines 2891–3100 (§20.3 the append procedure, whole, including its three
    blockquoted examples)
  - lines 3090–3268 (§20.4 whole, §20.5 whole, head of §21.1)
  - lines 3806–3829 (§23.1)
  - lines 4256–4328 (Appendix H, all five checklists)
  - plus every match context printed by the greps below (§5.2 note, §7.2, §7.3,
    §7.4 head, §11.1 note, §21.2–§21.6 rows, §22.3).

Ran: `grep -n` and a python3 whitespace-normalising matcher over `spec/tarn.md`
only (the document is hard-wrapped; every phrase search below was run against a
single-space-collapsed rendering of the file with a char→line map, so a phrase
spanning a line break still matches). Exact patterns and output are transcribed
in §3 and §5 below.

Did NOT read: full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, git history, the web.
I did not list the audit directory. No breaches.

## 1. The hunk

Lands at `spec/tarn.md` line 3117 per the hunk header; the changed table row is
line 3123 in the current file. One row of the §20.4 table changed: the
`MU = 0, PE = 0` cell. Two edits inside it:

(a) `adding or removing a layer` → `adding a layer ... — an appender never
    removes one (§20.4) —`
(b) the supersede carve-out

    > Superseding a stored tile's bytes is not such a change for either kind —
    > it re-places that layer's index region (§20.3, `[R-WRT-04]`) without
    > altering the scope any record attaches to — so a commit whose only change
    > is a supersede MUST retain the record.

    replaced by the opposite

    > Superseding a stored tile's bytes re-places that layer's index region
    > (§20.3, `[R-WRT-04]`) and so modifies that layer's record, which is such a
    > change: an appender superseding a tile MAY drop the record, and the
    > SHOULD-report below is what keeps the loss visible.

Everything else in the cell is untouched context.

## 2. The rule the repair adopts, in my own words

For a record whose type an updater does not implement and whose stored flags are
MU = 0, PE = 0:

- An appender may drop it only in a commit that independently changes the scope
  the record attaches to. (unchanged gate)
- **New:** a commit that supersedes a stored tile's bytes counts as such a
  change, because superseding forces that layer's tile-index region to a new
  placement, which changes the layer record's extent slot, i.e. modifies that
  layer's record — and the gate's own gloss makes "modifying any layer's record"
  a change to the file's layer set. So an appender doing an ordinary tile
  supersede may now drop such a record; previously it was expressly forbidden to
  in a supersede-only commit.
- **New:** an appender never removes a layer, so "removing a layer" is struck
  from the list of qualifying changes.

What it makes true of an implementation: an appender that supersedes one sample
of one tile of one layer may, in that same commit, silently delete an unknown
ancillary record from the live directory, subject only to a SHOULD to report.
That is the commonest commit shape in the format, so the licence went from
"rare" to "essentially always".

## 3. Check 1 — TENSE AND QUANTIFIER

### 3.1 Generation

The cell speaks about the commit being written and the record as it stands in
the superseded generation. No generation-sensitive predicate ("a tile the file
stores") appears in the new text — "Superseding a stored tile's bytes" is the
operation, not a set. §20.3's tense traps (`in the generation this commit
supersedes`, lines 2953, 2975, 2993–3004) are about the *declaration* bar, not
about record drops, and the repair does not touch them. **No tense defect.**

### 3.2 The set the new licence ranges over — DEFECT

The gate, verbatim (line 3123):

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record, the
> entry set of its index, or which of its tiles are stored; for a top-level
> record, the file's layer set — which a commit changes by adding a layer and
> equally by modifying any layer's record — an appender never removes one
> (§20.4) — or another *non-layer* top-level record.

Note the gate is **scope-matched and kind-split**:

- layer sub-record → the qualifying change must be to **that** layer (its
  record, its index's entry set, which of **its** tiles are stored);
- top-level record → the file's layer set (glossed to include modifying **any**
  layer's record) or another non-layer top-level record.

The repair's premise is "Superseding a stored tile's bytes ... modifies that
layer's record". Run that premise through the gate:

| record being dropped | does the premise satisfy the gate? |
|---|---|
| a top-level unknown record | yes — the gloss says modifying **any** layer's record changes the file's layer set |
| an unknown sub-record of layer A, tile superseded in layer A | yes — "that layer's record" |
| an unknown sub-record of layer **B**, tile superseded in layer **A** | **no** — nothing about B's record, B's index entry set, or B's stored-tile set changed |

The repair's conclusion is stated with no such restriction:

> an appender superseding a tile MAY drop the record

"the record" is the row's subject (the unknown MU = 0 / PE = 0 record), and the
sentence quantifies over none of the three cases. Read on its own it licenses
row 3 of that table — dropping layer B's unknown sub-record in a commit that
only touched layer A. The premise it is derived from does not support that.

This is exactly the "which set does it range over" shape: the deleted text was
explicitly kind-quantified ("is not such a change **for either kind**"); the
replacement dropped the quantifier and asserted an unqualified BCP 14 `MAY`.

I looked for a reading that rescues it. The best one is that the colon makes the
clause a derivation from the gate, so the gate's scope-matching is carried
implicitly. That is the charitable reading, and a careful implementer will reach
it. But the sentence's own conclusion is broader than its own premise, and the
one word that would have fixed it ("for that layer" / "such a sub-record of that
layer") is absent, while the deleted sentence had carried the equivalent word.
`MAY` is an ALL-CAPS BCP 14 permission (§2.1, line 98–102) and the restriction
that is supposed to bound it is two sentences earlier and lowercase.

**Finding B-01.**

### 3.3 The quantifier of the normative rule being restated

The repair IS the normative rule — there is no other statement of the appender
drop licence anywhere in the document. Confirmed by the greps in §5: the only
lines in the file that state when an appender may drop a record are inside line
3123. §21.6's row (line 3527) restates only "Ignored, and preserved or dropped
per its PE bit" and states no commit-shape condition; §20.5's lines 3153/3163
delegate to "§20.4's table" and add nothing.

## 4. Check 2 — CITATIONS RESOLVE

Every identifier and section number in the repaired text, opened and read.

### 4.1 `(§20.3, [R-WRT-04])` — for "Superseding a stored tile's bytes re-places that layer's index region" — **PASSES**

§20.3 line 2903: "An appender MUST, in order:" — a normative numbered list whose
requirement tag `[R-WRT-04]` sits at its end (line 3026). Step 4, lines
2937–2941:

> Every layer whose stored-tile set or index content this commit changes has its
> tile-index region re-emitted in full — entry_count entries plus the segment
> CRC array — necessarily at a new placement (`[R-LIF-01]`), with entries for
> tiles this commit stores or supersedes written to their new state

A supersede changes index content (the entry's offset at minimum, since
`[R-LIF-01]` freezes the committed prefix and the new payload lands at or after
F). So the region is re-emitted at a new placement. The claim is stated as a
rule, in normative text, under the cited identifier. Verdict: **resolves, and it
is a rule, not an implication.**

### 4.2 The uncited half of the same sentence — "and so modifies that layer's record"

This is the decisive link — it is what makes the supersede qualify under the
gate — and the citation `(§20.3, [R-WRT-04])` sits before it, covering only the
re-placement. §20.3 does not say the layer record is modified. What establishes
it is §7.4, line 1002:

> A layer record's extent slot addresses the layer's tile-index region (§15)

plus §20.3's contrapositive-shaped line 2946–2949 ("A layer whose record alone
changes keeps its extent slot, pointing at the existing region"). Neither is
cited. The inference is sound — new placement ⇒ new extent_offset ⇒ the record's
bytes differ ⇒ it is modified, and additionally crc_of_crc_array changes when a
segment CRC does — and I could not construct a counterexample: an appender
cannot re-place a region onto its old offset without violating `[R-LIF-01]`, and
a layer with no index region has no stored tile to supersede. So the chain
**holds for every layer and every commit shape**, not only the common case. But
the load-bearing step is uncited while the trivial step carries two citations.
Reported at low severity as part of **B-05**.

### 4.3 `(§20.4)` in "an appender never removes one (§20.4)" — resolves, but it is a self-citation

The cell is *in* §20.4. `grep -n "§20\.4" tarn.md` returns 15 lines; line 3123 is
the only one inside §20.4 itself. The claim is true and is grounded in §20.4 —
line 3109–3112 ("both registered types carry PE = 1, so neither can be dropped")
and the post-table paragraph line 3125 ("No commit therefore removes a layer
record, or a user-metadata record at either scope") — both normative, neither in
a `>` block. §23.1 line 3809 restates it ("no commit removing a layer at all
(§20.4)"). So the claim stands. The pointer, however, sends the reader to the
section they are already reading, and the nearest supporting sentence is a
"therefore" derived from the table the pointer was issued from. `[R-CNT-22]`
and §7.3 are the real ground and are cited elsewhere in the same subsection but
not here. Reported at low severity as part of **B-05**.

### 4.4 Citations elsewhere in the (unchanged) cell, re-checked because the cell changed around them

- `[R-WRT-06]` (MU = 1 row, "Compaction is barred on the same ground") — §20.5
  line 3179–3182 does bar a compactor from a file carrying an unimplemented
  MU = 1 record. **Passes**, untouched.
- `[R-CNT-18]`, `[R-CNT-15]`, `[R-CNT-12]`, `[R-CNT-22]`, §6.3, §7.3, §2.3 in the
  surrounding prose — all untouched by the hunk; I opened §7.2 (line 920–925),
  §7.3 (line 993–998) and §2.3 (line 184–188) and each says what the cell claims.
  **Pass.**

## 5. Check 3 — THE REPAIR SITS IN NORMATIVE TEXT

§2.1 line 104–106: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative. `[R-CNF-01]`"

The repaired cell is a table row in §20.4 body text. Not a `>` block, not
labelled Note/Example/Rationale, not an appendix. Line 3123 begins with `|`, not
`>`. **The repair is normative and it landed in normative text.** No
`>`-block-only rule here, and no stale normative twin: the greps below show the
old carve-out has no surviving statement anywhere.

Greps run (whitespace-normalised, whole file), with the material output:

```
pattern "MUST retain"        -> 1 hit, line 3123 only
pattern "such a change"      -> 2 hits: line 2973 (§20.3 declaration bar, unrelated
                                sense) and line 3123
pattern "supersed\w* [a-z ]{0,40}retain" -> 0 hits
pattern "drop"               -> 1487(§11.1 Note, tiles), 2922(§20.3 step 2),
                                2993/3012(§20.3, tiles), 3110/3112(§20.4 prose),
                                3123(the cell, 6x), 3144(§20.4 Rationale),
                                3153/3162/3164/3166(§20.5), 3527(§21.6 row)
pattern "may drop"           -> line 3123 only (3 occurrences)
pattern "MUST NOT drop"      -> line 2922 only
pattern "index region"       -> 30 hits; the ones bearing on the chain are 607-610
                                (§5.2 Note), 1002 (§7.4), 1991 (§15.1), 2938/2949
                                (§20.3 step 4), 3123 (the cell)
pattern "layer set"          -> line 3123 only
pattern "PE = 0"             -> 920, 925, 997, 3117, 3123, 4307
```

## 6. Check 4 — CONTRADICTION IN THE SAME PASSAGE, INCLUDING UNTOUCHED TEXT

I read the whole cell, both other rows, the prose above the table (3101–3117),
the paragraph below it (3125–3133), the `[R-WRT-08]` paragraph (3135–3139), the
Rationale block (3141–3147), and all of §20.5.

### 6.1 The stranded "either" — DEFECT

Next sentence in the cell, untouched by the repair:

> Dropping the record, or dropping another record in the same commit, is not
> itself such a change **either**, so a commit whose only effect would be the
> drop MUST retain it.

"either" is an additive negative particle: it requires a preceding negative
statement of the same shape. Its antecedent was the deleted sentence
("Superseding a stored tile's bytes **is not such a change** for either kind").
The sentence that now precedes it is affirmative — "which **is** such a change".
Likewise "not **itself** such a change" was drawing a contrast with the
supersede case that no longer exists.

The rule the sentence states is still correct and still unambiguous on its own
terms. What is damaged is the reader's search: "either" now points at nothing,
and a reader trying to resolve it will look upward, land on "which is such a
change", and have to decide whether they have misread one of the two. This is
the classic stranded-connective signature of a deletion that was not swept
through the sentences written around it. It costs nothing to fix ("is not itself
such a change, so a commit whose only effect...").

**Finding B-02.**

### 6.2 Contradictions I looked for and did NOT find

- **Within the cell.** The gate's layer-sub-record list ("that layer's record,
  the entry set of its index, or which of its tiles are stored") does not
  collide with the new licence: a supersede changes none of the other two (same
  entry set, same stored-tile set), and the ground the repair uses — "that
  layer's record" — is the first list item. Consistent.
- **The "*independently*" italic.** The gate requires the scope change to be
  independent of the drop. A supersede is independent of the drop. Consistent.
- **The drop-only carve-out.** Still coherent after the widening: a commit whose
  only effect is the drop still has no independent change, so "MUST retain"
  still bites. The repair did not swallow it.
- **`[R-WRT-08]`, line 3135–3139**: "An updater MUST NOT re-encode a record whose
  type it does not implement, and MUST NOT modify one except by relocating its
  extent and re-pointing its slot under §20.5." Dropping is neither re-encoding
  nor modifying; the paragraph does not bite on a drop. No collision.
- **The paragraph below the table** (3125–3133) is entirely about layer records
  and user-metadata records, both PE = 1. The widened MU = 0 / PE = 0 licence
  cannot reach them. No collision.
- **§20.5** (3151–3182): "less any record §20.4 lets it drop", "only where
  §20.4's table licenses it", "Where the table does not license a drop the
  compactor MUST refuse." All of these delegate to the table and are indifferent
  to which commits license an *appender*. The cell's own "A compactor may drop it
  whenever it rewrites the file" is untouched and still wider than the appender
  licence, as before. No collision.
- **§2.4 preserve-verbatim row** (line 241): "§20.4's table states the cases: its
  MU = 1 and MU = 0 / PE = 1 rows." A closed two-item enumeration that excludes
  the MU = 0 / PE = 0 row. That exclusion was there before the repair and the
  repair, which widens the drop licence, makes the exclusion *more* apt, not
  less. Not a repair defect; not reported.
- **§20.3 step 2, line 2920–2923**: "Against any other structure the appender
  carries forward, it MUST NOT repair the defect ... and MUST NOT drop the
  record (§20.4)." I probed this hard as a candidate MUST/MAY collision. Under
  the reading that makes it non-vacuous — an appender may not dispose of a
  *defect* by dropping the record, in contrast with §20.5 where "Dropping is the
  one disposal that answers" — it does collide with §20.4's MAY. But it collided
  equally under round 16's text (an appender adding a layer could already drop),
  so the repair did not create it; it only enlarged the commit shapes in which it
  bites. I judged it out of scope for a *repair* audit and do not report it as a
  finding. Flagging it here so a maintainer sweeping §20.3 knows it is live.

### 6.3 The overclaim that carries the widening — DEFECT

> ... which is such a change: an appender superseding a tile MAY drop the
> record, **and the SHOULD-report below is what keeps the loss visible.**

The SHOULD below is "An updater that drops such a record SHOULD report the loss;
unreported, application state disappears with no diagnostic." A SHOULD does not
keep anything visible — by BCP 14 an implementation may deviate with reason, and
the cell itself spells out that the deviating case is exactly the invisible one.
So the clause asserts, in normative text, a guarantee that the cited obligation
cannot carry, and it does so in the position of the justification for the
widening. Before the repair, the invisible-loss case was structurally rare
(drops needed a layer add or a non-layer record edit); after it, the commonest
commit in the format can silently delete an unknown record, and the sentence
that says this is fine is leaning on a SHOULD. Either the clause should be
softened ("the SHOULD-report below is the mechanism by which the loss is meant
to surface") or the report obligation should be a MUST for this case — the
latter is a maintainer's decision, not an editorial one.

**Finding B-03.**

## 7. Check 5 — EXHAUSTIVE CLAIMS

Words in the repaired text that promise completeness, each tested:

- **"never"** in "an appender never removes one (§20.4)". Tested: §20.4 line
  3125 "No commit therefore removes a layer record", grounded in `[R-CNT-22]`
  (registry-fixed flags, both registered types PE = 1) and §7.3's registry row
  for the layer type. §23.1 line 3809 restates it. Could not falsify. **Holds.**
- **"any"** in "modifying any layer's record" — unchanged from round 16, and the
  broadest reading is the one the repair relies on. **Holds** (it is a
  stipulation, not a claim).
- **"is what keeps the loss visible"** — a definite description asserting the
  SHOULD is *the* mechanism and that it succeeds. Falsified above: a conforming
  appender may drop and not report. → **B-03**.
- **"an appender superseding a tile MAY drop the record"** — an unrestricted
  universal over records. Falsified by the layer-B sub-record case. → **B-01**.
- No counts, no closed lists, no "the two X" constructions in the repaired text.

## 8. Orphan sweep — did deleting the carve-out strand anything?

I searched for every restatement of the deleted sentence and for anything that
depended on it.

- **Register (§21.2–§21.5).** No row states a record-drop condition. The only
  register-side mention of dropping is §21.6 line 3527, a *not-a-violation* row:
  "A record type this specification has not assigned, from the experimental
  range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
  per its PE bit". That row states no commit-shape condition and is therefore
  neither orphaned nor now-wrong. **Clean.**
- **Appendix H, conforming-updater checklist** (lines 4292–4300). Its four
  §20.4 clauses are: re-emit every retained record byte-identically; respect MU
  and PE bits; never remove a layer record or a user-metadata record at either
  scope; never modify a scope governed by an unknown critical record. None
  restates the supersede carve-out. **Clean** — and correctly so, since the
  repair did not change any of those four.
- **§20.3's examples** (blockquotes 3036–3043 and 3045–3097). The supersede
  example says "the new directory (every record byte-identical except the
  modified layer's)". That is a description of one concrete commit, not a claim
  that no record may be dropped, and it is non-normative anyway. It does not
  become wrong; it merely no longer illustrates the only permitted shape.
  **Clean, but worth a maintainer's eye** — a reader who takes the example as
  exhaustive will now be surprised. Not reported: it was already an example, not
  an enumeration.
- **§5.2's note** (lines 602–610) — about index re-placement, says nothing about
  record drops. **Clean.**
- **§22.3** (line 3757) — "§20.4's byte-identical re-emission (`[R-WRT-05]`)
  carries such an extent forward unread". Still true of a *retained* record.
  **Clean.**
- **§23.1** (lines 3808–3810) — NOT clean, see below.

### 8.1 §23.1 was not swept — DEFECT

> The append-only model (§9.1) means a commit that supersedes data — **the only
> removal a commit performs**, no commit removing a layer at all (§20.4) —
> removes only that data's *reachability*

§23 is normative text (not §1, not a Note/Example/Rationale, not an appendix),
so this is a normative claim: superseding data is the only removal a commit
performs. Under the repaired §20.4 a commit also removes an unknown
MU = 0 / PE = 0 record from the live state — its extent becoming slack, which is
precisely §23.1's subject matter, and the cell itself says "application state
disappears" when this happens unreported.

Honest framing: this claim was already loose under round 16's text, because a
layer-adding commit could already drop such a record. What the repair changes is
that the second kind of removal now occurs inside the exact commit shape §23.1's
sentence is describing — a supersede commit — so the appositive now reads as
directly false of the sentence's own subject. §23.1 is also the one place in the
document that reasons about what disappears from reachability and what stays as
slack, which makes it the place a maintainer would expect the sweep.

Repair: "— the removal a commit most often performs, and the only one that
removes sample data; no commit removes a layer at all (§20.4), and §20.4's table
governs the one other removal, the drop of an unknown ancillary record —" or
similar. A maintainer's wording call; the defect is that the sentence says
"only" and the repair made a second case ordinary.

**Finding B-04.**

## 9. Overshoot / undershoot

- **Overshoot:** yes, in the quantifier (B-01) — the licence as written reaches
  further than the reasoning that justifies it. The *direction* of the repair is
  not an overshoot: round 16's cell was internally inconsistent (the gate's own
  gloss made "modifying any layer's record" qualify, while the carve-out said a
  supersede — which does modify a layer's record — does not), and resolving in
  favour of the gloss is a coherent choice.
- **Undershoot:** the (a) edit — striking "removing a layer" — is exactly sized
  and matches line 3125 and §23.1 line 3809. No undershoot there.

## 10. Byte-level determinations

- **B-01: byte-level.** Two conforming appenders, given the same input file
  (layer A with a stored tile, layer B carrying an unknown experimental
  MU = 0 / PE = 0 sub-record) and the same instruction (supersede one tile of
  A): implementation X reads the unqualified `MAY` and emits generation n+1 with
  B's sub-record absent from the directory and its extent reclassified as slack;
  implementation Y applies the gate's scope match and emits generation n+1 with
  B's sub-record re-emitted byte-identically. The two directories differ by that
  record's 24-byte header plus its inline payload, and the dir_length and
  directory CRC differ accordingly. The discriminating question: **is X's file
  conforming?** Yes — a file with one fewer unknown ancillary sub-record trips no
  §21.2–§21.5 row (grep confirms no row keys on record presence), so `[R-CNF-05]`
  does not bar it and the two readings genuinely differ on what a conforming
  appender may emit. The emittable set moves.
- **B-02: not byte-level.** A stranded connective. Both readings of "either"
  leave the same rule ("a commit whose only effect would be the drop MUST retain
  it") in force.
- **B-03: not byte-level** on its own — it is an assertion, not an obligation,
  and the SHOULD it describes is unchanged. It becomes byte-level only if the
  maintainer resolves it by promoting the report to a MUST, and even then the
  report is out-of-band, not bytes on disk.
- **B-04: not byte-level.** `[R-PRV-01]`'s MUST NOT is about representation to
  users, not about emitted bytes; the appositive is descriptive.
- **B-05: not byte-level.** Citation hygiene; both claims are true and both
  resolve within the document.

## 11. Verdict

The repair does what it claims and lands in normative text. Its central chain —
supersede ⇒ index region re-placed ⇒ layer record modified ⇒ qualifying change —
holds at every link, for every layer and every commit shape, and I could not
break it. But the conclusion it draws is stated one quantifier wider than the
premise supports (B-01, byte-level), the deletion stranded the connective in the
following sentence (B-02), the clause carrying the widening leans a guarantee on
a SHOULD (B-03), and the sweep missed §23.1 (B-04). B-05 is citation hygiene.

Findings: B-01 (byte-level), B-02, B-03, B-04, B-05.
