# Audit — lane "downstream-accounts"
# Charter hunks: hunk-01, hunk-07, hunk-08, hunk-09
# Subject: everything outside §21.7 that depends on §21.7

## 0. Disclosure

Read (files opened):
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-01.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-07.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-08.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-preaudit/case/hunk-09.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (portions listed below)

Nothing else. No docs/, no conformance/, no registry.json, no git, no web,
no full.diff, no other hunk file, no directory listing of the case dir.

Files I wrote: this transcript only. My scratch directory
.../scratch/downstream-accounts/ was created but I needed no working file
(all computation was quantifier bookkeeping done in-head and re-checked by
re-reading the text; no CRC or arithmetic script was required).

Unrequested context that appeared before I began: a CLAUDE.md pointer to
AGENTS.md, and an index of the maintainer's auto-memory naming several
project notes (working cadence, prior verifier-failure shapes, a note about
§21 and a corpus build list, and a naming constraint). I did not open any of
it and I did not use any of it. I name its appearance here as the access
rule requires; I do not repeat its contents. No conclusion below was
suggested by it — every finding is anchored to a line number in tarn.md
that I quote.

Spec passages read in full:
- §2.1 / [R-CNF-01] (lines 95-115)
- §2.2 definitions [R-CNF-02], [R-CNF-04..07], [R-CNF-11] (155-215, 235-260)
- [R-CNF-13] and its Note (260-285)
- §2.4 outcome classes / [R-CNF-07] (285-300)
- §7.4 closing Note on nesting (1160-1180)
- §7.2 [R-CNT-17] (1095-1115)
- §9.7 coverage verification / [R-LIF-08] (1440-1490)
- §11.1 in full incl. the repaired Rationale (1584-1660)
- §11.2 (grid arithmetic), §12/§13 [R-GEO-06] (1690-1712)
- §17.2 codec 3 zstd (2405-2425)
- §17.3 byte-shuffle / [R-COD-10] (2500-2525)
- §18.x user-metadata encoding 2 / R4 passage (2595-2625)
- §20.3 step 4 in full (3120-3270)
- §20.5 compaction (3425-3470)
- §21.1 in full (3545-3625)
- §21.2 header + rows F1-F22 (3625-3680)
- §21.4 row T26 (3774)
- §21.6 in full (3835-3864)
- §21.7 in full, post-repair (3864-3995)
- §21.8, §21.9 opening (3995-4012)

## 1. The rules the repairs adopt (my words)

**hunk-01 (§11.1 Rationale, non-normative).** Makes true of no
implementation directly — it is a labelled Rationale. What it asserts about
the document: §20.3 step 4 contains exactly two bars on a declaration
change; the one that bears on a shrink or a growth is the §14 bar; the
other bars only a channel-declaration change that moves a stored tile's
disk ordinal, and reaches neither a shrink nor a growth. It also restates
the empty-layer permission in the superseded generation's tense and adds
that a layer the commit itself empties does not qualify, and pins re-typing
as the §14 bar's own subject.

**hunk-07 (§21.1 completeness clause, normative).** Makes true: the gate on
which the register's normative completeness turns is now spelled out in
§21.1 itself — a violation is detectable exactly where **some file
exhibiting it differs, in its live state, from every file that does not** —
and attributes that test to §21.7.

**hunk-08 (§21.1, normative).** Renames what §21.7 is, from "account of
what no check detects" to "test for what no check detects", for the purpose
of saying the completeness clause and instance arithmetic do not reach it.

**hunk-09 (§21.7).** Two things at once. (a) It replaces a list with a
general normative test: a condition is *unwitnessed* where for every file
exhibiting it some non-exhibiting file cannot be told apart from it by any
check the specification **obliges** a reader or verifier to perform, and
*detectable* in the contrary case; the register carries a row exactly where
detectable; the subject is the condition, not the requirement; and a
requirement stating no condition a file can exhibit ([R-ENC-06]) is a third
thing again. (b) It moves the whole former enumeration of unwitnessed
obligations into a blockquote **labelled Rationale**, i.e. out of normative
force, adding a disclaimer that the test governs where the walk-through
disagrees, and splitting §20.3 step 4's single "bar on a declaration
change" into "the §14 bar" and "its companion bar on a planar layer's disk
ordinals".

