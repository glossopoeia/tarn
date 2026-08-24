# Cleanroom round 23 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 22's survivor was the previous cycle's own repair sentence — a rule that
supplied one quantifier for three table rows whose instances are individuated
differently. Six reporters found it independently, the widest convergence on a
single defect in this project's history.

Since then the document has been changed by **three separate cycles**, and none
of them has been read by a fresh-context round. The repair audit that precedes
this round read all of them together: eighteen findings, adversarially verified,
then a refute-only pass over every group. **It returned no byte-level defect**,
and the five real defects it did find are fixed in the text you are reading.

So the changed text has been read harder than in any previous round, and by
instruments that read the *commit* rather than the document. What a cold reader
can still find there is worth more than in any previous round.

You are told none of what those instruments found, or where.

## The changed surface

**Five passages — §18.2, §21.5, §21.7, §21.8 and §21.9** — 69 lines inserted,
37 deleted. The document is 4,426 lines.

**§18.2's compressed-document passage is the most-repaired passage in this
specification.** Three consecutive cycles have rewritten parts of it, each
holding a different defect in mind, and the text you have is their accumulated
result rather than anyone's single draft. Two of those cycles were repairs of
the cycle before. Read it as a whole passage, not as a sequence of rules.

The other four are a register row and its neighbours: a row's condition text, an
account of what no check detects, a stated total, and a table of guarantees with
a paragraph saying which of its rows range over what.

Three shapes are worth carrying into any passage, changed or not:

1. **Quantifier and scope.** *Four of the last five byte-level defects in this
   document have been quantifier or scope questions* — which records a licence
   covers, which placements a refusal reaches, which instances a limit bounds.
   Look at any rule that states a bound or a permission over a structure without
   saying which instances of that structure it ranges over.

2. **One quantity named where two are in play.** A rule can be perfectly correct
   about the thing it mentions while a sibling quantity of the same structure —
   the same header, the same record, the same field group — is governed by
   nothing. That defect does not read as a contradiction or an overclaim. Name
   the structure, list everything it can carry, and ask what fixes each.

3. **Argument by analogy.** Where the document justifies one rule by pointing at
   another — "exactly as", "the same way", "for the same reason", "transposed
   from", "likewise" — put the two governing verbs side by side and read them
   word for word. An analogy can be sound for one member of a set and unsound
   for the next.

And one method question, which applies everywhere: **for any rule you can only
defend by reasoning you supply yourself, ask whether the document supplies it.**
A rule whose correctness depends on a fact stated nowhere in `spec/tarn.md` is
not a rule a fresh implementer can apply, however right it is.

Read the five passages first — then do not stop there. **Rounds 18, 19, 20 and
22 each found their survivor in text no recent round had touched**, and round 21
found one of its two by building a legal-but-degenerate file and asking what a
table said about it.

This tells you **where to look and nothing about what the answers are.**

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, not this file. Not
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`. Not `conformance/` —
no tooling, no vectors, no manifest. Not `spec/registry.json`. No git history,
no web.

No agent reads the round's own output directory. The three triage passes are
additionally barred from each other's transcripts by name.

A conclusion you reach because a test vector or an ADR told you is not evidence
that the specification says it, and this gate's whole claim is that the document
stands alone. A disclosed breach is a usable result; an undisclosed one poisons
the round.

**Context you did not ask for.** Your runtime may place material in your context
before you begin — a project instruction file, an index of the maintainer's
notes, a task list. None of it is part of the specification and none of it is
evidence about the specification. It may name this round's position, prior
findings, or things that look like answers. Disregard all of it, and disclose
that it appeared without repeating its contents. Every agent in the two runs
that preceded this round disclosed exactly that, which is what the field is for.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a **diagram
auditor**, a **register hunter**, an **adversary**, and a **quiz** authored,
answered and keyed by three agents blind to one another. Then three blind triage
passes, then the refute phase.

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

Flagged by reporters / survived triage, rounds 6–22: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 2/2, 5/1.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Two discriminators this project learned the hard way.** First: §2.1 binds BCP
14 keywords "when, and only when, they appear in all capitals". A restriction
written in lowercase does not bound a permission written in capitals — that was
round 17's surviving defect. **But do not extend that to "a clause with no
keyword has no force":** `[R-CNT-13]` carries no keyword and §21.7 calls that
very sentence a *prohibition*, and `[R-CNT-02]`, `[R-SER-01]` and `[R-SER-02]`
are the same construction. Round 19's charter asserted the stronger claim and it
caused a real defect to be under-graded. Where two clauses of one rule appear to
disagree, check their casing before their logic — and check the document's own
practice before concluding a clause is inert.

Second, and it cuts the other way: `[R-CNF-12]` places SHOULD deviation outside
the register entirely, and `[R-CNF-05]` gates emission on file conformance. **A
dispute about what a SHOULD requires cannot move the emittable set**, however
different the resulting bytes. If your finding turns on a SHOULD, say what it
costs an implementer and grade it honestly rather than reaching for byte-level.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind to
each other; the refute phase then attacks every unanimous byte-level downgrade
**and every split verdict**. Reconciliation is done by the maintainer's agent
directly and mechanically: union-find over the passes' groupings and a set
difference on finding ids. Each walk's transcript is diffed against its own
structured return, and the workflow's own error report is read before any
result. The maintainer additionally reads the same repairs independently and
reports what the round missed as well as what it found.

**And a zero is not a result.** The repair audit preceding this round had 18
findings adversarially verified by agents told to default to REFUTED; that
returned zero byte-level, and eight refuters were then run against it anyway.
They upheld the zero — but an earlier audit of the same shape had all four of
its byte-level downgrades overturned by the same instrument. A shared
instruction is a shared premise. Zero is the trigger for the refute phase.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**, surviving the
refute phase — **and the next round, reading this round's own repairs, must
return zero too.** One clean round has never been enough: rounds 7, 9 and 13
each hit zero and rounds 8, 10 and 14 each found the defect in the repairs that
zero produced.
