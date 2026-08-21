# Cleanroom round 16 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone, plus an
adversarial pass against the round's own verdict.

## Verdict

**Byte-level after the round's triage: 0. Byte-level after adversarial
verification: 4. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** (tenth round running) |
| Findings | 33 — reader 4, writer 6, verifier 5, diagrams 5, register 5, adversary 5, quiz author 3 |
| Distinct defects | **14** from the round, **+4 byte-level** from adversarial verification, **+2** from the maintainer's pass |
| Harness | first clean run since round 14 — 12/12, every transcript matching its return |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1
→ 1 → **1** (the shrink class; three further candidates fixed with it).

## The round's zero did not survive

The round's three triage passes unanimously downgraded the single
byte-level flag its reporters raised. Their argument was quoted, specific
and correct as far as it went: the disputed shrink leaves a surviving stored
tile with wrong padding content, that is a T4 violation, so the output is
nonconforming and `[R-CNF-05]` bars every conforming writer from emitting it
under **both** readings — the emittable set does not move.

That is true of the counterexample the reporter chose. It is false of the
class the defective sentence governs, and an adversarial pass whose only
instruction was to refute the downgrade found the construction that shows
it:

> Shrink an extent so a stored tile gains padding positions, **and in the
> same commit write that tile's index entry as the sentinel.**

§3.1 makes a tile stored in a generation only if that generation's entry is
not the sentinel, and says superseded bytes from earlier generations do not
make a tile stored. T4's subject is a padding position in a decoded tile
image, and an unstored tile has none. Its old bytes are slack, which
`[R-CNT-21]` puts beyond every conformance requirement. **The output is a
conforming file.** Only one reading permits an appender to produce it, and a
creator emits generation 1 only — so the emittable set moves. Byte-level.

Each link was verified by hand against the text before the verdict was
changed.

The specification had already conceded the class. §21.7, written two rounds
ago, says "a commit that supersedes every tile it would have damaged leaves
the live state clean, so the bar is unwitnessed there" — a passage written
to record a limitation, which turned out to be the proof that the
byte-level sub-class exists.

**The repair written earlier the same day did not close it and made it
sharper.** ADR-0079 stated the shrink permission over "any tile the new
state still stores" while the bar it adopts is quantified over the
superseded generation. Those domains come apart exactly where the damaged
tile is unstored — the construction above.

Three further byte-level candidates came from the same adversarial run, and
**two were in text written during this round, within an hour**: §20.5's
"carried forward as it stands, its offset re-pointed like any other" told a
compactor two contradictory things about one entry, and "a record §20.4 does
let it drop is no exception" read as both *refuse* and *drop*. All four are
closed in
[ADR-0080](../../decisions/0080-the-shrink-permission-takes-the-bar-s-tense.md).

## What this says about the instrument

Three independent passes agreed, each quoting text, and all three were wrong
in the same way — not in reasoning but in scope, because they shared a
premise no one attacked. **Unanimity among passes graded the same way is not
independent evidence when the premise is common to them.** What found the
error was a pass instructed only to refute, and given the conforming-file
distinction as an explicit test rather than left to judgement.

The round's own reporters were right to raise it; the triage layer is where
it was lost.

## The maintainer's own pass

- **M-01** — §20.3's shrink branches stated as exhaustive alternatives when
  one commit can be in both — the round **found independently** (writer-02
  and quiz-01, one flagging it byte-level). I had also graded it byte-level,
  and I was wrong on the instance for the same reason the passes were: I did
  not check whether the resulting file is conforming. It is not, in that
  construction. The finding is byte-level in *scope*, which is what the
  adversarial pass established.
- **M-02** — §21.1's `[R-SER-08]` repair attributing to §14.2 a
  characterization that is §12.3's — the round did **not** find.

## Disposition

All 14 round defects fixed, the 4 adversarial byte-level candidates fixed,
and the maintainer's 2. Four decisions were the maintainer's: §20.4's drop
trigger reaches any layer-record edit (its silent-loss cost recorded rather
than argued away); a verifier owes no search for SHOULD deviations; T18's
placement is not a distinct shape; and the shrink permission takes the bar's
tense.

Notable among the rest: `[R-WRT-06]`'s three-limb prohibition repeated its
first limb verbatim as its third — an editing error left by round 15's own
repair; `[R-CNT-04]` put a normative MUST on a "content sniffer", an actor
outside §2.3's five conformance classes; §21.7's "and nowhere else" asserted
a false converse; §19.3's enumeration of layer-access checks omitted
`[R-ENC-04]` and the §14 decoded sizes derived under it; §20.5's compaction
Example claimed every record extent survives byte-for-byte, when a relocated
index region is a record extent and is regenerated; and **R3's parenthetical
carried a third copy of the unassigned-versus-experimental error** first
introduced in round 13 and fixed in two other places in round 14.

Register and corpus: **121 conditions over 273 instances, 327 vectors.**
