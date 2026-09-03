# Repair audit — hunk-04.diff

## 0. Access disclosure

Read only:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-decaudit/case/hunk-04.diff` (my assigned hunk, in full)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, specifically:
  - lines 3820-3959 (§21.6 tail, §21.7 in full, §21.8, start of §21.9)
  - lines 3556-3675 (§21.1 in full, plus §21.2 header and first rows F1-F25)
  - lines 240-300 (§2.3's "reach" definition and §2.4, for `[R-CNF-13]`/`[R-CNF-07]`)
  - lines 2400-2440 (codec 3 / R-COD-08 discussion of undetectable dictionary use)
  - lines 2510-2535 (byte-shuffle / R-COD-10, "undetectable by construction (§21.7)")
  - lines 2600-2630 (compression-frame carve-outs, "falls outside the register... an unwitnessed condition ... (§21.7)")
  - line 3786 (T26 row, cites §21.7's undetectable-by-construction test)

Ran only `grep`/`sed` against `tarn.md` (no other files touched, no web, no git).

**Context-contamination note:** my system prompt/CLAUDE.md context contained an unsolicited "TARN repair prose vs rules" memory-file title and other project memory titles. I did not open or use any of that material's contents; I disregarded it per the access rule. Flagging its presence here as required, not because it informed anything below.

Working scratch file written: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-decaudit/scratch/the-test/notes.md` (formalization scratch-work only, superseded by this transcript).

## 1. The hunk, verbatim

```
@@ -3892,16 +3900,17 @@ check from every file that does not. The two are stated over the
 same subject, and each quantifier is the other's dual, so each is
 exactly the negation of the other, and detectability so stated is
 the gate `[R-CNF-07]` applies in assigning an outcome and §21.1's
-completeness clause turns on. The register carries a row for a
-condition exactly where it is a detectable file-conformance
-violation, so an unwitnessed condition is absent from it by that
-clause's own terms rather than in breach of them.
+completeness clause turns on. The register carries a row for every
+condition that is a detectable file-conformance violation, so an
+unwitnessed condition is absent from it by that clause's own terms
+rather than in breach of them.

 That is the whole of the test, and it decides any condition put to it
 without appeal to a list: ask whether a breach can be made to leave
-behind a file no obliged check separates from a conforming one. The
-instrument is the checks this specification obliges an actor to
-perform, and deliberately not the register's own rows — a test
+behind a file no obliged check separates from one that does not
+exhibit the condition. The instrument is the checks this
+specification obliges an actor to perform, and deliberately not the
+register's own rows — a test
 keyed to the rows would make §21.1's completeness clause vacuous,
 every omitted condition being undetectable by construction.
```

