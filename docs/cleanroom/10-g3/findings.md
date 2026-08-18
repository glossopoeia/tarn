# Cleanroom round 10 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**One byte-level ambiguity, in a clause ADR-0066 wrote. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 44 — reader 7, writer 7, verifier 4, diagrams 8, register 4, adversary 7, quiz 7 |
| Flagged byte-level by their reporter | 7 |
| Distinct defects | **27** |
| **Byte-level, after triage and hand-check** | **1** |
| Severity | 18 editorial · 4 register bookkeeping · 3 design decision · 1 byte-level · 1 figure |

## The trend

| Round | Byte-level | Quiz |
|---|---|---|
| 7 | 0 | 15 / 0 / 0 |
| 8 | 2 | 15 / 0 / 0 |
| 9 | 0 | 15 / 0 / 0 |
| **10** | **1** | **15 / 0 / 0** |

Four rounds running with no question either quiz agent judged
underdetermined. Four rounds running in which the defect found was in the
previous round's repair.

## The survivor

§20.4's MU = 0 / PE = 0 row lets an appender drop an unknown record only in
a commit that *independently* changes the scope the record attaches to,
enumerating two branches and closing with an em-dash caveat: *"a commit that
only supersedes a layer's tiles is not such a change, though it re-places
that layer's index region."*

The caveat can attach to the top-level branch alone or to the whole
enumeration. Narrowly, superseding a tile changes *"that layer's … stored
tiles"* and licenses dropping that layer's unknown sub-record; globally, it
never does. Two appenders given the same file and the same instruction —
supersede one tile of a layer carrying an unknown MU = 0 / PE = 0 sub-record
— emit directories differing by the record, its `inline_length`, `dir_length`,
the directory CRC, the pad and the trailer, with the extent falling to slack
in one. Both outputs conform; exactly one appender does.

Two reporters reached the narrow reading independently. Two of three triage
passes upheld it as byte-level. The skeptic downgraded on the ground that the
following sentence reuses *"such a change"* with a global antecedent — a real
argument, and one that shows the global reading is *available* rather than
that the embedded clause is unambiguous. The drafting intent covered neither
branch: the caveat was added to stop a tile commit licensing the drop of a
*top-level* ancillary, and the sub-record branch was never considered. A
clause whose author's intent does not reach the case a competent reader hits
is the definition of the defect this gate tests for.

Decided global, in [ADR-0070](../../decisions/0070-a-supersede-only-commit-drops-nothing.md).

## The candidate that did not survive

`[R-CNT-04]`'s residency gloss leads with *"a local file"* — a transport
classification, in a paragraph that twice says the test is residency and not
transport. Round 9 found this and deferred it as editorial; round 10's reader
argued it to byte-level, on the ground that a pread-only local reader is
classified both ways and the two readings fork accept against reject on a
file with a damaged front block.

It is decided, by the rule's own closing sentence — *"The test is residency,
not transport, so an implementation decides it at its own open path"* — and
by **Appendix A applying it**: *"bytes [0, 16) stay non-resident, so §6.1
leaves the front-block check to the reader."* The document's own worked
example uses literal residency. Not byte-level; the gloss is repaired anyway,
having now cost two rounds' attention.

## The guard held

Round 9's most valuable result was a process failure: a walk wrote eight
findings into its transcript and returned one, with its disclosure field
reading `test`, and nothing in the pipeline could see it. This round every
walk reported `transcript_finding_count`, checked mechanically against the
returned array and against the transcript on disk. **All six agreed** — and
the diagram auditor, the walk that failed last round, returned 8 of 8. Every
triage pass echoed the complete 44-id input and its groups unioned to it
exactly, with no duplicates and no drops.

## What else the round caught

Three defects are consequences of the two preceding ADRs, which is the
pattern this gate keeps producing. **`[R-ENC-06]` had no register row and no
exemption** — ADR-0069 retired its rows and left §21.7, the account of what
escapes the register, not saying so. **ADR-0068's summary omitted the
layer-scope user-metadata sub-record**, in §20.4 and again in Appendix H.
**§18.4 cited §21.7 for a ground §21.7 does not state.**

Beyond those: §21.8 called a row's outcome a *verdict*, a closed three-value
term that contains no outcome; T15 and T16 lacked the cause-row annotation
T13 and T26 carry; L22's Instances cell named three fields its equality never
reads; `[R-MTA-09]`'s decline was unscoped; Appendix G's zeroing reached only
gaps a *declared* alignment forces, leaving the pre-trailer pad free; and the
front matter claimed conformance checklists cite identifiers and never prose
positions, which Appendix H contradicts throughout.

## Disposition

All 27 dispositioned: **13 fixed** (13 edits, zero anchor misses), **6
deferred as maintainer decisions**, **8 carried to round 11 as editorial**.

Register and corpus unchanged at **121 conditions over 248 instances, 300
vectors** — L22's relabelling kept its count at three and re-annotated its
three existing vectors, which already built the three alternatives.

**All six decisions are settled in
[ADR-0071](../../decisions/0071-six-decisions-round-ten-raised.md).** The
taxonomy's `structural` class is broadened to the sense `[R-CNT-07]`,
`[R-MTA-02]` and `[R-SEC-06]` already use, leaving `fill` the only semantic
field and `version_minor` the only descriptive one. The partial slack total
becomes an upper bound — F less what the walk enumerated — amending ADR-0065,
since only 12 of 522 slack bytes were provably claimant-free in the worked
case. §20.3 gains the appender's counterpart in the *proceed* direction, on
`[R-WRT-05]`'s distinguisher that a record it **modifies** is new output;
§20.5's third justification is trimmed, the same reasoning cutting against it.
`[R-ERR-03]` becomes a finding aid rather than an inventory. **COV-06** now
asserts a vector's recorded rule is its row's governing rule, closing the
row-label drift COV-05 is blind to on the 50 rows sharing the instance `—`.
And `[R-VEC-04]`'s pair is qualified to reader-detected rows.

Working those up found **seven vectors that would fail a correct
implementation**, all repaired: TV-0226 and TV-0950 asserted a reader must
refuse on a verifier-detected row (`L()` hard-coded it), and TV-0400, TV-0407,
TV-0408, TV-0409 and TV-0410 recorded expected content from the seed while
their own patches re-declared the layer.

## Artifacts

`transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`,
`transcript-diagrams.md`, `transcript-register.md`, `transcript-adversary.md`,
the three quiz transcripts, and the three blind triage passes.
