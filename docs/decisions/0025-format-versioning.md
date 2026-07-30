# 0025. Format versioning: trailer major/minor, additive minors, forever clause

- Status: Accepted (resolves Q-G1)
- Date: 2026-07-30
- Covers: version semantics; compatibility lanes; cross-major invariants
- Confirm: none

## Context

This is the **format** version — which parser contract a file requires —
distinct from the per-file generation counter (dataset evolution,
ADR-0017) and from domain dataset versioning (user metadata). A version
field protects readers only if the rules for bumping and reacting to it
are mechanical: version fields without flags end in forks (BigTIFF);
flags without a version lose the blunt refuse-early lever. TARN takes
both, with the version reserved for outer-framing changes and per-record
flags (ADR-0026) doing the day-to-day feature negotiation.

## Decision

The trailer (ADR-0018) carries `version_major u16`, `version_minor u16`;
value 0 is invalid for major (zeroed bytes never masquerade). Reader
rules: unknown major → reject-file with a precise diagnostic ("TARN major
N; this reader supports major 1"), distinct from "not TARN" and
"corrupt"; unknown minor → MUST proceed. Minors are **additive-only**,
defined by an exhaustive whitelist: new registered record types; new enum
values inside ranges v1 already reserves with defined unknown-value
outcomes (codec, filter, type, linearization, index-encoding — all
reject-layer); new ignore-lane flag bits; new standardized metadata keys.
The bright-line test: *expressible as a new record type plus a registry
entry → minor; otherwise → major or rejected.* A minor MUST NOT
reinterpret any existing byte, grow any fixed structure, or alter framing.
New trailer `metadata-codec` values are **major-only** (an undecodable
directory cannot be additive).

Trailer `flags u32` splits into lanes: bits 0–15 **incompat** — creators
MUST zero in v1; readers MUST reject-file on any unknown set bit (the
refuse lever that spares the major); bits 16–31 **ignore** — readers MUST
ignore; creators MUST zero, and **updaters MUST copy unknown ignore-lane
bits forward** (else the first older-tool append strips them).

**Forever clause, binding on every future major:** the final 64 bytes
contain the tail magic at EOF−64, major/minor at EOF−56, and a CRC-32C
over those 64 bytes at EOF−4; the 16-byte front block is constant across
all majors. Future majors may rearrange only the remaining 48 trailer
bytes; more space comes from extension blocks *before* the footprint,
never by growing it. This is what makes the precise unknown-major error
implementable by every reader ever shipped. Fixed structures never grow
(per major and, for the index, per encoding): a known structure at an
unexpected size is a validity error at its owning scope, never evidence
of a newer version. Front-block verification is required for local opens
and sniffers; remote readers MAY defer it (ADR-0019's two-request
accounting is unchanged).

The spec carries the degradation table: for every anticipated feature
(curve orders, new codecs, fp8 types, new index encodings, stats records,
incompat-lane uses), the vehicle and the exact v1-reader outcome.

## Consequences

Major bumps should be generational rarities; everything anticipated
travels through reserved enums, new record types, or flag lanes with
defined old-reader outcomes. Writers state a floor honestly (emit the
lowest minor defining every feature present); appenders emit
max(prior, own floor).

## Precedent

- PNG's 30 versionless years on per-chunk criticality; BigTIFF as the
  version-without-flags fork; Zarr's additive-minor contract; the
  ext4 compat/incompat flag-lane pattern.
