# 0013. Closed sample-type list with zero optional members

- Status: Accepted
- Date: 2026-07-29
- Covers: data types
- Confirm: whether any near-term consumer justifies shipping OCP FP8 types in
  v1 rather than reserving them; whether an `opaque<N>` raw-bytes type makes
  v1 (see OPEN-QUESTIONS Q-D1, Q-D2).

## Context

Every core data type is a permanent obligation on every conforming reader,
forever. Zarr's experience makes the cost concrete: types that are "optionally
supported" fracture the implementation matrix — a file that is valid for one
reader and unopenable for the next repeats the optional-everything failure
TIFF demonstrated.
The discipline that follows: the type list is closed, every listed type is
mandatory, and a type earns its slot only with a demonstrated interchange
need. For 8-bit floats specifically, the only definitions worth standardizing
on are the OCP OFP8 formats (E4M3: no infinities, S.1111.111 as NaN, ±448
max; E5M2: IEEE-structured) — a nonstandard minifloat variant would be a
permanent interoperability wart.

## Decision

The v1 type list, closed, all reader-MUST, all stored as raw little-endian
bit patterns:

> bool, int8, int16, int32, int64, uint8, uint16, uint32, uint64,
> float16 (IEEE 754 binary16), bfloat16, float32, float64

Type identifiers are pure enums: no flag bits, no presence bits, no metadata
smuggled into the type word — a type ID compares equal or it doesn't.

Not in v1, with identifiers **reserved**: 8-bit floats (only ever as
bit-exact OCP E4M3/E5M2; nothing else will be considered), int128, uint128,
float128. Reserved types enter, if ever, through a minor revision with
must-understand semantics once a concrete consumer materializes. An
`opaque<N>` fixed-size raw-bytes type is under consideration as the pressure
valve that keeps the numeric list closed.

## Consequences

Every conforming reader opens every conforming file — no dtype dialects. ML
workloads get float16/bfloat16 first-class. Anyone needing 128-bit or FP8
types today must wait or carry them as opaque bytes; that friction is the
deliberate price of the no-dialects guarantee. The spec must still define
NaN/−0.0 handling once, in one place, for all float types (fill, statistics,
and comparison semantics).

## Precedent

- Zarr's optional-type fragmentation as the direct cautionary tale; its
  raw-bits `r*` types as the escape-hatch pattern.
- OCP OFP8 specification (E4M3/E5M2) as the only 8-bit float definitions
  eligible for future inclusion.
- PNG's no-subset conformance philosophy applied to a type system.
