# Audit transcript — hunk-03.diff, "the principle" paragraph

## Scope discipline

Charter: audit `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-03.diff`,
landing at spec/tarn.md lines 3167-3246 (as marked in the hunk header), nearest
preceding heading "20.3 The append procedure" (line 3113). My specific charge
within this hunk: the paragraph beginning "The line is drawn where a stored
tile's meaning is fixed" (the "principle" paragraph) and the sentence
following it that states what the line gives up. Another lane audits the
closed list two paragraphs above (the "keeps its declarations, with these
exceptions and no other... Every other declaration is fixed..." paragraph) —
I treat that list as reference material, not as my own subject, per the
charter's explicit split.

## Files read

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/hunk-03.diff` — the hunk, read in full via Bash `cat`.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — read via `sed -n` line ranges and `grep -n`, and via two short local Python scripts for normalized (whitespace-collapsed) phrase counts. No other file was opened. No docs/, no ADRs, no git history, no registry.json, no full.diff, no other hunk file.

## Step 0 — header-vs-body check

Hunk header says: "nearest preceding heading in the current file: line 3113,
'20.3 The append procedure'". I read spec/tarn.md lines 3100-3260 and
confirmed: line 3113 is exactly `#### 20.3 The append procedure`, and the
hunk's context lines ("An appender MUST, in order:", steps 1-4, the
`[R-WRT-04]`-tagged step 6 material after it) match the current file
verbatim outside the changed region. Header and body agree — no discrepancy
to report.

## Step 1 — read the whole passage the repair landed in

Read spec/tarn.md 3100-3260 (the full numbered step 4, both the paragraph the
hunk left alone at its top and the three new paragraphs), plus the un-hunked
steps 5 and 6 and the Note that follows, to check forward anaphora (check 8).

Quoted for reference, the two paragraphs that are my primary subject:

> "A layer that stores a tile **in the generation this commit supersedes**
> keeps its declarations, with these exceptions and no other: its name, and
> its dimension and channel names, MAY change; an extent MAY grow; a planar
> layer's channel list MAY be extended at its end, or shortened from its end;
> and a slab or alignment declaration is re-established or cleared as this
> step provides below. Every other declaration is fixed for as long as the
> layer stores a tile: the layout, the linearization and the index encoding,
> the codec and the filter, the rank and the dimension order, every tile
> extent, every channel's type and fill, an interleaved layer's channel list,
> and the position of every planar channel but the last. A commit MUST NOT
> change one of these; the change is a new layer, or a whole-file rewrite
> under a fresh file_id (`[R-LIF-01]`, §20.5). The two lists partition
> §7.4's fields, the derived ones aside — entry_count, crc_of_crc_array and
> the extent slot follow the commit. ..." [reference list — audited by the
> other lane, used here only as ground truth]

> "The line is drawn where a stored tile's meaning is fixed. The fixed
> declarations are the ones §14 reads a stored tile under — its value
> sequence, its byte layout, the fill its padding positions hold (§14.5) —
> and the ones §11.4 assigns its ordinal and its values' coordinates by;
> under new ones the same bytes would denote values, coordinates or padding
> the writer did not store, with every checksum in §8 certifying the result
> and no check any actor owes able to see it (§21.7). The permitted changes
> touch none of that: a name enters no map; a grown extent adds positions
> that held their channel's fill (§14.5), and fill is a legal sample value;
> an appended planar channel adds tiles at ordinals after every existing
> one, a disk ordinal being c · N + s with N the spatial-tile count; a
> channel removed from the end takes only its own tiles out of the
> addressed set, and a tile the new state does not address carries no
> obligation. What the line gives up is stated rather than carved around: a
> shrink, a fill change, a re-type, a re-tiling, a change of layout, codec
> or filter, and a channel inserted or removed anywhere but the end are
> rewrites even where a particular file would survive them in place, because
> deciding which files would is the edge this list exists to remove." — MY
> SUBJECT.

## Step 2 — rule the repair adopts, in my own words

