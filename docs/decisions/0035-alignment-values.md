# 0035. Alignment value sets

- Status: Accepted (discharges ADR-0005's Confirm)
- Date: 2026-07-30
- Covers: per-tile alignment floor and default; slab-alignment floor
- Confirm: none

## Context

ADR-0005 accepted per-tile alignment as a declared invariant and left
the value set open; ADR-0022's slab declaration added a second
alignment knob (A_slab). The two serve different consumers: per-tile
alignment exists for direct I/O and memory mapping, where values below
the storage sector size are useless, while slab alignment rides a
contiguity guarantee that is independently valuable — HTTP range
coalescing wants contiguous runs and could not care less about their
starting offsets, and forcing an alignment floor there would impose
padding on writers who get nothing for it.

## Decision

- **Per-tile alignment A**: when declared, a power of two ≥ 512 (the
  legacy sector floor). The recommended default for writers that align
  is 4096 — page size and modern physical sector size, satisfying
  O_DIRECT, mmap, and GPUDirect everywhere — stated non-normatively.
- **Slab alignment A_slab**: when a slab is declared, any power of two
  ≥ 1. A_slab = 1 is the *contiguity-only* slab: runs are contiguous
  and packed with no alignment promise — the right declaration for
  remote-coalescing workloads.

## Consequences

Value validity lands in the layer-record constraints and §16's
invariants; two vector candidates (A = 256 rejected; A_slab = 1
accepted). Foreclosed: sub-sector per-tile alignment, which no I/O
path can use.

## Precedent

- 512/4096 as the industry sector and page constants; ADR-0005's
  reader-invisible-option principle extended to its cheapest form
  (contiguity with no alignment at all).
