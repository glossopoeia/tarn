# 0086. §21.9's per-instance rows range over instances, not declarations

- Status: Accepted (resolves round 21's unanimous byte-level finding)
- Date: 2026-08-21
- Covers: §21.9's limits table quantifier; `[R-ERR-03]`/`[R-ERR-04]`
- Confirm: none

## Context

Round 21's writer walk built a schema-first layer — dimension extent 0, tile
extent 2³¹, one uint8 channel, interleaved — and asked whether §21.9's *decoded
size of one tile* row reaches it. **All three triage passes graded it
byte-level independently.**

The mechanics: §3.1 defines a tile as "the unit a tile-index entry addresses",
and §11.1 says "A dimension with extent 0 is valid: its grid count is 0, the
layer has zero addressed tiles, its tile index has zero entries." So the layer
addresses **no tile** — while its declaration-derived decoded size is
P·Q = 2³¹ = 2048 MiB, eight times the row's 256 MiB guarantee, a quantity §19.3
obliges a reader to derive at layer access anyway.

`[R-ERR-04]`'s two halves then point opposite ways:

- its **licence** is declaration-based — "at the narrowest scope whose
  **declarations** exceed what it can serve";
- its **bar** is quantity-based — "Software that declines on that ground a file
  whose every **quantity** lies within the table is not a conforming reader."

If no tile exists, no such quantity exists, nothing exceeds, and the bar makes
the declining reader nonconforming. If declarations govern, the licence covers
it. Same file, opposite answers to whether the reader conforms.

## Decision

**The table's last three rows are per-instance and range over instances the
file actually contains.** A file containing none of a kind does not exceed that
row, whatever its declarations would derive. The first five rows range over
declarations, which every file and every layer carries.

The split is not arbitrary. Rows 1–5 — rank, channel count, `entry_count`,
layer count, `dir_length` — are properties every file and layer has, `entry_count`
included, which is 0 for an empty layer rather than absent. Rows 6–8 — a tile's
decoded size, a user-metadata document's decoded size, a zstd frame's
`Window_Size` — presuppose a structure the file may simply not contain.

**The document had already made this choice once and said so.** `[R-COD-07]`'s
lz4 cap is written "for a layer any of whose **addressed tiles'** decoded size
exceeds 0x7E000000", and §20.3 remarks that an empty layer "escapes only
because that cap is quantified over addressed tiles". Round 21's finding is
that same choice left unmade for the limits table; making it here aligns the two
rather than inventing a rule.

**It costs nothing operationally.** A reader asked to accept a layer declaring a
2048 MiB tile size that addresses no tile allocates nothing, because there is no
tile to read. And it defers rather than traps: if a later commit stores a tile
in that layer, the instance exists, the row bites, and the reader may decline
then under `[R-ERR-04]`'s ordinary licence.

## Consequences

This is the third time in four rounds that a defect has been a **quantifier or
scope question about which things a rule ranges over** — after §20.4's drop
licence and §21.6's file-wide-versus-layer refusal. The shape is not a
coincidence: a specification that defines structures and then states limits over
them has one such question per limit, and stating the general rule once is
cheaper than answering them one at a time.

The register does not grow, and the corpus is unchanged at 121 conditions over
273 instances.

## Precedent

- `[R-COD-07]`'s addressed-tiles quantifier and §20.3's remark on it, which made
  this decision once already for a structurally identical cap.
- ADR-0085, whose repair named one quantity of a frame header where two were in
  play — the same family of defect, caught one round later.
