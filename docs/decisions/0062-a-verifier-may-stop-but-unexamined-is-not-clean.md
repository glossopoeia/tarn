# 0062. A verifier may stop, but unexamined is not clean

- Status: Accepted
- Date: 2026-08-11
- Covers: how much of a file a verifier must check, and what its report must say
- Confirm: none

## Context

`[R-CNF-11]` gives a verifier three verdicts — *conforming*, *nonconforming*,
*cannot establish* — and says nothing about how much of a file it must walk to
reach one. Cleanroom round 6 asked whether a verifier may stop at the first
violation.

Either answer alone is wrong. Requiring exhaustive enumeration puts unbounded
work on a hostile file, and §21.9's limits bound a reader's resources rather than
a search. Permitting an early stop with no further obligation lets a report
naming one violation be read as *"there is one violation"* — which sends an
operator to fix one field and re-run straight into the next.

## Decision

**A verifier MAY stop at the first violation.** *Nonconforming* is a verdict,
not an inventory, and nothing obliges a verifier to enumerate.

**A verifier that stops MUST report the scopes it did not examine as
*unexamined*, distinct from examined-and-clean.** Silence about a scope
otherwise asserts that the scope was checked. A verifier that halts at a
layer-scope violation in layer 3 and says nothing about layers 4 and up has not
found those layers clean, and its report must not read as though it had.

*Unexamined* is not a fourth verdict, and it is not *cannot establish*. Cannot
establish names a requirement the verifier was unable to check (`[R-CNF-11]`);
unexamined names a scope it chose not to reach. A file whose verdict is
*nonconforming* stays nonconforming however much went unexamined — the marking
constrains the report, not the verdict.

## Consequences

The obligation lands on a verifier's output, so it costs a stopping verifier one
field per unreached scope and costs an exhaustive verifier nothing. It gives two
verifiers' reports a common floor without making them identical: a report becomes
readable as a claim about what was checked, not only about what was found.

The corpus already depends on this distinction from the other side. §24's
`[R-VEC-02]` records that a vector built for one row may exercise others, and
that where conditions cannot be isolated — §6.2's field gates are validated
together — the entry names every row the file exercises. Coverage and
verification meet the same fact, that reaching a scope and finding it clean are
different claims, and this makes both sides say so.

Foreclosed: a conformance report that is silent by default. A verifier may still
be terse; terseness now has to name its own boundary.

Priced knowingly: this specification does not fix a report format, and does not
start here. It requires that the distinction be expressible and expressed, and
leaves how to say it to the implementation, exactly as §2.4 leaves how a failure
is reported to implementation technique.

## Precedent

- §21.1's instance-counting rule, which already separates a condition from the
  instances that can exhibit it; this applies the same separation to what a
  verifier reports having visited.
- JSON Schema's standardized output formats, where *flag* and *verbose* are
  distinct declared modes rather than one implementation's terseness — the
  declaration, not the mode, is what this decision borrows.
- ADR-0042, under which the register is derivative and per-violation: a report
  that hides its own coverage would make that register unusable as evidence.
