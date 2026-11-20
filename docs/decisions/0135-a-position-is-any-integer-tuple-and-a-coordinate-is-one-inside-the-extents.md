# 0135. A position is any integer tuple, and a coordinate is one inside the extents

- Status: Accepted (resolves Q-I8, option (a), the maintainer's own
  suggestion, with the reading of *sample position* the driver proposed, on
  the maintainer's direction of 2026-11-20; drafted by the driver at the
  maintainer's request; the second decision against edition A since the
  readable edition opened, ported to it under ADR-0133 decision 1)
- Date: 2026-11-20
- Covers: §3.1's *dimension*, *position* (new) and *coordinate* entries;
  §3.2 `[R-MDL-01]`; §11.3 `[R-GEO-04]`; §14.2's Example; §14.5 `[R-SER-05]`
  and its Example; §19.4 `[R-RDR-04]`'s lead-in and step 1; §21.6's row on a
  request outside the extents
- Confirm: none. No requirement identifier, register row, vector or outcome
  changes, and no byte of the corpus moves.

## Context

Q-I8 (2026-11-19, the maintainer reading §19.4's lead-in in the readable
edition). §3.1 defined a coordinate as a *d*-tuple "with 0 ≤ xᵢ < Eᵢ", so no
coordinate lay outside the extents, and six passages used the word for a
tuple that did, or for a request that could name one: `[R-MDL-01]`'s
sentence on padding, `[R-GEO-04]`'s definition of a padding position,
§14.5's Example, §19.4's lead-in, its step 1, and §21.6's row. Read by the
definition, a point request named only a tuple inside the extents and step
1's test could not fail; read by step 1, it named any tuple. Neither reading
moved a byte, since step 1 and §21.6 say what a reader does with every tuple
a request names. But the bound is one the document leans on: ADR-0123
records that §3.1 bounds a coordinate by the extents, and §20.3 step 4 still
explains its bar by a stored tile's *"values' coordinates"*. The document
also had a wider word in use and undefined. A *sample position* was a slot
of the tiling grid whether inside the extents or not (§11.2's counts,
§11.3's padding positions), and §3.1 used the phrase in three entries. Three
options stood: a wider word for the tuple, with *coordinate* kept to the
extents; *coordinate* widened by dropping its bound; the text left as it
was.

## Decision

1. **Three nested words.** A **position** is *"a d-tuple of integers (x₀, …,
   x_{d−1}), in declared dimension order"*: any integers, so a request can
   name a position no tile covers. A layer's **sample positions** are *"the
   positions its tiles cover: its coordinates, and the padding positions of
   its edge tiles (§11.3)"*. A **coordinate** is *"a position with 0 ≤ xᵢ <
   Eᵢ for every dimension, identifying one sample of a layer with extents
   (E₀, …, E_{d−1})"*. §3.1 gains the entry *position*, which carries
   *sample position* with it, and states *coordinate* over a position; the
   bound on a coordinate is unchanged, and its quantifier is now written
   out.
2. **The six passages take the wider word.** `[R-MDL-01]`: sample positions
   that exist only as padding *"lie outside the layer's extents"*.
   `[R-GEO-04]`: padding positions are *"sample positions with xᵢ ≥ Eᵢ"*,
   still a condition that forms no product (ADR-0102). §14.5's Example: the
   edge tile *"covers sample positions 4–7 along both axes"*. §19.4's
   lead-in: a point request *"names a single position (§3.1)"*, and a region
   request names *"a rectangular range of positions"*. Step 1: *"a position
   outside the extents addresses nothing in the reference array"*. §21.6:
   *"A requested position lies outside the layer's extents"*.
3. **What the new entry reaches.** Three more sentences used a word the
   entry now fixes. §3.1's *dimension* entry glossed an extent as a count of
   sample positions along the axis, which would now count an edge tile's
   padding as well: an extent is *"the number of samples along the axis"*,
   and a tile extent stays a count of sample positions. `[R-GEO-04]` and
   `[R-SER-05]` each said that padding positions are serialized like any
   other position, a statement over every tuple; both now say *"like any
   other sample position"*. §19.4's lead-in counted what an interval holds
   in positions, and an interval of one dimension holds integers: *"a range
   whose every interval holds a single integer is a region request"*.
4. **One slip of the other kind.** §14.2's Example wrote "in-tile
   coordinates" for what §11.4 defines as the in-tile position. It reads
   *"The sample position at in-tile position (1, 2)"*.
5. **What stands.** Every use of *coordinate* for a tuple inside the
   extents: §3.1's *sample*, §3.2's reference array, §11.4's `[R-GEO-06]`,
   §18.4's `tarn.axes`, §20.3 step 4. *Tile coordinates* and *in-tile
   position* (§11.4) are terms of their own. "Position" without "sample" is
   left where the text says whose it is, a tile's positions and the
   positions an entry carries being that tile's sample positions, and where
   it is the ordinary word: a record's position in the sequence, a bit
   position, a disk-ordinal position.

## Consequences

No byte moves and no outcome changes. A point request for a position outside
the extents fails as a request, and a region request returns its
intersection with them, as before; what changes is that the sentences saying
so have a subject that can lie outside the extents. §3.1's *coordinate* now
holds at every use, and ADR-0123's ground stands with the bound. The terms
list grows from eighteen entries to nineteen, in both editions, and
ADR-0133's equivalence contract reads the new entry in each. The readable
edition takes the change as a listed edit naming this ADR, in its own
wording where it has reworded the paragraph. A comment in the corpus
definitions that named §21.6's row by the old word follows the row; no
vector, manifest entry or fixture changes.

## Alternatives rejected

- **Widen *coordinate*** (option (b)): §3.1 drops the bound and the six
  passages stand, at the price of re-reading every rule that leans on it,
  §3.2's reference array, `[R-GEO-06]` and §20.3 step 4's bar first, and
  ADR-0123's ground with them.
- **Leave the text** (option (c)): each loose use said "outside the extents"
  in so many words, and the cost was a defined term used against its
  definition under three rules.
- **One wider word.** Making *sample position* the word for every tuple
  fails on a request, which can name a tuple beyond the tiling grid, and on
  §11.2, whose P and N · P count the slots that tiles hold.

## Precedent

- **ADR-0123**: §3.1's bound on a coordinate decided a reading of §20.3 step
  4's bar.
- **ADR-0102**: `[R-GEO-04]`'s overhang condition forms no product; the
  padding definition keeps that form.
- **ADR-0134**: the first decision against A ported to B; this is the
  second.
- **ADR-0133** decision 1 and its erratum of 2026-10-14: a decision against
  A on `main`, ported to B as a listed edit.
