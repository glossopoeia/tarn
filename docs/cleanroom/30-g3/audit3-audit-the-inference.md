# Audit transcript — hunk-02.diff (§21.7, "unwitnessed"/"detectable" duality sentence)

## Access disclosure

Read exactly:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-audit3/case/hunk-02.diff` (my charter's hunk file, in full).
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, at these offsets: 3860-3960 (first pass, landing area + §21.7-21.9), 3555-3645 (§21.1 "How to read the register" + start of §21.2), 3823-3877 (§21.6 in full), 2600-2635 (the undisclosed-dictionary-use "unwitnessed" worked example), 225-249 (R-CNF-11's defining paragraph and the "condition"/"reaches" definitions), 195-224 (Conforming verifier / R-CNF-11 lead-in), 285-301 (§2.4, R-CNF-07's defining sentence and the outcome table), 735-749, 1160-1178, 2315-2331 (three Note blocks that reason "no register row" for other reasons, checked for whether they depend on this hunk's exact wording).

Ran only `grep`/`rg` against `spec/tarn.md` (see Sweeps run below) and no other file. Wrote no scratch files — all reasoning was done in this transcript; no script was needed since the only arithmetic involved is a propositional-logic duality check, done by hand below.

**Contamination check**: my system/session context included a CLAUDE.md, a user MEMORY.md index, and skill listings unrelated to this spec. The MEMORY.md index lists titles like "TARN repair prose vs rules" and "TARN lineage gate word list" but I did not open any of the linked memory files, and none of the titles told me anything about hunk-02 specifically (they read as generic project notes about a different round). I did not act on any of it; noting it per the disclosure requirement.

## The hunk

Lands at spec/tarn.md lines 3905-3907, inside §21.7 "What no check detects", in the paragraph that defines "unwitnessed" and "detectable" as exact duals.

BEFORE:
> The register carries a row for every condition that is a detectable file-conformance violation, so an unwitnessed condition is absent from it by that clause's own terms rather than in breach of them.

AFTER:
> The register carries a row for every condition that is a detectable file-conformance violation. An unwitnessed condition is not one, so that clause requires no row for it and its absence from the register breaches nothing.

Header line sanity check: the diff's own comment says the nearest preceding heading is "21.7 What no check detects" at line 3877 in the current file. I confirmed this directly — read_page/grep both show `#### 21.7 What no check detects` at line 3877, and the hunk's landing lines (3905-3907) sit inside that subsection, before `#### 21.8` at line 3935. No mismatch.

## The rule the repair adopts, in my own words

The repair restates (unchanged) that the error-handling register (§21.2-§21.5) contains a row for a condition exactly when that condition is both (a) detectable — some file exhibiting it is separated by an obliged check from every file that doesn't — and (b) an actual file-conformance violation. It then draws a new explicit inference: because "unwitnessed" and "detectable" are stated as exact logical duals two sentences earlier, an unwitnessed condition automatically fails clause (a), so it can never be the kind of thing the completeness clause (§21.1) requires a row for; therefore that clause imposes no obligation regarding it, and — per the repair's added final clause — the condition's absence from the register is not a breach of *anything*.

## Formal check (charter's mandatory step: do the logic before reading for sense)

