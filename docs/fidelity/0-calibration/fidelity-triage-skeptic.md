# Triage — Skeptic lens — working notes

## Disclosure

The 67 findings under review, their ids, quotes and citations, arrived in my
context as the computed task itself (harness-assembled), before I began any
reading. I am treating that material as the claims to check, not as evidence
of what the editions say — every quote I rely on below was independently
re-read from the two files at the cited byte/line location during this
session, not trusted from the findings' own quotes. I did not list any
directory. I opened only:
 - editions/a/tarn.md, editions/b/tarn.md (by name, full reads of the cited
   sections plus a full `diff` of both complete files)
 - no transcript-*.md files were opened; the 67 findings as given carry full
   quotations and citations, and cross-checking those against the two
   editions directly was sufficient to grade every group without needing the
   reporters' own reasoning chains beyond what is quoted in the findings
   text supplied.

## Method

Two editions are ~4980 hard-wrapped lines each (4981 / 4977). Rather than
grep short fragments (risky across hard-wrap reflow), I ran a full-file
`diff editions/a/tarn.md editions/b/tarn.md`. This is immune to the
hard-wrap/grep problem: diff compares every line of both files; a real
content edit anywhere would show up as a hunk (if edited text reflows a
paragraph's wrapping, MORE lines show as changed, never fewer — so the
method cannot silently miss a difference). The control check: the line-count
delta (4981 − 4977 = 4) exactly matches the net line delta implied by the
hunks found (−1 −1 +0 −2 +0 = −4), cross-confirming the diff is complete and
not truncated.

Result: **the entire ~302 KB document is byte-identical between edition A
and edition B except for six localised hunks.** Full diff output:

```
908,909c908
< copy forward unknown ignore-lane bits of its input file, MUST
< NOT clear them, and MUST NOT set any other: no writer under this text
---
> copy forward unknown ignore-lane bits of its input file, MUST NOT set any other: no writer under this text
3219,3220c3218
<    freezes the committed prefix — and MUST NOT drop the record save
<    where §20.4 licenses the drop.
---
>    freezes the committed prefix — and MUST NOT drop the record.
3400c3398
< > bytes), the layer's full new index region (32 · 20 + 4 = 644
---
> > bytes), the layer's full new index region (32 · 20 + 4 = 664
3497,3498c3495,3496
< whichever flags govern it. Its MU = 1 row reaches only a type the
< updater does not implement — an updater implements both registered
---
> whichever flags govern it. Its MU = 1 row reaches every type,
> implemented or not — an updater implements both registered
3512,3514c3510
< whatever their PE bits. One sub-record blocks the drop, a sub-record
< of a type the updater does not implement with MU = 1, the drop being
< a modification of the scope it governs (the table's first row). A
---
> whatever their PE bits. A
3863c3859
< | F19 | ... | flags bits 0-15 | reader | open | `[R-CNT-08]` |
---
> | F19 | ... | flags bits 0-7 | reader | open | `[R-CNT-08]` |
```

