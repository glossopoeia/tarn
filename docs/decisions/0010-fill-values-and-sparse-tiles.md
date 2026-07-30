# 0010. Mandatory per-channel fill values; unstored tiles read as fill

- Status: Accepted
- Date: 2026-07-29
- Covers: fill/nodata semantics; sparse tiles; index sentinel
- Confirm: sentinel fixed by ADR-0024 (all-ones offset+length, CRC 0);
  packed-boolean fill mechanics remain open (Q-D3).

## Context

Sparse and partially-written arrays are the common case in scientific and
geospatial data, and a format that treats an unwritten region as an error
forces every writer to materialize oceans of constant data. Zarr settled the
semantics that work: a chunk absent from storage reads as the array's fill
value, and fill is recorded rather than assumed. Zarr also supplies the
representation lesson: its JSON fill values could not express NaN payloads or
distinguish −0.0, and needed a hex-bit-pattern retrofit. A binary format can
sidestep that entire wound by storing fill as raw element bytes from day one.

## Decision

Every channel records a fill value as raw little-endian element bytes —
bit-exact, so NaN payloads and −0.0 round-trip by construction. Fill is
mandatory-with-default: if the user does not choose one, the writer records
its default (all-zero bits) explicitly; readers never guess. A reserved
index-entry sentinel marks a tile that is addressed but not stored; reading
such a tile yields fill for every sample, as a defined semantic rather than an
error. Every other malformed index-entry combination (sentinel-offset with
nonzero length, nonzero checksum on a sentinel entry, ranges past EOF,
overlapping extents) is enumerated as invalid with an assigned outcome class.
Growing a layer's extent is a metadata-only operation, stated as a supported
property.

## Consequences

Sparse layers are first-class and near-free; edge-padding content has a
natural definition available (ADR-0011); "read of unwritten data" becomes
deterministic across implementations. Because the index is checksummed
(ADR-0008), corruption can never be silently misread as "tile absent, return
fill" — a sentence the spec must contain. Writers pay one rule: record fill
always, even when defaulted.

## Precedent

- Zarr v3 fill-value semantics (missing chunk reads as fill) and the
  hex-bit-pattern retrofit (zarr-specs PR #236) that bit-exact binary storage
  avoids.
- Zarr sharding's empty-chunk sentinel, with its undefined
  malformed-combination space closed here.
- TIFF's optional-with-dangerous-default fields (SampleFormat) as the
  counterexample to optional fill.
