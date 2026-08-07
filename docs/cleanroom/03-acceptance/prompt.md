# Cleanroom round 3 — acceptance (prompt record)

Run against `spec/tarn.md` as of the Batch 13 text (commit c75a127):
the complete document — §§1–24 and Appendices A–H, no `[Reserved]`
markers, the decision ledger fully resolved into ADRs 0001–0047.

This is the **acceptance round** of PLAN §1: it evaluates gates G1
(afternoon-readable), G2 (weekend-implementable), and G3
(cleanroom-clean — *zero* byte-level ambiguities). ADR-0034 pins four
roles; round 3 adds a fifth, the navigator, because G1 is a property
of the document as a whole that no implementer role measures.

**Access rule given to every agent:** read `spec/tarn.md` and nothing
else — no other repository files, no version control history, no web.
Every conclusion must cite section numbers and requirement IDs. Where
the text under-determines, record an AMBIGUITY; where it contradicts
itself, a CONTRADICTION; effort-disproportionate but decidable points
are OBSERVATIONS. **New for this round:** every agent flags separately
any ambiguity that is *byte-level* — one where two permitted readings
would produce or accept different bytes — because G3 requires zero of
those. An ambiguity resolved after re-reading still counts.

**Five charters, run independently and in parallel:**

1. **Minimal reader (G2).** Build a minimal conforming reader — codec
   1 only, no slabs, no alignment, local files: the complete
   byte-precise implementation plan, the coordinate-to-value walk for
   both layouts, which sections were actually needed, an honest hour
   estimate with the three hardest things to get right, and every
   place a rule had to be reconstructed from scattered statements.
2. **Verifier.** The complete certification procedure in dependency
   order across container, array model, decoded content, coverage,
   and multi-generation attribution; what a verifier cannot establish;
   a worked two-generation trace classifying every byte; and an audit
   of §21's register against the procedure in both directions.
3. **Writer.** Byte-exact creation of a one-layer interleaved file
   (t 2/1 · x 3/2; channels p uint8 fill 0x00, q bool fill 0x01),
   every chosen value named as a choice and every stored tile's
   decoded image including padding; then an append superseding one
   tile; then a compaction; then the legitimate-divergence catalogue.
4. **Quiz.** Fifteen byte-level questions spanning the whole document
   — minimal-file bytes, transport-size mismatch, planar region
   arithmetic and disk ordinals, a complete packed edge-tile plane,
   interleaved stride with a bool channel, two malformed index
   entries, unsorted metadata keys, `1e400`, an experimental codec
   value, an unknown MU = 1 record at two scopes, segment arithmetic
   at 70,000 entries, the rank-32/rank-40 acceptance split,
   compaction identity, and Appendix A's trailer CRC — graded against
   a key derived independently and verified computationally before
   the round.
5. **Navigator (G1 evidence).** Structure and spine coherence, the
   three densest passages, restatement drift, and whether the three
   lookup questions an implementer actually asks are answerable
   without reading linearly — with the explicit instruction that a
   final G1 judgment belongs to a human reader.

Verbatim outputs: `transcript-reader.md`, `transcript-verifier.md`,
`transcript-writer.md`, `transcript-quiz.md`,
`transcript-navigator.md`. Consolidated results, gate verdicts, and
the disposition of every finding: `findings.md`.
