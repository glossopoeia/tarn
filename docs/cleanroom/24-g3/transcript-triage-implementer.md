# Round 24 triage — implementer-consequence pass

## What I read

Only `spec/tarn.md` (whole file, in sections, via `sed`/`grep`). I opened **no**
walk transcript and **no** `transcript-triage-*.md`. I did not list the round24
directory; I only `mkdir -p`'d it to write this file. I read no `docs/`, no
`PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web.

Sections read in full or in relevant part: §2.3, §2.4, §2.5, §4.7, §5.1, §5.2,
§6.1(via map), §6.2, §6.3, §7.2, §7.4, §8.1, §8.2, §9.1, §9.2, §9.3, §9.7,
§11.4, §14.2, §14.3, §16.1, §17.3, §18.2 ([R-MTA-04], [R-MTA-05], [R-MTA-10]),
§20.1–§20.5, §21.1–§21.8, §22.3, §23.1, §23.2, Appendix G (head, items 8–10,
closing), Appendix H.

## Mechanical checks I ran myself

- §20.5 contains no occurrence of `barrier`, `durable`, or `[R-LIF-02]`
  (`grep` over lines 3192–3316 and over the whole file). writer-01's grep is
  accurate. The only `barrier` hits are 783, 1174, 1183, 1193, 2927–2929
  (creator), 3066/3069 (appender step 6), 4406 (Appendix H writer checklist).
- §21.7's second-set paragraph: `[R-LIF-02]` appears nowhere in §21.7.
  Confirmed by reading the whole subsection.
- Register totals: §21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10 →
  121, matching §21.8's "121 conditions over 277 instances".
- Shuffle fixed point (register-02): filtered offset = i·n + j, n = L/s. Set
  i = s−1, j = n−1 → (s−1)n + n−1 = sn−1 = L−1; its source offset is
  j·s + i = (n−1)s + s−1 = ns−1 = L−1. The last byte is a fixed point for every
  stride dividing L. §17.3's own worked example agrees (both sequences end
  `40 40`). So a wrong stride never disturbs a packed plane's final byte, and
  T5 cannot witness one. T26's own cell says "the check that detects it is
  T2's or T4's".
- reader-01's planar worked instance: E=T=4 → G=1, N=1, P=4; channels uint8
  (B=1) and uint32 (B=4); disk ordinals c·N+s → 0 and 1; decoded sizes
  P·Bᶜ = 4 and 16 (§14.2 table). A swap yields entry lengths 16 and 4 against
  derived 4 and 16 → T14 under codec 1, T3 under codecs 2–4. No §14 content
  constraint anywhere in the layer. Route verified.
- adversary-01's "new padding position has exactly one referent": grow E from 6
  to 9 with T=4 takes G from 2 to 3; tile 1 (x 4–7) *loses* padding, and tile 2
  is new (not stored in the superseded generation). So a grow never adds a
  padding position to a prior-generation stored tile. Verified; the carve-out's
  only referent is the shrink.
- §20.3 step 4 does list three entry dispositions, unstoring among them:
  "entries for tiles this commit stores or supersedes written to their new
  state, entries for tiles that become unstored written as the sentinel,
  entries new to this generation … emitted per §15". writer-04's quote is
  accurate.
- §20.3 step 6 does carry the appender's [R-CNT-08] duty: "unknown ignore-lane
  flag bits copied forward (`[R-CNT-08]`)". reader-04's premise verified.
- `geometry` in the document: layer geometry at 91, 1041, 1467, 1508, 1919,
  2804, 2988, 3024, 3030–3031, 3127, 3480 (L21), 3491 (L32), 3813, 3934, 4206.
  Line 3401 is §21.2's, and it is the only use that could mean a *file's* byte
  geometry. quiz-03 verified.
- [R-CNT-13] reads "an extent_offset < 16" (line 930). F31 renders it "in
  1-15"; L16 renders it "< 16". register-05 verified.
- §7.4's inline-payload table has columns Field | Type | Constraint — three, so
  it omits offset, **size**, and class. §4.7's Note names only "the offset and
  class columns". diagrams-04 verified.
- §4.5/§8.1 map's last row: "| Extent of a record of a type this specification
  has not assigned | none — the bytes are opaque (§7.2) | — |". No reporting
  duty anywhere for it; Appendix H's verifier entry carries the [R-MTA-10] line
  and no counterpart. verifier-03 verified.
- register-03's constructed file: a trailer re-pointed at generation n's
  directory leaves gen n's directory-pad-trailer as *slack* under §5.2
  ("everything an earlier commit superseded"), so F7 does not fire — F7's
  instances are stored-tile extents, tile-index regions, record extents,
  sub-record extents, none of which a superseded trailer is. Verified.

## Grouping

21 groups over 27 ids. Union checked by hand against the input list.

1. `geo06-disk-ordinal-witness-account` — reader-01, quiz-04
2. `misstrided-filter-t5-attachment` — register-02
3. `21-7-omits-lif-02` — writer-03, diagrams-01, register-03, quiz-02
4. `21-7-omits-appender-ignore-lane` — reader-04
5. `cnf-03-missing-top-level-qualifier` — reader-03, adversary-02
6. `verifier-verdict-mu1-subrecord` — verifier-02
7. `index-regen-trigger-keyed-on-region` — writer-02, quiz-01
8. `compactor-unbound-by-commit-protocol` — writer-01
9. `compactor-minor-floor-antecedent` — reader-02
10. `deletion-enumeration-omits-unstore` — writer-04
11. `r8-collapses-non-finite-forms` — writer-05
12. `r7-condition-drops-bom` — register-04
13. `slack-total-owed-before-trailer` — verifier-01
14. `appendix-h-partial-total` — diagrams-02
15. `unassigned-extent-unreported` — verifier-03
16. `foreign-major-rows-reach` — register-01
17. `geometry-word-sense` — quiz-03
18. `f31-l16-boundary-divergence` — register-05
19. `shrink-into-fill-padding-contradiction` — adversary-01
20. `trailer-mimic-justification` — diagrams-03
21. `presentation-contract-omits-size` — diagrams-04

Grouping calls worth stating:
- reader-01 and quiz-04 both attack §21.7's account of [R-GEO-06]. Same sentence,
  same repair (name the omitted witness routes for the disk-ordinal half).
  register-02 attacks the *tail clause* of the same sentence with a different
  repair (fix the comparison to a mis-strided filter), so it stays separate.
- writer-03, diagrams-01, register-03 and quiz-02 all say §21.7's second-set
  list omits [R-LIF-02]. writer-03 additionally names §20.4's preservation
  regime; that is the same enumeration and the same repair, so it goes here.
- reader-04 also names an omission from §21.7 but a different rule ([R-CNT-08])
  and rests on a claim about §21.7's *stated reason* that I partly refute; kept
  separate so the reconciler sees the PARTIAL.
- reader-03/adversary-02 (reader bullet) and verifier-02 (verifier bullet) are
  about different sentences and reach opposite conclusions about the verifier
  bullet — adversary-02 says it is correct there, verifier-02 says it is not.
  Definitely separate.
- writer-02 and quiz-01 are the same defect verbatim.

## Byte-level judgements, and the quotation behind every downgrade

### Upheld byte-level (2)

**19 `shrink-into-fill-padding-contradiction` (adversary-01).** Two sentences of
§20.3 step 4 give opposite answers for one commit.

(A) "a change that leaves every one of those tiles' stored bytes meaning exactly
what they meant — a filter whose mandated stride makes it the identity
(`[R-COD-10]`), or a new padding position whose stored byte already holds the
fill `[R-SER-05]` fixes — is not what this bars."

(B) "so a shrink that turns real positions into padding of a tile stored there
is barred whether or not the new state still stores it."

I looked for the sentence that decides it and the candidate is "the bar above is
the whole of the test, **in the bar's own tense**". That sentence makes (A) part
of the operative test — but (B) then states an unconditional consequence that
(A) contradicts on exactly the case (A) carves out. There is no reading of (B)
that excludes the fill case without importing (A), and if (A) is imported (B) is
false as written. I verified independently that (A)'s "new padding position"
example has *only* the shrink as a referent (a grow removes padding from
prior-stored tiles and adds it only to new ones), so (A) is not about some other
operation.

Implementer consequence, both sides concretely: appender P (reading A) takes the
caller's "shrink x from 6 to 5", finds that the newly-padding position already
holds the recorded fill, and appends a directory-only generation 2 — a few
hundred bytes. Appender Q (reading B) refuses the commit and tells its caller
the operation needs a whole-file rewrite under a fresh file_id. P's output is a
conforming file (T4 passes; the byte already holds fill). Under B no conforming
writer may emit it — a creator emits generation 1, a compactor emits generation
1 under a fresh file_id, and the only route to generation 2 with that committed
prefix is the barred commit. So the set of byte sequences a conforming
implementation may emit differs between the readings. Byte-level on the emit
half; not on the accept half, since §21.7 says the bar has no live-state witness
and every verifier certifies P's file under either reading. Trimming a time axis
after a partial ingest is the ordinary case, so this is not a corner.

**8 `compactor-unbound-by-commit-protocol` (writer-01).** I could not find the
sentence that binds a compactor to [R-LIF-02], and the text I did find points
the other way:

- [R-LIF-01]: "every conforming mutation of a file is either a commit (§9.2) or
  a whole-file rewrite under a new file_id (compaction, §20)" — compaction is
  expressly *not* a commit.
- [R-LIF-02] binds "A writer performing a commit".
- [R-WRT-02] binds "A creator", and §20.1 makes creator and compactor distinct
  tiers.
- [R-CNT-05]: the pre-trailer pad's number is bounded "**only** through step 5
  of the commit protocol … — a longer gap is conforming, and no conforming
  **commit** produces one." The qualifier is *commit*, not *writer*.
- Appendix G's item 8 and closing paragraph show the document distinguishing "a
  creator's rule, not a compactor's" explicitly where it means to.

So reading B (compactor unbound) has textual support and reading A has only
design sense. Consequence: compactor P pads to the next 64-byte boundary and
emits F = 4096; compactor Q aligns its trailer to a 4 KiB device boundary
(§16.1's Note shows why a writer wants that) and emits F = 8192 with a
3452-byte pre-trailer gap. Both outputs are conforming *files* — §2.3 names
"§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad" among the writer
obligations whose violation is not a file-conformance violation — so no reader
or verifier separates them. What forks is whether Q is a conforming compactor,
which is exactly the emit half of the test. The durability half (a compactor
owes no barrier at all under B, so a crash leaves an output with a valid trailer
over payloads that never reached the medium) is the more consequential half and
is not byte-level. Both halves want the same one-clause repair.

### Downgraded, with the deciding quotation

**1 (reader-01, quiz-04).** §21.1: "The subsections after §21.5 are not part of
the register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's
account of what no check detects, or §21.9's limits." T3 and T14 are register
rows with detector *reader* and outcome reject-tile regardless of how §21.7 is
worded, so a conforming reader rejects the mis-mapped planar tiles either way.
Premise of the downgrade, stated so it can be attacked: that §21.7's account is
purely descriptive and no obligation is sourced from it. If anyone can show a
rule that *derives* an obligation from §21.7's enumeration, this flips.

**2 (register-02).** §21.7's own later sentence: "the check that detects it is
T2's or T4's, exactly as T26 has it", and T26's cell: "the check that detects it
is T2's or T4's, and this row records the cause rather than a procedure of its
own". T5 is a verifier MUST under [R-SER-05] regardless. Nothing emitted or
accepted moves; a corpus author could waste a day trying to build a T5 vector
for a stride error.

**3 (writer-03, diagrams-01, register-03, quiz-02).** Same §21.1 quote as group
1. Additionally §9.2's own Note states the step-3 obligation in terms — "A
writer that re-points a new trailer at a prior generation's directory region has
left step 3 unperformed" — so a writer implementer reading §9.2 gets it right
whatever §21.7 says. And §21.7's first paragraph fixes the verdict question:
"no file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected."

**4 (reader-04).** [R-CNT-08]: "An updater MUST copy forward unknown ignore-lane
bits of the file it modifies and MUST NOT clear them", repeated at §20.3 step 6.
Unambiguous, so no byte moves. Also PARTIAL: reader-04 says §21.7's stated
reason "does not transfer" to the appender, but §21.7 supplies a *second* reason
for exactly these two obligations — "For the last two there is a second, the
output carrying no record of its input's flags or its input's minor either" —
and that one transfers cleanly to an append output. The omission is real; the
"positively obstructs" framing overstates.

**5 (reader-03, adversary-02).** [R-CNT-18]: "an unknown sub-record type with
MU = 1 is reject-layer, and where the file is otherwise conforming a reader MUST
NOT reject the file for it — on a nonconforming file `[R-CNF-12]`'s licence to
reject on any detected violation is untouched". A capitalised MUST NOT directly
on point, plus [R-CNF-12]'s licence running only "For a nonconforming file". A
reader that refuses the whole file is nonconforming, not a second defensible
position. Premise: that removing a duty to accept is not a licence to reject in
the face of a MUST NOT. Attackable only by arguing [R-CNF-03]'s carve-out is
*lex specialis* over [R-CNT-18], which the "MUST NOT" and §21.6's "The qualifier
is load-bearing" both foreclose. Still a normative scope error worth a
five-word repair.

**6 (verifier-02).** §2.3: "*Cannot establish* is not a finding that the file is
nonconforming", and [R-CNT-18] fixes the reader side (accept the file, reject
the layer). So no byte is accepted or rejected differently; what differs is
which of three certificate labels prints. Premise: a verifier's three-valued
verdict is a report about the file, not an accept/reject of bytes. Someone could
attack that — a CI gate keyed on "verdict == conforming" does fork — and I say
so in the group. PARTIAL, because §2.3's own ground list *does* name the case
without a scope qualifier ("when a record carries MUST_UNDERSTAND = 1 with a
type it does not implement"), which supports cannot-establish; the reporter's
"nothing says which" overstates. The confusing part is the parenthetical
"(§21.6)", which points at a passage answering a different question.

**7 (writer-02, quiz-01).** [R-WRT-06]: "Given a conforming input the output is
a conforming file", and [R-WRT-07]'s closing MUST: "The output's reference
arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`): compaction
changes where bytes live, never what a layer denotes." A region carrying stale
offsets fails the partition ([R-CNT-02]), T9's bound, or T1 at minimum, so the
literal reading's output is not a conforming file and [R-CNF-05] bars a
conforming compactor from emitting it. The clause is still bug-bait: an
implementer who codes the exception clause literally ships stale indexes
whenever placement leaves a region in situ, which §20.5 expressly permits
("preserves no placement … free to place structures anywhere §5.2 admits").

