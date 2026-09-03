# Repair audit — hunk-01, hunk-03 (r29-audit3, "the-profile-and-gloss")

## Access disclosure

Read exactly:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-01.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-03.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `sed -n` / `grep -n`, various ranges, listed below)

Ran only `sed -n` and `grep -n` against `spec/tarn.md`. No other files opened, no git history, no docs/, no conformance/.

**Contamination note (mandatory disclosure):** my context contained a system-level project-instructions block (from CLAUDE.md → AGENTS.md pointer, which I did NOT open) and a user MEMORY.md index with entries such as "TARN repair prose vs rules — where this project's repair defects actually live" and "TARN lineage gate word list". I did not open any linked memory file, did not follow up on these titles, and did not let them steer where I looked — my search was driven entirely by the charter's own instructions (find the rule in §4.7, verify item 2's closing sentence, resolve §11.2/§14.2). Disclosing per the access rule; treating it as noise, not evidence.

Working notes below are the verbatim commands and outputs I used to reach each conclusion.

---

## Hunk 01

### The diff

Lands at spec/tarn.md lines 19-20, inside the very first block of the document (before "Part 0"), a blockquote beginning "> **Note.**".

Before:
```
> **structural** (its value affects where a byte lies, how it decodes,
> what a decoded value is, or whether the file is accepted) or
```
After:
```
> **structural** (its value affects where a byte lies, how it decodes,
> what a decoded value is, or whether the file, layer or tile is
> accepted at all) or
```

### Step 1 — confirm the label (R-CNF-01 test, not the ">" marker)

