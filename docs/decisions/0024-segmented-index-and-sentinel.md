# 0024. Tile index: raw segmented encoding, all-ones sentinel, exactly-once extents

- Status: Accepted (resolves Q-E3, Q-D4, Q-B4; amends ADR-0008's whole-
  structure CRC to segment granularity for the index; discharges
  ADR-0010's sentinel Confirm)
- Date: 2026-07-30
- Covers: index layout and integrity; unstored-tile sentinel; extent
  ownership
- Confirm: none (the sparse-segment CRC constant is recomputed and pinned
  when the final field order freezes in drafting)

## Context

A flat array of 20-byte entries is the simplest possible index — entry k
at byte 20·k, mmap-able, one decode path. But verify-before-use (ADR-0008)
against a single whole-index CRC would force a conforming remote reader to
download the entire index to use one entry: 19 MiB at 1M tiles, 190 MiB at
10M. Separately, the unstored-tile sentinel needed a bit pattern, and the
deciding hazard is the commonest storage bug there is: a zeroed region
(uninitialized buffer, filesystem hole) that the writer then honestly
checksums. Under a zero/zero sentinel that region parses as valid
all-sparse and silently reads as fill — silent data loss; under all-ones it
is loudly invalid.

## Decision

**Encoding.** Per-layer index region, contiguous:
`[entry array: n × 20 B] ‖ [segment CRC array: ⌈n/2¹⁶⌉ × 4 B]`, both
bare. Entry: offset u64 · length u64 · crc32c u32, LE. Segment s covers
entries [s·2¹⁶, min((s+1)·2¹⁶, n)); the final partial segment's CRC covers
only its actual bytes. The layer record's index reference uses the record
header's extent slot (ADR-0026) for offset/length; its inline payload
carries `entry_count u64` and `crc_of_crc_array u32`, with the cross-checks
`extent_length == entry_count×20 + ⌈entry_count/2¹⁶⌉×4` and entry_count
equal to the geometry-derived tile count (mismatch → reject-layer). Chain
of trust: trailer → directory → CRC array → segment → entry → tile. A
reader for tile k fetches the CRC array and segment k≫16 **in parallel**
(both ranges computable from the layer record alone): verified index cost
≤ ~1.25 MiB at any scale, serial depth unchanged from ADR-0019. Files with
n ≤ 2¹⁶ are single-segment — the naive whole-index reader, unchanged; the
fetches coalesce when adjacent (non-normative note). The per-layer
`index_encoding` u8 is 0 = invalid, 1 = raw-segmented (only emittable v1
value), 2 reserved columnar, ≥ 0x80 experimental; unknown → reject-layer.

**Sentinel.** Addressed-but-unstored tile: offset = 2⁶⁴−1, length = 2⁶⁴−1,
CRC field = 0 (`FF×16 00×4`). Zeroed regions parse as offset 0/length 0 —
invalid (offset 0 is the front block; zero-length stored tiles do not
exist); all-0xFF regions are invalid too (nonzero CRC field on sentinel).
The spec carries the full invalid-combination table — sentinel/real field
mixtures, zero length, offset into the front block, overflow, extent past
`committed_file_length`, extent into the live trailer's final 64 bytes
(reject-tile, decidable from one entry), overlap and alignment violations
(verifier-level) — one outcome and one corrupt-file vector per row. An
all-sentinel segment's CRC is a spec constant sparse writers may emit
without computing (pinned at drafting; equality is never a licensed
shortcut for skipping verification).

**Extent ownership (Q-B4).** Every stored-tile extent and every metadata
extent is referenced exactly once within the live generation — no
deduplication, no overlap. Constant tiles are the sentinel's job at 20
bytes each. Overlap within a layer → reject-layer (both entries' layer);
overlap across layers or with any metadata structure → reject-file.

## Consequences

One index format; O(1) entry arithmetic; bounded verified fetch at any
scale; sparse layers cheap; every malformed shape loud. Foreclosed:
columnar compression (reserved enum) and implicit-offset encodings.
Growth re-emits the layer's index region (ADR-0021). The Q-B5 coverage
rule inherits a clean exactly-once partition to build on.

## Precedent

- Zarr sharding's (2⁶⁴−1, 2⁶⁴−1) empty-chunk sentinel — adopted, with its
  undefined-combination space closed.
- PMTiles' columnar directories — the road reserved, not taken, with the
  CRC-column floor and segment fetch analysis as the reasons.
