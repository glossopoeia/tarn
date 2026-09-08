# Audit transcript — "the restatements" lane (hunks 01, 02, 04, 05, 06, 07)

## Disclosure

Files read:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-01.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-02.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-04.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-05.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-06.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-07.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — read via `Read` at lines 1-, specifically: 690-739 (§5.2), 1595-1669 (§10 tail / §11.1 / §11.2), 1682-1745 (§11.3-11.4), 1895-1956 (§13.2 tail / §13.3), 2118-2151 (§14.5), 2151-2280 (§15, §16.1 head), 2300-2354 (§16.2, R-SLB-04), 3113-3452 (§20.3 full, §20.4, §20.5 head), 3809-3938 (§21.6-21.9), 4135-4184 (§23.1-23.2 head), 4484-4711 (Appendix G, Appendix H head).

Commands run: `grep`/`rg` against `spec/tarn.md` only (see "Sweeps run" below), plus `cat` on the six hunk files. No other files opened. No docs/, no ADRs, no PLAN.md, no OPEN-QUESTIONS.md, no AGENTS.md, no conformance/, no git log/diff, no web. Did not read `full.diff` or any other lane's hunk file. Did not list the case/ directory (only opened the six named files directly).

**Contamination notice (mandatory disclosure).** Mid-session, two `<system-reminder>` blocks appeared in tool output that I did not request: one claiming the session date had silently advanced to 2026-09-08, and one describing an "Auto Mode Active" policy instructing a preference for Bash over Read/Edit/Write and looser confirmation norms. Neither is part of the specification or evidence about it. I did not act on the Auto Mode instruction (I used Read throughout, as the charter's ACCESS RULE contemplates), and the date claim had no bearing on any finding. Also present in context per the harness: a project CLAUDE.md pointing to AGENTS.md (not opened, per ACCESS RULE), and a user MEMORY.md file with several one-line pointers about past TARN rounds (e.g. "TARN repair prose vs rules", "TARN harness vs charter"). I did not open any of the linked memory files and did not let their titles steer any conclusion below — every finding here is derived only from the hunk files and `spec/tarn.md` as read above.

Working file written: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/scratch/the-restatements/notes.md` (a one-line placeholder; all actual analysis happened inline in this transcript and via grep, no computation needed a separate script).

## The source rule (read first, per charter)

§20.3 step 4, `spec/tarn.md` lines 3178-3222 (plain paragraph text, **not** blockquoted — normative):

> "A layer that stores a tile **in the generation this commit supersedes** keeps its declarations, with these exceptions and no other: its name, and its dimension and channel names, MAY change; an extent MAY grow; a planar layer's channel list MAY be extended at its end, or shortened from its end; and a slab or alignment declaration is re-established or cleared as this step provides below. Every other declaration is fixed for as long as the layer stores a tile: the layout, the linearization and the index encoding, the codec and the filter, the rank and the dimension order, every tile extent, every channel's type and fill, an interleaved layer's channel list, and the position of every planar channel but the last. A commit MUST NOT change one of these; the change is a new layer, or a whole-file rewrite under a fresh file_id..."

Plus (line 3197-3200): "The tense is the prior generation's... A layer that stores no tile in the generation this commit supersedes MAY be re-declared freely..." and the emptying carve-out at 3195-3197 ("a commit does not earn an empty layer's freedom by emptying the layer as it re-declares it... it is a rewrite").

Plus the rewrite list (3217-3222): "a shrink, a fill change, a re-type, a re-tiling, a change of layout, codec or filter, and a channel inserted or removed anywhere but the end are rewrites."

**Closed permitted-change set, for a layer that stores a tile:**
1. layer name / dimension names / channel names — MAY change
2. an extent — MAY grow (never shrink)
3. planar layer's channel list — MAY extend or shorten **at the end only**
4. slab or alignment declaration — re-established or cleared

Everything else (layout, linearization, index encoding, codec, filter, rank, dimension order, every tile extent, every channel's type and fill, interleaved channel list, non-last planar channel position) is fixed; changing it is a new layer or a whole-file rewrite.

For a layer that stores **no** tile in the superseded generation: free re-declaration, EXCEPT a layer the commit itself empties (that's a rewrite, not a free re-declaration).

---

## Hunk 01 — §11.1's Rationale (lines 1636-1655)

**Block label check (Check 3).** The hunk lands entirely inside `> **Rationale.**` (opens line 1636). Per `[R-CNF-01]` this block is non-normative. So the rule it states carries no independent force — it is only as good as its accuracy in restating §20.3, which is what I checked.

**Rule the repair adopts (paraphrase):** "§20.3 permits, for a layer that already stored tiles: extent growth, planar channel-list extension/shortening at the end, name changes, and slab/alignment changes; everything else is fixed while the layer stores a tile (else new layer/rewrite). An empty layer may be freely re-declared unless the commit itself emptied it."

**Item-by-item against source's closed list:**
| Source item | Hunk 01 text | Match? |
|---|---|---|
| name / dim names / channel names MAY change | "its names ... may change" | Compressed but faithful — "names" plausibly covers all three named categories |
| extent MAY grow | "its extents may grow, subject to every rule the grown geometry is under" | Matches verbatim in substance, even reuses source's own qualifying clause |
| planar channel list extended at end / shortened from end | "a planar layer's channel list may be extended or shortened at its end" | Matches; hunk applies "at its end" to both operations, source phrases them as "at its end" / "from its end" — same operation, no behavior difference |
| slab/alignment re-established or cleared | "its ... slab and alignment declarations, may change" | Checked against `[R-SLB-04]` (line 2339-2347): a commit that changes "the slab declaration itself" must re-establish invariants for the new run partition or clear it — i.e. changing to a *new* value is contemplated as long as invariants hold. "May change" is accurate under this reading. |
| empty-layer free re-declaration; self-emptied layer excluded | "A layer that stored no tile in the generation the commit supersedes may be re-declared freely; a layer the commit itself empties does not qualify." | This sentence is **byte-identical** to the old (pre-repair) text — retained unchanged by the hunk, and it matches source's own wording (3198-3200, 3195-3197) closely. |

**What follows, untouched by the hunk (Check 4/8):** the "Growth that leaves entry_count unchanged..." / "Growth that changes entry_count..." sentences (1647-1655) still read correctly under the new closed-list framing — growth is still permitted, so the mechanics described (grid-count product staying at 0, entry_count changing when it doesn't) remain accurate and are not contradicted by the rewritten lead-in.

**Findings:** none that rise to a defect. The "One commit can do several of these at once" sentence, present in the old text just before the empty-layer sentence, was dropped by the rewrite — a minor loss of an explanatory remark (multiple permitted changes may combine in one commit), but nothing in the new text asserts or implies the opposite, so this is not a contradiction or an under/overclaim — just a style loss. Logged as a rejected candidate, not a finding (see below).

**Byte-level:** N/A — whole passage is a labeled Rationale block, no normative force either way.

---

## Hunk 02 — §13.3's "Note — sparse writing" (lines 1940-1948)

**Block label check.** `> **Note — sparse writing.**` (opens 1940) — non-normative per `[R-CNF-01]`.

**Rule the repair adopts:** "A commit that changes a layer's stored-tile set, or its entry_count, re-emits the layer's whole tile-index region — and entry_count changing is the *only* way index content (ordinal placement) moves, given what §20.3 permits a layer that already stores a tile."

**Old vs. new:** old text had *three* disjuncts triggering re-emission — stored-tile-set change, entry_count change, or "which ordinal an entry sits at" changing. New text folds the third into the second via the parenthetical claim.

**Testing the "only way" claim (charter's specific ask — a growth of one grid count while another is 0):**

Let N = ∏ Gᵢ (interleaved entry_count) or C·N (planar). A layer "stores a tile" in the superseded generation ⟹ some entry is non-sentinel ⟹ that entry is addressed ⟹ entry_count = N (or C·N) > 0 already ⟹ **every** Gᵢ ≥ 1 already (a product of naturals is 0 iff some factor is 0).

- Growth changes some Gⱼ, Gⱼ_new > Gⱼ_old ≥ 1, all other Gᵢ ≥ 1 unchanged ⟹ N strictly increases (product of positive integers, one factor strictly larger) ⟹ entry_count strictly changes. So for a layer that already stores a tile, growth **always** changes entry_count — the "one grid count grows while another stays 0" case the charter names cannot occur here, because if any Gᵢ = 0, N = 0, and a layer with N = 0 has zero addressed tiles and hence cannot be "a layer that stores a tile" (there is nothing to address, let alone store). That degenerate case is squarely inside "a layer that stored no tile" (source 3198), which the Note's parenthetical explicitly does *not* claim to cover.
- Ordinal *reflow* from growth: R-GEO-06 (line 1727-1730) gives disk ordinal = c·N + s, s = Σᵢ tᵢ·∏_{j>i} Gⱼ. Growing a non-last dimension's Gⱼ changes the weight ∏_{j>i}Gⱼ for every i < j, reflowing existing tiles' ordinals — but as just shown, any such growth (on an already-nonzero-N layer) also strictly increases N, hence entry_count. So reflow never happens without an entry_count change, on this scope.
- Channel-list extend/shorten at the end: extend adds tiles at ordinals *after* every existing one (existing ordinals c·N+s for c < C_old unaffected) — no reflow, but entry_count (C·N) changes. Shorten similarly: entry_count changes, no reflow of survivors.
- Name changes, slab/alignment changes: touch neither ordinals nor entry_count.

So, restricted to "a layer that stores a tile" (the Note's own explicit scope), no permitted §20.3 operation moves an index entry's ordinal, or adds/removes an entry, without also changing entry_count. The claim holds.

**Citations:** "(§11.1, §20.3, `[R-WRT-04]`)" — unchanged from before the hunk (present in both `-` and `+` blocks). `[R-WRT-04]` located at line 3256 (end of step 6, covering the whole write/commit sequence steps 4-6) — appropriate citation for "re-emits that layer's whole tile-index region." §11.1 and §20.3 both discuss re-emission — appropriate.

**Findings:** none. The claim is correct as scoped.

**Byte-level:** N/A — labeled Note, non-normative.

---

## Hunk 04 — the Example's shape (c) (lines 3307-3320)

**Block label check.** Part of `> **Example — the three shapes a commit takes.**` (opens 3275) — non-normative.

**Rule the repair adopts:** "(c) directory-only changes are: clearing a slab declaration, renaming a layer, dropping a licensed PE=0 record. Any change to a *fixed* declaration (fill, type, tile extent, etc.) of a layer that stored a tile in that generation is not an appender operation at all — it's a rewrite, because it would reinterpret every stored tile it reaches."

**Against source:** the old text carved out a narrow *exception*: a fill-value change was directory-only **when that channel carries no padding position and no pad bit anywhere in the layer's stored tiles**. That carve-out reflected the pre-round-31 "two-bar" rule. Under the current closed list (3184-3222), fill is unconditionally in the *fixed* set — "every channel's type and fill" — with no carve-out for channels lacking padding. The hunk correctly deletes the old carve-out and folds fill (along with type, tile extent) into the barred set, replacing "invalidate" with "reinterpret" — which better matches source's own language ("under new [declarations] the same bytes would denote values, coordinates or padding the writer did not store," 3206-3207): the bytes aren't invalidated, they're *reinterpreted*.

Verified against source item-by-item: nothing in the new (c) list (slab-clear, rename, PE=0-drop) exceeds source's directory-only-compatible set — none of them touch tile data or index content, matching "Only the directory is re-emitted."

**Check 8 — anaphora (the one real finding here).** The deleted clause was:

> "...changing a channel's fill value where that channel carries no padding position and no pad bit in any tile **the layer stores in the generation the commit supersedes**, or dropping a PE = 0 record... A fill change on a channel that carries a padding position or a pad bit in a tile the layer **stored** in **that generation** is not an appender's operation..."

The bolded first occurrence is what "that generation" (second occurrence, retained verbatim in the new text) resolved to. The hunk deletes the *first* occurrence but keeps the referring phrase "in that generation" attached to the (rewritten) sentence: "A change to any fixed declaration of a layer that **stored** a tile in **that generation** — a fill value, a type, a tile extent — is not an appender's operation..."

I checked what "generation" now resolves to by nearest-antecedent search:

```
grep -n "generation" spec/tarn.md | awk -F: '$1>=3230 && $1<=3320'
```
Result: only two hits in that whole span — line 3312 ("that generation", the phrase itself) and line 3315 ("generation the commit supersedes", in the very next, untouched sentence about empty layers). **Nothing between the start of shape (c) and line 3312 mentions "generation" at all** — the local antecedent was deleted along with the fill carve-out clause, and not replaced.

Extending the search further back (to the top of step 4, line 3100+):
```
grep -n "generation" spec/tarn.md | awk -F: '$1>=3100 && $1<=3313'
```
Nearest actual antecedent by raw proximity is line 3198 ("the generation this commit supersedes" — but that clause is about a layer that does **not** store a tile, i.e. the opposite predicate from the one governing line 3312's sentence), or line 3178 (a layer that **does** store a tile, ~134 lines earlier, in the main step-4 prose rather than the Example). A reader relying on the document's recurring idiom ("stored a tile in the generation the commit supersedes") will almost certainly infer the intended meaning correctly by convention — the very next sentence spells it out in full ("the generation the commit supersedes") — but formally, the phrase's local textual anchor was removed by this edit and not restored. This is exactly the anaphor-stranding shape the charter warns about (Check 8): the deletion, not an insertion, left a back-reference dangling.

**Byte-level:** No — this is inside a labeled, non-normative Example, and even setting that aside, no conforming implementation's behavior turns on which "generation" a reader infers here (the actual rule is stated unambiguously and completely in step 4 itself, which this Example only illustrates). This is a documentation-clarity defect (NEW_AMBIGUITY / stranded ANAPHOR), not a byte-level one.

---

## Hunks 05 and 06 — §23.1 "Deletion is not erasure" (lines 4139-4163)

These two hunks land in the *same* paragraph and are best audited together. **Not blockquoted** — confirmed by re-reading lines 4135-4184 directly: no line in this span begins with `>`. This is normative prose, tagged `[R-PRV-01]` / `[R-PRV-02]`.

**Rule the repair adopts:** "A commit makes sample data unreachable only by: superseding a stored tile's payload, unstoring a tile, removing a planar layer's last channel, or dropping/superseding a record's extent. In every case the bytes simply leave the live state (become slack) — never staying inside a still-addressed structure as reinterpreted padding — because a shrink (the only mechanism that could do the latter) is always a rewrite, not a commit, under the current rule. So 'the structure leaves the live state' is the *only* case; the enumerated list of operations is still not offered as a closed enumeration of *that* case's members."

**Hunk 05's substitution — "shrink" → "removing a planar layer's last channel" in the operation list (line 4144-4146).**

Checked: is a "shrink" (extent decrease) still ever a legitimate commit for a layer that stores a tile? No — source 3217-3222 explicitly puts "a shrink" in the list of changes that "are rewrites even where a particular file would survive them in place." So a bare "shrink" no longer belongs in a list of things *a commit* can legitimately do. "Removing a planar layer's last channel" *is* still permitted (source: "shortened from its end") and *does* take that channel's tiles "out of the addressed set" (source 3231-3232: "A channel removed from the end leaves its stored tiles' extents as slack"). The substitution is a correct update to the closed-list world, not an overshoot (it doesn't broaden the claim — it swaps one no-longer-valid example for a still-valid one covering the same underlying mechanism, "tiles drop out of the addressed set").

**Hunk 06's universal claim — "no commit turns a real position of a stored tile into padding, a shrink being a rewrite."**

Tested against every permitted change for a layer that stores a tile:
- Extent growth: only ever adds positions that already held fill (source 3210-3211) — moves padding→real, never real→padding. No counterexample.
- Planar channel-list end-extend/shorten: removes/adds whole tiles from the addressed set; does not reclassify positions *within* a still-addressed tile as padding. No counterexample.
- Slab/alignment re-establish/clear: repacking only, doesn't touch which positions are real vs. padding. No counterexample.
- Name changes: no effect on tile content classification.
- Tile extent, layout, type/fill, codec/filter, rank, dimension order, interleaved channel list, non-last planar channel position: all *fixed* — cannot change at all while the layer stores a tile, so cannot flip any position's classification.
- A **shrink** (the only operation that, historically, under the old two-bar rule, could turn a real position into an edge tile's padding) is now unconditionally a rewrite for a layer that stores a tile (source 3217-3222) — hence never available to a commit.

So for a layer that already stores a tile, the claim holds without exception under the closed list.

**Tested against a compactor** (per charter instruction): §20.5 states a compactor's output "contains only the structures reachable from the input's live trailer... less any record §20.4 lets it drop" and that compaction "carries every layer of its input forward" (§20.4, line 3371). Compaction does not alter declared geometry — it relocates/removes slack, not live structures — so it cannot convert a real position into padding either. No counterexample from compaction. (Also, the sentence's subject is "a commit," and compaction is explicitly a distinct, non-commit whole-file-rewrite operation per `[R-LIF-01]` — so even if it could, it would be out of this sentence's scope, but I checked it anyway per the charter's explicit instruction.)

**A residual scope ambiguity (finding).** The clause "a shrink being a rewrite" is stated with no explicit restriction to "a layer that stores a tile." Source's own "a shrink ... [is a] rewrite" statement (3217-3222) lives inside the paragraph specifically governing a layer *that stores a tile* — for a layer that stores **no** tile, source explicitly permits free re-declaration (3198-3200), which can include reducing an extent, and that is *not* a rewrite. So "a shrink is a rewrite," read as an unrestricted universal, is false of an empty layer's extent reduction. In context the restriction is almost certainly intended (the whole passage is about "a real position of a **stored** tile"), and an empty layer never had any "real position of a stored tile" to protect, so the false reading and the true reading agree on every case that actually matters to the sentence's own claim (no real, byte-affecting consequence). But the parenthetical, read on its own, overclaims: it asserts an unconditional equivalence ("shrink = rewrite") that source itself only asserts conditionally on the layer already storing a tile. I'm reporting this as a genuine but low-severity/non-byte-level finding (OVERCLAIM / TENSE_QUANTIFIER): the true governing rule remains in §20.3 untouched, so no implementation's accept/reject or emit behavior turns on this sentence.

**"Where the structure carrying the bytes leaves the live state" (line 4152, untouched) vs. hunk 06's "That is every case."** The old text used this bolded lead-in as one half of an explicit if/else pair with a second bolded "**Where it does not**" clause (now deleted). The remaining bolded lead-in is still grammatically self-contained and its claim ("they remain in the file as slack... recoverable...") is unaffected; "That is every case" correctly asserts there is no second branch anymore. The leftover bold emphasis is a minor stylistic residue (it no longer contrasts with a paired clause) but not a substantive defect — logged under rejected candidates.

**"The list of operations above is not offered as closed" — does it still have work to do (charter's specific question)?** This sentence is retained verbatim from the old text (present in both `-` and `+` blocks) — not new work product of the repair itself, but I checked its accuracy under the new regime as instructed. I attempted to construct a fifth "commit removes reachability of sample data" case beyond the four enumerated (supersede-payload, unstore, remove-last-channel, drop/supersede-a-record's-extent) and could not find one: every permitted §20.3 operation that touches which bytes are live either falls under one of those four or doesn't remove data at all (name/slab/alignment changes, growth). So, on the current closed-list rule, the hedge "not offered as closed" appears **vestigial** — it no longer guards against an actual omitted case, though it remains true as stated (it doesn't claim there *is* a fifth case, only that the list isn't presented as exhaustive). I flag this as a rejected candidate rather than a finding: it's not wrong, and the charter's own framing ("still has work to do") invites checking rather than asserting a specific defect, and I found none — no real ambiguity or false claim results from keeping a conservative hedge that happens not to be strictly needed.

**Check 7 — analogy.** "...misleads exactly as a supersede so reported does" (line 4162, new text, matches old text's parallel "a shrink reported as erasure misleads exactly as a supersede so reported does" with "shrink"→"channel removal"). Governing verb both sides: "misleads." Both sides are instances of the same general MUST NOT stated the sentence before ("MUST NOT represent any commit that makes sample data unreachable as erasure of it") — channel-removal and supersede are both still-legal, still-slack-producing commit operations, so the analogy is sound on both sides; no quantifier mismatch (both are single concrete examples of the same general rule, not two different-shaped rules like the historical "contains" vs. "addressed" defect).

**Citations checked:** "(§20.3 step 4)" ×2 (hunk 05, hunk 06) — both point at the correct paragraph (the closed permitted-change list and its "rewrites" enumeration). "(§15.2)" for unstoring, "(§20.4)" for record drop/supersede — both pre-existing, unaffected by the hunks, both verified accurate on inspection of those sections.

**Byte-level:** No finding here forks bytes. The MUST NOT in this passage governs how writers/tools *represent* (report/label) an operation, not what bytes they may emit — the underlying legality of any given commit is still governed entirely by §20.3, unaffected by any imprecision in this exposition.

---

## Hunk 07 — Appendix H, "Conforming updater" entry (lines 4688-4702)

**Block label check.** Appendix H's header (line 4649) reads "### Appendix H — Conformance checklists (**non-normative**)" — explicitly self-identified non-normative per `[R-CNF-01]`'s "appendices identified as non-normative" clause.

**Rule the repair adopts:** "An updater changes a layer that stores a tile only as §20.3 step 4 permits (names / grown extent / planar channel at the end / slab-or-alignment declaration), and any other change to it is only legitimate as a new layer or whole-file rewrite."

**Against source:** four items in the new clause map 1:1 onto source's four-item closed list (names; extent growth; planar-channel-list-at-the-end; slab-or-alignment). All four present, none added, none omitted, none broadened. "only as §20.3 step 4 permits" correctly conveys exclusivity, matching source's "with these exceptions and no other."

**Other clauses in this entry, untouched by the hunk — checked for continued agreement (charter's explicit ask):**
- "validates the trailer and full directory, and every layer it modifies (§20.3)" — consistent, no conflict (a separate validation-depth obligation, matches §20.3's opening paragraph on verification depth, line 3115-3123).
- "re-emits every retained record byte-identically (§20.4)" — consistent with §20.4 (line 3333-3337).
- "copies forward the input's unknown ignore-lane flag bits, clears none and sets no other (`[R-CNT-08]`, §6.3)" — unrelated to step 4, unaffected, still correct per §6.3/step 6 (line 3253-3255).
- "respects every record's MU and PE bits, the registry's fixed values governing for a registered type (§20.4, `[R-CNT-22]`)" — matches §20.4's table (line 3357-3361) and its registered-type gloss (3341-3343).
- "never removes a layer record, or a user-metadata record at either scope (§20.4)" — matches §20.4's "No commit therefore removes a layer record, or a user-metadata record at either scope" (line 3363-3364) — this governs *whole-record removal*, a different axis from step 4's *declaration-level* closed list; no collision (a layer record can be modified within step 4's bounds while never being *removed*).
- "never modifies a scope governed by an unknown critical record, and rejects outright a file carrying an unimplemented top-level MU = 1 record (`[R-CNT-15]`, §20.4)" — matches the MU=1 row of §20.4's table (line 3359) and `[R-CNT-15]`.

No contradiction found between the newly inserted clause and any of the entry's other, untouched clauses.

**Check 8 — anaphora.** The insertion sits between "validates..." and "re-emits every retained record byte-identically..." Checked every pronoun/back-reference in the rest of the entry ("it" in "and makes any other change to **it**" resolves within its own clause to "a layer that stores a tile" — unambiguous). No later clause in the entry uses a back-reference whose nearest antecedent shifted because of this insertion.

**Check 5 — exhaustive claim.** "only as §20.3 step 4 permits" — verified true (source's list is explicitly closed, "no other").

**Findings:** none.

**Byte-level:** N/A — non-normative appendix; the entry is a checklist summary whose "authority is the requirement or section cited, never this summary" (per Appendix H's own preamble, line 4651-4653).

---

## Sweep — searching the rest of the document for stray restatements of the old (pre-round-31) permissive rule

Charter's named old permissions to hunt for: a shrink; a fill change on a tile-aligned layer; an identity-filter change; de-addressing by a falling grid count — anywhere they might still be described as an appender's legitimate operation.

```
grep -n "identity filter\|identity-filter" spec/tarn.md          → 0 hits
grep -n "fill change\|change.*fill value\|fill value.*change" spec/tarn.md → 0 hits
grep -n -i "re-typ" spec/tarn.md                                  → 1 hit (line 3218, "a re-type" — in source's own rewrite-triggers list, correctly classifying it as barred, not permitted)
grep -n "falling\|grid count.*fall\|fall.*grid" spec/tarn.md      → 0 hits
grep -n -i "de-address\|deaddress" spec/tarn.md                   → 0 hits
grep -n "shrink" spec/tarn.md                                     → 2 hits: line 3217 (source, "a shrink ... are rewrites") and line 4157 (hunk 06, "a shrink being a rewrite") — both correctly classify shrink as *not* an appender operation
```

Controls proving these zeros are not tooling failures (per charter's warning about hard-wrap and broken normalization):
```
grep -c "filter" spec/tarn.md   → 36 (nonzero; "identity filter" 0-hit is real, not a search failure)
grep -n -i "identity" spec/tarn.md → 6 hits, none about a filter-declaration *change*; the one filter-adjacent hit (line 4574, "The filter is the identity...") is Appendix G's reproducible-writer profile discussing the *mathematical* identity permutation of a filter within one creation, unrelated to an updater changing a declared filter across commits — not a restatement of the old permissive rule.
grep -n "grid count" spec/tarn.md → 8 hits, all either §11.1/§11.2/§11.4's normal grid-count arithmetic (unrelated to the old permissive de-addressing claim) or Appendix G item 5 (creation-time pinning, not an update permission).
```

Targeted section reads (full text inspected, not just grep hits), per charter's list:
- **§5.2** (line 690-739): byte-coverage/slack definitions. No mention of shrink/fill-change/filter-change/de-addressing as an appender operation.
- **§11.3** (line 1682-1699): edge padding definition + a Note on tile-extent choice. No stray restatement.
- **§14.5** (line 2118-2150): padding content rule + Example + Rationale + Note. No stray restatement; the Note there (2146-2149) is about slack vs. padding, unrelated.
- **§15** (line 2151-2280): index region, sentinel, entry validity, segments. No stray restatement.
- **§16** (2276-2354, through §16.2/R-SLB-04): alignment/slab. `[R-SLB-04]` (2339-2347) is the provision hunk 01's Rationale cites via "may change" for slab/alignment — checked above, consistent, not a stray restatement of the old *shrink/fill/filter* permissions.
- **§21.6** (3809-3865): conditions-that-are-not-violations table. No row treats a shrink, an unconditional fill change, a filter change, or grid-count-triggered de-addressing as a defined/legitimate appender behavior.
- **§21.7** (3866-3921): "What no check detects." Mentions "a mis-strided filter" (`[R-COD-10]`, line 3871) only as an example of *undetectable wrong content a writer might emit on creation*, not as a legitimate cross-commit filter change — different subject, no restatement.
- **§21.9** (3930-3938 read; table itself not needed for this sweep — no shrink/fill/filter/de-address language in the section's prose header).
- **Appendix G** (4484-4610): reproducible-writer profile. Item 5 pins "a fixed filter value," tile extents and layout — but this is a *single-creation* determinism profile ("two writers agreeing on everything else"), not a claim about what an *updater* may change across commits. No restatement of the old permissive rule.

Register rows T4/T5 (padding-content violations, line 3751-3752): both are about a *writer* failing to encode fill correctly in padding — unrelated to whether an *appender* may change a fill declaration across commits. No restatement.

**Conclusion of sweep:** zero surviving restatements of the old (shrink / fill-change / identity-filter-change / falling-grid-count de-addressing) permissive language found outside source's own (correct, already-updated) step 4 text and the six hunks under audit, which themselves correctly reflect the new closed-list rule (modulo the two non-byte-level findings above).

---

## Findings summary

- **C-01** (hunk 04, ANAPHOR, non-byte-level): "that generation" in the rewritten shape-(c) sentence lost its local antecedent when the fill-carve-out clause that supplied it was deleted; nearest surviving mention of "generation" in the reduced local span is 100+ lines away and governs the opposite predicate (a layer that does *not* store a tile). Almost certainly resolved correctly by convention/context (the next sentence spells out "the generation the commit supersedes" in full), but formally dangling.
- **C-02** (hunks 05/06, OVERCLAIM/TENSE_QUANTIFIER, non-byte-level): "a shrink being a rewrite," stated without the explicit "for a layer that stores a tile" qualifier that source itself carries, reads as an unrestricted universal that is false of a shrink applied to re-declaring an empty layer (source 3198-3200 permits that as a free re-declaration, not a rewrite). No byte-level consequence — the sentence's own actual claim (about real positions of *stored* tiles) is unaffected either way, and the governing rule remains correctly stated in §20.3 itself.

## Checks that passed with no finding (explicit, per instructions)

- Hunk 01: item-by-item list match (Check 1/2/4/5/6) — passed; empty-layer clause retained verbatim and consistent.
- Hunk 02: "only way" claim (Check 1/5/6) — proved algebraically for both interleaved and planar layers, both leading and non-leading dimension growth; passed.
- Hunk 04: closed-list correctness (Check 1/4/5) — passed; only the anaphor issue (C-01) survived.
- Hunk 05: substitution correctness (Check 1/2/5) — passed.
- Hunk 06: universal claim tested against every permitted operation and against a compactor (Check 5) — passed except for the scope nuance in C-02; "not offered as closed" hedge checked for continued necessity — found vestigial but not false (rejected candidate, not a finding); Check 7 analogy — passed, verbs and scope match on both sides.
- Hunk 07: four-item list match against source, and all five untouched sibling clauses checked for continued agreement (Check 4) — passed; Check 8 anaphora — passed, no stray back-references.
- Sweep across §5.2, §11.3, §14.5, §15, §16, §21.6, §21.7, §21.9, Appendix G, and register rows T4/T5 — zero stray restatements of the old permissive rule, with control searches proving the zeros are real.
- NESTED_DASH — checked every hunk's inserted text; no em-dash pair nested inside another dash-delimited clause in any of the six.
