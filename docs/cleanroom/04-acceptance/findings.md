# Cleanroom round 4 — findings, disposition, and gate verdicts

**Verdict: G2 PASS · G3 not yet met — 3 byte-level ambiguities, all
fixed, one of them forcing a further simplification · G1 evidence
positive, judgment reserved.**

Seven fresh-context roles worked the complete document — the four
ADR-0034 roles, the navigator for G1, and the two instruments that
earned their place across the G3 attempts: the coverage adversary
(the only role that ever constructed a file two verifiers judge
differently) and the differential writer. The quiz scored **15/15**
against a key derived independently and verified computationally
before the round, probing the post-ADR-0048 material specifically.

| Role | Implementable | Byte-level |
|---|---|---|
| reader (G2) | yes | 0 |
| writer | yes | 0 |
| quiz | yes | 0 |
| differential | yes | **0** |
| navigator | qualified | 0 |
| adversary | qualified | 1 |
| verifier | qualified | 2 |

Trend across rounds: **5 → 4 → 4 → 3**.

## The finding that mattered: declared padding could not survive

The adversary and the verifier found the same defect from opposite
directions, and tracing it produced a conclusion that was *forced*
rather than chosen.

ADR-0048 left "declared padding MUST be zero" as a certified class.
To check it, a verifier must identify which unclaimed bytes are
padding — and after ADR-0048 no discriminator survives:

- **"maximal unclaimed run shorter than the modulus"** — superseded
  bytes are also unclaimed, so the run reaches backward through them.
  The verifier built the discriminator: a generation-1 file of
  Appendix A's 128 bytes, then a commit adding a layer with
  A = 4096. The maximal run before the aligned tile is [16, 4096) —
  4080 bytes, under the modulus, therefore declared padding — and it
  *contains generation 1's trailer*, which is not zero. Reject-file,
  and since committed bytes are immutable no writer can ever repair
  it: a natural append pattern becomes unconstructible.
- **"the run bounded by the previous claimed structure"** — fails
  identically; the front block is claimed at 16.
- **"bytes this commit wrote"** — requires knowing F_prev, i.e. the
  generation awareness ADR-0048 removed.

The adversary reached the same place from the writer's side: §16.1
and §16.2 asserted flatly that the gap before an aligned tile *is*
declared padding, with no modulus qualification, so an ordinary
writer using fixed aligned slots for variable-length tiles produced a
924-byte gap that one reading certifies and another rejects. Under
A_slab = 1 — the recommended contiguity-only declaration — *no*
nonempty gap can satisfy "shorter than the modulus" at all.

**Disposition.** Declared padding ceases to be a coverage class.
Every byte the live state does not claim is **slack** — alignment and
slab gaps, the pre-trailer pad, and everything superseded — with
unconstrained content, no conformance requirement, and a verifier
obligation to report the total. Zeroing survives as writer advice
with its consequence stated. ADR-0048 is amended to record that this
was forced by the model it chose, not a further preference.

## Third finding

`[R-MTA-09]` let a reader decline an oversized user-metadata document
as ignore-record, but said nothing about a **verifier** in the same
position — which could then certify a file whose document it never
examined, checking none of §18.2's content rules. Now: a verifier
that declines to decode a document cannot establish its conformance
and MUST NOT certify, mirroring `[R-COD-11]`.

## Register effect

120 conditions over 214 instances (was 121/213). F10 — nonzero
declared padding — is gone, since the condition no longer exists; F9,
F12 and F36 drop declared padding from their class lists; F-rows
renumbered contiguous.

## Gate G2 — weekend-implementable: PASS

The reader produced a complete byte-precise plan for a minimal
conforming reader and confirmed it buildable from the text alone, at
high confidence with zero byte-level ambiguities — and made the
honest distinction the document invites: a codec-1-only reader is a
*correct partial reader*, not a conforming one, and must report its
refusals as capability rather than corruption. The writer produced a
byte-exact create, a growth commit, and a store-into-new-tile commit,
also at yes/high.

## Gate G3 — zero byte-level ambiguities: not met this round

Three were found. All are fixed, but the gate asks for a round that
finds none, and this round found three. What has changed is the
character of the finding: rounds 1–3 kept producing *new* classes of
coverage ambiguity, whereas this round produced one residue of the
previous fix plus one unrelated verifier gap. The differential
writer returned zero for the third consecutive time, now on an input
carrying declared alignment, a sentinel tile, a bool channel and a
metadata record.

## Gate G1 — afternoon-readable: evidence positive, judgment reserved

The navigator found the spine coherent, the declared reading order
consistent with the material's actual dependencies, and the three
lookup questions an implementer asks answerable without linear
reading. A final G1 verdict belongs to a human reader; this round
establishes the document remains the right size and shape for the
claim.

## Implementer notes (no spec change)

Every fixed constant in the document was independently recomputed by
two roles and reproduced exactly, including Appendix A's file, which
still matches byte-for-byte after this round's edits. The reader
noted that because sample values are bit patterns a reader must not
alter, the thirteen sample types collapse on the read path into a
thirteen-entry element-size table — no IEEE 754 arithmetic anywhere
in a conforming reader.
