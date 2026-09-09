# Cleanroom round 35 — refute-phase verdicts

The workflow's own log line is the record of what fired:

    refute phase: 0 unanimous downgrade(s), 0 split verdict(s), 1 unanimous uphold(s); byte-level upheld anywhere: true

One shape, one refuter. No reporter flagged a finding byte-level, so
neither the downgrade-refuters nor the split-refuters had a target, and the
zero-trigger was suppressed by the one group all three passes upheld
byte-level against both of its reporters' own grading. That group got the
uphold-refuter. Configured on Opus, the refuter was refused at zero tokens
with `[reasoning_extraction]` at launch and again on the unchanged resume,
which replayed every cached result in six seconds; it ran on Sonnet after
that one call's model was changed without rewording, and returned in six
minutes. Its verdict was hand-checked in both directions before the round's
verdict rested on it; `findings.md` carries the hand-check.

## `compactor-copies-vs-relocated` — unanimous byte-level uphold

**Refuter (Sonnet, after two Opus refusals): UPHOLD_STANDS.** Brief: find
the sentence that decides the finding against the reporters. Sections
opened: §2.3's role definitions with `[R-CNF-11]` whole; §8.1's coverage
map and §8.2's chain of trust; §19.2 through §19.4; §20.1, §20.2 and §20.3
with `[R-WRT-03]`; §20.3's three shapes and §20.4's opening and table; the
whole of §20.5 with its figure; R1 through R3; the closing checklists.

The fork it tested: whether `[R-WRT-09]`'s duty reaches a top-level,
PE = 1 user-metadata extent a compactor copies to its input offset with a
bad terminal CRC. Under the enumeration reading the duty names *each
relocated extent's checksum* and the check never fires, so the compactor
emits the file; under the premise reading, *it relies structurally on every
structure it copies*, the check fires, fails, and §20.5's refusal is
mandatory. Its candidate closers, each pushed and found not to reach:

- §8.2's chain of trust, which gives a user-metadata extent's CRC a
  separate outcome outside the chain, and so is evidence that *the chain*
  excludes such extents as a term of art; but `[R-WRT-09]`'s own list
  already departs from §8.2's chain, naming the open and each retained
  layer's record, so it restates a looser concept whose completeness is the
  very question.
- `[R-WRT-03]`, the appender's reliance rule, which gates the duty to
  structures the commit modifies or reuses and says the rest *impose no
  further obligation*; `[R-WRT-09]` opens by contrasting itself with that
  rule, *reliance over everything it carries*, which reads as a deliberate
  widening and cuts toward the fork being real.
- `[R-WRT-07]`'s restatement, which narrows only within the tile and index
  domain and says nothing of a non-tile extent the output does not move.
- `[R-RDR-02]`'s *before anything the extent holds is returned*, which
  `[R-WRT-09]` does not invoke, stating its own emission-timed trigger
  instead.

It also checked verifier-02's own downgrade ground, that `[R-CNF-05]` bars
the output under both readings, and found it contradicted by `[R-WRT-01]`
(*a violation latent in a structure they carry forward unmodified travels
with it, seen or unseen*) and by §20.5's conditional *Given a conforming
input the output is a conforming file*.

**Hand-check verdict: UPHOLD STANDS.** The driver's own search reached the
same sentences and one more, §20.5's *free to place structures anywhere
§5.2 admits*, which is what makes a placement that relocates nothing
available and so gives *relocated* a non-empty complement. The
construction was checked by hand: input I with a user-metadata extent whose
terminal CRC fails (R2), a PE = 1 record no table licenses dropping, a
stored tile and its index, no interior slack; a compactor that keeps every
structure at its input offset verifies the open, the layer record, the index
chain and the tile's entry crc, and under the enumeration reading never
reads the extent's CRC, detects nothing, and emits output O under a fresh
file_id, while under the premise reading it MUST refuse. O is a byte
sequence a conforming compactor may emit under one reading and none may
under the other, and the discriminating test's usual escape, that the
output is nonconforming anyway, is closed for a compactor by `[R-WRT-01]`
in terms. No sentence decides it; three formulations exist and no two
agree. It is new: the ledger's Q-C10 asks the neighbouring question, an
index entry's value-domain classification, and names `[R-WRT-09]` only as
the depth bound. It sits in §20.5, text this round was not chartered to
read.
