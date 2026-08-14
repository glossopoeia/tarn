# Cleanroom round 8 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**G3 is not met. Two byte-level ambiguities survived, unanimously — and
both are in §20.4, the table round 7 repaired.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings | 33 — reader 4, writer 5, verifier 5, diagrams 6, register 6, adversary 4, quiz author 3 |
| Flagged byte-level by their reporter | 5 |
| Distinct defects after mechanical three-way dedup | **22** |
| **Byte-level, after triage** | **2 — unanimous across all three passes** |
| Consensus status | 14 CONFIRMED by all three · 5 mixed · 3 with a REFUTED among them |
| Severity (majority of the three passes) | 15 editorial · 5 register bookkeeping · 2 byte-level |

The acceptance criterion is *zero byte-level ambiguities outright*. Two is
not zero, and neither is a technicality: each forks what bytes a
conforming updater may emit from one input file and one instruction.

## The trend, stated plainly

| Round | Byte-level defects | Quiz |
|---|---|---|
| 4 | 4 | — |
| 5 | 3 | — |
| 6 | 5 | 14 / 1 diverge |
| 7 | **0** | 15 / 0 / 0 |
| **8** | **2** | **15 / 0 / 0** |

Round 7's zero did not survive contact with a second reading of the same
document. That is the result worth sitting with: the text round 7 declared
clean is, in the two respects below, not clean — and the defects are in
text round 7 itself wrote.

The quiz held at 15/15 with nothing underdetermined, two rounds running.
The two questions whose answer strings differed did so only in the letter
case of hex digits. Reporters self-flagged 5 findings byte-level and 2
survived — the first round in three where the survivor count is neither 0
nor a large over-claim, which is roughly what a calibrated reporter pool
should look like.

## The two that gate the round

**§20.4 directs an updater to commit against a file §7.2 obliges it to
reject.** The chain to *reject* is unbroken and every link is normative:
§2.3, *"Verifiers and updaters are readers of the files they process and
inherit every reader obligation"*; §20.3 step 2, *"Perform §19.1's open
— the appender is a reader here"*; §19.1 step 4, applying *"the
MUST_UNDERSTAND gate for unknown top-level types (`[R-CNT-15]`)"*;
`[R-CNT-15]`, *"An unknown record type at file scope: MU = 1 →
reject-file"*; §2.4, *"A reader MUST NOT rely on any structure in it."*
Against it, §20.4's MU = 1 row grants that *"a commit that only changes a
layer's own tiles, index, or record remains permitted."*

The obvious carve-out is not one. `[R-CNT-15]`'s closing sentence —
*"Updater obligations for unknown records are §20's subject"* — says where
the obligations live, not that the updater is relieved of reject-file. A
grep of every occurrence of *updater*, *appender* and *compactor* turns up
no carve-out, and the one place the document handles the analogous case it
goes the other way: §6.3, *"an updater encountering an unknown
incompat-lane bit is a reader first, and therefore rejects the file before
modifying anything."*

Two updaters, one generation-1 file carrying a top-level experimental-range
MU = 1 record, one instruction *supersede tile 1 of layer elev*. One emits
a payload, a re-emitted index region, a four-record directory, a pad and a
generation-2 trailer. The other emits nothing. Both results are conforming
files, so no verifier verdict and no reader outcome corrects the fork.

This is a propagation failure of round 7's own repair. Round 7 restored the
table's scope to *"a type the updater does not implement"* — correct for
the layer-scope half, since `[R-CNT-18]` makes an unknown MU = 1 sub-record
reject-*layer* and other layers stay editable. For the file-scope half, the
same scoping walks the row straight into `[R-CNT-15]`.

**§20.4's drop licence may or may not include layer records.** The MU = 0 /
PE = 0 row lets an appender drop an unknown record only in a commit that
*independently* changes *"the file's layer set or another top-level
record."* Whether a layer record is *another top-level record* decides
whether a routine tile update may destroy application state.

The literal reading says yes. `[R-CNT-13]` writes *"the layer for a layer
record and for sub-records, the file for **other** top-level records"* —
that *other* settles that a layer record is one. §7.3 scopes type 0x0001 to
*file*. And where the document means to exclude layer records it says so:
*"non-layer top-level record"* occurs 8 times, at F3, F4, F28, F29, F31 and
F33–F35, while §20.4's clause is unqualified. Since `[R-WRT-04]` makes
superseding a stored tile re-emit that layer's index region *"necessarily
at a new placement"*, every tile commit changes a layer record's extent
slot — so on the literal reading every tile commit licenses the drop, which
makes the first disjunct redundant and the row's own stated purpose
(*"Dropping the record is not itself such a change"*) nearly vacuous.

The narrow reading rests on the MU = 1 row of the same table, which glosses
file-scope structural change as *"adding, removing, or reordering top-level
records"* and contrasts it with *"a commit that only changes a layer's own
tiles, index, or record"*. That is an inference across rows about a
different obligation, in different vocabulary. Nothing decides it.

