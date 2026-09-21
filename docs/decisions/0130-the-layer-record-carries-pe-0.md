# 0130. The layer record carries PE = 0: a commit MAY drop a layer

- Status: Accepted (resolves Q-A9 on the maintainer's direction of
  2026-09-09; supersedes ADR-0068 and withdraws ADR-0129's decision 2; the
  erratum's decisions E1 and E2 confirmed by the maintainer, on 2026-09-19
  and 2026-09-21)
- Date: 2026-09-09
- Covers: §7.3's registry table and `spec/registry.json`; Appendix C; §20.4's
  flags paragraph and its layer-removal paragraph; §20.3 step 4's tense
  sentence; §20.5's dropping case, its disposal sentence and its regeneration
  paragraph; §20.3's three-shapes Example; §23.1; Appendix H's updater entry;
  the conformance corpus's seed builder and five vector definitions
- Confirm: none. The maintainer directed the change on 2026-09-09 after
  reading ADR-0068's cost as a warning. One consequence is stated below so a
  superseding ADR can withdraw it alone: a rewriter that detects a violation
  in a layer while regenerating its region may drop the layer, reporting the
  loss, where ADR-0082 had it refuse (decision 3). The erratum of
  2026-09-19 took two decisions the pre-round-36 audit forced. E1, that a
  dropped layer goes whole, its sub-records with it, was confirmed by the
  maintainer on 2026-09-19, and E2, that a sub-record of an unimplemented
  type with MU = 1 blocks the drop, on 2026-09-21.

## Context

ADR-0068 made layer deletion no defined operation, on the ground that an
in-place removal strands the layer's stored tiles and tile-index region as
slack and *"would cost what it appears to save"*; both registered types
carried PE = 1, and a file without a layer was a creator's new file, which
keeps nothing the creator does not understand. ADR-0129 named a
layer-dropping rewrite and, because the table forbade the drop, had to make
that rewrite the table's one exception. The maintainer's reading is that
the stranding cost is a warning and not a bar: on object storage a
kilobyte commit that drops a layer beats rewriting gigabytes to reclaim it,
and an operator who wants the space back rewrites when it suits.

**Why PE = 0 needs MU = 0.** `[R-CNT-12]` forbids a writer to emit MU = 1
with PE = 0 and has a reader treat the combination as PE = 1, so the layer's
PE bit cannot fall alone. Carving registered types out of that rule would
falsify L46, whose condition names a layer record carrying the combination,
and move the register. Clearing MU costs nothing: every conforming reader
and updater implements the layer type (`[R-CNF-03]`), so the bit binds no
actor within format major 1, and the registry's fixed values are what
`[R-CNT-22]` holds a stored record to.

**What else moves with it.** Once a commit may drop a layer and add one
under its name in the same commit, §20.3 step 4's tense sentence, *"unstoring
or superseding every tile of a layer and re-declaring it is one operation,
and it is a rewrite"*, forbids in one clause what the next commit route
permits. The route was already open by unstoring every tile, renaming the
layer and adding a new one over the same bytes; the drop makes it clean. So
the bar's scope is stated: it binds the layer's identity, and a new layer is
new whatever bytes its entries address.

## Decision

**1. The layer record's registry-fixed flags are MU = 0, PE = 0**, in §7.3's
table, `spec/registry.json` and Appendix C. §20.4's flags paragraph reads
*"the layer record carries PE = 0 and is dropped under the table's last row,
the user-metadata record PE = 1 and never; implementing a record's type
confers understanding of it, and the permission to drop it is the bit's
alone"*. Its removal paragraph reads *"A commit MAY therefore drop a layer
record, and never removes a user-metadata record at either scope"*, states
the stranding cost, and adds the guidance step 4 already gives a shortening:
*"a writer SHOULD instead rewrite where a drop would strand a large share of
the file's stored bytes"*. §20.5's dropping case is *"a layer or another
record §20.4's table licenses dropping, which a commit does by omitting the
record and stranding what it addressed (§20.4) and a rewrite does reclaiming
it"*, and the table's exception is gone. Shape (c) in §20.3's Example, §23.1
and Appendix H's updater entry say the same. ADR-0068 is superseded and
ADR-0129's decision 2 withdrawn.

**2. The fixed-declaration bar binds a layer's identity.** Step 4's tense
sentence reads *"a layer that stored a tile keeps its declarations through
the commit that empties it. The bar binds the layer's identity and nothing
else: a commit MAY drop the layer (§20.4) and add a new one under its name
and other declarations, the new layer being new whatever bytes its entries
address within §5.2's partition, and what the bar removes is a
re-declaration carried as the same layer over the tiles it stored."*

