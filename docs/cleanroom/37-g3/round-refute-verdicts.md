# Cleanroom round 37 — refute-phase verdicts

The workflow's own log lines are the record of what fired:

    6 findings from 6 walks + quiz author; 0 self-flagged byte-level
    refute phase: 0 unanimous downgrade(s), 0 split verdict(s), 0 unanimous uphold(s); byte-level upheld anywhere: false
    REFUTE FIRED ON A ZERO: no reporter flag and no pass upheld one, so the phase selects by subject instead. 6 group(s) available, attacking 6: trailer-flags-cell-actor-list, single-channel-layout-confirmed-unwitnessed, appender-rewriter-narrowing-confirmed, diagrams-bracket-overrun, layer-drop-mu1-row-label-scoping, r-wrt-06-missing-conduct-only-disclaimer
    round-wide zero attack: DOWNGRADE_STANDS

No reporter flagged a finding byte-level and no pass upheld one, so the
zero-trigger fired, as it has on every zero since round 29: six targeted
refuters, one per group (the cap of ten left none unattacked), and a
round-wide attacker told to find the fork the round had not asked about.
Every call ran on Sonnet, as every lane of this round did; none was refused,
none stalled, and each returned at its first attempt in three to six
minutes. **Every refute call answered in its own vocabulary this round**: the
per-call verdict enum round 36 owed (`DOWNGRADE_STANDS | DOWNGRADE_REFUTED |
UNDECIDED` for the targeted refuters and the attacker) held, and the
round-wide attacker's `DOWNGRADE_STANDS` is the label the brief asked for.
All seven verdicts are in the direction that clears the gate, so all seven
are provisional on the hand-check `findings.md` carries.

## The round-wide attacker — `DOWNGRADE_STANDS`, with its account

It read the document whole, front to back, and stayed off the six groups'
ground on purpose. It carried three constructions to numbers and walked six
more areas without finding daylight between two readings:

1. **The index-region formula at segment boundaries.** `extent_length =
   entry_count · 20 + ⌈entry_count / 2¹⁶⌉ · 4` at entry_count 0, 65,535,
   65,536, 65,537, 131,072 and 131,073: one segment and 1,310,724 bytes at
   65,536, two segments and 1,310,748 at 65,537, three at 131,073, none at 0;
   §15.4's worked example at 1,000,000 entries (16 segments, a 64-byte CRC
   array) reproduced by the same formula. Two ceiling implementations agree
   at every seam; no off-by-one lets one reader accept a boundary
   entry_count another rejects.
2. **The sentinel and crc combinations.** §15.2 and §15.3's three rows
   partition every pattern of which of offset and length equal the sentinel,
   and T6 through T12 cover the remaining value-domain and bounds failures;
   no fourth combination is left unrouted.
3. **`[R-ENC-04]`'s designation carve-out.** It looked for a sum used only
   inside a comparison, undesignated, whose overflow two readers could treat
   differently, and tried §14.2's channel offset and sample stride; §14.2
   designates them expressly, and at the declared ceilings the stride's
   maximum is 524,280, nowhere near 2⁶³ − 1.

The areas walked without a fork: the extent-slot cross-checks against
entry_count (§7.2, §7.4, `[R-CNT-13]`, `[R-CNT-17]`, L15, L21, L22); the
alignment and slab limits at every stated boundary (L20, L28, L29, L39, L41,
L42); step 4's two lists, which bind the committing actor under `[R-CNF-02]`
and so cannot fork a file's conformance; `[R-WRT-07]`'s regeneration rule
for a moved entry; the codec framing rows T15 through T25; and the worked
numeric examples. *"None produced a case where two spec-faithful
implementations must emit different bytes or reach different accept/reject
verdicts on the same file."*

## The six targeted refuters — all `DOWNGRADE_STANDS`

Each was told to overturn the passes' reading that its group is not
byte-level, by building a conforming file two readings treat differently.

