# The repair audit of ADR-0085, before round 21

One hunk, seven lines. Two auditors, adversarial verification, then a
refute-only pass over both downgraded byte-level flags.

| | |
|---|---|
| Findings | 10 |
| After adversarial verification | 1 PARTIAL, 9 REFUTED |
| Reporter-flagged byte-level | 3 |
| **Byte-level after the refute phase** | **0** |
| Harness | 12 agents + 2 refuters, 0 errors |

**The first pre-round audit to come back with no byte-level defect.** The two
downgraded flags were attacked and both returned DOWNGRADE_STANDS, each on an
independent ground rather than by endorsing the downgrader's reasoning — X-03's
refuter verified the load-bearing premise three separate ways in the document,
and X-01's found the downgrade's own point 1 unsound while the verdict stood
anyway.

## What was fixed

- **§21.5's capability carve-out named only "the size bound"** — the sweep made
  in ADR-0083 covered one bound, and ADR-0085 created a second. Both bounds are
  now named. This is the unswept-restatement shape the audit exists for, caught
  one repair after the repair that created it.
- **`[R-ERR-03]` was cited for two propositions that are `[R-ERR-04]`'s** —
  "remains conforming" and "a reader MAY decline it" are the next paragraph.
  Two auditors found it independently, and §2.3 settles it: `[R-CNF-03]` says
  "§21.9's `[R-ERR-04]` governs a refusal on that last ground". Now cited to
  `[R-ERR-04]`.

## A process artifact, recorded because it would otherwise be invisible

The §21.5 fix was applied **while the refute pass was running**, so X-01's
refuter read the already-corrected preamble and reported, honestly, that it
could not tell whether the auditor had misread the text or the text had been
amended under it — being barred from git history. Its verdict does not depend
on the difference: it granted the auditor's own quoted wording and showed the
emittable set does not move under it either. But the sequencing was wrong.

**Rule for future rounds: do not apply repairs to a passage while a refute pass
is reading it.** The refuter's whole value is judging the text the finding was
written against.

## The injected context, again

Both auditors and one refuter disclosed the runtime injection unprompted. One
refuter went further and named the specific contamination: a completed-task
list carrying prior ADR identifiers, one of whose titles states a scope
conclusion about a metadata refusal — and it said plainly that this *suggested
a construction to it*, which it then tested against the document and reported
as dead on the document's own words rather than on the hint.

That is the ADR-0084 clause working at its limit: the leak is not fully closed
— a task list is not something the charter can suppress — but the agent
recognised it, refused to rest on it, and said so.
