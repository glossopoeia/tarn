# Audit transcript — "the drop" (hunks 06, 07, 13, 14, 15, 17, 19, 26)

## Disclosure of context contamination

Before any spec/hunk reading, my context already contained, via system-reminders I did not request:

- The project's `MEMORY.md` index, whose entries include titles that directly describe this
  round's subject matter, e.g. "TARN repair prose vs rules — where this project's repair
  defects actually live", "TARN closed-list exceptions compose — check the pairs, not only the
  members, and every restatement", "No nested em-dash phrases", "TARN repair list vs diff".
- A `gitStatus` block naming the five most recent commit subjects on `main`, including
  `38dc23d ADR-0130's erratum decision E2 confirmed; §7.2 notes that MU and PE are not
  orthogonal` and `f61f2aa ADR-0130's erratum decision E1 confirmed` — this names, almost
  verbatim, the content and the *disposition* ("confirmed") of the §7.2 Note that is exactly
  hunk-06's subject.
- `CLAUDE.md`'s pointer to `AGENTS.md` (not read, per the access rule).

None of this was used as evidence. Where it overlapped with a conclusion I reached (hunk-06's
Note), I re-derived that conclusion independently from R-CNT-12, the §20.4 table text, and
[R-CNF-01]'s label rule, before consulting what the commit-subject implied, and I deliberately
re-opened the Note a second time skeptically (looking for a check-3 label violation) precisely
because the contamination told me it had been "confirmed" — a fact that should not lower my
guard. I flag this per the brief's disclosure requirement; it is a disclosed breach, not an
acted-on one.

## Setup

Read (full): spec/tarn.md — §5.2 (698–781), §6.1 (782+, spot), §7.1 tail (990–1006), §7.2
(1007–1095), §7.3 (1096–1120), §7.4 (1121–1189), §20.3 step 4 in full context (3188–3330),
§20.3's three-shapes Example (3395–3474), §20.4 in full (3476–3550), §20.5 in full (3552–3728),
Appendix H's Conforming-file/reader/writer/updater/verifier entries (4882–4980), §23.1
(4353–4390 area), the "Conforming reader/writer/updater/verifier" definitions in §2.3 (180–260).

Read (full): all eight hunk files named in the charter, verbatim, before opening the spec.

No other files read. Did not read full.diff, other hunk files, docs/, AGENTS.md, registry.json,
git log/diff, or the web. Did not list the case/ directory.

## Hunk header sanity check

For each hunk, I compared its stated "lands at lines NNNN–NNNN" / "nearest preceding heading"
against the current file and the hunk body's own content:

- hunk-06: claims landing 1036–1042, heading "7.2 Record framing" (line 1007). Confirmed: the
  Note now sits at 1036–1041 in the current file, directly under §7.2. Match.
- hunk-07: claims landing 1056–1062, heading "7.2 Record framing". Confirmed: edited text sits
  at 1056–1061. Match.
- hunk-13: claims landing 3293–3301, heading "20.3 The append procedure" (3188). Confirmed: the
  "bar binds a layer the commit keeps" sentence sits at 3293–3301, inside step 4. Match.
- hunk-14: claims landing 3488–3489, heading "20.4 Re-emission and preservation" (3476).
  Confirmed at 3488–3489. Match.
- hunk-15: claims landing 3506–3526, same heading. Confirmed — MU=1 row edit at 3506, new
  paragraph 3510–3526. Match.
- hunk-17: claims landing 3582–3583, heading "20.5 Rewriting" (3552). Confirmed. Match.
- hunk-19: claims landing 3655–3656, same heading. Confirmed. Match.
- hunk-26: claims landing 4940–4953, heading "Appendix H" (4882). Confirmed. Match.

No header/body disagreement found in any of the eight hunks.

---

## Hunk-06 — §7.2's new Note (MU/PE not orthogonal)

**Rule the repair asserts.** The Note claims: (a) [R-CNT-12] leaves a record only three
*effective* flag-states, not four raw combinations, because MU=1 forces the effective PE to 1
regardless of the stored bit; (b) those three states are exactly §20.4's three table rows; (c)
consequently PE only varies meaningfully when MU=0; and (d) an updater that does not implement
an MU=1 record's type can never drop that record, whether alone (leaving its governing scope
otherwise unmodified) or together with the scope it governs.

**Check 3 — label vs. marker.** The block is headed `> **Note.**` — under [R-CNF-01] this is
explicitly non-normative. I therefore checked whether any clause in it is the *sole* statement
of a rule the document otherwise never states normatively (a real check-3 defect), versus a
correct restatement of a rule stated elsewhere in unlabeled (normative) text.

