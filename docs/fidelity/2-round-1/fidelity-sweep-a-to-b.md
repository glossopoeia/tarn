# Completeness sweep, edition A → edition B — working transcript

## Access and method

Read only:
- A: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (4981 lines)
- B: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (4847 lines)

No other file was opened; no directory was listed except my own scratch directory
(`mkdir -p` on it). All commands below ran only `sed`, `grep`, `diff`, `wc` and a
local `python3 -I` script against these two paths.

Working files, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/sweep-a-to-b/`:
- `extract.py` — joins hard-wrapped paragraphs (including `> `-quoted ones, prefix
  stripped) into single lines, so wrap differences don't show as diffs; structural
  lines (headers, list items, table rows, fences, `$$`) pass through unjoined.
- `ranges_A.txt`, `ranges_B.txt` — every header's line range and level, by title.
- `titles_A.txt`, `titles_B.txt` — the title lists, diffed first to find structural
  moves/drops.
- `d_a_<slug>.txt` / `d_b_<slug>.txt` — normalized text of each leaf (`####`)
  subsection under its matched title, for every subsection whose normalized text
  differed between editions (determined by an exact-string comparison across all
  131/130 leaf headers first).
- `na_*.txt` / `nb_*.txt` — normalized text of the Introduction, the preambles of
  level-3 sections that carry direct prose (12, 13, 14, 16, 17, 19, 20, 24, and
  Appendices A–H), compared the same way.

Every zero I report is backed by a control grep that found a phrase I knew was
present (e.g. grepping `R-ENC-15`, `R-CNT-25`, `strictly increasing`, `addressed`
and getting hits proves the search works before I trust a zero elsewhere). Per
the mechanical checker's prior pass, I did not re-diff requirement-ID paragraphs,
register rows, §3.1's term list, tables, or fenced blocks as such — but I did grep
through them as *controls*, to check whether a sentence or Note apparently dropped
from a non-ID location had in fact been relocated into one of those ID paragraphs
or tables elsewhere in the same edition. That relocation-check is why most
candidate findings below resolved to EQUIVALENT rather than LOSS.

Material that was in my context before I began this task (the harness's own
framing text, memory file, CLAUDE.md pointer) is not evidence for this sweep; I
did not use or repeat it as a source of fidelity facts.

## Section-by-section inventory

Verified by exact match after normalization (both editions byte-identical modulo
wrapping): 2.1, 2.2, 2.5, 3.2, 4.1, 4.3, 9.1–9.7, 10.1–10.4, 11.1–11.4, 12.1–12.3,
13.1–13.3 (and §13 preamble), 14.1–14.5 (and §14 preamble), 15.1–15.4, 16.1–16.2
(and §16 preamble), 17.1–17.4 (and §17 preamble), 18.2–18.4, 19.1–19.4 (and §19
preamble), 20.1–20.5 (and §20 preamble), 21.1–21.5, 21.7–21.9, 22.1–22.3, 22.5,
23.1, 23.3, §24 (whole section, no subheadings), Appendix A, C, D, E, F, G, H.
These carry zero completeness findings by construction.

Differed and were read side by side (title, A-location, B-location, verdict):

- Title-block Note ("How to read this document") — A ll.12–23 (before Part 0) →
  content moved into B's §1 Introduction closing paragraph, B ll.17–59. Checked
  every clause: the rubric itself and the offsets-to-give aside land in B's §1;
  the structural/descriptive classification is unchanged in §4.7 in both
  editions; the "test vectors cite identifiers, not prose positions" claim is
  restated with more precision in §24's manifest-entry rule (identical in both
  editions). EQUIVALENT in full — no residue.
- §1 Introduction — A ll.29–94 vs B ll.16–59. Heavily reworded; every substantive
  claim checked against its governing section. Two architectural claims
  (Part I/Part II independence; "Part I alone yields a container reader") do not
  reappear anywhere in B — see swab-01, which treats this together with §3.3's
  loss of the same claim.
- §2.3 Conformance classes — A ll.95–151 (as "2. Conformance" subsection) vs
  B ll.146–203. R-ID paragraphs trimmed; content checked against §21.6, §21.2,
  register rows — EQUIVALENT (migrated, not lost) except swab-05 and swab-06
  (two Note/derived-clause drops with no restatement found).