**3. A rewriter meeting a violation in a layer may drop the layer.** §20.5's
disposal sentence names *"a layer with its index region and stored tiles"*
among the records a drop removes from the output, and its regeneration
paragraph reads *"`[R-WRT-06]` then leaves it two disposals, since it can
neither reproduce the entry nor invent a replacement: drop the layer, which
§20.4's table licenses and the rewriter reports, or refuse."* `[R-WRT-09]`'s
refusal on a failed check is untouched: a failed checksum still refuses the
rewrite outright.

**The corpus is rebuilt.** The seed builder writes the layer record's flags
as 0; TV-0305 and TV-0009 set a reserved bit over 0/0 so that L47 alone
fires; TV-0956 sets PE alone and TV-0306 both bits, so that L49's two
layer-record instances fire without L46; TV-0951 keeps MU = 1 with PE = 0,
which is L46 and L49 together as before; the nested-layer seed for L26
carries 0/0. Every vector with a layer record changes in two bytes and its
covering checksums.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors;
L46 and L49 keep their conditions and instances, and the corpus rebuilds
them. **The format moves by two bytes in every layer record**: a file
written under ADR-0068's registry carries a layer record whose stored flags
differ from the registry, which is L49 under this text. No file outside
the corpus was written under the old registry.

**What a caller gains**: a layer removed by one commit, its name free, its
bytes stranded until a rewrite; the tool reports the loss and the document
warns of the cost. **What a reader loses**: nothing; no reader behaviour
changes. **What a rewriter gains**: a disposal short of refusal for a layer
whose region it cannot regenerate, at the price of reporting it.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: every site named above is in the diff, sixteen edits over
the specification, the registry, the ledger and two ADR headers, and the
corpus rebuilt behind `tarn_check`'s coverage checks.

## Alternatives rejected

- **Keep MU = 1 and carve registered types out of the MU = 1 with PE = 0
  rule.** Rejected: L46's condition names the layer record carrying that
  combination and would be false; the register would move for a bit that
  binds no actor.
- **Keep PE = 1 and ADR-0129's exception.** Rejected on the maintainer's
  reading: the exception existed only to route around a bar whose reason
  was a warning.
- **Keep refusal mandatory for a rewriter meeting a violation in a
  droppable layer.** Rejected: §20.5's own rule is that dropping answers
  wherever the table licenses it, and the loss is reported. Stated here so
  the maintainer can withdraw decision 3 alone.

## Precedent

- **ADR-0068**: superseded; its cost argument survives as §20.4's warning.
- **ADR-0061** and **ADR-0120**: the preservation table governs every
  record type, and the licence to drop is the bit's own.
- **ADR-0082**: the regenerating rewriter answers for what it meets; this
  ADR adds a disposal.
- **ADR-0129**: obligations attach to operations, and a layer drop is one.
- **ADR-0124**: the closed list and the principle beside it; decision 2
  states that principle's scope.
- **ADR-0119**: the repair list against the diff.

## Erratum, 2026-09-19 — the pre-round-36 audit

Nine lanes read the 49 hunks of `f987777..4151e57`, the commits of ADR-0128,
ADR-0129 and this decision as one combined diff: seven subject lanes on
Sonnet from the start, and two cross-hunk passes started on Opus, one grouped
by rule and one by operation. **Opus refused both passes at zero tokens, at
launch and on the unchanged resume**, the first audit in which the cross-hunk
brief was refused outright, and both ran on Sonnet after their calls were
changed. So every lane of this audit is fallback-grade, no Opus reading of
this surface exists, and the hand-check carries more of the verdict than in
any audit since the model policy was set. The nine returned 44 findings: 5,
5, 8, 8, 4, 0 and 4 from the lanes, the register lane empty with a full
account of its sweeps, and 4 and 6 from the passes. They merge by hand into
twenty-nine distinct defects, nine in this decision's wording, sixteen in
ADR-0129's and four in ADR-0128's. Each ADR's erratum records its own;
twenty-five are repaired and four declined in the commit carrying the three.