**9 (reader-02).** [R-CNF-12]: "Deviation from a SHOULD is not a violation for
this purpose: §21's register enumerates MUST-level conditions only, and a
verifier reports a SHOULD deviation as an advisory that does not bar
certification." Plus [R-CNT-07]: "A reader MUST NOT reject a file for its
version_minor", and [R-ENC-16] makes version_minor the only *descriptive* field
— "its value determines nothing a conforming reader does". So both compactors
emit conforming files and neither is nonconforming; the two bytes at [10,12)
differ but the emittable set does not move. The defect is real all the same: the
antecedent is not evaluable for one of the two cases the rule names, because
[R-WRT-09]'s depth stops at "each relocated extent's checksum" and §20.5 says
its depth "reaches no decoded content". This wants a maintainer decision, not a
word change.

**10 (writer-04).** [R-PRV-01] quantifies over "**any** commit that makes sample
data unreachable", so the omitted case is already covered by the rule's own
force. Verified that §20.3 step 4 does treat unstoring as its own disposition.
Pure enumeration defect; the cost is a writer who does not recognise their
"delete region" operation in the list.

**11 (writer-05).** [R-MTA-04]: "A document is unreadable if it contains a
number whose binary64 interpretation is not finite — which covers a magnitude
that overflows on conversion, `1e400` being the ordinary case — or any of the
bare tokens `NaN`, `Infinity`, or `-Infinity`". All four forms take
ignore-record under every conforming reader. No byte, no verdict. But this is
the finding in the set with the largest *practical* bite that is not byte-level:
under §21.8's "one vector per instance" a corpus built mechanically from R8's
two instances need contain no bare-token vector, and a reader whose JSON library
accepts bare `NaN` by default — the commonest way to be wrong about this bullet
— passes that corpus while being nonconforming. Repair note: raising R8's
instances raises §21.8's 277 (to 279 at two shapes × two containers, 283 at four
forms × two), so the total must move with it.

