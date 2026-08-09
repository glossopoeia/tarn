# 0050. Tooling that checks the specification against itself

- Status: Accepted
- Date: 2026-08-09
- Covers: what code this repository may contain; the scope and limits of
  `conformance/tools/`; which of the specification's mechanical gates are
  automated and which stay human
- Confirm: none

## Context

This specification restates its rules on purpose. A rule appears in its
section, again in the error register, again in a constants table, again
in a conformance checklist. That redundancy is what makes the document
navigable, and it is also where every defect found in cleanroom rounds 4
and 5 lived: a rule changed in one place and left standing in another.
Five rounds of fresh-context review did not catch the register defects
ADR-0049 repaired, because reading finds ambiguity and not bookkeeping.

AGENTS.md permits no implementation code in this repository, with one
exception: tooling for test vectors, landing under `conformance/` with
an ADR noting its scope. That exception has to be drawn carefully. A
reader written here would quietly become the definition of conformance,
which is precisely what ADR-0046 exists to prevent.

## Decision

- **The tool reads and reports; it never writes.** `tarn_check.py`
  parses `spec/tarn.md` and prints findings. It does not edit the
  specification, and no check is auto-fixed.
- **It implements no part of the format.** No reader, no decoder, no
  validator of TARN files. The single place it constructs bytes is
  Appendix A's minimal file, rebuilt from the rules the specification
  states in order to compare against the hex dump the specification
  prints — the one check that cannot be made any other way.
- **Its scope is the specification's own mechanical gates**, in two
  subcommands sharing one parser: `register` (the §21 table's internal
  integrity) and `spec` (identifier discipline, keyword case, retired
  vocabulary, restated constants, Appendix A). A third, `coverage`, is
  reserved for the conformance corpus and shares the same §21 parser;
  it is not written until vectors exist.
- **Stdlib only.** A specification repository that grows a dependency
  tree has acquired a build, and a build is a thing that can break the
  document's checkability. Python 3, no packages.
- **A heuristic warns; a fact fails.** Checks that read prose —
  register completeness above all — report warnings, and their residual
  set is dispositioned in the source with a reason per entry, so what
  the tool surfaces is what is *new*. Checks that compare two stated
  numbers, or recompute a constant, fail the run.
- **The tool is testable against its own history.** `--rev` runs any
  check against a git revision. The regression test is not synthetic:
  every revision from `c75a127` forward fails, the revision immediately
  before ADR-0049 fails with exactly the defects that ADR repaired, and
  only the repaired document passes.

Licensing follows NOTICE unchanged: this is tooling, so Apache-2.0,
carrying an SPDX header. The specification stays CC BY 4.0 and the
future vectors stay CC0.

## Consequences

A defect class that recurred through five cleanroom rounds becomes a
command that runs in under a second, before any vector exists. That
ordering was the point: the register is the corpus's build list, and
generating ~300 files against an unchecked list would have frozen its
errors into the corpus.

The tool earned its scope on its first run by finding a defect the
hand audit behind ADR-0049 had missed — `[R-MTA-09]` names frame
constraints for a user-metadata document under encoding 2, and §21.5
covered only documents whose bytes *fail to decode*. A frame carrying a
content-checksum flag decodes perfectly and was unregistered. §21.5
gains that row, taking the register to 128 conditions over 234
instances.

Priced knowingly. Register completeness cannot be decided mechanically:
the tool matches on outcome vocabulary in a rule's defining paragraph,
which over-reports rules that use the vocabulary without naming a
malformed file. Nine such rules are dispositioned in the source today.
That list is maintenance — a rule that stops belonging on it must be
removed, not silenced, and the tool reports an entry that is no longer
needed. What the tool cannot check at all is whether a row's *prose*
matches the rule it cites; §21.1 resolves that in the rule's favour,
and only a reader can notice it. Two of the defects behind ADR-0049
were exactly that shape.

## Precedent

- PLAN.md §9, which named the mechanical consistency check as one of
  two things that would close G3 better than a sixth cleanroom round,
  the other being the corpus itself.
- ADR-0034's cleanroom protocol, whose complement this is: cleanroom
  agents find ambiguity a machine cannot, and miss bookkeeping a
  machine cannot miss.
- ADR-0046's derivative corpus and ADR-0042's derivative register: in
  both, the document is the fixed point and the artifact is corrected
  against it. A checker is that principle made executable.
