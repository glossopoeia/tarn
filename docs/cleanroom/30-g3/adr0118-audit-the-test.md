# Repair audit — lane "the-test" — hunks 01, 06, 12, 17, 18

## 0. Disclosure

Read: the five hunk files named in my charter under r30-audit/case/
(hunk-01.diff, hunk-06.diff, hunk-12.diff, hunk-17.diff, hunk-18.diff), and
spec/tarn.md (4739 lines) via sed/grep — ranges 95–240, 240–345, 344–352,
432–500, 801–851, 1160–1180, 1202–1222, 1248–1262, 1505–1520, 2615–2632,
2895–2930, 2930–2995, 3252–3268, 3470–3486, 3560–3668, 3820–3990, plus grep
hits quoted below. Did not read full.diff, other hunks, docs/, conformance/,
AGENTS.md, README.md, PLAN.md, git history, or the web. Did not list the
case directory.

Wrote: only this file. No scratch scripts were needed (the only computation
was counting table rows, done by grep).

Unrequested context that appeared before I began: a project-instruction
pointer (CLAUDE.md → AGENTS.md; I did not open AGENTS.md), an index of four
auto-memory note titles, and an environment block listing recent commit
subjects that name round numbers and ADRs. None of it is the specification
and I drew nothing from it; noted here as a disclosed exposure.

Hunk headers vs bodies: all five headers agree with the current file —
hunk 01 at 321–326 under §2.4 (line 285); hunk 06 at 2950–2958 under §19.3
(2941); hunk 12 at 3585–3590 under §21.1 (3571); hunk 17 at 3911–3924 under
§21.7 (3893); hunk 18 at 3945–3951 under §21.7. No discrepancy.

## 1. Normative-label check (Check 3), all five hunks

Applied the [R-CNF-01] label test, not the ">" marker. [R-CNF-01] (line
105–107): "All text in this document is normative except: §1; any text
labeled Note, Example, or Rationale; and appendices identified as
non-normative."

- Hunk 01: unquoted paragraph ending `[R-CNF-12]`. No label. Normative.
- Hunk 06: unquoted paragraph ending `[R-RDR-03]`. Normative.
- Hunk 12: unquoted paragraph of §21.1 (no ID; normative by R-CNF-01).
- Hunk 17: unquoted paragraph of §21.7 (no ID until R-ERR-01 later). Normative.
- Hunk 18: unquoted paragraph ending `[R-ERR-01]`. Normative.

Nearby labeled blocks that could have absorbed a repair: §2.4's closing
"> **Note.**" (line 328) — not edited; §4.2's "> **Rationale.**" — not
edited; §7.4's "> **Note.**" at line 1170 (the nesting-witness note) — not
edited. All repairs landed in normative text.

## 2. The formulas (charter item 1)

Let K = the checks this specification obliges a reader or a verifier to
perform; sep_k(f, g) = check k tells f and g apart; ex_c(f) = f exhibits
condition c. Subject in every case: "a condition this specification names".

§21.7 unwitnessed (lines 3911–3914):
  U(c) := ∀f [ex_c(f) → ∃g [¬ex_c(g) ∧ ∀k∈K ¬sep_k(f,g)]]
  order: ∀f ∃g ∀k — innermost predicate ranges over checks.

