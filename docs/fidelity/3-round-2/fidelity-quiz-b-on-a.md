# Transcript — quiz-b-on-a

## Disclosure

- A relayed "user request" (the single word "Go") appeared above the task brief. Per the
  brief's own instructions, this is the launcher's message to the orchestrator, carries
  no task content for me, needs no reconciliation with the brief, and does not widen the
  access rule. Noted and set aside.
- My runtime also placed unsolicited context ahead of the task: a project CLAUDE.md
  pointer, a long list of the user's auto-memory note titles about this TARN project, a
  git-status block, and an attribution-footer reminder. None of this is part of the
  specification and none of it is evidence about the specification's content; I disregarded
  all of it and did not open any of the referenced memory files, ADRs, or other project
  documents. I am not repeating its contents here beyond naming that it appeared.
- The only file I read for substantive content was the one named by the brief:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`.
  The path matched exactly what the brief specified; I note this so the path claim itself
  is checked. I did not open any other copy of this specification, and did not list any
  other directory (docs/, conformance/, spec/, etc.) or read any other project file.
- Commands run: `wc -l` and `grep -n` / `sed -n` against that single file only (plus
  `mkdir`/`ls` against my own scratch directory). No web search, no web fetch, no git
  history commands.
- My scratch directory
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/quiz-b-on-a/`
  was empty when I started (verified with `ls -la`); there was no previous attempt's
  files to report.
