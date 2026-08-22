# Cross-hunk consistency audit — r20

## 0. Access and disclosure

Read: `spec/tarn.md` only, plus the hunk diffs in the r20audit scratchpad.
`ls` of that directory showed **only three hunk files** exist (hunk-01/02/03),
not ten; each file's own header reads "Hunk N of 3". I did not open
`full.diff`. I did not read docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, spec/registry.json, or any git history.

Context I did not ask for appeared before I began: a project instruction file
pointer and an index of maintainer memory notes, plus a task list. I did not
read the memory files and drew no conclusion from any of it. Contents not
repeated here.

## 1. The three repairs, and the rule each adopts

### Hunk 1 — §7.4, `[R-CNT-18]` (line 1052)
was: "an unknown sub-record type with MU = 1 is reject-layer — never
reject-file — and with MU = 0 is ignore-record."
now: "an unknown sub-record type with MU = 1 is reject-layer, **and a reader
MUST NOT reject the file for it**; with MU = 0 it is ignore-record."

Rule adopted: the outcome-class assignment (reject-layer) is upgraded to a
*normative prohibition on readers*. It is no longer merely "the outcome for
this condition is layer scope"; a reader that rejects the whole file on this
ground is now nonconforming. Quantifier: ranges over *unknown* sub-record
types with MU = 1 — every one of them, conforming file or not, experimental
range or reserved range. Actor: readers only. Generation: not a
generation-sensitive rule.

### Hunk 2 — §20.5, the paragraph under `[R-WRT-07]` (line 3192)
was: "A compactor preserves content but not placement — …"
now: "A compactor **MUST preserve content, and preserves no placement** — …"

Rule adopted: content preservation becomes an obligation rather than a
description. Its object ("content") is defined only by the colon-list forty
words later: every stored tile's bytes verbatim, plus every *retained* record
per §20.4, minus the relocation exceptions. Generation: the input's live
committed state (§20.5 ¶1). Actor: compactor.

