# G3 round 5 — findings and disposition

**Verdict: G3 not met. Two distinct byte-level defects, both
incomplete propagation of the previous round's own fix. One role of
six did not return.**

Six blind fresh-context roles, third distinct partition, standard
unchanged: every report had to carry a discriminator, and every agent
had to attempt refutation first and say what it searched.

| Role | Byte-level | Confidence |
|---|---|---|
| adversary | **0** | medium |
| differential writer | **0** | high |
| hunter §11–§18 | **0** | high |
| hunter §2–§10 | 2 | high |
| hunter §19–§24 + appendices | 1 | high |
| verifier implementer | **did not return** — stalled on all six attempts | — |

Byte-level trend: 5 → 4 → 4 → 3 → **2 distinct** (3 reports, two of
them the same defect found independently).

## The strongest positive result so far

The **adversary could not break it**, and said so explicitly with a
23-attack ledger, each attack paired with the sentence that killed
it. Among the attacks it tried and failed: pointing a live index
entry at superseded bytes ("slack resurrection"); two layer records
sharing one index region; an unknown MU = 0 record's extent falling
outside the coverage classes; a fresh file claiming `generation = 5`;
a zstd tile below the minimum window size; an edge tile made entirely
of padding positions. It also recomputed every fixed constant in the
document and reproduced all of them.

This is the first round in which the role designed to construct
divergence reported that it could not. The **differential writer**
returned zero for the third consecutive round, this time across a
two-commit sequence with byte-shuffle, declared alignment, a sentinel
tile and a superseded tile.

## Defect 1 — the pad's content: MUST be zero, or unconstrained slack

Found independently by two hunters, with the same discriminator:
Appendix A's 128-byte file with bytes [20, 64) set to `AA`. No
checksum covers them, so every gate and both CRCs still pass. One
verifier rejects the file; another certifies it and reports 44 slack
bytes.

The cause is mine. ADR-0048 made slack content unconstrained and
zeroing advisory in §5.2, but six other sites still asserted the old
rule: `[R-CNT-05]`'s "only the **zero** pre-trailer pad … a verifier
MUST treat a violation as a validity error", `[R-LIF-02]` step 5's
"append the **zero pad**", §20.3 step 6, `[R-SEC-04]`'s "caught only
by a verifier's **zero check**", Appendix G's "already mandatory",
Appendix H's "declared-padding content", and §5.1's structure list.
The hunter noted correctly that §21.1's tiebreak could not resolve
it — the conflict was rule-versus-rule, both carrying MUST.

**Fixed** at all seven sites: the gap is slack, a verifier checks
that no *structure* occupies it, and its content is unconstrained.
"Declared padding" no longer appears in the document.

## Defect 2 — which readers are "local"

`[R-CNT-04]`'s definition, added two rounds ago, was circular: a
local reader was "one whose transport delivers the file's bytes from
offset 0 without a separate request", but a `pread`-based reader on a
local disk fetches byte ranges, which is how §6.4 characterises a
*remote* reader. Discriminator: Appendix A's file with the front
magic byte-reversed — an mmap reader rejects it, a `pread` reader on
the same file opens it and reports zero layers, both claiming
conformance.

**Fixed**: the test is now the per-range round trip, which is what the
exemption exists to save. A local reader's transport serves any range
at no per-range round trip; a remote reader's charges one.

## The missing role

The verifier implementer stalled on all six attempts and returned
nothing. It is the role that found two byte-level defects in round 4,
so this round's coverage is incomplete and its clean-ish result
should be read accordingly. Re-running that charter alone is the
cheapest way to close the gap.

## Disposition

Both defects fixed; gates re-run clean; Appendix A still byte-exact.
Nothing deferred.
