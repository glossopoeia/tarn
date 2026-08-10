# TARN conformance vectors

CC0 1.0 Universal. Vendor these files freely; using them imposes nothing on
an implementation.

The corpus is **derivative evidence**, never a definition of conformance:
where a recorded expectation and `spec/tarn.md` disagree, the specification
governs and the vector is corrected (§24, ADR-0046).

## Layout

`manifest.json` records every vector. Files are grouped by the outcome a
reader owes, because `[R-CNF-07]` fixes that vocabulary permanently while
section numbers renumber:

    conforming/      files a reader must accept
    reject-file/     reject-file/  reject-layer/  reject-tile/  ignore-record/

## Reading an entry

`conforming` is a property of the bytes. `violations` lists the register rows
the file exercises. `expect` is a pair, not a verdict:

- `must_not_serve` — scopes no reader may return data from
- `serves` — the content a reader that returns anything at all must return,
  with every value as a hexadecimal bit pattern so no comparison depends on a
  number formatter
- `may_escalate_to` — the wider scope a reader is permitted to refuse instead

A reader that rejects a nonconforming file entirely **passes**, because
`[R-CNF-12]` permits it; it is recorded as *scope untested*. A reader that
reads the intact sibling and refuses only the damaged scope is *scope
verified*. ADR-0054 states the pass/fail algorithm in full.

## Regenerating

    python3 conformance/tools/tarn_vectors.py --emit
    python3 conformance/tools/tarn_check.py coverage

Every vector is a seed plus a recipe — a named field, a value, and the
checksums to repair — and the build refuses to emit a vector carrying any
undeclared checksum failure, since such a file tests the covering rule rather
than the row it names.
