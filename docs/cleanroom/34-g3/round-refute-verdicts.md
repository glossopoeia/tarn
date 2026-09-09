# Cleanroom round 34 — refute-phase verdicts

The workflow's own log lines are the record of what fired:

    refute phase: 0 unanimous downgrade(s), 0 split verdict(s), 0 unanimous uphold(s); byte-level upheld anywhere: false
    REFUTE FIRED ON A ZERO: no reporter flag and no pass upheld one, so the phase selects by subject instead. 21 group(s) available, attacking 7

No reporter flagged a finding byte-level, no pass upheld one, and no verdict
split, so neither the downgrade-refuters, the split-refuters nor the
uphold-refuters had a target. The phase fired on the zero, as it has since
round 29: seven groups chosen by subject, each attacked by a Sonnet refuter
told to find a construction on which the disputed file is conforming and only
one reading lets a conforming actor produce it, and one round-wide attacker
told to find the byte-level question the round did not ask. The fourteen
groups the cap left unattacked are named in the log line and in
`findings.md`; every one of them is hand-checked there.

The round-wide attacker, configured on Opus, was refused at zero tokens with
`[reasoning_extraction]` at launch and again on the unchanged resume, the
first time this call has been refused; it ran on Sonnet after that one call's
model was changed without rewording, in nine minutes. Every verdict below is
in the direction that clears the gate, so every one was hand-checked before
the round's verdict rested on it: the driver read the sentences each refuter
quoted, opened the paragraph above each, and looked for the construction the
refuter did not find.

## The seven targeted attacks — all DOWNGRADE_STANDS

### `slab-verb-re-established-vs-kept` — reader-01, adversary-01, quiz-01

**Refuter: DOWNGRADE_STANDS.** Opened §20.3 step 4 whole, §16 in full,
§11.1's Rationale, §11.4, §20.4, Appendix H, §7.4's field rows. Enumerated
the transitions a declaration's value can make, found the some-to-same case
the step's own default, and built the hardest construction against the
premise: a slab-declared layer whose extent growth renumbers ordinals under
`[R-GEO-06]`. `[R-SLB-04]`'s trigger list fires on *the disk ordinal of any
tile the new state stores* whatever the member's verb says, and its two
discharges are the same under either reading.

**Hand-check: STANDS.** The member's verb names nothing `[R-SLB-04]` reads;
every transition is named or defaulted; the emittable set is fixed by
`[R-SLB-01]`, `[R-SLB-03]` and `[R-CNF-05]`. A wording defect in chartered
text, repaired under ADR-0127.

### `both-sides-and-reach-claim` — writer-04, adversary-02

