# Cleanroom round 17 — findings

Protocol: ADR-0034, with the refute phase added this round. Charters and
access rule: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity, and it is the direct consequence of a decision
taken the same day. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — eleventh round running, and the first needing no normalization to see it |
| Findings | 34 — reader 4, writer 6, verifier 4, diagrams 5, register 6, adversary 4, quiz author 3 |
| Self-flagged byte-level | **6** — the most since round 10 |
| Distinct defects | **17** |
| **Byte-level after triage and hand-check** | **1** |
| Harness | clean: 12/12, every transcript matching its return |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1 →
1 → 1 → **1**.

## The refute phase, and why it stood down

Round 16's lesson became protocol this round: a refute-only pass now fires
automatically on every group where a reporter flagged byte-level and no
triage pass upheld it, told to attack the shared premise rather than the
finding.

**It correctly spawned nothing.** Six reporters flagged byte-level, and
every one of those flags landed in a group at least one pass upheld — so
there were no unanimous downgrades to attack. The reconciler confirmed this
independently: "Reporter-flagged, downgraded by all passes: 0."

That is the phase working, but it also exposed a gap in how it was scoped.
**It attacks unanimous downgrades and not split upholds**, and this round
produced exactly the second shape: a finding two passes called byte-level,
one did not, and whose own reporter said it was not. Hand-checking settled
it (below), but the asymmetry is worth closing.

## The survivor: §20.4's drop licence

§20.4's MU = 0 / PE = 0 row was widened the same day, on a maintainer
decision, so that the file's layer set changes "equally by modifying any
layer's record". Four reporters found, and all three passes upheld, that
this contradicts a carve-out three sentences later in the same cell:

> "Superseding a stored tile's bytes is not such a change for either kind …
> so a commit whose only change is a supersede **MUST retain** the record."

A supersede necessarily modifies the layer record: `[R-LIF-01]` freezes the
prior index region, so §20.3 step 4 re-emits it "necessarily at a new
placement", so `extent_offset` moves and `crc_of_crc_array` changes. Under
the widening that is "modifying any layer's record", and the drop licence
fires. **MAY drop against MUST retain, on the same commit** — two conforming
updaters emitting different files for the same edit.

**This was the maintainer's agent's error in framing the choice.** The
carve-out was already in the cell, and was quoted in the message that
offered the two drafts; neither draft was checked against it. Resolved by
maintainer decision: keep the widening, delete the carve-out. A supersede-only
commit may now drop a disposable ancillary, and the row's SHOULD-report is
what keeps the loss visible.

## The one that did not survive hand-check

Five reporters and two of three passes called §20.5's compactor clauses
byte-level: `[R-WRT-06]` says a compactor MUST refuse where the table
licenses no drop, while `[R-WRT-07]` said a structurally invalid index entry
"is not one `[R-WRT-06]` obliges a compactor to refuse".

The contradiction is real — and it is text this project wrote the day
before. But it is **not byte-level**, on the discriminating test: §20.1
makes a compactor "satisfy every writer requirement for the bytes it
produces", and a regenerated index region is bytes it produces, so
reproducing an invalid entry is barred by `[R-CNF-06]` under either reading.
No file's bytes differ; one reading emits a file and the other emits
nothing. The reporter's own rationale said as much, and the skeptic pass
agreed against the other two.

Repaired by making the disposal explicit: such an entry obliges refusal,
because the compactor answers for the region it regenerates.

## Disposition

All 17 dispositioned: **15 fixed, 2 recorded as needing no change**
(R2 is a violation at every encoding value and the text already says so;
§6.1's "and nothing else" is decided by §6.2), and two low-priority
maintainer questions deferred with owners — whether `[R-LIF-02]`'s
durability barriers belong in §21.7's no-witness classes, and whether
§21.1's meta-rules should carry permanent requirement identifiers.

Notable among the rest: §11.1's Rationale still stated the shrink bar over
the **new** generation's stored tiles where §20.3 states it over the
superseded one — the same tense mismatch that produced round 16's
byte-level defect, surviving in the Rationale; §21.7 described T3 as reading
the index entry when T3's condition is a property of the decoded payload;
Appendix G's fallback `file_id` was "any other fixed nonzero value", which
is not a reproducible-writer rule at all and is now a named constant;
Appendix H's verifier checklist omitted pad bits from the decoded-content
obligations; `[R-ERR-04]`'s non-conformance sentence read over the two
capability refusals §21.6 names; and §20.4's licence was keyed on "removing
a layer", which an appender never does.

Register and corpus unchanged: **121 conditions over 273 instances, 327
vectors.**
