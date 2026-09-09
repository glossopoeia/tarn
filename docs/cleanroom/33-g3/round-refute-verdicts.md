# Cleanroom round 33 — refute-phase verdicts

The workflow's own log line is the record of what fired:

    refute phase: 0 unanimous downgrade(s), 0 split verdict(s), 1 unanimous uphold(s); byte-level upheld anywhere: true

One shape, one refuter. The round's one reporter flag was upheld by all
three passes, no verdict split, and no reporter flag was downgraded, so
neither Sonnet refuter launched. The uphold-refuter, configured on Opus,
was refused at zero tokens with `[reasoning_extraction]` at launch and again
on the unchanged resume, and ran on Sonnet after that one call's model was
changed without rewording. Its verdict was hand-checked in both directions
before the round's verdict rested on it; `findings.md` carries the
hand-check.

## `alignment-slab-value-change` — unanimous byte-level uphold

**Refuter (Sonnet, after two Opus refusals): UPHOLD_STANDS.** Brief: find
the sentence that decides the finding against the reporter. Sections
opened: §20.3 step 4 whole with its closing paragraph; §16.1 `[R-SLB-01]`;
§16.2 `[R-SLB-02]` to `[R-SLB-05]`; §11.1's Rationale; Appendix H's two
sites; §7.4's field table with `[R-CNT-16]` and `[R-CNT-23]`; a
whitespace-normalised search for every occurrence of *re-establish*.

Its own candidate closer, pushed further than the passes had: that the
fifth member's *"as this step provides below"* delegates to `[R-SLB-04]`,
whose trigger list names *"the slab declaration itself"* changing, so that a
rule regulating the change implies the change may occur. Found not to
reach: the trigger is written over *"a layer slab-declared in either the
superseded or the new generation"* and is fully explained by a first
declaration, a whole-file rewrite, and an empty layer re-declared freely,
none of them the disputed case of a layer that stores a tile through the
commit. Every one of the five sites restates the same three verbs with no
added disambiguation; §7.4 defines the fields' wire encoding and no
re-declaration semantics; `[R-SLB-01]` and `[R-CNT-16]` state
single-generation invariants.

Sentences it quoted as bearing on the question and deciding none of it:

- *"a slab or alignment declaration MAY be declared, re-established or
  cleared as this step provides below"*
- *"keeps its declarations, with these exceptions and no other"*
- `[R-SLB-04]` whole, with *"or the slab declaration itself"*
- *"a slab declaration is re-established or cleared (`[R-SLB-04]`), and an
  aligned layer's stored tiles — every one the new state keeps, not only
  those this commit adds — satisfy its invariant or the declaration is
  cleared"*
- §7.4's alignment row, *"0 = none declared; else a power of two"*

**Hand-check verdict: UPHOLD STANDS.** The driver's own search reached the
same sentences and one more, *"A commit MAY make several of these changes
at once"*, under which a clearing and a declaration might compose into a
change; a reader of the strict construction can refuse that route on the
ground that a change with no cleared state between is not two of the listed
changes, and no sentence says otherwise. The construction was checked by
hand, the disputed file is conforming, and the text provides for the change
twice, in `[R-SLB-04]` and in step 4's *"every one the new state keeps"*
clause, without once saying it may be made.
