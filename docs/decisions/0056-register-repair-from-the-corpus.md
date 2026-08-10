# 0056. Five register defects the corpus found

- Status: Accepted
- Date: 2026-08-10
- Covers: the unknown-record-type rows and the missing reserved-range
  violation; the vacuous coverage row; two instance-cell miscounts; the
  value-domain rows that contradict §21.1
- Confirm: none

## Context

PLAN.md §9 predicted that the conformance corpus would catch defects a
sixth cleanroom round would not, because *"a vector encoding the wrong
verdict is exactly how a stale restatement gets caught."* Building 229
vectors produced five, and the mechanism was the one predicted: a vector
forces a yes-or-no answer where prose stays comfortably ambiguous.

The sharpest was self-announcing. Two vectors came out **byte-identical**
— the same 448 bytes emitted once as a violation of a register row and
once as a conforming file. A corpus cannot ship both.

## Decision

**A — Unknown record types are split by range.** `[R-CNT-15]` names
three cases and the register captured them backwards: it gave rows to the
two that leave a file conforming and none to the one that does not.

- The row *"An unknown record type carries MU = 0"* is **deleted** from
  §21.5. §21.6's table already carries the identical condition as a
  defined behavior, and `[R-CNT-15]` agrees with §21.6: this *"governs a
  reader's treatment, not the file's validity."*
- Two rows are **added**, one at file scope and one at layer scope, for
  the violation that had none: a type value from the **reserved** range,
  whose emission `[R-CNT-15]` makes a violation whatever its MU bit,
  detected by a verifier at the record's governing scope.
- The unassigned-type-with-MU-=-1 row **narrows to the reserved range**,
  so that every row in §21.2 describes a nonconforming file. The
  experimental-range case joins §21.6's closing paragraph beside
  version_major, where a conforming file is refused because of a reader's
  capability rather than a defect in the bytes.

**B — The vacuous coverage row is deleted.** *"A byte of the live
committed state is claimed by no coverage class"* cannot be exhibited:
§5.2 defines the live committed state as the front block plus what the
coverage walk reaches, and `[R-LIF-08]` makes every byte the walk misses
slack. There is no third category. §5.2 gains a note recording that
`[R-CNT-02]`'s covering half is therefore trivially satisfied and only
its disjointness half is testable, so the row is not re-added by someone
reading the rule in isolation.

**C — A conjunctive predicate is one instance.** The unassigned-type row
listed `type; flags bit 0` — the two fields of one conjunction, which
§21.1 excludes: *"no two files could differ."*

**D — `file_id` has no detectable byte-reversal.** The endianness row
qualifies itself as *"detectable only through that field's own value or
range gate"*, and §6.2 gates `file_id` on `≠ 0` alone. Byte reversal is a
bijection preserving nonzero-ness, so the instance fails the row's own
premise and is removed.

**E — Value-domain rows enumerate their alternatives.** Eight §21.3 rows
read `—` while their condition text names two to four ways to miss the
domain. §21.1 counts *"one of several alternatives the condition text
states"* as an instance; the cells now say so, as §21.5's already did.

The register is **128 conditions over 248 named instances**.

## Consequences

The one genuine violation among the unknown-type cases gains the rows it
never had, and the register stops describing conforming files as
violations except where §21.6 explicitly says why.

Renumbering moved 56 row identifiers. Because ADR-0053 made vector
identity an opaque serial and the register row a *field*, that cost one
mechanical remap of the corpus's citations and no renamed file — which is
the property that decision was bought for, tested for the first time.

Priced knowingly. Deleting the coverage row narrows what a verifier is
told to check: `[R-CNT-02]` still says the live state partitions, and a
verifier may still assert both halves, but only one can fail. The
alternative was keeping a row whose vector could never be built, which
`[R-VEC-03]` would then count forever as a gap.

The instance total rose by 14 while row count held, so the corpus's
coverage percentage fell without any vector being removed. That is the
gate working as ADR-0055 intended: coverage is computed from the register,
so a repair that finds more to test lowers the score honestly rather than
leaving it flattering and stale.

## Precedent

- ADR-0049, the same defect class found by a different instrument. That
  one came from a mechanical recount; these came from files that had to
  be one thing or the other.
- ADR-0042's principle, applied twice over: where a row and the rule it
  cites diverge, the rule governs — which is how `[R-CNT-15]` settled A
  and `[R-LIF-08]` settled B.
- PLAN.md §9's claim that the corpus and the consistency checker are
  complementary instruments. The checker found ADR-0049's defects and
  could not have found these; the corpus found these and could not have
  found those.
