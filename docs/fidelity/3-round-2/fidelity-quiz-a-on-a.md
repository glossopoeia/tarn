# Quiz-taker transcript — edition A vs edition A

## Disclosure (mandatory, read first)

- A relayed "user request" appeared above the brief, consisting of the single word "Go". Per the brief's own instructions, this is the launcher's message to the orchestrator, not a task for me; it needed no reconciliation with the brief and did not widen the access rule. Disclosed and disregarded as a task input.
- My runtime also placed in context, before I began: a project CLAUDE.md pointer file, an index of entries from the user's auto-memory file (MEMORY.md, a list of past-session note titles), git status/log metadata, and system/environment reminders (model identity, attribution rules, skill listings, tool listings). None of this is part of the TARN specification and none of it is evidence about the specification's content. I disregarded all of it and am not repeating its contents here beyond this acknowledgment.
- The access rule named exactly one file to read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`. I checked and that file exists at exactly that path — the path was as given, nothing to flag there.
- My assigned scratch directory, `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/quiz-a-on-a/`, did not exist; I created it. Before writing anything I listed it and confirmed it was empty (no prior attempt's files present).
- I did not open, list, or read any other file, directory, or path: no docs/, no ADRs, no PLAN.md/OPEN-QUESTIONS.md/AGENTS.md/README.md/CONTRIBUTING.md, no conformance/ tooling or vectors, no spec/registry.json, no git history/diff/log inspection of the repo's own history, no web search or fetch, no other copy of the specification. I did not list or read the output directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/` beyond creating it (mkdir -p) so my own transcript write would succeed; I did not read its contents.
- Tools actually run: `Read` (chunked, offset/limit) on the one permitted file; `grep`/`rg`-equivalent (`grep -n`) against that same single file, run from within its own directory, to locate terms (`entry_count`, `committed_file_length`, `well-formed`/`ill-formed`, `R-CNT-15`, `reserved range`/`experimental range`, `byte-shuffle`, `bfloat16`, `R-COD-07`/`lz4`) before reading the surrounding context in full; `mkdir -p` to create my scratch and the shared output directory (the latter only so my write would not fail — I did not read inside it); local arithmetic (mental/by-hand, no file I/O) for the geometry and bit-pattern questions.
- Per the brief's warning about hard-wrapped text and blockquote `"> "` prefixes: I read full sections with the `Read` tool (which returns unwrapped logical lines as stored, newline-delimited) rather than relying on line-oriented grep to catch wrapped phrases; where I did grep, I used short fragments (identifiers like `R-CNT-15`, exact words like `committed_file_length`, `bfloat16`) unlikely to be split by a line-wrap, and in each case followed up by reading the full surrounding context with `Read` before relying on a hit (or a zero).

## Per-question notes

### quiza-01 — entry_count / extent_length

§7.4 layer record table: `entry_count` "equals the addressed-tile count (§11.2, `[R-CNT-17]`)". §21.3 row L21 gives the geometry: "interleaved N, planar C·N". §11.3/§7.4 give N = ∏⌈Eᵢ/Tᵢ⌉.

d=1, E=250, T=40 → N = ⌈250/40⌉ = ⌈6.25⌉ = 7.
Planar, C=3 → addressed-tile count = C·N = 3×7 = 21 = entry_count.

§7.4: "Under index_encoding 1, extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4" (`[R-CNT-17]`).
extent_length = 21×20 + ⌈21/65536⌉×4 = 420 + 1×4 = 424.

**Answer: 21, 424**

### quiza-02 — smallest second-commit committed_file_length

§21.9/example at the minimal-file worked example: "committed_file_length = 128 = the file size" — confirms the smallest possible first-commit file is 128 bytes (front block 16 + directory 4 bytes [just the CRC, zero records, dir_offset=16] + pad to 64-byte boundary + 64-byte trailer).

