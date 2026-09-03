# Repair audit: hunk-03 and hunk-04 (§21.1 / §21.7 detectability test)

## Disclosure

Files read: the two charter-named hunk files
(`case/hunk-03.diff`, `case/hunk-04.diff`), and the specification
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
at the lines the hunks land on plus their surrounding subsections
(§2.4 around line 286; §21.1 in full, lines 3546-3632; §21.5 in full,
lines 3780-3814; §21.6 in full, lines 3814-3868; §21.7 in full, lines
3868-4003; §21.8, lines 4003-4009; and spot checks at lines 692-753,
1170, 2416-2418, 2500-2530, 2600-2625, 3778, 3947-3997 found by grep).
Commands run: `sed -n` reads of those ranges, and `grep`/`tr`-normalized
searches listed verbatim under "Sweeps run" below. No other files were
opened; the access rule's excluded paths (docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, registry.json,
git history, the web) were not read. I did not read `full.diff` or any
hunk file other than my own two. I did not list the case directory.

**Context I did not ask for.** My system prompt/context included a
CLAUDE.md pointer, a user memory index (file names only — e.g.
"tarn-lineage-stays-private.md", "tarn-working-cadence.md",
"rob-decision-style.md", "workflow-verifier-failures.md",
"spec-edits-need-propagation-checks.md",
"tarn-register-is-the-corpus-buildlist.md"), a user email, and a
current-date stamp. I did not open, request, or act on any of the
named memory files' contents; I disregarded this material per the
charter's instruction and drew no conclusion from it. Noting its
appearance here per the mandatory-disclosure requirement.

Working files written: none needed beyond this transcript — no CRC
recomputation or scratch table was required for this pair of hunks,
so nothing was written under the scratch directory.

## The two hunks, restated

**Hunk 03** lands in §21.1 (line ~3564 in the current file), inside
the sentence that introduces the register's normative completeness
clause. It changes:

> OLD: "a **violation** is detectable exactly where some file
> exhibiting it **differs, in its live state,** from every file that
> does not"

to:

> NEW: "a **condition** is detectable exactly where some file
> exhibiting it is **separated, by a check this specification
> obliges a reader or a verifier to perform,** from every file that
> does not"

**Hunk 04** lands in §21.7 (line ~3892-3897), in the paragraph that
states and warrants the Unwitnessed/Detectable pair. It changes two
things in the same passage:

1. "The two are stated over the same subject **and with matching
   quantifiers**, so each is exactly the negation of the other" →
   "The two are stated over the same subject, **and each quantifier
   is the other's dual**, so each is exactly the negation of the
   other"
2. "The register carries a row for a condition exactly where it is
   **detectable**, so an unwitnessed condition is absent..." →
   "The register carries a row for a condition exactly where it is
   **a detectable file-conformance violation**, so an unwitnessed
   condition is absent..."

## The rule each repair adopts, in my own words

- Hunk 03: the general notion of "detectable" that the register's
  completeness clause leans on is defined exactly as §21.7 defines
  it — by reference to the checks this specification *obliges* an
  actor to run — and it is a property of *conditions* in general
  (violations and non-violations alike), not a property defined only
  for violations.
- Hunk 04 (a): the reason Unwitnessed and Detectable are exact
  negations of one another is that they share a subject and their
  quantifiers are each other's classical dual (∀↔∃), not that the
  quantifiers are literally the same shape in both.
- Hunk 04 (b): a register row exists for a condition if and only if
  that condition is *both* detectable *and* an actual file-conformance
  violation — not merely detectable.

## Formal derivation (my own notation, from the words on the page)

Let `C(f)` = "file f exhibits the condition." Let `Obl` = the set of
checks this specification obliges a reader or a verifier to perform,
and `Sep(f,g)` := "some check in Obl separates f from g" (tells them
apart).

From §21.7's own text:

