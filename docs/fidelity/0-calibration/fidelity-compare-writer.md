# Writer comparator — transcript

## Disclosure

**What I read.** Exactly four files, all named by the brief:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md` (4977 lines)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-writer-a.md`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-writer-b.md`

The two edition files exceeded my file-reader's 256KB single-call cap, so I
read the two transcripts in full with the Read tool, and worked the two
edition files with `diff` (Bash, reading only these two named files) plus
targeted `sed`/`grep` pulls by exact line number once `diff` told me where to
look. I did not read either edition file as unstructured line-offset chunks
the way both walkers did, because a full structural `diff` is a stronger tool
for exactly this charter than sampling: it is exhaustive over the whole file,
not a sample, and its correctness is self-checking (see "Proof of
exhaustiveness" below) in a way a handful of grep fragments is not.

**Method for the hard-wrap / "> " caveat.** I did not rely on any single-line
grep match to conclude a phrase was absent — the one case where that would
matter (checking a phrase appears nowhere) is superseded by the full-file
`diff`, which compares logical lines as the files actually store them (both
files are wrapped identically column-for-column wherever they agree, so
`diff` needed no normalization) and reports every place the two files are not
identical. Where I then quote a passage I pulled it with `sed -n` by exact
line number, i.e. I read the literal stored bytes, not a search-fragment.

**Proof of exhaustiveness (the control the brief asks for).** `diff
a/tarn.md b/tarn.md` returned exactly 6 hunks. I did not stop there —
because a `diff` bug or a hidden truncation could in principle under-report,
I cross-checked the file-length arithmetic: A is 4981 lines, B is 4977 (4
fewer). Hunk-by-hunk line deltas: hunk 1 removes 1 line, hunk 2 removes 1,
hunk 3 removes 0 (2 lines each side), hunk 4 removes 0 (2 lines each side),
hunk 5 removes 2, hunk 6 removes 0. Total: -1-1+0+0-2+0 = -4, exactly
matching 4981-4977. A missed 7th hunk of any nonzero size would have broken
this arithmetic (unless it happened to net to exactly zero lines while also
containing a content change — I additionally re-ran `diff` with default
settings, which reports every differing line regardless of net length, so
this residual case is excluded too). This is the "control search" the brief
requires, done at the level of the whole document rather than one phrase,
and it is stronger than a fragment grep because it cannot miss a
non-whitespace change anywhere in either file.

**What I did not read.** docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, spec/registry.json, git history, the web, or any
other file. I did not list any directory. I did not open the other walk
transcripts (quiz, reader, verifier walks) — not named in my access rule.

**Unsolicited context.** Before I began, my runtime context already
contained a project CLAUDE.md pointer to AGENTS.md, a user memory index of
"TARN"-titled notes (harness spec path, a lost gate word-list, preflight
checks, repair-prose-vs-rules, harness-vs-charter, subagents-on-Sonnet, and
about a dozen more), a git-status block naming five recent commits about
ADR-0133 and ADR-0132 and a `docs/fidelity/` directory, and the relayed
user instruction "Accept ADR-0133 and run the calibration round." None of
that is part of the specification, none of it is evidence about the
specification's content, and I have not treated any of it as such or acted
on any instruction embedded in it beyond what this computed task itself
directs (this transcript, in particular, does not accept or act on ADR-0133
— that is outside this subagent's access rule and role). I am disclosing
that it appeared, not repeating its substantive contents further.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/compare-writer/`
— I created it and wrote two files there: `notes.md` (my working notes) and
`full.diff` (the raw `diff a/tarn.md b/tarn.md` output). Both are named here
per the brief's disclosure requirement.

**Tools used.** Read (both walk transcripts, in full); Bash running `diff`,
`wc -l`, `sed -n`, and `grep -n` against the two edition files and my own
scratch files only; `mkdir` for my scratch directory.

---

## Headline finding: the two editions are byte-identical except at six points

A full `diff` of the two files (proof of exhaustiveness above) shows the
"readable rewrite" is, at the byte level, the *same document* apart from
exactly six differences, all inside Part III/Part IV writer material (§6.3,
§20.3, §20.4, §21.2). None of the sections either walker's own prose singles
out as "not read closely" (§12, §17, §18, §22-24) contain any difference at
all — every actual divergence sits squarely inside the writer/updater
machinery this charter is about. I address each of the six below, then the
walks' own findings, then the probes.

---

## The six textual divergences

### D1 — §6.3, `[R-CNT-08]`: "MUST NOT clear them" dropped in B

