# 0100. The audit-chain invariant becomes mechanically checkable, and is corrected

- Status: Accepted
- Date: 2026-08-25
- Covers: `conformance/tools/tarn_chain.py`; the invariant ADR-0097 recorded
- Revises: ADR-0097's statement of the invariant, which is too strong as written
- Confirm: none

## Context

ADR-0081 put a repair audit in front of every cleanroom round, because for four
consecutive rounds the defect the next round found was in the immediately
preceding round's repair. The instrument works. Nothing tracked whether it ran.

ADR-0095's diff was skipped entirely — the sequence went 0093 audited, 0094
audited, 0095 missed, 0096 audited — and was found only by walking the chain by
hand, weeks of cycles later. ADR-0097 recorded the failure, named the invariant
behind it, and observed that it is checkable from git. That observation has sat
unactioned since, which is the same shape as the gap it describes: a check
identified but not built is a check that does not run.

`SPEC-03`'s blind spot was closed the same way and is the model. The measurement
there was one cell wide and pointed at the document's most defect-prone passage;
nobody would have found it by reading.

## Decision

**The check lands as `conformance/tools/tarn_chain.py`**, alongside
`tarn_propagate.py`, which it complements: propagation asks what a change left
behind in the document, and this asks whether the change was read by anything at
all.

**The invariant is corrected.** ADR-0097 states it as "every commit touching
`spec/tarn.md` between two charters appears in some audit's range." Run
literally over the history, that reports two false positives. ADR-0092 landed
two minutes before round 24's charter and ADR-0097 one minute before round 25's;
neither was audited, and neither is a gap. **A repair committed just before a
charter is handed to the round rather than to an audit**, and the round is the
stronger of the two readings — fresh context over the whole document against one
auditor over a diff. Round 25's charter says so in terms: auditing every repair
of every repair does not converge, and a fresh reading is what the round is for.

So the invariant is a disjunction — every commit touching the specification is
covered by some audit's range, **or** it is followed by a charter, whose round
read it — and it collapses to something sharper than either half:

> **The only commits that can violate it are those after the most recent
> charter.** Those have no round coming to read them, so an audit must.

That open interval is what the tool checks by default, and it is exactly the set
the next charter closes. Coverage is decided on payload containment: a commit's
added and removed lines, whitespace-normalised, wholly inside one committed
audit artifact. Coverage spread across two artifacts is reported as partial and
does not satisfy the invariant, because no auditor read the commit whole.
Artifacts still uncommitted in the working tree count, since the audit for the
most recent repair is normally still there at the moment the answer matters.

## Consequences

Run over all 84 commits that have touched `spec/tarn.md`, the corrected
invariant holds throughout, with exactly one commit outstanding: ADR-0099's
repairs, which is the interval this cycle's audit closes. The tool therefore
reproduces by construction the state the chain was hand-checked into, and would
have reported ADR-0095's skip the day it happened.

What it does not do is judge an audit's quality. An artifact covering a commit
satisfies this check however thin the reading behind it was, exactly as an
acknowledged pair in `propagation-acks.txt` is a judgement on the record rather
than a proof. It answers "did anything read this", which is the question that
was going unasked.

The reader-side obligation: a run exiting 1 before a charter is committed means
the charter is about to hand a round a repair nothing has checked, and the audit
is owed before the launch, not after.

## Precedent

- ADR-0097's own closing observation, that the invariant is mechanically
  checkable from git and worth closing the way `SPEC-03`'s blind spot was. This
  ADR takes it up and corrects its statement.
- ADR-0081, which established that a repair audit and a cleanroom round find
  different classes of defect — the fact that makes the disjunction sound rather
  than a loophole.
- `tarn_propagate.py`'s acknowledgement file, whose discipline this follows: a
  mechanical check whose exceptions are recorded judgements rather than silence.
