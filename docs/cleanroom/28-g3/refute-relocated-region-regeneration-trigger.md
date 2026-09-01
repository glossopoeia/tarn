# Refute-only verification — R28 finding: §20.5 [R-WRT-07] regeneration trigger

Verdict: **NOT_BYTE_LEVEL**

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
Commands run, all against that file only: `wc -l`, `sed -n` on line ranges,
`grep -n` for rule identifiers and for `compact|relocat`. No other file was
read, no directory listed, no git, no network, no scratch scripts executed.
Scratch dir created (`priv-relocated-region-regeneration-trigger/`) but never
needed; only this transcript was written.

Unrequested context appeared in my context before I began: a project
instruction block naming a CLAUDE.md/AGENTS.md, a user email, a date, and an
environment/git block naming the repository, branch and recent commit subject
lines (several of which describe cleanroom rounds and ADRs in prose). I
disregarded all of it; none of it entered the reasoning below.

## Sections opened

§2.1 [R-CNF-01] normative text; §2.2; §2.3 [R-CNF-02]/[R-CNF-05]/[R-CNF-06]/
[R-CNF-11]/[R-CNF-13]; §2.4 [R-CNF-07]/[R-CNF-08]/[R-CNF-12] incl. the
preserve-verbatim row; §2.5; §4.1 [R-ENC-01] (little-endian); §5.1 [R-CNT-01]/
[R-CNT-27] + the three-commit Example; §5.2 [R-CNT-02]/[R-CNT-21]/[R-CNT-03];
§7.1 [R-CNT-11]/[R-CNT-25]; §7.2 [R-CNT-12] record framing + extent slot;
§7.4 [R-CNT-23]/[R-CNT-17]/[R-CNT-18] layer record + its Example; §15.1
[R-IDX-01]; §15.2 [R-IDX-02]; §15.3 [R-IDX-03]; §15.4 [R-IDX-04]/[R-IDX-05];
§20.1 [R-WRT-01]; §20.2 [R-WRT-02]; §20.3 [R-WRT-04] steps 1–6; §20.4
[R-WRT-05]/[R-WRT-08] + table; §20.5 [R-WRT-06]/[R-WRT-07]/[R-WRT-09] + both
Examples and the Note; §21.1 (how to read the register); §21.2 F27/F28/F33;
§21.3 L18/L23/L27/L37/L40–L42; §21.4 T1/T6–T12; §21.6; §21.7 [R-ERR-01];
§21.8; Appendix G items 1–10.

## The two readings, restated precisely

Governing sentence, §20.5 [R-WRT-07] (lines 3403–3410):

> A compactor MUST preserve content, and preserves no placement — placement is
> not among the things it carries forward, and it is free to place structures
> anywhere §5.2 admits and every declared layout invariant permits
> (`[R-SLB-01]`, `[R-SLB-03]`): every stored tile's bytes verbatim — each index
> entry's crc is unchanged — and every retained record per §20.4, except that
> relocation re-points extent slots, regenerates each relocated tile-index
> region (entry offsets new; entry lengths, entry crcs, and sentinel entries
> unchanged; segment CRCs recomputed over the entries as re-emitted), and
> updates the layer-record fields covering a regenerated region
> (crc_of_crc_array).

(i) literal: the exception fires on relocation *of the region*.
(ii) purposive: it fires on relocation of *the extents its entries address*.

## Construction A — the reporter's direction, made concrete

Layer `sst` of §7.4's Example (rank 1, extent 100, tile extent 32 → grid count
4 → entry_count = 4; index region = 4×20 + ⌈4/2¹⁶⌉×4 = 84 bytes; layer-record
inline payload 81 bytes, header 24, so the directory is 24+81+4 = 109 bytes).
Tile 0 stored, 128 bytes (32 float32, codec 1); entries 1–3 sentinel.

