# Audit transcript — lane "the-bar" (hunks 04, 07, 08, 09)

## 0. Disclosure

Read:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-04.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-07.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-08.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/case/hunk-09.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md — by sed ranges: 95-116, 152-225, 285-330,
  342-402, 684-756, 1068-1180, 1225-1235, 1595-1730, 1808-1932, 1933-2130, 2131-2255, 2256-2360, 2455-2546,
  2618-2630, 2941-3045, 3046-3320, 3320-3422, 3423-3500, 3571-3656, 3711-3804, 3839-3952, 4020-4050,
  4161-4200, 4668-4739; plus greps over the whole file (listed in §6).

Did not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json,
git history/log/diff, full.diff, any other hunk file, the case directory listing, the out directory.

Wrote:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-audit/scratch/the-bar/ordinals.py (derivations, reads no files)
- this file.

Unrequested context: my runtime placed a project-instruction pointer (CLAUDE.md -> AGENTS.md), an index of four
memory-note titles, and a git-status block with five recent commit subjects into my context before I began. I
opened none of the files those pointed at and drew no conclusion from them. I note that one commit subject
named the round number and another the ADR series; neither was used.

Hunk files were where the brief said. Each hunk header's line range matched its body in the current file
(verified by grep, §1 below).

## 1. Hunk header verification

grep -n 'run partition, the byte placement of any run, or the slab' -> 2320  (hunk 04 says 2320-2322) OK
grep -n 'the set of padding positions (§11.3), the pad bits'        -> 3152  (hunk 07 says 3152-3155) OK
grep -n "fill is a legal sample value. The bar's"                     -> 3222  (hunk 08 says 3222-3227) OK
grep -n 'is not one. A shrink whose damage falls'                     -> 3261  (hunk 09 says 3261-3264) OK
Nearest headings: 2286 "16.2 The slab declaration" (hunk 04); 3088 "20.3 The append procedure" (07,08,09). OK.

## 2. The passages, as read

§16.2 in full (2286-2360): [R-SLB-02] run partition over disk ordinals; [R-SLB-03] invariants (packed in
ordinal order; first stored tile offset mod A_slab = 0; sentinels and structural reject-tile entries
transparent; crc-only failures not transparent; empty run imposes nothing; verifier MUST check, reject-layer);
[R-SLB-04] (the hunk-04 paragraph); three blocks labeled **Note.** below it.

§20.3 step 4 in full (3130-3281). Governing clauses above the hunks:
- 3148-3151: "A commit MUST NOT change a layer's declarations in a way that alters, for any tile that layer
  stores **in the generation this commit supersedes**, what §14 fixes for its stored bytes or how they decode —"
  then the list (hunk 07), "Call this the **§14 bar**."
- 3157-3158: "The tense is the prior generation's (§3.1 defines *stored* against a generation)".
- 3161-3169: "The test is the effect on such a tile, and the list names where that effect arises rather than
  standing on its own: a change that leaves every one of those tiles' stored bytes meaning exactly what they
  meant — a filter whose mandated stride makes it the identity ([R-COD-10]), or a new padding position whose
  stored byte already holds the fill [R-SER-05] fixes — is not what this bars."  (the carve-out)
- 3236-3238: "the §14 bar is the whole of the test of what a shrink **alters**, **in that bar's own tense**"
- 3253-3258: "What counts as such an alteration is the §14 bar and nothing else, its carve-out included".

Normative-placement test applied: [R-CNF-01] (line 105-107) exempts text *labeled* Note/Example/Rationale,
§1, and non-normative appendices. Hunks 07/08/09 sit in the body of numbered step 4, no label. Hunk 04 sits in
a plain paragraph of §16.2, no ">" marker and no label. All four land in normative text. The block at 2328
("**Note.** Because this rule's detection *is* [R-SLB-03]'s ...") is labeled Note and is non-normative; it is
consistent with the repaired [R-SLB-04] but carries no force, and nothing in the repair relies on it.

## 3. Hunk 04 — [R-SLB-04]

