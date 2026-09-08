# 0123. Round 31's repairs, and the geometry the §14 bar did not name

- Status: Accepted (resolves round 31's repairable findings) — decision 1 superseded in the form it landed by ADR-0124, which puts the tile extents and dimension order on a populated layer's fixed list
- Date: 2026-09-03
- Covers: §20.3 step 4's §14 bar, its gloss and a new paragraph on the tile
  extents and dimension order; §11.1's Rationale; §2.3 `[R-CNF-03]`; §21.9
  `[R-ERR-04]` and its hard-limit list; §5.2 `[R-CNT-21]` and §9.7
  `[R-LIF-08]`; §20.3 step 2, the re-emission clause, the ordinal bar's gloss,
  the growth and shrink paragraphs, ADR-0122's erratum sentence and the
  three-shapes Example; §23.1 `[R-PRV-01]`; §6.2's trailer table; §21.6's
  zero-layers and experimental-type entries; §13.3's sparse-writing Note;
  Appendix H's writer and updater checklists; §14.2 `[R-SER-08]`, §19.4 step 8
  and §21.1; §20.4's preservation table; §22.3 `[R-SEC-04]`
- Confirm: none. Two decisions were put to the maintainer and confirmed on
  2026-09-04. (1) That the §14 bar reaches a change to a layer's tile extents
  or to the declared order of its dimensions wherever the layer stores any
  tile, decided on the ground ADR-0081 and ADR-0114 already record; the
  alternative is stated below so a superseding ADR can choose it. (2) That
  `[R-ERR-04]`'s scope enumeration is a floor rather than a ceiling, which is
  how `[R-COD-06]` and `[R-CNF-11]` already read it. The maintainer confirmed
  the round-31 model policy the same day, Opus standing for every lane, and
  directed that specification prose carry no nested em-dash phrase; decision
  11's sentence, the one place these repairs had introduced one, was
  restructured into two sentences on 2026-09-04.

## Context

Round 31 read round 30's repairs and the three decisions taken after them —
ADR-0119 through ADR-0122 and the pre-round-31 audit's sixteen edits, seventeen
passages over five commits — with every lane on Opus. It returned 24 findings
from 7 reporters, 20 distinct defects with all three passes agreeing on the
partition, a 15/15 quiz, and **one byte-level flag, new, upheld by all three
passes and confirmed by hand.** The refute phase never attacked it: the phase
fires on a downgrade, a split or a zero, and a unanimous uphold is the one
shape it does not test.

**The flag.** A commit that permutes a layer's declared tile extents.
Interleaved, rank 2, extents (4, 4), one uint8 channel, codec 1, filter 1, tile
extents changed from (4, 1) to (1, 4): the grid goes from (1, 4) to (4, 1) and
N, P, Q, the decoded size, entry_count, `[R-CNT-17]`'s extent_length, the byte
offset and type of every value, and the disk-ordinal set are all unchanged;
there is no padding position either way, since 4 mod 4 = 0 and 4 mod 1 = 0.
Not one index entry changes, so the re-emission clause does not fire and the
commit is a shape-(c) directory-only commit rewriting sixteen bytes of one
layer record. But by `[R-GEO-06]` byte k of the tile at ordinal s denoted
coordinate (k, s) before and denotes (s, k) after: the array is transposed
over bytes the writer never stored that way, and the output is an ordinary
conforming file that every checksum certifies and §21.7 leaves unwitnessed.

The §14 bar's subject was *"what §14 fixes for its stored bytes or how they
decode"*, and its list named no geometry. The coordinate a stored value denotes
is §11.4's, which §14.1 cites and does not state; §20 never mentioned tile
extents; the bar's gloss stated a sufficient condition for permission and not
its contrapositive; and the sample-type paragraph ran the argument that
decides the case — *"the type is what fixes the value a stored bit pattern
denotes, so under a new one the same bytes denote different values"* — for the
type alone. One updater re-tiles in place and emits a conforming file; another
refuses and writes a new layer or a whole-file rewrite. The disputed file is
conforming and only one reading lets a conforming updater produce it. The same
fork reaches a reordering of the dimension entries, which transposes by the
same mechanism.

**Why this is a repair here and not a ledger entry.** ADR-0081 read step 4 as
the rule that a declaration change which would reinterpret stored bytes is not
an appender's operation but a new layer or a rewrite; ADR-0113 applied it to a
planar layer's disk ordinals; ADR-0114 withdrew a redundant sample-type bar on
the ground that the §14 bar was always that rule and made the type case
concrete in the gloss because the misreading was available to any reader. The
tile extents and the dimension order are the same case for the coordinate that
the type is for the value, and the trail has decided the principle twice. What
the document lacked was the sentence, and ADR-0091's rule — a rule's reach is
settled by an ADR — is satisfied by this one. The maintainer's confirmation is
asked for in the Confirm line because the skeptic pass graded it a decision,
and the alternative is recorded under *Alternatives rejected*.

**The other nineteen** are editorial, register-bookkeeping or figure defects,
every one confirmed by all three passes, and eight of them sit in this cycle's
own surface: four in sentences the surface rewrote and four in text a decision
left leaning on the rule it replaced — the twelfth shape round 31's charter
named. The findings file records each with its reporters.

## Decision

**1. The §14 bar names the coordinate, and the declarations that fix it.** Its
subject now reads *"what §14 fixes for its stored bytes or how they decode, or
the coordinate §11.4 assigns any value they decode to"*; its list gains *"the
coordinate (`[R-GEO-06]`) each value in the image denotes"*; and its gloss says
what *meaning* is — a change that leaves every stored byte meaning what it
meant, *"the value each denotes, at the coordinate it denotes it"*, is not what
the bar bars. A paragraph on the sample-type paragraph's model follows it:
*"A layer's declared tile extents, and the declared order of its dimensions,
are such declarations too, and changing either is such a change wherever the
layer stores any tile: they are what fix the coordinate each stored value
denotes (`[R-GEO-06]`), so under new ones the same bytes denote samples the
writer did not store there"* — and it says why no listed quantity need move,
gives the re-type's escape, *"a new layer, or a whole-file rewrite"*, and names
an extent's growth and shrink as *"the geometry changes this step permits"*.
§11.1's Rationale names the case beside re-typing: *"so is a change to the tile
extents or the dimension order, barred wherever the layer stores any tile"*.
The quantifier is *any tile* because every tile of a layer, planar or
interleaved, is addressed under the same tile extents and dimension order.

**2. `[R-CNF-03]`'s exclusion says *top-level*.** The acceptance duty is now
withheld only from a file *"carrying no top-level record of a type it does not
implement with MUST_UNDERSTAND = 1"*, which is the qualifier §21.6's closing
paragraph calls load-bearing and `[R-CNT-18]` states as a prohibition; §21.9's
`[R-ERR-04]` names *"an unimplemented top-level MU = 1 type"* the same way.
Four reporters found the unqualified form.

**3. The growth paragraph describes the carve-out's padding limb as a limb.**
*"its padding limb covers a position whose stored byte, or bit in a packed
plane, already holds the fill it keeps"*, after two reporters read the
sentence as defining a one-limbed carve-out three paragraphs after the bar
gave it two.

**4. A resource decline is a third cause of an incomplete walk**, at §5.2 and
§9.7: *"because the verifier declined a scope on resource grounds
(`[R-ERR-04]`)"*. Both statements had enumerated two causes, each presupposing
an established violation, and a verifier that declines a conforming layer
declaring entry_count = 2³² cannot enumerate that layer's extents.

**5. The carve-out reaches a bit.** *"or bit in a packed plane"* at the bar's
gloss, the growth sentence and the shrink paragraph, in §11.1's Rationale, and
in §23.1's privacy claim, where a packed planar bool plane's padding position is
a bit `[R-SER-05]` fixes and the carve-out had been stated over a byte.

**6. §6.2's `flags` cell states a value**, as its nine sibling cells do:
*"bits 0–15 (incompat lane) all zero, a set bit being reject-file (F19); bits
16–31 (ignore lane) 0 when created under this text, a set bit carried and
ignored (§6.3)"*.

**7. §21.6's zero-layers entry** no longer fuses `[R-CNT-14]`'s two statements:
*"a directory carrying no layer record is a conforming generation whether or
not it carries other records, an empty directory included"*.

**8. §13.3's sparse-writing Note** is keyed as `[R-WRT-04]` is — *"each commit
that changes a layer's stored-tile set or its index content"* — a shrink that
drops only sentinel tiles and a permitted planar channel removal both
re-emitting the region without a growth.

**9. Shape (c) of the three-shapes Example names the drop** ADR-0120 licensed:
*"or dropping a PE = 0 record where §20.4 licenses the drop, any extent it
owned becoming slack"*. No fourth shape: a drop-only commit re-emits only the
directory, which is (c)'s defining sentence.

**10. Appendix H's writer and updater entries carry the `flags` rules** ADR-0121
stated in four normative places — *"writes flags = 0 on creation"*; *"copies
forward the input's unknown ignore-lane flag bits, clears none and sets no
other"* — the one obligation `[R-CNF-02]` declares no verifier can witness.

**11. `[R-ERR-04]`'s enumeration is a floor.** *"It MAY also decline at any
scope that contains the narrowest one, as `[R-COD-06]` provides for a frame's
window and `[R-CNF-11]` presupposes"*. Both citing rules already grant a layer-scope decline over a
tile's frame window; an enumeration in one rule does not repeal a grant in
another, so nothing a reader may do changes, and the three passages now agree.

**12. §21.9's hard-limit restatement of the lz4 cap** carries both of
`[R-COD-07]`'s qualifiers again: *"with every addressed tile's decoded size at
most `0x7E000000`, the largest channel plane governing in a planar layer"*.

**13. §21.6's experimental-type entry cites `[R-CNT-18]`** beside `[R-CNT-15]`,
its Defined-behavior cell naming L25, a layer sub-record row.

**14. §11.1's Rationale names the growth permission** it had omitted while
restating the bar as reaching a growth: *"A growth is permitted outright"*, in
§20.3's own words.

**15. The renumbering occasions are two.** The re-emission clause's
parenthetical reads *"a geometry change, or a permitted change to a planar
layer's channel declarations, renumbers ordinals wherever `[R-GEO-06]` moves
them"*, and the ordinal bar's gloss no longer says a geometry change is the
*only* stated occasion: ADR-0122 made a planar channel removal an operation,
and one that removes a channel none of whose successors store a tile renumbers
sentinel entries with no geometry change. ADR-0113 left the parenthetical
untouched on the ground that a permutation was barred wherever a tile is
stored; that ground still holds for stored tiles and never covered this case.

**16. ADR-0122's erratum sentence names its antecedent**: *"a commit that also
alters what §14 fixes for a tile the layer stores in the generation this
commit supersedes is barred"*, where *such a tile* had its nearest antecedent
in the de-addressed tiles the preceding clause says carry no §14 obligation.

**17. `[R-SER-08]` says what a reader returns**, as §19.4 step 8 already says of
it: *"MUST return 0x00 as false and every other byte as true — the value,
encoded 0x00 or 0x01 as above, and not the stored byte"*. §19.4 and §21.1 no
longer say *the one byte* where 254 byte values are excluded.

**18. Step 2 no longer borrows `[R-WRT-01]`'s reliance clause** for a re-emitted
record that `[R-WRT-03]` says re-emission relies on: *"a violation latent in a
structure it carries forward unmodified travels with that structure"*, and
*"validating either to `[R-WRT-03]`'s depth is not authoring it"*.

**19. §20.4's table is headed *Governing flags***, and its introducing clause
reaches all three flag sources the paragraph names: *"Whichever source governs,
its flags carry these obligations"*.

**20. §22.3's third residue states its trigger once**, `[R-LIF-06]`'s, the
dangling *before any use* and the third restatement cut.

**Declined.** Widening the carve-out's filter limb to a single-group image — the
limb is a property, satisfied wherever the identity holds. A fourth commit
shape.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors,
Appendix A byte-identical. Decision 1 constrains updater conduct with no
single-file witness and belongs where the bar already sits, outside
§21.2–§21.5; §21.7's test decides it without a row. Decision 11 changes what no
reader may do, the two citing rules having granted it already.

**What decision 1 costs a caller**: nothing that was ever coherent. Re-tiling or
transposing a populated layer in place made the stored bytes denote samples
the writer never stored, with every checksum certifying the result; it is now
what re-typing is, a new layer or a whole-file rewrite. An empty layer is
re-declared freely as before, and growth and shrink are untouched.

**The round did not meet G3's second half.** The criterion asks that the round
reading the previous round's repairs return zero; round 31 returned one, new,
in the step this cycle edited most, in a sentence it did not edit. Round 32
reads this ADR's repairs, and the criterion turns on it.

**The repair list was ticked against the diff**, as ADR-0119 records is owed
after every repairs commit: twenty items, thirty-one anchors, every item in the
diff and none deferred.

**A harness obligation, for round 32**: the refute phase attacks downgrades,
splits and zeros, and never a unanimous uphold. This round the driver's
hand-check stood in for the refuter it did not run; the next harness should run
one, told to find the sentence that decides the finding.

## Alternatives rejected

- **Permit the re-tiling**, by stating that the §14 bar does not reach a
  tile-extent or dimension-order change. Coherent as a sentence, and it would
  let a directory-only commit transpose an array over unchanged bytes with no
  check able to see it (§21.7); it contradicts the bar's own gloss and the
  ground ADR-0081 and ADR-0114 record. Stated here so the maintainer can choose
  it by superseding decision 1.
- **Send the geometry question to the ledger** as a reach question, on
  ADR-0091's rule. Rejected: the principle is decided twice in the trail, the
  alternative has no defender, and a round-32 reading of an unrepaired fork
  is the shape that has produced the next finding every time (ADR-0122's
  ground); the Confirm line keeps the maintainer's veto.
- **Narrow `[R-COD-06]` and `[R-CNF-11]` to the tile** instead of reading
  `[R-ERR-04]` as a floor. That would withdraw a decline two rules grant and
  make §18.2's Note, which lets a reader decline the whole file for a
  document, an exception rather than an instance.

## Precedent

- **ADR-0081** and **ADR-0114**: a declaration change that reinterprets stored
  bytes is not an appender's operation, and the §14 bar was always that rule.
- **ADR-0113**: the disk-ordinal bar, whose tense and escape decision 1 shares.
- **ADR-0119**: the repair list against the diff, owed after every repairs
  commit and paid here.
- **ADR-0091**: a rule's reach is settled by an ADR; this is the ADR.
- **ADR-0104**: editorial changes need a check, not an ADR — the nineteen
  editorial repairs ride with decision 1 rather than separately.

## Erratum, 2026-09-08 — the pre-round-32 audit

Nine lanes read the twenty-five hunks of this decision's two commits before
round 32 was chartered: two Opus passes of the cross-hunk lane — the resume
re-ran it rather than replaying its cache — returning 14 and 17 findings, and
seven subject lanes that Opus refused twice each at zero tokens and Sonnet then
ran, returning 14, one lane empty with a full account of its search. Forty-five
findings merge by hand into thirty-one distinct defects, every one in this
decision's own wording, and every one is repaired in the commit carrying this
erratum. Coverage of the seven subject lanes is fallback-grade; the two Opus
cross-hunk passes found the defects that mattered, and the lanes' fourteen
findings converge on them in nine cases and add six small ones.

**Two of the second pass's four byte-level grades are confirmed by hand, and
both fork what an updater may emit.**

- **§20.4's introducing clause routed every type into the table.** *"Whichever
  source governs, its flags carry these obligations"* read the registered layer
  record — MU = 1, PE = 1 in §7.3 — into the MU = 1 row, whose obligation is
  *"The updater MUST NOT modify the scope the record governs"*; taken that way,
  no updater could edit a layer and no compactor could compact a file that had
  one, while Appendix H said in the same commit that an updater validates
  *"every layer it modifies"*. The old introducing clause had scoped the table
  to a type the updater does not implement, and the table's rows still say
  *"unknown critical"* and *"unimplemented"*. The scope is restored in the
  terms the paragraph's three sources need: *"The table states what an updater
  owes a record it does not logically modify, read under whichever flags
  govern it. Its MU = 1 row reaches only a type the updater does not
  implement"*, so for an implemented type only the PE bit bites. The PE = 0
  row's licence is now source-neutral — *"whoever fixed PE = 0 for the record,
  the writer that stored it or the definition that governs it"*.
- **The coordinate limb reached a shrink on one reading and not the other, and
  the shorthand for the bar had stopped naming it.** §11.4's ordinals take the
  grid counts, which take the extents, and §3.1 bounds a coordinate by the
  extents, so a reader could hold that a shrink alters *"the coordinate §11.4
  assigns any value they decode to"* and refuse every shrink of a populated
  layer; and four restatements — the shrink permission's *"exactly where"*
  sentence among them — still tested *"what §14 fixes"*, a set the bar had
  outgrown, so a shrink combined with a re-tiling that preserves §14's
  quantities was permitted by one sentence and barred by the next. Both close
  on one statement of what a tile is: *"The tile is the prior generation's
  too: it is its grid position and, in a planar layer, its channel, whatever
  disk ordinal either generation assigns it, and its stored bytes lie where
  `[R-LIF-01]` leaves them"*. The geometry paragraph now says that the tile
  extents and the dimension order fix the coordinate *given its tile*, cites
  §11.4 — `[R-GEO-06]` closes the list that fixes ordinals — and closes with
  *"An extent's growth and shrink, below, are permitted: tile coordinates and
  in-tile positions turn on the tile extents alone (§11.4), so neither moves
  the coordinate a stored value denotes"*, in place of the exhaustive *"the
  geometry changes this step permits"*, which excluded a free re-declaration
  and a rename. The four restatement sites read *"what the §14 bar protects"*.

The second pass's other two byte-level grades and the scope-floor lane's one
are settled below the line: the exhaustive closer is cut, and §18.2's Note and
§21.6's row offering only the record and the whole file are swept to *"any
scope containing the record, the whole file included"* — a file exceeding a
guarantee is outside `[R-CNF-03]`'s duty under every reading, so no verdict
forked, and the three passages now agree.

**The bar's sentence is split**, on the maintainer's direction of 2026-09-04:
the subject clause ends at *"the coordinate §11.4 assigns any value they decode
to"*, and *"The quantities are these:"* opens a semicolon list with no dash in
it. The gloss is quantified over values, as the packed plane needs — *"every
value they carry denoting, at the same coordinate, what it denoted"* — and the
geometry paragraph says *"no other listed quantity moves"* where it had said no
listed quantity did, the coordinate being the listed quantity that does. §5.2's
partial-total sentence, which the round-31 repair had lengthened around a
parenthesis holding a dash inside a dash pair, is three sentences now.

**The ordinal bar's opening and ground**: *"One effect is barred beside the §14
bar"*, its ground naming the decoding and the coordinates as well as the bytes
an ordinal move leaves alone, and its occasions *"a geometry change and a
channel-declaration change this bar leaves permitted, wherever either moves an
entry"*, which the re-emission clause's parenthetical states the same way in
place of the circular *"a permitted change"*.

**The third cause of a partial total** is narrowed to the scope that stops the
walk: *"where the verifier declined a layer on resource grounds (`[R-ERR-04]`)
and so never enumerated its claimants"*, since *"a tile's or a document's decode
declined leaves the walk complete, that claimant being enumerated from its
index entry or extent slot"*; §9.7 says the same, and its untouched sentence
now reads *"A verifier that certifies decodes every stored tile"*, with the
declining verifier reporting the check unmade. `[R-ERR-04]`'s narrowest scopes
are no longer a closed three — *"or the file itself where the quantity is the
file's, as layers per file and dir_length are"* — and *"In every case"* replaces
an *"Either way"* that had counted two options after a third was added.

**The flags rule's five restatements**: §6.2's cell now reads *"0 from a
creator, carried forward unchanged by an updater or a compactor, a set bit
ignored"*, where *"0 when created under this text"* had contradicted the
compactor's carve-out; Appendix H's writer line carries that carve-out —
*"a compactor instead carrying its input's unknown ignore-lane bits forward and
setting no other"* — where its two new lines had given a compactor opposite
instructions.

**Unswept restatements**: `[R-CNT-14]`'s own gloss, *"a directory carrying no
layer record is a conforming generation, an empty directory included"*;
Appendix H's reader line, *"the sole resolved case"*; `[R-WRT-01]`, which now
says *"a violation latent in a structure they carry forward unmodified travels
with it, seen or unseen"* in the words step 2 borrows from it; §11.1's
Rationale, *"An extent's growth is permitted whether or not the layer stores a
tile"* with the proviso the permission carries; §13.3's Note keyed to *"its
entry_count, or which ordinal an entry sits at"*; shape (c)'s *"a padding
position or a pad bit"* in place of an *either* whose pair the new item had
displaced, and its drop clause noting *"a run the figure below does not draw"*.

**Register unchanged**: 120 conditions, 277 instances, 331 vectors; `tarn_check`
PASS; two propagation acknowledgements and eleven quotation acknowledgements,
each for a Decision sentence this erratum supersedes. The repair list of this
decision was ticked against its diff by the cross-hunk lane, hunk by hunk, all
twenty-five accounted for.
