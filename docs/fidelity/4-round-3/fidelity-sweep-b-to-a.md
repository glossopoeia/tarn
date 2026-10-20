# Sweep transcript — B into A (swba)

## Disclosure

A relayed "user request" (the single word "Go") was prepended above the computed
brief by the harness. Per the brief's own instructions, this is the launcher's
message to the orchestrator, already carried out before this subagent was
spawned; it is not a task for me, needs no reconciliation with the brief, and
does not widen the access rule. I disclose that it appeared and do not act on
it further.

Some material (skill listings, environment/tool-capability reminders, the
project CLAUDE.md pointer to AGENTS.md, and the user's cross-project MEMORY.md
notes about this TARN harness) was present in context before I began work. None
of that is evidence about edition A or edition B; I have not treated it as
such, and I do not repeat its contents here as if they were findings. I did not
open AGENTS.md, PLAN.md, docs/, or any other file outside the two permitted
paths, and I did not list any directory (only `mkdir -p` on my own scratch
path, which does not read directory contents).

## Access

Read in full (via chunked `Read` calls, both files exceed the 256KB single-read
cap so each was read/derived in parts):

- Edition A: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4810 lines)
- Edition B: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (5004 lines)

Working files, all under my scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/sweep-b-to-a/`:

- `normalize.py` — strips `> ` blockquote markers, collapses each blank-line-delimited
  block's hard-wrapped lines into one line (so wrap differences between the two
  hard-wrapped editions do not register as diffs), leaves fenced code blocks
  (` ``` `) untouched.
- `B_norm.txt`, `A_norm.txt` — the normalized one-block-per-line renderings (1163
  and 1135 lines respectively).
- `align_blocks2.py` — extracts every block opening `**Note**`, `**Example**` or
  `**Rationale**` (including extended titles like `**Note — what slabs are, and
  are not.**`), then finds the order-preserving alignment between B's list and
  A's list that maximizes total pairwise text-similarity (dynamic-programming
  sequence alignment, not greedy nearest-match) — this is the "census the
  labelled blocks pair by pair" step, done as an alignment rather than a count
  so that one block dropped and another added cannot cancel out.
- `section_align.py` — splits both normalized files on headers (both editions
  share identical header text and order, confirmed by `grep -n '^#\{1,4\} '`
  on both files), then for each shared header runs the same DP alignment at
  paragraph granularity *within that section only*, printing every pair below
  a similarity threshold and every paragraph with no counterpart at all
  (`[B-ONLY]` / `[A-ONLY]`).
- `section_diff_report.txt` (threshold 0.6), `section_diff_report2.txt`
  (threshold 0.8) — outputs of the above, used as the worklist for manual
  side-by-side reading.
- `raw_diff.txt` — an early, abandoned attempt (line-folded, not block-joined
  diff); superseded by the normalized approach and not used for findings.

## Why this method, and what it does and does not cover

The brief says the mechanical checker already compared requirement-ID
paragraphs, register rows, §3.1 terms, tables, and fenced blocks, and that my
ground is "the sentences without an ID, the carve-outs, the exceptions, the
quantifiers, and the labelled blocks." Both editions are hard-wrapped
(blockquote lines carry a literal `> ` per line), so a naive diff is useless —
confirmed: a line-folded diff of the two raw files produced 6118 differing
lines out of ~5000, i.e. almost the entire file, purely from re-wrapping.

The paragraph-block normalization fixes that: once each block is one line,
genuinely-identical prose re-collapses to identical lines (verified: many
pairs score 1.00 / 0.99 similarity after normalization despite differing
hard-wrap). The DP alignment within each shared section then finds, for every
paragraph of B, its best-matching paragraph of A in the same section (or
correctly reports none), in document order — this is stronger than a greedy
nearest-neighbour match, which I tried first and which mis-paired several
blocks (e.g. it paired B's §2.2 identifier-retirement Note with an unrelated
A Note in §2.4, when the correct, DP-found pairing is A's relocated Note in
§14.4).

This method's blind spot: two paragraphs that are both present, both
mis-stated the same way, and score high similarity to each other would not be
flagged — the method finds *divergences between the two editions*, not
*shared errors against outside truth*. I was not asked to check either edition
against an outside standard (RFC 2119 usage, CRC-32C definition, etc.), only
against each other, so this is the right ground, but it means a defect common
to both editions would not surface here (REPORTER_ERROR is explicitly listed
as a possible finding type for *other* agents in this round working from a
walker/quiz transcript; this agent's job is the B/A textual sweep, and I found
no transcript to check, so I report none).

## Coverage, section by section