§21.7 detectable, post-repair (3914–3917: "some file exhibiting it is
separated from every file that does not by some such check, which need not
be the same check for every one of them"):
  D(c) := ∃f [ex_c(f) ∧ ∀g [¬ex_c(g) → ∃k∈K sep_k(f,g)]]
  order: ∃f ∀g ∃k.

Mechanical check: ¬U(c) = ∃f [ex_c(f) ∧ ¬∃g[¬ex_c(g) ∧ ∀k ¬sep]]
                        = ∃f [ex_c(f) ∧ ∀g [¬ex_c(g) → ∃k sep_k(f,g)]] = D(c).
The claimed relation ("each quantifier is the other's dual, so each is
exactly the negation of the other") holds. Pre-repair D read "separated by
such a check from every file that does not", which admits ∃k∀g; the repair
pins ∀g∃k, which is the true dual. PASS.

§21.1 restatement, post-repair (3586–3590: "some file exhibiting it is
separated from every file that does not by some check this specification
obliges a reader or a verifier to perform, not necessarily the same check
for each"):
  D'(c) := ∃f [ex_c(f) ∧ ∀g [¬ex_c(g) → ∃k∈K sep_k(f,g)]]
Quantifier by quantifier against D: ∃f = ∃f; ∀g = ∀g; ∃k = ∃k; K identical
("obliges a reader or a verifier to perform" in both). Subject identical
("a condition"). PASS. ("for each" — see rejected candidate R-1.)

Third form, §21.7 line 3926–3929, untouched by the repair: "ask whether a
breach can be made to leave behind a file no obliged check separates from
one that does not exhibit the condition":
  T(c) := ∃f [ex_c(f) ∧ ∃g [¬ex_c(g) ∧ ∀k∈K ¬sep_k(f,g)]]
  order: ∃f ∃g ∀k.
Compare U: ∀f ∃g ∀k. The outer quantifier differs. T is strictly weaker
than U (U ⇒ T, not conversely). A condition with one exhibiting file that
no check separates and another exhibiting file separated from every
non-exhibiting file satisfies T (test says: unwitnessed) and satisfies D
(definition says: detectable). See finding B-03.

## 3. The conclusion sentence (charter item 2)

Sentence (3921–3924): "The register carries a row for every condition that
is a detectable file-conformance violation. An unwitnessed condition is not
one, so that clause requires no row for it, and its absence is not the
defect that clause names."

Premise, from §21.1 line 3583–3585: ∀c [D(c) ∧ V(c) → Row(c)], and its
contrapositive framing "a detectable file-conformance violation ... the
register omits is a defect in this document".
Conclusion: for c with U(c): ¬D(c) (by §2 above), so ¬(D(c) ∧ V(c)), so the
clause's antecedent is unmet, so the clause imposes no Row(c) and an
omission of c is not the defect the clause names. Follows. PASS.

Anaphors: "one" → "a detectable file-conformance violation" (preceding
sentence). "that clause" → "§21.1's completeness clause" (3920–3921); the
intervening sentence "The register carries a row for every condition ..."
is that clause restated, so either resolution yields the same content.
"it" / "its" → "an unwitnessed condition". "the defect that clause names"
→ §21.1's "is a defect in this document". All resolve.

Old form "its absence from the register breaches nothing" widened the
conclusion (nothing at all is breached); new form claims only that the
omission is not §21.1's named defect. The narrowing is correct.

Other passages reasoning from "no witness, therefore …":
- 1170–1172 (Note, non-normative): "in format major 1 it has no
  reader-detectable witness, and so no register row." Conclusion: a
  factual "no row". Within licence. Actor named is "reader" where the
  definition says "reader or a verifier" — but the note's next sentence
  explains a verifier is a reader parsing the same payloads, so the sets
  coincide here. Not a finding.
- 2623–2628 (§18.2 normative): "Two of those fall outside the register, on
  the two distinct grounds §21.7 separates ... an unwitnessed condition ...
  while the bar on sizing a buffer binds a reader rather than the document,
  and so states no condition a file can exhibit at all." Conclusion: "fall
  outside the register". Within licence; the two grounds are exactly §21.7's
  two paragraphs (unwitnessed; no condition a file can exhibit). PASS.
- 3260–3264 (§20.x step): "precisely where the §14 bar has no witness ...
  which is why the rule is stated here and not left to the rows." Conclusion:
  stated in prose rather than a row. Within licence. PASS.
- 3479–3482: "Neither obligation has a witness in the output alone, save
  that ..." — draws no row conclusion. PASS.
- 3906–3910 (§21.7 ¶1): "no file-level witness exists to check, so nothing
  about the file is left undetermined and the verdict is unaffected." A
  different conclusion (R-CNF-11's cannot-establish), consistent with 3938–
  3942 "Being unwitnessed bears on detection and not on permission". PASS.

## 4. Hunk 01 — §2.4 [R-CNF-12]

Rule adopted: the verifier's §2.3 duty runs to MUST-level conditions (not
SHOULDs), and — new, by appositive — §21 inventories MUST-level conditions.

Before: "runs to the MUST-level conditions §21 inventories" (restrictive:
the duty is bounded by what §21 lists — row-keyed).
After: "runs to MUST-level conditions, which §21 inventories" (appositive:
the duty runs to the class; the class is inventoried by §21).

What the sentence now asserts of the class: that §21 inventories MUST-level
conditions, i.e. MUST-level ⊆ §21.

Passages that deny it:
- §21.1 3581–3583: the register "enumerates every *detectable*
  file-conformance violation" — detectable only.
- §21.7 3922–3924: "An unwitnessed condition is not one, so that clause
  requires no row for it" — unwitnessed MUST-level conditions are not
  inventoried. Concrete members: R-COD-06's undisclosed dictionary
  (2624–2626 "a writer violation nothing in the extent shows — an
  unwitnessed condition"); §7.4's nesting prohibition (1170–1172 "no
  register row").
- §2.3 [R-CNF-02] 165–176: conduct rules (MUST-level: §10.3, §18.3, §9's
  barrier steps 4 and 6 at 1252–1258) are "never" file-conformance
  violations and carry no row.
- §21.7 3944–3951: R-ENC-06, a MUST-level requirement, has no row, "there
  being no condition to omit".
So the appositive overclaims. Worse, taken literally it re-imports the
reading the repair was written to remove: if §21 inventories all MUST-level
conditions, the duty "runs to" exactly the rows, which §21.7 3929–3933
rejects ("deliberately not the register's own rows — a test keyed to the
rows would make §21.1's completeness clause vacuous").

Citations: "§2.3" — the verifier bullet (208–211): "A reader that
additionally checks every file-level requirement — including those
ordinary readers are exempted from — and certifies conformance." PASS
(the duty exists there). Duty runs to "every file-level requirement"; the
repaired sentence says it runs to "MUST-level conditions". Requirement vs
condition unit shift is pre-existing (old text too); the MUST-only
narrowing is R-CNF-12's own contribution. "§21" — the register. PASS as a
pointer; the appositive's claim about it FAILS as above.

Check 4 (same passage): 320–323 "§21's register enumerates MUST-level
conditions only" (register ⊆ MUST-level) — not the converse, no
contradiction with the appositive by itself; the contradiction is with
§21.1/§21.7 above. Check 5: no other completeness word. Check 6: the
verifier's reporting structure — MUST-level (checked), SHOULD (advisory,
observed not hunted), conduct rules (R-CNF-02, no file witness),
unwitnessed (no check) — every member is governed somewhere; nothing left
open beyond the appositive. Check 7: no analogy. Check 8: the sentence is a
rewrite, not an insertion; the following Note's "Reject" is unaffected; no
back-references after it in §2.4.

Byte-level? No. A verifier cannot check an unwitnessed condition under either
reading, and a conduct rule has no witness; the only file on which two
verifiers could diverge would be one exhibiting a detectable MUST-level
condition the register omits — a document defect the completeness clause
already obliges the maintainer to fix, and I found no such condition
(F7 covers R-CNT-05's gap structure; R-ENC-07 is read through F16/F23/L12
etc.). Finding B-01, not byte-level.

## 5. Hunk 06 — §19.3 [R-RDR-03]

Rule adopted: full layer-record validation includes "the field widths at
which §4 fixes the parse ([R-ENC-06]) and the u64 value domain of §4.2
([R-ENC-03])".

Citations: [R-ENC-06] at line 476–478, inside §4.2 (§4.3 begins at 480) —
"§4" is true, "§4.2" would be exact. Its text: "every field's width is
fixed by this specification, and a structure whose fields appear at any
other width is invalid at its owning scope." PASS as a pointer. [R-ENC-03]
at 451–456 in §4.2: "valid range of every offset, length, extent, and
count ... 0 to 2⁶³ − 1 inclusive; a reader MUST treat a value above ... as
a validity error at the owning scope." PASS; L1 (3718) is the row.

Agreement with §21.7 (hunk 18): §19.3 now describes R-ENC-06 as fixing
the parse; §21.7 3945–3947 says "the parse is always at the widths this
specification fixes". Same thing. PASS.

What every other member of the list has in common: each names a
condition the layer record can violate, cites the rule stating it, and
"failure takes each cited rule's own scope" (2965–2966); each is
"decidable from the resident directory and F". The edited member does not
have it: per §21.7 [R-ERR-01], R-ENC-06 "states no condition a file can
exhibit", so there is nothing to decide and no failure to take a scope.
The parse at other widths is already what the "exact parse" (R-CNT-18)
member rules out via payload length. So the member is a parse premise
placed in a list of checks. Finding B-02, not byte-level (a reader that
performs no "width check" and one that equates it with the exact parse
emit and accept identical bytes).

Check 6, siblings of the parse-fixing rule: byte order (R-ENC-01, 435–
438), bit numbering (R-ENC-08, 495–496), and widths (R-ENC-06) all fix the
parse of the layer record and none is a file condition; only widths is
named. Harmless, since none is a check — noted, not a finding. Check 7: no
analogy. Check 8: "All are decidable" / "each cited rule's own scope" —
antecedents unchanged (the list); the edited member is the odd one out
under both phrases, which is B-02.

## 6. Hunk 12 — §21.1

Rule adopted: the §21.1 statement of detectability is ∃f ∀g ∃k (§2).
Matches §21.7 and is the true dual of U. PASS.

Citations: [R-CNF-07] (287–289) "Every detectable file-conformance
violation ... is assigned exactly one reader outcome" — PASS, it is the
gate the clause says it is. "§21.7 states the test" — PASS.

Check 4: same paragraph, "where a row and the rule it cites diverge, the
rule governs"; "neither this completeness clause ... reaches §21.6's
defined non-violations, §21.7's test for what no check detects" —
consistent (the clause ranges over violations; §21.7 is the test, not a
row). Check 5: "exactly where" — the biconditional is what D states;
holds. Check 6: the definition's structure — subject c, file set, check
set K, separation — all pinned identically in §21.1 and §21.7. Check 7:
no analogy. Check 8: forward back-references — "the same exception stated
above" → "except where a rule assigns one expressly" (3574–3575),
unchanged; "this completeness clause" → 3583; "the instance arithmetic
below" → Instances paragraph. None re-resolves. Backwards: "such" absent;
"for each" → "every file that does not" (nearest distributive noun) — see
R-1.

## 7. Hunk 17 — §21.7 definition and conclusion

Formulas and conclusion: §2 and §3 above. PASS on the relation claimed.
Citations: [R-CNF-07] PASS (as §6). "§21.1's completeness clause" PASS
(3583–3585). Check 5: "exactly the negation" — verified by formula;
"every one of them" — them = the non-exhibiting files, correct set;
"whole of the test" (untouched) — see B-03. Check 4: 3938–3942 "Being
unwitnessed bears on detection and not on permission" — consistent with
the narrowed conclusion. 3936–3937 "as [R-CNT-06] shows by stating nine"
— see §9 count. Check 8 forward: "That is the whole of the test" — "That"
resolves to the definitional pair, as before the repair (the same sentence
preceded it before); "The instrument"; "The subject" — unaffected.
Check 6: what the definition leaves open — which tier's obligations K
includes (a verifier's "every file-level requirement" duty is not itself a
separating check; §21.7 ¶1 3906–3910 makes that explicit); pre-existing
and unchanged by this hunk.

## 8. Hunk 18 — §21.7 [R-ERR-01]

Rule adopted: values read at the fixed widths from a structure written at
other widths are caught by the rows for those fields *only where* the
shifted value is one those rows reject.

Case the qualifier excludes: a writer lays the layer record's fields at
widths other than §7.4's, and the bytes, parsed at the fixed widths, yield
values every row accepts (every scalar in range, name lengths consistent,
payload length exactly 81 + entries, index arithmetic consistent). Is the
file conforming? Yes: the parse is the only parse (R-ENC-06, 3945–3947),
so the file simply *is* a different, conforming layer record. Does the
closing claim "Nothing is omitted from the register on its account, there
being no condition to omit" hold of it? Yes — no condition is exhibited;
the writer's intention is not a state of the bytes. The old text ("caught
by the rows") implied every mis-width write is caught, which this case
falsifies; the qualifier makes the sentence true. PASS.

Contrast with §21.7's unwitnessed class (R-COD-06's dictionary): there
the bytes *have* the property (compressed against a dictionary) and no
check sees it; here the bytes have no width property at all. The
distinction the paragraph draws survives. Citations: [R-ENC-06] PASS.
Check 6: fields with no rejecting row (e.g. version_minor "any") — the
qualifier now covers them. Check 8: "Nothing is omitted ... on its
account" — "its" → R-ENC-06; unchanged.

Residual: R-ENC-06's own clause "a structure whose fields appear at any
other width is invalid at its owning scope" reads as a condition with an
outcome, while §21.7 reads it as vacuous. See R-2.

## 9. The count

§21.7 3936–3937: "as [R-CNT-06] shows by stating nine". Counted the §21.2
rows whose Governing rule cell names `[R-CNT-06]` first:
`grep -n '^| F[0-9]*.*| \`\[R-CNT-06\]\`' spec/tarn.md` → F8, F9, F10,
F12, F13, F14, F15, F16, F17 = **9**. Cross-check against the R-CNT-06
text (836–846): magic; CRC; [version gate → §6.3's rule, not counted];
[flag gates → §6.3, not counted]; CFL = file size (F17); CFL multiple of
64 (F13); dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); sum ≤ F − 64 (F10);
file_id ≠ 0 (F12); reserved zero (F15) = 9. Matches. §2.3 line 250–252
"nine, of which the trailer magic and the trailer CRC assert invariants
[R-CNT-24] fixes and the other seven do not" — 2 + 7 = 9, and §21.2's
preamble (3660–3662) lists F8 and F14 among the reaching rows. Consistent.

## 10. Sweeps run (verbatim, with counts)

- `grep -n -i 'unwitnessed\|no witness\|witness'` → 10 hits (1172, 2625,
  3262, 3479, 3908, 3911, 3923, 3938, 3944 …); each examined in §3.
- `grep -n -i 'no row\|requires no row\|no such row\|without a row\|omitted from the register\|omits'` → 6 hits (607, 1256, 3585, 3606, 3923, 3950).
- `grep -n -i 'field width'` → 2 hits (1514, 3945). Control for hard-wrap:
  `grep -n -i 'fixes the parse\|fixed the parse\|fix the parse'` → 1 hit
  (2954), and the phrase at 3946 wraps as "the parse is always at the
  widths this specification / fixes" — confirmed by reading, not by grep.
- `grep -n -i 'advisory\|hunted\|MUST-level\|SHOULD deviation'` → 8 hits;
  the only R-CNF-12 restatement is R-CNF-12 itself (321–326).
- `grep -n -i 'told apart\|separated\|separates\|the same check\|dual'`
  → 10 hits; the three detectability forms are 3586–3590, 3911–3917,
  3926–3929.
- `grep -n -i 'every file-level requirement\|file-level requirement'` →
  3 hits (210, 324, 348).
- `grep -n -i 'shifted\|other width\|any other width'` → 2 hits (449, 3949).
- `grep -n 'inventor'` → 3 hits (325, 2838, 3966); no other passage claims
  §21 inventories MUST-level conditions.
- `grep -n 'keyed to the rows\|appeal to a list\|the register.s own rows'`
  → 2 hits (3927, 3932).
- `grep -n 'conduct'` → 6 hits (167, 169, 1035, 1252, 3855, 3882).
- Rows: `grep -n '^| F.*R-CNT-05\|^| L.*R-CNT-05'` → 1 (F7);
  `grep -n 'R-ENC-07'` → 8 hits incl. rows F16, F22, F23, F29, L11, L12,
  L14, L22; `grep -n 'R-ENC-06\]\|R-ENC-03\]…'` → R-ENC-06 at 478, 2954,
  3945 only (no row cites it — consistent with R-ERR-01).
- Controls proving the instrument works: `grep -c 'register'` → 54;
  `grep -n 'whole of the test'` → 1 (3926); `grep -n 'the same check'` →
  1 (3590) — the §21.7 form wraps ("the same / check for every one") and
  was found by reading, which is the hard-wrap caveat in action.

## 11. Rejected candidates

R-1. Hunk 12 "not necessarily the same check for each" — "each" could
be read as each *condition*. Dropped: the nearest distributive noun is
"every file that does not", and §21.1 expressly defers ("§21.7 states the
test for"), where the form is "every one of them" and unambiguous.
R-2. R-ENC-06's own "is invalid at its owning scope" vs §21.7's "not a
state a file can be in". Dropped as a finding: §21.7 [R-ERR-01] is the
document's explicit reading of that clause as vacuous, no reader verdict
differs, and neither hunk 06 nor 18 changed R-ENC-06's text.
R-3. §21.7 "as [R-CNF-13] individuates them" while R-CNF-13 says "as
§21.1 individuates them" — a pointer loop. Dropped: pre-existing, outside
the hunks, and §21.1 does individuate (one row = one malformed condition).
R-4. §7.4 Note's "reader-detectable witness" vs the definition's "reader
or a verifier". Dropped: non-normative, and the note's own next sentence
shows the sets coincide for nesting.
R-5. Hunk 06 cites "§4" for R-ENC-06 and "§4.2" for R-ENC-03 though both
live in §4.2. Dropped: "§4" is true, only less precise.
R-6. Hunk 18's singular "the shifted value" against plural "different
values". Dropped: distributive reading is the only sensible one.
R-7. Hunk 01's "condition" vs §2.3's "requirement". Dropped: pre-existing
in the old text; R-CNF-13 (245–247) sets the condition/requirement
distinction and the sentence uses it deliberately.

## 12. Findings (3)

B-01 — hunk 01 — OVERCLAIM — §2.4 [R-CNF-12] line 324–325. The appositive
"MUST-level conditions, which §21 inventories" asserts §21 inventories the
class; §21.1 (detectable only), §21.7 (unwitnessed conditions have no row;
R-ENC-06 has no row), and R-CNF-02 (conduct rules) deny it, and read
literally it re-keys the duty to the rows, which §21.7 3929–3933 rejects.
Repair: cut the clause — "runs to MUST-level conditions, and a SHOULD
deviation is reported ..." — the preceding sentence already states the
register/MUST relation in the direction that is true; or "MUST-level
conditions, the detectable ones of which §21 inventories". Not byte-level.

B-02 — hunk 06 — UNCONSTRAINED_SIBLING (list-membership) — §19.3 line
2953–2954. "the field widths at which §4 fixes the parse ([R-ENC-06])" is
the one member of a list of checks that names no check: per [R-ERR-01] it
states no condition, so "failure takes each cited rule's own scope" and
"All are decidable" have nothing to bind for it, and an implementer
hunting for the width check either finds none or re-invents the exact
parse (R-CNT-18) already listed. Repair: drop the member, or demote it to a
premise: "— parsed at the widths §4 fixes (`[R-ENC-06]`) — the u64 value
domain of §4.2 (`[R-ENC-03]`) …". Not byte-level.

B-03 — hunk 17 (adjacent, untouched) — UNSWEPT_RESTATEMENT — §21.7 line
3926–3929. "ask whether a breach can be made to leave behind a file no
obliged check separates from one that does not exhibit the condition" is
∃f ∃g ∀k; the definition it calls "the whole of the test" is ∀f ∃g ∀k.
The third form is weaker than the definition, so a condition with one
inseparable exhibiting file and one separable exhibiting file is
unwitnessed by the procedure and detectable by the definition. Repair:
"ask whether every file a breach can leave behind is one no obliged check
separates from a file that does not exhibit the condition." Not
byte-level: it decides rows, and R-CNF-04 binds readers to rows as
written; no file I could construct from the document's own conditions
splits the two forms.

Checks 1–8 otherwise passed on all five hunks as recorded above.