Rule adopted: an updater's commit that (a) changes the stored-tile set, (b) changes the run partition, (c)
changes the byte placement of any run, or (d) changes the slab declaration itself, of a layer that is
slab-declared in the superseded generation OR in the new one, must leave every run of the new generation
satisfying [R-SLB-03], or must clear the declaration in the new generation. Two widenings: (d) is new; "in
either the superseded or the new generation" is new (the old text said "of a slab-declared layer", tenseless).

Check 1 (tense/quantifier): both generations now named explicitly. "any run" / "every such run": "such" has
no clean antecedent (the trigger's only "run" noun is "the byte placement of any run"); but under every reading
the effective obligation is the same — [R-SLB-03] is a whole-layer invariant over every run, unchanged runs
satisfy it by immutability ([R-LIF-01]), so "every such run" = "every run the invariant could fail on" in
effect. No fork.

Check 2 (citations): [R-SLB-03] at 2296-2317 — states the invariants and "A verifier MUST check these
invariants (violation: reject-layer, §15.3)" — matches "detected as the invariant failures of [R-SLB-03] are:
by a verifier". PASS. §20.3 cross-references at 3239 ("a slab or alignment declaration ([R-SLB-04],
[R-SLB-01])") and 3276-3277 ("a slab declaration is re-established or cleared ([R-SLB-04])") — both
consistent with either disjunct. PASS.

Check 3: normative, see §2.

Check 4 (contradiction in passage): The Note at 2328 says "a stale declaration carries no register row of its
own: every file exhibiting one exhibits a run whose tiles are unpacked or whose first stored tile is
misaligned" — still true for every case the widened trigger reaches (a newly declared slab whose runs fail
also exhibits L41/L42). The Note at 2335 ("The declaration is never copied blindly ... updater obligations
detailed in §20") consistent. §20.3 example (c) at 3339: "clearing a slab declaration" is a directory-only
commit — under hunk 04 clearing is a change to "the slab declaration itself" satisfied by the second disjunct.
Consistent. No MUST elsewhere in §16.2 collides.

Check 5 (exhaustive claims): "either ... or" — the two generations a commit has; complete. "every such run" —
see check 1.

Check 6 (structure / siblings): Structure = the layer record's placement declarations: A (per-tile
alignment), S, A_slab. Hunk 04 governs S and A_slab (the "slab declaration"). Sibling A is governed by the
§20.3 sentence at 3277-3280 ("an aligned layer's stored tiles — every one the new state keeps ... satisfy its
invariant or the declaration is cleared ([R-SLB-01], [R-CNF-05])"). Both governed.
Derivation of what can break [R-SLB-03]'s invariants (from its own terms: packing in ordinal order within a
run; first stored tile aligned; run membership by disk ordinal per [R-SLB-02]):
  1. storing a new tile in a run — "stored-tile set" NAMED
  2. unstoring a middle tile of a run (leaves a gap) — "stored-tile set" NAMED
  3. superseding a tile's bytes (its offset moves) — "byte placement of any run" NAMED
  4. changing S — "run partition" / "slab declaration itself" NAMED
  5. changing A_slab — "slab declaration itself" NAMED (new)
  6. declaring a slab where none was — "slab declaration itself" + "slab-declared in ... the new generation"
     NAMED (new)
  7. a geometry change that changes N — the blocks [0,N) / [c·N,(c+1)·N) change, so "the run partition"
     (a partition of ordinals, [R-SLB-02]) changes — NAMED
  8. a geometry change that leaves N unchanged but renumbers ordinals (simultaneous grow of one dimension and
     shrink of another). Computed (ordinals.py): G=(2,4)->(4,2), S=4, stored tiles (0,0),(1,0): ordinals
     0 and 4 (runs 0 and 1) become 0 and 2 (both run 0). Two tiles that only needed alignment now need
     packing. Stored-tile set as tiles: unchanged (a tile is a grid cell, §3.1). Run partition of ordinals:
     unchanged. Declaration: unchanged. "byte placement of any run": the run's *composition* changed while
     no byte moved — a stretch to call that a placement change. NOT CLEANLY NAMED. -> finding A-03.
  9. planar channel reorder moving stored tiles between channel blocks — barred outright by the "bar beside"
     (3191-3202) where the moved channels store tiles; where they store none the affected runs are empty and
     impose nothing. Not a slab question.

