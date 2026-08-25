# Second look — the three findings left without a verdict

> *Editorial substitution for the repository's vocabulary gate: an ordinary-English
> use of a gate word has been replaced with an exact synonym. The substitution is
> recorded here and changes no finding, quotation or verdict.*

*`verify:B-02`'s original verifier died mid-response having stated no verdict;
X-05 and X-06 were starved by the per-auditor cap of 4. All three were
re-verified rather than assumed. Structured returns, verbatim.*


## B-02 — REFUTED, byte-level False

### Disclosure

I read exactly three files: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0099/case/case-B-02.md, the hunk /private/tmp/claude-501/.../case-adr0099/hunk-01.diff, and the specification /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. Against the spec I ran only sed line-range reads (lines 60-70, 100-112, 1460-1580, 1490-1506, 2196-2206, 1785-1800, 2820-2845, 2941-3010, 3680-3692) and greps for "R-CNF-01", "R-CNT-17", "zero-extent", "\blast\b", "^| L2[0-9]", "20.3". I read no ADRs, no docs/, no conformance/, no registry, no git history, no full.diff, no other hunk files, and did not list the case directory. Context I did not ask for did appear before I began: a project CLAUDE.md pointer, an index of the maintainer's auto-memory files (titles only, not contents), and an MCP/skills listing. I did not open any of the memory files and drew nothing from those titles; no conclusion below rests on them.

### Reasoning

The brief's quotations are all accurate and correctly located (clause at 1502-1503; preceding sentence at 1496-1498; §11.4 at 1553; §11.2 example at 1527). The repair is also substantively correct under its intended reading: since Tᵢ ≥ 1, Gᵢ = 0 iff Eᵢ = 0, so while any zero grid count stands N = ∏ Gᵢ = 0 and the addressed-tile count is 0; raising the final zero one forces N ≥ 1 and so entry_count 0 → nonzero. So the only question is whether the positional reading of "last" is live enough to be a new ambiguity. Four things foreclose it.

(1) The sentence states its own criterion, and the appositive is subordinate to it. The main clause is "Growth that changes entry_count changes extent_length with it ([R-CNT-17]) …"; "— the growth that raises … included" adds a member to a class whose membership test is already stated as an unambiguous predicate over entry_count. No reading of "last" can displace that test.

(2) The adjacent sentence is the disambiguator, eight lines above in the same block: line 1496-1498 assigns exactly the brief's case — "a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among them, the product holding at 0" — to the directory-alone class. The brief's own argument is that the positional reading makes the passage's two halves contradict each other in consecutive sentences; that is the standard ground for rejecting a reading, not for adopting it.

(3) The document's term for declaration order is the hyphenated compound "last-declared", and it is attached to "dimension", both times it occurs (line 1553 "the last-declared dimension varies fastest"; line 2202 "a band along the last-declared dimension"). Bare "last" is never used in this document for declaration order — I grepped every occurrence of the standalone word (lines 163, 194, 504, 566, 614, 1249, 1294, 1527, 1900, 2096, 3717, 3755, 4296) and each is enumeration order in prose, file order, or a spatial edge. The §11.2 example the brief cites, "the last row of tiles is padded", is the high-edge sense of a grid row, not a per-dimension index, and modifies "row of tiles", not a count. The repair says "a zero-extent layer's last zero grid count", not "the last-declared dimension's grid count".

(4) The normative rule an implementer actually builds against decides both cases and never mentions "last". §20.3 step 4 keys re-emission on "Every layer whose stored-tile set or index content this commit changes", and adds "A layer whose record alone changes keeps its extent slot, pointing at the existing region". The §13 Note at line 1791-1793 restates the same criterion and points back here: "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3, [R-WRT-04])."

The two claimed harms also do not survive. The verifier harm is refuted by the wording of row L22 itself, which tests extent_length against a formula in the current entry_count — "extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0" — not against any change across generations; the brief's E = (0, 65536) file has entry_count = 0 and slot (0,0) and passes. L21 is likewise stated over the geometry-derived count. And the writer harm is empty: with entry_count = 0 the formula yields extent_length = 0 and L22 forbids a nonzero slot, so an appender misled into "re-emitting" has zero entries and a zero-length CRC array to emit and the slot is pinned at (0,0). This is stronger than the reporter's own concession that the extra emission would merely be conforming-but-larger — in the case complained of there is nothing to emit at all.

