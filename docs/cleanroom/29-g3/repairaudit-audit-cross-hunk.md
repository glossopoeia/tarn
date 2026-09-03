# Cross-hunk consistency audit — working transcript

## Access disclosure

Read: spec/tarn.md (full file, 4775 lines; targeted re-reads of lines
2500-2660, 3075-3260, 3540-3610, 3750-3810, 3860-4000).
Read: hunk-01.diff through hunk-06.diff in the case/ directory (all six,
via `cat` in a single Bash loop). Did NOT read full.diff, other hunk files
beyond my six, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, or git history, per the access rule.

**Contamination notice.** Before this task began, my context already
contained project material I did not ask for and could not avoid: a
`CLAUDE.md` pointer, a user-memory index (`MEMORY.md`) listing file names
such as "tarn-lineage-stays-private.md", "TARN working cadence",
"Workflow verifier failures", "Spec edits need propagation checks", "TARN
register is the corpus build list", plus the user's email and the current
date. I did not open any of the named memory files, did not act on any of
it, and treated none of it as evidence about which hunks are defective. It
is disclosed here per the charter's instruction; nothing in my findings
below relies on it.

Grep/search commands run (all local, against spec/tarn.md only):
- `grep -n "R-CNF-13"` → 4 hits (lines 161, 269, 3635, 3909)
- `grep -n "R-COD-06"` → 9 hits (2432, 2602, 2614, 2629, 2647, 3765,
  3769-3774 (T17-T22), 3806 (R4), 3874, 4118)
- `grep -n "R-CNF-07"` → 2 hits (288, 3563, 3894)
- `grep -n "R-MTA-09|R-MTA-10"` → ~15 hits
- `grep -n "live state"` → 15 hits
- `grep -n "strand|as slack|whole layer"` → 9 hits
- `grep -n "interleaved layer|planar layer|its own tiles|planar channel"` →
  ~20 hits
- `sed -n | grep -c "^>"` checks on the hunk-01/02/03/04 landing zones, to
  confirm none of them sit inside a blockquote (all confirmed plain text,
  no leading `>`).

## The six hunks, one-line rule each

1. **hunk-01** (§18.2, normative prose, no `>`): splits a mis-stated single
   ground ("carry no witness") for two carried-over R-COD-06 exceptions
   (undisclosed dictionary use; the buffer-sizing bar) into the two
   distinct grounds §21.7 actually offers — *unwitnessed condition* vs.
   *states no condition a file can exhibit at all*.
2. **hunk-02** (§20.3 step 4, the §14-bar re-typing rule, normative): scopes
   the "stranded as slack" consequence of a barred re-typing to *every tile
   the change reaches*, adding "and for a change reaching every channel[,]
   the whole layer's worth" as the special case that recovers the old,
   broader phrase.
3. **hunk-03** (§21.1, normative): rewrites the register's completeness
   clause's inline restatement of "detectable" from "differs ... in its
   live state" to "is separated, by a check this specification obliges a
   reader or a verifier to perform, from every file that does not."
4. **hunk-04** (§21.7 main text, normative, no `>`): (a) replaces "matching
   quantifiers" with "each quantifier is the other's dual" as the reason
   unwitnessed/detectable are exact negations; (b) narrows "carries a row
   for a condition exactly where it is detectable" to "...where it is a
   detectable file-conformance violation."
5. **hunk-05** (§21.7 Rationale, labeled, non-normative): adds "and its
   list is not offered as closed" and "or an obligation the list omits" to
   the walkthrough's own disclaimer.
6. **hunk-06** (§21.7 Rationale, labeled, non-normative): completes the
   fills-agree/fills-differ split for a planar disk-ordinal permutation by
   adding the case where the layer has *neither* a padding position nor a
   pad bit — unwitnessed regardless of fill agreement.

## Grouping by rule, not by section

**Group A — the unwitnessed/detectable/no-condition-to-exhibit framework**:
hunks 01, 03, 04, 05, 06. All either state, restate, or apply the
unwitnessed/detectable distinction of §21.7 and the "no condition a file
can exhibit" category next to it.

**Group B — the §14 bar (re-typing) and its consequences**: hunk 02 (the
bar's writer-side consequence, in §20.3) and hunk 06 (the bar's
reader/verifier-side witnessing, in the §21.7 Rationale, which explicitly
opens by naming "§20.3 step 4's §14 bar"). Hunk 06 sits in both groups.

## Group A — checked pairwise

**01 vs 03/04 (citation/ground check).** Hunk-01's two grounds:
- "dictionary use the header does not disclose is a writer violation
  nothing in the extent shows — an unwitnessed condition, exactly as
  `[R-COD-06]` has it for a tile (§21.7)". Verified against the tile text
  at lines 2411-2419: "Dictionary use the header does not disclose is not
  detectable by inspection and need not decode to an error: it is a writer
  violation whose consequence is wrong decoded content, the same
  undetectable class as any other writer that emits wrong bytes (§21)."
  Same governing verb ("is a writer violation"), same quantifier (one
  instance: one frame / one tile), same undetectable status. Analogy holds.
