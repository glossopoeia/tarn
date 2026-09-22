# Quiz-author (edition B) — working transcript

## Disclosure

**Scratch directory.** I created
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/quiz-author-b/`
myself. I listed it (`ls -la`) before doing anything else and found it
empty — no prior attempt's files were present.

**File read.** I read exactly one file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md`.
This is the exact path the brief named — no discrepancy to report. The file
is 302,125 bytes / 4,977 lines. Both the Artifact-style Read tool's per-call
character/token cap and its whole-file size cap are smaller than this file,
so I could not read it in one call; I instead:
- ran `wc -l` and `wc -c` via Bash directly on this one file (not grep/rg,
  but a metadata read of the one permitted file, needed only to plan how to
  paginate the Read tool — no other file was touched by these commands);
- issued a sequence of `Read` calls with increasing `offset`/`limit` against
  that same single file until I had covered lines 1 through 4977 with no
  gaps (verified by checking that each chunk's ending line number matched
  the next chunk's starting offset).

I did not use grep/rg at all in the end — the paginated Read calls gave me
the full text directly, in order, so I never needed to search for a
wrapped phrase. I did not open, list, or peek at any other file or
directory: not docs/, not PLAN.md, not conformance/, not spec/registry.json,
no git commands beyond the two `wc` invocations on the one approved file,
no web search or fetch.

**Unbidden context.** Before I did any of the above, my runtime had already
placed material in context that I did not ask for and that is not part of
the specification: a `CLAUDE.md` pointer to an `AGENTS.md` file, a user
memory file listing many TARN-related notes/pitfalls, a git-status block
naming recent commit subjects (about ADR-0133 and ADR-0132), an environment
block naming the working directory and scratchpad path, a list of available
skills, and today's date. I have disregarded all of it as evidence about
the specification's content — none of it informed any question below — and
I am not repeating its substance here beyond naming that it appeared.

**Paths.** The one file I was told to read was present at exactly the path
given. I inferred nothing from the path's own name (e.g. "edition b" tells
me nothing about what the text says, only which copy I was handed).

## Reading approach

Given the file's length, I read straight through in document order (Part
0 preliminaries; Part I §5–§10; Part II §11–§18; Part III §19–§24;
Appendices A–H), taking notes on concrete numeric worked examples, exact
table values, and — especially — prose rules carrying carve-outs,
exceptions, or quantifiers (the kind flagged in the brief as what a
rewording loses). I did not skim; every line number range from 1 to 4977
was covered by some Read call.

## Slate construction

I aimed for questions that require combining two or more places in the
document, or applying a stated rule/formula to a concrete case I
construct, rather than reading a single table cell back. Where I invent
concrete numbers (tile extents, coordinates, fill values, entry states), I
verified by hand that the document's own stated formulas and rules yield
one specific, checkable answer — I am not recording those computed
answers here, per the brief's instruction not to record my own answers
anywhere, but each question below was checked for a single determinate
answer before being kept.

Coverage by Part:
- Part I (container, §5–§10): Q1, Q2, Q3, Q12, Q15 — five questions,
  covering the lz4 cap interacting with declared geometry, the front-block
  residency carve-out, the index-region length formula under
  index_encoding 1, the fixed validation order of the trailer gates versus
  the directory fetch, and the one numeric-identifier space with no
  experimental range.
- Part II (array model, §11–§18): Q4, Q5, Q6, Q7, Q13 — five questions,
  covering linearization + byte-offset arithmetic end to end, padding
  content forced to equal fill (with little-endian encoding), planar
  per-channel storedness independence under sparse reads, the packed-
  boolean-plane carve-out on the byte-shuffle stride, and the
  "transparent" carve-out for structurally-rejected/sentinel entries
  inside slab run-continuity checking.
- Part III (behavior, §19–§24): Q8, Q9, Q10, Q11, Q14 — five questions,
  covering a verifier's *cannot establish* verdict together with a partial
  slack total, the coverage-walk consequence of a structurally-rejected
  tile-index entry, the closed list of what an appender may change on a
  layer that stored a tile in the superseded generation, the mandatory
  fresh file_id on a rewrite even under byte-for-byte-identical content,
  and an appender's verification-depth obligation over index segments it
  copies forward unchanged during a full index re-emission.

At least nine of the fifteen turn on a prose rule (carve-out, exception,
or quantifier) rather than a table lookup, comfortably over the brief's
floor of four: Q2, Q5, Q7, Q8, Q10, Q11, Q12, Q13, Q15.

## Rejected candidates

- A pure "what is the smallest conforming file size" question — the
  document states 128 bytes directly in a worked example; this is a
  table/example quote-back with no second place to combine, so I dropped
  it.
- A request-accounting question ("how many HTTP requests does the open
  cost") built around a transport that does not disclose a range
  response's complete length — the interaction between the fallback size
  probe, suffix-window containment, and "MAY" phrasing left me unable to
  pin one crisp integer for every reasonable construction of the scenario,
  so I dropped it rather than risk an underdetermined question.
- A question about how many commits separate two generations of a file —
  the document is explicit that this is *not* recoverable from the format
  at all (no field counts commits), so it cannot be posed as a "the
  document determines a single answer" question; it would only be usable
  as a question whose answer is "indeterminate by design," which is a
  fact about the model, not a fidelity-testable byte-level answer.
- A duplicate-purpose question about zstd's Window_Size derivation
  (Single_Segment_Flag path) — I judged this too close in shape and
  failure surface to the lz4 decoded-size-cap question (Q1) I kept: both
  are "does this codec's declared/derived size exceed a cap" questions,
  and the brief asks me not to bank two questions that fail together for
  the same reason. I kept the lz4 one (Part I/II boundary, cleaner
  arithmetic) and dropped the zstd one.
- A question on how many distinct "false" encodings the format admits for
  interleaved booleans — this just restates `[R-SER-08]`/`[R-TYP-07]`'s
  rule back as a fact rather than requiring the answerer to combine or
  apply anything, so I dropped it in favor of Q5's padding-content
  question, which forces the same fill-authoritative rule to be applied
  to a geometry- and type-derived byte pattern.

## Findings

None. I did not encounter a question candidate for which this text failed
to determine a single answer; no AMBIGUITY findings are reported below.
