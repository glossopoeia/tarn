# 0005. Optional per-layer tile alignment as a checkable invariant

- Status: Accepted
- Date: 2026-07-29
- Covers: physical layout; O_DIRECT / GPUDirect Storage / mmap support
- Confirm: minimum and default alignment values (proposed: ≥ 512, with 4096
  as the recommended default).

## Context

Direct-I/O paths (O_DIRECT, GPUDirect Storage) and memory mapping require
payload offsets aligned to device or page boundaries. A layout property is
only real if a validator can check it: PMTiles' `clustered` flag demonstrates
the pattern — declare the invariant in the file, and tools can verify it —
and its offset-reuse deduplication demonstrates the conflict: two index
entries sharing one payload extent are arithmetically incompatible with
stride-aligned layout and with byte-coverage accounting.

## Decision

A layer MAY declare an alignment value A (a power of two; minimum and
default under Confirm — proposed ≥ 512, default 4096). When declared: every
stored tile's start offset satisfies `offset mod A == 0` (slabs inherit the
same rule), inter-tile gaps introduced by alignment are explicit padding
(zero bytes, per the leaning in OPEN-QUESTIONS Q-C4), and stored-tile
extents in an aligned layer are never shared or overlapping — no
deduplication by offset reuse. Alignment is reader-invisible: offsets are
always explicit in the index, so a reader that ignores the flag needs no
additional code path. Verifiers check the invariant.

## Consequences

GPU and direct-I/O consumers get a guarantee, not a hope; the padding cost is
the writer's declared, bounded choice. Deduplication is foreclosed in aligned
layers — an easy price, since constant-content tiles are better served by the
fill-value sentinel (ADR-0010) than by shared payloads.

## Precedent

- PMTiles v3 `clustered` flag (declared layout invariants) and its
  offset-reuse dedup as the documented tension.
- The reader-invisible-option principle: options that only constrain writers
  are the cheapest kind of option a spec can add (BCP 14 reciprocity
  analysis, `docs/research/reference-format-lessons.md`).
