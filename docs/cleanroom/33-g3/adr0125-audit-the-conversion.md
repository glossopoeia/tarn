# Audit transcript — lane "the-conversion"

Charter: hunk-07, hunk-17, hunk-14, hunk-15 (rounding-direction attribute, its
Appendix F citation, F3, L14).

## Disclosure

Read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `sed -n` ranges and `grep -n`, never in full at once)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/hunk-07.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/hunk-17.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/hunk-14.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/hunk-15.diff`

Did NOT read: full.diff, other hunk files, docs/, PLAN.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, the web. Did not list the case
directory (only cat'd the four named files by exact path).

Ran only `grep`/`sed`/`python3` (local, pure computation, no file reads other
than the spec and my own hunk files) and `Bash`. Wrote one scratch computation
inline via heredocs to `/dev/stdin` (no files written outside the mandated
scratch dir); no files were actually written to disk during the exact-integer
DBL_MAX computation — I ran python3 heredocs directly, no intermediate script
files persisted. (No script file was left on disk; if any transient file had
been needed I would have put it under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/scratch/the-conversion/`.)

**Context contamination check.** My system/tool context included a CLAUDE.md
and a MEMORY.md with prior-round file names like "TARN repair prose vs
rules.md", "TARN lineage gate word list", etc. I did not open any of those
memory files (they are not among my two permitted reads), and I did not let
their titles steer my conclusions — I did not, for instance, assume any
particular hunk was clean or dirty because of a memory-file title. This is a
disclosed exposure to material outside the access rule (the memory index
appeared in my context unbidden); I am flagging it per the access rule's
disclosure requirement. I did not act on its contents beyond what is stated
here.

Also: the harness's own boilerplate at the top of this conversation is
generic (git safety, artifact rules, etc.) and is not spec content; ignored
for audit purposes.

## Hunk 07 — §18.2 "Finite numbers only" (lines 2727-2738 in body)

### The rule this repair adopts

Before: "A reader interprets every JSON number as an IEEE 754 binary64 value
and MAY use a wider representation." — silent about *which* binary64 value a
given decimal literal denotes when the literal isn't exactly representable.

After: "A reader interprets every JSON number as the IEEE 754 binary64 value
its decimal text converts to under IEEE 754's default rounding-direction
attribute, roundTiesToEven, and MAY use a wider representation."

This pins the interpretation to a specific, deterministic, byte-level
function of the JSON number's decimal source text: the IEEE-754-correctly-
rounded conversion under roundTiesToEven. It also updates the overflow
clause: "overflows on conversion" → "overflows on **that** conversion",
tying the overflow test explicitly to the newly-named conversion.

### Check 1 — tense/quantifier

Actor: "a reader." Range: "every JSON number" (unchanged quantifier, not
narrowed or widened). The value spoken of ("the IEEE 754 binary64 value ...")
is a function of the bytes of the decimal text alone — not of which reader is
asked, not of what representation that reader chooses to hold it in. That
purity matters for Check on R-CNF-02 below.

### Check 2 — citations

No requirement ID or section number is introduced inside this hunk's own
text. I still verified the surrounding-passage citations that the check
requires me to hold this hunk against:

