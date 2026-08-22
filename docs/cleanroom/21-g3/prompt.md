# Cleanroom round 21 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 20 returned one byte-level ambiguity — the **constructive adversary's
first survivor in fifteen rounds**, and the third round running whose survivor
sat in text no recent round had touched. It was repaired, and that repair was
audited before you read it: two auditors, adversarial verification, and a
refute pass over every downgraded byte-level flag. **That audit came back with
no byte-level defect — the first pre-round audit to do so.** It found and fixed
two lesser things: a carve-out that named one of two bounds, and a citation
pointing one paragraph short of the rule it needed.

So the changed text has been read hard already. That raises the bar rather than
lowering it: what a cold reader can still find there is worth more than in any
previous round, because four instruments that could all see the diff did not
find it.

You are told none of what they found, or where.

## The changed surface

**One passage in §18.2, one clause in §21.5** — 11 lines inserted, 3 deleted.
The document is 4,377 lines.

Both settle the same kind of question: whether a case is a **defect in the
file** or a **limit of the actor reading it**. That boundary has now produced
two byte-level defects in three rounds, and it is the one place this document
has repeatedly found itself with a rule that names one quantity where two are
in play.

Read those two first — then do not stop there, and this round means it more
than any before. **Rounds 18, 19 and 20 each found their surviving defect in
text no recent round had touched**, by three different instruments: a missing
modal, a paragraph another section had designated authoritative, and a
constructed pair of files one bit apart. None was in the changed surface.

This tells you **where to look and nothing about what the answers are.**

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

Flagged by reporters / survived triage, rounds 6–20: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under
both readings and the emittable set does not move. If the disputed file is
conforming and only one reading permits an actor to produce it, the set moves.

**Two discriminators this project learned the hard way.** First: §2.1 binds
BCP 14 keywords "when, and only when, they appear in all capitals". A
restriction written in lowercase does not bound a permission written in
capitals, and a clause with no keyword at all has no force of its own — those
two were the surviving byte-level defects of rounds 17 and 18. Where two
clauses of one rule appear to disagree, check their casing before their logic.

Second, and it cuts the other way: `[R-CNF-12]` places SHOULD deviation
outside the register entirely, and `[R-CNF-05]` gates emission on file
conformance. **A dispute about what a SHOULD requires cannot move the
emittable set**, however different the resulting bytes. If your finding turns
on a SHOULD, say what it costs an implementer and grade it honestly rather
than reaching for byte-level.

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
