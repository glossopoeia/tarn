# Maintainer's own pass over round 13's repairs (found while round 14 ran)

**M-01 — §20.3 step 4's repair is ambiguous, not self-contradictory. REAL but weaker than first judged.**
The sentence reads "a change that reaches none of these for any tile the
layer stores — a filter whose mandated stride makes it the identity, or a
new padding position whose stored byte already holds the fill — leaves
every stored tile conforming and is not what this bars."
"These" refers to the preceding enumeration (padding-position set, decoded
size, sample offset, codec and filter). Both illustrations DO alter an
enumerated item: a filter change alters "the codec and filter that produced
the stored bytes"; a new padding position alters "the set of padding
positions". So the sentence defines the exempt class by the enumeration and
then illustrates it with changes the enumeration covers.
CORRECTION on re-reading: "these" has two possible antecedents — the
enumerated declarations (contradictory reading) or the effect clause "what
§14 fixes for its stored bytes or how they decode" (coherent reading). The
preceding clause, "the list names where that effect arises rather than
standing on its own", explicitly subordinates the list and signposts the
coherent reading. So this is an AMBIGUITY whose charitable reading is
available and signposted, not a flat contradiction — I overstated it on
first pass. It still deserves a fix, because the sentence exists precisely
to remove this confusion and instead reproduces it one clause later.
Fix: name the effect explicitly — "a change that leaves every stored tile's
bytes meaning exactly what they meant".
Byte-level: NO — both readings leave the emitted/accepted byte sets
identical (a creator could emit the same file from scratch); what differs is
one updater's permission.

**M-02 — four prose lines exceed the document's hard wrap.** Lines 538 (79),
3203 (92), 3468 (113), 4042 (107), all introduced by round 13's repairs.
Cosmetic, but the hard wrap is load-bearing for line-oriented tooling.

**M-03 — "the run partition" in [R-SLB-04] is grounded but unlinked.**
[R-SLB-02] says "Runs partition each contiguous block of disk ordinals
independently", so the term is readable, but the rule would be clearer as
"the partition of ordinals into runs (`[R-SLB-02]`)". Marginal.
