# Cleanroom round 15 — G3 acceptance

Protocol: ADR-0034. Gate: PLAN.md G3, *zero byte-level ambiguities*.

## Why this round exists

Round 13 met G3's criterion. Round 14 read round 13's repairs and found a
byte-level defect in one of them. This round reads round 14's repairs.

That is now the project's most reliable finding about itself: **every round
that has hit zero has been followed by a round that found a defect in the
repairs the zero round produced.** Rounds 7, 9 and 13 each hit zero; rounds
8, 10 and 14 each found the next defect in the previous round's own text.
Fourteen rounds have not yet produced two clean readings in a row.

So this round is not asking whether the document is clean. It is asking the
narrower question that has actually discriminated: **do round 14's repairs
hold, read cold?**

**The changed surface is 100 lines inserted and 41 deleted across 18 hunks,
touching 10 sections** — §5.2, §11.1, §16.2, §20.3, §20.5, §21.1, §21.2,
§21.7, §21.3, and Appendix G. It is concentrated: three hunks in §20.3,
three in §21.1, three in Appendix G.

Two facts about it are given to the walks, and neither says what any answer
is. **One of these repairs was itself the repair to a byte-level defect** —
the highest-risk class of text there is, written by someone who had just
persuaded themselves they understood a subtle question. And **one rule in
this set has been rewritten three rounds running**, narrowing each time,
which makes it a rule whose author has been wrong about it twice rather
than a rule now known to be right.

Both of ADR-0073's recorded blind spots remain live: the propagation check
is a term-overlap heuristic that cannot see two passages contradicting each
other without shared vocabulary, and it cannot see two passages written to
disagree in the same commit — which is the shape of every repair round.

## Access rule

Each agent reads **`spec/tarn.md` and nothing else.**

Not `docs/` — no ADRs, no findings from earlier rounds, no research notes,
not this file. Not `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, or
`README.md`. Not `conformance/` — no tooling, no vectors, no manifest. Not
`spec/registry.json`. No git history, no web.

No agent reads the round's own output directory. The three triage passes
are additionally barred from each other's transcripts by name.

A conclusion you reach because a test vector or an ADR told you is not
evidence that the specification says it, and this gate's whole claim is
that the document stands alone. A disclosed breach is a usable result; an
undisclosed one poisons the round.

Every conclusion cites section numbers and requirement IDs.

## Roles

Run independently, in parallel, with no visibility of each other: a
**reader** implementer, a **writer** implementer, a **verifier**
implementer, a **diagram auditor**, a **register hunter**, an
**adversary**, and a **quiz** authored, answered and keyed by three agents
blind to one another.

Standing charges: the register hunter checks **every cross-reference to a
register row against the row it lands on** and **recounts by hand every
total the document states about itself**; the diagram auditor treats the
conformance checklists and any table restating a rule as figures, and
checks every worked example byte by byte.

## Finding taxonomy

**AMBIGUITY** (location, permitted readings, which you picked and why),
**CONTRADICTION** (both citations, quoted), **OBSERVATION** (decidable but
disproportionately expensive). Reserved values and sections are not
defects; unresolvable forward references into them are reportable and
expected.

## The byte-level test

> Does resolving this change which byte sequences a conforming
> implementation may emit, or must accept or reject?

Fourteen rounds: 33 flagged / 5 survived; 8/0; 5/2; 3/0; 7/1; 3/1; 6/1;
0/0; 1/1.

Two cautions carried into this round's triage charter, both earned last
round. Two of three passes upheld the surviving finding while asserting no
text decided it, when a definition in §3 decided part of it and only the
third pass found it — so search for the deciding sentence as hard as you
would search to refute. And round 13 graded a structurally similar finding
the opposite way, correctly: the two differ on whether the disputed bytes
were emittable by some other conforming actor, a distinction to make
explicitly rather than by feel.

## Disposition

Three independent triage passes deduplicate and re-judge every finding,
blind to each other. The three-way reconciliation is done by the
maintainer's agent directly, not delegated, and mechanically: union-find
over the passes' groupings and a set difference on finding ids. **Each
walk's transcript is diffed against its own structured return, and the
workflow's own error report is read before any result.** The maintainer
additionally reads the same repairs independently, and reports what the
round missed as well as what it found.

## Pass criteria

Every implementer walk correct against the drafter's intent; the quiz fully
graded with every divergence resolved by a spec fix or a key correction;
zero findings left without a disposition. This being an acceptance round,
G3 additionally requires **zero byte-level ambiguities outright**.
