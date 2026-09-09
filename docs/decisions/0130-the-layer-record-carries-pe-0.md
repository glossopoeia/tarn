# 0130. The layer record carries PE = 0: a commit MAY drop a layer

- Status: Accepted (resolves Q-A9 on the maintainer's direction of
  2026-09-09; supersedes ADR-0068 and withdraws ADR-0129's decision 2)
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
  loss, where ADR-0082 had it refuse (decision 3).

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
