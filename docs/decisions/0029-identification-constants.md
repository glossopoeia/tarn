# 0029. File identification constants

- Status: Accepted (resolves Q-G4; discharges ADR-0002's signature
  Confirm)
- Date: 2026-07-30
- Covers: front signature bytes; trailer magic; MIME type
- Confirm: none

## Context

ADR-0002 settled that the magic contains ASCII "TARN" and left the form
open; ADR-0018 fixed a 16-byte constant front block and a distinct
trailer magic. The front signature adopts PNG's engineered construction
— a high-bit byte catches 7-bit stripping, embedded CR LF catches
line-ending translation, ctrl-Z stops accidental console display — and
the trailer magic must be distinct from the front signature so a
recovery scan-back can never mistake offset 0 (which is 64-aligned) for
a trailer, and should fail probe comparisons on its first byte.

## Decision

- **Front signature** (bytes 0–7 of every file):
  `89 54 41 52 4E 0D 0A 1A` — `\x89`, ASCII "TARN", CR LF, ctrl-Z.
  Bytes 8–15 of the front block are zero. The block is constant across
  all format majors (ADR-0025's forever clause).
- **Trailer magic** (bytes 0–7 of the trailer, at EOF−64):
  `8A 4E 52 41 54 0D 0A 1A` — `\x8A`, ASCII "NRAT" (TARN reversed, at
  the reversed end of the file), CR LF, ctrl-Z. The first byte differs
  from the front signature's, so scan-back probes reject front-block
  collisions on the first comparison, and a hex dump's ASCII column
  shows `.NRAT..` at the tail.
- **Media type:** `application/vnd.tarn` is the intended registration;
  extension `.tarn` (ADR-0002).

## Consequences

Both constants are pinned in the spec's constants appendix and carried
by every conformance vector. Text-mode mangling of either end of the
file is detectable before any structural parsing.

## Precedent

- PNG §5.2's signature construction and rationale, applied at both ends
  of the file.
