# Repair audit — hunks 07, 08, 09 (§21.1 gloss, §21.1 sweep, §21.7 rewrite)

## 0. Disclosure

Files opened:
- /private/tmp/.../case-adr0113/hunk-07.diff
- /private/tmp/.../case-adr0113/hunk-08.diff
- /private/tmp/.../case-adr0113/hunk-09.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (many ranges, listed below)

Nothing else. I did not open full.diff, other hunk files, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json,
git history, or the web. I did not list the case directory (I cat'd the three
named files by absolute path).

Unrequested context appeared before I began: a project instruction file
(CLAUDE.md pointing at AGENTS.md) and an index of the maintainer's memory
notes naming a harness spec path and a "lineage gate word list". I read
neither target, and nothing in this audit derives from them. Their presence
is disclosed here; contents not repeated.

Spec ranges read in full:
92-112 (§2.1, [R-CNF-01]), 278-300 (§2.4, [R-CNF-07]), 670-760 (§5.2 byte
coverage + its Rationale + two Notes), 1005-1025 ([R-CNT-13]), 1105-1130
([R-CNT-17], [R-CNT-18]), 1224-1240 (§9.1 [R-LIF-01], §9.2), 1440-1500 (§9.7
coverage verification + its Note), 1728-1760 (§12.1), 2405-2425 (codec 3),
2496-2535 (§17.3 filter, [R-COD-09], [R-COD-10] + Example + Rationale),
2600-2620 (§18.2 encoding 2), 3130-3175 (§20.3 step 4, the §14 bar),
3225-3260 (§20.3 step 4 shrink/rescue), 3401-3470 (§20.5 compaction),
3540-3620 (§21.1 entire), 3641-3810 (register rows F2-R4, sampled by grep),
3855-3995 (§21.6 tail, §21.7 entire, §21.8, §21.9 head).

## 1. What the three hunks are

- **hunk 07** (§21.1, line ~3558-3563): replaces "§21.7 the account, by
  class, of what fails it" with "§21.7 states the test for: a violation is
  detectable exactly where some file exhibiting it differs, in its live
  state, from every file that does not".
- **hunk 08** (§21.1, line 3580): "§21.7's account of what no check detects"
  -> "§21.7's test for what no check detects". A one-word sweep of the same
  characterisation.
- **hunk 09** (§21.7, lines 3882-3983): replaces a single 926-word normative
  paragraph (an inventory of obligations outside the register) with (a) three
  new normative paragraphs — the *unwitnessed* test, the *detectable*
  definition, the *unviolatable* distinction — and (b) the old inventory,
  lightly edited, moved inside a blockquote whose first word is
  **Rationale.**

Header check: hunk 09's stated nearest heading, "21.7 What no check
detects" at line 3864, matches the body (verified: `#### 21.7 What no check
detects` is at 3864). Hunks 07 and 08 state "21.1 How to read the register"
at 3545; verified (`#### 21.1` at 3545). No mismatch.

## 2. The rule each repair adopts, in my words