```
$ grep -n "" spec/tarn.md | sed -n '1,26p'
1:# The TARN Format Specification
...
12:> **Note.** How to read this document. Sections follow a fixed
13:> rubric where applicable: ...
...
23:> identifiers rather than prose positions.
24:
25:---
```
Lines 12-23 are one continuous blockquote, and its opening words are `> **Note.**`. Per `[R-CNF-01]` (quoted at spec line ~105-106: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative.") this entire block is **non-normative**. I applied the label test, not the ">" marker test — this block happens to also start with ">", but that is not why it is inert; it is inert because its first words are "**Note.**".

**Conclusion: hunk 01 lands in non-normative text**, confirming the charter's framing.

### Step 2 — find the rule this gloss restates, and compare word for word

```
$ grep -n "^#### 4\.\|^### 4\." spec/tarn.md
...
585:#### 4.7 Field taxonomy and presentation
```
§4.7 (spec lines 585-597), plain prose, **not** inside a blockquote — normative:

> "A field is **structural** if its value determines anything a conforming reader or verifier does with the bytes it reads — where a byte lies, how it decodes, what a decoded value is, or whether the file, layer or tile is accepted at all, which is the sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use."

Side by side, the enumerated clause only:

| §4.7 (normative rule) | Intro Note (repaired gloss) |
|---|---|
| "where a byte lies, how it decodes, what a decoded value is, or whether the file, layer or tile is accepted at all" | "where a byte lies, how it decodes, what a decoded value is, or whether the file, layer or tile is accepted at all" |

**Identical, word for word**, including the added "layer or tile" and "at all". Before the repair the Note said only "...or whether the file is accepted" — narrower than §4.7's actual rule (file, layer, or tile). The repair makes the gloss an exact restatement of §4.7's enumerated clause.

The repair does **not** copy §4.7's governing clause ("if its value determines anything a conforming reader or verifier does with the bytes it reads") or its trailing citation ("which is the sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use") — only the parenthetical list. That was already the Note's structure pre-repair (it never carried the "reader or verifier" framing or the three citations), so this asymmetry is pre-existing, not something hunk 01 introduced.

### Step 3 — does the gloss now import something a reader shouldn't get without context?

Checked whether "layer or tile is accepted at all" pulls in machinery (reject-file / reject-layer / reject-tile) that the intro Note, sitting before §1 and before §2.4 even exists in reading order, hasn't yet earned:

```
$ grep -n "reject-layer\b" spec/tarn.md | head -5
288: ... reject-file, reject-layer, reject-tile, or ignore-record ...
298: **reject-layer** | The affected layer's data and metadata are not usable...
```
§2.4 "Outcome classes and owning scope" (spec lines 285-311) is where reject-file/reject-layer/reject-tile are formally defined, and it comes *after* the intro Note in reading order. So a reader hitting the intro Note first sees "layer or tile accepted at all" before those outcome classes are spelled out.

But: (a) this same forward-reference shape already exists in §4.7 itself — §4.7 uses the identical enumerated clause and is also read before §2.4's... no, wait: §4.7 is at line 585, well *after* §2.4 at line 285, so §4.7 does *not* have this forward-reference problem — only the intro Note does, being the very first block in the file. (b) The Note immediately anchors the whole classification sentence to "§4.7" — `**descriptive** (none of those — §4.7)` — pointing the reader who wants grounding to the place where it's explained. (c) The Note is explicitly framed as "How to read this document" — an orientation block that precedes formal definitions by design; the document's own §1 Introduction (which the Note precedes) already uses "layer" and "tile" informally ("a per-layer index with one entry per tile") before either term is formally defined in §3. Using "layer"/"tile" informally in front matter is the document's established idiom, not something this hunk introduced.

I treat this as **not a defect**: the repair made the Note exactly match its cited source (§4.7); it did not add a new forward-reference risk beyond what already existed in the intro Note's role and the document's own front-matter idiom. It is a live judgment call, so I record it here rather than silently dropping it — but it does not survive as a finding.

### Step 4 — check 3 (label) applied fully, check 5 (exhaustive claims)

The phrase "file, layer or tile" mirrors the closed 3-way (plus ignore-record, which is record-scoped, not accept/reject-scoped) outcome-class taxonomy at spec line 288: "reject-file, reject-layer, reject-tile, or ignore-record." "File, layer or tile" exactly matches the three *rejection* scopes (ignore-record is a different kind of outcome, for records, not files/layers/tiles, and correctly excluded here since the sentence is about "accepted/not accepted" of the three addressable scopes). No overclaim.

### Step 5 — sweep for other restatements

```
$ grep -n "is accepted" spec/tarn.md
592:file, layer or tile is accepted at all, which is the sense
```
Only one other occurrence (§4.7 itself) — no stale restatement left elsewhere using the old, narrower "file is accepted" wording.

```
$ grep -n "affects where a byte lies\|value affects\|its value determines" spec/tarn.md
18: > **structural** (its value affects where a byte lies, how it decodes,
589:A field is **structural** if its value determines anything a
594:**descriptive** if it determines none of those: its value determines
```
Confirms there are exactly two places stating this classification (the Note and §4.7), and both now agree.

### Step 6 — surrounding text still reads correctly

Re-read lines 12-23 in full (above). The sentence "Every field is classified as **structural** (...) or **descriptive** (none of those — §4.7)." reads correctly with the lengthened parenthetical; no dangling clause, no broken punctuation, no orphaned "or".

### Hunk 01 — checks 1, 2, 4, 6, 7, 8 (explicit)

1. **Tense/quantifier**: the rule is atemporal (a definitional classification, not "a tile the file stores" vs "stored"). Quantifier ("the file, layer or tile") matches §4.7's quantifier exactly (verified above) — this repair *is* an exact restatement, not an independent normative rule, so check 1's concern (mismatched tense/quantifier between two independently-worded statements of the same rule) is moot: the words are identical.
2. **Citations**: `§4.7` (twice, one per class) — checked, correctly names the section holding the rule. `[R-IDX-03]` in the following sentence — untouched by this hunk, not re-verified (out of scope for the repair itself), but noted no contradiction.
3. **Label check**: done above — Note-labeled, non-normative; the *governing* rule lives in §4.7, unlabeled prose, normative, and already stated the full three-way scope before this hunk landed (so hunk 01 fixed the Note to catch up with an already-correct normative rule, not the other way around).
4. **Contradiction**: none found — the Note's new wording is a strict subset restatement of §4.7's already-existing rule; nothing elsewhere asserts "only the file can be structurally gated," which would have collided.
5. Exhaustive claims — see step 4.
6. **What's left unconstrained**: the structure here is a binary taxonomy (structural / descriptive), stated as exhaustive by construction in §4.7 ("each class being what the one before it is not"). Nothing is left as a third, ungoverned category.
7. **Analogy warrant**: none present — this hunk is a direct restatement, not an analogy ("exactly as", "likewise", etc. do not appear in the touched lines).
8. **Back-references**: the touched text introduces no new pronoun/anaphor, and none of the surrounding untouched sentences ("Normative requirements carry stable identifiers...") refer back into the touched clause. No resolution shift.

**Verdict, hunk 01: no defect found.** The restatement is exact (word for word) against its stated source (§4.7), it lands in non-normative text (correctly, since it's a gloss of a normative rule stated in full elsewhere), and it introduces no contradiction, no overclaim, and no broken back-reference.

---

## Hunk 03

### The diff

Lands at spec/tarn.md, Appendix G (line 4489, "non-normative"), inside numbered item 5.

Before:
```
   extents and a fixed layout** likewise, and item 2 names both:
   §11.3 states that tile extents are a writer's choice and that this
   specification imposes none, and §14.1 leaves the layout to the
   writer, so two writers agreeing on everything above still emit
   different numbers of tiles, of different shapes, without both
   pinned.
```
After:
```
   extents and a fixed layout** likewise, as item 2's closing sentence
   names both:
   §11.3 states that tile extents are a writer's choice and that this
   specification imposes none, and §14.1 leaves the layout to the
   writer. Without both pinned, two writers agreeing on everything
   above still disagree on bytes: the tile extents fix every tile's
   shape and with it the grid count, while the layout fixes how many
   tile-index entries the layer addresses (§11.2) and how each tile's
   values are arranged (§14.2).
```

### Step 1 — confirm non-normative status

```
$ grep -n "^### Appendix G" spec/tarn.md
4489:### Appendix G — Reproducible-writer profile (non-normative)
```
Heading itself is marked "(non-normative)", and the appendix's own preamble (spec lines ~4491-4497) states: "It adds no requirement to any actor: a writer ignoring it is fully conforming." `[R-CNF-01]` exempts "appendices identified as non-normative" — this one is identified as such in its own heading. Confirmed non-normative, matching the charter.

### Step 2 — the cross-reference: "item 2's closing sentence names both"

Read item 2 in full (Appendix G, spec lines ~4501-4514). Its last sentence, verbatim:

> "Hashing the bytes rather than an abstract notion of 'content' is what makes the identifier well defined: this format fixes no canonical serialization of logical content, and two files carrying the same arrays can legitimately differ in tiling, layout, and codec."

This is literally item 2's final sentence (item 3 begins immediately after), and it names both "tiling" and "layout" (plus "codec"). So "item 2's closing sentence names both" is accurate — not just "item 2" loosely, but specifically its closing sentence, which is the more precise claim the repair now makes. **Cross-reference resolves correctly, and at the place claimed** (the closing sentence, not merely somewhere in item 2).

### Step 3 — derive both halves of the split consequence independently

**Cause A: tile extents (§11.3).**
```
$ sed -n '1664,1682p' spec/tarn.md
```
> "Every tile of a layer has the same logical shape (T₀, …, T_{d−1})." (§11.3)
> Note (§11.3): "Tile extents are a writer's choice, and this specification imposes none..."

```
$ sed -n '1639,1648p' spec/tarn.md
```
> "For each dimension, the **grid count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉... The layer's **spatial-tile count** is N = ∏ Gᵢ..." (§11.2)

Grid count Gᵢ is a direct function of declared extent Eᵢ (fixed by "the same input," per Appendix G's own framing: "two conforming writers given the same input can emit different files") and tile extent Tᵢ (the writer's free choice, this item's subject). With E held fixed by the input, T alone determines both every tile's shape (T *is* the shape, definitionally, per §11.3's "same logical shape") and the grid count G (via the ceiling-division formula). **Attribution to "tile extents" for "shape" and "grid count" is correct** — derived, not assumed.

**Cause B: layout (§14.1).**
```
$ sed -n '1953,1959p' spec/tarn.md
```
> "The layer's layout field (§7.4) selects the mode. Field values: 0 is invalid; 1 = interleaved and 2 = planar are the only values..." (§14.1)

§11.2: "The layer's **addressed-tile count** — the number of its tile-index entries (§15) — is N for an interleaved layer and C · N for a planar layer, where C is the channel count." Given N is already fixed once tile extents are fixed (Cause A, established in the same sentence's first clause), the *only* remaining source of variability in the addressed-tile count is whether the file is interleaved (×1) or planar (×C) — i.e., **layout**, exactly as claimed and exactly matching §11.2's own stated formula.

§14.2 (spec lines 1963-1972) gives two distinct byte-offset/decoded-size formulas, selected by layout:
```
| planar, numeric channel c | P · Bᶜ | k · Bᶜ |
| interleaved | P · Q | (k div C) · Q + F_{k mod C} |
```
With P (from tile extents, Cause A) already fixed, which of these two formulas applies — and hence how bytes for a given value are arranged — is determined by layout alone. **Attribution to "layout" for "how many tile-index entries the layer addresses" and "how each tile's values are arranged" is correct**, derived from §11.2 and §14.2 respectively, given the paragraph's own "everything above [already fixed]" framing.

**Both halves check out under independent derivation — the split attributes each effect to the correct cause.**

### Step 4 — check 2, citations resolve

| Citation | Claim | Verified against | Verdict |
|---|---|---|---|
| §11.3 | "tile extents are a writer's choice and that this specification imposes none" | spec 1664-1681, Note: "Tile extents are a writer's choice, and this specification imposes none" | PASS — exact |
| §14.1 | "leaves the layout to the writer" | spec 1953-1959: layout field, writer selects 1 or 2 | PASS |
| §11.2 | "how many tile-index entries the layer addresses" | spec 1645: "addressed-tile count — the number of its tile-index entries (§15) — is N ... or C·N..." | PASS — exact phrase match |
| §14.2 | "how each tile's values are arranged" | spec 1963-1972: byte-offset table keyed by layout (planar/interleaved) | PASS |
| item 2 (internal) | "item 2's closing sentence names both [tiling, layout]" | spec ~4513-4514, item 2's actual last sentence | PASS — verified it is literally the closing sentence |

All five citations checked and pass.

### Step 5 — terminology check: "the grid count" (singular) for the aggregate tile count

```
$ grep -n "grid count\|spatial-tile count\|addressed-tile count" spec/tarn.md
1641: For each dimension, the **grid count** Gᵢ is the ceiling division
1643: The layer's **spatial-tile count** is N = ∏ Gᵢ...
1133: > no sub-records. The grid count is ⌈100 / 32⌉ = 4 (§11.2), so
```
§11.2 formally defines "grid count" as the *per-dimension* quantity Gᵢ, and separately defines "spatial-tile count" N = ∏Gᵢ as the aggregate tile count. Hunk 03's phrase "the tile extents fix every tile's shape and with it **the grid count**" uses "grid count" in the loose, aggregate sense (consistent with the informal usage already at spec line 1133's worked example, "The grid count is ⌈100/32⌉ = 4," itself singular for a specific dimension in a 1-D-flavored example). This is imprecise relative to §11.2's own defined-term split (grid count vs. spatial-tile count), but:
- It sits in a non-normative appendix, so it cannot move any byte an implementation emits or accepts.
- It doesn't contradict anything: the surrounding sentence never needs to distinguish "grid count" from "spatial-tile count" for its own point (the point is just "the tile geometry is pinned"), and the document's own example usage at line 1133 sets a precedent for this looser register.
- No other passage restates this specific sentence with the precise term that this one now imprecisely echoes.

**Logged as a rejected candidate**, not a finding: imprecise but not incorrect, non-normative, non-byte-level, and consistent with existing documentary register.

### Step 6 — sweep for restatements elsewhere needing the same fix

```
$ grep -n "different numbers of tiles\|disagree on bytes\|addresses (§11.2)\|arranged (§14.2)" spec/tarn.md
4576: disagree on bytes without it pinned. The filter is the identity
4586: above still disagree on bytes: the tile extents fix every tile's
4588: tile-index entries the layer addresses (§11.2) and how each tile's
4589: values are arranged (§14.2).
4592: agreeing on content still disagree on bytes.
```
No other location in the document restates this specific "tile extents + layout must both be pinned for byte reproducibility" claim — nothing left unswept.

### Step 7 — surrounding text: numbered item continues correctly after the lengthened sentence

Read item 5 through item 6 in full (spec lines 4569-4592). Item 5's expanded sentence ends cleanly with "...(§14.2)." and item 6 begins as a new list entry ("6. **The sentinel for every all-fill tile**..."), independent of item 5's content, no dangling reference. Confirmed the insertion did not break the list structure or leave item 5 syntactically incomplete.

### Step 8 — back-references (check 8)

The old text's clause "so two writers agreeing on everything above still emit different numbers of tiles, of different shapes, without both pinned" became, in the new text, "Without both pinned, two writers agreeing on everything above still disagree on bytes: ...". The phrase "everything above" was present in both old and new text (not newly introduced by this hunk) and resolves the same way in both — to items 1-4 and the earlier clauses of item 5 (codec, file_id, emission order, single generation, no alignment/slab, fixed filter) that the enumeration has already covered by this point. No shift in resolution since the phrase itself, and its position relative to the preceding items, is unchanged by the edit.

Checked forward into item 6 and beyond (through item 10 and the appendix's closing paragraph) for any "it"/"that"/"such"/"the X above" that might now resolve into the newly-lengthened item 5 sentence instead of its old target — item 6 opens fresh ("The sentinel for every all-fill tile, so that a tile whose samples all equal fill is never stored; otherwise two writers agreeing on content still disagree on bytes") with its own self-contained "otherwise," not a back-reference into item 5. No resolution shift found.

### Hunk 03 — checks 1, 5 (explicit)

1. **Tense/quantifier**: "the tile extents fix every tile's shape" — "every tile" matches §11.3's own claim ("Every tile of a layer has the same logical shape"), an existing normative rule (§11.3 itself, outside the blockquote — confirmed by re-reading spec lines 1664-1669, plain prose, not a Note). Quantifier matches.
2. Citations — step 4 table above, all pass.
3. Label — appendix is explicitly non-normative by its own heading; confirmed above.
4. Contradiction — none found in the surrounding item 5/6 text.
5. **Exhaustive claim**: "every tile's shape" — checked against §11.3's "Every tile of a layer has the same logical shape" — true, not an overclaim (uniform tiling is the specified invariant, not a special case).
6. **What's left unconstrained**: the structure here is "the pair (tile extents, layout) and the byte-affecting consequences of each." I enumerated every consequence of tile extents (shape, grid count G, and derivatively P) and of layout (addressed-tile-count multiplier C, byte-offset/decoded-size formula selection) reachable from §11.2/§14.1/§14.2, and every one is named in the repaired sentence or already covered by a separate, already-pinned item elsewhere in Appendix G (codec: item 1; fill/padding: closing paragraph's `[R-SER-05]`/`[R-TYP-06]`). No sibling quantity of this same "tile extents + layout" structure was found ungoverned.
7. **Analogy**: the sentence doesn't argue by analogy to another rule (it derives directly from §11.2/§14.1/§14.2, cited plainly, not "exactly as" framing). The pre-existing "likewise" two lines earlier (comparing this item to the filter-value item) was not touched by this hunk and remains structurally sound — both items follow the same "writer's choice, not implied by content, so pin it" pattern.
8. Back-references — step 8 above, no shift found.

**Verdict, hunk 03: no defect found.** The cross-reference resolves exactly where claimed (item 2's literal closing sentence). Both halves of the split consequence are independently derivable from §11.2/§11.3/§14.1/§14.2 and are attributed to the correct cause. One minor terminological looseness ("the grid count" used for the aggregate rather than the per-dimension quantity §11.2 formally defines it as) is noted but is non-normative, non-contradictory, and not byte-level.

---

## Summary of rejected candidates

1. Hunk 1: §4.7's "reader or verifier" framing and its three-citation tail are not mirrored in the Note — pre-existing asymmetry, untouched by this hunk, not a new defect.
2. Hunk 1: "layer or tile accepted at all" appears in front matter before §2.4 formally defines reject-layer/reject-tile — judged not a defect: matches §4.7 exactly, is anchored by an explicit "§4.7" citation, and matches the document's own front-matter idiom of using "layer"/"tile" informally before Part I formalizes them.
3. Hunk 3: "the grid count" (singular, aggregate) vs. §11.2's per-dimension definition of that exact term — imprecise but non-normative, non-contradictory, precedented elsewhere in the doc (line 1133), not byte-level.
4. Hunk 3: possible under-attribution of addressed-tile-count to "layout" alone, ignoring its joint dependence on N (from tile extent) — closed by re-reading the sentence's framing: N is already fixed by the first clause ("the tile extents fix... the grid count"), so layout is correctly identified as the sole *remaining* source of variability once tile extent is already pinned.

## Byte-level assessment

Both hunks sit in text `[R-CNF-01]` exempts from normative force (a Note-labeled block; an appendix identified as non-normative in its own heading). No finding survived to report, so the byte-level question is moot for this audit — there is no disputed reading here under which two conforming implementations would disagree about accept/reject or about emitted bytes.