Finally, [R-CNF-01] at line 104-106 places the whole block outside normative force ("All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale* …"), and this block opens "> **Rationale.** Empty layers serve schema-first workflows" at line 1483. That does not by itself refute a NEW_AMBIGUITY finding, but combined with (1)-(4) there is no reading under which an implementer is routed wrong. I searched specifically for a normative statement that keys re-emission on anything other than entry_count/index content, for any other use of bare "last" as declaration order, and for any second definition of "zero-extent layer" (only lines 66 and 2834, both consistent); none exists. Graded REFUTED rather than PARTIAL because I found no residual defect the brief describes wrongly — the clause is true, correctly scoped, and disambiguated in place.

### Decisive quotes

§11.1 lines 1496-1499, the sentence pair as it actually stands: "Growth / that leaves **entry_count** unchanged touches the directory alone — / a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another / stays 0 among them, the product holding at 0. Growth that changes / entry_count changes extent_length with it (`[R-CNT-17]`) …" — the criterion is entry_count, and the brief's case is expressly assigned to the other half.

§20.3 step 4 (normative, under "An appender MUST, in order"): "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full … A layer whose record alone changes keeps its extent slot, pointing at the existing region".

§13 Note, lines 1791-1793: "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

Row L22, §21: "extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0" — a formula in the current entry_count, so no verifier verdict moves and, at entry_count = 0, the slot is pinned to (0,0).

§11.4 line 1553 and §16 line 2202, the document's only declaration-order usages, both hyphenated and both modifying "dimension": "**1 = row-major** — the last-declared dimension varies fastest"; "under row-major, a run is a band along the last-declared dimension."

[R-CNF-01], line 104-106: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale* …" — and the clause sits in the block opening "> **Rationale.** Empty layers serve schema-first workflows".

## X-05 — REFUTED, byte-level False

### Disclosure

I read exactly three files: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0099/case/case-X-05.md, the hunk /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0099/hunk-01.diff, and the specification /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. I did not open full.diff, did not list the case directory, and did not read any other hunk, docs/, conformance/, registry.json, git history, or the web. Everything else I ran was sed/awk/grep against spec/tarn.md only (short non-wrapping fragments: "re-emit", "grown extents", "zero-extent", "no region at all", "entry_count = 0", "re-emitted in full", heading greps).

Unsolicited context did appear in my prompt before I began: a project instruction pointer, an index of the maintainer's private memory-note titles, and an environment preamble containing git status plus five recent commit subject lines — one of which names §11.1 and the entry_count rule, i.e. this very repair. I did not open git or those notes, and my conclusion rests only on passages I located by grepping the specification myself (§20.3 step 4 at lines 2984-2993 and the §13 Note at lines 1785-1792), but I disclose that the commit subjects were visible to me.

### Reasoning

The finding asserts that §11.1's repaired Rationale mislabels a first emission as a "re-emission", contradicting §15.4 and §5.1. The deciding text is the normative rule the repaired clause cites and summarizes, and it says the opposite.

1. The governing normative rule uses "re-emitted" for exactly this case. §20.3 step 4, [R-WRT-04], lines 2987-2994 (a numbered step, not a blockquote — normative): "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array — necessarily at a new placement ([R-LIF-01]), with ... entries new to this generation (added tiles, grown extents) emitted per §15". "Grown extents" is precisely the growth that lifts a zero-extent layer's last zero grid count. The normative rule folds that growth into "re-emitted in full" by name. §11.1's clause cites "(§20.3, `[R-WRT-04]`)" in the same breath and reuses that rule's own word. A Rationale restating its rule in the rule's vocabulary is not a local contradiction.

2. The same usage already existed elsewhere, untouched by this repair. §13's Note, line 1789-1792: "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3, `[R-WRT-04]`)." A layer at entry_count = 0 whose extents grow so entry_count changes is squarely inside that sentence. So this is settled house usage, not something hunk-01 introduced. The reporter concedes as much ("The [earlier] text had the same flaw"), which means the complaint is not against the repair at all.

3. The §5.1 quotation does not range over the same case. Its "first time" sentence is about a layer being *added* to the file: "The commit that added layer B emitted B's index region for the first time." §11.1's clause is about a layer that already exists in the directory, already has a record and an extent slot, and whose grid counts rise. Different structural event. And §5.1's own governing sentence three lines earlier (line 606-608) uses the broad form with no first/re distinction: "A commit that changes a layer's stored-tile set or index content re-emits that layer's whole tile-index region as well, at a new placement (§20.3, `[R-WRT-04]`)." The finding elevates a parenthetical illustration about a different event over the general statement that introduces it.

