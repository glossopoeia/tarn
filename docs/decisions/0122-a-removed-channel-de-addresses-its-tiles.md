# 0122. A removed channel de-addresses its tiles, as a shrink does

- Status: Accepted (resolves Q-B10)
- Date: 2026-09-03
- Covers: §20.3 step 4's de-addressing carve-out and its planar-ordinal
  paragraph; §11.1's Rationale
- Confirm: none

## Context

§20.3 step 4's §14 bar forbids a commit from altering what §14 fixes for any
tile the superseded generation stored. Its carve-out let a tile drop out of
the addressed set — *"(§11.2's grid count falls)"* — on the ground that a tile
the new state does not address carries no §14 obligation and its extent
becomes slack. The grid count is a per-dimension quantity, so that
parenthetical named an extent shrink and nothing else; removing a channel
from a planar layer de-addresses that channel's N tiles by a different
mechanism, and no sentence in the document said whether a commit may do it
where the superseded generation stored any of them. ADR-0113's third audit
flagged it, its refute phase recovered it from a downgrade, and the ledger
carried it as Q-B10, the last byte-level entry gating G3. A challenge
that the channel count is *geometry* and so already inside the carve-out
was raised twice and failed on `[R-GEO-01]`'s own words; that framing stands.

The construction is a planar layer with channels `a` and `b`, N = 2, all four
tiles stored; a commit removes `b` and touches nothing of `a`. Neither of
step 4's other bars reaches it — no declared type changes, and `a` stays
first, so no surviving stored tile's ordinal moves, as the step says in terms
of *"removing the last"*. Under the restrictive reading the §14 bar bars the
commit, `b`'s stored tiles decoding as nothing afterwards; under the extensive
reading the carve-out states a principle about de-addressing and the commit
is permitted, `b`'s two stored payloads becoming slack. The output is an
ordinary conforming appended file that only the second reading lets an
appender produce.

## Decision

**The carve-out covers any de-addressing.** Step 4 now reads: *"Dropping a
tile out of the addressed set — §11.2's grid count falling, or a channel
removed from a planar layer taking its N tiles with it — is not itself such
an alteration, a tile the new state does not address carrying no §14
obligation and its extent becoming slack however it was de-addressed"*. The
bar's own test is the effect on a stored tile's bytes or their decoding, and
a de-addressed tile is not decoded at all; the document already says of a
shrink that discarding data is the caller's operation and this specification
does not bar it, and there is no principled line between de-addressing by
shrinking an extent and de-addressing by removing a channel.

**The permission owes the stranding sentence, and now carries it.** The
planar-ordinal paragraph, which blessed the operation in passing with
*"removing the last, re-indexes nothing and moves no ordinal at all"*, goes on
to say what becomes of the removed channel's stored tiles: they carry no §14
obligation afterwards, their extents become slack that only compaction
reclaims, and the shrink paragraph's SHOULD to produce a new file instead
reaches a commit that would strand a large share of a layer's stored bytes
this way too. §11.1's Rationale, the only other statement of the principle,
names both mechanisms.

**What stays barred.** An interleaved layer's channel removal changes the
sample stride and every value's offset, which the bar names, so it remains a
new layer or a whole-file rewrite wherever the layer stores a tile. Removing
a planar channel that later channels follow moves those channels' ordinals,
which the planar-ordinal bar reaches wherever they store tiles. What this
decision permits is exactly the case the text already described as moving
nothing: removing a channel whose successors store nothing, the last channel
included.

## Consequences

**Q-B10 is resolved and no byte-level ledger entry gates G3.** Nothing moves
in the register, the corpus, or any reader: the output of a permitted removal
is a conforming file under both readings, and the bar binds a commit's
conduct.

**The cost is the one §20.4 names for a removed layer** — the stranded bytes
are paid for and never read until a compaction — and it is now stated where
the operation is, beside the recommendation that already governs a shrink.

## Alternatives rejected

- **Bar the removal wherever the channel had a stored tile.** Coherent, on
  §20.4's reasoning that stranding makes the operation cost what it appears
  to save; rejected because §20.4 bars layer removal on PE = 1's ground and
  only *explains* it by cost, because the same cost is already accepted for a
  shrink, and because it would qualify a sentence the step states without
  qualification.
- **Leave it to round 31.** Rejected: the round would read a sentence that
  blesses an operation the document elsewhere neither permits nor bars, which
  is the shape that has produced the next finding every time.

## Precedent

- **ADR-0113** and **ADR-0114**, which made the §14 bar's test the effect on a
  stored tile and named channel removal as an operation for the first time.
- **ADR-0068**, *no commit removes a layer*, whose stranding argument this
  decision carries over to a channel as an account of cost rather than a bar.
- **ADR-0120**, taken the same day on the same ground: where the document's
  caller has chosen the operation, the specification states its cost and
  does not bar it.

## Erratum, 2026-09-03 — the pre-round-31 audit

Four defects in this decision's wording, none byte-level, all repaired in the
commit carrying this erratum.

- **Channel removal was introduced inside shrink-framed sentences.** The
  carve-out in the shrink paragraph enumerated it as a way of dropping a tile
  out of the addressed set, and the paragraph goes on to say the ordinal bar
  *"does not reach a shrink"*; §11.1's Rationale did the same under *"a
  shrink"*. Two lanes found it: a reader taking channel removal as a species
  of shrink concludes the ordinal bar does not reach it, which is false for a
  non-last removal. Both places now say the removal *"is not one"* and that
  the other bar judges it on its own ground; the Rationale's list is a list
  again and its closing sentence says *"One commit"*.
- **The ordinal paragraph's new sentence dropped the *planar* qualifier its
  siblings carry**, and the untouched *"An interleaved layer is unaffected"*
  after it could be read over the removal; now *"Removing a planar channel"*,
  and the interleaved sentence names its bar and says a removal there *"is the
  §14 bar's subject"*.
- **The same sentence lacked the caveat both its siblings carry**, that
  de-addressing rescues nothing; it now carries it.
