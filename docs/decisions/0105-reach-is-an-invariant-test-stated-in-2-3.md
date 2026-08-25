# 0105. Reach is a test on the invariant violated, stated in §2.3

- Status: Accepted (resolves Q-H4, Q-H5 and Q-H6)
- Date: 2026-08-25
- Covers: §2.3's `[R-CNF-02]` and the new `[R-CNF-13]`; §21.2's opening paragraph
- Revises: the reach reasoning §21.2 has carried since it was written
- Confirm: none

## Context

§21.2's opening paragraph decided which file-scope rows reach a file declaring a
format major other than 1. It drew findings in three consecutive cleanroom
rounds and spawned three ledger entries — **Q-H4** (can detection order settle
reach), **Q-H5** (which verdict follows once a row reaches), **Q-H6** (can the
paragraph's design work at all). A sweep run before any option was put to the
maintainer — four independent spec-only readings, two option drafts, and
adversarial verification of every claim that the document already decided
something — established that three of those questions were partly misframed and
one real contradiction sat underneath all of them.

**What was already decided, and so needed no decision.** Q-H4's leading option
was to make §6.2's validation order a MUST. It already is: `[R-CNT-06]` reads "A
reader MUST validate, **in order**: the trailer magic; the trailer CRC; the
version gate". And the reach *count* was not wrong — five rows have a
`[R-CNT-24]`-fixed subject, but F18 is outside the premise, since
version_major = 0 declares no major at all, so four reach and the paragraph said
four.

**What was wrong.** The excusing property was empty: a walk of all 36 file-scope
rows found **no sense of "geometry" that any of them satisfies**, so the
partition's first half selected nothing. The warrant was miscited: the paragraph
says the four reach "because their subject is a field fixed across every major
(`[R-CNT-24]`)", but F8 and F14 are governed by `[R-CNT-06]`, F6 by `[R-CNT-04]`
and F1 by `[R-ENC-02]` — not one by `[R-CNT-24]`. The procedural argument did not
cover its own cases: the front-block check is not in §6.2's ordered list at all,
`[R-CNT-04]` places it, and `[R-RDR-02]` licenses a reader to detect any
violation earlier in any case. Two conforming readers were shown to report
materially different verdicts on one 100-byte file declaring major 2.

**And underneath, a contradiction nothing in the document resolved.** §21.2 says
four rows reach such a file. §21.1 makes a row a file-conformance violation.
`[R-CNF-11]` gives an established violation priority and forces *nonconforming*.
But `[R-CNF-02]` says such a file is "neither conforming nor nonconforming". A
major-2 file with a failing trailer CRC therefore had two incompatible answers,
and §21.1's "the rule governs" does not reach it, because the divergence is
between §21.2's prose and `[R-CNF-02]`, not between a row and the rule it cites.
The fault line is that **"reach" was never defined.**

## Decision

**Reach is a test on the invariant a condition violates, and it is stated in
§2.3 as `[R-CNF-13]`.**

> A requirement reaches a file declaring a format major other than 1 when, and
> only when, the invariant its condition violates is one `[R-CNT-24]` fixes in
> every format major version.

**The test is the invariant asserted, not the bytes read**, and that distinction
carries the weight. F14 reaches although the bytes it checksums include fields a
future major is free to redefine: it consumes them as CRC input and asserts only
`[R-CNT-24]`'s CRC-32C at F − 4. F5 does not reach although its subject is the
physical file size, which no major can redefine: the 128-byte floor it asserts is
derived from a directory of at least 4 bytes at an offset of at least 16 and a
64-aligned F, which are major 1's. F15 does not reach although its Governing rule
cell cites `[R-CNT-24]`: the trailer bytes it requires be zero are inside the 48
that rule lets a future major redefine. Every reading that admits F14 on a
"fields consulted" test also admits F5 wrongly; every reading that excludes F5
also excludes F14. The invariant test separates them.

**"Reach" is substantive, so the verdict is *nonconforming*** — and it needs no
relativising. The invariant broken is one the file's own major shares, so the
finding is not relative to format major 1 and a verifier reports it whether or
not it implements the declared major. `[R-CNF-02]`'s "neither conforming nor
nonconforming" is bounded to the requirements that do *not* reach. That reading
is what §21.2's own stated reason presupposed — a rule holding in every major is
one whose breach a major-1 verifier can establish without judging major 2 — and
it is what §9.6's `[R-LIF-06]` ("fails `[R-CNT-06]`'s gates") and §5.2's
`[R-CNT-21]` ("the verifier reports the trailer failure") already describe. The
alternative, reading reach as the reader's detect-and-reject duty alone, would
oblige a verifier that has *proved* the trailer magic wrong to report that it
established nothing.

**§2.3 is where it belongs**, and §21.2's preamble is reduced to a restatement.
The document's placement discipline is uniform and written down four times —
`[R-CNF-08]`'s "owning scope … stated in the section that defines the
structure", §21.9's "each is normative where the structure forcing it is
defined", §20.5's "which is why the rule is stated here and not left to the
rows", and §21.1's "each row *restates* its governing rule … the rule governs".
A rule deciding which requirements apply had been sitting in the section whose
own opening says rows restate rather than state. §2.3's first bullet already
defines the premise.

## Consequences

**The register does not move: 121 conditions, 277 instances, 331 vectors.** The
dispositions `[R-CNF-13]` yields — F1's two instances, F6, F8 and F14 reaching,
F18 outside the premise, the other 31 not reaching — are the ones the old
paragraph reached by listing, so nothing a reader was told before becomes false,
and no Condition, Instances, Detector, Detected or Governing rule cell changes.
No vector is owed: a file this text declines to judge is not a register instance.

One identifier is added, `[R-CNF-13]`, in a space that ran 01–12 without gaps.
Five propagation acknowledgements, all for passages that corroborate the new rule
rather than lag it — §9.6 and Appendix H both already described the gate outcome
as a failure the verifier reports.

**`SPEC-03` caught a defect in this ADR's own drafting.** The first version of
`[R-CNF-13]` wrote "a check may consume bytes a future major may redefine", and
the gate flagged both as lowercase BCP 14 keywords in normative text. They were
descriptive, not permissive — but §2.1 binds keywords only in capitals, and a
lowercase *may* in normative prose is exactly the ambiguity that discriminator
exists to prevent. The sentence now avoids the word. That is the same gate whose
one-cell blind spot ADR-0081 closed, working on new text.

**Q-H4, Q-H5 and Q-H6 are all resolved by this one decision**, which is what
Q-H6 predicted: "Q-H4 and Q-H5 fold into whichever is chosen." Sixteen ledger
entries remain.

## Precedent

- ADR-0095's rule that a partition stated by a property beats a list, applied to
  the property itself: the failure here was a partition whose excusing half
  selected nothing, and no amount of adding members would have found that.
- ADR-0094's rule that a decision offered before the document has been swept is
  taken blind. The sweep is what showed Q-H4's leading option was already law and
  the alleged miscount was not a miscount.
- §21.1's "the rule governs", which is why a rule stated in the restating section
  was the wrong shape regardless of what it said.
