# X-01 refute pass — lens: QUANTIFIER

## What I read / ran
- case/case-X-01.md, hunk-02.diff, hunk-10.diff (charter-permitted).
- spec/tarn.md: lines 98-112 ([R-CNF-01]), 130-270 (§2.3 incl. [R-CNF-02], [R-CNF-03],
  [R-CNF-11], [R-CNF-13] and its Note), 400-425 (§4.1 [R-ENC-01]/[R-ENC-02]),
  770-860 (§6.2 trailer table, [R-CNT-05], [R-CNT-06]; §6.3 [R-CNT-07], [R-CNT-24],
  [R-CNT-08]), 2745-2790 (§19.1 steps 1-4), 3350-3425 (§21.1), 3460-3505 (§21.2
  preamble + rows F1-F27), 3665-3700 (§21.6).
- greps (all against spec/tarn.md only):
  - `grep -n "does not implement\|it implements\|implements major\|another major\|other than 1"`
  - `grep -n "future major\|a later major\|majors\b"`
  - `grep -n "R-CNF-01"`
  - whitespace-normalised (`tr '\n' ' ' | tr -s ' '`) `grep -o -E ".{120}reaching requirement.{160}"`
    and `.{80}\*\*reaches\*\*.{240}` — to defeat the hard wrap.

## Grep output that matters
Whitespace-normalised search for "reaching requirement" returns exactly two windows
(plus the defining sentence). Every occurrence is requirement-quantified:

1. §2.3 [R-CNF-02]: "...a file declaring another major is neither conforming nor
   nonconforming under it **save as to the requirements that reach it**
   (`[R-CNF-13]`) ... while the failure of a **reaching requirement** is."
2. §2.3 [R-CNF-13] definition: "**A requirement** of this specification **reaches**
   a file ... when, and only when, the invariant **its condition** violates is one
   `[R-CNT-24]` fixes..."
3. §2.3 [R-CNF-13] operative: "A reader MUST apply **every reaching requirement** to
   a file whatever major it declares..."
4. §2.3 [R-CNF-13] residual: "**Every other requirement** of this specification
   governs a structure this text defines for format major 1 alone..."

There is no occurrence anywhere in normative text of "reaching condition" or of any
per-condition quantifier on the obligation. Three normative sites quantify over
requirements; zero over conditions. The only condition-granular reasoning is in the
Note (blockquote, non-normative by [R-CNF-01] line 105-106) and in §21.2's preamble,
which is a restatement that §21.1 and its own text subordinate to the rule.

## The downgrade's load-bearing claim
Verifier §2, verbatim: "For a file declaring major 7 **read by a reader that
implements major 1**, the version gate does not pass ... so the dir_offset >= 16
obligation is never triggered." Everything downstream — "F8 and F14 therefore reach,
and F9-F13 and F15-F17 do not, as a theorem of the open algorithm" and the whole
byte-level section — rests on that instantiation.

That is a quantifier slip. [R-CNF-13] binds "**A** reader" and "**a** file whatever
major it declares". The verifier universally instantiated "a reader" as a major-1-only
reader. The document expressly contemplates the other actor.

## The actor the downgrader did not enumerate: a reader implementing majors 1 and 7
Textual support that this document contemplates such a reader:
- §2.3 [R-CNF-13] line 239-241: a verifier reports nonconforming "whatever major the
  file declares and **whether or not it implements that major**". The document itself
  entertains a verifier that implements a major other than 1.
- §2.3 [R-CNF-03] line 159-160: "MUST accept every conforming file of **a format
  major version it implements**" — no restriction to major 1.
- §6.3 [R-CNT-07] line 827-829: reject "when version_major is 0 (invalid) or is **a
  major it does not implement**". The negative space is majors it does implement.
- §21.6 line 3675-3678: "version_major naming a major **this reader does not
  implement**: the reader rejects the file ... but **the file can be perfectly
  conforming under that major**."

Nothing in the document exempts such a reader from [R-CNF-13]; [R-CNF-13] exists
precisely to bind readers across majors.