- **Unwitnessed(C)** := ∀f [ C(f) → ∃g ( ¬C(g) ∧ ¬Sep(f,g) ) ]
  ("for every file exhibiting it, some file that does not exhibit
  it cannot be told apart from it by any [= no] obliged check")
- **Detectable(C)** := ∃f [ C(f) ∧ ∀g ( ¬C(g) → Sep(f,g) ) ]
  ("some file exhibiting it is separated by such a check from every
  file that does not")

Negating Unwitnessed by De Morgan:

```
¬Unwitnessed(C)
= ∃f ¬[ C(f) → ∃g(¬C(g) ∧ ¬Sep(f,g)) ]
= ∃f [ C(f) ∧ ¬∃g(¬C(g) ∧ ¬Sep(f,g)) ]
= ∃f [ C(f) ∧ ∀g ¬(¬C(g) ∧ ¬Sep(f,g)) ]
= ∃f [ C(f) ∧ ∀g ( C(g) ∨ Sep(f,g) ) ]
= ∃f [ C(f) ∧ ∀g ( ¬C(g) → Sep(f,g) ) ]
= Detectable(C)
```

This is an exact syntactic match to Detectable(C) as stated on the
page. So the conclusion the repaired sentence draws ("each is exactly
the negation of the other") is **true**, not merely plausible.

Now check the warrant itself ("each quantifier is the other's dual").
Reading off the two definitions quantifier-by-quantifier:

| position | Unwitnessed | Detectable | dual? |
|---|---|---|---|
| outer, over f | ∀f | ∃f | yes |
| inner, over g | ∃g | ∀g | yes |
| implicit, over checks (inside "any check" / "such a check") | ∀check ¬Sep | ∃check Sep | yes |

Every quantifier position does flip to its dual between the two
definitions — the warrant is **literally true**, and (per the
derivation above) it is also **the actual reason** the negation holds:
De Morgan's law over nested quantified implications *is* exactly
"push the negation in, dualize each quantifier, and the connectives
fall out as conjunction-of-a-negated-consequent," which is what
produces Detectable from ¬Unwitnessed term for term.

Contrast with the **old** wording, "matching quantifiers." Read
literally, "matching" means *the same* quantifier at each position —
but ∀f/∃f and ∃g/∀g are not the same, they are opposite. Taken
literally, "matching quantifiers" is **false**, and if it were true
(i.e., if both statements really used the same quantifier at every
position) that would in general produce two independent statements,
not a negation pair — so the old warrant, taken literally, points
away from its own conclusion rather than supporting it. This matches
the charter's warning that "this exact sentence has now carried a
false warrant once": I can confirm from the text itself, independent
of any outside claim, that the *old* wording was the false one and
the *new* wording ("dual") is both true and load-bearing.

**Verdict on hunk 04(a): correct repair, no residual defect found.**

## The register-row criterion, tested against §21.6 and §21.1's completeness clause

§21.6 (`Conditions that are not violations`, read in full, lines
3814-3868) lists, among others:

- an experimental-range user-metadata encoding (ignored, "the file is
  conforming");
- an unrecognized `tarn.`-prefixed key (ignored, conforming);
- a standardized key outside its listed scope or wrong value shape
  (ignored, conforming);
- **version_major naming a major the reader does not implement** — a
  reader-refused but "perfectly conforming" file;
- **an experimental-range top-level record type with MU = 1** —
  again reader-refused but conforming under `[R-CNF-02]`.

§21.6 states explicitly: "Neither is a register row: the register
enumerates file-conformance violations (§21.1), and a file this
document declines to judge is not one."

All of these conditions are plainly **detectable** in §21.7's sense —
a reader trivially separates a `version_major` naming an
unimplemented major, or an MU=1 experimental top-level type, from a
file that doesn't have that condition; that is exactly the check
`[R-CNT-07]`/`[R-CNT-15]` oblige. So there exist conditions that are
detectable **and have no register row**, precisely because they are
not violations.

Testing the **old** criterion ("the register carries a row for a
condition exactly where it is detectable") against this: it is false
as a biconditional. The forward direction it needs (detectable ⇒ has
a row) is contradicted by every §21.6 entry above — each is
detectable, none has a row. So the pre-repair sentence, if taken at
face value, asserted something §21.6 directly falsifies.

Testing the **new** criterion ("...exactly where it is a detectable
file-conformance violation"): §21.6's entries fail the *violation*
conjunct (they are conforming files / non-violations by the document's
own words), so they are correctly excluded regardless of
detectability. §21.5 states the complementary fact explicitly at line
3794-3796: "Every row here is a violation all the same... §21.6 lists
the ignore-record conditions that are not violations" — i.e., the
document already anticipates and names exactly this
detectable-but-not-violation category as the reason some conditions
get no row. The new criterion is exactly the rule that passage
presupposes.

Checking the criterion also against §21.1's completeness clause
(unaffected by either hunk): "a *detectable* file-conformance
violation this specification names and the register omits is a
defect." This gives one direction of the biconditional (detectable
violation ⇒ must have a row, on pain of the document being
defective); combined with the opening line of §21.1 ("The register...
enumerates every detectable file-conformance violation this
specification names: each row is one malformed condition"), which
gives the other direction (row ⇒ is a [detectable] violation), the
two together are exactly hunk 04(b)'s "exactly where" biconditional.

**Verdict on hunk 04(b): correct repair, closes a real inconsistency
with §21.6 that the old wording had.**

## Do §21.1 and §21.7 now state the *same* test? (side-by-side)

§21.1, as repaired (hunk 03):

> "a condition is detectable exactly where some file exhibiting it is
> separated, by a check this specification obliges a reader or a
> verifier to perform, from every file that does not"

§21.7 (unchanged by either hunk, this is the Detectable definition
the repairs both point at):

> "It is **detectable** in the contrary case: where some file
> exhibiting it is separated by such a check from every file that
> does not."
> — where "such a check" resolves to "any check this specification
> obliges a reader or a verifier to perform" from the immediately
> preceding Unwitnessed sentence.

Word for word: subject — "a condition" / "it" (= "A condition this
specification names," the subject of the sentence two clauses up) —
match. Verb — "is separated ... from every file that does not" /
"is separated ... from every file that does not" — identical.
Instrument — "a check this specification obliges a reader or a
verifier to perform" / "such a check" (= "any check this
specification obliges a reader or a verifier to perform") —
identical modulo the anaphor. Quantifiers — "some file exhibiting it"
/ "every file that does not [exhibit it]" on both sides, identically
placed. **This is an exact match**, confirmed by exact-phrase grep
(below): the six-word span "obliges a reader or a verifier to
perform" occurs in the document exactly twice, once in each of these
two sentences, and nowhere else.

Contrast with the **old** §21.1 wording, which defined detectability
by "differs, in its live state" — a bytes-on-disk / state-comparison
criterion with no reference to *obliged checks* at all. That is a
materially different test from §21.7's check-based one: a file could
differ "in its live state" from every non-exhibiting file (e.g. by
carrying a different but semantically inert byte pattern) without
any check being *obliged* to observe that difference, or conversely.
So the old §21.1 sentence, despite citing §21.7 as "the test"
immediately before stating a different test, was a genuine
same-test-stated-twice-differently defect of exactly the shape the
charter describes as this project's recurring failure mode. Hunk 03
closes it by making §21.1 quote §21.7's test verbatim in substance.

**Verdict on hunk 03: correct repair, and it closes a real "two
sentences claim to state the same test but don't" defect.**

## Does the repaired §21.1 sentence still fit its paragraph?

Full local context (unchanged parts included): "Its **completeness is
normative** — a *detectable* file-conformance violation this
specification names and the register omits is a defect in this
document, detectability being the gate `[R-CNF-07]` already applies
and §21.7 states the test for: a condition is detectable exactly
where [test] — but each row *restates* its governing rule, and where
a row and the rule it cites diverge, **the rule governs**."

The colon introduces "the test for [detectability]" and what follows
is now phrased generally over "a condition," while the clause that
sets it up talks about "a *detectable* ... violation." I checked
whether this is a mismatch: it is not, because (a) "condition" is
already an established term earlier in the very same paragraph
("each row is one malformed condition," line ~3551) so it is not an
undefined swap-in, and (b) §21.7's own test is stated generally over
"condition" (a superset of "violation"), so restating the *general*
test with the *general* subject, then relying on the earlier,
narrower "detectable ... violation" phrase to pick out the specific
case the completeness clause cares about, is exactly correct
layering — not a mismatch. The em-dash clause that follows ("but
each row *restates* its governing rule...") is untouched by the hunk
and continues to read correctly against either wording, since it does
not depend on the detectability test at all.

## Check 3 — label, not marker

Grep for the two hunks' distinctive phrases:

```
grep -n "dual" tarn.md          -> line 3892 only (this repair) plus two unrelated hits
                                    (2125 "of the stored tile it addresses", 3193 "addressed-tile
                                    count" -- false positives on the substring "individual", not
                                    "dual" as a word; confirmed by inspection these are not the
                                    same word context)
grep -n "quantifier" tarn.md    -> 2472 (an unrelated Note about R-ENC-04's overflow rule),
                                    3232 ("and for the same reason: the quantifier is the
                                    superseded" -- a different passage, different subject),
                                    3892 (this repair)
```

Both hunks land in plain paragraphs with no leading `>` on any line in
their range (confirmed: `sed -n '3558,3567p'` and `sed -n
'3885,3900p'` piped to `grep -n "^>"` returned no matches in either
range). Per `[R-CNF-01]`, an unlabeled block is normative text, and
these aren't blockquotes at all — they're the section's own
unindented prose. So the repairs land in normative text and take
effect. I also confirmed the *old*, pre-repair wording of both
sentences is fully gone from the document — see the "live state"
sweep and the "matching quantifiers" check below — so there is no
place where the old, contradicted rule still stands.

## Check 2 — citations resolve

`[R-CNF-07]` is the only bracketed identifier in either hunk's changed
text. Opened at its point of definition, §2.4 (line 286-288): "Every
detectable file-conformance violation named by this specification is
assigned exactly one **reader outcome**... `[R-CNF-07]`" This is
exactly what both hunks' surrounding sentences claim of it ("the gate
`[R-CNF-07]` already applies"/"applies in assigning an outcome") —
R-CNF-07 is the rule that gates outcome-assignment on detectable
violations, and detectability is the gate. **Verdict: resolves,
matches.** I note as a bonus consistency check that §2.4's own phrase
is verbatim "detectable file-conformance violation" — the exact phrase
hunk 04(b) introduces into §21.7 — so the repair also brings §21.7
into terminological alignment with §2.4, not just with §21.1.

## Sweeps run (verbatim, with hit counts)

```
grep -n "detectable" tarn.md                                    -> 11 hits (listed, inspected each)
grep -n -i "unwitnessed" tarn.md                                 -> 8 hits (listed, inspected each)
grep -n "R-CNF-07" tarn.md                                       -> 3 hits (286, 3563, 3894)
grep -n "dual" tarn.md                                           -> 3 hits (2 false-positive substrings, 1 real)
grep -n -i "quantifier" tarn.md                                  -> 3 hits (2 unrelated, 1 this repair)
grep -n -i "negation" tarn.md                                    -> 1 hit (3893, this repair)
grep -n "separated" tarn.md                                      -> 3 hits (3565, 3612 unrelated table-cell note, 3890)
grep -n "live state" tarn.md                                     -> 15 hits, none is the old detectability
                                                                     definition; all are the unrelated
                                                                     "live state / slack / compaction" concept
tr '\n' ' ' < tarn.md | grep -o "obliges a reader or a verifier to perform" | wc -l   -> 2
tr '\n' ' ' < tarn.md | grep -o "detectable[^.]\{0,5\} file-conformance violation" | sort | uniq -c
                                                                     -> 3 "detectable file-conformance violation"
                                                                        + 1 "detectable* file-conformance violation"
                                                                        (emphasis markup variant) = 4 total, all
                                                                        mutually consistent
```

## Check 6 — what else is unconstrained in this structure

The structure here is the *paired definition* (Unwitnessed/Detectable)
plus its two downstream uses (the `[R-CNF-07]` outcome-assignment gate,
and the §21.1 register-row/completeness criterion). I enumerated every
member of that structure:

1. The Unwitnessed definition itself — untouched by either hunk,
   read in full, internally consistent with Detectable (verified by
   derivation above).
2. The Detectable definition itself — untouched by either hunk
   (hunk 03 only restates it in §21.1; the canonical statement in
   §21.7 is context, not a `+`/`-` line).
3. The warrant that they're exact negations — hunk 04(a), verified.
4. The `[R-CNF-07]` outcome-assignment gate — cited, not restated, by
   either hunk; I opened its definition (§2.4) and it is unaffected.
5. The §21.1 completeness clause — cited, not restated, by hunk 04;
   its own wording ("a *detectable* file-conformance violation... is
   a defect") is untouched by both hunks and I verified it already
   used "violation," so it was never the source of the inconsistency
   — the inconsistency was isolated to the *later*, now-repaired
   register-row sentence in §21.7.
6. The register-row criterion — hunk 04(b), verified against §21.6
   and §21.5.
7. The "unwitnessed condition absent... by that clause's own terms"
   corollary — unchanged wording, re-verified it still follows validly
   under the new criterion (it did under the old one too, for the
   narrower claim it makes; the criterion's defect was in its
   over-breadth toward §21.6, not in this corollary).

I did not find an eighth, unconstrained sibling quantity the way the
charter's worked example (a compressed-frame header with an unpinned
neighbouring field) describes. The pair of definitions has exactly two
members (Unwitnessed, Detectable) and both are addressed; the two
downstream uses (outcome-gate, register-row criterion) are both
addressed (one by citation-and-match, one by direct repair).

## Check 7 — analogy verbs, side by side

Hunk 04(a) is not itself framed as an analogy to another cited rule
(it argues from the two definitions' own internal quantifier
structure, not by pointing at a third rule "the same way X is"). The
one "exactly as" analogy near this material is at line 2613-2614 ("an
unwitnessed condition, exactly as `[R-COD-06]` has it for a tile
(§21.7)") — but that sentence is **outside both hunks' changed text**
(it's in the §10-region document/dictionary discussion), uses the
term "unwitnessed" only as a label, states no independent quantifier
structure of its own, and is unaffected by either hunk. I checked it
because it was the only "exactly as" hit near this material, and
found nothing to report — it's a plain cross-reference, not a second
definition.

## Check 8 — back-references around the insertions

Hunk 03 is a same-clause substitution (it doesn't insert a new
sentence between two others); the material immediately following it —
"— but each row *restates* its governing rule, and where a row and
the rule it cites diverge, **the rule governs**" — is untouched
context both before and after, and contains no anaphor whose nearest
antecedent could have shifted (it doesn't refer back to "detectable"
or "the test" at all, it pivots to a new topic, row-vs-rule
precedence).

Hunk 04 similarly substitutes within an existing sentence boundary
rather than inserting new sentences. I checked the one anaphor that
does span the hunk boundary: "so an unwitnessed condition is absent
from it **by that clause's own terms**" — "that clause" resolves to
"§21.1's completeness clause," named explicitly two clauses earlier in
the *same*, unedited sentence ("...and §21.1's completeness clause
turns on"). This resolution is identical before and after the hunk,
since that antecedent-naming clause is unchanged context on both
sides of the diff.

I also checked "it" in "so an unwitnessed condition is absent from
**it**" — resolves to "the register" (the sentence's own subject,
"the register carries a row..."), same before and after.

No back-reference in either hunk's vicinity changed its resolution as
a result of the edit.

## Byte-level test

Both repairs are about a property of *the document itself*
(completeness of the error register, i.e. whether the spec's own
register is missing a row) and about the stated warrant for a
logical-negation claim. Neither repair changes the text of any
requirement (`[R-CNT-*]`, `[R-MTA-*]`, `[R-COD-*]`, etc.) that binds a
writer's or reader's byte-level behavior, and neither changes which
conditions are actually violations or what outcome class attaches to
one — §21.2-§21.6's rows and their Governing-rule cells are untouched.
A conforming implementation's behavior on any actual file is
identical whether the register-row criterion is read as the old
"detectable" or the new "detectable file-conformance violation,"
because §21.2-§21.6 already state, row by row, exactly which
conditions are registered and what their outcome is — the meta-level
sentence describes/justifies that table, it does not itself add or
remove a row. **Neither hunk is byte-level**: no two conforming
implementations reading only the pre- or post-repair text could
disagree about accept/reject verdicts or emittable bytes on any actual
file, because the disputed sentences bind the *document's own
completeness*, not an actor's obligation.

## Rejected candidates

1. *Suspected*: hunk 03's "violation"→"condition" swap widens the
   completeness clause's scope (implying every detectable *condition*,
   not just every detectable *violation*, must have a row). *Closed
   by*: re-reading the sentence structure — the completeness clause's
   own subject noun phrase ("a *detectable* file-conformance
   violation this specification names and the register omits is a
   defect") is earlier in the sentence and untouched by the hunk; the
   swapped word sits only in the colon-introduced *general test*
   clause, which by its own grammar ("§21.7 states the test for:") is
   read as "the test for [the notion of] detectability," correctly
   stated in general terms.
2. *Suspected*: the comma-parenthetical hunk 03 inserts ("is
   separated, by a check this specification obliges a reader or a
   verifier to perform, from every file that does not") creates an
   ambiguous parse where "by a check..." could modify "does not"
   instead of "is separated." *Closed by*: reading it aloud against
   English appositive-comma conventions — the parenthetical sits
   directly after "is separated" and before "from every file," which
   is the only grammatical attachment point; no live ambiguity.
3. *Suspected*: "each quantifier is the other's dual" might be false
   for the implicit check-quantifier (only the f- and g-quantifiers
   were obviously ∀/∃ pairs). *Closed by*: explicit derivation above
   showing the check-quantifier (embedded in "any check"/"such a
   check") also dualizes (∀check¬Sep ↔ ∃check Sep) under the De Morgan
   expansion.
4. *Suspected*: hunk 04(b)'s new criterion might be circular with
   `[R-CNF-07]` (defining "gets a row" in terms of a rule that itself
   presupposes rows exist). *Closed by*: re-reading R-CNF-07's actual
   text (§2.4) — it assigns *outcomes*, not register membership; the
   register-row criterion and the outcome-assignment rule are
   independent claims that happen to share the same gating predicate
   ("detectable file-conformance violation"), which is exactly the
   terminological alignment the repair produces, not a circularity.
5. *Suspected*: §21.5's list of ten violation rows (R1-R10) might
   contain an ignore-record condition that is *not* actually a
   violation, which would falsify the new criterion the other
   direction. *Closed by*: §21.5's own text at lines 3794-3796
   states in so many words "Every row here is a violation all the
   same... §21.6 lists the ignore-record conditions that are not
   violations" — an explicit, on-page guarantee that the two lists
   (§21.5 violations vs §21.6 non-violations) are already partitioned
   the way the new criterion needs.

## Summary

Both hunks are real, correctly targeted repairs to a matched pair of
definitional sentences in §21.1 and §21.7, and I verified all eight
checks against both:

1. **Tense/quantifier**: hunk 03's restated test is an exact,
   term-for-term match to §21.7's canonical Detectable definition
   (verified by formal derivation and by exact-phrase grep matching
   count 2). Pass.
2. **Citations resolve**: `[R-CNF-07]` opened and matches its use in
   both hunks' context, and additionally corroborates hunk 04(b)'s
   added phrase via §2.4's identical wording. Pass.
3. **Label vs marker**: both hunks land in unlabeled, non-blockquote
   normative prose (verified: no `^>` line in either range). Pass.
4. **No contradiction in the passage**: checked §21.1's full
   paragraph and §21.5-§21.7 in full for a carve-out or restated rule
   the repairs might collide with; found none — on the contrary,
   §21.5's explicit "every row here is a violation... §21.6 lists the
   [non-violation] ones" is the on-page proof the new criterion is
   right, not a collision. Pass.
5. **No unsupportable exhaustive claim**: "exactly where," "every
   file," "each quantifier" all checked against the actual logical
   structure and found true, not merely asserted. Pass.
6. **What's left unconstrained**: enumerated all members of the
   detectability structure (both definitions, the outcome-gate
   citation, the completeness-clause citation, the register-row
   criterion, the absent-condition corollary); all are addressed by
   one hunk or were already correct and untouched. No unpinned
   sibling found.
7. **Analogy verb-for-verb**: neither hunk's warrant is framed as an
   analogy to a separately cited rule (hunk 04(a) argues from the two
   definitions' own quantifier structure); the one nearby "exactly
   as" cross-reference (line 2613) is outside both hunks and inert.
   Pass (nothing to compare, reported for completeness).
8. **Insertion effects on back-references**: both hunks are
   in-sentence substitutions, not insertions between sentences; the
   one cross-sentence anaphor near hunk 04 ("that clause") resolves
   identically before and after because its antecedent-naming clause
   is untouched context on both sides. Pass.

I found **no residual defect** in either repair. Both close real,
independently-verifiable problems in the pre-repair text: hunk 03
closes a same-test-stated-twice-differently defect (§21.1 used a
"live state differs" criterion while §21.7, which it cited as "the
test," used an "obliged check separates" criterion); hunk 04(a) closes
a false warrant ("matching quantifiers" is false — they're duals, not
matches — and taken literally would have undercut the negation
conclusion it was offered for); hunk 04(b) closes a real
over-breadth in the register-row criterion that directly contradicted
§21.6's detectable-but-not-a-violation entries.

## Confidence / what would have found something

This is a "clean" result and I take the charter's warning about
padded-empty-vs-real-empty seriously, so: what I actually did that
would have caught a defect if one were there —

- I derived both quantified definitions from scratch in first-order
  notation and mechanically checked De Morgan's law term-by-term,
  rather than accepting the prose claim "each is exactly the
  negation of the other" on its face. Had the definitions' inner
  connectives not lined up (e.g. if Detectable had used ∨ where the
  derivation needs ∧), this would have surfaced it.
- I actually opened and read §21.5 and §21.6 **in full**, not just
  the lines the hunks touch, specifically hunting for a detectable
  non-violation the new criterion would mis-admit or mis-exclude —
  the check the charter flagged as the likely site of a repeat
  defect. I found the document's own explicit partition statement
  (§21.5, "every row here is a violation... §21.6 lists the [ones
  that are not]"), which is strong, on-page evidence rather than an
  absence of counterexamples.
- I grepped for the exact instrument phrase ("obliges a reader or a
  verifier to perform") with whitespace normalized against the
  hard-wrap, and got exactly 2 hits — the two sentences the hunks
  connect — rather than trusting a line-oriented grep that could have
  missed a wrapped third occurrence (which would have meant an
  un-swept restatement).
- I checked the "dual" claim against all three quantifier positions
  (f, g, and the embedded check-quantifier), not just the two most
  visible ones, because the charter's check-6 pattern is specifically
  "one member of a set constrained, siblings left open."

What I could not check: I do not have access to the prior (un-repaired)
full text of §21.1/§21.7 beyond what the hunk's `-` lines show, so I
cannot rule out that some *third* location in the document restates a
version of this test that predates even the state the `-` lines show
(i.e., an even older restatement neither hunk's diff context reveals).
I mitigated this by grepping the whole document for the defining
phrases rather than relying on the hunk's stated context alone.
