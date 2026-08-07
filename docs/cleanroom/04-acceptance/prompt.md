# Cleanroom round 4 — acceptance, post-ADR-0048 (prompt record)

Run against `spec/tarn.md` as of commit f738b29 — the complete
document after ADR-0048 replaced history-wide byte coverage with
live-state coverage. That change touched §1, §5.2, §9.7, §16, §20,
§21, §22, §23 and Appendix D and retired requirements, so the round
was run in full rather than as a G3 spot-check.

**Access rule given to every agent:** read `spec/tarn.md` and nothing
else — no other repository files, no version control history, no web.
Every conclusion cites section numbers and requirement IDs.

**The standard, tightened since round 3:** a byte-level ambiguity is
one where two permitted readings would make two implementers produce
different bytes, or reach opposite verdicts on the same bytes, and
every report must carry a **discriminator** — a concrete file or
input with the two divergent outcomes. An ambiguity a careful reader
resolves is an OBSERVATION, not byte-level. Each agent had to attempt
to refute its own finding first and say what it searched.

**Seven charters, run independently and in parallel:**

1. **Minimal reader (G2)** — codec 1, no slabs, no alignment: the
   byte-precise plan, the coordinate-to-value walk for both layouts,
   which sections were needed, an honest hour estimate, and the three
   hardest things to get right.
2. **Verifier** — the full certification procedure in dependency
   order, then a worked three-commit trace classifying every byte and
   stating what is reported to the operator.
3. **Writer** — byte-exact creation of a one-layer interleaved file,
   then a growth commit, then storing a non-fill value into a newly
   addressed tile, plus the legitimate-divergence catalogue.
4. **Quiz** — fifteen questions weighted toward the changed material:
   what coverage now certifies and what happens to the rest; whether
   a 90%-slack file is conforming; what a trailer-mimicking payload
   does now that nothing enumerates unreachable bytes; whether a
   4096-byte gap before a 512-aligned tile is padding, slack or a
   defect; the growth mechanics; and a full edge-tile decoded image.
   Graded against a key derived independently and verified
   computationally before the round.
5. **Navigator (G1 evidence)** — spine, density, restatement drift,
   and whether the three lookup questions are answerable without
   linear reading, with the final G1 judgment explicitly reserved to
   a human reader.
6. **Adversary** — construct a file one verifier certifies and
   another rejects, or a conforming file carrying bytes no rule
   accounts for; report a failed attack explicitly if it cannot.
7. **Differential writer** — write the same two-layer file twice
   making different legitimate choices at every free point (declared
   alignment, a sentinel tile, a bool channel, a metadata record),
   then classify every differing byte range as granted freedom or as
   one writer being wrong.

Verbatim outputs: `transcript-*.md`. Consolidated results, gate
verdicts, and disposition: `findings.md`.
