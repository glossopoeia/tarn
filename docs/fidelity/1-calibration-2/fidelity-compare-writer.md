# Writer comparator — fidelity round 2

## Disclosure

**Files read (exactly the four permitted, nothing else):**
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4,981 lines) — read via `sed -n` ranges over multiple Bash calls, ultimately covering the entire file at least once (front matter through the appendices), plus targeted re-reads of §1–§2, §2.3/2.4, §3.1–3.3, §4.7, §5.1, §6.2–6.3, §7.2–7.4, §9.2–9.7, §12, §14.5, §20.1–20.5, §21.4, §21.6–21.7, and the "Conforming X" appendix checklist near the end of the file.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md` (edition B, 4,885 lines) — read the same way, same coverage.
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-writer-a.md` (167 lines) — read in full via Bash `cat -n`.
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-writer-b.md` (476 lines) — the Read tool's own output was too large to inline, so the harness saved it to a local tool-results file under my own session's directory (`.../tool-results/b4i09lo0e.txt`); I read that saved copy in full via the Read tool. This is the identical content of the one permitted file, not a fifth file — the harness's own overflow mechanism, not a choice of mine to read something else.

**Method.** Both editions are hard-wrapped prose, so I did not rely on single-line `grep` hits to conclude anything was present or absent. My primary method was a whole-file `diff -u a/tarn.md c/tarn.md`, which is immune to the wrap problem (it compares full lines, and reports every changed region regardless of phrase boundaries) — this produced exactly **6** diff hunks across the full ~4,900-line document. I then read each hunk's surrounding paragraphs in both files with `sed -n` to get full, unwrapped context, and cross-checked every section either walker's transcript cited (§5.1, §20.3, §20.4, §20.5, §9.2, §9.4–9.6, §6.2–6.3, §7.2–7.4, §14.5, §21.4, §21.6–21.7, §3.3, §20.1–20.2) with targeted `diff <(sed -n ...) <(sed -n ...)` calls between the two editions, confirmed byte-identical (exit 0 / empty diff) in every case except the 6 hunks. Where I report a phrase as absent from one edition, I ran a `grep -n` for it and a control `grep -c` for a phrase I already knew was present in the same file, to confirm grep was actually searching that file's content and not silently matching nothing because of wrapping or a path error (see "sweeps" below for the specific counts).

**Context that arrived unbidden.** My runtime context already contained a project `CLAUDE.md` pointer to `AGENTS.md`, a user memory-index file listing many prior-round note titles about a "TARN" project (things like a "harness vs charter" note, a "repair list vs diff" note, a "readable edition process" note, etc.), a git-status block naming five recent commit subjects on a branch called `readable`, a long list of available skills, and other environment/model/date boilerplate. None of this is part of either specification edition and I have not treated any of it as evidence about either edition's content. I did not open `AGENTS.md` or any memory-index target file. I disclose that it appeared; I am not repeating its contents beyond this notice, and nothing below relies on it. I did not list any directory (the ACCESS RULE forbids it) and did not run `git log`, `git diff`, or any web search/fetch.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/compare-writer/` was created by me (`mkdir -p`) and was empty beforehand. Working files there: `full.diff` (the `diff -u a/tarn.md c/tarn.md` output) and this transcript, which is also written verbatim to the required output path.

---

## Sweeps run, with counts (evidence for every zero claimed below)