## 2. Normativity test applied (check 3) — by LABEL, not by ">"

| Passage | Marker | Opening words | Verdict |
|---|---|---|---|
| §21.1 completeness clause (3556-3566) | no ">" | plain prose; text says "Its **completeness is normative**" | NORMATIVE |
| §21.1 second §21.7 reference (3578-3581) | no ">" | plain prose | NORMATIVE |
| §21.7 opening paragraph (3866-3880) | no ">" | "Stated plainly, because a register invites…" | NORMATIVE |
| §21.7 new test paragraphs (3882-3919) | no ">" | plain prose | NORMATIVE |
| §21.7 moved enumeration (3921-3992) | ">" | "> **Rationale.** The obligations this test places outside…" | NON-NORMATIVE by [R-CNF-01] |
| §11.1 block (1602-1628) | ">" | "> **Rationale.** Empty layers serve schema-first workflows" | NON-NORMATIVE by [R-CNF-01] |
| §7.4 nesting block (1169-1177) | ">" | "> **Note.**" | NON-NORMATIVE |
| §21.6 table + closing prose | no ">" | plain prose/table | NORMATIVE |
| §20.3 step 4 (3141-3245) | no ">" (numbered list) | plain prose | NORMATIVE |
| §20.5 (3425-3462) | no ">" | plain prose | NORMATIVE |

I applied the label test, not the marker test, everywhere. The §21.7
restructure's entire effect is a label question: the enumeration did not
change force because it acquired ">", it changed force because it acquired
"**Rationale.**".

## 3. Every citation of §21.7 in the document

Grep run (line-oriented is safe here — "21.7" never wraps):

    $ grep -n "21\.7" spec/tarn.md
    2521, 2613, 3240, 3457, 3560, 3580, 3774, 3864(heading)   -> 7 citations

I also re-ran the search on a whitespace-normalised copy of the whole file
in Python (re.sub(r'\s+',' ')) and printed ±500 chars around each "§21.7";
same 7 sites, no wrapped occurrence missed.