### Hunk 3 — §21.6 closing paragraph (line 3566)
was: "The second is an **experimental-range record type carrying MU = 1**
(§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
makes the file conforming all the same, since the prohibition …"
now: "… an **experimental-range top-level record type carrying MU = 1** …
The qualifier is load-bearing — the same type as a layer sub-record is
reject-layer and **never a ground to refuse the file** (`[R-CNT-18]`), so
**only the top-level case** is a file a reader refuses, since …"

Rule adopted: the set of "conforming files a reader nevertheless refuses" is
narrowed — the experimental MU = 1 case counts only at top level; the same
type as a sub-record is excluded from the set entirely, on a stated ground
that is *unqualified as to actor* ("never a ground to refuse the file").

## 2. Grouping by rule, not by section

**Group A — "an unimplemented MU = 1 record: whose fault, and how far does
the refusal reach?"** — hunks 1 and 3, and, because [R-WRT-06] is the
compactor's version of exactly this refusal, the paragraph hunk 2 edits.
All three repairs land on one underlying rule seen from three places:
§7.4 (the outcome), §21.6 (whether the file is at fault), §20.5 (whether an
actor may decline the file). Hunks 1 and 3 *agree with each other*: both
narrow file-level refusal to the top-level case. The defects are all at the
boundary of that group with text no hunk touched.

**Group B — "what a compactor owes on the bytes it carries and regenerates"**
— hunk 2 alone, with §20.4's drop licence as its counterparty.

## 3. Searches run (whitespace-normalised, so the hard wrap cannot hide a hit)

A python pass over the whole file with `\s+`-flexible patterns:

    'MUST accept every conforming file'                    1 hit  L157
    'carrying no record of a type it does not implement'   1 hit  L158
    'MAY reject it upon detecting any violation'           1 hit  L258
    'MUST refuse to compact a file carrying any record'    1 hit  L3187
    'never reaches this step'                              1 hit  L3217
    'never a ground to refuse the file'                    1 hit  L3571
    'MUST NOT reject the file for it'                      1 hit  L1053
    'never reject-file'                                    0 hits  (old text gone)
    'MUST accept any conforming file'                      2 hits L275, L3654
    'unknown sub-record type'                              1 hit  L1052
    'top-level MU = 1 record'                              2 hits L3121, L4340
    'unimplemented top-level MU = 1'                       2 hits L3121, L4339
    'MUST_UNDERSTAND = 1 with a type it does not implement' 1 hit L198
    'MUST preserve content'                                1 hit  L3192
    'preserves no placement'                               1 hit  L3192

Line-oriented greps: `reject-layer|reject-file|ignore-record` (43 hits, all
inspected); `incompat` (6 hits); `sub-record` (all, incl. appendices);
`R-ERR-04` (6 hits).

Every hit was opened and read in place. The restatements of Group A's rule
that exist in the document are:

| where | text | touched by a hunk? |
|---|---|---|
| §2.3 `[R-CNF-03]` L157-164 | reader's must-accept carve-out, **no scope qualifier**, cites §21.6's closing paragraph | **no** |
| §2.3 `[R-CNF-11]` L198 | verifier *cannot establish* ground, **no scope qualifier**, cites §21.6 | **no** |
| §2.4 `[R-CNF-12]` L258 | reader MAY reject a nonconforming file on **any** violation | **no** |
| §7.2 `[R-CNT-15]` L964 | unknown type **at file scope**: MU = 1 → reject-file | no |
| §7.4 `[R-CNT-18]` L1052 | sub-record rule | **hunk 1** |
| §10.3 `[R-EXT-03]` L1425 | "the MU-bit outcome of [R-CNT-15] at file scope and [R-CNT-18] for layer sub-records" | no — and it already drew the distinction hunk 3 now draws |
| §19.1 step 4 L2672 | "the MUST_UNDERSTAND gate for **unknown top-level types**" | no — already qualified |
| §20.4 table, MU = 1 row L3121 | layer scope blocks that layer; file scope bars commits; "Compaction is barred on the same ground ([R-WRT-06])" | no |
| §20.5 `[R-WRT-06]` L3187 | compactor MUST refuse "a file carrying **any record** … MU = 1" | no (hunk 2 is the next paragraph) |
| §20.5 L3217 | "an MU = 1 type the compactor does not implement **never reaches this step**" | no |
| §21.2/§21.3 F35/F36/L24/L25 | reserved-range rows | no |
| §21.6 table row L3540 | experimental type with **MU = 0** | no |
| §21.6 prose L3563-3583 | the two structural cases | **hunk 3** |
| App. H L4339 | updater "rejects outright a file carrying an **unimplemented top-level MU = 1** record" | no — already qualified |

So of the fourteen restatements, hunks 1 and 3 swept two. Four of the
remaining twelve now disagree with them; the other eight already carried the
top-level qualifier or are silent on scope in a way that does not bite.

## 4. Check-by-check

### Hunk 1

1. TENSE/QUANTIFIER. Ranges over *unknown* sub-record types, MU = 1, all of
   them. It IS the normative rule (`[R-CNT-18]`); there is no upstream rule it
   restates. But the set it ranges over includes reserved-range types, which
   L24 registers as a **violation** — so the new MUST NOT now speaks about
   nonconforming files as well as conforming ones. That is where it collides
   with `[R-CNF-12]`. See X-02.
2. CITATIONS. Hunk 1 adds none. The unchanged §7.3 reference in the following
   sentence resolves (§7.3's table scopes 0x0001 file, 0x0002 both). PASS.
3. NORMATIVE PLACEMENT. Line 1053 is body prose inside §7.4, not a ">" block.
   Tagged `[R-CNT-18]` at line 1057. PASS — the repair has force.
4. SAME-PASSAGE CONTRADICTION. Nothing in §7.4 collides. The collision is at
   §2.3 and §2.4 (X-01, X-02).
5. EXHAUSTIVE CLAIMS. "MUST NOT reject the file for it" is an absolute; "it"
   is the record, and a reader that detects, e.g., a cross-layer extent
   overlap involving that sub-record ([R-CNT-13], reject-file) is arguably
   rejecting "for it". Minor; noted in X-02's detail, not raised separately,
   because [R-CNT-13] assigns that check to a verifier.

### Hunk 2

1. TENSE/QUANTIFIER. "every stored tile" = tiles stored in the *input's* live
   committed state (§20.5 ¶1 fixes the generation). Correct tense. "every
   retained record per §20.4" correctly carries the drop licence. But the
   head clause's object — "content" — is separated from its defining list by
   the placement aside; read as a free-standing MUST it forbids the drop
   §20.4 licenses. See X-06.
2. CITATIONS. §5.2 (byte coverage) PASS. `[R-SLB-01]` (per-tile alignment,
   L39/L40) PASS. `[R-SLB-03]` (slab contiguity/first-tile alignment,
   L41/L42) PASS. §20.4 (re-emission and preservation, incl. the compactor
   drop row) PASS.
3. NORMATIVE PLACEMENT. Body prose in §20.5. The paragraph carries no
   identifier of its own; the next tag is `[R-WRT-07]` two paragraphs later,
   and §20.5's tag rhythm (¶1 → [R-WRT-06]; ¶2–¶4 → [R-WRT-07]; the post-example
   ¶ → [R-WRT-09]) makes the new MUST part of `[R-WRT-07]`. I checked §2.2
   ("Normative requirements carry identifiers") and judged this satisfied by
   the trailing tag, so I am **not** raising an unidentified-requirement
   finding. Recorded here because it was close.
4. SAME-PASSAGE CONTRADICTION. §20.5 ¶1 ("less any record §20.4 lets it
   drop"), the dropping paragraph ("Dropping is the one disposal that
   answers"), and §20.4's row ("A compactor MAY drop it whenever it rewrites
   the file") are the counterparties. See X-06.
5. EXHAUSTIVE CLAIMS. "preserves **no** placement" — falsifiable in the
   letter: the front block stays at [0,16), the trailer at F−64
   (`[R-CNT-24]`), no structure may sit between the live directory's end and
   the trailer (`[R-CNT-05]`, F7), and a declared A or S forces placement
   (§16). The same sentence's own aside ("anywhere §5.2 admits and every
   declared layout invariant permits") rescues it, so I fold this into X-06
   rather than raise it alone. "every stored tile's bytes verbatim" — holds.
   "each index entry's crc is unchanged" — holds, and the reject-tile
   paragraph below is consistent with it.

### Hunk 3

1. TENSE/QUANTIFIER. Narrows the second case from "an experimental-range
   record type carrying MU = 1" to the top-level occurrence. The normative
   rule behind it is `[R-CNT-15]`, which says "An unknown record type **at
   file scope**: MU = 1 → reject-file" — and §7.3/`[R-CNT-13]` make a
   non-layer top-level record file-scope, so "top-level" and "file scope"
   coincide here. Quantifier match: PASS. `[R-EXT-03]` already split the two
   scopes the same way, so hunk 3 agrees with it: PASS.
2. CITATIONS.
   - §10.2 — record type experimental range ≥ 0x8000. PASS.
   - §10.3 `[R-EXT-03]` — "for record types, the MU-bit outcome of
     `[R-CNT-15]` at file scope and `[R-CNT-18]` for layer sub-records".
     PASS, and it corroborates the repair.
   - `[R-CNT-15]` — "obliges the reader to reject". PASS for a reader that
     does not implement the type (which §21.6's capability framing supplies).
   - `[R-CNF-02]` — conduct-vs-bytes. PASS.
   - `[R-CNT-18]` — cited for "reject-layer and never a ground to refuse the
     file". PARTIAL FAIL: the rule (as repaired by hunk 1) binds *readers*
     only, and says nothing about a compactor. See X-03.
   - `[R-CNT-07]` — §6.3, reader MUST reject-file on an unimplemented major.
     PASS.
   - §21.1 — "the register enumerates file-conformance violations". PASS.
   - F18 (version_major = 0), F35/F36 (top-level reserved range), L24/L25
     (sub-record reserved range) — all four rows exist and say what the
     paragraph says. PASS individually; but L24/L25 are now the neighbours of
     a case the repair has excluded. See X-04.
3. NORMATIVE PLACEMENT. §21.6 prose, not a ">" block. Note §21.1's precedence
   clause covers "§21.6's **entries**" — the table rows — and the closing
   prose paragraphs are not entries, so this paragraph is not demoted by it
   and its "never a ground to refuse the file" stands as normative prose
   against `[R-WRT-06]`. That is why X-03 is byte-level rather than resolved.
4. SAME-PASSAGE CONTRADICTION. The paragraph's own last sentence still cites
   L24/L25 (X-04). The preceding paragraph ("Two conditions that once sat in
   this table … neither is a reason for a reader to reject anything") is
   unaffected.
5. EXHAUSTIVE CLAIMS. "only the top-level case is a file a reader refuses" —
   I tried to falsify it three ways. (a) An unimplemented **incompat-lane**
   bit: F19 registers any set bit 0–15 as a file-scope violation, so such a
   file is nonconforming and is not a counterexample. PASS. (b) A
   **reserved**-range top-level MU = 1 type: F35, a violation. PASS.
   (c) A **resource** refusal: `[R-CNF-03]` puts that under `[R-ERR-04]` and
   outside §21.6's "structural" pair. PASS. So the claim survives *for
   readers*. It does not survive for actors generally — X-03.
   "Two structural cases" (unchanged) still counts correctly.

## 5. Direction of each disagreement

- X-01: **§2.3 `[R-CNF-03]` should change**, not the repairs. `[R-CNT-18]` is
  the specific rule for sub-records and hunks 1/3 agree with each other and
  with `[R-EXT-03]`, §19.1 step 4 and Appendix H, all of which already say
  *top-level*. Insert "top-level" into the carve-out.
- X-02: **the repair should change.** `[R-CNF-12]`'s blanket MAY is
  load-bearing and older; hunk 1's MUST NOT should be confined to the
  conforming case, or stated as an outcome assignment rather than a reader
  prohibition.
- X-03: **the repair (hunk 3) should change.** `[R-WRT-06]` is the operative
  rule for compactors and is stated in the affirmative with "any record"; the
  §21.6 gloss should say "never a ground for a *reader* to reject the file".
- X-04: **the repair should finish the sweep** — drop L24/L25 from the
  closing sentence, or restore a clause the sub-record case can hang on.
- X-05: **§2.3 `[R-CNF-11]` should change** (add the scope, or point at
  `[R-CNT-18]` for the sub-record half).
- X-06: **the repair should change** — move the colon-list up against the
  MUST, or qualify with "retained".
- X-07: **`[R-CNT-18]` should change** — define "known".
