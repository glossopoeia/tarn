# diff-adversary working transcript — fidelity round 2

## Scope and access

Read only:
- A = /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (4981 lines, 302380 bytes)
- C = /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md (4885 lines, 296597 bytes)

("C" is the path segment for the file the task calls "edition B" — the task's ACCESS RULE names the second file's directory as `editions/c/`. I use "C" throughout to match the actual path; it is edition B of the fidelity test.)

No other file was opened. No directory was listed except `mkdir -p` of my own scratch/out directories (not a listing of an existing directory). All commands run were `wc`, `grep -n`, `sed -n`, and one small Python script that reads only A and C to compute heading-aligned section ranges and diff them — no other file touched.

Disclosure of context contamination: my invocation context (system reminders) included a CLAUDE.md pointer, a MEMORY.md index with entries about this project (TARN harness, lineage gate, repair defects, subagent model, refute phase, etc.), and git status showing recent commits about a "readable" branch and an "Edit log". I did not open any of the files those memory/CLAUDE.md entries name, and I did not use their claims as evidence — the paragraph below records only what I derived from reading A and C myself. The memory titles suggested *categories* of place to look (conformance classes, updater preservation, register vs. prose) which I used as a search heuristic only; every finding below is independently re-derived and quoted from A and C, not asserted on the memory's authority.

## Method

1. Extracted heading lists from both files (`grep -n '^#'`) and confirmed the section skeleton is identical except that C moves §3 (Terminology) to appear before §2 (Conformance) in reading order, while keeping the original section numbers (2.x, 3.x) — a pure reorder, not a renumbering.
2. Wrote a small Python script that pairs every heading common to both files (by normalized text) and diffs the line-range between one heading and the next, per file. This is safe against hard-wrap reflow because it compares raw line arrays, not normalized text — a false hit only means "these lines are byte-different", which I then inspected manually to classify as reflow-only or substantive.
3. Result: of ~140 headings, only these ranges differ at all:
   - front matter / title block (Note on "how to read this document" dropped)
   - §1 Introduction
   - §2.3 Conformance classes
   - §2.4 Outcome classes and owning scope
   - §2.5 (line-range artifact only, content identical — confirmed by direct `sed` comparison)
   - §3.1 Terms
   - §3.2 The reference array / §3.3 Container and array model (§3.3 is entirely absent from C)
   - §12 intro paragraph (one clause reworded)
   - §21.6 Conditions that are not violations (one paragraph appended in C)
   - Everything else — §4 through §11, §13 through §11.4, §13–§20 (all of Part I and Part II), §21.1–§21.5, §21.7–§21.9, §22, §23, §24, all Appendices A–H — is **byte-identical** between A and C. I confirmed this is not a script artifact by direct `sed`-range diffs on §2.5, §6.2, §6.3, §7.3, §17.4, §20.1, §20.3(cited), §20.4, §9.7(cited passage), §21.1–part of §21.2 (via `diff` with zero output).
4. For every place the two texts differ, I quoted both editions verbatim (control fragments only — no long verbatim reproduction) and, where a term/rule appeared to be dropped from a definitional passage, I searched the *rest of each document* for the same content restated in a technical section, to distinguish a genuine LOSS (content that appears nowhere else) from EQUIVALENT reorganization (content preserved verbatim in a numbered section, just not repeated in the glossary/overview prose).

## Findings carried to verdict — the confirmed set

### F1 — §2.3 "Conforming TARN file": the conduct/predicate rule is reversed

A (line 156, bullet body lines ~180-192 for reader; conduct clause at lines 168-179):
> "A few obligations this specification places on writers govern their *conduct* rather than their output — ... and a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes. A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags rules against a set ignore-lane bit (a creator's flags = 0, and an updater's copy-forward and set-no-other, §20.3 step 6 and §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step 4's bar on the fixed declarations of a layer that stores a tile are the cases this text states..." `[R-CNF-02]`

C (lines 206-217):
> "A writer obligation that governs conduct rather than output, or whose violation this specification expressly declares not to be a file-conformance violation, binds the writer, **and a file that breaks one is nonconforming.**" `[R-CNF-02]`

