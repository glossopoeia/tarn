# The repair audit of ADR-0086 and the FCS repair, before round 22

Two hunks, the first audit to run **check 6** — the "what did the repair leave
open?" check added after round 21 found a second defect in ADR-0085's sentence.

| | |
|---|---|
| Findings | 16 |
| After adversarial verification | 2 CONFIRMED, 14 REFUTED |
| Byte-level after verification | **0** |
| Harness | 18 agents, 0 errors |

## Fixed

**A-02 — an overclaim I wrote.** "the one header quantity that is *not* left to
the reader" is a closure claim over a set I did not check. Replaced with a
contrast that promises nothing: "unlike the decoded size and the window".

## Recorded, not fixed — and the gates cannot see it

**A-06: the FCS repair added a detectable violation and no register row gained
an instance.** §21.1 makes the register the inventory of detectable
file-conformance violations; §21.8 states "121 conditions over 273 instances";
`[R-VEC-03]` requires one vector per named instance. The new condition — a
content-size field present and unequal to the decoded length — is detectable,
and it is enumerated nowhere.

By §21.1's own instance criterion it is **four** instances, not one: the
mismatch is a magnitude comparison, so it takes the direction axis (declared
larger / declared smaller) exactly as F23 and L12 do under ADR-0079, across the
two placements R3 and R4 both carry (top-level extent; layer sub-record
extent).

**Cost, honestly:** 4 instances → §21.8's total 273 → 277 → 4 new vectors, and
per this project's standing rule the register rewording and its vectors land in
**one commit**. `COV-05` then recounts.

**Why every gate passed anyway.** `tarn_check` verifies register↔corpus
consistency — that every enumerated instance has a vector. It does not verify
spec↔register completeness, so a rule added to normative text without a
matching row or instance is invisible to it. That is a tooling blind spot of
the same family as the `SPEC-03` one ADR-0081 closed, and it is worth closing
the same way.

## The routing question the audit could not settle

Four findings (A-01, X-05, and two others) argued the FCS mismatch belongs to
**R4**, not R3: R4's condition is "breaks one of the frame constraints §18.2
states", and the new sentence *is* a §18.2 frame constraint. The counter, which
the verifiers accepted, is R4's own "unlike R3, the constraint is broken whether
or not the bytes decode" — and an FCS mismatch can only be found by decoding
and measuring.

Both readings are defensible and the instance count is the same either way, so
the routing is a maintainer's call and does not block the corpus work.
