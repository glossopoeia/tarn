# Maintainer's own pass over round 15's repairs (run while round 16 was in flight)

**M-01 — §20.3 step 4's shrink branches are stated as alternatives but
overlap. REAL, mine, in the sentence's fourth revision.**
The text reads "Where the shrink leaves a stored tile addressed it is the
case above — barred wherever it alters what §14 fixes for that tile — but
where it drops a tile out of the addressed set entirely …, nothing is
altered for a tile the new state stores, and the commit is permitted".
Counterexample, one commit in both branches: extents (8,8), tile extents
(4,4), all four tiles stored. Shrink to (4,7). Grid falls (2,2) → (1,2), so
the two t_y = 1 tiles are de-addressed — the second branch, "permitted" —
while the surviving edge tile t = (0,1) gains a padding column at x = 7,
which [R-SER-05] fixes to fill and which its stored bytes need not hold —
the first branch, "barred". The clause "nothing is altered for a tile the
new state stores" is asserted as a consequence of de-addressing and is
simply false here.
Fix: make the test uniform rather than branched — a shrink is permitted
exactly where it alters nothing §14 fixes for any tile the new state still
stores; tiles it drops out of the addressed set are gone, their extents
becoming slack.
Byte-level: this is the same class as rounds 14 and 15 — two readings of
whether a conforming appender may emit a given generation-g+1 file. I grade
it byte-level pending triage's independent view.

**M-02 — the [R-SER-08] repair fixed a mis-citation and introduced a
mis-attribution. REAL, mine.**
§21.1 now reads "`[R-SER-08]` is the one rule that goes the other way …
which is why §14.2 calls it the sole resolved byte in this format."
[R-SER-08] is indeed defined in §14.2 (line 1849), but §14.2 never
characterizes it that way. The uniqueness claim is §12.3's — "the one case
where a reader resolves a byte to a value rather than passing it through
arises only in a nonconforming file, and [R-SER-08] states it" — and the
phrase "sole resolved byte" is Appendix H's checklist wording.
This is the overcorrection class: a repair to a wrong citation that lands a
second wrong citation one clause later.
Byte-level: NO. Editorial.
Fix: attribute it to §12.3, which makes the claim, rather than to §14.2,
which states the rule.