- §2.4 Outcome classes and owning scope — A ll.296–341 vs B ll.294–332.
  Two real drops: swab-02 (preserve-verbatim/ignore orthogonality sentence) and
  swab-03 (the "Reject ≠ UI" Note).
- §3.1 Terms — A ll.351–413 vs B ll.62–124. Reordered and several entries
  rephrased with more specificity. Checked each rephrasing against its owning
  section (§9.2, §9.3, §11.4, §14, §15) — all EQUIVALENT, the "load-bearing"
  placeholders cashed out into facts already stated identically in both editions'
  bodies.
- §3.3 Container and array model — A ll.435–442, **entirely absent from B**
  (no heading, no body). See swab-01.
- §4.2 Integer types and domains — A ll.455–490 vs B ll.354–386. Rephrased
  (3 exceptions enumerated instead of 2 clauses); content preserved. EQUIVALENT.
- §4.4 Bit numbering — A ll.504–511 vs B ll.400–404. Note dropped ("this rule is
  general; bool-sample-to-bit mapping is §14's"); §14.3 (identical in both)
  already cross-references §4.4 itself, so no ambiguity results. EQUIVALENT.
- §4.5 Checksums — A ll.512–549 vs B ll.405–430. The three-exceptions passage
  that A states here is absent from B's §4.5, but reappears, expanded, in §8.1
  (identical point, more detail) in both editions' already-matching §8.1 bodies.
  EQUIVALENT (relocated to §8.1).
- §4.6 Strings and names — A ll.550–595 vs B ll.431–476. One explicit outcome
  ("...the outcome is ignore-record") compressed to "the same exception"; R-CNT-25
  states the outcome at its own definition in both editions. EQUIVALENT.
- §4.7 Field taxonomy and presentation — A ll.596–630 vs B ll.477–505. Note
  reworded; three sentences dropped (name-duplicate pointer, "every non-obvious
  encoding has a worked example" documentation-convention sentence, "constants
  appear once in Appendix B" convention sentence). First is EQUIVALENT (R-ENC-15
  stated at its own location in both); other two are editorial/meta-documentation
  claims about this document's own apparatus, not format rules — not filed as
  findings (no byte-level effect; not rules A "decides").
- §5.1 Anatomy — A ll.635–697 vs B ll.510–574. Rewording only; every relocated
  clause checked and found restated. EQUIVALENT.
- §5.2 Byte coverage — A ll.698–781 vs B ll.575–647. Heavily restructured into
  more paragraphs; the clause on a structurally-rejected tile-index entry leaving
  the coverage walk complete "for the opposite reason" is dropped from §5.2 but
  is present, identically, in §9.7 in both editions (A l.1539, B confirmed by its
  "SAME" status). EQUIVALENT.
- §6.1 Front signature block — A ll.784–827 vs B ll.650–692. Rewording only
  (sentence-splitting, "e.g." for the dash construction). EQUIVALENT.
- §6.2 Trailer — A ll.828–877 vs B ll.693–743. Rewording only. EQUIVALENT.
- §6.3 Version and flag gates — A ll.878–922 vs B ll.744–786. One sentence on
  rewriters specifically carrying forward ignore-lane bits ("though its output is
  a new file...") is dropped; the general "updater" rule in both editions already
  covers rewriters by definition (updater's tiers are appender and rewriter,
  §2.3/§20.1, identical in both), and §20.5 (identical in both) is the rewriter's
  own governing section. EQUIVALENT.
- §6.4 Remote open accounting — A ll.923–966 vs B ll.787–826. Rewording and
  clause-reordering only, including inside the Note; checked word-for-word.
  EQUIVALENT. (This section anchors the Introduction's "two range requests" claim
  that both editions still state identically here — see note under swab-01's
  rejected candidates.)
- §7.1 Directory region — A ll.969–1006 vs B ll.829–837. An entire paragraph
  (the R-CNT-25 user-metadata-quarantine definition) is absent from §7.1 in B —
  but present, fuller and intact, in §7.3 in B (B ll.943–970). EQUIVALENT
  (relocated from §7.1 to §7.3; downstream cross-references to "§7.1" for this
  content were correspondingly repointed to "§7.3" in §18.1, §22.4, §23.2 — all
  checked and consistent, not independent errors).
- §7.2 Record framing — A ll.1007–1095 vs B ll.838–921. Rewording/sentence-
  splitting only; the "readers not obligated to detect overlap" and multiplicity
  clauses all present, just repunctuated. EQUIVALENT.
- §7.3 Record types of format major 1 — A ll.1096–1120 vs B ll.922–972. Receives
  the relocated §7.1 paragraph (see above); one analogy clause to R-CNT-12's
  treatment dropped, explanatory only. EQUIVALENT.
- §7.4 The layer record — A ll.1121–1232 vs B ll.973–1084. Sentence-splitting
  only. EQUIVALENT.
- §8.1 Coverage map — A ll.1235–1254 vs B ll.1087–1111. B's version is fuller
  than A's (absorbs the §4.5 material, see above). Not a loss in either direction.
- §8.2 Verification obligations and outcomes — A ll.1255–1275 vs B ll.1112–1131.
  Punctuation only. EQUIVALENT.
- §12 preamble (channel declaration) — A ll.1791–1797 vs B ll.1647–1653. "the
  declared order is load-bearing" → "fixes each channel's index"; cashed out
  identically to the §3.1 pattern. EQUIVALENT.
- §18.1 The document — cross-reference renumbering only (§7.1→§7.3), consistent
  with the §7.1→§7.3 relocation above. EQUIVALENT.
- §21.6 Conditions that are not violations — A ll.3834–3887 vs B ll.3690–3743.
  B gains a paragraph (the capability/resource-ground list) that in A sits inside
  §2.3's R-CNF-11 paragraph; migrated, not added de novo. EQUIVALENT.
- §22.4 Content the reader hands onward — cross-reference renumbering only.
  EQUIVALENT.
- §23.2 What a file discloses — cross-reference renumbering only. EQUIVALENT.
- Appendix B — one table cell's cross-reference differs (§7.1 vs §7.3) for the
  user-metadata extent-minimum constant — consistent with, and correctly updated
  for, the §7.1→§7.3 relocation above (A's §7.1 citation was right for A's own
  layout; B's §7.3 citation is right for B's). Not filed: it is a table cell,
  already in the mechanical checker's remit, and it is not an error.

## Note/Example/Rationale census (whole-document control)

- Note blocks: A 57, B 52. All five of the net-missing ones were traced:
  1. title-block Note → relocated into §1 Introduction (EQUIVALENT, see swab-07
     for the one clause not carried over);
  2. §2.3's three-row (F14/F5/F15) illustration of the "reach" test → dropped,
     see swab-06;
  3. §2.4's "Reject ≠ UI" Note → dropped, see swab-03;
  4. §3.3's whole Note → dropped, see swab-01;
  5. §4.4's Note → dropped but EQUIVALENT (§14.3 already self-cross-references
     §4.4 in both editions).
- Example blocks: A 20, B 20 — equal count; sampled several (§14.2, §14.3) and
  found them reworded but figure-for-figure identical. Not exhaustively re-walked
  given the count parity and the sample.
- Rationale blocks: A 13, B 13 — equal count; sampled (§5.2, §9.2, §14.2) and
  found reworded-but-equivalent. Not exhaustively re-walked given count parity
  and the sample.

## Sections reached vs not

Reached and checked at the depth described above: Part 0 (§1–§4 and all
subsections), Part I (§5–§10), Part II (§11–§18), Part III (§19–§23), §24,
Appendices A–H. I did not re-verify §24's and the Appendices' internal
worked-example numbers against each other digit-by-digit beyond the
normalized-identical check (they matched exactly, including Appendix B's one
cross-reference difference noted above) — given exact-match status, further
reading would not add information. I did not hunt the Example/Rationale set
exhaustively past the count-parity control described above; if either edition
dropped one Example while adding an unrelated one elsewhere (preserving the
count), my census would miss it. That is the one coverage gap I flag rather than
silently close.
