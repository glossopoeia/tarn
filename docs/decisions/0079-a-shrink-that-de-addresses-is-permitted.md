# 0079. A shrink that de-addresses is permitted

- Status: Accepted
- Date: 2026-08-20
- Covers: §20.3 step 4's treatment of a shrink that drops tiles out of the
  addressed set; §11.1's Rationale; §21.1's magnitude carve-out; F23 and L12
- Revises: ADR-0074 and ADR-0078, whose stranding argument this narrows
- Confirm: reverses part of the reasoning of two accepted ADRs

## Context

Cleanroom round 15 read round 14's repairs and found a byte-level
ambiguity in the sentence ADR-0078 had written one day earlier. §20.3 step
4 bars a commit that alters what §14 fixes for a tile the layer stores in
the superseded generation. It does not say what happens when a shrink drops
a tile out of the **addressed** set entirely — §11.2's grid count falls and
the tile leaves the index. Under one reading the commit is barred and the
operation is a whole-file rewrite; under the other it is an ordinary commit
and the de-addressed extents become slack.

The check that settled it is worth recording. **The word *shrink* appears
exactly once in the whole document**, and that occurrence is inside a block
labelled `> **Rationale.**`, which §2.1 strips of force. The only text
addressing the case carried no force — and it was the sentence written in
round 14 to repair a finding about precisely that hazard.

Byte-level on the usual test: a generation-≥2 file is producible only by a
commit (a creator emits generation 1, §20.1), so the two readings differ on
whether a conforming implementation may emit those bytes. All three triage
passes upheld it, the implementer pass overriding two reporters' own
gradings to do so.

## Decision

**A shrink that de-addresses is permitted.** §20.3 step 4 now says so:
where a shrink leaves a stored tile addressed it is the existing case,
barred wherever it alters what §14 fixes for that tile; where it drops
tiles out of the addressed set, nothing is altered for any tile the new
state stores, `[R-CNT-17]` obliges the smaller entry_count and a re-emitted
index, the de-addressed extents become slack, and every surviving stored
tile is untouched. Discarding data is the caller's operation and this
specification does not bar it.

Paired with it, a **SHOULD**: produce a new file wherever a commit would
strand a large share of a layer's stored bytes, and always where it would
re-emit every one of them. A file is charged for by its length wherever
storage is metered, so slack that is not data the caller chose to discard
is paid for and never read.

### What this revises, and what it leaves standing

ADR-0074 and ADR-0078 both reasoned from stranding: `[R-LIF-01]` freezes
committed bytes, so an operation that looks like a directory edit and
leaves the file larger is a cost discovered rather than chosen, and should
be barred. **That argument is narrowed here.** Barring an operation because
its slack is unwelcome is the wrong instrument: it is arbitrary against a
caller who wants the data gone, and it is trivially circumvented in two
commits.

What survives is the distinction the maintainer's own cost argument draws.
In a de-addressing shrink the slack **is** the data the caller chose to
discard — proportionate, and exactly what deletion costs in an append-only
format. In the recompression case ADR-0078 barred, the caller keeps every
sample and the slack is a full duplicate of the layer: bytes paid for and
never read. So recompress-as-a-commit stays barred, not because it strands
slack but because the surviving stored tiles would decode under a codec
that did not produce them — the tile-breaking test ADR-0074 states, which
is untouched.

Round 12's original defect is likewise untouched: a shrink that turns real
positions into padding of a tile that **remains** stored still breaks that
tile, and step 4 still bars it.

## Consequences

§11.1's Rationale is rewritten to restate the rule rather than to be the
only place it appears, and now defers to §20.3 in terms. The register gains
nothing: a permitted operation names no condition.

Two other decisions ride along. §21.1's magnitude carve-out is applied to
F23 and L12, whose "inline_length is not 1" admits both directions —
inline_length 0, the encoding byte absent, and inline_length ≥ 2 — taking
the register to **121 conditions over 275 instances** and the corpus to
**327 vectors**. Both new vectors needed constructions rather than patches,
since a stored inline_length must match the bytes actually present or the
sequence carries residue and the file exhibits a framing row instead.

Twenty-two further defects are repaired, the largest of which correct text
this project wrote in the two preceding days: `[R-SER-08]` was cited in
§21.1 for the opposite of what it says, §20.5 cited §20.4 for a proposition
§20.4 denies, §21.7's "the §21.4 rows then fire" asserted a false converse,
and §21.2's new preamble claimed no row reaches a foreign-major file when
four do.

## Precedent

- ADR-0068's cost-discovered-versus-chosen principle, kept for the case it
  fits and withdrawn from the case it does not.
- §2.1's non-normative classes, which have now absorbed a repair three
  times — rounds 9, 14 and 15. A disambiguating sentence placed in a Note,
  Example or Rationale is not a weaker rule; it is no rule.
