# 0030. Byte coverage is file validity

- Status: Accepted (history-wide coverage superseded by ADR-0048; the live-state partition it established stands) (resolves Q-B5; pins the alignment-gap half of Q-C4)
- Date: 2026-07-30
- Covers: the byte-coverage partition; declared padding content;
  unclaimed bytes
- Confirm: none

## Context

Ordinary readers touch only live structures, so unreferenced byte
ranges are invisible to them — which is exactly what makes such ranges
a smuggling channel: arbitrary bytes written between generations by a
nonconforming writer ride inside a file whose every checksum verifies.
The alternatives were to make coverage a validity property (unclaimed
bytes ⇒ nonconforming file) or a verifier diagnostic (reported, not
invalidating). The diagnostic option permanently concedes "a conforming
TARN file can carry arbitrary undeclared bytes" — the
PNG-after-IEND/TIFF-unreferenced-ranges weakness the research catalog
names — while the validity option's entire cost lands on the verifier
role, since conforming writers produce partitioned files by
construction and readers never perform the check.

## Decision

Every byte of a conforming file belongs to exactly one class: the front
block; a structure (stored-tile extent, index region, user-metadata
extent, directory, trailer) of exactly one generation; or declared
padding of exactly one generation. Declared padding bytes — alignment
gaps in aligned or slab-declared layers, and the pre-trailer pad — MUST
be zero. A file containing bytes claimed by no generation's structures
or padding is not a conforming file. The verification procedure
(enumerate generations by trailer scan-back; check the partition) is
specified with the container; it is a verifier procedure, never a
reader obligation. Superseded structures of prior generations are dead
space: never interpreted by readers, reclaimed only by compaction.

The remaining half of Q-C4 — the content of edge-tile padding
*samples*, which live inside stored payloads — stays open for the tile
serialization section.

## Consequences

"Integrity by default" extends from bytes-are-uncorrupted to
bytes-are-accounted-for: a verifier can certify that a file contains
nothing but what it declares, and ADR-0017's append discipline becomes
a checkable property of the artifact rather than a promise about tools.
The risk — some legitimate writer sequence we failed to classify — is
recoverable by ADR; the rejected option's smuggling channel would have
been permanent.

## Precedent

- PNG's forbid-but-warn trailing-data gap and TIFF's unreferenced
  ranges as the weakness class this closes; PMTiles' relocatable
  sections as the certification gap named in the research catalog.
