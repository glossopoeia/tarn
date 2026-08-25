# Cleanroom round 25 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 23 returned zero. Round 24, reading its repairs, returned **two** — so the
gate's criterion reset, and this round starts a fresh attempt at its first half.

Both of round 24's survivors are resolved, and one of them the hard way: the
first repair chose a reading the document contradicted in five places, and had
to be reversed. The other was settled by a six-agent panel rather than in a
repair slot.

The text you are reading has been through **five repair cycles and five audits**
since round 24 saw it. Those audits found defects in four of the five cycles.
The last two returned almost clean — twelve findings against one cycle with
eleven refuted and none confirmed — but **the most recent repair of all is
unaudited**, because auditing every repair of every repair does not converge and
a fresh reading is what this round is for.

You are told none of what those instruments found, or where.

## The changed surface

**Seven passages — §11.1, §20.3, §20.5, §21.2, §21.3, §21.5, §23.1** — 49 lines
inserted, 17 deleted. The document is 4,477 lines.

That is the net of five cycles, not one. Several of these lines have been
written, found defective, rewritten, and in one case **reverted to the opposite
rule**. At least two passages stand today at wording an earlier cycle had
replaced. **Read each passage as it now reads**, and do not assume that heavy
recent attention means it is right — four of the five cycles introduced a defect
the next audit found.

Two passages are register rows whose cells were edited; one is a non-normative
Rationale; the rest are normative prose.

Five shapes are worth carrying into any passage, changed or not:

1. **Quantifier and scope.** *Four of the last six byte-level defects in this
   document have been quantifier or scope questions.* Look at any rule stating a
   bound or a permission over a structure without saying which instances of that
   structure it ranges over, and at any rule whose permission and whose
   consequence might be quantified over different generations.

2. **One quantity named where two are in play.** A rule can be correct about the
   thing it mentions while a sibling quantity of the same structure is governed
   by nothing. Name the structure, list everything it carries, ask what fixes
   each.

3. **Argument by analogy.** Where the document justifies one rule by pointing at
   another — "exactly as", "the same way", "for the same reason", "likewise" —
   put the two governing verbs side by side and read them word for word.

4. **A claim about *when* rather than *what*.** Where a rule says one check
   precedes another, ask what fixes the order and whether that rule is a MUST or
   a MAY. An ordering asserted as fact may be an actor's option.

5. **A closed count, or a list presented as complete.** Derive the members
   yourself from the rule the list is about, then compare. This document has had
   four counts found short in four cycles, every one written by enumerating from
   a reading of the passage rather than from the rule.

And one question that applies everywhere: **for any rule you can only defend by
reasoning you supply yourself, ask whether the document supplies it.** A rule
whose correctness depends on a fact stated nowhere in this file is not one a
fresh implementer can apply.

Read the seven first — then do not stop there. **Rounds 18, 19, 20 and 22 each
found their survivor in text no recent round had touched**, and round 21 found
one of its two by building a legal-but-degenerate file and asking what a table
said about it.

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
and recent commit subject lines. Some of it names section numbers and decision
outcomes. **None of it is part of the specification and none of it is evidence
about the specification.** Disregard all of it, and disclose that it appeared
without repeating its contents.

**Paths are context too.** If any file you are told to read is not where your
charter says, say so and say what you did to find it — a directory name can
carry information your charter deliberately withheld. That has happened in this
project, and it was caught only because an agent disclosed it.

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

Flagged by reporters / survived triage, rounds 6–24: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 2/2, 5/1, 1/0, 2/2.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Two discriminators this project learned the hard way.** First: §2.1 binds BCP
14 keywords "when, and only when, they appear in all capitals". A restriction
written in lowercase does not bound a permission written in capitals. **But do
not extend that to "a clause with no keyword has no force":** `[R-CNT-13]`
carries none and §21.7 calls that very sentence a *prohibition*, and
`[R-CNT-02]`, `[R-SER-01]` and `[R-SER-02]` are the same construction. A
previous charter asserted the stronger claim and it caused a real defect to be
under-graded.

Second, and it cuts the other way: `[R-CNF-12]` places SHOULD deviation outside
the register entirely, and `[R-CNF-05]` gates emission on file conformance. **A
dispute about what a SHOULD requires cannot move the emittable set**, however
different the resulting bytes.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind to
each other; the refute phase then attacks every unanimous byte-level downgrade
**and every split verdict**. Reconciliation is mechanical — union-find over the
passes' groupings and a set difference on finding ids — and **not** by any pass's
own coverage claim, which in round 23 was complete in the field the harness
checks and corrupt in the field it does not. Each walk's transcript is diffed
against its own structured return, and the workflow's error report is read
before any result. A started agent with no result is checked on disk before it
is assumed empty.

**And a zero is not a result.** An audit this week returned twelve findings with
eleven refuted, and the refute pass over its byte-level downgrades had to be run
twice — the first run's briefs sat in a directory whose name disclosed the
expected verdict. A shared instruction is a shared premise, and so is a path.
Zero is the trigger for the refute phase.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction; zero
findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright**, surviving the
refute phase — **and the next round, reading this round's repairs, must return
zero too.** One clean round has never been enough: rounds 7, 9, 13 and 23 each
hit zero, and rounds 8, 10, 14 and 24 each found the next defect in the repairs
that zero produced.
