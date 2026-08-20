# 0076. The instance criterion applied in one direction

- Status: Accepted
- Date: 2026-08-19
- Covers: §21.1's instance arithmetic as applied; cells T14, F7, L41,
  L44, T21, T22; register totals; sixteen new vectors
- Confirm: none

## Context

Cleanroom round 12 found §21.1's instance criterion applied in
opposite directions to conditions of the same shape, and deferred the
fix. T3 enumerates six instances — three decoded-size formulas
(interleaved P·Q, planar numeric P·Bᶜ, packed planar bool ⌈P/8⌉),
each in both directions — while T14, the same equality read from the
index entry under codec 1, counted one. F33 enumerates five claimant
families for a cross-scope overlap, and L18 three for the intra-layer
case, while F7 — a placement test over the same families — counted
one.

The sweep preceding the fix found the class is larger than the two
rows the round named. L41's own condition text names three
alternatives — *gap, overlap, or out-of-ordinal placement* — against
a cell that counted one; its vector module had already recorded the
discrepancy in a comment. And T21, T22, and L44 each compare a frame
field or a bound against the same decoded-size formula family that T3
enumerates.

Two directions were available: enumerate the under-counted cells up,
consistent with T3, F33, L18, L47 and the R-rows' container axis; or
state a narrower criterion — instances only where the condition text
names alternatives — and collapse the enumerated cells. The second is
cheaper (no new vectors) but weakens what the register demands of the
corpus: the Instances column is the corpus build list, and a register
that demands one T3 file where six materially different shapes exist
certifies less than G5 claims.

## Decision

Enumerate up, in one direction, under the criterion §21.1 already
states: a row whose check ranges over a family whose members give the
condition materially different shapes enumerates them.

- **T14** — 6 instances: the three decoded-size formulas × entry
  length longer/shorter. Under codec 1 the entry's length is the
  stored payload's length, so T14 takes T3's direction axis with it.
- **F7** — 4 instances: stored-tile extents, tile-index regions,
  record extents, sub-record extents. The live directory bounds the
  gap and the live trailer ends it, so neither can occupy it, which
  is why F7 counts four families where F33 counts five.
- **L41** — 3 instances: gap, overlap, out-of-ordinal placement — the
  alternatives its condition text has named all along.
- **L44, T21, T22** — 3 instances each: the three decoded-size
  formulas. No direction axis: their subject is a declared frame
  field or a fixed bound against the derived size, where longer and
  shorter do not change the check's shape — unlike T3 and T14, whose
  subject is the payload's own length.

Register totals move from 121 conditions over 248 instances to **121
conditions over 264 instances**; the corpus from 300 to **316
vectors**. `COV-05` fails on any instance without a vector, so the
cells and the sixteen files land in one commit.

## Consequences

Sixteen vectors, none requiring new checking machinery:

- T14 ×5 on seed `pair`, TV-0419's construction with the other
  formula and direction combinations — declaration patches, codec 1
  throughout. Each nominally also satisfies T3's predicate, as
  TV-0419 always has; §19.2's order detects at the entry, which is
  T14's subject, and ADR-0056 already retired the reverse claim.
- F7 ×3 as self-contained seeds: the structure is placed in the
  pre-trailer pad — slack, whose content is unconstrained — and the
  owning slot repointed, so every checksum verifies over exactly the
  shipped bytes. The tile-index variant writes a verbatim copy of the
  region into the pad; the record and sub-record variants use an
  unregistered experimental type, whose extent §8.1 covers with no
  checksum.
- L41 ×2 on seed `slabrun`: *gap* by unstoring the run's middle tile
  (sentinels are transparent, so the run's stored neighbours now
  straddle four unclaimed bytes); *overlap* by pointing ordinal 2 at
  ordinal 1's identical payload, which inherently co-satisfies L18's
  intra-layer overlap — noted at the vector, outcomes agreeing, the
  T17/T18 precedent.
- L44 ×2 and T21/T22 ×2 each: TV-0301's and TV-0718/0719's
  constructions re-run under planar and packed-bool geometry.

Existing vectors TV-0419, TV-0119, TV-0912, TV-0301, TV-0718 and
TV-0719 are re-annotated from `—` to the instance each has exhibited
all along.

The direction judgment — which rows carry longer/shorter — is stated
in the Decision and is now the precedent for future rows: the
direction axis belongs to rows whose subject is a measured length,
not to rows whose subject is a declared field compared against one.

## Precedent

- ADR-0049, which recounted the register against its own counting
  rule and set the T3/F33 cells this decision completes.
- ADR-0064, which made the instance's verbatim cell text the corpus
  key — why re-annotation is a vector edit, not a manifest edit.
- ADR-0056, which retired the codec-1 T3 claims and fixed the
  detection-order reading this decision's T14 vectors rely on.