**12 (register-04).** [R-MTA-04]: "the encoding carries no byte-order mark: a
leading U+FEFF makes the document unreadable", plus §21.1's "where a row and the
rule it cites diverge, **the rule governs**". Confined to the finding aid. Note
the repair direction is opposite to group 11's: R7's *Condition* cell gains the
BOM limb and the instance count and §21.8's total stay at 6 and 277.

**13 (verifier-01).** §5.2 itself: "there is no F and no live state to walk, so
the total is not owed at all: the verifier reports the trailer failure and
nothing about slack, which is not a partial total but the absence of one." The
reason is stated and generalises to any pre-trailer rejection; F5 and F6 are
both reject-file at open under either reading, so no verdict on bytes moves. But
the antecedent names "§6.2's ordered validation" while F5's rule is [R-CNT-27]
(§5.1) and F6's is [R-CNT-04] (§6.1), and §21.2's preamble expressly puts
F6/F1's front-block instance ahead of §6.2's gates. Widen the antecedent.

**14 (diagrams-02).** Appendix H's own preamble: "each entry's authority is the
requirement or section cited, never this summary", and its citation is
[R-CNT-21], which states three cases. Non-normative and self-disclaiming. Still
worth fixing: an implementer auditing against the checklist emits, for a torn
file, a slack figure computed from the physical length — a number §5.2 calls
"not a partial total but the absence of one", and §22.3 makes that figure
load-bearing.

