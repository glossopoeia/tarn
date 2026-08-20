# 0077. The instance criterion stated, and the ordering key de-circularized

- Status: Accepted
- Date: 2026-08-20
- Covers: §21.1's instance axes; cells T22 and L21; Appendix G item 3's
  record ordering key
- Supersedes: ADR-0076's direction rule (its cells stand; its stated
  criterion does not)
- Confirm: none

## Context

Cleanroom round 13 raised two defects in text this project wrote the day
before, and both are the same shape: a rule applied correctly in the cells
but never written down where a reader could reproduce it.

**The instance criterion.** ADR-0076 enumerated six cells and stated a
precedent for which rows carry a longer/shorter axis: "the direction axis
belongs to rows whose subject is a measured length, not to rows whose
subject is a declared field compared against one." Three reporters
independently found that this does not survive contact with the register.
T14's subject is the *index entry's declared length* against the derived
decoded size, and ADR-0076 gave it six instances; T22's subject is the
*frame's declared Frame_Content_Size* against the same derived size, and
ADR-0076 gave it three. Under the stated criterion both are declared
fields, so both should have three; under the cells as written they differ.
The criterion did not describe the cells.

What does describe them is simpler and was visible in the condition texts
all along. T21 says "*larger than*" and L44 says "*exceeds*": each bounds
its comparison in one direction, so there is one shape. T3, T14 and T22 say
"*is not exactly*", "*differs from*" and "*does not equal*": either
quantity can be the greater, so there are two. L21 names two layout
formulas in its own text — "N interleaved, C·N planar" — against a cell
reading `—`.

And §21.1 never stated either axis. The criterion lived only in an ADR, so
a corpus builder reading the specification alone could not reproduce the
counts the specification publishes.

**The ordering key.** Appendix G's reproducible-writer profile ordered
records "by type, and within a type by their encoded bytes compared
lexicographically". A record's encoded bytes are its 24-byte header, and
the header contains extent_offset — which item 3's own emission order is
what fixes. The key therefore depended on its own result, and for two
records of one type other than 0x0001 it could not be evaluated at all.
Three reporters found it independently.

## Decision

**State both axes in §21.1**, as rules rather than judgements: where the
quantity a condition derives varies by layout, the layout formulas are
materially different shapes and the cell enumerates them; where the
condition compares two quantities and either can be the greater, the two
directions are enumerated; where its own text bounds the comparison in one
direction, there is one.

The cells follow: **T22 gains the direction axis** it shares with T14 (3 →
6) and **L21 enumerates its two layout formulas** (1 → 2). T21 and L44
keep three — their conditions are one-directional, which is now something
the specification says rather than something an ADR asserted. Register
totals move from 121 conditions over 264 instances to **121 conditions
over 268 instances**, and the corpus from 316 to **320 vectors**.

ADR-0076's cells stand unchanged. What is superseded is its criterion,
which described the intent and not the result.

**De-circularize the ordering key.** Within a type, type 0x0001 ties by
layer name; every other type ties by the record's header **with
extent_offset masked to zero**, then its inline payload, then the contents
of its extent, compared lexicographically. Masking extent_offset is what
makes the key evaluable — it is the one component this order fixes. Every
remaining component is a function of content alone, so the key stays
derivable by a reader, which a creation order is not. Two records the key
does not separate are byte-identical in type, flags, lengths, payload and
extent content, so emitting them in either order yields the same file and
the writer chooses.

The alternative — dropping item 3's total-order promise for multiple
records of one type — was rejected because the profile's whole value is
that a caller can predict the bytes, and the gap is closable exactly.

## Consequences

Four vectors, on the constructions their siblings already use. L21's
planar instance is the interleaved one under layout 2, where the derived
count is C·N. T22's three "declared larger" instances need one care the
"declared smaller" three did not: those frames are single-segment, where
Window_Size *is* Frame_Content_Size, so declaring a larger value would also
declare an oversized window and co-violate T21. Clearing Single_Segment
with an explicit window_log of 10 fixes Window_Size at 1024, above every
decoded size in play, so only the Frame_Content_Size relation fails.

`COV-05` failed on twelve findings until the cells and the vectors agreed,
which is the design: a register rewording breaks the build until its
vectors are re-annotated.

The deeper lesson is about where a criterion lives. ADR-0076 applied a rule
correctly to six cells and stated it wrongly, and nothing caught the gap
because no instrument compares an ADR's prose against the cells it
authorises. What closed it was a fresh reader holding the register to
§21.1 — the instrument ADR-0034 exists to provide, doing exactly the work
`conformance/README.md` says the mechanical checks cannot.

## Precedent

- ADR-0049, which recounted the register against its own counting rule;
  this states the rule that recount was applying.
- ADR-0064, which made the instance's verbatim cell text the corpus key —
  why re-annotation is a vector edit and why COV-05 fails rather than warns.
- ADR-0073's blind spot, restated: a term-overlap check cannot see two
  passages that disagree, and cannot see prose that lives outside the
  document entirely.
