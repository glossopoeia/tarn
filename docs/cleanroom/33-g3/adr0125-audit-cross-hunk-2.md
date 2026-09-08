# Cross-hunk audit 2 — by operation, not by rule

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole
file, in ranges, via `sed -n`) and all nineteen `hunk-NN.diff` files in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/`.
Did NOT read `full.diff`, `docs/`, `conformance/`, `spec/registry.json`, git history,
or the web. I ran `ls -la` on the case directory once before the brief's "do not list
that directory" registered; the listing showed only file names and sizes and I read no
file other than my nineteen hunks.

Context I did not ask for, and disregarded: a project instruction file
(`CLAUDE.md` -> `AGENTS.md`), a user auto-memory index naming prior TARN findings and
process notes, and an environment block naming recent commit subjects. None of it is
evidence about the specification and none of my conclusions rests on it. I name that it
appeared; I do not repeat its contents.

Files written (mine alone):
- `/private/tmp/.../r33-audit/scratch/cross-hunk-2/ops.py`
- this transcript.

## Method

I took the operations one at a time and read the document as the writer attempting each.
Four were worked to bytes on a concrete layer.

### The concrete layer

Planar, rank 1, dimension `x`, T = 32; channels uint16 with fill `0x0000`;
index_encoding 1. entry_count = C*N, extent_length = entry_count*20 +
ceil(entry_count/2^16)*4 (`[R-CNT-17]`), disk ordinal = c*N + s (`[R-GEO-06]`).

    E=100 C=2  -> G=4 N=4 entry_count=8  extent_length=164 ordinals 0:[0,3] 1:[4,7]
    E=100 C=3  -> G=4 N=4 entry_count=12 extent_length=244 ordinals 0:[0,3] 1:[4,7] 2:[8,11]
    E=128 C=3  -> G=4 N=4 entry_count=12 extent_length=244 (grid unchanged)
    E=128 C=2  -> G=4 N=4 entry_count=8  extent_length=164 ordinals 0:[0,3] 1:[4,7]
    E=256 C=1  -> G=8 N=8 entry_count=8  extent_length=164 ordinals 0:[0,7]
    E=200 C=2  -> G=7 N=7 entry_count=14 extent_length=284 ordinals 0:[0,6] 1:[7,13]

### Operation 1 — append a planar channel (worked to bytes)

Deciding sentence: 20.3 step 4, "a planar layer's channel list MAY be extended at its
end". C 2->3: entry_count 8 -> 12, extent_length 164 -> 244. Index content changes, so the
whole region is re-emitted at a new placement (step 4; `[R-WRT-04]`); channels 0 and 1
keep ordinals 0..7 byte-identical, ordinals 8..11 are new sentinels. Old 164-byte region
becomes slack, with the old directory, pad and trailer. Restatements: 11.1 Rationale,
13.3 Note, Appendix H updater. All agree.

### Operation 2 — grow an extent with no grid count changing (worked to bytes)

E 100 -> 128, T = 32, G = 4 both sides. entry_count and extent_length unchanged, entry
bytes unchanged, so index content is unchanged: the region is NOT re-emitted and the
layer keeps its extent slot ("A layer whose record alone changes keeps its extent
slot"). Only directory + pad + trailer are appended. 11.1: "A growth that changes no grid
count ... moves no entry and adds none, and taken alone touches the directory alone" —
agrees. 13.3 Note agrees. Positions x = 100..127 were padding in tile t=3 and held fill
by `[R-SER-05]`, so the principle's "a grown extent adds positions that held their
channel's fill (14.5)" holds exactly.

### Operation 3 — grow + shorten in one commit (worked to bytes)

(a) E 100->128 (G stays 4), C 3->2. entry_count 12 -> 8, extent_length 244 -> 164.
    Retained ordinals: channel 0 [0,3], channel 1 [4,7] — UNCHANGED. No ordinal moves;
    the count changes.
(b) E 100->256 (G 4 -> 8), C 2->1. entry_count 8 -> 8, extent_length 164 -> 164.
    Retained channel-0 tiles keep ordinals 0..3 (rank 1: s = t0). No ordinal moves and
    the count does not change. Ordinals 4..7 now denote channel 0's new spatial tiles
    (sentinels) where they denoted channel 1's tiles.
Both are cases hunk 10's new clause says cannot occur — see finding Y-03.

### Operation 4 — extension and shortening netting longer (worked to bytes)

Start C=3 [a,b,c], all uint16 fill 0x0000, E=100, N=4, entry_count 12, extent_length 244.
Commit: drop `c`, append `x` (int16, fill 0x0000) and `y` (uint16). New C=4,
entry_count 16, extent_length 324. Channel 2's stored tiles are carried forward
byte-identically at ordinals 8..11 and are now declared int16.
Nothing detects it: decoded size P*B = 32*2 = 64 both ways (T3, T14 silent); padding
positions hold `00 00`, which is int16 fill too (T4, T5 silent); not bool (T2 silent);
entry crcs unchanged (T1 silent); entry_count matches C*N (L21 silent); extent_length
matches the formula (L22 silent); fill length 2 = element size (L30 silent).
The file is conforming and a stored `FF FF` now reads -1 where it read 65535.
See finding Y-01.

### Operation 5 — rename an interleaved channel

Permitted: "its name, and its dimension and channel names, MAY change". Forbidden by the
same step's closing list: "any change to an interleaved layer's channel list ... are
rewrites". See finding Y-02.

### Other operations checked (not worked to bytes)

- Supersede / store / unstore a tile: index content changes -> whole region re-emitted at
  a new placement; superseded payload and old region become slack. 20.3's Example checks
  out: 32 entries -> 32*20 + ceil(32/65536)*4 = 644.
- Growth from and to zero: at E=0 the grid count is 0, N=0, entry_count 0, extent (0,0);
  the layer stores no tile, so it is freely re-declarable anyway. 11.1's "the growth that
  raises a zero-extent layer's only remaining zero grid count included" is right, and the
  "one that raises a grid count while another stays 0, the product holding at 0" case is
  right.
- Remove the last planar channel: its stored extents become slack (23.1 agrees, plural
  "channels"); entry_count drops by N; no other ordinal moves.
- Replace the last channel in two commits: commit 1 shortens, commit 2 appends. Legal;
  if commit 1 empties the layer, commit 2 meets a layer that stores no tile and may
  re-declare freely. Consistent.
- Point an appended channel's entries at extents a superseded generation's entries
  addressed: permitted. Those bytes are slack in the superseded live state, so claiming
  them creates no `[R-CNT-02]` overlap (F33, L18 range over the live state only). The new
  tiles must decode under the new declarations like any others.
- Clear a slab and declare an alignment in one commit: net A != 0, S = 0, so
  `[R-CNT-16]` is satisfied; 20.3's tail requires the aligned layer's stored tiles —
  "every one the new state keeps" — to satisfy the invariant or the declaration to be
  cleared. Decided.
- Re-declare an empty layer / empty and re-declare: "The tense is the prior generation's
  ... unstoring or superseding every tile of a layer and re-declaring it is one
  operation, and it is a rewrite." Decided; hunk 11 sweeps the Example's wording to match
  ("its new declarations", not "its new geometry").
- A commit touching no layer that adds a top-level metadata record: appends the document
  extent, then directory + pad + trailer. Hunk 2's insertion into 5.1 makes the Example
  agree with 20.3 shape (b). Correct.
- Editing a layer's user-metadata sub-record: appends a new extent, re-points the
  sub-record slot, re-emits the directory; the tile-index region is untouched
  ("a layer's sub-records are 20.4's subject whether or not the layer stores a tile").
- A compactor moving one layer's tiles and not another's: see finding Y-10.
- binary64 conversion at and around the largest finite value: see below.

### The 7.4 field table as the list's inventory (partition claim)

"Between them the two lists reach every declaration field of 7.4":
name -> permitted; layout, linearization, codec, filter, rank, index_encoding -> fixed;
alignment A, slab S, slab alignment A_slab -> permitted (declared / re-established /
cleared; `[R-SLB-04]` expressly contemplates "the slab declaration itself" changing, and
20.3's tail states the alignment case, so the value may change under "re-established");
channel count C -> permitted for planar, fixed for interleaved via "an interleaved
layer's channel list (its names aside)"; dimension entries: name permitted, extent
permitted (grow only), tile extent fixed; channel entries: name permitted, type and fill
fixed; entry_count and crc_of_crc_array -> "follow the commit"; sub-records -> 20.4's.
The partition holds after hunk 8's "(its names aside)", which is what closes the
interleaved-channel-name hole in the fixed side. What it does NOT close is the
gives-up restatement three paragraphs later (Y-02).

### The principle paragraph's arguments, one per permitted change

1. "a name enters no map" — true of one rename; see Y-08 for the pair.
2. "a grown extent adds positions that held their channel's fill (14.5), and fill is a
   legal sample value" — confirmed against `[R-SER-05]`, which makes padding content
   mandatory fill, and against 13.3 for wholly new tiles. Sound.
3. "an appended planar channel adds tiles at ordinals after every existing one, a disk
   ordinal being c * N + s with N the spatial-tile count" — sound; where a growth in the
   same commit changes N, "N" is the new state's, which `[R-GEO-06]` and the re-emission
   clause settle.
4. "a channel removed from the end takes only its own tiles out of the addressed set" —
   sound.
5. "a slab or alignment declaration governs placement (16), not a value, its coordinate
   or its padding" — sound.
The fifth fixed declaration group the paragraph does NOT argue for is the codec and the
filter; see Y-07.

### binary64 (hunk 7, hunk 17)

maxfinite  = 2^1024 - 2^971 = 1.7976931348623157e308
midpoint   = 2^1024 - 2^970 (a 309-digit integer)
Under roundTiesToEven the midpoint ties between maxfinite (odd significand) and 2^1024
(even, unrepresentable), so it rounds to 2^1024, overflows, and yields +inf — NOT finite,
so the document is unreadable. midpoint - 1 rounds to maxfinite and is readable.
Verified: `float(str(2**1024 - 2**970))` -> inf; `float(str(2**1024 - 2**970 - 1))` ->
1.7976931348623157e+308. So the repair decides all three cases the charter names, and
underflow too (1e-400 -> 0.0, finite, readable). Appendix F's added line agrees with
18.2's wording. This repair is sound.

## Sweeps run (with hit counts and controls)

    grep -n "shorten\|shortened\|shortening" tarn.md            -> 9 hits (1460, 1648,
        3194, 3198, 3200, 3271, 3275, 3565, 4191, 4745)  [control: "channel list" -> 8
        hits, so the file is being matched]
    grep -n "channel list" tarn.md                              -> 8 hits (1647, 3198,
        3199, 3205, 3211, 3251, 4191, 4744)
    grep -n "stores a tile\|stored a tile\|stored no tile\|keeps its declarations"
                                                                -> 8 hits
    grep -n "index content" tarn.md                             -> 4 hits (1661, 1955,
        3173, 3270)
    grep -n "tile-index region" tarn.md                         -> 19 hits
    grep -n "R-CNF-12\|R-MTA-05\|R-IDX-03\|R-GEO-06\|R-COD-07\|R-WRT-05\|R-CNT-25`"
                                                                -> 50+ hits
    grep -n "^#### 14.5\|^#### 4.6\|^#### 5.2\|^#### 18.2\|^#### 21.6\|^#### 9.7\|
        ^#### 11.4\|^#### 15.2\|^#### 16.1\|^#### 16.2\|^#### 13.3"  -> 11 hits
    grep -n "^| F[0-9]* " tarn.md                               -> 35 rows
    grep -n "^| L1[0-9] \|^| L2[0-9] \|^| L3[0-9] " tarn.md      -> 30 rows
    grep -n "^#### 7.4\|^#### 7.3\|^#### 7.5" tarn.md            -> 2 hits; 7.5 does not
        exist, which is the control that the pattern was live (7.3 and 7.4 both matched).

