# Cleanroom round 32 — refute-phase verdicts

The workflow's own log line is the record of what fired:

    refute phase: 1 unanimous downgrade(s), 1 split verdict(s), 1 unanimous uphold(s); byte-level upheld anywhere: true

Three shapes, three refuters. The two refuters of the downgrade and the
split ran on Sonnet, as configured; a verdict from either in the direction
that clears the gate is provisional until the hand-check confirms it. The
uphold-refuter, configured on Opus, was refused at zero tokens with
`[reasoning_extraction]` at launch and again on the unchanged resume, and
ran on Sonnet after that one call's model was changed without rewording.
Every verdict below was hand-checked, in both directions, before the round's
verdict rested on it; `findings.md` carries the hand-check.

## `channel-list-shorten-extend-composition` — unanimous byte-level uphold

**Refuter (Sonnet, after two Opus refusals): UPHOLD_STANDS.** Brief: find
the sentence that decides the finding against the reporters. Sections
opened: §20.3 whole; §20.4; the start of §20.5; §11.1's Rationale; §11.2;
§11.4 `[R-GEO-06]`; §16.1 and §16.2 with `[R-CNT-16]`; §23.1; Appendix H's
updater entry; whole-document searches for *not both*, *exactly one*, *net
effect*, *at most one*, *mutually exclusive*, with a control search first.

Its own candidate closer, beyond the five the passes had tested: that
*"A commit MAY make several of these changes at once"* reaches only across
the four items and not within one. Found unforced: §11.1's Rationale
restates the rule with the same shape and no exclusivity marker, and the
passes' slab-and-alignment example needs the sentence to reach within an
item. `[R-GEO-06]`'s formula is positional and confirms the mechanism rather
than barring it; §23.1 and Appendix H restate the shortening and the
addition without deciding their composition; the closure clause closes the
outer list and not the alternatives inside one item.

Sentences it quoted as bearing on the question and deciding none of it:

- *"keeps its declarations, with these exceptions and no other: … a planar
  layer's channel list MAY be extended at its end, or shortened from its
  end; … A commit MAY make several of these changes at once."*
- *"the position of every planar channel but the last"*
- *"where a field is on both sides — a dimension extent, a planar layer's
  channel list — the permitted side states the whole of what a commit MAY
  do to it"*
- *"an appended planar channel adds tiles at ordinals after every existing
  one, a disk ordinal being c · N + s with N the spatial-tile count; a
  channel removed from the end takes only its own tiles out of the
  addressed set"*
- `[R-GEO-06]`'s disk-ordinal formula; §16.2's `[R-CNT-16]` clause; §11.1's
  *"several of these in one commit"*; Appendix H's *"a planar channel added
  or removed at the end"*.

**Hand-check verdict: UPHOLD STANDS.** The driver's own search reached the
same sentences and the same end; the construction was recomputed
independently, both CRCs reproduced, and the disputed file is conforming.

## `json-number-rounding-direction` — split, one uphold against two downgrades

**Refuter (Sonnet): DOWNGRADE_REFUTED.** Brief: overturn the downgrade.
It re-read §18.2 whole, searched the whole document for any rounding
vocabulary with a normalised search and a control, recomputed `DBL_MAX`, the
midpoint 2¹⁰²⁴ − 2⁹⁷⁰ and its conversion under the platform's default,
opened Appendix F and §12.1, and held that Appendix F's *"(§12.1)"* scopes
the IEEE 754 reference to the sample-type table so that §18.2's conversion
carries no attribute. Quoted: §18.2's rule; §21.5's *"Every row here is a
violation all the same"*; R8's row; `[R-CNF-12]`; `[R-CNF-05]`; Appendix F's
two entries; §12.1's table.

Its brief carried a harness defect it disclosed: the field headed *"The
passes' stated reason for downgrading"* held the first pass's rationale,
which on this split was the uphold. It reached its verdict from the
document.

**Hand-check verdict: NOT BANKED as byte-level.** The quotations establish
that no attribute is named and what follows if the fork is real; none
decides whether naming the standard imports its default, which is the
question, and the driver holds that it does: `[R-CNF-02]` fixes conformance
independent of any environment, IEEE 754-2019 fixes roundTiesToEven as the
default for every binary-format result absent a stated attribute, and
Appendix F's parenthetical indexes a use rather than limiting the standard.
The contrary verdict, and the pass that shares it, are recorded in full in
`findings.md`, the text is repaired under ADR-0125 decision 2 so the
question cannot recur, and the round's verdict does not turn on it.

## `permitted-change-biconditional` — unanimous downgrade of a reporter's flag

**Refuter (Sonnet): DOWNGRADE_STANDS.** Brief: overturn the downgrade.
Quoted, with line numbers: *"with these exceptions and no other"*; *"A
commit MUST NOT change one of these; the change is a new layer, or a
whole-file rewrite under a fresh file_id"*; the bounds paragraph whole,
whose four-item list is the nearest antecedent of *"The list"*; §11.1's
Rationale, *"several of these in one commit, each subject to every rule the
declarations it produces are under"*, a necessary condition; §2.1's *"when,
and only when, they appear in all capitals"*. It checked `writer-01`'s
arithmetic and found it sound, and found no reading under which the
lowercase sentence lifts the capitalised prohibition.

**Hand-check verdict: DOWNGRADE STANDS.** A gate-clearing verdict from a
Sonnet refuter is provisional; the driver opened the same four sentences and
agrees. The wording is repaired under ADR-0125 regardless.
