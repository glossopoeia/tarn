# Quiz-author A — working transcript

## Disclosure

- A "relayed user request" (the single word "Go") was prepended above this
  brief by the harness. It is the message that launched the orchestrator run,
  not a task for me; it needed no reconciliation with the brief and did not
  widen the access rule. Noted and set aside.
- Unrequested context appeared in my window before this brief: a project
  CLAUDE.md pointer, an index of the user's own memory-file titles about this
  TARN project, a git-status block (branch, recent commit subjects), and an
  attribution/skill-listing block. None of it is part of the specification and
  none of it was treated as evidence about the specification's content; I did
  not open or read any of the files that index names.
- I read exactly one file: `scratch/cleanroom/editions/a/tarn.md`, at the path
  the brief gave, and nothing else. I did not list any directory other than
  creating my own scratch directory, did not open any other copy of the
  specification, did not consult docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
  README.md, conformance/, or spec/registry.json, and did not use git or web
  tools.
- Method: I read the file end-to-end in sequential large offset/limit chunks
  via the Read tool (covering roughly lines 1–4800 of 4981, i.e. the full
  normative body, Parts 0–III, §21's register, §22–24, and Appendices A–D plus
  most of G), rather than grep. This sidesteps the hard-wrap/grep pitfall the
  brief warns about — I never searched for a phrase and trusted a zero result,
  because I read the running text directly instead of pattern-matching it. I
  did not finish the remainder of Appendix G or read Appendix H (non-normative
  checklists); nothing in my slate depends on content past line ~4800, which is
  all non-normative appendix material (constants/registry/rationale/changelog/
  references/reproducible-writer profile already covered where it restates
  normative rules).
- My scratch directory, `/private/tmp/claude-501/.../fidelity-4/scratch/quiz-author-a/`,
  was empty when I started (verified with `ls -la`); no prior attempt's files
  were present.
- I ran no grep/rg in the end; local arithmetic (grid counts, ceiling
  divisions, IEEE-754 bit layouts, byte-shuffle permutations) was done by hand/
  reasoning while drafting questions, reading no files.
- No answers are recorded anywhere in this transcript or in my structured
  return, per the charter.

## Coverage strategy

Read the whole document once, section by section, flagging candidate loci for
pointed questions as I went: the container (front block, trailer, directory,
records, layer record, integrity map, lifecycle/commit protocol, extension
points), the array model (geometry/grid arithmetic, linearization and disk
ordinals, sample types including bfloat16, fill and sparse tiles, tile
serialization byte layout, packed booleans, tile index and segments, slabs and
alignment, codecs and filters, user metadata), and Part III (the open
algorithm and its request accounting, validation timing, the tile-read
algorithm, writer tiers and the append procedure's declaration-change rules,
re-emission/preservation, rewriting, the error register's instance/outcome/
detector apparatus, security/privacy considerations, and the vector-coverage
rules).

I then built the 15-question slate against the charter's distribution
requirement (≥3 Part I, ≥3 Part II, ≥3 Part III, ≥4 turning on a prose rule —
a carve-out, exception, quantifier, or keyword) and against its other
constraints (single determinate answer; combines ≥2 places or applies a rule
to a concrete case; checkable; no two questions failing together for the same
reason).