- **R8** (§21.5, line 3849): "A user-metadata document contains a non-finite
  number — a magnitude whose binary64 interpretation overflows (`1e400`), or
  one of the bare tokens `NaN`, `Infinity` and `-Infinity`..." — **PASS**,
  unaffected by the hunk (not touched by it) and not contradicted by it: R8
  doesn't name the rounding-direction attribute, but under §21.1's rule ("each
  row *restates* its governing rule, and where a row and the rule it cites
  diverge, the rule governs") R8 is a restatement, and the governing rule
  (`[R-MTA-04]`, which covers this whole bulleted list) is what now names
  roundTiesToEven. No divergence: R8's "binary64 interpretation overflows" is
  a strict subset description of the same fact the repaired sentence states,
  just without the added precision. **PASS.**
- **[R-CNF-02]** (§2.3, line 152-177): "File conformance is a pure predicate
  on bytes: it does not depend on any reader, writer, or environment." I
  checked whether "MAY use a wider representation" creates a reader-dependent
  conformance test. It does not: the *readability* test ("unreadable if ...
  binary64 interpretation is not finite") is stated over the deterministic
  conversion result, not over whatever representation an individual reader
  chooses to hold the value in afterward. The "MAY use a wider
  representation" clause governs what a reader does with an *already-defined*
  value, not how the document's readability is decided. No conflict with the
  purity clause. **PASS.**
- **[R-CNF-02]**'s companion sentence at line 2779 ("file conformance — a pure
  predicate on bytes (`[R-CNF-02]`) — is decided by the structural checks that
  precede the document alone") is about the *unassigned-encoding* case, a
  different fork; read for context, not in conflict. **PASS** (not directly
  on point, correctly not cited by the hunk).
- **Writers SHOULD NOT** sentence (same bullet, untouched): "Writers SHOULD
  NOT emit a number binary64 cannot represent exactly; a value needing
  bit-exact representation belongs in a structural field (§13.1), not here."
  Exact representability of a decimal value in binary64 is independent of
  rounding-direction attribute (rounding mode only matters for values that
  are *not* exactly representable, to decide which neighbor they round to).
  No interaction, no contradiction. **PASS.**

### Check 3 — normative label

The whole four-bullet list ("A JSON object, unmarked." / "Finite numbers
only." / "No duplicate keys." / "Well-formed UTF-8 throughout") sits in plain
body prose under `#### 18.2 Encoding`, not inside any blockquote. It carries
the trailing tag `` `[R-MTA-04]` `` right after the list. This is normative
text by the ordinary rule (§1 aside, everything is normative unless labeled
Note/Example/Rationale or is a non-normative appendix) — no ">" marker is even
in play here, so the "check the label not the marker" caution is moot for
this hunk; it plainly lands in force. **PASS.**

### Check 4 — contradiction in the passage

Read the whole `#### 18.2 Encoding` subsection (lines 2620-2790) end to end.
Looked specifically for: a carve-out that collides with the newly-precise
overflow test; a MUST that the new text lets someone violate. Found none.
The Note right before this bullet list ("The 16 MiB figure is a §21.9 minimum
guarantee...") is about decoded-document size / window size, a different
axis entirely (byte length of the decoded JSON text vs. the numeric value of
one JSON number) — no collision. **PASS**, no contradiction found.

### Check 5 — exhaustive claims

Words promising completeness in the repaired text: "every JSON number", "any
of the bare tokens". "Every JSON number" — checked: yes, every JSON number
syntactically possible per RFC 8259 grammar is covered by "the IEEE 754
binary64 value its decimal text converts to," since RFC 8259 numbers are
always finite decimal literals with optional exponent — the conversion
function is total over that grammar (always produces either a finite
binary64 value or infinity on overflow; never undefined). Not falsified.
"Any of the bare tokens NaN, Infinity, -Infinity" — closed, 3-item list,
matches R8's 4-instance split of "bare token" as its own category with 2 sub-
instances (top-level/layer-sub-record) × that same 3-token set implicitly.
Not falsified. **PASS.**

### Check 6 — what's left unconstrained

Structure: a single JSON number token (sign, integer part, fractional part,
exponent). Quantities in play: (a) whether it's finite under binary64
(constrained, now precisely); (b) which exact binary64 bit pattern it becomes
when finite (constrained by "converts to under roundTiesToEven" — that's a
correctly-rounded, hence unique, answer); (c) underflow/subnormal behavior —
not separately addressed, but underflow never produces a non-finite result,
so it's out of scope for *this* rule by construction, not a gap; (d) sign of
zero (-0.0) — not mentioned, but nothing in this bullet claims to constrain
it and no other passage needs it constrained here. I don't find a sibling
quantity of "a JSON number" that this rule was supposed to pin and left open.
**No new gap found** attributable to this hunk.

### Check 7 — analogy

No "exactly as," "the same way," "on the model" language appears in this
hunk's own inserted text. (The surrounding paragraph does use such language
elsewhere — e.g., "the tile rule of `[R-COD-06]` transposed to the quantity a
document does have" — but that is pre-existing text about the frame's
content-size field, untouched by this hunk, and out of my hunk's scope.)
**N/A for this hunk's own text.**

### Check 8 — anaphora from insertion

Forward from the insertion point to the end of the bulleted list: "that
conversion" (added by the hunk) — resolves, before and after, to the single
decimal→binary64 conversion named two clauses earlier in the *same* sentence;
there is no competing "conversion" noun anywhere upstream, so this
back-reference is unambiguous both before and after the edit (before the
edit there was no "that" at all — bare "conversion" — the edit only adds
precision, doesn't relocate an existing pronoun). "the decoded-document
restrictions above" (later, line ~2771, pre-existing, unaffected) still
resolves to this same four-bullet list including the now-amended "Finite
numbers only" bullet — unaffected in identity. **PASS**, no anaphor
resolution changed.

### Byte-level analysis and derived numbers (top of the binary64 range)

Computed with Python using exact integers (not floating hardware, not the
`decimal` module's default 28-digit context — the first attempt using
`decimal.Decimal(2)**-52` silently truncated to 28 significant digits and
gave a **wrong** answer; caught by recomputing with exact integer arithmetic
and getting a different, correct result — recorded as a rejected candidate
below):

- Largest finite binary64 (DBL_MAX) = (2 − 2⁻⁵²) × 2¹⁰²³
  = 2¹⁰²⁴ − 2⁹⁷¹ =
  179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368
  — verified against `struct.unpack('<d', struct.pack('<Q', 0x7FEFFFFFFFFFFFFF))` in the
  same session: **matches**, confirming the integer is the actual DBL_MAX.
- Next power of two: 2¹⁰²⁴ = DBL_MAX + 2⁹⁷¹ (one ULP at this exponent, since
  the ULP of the max normal = 2^(1023−52) = 2⁹⁷¹).
- Midpoint between DBL_MAX and 2¹⁰²⁴ = DBL_MAX + 2⁹⁷⁰ = 2¹⁰²⁴ − 2⁹⁷⁰.
- Decided under roundTiesToEven (verified by converting the *exact* integer
  value at each point to `float` via a 400-digit-precision `decimal.Decimal`,
  i.e. an exact, non-lossy conversion into Python's correctly-rounded
  `float()`):
  - `DBL_MAX` → `1.7976931348623157e+308`, **finite** (readable).
  - `midpoint − 1` → `1.7976931348623157e+308` (rounds down to DBL_MAX),
    **finite** (readable) — this is "a literal between them."
  - `midpoint` exactly → `inf`, **non-finite** (unreadable) — the tie breaks
    to the "even" candidate 2¹⁰²⁴ (mantissa 0, even) over DBL_MAX (mantissa
    all-ones, odd), which is the standard roundTiesToEven overflow
    convention.
  - `midpoint + 1` → `inf`, **non-finite** (unreadable).

So the sentence, under the newly-named roundTiesToEven attribute, cleanly and
correctly decides all three probe points, including the exact tie — and the
tie's resolution is *specific to roundTiesToEven* (a different
rounding-direction attribute, e.g. roundTowardZero, would decide the exact
midpoint the other way). This means naming the attribute is not cosmetic: it
pins a real byte-level boundary that was previously underspecified. I judge
the *repair itself* correct and consequential (a genuine improvement), not a
defect.

R8's Condition cell, untouched by the hunk, still reads "a magnitude whose
binary64 interpretation overflows" — consistent with all four probe results
above (silent on the *mechanism*, but not contradicting it). **PASS**, R8
still says the same thing.

### Verdict for hunk-07

No defect found. All eight checks pass; the repair is precise and the
boundary computation confirms it resolves the byte-level tie case it was
apparently written to pin down.

---

## Hunk 17 — Appendix F, the `[IEEE 754]` entry (lines 4517-4527)

### The rule this repair adopts

Before: `[IEEE 754]` cited only for "binary16, binary32, and binary64
(§12.1)." After: adds "and the conversion from decimal text to binary64
under its default rounding-direction attribute, roundTiesToEven (§18.2)."
— i.e., extends the bibliography entry to also cover §18.2's newly-precise
citation of the standard (hunk-07's addition).

### Check 2 — citations / form match

Compared word for word against §18.2's own phrase (hunk-07's text): "the
IEEE 754 binary64 value its decimal text converts to under IEEE 754's
default rounding-direction attribute, roundTiesToEven." Appendix F's new
clause: "the conversion from decimal text to binary64 under its default
rounding-direction attribute, roundTiesToEven (§18.2)." Same substance
("decimal text," "binary64," "default rounding-direction attribute,"
"roundTiesToEven" all reproduced), same section pointer. **Citation
verified — the entry correctly restates what §18.2 says, PASS** — with one
caveat raised under Check 8 below.

Compared against the form of Appendix F's other entries (all read, lines
4519-4527): each is `**[ID]** description — usage (§section)`, several with
multiple usage phrases joined by "and" sharing one trailing parenthetical
(e.g. `[RFC 8878]`: "codec 3 and metadata encoding 2 (§17.2, §18.2)"). The
`[IEEE 754]` entry instead gives each of its two usages its own trailing
parenthetical mid-sentence. This is a style variant already visible in the
document (not every entry shares one parenthetical), not itself a defect.

### Check 6 — what else does this entry leave uncited (§12.1 bfloat16, §14 bit
patterns, §13 fill)

- **§12.1's bfloat16 paragraph** (line ~1797-1802): "A bfloat16 bit pattern b
  denotes exactly the value that the IEEE 754 binary32 bit pattern b × 2¹⁶ ...
  denotes." This *is* an IEEE-754 reliance (binary32 bit-pattern semantics),
  but it is already covered by the *original, untouched* half of the entry:
  "binary16, binary32, and binary64 (§12.1)" — §12.1 is already cited. **No
  gap attributable to this hunk.**
- **§14's bit patterns / §13's fill**: grepped `IEEE 754` across the whole
  document (see sweep below) — the only two locations are §12.1 and §18.2.
  §13.2 states "For the twelve numeric types, every bit pattern of the
  element size is a valid fill (`[R-TYP-05]`), NaN payloads and −0.0
  included" — this *invokes* IEEE-754 bit-pattern concepts (NaN, signed
  zero) without naming or citing IEEE 754 at all, and Appendix F's entry does
  not list §13.2 in its parenthetical set either before or after this hunk.
  This is a real citation gap in Appendix F **but it predates this round's
  repair** — the old entry (`IEEE 754-2019 — binary16, binary32, and binary64
  (§12.1)`) also omitted §13.2, and this hunk only *adds* a §18.2 clause; it
  neither creates nor worsens the §13.2 gap. I record this as a rejected
  candidate (pre-existing, not this repair's doing) rather than a finding
  against hunk-17.

### Check 3 — normative label (the important one for this hunk)

Grepped all appendix headings (`^### Appendix`): A, B, C, D, E, G, H are each
explicitly suffixed "(non-normative)"; **Appendix F — Normative references is
not** so suffixed. Per `[R-CNF-01]` ("all text in this document is normative
except: §1; any text labeled Note/Example/Rationale; and appendices
identified as non-normative"), Appendix F **is normative text** by its own
absence of the non-normative label — this is the ">"-free, label-driven
determination the charter and access notes specifically warn me to make
explicitly rather than assume. This matters for the finding below: the
ambiguity I found sits in force, not in an aside.

### Check 8 — anaphora introduced by the insertion (FINDING)

The repaired sentence: "**[IEEE 754]** IEEE 754-2019 — binary16, binary32,
and binary64 (§12.1), and the conversion from decimal text to binary64 under
**its** default rounding-direction attribute, roundTiesToEven (§18.2)."

Reading forward with nearest-antecedent resolution (the method Check 8
requires): the pronoun "its" is preceded immediately by "binary64" (in "the
conversion from decimal text to **binary64** under its default
rounding-direction attribute") — a numeric format, three words away — versus
the intended referent "IEEE 754" (i.e., "IEEE 754-2019"), which is the
subject of the whole bullet but sits roughly 20 words earlier, before an
intervening clause with its own parenthetical citation "(§12.1)." A
rounding-direction attribute is a property the IEEE 754 standard defines for
its arithmetic/conversion operations — not a property "binary64" itself
possesses independent of the standard — so the nearest-antecedent reading
("binary64's own default rounding-direction attribute") is not just
inelegant, it does not actually parse as a coherent claim. §18.2's own
sentence, by contrast, avoids this entirely by writing out "under **IEEE
754's** default rounding-direction attribute" in full, using no pronoun.

This ambiguity is wholly new: the pre-repair entry ended at "(§12.1)." with
no pronoun anywhere in the bullet. The repair's added clause is the only
source of "its" in this entry, so this is squarely introduced by hunk-17,
in the shape Check 8 warns about (a pronoun landing on a closer, wrong
antecedent after an insertion) — except here the insertion supplies both the
new antecedent-candidate ("binary64") *and* the new pronoun *and* the
intended-but-distant true antecedent, all inside one bullet, rather than the
insertion sitting between two pre-existing sentences.

**Byte-level:** No. Appendix F is a bibliography of provenance citations; it
does not itself state a rule a reader/writer/verifier checks bytes against.
The actual behavioral rule lives in §18.2, whose wording is unambiguous
(spells out "IEEE 754's," no pronoun). Resolving the Appendix F ambiguity
changes no accept/reject verdict and no emittable byte sequence — it is a
prose defect in normative text (normative because Appendix F carries no
non-normative label), not a fork in conformance. I state this plainly: two
readers of this bullet could disagree about what "its" grammatically points
to, but neither disagreement changes what any implementation does with
actual file bytes.

### Verdict for hunk-17

One finding: **C-01**, ANAPHOR / NEW_AMBIGUITY, not byte-level, in normative
text (Appendix F is not labeled non-normative).

---

## Hunk 14 — F3 (§21.2 File-scope violations, line 3685)

### The rule this repair adopts

Before: "A sum of a u64 offset and length taken from the file exceeds
2^63 - 1, so the sum wraps." After: "...exceeds 2^63 - 1 although each field
alone is in domain."

### Check 7 — analogy (the load-bearing check here)

The charter directs me to hold this word for word against L2 and T12.
Grepped both:

- **L2** (§21.3, line 3733): "A declaration-derived sum or product of a
  layer exceeds 2^63 - 1 **although every contributing field is in domain**"
  — governing rule `[R-ENC-04]`, same as F3.
- **T12** (§21.5, line 3803): "A non-sentinel tile-index entry's offset +
  length exceeds 2⁶³ − 1 **although each field alone is in domain**" —
  governing rule `[R-IDX-03]` (R-ENC-04).

F3's new text — "exceeds 2^63 - 1 although each field alone is in domain" —
is **word-for-word identical** to T12's qualifying clause ("although each
field alone is in domain"), and uses the same governing verb ("exceeds ...
although ... is in domain") as L2, whose clause differs only in "every
contributing field" vs. "each field" — appropriate given L2's condition has
many multi-term sums/products (up to 8+ contributing fields) while F3 and
T12 each have exactly two addends. **The analogy holds for both siblings,
word for word, with no quantifier mismatch** — unlike the Check-7 warning
case (contains/addressed), "each field alone is in domain" ranges over
exactly the same thing in F3 as in T12: the two u64 fields being summed. This
is the check that historically catches the worst defects in this project,
and it comes back clean here.

### Check 2 — citations

`[R-ENC-04]`'s own text (line 479-478): "MUST treat any quantity this
specification **designates** a declaration-derived sum or product of
integers obtained from a file (offsets plus lengths, ...) whose mathematical
value would exceed 2⁶³ − 1 as a validity error at the owning scope." This
condition is stated purely in terms of the sum's mathematical value — it
does not itself carve out "although each field alone is in domain." Under
§21.1's "the rule governs" clause, this is fine: F3 (and L2/T12) are
restatements narrowed by the specialization principle (below), and R-ENC-04
is the actual governing text; the row need not repeat every nuance R-ENC-04
implies via specialization. **Verified, PASS** (rule read, matches, no
divergence that would misstate R-ENC-04).

### Check 4/6 — specialization and completeness (why the qualifier is not a
new restriction, just an explicit statement of one)

§21.1 (lines 3585-3620): "Some rows are strict specializations of others:
where every file exhibiting one row's condition ... necessarily exhibits
another's, the file is recorded against the narrower row ... F1's
front-block instance of F6 ... stand in that relation; the property decides
any pair and **this list is not offered as closed**."

Worked this out concretely: F2's instances include `dir_offset` and
`dir_length` individually; F3's (unchanged) instances are `dir_offset +
dir_length` and the extent-slot pair. If `dir_offset` alone already exceeds
2⁶³ − 1 (an F2 violation), then `dir_offset + dir_length` trivially also
exceeds 2⁶³ − 1 (since `dir_length` is unsigned, hence ≥ 0) — so **every**
file exhibiting F2 on one of F3's two summed fields **necessarily** also
exhibits the pre-repair F3 condition ("sum exceeds 2⁶³ − 1"), while the
converse is false (e.g. `dir_offset = dir_length = 2⁶²`, individually
in-domain, sum exceeds 2⁶³ − 1 without ever tripping F2). That is exactly
the "strict specialization" shape §21.1 describes, so per §21.1's own rule
such files were already classified against the narrower row (F2), even
under the pre-repair F3 wording — the specialization mechanism, not the
row's prose, does the actual classification work. The added qualifier
therefore makes explicit (and matches its two siblings' existing wording)
something the register's specialization rule already enforced; it does not
itself move which files land in F2 vs. F3.

**Byte-level: No.** The set of byte sequences that trigger F2 vs. F3 as
*outcomes* was already fixed by §21.1's specialization clause before this
repair (both rows have the same outcome — reject-file / "open" — and the
same ultimate governing citations feeding into R-CNF-05 nonconformance, so
even mis-filing under the wrong row name would not change accept/reject).
This is an editorial harmonization with L2/T12, not a behavior change.

### Instances / register-count check

F3's Instances cell is untouched by the diff: "dir_offset + dir_length;
non-layer top-level record extent_offset + extent_length" (2 instances,
unchanged before/after). The wording change affects only the Condition
cell's prose, not the enumerated alternatives, so §21.8's totals ("120
conditions over 277 instances") are unaffected by this hunk. §21.2's own
count line ("35 conditions") is unaffected — no row added or removed.

### Verdict for hunk-14

No defect found. The repair's wording is a verified, word-for-word match to
its two siblings (L2, T12), correctly restates a pre-existing specialization
relationship with F2, and changes no byte-level outcome.

---

## Hunk 15 — L14 (§21.3 Layer-scope violations, line 3745)

### The rule this repair adopts

Before: "A sub-record does not fit in the layer record's inline payload: its
24-byte header is truncated at the payload end, or its inline_length runs
past that end." After: adds a third alternative, "or bytes remain after the
last complete sub-record."

### Check 2 — citations

`[R-CNT-18]` (line 1136-1143): "The inline payload MUST parse exactly:
fields are packed in table order with no alignment or padding between them;
... and **the remaining bytes MUST parse as zero or more complete
sub-records under §7.2's framing with no residue**; any **overrun**,
**truncation**, or **residue** is a validity error at layer scope." This is
the governing text, and it names exactly three terms: overrun, truncation,
residue. Pre-repair L14 named only two of the three (truncation via "header
is truncated," overrun via "inline_length runs past that end"); the third
named term, residue, had **no** corresponding clause in L14's Condition text
even though it is one of R-CNT-18's three explicitly-named failure shapes.
**Citation check: the pre-repair text under-covered its own governing rule;
the repair completes it. PASS for the post-repair text.**

### Check 6/1 — the Instances-cell mismatch this repair actually fixes

L14's Instances cell — **unchanged by this diff** — already read "sub-record
header; sub-record inline_length; **trailing residue**" (3 items) even
*before* the repair, while the pre-repair Condition text stated only 2
alternatives. Per §21.1's own instance-counting rule ("one of several
alternatives the condition text states ... [is] an instance"), a
3-instance cell demands 3 stated alternatives in the Condition text — the
pre-repair row was internally inconsistent (an instance, "trailing residue,"
with no textual alternative producing it). The repair's added clause,
"bytes remain after the last complete sub-record," is the natural textual
counterpart to the pre-existing "trailing residue" instance. **This
resolves a real internal defect** (Condition/Instances mismatch) rather than
introducing scope — an UNDERSHOOT being corrected, not an overshoot.

Recount: L14 instances = 3 after the repair, and = 3 (nominally) before it
per the Instances cell — **no change to the instance count**, hence no
change to §21.8's "277" total attributable to this hunk. §21.3's own count
line ("49 conditions") is unaffected (no row added/removed).

### Check 7 — analogy to F29 (the file-scope sibling)

F29 (§21.2, line 3710): "A top-level record's 24-byte header or its inline
payload extends past the end of the directory's record sequence (dir_offset
+ dir_length - 4), **or bytes remain after the last complete record**" —
Instances: "record header; inline_length; trailing residue" — the exact same
3-way split, same governing rule family (`[R-CNT-12]` + `R-ENC-07`), and
**word-for-word identical trailing clause** ("bytes remain after the last
complete record" vs. L14's "... sub-record"). This is strong, confirming
precedent that residue is meant to be its own named instance alongside
truncation/overrun, exactly as R-CNT-18 (and its file-scope analogue) name
it. **Analogy holds.**

However, comparing the *framing*, not just the trailing clause: F29's three
alternatives are coordinated directly ("A record's header **or** payload
extends past X, **or** bytes remain...") with no subsuming headline verb.
L14 instead frames all three under a single opening clause, "**A sub-record
does not fit** in the layer record's inline payload: [alt1], [alt2], or
[alt3]." The first two alternatives genuinely describe *a sub-record*
failing to fit (a truncated header, an overrunning inline_length). The third
— "bytes remain after the last complete sub-record" — describes leftover
bytes that were never even the start of an attempted sub-record (e.g., 3
stray bytes, too few even to be examined as a header); grammatically this
is not naturally described as "**a sub-record** does not fit," it's a
residue condition with no sub-record as its grammatical subject at all.
F29 avoids this problem because it never uses a "does not fit"-style
subsuming headline to begin with — this framing mismatch is specific to how
the repair grafted its new clause onto L14's older two-clause "does not
fit:" sentence, not to the same clause's use in F29.

I checked whether this actually creates a *coverage* gap (a byte pattern
neither the old L14 nor the new clause plainly covers) and could not find
one: any leftover residue, if you attempt to read it as the next sub-record,
is necessarily either too short to hold a 24-byte header (already alternative
1) or long enough to have a header but overrun on `inline_length`
(alternative 2) — there is no third mathematically distinct case; "bytes
remain after the last complete sub-record" is a restatement of "alternative
1 or alternative 2 happened, and here is the resulting fact from the
reader's point of view" rather than a logically independent trigger. This
matches R-CNT-18's own three named terms (overrun/truncation/residue),
which likewise treats "residue" as the resulting-fact vocabulary word rather
than a fourth, disjoint mechanism — so the document's own convention
already treats it this way, and F29 (untouched, pre-existing, using the same
three-way split) confirms this is the house style, not a slip specific to
this repair's substance.

**Byte-level:** No. The set of files L14 fires on is unchanged (any residue
after the layer record's parseable sub-record sequence was always going to
be either a truncated header or an overrunning inline_length, both already
reject-layer under the pre-repair text); the new clause supplies vocabulary
matching the Instances cell and R-CNT-18, not new coverage.

**Verdict on the framing:** I record this as a minor, non-byte-level finding
(**C-02**, NEW_AMBIGUITY) — the "does not fit" headline no longer accurately
subsumes all three of its own listed alternatives — but flag it as low
severity: it does not change what an implementation accepts or rejects, and
the underlying vocabulary is precedented elsewhere in the document (F29).

### Verdict for hunk-15

One low-severity, non-byte-level finding (C-02); the substantive fix (adding
the missing "residue" alternative to match the pre-existing Instances cell
and R-CNT-18) is correct and needed.

---

## Sweeps run (verbatim, with hit counts and controls)

```
grep -n "R8" spec/tarn.md                                    -> 1 (line 3849)  [control: nonzero, fine]
grep -n "R-CNF-02" spec/tarn.md                               -> 6 hits (152-block via context, 1058, 1275, 1280, 2691, 2779, 3871, 3897 — I opened 152 and 2779)
grep -n "IEEE 754" spec/tarn.md                               -> 4 hits (1782,1784,1785 unrelated table cells + 1787,1801,2730,2731,4521 header/entry) — precisely hunk-07 + hunk-17 + §12.1
grep -n "rounding-direction\|roundTiesToEven" spec/tarn.md    -> 2 exact-phrase hits (2731, 4523) for "rounding-direction"; "roundTiesToEven" control -> 2 hits (2731 area, 4523 area)
grep -n "non-finite\|is finite\|not finite\|finiteness" spec/tarn.md -> 2 hits (2734, 3849)
grep -n "dir_offset + dir_length\|extent_offset + extent_length" spec/tarn.md -> 8 hits, all read and reconciled against F3/F10/F29/F32/L2/L17
grep -n "R-ENC-04" spec/tarn.md                               -> 11 hits; opened the definition (479) and both register hits relevant to my hunks (3685, 3733, 3803)
grep -n "R-CNT-18\]" spec/tarn.md                             -> 9 hits; opened the definition (1136-1143) and L13/L14/L24/L26 register rows
grep -n "^### Appendix" spec/tarn.md                          -> 8 hits; used to determine Appendix F carries no "(non-normative)" suffix unlike A/B/C/D/E/G/H
grep -n "277" spec/tarn.md                                    -> 1 hit (3971, the §21.8 total)
Control for hard-wrap risk: grep -n "binary64 value its decimal text converts" -> 1 (line not wrapped here);
  cross-checked with whitespace-normalized `tr '\n' ' ' | tr -s ' ' | grep -o` for the full sentence -> 1 (matches, confirms grep -n was not silently failing on a wrap)
Control fragment "roundTiesToEven" (known-present, short, unwrappable) -> 2 hits, matching the 2 real occurrences -- proves grep is not systematically missing hits in this file for these hunks.
```

## Derived numbers

- DBL_MAX as exact integer = 2¹⁰²⁴ − 2⁹⁷¹, verified byte-identical to
  `struct.pack('<Q', 0x7FEFFFFFFFFFFFFF)` unpacked as `<d`.
- ULP at the max exponent = 2^(1023−52) = 2⁹⁷¹; half-ULP = 2⁹⁷⁰.
- Midpoint to next power of two = DBL_MAX + 2⁹⁷⁰ = 2¹⁰²⁴ − 2⁹⁷⁰.
- Verified (exact-integer → 400-digit-precision Decimal → Python `float()`,
  which is correctly-rounded/roundTiesToEven on the platform used) that:
  DBL_MAX → finite; midpoint−1 → finite (rounds to DBL_MAX); midpoint exactly
  → `inf`; midpoint+1 → `inf`. This matches §18.2's overflow rule exactly and
  demonstrates the repair pins a real tie-breaking boundary.
- L14 instance count: 3 before and after (Instances cell untouched); F3
  instance count: 2 before and after (Instances cell untouched). Neither
  affects §21.8's "120 conditions over 277 instances" total, and I did not
  recompute the full 277 from scratch (out of scope — no row was added or
  removed by any of my four hunks, which is the only way that total could
  move).

## Rejected candidates

1. **Hunk-07: "MAY use a wider representation" undermining the finiteness
   test.** Suspected a reader could hold a value in e.g. binary128 and thus
   treat an overflowing-in-binary64 number as finite. Closed by re-reading
   the sentence: the readability/finiteness test is stated over "the
   binary64 value ... converts to," a fixed byte-level fact independent of
   what a reader subsequently stores it as; "wider representation" only
   permits richer storage of that already-fixed value, and R-CNF-02's
   purity clause forbids the test itself from turning on reader choice.
   Confirmed not a defect.
2. **Hunk-17: §13.2's uncited NaN/−0.0 reliance on IEEE-754 bit-pattern
   semantics.** Real gap in Appendix F, but present in the *original*
   pre-repair entry too (which also omitted §13.2) — not created or
   worsened by this hunk. Rejected as out-of-scope for this repair
   specifically, recorded for completeness.
3. **Hunk-14: F3/F2 overlap as a completeness violation.** Initially looked
   like F2 and old-F3 conditions overlapped without being declared a
   specialization pair in §21.1's example list. Closed: §21.1 explicitly
   says its example list "is not offered as closed," and the specialization
   rule (not the row's own prose) already governs which row a given file is
   recorded against — so the pre-repair wording, while less explicit, was
   not itself wrong; the repair is a clarity improvement matching L2/T12,
   not a fix to a real coverage hole.
4. **Hunk-15: apparent 4th failure mode ("too few bytes to even attempt a
   header, before any complete sub-record exists").** Checked whether
   "the last complete sub-record" phrase presupposes at least one complete
   sub-record exists, potentially leaving the zero-sub-records-plus-residue
   case uncovered. Closed: that case is still caught by alternative 1
   ("header is truncated at the payload end") regardless of how many
   complete sub-records preceded it, since alternative 1 doesn't reference
   "the last complete sub-record" at all. Not a gap.
5. **Decimal-module precision trap.** My first attempt to compute the exact
   midpoint using `decimal.Decimal(2)**-52` silently rounded to the default
   28-significant-digit context and gave a wrong "midpoint rounds down"
   answer. Caught by redoing the computation with exact Python integers
   (arbitrary precision) and 400-digit Decimal context, which gave the
   opposite, correct answer (verified self-consistent: midpoint−1 finite,
   midpoint itself infinite). Recorded per the harness's own warning about
   broken-normalization traps in this project.

## Confidence / where little was found

Hunks 07 and 14 returned no defects. For both, I did the full derivation
(exact DBL_MAX/tie-point arithmetic for 07; word-for-word triple comparison
against L2 and T12, plus working out the specialization argument by hand,
for 14) rather than reading the prose and pattern-matching for smell. Had
either hunk left a boundary case undecided or misquoted its sibling row, the
arithmetic or the word-for-word comparison would have surfaced it — both
came back clean under direct computation, not under a plausibility read.
