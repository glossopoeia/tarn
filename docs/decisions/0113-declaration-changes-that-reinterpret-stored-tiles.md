# 0113. A commit may not reinterpret a stored tile: the sample-type and disk-ordinal bars

- Status: Accepted (resolves Q-B6)
- Date: 2026-09-01
- Covers: §20.3 step 4's declaration-change bar; §21.7's account of unwitnessed
  obligations
- Confirm: none

## Context

Round 28's refute phase found `[R-WRT-04]`'s step 4 byte-level. The step requires
an appender to re-emit a layer's tile-index region with "every other entry
byte-identical at its **disk-ordinal position** (a geometry change renumbers
ordinals wherever `[R-GEO-06]` moves them)", and that parenthetical is the only
text in the document saying when ordinals renumber.

**Two readings, and the document supplied nothing to choose between them.**
`[R-GEO-06]` gives a planar tile the disk ordinal **c · N + s**, "where c is the
channel's index (§3.1)", and §3.1 fixes that index as "its 0-based position in
that order". So either a carried-forward entry belongs to a *named* channel and
moves when that channel's index moves — making the parenthetical under-inclusive
— or it belongs to the tile at (k div N, k mod N) and never moves without N, making
the parenthetical exact. **Every rule individuating a planar tile's channel does
so positionally** (`[R-GEO-06]`, `[R-SER-01]`, `[R-IDX-01]`, §19.4 step 2), and
**no rule ties a channel's identity across generations to its name**, so the
second reading needs no unstated premise and the first does.

The construction: a planar layer, E = 2, T = 1, N = 2, P = 1 — the grid covers the
extent exactly, so there is no padding position and `[R-SER-05]`, T4 and T5 are
vacuous — with channels `a` and `b` both uint8, so every tile's decoded size is
P·B = 1 whichever channel it is taken to carry. §20.3's bar permits a commit that
exchanges the two declarations under either reading. One reading permutes the
entries, re-emits the index region and writes `crc_of_crc_array` = `cb 83 76 80`;
the other appends no region and keeps `21 3e a9 bc`. **Both files conform, a
reader MUST accept both (`[R-CNF-03]`), and each reading bars the other's.** Every
figure was re-derived by hand from `[R-ENC-09]`'s parameters.

**The fork is narrower than it first looks, and that shaped the decision.** An
interleaved layer's disk ordinal is s, which no channel declaration enters, and a
channel-set change there moves the sample stride Q and every Fᶜ, so the existing
bar already reaches it. Within planar, a disk ordinal is c · N + s and **N is the
spatial-tile count: the channel count enters C · N but no individual ordinal.**
So appending a channel, or removing the last, moves nothing and the two readings
agree. The fork is exactly a *permutation* of channel indices on a layer that
stores a tile.

**Q-B6's other limb had the same shape and had not been graded.** The entry, open
since round 25, also asks whether the bar reaches a channel's declared **sample
type**. It does — but only where the element size moves with it, through the
decoded size and the sample byte offsets. A change between two types of equal
width (uint8 to int8; any two of the four-byte types) changes no stored byte and
no offset, and reinterprets every value those bytes carry.

## Decision

**Two bars are added to §20.3 step 4, on the same tense as the bar they sit
beside and with the same escape route — a new layer, or a whole-file rewrite
under a fresh `file_id`.**

**A commit MUST NOT change the declared sample type of any channel of a layer
that stores a tile in the generation this commit supersedes**, whatever the
layer's layout and whether or not the element size moves. The maintainer's
ground, and it is the better one: a type change without rewriting the data is a
silent reinterpretation, and **the caller should be made to decide what becomes
of the values the new type cannot carry** — a magnitude the narrower type cannot
hold, a negative the unsigned type cannot. That decision is expressed by writing
the tiles, which is a rewrite by definition.

**For a planar layer, a commit MUST NOT change the channel declarations in a way
that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the
generation this commit supersedes.** Reordering the channels, or inserting or
removing one other than after the last, is such a change; appending a channel, or
removing the last, is not, and the text now works the arithmetic rather than
asserting it.

