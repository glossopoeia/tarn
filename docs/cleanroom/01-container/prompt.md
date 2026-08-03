# Cleanroom round 1 — container spine (prompt record)

Run against `spec/tarn.md` as of the Batch 3 container text (pilot: run
after Batch 3, before Batch 4, so §15/§16 were still reserved; the
index-facing half of the nominal round-1 scope folds into round 2).

**Access rule given to every agent:** read `spec/tarn.md` and nothing
else — no other repository files, no version control history, no web.
Every conclusion must cite section numbers and requirement IDs. Where
the text under-determines, record an AMBIGUITY (location, the readings
permitted, the pick and why); where it contradicts itself, a
CONTRADICTION with both citations; effort-disproportionate but
decidable points are OBSERVATIONS. Reserved sections are not defects,
but unresolvable forward references into them are reportable.

**Four charters, run independently and in parallel:**

1. **Reader** — describe a conforming container reader byte-precisely:
   local open; remote open (exact Range headers for a 10,000,000-byte
   file, baseline and speculative variants, all obliged transport edge
   cases); degradation walkthroughs (bad directory CRC, malformed
   extent slot, unimplemented codec value); confirm or refute
   codec-free implementability.
2. **Verifier** — the full certification procedure; the byte-coverage
   walk (generation enumeration, attribution, claimed sets); a worked
   generation-3 trace (superseded tile + retag) classifying every
   region; what the text leaves undecidable.
3. **Writer** — create a minimal one-layer file (complete byte layout,
   every undetermined byte named); append a second layer (every byte,
   barriers, generation-2 trailer); torn-append recovery obligations
   and prohibitions; catalog of legitimate byte divergence between
   conforming writers.
4. **Quiz** — fifteen byte-level questions with citations and
   per-answer confidence, graded against an answer key derived
   independently from the spec (minimum-file bytes; request ranges and
   largest conforming dir_offset; generation 0; unknown major;
   transport-size mismatch; stored-flag mismatch on a known type;
   planar entry-count/extent arithmetic; duplicate names; CRC
   coverage; locating a prior generation's directory; zero-layer
   validity; index/user-metadata codec scoping; front-block
   corruption local vs remote; the 92-byte-gap two-actor split;
   validation-order rationale).

Verbatim outputs: `transcript-reader.md`, `transcript-verifier.md`,
`transcript-writer.md`, `transcript-quiz.md`. Consolidated results and
disposition of every finding: `findings.md`.