**Two are byte-level by the hand-check, both are this decision's, and one
lane of nine saw them.** The drop lane asked what becomes of a dropped
layer's sub-records, and no sentence answered. §20.4 said in one breath that
a commit MAY drop a layer record and "never removes a user-metadata record at
either scope", while a layer record carries its sub-records in its own
inline payload (§7.4) and a user-metadata sub-record carries PE = 1. Under
one reading the drop takes the sub-record with it and the *never* is false;
under the other the PE = 1 row's *Retain byte-identical* pins every layer
that carries user metadata, and no commit and no rewrite could ever drop
one. The table's MU = 1 row forks the same way over a sub-record of a type
the updater does not implement: its bar on modifying the layer either
reaches the drop or does not. The disputed file, the input less the layer,
is conforming under both readings of both, and one reading of each lets an
updater emit it, which is the byte-level test. Neither this ADR nor ADR-0129
mentions a sub-record, and neither cross-hunk pass raised either.

**Decision E1. A dropped layer goes whole.** A sub-record's flags govern it
within a layer the updater keeps; a layer dropped under its own PE = 0 takes
its sub-records and their extents with it, whatever their PE bits. The
ground is this decision's purpose, a layer removed by one commit, which the
other reading withholds from every layer carrying user metadata, by commit
and by rewrite alike; and containment, a sub-record being bytes of the layer
record's payload, and layer-scoped state having no scope to persist in
without its layer. §20.4 reads *"the drop takes the layer whole: a
sub-record's flags govern it within a layer the updater keeps, so a dropped
layer's sub-records and their extents go with it whatever their PE bits"*
and *"A commit never removes a user-metadata record from a scope it keeps"*;
its flags paragraph reads *"the user-metadata record PE = 1 and is dropped
only with a layer that carries it"*; §20.5's disposal sentence names *"a
layer with its sub-records, its index region and stored tiles"*; Appendix H
says the same. **Confirmed by the maintainer on 2026-09-19.** The
alternative, that a PE = 1 sub-record pins its layer, stays stated so a
superseding ADR can choose it: the drop paragraph
would say so, and a caller would have no way to make such a layer
droppable, PE = 1 forbidding the sub-record's removal first.

**Decision E2. A sub-record of a type the updater does not implement with
MU = 1 blocks the drop.** The ground is the MU = 1 row's own words, *"The
updater MUST NOT modify the scope the record governs"*, removing a scope
being the limiting case of modifying it, and `[R-CNT-12]`'s gloss on why
MU = 1 with PE = 0 is read as PE = 1, *"never silently deletable"*: a tool
that cannot read a critical record does not delete it by deleting its
container. The row reads *"blocks modification of that layer, its drop
included"*, the drop paragraph names the one blocking sub-record, and
Appendix H reads *"never modifies or drops a scope governed by an unknown
critical record"*. A rewriter already refuses such a file whole
(`[R-WRT-06]`). **Confirmed by the maintainer on 2026-09-21**, who chose the
blocking reading over the alternative, that the layer record's own PE = 0
licenses the drop whatever the layer carries; the alternative stays stated
so a superseding ADR can choose it. The maintainer asked with it that the
coupling of the two bits be surfaced, PE having become a choice within
MU = 0: §7.2 gains a Note under `[R-CNT-12]`, *"The two flag bits are not
orthogonal"*, which names the three states the rule leaves a record as
§20.4's three rows and adds no rule.

**The scope sentence.** Decision 2's sentence said the bar binds "the
layer's identity", a property the document nowhere defines and no byte
carries, and cited §5.2's partition as though it warranted the new layer's
newness, which a rule about byte ownership does not. It reads *"The bar
binds a layer the commit keeps and nothing else"* and *"§5.2's partition
being over the new state alone"*. The step lane and the by-rule pass both
observed that a drop and addition over the dropped layer's own extents
yields, byte for byte, the directory a barred re-declaration would; the lane
graded it byte-level and the pass did not. **Not byte-level by the
hand-check**: decision 2 says *whatever bytes its entries address* in terms,
so the text has one reading, the file is emittable under it, and the bar
binds conduct. The sentence now says so: *"no byte tells the two apart,
which is the sense in which the bar binds the commit as an actor and makes
no file nonconforming"*. What that leaves with the maintainer: the principle
paragraph beside the bar still gives as its reason that under new
declarations the same bytes would denote values the writer did not store,
which is what the permitted route does. Whether a new layer's entries should
be held to bytes its own commit wrote is a decision, and this erratum does
not take it.

