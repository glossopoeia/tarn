# 0053. Corpus layout, vector identity, and one defect per vector

- Status: Accepted
- Date: 2026-08-10
- Covers: the tree under `conformance/`; how a vector is identified and how
  that identity survives register renumbering; seeds and recipes; the
  isolation rule; the licence boundary inside the directory
- Confirm: none

## Context

ADR-0046 fixed what the corpus *is* — derivative evidence, CC0, a JSON
manifest — and left its mechanics open. Three of those mechanics decide
whether the corpus stays trustworthy as it grows past a handful of files.

The first is identity. §21's row identifiers are positional labels, and
this repository has already proved they move: L40 was a hole from the
day the register was drafted, and ADR-0049 renumbered every row of §21.2
and §21.3 to repair an edit that had shifted them. Any scheme deriving a
vector's name from a row's name inherits that.

The second is provenance. A committed binary is unreviewable: a diff
shows that bytes changed and nothing about intent.

The third is the one that decides whether a vector means anything at
all. Almost no mutation is a single byte, because every field sits under
a covering checksum. Editing `trailer.dir_offset` without repairing
`trailer.crc` yields a file a reader rejects at the CRC — so the vector
evidences `[R-CNT-06]`'s checksum clause while claiming to evidence its
dir-bounds clause. Nothing about the file announces the substitution.

## Decision

- **The tree.** `conformance/vectors/` is a self-contained CC0 subtree:
  the manifest, and one directory per outcome class —
  `conforming/`, `reject-file/`, `reject-layer/`, `reject-tile/`,
  `ignore-record/`. Directories are named for outcomes because
  `[R-CNF-07]` fixes that vocabulary permanently, while section numbers
  renumber. `conformance/tools/` is Apache-2.0 per NOTICE, and holds the
  recipes.
- **Vector identity is an opaque serial** — `TV-0007` — assigned once
  and never reused, never renumbered, never deleted once published. The
  register row is a *field* in the manifest, not part of the path. A row
  that renumbers changes one field; a published path never moves, which
  matters because CC0 exists so third parties vendor these files, making
  every path a compatibility surface.
- **Seeds and recipes are both committed.** A vector is a named seed
  plus a recipe: an ordered list of patches and the checksums to repair.
  Patches address fields **by name** — `layer[bad].index_encoding` — from
  a layout map the builder returns, never by raw offset. An offset in a
  recipe is a restatement of the file's geometry, and restatements drift.
  The binaries are committed too, so an implementer needs no tooling to
  use the corpus.
- **One declared defect per vector.** Every checksum in a vector's file
  MUST verify except those the vector explicitly declares it breaks. A
  build that finds an undeclared checksum failure fails, because such a
  vector tests the covering rule rather than the row it names.
- **Coverage is reported, never failed.** A partial corpus is work in
  progress. `[R-ERR-02]` makes a missing vector a gap in the corpus and
  never a licence to skip the check it would have exercised, and a build
  that failed on incompleteness would tempt exactly the shortcut that
  rule forbids.

## Consequences

Review works on the recipe and CI works on the bytes: a reviewer reads
"patch `layer[bad].index_encoding` to 0, repair the directory and trailer
CRCs", and the manifest's digest proves the committed file is what that
recipe produces.

The isolation rule earned itself on the first nine vectors. Two claimed
tile-scope rows while actually testing the directory CRC, because
`crc_of_crc_array` lives in the layer record and a repaired index
propagates into the directory and then the trailer — a chain no one had
written down. Had the corpus been generated from the design rather than
built against it, every index-touching vector would have carried that
defect while the corpus looked complete.

Priced knowingly: isolation checks *checksums*, which is mechanical. It
cannot tell that a file violates two different structural rules at the
same validation tier — that a patched value is in domain after all, or
that an earlier rule masks the one a vector names. Those need a reader
of the register, and they are why the corpus is reviewed as well as
built.

Opaque serials cost readability: `TV-0137` does not say what it tests,
so the manifest is the only index. That is the trade for paths that
never move.

## Precedent

- ADR-0049, whose repair is the direct evidence that row identifiers are
  positional and must not be load-bearing anywhere else.
- ADR-0046's derivative corpus: the specification is the fixed point,
  and a vector that disagrees is corrected.
- PNG's and WebP's published test suites, vendored wholesale by
  downstream projects — which is what makes a stable path a contract
  rather than a convenience.