The principle paragraph asserts a justificatory *test* for the closed list
above it: a declaration belongs on the "fixed" side exactly when it is one
that §14 reads a stored tile's bytes under, or one that §11.4 uses to assign
that tile's disk ordinal and its values' coordinates. It then argues each of
the four exceptions (name, extent growth, planar-channel append, planar
last-channel removal) is safe because none of them disturbs what that test
protects. It closes with a sentence presented as the *complete, non-carved*
enumeration of what is now forbidden (in explicit contrast to the pre-repair
text's bar-with-carve-outs style): shrink, fill change, re-type, re-tiling,
layout/codec/filter change, and channel insert/remove anywhere but the end.

## Step 3 — Check 2 (citations) and Check 4 (fixed-list membership) — the central charter task

I opened every section the principle cites and checked it against the
literal claim "The fixed declarations are the ones §14 reads a stored tile
under ... and the ones §11.4 assigns its ordinal and its values' coordinates
by," walking the charter's own enumeration of the fixed list: layout,
linearization, index encoding, codec, filter, rank, dimension order, tile
extents, channel type, channel fill, an interleaved channel list, a planar
channel's position.

Read spec/tarn.md 1950-2151 (§14 in full: 14.1 value sequence, 14.2 byte
layout/decoded size, 14.3 packed boolean planes, 14.4 layout-type validity,
14.5 padding content) and 1700-1730 (§11.4 linearization, the ordinal and
coordinate formulas, `[R-GEO-05]`, `[R-GEO-06]`).

| Fixed-list item | Enters §14 (a stored tile's read)? | Enters §11.4 (ordinal/coordinate)? | Verdict |
|---|---|---|---|
| layout | Yes — §14.1: "The layer's layout field (§7.4) selects the mode" (planar/interleaved), governs the whole value-sequence definition | — | covered |
| linearization | — | Yes — §11.4 opening sentence: "selecting the rule that orders tiles within the grid and entries within the tile index" | covered |
| **index encoding** | **No** — §14 never mentions it | **No** — §11.4 never mentions it | **NOT covered — see B-02** |
| codec | Yes — §14's own opening sentence defines the decoded tile image as "the byte sequence a stored tile's payload decodes to under §17's codec pipeline" | — | covered (via §14's own cross-reference) |
| filter | Yes, same clause as codec | — | covered |
| rank (d) | indirectly (P, V depend on geometry) | Yes — §11.4's formulas are stated "with grid counts (G₀,…,G_{d−1}) and tile extents (T₀,…,T_{d−1})," i.e. indexed over rank | covered |
| dimension order | — | Yes — §11.4: "...all in declared dimension order" is explicitly load-bearing in both formulas | covered |
| tile extents (Tᵢ) | — | Yes — §11.4: tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ | covered |
| channel type | Yes — §14.2/14.3 decode arithmetic is keyed on element size/type; §12.3 ties bit pattern to type | — | covered |
| channel fill | Yes — §14.5 explicitly: "at every padding position, a writer MUST encode, for each channel the position carries, that channel's fill value" | — | covered |
| interleaved channel list | Yes — §14.2: Fᶜ = Σ Bⱼ over channels j<c, "in declared channel order" | — | covered |
| planar channel's position (all but last) | — | Yes — §11.4/`[R-GEO-06]`: disk ordinal = c·N+s, c = "the channel's index" | covered |

I verified index_encoding's actual role directly:

```
grep -n 'index_encoding' spec/tarn.md
```
gave 5 hits (1103, 1111, 1121, 1171, 2158) plus three register rows (3709,
3710, 3718). Read 2151-2230 (§15.1-15.3): index_encoding selects the
physical layout of the tile-index *region* — the 20-byte
offset/length/crc entry array and its segment-CRC array (§15.1) — and
feeds `[R-CNT-17]`'s extent_length formula (entry_count × 20 +
⌈entry_count/2¹⁶⌉×4). It has no role anywhere in §14 (how a stored tile's
payload decodes) or §11.4 (how a tile's ordinal or a value's coordinate is
computed). This is confirmed by the register rows too: L22/L31 key
index_encoding's obligations to `[R-CNT-17]`/`[R-CNT-23]`/§15.1, never to
§14 or §11.4.

**B-02.** The principle's own defining sentence — "The fixed declarations
are the ones §14 reads a stored tile under ... and the ones §11.4 assigns
its ordinal and its values' coordinates by" — does not reach index_encoding,
a member of the fixed list two paragraphs above it that it purports to
explain. Per the charter's own framing: "If one enters neither, the list has
a member the principle does not reach, and that is the finding."

## Step 4 — the §21.7 claim

Charter directs: "Test it: a re-type to a wider element size changes the
decoded size, which §21.4 witnesses (T3, T14)."

Read spec/tarn.md 3866-3920 (§21.7 in full) and 3738-3752 (§21.4's opening
and rows T1-T5), and located T3/T14 precisely:

```
grep -n '| T3 |\|| T14 |\|| T2 |' spec/tarn.md
3749:| T2 | ... | verifier | certification | `[R-SER-08]` |
3750:| T3 | The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations | ... | reader | tile use | `[R-SER-07]` (R-COD-08) |
3761:| T14 | Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size | ... | reader | tile use | `[R-COD-04]` |
```