These are opposite conclusions attached to the *same requirement ID* (`[R-CNF-02]`) and the same category of obligation. I checked this against §6.3, which A explicitly cites as one of the worked examples of a "conduct-only" obligation (the creator's `flags = 0` rule). §6.3 is byte-identical in both editions:

> "a writer creating a file under this text MUST write flags = 0, but a set ignore-lane bit is not a file-conformance violation — such bits are defined by later minor versions, and files carrying them are conforming files this text's readers ignore." (A line ~900 / C same text, confirmed identical by direct `sed` diff)

So edition C's own §6.3 says a file with a set (undefined) ignore-lane bit is conforming, while edition C's own §2.3 general rule (as reworded) says a file that breaks a conduct-type writer obligation ("a writer... MUST write flags = 0" is exactly such an obligation) is nonconforming. C contradicts itself; A does not (A's §2.3 explicitly carves this exact case out by name).

Construction to bytes: **File X** — a byte-for-byte conforming minimal file per Appendix A's model (single trailer, one commit, valid directory, valid checksums throughout) except that trailer flags has bit 16 (an ignore-lane bit, undefined by this text) set to 1, with the trailer CRC-32C recomputed correctly over the changed 60 bytes so F14's checksum still verifies.
- A verifier built from A's §2.3 + §6.3: reports **conforming** (§6.3 says so explicitly, §2.3's conduct/predicate split agrees).
- A verifier built from C's §2.3 general rule alone (ignoring the contradiction and taking the newly-stated conclusion at face value): must report File X **nonconforming**, since flags=0 is exactly a writer obligation "whose violation this specification expressly declares not to be a file-conformance violation" and C says breaking it makes the file nonconforming.
- A verifier that reads all of C (§2.3 and §6.3 together) hits a live self-contradiction on the identical byte sequence.

This is a **LOSS/CONTRADICTION**, byte-level: same file, opposite certification verdict depending on which of C's own two passages (both unchanged in scope/subject from A except one word's conclusion) is applied.

### F2 — §2.3 "reaching condition" paragraph: two MUST-level clauses reversed

A (lines 253-281), the two load-bearing clauses:
> "...an exemption the condition's governing requirement grants on a ground other than the declared major **applies unchanged**, `[R-CNT-04]`'s residency exemption among them — and MUST treat its failure as **reject-file on the ground of the requirement stating it rather than on capability grounds**; the distinct diagnostic `[R-CNT-07]` asks for is owed where every reaching condition is satisfied and the declared major is one the reader does not implement."

C (lines 267-290), same two clauses:
> "...an exemption that the condition's own requirement grants for a reason other than the declared major **lapses**, `[R-CNT-04]`'s residency exemption among them. ... MUST treat a failure as **a capability refusal, not as reject-file** under the requirement that states the condition..."

Both are stated as MUST-level obligations in both editions, and both clauses are flipped to their opposite: "applies unchanged" ↔ "lapses"; "reject-file ... rather than capability grounds" ↔ "capability refusal ... not reject-file". This is not reflow or paraphrase — every content word of the conclusion is swapped for its antonym while the surrounding sentence scaffolding is preserved almost verbatim (I diffed the two 24-30 line paragraphs above line-by-line).

Construction to bytes, isolating the residency-exemption clause (`[R-CNT-04]`): `[R-CNT-04]` (A line ~4964, C same, identical text) reads: "`[R-CNT-04]` lets a reader not holding it [the front signature block, bytes [0,16)] resident defer or omit [the byte-identity check]." §6.4's remote-open path is exactly a reader that does not fetch bytes [0,16) up front (it validates the trailer from the tail and defers/omits the front-block check, per F6's register row, byte-identical in both editions: "the obligation binds a reader holding those bytes resident, and a reader that would have to fetch them MAY defer or omit the check").

**File Y** — declares version_major = 2 (a major this text's reader does not implement — only major 1 is defined); trailer magic, version fields and trailer CRC are all internally consistent and correct (so every trailer-level reaching condition the remote reader evaluates passes); bytes [0,16) (the front signature block, also a reaching condition per §6.3's "front signature block is constant... permanently") are corrupted — one byte differs from the required constant.

- Under A: the remote reader, per R-CNT-04, "applies unchanged" — it may go on deferring/omitting the front-block check exactly as it always could, reach or no reach. Having legitimately not looked at the corrupted bytes, and having every reaching condition it *did* check pass, A directs it to the `[R-CNT-07]` branch: report the distinct capability diagnostic ("TARN format major 2; this reader supports major 1") and treat File Y, from that reader's point of view, as a file it cannot open for capability reasons — it never fetches bytes [0,16) at all.
- Under C: the same exemption "lapses" for reach purposes — the remote reader is now told it MUST check every reaching condition, front-block byte-identity among them, despite not otherwise holding those bytes resident. To comply it must issue an extra range-fetch for bytes [0,16) that A never required of it. Having fetched them and found the mismatch, C's parallel clause then tells it to report this specific, real, un-fixable-by-any-future-reader defect as "a capability refusal, not reject-file" — the opposite of what §6.3's own admonition warns against ("a reader that reports an unimplemented major as corruption misleads users into discarding files that current software reads" cuts both ways: here the file *is* actually corrupt in a way no future major fixes, since F6's invariant is one `[R-CNT-24]` fixes for every major, and C's instruction to call it a capability issue anyway is the exact misdiagnosis §6.3 warns against).

