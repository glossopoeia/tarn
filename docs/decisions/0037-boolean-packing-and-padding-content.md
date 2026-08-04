# 0037. Packed booleans over the value sequence; fill-encoded edge padding

- Status: Accepted (discharges ADR-0011's and ADR-0012's remaining
  Confirms; resolves Q-D6 and Q-C4's stored-sample half)
- Date: 2026-08-04
- Covers: boolean in-tile representation; edge-tile padding content;
  the layout × boolean validity cell
- Confirm: none

## Context

Two forces. Bit-packing is 8× on masks — the dominant boolean
workload — but bits have no byte addresses, so a bool channel mixed
with numeric channels in an interleaved sample would need a hoisted
per-sample packed sub-field: kind-conditional offset arithmetic and
its own pad rules, the underspecified-interaction pattern TIFF's
PlanarConfiguration teaches against (ADR-0012). Byte-per-bool avoids
that but creates the format's only invalid decoded content (what is
0x02?) — a two-encodings trap or a new per-byte screening obligation.
Separately, edge tiles are stored full-size (ADR-0011), so padding
content participates in codecs and checksums and must be
deterministic.

## Decision

- **Booleans are bit-packed, LSB-first, over the tile's decoded value
  sequence:** value k at byte k div 8, bit k mod 8, matching the
  spec's bit-0-is-LSB numbering with no reversal step. Planar bool
  plane: ⌈P/8⌉ bytes, bit position = in-tile ordinal mod 8. All-bool
  interleaved tile: ⌈P·C/8⌉ bytes, value index = ordinal·C + c. One
  rule for both layouts; a single-bool-channel layer serializes
  identically in either.
- **Mixed is planar-only:** a layer whose channels include bool
  together with any non-bool channel MUST NOT be interleaved —
  a validity error at layer scope (the ADR-0012 validity-table
  mechanism: writer-MUST-NOT paired with reader-MUST-reject).
  Foreclosed: per-sample packed sub-fields.
- **Edge padding carries fill:** every stored value at a padding
  position is, per channel carried, that channel's fill encoding, and
  every packed-boolean pad bit beyond the last value carries the fill
  bit of the channel its value index maps to under the sequence rule
  extended past the last value (channel k mod C interleaved; the
  plane's channel planar). Alignment-gap and structural padding stay
  zero bytes (ADR-0030) — different mechanism, unchanged.
- **Enforcement:** writers MUST; the properties are file conformance,
  detectable only by decoding, so their assigned checker is the
  verifier (reject-tile). Ordinary readers clip and never pay.

## Consequences

Masks cost ⌈P/8⌉ bytes before compression instead of P. No invalid
decoded states exist anywhere in the format — every bit pattern of
every conforming tile decodes; the pad-bit and padding rules bind
writers, never reader decode paths. Unclipped-reader bugs surface as
fill, not garbage, and padding bytes cannot leak writer memory. The
spec gains the packing formula, worked byte examples, and one
validity cell. Foreclosed: mixed bool+numeric interleaved layers
(planar serves that data), and any meaning for pad bits.

## Precedent

- TIFF PlanarConfiguration's underspecified interactions (ADR-0012)
  as the argument against per-sample sub-fields.
- PNG packs sub-byte samples MSB-first ("leftmost pixel in the
  high-order bits"), coherent with its big-endian conventions; under
  this specification's bit-0-is-LSB numbering (spec §4.4, of a piece
  with ADR-0014's little-endian discipline) the coherent pairing is
  LSB-first — importing PNG's order would cost an index reversal
  (bit 7 − k mod 8) in every packing loop.
- The uninitialized-padding leak class in image encoders, and the
  determinism lesson (QOI boundary analysis,
  docs/research/reference-format-lessons.md) for fill-encoded
  padding.
- Zarr's regular chunk grid edge semantics (ADR-0011).
