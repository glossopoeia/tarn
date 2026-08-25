# 0099. §11.1 states its rule by `entry_count`, and `[R-SLB-03]` loses the pronoun

- Status: Accepted (resolves the ADR-0098 audit)
- Date: 2026-08-25
- Covers: §11.1's growth Rationale; `[R-SLB-03]`'s contiguity clause; §13.3's
  sparse-writing Note
- Revises: two repairs ADR-0098 wrote
- Confirm: none

## Context

The audit of ADR-0098's four corrections lost **two of its three auditors** to
connection errors mid-response. Both had written complete transcripts — 42 KB
and 26 KB — and both were recovered from disk with their findings intact. The
surviving cross-hunk auditor independently reached the same conclusion as one of
them.

**The audit also found a defect in the audit's own inputs.** My hunk builder
mislabelled two of four headers: `hunk-01` was described as §11.1's Rationale
while its body is §9.6, and `hunk-02` the reverse. All three auditors worked
from the bodies rather than the headers, and one flagged the swap explicitly and
warned that an auditor trusting the headers would mis-site both. No finding was
affected. The bug is mine — the location map was keyed by index against hunks
git had ordered by line number.

**Two of ADR-0098's four repairs were wrong, and in the same two ways this week
has repeatedly produced.**

`L41`'s pronoun was disambiguated **in the row and not in the rule**. §21.1
says: "where a row and the rule it cites diverge, **the rule governs**."
`[R-SLB-03]` still read "each stored tile's offset equals the previous stored
tile's offset plus **its** length" — the identical ambiguity — so the row's fix
was overridden by the rule it restates. Three auditors found this
independently.

§11.1's Rationale gained an **exception clause**, and the exception then had to
be replicated in three further places or contradict them. The trailing
appositive in its own sentence — "the first growth of a zero-extent layer
included" — was falsified by it: a rank-2 layer at E = (0, 0) growing to
(50, 0) has G = (5, 0), `entry_count` stays 0, and §15 says at `entry_count` = 0
"there is no region at all", so nothing is re-emitted while the clause says it
is. §13.3's Note asserted the unexcepted claim, and §20.3's shrink clause its
mirror.

That is ADR-0095's lesson recurring: **a claim patched with an exception is a
list by another name.**

## Decision

**§11.1's Rationale states the rule by the quantity that decides it.** Growth
that leaves `entry_count` unchanged touches the directory alone — a growth
raising one grid count while another stays 0 among them, the product holding at
0. Growth that changes `entry_count` changes `extent_length` with it, so the
region is re-emitted and ordinals renumber. The partition is exhaustive by
construction, needs no exception, and makes the trailing case precise: the
growth that raises a zero-extent layer's **last** zero grid count.

**`[R-SLB-03]` says "that previous tile's length".** The fix belongs in the rule,
which governs; L41's row wording, corrected by ADR-0098, now matches it.

**§13.3's Note keys on `entry_count` changing** rather than on growth "across a
grid boundary".

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors.

One propagation acknowledgement. §5.1's Note keys on "a layer's stored-tile set
or index content" — the formulation §20.3 step 4 uses normatively — and was
already correct without an exception, since unchanged `entry_count` with
unchanged entries is unchanged index content. It is the model §13.3 was moved
toward.

**On recovering two dead auditors.** Both transcripts were complete. The
standing rule — read the failures line, then recover from disk — has now paid
out four times this week: round 25's verifier walk, and both of these. A
connection error is not lost work, and an audit reporting five of seven agents
is not an audit that found less.

**On the hunk-header bug.** No check catches it: the headers are prose in a
scratch file, invisible to `node --check`, to the constant evaluation, and to
the parity scan. What caught it was an auditor reading its inputs critically and
disclosing the discrepancy — the same instrument that caught the path-name leak
two days ago. Charter agents to distrust their own inputs and they will.

## Precedent

- §21.1's "where a row and the rule it cites diverge, the rule governs", which
  is why a register-row repair that leaves the rule alone is not a repair.
- ADR-0095's rule about closed counts, applied here to its near relative: a
  claim carrying an exception, where the property that decides the claim was
  available all along.
- ADR-0084's disclosure paragraph, which has now surfaced a fourth distinct
  defect class — this time in the audit's own inputs rather than in the
  document.
