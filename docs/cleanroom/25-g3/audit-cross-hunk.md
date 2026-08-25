# Cross-hunk consistency audit — round 25, hunks 01/02/03

## Disclosure

Read: /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (via sed ranges:
§2.3–§2.4 134-271, §3.1 282-345, §5.1 tail/§5.2 600-690, §6.2–§6.4 735-866,
§9.1–§9.4 1156-1260, §10.1–§10.3 1372-1432, §11.3–§11.4 1526-1600, §13 1693-1795,
§14.3–§14.5 1889-1990, §15.1–§15.3 1989-2065, §20–§20.4 2894-3200, §20.5 3199-3340,
§21.6 3595-3650, §21.7 3649-3730, §23.1–§23.3 3923-3995, Appendix G 4256-4396,
Appendix H 4396-4467), plus greps listed below.
Read: hunk-01.diff, hunk-02.diff, hunk-03.diff in the r25audit-b scratchpad.
Did NOT read: full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, git history, the web.
Did not list the scratchpad directory (globbed hunk-*.diff only).
Unrequested context appeared before I began: a CLAUDE.md pointer, an index of the
maintainer's memory files with descriptive titles, and a git status/recent-commit
listing including commit subject lines. I did not open any of those files and did
not use their contents as evidence; the commit subjects were visible in the
environment block. No conclusion below rests on them — every claim is quoted from
spec/tarn.md or from the three hunk files.

## Greps run

  grep -n "^#\{2,4\} " spec/tarn.md            -> section map
  grep -n -i "compact" spec/tarn.md            -> 40 hits, all inspected
  grep -n -i "barrier|durable|durability|fdatasync" -> 1174,1180,1183,1193,2929-2931,3073-3076,3228,4428
  grep -n "whole-file rewrite"                 -> 1162, 3019, 3181, 3220
  grep -n "supersed"                           -> 30 hits
  grep -n "R-CNT-17"                           -> 934,1021,1042,1097,1497,2076,2103,2811,3056,3497,3498,3845
  grep -n "^| F3[456]|^| L2[45]|^| L31|..."    -> register rows F34-F36, L24,L25,L31,L33,L34,L36,L43,L45,R1
  grep -n "pre-trailer|different lengths|does not bind|torn output" -> 153,566,631,661,755,837,1983,3437,3609,4085,4104,4330

(Hard-wrap noted: all searches used short fragments or identifiers that cannot wrap.)

## Grouping (by rule touched, not by section)

Group A — "what a shrink of a layer extent may do, and how many shapes it has":
  hunk 01 (§11.1 shrink Rationale) + hunk 03 (§23.1 removal enumeration).
  Both are completeness claims over the same partition of shrinks; both were
  written to register the SAME newly-recognised second shape (a shrink that turns
  real positions of a stored tile into padding, permitted only where the stored
  byte already holds the fill).

