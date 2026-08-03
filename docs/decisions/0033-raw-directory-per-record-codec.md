# 0033. The directory is raw; user-metadata records declare their own codec

- Status: Accepted (amends ADR-0032's internal-codec bullet and
  ADR-0025's metadata-codec degradation row)
- Date: 2026-07-30
- Covers: metadata compression scoping; trailer byte 56
- Confirm: none

## Context

A maintainer challenge to the freshly drafted container caught an
inherited-momentum decision: the internal metadata codec was justified
by the PMTiles precedent, but PMTiles compresses *per-tile*
directories (millions of entries), and TARN moved all per-tile data
into the tile index — which the codec already exempted. What remains
in the directory is O(layers): ~1.2 KB at 5 layers, ~4.5 KB at 20,
against a 64 KiB fetch window — compression saves noise, and only
begins to matter near ~290 typical layers, where the degradation is
one extra exact-range request anyway. Meanwhile the codec's real
payoff is user-metadata documents (10 KB–1 MB of JSON-shaped content,
compressing 5–10×), and putting the declaration in the trailer forced
two decode paths onto the mandatory open sequence and made new codec
values major-only (an undecodable directory kills the file).

## Decision

- The **directory region is always raw**: its bytes are the record
  sequence followed by its CRC, with no codec involvement. The
  mandatory open path (trailer → directory) is codec-free.
- **Trailer byte 56 is reserved** and MUST be zero (validated with the
  pad bytes); the metadata_codec field is removed from the trailer.
- Each **user-metadata record declares its document's encoding in its
  own payload** (u8: 0 invalid, 1 = none, 2 = zstd; details with the
  user-metadata section). An unknown encoding value makes that record
  unreadable, with the same outcome as its CRC failing: ignore-record,
  SHOULD be reported (ADR-0031). File-scope and layer-scope documents
  may differ in encoding.
- The tile index remains raw always (unchanged from ADR-0032).

Consequently, new metadata-codec values are no longer major-only:
their unknown-value outcome is defined at ancillary-record scope, so
future codecs can arrive as additive minors under ADR-0025's
whitelist. ADR-0025's degradation table is amended accordingly.

## Consequences

A minimal reader that ignores user metadata never decodes anything on
the metadata path; the two-path directory open, its
exactly-one-frame validation, and its conformance vectors disappear;
compression stays exactly where it pays. Foreclosed: compressed
directories — files with many hundreds of layers pay the second
request slightly sooner, an accepted tail cost.

## Precedent

- PMTiles' directory compression as the precedent that did not
  transfer once per-tile data moved to the exempt index — recorded as
  a worked example of challenging inherited defaults.
