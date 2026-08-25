# Cleanroom round 24 — findings

Protocol: ADR-0034, four phases, preceded by three repair audits in this
directory. Charter: [prompt.md](prompt.md).

## Verdict

**Two byte-level ambiguities. G3 is not met.**

Round 23 returned zero and supplied the first half of G3's criterion. This
round, reading round 23's repairs, was the fourth attempt at the second half —
and it failed the same way rounds 8, 10 and 14 did.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — eighteenth round running |
| Findings | 27, from seven reporters |
| Self-flagged byte-level | **2** (writer-01, adversary-01) |
| Distinct defects after union-find | **20** — 2 byte-level, 3 design-decision, 3 register-bookkeeping, 13 editorial (pass groupings 20/21/21) |
| Byte-level after three blind triage passes | **2** |
| Refute phase | **fired on nothing, correctly** — no downgrade and no split existed |
| Harness | 12 results, 0 errors; 8 retried attempts recovered and checked |

Byte-level history: … → 1 → 1 → 2 → 1 → 0 → **2**.

**All three passes upheld exactly the same two findings**, by membership and not
merely by count, and both were the two their reporters had self-flagged. Because
no pass downgraded either and no pass disagreed with another, the refute phase
had no target — which is the trigger working as specified, not the trigger
failing.

## Survivor 1 — writer-01, and it was in the ledger

**§20.5 never binds a compactor to `[R-LIF-02]`, leaving its durability
barriers and its pre-trailer pad length unfixed.**

`[R-LIF-02]` is invoked by name for a creator (§20.2, "both barriers, not one")
and for an appender (§20.3 step 6). §20.5 contains no occurrence of
`[R-LIF-02]`, "barrier" or "durable" — the walk grepped all three. A compactor
is a third tier (§20.1), `[R-LIF-01]` classifies its output as a whole-file
rewrite rather than a commit, and `[R-WRT-01]` binds it only to "every writer
requirement for the bytes they produce".

The construction: compactor P pads from the directory's end to the next 64-byte
boundary and emits F = 4,096. Compactor Q aligns its trailer to a 4 KiB device
block, pads 3,392 bytes further, and emits F = 8,192 with a 3,452-byte
pre-trailer gap. **Both files are conforming** — `[R-CNF-02]` expressly names
"§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad" among the writer
obligations whose violation is not a file-conformance violation — so no reader's
verdict separates them, and the emittable set moves.

**This is Q-A6.** Round 23's writer walk reported the same defect; round 23's
three triage passes graded it *design-decision*, and the maintainer's
disposition sent it to the ledger as an open question. Round 24's three passes
graded it **byte-level**, unanimously. A byte-level defect sat in
OPEN-QUESTIONS for a cycle. The grading changed between rounds rather than the
text, which is worth recording plainly: **a design-decision grade is not a
finding that something is not byte-level.**

## Survivor 2 — adversary-01

**§20.3 step 4 both permits and bars a shrink whose new padding positions
already hold the fill.**

Two sentences of `[R-WRT-04]` step 4 give opposite answers for one commit. The
first withdraws the bar's list as a standalone test and carves out "a new
padding position whose stored byte already holds the fill `[R-SER-05]` fixes" as
"not what this bars". The second, two paragraphs later, says "a shrink that
turns real positions into padding of a tile stored there is barred whether or
not the new state still stores it" — unconditionally.

The adversary showed the conflict is not an ellipsis: a new padding position
inside an already-stored tile can arise from a shrink and from nothing else,
every other declaration change being barred outright on other grounds. Appender
P emits a 448-byte generation-2 file; appender Q refuses. That byte sequence is
producible by no other conforming writer, since a creator and a compactor both
emit generation 1.

## Harness integrity

Read before any result was believed.

- **20 agents started, 12 returned.** The usage line reported 12 done and 0
  errors. Each of the eight without a result was checked on disk: **none had
  called StructuredOutput and none contained a single finding id** in files up
  to 376 KB. They were cut off mid-read and retried, and the retries are among
  the 12. READER, WRITER, VERIFIER and DIAGRAMS each appear once missing and
  once returned. **No findings were lost.**
- All six walks' `transcript_finding_count` matched their returned arrays.
- **All three passes grouped all 27 ids**, none missing, none extra — checked by
  set difference against the reporters' ids, not by the passes' own claims.
- Union-find over the three partitions gives **20** against pass counts of 20,
  21 and 21, so the passes agree on the defects and differ only on two merges.
- Byte-level membership is identical across all three passes, not just the
  count.

## Disclosures

All 12 disclosed. The injected material again included an index of the
maintainer's notes whose entry titles referenced prior-round findings and how
§21 relates to the vector corpus, alongside the environment block. Each agent
stated it opened none of the named files and that no conclusion rested on the
material. Both parts of the lineage gate return clean.

## Disposition

**Both byte-level survivors resolved.** `[R-LIF-02]` binds a compactor
(ADR-0093 decided it did not, and ADR-0094 reversed that against five
contradicting passages the audit found); §20.3 step 4's carve-out governs the
shrink, settled by a six-agent panel with an unprimed control (ADR-0093).

**The 18 non-byte-level defects**, dispositioned by the maintainer after a
document sweep. Two needed no action at all:

| Finding | Disposition |
|---|---|
| writer-04 — §23.1 omits unstoring a tile | **Already fixed** by ADR-0095, which replaced §23.1's closed count with a partition by consequence |
| writer-05 — R8 collapses `[R-MTA-04]`'s alternatives | **Already Q-I4**, opened by ADR-0092; round 24's register hunter re-reported it independently |

**Fixed — ADR-0096.** Both are checkable against a named rule, which is the
class of repair this project's audits have not been finding defects in.

| Finding | Repair |
|---|---|
| register-04 | R7's Condition cell gains the leading-U+FEFF alternative its own Instances cell already counted twice and §18.2 states |
| register-05 | **L16** takes F31's bound, not the reverse: F30 and L15 already register the one-half-zero case, so a *nonzero* extent slot has `extent_offset` ≥ 1 and "in 1-15" is the precise form. The finding's phrasing suggested changing F31; the sweep showed F31 was right |

**Sent to the ledger.** §21.7's eight findings are not dispositioned singly:
four ADRs have repaired that section in four days and it has drawn a cluster in
five consecutive rounds, so **Q-I5** asks what the section is *for* and what
its account must cover, with three options priced. The three design-decisions
become **Q-A7** (§20.5's version_minor floor turns on a fact a compactor cannot
obtain), **Q-H5** (which verdict a verifier reports for a foreign-major file a
row reaches — distinct from Q-H4, which asks which rows reach), and **Q-C5**
(whether §8.1's one unchecksummed live region owes a verifier report).

**Deferred, with named owning sections.** reader-03/adversary-02 and verifier-02
(§2.3's MU = 1 carve-out and where the sub-record verdict is stated — §2.3);
writer-02/quiz-01 (§20.5's index-regeneration trigger — §20.5); quiz-03
(§21.2's use of "geometry" — §21.2); verifier-01 with diagrams-02 (§5.2's
no-total-owed exemption against Appendix H's verifier checklist — §5.2, and
they are one defect seen from two sides); diagrams-03 (§21.6's trailer-mimic
row — §21.6); diagrams-04 (§4.7's presentation contract against §7.4's table —
§4.7).