**(a) 2521, §17.3 [R-COD-10] byte-shuffle.** Cites §21.7 for: wrong sample
content resulting from a wrong stride, where no structural obligation is
broken, is "undetectable by construction". §21.7 still says this, in its
**opening paragraph**, which is normative and untouched by hunk-09
("this format detects *corruption of structure*, not *incorrectness of
content*… a mis-strided filter (`[R-COD-10]`)"). **PASS**, and the landing
sentence carries force.

**(b) 2613, §18 encoding 2 / R4.** Cites §21.7 for: undisclosed dictionary
use is a writer violation nothing in the extent shows, "exactly as
[R-COD-06] has it for a tile". §21.7's opening paragraph still names "an
undisclosed compression dictionary (`[R-COD-06]`…)". **PASS**; normative
landing. Check 7 on the analogy: the citing verb is "shows" ("nothing in
the extent **shows**") against §21.7's "every checksum in §8 **certifies**"
and the new test's "**separated by** such a check". All three range over
what an obliged check can distinguish; the frame case and the tile case are
individuated the same way (one compressed stream whose header omits the
dictionary flag). Analogy sound.

**(c) 3240, §20.3 step 4.** "§21.7 records the consequence — that this is
precisely where the §14 bar has no witness, the live state being clean".
§21.7 still records that a commit superseding every tile it would have
damaged leaves the §14 bar unwitnessed — but only in the **Rationale
block** now (3983-3986), and §21.7 now says explicitly that this is *not*
the only place the §14 bar is unwitnessed. See finding B-03. **FAIL on the
exhaustive quantifier; the underlying fact still holds.**

**(d) 3457, §20.5 [R-WRT-06].** "Neither obligation has a witness in the
output alone (§21.7)." The two obligations are the ignore-lane carry-forward
MUST and the version_minor SHOULD floor. §21.7 still says so — in the
Rationale block (3987-3992): "…are unwitnessed for a reason all three
share: the output carries no record that it is a compaction output at all…
For the last two there is a second, the output carrying no record of its
input's flags or its input's minor either." **PASS.** Count check: §21.7
says *three* obligations, §20.5 says *neither* (two). Not a conflict —
§20.5's sentence sits after the two paragraphs stating exactly those two,
and the third (fresh file_id) is carried normatively by §20.5's own earlier
sentence ("nothing in the output's trailer records that it is a first
committed state — no field counts commits"). Normative force for §20.5's
claim comes from §20.5's own sentence; the §21.7 pointer is a pointer.

**(e) 3560, §21.1 completeness clause.** Cites §21.7 as *stating the test*
and then glosses the test. The gloss is not §21.7's test. Finding B-01.
**FAIL.**

**(f) 3580, §21.1.** "§21.7's test for what no check detects" — accurate
description of §21.7's new shape (§21.7 now states a test, headed "What no
check detects"). **PASS.**

**(g) 3774, §21.4 row T26.** "(a wrong stride with no such structural
constraint is undetectable, §21.7)". Supported by §21.7's normative opening
paragraph. **PASS** — and this row is one of the texts B-01 collides with.

## 4. hunk-07 — §21.1's completeness clause against §21.7 (the charter's
   first named task)

Side by side, verbs and quantifiers verbatim.

§21.1 (3560-3563), normative:
> "a violation is detectable exactly where some file exhibiting it
> **differs, in its live state,** from every file that does not"

§21.7 (3885-3888), normative:
> "It is **detectable** in the contrary case: where some file exhibiting it
> **is separated by such a check** from every file that does not."
where "such a check" = (3882-3885) "any check this specification obliges a
reader or a verifier to perform".

The governing predicates are **"differs, in its live state"** against
**"is separated by such a check"**. The existential/universal skeleton
(∃f∈E, ∀g∉E) is identical in both; what §21.1 drops is the **instrument**.
§21.7 makes the instrument load-bearing on purpose, one paragraph later
(3896-3902): "The instrument is the checks this specification obliges an
actor to perform, and deliberately not the register's own rows".

Falsification, from the document:
- A file whose tile was filtered at a wrong stride with no structural
  constraint broken *differs in its live state* from every correctly
  filtered file — its stored bytes are different bytes. Under §21.1's
  gloss it is therefore **detectable**, so the register omitting it is
  "a defect in this document". §21.7's opening paragraph and row T26 both
  say it is undetectable and rightly unregistered.
- Same for undisclosed dictionary use ([R-COD-06]; §18's R4 passage at
  2610-2613 says "R4 registers neither").
- Same for [R-CNT-18] nesting: §7.4's Note (1170-1171) says "in format
  major 1 it has no reader-detectable witness, and so no register row."
  A nested sub-record's payload bytes differ in the live state from a
  non-nested one's.

So §21.1's normative completeness clause now declares the register
defective for three omissions the rest of the document says are correct.
Finding B-01.

Secondary, opposite-direction observation folded into B-01: §21.1 also
*adds* "in its live state", a qualifier §21.7's test does not contain. I
looked for a register row this would wrongly exclude — a condition whose
only witness is outside the live state — and could not confirm one:
- F7 (a structure between the live directory's end and the live trailer):
  the claimants are live-state members and their placement is declared in
  live records, so two files differing on F7 differ in live state. Not a
  counterexample.
- F17 (committed_file_length vs physical size): the trailer's position is
  fixed at F−64, so the live state's byte ranges differ. Not clean.
- Slack content is expressly unconstrained (§21.6, [R-CNT-21]), so no row
  turns on it.
I therefore report the addition as an unwarranted divergence rather than
as a second falsified claim.

## 5. hunk-08

"§21.7's account of what no check detects" -> "§21.7's test for what no
check detects". Accurate post-repair. **PASS.** Check 4 on the sentence it
sits in: "The subsections after §21.5 are not part of the register and
carry no rows: neither this completeness clause nor the instance arithmetic
below reaches §21.6's defined non-violations, §21.7's test…, or §21.9's
limits." This sentence is the one §21.7's new "The register carries a row
for a condition exactly where it is detectable" collides with — see B-02.

## 6. Sweep for the old shape (charter task 3)

    $ grep -n -i "account"    -> 773, 785, 891, 2879, 3918, 4135, 4492
    $ grep -n -i "inventory"  -> 2823, 4009
    $ grep -n -i "catalog"    -> 0 hits
    $ grep -n -i "roster"     -> 0 hits
    $ grep -n -i "the list"   -> 3146, 3211, 4225, 4510
    $ grep -n -i "a list"     -> 3897
    $ grep -n -i "enumerat"   -> 22 hits (listed in my notes)
    $ grep -n -i "collects"   -> 1494, 4007

Each hit checked against what §21.7 now is:
- 3918 "omitted from the register on its account" — the idiom "on its
  account" (= because of it), not "an account of". Not stale.
- 773/785/891/2879/4492 — §6.4 request *accounting*. Unrelated.
- 4135 "accounted for" — §22-ish prose on slack. Unrelated.
- 2823 "enumerations are not the complete inventory of what a reader…" —
  about §19.2 reader checks, not §21.7.
- 4009 "a finding aid rather than an inventory" — §21.9's self-description,
  correct and about §21.9.
- 3897 "without appeal to a list" — this is §21.7's own new text disavowing
  the list shape. Correct.
- 3547/3856 "the register enumerates…" — about §21.2-§21.5, correct.
No stale characterisation of §21.7 as an account, inventory or list
survives. **Sweep clean.**

## 7. hunk-09 — the checks

**Check 1 (tense/quantifier).** The new test quantifies over files, not
generations, so the generation trap does not arise in the test itself. It
does arise in the moved block, and the move handled it correctly: the old
opener "A **second** set of obligations is omitted…" (an ordinal anaphor to
the first set, the content wrongness of the opening paragraph) became
"Beyond the content-wrongness this section opens with, these obligations
are omitted…". That is the check-8 repair done right, and I record it as a
pass. The "§14 bar" disambiguations inside the block ("so the **§14 bar**
is unwitnessed there", "§20.3 step 4's **§14 bar**") likewise track §20.3's
new two-bar vocabulary.

**Check 2 (citations in the repaired text).**
- `[R-CNF-07]` (3890): "Every detectable file-conformance violation named
  by this specification is assigned exactly one **reader outcome**" (286-288).
  §21.7's claim — detectability "is the gate [R-CNF-07] applies in assigning
  an outcome" — **PASS**.
- `[R-CNF-13]` (3905), cited for individuating conditions: "A **condition**
  this specification names — one malformed state, as §21.1 individuates
  them, and not the requirement that defines it" (260-262). **PASS on the
  words**, but see B-04: the chain terminates in §21.1's rows.
- `[R-CNT-06]` "shows by stating nine" (3905-3906): [R-CNF-13] says
  "`[R-CNT-06]` states nine, of which the trailer magic and the trailer CRC
  assert invariants `[R-CNT-24]` fixes and the other seven do not"
  (2 + 7 = 9, arithmetic checks). **PASS.**
- `[R-ENC-06]` (3914): cited for fixed field widths. Consistent with the
  claim that no file state corresponds. **PASS** (unchanged claim, merely
  relocated out of the deleted paragraph into normative prose — note this
  one item was *kept* normative while its neighbours went to Rationale,
  which is the right call since it is the one item that states a rule about
  the register rather than an example of one).
- `[R-ERR-01]` (3919): still terminates a normative paragraph of §21.7, as
  before. **PASS** — the section's requirement tag did not fall inside the
  Rationale block.
- `[R-CNF-11]` (3879): opening paragraph, untouched. **PASS.**
- §2.4 (3909): outcome classes. **PASS.**
- Inside the Rationale: §9.7, §7.4's closing Note, §14.5, §14.3, §12.1,
  §17.3, [R-SER-08], T2/T3/T4/T5/T14/T15/T17/T23/T25/T26, [R-LIF-01/02],
  [R-GEO-06], [R-SER-01], [R-CNT-13], [R-CNT-18], [R-WRT-06]. I spot-checked
  §9.7 ("A verifier checking [R-CNT-02]'s partition walks the live state
  only… Nothing here enumerates prior commits"), §7.4's Note (1169-1177),
  T26 (3774) and §12.1's element sizes claim via §14.5/§14.3. All resolve.
  These sit in non-normative text and so cannot mis-bind an implementation.

**Check 3.** Applied by label above. The moved block is labelled
**Rationale.** and therefore non-normative. This is deliberate — the block
says so — and the load-bearing question is whether any *rule* now lives
only there. I looked: the block contains no MUST/MUST NOT/SHOULD/MAY and no
requirement identifier of its own; every obligation it discusses is stated
normatively in §20.3, §20.5, §17.3, §7.4 or the requirement cited. The
facts §20.3 and §20.5 draw from it are each also asserted in normative text
at the citing site. **No rule lost force.**

**Check 4 (contradiction in the same passage, including untouched text).**
- Against §21.7's own opening paragraph: no contradiction. The opening's
  content-wrongness class satisfies the new definition of unwitnessed.
- Against §21.6: "The register carries a row for a condition **exactly
  where** it is detectable" (3891-3892) omits the qualifier *file-conformance
  violation* that §21.1 (3547-3548, 3558) and §21.6's own closing prose
  ("the register enumerates file-conformance violations (§21.1)") both
  carry. §21.6's table holds plainly detectable conditions with no row —
  "An ignore-lane flag bit (16-31) is set", "A dimension has extent 0",
  "version_minor is higher than this text defines". Under the unqualified
  sentence each of those should have a row. Finding B-02.
- Against §21.1's hunk-08 sentence: direct — §21.1 says the completeness
  clause does not reach §21.6's defined non-violations; §21.7's new
  biconditional reaches them.

**Check 5 (exhaustive claims in the repaired text).** Enumerated:
- "the whole of the test" (3893) — supported; the paragraph names the
  instrument and the subject and disavows a list.
- "any condition put to it" (3893) — see B-04 on granularity.
- "each is exactly the negation of the other" (3889-3890). I checked the
  arithmetic. Unwitnessed = ∀f∈E ∃g∉E ∀c ¬sep(c,f,g). Its negation =
  ∃f∈E ∀g∉E ∃c sep(c,f,g). Detectable as written = "some file exhibiting
  it is separated by such a check from every file that does not" — which is
  ∃f ∀g ∃c under a distributive reading and ∃f ∃c ∀g under a collective
  one. Under the distributive reading the claim is exactly right. I
  considered filing the collective reading as an ambiguity and rejected it
  (see rejected candidates).
- "exactly where it is detectable" (3891) — the biconditional. Finding B-02.
- "deliberately not the register's own rows" (3898) — supported by the
  vacuity argument given.
- "as [R-CNT-06] shows by stating nine" — a count, verified against
  [R-CNF-13].
- "the outcome classes of §2.4" — §2.4 lists reject-file, reject-layer,
  reject-tile, ignore-record (4) plus preserve-verbatim (an updater
  obligation, expressly "orthogonal to reader outcomes"). §21.7 does not
  count them, so no miscount.
- Inside the Rationale: "the two of §10.1's four vehicles" is §20.5's, not
  §21.7's; "all three share" — verified against §20.5's three obligations.

**Check 6 (what the repair left unconstrained).** The structure §21.7 now
governs is the *classification of every condition this document names*.
Its members: (i) detectable conditions (rows), (ii) unwitnessed conditions
(no row, correctly), (iii) requirements stating no condition a file can
exhibit ([R-ENC-06]), (iv) conditions that are not violations at all
(§21.6), (v) conduct rules that never bear on bytes ([R-CNF-02]: §10.3 and
§18.3 publication/registry-targeting), and (vi) requirements a verifier is
*unable to check* on a capability or resource ground ([R-CNF-11]).
The repair fixes (i), (ii) and (iii) and expressly separates (vi) in the
opening paragraph. It does **not** fence (iv) or (v): the new biconditional
at 3891-3892 ranges over "a condition" without the violation qualifier, so
(iv) falls inside it wrongly (B-02), and (v) — a conduct violation exhibits
no file state at all, so it is vacuously "unwitnessed" under 3882-3885 and
the reader is left to work out that [R-CNF-02] already removes it from
scope. (v) is the sibling quantity left unpinned; it is milder than (iv)
because [R-CNF-02] is explicit that a file is never nonconforming by virtue
of a conduct rule, so nothing turns on it. I name it here rather than
filing it.

**Check 7 (analogy / warrant).** Three warrant-pointers in the repaired
normative text:
- "as `[R-CNF-13]` individuates them" (3905). Repair's verb: "The subject
  is the condition and not the requirement". Cited rule's verb: "one
  malformed state, **as §21.1 individuates them**, and not the requirement
  that defines it". Both range over conditions, so the surface match is
  exact — but the cited rule's own warrant is §21.1, whose individuation is
  "each row is one malformed condition" (3548-3549), i.e. by row. Finding
  B-04.
- "as `[R-CNT-06]` shows by stating nine" (3905-3906). Repair's verb:
  "states several"; cited rule's verb: "states nine". Same set (the
  conditions one requirement states). **Analogy sound.**
- "detectability so stated is the gate `[R-CNF-07]` applies" (3889-3890).
  Repair's verb: "is separated by such a check"; [R-CNF-07]'s verb: "Every
  **detectable** file-conformance violation … **is assigned** exactly one
  reader outcome". [R-CNF-07] does not itself define detectable, so §21.7
  is supplying the definition rather than borrowing one. **Sound**, and it
  is precisely this supplied definition that §21.1 then mis-glosses (B-01).
- In §17.3/§18 the analogy "exactly as `[R-COD-06]` has it for a tile"
  (2612-2613) — checked at §3(b) above, sound.
- In §11.1's Rationale: "exactly as above" is §20.3's, not this block's.

**Check 8 (what the insertion did to the sentences around it).** Run both
directions, on both inserting hunks.

*hunk-09, forward.* Back-references from the insertion to the end of §21.7:
- "That is the whole of the test" (3893) — "That" resolves to the
  unwitnessed/detectable definition immediately above. Before the repair
  the sentence did not exist. **OK.**
- "the gate `[R-CNF-07]` applies" / "§21.1's completeness clause turns on"
  (3889-3891) — explicit referents. **OK.**
- "that clause's own terms" (3892) — nearest antecedent is "§21.1's
  completeness clause" two lines above, not "the register". **OK.**
- "It is **detectable** in the contrary case" (3885) — "It" = "A condition
  this specification names". **OK.**
- "The two are stated over the same subject" (3888) — the two definitions.
  **OK.**
- "Being unwitnessed bears on detection and not on permission" (3907) —
  "unwitnessed" as defined at 3882. **OK.**
- "there being no condition to omit" (3918-3919) — [R-ENC-06]. **OK.**
- Rationale: "where an item here and **the test above** disagree" (3924) —
  candidates between the Rationale and the definition are P4 ("The subject
  is the condition…") and P5 ("Distinguish an unwitnessed condition…").
  Neither is called a test; the nearest thing named "test" is 3893's "That
  is the whole of the test", pointing at the definition. **Resolution
  unchanged and correct.**
- Rationale: "Its companion bar" (3949) — "Its" = §20.3 step 4's §14 bar,
  named in the immediately preceding sentence. **OK**; this is new text
  written for the new two-bar vocabulary.
- Rationale: "for the same reason no check knows which ordinal a stored
  tile used to occupy" (3950-3951) — "the same reason" points at "the prior
  generation's declarations are not part of the live state". **OK.**
- Rationale: "so the **§14 bar** is unwitnessed there" (3985) — the repair
  replaced a bare "the bar", which after §20.3's split would have been
  ambiguous between the two bars. **A check-8 hazard correctly closed.**
- §21.8, the next section, opens "Every row of §21.2 through §21.5 — 120
  conditions over 275 instances —" with no anaphor back into §21.7. **OK.**

*hunk-09, backward.* Does the inserted text lean on an antecedent further
away than a reader will look? "Beyond the content-wrongness this section
opens with" reaches back over four intervening paragraphs to the opening —
but it names it ("this section opens with") rather than pointing. **OK.**

*hunk-01, forward.* The insertion sits between "One shrink can do several
of these at once." and "Growth that leaves **entry_count** unchanged…".
Back-references after it:
- "Growth that changes entry_count changes extent_length with it" — "it"
  = entry_count, in-sentence. **OK.**
- "so **the layer's** whole tile-index region is re-emitted" (1624-1625).
  Before the insertion the nearest "layer" was "A layer that stored nothing";
  now it is "a **planar** layer's channel declarations". The definite
  article could be read as narrowing the sentence to planar layers.
  Considered and rejected as a finding: the sentence's subject is "Growth
  that changes entry_count", a generic, and the block is non-normative
  Rationale whose governing text (§20.3 step 4, 3120-3128) states the
  re-emission rule for any layer.
- "disk ordinals renumber wherever `[R-GEO-06]` moves them" (1625-1626) —
  "them" = disk ordinals, in-sentence. The insertion did place a sentence
  about a *barred* ordinal move immediately before a sentence about a
  *permitted* renumbering. Considered and rejected: §20.3 (3178-3180)
  expressly separates them — the new bar is on **channel declarations**,
  while "the re-emission rule above, whose only stated occasion for a
  renumbering is a geometry change" covers growth. The adjacency is
  unfortunate, not wrong.

*hunk-01, backward.* "such a tile" (1606) — antecedent "a layer that
already stored tiles in the generation a commit supersedes", one sentence
back. **OK.** "Of its two bars" (1605) — "its" = §20.3. **OK.**

*hunk-07/08, insertion effects.* hunk-07 lengthens the completeness clause
between "detectability being the gate" and "— but each row *restates* its
governing rule". Back-reference audit: "each row" (3564) — rows of the
register, unchanged; "the same exception stated above" (3567) — resolves to
"except where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine
does" (3549-3551), which is above both the old and the new text and is
still the nearest exception. **Unchanged.** "the instance arithmetic below"
(3579) — the Instances paragraph at 3585ff. **Unchanged.**

## 8. hunk-01 — the remaining checks

**Check 1.** "A layer that stored no tile in the generation the commit
supersedes may be re-declared freely; a layer the commit itself empties
does not qualify." Normative rule restated (§20.3, 3200-3204): "A layer
that stores no tile **in the generation this commit supersedes** MAY be
re-declared freely… the tense is both bars', so a commit does not earn this
permission by emptying the layer as it re-declares it". Quantifier and tense
**match**, including the "does not qualify" clause.
"barred wherever the layer stores a tile that carries that channel, and
free where it does not" against §20.3 (3155-3168): "changing it is such a
change wherever the layer stores a tile that carries that channel… Where
the superseded generation stored no tile carrying that channel there is
nothing to reinterpret, and this bars nothing". **Match.**

**Check 5.** "Of its two bars" — a count. Verified: §20.3 step 4 states the
§14 bar (3141-3153, "Call this the **§14 bar**") and one other (3170-3176,
"One effect is barred beside it… a commit MUST NOT change the channel
declarations in a way that alters the disk ordinal"). §20.3's own text says
"the tense is **both bars'**". Count = 2. **PASS.**
"The other bar reaches neither a shrink nor a growth" — §20.3 states only
the shrink half ("The bar beside the §14 bar does not reach a shrink
either"). The growth half is the Rationale's own inference. It is sound:
the bar is on *channel declarations*, while a growth changes extents; and
§20.3 expressly contemplates geometry-driven renumbering as permitted. But
note the inference is drawn in non-normative text and not stated normatively
anywhere — I record it as an observation, not a finding, because §20.3's
bar text is unambiguous on its face about what it is a bar on.

**Check 2 (citations).** §20.3 — resolves. §14 / §14.5 fill — resolves
([R-SER-05] fixes padding content). §11.2's ⌈Eᵢ / Tᵢ⌉ — resolves (1633ff).
[R-CNT-17] — "extent_length MUST equal entry_count × 20 + ⌈entry_count /
2¹⁶⌉ × 4… a mismatch, or an entry_count that does not equal the
geometry-derived addressed-tile count, is a validity error at layer scope"
(1105-1110). Supports "Growth that changes entry_count changes
extent_length with it". **PASS.** [R-GEO-06] — "The **disk tile ordinal**…
is s for an interleaved layer, and **c · N + s** for a planar layer"
(1700-1703). Supports both the renumbering claim and §20.3's "an
interleaved layer is unaffected". **PASS.** [R-WRT-04] — §20.3 step 6's
tag. **PASS.**

**Check 4.** Read the whole of §11.1 (1584-1628) and the whole of §20.3
step 4 (3120-3245). No carve-out in §11.1 collides with the new breadth;
the Rationale defers to §20.3 in its second sentence and every claim in it
is a narrowing restatement of §20.3, not a widening.

**Check 6.** The structure hunk-01's Rationale describes is *a commit's
permitted declaration changes for one layer*. Members: extent Eᵢ (shrink,
growth), tile extent Tᵢ, rank d, channel count C, channel order, channel
sample type, channel fill, layout, codec, filter, index_encoding, slab/
alignment declarations, name. The Rationale now covers shrink, growth,
re-typing, and channel reordering/insertion/removal. It says nothing about
**tile extent Tᵢ**, **layout**, **codec**, **filter** or **fill** changes —
but each of those is inside the §14 bar's own list at §20.3 (3143-3149:
"the set of padding positions… the decoded size, the byte offset of any
sample… the sample type… or the codec and filter"), and the Rationale
correctly says the §14 bar is "the whole of the test". So the silence is
covered by the governing rule it defers to. Fill is covered by §14.5 via
the padding-position clause. **Nothing left unconstrained by the omission.**

## 9. Findings filed

B-01 — §21.1's gloss of §21.7's detectability test drops the obliged-check
       instrument (CITATION, CONFIRMED, not byte-level)
B-02 — §21.7's "a row exactly where it is detectable" omits the
       file-conformance-violation qualifier (OVERCLAIM, CONFIRMED, not
       byte-level)
B-03 — §20.3's "precisely where the §14 bar has no witness" not swept
       against §21.7's now-explicit second unwitnessed case
       (UNSWEPT_RESTATEMENT, CONFIRMED, not byte-level)
B-04 — the test's subject-granularity is handed to §21.1, whose
       individuation is by row, while the instrument is expressly not the
       rows (NEW_AMBIGUITY, PLAUSIBLE, not byte-level)

## 10. Byte-level reasoning, applied once for all four

The discriminating question is whether the disputed file is itself
conforming and whether only one reading lets an actor produce it.

For B-01, B-02 and B-04 the disputed object is a *condition's
classification*, which decides (a) whether this document is defective for
omitting a row and (b) whether [R-CNF-07] assigns an outcome. Neither
moves the emittable set: file conformance is "a pure predicate on bytes"
([R-CNF-02]/[R-CNF-05] at 155-160, 200-202) and does not depend on
detectability, so [R-CNF-05] bars a conforming writer from emitting a
file with a mis-strided filter, an undisclosed dictionary or a nested
sub-record under **both** readings. Nor does a verifier's verdict fork:
under the wide reading the extra conditions still have no register row and
no obliged check, so a verifier that cannot establish them reports the same
thing either way. **Not byte-level.**

For B-03 the disputed object is where a rule is *stated*, not what any file
may be; §20.3's bar binds identically under both readings. **Not
byte-level.**

I record this as a deliberate non-inflation. The charter warns that a prior
round's "editorial" group hid a byte-level defect, so I tested each finding
against a concrete pair of files (wrong-stride tile, nested sub-record,
re-typed int8/uint8 channel with the tile still stored, compaction output
with a carried ignore-lane bit) and asked which bytes two implementations
would disagree about. In each case the disagreement is about a sentence in
this document, not about a byte or a verdict.
