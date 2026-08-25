# 0096. Round 24's register cells are corrected, and §21.7 goes to the ledger whole

- Status: Accepted (dispositions round 24's non-byte-level findings)
- Date: 2026-08-25
- Covers: R7's condition cell; L16's bound; the disposition of round 24's
  remaining findings
- Confirm: none

## Context

Round 24 returned 18 non-byte-level defects alongside its two byte-level ones.
Before proposing any disposition, the document was swept for what already
answered each — the step ADR-0094 recorded as missing when a decision was put to
the maintainer without it. **Two of the eighteen needed no action:**
`writer-04` (§23.1 omitting the unstored case) had been fixed by ADR-0095 hours
earlier, and `writer-05` (R8 collapsing `[R-MTA-04]`'s alternatives) was already
**Q-I4**, opened by ADR-0092 — round 24's register hunter re-reported it
independently, which is corroboration that the entry is live.

A third looked answered and was not. `register-01` asks which of §2.3's three
verdicts a verifier reports for a foreign-major file a register row reaches.
That reads like **Q-H4**, which asks *which rows reach* such a file. It is a
different question — which rows, versus what follows — and folding it in would
have buried it.

## Decision

**Two register cells are corrected**, both checkable against a named rule, which
is the class of repair this week's audits have not been finding defects in.

`R7`'s Condition cell states two alternatives while its own Instances cell
counts three, the third — a leading U+FEFF byte-order mark — being one §18.2
states plainly. The cell now names it.

`L16` takes `F31`'s bound rather than the reverse. The finding's phrasing
pointed at F31, whose "in 1-15" looked like a loose restatement of
`[R-CNT-13]`'s "extent_offset < 16" beside L16's faithful one. **The sweep
showed F31 was right**: F30 and L15 already register the one-half-zero case, so
a *nonzero* extent slot necessarily has `extent_offset` ≥ 1 and 1–15 is the
precise range. Repairing in the direction the finding suggested would have made
the more accurate row worse.

**§21.7 goes to the ledger as a whole, not as eight repairs.** Four ADRs have
repaired that section in four days, and it has drawn a finding cluster in five
consecutive rounds — eight in round 24 alone, each a member missing from or
wrongly attached to one of its lists. Patching it a fifth time repeats what has
failed four times. **Q-I5** asks what the section is *for* and what its account
must cover, with three options priced: restate it as a test rather than an
inventory; keep the inventory but derive it mechanically as a checked artifact;
or split the normative claim from the illustrative walk-through that keeps going
stale.

**Three design questions become ledger entries** rather than spec text, per
AGENTS.md rule 3: **Q-A7** (§20.5's version_minor floor turns on a fact a
compactor cannot obtain for one of the two cases the rule names), **Q-H5**
(above), and **Q-C5** (§8.1's one live region under no checksum carries no
verifier reporting duty, unlike `[R-MTA-10]`'s uninspected extents, which §22.3
requires be counted and named).

**Seven findings are deferred with named owning sections**, as ADR-0034
requires. They are recorded in round 24's findings, including that `verifier-01`
and `diagrams-02` are one defect seen from two sides — §5.2 says no slack total
is owed in a case where Appendix H's verifier checklist demands a partial one.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. Neither
cell edit changes a condition's extension — R7's third alternative was already
instanced and vectored, and L16's range was already the only satisfiable one.

**What the sweep is worth, measured.** It resolved two findings without a repair,
prevented one wrong repair, and separated one question from a ledger entry it
would otherwise have been folded into. That is four of eighteen findings decided
by reading rather than editing, at the cost of a few greps — against a week in
which four of five repair cycles introduced defects.

## Precedent

- ADR-0094's closing lesson, that a decision offered before the document has been
  swept for what already answers it is a decision taken blind. This is the first
  disposition made with the sweep run first.
- ADR-0095's rule about closed counts, which is why §21.7's cluster is now read
  as a contract problem rather than eight enumeration slips.
- AGENTS.md rule 3, under which a question with options belongs in the ledger
  before it belongs in normative text.
