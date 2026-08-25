# Cleanroom round 25 — findings

Protocol: ADR-0034, four phases, preceded by five repair audits in this
directory. Charter: [prompt.md](prompt.md).

## Verdict

**Zero byte-level ambiguities** — across all **26** findings, not the 21 the
round's own triage saw.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — nineteenth round running |
| Findings | **26** — 21 through the round's triage, **5 recovered from a dead agent** |
| Self-flagged byte-level | 0 (main round) and 0 (recovered) |
| Distinct defects, main round | **17** by union-find (passes reported 17/18/18) |
| Byte-level after three blind passes | **0** — main round and recovered set alike |
| Refute phase | fired on the recovered AMBIGUITY → **GRADE_STANDS** |
| Harness | 12 agents, **1 error**, five findings recovered from disk |

Byte-level history: … → 2 → 1 → 0 → 2 → **0**.

**G3 is not met.** This is the first half of its criterion for the fifth time.
Rounds 7, 9, 13 and 23 each hit zero, and rounds 8, 10, 14 and 24 each found the
next defect in the repairs that zero produced. Round 26, reading this round's
repairs, decides it.

## The harness failure, and why the verdict is over 26 and not 21

**The verifier walk died** on the StructuredOutput retry cap. It had completed
its work: a 61 KB transcript — the round's largest — carrying a full
certification procedure, a coverage walk, a multi-generation trace, and **five
findings**. Its structured return was lost, so those five never reached the
round's triage. All three passes reported `byte_level_count = 0` over a set
missing a fifth of the round's findings.

Taken at face value, this round would have been reported as zero byte-level on
21 of 26 findings. That is the shape that cost rounds 9, 13 and 15, and it is
why the standing rule reads the `<failures>` line first and recovers from disk
before believing any count.

**All five were recovered verbatim** and put through the three blind passes they
had missed, on the round's own lenses, with the walk's self-grades included in
the brief and marked explicitly as *not evidence*. All three passes graded all
five not byte-level.

**The one AMBIGUITY then went to a refuter**, because a finding that bypassed
the entire pipeline and carried only its author's grade is the weakest evidence
this protocol admits.

## verifier-01, the recovered AMBIGUITY

**§5.2 and §9.7 fix what a *partial* slack total means when a layer is rejected,
and say nothing when the rejection is at file scope.** Every clause naming which
claimants survive is written about a layer; F20 (directory CRC), F33
(cross-scope overlap) and F7 (a structure in the pre-trailer gap) all reject at
file scope *after* a live trailer is established, and §5.2's excusal from
reporting a total covers only rejection *before* one is. So a total is owed and
its value is unfixed.

The walk built a file at F = 576 and derived three defensible totals — **387,
496, 576** — and a second instance where the readings disagree over whether the
total is labelled *exact* or *partial*, a label §5.2 itself treats as normative.

**Not byte-level, and the refuter's ground is stronger than the walk's own.**
The walk argued that only a reported quantity changes. The refuter attacked the
verdict question directly and found §2.3's `[R-CNF-11]` forecloses it: "An
established violation takes priority … and *cannot establish* is available only
to a traversal that established no violation." Both instances are ones where the
verifier has *established* a violation, so both readings report **nonconforming**
and no certification flips. **GRADE_STANDS.**

Two of three passes graded it editorial, one design-decision; two PARTIAL, one
CONFIRMED. The gap is real and worth repairing.

## Harness integrity

- **12 agents started, 11 returned, 1 error** — reported on the `<failures>`
  line and not silently.
- **Every walk's transcript ids match its structured return exactly**, checked
  by independent id-scrape: reader 3, writer 4, verifier 5 (recovered),
  diagrams 5, register 3, adversary 3.
- **All three passes grouped all 21 main-round ids**, none missing, none extra,
  checked by set difference against the reporters' ids rather than by any pass's
  own coverage claim.
- **Union-find gives 17** against pass counts of 17, 18 and 18 — three merges,
  the passes agreeing on the defects and differing only on grouping.
- The recovery passes' `all_input_ids_seen` covered all five.

## Disclosures

All 11 returned agents disclosed. **Four explicitly answered the charter's new
"paths are context too" question**, each confirming the specification was where
the brief said it was — the first round in which that channel was checked rather
than assumed. The injected material was as before: a project instruction
pointer, an index of the maintainer's notes, and an environment block naming the
branch and recent commit subjects.

Both parts of the lineage gate return clean.

## Disposition

Not decided here. 17 distinct main-round defects (5 design-decision, 8
editorial, 3 register-bookkeeping, 1 figure, 1 graded not-a-defect) plus the
five recovered, of which `verifier-01` is the substantial one.
