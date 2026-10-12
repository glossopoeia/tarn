# Writer comparator — transcript

## Disclosure (mandatory)

- A harness-relayed "user request" ("Go") appeared above the computed brief.
  Per the brief's own instructions this is the launcher's message to the
  orchestrator, carried out before I was spawned; it is not a task for me,
  needs no reconciliation, and does not widen the access rule. Disregarded
  as a task instruction; disclosed in this one clause.
- My runtime context also contained, before I began, unasked: a CLAUDE.md
  pointer to AGENTS.md (not opened, per the access rule), a user MEMORY.md
  index of many TARN-process notes, a git status/log block for branch
  `readable`, a commit/PR attribution-footer instruction, a userEmail
  identification block, and a long list of skills/deferred tools. None of
  this is part of either specification edition and none of it is evidence
  about their content. Disregarded as a source of fact; not repeated beyond
  this clause.
- Files read, exactly: `scratch/cleanroom/editions/a/tarn.md` (edition A,
  4,981 lines), `spec/tarn.md` (edition B, 4,755 lines),
  `fidelity-4/out/transcript-writer-a.md` (178 lines), and
  `fidelity-4/out/transcript-writer-b.md` (694 lines). No other file was
  opened; no directory was listed except creating my own scratch directory
  `fidelity-4/scratch/compare-writer/` (empty when created).
- Commands run: `wc -l`, `grep -n` for section-header sweeps, and `sed -n`
  to print whole paragraph ranges of the two spec files (never truncating a
  hard-wrapped line to a fragment), plus `diff` between extracted
  equal-length excerpts of the same section from both editions. All reads
  were of the four files listed above; local computation only.

## Method

