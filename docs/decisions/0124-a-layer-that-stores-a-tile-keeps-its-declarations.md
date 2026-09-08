# 0124. A layer that stores a tile keeps its declarations

- Status: Accepted (supersedes ADR-0113's disk-ordinal bar, ADR-0114's gloss,
  ADR-0122, and ADR-0123's decision 1 in the form it landed; Q-B6 and Q-B10's
  operations become rewrites; Q-B8's premise is settled)
- Date: 2026-09-08
- Covers: §20.3 step 4 whole; §11.1's Rationale; §13.3's sparse-writing Note;
  §20.3's three-shapes Example; §23.1 `[R-PRV-01]`; Appendix H's updater entry
- Confirm: none

## Context

§20.3 step 4 governed what a commit may change in the declarations of a layer
that already stores tiles by stating a bar on effects — the §14 bar, over
everything §14 fixes for a stored tile and, since ADR-0123, the coordinate its
values denote — a second bar on a planar layer's disk ordinals, and a set of
carve-outs and permissions around them: growth as an express exception, a
shrink permitted exactly where it altered nothing the bar protected, a channel
removal judged under both bars, a filter change permitted where the shuffle
was the identity, a fill change permitted where no stored tile carried padding
for it, and a re-type permitted where no stored tile carried the channel. That
passage produced the byte-level finding of rounds 10, 14, 16, 17, 25, 27, 28,
29, 30 and 31, the ledger entries Q-B6 and Q-B10, and the two byte-level
defects of the pre-round-32 audit — both in the repairs the round before it had
made to the same step. Every one turned on whether a particular change to a
particular file fell inside or outside a carve-out.

**The maintainer put the design question**, on 2026-09-08, after the audit:
what edits are actually open on a committed layer, and are they useful enough
to carry the machinery that permits them? The answer the document gave was
that the operations the append model exists for — superseding, storing and
unstoring tiles, growing extents, adding layers and records, amending metadata
— are open and cheap, while every change to a populated layer's schema was a
rewrite in any case; the carve-outs bought a shrink in place, a fill change on a
tile-aligned layer, an identity filter change and a planar channel removed from
the end, at the cost of the passage above. The maintainer's direction: do not
constrict writers and updaters without an architectural or logical reason, but
stop enumerating carve-outs, and guide writers to a path on which the edge
cases do not arise, for predictability's sake when modifying an existing file.

## Decision

**A layer that stores a tile in the generation a commit supersedes keeps its
declarations, with a closed list of exceptions and no other.** Step 4 now
states the list in terms: *"its name, and its dimension and channel names, MAY
change; an extent MAY grow; a planar layer's channel list MAY be extended at
its end, or shortened from its end; and a slab or alignment declaration is
re-established or cleared as this step provides below"*. Every other
declaration is fixed for as long as the layer stores a tile — *"the layout, the
linearization and the index encoding, the codec and the filter, the rank and
the dimension order, every tile extent, every channel's type and fill, an
interleaved layer's channel list, and the position of every planar channel but
the last"* — and *"A commit MUST NOT change one of these; the change is a new
layer, or a whole-file rewrite under a fresh file_id"*. The two lists partition
§7.4's field list, the derived fields aside. The tense clause stands, so
emptying a layer as it is re-declared is a rewrite, and an empty layer is
re-declared freely as before.

**The principle is stated beside the list, so the list is not arbitrary and
can be checked against it.** *"The line is drawn where a stored tile's meaning
is fixed"*: the fixed declarations are the ones §14 reads a stored tile under
and the ones §11.4 assigns its ordinal and coordinates by, and the permitted
changes touch none of that — a name enters no map, a grown extent adds
positions that held fill, an appended channel adds tiles after every existing
ordinal, a channel removed from the end takes only its own tiles out of the
addressed set. What the line gives up is stated rather than carved around:
*"a shrink, a fill change, a re-type, a re-tiling, a change of layout, codec or
filter, and a channel inserted or removed anywhere but the end are rewrites
even where a particular file would survive them in place, because deciding
which files would is the edge this list exists to remove"*.

**The §14 bar, the disk-ordinal bar, the sample-type paragraph, the geometry
paragraph, the shrink paragraph and every carve-out are withdrawn**, their
work done by the list. The re-emission clause's renumbering occasion is one —
*"a growth renumbers ordinals wherever `[R-GEO-06]` moves them, and nothing
else this step permits moves one"* — because nothing else the step permits
moves a stored tile's ordinal. §11.1's Rationale, §13.3's Note, the
three-shapes Example, §23.1 and Appendix H restate the list and nothing else.

## Consequences

**What is given up.** A shrink in place, a fill change on a populated layer, a
filter change whose shuffle happens to be the identity, and a planar channel
inserted or removed anywhere but the end, each of which the document had
permitted for some files and barred for others by a test on that file. Each is
a new layer or a whole-file rewrite now, whatever the file. Unstoring tiles
remains the way to discard data in place, and a channel removed from the end
strands its tiles as slack exactly as before.

**What is kept.** Everything the append model is for: superseding, storing and
unstoring tiles; growing extents, including declare-then-fill from a zero
extent; appending a planar channel; adding layers and records; amending
metadata; renaming; clearing or re-establishing slab and alignment
declarations; re-declaring an empty layer. The slack model is unchanged, and so
is the cost the §20.3 Note states: a commit re-emits the whole index region of
every layer whose stored-tile set or entry_count it changes.

**The register does not move**: 120 conditions, 277 instances, 331 vectors.
The rule binds a commit's conduct and has no single-file witness, as the bars
it replaces had none; §21.7 is unchanged. No reader behaviour changes.

**Q-B8's premise is settled.** §13.3's Note may key re-emission to entry_count
because, under the changes the step now permits a populated layer, entry_count
is the only way its index content moves: a growth that changes any grid count
changes the product unless the product is already zero, and no permitted change
moves an ordinal otherwise.

**ADR-0113, ADR-0114 and ADR-0122 are superseded** — the disk-ordinal bar,
the §14 bar's type gloss and the channel-removal carve-out are subsumed by the
list — and ADR-0123's decision 1 is superseded in the form it landed: its
principle, that the tile extents and dimension order fix the coordinate a
stored value denotes, is the reason those declarations are on the fixed list.
ADR-0081's reading of the step stands as the whole rule.

**Round 32 reads this decision.** Its charter over `72c41e1..HEAD` covers the
audit's repairs and these edits together; the audit chain names both until
then.

## Alternatives rejected

- **Keep the bars and their carve-outs, repaired again.** Rejected on ADR-0106's
  rule and the record above: the passage has been false in twelve rounds and
  in the audit of its own last repair.
- **Freeze every declaration of a populated layer, extents included.** Rejected:
  growth is what declare-then-fill and time-series appends need, and it
  reinterprets nothing, a grown position having held its channel's fill.
- **Keep a shrink to a tile-aligned extent, or a fill change where no stored
  tile carries padding.** Each is correct for the files it names and is a
  carve-out with a per-file test, which is the shape being removed.
- **State the principle alone and no list.** Rejected on ADR-0106's limit: a
  property closes a fork only where it is determinate, and this passage's
  history is of properties read two ways. The list is the rule; the principle
  explains it and lets a reader check it.

## Precedent

- **ADR-0081**: a declaration change that would reinterpret stored bytes is
  not an appender's operation but a new layer or a rewrite.
- **ADR-0106**: a passage false repeatedly is replaced, not repaired again.
- **ADR-0120**: where the document's caller has chosen the operation, the
  specification states its cost and does not carve around it; and the
  maintainer's question is what a rule is for.
- **ADR-0068**: no commit removes a layer, whose stranding argument this
  decision carries to the operations it now sends to a rewrite.
