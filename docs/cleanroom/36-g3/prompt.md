# Cleanroom round 36 — G3 acceptance, the reading after the first half was reopened and repaired

Protocol: ADR-0034, with the refute phase standing since round 17, firing on a
zero since round 29, and on a unanimous uphold since round 32. Gate: PLAN.md
G3, *zero byte-level ambiguities* — and its second half, that the round reading
the previous round's repairs returns zero too, was met at round 34 and held at
round 35, whose chartered text returned zero. Round 35 found one byte-level
ambiguity outside that text, in a rule no recent cycle had touched, so the
criterion's first half was reopened and repaired. This round reads that repair,
the two decisions the maintainer took after it, and the audit of all three: a
zero here meets the criterion in both halves, and a flag in that text reopens
the second.

## Why this round exists

Round 35 read the repairs of the round before and the audit of them, and
returned **no** byte-level flag in that text: the criterion's second half, that
the round reading the previous round's repairs returns zero, held across one
more repair cycle. It returned one outside it. No reporter flagged it; all
three triage passes upheld one group byte-level against both reporters' own
grading, its refuter could not overturn the uphold, and the hand-check
confirmed it as new, in a section no recent cycle had touched. So the
criterion's first half, zero byte-level ambiguities anywhere, was reopened and
repaired. This round reads that repair, the two decisions the maintainer took
after it, and the audit of all three; a zero here meets the criterion in both
halves, and a flag in that text reopens the second.

The surface is wider than any recent round's — three decisions and the audit
of them. The first moved a writer's checksum duty from the structures it
*relocates* to the structures it *copies*, and repaired seventeen sentences
the round found wanting. The second restated the
writer tiers: obligations attach to operations rather than to an actor's
name, the third tier was renamed across fifteen sections, and the section
that specified it was rebuilt around three named cases of one operation. The
third changed a constant in a registry table, the flags of the record type
every file is built from, and with it turned a paragraph saying what no
commit does into a permission with a warning, and a sentence that forbade by
fusing two operations into one into a statement of what a bar binds and what
it does not. These are decisions, not wording repairs, and the text around a
decision was written under the rule it replaced. The audit that read them
before this round found twenty-nine defects, three of them byte-level,
repaired twenty-five in one further commit, and in repairing the three
decided two questions the decisions had not asked; you are reading those
repairs too, and they are the freshest text in the document.

**Do not read a clean passage as a checked passage.** The single most reliable
finding in this project's history is that heavy recent attention predicts
defects rather than correctness. Every changed line here was written since
the last round, and the audit that read them before this round found the next
defect in several.

You are told none of what those readers found, or where.

## The changed surface

**Thirty-one passages** — §2.3; §3.3; §4.7; §5.1; §5.2; §6.1; §6.2; §6.3; §6.4; §7.2; §7.3; §7.4; §9.1; §9.3; §9.7; §10.2; §10.3; §19.1; §19.3; §20.1; §20.3; §20.4; §20.5; §21.1; §21.6; §22.3; §23.1; §23.2; and Appendix C and Appendix G and Appendix H — 54 hunks over
4 commits, 282 lines inserted and 177 deleted. The document is
4,969 lines and about 49,700 words.

Six things that shape carries:

- **Obligations attached to operations rather than to an actor's name.**
  Where the document says which writer owes a duty by what the writer does —
  carries a structure forward, re-creates it, drops it; extends a file, or
  writes a new one — take a concrete tool and classify it by every test the
  text gives. A tool two tests classify differently is the finding; so is a
  duty stated of a class that one of its tiers cannot perform.
- **An actor renamed across many sections.** A sentence written for the
  narrow case can be false of the wide one. Where a sentence names the
  renamed actor or its operation, ask which of the operation's named cases
  the sentence was written for, and check it against each of the others
  separately; where the old name survives, ask whether the sentence needs
  the narrow word or the wide one.
