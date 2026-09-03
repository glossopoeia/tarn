# Repair audit — "the force and conduct" (hunk-01, hunk-02, hunk-06)

## Disclosure

Read only:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `sed -n` ranges and `grep -n`), at the regions cited below.
- The three hunk files named in the charter: `case/hunk-01.diff`, `case/hunk-02.diff`, `case/hunk-06.diff`.

Ran only `grep -n` / `sed -n` against `spec/tarn.md`; no other files, no git history, no docs/, no full.diff, no other hunk files. Did not list the case/ directory.

Wrote only this transcript file, into the `out/` directory named in the charter (not the scratch dir, since I wrote no intermediate working files — no CRCs, no scratch copies were needed for these three hunks).

**Context contamination note:** my context did contain a large amount of material beyond the charter — a project CLAUDE.md, a user MEMORY.md index (with entries like "TARN repair prose vs rules", "TARN lineage gate word list", "TARN preflight before launch"), and various tool-availability system reminders. None of this was read as part of the audit; none of it named specific defects in these three hunks; I did not open any of the referenced memory files. I disregarded it per the charter's instruction and drew every finding below strictly from the hunk files and the specification text quoted.

## Hunk 01 — the front-matter reading-guide block's label

### The rule the repair adopts

Before: the blockquote at the top of the document (before "Part 0") read `> **How to read this document** *(non-normative).* Sections follow a fixed rubric...` — a bolded ad hoc heading followed by a parenthetical self-declaration of non-normativity, but *not* a label of the form `Note`, `Example`, or `Rationale` that `[R-CNF-01]` actually exempts by.

After: `> **Note.** How to read this document. Sections follow a fixed rubric...` — now carries the exact label `[R-CNF-01]` names.

### Check 3 — label, not marker

`[R-CNF-01]` (§2.1, line 106): "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."

This block sits **before** "### 1. Introduction" (line 27) — it is front matter (title / status / license / this blockquote), not inside §1. So the §1 exemption does not reach it. Before the repair, its only non-normativity claim was the parenthetical "*(non-normative)*", which is not one of the three magic labels `[R-CNF-01]` names. Read strictly, the pre-repair block was **not exempted by any of R-CNF-01's three carve-outs** — it was, technically, normative text, despite announcing itself otherwise. That is exactly the "check the label, not the marker" trap the charter describes, run in the opposite direction: here a `>`-marked block that *called itself* non-normative was arguably still normative under the letter of the rule.

The repair closes that gap cleanly: `**Note.**` is byte-for-byte the label pattern used by every other Note block in the document (checked at lines 108, 271, 327, 425, 497, 533, 601, 740, 750, 794, 829, 845, 907, 1169, 1217, 1265, 1271, 1283, 1330, and 25 more instances via `grep -n '^> \*\*Note\.\*\*'`). So after the repair this block is unambiguously exempt.

**Verdict:** the label change is a real, well-targeted fix of a genuine (if narrow) normative-placement defect, and it lands correctly.

### Compare the block's gloss against §4.7 (the term it restates)

Charter for hunk 1 specifically directs: does the block gloss a term the document defines normatively elsewhere, and do the two agree word for word?

Front-matter block (line 12, now inside a Note — non-normative):
> "Every field is classified as **structural** (its value affects where a byte lies, how it decodes, what a decoded value is, or whether **the file** is accepted) or **descriptive** (none of those — §4.7)."

§4.7 (line 584, "Field taxonomy and presentation", `[R-ENC-16]`, normative running text — not inside a Note/Example/Rationale block):
> "A field is **structural** if its value determines anything a conforming reader or verifier does with the bytes it reads — where a byte lies, how it decodes, what a decoded value is, or whether **the file, layer or tile** is accepted at all... It is **descriptive** if it determines none of those..."