Input I (conforming; the 200-byte hole is a superseded commit's dir/pad/trailer):
  front [0,16) · index region [16,100) at X = 16 · slack [100,300) ·
  tile 0 [300,428) · directory [428,537) · pad [537,576) · trailer [576,640),
  F = 640 (64 | 640 ✓). Entry 0 = (offset 300, length 128, crc c).

Compactor chooses the placement §20.5 expressly grants it ("free to place
structures anywhere §5.2 admits"): region back at 16, tile packed to 100.

Output Q (reading ii): front [0,16) · region [16,100) · tile [100,228) ·
  directory [228,337) · pad [337,384) · trailer [384,448), F = 448 (64 | 448 ✓).
  Region regenerated: entry 0 offset = 100 → bytes at file offset 16 are
  `64 00 00 00 00 00 00 00` (little-endian, [R-ENC-01]); segment CRC at
  [96,100) recomputed; crc_of_crc_array in the layer record updated.
  Reclaimed 640 − 448 = 192 bytes. Q is conforming.

Output P (reading i, same placement): region preserved verbatim → bytes at
  offset 16 are `2C 01 00 00 00 00 00 00` (300). In Q's layout F − 64 = 384 and
  300 + 128 = 428 > 384 → **T9**; the extent also overlaps the directory
  [228,337) → **F33**. P is nonconforming.

So P is barred under both readings by [R-CNF-05] ("A writer MUST emit only
conforming files") and by [R-WRT-07]'s own closing MUST. Triage's verdict on
this half is right. The half triage never tested is the mirror: **is Q
emittable under reading (i)?**

## The mirror question, and why it still does not fork the bytes

Under (i) the exception does not reach a region that stayed at X, so the
region's extent content is preserved (§20.4's preserve-verbatim, which §2.4
routes through the MU = 1 and MU = 0/PE = 1 rows; the layer record is
registry-fixed MU = 1, PE = 1 per §7.4's Example). Regenerating it is then
unlicensed, so under (i) *this compactor, on this input,* cannot produce Q: at
that placement it would have to emit P, which is barred, so it must pick
another placement (relocate the region, or leave the tile where it lies). Under
(ii) Q is exactly what is owed. The input→output pair (I, Q) is therefore
permitted under (ii) and not under (i).

That is a difference in one operation's mapping, not in the emittable set. The
byte string Q is emittable under reading (i) too, by two independent routes:

1. **By a compactor under reading (i).** Take I₂: front [0,16) · tile
   [16,144) · index region [144,228) · slack [228,428) · directory [428,537) ·
   pad · trailer, F = 640. I₂ is conforming and its layer record differs from
   Q's only in extent_offset (144) and crc_of_crc_array. Compacting I₂, the
   compactor places the region at 16 and the tile at 100. The region *is*
   relocated (144 → 16), so even the literal trigger fires: entry offsets new
   (100), lengths/crcs/sentinels unchanged, segment CRC recomputed,
   crc_of_crc_array updated. The output is Q, byte for byte. [R-WRT-06]'s
   fresh file_id is a MUST on the draw, not on the value (§9.3 is advice,
   and [R-CNF-12] puts SHOULD deviation outside the register), so Q's file_id
   is available.
2. **By a creator, under either reading.** [R-WRT-02] admits Q's layout
   exactly — "each layer's stored tiles, tile-index region, and any record
   extents, in any order satisfying §5.2's coverage classes … placement is
   otherwise free (`[R-SLB-05]`)". And §21.7 forecloses any way to tell the
   two apart: "the output carries no record that it is a compaction output at
   all".

Symmetrically, every *conforming* output reading (i) permits is emittable under
(ii). Proof (this is the general form of the reporter's case, not one example):
suppose a compactor under (i) leaves the region at X with stale entries and the
output is conforming. Entry k's extent [oₖ, oₖ+lenₖ) is a claimant of the live
state, so by [R-CNT-02] it overlaps nothing else and is not slack; by T1 the
bytes there carry crc ₖ; by [R-WRT-07]'s closing MUST the reference array is
unchanged. Hence tile k's bytes lie at oₖ — its input offset — i.e. no affected
tile actually moved. A compactor under (ii) reproduces that byte string by
placing tile k at oₖ, whereupon no entry's extent is relocated, no regeneration
is owed, and the region is preserved verbatim: identical output. (The variant
where a *different* tile with identical bytes sits at oₖ collapses the same
way: the bytes are the same file.)

So: emittable-set under (i) = emittable-set under (ii), as sets of byte
sequences. What the two readings actually disagree about is which *placements*
a compactor may use — and placement is the one dimension the same sentence
declares free ("preserves no placement … free to place structures anywhere
§5.2 admits") and [R-CNF-05] declares non-canonical ("two conforming writers
given identical input MAY produce different conforming files"). Discriminator 4
allows that sentence to license divergence "within what the rules leave open";
placement is left open by [R-WRT-07] itself.

## No accept/reject verdict moves

The disputed text binds writers only. No §21 row keys on whether a region was
regenerated; §21.7 states the ground — "the output carries no record that it is
a compaction output at all, so no check can know that any of the three was
owed" — for [R-WRT-06]'s three trailer obligations, and it holds a fortiori
here. Q is accepted under both readings; P is rejected under both (T9, F33).

## Refutation attempts and what killed each

See `constructions_tried` in the structured result — eight constructions, each
with the sentence that killed it.

## Residual

The finding is real and the repair is right: the trigger names the wrong
condition, and an implementer who takes it literally and holds the placement
fixed writes a file that fires T9/F33. That is a genuine defect. It is not
byte-level, because (a) the file the literal reading produces at that placement
is nonconforming and barred under both readings, and (b) the file the purposive
reading produces is emittable under the literal reading too — by the same
compactor on a neighbouring input, and by any creator — so no byte sequence
enters or leaves the emittable set and no file's verdict changes.