- **A duty quantified over what an actor carries rather than where it places
  it.** List every kind of structure the actor can carry, and ask what the
  duty is over each — what is checked, against what, and what the actor does
  when the check fails. A kind the duty reaches with nothing to check it
  against is the finding, and so is a restatement elsewhere that still
  carries the old quantifier.
- **A registry constant changed, and a bar restated as a scope.** A constant
  in a registry table is read by every rule and every register row that
  tests it: find them all, and run the new value, the old value stored in a
  file, and each mixed value through each. And where a prohibition is stated
  as what it binds and what it does not, build the operation on each side of
  the line and ask whether any actor holding only the bytes can tell them
  apart; a bar no actor can see broken is a finding about the bar.
- **A permission over a container.** Where an actor MAY remove or replace a
  structure that holds other structures, list what it can hold and ask which
  rule governs each held thing when the container goes, and which when it
  stays; a held thing two rules dispose of differently is the finding.
- **Repairs to repairs.** Many rewritten sentences here are a second, third
  or fourth repair of a passage no round had read clean. In recent cycles
  repairs failed in a shape different from the defect they fixed — a scope
  corrected and a tense broken, a conflation split and an anaphor stranded, a
  list widened and its partition claim broken, an exception added and its
  gloss keyed on the wrong quantity, a verb list extended and a restatement
  left short, a restatement grounded in a rule and the rule's trigger left
  behind. Where a sentence reads as recently rewritten, ask what the rewrite
  opened, not only whether it is now true.

And one thing the last round taught about grading, which belongs to reporters
as much as to the passes: **a construction closed on a general rule is closed
only if the rule binds the actor in the construction.** Two reporters built
last round's fork and each graded it down on a sentence that the document
itself carves that actor out of. When you have carried a construction to
bytes and find yourself closing it, quote the closing sentence's actor and
the construction's actor side by side.

Twelve shapes are worth carrying into any passage, changed or not. The first
seven have each caught a real defect in this document; the eighth and ninth
were learned expensively, the tenth and eleventh are what recent cycles cost,
the twelfth is what most of this surface is made of, and the last round found
its fork under the first, in text no charter had named.

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
   yourself from the rule the list is about, then compare. Where the list is a
   partition — everything on one side or the other — find the member on neither,
   and the member on both.

6. **A rule keyed to a quantity that does not decide it.** Ask whether the named
   value actually determines the outcome. A derived quantity can hold still while
   the thing that decides the outcome moves. **What may a single commit do at
   once?**

7. **A word whose sense you supplied yourself.** Where a passage turns on an
   ordinary English word — *last*, *first*, *every*, *its*, *such*, *either*,
   *only*, *any*, *end* — census the document's own other uses before settling its
   reading.

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
    check that the current subject has that property.**

11. **A sentence that was rewritten to close a reading.** Where a passage bears
    the marks of recent repair — a qualifier bolted onto a universal, an
    antecedent spelled out, a count replaced by a list, a clause turned from
    restrictive to appositive, an exception explained — ask what the rewrite
    opened. And where a passage has plainly been rewritten more than once, do not
    repair it in your head: say which readings it still admits and leave the
    wording to human disposition.

12. **A rule whose reach was decided rather than repaired.** Where a permission
    now reads "in any commit", where a prohibition names every writer, where a
    bar became a list — ask what the sentence three paragraphs away still
    assumes, and whether the actor the rule now binds is the actor the
    neighbouring sentences address. A decision changes what a rule *does*; the
    text around it was written under the rule it replaced.

And one question that applies everywhere: **for any rule you can only defend by
reasoning you supply yourself, ask whether the document supplies it.**

Read the thirty-one first — then do not stop there. **Rounds 18, 19, 20 and 22
each found their survivor in text no recent round had touched**, round 21 found
one of its two by building a legal-but-degenerate file, round 30 found eleven of
its fourteen defects in text no recent round had touched, round 31 found its
survivor in a sentence the surface had not touched, in the step it touched most,
round 32 found its survivor in the sentence the surface had added last, round
33 found its survivor in a member of the list two audits and a round had read,
round 34 found no survivor and five of its twenty-one defects in text the
charter did not name, and round 35 found its survivor, and eight of its
twenty-two defects, in text the charter did not name.

