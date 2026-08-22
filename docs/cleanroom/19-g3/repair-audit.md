# The repair audit of ADR-0083, before round 19

Second run of the instrument ADR-0081 introduced. Three hunks,
`2f54d8d..62d0310` — the repairs that resolved round 18's byte-level finding.

## Result

| | |
|---|---|
| Auditors | 3 (2 hunk-group + 1 cross-hunk) |
| Findings | 16 |
| After adversarial verification | **3 CONFIRMED, 1 PARTIAL, 12 REFUTED** |
| Byte-level confirmed | **1** |
| Harness | 19 agents, 0 errors, 0 empty returns |

**Sixteen findings in a twenty-line repair, one of them byte-level.** The
repair was written with the round-18 finding in hand, ran four gates clean, and
was still the most defective text in the document an hour later. That is the
pattern the gate board has recorded for five rounds, now measured directly
rather than inferred a round late.

## The byte-level defect: a scoping fix that overshot

ADR-0083 scoped the compactor's `version_minor` floor to "where any unknown
ignore-lane bit is set" — narrowing it to the case its rationale named. But the
rationale is not specific to flag bits. §10.1 `[R-EXT-01]` says the format
grows through **four** vehicles, and §18.3 `[R-MTA-06]` equates two of them in
terms: "later minor versions register keys, **exactly as they define
ignore-lane flag bits** (§6.3), and this text's readers skip both harmlessly."

A compactor MUST carry a user-metadata record forward (§20.4: both registered
types carry PE = 1) and **cannot inspect it** — §20.5 fixes its verification
depth at `[R-WRT-09]`'s, which "reaches no decoded content". So for an input
whose only later-minor feature is an unrecognized `tarn.` key, the else-branch
fired and `[R-CNT-26]`'s floor is not computable: the floor is "the lowest
version_minor that defines every feature present in the file", and the
compactor cannot see the feature. Two compactors, one input, different bytes at
the trailer, both outputs conforming.

Fixed by widening the trigger to any feature the compactor does not implement,
naming both vehicles.

## The two the cross-hunk auditor was needed for

- **Appendix G item 8** told a profile-adopting compactor to write `flags = 0`,
  which §20.5's new MUST forbids. The auditor noted why nothing else could have
  caught it: invisible to a single-hunk auditor with no reason to open the
  appendix, and invisible to `tarn_propagate`, since item 8 and §20.5 "share
  almost no vocabulary beyond the field names." Item 2 of the same appendix
  already carries the exact carve-out pattern for `file_id`; item 8 now mirrors
  it.
- **§21.7 recorded only one of the two obligations** §20.5 claimed were
  unwitnessed — a citation reaching half as far as the sentence citing it. The
  maintainer's independent pass found this too, before reading any return.

## The instrument reading on itself

Twelve of sixteen findings were REFUTED by adversarial verifiers, and the three
that survived were each independently corroborated — one by the maintainer's
own pass, one by three separate auditors, one by a walk of the appendix. The
verifier pool's REFUTED-by-default framing again suppressed a real one: A-02
and A-04 were graded REFUTED while B-01, the same underlying defect seen from
another hunk, was CONFIRMED. **A split across verifiers on one defect is the
shape the refute phase exists for**, and it is why the confirmed set was
cross-checked by hand rather than taken as given.

---

# Second and third passes, over the fixes

The audit above found four defects; fixing them produced a diff that was
audited again, and that produced a third.

| pass | surface | findings | confirmed / partial | byte-level after refute |
|---|---|---|---|---|
| 1 | ADR-0083's three hunks | 16 | 3 / 1 | **1** |
| 2 | the four fixes, plus two I found myself | 15 | 1 / 3 | **0** |

**Pass 2's byte-level flag was downgraded, and the refute phase upheld the
downgrade on a general ground rather than a case-specific one.** `[R-CNF-12]`:
"Deviation from a SHOULD is not a violation for this purpose: §21's register
enumerates MUST-level conditions only." Since ADR-0083 made the clause
explicitly a SHOULD, and `[R-CNT-07]` forbids a reader rejecting on
`version_minor`, and `[R-CNF-05]` gates emission on file conformance, **no
formulation of this clause can move the emittable set.** The question is closed
permanently, not settled for one wording.

That also re-reads round 18's finding: it was byte-level *because the mandatory
reading was still available*. Fixing the modal did not merely repair the
sentence — it removed the sentence from the class of things that can be
byte-level at all.

## What pass 2 corrected

- **The enumeration, twice wrong in opposite directions.** ADR-0083 named two
  growth vehicles and pass 1 found it short; I replaced it with a deferral to
  all four of §10.1's, and pass 2 found *that* over-reaching — two of the four
  reach a conforming file only as reserved-range values this text registers as
  violations (F36, L25, R1). The stable form is the original two **with the
  reason they are exhaustive**, which is what was missing all along.
- **Appendix G item 8** claimed "both are creator's rules"; the `version_minor`
  half binds a compactor too. Each half now carries its own scope, and the item
  concedes what the profile cannot deliver: a compactor's output is
  reproducible only modulo its trailer, since `[R-WRT-06]`'s fresh `file_id` is
  no function of content.
- **Appendix G's closing paragraph**, which pass 1 had explicitly told me to
  sweep and I had not.

## The reading

Three passes, three sets of defects, each in the fix for the last. The
instrument is not converging on a clean diff by iteration — it is finding a
different defect each time because each fix is new text. What changed by pass 2
is the *severity floor*: pass 1 found a byte-level defect, pass 2 found none
that survived, and the reason is structural rather than lucky. That is the
first evidence in this project that a passage can be argued out of the
byte-level class entirely.