- "the bar on sizing a buffer binds a reader rather than the document, and
  so states no condition a file can exhibit at all" — checked against the
  untouched category definition at lines 3917-3923 ("Distinguish an
  unwitnessed condition from a requirement that states no condition a file
  can exhibit... `[R-ENC-06]`'s fixed field widths are not a state a file
  can be in"). The category as *stated* is general ("a requirement that
  states no condition a file can exhibit"); a pure reader-implementation
  bar (nothing about it is a fact about file bytes) is a valid instance of
  that general category even though its reasoning (implementation-only
  requirement) differs from the one worked example given (fixed-width
  parsing). No contradiction found. Cross-checked against §21.5's own
  parallel language (line 3789-3791): "except where a reader or verifier
  declines the decode on the size bound or on the frame's declared window,
  which `[R-MTA-09]` makes that actor's capability and not a fact about
  the file" — independently confirms the same framing for the identical
  buffer/window bound. Consistent.
- Checked "R4 registers neither": R4's instance list (line 3806) was read
  in full; it lists frame magic, skippable frame, second frame, nonzero
  dictionary ID, content-checksum flag, trailing bytes, content-size
  larger/smaller — for both top-level and sub-record extents. No instance
  for undisclosed dictionary use or for a buffer-sizing violation. Claim
  holds.

**03 vs 04 (the definition-and-its-restatement pair the charter flags).**
This is the one candidate that matches the charter's "one definition and
one sentence reporting that definition were edited in the same commit"
description exactly: hunk-03 is §21.1's inline restatement of
"detectable"; hunk-04 touches sentences in §21.7 that talk *about* the
same detectable/unwitnessed pair (though hunk-04 does NOT edit the actual
defining sentences at lines 3886-3891, which are quoted verbatim as
unchanged context in the diff).

Compared word for word:
- §21.1 (hunk-03): "a condition is detectable exactly where some file
  exhibiting it is separated, by a check this specification obliges a
  reader or a verifier to perform, from every file that does not"
- §21.7 (untouched definition, quoted as context in hunk-04's diff): "It
  is **detectable** in the contrary case: where some file exhibiting it is
  separated by such a check from every file that does not."

These match exactly in governing verb ("separated ... from every file
that does not") and in what "such a check" cashes out to. No disagreement.

Then checked the *other* half of the pairing — the register-inclusion
criterion, which both hunk-03's location and hunk-04 state independently:
- §21.1 (untouched sentence immediately preceding hunk-03's edit, line
  3560-3562): "a *detectable* file-conformance violation this
  specification names and the register omits is a defect in this
  document"
- §21.7 (hunk-04's edit): "The register carries a row for a condition
  exactly where it is a **detectable file-conformance violation**"

Both editors landed on the identical phrase "detectable file-conformance
violation" for the register-inclusion criterion. Since both sentences were
edited in this commit and could have silently drifted (per the charter's
warning that "no diff shows it, because both changed"), I checked this
explicitly: they agree, verbatim, on the operative phrase. This looks like
the deliberate target of the pairing, and it passes.

**Quantifier-duality claim (hunk-04, part a).** Worked the logic by hand:
*unwitnessed(C)* = ∀f∈C ∃f'∉C ∀check: ¬Separates(check,f,f'). Negating:
∃f∈C ∀f'∉C ∃check: Separates(check,f,f'). *detectable(C)*, read as "some
file exhibiting it is separated by such a check from every file that does
not," is ambiguous between a single fixed check working for every f'
(∃check∀f', which is *stronger* than ¬unwitnessed and not its exact
equal) and a per-f' check (∀f'∃check, which *is* the exact negation). This
ambiguity is not new — the sentence being interpreted is the untouched
definition, not hunk-04's edit; hunk-04 only replaced "matching
quantifiers" (which would make the two statements identical, not
negations — arguably a *worse* description) with "each quantifier is the
other's dual" (which, under the charitable/needed per-file reading, is
the mathematically correct description of a De Morgan negation). I could
not find text elsewhere that resolves the ambiguity either way, so I am
not filing this as a hunk defect: hunk-04's contribution is a repair in
the more-defensible direction on a pre-existing ambiguity it did not
create and did not worsen. Logged here as a rejected candidate.

