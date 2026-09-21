# Cross-hunk consistency audit — working transcript

## Disclosure

**Context I did not ask for.** Before this task began, my session context
contained a project CLAUDE.md pointer to AGENTS.md (not read, per the access
rule) and a user auto-memory file (MEMORY.md) with ~16 entries whose titles
strongly resemble prior findings/answers about this exact TARN cleanroom
project (e.g. "TARN harness spec path", "TARN repair prose vs rules", "TARN
closed-list exceptions compose", "TARN ADR status change gates quotes"). I did
not open any of the linked memory note files, did not use their titles to
steer my search, and did not treat any of it as evidence about the
specification. I disregarded it entirely, as instructed, and am naming its
presence here rather than repeating its contents. I also received standard
session boilerplate (git status, environment block, skill lists) which is
likewise not part of the specification and was disregarded.

**Access performed.** I read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (full
  document, via multiple `Read` calls covering the whole file — front matter,
  §1–§10, §11.1, §14.3–§14.4, §15.1–§15.2, §19, §20 in full, §21 (register rows
  I grepped and read in context), §23.1, Appendix C, Appendix D excerpt,
  Appendix G, Appendix H).
- All 26 `hunk-01.diff` through `hunk-26.diff` files in
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-audit2/case/`.
  I located these by constructing the path from the documented naming
  pattern (`hunk-NN.diff`, NN = 01..26) and testing existence with `[ -f ... ]`
  in a loop — I did not run `ls` on the directory itself, so I did not "list"
  it. I did not read `full.diff` and did not read any other auditor's files
  (I only ever named my own 26 paths).

**Tools run.** `grep -n` / `python3` regex scans against
`spec/tarn.md` only (no other file read for computation), to locate section
headings, register rows, and to run whitespace-normalized phrase searches
(the document is hard-wrapped, so I normalized `\s+` to a single space before
substring search, and ran control searches — e.g. for "layer's tiles and
index region" I confirmed 2 hits and inspected both, rather than trusting a
naive line-grep that would have missed the wrapped instance). No file outside
`spec/tarn.md` was used as search input.

**Scratch files.** None written — all work was done via direct reads/greps
and reasoning in this transcript; no intermediate script or data file was
needed for the findings below.

**Path check.** All 26 hunk files and the spec file were exactly where the
brief said. No discrepancy to report.

---

## What these 26 hunks are, grouped by rule (not by section)

Working from the hunk file headers/diffs themselves (not from any commit
history, which I was not allowed to read):

**Group A — the drop and what goes with it** (the erratum's forced
decision that a dropped layer's sub-records go with it, and an
unimplemented MU=1 sub-record blocks the drop):
hunks 6, 7(partially — the "MU=1 carries further references" sentence is
adjacent), 13, 14, 15, 17, 19, 21, 25, 26.

**Group B — the record flags (MU/PE) and what each combination means**:
hunks 6, 8, 14, 15 (the three-row table itself).

**Group C — the writer classes/tiers and what each owes (rewriter vs.
creator; updater = appender ∪ rewriter)**:
hunks 1, 2, 4, 10, 11, 16, 17 (opening), 23 (indirectly, "a rewriter" scope),
24, 25, 26.

**Group D — step 4's bar and its "entries new to this generation"
parenthetical**:
hunks 12, 13.

**Group E — the rename's leftovers ("compaction" → "a rewrite" where the
claim is really general)**:
hunks 9, 21, 24.

**Group F — identifier spaces / citations and the remote-open accounting**:
hunks 5, 18, 22.

**Group G — pure wording/citation repairs checked against the rule they
restate**: hunks 3 (§3.3 Note), 20 (§20.5 Example), 23 (Appendix G item 5).

---

## Per-hunk notes (abbreviated; full 8-check pass run on every hunk, only
non-trivial results kept here — see "Rejected candidates" for the rest)

### Group A/B core: hunks 6, 14, 15, 17, 26 (the drop-carries-sub-records rule)

Rule adopted: dropping a layer record under §20.4's PE=0 licence takes the
whole layer — its tile-index region, its stored tiles, **and its
sub-records' extents, whatever their PE bits** — with it as slack in one
commit, UNLESS the layer carries a sub-record of an unimplemented type with
MU=1, in which case the entire drop (not just that sub-record) is blocked.

Checked word-for-word across the five sites that state it:
- §7.2 Note (hunk 6): "An updater that does not implement an MU = 1 record's
  type never drops the record, alone or with the scope it governs (§20.4)."
- §20.4 table, MU=1 row (hunk 15): "At layer scope an unknown critical record
  blocks modification of that layer, **its drop included**..."
- §20.4 running text (hunk 15): "the drop takes the layer whole: ... so a
  dropped layer's sub-records and their extents go with it whatever their PE
  bits. One sub-record blocks the drop, a sub-record of a type the updater
  does not implement with MU = 1..."
- §20.5 (hunk 17): "a record dropped, a layer with **its sub-records**, its
  index region and stored tiles among them, is not in the output..."
- Appendix H (hunk 26): "drops a layer record only under §20.4's PE = 0
  licence, its sub-records with it..." and "never modifies **or drops** a
  scope governed by an unknown critical record..."

All five agree, word for word and quantifier for quantifier ("whatever their
PE bits" / "its sub-records" / "its drop included" / "or drops"). CITATION
check: §20.4's MU=1 row citation to `[R-CNT-18]` (layer-scope blocking) and
`[R-CNT-15]` (file-scope reject) both check out against those requirements'
own text. FORCE check: §20.4's table is a plain (non-blockquote) markdown
table in running prose — normative, not a Note/Example — so the repair lands
in force-carrying text; the §7.2 restatement is a labeled Note but is not the
*only* place the rule is stated (§20.4's table is the authority it cites), so
it is a legitimate summary, not a force failure.

**This is the group where I found the two real defects below — the sweep
stopped one restatement short in each of two places the rule ranges over.**

### FINDING: §20.3's "three shapes" Example, shape (c) — not swept (UNSWEPT_RESTATEMENT)

Location: line 3443–3447, inside the block `> **Example — the three shapes a
commit takes.**` (started line 3409), sub-item **(c)**. No hunk touches this
line range (the nearest hunk, #13, lands at 3293–3301, forty-plus lines
earlier in the same subsection but a different paragraph).

Quoted text (unchanged by any of the 26 hunks):

> "**(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or dropping a layer or another PE = 0 record where
> §20.4 licenses the drop, any extent it owned, **a dropped layer's tiles
> and index region included**, becoming slack, a run the figure below does
> not draw."

Contradicting quotation (the corrected, authoritative statement, §20.4,
hunk 15): "the drop takes the layer whole: a sub-record's flags govern it
within a layer the updater keeps, so **a dropped layer's sub-records and
their extents go with it whatever their PE bits**." And §20.4's very next
sentence: "Dropping a layer by commit strands its stored tiles, **its
tile-index region and its sub-records' extents** as slack."

I ran a normalized-whitespace search for "layer's tiles and index region"
(control: I first confirmed the phrase can appear unwrapped by finding it at
all) and got exactly 2 hits: this one, and an unrelated one in Appendix G
item 3 about emission order. I also searched "strands its stored tiles" (1
hit — the corrected §20.4 sentence, which *does* include "and its
sub-records' extents"). This confirms the shape-(c) Example is the one site
that still lists only "tiles and index region," omitting sub-records, while
the sibling sentence in §20.4 that states the same operation was updated to
include them.

Both texts speak about the same generation (the state right after a commit
drops a layer) and the same actor (the commit/updater), so this is not a
tense mismatch — it is a plain enumeration left one item short after its
sibling enumeration was widened.

Byte-level: **No.** The block is explicitly headed `> **Example**`, which
`[R-CNF-01]` exempts from normative force; the authoritative rule is §20.4's
un-blockquoted table and running text, which *does* say the right thing. No
conforming implementation's bytes turn on what this Example enumerates. But
it is a real defect: an implementer reading only the illustrative "three
shapes" figure — which is exactly the passage a reader skims for a quick
mental model — comes away believing a layer's sub-record extents are *not*
stranded by a layer drop, which is false under the corrected §20.4 rule.

Repair: append ", its sub-records' extents among them" (or identical
wording to §20.4's "its sub-records' extents") to the shape-(c) sentence, so
it reads "...any extent it owned, a dropped layer's tiles, index region and
sub-records' extents included, becoming slack..."

### FINDING: §23.1 (Privacy) — "strands every tile it stored" not swept (UNSWEPT_RESTATEMENT)

Location: line 4369 (§23.1, "Deletion is not erasure"). This paragraph
carries `[R-PRV-01]`'s tag at its end and is normative running prose, not a
Note/Example. No hunk touches this sentence — hunk 21 touches a *different*
sentence eight lines later in the same subsection (line 4383, "Compaction
(§20.5) is the only operation..." → "A rewrite (§20.5) is..."), which is
part of the following paragraph carrying `[R-PRV-02]`, not this one.

Quoted text (unchanged):

> "...editing a user-metadata document appends a new extent and strands the
> old one (§20.3 places this with shape (b)), which is the case most likely
> to strand content a caller believes it deleted, and **a commit that drops
> a layer (§20.4) strands every tile it stored.**"

Contradicting quotation: same §20.4 sentence as above — "Dropping a layer
by commit strands its stored tiles, **its tile-index region and its
sub-records' extents** as slack."

This is the section whose entire subject is *what remains recoverable after
a commit that a caller might believe erased something* — a user-metadata
sub-record attached to a dropped layer (which can carry an arbitrary JSON
document, per §18) is exactly the kind of content a privacy section exists
to warn about, and this sentence's enumeration omits it (and omits the
tile-index region too, though that gap predates this round's repairs — the
tile-index-region omission already existed before hunk 15, so I am not
crediting it to this round's defect count, only noting it as context; the
sub-records omission is new relative to the corrected rule these hunks
establish).

Byte-level: **No**, for the same reason as the shape-(c) finding, and also
because the paragraph explicitly disclaims exhaustiveness ("the list of
operations above is not offered as closed") and the general closing clause
("the bytes a commit makes unreachable always leave the live state whole")
already covers the sub-record case in principle. `[R-PRV-01]`'s actual MUST
NOT (misrepresenting a commit as erasure) does not hinge on this specific
list being complete. Still worth flagging as a restatement the repair should
have swept, precisely because this is the privacy section and the omission
concerns what "remains" — exactly the phrase the brief calls out.

Repair: extend the clause to "...a commit that drops a layer (§20.4)
strands every tile it stored, its tile-index region, and its sub-records'
extents," matching §20.4's own list.

### Group C (rewriter/creator two positions) — checked, no defect found

Checked hunk 11's R-WRT-01 rewrite ("A writer of a new file from an existing
one takes one of two positions...") word for word against:
- §20.1's tier definitions (hunk 10: creator/appender/rewriter) — no
  conflict; a from-scratch creator with no existing input is simply outside
  the "writer of a new file from an existing one" sentence's scope and
  remains a plain creator via §20.1's own (unconditional) tier definition.
- §2.3's Conforming updater (hunk 2: "modifies an existing file, or writes a
  new one that preserves it (§20.1)") — "preserves it" uses the same
  technical sense R-WRT-01 defines (preservation = following §20.4's table +
  §6.3's ignore-lane copy-forward + §20.5, which itself licenses drops and
  re-creates as legitimate exercises of preservation, not violations of it).
  Consistent.
- §6.2's trailer flags cell (untouched, line 838: "carried forward
  unchanged by an updater, appender or rewriter alike") — consistent with
  the two-tier updater class.
- `[R-CNF-05]`, `[R-CNF-06]`, `[R-CNF-11]` — all cited correctly (verified
  each requirement's own text says what the citing sentence claims).
- `[R-CNT-08]` (hunk 4, "of its input file" replacing "the file it
  modifies") — this generalization is *necessary* for the two-position
  framework: "the file it modifies" does not describe what a rewriter does
  (a rewriter does not modify a file, it creates a new one from an input),
  so narrowing/renaming to "its input file" is required for the sentence to
  correctly bind both appender and rewriter. Confirmed against §20.1's own
  "the appender's commit extends its input... the rewriter's output is a new
  file" (input is the general term for both tiers already, so "input file"
  is not a new coinage).
- §20.2 (Creation) and §20.5 (Rewriting) opening — both consistent with the
  "creator undertakes nothing / rewriter undertakes to preserve" framing.
- Appendix G items 2 and 8, Appendix H's writer/updater/rewriter entries
  (hunks 23, 24, 26) — checked; see Group E notes below. All consistent.

ANAPHOR check on hunk 2's insertion: "A tool that modifies an existing file,
or writes a new one that preserves **it** (§20.1), without necessarily
understanding all of **its** content." The insertion adds "or writes a new
one that preserves it" before the existing "without necessarily
understanding all of its content." I checked whether the second "its" now
has a new nearer candidate antecedent ("a new one") competing with the
original ("an existing file"). Grammatically the qualifying clause "without
necessarily understanding all of its content" reads as modifying the whole
disjunction (applies to a tool doing (a) or (b)), and the content in
question is the *input's* content in both readings (for (a) it's the file
being modified; for (b) it's "it" = the existing file being preserved) — so
both a modifying tool and a preserving tool "not necessarily understanding"
the content is the *existing file's* content either way. I judged this not
ambiguous enough to file as a finding (see rejected candidates).

### Group D (step 4's parenthetical) — checked, no defect found

Hunk 12 adds "(every entry of a layer this commit adds or re-declares, and
...)" to the "entries new to this generation" parenthetical. Checked against:
the governing sentence's own scope ("Every layer whose stored-tile set or
index content this commit changes has its tile-index region re-emitted in
full..." — so the parenthetical only ever fires inside that already-scoped
branch); against shape (a) ("A new layer" — nothing existing rewritten,
matches "adds"); against shape (b)/(c)'s "a re-declaration of an empty layer
that changes its index content...with no tile written" and "A re-declaration
that leaves the index content unchanged is shape (c) too" (no index
re-emission at all in that case, so the parenthetical correctly never fires
there); and against the drop (a layer dropped-and-replaced-under-the-same-
name in one commit is covered by "adds," consistent with §20.3's bar
paragraph two pages earlier: "a commit MAY drop the layer (§20.4) and add a
new one under its name"). Consistent throughout.

### Group E ("compaction" → "a rewrite") — checked, all three generalizations are correct fixes, not new errors

- Hunk 9 (§9.3 Note): "Compaction (§20.5) is the continuation from there" →
  "A rewrite (§20.5) is the continuation from there." Correct: what actually
  restarts F is minting a fresh file_id, which *any* rewrite does
  (`[R-WRT-06]`), not only compaction.
- Hunk 21 (§23.1): "Compaction (§20.5) is the only operation that removes
  slack" → "A rewrite (§20.5) is the only operation that removes slack."
  Correct, and it now *matches* §20.5's own unedited Example text a few
  hundred lines later ("A rewrite is the only operation that reclaims
  slack..." — this phrase was already "rewrite," not "compaction," before
  this round, so hunk 21 removes a pre-existing inconsistency rather than
  creating one). Confirmed: every rewrite's output is defined to carry "no
  slack" (§20.5 opening sentence), so *any* rewrite reclaims all pre-existing
  slack, not only compaction specifically — "compaction" was the too-narrow
  term.
- Hunk 24 (Appendix G item 8): "A compaction's output is therefore
  reproducible only modulo its trailer and the records §20.4 lets it drop"
  → "A rewriter's output is therefore reproducible..." I checked this one
  hardest, because it looked backwards at first (item 8 is discussing what's
  *not* pinned for byte-identity). But compaction is *defined* (§20.5
  opening) as "carr[ying] every structure forward and chang[ing] nothing but
  placement" — i.e. compaction never drops anything. So the modulo-drop
  qualifier ("the records §20.4 lets it drop") cannot coherently describe
  compaction's output at all; it only makes sense for a general rewriter
  (which may drop). The original "compaction" was the actual defect here
  (a scope mismatch pre-dating this round), and hunk 24's generalization to
  "rewriter" is the correct fix, consistent with the rest of item 8's
  paragraph, which already talks about "a rewriter" throughout.

None of these three is a new defect; all are correct, and I checked each
against its own paragraph's other sentences per the byte-level test's
"read the governing clause above" instruction.

### Group F (identifier spaces / remote open) — checked

- Hunk 22 (Appendix C): "**Index encodings** (§15.1)" → "(§7.4)". Verified:
  §10.2's table (line 1597) already cites "(§7.4)" for the index-encoding
  space, and §7.4's own layer-record table (line 1141) is where the
  index_encoding field and its value-space (1 assigned; 2–0x7F reserved;
  ≥0x80 experimental) are actually declared. §15.1 only describes the
  *region layout* under index_encoding 1, and even cross-references back to
  §7.4 itself for "the only encoding this format major version defines,
  §7.4." So the fix is correct, not a new error, and it resolves a
  pre-existing mismatch between Appendix C and §10.2's own citation.
- Hunk 18 (§20.5): the only change is an em-dash → colon after "reserved-
  range violations." I checked the enclosing sentence: it is one long
  em-dash-bounded aside ("Where the output carries a feature... —
  ... (L31, L33, L34, L36, L43, L45, R1) — the output's version_minor
  SHOULD..."), and the *original* text had a second, inner em-dash right
  after "violations," nesting one dash pair inside another — exactly the
  NESTED_DASH pattern the maintainer has banned. The hunk's colon correctly
  removes the nesting without changing meaning. I verified no residual
  nested pair remains in the corrected sentence. This is a fix, not a
  residual defect, so I am not filing it as a finding — but I record it
  because it demonstrates the check found real (already-resolved) instances
  of the banned pattern elsewhere in this document's editing history.
  I also verified the L31/L33/L34/L36/L43/L45/R1 + F36/L25 citation list:
  §10.2 tabulates 8 identifier spaces total; record type is covered by
  F36/L25, and the "other seven" are exactly the seven rows listed (index
  encoding→L31, linearization→L33, sample type→L34, channel layout→L36,
  codec→L43, filter→L45, metadata encoding→R1). Count and mapping both
  check out against §21's actual rows.
- Hunk 5 (§6.4): see the standalone finding below.

### FINDING (weak / low confidence): §6.4's "baseline three" parenthetical overstates what `[R-CNT-10]` guarantees

Location: line 928–930 (§6.4, normative running prose, not a Note).

Quoted repaired text: "...whose response also carries the
transport-authoritative file size F where the transport discloses a range
response's complete length (`[R-CNT-10]`, which governs where it does not,
**a separate size probe then making the baseline three**), so that §19.1's
first two steps cost one request between them..."

`[R-CNT-10]`'s actual text: "...a reader that cannot obtain one **MUST probe
separately or fail the open**..." — R-CNT-10 gives the reader two options
when the transport doesn't disclose a size, not one. The inserted
parenthetical presents "a separate size probe" as *the* consequence and
derives a specific count ("the baseline three") from it, but a reader that
takes the fail-the-open branch instead never reaches 3 requests — it fails
after 1. So the claim "making the baseline three" is true of one of
R-CNT-10's two licensed paths, not of what R-CNT-10 "governs" as a whole.

Byte-level: **No.** This is descriptive accounting inside §6.4, and the
Note immediately following it (§6.4's own Note, unedited) explicitly states
"no request count is a conformance property, and nothing here bounds what a
reader fetches" — so no conforming implementation's request count, and
certainly no byte on disk, turns on whether "baseline" is quoted as two or
three. I flag this at low confidence because the imprecision is real (a
quantifier mismatch between "governs" and the specific "three" it's paired
with) but the passage it sits in already disclaims exactly this kind of
strict reading.

### Everything else (Group B's flags-table repairs, Group G) — checked, no defect found

- Hunk 8 (§7.4 worked Example, MU=1/PE=1 → MU=0/PE=0): matches §7.3's
  registry table exactly (layer type: MU=0, PE=0). Correct fix of what was
  otherwise an internally-contradictory worked example.
- Hunk 14 (§20.4: "the user-metadata record PE = 1 and never" → "...and is
  dropped only with a layer that carries it"): checked against the newly
  added §20.4 sentence "A commit never removes a user-metadata record from a
  scope it keeps: a top-level one from the file, or a sub-record from a
  layer the commit retains" (hunk 15) — consistent: a top-level
  user-metadata record has no layer to be dropped with, so it is (still,
  correctly) never dropped; a sub-record is dropped only as a consequence of
  its layer's drop, never independently (PE=1 blocks independent drop).
- Hunk 6's "PE is a choice within MU = 0": checked against §7.3 ("writers
  MUST emit exactly the flag values fixed in the table" — i.e. PE is *not* a
  per-instance writer choice for a *registered* type) and §10.4 ("for a
  record type, its MU and PE assignment with justification" — i.e. PE *is* a
  choice made once, at registration, for a new type). Read in that light,
  "choice" refers to the registration-time decision (or, for an unregistered
  type the updater implements from its own definition, the definition's
  choice), not a per-write free choice — consistent with §20.4's own "the
  writer that stored it or the definition that governs it" framing for who
  fixes PE. Not an overclaim.
- Hunk 7's "The layer record is the one exception, and this specification's
  own": tested for exhaustiveness (EXHAUSTIVE-CLAIM check). Since §7.2 itself
  is normative and constrains what a *future* registered type may do (an
  MU=0 type may not carry further off-slot references — only the layer
  record, defined by this document itself rather than by later registry
  review, is exempted), "the one exception" is a rule this document commits
  future registrations to respect, not a falsifiable empirical claim about
  registrations outside its control. Not an overclaim.
- Hunk 25 (Appendix H, "as an appender, changes a layer..."): the added
  qualifier correctly narrows an obligation that, unqualified, would have
  misdescribed a rewriter (which changes fixed declarations by
  *re-declaring* under §20.5, not by the §20.3-step-4 bar an appender is
  held to). I checked whether Appendix H's separate "A rewriter, in
  addition..." paragraph restates the rewriter's own re-declare allowance
  and it does not explicitly — but Appendix H opens by disclaiming itself as
  authoritative ("never this summary") and is explicitly non-normative, so I
  did not file this as a finding; it is a checklist completeness gap, not a
  contradiction.
- Hunk 26's `[R-WRT-07]` rewording ("carries every structure it does not
  decode forward verbatim..." → "preserves the content of every structure
  it carries forward, re-pointing each extent slot..."): matches §20.5's own
  R-WRT-07 paragraph almost verbatim. The removed "does not decode" framing
  was residue of the old creator/rewriter test (decoded-everything) that
  hunk 11 replaced; removing it here is required for consistency and is
  correctly done.
- Hunk 3 (§3.3 Note): "compactors" → "rewriters carrying a layer forward" —
  consistent with the broader compaction→rewrite terminology cleanup
  (Group E) and with §20.5's actual scope (any rewriter, not just a
  compactor, operates on files whose layers it cannot decode).
- Hunk 1 (§2.3, citation list): adds "§20.3 step 6" alongside "§20.5" for
  the ignore-lane copy-forward/set-no-other behavior. Verified: §20.3 step 6
  (the appender's Commit step) does state "unknown ignore-lane flag bits
  copied forward and no other set (`[R-CNT-08]`)" — this was a real citation
  gap (only the rewriter's version, §20.5, was cited before) and the fix is
  correct and necessary now that the ignore-lane rule explicitly covers both
  tiers.
- Hunk 4 (§6.3, "the file it modifies" → "its input file"): see Group C
  notes above.
- Hunk 20 (§20.5 Example, "moves live bytes" → "changes what a range
  holds"): consistent with the surrounding cache-contract discussion
  (`[R-LIF-03]`'s "ranges never change beneath a file_id"); the new phrasing
  is the more precise one and does not conflict with anything else in the
  Example.
- Hunk 23 (Appendix G item 5, "Where neither reaches the data" → "Where
  neither *effect of the layout* reaches the data"): verified against §14.4's
  Note ("A single-channel numeric layer produces byte-identical tile images
  under either layout") that BOTH of the layout's two named effects (entry
  count via §11.2, and value arrangement via §14.2) fail to reach the data
  for a single-channel numeric layer, while the tile-extent effect (shape/
  grid count, the third quantity named two sentences earlier) always reaches
  the data. So restricting "neither" to "neither effect of the layout"
  (excluding tile extent) is the correct, more precise reading — the
  original "neither reaches the data" was ambiguous as to which of the three
  named quantities "neither" ranged over, and the fix resolves it correctly.
- Hunk 24: see Group E.
- Hunk 15's table's own internal consistency (all three rows, MU=1 /
  MU=0,PE=1 / MU=0,PE=0): cross-checked against the governing paragraph
  above the table ("Its MU = 1 row reaches only a type the updater does not
  implement... so for an implemented type only the PE bit bites") — this
  paragraph is pre-existing, untouched by any hunk, and is fully consistent
  with what the hunks added to the MU=1 row and to the paragraph below the
  table.
- Register rows (§21) sanity-checked against the table's citations:
  L46/L47 (reserved flags / MU=1,PE=0) against `[R-CNT-12]`; L49 (stored
  flags vs. registry) against `[R-CNT-22]`; F36/L25 (reserved-range record/
  sub-record types) against `[R-CNT-15]`. All consistent with the prose they
  restate; none of these rows was touched by any hunk, and none disagrees
  with the repaired prose, so §21.1's row-vs-prose precedence rule was never
  triggered.

---

## Rejected candidates (looked, found nothing)

1. Hunk 2's inserted "it"/"its" anaphor in the Conforming-updater bullet —
   checked for a stranded pronoun after insertion (check 8); concluded the
   qualifying clause modifies the whole disjunction and both readings point
   at the existing file's content, so not ambiguous enough to file.
2. Hunk 6's "PE is a choice within MU = 0" — checked against §7.3's
   writer-MUST-emit-fixed-values rule as a possible overclaim; concluded
   "choice" refers to the registration-time (or defining-registry-entry)
   choice, consistent with §10.4 and §20.4's own "whoever fixed PE=0...the
   writer...or the definition" phrasing.
3. Hunk 7's "the layer record is the one exception" — checked for an
   exhaustiveness overclaim against future registry growth; concluded the
   sentence is itself a constraint on future registration (normative,
   self-enforcing), not a falsifiable empirical count.
4. Hunk 25's Appendix H narrowing to "as an appender" — checked whether the
   rewriter's parallel re-declare allowance needed restating in the same
   appendix; concluded Appendix H's own "never this summary" disclaimer and
   non-normative status make this a completeness note at most, not a
   contradiction, so not filed.
5. Ran a control search for every "compaction" occurrence in the document
   (8 hits) to make sure hunks 9/21/24 were the only stale ones and that no
   *other* "compaction"-only claim was left overly narrow; the remaining 5
   (lines 62, 64, 746, 3560/3568, 3675) are all either non-normative intro
   prose, already correctly scoped to "a rewrite" pre-existing this round, or
   deliberately specific to compaction as one example (the "what compaction
   reclaims" worked Example). None needed a sweep.
6. Searched for other "dropped layer" / "drops a layer" occurrences (4 hits
   each via whitespace-normalized search) beyond the two findings above;
   the other two are the §20.3 step-4 bar paragraph ("a commit MAY drop the
   layer (§20.4) and add a new one under its name") and the §20.4 body text
   itself (the corrected one) — neither needs a sweep, both are already
   consistent with the corrected rule.

---

## Summary of findings to report

1. UNSWEPT_RESTATEMENT — §20.3 shape-(c) Example (line 3445) omits
   sub-records from what a dropped layer strands. Not byte-level (Example
   block, non-normative).
2. UNSWEPT_RESTATEMENT — §23.1 privacy passage (line 4369) omits
   sub-records (and the tile-index region) from what a dropped layer
   strands. Not byte-level (illustrative list, explicitly non-exhaustive,
   general clause already covers it).
3. TENSE_QUANTIFIER (low confidence) — §6.4's "baseline three" parenthetical
   (line 929) treats R-CNT-10's probe-or-fail-open choice as if only the
   probe branch existed. Not byte-level (request-count accounting, adjacent
   Note disclaims conformance weight).

Hunks involved across all findings and the analysis that produced them:
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21,
22, 23, 24, 25, 26 (all 26 were read and checked; findings anchor to hunks
5, 13, 14, 15, 17, 21, 26 specifically, since findings 1 and 2 are about
text those hunks' sibling repairs should have sept but is in untouched
lines, and finding 3 is about hunk 5 itself).
