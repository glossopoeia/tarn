# Refute pass on the REFUTED grade for finding X-01

## What I read / ran
- /private/tmp/.../r24audit/finish/finding-X-01.md
- /private/tmp/.../r24audit/hunk-04.diff
- spec/tarn.md via sed ranges: 170-230 (§2.3 [R-CNF-04]/[R-CNF-05]/[R-CNF-11]),
  2350-2400 (§17.3, [R-COD-09], [R-COD-10]), 2990-3055 (§20.3 step 4),
  3220-3240 (§20.5 [R-WRT-06]), 3319-3400 (§21.1), 3504-3510 (L43/L44/L45),
  3520-3560 (§21.4 T2-T26), 3580-3634 (§21.6), 3630-3720 (§21.7-§21.9).
- greps: "17.3", "R-COD-10", "R-CNF-11|R-CNF-05|R-ERR-01", "21.7", "L45|L43|L44",
  "#### 21."
- whitespace-normalised python regex scan over the whole spec for the five
  disputed fragments (line-wrap safe).
- blockquote check: `awk 'NR>=3634 && NR<=3698 && /^>/'` -> EMPTY. §21.7 carries
  no blockquote lines; the disputed sentence is normative prose closed by
  `[R-ERR-01]`. It is NOT a Note/Rationale.

## The disputed sentence (normalised, verbatim)
"A change reaching the filter, or moving a sample's byte offset within the
decoded image without changing that image's length, has no witness at all —
both filter values are length-preserving (§17.3), and the content rows test
only the bytes §14 constrains."

## Question 1: real as text? YES.