4. Quotation defects in the brief. (a) It cites the entry_count = 0 passage as "§15.4's Note (line 2105-2108)". It is not a Note; lines 2095-2108 are one **Example** block opening "> **Example.** A layer with entry_count = 1,000,000". Both are non-normative under [R-CNF-01], so meaning is unchanged, but the mislabelling indicates the location was quoted rather than opened. (b) The Detail argues that the extent slot and crc_of_crc_array changes are "neither of which is what 're-emitted ... at a new placement' describes" — but the repaired §11.1 clause contains no "at a new placement"; that phrase is §5.1's and §20.3's. (c) Both of those fields live in the layer *record* (§7.4 payload table, line 1002-1022), not in the tile-index *region* that the §11.1 clause is describing, so they bear on nothing the sentence claims. And §15.4's "no region at all" is a statement about what a reader fetches and verifies, not about emission vocabulary.

5. On the repair's own merits, it is an improvement, not a carried-forward defect in the sense that matters. The earlier text said "the first growth of a zero-extent layer included", which is wrong for a multi-dimensional layer: the first growth may raise one grid count while another stays 0, holding the product at 0. The new text names the correct growth — the one raising the **last** zero grid count — and the new leading sentence ("Growth that leaves **entry_count** unchanged touches the directory alone") is strictly more accurate than the earlier text's "leaves every grid count unchanged", since the two coincide except in the zero-product case the em-dash clause now names. [R-CNT-17] makes extent_length 0 whenever entry_count is 0, so "directory alone" holds.

What remains is a defensible terminological preference — one could prefer "emitted" where the region did not previously exist — inside a Rationale blockquote, against the grain of the normative rule's own wording, in text the repair did not change in that respect. That is not a local contradiction.

### Decisive quotes

Normative, §20.3 step 4, [R-WRT-04], spec/tarn.md lines 2987-2994 (numbered list item, not a blockquote): "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array — necessarily at a new placement (`[R-LIF-01]`), with entries for tiles this commit stores or supersedes written to their new state, entries for tiles that become unstored written as the sentinel, entries new to this generation (added tiles, grown extents) emitted per §15, and every other entry byte-identical at its disk-ordinal position".

§13 Note, lines 1789-1792 (pre-existing, untouched by the repair): "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

§5.1 Example, lines 606-608, the general statement the brief's quotation omits: "A commit that changes a layer's stored-tile set or index content re-emits that layer's whole tile-index region as well, at a new placement (§20.3, `[R-WRT-04]`)."

[R-CNF-01], lines 104-106: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."

Block-type correction: spec/tarn.md line 2095 opens "> **Example.** A layer with entry_count = 1,000,000: 16 segments", and the sentence the brief attributes to a "§15.4 Note" sits at lines 2105-2108 inside that same Example block.

## X-06 — REFUTED, byte-level False

### Disclosure

I read exactly three files: the finding brief /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0099/case/case-X-06.md, the hunk /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0099/hunk-01.diff, and the specification /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md. Against the spec I ran only sed line-range reads, grep for the identifiers R-CNF-01, R-CNT-17, R-GEO-06 and the string entry_count, an awk pass printing the first three characters of lines 2955-3000 (to test whether §20.3 step 4 sits inside a ">" blockquote), and a grep for section headings. I did not open full.diff, any other hunk, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, registry.json, git history, or the web, and I did not list the case directory. Unrequested context did appear in my context before I began: a project instruction file pointing at AGENTS.md, and an index of the maintainer's memory notes naming several TARN working-practice documents. I did not open any of them and drew no conclusion from their contents; I mention their presence only as required. The hunk header's claimed nearest heading ("11.1 Geometry and its validity floor" at line 1466) matches the file.

### Reasoning

The brief's quotation is accurate and in context — lines 1495-1503 read as quoted. But every load-bearing claim in the finding fails.

1. The "ordinary case" is not missing; it is subsumed by the repaired sentence's own condition. The repair did not swap one case for another — it replaced a narrower condition with a strictly more general one. {growth leaving every grid count unchanged} is a proper subset of {growth leaving entry_count unchanged}, because entry_count is normatively defined in §8's layer-record table as "equals the addressed-tile count (§11.2, `[R-CNT-17]`)" and §11.2 gives that count as N = ∏Gᵢ (or C·N planar) with Gᵢ = ⌈Eᵢ/Tᵢ⌉. The reporter's own worked example — E 100 → 120, T 32, G stays 4 — therefore satisfies "leaves entry_count unchanged" by the document's definitions, and the sentence assigns it "touches the directory alone". Nothing true was lost; the illustration changed, not the coverage. The title's assertion that the ordinary case "is no longer stated anywhere in the passage" is false as a matter of what the passage states.

