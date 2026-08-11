# 0061. Persistence governs every record type, implemented or not

- Status: Accepted
- Date: 2026-08-11
- Covers: whether an updater may drop a record whose type it implements
- Confirm: none

## Context

`[R-WRT-05]` obliges an updater to re-emit byte-identically every record it
retains and does not logically modify, *"whether or not it implements the
record's type"*. The table beneath it is introduced with *"For record types the
updater does not implement, the stored flags govern"* — and then never says what
governs for a type it does implement. Cleanroom round 6 read the omission as the
permission it resembles, and asked whether an appender may drop a record of a
type it understands.

The table's MU = 0, PE = 0 row is what makes the question sharp: it is the only
row that licenses dropping a record at all.

## Decision

**PE governs in both cases. Only whose PE is authoritative differs.**

- For a record type this specification registers, the **registry's** fixed flags
  govern, not the stored ones — `[R-CNT-22]` already requires a reader to apply
  a known type's specified semantics regardless of its stored MU and PE bits.
- For any other type, the **stored** flags govern (`[R-CNT-15]`).

Implementing a type is not a licence to drop it. Understanding a record tells an
updater what the record means; PE tells it whether the record must survive. The
two are independent, and §7.3 sets PE deliberately per type.

Both types §7.3 registers carry PE = 1 — layer at MU = 1, PE = 1 and user
metadata at MU = 0, PE = 1 — so **no registered record type may be dropped in
major version 1**. The MU = 0, PE = 0 row therefore has no subject among
registered types; it governs unregistered records, whose stored flags say what
they say.

## Consequences

§20.4's table header now states which flags are authoritative, and stops
implying a different rule for implemented types. §20.5's compactor obligation —
the live committed state *"less any record §20.4 lets it drop"* — resolves to a
single class: unregistered records whose stored flags are MU = 0, PE = 0.

What this forecloses is exactly the failure it was reported as: an appender that
implements user metadata dropping the document *because* it understood it. A user
who set metadata through one tool would have lost it to another tool's ordinary
append, with nothing in the file recording that it had ever been there — and
`[R-CNT-21]` makes the superseded bytes slack, so nothing recoverable either.

Priced knowingly: major version 1 has no droppable registered type, so the
MU = 0, PE = 0 row does no work until a future minor version registers one.
That is the right order. The row is the mechanism; registering a type into it is
a decision to be made once there is a type that wants it.

## Precedent

- PNG (ISO/IEC 15948), the safe-to-copy bit in the fourth letter of a chunk
  name: whether an editor may drop a chunk it does not recognize turns on the
  chunk's own declared bit, never on the editor's knowledge of the chunk.
  `[R-WRT-05]` is that rule, and this decision keeps its two halves consistent.
- `[R-CNT-22]`, which had already made the registry authoritative over stored
  bits for readers; this extends the same authority to updaters, where it was
  merely unstated.
- ADR-0041, which fixed updater re-emission and compaction identity, and left
  this seam between *implements* and *retains* unexamined.