The repaired paragraph enumerates five branches keyed to §20.3 step 4's own
list ("the set of padding positions (§11.3) and the content [R-SER-05] fixes
there, the decoded size, the byte offset of any sample within the decoded tile
image, or the codec and filter that produced the stored bytes"). The sentence
is false under BOTH available readings of that enumeration, and I checked both.

READING (i) — branches partition by *which declaration item changed*.
Then a pure filter-declaration change does not alter the set of padding
positions (geometry-determined, §11.3) nor the fill [R-SER-05] fixes, so
branch 1's antecedent does not obtain and branch 5's does. Yet the reader now
applies (or omits) the inverse byte-shuffle over bytes not produced under it,
so the decoded image is a permutation. §21.4 T4 — "A padding position does not
encode, for each channel it carries, that channel's recorded fill value",
detector *verifier*, governing rule [R-SER-05] — fires on the permuted image.
T2 fires where a real-position interleaved bool byte becomes neither 0x00 nor
0x01; T5 where a packed-plane pad bit flips. So "no witness at all" is false.

READING (ii) — branches partition by *effect*, which is how branch 1 is
actually worded: "A change reaching a byte §14 structurally constrains — a
padding position, a pad bit, or a boolean byte — fires §21.4's content rows."
A filter change does reach such bytes. Branches 1 and 5 then overlap and
return opposite answers. Self-contradiction inside the repaired sentence.

Four independent anchors, three of them normative and one untouched:

(a) §21.7 itself, 18 lines above, untouched by the hunk: "...except where §14
constrains a byte's content — a padding position, a pad bit, or an interleaved
boolean — and a mis-ordered image is then witnessed by T2, T4 or T5, exactly
as a mis-strided filter is". The second half of the disputed sentence
("moving a sample's byte offset within the decoded image without changing that
image's length") is the mis-ordered-image case verbatim. Head-on collision.

(b) §21.4 T26: "Filter 2 applied at a stride other than the mandated one, where
the resulting image breaks §14.5's padding content or [R-SER-08]'s bool bytes
(a wrong stride with no such structural constraint is undetectable, §21.7);
the check that detects it is T2's or T4's". A 1->2 declaration change over
already-stored bytes is observationally the same class as a wrong stride.

(c) [R-COD-10] in §17.3, normative voice: "where the resulting decoded image
breaks a stated content obligation (§14.5's padding, [R-SER-08]'s bool bytes)
a verifier detects it as a validity error at tile scope, and otherwise the
consequence is wrong sample content — undetectable by construction (§21.7)."
That is precisely the hedge the repair withheld from the filter branch.

(d) L45 (spec/tarn.md:3506): "Layer record's filter is a value other than 1 or
2 — 0, reserved 3–0x7FFF, or experimental >= 0x8000", detector *reader*,
detection point *layer access*, [R-COD-09] (R-CNT-23). A step-4 change into a
reserved or experimental filter value is witnessed at layer access, by a
reader, not merely by a verifier. "No witness at all" is false there too.

Note the internal asymmetry the repair itself created: the sibling codec branch
was hedged correctly in this same hunk ("is *sometimes* witnessed ... but
neither is assured"), and the filter branch was absolutised. The identical
hedge is owed for the identical reason. Also, the repair's own stated ground —
"the content rows test only the bytes §14 constrains" — is a reason the change
IS witnessed wherever the permutation reaches such a byte, not a reason it is
not; it supports at most "unwitnessed where no such byte exists".

Steelman of the REFUTED grade, and why it fails: a verifier defaulting to
REFUTED could say the auditor conflated the [R-GEO-06]/[R-SER-01] mis-ordering
clause (writer emits samples wrongly, declarations fixed) with a declaration
change. That distinguishes anchor (a) only. It leaves T26, [R-COD-10] and L45
untouched, and it does not touch the branch-1/branch-5 overlap. A refutation
must establish the repaired sentence is CORRECT; the best available refutation
establishes only that anchor (a) is an analogy rather than an identity. That
is imprecision in the report, not correctness in the text.

## Question 2: byte-level? NO — the not-byte-level grade stands.

Constructions built and tested for a divergence between reading A (sentence as
written: no witness) and reading B (witnessed on T26's terms):

1. Layer declares filter 1, stores planar numeric tiles with padding positions
   holding fill; commit re-declares filter 2. Verifier decodes, un-shuffles,
   padding positions hold permuted bytes -> T4. T4 is a §21.4 row whose
   governing rule is [R-SER-05]; §21.1 makes the rule govern over a row, and
   §21.7 is neither ("The subsections after §21.5 are not part of the register
   and carry no rows"). §21.7 cannot narrow T4. [R-CNF-04] obliges detection.
   Same verdict under A and B. No divergence.
2. Interleaved layer with a bool channel; same change -> real-position bool byte
   becomes >= 0x02 -> T2. Same reasoning. No divergence.
3. Filter re-declared to 3 (reserved) -> L45, detector *reader*, layer access.
   L45's condition is a fact about the layer record's bytes; a reader MUST
   detect it under [R-CNF-04] whatever §21.7 says. No divergence.
4. Charter move: leave the damaged structure out of the new live state. §20.3
   step 4 already forecloses the rescue ("Unstoring that tile in the same
   commit does not rescue it either ... the quantifier is the superseded
   generation's"), and §21.7's NEXT clause — untouched by this hunk — already
   grants the no-witness result for it ("a commit that supersedes every tile it
   would have damaged leaves the live state clean"). Both readings agree there.
   No divergence.
5. Charter move: other actors. Enumerated creator/appender/updater/compactor
   ([R-CNF-05], [R-CNF-06], [R-WRT-06]) and reader/verifier ([R-CNF-04],
   [R-CNF-11]). §20.3 step 4 binds a commit; §21.7 imposes no obligation on any
   of them and grants no permission to any of them. The emittable set is fixed
   by step 4's MUST NOT plus [R-CNF-05], both untouched.
6. Degenerate case: packed planar bool plane, s = 1, filter is the identity
   (§17.3). Step 4 expressly carves this out ("a filter whose mandated stride
   makes it the identity ([R-COD-10]) ... is not what this bars"). Conforming
   under both readings. No divergence.

§21.7's own paragraph 1 states the principle that settles it: "no file-level
witness exists to check, so nothing about the file is left undetermined and the
verdict is unaffected." Under reading A the sentence merely misclassifies which
requirements are undetectable. §21.1 makes that classification load-bearing for
the register's normative completeness — a detectable violation the register
omits "is a defect in this document ... §21.7 the account, by class, of what
fails it" — and §21.8/[R-ERR-02] quantifies the corpus over §21.2–§21.5 rows
only. So the damage is to the document's completeness claim and to the corpus
build list, not to the set of bytes a writer may emit or a reader/verifier must
accept or reject. Real, and in normative text, but not byte-level.

## Missing sentence
None. The document already states the correct rule in three places (§21.7's
earlier clause, T26, [R-COD-10]) and registers L45. The repair contradicts text
the document already has; the fix is a correction of the new sentence, not an
addition.
