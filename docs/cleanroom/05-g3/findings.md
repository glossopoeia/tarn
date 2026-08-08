# G3 round 5 — findings and disposition

**Verdict: G3 not met. Three distinct byte-level defects across the
round and its re-run — all three in text this project had recently
written or amended.**

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

## The missing role, re-run

The verifier implementer stalled on all six attempts and returned
nothing — the role that found two byte-level defects in round 4. It
was re-run afterwards as two independent agents against the amended
text: **A** on the original four-commit trace (slab cleared mid-life,
first-axis extent grown, unknown `MU = 0 / PE = 0` record dropped),
**B** on the specification of certification itself — every
verifier-only check and whether it is decidable from bytes alone,
every reported figure and whether two verifiers must agree on it, and
every place the verifier's obligations are stated twice.

**B found nothing.** **A found one**, in text this project wrote:
§20.4's `MU = 0 / PE = 0` drop licence was **circular**. An appender
could drop such a record "only in a commit that modifies the scope
the record attaches to" — but §20.4's own MU = 1 row defines
file-scope modification as "adding, removing, or reordering top-level
records", so dropping the record *is* the modification that licenses
dropping it. The precondition satisfied itself, making the
restriction inoperative.

**Fixed**: the change must be independent of the drop — for a layer
sub-record, that layer's record, index, or stored tiles; for a
top-level record, the file's layer set or another top-level record —
and a commit whose only effect would be the drop MUST retain it.

Both agents produced complete certification procedures. A's is a
41-row dependency-ordered table marking every verifier-only row, with
the reported figures and their computations — including the slack
total as `F − claimed bytes`, which is the figure ADR-0048 made
mandatory.

## Disposition

Both defects fixed; gates re-run clean; Appendix A still byte-exact.
Nothing deferred.
