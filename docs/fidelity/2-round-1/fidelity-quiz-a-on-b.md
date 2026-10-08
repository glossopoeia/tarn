# Working notes (quiz-a-on-b)

Scratch dir was empty at start (no prior attempt files found).

Only file read: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md
(4847 lines, 294876 bytes). Read via Bash (sed -n, grep -n, awk) in ranges; no
other files opened, no directories listed except the scratch dir itself and a
confirmatory `ls -la` on the spec file's own path (not its containing
directory's listing of other files). No git commands, no web access.

## Section map built first
`grep -n "^#" spec/tarn.md` to get the table of contents / line numbers for
all sections, then targeted `sed -n 'A,Bp'` reads of:
- §2.4 Outcome classes (lines 294-342)
- §5.2 Byte coverage, §6.1-6.4 Front signature/Trailer/Version gates/Remote
  open (575-827)
- §18.1-18.2 User metadata document & encoding (2489-2530)
- §11.1-11.4 Geometry, grid arithmetic, padding, linearization (1514-1646)
- §14.3-14.5 Packed boolean planes, layout-type validity, padding content
  (1951-2051)
- §15.1-15.4 Tile index region/entry layout, sentinel, entry validity,
  segments (2051-2177)
- §16.2 The slab declaration (2207-2282)
- §17.2 Codecs (2305-2431)
- §20.5 Rewriting (3407-3589)
- §21.1-21.9 Error-handling register and limits (3591-4107), including the
  full F-row table (21.2), L-row table (21.3), T-row table (21.4), R-row
  table (21.5)
- §7.4 The layer record (973-1085)

Targeted `grep -n` passes used to locate specific requirement IDs and rows,
e.g. `grep -n "R-CNT-25\]"`, and an `awk '/#### 21.3/,/#### 21.4/'` slice
piped to `grep` for the L-rows (L43/L44) and index_encoding (L31) rows.

Local computation only (python3, no file I/O): arithmetic for entry_count,
extent_length, 0x7E000000 vs 2,150,000,000, disk-ordinal row/channel
linearization, and the packed-boolean-plane bit arithmetic for Q7.

## Per-question reasoning summary

- Q1: F=1,048,576; committed_file_length=1,048,512 (a multiple of 64, so not
  F13) but != F -> F17 (committed_file_length != transport-authoritative
  file size) -> reject-file. (R-CNT-06, F17 row, §21.2)
- Q2: top-level user-metadata record, extent (10,40), both nonzero. Per
  §18.1, the quarantine (R-CNT-25) covers the *document* only; "a malformed
  extent slot on such a record ... is a validity error at the record's
  containing scope ... because that failure precedes the document."
  extent_offset=10 lies in 1-15 -> matches F31 (nonzero extent slot,
  extent_offset in 1-15, pointing into front signature block) -> reject-file,
  not ignore-record.
- Q3: §6.3 R-CNT-08: "An updater MUST copy forward unknown ignore-lane bits
  of its input file, MUST NOT clear them" - explicitly "every updater under
  this text, appender and rewriter alike." §20.5 restates for rewriters: "The
  output trailer MUST copy the input's unknown ignore-lane flag bits forward
  and set no other." -> must be set.
- Q4: extent_offset=0, extent_length=500: exactly one half zero (offset 0,
  length != 0) -> F30 by definition; F33's own note confirms this exact
  (0,N) N!=0 case belongs to F30, not F31 or F33.
- Q5: addressed-tile count (entry_count) for a planar layer = C * N
  (§11.2, R-GEO-03) = 7 * 1,000,000 = 7,000,000. Under index_encoding 1,
  extent_length = entry_count*20 + ceil(entry_count/65536)*4 (§7.4,
  R-CNT-17) = 140,000,000 + ceil(106.811...)=107 * 4 = 140,000,000 + 428 =
  140,000,428.
- Q6: §17.2's note on codec 4 (R-COD-07): the 0x7E000000 cap is "quantified
  over the layer's addressed tiles," so a layer addressing none (any
  dimension extent 0) "satisfies it whatever its tile shape declares... The
  escape ends exactly when the layer's addressed-tile count rises above 0."
  After growth, the layer addresses tiles and the largest channel plane
  (2,150,000,000 bytes) exceeds 0x7E000000 = 2,113,929,216 -> now a
  violation -> yes, L44 (§21.3).