This tells you **where to look and nothing about what the answers are.** You are
not being told what changed, why, or what any edit was meant to accomplish — and
you must not infer that a listed section is wrong, or that an unlisted one is
right.

## A convention you must check rather than assume

[R-CNF-01] says: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices
identified as non-normative."

**The exemption is by the label, not by the ">" marker.** A blockquote carrying no
such label is normative. At least one exists. An earlier briefing in this project
stated the rule the other way and a tool was built on that error; both were found
by a reader who checked the document instead of the briefing. Check the label.

**And check which side of that line a sentence is on before you judge it.** Several
of the passages in this surface are labelled blocks, and three are
non-normative appendices, restating rules stated in normative text sections
away; a defect in
an unlabelled block is a defect in normative text, a defect in a labelled one is
not the same finding, and saying which you have found is part of the finding.

## The document is hard-wrapped

A phrase you search for will often span a line break, and inside a blockquote the
wrap inserts `> ` as well — so a line-oriented `grep` will miss it, and a zero
from such a search is worth nothing. Search a short fragment that cannot wrap, or
normalise whitespace yourself before matching. **Before you rest any conclusion on
a zero, run the same search for a phrase you know is present in that passage.**
Round 29's quiz author did exactly that, found its own normalisation broken, fixed
it, and re-ran.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, not this file. Not
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`. Not `conformance/` — no
tooling, no vectors, no manifest. Not `spec/registry.json`. No git history, no web.

No agent reads the round's own output directory. The three triage passes are
additionally barred from each other's transcripts by name, and their transcripts
are written outside that directory so there is nothing there to find.

**Write any working file into your own private scratch directory**, named in your
charter, and nowhere else. In a recent round every lane wrote a file of the same
obvious name into one shared directory, one lane's script was silently replaced by
another's between two calls, and that lane executed the other's code and had its
numbers printed into its context. It found out only because it re-derived them.
Files already in an agent's scratch directory when it begins are a previous
attempt's, made under the same charter before the runtime restarted a stalled
agent; they are not read, and their presence is disclosed.

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
repeating its contents. This channel has been disclosed round after round by
agents who were asked to look, in several distinct forms, and no
mechanical check in this project can see any of it. In rounds 30 and 31
agents disclosed a form the harness itself creates: an over-long `sed` or `Read` output
that the runtime persisted to a file outside the specification. None opened it.
Do the same.

**Paths are context too.** If any file you are told to read is not where your
charter says, say so and say what you did to find it — a directory name can carry
information your charter deliberately withheld.

**And distrust your own inputs.** Recent rounds found a mislabelled hunk header, a
path that disclosed an expected verdict, a briefing that contradicted the
document, a briefing that stated the wrong size of the agent's own subject, a
charter that carried a count copied from the round before, and a file that changed
underneath a reader mid-session — none visible to any mechanical check, all found
by an agent that reported a discrepancy instead of picking a side. **If anything
you are handed disagrees with itself or with the document, say so.**

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a **reader**
implementer, a **writer** implementer, a **verifier** implementer, a **diagram
auditor**, a **register hunter**, an **adversary**, and a **quiz** authored,
answered and keyed by three agents blind to one another. Then three blind triage
passes, then the refute phase.

Standing charges: the register hunter checks **every cross-reference to a register
row against the row it lands on** and **recounts by hand every total the document
states about itself** — none of those totals is meant to have moved in this
surface, which is itself a claim to check; the diagram
auditor treats the conformance checklists and any table restating a rule as
figures, and **checks every worked example byte by byte, recomputing every
checksum it can rather than reading the printed value.**

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Flagged by reporters / survived triage, rounds 6–35: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 1/1, 2/2, 5/1, 1/0, 2/2, 0/0, 2/1,
4/2, 0/1, 1/0, 2/0, 1/1, 4/1, 1/1, 0/0, 0/1 — thirty rounds. Round 35's
reporters flagged none, and all three passes upheld one group byte-level
against both reporters' own grading: each reporter had built the construction
and then closed it on a general rule that does not bind the actor in it. The
uphold-refuter could not overturn it and the hand-check confirmed it as new,
outside the chartered text; the rule was requantified since, and this round
reads that repair.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Five discriminators this project learned the hard way.** First: §2.1 binds BCP
14 keywords "when, and only when, they appear in all capitals". A restriction
written in lowercase does not bound a permission written in capitals. **But do not
extend that to "a clause with no keyword has no force":** `[R-CNT-13]` carries none
and this document calls that very sentence a *prohibition*.

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

**Fifth, from the two cycles before this one.** Every byte-level flag raised in
them died on a governing clause **above the sentence quoted** — a paragraph fixing
the tense for everything below it, a clause stating that a passage is "the whole
of the test", a rule already stated unconditionally earlier in the same numbered
step, a layout-keyed table that a summary sentence was summarising. **Before you
grade a sentence, read the paragraph it lives in and the one before that.** A
finding that dies on a sentence you did not read costs the round more than one you
never filed. Since round 30 it is stated in the brief every agent reads, not only here.

## Disposition

Three independent triage passes deduplicate and re-judge every finding, blind to
each other; the refute phase then attacks every unanimous byte-level downgrade,
**every split verdict**, and — when nothing else fires — the zero itself.
Reconciliation is mechanical — union-find over the passes' groupings and a set
difference on finding ids — and **not** by any pass's own coverage claim. Each
walk's transcript is diffed against its own structured return, and the workflow's
error report is read before any result. A started agent with no result is checked
on disk before it is assumed empty; a transcript that shows the work and states no
verdict is not a verdict, and the finding is re-run rather than inferred.

**And a zero is not a result.** Round 28's zero was overturned by a refute phase
run over it by hand. Rounds 29 and 30 each produced splits, the splits fired the
refute phase, and each refuter's verdict was the weak direction for a weaker
model — so none was banked, and hand-checks settled them instead. Round 31
produced a unanimous uphold, which fired nothing, and the driver's hand-check
stood in for the refuter; since round 32 the phase attacks that shape too, and
in rounds 32 and 33 its refuter could not overturn the uphold. Round 34
produced no uphold and no downgrade, the zero-trigger fired, and its eight
attackers all stood, each hand-checked. Round 35 produced a unanimous uphold
no reporter had flagged, and its refuter stood. A refuter's
verdict in either direction is checked by hand before it is banked, and in
round 32 one refuter's verdict against a downgrade was not banked, on a
standard the document names by reference. **Zero is the
trigger for the refute phase**, and a refuter's verdict in the direction that
clears the gate is provisional until a hand-check confirms it. The round's full
result is rebuilt from the run's journal before any reconciliation, because the
workflow's output file truncates long strings.

Equally, **an empty return is not a clean result.** A reporter that finds nothing
should say what it did that would have found something.

**Convergence is not verification.** Twice in the cycle before this round, two
independent lanes converged on a claim a nearby line falsified — both missed a
rule forty lines up, and both read an item's bold headline and stopped without
reading its body. Two reporters agreeing means they agree, not that either looked.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully graded
with every divergence resolved by a spec fix or a key correction; zero findings
left without a disposition. This being an acceptance round, G3 additionally
requires **zero byte-level ambiguities outright**, surviving the refute phase —
and this round reads round 35's repair of the one fork it found, the two
decisions taken after it and the audit of all three, so a zero here meets the
criterion in both halves, and a flag in that text reopens the second. A flag
that is a known open question is recorded against that question and is not
new; a flag in text this round was chartered to read is.

**On prose defects, the maintainer's standing direction applies**: prose is not
expected to converge, and a round is not failed by finding wording that could be
misread. What matters is the *impact* of a misreading — its force, its reach, and
whether a wrong reading changes bytes. Where a passage proves genuinely
intractable to disambiguate, or reads as overly complicated, say so plainly and
leave it to human disposition rather than proposing a fourth rewording.
