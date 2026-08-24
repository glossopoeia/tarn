# Cleanroom round 23 — findings

Protocol: ADR-0034, four phases, preceded by the repair audit in
[repair-audit.md](repair-audit.md). Charter: [prompt.md](prompt.md).

## Verdict

**Zero byte-level ambiguities.** The fourth zero in twenty-three rounds, and
the first since round 13.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — seventeenth round running |
| Findings | 19, from seven reporters |
| Self-flagged byte-level | **1** (adversary-02) |
| Distinct defects after union-find | **17** — 5 design-decision, 9 editorial, 3 register-bookkeeping |
| Byte-level after three blind triage passes | **0** |
| Refute phase | fired on the one unanimous downgrade → **DOWNGRADE_STANDS** |
| **Byte-level after the refute phase** | **0** |
| Harness | 13/13, 0 errors, 111 minutes |

Byte-level history: … → 1 → 1 → 1 → 1 → 2 → 1 → **0**.

**G3 is not met yet, and this is only the first half of its criterion.** The
gate requires a round to return zero *and* the next round, reading that round's
repairs, to return zero too. Rounds 7, 9 and 13 each hit zero; rounds 8, 10 and
14 each found the next defect in the repairs that zero produced. This is the
fourth attempt at the second half.

## The one that was flagged, and what the refute phase did with it

**adversary-02 — JSON structural nesting depth is bounded nowhere.** The
adversary built a conforming 1.14 MiB user-metadata document of the form
`{"a":` ×200,000 + `1` + `}` ×200,000: a top-level object, BOM-free, one finite
number, one one-byte key per object, trivially sorted at every nesting depth,
valid UTF-8, well inside §21.9's 16 MiB row. RFC 8259's grammar carries no depth
bound and its §9 latitude is about implementations rather than about what a JSON
text is, so the document is well-formed and the file is conforming.

All three triage passes downgraded it independently — two grading CONFIRMED as a
design decision, one PARTIAL — so the refute phase fired, as a unanimous
downgrade always makes it. The refuter re-derived the byte arithmetic itself
rather than inheriting the reporter's example, tested the R7 route (the only one
that would move the emittable set), and found it barred: R7's condition is "not
well-formed JSON, or its top-level value is not an object", and a 200,000-deep
object is well-formed JSON. **DOWNGRADE_STANDS.**

It remains a real design question — a reader with a recursive-descent parser
meets a stack it cannot bound from any declaration — and it is recorded as one.

## The 17 distinct defects

**Design decisions (5)** — reader-01/adversary-04 (§21.9 states no guarantee
over any stored on-disk quantity), writer-01 (§20.5 binds a compactor to no
write procedure while §20.2 and §20.3 bind creator and appender), verifier-02 (a
certificate covers an unassigned-type record's extent uninspected and unnamed,
against `[R-MTA-10]`'s own stated principle), diagrams-02 (`[R-VEC-04]`'s
intact-sibling requirement and its range), adversary-02 (above).

**Editorial (9)** — reader-02, reader-03/adversary-01, diagrams-01,
diagrams-03, register-03, adversary-03, quiz-01, quiz-02, quiz-03.

**Register bookkeeping (3)** — verifier-01 (`[R-CNT-27]`'s 128-byte floor has no
position in §6.2's validation order), register-01 (R8 states as one range the
two alternatives `[R-MTA-04]` gives disjunctively), register-02 (R6 and R10 come
from one clause of `[R-MTA-04]` and name different governing rules).

**§21.7 is this round's cluster.** Five findings land on it — reader-02,
diagrams-01, adversary-03, quiz-01, and part of register-03. It is a passage
ADR-0089 touched days ago, and it is the section that accounts for what no check
detects, so an incomplete enumeration there is a claim the document cannot
carry. None is byte-level; together they are the strongest signal in the round.

## Harness integrity

Read before any result, per standing rule: the workflow's own failure line
(0 errors), then every walk's transcript against its structured return, then
`journal.jsonl`.

