# Cleanroom round 24 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

**Round 23 returned zero byte-level ambiguities** — the fourth zero in
twenty-three rounds and the first since round 13. That is half of what this gate
asks. The other half is this round: G3 requires a round to return zero *and* the
next round, **reading that round's repairs**, to return zero too.

Rounds 7, 9 and 13 each hit zero. Rounds 8, 10 and 14 each found the next defect
in the repairs that zero produced. **This is the fourth attempt at the second
half, and every previous one failed.**

The repairs you are reading have been through **three repair cycles and three
audits** since round 23 saw the document. Each audit found defects in the
previous cycle's repairs; each was fixed; the last audit returned five confirmed
defects, four of them in the cycle before it. None of those, at any stage, was
byte-level.

So the changed text has been attacked harder than in any previous round, by
instruments that read the *commit* rather than the document. What a cold reader
can still find there is worth more than in any previous round.

You are told none of what those instruments found, or where.

## The changed surface

**Four passages — §20.5, §21.2, §21.5 and §21.7** — 37 lines inserted, 18
deleted. The document is 4,445 lines.

That is the net of three cycles, not one. Some of these lines have been written,
reverted and rewritten; at least one passage stands today at text a previous
cycle replaced and a later one restored. **Read each passage as it now reads,
not as a sequence of edits**, and do not assume that recent attention means it
is now right — three consecutive audits found the opposite.

**§21.7 is the most-worked passage in the document.** It accounts, by class, for
what no check detects. An enumeration there is not a convenience: it is a claim
that the listed cases *are* the cases, and a reader who trusts it will conclude a
witness exists where none does, or none where one does. It has been edited by
four consecutive cycles.

Four shapes are worth carrying into any passage, changed or not:

1. **Quantifier and scope.** *Four of the last six byte-level defects in this
   document have been quantifier or scope questions* — which records a licence
   covers, which placements a refusal reaches, which instances a limit bounds.
   Look at any rule stating a bound or a permission over a structure without
   saying which instances of that structure it ranges over.

2. **One quantity named where two are in play.** A rule can be perfectly correct
   about the thing it mentions while a sibling quantity of the same structure is
   governed by nothing. Name the structure, list everything it can carry, and
   ask what fixes each.

3. **Argument by analogy.** Where the document justifies one rule by pointing at
   another — "exactly as", "the same way", "for the same reason", "transposed
   from", "likewise" — put the two governing verbs side by side and read them
   word for word. An analogy can be sound for one member of a set and unsound
   for the next.

4. **A claim about *when* rather than *what*.** Several rules here say a check
   happens before or after another, or that one thing is established first. Ask
   what fixes the order, whether that rule is a MUST or a MAY, and whether
   anything downstream depends on the order being fixed.

And one question that applies everywhere: **for any rule you can only defend by
reasoning you supply yourself, ask whether the document supplies it.** A rule
whose correctness depends on a fact stated nowhere in this file is not a rule a
fresh implementer can apply, however right it is. If you find yourself saying
"this is fine because obviously X", check that X is written down.

Read the four passages first — then do not stop there. **Rounds 18, 19, 20 and
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
notes, a task list, or an environment block naming the repository, the branch
and recent commit subject lines. **None of it is part of the specification and
none of it is evidence about the specification.** Some of it names section
numbers and decision outcomes. Disregard all of it, and disclose that it
appeared without repeating its contents. Every agent in the three runs preceding
this round disclosed exactly that.

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

Flagged by reporters / survived triage, rounds 6–23: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 2/2, 5/1, 1/0.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Two discriminators this project learned the hard way.** First: §2.1 binds BCP
14 keywords "when, and only when, they appear in all capitals". A restriction
written in lowercase does not bound a permission written in capitals — that was
round 17's surviving defect. **But do not extend that to "a clause with no
keyword has no force":** `[R-CNT-13]` carries none and §21.7 calls that very
sentence a *prohibition*, and `[R-CNT-02]`, `[R-SER-01]` and `[R-SER-02]` are
the same construction. A previous charter asserted the stronger claim and it
caused a real defect to be under-graded.

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
difference on finding ids — **not** by any pass's own coverage claim, which in
round 23 was complete in the field the harness checks and corrupt in the field
it does not. Each walk's transcript is diffed against its own structured return,
and the workflow's own error report is read before any result.

**And a zero is not a result.** Round 23's own byte-level flag was downgraded by
all three passes and the refute phase upheld the downgrade — but an earlier
audit of that same shape had all four of its byte-level downgrades overturned by
the same instrument. A shared instruction is a shared premise. Zero is the
trigger for the refute phase.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**, surviving the
refute phase.

**If this round returns zero, G3 is met** — round 23 supplied the first half and
this round reading its repairs supplies the second. That is the first time this
project has been in a position to close the gate, and it is exactly the position
rounds 8, 10 and 14 were in when they failed it.