**Refuter: DOWNGRADE_STANDS.** Opened §20.3 whole, §7.4, §11.1, §11.2.
Confirmed the premise (a dimension extent Eᵢ is on the permitted side only;
the fixed list's *every tile extent* is Tᵢ) and tried three constructions,
each failing because *an extent MAY grow, and MUST NOT shrink* states the
whole rule for Eᵢ under either reading of *both sides*, and the trailing
clause states the rule for the four fields the lists miss.

**Hand-check: STANDS.** The fixed list opens *Every other declaration*, the
permitted list's complement by construction. Repaired: the example is
dropped.

### `structural-descriptive-actor-sets` — verifier-01, adversary-04

**Refuter: DOWNGRADE_STANDS.** Opened §4.7, §1's Note, §7.2, §7.3, §4.5, §6.3,
and every occurrence of *structural* and *descriptive*. Both witnesses
(reserved flag bits, a registered type's stored MU and PE bits) are
nonconforming under `[R-CNT-12]` and `[R-CNT-22]` whatever the class label,
and `[R-ENC-16]` is cited by no register row.

**Hand-check: STANDS.** `[R-ENC-16]`'s closing sentence assigns every field of
format major 1 by name. Repaired: the descriptive clause names both actors.

### `bar-classified-no-condition-vs-unwitnessed` — reader-02, writer-02

**Refuter: DOWNGRADE_STANDS.** Opened §2.2 through §2.5, §5, §9, §18.2, §20.3
step 4, §21.1, §21.4, §21.6, §21.7, §21.8. Three grounds: the sentence names
its own class; both §21.7 classes yield no row; `[R-CNF-02]` names the bar
outright. Tried writer-02's witness, a single-commit file whose slack mimics a
prior generation, and found it a file a creator may write under either
classification, slack content being unconstrained.

**Hand-check: STANDS.** The bar's subject is a commit's event; the live
state, which is what file conformance is a predicate over, carries no record
of it, and a superseded directory in slack is content `[R-CNT-21]` leaves
unconstrained. §18.2 uses the class on the same actor-bound ground. Declined.

### `http-vocabulary-unpinned` — adversary-06

**Refuter: DOWNGRADE_STANDS.** Opened §2.1, §2.3, §6.4, §7.1, §7.2, §19.1,
§21.1, §21.2 (F17), Appendix F. `[R-CNT-10]` binds a remote reader's
transport conduct, defines the transport-authoritative size in its own
parenthetical, and no register row's firing depends on the vocabulary.

**Hand-check: STANDS.** No byte on disk and no verdict turns on it. Repaired
as a reference: Appendix F lists RFC 9110, a decision the maintainer can
reverse.

### `f5-pad-in-floor-derivation` — diagrams-04

**Refuter: DOWNGRADE_STANDS.** Opened §5.1, §6.2, §21.1, F5, §21.9's
hard-limits restatement. The pad's minimum is zero (`[R-CNT-05]`), so a
four-component reading still derives 128; F5's predicate reads F alone; §21.1
makes the rule govern the row.

**Hand-check: STANDS.** The reporter's own 128-byte witness with no pad is a
conforming file. Repaired: the cell lists the three components the rule does.

### `decoded-size-parenthetical-omits-l44` — adversary-05

**Refuter: DOWNGRADE_STANDS.** Opened §20.3 step 4 whole, §21.1 through
§21.6 for the rows named, §21.7, §21.9. The parenthetical's subject is the
reinterpretation of stored bytes; L44 reads declarations alone and fires on an
empty layer; the bounds paragraph two paragraphs later names L44 for every
permitted change; the reporter's re-tiling is a rewrite, outside the
paragraph.

**Hand-check: STANDS.** Two passes held the text decided it; repaired for its
wording with two words, *a stored tile's*.

## The round-wide attacker — DOWNGRADE_STANDS

**Refuter (Sonnet, after two Opus refusals): DOWNGRADE_STANDS**, with the
account the brief demands. It read the document end to end, re-derived five
CRC constants from its own table (the §4.5 check vector, `[R-IDX-05]`'s
all-sentinel constant, the §7.4 example's segment CRC and crc_of_crc_array,
Appendix A's trailer CRC) and reproduced every one, closing the one avenue on
which a writer's licence and a verifier's arithmetic could have diverged
mechanically. Its one textual candidate it carried to bytes: Appendix A's
file with the front-block magic's first byte flipped, which a reader holding
bytes [0, 16) resident rejects at open (F6) and a reader that never fetches
them serves forever. It killed the candidate itself, on `[R-CNT-04]`'s own
words and their restatement in F1's Condition cell, F6, Appendix A and
Appendix H: a divergence the document licenses in the requirement's own text
is not a question the document leaves open. Three narrower candidates were
closed on the text: the six experimental ranges §10.3 carves out as validity
errors, an empty layer's extent slot (forced to (0, 0) by L22 and L15), and
the trailer's unordered second batch of gates (every member reject-file).

**Hand-check: STANDS.** The residency asymmetry is a designed licence, stated
at four sites and carried by F1's own row, not two readings of one sentence;
the driver's search of the chartered passages found no sentence admitting two
readings that reach a byte, and the seven groups above are the nearest the
round came. No flag survives; none was raised.
