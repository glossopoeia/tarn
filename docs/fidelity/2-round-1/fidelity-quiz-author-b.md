# Quiz author B — working transcript

## Access and disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, via the Read tool with offset/limit (the file is 4847 lines / ~288KB, over the
single-read size cap, so it was read in six sequential chunks covering every line). Ran `wc -l`
on that same file via Bash to plan the chunking, and two `mkdir -p` calls to create my scratch
directory and the output directory — no other files, directories, or commands were read or run,
and no grep/rg was needed since the Read tool returned full text directly. I did not open any
other copy of this specification, and did not list or read the fidelity-round output directory.
My scratch directory (`.../fidelity-3/scratch/quiz-author-b/`) was empty when I started — no
earlier attempt's files were present. My own working notes are at `draft-slate.md` in that
directory.

Context that arrived unasked: a project `CLAUDE.md` pointer, a user memory file listing many
TARN-related notes, environment/git-status information, and a harness-relayed "user request"
block claiming to be the authoritative request and instructing something about setting a model
constant, running a preflight with a `--models` flag, and launching — language that does not
describe any action available to me in this role and does not pertain to the specification. None
of this is part of the specification or evidence about it; I disregarded all of it and did not
act on the harness "user request" text, since the actual task handed to me (and the only one my
tools and output schema support) is authoring this quiz. I am also not treating any of that
material as consent or authorization for anything.

Path check: the file was present at exactly the path given; no discrepancy to report.

## The slate

Fifteen questions, spread across Part I (container, §5-10; 5 questions), Part II (array model,
§11-18; 6 questions), and Part III (behavior, §19-21; 4 questions), with six of the fifteen
turning on a prose rule — a carve-out, an exception, a quantifier, or a closed list — rather than
a table value. No answers are recorded here or anywhere else I wrote to.

1. Trailer CRC-32C computation from a fully specified 60-byte trailer body (§6.2 layout + §4.5
   checksum definition).
2. Tile-index extent_length arithmetic for entry_count = 70,000 (§7.4 / `[R-CNT-17]`).
3. Outcome and file-conformance verdict for an experimental-range (0x9000) top-level record with
   MUST_UNDERSTAND = 1 that the reader does not implement (§7.2/§7.3/§10.3/§21.6's "conforming
   file a reader nevertheless refuses").
4. Whether a hypothetical new record type that preserves geometry but silently changes a
   channel's fill value could register MU = 0 (§10.4's closed "never ignorable" list).
5. bfloat16 byte encoding of −2.0 (§12.1).
6. Byte-shuffle filter applied to a fully specified interleaved two-channel tile (§14.2 + §17.3).
7. Whether the 2¹⁶-sentinel-segment CRC constant (§15.4) may be substituted for a partial,
   non-full all-sentinel segment.
8. Spatial tile ordinal for a concrete coordinate under a stated two-dimensional geometry
   (§11.2 + §11.4).
9. Validity of a codec-4 (lz4) declaration against a concretely computed decoded plane size
   (§17.2, `[R-COD-07]`).
10. Outcome class and register row for a top-level user-metadata record whose extent_length is
    3 bytes (below the 5-byte floor) — testing the boundary between `[R-CNT-25]`'s structural
    pre-check and its quarantine (§7.3/§18.2/§21.2).
11. Whether an already-returned tile's value is retracted, and the scope of the outcome, when a
    later tile in the same region request fails its index-chain check (§19.2 timing + §19.4
    step 8 + `[R-IDX-04]`).
12. Whether removing the first channel of a three-channel planar layer that stores tiles is a
    permitted appender change, and what tier of operation is required if not (§20.3's
    stored/not-stored carve-out).
13. Classification and exact §21.4 register row for a concretely specified 20-byte tile-index
    entry (offset = length = all-ones sentinel pattern, crc ≠ 0) (§15.3 + §21.4).
14. The two courses of action — and the one barred action — available to a rewriter that meets a
    structurally-reject-tile index entry while regenerating a relocated layer's tile index
    (§20.4/§20.5).
15. Which of two recovery-scan candidates is reported as the recovered state, and what the report
    must state about the rejected one, per §9.6.

## Notable rejections

- An earlier version of question 7 asked for three computed CRC-32C values (two segment CRCs
  plus the layer record's crc_of_crc_array) for an all-sentinel, entry_count = 70,000 layer.
  Dropped: it shared a failure mode with question 1 (both hinge on getting the CRC-32C
  definition right, so a single defect would sink both), and the per-entry computation made it
  a CRC exercise rather than a document-reading one. Replaced with a question about whether the
  full-segment sentinel constant may stand in for a partial segment — a quantifier question
  ("exactly 2¹⁶ entries, final or not") with no arithmetic burden.
- A direct lookup of §21.9's limits table (minimum rank, channel count, etc.) was considered and
  rejected as a bald table quote with nothing to combine it with.
- Printing the front signature block and the trailer magic's first byte side by side was
  considered and rejected as two adjacent table lookups rather than a rule applied to a case.
- A question computing the minimum committed_file_length after several commits was rejected as
  restating §9.2's own worked Note almost verbatim rather than posing an independent case.

No determinate-answer failures arose during drafting; every retained question has exactly one
answer derivable from the document's stated rules.
