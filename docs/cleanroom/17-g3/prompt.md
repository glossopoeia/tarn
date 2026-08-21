# Cleanroom round 17 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 16's triage returned zero byte-level findings. A refute-only pass
overturned it: the finding was real, and three careful readers had
downgraded it together because they shared a premise none of them tested.
Four byte-level defects were fixed as a result, **two of them in text
written during round 16 itself, within an hour of being committed.**

This round reads those repairs. Sixteen rounds now support two claims about
this process, and both shape the charters:

- **No two consecutive rounds have ever come back clean.** Every round that
  found nothing was followed by one that found a defect in the repairs that
  round produced.
- **A unanimous downgrade is not evidence.** Blind triage passes are
  independent in reasoning, not in framing; they inherit the reporter's
  example and its limits along with it.

**The changed surface is 64 lines inserted and 29 deleted across 15 hunks,
touching 11 sections** — §2.4, §6.1, §11.1, §19.3, §20.3, §20.4, §20.5,
§21.4, §21.5, §21.7 and Appendix G, with three hunks in §20.5 and two each
in §20.3 and §21.7.

Four properties are given to the walks, none of which says what any answer
is. One passage here is on its **fifth revision**, having been rewritten in
each of the last four rounds. **Two repairs were written and corrected
within the same hour**, the correction fixing a contradiction the first
repair introduced. **Several turn on a tense or a quantifier** — which
generation a rule speaks about, which set of tiles it ranges over — because
that is the shape every recent defect has had. And **one repair narrowed an
enumeration while another widened a licence**, both of which tend to
overshoot.

## What is new in the protocol

**A refute-only pass is now a standing phase**, not an ad-hoc follow-up. It
fires on every group where a reporter flagged byte-level and no triage pass
upheld it. Its only instruction is to overturn the downgrade; it is told to
attack the shared premise rather than the finding, and is handed the
discriminating test — *is the disputed file itself conforming?* — as a
stated rule rather than left to derive it. The triage charter now says so,
so that passes state their premises explicitly enough to be attacked.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes,
not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or
`README.md`. Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

No agent reads the round's own output directory. The three triage passes are
additionally barred from each other's transcripts by name.

A conclusion you reach because a test vector or an ADR told you is not
evidence that the specification says it, and this gate's whole claim is that
the document stands alone. A disclosed breach is a usable result; an
undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a
**reader** implementer, a **writer** implementer, a **verifier**
implementer, a **diagram auditor**, a **register hunter**, an **adversary**,
and a **quiz** authored, answered and keyed by three agents blind to one
another. Then three blind triage passes, then the refute phase.

Standing charges: the register hunter checks **every cross-reference to a
register row against the row it lands on** and **recounts by hand every
total the document states about itself**; the diagram auditor treats the
conformance checklists and any table restating a rule as figures, and checks
every worked example byte by byte.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not defects;
unresolvable forward references into them are reportable and expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Sixteen rounds: 33 flagged / 5 survived; 8/0; 5/2; 3/0; 7/1; 3/1; 6/1; 0/0;
1/1; 1/1; 1/1.

The discriminating question, now stated in the charters rather than left to
judgement: **is the disputed file itself conforming?** If a permissive
reading lets a writer produce a file that carries a register-row violation,
`[R-CNF-05]` bars every conforming writer from emitting it under both
readings and the emittable set does not move. If the disputed file is
conforming and only one reading permits an actor to produce it, the set
moves.

## Disposition

Three independent triage passes deduplicate and re-judge every finding,
blind to each other; the refute phase then attacks every unanimous
byte-level downgrade. The three-way reconciliation is done by the
maintainer's agent directly, not delegated, and mechanically: union-find over
the passes' groupings and a set difference on finding ids. **Each walk's
transcript is diffed against its own structured return, and the workflow's
own error report is read before any result.** The maintainer additionally
reads the same repairs independently, and reports what the round missed as
well as what it found.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction;
zero findings left without a disposition. This being an acceptance round, G3
additionally requires **zero byte-level ambiguities outright** — and, after
round 16, a zero that has survived the refute phase.
