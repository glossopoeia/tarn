# Cleanroom round 36 — refute-phase verdicts

The workflow's own log lines are the record of what fired:

    8 findings from 6 walks + quiz author; 0 self-flagged byte-level
    refute phase: 0 unanimous downgrade(s), 0 split verdict(s), 0 unanimous uphold(s); byte-level upheld anywhere: false
    REFUTE FIRED ON A ZERO: no reporter flag and no pass upheld one, so the phase selects by subject instead. 8 group(s) available, attacking 7
    NOT ATTACKED (zero-trigger cap 7): pe0-updater-commit-clause-loose
    round-wide zero attack: UPHOLD_STANDS

No reporter flagged a finding byte-level and no pass upheld one, so the
zero-trigger fired, as it has on every zero since round 29: seven targeted
refuters on seven of the eight groups, and a round-wide attacker told to find
the fork the round had not asked about. Every call ran on Sonnet, as every
lane of this round did (the maintainer's instruction of 2026-09-21); none was
refused. All eight verdicts are in the direction that clears the gate, so all
eight are provisional on the hand-check `findings.md` carries, and the one
group the cap left unattacked was checked by hand alone.

## The round-wide attacker — the zero stands, under the wrong label

**Verdict as returned: `UPHOLD_STANDS`. Verdict in substance:
`DOWNGRADE_STANDS`.** The brief told it to return `DOWNGRADE_REFUTED` with a
construction if it found a fork and `DOWNGRADE_STANDS` with an account if it
found none. It returned a label from the uphold-refuter's half of the enum,
and its reasoning leaves no doubt which it meant: *"none produced a case where
two spec-faithful implementations must emit different bytes or reach different
accept/reject verdicts on the same file"* and *"the round's zero-finding
conclusion stands"*. The label is recorded as a defect of the return, not read
as a finding; the account is what the hand-check reads.

It read the document whole and carried four constructions to arithmetic:

1. **The 128-byte floor against a file declaring another format major.**
   §19.1 step 1 makes F below 128 a validity error *"decided from F alone and
   needing no other byte of the file"*, before the trailer that declares the
   major is read; `[R-CNF-13]` says F5 *"does not reach"* such a file. It
   closed the construction two ways: no reader under this text implements
   another major, so `[R-CNT-07]` refuses the file whichever check fires
   first and the accepted set does not move; and the front block and trailer
   are both `[R-CNT-24]` constants that overlap for every F below 80, which
   removes most of the region. What is left is which diagnostic a reader
   gives, a SHOULD.
2. **A planar channel list shortened from its end under a slab declaration**:
   disk ordinals of the retained channels do not move, and the slab clause
   ranges over the new state.
3. **The segment and `extent_length` arithmetic at the 2¹⁶ boundary**: the
   ceiling formula and `[R-CNT-17]` agree at 65,535, 65,536 and 65,537
   entries.
4. **Nesting depth beyond two against L26**: a nested layer record is L26's
   before any depth rule can fire, and no other type can nest.

## The seven targeted refuters — all `DOWNGRADE_STANDS`

Each was told to overturn the passes' reading that its group is not
byte-level, by building a conforming file two readings treat differently.

- **`both-sides-sentence-imprecise`** (reader-01). Confirmed the premise: the
  permitted list names the planar channel list literally and reaches the
  interleaved one only through *its dimension and channel names*; the fixed
  list names the interleaved one and reaches the planar one only through *the
  position of every planar channel the new state keeps*. Tried every commit on
  either kind of channel list under the face-value reading and the
  cross-checked one; both classify each the same way, because the two lists
  themselves decide and the summarizing sentence adds nothing to them.
- **`appender-rewriter-mu1-asymmetry-unexplained`** (reader-02). Tried a
  commit growing an editable layer beside a blocked one, a commit dropping the
  blocked layer, and a rewrite of the same file. `[R-LIF-01]`'s append-only
  protocol keeps the first from touching the blocked layer's bytes whatever
  rationale is nearby; the row's *"its drop included"* decides the second;
  `[R-WRT-06]` decides the third. The missing sentence is an explanation, and
  no actor's bytes turn on it.
- **`verifier-decode-note-overstated`** (writer-01). The Note is labelled, so
  `[R-CNF-01]` takes its force away; looked for any normative sentence that
  defers to it and found none; §9.7, `[R-CNF-03]` and `[R-COD-11]` fix a
  certifying verifier's decode duty on their own.
- **`conformance-vector-total-unverified`** (verifier-01). Four constructions,
  one ground: `[R-CNF-02]`'s conforming-file predicate is stated over the
  rows' conditions and nowhere reads §21.8's total, and §24 makes the corpus
  derivative, so no file's status turns on whether the figure is 277.
- **`crc-fail-transparency-already-stated`** (verifier-02). Found the rule
  stated three times in terms, §16.2, §15.3 and row L41, so the second reading
  the finding worries about is one the text forecloses.
- **`figure-b-unclosed-bracket`** (diagrams-01). Confirmed the typo at byte
  level: the first annotation closes with `┘` and the second does not. The
  figure sits in a labelled Example; step 4's re-emission clause names what is
  re-emitted without it.
- **`unlabeled-normative-blockquote-15-1`** (adversary-01). Confirmed the
  block carries no label and is therefore normative under `[R-CNF-01]`, and
  that every fact inside it is pinned again in unquoted prose by `[R-IDX-01]`
  and `[R-CNT-17]`, so crediting or skipping the block yields one layout.

## Not attacked — the cap

`pe0-updater-commit-clause-loose` (adversary-02) was the eighth group and the
cap is seven. `findings.md` carries its hand-check.
