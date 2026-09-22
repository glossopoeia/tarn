# Quiz transcript — quiz-a-on-b (edition B)

## Disclosure

- Scratch directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/quiz-a-on-b/` was empty when I began (no prior attempt's files were present).
- I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md`, in full, via the Read tool in six sequential chunks covering all 4977 lines / 302,125 bytes. I did not open any other file, any other copy of this specification, or any directory listing other than my own scratch directory (created and checked with `mkdir -p` / `ls -la`, which was empty).
- I ran `wc -l` and `wc -c` against that same one file (and no other) purely to learn its line/byte extent before deciding how to chunk my reads; I performed no grep/rg searches this round, since reading the file directly in full-content chunks let me see every byte without the hard-wrap risk that a line-oriented grep would carry.
- I did not read docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md, conformance/, spec/registry.json, git history, or any other project file. I did not web search or web fetch.
- My runtime placed material in context before I began that I did not ask for and that is not part of the specification: a project CLAUDE.md pointer, a user memory index of prior-round notes (titled things like "TARN harness spec path", "TARN lineage gate word list", etc.), a git-status block naming recent commit subjects (including ADR-0133 and ADR-0132 commits), an attribution/footer instruction block, a skills listing, and an environment/model block. I disregarded all of it as non-evidence about the specification's content and am not repeating its contents here beyond naming that it appeared.
- The file I was pointed to was present at exactly the stated path and of the stated general shape (a full TARN format specification draft); I have no basis to say the path was wrong.
- All answers below are cited to edition B's own section numbers, requirement IDs, and register rows, and all arithmetic is shown.

## Working notes per question

