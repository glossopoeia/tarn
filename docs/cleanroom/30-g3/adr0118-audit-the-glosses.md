# Audit: the-glosses (hunks 03, 05, 21) — round 30 repair audit

## Disclosure

Read:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-03.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-05.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-21.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md — ranges via sed: 95-110, 160-180, 195-245,
  325-340, 1085-1115, 1595-1720, 1918-1932, 1941-2098, 2395-2565, 2588-2762, 2975-2990, 3088-3300,
  3839-3952, 3960-4050, 4510-4667, 60-70; plus grep hits across the whole file.

Wrote (scratch only):
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/scratch/the-glosses/flat.txt
  (spec with newlines and "> " removed, whitespace collapsed)
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/scratch/the-glosses/flat-nobold.txt
  (same with `**` stripped)
- this file.

Did NOT read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json,
git history/log/diff, full.diff, any other hunk file, the out/ directory listing, the web.

Context I did not ask for: the runtime placed in my context a project-instruction pointer (CLAUDE.md -> AGENTS.md,
which I did not open), an index of four auto-memory note titles, an environment block naming five recent commit
subjects (which name ADR numbers and "round 29"), and the git status. None of it was used as evidence; nothing
below rests on it. All three hunk files were where the brief said they were, and each hunk's header line range
agrees with its body (verified: hunk 03 -> spec lines 1638-1639; hunk 05 -> line 2662; hunk 21 -> lines 4601-4603).

## Force of each landing site ([R-CNF-01], spec line 105-107)

[R-CNF-01]: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*,
or *Rationale*; and appendices identified as non-normative."

- Hunk 03 lands in the blockquote in §11.1 that opens "> **Rationale.** Empty layers serve schema-first
  workflows" (line 1613). Label test: labeled Rationale -> NON-NORMATIVE. (Not by the ">" marker; by the label.)
- Hunk 05 lands in the running prose paragraph of §18.2 that ends "`[R-MTA-09]`" (line 2675). No block, no
  label -> NORMATIVE. The sentence carries "MUST NOT certify" and "MUST NOT report".
- Hunk 21 lands in "### Appendix G — Reproducible-writer profile (non-normative)" (line 4510), item 5.
  Heading says non-normative -> NON-NORMATIVE.

So hunks 03 and 21 are glosses; hunk 05 is normative text.

---

## Hunk 03 — §11.1 Rationale, "last" -> "only remaining"

### Passage (lines 1613-1639, whole Rationale block read)