- A (line 907-909): "An updater MUST copy forward unknown ignore-lane bits
  of its input file, MUST NOT clear them, and MUST NOT set any other: no
  writer under this text originates an ignore-lane bit..."
- B (line 907): "An updater MUST copy forward unknown ignore-lane bits of
  its input file, MUST NOT set any other: no writer under this text
  originates an ignore-lane bit..."

**Kind: EQUIVALENT.** "Copy forward X" already means the output's
corresponding bits equal the input's; that relation is violated exactly as
much by clearing a set bit as by setting an unset one. B's "MUST NOT clear
them" was restating what "copy forward" already entails (A's own §20.5
rewriter-specific restatement, unchanged in both editions, never separately
states a "must not clear" duty either — it also just says "carries the
input's unknown ignore-lane bits into its output trailer... and sets no
other"). No register row anywhere in either edition distinguishes "cleared a
bit" from "failed to copy a bit forward" as separate violations (I checked:
neither file has such a row — this is confirmed by the exhaustive diff
itself, since if such a row existed differently worded in each file it would
be a 7th hunk).

**Byte-level test:** No. An implementation built from B alone that
satisfies "copy forward ... MUST NOT set any other" bit-for-bit equals one
built from A alone; there is no daylight between "copy forward" and "don't
clear."

### D2 — §20.3 step 2: the drop exception is missing in B — **LOSS**

- A (lines 3218-3220): "Against any other structure the appender carries
  forward, it MUST NOT repair the defect — `[R-LIF-01]` freezes the
  committed prefix — and MUST NOT drop the record save where §20.4 licenses
  the drop."
- B (line 3218): "Against any other structure the appender carries forward,
  it MUST NOT repair the defect — `[R-LIF-01]` freezes the committed prefix
  — and MUST NOT drop the record."

**Kind: LOSS.** This is the general reliance/no-repair rule for anything an
appender carries forward unmodified (§20.3 step 2, feeding `[R-WRT-04]`).
A states it with an explicit carve-out for §20.4's own licensed drops (the
MU=0/PE=0 row both editions state identically at §20.4, quoted in both
walks' W4 answers: "an appender MAY drop the record in any commit it is
otherwise free to make"). B states the *same* general rule with **no**
carve-out — read on its own, B's sentence is an unqualified "MUST NOT drop
the record," which directly contradicts §20.4's own later, unchanged
"appender MAY drop" permission a few dozen lines on in the very same file.
A resolves the tension explicitly; B does not — B is internally
self-contradictory on a question (may a live, in-place appender ever drop a
carried-forward record?) that A resolves without contradiction.

Neither walker's transcript surfaces this: both W4 answers (quoted
identically in each transcript) are built entirely from the §20.4 table,
which is unchanged, so both walkers reach the same (correct, and in A's
case fully consistent) answer without ever quoting the step-2 sentence that
diverges. An implementer who read B's step 2 first and took it literally,
however, would have reason to build an appender that never drops any
carried-forward record at all — including the MU=0/PE=0 record W4 asks
about — until/unless they separately notice and prioritize §20.4's later,
contradicting permission. That is a real fork in what a B-only
implementation might emit (retain vs. drop the same record) that an
A-only implementation does not face.

**Byte-level test:** Yes, conditionally — an implementation of B that
resolves the two competing statements the "wrong" way (favoring the
absolute step-2 prohibition over §20.4's specific license) emits a
different, larger file (record retained) for the same W4 scenario than any
implementation of A, which has no such competing statement.

### D3 — §20.3 Example, W2's own figure: 644 (A) vs 664 (B) — **matches writerb-01**

- A (line 3400): "the layer's full new index region (32 · 20 + 4 = 644
  bytes — one entry re-pointed, 31 byte-identical)"
- B (line 3398): "the layer's full new index region (32 · 20 + 4 = 664
  bytes — one entry re-pointed, 31 byte-identical)"

I confirm this is a genuine cross-edition divergence, not merely a defect
walker B noticed in isolation: **edition A's own worked Example is
arithmetically correct** (32×20+4=644, matching `[R-CNT-17]`'s formula,
identical in both editions), and **edition B's is not**. Walker A quoted the
correct "644" straight from A's text; walker B independently recomputed and
caught B's "664" as wrong. Both walkers are right about their own edition's
text.