Divergent, concretely: (a) which bytes a conforming remote reader is required to fetch for File Y differs between the two editions (A: need not fetch [0,16) at all; C: MUST fetch them), and (b) the diagnostic category a MUST-level rule assigns to the identical discovered defect is the opposite string in each edition. This is a **LOSS/CONTRADICTION**.

### F3 — §2.3 "Conforming reader": "both record types §7.3 registers" dropped from the no-subset-profiles list, contradicting C's own Appendix H

A (lines 188-196):
> "...and MUST handle every codec and filter that §17 designates as core, both channel layouts (§14), every sample type that §12 designates as core, every user-metadata encoding §18.2 assigns, and **both record types §7.3 registers**. There are no subset profiles: software that declines to support a core codec, a core filter, either channel layout, a core sample type, an assigned user-metadata encoding, **or a registered record type** is not a conforming reader..." `[R-CNF-03]`

C (lines 219-227), the same list and its closing sentence:
> "...and MUST handle every codec and filter that §17 designates as core, both channel layouts (§14), every sample type that §12 designates as core, and every user-metadata encoding §18.2 assigns. There are no subset profiles: software that declines any of those is not a conforming reader..." `[R-CNF-03]`

C's enumerated list has 4 items where A has 5; "both record types §7.3 registers" is gone, and "or a registered record type" is gone from the disjunctive close (which now just says "any of those", i.e., only the shortened list).

I checked whether this is a real rule change or a glossary-style trim by searching C's own document for an independent restatement — and found the opposite of a restatement: **C's own Appendix H conformance checklist still cites the record-types requirement under this exact requirement ID**, byte-identical to A:

A line 4901 / C line 4805 (identical text, confirmed by direct comparison):
> "**Conforming reader** — ... implements all four codecs, both filters, both layouts, all thirteen sample types, both user-metadata encodings, and **both registered record types** (`[R-CNF-03]`, §2.3); ..."

So in edition C, Appendix H tells an implementer that `[R-CNF-03]` (defined at §2.3) requires implementing both registered record types, while §2.3 — the actual definition of `[R-CNF-03]` — no longer says so. This is a genuine internal inconsistency introduced in C, not present in A (where §2.3 and Appendix H agree word-for-word on the same five-item list).

Construction to bytes: **Reader R** — fully implements every codec, filter, layout, sample type and user-metadata document encoding, but treats top-level record type 0x0002 (user metadata) as an unrecognized type under the generic "MU=0 → ignore" rule of §7.2 (byte-identical in both editions) rather than as the registered, PE=1 type of §7.3 — i.e., it never surfaces user metadata to callers at all, though it opens every file structurally.
- Built strictly from A's §2.3 text: Reader R is explicitly **not a conforming reader** — "a registered record type" is named in the disjunctive list of declines that disqualify it.
- Built strictly from C's §2.3 text alone (the actual rule-defining passage, read without also consulting Appendix H): Reader R's behavior is not covered by the shortened list ("any of those" refers only to codec/filter/layout/sample-type/encoding), so nothing in §2.3 disqualifies it — a self-certifying implementer following only the normative definition would conclude Reader R qualifies.
- The same implementer, if it separately consulted Appendix H's checklist (also part of edition C), would be told the opposite. The document disagrees with itself about whether Reader R is conforming.

This is a **LOSS**: a normative disjunct present in A's requirement is missing from C's statement of the same requirement, and the gap is provable without reference to edition A at all, from C's own cross-reference.

## Rejected candidates (constructions and leads that closed)

1. **§2.3 verifier bullet drops "Verifiers and updaters are readers of the files they process and inherit every reader obligation" (A) → "Verifiers are readers..." (C, "and updaters" removed).** Candidate LOSS: does C now leave updaters' reader-obligations unstated? Closed by §20.1 (byte-identical in both editions): "An appender and a rewriter are updaters: ... and is a reader of every structure it processes (`[R-CNF-11]`)" — the same fact, tagged with the same requirement ID, stated independently in the unchanged technical section. EQUIVALENT — a duplicate sentence trimmed from the overview bullet, not a rule dropped from the document.

2. **§2.3 "Conforming updater" bullet drops "— which govern every record type, not only those it does not understand" (A) after "the preservation obligations of §20.4" (C omits the clause).** Candidate LOSS: does C narrow preservation's scope to only-unrecognized records? Closed by §20.4 itself (byte-identical in both editions): "Persistence governs every record type; only the authoritative source of the flags differs" — opening sentence of the very table the bullet points to. EQUIVALENT.

