# 0064. A vector names the instance it exercises, by the register's own words

- Status: Accepted
- Date: 2026-08-11
- Covers: how the corpus manifest identifies which §21 instance a vector
  exercises, and how per-instance coverage is measured
- Confirm: none

## Context

§21.8's `[R-ERR-02]` requires one conformance vector per register **instance**,
not per row. The corpus never recorded which instance a vector exercised — a
manifest violation entry carried `row`, `rule`, `outcome`, `scope`, `detector`
and `detected`, and nothing more — so the requirement was unmeasurable, and
`COV-03` reported **row** coverage instead. Its docstring said instances while
its code counted rows.

The consequence was a true statement standing in for a weaker one. G5 read
125/125 at 100% for as long as the corpus has existed, and the criterion the
specification actually states went unchecked. Cleanroom round 7 surfaced it
while repairing §21.1's instance arithmetic, which moved the register from 242
to 252 instances and made the question unavoidable.

## Decision

**A vector names the instance it exercises by the instance's verbatim §21
text.** A manifest violation entry gains an `instance` field whose value is one
of the semicolon-separated entries of its row's Instances cell, copied exactly,
or `—` where the cell names none.

**`COV-05` measures per-instance coverage**, and distinguishes two conditions
that are not alike:

- An instance with no vector **warns**. A partial corpus is work in progress,
  and `[R-ERR-02]` makes a gap a gap, not a licence to skip the check. This
  flips to a failure in the commit that first reaches 100%, so coverage can
  never silently regress afterward.
- A vector naming an instance its row does not list **fails outright**. That
  means the register was reworded and the vector was never rechecked.

Identity is the text and not a position, for the reason ADR-0049 already
settled: row identifiers are positional labels that renumber, and vector
identity must never derive from one. An ordinal index would survive a rewording
that changed an instance's meaning, silently re-pointing a vector at a
condition nobody re-examined. Verbatim text fails loudly instead, and the
failure names exactly the vectors that need a second look.

## Consequences

Coverage is now **236 of 252 instances (93.7%)** across 289 vectors, against a
row coverage of 125/125 that has not moved. Sixteen instances owe a vector;
they are listed by `COV-05` on every run.

The annotation surfaced two mis-filed vectors, both the same defect and both
corrected here under ADR-0046's rule that the spec governs and the vector is
corrected. `TV-0152` claimed **F38** and `TV-0813` claimed **L25**, rows scoped
to the *reserved* type range 0x0003–0x7FFF, while both files carry
*experimental*-range types (≥ 0x8000). §21.6 makes that case a conforming file
a reader nevertheless refuses — `[R-CNT-15]` obliges the refusal and
`[R-CNF-02]` leaves the bytes conforming — so `TV-0152` was additionally
recorded as nonconforming when the specification calls it conforming. Both now
name no register row and ship as positive vectors for §21.6's second exception.
`TV-0910` and `TV-0915` cover F38 and L25 properly, with reserved-range types.

`TV-0813`'s stale comment is worth recording as evidence rather than merely
deleting: it asserted that the vector "carries L25 and nothing else", which was
true of the L25 that existed when it was written. ADR-0057 deleted three rows,
§21 renumbered contiguously, and the citation quietly came to mean a different
condition. That is precisely the failure ADR-0049 predicted, observed in the
wild, and it is the argument for this decision in one example.

Priced knowingly: the manifest grows by one string per violation entry, and
rewording any instance cell breaks the build until its vectors are
re-annotated. That cost is the mechanism. A coverage claim that survives a
change to what it measures is not a coverage claim.

## Precedent

- ADR-0049, which established that vector identity never derives from a
  positional row label; this applies the same rule one level down.
- ADR-0046, under which the specification governs and a disagreeing vector is
  corrected — the authority for re-filing `TV-0152` and `TV-0813`.
- ADR-0055, which made coverage a measured and reported quantity rather than an
  asserted one. This supplies the measurement it named.
