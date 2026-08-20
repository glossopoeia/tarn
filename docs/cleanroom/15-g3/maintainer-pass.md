# Maintainer's own pass over round 14's repairs (run while round 15 was in flight)

**M-01 — §21.1 states the outcome-follows-from-scope claim TWICE, and round
14's repair fixed only one. REAL, mine.**
Line 3199 now reads "with the outcome class its scope determines (§2.4) —
except where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine does
for every §21.5 row, whatever the containing scope —".
Line 3214 still reads "Conditions attach to the finest structure they
damage, and the outcome follows from that scope, never from the severity of
the corruption", with no exception.
Round 14's own triage note named both sites verbatim; the repair swept one.
`tarn_propagate` cannot see this: both sites are in one section and one of
them changed in the same commit, which is the blind spot ADR-0078 records.
Byte-level: NO — §21.5's rows state their own outcome and §21.1 resolves a
row/rule divergence in the rule's favour, so no verdict turns on it.
Fix: carry the same exception to the second statement, or make the second
refer to the first rather than restating it.

**M-02 — Appendix G item 2 explains a word it no longer uses. Mine.**
The repair replaced "its low eight digest bytes" with "the digest's **last
eight bytes in output order**", but kept the gloss "*low* names their
position in the digest, not an arithmetic magnitude, and the two readings of
that word are why this says which end." A reader meeting this fresh finds
*low* defended but never used. Fix: drop the gloss — explicit wording needs
no defence — or keep one clause noting the term it replaced.
Byte-level: NO. Editorial.

**M-03 — §21.2's new preamble over-claims. REAL, mine.**
It says a file declaring another format major is one "no row below reaches".
But §6.2 validates "the trailer magic; the trailer CRC; the version gate" in
that order, so three rows fire before the major is ever read: F8 (trailer
magic), F14 (trailer CRC), and F1's trailer-magic instance. Those fields are
the ones `[R-CNT-24]` fixes across all majors, which is exactly why §6.2
puts them first. The sentence should except them rather than deny them.
Byte-level: NO — §2.3 already governs the verdict for a foreign-major file
and the rows state their own detection points; this is register prose
claiming more than it can.

**Considered and not changed:** §22.3 and Appendix H restate the slack-total
obligation without round 14's new "reaches a live state" carve-out. Both
describe the ordinary case, §5.2 states the rule, and the carve-out concerns
a file that fails the trailer gate — which is not what either passage is
about. Recorded so the omission is a decision rather than an oversight.