3. **§21.6 appends a new closing paragraph in C** ("A verifier is unable to check a requirement on a capability or resource ground, and so reports *cannot establish*... as when the file names a format major version it does not implement, a record carries MUST_UNDERSTAND = 1 with a type it does not implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4), or it declines to decode a user-metadata document (`[R-MTA-09]`)") that is shorter than A's §2.3 enumeration of the same grounds and omits the layer/tile resource-decline ground (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`). Candidate LOSS. Closed by §9.7 (byte-identical in both editions, lines ~1536-1548 A / ~1433-1445 C): "one that declines a tile's decode on resource grounds reports that check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)" and "the verifier declines a layer on resource grounds..." — and by §17.4 (byte-identical): "A verifier that cannot execute a layer's codec or filter cannot establish that layer's conformance." Both grounds are fully and normatively stated elsewhere, unchanged. EQUIVALENT — the §2.3/§21.6 material is a relocated summary, not a dropped rule.

4. **§3.3 "Container and array model" is entirely absent from C** (present in A as a single non-normative Note with no requirement ID: Part I/Part II independence). Candidate LOSS. Closed on two grounds: (a) the removed text carries no MUST/SHOULD and no `[R-*]` tag in A — it is already non-normative under this task's own rule that only a Note *carrying a normative statement A states elsewhere as normative* counts as a LOSS; this Note states nothing that is normative anywhere; (b) `grep -n "§3\.3"` against both files returns zero hits — nothing else in either document points to this section, so no dangling cross-reference results. EQUIVALENT / non-normative cut.

5. **§3.1 "addressed tile" glossary entry**: A: "every tile of a layer is *addressed*" (unconditional). C: "a tile is *addressed* in a generation if that generation's tile index has an entry for it: the tiles of the layer's grid under the geometry that generation declares (§11.2, §15)" (explicitly per-generation/geometry-conditional). Candidate LOSS/ADDITION: does C introduce a generation-relative notion of addressing A does not have? Closed by checking that A's own body text already ties addressed-tile count to "the geometry-derived addressed-tile count" per generation (§7.4 area, e.g. line 1142 "entry_count ... equals the addressed-tile count (§11.2)", byte-identical in C) and that extents can grow across commits (§20.3, unchanged) — so "addressed" was always implicitly a function of the generation's declared geometry in A; C's glossary entry just states explicitly what A's body already required. EQUIVALENT — a clarifying restatement, not a new rule.

6. **§1 Introduction pillar bullets drop specific figures**: A's "Random access without a server" pillar states "two range requests" for opening and a three-part cost breakdown (segment-CRC array, index segment, tile bytes) for reading a tile, tied to §21.9's guarantee; C's rewrite says only "a small fixed number of range requests." Similarly A's "Append without rewriting" pillar names the recovery-truncation and no-backward-scan behaviors and the "full tile and whole index" cost of small edits; C drops these specifics. Candidate LOSS. Closed by confirming §6.4, §19.4, §9.5, §9.6, §20.3, §21.9 are all byte-identical between editions (per the heading-aligned diff sweep) and state every one of these figures in full normative form; the Introduction in both editions is an unnumbered, non-normative overview with no requirement IDs of its own. EQUIVALENT — the readability pass thinned the preview, not the specification.

7. **Front-matter "how to read this document" Note** (rubric + structural/descriptive field classification) dropped from C's title block. Closed: content restated in full, unchanged, at §4.7 (byte-identical in both editions) which the Note itself points to. EQUIVALENT.

## Evidence for the "confidence_empty" ground

I ran the heading-aligned section diff (step 3 above) over the entire document, both directions (every A heading matched against C and vice versa via the shared normalized-text index), and it is a *complete* sweep, not a sample: every one of the ~140 headings in A has a matching heading in C, and the diff reports **byte-identical** ranges for roughly 130 of them. I did not stop after finding the three §2.3 issues; I additionally hand-verified (full `sed`+read, not just `diff`) §2.4, §2.5, §3.1, §3.2, §3.3, §6.2 (implicitly via §2.3's citation), §6.3, §7.3, §9.7's relevant passage, §12's intro, §17.4, §20.1, §20.4, and §21.6 in full, and spot-checked the Appendix H checklist lines for both `[R-CNF-03]` and general structure. Every zero I report above ("§6.3 identical", "§20.1 identical", "§20.4 identical", "§9.7 passage identical", "§17.4 identical", "Appendix H line identical") is backed by a control: I obtained both editions' text for that exact passage side by side (via `sed -n` on both files) and compared them, not merely searched for a keyword's presence.

## Output note

This transcript is written to /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-diff-adversary.md as instructed. My scratch directory (/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/diff-adversary/) holds this same file (transcript.md) as my working copy before final copy-out.
