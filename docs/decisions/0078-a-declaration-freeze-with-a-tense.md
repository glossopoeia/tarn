# 0078. A declaration freeze with a tense

- Status: Accepted
- Date: 2026-08-20
- Covers: §20.3 step 4's tense; §21.7's witness list; §21.1's direction
  criterion; cells F17, L21, L22, L30
- Supersedes: ADR-0077's direction criterion (its cells stand; the
  criterion is narrowed)
- Confirm: none

## Context

Cleanroom round 14 read round 13's seventeen repairs and found fifteen
defects in them. One was byte-level — the first since round 12 — and it sat
in the repair ADR-0074 had written to close round 12.

**The tense.** §20.3 step 4 bars a commit that changes a layer's
declarations "in a way that alters, for any tile that layer **stores**,
what §14 fixes for its stored bytes or how they decode". Nothing said which
generation *stores* refers to. The separating operation is ordinary:
**recompressing a layer** — change the codec, re-emit every stored tile
under it. Read against the prior generation's stored set the commit is
barred; read against the set the commit publishes it is permitted, because
every tile the new generation stores was produced under the new codec and
is consistent with it.

Two of the three triage passes upheld it byte-level and asserted that no
text in the document names a tense. **That assertion was wrong**: §3.1 says
"unqualified *stored* means stored in the live generation", which the third
pass found and the other two missed. But §3.1 does not finish the argument
either, because the live generation during a commit in flight is the
pre-commit one while §20.3's own gloss is framed on the committed outcome,
and nothing arbitrated between them.

The finding is byte-level on the narrow test. A creator emits generation 1
(§20.1) and a compactor generation 1 under a fresh `file_id`, so a
generation-g+1 file is producible only by a commit; the two-commit
workaround publishes at g+2. The disputed byte sequence is therefore
emittable under one reading and by no conforming implementation under the
other.

**The direction criterion, a third time.** ADR-0076 enumerated six cells
and described the rule wrongly. ADR-0077 stated the rule in §21.1 and fixed
the two cells round 13 named. Round 14 found four more of the same shape,
seven of its eight reporters independently. A mechanical sweep of all 121
rows confirmed their list exactly — and, in the process, falsified the
criterion ADR-0077 had written.

## Decision

**The tense is the prior generation's.** §20.3 step 4 now reads "for any
tile that layer stores **in the generation this commit supersedes**", and
says outright that a commit does not escape the bar by unstoring in the
same breath.

The ground is the one ADR-0068 and ADR-0074 already settled, and it is the
maintainer's: `[R-LIF-01]` freezes committed bytes where they lie, so
re-emitting a layer's tiles strands the originals as slack — a whole
layer's worth, reclaimed only by compaction. Recompress-as-a-commit is
exactly the operation that reads like a directory edit and leaves the file
larger, and the reading that permits it is the reading that hides the
cost. Barring it steers the operation to the whole-file rewrite, which is
the only path that strands nothing.

Two costs are recorded rather than argued away. **The rule steers; it does
not prevent.** A tool can still reach the same end state in two commits —
unstore every tile, then re-declare a layer that now stores none — and
strand the same bytes plus an extra index region, directory and trailer.
What the rule buys is that the expensive path is visibly two operations
instead of one that looks free. **And the bar loses its witness in exactly
the case that motivated the question.** Where the affected tiles remain
stored the §21.4 rows fire; where a commit supersedes every tile it would
have damaged, the live state is clean and nothing in the file records the
violation. §21.7 now says so, on the same footing as `[R-LIF-01]`: it is a
property of the prior generation, which §9.7 does not reconstruct.

**The direction criterion is narrowed to what it meant.** §21.1 now
excludes two classes the earlier wording swept in: a comparison with no
magnitude ordering — a stored checksum against a computed one, a byte
pattern against a constant, where *greater* names nothing — and a field
tested only for being nonzero, an *A ≠ 0* or *S ≠ 0*, which is a value test
and not a comparison of two quantities at all. Both exclusions were found
by running the criterion mechanically over all 121 rows and reading what it
wrongly caught: F14's trailer CRC, and L20, L29 and T5's nonzero tests.

Under the narrowed criterion four cells gain the axis — F17, L21, L22 and
L30 — taking the register from 121 conditions over 268 instances to **121
conditions over 273**, and the corpus from 320 to **325 vectors**.

## Consequences

Five vectors. F17's "physical file longer" needed a construction the
corpus had recorded as unbuildable: appending arbitrary bytes displaces the
trailer, so the file fails F8's magic instead. Appending a byte-identical
copy of the trailer keeps a valid, CRC-verifying trailer at the physical
end whose `committed_file_length` names 128 against a 192-byte file — F17
and nothing else. L21's and L22's larger directions needed a seed deriving
more than one tile, since seed `pair` sits at the N = 1 floor where nothing
can make `entry_count` the larger side; seed `l21big` supplies it, with a
512-aligned spacer layer whose gap is what lets L22's `extent_length` grow
without running into the next structure.

The maintainer's own pass over round 13's repairs, run while round 14 was
in flight, found one defect the round did not: §20.3's "a change that
reaches none of **these**" binds either to the enumerated declarations or
to the effect clause they gloss, and the two readings disagree. It is
repaired here in the same sentence as the tense.

**The recurrence is the finding.** Three consecutive rounds have found this
one criterion incomplete, because each round fixed the rows it named rather
than sweeping the rule across the register. This round swept it. The
maintainer declined a mechanical check for it, so the sweep is recorded
here as the method: applying §21.1's criterion to all 121 rows is what
found F14's false positive and the three nonzero tests, and it is what a
fourth recurrence would need.

## Precedent

- ADR-0068 and ADR-0074, whose cost argument this applies to a new
  operation: a cost discovered is worse than a cost chosen.
- ADR-0073's blind spots, both live here — round 14 read one commit's worth
  of repairs, which is the shape the propagation check cannot audit.
- §3.1's definition of *stored*, which existed all along and which two of
  three triage passes denied existed. A term defined once and relied on
  implicitly is a term two careful readers will miss.
