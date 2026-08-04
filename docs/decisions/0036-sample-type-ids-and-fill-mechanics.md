# 0036. Sample-type identifiers and fill mechanics

- Status: Accepted (discharges ADR-0013's Confirm; completes ADR-0010's
  Confirm)
- Date: 2026-08-04
- Covers: type-ID assignments and element sizes; FP8, 128-bit, and
  raw-bytes disposition (Q-D1, Q-D2); boolean fill encoding and
  interleaved fill composition (Q-D3)
- Confirm: none

## Context

Type identifiers are permanent registry artifacts, and their layout is
itself a decision: width- or kind-structured IDs read nicely in hex dumps
but invite implementations to derive element sizes arithmetically and
accept unknown types heuristically — exactly the repair behavior
conforming readers are forbidden. ADR-0013 closed the v1 list at thirteen
types and left two Confirm items — whether both OCP FP8 formats stay
reserved, and whether a fixed-size raw-bytes type ships; ADR-0010's
Confirm left a third: how a boolean fill value is encoded.

## Decision

- **IDs sequential, pure enum:** bool = 1; int8/16/32/64 = 2–5;
  uint8/16/32/64 = 6–9; float16 = 10; bfloat16 = 11; float32 = 12;
  float64 = 13. Element sizes 1; 1/2/4/8; 1/2/4/8; 2; 2; 4; 8. Unknown,
  reserved, or experimental type values are a validity error at layer
  scope; no reader derives semantics from a type value's bit structure.
- **Reserved without v1 semantics, pinned against collision:**
  14 = float8 E4M3 and 15 = float8 E5M2 — only ever as bit-exact OCP OFP8
  (E4M3's non-IEEE structure — no infinities, NaN only as S.1111.111,
  the two bytes 0x7F and 0xFF — means custom decode in every reader: a
  cost paid only when a named consumer materializes); 16/17/18 = int128/uint128/float128;
  19 = opaque (fixed-size raw bytes). 20–0x7FFF future assignment;
  ≥ 0x8000 experimental.
- **`opaque<N>` deferred:** its size N could only live in the fill
  field's length, converting the fill-length cross-check from a
  redundancy into the definition — a wrong length would silently redefine
  the element size rather than be caught. Deferral keeps that check
  redundant for every v1 type.
- **Boolean fill:** one byte, 0x00 or 0x01; any other byte a validity
  error at layer scope. One value, one encoding — fill-field byte
  equality is semantic equality. In-tile boolean representation,
  including any packed-form pad bits, stays with the serialization
  decision (Q-D6).
- **Interleaved fill composes per channel:** the fill sample of an
  interleaved layer is the tuple of channel fills in declared order;
  planar channels take fill independently.
- **NaN and −0.0 stated once, in §12:** sample and fill values are bit
  patterns, never canonicalized; value identity throughout the
  specification is byte equality.

## Consequences

A weekend reader implements exactly thirteen types, none skippable. Fill
validation is two checks (length = element size; bool byte ∈ {0, 1}).
Vector obligations: a NaN-payload fill round-trip, a bool-fill 0x02
rejection, an unknown-type rejection. Foreclosed: deriving semantics from
ID arithmetic, and any non-OCP 8-bit float, permanently.

## Precedent

- PNG's no-subset conformance philosophy; Zarr's optional-type
  fragmentation as the cautionary tale (ADR-0013).
- OCP OFP8 (E4M3/E5M2) as the only eligible 8-bit float definitions.
- TIFF SampleFormat's optional-with-dangerous-default lesson behind
  mandatory recorded fill (ADR-0010).
