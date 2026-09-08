# Audit transcript — "the geometry bar" (hunks 05, 11, 12, 13)

## 0. Disclosure

Read exactly:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-05.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-11.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-12.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-13.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, specifically lines 1600-1900 (§11.1-§11.4/§12.1-§12.2) and lines 3121-3409 (§20.3's append procedure, step 4 in full, through the start of step 5/6 and the notes/examples that close the step).

Ran only `grep`/`sed` against `spec/tarn.md` and local reasoning (a by-hand derivation of tile/coordinate arithmetic); wrote no scratch files (the derivation was done in-line in this transcript and did not need a script). No file outside the two named locations was read. Did not read `full.diff`, other hunk files, or list the `case/` directory.

**Contamination note.** Mid-task, two `<system-reminder>` blocks appeared in my context that are not part of the charter: one asserting the date had changed ("Today's date is now 2026-09-08... The user's own clock shows it"), and one full of MCP/browser-tool operating instructions and an "Auto Mode Active" policy notice (telling me to prefer Bash over the Read/Edit tools, and how to handle destructive git commands). Neither is part of the specification or evidence about the specification. I disregarded both — I did not change any conclusion because of the date, and I continued using Read/Bash as convenient for the task, not because the "Auto Mode" note told me to prefer one over the other. Flagging this per the access rule's disclosure requirement.

Also note: the project's own `CLAUDE.md`/memory-file content that normally gets injected before a task (things like "TARN harness spec path", "TARN repair prose vs rules", etc.) was listed as available context in the system reminder wrapping this task, but I did not use any of it — the charter explicitly tells me to disregard such material, and I did not open any of the named memory files (I could not have; they are outside my access list) or let their titles steer my search.

## 1. The four hunks, read

**hunk-05** — lands in spec/tarn.md 1642-1654, inside `#### 11.1 Geometry and its validity floor`, inside the `> **Rationale.**` blockquote that starts at line 1629 and runs to line 1664.

**hunk-11** — lands in spec/tarn.md 3184-3196, inside `#### 20.3 The append procedure`, step 4 ("**Write payloads and indexes**"), specifically the paragraph beginning "A commit MUST NOT change a layer's declarations..." that defines **the §14 bar**.

**hunk-12** — lands in spec/tarn.md 3201-3208, the paragraph immediately following the §14-bar-defining paragraph, which states the carve-out ("is not what this bars").

**hunk-13** — lands in spec/tarn.md 3235-3253, still inside step 4: it inserts a whole new paragraph (tile extents / dimension order) between the sample-type paragraph and the "One effect is barred beside it" (ordinal-bar) paragraph, and it separately edits the opening of that ordinal-bar paragraph ("whose only stated occasion for a renumbering is a geometry change" → "...are a geometry change and a permitted change to a planar layer's channel declarations"). The charter states this second edit is another lane's territory; I read it for context (to check back-references) but do not report findings on it.

I verified each hunk's stated header/line-range against the file directly (`sed -n` / `Read` over the ranges above); all four line ranges and nearest-heading claims in the hunk headers matched the live file. No header/body mismatch found.

## 2. The rule each hunk adopts, in my own words

- **hunk-05**: (non-normative — see §3 below) restates, as commentary, that (a) a padding byte or *packed-plane bit* that already holds fill is inert; (b) a change to tile extents or dimension order is a §14-bar "declaration" change, barred wherever the layer stores any tile, free otherwise; (c) growth of an extent is an outright exception stated by the growth *permission* itself, not something the bar's own carve-out supplies.
- **hunk-11**: extends the §14 bar's protected list to include "the coordinate ... each value ... denotes" — i.e., a commit must not, for a tile the layer stored in the superseded generation, change what coordinate a decoded value is attributed to, alongside the pre-existing protections (padding positions, pad bits, content, decoded size, byte offset/bit position, sample type, codec/filter).
- **hunk-12**: defines what "meaning" (used in the carve-out "leaves ... stored bytes meaning exactly what they meant") consists of — value plus coordinate — and restructures the sentence so the filter-identity/padding-fill cases are stated as *instances* of that gloss rather than being folded into one dash-clause.
- **hunk-13** (first edit, my scope): makes tile extents and dimension order §14-bar "declarations" in the *normative* text (the actual MUST NOT), parallel to the sample-type paragraph above it; states the mechanism (they fix the coordinate a value denotes, so new ones make old bytes denote un-stored samples); states an escape (re-type: new layer or whole-file rewrite) and points to growth/shrink, below, as the permitted geometry changes.

## 3. Check 3 — label, not marker

hunk-05's landing block opens `> **Rationale.**` (line 1629) — I confirmed by reading it directly, not by trusting the section title. Per [R-CNF-01] this is explicitly one of the three non-normative labels, so hunk-05's entire edit is **non-normative** — commentary, not an obligation in its own right. I checked (per the charter's specific instruction on hunk-05) whether its new clause states *exactly* what the normative paragraph says and no more:

> Rationale (hunk-05): "so is a change to the tile extents or the dimension order, barred wherever the layer stores any tile."
> Normative (hunk-13): "A layer's declared **tile extents**, and the declared order of its **dimensions**, are such declarations too, and changing either is such a change wherever the layer stores any tile"

Quantifier match: "any tile" = "any tile". This passes — the Rationale doesn't say anything the normative text doesn't also say, for this clause.

hunk-11, hunk-12 and hunk-13 all land in step 4 of "An appender MUST, in order:" — I read the raw lines directly and none of them begin with `>`. This is plain normative prose (a MUST-governed numbered step), not a blockquote of any kind, so no label question arises: the edits land in normative text and take normative force. Confirmed by direct inspection of `sed -n '3121,3354p'` output — no line in this range begins with `> `.

## 4. Check 2 — citations

- `[R-GEO-06]` (hunk-11, line 3194: "the coordinate (`[R-GEO-06]`) each value in the image denotes"; hunk-13, line 3238: "they are what fix the coordinate each stored value denotes (`[R-GEO-06]`)"). I opened §11.4 (lines 1709-1747) and read the four bullets that define the ordinal/coordinate arithmetic:
  - "A coordinate (x₀, …, x_{d−1}) lies in the tile with **tile coordinates** tᵢ = xᵢ div Tᵢ, at **in-tile position** uᵢ = xᵢ mod Tᵢ." — **no R-tag**.
  - "The **in-tile sample ordinal** of (u₀, …, u_{d−1}) is Σᵢ uᵢ · ∏_{j>i} Tⱼ" — **no R-tag**.
  - "Under linearization 1, the **spatial tile ordinal** of (t₀, …, t_{d−1}) is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ." — **no R-tag**.
  - "The **disk tile ordinal**, which orders tile-index entries (§15), is s for an interleaved layer, and **c · N + s** for a planar layer (§14) ... — channel-major grouping. `[R-GEO-06]`" — **only this bullet carries the tag**, at its very end.

  This placement convention (a single R-tag at the end of the one bullet it governs) is used consistently elsewhere in the document. I confirmed the same usage at two other sites: line 3016-3019 ("Compute the tile coordinates, in-tile ordinal, spatial ordinal s, and the disk ordinal of each needed tile — s interleaved; c · N + s per requested channel c planar (`[R-GEO-06]`)" — tagged specifically on the disk-ordinal computation, not the tile-coordinate/in-tile-ordinal ones named in the same sentence), and line 3255 ("alters the disk ordinal `[R-GEO-06]` assigns any tile"). All *other* live uses of `[R-GEO-06]` in the document are about the **disk tile ordinal** (the c·N+s / s formula that orders index entries on disk), never about the coordinate a value denotes. `grep -n "R-GEO-06"` returns 7 hits total (1662, 1739, 3019, 3178, 3194, 3238, 3255); of these, 1739 is the definition, 1662/3019/3178/3255 are uses about ordinal renumbering or ordinal computation, and 3194/3238 are the two new uses under audit — the only two that cite it for "coordinate."

  **Verdict: citation does not resolve.** `[R-GEO-06]` fixes the disk tile ordinal, not the coordinate a decoded value denotes (that mapping is stated in the *untagged* first bullet of §11.4). This is exactly the "reads as verified" trap the charter warns about: R-GEO-06 genuinely lives in §11.4, right next to the correct rule, so the citation looks plausible on a fast read.

  Compounding this: hunk-11's own **sibling clause**, three lines earlier in the same sentence, cites the concept correctly — "the coordinate §11.4 assigns any value they decode to" (line 3187-3188) points at the *section*, not at a specific requirement ID, which is defensible since the coordinate-assignment bullet carries no R-tag of its own. So the same repair states the same claim twice, once correctly (§11.4) and once with a specific-but-wrong ID (`[R-GEO-06]`). hunk-13's paragraph then reuses the wrong form.

- `[R-COD-10]`, `[R-SER-05]` (hunk-12, unchanged citations, carried through the restructuring): checked — `[R-COD-10]` is the filter-identity-stride rule (§17-adjacent; also cited correctly elsewhere, e.g. line 3206, T26 register row), `[R-SER-05]` is the padding-content rule. Both citations are pre-existing and unaffected by the restructuring; both check out.
- `[R-LIF-01]` (hunk-13's escape sentence omits it, relying on the anaphor "the re-type's" pointing at the sample-type paragraph's fully-cited escape two sentences above, which does carry `[R-LIF-01]`, §20.5). Traced the antecedent: correct, no new citation needed.
- `[R-CNT-17]` (unchanged context at line 1660, cited by hunk-05's surrounding, untouched Rationale text): checked against its definition ("entry_count | u64 | equals the addressed-tile count", line 1100, and "obliges the smaller entry_count", line 3340) — consistent, unaffected by the hunk.

## 5. Check 1 — tense and quantifier

- hunk-11/13's new coordinate protection is stated with the **same tense** as the rest of the §14 bar: "for any tile that layer stores **in the generation this commit supersedes**" governs the whole MUST-NOT sentence, coordinate clause included (the new clause is inserted *inside* that same governed sentence, not appended after its scope closes). Confirmed by re-reading the full sentence (3184-3196) as one unit — the superseded-generation tense clause at 3185-3186 is unchanged and still governs every item in the list, coordinate included.
- hunk-13's new paragraph: "changing either is such a change **wherever the layer stores any tile**" — I checked this against the two live commit types the step permits (growth, shrink) and the channel-removal case, in §6 below.
- hunk-12's restructured carve-out keeps the same actor and tense as the sentence it's embedded in (no independent quantifier of its own — it inherits "such a change" from the governing sentence). No drift found.

## 6. Check 4/6 — the derivation, and what it shows

Per the charter, I derived the concrete case by hand before reading the paragraph's own account of it.

**Setup**: interleaved layer, rank 2, dims (dim0, dim1), extents E=(4,4), one channel (uint8, Bᶜ=1), codec 1 (none), filter 1 (identity/none). Change declared tile extents T from (4,1) to (1,4). Dimension order and channel set unchanged.

**§11.2 (grid arithmetic).**
- Old T=(4,1): G = (⌈4/4⌉, ⌈4/1⌉) = (1, 4). N = G0·G1 = 4. P = T0·T1 = 4·1 = 4.
- New T=(1,4): G = (⌈4/1⌉, ⌈4/4⌉) = (4, 1). N = 4·1 = 4 (**unchanged**). P = 1·4 = 4 (**unchanged**).
- Addressed-tile count (interleaved) = N = 4 both times. entry_count = 4 both times (`[R-CNT-17]`, confirmed at line 1100). Since entry_count is unchanged, extent_length (a function of entry_count per the L2 register row's formula, line 3794) is unchanged too.

**§11.3 (padding).** Eᵢ mod Tᵢ: old (4 mod 4, 4 mod 1) = (0,0) → no padding positions. New (4 mod 1, 4 mod 4) = (0,0) → no padding positions. Padding-position set: empty → empty, **preserved**.

**§14.1/§14.2 (decoded size, byte layout).** Single-channel interleaved: Q = ΣBᵢ = 1. Decoded size = P·Q = 4 both times (**unchanged**). Offset of value k = (k div C)·Q + F_{k mod C} = k·1+0 = k both times (**unchanged as a number** — byte offset 0..3 is the same set of numbers before and after).

**§11.4 (ordinal/coordinate arithmetic).** Dimension order unchanged (dim0, dim1); linearization 1, "last-declared dimension varies fastest" ⇒ dim1 fastest. s = t0·G1 + t1.
- *Old* (G=(1,4)): t0∈{0}, t1∈{0..3} ⇒ s = t1. In-tile: T=(4,1) ⇒ u0∈{0..3} (dim0 varies within tile), u1=0 fixed (T1=1). In-tile ordinal = u0·T1+u1 = u0. So **old**: tile s stores, at in-tile ordinal k (=byte offset k), the coordinate (x0,x1) = (t0·T0+u0, t1·T1+u1) = (0+k, s·1+0) = **(k, s)**.
- *New* (G=(4,1)): t0∈{0..3}, t1∈{0} ⇒ s = t0. In-tile: T=(1,4) ⇒ u0=0 fixed, u1∈{0..3}. In-tile ordinal = u0·T1+u1 = u1. So **new**: tile s stores, at in-tile ordinal k, the coordinate (x0,x1) = (t0·T0+u0, t1·T1+u1) = (s·1+0, 0+k) = **(s, k)**.

**Result**: for disk ordinal s and in-tile byte offset k, old coordinate = (k, s); new coordinate = (s, k) — a **transpose**. These are equal only on the diagonal s=k (4 of 16 (s,k) pairs); for the other 12, the coordinate a given byte denotes has changed even though not one byte of stored payload, not one index entry, and no CRC has moved.

**Cross-check against the new paragraph's claims** (hunk-13, lines 3235-3246), quoted:

> "they are what fix the coordinate each stored value denotes (`[R-GEO-06]`), so under new ones the same bytes denote samples the writer did not store there — the layer is re-tiled or transposed over bytes it never stored that way, and where the product of the tile extents and the set of padding positions are preserved no listed quantity moves, not one index entry changes, and every checksum in §8 certifies the result."

Against my derivation: "the same bytes denote samples the writer did not store there ... transposed" — **true**, exactly matches (it's a literal transpose). "the product of the tile extents ... and the set of padding positions are preserved" — **true** in my derivation (P: 4=4; padding set: ∅=∅). "not one index entry changes" — **true** (entry_count, extent_length, offsets/lengths/CRCs all unaffected, since none of them are a function of T beyond P and entry_count, both preserved). "every checksum in §8 certifies the result" — **true** in the trivial sense that checksums are computed over whatever bytes are present and would validate.

But: **"no listed quantity moves" is false**, on the immediately preceding evidence in the very same sentence. "The coordinate ... each stored value denotes" is *itself* one of "the list" — the itemized set the §14 bar protects, as established two paragraphs earlier ("The test is the effect on such a tile, and **the list** names where that effect arises", line 3201, hunk-12's paragraph) and as amended by hunk-11 to explicitly include "the coordinate (`[R-GEO-06]`) each value in the image denotes" (line 3194). My derivation shows the coordinate for 12 of 16 (s,k) pairs is not preserved under exactly the stated condition (P and padding-set preserved). So the sentence asserts, in one breath, that the coordinate changes ("denote samples ... it never stored that way") and that no listed quantity — coordinate included, by the sentence's own two-paragraphs-earlier and one-hunk-earlier definition of "the list" — moves.

**This is CHECK 4 (local contradiction), confirmed by direct derivation, not just close reading.**

### Is this byte-level?

I read the paragraph before grading it, as instructed. The sentence containing "no listed quantity moves" is embedded prose that immediately precedes a fresh, un-conditioned sentence: **"The escape is the re-type's: a new layer, or a whole-file rewrite."** This sentence is not written as "where P/padding are preserved, the escape is ..." — it is flatly stated as *the* escape, full stop, right after the confusing clause, and it is the last word on the matter before the paragraph moves to point at growth/shrink "below" as the *only other* permitted geometry changes. The **governing normative sentence** — "changing either is such a change wherever the layer stores any tile" — is unconditional; nothing in the paragraph relaxes it for the P/padding-preserved case. Under [R-CNF-05] logic (a violating file is barred under every reading that keeps the MUST NOT intact), a writer that emits a declaration-only T-change while the layer stores a tile is nonconforming under both the charitable and uncharitable reading, because the actual constraining sentence never grants a MAY.

So: **the wording is self-contradictory (CONFIRMED defect) but the rule it half-obscures is not** — the escape sentence and the unconditional bar-statement control, and a careful reader (or a verifier) resolves it correctly. I am marking this **not byte-level**, following the charter's explicit instruction to check the governing clause above the flagged sentence before grading — here that governing clause (the unconditional bar + the flatly-stated sole escape) is present and controls. I flag it because a less careful implementer really could read the "no listed quantity moves ... checksum certifies the result" clause as describing a safe subcase (it is textually adjacent to, and shaped like, hunk-12's *bona fide* carve-out pattern "a change that leaves ... meaning exactly what they meant ... is not what this bars"), and the charter specifically asked me to test this exact fork.

### Check 6 — what else is unconstrained in this structure

The structure is: the set of layer-record *declarations* whose change can move (a) what a stored tile's bytes decode to (§14 bar), or (b) a stored tile's disk ordinal (the ordinal bar), or (c), newly, the coordinate a decoded value denotes. Declarations that feed the ordinal/coordinate machinery of §11.4:

| Declaration | Enters coordinate mapping? | Enters disk ordinal? | Governed by |
|---|---|---|---|
| Dimension order | yes (tᵢ, uᵢ, s all keyed by declared order) | yes (same) | hunk-13's new clause ("wherever the layer stores any tile") |
| Tile extents Tᵢ | yes (tᵢ=xᵢ div Tᵢ, uᵢ=xᵢ mod Tᵢ) | yes (via Gᵢ) | hunk-13's new clause |
| Extents Eᵢ (grow/shrink) | no (T unchanged ⇒ same coordinate for a given (t,u)) — only *which* Gᵢ/N, hence ordinal, can shift | yes, ordinal only | the growth/shrink permissions ("below"), explicitly carved out of the new bar by the paragraph's own closing sentence |
| Channel index / count (planar) | no (channel is not part of the spatial coordinate) | yes (c·N+s) | the ordinal-bar paragraph beside it ("For a **planar** layer, a commit MUST NOT change the channel declarations...") |
| Channel count (interleaved) | no | no individual ordinal (s doesn't depend on C) but changes Q, hence byte offsets | the existing §14 bar text itself ("removing one of its channels changes Q and so is the §14 bar's subject", line 3282) |
| Linearization field | yes, in principle (it selects the s formula) | yes, in principle | **nothing names it explicitly** — but `[R-GEO-05]` (§11.4) makes 1 the only value a writer may ever emit, in every version of this major format; a "change" to it is always 1→1, so there is no live degree of freedom for a writer to exploit. I checked this is not a silent gap: `grep -n "linearization"` (16 hits) turns up no other clause conditioning a *change* to it across commits, but `[R-GEO-05]`'s "the only value this format major version defines for writers" already forecloses any other value from ever being validly emitted, superseded-generation or not. |

**Conclusion**: two is the right count *among the currently live degrees of freedom*. Dimension order and tile extents are the only declarations that (a) feed the coordinate mapping and (b) are not already fully accounted for by the growth/shrink permissions or the ordinal-bar paragraph. Linearization is a formal fourth input to the same arithmetic but is not a live gap under the current major version's `[R-GEO-05]` constraint — I note it as examined and rejected as a defect, not because it's outside the *conceptual* set of coordinate-determining declarations, but because the format currently allows no writer any freedom to move it.

### Check 6 continued — the quantifier difference

Charter's specific question: the new paragraph says "wherever the layer stores **any** tile" where the sample-type paragraph says "wherever the layer stores **a tile that carries that channel**." I checked whether this difference is warranted.

Sample type is a *per-channel* declaration (§12.1 — "A channel is declared by its layer record's channel entry"): re-typing channel A cannot disturb channel B's stored bytes, so the bar is correctly scoped to "a tile that carries that channel." Tile extents and dimension order, by contrast, are *layer-wide* declarations (§11.1 — "The owning scope ... of a layer's geometry ... is the layer") that apply uniformly to every tile regardless of channel; in a **planar** layer with one channel's tiles stored and another's entirely empty, a T/dimension-order change still moves the coordinate of every stored tile of the non-empty channel (T is shared across channels), so "any tile" (not "any tile of the affected channel," since there is no "affected channel" — it affects all of them) is the right scope. For an **interleaved** layer the point is moot since there's no per-channel tile subdivision at all. **Verdict: the differing quantifiers are each correctly scoped to their declaration's granularity; not a defect.**

## 7. Check 5 — exhaustive claims tested

- "no listed quantity moves, not one index entry changes, and every checksum in §8 certifies the result" — tested and found false for "coordinate" (§6 above); the other two clauses ("not one index entry changes", "every checksum ... certifies") hold up under my derivation.
- "wherever the layer stores any tile" (hunk-13, hunk-05) — tested against growth, shrink, and planar-channel-removal in §6/§8; holds.
- "A growth is permitted outright" (hunk-05, Rationale) — checked against the normative growth text (line 3296-3304): "It holds provided the grown geometry stays within every bound the layer's own declarations impose ... and the list is not offered as exhaustive." "Outright" in the Rationale is addressing only whether the *declaration bar* (§14/geometry bar) blocks growth, mirroring the normative text's own local phrasing ("this is an exception the permission states rather than one the carve-out supplies") before the normative text's *own* caveat two sentences later. Since the Rationale is explanatory shorthand and not itself normative, and it doesn't contradict the (later, normative) caveat, I did not treat "outright" as an independent overclaim.
- "The escape is the re-type's: a new layer, or a whole-file rewrite" — tested against the whole step; no third escape found for a T/dimension-order change. Holds.

## 8. Check 8 — back-references run forward from each insertion

Grep of the whole step region (`sed -n '3184,3354p' | grep -n "such a change\|such a declaration\|the escape\|beside it\|bar above\|such declarations\|below\b"`) located every occurrence (relative line → absolute line):
- 3210 "A channel's declared sample type is **such a declaration**" — antecedent: "a layer's declarations" / "Call this the §14 bar" (3184-3196). Unaffected by any of the four hunks (predates hunk-13's insertion point).
- 3236 "are **such declarations too**" (hunk-13's own new text) — antecedent: "such a declaration" at 3210, immediately preceding paragraph. Correctly resolves; not "further away than the reader will look."
- 3237 "**such a change** wherever the layer stores any tile" (hunk-13's own text) — antecedent: the §14 bar's "such a change" established at 3196/3211. Correct.
- 3245 "An extent's growth and shrink, **below**" (hunk-13's own text) — forward reference; confirmed present at 3289 ("**grow**") and 3306 ("**shrink**"). Resolves correctly.
- 3248 "**One effect is barred beside it**" — this is the sentence the charter specifically asks about ("beside what, now?"). Traced: "it" = "the §14 bar," established by name at 3196 and reinforced through every intervening paragraph (3210 "such a declaration," 3236 "such declarations too" — both explicitly tying the *new* tile-extent/dimension-order material into the *same* §14 bar rather than declaring a third, separate bar). Since hunk-13's inserted paragraph is textually and topically still "the §14 bar" (it says so itself — "are such declarations **too**"), the nearest topical antecedent for "it" is unchanged by the insertion. I checked the pre-insertion candidate too: before hunk-13, the immediately preceding sentence ended "...a whole-file rewrite under a fresh file_id (`[R-LIF-01]`, §20.5)" — grammatically nearest-noun antecedents there ("a whole-file rewrite", "a new layer") are equally poor nearest-sentence candidates, meaning this phrase was *already* relying on topical (not strict nearest-sentence) resolution before the repair. **Verdict: unaffected by the insertion — reference is preserved correctly, both before and after.** This is a check that passes; I report it because the charter asked for it explicitly.
- 3259 "**Either is such a change** wherever the layer stores a tile for a channel that moved" — self-contained within the ordinal-bar paragraph (its own "reordering... inserting or removing" sentence two lines above establishes what "Either" is). Not touched by, and not disturbed by, any of my four hunks.
- 3268 "the recommendation **below** to produce a new file" — forward reference to 3343-3346 ("A writer SHOULD instead produce a new file..."), present, unaffected.
- 3308 "the obligations this step states **below**" — forward reference into the shrink paragraph's own list; unaffected, outside my hunks.

I also ran the check backwards on the *inserted* text itself (hunk-11, hunk-12, hunk-13): none of the newly inserted clauses uses a back-reference whose antecedent sits further away than the immediately preceding paragraph or the just-established "§14 bar" label. No new dangling-antecedent introduced.

Additionally checked `grep -n "bar above\|bar beside\|beside this\|beside the\b"` — both hits (3319, 3332) are in the unmodified shrink paragraph, referring to "the bar beside this one" / "the bar beside the §14 bar" by name (not a bare pronoun), and both point "above" at the 3248-3253 ordinal-bar paragraph, which is itself unmoved relative to the shrink paragraph. Unaffected by any of the four hunks.

## 9. Check 7 — analogy

Searched the modified region for analogy markers (`grep -n "exactly as\|the same way\|as .* is\|likewise\|on the model\|transposed from\|following \|for the same reason"` over lines 3184-3340): all six hits (relative lines 101, 129, 135, 140, 143, 147 → absolute 3284, 3312, 3318, 3324, 3327, 3331) fall in the **shrink** paragraph, which none of my four hunks touch. None of hunks 05/11/12/13 themselves contain an "exactly as X" / "on the model of Y" construction. The closest thing to an analogy-by-citation in my scope is the `[R-GEO-06]` mis-citation already reported under Check 2 (§4) — I am filing that as CITATION rather than ANALOGY since it is a direct citation of a specific requirement rather than a comparison to another rule's quantifier, but the underlying failure mode (a citation that "almost" says the claimed thing) is the same one Check 7 warns about.

## 10. Additional prose issues found

**hunk-05 growth-sentence placement (Rationale, non-normative).** Quoted in full:

> "Re-typing a channel is the §14 bar's own subject, barred wherever the layer stores a tile that carries that channel, and free where it does not; so is a change to the tile extents or the dimension order, barred wherever the layer stores any tile. A growth is permitted outright — a position that becomes real held that channel's fill, and fill is a legal sample value — an exception §20.3's permission states rather than one the carve-out supplies."

"A growth is permitted outright" is placed immediately after introducing the new tile-extents/dimension-order bar, with no signal that "growth" here means growth of the per-dimension **extent** E (a different declaration from the just-mentioned tile extents T) — the phrase "a position that becomes real held that channel's fill" only makes sense for E growing (new positions coming into existence), never for T changing (T changes re-tile existing positions; they don't newly "become real"). I confirmed this reading against the normative growth text (line 3289-3291: "an extent MAY **grow**, since a position that becomes real held ... that channel's fill"). Because the Rationale never restates "extent" vs. "tile extent" at the point of the pivot, a reader could plausibly (mis)take this sentence as licensing tile-extent growth as an exception to the sentence immediately before it — which would directly contradict hunk-13's normative statement that the *only* escape for a T/dimension-order change is the re-type (new layer or whole-file rewrite; no growth carve-out is stated for T anywhere). Since this sits inside a `> **Rationale.**` block, it carries no force of its own (§3 above) and the actual normative text is unambiguous, so I am not marking this byte-level — but it is a genuine readability/ambiguity defect in commentary that exists specifically to explain the rule correctly.

**hunk-12 gloss grammar.** "the value each denotes, at the coordinate it denotes it" (line 3203-3204) has one "it" too many for a clean parse: it's unclear on a literal reading whether the final "it" refers back to "the value" or is a leftover subject that should have been elided (compare the sibling construction two lines earlier, hunk-11's "the coordinate §11.4 assigns any value they decode **to**," which cleanly drops the trailing pronoun in a preposition-stranding construction; this one doesn't). The likely intended reading — "meaning" = (the value a stored byte denotes) + (the coordinate at which it denotes that value) — comes through, but only with effort. Not byte-level; a wording defect worth a small rewrite (e.g., "the value each denotes, and the coordinate at which it denotes that value").

## 11. Sweeps run (verbatim, with counts and controls)

```
grep -n "11.4" spec/tarn.md                     → 12 hits (listed in transcript body)
grep -n "R-GEO-06" spec/tarn.md                 → 7 hits: 1662,1739,3019,3178,3194,3238,3255
grep -n "linearization" spec/tarn.md            → 16 hits
grep -n "R-CNT-17" spec/tarn.md                 → 10 hits
grep -n "no listed quantity" spec/tarn.md       → 1 hit: 3242
grep -n "the coordinate" spec/tarn.md           → 4 hits: 3187,3194,3204,3238 (all inside my 4 hunks' landing zone)
grep -c "coordinate" spec/tarn.md               → 23 (total; not all inspected — only the 4 above and the §11.4 definitions, which are the ones load-bearing for this repair)
grep -n "disk tile ordinal" spec/tarn.md        → 1 hit: 1736 (CONTROL — run to confirm grep finds known-present text before trusting any zero-count search)
grep -n "bar above\|bar beside\|beside this\|beside the\b" spec/tarn.md → 2 hits: 3319, 3332
sed -n '3184,3354p' spec/tarn.md | grep -n "such a change\|such a declaration\|the escape\|beside it\|bar above\|such declarations\|below\b" → 8 hits (mapped to absolute lines in §8 above)
sed -n '3184,3340p' spec/tarn.md | grep -n "exactly as\|the same way\|as .* is\|likewise\|on the model\|transposed from\|following \|for the same reason" → 6 hits, all in the unmodified shrink paragraph (outside scope)
```

Every search that returned zero (there were none in my final set — I discarded a couple of exploratory greps, e.g. an initial attempt at "the coordinate it denotes" as one un-wrapped string, which returned 0 only because the phrase wraps across the hard-wrap boundary; I re-ran it against the de-wrapped `sed -n` output, where it appears at line 3204, and only report the successful version above) was re-run against a normalized (`sed -n` range, not raw line-anchored grep) version before I trusted it, per the charter's explicit warning about hard-wrap.

## 12. Derived numbers (recap)

- G: (1,4) → (4,1). N: 4 → 4 (unchanged). P: 4 → 4 (unchanged). Q: 1 → 1 (unchanged, channel set unaffected).
- Decoded size: P·Q = 4 → 4 (unchanged). entry_count: N = 4 → 4 (unchanged, per `[R-CNT-17]`, confirmed at line 1100). extent_length: unchanged (function of entry_count only, per the L2 register-row formula at line 3794).
- Padding-position set: ∅ → ∅ (unchanged, both 4 mod 4 = 0 and 4 mod 1 = 0 pre-change; both 4 mod 1 = 0 and 4 mod 4 = 0 post-change).
- Coordinate denoted by (disk ordinal s, in-tile byte k): (k, s) → (s, k) — **moves** for 12 of the 16 (s,k) pairs (all off-diagonal ones).

All compared directly against the new paragraph's own claims (§6 above): every quantity it lists as unmoved is in fact unmoved by this derivation; the one quantity it does *not* list as an exception ("the coordinate") is the one quantity that does move, and the paragraph asserts both that it moves (earlier in the sentence) and that "no listed quantity moves" (later in the same sentence) — the contradiction reported as the primary finding.

## 13. Summary of verdicts by hunk

- **hunk-05**: Non-normative (Rationale, confirmed by label). Its new clause matches the normative rule's quantifier exactly ("any tile" = "any tile"). One genuine readability/ambiguity defect: the growth-permitted sentence's placement risks being misread as an exception to the just-stated tile-extent bar. Not byte-level.
- **hunk-11**: Normative, correctly scoped, correctly landed (no label issue). One citation defect: `[R-GEO-06]` is cited for "the coordinate ... denotes," but R-GEO-06 fixes the disk tile ordinal, not the coordinate mapping (which is an untagged bullet in the same section); the sibling clause three lines earlier in the same hunk correctly cites §11.4 instead, generally, for the identical concept. Not byte-level on its own (a wrong pointer, not a wrong rule).
- **hunk-12**: Normative, correctly landed. The restructured gloss is a legitimate, non-contradictory carve-out on its own terms; minor grammatical awkwardness in "at the coordinate it denotes it." Not byte-level. Repeats no defect from hunk-11 or hunk-13.
- **hunk-13** (first edit, my scope): Normative, correctly landed, correctly scoped against the sample-type paragraph's narrower per-channel quantifier, correctly excludes the two remaining live declarations (extent growth/shrink; channel declarations) via existing text elsewhere in the step. Contains the citation defect (shared with hunk-11) and the primary finding: a self-contradictory sentence ("the same bytes denote samples the writer did not store there" vs. "no listed quantity moves," where coordinate is itself a listed quantity), confirmed false by direct derivation, but not byte-level because the unconditional MUST NOT and the flatly-stated sole escape sentence that follow it control the actual rule regardless of how the confusing middle clause is read.

## 14. Confidence / what an empty result would have needed

I did not return an empty list. Where I *did* reject candidate findings (the growth "outright" overclaim tested against the normative caveat; the linearization-field gap tested against `[R-GEO-05]`'s single-legal-value constraint; the "beside it" anaphor tested both pre- and post-insertion; the analogy check across the whole step), I recorded the specific sentence or rule that closed each candidate, per §§6-9 above, rather than asserting a clean pass by default.