Both reporters picked the narrow reading and both said the literal one is
the more natural. That is the signature of a defect rather than a
preference.

**Both are now decided** ([ADR-0066](../../decisions/0066-round-eight-reopens-the-updater-table.md)):
the grant is deleted, and the drop licence is narrowed to a non-layer
record. What settled the first was not the citation chain but the
mechanism behind it — `[R-WRT-06]` bars a *compactor* from such a file
because *"its bytes cannot be safely relocated"*, and `[R-WRT-04]` makes
the very commit §20.4 permitted re-place the layer's index region. The
grant licensed the harm the compactor rule names.

## What else the round caught

**§20.3's example (c) invites a corrupting updater.** It listed *changing a
channel's fill value* among changes *"confined to the directory"*. For any
layer with a padding position or a pad bit, `[R-SER-05]` fixes the content
of those samples to the fill, so a directory-only fill change leaves every
edge tile in violation — on exactly the layers where fill matters most, the
ones with ragged edges. An updater author reading the example ships
`set_fill()` as a cheap metadata edit that silently produces files every
conforming verifier condemns tile by tile. Fixed.

**§15.3 told verifiers to over-count slack.** Its clause read that the walk's
slack total *"therefore includes whatever bytes such an entry nominally
addresses"* — but four of the six structural shapes are entries whose bytes
*do not exist*: length 0, offset past F − 64, an offset/length overflow. An
implementer reading it as an instruction adds `entry.length` to the counter
and reports totals larger than the file. Reworded to state the consequence
rather than an arithmetic instruction.

**The register's completeness claim was wider than the register.** Both
`[R-CNF-07]` and §21.1 claimed to cover every *detectable violation*, where
they mean every detectable *file-conformance* violation. An over-long
pre-trailer pad is a detectable violation of a named MUST that the register
omits by design — a counterexample to a normative claim, and enough to send
a verifier author building a check and a corpus author hunting a row that
does not exist. Qualified at all three sites.

**Appendix H's checklists drifted from the rules they cite.** The verifier
list reached 17 of the 20 verifier-detected rows, omitting F9, F39 and L26
— so a checklist-derived verifier accepts a reserved-range MU = 0 record
silently. The reader list repeated four of `[R-CNF-03]`'s five no-subset
clauses, dropping the user-metadata encodings. The writer list carried
`[R-CNT-03]`'s SHOULD undifferentiated among seven MUSTs, in a list whose
stated purpose is self-audit — the shape that produces a false negative
against a conforming writer, or a reviewer condemning a conforming file for
non-zero slack. All fixed.

## The three byte-level claims that did not survive, and why

Each was re-judged by three passes; I then re-read the decisive text myself
rather than accept the verdicts.

- **Whether a verifier may certify any file using filter 2 or codec 2/3/4.**
  The adversary built a 256-byte file whose writer shuffled at the wrong
  stride, and argued that since no verifier can check `[R-COD-10]` for it,
  §2.3's unscoped *"unable to check"* forces *cannot establish* — making
  *conforming* unreachable for most of the format. Refuted by `[R-COD-10]`'s
  own closing clause, quoted: a wrong stride with no padding or bool witness
  means *"the consequence is wrong sample content — undetectable by
  construction (§21.7)"*. The verifier is not unable to check a violation;
  there is no file-level violation to check. §21.7 names this exact pair of
  rules, and `[R-CNF-02]` supplies the general form — *"conduct rules bind
  the actor, the predicate binds the bytes."* The scoping gap the adversary
  identified was real and is now closed in the text.
- **Whether creation pins the first structure at offset 16.** Refuted:
  §21.6's own coverage row makes *alignment gaps* slack, and a layer
  declaring A = 4096 cannot place its first tile at 16 at all, so the
  creation sentence cannot mean what the reporter feared. Its wording is
  aligned with step 1's all the same.
- The remaining reporter flag reduced the same way: the rule states the
  verdict, so both implementations reach it.

## Two honest notes

**The triage passes were told the anchoring risk, and it did not silence
them.** All three received the 33:5 and 8:0 calibration together with an
explicit warning that two rounds of *"almost nothing survives"* biases a
judge toward downgrading, and a rule that a downgrade without a quotation
is not a judgement. All three then upheld both survivors, and the skeptic
— whose lens is to assume the finding is wrong — recorded one of them as
*"the group I tried hardest to kill and failed"*. That is the first round
whose byte-level verdict was not reached under an unmitigated prior.

**Every coverage claim checked out this round — the first time.** Rounds 6
and 7 each had a triage-stage agent overstate its own coverage. This round
all three passes echoed the complete 33-id input list, and the union of
each pass's groups equalled it exactly, with no duplicates and no drops.
Verified mechanically by union-find over the three groupings and a set
difference on ids, not by taking any pass's word. Worth noting that the
three passes reported 24, 24 and 23 groups and the merge is 22: three
passes agreeing on a count is not agreement on a partition, and only the
id-level merge shows it.

