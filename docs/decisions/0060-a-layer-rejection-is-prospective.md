# 0060. A layer rejection is prospective

- Status: Accepted
- Date: 2026-08-11
- Covers: what a reader may keep serving after a reject-layer outcome
- Confirm: none

## Context

§2.4's reject-layer row says the affected layer's data and metadata *"are not
usable"* and permits a reader to keep listing the rejected layer's name.
Cleanroom round 6 asked how far that reaches: must a reader retract values it has
already returned from the layer, or only refuse further service?

The question matters to anything that streams. A reader answering a region read
returns tiles as it resolves them; a catalog service answers a layer's geometry
long before anyone asks for a tile. If rejection were retroactive, both would owe
a retraction channel this specification never describes, and neither could serve
anything until it had validated everything.

## Decision

**A reject-layer outcome is prospective.** It bars further service from the
layer and does not retroactively invalidate content already returned under
§19.2's validation timing (`[R-RDR-02]`).

The tier rule is what makes this safe rather than merely convenient.
`[R-RDR-02]` forbids returning data whose governing structure has not passed the
validation its tier requires, and `[R-RDR-03]` puts the whole layer record — the
record walk, the name rules, the value sets of §11.4 through §17.3, the geometry
floor, the codec declaration bounds, the I/O-free index cross-checks — before
the first layer access. A reader that observed those obligations cannot have
served anything layer-derived before the check that rejects it. What it may have
served is the layer's *name*, from the open, and §2.4 already permits keeping
that.

So the prospective reading licenses nothing new. It records that a conforming
reader never had anything to retract. A reader detecting early under
`[R-CNF-12]` is in the same position, only sooner.

## Consequences

No retraction channel is needed, and none is specified. A streaming reader may
return each tile as it resolves it, without buffering a layer to completion
against a rejection it has not yet met.

The obligation this creates falls on a reader's *ordering*, not its memory: the
licence to keep what it served depends entirely on having validated at the tier
that authorized serving it. A reader that serves first and validates later takes
no shelter here — it was already violating `[R-RDR-02]`.

**This clause is already in §2.4.** It landed in the editorial pass of `d29d9d7`,
drafted by that section's owner, while a second agent escalated the same finding
as a design decision. Both were right: the text is correct, and it needed an ADR.
This one ratifies text that is already normative rather than introducing it — and
that sequence is itself the defect worth recording. Spec text reached `main` one
commit ahead of the decision record that authorizes it, which AGENTS.md's rule
that spec text encodes Accepted decisions only exists to prevent.

## Precedent

- §19.2's detection-timing rule and ADR-0040 (*validation follows reliance*),
  which is where this answer already was; this decision reads it out rather than
  choosing against it.
- HTTP's handling of incomplete messages, which meets the same shape and answers
  it the same way: a server that has begun a response cannot unsend it, so
  failure surfaces as a truncated message the client detects, never as a
  retraction of bytes already delivered.
