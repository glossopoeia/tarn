# Repair audit — lane: downstream dependents of §21.7
# Hunks: 01 (§11.1 Rationale), 07 (§21.1 completeness clause),
#        08 (§21.1 second reference), 09 (§21.7 body)

## 0. Disclosure

Read: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md
(sections read in full: §2.1, §2.3, §2.4, §2.5, §7.4 incl. its closing Note,
§11.1, §11.2 opening, §13/§14 ordinal rule [R-GEO-06] and its Example,
§17.3 tail, §17 R4 zstd paragraph, §20.3 step 4 in full (lines 3150-3260),
§20.5 (lines 3410-3470), §21.1 in full, §21.2-§21.5 rows T2/T3/T4/T5/T14/T26
and the L-rows governed by [R-CNT-18], §21.6 tail, §21.7 in full, §21.8,
§21.9 opening).
Read: the four hunk files named in my charter, and only those:
  scratchpad/case-adr0113/hunk-01.diff, hunk-07.diff, hunk-08.diff, hunk-09.diff
Did NOT read: full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, git history, the web.
Did not list the case directory (I catted the four paths named in my charter).
Ran: grep and python3 regex sweeps over spec/tarn.md only (transcribed in §2).
No network, no other files.

CONTEXT I DID NOT ASK FOR: material was injected into my context before I began
— a project instruction file (CLAUDE.md pointing at AGENTS.md), a user
auto-memory index naming two memory notes about this project's harness and a
"lineage gate word list", an MCP server instruction block, and a skills
listing. I did not open any of the files those referred to and I drew no
conclusion from them. I name that they appeared; I do not repeat their content.

## 1. The rule each repair adopts, in my own words

HUNK 01 (§11.1 Rationale, non-normative). What it makes true of an
implementation: nothing directly — it is a labeled Rationale. What it asserts
about the normative rules: §20.3 step 4 carries exactly two bars; the one that
can bite a shrink or a growth is the §14 bar; the other bar (planar disk
ordinals) bites neither a shrink nor a growth; the free-redeclaration permission
is quantified over the *superseded* generation, so a commit cannot earn it by
emptying the layer in the same commit; re-typing a channel is the §14 bar's
subject and is barred where the layer stores a tile carrying that channel.

HUNK 07 (§21.1 completeness clause, expressly normative). It replaces a
pointer ("§21.7 the account, by class, of what fails it") with an embedded
*definition*: a violation is detectable iff some file exhibiting it differs, in
its live state, from every file that does not. Effect on an implementation: the
term that gates [R-CNF-07] and gates the register's normative completeness now
has a stated extension.

HUNK 08 (§21.1, normative). One word: §21.7 is characterised as a "test" rather
than an "account". Effect: §21.7 stops being a list and becomes a decision
procedure, and the sentence saying the completeness clause does not *reach* it
now denies reach to the very thing the clause turns on.