Check 7: "detected as the invariant failures of [R-SLB-03] are: by a verifier" — governing verbs: repair
"detected ... by a verifier"; [R-SLB-03] "A verifier MUST check these invariants". Same actor, same set (runs of
a declared layer). PASS.

Check 8: rewrite in place, not an insertion. Back-references in the sentence: "such run" (discussed); "the
declaration" in "clear the declaration" = the slab declaration; "a stale declaration" / "forward" — describes
the carried-forward case only; for case 6 (new declaration) nothing is carried forward. The MUST clause reaches
case 6; the consequence for a failing new declaration is [R-SLB-03]'s reject-layer directly. Loose wording,
no gap in obligation or outcome. Rejected as a finding.

Byte-level for A-03: no. The file produced in case 8 exhibits L41 (row 3758) and [R-CNF-05] bars every
conforming writer from emitting it whether or not [R-SLB-04]'s trigger is read to fire. The emittable set does
not move.

## 4. Hunk 07 — the §14 bar's list

Rule adopted: the list of what §14 fixes now names (1) the set of padding positions (§11.3), (2) the pad bits
[R-SER-03] gives a packed planar bool plane, (3) the content [R-SER-05] fixes at both, (4) the decoded size,
(5) the byte offset of any value within the decoded tile image, (6) the sample type each value is read under,
(7) the codec and filter. Member (2) is new; member (3) is widened from "there" to "at both"; member (5) is
renamed from "sample" to "value".

Check 1: the tense is fixed by the governing clause at 3148-3151 ("for any tile that layer stores in the
generation this commit supersedes") and restated at 3157. The list inherits it. PASS.

Check 2: §11.3 (1666-1675) defines padding positions. PASS. [R-SER-03] (2033-2044): "The final byte's high
bits beyond the last value (bit positions P mod 8 through 7, when P mod 8 ≠ 0) are the tile's **pad bits**;
their content is fixed by [R-SER-05]" and "Packing is exclusive to planar bool planes" — so R-SER-03 does
give exactly packed planar bool planes their pad bits. PASS. [R-SER-05] (2100-2109): "at every padding
position, a writer MUST encode ... that channel's fill value ... Every pad bit (§14.3) MUST carry the plane's
channel's fill bit." — fixes content at both padding positions and pad bits. "at both" PASS. §14.2 table
header "Offset of value k" — the renamed member's word is the defining section's word. §3.1: "sample — the
tuple of one value per channel at one coordinate"; a planar tile carries no samples in that sense, so the old
"sample" was wrong for planar tiles and "value" is right for both layouts. PASS.

Check 3: normative body of step 4.

Check 4: the carve-out at 3162-3169 speaks of "a new padding position whose stored byte already holds the
fill"; adding pad bits to the list creates no collision — pad bits cannot become new or cease (they depend on
P alone, and a change to P changes the decoded size, already barred), and their content is fixed to fill, so
the only declaration change reaching them is a fill change, which example (c) at 3339-3346 states is barred
"where that channel carries ... [a] pad bit in any tile the layer stores". Consistent. §21.7 (3904-3905) names
"padding positions, pad bits, and boolean bytes" as the structurally constrained content — consistent with the
list now naming pad bits.

Check 5: no exhaustive word in the list; the sentence after it (3161) says the list "names where that effect
arises rather than standing on its own". So the list is declared non-closed.