1. `diff -u a/tarn.md c/tarn.md` → exactly 6 `@@` hunks (`grep -c "^@@" full.diff` = 6). This is the master sweep: everything not inside one of those 6 hunks is byte-identical between editions, including every passage either walker cited for W1, W2, W3, W4, W5, W7, W9, W10, W11.
2. `grep -n "§3\.3"` in both files → **1 hit in A** (none — actually zero cross-references to "§3.3" in either file; the header itself is what differs, see finding cmp-writer-04), **0 hits in C**. Control: `grep -c "Part I" c/tarn.md` = 5 (proves grep matches real content in `c/tarn.md`, so the 0 is a genuine absence, not a tooling miss).
3. `grep -n "^#### 3\.3"` → 1 hit in `a/tarn.md` (line 435), 0 hits in `c/tarn.md`. Control: `grep -n "^#### 3\."` lists 3.1 and 3.2 in both files, so headers are matchable in `c/tarn.md`; 3.3 is genuinely missing there.
4. `grep -n "cannot decode"` → 1 hit in A (line 440, inside the §3.3 Note), 0 hits in C. Control: `grep -n "Part II"` returns hits in both files (proves grep works on both).
5. `grep -n "record types §7.3 registers"` → 1 hit in A (line 191), 0 hits in C. Control: `grep -c "R-CNF-03"` in C = 11 (nonzero; the identifier itself appears repeatedly in C, so the specific 6-word phrase's absence there is genuine, not a search failure).
6. `grep -n "unable to check a requirement"` → 0 hits in A, 1 hit in C (line 3975). This is the reverse direction: content added in C that A lacks. Control: the same `diff` hunk (#6) independently shows this as an addition, corroborating the grep.
7. `grep -n "resource ground"` (control, both files) → 6 hits in A, 6 hits in C, at parallel line numbers offset by the file's constant ~103-line shift — this is the control proving that every other "resource ground" occurrence in the document (§9.7's coverage-walk rule among them) is identical text at a shifted offset, and only the two specific spots (finding cmp-writer-02/03) actually differ in content.
8. Targeted section diffs, each returning exit 0 (byte-identical) unless noted: §5.1 (empty diff), §20.3's worked example (empty diff), §20.4 in full (empty diff), §20.5 in full (empty diff), §20.1–20.2 (empty diff), §9.2 (empty diff), §9.3–9.6 (empty diff), §6.2–6.3 (empty diff), §7.2–7.4 (empty diff), §14.5 (empty diff), §21.4 (empty diff), the "Conforming reader/writer/updater/verifier" appendix checklist near the end of both files (empty diff, confirmed with `diff <(sed -n '4889,4981p' a/tarn.md) <(sed -n '4793,4885p' c/tarn.md)`). §21.6–21.7 differed by exactly the one added paragraph (hunk 6, finding cmp-writer-03).

## Derived numbers checked against the document's own arithmetic

- W2's index-region size: 32 entries × 20 bytes = 640, plus one 4-byte segment CRC (since 32 ≤ 2¹⁶ fits one segment per `[R-CNT-17]`'s `⌈entry_count / 2¹⁶⌉` term) = 644 bytes. This matches the document's own worked example number (644) in both editions verbatim, so no independent derivation was load-bearing here — I only confirmed the formula and the example agree with each other and with both walkers.
- Line-count shift between editions: A is 4,981 lines, C is 4,885 lines, a difference of 96 lines. The 6 diff hunks account for this: hunk 1/2 (the §1–§3.2 rewrite and reordering) nets out to roughly +50/-99 lines net change in that span; hunk 3 (§3.3 removed) is -9 lines; hunk 4 removes a duplicated "### 3. Terminology" header block that hunk 1 had already relocated earlier (-92 net, since the terms were moved up into hunk 1's span rather than deleted twice — see main findings); hunk 5 is a wash (0 net); hunk 6 adds +7 lines. These reconcile to within a few lines of the observed 96-line shift, which is a sanity check that `diff`'s 6 hunks are the complete story and I have not missed a 7th silent hunk.

## Rejected candidates (suspicions opened and closed)

- **Suspicion:** the missing §3.3 Note (Part I/Part II independence) is a LOSS, since writer-a's W8 answer leaned on it by name. **Closed:** the actual operative rule for W8 is `[R-WRT-09]`'s verification-depth text and §20.5's carry/re-create/drop framework, both of which are byte-identical in both editions (confirmed by direct diff). The §3.3 Note was itself inside a `> **Note.**` block in edition A — i.e., already non-normative there under `[R-CNF-01]`'s own logic — so its removal in B does not remove a rule, only removes rationale. Writer-b, working from the edition lacking this Note, independently reached the identical conclusion on W8 from the surviving operative text, which is itself evidence the Note was not load-bearing for the byte-level answer. Recorded as an OBSERVATION (cmp-writer-04), not a LOSS.
- **Suspicion:** the dropped "registered record types" item from edition B's §2.3 "conforming reader" list, and the dropped ground from B's §21.6 "cannot establish" paragraph, are full-strength LOSSes that would make a B-only implementation behave differently. **Closed (downgraded, not dismissed):** both items turn out to be restated, verbatim and identically between editions, elsewhere in the same document — the "Conforming reader —" checklist bullet near the end of both files still lists "both registered record types (`[R-CNF-03]`, §2.3)" character-for-character in both editions, and §9.7's coverage-walk text still states, identically in both editions, that a verifier declining a tile's decode on resource grounds "reports that check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)". So a complete reading of either edition yields the same operative rule. What differs is that edition B's own *local, defining* text at §2.3/§21.6 no longer matches what the rest of the same edition (via `[R-CNF-03]`/`[R-CNF-11]`) still promises it says — an internal-consistency defect introduced by the rewrite, not a whole-document rule loss. Recorded as two OBSERVATION-grade findings (cmp-writer-02, cmp-writer-03), distinguished from the one true LOSS/CONTRADICTION below.
- **Suspicion:** W6's two walkers might have answered from different rules, since edition B's rewrite touches the front matter's conformance definitions extensively. **Closed for the probe itself:** §20.3 step 4 and §21.7's unwitnessed-condition test — the passages both walkers actually quoted for W6 — are byte-identical between editions (confirmed by direct diff, and by `grep -n "no condition a file can exhibit"` returning matching lines in both files at the parallel offset). Both walkers' W6 answers, and their independent findings (writera-03 and writerb-01), describe the same real, edition-independent feature of the design (padding-geometry-dependent witnessing of a fill-value change). This is EQUIVALENT, not luck: the source text is identical, so agreement is expected, not coincidental. **Not closed, escalated instead:** reading the *general* definition this passage cites — `[R-CNF-02]`, in §2.3 — for both editions turned up the one substantive CONTRADICTION of this round (cmp-writer-01, below), which neither walker noticed because neither walker's W6 answer quoted §2.3's own text, only §20.3's application of it.

## Confidence / where I found little

I ran the master `diff -u` sweep before doing anything else, specifically so that a claim of "no other differences" would not rest on my own reading coverage but on a mechanical, complete comparison of every byte in both files. Every "identical" claim below is backed by either that diff (silence in a region = identical) or an explicit `diff <(sed ...) <(sed ...)` returning empty. I found real content in only 6 places out of a ~4,900-line document; I did not stop after finding the first (the big front-matter rewrite) and went on to check all 6, including the two small ones (a one-line rewording at old-§12.1, and the two-clause split of the "cannot establish" grounds) that a line-count-only tool might have rounded away as noise. Sections I did not re-derive independently (Part II array-model chapters, Appendices B–H) were confirmed as unchanged by the master diff, so no separate reading pass was needed for them, and I did not need to force any control search to a "confirmed present" contrast because the master diff already provides positive/negative evidence for the whole file at once.

---

## Findings

### cmp-writer-01 — CONTRADICTION (edition B only): `[R-CNF-02]`'s own definition of a conduct-rule violation directly contradicts §20.3's application of the same identifier

**Where.** Edition A, §2.3 "Conforming TARN file" (`[R-CNF-02]`), vs. edition B (`c/tarn.md`), same bullet, same identifier. Both editions' §20.3 step 4 (identical text, untouched by the rewrite) independently states the same rule as edition A's §2.3.

**Edition A, §2.3 (`[R-CNF-02]`):**
> "A few obligations this specification places on writers govern their *conduct* rather than their output — where a value is published, which registry version a writer targets (§10.3, §18.3), or the barriers a commit performs (§9.2) — and a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes. A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags rules against a set ignore-lane bit ..., §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step 4's bar on the fixed declarations of a layer that stores a tile are the cases this text states..."

**Edition B, §2.3 (same `[R-CNF-02]`):**
> "A writer obligation that governs conduct rather than output, or whose violation this specification expressly declares not to be a file-conformance violation, binds the writer, and a file that breaks one is nonconforming. `[R-CNF-02]`"

Edition B's sentence says the *opposite* of edition A's, and is self-contradictory on its own terms: it names the very category ("whose violation this specification expressly declares not to be a file-conformance violation") and then declares that breaking it makes the file nonconforming anyway.

**§20.3 step 4, identical text in both editions, applying the same `[R-CNF-02]` identifier:**
> "...This bar binds the commit as an actor: no file is nonconforming by virtue of its violation... a file such a commit leaves can be nonconforming **on its own terms**... but for a stored tile's decoded size, a padding position or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2)... no check any actor owes able to see it." (cited `[R-ERR-01]`, `[R-CNF-02]`)

This is byte-identical in both `a/tarn.md` (around line 3277–3280) and `c/tarn.md` (around line 3174–3177), and it states edition A's polarity — a conduct violation, standing alone, does **not** make the file nonconforming — inside edition B as well. So edition B now contains two passages under the same normative identifier that assert opposite rules, where edition A's two passages agree.

**Kind:** CONTRADICTION (internal to edition B; a genuine LOSS relative to edition A, which has no such tension).

**Byte-level test (edition B):** Yes. Take a file whose only defect is a writer-conduct violation with no independently witnessed byte consequence — e.g., W6's own no-padding case (a fill-value change on a layer with no edge-tile padding at all, where both walkers and I agree no register row is triggered). A verifier built strictly from edition B's §2.3 definition of `[R-CNF-02]` ("a file that breaks one is nonconforming") would report this file **nonconforming**. A verifier built from either edition's §20.3 step 4 ("no file is nonconforming by virtue of its violation... unwitnessed... no check any actor owes able to see it") — or from edition A's §2.3, which agrees with §20.3 — would report the same file **conforming**. That is a different accept/reject verdict on an identifiable file, produced by two halves of the same edition B, a tension edition A does not have anywhere in its text. Neither walker's W6 answer surfaced this, because neither quoted §2.3's own text for `[R-CNF-02]`; both quoted only §20.3's application of it (which happens to be edition A's polarity in both editions).

