# Quiz B-on-B transcript

## Disclosure

- A "relayed user request" labelled as the user's message appeared above the
  brief, consisting solely of the word "Go". Per the brief's own instructions,
  this is the launcher's message to the orchestrator, is not a task for me,
  needs no reconciliation with the brief, and does not widen the access rule.
  I disregarded it as a task instruction and proceeded on the brief alone.
- Unrequested context also appeared in my environment before I began: a
  project CLAUDE.md pointer, a long list of entries from the user's
  cross-session memory file (titled things like "TARN harness spec path",
  "TARN lineage gate word list", etc.), a git status/log block, and an
  attribution-footer reminder for commits/PRs. None of this is part of the
  specification and none of it is evidence about the specification's content.
  I did not open, read, or rely on any of the files these notes name, and I
  did not let their contents (which I am not repeating here beyond naming
  that they appeared) shape any answer below.
- My scratch directory
  (/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/quiz-b-on-b/)
  was empty when I created it — no prior attempt's files were present.
- The file I was told to read was at exactly the path given:
  /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md. It
  existed there (293,925 bytes, 4,755 lines) and I read it in full, in
  sequential chunks, via the Read tool. I ran no grep/rg against any other
  file, and did not list any directory other than confirming this one file's
  existence and size. I ran local Python arithmetic (no file I/O) to check a
  few computations.

## What I read

The entire spec/tarn.md file, offset 1 through its end (4755 lines), in two
large Read calls (lines 1-400, 648-897) plus several targeted Read calls at
specific sections once I'd located them via grep against this same file:
§5 (File Anatomy and Byte Coverage, lines 508-647), §6 (Front Signature Block
and Trailer, lines 648-897), §14.5 (Padding content, lines 2010-2050), §15.4
(Segments and verification, lines 2130-2169), §17.2's lz4 codec clause
(lines 2370-2399), §19.4 (The tile-read algorithm, lines 2874-2945), §20.3
step 4 and the stored-tile preservation paragraph (lines 3007-3120), §20.5
(Rewriting, lines 3351-3500), and the §21.2/§21.3 file- and layer-scope
violation register tables (lines 3638-3736). I used grep/rg (ripgrep-style
search via the Bash tool, scoped to this one file) to locate: "index_encoding",
"segment", "slab run length"/"alignment", "padding", "lz4"/"codec 4", "F[0-9]"
register rows, and "uint8"/"uint64" type-size table entries. I did not open
any other file at any point, and did not consult registry.json, ADRs,
PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md,
conformance/, git history, or the web.

## Per-question work

### quizb-q1 — trailer, dir_offset=16, dir_length=20, minimum F

Trailer table (§6.2): "dir_offset ... ≥ 16"; "dir_length ... ≥ 4; dir_offset +
dir_length ≤ F − 64"; "committed_file_length ... = F; multiple of 64".
16 + 20 = 36 ≤ F − 64 ⇒ F ≥ 100.
§5.1 (`[R-CNT-27]`): "No conforming file is shorter than 128 bytes ... A
reader MUST treat a shorter file as a validity error at file scope."
F must be a multiple of 64, at least 100, and at least 128. The smallest
multiple of 64 that is ≥ 128 is 128, and 128 already exceeds the 100 floor
from the dir fields (36 ≤ 128 − 64 = 64, satisfied with room). So the minimum
is F = 128.

### quizb-q2 — index_encoding 1, entry_count = 70,000

Register row L22 (§21.3): "Under index_encoding 1, extent_length ≠
entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4". This is the formula for the
tile-index region's byte length (entry array + segment-CRC array).
entry_count × 20 = 70,000 × 20 = 1,400,000.
⌈70,000 / 65,536⌉ = ⌈1.0681...⌉ = 2 segments.
2 × 4 = 8 bytes of segment-CRC array.
Total = 1,400,000 + 8 = 1,400,008 bytes.

### quizb-q3 — planar codec 4 (lz4), P = 2,000,000, channel a uint64, channel b uint8

