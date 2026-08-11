# 0059. Metadata encoding 2 is core

- Status: Accepted
- Date: 2026-08-11
- Covers: whether a conforming reader may decline zstd-encoded user metadata
- Confirm: none

## Context

§1 promises *"no subset profiles, no subset readers, and no feature a conforming
reader can decline"*, and §2.3 spells that promise out over codecs, filters,
channel layouts, and sample types. §18.2 then reads the other way: an encoding
*"this specification does not assign, or one the reader does not implement, is
ignore-record"* (`[R-MTA-03]`, `[R-CNT-25]`) — which contemplates a reader that
declines encoding 2 and conforms anyway. Cleanroom round 6 reported the pair,
and a drafter declined to reconcile it editorially on the ground that it decides
which files a conforming reader must accept. It does.

## Decision

**Metadata encoding 2 is core.** A conforming reader MUST be able to decode it.
§18.2's *"or one the reader does not implement"* narrows to encodings this
specification does not assign.

The capability is already mandatory, which is why this costs nothing. §17.2
assigns codec 3 as zstd and `[R-COD-11]` makes every assigned codec core —
software unable to execute one is not a conforming reader. §18.2 already builds
encoding 2 from `[R-COD-06]`'s frame constraints, the same rule codec 3 uses,
less the clauses that reference a tile's declared decoded size. A reader that
conforms at all therefore links this decoder already. Designating the encoding
core adds no code path; it withdraws a permission no reader had reason to take.

**`[R-MTA-09]`'s decline stands, and is not that permission.** A reader decodes
with a bound of its own choosing, no smaller than §21.9's user-metadata
guarantee, and a document exceeding that bound is ignore-record. That is a
resource limit, not a capability gap: such a reader has declined an oversized
document, not an encoding. A verifier that stops there still reports *cannot
establish* and MUST NOT certify the file.

## Consequences

§1's sentence stands unqualified, and §2.3's core list gains metadata encodings
alongside codecs, filters, layouts, and sample types. After this, a user-metadata
document reaches ignore-record by an unassigned or experimental encoding, by
exceeding the reader's size bound, or by the structural failures §18 already
names — never by *"this reader does not do zstd"*.

Foreclosed: a reader that serves tiles but declines metadata on capability
grounds. That reader was never honestly buildable — it had to link a zstd
decoder for codec 3 and then refuse to call it.

Priced knowingly, and the price is worth stating plainly: this is stricter than
the precedent below. PNG lets a decoder ignore an ancillary chunk outright, so a
PNG decoder may skip `zTXt` without decompressing anything. This format made a
stronger promise in §1 than PNG ever made, so it has to choose — and given
codec 3, choosing *core* costs an implementer nothing while keeping the promise.

## Precedent

- PNG (ISO/IEC 15948): `zTXt` and `iTXt` reuse the same zlib stream that `IDAT`
  already obliges every decoder to implement, rather than introducing a second
  compressor for text. Reuse of an already-mandatory decoder is what makes a
  capability free; this decision is that reuse made explicit.
- Zarr v3's *core codecs* set, which names a mandatory subset rather than
  leaving every codec an extension point.
- §2.3 and `[R-COD-11]`, which already answer the identical question for tile
  codecs, and ADR-0043, under which limits bound resources rather than validity.