These do **not** agree word for word: the front-matter gloss says "whether the file is accepted"; §4.7 says "whether the file, layer or tile is accepted at all." That is not stylistic compression — the document distinguishes these three acceptance scopes as substantively different things. I confirmed via `grep -n "scope"` that "validity error at layer scope" and "validity error at tile scope" are pervasive, distinct outcome scopes throughout Part I/II (lines 1029, 1099, 1988, 2059, 2105, 2395, 2418, 2423, 2431, 2434, etc.), separate from "validity error at file scope" (lines 825, 1031). A field whose value determines only whether a *layer* or *tile* is accepted — with the file otherwise still valid — is structural under §4.7 but would not obviously be so under the front-matter block's narrower wording.

**Was this introduced by the repair?** No — the hunk only changed the label line (`> **How to read this document** *(non-normative).*` → `> **Note.** How to read this document.`); the sentence containing "whether the file is accepted" is untouched, present before and after. So this discrepancy predates hunk 01.

**Does the repair make it safe?** Yes, on the normative-force axis: now that the block is unambiguously a `Note`, `[R-CNF-01]` strips it of force, so a narrower/wrong restatement here cannot itself create a conflicting *normative* rule — §4.7 is the sole authority. Before the repair, if the block really was (per strict reading) normative text, the two passages would have been two normative statements in live disagreement about what "structural" means for layer/tile-scope-only fields — a real defect. The repair, as a side effect of fixing the labeling, also retires that live conflict.

**But:** the repair touched this exact passage and had the opportunity to also correct the narrower gloss to match §4.7 (or simply say "see §4.7" without restating the definition) and did not. This is an unswept restatement inside the very block the repair edited — not introduced by the hunk, but not fixed by it either, and the hunk's own touch to this text makes leaving it stand a missed opportunity rather than a neutral non-issue. Not byte-level (the block carries no force either before this discrepancy is noticed or after), but worth recording as C-01.

### Checks 1, 2, 4, 5, 6, 7, 8 for hunk 01

- **1 (tense/quantifier):** N/A in the interesting sense — the repair doesn't restate a rule's quantifier, it relabels a block. The quantifier mismatch found is the one reported above (file vs. file/layer/tile), captured as C-01.
- **2 (citations resolve):** The block's own citation, "§4.7", is correct — §4.7 does state the taxonomy referenced. Verified by reading §4.7 in full (lines 584–610).
- **4 (contradiction in the passage):** See C-01 above — this is the one contradiction found, and it predates the hunk.
- **5 (exhaustive claims):** None introduced by the label change itself.
- **6 (uncoinstrained siblings):** N/A — no field/header structure is being pinned by this hunk.
- **7 (analogy comparison):** N/A — the hunk doesn't argue by analogy to another rule.
- **8 (insertion effects on surrounding sentences):** The hunk is a substitution, not an insertion of new material between two existing sentences — nothing before or after this blockquote refers back to it (`grep -n "How to read\|reading guide\|the block above\|the guide above"` → only the block's own line and the unrelated §21.1 heading "How to read the register" turned up). No back-reference resolution changed.

## Hunk 02 — steps 4 and 6 of the commit protocol are conduct, not output

### The rule the repair adopts

It declares, as new normative running text (not inside a Note — this matters, see below) sitting between `[R-LIF-02]`'s six-step commit protocol and the following "On creation there is no prior trailer" paragraph in §9.2:

> Steps 4 and 6 [of `[R-LIF-02]`, i.e. "make steps 1–3 durable" and "make the trailer durable" — the two storage barriers] bind a writer's conduct rather than its output. A barrier orders writes against power loss and leaves no byte trace, so a file committed without one can be byte-identical to a file committed with one. A writer that omits a barrier violates `[R-LIF-02]`, but the file it produces is not thereby nonconforming.

### Check 2 — citations resolve: `[R-CNF-02]`

Read `[R-CNF-02]` in full (§2.3, lines 150–174):

> "A few obligations this specification places on writers govern their *conduct* rather than their output — where a value is published, or which registry version a writer targets (§10.3, §18.3) — and a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes. A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text states, **and each is declared where it arises rather than enumerated here**."

This is a direct, word-for-word match to the hunk's framing:
- "bind a writer's **conduct** rather than its output" (hunk) ↔ "govern their **conduct** rather than their output" (`[R-CNF-02]`) — same governing phrase, same distinction.
- "are declared so **here**" (hunk) ↔ "each is declared **where it arises** rather than enumerated here" (`[R-CNF-02]`) — the hunk is doing exactly what `[R-CNF-02]` says such declarations do: it declares the conduct-only status of steps 4/6 at their point of definition (§9.2), rather than trying to enumerate them back at §2.3. This also explains why §2.3's own list (flags=0 / step-5 pad / §10.3 / §18.3) does *not* already include the barrier steps — by `[R-CNF-02]`'s own design, that's expected, and this hunk is the first place the barrier case gets declared. Verified with `grep -n "\[R-CNF-02\]"` (7 hits total) and `grep -n "conduct rather than\|govern their"` — only the one definitional occurrence exists, confirming no other passage had already made this declaration and the hunk isn't duplicating (or contradicting) an existing one.

**Citation verdict: resolves correctly, and precisely.**

### Check 3 — normative placement

Critical check: the new paragraph is a **plain paragraph**, not inside a `>` blockquote. This matters a great deal here, more than in most repairs, because the paragraph's content is itself doing normative work (declaring a conformance consequence under `[R-CNF-02]`'s framework), not merely explaining a rule stated elsewhere. Had this been wrapped in a Note (as its neighbors — the "Step 3 is not discharged..." Note, the "Step 5's strict increase..." Note, the "Where barriers are weaker..." Note — all are), `[R-CNF-01]` would strip it of force and the "steps 4/6 are conduct-only" declaration would not actually bind anything; the ambiguity it's meant to resolve would remain live. Confirmed by re-reading the diff: no leading `>` on any of the seven new lines. **Placement is correct and load-bearing.**