### quiza-01
Front block [0,16). User-metadata record: header 24 bytes + inline_length 1 byte = 25 bytes (record framing, §7.2: "Each record is a 24-byte header followed by inline_length bytes of inline payload"). Extent placed at the smallest legal offset, 16 (extent_offset ≥ 16 per the extent-slot rule, §7.2 `[R-CNT-13]`), extent_length = 5 (the given minimum: "one whose extent_length is less than 5 — too short to hold both a document and the terminal CRC-32C ... in its final 4 bytes — is a validity error", §7.1). Extent occupies [16,21).
Directory placed immediately after (dir_offset = 21, per the question's stipulation). Directory region = record sequence (25 bytes, one record) + 4-byte CRC = 29 bytes (dir_length ≥ 4 is satisfied exactly, no slack inside the directory: "dir_length as small as the record framing allows"). Directory occupies [21,50).
Pre-trailer pad: trailer must start at a 64-aligned offset F−64, and F must be a multiple of 64 (§6.2). Smallest F with F−64 ≥ 50 and F a multiple of 64 is F = 128 (F−64 = 64 ≥ 50). Pad = 64 − 50 = 14 bytes — the shortest legal pad (`[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary").
Total: front(16) + extent(5) + directory(29) + pad(14) + trailer(64) = 128 bytes.
This also respects the 128-byte floor of `[R-CNT-27]`.

**Answer: 128**

### quiza-02
§2.3: "A file whose version_major is 0 declares no major at all (§6.3): it is not a file declaring a format major other than 1, no reach question arises for it, and `[R-CNT-07]` rejects it (§21.2, F18)."

**Answer: no; reject-file, F18**

### quiza-03
§6.3 `[R-CNT-08]`: "An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT set any other: no writer under this text originates an ignore-lane bit..." Bit 20 must be carried forward as 1; bit 25 (currently 0, unset) may not additionally be set by the appender.

**Answer: (a) 1; (b) not permitted**

### quiza-04
Creation minimum is 128 bytes (§5.1 example / `[R-CNT-27]`). §9.2's note on `[R-LIF-02]` step 5: "The new F is therefore at least the prior F plus 68, and since `[R-CNT-06]` makes every committed file length a multiple of 64, at least the prior F plus 128." 128 + 128 = 256. Verified by direct construction: second commit begins at F=128, appends an (unchanged, still-empty) directory of 4 bytes at [128,132), needs trailer start (F′−64) ≥ 132 and F′ a multiple of 64 ⇒ smallest F′ = 256 (pad = 192−132 = 60).

**Answer: 256**

### quiza-05
§21.2, F30: "A non-layer top-level record's extent slot has exactly one half zero (offset 0 with length != 0, or offset != 0 with length 0)." extent_offset=0, extent_length=40≠0 matches exactly. F33's note confirms: "a record extent slot of (0, N) with N nonzero reaches the block through its zero offset and is theirs [F30's] rather than F31's." F31 requires a *nonzero* extent_offset in 1–15, which does not apply here.

**Answer: F30; reject-file**

### quiza-06
§20.3 step 4: a layer that "stores a tile in the generation this commit supersedes keeps its declarations, with these exceptions and no other" (name changes, extent growth, channel-list extend/shorten at the end, slab/alignment changes) — "Every other declaration is fixed for as long as the layer stores a tile: ... every channel's type and fill ... A commit MUST NOT change one of these; the change is a new layer, or a rewrite that re-declares it under a fresh file_id." Crucially: "The tense is the prior generation's ... so a commit does not earn an empty layer's freedom by emptying the layer as it re-declares it: a layer that stored a tile keeps its declarations through the commit that empties it." Since the layer stored a tile in generation N (the superseded generation), the fill-value change in the very commit that empties it is barred from being an appender operation.

**Answer: requires declaring a new layer or performing a whole-file rewrite (not a valid appender commit)**

### quiza-07
§11.2: G_y = ⌈1200/300⌉ = 4; G_x = ⌈2000/250⌉ = 8; N = 4×8 = 32. Interleaved layer ⇒ one block [0, N) = [0,32) (§16.2 `[R-SLB-02]`). "Run r of a block starts at ordinal block_start + r·S." Run 2 (0-based): start = 0 + 2×5 = 10.

**Answer: 10**

### quiza-08
Value sequence (interleaved, sample-major, C=2, §14.1): k=0 → x@pos0; k=1 → y@pos0; k=2 → x@pos1; k=3 → y@pos1.
Bytes: x0=0x01020304 LE → 04 03 02 01; y0=0xAA → AA; x1=0x05060708 LE → 08 07 06 05; y1=0xBB → BB.
Decoded image (10 bytes): 04 03 02 01 AA 08 07 06 05 BB.
Byte-shuffle (§17.3): stride s = Q (sample stride) = Bx+By = 4+1 = 5. n = L/s = 10/5 = 2. Groups of 5: group0 = [04,03,02,01,AA]; group1 = [08,07,06,05,BB]. Filtered placement: byte i of group j → offset i·n+j (n=2):
i=0: 04→0, 08→1
i=1: 03→2, 07→3
i=2: 02→4, 06→5
i=3: 01→6, 05→7
i=4: AA→8, BB→9
Filtered/stored bytes (codec 1 = none, so stored bytes = filtered image verbatim): 04 08 03 07 02 06 01 05 AA BB.

**Answer: 04 08 03 07 02 06 01 05 AA BB**

### quiza-09
§11.2: addressed-tile count for a planar layer = C·N = 3 × 70,000 = 210,000 = entry_count (§7.4: "entry_count | u64 | equals the addressed-tile count").
Region length, `[R-CNT-17]`: entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 = 210,000×20 + ⌈210,000/65,536⌉×4 = 4,200,000 + ⌈3.204...⌉×4 = 4,200,000 + 4×4 = 4,200,000 + 16 = 4,200,016.

**Answer: 210,000; 4,200,016**

### quiza-10
`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes — the block format's practical interoperability bound; in a planar layer each channel's plane carries its own decoded size (§14.2, §14.3), and the largest governs."
0x7E000000 = 126 × 16,777,216 = 2,113,929,216 bytes.
Channel a's plane (float64) is 2,400,000,000 bytes, which exceeds 2,113,929,216. The largest plane governs, so the cap is exceeded regardless of channel b's smaller size.

**Answer: no**

### quiza-11
§2.4, reject-layer row: "The outcome is prospective: it bars further service from the layer, and does not retroactively invalidate content already returned under §19.2's validation timing." §19.4 `[R-RDR-04]`: "the bar is prospective, so values the reader has already returned under §19.2's timing stand." The index-chain failure (`[R-IDX-04]`) takes layer scope and "bars the request's remaining entries and all further service from the layer."

**Answer: (a) no; (b) barred (reject-layer)**

### quiza-12
§7.2 `[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a reader or updater encountering it MUST treat the record as PE = 1 (never silently deletable). Both writer violations make the file nonconforming (`[R-CNF-05]`) while leaving conforming behavior unchanged, so their detection is a verifier's: a verifier MUST treat a nonzero reserved flag bit or the MU = 1 with PE = 0 combination as a validity error at the record's governing scope." So: detection duty falls on the verifier (not the reader); independent of detection, any reader/updater must treat PE as 1 for drop-eligibility purposes.

**Answer: verifier; 1**

### quiza-13
§20.5: "Regenerating a region means classifying every entry in it... An entry §15.3 classifies reject-tile on a structural ground is neither [a sentinel nor a well-formed stored entry] — `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so regenerating the region cannot proceed without meeting it, and the violation is thereafter one the rewriter has detected. `[R-WRT-06]` then leaves it two disposals, since it can neither reproduce the entry nor invent a replacement: drop the layer, which §20.4's table licenses and whose loss the rewriter SHOULD report as that table says, or refuse."
Refusing means the rewrite does not happen, so nothing is reclaimed; dropping the layer is the disposal under which the rewrite proceeds and slack is reclaimed (§20.5's compaction discussion: "a rewrite that drops the layer (§20.5) reclaiming what the commit would strand").

**Answer: drop the layer; refuse (to rewrite the file) — dropping the layer is the one that reclaims the layer's slack**

### quiza-14
File X: valid magic, valid preceding length gates, but trailer CRC mismatch at [60,64) vs [0,60) ⇒ §21.2, F14: "The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes [0,60)" — detector reader, governing `[R-CNT-06]`.
File Y: correct CRC but dir_offset = 10 < 16 ⇒ §21.2, F9: "Trailer dir_offset is less than 16, pointing the directory into or before the front signature block" — detector reader, governing `[R-CNT-06]`.

**Answer: X: F14; Y: F9**

### quiza-15
`[R-CNF-11]`: "A verifier MAY stop at the first violation it finds; one that does MUST report each scope it did not examine as *unexamined*, which is not a finding that the scope is clean. *Unexamined* is neither a verdict nor *cannot establish* — it constrains the report, not the verdict."

**Answer: unexamined; no**
