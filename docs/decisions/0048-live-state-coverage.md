# 0048. Coverage certifies the live state; dead space is counted, not modelled

- Status: Accepted (supersedes ADR-0030's history-wide coverage;
  amends ADR-0017's consequences)
- Date: 2026-08-07
- Covers: what byte coverage certifies; the status of superseded
  bytes; what a verifier reports; the retirement of generation
  attribution
- Confirm: none

## Context

ADR-0030 made byte coverage a property of a file's whole history:
every byte attributed to the commit that appended it, verified by
enumerating every generation and validating a trailer chain. Its own
"what settles it" asked whether declaring dead ranges costs more than
it buys. Three cleanroom rounds answered.

Coverage and its attribution machinery are under 4% of the normative
text and produced essentially all remaining byte-level ambiguity —
new edges every round, including edges created by the previous
round's fix. The acceptance round's adversary ultimately constructed
a complete file that one conforming verifier certifies and another
rejects, which `[R-CNF-02]` forbids outright.

The deeper problem is what the model asserts. It certifies the
internal structure of bytes whose entire purpose is to be discarded.
This format is not a version store: an operator paying for storage
compacts, and nobody retains a commit log riding inside a data file.
Append exists for two things — a torn write leaves the previous state
intact, and a layer can be added to a large file without rewriting it
— and both are properties of the *transition*, needing no certified
record of every commit the file ever took.

## Decision

- **Coverage is a property of the live committed state.** Every byte
  reachable from the live trailer belongs to exactly one class —
  front block, structure, or declared padding — with no overlaps.
  That partition is file validity, and it is decidable in one pass
  from the live trailer.
- **Every other byte is dead space**: unconstrained content, no
  internal structure this specification defines, no conformance
  requirement. A reader MUST NOT interpret it; a verifier MUST
  **report the total number of dead bytes**, which is the number that
  tells an operator to compact.
- **Generation attribution and the trailer chain are retired.**
  §9.7's enumeration, candidate qualification, chain selection, and
  per-generation partition go, and with them `[R-LIF-09]` and five
  register rows. The generation counter survives as an informational
  field; nothing structural reads it.
- **Recovery is unaffected.** §9.6's backward scan finds trailers by
  magic and CRC — tool behaviour that never depended on attribution —
  so truncating to an earlier state still works, and its output is
  still re-verified whole.

## Consequences

The ambiguity cluster dissolves rather than shrinks: "which
generation", "which chain", "how deep into superseded structures",
and "may a live extent point into a prior generation's padding" all
stop being questions. §9.7 drops from roughly 530 words to 120,
§5.2 states a constructive rule over one state, and the register
loses five rows and rewords four.

Given up: the ability to certify that every byte in a file was
legitimately committed. That property was always weaker than it
sounded — an adversary who can write the file can commit junk as a
payload under any model — and §22.3 already conceded that dead space
can hold anything. What replaces it is more useful to an operator: a
verifier that certifies exactly what a reader can reach, and counts
what it cannot.

Foreclosed: treating a TARN file as a history one can audit. The
specification now says plainly what it always meant — bulk work then
compaction is the intended shape, and a long series of small edits is
supported but wasteful.

## Precedent

- ADR-0030's own settling condition, answered by three cleanroom
  rounds' evidence that was unavailable when it was decided.
- ADR-0017's append model, unchanged: crash safety and cheap
  extension survive intact, since both are transition properties.
- PMTiles' blunt honesty about what a single-file format is for, as
  the tone this decision restores: certify what is read, count what
  is waste, and say which is which.
