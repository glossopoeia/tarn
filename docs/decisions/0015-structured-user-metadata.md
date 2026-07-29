# 0015. Structured, quarantined user metadata instead of flat string tags

- Status: Proposed
- Date: 2026-07-29
- Covers: user metadata (tags); extension registry hook for standardized keys
- Confirm: (a) encoding — UTF-8 JSON (recommended) vs canonical CBOR;
  (b) granularity — one document per file, plus optionally one per layer
  (see OPEN-QUESTIONS Q-F1).

## Context

Flat string pairs are where metadata needs start, never where they end, and
the retrofit history is consistent. PNG grew three text-chunk types (tEXt,
zTXt, iTXt) because charset and compression were baked into record identity
rather than kept orthogonal. The opposite failure is structural: metadata
that can alter decoding is a second parser with security consequences. The
proven shape is a single structured document, quarantined from structural
metadata, with a small registry of standardized keys — Zarr's `attributes`
object and PMTiles' compressed JSON blob (whose v2 placement-derived size cap
taught: never size-limit metadata by where it happens to sit) both landed
there. Determinism matters too: metadata serialized in nondeterministic
order produces different bytes for identical content, breaking
reproducibility and content-addressing.

## Decision

One structured user-metadata document per file, and optionally one per layer:
UTF-8 JSON (recommended; canonical CBOR is the Confirm alternative),
compressed with the internal metadata codec (contingent on ADR-0009's
Confirm item; stored uncompressed if that resolves to none), offset-addressed
from the directory (never inside the fixed discovery structure, so its size
is unbounded by placement), and checksummed. Writers serialize
deterministically (sorted keys). Structural facts — types, geometry, codecs,
fill — never live here; readers MUST NOT let user metadata alter decoding;
updaters preserve it verbatim. A registry of standardized keys (units,
coordinate/axis conventions, domain profiles) gives communities a defined
home, with conditional requirements expressible per profile ("a file claiming
profile X MUST carry key Y").

## Consequences

Metadata needs stop generating new record types; unbounded metadata never
touches the O(1) discovery budget; flat key-value pairs remain trivially
expressible, so the upgrade is strictly additive in capability. Dimension
coordinate/unit conventions get a home without expanding the core (see
OPEN-QUESTIONS Q-F3). The cost: one structured-text dependency in an
otherwise binary spec — the encoding Confirm item weighs exactly that.

## Precedent

- PNG tEXt/zTXt/iTXt triplication — orthogonality baked into identity.
- Zarr `attributes` (structural/user quarantine); PMTiles metadata JSON and
  its v2 size-cap lesson, plus its `vector_layers` conditional-requirement
  pattern.
- GeoTIFF/EXIF as layered key registries thriving outside a core format.
