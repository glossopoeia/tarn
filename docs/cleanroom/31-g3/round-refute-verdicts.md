# Cleanroom round 31 — refute-phase verdicts

**No refuter ran.** The workflow's own log line is the record:

    refute phase: 0 unanimous downgrade(s), 0 split verdict(s); byte-level upheld anywhere: true

The phase fires on three shapes — a reporter's byte-level flag that no pass
upheld, a group the passes split on, and a round-wide zero — and this round
produced none of them. Its one byte-level flag, `writer-01`, was upheld by all
three passes; a unanimous uphold is not a downgrade and not a split, and its
presence is exactly what suppresses the zero-trigger. So the harness attacked
nothing, and the two refuters that were configured on the fallback model never
launched. Twelve agents ran; twelve is the author, the six walks, the two
takers and the three passes.

That is a gap in the phase, recorded here and in the findings: the phase was
built to overturn verdicts in the direction that *clears* the gate, and a
unanimous verdict in the direction that *fails* it is the one shape it never
tests. The hand-check below stood in its place.

## `writer-01` — the §14 bar's reach over a tile-extent permutation

**Hand-check verdict: UPHOLD STANDS.** The construction is arithmetically
right and was recomputed independently; the disputed file is conforming; no
sentence in the document decides whether the coordinate a stored byte denotes
is part of what the §14 bar protects. The passages opened in the direction that
would have cleared the gate — §3.2 `[R-MDL-01]`, §11.4 `[R-GEO-06]`, §14's
opening sentence and §14.1 `[R-SER-01]`, §20.1 `[R-WRT-01]`, §20.3 step 4 whole
(the re-emission clause, the bar, its gloss, the sample-type paragraph, the
ordinal bar, the growth and shrink paragraphs), §20.5 `[R-WRT-07]`, §21.7, §23.1
`[R-PRV-01]`, Appendix G item 5 — and the sentence that would decide it is in
none of them. The full account is in `findings.md`.