Group B — "which text establishes a rule / which rules govern an actor":
  hunk 01 ("§20.3 states normatively, and governs, ...") + hunk 02 ("That a
  compaction is a whole-file rewrite rather than a commit fixes what the output
  *is*, not which rules govern the writing of it").
  Hunk 01 disclaims force for a Rationale and points at the normative home;
  hunk 02 reverses a claim that a normative protocol did not reach an actor.

Hunk 02 shares no rule with Group A. Its cross-checks are against §6.2, §2.3,
§21.7, Appendix G item 8 and Appendix H's writer checklist.

## Rule each repair adopts (in my words)

H1: For a layer that stored tiles in the superseded generation, a shrink is
    barred iff it alters what §14 fixes for one of those tiles (regardless of
    whether the new state still stores it); the permitted shrinks are (i) drops
    out of the addressed set and (ii) new padding positions already holding fill.
    Non-normative; §20.3 governs.
H2: A compactor is bound by [R-LIF-02]'s creation path in full — step 5's pad and
    the barriers of steps 4 and 6 included — exactly as a creator is. Compaction's
    status as a non-commit fixes the output's identity, not the writing rules.
H3: A commit makes sample data unreachable in exactly three ways; the third
    (padding-conversion inside a still-addressed stored tile) leaks nothing
    because the bytes must already equal the published fill.

## Group A — do the two repairs agree with each other?

Yes on the substance. H1's second permitted shape and H3's third way are the same
operation, and their preconditions match ("whose stored byte already holds the
fill" / "only where those bytes already hold the channel's recorded fill").
Quantifiers agree: H1's singular "a new padding position" distributes over every
new padding position exactly as §20.3's does; H3's plural "those bytes" says the
same thing.

They agree with §20.3's *test*:
  "a shrink is permitted exactly where it alters nothing §14 fixes for any tile
   the layer stores in the generation this commit supersedes"
  "... a new padding position whose stored byte already holds the fill
   `[R-SER-05]` fixes is not one, so a shrink producing only those is permitted
   here exactly as it is there"

They do NOT agree with §20.3's *consequence* sentence four sentences later
(untouched by any hunk):
  "Where a shrink is permitted the de-addressed tiles' extents become slack
   (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
   re-emitted index region, and every surviving stored tile is untouched."
A padding-only shrink de-addresses nothing: it keeps every grid count
Gi = ceil(Ei/Ti) (if one fell, tiles would be de-addressed), so entry_count is
unchanged. Worked instance: E=10, T=4, G=3 (padding at 10,11); shrink E to 9;
G stays 3; position 9 becomes padding in the stored edge tile. [R-CNT-17] fixes
entry_count to the geometry-derived count (L21), so "the smaller entry_count" is
not merely unobliged — it is unemittable. And §20.3 itself, twelve lines earlier,
says such a layer "keeps its extent slot, pointing at the existing region, ...
relocating a live index region is compaction's operation ... not an appender's."
=> finding X-01.

Both enumerations close over the same case and miss the same one: a shrink whose
new padding positions fall only in ADDRESSED-BUT-UNSTORED tiles (grid counts
unchanged, no stored tile touched). §20.3 permits it — its bar ranges only over
tiles the layer *stores* in the superseded generation, and an unstored tile has
no §14 obligation and no "stored byte". H1 says the two shapes are "the ordinary
case" and "the other"; H3 says "three ways". => finding X-02 (non-byte-level:
H1 is a ">" Rationale, [R-CNF-01]; H3's list precedes a MUST NOT quantified over
"any commit that makes sample data unreachable").

## Group B — do H1 and H2 agree about where rules live?

Yes, and they use the same move in opposite directions, correctly.
H1: a Rationale must not carry the rule -> points at §20.3 as the normative home.
    Verified: §20.3 step 4 does state the bar, the tense, the carve-out and the
    rescue answer normatively. H1 adds no rule not present there.
H2: the classification of an operation ("a whole-file rewrite, not a commit")
    must not be read as an exemption from a protocol -> imports [R-LIF-02]'s
    creation path by an explicit MUST in §20.5.
No conflict. H1 never mentions compaction; H2 never mentions geometry.

## Direction check on H2 (is the new side the right side?)

Corroborating the new side, all untouched:
 - Appendix H, "Conforming writer": "follows the commit protocol including both
   barriers (§9.2)". A compactor is a writer for the bytes it produces
   ([R-WRT-01], [R-CNF-06]).
 - §6.3 needs an explicit compactor carve-out from flags = 0 ("A compactor,
   though its output is a new file, carries the input's unknown ignore-lane bits
   ... rather than writing flags = 0"). A carve-out is only needed if creator
   rules otherwise reach a compactor.
 - Appendix G item 8: "A compactor's output is therefore reproducible only modulo
   its trailer" — true under the new text; under the deleted text the output's
   LENGTH also varied, and only profile item 3 (not the format) pinned it.
So the deleted paragraph was the defect and the reversal is correct.

## Citations opened

[R-LIF-02] §9.2 creation path: "On creation there is no prior trailer: the writer
  first emits the front signature block (§6.1) ... then performs steps 2-6,
  writing beginning at offset 16, with generation 1." -> H2's "the output has no
  prior trailer and stands at generation 1, which is the case that path states"
  PASSES; steps 2-6 do contain step 4's barrier, step 5's pad+trailer, step 6's
  barrier.
§20.2 [R-WRT-02]: "A creator MUST follow `[R-LIF-02]`'s creation path ... 
  (`[R-LIF-02]` steps 4-6 — both barriers, not one)." -> H2's "as §20.2 obliges a
  creator" and "both, not one" are word-for-word the same governing verb and the
  same emphasis. PASSES.
[R-WRT-01] §20.1: "An appender and a compactor satisfy every writer requirement
  for the bytes they produce". H2: "already has a compactor satisfying every
  writer requirement for the bytes it produces." Quote matches, but the analogy
  overreaches for the barriers — see X-06.
[R-LIF-01] 9.1: "every conforming mutation of a file is either a commit (§9.2) or
  a whole-file rewrite under a new file_id (compaction, §20)". PASSES for H2's use.
[R-LIF-03] §9.3 (cache contract, (file_id, range)). PASSES (context line).
[R-CNT-08]/§6.3 (ignore-lane carry-forward). PASSES, no collision with the
  creation path: flags = 0 is §6.3's rule, not [R-LIF-02]'s.
[R-CNT-26] §6.3 minor floor. PASSES.
§10.1 four vehicles / §10.2 eight spaces / §21.6: "the two of §10.1's four
  vehicles §21.6 makes conforming" = ignore-lane bit + unrecognized tarn. key,
  both present in §21.6's table. "one row for each of the other seven spaces
  §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" — §10.2 tabulates 8 spaces,
  minus record type = 7, and 7 rows are named. F36/L25 are the "whatever its MU
  bit" emission rows (F35/L24 are the MU=1 reader rows), so naming F36 and L25
  for the emission violation is right. PASSES (context, unchanged by this commit).
§20.3 step 4 (H3's citation): the shrink rule and its carve-out are there. PASSES.
[R-SER-05] §14.5: "at every padding position, a writer MUST encode ... that
  channel's fill value". [R-TYP-06] §13.1: fill is recorded in the channel entry
  and readers MUST take it from there. -> H3's "already hold the channel's
  recorded fill, which the layer record publishes" PASSES.
[R-CNT-21] §5.2 slack. PASSES for H3's "leave the bytes in the file as slack".
§9.6 recovery scan. PASSES. §20.4 dropped record's extent becoming slack. PASSES.
[R-CNT-17]: "entry_count ... equals the addressed-tile count"; L21 makes a
  mismatch reject-layer. This is the citation that defeats §20.3's consequence
  sentence for a padding-only shrink (X-01).
§21.7's "§20.3 step 4's bar ... is witnessed only where the affected tiles remain
  stored" and "a commit that supersedes every tile it would have damaged leaves
  the live state clean" -> §20.3's "§21.7 records the consequence" PASSES (its
  antecedent is the rescue question, which is what §21.7 records).

## Check 6 — what the repairs leave unconstrained

Structure H1/H3 govern: a layer's declarations a commit may change. Members:
extents Ei, tile extents Ti, rank, dimension names, channel names/types/fills,
layout, linearization, codec, filter, index_encoding, slab/alignment.
 - Ti change: alters P, decoded size -> barred by the §14 list. Constrained.
 - Ei shrink within a tile: the carve-out. Constrained (fill precondition).
 - Ei shrink across a tile boundary: de-address. Constrained.
 - pad bits (§14.3): count is P mod 8, P = prod(Ti) — an extent change cannot move
   them. No unconstrained sibling here.
 - decoded size / sample byte offsets: functions of Ti, layout, types
   ([R-SER-07]) — untouched by an extent change. Consistent.
 - fill value change: §20.3 example (c) handles.
 - slab/alignment: §20.3's closing clause handles ([R-SLB-04], [R-SLB-01]).
No unpinned sibling found for Group A.

Structure H2 governs: the compaction output's writing procedure + its trailer.
Members: front block, structure placement, directory+CRC, pad, trailer fields
(magic, version_major, version_minor, flags, generation, dir_offset, dir_length,
committed_file_length, file_id, reserved, CRC), barriers.
 - pad: NOW pinned (was the gap).      - barriers: NOW pinned.
 - file_id, generation, flags, version_minor: pinned in §20.5.
 - committed_file_length, dir_offset/dir_length: pinned via step 5 + §6.2/[R-CNT-06].
 - version_major, reserved, CRC: pinned by §6.2 + file conformance.
 - physical length beyond F: pinned by [R-CNT-06] (size must equal F).
No unpinned sibling found for H2 either. What the repair did leave is the two
stale restatements X-04 (§21.7's count of four) and X-05 (§6.2's "no conforming
commit").

## Check 7 — analogies, verb by verb

H2 (i): repair "A compactor MUST **follow** [R-LIF-02]'s creation path" vs
        §20.2 "A creator MUST **follow** [R-LIF-02]'s creation path". Same verb,
        same object, same set (a writer emitting a generation-1 file with no
        prior trailer). SOUND.
H2 (ii): repair "the barriers of steps 4 and 6 — **both, not one**" vs §20.2
        "([R-LIF-02] steps 4-6 — **both barriers, not one**)". SOUND.
H2 (iii): repair "[R-WRT-01] already **has a compactor satisfying every writer
        requirement for the bytes it produces**" vs [R-WRT-01] "satisfy every
        writer requirement **for the bytes they produce**". Same words — and that
        is the problem: the cited rule ranges over produced BYTES, while two of
        the three obligations the sentence is supporting (the barriers) produce
        no byte and are not properties of any byte. Sound for the pad, unsound for
        the barriers. => X-06. Tested member by member as the charter requires.
H1: "§20.3 states normatively, and governs" — not an analogy but a locus claim;
    verified above. H1's "barred wherever it alters what §14 fixes for such a
    tile" vs §20.3's "alters nothing §14 fixes for any tile the layer stores in
    the generation this commit supersedes": "such a tile" distributes as "any",
    and both are in the superseded generation's tense. SOUND.
H3: "goes the same way" (dropped ancillary record's extent) vs §20.4's "drop it —
    its extent becoming slack". Both are "becomes slack". SOUND.

## Findings

X-01 hunks 1,3 — §20.3's consequence sentence restates the narrow shrink
X-02 hunks 1,3 — both enumerations close over two/three cases and miss one
X-03 hunk 3   — "without de-addressing it": pronoun
X-04 hunk 2   — §21.7's "four obligations" not swept
X-05 hunk 2   — §6.2's "no conforming commit produces one" not swept
X-06 hunk 2   — [R-WRT-01] warrant does not reach the barriers