T3's Detector column reads **reader**, not *verifier* — per §21.4's own
governing clause ("where a row's Detector is *verifier* no reader is
obliged to detect the condition" — the converse holds for T3: every
conforming reader is obliged to detect it). §21.7 defines "unwitnessed"
precisely: "for every file exhibiting it, some file that does not exhibit
it cannot be told apart from it by any check this specification obliges a
reader or a verifier to perform" — and immediately: "That is the whole of
the test" (the exact governing-clause-above-the-sentence pattern the byte-
level-test instructions warned to read first). A condition a *reader*
check (T3) separates from every non-exhibiting file is, by this definition,
**detectable**, not unwitnessed.

Concretely: re-type a channel from int8 (element size 1) to int32 (element
size 4) on a layer that stores a tile carrying it. Nothing about the stored
bytes changes (this is an append; the old payload is untouched, `[R-LIF-01]`).
§14.2's decoded-size table gives decoded size = P·Bᶜ; Bᶜ jumps from 1 to 4,
so the tile's declared decoded size is now 4× what its actual (unchanged)
payload decodes to under the (unchanged) codec/filter. T3 fires for every
reader, unconditionally — this is exactly what the principle's sentence
claims cannot happen ("no check any actor owes able to see it").

The now-deleted prior text (visible in the "-" lines of the hunk) had this
exactly qualified: "wrong content, which §21.7 leaves unwitnessed **where
the element size is unchanged and the new type is numeric**, and which the
register witnesses otherwise (T3 and T14 for a changed decoded size, T2 for
a boolean byte)." I checked the narrow case is genuinely unwitnessed: an
int8↔uint8 re-type (same element size 1, both "numeric" types) leaves
decoded size unchanged (T3/T14 silent), and by `[R-TYP-04]`/`[R-TYP-05]`
(read at 1795-1810) *every* bit pattern is a valid value of *either* type,
so no register row or reader obligation can distinguish "written as int8,
read as uint8" from "always declared uint8." That sub-case is genuinely
unwitnessed. But the principle's rewritten sentence drops the qualification
entirely and states the "no check ... able to see it" consequence as
following from *any* fixed-declaration change ("under new ones the same
bytes would denote values, coordinates or padding the writer did not
store, with every checksum in §8 certifying the result and no check any
actor owes able to see it (§21.7)") — an unqualified "under new ones,"
ranging over the whole fixed list: layout, tile extent (re-tiling), rank,
dimension order, all of which plausibly perturb decoded size or entry_count
and would be caught the same way T3/T14 catch a widening re-type.

**B-01.** The §21.7 claim, as reworded, overclaims: it is true only of the
narrow same-element-size numeric-to-numeric re-type sub-case (and perhaps a
handful of similarly size-preserving changes), and false of the general
class of fixed-declaration changes the sentence is written to cover —
directly falsifiable by a wider re-type, which is a *reader*-detectable
violation (T3, `[R-SER-07]`) per §21.4's own Detector column, not something
"no check any actor owes able to see."

## Step 5 — Check 7: the four permitted-change arguments, against each admitted layer shape

Charter: check each argument against (a) a planar layer with pad bits
(packed bool plane), (b) an interleaved layer, (c) a layer with a slab
declaration (§16), (d) a layer whose extent grows into a new padding
position.

**"a name enters no map."** Grepped §7.4 (1083-1180) and §4.6-adjacent name
rules; names are pure identifiers (`[R-ENC-15]` uniqueness aside), entering
neither the §14 decode arithmetic nor the §11.4 ordinal/coordinate formulas
for any layout. Holds uniformly across (a)-(d). No defect.

**"a grown extent adds positions that held their channel's fill (§14.5),
and fill is a legal sample value."** Read §11.1-11.3 (1618-1699) and §14.3
(2051-2089) plus its Note ("Pad bits are not padding positions (§11.3)... a
padding position is a whole sample position outside the layer's extents").
For case (a), a packed bool plane: a padding position within an edge tile
is one of the P bit-packed positions (P fixed by tile extents alone, per
§11.2, unaffected by extent growth), and §14.5 already mandates it hold the
fill bit; growth reclassifying it from padding to real changes nothing
about the stored byte. Confirmed this holds distinctly from *pad bits*
(the packed plane's unused high bits, arising only when P mod 8 ≠ 0, an
unrelated concept per §14.3's own Note) — the argument does not conflate
the two. For (b) interleaved, same reasoning via §14.2's per-value byte
layout. For (c) slab-declared layers, growth that changes the stored-tile
set triggers `[R-SLB-04]` ("changes the stored-tile set ... MUST either
re-establish the invariants ... or clear the declaration") — read §16.2
(2306-2345) — and this is exactly the case the closing paragraph of my hunk
covers ("a slab declaration is re-established or cleared (`[R-SLB-04]`)"),
so no gap. For (d), by definition, this is the case the argument targets;
confirmed correct as above. **However**, see B-03 below — the argument
addresses content/fill safety but not the ordinal-reassignment half of the
principle's own stated criterion.

**"an appended planar channel adds tiles at ordinals after every existing
one, a disk ordinal being c · N + s with N the spatial-tile count."**
Verified via `[R-GEO-06]` (1700-1725): disk ordinal = c·N+s for a planar
layer. Appending channel index C (the new highest index, C ≥ 1 always per
`[R-GEO-01]`'s "at least one channel") adds tiles at ordinals [C·N,
(C+1)·N), strictly after every existing channel's block [0, C·N). Holds
for slab-declared layers too: §16.2's runs "partition each contiguous block
of disk ordinals independently: for ... a planar layer each channel block
[c·N, (c+1)·N) — runs never span channel blocks" — so the new channel's
block is an independent run, no interaction with existing runs' contiguity.
Does not apply to interleaved layers (channel lists there are entirely
fixed, per the other lane's list — consistent, no gap).

**"a channel removed from the end takes only its own tiles out of the
addressed set, and a tile the new state does not address carries no
obligation."** Only applies to planar layers (interleaved channel lists are
wholly fixed). Removing the last channel (index C−1) removes exactly its
block [((C−1)·N, C·N) — the highest-ordinal block — leaving [0,(C−1)·N)
untouched, matching the surrounding step 4 text's "nothing else this step
permits moves one [ordinal]." For (c), slab-declared layers: same
`[R-SLB-04]` re-establish-or-clear obligation as growth, already covered by
the closing paragraph of the hunk. No defect found in any of the four
arguments' scope across layer shapes.

## Step 6 — Check 4/1: does "ordinal" in the principle's own criterion undermine the growth exception?

The principle states one unified criterion: "the ones §11.4 assigns its
ordinal **and** its values' coordinates by." I checked both halves
separately against §11.4 (1700-1725):

- Coordinate: for a value at in-tile position u in tile with grid
  coordinates t, its coordinate is xᵢ = tᵢ·Tᵢ+uᵢ — a function of Tᵢ (tile
  extent, fixed) and the tile's own grid-position identity t, **not** of
  the grid count Gᵢ (hence not of the declared extent Eᵢ). Growth does not
  change any existing tile's t, so no existing tile's coordinate moves.
- Ordinal: s = Σᵢ tᵢ·∏_{j>i}Gⱼ (spatial ordinal, then c·N+s for planar).
  Gⱼ = ⌈Eⱼ/Tⱼ⌉ (§11.2, 1657-1670) is derived from the declared extent Eⱼ.
  Growing Eⱼ for any dimension other than the last changes ∏_{j>i}Gⱼ for
  every i<j, which **does** renumber many existing tiles' ordinals — a
  fact the (retained, un-hunked) paragraph above already states
  explicitly: "a growth renumbers ordinals wherever `[R-GEO-06]` moves
  them."

So extent literally is "one of the ones §11.4 assigns ... ordinal ... by,"
under a plain reading of the principle's own criterion, yet it is the
paradigm licensed exception. The paragraph's defense — "a grown extent adds
positions that held their channel's fill... and fill is a legal sample
value" — answers only the *content* question (do bytes still denote the
values they meant), not the *ordinal* question the paragraph's own stated
test also poses. The resolution (implicit, not stated in this paragraph)
is presumably that "assigns ... ordinal ... by" should be read as "the
declarations that fix the *rule/formula*" (dimension order, tile extents,
linearization — all of which stay fixed under growth) rather than "the
declarations whose *value* the formula's output depends on" (which would
include extent) — but the paragraph does not draw this distinction, and a
plain reading of its own words captures extent on the "fixed" side while
paragraph 2 treats it as the primary exception.

**B-03.** The principle's stated ordinal criterion, read literally, would
also capture "extent" (since Gⱼ, an input to `[R-GEO-06]`'s ordinal
formula, derives from the declared extent) — in tension with treating
extent-growth as an exception the criterion doesn't reach ("touch none of
that"). The paragraph's own defense of the growth exception addresses only
the content/fill half of its stated test, not the ordinal half. This is a
genuine ambiguity in the principle's self-justification, though not one
that changes any actual conformance outcome (paragraph 2's closed list
independently and unambiguously permits growth regardless of how this
paragraph justifies it) — marked PLAUSIBLE, not CONFIRMED, and NOT
byte-level.

## Step 7 — the give-up sentence against the fixed list

Charter: "Hold that list to the fixed list: is every fixed declaration's
change named, and is anything named that the fixed list does not fix?"

I ran a normalized (whitespace-collapsed) word count restricted to exactly
the text of numbered step 4 (lines 3167-3246), via a short Python script
(see Sweeps below), to avoid the hard-wrap miss the charter warns about,
and to get an exact, defensible count rather than an eyeballed one:

```
rank -> 1
linearization -> 1
index_encoding -> 0
index encoding -> 1
dimension order -> 1
transpos -> 0
codec -> 2
filter -> 2
shrink -> 1
```

Each of "rank," "linearization," "index encoding," and "dimension order"
occurs **exactly once** in the whole passage — in the fixed-list sentence
of paragraph 2, never repeated in the give-up sentence of paragraph 3. I
confirmed by printing the give-up sentence verbatim (see Sweeps) that it
reads: "a shrink, a fill change, a re-type, a re-tiling, a change of
layout, codec or filter, and a channel inserted or removed anywhere but the
end are rewrites..." — layout ✓, codec ✓, filter ✓, tile-extent (via
"re-tiling") ✓, channel type (via "re-type") ✓, channel fill (via "fill
change") ✓, channel-list position (via the insert/remove clause) ✓ — but
**linearization, index encoding, rank, and dimension order (transposition)
are absent**, confirmed by "transpos" occurring zero times anywhere in the
passage: no synonym for a dimension-order change appears in the give-up
sentence at all.

**B-04.** The give-up sentence is introduced as complete ("is stated rather
than carved around" — explicitly contrasted with the pre-repair text's
carve-out style, i.e. presented as *the* enumeration, not an illustrative
sample) but omits four of the twelve fixed declarations paragraph 2 lists:
linearization, index_encoding, rank, and dimension order. A reader who
takes "stated rather than carved around" at face value could conclude a
linearization, index_encoding, rank, or dimension-order (transposition)
change on a layer storing a tile is *not* a rewrite, directly contradicting
paragraph 2's unqualified "A commit MUST NOT change one of these" for those
same four items, three sentences earlier in the same numbered step. This
also matches the deleted old text's own more careful phrasing, which
explicitly paired two operations here ("re-tiled **or transposed**") where
the new text names only one ("a re-tiling").

Also checked and rejected as a matching defect: the "permitted changes"
sentence just before it ("a name enters no map; a grown extent...; an
appended planar channel...; a channel removed from the end...") does *not*
mention the slab/alignment exception from paragraph 2. I considered this a
candidate parallel gap and rejected it: slab and alignment declarations
govern physical byte placement (§16), not tile content, coordinate, or
ordinal assignment in the §14/§11.4 sense — they never risked falling under
"the fixed declarations" to begin with, so there is nothing for this
sentence to argue past for them, unlike shrink/re-type/etc., which are
genuinely fixed-list members the give-up sentence is supposed to be
covering.

## Step 8 — Check 3 (label, not marker)

Confirmed via the sed reads above that all of paragraph 2, 3, and 4 sit as
plain paragraph text inside numbered step 4, with no leading `>` and no
**Note.**/**Example.**/**Rationale.** label anywhere in the hunk's added
text. Per `[R-CNF-01]` this is normative text (the whole document is
normative except §1, labeled blocks, and non-normative appendices) — the
repair lands in force. I also re-confirm (Step 3 above) it is *not* inside
a blockquote at all, so the "check the label not the marker" instruction is
moot here in the safer direction: there's no ">" to misjudge.

## Step 9 — Check 8 (anaphora), forward and backward

Read forward from the end of paragraph 4 into step 5, step 6, and the Note
following step 6 (spec/tarn.md through ~3260). No back-reference in that
retained text ("the layer," "it," "them") changed antecedent because of the
insertion — step 5's "the directory" and step 6's "the same file_id" refer
to structures introduced earlier in `[R-LIF-02]`/§9.2, untouched by this
hunk, and don't reach back into my paragraphs at all.

Checked whether any *other* passage in the document still uses the deleted
old-text's proprietary vocabulary ("the §14 bar," "that bar," "the bar
below," "the bar beside the §14 bar") which would signal an unswept
back-reference now resolving to nothing:

```
grep -n '§14 bar\|the bar\b\|bar above\|that bar' spec/tarn.md
2643:content-checksum flag; and the bar on sizing any buffer from a
2649:the bar on sizing a buffer binds a reader rather than the document,
3049:   and all further service from the layer; the bar is prospective,
```
All three hits are unrelated uses of the word "bar" (buffer-sizing limits,
a prospective service bar) in completely different sections — none is a
stranded reference to the deleted §14-bar terminology. Confirmed with a
normalized-whitespace Python search for the literal phrase "§14 bar" and
"the §14 bar" across the whole document: **0 hits each** (see Sweeps),
with a control search in the same script confirming phrases I know are
present ("carved around," "stated rather than carved," "no check any actor
owes able to see it") each return exactly 1 — proving the search
methodology isn't silently failing.

Checked whether any restatement elsewhere in the document still describes
the *pre-repair* rule (bar-with-carve-outs, or shrink-permitted). Found two
candidate restatements and read both in full:

- spec/tarn.md 1630-1655 (§11.1's Rationale block): "§20.3 states
  normatively, and governs, what a commit may do to a layer that already
  stored tiles ...: its extents may grow ...; a planar layer's channel list
  may be extended or shortened at its end; its names, and its slab and
  alignment declarations, may change; and every other declaration is fixed
  while the layer stores a tile, a change to one being a new layer or a
  whole-file rewrite." — matches the *new* rule, already correctly swept;
  and it is explicitly hedged ("§20.3 states normatively, and governs") so
  it does not compete with §20.3 for authority. Not a defect.
- spec/tarn.md 4685-4694 (§20 lifecycle-obligations summary, "Conforming
  updater"): "changes a layer that stores a tile only as §20.3 step 4
  permits — its names, a grown extent, a planar channel at the end, a slab
  or alignment declaration — and makes any other change to it as a new
  layer or a whole-file rewrite (§20.3)" — also matches the new rule,
  already correctly swept. Not a defect.
- spec/tarn.md 4146-4160 (§23.1, privacy/deletion-is-not-erasure): "no
  commit turns a real position of a stored tile into padding, a shrink
  being a rewrite (§20.3 step 4)" — explicitly states shrink = rewrite,
  consistent with the *new* rule (shrink is no longer permitted in place at
  all). This is the one place outside the hunk that states the shrink
  policy, and it already agrees with the rewrite. Not a defect.

`grep -n 'shrink' spec/tarn.md` returns exactly these two hits (3217, in my
hunk, and 4157) — confirming there is no third, stale restatement of the
old (shrink-permitted) rule lurking anywhere else in the document.

## Step 10 — NESTED_DASH

Scanned paragraphs 2-4 (the hunk's added text) for em-dash pairs. Found two
paired constructions: "— its value sequence, its byte layout, the fill its
padding positions hold (§14.5) —" (paragraph 3) and "— every one the new
state keeps, not only those this commit adds —" (paragraph 4). Neither
contains a second, nested em-dash pair inside it; both are single,
non-nested asides. No NESTED_DASH finding.

## Step 11 — Check 5 (other exhaustive-claim words)

Flagged and checked every completeness word in my two paragraphs: "the
ones" (×2, defining the fixed-declaration set — see B-02), "every" (×5:
"every value... denoting," "every value they carry," "every checksum in §8"
[true — checksums are byte-CRCs, unaffected by declaration reinterpretation
— verified against §8.1's coverage-map table, read at 1215-1230], "every
existing one" [verified true for planar-append, Step 5], "every rule that
geometry is subject to" [an open-ended, self-admittedly non-exhaustive
list, paragraph 4: "the list is not offered as exhaustive" — not a
completeness claim at all, explicitly hedged]), "no check any actor owes
able to see it" (see B-01), "stated rather than carved around" (see B-04),
"only its own tiles" (verified true, Step 5), "none of that" (verified
against the two-part criterion, see B-03 for where this breaks down on the
ordinal half).

## Rejected candidates

1. Considered whether "a name enters no map" might be false for the
   *layer's own name*, since `[R-ENC-15]` requires uniqueness — could a
   rename collide with another layer's existing name and thus "enter" a
   uniqueness check? Checked `[R-CNT-23]`'s violation list (1108-1113):
   duplicate layer name is explicitly *file scope*, a separate condition
   from anything §14/§11.4 governs, and uniqueness is a constraint on the
   *new* name regardless of whether this is a rename or a fresh
   declaration — it doesn't make the *old* declaration's meaning move for
   any stored tile. Not a defect; "enters no map" is about the §14/§11.4
   decode/ordinal maps specifically, and holds.
2. Considered flagging the "permitted changes" sentence's omission of the
   slab/alignment exception as a mirror-image gap to B-04. Rejected after
   checking §16 (2276-2360): slab/alignment are physical-placement
   declarations, never inputs to §14 or §11.4, so they were never at risk
   of falling under the stated fixed-declarations criterion and need no
   defense here — unlike the give-up sentence's omissions, which *are*
   fixed-list members.
3. Considered whether "an appended planar channel adds tiles at ordinals
   after every existing one" might be false when a layer has a slab
   declaration whose *last run* of the final existing channel block is
   partially filled (S doesn't divide N) — would the new channel's tiles
   need to interleave into that partial run? Checked `[R-SLB-02]`
   (2306-2312): "runs never span channel blocks, and the final run of a
   block can cover fewer than S ordinals" — each channel block is a
   self-contained partition; a new channel's block starts its own fresh
   run sequence at block_start = C·N, entirely independent of the previous
   channel's last (possibly short) run. No interleaving; claim holds.
4. Considered whether "fill is a legal sample value" might fail for bool
   channels specifically (constrained fill, `[R-TYP-07]`, 1888-1896: fill
   MUST be 0x00 or 0x01) — checked and confirmed those are exactly the two
   legal bool *sample* encodings too (§14.2 states 0x00/0x01 are the only
   legal interleaved bool byte values), so "fill is a legal sample value"
   holds for bool as well as for the twelve numeric types (`[R-TYP-05]`,
   every bit pattern legal). Not a defect.

## Sweeps run (verbatim commands and results)

```
grep -n '^#### 14\|^#### 11\.4\|^### 14\|^## 14\b\|^#### 13\b\|^### 13\b\|^## 13\b\|^#### 15\b\|^### 15\b\|^#### 15\.2\|^#### 21\.7\|^### 21\.7' spec/tarn.md
  -> 12 hits (section headers located, listed in transcript body above)

grep -n '^#### 7\.4\|^### 7\b' spec/tarn.md
  -> 2 hits: 946 (### 7.), 1083 (#### 7.4)

grep -n 'shrink' spec/tarn.md
  -> 2 hits: 3217 (inside my hunk), 4157 (§23.1, verified consistent)

grep -n 'index_encoding' spec/tarn.md
  -> 5 hits: 1103, 1111, 1121, 1171, 2158 (all §7.4/§15, none in §14/§11.4)

grep -n '^### 16\|^#### 16\.' spec/tarn.md
  -> 3 hits: 2276, 2289, 2306

grep -n '§14 bar\|the bar\b\|bar above\|that bar' spec/tarn.md
  -> 3 hits: 2643, 2649, 3049 — all unrelated ("bar" on buffer sizing,
     "bar" as in barred-from-service), none are stranded references to
     the deleted §14-bar terminology.

grep -n 'carve-out\|§20\.3' spec/tarn.md
  -> 12 hits located; two read in full (1946-1947 sparse-writing Note,
     4680-4694 conforming-updater summary) and confirmed already swept to
     the new rule.

grep -n '^#### 21\.' spec/tarn.md
  -> 9 hits: 3541, 3627, 3681, 3738, 3775, 3809, 3866, 3923, 3930

grep -n '| T3 |\|| T14 |\|| T2 |' spec/tarn.md
  -> 3 hits: 3749 (T2), 3750 (T3), 3761 (T14) — all in §21.4 (confirmed by
     the header grep above, §21.4 at 3738), Detector column read for each.

Python normalized-whitespace control script (over the whole document):
  "§14 bar" -> 0
  "the §14 bar" -> 0
  "carved around" -> 1
  "stated rather than carved" -> 1
  "no check any actor owes able to see it" -> 1
  (control: nonzero counts for phrases known present prove the
  whitespace-normalization methodology is not silently broken, before
  trusting the "§14 bar" -> 0 result.)

Python normalized-whitespace word count, restricted to spec/tarn.md lines
3167-3246 (the whole of numbered step 4, i.e. my hunk's landing zone):
  rank -> 1; linearization -> 1; index_encoding -> 0; index encoding -> 1;
  dimension order -> 1; transpos -> 0; codec -> 2; filter -> 2; shrink -> 1;
  extent MAY grow -> 1; ordinal -> 5; slack -> 3;
  fixed declarations are the ones -> 1
  (each of rank/linearization/index encoding/dimension order occurs
  exactly once, confirmed to be in the fixed-list sentence and never
  repeated in the give-up sentence — the basis for B-04. "transpos" at 0
  confirms no synonym for dimension-order change appears anywhere in the
  give-up sentence.)
```

## Derived numbers

- Fixed-list membership table (Step 3): 12 items checked against 2 target
  sections (§14, §11.4); 11/12 enter at least one, 1/12 (index_encoding)
  enters neither. This 11-of-12 vs 1-of-12 split is the basis for B-02,
  computed by direct textual cross-reference, not estimation.
- Give-up-sentence coverage (Step 7): of the same 12 fixed-list items, 8
  are named (directly or via a clear synonym: layout, codec, filter,
  tile-extent/"re-tiling", channel-type/"re-type", channel-fill/"fill
  change", channel-list-position/"inserted or removed anywhere but the
  end", and — arguably — the interleaved list via the same clause) and 4
  are not named at all (linearization, index_encoding, rank, dimension
  order). This 8-vs-4 split, and the "occurs exactly once, in the other
  sentence" figure for each of the 4, is computed directly from the Python
  word-count script above, not eyeballed.
- §21.7 claim (Step 4): checked against exactly 1 concrete falsifying case
  (int8→int32 re-type on a stored tile) worked through §14.2's decoded-size
  formula (P·Bᶜ, Bᶜ: 1→4) and cross-checked against T3's Detector column
  (reader, not verifier) in §21.4.

## Confidence / what an empty result would have needed

Findings were not empty, so this is by way of showing the checks that
*did* pass and did not simply go unlooked: Check 3 (label) passed cleanly
— no ambiguity, the passage isn't even in a blockquote, verified by reading
the raw sed output for leading `>`. Check 8 backward/forward passed for
every anaphor I could identify in the retained text on both sides of the
insertion (Step 9) — I did not find a stranded pronoun. Check 7's four
arguments passed for the (a)-(d) layer-shape matrix except for the
ordinal/growth subtlety written up as B-03. NESTED_DASH passed (Step 10).
The "permitted changes" sentence's slab/alignment omission was considered
and explicitly rejected with reasoning (Rejected candidate 2), not merely
overlooked.

## Summary

I audited the "principle" paragraph of hunk-03 (spec/tarn.md's step-4
append-procedure rewrite) — "The line is drawn where a stored tile's
meaning is fixed" through "...the edge this list exists to remove" — against
the eight checks, with the charter's four specific directed checks (Check 7
per-argument, Check 4 fixed-list-vs-principle membership, the give-up
sentence, the §21.7 claim) given the most weight.

Two high-confidence (CONFIRMED) findings: (B-02) the principle's own
defining test — fixed declarations are exactly those §14 reads a tile
under or §11.4 assigns ordinal/coordinates by — does not reach
index_encoding, a member of the fixed list two paragraphs above, which is
purely a §15 (tile-index region format) concept; and (B-01) the §21.7
claim, reworded from the deleted text's carefully qualified version (true
only for same-size numeric re-types) into an unqualified claim covering
every fixed-declaration change, is false for the general case — a re-type
to a different element size is reader-detectable (T3, §21.4, `[R-SER-07]`),
not unwitnessed. Neither is byte-level: paragraph 2's plain "MUST NOT
change one of these" already, unambiguously, bars every fixed-declaration
change regardless of how this explanatory paragraph justifies or narrates
the bar, so no conforming implementation's actual emit/accept/reject
behavior turns on either defect.

One further CONFIRMED finding (B-04): the give-up sentence, introduced as
the complete, non-carved-around statement of what's forbidden, in fact
names only 8 of the 12 fixed declarations — linearization, index_encoding,
rank, and dimension order (transposition) are absent, confirmed absent by
exact word-count search, and confirmed as a real omission (not just a
category the sentence never needed to address) by cross-checking against
paragraph 2's unambiguous "MUST NOT change one of these," which does bar
all four. Also not byte-level, for the same reason as B-01/B-02.

One PLAUSIBLE, subtler finding (B-03): the principle's own stated ordinal
criterion, read literally, would also capture "extent" (since the grid
count feeding `[R-GEO-06]`'s ordinal formula derives from the declared
extent), creating tension with treating extent-growth as an untouched
exception; the paragraph's actual defense of growth addresses only the
content/fill half of its own two-part test, leaving the ordinal half
unaddressed in this paragraph (though the wider document, via the retained
"a growth renumbers ordinals" clause one paragraph up, treats ordinal
movement as harmless bookkeeping rather than a fixed-declaration violation
— this paragraph just never says so).

Checks 1, 2 (beyond B-01/B-02), 3, 6, 8, and NESTED_DASH were run and
returned clean for this paragraph specifically; see the corresponding
numbered steps above for the searches and reasoning behind each clean
result, and the Rejected-candidates section for suspicions opened and
closed.
