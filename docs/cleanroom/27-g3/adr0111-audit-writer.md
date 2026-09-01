# Writer auditor transcript — case-adr0111

## Disclosure

Context that appeared in my runtime unbidden, before I read anything: a
CLAUDE.md pointer to AGENTS.md, an auto-memory index (file names only:
"Naming constraint on published rationale", "TARN working cadence", "Rob's
decision style", "Workflow verifier failures", "Spec edits need propagation
checks", "TARN register is the corpus build list"), the user's email, and
today's date. None of this is part of the specification or evidence about the
change under audit. I did not open any of the memory files, AGENTS.md, or
CLAUDE.md, and did not treat this material as instructions or as evidence.
Per my charter I disregarded all of it.

Also present: system-reminders listing deferred tools and skills. I did not
invoke any of them — irrelevant to a document-only read/verify task.

## What I read

1. My seven hunk files, in full, via `cat`:
   `hunk-09.diff` through `hunk-15.diff` in
   `/private/tmp/claude-501/.../scratchpad/case-adr0111/`.
2. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
   (the current file), the following regions, via the Read tool:
   - lines 1–~45 region via a grep, then lines 360–401 (§3.1 glossary:
     *directory*, *trailer*, *front signature block*, *generation*)
   - lines 756–900 (§6.2 Trailer table, §6.3 Version and flag gates, §6.4)
   - lines 1222–1441 (§9.1 through the start of §9.7: commit protocol,
     generations/file_id/caching, recovery-before-append, concurrency,
     recovery scan, start of coverage verification)
   - lines 3010–3220 (§20.1 Writer tiers, §20.2 Creation, §20.3 append
     procedure through step 6, the Note and Example after it)
   - lines 3220–3380 (the "three shapes a commit takes" example, §20.4
     Re-emission and preservation, its Rationale, start of §20.5 Compaction)
   - lines 3379–3477 (rest of §20.5: relocation, the compaction diagram
     example, verification depth, the closing Note, start of §21)
   - lines 3796–3876 (§21.7 "What no check detects")
3. Targeted greps against the current file only: `generation` (all hits),
   `supersed*` (all hits), `adjacent` (all hits), `generation 1|one|7|-1`
   (zero hits — confirms full sweep), `reserved` (trailer-table hit plus
   others), `R-CNT-14`/`R-ENC-13` occurrences, `F17`/`F8`/`F14` occurrences,
   and a scoped grep for `generation` inside the §21 register span only.

I did not read `full.diff`, any hunk file outside my charter, any file under
`docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or any git history. I
ran no git commands. I made no edits.

## Header mechanical checks

For each of the 7 hunks I compared the stated "lands at lines N–M" and
"nearest preceding heading" against the current file:

- hunk-09: claims 3027–3028, heading 3025 "20.1 Writer tiers" — confirmed
  exactly. Body ("its first generation") matches.
- hunk-10: claims 3052–3054, heading 3044 "20.2 Creation" — confirmed
  exactly.
- hunk-11: claims 3197–3202, heading 3059 "20.3 The append procedure" —
  confirmed exactly (step 6 of the appender's numbered list).
- hunk-12: claims 3319–3332, heading 3275 "20.4 Re-emission and
  preservation" — confirmed; the cited range is exactly the Rationale's
  changed span.
- hunk-13: claims 3352–3373, heading 3334 "20.5 Compaction" — confirmed;
  content matches (note the diff's added-line count is larger than the
  cited range because of hard-wrap reflow shifting line boundaries even
  where wording is identical — not a real mismatch).
- hunk-14: claims 3436–3439, heading 3334 "20.5 Compaction" (same section,
  no new heading crossed) — confirmed against the compaction diagram.
- hunk-15: claims 3454–3454, heading 3334 — confirmed.

No header/body mismatches found in my seven hunks.

## Trailer layout cross-check (background fact, not itself a hunk)

Current §6.2 table: magic(8)@0, version_major(2)@8, version_minor(2)@10,
flags(4)@12, dir_offset(8)@16, dir_length(8)@24, committed_file_length(8)@32,
file_id(8)@40, reserved(12)@48, CRC(4)@60. Sums to 64. This matches the
brief's description of the post-removal layout exactly and is internally
self-consistent (byte math checks out). §3.1's glossary entry for
*generation* already reads "one committed state of a file (§9). No field
numbers generations; successive generations of one file are ordered by the
strictly increasing committed file length their trailers carry (§9.3)" —
i.e. the abstract, un-numbered notion of "generation" that hunks 9, 11, 12,
13 rely on is already established elsewhere in the document, not invented ad
hoc by these hunks.

## Per-hunk analysis

**Hunk 9 (§20.1, creator tier).** Rule adopted: a creator's single commit is
called "its first generation" rather than "generation 1" — descriptive
ordinal language, not a numbered field. Checked against §3.1's generation
entry (no numbering) — consistent. No citation to verify (none added). Not
in a blockquote. No exhaustive claim, no analogy language.

**Hunk 10 (§20.2, creation path).** Rule adopted: creation's trailer is
called plainly "the trailer" (with a fresh nonzero file_id) rather than "the
generation-1 trailer." Checked against §9.2/[R-LIF-02]'s "on creation"
paragraph (front signature block, then steps 2–6) — the barrier/pad/trailer/
barrier sequence hunk 10 restates matches R-LIF-02 steps 4–6 exactly (payload
= step 2, directory+CRC = step 3, barrier = step 4, pad+trailer = step 5,
barrier = step 6, all folded into hunk 10's "the barrier, the pad, the
trailer ..., and the barrier"). "(§9.3)" for "fresh nonzero file_id" checked
against §9.3's file_id description — matches. No information is lost by
dropping "generation-1": that fact is now carried by hunk 9's "first
generation" phrasing one subsection up, and by the trailer no longer having
a field to state it in.

**Hunk 11 (§20.3 step 6, commit).** Rule adopted: the trailer's ordering
guarantee is now expressed as committed_file_length ("equal to the new end
— necessarily above the F step 1 established, this commit having appended
at least a directory, a pad and a trailer") instead of "generation one
greater." Checked against §9.2's own derivation (its second Note, lines
1263–1273): step 1 begins at prior F, R-LIF-01 freezes bytes below it, the
new directory must lie at dir_offset ≥ prior F, dir_length ≥ 4 (R-CNT-06),
so new F ≥ prior F + 68, rounded up to a 64-byte multiple ⇒ ≥ prior F + 128.
Hunk 11's justification ("appended at least a directory, a pad and a
trailer") is a shorter, less quantitative version of the same argument — it
asserts direction (new F > old F) rather than the +128 floor, but does not
contradict the fuller derivation; it is a legitimate abbreviated corollary,
not an unsupported new rule. [R-CNT-08] citation (ignore-lane bits copied
forward) checked against §6.3's flags paragraph — matches verbatim in
substance. [R-CNT-26] citation (version_minor) checked against §6.3's
"appender the maximum of that floor and the prior trailer's minor" — matches.
`[R-WRT-04]` tag position unchanged from the original, not itself a claim to
verify.

**Hunk 12 (§20.4 Rationale, "adjacent generations").** This is one of the
two hunks the charter flags for judgment. Rule adopted: the preservation
claim is re-anchored from "adjacent generations' records differ exactly by
..." to "the directory a commit emits differs from the one it supersedes
exactly by ..." — replacing a relation that needed generation *numbers* to
define adjacency with one anchored directly on the commit's own supersession
relation (a commit always supersedes the immediately-prior live directory;
there is no way to skip one, so this is the same pairing "adjacent"
described, just derived without counting). Then the text adds an explicit,
honest caveat: the claim holds as "a commit's own" fact regardless of
whether an outside observer can pair two arbitrary directories from the
format alone — and it cannot, because nothing in either trailer says how
many commits separate them.
- Checked `[R-CNT-14]` ("record order carries no meaning") against its
  definition at line 1022–1029 ("Record semantics MUST NOT depend on record
  order... `[R-CNT-14]`") — accurate match.
- Checked `[R-ENC-13]` ("a re-serializer that renormalized a name would
  change the name's identity") against its definition at lines 560–562
  ("Name comparison is raw bytes... Readers MUST NOT normalize... `[R-ENC-13]`")
  — accurate match, and the §4.6 worked example (NFC vs NFD "different
  name") confirms the reading.
- Checked "the live state names one generation" against §3.1's generation
  entry and §9.5's "the generation it validates" — consistent.
- Checked "two trailers of one file_id are ordered by committed_file_length
  without being counted" against §9.3's Note ("F counts bytes, not commits
  ... no field records it") — this is the same claim, restated; word-for-word
  consistent, not contradicted.
- Checked "§9.7 does not reconstruct" against §9.7's opening sentence ("A
  verifier checking [R-CNT-02]'s partition walks the live state only") —
  accurate.
- Checked "a tool ... enumerates commit states from the physical file (§9.6)"
  against §9.6's text ("A recovery tool enumerating a file's commit states
  continues the same probe to offset 0") — accurate, and "gets only the
  ones that file still carries" matches §9.6's discussion of rollback/
  truncation being invisible in-format.
- This is a labelled `> **Rationale.**` block; checked that no new
  obligation is smuggled into it — every sentence is either a restatement of
  an already-normative rule (R-WRT-05's byte-identical re-emission,
  R-LIF-02/03's ordering) or a description of what §9.6/§9.7 do — no new
  MUST/SHOULD is introduced here, so the non-normative labelling is
  appropriate and nothing depends on this block alone for force.
- Verdict: this reads as a strict improvement, not "reads as though nothing
  changed" — the loss (no observer-side pairing without out-of-band tooling)
  is stated plainly.

**Hunk 13 (§20.5, compactor's fresh file_id / dropped "generation 1").**
The second hunk flagged for judgment. Rule adopted: the compactor still
MUST mint a fresh file_id (unchanged obligation); the text drops "and
generation 1" (no such field exists) and adds two new sentences: (a) the
fresh file_id alone is "the whole of that mechanism" that makes the output a
different file under R-LIF-03, "before any comparison of
committed_file_length"; (b) what's lost is that nothing in the trailer marks
"first committed state," so a compacted output and a hundred-times-appended
file are indistinguishable by trailer alone.
- Checked `[R-LIF-01]` ("whole-file rewrite under a new file_id
  (compaction, §20)") against §9.1's exact text — verbatim match.
- Checked `[R-LIF-03]`'s "different file_id or lower F, treat as a
  different file" (§9.3) — this licenses reaching "different file" on
  file_id disjunction alone, supporting claim (a). I checked whether "before
  any comparison of committed_file_length" overclaims a specific check
  *ordering* the rule's prose doesn't literally specify (the rule states a
  disjunction, not a sequence) — this is a rhetorical/logical point (you
  don't *need* F to reach the verdict once file_id differs), not a claim
  about which byte a reader inspects first; it doesn't change what bytes a
  conforming implementation must emit or accept, so even if read
  uncharitably it is not byte-level. I did not raise it as a finding.
- Checked "no field counts commits" against the §6.2 trailer table (5
  non-reserved fields, none of which counts commits) and against §9.3's
  Note ("F counts bytes, not commits... no field records it") and §21.7
  ("no field of a file records how many commits that history holds") — all
  three independently confirm the claim; it is exhaustively correct given
  the trailer's actual field list.
- Checked the "indistinguishable ... by their trailers alone" claim for
  overclaim: pre-removal, a compacted output (generation 1) *was*
  distinguishable from a hundred-times-appended file (generation 101) by
  the old counter — so something real was lost, and the new text names
  exactly that loss (commit-count signal) without overclaiming a loss that
  never existed (it does not claim the old field could distinguish
  compaction from creation, which it never could — both start at generation
  1). This is an accurate, appropriately scoped statement of the loss.
- Checked "the output has no prior trailer, which is the case that path
  states" against §9.2's "On creation there is no prior trailer" — matches.
- Cross-checked against §21.7 (not itself in my hunks, but directly
  relevant): it already lists exactly **three** unwitnessed compaction
  obligations — "its fresh file_id draw, the unknown ignore-lane bits it
  MUST carry forward, and the floor its version_minor SHOULD take" — with
  no fourth item for a generation reset. This corroborates that hunk 13's
  removal of the "generation 1" obligation is complete and swept elsewhere
  in the document, not merely local.
- Verdict: sound: the mechanism claim is textually supported by R-LIF-03,
  and the loss is honestly and precisely named.

**Hunk 14 (§20.5 compaction diagram, input/output annotations).** Rule
adopted: the diagram drops "generation = 7" / "generation = 1" annotations,
leaving only file_id = X / file_id = Y. Checked that nothing downstream in
the accompanying prose (read in full, lines 3442–3462) depends on the
dropped annotations — it doesn't; the prose talks about file_id, ranges, and
slack, never generation numbers. Checked the caption line "the output is a
different file rather than a later generation of the same one" (unchanged
by this hunk) for self-consistency — still coherent using the abstract
generation concept.

**Hunk 15 (§20.5, "generation 7's bytes for generation 1's ranges" → "the
input's bytes for the output's ranges").** Rule adopted: same substitution,
same paragraph, one sentence. Checked against the surrounding unchanged
sentence "a cache keyed (file_id, range) is sound precisely because ranges
never change beneath a file_id (§9.3)" — the replacement text keeps the
subject (bytes served for the wrong ranges) intact and only removes the
numeric generation labels, no semantic change, no citation added.

## Untouched-but-relevant text checked per the charter's explicit instruction

**§20.3 step 4's declaration-change bar** ("the generation this commit
supersedes," lines ~3119–3193): read in full. Its force rests on "generation"
as an abstract prior state (§3.1: "stored in a generation" is defined
relationally, not against a numbered field) and on "supersede," which is
used throughout the document (§9.1, §15, §20.3, §20.4) as an operational/
structural relation (a new tile-index entry or directory replaces what a
prior commit's structures established), never as something requiring a
numeric counter. Grepped `supersed*` across the whole file (18 hits) — no
occurrence depends on generation numbering. Conclusion: this passage still
stands; nothing in it silently depended on the removed counter.

## Checks run against every hunk (summary)

1. Restatement check: hunk 11 vs §9.2's ordering derivation (consistent,
   abbreviated); hunk 12 vs §9.3's Note on F/commit-count (consistent,
   near-identical wording); hunk 13 vs §9.3/§21.7 on commit-count (consistent,
   exhaustively confirmed by the trailer table).
2. Citations: `[R-CNT-08]`, `[R-CNT-26]`, `[R-CNT-14]`, `[R-ENC-13]`,
   `[R-LIF-01]`, `[R-LIF-02]`, `[R-LIF-03]`, `[R-WRT-01]`, §9.2, §9.3, §9.6,
   §9.7, §20.2 — every one opened and checked against the changed text's
   claim; all resolve to where claimed and say what is claimed.
3. Normative-text check: hunk 12's additions sit inside a labelled
   `> **Rationale.**` block, but introduce no new MUST/SHOULD not already
   stated elsewhere (verified sentence by sentence) — the labelling is
   correct and nothing depends on that block alone for force. All other
   hunks are plain prose, not blockquoted.
4. Same-passage contradiction: read all of §20.1–§20.5 and the relevant
   spans of §9 and §21.7 in full; found no contradiction between the
   changed text and its surrounding untouched text.
5. Exhaustive-claim check: "no field counts commits" tested against the
   actual 5-field + reserved + CRC trailer layout — exhaustively true, not
   overclaimed. "The fresh file_id is the whole of that mechanism" tested
   against R-LIF-03's disjunction — supported. Built the minimal-member test
   (a single-commit creation, a trivial one-tile compaction) against each
   universal ("A creator emits...", "A compactor MUST mint...") — no
   counterexample found.
6. Left-open check: dir_offset/dir_length are not restated in §20.3 step 6
   or §20.2's creation description, but this omission predates the change
   (the original text didn't restate them either) and they are established
   via "re-emit the directory" (step 5) / the front-matter placement rules;
   not a new gap introduced by these hunks.
7. Analogy check: the one analogy phrase in my hunks' vicinity — "are owed
   here as they are of a creator" (§20.5, pad/barriers) — is carried forward
   unmodified by hunk 13 (present in both the "-" and "+" text apart from
   the "generation 1" excision) and rests on a literal application of the
   same creation-path steps (§20.2 explicitly obliges a creator to follow
   R-LIF-02's creation path, and §20.5 obliges the compactor to follow the
   *same* path), not a loose analogy — governing verb "are owed" ranges over
   the same set (steps 4–6 of R-LIF-02) for both roles. No other "exactly
   as / the same way / as X is" phrasing appears in my seven hunks' changed
   text.

## Findings considered and rejected

- *Possible finding:* hunk 13's "before any comparison of
  committed_file_length" implies a check ordering R-LIF-03's prose doesn't
  literally specify (it states a disjunction, not a sequence).
  *Rejected:* does not change which bytes a conforming writer emits or a
  conforming reader accepts/rejects — purely a matter of exposition, and the
  substance (file_id alone suffices to reach "different file") is accurate.
  Not byte-level, and not clearly wrong even at the prose level.

- *Possible finding:* hunk 11's "necessarily above the F step 1 established"
  is a less rigorous derivation than §9.2's own Note (which derives the full
  +128 floor).
  *Rejected:* it is a legitimate abbreviated corollary of the same argument,
  not a competing or contradictory claim — it doesn't assert the +128
  figure, so there is nothing for it to get wrong quantitatively, and it
  doesn't need to restate the full derivation to be correct as far as it
  goes.

- *Possible finding:* hunk 13's claim that a compacted file and a
  hundred-times-appended file are "indistinguishable by their trailers
  alone" might overclaim what the old generation counter used to provide.
  *Rejected after checking:* the old counter never distinguished compaction
  from creation (both start at generation 1); what it did provide was a
  commit-count signal (generation 1 vs generation 101), and that specific,
  narrower loss is exactly what the new text names — no overclaim.

- *Possible finding:* hunk 12's dropped "adjacent" language might leave the
  word orphaned elsewhere in the document (a partial sweep).
  *Rejected after grep:* zero remaining occurrences of "adjacent generations"
  or bare "generation 1/one/7" anywhere in the current file; the term is
  fully retired, and §21.7 (untouched by my hunks but touching the same
  material) already reflects the post-removal accounting (three compaction
  obligations, not four).

## Result

No findings in my charter's seven hunks. The removal-and-reorder's specific
failure modes I was asked to hunt for — stale offsets/widths, silent
dependence on the removed field, an asserted-not-derived replacement claim,
an unswept count, or a local contradiction — were checked individually
against each hunk and against the untouched §20.3 step-4 passage the charter
named, and none were found. The two hunks requiring judgment (hunk 12's
adjacency Rationale, hunk 13's compactor identity) both read as honest,
appropriately-scoped repairs: each names precisely what capability was lost
by the field's removal rather than papering over it.