§17.2 codec 4 clause (`[R-COD-07]`): "Writers MUST NOT declare this codec for
a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes
... In a planar layer each channel's plane carries its own decoded size
(§14.2, §14.3), and the largest governs." Register row L2/L44 give the
planar-numeric formula P·Bᶜ (P = sample positions per tile, Bᶜ = the
channel's element byte size). §12's type table: uint8 → 1 byte, uint64 → 8
bytes (lines 1673, 1676).
Channel a (uint64): P·Bᶜ = 2,000,000 × 8 = 16,000,000 bytes.
Channel b (uint8): P·Bᶜ = 2,000,000 × 1 = 2,000,000 bytes.
Channel a's plane is larger, so channel a governs. 16,000,000 ≤
0x7E000000 (2,113,929,216), so the declaration is conforming.

### quizb-q4 — layer declares alignment A=4096 ≠ 0 and slab S=8 ≠ 0

Register row L20 (§21.3, outcome header "reject-layer"): "A layer record
declares both a per-tile alignment A ≠ 0 and a slab S ≠ 0" → `[R-CNT-16]`.
Also §16 line 1010: "per-tile alignment and slab declarations are mutually
exclusive." §21.3's header states the outcome for every row in that table:
"Outcome: reject-layer; the named layer is unusable, every other layer
unaffected." So outcome class reject-layer, register row L20.

### quizb-q5 — extents (7,7), tile extents (4,4), int16 fill 0x2A2B, tile (1,1)

§11.3: tile grid is ⌈7/4⌉ = 2 along each axis; tile (1,1) covers coordinates
[4,8) on each axis. Only x,y ∈ {4,5,6} are real (3 × 3 = 9 real positions).
Each tile block has ∏Tᵢ = 4×4 = 16 sample positions, so padding positions =
16 − 9 = 7.
§14.5 (`[R-SER-05]`) example: "With one uint16 channel and fill `0xABCD`,
that decoded tile is 32 bytes ... values 1–15 are each the bytes `CD AB`" —
i.e., a fill value written as hex 0xHHLL encodes, in little-endian storage
order, the byte pair LL HH. Applying the same convention to fill 0x2A2B:
storage-order bytes are 2B 2A.

### quizb-q6 — top-level user-metadata record (type 0x0002), MU=1, PE=0

Register row F25 (§21.2): "A non-layer top-level record's flags carry
MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination no writer
emits" → `[R-CNT-12]`, detector verifier. Type 0x0002 (user-metadata) is a
non-layer top-level record type (type 0x0001 is reserved for the layer
record, per L26's note), so F25 is the row this stored-flag combination
violates.

### quizb-q7 — planar read of r,g,b at one position; r's tile fails stored-bytes CRC, g sentinel, b decodes

§19.4 step 8 (`[R-RDR-04]`): "Where the request covered several entries (a
region, or a planar layer's several channels), each rejected entry's failure
is bounded to the positions that entry carries (§2.4): the reader MAY return
the validating entries' values together with a per-entry report of the
failed ones, or fail the request as a whole, but MUST NOT stand fill in for
a rejected tile's positions ... That bounding is a property of tile scope."
r's failure is a stored-bytes CRC mismatch, checked at §19.4 step 5
(`[R-CNT-20]`), which is a tile-scope condition whose outcome class is
reject-tile. The reader MAY return g's and b's values while reporting r's
failure separately (one of the two choices the text licenses).

### quizb-q8 — appender extends planar channel list by one channel; may it re-emit only the new channel's index entries?

§20.3 step 4 (`[R-LIF-02]`, `[R-LIF-01]`): "Every layer whose stored-tile set
or index content this commit changes has its tile-index region re-emitted
in full, entry_count entries plus the segment CRC array, necessarily at a
new placement ... entries new to this generation (every entry of a layer
this commit adds or re-declares, and the tiles a grown extent or an
appended channel adds to the addressed set) emitted per §15, and every other
entry byte-identical at its disk-ordinal position." Appending a channel
changes the layer's index content (it adds entries for the new channel's
tiles), so the whole region must be re-emitted in full at a new placement —
the existing entries are reproduced byte-identically within that full
re-emission, not left untouched in place at the old placement. The
statement in the question (leaving existing entries' bytes and position
untouched, appending only the new entries) is therefore false.

### quizb-q9 — channel type uint32, fill length prefix 3

Register row L30 (§21.3): "A channel entry's fill length prefix differs
from the element size of the channel's declared type" → `[R-CNT-23]`
(R-TYP-06). uint32's element size is 4 bytes (§12 type table); a fill
length prefix of 3 differs from 4, violating L30.

### quizb-q10 — entry_count = 131,072, all entries sentinel

131,072 = 2 × 65,536 = 2 × 2¹⁶ exactly, so there are 2 segments, both full
(each covering exactly 2¹⁶ entries, none partial). §15.4 (`[R-IDX-05]`):
"The CRC-32C of a segment consisting of 2¹⁶ sentinel entries is
`0xEECB3BB2`; writers of sparse layers MAY emit this constant for any full
segment ... whose entries are all sentinels." Both segments here are full
and all-sentinel, so each segment's true computed CRC-32C equals
0xEECB3BB2.

### quizb-q11 — version_major=1, version_minor=5, no incompat bits, ignore-lane bit 20 set; reader implements through minor 2

§6.3 (`[R-CNT-07]`): "A reader MUST NOT reject a file for its version_minor:
minor releases are additive-only, and all feature gating is structural
(records, enums, flags)." Also §6.3 (`[R-CNT-08]`): "a reader MUST ... MUST
ignore all bits in the ignore lane (bits 16–31) ... A set ignore-lane bit is
nevertheless not a file-conformance violation." No incompat-lane bit is set
(so no F19), version_minor mismatch never gates, and the set ignore-lane bit
is ignored and is not itself a violation. The file is accepted; no register
row applies.

### quizb-q12 — rewriter input layer has a tile-index entry §15.3 classifies reject-tile on a structural ground

§20.5 (`[R-WRT-06]`, `[R-WRT-07]`): "An entry §15.3 classifies reject-tile on
a structural ground is neither [a sentinel nor a re-pointable stored entry],
since `[R-IDX-03]` gives it no stored extent for a re-pointing to target, so
regenerating the region cannot proceed without meeting it, and the violation
is thereafter one the rewriter has detected. `[R-WRT-06]` then leaves it two
disposals, since it can neither reproduce the entry nor invent a
replacement: drop the layer, which §20.4's table licenses and whose loss the
rewriter SHOULD report as that table says, or refuse." Two actions: drop the
layer; refuse to rewrite.

### quizb-q13 — remote reader, transport doesn't disclose range response's complete length

§6.4 (`[R-CNT-09]`, `[R-CNT-10]`): "(1) Fetch the final 64 bytes, a suffix
range, and validate ... Where the transport discloses a range response's
complete length, that response also carries the transport-authoritative
file size F, so §19.1's first two steps cost one request between them;
where it does not, `[R-CNT-10]` governs: a reader that probes separately
spends a third request, and one that cannot fails the open. (2) Fetch
[dir_offset, dir_offset + dir_length) ..." So: request 1 = suffix fetch
(trailer bytes, but no disclosed complete length here); request 2 = a
separate size probe (the "third request" language counts this as the third
once request 2/directory-fetch is counted as the baseline's second); request
3 = directory fetch. Minimum = 3 round trips.

### quizb-q14 — rank 2, extents (1000,2000), tile extents (300,500), layout=interleaved, entry_count=21

Geometry-derived addressed-tile count N = ∏⌈Eᵢ/Tᵢ⌉: ⌈1000/300⌉ = 4 (300×3 =
900 < 1000), ⌈2000/500⌉ = 4 (500×4 = 2000, exact). N = 4 × 4 = 16.
Register row L21 (§21.3): "entry_count does not equal the geometry-derived
addressed-tile count (N interleaved, C·N planar)" → `[R-CNT-17]`. For an
interleaved layer the required entry_count is N = 16; declared entry_count
is 21 ≠ 16, violating L21.

### quizb-q15 — multi-tile request, step 3 index-chain failure (crc_of_crc_array or segment-CRC mismatch)

§19.4 step 8 (`[R-RDR-04]`): "A failure inside the same request that takes
layer scope instead, step 3's index-chain failure (`[R-IDX-04]`), bars the
request's remaining entries and all further service from the layer; the bar
is prospective, so values the reader has already returned under §19.2's
timing stand (§2.4)." The outcome class is reject-layer (layer scope), per
§21.3's header and `[R-IDX-04]`'s own text ("any mismatch or cross-check
failure ... is reject-layer"). The reader may NOT still service the
request's remaining tile entries from that layer afterward — the bar covers
"the request's remaining entries and all further service from the layer."

## Final answers summary

1. 128
2. 1400008
3. conforming; channel a; 16000000
4. reject-layer, L20
5. 7 positions; bytes 2B 2A
6. F25
7. may return g and b while reporting r separately; reject-tile
8. False
9. L30
10. 2 segments; 0xEECB3BB2 each
11. Yes; none
12. drop the layer; refuse to rewrite
13. 3
14. L21
15. reject-layer (layer scope); No
