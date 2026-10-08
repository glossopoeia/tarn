# Quiz-author transcript — edition A

## Disclosure

- Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4,981 lines / ~295 KB), in full, via five sequential `Read` calls (offset/limit chunks: 1-1000, 1001-2000, 2001-3000, 3001-3650, 3651-4981). No other project file was opened.
- Ran `wc -l` on that same file to plan chunk boundaries, and `ls -la` once on its containing directory (`.../editions/a/`) and once on my own scratch directory — both only to confirm the single file's presence/size and that my scratch directory was empty before starting. Neither listing reached outside those two directories (no sibling `editions/b`, no `docs/`, no repo root). This is the one minor deviation from "do not list directories": disclosed, not acted on beyond confirming the one permitted file.
- My scratch directory (`/private/tmp/claude-501/.../fidelity-3/scratch/quiz-author-a/`) was empty when I started (only `.`/`..`).
- Ran local Python-only arithmetic (no file I/O) to verify the numeric answers behind five of the questions before finalizing them (grid-ordinal arithmetic, index-region byte arithmetic, packed-boolean-plane bit arithmetic). No prior knowledge of another array/image format was used to settle anything — only this document's own stated rules.
- Context that arrived unasked and was disregarded as non-evidence about the specification: a project `CLAUDE.md` pointer, a user memory-file index (file names referencing a "TARN harness" and related process notes), environment/session metadata (user email, git branch/status/recent-commit-subjects), and a "workflow harness — user request" line instructing me to "set the constant to claude-sonnet-5, preflight with --models, then launch." That last item does not match this task's charter or tools (I have no such constant, preflight flag, or launch action available, and it is unrelated to authoring a quiz from one document) and was treated as unrelated/injected content, not acted on. None of this material was used to write, select, or justify any question below.
- The path handed to me matched the brief exactly (`.../editions/a/tarn.md`); no discrepancy to report there.

## Notable rejections

- Rejected a direct restatement of §4.6's own NFC/NFD worked example (`température`) — too close to quoting the text's worked example back; replaced with a question about byte-identical-but-invalid names and the §19.1 clarification that duplicate-detection runs over raw bytes "whether or not each name is itself well-formed" (a different, less obvious clause).
- Rejected a direct restatement of §11.4's own worked example (tile (1,2), spatial ordinal 10, disk ordinal 74) — that is the document's own numbers; replaced with fresh grid dimensions, channel index, and tile coordinates, and extended it to require locating the entry's byte range in the index region (combining §11.4 with §15.1), and a second question reusing similar notation but testing the *renumbering-on-growth* rule from §20.3 step 4 instead.
- Rejected a question asking only "what is CRC-32C of the empty byte string" (Appendix A trivia) — single fact, no rule combination, fails the "lazy / quotes a table back" bar.
- Considered but dropped a question about `tarn.stats`/`tarn.axes` placement, since every outcome there is "ignored, document stays conforming" regardless of the scenario specifics — too easy to get right by a blanket "metadata never matters" heuristic rather than genuine rule-tracing.
- No question was abandoned for lack of a determinate answer; no AMBIGUITY findings resulted.

## The slate (questions only — no answers recorded)

1. **[Part I — container]** Trailer gate ordering / F17. (see structured output for exact wording)
2. **[Part I — container, prose]** Top-level user-metadata record, malformed extent slot vs. the quarantine's precedence.
3. **[Part I — container, prose]** Rewriter's obligation on an unknown ignore-lane trailer flag bit.
4. **[Part I — container, prose]** Extent slot (0, 500): disambiguating F30 from F31/F33.
5. **[Part II — array model]** `extent_length` arithmetic for a planar layer with a 7,000,000-entry index.
6. **[Part II — array model, prose]** lz4 decoded-size cap: the zero-addressed-tile escape and what ends it.
7. **[Part II — array model]** Packed boolean plane: exact two-byte decoded image combining grid overhang, bit packing, and pad-bit fill.
8. **[Part II — array model]** Disk ordinal and tile-index entry byte range for a planar layer (fresh grid/channel numbers).
9. **[Part II — array model, prose]** Slab run continuity: an entry whose only defect is a failed stored-bytes CRC is not "transparent" like a sentinel.
10. **[Part III — behavior, prose]** Prospective-only bar: already-returned tile values in a region read survive a later index-chain failure on a sibling tile.
11. **[Part III — behavior]** Disk-ordinal renumbering under an appender's dimension-growth commit.
12. **[Part III — behavior]** Register-row match: T6 vs. T7 for a specific stored entry.
13. **[Part III — behavior, prose]** Rewriter facing a structurally-malformed index entry while regenerating a relocated region: no repair path exists.
14. **[Part I — container, prose]** `index_encoding` reserved (0x50) vs. experimental (0x90): same register row, no special carve-out (unlike record types).
15. **[Part III — behavior, prose]** Minimum guarantee (2^32 entries) vs. a hard limit: file stays conforming; a capability decline must be reported as a resource limit, never as corruption.

Full question text, section citations, answer form, and rationale for each are in the structured result returned alongside this transcript (not duplicated here to avoid drift between two copies).
