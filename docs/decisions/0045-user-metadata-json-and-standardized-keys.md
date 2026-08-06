# 0045. User metadata is restricted JSON; conventions live as keys

- Status: Accepted (resolves Q-F1, Q-F3, Q-D5; discharges ADR-0015's
  encoding Confirm)
- Date: 2026-08-05
- Covers: the user-metadata document's encoding and value profile;
  key namespacing; the standardized-key mechanism; axis/unit
  conventions; per-channel statistics
- Confirm: none

## Context

ADR-0015 left the encoding open between UTF-8 JSON and canonical
CBOR, resting the case largely on determinism: metadata serialized
in nondeterministic order yields different bytes for identical
content. That argument has weakened as the specification matured.
`[R-CNF-05]` declines to promise canonical bytes anywhere — two
conforming writers given identical input may produce different
conforming files — so byte-determinism of the metadata blob alone
would buy a property the format does not have at any other level.
What remains decisive is the pair of gates: a normative CBOR
reference costs afternoon-readability, and a CBOR dependency costs
weekend-implementability, in a document whose external normative
references are otherwise BCP 14, RFC 3720 for CRC-32C, RFC 1951 and
RFC 8878, the LZ4 Block Format Description, and IEEE 754 — none of
which is a general-purpose data model an implementer must learn.
JSON adds RFC 8259, and RFC 3339 for one date-time key.

Separately, two ledger entries were waiting on this section — axis
and unit conventions (Q-F3) and per-channel statistics (Q-D5) — and
both asked whether they belong in the core.

## Decision

- **UTF-8 JSON (RFC 8259), restricted.** The document is a JSON
  object. Forbidden: NaN and the infinities, which JSON cannot
  express and which belong to structural fields anyway (fill values
  are raw element bytes, ADR-0010). Writers MUST sort object keys by
  their UTF-8 bytes, which makes identical content reproducible from
  one writer without promising byte-identity across writers.
  Duplicate keys within an object make the document unreadable —
  ignore-record, under the quarantine.
- **Keys are namespaced.** The prefix `tarn.` belongs to this
  registry. Everything else is application space, and applications
  SHOULD use a reverse-DNS prefix; unprefixed keys are legal and
  unreserved, and colliding on one is the application's problem.
- **Conventions live as standardized keys, not core fields**
  (Q-F3): axis metadata — unit, origin, step, giving the affine
  mapping scientific users need — is registered as
  `tarn.axes`, not as dimension-record fields. The core stays
  neutral; GeoTIFF and EXIF demonstrate domain semantics thriving as
  layered registries over a neutral core, and the extension
  mechanism is the promotion path if a convention ever earns core
  status.
- **Per-channel statistics are standardized keys** (Q-D5):
  `tarn.stats` carries advisory min/max per channel. Because user
  metadata is non-structural by construction, "advisory" needs no
  new rule — a reader already MUST NOT let metadata affect decoding,
  so stats cannot be relied on for correctness by anyone, and no
  staleness machinery, verifier obligation, or preserve-on-edit
  semantics has to be written. NaN is excluded from min and max,
  stated once in the key's definition.

## Consequences

The metadata story costs one restricted profile of a format every
language already parses. Applications get an unbounded, quarantined,
compressible place for annotations that never touches the discovery
budget; communities get a registry rather than a fork. Priced
knowingly: no binary values (base64 in a string is the escape, and
bit-exact numbers belong in structural fields), and no byte-identical
metadata across writers — an application needing content-addressed
metadata canonicalizes the decoded document itself. Foreclosed: a
second binary parser in the format, and dimension-semantics fields
in the core that every reader would carry forever.

## Precedent

- Zarr's `attributes` object as the structural/user quarantine, and
  its JSON encoding at the same layer.
- PMTiles' compressed JSON metadata blob.
- GeoTIFF and EXIF as layered key registries over neutral cores
  (ADR-0015's own precedent, now acted on).
- RFC 8259 for the encoding; the determinism limits of JSON numbers
  are why byte-identity is disclaimed rather than mandated.
