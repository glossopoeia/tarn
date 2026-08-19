# 0074. A stored tile freezes the declarations it depends on

- Status: Accepted
- Date: 2026-08-18
- Covers: declaration changes that invalidate stored tiles; §20.3 step 4;
  §11.1's growth rationale
- Confirm: reverses the fill obligation landed hours earlier in the same round

## Context

Cleanroom round 12 found that a commit shrinking a dimension extent silently
breaks its own file. Extents (8, 8) with tile extents (4, 4) give grid counts
(2, 2). Shrink `E_x` to 7 and `⌈7/4⌉` is still 2: `entry_count` is unchanged,
the stored-tile set is unchanged, the index content is unchanged, so §20.3
step 4 forces no re-emission. But column x = 7 has become a padding column,
and `[R-SER-05]` fixes every padding position's content to the channel's fill.
Two untouched edge tiles are now T4 violations, in a file a conforming
appender just produced.

Investigating it turned up two larger facts.

**Fill was one of ten.** The same hole reaches a changed tile extent, channel
type, channel set, layout, linearization, codec and filter — every declaration
a stored tile's bytes depend on. The document answered exactly one of them,
and only since earlier the same day, when the round-9 repair was moved out of
a non-normative Example into step 4.

**The document only ever names growth.** §20.1's appender does "adding layers
or records, superseding tiles, *growing* extents"; §11.1's rationale says
"*grow* extents as data arrives"; step 4 says "added tiles, *grown* extents".
The words *shrink* and *shrunk* appear nowhere. That is silence, not a
decision — and the asymmetry behind it is provable. Growing an extent turns
padding positions into real ones, and those held fill, which is a legal sample
value, so the tile stays conforming. Shrinking turns real positions into
padding, where `[R-SER-05]` now demands fill the bytes do not carry.

## Decision

**A commit MUST NOT change a layer's declarations in a way that alters, for
any tile that layer stores, what §14 fixes for its stored bytes or how they
decode** — the set of padding positions and the content `[R-SER-05]` fixes
there, the decoded size, the byte offset of any sample within the decoded tile
image, or the codec and filter that produced the stored bytes. Such a change
is a new layer, or a whole-file rewrite under a fresh `file_id`.

Two permissions are stated with it, because they are the cases that matter and
the prohibition would otherwise read wider than intended. **A layer that
stores no tile may be re-declared freely** — which is exactly what
schema-first creation needs, and leaves the declare-then-grow workflow §11.1
describes completely untouched. **An extent may always grow**, for the reason
above.

The alternative was to permit the change and oblige the commit to re-emit
every tile it invalidates, generalising the fill rule rather than replacing
it. It was rejected on the ground ADR-0068 already settled for layer deletion:
**`[R-LIF-01]` freezes committed bytes where they lie**, so re-emitting a
layer's tiles strands the originals as slack — the whole layer's worth,
reclaimed only by compaction. An operation named "shrink an extent" or "change
a channel's fill" would read like a directory edit and deliver a file larger
than it started, and the rewrite the user would then perform is the one the
obligation performed anyway, only unasked. A cost discovered is worse than a
cost chosen.

Workload supports it. The natural operation is *adding* a decimated layer, not
mutating an existing one — that is shape (a), and nothing existing is
rewritten. Cropping is naturally a new file. A wrongly declared channel type is
a rewrite in any tool. The one plausible casualty is correcting an
over-declared extent after a short acquisition, and declare-then-grow already
answers that: leave the extent and accept a fill-valued tail, which is what
fill means.

## Consequences

This **reverses the fill obligation landed hours earlier in this same round**,
which permitted a fill change on a padded layer at the price of re-emitting
its tiles. Under this ADR that change is not an appender's operation. The
reversal is defensible on its own terms — `fill` defines what *unstored* tiles
read as, so changing it retroactively rewrites the meaning of every unstored
tile as well as the padding of every stored one — but it is a reversal inside
one round, and worth naming as such rather than presenting as refinement.

Stated once and generally, in terms of what a change does to a stored tile,
rather than as a list of declarations. §21.9's hard-limit list has been found
short twice; enumerated lists in this document drift.

Register and corpus unchanged: 121 conditions over 248 instances, 300 vectors.
The rule bars a writer's operation and names no new file condition, so it takes
no register row — `[R-CNF-02]`'s conduct-versus-predicate split, the same
footing §20.3's other appender obligations sit on.

Priced knowingly. A producer who over-declares an extent and finishes early
carries a fill-valued tail or rewrites the file; there is no third option, and
the second costs a full copy. §11.1's rationale now says so where the workflow
is described, rather than leaving it to be discovered in §20.3.

## Precedent

- ADR-0068, whose reasoning this extends verbatim: an in-place operation that
  strands the bytes it replaces "would cost what it appears to save".
- `[R-LIF-01]`'s append-only model, which is what makes re-emission expensive
  rather than merely inconvenient.
- ADR-0072's line that a rule whose trigger cannot produce its outcome is not
  a rule — here, a permission whose price is a hidden full-layer rewrite is not
  a permission worth having.