- Clause (d) ("never drops the record, alone or with the scope it governs") restates the §20.4
  table's MU=1 row, which — after hunk-15's edit — reads: "The updater MUST NOT modify the scope
  the record governs. At layer scope an unknown critical record blocks modification of that
  layer, its drop included..." That row sits in an ordinary Markdown table cell, not inside any
  `>` block — normative text per [R-CNF-01]. "Modify the scope" already covers dropping the
  record alone (dropping a sub-record from a layer it governs is a modification of that layer);
  "its drop included" (hunk-15) covers dropping the whole scope. Both halves of the Note's claim
  (d) are independently grounded in unlabeled, normative table text. **Not a check-3 violation.**
- Clauses (a)–(c) are commentary/arithmetic over R-CNT-12 and the table, not new rules. No
  normative content originates solely in this Note.

**Check 2 — citations resolve.**
- `[R-CNT-12]` (1020–1034): "Writers MUST NOT emit the combination MU = 1 with PE = 0; a reader
  or updater encountering it MUST treat the record as PE = 1 (never silently deletable)." This
  supports "PE bit is read as 1 whatever is stored" when MU=1 (stored PE=0 is forced to 1; stored
  PE=1 is already 1) — accurate for both sub-cases. Verified, PASS.
- §20.4's table (3504–3508): three rows, MU=1 / MU=0,PE=1 / MU=0,PE=0 — matches "§20.4's three
  rows" exactly. Verified, PASS.
- §20.4 (cited parenthetically for clause (d)): verified above. PASS.

**Check 1 — tense/quantifier.** "An updater that does not implement an MU = 1 record's type" —
this correctly matches the table's own scoping sentence: "Its MU = 1 row reaches only a type the
updater does not implement... so for an implemented type only the PE bit bites." I checked the
Note against an MU=1 record of a type the updater *does* implement (per the charter's
instruction): the Note is silent about that case, and correctly so — it never claims anything
about an implemented MU=1 type, so there is no overreach into the case the table itself carves
out of the MU=1 row.

**Check 4 — contradiction in the passage.** None found: the Note's claims track the table before
and after hunk-15's edit without conflicting with the MU=0/PE=1 or MU=0/PE=0 rows, or with
§7.3's registry-flags-govern rule ([R-CNT-22]).

**Check 5 — exhaustive claims.** "three states, not four" — verified true (see check 2). "whatever
is stored" — verified true for both raw PE values under MU=1. "never drops... alone or with the
scope" — verified against the table, true given the table's own MU=1 scoping.

**Check 8 — anaphora.** The Note is inserted between two normative sentences (the [R-CNT-12]
closer above it, and "The **extent slot**..." below it). Read forward: no back-reference in the
following text ("The extent slot (extent_offset, extent_length)...") depends on anything in the
Note; it is a fresh topic sentence with its own noun phrase. No re-resolution found.

**Verdict:** no defect. Passes all eight checks I could apply. (See "second look" note above:
I re-ran check 3 specifically because contaminated context told me this repair was "confirmed";
the independent re-derivation still finds no violation.)

---

## Hunk-07 — §7.2's layer-record exception

**Rule the repair asserts.** Before: the layer record's tile index was offered as an instance of
"records with MU=1 carry further references" — but the registered layer type is MU=0, PE=0
(§7.3 table), so that framing misclassified it. After: the layer record is separated out as "the
one exception" to the general MU=0 rule ("the extent slot is its only sanctioned reference..."),
justified because (i) the tile index is this specification's own defined structure and (ii)
every conforming reader/updater implements the layer type, so no one ever meets it "as an
unknown ancillary."

**Check 2 — citations resolve.**
- `[R-CNF-03]` (line 196, "Conforming reader" bullet): "...and both record types §7.3 registers.
  There are no subset profiles..." — supports "every conforming reader... implements the type."
  For "and updater": [R-CNF-03] itself is a *reader* requirement. The updater half of the claim
  is supported instead by a separate, uncited sentence under "Conforming verifier" (line 217–218):
  "Verifiers and updaters are readers of the files they process and inherit every reader
  obligation." **Finding A-05** — the citation covers the reader half fully but not the updater
  half; the claim is true, but the sole cited authority ([R-CNF-03]) does not itself say
  anything about updaters. Not byte-level (the claim is correct; only the citation is
  incomplete).

**Check 6 — what else does this structure carry that the sentence doesn't name?** I enumerated
every reference to other file bytes a layer record's inline payload can carry: (1) the layer
record's own extent slot → tile-index region; (2) the tile-index region's entries → stored-tile
extents (the case the sentence names); (3) each sub-record nested in the inline payload has its
own, separate extent slot (§7.2 framing applies recursively to sub-records). I checked whether
(3) is a second, unaddressed exception to the general MU=0 rule. It is not: the general rule
("the extent slot is its only sanctioned reference... for a record with MU=0") is stated
per-record, and a sub-record is itself a distinct record under the same rule, individually
budgeted its own single extent slot — not an additional reference smuggled into the *layer
record's own* inline-payload/extent-content budget. The "one exception" is specifically about
the layer record's own extent *content* (the tile index) encoding further offsets, which no
ordinary MU=0 record's extent content does. Checked, no gap found (rejected candidate).