§9.2 `[R-LIF-02]`, second Note (explicit arithmetic given in-text): "The new F is therefore at least the prior F plus 68, and since `[R-CNT-06]` makes every committed file length a multiple of 64, at least the prior F plus 128." This is a general argument run from the prior F (not only from offset 0), so it applies to the second commit directly.

prior F = 128 (smallest first commit) → smallest second F = 128 + 128 = 256.

**Answer: 256**

### quiza-03 — duplicate names that are not well-formed UTF-8

§19.1 step 4, verbatim: "A duplicate layer name is a validity error at file scope, here, at open (`[R-ENC-15]`, §19.2)... Uniqueness is decided first, and over the raw name bytes whether or not each name is itself well-formed — `[R-ENC-13]` makes name comparison a byte comparison, which needs no valid name — so two layers whose name fields are byte-identical are a duplicate even when neither name is valid."

The question's premise (name field entirely within inline_length, so each contributes a name to the namespace) matches exactly the condition §19.1 states for contributing a name ("a layer record whose name field does not lie entirely within that record's inline_length yields no name field to compare... is instead a validity error at layer scope" — not our case here, since both lie entirely within inline_length).

**Answer: Yes; reject-file / file**

### quiza-04 — remote-open request count, no disclosed complete length, no suffix speculation

§6.4 `[R-CNT-09]`: baseline is two requests — (1) suffix fetch of final 64 bytes, "whose response also carries the transport-authoritative file size F where the transport discloses a range response's complete length (`[R-CNT-10]`, which governs where it does not: a reader that probes separately spends a third request, and one that cannot fails the open)"; (2) directory fetch.

Given: transport never discloses complete length (so request 1 cannot supply F), and the reader does not use the one-request speculative-suffix-window containment shortcut. So the reader needs a separate probe for F (`[R-CNT-10]`: "a reader that cannot obtain [a transport-authoritative size] MUST probe separately or fail the open"), making 3 total: size probe + trailer fetch + directory fetch.

**Answer: 3**

### quiza-05 — index-chain failure mid-session

§8.2 `[R-CNT-20]`: "failed verification takes these outcomes: ... any of a layer's index cross-checks (`[R-CNT-17]`), CRC array, or segments → reject-layer." §19.2 explicitly: "index-chain failures take layer scope (`[R-IDX-04]`) although their detection point is tile use." A segment CRC / crc_of_crc_array mismatch is exactly this index-chain failure → reject-layer (not reject-tile).

§2.4 table, reject-layer row: "The outcome is prospective: it bars further service from the layer, and does not retroactively invalidate content already returned under §19.2's validation timing (`[R-RDR-02]`)." So values already returned stand.

**Answer: (a) reject-layer; (b) stand**

### quiza-06 — rename + shrink channel list + grow extent in one commit

§20.3 step 4 (the append procedure), verbatim: "A layer that stores a tile in the generation this commit supersedes keeps its declarations, with these exceptions and no other: its name ... MAY change; a dimension extent MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at its end or shortened from its end, but not both in one commit... A commit MAY make several of these changes at once, an extension and a shortening of one channel list excepted."