**15 (verifier-03).** §8.1's map row states the position: "none — the bytes are
opaque (§7.2)", and §2.3 confirms nothing is left unchecked at such an extent
("no content rule attaches there, so nothing is left unchecked"). So no duty
exists and no verifier verdict moves. The asymmetry against [R-MTA-10]'s
reporting duty is real and §22.3 constructs it deliberately ("equally
invisible") without completing it. Maintainer decision, not an edit.

**16 (register-01).** [R-CNT-07]: "A reader MUST reject-file when version_major
is 0 (invalid) or is a major it does not implement", so every reader rejects a
major-7 file either way; and §2.3: the refusal "is not a finding about its
bytes". No writer emits a major-7 file under this text. Only the verifier's
label forks. PARTIAL: §21.2's preamble justifies the *first* half of its
contrast with reader ordering ("§6.2 puts the version gate ahead of every check
but the trailer magic and the trailer CRC, so such a file is refused on
capability grounds first"), which is evidence for reading (b) — "reach" as "the
check still runs" — against register-01's confident (a). The residual open
question (which verdict a verifier prints) is genuine.

**17 (quiz-03).** §6.2 [R-CNT-06] fixes the order independently: "A reader MUST
validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3)
… and then, those gates passed, MUST validate all of the following". Both senses
of "geometry" land on the same set of checks for any concrete file. I confirmed
by grep that this is the document's only use of "geometry" that is not a layer's
extents/tile extents.

**18 (register-05).** §21.1: "where a row and the rule it cites diverge, the
rule governs", and [R-CNT-13] states "an extent_offset < 16". So the operative
bound is < 16 at both scopes and F31's "1-15" has no normative force. Identical
outcome, detector and detection point either way. Only corpus attribution for
the single slot (0, nonzero) is affected.

**20 (diagrams-03).** §21.1: "§21.6's entries restate their governing rules on
the same terms a row does, and where such an entry and the rule it cites
diverge, the rule governs there too." The verdict (Inert) and the citation
([R-LIF-06]) are both right; only the first justification clause belongs to the
slack case rather than the payload case the row states. §22.3 keeps the two
apart correctly.

**21 (diagrams-04).** §7.4's Type column gives u8/u16/u64 for every fixed field
and §4.2 fixes those widths normatively, so no implementation can read a
different width out of this. The Note is simply one column short of describing
its own table.

## Notes on completeness

27 input ids; 21 groups; member_ids union counted by hand against the input list
and equal to it, no duplicates. No finding was dropped or left unevaluated. I did
not verify register-04's arithmetic claim (58 + 116 + 55 + 48 = 277) row by row —
I verified only that the four subsection counts sum to §21.8's 121 conditions and
that R7's cell as printed carries six instances. That is the one input claim I
took on trust; it does not change the group's grade, since the Condition-cell
omission is visible on its face.
