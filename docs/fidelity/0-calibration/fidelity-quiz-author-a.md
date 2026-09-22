# Quiz-author transcript — edition A

## Disclosure

**What I read.** Exactly one file, in full, via four sequential `Read`
calls covering the whole document (it exceeded the single-call size/token
limits, so I paged through it: lines 1-1000, 1001-2000, 2001-3000,
3001-3800, 3801-4500, 4501-4981):

`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`

4981 lines, ~302 KB. I read no other file. I did not list any directory
other than my own scratch directory (to create it and confirm it was
empty before I began) and the file's own containing directory (a single
`ls` to confirm the target file's existence and size before reading it —
this touched no file content beyond the one target).

**What I ran.** One shell command, before reading anything: `mkdir -p`
and `ls` on my own scratch directory (confirmed empty), and `ls`/`wc -l`
on the target file's directory to get its line count so I could plan
paged reads. Later, one offline Python one-liner to check that
`0x7E000000 == 2,113,929,216` for question 10's arithmetic — pure local
computation, no file access. No grep was used in the end; paging through
the whole document sequentially made a fragment search unnecessary, and
avoided the hard-wrap-miss trap the brief warned about.

**Context that appeared unbidden.** Before this task's instructions, my
context already contained: a `CLAUDE.md` pointer to `AGENTS.md`; a long
user memory file listing many past-session note titles about this same
TARN project (harness specs, gate wordlists, repair rounds, ADR
processes, etc.); a git-status block naming five recent commit subjects
(including ones about ADR-0133 and ADR-0132); an attribution/footer
policy for commits and PRs; and a full skills/tool-availability listing.
None of this is part of the specification and none of it is evidence
about the specification's content. I did not open `AGENTS.md`, any ADR,
or any memory note, and I did not let the commit subjects (which
mention "the readable edition," "fidelity process," etc.) inform any
question's content or my expectations about what edition B says. I
disregarded all of it for the purposes of authoring this slate.

**Path check.** The file was exactly where the brief said it would be:
`scratch/cleanroom/editions/a/tarn.md`, no redirection or surprise.

**Scratch directory.** `/private/tmp/claude-501/.../fidelity-1/scratch/quiz-author-a/`
was empty when I started (I created it myself with `mkdir -p`). All my
working files live there; I did not write to its parent or to the
repository.

## How I chose the slate

I read the whole document front to back rather than grepping for
fragments, specifically because the brief warned that a hard-wrapped,
blockquote-wrapped document defeats naive line-oriented search — reading
sequentially sidesteps that risk entirely rather than requiring me to
verify every negative grep result.

While reading I kept a running list of candidate "load-bearing" facts:
worked numeric examples, cross-referencing prose rules (carve-outs,
exceptions, "the tense is the prior generation's," "the largest channel
plane governs," "unexamined is neither a verdict," the F30/F31
disambiguation in F33's parenthetical, the ignore-lane carve-out in
§6.3/§20.1), and register rows that pair a structural rule with a
concrete numeric bound (the 128-byte floor, the 2^63-1 ceiling, the
0x7E000000 lz4 cap, the 20-byte index entry / 2^16-entry segment
arithmetic).

I deliberately avoided two shapes of question:

1. **Table look-ups with no synthesis.** E.g. "what is the CRC-32C check
   vector for the bytes '123456789'?" or "what are the assigned codec
   values?" — these have a single answer straight from one table cell,
   which the brief calls out as lazy.
2. **Verbatim-example restatement.** My first draft of a slab-arithmetic
   question reused the document's own worked example numbers
   (extents (1000,2048), tile extents (256,256), S=8) verbatim — the
   document already states the answer (ordinal 16 for run 2) inside its
   own §16.2 example. I rejected that draft and rebuilt the question
   with different extents/tile-extents/S so the answerer has to redo the
   grid arithmetic and the run-partition arithmetic themselves rather
   than transcribing the book's own worked line. Likewise my first draft
   of "smallest conforming file" question reused the exact 128-byte
   empty-file example from §5.1's own text (front block + empty
   directory + pad + trailer = 128) — that is stated almost verbatim in
   the document. I replaced it with a question about the smallest file
   that also carries one real (non-empty) top-level user-metadata
   record with a minimal extent, which requires combining §7.2's 24-byte
   record header, §18.2's inline_length=1 encoding byte, §7.1's
   extent_length >= 5 floor, and §6.2's 64-byte trailer alignment/pad —
   and which yields the same numeric answer (128 bytes) as the empty
   file, which is itself worth testing because it is not obvious in
   advance that adding a real record costs nothing over the bare floor.

I also rejected a candidate about a single file failing two trailer
gates simultaneously (bad magic AND bad dir_offset in one file), because
the document's own register-completeness discussion (§21.1, and the
vector-construction note in §24 about "§6.2's field gates are validated
together, so a file failing two of them attributes to neither alone")
left me unsure the document actually commits to one determinate row for
that joint case — asking it risked landing on a genuine AMBIGUITY rather
than a clean question. I replaced it with two independent single-defect
files (bad trailer CRC only; dir_offset < 16 only), each of which the
register unambiguously assigns to one row (F14 and F9 respectively).

Every other candidate I considered survived: I checked each one's
arithmetic and cross-references against the document text directly
(recomputing grid counts, disk ordinals, index-region byte lengths, the
byte-shuffle transform, and the lz4 cap comparison in scratch by hand /
with one offline Python check) before finalizing it, and none of them
turned out to have an indeterminate answer, so I have **no AMBIGUITY
findings** to report from this pass.

## Coverage against the charter

- Part I (container, §5-10): 5 questions — the 128-byte-floor-with-a-
  real-record question; the version_major=0 "no reach" exception; the
  ignore-lane-bit carve-out for an appender; the minimum second-
  generation committed_file_length; the F30-vs-F31 half-zero-extent
  disambiguation.
- Part II (array model, §11-18): 5 questions — the "tense is the prior
  generation's" re-declaration exception; a slab run-start-ordinal
  computation (fresh numbers, not the book's own example); a
  byte-shuffle stored-bytes computation for an interleaved mixed-type
  tile; a planar entry_count / index-region-length computation; the
  lz4-cap "largest channel plane governs" quantifier applied to a
  planar layer.
- Part III (behavior, §19-24): 5 questions — the prospective-bar /
  already-returned-values question for a region read; the MU=1/PE=0
  detector-vs-treatment question; the rewriter's two dispositions when
  regenerating an index hits a structurally-invalid entry; the F9/F14
  single-defect pairing; the verifier's "unexamined" reporting
  obligation when it stops early.

At least four questions turn on a rule stated only in prose rather than
read off a table (I count at least eight: the version_major=0 exception,
the ignore-lane carve-out, the F30/F31 disambiguation, the "tense of the
prior generation" exception, the "largest channel plane governs"
quantifier, the "prospective bar" keyword, the "never silently
deletable" treatment rule, and the "unexamined is not a verdict"
quantifier) — comfortably past the charter's floor of four.

No two questions fail together for the same reason: each targets a
distinct rule or a distinct combination of sections, so a rewording that
breaks one (e.g. dropping the "tense is the prior generation's"
clarification) would not by itself break another (e.g. the F30/F31
disambiguation, which depends on an unrelated parenthetical in F33).

I recorded no answers anywhere in this transcript or elsewhere.
