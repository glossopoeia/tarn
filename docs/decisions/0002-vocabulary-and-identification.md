# 0002. Core vocabulary and file identification

- Status: Accepted
- Date: 2026-07-29
- Covers: terminology; file identity (name, extension, magic)
- Confirm: the signature form — bare ASCII `TARN` or a PNG-style hardened
  8-byte signature that *contains* ASCII "TARN" (e.g.
  `89 54 41 52 4E 0D 0A 1A`). What is settled: the magic contains ASCII
  "TARN". Leaning: hardened, per the transport-corruption argument in
  Context (tracked as OPEN-QUESTIONS Q-G4).

## Context

A format's noun set is its first interoperability surface: when two
implementers mean different things by "tile," no amount of byte-layout
precision saves them. PNG anchors its conformance story in a defined
"reference image"; PMTiles distinguishes tiles that are *addressed* by the
coordinate space from tiles that are physically *stored* — the distinction that
makes sparse data well-defined. On identification: PNG's signature is
deliberately engineered — a high-bit byte catches 7-bit stripping, embedded CR
LF catches line-ending translation, and ctrl-Z stops accidental console
display — and that engineering has caught real transport corruption for three
decades. Bare ASCII magic detects none of those corruption classes.

## Decision

The fixed noun set, used consistently in every ADR and spec section:

- **file** — a single TARN artifact.
- **layer** — a named N-dimensional array within a file.
- **dimension** — one axis of a layer's grid; dimensions define extent and
  tiling.
- **channel** — a named, typed per-sample value; a **sample** is the tuple of
  channel values at one coordinate.
- **tile** — one cell of the tiling grid (a logical unit). An **addressed**
  tile is any tile in the grid; a **stored** tile additionally has payload
  bytes in the file. An addressed-but-unstored tile reads as fill.
- **slab** — an aligned, contiguous run of stored tiles treated as one I/O
  unit.
- **directory** — the consolidated metadata structure; **index** — the
  per-layer table of stored-tile locations.
- **reference array** — the exact N-dimensional array of channel values a
  conforming reader must reconstruct; the target all conformance statements
  point at.

Identity: the format is TARN, the extension is `.tarn`, and the magic contains
ASCII `TARN`. A MIME type is declared in the spec (`application/vnd.tarn`
proposed).

## Consequences

Every subsequent decision can be stated in one vocabulary; the
addressed/stored split is what makes fill-value semantics and the index
sentinel definable without ambiguity. The signature Confirm item is the one
deliberately held-open sub-question: hardening costs four bytes and buys
detection of text-mode mangling before any other validation runs.

## Precedent

- PNG §5.2 (signature construction and rationale), PNG's "reference image"
  conformance device.
- PMTiles v3 addressed/stored tile vocabulary and its RunLength encoding.
