# A-02 refute pass — lens: shared premise

## Access disclosure
Read: case/case-A-02.md, hunk-01.diff, spec/tarn.md (sed/grep only). Nothing else.
Did not read full.diff, other hunks, docs/, conformance/, git history, or the web.
Unrequested context appeared before I began (project instruction pointer + an index of the
maintainer's memory notes). I opened none of the files it named; nothing from it entered the
reasoning. Every claim below is sourced to a quoted line of spec/tarn.md.

## Passages read
1466-1520 (§11.1 whole + §11.2); 100-115 ([R-CNF-01]); 1034-1042 ([R-CNT-17]);
1544-1560 (§11.4/[R-GEO-05]); 1566-1580 ([R-GEO-06]); 2098-2110 (§15 Note);
2828-2842 (§19.2); 2975-3000 (§20.3 step 4 / [R-WRT-04]).

## Greps and exact output
$ grep -n "last-declared" spec/tarn.md
1553:the last-declared dimension varies fastest — is the only value this
2202:> last-declared dimension. Rectangular-window locality is therefore

$ grep -n "\blast\b" spec/tarn.md
163: that last / 194: the last where / 504: The last two / 566: trailer last, in that order /
614: the last ones in the file / 1249: the last committed state / 1294: nearest-to-end ... last
committed state / 1502: FLAGGED / 1527: the last row of tiles / 1553: last-declared /
1900: beyond the last value / 2096: the last covering 16,960 entries / 2202: last-declared /
3466: after the last complete record / 3717: the last two / 3755: The last three rows /
4296-4297: the last eight bytes in output order — the eight a named hash emits last

$ grep -n "zero-extent" -> 66 (§1 intro), 1502 (flagged), 2834 (§19.2). Term never defined.
$ grep -n "§11.1"      -> 1018, 1793, 3027. No normative rule leans on the §11.1 Rationale.
$ grep -n "no region at all" -> 2105.
$ grep -n "leaves \*\*entry_count\*\*|stays 0 among them|count included|Growth that changes"
  -> 1496, 1498, 1503.

## Downgrade's props, tested
(1) subject defines the set, clause is a checkable membership claim; (2) preceding sentence
decides every divergent case; (3) the positional idiom is "last-declared", not bare "last";
(4) [R-CNF-01] force.

### (3) is false on the document's own evidence, and inverted
13 of the 15 other bare-"last" occurrences mean *final member of an ordered sequence*
(163,194,504,566,614,1527,1900,2096,3466,3717,3755,4296,4297). The two remaining (1249,1294)
mean *most recent committed state*, and 1294 re-glosses even that positionally: "The
nearest-to-end valid candidate is the last committed state." ZERO occurrences use "last" in
the sense the repaired clause needs — final remaining member of a set exhausted across a
history of commits. The house sense of bare "last" is ordinal-in-sequence: the reading that
breaks the clause.

### Referent asymmetry the downgrade never addresses
Positional reading has an antecedent in the same sentence pair: "one grid count ⌈Eᵢ / Tᵢ⌉
(§11.2)" (1497), an i-indexed sequence whose declared order the document makes load-bearing at
[R-GEO-05] (1553) and [R-GEO-06] ("s = Σᵢ tᵢ · ∏_{j>i} Gⱼ", 1571). Temporal reading needs an
antecedent the paragraph never supplies — a sequence of prior growth commits. The subject is a
single growth; no history is introduced anywhere in the block.

### (2) is self-correction, not correctness
Divergence requires >=2 zero grid counts. Constructions built:
- rank 1 / exactly one zero: readings coincide. No divergence.
- E=(0,100,0) T=(4,4,4), raise E_2 -> G=(0,25,25): clause (positional) says branch 2; N=0 =>
  branch 1. Preceding sentence's illustration matches literally.
- E=(0,0,0), raise E_1 and E_2, leave E_0=0: positional "last zero" G_2 IS raised, clause says
  branch 2; N=0 => branch 1. The illustration ("raising ONE grid count") does not literally
  match; only the general antecedent decides, and only if the reader recomputes ∏Gᵢ.
- E=(0,100,0)->(0,100,100)->(50,100,100): on growth 2 the only remaining zero is G_0, which is
  also the positionally-last zero. Readings coincide.
Containment holds — but what it establishes is that the paragraph contradicts itself four
lines apart under the positional reading. That is a second defect, not a cure, and it fires
only for a reader who re-derives ∏Gᵢ instead of trusting an "— X included" appositive whose
entire function is to name a member the reader would not otherwise derive. Prop (1) has the
same shape and concedes the point: a reader "handed the test that tells him he picked the
wrong referent" is a reader the text sent down the wrong branch first.

### (4) byte-level — tried to break it, could not; stronger than stated
- Writer/updater over-emitting: positional reader commits (0,100,0)->(0,100,100), believes
  entry_count changed, sets out to re-emit "the whole tile-index region". entry_count is still
  0, so [R-CNT-17] forces extent_length "0 when entry_count is 0" and §15 forces "extent slot
  (0, 0) and crc_of_crc_array = 0 — zero segments, a zero-byte CRC array". The region is zero
  bytes; nothing to write, not even slack. Byte-identical under both readings.
- Writer/updater under-emitting: declining to emit on the growth that does take entry_count off
  0 yields extent_length 0 with entry_count N>0 — a straight [R-CNT-17] validity error at layer
  scope. Barred under both readings ([R-CNF-05] shape). Emittable set does not move.
- Reader/verifier: §19.2 step 1 routes "any region of a zero-extent layer" to "succeeds and
  returns no samples ([R-GEO-02])"; §20.3 step 4 keys on "stored-tile set or index content" and
  names "entries new to this generation (added tiles, grown extents)". No verdict touches "last".
- Dependency: no normative rule references the §11.1 Rationale; §13's Note (1791-1793) restates
  the rule with no "last" in it.

## Answers
1. Real as text: YES. Repair-introduced NEW_AMBIGUITY. Correct grade CONFIRMED, not REFUTED.
2. Byte-level: NO. Confirmed independently, by a tighter route than the downgrade used.

## Missing sentence
Replace 1502-1503 with: "— the growth after which no grid count of a zero-extent layer is 0
included, whichever dimension it belongs to." Everything the downgrade uses to resolve the
clause is in the document; what is absent is any sentence fixing the sense of bare "last" in
this clause. §11.4 fixes only the compound "last-declared".