**05 and the labeled-block force question.** Hunks 05 and 06 are the two
that land inside the `>` blockquote headed **Rationale.** — confirmed by
direct inspection (`> **Rationale.**` at line 3925) — and are therefore
non-normative under `[R-CNF-01]`. Checked whether anything that *does*
carry force (hunks 01-04, or any other untouched normative passage) now
leans on hunk-05's or hunk-06's content for its own truth:
- §20.3 (hunk-02's location) does not cite §21.7 anywhere in its text
  (checked with a targeted grep restricted to lines 3075-3210: zero hits
  for "21.7", "Rationale", "witnessed").
- The normative §21.7 main text (lines 3868-3923, unedited except
  hunk-04's two clauses) explicitly forecloses any such dependency in the
  *other* direction: "This walk-through illustrates the test and does not
  extend it" (pre-existing) and hunk-05's own addition, "an obligation the
  list omits ... is a defect in this block and not in the register" —
  i.e., the block is deliberately firewalled from the normative
  completeness clause it discusses. §21.1's own text (untouched, lines
  3581-3587) independently confirms the firewall: "neither this
  completeness clause nor the instance arithmetic below reaches ...
  §21.7's test for what no check detects."
- Conclusion: nothing normative depends on the Rationale block for its own
  force. The two labeled-block edits (05, 06) are consistent with staying
  inertly illustrative, and the document says so explicitly, now twice
  reinforced by hunk-05's own addition. This is a check that *passes*,
  not a defect — reported as required by the charter's instruction to
  report the comparison "even where it passes."

## Group B — hunk-02 and hunk-06 (the §14 bar, two sides)

Hunk-02 states the writer-side consequence (a barred re-typing, if
committed anyway, strands "every tile the change reaches, and for a
change reaching every channel[,] the whole layer's worth"). Hunk-06
states the reader/verifier-side witnessing of the *companion* disk-ordinal
bar (a different but adjacent §14-family bar), not of the re-typing bar
itself — the sample-type witnessing discussion sits earlier in the same
Rationale paragraph, unedited by any hunk ("a re-typing that alters no
length and no byte §14 constrains among the cases no witness reaches...").

Checked hunk-02's "for a change reaching every channel[,] the whole
layer's worth" for an overclaim: if "every channel" includes channels
with zero stored tiles in the superseded generation (explicitly permitted
free re-typing per lines 3165-3167), does "the whole layer's worth" still
hold? Yes — a channel with zero stored tiles contributes zero tiles to
strand either way, so "every channel reached" trivially reaches every
*channel that has any stored tile*, which is exactly the layer's full set
of currently-stored tiles. Verified this holds for both the planar case
(worked the (`a` stored, `b` empty) example against the text) and the
interleaved case (line 411: in an interleaved layer channels are "stored
or fill together," so reaching any one channel already reaches every
tile). No overclaim found.

Checked hunk-06's added case ("where it has neither, the permutation is
unwitnessed whether the fills agree or not") for completeness against its
own siblings: the full disjunction is now (same length, fills agree) →
unwitnessed; (same length, fills differ, has padding-position-or-pad-bit)
→ witnessed by T4/T5; (same length, fills differ, has neither) →
unwitnessed [hunk-06's addition]; (different length) → witnessed by
T3/T14, independent of padding/pad-bit existence (T3/T14 are pure length
checks — verified against their register text at lines 3755, 3766). This
is now an exhaustive 2×2 split of the same-length case plus the
different-length case; no sibling left unconstrained.

Cross-checked hunk-06's row citations: T4 (line 3756, padding position not
encoding recorded fill, verifier/certification), T5 (line 3757, pad bit,
verifier/certification), T3 (line 3755, decoded length mismatch,
reader/tile use), T14 (line 3766, codec-1 length mismatch, reader/tile
use) — all four read and all match the claims made about them.

No contradiction found between hunk-02 and hunk-06: they address
different sub-cases of the §14-adjacent bar family (sample-type
reinterpretation's writer-side consequence vs. disk-ordinal permutation's
detectability) and do not restate each other's quantifiers.

## Other checks run and passed without incident

- **Back-reference check (check 8) on hunk-01's insertion.** "The first
  exception holds because a document has no declared size..." (the
  untouched sentence immediately after hunk-01's edit) resolves to "save
  two: what it states against a tile's declared decoded size, and what it
  states about the frame's declared Window_Size" (line 2603-2605), not to
  hunk-01's own "two distinct grounds" a few sentences later, despite both
  using the word "two." Checked the word "exception" for prior occurrences
  in the paragraph: none — the resolution is by content-matching ("no
  declared size" ↔ "declared decoded size"), not by nearest-antecedent
  counting, and this structure (a "two"-labeled aside sitting between the
  "save two" list and "the first exception") is unchanged by the hunk —
  the intervening material was already there in the same shape pre-repair,
  so the hunk did not newly endanger this resolution.
- **Exhaustive-claim check (check 5) on hunk-01's "Two of those."**
  Verified against the full carried-over list (frame magic; no
  skippable/second frame; no dictionary disclosed or not, no nonzero ID;
  no content-checksum flag; the buffer-sizing bar) that exactly two items
  (undisclosed dictionary use, buffer-sizing bar) are absent from R4's
  instance list and the rest are present. Holds.
- **Citation check (check 2), full list:** `[R-COD-06]` (hunk-01, tile
  text at 2405-2432 — verified, matches); `[R-CNF-07]` (hunk-03 and
  hunk-04 — verified against its definition at lines 286-288, matches
  both); `[R-LIF-01]` (hunk-02 — checked it is the freeze rule the
  surrounding unedited text already cites this way; consistent);
  `[R-ERR-01]` (untouched, adjacent to hunk-04/05 boundary — not itself
  edited, not re-verified in depth as it is outside the hunks).