**Kind:** By the letter of the four-way test this is closest to
**EQUIVALENT** at the byte level, because this passage is labelled
"**Example.**" in both editions (confirmed identical bold label, both
files) and `[R-CNF-01]` (identical text, both editions) makes Example blocks
non-normative — the number that actually governs any implementation's
output is `[R-CNT-17]`'s formula, unchanged and correct in both editions.
But per the charter's instruction to treat a defect found in one edition's
own walk as a LOSS when the other edition does not share it: A does *not*
share this defect (A's Example is correct), so under that framing this is a
**LOSS of internal-consistency/determinacy unique to B** — a reader of B
alone hits a document that contradicts itself between its own formula and
its own worked example, where a reader of A does not.

**Byte-level test:** No for real output/accept-reject (governed by the
unchanged, correct formula in both editions) — but yes for anyone
self-checking a test vector against the Example's own stated total, who is
misled only in B.

### D4 — §20.4 intro: MU=1 row's scope — self-contradiction unique to B — **LOSS**

- A (lines 3505-3508): "Its MU = 1 row reaches only a type the updater does
  not implement — an updater implements both registered types and
  understands an unregistered type it implements from its definition,
  modifying their records as §20.3 and that definition provide — so for an
  implemented type only the PE bit bites"
- B (lines 3495-3498): "Its MU = 1 row reaches every type, implemented or
  not — an updater implements both registered types and understands an
  unregistered type it implements from its definition, modifying their
  records as §20.3 and that definition provide — so for an implemented type
  only the PE bit bites"

**Kind: LOSS (of determinacy).** A's sentence is internally consistent: the
MU=1 row (whole-scope "retain byte-identical," blocking modification/drop,
possibly reject-file) applies only where the updater does not implement the
record's type; for an implemented type, the updater instead follows the
type's own definition, and only the PE bit (droppable or not) is left for
the generic table to state. B's edited clause says the *opposite* of that
premise — "reaches every type, implemented or not" — while keeping,
word-for-word, the conclusion that only follows from the original premise
("so for an implemented type only the PE bit bites"). B's paragraph now
asserts two things that cannot both be true in the same breath. A states
one coherent rule; B states a contradiction where A states a rule.

This does not change either walker's actual W3/W8 answers, because both
probes stipulate a type the updater does *not* implement — the one case
both readings of the sentence agree the MU=1 row governs. But it is a real
place where B, read for any *other* scenario (e.g., an implemented-but-
untouched record whose stored/registry flags happen to be MU=1), gives an
implementer no coherent instruction, where A does.

**Byte-level test:** Conditionally yes, for scenarios outside the eight
probes (an implemented type carrying MU=1 on a record the commit does not
logically modify): an implementation of A applies only the PE bit; an
implementation of B that takes "reaches every type, implemented or not" at
face value could apply the MU=1 row's blocking/refusal behavior where A's
text would not, a genuine accept/reject divergence on some file.

### D5 — §20.4, after the table: the sub-record-blocks-the-drop exception is entirely absent from B — **LOSS**

- A (lines 3510-3513): "...so a dropped layer's sub-records and their
  extents go with it whatever their PE bits. **One sub-record blocks the
  drop, a sub-record of a type the updater does not implement with MU = 1,
  the drop being a modification of the scope it governs (the table's first
  row).** A commit never removes a user-metadata record from a scope it
  keeps..."
- B (lines 3508-3510): "...so a dropped layer's sub-records and their
  extents go with it whatever their PE bits. A commit never removes a
  user-metadata record from a scope it keeps..."

**Kind: LOSS.** This is not a narrowing or a rewording — the entire
sentence stating the exception is gone from B. A states plainly that a
layer otherwise licensed to be dropped (its own record is PE=0, registry-
fixed) *cannot* actually be dropped if one of its sub-records is itself an
unimplemented-type record carrying MU=1, because dropping the layer would
modify the very scope that sub-record's MU=1 status protects. B's text, as
it now stands, states only the unqualified rule ("the drop takes the layer
whole... whatever their PE bits") with nothing to stop a reader concluding
that an unimplemented-type MU=1 sub-record is no obstacle at all — directly
opposite to what MU=1's own row two paragraphs earlier says a sub-record's
MU=1 status does ("blocks modification of that layer, its drop included").
B is now internally inconsistent in the same direction as D4: the MU=1
row's own text (identical in both editions, inside the table) already says
an unknown-critical sub-record "blocks modification of that layer, its drop
included" — A's post-table sentence is simply restating/cross-referencing
that consequence for the specific "drop the whole layer" case; B, having
deleted the restatement, leaves a reader who reaches this later paragraph
without independently re-deriving it from the table three paragraphs back
free to miss the constraint entirely.

Walker A's own transcript (§1b) explicitly relies on and quotes this exact
sentence ("blocks the drop… the drop being a modification of the scope it
governs") as load-bearing for its account of layer-drop mechanics; walker
B's transcript, working from B alone, never mentions this exception at all
— because it is not there to find. This is exactly the kind of walker
divergence the charter's item 4 asks me to check for a forcing text vs. a
silent one: edition A's text forces this point into view; edition B's text
does not raise it at all, and B's walker did not independently derive it
(nor should be expected to — it is not implied elsewhere in the retained
text).

**Byte-level test:** Yes. Take a layer whose own record is PE=0 (registry-
fixed, so ordinarily droppable) but which carries one sub-record of an
unimplemented type with MU=1. An implementation built from A alone must
refuse to drop that layer via a commit (the drop is blocked at file
scope for the top level or blocks that layer under §20.4's own table, and
A's restated sentence removes any doubt for the "drop the layer" path
specifically). An implementation built from B alone, having never been told
of this exception in the passage that actually discusses dropping whole
layers, has a real chance of emitting a commit that drops the layer anyway
— a different accept/reject/output-bytes outcome for the identical input
and identical operation.

### D6 — §21.2 register row F19: field column says "bits 0-7" in B, prose still says "bits 0-15" — **LOSS**

- A (line 3863): `| F19 | Any bit of the flags incompat lane (bits 0-15) is
  set... | flags bits 0-15 | reader | open | [R-CNT-08] |`
- B (line 3859): `| F19 | Any bit of the flags incompat lane (bits 0-15) is
  set... | flags bits 0-7 | reader | open | [R-CNT-08] |`

**Kind: LOSS (internal inconsistency unique to B).** Every other mention of
the incompat lane in *both* editions — the §6.2 structural-field table
(line 838, identical in both), §6.3's prose (line 899, identical in both),
and even F19's own prose cell in this very row — says "bits 0-15." Only
B's machine-readable "Field/bytes" column for F19 was changed to "bits
0-7," with nothing elsewhere in B corroborating an 8-bit incompat lane. A
has no such inconsistency anywhere.

**Byte-level test:** Conditionally yes. This register table's "Field/bytes"
column is exactly the kind of column a conformance-test generator or a
register-driven verifier reads mechanically to know which bits an F19 check
covers. An implementation built from B that trusts this column literally
checks only bits 0-7 for F19 and would *accept* a file with, say, bit 10 set
(an unimplemented incompat bit) that F19's own prose — and any
implementation built from A — reject-file. This is not one of the eight
writer probes (F19 is a reader/open-time check, not directly a writer
duty), so I report it under charter item 5 (reading past the probes) rather
than as a probe divergence, but it is squarely inside the register a writer
must itself satisfy at creation (a creator writes flags=0, so never
triggers F19 itself, but a rewriter/appender preserving an input's set
incompat bits — which none may do, since incompat bits must never be set at
all under `[R-CNT-08]` — depends on the same bit-range definition being
consistent).

---

## The walks' own findings, checked against the other edition

### writera-01 (zero-copy drop-and-recreate reuse) — shared, not a divergence

The supporting text walker A quotes ("a commit MAY drop the layer (§20.4)
and add a new one under its name and other declarations... the dropped
layer's former extents included") sits at A:3294-3298 and is byte-identical
at B:3292-3296 (confirmed by `sed`, and by the full-file diff showing no
hunk in this range). The ambiguity walker A identifies — whether a
same-commit drop-and-recreate may legitimately re-point at the just-vacated
extents, achieving a forbidden fill-change's effect at zero cost for
padding-free tiles — is present, word for word, in edition B as well. This
is neither a LOSS nor an ADDITION: it is a shared indeterminacy both
editions carry equally. I looked for anything in B's surrounding, unchanged
text (§9.1's immutability rule, `[R-CNT-13]`'s single-ownership rule, both
identical in both editions per the same check) that might resolve it one
way in B and not in A, and found none — same text, same gap.

### writera-02 (cross-layer slab-invariant re-check ambiguity) — shared, not a divergence

Every citation walker A gives (`[R-WRT-03]`'s reliance principle at
A:3198/3227/3232/3717, matching B:3197/3225/3230/3713; §11.1's Rationale
note on grid-count-unchanged growth) falls outside all six diff hunks. I
independently confirmed the `[R-WRT-03]` line locations are identical
text at the corresponding (off-by-one-to-two, matching the upstream hunks'
cumulative line-count shift) positions in B. This is the same shared
indeterminacy in both editions, not a divergence.

### writerb-01 (644 vs 664) — real cross-edition divergence, already covered as D3 above.

---

## The eight probes

For W1, W6, and W7, I confirm — by the same full-file diff, not by spot
sampling — that every section either walker cites for these three probes
(§5.1's Example and §6.1/§6.2's tables for W1; §20.3 step 4's full
fixed-declaration paragraph, including its "sentinel tile" and padding
consequences, for W6; §9.1 through §9.6, including the crash-example block
and the recovery-scan procedure, for W7) is **byte-identical** between the
two editions. None of the six hunks fall inside any of these ranges. Where
the two walkers' answers read slightly differently for W6 (walker B
separately calls out the sentinel/unstored-tile case as a second witness-
gap, alongside the padding case walker A gives), that is a difference in
each walker's own thoroughness reading *the same, unchanged text* — not a
document defect and not something one edition states that the other
doesn't. I confirm this rather than assume it: I read A's full paragraph
(A:3255-3272) side by side with B's (B:3253-3270) and they are identical,
sentinel-tile language included in both (A:3260-3262, "a fill value is a
legal sample value... an unstored (sentinel) tile" language is present via
the same "§14.5" and reference-array citations in both — the register
witnesses list T3/T14/T21/T22/T4/T5/T2 is identical in both). Walker A's
own W6 answer simply did not draw out the sentinel-tile branch explicitly;
the text supporting it was equally available to both walkers.

**W2 —** the only probe whose two answers actually diverge is exactly
D3 above (644 vs 664), a genuine, if non-normative, cross-edition
difference. Both walkers otherwise agree completely (order of appended
regions, what becomes slack, the formula), because the rest of the section
(§20.3 step 4's appended-regions description, `[R-WRT-04]`, `[R-CNT-17]`)
is identical in both editions.

**W3 —** both answers agree and both cite text identical in both editions
(the MU=1 table row itself, `[R-CNT-15]`, `[R-WRT-06]`, §21.6). D4's
scope-of-the-MU=1-row wording difference does not change this probe's
answer, since the scenario stipulates an unimplemented type — the one case
both readings of D4 agree the row covers.

**W4 —** both answers agree, both citing the (identical, in both editions)
§20.4 MU=0/PE=0 row. Neither walker's answer is wrong, but D2 (above) shows
edition B contains a second, unqualified statement of the general
no-drop rule that — read alone, before reaching the table — would mislead
an implementer of B specifically; A's parallel statement heads off that
exact confusion with its own "save where §20.4 licenses" clause. I record
this as a LOSS at the document level even though it did not surface as a
difference in either walker's probe *answer*.

**W5 —** both answers agree; the relevant `[R-CNT-08]`/`[R-WRT-06]`/§20.1
text differs only by D1 (above), which I found to be EQUIVALENT (no
byte-level effect).

**W6 —** both answers agree in substance (padding positions -> T4;
padding-free interior tiles -> unwitnessed); text identical in both
editions per the check above. B's answer is more complete (adds the
sentinel-tile witness-gap) but from the same, unchanged text.

**W7 —** both answers agree essentially verbatim (they even converge on
near-identical phrasing, since the underlying text is byte-identical);
no divergence.

**W8 —** both answers agree in substance and converge on the same
"foreclosed premise" reading of `[R-TYP-01]`/`[R-CNF-03]`/L34. The table
row and `[R-WRT-09]`/`[R-WRT-06]` text both cite is identical in both
editions. D4 and D5 (above) are both inside this same neighborhood of text
(§20.4) but do not change the specific W8 scenario's answer, since W8
concerns a *sample*-type violation caught at layer access (L34), not a
*record* sub-record's MU=1 status — D5's missing exception would matter for
a different, adjacent scenario (a layer with an unimplemented-type MU=1
*sub-record*), which W8 does not ask about, but which the general
"rewriter dropping a layer" mechanics both walkers otherwise treat as
settled do depend on.

---

## Evidence-gathering notes (what a zero really means here)

I ran the `diff` once, over the whole file, rather than many small greps —
so there is exactly one "sweep" to report, and it returned 6 hits, not 0.
Everywhere above I report a *zero* (e.g. "no other mention of the incompat
lane says bits 0-7"), that zero is a `grep -n` across the *entire* file for
the competing pattern, and I list the exact non-zero count of *matching*
(consistent) occurrences found instead, which is the positive control the
brief asks for (proving the search mechanism itself works, since it finds
the consistent occurrences reliably).
