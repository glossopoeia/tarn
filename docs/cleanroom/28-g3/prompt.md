# Cleanroom round 28 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 27 returned **two** byte-level ambiguities — the highest count since round
21, and the first round in this project's history to return more than one from a
fresh first half. So the gate's criterion did not even reach its second half, and
this round starts another attempt at the first.

That is the seventh time. Rounds 7, 9, 13, 23 and 25 each hit zero; rounds 8, 10,
14, 24 and 26 each found the next defect in the repairs that zero produced; and
round 27 found two without any zero to follow.

**The text you are reading has changed more since the last round than in any
previous cycle of this project.** Four commits, three of them repair cycles and
one of them a change to the format itself. Two of the three repair cycles were
repairs of the previous cycle's repairs, and the audits that ran over them
confirmed defects in every one.

**Read each passage as it now reads.** Do not assume that heavy recent attention
means it is right; on this project's evidence it means the opposite. The most
recent audit found seven defects in text written four hours earlier by a process
that had already cross-checked every anchor and recomputed every number.

You are told none of what those instruments found, or where.

## The changed surface

**Twenty-five passages — §2.3, §3.1, §6.2, §9.2, §9.3, §9.6, §14.4, §20.1
through §20.5, §21.1, §21.2, §21.4 through §21.8, §22.5, §23.2, §24, and
Appendices A, D and G** — 228 lines inserted, 129 deleted, over thirty-six hunks.
The document is 4,649 lines.

That is the net of four commits, not one, and they are not all of a kind.

**One of them changes the format.** A structural field has been removed from a
fixed-size structure, and the fields that followed it have moved. The structure's
overall size did not change, and the bytes the removal freed were not reclaimed.
A quantity that the removed field used to supply is now carried by a different
field, on a property of that field which the document did not previously state
and now does.

**That is a shape no previous round has read.** Every round before this one
audited repairs to prose. This one reads a change to the bytes, and the failure
modes differ: a stale offset or width in a passage nobody thought to sweep; a
worked example whose arithmetic no longer follows; a rule that silently depended
on the removed field; a claim that was true of the old quantity and is merely
plausible of the new one.

**Two of the passages are a byte-level worked example and its annotation table.**
Check them against each other and against the structure's own layout, byte by
byte. A constant, an offset or a checksum stated in this document and wrong is
the highest-value finding available to you, and you can settle it by computing.

The rest are repairs: a register row struck and its label disposed of, a
register's stated totals, several restatements re-pointed at the new quantity,
and three non-normative appendices brought into line.

Ten shapes are worth carrying into any passage, changed or not. The first seven
have each caught a real defect in this document; the eighth and ninth were
learned expensively, and the tenth is what the most recent cycle cost.

1. **Quantifier and scope.** *Most recent byte-level defects in this document
   have been quantifier or scope questions.* Look at any rule stating a bound or
   a permission over a structure without saying which instances of that structure
   it ranges over, and at any rule whose permission and whose consequence might be
   quantified over different generations.

2. **One quantity named where two are in play.** A rule can be correct about the
   thing it mentions while a sibling quantity of the same structure is governed by
   nothing. Name the structure, list everything it carries, ask what fixes each.

3. **Argument by analogy.** Where the document justifies one rule by pointing at
   another — "exactly as", "the same way", "for the same reason", "likewise" — put
   the two governing verbs side by side and read them word for word.

4. **A claim about *when* rather than *what*.** Where a rule says one check
   precedes another, ask what fixes the order and whether that rule is a MUST or a
   MAY. An ordering asserted as fact may be an actor's option.

5. **A closed count, or a list presented as complete.** Derive the members
   yourself from the rule the list is about, then compare.

6. **A rule keyed to a quantity that does not decide it.** Ask whether the named
   value actually determines the outcome. A derived quantity can hold still while
   the thing that decides the outcome moves. **What may a single commit do at
   once?**

7. **A word whose sense you supplied yourself.** Where a passage turns on an
   ordinary English word — *last*, *first*, *every*, *its*, *such* — census the
   document's own other uses before settling its reading.

8. **A universal that a degenerate but legal case falsifies.** Every sentence
   saying a thing happens to *every*, *any*, or *no* member of a class is a claim
   about the whole class. Build the smallest legal member you can — one tile, one
   channel, extent 1, a single group, a value that is already what the rule would
   set it to — and check the sentence against it.

9. **A rule whose object is defined so precisely that it excludes its own
   exceptions.** Where a rule says what kind of thing it governs, check whether
   some exemption or permission that used to reach the governed thing now sits on
   the *other* side of that definition. A definition that tightens can sever a
   rule from the text that qualified it, and neither passage need change a word.

10. **A sentence re-pointed at a different quantity.** Where a rule, a gloss or a
    bound now names a quantity other than the one it used to name, its truth may
    have rested on a property the old quantity had and the new one does not — a
    range it could reach, a thing it counted, a pair it could tell apart. **Ask,
    of every such sentence, which property of its subject makes it true, and then
    check that the current subject has that property.** A ceiling, an identity
    claim, and a restated bound have each failed this way. The sentence will read
    perfectly, because it was true when it was written about something else.

And one question that applies everywhere: **for any rule you can only defend by
reasoning you supply yourself, ask whether the document supplies it.**