Every zero I relied on was paired: I never rested a conclusion on a search that returned
nothing without a companion search on the same passage that returned something.

## Blockquote label test applied to every hunk

- h02 (5.1)  : block opens "> **Example — a file after three commits.**" -> NON-normative.
- h05 (11.1) : block opens "> **Rationale.**" -> NON-normative; it says "20.3 states
               normatively, and governs", so the restatement is properly subordinated.
- h06 (13.3) : block opens "> **Note — sparse writing.**" -> NON-normative.
- h11 (20.3) : block opens "> **Example — the three shapes a commit takes.**" -> NON-norm.
- h12, h13 (20.5): block opens "> **Example — what compaction reclaims.**" -> NON-norm.
- h01, h03, h04, h07, h08, h09, h10 : running prose, no blockquote, no label -> NORMATIVE.
- h14, h15 : register table rows in 21.2 / 21.3 -> NORMATIVE (21.1 governs conflicts).
- h16 (21.6): running prose after the table -> NORMATIVE.
- h17 (Appendix F — Normative references) -> NORMATIVE.
- h18, h19 (Appendix H) : heading says "(non-normative)" -> NON-normative.
I applied the LABEL test, not the ">" test, in every case.

## Back-reference resolution (check 8), every hunk that inserts

- h02: "as well" in the next sentence -> still "in addition to the directory, the pad and
  the trailer". Unchanged by the insertion.