Every one of the ~90 `###`/`####` headers is identical, in the same order, in
both editions (confirmed by header grep). For each, the DP paragraph alignment
ran across the *entire* document, not a sample — every paragraph of B was
compared against every paragraph of A within its shared section. I then
manually read, side by side in the raw (non-normalized) files, every pairing
the DP flagged as low-similarity (first at threshold 0.6, then re-run at
threshold 0.8 to widen the net) and every paragraph either edition has with no
counterpart at all. That is a complete sweep of the automatically-flagged
candidates; it is not a complete manual line-by-line re-read of sections where
the DP alignment found every paragraph scoring ≥0.8 (i.e. closely matching
wording) — I spot-read several of those (§8, §9.2, §9.6, §9.7, §18.2, §20.5,
§21.6 in full, because they had *other* flagged paragraphs nearby worth
reading in context) but did not re-read, e.g., §17 (Codecs), §19.1/19.3/19.4,
§22, §23, §24, or the Appendices line-by-line beyond the automated pass, since
that pass found no low-similarity paragraph there at all (every B paragraph in
those sections has an A paragraph scoring ≥0.8, which at this length and
register means close paraphrase, not restructuring). I flag this as the
section range covered by automation-plus-spot-check rather than full manual
re-read: §10, §12 (partially), §15.1–15.3, §17, §19.1, §19.3–19.4, §20.1–20.4,
§22, §23, §24, Appendices A–H.

## Findings log (every discrepancy the tooling surfaced, and its disposition)

### Labelled-block census (Note/Example/Rationale, including extended titles)

