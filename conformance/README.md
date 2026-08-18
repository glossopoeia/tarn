# Conformance

This directory holds the conformance test-vector corpus and the tooling
that maintains it. Today it holds only the tooling: the corpus is gate
G5, and its structure is not yet decided.

## What is here

```
conformance/
  tools/
    tarn_check.py      mechanical consistency checks for spec/tarn.md
    tarn_propagate.py  what else restates the rule a change touched
```

## Running the checks

```bash
python3 conformance/tools/tarn_check.py
```

No dependencies — Python 3, standard library only. Subcommands:

| Command | Checks |
|---|---|
| `tarn_check.py register` | §21's error register: row-id contiguity, duplicate conditions, governing rules resolving, every stated count agreeing with the table, the detector/detection-point invariant, and a completeness heuristic over the requirement identifiers |
| `tarn_check.py spec` | Identifier discipline (§2.2), BCP 14 keyword case, retired vocabulary, Appendix B's restated constants, and Appendix A's hex dump rebuilt from the specification's own rules |
| `tarn_check.py` | Both |
| `tarn_propagate.py` | What a *change* leaves behind. For each changed hunk in `spec/tarn.md` it extracts the rule's anchors — the requirement ids and register rows it cites, the field names it uses, the terms it emboldens, its distinctive phrasing — and reports every other passage carrying enough of the same anchors that was **not** changed with it. Exits 1 on an unswept site unless the pair is recorded in `tools/propagation-acks.txt` with a reason. |

Run `tarn_propagate.py` before every commit that touches `spec/tarn.md`. Every
byte-level defect found since round 7 has been one rule repaired in one place
and left standing in another; `tarn_check.py` checks the document against
itself at rest, and this checks a change against the document.

    python3 conformance/tools/tarn_propagate.py            # working tree vs HEAD
    python3 conformance/tools/tarn_propagate.py --rev <sha> # what that commit should have swept


`--rev <commit>` checks a git revision instead of the working tree,
which is how the tool is regression-tested: every revision from
`c75a127` forward fails, and only the post-ADR-0049 document passes.

Exit status is 0 when nothing fails. Warnings never fail the run —
they mark checks that read prose, where a human decides.

## What the checks do not cover

They compare the document against itself. They cannot tell whether a
register row's prose matches the rule it cites — §21.1 resolves that
in the rule's favour, and noticing it takes a reader. Two of the
defects ADR-0049 repaired were exactly that shape, and the cleanroom
protocol (ADR-0034) remains the instrument for them.

## Scope and licensing

ADR-0050 fixes what this tooling may be: it reads the specification and
reports, implements no part of the format, and adds no dependencies.
Under [NOTICE](../NOTICE), code here is Apache-2.0; the specification is
CC BY 4.0; the vectors, once they exist, will be CC0 so that using them
imposes nothing on an implementation.