**hunk 07/08.** §21.1's completeness clause is normative and its gate word
is *detectable*; the gate is now given a definition by reference, and that
definition is informational rather than procedural: a violation counts as
detectable when the file's *live state* distinguishes it, whether or not any
enumerated check looks. §21.7 is recharacterised from an enumeration ("the
account, by class") to a decision procedure ("the test").

**hunk 09.** For an implementation: nothing changes about what any actor must
emit or reject. What changes is how a reader of the document decides whether
a requirement's absence from §21.2-§21.5 is legitimate. Formally the repair
adopts

  U(R)  ≡  ∃ f1 violating R, ∃ f2 satisfying R : live(f1) = live(f2)
           ["a file that violates it and a file that satisfies it CAN
            present identical live states"]
  D(R)  ≡  ∃ f exhibiting the violation : ∀ g not exhibiting it,
           live(f) ≠ live(g)
           ["some file exhibiting it differs, in its live state, from
            every file that does not"]

and asserts D = ¬U ("**Detectability is its negation**"), plus a third
category, "no file can violate", exemplified by [R-ENC-06].

## 3. Check 3 — label, not marker

[R-CNF-01] verbatim (line 104-106): "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative."

Test applied: **the block's opening label**, not the ">" marker. The moved
inventory opens `> **Rationale.** The obligations this test places outside
the register...`. Label = Rationale. Verdict: **non-normative**. The three
new paragraphs (3882-3909) carry no label and are outside any blockquote:
**normative**, and they close with `[R-ERR-01]`, which is §21.7's own
requirement id and appears nowhere else in the document (grep "R-ERR-01" ->
1 hit, line 3909). So [R-ERR-01]'s normative content is now exactly the four
paragraphs 3866-3909, and no longer the inventory.

What that demotion costs is worked in §7 below (finding A-06).

## 4. Check 2 — every citation in the repaired text, opened

| Citation | Where | Claim made | Verdict |
|---|---|---|---|
| `[R-CNF-07]` | hunk 07, §21.7 ¶3 | detectability is "the gate [R-CNF-07] already applies" | **PASS**. §2.4 line 286: "Every detectable file-conformance violation named by this specification is assigned exactly one reader outcome." The word *detectable* is indeed the gate. |
| §21.7 | hunk 07, hunk 08 | "states the test for" detectability | **PASS** (it now does). |
| §21.2 through §21.5 | §21.7 ¶2 | the register's checks | **PASS**. §21.2 at 3628, §21.3 at 3682, §21.4 at 3739, §21.5 at 3776. |
| §9.7 | §21.7 ¶2 | "the live state, which is all §9.7 walks" | **PASS as to §9.7's scope** — line 1442: "A verifier checking [R-CNT-02]'s partition walks the live state only." But see A-07: §9.7 is a *coverage* walk and the sentence is being used to fix what "live state" contains. |
| §2.4 | §21.7 ¶3 | "the outcome classes of §2.4" | **PASS**. §2.4 at 284, table of reject-file / reject-layer / reject-tile / ignore-record / preserve-verbatim. |
| `[R-CNF-11]` | §21.7 ¶1 (untouched) | "unable to check" | not re-verified in depth; untouched by the repair. |
| `[R-ENC-06]` | §21.7 ¶4 | fixed field widths, not a state a file can be in | **PASS as a claim** (unchanged text, merely moved out of the inventory into its own paragraph). |
| §21.6 / §21.9 | hunk 08 context | not part of the register | **PASS**: §21.6 at 3810, §21.9 at 3992. |
| §12.1 | Rationale block | element sizes; uint8 and bool both 1 | **PASS**. §12.1 table (1740, 1745): bool element size 1, uint8 element size 1; "a planar bool plane is sized by packing (§14.3)". Arithmetic P·Bᶜ = P vs ⌈P/8⌉ checks out. |
| §17.3 | Rationale block | "both filter values are length-preserving" | **PASS**. §17.3 (2498-2516): values are 1 = none and 2 = byte-shuffle; "Length is unchanged." Two values, both length-preserving. |
| §14.5 / §14.3 / `[R-SER-08]` / T2 / T4 / T5 / T3 / T14 / T26 / T15 / T17 / T23 / T25 | Rationale block | various | spot-checked T26 (3774) and T17-T22 (3765-3770); consistent with the block's claims. |
| §20.5's "three obligations" of `[R-WRT-06]` | Rationale block | fresh file_id, ignore-lane bits, version_minor floor | **PASS, count verified**: §20.5 has exactly those three trailer obligations — "It MUST mint a fresh file_id" (3419), "The output trailer MUST copy the input's unknown ignore-lane flag bits forward" (3441-3443), "the output's version_minor SHOULD be at least the input's" (3452). Three. §20.5's own "Neither obligation has a witness in the output alone (§21.7)" (3457) refers to the latter two only, which is consistent. |
| §7.4's closing Note | Rationale block, [R-CNT-18] item | — | not opened (block is non-normative and the item is illustrative); noted as unchecked. |

## 5. Check 1 — tense and quantifier

Old wording (deleted): "A second set of obligations is omitted from the
register because **a single file exhibits no witness of their violation**."
Subject set: *obligations already omitted from the register*. Quantifier over
files: effectively universal — no file witnesses.

New wording (normative): "**A requirement of this specification** is
**unwitnessed** where **a file that violates it and a file that satisfies it
can present identical live states**." Subject set: every requirement in the
document. Quantifier over files: **existential over a pair** — it suffices
that *some* violating file and *some* satisfying file coincide.

Two shifts, both silent:

1. Subject widened from "obligations omitted from the register" to "a
   requirement of this specification". The consequent, however, was written
   for the narrow set: "so none is omitted from the register by oversight:
   **there is no condition for a row to carry**."
2. The file quantifier went from universal to existential. An existential
   is satisfied by every *partially* witnessed requirement — the class the
   Rationale block itself spends most of its length describing ("witnessed
   only where...", "*sometimes* witnessed", "witnessed indirectly and only
   sometimes", "neither is assured").

Worked consequence — see A-01.

## 6. Putting the test to requirements (the charter's central exercise)

Reading used: live(f) = the bytes of f's live committed state at their
offsets (§5.2: "Every byte of the live committed state belongs to exactly
one of..."). Alternative readings are treated in A-07.

| # | Requirement | Test's answer | Right answer | Verdict |
|---|---|---|---|---|
| 1 | `[R-CNT-02]` disjointness | not unwitnessed | witnessed (F33, L18) | **right** |
| 2 | `[R-CNT-07]` version_major = 0 | not unwitnessed | witnessed (F18) | **right** |
| 3 | `[R-COD-09]` filter value not 1 or 2 | not unwitnessed | witnessed (a layer row) | **right** |
| 4 | `[R-CNT-03]` writers SHOULD zero gaps | unwitnessed (slack is outside the live state, §5.2) | unwitnessed | **right** — a good result for the test |
| 5 | `[R-CNT-13]` MU = 0 record encoding file offsets | unwitnessed (opaque payload; violation not a function of the bytes) | unwitnessed | **right** |
| 6 | `[R-GEO-06]`, `[R-SER-01]` ordinal mappings | unwitnessed | *partly* witnessed (T2/T4/T5 where §14 constrains a byte) | **wrong in part** — see A-01 |
| 7 | `[R-COD-06]` zstd, incl. undisclosed dictionary | **unwitnessed** | has six rows: T17, T18, T19, T20, T21, T22 | **WRONG** — A-01 |
| 8 | `[R-COD-10]` shuffle stride | **unwitnessed** | has T26 | **WRONG** — A-01 |
| 9 | `[R-MTA-09]` user-metadata document | **unwitnessed** | has R4 | **WRONG** — A-01 |
| 10 | `[R-CNT-18]` "a sub-record MUST NOT itself contain records" | **not unwitnessed** (the nesting is in the live bytes; no satisfying file shares those bytes), hence detectable | §21.7's own block lists it among the omitted, and no row covers depth-beyond-two (L23, L24, L26 are the [R-CNT-18] rows; none is this condition) | **WRONG** — A-02 |
| 11 | `[R-LIF-01]`, `[R-LIF-02]` | antecedent has no referent: the actor is a writer ("a writer MUST NOT modify them", §9.1), no *file* violates it, so "a file that violates it" is empty and the requirement is **not unwitnessed** | unwitnessed — the block's own headline case | **WRONG** — A-04 |
| 12 | `[R-WRT-06]`'s three compaction-trailer obligations | same defect, plus the §9.7 gloss excludes compaction outright | unwitnessed | **WRONG** — A-03, A-04 |
| 13 | `[R-ENC-06]` | not unwitnessed (no violating file) | no file can violate | **right, but only because ¶4 rescues it** — the test alone plus "detectability is its negation" would make it detectable |
| 14 | Any reader/verifier obligation (`[R-CNF-11]`, `[R-RDR-02]`) | not unwitnessed -> detectable -> §21.1 wants a row | no file can violate; not a file-conformance violation at all | **wrong**, mitigated by ¶4 — A-04 |

## 7. Findings

### A-01 — the existential quantifier classifies as *unwitnessed* three requirements that carry register rows

Repaired text (3882-3886): "A requirement of this specification is
**unwitnessed** where a file that violates it and a file that satisfies it
can present identical live states. No check §21.2 through §21.5 states can
separate two such files, so none is omitted from the register by oversight:
**there is no condition for a row to carry.**"

Apply to `[R-COD-06]`. §21.7's own first paragraph (untouched, normative,
3869-3871) names "an undisclosed compression dictionary (`[R-COD-06]`, and
`[R-MTA-09]` ...)" among the things this format does not detect. §17.2
(2415-2418): "Dictionary use the header does not disclose is not detectable
by inspection ... it is a writer violation whose consequence is wrong decoded
content". So a file compressed with an undisclosed dictionary and a file
compressed without one can present identical live states — the violation is a
fact about the writer's process, not about the bytes. The test therefore
returns **unwitnessed** for `[R-COD-06]`, and the consequent asserts "there is
no condition for a row to carry". But §21.4 carries six:

  | T17 | Codec 3 (zstd) and the stored bytes do not begin with the compressed-frame magic 28 B5 2F FD | ... | `[R-COD-06]` |
  | T19 | Codec 3 (zstd) and the frame header carries a nonzero Dictionary_ID | ... | `[R-COD-06]` |

(T18, T20, T21, T22 likewise.) The same falls out for `[R-COD-10]` (test:
unwitnessed, via the mis-stride case §21.7 ¶1 names; but T26 is its row) and
for `[R-MTA-09]` (test: unwitnessed; R4 is its row).

The old sentence could not make this mistake, because its subject set was
"obligations *omitted from the register*" and its file quantifier was
universal. The repair generalised the subject to "a requirement of this
specification" while keeping a consequent written for the narrow set.

Repair: quantify per *violating instance*, not per requirement, and keep the
consequent's subject narrow — e.g. "A violation ... is **unwitnessed** where
every file exhibiting it can be matched by a file that does not, presenting
an identical live state," with the row consequent reading "no row is owed for
an unwitnessed violation" rather than "there is no condition for a row to
carry".

Byte-level: **no**. A verifier is obliged by the rows and by the governing
MUSTs (§17.2: "a reader MUST treat a frame carrying a nonzero dictionary ID
as a validity error at tile scope"); §21.1 already says the rule governs over
the row. No competent implementation drops T19 on the strength of §21.7. The
emittable set and the accept/reject verdicts do not move; what moves is
whether §21.7 is true of the register.

### A-02 — under the new definition `[R-CNT-18]`'s nesting bar is *detectable*, the register omits it, and §21.1's normative completeness clause then convicts the document

§21.1, normative and edited by hunk 07: "Its **completeness is normative** —
a *detectable* file-conformance violation this specification names and the
register omits is a defect in this document, detectability being the gate
`[R-CNF-07]` already applies and §21.7 states the test for: a violation is
detectable exactly where some file exhibiting it differs, in its live state,
from every file that does not".

[R-CNT-18] (1123-1125): "Sub-records are layer-scope records; a sub-record
MUST NOT itself contain records (nesting depth beyond two **is a validity
error at layer scope**)".

A file whose sub-record inline payload contains a further record differs, in
its live bytes, from every file that does not — the nesting is *in* the live
state. So under the new definition the violation is **detectable**, and it
carries an assigned outcome already (layer scope), which is [R-CNF-07]'s
signature for a detectable violation. The register's [R-CNT-18] rows are L23
(payload region overrun), L24 (reserved-range sub-record type, MU = 1) and
L26 (a layer record nested as a sub-record — depth two, not beyond two). None
covers nesting beyond two. By §21.1's own normative clause that omission is
"a defect in this document".

Before the repair, "detectable" was undefined and §21.7 excused the omission
in procedural terms ("detectable only by parsing a payload no format-major-1
reader parses as a record sequence" — still in the block, 3930-3932). The
repair replaced the procedural sense with an informational one in the
normative text while leaving the procedural sense in the illustration. That
is precisely the "term defined in one section and used in another on
different terms" shape. The document's other uses of the word are procedural
too: 1170 "no reader-detectable", 2416 "not detectable **by inspection**",
2418 "the same undetectable class", 3774 "is undetectable".

Repair: either (i) make the definition procedural — "detectable where some
check this document obliges an actor to perform can separate it" — or (ii)
keep the informational definition and add the missing row for nesting depth
beyond two.

Byte-level: **no**, on the discriminating question. The disputed file
violates a MUST, so [R-CNF-05] bars every conforming writer from emitting it
under both readings; and with no row and no detection assignment
([R-CNF-04]/[R-CNF-11] work through rows), no verifier is obliged to look, so
verdicts do not fork either. What forks is whether the document is
self-consistent.

### A-03 — "Detectability is its negation" is false of the two definitions as they are quantified

3891-3895: "**Detectability is its negation**, and this is the gate
`[R-CNF-07]` applies ... a violation this specification names is
**detectable** exactly where **some file** exhibiting it differs, in its live
state, from **every file** that does not."

¬U is a universal over pairs ("*every* violating file differs from *every*
satisfying file"); D is an existential over violating files ("*some* file
exhibiting it"). D ⇏ ¬U. For any requirement some of whose violations are
witnessed and some not — which is the majority of the illustration's own
items — both U and D hold at once, so the requirement is simultaneously
unwitnessed (excused from the register) and detectable (required by §21.1's
normative completeness clause to be in it). §20.3 step 4's §14 bar is the
document's own worked example: the block says it "is witnessed only where the
affected tiles remain stored, and then only for part of what it bars", and
names T3 and T14 as catching part of it.

Note also that the two predicates have different subjects: U is stated of "a
requirement", D of "a violation". Equating them across that shift is the
whole of the error.

Repair: state both over violations, both existentially or both universally,
and say explicitly that a requirement with both witnessed and unwitnessed
violations is registered for the witnessed ones.

Byte-level: **no** — same reasoning as A-01.

### A-04 — the test's antecedent has no referent for every requirement whose actor is not a file

"a file that violates it": §9.1's `[R-LIF-01]` binds a writer ("a writer MUST
NOT modify them"); `[R-WRT-06]` binds a compactor; §20.3 step 4's §14 bar
binds a commit ("A commit MUST NOT change a layer's declarations..."). No
*file* violates any of them. The antecedent is therefore unsatisfiable, the
test returns "not unwitnessed", and with "detectability is its negation" they
come out detectable — the exact opposite of what §21.7 says of them two
paragraphs later ("the §14 bar is unwitnessed there for the same reason
`[R-LIF-01]` is"). The block concedes the test wins: "where an item here and
the test above disagree, **the test governs**".

The deleted text did not have this problem: it said "a single file exhibits
**no witness of their violation**" — witness-in-a-file, not violation-by-a-
file — and it framed [R-LIF-01]/[R-LIF-02] as "properties of a file's
history".

The same antecedent failure sweeps in every reader-, verifier- and updater-
facing requirement, pushing them all into §21.1's completeness clause. ¶4's
"no file can violate" category catches them only if a reader thinks to apply
it; ¶4 is written about field widths, not about actors.

Repair: restore the witness framing — "where no file exhibits a witness of
its violation: a file whose live state is consistent with the requirement
having been met and with its having been broken".

Byte-level: **no**.

### A-05 — the §9.7 gloss narrows the test to breaches by a commit, excluding compaction

3887-3890: "ask whether the breach can be **made to leave the live state** ...
**exactly as a conforming commit would leave it**."

This is the repair's own gloss on its test and it is an "exactly as" analogy.
Verbs side by side: the definition's is "**can present** identical live
states" (of two files, however produced); the gloss's is "**can be made to
leave** the live state ... as **a conforming commit** would leave it" (of an
act of committing). Different sets. §9.1 (`[R-LIF-01]`): "every conforming
mutation of a file is either **a commit** (§9.2) **or a whole-file rewrite
under a new file_id (compaction, §20)"; §20.5: "That a compaction is a
whole-file rewrite **rather than a commit**". So the gloss excludes
compaction — and `[R-WRT-06]`'s three compaction-trailer obligations are the
illustration's closing and most detailed unwitnessed case, cross-referenced
from §20.5 ("Neither obligation has a witness in the output alone (§21.7)").
It also excludes a creator's first write, which is where `[R-COD-06]`'s and
`[R-COD-10]`'s unwitnessed breaches actually occur.

Repair: drop "as a conforming commit would leave it" or widen it to "as a
conforming writer would leave it".

Byte-level: **no**.

### A-06 — the reconciliation §21.1's normative completeness clause depends on is now non-normative, and two normative sentences point into it

§21.1's completeness clause is expressly normative. What discharges it for
the partially witnessed obligations is the identification of which rows catch
which instances — "witnessed by T2, T4 or T5", "witnessed by T3 or T14",
"witnessed by the rows for the codec now declared ... (T15, T17, T23, T25)",
"caught by T3, or by T14 under codec 1". Every one of those sentences is now
inside the **Rationale.** block and carries no force ([R-CNF-01]). The
replacement normative text is bivalent and does not reconcile them (A-03).

Two normative sentences elsewhere lean on the demoted text by name:
- §20.3 step 4 (3239-3242): "**§21.7 records the consequence** — that this is
  precisely where the §14 bar has no witness, the live state being clean —
  which is why the rule is stated here and not left to the rows." The record
  it names is now at 3972-3976, inside the Rationale block.
- §20.5 (3457): "**Neither obligation has a witness in the output alone
  (§21.7).**" The supporting account is now at 3976-3983, inside the block.

Both citations remain *literally* true (§21.7 does still contain the words),
and both sentences state the fact themselves, so nothing is left unstated.
But a reader following either pointer lands in text the document declares
non-normative, and the discharge of a normative completeness clause is no
longer normative anywhere.

Repair: keep the row-attribution sentences (which rows witness which partial
breaches) in normative text and demote only the narrative.

Byte-level: **no**.

### A-07 — check 8: "A second set of obligations" now counts from the wrong antecedent

Before the insertion, the block's opening sentence sat immediately after the
paragraph ending "no file-level witness exists to check", whose subject was
the *first* set: wrong sample content — mis-strided filter, undisclosed
dictionary, "or simply wrong data". "A second set" resolved to that.

Three paragraphs now intervene: the unwitnessed test, the detectable
definition, and the "no file can violate" class. The nearest preceding
grouping is now `[R-ENC-06]`'s unviolatable class, and the block is now at
least the *third* grouping the section describes. The referring sentence did
not change a word and no diff shows the re-resolution.

Other back-references checked:
- "**Detectability is its** negation" — "its" -> the unwitnessed test
  ("That is the whole of the test"). Unaffected, correct.
- "and **this** is the gate [R-CNF-07] applies" -> detectability. Correct.
- "a claim about **those** and no others" -> detectable violations. Correct.
- "absent from **it** by the clause's own terms rather than in breach of
  **them**" -> "it" = the register, "them" = the completeness clause's terms.
  Slightly strained (the nearest noun to "it" is "The register's
  completeness") but resolvable; unaffected by the insertion.
- "**the test above** governs" (inside the block) -> the unwitnessed test
  at 3882. The nearest preceding paragraph is the [R-ENC-06] one, which is a
  distinction rather than a test, so this still resolves correctly, but only
  just.
- "so the **§14 bar** is unwitnessed there" — the repair replaced a bare "the
  bar" with "the §14 bar" here and at 3933. That is a correct sweep and the
  anaphor now resolves to §20.3 step 4's named bar rather than to the nearest
  preceding "bar". **Good repair, reported as passing.**
- "For **the last two** there is a second" -> ignore-lane bits and
  version_minor. Correct; §20.5's own "Neither obligation" agrees.

Repair: "A second set" -> "Obligations of a second kind", or restore the
adjacency by moving the first paragraph's summary into the block.

Byte-level: **no**.

### A-08 — overclaim: "it decides any requirement put to it without appeal to a list"

3886-3888: "That is the whole of the test, and **it decides any requirement
put to it without appeal to a list**".

Falsified from within the same subsection: two paragraphs later the document
must add a second, independent category — "Distinguish an unwitnessed
requirement from one **no file can violate**" — because the test alone gives
`[R-ENC-06]` an answer ("not unwitnessed", hence by the negation claim
"detectable") that the document then has to correct by hand. If the test
decided any requirement, that paragraph would not be needed. It is also
falsified by A-04's class (requirements no file can violate because their
actor is a reader, verifier, updater or writer) and by A-01's class
(partially witnessed requirements, which it decides *wrongly*).

Two further exhaustive claims in the repaired normative text, tested:
- "No check §21.2 through §21.5 states can separate two such files" —
  **holds** if every register check reads only the live state. I looked for a
  row that reads outside it: slack content is unconstrained (§5.2, [R-CNT-03])
  so no row reads it; F/placement rows read offsets, which are part of the
  live state. Passes.
- "there is no condition for a row to carry" — fails, see A-01.
- "The register's completeness is a claim about those and no others" — this
  is a claim about §21.1, and §21.1 as edited does say exactly that. Passes.

Repair: "it decides any requirement whose violation a file can exhibit".

Byte-level: **no**.

### A-09 — "identical live states" is undefined, and the §9.7 gloss admits a reading that empties the content rows

"live state" is used 20 times in the document but the phrase "identical live
states" introduces a comparison the document has never made. §5.2 defines the
**live committed state** as "the front signature block, and every structure
reachable from the live trailer ... Every byte of the live committed state
belongs to exactly one of ...", which supports a byte-content reading. But the
repair's gloss ties it instead to a walk: "the live state, **which is all
§9.7 walks**", and §9.7 is *Coverage verification* — it enumerates claimants
and checks disjointness, bounds and checksums, and says of the bytes it does
not reach that "their content is not its concern".

Under a claimants-and-extents reading, two files differing only in the fill
byte at a padding position present identical live states, so §14.5 /
`[R-SER-05]` is "unwitnessed" and "there is no condition for a row to carry"
— yet T2 and T4 are exactly those rows. Under the byte-content reading the
test behaves (see §6 above). Nothing in the repaired text picks the reading,
and the one cross-reference it supplies points at the walk rather than at
§5.2's byte definition.

Repair: "present identical live states (§5.2: the same bytes at the same
offsets in every structure the live committed state claims)".

Byte-level: **no** — a verifier does not drop T4 because of §21.7; the rows
and their governing rules stand and §21.1 gives the rule precedence.

### A-10 — §18.2 restates the pre-repair notion and was not swept, and one of its two members fails the new test

§18.2 (2610-2615), normative, untouched: "**Two of those carry no witness a
file exhibits**, and R4 registers neither: dictionary use the header does not
disclose is a writer violation nothing in the extent shows, exactly as
`[R-COD-06]` has it for a tile (§21.7), and **the bar on sizing a buffer
binds a reader rather than the document**."

This is the same concept the repair has just made a defined term
(**unwitnessed**) with a stated test, stated here in the old prose and not
swept. Worse, its two members now fall on opposite sides of the new
apparatus: the undisclosed dictionary is unwitnessed under the test, while
"binds a reader rather than the document" is A-04's case — the test's
antecedent has no referent, so it is *not* unwitnessed, and belongs (if
anywhere) in ¶4's "no file can violate" class, which §21.7 illustrates only
with field widths. §18.2 also cites §21.7 for the analogy ("exactly as
`[R-COD-06]` has it for a tile (§21.7)"), and after the repair §21.7's
support for that is inside the Rationale block.

Repair: sweep §18.2 to the defined term and split its two members —
"Neither is registered by R4: the first is **unwitnessed** (§21.7), the
second binds a reader and so is not a file-conformance violation at all."

Byte-level: **no**.

## 8. Check 6 — what the repair left unconstrained

Structure governed: the classification of every requirement in the document
against the register. Its members, enumerated:

  (a) a requirement every violation of which the live state shows;
  (b) a requirement no violation of which the live state shows;
  (c) a requirement no file can violate because the state it forbids is not
      a state ([R-ENC-06]);
  (d) a requirement no file can violate because its actor is a reader,
      verifier, updater or writer-process ([R-CNF-11], [R-RDR-02], the
      buffer-sizing bar of §18.2);
  (e) a requirement **some** of whose violations the live state shows and
      some of whose it does not ([R-COD-06], [R-COD-10], [R-MTA-09],
      [R-GEO-06], [R-SER-01], §20.3 step 4's §14 bar and its companion
      ordinal bar);
  (f) a requirement over a *transition* rather than a state ([R-LIF-01],
      [R-LIF-02], [R-WRT-06], §20.3 step 4).

The repair pins (a), (b) and (c). (d) is arguably covered by ¶4's wording but
is nowhere named and ¶4's example points the reader elsewhere. **(e) is
governed by nothing** — or rather by two rules pointing opposite ways, §21.7
excusing it and §21.1 demanding it (A-01, A-03). **(f) is mis-sorted** by the
antecedent (A-04). (e) is the largest class in the illustration by word
count, and the repair replaced the prose that handled it with a test that
does not.

## 9. Check 4 — contradictions with untouched text in the same passage

Looked for and **found**:
- §21.7 ¶1 (untouched) naming `[R-COD-06]`, `[R-COD-10]`, `[R-MTA-09]` as
  content-incorrectness cases, against §21.4/§21.5's rows for all three, with
  the new test calling all three unwitnessed. (A-01)
- §21.7 ¶4's "no file can violate" category against ¶2's claim that the test
  "decides any requirement put to it". (A-08)
- §18.2's "carry no witness a file exhibits". (A-10)
- §20.3 step 4's "§21.7 records the consequence" and §20.5's "Neither
  obligation has a witness in the output alone (§21.7)" against the demotion.
  (A-06)

Looked for and **not found**:
- A MUST the repair's new text lets an actor violate: none. The repair states
  no permission and no obligation on any actor; it is entirely about how the
  register is to be read. "Being unwitnessed bears on detection and not on
  permission: the requirement binds its actor as any other does" is a
  correct and welcome guard, and I checked it against §2.4's outcome table
  and [R-CNF-05]; no conflict.
- A carve-out the repair's new breadth collides with: §21.1's "subject to the
  same exception stated above, a rule that assigns an outcome expressly" is
  about outcome assignment, untouched by the detectability gloss.
- hunk 08's "neither this completeness clause nor the instance arithmetic
  below reaches ... §21.7's test" against hunk 07's making the clause *turn
  on* §21.7's test: **not** a contradiction. "Reaches" there means "requires
  rows of"; §21.7 supplying the gate's definition is a different relation.
  Reported as checked and passing.
- The Rationale block's internal precedence sentence ("where an item here and
  the test above disagree, the test governs") is itself non-normative, so it
  cannot bind. Harmless: [R-CNF-01] already denies the block force, so the
  sentence is redundant rather than wrong. Not reported.
- §5.2's Note ("a register row for it would be a row no file could exhibit")
  describes a member of ¶4's unviolatable class that §21.7 does not name.
  ¶4 does not present itself as a closed list ("`[R-ENC-06]`'s fixed field
  widths are not a state a file can be in" is an instance, not an
  enumeration), so this is not an overclaim. Not reported.

## 10. Greps run, verbatim, with hit counts

    grep -n -i "detectab" spec/tarn.md                     -> 10 hits
      (286, 1170, 2416, 2418, 2521, 3548, 3558, 3559, 3561, 3891, 3893, 3931
       — 12 lines; "detectab" stem)
    grep -n -i "live state" spec/tarn.md                   -> 20 hits
    grep -n "R-COD-06\|R-COD-10\|R-ERR-01\|R-CNF-07\|R-MTA-09" -> 22 hits
    grep -n "R-CNT-18\|R-CNT-13" spec/tarn.md              -> 30 hits
    grep -n "21\.7" spec/tarn.md                           -> 7 hits
    grep -n "R-CNF-01" spec/tarn.md                        -> 1 hit (line 106)
    grep -n "unwitnessed\|no witness\|witnessed" spec/tarn.md -> 16 hits
    grep -n "^#### 21\.\|^#### 17\.\|^#### 20\.\|^#### 12\.1\|^#### 14\." -> 22 hits

Wrap caution observed: I searched only short fragments that cannot wrap
("detectab", "live state", "21.7", requirement ids, "witness"). I did not
draw any conclusion from a failed multi-word grep.

## 11. Derived numbers

- Register rows whose Governing rule cell is `[R-COD-06]`: **6** (T17, T18,
  T19, T20, T21, T22). §21.7's test implies 0 conditions for it.
- Rows whose Governing rule is `[R-COD-10]`: **1** (T26). Test implies 0.
- Rows whose Governing rule is `[R-MTA-09]`: **1** (R4). Test implies 0.
- Rows whose Governing rule is `[R-CNT-18]`: **3** (L23, L24, L26); rows
  covering "nesting depth beyond two": **0**. §21.1's completeness clause,
  with the new definition, requires ≥ 1.
- §20.5 trailer obligations on `[R-WRT-06]`: **3** — matches the block's
  "three obligations" and its "all three share"; §20.5's local "Neither
  obligation" covers **2** of them, which is consistent.
- §12.1 element sizes: bool = 1, uint8 = 1 (13 types listed, "exactly
  thirteen" — count of table rows is 13, matches). Planar plane sizes:
  uint8 P · 1 = P bytes; bool ⌈P/8⌉. The block's claim that element size
  does not decide the case checks out.
- §17.3 filter values: **2** assigned (1 and 2); both length-preserving
  ("Length is unchanged"). The block's "both filter values are
  length-preserving" matches.
- Predicate arity: U is ∃∃, D is ∃∀. ¬U is ∀∀. D ≠ ¬U. (A-03.)

## 12. Rejected candidates

1. *"Detectability is its negation" leaves `[R-ENC-06]` detectable, which
   §21.1 then requires a row for.* Opened; partly closed by ¶4's explicit
   "Nothing is omitted from the register on its account, there being no
   condition to omit", which forecloses the §21.1 consequence directly.
   Folded into A-08 as evidence of the overclaim rather than reported as its
   own defect.
2. *hunk 07's insertion breaks the "— but each row *restates*" resumption.*
   The em-dash now trails a colon-introduced definition rather than the gate
   clause. Read aloud twice; the resumption still attaches to "Its
   completeness is normative". Stylistic, not a defect. Dropped.
3. *§21.8's "120 conditions over 275 instances" may be stale.* Not in my
   hunks, not touched, and I did not recount. Not reported; flagged here as
   unchecked.
4. *The Rationale block contains a MUST ("the unknown ignore-lane bits it
   MUST carry forward").* A restatement of §20.5's own MUST, now correctly
   non-normative. Not a defect — arguably an improvement.
5. *§5.2's Note names a second unviolatable requirement §21.7 omits.* ¶4 is
   not a closed list. Dropped (see §9).
6. *The block's "an item found stale is a defect in this block and not in the
   register" tries to reallocate §21.1's normative defect finding from
   non-normative text.* Non-normative text cannot override normative text, so
   the sentence is inert rather than wrong. Dropped.
7. *"a mis-ordered image is then witnessed by T2, T4 or T5" — three rows
   named; is T5 real?* Present in §21.4's range; not individually opened, and
   the block is non-normative. Not reported.
