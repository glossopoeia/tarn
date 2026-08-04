# Cleanroom round 2 — findings and disposition

**Verdict: PASS with findings.** All four fresh-context implementers
produced correct, citation-grounded array-model implementations from
the spec text alone. The quiz scored **15/15** against the
independently derived, computationally verified answer key — zero key
corrections — including the deliberate probes (the planar
sentinel-independence sample at Q6; the full edge-tile bool plane
`E0 E0 FF FF` at Q4; the 65,536/65,537 licensing boundary of the
sparse-segment constant at Q12; the planar-vs-interleaved single-bool
size asymmetry at Q15, which exercises the ADR-0038 amendment). The
reader independently re-derived all three stated CRC-32C constants
from §4.5's definition alone, `0xEECB3BB2` included, and re-verified
every worked example in §11–§16. The verifier found the round's one
genuine contradiction. Every reported confusion was treated as a spec
bug per PLAN §6.

## Findings fixed in the spec (this round)

| Finding (reporter) | Fix |
|---|---|
| §4.5 "checksum fields covered by no further checksum" vs §8.1's segment-CRC array covered by crc_of_crc_array; §8.1's "sole exception" vs §4.5's two exceptions (verifier — **contradiction**) | §4.5 now distinguishes terminal checksum fields (trailer, directory-region, user-metadata — covered by nothing) from interior ones (segment CRC arrays, crc_of_crc_array — comparison-verified *and* covered exactly once); §8.1's lead sentence aligned |
| `[R-IDX-05]` "full" segment undefined — final segment of exactly 2¹⁶ entries ambiguous (quiz) | §15.4: "full" defined inline — exactly 2¹⁶ entries, final or not; "final partial" reduced to "partial" |
| `[R-IDX-04]` per-use vs cached verification (reader) | §15.4 Note: "to use" obliges verification, not re-verification; caching per §9.3 `[R-LIF-03]` |
| §15.3: do reject-tile-invalid entries contribute extents to the verifier overlap rows? (verifier) | `[R-IDX-03]`: reject-tile entries contribute no stored extent; verifier rows bind over well-formed entries only |
| `[R-SLB-03]` inter-run placement underdetermined; "gaps A_slab creates" presupposed consecutive runs (writer) | §16.2: runs are not mutually ordered or joined — `[R-SLB-05]` freedom governs between runs; unclaimed placement slack is declared padding. §16.1's gap wording aligned |
| `[R-SLB-04]` "every affected run" undefined (writer) | Defined inline: a run whose stored-tile set or byte placement the commit changes |
| Pad bits vs padding positions — near-identical terminology, distinct mechanisms (quiz, verifier) | §14.3 Note distinguishing the two, with §14.5 as the shared content rule |
| §14.2's sequence-indexed offset formula forces each implementer to re-derive the per-(channel, ordinal) form (quiz) | §14.2 example now states the identity: channel c at ordinal u sits at u · Q + Fᶜ (k = u · C + c) |

## Findings deferred, with owners

- Codec value set unresolvable; `[R-CNT-23]`'s codec check unwritable
  until §17 (reader, verifier, writer) → Batch 7, as already planned.
- Verifier conformance class facing an unimplemented-but-assigned
  codec (decoded-content checks blocked) → §17 (Batch 7; PLAN row
  updated).
- Duplicate-name detection timing on the read path (reader) → §19's
  eager-vs-lazy validation treatment (Batch 8; PLAN row updated).
- Multi-segment planar all-channel read accounting (reader) → §19
  note candidate (Batch 8; PLAN row updated).
- entry_count bound capping segment-CRC-array growth (reader);
  checksum-uncovered padding bytes noted for security text
  (verifier) → limits table / §22 (Batch 11; PLAN row updated).
- Stored-length vs decoded-size bounds under the codec pipeline
  (writer) → §17 (Batch 7; PLAN row updated).

## Resolved without spec change

- `[R-SER-08]` detecting-reader scope (reader AMBIGUITY): the
  nonconforming-file regime (`[R-CNF-12]`) deliberately leaves a
  detecting reader's response unconstrained; the verifier row is the
  normative anchor. Recorded as intended freedom, not a gap.
- Notation reuse (S sentinel vs S slab; F file length vs Fᶜ offset)
  (verifier): each is locally defined at use; no collision within any
  one derivation. No change.
- The sparse-segment constant is unusable below entry_count 65,536
  (writer): by design — the constant exists for the large-sparse
  case; small layers compute one CRC.

## Implementer notes (no spec change)

The reader implemented the array model with the codec as an opaque
transform and confirmed §11–§16 implementable from the text alone on
that basis; its cold-read accounting reproduced §15.4's worked
numbers exactly. The verifier's worked trace over the planar
two-channel layer (sentinel at one m-plane ordinal) classified all
12 entries, both CRC coverages, and the edge-tile content
obligations correctly, and observed that integrity verification is
fully executable today while decoded-content verification awaits
§17 — the intended staging. The writer produced the complete decoded
edge-tile image with every padding byte justified, the full
index-region byte layout for a mixed stored/sentinel pattern, and
independently derived that decoded images are byte-deterministic
while index bytes legitimately diverge — the content-addressing
split §14.5's rationale claims.
