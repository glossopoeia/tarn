# 0097. Two glosses, F33's row list, and §23.1's superseded extent

- Status: Accepted (resolves the ADR-0096 and ADR-0095 audits)
- Date: 2026-08-25
- Covers: L16's and F31's gloss; F33's carve-out row list; §23.1's account of a
  record extent
- Confirm: Q-C6 records the half of `X-04` this does not decide
- Confirm: none beyond that

## Context

Two audits ran. The first read ADR-0096's two register-cell edits; the second
read **ADR-0095, a diff the chain had skipped** — the audit sequence had gone
0093 → audited → 0094 → audited → 0095 → *(missed)* → 0096, because the
disposition instruction was followed without re-checking the invariant behind
it. That is the same failure shape as ADR-0094's menu, one level down.

**ADR-0095's rewrite held.** Twelve findings, three self-flagged byte-level,
**eleven refuted and one partial, none confirmed.** The auditor attacked §23.1's
exhaustiveness claim directly — trying new structures, partly-superseded
structures, and unnamed operations — and could not construct a third case. It
found that §5.2's `[R-CNT-02]` supplies a *stronger* warrant than the one
ADR-0095 chose: every byte is live-claimed or slack, so the dichotomy holds over
bytes rather than over structures.

**The refute pass had to run twice, and the reason is recorded here because no
existing check could have caught it.** The finding briefs were written to a
directory named `refute/` while the workflow's charter still named `finish/`
from the harness it was copied from. Every agent's charter therefore pointed at
a file that did not exist; each ran `find`, located it, and in doing so read a
path segment naming the expected disposition. All four disclosed it unprompted,
and one stated the risk exactly: it could bias toward REFUTED — which is what
all three refuters returned. The pass was re-run with briefs under a neutral
`case/` directory and transcripts written as `analysis-*.md`. **The second look
returned identical verdicts with no contamination disclosed**, so the outcome
was sound; the leak was harmless this time and is not thereby acceptable.

`node --check`, the constant-evaluation check and the backtick-parity scan are
all blind to this class. **A path name is part of an agent's context**, and only
the mandatory disclosure field surfaced it — the third distinct leak that field
has caught, after the injected notes index and the environment block's commit
subjects.

## Decision

**L16 and F31 say "pointing into" the front signature block, not "placing the
extent inside" it.** ADR-0096 changed L16's bound *and* its gloss, importing
F31's wording; the audit confirmed that gloss is false for any extent longer
than the block's 16 bytes, which a layer record's tile-index region routinely
is. L16's original wording was the accurate one. The fix reaches F31, which had
carried the defect since it was written.

**F33 names the half-zero rows.** F33 is the only passage in the document that
cites L16, and its carve-out routes a front-block-reaching claimant to F31/F32
and L16/L17. A record extent slot of (0, N) reaches the block through its zero
offset and is caught by F30 and L15, which F33 did not name — a hole that
already existed on the file tier before this cycle. F33 now names them and says
why.

**§23.1 names the superseded record extent.** Its account covered a *dropped*
ancillary record's extent and not a *superseded* one, of which the user-metadata
document is the privacy-relevant case: §20.3's shape (c) states that editing
metadata appends a new extent and strands the old one. The section now says so,
and says it is the case most likely to strand content a caller believes it
deleted.

**What this decision does not settle.** `[R-PRV-01]`'s MUST NOT still reaches
only *sample data*, so a tool may report a metadata edit as a deletion without
breaking it. Widening a MUST NOT changes what a conforming actor may do, and
ADR-0091's rule governs: a repair that must decide a rule's reach is a decision.
It becomes **Q-C6**, with three options priced.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. Neither
gloss edit changes a condition's extension, and F33's addition names rows that
already registered the case.

**On the audit chain.** The skipped diff was found by checking the chain rather
than by any tool — nothing in the harness tracks which diffs have been audited.
That is a gap worth closing the way `SPEC-03`'s was: the invariant is that every
commit touching `spec/tarn.md` between two charters appears in some audit's
range, and it is mechanically checkable from git.

## Precedent

- ADR-0094's lesson about sweeping before deciding, applied here to the chain
  itself rather than to a question.
- ADR-0084's disclosure paragraph, which has now surfaced three distinct
  contamination channels, none of which any mechanical check could see.
- `[R-CNT-02]`'s live-claimed-or-slack partition, which the audit identified as
  the warrant ADR-0095 should have cited.