Check 6 inventory — every quantity §14 fixes for a stored tile's bytes or their decoding:
  §14.1 [R-SER-01]: value order (planar: channel c's values in in-tile ordinal order; interleaved: sample-major
        in declared channel order); V. [R-SER-06]: layout value set.
  §14.2 [R-SER-02]: per-value encoding (element size, little-endian, bool byte), decoded size P·Bᶜ / P·Q, byte
        offset of value k, Q, Fᶜ. [R-SER-08]: interleaved bool byte in {0x00,0x01}.
  §14.3 [R-SER-03]: LSB-first packing — value k at bit k mod 8 of byte k div 8; decoded size ⌈P/8⌉; pad bits.
        [R-SER-07]: decoded size exactness.
  §14.4 [R-SER-09]: all layout/type combinations defined (nothing to alter).
  §14.5 [R-SER-05]: padding content, pad-bit content.
  Mapping to the list: padding positions (1); pad bits (2); content at both (3); decoded size (4); byte offset
  (5) — covers interleaved channel reorder (Fᶜ changes), dimension reorder in unpacked layouts (k changes and so
  k·Bᶜ), tile-extent change (already changes P); sample type (6); codec/filter (7). Value order in an
  interleaved layer is captured by (5) since a value is identified by (channel, position) and its offset moves.
  Which channel a planar tile carries is the other bar's subject (disk ordinal).
  GAP: the bit position k mod 8 in a packed plane. Computed (ordinals.py): packed planar bool plane, T=(2,4),
  P=8, no padding; reorder the dimensions to (x,y), T'=(4,2). Coordinate (y=1,x=0): k 4 -> 1; (y=0,x=1): k 1 ->
  2. Every value stays at byte 0; decoded size stays 1; no padding position, no pad bit, no type, no codec
  changes. Nothing the list names moves, but §14.3 fixes the bit and the tile's one stored byte now decodes to
  a transposed value sequence. The governing clause ("what §14 fixes for its stored bytes or how they decode")
  and the "list names where that effect arises rather than standing on its own" sentence do reach it. So by the
  list's own terms the omission is not a defect of the bar; but the repair renamed exactly this member and left
  it byte-only. -> finding A-02, not byte-level (a competent reader applies the governing clause; the sentence
  after the list forbids reading the list as the test).

Check 7: no analogy in the repaired text.

Check 8: the edit is in place within one sentence. Forward references: "Call this the **§14 bar**" — the
whole MUST NOT sentence, unchanged. "The tense is the prior generation's" — unchanged antecedent. "such a
tile" at 3161 = a tile stored in the superseded generation — unchanged. "there" no longer appears (the repair
replaced "fixes there" with "fixes at both") — verified by normalised search: "the content [R-SER-05] fixes
there" count 0; "fixes at both" count 1.

Restatement sweep: "byte offset of any sample" — 0 hits (normalised); "byte offset of any value" — 1 hit.
Example (c) at 3339-3346 already names "padding position and no pad bit". §11.1 Rationale (1613-1639,
non-normative) restates the carve-out without pad bits; no force, and not wrong. Appendix H (4696, 4728)
names padding and pad bits. Nothing left unswept.

## 5. Hunk 08 — growth as an exception

Rule adopted: a growth of an extent that turns a stored tile's padding positions into real positions is an
alteration the §14 bar's list names ("the set of padding positions"), the carve-out (new padding positions
whose byte already holds fill) does not reach it (it is the reverse direction), and the growth is nevertheless
permitted because "an extent MAY grow" is stated as an exception to the bar — subject to every bound the new
geometry is subject to.

The logic, from the text:
  Prohibition (3148-3155): MUST NOT alter, for a prior-generation stored tile, ... "the set of padding
  positions (§11.3)" ...
  Carve-out (3161-3169): a change leaving every stored byte "meaning exactly what they meant" — examples:
  identity-stride filter; "a new padding position whose stored byte already holds the fill".
  Permission (3220-3222): "an extent MAY **grow**, since a position that becomes real held ... that channel's
  fill (§14.5), and fill is a legal sample value."
  A growth E: 5 -> 6 with T = 4 makes position 5 of tile 1 real (ordinals.py). The set of padding positions
  of that stored tile changes {5,6,7} -> {6,7}: it falls under the prohibition's list. The carve-out's stated
  example is a position *becoming* padding; a position *ceasing* to be padding is not that. Whether the
  carve-out's general principle ("meaning exactly what they meant") could stretch to it is arguable (the byte
  decodes to the same value, but §11.3/[R-GEO-04] change its status from never-returned to returned); the
  hunk settles it by declaring the permission an exception. For the step to be consistent the MAY must
  override the MUST NOT for this one alteration, and the text now says so in normative prose. PASS.

