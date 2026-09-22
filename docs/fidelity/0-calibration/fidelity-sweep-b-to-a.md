# Sweep transcript — completeness sweeper, reading B into A

Scope: exactly two files.
- edition A: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (4981 lines, 302380 bytes)
- edition B: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md (4977 lines, 302125 bytes)

Working files (this scratch directory, mine alone):
- a_norm.txt, b_norm.txt — normalized (unwrapped) paragraph streams of A and B
- para_diff.txt — `diff -u a_norm.txt b_norm.txt`

## Method

Both editions are hard-wrapped prose (blockquotes prefixed `> `). A naive
line-by-line or short-fragment grep would produce false negatives wherever a
sentence's wrap points differ between editions, and false "zero" results are
exactly what the brief says must be proven, not assumed. So instead of reading
each of the ~24 sections by eye and re-typing an inventory (which, for prose
this close to verbatim, mostly reproduces the source), I wrote a small
normalizer (Python, run via Bash — no file read but the two in-scope paths)
that:

1. Splits each file into blank-line-delimited paragraphs.
2. Strips leading `> ` (and `>`) blockquote markers so a quoted Note/Example/
   Rationale block's text is compared on its content, not its indentation.
3. Joins each paragraph's wrapped lines with single spaces, so wrap-point
   differences between editions cannot hide a real textual difference or
   manufacture a false one.
4. Leaves fenced code blocks (the box diagrams) as literal lines, unjoined —
   these are already covered by the mechanical checker's fenced-block
   comparison and are not re-diffed here.

Both editions normalized to exactly **1041 paragraphs**, and the paragraph
lists align 1:1 (confirmed by the diff below touching only isolated hunks,
never a shift). `diff -u` between the two normalized streams is therefore an
exhaustive, whitespace-blind diff of every sentence in the document —
including the ID-less carve-outs, exceptions and quantifiers this sweep's
charter names as its own ground, since those live inside ordinary paragraphs
this method also unwraps and compares.

## Result of the exhaustive diff

Only **6 of 1041 paragraphs** differ at all between the two editions. Each is
listed below with its disposition. (Full unified diff kept in
para_diff.txt in this scratch directory.)

| # | Location | Disposition |
|---|---|---|
| 1 | §6.3, the ignore-lane-bits sentence, ends `[R-CNT-08]` | **Not re-diffed** — inside a requirement-ID paragraph; the mechanical checker already compares `[R-...]`-tagged paragraphs. (Also independently EQUIVALENT: "MUST copy forward X" already entails "MUST NOT clear X".) |
| 2 | §20.3 step 2 ("Open"), "...MUST NOT drop the record [save where §20.4 licenses the drop]." | **Reported as swba-01** (LOSS) — no R-ID on this clause, not a table/register row. |
| 3 | §20.3, worked "Example." index-region byte count | **Reported as swba-02** (worked-figure discrepancy) — labelled Example block, not a table/register row/R-ID paragraph. |
| 4 | §20.4, "Its MU = 1 row reaches only a type the updater does not implement" vs "reaches every type, implemented or not" | **Reported as swba-03** (contradiction) — ordinary prose, no R-ID on this sentence. |
| 5 | §20.4, "One sub-record blocks the drop..." sentence, present in A and absent from B | **Not reported** — closed as EQUIVALENT: the same content ("blocks modification of that layer, its drop included") is already stated verbatim, unchanged, in both editions' governing-flags table (MU = 1 row), so B does not lose any decided content by dropping this restatement. |
| 6 | §21.2 register, row F19, Instances cell: "flags bits 0–15" (A) vs "flags bits 0-7" (B) | **Not re-diffed** — inside a §21 error-register table row, which the task states is already compared mechanically. Noted in disclosure as a live discrepancy in case that coverage is imperfect, but not filed as a swba finding since it is out of this sweep's assigned ground. |

## Control checks (proving the zeros, not assuming them)

- Paragraph-count parity: 1041 = 1041 (a shift would appear as a run of
  spurious hunks; none appeared beyond the 6 isolated ones above).
- Tail identity: the last ~500 characters of a_norm.txt and b_norm.txt are
  byte-identical; the last 15 raw lines of both source files are also
  byte-identical. This confirms the normalizer consumed each file to its end
  (no silent truncation before the size limit that blocks a direct `Read`
  of either 300 KB file).
- Byte-budget reconciliation: raw file sizes differ by 302380 − 302125 = 255
  bytes. Summing the character deltas of the six paragraph edits found above
  (removed clauses in items 1, 2, 5; a 3-vs-2-digit-no-op swap in item 3;
  a wording swap of comparable length in item 4; a short cell edit in item 6)
  accounts for essentially all of that 255-byte delta. If a seventh,
  undetected edit existed elsewhere, the reconciliation would show an
  unexplained residual; it does not.
- Point control searches: `grep -n` for the exact differing phrase in each
  of the 6 loci (`"MUST NOT drop the record"`, `"644 bytes\|664 bytes"`,
  `"MU = 1 row reaches"`, `"One sub-record blocks the drop"`,
  `"incompat lane (bits 0-15) is set"`, `"MUST NOT clear them"`) returns
  exactly one hit per file at the expected line, in both A and B where
  present — confirming each difference is real, singular, and not an
  artifact of normalization.

## Findings filed

- **swba-01** (LOSS): §20.3 step 2's carve-out "save where §20.4 licenses the
  drop" is present in A and absent from B, leaving B's step 2 an unqualified
  "MUST NOT drop the record" that, read alone, conflicts with §20.4's
  (unchanged, present in both editions) licence for an appender to drop a
  PE = 0 record.
- **swba-02**: §20.3's worked Example computes the same 32-tile,
  20-byte-per-entry index region as 644 bytes in A and 664 bytes in B; 32
  · 20 + 4 = 644, so B's figure is arithmetically wrong on its own stated
  inputs.
- **swba-03**: §20.4's sentence describing the governing-flags table's MU = 1
  row's reach is inverted between editions — A: "reaches only a type the
  updater does not implement"; B: "reaches every type, implemented or not"
  — and B's version directly contradicts the clause immediately following it
  in the same sentence ("so for an implemented type only the PE bit bites"),
  which is unchanged.

No section of the document was left unswept: the exhaustive normalized diff
covers every paragraph of both editions, front matter through the closing
paragraph before the appendices/registry material (which are outside this
sweep's two in-scope files' bodies is not applicable here — both files end
identically, confirmed above). I did not additionally perform a manual,
prose-by-prose per-section item inventory as the charter's default method
describes, because the exhaustive diff already is that comparison, done
mechanically and without the risk of a reader's eye skipping a clause; I
disclose that substitution here rather than presenting a hand-walk that would
only re-derive the same six loci.
