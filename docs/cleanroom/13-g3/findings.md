# Cleanroom round 13 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**Zero byte-level ambiguities.** G3's acceptance criterion is met on this
round's evidence.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 27 — reader 2, writer 4, verifier 2, diagrams 6, register 5, adversary 5, quiz author 3 |
| Distinct defects | **17** |
| Self-flagged byte-level by reporters | **0** — the first round of thirteen |
| **Byte-level, after triage and hand-check** | **0** |

The changed surface was the largest of any round — 200 lines inserted and 54
deleted across 36 hunks in 29 sections — and it was the first to include
newly authored normative material rather than only repairs.

## A fourth shape of harness failure, and a recovery

**The quiz author died mid-response and the round did not stop.** Its
failure reached the log as `[quiz:author] failed`, and `slate` came back
`null` — so the answerer and the keyer each received a brief containing the
heading `## The slate` followed by nothing. Both returned fifteen
schema-valid answers to questions **they had invented themselves**, and
therefore to different questions. Nothing in either return was malformed.
A round reported from the structured results alone would have recorded a
graded quiz that never existed.

The answerer disclosed the empty slate in its first sentence and asked to be
re-run, which is the behaviour the disclosure field exists to produce. The
quiz was re-run in full — author, answerer and keyer — against the
identical commit, `spec/tarn.md` untouched in between.

That is the fourth distinct shape: a degenerate return (round 9), a dead
agent (round 11), a wrong detector (round 12), and now **a dead agent whose
absence silently emptied its consumers' inputs**. The pattern across all
four is that no downstream agent can tell a missing input from an empty
one, so the failure surfaces only in the workflow's own error line.

**The dead author's transcript was on disk and carried two findings its
return never delivered** — the round-11 shape again. Both were recovered.
Both proved to be independent corroborations of findings live walks had
also filed (the §11.1 Rationale divergence, and the §21.1 instance
criterion), so nothing was lost in substance. That was luck, not design.

## What the round found

All six walks were self-consistent: claimed = returned = transcript, 24
findings. All three triage passes covered all 24 ids exactly, with
`all_input_ids_seen` complete and no id in two groups. Union-find over the
three groupings merged them into 14 defects; the re-run quiz author added
three more, judged by hand.

**Two of the seventeen were defects introduced the day before, by the
commits this round was convened to read.**

- **§21.5's preamble excepted "an unassigned encoding"** from violation
  status, where only the *experimental* range is exempt. Encoding 0 and the
  reserved range 3–0x7F are unassigned too, and row R1 four lines below
  registers both as violations. Four reporters found it independently. The
  same overstatement had propagated to Appendix H and to §21.6's row — and
  the mechanical propagation check caught the §21.6 copy during the repair,
  which is exactly the class ADR-0073 built it for.
- **ADR-0074's own commit wrote two texts that disagree.** §11.1's
  Rationale says flatly "Extents grow; they do not shrink"; the normative
  rule in §20.3 step 4 bars only a change that alters what §14 fixes *for a
  tile the layer stores*. A shrink reaching no stored tile is permitted by
  the rule and forbidden by the Rationale. **The propagation check cannot
  see this shape**: it reports restatement sites a change did *not* sweep,
  and here both passages were written in the same commit. That is a second
  blind spot, beside the term-overlap one ADR-0073 already records.

Neither is byte-level. `[R-CNF-01]` makes a Rationale non-normative, §21.1
resolves a row-versus-rule divergence in the rule's favour, and §21.7
confirms a cross-generation declaration change has no single-file witness —
so no verifier verdict and no emitted byte turns on either.

The most-reported *pre-existing* defect was **§20.3 step 4's justification
sentence**, which the writer walk falsified in three ways: a filter change
whose mandated stride makes the shuffle the identity, a shrink whose new
padding position already holds fill, and the paragraph's own "an extent MAY
always grow" exception. The prohibition is sound; the sentence explaining it
claimed more than it can carry. Repaired by making the effect on a stored
tile the operative test and the enumeration illustrative of it.

## The quiz

15 agree / 0 diverge / 0 underdetermined, the seventh round running. Five of
the fifteen answers were recomputed by hand from the specification's rules
rather than accepted on the two agents' agreement — a trailer CRC over
stated field values (`8d 9a c0 98`), an interleaved in-tile byte offset
(1549), a packed planar bool edge tile including its pad bits (`e4 ff`), a
byte-shuffle at stride Q, and the smallest conforming file carrying one
layer record (192 bytes). All five reproduced.

The re-run author's three findings were judged directly. One duplicated the
register defect above. One was **refuted**: it read §19.1 step 4 (which
places a name-overrun at the open) against L23's *Detected* cell of "layer
access", where §21.1 defines that column as "the point **by which**
detection is due" — detecting earlier satisfies it, and the reporter had
quoted that sentence without applying it. One was confirmed:
`[R-CNF-02]`'s conduct carve-out named its single member in an em-dash
apposition that reads as exhaustive, while §6.2 creates a second (an
over-long pre-trailer gap is expressly conforming though `[R-LIF-02]` step
5 is a writer MUST).

## Disposition

All 17 dispositioned: **17 fixed, 0 deferred, 0 escalated.**

Beyond those already named: F33's gloss gained `[R-CNT-13]`'s third
reject-file overlap case; `[R-SLB-04]`'s trigger gained the run partition,
which a geometry growth can change without moving a byte; §5.2's
partial-total aside was re-punctuated, its four nested em-dashes having made
the inner clause's grammatical role genuinely ambiguous; §24 stopped
attributing a row-label policy to §21.1 that §21.1 does not state; §4.7's
six-column promise named its other two carve-outs; §21.7 gained the
undetectable-by-parse class (`[R-CNT-18]`'s nesting prohibition); §21.9's
finding-aid framing was scoped to the hard limits so it no longer reads onto
the guarantees table; Appendix H's verifier checklist gained the front
signature block, which `[R-CNT-04]` lets a reader defer and §2.3 does not;
and the "a geometry change renumbers ordinals" gloss became true.

Two decisions are recorded in
[ADR-0077](../../decisions/0077-the-instance-criterion-stated-and-the-ordering-key-decircularized.md):
**§21.1's instance criterion is now stated in the specification** rather
than asserted in an ADR — ADR-0076 applied a rule correctly to six cells and
described it wrongly, which nothing mechanical could catch — and **Appendix
G's record ordering key was de-circularized**, having contained the very
`extent_offset` the ordering fixes.

Register and corpus: **121 conditions over 268 instances, 320 vectors** (T22
gained the direction axis it shares with T14, L21 its two layout formulas).