- I did not read or list the output directory
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/`.
- Whitespace/hard-wrap caveat followed: every grep I used targeted short fragments
  or table/code text that does not wrap (e.g. field names, register-row labels, numeric
  constants), and I cross-checked suspicious zero-hits against known-present text in the
  same passage before relying on them (e.g. confirming "committed_file_length" and
  "dir_offset" each appear plainly, and reading full section spans with `sed -n` rather
  than relying solely on line-oriented grep for prose passages).

## Sections read (by line range, via sed -n on the one file)

§2.4 (296–345), §4.1–4.2 (443–460), §5.1–5.2 (635–700), §6.2–6.4 (828–970),
§7.4 (1121–1233), §11.1–11.4 (1655–1745), §12 (1790–1900), §13 (1894–1994),
§14 (1994–2195), §15 (2195–2330), §16 (2321–2426), §17 (2426–2635),
§19.4 (3047–3126), §20.3 (3188–3475), §20.5 (3551–3735), §21.2 register (3834–3890),
§21.3 register rows L1–L49 (3895–3943).

## Work

### q1 — minimum F with dir_offset=16, dir_length=20
§6.2 trailer table: dir_offset ≥ 16 (16 ok); dir_length ≥ 4 (20 ok);
dir_offset + dir_length ≤ F − 64 → 36 ≤ F − 64 → F ≥ 100.
committed_file_length = F, multiple of 64 (§6.2, R-CNT-01).
§5.1/§21.2 (F5, R-CNT-27): F ≥ 128 (no conforming file shorter than 128 bytes).
Smallest F that is a multiple of 64, ≥ 100, and ≥ 128 → F = 128.
Check: 16 + 20 = 36 ≤ 128 − 64 = 64. Holds.
**Answer: 128**

### q2 — index_encoding 1, entry_count = 70,000
§15.1: entry array = entry_count × 20 bytes; segment CRC array =
⌈entry_count / 2¹⁶⌉ × 4 bytes.
entry array = 70,000 × 20 = 1,400,000.
segments = ⌈70,000 / 65,536⌉ = 2 → segment CRC array = 2 × 4 = 8.
Total = 1,400,000 + 8 = 1,400,008.
**Answer: 1,400,008**

### q3 — codec 4 (lz4), planar, P = 2,000,000, channel a uint64, b uint8
§14.2: planar numeric decoded size = P · Bᶜ. §12.1 element sizes: uint64 = 8,
uint8 = 1.
a: 2,000,000 × 8 = 16,000,000. b: 2,000,000 × 1 = 2,000,000.
§17.2/R-COD-07 (L44): "in a planar layer each channel's plane carries its own
decoded size... and the largest governs," cap 0x7E000000 = 2,113,929,216.
Largest plane is channel a (uint64) at 16,000,000, well under the cap.
**Answer: conforming; governing channel a; 16,000,000 bytes**

### q4 — A = 4096 and S = 8, both nonzero, same layer record
§7.4/R-CNT-16: "Declaring both A ≠ 0 and S ≠ 0 is a validity error at layer
scope: the per-tile alignment and slab declarations are mutually exclusive."
Register row L20 (§21.3): "A layer record declares both a per-tile alignment
A ≠ 0 and a slab S ≠ 0" — detector reader, detected layer access, governing
rule R-CNT-16. A validity error at layer scope is reject-layer (§2.4).
**Answer: reject-layer, L20**

### q5 — extents (7,7), tile extents (4,4), int16 fill 0x2A2B, tile (1,1)
Grid Gᵢ = ⌈7/4⌉ = 2 per axis (§11.2). Tile (1,1) covers global coordinates
[4,8) on each axis. Valid real coordinates are [0,7), i.e. 0..6, so within
[4,8) only 4,5,6 are real (3 per axis) and 7 is padding.
Total positions per tile P = 4×4 = 16. Real = 3×3 = 9. Padding = 16 − 9 = 7.
§4.1 little-endian: int16 value 0x2A2B stores low byte first: byte0 = 0x2B,
byte1 = 0x2A. §14.5: every padding position encodes the channel's fill bytes
unchanged.
**Answer: 7 positions; bytes 2B 2A**

### q6 — top-level user-metadata record (0x0002), MU=1, PE=0
§21.2 register row F25: "A non-layer top-level record's flags carry
MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination no writer
emits" — detector verifier, certification, governing rule R-CNT-12. A
user-metadata record (type 0x0002) is a non-layer top-level record, so F25
applies (not L46, which is the layer-record/sub-record analogue).
**Answer: F25**

### q7 — planar read of r,g,b at one position; r fails crc, g sentinel, b clean
§19.4 step 8/R-RDR-04: "Where the request covered several entries — a
region, or a planar layer's several channels — each rejected entry's
failure is bounded to the positions that entry carries ... the reader MAY
return the validating entries' values together with a per-entry report of
the failed ones, or fail the request as a whole, but MUST NOT stand fill in
for a rejected tile's positions ... That bounding is a property of tile
scope." r's stored-bytes crc failure is a tile-scope reject-tile outcome
(§15.3: "stored bytes fail the entry's crc | reject-tile").
**Answer: may return g and b while reporting r separately; reject-tile**

### q8 — appender extends channel list by one, re-emission via entries-only append
§20.3 step 4 (R-WRT-04): "Every layer whose stored-tile set or index content
this commit changes has its tile-index region re-emitted in full —
entry_count entries plus the segment CRC array — necessarily at a new
placement ... with entries ... new to this generation (every entry of a
layer this commit adds or re-declares, and the tiles a grown extent or an
appended channel adds to the addressed set) emitted per §15, and every
other entry byte-identical at its disk-ordinal position." The whole region
moves to a new placement; existing entries are byte-identical in *content*
but are not left untouched in *position* — the obligation is a full
re-emission at a new placement, not an append of only the new channel's
entries in place.
**Answer: False**

### q9 — channel entry type uint32, fill length prefix 3
§12.1: uint32 element size = 4. §7.4/R-CNT-23: "fill length equals the
type's element size." Register row L30 (§21.3): "A channel entry's fill
length prefix differs from the element size of the channel's declared
type" — governing rule R-CNT-23 (R-TYP-06). prefix 3 ≠ element size 4.
**Answer: L30**

### q10 — entry_count = 131,072, all sentinel
§15.4: segment s covers [s·2¹⁶, min((s+1)·2¹⁶, entry_count)).
131,072 / 65,536 = 2 exactly → 2 full segments, no partial segment.
§15.4/R-IDX-05: "The CRC-32C of a segment consisting of 2¹⁶ sentinel entries
is 0xEECB3BB2; writers of sparse layers MAY emit this constant for any full
segment ... whose entries are all sentinels." Both segments here are full
(exactly 65,536 entries each) and all-sentinel.
**Answer: 2 segments; 0xEECB3BB2 each**

### q11 — version_major=1, version_minor=5, no incompat bits, ignore-lane bit 20 set; reader implements through minor 2
§6.3/R-CNT-07: "A reader MUST NOT reject a file for its version_minor: minor
releases are additive-only, and all feature gating is structural." §6.3/
R-CNT-08: "a reader MUST ignore all bits in the ignore lane (bits 16–31)."
Bit 20 is in the ignore lane (16–31) and is not a conformance violation for
a file under this text — it is carried-forward feature data a later minor
defines. No incompat bit is set (so F19 does not apply), version_minor
itself cannot trigger rejection, and nothing else in the trailer is at
issue. The file is accepted; no file-scope register row applies.
**Answer: yes; none**

### q12 — rewriter input layer has a reject-tile-on-structural-ground entry
§20.5: "Regenerating a region means classifying every entry in it: a
sentinel is re-emitted unchanged, and every other entry is re-pointed to
where its stored extent now lies. An entry §15.3 classifies reject-tile on
a structural ground is neither ... so regenerating the region cannot
proceed without meeting it, and the violation is thereafter one the
rewriter has detected. [R-WRT-06] then leaves it two disposals, since it
can neither reproduce the entry nor invent a replacement: drop the layer,
which §20.4's table licenses and whose loss the rewriter SHOULD report as
that table says, or refuse."
**Answer: drop the layer; refuse to rewrite**

### q13 — remote reader, transport doesn't disclose complete length, must probe separately
§6.4/R-CNT-10: baseline remote open is two requests (suffix fetch of final
64 bytes + directory fetch), where the first normally also discloses file
size. "(`[R-CNT-10]`, which governs where it does not: a reader that probes
separately spends a third request, and one that cannot fails the open)."
Minimum = 2 (baseline) + 1 (separate size probe) = 3.
**Answer: 3**

### q14 — rank 2, extents (1000,2000), tile extents (300,500), interleaved, entry_count=21
§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉. G1 = ⌈1000/300⌉ = 4, G2 = ⌈2000/500⌉ = 4. N = G1×G2 = 16.
Interleaved addressed-tile count = N = 16 (§11.2). Declared entry_count = 21
≠ 16. Register row L21 (§21.3): "entry_count does not equal the
geometry-derived addressed-tile count (N interleaved, C·N planar)" —
instance "interleaved N, entry_count larger" — governing rule R-CNT-17.
**Answer: L21**

### q15 — step 3 index-chain failure (crc_of_crc_array or segment-CRC mismatch) mid multi-tile request
§19.4 step 8/R-RDR-04: "A failure inside the same request that takes layer
scope instead — step 3's index-chain failure (`[R-IDX-04]`) — bars the
request's remaining entries and all further service from the layer; the
bar is prospective, so values the reader has already returned under
§19.2's timing stand." This is a layer-scope reject-layer outcome, and it
bars both the rest of this request's entries and all further service from
the layer — the reader may NOT continue servicing remaining entries from
that layer.
**Answer: reject-layer (layer scope); no**

## Final answers summary
q1: 128
q2: 1,400,008
q3: conforming; channel a; 16,000,000 bytes
q4: reject-layer, L20
q5: 7 positions; bytes 2B 2A
q6: F25
q7: may return g and b while reporting r separately; reject-tile
q8: False
q9: L30
q10: 2 segments; 0xEECB3BB2 each
q11: yes; none
q12: drop the layer; refuse to rewrite
q13: 3
q14: L21
q15: reject-layer (layer scope); no