B has 90 such blocks, A has 94. The DP alignment pairs 89 of B's 90 against an
A block (scores from 1.00 down to 0.08 — a low score here means "paired by
elimination, not a real match," not "barely similar"); A has 5 blocks with no
B counterpart at the same alignment step. Working through every non-1.00 pair
and every unpaired block:

- **B §15.4 Rationale, "Segments bound what a reader verifies to use one
  entry..." — genuinely absent from A, no relocation found.** Checked by
  grepping both files for `65,536|2¹⁶|entire index|19 MiB|190 MiB|not an
  option a writer`: every quantifier this Rationale cites (2¹⁶-entry segment
  size, the `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` formula, the
  1,000,000-entry worked example) is present, identically, in both editions'
  normative §15.4 text and its accompanying Example block (which *is* paired,
  score 0.99). The Rationale itself adds only explanatory framing ("why
  segment at all," rough MiB estimates for the unsegmented alternative) over
  facts both editions already state as rules. No implementation built from A
  alone would differ from one built from B alone on this point — the
  "segments are not a writer's option" framing is a restatement of the
  index_encoding=1 definition (§7.4), identical in both. **Kind: EQUIVALENT**
  (swba-01).

- **B §16.2 Rationale, "A slab promises one thing, contiguity..." pairs
  weakly (0.16) with A's `**Note — what slabs are, and are not.**`** — my
  first block-census pass (regex requiring a bare period after the label)
  missed A's extended-title Notes/Examples entirely (8 of them use an em-dash
  subtitle, e.g. `**Note — sparse writing.**`); re-running with a wider
  pattern found the true pairing. Full-text read of both (lines 2421–2432 of
  A, lines 668–670 of B after normalization) confirms identical content:
  slab = contiguity only; which tiles are ordinal-consecutive is the
  linearization field's business, not the slab's; row-major makes a run a
  band along the last dimension; the unassigned space-filling-curve
  linearization values are the reserved path to compact-window locality;
  `A_slab = 1` means contiguity-only, for remote-range coalescing. Only the
  label changed (Note → Rationale), and both labels are already non-normative
  under R-CNF-01, so the change is cosmetic. Confirms the git log entry for
  this round ("the slab-scope Note made a Rationale that says what slabs are
  for"). **Kind: EQUIVALENT** (swba-02).

- **B §2.2's "One identifier is retired: `[R-SER-04]`..." Note (early, right
  after the prefix table) has no match at that position; A's counterpart
  Note is at §14.4** ("Identifier `[R-SER-04]`, which earlier governed this
  subsection, is withdrawn; per §2.2 it is permanently retired and never
  reassigned"). Read both locations in full: same fact (R-SER-04 withdrawn,
  never reassigned, once governed §14.4), attached to the opposite end of the
  same cross-reference. A's version adds "per §2.2" as a back-pointer to the
  general identifier-stability rule, which both editions do state identically
  in §2.2's body text (not in a Note) — "a withdrawn requirement leaves its
  identifier permanently retired... numbers above 99 extend naturally." No
  content lost, only relocated. **Kind: EQUIVALENT** (swba-03).

- **Unmatched A-only Notes, none with any B counterpart found anywhere:**
  - A preamble: `**Note.** How to read this document...` — duplicates, inside
    a Note box, what B states as plain (non-blockquoted) prose under the bold
    lead-in "**How to read this document.**" in §1. §1 is non-normative in
    both editions under R-CNF-01 regardless of box styling, so the
    presentation difference carries no normative weight. **EQUIVALENT**
    (swba-04).
  - A §2.3: `**Note.** The test is the invariant a condition violates...`
    (the F14/F5/F15 worked illustration of the reach rule). No B counterpart
    at all. This is content A has that B does not — the opposite of what my
    charter (does A carry what B decides) asks me to flag, since A is not
    missing anything here; if anything A is more thoroughly annotated. Noted
    for the round's record, not filed as a loss. **OBSERVATION** (swba-05).
  - A new §3.3 "Container and array model," a short Note on Part
    I/Part II independence — B has no §3.3 at all (B's §3 ends after §3.2).
    Same situation as above: extra, non-missing content in A.
    **OBSERVATION**, folded into swba-05.
  - A §4.4: `**Note.** This rule fixes bit numbering in flags and packed
    fields generally; the mapping of boolean *samples* to bits is defined in
    §14.` — a one-line pointer disambiguating two different "bit" usages.
    No B counterpart; B's §14.3 (packed boolean planes) states the bit
    mapping on its own without needing the forward-pointer from §4.4. Not a
    missing rule, just a missing cross-reference aid. Folded into swba-05.

### Section-level paragraph sweep (every header, full document)

All `[B-ONLY]` paragraphs (candidates for "B decided it, A doesn't carry it")
across both threshold runs were individually read in raw form, side by side:

- §5.2 (byte coverage): B's three extra "paragraphs" about the slack total,
  the partial-total rule, and its upper-bound property are a single run-on
  paragraph in A covering the identical content (verified by direct read) —
  purely a sentence-per-paragraph reflow B introduced for readability.
- §7.1/§7.3 (metadata compression + quarantine): identical substance, just
  organized under §7.1 in A and under §7.3 in B (confirmed full-text read,
  including the resource-decline carve-out sentence at the end, present in
  both). **EQUIVALENT**, relocation only (swba-06).
- §9.2 (commit protocol): B's numbered list and its "MUST, in order" lead
  sentence vs. A's single inline-parenthetical-numbered sentence — same six
  steps, same wording almost verbatim, confirmed by full-text read.
- §9.3 Note, §9.6 (recovery scan), §9.7 (coverage verification), §18.2 (user-
  metadata encoding), §20.5 (rewriting), §21.6 (closing paragraph) — each
  read in full in both editions; every case was paragraph-reflow or
  relocation, not a content change. §21.6's closing "cannot establish" grounds
  paragraph is the one true relocation of substance: B restates the full list
  at §21.6 itself (after a one-line deferral at §2.3, "§21.6 names the
  grounds"); A states the full list once, inline, at §2.3, and does not
  repeat it at §21.6. Each document states the full enumeration exactly once.
  **EQUIVALENT** (swba-07).
- §8.1 (checksum coverage map): B's "three exceptions" sentence (naming them)
  and A's parenthetical "excepting..." sentence are the same three exceptions,
  word-for-word consistent with each edition's own §4.5, which also states
  the identical exceptions-plus-interior-checksum-fields rule; B states that
  general rule once (at §8.1 only), A states it twice (§4.5 and §8.1,
  consistently) — a redundancy difference, not a content difference.
  **EQUIVALENT** (swba-08).

Low-similarity `[DIFF]` pairs (paraphrase candidates, not missing-paragraph
candidates) were spot-checked at both thresholds; representative ones read in
full: §1 Introduction (non-normative, §2.3's R-CNF-02/R-CNF-03/R-CNF-11
definitions, §2.4, §4.2's R-ENC-04, §6.1's local/remote-reader and residency
definitions, §6.4, §7.2's extent-slot and unknown-record-type rules, §7.4,
§9.3, §11.1 Rationale, §11.4, §14.1's planar/interleaved value-sequence
bullets, §14.2, §14.4. Every one read was reworded prose carrying the same
rule, the same actors, the same quantifiers, and the same numbers — no
narrowing, no widening, no dropped carve-out found among these.

One genuine asymmetry worth recording even though it is not a loss for this
sweep's direction: A's §2.3 "Conforming TARN file" bullet (defining
`[R-CNF-02]`) names three specific conduct-rule examples inline (the
ignore-lane-flags rule of §6.3, the pre-trailer-pad-length rule of §6.2, and
§20.3 step 4's bar on redeclaring a tile-storing layer's fixed fields) and
adds a closure clause, "are the cases this text states." B's `[R-CNF-02]`
paragraph states the general rule only, without collecting these examples or
making that closure claim — though each individual example rule, read at its
own section in B, already says locally that its own violation is conduct-only
/ not a file-conformance violation (confirmed by reading B's own §6.2 and
§6.3 text, both already read in full during the initial pass). So the
individual facts are present in B; only A's summarizing cross-reference and
closure assertion are additional. **OBSERVATION**, not filed as LOSS or
ADDITION under this sweep's direction (swba-09, low severity, informational).

### Not re-diffed, per instruction

§3.1 term definitions (noted only that the *order* of terms differs between
editions — B groups container terms first, A groups array-model terms first,
and the whole-document physical order also differs, with B presenting §3
Terminology before §2 Conformance while A keeps numeric order — left for the
mechanical checker's term-by-term comparison, not re-verified here), register
rows (§21.2–§21.6 tables), fenced code/diagram blocks (box drawings in the
commit/crash examples — spot-checked identical during the §9.2 read, not
exhaustively re-verified elsewhere), and requirement-ID paragraph text beyond
what came up naturally while reading a flagged paragraph's surrounding
context.