**Quotations:** given in full above, with section numbers and the shared identifier `[R-CNF-02]`.

---

### cmp-writer-02 — OBSERVATION (edition-B-only internal inconsistency): "both registered record types" dropped from `[R-CNF-03]`'s own defining list, though a later checklist (identical in both editions) still attributes the full list to it

**Where.** Edition A §2.3 "Conforming reader" (`[R-CNF-03]`) vs. edition B, same bullet; both editions' "Conforming reader —" appendix checklist near the end of the file (byte-identical).

**Edition A:**
> "...and MUST handle every codec and filter that §17 designates as core, both channel layouts (§14), every sample type that §12 designates as core, every user-metadata encoding §18.2 assigns, **and both record types §7.3 registers**. There are no subset profiles: software that declines to support a core codec, a core filter, either channel layout, a core sample type, an assigned user-metadata encoding, **or a registered record type** is not a conforming reader, even if it reads all other conforming files correctly. `[R-CNF-03]`"

**Edition B (same bullet, same identifier):**
> "...and MUST handle every codec and filter that §17 designates as core, both channel layouts (§14), every sample type that §12 designates as core, and every user-metadata encoding §18.2 assigns. There are no subset profiles: software that declines any of those is not a conforming reader, even if it reads all other conforming files correctly. `[R-CNF-03]`"

