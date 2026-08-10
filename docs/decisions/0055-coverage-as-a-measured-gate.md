# 0055. Coverage is measured against the register, and reported

- Status: Accepted
- Date: 2026-08-10
- Covers: what `tarn_check coverage` asserts; what counts as covering an
  instance; how G5 is declared met; how corpus and specification stay
  bound to each other
- Confirm: none

## Context

`[R-ERR-02]` and `[R-VEC-03]` make coverage the corpus's own normative
claim: every register row has at least one vector per instance it names,
and every sentinel, boundary value and hard limit has one at its bound.
G5 is that claim, demonstrated.

A claim of this shape can be asserted or it can be computed. Asserted,
it decays the moment a row is added — which ADR-0049 has already done
once, and §21.1's completeness clause guarantees will happen again. The
register is a table in a Markdown document, so computing it is cheap:
the same parser the consistency checks already use.

## Decision

- **Coverage is computed from `spec/tarn.md`, never recorded.** The
  checker parses §21.2–§21.5, reads the manifest, and reports rows
  covered against rows present. No count of covered instances is written
  down anywhere, because a written count is a restatement and
  restatements drift — the defect ADR-0049 exists to have repaired.
- **What the checker asserts** — these fail the run:
  - every file the manifest names exists and matches its recorded
    digest and size;
  - every register row a vector cites still exists in the register;
  - every vector carries exactly the defect it declares (ADR-0053).
- **What the checker reports** — these never fail the run: rows with at
  least one vector, instances named against vectors built, and the
  breakdown by outcome class. `[R-ERR-02]` makes a missing vector a gap
  in the corpus and never a licence to skip a check; a build that failed
  on incompleteness would make deleting the row the cheapest way to go
  green.
- **An instance is covered when a vector names it** — the row and, where
  a row names several, which instance. A vector that names a row without
  naming its instance covers the row and no instance.
- **G5 is met when coverage reaches every constructible instance, and
  every unconstructible one carries a recorded reason.** `[R-VEC-03]`
  already concedes one — the tile-count guarantee, whose index region
  alone runs to tens of gigabytes — and the corpus records each further
  concession beside the row it belongs to, with the arithmetic. A gate
  met by silence about what was skipped is not met.
- **Corpus and specification ship together.** The manifest carries the
  corpus version; the binding that is *checked* is the register itself,
  since a vector citing a row that no longer exists fails the run. No
  separate version handshake is introduced, because the failure mode it
  would guard against is the one the row-existence check already catches.

## Consequences

G5 becomes a number anyone can recompute in under a second rather than a
claim in a plan file, and it moves on its own as rows are added: a new
register row lowers coverage without anyone remembering to say so.

The split between what fails and what reports is the substance. Digests,
citations and isolation are facts about artifacts that exist, and a
violation of any of them means something is broken now. Coverage is a
statement about work not yet done, and reporting it keeps the incentive
pointed at writing the missing vector rather than at removing the row
that demands it.

Priced knowingly: coverage counts vectors against instances, and a
vector that names a row can still test the wrong condition. The checker
verifies that a vector's *checksums* isolate its defect; it cannot verify
that the file exhibits the condition the row's prose describes. That
remains a reading task, which is why the corpus is reviewed as well as
computed — and why §21.1's rule that the governing rule wins over the
row's restatement applies to vectors too.

This ADR completes the set G5 needed: ADR-0053 for layout and identity,
ADR-0054 for the manifest and its expectations, and this one for the
gate. ADR-0050 and ADR-0052 already fixed what the tooling may be.

## Precedent

- ADR-0049's repair, which is why no count of the register's size lives
  outside the register.
- ADR-0042's and ADR-0046's shared principle: completeness is the
  normative claim, and the artifact restating it is corrected against the
  document rather than the reverse.
- The consistency checker of ADR-0050, whose parser this shares and whose
  regression test — every historical revision fails, only the repaired
  one passes — is the model for making a gate computable.
