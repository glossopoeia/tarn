# Working transcript — quiz-a-on-a

## Access and setup
- Created my own scratch directory:
  /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/quiz-a-on-a/
  It was empty when I began (no prior attempt's files found).
- The one file I read: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md
  (4981 lines). Confirmed this exact path exists and matches the brief's named path — no path discrepancy.
- I did not list any directory other than my own scratch dir (and the one `ls` on the target file's parent
  to confirm it exists, which only inspected that one file's stat, not a directory listing of siblings).
- I did not read any other file, ADR, docs/ content, PLAN.md, AGENTS.md, conformance/ tooling, registry.json,
  git history/diff/log, or any web resource. All reads below are `sed -n` line-range reads or `grep`/`wc`
  over the single allowed file.
- Context that arrived unbidden in my runtime environment (disclosed per the brief, contents not repeated):
  a project CLAUDE.md pointer, a user MEMORY.md index of prior-round notes, a git-status block (branch,
  recent commit subjects), skill-availability listings, and other environment/system reminders. None of
  this was treated as evidence about the specification's content; all of it is disregarded for answering
  the quiz.
- A harness-relayed "user request" line ("Set the constant to claude-sonnet-5, preflight with --models,
  then launch") appeared above the computed quiz task. I treated this as prior provenance for how this
  session was launched (consistent with the environment stating the active model is claude-sonnet-5),
  not as an instruction to act on now — it required no action from me, and is unrelated to the quiz content.

## Commands run (all against the one allowed file, plus local arithmetic)
1. `wc -l tarn.md` -> 4981 lines.
2. `grep -n "^#" tarn.md` -> full heading map (sections 1–24, Appendices A–H).
3. `sed -n '3733,3990p' tarn.md` -> §21.1 (how to read the register), §21.2 (file-scope, F1–F36),
   §21.3 (layer-scope, L1–L49), start of §21.4 (tile-scope, T1–T26).
4. `sed -n '3990,4080p' tarn.md` -> rest of §21.4/§21.5 (ignore-record, R1–R10), start of §21.6.
5. `sed -n '296,351p' tarn.md` -> §2.4 outcome classes (reject-file/-layer/-tile, ignore-record;
   reject-layer's "prospective, does not retroactively invalidate" clause).
6. `sed -n '828,967p' tarn.md` -> §6.2 trailer layout/fields, §6.3 version/flag gates (rewriter carries
   forward ignore-lane bits), §6.4.
7. `sed -n '1121,1235p' tarn.md` -> §7.4 the layer record (field table, extent_length formula for
   index_encoding 1, worked example).
8. `sed -n '2095,2321p' tarn.md` -> §14.3 packed boolean planes, §14.4–14.5, §15.1 tile-index region/entry
   layout, §15.2 sentinel, §15.3 entry-validity table, §15.4 segments.
9. `sed -n '1700,1790p' tarn.md` -> §11.2 grid arithmetic, §11.3 padding, §11.4 linearization (spatial and
   disk ordinal formulas, planar c·N+s rule).
10. `sed -n '3475,3733p' tarn.md` -> §20.4 re-emission/preservation (MU/PE table), §20.5 rewriting
    (regenerating a tile-index region; structural reject-tile entries leave only "drop the layer" or
    "refuse").
11. `grep -n -i "grow\|grid count\|re-emit\|disk ordinal\|relocat" tarn.md` -> located the growth/grid-count
    renumbering passage.
12. `sed -n '1676,1700p' tarn.md` -> the exact growth rule: a growth changing a grid count (other than the
    0-stays-0 case) renumbers disk ordinals and re-emits the layer's whole tile-index region.
13. `sed -n '2321,2426p' tarn.md` -> §16 slabs/alignment, §16.1 per-tile alignment, §16.2 slab declaration
    (packing invariant; crc-only-failure entries are "not transparent").
14. `sed -n '4142,4241p' tarn.md` -> §21.9 implementation limits (2^32 addressed-tiles-per-layer minimum
    guarantee is a floor, not a cap; resource decline reported as a resource limit, never as corruption).
15. `grep -n "index_encoding" tarn.md` -> confirmed L31 is the single row covering index_encoding 0,
    reserved 2–0x7F, and experimental >=0x80 alike, no separate carve-out anywhere else in the file.
16. `sed -n '2449,2460p;2614,2633p' tarn.md` and `grep -n "R-COD-07\|0x7E000000\|lz4" tarn.md` -> confirmed
    the lz4 decoded-size cap 0x7E000000 and that L44/§21.9/§17.2 agree ("largest channel plane governs"
    in a planar layer).

## Per-question work

### quiza-q01
Trailer fields given: F (physical/transport size) = 1,048,576; committed_file_length = 1,048,512 (a
multiple of 64, since 1,048,512/64 = 16,383); all other trailer gates pass. §21.2 row F17: "Trailer
committed_file_length does not equal the transport-authoritative file size." This is exactly our case
(1,048,512 ≠ 1,048,576). §21.2's header: "Outcome: reject-file." -> F17, reject-file.

### quiza-q02
Top-level user-metadata record, extent_offset=10, extent_length=40 (F=100,000). Not (0,0) so not F21;
extent_length=40 ≥ 5 so not F22. §21.2 F31: "A non-layer top-level record's nonzero extent slot has
extent_offset in 1-15, pointing into the front signature block." 10 ∈ [1,15] -> F31 applies, outcome
reject-file (§21.2 header). This is a structural/location defect in the extent slot itself, not a
document-content problem, so the §21.5 "quarantine" ignore-record treatment (R1–R10, for unreadable
*documents*) does not reach it.

### quiza-q03
§6.3: "A rewriter, though its output is a new file, carries the input's unknown ignore-lane bits into
its output trailer rather than writing flags = 0, and sets no other." Plain compaction is still "a
rewriter['s]... output" under this rule -> must be set.

### quiza-q04
extent_offset=0, extent_length=500 (500 ≠ 0): §21.2 F30, "exactly one half zero (offset 0 with length
!= 0 ...)". The F33 row's own parenthetical confirms: "a record extent slot of (0, N) with N nonzero
reaches the block through its zero offset and is theirs rather than F31's" (and not F33's, since F33
explicitly excludes cases caught by the bounds/half-zero rows). -> F30.

### quiza-q05
Rank 1, extent 1,000,000, tile extent 1 -> N = ceil(1,000,000/1) = 1,000,000 (§11.2). Planar, C=7 ->
addressed-tile count (entry_count) = C·N = 7,000,000 (§11.2, confirmed by L21's "C·N planar").
§7.4: under index_encoding 1, extent_length = entry_count×20 + ceil(entry_count/2^16)×4.
entry_count×20 = 140,000,000.
entry_count/65536 = 7,000,000/65536 = 106.81...  -> ceil = 107.
107×4 = 428.
Total = 140,000,428.

### quiza-q06
Before growth: dimension extent 0 -> N=0, layer addresses zero tiles (§21.6: "A dimension has extent
0 | A valid, empty layer: zero addressed tiles..."); §21.9 "A layer addressing no tile... therefore has
no tile whose decoded size the table bounds" — so L44 cannot bite with zero tiles.
0x7E000000 = 2,113,929,216 (126 × 16^6; computed locally).
After growth: tiles now exist, and the largest channel plane is 2,150,000,000 bytes (given) >
2,113,929,216. L44: "Codec 4 (lz4) declared on a layer any of whose addressed tiles' decoded size
exceeds 0x7E000000 bytes — in a planar layer the largest channel plane governs." -> yes, L44.

### quiza-q07
Rank 1, tile extent 13 -> P = 13 sample positions per tile (ordinals 0–12); real positions 0–9,
padding positions 10–12 (§11.3). Planar bool -> packed, decoded size = ceil(13/8) = 2 bytes (§14.3).
Fill = true = bit 1. Padding positions encode fill (§14.5); the final byte's pad bits beyond the last
value (P mod 8 = 5, so bits 5–7 of byte 1) also carry the fill bit (§14.3/R-SER-05).
Values by ordinal 0..12: 0=T,1=T,2=F,3=F,4=T,5=T,6=F,7=F,8=T,9=T,10=fill=T,11=fill=T,12=fill=T.
Byte 0 (ordinals 0–7), bit k = ordinal k, LSB-first (§4.4/§14.3 "value k occupies bit k mod 8 of byte
k div 8"):
  bits: 1,1,0,0,1,1,0,0 -> 1 + 2 + 16 + 32 = 51 = 0x33.
Byte 1 (ordinals 8–15; only 8–12 exist, 13–15 don't exist as sample ordinals but fall in the pad-bit
range since P mod 8 = 5):
  bit0(k=8)=1, bit1(k=9)=1, bit2(k=10,pad pos,fill)=1, bit3(k=11,pad pos,fill)=1,
  bit4(k=12,pad pos,fill)=1, bits5-7 (pad bits beyond P, fill bit per R-SER-05)=1,1,1
  -> 1+2+4+8+16+32+64+128 = 255 = 0xFF.
Sanity check against spec's own worked example (§14.3 note): alternating T,F,...,  byte0=0x55,
matches the same bit-k-is-value-k LSB-first method -> method confirmed.
-> "33 FF".

### quiza-q08
Dims (y,x), G_y=5, G_x=7 -> N=35. Channel index c=4. Tile (t_y,t_x)=(3,2).
§11.4: spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ = t_y·G_x + t_x = 3·7+2 = 23.
Disk ordinal (planar) = c·N + s = 4·35 + 23 = 140+23 = 163.
§15.1: "entry for the tile with disk ordinal k is the k-th entry, at region byte 20·k", entries are
20 bytes. start = 20×163 = 3260; end = 3260+20 = 3280.
-> disk ordinal 163; byte range [3260, 3280).

### quiza-q09
Run [12,16): ordinal 14 has well-formed offset/length fields but its stored payload bytes fail the
entry's own crc; ordinal 15 is a valid sentinel.
§16.2: "An entry whose only defect is that its stored bytes fail its crc is not transparent — its
offset and length stand, and the packing relation reads them as it does any other stored tile's."
-> must satisfy the packing relation (not transparent).

### quiza-q10
§2.4 reject-layer: "The outcome is prospective: it bars further service from the layer, and does not
retroactively invalidate content already returned under §19.2's validation timing (R-RDR-02)."
B and C were already returned before A's layer-scope failure was discovered.
-> stand as validly returned.

### quiza-q11
Superseded generation: G_y=4, G_x=8 -> N=32; channel c=2; tile (1,0); given disk ordinal 72
(check: s = 1·8+0=8; c·N+s = 2·32+8 = 72 ✓, confirms the formula/my reading).
Commit grows G_x to 10 (G_y stays 4): new N = 4·10 = 40.
New s = t_y·new_G_x + t_x = 1·10+0 = 10.
New disk ordinal = c·N_new + s = 2·40+10 = 90.
§11.2 rationale note: "A growth that changes no grid count ... moves no entry and adds none, ... so
does one that raises a grid count while another stays 0 .... Any other growth changes the index
content — entry_count and extent_length with it, and disk ordinals renumber wherever R-GEO-06 moves
them — so the layer's whole tile-index region is re-emitted." This growth (G_x: 8->10, both G_y and
G_x nonzero throughout) is "any other growth" -> disk ordinals renumber and the whole region is
re-emitted.
-> new disk ordinal 90; must be re-emitted at a new position.

### quiza-q12
Entry: offset = all-ones sentinel value; length = 1337 (not the sentinel); crc = 0.
§15.3 table: "offset = S ∧ length = S ∧ crc ≠ 0" is T6's row (both fields sentinel). Our entry has only
one field (offset) at the sentinel value -> matches "offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S"
which is T7's register condition: "A tile-index entry sets exactly one of offset and length to the
sentinel value."
-> T7.

### quiza-q13
§20.5: "Regenerating a region means classifying every entry in it: a sentinel is re-emitted unchanged,
and every other entry is re-pointed to where its stored extent now lies. An entry §15.3 classifies
reject-tile on a structural ground is neither — R-IDX-03 gives it no stored extent for a re-pointing to
target — so regenerating the region cannot proceed without meeting it... R-WRT-06 then leaves it two
disposals, since it can neither reproduce the entry nor invent a replacement: drop the layer, which
§20.4's table licenses and whose loss the rewriter SHOULD report as that table says, or refuse."
-> (c); the two options are: drop the layer, or refuse to rewrite (the file).

### quiza-q14
§7.4 layer-record field table: index_encoding "any other value — including 0, reserved 2-0x7F, and the
experimental range >= 0x80 (§10) — is a validity error at layer scope." §21.3 register row L31: "Layer
record's index_encoding is a value other than 1 — 0, reserved 2-0x7F, or experimental >= 0x80" lists all
three as *instances* of one row. No other passage in the file (grep over "index_encoding" confirms)
treats the experimental value differently for this field.
-> same row: L31 (both reject-layer / validity error at layer scope, identically).

### quiza-q15
§21.9 table: "addressed tiles per layer (entry_count) | 2^32" is a conforming reader's MUST-accept
minimum guarantee, explicitly "minimum guarantees, not caps." entry_count = 2^33 exceeds that floor.
"A file exceeding any of these remains conforming, and a reader MAY decline it..." -> (a) conforming.
"In every case, a refusal on resource grounds MUST be reported as a resource limit and not as a
validity error: the two send a user to opposite remedies..." (R-ERR-04) -> (b) resource limit, not
a validity/corruption error.
