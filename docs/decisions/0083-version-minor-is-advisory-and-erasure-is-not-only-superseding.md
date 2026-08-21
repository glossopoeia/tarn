# 0083. `version_minor` is advisory for a compactor, and erasure is not only superseding

- Status: Accepted (resolves round 18's byte-level finding)
- Date: 2026-08-21
- Covers: §20.5's ignore-lane carry-forward and `version_minor` clause;
  §21.7's no-witness list; §23.1's removal enumeration and `[R-PRV-01]`'s scope
- Confirm: none

## Context

Round 18 returned **one** byte-level ambiguity, upheld by all three triage
passes independently, each having tried to kill it and said what it searched
for. The refute phase had neither a downgrade nor a split to attack and
correctly stood down.

§20.5's clause read:

> "The output trailer **copies** the input's unknown ignore-lane flag bits
> forward (`[R-CNT-08]`) and **carries** the greater of `[R-CNT-26]`'s floor
> and the input's version_minor …"

Two bare declarative verbs and no BCP 14 keyword, in a paragraph otherwise
dense with explicit MUSTs on the same actor. The only requirement the second
conjunct cites for the floor, `[R-CNT-26]`, is stated **entirely in the SHOULD
register** — and the *identical* max(floor, prior minor) construction is
expressly advisory for an appender at §20.3 step 6 ("version_minor per
`[R-CNT-26]`"), a MUST to comply with a SHOULD being a SHOULD.

**The fork, in bytes.** Compactor A reads the clause as mandatory and writes
`version_minor` = 7 for a minor-7 input; compactor B reads it as restating
`[R-CNT-26]`'s SHOULD and, creating a new file whose every feature is
expressible under this text, writes 0. The outputs differ in the two bytes at
trailer offset 10 (`07 00` against `00 00`) and consequently in the four CRC
bytes at offset 60. **Both outputs are conforming** — §6.2 admits any
`version_minor`, and `[R-CNT-07]` forbids a reader to reject on it — so
`[R-CNF-05]` bars neither, only one reading permits an actor to produce each,
and the emittable set moves.

The clause's stated rationale reaches less far than the rule it justifies: "a
compactor cannot know which minor version defined an ignore-lane bit it does
not implement" is true only of inputs that *carry* such a bit, while the rule
was written unconditionally.

## Decision

**The two conjuncts take different modals, and that is the point.**

- **The ignore-lane carry-forward is a MUST.** Clearing those bits destroys
  information the compactor is provably unable to evaluate, and `[R-CNT-08]`
  already binds an updater with "MUST copy forward … and MUST NOT clear them".
  §6.3 and §20.5 had each stated the compactor's case without a modal while
  pointing at the other — a circular deferral neither closed. §20.5 now states
  it outright, as the carve-out from §6.3's `flags = 0` requirement that it is.
- **The `version_minor` floor is a SHOULD**, scoped to the case its rationale
  actually reaches: *where an unknown ignore-lane bit is set*, the output's
  minor SHOULD be at least the input's. Where none is set, `version_minor`
  follows `[R-CNT-26]` exactly as it does for an appender. The deviation
  consequence is stated, as `[R-CNT-26]`'s own discipline requires of a SHOULD.

**Why SHOULD and not MUST.** `version_minor` is the trailer's only
`descriptive` field (§6.2's layout table: valid values *any*), `[R-CNT-07]`
forbids rejecting on it and makes all feature gating structural, and §21.6
registers a too-high minor as an explicit non-violation. No verdict, no
reader behaviour and no register row turns on it. Making the compactor's duty
mandatory would also demand an argument for why it exceeds the appender's for
an identical construction — and unexplained asymmetry between the two writer
tiers is precisely the shape the round-18 repair audit was built to catch.

**The deciding consideration is the absence of a witness.** A verifier sees
the output alone; it never sees the input, so it cannot know what minor the
input carried. A MUST no verifier can check is a weak MUST, and this document
already has a home for that class. §21.7 now records it, next to
`[R-LIF-01]`'s committed-prefix immutability, which is unwitnessed for the
same reason.

**§23.1 stops claiming a completeness it never had.** This session had already
replaced "the only removal a commit performs" with "the only removal of
*sample data* a commit performs" — a narrower version of the same falsehood,
and round 18 found it within hours. §20.3 step 4 describes a second removal of
sample data and distinguishes it from superseding **in the same paragraph**,
using *de-addressed* and *supersedes* for different things. The claim is now
an enumeration rather than an "only".

**And `[R-PRV-01]` widens to match.** Its prohibition was scoped by that same
word — "MUST NOT represent a commit that supersedes data as erasure of it" — so
a tool that shrinks an extent and reports "rows 900–1000 deleted" escaped it on
the narrow reading §20.3 itself supports, even though the de-addressed bytes
remain in the file exactly as superseded ones do. **Shrink-as-delete is the
more natural user-facing operation, so it is the case the rule most needs to
cover.** The prohibition now reaches any commit that makes sample data
unreachable.

## Consequences

Round 18 was the first round in five whose byte-level survivor was **not** in
the previous round's repair — it was in text no recent round had touched. What
aimed the round at it was the discriminator the charter carried for the first
time: §2.1 binds BCP 14 keywords "when, and only when, they appear in all
capitals", so a rule's force is a property of its casing before it is a
property of its logic. The repair audit had found the same class in §20.4
hours earlier, as a lowercase restriction failing to bound an ALL-CAPS
permission; here it is a clause with no modal at all.

Two of round 18's design-level findings were also in text written that day,
including §23.1's narrowed overclaim. The repairs remain the defect surface;
what changed is that the defects in them are no longer byte-level.

## Precedent

- `[R-CNT-26]`'s own SHOULD, whose register this decision joins rather than
  contradicts.
- §21.7's no-witness class, which decided the modal here as it supplied the
  evidence in ADR-0080.
- ADR-0081's casing discriminator, which this round's survivor confirms as a
  general instrument rather than a one-off.
