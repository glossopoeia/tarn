# 0018. Discovery anchoring: constant front signature block + authoritative trailer

- Status: Accepted (resolves Q-A1; exact signature byte values remain Q-G4)
- Date: 2026-07-29
- Covers: file identification; trailer layout; directory placement
- Confirm: none beyond Q-G4's byte values

## Context

With ADR-0017's append-only contract, a front-anchored directory is ruled
out (every append would rewrite it in place — the exact torn-write hazard
the contract eliminates). A pure tail anchor works but leaves the file
unidentifiable by prefix: `file`, MIME sniffers, and magic databases all
read from offset 0. A front block containing a *pointer* to the current
trailer was considered and rejected: the pointer would be patched on every
append, re-importing in-place mutation, breaking S3-style server-side
compose, and reintroducing a torn-write window — for zero saved requests.

## Decision

- **Front signature block, 16 bytes, constant and pointer-free**, written
  once at creation and never touched again: the 8-byte hardened signature
  (Q-G4) plus 8 reserved-zero bytes. It asserts "this is TARN; authority is
  at the tail" and guarantees offset 0 is never payload.
- **Trailer, exactly 64 bytes, at EOF**, with a tail magic distinct from
  the front signature (so recovery scans cannot false-positive on it):
  magic (8) · version major/minor u16+u16 (4) · flags u32 (4) ·
  generation u64 (8) · directory offset u64 (8) · directory length u64 (8)
  · committed file length u64 (8) · file id u64 (8) · metadata-codec u8
  (1) · pad (3) · CRC-32C (4). This is **64 bytes with zero slack** — any
  future field proposal forces either a flag bit or a 128-byte trailer;
  the drafting section should say so explicitly.
- The **directory sits immediately before the trailer** (only declared
  padding between), so its bytes are always at a knowable tail location;
  `committed file length` makes the trailer self-consistent
  (verifiable against actual size), and `file id` + `generation` carry the
  cache-revalidation story from ADR-0017.

## Consequences

The file is identifiable from either end: 16-byte prefix for sniffers,
64-byte suffix for readers. Early validation (front signature → trailer
magic → trailer CRC) rejects text-mode-mangled and truncated files before
any further I/O. A guaranteed non-payload byte at offset 0 also removes one
argument in the index-sentinel debate (Q-D4): offset 0 can never address a
stored tile. The 16 front bytes are the entire cost.

## Precedent

- PNG §5.2's engineered signature (the construction Q-G4 inherits).
- PMTiles v3's fixed-size discovery structure, inverted to the tail for
  appendability; its field-by-field offset/size/type table is the
  presentation model for the trailer section.