- h03: "and so does" -> "leaves the walk complete"; the following relative clause supplies
  the different mechanism, so no mis-resolution. "the walk" -> 9.7's coverage walk.
- h04: "it there" -> "at the file or the layer"; "for it" -> the document's defect. Both
  in-sentence. The next sentence's "The directory and the tile-index region are always
  raw" has no anaphor into the insertion.
- h05: "so does one that raises a grid count" -> "moves no entry and adds none, and taken
  alone touches the directory alone". Correct. "them" in "wherever `[R-GEO-06]` moves
  them" -> disk ordinals. Correct.
- h07: "that conversion" -> the decimal-to-binary64 conversion under roundTiesToEven that
  the inserted clause names. This is the repair working: before the insertion the nearest
  antecedent was the bare "an IEEE 754 binary64 value".
- h08: "these changes" -> the permitted list (unchanged); "one of these" -> the fixed list
  (unchanged); "Between them the two lists" -> permitted + fixed (unchanged); "the
  permitted side states the whole of what a commit MAY do to it" -> now includes the new
  restriction, which strengthens it correctly. "the last channel" -> of a planar layer.
- h09: "that" in "The permitted changes touch none of that" -> the preceding sentence's
  denoting-and-certifying clause; unaffected by widening the parenthetical.
- h10: "the clause above" -> step 4's re-emission clause ("Every layer whose stored-tile
  set or index content this commit changes ..."). Correct, but see Y-03. "These bounds"
  -> the four bounds just listed; before the repair the sentence said "The list", which
  ambiguously reached the permitted list — the repair fixes that, correctly.
