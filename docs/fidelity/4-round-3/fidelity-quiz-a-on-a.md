# Fidelity round transcript — quiz-a-on-a

## Disclosure

- My scratch directory (`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/quiz-a-on-a/`) was empty when I began; I created it myself. This transcript file is the only file I wrote there.
- I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`. I opened no other copy of this specification, no docs/, no ADRs, no PLAN.md/OPEN-QUESTIONS.md/AGENTS.md/README.md/CONTRIBUTING.md, no conformance/ tooling or vectors, no spec/registry.json, no git history/log/diff, and did not web search or web fetch. I did not list that file's directory or any sibling edition directory. The path given matched where the brief said it would be.
- Context I did not ask for appeared before this task began: a project CLAUDE.md pointing to an AGENTS.md (which I did not open), a user auto-memory file listing many TARN-related note titles (about harness specs, lineage gates, repair passes, etc. — titles only, not opened as files, and I did not treat their contents as evidence about the specification), a git-status block naming recent commit subjects on a branch called "readable", and a model/attribution system reminder. None of this is part of, or evidence about, the specification text, and I disregarded all of it when answering the slate below.
- A relayed "user request" appeared above the computed brief, consisting of the single word "Go." I treated it exactly as the brief describes: the message that launched this round, not a task for me, needing no reconciliation with this brief.
- I ran `mkdir -p` and `ls` only on my own scratch directory (to confirm it was empty before writing to it), and I did not list or read the output directory (`fidelity-5/out/`) beyond creating/writing into it.
- I ran `grep -n "^#"` and several targeted `grep -n` searches against the one permitted file (`tarn.md`) to locate section/row numbers, and I ran local Python arithmetic (`python3 -I`, reading no files) to compute index-region sizes, hex values, tile ordinals, and segment memberships. No other files were read, and no other commands were run.
- Per the hard-wrap warning, for every arithmetic/lookup question I grepped a short, unwrappable fragment (row labels like `F36`, rule IDs like `R-COD-07`, `R-VEC-04`, `R-RDR-04`) rather than long phrases, and then read the surrounding prose with the Read tool at the located line numbers, so wrapped blockquote text was read in full rather than line-matched.

## Per-question work

### quiza-01 — index_encoding 1, entry_count = 70,000 → extent_length (hex u64)

§15.1: region = entry array (entry_count × 20 bytes) + segment CRC array (⌈entry_count / 2¹⁶⌉ × 4 bytes), no padding.

- entry array = 70,000 × 20 = 1,400,000 bytes
- segments = ⌈70,000 / 65,536⌉ = 2
- segment CRC array = 2 × 4 = 8 bytes
- total = 1,400,000 + 8 = 1,400,008 = 0x155CC8

Answer: `0x155CC8`

### quiza-02 — §6.4 writer guidance, max dir_length for a 64 KiB suffix fetch

§6.4, R-CNT-09: "Writers SHOULD keep dir_length plus the pre-trailer pad plus 64 within 65,536 bytes so that a 64 KiB suffix fetch captures trailer and directory together."

§9.2 step 5 / §6.2: the pre-trailer pad runs up to the next 64-byte boundary, so its worst case is 63 bytes (0–63).

dir_length_max = 65,536 − 64 − 63 = 65,409 bytes.

Answer: `65409`

### quiza-03 — §2.3 R-CNF-13 reach rule applied to §21.2

§21.2's own lead-in states it directly: "Deriving it there yields F8, F14, F6 and both of F1's instances — each asserting an invariant `[R-CNT-24]` fixes in every major — and no other row."

F1 has 2 instances (front-signature-block byte-reversal; trailer-magic byte-reversal), F6, F8, F14 each 1 instance. Total = 2+1+1+1 = 5.

Answer: rows F1, F6, F8, F14; total instances = 5.

### quiza-04 — committed_file_length = 1,048,576 → minimum legal next value (hex u64)

§9.2 R-LIF-02: "A commit's committed_file_length is strictly greater than the prior trailer's, by at least 128."

1,048,576 + 128 = 1,048,704 = 0x100080.

Answer: `0x100080`

### quiza-05 — planar layer, dims (y,x) extents (1000,2049), tiles (256,256), C=3; disk ordinal of tile (y=3,x=7), channel 1

§11.2: G_y = ⌈1000/256⌉ = 4; G_x = ⌈2049/256⌉ = 9; N = G_y·G_x = 36.
§11.4: linearization 1, last-declared dimension (x) varies fastest: s = t_y·G_x + t_x = 3·9 + 7 = 34.
Planar disk ordinal = c·N + s = 1·36 + 34 = 70.

Answer: `70`

### quiza-06 — interleaved u(uint32)/v(int16)/w(bool), tiles (4,4); byte offset of w at in-tile (2,3)

§14.2: Q = ΣBᵢ = 4+2+1 = 7; F_w = ΣB_j (j<w) = 4+2 = 6.
§11.4 in-tile ordinal (row-major, 2D): u = u₀·T₁+u₁ = 2·4+3 = 11.
Offset = u·Q + F_w = 11·7 + 6 = 83.

Answer: `83`

### quiza-07 — planar bool, fill=true, P=20 real positions all stored false; 3 decoded bytes

§14.3: packed LSB-first, decoded size = ⌈20/8⌉ = 3 bytes. Pad bits are bit positions P mod 8 (=4) through 7 of the final byte (byte index 2).
§14.5/R-SER-05: every pad bit MUST carry the plane's channel's fill bit (fill = true = 1); the 20 real values are all false = 0.

- byte 0 (values 0–7, all false): 0x00
- byte 1 (values 8–15, all false): 0x00
- byte 2: bits 0–3 = values 16–19 = 0; bits 4–7 = pad bits = 1 → 0b11110000 = 0xF0

Answer: `00 00 F0`

### quiza-08 — planar uint64 channel, P=300,000,000 per addressed tile, codec 4 (lz4)

§17.2 R-COD-07: lz4 cap is per-channel-plane decoded size ≤ 0x7E000000 bytes (checkable from declarations alone: P and the channel's element size).

decoded size = P·B = 300,000,000 × 8 = 2,400,000,000 = 0x8F0D1800, which exceeds 0x7E000000 (2,113,929,216).

"Writers MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes ... and a reader MUST treat such a declaration as a validity error at layer scope, checkable from declarations alone."

Answer: Nonconforming; outcome class reject-layer; owning scope layer; yes, declaration-only detectable.

### quiza-09 — one layer, a dimension named z and a channel also named z

§4.6 R-ENC-15: "Names are unique within their scope: layer names among a file's layers, dimension names among a layer's dimensions, and channel names among a layer's channels. The last two are separate namespaces, so a dimension and a channel of one layer are permitted to share a name — the ordinary way to name a channel after the axis it samples."

Answer: Conforming (permitted); reason: dimension names and channel names are separate namespaces.

### quiza-10 — planar N=100,000, C=4, read all 4 channels at s=50,000; distinct index segments (excluding crc_of_crc_array)

Disk ordinals k = c·N+s for c=0..3: 50,000; 150,000; 250,000; 350,000.
Segment = ⌊k/65,536⌋: 0; 2; 3; 5 — four distinct segments (verified by computation; no two channels fall in the same segment here).

Answer: `4`

### quiza-11 — reserved-range type 0x1234, MU=0, in the directory's top-level sequence

§21.2 F35 (reader/open, R-CNT-15): triggers only when MU=1 on a reserved-range type; here MU=0, so this row does not fire and no reader obligation to reject arises from it.

§21.2 F36 (verifier/certification, R-CNT-15): "A top-level record carries a type value from the reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is a violation whatever its MU bit." §21.2's outcome for all its rows is reject-file.

Answer: No, a conforming reader need not reject the file on this record's account (MU=0 does not trigger F35); yes, the file is nonetheless nonconforming under row F36, outcome class reject-file, detector the verifier.

### quiza-12 — §20.3 step 4, layer stored a tile in the superseded generation; commit shrinks one dimension extent only

§20.3 step 4: "a dimension extent MAY grow, and MUST NOT shrink ... A commit MUST NOT change one of these; the change is a new layer, or a rewrite that re-declares it under a fresh file_id." And: "The bar binds a layer the commit keeps and nothing else: a commit MAY drop the layer (§20.4) and add a new one under its name and other declarations ... What the bar removes is a re-declaration carried as the same layer over the tiles it stored." A later passage also names "a shrink" among the changes that "are rewrites even where a particular file would survive them in place."

Answer: (1) as a new layer (drop the existing layer and declare a new one under its name/other declarations), or (2) via a rewrite that re-declares the layer under a fresh file_id.

### quiza-13 — unregistered type 0x1234 implemented by its own external definition (MU=0,PE=1 fixed); stored bits read MU=0,PE=0; commit does not logically modify the record

§20.4 (preservation table, R-WRT-05/R-CNT-22): "For a type the updater implements that this specification does not register, the definition it implements the type from supplies the flags, and the stored bits never do." Table row "MU = 0, PE = 1 → Retain byte-identical, extent content unmodified."

Answer: The type's own (external) definition governs — MU=0, PE=1 — not the stored bits; no, the updater may not drop the record (it must retain it byte-identical).

### quiza-14 — R-VEC-04, every reject-layer vector

§24 R-VEC-04: "Every vector whose recorded outcome is reject-layer or reject-tile is built inside a file that also carries an **intact sibling** — another layer, or another tile of the same layer where that layer is one a reader is still permitted to serve — whose decoded content the manifest records, and a vector's expectation is therefore a pair."

Answer: an intact sibling (another layer, or another still-servable tile of the same layer); the manifest must record its decoded content.

### quiza-15 — R-RDR-04, interleaved layer, region read, earlier tiles already returned, later tile's segment CRC fails

§19.4 step 8 / R-RDR-04: "A failure inside the same request that takes layer scope instead — step 3's index-chain failure (`[R-IDX-04]`) — bars the request's remaining entries and all further service from the layer; the bar is prospective, so values the reader has already returned under §19.2's timing stand (§2.4)."

Answer: (a) the values already returned earlier in the request stand (they are not withdrawn or invalidated); (b) the layer is barred from all further service to that reader for the rest of the session (every later request against that layer fails).