Read the twenty-five first — then do not stop there. **Rounds 18, 19, 20 and 22
each found their survivor in text no recent round had touched**, round 21 found
one of its two by building a legal-but-degenerate file, and the audits of the
last two cycles repeatedly found their clearest defects in passages that were in
no hunk at all.

This tells you **where to look and nothing about what the answers are.** You are
not being told what changed, why, or what any edit was meant to accomplish — and
you must not infer that a listed section is wrong, or that an unlisted one is
right.

## A convention you must check rather than assume

`[R-CNF-01]` says: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices
identified as non-normative."

**The exemption is by the label, not by the `>` marker.** A blockquote carrying no
such label is normative. At least one exists. An earlier briefing in this project
stated the rule the other way and a tool was built on that error; both were found
by a reader who checked the document instead of the briefing. Check the label.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, not this file. Not
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`. Not `conformance/` — no
tooling, no vectors, no manifest. Not `spec/registry.json`. No git history, no web.

No agent reads the round's own output directory. The three triage passes are
additionally barred from each other's transcripts by name, and their transcripts
are written outside that directory so there is nothing there to find.

A conclusion you reach because a test vector or an ADR told you is not evidence
that the specification says it, and this gate's whole claim is that the document
stands alone. A disclosed breach is a usable result; an undisclosed one poisons
the round.

**Context you did not ask for.** Your runtime may place material in your context
before you begin — a project instruction file, an index of the maintainer's notes,
a task list, or an environment block naming the repository, the branch and recent
commit subject lines. Some of it names section numbers and decision outcomes, and
the most recent commit subjects describe the very change you are reading. **None
of it is part of the specification and none of it is evidence about the
specification.** Disregard all of it, and disclose that it appeared without
repeating its contents. This channel has now been disclosed in six distinct forms
by agents who were asked to look, and no mechanical check in this project can see
any of them.

**Paths are context too.** If any file you are told to read is not where your
charter says, say so and say what you did to find it — a directory name can carry
information your charter deliberately withheld.

**And distrust your own inputs.** Recent audits found a mislabelled hunk header, a
path that disclosed an expected verdict, a briefing that contradicted the
document, and a file that changed underneath a reader mid-session — none visible
to any mechanical check, all found by an agent that reported a discrepancy instead
of picking a side. If anything you are handed disagrees with itself or with the
document, say so.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a **diagram
auditor**, a **register hunter**, an **adversary**, and a **quiz** authored,
answered and keyed by three agents blind to one another. Then three blind triage
passes, then the refute phase.

Standing charges: the register hunter checks **every cross-reference to a register
row against the row it lands on** and **recounts by hand every total the document
states about itself**; the diagram auditor treats the conformance checklists and
any table restating a rule as figures, and **checks every worked example byte by
byte, recomputing every checksum it can rather than reading the printed value.**

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Flagged by reporters / survived triage, rounds 6–27: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 1/1, 2/2, 5/1, 1/0, 2/2, 0/0, 2/1,
4/2 — twenty-two rounds.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Four discriminators this project learned the hard way.** First: §2.1 binds BCP
14 keywords "when, and only when, they appear in all capitals". A restriction
written in lowercase does not bound a permission written in capitals. **But do not
extend that to "a clause with no keyword has no force":** `[R-CNT-13]` carries none
and §21.7 calls that very sentence a *prohibition*.

Second, cutting the other way: `[R-CNF-12]` places SHOULD deviation outside the
register entirely, and `[R-CNF-05]` gates emission on file conformance. **A dispute
about what a SHOULD requires cannot move the emittable set.**

Third: a defect confined to genuinely non-normative text usually cannot move the
emittable set — **but check the label before relying on that**, and note that a
non-normative block disagreeing with the normative text it glosses is itself the
finding, wherever it lands.

Fourth, and it cost this project a headline verdict: **`[R-CNF-05]` is two
sentences and the second does not swallow the first.** "A writer MUST emit only
conforming files. Writer conformance is semantic: this specification does not
promise canonical bytes, and two conforming writers given identical input MAY
produce different conforming files." The second licenses divergence *within* what
the rules leave open; it does not license violating a rule. Read as though it did,
no writer requirement could ever be byte-level and this gate would be vacuous.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind to
each other; the refute phase then attacks every unanimous byte-level downgrade
**and every split verdict**. Reconciliation is mechanical — union-find over the
passes' groupings and a set difference on finding ids — and **not** by any pass's
own coverage claim. Each walk's transcript is diffed against its own structured
return, and the workflow's error report is read before any result. A started agent
with no result is checked on disk before it is assumed empty; a transcript that
shows the work and states no verdict is not a verdict, and the finding is re-run
rather than inferred.

**And a zero is not a result.** A byte-level flag has been downgraded and restored
by refuters more than once, and a downgrade has been overturned only because a
refuter insisted on the distinction between *the reporter described it imprecisely*
and *the text is correct*. **Zero is the trigger for the refute phase.**

Equally, **an empty return is not a clean result.** A recent audit had five of
seven lanes report nothing with no evidence of having looked, and the fix was to
require the searches run, the numbers derived, and the candidates rejected. A
reporter that finds nothing should say what it did that would have found
something.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully graded
with every divergence resolved by a spec fix or a key correction; zero findings
left without a disposition. This being an acceptance round, G3 additionally
requires **zero byte-level ambiguities outright**, surviving the refute phase —
**and the next round, reading this round's repairs, must return zero too.**