One disclosed deviation, recorded because it strengthens the round: the
adversary built a TARN writer and a TARN verifier from Part I and Part II
alone, emitted three files with them, and mechanically re-derived §21's
totals from the register tables — 39 + 50 + 26 + 10 = 125 conditions over
61 + 102 + 45 + 44 = 252 instances, matching §21.8. Three other agents
independently reproduced CRC-32C constants `E3069283`, `00000000`,
`EECB3BB2` and Appendix A's trailer CRC `E00938D2` from §4.5's stated
parameters. Each read only files it had itself written.

## Disposition

All 22 defects are dispositioned: **16 fixed, 3 escalated, 2 deferred, 1
judged to need no change.**

**Fixed — 23 edits, zero anchor misses.** Applied one at a time with a
write after each and an ok/MISS line per anchor. The two byte-level
defects were decided by the maintainer and are recorded in
[ADR-0066](../../decisions/0066-round-eight-reopens-the-updater-table.md).

| Defect | Where | Repair |
|---|---|---|
| `wrt08-mu1-file-scope-grant` **(byte-level)** | §20.4, Appendix H | the file-scope grant is deleted: an unimplemented top-level MU = 1 record leaves an updater no commit at all, as §6.3 already says for an unknown incompat-lane bit |
| `wrt08-pe0-drop-licence` **(byte-level)** | §20.4 | "another **non-layer** top-level record", with the tile-supersede case named |
| `cnf11-unable-to-check-unscoped` | §2.3, §21.7, Appendix H | *cannot establish* scoped to a capability or resource ground, at the verdict clause and the report clause; §21.7 states that a requirement with no file-level witness is not one a verifier is "unable to check" |
| `s203-example-c-fill` | §20.3 | fill change is directory-only only on a layer with no padding position and no pad bit |
| `s153-slack-over-count` | §15.3 | states the consequence, not an arithmetic instruction |
| `s97-structural-ground` | §9.7 | the missing "on a *structural* ground" carried into the closing sentence |
| `s97-omits-sub-records` | §9.7 | the claimant enumeration names sub-records |
| `register-completeness-unqualified` | §2.4, §21.1 ×2 | "detectable **file-conformance** violation" at all three sites |
| `f36-at-open` | §21.2 F36 | "each at its own tier" replaces "at open" |
| `enc12-no-quarantine-carve-out` | §4.6 | `[R-ENC-12]` gains the carve-out `[R-ENC-11]` already carries |
| `appendix-h-verifier-omits-f9-f39-l26` | Appendix H | three clauses added |
| `appendix-h-reader-drops-encodings` | Appendix H | "and both user-metadata encodings" |
| `appendix-h-writer-flattens-should` | Appendix H | the SHOULD moved to its own advisory line |
| `preserve-verbatim-unbound` | §2.4 | bound to §20.4's rows |
| `s74-no-class-column` | §4.7 | the Note softened to match what §7.4 delivers; the column itself was refused in round 7 as normative drift and is refused again |
| `creation-offset-16` | §9.2 | wording aligned with step 1; substantively refuted |

**Escalated — three maintainer decisions still open.** F21's registration
against §21.6's account of the same condition; L2's collapsed instance
arithmetic; and whether `[R-ENC-06]` gains a tile-scope cause row. All
three move §21.8's totals and the corpus, so none was applied
unilaterally. The two byte-level defects were also escalated and have been
decided — see ADR-0066 and the *Fixed* table above.

**Deferred, with owners.** §21.9's hard-limit list omits the alignment
bounds and the 128-byte floor, and `[R-VEC-03]` binds corpus construction
to that enumeration — a short list is a short corpus. Appendix G's
reproducible-writer profile fixes emission order but not gap extent,
sub-record order, or the fill default, so two profile-conforming writers
can still differ. Both want a decision about what the document should
require, not an edit.

**No change.** L24's name instance is due at layer access while L4/L6/L7
place the same field's checks at open. A reader that runs L4/L6/L7 at open
has already established L24's name instance, so nothing is wrong; the
asymmetry is recorded rather than repaired, because repairing it means
revisiting four rows to gain uniformity and no correctness.

## Artifacts

- [prompt.md](prompt.md) — charters, access rule, taxonomy, pass criteria
- `transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`
  — the three implementer walks
- `transcript-diagrams.md` — the figure audit
- `transcript-register.md` — §21 against the rules it restates
- `transcript-adversary.md` — attacks tried, and which the text refutes
- [transcript-quiz.md](transcript-quiz.md) — the adjudication, over
  `transcript-quiz-author.md`, `transcript-quiz-answers.md` and
  `transcript-quiz-key.md`
- `transcript-triage-correctness.md`, `transcript-triage-implementer.md`,
  `transcript-triage-skeptic.md` — the three blind triage passes
