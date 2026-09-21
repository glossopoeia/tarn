# 0131. Round 36's repairs: three clauses, after a zero read on a weaker instrument

- Status: Accepted (resolves round 36's repairable findings, on the
  maintainer's direction of 2026-09-21)
- Date: 2026-09-21
- Covers: §3.3's Note; §20.3's three-shapes Example, figure (b); §20.4's
  preservation table, its MU = 0, PE = 0 row
- Confirm: none. Nothing here takes a decision about what a conforming actor
  may do. The maintainer directed the three repairs on 2026-09-21 and, with
  them, that the cycle begin again: an audit of this commit and a round 37.
  Round 36's zero is recorded in its findings and G3 is not declared met on
  it.

## Context

Round 36 read ADR-0128, ADR-0129 and ADR-0130 with their errata, two audits
and the maintainer's rulings, thirty-one passages over seven commits. It ran
on Sonnet throughout, on the maintainer's instruction of 2026-09-21, after
Opus had refused every whole-surface audit brief of the cycle and the round's
quiz author, twice each, and a run on the driver had eleven of its twelve
started lanes refused. It returned 8 findings from 5 reporters, 8 distinct
defects with the three passes partitioning identically, a 15/15 quiz by hand,
and **no byte-level finding: none self-flagged, none upheld by any pass.** The
refute phase fired on the zero: seven targeted refuters returned
DOWNGRADE_STANDS with their constructions stated, the round-wide attacker
found no fork after four constructions, and the hand-check of every verdict,
and of the one group the cap left unattacked, found no sentence two
implementations read to different bytes. The findings file records every
verdict.

**The zero is recorded and the criterion is not declared met.** Rounds 31
through 35, on Opus, returned 24 to 29 findings each; this round returned 8
over a wider surface, in the proportion of the one measurement on record,
Sonnet's 2 findings to the driver's 8 on identical hunks. The record cannot
tell a settled text from a weaker reader. The maintainer's direction is to
repair what the round found and read the document again.

**What the round found** is wording, three clauses of it repairable. Decisions
E1 and E2 of ADR-0130 and E3 of ADR-0129, the text the two audits and the
maintainer's rulings had settled, drew no finding.

## Decision

Three repairs, each one clause.

1. **§3.3's Note listed verifiers among the actors that operate on files
   whose layers they cannot decode.** §9.7 has a verifier that certifies
   decode every stored tile, and `[R-CNF-03]` with `[R-COD-11]` makes every
   core codec and filter a verifier's to implement. The claim about verifiers
   predates this cycle; ADR-0129's erratum renamed the sentence's third actor
   and left its first. The Note reads *"so appenders, and rewriters carrying a
   layer forward, operate on files whose layers they cannot decode"*. A
   labelled Note; no normative sentence deferred to it.
2. **Figure (b) of §20.3's three-shapes Example carried the document's one
   unclosed annotation bracket.** Its label opened under the boundary between
   the new tiles and the new index region and ran to the end of the line, so
   a reader could take *re-emitted* to describe the tiles a commit appends,
   which step 4 never says of new bytes. The bracket closes under the new
   index region alone, columns 54 to 63 between that field's two separators,
   and the caption follows it: *"└────────┘ every entry, re-emitted"*.
3. **§20.4's last row gave a commit-shaped licence to a class one of whose
   tiers never commits.** *An updater MAY drop the record in any commit*
   reached the rewriter in its words and not in its sense, the same sentence
   licensing the rewriter's drop in its next clause. The pre-round audit's
   tiers lane raised the clause and the driver declined it; a second
   independent reader found it in the round. It reads *"so an appender MAY
   drop the record in any commit it is otherwise free to make"*. No actor
   gains or loses a drop: an updater that commits is an appender, and the
   rewriter's licence stands where it stood. The row's closing sentence, that
   an updater that drops such a record SHOULD report the loss, keeps the
   class, since it binds both tiers.

**Left to the maintainer, not reworded.** Step 4's tie-break sentence, which
ADR-0126 and ADR-0127 each rewrote, says a planar and an interleaved channel
list are each on both sides of the two lists; each list names one of them and
reaches the other through a general clause. The face-value reading is false
of both examples, the cross-checked reading is true, and the two decide every
commit alike. The standing direction is to say so and stop.

**Declined.** The register's total of 277 instances, recounted by the round's
own register walk by hand and by script and established by `tarn_check`. The
slab-run carve-out for a crc-only failure, stated in terms in §16.2, §15.3
and row L41. §15.1's unlabelled blockquote, normative under `[R-CNF-01]`,
known, named by the charter, and pinned again by `[R-IDX-01]` and
`[R-CNT-17]`. And the unexplained difference between an appender blocked from
one layer and a rewriter from the whole file on an unimplemented MU = 1
record, each rule being plain where it stands.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors.
No reader, writer or verifier behaviour changes.

**The audit chain opens again**, as it does after every repair commit: this
commit is unaudited until the pre-round-37 audit reads it or round 37's
charter hands it to the round. Three clauses are within what the convention
hands to a round.

**The harness owes three fixes before round 37**, none of them the
document's: each refute call's verdict enum restricted to its own labels,
the round-wide attacker having answered in the uphold-refuter's; *do not list
it* said where a brief names the shared output directory, three agents having
listed it and disclosed it; and the quiz normaliser taught to ignore answer
enumerators.

**The repair list was ticked against the diff** before the commit, on
ADR-0119's rule: three items, three edits, none deferred.

## Alternatives rejected

- **Declare G3 met on round 36's zero.** Not taken: the zero is real and the
  instrument is unmeasured against the one that set the project's calibration
  lines. Stated so the maintainer can take it.
- **Hold the repairs and read the same charter again on another instrument.**
  Rejected on the maintainer's direction: Opus and the driver refuse these
  briefs as written, a reworded brief is untried, and three clauses do not
  justify holding the document still.
- **Restore verifiers to §3.3's Note with a qualifier**, a verifier checking
  every Part I structure of a file whose layers it cannot decode and
  reporting *cannot establish*. Rejected: true, and a restatement of §9.7 in
  a Note that needs none.

## Precedent

- **ADR-0127**: the previous zero's repairs, and the form of this ADR.
- **ADR-0129** and **ADR-0130**, with their errata: the text the round read
  and found settled.
- **ADR-0119**: the repair list against the diff.
- **ADR-0104**: editorial repairs ride with the round that found them.