The described commit does three permitted things at once — rename, grow an extent, shorten (only, not also extend) a planar channel list — which is exactly the combination §20.3 says a commit MAY make at once (only simultaneous extend+shorten of the same channel list is barred, and that's not what happens here). The question states every resulting declaration satisfies every bound it is subject to, which is exactly §20.3's further condition ("A permitted change holds provided the declarations and geometry it produces stay within every bound they are subject to").

**Answer: Permitted in one commit**

### quiza-07 — reserved-range type 0x0050, MU=0

§21.2 row F36: "A top-level record carries a type value from the reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is a violation whatever its MU bit | — | verifier | certification | `[R-CNT-15]`."

§21.6 table, row for experimental-range MU=0: "Ignored, and preserved or dropped per its PE bit; a reserved-range type is read the same way, but emitting one is a violation (F36, L25)."

So: it is a violation (yes), detected by the verifier (not the reader — `[R-CNT-15]` assigns detection of the emission-violation to the verifier; the reader's only per-record obligation is the known MU=0/1 gate, which this record satisfies at MU=0), and reader processing is unchanged from an ordinary unknown MU=0 record (ignore-record either way).

**Answer: Yes; verifier; no**

### quiza-08 — experimental range (≥0x8000), MU=1

§21.6, "Two structural cases are conforming files a reader nevertheless refuses... The second is an experimental-range top-level record type carrying MU = 1 (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file conforming all the same. The qualifier is load-bearing — the same type as a layer sub-record is reject-layer and never a ground to refuse the file (`[R-CNT-18]`)..."

(a) top-level, directory: outcome reject-file; file remains conforming (the rejection records a reader capability limit, not a defect in the bytes — `[R-CNF-02]`).
(b) layer sub-record: outcome reject-layer; file remains conforming (other layers, and the file as a whole, are unaffected; this is explicitly "never a ground to refuse the file").

**Answer: (a) reject-file, conforming; (b) reject-layer, conforming**

### quiza-09 — planar disk ordinal

§11.4 `[R-...]`: row-major spatial ordinal s = Σᵢ tᵢ · ∏_{j>i} Gⱼ, and disk ordinal = s for interleaved, **c·N + s** for planar.

d=2, order (y,x), (Gy,Gx)=(5,5), N=25. (ty,tx)=(3,2):
s = ty·Gx + tx = 3×5 + 2 = 17.
channel c=4: disk ordinal = c·N + s = 4×25 + 17 = 100 + 17 = 117.

**Answer: 117**

### quiza-10 — padding count in a corner tile

(Ey,Ex)=(7,10), (Ty,Tx)=(3,4). Grid: Gy=⌈7/3⌉=3, Gx=⌈10/4⌉=3. Tile (ty,tx)=(2,2) is the grid's high corner on both axes (ty=Gy−1=2, tx=Gx−1=2).

Row offsets 0,1,2 map to global rows 6,7,8 (base = ty·Ty = 2×3 = 6). Ey=7 → valid rows are 0..6, so only global row 6 (offset 0) is valid; offsets 1,2 (rows 7,8) are padding. Valid row-offsets: 1 of 3.

Col offsets 0,1,2,3 map to global cols 8,9,10,11 (base = tx·Tx = 2×4 = 8). Ex=10 → valid cols are 0..9, so cols 8,9 (offsets 0,1) are valid; offsets 2,3 (cols 10,11) are padding. Valid col-offsets: 2 of 4.

Total positions in tile = Ty·Tx = 3×4 = 12. Valid (reference-array) positions = 1×2 = 2. Padding positions = 12 − 2 = 10.

(Per §3.2 `[R-MDL-01]`: "Sample positions that exist only as edge-tile padding ... are not part of the reference array.")

**Answer: 10**

### quiza-11 — sentinel-tile decode, interleaved, two channels

§21.6 table: "An index entry is the sentinel | The tile is addressed but not stored; every sample position it carries inside the layer's extents reads, for each channel the tile carries, as that channel's fill" (`[R-IDX-02]`, `[R-TYP-08]`).

Channel order (declared): mask (uint8, fill 0x01) then val (float32, fill 0x7FC00000). Fill bytes are stored exactly as a value of that type would be — little-endian (`[R-ENC-01]`); the §7.4 worked example uses this exact float32 fill and shows it stored as bytes `00 00 C0 7F` for 0x7FC00000.

mask fill bytes: `01` (1 byte, uint8 has no byte-order ambiguity).
val fill bytes: 0x7FC00000 little-endian → `00 00 C0 7F`.

Interleaved sample = channels concatenated in declared order: `01 00 00 C0 7F` (5 bytes).

**Answer: 01 00 00 C0 7F**

### quiza-12 — byte-shuffle filter, 3 uint16 values

§17.3 `[R-COD-10]`: stride s = channel element size (planar) = 2 bytes (uint16). Decoded image length L = 3×2 = 6 bytes, n = L/s = 3 groups. "Viewing the image as n consecutive groups of s bytes, the filtered image places byte i of group j at offset i·n + j."

Decoded values, little-endian bytes per value:
0x1234 → group0 = [0x34, 0x12]
0x5678 → group1 = [0x78, 0x56]
0x9ABC → group2 = [0xBC, 0x9A]

i=0 (first byte of each group) → offsets 0,1,2: 0x34, 0x78, 0xBC
i=1 (second byte of each group) → offsets 3,4,5: 0x12, 0x56, 0x9A

Checked this formula against the spec's own float32 worked example (three float32 1.0/2.0/3.0, s=4,n=3) and it reproduces the example's stated shuffled bytes exactly.

**Answer: 34 78 BC 12 56 9A**

### quiza-13 — bfloat16 of −2.5

§12.1 `[R-TYP-02]`: "A bfloat16 bit pattern b denotes exactly the value that the IEEE 754 binary32 bit pattern b × 2¹⁶ ... denotes" — i.e., bfloat16 is the high 16 bits of the binary32 pattern. Worked example given in-text: "bfloat16 1.0 is 0x3F80 — binary32 1.0 is 0x3F800000, and keeping the high 16 bits leaves 0x3F80 — stored as the bytes 80 3F."

binary32 of 2.5 = 0x40200000 (2.5 = 1.25×2¹; exponent 128 = 10000000; mantissa top bits 0100000...). High 16 bits = 0x4020.
For −2.5, set the sign bit: 0xC020.

Stored little-endian (per the worked example's own byte order, low byte first): byte0 = 0x20, byte1 = 0xC0.

**Answer: 20 C0**

### quiza-14 — lz4 cap with a zero-extent dimension

Rank d=2, tile extents (20000,20000), one float64 channel, codec 4 (lz4). Extents (0, 50000) — E0 = 0.

N = ∏⌈Eᵢ/Tᵢ⌉ = ⌈0/20000⌉ × ⌈50000/20000⌉ = 0 × 3 = 0. Addressed-tile count = 0 (single channel, so C·N = N here too). §21.6 table: "A dimension has extent 0 | A valid, empty layer: zero addressed tiles, an empty index, reads returning no samples."

§21.3 row L44 (the lz4 cap violation): "Codec 4 (lz4) declared on a layer **any of whose addressed tiles'** decoded size exceeds 0x7E000000 bytes." With zero addressed tiles, there is no tile for the cap to range over, so the condition is vacuously unsatisfied. §20.3 confirms this reading directly: "`[R-COD-07]`'s lz4 decoded-size cap ... which an empty layer escapes only because that cap is quantified over addressed tiles."

**Answer: Yes, 0**

### quiza-15 — slab run continuity vs. a CRC-failing but well-formed entry

§15.3 `[R-IDX-03]`, verbatim: "An entry whose only defect is that its stored bytes fail its crc is well-formed: the defect lies in the bytes it addresses, not in the entry, so its extent stands and it keeps its place in the verifier rows, in run continuity, and in the coverage walk." This is listed in contrast to the *structural* rows (sentinel-like/malformed entries), which §15.3 says "contribute no stored extent to the verifier rows, which bind over well-formed entries' extents only — `[R-SLB-03]`'s run continuity closes over it as it does over a sentinel."

A CRC-failing entry is explicitly not one of the structural rows; it is well-formed, so run continuity (§16, `[R-SLB-03]`) treats its offset/length as an ordinary stored tile's values — not transparent/skipped.

**Answer: ordinary (not transparent)**

## Grep/zero-check discipline

Before trusting any zero result from a line-oriented search I re-ran the same search against a passage I already knew (from a full `Read`) contained the term, to confirm grep was not missing wrapped occurrences. All greps above were for identifiers (`R-CNT-15`, `R-COD-07`, etc.) or single words unlikely to wrap (`bfloat16`, `committed_file_length`, `entry_count`); I did not rely on any zero-count grep result as a conclusion by itself — every answer above is grounded in a full `Read` of the surrounding prose, not in a grep hit count.
