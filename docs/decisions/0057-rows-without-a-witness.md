# 0057. Three rows that name a cause rather than a state

- Status: Accepted
- Date: 2026-08-11
- Covers: the residue-past-a-commit row; the stale-slab-declaration row;
  the sub-record-nesting row
- Confirm: none

## Context

ADR-0056 removed a register row that no file could exhibit. Finishing the
corpus surfaced three more of a related but distinct shape: rows whose
condition *can* occur, but which no reader or verifier can tell apart
from a neighbouring row. §21.1 requires an instance to be one
*distinguishable* file, so a row with no distinguishing witness obliges a
vector that can only duplicate another.

All three were caught the same way — by trying to build the vector and
finding that the file produced evidenced a different row. Two of them
shipped briefly under the wrong label before an adversarial review
re-parsed the bytes and reported what they actually exhibited.

## Decision

All three rows are **deleted**. Each rule stays exactly as it is, and
each gains a note recording why the register carries no row for it, so
the row is not restored by someone reading the rule in isolation.

**Residue past a completed commit.** The row's own condition ends *"so
the tail read at [size − 64, size) is not a valid trailer"* — which is
the state, and that state is already three registered rows: the magic,
the trailer CRC, and committed_file_length against the transport size.
That last row even carries the parenthetical *"(physical file not
truncated or extended to it)"*. `[R-LIF-05]` forbids a reader to scan
backward, so it cannot distinguish residue from corruption and is not
asked to. What residue violates is `[R-LIF-04]`'s writer obligation to
truncate or overwrite; the row named the cause, not the observation.

**A stale slab declaration.** `[R-SLB-04]` delegates its own detection in
as many words: *"carrying a stale declaration forward is a validity error
at layer scope, detected as the invariant failures of `[R-SLB-03]` are:
by a verifier."* So every file exhibiting a stale declaration exhibits a
run whose stored tiles are unpacked or whose first stored tile is
misaligned — both registered. The rule is the writer's obligation, and it
is what makes those two rows reachable after a commit at all.

**Sub-record nesting.** Detecting nesting means parsing a sub-record's
payload as records, which a reader does only where this specification
defines that payload as a record sequence. Format major 1 defines exactly
one: the layer record — whose appearance as a sub-record is its own
registered row. A user-metadata payload is one byte (`[R-MTA-03]`) and an
unknown type's payload is opaque (`[R-CNT-15]`). The prohibition binds
writers and any type a later version registers; today it has no witness.

The register is **125 conditions over 244 named instances**, and every
one of the 125 rows now has at least one vector.

## Consequences

G5's row coverage closes at 100%. That is worth stating precisely,
because the number is smaller than it sounds: it means every row the
register carries has a file, not that the corpus exercises everything the
specification says. §24 already says the second thing is impossible, and
`[R-VEC-03]`'s sentinel, boundary and hard-limit obligations are reviewed
rather than computed.

The three deletions share a shape worth naming for future rows: a
register row must describe a **state a detector can observe**, not the
history that produced it or the obligation it breaches. Residue is a
cause; a stale declaration is a writer's omission; nesting is a rule
awaiting a type that can express it. Each remains a rule; none is a row.

Priced knowingly. A verifier written from the register alone will no
longer be told to check for a stale slab declaration by name — it will
check `[R-SLB-03]`'s invariants, which is the same check and the only one
it could have performed. And a future minor version registering a
record-bearing sub-record type will need the nesting row restored; the
note at `[R-CNT-18]` says so, which is the point of putting it there.

## Precedent

- ADR-0056, whose deleted row was vacuous where these are merely
  indistinguishable — the weaker defect, and the one only a build could
  find.
- §21.1's own rule that an instance is one distinguishable file, which is
  what makes indistinguishability a defect rather than a redundancy.
- ADR-0053's isolation rule, one layer up: a vector must carry the defect
  it claims. A row that cannot be isolated makes that impossible for
  every vector written against it.
