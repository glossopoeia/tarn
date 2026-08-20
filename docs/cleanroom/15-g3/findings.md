# Cleanroom round 15 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone.

## Verdict

**One byte-level ambiguity, in the repair round 14 landed one day earlier.
G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** (re-run; one comma-vs-semicolon difference, not a divergence) |
| Findings | 38 — reader 6, writer 5, verifier 4, diagrams 7, register 6, adversary 7, quiz author 3 |
| Distinct defects | **23** (plus 3 the maintainer found independently) |
| **Byte-level, after triage and hand-check** | **1** — unanimous across all three passes |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1
→ **1**. No two consecutive rounds have ever been clean.

## The worst harness failure the project has recorded

**Three agents returned schema-valid placeholders at once** — the quiz
author, the reader walk and the adversary — each with `disclosure: "test"`.
The author's fifteen questions were each the single character `a`; the
adversary's one returned finding was titled `x`.

The guard added after round 13 checked whether the slate was *empty*. This
slate had fifteen elements. **Schema validity is not evidence of content**,
and the guard had been written for the previous shape rather than the
general one.

The three detectors behaved differently, and the difference is the lesson:

- The **count check** caught the adversary (returned 1, claimed 7).
- The **reader passed every check** — 0 returned, 0 claimed, perfectly
  self-consistent — while its transcript held six findings.
- The **quiz answerer caught it itself**, refused to invent questions,
  marked all fifteen underdetermined and asked to be re-run. That is what
  the mandatory disclosure field is for.

**Triage graded 23 findings when 38 existed.** Fifteen never reached it —
the largest loss in the project's history, and the incomplete round would
have reported a smaller, cleaner-looking result. All fifteen were recovered
from disk and the round was re-run: a fresh quiz behind a hardened guard,
and all three triage passes over the complete set.

The guard is now general — `assertNotDegenerate` rejects any return whose
prose fields are too short to be prose — and is wired into the slate, the
six walks, both quiz takers and all three triage passes.

## The survivor

§20.3 step 4 does not settle whether a commit may shrink an extent so that
whole stored tiles cease to be **addressed**: the grid count falls and the
tiles leave the index entirely.

The decisive check, verified by hand rather than taken from the passes:
**the word *shrink* occurs exactly once in 4,227 lines**, inside a
`> **Rationale.**` block that §2.1 strips of force. The only text in the
specification that addresses shrinking at all carries no force — and it is
the sentence round 14 wrote to repair a finding about that very hazard.
That is the third time (rounds 9, 14, 15) a repair has been placed where
`[R-CNF-01]` denies it effect.

Settled in [ADR-0079](../../decisions/0079-a-shrink-that-de-addresses-is-permitted.md):
**permitted**, with a SHOULD steering callers to a new file wherever a
commit would strand a large share of a layer. The ADR records that this
narrows ADR-0074's and ADR-0078's stranding argument, and why recompression
stays barred on a different ground — there the slack is a full duplicate of
data the caller is keeping, where here it is exactly the data the caller
chose to discard.

## The maintainer's own pass

Run against the same repairs while the round was in flight, and reported
because a round is measured by what it misses as well as what it finds.

- **M-03** — §21.2's preamble claiming no row reaches a foreign-major file
  — the round found **three times over** (verifier-02, register-01,
  adversary-03) and with better coverage than the maintainer's: it named
  F18, F6 and F1's front-block instance beside the F8/F14 pair.
- **M-01** — §21.1 stating outcome-follows-from-scope **twice**, where
  round 14's repair swept only one site — the round did **not** find. The
  propagation check cannot see it either: both sites sit in one section and
  one changed in the same commit.
- **M-02** — Appendix G defending the word *low* after the repair removed
  it — the round did **not** find.

Also considered and declined: §22.3 and Appendix H restate the slack-total
obligation without round 14's "reaches a live state" carve-out. Both
describe the ordinary case and §5.2 states the rule; recorded so the
omission is a decision rather than an oversight.

## Disposition

All 23 dispositioned: **23 fixed**, plus the maintainer's three.

The heaviest concentration is in text written in the two days before this
round: `[R-SER-08]` was cited in §21.1 for the opposite of what it says
(it is the format's one *resolved* byte, not one served through); §20.5
cited §20.4 for a proposition §20.4 denies; §21.7's "the §21.4 rows then
fire" asserted a converse that is false where a change reaches no
structurally constrained byte; §20.3 named the lz4 cap as the *only* bound
a growth can breach, where `[R-ENC-04]`'s ceiling is another; and §20.3's
alignment half quantified over a commit's new tiles where `[R-SLB-01]`
binds every stored tile.

Beyond those: `[R-GEO-01]`'s parenthetical was false at extent 0; §4.2
claimed all byte lengths are `u64` where `inline_length` is `u32` and every
length prefix a `u8`; `[R-WRT-07]`'s regeneration enumeration had no case
for a structurally invalid entry; §20.5's placement freedom ignored the
layout invariants; F27 and L48 dropped `[R-MTA-05]`'s "at every nesting
depth"; §21.7 over-claimed that the ordinal mappings have no witness; and
Appendix G pinned record placement without pinning record order.

Register and corpus: **121 conditions over 275 instances, 327 vectors** —
F23 and L12 gained the direction axis §21.1's magnitude criterion gives
them.