**Check 3 — label.** Unlabeled body text (not inside a `>` block). Normative, and the repair
lands in normative text. The paragraph after the insertion ("Records with MU = 1 carry further
references only where..."; "Extents are owned exactly once...") still reads coherently — checked
per the charter's explicit instruction to verify the trailing sentences still read.

**Check 8 — anaphora.** Read forward from the insertion to the paragraph's end ("...no two
structures overlap; a verifier MUST treat an intra-layer overlap... [R-CNT-13]"). "it" in the
untouched preceding sentence ("...without parsing it (§20)") resolves within its own sentence
(to "an unknown ancillary's extent"), unaffected by the insertion which follows it. "none" in the
inserted text resolves to "every conforming reader and updater" in the same sentence. No stranded
pronoun found.

**Verdict:** one citation-completeness finding (A-05), non-byte-level; otherwise passes.

---

## Hunk-13 — §20.3 step 4's scope sentence

**Rule the repair asserts.** Old: "The bar binds the layer's identity and nothing else." New:
"The bar binds a layer the commit *keeps* and nothing else" — i.e. the fixed-declarations bar
(§20.3 step 4) applies only to a layer the commit retains, not to one it drops-and-replaces under
the same name; a re-declared "new" layer is new "whatever bytes its entries address, the dropped
layer's former extents included"; and "no byte tells the two apart" between a legitimate
re-declaration-as-new-layer and an illegitimate continuity fiction, which the repair offers as
*why* this is an actor-binding rule with no register row, not a file-conformance condition.

**Check 6/7 census of "keeps."** Every other use of "keeps" in step 4 (3249, 3256, 3273, 3292)
has the *layer* (or "the new state") as subject, retaining one of its *own* properties
(extent slot, declarations, channel position). Hunk-13's new usage, "a layer the commit keeps,"
flips subject/object: the *commit* is the actor, the *layer* is what is kept-or-dropped as a
whole entity. Grammatically this is unambiguous on its own ("a layer [that] the commit keeps"
cannot parse as "a layer that keeps X"), so I do not find a genuine parsing hazard, but the
polysemy is real and I record it as checked (rejected candidate, not filed as a finding).

**Check 5 — exhaustive claim, tested against hunk-15.** "no byte tells the two apart" is stated
without qualification, immediately following "What the bar removes is a re-declaration carried
as the same layer over the tiles it stored." I tried to falsify it with a layer carrying a
sub-record, per the charter's explicit instruction, using hunk-15's own new rule (3516–3518):
"A commit never removes a user-metadata record from a scope it keeps: a top-level one from the
file, or a sub-record from a layer the commit retains." Consequence: if layer L carried a
user-metadata sub-record before a commit, and after the commit a same-named layer L′ carries no
such sub-record, then per hunk-15's own rule L′ *cannot* be "the same, kept" L (keeping it would
forbid removing the sub-record) — it must be a genuinely new, dropped-and-replaced layer. That is
exactly a byte (the sub-record's presence/absence) telling the two apart, for any layer that ever
carried a PE=1 sub-record. **Finding A-01.**

**Check 8, "which is the sense in which."** The untouched paragraph above (3276–3282) already
gives an independent, structural reason the bar binds the commit as an actor rather than the
file: the error register (§21.1) enumerates only file-conformance violations, and "the bar
stat[es] no condition a file can exhibit" (§21.7, [R-ERR-01], [R-CNF-02]) — a claim that does not
depend on byte-detectability at all. Hunk-13's new clause offers a second, narrower,
*empirical* warrant ("no byte tells the two apart") for the same conclusion. Since (per check 5)
that empirical warrant is false in the sub-record case, but the structural warrant above is
independent of it and still holds unconditionally, the ultimate conclusion ("makes no file
nonconforming") is unaffected — but the sentence attached the wrong, falsifiable reason to it, in
the same passage as a sibling rule (hunk-15) that falsifies it. Classified as **OVERCLAIM**
(check 5) with a **LOCAL_CONTRADICTION** component against hunk-15 (check 4) and a **check-7**
component (the new clause's warrant — a claim about what the *bytes* show — is not the same
quantifier as the paragraph-above's warrant — a claim about what the *register* enumerates — so
grafting one as "the sense in which" the other holds conflates two different grounds).

**Byte-level test.** The disputed premise is explanatory prose feeding a conclusion that is
independently, definitionally secured (register scope + §21.7) regardless of the premise's
truth. No conforming writer's emittable byte set, and no verifier's accept/reject verdict, turns
on whether "no byte tells the two apart" is true. **Not byte-level.**

**Other clauses checked, no issue found:**
- "the new layer being new whatever bytes its entries address, the dropped layer's former
  extents included" — under append-only writing (F only grows), a newly-appended layer's stored
  tiles cannot physically coincide with a dropped layer's former (stranded) extents in the same
  commit; the clause reads as a defensive, always-true generalization rather than a claim about
  an actually-occurring scenario. No falsification found.
- "§5.2's partition being over the new state alone" — consistent with §5.2's own definition of
  coverage as a property of "the live committed state" (the current generation only). No
  contradiction found.

**Verdict:** one real finding (A-01), non-byte-level; other clauses checked and pass.

---

## Hunk-14 — §20.4's flags paragraph (user-metadata drop condition)

**Rule the repair asserts.** Old: "...the user-metadata record PE = 1 and never [dropped]." New:
"...the user-metadata record PE = 1 and is dropped only with a layer that carries it" — narrowing
"never" to "never, except as a side effect of its containing layer's drop."

**Check 1 — quantifier, held against a top-level user-metadata record (per the charter).** The
user-metadata type occurs in two scopes (§7.3: "file when top-level; layer as sub-record"). The
sentence states the drop condition once, generically, for "the user-metadata record" — worded
identically for both scope-instances. For the sub-record instance the new wording is accurate
(verified against hunk-15, 3516–3518). For the *top-level* instance, "dropped only with a layer
that carries it" is vacuously true only because no layer ever carries a top-level record — i.e.
it is logically consistent (the condition can never be satisfied, so a top-level record is never
dropped) but the sentence does not separately say so, forcing the reader to notice the
scope-distinction and resolve it via the immediately following paragraph (hunk-15) rather than
from this sentence alone. **Finding A-04**, category NEW_AMBIGUITY: the general noun phrase
"the user-metadata record" is used to state a condition that is really scope-specific, echoing
the tense/quantifier failure-shape the charter describes ("a tile the new state stores" vs. "a
tile the superseded state stored" — here, "a user-metadata sub-record" vs. "a top-level
user-metadata record").

**Check 4 — held against §20.4's MU=0,PE=1 table row (unmodified) and by-rewrite behavior.** The
row itself ("Retain byte-identical, extent content unmodified") forecloses dropping *any* PE=1
record — top-level or sub — independent of hunk-14's added clause, and this applies to both
commit and rewrite (the row is actor-neutral). So under either reading of hunk-14's sentence, no
byte-level fork results: a top-level user-metadata record is never droppable by any actor, by the
table row alone. **Not byte-level.**

**Verdict:** one ambiguity finding (A-04), non-byte-level.

---

## Hunk-15 — §20.4's MU=1 row and post-table paragraph (the hunk to read hardest)

**Rule the repair asserts.** (1) MU=1 row: an unimplemented critical sub-record now explicitly
blocks *dropping* its containing layer, not just other modification. (2) New paragraph: a
layer's drop takes all its sub-records and their extents with it "whatever their PE bits" —
except an unimplemented-MU=1 sub-record, which blocks the drop entirely, because the drop is
itself "a modification of the scope it governs" (the layer, per row 1). (3) A commit can never
remove a user-metadata record from a scope it *keeps* (top-level from the file, sub-record from
a retained layer) — only from one it drops. (4) Stranding on a layer-drop now explicitly
includes the tile-index region and sub-records' extents, not just stored tiles. (5) Reporting a
layer-drop's loss is downgraded from an unqualified "reports the loss" to "SHOULD report... as
the table says of any record dropped," aligning it with the table's own advisory phrasing.

**Check 6 — enumerate every sub-record kind, what a layer-drop does to it, what its sentence is.**

| Sub-record kind | Layer kept | Layer dropped | Deciding text |
|---|---|---|---|
| user-metadata (registered, MU=0,PE=1) | Retained byte-identical (table row 2); may be *edited* (new extent) but not removed (3516–3518) | Goes with the layer, extent → slack, regardless of PE=1 (3510–3513) | Table row 2 + new paragraph + hunk-14 |
| unimplemented type, MU=0,PE=1 | Same as above (stored flags authoritative, table row 2) | Same — goes with the layer (3512–3513, "whatever their PE bits") | Table row 2 + new paragraph |
| unimplemented type, MU=0,PE=0 | MAY be dropped individually or retained (table row 3) | Goes with the layer (moot given row 3 already permits individual drop) | Table row 3 + new paragraph |
| unimplemented type, MU=1 | Retained byte-identical; blocks modification of the whole layer (table row 1, "its drop included") | **Blocks the drop entirely** — the layer cannot legally be dropped while this sub-record is present (3513–3515) | Table row 1 (as amended) + "One sub-record blocks the drop" sentence |
| reserved-range type | Governed by the same unimplemented-type rules above (§7.2: "a verifier MUST treat a reserved-range record type as a validity error at the record's governing scope" — the file/layer is already nonconforming at that layer independent of drop mechanics) | Same; moot under a nonconforming-input scenario | §7.2 (1085–1094) + table rows |
| nested layer record (illegal) | Not a legitimate sub-record at all — R-CNT-18: "a validity error at layer scope, not an unknown type"; explicitly *not* processed under the unknown-type MU/PE machinery | Moot — file already nonconforming at that layer | §7.4, R-CNT-18 (1178–1180) |

No sub-record kind is left ungoverned by the amended table plus the new paragraph. This is the
one place check 6 did **not** surface a new defect on its own — but running it surfaced the
user-metadata row's kept/dropped asymmetry that hunk-13 (elsewhere) overclaims about (A-01).

**Check 1 — actors, held against the last row's "any rewrite" and the MU=1 row's "a rewriter
MUST refuse to rewrite the file."** The new paragraph's sentences consistently use "a commit" /
"the updater" (never "a rewriter") as their actor: "A commit MAY therefore drop a layer
record..."; "an updater that drops a layer SHOULD report the loss." The paragraph's own closing
sentences explicitly contrast this with rewrite as a *separate* operation ("a rewrite that drops
the layer (§20.5) reclaiming what the commit would strand"). I checked whether "One sub-record
blocks the drop" could be misread as also being the rewrite rule, which would then conflict with
the row's own (unmodified) "At either scope a rewriter MUST refuse to rewrite the file" sentence
— a *much* stronger consequence (refuse the whole rewrite, not just that layer's drop). Given the
paragraph's actor is "commit"/"updater" throughout and the stronger rewrite-refusal rule is
untouched and independently stated in the very same row, I find no contradiction: for a rewrite,
any unimplemented MU=1 record anywhere (not just in a to-be-dropped layer) already forecloses the
entire rewrite per [R-WRT-06], a broader and unaffected rule. Checked, no defect (rejected
candidate).

**Check 2 — citations.**
- `[R-CNT-18]` for "leaving other layers editable": verified at 1174–1180 — an unknown
  sub-record type with MU=1 is *reject-layer* (not reject-file), which is exactly what licenses
  other layers to remain editable. PASS.
- `[R-CNT-15]` for the file-scope reject-file consequence: verified at 1085–1094. PASS.
- `[R-WRT-06]` for "a rewriter MUST refuse to rewrite the file": verified verbatim at 3624–3627.
  PASS.
- "(the table's first row)": verified — MU=1 is literally the table's first row. PASS.
- §5.2 for "strands... as slack": verified — §5.2 (698–708) defines "structure" as including
  "a record extent (the bytes any record's extent slot references, whatever the record's type,
  §7.2)" — this covers stored tiles, the tile-index region, and each sub-record's own extent
  uniformly. PASS.
- §23.1 for "the bytes remain in it": the *general* R-PRV-01/R-PRV-02 principle is correctly
  cited (stranded bytes remain, recoverable) — but see Finding A-02 below: §23.1's own worked
  sentence about layer-drops is stale relative to this citation's target.

**Check 4 — contradiction, swept restatements.** I checked §23.1 (Privacy Considerations,
4353–4390) and §20.3's three-shapes Example, shape (c) (3443–3465), per the charter's explicit
instruction, since neither was touched by any of the eight hunks:

- §23.1 (line 4369): "...and a commit that drops a layer (§20.4) strands every tile it stored."
  This is the *only* place in the document describing what a layer-drop strands outside §20.4
  itself (confirmed by `grep -n "strands"`, four total hits, one per location, no duplicate). It
  names only "tiles" — omitting the tile-index region and, now, sub-records' extents that
  hunk-15 makes explicit ("strands its stored tiles, its tile-index region and its sub-records'
  extents as slack"). Not false, but materially incomplete for a *Privacy Considerations*
  section whose purpose is exactly to tell a reader what remains recoverable — sub-record
  content (which can include user-metadata, arguably the most privacy-sensitive category) is
  now, after hunk-15, known to strand alongside a dropped layer but §23.1 does not say so.
  **Finding A-02**, UNSWEPT_RESTATEMENT, non-byte-level (a documentation/disclosure gap, not a
  conformance rule; §23.1's list of *operations* is explicitly non-closed, but this is an
  incompleteness in what a *named* operation strands, not in the list of operations).
- §20.3 shape (c) (3444–3446): "...dropping a layer or another PE = 0 record where §20.4
  licenses the drop, any extent it owned, a dropped layer's tiles and index region included,
  becoming slack..." This names tiles *and* the index region (more complete than §23.1) but
  still not sub-records' extents, which hunk-15 now names explicitly as a third category.
  **Finding A-03**, UNSWEPT_RESTATEMENT, non-byte-level (same reasoning: this is a worked example
  illustrating what becomes slack, not itself the normative drop-licensing rule, which is fully
  and correctly stated at §20.4).

**Check 8 — anaphora.** Read forward from the paragraph's insertion point (3510) through the end
of §20.4 (to 3550, the Rationale block). "the table" (3515, 3526) resolves to the just-above
§20.4 table in both cases — unaffected by the insertion, since the insertion is itself
*adjacent* to the table, not interposed between the table and some other later reference to it.
No stranded back-reference found.

**Verdict:** two real findings (A-02, A-03), both non-byte-level documentation gaps; the table
edit itself and the new paragraph's core claims (rows, blocking condition, "whatever their PE
bits") check out against every sub-record kind enumerated.

---

## Hunk-17 — §20.5's disposal sentence

**Rule the repair asserts.** "...a record dropped, a layer with its sub-records, its index region
and stored tiles among them, is not in the output..." — adds "its sub-records" to the existing
enumeration (index region, stored tiles), matching hunk-15's "the drop takes the layer whole."

**Check 4 — contradiction with surrounding text.** Read the full disposal paragraph (3576–3586):
"Dropping is the one disposal that answers, and only where §20.4's table licenses it... Where the
table does not license a drop the rewriter MUST refuse." Consistent with §20.4 as amended by
hunk-15 (a layer drop is licensed under the last table row for the layer itself, and now
explicitly takes its sub-records too, save the MU=1-unimplemented-sub-record block). No
contradiction found; this hunk is a **correct sweep** of hunk-15's change into §20.5's own
enumeration (the positive case the charter warns is often missing elsewhere).

**Verdict:** no defect found. Passes.

---

## Hunk-19 — §20.5's regeneration paragraph (report-the-loss wording)

**Rule the repair asserts.** Old: "...drop the layer, which §20.4's table licenses and the
rewriter reports, or refuse." New: "...drop the layer, which §20.4's table licenses and whose
loss the rewriter SHOULD report as that table says, or refuse." Downgrades an unqualified
"reports" to the correctly-hedged "SHOULD report... as that table says."

**Check 2 — citation ("as that table says").** §20.4's table's PE=0 row: "An updater that drops
such a record SHOULD report the loss" and the post-table paragraph (as amended by hunk-15): "an
updater that drops a layer SHOULD report the loss, as the table says of any record dropped."
Both use SHOULD, matching hunk-19's SHOULD exactly. PASS — this is also a correct sweep (fixing
what was, before, an overclaim: stating flatly that "the rewriter reports," which read as
mandatory).

**Check 4 — surrounding paragraph.** Read 3647–3660 in full: no contradiction with the two
disposals ("drop the layer... or refuse"), [R-WRT-06]'s framing, or [R-WRT-09]'s scope
("[R-WRT-09]'s checks reach the index chain... rather than an entry's own value domain bounds how
far a rewriter goes looking").

**Verdict:** no defect found. A correct fix (removes an overclaim the old wording had).

---

## Hunk-26 — Appendix H's updater entry and rewriter sentence

**Rule the repair asserts.** (1) "drops a layer record only under §20.4's PE = 0 licence, its
sub-records with it, and never removes a user-metadata record from a scope it keeps" — sweeps
hunk-15's rule into the checklist. (2) "never modifies or drops a scope governed by an unknown
critical record" — adds "or drops" to reflect hunk-15's "its drop included." (3) A rewriter
sentence restating [R-WRT-07]: "preserves the content of every structure it carries forward,
re-pointing each extent slot it relocates and regenerating each tile-index region any of whose
stored extents it relocates" — replacing an older, ambiguous "regenerating each index region it
relocates" (ambiguous between "the region is physically placed somewhere new" — true almost
always — and "the region's referenced stored extents moved" — the actual trigger). (4) A new,
explicitly-advisory sentence: "Advisory, and not a conformance condition: an updater that drops a
record SHOULD report the loss (§20.4)."

**Check 2 — citations.**
- (1) against §20.4's last table row + hunk-15's paragraph: verified, matches word for word.
  PASS.
- (2) against the amended MU=1 row ("...blocks modification of that layer, its drop included"):
  verified. PASS. Charter asks what "drops a scope" means at file scope: only a layer record
  "governs" a scope (layer scope) in this document's usage; a plain top-level record does not
  contain anything to "drop." At file scope the very next clause handles the relevant case
  separately and completely ("rejects outright a file carrying an unimplemented top-level MU = 1
  record"), so "drops a scope" is, in practice, read as the layer-scope case only. This is a
  **minor readability gap** (the sentence does not itself restrict "scope" to layer scope) but
  the adjacent clause forecloses any actual misapplication. **Finding A-07**, NEW_AMBIGUITY,
  non-byte-level.
- (3) against [R-WRT-07]'s actual text (3629–3641): "...except that relocation re-points extent
  slots, regenerates each tile-index region any of whose stored extents the output relocates..."
  — matches the new Appendix H wording closely and correctly; the *old* wording ("index region it
  relocates") is the one that mismatched the rule (conflating region-placement with
  extent-relocation, contradicted by the compaction Example at 3675–3696, where "A's index is
  copied and only its slot re-pointed" despite A's index region itself being placed somewhere new
  in the output). This is a **correct fix**, verified against both R-WRT-07's prose and its
  worked example.

**Check 8 — where does the trailing Advisory sentence land?** It appears immediately after the
rewriter-specific sentence ("...refuses to rewrite a file carrying an unimplemented MU = 1 record
(§20.5)."), at the very end of the combined "Conforming updater" entry (which covers both
appenders and rewriters, per its own heading, "an appender or a rewriter"). I checked whether a
reader would take the SHOULD-report duty as rewriter-specific rather than updater-general.
Cross-checking against the document's established pattern, the **Conforming writer** entry
(4911–4921) ends the identical way — "Advisory, and not a conformance condition: a writer SHOULD
zero the gaps it creates" — trailing after writer-specific detail but understood to cover the
whole entry. Given that precedent, I lean toward this being intentional and consistent, but it is
genuinely positioned right after rewriter text and cites only "(§20.4)" (not the appender-side
report duty that was *removed* from its earlier position in clause (1) of this same entry — the
old text had "reporting the loss" attached directly to the appender's layer-drop clause; the new
text moved it out entirely, leaving clause (1) silent on reporting and relying solely on the
trailing sentence to cover it). **Finding A-06**, NEW_AMBIGUITY, low confidence, non-byte-level.

**Verdict:** two low-severity ambiguity findings (A-06, A-07), non-byte-level; the substantive
content of all four claims checks out against its cited rule.

---

## BCP 14 casing sweep (all eight hunks)

`grep -n '^+' <hunk>.diff | grep -iEo '\b(must not|must|shall not|shall|should not|should|may
not|may|required|recommended|optional)\b'` run against every hunk's added lines. Every keyword
hit (hunk-13: MAY; hunk-15: MUST NOT, MUST, MAY, SHOULD; hunk-19: SHOULD; hunk-26: SHOULD) is
already fully capitalized in the diff. Zero lowercase-keyword hits across all eight hunks. No
finding.

## NESTED_DASH sweep (all eight hunks)

`grep -n '^+' <hunk>.diff | grep -o '—'` counted per added line. Only one added/modified line in
all eight hunks contains an em dash at all: hunk-15's amended MU=1 table row (line 3506), which
contains exactly **one** em dash ("...reject-file — the same treatment §6.3 gives an unknown
incompat-lane bit."), not a pair, and not nested inside another dash-delimited clause. No
NESTED_DASH finding in any of the eight hunks. Control: I confirmed the grep mechanism finds
em-dashes at all by first running it against the full hunk files (unfiltered), which returned
positive counts (2, 5, 2, 3, 8, 4, 3, 4 respectively) coming from unchanged context lines,
proving the search pattern works and that the zero-on-added-lines result is a real zero, not a
broken search.

## Sweeps run (verbatim, with hit counts)

- `grep -n "R-CNF-03" spec/tarn.md` → 9 hits (196, 1059, 1802, 2454, 2581, 2627, 2670, 2714,
  2751, 4188, 4900 — 11 actually, recount below). Control: same grep for "R-CNT-12" (used
  earlier) returned hits at expected lines, proving the pattern isn't silently failing on
  hard-wrapped bracket text — R-requirement IDs are short and never wrap.
- `grep -n "R-WRT-07\|R-WRT-06\|R-WRT-09" spec/tarn.md` → 17 hits, used to locate the actual
  R-WRT-07/-06/-09 defining prose (3629–3728) versus mere citations.
- `grep -n "strands" spec/tarn.md` → 4 hits (3519 [hunk-15 itself], 3713, 4366, 4369). Control:
  the word "strands" is short and mid-word, cannot wrap; the fact that only one non-hunk hit
  (4369, §23.1) discusses a layer-drop specifically (4366 is about user-metadata edits; 3713 is
  about a shortening) confirms §23.1's layer-drop sentence really is the singular restatement I
  am holding hunk-15 against, not one of several.
- `grep -n "sub-records" spec/tarn.md | wc -l` → 13 hits total, cross-checked to confirm the
  concept "sub-records' extents" is not restated with full fidelity anywhere outside §20.4 itself
  and hunk-17/hunk-26's sweeps.
- `grep -n "never drops\|never removes" spec/tarn.md` → 3 hits (1040 [hunk-06], 3516 [hunk-15],
  4940 [hunk-26]) — confirms these three are the only "never drops/removes" formulations in the
  document; no fourth, unswept copy of this rule exists elsewhere with stale wording.
- `awk 'NR==3200,NR==3330' spec/tarn.md | grep -n "keep"` → 5 hits, tabulated above for the
  "keeps" census (check 7 discipline).
- BCP-14 and NESTED_DASH sweeps as described above, run separately per hunk (16 total grep
  invocations), all reported with exact hit counts inline above.

Control for the hard-wrap warning: I deliberately used the `Read` tool (not `grep`) for every
full passage I needed to judge in context (§5.2, §7.2–7.4, §20.3, §20.4, §20.5, §23.1, Appendix
H), and reserved `grep` only for short, non-wrapping tokens (requirement IDs, single words,
em-dash characters) — exactly the discipline the brief requires. I did not draw any conclusion
from a grep of a multi-word phrase that could have wrapped.

## Derived numbers

- §20.4's table: 3 rows, confirmed by direct reading (not computed) — cited by hunk-06's Note
  ("three rows") and matches.
- Count of "strands" hits used to locate the single §23.1 layer-drop sentence: 4 total, 1
  relevant (see above).
- Count of "sub-records" occurrences: 13 (used only as a locator, not as a claim in any finding).
- Count of em-dash characters on hunks' added lines: 0 pairs (1 single dash, hunk-15 line 3506)
  across all eight hunks combined — the basis for the NESTED_DASH null result.
- Count of lowercase-keyword hits across all eight hunks' added lines: 0 — the basis for the
  BCP-14 null result.

## Rejected candidates

1. Hunk-13's "keeps" polysemy (commit-keeps-layer vs. layer-keeps-declarations): real polysemy,
   but grammatically unambiguous in the actual sentence ("a layer the commit keeps" has an
   explicit subject); closed after parsing the relative clause both ways and finding only one
   reading survives.
2. Hunk-07's sub-record extent slots as a "second exception": closed — sub-records are
   individually covered by the same general per-record MU=0 rule, recursively, not folded into
   the layer record's own single-extent-slot budget; the "one exception" framing is specifically
   about the layer's own extent *content* (the tile index) referencing further bytes, which is
   a different thing.
3. Hunk-15's "editing user metadata" vs. "never removes... from a scope it keeps": closed —
   editing replaces content via a new extent (shape (b)) and is a modification, not a removal;
   no conflict with the new "never removes" sentence.
4. Hunk-15 MU=1-implemented-by-the-updater case creating a two-updater fork (one blocked, one
   not, on the same file): closed as a pre-existing, intentional asymmetry in the base
   specification ("Stored flag bits are authoritative only for record types the consuming tool
   does not implement", §7.3/[R-CNT-22]), not something hunk-15 newly introduces; not a defect
   caused by this repair.
5. Hunk-15 against reserved-range and nested-layer-record sub-record kinds (charter's own
   enumeration): closed — both are already-nonconforming-input scenarios governed by
   [R-CNT-15]/§7.2 and [R-CNT-18] respectively, independent of and unaffected by the drop
   mechanics hunk-15 adds.
6. Hunk-13's "the new layer being new whatever bytes its entries address, the dropped layer's
   former extents included": tried to construct a same-commit physical-offset collision between
   a dropped layer's former extent and the new layer's freshly-written extent; closed because
   append-only writing (F only grows within one commit) makes this physically impossible within
   a single commit, so the clause is a defensive, always-vacuously-true generalization, not a
   false claim.
7. Hunk-26's advisory-sentence placement (A-06 above): considered filing as a harder
   NEW_AMBIGUITY/contradiction, closed down to low-confidence given the document's own
   established "Advisory..." trailing-sentence pattern in the Conforming-writer entry.

## Confidence / where little was found

Hunks 17 and 19 returned no findings at all after full application of all eight checks; for both
I specifically re-read the full enclosing paragraph (not just the touched sentence, per the
byte-level test's own instruction to read "the paragraph it lives in and the one before that")
and cross-checked every citation and every "sweep" of hunk-15's vocabulary into the paragraph.
Both are, on my reading, purely corrective (they fix real imprecision in the pre-repair text —
hunk-19 removes an overclaim, hunk-26's R-WRT-07 rewording removes a genuine ambiguity that the
compaction Example already contradicted). I did not stop at "the words are right"; for hunk-17 I
specifically tried to find a MUST elsewhere in §20.5 that the new "with its sub-records" breadth
might collide with (check 4) and found none — the table (§20.4, amended) already licenses exactly
this breadth.

## Findings summary

- A-01 (hunk-13): "no byte tells the two apart" is an overclaim falsified by hunk-15's own
  user-metadata-survival rule. Not byte-level.
- A-02 (hunk-15, sweep failure): §23.1's layer-drop sentence names only "tiles," omitting the
  index region and sub-records' extents that hunk-15 makes explicit. Not byte-level.
- A-03 (hunk-15, sweep failure): §20.3 shape (c)'s Example names tiles and index region but not
  sub-records' extents. Not byte-level.
- A-04 (hunk-14): "the user-metadata record... is dropped only with a layer that carries it" does
  not separately state the (vacuously-true) top-level case. Not byte-level.
- A-05 (hunk-07): [R-CNF-03] alone is cited for a claim that also covers updaters; the updater
  half rests on a separate, uncited sentence. Not byte-level.
- A-06 (hunk-26): the trailing Advisory/SHOULD-report sentence sits right after rewriter-specific
  text; low-confidence ambiguity. Not byte-level.
- A-07 (hunk-26): "never modifies or drops a scope governed by an unknown critical record" does
  not itself restrict "scope" to layer scope. Not byte-level.

No byte-level finding survived scrutiny in this batch of eight hunks: every candidate I could
construct either (a) was independently foreclosed by a rule the disputed sentence did not carry
the weight of (hunk-13's rationale, hunk-14's vacuous top-level case), or (b) was a documentation
completeness gap in explanatory/privacy text rather than in the operative table (A-02, A-03), or
(c) was a citation-attribution or placement imprecision that does not change what any correct
reader would conclude about actual bytes (A-05, A-06, A-07).
