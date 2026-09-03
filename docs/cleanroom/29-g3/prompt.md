# Cleanroom round 29 — G3 acceptance

Protocol: ADR-0034, with the refute phase standing since round 17. Gate:
PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 28 returned **one** byte-level ambiguity, and the manner of it matters more
than the count. The round as run returned **zero** — no reporter flagged one and
none of the three triage passes upheld one — and that zero did not survive. A
refute phase run over it by hand established a byte-level fork in a group all four
readers had graded *editorial*, and every number in its construction reproduced
independently.

So this is another attempt at the first half of the criterion. That is the eighth.
Rounds 7, 9, 13, 23 and 25 each hit zero; rounds 8, 10, 14, 24 and 26 each found
the next defect in the repairs that zero produced; round 27 returned two, and
round 28 returned one.

**Do not read a clean passage as a checked passage.** The single most reliable
finding in this project's history is that heavy recent attention predicts defects
rather than correctness. The surface you are about to read has had more instrument
time spent on it than any other in this project — and every one of those passes
found defects in the text the pass before it had just repaired, including in
repairs written specifically to close the previous finding.

You are told none of what those instruments found, or where.

## The changed surface

**Five sections — §11.1, §18.2, §20.3, §21.1 and §21.7** — 137 lines inserted, 88
deleted, over seventeen hunks and sixteen commits. The document is 4,698 lines and
about 46,900 words.

That is a narrower surface than round 28 read, and a deeper one. It is not four
repair cycles laid side by side; it is **one section rebuilt twice and then cut
back**, with four other passages moved to follow it.

**One section changed category, not just wording.** §21.7 was an enumeration: a
long list of obligations, each with an account of why no check catches it. It is
now a **test** — a definition you are expected to apply, stated over a subject
with quantifiers that decide membership. In between, it was a test *plus* the old
enumeration kept as illustration; the illustration has since been removed
entirely. So the section you are reading has had two intermediate forms, and the
prose around it was written against all three at different times.

**That is a shape no previous round has read.** Earlier rounds audited repairs to
rules. This one reads a section whose *kind* changed, and the failure modes
differ:

- a passage elsewhere that cites the section for a fact it used to state and no
  longer does, or that describes it as the kind of thing it no longer is;
- a definition whose quantifiers do not do what the sentence claims they do —
  this is decidable by writing them out, and you should write them out;
- a term defined in one section and used in another on different terms;
- a claim about the section's own completeness that the section cannot carry;
- a reader who cannot actually apply the test, because it turns on something the
  document does not fix.

**Put the test to requirements yourself.** Take a dozen from across the document —
some you would expect it to catch, some you would not, some near the boundary —
and work out what it says of each. **A requirement the test does not decide, or
decides wrongly, is the highest-value finding available in this round**, and you
can settle it from the text alone. Report the ones it gets right as well: an
account of where a test works is what makes the report of where it fails
credible.

**The other four sections cash it out.** One numbered procedure gained a
prohibition and lost another, and the prose explaining both has been rewritten
several times. One section's normative completeness clause turns on the new test
and restates it. Two more apply the test's distinctions to particular cases. Check
each restatement against the definition **word for word, and quantifier for
quantifier** — this document restates rules deliberately, and a restatement that
drifts is its single most common defect.

## A convention you must check rather than assume

`[R-CNF-01]` says: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices
identified as non-normative."

**The exemption is by the label, not by the `>` marker.** A blockquote carrying no
such label is normative. At least one exists. An earlier briefing in this project
stated the rule the other way and a tool was built on that error; both were found
by a reader who checked the document instead of the briefing. Check the label.

**And this round more than any other, check which side of that line a sentence is
on before you judge it.** Text has moved across it in both directions in the
surface you are reading. A defect in an unlabelled block is a defect in normative
text; a defect in a labelled one is not the same finding, and saying which you
have found is part of the finding.

## The document is hard-wrapped

A phrase you search for will often span a line break, and inside a blockquote the
wrap inserts `> ` as well — so a line-oriented `grep` will miss it, and a zero
from such a search is worth nothing. Search a short fragment that cannot wrap, or
normalise whitespace yourself before matching. **Before you rest any conclusion on
a zero, run the same search for a phrase you know is present in that passage.**

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
repeating its contents. This channel has now been disclosed in seven distinct
forms by agents who were asked to look, and no mechanical check in this project
can see any of them.

**Paths are context too.** If any file you are told to read is not where your
charter says, say so and say what you did to find it — a directory name can carry
information your charter deliberately withheld.

**And distrust your own inputs.** Recent rounds found a mislabelled hunk header, a
path that disclosed an expected verdict, a briefing that contradicted the
document, a briefing that stated the wrong size of the agent's own subject, and a
file that changed underneath a reader mid-session — none visible to any mechanical
check, all found by an agent that reported a discrepancy instead of picking a
side. **If anything you are handed disagrees with itself or with the document, say
so.** Two agents caught a briefing error that way in the pre-round work for this
round, and both were right.

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

Flagged by reporters / survived triage, rounds 6–28: 33/5, 8/0, 5/2, 3/0, 7/1,
3/1, 6/1, 0/0, 1/1, 1/1, 1/1, 6/1, 1/1, 1/1, 1/1, 2/2, 5/1, 1/0, 2/2, 0/0, 2/1,
4/2, 0/1 — twenty-three rounds.

The discriminating question: **is the disputed file itself conforming?** If a
permissive reading lets a writer produce a file that carries a register-row
violation, `[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is conforming
and only one reading permits an actor to produce it, the set moves.

**Four discriminators this project learned the hard way.** First: §2.1 binds BCP
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

**A fifth, from the pre-round work for this round.** Three separate byte-level
flags died on a governing clause **eleven to fifty lines above the sentence
quoted** — a paragraph fixing the tense for everything below it, a clause stating
that a passage is "the whole of the test", a rule already stated unconditionally
earlier in the same numbered step. **Before you grade a sentence, read the
paragraph it lives in and the one before that.** A finding that dies on a sentence
you did not read costs the round more than one you never filed.

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

**And a zero is not a result.** Round 28's zero was overturned by a refute phase
run over it by hand, and the harness could not fire that phase itself because its
trigger was keyed to a reporter flag that did not exist. **Zero is the trigger for
the refute phase**, and this round's harness fires it on a zero.

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

**On prose defects, the maintainer's standing direction applies**: prose is not
expected to converge, and a round is not failed by finding wording that could be
misread. What matters is the *impact* of a misreading — its force, its reach, and
whether a wrong reading changes bytes. Where a passage proves genuinely
intractable to disambiguate, or reads as overly complicated, say so plainly and
leave it to human disposition rather than proposing a fourth rewording.