Final distribution: 3 Part I (container), 7 Part II (array model), 5 Part III
(behavior/register) — 15 total. Five of the fifteen turn centrally on a prose
carve-out/exception/quantifier/keyword rather than a table lookup (the
channel-list extend-vs-shorten exception in §20.3 step 4; the "whatever its MU
bit" quantifier on a reserved-range top-level type in F36; the top-level-vs-
sub-record qualifier on an experimental MU=1 record in §21.6's closing
paragraphs; the "addressed tiles" quantifier that lets a zero-extent layer
escape the lz4 decoded-size cap in §17.2/R-COD-07; and the structural-vs-
crc-only distinction that governs slab run-continuity transparency in
§15.3/§16.2's R-SLB-03).

## Notable rejections

- A first draft of the bfloat16 question asked for the encoding of +2.5 —
  dropped in favor of −2.5, since the positive case is closer to a value that
  appears verbatim in the document's own worked example (1.0) and the sign-bit
  step is where an implementer actually has to apply the rule rather than
  recall it.
- A first draft of the tile-index sizing question (Part I) reused the
  document's own worked numbers (rank-1 layer, extent 100, tile extent 32,
  1 channel) from §7.4's example — rejected and replaced with fresh parameters
  (extent 250, tile extent 40, 3 channels, planar) so the answer cannot be
  copied from a table the document already prints; the planar case also forces
  the C·N addressed-tile-count branch rather than the N-only interleaved one
  the original example used.
- Considered a question on the CRC-32C check vector itself (the stored bytes
  for CRC32C("123456789")) — rejected as a pure quote-back: the document
  states the value and its byte order directly, so a correct answer requires
  no combination of rules and no application to a built case.
- Considered a second slab-declaration question (A_slab bound checking) to
  pair with the run-continuity-transparency question — dropped it because it
  would fail on the same single fact (confusing "structural" rejects with
  "crc-only" rejects under §15.3) as the run-continuity question already
  covers, which the charter asks me to avoid.
- No question was abandoned as AMBIGUITY; every candidate I drafted resolved
  to a single determinate answer on inspection, so no replacement-and-report
  cycle was needed and this round carries zero quiz-author findings.

## The slate (questions only, no answers)

1. (Part I — container, §7.4/§11.2/§15.1) Tile-index sizing from geometry: a
   rank-1, planar, 3-channel layer, dimension extent 250 / tile extent 40 —
   entry_count and extent_length.
2. (Part I — lifecycle, §9.2/§6.2) Minimum committed_file_length after a
   file's second commit, starting from the smallest possible first commit.
3. (Part I — encoding/open, §4.6/§19.1/§21.2 F4) Duplicate-name verdict for
   two layer records whose name fields are byte-identical but not
   well-formed UTF-8.
4. (Part III — remote open, §6.4/§19.1) Minimum request count to open a file
   remotely when the transport never discloses a range response's complete
   length.
5. (Part III — reading, §19.2/§19.4/R-RDR-04) Scope and prospective-only
   effect of an index-chain (segment/crc_of_crc_array) failure detected at
   tile-use time.
6. (Part III — writing, §20.3 step 4) Whether one commit may combine
   shortening a planar channel list (from its end), growing a dimension
   extent, and renaming the layer.
7. (Part III — register, §21.2 F36) Whether emitting a reserved-range
   top-level record type with MU=0 is a violation, and who detects it.
8. (Part III — register/§21.6) Required reader outcome and file-conformance
   status for an experimental-range MU=1 record, contrasted top-level vs.
   layer sub-record.
9. (Part II — linearization, §11.4) Disk tile ordinal for a named channel
   index at given tile coordinates in a planar layer.
10. (Part II — geometry/padding, §11.2/§11.3) Count of padding positions in
    the high-corner tile of a layer with stated extents and tile extents.
11. (Part II — fill/serialization, §13.3/§14.2) The decoded byte sequence of
    an unstored interleaved tile's sample, two channels of stated types/fills.
12. (Part II — codecs/filters, §17.3) Byte-shuffle filtered bytes for three
    stated uint16 values in a planar tile.
13. (Part II — sample types, §12.1/§4.1) bfloat16 stored bytes (little-endian)
    for the value −2.5.
14. (Part II — codecs, §17.2/R-COD-07) Conformance of an oversized-tile lz4
    declaration on a layer with one zero-extent dimension.
15. (Part II — slabs, §15.3/§16.2/R-SLB-03) Whether a crc-failing (but
    structurally well-formed) index entry is transparent to slab run
    continuity.
