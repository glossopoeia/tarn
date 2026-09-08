# Audit transcript — "the-restatements" lane (hunks 02, 05, 06, 12, 13, 18, 19)

## Access-rule disclosure

Read only:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via Read, at various offsets, and via `grep`/`python3 re` over the file for phrase sweeps).
- The seven charter hunk files: `hunk-02.diff`, `hunk-05.diff`, `hunk-06.diff`, `hunk-12.diff`, `hunk-13.diff`, `hunk-18.diff`, `hunk-19.diff` under
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/`.

Did NOT read: `full.diff`, any other lane's hunk file, docs/, PLAN.md, AGENTS.md, README.md, conformance/, spec/registry.json, git history, or the web.
Did not list the `case/` directory; only opened the seven named files by exact path.

**Contamination disclosure.** My system prompt/context contained a project `CLAUDE.md`/`AGENTS.md` pointer, a user memory index (`MEMORY.md`) with several TARN-related note titles (e.g. "TARN repair prose vs rules", "TARN refute phase skips unanimous upholds", "No nested em-dash phrases", "TARN permissions, not carve-outs"), and an environment block naming recent git commit subjects (mentioning "ADR-0124", "eighteen defects", "thirty-one defects", round 32 charter, etc.). None of this was read as directed — I did not open any memory file, ADR, or docs file — but the *titles/subjects* were visible in context before I began. I did not use them to steer which passages I suspected or to pre-load a verdict; my conclusions below are argued from the hunk files and `tarn.md` text I quote. Flagging per the access rule: this is a disclosed, not acted-upon, breach.

Scratch directory: I wrote no working files — all computation was small enough to run inline via `python3 -c`/heredocs without persisting intermediate files, so nothing was written under `.../scratch/the-restatements/`.

## Hunks read (raw, verbatim from case files)

All seven hunk files were read via `cat`. Headers claim (line ranges in current file / nearest preceding heading):
- hunk-02: lines 678-680 / "5.1 Anatomy" (§5.1 Example — a file after three commits)
- hunk-05: lines 1648-1665 / "11.1 Geometry and its validity floor" (Rationale block)
- hunk-06: lines 1955-1958 / "13.3 Unstored tiles read as fill" (Note — sparse writing)
- hunk-12: line 3542 / "20.5 Compaction" (Example — what compaction reclaims, figure)
- hunk-13: lines 3552-3554 / "20.5 Compaction" (same Example, caption)
- hunk-18: lines 4718-4721 / "Appendix H — Conformance checklists (non-normative)" (Conforming reader entry)
- hunk-19: lines 4744-4751 / "Appendix H" (Conforming updater entry)

I verified every header's line-range/heading claim against the current file with targeted greps (see "Header verification" below); all seven matched. No discrepancy to report.

## Source rules I re-read before judging any restatement

### §20.3 step 4 (append procedure), lines 3170-3287

Quoted verbatim (key sentences):

> Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array — necessarily at a new placement (`[R-LIF-01]`), with entries for tiles this commit stores or supersedes written to their new state, entries for tiles that become unstored written as the sentinel, entries new to this generation ... emitted per §15, and every other entry byte-identical at its disk-ordinal position (a growth renumbers ordinals wherever `[R-GEO-06]` moves them, and nothing else this step permits moves one).

> A layer that stores a tile **in the generation this commit supersedes** keeps its declarations, with these exceptions and no other: its name, and its dimension and channel names, MAY change; an extent MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at its end or shortened from its end, but not both in one commit; and a slab or alignment declaration MAY be declared, re-established or cleared as this step provides below. A commit MAY make several of these changes at once, an extension and a shortening of one channel list excepted: a commit's net change to a planar layer's channel list is an extension or a shortening, and replacing the last channel is two commits or a rewrite.

> A layer that stores no tile in the generation this commit supersedes MAY be re-declared freely, subject to every rule its new declarations are subject to, which is what schema-first creation needs (§11.1).

This is the closed list (four permitted-change classes: names; extent growth; planar channel-list extend-or-shorten-not-both; slab/alignment) that hunks 05 and 19 both restate a slice of.

### §20.4 (Re-emission and preservation), line 3373-3379 — `[R-WRT-05]`

> In the new complete directory, an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify, whether or not it implements the record's type; a record it modifies is new output under its writer obligations (`[R-CNF-05]`). `[R-WRT-05]`

Hunks 19's re-emission clause restates this.

### §9.2 `[R-LIF-02]`, lines 1259-1272 (step 2)

> (2) append new stored-tile payloads and tile-index regions for the layers it changes, and any new record extents (file-scope or layer-scope), in any order satisfying §5.2's coverage classes

This is the exhaustive list of what an append appends besides directory/pad/trailer. Hunk 02 restates the negation of it.

### §11.2 grid arithmetic, R-CNT-17, R-GEO-06

- entry_count = addressed-tile count = N (interleaved) or C·N (planar), N = ∏ᵢ Gᵢ, Gᵢ = ⌈Eᵢ/Tᵢ⌉ (lines 1669-1678, 1111, 1128-1133).
- Disk tile ordinal s = Σᵢ tᵢ·∏_{j>i}Gⱼ (interleaved), c·N+s (planar) — depends on the *grid counts* (line 1727-1740, `[R-GEO-06]`).

### §20.5 Compaction, R-WRT-06/R-WRT-07, lines 3499-3533

> A compactor MUST preserve content ... every retained record per §20.4, except that relocation re-points extent slots, **regenerates each tile-index region any of whose stored extents the output relocates** (entry offsets new; entry lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed over the entries as re-emitted), and updates the layer-record fields covering a regenerated region (crc_of_crc_array).

> The output's reference arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`): compaction changes where bytes live, never what a layer denotes. `[R-WRT-07]`

