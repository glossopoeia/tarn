# 0112. Seven defects in ADR-0111's own text, and an audit that lost power partway

- Status: Accepted (resolves the ADR-0110/ADR-0111 audit)
- Date: 2026-08-31
- Covers: §9.3's two new Notes and its body; §9.6's rollback caution; §20.3
  step 6; §20.5's compaction paragraph; §21.7's citation; §23.2's disclosure
- Revises: six passages ADR-0111 wrote and one it left stale
- Confirm: none

## Context

ADR-0110 and ADR-0111 were audited together over 29 spec hunks and a 445-line
tools diff, findings-only with no verification cap. Eight auditors ran: five over
disjoint hunk groups, one on the code, a cross-hunk pass, and a downstream pass.

**Seven distinct defects, none byte-level.** Every one is in text ADR-0111 wrote,
and every one was checked against the document by hand before repair.

**The audit's coverage is uneven and this ADR records that rather than hiding
it.** Seven of the eight auditors failed on the primary model with a service-side
error and were re-run on a smaller one. **Five of those seven returned zero
findings** — layout, register, periphery, tools, writer — while the single
auditor that completed on the primary model found six defects in the same text.
Two auditors on the fallback found one apiece: a duplicate of a defect the first
had already found, and one citation slip. **Five empty returns from a weakened
instrument are not evidence that five groups are clean**, and §6.2's table, §21's
counts, Appendix A's dump and the tool changes should be treated as unaudited
until a healthy pass covers them.

## Decision

**Six of the seven are the same failure in different clothes: a sentence carried
across to a new quantity without re-deriving it.**

**§9.3's ceiling Note named a length no conforming file can hold.** It said F is
a u64 under `[R-ENC-03]`, so F ≤ 2⁶³ − 1, and "a file at that ceiling admits no
further commit". But `[R-CNT-06]` also requires F to be a multiple of 64, and
2⁶³ − 1 is odd. The reachable ceiling is **2⁶³ − 64**. The sentence's previous
form was tight for `generation`, which carried no such side constraint; re-keying
it onto F silently dropped one. Two auditors found this independently, on
different models — the widest convergence in this audit.

**§9.3's revalidation Note inferred file identity from `file_id`.** It concluded
that "a matching (file_id, F) pair names the same committed prefix a cache
already holds" from the premise that no two commits *of one file* share an F. The
step from one file to one `file_id` needs `file_id` uniqueness, which is a
**SHOULD** — and the same requirement's own parenthetical warns that "a
predictable or reused file_id lets two distinct files collide in the (file_id,
range)-keyed caches this rule licenses, serving bytes from the wrong file". The
Note now binds its conclusion to the premise it has, and names the reused-file_id
case as what defeats the contract without any violation.

**§9.6 offered as a defence the thing it had just refuted.** Two sentences after
showing that an expected committed file length is no substitute — a party that
truncates and re-appends reaches any F at or above the expected one — it listed
"a signed (file_id, committed_file_length) pair held elsewhere" among the state a
file cannot manufacture. Signing pins the value; the value is exactly what the
re-append reproduces. The item is struck and the reason stated, leaving the
detached hash over the committed prefix and the append-only transport, which do
survive the attack.

**§20.5 overstated the loss.** It said a compacted file and a file appended to a
hundred times "are indistinguishable by their trailers alone", while §23.2 — in
the same commit — says the commit count is recoverable by probing backward for
superseded trailers and is "absent altogether from a compacted file, which
retains no earlier trailer to find". The two are distinguished *precisely* by
their trailers; what is indistinguishable is their **live** trailers, and the
sentence now says so.

**§20.3 step 6 restated the growth short.** `[R-LIF-02]` states the bound as "by
at least 128"; step 6, which is where an appender actually reads its obligations,
said only "necessarily above the F step 1 established". Its justification also
named "a pad" among what the commit appended, where §6.2 says "a writer that ends
its directory on a 64-byte boundary leaves none". The magnitude is restored and
the pad dropped; the conclusion holds on the directory and trailer alone.

**§21.7 cited the rule that consumes the growth, not the one that states it.**
ADR-0111 reworded the entry from "the generation sequence" to the strict growth
of `committed_file_length` and carried `[R-LIF-03]` forward. Under the old text
that was right: §9.3 stated the counter's increment. It is now stated in §9.2
under `[R-LIF-02]`, and the citation follows it.

**§23.2 was written relative to the diff.** "What the file **no longer** states
is how many commits produced it" has no referent in a published specification —
no longer than what? The sentence now describes the format: no field carries a
count, so the number follows only from the backward probe.

## Consequences

The register does not move: 120 conditions, 275 instances, 329 vectors, coverage
120/120 and 275/275, Appendix A still byte-identical to the builder's
reconstruction. No propagation acknowledgement was needed. Every repair is prose;
none touches a field, an offset or a count.

**What the audit shows about ADR-0111, and it is not comfortable.** That change
was planned by six agents, cross-checked by a seventh that verified all 49
anchors and recomputed every number, applied one edit at a time with each seam
rendered, and passed five gates. It still shipped seven defects, six of them the
same shape: **a sentence whose truth depended on a property of the quantity it
described, re-pointed at a quantity with different properties.** The ceiling, the
identity inference, the rollback token, the "trailers", the growth restatement —
each was true of what it used to describe.

**The mechanical checks cannot see this class.** `tarn_propagate` finds a rule
that moved and left a restatement behind; every one of these was written *with*
the change and was wrong on arrival. Only a reader comparing the new sentence
against the properties of its new subject finds them, which is what the repair
audit is for and why ADR-0081 put it before the round rather than after.

**On the instrument.** A repair audit that loses five of eight lanes is worth
less than its finding count suggests, and the honest response is to say which
lanes are unestablished rather than to report seven findings as a sweep. The
model fallback is recorded in `scratch/cleanroom/README.local.md` with the
failure signature, since it is now the second cycle in which it has bitten.

## Precedent

- ADR-0110's relation to ADR-0109, and ADR-0107's to ADR-0106: an audit of a
  repair batch, recorded as a revising ADR rather than as an edit to the ADR it
  corrects.
- ADR-0099's re-keying defect and ADR-0106's rule that a repair which generalises
  needs a new rule's derivation — here applied to six sentences that were
  re-pointed rather than re-derived.
- ADR-0106's own lesson about a starved audit: the cap must scale with the diff,
  and where it cannot, the shortfall is named.
