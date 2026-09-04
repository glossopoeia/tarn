# Cleanroom round 31 — Adversary transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,790 lines, at the path the brief gave — it was where the brief said it was).
I opened no ADR, no PLAN.md, no OPEN-QUESTIONS.md, no conformance material, no
registry.json, no git history. I ran no web search or fetch, and listed no
directory.

Material appeared in my context before I began that is not part of the
specification: a project instruction file (CLAUDE.md pointing at AGENTS.md), an
index of the maintainer's auto-memory notes with titles naming TARN harness and
repair topics, a git-status snapshot with five recent commit subject lines, and
an MCP/skills listing. The commit subjects name ADR numbers and describe rule
changes. I disregarded all of it as evidence: I did not open any of the named
files, and I derived the changed-surface hypotheses below from the brief's own
section list plus my own reading of the document. I flag it here because the
commit subjects are the kind of thing that could have steered me, and a reader
of this transcript should discount anything of mine that looks like it came from
them. In particular I did *not* use them to decide where to look — the brief
already named seventeen sections, which is where I started.

Files I wrote, all under my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/adversary/`:

- `adv_crc.py` — a CRC-32C (Castagnoli) implementation, table-driven, reflected,
  init 0xFFFFFFFF, final XOR 0xFFFFFFFF.
- `adv_appA.py` — reconstructs Appendix A's 128 bytes from its hex dump and
  checks every checksum the document states for it and for §7.4/§15.4.
- `adv_count.py` — parses §21.2–§21.5's four register tables out of the markdown
  and counts rows and semicolon-separated instances.

Plus this transcript at the single output path the brief named. I did not read
that directory.

## 1. First pass: read the whole document

I read all 4,790 lines in six chunks before searching for anything. That was
deliberate: the brief's warning about hard wraps and blockquote `> ` prefixes
means a line-oriented grep is untrustworthy, and I wanted a mental index built
from reading rather than from matching. Every subsequent search I ran was over a
whitespace-normalised copy of the file (newlines and `>` markers collapsed to
single spaces) built in-process, never over the raw lines, and I ran a control
phrase through the same matcher each time (see §3 below).

## 2. Mechanical checks first, because they are cheap and falsifiable

### 2.1 The checksum function

`CRC-32C("123456789")` → `0xE3069283`; `CRC-32C(<empty>)` → `0x00000000`. Both
match §4.5's check vector, so my implementation is the document's.

### 2.2 Appendix A's minimal file

I typed the four hex-dump rows of Appendix A into `adv_appA.py` and rebuilt the
128 bytes.

- Length: 128. Matches §5.1's `[R-CNT-27]` floor and the Example's claim.
- Trailer at [64, 128). `CRC-32C(trailer[0,60))` = `0x402F157E`. The dump stores
  `7E 15 2F 40` at [124, 128) = `0x402F157E` little-endian. **Match.**
- Directory at [16, 20) = `00 00 00 00`, and `CRC-32C(<empty>)` = `0x00000000`.
  **Match** — a zero-record sequence with its terminal CRC.
- dir_offset = 16 ≥ 16 ✓; dir_length = 4 ≥ 4 ✓;
  dir_offset + dir_length = 20 ≤ F − 64 = 64 ✓; committed_file_length = 128,
  a multiple of 64 ✓; file_id = 0x0123456789ABCDEF ≠ 0 ✓; reserved [112,124)
  zero ✓; version_major = 1 ✓.
- Slack = 128 − (16 front + 4 directory + 64 trailer) = 44, which is exactly what
  the [20, 64) row says. The coverage walk of §9.7 claims the front block and the
  live trailer, so this arithmetic is the walk's, not mine.

I also re-derived §5.1's floor argument from scratch: dir_offset ≥ 16 and
dir_length ≥ 4 force dir_offset + dir_length ≥ 20; `[R-CNT-06]` forces that
≤ F − 64, so F ≥ 84; F mod 64 = 0 forces F ≥ 128. Agrees with `[R-CNT-27]` and
with §9.2's second Note run from F rather than from 0.

### 2.3 §7.4's worked layer record

I re-derived the whole example rather than trusting it.

- All-sentinel entry = `FF ×16 00 ×4` (20 bytes). Four of them = 80 bytes.
  `CRC-32C` of those 80 bytes = **0x80A34955**. The Example says `0x80A34955`,
  stored `55 49 A3 80`. Match.
- `CRC-32C` of the 4-byte array `55 49 A3 80` = **0xC4EE982E**. The Example says
  `crc_of_crc_array = 0xC4EE982E`. Match.
- Field offsets: name 4 bytes [0,4); layout 1 at 4; linearization 2 at [5,7);
  codec 2 at [7,9); filter 2 at [9,11); A 8 at [11,19); S 8 at [19,27);
  A_slab 8 at [27,35); rank 1 at 35; C 2 at [36,38); dimension entry
  (1+1 name, 8 extent, 8 tile extent) = 18 at [38,56); channel entry
  (1+4 name, 2 type, 1+4 fill) = 12 at [56,68); index_encoding 1 at 68;
  entry_count 8 at [69,77); crc_of_crc_array 4 at [77,81). Total **81**.
  The Example says 81 and decomposes it as 4 + 34 + 18 + 12 + 13; the nine
  scalars from layout through channel count sum to 1+2+2+2+8+8+8+1+2 = 34, and
  the trailing fixed fields to 1+8+4 = 13. Match on every term.
- `[R-CNT-17]`'s extent length for entry_count 4: 4×20 + ⌈4/2¹⁶⌉×4 = 84. The
  Example says 84. Match.
- Grid count ⌈100/32⌉ = 4. Match.

### 2.4 §15.4's all-sentinel segment constant

`CRC-32C` of 2¹⁶ concatenated sentinel entries (1,310,720 bytes) =
**0xEECB3BB2**. `[R-IDX-05]` and Appendix B both say `0xEECB3BB2`. Match.

### 2.5 §15.4's large-layer example

entry_count = 1,000,000. Segments = ⌈10⁶/65536⌉ = 16 (15 full covering 983,040
entries, the last covering 16,960). CRC array = 16×4 = 64 bytes. Region =
20,000,000 + 64 = 20,000,064. Tile 999,999 is at segment index
(999,999 − 983,040) = 16,959 within segment 15, at segment-relative byte
20×16,959 = 339,180. CRC array at [20,000,000, 20,000,064); segment 15 at
[19,660,800, 20,000,000) — length 339,200 ≈ "~339 KB". A full segment is
65,536×20 = 1,310,720 = 1.25 MiB. Every figure in the Example matches.

### 2.6 §11.4, §14.2, §14.3, §14.5, §20.3 examples

- (300,700) with T = (256,256), G = (4,8): tile (1,2), s = 1·8+2 = 10; in-tile
  (44,188); ordinal 44·256+188 = 11,452; planar channel 2 disk ordinal
  2·32+10 = 74; entry at [1480,1500). All match.
- Planar C = 4, N = 32: channel 3's tiles are ordinals 96..127, 32 entries. Match.
- Interleaved (2,3), a:uint8 b:uint16 → Q = 3, decoded size 18; ordinal 5 at
  [15,18). Planar b: 12 bytes, ordinal 5 at bytes 10–11. t:float32 m:bool →
  Q = 5, size 30, ordinal 5 at [25,30). All match.
- Packed bool P = 10, alternating from true: byte 0 = 0x55; values 8,9 = true,
  false → bits 0,1 = 1,0; with fill true the six pad bits set → 0xFD; with fill
  false → 0x01. `55 01` / `55 FD`. Match.
- Extents (5,5), tiles (4,4): grid 2×2, edge tile (1,1) has one real position and
  15 padding; one uint16 channel → 32 bytes. Match.
- 32-tile index region: 32×20 + ⌈32/2¹⁶⌉×4 = 644. Match.

### 2.7 The register's own arithmetic

`adv_count.py` parses the four register tables. Rows: F 35, L 49, T 26, R 10 —
**120**, matching each subsection's stated count and §21.8's "120 conditions".
Instances, counting a cell of `—` as one and otherwise counting
semicolon-separated items: F 56, L 116, T 55, R 50 — **277**, matching §21.8's
"277 instances" exactly.

I then hand-checked a sample against §21.1's individuation rules, because a
matching total proves consistency and not correctness:

- L21 (`entry_count` vs the geometry-derived count): "does not equal", two
  magnitudes, two layout formulas → 2×2 = 4. Cell has 4. ✓
- L22: two directions plus the two slot/count special cases → 4. Cell has 4. ✓
- T3 and T14: "not exactly"/"differs from", three layout formulas × two
  directions → 6 each. Both cells have 6. ✓
- T21: "larger than" bounds the comparison in one direction, three layouts → 3.
  Cell has 3. ✓
- T22: "does not equal", three layouts × two directions → 6. Cell has 6. ✓
- L44: "exceeds", one direction, three layouts → 3. Cell has 3. ✓
- L29/L39: A_slab and A each get three alternatives; note L39 excludes A = 0
  because that means "none declared" and L29 includes A_slab = 0 because with
  S ≠ 0 zero is out of range. The asymmetry is correct.
- R4: eight frame alternatives × two containers = 16. Cell has 16, and the
  alternatives are exactly the ones §18.2 carries over or states, minus the two
  §18.2 explicitly routes outside the register (undisclosed dictionary use, an
  unwitnessed condition; and the buffer-sizing bar, which binds a reader).
- R5: two failure modes × key/string-value × two containers = 8. Cell has 8. ✓

So the instance counts are not merely self-consistent; the ones I sampled follow
§21.1's stated rules.

## 3. Search discipline

Every phrase search ran over the normalised text, and I paired each sweep with a
control phrase I knew was present in the passage. The control I used most was
`no writer under this text`, which occurs once — a phrase that spans a hard wrap
in the raw file (§6.3 breaks it after "under") and returns zero from a
line-oriented grep. My normalised matcher returns 1 for it, which is what tells
me a zero from the same matcher is a real zero.

Sweeps and hit counts (normalised text):

- `ignore-lane` 14, `ignore lane` 3, `incompat lane` 4, `incompat-lane` 2
- `originates` 1, `copy forward` 1, `copied forward` 1, `carries the input` 1,
  `set no other` 1, `sets no other` 1, `no other set` 1
- `drop` 20 occurrences dumped in full with context
- `MUST_UNDERSTAND = 1` 4, `MU = 1` 21, `top-level` 58
- `disk ordinal` 16, `de-address` 4, `re-declared freely` 3,
  `geometry change renumbers` 1, `such a tile` 3, `carve-out` 3, `§14 bar` 9,
  `the other bar` 1, `bar beside` 2
- `otherwise free to make` 1, `only effect is the drop` 1

## 4. The three decisions, taken one at a time

### 4.1 The removed gate — §20.4's MU = 0 / PE = 0 row

The row now reads:

> MU = 0, PE = 0 | Retain byte-identical, or drop it — its extent becoming
> slack. The licence is the bit's own: the writer that stored PE = 0 declined
> preservation across edits, so an updater MAY drop the record in any commit it
> is otherwise free to make — one whose only effect is the drop included — and a
> compactor MAY drop it whenever it rewrites the file.

I hunted for sentences written under a narrower licence. The `drop` sweep found
every occurrence:

- §20.3 step 2: "MUST NOT drop the record save where §20.4 licenses the drop" —
  defers entirely, no gate of its own. Clean.
- §20.5: "less any record §20.4 lets it drop"; "Dropping is the one disposal that
  answers, and only where §20.4's table licenses it"; "no drop is available, a
  tile-index entry being no record §20.4's table licenses dropping" — all defer.
  Clean.
- §20.4's own following paragraph: "No commit therefore removes a layer record,
  or a user-metadata record at either scope" — derived from both registered types
  carrying PE = 1, not from any gate on the shape of the commit. Clean.
- §21.6's experimental-MU = 0 row: "preserved or dropped per its PE bit" —
  consistent with the widened licence, and carries no shape condition.
- §23.1: "a record's extent goes the same way whether a commit drops the record
  (§20.4) or supersedes it" — no gate. Clean.
- §20.4's Rationale: "the directory a commit emits differs from the one it
  supersedes exactly by the records modified, added, or dropped" — a
  drop-only commit satisfies this (the difference is one dropped record). Clean.
- §5.1's Example: "a commit that touches no layer re-emits the directory, the pad
  and the trailer alone" — which is exactly the shape of a drop-only commit, and
  is already sanctioned. Clean.
- §20.3's shape catalogue (a)/(b)/(c): a drop-only commit is not listed under
  (c), but (c)'s list is exemplary ("clearing a slab declaration, renaming a
  layer, or changing a channel's fill value where…") and the paragraph goes on to
  exclude one case explicitly ("Editing user metadata is not this shape"), which
  is what an exemplary list does. I opened this as a suspicion and closed it.

I also checked whether the widened licence can produce a file a verifier would
reject. It cannot: a directory that omits a PE = 0 record is a complete
directory, the dropped extent becomes slack, `[R-CNT-21]` counts it, and
`[R-CNT-02]`'s partition is unaffected. And it cannot collide with `[R-WRT-08]`
("MUST NOT re-encode … MUST NOT modify one except by relocating its extent"),
because dropping is neither re-encoding nor modifying and the table licenses it
by name. **Nothing found here.**

### 4.2 The added MUST NOT — the ignore-lane bit, four normative places

I put the four side by side.

1. §2.3 `[R-CNF-02]`: "§6.3's flags rules against a set ignore-lane bit — a
   creator's flags = 0, and an updater's or compactor's copy-forward and
   set-no-other (§20.5) — and §6.2's pre-trailer gap longer than `[R-LIF-02]`
   step 5's pad are the cases this text states".
2. §6.3 `[R-CNT-08]`: "a writer creating a file under this text MUST write
   flags = 0 … A compactor, though its output is a new file, carries the input's
   unknown ignore-lane bits into its output trailer rather than writing
   flags = 0, and sets no other (§20.5, `[R-WRT-06]`). An updater MUST copy
   forward unknown ignore-lane bits of the file it modifies, MUST NOT clear them,
   and MUST NOT set any other: no writer under this text originates an
   ignore-lane bit".
3. §20.3 step 6 `[R-WRT-04]`: "unknown ignore-lane flag bits copied forward and
   no other set (`[R-CNT-08]`)".
4. §20.5 `[R-WRT-06]`: "The output trailer MUST copy the input's unknown
   ignore-lane flag bits forward and set no other, in place of the flags = 0 §6.3
   requires of a file created under this text (`[R-CNT-08]`)".

(Appendix G item 8 is a fifth, non-normative, and agrees: "`flags` = 0. The
`flags` half is a creator's rule … a compactor adopting the profile carries its
input's unknown ignore-lane bits forward instead, setting no other".)

Word-for-word differences I found and what each amounts to:

- §6.3's compactor clause is a bare declarative, not a MUST; §20.5's is a MUST.
  §20.5 supplies the deontic force and §6.3 cross-references it. No gap.
- §6.3 says a creator "MUST write flags = 0", which on its face also binds a
  compactor's output (a new file created under this text). §6.3 carves the
  compactor out in the very next sentence, and §20.5 says its rule stands "in
  place of the flags = 0 §6.3 requires of a file created under this text". So the
  two MUSTs are not jointly binding on one actor.
- I tested for joint unsatisfiability on the `flags` field. Under this text no
  ignore-lane bit is *known*, so "unknown ignore-lane bits" is every set
  ignore-lane bit, and "copy forward … set no other" fixes the output's ignore
  lane to equal the input's exactly — satisfiable, and satisfiable
  simultaneously with the incompat lane being zero, because an updater or
  compactor meeting a set incompat bit is a reader first and rejects the file
  (§6.3's closing sentence) so no input can carry one.
- §2.3 scopes its conduct-rule declaration to "flags rules **against a set
  ignore-lane bit**", which correctly leaves a creator that sets an *incompat*
  bit outside the declaration — that file is nonconforming (F19). This is precise
  where it could easily have been sloppy.
- I checked whether §9.2's newly-declared conduct rule (the step 4 and step 6
  barriers) makes §2.3's "are the cases this text states" false. It does not:
  §2.3 has two categories, and the barriers fall in the first (obligations that
  govern conduct rather than output at all — "a barrier … leaves no trace in the
  bytes"), whose examples are introduced by "A few obligations" and are
  illustrative. The "are the cases this text states" closes only the second
  category, the obligations whose violation is *expressly declared* not to be a
  file-conformance violation, and the barriers are not in it.
- §20.5's carried-feature paragraph names "the two of §10.1's four vehicles §21.6
  makes conforming" and then "one row for each of the other seven spaces §10.2
  tabulates (L31, L33, L34, L36, L43, L45, R1)". I checked this: §10.2 tabulates
  eight spaces; excluding record type leaves seven; the seven rows named map
  one-to-one onto index encoding, linearization, sample type, channel layout,
  codec, filter, metadata encoding. Correct.

**Nothing found here.** This is the passage the brief pointed hardest at, and it
survives a word-for-word comparison.

### 4.3 The widened carve-out — §20.3 step 4

The carve-out now names two mechanisms:

> Dropping a tile out of the addressed set is not itself such an alteration — a
> tile the new state does not address carries no §14 obligation and its extent
> becomes slack, whether §11.2's grid count fell, which is a shrink, or a planar
> channel was removed, which is not one and which the bar beside this one judges
> on its own ground above

and §11.1's Rationale carries the same pair. I built concrete commits against
both bars.

Layer: planar, C = 3 channels (a, b, c), N = 2 spatial tiles, entry_count = 6.
Disk ordinals: a → 0,1; b → 2,3; c → 4,5.

- **Case 1.** Gen 1 stores a's tiles; b and c all sentinel. Commit removes b.
  c re-indexes 2 → 1 and its ordinals move 4,5 → 2,3, but c stores nothing, so
  the ordinal bar is not engaged ("a commit that moves only the ordinals of
  channels the superseded generation stored no tile for alters nothing this
  bars"). a is unmoved and unchanged. Permitted. entry_count 6 → 4, index region
  re-emitted, `[R-CNT-17]` gives extent_length 4×20 + 4 = 84.
- **Case 2.** Same, but gen 1 also stores c's tiles. Removing b now moves c's
  stored tiles → barred by the ordinal bar. Correct.
- **Case 3.** Gen 1 stores only b's tiles. Commit removes b. b's two tiles are
  de-addressed; their extents become slack; c moves but stores nothing.
  Permitted. This is the widening's own case, and it works.
- **Case 4.** Gen 1 stores b's tiles and c's tiles. Removing b moves c's stored
  tiles → barred. Correct.
- **Case 5.** Removing the *last* channel (c) with a and b stored: no channel
  re-indexes, c's tiles de-address, permitted — and this strands N tiles' worth of
  payload as slack in a commit that reads like a directory edit. §20.3 covers the
  economics with a SHOULD ("the recommendation below to produce a new file
  instead reaches a commit that would strand a large share of a layer's stored
  bytes this way too") and §23.1's list of unreachability-producing operations is
  expressly not closed. Both clean.
- **Case 6.** Interleaved layer, remove a channel: "removing one of its channels
  changes Q and so is the §14 bar's subject wherever the layer stores a tile."
  Q = ΣBᵢ changes, so the decoded size and every in-sample offset change.
  Correct.

Then I looked for the sentence written under the old, one-mechanism rule. I found
one — §20.3 step 4's re-emission parenthetical — and one antecedent problem in
the widening's own prose. Both are written up as findings 3 and 4 below.

I also checked whether removing a planar channel can move the ordinal of a tile
the moved channel holds under a *malformed* entry, which §3.1 counts as "stored"
(an entry that is not the sentinel). It can, and the ordinal bar then bars the
commit, which is the right answer and needs no special text. Where the malformed
entry belongs to the removed channel itself, the commit is permitted and the
entry simply ceases to exist, which is also right.

Finally I asked whether any permitted channel-declaration change can produce two
different index regions under the two readings of the re-emission clause (see
finding 3). It cannot: the ordinal bar permits a move only for channels the
superseded generation stored no tile for, whose entries are therefore all
sentinels and byte-identical wherever they land. That is why finding 3 is graded
not byte-level; the bar is calibrated so the renumbering is unobservable.

## 5. Attacks I built and what foreclosed them

### 5.1 The smallest and emptiest files

- 128-byte zero-layer file (Appendix A). Conforming; every check re-derived above.
- A layer with rank 1, E₀ = 0, T₀ = 1, C = 1, bool channel, fill 0x00, planar,
  **codec 4 (lz4)**, filter 2 (byte-shuffle), entry_count 0, extent slot (0,0),
  crc_of_crc_array 0. N = 0 so no tile is addressed; `[R-COD-07]`'s cap is
  quantified over addressed tiles, so codec 4 is legal here (§17.2's Note states
  this outright); filter 2 on a packed bool plane has s = 1 and is the identity
  (`[R-COD-10]`); `[R-ENC-04]`'s designated quantities are all in domain. Two
  verifiers must both certify. Foreclosed by §17.2's Note and `[R-GEO-02]`.
- The same layer with codec 4 and E₀ = 1, T₀ = 2⁴⁰, C = 1 float64 interleaved:
  N = 1, one addressed and unstored tile with decoded size 2⁴³ > 0x7E000000 →
  L44, reject-layer, even with nothing stored. §17.2's Note: "The escape ends
  exactly when the layer's addressed-tile count rises above 0". Foreclosed.
- The same layer with codec 1: conforming, and §21.9's 256 MiB tile guarantee is
  exceeded, so a reader MAY decline the layer on resource grounds while another
  serves fill from it. Both conforming — licensed by `[R-ERR-04]` and recorded in
  §21.9's per-instance paragraph ("ranges over a layer's **addressed** tiles,
  stored or not"). Not a defect.

### 5.2 Boundary values on every size, offset, count

- F = 64: impossible, dir_offset + dir_length ≤ 0. F ≥ 128 forced.
- dir_length = 4 (zero records) and dir_length = 5 (a one-byte record sequence):
  the second is F29 either as a truncated header or as trailing residue. Both
  instances are in F29's cell and both are reject-file, so no verdict forks; §24
  already handles a file that cannot isolate one instance.
- dir_offset > 2⁶³ − 1: fires F2 and, necessarily, F3 (the sum exceeds the domain
  whatever dir_length is). §21.1's specialization property decides it in F2's
  favour and says the list of such pairs "is not offered as closed". Same
  detector, same tier, same outcome; no fork.
- Extent slot (0, 0) legal on any record but a user-metadata record (F21/L10);
  index entry (0, 0) illegal (T10 and T8 both, which merely overlap). §15.2's
  Rationale calls the zeroed-region case out by name.
- Alignment A = 2⁶² with two stored tiles: distinct multiples of 2⁶² inside
  [16, F − 64) with F ≤ 2⁶³ − 1 admit exactly one value, so such a layer can
  store at most one tile. Legal, degenerate, and no rule is broken.
- A_slab = 1: the alignment condition is vacuous; §16.2's Note says exactly that
  ("With A_slab = 1 a slab is contiguity-only").
- Codec 3 on an 18-byte tile: the Window_Descriptor cannot express below 1 KiB,
  so the frame must be single-segment, and then Window_Size = Frame_Content_Size
  = decoded size, satisfying both `[R-COD-06]` constraints. §17.2's Note derives
  this and I re-derived it against RFC 8878's window formula (windowLog = 10
  minimum → 1024). A 1024-byte tile can be either. Foreclosed.
- P = 1 packed bool plane: ⌈1/8⌉ = 1 byte, 7 pad bits, all fixed to the fill bit
  by `[R-SER-05]`. §14.4's Note states the coincidence with the interleaved form
  exactly when the fill is false; I checked it bit by bit.

### 5.3 Two structures claiming the same bytes

I enumerated the overlap cases against `[R-CNT-13]` and F33/L18:
same layer → reject-layer; two layers → reject-file; layer against non-layer →
reject-file; two non-layer structures → reject-file. Complete. The one hole I
looked for — a claimant overlapping the *front signature block*, which §5.2
classifies as neither a structure nor slack — is closed explicitly in F33's own
cell: "a claimant reaching the front signature block or the live trailer is
instead caught by the bounds rows F9/F10, F30/F31/F32, L15/L16/L17 and T8/T9,
each at its own tier", down to naming which row a (0, N) slot lands in.
I could not build an overlap with no row.

A layer's tile-index region placed *inside* the directory region is a real
construction: the slot rules (offset ≥ 16, offset + length ≤ F − 64) permit it,
and only the verifier-detected overlap rule catches it. A reader would parse the
directory bytes as index entries and almost certainly fail a segment CRC — but a
crafted file could pass. Both verifiers reject on F33, so no fork. `[R-CNT-13]`
says readers are not obliged to detect overlap; that is stated, not a gap.

### 5.4 The reader/verifier seam

I walked every §21 row whose Detector is *verifier* and asked whether a reader
meeting the same file diverges: F7, F25, F26, F27, F28, F33, L18, L25, L40, L41,
L42, L46, L47, L48, L49, T2, T4, T5, T26. In each case the governing rule states
what a reader does — serve the structure unchanged for `[R-CNT-22]` and
`[R-MTA-05]`, resolve the byte for `[R-SER-08]`, no obligation at all for the
rest — and `[R-CNF-12]` licenses a reader that does detect one to reject. §21.1's
closing paragraph anticipates the whole class. The only place a reader is
*obliged* to differ from serving-through is `[R-SER-08]`, and that is finding 5.

### 5.5 Is any detectable file-conformance violation missing a row?

This is §21.1's own normative claim, so I tested it. I walked every requirement
identifier in the document and asked what file witnesses its violation and which
row records it. Full mapping in §6 below. I found no requirement stating a
detectable file-conformance violation with no row. The cases with no row are all
accounted for by one of three stated devices: a SHOULD (`[R-CNT-03]`,
`[R-CNT-09]`, `[R-CNT-26]`, `[R-ENC-14]`, `[R-LIF-07]`, `[R-TYP-10]`), a conduct
rule (`[R-EXT-03]`, `[R-MTA-06]`'s registry-version clause, `[R-LIF-02]` steps 4
and 6, `[R-CNT-08]`'s ignore-lane rules, `[R-CNT-05]`'s pad length,
`[R-PRV-01]`), or §21.7's unwitnessed/no-condition classes (`[R-ENC-06]`,
`[R-LIF-01]`, `[R-GEO-06]`'s ordinal assignment, `[R-SER-01]`'s value order,
`[R-COD-10]`'s stride where nothing structural constrains the result,
`[R-COD-06]`'s undisclosed dictionary, §7.4's nesting prohibition — which carries
its own Note saying so).

The flag-bit rows are complete in a way worth recording, because it is the kind
of thing that is usually incomplete: F25/F26/F28 cover *non-layer top-level*
records and L46/L47/L49 cover *a layer record or a sub-record*, and between them
every record position is covered exactly once. Same for the extent-slot rows
(F30/F31/F32 against L15/L16/L17) and the domain rows (F2 against L1, F3 against
L2, with T11/T12 for index entries).

### 5.6 Format-major reach

§21.2 says exactly F8, F14, F6 and both of F1's instances reach a file declaring
a major other than 1. I derived it independently from `[R-CNT-24]`: what a future
major cannot redefine is the trailer magic at F − 64, version_major/minor at
F − 56, a CRC-32C at F − 4 over [F − 64, F − 4), and the front block. That yields
the trailer magic (F8, F1's trailer instance), the trailer CRC (F14), and the
front block (F6, F1's front instance) — and nothing else. F13's 64-alignment is
format major 1's; F17's committed_file_length sits in the 48 redefinable bytes;
F15's reserved bytes likewise (§2.3's Note says so); F5's 128-byte floor derives
from major-1 minimums (§2.3's Note says so). Agrees exactly.

I then built the diagnostic fork: a file with version_major = 2 and a bad trailer
CRC. F14 reaches, so `[R-CNF-13]` obliges rejection "on the ground of the
requirement stating it rather than on capability grounds" — corrupt, not
unimplemented-major — and a verifier reports *nonconforming*, not *cannot
establish*. §6.2's validation order (magic, CRC, version gate) already puts the
CRC first. Foreclosed.

And a file with version_major = 2 and a bad front block: a reader holding
[0, 16) resident rejects it as corrupt; a reader that would have to fetch them
MAY omit the check and rejects it as an unimplemented major. Two conforming
readers, two different diagnostics on one file — but the same verdict (reject),
and `[R-CNT-04]` licenses the deferral by name. Not a fork in bytes or verdicts.

### 5.7 The pre-trailer gap

A file whose pre-trailer pad is 128 bytes rather than the pad to the next
64-byte boundary. §6.2: "a longer gap is conforming, and no conforming commit
produces one." So it is a conforming file that no conforming writer emits — an
odd set, but §2.3 `[R-CNF-02]` declares it deliberately, and I could not make two
verifiers disagree: the gap is slack, and F7 bars only a *structure* in it.
Foreclosed.

### 5.8 User metadata

- extent_length 5 exactly: a one-byte document. Under encoding 1 it is not
  well-formed JSON (R7); under encoding 2 it cannot carry the four-byte frame
  magic (R4). Both ignore-record. Foreclosed.
- A 20 MiB verbatim (encoding 1) document. §18.2 makes the bound the reader's
  own, no smaller than §21.9's 16 MiB. Reader A decodes it; reader B declines it
  (ignore-record on resource grounds); verifier A certifies; verifier B reports
  *cannot establish*. Four actors, three outcomes, all conforming — because
  `[R-ERR-04]` and `[R-CNF-10]` make the bound a capability and §21.6 registers
  the decline as a non-violation. This is designed divergence, not a fork: no
  actor reports *nonconforming*.
- A 10 MiB single-segment-framed document: Window_Size = Frame_Content_Size =
  decoded length, which exceeds §21.9's 8 MiB Window_Size row while staying inside
  the 16 MiB document row. §18.2 states this case in terms ("§21.9's
  user-metadata row bounds a document's decoded size; it does not relieve the
  frame carrying it of the `Window_Size` row") and tells a writer to use a
  Window_Descriptor instead. Foreclosed, and unusually thoroughly.
- Experimental-range encoding: no content rule attaches (`[R-MTA-10]`), the
  extent's terminal CRC still applies (`[R-CNT-20]`, R2), certification is
  unaffected, and the verifier must name the record. §22.3's fourth residue and
  §9.7 both restate it consistently. Foreclosed.

### 5.9 Slabs

- A run with one stored tile: the packing relation is vacuous, the alignment
  condition applies. A run with none: "imposes nothing." Both stated.
- An entry whose stored bytes fail their crc is *not* transparent to run
  continuity, while a structurally-invalid entry is. §16.2 states both, §15.3
  states both, L41's cell restates both. I checked all three against each other
  word for word and they agree.
- A shrink moves planar disk ordinals (c·N + s with N falling), but the ordinal
  bar is scoped to *channel declaration* changes, and a shrink is a geometry
  change, which is the re-emission rule's own stated occasion for renumbering. So
  the two bars partition the renumbering cases correctly. This is the check that
  turned up finding 3: the partition leaves a third case — a permitted channel
  move — that the re-emission parenthetical does not name.

## 6. Findings

### adversary-01 — AMBIGUITY — §2.3 `[R-CNF-03]`, §21.9 `[R-ERR-04]`, §21.6

The acceptance duty is stated without the qualifier §21.6 declares load-bearing.

§2.3:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1

§21.6's closing paragraph:

> The second is an **experimental-range top-level record type carrying MU = 1**
> (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
> makes the file conforming all the same. The qualifier is load-bearing — the
> same type as a layer sub-record is reject-layer and never a ground to refuse
> the file (`[R-CNT-18]`), so only the top-level case is a file a reader refuses

§2.3's carve-out is unqualified: a conforming file carrying an experimental
MU = 1 record *as a layer sub-record* falls outside the acceptance duty as
written, even though §21.6 says such a file is not one a reader refuses.
§21.9 repeats the unqualified form ("an unimplemented MU = 1 type").

Permitted readings: (a) the carve-out means what it says, so no acceptance duty
attaches and a reader may refuse the whole file; (b) the carve-out is shorthand
for §21.6's top-level case, which §2.3's own parenthetical points at ("§21.6's
closing paragraph names the other two"). I pick (b), because `[R-CNT-18]` states
an express prohibition — "an unknown sub-record type with MU = 1 is reject-layer,
and where the file is otherwise conforming a reader MUST NOT reject the file for
it" — and an absent duty in one rule cannot license what another rule forbids.
Without (b) an implementer builds a reader that refuses a conforming file over
one bad layer, which is the exact behaviour §21.6 and `[R-VEC-04]` exist to
distinguish.

### adversary-02 — OBSERVATION — §11.1's Rationale block

A labelled (therefore non-normative, `[R-CNF-01]`) block restates §20.3's two
bars and omits the growth permission §20.3 states as an express exception:

> Of its two bars the one reaching a shrink or a growth is the §14 bar: a shrink
> is barred wherever it alters what §14 fixes for such a tile — whether or not
> the new state still stores it — and permitted wherever it does not: a tile
> dropped out of the addressed set … carries no §14 obligation and its extent
> becomes slack; a tile the superseded generation did not store carries none
> either; and a new padding position whose stored byte already holds the fill
> alters nothing.

The block asserts the §14 bar reaches a growth and then discusses growth only
through its effect on entry_count and the index. §20.3 says the opposite side of
it in terms:

> an extent MAY **grow**, since a position that becomes real held, for each
> channel the position carries, that channel's fill (§14.5), and fill is a legal
> sample value. The bar's carve-out does not reach a growth: it covers a position
> whose stored byte already holds the fill it keeps, not one that ceases to be
> padding, so this is an exception the permission states rather than one the
> carve-out supplies.

An ordinary growth of a layer with an edge tile changes the set of padding
positions of a prior-generation stored tile — the first item in the §14 bar's own
list — so a reader who takes §11.1's three carve-outs as the whole of the test
concludes almost every growth is barred. The block does say "§20.3 states
normatively, and governs", and the three carve-outs are attached grammatically to
"a shrink"; the block also carries the widened two-mechanism de-addressing
carve-out correctly. This is decidable against §20.3 and costs only the reading.

### adversary-03 — AMBIGUITY — §20.3 step 4

The re-emission clause's parenthetical is under-inclusive after the carve-out was
widened:

> and every other entry byte-identical at its disk-ordinal position (a geometry
> change renumbers ordinals wherever `[R-GEO-06]` moves them)

The paragraph two below it says the ordinal bar exists precisely because a planar
channel-declaration change disturbs "the re-emission rule above, whose only
stated occasion for a renumbering is a geometry change." But that bar reaches
only moves of tiles the superseded generation *stores*. A commit that removes or
reorders a planar channel whose neighbours store nothing is permitted, changes no
geometry, and renumbers ordinals — an occasion the parenthetical does not name.

Permitted readings: (a) the operative clause is "byte-identical **at its
disk-ordinal position**", the position being whatever the new declarations
assign, and the parenthetical is one illustration; (b) the parenthetical
restricts renumbering to geometry changes, so a permitted channel-declaration
change must keep entries at their old positions. I pick (a): under (b) a channel
removal is unimplementable, since entry_count falls and the old positions do not
exist. An implementer who reads (b) has no way to emit the index for a commit
§20.3 licenses.

Not byte-level: the ordinal bar permits a move only for channels the superseded
generation stored no tile for, so every moved entry is a sentinel, and the two
readings produce identical index bytes wherever (a) and (b) are both satisfiable.
I checked this by construction — planar C = 3, N = 2, a stored, b and c
sentinel, remove b — and could not make the emitted region differ.

### adversary-04 — AMBIGUITY — §20.3 step 4, the ordinal-bar paragraph

> Removing a planar channel de-addresses its N tiles: those the superseded
> generation stored carry no §14 obligation afterwards and their extents become
> slack (§5.2), as a shrink's de-addressed tiles do below … As there,
> de-addressing rescues nothing: a commit that also alters what §14 fixes for
> such a tile is barred.

"such a tile" has no clean antecedent. The nearest noun phrases are "its N tiles"
and "those the superseded generation stored", i.e. the de-addressed tiles of the
removed channel — but the same sentence pair has just said those carry no §14
obligation, so on that reading the sentence bars what the clause before it
permits. The parallel sentence in the shrink paragraph is explicit where this one
is not: "neither does it rescue a commit that damages a prior-generation stored
tile."

Permitted readings: (a) "such a tile" = any tile the layer stores in the
generation this commit supersedes, so the sentence says removing a channel does
not license damaging the *surviving* channels' stored tiles; (b) "such a tile" =
a de-addressed tile of the removed channel, which contradicts the preceding
clause. I pick (a), on the strength of "As there" pointing at the shrink
paragraph's formulation. An implementer taking (b) refuses commits §20.3 permits
— e.g. removing a planar channel while re-typing a different channel none of
whose tiles are stored.

### adversary-05 — OBSERVATION — §14.2 `[R-SER-08]`, §19.4 step 8, §12.3

> A reader that does not reject the tile and returns the value — whether or not
> it detected the violation — MUST report 0x00 as false and every other byte as
> true.

The rule fixes the *logical* value and does not say which byte the reader hands
back. §19.4 step 8 has the reader "Return the requested values' bit patterns
unaltered … for every byte a conforming file can carry, the whole of this step
(`[R-SER-08]` fixes what a reader returns for the one byte a conforming file
cannot)", and `[R-TYP-04]` calls this "the one case where a reader resolves a
byte to a value rather than passing it through". Two conforming readers handed a
tile whose interleaved bool byte is 0x7F can both report *true* while one returns
0x01 and the other returns 0x7F unaltered. §14.2's Rationale claims to have
closed exactly this: "two readers handed the same malformed tile could disagree
about a sample and both be conforming, which is the divergence this document
exists to prevent."

It is decidable, but only by assembling three passages: §14.2's table and
Appendix B fix the boolean encoding as 0x00 = false / 0x01 = true, and
`[R-TYP-04]` says "Wherever this specification treats two sample or fill values as
the same value, it means their encoded bytes are identical", so returning *true*
is returning 0x01. Not byte-level: the file is nonconforming, `[R-CNF-05]` bars
every conforming writer from emitting it under either reading, and no
accept/reject verdict moves — only what a reader hands its caller. Also worth
noting in passing that §19.4 and §21.1 both say "the one byte", where there are
254 of them; §12.3's "the one case" is the accurate form.

## 7. Honest summary

I did not find a byte-level fork. The three decisions the brief points at are, on
this reading, cleanly landed: the ignore-lane prohibition survives a word-for-word
comparison across all four normative restatements and the non-normative fifth;
the removed drop gate leaves no orphaned sentence anywhere `drop` occurs; and the
widened carve-out is stated consistently in §20.3 and §11.1 and behaves correctly
on the six commits I built against it. What the widening did leave behind is one
under-inclusive parenthetical (finding 3) and one stranded antecedent (finding 4),
both in §20.3 step 4 itself, which is the shape the brief predicted — a rewrite
opening something adjacent to what it closed — but neither moves a byte.

The register's completeness claim survived the strongest test I could run against
it: a requirement-by-requirement walk asking for the witness and the row. Its
arithmetic survived too — 120 rows and 277 instances, both exactly as stated, with
a sampled dozen cells re-derived from §21.1's individuation rules. Every checksum
and every worked figure I re-computed matched.