Edition B's enumeration — the paragraph the `[R-CNF-03]` tag is actually attached to — has five items where edition A has six; "registered record types" is gone from both the affirmative list and the "declines any of those" restatement.

**But** the "Conforming reader —" checklist bullet near the end of the document (an appendix-style summary, confirmed byte-identical between editions by direct diff) still reads, in both editions:
> "...implements all four codecs, both filters, both layouts, all thirteen sample types, both user-metadata encodings, **and both registered record types** (`[R-CNF-03]`, §2.3); ..."

So edition B's own appendix cites `[R-CNF-03]`/§2.3 as the place this requirement lives, but the §2.3 text under that tag no longer says it.

**Kind:** LOSS at the definition site (edition B states the rule "more narrowly" there, exactly the charter's LOSS pattern), but not a whole-document rule loss — the substance survives, verbatim, elsewhere in edition B.

**Byte-level test:** Weak/conditional. An implementation built strictly from edition B's §2.3 paragraph alone could treat a reader that fully implements every codec/filter/layout/sample-type/metadata-encoding but declines to process the layer or user-metadata record types themselves as a conforming reader (since "declines any of those" no longer reaches record types); an implementation that also reads the appendix checklist would not make that mistake, because the appendix (unchanged) still requires it. I record this as an internal-consistency defect specific to edition B rather than a full LOSS, since the complete document still states the rule.

---

### cmp-writer-03 — OBSERVATION (edition-B-only internal inconsistency): the "cannot establish" grounds, relocated from §2.3 to §21.6, arrive one ground short

**Where.** Edition A §2.3 "Conforming verifier" (`[R-CNF-11]`) vs. edition B's shortened §2.3 plus its new closing paragraph of §21.6; both editions' §9.7 (byte-identical).

**Edition A, §2.3, enumerates five grounds inline:**
> "...*cannot establish* — the last where some requirement is one it is unable to check on a capability or resource ground, as when the file names a format major version it does not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when it cannot execute a codec or filter (`[R-COD-11]`), **when it declines a layer's or a tile's decode on resource grounds and so cannot check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`)**, or when it declines to decode a user-metadata document (`[R-MTA-09]`)."

**Edition B, §2.3, defers entirely to §21.6:**
> "...*cannot establish*, the last where some requirement is one it is unable to check on a capability or resource ground (§21.6 names the grounds)."

**Edition B, §21.6's new closing paragraph (present only in B — hunk 6 of the diff), naming four grounds, not five:**
> "A verifier is unable to check a requirement on a capability or resource ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the file names a format major version it does not implement, a record carries MUST_UNDERSTAND = 1 with a type it does not implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4), or it declines to decode a user-metadata document (`[R-MTA-09]`)."

The layer/tile-decode-decline ground is absent from this paragraph, even though edition B's own §2.3 just promised "§21.6 names the grounds" (implying completeness).

**But**, identically in both editions, §9.7 ("Coverage verification") already states the operative consequence of that missing ground directly: "...one that declines a tile's decode on resource grounds reports that check unmade and cannot certify (`[R-CNF-11]`, `[R-ERR-04]`)." — so the rule survives, unchanged, elsewhere in edition B.

**Kind:** LOSS at the definition site (edition B's promised enumeration is incomplete), not a whole-document rule loss.

**Byte-level test:** Weak/conditional, for the same reason as cmp-writer-02 — a reader who trusts edition B's own cross-reference literally ("§21.6 names the grounds") and stops there would build an incomplete ground-list; a reader who also reaches §9.7 would not.

---

### cmp-writer-04 — OBSERVATION: §3.3's "Part I/Part II independence" Note is entirely absent from edition B, with no byte-level consequence found

**Where.** Edition A, §3.3 "Container and array model" (a `> **Note.**` block, the entire subsection); absent from edition B (no §3.3 header, no equivalent text; `grep -n "cannot decode"` and `grep -n "^#### 3\.3"` both return 0 hits in `c/tarn.md`).

**Edition A, §3.3, in full:**
> "**Note.** Part I (container) is independent of Part II (array model) by construction: no Part I structure requires decoding sample payloads, so appenders, and rewriters that carry a layer forward, operate on files whose layers they cannot decode — that independence is load-bearing for the updater rules of §7 and §20."

This Note is the passage writer-a's W8 answer cited by name ("Part I/Part II independence is stated explicitly (§3.3's Note)"). Writer-b, reading the edition that lacks it, reached the identical W8 conclusion (structural checksum verification only, no decode, for a rewriter carrying an unimplemented sample type forward) citing only `[R-WRT-09]` and §20.5 — both of which are byte-identical between editions (confirmed by direct diff).

**Kind:** the charter's LOSS test asks whether A states a rule, exception, quantifier, or definition that B does not. This Note states an architectural claim, but it was already inside a `> **Note.**` block in edition A itself — non-normative there by the document's own convention (the same convention `[R-CNF-01]`'s LOSS clause invokes for a normative statement demoted to a Note in B). Since the claim was never itself the operative rule — `[R-WRT-09]` and §20.5 carry the operative obligation, unchanged in both editions — I record this as an OBSERVATION, not a LOSS: the document's exposition of *why* the rule is safe is gone from B, but the rule itself is not.

**Byte-level test:** No. Both walkers' W8 derivations, and my own reading of `[R-WRT-09]`/§20.5 side by side (byte-identical), show the same accept/reject/drop outcome is reachable from edition B alone without this Note.

---

## Per-probe summary (W1–W11)

For every probe, I read both editions' cited passages directly rather than trusting either walker's citation.

- **W1–W5, W7, W9, W10, W11**: source passages byte-identical between editions in every case (§5.1, §20.3's worked example, §20.4 in full — including the MU=1/MU=0-PE=1/MU=0-PE=0 table and its connecting sentences, §20.5 in full, §9.2's "what a crash sees" example and §9.4–9.6, §6.2–6.3, §12's channel-declaration text). Both walkers' answers to these probes are **EQUIVALENT**: correct and matching by inheritance from identical text, not by luck — I confirmed the identity mechanically (diff) rather than assuming it from matching answers.
- **W2**: same conclusion; the exact worked example both walkers quote ("Superseding one 100,000-byte stored tile of a 32-tile interleaved layer appends...") is character-for-character identical at `a/tarn.md:3398` and `c/tarn.md:3295`.
- **W6**: both walkers' *specific* citations (§20.3 step 4, §21.7) are byte-identical between editions, and both answers are EQUIVALENT on that basis. But reading past the cited passages into §2.3's general definition of the identifier they both invoke (`[R-CNF-02]`) surfaced cmp-writer-01, a real CONTRADICTION specific to edition B that neither walker's transcript engages with, because neither quotes §2.3 itself for this probe.
- **W8**: operative rule (`[R-WRT-09]`, §20.5) byte-identical; both walkers reach the identical, correct answer. Edition A additionally carries an explanatory Note (§3.3) that edition B lacks (cmp-writer-04); this changes exposition, not the byte-level answer.
- **Each walk's own findings** (writera-01/02/03, writerb-01): all four rest on passages I confirmed byte-identical between editions (§20.4's connecting sentence for writera-01/W11; §6.3/§20.1/§20.5 for writera-02/W5; §20.3 step 4 + §21.7 for writera-03 and writerb-01/W6, which are in substance the same finding independently reached from identical text in both editions). None of these four is edition-specific; all four observations hold equally of A and B, so none is a LOSS or an ADDITION on its own — they are properties of the shared design, correctly and independently noticed by both walkers.
- **Guesses/re-reads**: neither transcript records being forced to re-read, guess, or consult another section because of textual ambiguity peculiar to its own edition; both walkers read their file in similar large sequential chunks and neither flagged uncertainty on any of the 11 probes. This is consistent with the finding that the two editions are byte-identical everywhere the probes actually turn.
