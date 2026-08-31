# 0110. Two defects in ADR-0109's own repairs, one byte-level

- Status: Accepted (resolves the ADR-0109 audit)
- Date: 2026-08-26
- Covers: §21.1's specialization property; §20.4's MU = 1 cell
- Revises: two repairs ADR-0109 wrote
- Confirm: none

## Context

The ADR-0109 repairs were audited by three agents over eight hunks, run
findings-only with no verification cap. Eighteen findings came back, **two
self-flagged byte-level and both naming the same defect**, reported
independently by two auditors that could not see each other.

**Both confirmed defects are in repairs ADR-0109 wrote**, and one of them is the
exact failure ADR-0106 recorded three weeks of evidence for: *a repair that
generalises is a new claim about the whole passage, and it needs the derivation a
new rule needs.*

## Decision

### §20.4's cell takes its warrant's verb — byte-level

ADR-0109 replaced a borrowed anaphor with `[R-WRT-06]`'s own ground and scope,
and wrote: "At either scope a compactor MUST **refuse the file**". The substance
is right — `[R-WRT-06]` reaches "any record whose type it does not implement with
MU = 1", and §7.4 makes a sub-record a record, so "at either scope" holds. **The
verb is wrong, and it is the one word this document legislates.**

`[R-WRT-06]` says a compactor "MUST refuse **to compact**" — it declines an
operation. "Refuse the file" is this document's phrase for the reader outcome
reject-file, and §21.6's closing paragraph forbids it in terms for exactly this
case: "the same type as a layer sub-record is reject-layer and **never a ground
to refuse the file** (`[R-CNT-18]`), so only the top-level case is a file a
reader refuses", a qualifier that paragraph calls load-bearing. `[R-CNT-18]`
states the same MUST NOT. And the sentence immediately before ADR-0109's in the
same cell had just set a reader-outcome frame, so the reader reading is the
natural one.

So after ADR-0109 there was a reader — `[R-WRT-01]` makes a compactor "a reader
of every structure they process" — instructed to refuse the file on the ground of
a layer sub-record, and §21.6 says there is never one. An implementer following
§20.4 violated `[R-CNT-18]`'s MUST NOT while believing itself compliant. **The
repair is one word**: refuse *to compact* the file.

This is check 7's shape exactly — argument by analogy, where the repair quotes
its warrant and the two governing verbs must be read side by side. ADR-0109's
repair quoted `[R-WRT-06]`'s *ground* faithfully and changed its *verb*, and the
check that exists for that caught it.

### §21.1's property is quantified per instance, not per row

ADR-0109 replaced a closed list of specialization pairs with the property that
decides any pair, and kept the old list's members as instances. **The property is
false of the first pair on its own list**, and ADR-0109's own new negative
sentence says so.

F1's condition is "A signature constant is stored byte-reversed", with **two
instances** — the front signature block at [0,8) and the trailer magic at F−64.
F6's condition is that the 16-byte front block is not byte-identical to the
constant; F8's is that the 8 bytes at F−64 are not the trailer magic. A file
whose trailer magic alone is reversed exhibits F1 and F8 and **not** F6; one
whose front block alone is reversed exhibits F1 and F6 and **not** F8. So neither
"every file exhibiting F1's condition necessarily exhibits F6's" nor the same for
F8 is true, and both pairs fall under ADR-0109's own closing sentence — "rows
that merely overlap, each reachable without the other, do not stand in it" —
which contradicts the list two sentences above it.

**The old list was instance-level and the property that replaced it was
row-level.** That is the whole defect: the containments do hold, per instance,
and neither signature constant is a palindrome, so a reversed front block is
never byte-identical to the constant and a reversed trailer magic is never the
magic. The property is now quantified over a row's condition *at a given instance
of it, where the row enumerates several*, and F1's two entries are stated per
instance. The four other pairs — F35 of F36, L24 of L25, F21 of F22, L10 of L11 —
each have a single instance, so the per-instance form leaves them unchanged.

**This is ADR-0106's lesson landing on the repair written to honour ADR-0095.**
ADR-0109 derived F21 ⊂ F22 and L10 ⊂ L11 from the rows and inherited the other
three pairs on the document's word. Changing the quantification of a list is a
claim about every member of it, and three members were never re-derived. A
property is only better than a list if it is true of the list it replaces.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors, isolation
clean. No propagation acknowledgement was needed.

**The repair audit did what ADR-0081 built it for.** Both defects were in repairs
committed hours earlier, in a batch whose every edit had been dry-run,
rendered before and after, and passed by five gates. Neither is visible to any of
them: one is a verb collision across three sections, the other is a quantifier
that changed unit. Two auditors found each independently, which remains this
project's most reliable signal.

**Sixteen further findings are recorded and not yet dispositioned**, none
byte-level. Four are the same shape as the five ADR-0109 repaired — a restatement
carrying a qualifier its rule no longer states, or never stated — in §21.3, §13's
lead-in, §24's Note, and F3. That the audit found four more of that class
immediately after eight repairs of it suggests the class is not exhausted, and it
is the one no mechanical check in this repository can see.

## Precedent

- ADR-0107's relation to ADR-0106: an audit of a repair batch, finding its
  defects before a fresh round reads them, recorded as a revising ADR rather than
  as an edit to the ADR it corrects.
- ADR-0106's rule that a repair which generalises needs a new rule's derivation —
  here applied to the ADR that cited ADR-0095 as its warrant.
- Check 7 (ADR-0081's audit, added after round 22): quote the repair's governing
  verb and its warrant's side by side. The verbs were "refuse the file" and
  "refuse to compact".