## Construction (the fork)
File P: F = 4096 (F mod 64 = 0). Front signature block bytes [0,16) byte-identical to
the constant. Trailer at [F-64, F):
  off 0..8   trailer magic 8A 4E 52 41 54 0D 0A 1A   (correct)
  off 8..10  version_major = 7
  off 10..12 version_minor = 0
  off 24..32 (major 1's dir_offset) = 8
  off 60..64 CRC-32C over trailer bytes [0,60)       (correct)
Per [R-CNT-24] the redefinable region is trailer offsets 12..60, which contains
dir_offset (24), dir_length (32), committed_file_length (40), file_id (48) and
reserved (56) — confirmed against §6.2's layout table, lines 779-791. So under major 7
the eight bytes at trailer offset 24 need not be an offset at all, and P is stipulated
perfectly conforming under major 7 (§21.6 licenses exactly this stipulation).

Reader R implements majors 1 and 7.

Implementation A — requirement branch (the plain reading of [R-CNF-13]):
  [R-CNT-06] reaches, because the invariant one of its conditions violates (the
  trailer magic at F-64) is one [R-CNT-24] fixes in every major. This existential
  reading of the definite description "its condition" is not a strained one: it is the
  ONLY requirement-level reading on which §21.2's own claim that F8 and F14 reach can
  be true, since the universal reading ("every condition of it") makes [R-CNT-06] not
  reach and kills F8 and F14 too.
  → "A reader MUST apply every reaching requirement to a file whatever major it
    declares" ⇒ apply [R-CNT-06]. Its internal order: magic ✓, trailer CRC ✓, version
    gate ✓ (R implements 7, so [R-CNT-07]'s antecedent fails). "those gates passed,
    MUST validate all of the following ... dir_offset ≥ 16" ⇒ 8 < 16 ⇒ **reject-file**
    on [R-CNT-06]'s own ground. §19.1 step 2 independently drives the same sequence:
    "magic, trailer CRC, version gate, **then the remaining field gates**" — for this
    actor the version gate passes, so step 2 runs to completion.
    Verdict per [R-CNF-13]: *nonconforming*, "whatever major the file declares and
    whether or not it implements that major".

Implementation B — row/condition branch (§21.2's derivation):
  Only F8, F14, F6 and F1's two instances reach. F9 (dir_offset < 16) does not. The
  condition "is not assessed against a file declaring another major, no violation of
  it is established there, and no §21 row restating it records such a file."
  P is conforming under major 7, and [R-CNF-03] obliges R to "accept every conforming
  file of a format major version it implements" ⇒ **MUST accept**.

Same bytes. A MUST reject-file; B MUST accept. Direct MUST-vs-MUST divergence.

## Why §6.2's ordering clause does not save the downgrade
The verifier called "only these touch fields whose positions are fixed across all
majors" plus "those gates passed" "the deciding sentence". It decides only for a
reader whose version gate FAILS. It is a conditional, and for the two-major reader the
antecedent is satisfied, so the clause hands the field gates to the reader rather than
withholding them. §19.1 step 2 does the same. Both of the downgrade's two
"stated twice, normatively" supports flip sign under this instantiation.

## Why the "self-refuting biconditional" argument does not save it either
Verifier §2 closing: "[R-CNT-06] cannot satisfy the 'only when' branch ... and cannot
satisfy the residual characterisation either. A reading on which a requirement is
neither reaching nor 'other' is incoherent; the condition-level reading is the only
one the biconditional admits."
That argument reaches the right *repair* by reductio — but it is reasoning the
document does not contain. It concedes the text as written is incoherent at
requirement granularity and then repairs it by charity. An implementer is entitled to
resolve the same incoherence the other way: read "its condition" existentially, which
makes the biconditional well-formed, makes [R-CNT-06] reaching, and makes F8/F14 come
out as §21.2 says. That resolution costs the implementer nothing and is reached
without ever opening the Note. §21.1 then actively pushes them there: "where a row and
the rule it cites diverge, **the rule governs**" — and §21.2's own repaired preamble
repeats it: "where this restatement and that rule diverge, the rule governs (§21.1)".
The repair in hunk-10 explicitly subordinates its own row list to a rule whose
quantifier does not yield that row list. That is self-undermining, not self-correcting.

## Why "The test is the invariant asserted, not the bytes read" does not fix the
## quantifier
It is normative body text and it does say "a check". But look at what it governs: it
clarifies *the test* (invariant vs bytes read) — the F14 case, where a check consumes
redefinable bytes yet asserts a fixed invariant. It does not requantify the
*obligation*. The obligation two sentences later is still "every reaching
**requirement**", and the residual is still "Every other **requirement**". So the test
is stated per-check while the operative MUST and the residual partition are stated
per-requirement, and "reaching" — the term that joins them — is defined with "A
requirement" as its subject. The downgrader treated a clarification of the test as a
requantification of the obligation. Establishing that the auditor's quotation elided a
sentence is not the same as establishing that the repaired sentence is correct.

## Residual: the [R-CNT-06] Note contradiction survives at requirement granularity
[R-CNF-13]'s residual sentence says of non-reaching requirements: "no §21 row
restating it records such a file." Under the plain requirement quantification
[R-CNT-06] is NOT among "every other requirement" (it reaches), so that exclusion does
not cover F9-F13, F15, F16, F17 — every one of which has Governing rule [R-CNT-06].
§21.2 says those eight do not reach. The rule and the restatement diverge, and §21.1
says the rule wins. The Note's "F15 does not reach although its Governing rule cell
cites [R-CNT-24]" is the only text that resolves it the other way, and it is a
blockquote — [R-CNF-01] line 105-106: "All text in this document is normative except
... any text labeled *Note*, *Example*, or *Rationale*." This is the exact failure
mode the charter names: the repair's granularity lives in a Note while the normative
statement it is fixing stands unamended.

## Discriminating test
"Is the disputed file itself conforming?" P is conforming under major 7 — §21.6 says
so in terms. Under reading B no §21 row records it ([R-CNF-13]'s own residual clause
forbids that), so no register-row violation exists for [R-CNF-05] to bar. The
emittable set does not move (no writer under this text emits a major-7 file), but the
test is disjunctive — "may emit, **or must accept or reject**" — and the accept/reject
side moves: a MUST-reject under A, a MUST-accept under B, on identical bytes. The
downgrade's byte-level section answers only for the major-1-only reader, where I agree
with it: there the version gate stops the walk, the diagnostic is owed either way, and
there is no fork. It never runs the test for the actor the document itself names.

## What I could not break
I looked for text scoping §6.2/§19.1 to major-1-only readers, or exempting a reader
that implements a foreign major from [R-CNF-13]. `grep` on "does not implement",
"it implements", "another major", "other than 1", "future major", "majors" returns
lines 142, 159-161, 199-200, 228, 238, 240, 244, 828, 845, 3469, 3676 and nothing that
narrows the actor. §21.6's two "conforming files a reader nevertheless refuses" is the
closest, and it points the other way.

## Verdict
DOWNGRADE_REFUTED. Real as text (three normative sites quantify over requirements,
none over conditions; the row set §21.2 asserts is not derivable from the rule §21.2
defers to). Byte-level YES on the two-major-reader construction.