Both transcripts (writer-a, writer-b) answer the same eleven probes (W1–W11)
and record their own findings (writera-01; writerb-01/02/03). For every
probe I opened both editions at the cited sections and read the passage in
full (not just the walker's quoted fragment), to check whether the two
editions actually diverge at that point, independently of whether the two
walkers' *answers* happened to agree.

Sections read in full, both editions, side by side (sed -n range extraction
+ diff where helpful): §2.3 (conformance classes incl. verifier verdicts),
§4.5 (checksums/check vectors), §5.1 (anatomy, incl. both examples), §6.1–
6.4 (front block, trailer, version/flag gates), §7.1–7.3 (directory region,
record framing, record types/registry, metadata quarantine), §9.2 (commit
protocol), §9.4–9.6 (recovery before re-append, concurrency/default read
path, recovery scan), §11.3 (edge padding), §15.1 (tile-index region/entry
layout, incl. the unlabeled blockquote), §15.4 (segments/verification),
§20.1 (writer tiers), §20.3 (append procedure, full, incl. both worked
examples and all three commit-shape figures), §20.4 (re-emission/
preservation, full, incl. the three-row table), §20.5 (rewriting, full,
incl. the compaction figure), §21.1 (register-reading rules), §21.4 (tile-
scope violations register, T1–T26), §21.6 (non-violations table and the
two closing paragraphs), §21.7 (what no check detects), Appendix A (minimal
file, full byte table), Appendix G (reproducible-writer profile, all 12
items).

## Findings from side-by-side reading

**Result: every one of these sections is substantively identical between
edition A and edition B.** Differences are confined to sentence-boundary
placement, list-vs-prose formatting (B sometimes renders the commit-protocol
steps 1–6 as a numbered list where A runs them as one sentence; see §9.2),
word order, and punctuation (colon vs. em-dash, parenthetical vs. clause).
No rule, exception, quantifier, worked figure, table row, byte value, or
requirement-ID citation differs. Two passages are relocated rather than
reworded or dropped, and I checked that the content survives the move
intact:

1. A's §6.3 states the rewriter's ignore-lane-copy-forward rule explicitly,
   in addition to §20.5 stating it; B's §6.3 omits that explicit restatement
   and the rule lives only in §20.5 (quoted identically in both editions:
   "The output trailer MUST copy the input's unknown ignore-lane flag bits
   forward and set no other, in place of the flags = 0 §6.3 requires of a
   file created under this text. [...] `[R-WRT-06]`"). Content preserved,
   stated once instead of twice. EQUIVALENT — does not change probe W5's
   answer, which cites §20.5 in both transcripts.
2. A's §2.3 "Conforming verifier" bullet spells out the *cannot establish*
   grounds in full ("as when the file names a format major version it does
   not implement, when a record carries MUST_UNDERSTAND = 1 with a type it
   does not implement (§21.6), when it cannot execute a codec or filter
   (`[R-COD-11]`), when it declines a layer's or a tile's decode on resource
   grounds [...], or when it declines to decode a user-metadata document
   (`[R-MTA-09]`)"). B's §2.3 abbreviates this to "(§21.6 names the
   grounds)" and B's §21.6 carries a new closing paragraph restating the
   same list verbatim-in-substance ("A verifier is unable to check a
   requirement on a capability or resource ground, and so reports *cannot
   establish* (`[R-CNF-11]`), as when the file names a format major version
   it does not implement, a record carries MUST_UNDERSTAND = 1 with a type
   it does not implement, it cannot execute a codec or filter..."). Content
   preserved, relocated. EQUIVALENT.
3. A's §7.1 carries the "metadata compression exists only at record
   granularity" / quarantine paragraph; B's §7.1 is a two-sentence stub
   (directory region, CRC verification only) and the quarantine paragraph
   reappears, reworded but intact, as the second half of B's §7.3. Content
   preserved, relocated. EQUIVALENT.

No LOSS, no ADDITION, and no byte-level divergence was found anywhere in
the territory read. Every probe's governing sentence(s), as cited by both
walkers, exist in both editions in the form quoted (checked by direct
re-reading, not by trusting either walker's citation).

## Per-probe disposition

**W1–W11, all: EQUIVALENT (texts agree; no REPORTER_ERROR, no byte-level
divergence).** Both walkers' answers to all eleven probes are not merely
*consistent with each other*; they are each drawn from passages that are
word-for-word (or, where reworded, substance-for-substance) identical
across editions:

- W1 (smallest conforming file): §5.1, §6.1, §6.2, §7.1(/§7.3 for the
  relocated quarantine text), §4.5 check vectors, Appendix A's byte table —
  identical. Both walkers independently re-derived CRC-32C and got the same
  Appendix A value; this is a correct cross-check against identical source
  text, not a coincidence of agreement on divergent texts.
- W2 (644-byte index region append): §20.3's worked example — byte-for-byte
  identical quote in both editions (confirmed by direct extraction above).
- W3 (unimplemented MU=1 top-level record): §7.2, §20.3 step 2, §20.4's
  MU=1 row — identical in both editions.
- W4 (drop-only commit, MU=0/PE=0): §20.4's MU=0/PE=0 row — identical.
- W5 (ignore-lane bit through appender/rewrite/creator): §6.3, §20.1,
  §20.5 — identical in substance (see relocation note 1 above); both
  walkers cite §20.5's `[R-WRT-06]` text, which is verbatim-identical.
- W6 (fill-value change on a stored-tile layer): §20.3 step 4 (fixed-
  declaration list, the "what the line gives up" sentence, the conduct-
  rule/[R-CNF-02] passage), §21.4's T4 row, §11.3's edge-padding rule — all
  identical, confirmed by full-text diff of §20.3 and byte-for-byte
  comparison of the T4 register row.
- W7 (crash between directory-durable and trailer-durable): §9.2's full
  commit protocol and crash example, §9.4, §9.5, §9.6 — identical.
- W8 (rewriter carrying an undecodable sample type): §20.5's `[R-WRT-09]`
  paragraph and verification-depth text — identical.
- W9 (PE=0 layer blocked by an MU=1 sub-record): §20.4's layer-drop
  paragraph and MU=1 row, §7.2's `[R-CNT-18]` — identical.
- W10 (appender dropping a carried MU=0/PE=0 record): §20.3 step 2, §20.4's
  MU=0/PE=0 row — identical.
- W11 (implemented unregistered type, definition fixes MU=1/PE=0): §20.4's
  "for an implemented type only the PE bit bites" passage — identical,
  confirmed verbatim in the full-text extraction above.

## Each walk's own findings, checked against the other edition

- **writera-01** (A's OBSERVATION: a fill-only change on a layer with no
  edge padding leaves no file-conformance witness, despite violating
  §20.3 step 4's conduct bar) and **writerb-02** (B's OBSERVATION, same
  substance) are the *same finding*, independently derived from *identical*
  source text (§20.3 step 4, §21.4 T4, §11.3, `[R-CNF-02]` — all confirmed
  byte-for-byte or substance-for-substance identical above). This is not a
  divergence between editions; it is the same true fact about the one
  format both editions describe, found twice because both walkers read it
  correctly. **cmp-writer-01 (EQUIVALENT / cross-walk confirmation, not a
  fidelity issue).**
- **writerb-01** (B's OBSERVATION: a creator that decodes-and-re-emits an
  existing file loses ignore-lane bits an appender/rewriter would keep,
  because the creator/updater tier distinction keys off the output's
  relationship to the input file, not off whether the writer read it) rests
  entirely on §20.1 ("As a creator it undertakes nothing toward its input,
  whatever it read...") and §6.3/§20.5's flags rules. §20.1 is
  word-for-word identical between editions (confirmed above), so this
  finding is **equally available from edition A** — walker A's own W5
  answer reaches the identical conclusion via the identical sentence,
  though walker A did not promote it to a numbered Finding. Not a
  B-specific defect. **cmp-writer-02 (EQUIVALENT; the underlying fact is
  edition-independent, present and correctly derivable from A).**
- **writerb-03** (B's OBSERVATION: §15.1's tile-index region-layout
  blockquote is the document's one *unlabeled* blockquote, hence fully
  normative under `[R-CNF-01]`, and is easy to miss as an aside) rests on
  §15.1's region-layout line. I confirmed by direct extraction above that
  edition A's §15.1 carries the **identical unlabeled blockquote**, in the
  identical position, with the identical "with no padding anywhere inside
  the region" sentence immediately after it. The "one unlabeled blockquote
  in the whole document" property, if true, is therefore equally true of
  edition A, and the risk writerb-03 names (a reader skipping it as a
  surface-level aside) is exactly as present for an implementer working
  from A as from B. Walker A did not surface this as a finding, but that is
  a difference in what each walker chose to report, not a difference in
  what the two texts say. **cmp-writer-03 (EQUIVALENT; B-specific framing
  is not B-specific in fact — A has the identical construct).**

I did not find a fourth class of finding: no defect present in one edition
and absent, narrowed, or widened in the other. Every substantive rule
checked traces to identical or substance-identical text.

## Transcript-reading for forced guesses (charter item 4)

Walker A's own methodology note says it read §1–§10, §15–§17 (scanned),
§19 (scanned), §20–§21 in full, and Appendices A/B/C/G in full, explicitly
*not* reading §11–§14 word-for-word (it used targeted greps/TOC checks
instead) and not §18, §22–24, Appendix D–F/H. Walker B read the entire
document front-to-back in six chunks. Neither transcript records a probe
answer that required re-reading, going elsewhere than the section the
probe names, or hedging/guessing — both walkers reached a single-citation
answer for all eleven probes without flagging indeterminacy. Since every
section I independently checked is identical or substance-identical
between editions, A's narrower reading did not cost it anything on these
probes: the sections A skipped (§11–14 in depth, §18, §22–24) are not the
sections any of W1–W11 or either walker's own findings depend on (I
confirmed this by checking that every citation either walker gave resolves
inside §2–§9, §11.3, §15, §20–21, or an appendix — all sections A did read,
at least in the specific paragraphs cited). No asymmetric difficulty
finding to report.

## What I did not find

No LOSS, no ADDITION, no CONTRADICTION, and no genuine REPORTER_ERROR (a
case where a walker answered wrong from a text that decides the question
correctly) anywhere in the eleven probes or either walk's own findings. The
three items above (cmp-writer-01/02/03) are EQUIVALENT-classed
cross-checks: cases where a walker's own finding, framed as being about
"this edition," turns out on inspection to be equally true of the other
edition because the underlying text is the same.
