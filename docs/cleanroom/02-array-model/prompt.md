# Cleanroom round 2 — array model (prompt record)

Run against `spec/tarn.md` as of the Batch 6 text plus the ADR-0038
amendment (commit f38b6ec): §11–§16 fully drafted — geometry, sample
types, fill, tile serialization, tile index, slabs — with §17
onward reserved. Scope per PLAN: the array-model gate (planar
offsets, edge tiles, unstored-tile reads) plus the index-facing half
deferred from round 1.

**Access rule given to every agent:** read `spec/tarn.md` and nothing
else — no other repository files, no version control history, no web.
Every conclusion must cite section numbers and requirement IDs. Where
the text under-determines, record an AMBIGUITY (location, the readings
permitted, the pick and why); where it contradicts itself, a
CONTRADICTION with both citations; effort-disproportionate but
decidable points are OBSERVATIONS. Reserved sections are not defects,
but unresolvable forward references into them are reportable.

**Four charters, run independently and in parallel:**

1. **Reader** — the byte-precise walk from coordinate request to
   returned value for both layouts, codec treated as an opaque
   stored→decoded transform; cold-read accounting at entry_count 10⁶
   (exact verified byte ranges for disk ordinal 999,999); degradation
   walks (sentinel, entry-CRC and segment-CRC mismatch, channel type
   14, over-long decoded payload, interleaved bool byte 0x02,
   linearization 2); the fill path (planar mixed sample, NaN-payload
   fill, unstored interleaved tile); edge-tile clipping; verdict on
   implementability of §11–§16 from the text alone.
2. **Verifier** — the full array-model check list (§15.3 rows,
   `[R-CNT-17]` cross-checks, segment-CRC chain, §16 invariants,
   §14.2/§14.5 decoded-content obligations) with outcome classes; a
   worked trace over layer L (planar, y 10/4 · x 13/8, channels
   m bool fill 0x01, t float32 fill −0.0; m sparse at spatial
   ordinal 3) — region layout, sentinel locations, edge tiles, every
   CRC's coverage; the conforming decoded bytes of m's (2,1) edge
   tile; what §11–§16 leave undecidable.
3. **Writer** — layer K (interleaved, y 5/2 · x 7/3, channels
   a uint16 fill FFFF, m bool fill 0x00): full arithmetic and the
   labeled hex of the (2,2) edge tile's decoded image; the complete
   index-region byte layout for a two-stored-tile pattern; packed
   plane padding and pad bits under fill true; the byte-for-byte
   agreement vs legitimate-divergence catalog; slab obligations under
   S = 3, A_slab = 4096.
4. **Quiz** — fifteen byte-level questions over layers L and K
   (declarations as above), graded against an answer key derived
   independently and verified computationally before the round:
   region arithmetic and CRC-array placement; disk-ordinal and
   entry-range location; coordinate→plane-offset walk; the complete
   edge-tile bool plane (fill-encoded padding); padding float bytes;
   planar sentinel independence at one sample; two malformed-entry
   classifications; interleaved stride/offset with a bool channel;
   the 0x02 conformance/reader/verifier split; segment arithmetic at
   entry_count 70,000; the sparse-segment constant's licensing
   boundary at 65,536/65,537; full-extent read clipping; slab run
   partition and packed offsets with a sentinel; the planar-vs-
   interleaved single-bool-channel size asymmetry.

Verbatim outputs: `transcript-reader.md`, `transcript-verifier.md`,
`transcript-writer.md`, `transcript-quiz.md`. Consolidated results and
disposition of every finding: `findings.md`.