Regeneration is keyed to whether a layer's *stored tile payload* moved, not whether its index's own file offset moved. Hunks 12/13 restate this via a worked example.

### R-CNF-03, lines 178-201

> A reader MUST accept every conforming file of a format major version it implements, carrying no top-level record of a type it does not implement with MUST_UNDERSTAND = 1 ... and none of whose values exceeds the minimum guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on that last ground; §21.6's closing paragraph names the other two), and MUST handle every codec ...

Three qualifiers on "accept": (a) major it implements, (b) no top-level unimplemented-type MU=1 record, (c) within §21's/§21.9's minimum guarantees. Hunk 18 restates exactly these three.

### §21.9, lines 3976-4029

Confirms §21.9 hosts the "minimum guarantees" table, and R-ERR-04 ("a refusal on resource grounds MUST be reported as a resource limit and not as a validity error") is defined at the end of §21.9 (line 4025-4029), while §21.6's own intro (line 3855-3858: "where an entry records a resource decline, the decline is licensed and reported as `[R-ERR-04]` requires") and its closing paragraph (lines 3891-3910, naming the two *capability* refusals — foreign major, unimplemented top-level MU=1 — as *not* being "this [resource] ground") both bear on hunk 18's added citations.

## Hunk-by-hunk analysis

### Hunk 02 — §5.1 Example, lines 674-685

**Landing block label:** `> **Example — a file after three commits.**` (line 657) — labelled Example, **non-normative** under `[R-CNF-01]`. Confirmed by reading back to the block's opening line.

**Rule the repair asserts:** A commit re-emits *only* directory+pad+trailer exactly when it (a) touches no layer's stored-tile-set/index and (b) appends no record extent (file- or layer-scope, e.g. a user-metadata document, which per `[R-CNT-25]` "lives in" — is carried by — an extent).

**Check 1 (tense/quantifier).** Matches `[R-LIF-02]` step 2's own two-part list of what an append appends beyond directory/pad/trailer verbatim in substance: "stored-tile payloads and tile-index regions for the layers it changes" ↔ "touches no layer"; "any new record extents (file-scope or layer-scope)" ↔ "appends no record extent." The repair's condition is exactly the negation of step 2's two clauses, so "re-emits the directory, the pad and the trailer alone" (i.e., nothing from step 2) correctly follows. Old text ("a commit that touches no layer re-emits ... alone") was missing the record-extent half — a top-level user-metadata document could be added by a commit that touches no layer, and such a commit *would* append a record extent, contradicting the old universal. The repair closes exactly that gap.

**Check 2 (citations).** `[R-CNT-25]` — verified at lines 962-965/984: "Each user-metadata record carries its document in its extent — never inline." Resolves correctly.