- Q7: P = tile extent = 13 (rank 1), decoded size = ceil(13/8) = 2 bytes.
  Packing is LSB-first, value k -> bit (k mod 8) of byte (k div 8) (§14.3).
  Real values at ordinals 0-9: T T F F T T F F T T. Padding positions
  (ordinals 10-12, inside the tile but beyond the dimension's real extent)
  carry the channel's fill value (true) per §14.5 (R-SER-05). Byte 1's
  three unused pad bits (k=13,14,15, beyond P=13) also carry the fill bit
  (true) per R-SER-05/R-SER-03. Byte0 (k=0..7): 1,1,0,0,1,1,0,0 -> value =
  1+2+16+32 = 0x33. Byte1 (k=8..15): bits0-1 real (T,T)=1,1; bits2-4
  padding positions (fill=1,1,1); bits5-7 pad bits (fill=1,1,1) -> all 8
  bits set -> 0xFF. Answer: "33 FF".
- Q8: linearization §11.4 (R-GEO-06): spatial ordinal s = t_y*G_x + t_x
  (y declared first, x last, last-declared varies fastest) = 3*7+2 = 23.
  disk ordinal = c*N + s (planar) = 4*35 + 23 = 163. Entry byte range:
  region byte 20*k (§15.1) -> [163*20, 163*20+20) = [3260, 3280).
- Q9: §16.2 (R-SLB-03) states explicitly: "An entry whose only defect is
  that its stored bytes fail its crc is not transparent — its offset and
  length stand, and the packing relation reads them as it does any other
  stored tile's." Ordinal 14 (crc-failed payload, well-formed fields) must
  satisfy the packing relation; only sentinels (ordinal 15) and
  structurally-invalid entries are transparent.
- Q10: §2.4's reject-layer definition: "The outcome is prospective: it bars
  further service from the layer, and does not retroactively invalidate
  content already returned under §19.2's validation timing (R-RDR-02)."
  -> B and C's values stand as validly returned.
- Q11: superseded s = t_y*G_x_old + t_x = 1*8+0 = 8; disk ordinal =
  2*32+8 = 72 (matches given). After growth G_x: 8->10 (G_y stays 4),
  N_new = 40; new s = 1*10+0 = 10; new disk ordinal = 2*40+10 = 90.
  §11.1's rationale paragraph: "Any other growth [one that changes a grid
  count, here, unlike a growth that doesn't] changes the index content —
  entry_count and extent_length with it, and disk ordinals renumber
  wherever R-GEO-06 moves them — so the layer's whole tile-index region is
  re-emitted." -> must be re-emitted at a new position (90).
- Q12: offset = all-ones sentinel, length = 1337 (not sentinel), crc = 0.
  §15.3's table: "offset = S ∧ length != S, or offset != S ∧ length = S" is
  the row for exactly-one-sentinel-field. Register (§21.4): T6 requires
  *both* fields sentinel with crc != 0 (not our case); T7 is "exactly one of
  offset and length ... the sentinel value" -> T7.
- Q13: §20.5 (Rewriting) on regenerating an index region: "An entry §15.3
  classifies reject-tile on a structural ground is neither [a sentinel nor
  a re-pointable stored tile] — R-IDX-03 gives it no stored extent for a
  re-pointing to target — so regenerating the region cannot proceed without
  meeting it... R-WRT-06 then leaves it two disposals, since it can neither
  reproduce the entry nor invent a replacement: drop the layer, which
  §20.4's table licenses ... or refuse." -> (c); the two options are
  "drop the layer" or "refuse to rewrite."
- Q14: §7.4's own text for index_encoding already treats 0, reserved
  2-0x7F and experimental >=0x80 identically ("any other value ... is a
  validity error at layer scope"). Register §21.3 row L31 lists all three
  (index_encoding 0; reserved 2-0x7F; experimental >=0x80) as instances of
  one row with one outcome (reject-layer). -> same row, L31.
- Q15: §21.9's table states these are "minimum guarantees, not caps": "A
  file exceeding any of these remains conforming, and a reader MAY decline
  it... a refusal on resource grounds MUST be reported as a resource limit
  and not as a validity error" (R-ERR-04). entry_count = 2^33 exceeds the
  2^32 minimum-guarantee row but is otherwise valid (well within the u64 /
  2^63-1 domain, R-ENC-03) -> (a) conforming; (b) must be reported as a
  resource limit, not a validity error / corruption.

## Context noise encountered (disclosed, not used as evidence)

Before this task's own content, the runtime surfaced: a project CLAUDE.md
pointing to an AGENTS.md (not opened), a user memory-file index listing
several TARN-related note titles (not opened, not followed), a userEmail
block, a gitStatus snapshot naming recent commit subjects on a branch
called "readable", an attribution-lines reminder for commits/PRs, a list of
available skills, and a "today's date" reminder. None of this was treated as
part of or evidence about the specification; none of it was read further or
acted on for this quiz. Per the brief's instruction, its contents are not
repeated here beyond naming the categories above.

The relayed "user request" context line ("Set the constant to
claude-sonnet-5, preflight with --models, then launch.") also appeared
ahead of this task's computed brief. It does not pertain to the quiz's
content (the spec file) and was not treated as instruction for how to
answer the slate; it looks like infrastructure/launch text for the
orchestrating harness, unrelated to the quiz content itself, so it was not
acted upon here beyond being noted as present.

## Path check

The brief said to read exactly
/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md. That
path existed and was read. No other copy of the specification was opened,
and no directory listing was performed beyond confirming that single file's
existence and the (empty) scratch directory's own contents.