- **`trailer-flags-cell-actor-list`** (diagrams-02; §6.2's flags cell,
  *"by an updater, appender or rewriter alike"*). Tried a third, bare
  updater the coordinate reading might bind differently: `[R-LIF-01]` closes
  mutation to a commit or a rewrite and `[R-CNF-06]` closes the class to the
  two tiers, so no such actor exists. Tried the cell's own force: it carries
  no keyword and forward-references §6.3, where `[R-CNT-08]` states the rule
  unconditionally and in the appositive form the passes named. Tried a
  disjunctive-permission reading: vacuous for the same reason. Stands.
- **`appender-rewriter-narrowing-confirmed`** (adversary-03; §20.4's last
  row). Tried reading the appender's dash-set clause, *one whose only effect
  is the drop included*, as a restriction to solo-drop commits, so that a
  combined commit would be barred where a combined rewrite is not. It fails
  on the word *included*, an appositive with no *only if*, and on §20.5's
  *"A rewrite MAY do several of these at once"*, which is why the rewriter's
  clause needs no such rider. Confirmed the narrowing exhaustive on
  `[R-CNF-06]` and §20.1, and the creator outside the table by definition,
  having nothing to retain or drop. Stands.
- **`diagrams-bracket-overrun`** (diagrams-01; figures (a) and (b) of the
  three-shapes Example). Grepped every *figure* and *diagram* in the
  document and found each descriptive, none binding; `[R-CNF-01]`'s
  exemption is closed and carves no diagram out of an Example; step 4's
  prose states the rule whole without the figure. §5.1's figure, whose
  brackets sit divider to divider, is itself labelled illustrative. Stands.
- **`layer-drop-mu1-row-label-scoping`** (adversary-02; §20.4's blocking
  sentence against an implemented MU = 1 sub-record). Built the fork the
  finding gestures at: an experimental-range sub-record type the updater
  implements, MU = 1 and PE = 0, dropped with its layer under the lead-in's
  reading and blocked under a literal reading of the row label. Then found
  the implemented/unimplemented qualifier stated five times: the lead-in,
  the blocking sentence itself (*"a sub-record of a type the updater does
  not implement with MU = 1"*), §7.2's Note, §20.5's *"An MU = 1 type it
  does implement is the remaining case"*, and Appendix H's *unknown critical
  sub-record*; and *the table's first row* and *MU = 1 row* each occur once,
  inside the span that carries the qualifier. The literal reading is not
  available from the document. Stands; the row label is, on its own,
  underspecified as writing, which is an editorial remark and not a fork.
- **`single-channel-layout-confirmed-unwitnessed`** (adversary-04; step 4's
  bar at C = 1). Tried a downstream exploitation, a later commit using the
  illegitimately reached layout: file conformance is a predicate on the live
  state alone, the superseded declaration is slack under `[R-CNT-21]`, and
  Appendix D says there is no generation attribution to certify. Tried
  generation comparison as a detectable-in-principle check: §21.7 puts the
  bar in the class that states no condition a file can exhibit, not among
  the unwitnessed. Stands.
- **`r-wrt-06-missing-conduct-only-disclaimer`** (adversary-01; §20.5's
  refusal on an unimplemented MU = 1 record). Asked the right question: is
  there a file a rule-breaking rewriter could produce that no conforming
  creator could? None: §20.1 has a creator answer for every byte of its
  output, *bytes it copied from another file included*, §20.2 bars it from
  no opaque record extent, and §7.2 defines no reference for an
  unimplemented MU = 1 type that this specification's predicate could
  examine. The identical byte sequence is emittable by a creator, so the
  emittable set does not move, and no verifier can tell the two producers
  apart. Stands; what remains is whether `[R-CNF-02]`'s list of stated
  conduct cases should name it, which is `findings.md`'s to raise.

The hand-check of each is in `findings.md`; none was overturned.