### Check 4 — contradiction in the passage

Read the whole of §9.2 (lines 1234–1310) and searched for conflicting language:

- §9.2's "Where barriers are weaker than assumed..." Note (line 1283) says safety degrades from "torn commits are invisible" to "torn commits are detected" — this is about a **crash actually occurring**; the new paragraph's claim ("can be byte-identical... in the absence of a crash") is about the **no-crash** case. These are complementary, not contradictory: skip the barrier and nothing goes wrong → byte-identical, conforming file, as the hunk says; skip the barrier and something does go wrong → torn/detected, exactly as the pre-existing Note already covered. No collision.
- §20.2 (`[R-WRT-02]`, line 3071): "A creator MUST follow `[R-LIF-02]`'s creation path... the barrier that makes the trailer durable (`[R-LIF-02]` steps 4–6 — both barriers, not one)." This is a **writer**-conformance requirement (a MUST binding the *creator* role), not a **file**-conformance requirement. Checked Appendix H's conformance-checklist entries (lines 4647–4694): "Conforming file" (§2.4, pure byte predicate) is listed separately from "Conforming writer" (§2.3), and "Conforming writer" explicitly includes "follows the commit protocol including both barriers (§9.2)" (line 4673) as one of its obligations. So the document already has, in an unrelated section, the exact two-tier structure the hunk's paragraph asserts: a writer that skips a barrier is not a *conforming writer* (violates `[R-WRT-02]`/`[R-CNF-02]`'s conduct rule), while the resulting bytes can still constitute a *conforming file*. No contradiction between these role-conditioned MUSTs and the hunk's file-level "not nonconforming" claim — they are talking about two different conformance classes, exactly as `[R-CNF-02]` sets up.
- Checked §21 (error register) for any row that would treat a missing barrier as a byte-detectable violation: `grep -n "barrier|durable|fdatasync"` (line 848, 1242–1283, 3077–3079, 3272, 3278, 3448, 4673) turned up no register row — all hits are in §9.2 itself, §20.2/20.3/20.5 writer-procedure text, or Appendix G/H. Consistent with the hunk's own logic: something invisible in the bytes cannot appear as a register row (rows are all keyed to byte-detectable conditions).

**No contradiction found**, including against text the repair did not touch.

### Check 5 — exhaustive claims

The paragraph uses "can be byte-identical" (existence claim), not "is always byte-identical" or "never differs" — correctly hedged; it does not overclaim that omitting a barrier is *always* invisible (a crash mid-write would produce a torn file, as the adjacent Note already establishes). No falsifiable universal claim found.

### Check 6 — what else in this structure is left unconstrained

Structure: `[R-LIF-02]`'s six-step commit protocol. Went through all six steps and what governs each:
1. "begin writing at exactly F" — byte-observable (subsequent Notes at lines 1265, 1271 derive dir_offset/F constraints from this; structural).
2. "append new stored-tile payloads..." — byte content; structural (§5.2 coverage classes govern it).
3. "append the new complete directory... CRC" — byte content; structural, and its own Note (line 1265) already exists.
4. **barrier** — now declared conduct-only by this hunk.
5. "append the pad... and the new trailer" — byte content; structural, and its own Note (line 1271) about the strict-increase derivation already exists; the pad-length-vs-longer-gap facet is *already* declared conduct-only elsewhere by `[R-CNF-02]` itself ("§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad").
6. **barrier** — now declared conduct-only by this hunk.

Every step in this six-step structure is accounted for: 1/2/3 are structural and independently documented; 5 has a pre-existing conduct-only carve-out for its own narrow facet (gap length) via `[R-CNF-02]`; 4 and 6 are the two the hunk newly declares. I did not find a step, or a sub-facet of a step, left ungoverned. This passes check 6 — I looked specifically for a second unpinned quantity hiding beside the one the repair names (the shape of defect the charter flags as this project's most common), and did not find one here.

### Check 7 — analogy quantifier comparison

Already covered under "Check 2" above — the hunk's governing verb ("bind... conduct rather than... output") is quoted essentially verbatim from `[R-CNF-02]`'s own governing verb ("govern their conduct rather than their output"), and the range matches: `[R-CNF-02]` ranges over "obligations this specification places on writers" generally; the hunk applies that to exactly two named steps (4 and 6) of one named requirement (`[R-LIF-02]`) — a single, well-scoped instance, not a blanket sentence trying to cover several rows/fields with one glossing verb. No mismatch found.

### Check 8 — effect on surrounding sentences

Read forward from the insertion to the end of §9.2 (through the "what a crash sees" Example, line ~1310) for every back-reference:

- "whose durability the barriers of steps 4 and 6 cover" (line 1260, in the very next paragraph after the insertion) — explicit numeric reference to "steps 4 and 6," unaffected by the insertion (nothing in the insertion redefines what "steps 4 and 6" means).
- "the strict increase above binds from the second commit onward" (same paragraph) — before the hunk this pointed one paragraph up, to "`A commit's committed_file_length is strictly greater than the prior trailer's...`" in the `[R-LIF-02]` paragraph. After the hunk, that target is now two paragraphs up, with the new barrier paragraph in between. Checked whether the new paragraph contains anything resembling "strict increase" that could hijack the reference: it does not (its content is entirely about barriers/durability/byte-identity). The phrase "strict increase" appears nowhere in the inserted text, so "the strict increase above" still resolves, unambiguously, to the same sentence it did before. **Confirmed unchanged.**
- "the Note above forbids reusing an earlier generation's [directory]" (inside the second Note, about step 5's strict increase) — resolves to the *first* Note (about step 3), which sits after the "On creation..." paragraph, i.e. entirely downstream of the hunk's insertion point. The insertion sits earlier in the sequence and does not fall between these two Notes. **Unaffected.**
- Within the inserted paragraph itself: "A writer that omits a barrier violates **this requirement**" — nearest antecedent is the paragraph's own topic sentence ("Steps 4 and 6 bind a writer's conduct...", i.e. the barrier obligation of `[R-LIF-02]` steps 4/6). Reads unambiguously; no farther-away antecedent competes for it.

No back-reference was found to have silently changed target as a result of this insertion.

### Hunk 02 summary

This repair is well-constructed: it cites its own warrant (`[R-CNF-02]`) accurately and specifically, sits in the correct (normative, unlabeled) place for its declarative force to actually take effect, does not contradict `[R-WRT-02]`'s writer-level MUST or Appendix H's "Conforming writer" checklist entry (different conformance classes, exactly as `[R-CNF-02]` distinguishes), does not overclaim, and does not leave a sibling quantity of the same structure unpinned. No back-reference shifted. I found no defect in hunk 02 itself.

## Hunk 06 — Appendix G item 5's new tile-extent/layout clause

### The rule the repair adopts

Appendix G ("Reproducible-writer profile", non-normative) item 5 previously closed two degrees of freedom (no declared alignment/slab or fixed values; a fixed filter value). The hunk adds a third: "Fixed declared tile extents and a fixed layout," justified by "item 2 names both: §11.3 states that tile extents are a writer's choice and that this specification imposes none, and §14.1 leaves the layout to the writer, so two writers agreeing on everything above still emit different numbers of tiles, of different shapes, without both pinned."

### Check 2 — citations resolve

- **§11.3** (line 1663, "Uniform tiles and edge padding"): its Note (line 1675) reads: "Tile extents are a writer's choice, and this specification imposes none..." — **matches the hunk's claim exactly**, essentially word for word.
- **§14.1** (line 1938, "The value sequence"): "The layer's layout field (§7.4) selects the mode. Field values: 0 is invalid; 1 = interleaved and 2 = planar are the only values this specification defines and the only values a writer MAY emit..." — a writer picks between the two values freely; this supports "leaves the layout to the writer," though the hunk's phrasing is a paraphrase rather than a quotation. **Verdict: accurate.**
- **"item 2 names both"** — this is the interesting one. Read Appendix G's own item 2 in full (lines 4517–4532): it is entirely about deriving `file_id` from a cryptographic hash of the file's own emitted bytes. It does not mention tile extents, layout, tile count, or tile shape anywhere. I confirmed "item 2" is correctly used *elsewhere* in the document as a reference to the file_id item — line 4596 ("The `flags` half is a creator's rule, as **item 2's identifier** is...") uses "item 2" to mean the file_id item, consistent with what item 2 actually says. So "item 2" unambiguously names the file_id/hash item throughout this document's own usage — and that item says nothing about tile extents or layout.

**This citation does not resolve.** "Item 2 names both" is false: no numbered item in Appendix G — including item 2 — names "tile extents and layout" prior to this hunk introducing the clause that itself does so, inside item 5. This reads exactly as the charter's warning describes: "a citation that points at a rule which almost says the claimed thing is the most expensive kind of defect here, because it reads as verified" — except here it doesn't even almost say it; it's a plain wrong pointer, most likely a slip (perhaps intending a self-reference to item 5, or confusing this construction with the "item 2's identifier" pattern used nearby at line 4596 for an unrelated purpose). This is C-02.

### Check 5 — exhaustive/precise claim: "different numbers of tiles, of different shapes... without both pinned"

The clause attributes one shared consequence — "different numbers of tiles, of different shapes" — jointly to *both* named freedoms (tile extents and layout) being unpinned. Tested each separately:

- **Tile extents (T₀,...,T_{d-1})**: directly fix each tile's shape and (combined with array extent) the grid counts, hence the tile count. Verified via §11.4 (line 1698): "With grid counts (G₀, …, G_{d−1}) and tile extents (T₀, …, T_{d−1})..." — unpinned tile extents genuinely produce both a different tile *count* and different tile *shape*. **Holds.**
- **Layout (interleaved vs. planar)**: checked §11.4's "disk tile ordinal" definition (`[R-GEO-06]`, line 1708): "s for an interleaved layer, and c · N + s for a planar layer... channel-major grouping." So a planar layer really does store C times as many disk-ordinal tile slots as an interleaved layer of the same geometry (confirmed by the worked Example at line 1712: disk ordinal 74 = 2·32+10 for a 4-channel planar layer where interleaved would have used ordinal 10). So unpinned layout *does* change the **number** of stored tiles — that part of the claim holds for layout too. But tile **shape** — each tile's spatial extent (T₀,...,T_{d-1}), which is what "shape" means everywhere else in this document (e.g. §11.3's "logical shape (T₀, …, T_{d−1})") — is unaffected by layout: a planar tile and an interleaved tile at the same spatial position have the identical geometric footprint; layout only changes which channel(s)' values a given disk-ordinal tile carries, not its shape. §14.1/§14.2 (byte layout, decoded size) confirm layout affects byte arrangement and per-tile byte length, not tile geometry.

So "of different shapes" is true for tile extents but **not** for layout — the compound sentence claims a single joint consequence for two freedoms where the claim is only fully accurate for one of them. This is the "analogy/claim sound for one member and unsound for the next" shape the charter specifically calls out (check 7's pattern, here arising inside check 5's exhaustive-claim test rather than via an explicit analogy marker). Recorded as C-03.

### Check 3 — normative placement

Appendix G's heading itself states "(non-normative)", and its own preamble (lines 4490–4497) is explicit: "It adds no requirement to any actor: a writer ignoring it is fully conforming." This is squarely one of `[R-CNF-01]`'s named exemptions ("appendices identified as non-normative"). Both findings above (C-02, C-03) are therefore **not byte-level**: no conforming implementation's accept/reject behavior or emittable byte set depends on this appendix being internally correct. They are genuine defects in the document's own self-consistency and citation accuracy, but carry no normative force.

### Check "appendix's own stated purpose"

Preamble's claim: the profile "closes the degrees of freedom this format deliberately leaves open," for applications needing byte-identical output. The appendix's own closing paragraph (lines 4622–4637) is explicitly framed as the authoritative summary of what the ten items close: "The items above add what is not, and the list is not short: [enumerates] ... Read the numbered items as the list; this paragraph names what they are for, not how many there are."

I checked that enumeration against item 5's actual current content (alignment/slab; filter value; and now, after this hunk, tile extents/layout):
- "the absence or fixing of a declared alignment and slab, which §16 leaves to the writer" — present, corresponds to item 5's first clause. **Holds.**
- The **filter value** clause (pre-existing, not part of this hunk) — **absent** from the closing paragraph's enumeration. Searched the full closing-paragraph list (gap content; gap extent; record/sub-record order; fill default; all-fill sentinel; single generation; alignment/slab; version_minor floor; file_id; NFC names; producer pinning of items 1/9) — no mention of "filter."
- The **tile extents / layout** clause this hunk just added — likewise **absent** from the closing paragraph's enumeration.

So the closing paragraph's claim to be "the list" of what the numbered items close is not true even before this hunk (the filter freedom was already missing), and this hunk — despite editing item 5 directly and adding a second new freedom to it — did not sweep the closing paragraph to add either the filter or the new tile-extent/layout freedom. This is an unswept-restatement pattern precisely of the kind the charter calls "this project's single most common defect": a passage that explicitly declares itself the itemized summary, and is now out of sync with the item it summarizes, in a place this repair touched but did not extend its edit to. Recorded as C-04 (non-byte-level, appendix is non-normative).

### Checks 1, 4, 6, 7, 8 for hunk 06

- **1 (tense/quantifier):** the two citations are correctly stated in their own tense/quantifier ("a writer's choice," "imposes none," "leaves... to the writer") and match §11.3/§14.1 as quoted above, aside from the "item 2" mislabel (C-02) and the shape overclaim (C-03).
- **4 (contradiction):** No local contradiction found within item 5 or against items 1–10 — the new clause doesn't collide with any carve-out or MUST in the surrounding items.
- **6 (uncoinstrained siblings):** Checked whether other tile-geometry-adjacent freedoms are left unpinned by the profile — e.g., declared channel order affects both planar disk-ordinal grouping and interleaved value order (§11.4/§14.1), but channel order is part of the caller-specified array content (declared per-layer schema), not a writer implementation choice the profile needs to close, so it is not a sibling gap of the kind check 6 looks for. No second unpinned quantity found alongside tile extents/layout specifically.
- **7 (analogy):** the "item 2 names both" clause is itself the analogy-by-citation the charter's check 7 targets; already covered as C-02 (wrong citation, not a mismatched-quantifier analogy — the cited item simply doesn't discuss the topic at all).
- **8 (insertion effects):** the new clause sits between the existing filter-value sentence and item 6 ("The sentinel for every all-fill tile..."). Checked item 6 onward through the end of Appendix G (items 6–10 and the closing paragraph) for "above"/"it"/"such" back-references: items 6–10 and the closing paragraph refer back exclusively by explicit item number ("item 1," "items 1 and 9," "item 8's creator's rule," "item 6 stores no tile...") — none use a bare "above"/"it" whose antecedent could have shifted. The hunk's own new text uses "everything above" ("two writers agreeing on everything above still emit different numbers of tiles..."), which is a vague summary phrase matching the appendix's established rhetorical template used throughout ("two writers agreeing on X still Y" — seen at items 1, 5's pre-existing filter clause, 6, and 7) rather than a technical anaphor pointing at a specific, locatable antecedent; I did not find this phrase's meaning to differ from what an equivalent phrase means elsewhere in the same appendix. No back-reference resolution was found to have changed.

## Summary

Three hunks audited, all eight checks run against each.

- **Hunk 01** — correctly moves a front-matter reading-guide block into R-CNF-01's Note exemption, resolving what was, on a strict reading, a genuine normative-placement ambiguity (the block was self-declared non-normative but did not carry the label the rule actually requires, and it sits before §1 so the Introduction exemption didn't reach it either). One residual issue: the block's field-taxonomy gloss ("whether the file is accepted") is narrower than, and disagrees with, §4.7's authoritative definition ("whether the file, layer or tile is accepted at all"); this predates the hunk and the hunk's own touch to this text was a missed chance to fix it. Not byte-level (the block carries no force either way).
- **Hunk 02** — clean. Accurately invokes and matches its warrant (`[R-CNF-02]`), is placed as unlabeled (hence normative) text so its declarative force actually lands, does not contradict the writer-level MUST for barriers elsewhere in the document (different conformance class, by the document's own design), does not overclaim, and leaves no sibling step of the six-step protocol unaccounted for. No defect found.
- **Hunk 06** — two real defects, both non-byte-level (Appendix G is non-normative): (1) the clause's own citation "item 2 names both" is simply wrong — item 2 is the file_id/hash item and never discusses tile extents or layout; (2) the clause's single stated consequence ("different numbers of tiles, of different shapes") is fully accurate for unpinned tile extents but only half-accurate for unpinned layout (layout does change tile *count*, confirmed via the planar c·N+s disk-ordinal rule, but not tile *shape*). Additionally, the appendix's own closing "summary" paragraph, which explicitly claims to enumerate everything the ten items close, omits both this hunk's new tile-extent/layout freedom and the pre-existing filter-value freedom — an unswept restatement the hunk had the opportunity, but did not take, to fix.

All eight checks were actually run for each hunk (not skipped): tense/quantifier, citation resolution, label-vs-marker, local contradiction, exhaustive-claim, sibling-quantity, analogy-quantifier, and insertion/back-reference effects. Where a check passed cleanly I said so explicitly above (hunk 02 all eight; hunk 01 all except the one gloss finding; hunk 06 all except the two/three findings noted).
