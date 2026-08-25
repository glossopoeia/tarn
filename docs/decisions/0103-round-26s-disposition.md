# 0103. Round 26's remaining findings: `[R-COD-04]`'s subject, and Appendix G's filter argument

- Status: Accepted (dispositions round 26's non-byte-level findings)
- Date: 2026-08-25
- Covers: §17's preamble; `[R-COD-04]`; Appendix G item 5; the disposition of
  round 26's remaining findings
- Confirm: none

## Context

Round 26 returned 25 findings over 17 distinct defects. ADR-0102 resolved the one
that was byte-level. This dispositions the rest.

Before proposing any repair the document and the ledger were swept for what
already answered each — the step ADR-0094 recorded as missing. **Six defects
needed no new entry**, four of them the widest convergence this project has
recorded: §11.1's "last" was reported by *five* independent walks and §13.3's
re-emission trigger by *four*, and both were already **Q-B8**, opened hours
earlier from the ADR-0099 audit. §21.7's account is **Q-I5**, §21.2's "geometry"
carve-out is **Q-H6** — whose text quotes that very property — and Appendix G's
closing enumeration and its undefined "same input" are **Q-I6**.

That five cold readers independently found what a single refuter had argued
against three verifiers a day earlier is the strongest corroboration a ledger
entry in this project has received.

## Decision

**§17 states its subject once, rather than three rules stating it separately.**

`adversary-01` reported that `[R-COD-04]` — "The index entry's length therefore
MUST equal the tile's decoded size" — carries no non-sentinel qualifier, while
T14 and seven other register rows do. §21.1 says "where a row and the rule it
cites diverge, **the rule governs**", so on that reading the unqualified rule
wins and a sentinel entry's length field (2⁶⁴ − 1) never equals a decoded size:
every sparse codec-1 layer nonconforming.

All three triage passes downgraded it, the refute phase overturned them, and two
independent checkers then graded it **not byte-level**, reaching texts no earlier
reader had opened. The MUST is *derived* — "The stored bytes are the filtered
image verbatim. The index entry's length **therefore** MUST equal…" — and §3.1
defines *stored* as exactly "not the sentinel", so the premise has no instance for
a sentinel entry. The reading also proves too much: `[R-COD-06]` and `[R-COD-08]`
share the shape, so it would abolish sparse layers under **all four** codecs,
against §13.3, §15.2 and §21.6, the last of which says "A reader that treats any
of them as a failure is the nonconforming party."

**So the defect is a drafting gap, not a fork — and the fix is stated as a
property rather than as three qualifiers.** §17's preamble now says every rule in
the section ranges over *stored* tiles, that a sentinel entry's tile is not
stored, and that such a tile satisfies those rules vacuously. `[R-COD-04]`
additionally gains the explicit "non-sentinel", because that is the divergence
§21.1 would have resolved against it, and a rule its own register row has to
correct is not a rule the row should be correcting.

**Appendix G item 5 stops overclaiming.** Its argument for pinning the filter was
that it "changes the stored bytes of every tile it touches". §17.3 makes
byte-shuffle **the identity** where the shuffle stride is 1 — expressly for a
packed boolean plane, and equally for any single-byte element size or sample
stride. The item now says it changes the stored bytes of any tile whose stride
exceeds 1, which is all the argument ever needed: one such tile is enough for two
writers to disagree.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. T14's
condition cell already carried "non-sentinel", so the row and the rule now agree
and nothing the row registers changes.

One propagation acknowledgement. §21.6's non-defect entry already states the
proposition §17's new sentence relies on; it is the source, not a site left
behind.

**On the refute phase, which got this one wrong.** It has now changed a headline
verdict three times, twice rightly. Here it overturned a downgrade that all three
passes had reached correctly, and it did so by arguing from §21.1 alone without
opening §15.2, §3.1 or §21.6. **A refuter is as exposed to a narrow reading as
the pass it attacks** — its instruction to attack the shared premise is not
itself a guarantee that it has read more widely. What caught it was neither the
phase nor the passes but a mechanical reconciliation that named the two
byte-level groups **HAND-CHECK REQUIRED** and said no agent's word was
sufficient. That line is the instrument that worked.

**Seven findings are deferred with named owning sections**, as ADR-0034 requires,
and are recorded in round 26's findings: `reader-03` (§16.1), `verifier-02`
(§5.2, held near Q-C7), `diagrams-01` (Appendix A), `diagrams-02` (§20.3),
`register-03` (§21.3), `quiz-01` (§9.6), and `writer-06` (§20.3, checked against
Q-B6 and distinct from it).

## Precedent

- ADR-0095's rule that a partition stated by a property beats a list, applied
  here to a rule's *subject*: §17 states it once instead of three rules carrying
  the same qualifier and a fourth being caught without it.
- §21.1's "the rule governs", which is why a rule its register row has to correct
  is a defect even when the row is right.
- ADR-0096's sweep-before-disposition, which resolved six of this round's
  seventeen defects with no new entry.