Notation:
- `D(c)` = c is detectable (§21.7's second definition).
- `U(c)` = c is unwitnessed (§21.7's first definition).
- `V(c)` = c is a file-conformance violation.
- `Row(c)` = the register carries a row for c.

**Premise, as stated in the (unchanged) first sentence of the repaired pair** —
the completeness clause restated:

    P:  ∀c [ D(c) ∧ V(c) → Row(c) ]

**Conclusion the repair draws, decomposed into its three coordinated parts:**

    Q1: ∀c [ U(c) → ¬D(c) ]                         ("An unwitnessed condition is not one" — read via duality)
    Q2: ∀c [ U(c) → ¬(clause obligates Row(c)) ]     ("so that clause requires no row for it")
    Q3: ∀c [ U(c) → ¬(∃ any rule R: ¬Row(c) breaches R) ]   ("its absence from the register breaches nothing")

**Does Q1 follow from P?** No — not from P alone. P says nothing about the relationship between U and D. Q1 follows instead from the *duality* sentence two sentences earlier in the same paragraph: "The two are stated over the same subject, and each quantifier is the other's dual, so each is exactly the negation of the other." I checked that duality claim itself from scratch by unfolding both definitions:

    U(c) ⟺ ∀f [ Exhibits(f,c) → ∃f' (¬Exhibits(f',c) ∧ Indistinguishable(f,f')) ]
    D(c) ⟺ ∃f [ Exhibits(f,c) ∧ ∀f' (¬Exhibits(f',c) → Distinguishable(f,f')) ]

    ¬U(c) ⟺ ∃f [ Exhibits(f,c) ∧ ¬∃f'(¬Exhibits(f',c) ∧ Indistinguishable(f,f')) ]
         ⟺ ∃f [ Exhibits(f,c) ∧ ∀f'(¬Exhibits(f',c) → ¬Indistinguishable(f,f')) ]
         ⟺ ∃f [ Exhibits(f,c) ∧ ∀f'(¬Exhibits(f',c) → Distinguishable(f,f')) ]   (Distinguishable = ¬Indistinguishable, a binary complement — check/separate is a check that either does or doesn't tell two files apart)
         = D(c)

So ¬U(c) = D(c) exactly, confirming the document's own duality claim is logically sound (this was my check on the sentence just before the hunk, not itself part of the diff, but it is the load-bearing premise Q1 depends on — per the charter's instruction to look outside the sentence for a missing step, I found it, and it holds). **So Q1 is sound**, sourced from the paragraph's earlier duality sentence, not from P.

**Does Q2 follow from P and Q1?** Yes, validly. P is a conditional `D(c)∧V(c) → Row(c)`. When `D(c)` is false (from Q1, given `U(c)`), the antecedent `D(c)∧V(c)` is false regardless of `V(c)`, so P is vacuously satisfied and places no obligation on `Row(c)` for that c. "Requires no row" is the correct, standard reading (idiomatic "X requires no Y" = "X does not obligate Y", not "X obligates ¬Y") and it is what a vacuously-true conditional gives you. **Q2 is sound and correctly derived.**

**Does Q3 follow from P and Q1/Q2?** **No — not validly, and this is the defect.** Q2 only establishes that *one specific rule* — §21.1's completeness clause — does not obligate a row for c. Q3 asserts that *no rule whatsoever* is breached by the row's absence. That is a strictly stronger claim, and nothing in the sentence, the paragraph, or the premise P supplies the auxiliary fact needed to license it: that §21.1's completeness clause is the *only* rule in the document that could possibly be breached by a missing register row. The move from "clause X doesn't require it" to "nothing requires it" is exactly the shape the charter's check 5 asks me to test (a completeness/exhaustiveness word — "nothing" — asserted without a supporting universal).

I then did what the charter's check 5 demands: tried to falsify Q3 by searching the rest of the document for any other completeness-type obligation on the register. (See Sweeps run.) I found none — the only place "completeness is normative" is asserted of the register is §21.1 (line 3569), and the §21.1 completeness clause covers exactly `D(c)∧V(c) → Row(c)` with no additional register-completeness rule anywhere else (§21.6's table entries and §21.8's per-row vector-coverage clause both presuppose a row already exists or address non-violations, not missing rows). So **Q3 happens to be true in this document** — but it is not established *by this sentence*, nor by anything the sentence points to. It is an unsupported broadening relative to the BEFORE text, which was correctly scoped ("...rather than in breach of *them*" — "them" = "that clause's own terms", i.e. scoped to the one clause) to an unscoped universal ("breaches *nothing*").

## Testing the conclusion against document practice (charter's third instruction)

Conditions the document says have **no register row**, checked against Q1-Q3:

1. **Undisclosed dictionary use in a compressed user-metadata frame** (lines 2620-2623): "dictionary use the header does not disclose is a writer violation nothing in the extent shows — an unwitnessed condition, exactly as `[R-COD-06]` has it for a tile (§21.7)... R4 registers neither." This is explicitly called **"a writer violation"** that is nonetheless unwitnessed and has no row. Sentence's Q1/Q2 give the right verdict (unwitnessed → no row required). Note this example also shows `V(c)` can be **true** while `U(c)` holds — confirming the duality argument (`¬D(c)`, independent of `V(c)`) is the right mechanism, not an implicit (and false) claim that unwitnessed conditions are never violations.

2. **The MU=1 experimental-range top-level record** (lines 3856-3868): reader-capability rejection, no register row — but for a *different* reason (declared "not a violation" outright, not because it's undetectable — it's very much detectable). The hunk's sentence doesn't claim to cover this case (it only asserts something about *unwitnessed* conditions), so it is not wrong about this case, just silent, correctly.

3. **`[R-ENC-06]`'s fixed field widths** (lines 3927-3933): "states no condition a file can exhibit" at all — a third, distinct category the very next paragraph (unchanged by the hunk) is careful to distinguish from "unwitnessed". Again outside the hunk sentence's claim, not contradicted by it.

4. Rows that **are** registered — F14 (line 274, reads bytes a future major may redefine but is still registered because the invariant it protects is fixed across majors), F18/F35/F36 (lines 3872-3875) — all satisfy `D(c)∧V(c)`, correctly requiring `Row(c)` under P. Consistent.

So on every test case I could find, the sentence's *narrow* claim (Q1, Q2) gives the right answer. It's specifically the *added, broader* Q3 ("breaches nothing", unqualified) that outruns what's established, even though I couldn't produce a case in this document where it's actually false.

## Check 1 — Tense and quantifier

The repaired sentence restates §21.1's completeness clause (line 3569, "Its completeness is normative — a *detectable* file-conformance violation this specification names and the register omits is a defect in this document") with the same quantifier shape: "for every condition that is a detectable file-conformance violation." Both range over the same set (all conditions this specification names that are detectable violations), both are present-tense, timeless statements about the register's contents. No tense/quantifier mismatch between the repair and the rule it restates — this is a faithful one-directional restatement of §21.1's clause. The repair is not itself the normative rule (§21.1's own text is), it is derived/explanatory text in §21.7, correctly citing "that clause" back to §21.1's completeness clause (confirmed by re-reading the immediately preceding sentence: "...and §21.1's completeness clause turns on").

## Check 2 — Citations resolve

The hunk's changed text carries **no bracketed requirement IDs**. It uses one implicit cross-reference, "that clause," which I resolved to §21.1's completeness clause (line 3569, "Its completeness is normative...") via the preceding (unchanged) sentence "...the gate `[R-CNF-07]` applies in assigning an outcome and §21.1's completeness clause turns on." That resolution is correct and unambiguous — there is exactly one "completeness clause" named in the document, at §21.1 (grep confirms; see Sweeps run). No citation to check-and-fail here; nothing to flag.

## Check 3 — Label, not marker

The repaired text is plain body prose, not inside a `>` blockquote at all (confirmed by reading raw lines 3877-3933: no line begins with `>`). Per `[R-CNF-01]` this text is normative by default (not exempted — it isn't §1, isn't inside a Note/Example/Rationale block, and §21.7 is not listed among non-normative appendices). So the repair lands in normative text and its force is real, not inert. No label-vs-marker issue.

## Check 4 — Contradiction within the passage

Checked the whole subsection (§21.7, lines 3877-3933) end to end for anything that collides with the new "breaches nothing" clause:

- The paragraph immediately following (unchanged, lines 3918-3925) states: "Being unwitnessed bears on detection and not on permission: the requirement binds its actor as any other does..." — this explicitly *forecloses* the one misreading I was worried the new wording could invite (that "breaches nothing" might be read as "the underlying condition is not a violation at all"). It's unchanged text, sitting right after the hunk, and it correctly disambiguates. So there is no live contradiction in the final document — but see the ambiguity finding below: for two sentences, the risk exists before the disambiguating paragraph is reached.
- §21.1 itself (line 3569-3571) calls an *omitted detectable violation* "a defect in this document" — i.e., IS a breach. The hunk's "breaches nothing" is scoped to *unwitnessed* conditions specifically (`U(c)`, hence `¬D(c)`), so it does not contradict §21.1's statement about *detectable* violations (`D(c)∧V(c)`) — the two are talking about disjoint sets of conditions (unwitnessed vs. detectable are exact duals, so no overlap). No contradiction.
- No MUST/MAY collision found elsewhere in the subsection.

## Check 5 — Exhaustive claim it cannot carry

Flagged word: **"nothing"** in "its absence from the register breaches nothing." Tried to falsify by searching for any other register-completeness-type obligation (see Sweeps run) — found none. So the claim is not falsifiable from this document as it stands, but (per the formal check above) it is **not entailed** by anything the sentence, its paragraph, or its cited clause actually establishes — it silently assumes §21.1's completeness clause is the sole possible source of such an obligation, a premise the text never states and that a reader has to supply. This is the shape check 5 is looking for: an unqualified completeness word doing work the stated premises don't license, even where I can't produce a counterexample. I'm reporting this as OVERCLAIM rather than a false statement.

## Check 6 — What else in this structure is left unconstrained?

The "structure" here is the two-way dichotomy the paragraph sets up: `D(c)` vs `U(c)`, proven to be exact duals. The repair's conclusion addresses one member (`U(c)` → no row needed). I checked whether the *other* member of any adjacent structure is left unaddressed the way the charter's worked example (one header quantity pinned, its sibling left open) describes. The two candidate siblings are:
- "detectable-but-not-a-violation" conditions (§21.6's table, MU=1 case) — handled by an entirely separate, already-existing paragraph (3869-3871: "the register enumerates file-conformance violations... and a file this document declines to judge is not one"), not something this sentence needed to cover and doesn't claim to.
- "not even a condition a file can exhibit" (R-ENC-06) — likewise handled by the next paragraph (3927-3933), unchanged, explicitly distinguished from "unwitnessed."

Neither sibling is left ungoverned by the document as a whole; both are governed by paragraphs the hunk didn't touch and didn't need to touch. I don't find a second, unpinned quantity of the kind check 6 is built to catch.

## Check 7 — Analogy comparison

The hunk's own changed text contains no analogy language ("exactly as", "the same way", "following", etc.). Nothing to compare here. (The nearby, unchanged line 2623 — "an unwitnessed condition, exactly as `[R-COD-06]` has it for a tile (§21.7)" — does use such language, but it points at the general *concept* of unwitnessedness defined in §21.7, which the hunk did not redefine; only the paragraph's closing inference changed. That external analogy is unaffected by this hunk.)

## Check 8 — What did the insertion do to nearby back-references?

The hunk turns one comma-joined sentence into two, and adds a new sentence-initial clause ("An unwitnessed condition is not one, so..."). Read forward from the insertion to the end of the subsection for back-references:

- "That is **the whole of the test**, and it decides any condition put to it..." (line 3909, first sentence of the next paragraph, unchanged). Antecedent of "the test": before the hunk, the immediately preceding text ended "...rather than in breach of them." — no candidate noun "test" nearby except the detectability/unwitnessedness definitions two sentences up. After the hunk, the immediately preceding text ends "...breaches nothing." — same situation: still no candidate "test" introduced by the insertion, so "the test" still resolves to the detectability/unwitnessedness pair defined earlier in the paragraph ("It is **detectable** in the contrary case..."). **Unaffected**, same resolution before and after.
- "**that clause** requires no row for it" (inside the hunk itself) — resolves to §21.1's completeness clause, established two sentences earlier (unchanged text, "§21.1's completeness clause turns on"). Checked above under check 2 — correct both before and after, since that antecedent-supplying sentence was not touched by the hunk.
- "its absence" — resolves to the just-introduced "an unwitnessed condition['s]" absence, within the same new sentence. Local, unambiguous.
- No other bare "it"/"that"/"such" back-reference appears between the insertion and the end of §21.7 that I could find pointing outside its own sentence, other than the two above, both checked.

No back-reference silently changed its target. Check 8 passes.

## Second finding: "breach" used in two senses close together (ambiguity, not a contradiction)

The very next paragraph (unchanged, line 3910-3911) uses "breach" in a different sense: "ask whether **a breach** can be made to leave behind a file no obliged check separates..." — here "a breach" means a violation of the underlying normative rule (the condition itself), not "a breach of the register-completeness clause." The hunk's new sentence uses "breaches" to mean the latter (a breach of the completeness clause specifically): "its absence from the register **breaches** nothing." Two sentences apart, "breach"/"breaches" shifts sense. A reader skimming could misread "an unwitnessed condition's absence... breaches nothing" as "an unwitnessed condition breaches nothing" (i.e., is never itself a violation) — which is false, per the dictionary-use worked example (§14.2/lines 2620-2623) that calls undisclosed dictionary use "a writer violation" that happens to be unwitnessed. This misreading is corrected two sentences later by the unchanged text at 3921-3922 ("Being unwitnessed bears on detection and not on permission: the requirement binds its actor as any other does") — so the *document as a whole* is not self-contradictory, but the repair introduced a term collision that didn't exist in the BEFORE wording (which said "in breach of *them*" — explicitly scoped to "that clause's own terms," not free-floating "breaches").

## Byte-level assessment

Both findings are about explanatory/derivational text in §21.7 that restates §21.1's already-existing completeness clause; neither changes any writer emission rule, reader accept/reject rule, or verifier verdict rule directly. Resolving either finding (re-scoping "breaches nothing" back to "breaches that clause", or picking a word other than "breaches" for the second sense) would not change which byte sequences a conforming writer may emit or a conforming reader/verifier must accept or reject — the underlying obligations (§21.1's completeness clause, `[R-CNF-07]`'s outcome-assignment, the individual governing rules like `[R-COD-06]` for dictionary use) are all unchanged, unchanged-text, and already correctly stated elsewhere. **Not byte-level**, for both findings.

## Sweeps run (verbatim, with hit counts)

- `grep -n "detectable file-conformance violation" tarn.md` → 3 hits: line 287 (R-CNF-07's own definition), line 3560 (§21.1's opening sentence), line 3905 (the hunk's landing line).
- `grep -n "completeness" tarn.md` → 3 hits: line 3569 ("Its **completeness is normative**" — §21.1), line 3591 ("neither this completeness clause..." — §21.1, re §21.6-21.9 exclusion), line 3915 ("would make §21.1's completeness clause vacuous").
- `grep -n "unwitnessed" tarn.md` → 5 hits: line 2622 (dictionary-use worked example), line 3895 (definition), line 3906 (hunk), line 3921 ("Being unwitnessed bears on detection..."), line 3927 ("Distinguish an unwitnessed condition from...").
- `grep -n "R-CNF-07\]" tarn.md` → 3 hits: line 289 (defining occurrence), line 3572, line 3903 (both citing occurrences in §21.1/§21.7).
- `grep -n "R-CNF-13\]" tarn.md` → 4 hits: lines 162, 270, 3644, 3919 — checked each is about condition/requirement individuation and format-major reach, not register completeness.
- `grep -n "R-CNF-11" tarn.md` → 9 hits (lines 243, 715, 1484, 2552, 2664, 2745, 3065, 3089, 3564, 3892, 4716 — 11 actually, recount below) — checked the defining one (line 243) and the citing one nearest the hunk (line 3892); confirmed R-CNF-11 is about "cannot establish" verdicts on capability/resource grounds, a different concept from "unwitnessed" (no file-level witness at all) — the document itself draws this distinction at lines 3890-3893, unchanged by the hunk.
- `grep -n "register row" tarn.md` → 7 hits (lines 745, 1172, 1390, 2326, 2837, 4247, 4286) — read the three that reason "no register row" for a condition (745, 1172, 2326); all three sit inside `>` blocks headed **Note.**, are non-normative, and none depends on the specific wording this hunk changed (they use their own, independent reasoning about strict-specialization or non-decidability, not the "unwitnessed" duality).
- `grep -n "no row" tarn.md` → 2 hits: line 3591 (§21.6-21.9 excluded from register-row bookkeeping) and line 3906 (the hunk itself).
- `grep -n "not registered\|registers neither\|registers no" tarn.md` → 1 hit: line 2621 (the dictionary-use worked example, "R4 registers neither").
- `grep -n "^#### 21\.\|^### 21" tarn.md` → confirms §21's subsection structure (21.1 at 3557 through 21.9 at 3942), used to scope "the register" and "completeness clause" searches correctly and to verify the hunk's own header-derivation comment (§21.7 at 3877).

## Derived numbers

None. This hunk contains no counts, offsets, sizes, or other numeric quantities — the only computation performed was the propositional-logic duality check (`¬U(c) = D(c)`), worked by hand above, not compared against any numeric figure in the document (there is none to compare against; it's a proof, not a count).

## Rejected candidates

1. **"Does Q1 (the duality step) actually hold, or is 'detectable'/'unwitnessed' not really an exact dual as claimed?"** — Opened by concern that the whole inference chain rests on an assumed duality. Closed by explicitly unfolding both definitions (§21.7, the two sentences just before the hunk) and confirming `¬U(c) = D(c)` by direct propositional manipulation (see Formal check section). The duality holds.
2. **"Does the new wording contradict §21.1's 'omission is a defect' statement for detectable violations?"** — Opened because both talk about register omission having/lacking consequences. Closed by confirming the two are scoped to disjoint sets of conditions (§21.1 talks about `D(c)∧V(c)` conditions being defects if omitted; the hunk talks about `U(c)` conditions, and `U(c) ⟺ ¬D(c)`, so the sets don't overlap) — see Check 4.
3. **"Is there a second, sibling register-completeness rule elsewhere that Q3 ('breaches nothing') might actually violate?"** — Opened as the central test of the "weakened claim" instruction. Closed by exhaustively grepping "completeness", "register row", "no row", "not registered" and reading every hit's context (see Sweeps run) — no such second rule exists in the document as I could access it.
4. **"Could the MU=1 top-level-record case (§21.6) or the R-ENC-06 fixed-width case (§21.7, later paragraph) be counterexamples to the hunk's claim?"** — Opened per the charter's "test against document practice" instruction. Closed: both are outside the hunk sentence's actual claim (which is specifically about *unwitnessed* conditions, not about "any condition lacking a row" in general) — see "Testing the conclusion against document practice."
5. **"Does the hunk's sentence-splitting (comma → period) break the antecedent of 'is not one' or 'that clause'?"** — Opened per check 8's general instruction to test back-references around any insertion. Closed: both antecedents resolve identically to the unsplit version — see Check 8.

## Confidence / where little was found

Checks 1, 2, 3, 6, 7, 8 all passed cleanly with specific, quoted verification (restated above) — I'm confident in those verdicts because each involved either an explicit grep-confirmed citation resolution, an explicit read of the cited section, or an explicit hand-worked formula. Check 4 found no live contradiction in the *final* document (the disambiguating paragraph at 3921-3922 is unchanged and does its job), which is why my strongest finding is filed as an ambiguity/overclaim rather than a contradiction or a false statement — I looked specifically for a MUST/MAY collision and for a restated rule elsewhere that the hunk should have swept (Sweeps run above) and did not find one. If there is a byte-level defect in this hunk that I missed, the most likely place I'd have missed it is in a downstream passage that cites §21.7's "unwitnessed" concept and relies on some property of it stronger than duality + non-obligation (e.g., relies on the OLD text's narrower "not in breach of them" scoping specifically) — I searched for such reliance (the "register row"/"no row" sweep) and found three Note-block examples, none of which depend on the hunk's exact wording.