HUNK 09 (§21.7, normative + a new Rationale). It replaces an enumeration with a
two-clause definition — unwitnessed / detectable — asserts they are complements,
carves out a third category ([R-ENC-06], "no file can violate"), states that
unwitnessedness bears on detection and not on permission, and demotes the whole
former enumeration into a **Rationale.** block with a priority clause ("the test
governs"). Effect on an implementation: an updater/writer is told plainly that an
unwitnessed obligation still binds it; a document maintainer is given a
mechanical test for what the register owes a row.

## 2. Sweeps run (verbatim, with hit counts)

All sweeps whitespace-normalised in python (`re.sub(r'\s+',' ',t)`) before
matching, because the document is hard-wrapped and every phrase I care about
spans a line break. Line-oriented greps are marked as such.

  grep -n '21\.7' spec/tarn.md                                  -> 8 lines
      2521, 2613, 3240, 3457, 3560, 3580, 3774, 3864(heading)
  normalised 'unwitnessed'                                      -> 7
  normalised 'witness'                                          -> 21
  normalised 'account'                                          -> 8
  normalised 'inventor'                                         -> 3
  normalised 'catalog'                                          -> 0
  normalised 'undetectab'                                       -> 3
  normalised 'detectab'                                         -> 13
  normalised 'no check'                                         -> 8
  normalised 'the list'                                         -> 6
  normalised 'a list'                                           -> 1
  normalised 'live state'                                       -> 23
  normalised 'by class'                                         -> 0   (old wording gone)
  normalised 'no witness'                                       -> 4
  normalised 'omitted from the register'                        -> 3
  normalised 'completeness'                                     -> 4
  normalised 'every detectable'                                 -> 2
  normalised 'can establish'                                    -> 1
  normalised 'establish'                                        -> 32
  grep -n 'nesting prohibition'                                 -> 1 line (1169)
  grep -n 'R-GEO-06|R-SER-01|R-COD-10|R-CNT-13|R-CNT-18|R-LIF-01|R-WRT-06|R-ENC-06'
                                                                -> 60 lines
  grep -n '^| T2 |^| T3 |^| T4 |^| T5 |^| T14 '                 -> 5 rows
  grep -n 'R-CNF-0[1-9]|R-CNF-1[0-9]'                           -> 48 lines

### 2a. Old-shape sweep result (charter item)

"account": 8 hits. Seven are unrelated senses ("request accounting" §6.4 x4,
"accounted for" §5.2 Rationale, "accounting" §19.1, "accounting" §23). The
eighth is inside §21.7 itself — "Nothing is omitted from the register on its
account, there being no condition to omit" — the idiom, not a characterisation.
"inventor": 3 hits. (i) [R-CNF-12]: "the MUST-level conditions §21 inventories"
— §21 as a whole, i.e. the register, not §21.7. (ii) §19 preamble: "not the
complete inventory of what a reader detects at that tier: §21's register is" —
again the register. (iii) §21.9: "a finding aid rather than an inventory" —
§21.9's own limits table.
"catalog": 0. "by class": 0 (the pre-repair phrase "the account, by class, of
what fails it" is gone everywhere).
VERDICT: the old shape has been swept. No surviving text calls §21.7 an
account, an inventory, a list or a catalogue.

## 3. Every citation of §21.7, with verdict

C1. §17.3 (line 2521), NORMATIVE (plain prose ending `[R-COD-10]`), quoting:
    "...and otherwise the consequence is wrong sample content — undetectable
    by construction (§21.7)."
    Cited for: a mis-strided filter with no §14-constrained byte is undetectable.
    §21.7 still says it, in its FIRST paragraph, which the repair did not touch
    and which is normative (unlabeled prose): "A writer that emits well-formed
    structures carrying wrong sample values — a mis-strided filter
    (`[R-COD-10]`) ... produces a file that every checksum in §8 certifies."
    Lands on normative text. Also survives the NEW test: whether a stride is
    "wrong" is not a function of the bytes, so a violating and a satisfying file
    can share a live state. VERDICT: PASSES.

C2. §17 R4 paragraph (line 2613), NORMATIVE, quoting:
    "Two of those carry no witness a file exhibits, and R4 registers neither:
    dictionary use the header does not disclose is a writer violation nothing in
    the extent shows, exactly as `[R-COD-06]` has it for a tile (§21.7)".
    Cited for: [R-COD-06]'s undisclosed dictionary is unwitnessed.
    §21.7 ¶1 still names it ("an undisclosed compression dictionary
    (`[R-COD-06]`, and `[R-MTA-09]` for a user-metadata document...)").
    Lands on normative text. VERDICT: PASSES.

C3. §20.3 step 4 (line 3240), NORMATIVE, quoting:
    "§21.7 records the consequence — that this is precisely where the §14 bar
    has no witness, the live state being clean — which is why the rule is stated
    here and not left to the rows."
    Cited for: a commit that supersedes every tile it would have damaged leaves
    the §14 bar unwitnessed.
    §21.7 still says it — but ONLY inside the new **Rationale.** block: "And a
    commit that supersedes every tile it would have damaged leaves the live
    state clean, so the §14 bar is unwitnessed there..."
    So the support moved from normative to non-normative. Does that break §20.3?
    No: §20.3's own sentence is the normative assertion and the §21.7 pointer is
    explanatory ("which is why the rule is stated here"). §21.7's normative test
    independently yields the same classification. Note also that the repair
    renamed "the bar" to "the §14 bar" inside that sentence, which was necessary
    once the block discusses two bars, and it now matches §20.3's own naming.
    VERDICT: PASSES, with the standing note that the cited sentence is now
    non-normative.

C4. §20.5 (line 3457), NORMATIVE, quoting:
    "Neither obligation has a witness in the output alone (§21.7)."
    Cited for: the ignore-lane carry-forward MUST and the version_minor SHOULD
    are unwitnessed. §21.7 says it, again only in the Rationale block: "§20.5's
    three obligations on a compacted file's trailer (`[R-WRT-06]`)...".
    Arithmetic check: §21.7 says THREE; §20.5's local "Neither" covers TWO. I
    counted §20.5's obligations: (1) "It MUST mint a fresh file_id for the
    output" (earlier paragraph); (2) "The output trailer MUST copy the input's
    unknown ignore-lane flag bits forward"; (3) "the output's version_minor
    SHOULD be at least the input's". Three total; "Neither" scopes to the two in
    its own paragraph. No conflict.
    Note: the unwitnessedness of the fresh file_id draw is asserted normatively
    in §20.5 itself ("a compacted file and a file appended to a hundred times
    are indistinguishable by their live trailers alone"), so nothing is left
    resting on the Rationale alone. VERDICT: PASSES.

C5. §21.1 completeness clause (line 3560, hunk 07), NORMATIVE (expressly:
    "Its **completeness is normative**"), quoting:
    "detectability being the gate `[R-CNF-07]` already applies and §21.7 states
    the test for: a violation is detectable exactly where some file exhibiting
    it differs, in its live state, from every file that does not"
    Word-for-word against §21.7: "a violation this specification names is
    **detectable** exactly where some file exhibiting it differs, in its live
    state, from every file that does not." Identical but for the qualifier "this
    specification names". VERDICT: the quotation PASSES; but see FINDING B-02
    for what the definition does to §21.1's own opening sentence.

C6. §21.1 second reference (line 3580, hunk 08), NORMATIVE, quoting:
    "neither this completeness clause nor the instance arithmetic below reaches
    §21.6's defined non-violations, §21.7's test for what no check detects, or
    §21.9's limits."
    Cited for: §21.7 carries no register rows. Still true. But the word swap
    collides with §21.7's own new sentence. See FINDING B-03.

C7. §21.4 row T26 (line 3774), NORMATIVE (a register row), quoting:
    "(a wrong stride with no such structural constraint is undetectable, §21.7)".
    Same subject as C1; §21.7 ¶1 still supports it, normatively.
    VERDICT: PASSES.

## 4. Citations inside the repaired text (check 2)

  [R-CNF-07] — opened, line 288: "Every detectable file-conformance violation
      named by this specification is assigned exactly one **reader outcome**:
      reject-file, reject-layer, reject-tile, or ignore-record." §21.7's claim
      that this is "the gate [R-CNF-07] applies in assigning an outcome" is
      correct: detectability is literally the gate. PASSES.
      BUT [R-CNF-07] says "detectable *file-conformance* violation"; §21.7's
      definition says "a violation this specification names". Wider set. Noted.
  [R-CNF-11] — opened, line ~242. §21.7 ¶1's disclaimer ("None of these is a
      requirement a verifier is *unable to check* within the meaning of
      `[R-CNF-11]`") is sound: [R-CNF-11] confines *cannot establish* to "a
      capability or resource ground". PASSES; see B-06 for what the repair did
      around it.
  §9.7 — opened, "Coverage verification": "A verifier checking `[R-CNT-02]`'s
      partition walks the live state only." §21.7's "the live state, which is
      all §9.7 walks" is accurate. PASSES.
  §2.4 — opened. The outcome classes are there. PASSES.
  [R-ENC-06] — opened, line 477 ("width is invalid at its owning scope").
      §21.7's characterisation ("the parse is always at the widths this
      specification fixes") is unchanged from the superseded text. PASSES.
  §21.1's completeness clause, as cited from §21.7 ("§21.1's completeness clause
      turns on") — opened; it does turn on "detectable". PASSES as a citation;
      see B-03 for the reach/turns-on collision.
  §20.3 step 4 (from hunk 01 and hunk 09) — opened in full. Two bars confirmed:
      the §14 bar, and "One effect is barred beside it, on the same tense and on
      its own ground ... For a **planar** layer, a commit MUST NOT change the
      channel declarations in a way that alters the disk ordinal `[R-GEO-06]`
      assigns any tile the layer stores in the generation this commit
      supersedes." PASSES.
  §12.1 element sizes (hunk 09's new sentence) — the claim "a planar `uint8`
      channel re-declared `bool` keeps its element size of 1 while its plane
      goes from P · Bᶜ bytes to ⌈P/8⌉" matches T3's instance list
      ("planar numeric P·Bᶜ ... packed planar bool ⌈P/8⌉"). PASSES.
  T2/T3/T4/T5/T14/T26 — all six opened and read; each is cited for what it
      actually tests. T3 = decoded payload byte length; T14 = codec 1 declared
      length; T4 = padding position fill; T5 = packed planar bool pad bit;
      T2 = interleaved bool value byte; T26 = wrong filter stride, detected by
      T2's or T4's check. PASSES.
  [R-GEO-06] / [R-SER-01] — opened (lines ~1690-1703, 1945). Disk ordinal
      c·N+s for planar, s for interleaved; [R-SER-01] the interleaved value
      sequence. PASSES as cited.
  [R-CNT-13], [R-CNT-18] — opened (1020, 1110-1128). See B-01/B-02.
  §7.4's closing Note — opened (line 1169). See B-05.

## 5. Check 3 — normative force, by LABEL not by marker

  §21.1: plain prose, no blockquote. Normative, and its completeness is
      expressly declared normative. Hunks 07 and 08 land in normative text. GOOD.
  §21.7 ¶1-¶4 (including both new definitional paragraphs and the
      "Distinguish..." paragraph ending `[R-ERR-01]`): plain prose, no
      blockquote, no label. Normative under [R-CNF-01]. Hunk 09's DEFINITION
      lands in normative text. GOOD — I applied the label test, not the ">"
      test; there is no ">" on those paragraphs at all.
  §21.7's walk-through: now inside a block whose opening words are
      "> **Rationale.** The obligations this test places outside the register,
      as the document stands." LABELED Rationale -> NON-NORMATIVE by
      [R-CNF-01]. This is a deliberate demotion, and the block says so ("This
      walk-through illustrates the test and does not extend it").
      Consequence checked: is any rule whose ONLY statement is now inside that
      block relied on normatively elsewhere? I checked C3 and C4 (the two
      citations that point at material inside the block). Both are backed by a
      normative sentence at the citing site. So the demotion did not orphan a
      rule. GOOD.
  §11.1 hunk 01: block opens "> **Rationale.** Empty layers serve schema-first
      workflows". LABELED Rationale -> NON-NORMATIVE. The repair therefore
      changes no obligation. I checked each rule it states against §20.3 step 4
      (see §7 below) — all four are stated normatively there, so the repair did
      not fail to land: it is a gloss on rules that hold anyway.
  §7.4's nesting note: block opens "> **Note.**" -> NON-NORMATIVE. See B-05.

## 6. Check 8 — what the insertions did to the sentences around them

HUNK 09, FORWARD. Text after the insertion is §21.8: "Every row of §21.2
through §21.5 — 120 conditions over 275 instances — has at least one
conformance vector (§24) whose expected outcome is that row's outcome, and one
vector per instance. A row without a vector is a gap in the corpus, not a
licence to skip the check. `[R-ERR-02]`". No anaphor reaches back into §21.7.
UNAFFECTED.

HUNK 09, BACKWARD (anaphors inside the moved block):
  - "A second set of obligations is omitted from the register because a single
    file exhibits no witness of their violation."  ->  FINDING B-04.
  - "where an item here and the test above disagree, the test governs" — "the
    test above" resolves to the new normative paragraph. Explicit, correct,
    UNAFFECTED (and it reaches across the quote boundary deliberately).
  - "Its companion bar on a planar layer's disk ordinals" — "Its" = §20.3 step
    4's §14 bar, named in the immediately preceding clause. UNAFFECTED.
  - "so the §14 bar is unwitnessed there for the same reason `[R-LIF-01]` is"
    — the repair changed a bare "the bar" to "the §14 bar" here. Before the
    repair the block discussed one bar; now it discusses two, so the bare
    anaphor WOULD have re-resolved. The repair pre-empted it. GOOD CATCH BY THE
    REPAIR — I record it as a check-8 pass, not a defect.
  - "the register's rows reach it on the terms they state there and no better"
    — "it" = the change that touches something §14 fixes, named in the same
    sentence. UNAFFECTED.
  - "For the last two there is a second" — "the last two" = the ignore-lane
    bits and the version_minor floor, named two clauses earlier. UNAFFECTED.
  - "`[R-ERR-01]`" moved: it formerly terminated the whole enumeration; it now
    terminates the "Distinguish an unwitnessed requirement from one **no file
    can violate**" paragraph, so its scope is now the normative test rather
    than the enumeration. That is coherent with the demotion. UNAFFECTED.

HUNK 09, ¶1 UNTOUCHED SENTENCE: "None of these is a requirement a verifier is
*unable to check* within the meaning of `[R-CNF-11]`". "these" resolved, before
the insertion, to ¶1's list AND stood immediately before "A second set of
obligations...", which made the scoping visible. It still resolves to ¶1's
list — but see B-06 for the gap this leaves now that the section defines a
general class.

HUNK 07, FORWARD. After the inserted definition: "— but each row *restates* its
governing rule, and where a row and the rule it cites diverge, **the rule
governs**. Conditions attach to the finest structure they damage, and the
outcome follows from that scope — subject to the same exception stated above, a
rule that assigns an outcome expressly — never from the severity of the
corruption." The one anaphor, "the same exception stated above", resolves to
"except where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine does
for every §21.5 row" in the same paragraph's opening. The insertion adds no
exception, so no re-resolution. UNAFFECTED. The "but" contrast still attaches to
"Its **completeness is normative**". UNAFFECTED. The pre-repair "of what fails
**it**" anaphor was deleted by the repair, which is an improvement.

HUNK 08. One-word swap, no insertion, no anaphor moved. But see B-03.

HUNK 01, FORWARD. The inserted sentence "The other bar reaches neither a shrink
nor a growth: it bars a change to a planar layer's channel declarations that
moves a stored tile's disk ordinal." now sits immediately before untouched text:
"Growth that leaves **entry_count** unchanged touches the directory alone ...
Growth that changes entry_count changes extent_length with it (`[R-CNT-17]`),
so the layer's whole tile-index region is re-emitted and disk ordinals renumber
wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`)". I looked hard at this:
the repair says the disk-ordinal bar does not reach a growth, and two sentences
later the same block says a growth renumbers disk ordinals. I traced it to
§20.3 step 4 and the collision resolves: the bar's antecedent is "change the
channel declarations in a way that alters the disk ordinal", and a growth
changes the geometry, not the channel declarations; §20.3 says exactly that
("what it disturbs is instead the re-emission rule above, whose only stated
occasion for a renumbering is a geometry change"). I also worked the combined
case — grow an extent (N changes) AND append a channel in one commit: ordinals
of stored tiles move, but the declaration change alone moves none, so the bar
is not triggered and the re-emission rule covers the renumbering. NOT A DEFECT;
recorded as a rejected candidate.
Other anaphors after the hunk-01 insertion: "the growth that raises a
zero-extent layer's **last** zero grid count included" — resolves within its
own sentence. UNAFFECTED.

HUNK 01, BACKWARD. The inserted text's own back-references: "Of its two bars"
("its" = §20.3, named in the preceding sentence — UNAFFECTED); "such a tile"
("a layer that already stored tiles in the generation a commit supersedes",
preceding sentence — UNAFFECTED); "The other bar" ("its two bars" minus the §14
bar — UNAFFECTED); "the §14 bar's own subject" — UNAFFECTED.

## 7. Check 1 — tense and quantifier, per hunk

HUNK 01. Four restated rules, each checked against §20.3 step 4:
  (a) "a shrink is barred wherever it alters what §14 fixes for such a tile —
      whether or not the new state still stores it"
      vs §20.3: "A shrink is permitted exactly where it alters nothing §14
      fixes for any tile the layer stores in the generation this commit
      supersedes ... the quantifier is the superseded generation's, so a shrink
      that alters what §14 fixes for a tile stored there is barred whether or
      not the new state still stores it."  MATCH. Generation: superseded.
      Quantifier: any/every such tile. MATCH.
  (b) "A layer that stored no tile in the generation the commit supersedes may
      be re-declared freely; a layer the commit itself empties does not qualify."
      vs §20.3: "A layer that stores no tile **in the generation this commit
      supersedes** MAY be re-declared freely ... the tense is both bars', so a
      commit does not earn this permission by emptying the layer as it
      re-declares it."  MATCH, and the repair's added second clause is exactly
      §20.3's own carve-out. This is the sentence hunk 01 rewrote (from the flat
      "A layer that stored nothing may be re-declared freely"), and the rewrite
      moves it INTO agreement with the normative rule. GOOD.
  (c) "Re-typing a channel is the §14 bar's own subject, barred wherever the
      layer stores a tile that carries that channel, and free where it does not."
      vs §20.3: "changing it is such a change wherever the layer stores a tile
      that carries that channel ... Where the superseded generation stored no
      tile carrying that channel there is nothing to reinterpret, and this bars
      nothing". The repair reproduces §20.3's own present-tense wording
      verbatim. Its tense is under-specified in isolation, but it is
      under-specified identically in the normative rule, and §20.3 disambiguates
      two sentences later. Not repair-introduced. RECORDED AS REJECTED
      CANDIDATE, not a finding.
  (d) "The other bar reaches neither a shrink nor a growth: it bars a change to
      a planar layer's channel declarations that moves a stored tile's disk
      ordinal."
      vs §20.3: "The bar beside the §14 bar does not reach a shrink either: it
      bars a change to a planar layer's channel declarations that moves a
      stored tile's disk ordinal, and a shrink is not one."  MATCH for shrink.
      For growth: §20.3 does not say it in those words, but a growth is not a
      channel-declaration change, so the extension is sound. See §6 above.

HUNK 07 / HUNK 09 definitions. This is where the quantifiers break. Written out:
  Unwitnessed(R)  ==  EXISTS f violating R, EXISTS g satisfying R:
                      live(f) = live(g)
      ("a file that violates it and a file that satisfies it CAN present
        identical live states"; reinforced by the gloss "ask whether the breach
        CAN BE MADE to leave the live state ... exactly as a conforming commit
        would leave it" — "can be made" is explicitly existential)
  Detectable(V)   ==  EXISTS f exhibiting V, FORALL g not exhibiting V:
                      live(f) != live(g)
      ("some file exhibiting it differs, in its live state, from every file
        that does not")
  NOT Detectable(V) == FORALL f exhibiting V, EXISTS g: live(f) = live(g)
So the negation of "detectable" is a FORALL-EXISTS statement and "unwitnessed"
is an EXISTS-EXISTS statement. NOT-detectable implies unwitnessed; unwitnessed
does NOT imply not-detectable. -> FINDING B-01.
Worse, the two halves range over different individuations: "unwitnessed" is
predicated of a REQUIREMENT, "detectable" of a VIOLATION. The document
individuates those apart on purpose — [R-CNF-13]: "A **condition** this
specification names — one malformed state, as §21.1 individuates them, and not
the requirement that defines it ... Reach is per condition because a single
requirement can state several: `[R-CNT-06]` states nine". -> FINDING B-01.

## 8. Check 5 — exhaustive claims in the repaired text, each falsified or not

  "That is the whole of the test, and it decides any requirement put to it
   without appeal to a list" — "any requirement", "the whole". Tried to
   falsify: the test is stated over files and live states, but several of the
   obligations §21.7 classifies are not properties of a file at all (a commit's
   history, a compaction's provenance, a superseded generation's declarations).
   The gloss that follows rescues the act-shaped cases ("ask whether the breach
   can be made to leave the live state ... exactly as a conforming commit would
   leave it"). I judged this SURVIVES, narrowly, and recorded it as a rejected
   candidate rather than a finding.
  "**Detectability is its negation**" — FALSIFIED. See B-01.
  "The register's completeness is a claim about those and no others" — "and no
   others". Checked against §21.1's opening sentence and clause. Collides for
   partially-witnessed requirements. See B-02.
  "Of its two bars" (hunk 01) — counted §20.3 step 4: the §14 bar, and "One
   effect is barred beside it". EXACTLY TWO. PASSES.
  "for a reason all three share" (§21.7 Rationale, §20.5) — counted §20.5's
   trailer obligations: fresh file_id MUST; ignore-lane bits MUST; version_minor
   SHOULD. THREE. PASSES.
  "Nothing is omitted from the register on its account, there being no condition
   to omit" ([R-ENC-06]) — checked: no register row cites [R-ENC-06] as its
   governing rule (grep 'R-ENC-06' returns only line 477 and line 3904).
   PASSES.
  "no field of a file records how many commits that history holds" — matched
   against §20.5's independent "no field counts commits". PASSES.
  "both filter values are length-preserving (§17.3)" — §17.3's filter 2 text:
   "Length is unchanged." PASSES.

## 9. Check 6 — what the structure leaves unconstrained

The structure the hunk-09 repair governs is §21.7's CLASSIFICATION OF
REQUIREMENTS. Its members, exhaustively as the section now presents them:
  (a) requirements about content-wrongness that structure cannot see (¶1);
  (b) unwitnessed requirements generally (¶2, the new definition);
  (c) detectable violations (¶3);
  (d) requirements no file can violate (¶4, [R-ENC-06]);
  (e) requirements a verifier is "unable to check" under [R-CNF-11]
      (mentioned in ¶1 only, to be excluded).
Now, for each: what fixes it?
  (a) fixed: ¶1 states the outcome (checksums certify; the verdict is
      unaffected; NOT an [R-CNF-11] ground).
  (b) fixed as to permission ("the requirement binds its actor as any other
      does") and as to the register ("absent from it by the clause's own
      terms"). NOT fixed as to (e): ¶1's disclaimer "None of these is a
      requirement a verifier is *unable to check*" is anchored to (a) by the
      anaphor "these", and the repair generalised (a) into (b) without
      generalising the disclaimer. -> FINDING B-06.
  (c) fixed by [R-CNF-07] and §21.1.
  (d) fixed: no outcome, no row, no omission.
  (e) fixed by [R-CNF-11] itself ("a capability or resource ground"), which is
      what keeps B-06 below the byte-level bar.
Sibling-quantity test on hunk 01: the structure is §20.3 step 4's pair of bars.
Quantities: (i) which operations each bar reaches; (ii) the tense each is
quantified over; (iii) the carve-outs. Hunk 01 fixes (i) for both bars, (ii)
for the §14 bar and for the free-redeclaration permission — and it explicitly
says nothing about (ii) for the disk-ordinal bar. §20.3 does say it: "One
effect is barred beside it, **on the same tense** and on its own ground".
So the sibling is governed, just not by the Rationale. NOT A GAP.

## 10. Check 7 — arguments by analogy in the repaired text

Hunk 09, "for the same reason `[R-LIF-01]` is: it is a property of the prior
generation, which §9.7 does not reconstruct".
  repair's governing verb: "leaves the live state clean" (a commit)
  cited rule's governing verb (§21.7's own gloss on [R-LIF-01]): "are
  properties of a file's history, which §9.7 does not reconstruct"
  Same set? Both range over facts §9.7's live-state walk cannot reach. YES.
  PASSES. (This analogy carries only ONE item, so no per-member retest needed.)

Hunk 09, "exactly as a mis-strided filter is" ([R-GEO-06]/[R-SER-01] witnessed
by T2, T4 or T5).
  repair's verb: "a mis-ordered image is then **witnessed by** T2, T4 or T5"
  cited row T26's verb: "the check that detects it is T2's or T4's"
  Same set? T26 names T2 and T4; the repair adds T5. T5 is "In a packed planar
  bool plane ... a final-byte pad bit ... is not the channel's fill bit", which
  a mis-ordered planar bool image can break and a mis-strided filter cannot
  (filter 2 on packed planar bool is the identity, s = 1, per T26's own
  instances). So the extra member is correct and the analogy is used only for
  the shared part. PASSES.

Hunk 09, "on the same terms T26 states for a wrong stride" (carried for TWO
things: a filter change, and a sample's byte offset moving).
  repair's verb: "is witnessed on the same terms T26 states"
  T26's verb: "where the resulting image breaks §14.5's padding content or
  `[R-SER-08]`'s bool bytes"
  Tested separately, as the charter requires:
   - filter change: filter values are length-preserving (§17.3), so no length
     row fires; only the content rows can. MATCHES T26's terms. PASSES.
   - sample byte-offset move at unchanged image length: no declared quantity
     changes, so again only the content rows can fire. MATCHES. PASSES.
  Both members sound. This is the exact shape that failed last cycle; it holds
  here.

Hunk 09, "exactly as `[R-COD-06]` has it for a tile" — that is §17's sentence
citing §21.7, not §21.7 citing out. Checked at C2. PASSES.

Hunk 09, "this is the gate `[R-CNF-07]` applies in assigning an outcome".
  repair's verb (one sentence later): "the outcome classes of §2.4 are assigned
  to violations a reader or verifier **can establish**"
  [R-CNF-07]'s verb: "Every **detectable** file-conformance violation named by
  this specification is assigned exactly one reader outcome"
  Same set? NO. §21.7 has just defined "detectable" as a property of live
  states, saying nothing about any actor's capability; "can establish" is a
  property of an actor. -> FINDING B-06.
  Also [R-CNF-07] says "file-conformance violation"; §21.7 drops the qualifier.

Hunk 01, "exactly as it is there" ("a shrink producing only those is permitted
here exactly as it is there") — that phrase is §20.3's, not hunk 01's. Hunk 01
argues by analogy nowhere; it restates. Nothing to compare. RECORDED.

## 11. Findings

### B-01  OVERCLAIM — "Detectability is its negation" is false as written
§21.7, normative paragraph 3.
QUOTE: "**Detectability is its negation**, and this is the gate `[R-CNF-07]`
applies in assigning an outcome and §21.1's completeness clause turns on: a
violation this specification names is **detectable** exactly where some file
exhibiting it differs, in its live state, from every file that does not."
AGAINST: "A requirement of this specification is **unwitnessed** where a file
that violates it and a file that satisfies it can present identical live
states."
Two independent reasons it fails.
(1) QUANTIFIER. "Unwitnessed" is EXISTS-EXISTS; the negation of "detectable" is
FORALL-EXISTS. Not-detectable entails unwitnessed; unwitnessed does not entail
not-detectable. A requirement some of whose breaches leave a twin and some of
whose breaches do not is BOTH unwitnessed and detectable.
(2) INDIVIDUATION. "Unwitnessed" is predicated of a REQUIREMENT; "detectable"
of a VIOLATION. The document individuates those apart deliberately —
[R-CNF-13]: "Reach is per condition because a single requirement can state
several: `[R-CNT-06]` states nine". A predicate on requirements cannot be the
negation of a predicate on conditions.
WORKED COUNTEREXAMPLE, from the document. [R-CNT-18] states several conditions.
One is "the fixed fields, the d dimension entries, the C channel entries, and
the trailing fixed fields MUST lie entirely within the inline payload ... any
overrun, truncation, or residue is a validity error at layer scope" — registered
as L23, and byte-determined, so some file exhibiting it differs in live state
from every file that does not: DETECTABLE. Another is "a sub-record MUST NOT
itself contain records", which §21.7's own Rationale calls "detectable only by
parsing a payload no format-major-1 reader parses as a record sequence" and
which §7.4's Note says has "no register row": UNWITNESSED. So [R-CNT-18] is
both, and the sentence is false of it. (Three register rows carry [R-CNT-18] as
governing rule: L23, L24, L26.)
The third category the repair itself supplies is a second counterexample:
[R-ENC-06] satisfies NEITHER definition — no file violates it, so there is no
violating/satisfying pair (not unwitnessed) and no file exhibiting it (not
detectable) — yet a true negation admits no third case. The very next paragraph
says "Distinguish an unwitnessed requirement from one **no file can violate**".
REPAIR: state detectability of a CONDITION and unwitnessedness of a CONDITION,
and make the negation a genuine complement: "A condition this specification
names is **unwitnessed** where every file exhibiting it shares its live state
with some file that does not; it is **detectable** otherwise." Then say
separately that a requirement may state conditions of both kinds, and that
[R-ENC-06] states none.
BYTE-LEVEL: NO. Both readings leave every register row, every reader duty under
[R-CNF-04], and every writer duty under [R-CNF-05] where they are. The dispute
is over whether the DOCUMENT is defective, not over any file's verdict.

### B-02  LOCAL_CONTRADICTION — §21.1's completeness clause and §21.7's licence
give opposite verdicts on the same requirement
§21.1 (untouched opening sentence, and the clause hunk 07 rewrote) against
§21.7 (hunk 09).
QUOTE (§21.7): "The register's completeness is a claim about those and no
others, so an unwitnessed obligation is absent from it by the clause's own terms
rather than in breach of them."
AGAINST (§21.1, opening sentence, untouched by any hunk): "The register — §21.2
through §21.5 (`[R-ERR-02]`) — enumerates every detectable file-conformance
violation this specification names"
and (§21.1, hunk 07): "Its **completeness is normative** — a *detectable*
file-conformance violation this specification names and the register omits is a
defect in this document".
Take [R-CNT-18] again. It is unwitnessed (its nesting prohibition has no
register row, by §7.4's Note and by §21.7's own Rationale). §21.7 therefore
licenses its absence from the register "by the clause's own terms". But its
overrun condition is detectable, so §21.1 requires a row and says its omission
is a defect. If a maintainer acted on §21.7's licence and dropped L23, L24 and
L26 — every row [R-CNT-18] governs — §21.1 would call the result a defect and
§21.7 would call it correct. Both sentences are normative.
This is a repair-introduced collision. Before hunk 07 and hunk 09, "detectable"
had no stated extension, and §21.1's opening sentence was a soft claim about a
term the document did not define. The repair pinned the term, and in pinning it
made the untouched opening sentence falsifiable. That is precisely the
"sentence written to be true only under the old wording" shape.
REPAIR: adopt B-01's per-condition individuation and say "an unwitnessed
CONDITION is absent from it by the clause's own terms"; a requirement's
unwitnessed conditions then license nothing about its detectable ones.
BYTE-LEVEL: NO. Applying the discriminating question: the disputed artifact is
the document, not a file. Under both readings L23/L24/L26 stand in the register
as written, [R-CNF-04] binds readers to them, and a file with an inline-payload
overrun is reject-layer either way. Nothing a writer may emit and nothing a
reader must reject moves.

### B-03  NEW_AMBIGUITY — hunk 08's word swap makes §21.1 deny reach to the very
thing §21.1 turns on
§21.1 (hunk 08) against §21.7 (hunk 09).
QUOTE (§21.1): "The subsections after §21.5 are not part of the register and
carry no rows: neither this completeness clause nor the instance arithmetic
below reaches §21.6's defined non-violations, §21.7's **test** for what no check
detects, or §21.9's limits."
AGAINST (§21.7): "this is the gate `[R-CNF-07]` applies in assigning an outcome
and **§21.1's completeness clause turns on**".
Hunk 08 replaced "§21.7's account of what no check detects" with "§21.7's test
for what no check detects". Under the old noun the sentence was innocuous: the
completeness clause does not reach §21.7's *account*, i.e. §21.7 supplies no
rows. Under the new noun the same sentence says the completeness clause does not
reach §21.7's *test* — while §21.7 says the clause turns on that test. "Reaches"
is meant in the row-carrying sense, and the parallel items (§21.6's entries,
§21.9's limits) support that reading, but the repair chose the one word that
makes the sentence collide with its counterpart. This is exactly the kind of
one-word substitution that lands in text nobody re-read around.
REPAIR: "...nor the instance arithmetic below carries rows into §21.6's defined
non-violations, §21.7's subject, or §21.9's limits" — or restore a noun that
names the section's content rather than its criterion ("§21.7's subject").
BYTE-LEVEL: NO. No file's status turns on which of §21.1's two senses of
"reaches" a reader picks.

### B-04  CHECK-8 — "A second set" lost its antecedent to three inserted
paragraphs
§21.7, first sentence of the new Rationale block's body.
QUOTE: "A second set of obligations is omitted from the register because a
single file exhibits no witness of their violation."
Before the repair, this sentence stood immediately after "None of these is a
requirement a verifier is *unable to check* within the meaning of
`[R-CNF-11]`: no file-level witness exists to check, so nothing about the file
is left undetermined and the verdict is unaffected." — i.e. immediately after
the FIRST set (mis-strided filter, undisclosed dictionary, wrong data), which is
what "second" counted from. The repair inserted three paragraphs between them,
each of which introduces a set of its own: unwitnessed requirements, detectable
violations, and requirements no file can violate. "A second set" now resolves to
the nearest preceding set, which is either "requirements no file can violate"
(making the sentence say the wrong thing) or "unwitnessed requirements" (making
it circular: a second set of obligations omitted because no file witnesses them,
where the immediately preceding paragraph has just defined exactly that class).
Neither reading is the intended one. The referring sentence did not change a
word, so no diff shows it.
REPAIR: "Beyond the content-wrongness of the opening paragraph, these
obligations are omitted from the register because a single file exhibits no
witness of their violation." — naming the antecedent instead of counting to it.
BYTE-LEVEL: NO. The block is labeled Rationale and carries no force; and its
own priority clause sends any disagreement to the test.

### B-05  UNSWEPT_RESTATEMENT — §7.4's Note still states the superseded
reader-capability criterion
§7.4 closing Note (line 1169), non-normative.
QUOTE: "The nesting prohibition binds writers and any type a later version
registers; in format major 1 it has no reader-detectable witness, and so no
register row. Detecting nesting means parsing a sub-record's payload as records,
which a reader does only where this specification defines that payload as a
record sequence".
AGAINST (§21.7, normative): "a violation this specification names is
**detectable** exactly where some file exhibiting it differs, in its live state,
from every file that does not."
The §7.4 Note derives "no register row" from what a READER does. The repair
replaced that criterion with one about live states, which says nothing about
reader behaviour: a verifier may parse whatever it likes ([R-CNF-12]: "a reader
MAY reject it upon detecting any violation"), and whether a sub-record's payload
contains records is a fact about the bytes. So under the new test the derivation
in §7.4's Note no longer follows, and the Note is the one place a reader is told
WHY that prohibition has no row. The repair generalised §21.7 into a test that
"decides any requirement put to it without appeal to a list" and did not sweep
the restatements that decide it the old way.
Same shape, weaker: §21.7's own Rationale keeps "opaque by construction"
([R-CNT-13]) and "detectable only by parsing a payload no format-major-1 reader
parses" ([R-CNT-18]) — both capability grounds, not live-state grounds. The
Rationale's priority clause ("where an item here and the test above disagree,
the test governs, and an item found stale is a defect in this block") absorbs
those two, but it cannot reach §7.4's Note, which sits in another section.
REPAIR: restate §7.4's Note on the test's own terms — "a payload this
specification does not define as a record sequence carries no obligation a
file's live state distinguishes, so §21.7 places the prohibition outside the
register" — or delete the "and so no register row" inference and let §21.7
carry it.
BYTE-LEVEL: NO. Both sentences sit in Note-labeled blocks and neither creates or
removes a register row.

### B-06  UNDERSHOT / TENSE_QUANTIFIER — the repair generalised the class and
left the [R-CNF-11] disclaimer pinned to the old one, then introduced
"establish"
§21.7 ¶1 (untouched) against §21.7 ¶3 (hunk 09).
QUOTE (¶3): "Being unwitnessed bears on detection and not on permission: the
requirement binds its actor as any other does, and the outcome classes of §2.4
are assigned to violations a reader or verifier **can establish** rather than to
every violation this document names."
AGAINST (¶1, untouched): "**None of these** is a requirement a verifier is
*unable to check* within the meaning of `[R-CNF-11]`: no file-level witness
exists to check, so nothing about the file is left undetermined and the verdict
is unaffected."
Two problems, both from the repair.
(1) The restatement's quantifier does not match the rule it restates.
[R-CNF-07] reads "Every **detectable** file-conformance violation named by this
specification is assigned exactly one reader outcome". §21.7 restates it as
violations "a reader or verifier can establish" — one sentence after defining
"detectable" as a property of live states that says nothing about any actor's
capability. The two sets come apart for any violation the bytes determine but
no defined check reaches, which is most of §21.7's Rationale list. §21.7 also
drops [R-CNF-07]'s "file-conformance" qualifier, widening the restatement to
writer- and updater-only obligations.
(2) "Establish" is this document's term of art for the verifier verdict:
[R-CNF-11] pairs it with "*cannot establish*" and "a verifier MUST NOT certify a
file it reports that way". ¶1 exists precisely to bar that inference — but its
"None of these" is anchored to ¶1's own list, and the repair generalised that
list into a defined class (all unwitnessed requirements) without generalising
the disclaimer. So the section now defines a class, tells the reader that
outcome classes go only to what an actor "can establish", and leaves the
[R-CNF-11] carve-out covering only the three examples in ¶1.
REPAIR: (a) say "assigned to detectable violations, as just defined, rather than
to every violation this document names", so the restatement uses the term it
just defined and matches [R-CNF-07]; (b) move ¶1's disclaimer down and
generalise it: "No unwitnessed requirement is one a verifier is *unable to
check* within the meaning of `[R-CNF-11]`: there is no file-level witness to
check, so nothing is left undetermined and the verdict is unaffected."
BYTE-LEVEL: NO — but only because [R-CNF-11] independently confines *cannot
establish* to "a capability or resource ground", which unwitnessedness is not.
I considered whether two verifiers could fork on the same bytes — one certifying
and one reporting *cannot establish* on [R-LIF-01] — and [R-CNF-11]'s own words
close it. Had that qualifier been absent, this would fork a verdict.

## 12. Candidates opened and closed

  - §21.7's Rationale says §20.5 has "three obligations" while §20.5 says
    "Neither obligation has a witness". CLOSED: §20.5 states three in total
    (fresh file_id, ignore-lane bits, version_minor); "Neither" scopes to the
    two in its own paragraph. No conflict.
  - The disk-ordinal bar vs. hunk 01's "reaches neither a shrink nor a growth",
    given that the same block says growth renumbers disk ordinals. CLOSED: the
    bar's antecedent is a channel-declaration change; a growth is a geometry
    change, and §20.3 assigns the renumbering to the re-emission rule expressly.
    Also worked the combined grow-and-append-a-channel case; still not barred.
  - Hunk 01's re-typing sentence drops the "superseded generation" tense.
    CLOSED: §20.3's normative sentence uses the identical present-tense wording
    and disambiguates two sentences later; not repair-introduced.
  - Citations C3 and C4 now point at material inside a non-normative Rationale.
    CLOSED: both citing sites assert the fact normatively themselves and cite
    §21.7 only for explanation.
  - "That is the whole of the test, and it decides any requirement put to it" —
    tested against history-shaped obligations ([R-LIF-01], [R-WRT-06]) that no
    file "violates". CLOSED, narrowly: the following gloss ("ask whether the
    breach can be made to leave the live state ... exactly as a conforming
    commit would leave it") is act-shaped and covers them.
  - Whether the demotion of the enumeration into a Rationale orphaned a rule
    relied on normatively elsewhere. CLOSED: I traced both §21.7 citations that
    point into the moved block (C3, C4) and both are backed at the citing site.
  - [R-CNF-12]'s "the MUST-level conditions §21 inventories" as a surviving
    old-shape word. CLOSED: it characterises the register, not §21.7, and
    predates this commit's subject.
  - §21.8's "120 conditions over 275 instances". NOT CHECKED — outside my
    charter and outside every hunk I hold; I did not recount it and make no
    claim about it.

## 13. Per-check verdicts

  check 1 (tense/quantifier): FAILED at hunks 07+09 -> B-01, B-06.
                              PASSED at hunk 01 (all four restatements).
  check 2 (citations resolve): PASSED everywhere. 13 identifiers and 9 section
                              numbers opened; every one says what the citing
                              sentence claims. The only slippage is
                              [R-CNF-07]'s dropped "file-conformance", folded
                              into B-06.
  check 3 (label not marker):  PASSED. Applied the LABEL test throughout; both
                              §21.1 landings and §21.7's definition are
                              unlabeled plain prose and therefore normative;
                              hunk 01 and the moved walk-through are labeled
                              Rationale and therefore not. No rule was orphaned.
  check 4 (contradiction in passage): FAILED -> B-02, B-03.
  check 5 (exhaustive claims):        FAILED -> B-01. Six other exhaustive
                                      claims tested and passed (§9).
  check 6 (what is left unconstrained): FAILED -> B-06 (the [R-CNF-11]
                                      disclaimer not generalised with the
                                      class). Hunk 01's sibling quantity is
                                      governed by §20.3.
  check 7 (analogy quantifiers):      FAILED once -> B-06. Three other
                                      analogies compared verb-for-verb and
                                      passed, including the two-member one.
  check 8 (insertion effects):        FAILED -> B-04. Fourteen back-references
                                      resolved and reported in §6; thirteen
                                      unaffected, one broken. The repair itself
                                      pre-empted one anaphor break ("the bar" ->
                                      "the §14 bar"), which I credit.