Check 1: "a position that becomes real held ... fill" — past tense "held" = the superseded generation's
stored tile (in a conforming file, [R-SER-05]); "the fill it keeps" — after the change. Actor: writer/updater.
PASS. (An appender does not decode tiles — §19.3 validation has no decoded-content check — so a latent T4
violation in the padding travels, [R-WRT-01]; the permission's reasoning assumes a conforming input, as the
whole step does.)

Check 2: §14.5 (2100-2109) padding holds fill — PASS. [R-COD-07] (2463-2474): cap over "addressed tiles",
"checkable from declarations alone"; L44 row 3761 — PASS (pre-existing). [R-ENC-04] (472) 2⁶³−1 — PASS
(pre-existing).

Check 3: normative body of step 4.

Check 4: shrink paragraph (3236-3264): "the §14 bar is the whole of the test of what a shrink alters" and "A
shrink is permitted exactly where it alters nothing §14 fixes" — shrinks have no exception; growth now has one;
the two do not collide because they are different operations and the text keeps them apart. §11.1 Rationale
(non-normative): "the one reaching a shrink or a growth is the §14 bar" — consistent with growth being under
the bar with an exception. Example (c) 3346-3349: empty-layer redeclaration "subject to every rule its new
geometry is subject to, which is the same step's permission" — consistent. "a growth is permitted exactly
where the geometry it produces satisfies every rule that geometry is subject to" (3233-3234, pre-existing)
remains true: the §14-bar alteration a growth makes is now expressly excepted, so the only remaining
conditions are geometry rules.

Check 5: "does not reach a growth" — universal. A growth (of an extent Eᵢ) can create no new padding
position (padding is ≥ Eᵢ; raising Eᵢ only removes them) and changes neither P nor decoded size, so no
carve-out case arises in a growth. Holds.

Check 6: structure = the padding set of a stored edge tile under a geometry edit. Both directions now
governed: position -> padding (carve-out, shrink paragraph); padding -> position (this exception). Pad bits:
unaffected by E. Decoded size: unaffected by E. Ordinal renumbering by a growth: the re-emission rule's
"geometry change renumbers ordinals" (3142) and the "bar beside" (3191-3195, planar channel declarations
only). Nothing left ungoverned.

Check 7: no analogy ("rather than one the carve-out supplies" is a contrast, not a warrant).

Check 8, anaphors in the insertion:
  "The bar's carve-out" — nearest "bar" mention is "both bars'" (3219); ambiguous by proximity, but the
  description that follows ("covers a position whose stored byte already holds the fill") is the §14 bar's
  carve-out verbatim, and the other bar has none. Resolves.
  "it covers" — the carve-out. "the fill it keeps" — the stored byte (or the position): after the change the
  byte still holds fill; either reading is the same fact. "not one that ceases to be padding" — a position.
  "so this is an exception" — the growth permission. "the permission states" — "an extent MAY grow".
  "It holds provided ..." — candidates: the exception / the permission / the carve-out. The third makes no
  sense with "holds provided the grown geometry"; the first two are the same licence. Resolves to the growth
  permission, as the pre-repair "— provided the grown geometry" did.
  Forward from the insertion: "is another" (3232) = another bound — unchanged; "the list is not offered as
  exhaustive" = the list of bounds — unchanged; "its carve-out included" (3254) = the §14 bar's carve-out — the
  new sentence also names "the bar's carve-out" and describes the same clause, so the two agree.
  Backwards: the inserted text's "The bar" reaches back past "both bars'" to "the §14 bar"; acceptable given
  the description, noted as a rejected candidate.