**The renumbering parenthetical is left exactly as it was, and this is the point
of resolving it here rather than patching it.** With a permutation barred on any
layer that stores a tile, the only thing that can renumber the ordinals of
carried-forward entries *is* a geometry change — so the sentence round 28 found
ambiguous becomes true as written. A layer storing no tile may still be
re-declared freely, and its entries are all sentinels, so permuting them is a
no-op byte for byte.

**Neither bar is witnessed**, and §21.7 says so: the prior generation's channel
declarations are not recoverable from the file, so no check can know which ordinal
a stored tile used to occupy, or which type of the same width its channel used to
be declared. A width-changing type change stays witnessed by T3 or T14, as §21.7
already recorded.

## Consequences

**The register does not move**: 120 conditions, 275 instances, 329 vectors,
coverage 120/120 and 275/275, Appendix A byte-identical. Both bars constrain
writer conduct with no single-file witness, so they belong in §21.7's omitted set
rather than in §21.2–§21.5, exactly as step 4's original bar does.

**The insertion broke an anaphor, and `tarn_propagate` caught it.** §20.3's
growth, shrink and re-declaration paragraphs all pointed back at "the bar above",
and putting two more bars between them and their antecedent gave that phrase two
nearer referents — the shrink paragraph would have read as saying the *ordinal*
bar "is the whole of the test" for a shrink, which is plainly false. This is the
shape round 27 recorded as `wrt06-same-ground-antecedent`, reappearing in the
repair for it. The original bar is therefore **named** at its own statement — the
**§14 bar** — and every reference in those three paragraphs and in §21.7 now
points at it by that name. The shrink paragraph also says outright that the two
bars beside it govern declaration changes, which a shrink is not. One propagation
acknowledgement is recorded, for shared tense phrasing rather than restatement.

**What this costs a caller.** Reordering channels, or inserting one other than at
the end, on a populated planar layer is no longer an appender's operation; nor is
any sample-type change on a populated layer. Both become a new layer or a
whole-file rewrite. **The operations people actually perform are untouched** —
appending a channel, removing the last, growing an extent, superseding tiles,
re-declaring an empty layer for schema-first creation.

**What it buys.** The fork closes with no new concept. The rejected alternative
that preserved reordering as a cheap append required the document to fix a
channel's identity **across generations by name** — machinery the format uses
nowhere else — and then needed a further rule for the commit that renames and
reorders at once, where that identity relation is undefined precisely when it is
needed.

**Q-B6 closes on both limbs.** The entry has been open since round 25 with its
sample-type limb ungraded; round 28 graded the order limb byte-level and the
maintainer extended the same treatment to the type limb on the overflow ground.

## Alternatives rejected

- **Entries follow the named channel.** Preserves reordering as an append-only
  commit. Rejected: it introduces cross-generation identity by name, and leaves
  rename-and-reorder undefined.
- **Entries stay at their ordinal**, stated as the rule. Cheapest to write and
  closest to what the text literally says. Rejected: reordering `(r, g, b)` to
  `(b, g, r)` would then silently repoint every stored tile to a different
  channel, conforming throughout, with no tile written and — §21.7 confirms — no
  check able to see it.
- **Bar only the sample-type change, leaving the ordinal question open.** It is
  the byte-level one; leaving it open leaves G3 gated.
- **State the bar as a property rather than a list** (ADR-0095's move). Rejected
  for the reason Q-B7's option sweep recorded: a property closes a fork only
  where it is determinate, and a property over "declaration changes that
  reinterpret a stored tile" is silent on which of *name* or *position*
  individuates the entry — the very question at issue.

## Precedent

- ADR-0081's reading of this same passage: a declaration change that would
  reinterpret stored bytes is not an appender's operation but a new layer or a
  rewrite. Both bars are that rule applied where it had not reached.
- ADR-0106's limit on ADR-0095's property-over-list move, applied here to reject
  the property option.
