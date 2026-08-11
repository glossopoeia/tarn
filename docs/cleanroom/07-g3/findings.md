# Cleanroom round 7 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**G3's byte-level criterion is met — zero byte-level ambiguities, for
the first time in seven rounds.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 63 — reader 8, writer 11, verifier 11, diagrams 9, register 12, adversary 12 |
| Flagged byte-level by their reporter | 8 |
| Distinct defects after three-way dedup | **44** (all three passes independently reached 44) |
| **Byte-level, after triage** | **0 — unanimous across all three passes** |
| Consensus status | 25 CONFIRMED · 17 PARTIAL · 2 REFUTED |
| Severity | 32 editorial · 8 register bookkeeping · 2 figure · 2 none |

The gate is not yet *closed*: ADR-0034 also requires zero findings left
without a disposition, and the 44 are undispositioned. What is settled
is the criterion that has failed six times running.

## The trend, stated plainly

| Round | Byte-level defects | Quiz |
|---|---|---|
| 3 | 4 | — |
| 4 | 4 | — |
| 5 | 3 | — |
| 6 | 5 | 14 / 1 diverge |
| **7** | **0** | **15 / 0 / 0** |

Two numbers moved together, and the second is the one worth trusting.
Reporters self-flagged 33 findings byte-level in round 6 and 5 survived;
this round they flagged 8 and none survived. Fifteen pointed byte-level
questions, authored by one agent, answered cold by a second and keyed
independently by a third, produced no divergence and — the stronger
signal — **no question either agent judged underdetermined.** Round 6
scored 14/1. The pilot round scored 15/15 on a document a tenth this
size.

## What the round caught that mattered

**§20.4's table now forbids every append — and I introduced it one commit
before the round ran.** ADR-0061's propagation replaced the table's
header. The old header scoped the whole table to *"record types the
updater does not implement"*; the replacement opens *"Persistence governs
every record type"*, and §7.3 fixes the layer record at MU = 1. The MU = 1
row reads *"Retain byte-identical. The updater MUST NOT modify the scope
the record governs"* — which, applied to a layer record, forbids every
append §20.3 defines. The writer walk hit it while tracing an append and
two triage passes confirmed it independently.

It is not byte-level: the cell's own gloss (*"an unknown critical record
at layer scope"*), `[R-CNF-06]`'s scoping to records an updater does not
understand, and Appendix H all recover the intended reading, and the
restrictive reading yields an updater that refuses to act rather than one
that emits different bytes. But it is a self-inflicted contradiction in
text that had existed for exactly one commit, and it is the clearest
argument this round could have made for running a cleanroom pass after
every substantive edit rather than every several.

**A violation the register does not carry.** `[R-MTA-07]` states that a
file carrying a standardized key outside its listed scope *"is
nonconforming, and a verifier detects it"* — and no row of §21.2–§21.5
registers the condition. Verified directly: the phrase *"standardized
key"* occurs in §18.4 and nowhere in §21. §21.1 makes register
completeness normative, so the omission is a defect by the document's own
terms.

This one is not bookkeeping, despite where triage filed it. The register
is partitioned by *reader* outcome, and this condition has none — a
reader ignores the key either way, so `[R-CNF-07]`'s four-value
vocabulary has no value that fits. §21.7 does not fit either, since that
is the inventory of what *no check* detects and a verifier detects this.
The condition is real, detectable, and unfileable under the present
taxonomy. It also moves G5's denominator: the register is 125 conditions
and should be 126, with a vector owed.

**A live structure no checksum covers.** §5.2 defines a structure to
include *"a record extent … whatever the record's type"*, §21.6 registers
an experimental-range MU = 0 record as conforming, and §7.2 lets it carry
an extent — but §8.1's checksum map has rows for only two record extents.
So a conforming file can carry a live-state structure covered by no
checksum, and §9.7's *"each verifies against the checksum covering it"*
is vacuous for it. §22.3 says two residues are stated rather than
defended; this is a third it does not name.