This gives a hard floor for the skeptic lens: **every one of the 67
findings must cash out as one of these six hunks, or as a claim about text
that is provably identical in both editions** (in which case it cannot be a
fidelity LOSS/ADDITION between A and B — at most it is REPORTER_ERROR, or an
OBSERVATION about a defect/gap shared equally by both editions, which grades
EQUIVALENT under "a difference ... that changes nothing the two texts
decide" — here there is not even a difference of wording).

I independently re-opened both editions at each of the six hunk locations,
plus at every section the walker/quiz findings cite outside those six
locations, to confirm this partition. Findings and exact line ranges
checked, with sub-findings noted below.

## Hunk-by-hunk re-judging (skeptic)

### H1 — §6.3 [R-CNT-08], ignore-lane "MUST NOT clear them" clause
A (line 908-909): "...MUST copy forward unknown ignore-lane bits of its
input file, MUST NOT clear them, and MUST NOT set any other..."
B (line 908): "...MUST copy forward unknown ignore-lane bits of its input
file, MUST NOT set any other..."

Skeptic search of B for the rule: §6.2's structural-field table row for
`flags` (line 838, **byte-identical in both editions**, not part of any
hunk): "bits 16–31 (ignore lane) 0 from a creator, **carried forward
unchanged by every updater** (appender and rewriter alike), a set bit
ignored (§6.3)". "Carried forward unchanged" is a stronger and more general
statement than "copy forward ... MUST NOT clear them": it binds the *whole*
ignore lane to the input's exact bit pattern, which already forecloses
clearing any bit that was set. This sentence sits in a paragraph the diff
proves is identical in both editions, so it is not something I am crediting
to B's editor — it was already there in A, already doing this work, before
the deletion. The deleted clause in §6.3 was redundant with the unaffected
§6.2 table cell in A too.
Verdict: **EQUIVALENT**. Not byte-level: an implementation satisfying
"copy forward ... MUST NOT set any other" (B) or "carried forward unchanged"
(both editions, §6.2) cannot clear a bit while conforming; no other
implementation is licensed by either edition to clear one.
Ids: cmp-reader-01, cmp-writer-06, cmp-verifier-06, swab-01, adv-05.

### H2 — §20.3 step 2, appender "MUST NOT drop the record [save where §20.4 licenses the drop]"
A (line 3219-3220): "...MUST NOT drop the record save where §20.4 licenses
the drop."
B (line 3218): "...MUST NOT drop the record."
§20.4 (unchanged both editions, confirmed by the diff showing no hunk there
apart from H4/H5 below): "MU = 0, PE = 0 | Retain byte-identical, or drop
it ... so an appender MAY drop the record in any commit it is otherwise
free to make". This is an unconditional MAY-drop licence for exactly the
class of record step 2's unqualified MUST-NOT-drop (in B) forbids dropping.
Skeptic search of B for a reconciling sentence anywhere in normative text:
none found. The only surviving occurrence of "§20.4 licenses the drop" in B
is inside the non-normative "Example — the three shapes a commit takes"
block (§20.3, line 3441, confirmed present and unchanged — checked
directly), which under [R-CNF-01] (identical, both editions, line 107)
states no requirement. So B's normative text contains a genuine, unresolved
contradiction between an absolute prohibition (step 2) and an unconditional
permission (§20.4) that A explicitly reconciles and B does not.
Verdict: **LOSS, BYTE-LEVEL**. An appender built strictly from B's step 2,
taken as the ordered procedure it is (a "MUST, in order" list), has no
license to drop an MU=0/PE=0 record it carries forward, and would retain
bytes (header, inline payload, extent slot) that an A-built appender (or a
B-built one that instead resolves the contradiction toward §20.4) discards.
Different directory bytes for the same requested edit.
Ids: cmp-reader-02, cmp-writer-02, cmp-verifier-03, swab-02, swba-01, adv-01.

### H3 — §20.3 worked Example, index-region arithmetic 644→664
A (line 3400): "32 · 20 + 4 = 644 bytes"
B (line 3398): "32 · 20 + 4 = 664 bytes"
32×20+4 = 644 (verified by direct arithmetic); B's stated result does not
equal its own printed formula on its own printed inputs — a clean
arithmetic slip. R-CNT-17's general formula (entry_count×20 +
⌈entry_count/2¹⁶⌉×4) is unchanged, correct, and identical in both editions
(confirmed no hunk there), so a conforming writer's/reader's/verifier's
*actual* extent_length check is governed by the formula, not by this
worked total. The passage is inside a block labelled "Example.", and
[R-CNF-01] (identical both editions) makes Note/Example/Rationale blocks
non-normative.
Verdict: **LOSS** (a worked figure A states correctly and B states
incorrectly — the charter's own "worked figure" clause), but **not
byte-level** for a conforming implementation: nothing in the register or
any R-ID is keyed to the example's own total (only to the general formula,
unaffected). I disagree with the byte-level tag some passes attach (via a
hypothetical vector-author who trusts the example over deriving from the
formula) — that is a corpus-authoring risk, not a divergence between what a
spec-following implementation of A vs. B would emit; a vector author
"built from B alone" who reads the whole of B, including the correct and
still-normative R-CNT-17, derives 644 regardless of the Example's error.
Severity: content (real defect, fix the arithmetic) rather than byte-level.
Ids: cmp-reader-03, cmp-writer-05, cmp-verifier-04, swab-03, swba-02,
adv-02, writerb-01.

