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

The document was swept first, before any repair or menu — the step ADR-0094
recorded as missing. **Four findings needed no action:**

| Finding | Sweep result |
|---|---|
| reader-01 / diagrams-02 / register-01 | **Already Q-H4**, opened by ADR-0091. Three reporters found it independently this round |
| diagrams-03 / adversary-02 | **Already Q-I4**, opened by ADR-0092. Third independent report across three rounds |
| adversary-03 | **Already deferred** in round 24 (`reader-03`/`adversary-02`), owning section §2.3 |
| quiz-03 | Graded **not-a-defect** by triage — §20.5's citation is correct in context |

**Fixed — ADR-0098.** Each is checkable against a named rule or against
arithmetic, which is the class of repair this project's audits have not been
finding defects in.

| Finding | Repair |
|---|---|
| reader-02 | §23.1 cited "§20.3's shape (c)" for a user-metadata edit. §20.3 says in terms: "Editing user metadata **is not this shape** … as in (b)." **A defect ADR-0097 introduced the previous day**, citing the one shape the document rules out |
| register-02 | §9.6 cited rows F8 and F17 for a failure of `[R-CNT-06]`'s gates and omitted **F14**, the trailer CRC — one of the three ordered gates, and squarely a way the final 64 bytes are not a valid trailer |
| writer-02 | §11.1's Rationale said growth raising a grid count changes `entry_count`. False where another dimension's grid count is 0: (2,0) → (3,0) leaves the product at 0 |
| quiz-02 | L41's "that tile's length" had two antecedents, one of which makes the row unsatisfiable. Now "the previous stored tile's length" |

**Sent to the ledger.** §21.2's preamble is not dispositioned finding by
finding: it has drawn findings in **three consecutive rounds**, and Q-H4 and
Q-H5 already carve pieces off it without asking whether its design can work.
**Q-H6** asks what the paragraph is *for* — its excusing property ("geometry")
and its excepting property ("fixed across every major") are not complements, and
`[R-CNT-27]`'s floor satisfies neither, which is why ADR-0090 placed it,
ADR-0091 reverted that, and round 25 found it again from three walks at once.
That is the §21.7 → Q-I5 pattern in a different section.

The recovered `verifier-01` becomes **Q-C7** (what a partial slack total is when
the rejection is at file scope, with the three candidate values and the
exact-versus-partial label axis). The remaining design-decisions become **Q-B6**
(does step 4's bar reach a channel's sample type and the channel order),
**Q-B7** (is adding a record an independent change licensing a drop) and
**Q-I6** (why Appendix G pins some degrees of freedom and not others).

**Deferred, with named owning sections.** quiz-01 (§21.2's two properties — held
with Q-H6); writer-01 (§20.3 step 4's enumeration names padding-position content
but not pad-bit content or interleaved boolean bytes — §20.3); diagrams-05
(§20.3's shrink sentence states three consequences, two holding only where a
grid count falls — §20.3); diagrams-01 (shape (c)'s condition against step 4's
per-tile bar — §20.3); diagrams-04 (§4.7's Note against §7.2's field table —
§4.7); register-03 (§21.9's "Two do not" omits the power-of-two form of A and
A_slab — §21.9); verifier-02 through verifier-05 (§21.2, §5.2, §21.6 and §21.9
respectively).