**§21.7 calls itself an inventory it is not.** It names five requirements
that fail the detectability gate and omits every §20 updater and
compactor obligation, `[R-CNT-08]`'s copy-forward, `[R-IDX-01]`'s
disk-ordinal entry order, and `[R-PRV-01]` — all MUST-level, all without
a single-file witness, all of exactly the kind already listed.

## The eight byte-level claims, and why none survived

Each was re-judged by three passes and the two strongest were then
checked by hand against the text.

- **The register-versus-§19 fork** (a top-level user-metadata record with
  extent slot (0, 0): reject-file under §21.2's F24, servable under
  §19.1's enumerated open). Refuted by `[R-CNF-04]`, quoted from the
  document: *"A reader MUST detect the violations enumerated in the error
  register (§21) and apply the outcome class this specification assigns
  to each."* One permitted reading, so no fork. §19's under-enumeration
  is a real defect for implementers and stays on the list as editorial.
- **The lz4 cap on a layer with zero addressed tiles.** Refuted by the
  rule's own quantifier — `[R-COD-07]` binds *"a layer any of whose
  addressed tiles' decoded size exceeds 0x7E000000"* — and by §21.6's row
  affirming a zero-extent dimension as *"A valid, empty layer: zero
  addressed tiles"*. The empty quantification is vacuously satisfied and
  the layer is conforming; a rejecting verifier is the nonconforming
  party. The reporter's offered second instance refutes itself, since
  `[R-ENC-04]` carries no addressed-tile quantifier at all.
- The remaining six reduced the same way: the rule states the verdict, so
  both implementations reach it.

The over-claim ratio fell from 33:5 to 8:0, which is the reporters
calibrating, not the document changing underneath them.

## Two honest caveats

**The triage passes were anchored.** All three were told round 6's
calibration — 33 flagged, 5 survived — which biases toward downgrading. I
mitigated it by verifying the strongest candidates against the text
myself rather than accepting the verdicts: `[R-CNF-04]`, `[R-COD-07]`
with §21.6's row, and `[R-MTA-07]`'s absence from §21 were each read
directly, and all three held. A reader who wants to discount this round
should discount it here first.

**One triage pass overstated its own coverage.** The skeptic pass wrote
*"All 63 input findings appear in exactly one judgement, and none was
dropped"* and then itemised a tally summing to 63 — while actually citing
62 unique ids. It dropped `register:RD-09`, which the other two passes
both graded CONFIRMED and not byte-level. The verdict does not move, but
the self-report was false, and it is the second round running in which a
triage-stage agent's coverage claim did not survive checking. The
mechanical union-find over all three passes' groupings is what caught it;
no agent did.

One disclosed deviation, recorded because it strengthens rather than
weakens the round: the verifier walk ran local CRC-32C computations in
Python, reading no files, and independently reproduced all four constants
the document states — `E3069283`, `00000000`, `EECB3BB2`, and Appendix
A's trailer CRC `E00938D2`. The reader walk separately recounted §21 by
hand and got 39 + 50 + 26 + 10 = 125 conditions over 242 named instances,
matching §21.8 exactly.

## Disposition

None of the 44 is dispositioned. They are not the same shape as earlier
rounds' findings: rounds 4 and 5 found propagation failures, round 6
found silences, and this round found mostly **restatements that stop
short** — §19's tier lists, §21.7's inventory, §8.1's checksum map, each
accurate about what it names and incomplete about what it omits. Three
warrant more than an edit and are named above.

## Artifacts

- [prompt.md](prompt.md) — charters, access rule, taxonomy, pass criteria
- `transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`
  — the three implementer walks
- `transcript-diagrams.md` — the figure audit
- `transcript-register.md` — §21 against the rules it restates
- `transcript-adversary.md` — attacks tried, and which the text refutes
- `transcript-quiz.md` — the slate, both independent answer sets, and the
  adjudication
- `transcript-triage-correctness.md`, `transcript-triage-implementer.md`,
  `transcript-triage-skeptic.md` — the three blind triage passes
