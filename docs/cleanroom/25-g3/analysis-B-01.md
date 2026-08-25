# Refute-only audit of the B-01 downgrade

## What I read / ran

- case/case-B-01.md, hunk-01.diff, hunk-02.diff (permitted).
- spec/tarn.md: sed ranges 100-110, 170-200, 1025-1050, 2900-2930, 2940-3110, 4400-4460.
- Whitespace-flattened whole spec into scratchpad/flat.txt (tr '\n' ' ' | tr -s ' ')
  and ran grep -o -E ".{N}<frag>.{M}" for: relocat, shrink, "record alone",
  "surviving stored", R-WRT-05, R-WRT-07, R-CNT-21, R-CNF-05, R-GEO-06.
- grep -n for "relocating a live index", "never relocates a live",
  "record alone changes keeps", "obliges the smaller entry_count",
  "An appender MUST, in order".
- awk 'NR>=2949 && NR<=3072 && /^[[:space:]]*>/' over tarn.md -> EMPTY OUTPUT.
  Confirms all of section 20.3 step 4, both disputed clauses included, is outside
  any blockquote and therefore normative.
- Nothing else. Did not read full.diff, other hunks, docs/, conformance/,
  registry.json, git.

Contamination: my runtime pre-loaded a project instruction file and an index of
the maintainer's memory notes before I began. I disregarded them; nothing below
derives from them.

## The finding at its strongest

Padding-only shrink: E=1000, T=256, G=4. Shrink E to 999. G stays 4, N stays 4,
coordinate 999 becomes a padding position whose stored byte already holds fill.

- L2993-2996: "A layer whose record alone changes keeps its extent slot, pointing
  at the existing region, as does a layer the commit leaves untouched
  ([R-WRT-05]); relocating a live index region is compaction's operation
  (20.5, [R-WRT-07]), not an appender's."
- L3056-3059: "Where a shrink is permitted the de-addressed tiles' extents become
  slack ([R-CNT-21]), [R-CNT-17] obliges the smaller entry_count and so a
  re-emitted index region, and every surviving stored tile is untouched."

Writer A: directory-only. Writer B: re-emits the index region at a new placement
at the unchanged entry_count, re-points the extent slot, strands the old region.
B's file is conforming, so the [R-CNF-05] escape hatch is unavailable and the
case reduces to: is Writer B barred?

## Constructions built to break the downgrade

1. Other actors. 20.1 defines creator/appender/compactor; 2.3 adds updater. A
   creator has no superseded generation and cannot shrink. A compactor cannot
   shrink: [R-MDL-02] inside [R-WRT-07] makes "the output's reference arrays MUST
   equal the live generation's bit for bit"; it also mints a new file_id at
   generation 1, so its output is not an append onto F. An updater is bound by
   [R-CNF-06] to every writer requirement for bytes it produces, which includes
   [R-WRT-04]. No actor escapes.
2. Commit shape where clause A's antecedent fails: padding-only shrink of L plus
   a change to a separate layer-scope ancillary record of L. The second half of
   the bar is unconditional and still applies.
3. Commit shapes where the trigger fires anyway (de-address in dim 0 + padding in
   dim 1; padding-only shrink plus a superseded tile). Both readings re-emit.
4. Degenerate geometry: some Ei = 0 gives N = 0, entry_count = 0,
   extent_length = 0, no region to relocate.
5. Index content genuinely unchanged: entries (offset/length/crc), segment CRCs,
   segment count ceil(entry_count/2^16), crc_of_crc_array all unchanged; disk
   ordinals do not renumber since [R-GEO-06] moves them only when a Gi changes.
6. Licensed route to a longer file: supersede a tile with byte-identical content,
   which trips the trigger. Available under BOTH readings and produces a
   different byte sequence from B's. Does not move the emittable set as a
   function of the disputed reading.
7. Literal misreader emitting entry_count = 3 fires L21; nonconforming under both
   readings; the auditor concedes this.

## Why the downgrade holds

Ground 2 of the refutation establishes correctness, not imprecision. L3057 does
not itself impose an entry_count; it delegates: "[R-CNT-17] obliges the smaller
entry_count AND SO a re-emitted index region." [R-CNT-17] (L1038-1042) quantifies
over "the geometry-derived addressed-tile count", unchanged here. Re-emission is
chained by "so" to a premise that fails, so nothing is derived. L2993-2996 gives
the affirmative answer plus a flat prohibition, in the same normative step under
"An appender MUST, in order:" (L2949, confirmed non-blockquote). A prohibition
against an inference with a dead premise is not a contradiction.

Corroboration neither side cited: L610, inside a blockquote (non-normative but
shows the intended uniform reading): "A commit never relocates a live index
region otherwise; that is compaction's operation (20.5, [R-WRT-07])."

Byte-level: Writer B violates [R-WRT-04]. 2.3's gloss "Writer conformance is
semantic" does not rescue B, because [R-CNF-06] binds appenders and updaters to
every writer requirement for the bytes they produce. Appendix H is non-normative
and disclaims exhaustiveness, so its silence is not a licence. Only Writer A's
byte sequence is emittable.

## Residual, not enough to overturn

L3056's antecedent is "Where a shrink is permitted", and eleven lines earlier the
same step certifies the padding-only shrink as permitted. Read as a plain
universal, the sentence asserts something untrue of one permitted shrink. Loose
drafting, worth fixing, but it self-corrects through [R-CNT-17], is answered by a
rule quantified over the case at L2993, was not touched by either hunk, and moves
no byte.

## Verdict

DOWNGRADE_STANDS. Byte-level: NO.