- h13: "the ' marks B's" -> the prime in the figure. Resolves, but see Y-10.
- h16: "its own case" -> `[R-CNT-18]`'s sub-record case. Resolves; see Y-05 for what the
  analogy imports.
- h18: "that carries no top-level MU = 1 record ... and lies within" -> both relative
  clauses attach to "file". Slightly strained but resolvable.
- h19: "a modified one" -> a retained record that is logically modified. Resolves.

## Citations checked

PASS: `[R-CNF-03]` (h01, h18); 7.3 registers exactly two types, layer 0x0001 and user
metadata 0x0002 — the count "both" is right. `[R-IDX-03]` and 9.7 (h03) — 9.7 says in
terms "An entry `[R-IDX-03]` classifies reject-tile on a structural ground does not make
the walk incomplete: the walk passes over it". `[R-MTA-05]`, F27, L48 (h04) — F27 is the
file-scope unsorted-document row, L48 the layer sub-record one, both verifier /
certification, both governed by `[R-MTA-05]`. `[R-CNT-17]` (h05, h10) — states the
extent_length formula and the entry_count = addressed-tile-count identity. `[R-GEO-06]`
(h05) — disk ordinal c*N + s. 11.2 (h05, h06) — grid count ceil(Ei/Ti). `[R-WRT-04]`
(h05, h06) — 20.3 step 6's rule id, which carries the whole procedure. T3, T14, T4, T5,
T2 (h09) — T3 and T14 are the two decoded-size rows, T4 and T5 the padding-position and
pad-bit rows, T2 the interleaved bool byte; the order matches the order of the three
items in the sentence. `[R-COD-07]`, L44 (h10). `[R-ENC-04]`, `[R-GEO-01]`, 4.6,
`[R-ENC-15]` (h10). `[R-CNT-18]` (h16) — it does say, verbatim, "on a nonconforming file
`[R-CNF-12]`'s licence to reject on any detected violation is untouched". `[R-CNF-12]`
(h16) — "For a nonconforming file no acceptance obligation exists — a reader MAY reject
it upon detecting any violation, including violations whose assigned detector is the
verifier." `[R-ENC-04]` / F2 partition (h14) — F2 is the single-field domain row, so F3's
new "although each field alone is in domain" makes the two disjoint and matches T12's
wording exactly. `[R-CNT-12]` / `[R-CNT-18]` / `[R-ENC-07]` (h15) — 7.4 requires the
sub-record sequence to parse "with no residue", and F29 already carries the same clause
for the directory, so L14 now parallels F29. `[R-ERR-04]`, 21.6, 21.9 (h18).
`[R-WRT-05]`, 20.4 (h19) — 20.4 says "a record it modifies is new output under its writer
obligations". IEEE 754-2019 / 12.1 / 18.2 (h17) — roundTiesToEven is the default
rounding-direction attribute for binary formats, and the added clause matches 18.2's new
sentence word for word.