Header sanity check: the hunk's own comment says the nearest preceding heading is line 3876, "21.7 What no check detects." I opened the live file at that line and confirmed: line 3876 reads `#### 21.7 What no check detects`, and the hunk's landing range (3900-3915 in the current numbering, matching the diff's `+3900,17`) sits inside that subsection, before §21.8 at line 3934. No mismatch.

Two edits in one hunk:

- **Edit A** (first paragraph): "The register carries a row for **a condition exactly where** it is a detectable file-conformance violation" → "The register carries a row for **every condition that is** a detectable file-conformance violation." The trailing clause "so an unwitnessed condition is absent from it by that clause's own terms rather than in breach of them" is **byte-identical** before and after (only its line-wrap position moved because the preceding clause got one word shorter... actually one clause longer; re-flow only).
- **Edit B** (second paragraph): "...leave behind a file no obliged check separates from **a conforming one**." → "...from **one that does not exhibit the condition**." The following sentence, "The instrument is the checks this specification obliges an actor to perform, and deliberately not the register's own rows — a test keyed to the rows would make §21.1's completeness clause vacuous, every omitted condition being undetectable by construction," is unchanged.

## 2. The rule each edit adopts

**Edit A** changes the truth-condition for "the register carries a row for condition x" from a **biconditional** to a **one-directional conditional**.

**Edit B** changes what set of files the detectability test compares an exhibiting file against: from "every **conforming** file" to "every file that **does not exhibit the condition**."

## 3. Formal statement of Edit A, both directions

Let `HasRow(x)` = the register (§21.2-§21.5) carries a row for condition x.
Let `Detectable(x)` = x is a detectable file-conformance violation, per §21.7's own definition (lines 3894-3899, unchanged by this hunk):

> "A condition ... is **unwitnessed** where, for every file exhibiting it, some file that does not exhibit it cannot be told apart from it by any check this specification obliges a reader or a verifier to perform. It is **detectable** in the contrary case: where some file exhibiting it is separated by such a check from every file that does not [exhibit it]."

i.e. `Detectable(x) := ∃f. Exhibits(f,x) ∧ ∀g. ¬Exhibits(g,x) → SeparatedBy(check,f,g)`, and `Unwitnessed(x) := ¬Detectable(x)` (the document says so explicitly: "each quantifier is the other's dual ... exactly the negation of the other," line 3900-3901, unchanged).

**Before (Edit A's old text):** "The register carries a row for a condition **exactly where** it is a detectable file-conformance violation."
"Exactly where" = iff. Formally: `HasRow(x) ↔ Detectable(x)`. This entails BOTH:
  (i) `Detectable(x) → HasRow(x)` — completeness (no detectable violation omitted)
  (ii) `HasRow(x) → Detectable(x)` — soundness (nothing but detectable violations gets a row)

**After (current text):** "The register carries a row for **every** condition that is a detectable file-conformance violation."
"Every ... that is" = universally-quantified one-directional conditional. Formally: `Detectable(x) → HasRow(x)` — **only direction (i)**. Direction (ii) is withdrawn; the new sentence does not assert it and does not entail it.

**Direction withdrawn: (ii), `HasRow(x) → Detectable(x)`** — i.e., "a row in the register implies the condition it registers is detectable" / equivalently "the register contains nothing but detectable violations."

This is a genuine weakening, not a paraphrase: (i) alone is consistent with a world where the register also carries rows for some undetectable (unwitnessed) conditions — nothing in the new sentence forbids that. (ii) alone is consistent with a world where some detectable violations lack rows. Only the conjunction (the old "exactly where") pins both.

## 4. Does the paragraph's own argument still follow?

The very next clause of the **same sentence**, left untouched by the hunk:

> "...so an unwitnessed condition is absent from it by that clause's own terms rather than in breach of them."

Formally this asserts: `Unwitnessed(x) → ¬HasRow(x)`, i.e. `¬Detectable(x) → ¬HasRow(x)`.

Is this entailed by what Edit A's new sentence actually states, `Detectable(x) → HasRow(x)`?

- The **contrapositive** of `Detectable(x) → HasRow(x)` is `¬HasRow(x) → ¬Detectable(x)` — logically equivalent to the premise, but a different statement from the one needed.
- The statement needed, `¬Detectable(x) → ¬HasRow(x)`, is the **inverse** of the premise, which is logically equivalent to its **converse**, `HasRow(x) → Detectable(x)` — i.e. exactly **direction (ii), the direction Edit A withdrew.**

So: **the conclusion drawn in the second half of the sentence no longer follows from the premise stated in the first half of the same sentence**, after Edit A. Before the edit, the biconditional supplied both directions and the inference was valid. After the edit, only direction (i) is stated, and the conclusion needs direction (ii). This is a broken inference introduced by the hunk, sitting in text the hunk did not itself flag as changed (the conclusion clause is byte-identical across the diff).

I looked for whether direction (ii) is established elsewhere nearby, so that the local sentence could lean on it as background fact rather than restate it:

- §21.1's completeness clause (lines 3568-3574, quoted in full below, §5) states only direction (i) as its normative content ("a *detectable* ... violation ... the register omits is a defect") — an omission rule, not an inclusion-cap rule. It does not say a row cannot exist for an undetectable condition.
- `[R-CNF-07]` (line 286-288): "Every detectable file-conformance violation named by this specification is assigned exactly one reader outcome" — again direction (i) shaped (detectable → gets an outcome/row), not (ii).
- I found no sentence anywhere in the document asserting "a register row implies its condition is detectable" as a standalone rule. The only place that assertion was ever made explicit was the old "exactly where" biconditional this hunk replaced.

So the gap is real: the argument as written no longer supports its own conclusion, and I could not find the missing premise supplied elsewhere.

## 5. §21.1's completeness clause vs. this passage — do they agree?

§21.1, lines 3568-3574:

> "Its **completeness is normative** — a *detectable* file-conformance violation this specification names and the register omits is a defect in this document, detectability being the gate `[R-CNF-07]` already applies and §21.7 states the test for: a condition is detectable exactly where some file exhibiting it is separated, by a check this specification obliges a reader or a verifier to perform, from every file that does not"

§21.7, current text (post-hunk), lines 3903-3906:

> "The register carries a row for every condition that is a detectable file-conformance violation, so an unwitnessed condition is absent from it by that clause's own terms rather than in breach of them."

These **agree** on direction (i) — both state, in the same words essentially, that a detectable violation must have a row (completeness). They are consistent with each other on that direction. §21.1 does not itself assert direction (ii) either, so there is no direct contradiction *between* §21.1 and the new §21.7 sentence — the problem is internal to §21.7's own sentence, whose second clause needs (ii) and whose first clause (post-edit) supplies only (i).

## 6. Reliance elsewhere on the withdrawn direction (ii)

Searched for other passages that reason "unwitnessed/undetectable therefore no row / falls outside the register," the shape the charter asks me to look for.

`grep -n "unwitnessed\|undetectable\|Unwitnessed"` over the whole file, hits:
```
2426  the same undetectable class as any other writer  [not row-relevant, describes writer-violation class]
2529  undetectable by construction (§21.7).             [R-COD-10, byte-shuffle]
2621  writer violation nothing in the extent shows — an unwitnessed
3786  T26 row — "a wrong stride with no such structural constraint is undetectable, §21.7"
3894  (the definition itself, in §21.7)
3905  (the sentence under audit)
3915  "every omitted condition being undetectable by construction."  [Edit B's sentence, §21.7]
3920  "Being unwitnessed bears on detection and not on permission..."
3926  "Distinguish an unwitnessed condition from a requirement that states..."
```

The clearest external reliance is lines 2619-2624 (§14.3-area, RFC 8878 frame carve-outs):

> "Two of those fall outside the register, on the two distinct grounds §21.7 separates, and R4 registers neither: dictionary use the header does not disclose is a writer violation nothing in the extent shows — an unwitnessed condition, exactly as `[R-COD-06]` has it for a tile (§21.7) — while the bar on sizing a buffer binds a reader rather than the document, and so states no condition a file can exhibit at all."

This passage treats "x is unwitnessed" ⟹ "x falls outside the register" (no row for x) as an established consequence, and cites §21.7 by name as its authority. That is precisely direction (ii)'s contrapositive-equivalent (`Unwitnessed(x) → ¬HasRow(x)`), asserted as fact and pointed at the very subsection whose local sentence, after this hunk, no longer states it. T26 (line 3786) and R-COD-10 (line 2529) do the same in miniature ("undetectable by construction (§21.7)" as the reason a condition is not separately registered).

None of these outside passages are broken by the hunk in the sense of now asserting something false — the underlying fact (register rows and detectable violations do coincide, as far as every example in the document shows) still holds. What is broken is that §21.7 — the subsection whose whole job, per its own heading and per these citing passages, is to state the test that justifies this equivalence — no longer states the direction that "falls outside the register" requires. The citing passages now rest on a premise that its cited source no longer supplies.

## 7. The gloss/definition consistency check (Edit B) — six named conditions

Edit B changes the *gloss* of the detectability test ("ask whether a breach can be made to leave behind a file no obliged check separates from **X**") from X = "a conforming one" to X = "one that does not exhibit the condition." This is directly beside Edit A but is a different, separable change, so I checked it on its own terms per the charter's instruction to state gloss and formal definition as quantified statements and test six conditions against both.

**Formal definition** (§21.7, unchanged, lines 3894-3899, quantifies over files that do/do not **exhibit the condition** — see §3 above).

**Old gloss:** "no obliged check separates [f] from **a conforming one** [g]" → reads g as ranging over `Conforming(g)`, i.e. `g` has *no* violations at all.
**New gloss:** "no obliged check separates [f] from **one that does not exhibit the condition**" → reads g as ranging over `¬Exhibits(g,x)` for the specific condition x under test.

`Conforming(g)` and `¬Exhibits(g,x)` are different sets whenever g could have some *other* violation y≠x while still lacking x. The formal definition (§3 above) quantifies over `¬Exhibits(g,x)`, matching the **new** gloss, not the old one. So Edit B is a genuine fix of a pre-existing mismatch between the gloss and the definition it glosses — the *old* wording was the one out of step.

Six named conditions, checked against both the (correct, current) gloss and the formal definition, to confirm they now state one test:

1. **F1**, front-block instance (byte-reversed signature, line 3652) — a file exhibiting it is separated from every file lacking it by the open-time byte-identity check (`[R-CNT-04]`/`[R-ENC-02]`) when that reader holds bytes [0,16) resident. Detectable under the formal definition; gloss agrees (some non-exhibiting file is in fact separated by an obliged check, when the residency condition holds) — **has a row (F1)**.
2. **F14** (trailer CRC mismatch, line 3664) — reader recomputes CRC-32C at open; any file lacking the mismatch is separated. Detectable; gloss agrees — **has a row**.
3. **R-COD-10** mis-strided byte-shuffle, line 2524-2529 — explicitly stated "undetectable by construction (§21.7)" where no structural obligation (padding/bool-byte) is also broken. Both formal def and gloss agree it is unwitnessed (no obliged check separates the miswritten file from a correctly-shuffled one bearing the same final bytes, since decoded content isn't independently checked) — **no row**, consistent with §21.7's own worked example in its lead paragraph (lines 3878-3892).
4. **R-COD-06** undisclosed compression dictionary (line 2619-2622, also 2423-2427) — explicitly "not detectable by inspection," "an unwitnessed condition" — **no row** (R4 "registers neither," per line 2620). Both formulations agree.
5. **R-MTA-09** wrong user-metadata document content (line 3882-3884, cited in §21.7's own opening) — a document with correct structure but wrong values; no checksum or structural check distinguishes it from a document with different, equally well-formed, correct values. Unwitnessed under both formulations — **no row**.
6. **R-CNT-22** (registered record type whose stored MU/PE bits differ from the §7.3 registry, lines 3846-3853) — a **verifier** check can compare the stored bits against the fixed registry entry, separating any such file from one whose bits match; detectable under the formal definition. Gloss agrees (a verifier check does separate it from every file that doesn't exhibit the mismatch, regardless of what *else* such files might be nonconforming for) — **has a row**, per line 3850 ("both carry detector *verifier*").

**Result: all six agree between the (post-edit) gloss and the formal definition.** Edit B is a correct repair on its own — it did not merely fail to break anything, it actively fixed a mismatch (old gloss used "conforming," a strictly narrower/wrong set, in place of "does not exhibit the condition").

## 8. Check 3 — normative placement / label

Grepped the hunk's landing region (lines 3876-3935) for blockquote markers:
```
sed -n '3876,3935p' tarn.md | grep -n "^>"
```
→ **no output** (no blockquote lines in this range). The whole of §21.7 as it stands, including both edited sentences, is plain paragraph prose with no ">" marker at all, so the Note/Example/Rationale label question does not arise here — this text is normative under `[R-CNF-01]`'s default rule regardless, and there is no labeled-block trap to check against. (The nearby `> **Example.**` block is at line 3931... actually the nearest one I found earlier in this general area was at line 2531 and one at line 271, both outside the hunk's own paragraph.) Confirmed by direct read of lines 3876-3932 (§5 above) — the two touched sentences sit in ordinary paragraphs, not blockquotes. **Check 3: pass, no defect.**

## 9. Check 2 — citations in the touched text

The two edited sentences carry **no bracketed requirement IDs and no section numbers of their own** — the only cross-reference is the anaphoric "that clause" (→ §21.1's completeness clause, named in the immediately preceding, untouched sentence) and "§21.1's completeness clause" itself two lines earlier (untouched). I opened §21.1 (full text, §5 above) and confirmed it does contain a completeness clause matching the reference. `[R-CNF-07]` appears in the untouched lead-in sentence ("...the gate `[R-CNF-07]` applies in assigning an outcome...") — I opened it (line 286-288, quoted in §6... actually §4 above) and confirmed it is about outcome assignment to detectable violations, consistent with what the sentence around it claims. Both citations check out. No new citations were introduced by this hunk.

## 10. Check 8 — back-references

The hunk is a word-level substitution within existing sentences, not an insertion of new sentences between old ones, so the anaphora-insertion failure mode (new text landing between a pointer and its antecedent) does not apply in its usual form. I checked anyway:

- "that clause" (post-Edit-A sentence) — antecedent is "§21.1's completeness clause," two lines earlier, **unchanged, unmoved** by the hunk. Resolves the same before and after.
- "the condition" (Edit B's new text, "one that does not exhibit **the condition**") — antecedent is "any condition put to it" earlier in the **same** sentence ("it decides any condition put to it without appeal to a list: ask whether..."), also unchanged. Newly-introduced anaphor, but intrasentential and unambiguous — resolves cleanly.
- No pointer's nearest antecedent changed position relative to the pointer as a result of this hunk. **Check 8: pass.**

## 11. Checks 5, 6, 7

**Check 5 (exhaustive claims):** "every condition that is a detectable file-conformance violation" (Edit A) — the "every" here is exactly §21.1's own completeness requirement restated, not an overclaim; verified against §21.1's text in §5 above — matches. No other absolute quantifier introduced by either edit that overclaims beyond what's supported.

**Check 6 (what's left unconstrained in the same structure):** The structure here is the two-way partition {Detectable, Unwitnessed} over "condition," stated as exhaustive and mutually exclusive by construction ("each is exactly the negation of the other," unchanged, line 3900-3901) — there is no third state left ungoverned on that axis. The actual gap this hunk leaves is not a *third value* of that structure but the *missing direction* of the HasRow/Detectable relationship, already reported as the main finding (§4, §6).

**Check 7 (analogy):** Neither edited sentence uses "exactly as," "the same way," "following," or similar analogy language. (That pattern appears elsewhere in the document — e.g. line 2622 "exactly as `[R-COD-06]` has it for a tile" — but that sentence is outside this hunk and unchanged by it.) Not applicable to this hunk's own text.

## 12. Byte-level assessment of the main finding

Does resolving the broken inference (§4/§6) change which bytes a conforming implementation may emit or must accept/reject?

I could not construct two competent implementations that disagree on any actual byte or verdict because of this defect. §21.1's completeness clause (the actual normative constraint on the register's contents) is unchanged by this hunk and still states only direction (i) — no detectable violation may be omitted. Nothing in this document actually *requires* direction (ii) to hold for any conformance purpose I could find: whether a specific condition has a row is settled row-by-row by the register itself and by §21.1, not by this passage's argument. The passage under audit is explanatory/justificatory prose arguing *why* the register's known shape is consistent with its own completeness rule; its conclusion happens to be true of every condition I checked (§7's six, plus the R-COD-06/R-COD-10/R-MTA-09/T26 examples the document itself works through), just not *entailed* by the sentence as now worded. This is a defect in the specification's self-consistency / argumentative soundness — a document defect — not a fork in emittable bytes or accept/reject verdicts. **Not byte-level.**

## 13. Summary of checks run against this hunk

- Check 1 (tense/quantifier): **defect found** — biconditional weakened to one-directional conditional; the withdrawn direction is needed by, and was previously supplying, the very next clause of the same sentence. Reported as B-01.
- Check 2 (citations): pass — `[R-CNF-07]` and the §21.1 back-reference both check out.
- Check 3 (label/normative placement): pass — no blockquote in the touched region.
- Check 4 (contradiction / broken argument in the passage): **same defect as check 1**, this is where I found it (the argument no longer follows).
- Check 5 (exhaustive claims): pass — the "every" in Edit A is exactly §21.1's own completeness scope.
- Check 6 (unconstrained siblings): pass — Detectable/Unwitnessed is a complete, exhaustive dual by the document's own unchanged statement; no third sibling value left open.
- Check 7 (analogy quantifier match): not applicable — neither edited sentence argues by analogy.
- Check 8 (back-reference resolution under insertion): pass — this hunk is substitution, not insertion between sentences; both back-references checked resolve unchanged.
- Edit B evaluated separately: **not a defect — a correct fix**, verified against six named conditions (F1, F14, R-COD-10, R-COD-06, R-MTA-09, R-CNT-22), all agreeing between gloss and formal definition post-edit, whereas the *old* gloss ("a conforming one") was the one out of step with the formal definition's own quantifier.
- Overshoot/undershoot: Edit A doesn't overshoot or undershoot a stated defect (I have no defect report to compare it to — my brief is to audit the repair standing on its own) but it does regress the local argument's validity, which is the finding.
- Unswept restatement: the direction-(ii) reliance at lines 2619-2624 (and, smaller, 2529 and 3786) is **not itself wrong** post-hunk (their conclusions remain true on the facts), so this is not a restatement that now contradicts the edited text — it is a restatement that now cites, as its authority, a passage that no longer carries the premise it needs. I am reporting it as supporting evidence for B-01 rather than as an independent second finding, since fixing B-01 (restoring or otherwise re-supplying direction (ii) in §21.7) fixes the gap for all of them at once.
