# 0132. Round 37's repair, and G3 declared met

- Status: Accepted (resolves round 37's repairable finding; records the
  maintainer's declaration of 2026-09-22 that gate G3 is met)
- Date: 2026-09-22
- Covers: §6.2's trailer table, the flags field's valid-values cell;
  PLAN.md §9's G3 status
- Confirm: none. The repair takes no decision about what a conforming actor
  may do. The declaration is the maintainer's own, given on 2026-09-22 on
  the record this ADR sets out, and this ADR records it rather than takes
  it.

## Context

Round 37 read the document over `96e4ad4..6c9470e` with this cycle's
decisions weighted first: ADR-0130's E1 and E2, ADR-0129's E3, §7.2's two
passages and step 4's scope sentence named as the text to read hardest, and
ADR-0131's three clauses with its erratum's two as the changed surface. It
ran on Sonnet throughout, nineteen agents at one launch, none refused, and
returned **six findings from two reporters, six distinct defects, and no
byte-level finding: none self-flagged, none upheld by any of three passes,
and the refute phase, firing on the zero, stood on six targeted refuters and
the round-wide attacker**, each answering in its own vocabulary. Decisions
E1, E2 and E3 drew two findings and both were found decided: the blocking
sentence for an unimplemented MU = 1 sub-record is stated five times across
three sections, and the one place the rewriter and creator positions diverge
is one the conformance predicate cannot see. The quiz was 15 of 15 on
verdicts by hand.

It is the second zero over these decisions from the same instrument. Round
36 returned 8 findings and no byte-level flag; round 37 returned 6 and none.
Both findings files recorded their zero and left the criterion to the
maintainer, because the instrument that returned them returns a third as
many findings as the one that set rounds 31 through 35's calibration lines,
and a count cannot tell a settled text from a weaker reader. **The
maintainer weighed that record on 2026-09-22 and declared G3 met.**

**What the round found** is one repairable clause, one question about a
closed list, and four groups declined or confirmed. This ADR makes the
repair and records the declaration with the record it rests on.

## Decision

1. **§6.2's flags cell names the class beside its tiers as three
   coordinate actors.** *"carried forward unchanged by an updater, appender
   or rewriter alike"* lets a reader take *updater* for a third kind, where
   `[R-CNF-06]` leaves none and §6.3's own statement of the rule reads *"by
   every updater under this text, appender and rewriter alike"*. The cell
   now uses that idiom: *"carried forward unchanged by every updater,
   appender and rewriter alike"*. A normative table cell; the rule it
   restates is `[R-CNT-08]`'s, which binds every updater whatever the
   cell's grammar, so no actor's obligation moves.

2. **Gate G3 is declared met, by the maintainer, on 2026-09-22.** PLAN.md
   §1 states the gate: *the final cleanroom round yields zero byte-level
   ambiguities*; the rounds' own convention added a second half, that the
   round reading the previous round's repairs returns zero too. The record
   the declaration rests on:

   - **Round 36** (`26b8066`): thirty-one passages over seven commits, the
     three decisions with two audits and the maintainer's rulings; 8
     findings, no byte-level flag, the refute phase standing on seven
     targeted refuters and the round-wide attacker; three wording repairs
     (ADR-0131), audited and repaired once more (ADR-0131's erratum).
   - **Round 37** (`3ec4b50`): the same decisions read again, weighted
     first, with those five clauses in front of it; 6 findings, no
     byte-level flag, the refute phase standing on six targeted refuters
     and the round-wide attacker. It is the round that read round 36's
     repairs, and it returned zero: both halves.
   - **The instrument.** Both rounds ran on Sonnet under the project-wide
     policy of 2026-09-21, after Opus refused every whole-surface brief of
     the cycle; their yields, 8 and 6 findings, are a third of rounds 31
     through 35's 24 to 29. The findings files say so and no passage was
     read as clean on a count. Rounds 34 and 35, on Opus, had already met
     the criterion's first half and then its second over ADR-0126 and
     ADR-0127's text; round 35's one fork outside that text was repaired
     (ADR-0128) and has since been read by two Sonnet rounds and three
     audits without a flag.
   - **Byte-level survivors, rounds 31 through 37**: 1, 1, 1, 0, 1, 0, 0.

   The maintainer's judgement is that two readings on this instrument, over
   decisions two audits had also read, meet the gate. The driver did not
   make that judgement and this ADR does not argue it; it records it, and
   what it rests on, so that a later reader can weigh the same record.

**Left to the maintainer, not reworded.** `[R-CNF-02]`'s three expressly
stated conduct-only cases are a closed list, and `[R-WRT-06]`'s refusal on
an unimplemented MU = 1 record has their shape: its refuter showed a creator
may emit, byte for byte, the file a rule-breaking rewriter would. Whether
the list gains a fourth member and `[R-WRT-06]`'s site the declaration, or
the general sentence is left to carry it, is a decision about §2.3's list
and is not taken here. Step 4's tie-break sentence stands as ADR-0131 left
it.

**Declined.** Figure (b)'s bracket, read this time against §5.1's
divider-to-divider convention: figure (a)'s two brackets abut and share a
divider, so the Example's own convention is forced by its layout, and the
row has been edited three times this cycle. The MU = 1 row label's missing
qualifier: the lead-in one sentence above states it, and the blocking
sentence carries it in terms. Two confirmations the reporter itself graded
as no defect.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors.
No reader, writer or verifier behaviour changes.

**PLAN.md §9's G3 row reads PASS**, with the declaration's date, the two
rounds, and the instrument named. M5 stays in progress: G1's verdict is
still the maintainer's to give, and the corpus and publication debts stand.

**The audit chain opens on this commit**, as it does after every repair
commit. With G3 declared, whether another cleanroom round is chartered is
the maintainer's; until an audit reads this commit or a charter hands it to
a round, `tarn_chain` reports it uncovered. One clause in a normative table
cell, restating a rule stated in terms one section away, is within what the
convention hands to a round; a one-lane audit of it is a twenty-minute run
if the maintainer wants the chain closed without one.

**The cleanroom protocol's standing instructions stay in force** for any
further spec commit: `[R-CNF-01]`'s label test, the repair-audit convention
(ADR-0081), the chain invariant (ADR-0097), and the instrument note in every
findings file and erratum.

**The repair list was ticked against the diff**: one item, one edit, +1/−1,
none deferred.

## Alternatives rejected

- **Leave G3 undeclared until an Opus or driver reading returns zero.**
  Rejected by the maintainer: those instruments refuse these briefs as
  written, and two Sonnet readings over decisions two audits had read is the
  record there is.
- **Declare G3 on round 36 alone.** Not taken then (ADR-0131): one zero from
  a new instrument was unmeasured. The second reading, weighted to the
  decisions, is what the maintainer waited for.
- **Repair `[R-CNF-02]`'s list in passing**, adding `[R-WRT-06]`'s refusal
  as a fourth stated case. Rejected here: a closed list is edited by
  decision, not beside a one-clause repair.

## Precedent

- **ADR-0131** and its erratum: the previous zero, its repairs, and the
  audit of them.
- **ADR-0127** and **ADR-0128**: rounds 34 and 35, where the criterion's
  two halves were first met and the first half reopened.
- **ADR-0055**: a gate declared on evidence the record can reproduce; G5's
  is computed, G3's is a judgement recorded with what it weighed.
- **ADR-0119**: the repair list against the diff.
