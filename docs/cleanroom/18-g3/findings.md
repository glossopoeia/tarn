# Cleanroom round 18 — findings

Protocol: ADR-0034, four phases, preceded for the first time by a **repair
audit** ([repair-audit.md](repair-audit.md)). Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity. G3 is not met.** But it is in text no recent round
touched, and it is not in the repairs this round read — which is the first
time in five rounds that is true.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — twelfth round running (Q10's difference was presentational: "File A: nonconforming; File B: conforming" against "nonconforming; conforming") |
| Findings | 26 — writer 6, diagrams 6, register 4, verifier 3, quiz author 3, reader 2, adversary 2 |
| Self-flagged byte-level | **1** |
| Distinct defects | **17** — 1 byte-level, 8 design-decision, 4 register-bookkeeping, 4 editorial |
| **Byte-level after triage** | **1**, upheld by all three passes independently |
| Harness | clean: 12/12, 0 errors, every `transcript_finding_count` matching its return, all three passes echoing all 26 ids with no gap, no duplicate and no extra |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1 →
1 → 1 → 1 → **1**.

## The refute phase correctly stood down

It fires on unanimous byte-level downgrades and on split verdicts. This round
produced **neither**: the single byte-level flag was upheld by all three
passes, independently, each having tried to kill it and said so. The skeptic
recorded four attempts and named the one that came closest.

That is the phase working. A zero would have triggered it; a unanimous
*uphold* is the one shape it has nothing to attack.

## The survivor: §20.5's compactor `version_minor` clause has no modal

> "The output trailer copies the input's unknown ignore-lane flag bits forward
> (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the
> input's version_minor …"

The first conjunct restates a MUST that lives in §6.3. The second restates
**a SHOULD** — `[R-CNT-26]` — and the clause itself carries no BCP 14 keyword,
so its force is undetermined. The appender's *identical* max-construction is
expressly advisory: §20.3 step 6, inside an "An appender MUST, in order" list,
defers with "version_minor per `[R-CNT-26]`", and a MUST to comply with a
SHOULD is a SHOULD. Appendix G's closing paragraph calls the same subject
"`version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD".

**The fork, and it is not the reporter's own example.** Take an input with
`version_minor` = 3 carrying **no** set ignore-lane bit, fully expressible
under this text. Read as mandatory, the output carries max(0, 3) = 3. Read as
advisory, `[R-CNT-26]`'s floor for the output is 0 and its own consequence
clause says a higher minor "misstates the file's feature floor to tooling" —
so a compactor following that advice writes 0. **Two conforming compactors,
one input, different bytes at the trailer's `version_minor` field, and both
outputs conforming.** The emittable set moves.

The clause's stated rationale — "a compactor cannot know which minor version
defined an ignore-lane bit it does not implement" — reaches only inputs that
*carry* such a bit, while the rule as written is unconditional. So fixing the
modal without settling the scope leaves a second reading standing.

**This is the same class the repair audit found in §20.4 hours earlier**, and
the charter's new discriminator is what aimed the round at it: §2.1 binds BCP
14 keywords only in capitals, so a rule's force is a property of its casing
before it is a property of its logic. There the defect was a lowercase
restriction failing to bound an ALL-CAPS permission; here it is a clause with
no modal at all, resting its force on a citation to a SHOULD.

## What it found in this session's own repairs

Two of the eight design-decision defects are in text written today, and both
are honest hits:

- **§23.1 still overclaims.** This session replaced "the only removal a commit
  performs" with "the only removal of **sample data** a commit performs". Still
  false: §20.3 step 4's permitted shrink de-addresses tiles and turns their
  extents to slack, which is a second removal of sample data — and §20.3 uses
  *de-addressed* and *supersedes* for different things in the same paragraph.
  A narrower version of the same falsehood, introduced while fixing it.
- **§20.5's regeneration-forces-detection argument is conditional.** The new
  paragraph argues a compactor cannot avoid meeting a structurally malformed
  entry — but regeneration is conditioned on *relocation*, and the sentence
  before it says a compactor "is free to place structures anywhere §5.2
  admits". Under that freedom a compactor may leave a region at its input
  offset, never regenerate it, and never meet the entry. Not byte-level (the
  output carries the violation under either reading), but the argument does
  not carry the whole class it claims.

Neither is byte-level, which is the difference from rounds 14–17. The repairs
are still the defect surface; the defects in them are no longer byte-level.

## Disposition

**Resolved by [ADR-0083](../../decisions/0083-version-minor-is-advisory-and-erasure-is-not-only-superseding.md).**
The two conjuncts take different modals, and that is the point: the ignore-lane
carry-forward is a **MUST** (clearing those bits destroys information the
compactor is provably unable to evaluate, and §6.3 and §20.5 had each stated
the compactor's case without a modal while pointing at the other); the
`version_minor` floor is a **SHOULD**, scoped to the case its rationale
actually reaches — where an unknown ignore-lane bit is set — with the deviation
consequence stated, and otherwise deferring to `[R-CNT-26]` exactly as an
appender does.

SHOULD because `version_minor` is the trailer's only `descriptive` field, no
verdict or reader behaviour turns on it, and above all **no verifier can check
it**: the output carries no record of its input's minor. §21.7 now records
that, next to `[R-LIF-01]`, which is unwitnessed for the same reason. The
appender/compactor asymmetry turned out to be an artefact of form rather than
substance — §20.3 step 6 sits inside "An appender MUST, in order:", so the
enclosing MUST already supplied the modal that §20.5's running prose lacked.

Both repair defects this round found in the same day's text are also fixed:
§23.1 stops claiming an "only" and enumerates the removals instead, and
`[R-PRV-01]` widens from "a commit that supersedes data" to any commit that
makes sample data unreachable — the shrink-as-delete case being the one a user
is most likely to meet.

Register and corpus unchanged: **121 conditions over 273 instances, 327
vectors.** The register hunter's hand recount reproduced §21.8's totals
exactly (36+49+26+10 = 121 rows over 58+116+55+44 = 273 instances).