Rejected candidate: the insertion characterises the carve-out narrowly ("it covers a position whose stored
byte already holds the fill it keeps") while the carve-out at 3162 is stated as a principle with two
examples. "Covers X, not Y" does not say "covers only X", and the original carve-out sentence stands, so no
narrowing lands. Also, whichever way the carve-out is read, growth is permitted: no fork.

## 6. Hunk 09 — the antecedent

Rule adopted (explanatory, in normative text): the shrink that the "no rescue" rule bars — one that alters
what §14 fixes for a prior-generation stored tile which the new state no longer stores (de-addressed or
sentinelled) — is the case no obliged check can see, because the live state carries no tile to check; that
is why the rule is stated in the step rather than by a register row.

Check 1: "a tile the new state no longer stores" — new-generation tense, explicit; the bar's own tense is the
prior generation's (3157, 3237, 3249-3252) and the sentence keeps both straight. Actor for "has no witness": a
reader or verifier holding the file, per §21.7's definition. PASS.

Check 2: [R-CNT-21] (684-727) — unclaimed bytes are slack — PASS for "de-addressed tiles' extents become
slack". [R-CNT-17] (1106-1111) — entry_count equals the addressed-tile count and extent_length follows — PASS
for "obliges the smaller entry_count and so a re-emitted index region" (a changed extent_length forces a new
region under [R-LIF-01]). §21.7 (3911-3924): "unwitnessed where, for every file exhibiting it, some file that
does not exhibit it cannot be told apart from it by any check this specification obliges a reader or a
verifier to perform"; "Being unwitnessed bears on detection and not on permission". The sentence's "has no
witness" is used in that sense (as at 1172, 3479, 3908). PASS.

Check 3: normative body of step 4.

Check 4: §23.1 [R-PRV-01] (4178-4183): "a shrink turning real positions into padding of a tile the new state
still stores — ... §20.3 step 4 permits that shrink only where those bytes already hold the channel's
recorded fill". This is the complement of hunk 09's class and agrees with it. The shrink paragraph's
"Unstoring that tile in the same commit does not rescue it either" (3248-3252) is the rule the sentence
explains — no collision.

Check 5 — "precisely where", tested in both directions:
  Inside the class: E=7, T=4, tile 1 stored with real positions 4,5,6 holding non-fill; shrink to E=4
  de-addresses tile 1; or shrink to E=6 and sentinel tile 1 in the same commit. The live state stores no tile
  1; its bytes are slack ([R-CNT-21], content unconstrained); the resulting file is indistinguishable from a
  freshly written file with those declarations and that tile unstored. No obliged check separates them. No
  witness. HOLDS.
  Outside the class, among shrinks: E=7 -> 6, tile 1 still stored, position 6 held non-fill. Position 6 is now
  a padding position not encoding fill -> T4 (row 3781, [R-SER-05], verifier, certification). Witness exists.
  Shrinking an extent changes nothing else §14 fixes (P, decoded size, offsets, types, pad bits all
  independent of Eᵢ), so every still-stored damage is a T4 case. HOLDS among shrinks.
  Outside shrinks: the sentence's predicate is "is precisely where the §14 bar has no witness", not "is the
  shrink at which". Re-typing a channel int8 -> uint8 on a still-stored tile is barred (3172-3175) and yields
  a conforming file (every bit pattern is a value, [R-TYP-05]; no row) — no witness. Swapping two same-size
  channels of an interleaved layer: barred (Fᶜ moves), conforming output, no witness. So the §14 bar is
  unwitnessed in places the sentence's class does not name. Read in its paragraph the claim is about shrinks;
  read as written it overclaims. -> finding A-01, not byte-level.
  Quantifier nit inside the class: "whose damage falls on a tile the new state no longer stores" — a shrink
  whose damage falls on one dropped tile AND one still-stored tile has a T4 witness via the second; the class
  as stated ("a tile") includes it. §11.1's Rationale notes "One shrink can do several of these at once".
  Folded into A-01's repair ("only on tiles").

Check 6: the structure is the pair (bar, witness) over shrink outcomes: dropped tile / sentinelled tile / still
stored with fill / still stored without fill. All four are now assigned: permitted-and-clean, barred-unwitnessed
(x2), barred-T4. Nothing left open.

Check 7: "exactly as it is there" (3256) is pre-existing and untouched; both sides are the same carve-out
applied to the same set (new padding positions of prior-generation stored tiles). PASS.

Check 8: replacement of "This is precisely where" by an explicit subject; no insertion between sentences.
Forward: "which is why the rule is stated here and not left to the rows" — "the rule" = the no-rescue rule
(3248-3252) or, equally, the §14 bar as applied to it; unchanged from before the repair since the intervening
"bar beside" sentence was already there. "Where a shrink is permitted ..." (3265) — unchanged. "every surviving
stored tile is untouched" — consistent with the class. Backwards: "the §14 bar", "the live state", "the rows"
— all defined earlier in the step or the document.

## 7. Sweeps run (verbatim) and hit counts

Line greps over spec/tarn.md:
  grep -n -i 'witness'                                   -> 8 hits (1172, 2625, 3262, 3479, 3908, 3911, 3923, 3938, 3944)
  grep -n -i 'pad bit\|padding position\|padding bit'    -> 27 hits (listed in transcript above)
  grep -n -c 'slab-declared'                             -> 1 (2321)
  grep -n -c 'stale'                                     -> 9 (2324, 2328 and seven unrelated uses)
  grep -n 're-establish'                                 -> 2 (2323, 3276)
  grep -n 'slab declaration'                             -> 5 (1082, 1105, 1132, 2286, 3276)
  grep -n 'carve-out'                                    -> 3 (3223, 3226, 3254)
  grep -n 'byte offset'                                  -> 2 (603, 3154)
  grep -n 'offset of any sample'                         -> 0; control grep 'offset of any value' -> 0 (wraps: "any\n   value") — zero not trusted, see normalised search
  grep -n -i 'MAY \*\*grow\|may grow\|a growth\|growing extents\|grow extents\|grows its extents' -> 8
  grep -n -i 'shrink'                                    -> 17
  grep -n 'precisely where'                              -> 1 (3262)
  grep -n 'whole of the test'                            -> 1 (3926; the step's phrase at 3236-3237 wraps and is missed — control confirms wrap effect)
  grep -n -i 'reorder\|dimension order\|declared order'  -> 7
  grep -n 'fill it keeps'                                -> 1 (3224)
Whitespace-normalised search (blockquote markers and backticks stripped, all whitespace collapsed):
  the pad bits [R-SER-03] gives a packed planar bool plane, and the content [R-SER-05] fixes at both -> 1
  the content [R-SER-05] fixes there                        -> 0   (old wording gone)
  the byte offset of any value within the decoded tile image -> 1
  the byte offset of any sample within the decoded tile image -> 0 (old wording gone)
  what §14 fixes for its stored bytes or how they decode     -> 1
  detected as the invariant failures of [R-SLB-03] are: by a verifier -> 1
  the sample type each value in the image is read under      -> 1
  The bar's carve-out does not reach a growth                -> 1
  an exception the permission states                         -> 1
  It holds provided the grown geometry                       -> 1
  no longer stores is precisely where                        -> 1
  This is precisely where                                    -> 0   (old wording gone)
  slab-declared in either the superseded or the new generation -> 1
  the slab declaration itself                                -> 1
  carrying a stale declaration forward                       -> 1
  the byte placement of any run of a slab-declared layer     -> 0   (old wording gone)
  every such run                                             -> 1
  stale declaration                                          -> 2 (2324 normative, 2328 Note)
  re-established or cleared                                  -> 1
  padding positions, pad bits, and boolean bytes             -> 1 (§21.7)
  no padding position and no pad bit                         -> 1 (example (c))
  every surviving stored tile is untouched                   -> 1
  Controls (known present): "whose only defect is that its stored bytes fail its crc" -> 2;
  "Runs partition each contiguous block of disk ordinals" -> 1; "packed planar bool plane" -> 3.
  The first pad-bits phrase returned 0 before backticks were stripped and 1 after — the normaliser was
  corrected and the control re-run.

## 8. Derived numbers

The charter names no document figure. Computed: (i) same-N renumbering: G=(2,4)->(4,2), N=8 both, tiles
(0,0),(1,0) at ordinals 0,4 -> 0,2; with S=4 runs {0,1} -> {0,0}. (ii) packed plane P=8, T=(2,4)->(4,2):
coordinate (1,0) k=4->1 (byte 0 bit 4 -> byte 0 bit 1); (0,1) k=1->2; decoded size ⌈8/8⌉=1 both. (iii) E=5,T=4:
grid 2, tile 1 real {4}, padding {5,6,7}; E=7->6 keeps tile 1 stored and makes position 6 padding.
Inventory counts: §14 has 5 subsections and 8 live requirement IDs (R-SER-01,02,03,05,06,07,08,09; 04
withdrawn); the repaired list has 7 members.

## 9. Findings

A-01 (hunk 09, OVERCLAIM, not byte-level) — "is precisely where the §14 bar has no witness" is exact among
shrinks and false about the bar at large (re-typing int8/uint8, same-size interleaved channel swap are barred,
conforming, unwitnessed); and "a tile" admits a shrink that also damages a still-stored tile, which has a T4
witness. Repair: "Among shrinks, one whose damage falls only on tiles the new state no longer stores is
precisely where the §14 bar has no witness, ...".

A-02 (hunk 07, UNCONSTRAINED_SIBLING, not byte-level) — "the byte offset of any value" does not name the bit
position §14.3 fixes in a packed planar bool plane; a dimension reorder on a P ≤ 8 plane moves values between
bits and no byte offset, so nothing the list names changes; the governing clause reaches it. Repair: "the byte
offset — or, in a packed plane, the bit position — of any value within the decoded tile image".

A-03 (hunk 04, UNDERSHOT, not byte-level) — the widened trigger does not cleanly name a geometry change that
renumbers ordinals with N unchanged (grow one dimension, shrink another), which moves stored tiles between
runs and can break packing while leaving the stored-tile set, the run partition of ordinals, and the declaration
all unchanged. The output file carries L41 and [R-CNF-05] bars it under either reading. Repair: add "the disk
ordinal of any stored tile" to the trigger list.

## 10. Rejected candidates

- Hunk 04 "carrying a stale declaration forward" does not describe a newly declared slab — the MUST clause
  reaches it and the outcome is [R-SLB-03]'s in every case; dropped.
- Hunk 04 "every such run" has no clean antecedent — every reading yields the same obligation because
  [R-SLB-03] binds every run of the new generation and unchanged runs hold by immutability; dropped.
- Hunk 08 "It holds provided" — three candidate antecedents, two of which are the same licence and the third
  ungrammatical with the predicate; dropped.
- Hunk 08 "The bar's carve-out" after "both bars'" — identified by its description; dropped.
- Hunk 08 characterises the carve-out narrower than its "meaning exactly what they meant" principle — "covers X,
  not Y" is not "covers only X", and growth is permitted under either reading; dropped.
- Carve-out's "stored byte" for a packed plane (a padding position there is a bit) — pre-existing wording at
  3167 and 3255, untouched by any of my hunks, and a reader maps it to the bit; dropped.
- Hunk 07 pad-bits member colliding with the carve-out — pad bits cannot become new; dropped.
- Hunk 09 "the rule is stated here" antecedent — unchanged by the repair (the intervening sentence pre-dates it);
  dropped.

## 11. Byte-level verdicts

None of A-01..A-03 forks emitted bytes or accept/reject verdicts. A-01 is a detectability statement.
A-02 dies on the governing clause at 3150-3151 and the sentence at 3161 — a competent implementation applies
"what §14 fixes ... or how they decode", under which the packed-plane reorder is barred. A-03's disputed file
exhibits L41, so [R-CNF-05] bars it from every conforming writer regardless of [R-SLB-04]'s trigger.