**Sentences written on the old registry value.** §7.2 gave the layer
record's tile index as its example of an MU = 1 record carrying further
references, two sentences after ruling that an MU = 0 record's extent
contents encode no offsets; with the layer record at MU = 0 the rule was
false of the specification's own record type, in normative text (the rewrite
lane and the by-operation pass). It reads *"The layer record is the one
exception, and this specification's own"*, on this decision's ground that
every conforming reader and updater implements the type (`[R-CNF-03]`).
§7.4's worked Example still stated MU = 1, PE = 1 beside a citation of §7.3
(three lanes).

**The report's keyword.** The table says an updater that drops a record
SHOULD report the loss. This decision's three restatements said "reports the
loss as the table requires", "the rewriter reports", and, in Appendix H's
list of duties, a flat "reporting the loss". All three carry the table's
SHOULD, Appendix H as an advisory sentence on its own convention. The
Consequences above say a rewriter's drop comes at the price of reporting it;
if that is meant as an obligation it is a MUST the table does not carry, and
a decision.

**Declined.** The step lane's B-05, that the bar's give-up sentence reads as
a closed two-way choice until the scope sentence five sentences on: the
paragraph states the third route, and a forward pointer would be one more
rewording of a sentence no reading of which is wrong.

**Register unchanged**: 120 conditions, 277 instances, 331 vectors;
`tarn_check` PASS; seven quotation and nine propagation acknowledgements.
The repair list of the three errata was ticked against the diff: twenty-seven edits over twenty-five defects, four declined, none
deferred.

## Erratum, 2026-09-21 — the scoped second audit

The erratum of 2026-09-19 took two decisions and made twenty-five other
edits, the maintainer's rulings added §7.2's Note and ADR-0129's E3, and no
audit had read any of it: `tarn_chain` hands a repair committed before a
charter to the round, a convention built for wording repairs and not for
decisions. On the maintainer's go-ahead a scoped audit read
`4151e57..cfa1073`, 26 hunks: two subject lanes on Sonnet over the fifteen
hunks that carry decisions, the drop and the positions, and two cross-hunk
passes over all 26. **Opus refused both passes at zero tokens, at launch and
on an unchanged retry**, as it had in the first audit, and both ran on
Sonnet; every lane is again fallback-grade. The four returned 7, 4, 3 and 4:
eighteen findings, twelve distinct defects, **none byte-level by any lane or
by the hand-check**. E1, E2 and ADR-0129's E3 drew no finding against what
they decide: the by-operation pass carried a drop through every kind of
sub-record a layer can hold, and four writers through the two positions to
the trailer's bytes, and found each decided. Seven of the twelve are this
decision's, all in the erratum's own wording or in sentences it should have
swept, and all are repaired in the commit carrying this erratum.

**The erratum's own overclaim.** Step 4's scope sentence had gained *no byte
tells the two apart* as the sense in which the bar binds the commit as an
actor. E1 falsifies it: a commit never removes a user-metadata sub-record
from a layer it keeps, so a layer that carried one and carries none under
the same name was dropped and added, and a byte says so. The paragraph above
already gives the true reason, that the bar states no condition a file can
exhibit, and the added clause is cut; the sentence ends *"What the bar
removes is a re-declaration carried as the same layer over the tiles it
stored."*

**What a dropped layer strands, swept.** §20.4 says a dropped layer strands
its tiles, its index region and its sub-records' extents; shape (c) of
§20.3's Example named the first two (three lanes) and §23.1 the first alone
(two lanes), and §23.1 is the privacy section, where a layer's user-metadata
document is the thing to name. They read *"a dropped layer's tiles, index
region and sub-records' extents included"* and *"strands every tile it
stored, its tile-index region and its sub-records' extents, a layer's
user-metadata document among them"*.

**Below the line.** The flags paragraph spoke of "the user-metadata record"
being dropped only with a layer that carries it, one clause for a record
that occurs at two scopes (two lanes): *"a top-level one never dropped and a
sub-record only with the layer that carries it"*. §7.2 cited `[R-CNF-03]`
for a claim about an updater that rests on `[R-CNF-11]`'s inheritance; it
cites both. Appendix H's *drops a scope governed by an unknown critical
record* did not read at file scope, where the next clause governs: *"a layer
that carries an unknown critical sub-record"*. Its advisory sentence on the
report followed the rewriter's list and says *"of an appender and a rewriter
alike"*.

**Register unchanged**: 120 conditions, 277 instances, 331 vectors;
`tarn_check` PASS. The repair list of the three errata of this date was
ticked against the diff: eleven edits over eleven defects, one declined,
none deferred.