- **All six walks' `transcript_finding_count` matched their returned array**,
  and an independent id-scrape of each transcript found exactly the ids each
  return carried. No round-9-shaped loss.
- **All three triage passes claimed all 19 ids and all three grouped all 19** —
  but **pass 0's grouping carries a corrupt member id.** Its group for
  verifier-02 lists `member_ids: ["verifier-01x-placeholder-not-used"]` while
  its title, severity and rationale are plainly verifier-02's. The finding *was*
  judged, and graded identically to the other two passes, so nothing was lost.
  This is a **new failure shape**: an id list that is complete in the field the
  harness checks (`all_input_ids_seen`) and corrupt in the field it does not
  (`member_ids`). The mechanical union-find caught it; the pass's own coverage
  claim did not.
- **Union-find over the three partitions gives 17, and each pass reported 17** —
  and unlike round 8, the partitions genuinely agree: the same two merges
  (adversary-01 + reader-03, adversary-04 + reader-01) in all three.

## Disclosures

All 13 agents disclosed. Ten named an injected index of the maintainer's notes
and an environment block carrying the repository, the branch and recent commit
subject lines — **several of which name section numbers and decision outcomes.**
Each stated it opened none of the referenced files and that no conclusion rested
on the material, which is what ADR-0084's ACCESS paragraph asks for. The commit
subject lines are a channel the charter cannot suppress and the notes index
cannot explain; it is worth recording that this round's agents could see, in
their environment block, that recent commits named §18.2 and §21.9.

Both parts of the lineage gate return clean.

## Disposition

Decided by the maintainer: repair the §21.7 cluster and the register cells,
defer the editorial findings with named owning sections, and send the design
decisions to the ledger rather than to spec text (AGENTS.md rule 3). The
repairs were kept deliberately narrow — round 24 must read them, and rounds 8,
10 and 14 each found their defect in a clean round's repairs.

**Fixed — ADR-0090.**

| Finding | Repair |
|---|---|
| quiz-01 | §21.7's "only where" now governs one conjunct, not two; the witnessed cases are separate sentences |
| adversary-03 | the codec witness is *sometimes*, not unconditional — both halves are constructible around |
| diagrams-01 | the filter and a sample's byte offset are named as unwitnessed; §20.3 step 4 bars four things and §21.7 accounted for three |
| reader-02 | `[R-WRT-06]` has four trailer obligations, not two, and the output carries no record that it is a compaction output at all |
| register-03 | §20.5's "(F36, L25, R1)" now names all seven identifier spaces §10.2 tabulates |
| verifier-01 | F5 is a fifth row reaching a foreign-major file — `[R-CNT-27]`'s floor **precedes** §6.2's order rather than sitting in it |
| register-02 | R6's governing-rule cell names `[R-MTA-04]`, the rule that defines it, as R10 already did; four vectors re-emitted |
| register-01 | **not** fixed as proposed. R8 keeps one instance, and the register now says why — the reason existed, in a comment in `r_rows.py`, where no reader of the specification can see it |

register-01 is worth naming separately. The reporter asked for a split; the
counter-argument was already correct and already written down, in the corpus
build script. **That is the same failure ADR-0089 closed in three other
places** — a document that cannot show its own reasoning — and it is the first
instance of it found by a round rather than by an audit.

**Deferred, with named owning sections.** The nine editorial findings not in
the §21.7 cluster: reader-03/adversary-01 (§18.2), diagrams-03 (§4.7 and §7.2),
quiz-02 (§21.8), quiz-03 (§21.9). Each is decidable from the text as it stands;
none changes an obligation.

**To the ledger, not the spec.** The five design decisions become Q-A6
(does `[R-LIF-02]` bind a compactor), Q-C5 (must a certificate name an
unassigned-type record's extent), Q-H2 (does any row bound a *stored* quantity),
Q-H3 (is nesting depth bounded), Q-I3 (does `[R-VEC-04]`'s intact-sibling rule
reach ignore-record vectors). Each carries options and a settling test.

The register does not move: 121 conditions, 277 instances, 331 vectors.
