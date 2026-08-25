# 0092. R8's warrant is removed rather than replaced, and three clauses are corrected

- Status: Accepted (resolves the ADR-0091 re-audit's confirmed findings)
- Date: 2026-08-24
- Covers: R8's condition cell; §21.7's `[R-WRT-06]` reason and its filter clause;
  §21.2's restatement of `[R-CNT-04]`
- Revises: three claims ADR-0091 wrote; corrects one pre-existing overclaim
- Confirm: none

## Context

The re-audit of ADR-0091 — itself a repair of ADR-0090's repairs — returned
**18 findings, none byte-level at any stage.** Verification gave 5 CONFIRMED,
1 PARTIAL, 5 REFUTED, with 7 unverified under the per-auditor cap, so the
confirmed list is a floor. **Four of the five confirmed defects were in
ADR-0091's own repairs.**

That is the third consecutive cycle in which a repair pass introduced roughly
as many defects as it fixed, and the honest reading is that these passes have
been net-negative on two passages: §21.7's account and R8's cell.

**R8 is the clearest case, and it decided this cycle's method.** Round 23's
register hunter reported that R8 collapses two alternatives `[R-MTA-04]` states
disjunctively. Two attempts to justify the collapse have now both been wrong:

- ADR-0090 cited "§21.1's distinguishability test". §21.1 states no such test.
- ADR-0091 cited `[R-VEC-02]` as a limit barring the instance. `[R-VEC-02]`
  says the opposite — "where a condition cannot be isolated … the entry
  **records every row the file exercises and says which it was built for**".
  It accommodates non-isolable conditions rather than excluding them.

ADR-0091 stated the rule that should have prevented this: *a repair that must
invent a warrant is a decision, not a repair.* It then violated that rule twice
in its own commit.

## Decision

**R8's warrant is removed, not replaced.** The condition cell keeps the useful
half — naming what "in any form" covers, an overflowing magnitude and the bare
tokens — and claims nothing about why they are one instance. Inventing a third
warrant is exactly what the last two cycles show does not work.

The underlying question becomes **Q-I4**, with the two failed arguments recorded
so nobody repeats them, and three options priced: split to four instances with
each new vector co-attributed to R7 under `[R-VEC-02]`'s own clause; keep two
with a ground that survives an audit, which nobody has produced; or state a
general rule in §21.1 about conditions whose second alternative cannot be
exhibited alone, which would also close L50's held fourth instance.

**§21.7's `[R-WRT-06]` reason gives one shared ground, then a second for two.**
ADR-0091 gave two reasons for all four obligations and then said two of them
were unwitnessed "twice over", which cannot both be true. All four now rest on
one ground — the output carries no record that it is a compaction output at
all, so no check can know any of the four was owed — and the ignore-lane bits
and version_minor floor carry a second, the input's flags and minor being
unrecorded too.

**§21.7's filter clause names the rows T26 names.** ADR-0091 claimed to state
"the same terms T26 states" and then named T2, T4 or T5 where T26 names T2's or
T4's. The clause now quotes T26's own formulation.

**§21.2 states `[R-CNT-04]` with its condition.** This one is *not* from a
recent repair — it is pre-existing text. The preamble said the front-block check
is what `[R-CNT-04]` "places before other processing", full stop. The rule is
conditional: a reader already holding bytes [0, 16) MUST verify before other
processing; one that would have to issue a further range request MAY defer or
omit. The qualification is now stated.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors.

**Not repaired, and deliberately.** `A-01` and `A-02` were refuted — the F5
revert does not leave a hole, and §21.2's "ahead of every check" reading
survived attack. `X-01` and `X-02` were refuted on the §20.5 "Neither" pairing.
`B-03` was refuted. Seven findings were unverified under the cap and are
recorded in the round-24 audit artifacts rather than acted on.

Two propagation acknowledgements recorded, both for phrase-level matches on the
register's cause-row idiom rather than for any restated rule.

**What three cycles of this establish.** The repair audit works: it caught every
one of these before a fresh-context round read them, which is its whole purpose.
What does not work is answering a register-bookkeeping finding with an argument
composed in the same sitting. Where a finding asks *why* a row is shaped as it
is, and the answer is not already written down somewhere that survives being
checked, the finding belongs in the ledger.

## Precedent

- `[R-VEC-02]`'s non-isolable clause, read correctly this time, which is what
  makes Q-I4's option (a) buildable rather than barred.
- T26, whose formulation §21.7 now quotes instead of paraphrasing.
- `[R-CNT-04]`'s own conditional, which no repair introduced and which had gone
  unstated in §21.2 since it was written.