QUALIFIED PASS: 21.7 (h09) — 21.7's narrowing clause names "padding positions, pad bits,
and boolean bytes" and does not name a decoded size, so the cite warrants two of the
three items in the sentence it is attached to. See Y-07.
QUALIFIED PASS: 21.6 (h04) — 21.6 does say neither condition obliges a reader to reject,
but the same section's `[R-MTA-09]` row licenses a reader to decline the whole file over
a user-metadata document. See Y-06.
QUALIFIED PASS: `[R-CNT-18]` as an analogy (h16) — see Y-05.

## Analogy comparisons, verb against verb (check 7)

- h16: repair's verb — `[R-CNF-12]`'s licence "is untouched"; cited rule's verb —
  "on a nonconforming file `[R-CNF-12]`'s licence to reject on any detected violation is
  untouched", which in `[R-CNT-18]` is the second half of a pair whose first half is
  "where the file is otherwise conforming a reader MUST NOT reject the file for it".
  Ranges: `[R-CNT-18]`'s case can leave the file conforming; 21.6's two conditions
  make the file nonconforming by their own operation (`[R-CNT-22]`: "makes the file
  nonconforming"). Not the same set. See Y-05.
- h13: repair's verb — "any of whose stored extents moved"; cited rule's verb
  (`[R-WRT-06]`) — "regenerates each tile-index region any of whose stored extents the
  output relocates". Same quantifier, same set. PASSES.
- h10: repair's verb — "a permitted change holds exactly where the declarations it
  produces satisfy every rule they are subject to"; the paragraph's opening verb —
  "A permitted change holds provided the declarations AND GEOMETRY it produces stay
  within every bound they are subject to". "declarations" against "declarations and
  geometry". Since 11.2's geometry quantities are declaration-derived, the two ranges
  coincide; PASSES, narrowly.
- h05: repair's verb — "extended or shortened at its end, one or the other in a commit";
  normative verb (20.3) — "MAY be extended at its end or shortened from its end, but not
  both in one commit". Same range. PASSES.
- h19: repair's verb — "extended at its end or shortened from it (not both in one
  commit)"; same normative verb. PASSES.
- h06: repair's verb — "each commit that changes a layer's stored-tile set OR ITS INDEX
  CONTENT re-emits that layer's whole tile-index region"; normative verb (20.3 step 4) —
  "Every layer whose stored-tile set or index content this commit changes has its
  tile-index region re-emitted in full". Same range. PASSES. (The old wording's
  "only a change to entry_count does" was the false gloss and is correctly gone.)