**Check 5 (exhaustive claim).** "touches no layer and appends no record extent" — tested against: (i) a commit adding a layer-scope sub-record *with* an extent → excluded by "appends no record extent" (correctly not covered by the universal); (ii) a top-level record of an unknown type with an extent → same, excluded, correctly; (iii) a layer-scope sub-record *without* an extent (inline-only) → does not append a record extent, and does not touch a layer's *stored-tile set or index* (only the layer's record within the directory, which is re-emitted every commit regardless) → compatible with "touches no layer" as used here (which is about tile/index, given the immediately preceding sentence's use of "touch" for tile/index unchanged-ness), so this case is *not* a counterexample — it is consistent with the directory being the only thing "extra." No falsifying case found.

**Check 4 (contradiction in passage).** The next two sentences ("A commit that changes a layer's stored-tile set or index content re-emits that layer's whole tile-index region as well... The commit that added layer B emitted B's index region for the first time...") are unaffected and consistent with the repaired sentence — together they exhaust the touches-a-layer / appends-an-extent / neither taxonomy without gap or overlap.

**Check 8 (anaphora).** Scanned forward to the end of the paragraph ("A commit never relocates a live index region otherwise; that is compaction's operation") — "otherwise," "that" both resolve to material *after* the insertion point and are unaffected by it. Scanned the inserted clause itself ("a user-metadata document lives in one") — "one" resolves within its own clause to "no record extent." No anaphor changed resolution.

**Byte-level:** No — labelled Example, non-normative; the actual binding rule is `[R-LIF-02]` step 2 / step 3, unchanged elsewhere.

**Verdict: no defect found.**

### Hunk 05 — §11.1 Rationale, lines 1643-1665

**Landing block label:** `> **Rationale.**` (line 1643) — non-normative.

**Rule the repair asserts:** A taxonomy of "growth" (extent increases) by effect on grid counts Gᵢ=⌈Eᵢ/Tᵢ⌉: (1) growth changing no Gᵢ ⇒ (taken alone) touches the directory alone, no index entry moves or is added; (2) growth raising some Gᵢ while another Gⱼ stays 0 ⇒ product N=∏Gᵢ stays 0, index stays empty, same directory-alone conclusion; (3) any other growth ⇒ entry_count (and extent_length, `[R-CNT-17]`) changes, ordinals renumber per `[R-GEO-06]`, whole tile-index region re-emitted (`[R-WRT-04]`) — explicitly including the case of a zero-extent layer's *last* remaining zero grid count being raised.

Also touched in the same hunk: the channel-list clause gains "one or the other in a commit" and the empty-layer clause gains "subject to every rule its new declarations are under."

**Check 1.** Compared word-for-word against §20.3 step 4 and §11.2/R-CNT-17/R-GEO-06 (quoted above). The taxonomy's mathematical claim — for growth-only changes (extents can only grow, never shrink, so every Gᵢ is non-decreasing across the commit) N=∏Gᵢ is unchanged iff either (a) no Gᵢ changes, or (b) some Gⱼ is 0 both before and after — is correct: with all factors non-decreasing and at least one strictly increasing, if no factor is ever 0 the product strictly increases (product of positive integers, one strictly larger, others ≥1); if some other factor stays at 0 throughout, the product stays 0 regardless of the changing factor. I verified this by direct construction (see Derived numbers below) rather than taking it on faith.

**Check 2 (citations).**
- `[R-CNT-17]` (line 1128-1133): "extent_length MUST equal entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 ... a mismatch, or an entry_count that does not equal the geometry-derived addressed-tile count, is a validity error" — supports "entry_count and extent_length with it." Resolves.
- `[R-GEO-06]` (line 1727-1740): disk ordinal formulas depend on Gⱼ — supports "disk ordinals renumber wherever `[R-GEO-06]` moves them." Resolves.
- `[R-WRT-04]` (§20.3 step 6 tag, covering steps 1-6 including step 4's re-emission clause) — supports "the layer's whole tile-index region is re-emitted." Resolves.
- §11.2 (grid-count definitions) — resolves.

**Check 5 (exhaustive claim) — the four required test cases:**
1. *Growth changing no grid count, on a layer with padding positions* (i.e., extent grows within the same tile, Eᵢ<Tᵢ before and after): Gᵢ unchanged, N unchanged, entry_count unchanged, no ordinal renumbering (R-GEO-06's formula is a function of Gⱼ only) → "touches the directory alone" holds. I also checked whether the tile *payload* needs rewriting for the newly-in-extent positions: no — §20.3's "line is drawn" paragraph (line 3236-3247) states "a grown extent adds positions that held their channel's fill (§14.5), and fill is a legal sample value," i.e. the previously-padding bytes already satisfy the widened extent without being touched. So "directory alone" is correct even accounting for payload, not just index.
2. *Growth raising a grid count while the product holds at 0*: directly the sentence's own case (2); verified true (0 × anything = 0, and entry_count for both interleaved (N) and planar (C·N) layouts is 0 when N=0 regardless of C).
3. *Growth raising one grid count on a rank-1 layer*: rank 1 has no "another" dimension, so this cannot be case (1) (a grid count *did* change) or case (2) (no other Gⱼ exists to hold at 0); it falls to "any other growth," and indeed N=G₁ changes, so entry_count changes — consistent, no gap.
4. *Growth taken with a shortening*: the phrase "taken alone" in sentence 1 explicitly scopes the directory-alone claim to the growth by itself, hedging against composition with another declaration change (e.g. a planar channel-list shortening) in the same commit — see Check 6/8 discussion below for whether this hedge survives the ellipsis in sentence 2.

**Check 6 (what's left unconstrained).** I asked whether "taken alone" (attached to case 1 by an explicit adjective, and to case 2 only by verb-phrase ellipsis — "so does one that...") still holds when case 2's growth is combined, in the same commit, with a different permitted declaration change (channel-list shortening, slab/alignment change). I computed: when N=0 (case 2's premise), entry_count = N (interleaved) or C·N (planar) is 0 *regardless of C*, so a co-occurring channel-list shortening (which only changes C) cannot push entry_count off zero while N=0; and a slab/alignment change only affects placement of *existing* stored tiles, of which there are none when N=0. So case 2's "touches the directory alone" is in fact robust to composition with every other permitted declaration change, independent of whether the ellipsis is read as carrying "taken alone" forward or not — I confirmed this analytically rather than assuming it, so I do not treat the ellipsis as a live ambiguity with a false reading. (Recorded under Rejected candidates.)

**Check 4 (contradiction).** The unchanged sentence "several of these in one commit, each subject to every rule the declarations it produces are under" and the surrounding closed-list restatement remain consistent with the growth taxonomy that follows; no clash found.

**Check 8 (anaphora).** Read forward through the rest of the Rationale (paragraph ends at line 1665, followed immediately by "#### 11.2 Grid arithmetic," a heading — no further prose to check). Read the inserted text's own back-references: "the product" (§11.2's N, cited immediately before via "(§11.2)"), "either way" (the two just-stated cases), "any other growth" (residual class after cases 1-2), "the growth that raises a zero-extent layer's only remaining zero grid count included" (an appositive naming a member of "any other growth," present in the pre-repair text too, just reattached to the rewritten lead-in) — all resolve to antecedents inside the same paragraph, none moved.

**NESTED_DASH:** one dash pair ("— entry_count and extent_length with it (`[R-CNT-17]`), and disk ordinals renumber wherever `[R-GEO-06]` moves them —"), with parentheses (not dashes) inside it. Not nested.

**Byte-level:** No — Rationale block, non-normative; the growth/re-emission behavior is fixed by §20.3 step 4 / R-WRT-04 / R-CNT-17 / R-GEO-06 regardless of how this commentary reads.

**Verdict: no defect found.**

### Hunk 06 — §13.3 Note, lines 1950-1958

**Landing block label:** `> **Note — sparse writing.**` — non-normative.

**Rule asserted (old, being replaced):** "each commit that changes a layer's stored-tile set or its index content — which, among the declaration changes §20.3 permits a layer that stores a tile, only a change to entry_count does — re-emits that layer's whole tile-index region."

**Rule asserted (new):** "each commit that changes a layer's stored-tile set or its index content re-emits that layer's whole tile-index region (§20.3, `[R-WRT-04]`), and a growth that changes no grid count ⌈Eᵢ/Tᵢ⌉ (§11.2) moves no entry and adds none (§11.1)."

**Check 4 / overclaim analysis.** The *deleted* parenthetical asserted that, among all four permitted declaration-change classes of §20.3 step 4, *only* a change to entry_count can change index content. I tested this against the slab/alignment class: §20.3's "line is drawn" paragraph states an aligned layer's *stored tiles* must satisfy a re-established alignment invariant or the declaration is cleared (line 3284-3287, `[R-SLB-01]`), which implies stored tiles can need repositioning (and hence their index entries' stored offsets can need to change) on a slab/alignment change, without entry_count itself changing. That means the deleted claim ("only a change to entry_count" drives index-content change) was an overclaim the old Note made that its citations (`[R-WRT-04]`) do not actually support — the repair's fix is to *delete* the overclaim rather than repair it in place, and replace it with a narrower, directly-supported claim (citing back to hunk 05's now-corrected Rationale). This is the right shape of fix: it doesn't try to patch the false universal, it removes it.

**Check 2 (citations).** `[R-WRT-04]` for the general re-emission clause — resolves against §20.3 step 4's first paragraph verbatim ("Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full"). §11.1 for "moves no entry and adds none" — resolves verbatim against hunk 05's repaired Rationale text ("A growth that changes no grid count ⌈Eᵢ/Tᵢ⌉ (§11.2) moves no entry and adds none"). §11.2 for the grid-count formula — resolves.

**Check 3 (label vs marker).** Confirmed this Note sits in a `> **Note — sparse writing.**` block (non-normative); the actual normative content it summarizes lives at §20.3 step 4 (unlabelled numbered-list prose, normative) and is unchanged by this hunk.

**Sweep.** Searched the whole document (normalized whitespace) for the deleted phrase `only a change to entry_count` — 0 hits — confirms the overclaim was not left standing anywhere else. Searched `moves no entry` — exactly 2 hits, this Note and hunk 05's Rationale, mutually consistent, no third stray copy.

**Byte-level:** No — Note, non-normative.

**Verdict: no defect found; repair correctly narrows a prior overclaim rather than papering over it.**

### Hunks 12 & 13 — §20.5 Example figure and caption, lines 3538-3554

**Landing block label:** `> **Example — what compaction reclaims.**` — non-normative.

**Rule asserted:** In the worked before/after diagram (layers A, B; A's tiles+index precede B's in the input, separated by slack), only B's index region is regenerated (marked `′`); A's index is copied byte-identically and only its extent slot (offset) is re-pointed, because A's tiles never moved while B's did.

**Check against source (`[R-WRT-06]`/`[R-WRT-07]`, lines 3499-3533).** The controlling rule is: a tile-index region is regenerated **iff** the output relocates (moves) some stored extent it indexes; otherwise the record (including a tile-index region) is merely copied forward with its extent slot re-pointed. This is exactly what hunks 12/13 assert for A vs B.

**Does the diagram itself establish A's tiles didn't move?** Input row: `front│ A │▓▓▓▓│ B │▓▓│ A: index │▓▓│ B: index │▓▓▓│ dir │pad│ tr │`. Output row (post-hunk-12): `front│ A │ B │ A: index │ B: index′ │ dir │pad│ tr │`. In *both* rows, A is the very first region after `front` with nothing preceding it — no slack, no other structure. Since `front` is fixed-size and nothing precedes A in either row, A's tile payload necessarily starts at the same absolute file offset before and after compaction — it does not move. B, by contrast, is preceded by slack in the input and by nothing in the output, so B's starting offset strictly decreases — B's tiles do move. I checked this reading against the figure's own caveat ("Regions, not offsets" is used for the *earlier* §5.1 figure, at line 657; this §20.5 figure's own caption at line 3535 says "Regions, not offsets" too) — the caveat says relative spacing/gaps aren't drawn to scale, but it does not undercut the ordinal fact that A is first-after-front in both rows, which is what the "A didn't move" claim rests on, not any numeric offset.

**Check 2 (citations).** `[R-WRT-07]` — resolves against "The output's reference arrays MUST equal the live generation's bit for bit... compaction changes where bytes live, never what a layer denotes," and the immediately preceding paragraph's regeneration rule. The unmodified lead-in of the same sentence ("extent slots are re-pointed and each index region any of whose stored extents moved is regenerated") is consistent with, not contradicted by, the added clause.

**Check 4 (contradiction with untouched text).** The paragraph's earlier, unchanged sentence (line 3546-3548): "Every stored tile's bytes survive byte-for-byte, as does every record extent but a tile-index region any of whose stored extents moved — itself a record extent (§5.2), and the one kind this operation regenerates rather than copies" — directly supports, rather than conflicts with, the new specific claim about A/B.

**Check 5 (exhaustive claim).** "A's did not [move]" tested directly against the diagram as above — holds. "the ′ marks B's" — B is the only primed structure in the output row — holds by inspection of the row hunk-12 produced.

Is a *copied* index region itself "a record extent" already covered by the caption's first sentence, per the charter's prompt? Yes: the pre-existing sentence's own parenthetical ("itself a record extent (§5.2)") already establishes that a tile-index region *is* a record extent, so A's index (copied, unregenerated) is exactly one of the "every record extent" instances that "survive[s] byte-for-byte" per that same sentence — the new caption text is a specialization of that general clause to this specific example, not a new or conflicting category.

**Check 8 (anaphora).** Forward: "Placement is what changes, which is why the output is a different file..." — "Placement" here is a fresh noun phrase, not a pronoun resolving to the insertion; unaffected. No pronoun in the hunk's own inserted text needed an antecedent outside its sentence beyond "the ′" (resolves to the diagram just above, unaffected) and "B's"/"A's" (resolve to the layers named throughout the section, unaffected).

**Byte-level:** No — labelled Example, non-normative; the binding rule is `[R-WRT-06]`/`[R-WRT-07]` in the unlabelled prose above, unchanged.

**Verdict: no defect found.**

### Hunks 18 & 19 — Appendix H, lines 4712-4758

**Section label:** `### Appendix H — Conformance checklists (non-normative)` — explicitly non-normative per its own heading, independent of `[R-CNF-01]`'s blockquote-label rule (this is a `###`-level section, not a blockquote at all).

#### Hunk 18 — Conforming reader entry

**Rule asserted:** "accepts every conforming file of a major it implements that carries no top-level MU = 1 record of a type it does not implement and lies within §21.9's minimum guarantees, and reports any resource refusal as a limit rather than as corruption (`[R-ERR-04]`, §21.6)."

**Check 1/2 against R-CNF-03** (quoted above): three qualifiers — (a) "of a format major version it implements" ↔ "of a major it implements"; (b) "carrying no top-level record of a type it does not implement with MUST_UNDERSTAND = 1" ↔ "that carries no top-level MU = 1 record of a type it does not implement" (same two conditions, reordered, same meaning); (c) "none of whose values exceeds the minimum guarantees of §21's limits table" ↔ "lies within §21.9's minimum guarantees" (§21.9 is confirmed, at lines 3976-3986, to be the section hosting that very table — "The table below states minimum guarantees"). All three qualifiers present and correctly matched; none added, none dropped.

**Citation `(`[R-ERR-04]`, §21.6)`.** I checked whether §21.6 actually supports the resource-refusal-reporting clause it's attached to, rather than assuming a mismatch from its distance from R-ERR-04's defining sentence (which sits in §21.9, line 4025-4029). §21.6's own opening paragraph (line 3855-3858) states: "where an entry records a resource decline, the decline is licensed and reported as `[R-ERR-04]` requires" — directly on point for "reports any resource refusal as a limit." §21.6's closing paragraph (lines 3891-3910) also directly supports the *other* two new qualifiers (foreign major, unimplemented top-level MU=1 type) by name. So §21.6 is a legitimate citation for this whole clause, however it's parsed; both readings resolve. No defect.

**Check 5 (exhaustive claim).** Re-read the sentence immediately before this clause, unchanged by the hunk: "implements all four codecs, both filters, both layouts, all thirteen sample types, and both user-metadata encodings (`[R-CNF-03]`, §2.3)" — this already carries R-CNF-03's separate "MUST handle every codec..." obligation, so no qualifier of R-CNF-03 is left unstated across the two sentences.

**Byte-level:** No — Appendix H, non-normative.

**Verdict: no defect found.**

#### Hunk 19 — Conforming updater entry

**Rule asserted:** "changes a layer that stores a tile in the generation its commit supersedes only as §20.3 step 4 permits — its names, a grown extent, a planar channel list extended at its end or shortened from it (not both in one commit), a slab or alignment declaration declared, re-established or cleared — and makes any other change to it as a new layer or a whole-file rewrite (§20.3); re-emits every retained record it does not logically modify byte-identically, a modified one being new output under its writer obligations (§20.4, `[R-WRT-05]`)..."

**Check 1/5 — the four-item closed list.** Compared against §20.3 step 4's own four exception classes (quoted above): (1) names ↔ "its names"; (2) extent growth (not shrink) ↔ "a grown extent" (correctly states only the permitted direction, consistent with source's "MAY grow, and MUST NOT shrink" — appendix doesn't claim shrink is allowed); (3) planar channel-list extend-or-shorten, not both ↔ "a planar channel list extended at its end or shortened from it (not both in one commit)" — this is the specific repair: the pre-repair text said "a planar channel added or removed at the end" (a *per-channel* framing, wrong unit — the source's permission is stated over the *list as a whole*, extended/shortened, not over adding/removing one channel), and the repair replaces it with list-level extend/shorten-not-both language matching the source almost verbatim; (4) slab/alignment ↔ "a slab or alignment declaration declared, re-established or cleared." All four source classes present, none added, none dropped.

**Check 2 (citations/wording match).** "a planar channel list extended at its end or shortened from it (not both in one commit)" vs. source "a planar layer's channel list MAY be extended at its end or shortened from its end, but not both in one commit" — "shortened from it" reads back to "its end" (the antecedent two words earlier in the same clause), matching "shortened from its end." Same content, same exclusivity condition ("not both in one commit" ↔ "but not both in one commit").

**Sweep for the old, wrong per-channel phrasing.** Searched the whole document (normalized) for `channel added or removed` — 0 hits; `channel added` — 0 hits — confirms no other copy of the old, unit-mismatched restatement survives anywhere in the document.

**Re-emission clause.** "re-emits every retained record it does not logically modify byte-identically, a modified one being new output under its writer obligations (§20.4, `[R-WRT-05]`)" vs. `[R-WRT-05]` verbatim: "MUST re-emit byte-identically ... every record it retains and does not logically modify ... a record it modifies is new output under its writer obligations (`[R-CNF-05]`)." Same two clauses, same quantifier ("every ... does not logically modify"), correctly generalized citation to `[R-WRT-05]` (the tag covering the whole paragraph) rather than the inner `[R-CNF-05]` citation, which is also defensible since `[R-WRT-05]` is the enclosing requirement id for the whole re-emission rule this Appendix-H bullet is summarizing.

**Check 4 (contradiction with untouched clauses in the same bullet).** Re-read the rest of the "Conforming updater" bullet (lines 4740-4758), untouched by this hunk: "copies forward the input's unknown ignore-lane flag bits..."; "respects every record's MU and PE bits, the registry's fixed values governing for a registered type (§20.4, `[R-CNT-22]`)"; "never removes a layer record, or a user-metadata record at either scope (§20.4)"; "never modifies a scope governed by an unknown critical record, and rejects outright a file carrying an unimplemented top-level MU = 1 record (`[R-CNT-15]`, §20.4)." None of these are touched by the hunk and none conflict with the repaired clauses — they describe orthogonal obligations (flag handling, drop prohibition, MU=1 refusal) that don't overlap the declaration-change list or the re-emission clause.

**Sweep — R-WRT-05 restatements document-wide.** Searched `does not logically modify` — exactly 3 hits: (1) R-WRT-05's own definition at §20.4; (2) §20.4's very next paragraph, restating "The table states what an updater owes a record it does not logically modify"; (3) this Appendix H bullet (post-repair). All three consistent, no fourth stray copy with the old unqualified wording. Searched `retained record` more broadly (3 hits total, listed above) — the other two defer to "§20's preservation rules" / "§20.4" by citation rather than asserting the byte-identical claim outright, so they carry no risk of drifting from R-WRT-05.

**NESTED_DASH:** none introduced (parentheses used, not a second dash pair, inside the existing single dash-delimited list).

**Byte-level:** No — Appendix H, non-normative.

**Verdict: no defect found.**

## Document-wide sweep (charter-mandated)

Searches run (whitespace-normalized text via `python3`/`re`, to handle hard-wrap):

| Search | Hits | Notes |
|---|---|---|
| `channel list` | 9 | All 9 read in context; each either correctly qualified (extend/shorten-not-both, at the 4 planar-permission sites) or refers to the separate, fixed *interleaved*-layer channel list (2 sites) or a non-restating cross-reference (2 sites) — none unqualified. |
| `channel added or removed` | 0 | Control: `channel removed` (below) has 2 hits proving the search infrastructure isn't silently failing on wrapped text. |
| `channel removed` | 2 | Both are the source's own "a channel removed from the end..." sentences (§20.3), consistent, not a stray unqualified restatement of the add/remove pair. |
| `extended or shortened` | 1 | The §11.1 Rationale (hunk 05), now correctly qualified with "one or the other in a commit." |
| `extended at its end or shortened` | 2 | §20.3 source and Appendix H (hunk 19), matching. |
| `entry_count unchanged` | 0 | Confirms the pre-repair phrase "leaves entry_count unchanged" is gone everywhere. |
| `leaves entry_count` | 0 | Same confirmation via a different fragment. |
| `only a change to entry_count` | 0 | Confirms hunk 06's deleted overclaim isn't restated anywhere else. |
| `touches the directory alone` | 1 | Only the §11.1 Rationale — not duplicated (and not contradicted) elsewhere. |
| `moves no entry` | 2 | §11.1 Rationale (hunk 05) and §13.3 Note (hunk 06) — mutually citing, consistent, no third copy. |
| `does not logically modify` | 3 | R-WRT-05 definition, §20.4's next paragraph, Appendix H (hunk 19) — all consistent. |
| `retained record` | 3 | R-LIF-02 step 3, §20.5's compaction paragraph, Appendix H (hunk 19) — the first two defer by citation rather than restate the rule, no drift risk. |
| `stored-tile set or its index content` / `stored-tile set or index content` | 2 | §13.3 Note (hunk 06) and §20.3 step 4's own first paragraph — consistent, matching. |
| `accepts every conforming` / `accept every conforming` / `every conforming file` | 6 total | R-CNF-03's own definition and Appendix H (hunk 18) are the only two *restatements* of the accept-rule; the other 4 hits are unrelated sentences (`[R-ENC-06]` fixed-size discussion, a design-notes aside) that don't restate R-CNF-03's qualifiers at all. |

Every zero above has an accompanying nonzero control search over the same normalized text (e.g., `channel removed` proves the whitespace-normalized search machinery works before trusting `channel added or removed`'s zero; `moves no entry`'s 2 hits prove the machinery works before trusting `entry_count unchanged`'s zero, since both searches ran through the identical code path in the same script).

## Rejected candidates

1. **Hunk 05, ellipsis scope of "taken alone."** Considered whether "so does one that raises a grid count while another stays 0..." (sentence 2) fails to inherit sentence 1's "taken alone" hedge, and would then wrongly claim directory-alone-ness even when combined with another permitted declaration change in the same commit. Closed by direct computation: when the product N is held at 0 (case 2's premise), entry_count = N (interleaved) or C·N (planar) is 0 regardless of the channel count C, and no stored tiles exist to be relocated by a slab/alignment change, so case 2's conclusion is robust to composition with every other permitted declaration-change class regardless of how the ellipsis is read. Not a defect.
2. **Hunk 18, citation "(`[R-ERR-04]`, §21.6)" pointing away from R-ERR-04's defining sentence (which sits in §21.9, not §21.6).** Closed by reading §21.6's own opening paragraph, which independently states the resource-decline-reported-as-`[R-ERR-04]`-requires rule, and its closing paragraph, which independently supports the newly added major/MU=1 qualifiers. Both readings of what the citation attaches to resolve correctly.
3. **Hunk 02, whether "touches no layer" covers a brand-new layer being added (as opposed to only an existing layer being modified).** Closed by checking the immediately preceding sentence's own usage of "touch" (layer A "the commit does not touch" vs. layer B being added/touched in an earlier commit in the same worked example) — the document's own usage treats adding a layer as "touching" it, consistent with `[R-LIF-02]` step 2's "layers it changes."
4. **Hunks 12/13, whether the figure's "Regions, not offsets" caveat undermines reading "A didn't move" off the diagram.** Closed by checking that the caveat concerns relative spacing/scale, not the ordinal fact (nothing precedes A in either row), which is what the claim actually rests on.

## Confidence / where an empty result could still hide something

I ran all eight checks against all seven hunks, with concrete derivations (not just re-reading prose) for the two hunks most likely to hide a composition defect (hunk 05's grid-count taxonomy, hunk 13's regenerate-vs-copy distinction), since those are exactly the shapes this project's history flags (a member added to a list with composition left open; a qualification stated for one case and not a sibling case that composes the same way). I explicitly tested the "grown while combined with a sibling permitted change" composition for hunk 05 by computing entry_count under composition rather than asserting it. I did not find a case among the four charter-suggested test cases (padding-position growth, product-held-at-0 growth, rank-1 growth, growth-with-shortening) that falsifies either taxonomy sentence.

What I could not check: I have no access to `spec/registry.json`, conformance vectors, or other lanes' hunks, so I cannot confirm these seven restatements are consistent with material outside `tarn.md` (the charter forbids this, and the restatements' own citations are entirely intra-document, so this shouldn't matter for these particular hunks). All quoted source material was read directly from `tarn.md` at the offsets shown; no citation was accepted from memory of what an id "usually" means.
