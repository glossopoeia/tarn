# Cleanroom round 18 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists, and what is different about it

Every previous round read the repairs of the round before it, cold. **This
round reads repairs that were audited before it ran.**

Rounds 14–17 each found their defect in the immediately preceding round's
repair, three of them in §20.3 step 4. Running a fifth round of the same shape
was unlikely to break that, so the instrument changed: a **repair audit** — a
spec-only pass over the repair diff, one auditor per two or three hunks plus a
cross-hunk auditor, every finding adversarially verified and every byte-level
downgrade attacked. See [repair-audit.md](repair-audit.md) and ADR-0081.

It found, in round 17's repairs, one byte-level defect and eight lesser ones,
plus two things no cleanroom round can reach because they are not in the
document: an Accepted ADR the spec contradicted, and a conformance check that
was structurally blind to the passage where four rounds' defects had landed.

So the text this round reads has already survived one adversarial pass. That
raises the bar rather than lowering it: **the marginal defect is now the one
the audit's own repairs introduced**, and that is what this round is for.

## The changed surface

**30 lines inserted and 18 deleted across 7 hunks, in 5 sections** — §20.4,
§20.5, §21.7, §23.1 and Appendix G. The document is 4,339 lines.

§20.5 carries the largest change: a passage rewritten so that a compactor's
obligation rests on a different requirement than it did yesterday, with two
claims about other requirements' scope deleted. **§20.4's cell is on its
fifth revision in five rounds.** One repair changed a lowercase modal into an
ALL-CAPS one, which changes what binds. One added a paragraph break inside
what had been a single sentence. Two are single-clause sweeps of text that
had gone stale when a rule moved elsewhere.

Read those five sections first — and then do not stop there. Each of the last
four rounds found real defects in text no recent round had touched, including
a requirement cited wrongly for nine rounds and a section that told a verifier
to reject every conforming file. **The marginal value of your walk is in the
parts nobody has had to implement from recently.** Cover the five, then spend
the bulk of your effort building the thing your charter names, end to end, and
report wherever you had to guess — whether or not the passage that made you
guess is new.

This tells you **where to look and nothing about what the answers are.** You
are not told what changed, why, or what any edit was meant to accomplish, and
you must not infer that a listed section is wrong or that an unlisted one is
right.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, not this file. Not
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`. Not `conformance/` —
no tooling, no vectors, no manifest. Not `spec/registry.json`. No git history,
no web.

No agent reads the round's own output directory. The three triage passes are
additionally barred from each other's transcripts by name.

A conclusion you reach because a test vector or an ADR told you is not
evidence that the specification says it, and this gate's whole claim is that
the document stands alone. A disclosed breach is a usable result; an
undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a **diagram
auditor**, a **register hunter**, an **adversary**, and a **quiz** authored,
answered and keyed by three agents blind to one another. Then three blind
triage passes, then the refute phase.

Standing charges: the register hunter checks **every cross-reference to a
register row against the row it lands on** and **recounts by hand every total
the document states about itself**; the diagram auditor treats the conformance
checklists and any table restating a rule as figures, and checks every worked
example byte by byte.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Flagged by reporters / survived triage, rounds 6–17: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under
both readings and the emittable set does not move. If the disputed file is
conforming and only one reading permits an actor to produce it, the set moves.

**A new discriminator, from this session.** §2.1 binds BCP 14 keywords "when,
and only when, they appear in all capitals". A restriction written in
lowercase does not bound a permission written in capitals — that asymmetry,
inside one table cell, was round 17's surviving byte-level defect and three
verifiers missed it. Where two clauses of one rule disagree, check their
casing before you check their logic.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind
to each other; the refute phase then attacks every unanimous byte-level
downgrade **and every split verdict**. Reconciliation is done by the
maintainer's agent directly and mechanically: union-find over the passes'
groupings and a set difference on finding ids. Each walk's transcript is
diffed against its own structured return, and the workflow's own error report
is read before any result. The maintainer additionally reads the same repairs
independently and reports what the round missed as well as what it found.

**And a zero is not a result.** This session's repair audit had 31 findings
adversarially verified by agents told to default to REFUTED; that returned
zero byte-level, and a refute-only pass then overturned all four byte-level
downgrades. A shared instruction is a shared premise. Zero is the trigger for
the refute phase.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**, surviving the
refute phase — **and the next round, reading this round's own repairs, must
return zero too.** One clean round has never been enough: rounds 7, 9 and 13
each hit zero and rounds 8, 10 and 14 each found the defect in the repairs
that zero produced.