- h18: repair's verb — "accepts every conforming file of a major it implements that
  carries no top-level MU = 1 record of a type it does not implement"; cited rule
  (`[R-CNF-03]`) — "MUST accept every conforming file of a format major version it
  implements, carrying no top-level record of a type it does not implement with
  MUST_UNDERSTAND = 1". Same range. PASSES.

## Findings

Y-01 hunk 8   — "a commit's net change ... is an extension or a shortening" does not
                decide a shorten-plus-extend that nets longer. BYTE-LEVEL.
Y-02 hunks 8, 10 — the gives-up list still says "any change to an interleaved layer's
                channel list" is a rewrite. BYTE-LEVEL.
Y-03 hunk 10  — "one taken with a growth moves ordinals whether or not the count changes"
                is false in two worked commits.
Y-04 hunks 1, 18 — Appendix H's reader checklist restates `[R-CNF-03]`'s handling duty
                and omits the record types hunk 1 added to it.
Y-05 hunk 16  — "the reader's side of them, and it is unchanged" is contradicted by the
                clause the repair appended to it.
Y-06 hunk 4   — "never makes the structural data it annotates unusable" against
                `[R-MTA-09]`'s row in the very section the repair cites.
Y-07 hunk 9   — the "but for" exception list is short: a codec change is a fixed-
                declaration change that reader-owed decode checks see.
Y-08 hunk 8   — the qualification closes one composition of permitted changes and leaves
                a dimension-name swap open. BYTE-LEVEL.
Y-09 hunk 8   — the gives-up list, which says it states rather than carves, omits the
                operation the qualification newly forbids.
Y-10 hunks 12, 13 — the Example's own caption disclaims offsets, and the added sentence's
                inference needs them.

## Candidates considered and dropped

- A_slab and A unconstrained by the permitted list's three verbs. Dropped: `[R-SLB-04]`
  expressly names "the slab declaration itself" among what a commit may change, and 20.3's
  tail states the alignment case ("an aligned layer's stored tiles ... satisfy its
  invariant or the declaration is cleared"), so "re-established" reaches the value.
- "nothing else this step permits moves one" (step 4). Dropped: I checked each permitted
  change. A shortening removes the last channel's N ordinals and leaves c*N+s unchanged
  for c < C-1; an append adds after every existing ordinal; names, slab and alignment
  move nothing. The claim holds.
- "an appended planar channel adds tiles at ordinals ... with N the spatial-tile count"
  read against a simultaneous growth. Dropped: `[R-GEO-06]` defines N over the layer, and
  step 4's parenthetical fixes the tense ("a growth renumbers ordinals wherever
  `[R-GEO-06]` moves them"), so N is the new state's.
- Hunk 3's "and so does" as a stranded parallel. Dropped: the relative clause that follows
  it supplies the different mechanism in the same breath.
- F3's siblings (hunk 14). Dropped: a layer record's or sub-record's offset+length is
  caught by L17, a tile-index entry's by T12, and T12's wording is now identical to F3's.
- L14's siblings (hunk 15). Dropped: F29 already carries "or bytes remain after the last
  complete record" for the directory's record sequence, so the residue case is covered at
  both scopes after the repair.
- Nested em-dash pairs in repaired text. Dropped: I read each hunk's inserted prose. h02,
  h05, h07 and h19 each carry one dash pair with no dash pair inside it; h19's inner
  material is parenthesised, not dashed; h13 uses a single terminal dash. The
  three-dash constructions I did find (Appendix H's verifier bullet, 21.6's slack row)
  are outside every hunk I was given.
- Hunk 18's acceptance clause as an overclaim. Dropped: 21.6 names exactly two structural
  cases and the clause covers both, with `[R-MTA-09]` excluded by the guarantees clause.
- Hunk 7's "MAY use a wider representation". Dropped: the sentence pins the
  interpretation to the binary64 value and permits a wider container for it; the
  readability test is separately pinned to "binary64 interpretation". Pre-existing and
  not worsened.
