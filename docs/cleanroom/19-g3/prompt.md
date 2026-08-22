# Cleanroom round 19 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists, and what is different about it

**This round reads repairs that were audited three times before it ran.**

Round 18's single byte-level finding was repaired; that repair was audited and
found to carry a byte-level defect of its own; the fix for *that* was audited
and found to carry four more; and the fix for those was audited a third time
and came back with none that survived an adversarial refute pass. Three passes,
three distinct sets of defects, each in the fix for the last.

So the text this round reads has survived more adversarial reading than any
text this project has shipped. That raises the bar rather than lowering it.
**Every easy defect in the changed surface is gone, and what a cold reader can
still find there is worth more than in any previous round** — because it will
be something four rounds of instruments, all of which could see the diff, did
not.

You are not told what those instruments found, or where. Do not assume the
changed sections are safe; do not assume they are the interesting ones.

## The changed surface

**38 lines inserted and 13 deleted across 5 hunks, in 4 sections** — §20.5,
§21.7, §23.1 and Appendix G. The document is 4,364 lines.

§20.5 carries the largest change and has been rewritten three times in a day.
One sentence there now assigns **two different BCP 14 modals to two clauses of
one rule**, on purpose. A second passage states a closed two-item enumeration
together with the argument for why it is closed — check the argument, not just
the count. §21.7 gained an entry; §23.1's opening was rewritten from a
completeness claim into an enumeration, and the requirement it carries had its
scope widened. Appendix G gained a carve-out and a concession about what the
profile cannot deliver.

Read those four sections first — and then do not stop there. Each of the last
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

Flagged by reporters / survived triage, rounds 6–18: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1.

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