2. The alleged "live misreading" is foreclosed normatively, outside the blockquote. §20.3 step 4 (normative — I checked line-by-line that lines 2984-3000 are a numbered list item, not a ">" block) says "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full" and "A layer whose record alone changes keeps its extent slot, pointing at the existing region". An intra-grid growth changes neither the stored-tile set nor index content, so the writer the reporter fears — one who concludes "any growth of a fully non-empty layer forces an index re-emission" — is corrected by a MUST-bearing procedure step, not by this Rationale. §13's sparse-writing Note (line 1786-1792) independently keys the same rule on entry_count: "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region".

3. The apposition claim is weak on the text as written. The subject is bare generic "Growth"; the dash clause is "**a** growth ... **among them**". An indefinite singular count noun cannot be co-extensive with a generic mass subject, and "among them" is an explicit partitive. The reader must ignore both the article and the partitive to reach the identity reading the finding requires.

4. The reporter's proposed repair would make the passage worse, and this is the strongest reason to refuse it. §20.3's MUST NOT bars a commit from altering, for any tile stored in the superseded generation, "the set of padding positions (§11.3)". §11.3 fixes padding positions by extent: positions whose coordinate along axis i is ≥ Eᵢ. Any growth of Eᵢ that stays inside the grid necessarily shrinks the padding set of the high-edge tiles along that axis. So the "case an implementer meets constantly" is permitted only when those edge tiles were unstored in the superseded generation — and naming it flatly as a member of the class, as the proposed wording does ("growth inside the existing grid, every ⌈Eᵢ/Tᵢ⌉ standing"), would state without caveat something §20.3 forbids in the common stored-edge-tile case. The retained illustration (a zero grid count holding the product at 0) is the one that carries no such caveat, since such a layer stores nothing. The narrowing the finding calls a loss is defensible on the document's own rules.

5. The finding's account of what was being repaired is also wrong. The old text already carried the zero-dimension carve-out ("save where another dimension's grid count is 0"). What it got wrong was its closing clause, "the first growth of a zero-extent layer included" — false for a rank ≥ 2 layer with two zero extents, where the first growth leaves N at 0. The repair's "the growth that raises a zero-extent layer's **last** zero grid count included" is the correction. I verified the surrounding claim that entry_count changes drag extent_length: index_encoding 1 is the only writable value per the layer-record table, and `[R-CNT-17]` makes extent_length a strictly increasing function of entry_count under it.

I searched for anything that would make the omission material and found the opposite each time. What would have moved me to CONFIRMED — a normative rule that depends on this Rationale to state the intra-grid case, or a place where the entry_count-keyed condition is false — does not exist; §20.3 step 4 states it normatively and §11.2 makes the derivation one ceiling division.

Byte-level: independently no. [R-CNF-01] puts all Rationale text outside the normative set, and the outcome for both cases is fixed by §20.3 step 4's MUST-bearing procedure plus `[R-CNT-17]`. A writer that never reads this blockquote emits the same bytes.

### Decisive quotes

Repaired text as it stands, spec/tarn.md 1495-1503 (blockquote): "Growth that leaves **entry_count** unchanged touches the directory alone — a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among them, the product holding at 0."

Normative force, line 104-106: "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative. `[R-CNF-01]`"

Definition that makes the "missing" case a member of the stated class, line 1021: "| entry_count | u64 | equals the addressed-tile count (§11.2, `[R-CNT-17]`) |", with §11.2: "the **grid count** Gᵢ is the ceiling division ⌈Eᵢ / Tᵢ⌉ ... The layer's **spatial-tile count** is N = ∏ Gᵢ".

The sentence that forecloses the alleged misreading, §20.3 step 4 (normative, lines 2984-2999): "Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array ... A layer whose record alone changes keeps its extent slot, pointing at the existing region".

Why the proposed repair would misstate the rule, §20.3 (lines 2996-3003): "A commit MUST NOT change a layer's declarations in a way that alters, for any tile that layer stores **in the generation this commit supersedes**, what §14 fixes for its stored bytes or how they decode — the set of padding positions (§11.3) and the content `[R-SER-05]` fixes there ..." with §11.3, `[R-GEO-04]`: "Where Gᵢ · Tᵢ > Eᵢ, the tiles at the high edge of dimension i contain **padding positions** — sample positions whose coordinate along that axis would be ≥ Eᵢ."

Independent restatement of the same entry_count-keyed rule, §13 Note, lines 1789-1792: "each commit that changes a layer's stored-tile set, or that grows its extents so that entry_count changes, re-emits that layer's whole tile-index region (§11.1, §20.3, `[R-WRT-04]`)."