# 0134. Truncation to the last committed state is an updater's operation

- Status: Accepted (resolves Q-A10, option (b), on the maintainer's
  direction of 2026-10-14; drafted by the driver at the maintainer's
  request; the first decision against edition A since the readable edition
  opened, ported to it under ADR-0133 decision 1)
- Date: 2026-10-14
- Covers: §9.6, a new `[R-LIF-09]`; §20.1 `[R-WRT-01]`; §2.3 `[R-CNF-06]`;
  Appendix H's updater entry
- Confirm: none. `[R-LIF-09]` carries no register row: the conditions it
  states are unwitnessed under §21.7's test, a truncated file being bytes
  a conforming creator could have written, as `[R-LIF-04]`'s and
  `[R-LIF-06]`'s are; so no vector either.

## Context

Q-A10 (2026-10-13, the maintainer reading §9.2's Example): §2.3 defines
five conformance classes and Appendix H carries five checklists, none for
recovery. §9.6 names a further actor, *"Recovery tools and verifiers —
never conforming readers on the default path — locate commit states as
follows"*, binds "the tool" by `[R-LIF-06]` alone (re-verify as a whole
file; report the candidate and the count rejected), and says of the
surviving candidate that *"truncating to it recovers the file"*.
Truncation is otherwise a writer's act: §9.4 has a writer that established
F from re-verified recovery output truncate to it or overwrite from it
before re-appending. So the tool that scans, picks and truncates belonged
to no class. Nothing said it answers for the file it leaves, and
`[R-LIF-01]`, which binds *a writer*, did not reach a tool that truncated
to generation n − 1 while n was intact, the rollback §9.6's two cautions
describe as an attack. Three options stood: a sixth class with its own
checklist; the truncating tool an updater performing a named operation;
recovery tools outside the classes, bound by `[R-LIF-06]` alone.

## Decision

1. **The operation.** Truncation of a file to its last committed state,
   the nearest-to-end candidate that survives §9.6's whole-file
   re-verification, is an operation of the updater class beside the
   appender's commit and the rewriter's rewrite, on ADR-0129's model:
   *"Every obligation of §20.3 through §20.5 attaches to an operation and
   binds whichever writer performs it"*. The tool performing it is an
   updater and the file it leaves is its output; it produces no bytes and
   carries forward every byte of the state it leaves. §20.1 and
   `[R-CNF-06]` say so in a sentence each.
2. **`[R-LIF-09]`**, a new paragraph of §9.6 after `[R-LIF-06]`'s, binds
   the operation: the tool MUST NOT modify a byte below the candidate's
   committed file length, and MUST leave the physical file length equal
   to it, so that it leaves exactly the committed state the
   re-verification established; `[R-LIF-01]` binds it as every updater, so
   an earlier commit state is not one it is free to truncate to, that
   truncation removing committed bytes; its probe is §9.6's and not the
   default read path, so `[R-LIF-05]` does not reach it there; a violation
   latent in the state it leaves travels with it, and certifying that
   state is a verifier's office (§9.7).
3. **The verifier's half is unchanged.** A verifier that runs the probe and
   truncates nothing is doing diagnosis, as §9.6 says; a tool that does
   both is bound as each.
4. **Appendix H's updater entry** carries the operation in one sentence.

## Consequences

A recovery tool that truncates can claim conformance as an updater, and
rollback by truncation is a conduct violation of `[R-LIF-01]` by a tool
calling itself conforming, unwitnessed as `[R-LIF-04]`'s residue is. The
class count, the checklist count and the register are unchanged. What the
tool cannot claim is the conformance of the state it leaves: `[R-LIF-06]`'s
re-verification is §8's chain, and certification stays a verifier's
office, the shape §20.1 already gives an updater's carried-forward
structures. Readers gain nothing new: a reader meets the file the tool
leaves as the committed state it is.

## Alternatives rejected

- **A sixth class** (option (a)): the same obligations plus bookkeeping in
  §2.3's class count, Appendix H and the register's actor vocabulary, for
  a name ADR-0129's model already supplies through the updater class, as
  compaction's came through the rewriter.
- **Outside the classes** (option (c)): the cheapest, and the one option
  that leaves rollback by truncation unforbidden for a conforming tool,
  `[R-LIF-01]` binding writers only.

## Precedent

- **ADR-0129**: obligations attach to operations and bind whichever writer
  performs them; compaction one rewrite among several.
- **ADR-0017** (Q-A2): the mutability contract `[R-LIF-01]` states.
- **ADR-0115**: §21.7's unwitnessed test, under which `[R-LIF-09]` needs no
  row.
- **ADR-0133** decision 1: a decision against A on `main`, ported to B as
  a listed edit.