### H4 — §20.4, MU=1 row's stated scope: "only a type ... does not implement" → "every type, implemented or not"
A (line 3497-3498): "Its MU = 1 row reaches only a type the updater does
not implement ... so for an implemented type only the PE bit bites."
B (line 3495-3496): "Its MU = 1 row reaches every type, implemented or not
... so for an implemented type only the PE bit bites."
Skeptic check: the table's own MU=1 row text three lines below (unchanged,
identical both editions): "At layer scope an **unknown** critical record
blocks modification of that layer..." — "unknown" here does restrict that
specific consequence (layer-drop blocking) to unimplemented types, which
weighs toward EQUIVALENT for *that* clause. But B's intro sentence is not
limited to the layer-drop consequence: it is the general premise for the
whole MU=1 row ("Retain byte-identical. The updater MUST NOT modify the
scope the record governs"), and B's own next clause in the same sentence
("so for an implemented type only the PE bit bites") only follows
logically from A's premise, not from B's. I could not find, anywhere in B,
a sentence that resolves this in the implemented-type direction the second
clause needs. Concretely: an updater implementing an unregistered type from
its own definition (this paragraph's own scenario, both editions), where
that definition's flags happen to be MU=1 on a sub-record the commit does
not touch — under A, the row does not reach it, only the PE-bit rows
matter; under B's literal first clause, the row does reach it, and "retain
byte-identical, MUST NOT modify" would forbid a commit that A's own text
permits.
Verdict: **LOSS, BYTE-LEVEL**. Two updaters built from B's literal text,
resolving its self-contradiction in the two different directions its own
sentence offers, diverge on whether a commit touching such a record is
legal — a genuine accept/reject and byte-output difference not present
under A (which has only one reading).
Ids: cmp-reader-04, cmp-writer-03, cmp-verifier-01, swab-04, swba-03, adv-03.

### H5 — §20.4, "One sub-record blocks the drop..." sentence deleted
A (line 3512-3514): "...whatever their PE bits. One sub-record blocks the
drop, a sub-record of a type the updater does not implement with MU = 1,
the drop being a modification of the scope it governs (the table's first
row). A commit never removes..."
B (line 3510): "...whatever their PE bits. A commit never removes..."
Skeptic search of B for the rule: the table's MU=1 row itself, three lines
*above* this paragraph, unchanged in both editions (see H4's quote): "At
layer scope an unknown critical record blocks modification of that layer,
**its drop included**, leaving other layers editable (`[R-CNT-18]`)." This
states exactly the fact the deleted sentence restates, and the deleted
sentence even names its source ("the table's first row") — it was a
cross-reference back to content that is still there, verbatim, in B. A
rewriter or updater built from the whole of B's §20.4 (table + prose) is
still bound not to drop a layer carrying an unimplemented-type MU=1
sub-record.
Verdict: **EQUIVALENT**. Not byte-level: the blocking rule survives
unchanged in the table row that governs it. Severity: clarity, not none —
I flag (as swab-05 does) that a reader of only the local paragraph in B,
stopping at "A commit MAY therefore drop a layer record, and the drop
takes the layer whole ... whatever their PE bits," could walk away with an
unqualified impression; the correction is three lines up, not local. This
is a readability regression, not a lost rule.
Ids: cmp-reader-05, cmp-writer-01, cmp-verifier-02, swab-05, adv-06.

### H6 — §21.2 register row F19, Instances cell "flags bits 0-15" → "flags bits 0-7"
A (line 3863) / B (line 3859): Condition cell identical in both editions:
"Any bit of the flags incompat lane (bits 0-15) is set...". Instances cell:
A "flags bits 0-15", B "flags bits 0-7".
Skeptic check of the governing text: §21.1 (unchanged both editions,
confirmed no hunk there): "each row *restates* its governing rule, and
where a row and the rule it cites diverge, **the rule governs**." The
governing rule here, [R-CNT-08] (§6.3, unchanged: "a reader MUST
reject-file on any set bit it does not implement in the incompat lane
(bits 0-15)"), is unqualified across all of bits 0-15 in both editions.
So a reader/verifier built from the whole of B — including §21.1's own
explicit precedence instruction and §6.3's rule — still rejects a file
with, say, bit 10 set; the Instances cell's narrowing does not license
accepting it, because the register is stated to be a restatement, not the
rule itself.
Verdict: **LOSS** (a quantifier A states more widely than B, per the
charter's own definition — the Instances cell is exactly that). Not
byte-level for a *conforming* implementation, because §21.1's own
precedence clause (identical in both editions) already resolves the
register/rule conflict in favor of the wider rule. I disagree with the
stronger byte-level claims (which construct a verifier that reads only the
Instances cell and ignores §21.1's precedence clause and §6.3's rule — that
is not "an implementation built from B alone," it is an implementation
built from one B table cell in isolation, contrary to B's own explicit
instruction for how to read that cell). The real, surviving harm is to
§21.8's conformance-vector-coverage promise (R-VEC-02/R-VEC-03): a corpus
built mechanically off this row's Instances cell, per the register's own
stated purpose, would omit vectors for bits 8-15. Severity: content.
Ids: cmp-reader-06, cmp-writer-04, cmp-verifier-05, swab-06, adv-04,
readerb-02.

## Shared indeterminacies / shared defects (no hunk at all — text identical)

Checked directly (each against the full diff, confirming no hunk in the
cited range):

- **writera-01 / cmp-writer-07** — §9.1, §20.3 step 4 escape-hatch sentence,
  §21.9/[R-CNT-13]: the zero-copy drop-and-recreate ambiguity. All cited
  text confirmed byte-identical (it sits well outside all six hunks).
  EQUIVALENT — the ambiguity, if real, is equally present/absent in both
  editions; it is not something one edition resolves and the other doesn't.
- **writera-02 / cmp-writer-08** — [R-WRT-03] and its citations, §11.1's
  Rationale note: byte-identical, no hunk nearby. EQUIVALENT.
- **cmp-verifier-07 (V1)** — §2.3 [R-CNF-11] verdict vocabulary: identical,
  no hunk. EQUIVALENT.
- **cmp-verifier-08 (V2)** — §10.2, F35/F36, §21.6: identical, no hunk.
  EQUIVALENT.
- **cmp-verifier-09 (V3)** — §5.1/§5.2/§9.2/§20.3/§9.7/[R-CNT-17] formula:
  identical, no hunk (distinct from H3's example — different entry_count,
  same unaffected formula). EQUIVALENT.
- **cmp-verifier-10 (V4)** — §17.4 [R-COD-11]: identical, no hunk.
  EQUIVALENT.
- **cmp-verifier-11 (V5)** — §20.3 step 4 fixed-declaration bar, §9.7:
  identical, no hunk. EQUIVALENT.
- **cmp-verifier-12 (V6)** — §7.2 [R-CNT-12], F25, L46: identical, no hunk.
  EQUIVALENT.
- **verifiera-01, verifiera-02, cmp-verifier-13** — §2.3/§21.6
  (uncertifiable-but-conforming file) and §21.1 (subsumption list "not
  offered as closed", quoted verbatim, confirmed present in both editions
  identically): both are genuine properties of the specification's design,
  present equally in both editions. EQUIVALENT (design property shared by
  A and B, not a fidelity difference between them).
- **verifierb-01, verifierb-02, cmp-verifier-14** — §5.2/§9.7/§17.4
  (R-COD-11 absent from the partial-total trigger list) and §20.3 step
  4/§21.7/§9.7 (silent fixed-declaration-bar violation undetectable):
  confirmed byte-identical in both editions (§5.2's precise trigger-list
  text — "a tile's or a document's decode declined leaves the walk
  complete" vs. "the verifier declined a layer on resource grounds" — was
  read directly at lines ~715-725 of A and is unchanged in B). EQUIVALENT.
- **readera-01, readerb-01** — §17.4 [R-COD-11], §2.3 [R-CNF-03], §21.6,
  §21.9: no outcome class for a reader lacking a mandatory codec/filter.
  Same underlying observation, found independently by both the A-walk and
  the B-walk, resting on text confirmed identical in both editions (no
  hunk anywhere near §17.4/§21.6/§21.9/§2.3 other than nothing). This is a
  pre-existing document gap present equally in A and B, not something one
  edition states and the other omits. EQUIVALENT.

## Quiz-matrix items (quiza-*, quizb-*)

None of the sections these 14 items cite (§20.3 step 4's fixed-declaration
paragraph, §11.2, §7.4/§15.1, §20.5, §14.2, §17.2, §21.3 rows L22/L44/T7,
§6.1, §19.1, §11.2/11.3, §14.5, §4.1, §13.1/§13.3/§3.2, §17.3, §5.2/§9.7,
§6.2/§6.3's ordered-validation sentence, §10.2) fall inside any of the six
hunks. I re-opened the exact quoted passages for each (the §20.3
"fixed-declaration bar" paragraph directly, since three of these items
cite it) and confirmed byte-for-byte identity with the full diff already in
hand. Since the text each pair of takers read is provably the same text,
none of these fourteen can be a LOSS or ADDITION between editions — the
charter's own quiz-grading rule applies directly: "a taker that misread a
text which decides the question is REPORTER_ERROR." All fourteen grade
REPORTER_ERROR. Two sub-cases:

1. **Formatting-only "divergences"** (quiza-09, quiza-13, quizb-01, 02, 03,
   05, 06, 07, 09, 10, 12, 15): FROM A and FROM B give the *same* substantive
   answer (same number, same verdict, same named row/scope); the
   mechanical detector flagged a difference in comma style, quoting
   granularity, or verbosity, not a difference in content. E.g. quizb-01:
   both say 2,147,483,648 bytes / validity error / reject-layer / layer
   scope. quiza-09: both say entry_count=210000, region=4,200,016 bytes.
   No real divergence exists to grade beyond REPORTER_ERROR (mechanical
   detection artifact).
2. **Genuine taker disagreement on identical text** (quiza-06, quizb-08):
   - quiza-06: taker A says "requires declaring a new layer" (medium
     confidence); taker B says "not a valid appender commit ... requires a
     new layer or rewrite" (high confidence). But §20.3's own text (both
     editions, identical, already quoted under H2's neighbourhood) frames
     "a commit MAY drop the layer (§20.4) and add a new one under its
     name" as an operation available *to an appender* — so "declaring a
     new layer" this way is itself an appender commit, not an alternative
     to one. Taker A's answer is the more defensible reading of the
     (identical) text; taker B's "not a valid appender commit" framing
     does not hold up against §20.3's own wording. Since the text is
     identical in both editions, this is a taker disagreement over
     identical text, not a fidelity difference. REPORTER_ERROR.
   - quizb-08: taker A says slack total "partial"; taker B says
     "complete". I re-read §5.2 directly (lines 715-725 of A, confirmed
     unchanged in B): "a tile's or a document's decode declined leaves the
     walk complete, that claimant being enumerated from its index entry or
     extent slot" vs. "the verifier declined a layer on resource grounds
     ... and so never enumerated its claimants" (→ partial). The question
     specifies the verifier declines "a layer whose **stored-tile
     decode**" it declines — i.e., a tile-decode decline, which the text
     explicitly assigns to the "walk stays complete" branch, not the
     "declined a layer" branch. Taker B's answer ("complete") is the
     textually correct one; taker A's ("partial") conflates a tile-decode
     decline with a whole-layer decline. Both editions state this
     identically. REPORTER_ERROR.

## Coverage check

67 input ids listed in the task. Grouped into 31 groups below; every id
appears in exactly one group; union of member_ids reconstructed and diffed
against the literal input list — see all_input_ids_seen in the structured
result, which is the literal list as given, and the group membership sums
to 67 with no duplicates (5+6+7+6+5+6 [hunks] + 2+2+1+1+1+1+1+1+3+3+2
[shared/EQUIVALENT] + 14×1 [quiz REPORTER_ERROR] = 35+18+14 = 67).