"... Growth that leaves **entry_count** unchanged touches the directory alone — a growth raising one grid count
⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among them, the product holding at 0. Growth that changes entry_count
changes extent_length with it (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and disk
ordinals renumber wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`) — the growth that raises a zero-extent
layer's **only remaining** zero grid count included."

### Rule the repair asserts (my words)
When a commit grows a layer that has zero-extent dimensions, its tile-index region is re-emitted iff entry_count
changes; entry_count changes iff the product of grid counts leaves 0, which happens exactly when the growth
raises every zero grid count — and the named instance is the growth that raises the sole zero grid count still
at 0.

### Cases built (grid arithmetic §11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, entry_count = N or C·N)
- Layer A, d=2, E=(0,100), T=(10,10): G=(0,10), N=0, entry_count 0.
  Growth E₀: 0->5: G=(1,10), N=10, entry_count 0->10 (interleaved) — CHANGES. This is "raises the only
  remaining zero grid count". Re-emission per §20.3 step 4 ("entries new to this generation ... grown
  extents"). Gloss correct.
- Layer B, d=2, E=(0,0), T=(10,10): G=(0,0), N=0.
  Growth E₀ alone 0->5: G=(1,0), N=0, entry_count unchanged — "directory alone". Matches the preceding
  sentence's "raising one grid count while another stays 0". Gloss correct.
  Then growth E₁ 0->5 in a later commit: raises the only remaining zero -> N=1 -> changes. Matches new wording.
  Growth of both at once 0->5, 0->5: N=1, entry_count changes. Covered by the head clause "Growth that changes
  entry_count"; not the named instance (neither zero is "the only remaining"), but "included" marks an
  instance, not an exhaustive characterisation. Not a defect (see rejected candidates).
- Old word "last": ambiguous between the last-DECLARED dimension (d−1) and the last zero in time. Under the
  first reading the gloss would be false for Layer A (dimension 0 is the zero one, not the last declared) —
  raising it does change entry_count. The new word removes that reading.

### Check 1 tense/quantifier
"raises" = the commit's effect from superseded to new generation; "only remaining zero grid count" is evaluated
in the superseded generation. Matches §20.3 step 4's tense ("entries new to this generation (added tiles, grown
extents)"). Normative rule restated: §20.3 step 4, line 3131-3137: "Every layer whose stored-tile set or index
content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment
CRC array — necessarily at a new placement". A change to entry_count is a change of index content (new entries).
Quantifiers agree.

### Check 2 citations
- [R-CNT-17] (line 1105-1111): "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when
  entry_count is 0)" — monotone in entry_count, so "changes extent_length with it" PASS.
- [R-GEO-06] (line 1702-1714): disk ordinal s / c·N+s — grid-count change renumbers. PASS.
- §20.3 (line 3088) is "The append procedure"; [R-WRT-04] (line 3289) closes its numbered steps. PASS.
- §11.2 (line 1641) defines ⌈Eᵢ/Tᵢ⌉. PASS.

### Check 3 label
Block is labeled **Rationale.** -> non-normative. The normative statements are §20.3 step 4 (line 3131-3142)
and [R-CNT-17]. Both say what the gloss says. The repair edited a gloss; the normative rule needed no change
and was not changed. Consistent.

### Check 4 contradiction in the passage
Read the whole Rationale and §20.3 step 4 growth paragraph (line 3222-3243: "an extent MAY grow ... a growth is
permitted exactly where the geometry it produces satisfies every rule that geometry is subject to"). Nothing
carves out the zero->nonzero grid case. [R-COD-07] Note (line 2476-2486): "The escape ends exactly when the
layer's addressed-tile count rises above 0, which takes every dimension's extent nonzero (§11.2) — a growth that
leaves any extent at 0 holds the count at 0" — agrees with both sentences of the gloss. §13.3 Note (line
1929-1931): "each commit that ... grows its extents so that entry_count changes, re-emits that layer's whole
tile-index region (§11.1, §20.3, [R-WRT-04])" — agrees. §20.3 Note (line 3293): "any change to a layer's
stored-tile set re-emits that layer's whole tile-index region" — agrees.

### Check 5 exhaustive claims
"whole tile-index region" — §20.3 says "in full". PASS. "wherever" — open, not exhaustive. "only remaining" —
picks out one instance; "included" frames it as an instance. No overclaim.

### Check 6 unconstrained siblings
Structure: a growth commit on a layer with zero grid counts. Members: entry_count (fixed by [R-CNT-17]),
extent_length (same), extent slot/placement (§20.3 step 4 + L22 (0,0) rule), disk ordinals ([R-GEO-06]),
declaration bounds ([R-ENC-04], [R-COD-07] per §20.3). All governed. Nothing left open by this gloss.

### Check 7 analogy
No "likewise / exactly as / the same way" in the hunk. N/A.

### Check 8 anaphors
Hunk substitutes two words for one; no sentence inserted. "the growth" — definite; with "only remaining" the
referent is unique. "included" attaches to "Growth that changes entry_count" — unchanged. Nothing re-resolves.

### Sweeps for restatements
grep 'last zero' -> 0; control 'zero grid count' -> 1 (this line). flat-nobold 'last zero grid count' -> 0;
control 'only remaining zero grid count' -> 1. No other restatement of the "last/only remaining" phrase exists.

### Verdict on hunk 03
Correct. The new adjective picks out exactly the case the rule makes special (the growth that lifts the product
of grid counts off 0 by raising the sole zero factor). No finding.

---

## Hunk 05 — §18.2 [R-MTA-09], "the bound above" -> "either bound above"

### Passage (lines 2588-2675 read in full, plus the Note after)

Bounds stated above the sentence (grep 'bound\|guarantee' over lines 2588-2662):
1. line 2608-2610: "Under either encoding a reader decodes with a bound of its own choosing, no smaller than
   §21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any other it
   cannot read" — the reader's DECODED-SIZE bound (floor 16 MiB).
2. line 2631: "which is why the bound above is the reader's own and not the file's" — refers back to bound 1,
   not a new bound.
3. line 2634-2639: "a reader's window bound is its own, no smaller than §21.9's guarantee for that quantity, and
   a frame declaring more than the reader admits is ignore-record on that ground — the reader's capability ...
   the reader MAY decline it (`[R-ERR-04]`)" — the reader's WINDOW bound (floor 8 MiB).
4. line 2649: "§21.9's user-metadata row bounds a document's decoded size" — verb; the guarantee row, a floor
   on bound 1, not a third bound a reader declines on.
5. §21.9's guarantees (16 MiB, 8 MiB) — floors on the two bounds, not bounds a verifier declines on.

Count: exactly TWO bounds a reader/verifier declines on. Each is stated as a ground for declining ("ignore-record
like any other it cannot read"; "ignore-record on that ground ... MAY decline it"). "either" therefore ranges over
exactly the right set. The charter's failure conditions (more than two; one not a decline-ground) do not obtain.

### Rule the repair asserts (my words)
A verifier that refuses to decode a user-metadata document because its own decoded-size bound OR its own window
bound is exceeded has not established that document's conformance, must not certify, must not call it a
violation, must report the unchecked requirement, and gets verdict cannot-establish only if nothing else was
found violated.

### Check 1 tense/quantifier
Actor: verifier. What it holds: its own two bounds and the stored extent. "either" = whichever of the two it
declined on; for an encoding-1 document only bound 1 applies and "either" still reads correctly (there is no
frame). Normative rule it restates: [R-CNF-11] verifier definition line 216-224: cannot establish "... or when it
declines to decode a user-metadata document (`[R-MTA-09]`)" — unqualified as to which bound. Old "the bound"
was NARROWER than [R-CNF-11] (only the size bound); new "either" matches [R-CNF-11]'s unqualified "declines to
decode". Quantifiers now agree. This sentence IS the [R-MTA-09] normative statement; [R-CNF-11] is its twin.

### Check 2 citations
- [R-COD-11] (line 2547-2560): "A verifier that cannot execute a layer's codec or filter cannot establish that
  layer's conformance and MUST NOT certify the file. That inability is not a finding that the file is
  nonconforming, and it fixes the file's verdict as cannot establish only where the verifier established no
  violation elsewhere". Sentence claims "exactly as [R-COD-11] requires of a codec it cannot execute" — PASS.
- [R-CNF-10] (line 331-338): "Readers MAY enforce resource limits, but MUST accept any conforming file within the
  minimum guarantees" — cited for "the bound is that verifier's capability and not a limit on validity". PASS.
- [R-CNF-11] (line 226-243): "A verifier MUST report each requirement it was unable to check on a capability or
  resource ground" — cited for "one of the unchecked requirements [R-CNF-11] obliges the verifier to report".
  PASS.
- [R-CNF-02] (line 160-176), [R-COD-06] (line 2416-2444), [R-MTA-10] (line 2733-2754), §17.2 — all in the same
  paragraph, unchanged by the hunk; opened and each says what the paragraph attributes to it (R4 routing
  "checkable from the bytes alone" — [R-CNF-02] "pure predicate on bytes"; [R-COD-06] content-size MUST equal
  decoded size; [R-MTA-10] unassigned encoding not a decline). PASS.
- [R-ERR-04] (line 4025-4037): "a reader MAY decline it — at the whole file, or at the narrowest scope ..." PASS
  for the window paragraph's "MAY decline it".

### Check 3 label
Landing is running prose, unlabeled, ending "`[R-MTA-09]`" -> normative. The repair lands in force. Sibling
statement [R-CNF-11] (§2.3) already carried the wider quantifier. No labeled block carries the only statement.

### Check 4 contradiction in the passage
- "the bound is that verifier's capability" (singular, next clause) after "either bound": resolves to whichever
  bound it declined on. Not a contradiction.
- Window paragraph: decline is "ignore-record on that ground ... no violation" — verifier sentence: "not a
  finding that the file is nonconforming" — agree.
- Following Note (line 2677-2686): "A reader that proceeds takes ignore-record for that record; a reader that
  instead declines on resource grounds under [R-ERR-04] does so at the whole file, a document having no declared
  size" — about readers and scope, not the verifier verdict; does not collide with "either".
- "The decline presupposes an encoding this specification assigns" — holds for both bounds (encoding 1 has bound
  1 only; encoding 2 has both). Consistent.
- §21.9 [R-ERR-04]: "Software that declines on that ground a file whose every quantity lies within the table is
  not a conforming reader" — a verifier with bounds at or above the floors never declines a within-guarantee
  document; consistent with "the bound is that verifier's capability".

### Check 5 exhaustive claims
"either" — a count of two. Falsification attempted above: two bounds found, no third. PASS.

### Check 6 unconstrained siblings
Structure: a verifier's decline report. Members: which bound (implied by "the bound it applied"), the bound's
value (SHOULD report), the stored length of the extent (SHOULD report), the requirement and ground ([R-CNF-11]
MUST name), the record's owning scope (not required here; [R-MTA-10] requires it for a different case). The last
is a pre-existing SHOULD-level gap, untouched by this hunk and not a fork of any verdict. Not filed.

### Check 7 analogy
"exactly as `[R-COD-11]` requires of a codec it cannot execute". Repair's governing verb: "declines to decode a
document on either bound above ... cannot establish that document's conformance and MUST NOT certify". Cited
rule's verb: "cannot execute a layer's codec or filter cannot establish that layer's conformance and MUST NOT
certify the file". The analogy is on the consequence (cannot establish + MUST NOT certify), which is word-for-word
the same. The grounds differ (declines on a bound vs cannot execute) and [R-CNF-11] lists them as separate
grounds, but the sentence does not claim the grounds are alike — only what they "require". PASS.

### Check 8 anaphors
One word swapped; nothing inserted. Forward: "the bound is that verifier's capability" (was "the bound" -> the
bound above; now -> either bound, whichever applied); "the decline" x3 -> the decline just described; "the bound
it applied" -> the one it declined on. Each resolves the same as before, with "the bound" now naturally reading
as "whichever". Backward: "either bound above" -> the two bounds enumerated above; both are within the same
paragraph. Unaffected.

### Sweeps
grep 'the bound above' -> 1 (line 2631, the decoded-size back-reference, correct as is); 'either bound' -> 1 (this
line). flat-nobold 'on the bound above' -> 0; control 'on either bound above' -> 1. grep 'declines to decode' -> 2
(line 222 [R-CNF-11], line 2661 this sentence). Both agree.

### Byte-level
No. The sentence governs a verifier's verdict on a conforming file; under both old and new wording [R-CNF-11]
already required cannot-establish for any decline to decode a document, so no verdict forks.

### Verdict on hunk 05
Correct and complete. No finding.

---

## Hunk 21 — Appendix G item 5, "every tile it touches" -> "any tile whose decoded image the permutation does not fix, and a fixed image is no evidence of which filter produced it"

### Passage (item 5, lines 4590-4610, whole item read; items 1-10 and closing paragraph read)

"**A fixed filter value** likewise: §17.3 leaves the choice to the writer, and no content implies it, so two
writers agreeing on everything else still disagree on bytes without it pinned. The filter is the identity exactly
where its permutation is — where the stride is 1, as for a packed boolean plane, and equally where the decoded
image is a single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of any tile whose
decoded image the permutation does not fix, and a fixed image is no evidence of which filter produced it. **Fixed
declared tile extents and a fixed layout** likewise, as item 2's closing sentence names both: ..."

### Rule the repair asserts (my words)
Where the shuffle is not the identity permutation, filter 2 changes a stored tile's bytes relative to filter 1
precisely for those tiles whose decoded image is not a fixed point of the permutation; and where the image is a
fixed point, the stored bytes look the same under both filters, so they cannot tell you which filter was
declared.

### [R-COD-10] permutation (line 2517-2533)
byte i of group j -> offset i·n + j (0 ≤ i < s, 0 ≤ j < n, n = L/s). Identity iff i·n + j = j·s + i for all i, j
⇔ i(n−1) = j(s−1) for all i,j ⇔ s = 1 or n = 1. So "exactly where ... stride is 1 ... [or] n = L/s being 1"
is exhaustive and correct (pre-existing, verified anyway).

### Constructed images (s = 2, n = 2; planar uint16, P = 2)
- Fixed, non-constant: bytes [01 02 | 02 03] (values 0x0201, 0x0302). Shuffle: offsets 0,1,2,3 receive
  g0b0=01, g1b0=02, g0b1=02, g1b1=03 -> [01 02 02 03]. Fixed.
- Not fixed: [01 02 | 03 04] -> [01 03 02 04].
The sentence claims a byte change only for the second, and says nothing false of the first. Under codecs 2-4
the stored bytes are the codec's output on the filtered image; lossless coding is injective, so a different
filtered image gives different stored bytes. TRUE of both images.
Old wording "every tile it touches" was false for the first image. The repair fixes that.

### Corollary "a fixed image is no evidence of which filter produced it"
Actor: a reader or verifier holding the stored bytes (and the decoded image). Under filter 1 the filtered image
is the decoded image ([R-COD-09] line 2510); under filter 2 with a fixed image the filtered image equals the
decoded image. Stored bytes identical -> no evidence. Does the document anywhere let an actor infer the filter
from stored bytes? Searched: §21.4 T26 (line 3803) — detects a WRONG STRIDE through T2/T4's padding-content and
bool-byte checks, and only "where the resulting image breaks" one of those; §21.7 (line 3897) — mis-strided
filter is otherwise undetectable; §17.3 [R-COD-10] same. For a fixed image the filtered bytes under either
filter are identical, so every such check gives the same answer under both. The filter VALUE is known from the
layer record's filter field (§7.4, [R-COD-09]), not inferred. The corollary is true as a statement about
evidence from bytes.

### Check 1 tense/quantifier
"any tile whose decoded image the permutation does not fix" — ranges over tiles with a stored image; an
unstored tile has no stored bytes to change (vacuous, harmless; noted under rejected). Present tense, no
generation issue (the profile is about one emission). Restated rule: [R-COD-10]'s permutation. Agrees.

### Check 2 citations
- [R-COD-10] (line 2517-2533): defines s, n = L/s, and the permutation; "for a packed boolean plane s = 1 and the
  filter is the identity". PASS for "n = L/s being 1 ([R-COD-10])" and "stride is 1, as for a packed boolean
  plane".
- §17.3 (line 2508): "Writers MUST NOT emit a filter value other than 1 or 2" — "leaves the choice to the
  writer": both are core and either MAY be emitted. PASS.
- §11.3 (line 1666; its Note line 1678): "Tile extents are a writer's choice, and this specification imposes
  none" — quoted accurately (it is a Note, but the profile is non-normative and the quotation is faithful). PASS.
- §14.1 (line 1941, [R-SER-06] line 1958): "1 = interleaved and 2 = planar are the only values ... a writer MAY
  emit" — "leaves the layout to the writer". §14.4 [R-SER-09] confirms every layout/type combination is defined,
  so no rule forces one layout. PASS.
- "item 2's closing sentence names both": line 4548-4550 "two files carrying the same arrays can legitimately
  differ in tiling, layout, and codec". Names tiling and layout. PASS.
- §11.2 (grid count / addressed-tile count), §14.2 (value arrangement) — cited in the following sentence; both
  say so. PASS.

### Check 3 label
Appendix G is headed "(non-normative)". The normative permutation rule is [R-COD-10] and is unchanged. The gloss
now agrees with it (old gloss contradicted it for fixed-point images). Correct place to edit; nothing else
restates "every tile it touches" (grep -> 0 in raw and flat files; control 'fixed image is no evidence' -> 1).

### Check 4 contradiction in the item
- "two writers agreeing on everything else still disagree on bytes without it pinned" — true regardless of tile
  bytes, because the layer record's filter field (§7.4) differs. Not contradicted by "the filter is the identity
  where ..." (that speaks to tile bytes, the first sentence to the file).
- §20.3 step 4 carve-out (line 3164-3166): "a filter whose mandated stride makes it the identity ([R-COD-10])" —
  names only the stride-1 identity; Appendix G names stride 1 AND n = 1. §20.3's governing sentence says the
  list "names where that effect arises rather than standing on its own", and "the test is the effect", so an
  n = 1 identity also passes the §14 bar. Not a contradiction with the hunk (and that clause is pre-existing
  context, not the changed text).
- Item 6 (never store an all-fill tile) and item 5 do not interact with the new clause.

### Check 5 exhaustive claims
"exactly where" (pre-existing) — verified exhaustive above. "any tile" — open. "no evidence" — an absolute; tried
to falsify via T26/§21.7/§17.3: none separates filter 1 from filter 2 on a fixed image. Holds.

### Check 6 unconstrained siblings
Structure: profile item 5's pinned declarations — alignment A, slab (A_slab, S), filter, tile extents, layout.
Codec: item 1. Fill: item 7. Linearization and index_encoding admit one value each ([R-GEO-05], §7.4 table).
Channel order/names/types: content. All members pinned by some item or admit one value. Nothing left open.

### Check 7 analogy — "likewise" (twice in item 5; the second follows the edit)
(a) "**A fixed filter value** likewise" likens the filter to alignment/slab: "both change placement and neither
is implied by content" vs "§17.3 leaves the choice to the writer, and no content implies it". Verbs: "is implied
by content" / "implies it". Same relation, same direction (content -> declaration). PASS.
(b) "**Fixed declared tile extents and a fixed layout** likewise" likens tile extents and layout to the filter.
Profile says of the filter: "§17.3 leaves the choice to the writer, and no content implies it, so two writers
agreeing on everything else still disagree on bytes without it pinned". Of tile extents: "§11.3 states that tile
extents are a writer's choice and that this specification imposes none". Of layout: "§14.1 leaves the layout to
the writer". Then jointly: "Without both pinned, two writers agreeing on everything above still disagree on
bytes". Verbs side by side: "leaves the choice to the writer" (filter) / "are a writer's choice" (extents) /
"leaves the layout to the writer" (layout); "disagree on bytes without it pinned" / "Without both pinned ...
disagree on bytes". Tested separately: tile extents — §11.1 imposes only Tᵢ ≥ 1 plus bounds ([R-ENC-04],
[R-COD-07]); within them, free; the same arrays serialize under any choice -> not implied by content. Layout —
[R-SER-06]/[R-SER-09]: either value for any type mix -> not implied by content (§14.4's Note even shows a
single-channel numeric layer gives identical tile images either way, so content cannot distinguish them). Both
members carry the analogy. PASS for each.
Did the insertion shift what "likewise" attaches to? Before: nearest preceding clause "elsewhere it changes the
stored bytes of every tile it touches"; after: "a fixed image is no evidence of which filter produced it". In
both cases "likewise" attaches to the bold item-head pattern (a writer's free choice, not implied by content,
must be pinned), as the continuation "as item 2's closing sentence names both ... Without both pinned" confirms.
Unchanged.

### Check 8 anaphors
Inserted text's own back-references: "it" in "elsewhere it changes" -> the filter (unchanged from before); "the
permutation" -> "its permutation" two clauses earlier; "it" in "which filter produced it" -> "a fixed image"
(the filtered image that equals the decoded image). Antecedents are within the sentence. Forward from the
insertion to the end of item 5: "likewise" (discussed, unaffected), "both" -> tile extents and layout (its own
sentence), "everything above" -> items 1-4 and the earlier parts of 5 (unchanged). Nothing re-resolved.

### FINDING E-01 (NEW_AMBIGUITY, not byte-level)
The repair introduces "fix"/"fixed" in the mathematical sense (fixed point of a permutation) into an appendix
whose every other use of "fixed" — seven occurrences in items 1, 5, 9 — means "pinned by the profile", and
places "a fixed image" immediately before a bold item head that opens "**Fixed declared tile extents and a fixed
layout** likewise". A profile reader carrying the appendix's sense reads "a fixed image is no evidence of which
filter produced it" as "pinning the image does not pin the filter" — a different proposition from the one
intended ("an image the permutation leaves unchanged yields stored bytes that cannot distinguish filter 1 from
filter 2"). Both readings happen to be consistent with the item's thrust, which is why this is not a
contradiction and not a fork of any implementation behaviour: the profile pins the filter value under either
reading, and Appendix G binds no actor. It is a readability defect the repair created. Repair: "and an image the
permutation fixes is no evidence, in its stored bytes, of which filter produced them" — or drop the clause,
since the item's first sentence ("no content implies it") already carries the point.
Byte-level: no. Non-normative appendix; the layer record's filter field differs under either reading and the
profile's obligation to pin it is unchanged.

### Sweeps
grep 'every tile it touches' -> 0 (raw and flat; control 'fixed image is no evidence' -> 1).
grep -n 'permutation' -> 2: lines 4598 and 4601, both in item 5 ([R-COD-10] describes the mapping without using
the word). grep -n 'does not fix' -> 2: line 4585 (item 3, "order alone does not fix bytes" — the PINNED sense of
"fix", in the same appendix) and line 4602 (the hunk). So no other restatement of the filter gloss exists, and
the appendix's other use of the verb "fix" is the pinned sense — supporting E-01.
grep 'the identity' -> 3: 2523 ([R-COD-10], packed bool), 3166 (§20.3 carve-out), 4597 (item 5). All consistent
with the repaired sentence (see check 4 on §20.3's narrower example).

---

## Rejected candidates
1. Hunk 03: "only remaining" does not name the growth that raises two zero grid counts at once. Dropped: the head
   clause "Growth that changes entry_count" governs and the tail is marked "included", an instance not a
   definition; the simultaneous growth changes entry_count and is covered.
2. Hunk 03: "remaining" presupposes earlier zeros were raised, which is false for a layer created with one zero
   dimension. Dropped: "only remaining" reads naturally as "the sole grid count still at 0"; no second reading
   changes which case is meant.
3. Hunk 03: "re-emitted" for a layer whose index region did not previously exist (extent slot (0,0)). Dropped:
   §20.3 step 4 itself uses "re-emitted in full" for regions gaining "entries new to this generation"; same usage.
4. Hunk 05: "the bound is that verifier's capability" is singular after "either bound". Dropped: resolves to
   whichever bound was applied; no reading assigns it to the wrong one, and "the bound it applied" later in the
   same requirement uses the same singular the same way.
5. Hunk 05: the following Note says a resource decline under [R-ERR-04] is "at the whole file, a document having
   no declared size", which reasons only from the decoded-size bound though the frame does declare a window.
   Dropped: pre-existing, about a reader's scope of refusal rather than the verifier verdict the hunk governs,
   and the window paragraph's own "the reader MAY decline it ([R-ERR-04])" is not in the hunk. Not a
   contradiction with "either".
6. Hunk 05: the SHOULD-report names the bound and the extent length but not the record's owning scope, which
   [R-MTA-10] requires for ignored records. Dropped: pre-existing, SHOULD-level, no verdict forks.
7. Hunk 21: "any tile whose decoded image the permutation does not fix" ranges vacuously over unstored tiles
   (an all-fill image with a multi-byte fill is not fixed by the permutation, yet no stored bytes exist to
   change). Dropped: "changes the stored bytes of" a tile with none is vacuous, not false; item 6 stores no such
   tile anyway.
8. Hunk 21: §20.3 step 4's carve-out names only "a filter whose mandated stride makes it the identity", not the
   n = 1 case Appendix G also names. Dropped: §20.3 states the test is the effect and its list "names where that
   effect arises rather than standing on its own"; also the clause is pre-existing context, not the changed text.
9. Hunk 21: "elsewhere" is redundant once the "does not fix" qualifier is present (where the permutation is the
   identity, no image fails to be fixed). Dropped: redundant, not wrong.

## Derived numbers
- Identity condition of the [R-COD-10] permutation: i(n−1) = j(s−1) for all 0≤i<s, 0≤j<n ⇔ s=1 or n=1. Compared
  against item 5's "where the stride is 1 ... and equally where ... n = L/s being 1" — agree.
- Shuffle of [01 02 02 03] at s=2,n=2 -> [01 02 02 03] (fixed); of [01 02 03 04] -> [01 03 02 04] (not fixed).
  Compared against the repaired sentence — true of both.
- Grid cases: E=(0,100),T=(10,10): G=(0,10), N=0 -> grow E₀ to 5: G=(1,10), N=10. E=(0,0): grow one: N=0; grow
  both: N=1. Compared against the two Rationale sentences — agree.
- extent_length = entry_count×20 + ⌈entry_count/2¹⁶⌉×4: strictly increasing in entry_count -> "changes
  extent_length with it" holds.
- Count of bounds a reader declines on in §18.2 above line 2662: 2 (decoded-size, window). Compared against
  "either" — agree.
- Count of "fixed" occurrences in Appendix G (grep -c over lines 4510-4667): 7 lines, all in the "pinned" sense
  except the two in the hunk.

## Confidence
Two of three hunks yielded no finding. What would have caught one: the grid cases for hunk 03 (a wrong adjective
would have mis-sorted Layer A); the bound count for hunk 05 (a third bound or a non-decline bound would have
broken "either"); the constructed fixed/non-fixed images and the T26/§21.7 search for hunk 21 (a check that
infers the filter from a fixed image would have falsified the corollary). Not checked: conformance vectors and
tooling (access rule); whether the round's stated defect for each hunk was the one I reconstructed (no ADR
access) — I judged each repair against the passage and the normative rule instead.
