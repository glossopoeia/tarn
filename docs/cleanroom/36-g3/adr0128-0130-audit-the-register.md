# Audit transcript — lane "the-register" — hunks 03, 04, 34, 35, 36, 37, 38

## 0. Disclosure of context contamination

Before any file access, my session context already contained: a CLAUDE.md
pointer (`See AGENTS.md`), a user MEMORY.md file with ~17 bullet points
about "TARN" topics (harness spec path, lineage gate word list, repair
prose vs rules, harness vs charter, subagents on Opus, refute phase,
nested em-dash, permissions not carve-outs, task output wrapper path,
closed-list exceptions, walk stall/retry, lowercase keywords, ADR status
gates, scratchpad reboot, etc.), a git status/log block showing five
recent commit subjects (ADR-0130, ADR-0128, ADR-0129, Q-A8, etc.), and
later in the session an MCP-server instructions block (Claude Docs,
claude-in-chrome) and an "Auto Mode Active" harness block. None of this
was requested by me, none of it is the specification or evidence about
the specification, and the charter explicitly told me to disregard it and
just disclose that it appeared. I am disclosing it here and have not used
any of its content (commit subjects, ADR numbers, "lineage gate",
"walk stall", etc.) to steer any finding below. Every claim below is
sourced only from spec/tarn.md and my seven hunk files.

## 1. What I read and ran

- Read (in full or by targeted offset/limit) `spec/tarn.md` at: lines
  440-670 (§4.2-4.7 and the Note), 590-670 (§4.7/§5.1 boundary), 697-750
  (§5.2 byte coverage and slack), 1000-1150 (§7.2/§7.3/§7.4), 1080-1150
  (§7.4 layer-record table), 1855-1915 (§12.3, §13.1 fill field), 2205-
  2225 (§15.2 sentinel), 2935-2965 (open algorithm step 4), 3701-3800
  (§21.1 in full), 3800-3920 (§21.2, §21.3 register tables), 3948-4025
  (§21.5, §21.6), 4165-4210 (§21.9 hard limits incl. user-metadata key),
  4235-4265 (§22.3), and small targeted reads around each grep hit.
- Read all seven hunk files verbatim (hunk-03..hunk-38) at the paths
  named in my charter.
- Ran the greps listed in `sweeps_run` below.
- Wrote nothing except this transcript, under my scratch directory.

## 2. Hunk-by-hunk analysis

### Hunk 03 — §4.7 opening

**Diff.**
```
- classified by what its
- *value* determines, each class being what the one before it is not.
- A field is **structural** if its value determines anything a
+ classified by what its
+ *value* determines. A field is **structural** if its value determines anything a
```

**Rule the repair adopts.** Removes the clause "each class being what the
one before it is not" from the sentence that opens the field-taxonomy
classification, leaving: "Every field ... is classified by what its
*value* determines. A field is **structural** if ... It is **descriptive**
if it determines none of those ...".

**Check 1 (tense/quantifier).** No tense change; quantifier is "every
field this specification defines," unchanged before/after.

**Check 2 (citations).** No requirement IDs touched by this hunk.

**Check 3 (label).** Lines 595-608 are plain paragraph text (no `>` at
line start) — normative, not inside a Note/Example/Rationale block.
Confirmed by reading lines 590-628 verbatim.

**Check 4 (contradiction).** The removed clause asserted mutual exclusion
and an implicit ordering between the two classes. I checked whether
anything downstream still needs that clause to hold. The retained text
defines the two classes as complements by construction: structural =
"determines anything [of 4 named things]"; descriptive = "determines
none of those" (an explicit backward reference to the same 4-item test).
"None of those" is logically the negation of "anything," so mutual
exclusion and exhaustiveness (every field is one or the other) survive
the deletion without needing the removed sentence — they are restated,
not lost. I looked for a third class anywhere in the document
(`grep -n "presentation"` — only the §4.7 heading itself and unrelated
type-table hits, no third class name). I conclude the deleted clause was
redundant with the "if X / if none of those" structure that follows it,
and no defect survives its removal.

**Check 5 (exhaustive claims).** "Every field this specification
defines" — checked against §4.7's own body: "In format major 1
`version_minor` is the only descriptive field, and every other field
this specification defines is structural. [R-ENC-16]" This is itself a
normative closed claim (checked under hunk 04 below, since hunk 04's
repair depends on it for the "name" field).

**Check 6 (unconstrained siblings).** Structure governed: the
structural/descriptive partition. Only two classes exist in this
document (confirmed by the "presentation" grep above and by re-reading
the whole of §4.7); nothing is left an unconstrained third state.

**Check 7 (analogy).** None present in this hunk.

**Check 8 (anaphor).** This hunk is a deletion plus a punctuation/clause
merge, not an insertion of new material between two existing sentences,
so the check-8 shape (something inserted, changing what a later "it"/
"that" resolves to) does not apply. I still read forward to the end of
§4.7 (through the Note) for any back-reference to "the one before it"
(the deleted clause's own referent) — none exists; nothing downstream
depended on that phrase.

**Byte-level test.** Not byte-level: the deleted clause was a derived
restatement of the immediately following definitions, not an independent
source of obligation, so no conforming implementation's accept/reject or
emit behavior changes.

**Verdict: no defect found.**

### Hunk 04 — §4.7's Note, name field taxonomy

**Diff.**
```
- table. A variable-length field's value
- includes its length prefix, so a name is structural: it determines
- where the field after it begins. Every non-obvious encoding is followed by a worked numeric
+ table. A name is structural: a duplicate is a validity error at file
+ or layer scope (`[R-ENC-15]`, F4, L9), and its length prefix is §7.4's
+ framing, not its value. Every non-obvious encoding is followed by a worked numeric
```

**Rule the repair adopts.** Replaces the old justification for "a name
is structural" (its value, defined to include the length prefix,
determines where the next field begins) with a new one: a name is
structural because a duplicate name is a validity error (an acceptance
consequence), and separately states that the length prefix is §7.4's
*framing*, explicitly *not* part of the name's *value*.

**Check 3 (label) — required by charter for this hunk.** I read lines
595-628 verbatim. The block starting at line 610, `> **Note.** Layout
tables for fixed-layout structures give, per field: ...`, runs
unbroken (every line prefixed `> `) through line 626, `> Appendix B.`
There is no second block-opening label anywhere in that span. Hunk 04's
edited text (lines 621-623) sits inside this single Note-labeled block.
**Under [R-CNF-01], this whole block — including the repaired sentence
— is non-normative.** This is true both before and after the repair
(the old sentence occupied the same block), so the repair did not move
normative text into a Note or vice versa; it edited already-non-normative
prose. I then checked whether the *substance* of the repaired sentence
is independently stated, with force, somewhere else:
  - "a duplicate is a validity error at file or layer scope" — yes,
    verbatim in force at lines 582-586 (plain prose, not a blockquote):
    "Writers MUST NOT emit duplicates; a reader MUST treat a duplicate
    name as a validity error at the owning scope — a duplicate layer
    name is a file-scope error (reject-file); a duplicate dimension or
    channel name is a layer-scope error (reject-layer). `[R-ENC-15]`"
  - "a name is structural" (the classification itself, independent of
    the Note's rationale) — yes, at lines 606-608 (plain prose): "In
    format major 1 `version_minor` is the only descriptive field, and
    every other field this specification defines is structural.
    `[R-ENC-16]`" Since "name" is not `version_minor`, R-ENC-16 alone
    already makes it structural, with no dependency on the Note's
    reasoning.
  - "its length prefix is §7.4's framing, not its value" — the
    *operational* consequence of this (that a name's length prefix must
    be located to find the field's end, and this happens at *open* for
    the layer name specifically) is stated in normative prose at the
    open algorithm, step 4 (lines 2945-2953): "each layer record's name,
    parsed and checked per §4.6" and register row L23 (§21.3): "open
    (the name field, §19.1 step 4); layer access (every other field and
    entry)."
  So the Note's claims are non-normative *as stated here*, but every
  substantive part of them is independently backed by force-carrying
  text elsewhere. This is the "repair edited a labeled block" case the
  charter warns about, but here it does **not** fail to land, because
  nothing depends on this specific sentence for force. I am reporting it
  anyway per the charter's instruction to report the label test result
  for this hunk explicitly, and because it is exactly the shape of
  finding the charter asks me to be alert to, even though I conclude it
  is not a live defect.

**Check 2 (citations).**
  - `[R-ENC-15]` — opened at lines 578-587. Confirms: duplicate layer
    name → file-scope error; duplicate dimension/channel name →
    layer-scope error. Matches "a validity error at file or layer
    scope" exactly. PASS.
  - F4 — opened at line 3815: "Two layer records in the live directory
    carry byte-identical name fields ... | reader | open |
    `[R-ENC-15]` (R-ENC-13)". Detector "open", outcome class of §21.2
    is "reject-file" (line 3802) — i.e. file scope. Matches. PASS.
  - L9 — opened at line 3869: "Two dimension entries, or two channel
    entries, of one layer carry byte-identical name fields | ... |
    layer access | `[R-ENC-15]` (R-CNT-23)". §21.3's outcome (line
    3856) is "reject-layer" — layer scope. Matches. PASS.
  - "§7.4's framing" for the length prefix — opened §7.4's table (lines
    1109-1132). The `name` field of the layer record is `u8 len +
    bytes` (line 1117); the dimension-entry and channel-entry name
    sub-fields are each `name (u8 len + bytes)` (lines 1127-1128). All
    three of the document's "name" fields (layer, dimension, channel —
    confirmed as the closed set via `grep -n "layer name\|dimension
    name\|channel name"`, see sweeps below) have their length-prefix
    framing defined in this one table. PASS, with one caveat noted
    under check 5.

**Check 5 (exhaustive claims) — is "its length prefix is §7.4's framing"
true of every *name* field, and does the sentence's "A name" risk
over-including a field the document calls something else?** I checked
whether "a name" could be read to include the **user-metadata key**,
which the document explicitly runs §4.6's *name rules* over (line 4184:
"a user-metadata key at most 255 bytes by §18.2's folding of §4.6's name
rules onto keys") but which **carries no length prefix at all** (line
4184-4185: "which carry no such prefix"; restated at line 4205: "the
255-byte cap on a user-metadata key is this specification folding §4.6's
name rules onto keys, which carry no length prefix to force it"). If "A
name" in the Note were read to include keys, "its length prefix is
§7.4's framing" would be **false** for a key (no length prefix exists to
be framing). I resolved this by checking the document's own vocabulary:
every place a "key" is discussed it is called "key," never "name" (line
4183-4184 keeps them grammatically distinct: "a layer, dimension or
channel name ... and a user-metadata key ..."), and R-ENC-15's own
uniqueness rule explicitly carves user-metadata keys out ("Uniqueness of
user-metadata keys is defined by the user-metadata document (§18)," line
586-587) — meaning keys are not covered by the very citation (R-ENC-15)
the repaired sentence leads with. So "A name" in this Note, read in the
document's own idiom, denotes only the layer/dimension/channel name
fields it is citing (via R-ENC-15/F4/L9), not user-metadata keys. I
treat this as a **rejected candidate**, but it is close enough to the
"exhaustive claim" failure shape that I want it on record: a reader who
does not check the key/name distinction could draw the wrong conclusion
from this sentence.

**Check 4 (contradiction) — does the new "not its value" framing
contradict anything?** I found the direct precedent this repair is
bringing "name" into line with: §13.1's fill-field paragraph (lines
1901-1906), pre-existing and untouched by any of my hunks: "The fill
value is structural (§4.7): it fixes what unstored samples read as, and
a verifier's acceptance of a tile turns on it ... though it never
affects how any byte is located or decoded; the field's length prefix is
§7.4's framing, cross-checked against the element size (`[R-CNT-23]`)."
This is structurally identical to the new name sentence: structural via
an *acceptance* consequence, with the length prefix separately carved
out as "framing" rather than "value." The **old** name sentence ("A
variable-length field's value includes its length prefix") directly
contradicted this established convention (value vs. framing are treated
as distinct throughout §4.2-4.6, e.g. line 460-461: "a record's
inline_length is a `u32` (§7.2), and a name's or fill's length prefix a
`u8` (§4.6, §7.4)" — length prefixes are given their own field-width
rule, separate from the "value" concept). So the repair removes a real
inconsistency and brings "name" into alignment with the already-
established "fill" pattern. I looked for any other place that still
asserts the *old* claim ("a field's value includes its length prefix")
and found none (`grep -n "includes its length prefix"` → zero hits,
confirmed by a control search for a phrase from the same paragraph, see
sweeps below). **PASS — the repair is a genuine, well-grounded fix, not
a new contradiction.**

**Check 6 (unconstrained siblings).** The structure here is "a name
field" (layer/dimension/channel). Two facets: (a) is it structural?
(b) what determines its length? (a) is answered by R-ENC-16 (all fields
but version_minor are structural) — fully constrained. (b) is answered
by §7.4's table (`u8 len + bytes`) for all three name instances — fully
constrained. I looked for a sibling quantity left hanging (in the style
of the charter's compressed-frame-header example) and did not find one:
this sentence touches one field (name) with one binary classification
and one already-fixed length-prefix width; there is no second,
unconstrained quantity riding alongside it in this passage.

**Check 7 (analogy).** None present (no "as X does" construction).

**Check 8 (anaphor).** This hunk replaces one sentence with two new ones
inside the Note; nothing after it in the Note refers back with "it" /
"that" / "such" to the deleted sentence's content. I read forward to the
end of the Note (line 626) — the remaining sentences ("Every non-obvious
encoding is followed ...", "All named constants appear once in Appendix
B") are self-contained and do not backreference the name discussion.

**Byte-level test.** Not byte-level. The sentence sits in a non-normative
Note (see check 3), and even setting that aside, both the "duplicate →
error" and "name is structural" claims are independently normative
elsewhere and unchanged in substance; no conforming implementation's
accept/reject or emit behavior turns on this sentence's wording.

**Verdict: repair is sound and fixes a genuine internal inconsistency
(value vs. framing for names, now matching the fill-field precedent);
flagging for the record that its landing spot is non-normative and that
"A name" could, on a careless reading, be conflated with "a
user-metadata key" — both reported as non-defects on inspection.**

### Hunk 34 — §21.1 opening (two edits in one hunk)

**Diff (edit A).**
```
- quarantine does for every §21.5 row and `[R-MTA-09]` for the frame
- constraints R4 registers, whatever the containing scope —
+ quarantine does for every way a §21.5 row makes the document
+ unreadable and `[R-MTA-09]` for the frame constraints R4 registers,
+ whatever the containing scope —
```

**Diff (edit B).**
```
- identifiers following it in parentheses are the further rules the
- condition reads, or the section stating what it reads where no
+ identifiers following it in parentheses are further rules the
+ condition reads, a finding aid and not the whole of them, or the
+ section stating what it reads where no
```

**Rule the repair adopts (A).** Narrows the express-assignment clause
for `[R-CNT-25]` from "every §21.5 row" (a row-level quantifier) to
"every way a §21.5 row makes the document unreadable" (a condition-level
quantifier keyed to unreadability).

**Rule the repair adopts (B).** Withdraws the implicit completeness
claim in "the further rules the condition reads" (definite article) and
replaces it with an explicit disclaimer: parenthetical identifiers are
"further rules ... a finding aid and not the whole of them."

**Check 1 (tense/quantifier), edit A.** I opened every §21.5 row (lines
3948-3981) to test whether each is "a way the document can be
unreadable." §21.5's own pre-existing lead paragraph (untouched by my
hunks, lines 3950-3966) already makes this exact classification: "User
metadata is quarantined (`[R-CNT-25]`): every way its document can be
unreadable takes this outcome, whatever the containing scope — as a
violation in the rows below, except at an experimental-range encoding
... and except where a reader or verifier declines the decode on the
size bound or on the frame's declared window, which `[R-MTA-09]` makes
that actor's capability and not a fact about the file." So the document
itself already frames R1-R3 and R5-R10 as "ways [the] document can be
unreadable," and separately carves R4 (frame constraints) out to
`[R-MTA-09]` — exactly mirroring the two-clause structure the repaired
§21.1 sentence keeps (R-CNT-25 clause + separate R-MTA-09 clause for
R4). Going row by row: R1 (unassigned/reserved encoding — undecoadable),
R2 (extent CRC mismatch — unverifiable, so unreadable under [R-ENC-10]'s
verify-before-use rule), R3 (decode failure under declared encoding —
literally undecoadable), R5 (ill-formed UTF-8/unpaired surrogate in
decoded content — malformed at the encoding level), R6 (empty/control-
char key), R7 (not well-formed JSON / wrong top-level type / BOM), R8
(non-finite number, which RFC 8259 disallows), R9 (duplicate keys), R10
(overlong key) — every one of these is already covered by §21.5's own
"every way ... can be unreadable" framing, which is *pre-existing text*,
not part of my hunk. **The repair's new wording in §21.1 is not a new
claim; it is §21.1 adopting §21.5's own, already-established
vocabulary.** I did not find a §21.5 row excluded from that framing that
the new §21.1 wording would wrongly sweep in. PASS.

**Check 5, edit A.** "every way" is an exhaustive claim; I tested it
against R4 specifically, since R4 is explicitly the one row NOT meant to
fall under the `[R-CNT-25]` clause (it gets its own `[R-MTA-09]` clause
in the same sentence). R4's own Governing rule cell (line 3974) is
`` `[R-MTA-09]` (R-COD-06, R-CNT-25) `` — R-MTA-09 primary, confirming R4
is exactly the row carved out of the R-CNT-25 clause and into the
R-MTA-09 clause, consistent with the sentence's own two-part structure.
PASS.

**Check 2/6, edit B.** Charter directs: "open ten Governing-rule cells
with parentheses and say whether the sentence describes them." I opened
the following ten (§21.2/§21.3, chosen for citation-count diversity):
  - F1 `` `[R-ENC-02]` (R-CNT-04, R-CNT-06) `` — condition text
    distinguishes two instances (front-block, binds R-CNT-04; trailer-
    magic, binds R-CNT-06 "every reader"). Each parenthetical rule
    governs one instance, not the row as a whole — a "finding aid," not
    an exhaustive single-source list. Matches new wording.
  - F2 `` `[R-ENC-03]` (R-CNT-06, R-CNT-13) `` — condition is a bare
    domain check (R-ENC-03); the two parenthetical rules are why the
    *specific fields* (dir_offset etc., extent_offset/length) are
    read at all (R-CNT-06 trailer fields, R-CNT-13 extent slot) — again
    partial, not exhaustive (nothing here documents, e.g., why
    dir_length specifically is u64, which is R-ENC-03 itself, already
    the primary).
  - L2 `` `[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07) `` — the
    condition text lists 9 distinct derived quantities (extent sums, N,
    P, N·P, planar C·N, interleaved P·Q, planar numeric P·Bᶜ, the index
    formula). Four rules cannot exhaustively source nine quantities'
    individual definitions (e.g., Tᵢ/Eᵢ themselves are defined in
    §11.1, not listed). Confirms "not the whole of them."
  - L21 `` `[R-CNT-17]` (R-CNT-20) `` — R-CNT-20 is cited for the CRC
    verification precondition on reading entry_count-adjacent bytes,
    not for the addressed-tile-count arithmetic itself (that's
    L21's own condition, sourced from §11.2). Partial.
  - L37 `` `[R-IDX-04]` (R-CNT-20, R-ENC-10) `` — similarly, the
    parenthetical rules are about checksum-verification preconditions,
    not the CRC-mismatch condition itself. Partial.
  - F17 `` `[R-CNT-06]` (R-LIF-04, R-CNT-10) `` — R-LIF-04/R-CNT-10
    concern transport-authoritative file size and truncation/extension,
    read alongside but not exhausting §6.2's trailer rule set. Partial.
  - F29 `` `[R-CNT-12]` (R-ENC-07) `` — R-ENC-07 (fixed field widths)
    is one contributing rule among several a reader needs (record
    framing widths, walk termination) to detect this condition; not the
    whole of what's read. Partial.
  - F33 `` `[R-CNT-13]` (R-CNT-02, R-IDX-03) `` — this condition
    explicitly cross-references bounds rows "at [their] own tier"
    (F9/F10, F30-32, L15-17, T8/T9) in its own prose, none of which
    appear in the Governing-rule parenthetical at all — direct evidence
    the parenthetical is a "finding aid," since the condition text
    itself names more rules than the cell does.
  - L44 `` `[R-COD-07]` `` (single rule, no parens) — not applicable to
    this test but confirms not every cell has a parenthetical; when one
    exists, it is added information, not obligatory completeness
    machinery.
  - F14 `` `[R-CNT-06]` (R-CNT-20, R-ENC-10) `` — R-CNT-20/R-ENC-10 are
    about the checksum-verification-before-acting discipline, which
    applies generally (line 524-528) and is not specific or exhaustive
    to this one field's CRC check.
  In all ten, the parenthetical set reads as a *pointer* to related
  rules the condition also touches, never as a claim that nothing else
  is involved. This is a positive, well-evidenced confirmation of the
  new wording. **The old wording ("the further rules the condition
  reads") — definite article — was the overclaim; the repair correctly
  withdraws it.** PASS.

**Check 4 (contradiction).** I checked the repair's B-clause against the
completeness clause that follows two sentences later in the same
paragraph: "Its **completeness is normative** — a *detectable*
file-conformance violation this specification names and the register
omits is a defect in this document ..." (line 3718-3720). This is a
claim about **row-level** completeness (every violation has a row), a
different axis from **citation-level** completeness inside one cell
(every rule the row's condition reads is named in the cell). The two do
not conflict: a row can be present (satisfying row-completeness) while
its Governing-rule cell cites only a finding aid (not citation-
completeness). No contradiction. PASS.

**Check 8 (anaphor), both edits.** Edit A's insertion ("every way a
§21.5 row makes the document unreadable") sits inside the existing
em-dash-delimited parenthetical, before the sentence's main clause
resumes at "the actor obliged to detect it." I traced "it" here: its
antecedent is "one malformed condition" from the sentence's opening
clause ("each row is one malformed condition, with the outcome class
its scope determines ... — except ... — the actor obliged to detect
it"), which sits *outside and before* the entire dash-parenthetical.
The insertion, being inside that parenthetical, does not introduce a
new noun phrase between "condition" and "it" that a reader would
mistake for the nearer antecedent (the parenthetical is itself
bracketed off by dashes, standard "read across the asides" parsing).
Unaffected — before and after, "it" = "condition." Edit B's insertion
sits between "further rules the condition reads" and "or the section
stating what it reads" — I traced "it" here too: by parallel structure
with "the condition reads" immediately prior, "it" = "the condition" in
both the old and the new text (the OLD sentence had exactly the same
"the condition reads ... what it reads" pairing). The inserted "a
finding aid and not the whole of them" sits between these and does
introduce one more plural noun phrase ("them" = "further rules") ahead
of "the section stating what it reads," but "it" is a bare singular
pronoun and "the condition" (singular) remains its only grammatically
compatible antecedent in the sentence (the newly inserted "them" is
plural and cannot be "it"'s antecedent) — so this resolves the same way
before and after. I also traced the sentence's final "them" ("cited
without brackets to keep them distinct from the governing one"): this
is grammatically bound to the sentence's subject, "any identifiers
following it in parentheses" (only "identifiers" can sensibly be "cited
without brackets"), not to the newly inserted "them" (which refers to
"further rules," a subset of "identifiers," so even a loose subset
reading would not produce a wrong answer). I flag this as a considered-
and-rejected candidate: the insertion does add one more plural noun
phrase for a reader to hold in mind between "further rules" and the
final "them," which is worth a maintainer's attention for readability,
but it does not change what either pronoun resolves to.

**Byte-level test, both edits.** Not byte-level for either edit: both
concern which *citation* accompanies a row/condition (a documentation
aid) or restate an existing outcome-assignment framing already present,
unchanged, in §21.5's own lead paragraph. No conforming
implementation's emit or accept/reject behavior turns on either phrase.

**Verdict: both edits are well-supported corrections; no defect found.**

### Hunk 35 — §21.1 on §21.6

**Diff.**
```
- the same terms a row does, and where such an entry and the rule it
- cites diverge, the rule governs there too.
+ the same terms a row does, each rule its Rule cell lists governing
+ the part of the entry it states and none first among them, and where
+ such an entry and a rule it cites diverge, the rule governs there
+ too.
```

**Rule the repair adopts.** Inserts a clause explaining that, unlike a
register row (which names one rule first per line 3712, "A Governing
rule cell names that requirement first"), a §21.6 entry's Rule cell,
when it lists several rules, has none of them "first" — each covers only
the part of the entry's prose it corresponds to. Also changes "the rule
it cites" (definite, implying one rule per entry) to "a rule it cites"
(indefinite, allowing several), consistent with the new premise.

**Check 1 (tense/quantifier).** "the rule" → "a rule" is exactly the
quantifier shift the charter's check 1 is built to catch, and it is
*correct* here: given the new premise (an entry can cite several
co-equal rules), the divergence test must be able to fire against *any
one* of them, not presuppose a single governing rule. I checked that
"the rule governs there too" (unchanged) still parses: within the same
sentence, "the rule" refers back to the "a rule" just introduced
(ordinary definite-reference-to-just-mentioned-indefinite, not a stale
cross-sentence anaphor). PASS.

**Check 7 (analogy) — required by charter.** Governing verb comparison:
the row convention states "each row *restates* its governing rule" (line
3726); this repair says "§21.6's entries restate their governing rules
on the same terms a row does" — same verb, "restates," used for both.
I tested the analogy on three §21.6 entries with multi-rule Rule cells,
per the charter's instruction:
  1. **"An index entry is the sentinel"** — Rule cell `` `[R-IDX-02]`,
     `[R-TYP-08]` ``. Defined behavior: "The tile is addressed but not
     stored [→ R-IDX-02, opened at lines 2209-2218: defines the
     sentinel pattern and that it means "addressed but not stored"];
     every sample position it carries ... reads ... as that channel's
     fill [→ R-TYP-08, opened at line 1943: "decoded and fill
     channels"]." Each rule governs a **different clause** of the same
     entry, exactly as the new text claims, and neither is "first" in
     any operative sense (both are needed, for different halves of the
     sentence). Analogy holds for this row.
  2. **"A user-metadata record declares an experimental-range (≥ 0x80)
     document encoding"** — Rule cell `` `[R-MTA-03]`, `[R-EXT-03]`,
     `[R-CNF-02]`, `[R-MTA-10]` ``. Defined behavior text: "Ignored
     (ignore-record); the file is conforming — §10.3's prohibition
     binds a writer's conduct, not the bytes. No document rule attaches
     at such an encoding, so a verifier certifies, reporting the record
     it ignored." Four clauses, four rules — consistent with "each rule
     ... governing the part of the entry it states," none singled out
     as primary.
  3. **"A payload contains a byte string that mimics a trailer"** — Rule
     cell `` `[R-LIF-05]`, `[R-LIF-06]`, `[R-LIF-08]` ``. Defined
     behavior: "Inert: no reader scans backward (`[R-LIF-05]`), the
     coverage walk claims a live payload's bytes ... (`[R-LIF-08]`),
     and enumerates nothing in slack, and a recovery tool re-verifies
     its output whole (§9.6) ..." — two of the three rules are pinned
     inline to their clauses by the prose itself; the third (R-LIF-06)
     is the remaining, unpinned middle clause. Consistent with "none
     first among them," and also illustrates the entries are not always
     as neatly one-rule-per-clause as example 1 — still no single
     "first" rule, though.
  Governing verb in all three cases: "restates" (§21.1's framing) vs.
  what the entries actually do (state a defined behavior and cite the
  rule(s) it comes from) — I read this as the same relationship the
  register rows have to their own governing rule, just distributed
  across more than one citation per entry. Analogy reported as sound in
  the sense used; the one place it strains is that entry 3 does not
  cleanly assign one rule per clause the way entry 1 does, but the
  repair's own wording ("governing the part of the entry it states")
  is loose enough to cover that case without becoming false.

**Check 4 (contradiction).** Compared against the row convention two
paragraphs up ("A Governing rule cell names that requirement first" —
line 3712). The new clause explicitly says §21.6 entries do *not* work
that way ("none first among them"), which is a *stated* difference
between rows and entries embedded inside a sentence that otherwise says
they work "on the same terms." I read this as the sentence narrowing
what "same terms" means (both restate, and both yield to a cited rule on
divergence) while explicitly excepting the one convention (single "first"
rule) that does differ — not a silent contradiction, since the exception
is spelled out in the same breath, not left implicit. I flag this as a
considered-and-rejected candidate: a very literal reading of "on the same
terms" before the explanatory clause could momentarily suggest full
symmetry with rows, but the sentence itself immediately corrects that
before a reader could act on it.

**Check 8 (anaphor) — required for insertions.** Read forward from the
insertion to "The **Instances** column enumerates ..." (next paragraph
start, line 3750) and traced every back-reference in between: "the rule
governs there too" — "the rule" resolved above (= "a rule" just
introduced); "there" = "in a §21.6 entry" (the sentence's own topic,
untouched by the insertion, since the insertion sits *before* "and where
such an entry ..." not between it and "there"). No other bare "it" /
"that" / "such" appears before the paragraph boundary. Unaffected.

**Byte-level test.** Not byte-level: this is a citation/convention
clarification, not a change to which bytes a conforming file may
contain or which verdict a reader/verifier must reach.

**Verdict: no defect found; analogy checked and holds under the
document's own examples.**

### Hunk 36 — §21.1, R-TYP-04 / R-SER-08

**Diff.**
```
- is why `[R-TYP-04]` (§12.3) makes it the one case where a reader
- resolves a byte to a sample value rather than serving it through; `[R-CNT-12]`'s reading of MU = 1 with PE = 0 as PE = 1 (F25,
- L46) resolves a flag and returns no data.
+ `[R-TYP-04]` (§12.3) records as the one such case; `[R-CNT-12]`'s
+ reading of MU = 1 with PE = 0 as PE = 1 (F25, L46) resolves a flag
+ and returns no data.
```

**Rule the repair adopts.** Changes the relationship asserted between
R-SER-08 and R-TYP-04 from causal/defining ("which is why `[R-TYP-04]`
... makes it the one case") to descriptive ("which `[R-TYP-04]` ...
records as the one such case").

**Check 2 (citations) — required by charter ("resolve 'such'").** Opened
R-TYP-04 (§12.3, lines 1855-1867): "A sample value is its bit pattern
... Writers and readers MUST NOT alter a value's encoded bytes ... In a
conforming file this rule admits no exception; **the one case** where a
reader resolves a byte to a value rather than passing it through arises
only in a nonconforming file, and `[R-SER-08]` **states** it.
`[R-TYP-04]`" Opened R-SER-08 (line 2051, in context 2040-2051): defines
the specific behavior — resolving a nonconforming interleaved boolean
byte to a sample value. So, in the document's own words: **R-TYP-04
makes the uniqueness/exclusivity assertion** ("the one case ... arises
only ..."), and **R-SER-08 states the specific rule**. "Such" in the
repaired sentence ("records ... as the one such case") resolves
unambiguously to "a case where a reader resolves a byte to a sample
value rather than serving it through" — the clause immediately
preceding it in the same sentence. Both "records" (new) and "makes"
(old) are defensible glosses of what R-TYP-04's own sentence does
(it is R-TYP-04, not R-SER-08, that asserts the "one case" framing) —
if anything "records" undersells R-TYP-04's role slightly less than
"makes" does, since R-TYP-04's own wording ("this rule admits no
exception; the one case ... arises only ...") is itself already an
assertion, not a report of someone else's fact. I do not find this
substitution to change the truth conditions of the sentence; it is a
stylistic softening, not a citation error. PASS (both citations resolve
to text that supports the repaired claim).

**Check 4 (contradiction).** I checked R-TYP-04's own exclusivity claim
("this rule admits no exception ... the one case ... arises only in a
nonconforming file") against the paragraph's second half, unchanged by
this hunk: "`[R-CNT-12]`'s reading of MU = 1 with PE = 0 as PE = 1 (F25,
L46) resolves **a flag** and **returns no data**." This is explicitly
distinguished from R-SER-08's case by the paragraph's own wording
("`[R-SER-08]` is the one rule that goes the other way **for a value a
reader returns**" — line 3793) — R-CNT-12's flag resolution does not
return a value at all ("returns no data"), so it is not a counter-
example to R-TYP-04's "one case" claim, which is scoped to values a
reader *returns*. No contradiction. Verified F25/L46 both cite
`[R-CNT-12]` and both concern the MU=1/PE=0 combination (opened at lines
3835, 3906), consistent with the sentence.

**Check 8.** No new back-reference introduced; "which" in "which
`[R-TYP-04]` (§12.3) records" refers to the immediately preceding clause
in the same sentence ("it resolves a nonconforming interleaved boolean
byte to a sample value rather than serving it through"), unchanged in
position and content by the edit.

**Byte-level test.** Not byte-level — purely a description of the
relationship between two already-existing, unchanged rules.

**Verdict: no defect found.**

### Hunk 37 — §21.6, two cells

**Diff (cell 1, zero-layers row).**
```
-| The file contains zero layers | ... | `[R-CNT-14]` (R-CNT-02) |
+| The file contains zero layers | ... | `[R-CNT-14]`, `[R-CNT-02]` |
```

**Diff (cell 2, slack row).**
```
-...; only compaction reclaims it | `[R-CNT-21]` |
+...; only a rewrite reclaims it | `[R-CNT-21]` |
```

**Cell 1 — Check 2/4.** Charter: "hold the first to hunk 35's convention
and to the cell's other citations' form." I read every multi-rule Rule
cell in §21.6 (lines 3991-4005, reproduced in full above under my
reading): every single one uses comma-separated bracketed citations —
`` `[R-IDX-02]`, `[R-TYP-08]` ``; `` `[R-MTA-03]`, `[R-EXT-03]`,
`[R-CNF-02]`, `[R-MTA-10]` ``; `` `[R-CNT-15]`, `[R-CNT-18]`,
`[R-WRT-08]` ``; `` `[R-LIF-05]`, `[R-LIF-06]`, `[R-LIF-08]` ``; ``
`[R-MTA-09]`, `[R-ERR-04]` ``. The old zero-layers cell,
`` `[R-CNT-14]` (R-CNT-02) ``, was the **only** cell in this table using
the register's own (§21.2-21.5) first-plus-unbracketed-parenthetical
convention — inconsistent with every sibling cell in its own table, and
inconsistent with hunk 35's just-inserted rule that §21.6 citations have
"none first among them." The repair's comma-bracketed form brings it
into line with both. Also verified R-CNT-14 itself (lines 1063-1071):
"any number of layer records (zero is valid: a directory carrying no
layer record is a conforming generation, an empty directory included)"
— near-verbatim source for the cell's defined-behavior text. R-CNT-02
was already cited before this hunk (only its punctuation changed), so
no new citation-accuracy question is introduced. PASS — this is a
format-consistency fix, not a citation-accuracy fix, and it is fully
warranted by the evidence.

**Cell 2 — Check 2/4, required by charter ("hold ... to [R-CNT-21] and
§5.2").** Opened R-CNT-21 itself (lines 740-747, the paragraph defining
what a partial slack total is and how it is reclaimed): "**Only a
rewrite (§20.5) reclaims it, compaction being the rewrite an operator
runs for that alone.** `[R-CNT-21]`" This is a **verbatim match** for
the repaired cell's "only a rewrite reclaims it" — meaning the *old*
cell text ("only compaction reclaims it") had gone stale relative to
R-CNT-21's own (already-updated, by a different commit in this round)
wording, and this hunk is the correct sweep of that restatement. Also
checked §5.2 (lines 697-748): its own slack paragraph (line 709-720)
does not use either "compaction" or "rewrite" for the reclaiming actor
directly, but does say "a verifier ... MUST report the total number of
slack bytes, since that number is what tells an operator to **compact**"
(line 714-715) — this is *not* swept by this hunk (it is untouched
context, outside the two hunks I was given), and it is **not
inconsistent** with the repaired cell, because R-CNT-21's own text
explains why: compaction is specifically "the rewrite an operator runs
for [reclaiming slack] alone" — i.e. compaction remains the correct,
specific term for "the reclaiming action an operator chooses to run,"
while "a rewrite" is the correct general term for "the class of writer
tier capable of reclaiming it" (which also includes rewrites run for
other reasons, e.g. dropping or re-declaring a layer, that reclaim slack
as a side effect). Both statements are true simultaneously under
R-CNT-21's own gloss; not a contradiction, and not something this
hunk's charter asked me to sweep. PASS.

**Check 8.** Table cells; no anaphora to trace.

**Byte-level test.** Cell 1: not byte-level (citation formatting only).
Cell 2: not byte-level — R-CNT-21 itself (the actual normative source)
already said "only a rewrite ... reclaims it" before this hunk; the
§21.6 cell was a restatement lagging behind its own governing rule, and
per §21.1's own "where such an entry and a rule it cites diverge, the
rule governs" (hunk 35, same subsection), R-CNT-21 already controlled
even while the stale cell text stood. Fixing the restatement does not
move the emittable/acceptable byte set.

**Verdict: both cells are correct, well-evidenced sweeps of stale
restatements; no defect found.**

### Hunk 38 — §22.3 byte coverage

**Diff.**
```
-exactly: every byte a reader can reach belongs to one named structure.
+exactly: every byte a reader can reach is the front signature block or
+belongs to exactly one named structure.
```

**Rule the repair adopts.** Adds the front signature block as an
explicit alternative to "belongs to ... a named structure," and restores
"exactly one."

**Check 2/4 — required by charter ("hold it to [R-CNT-02] and to §5.2's
own words on what the front block and the trailer are counted as").**
Opened R-CNT-02 directly (§5.2, lines 697-707): "Every byte of the live
committed state belongs to **exactly one of: the front signature block;
or a structure** — a stored-tile extent, a record extent ..., **the
directory, or the trailer**. No two of them overlap ... `[R-CNT-02]`"
This is the authoritative partition, and it treats the front signature
block as a category **distinct from** "a structure," while the
**trailer is explicitly enumerated as one of the things that counts as
"a structure."** The **old** §22.3 sentence ("every byte a reader can
reach belongs to one named structure") is inconsistent with this: taken
literally, it would require the front signature block's 16 bytes to
"belong to ... a named structure," which R-CNT-02 itself says they do
not (they are the alternative to "a structure," not an instance of it).
The **new** sentence — "is the front signature block or belongs to
exactly one named structure" — reproduces R-CNT-02's own "front
signature block; or a structure" split exactly, and reinstates "exactly
one," matching R-CNT-02's "exactly one of." The trailer is correctly
left folded into "structure" (not given its own special case), matching
R-CNT-02's enumeration. PASS on both counts the charter named.

**Check 5 (exhaustive claim).** "exactly one" checked against R-CNT-02's
"exactly one of" and against "No two of them overlap" (line 706) — the
repaired wording's "exactly" is directly licensed by this text, not an
overclaim.

**Check 8 (anaphor) — required for insertions.** Read forward to the end
of the paragraph (line 4260): "**It** bounds nothing outside that —
slack is unconstrained ... — so coverage makes bytes reachable by a
reader accounted for ..." "It" = "Byte coverage" (the sentence's
subject, established two sentences earlier: "Byte coverage
(`[R-CNT-02]`) partitions the *live* state exactly"). The insertion sits
*inside* the sentence that "It" refers back to (it modifies what the
partition consists of), not between that sentence and "It" — so "It"'s
resolution is unaffected before and after. No other back-reference
appears before the paragraph ends at "accounted for, and makes
everything else *countable* rather than / absent."

**Byte-level test.** I considered this carefully since §22.3 is
normative prose citing R-CNT-02 directly, unlike hunk 04's Note.
**Conclusion: still not byte-level**, because R-CNT-02 itself (the
actual rule with force, opened above) already states the front-block/
structure split and the "exactly one" requirement; §22.3's sentence is
explicitly introduced as a restatement ("Byte coverage (`[R-CNT-02]`)
partitions ... exactly:"), and per this document's own convention
(stated for both §21 rows and §21.6 entries, and reasonably read as
general practice given how consistently it is applied everywhere I
checked in this audit), a restatement that diverges from the rule it
cites yields to the rule. R-CNT-02 was never ambiguous about the front
block; the old §22.3 sentence was an imprecise gloss of an unchanged
rule, not an independent source of a different requirement. No
conforming implementation's accept/reject or emit set moves.

**Verdict: correct, well-evidenced fix; no defect found.**

## 3. Rejected candidates (recorded in full above, summarized here)

1. Hunk 04: "A name" could, on a careless reading, be conflated with "a
   user-metadata key," which the document's own §4.6/§18.2 language
   folds the same *name rules* onto but which explicitly "carries no
   length prefix." Resolved: the document's own vocabulary keeps "name"
   and "key" distinct everywhere I checked, and R-ENC-15 (the sentence's
   own leading citation) explicitly excludes keys from its uniqueness
   rule. Not a defect.
2. Hunk 04: the repaired sentence sits inside a Note-labeled (non-
   normative, per [R-CNF-01]) blockquote. Resolved: both the "duplicate
   → error" and "name is structural" substance are independently
   normative elsewhere (R-ENC-15, R-ENC-16), so the repair's location
   does not create a force gap. Reported for the record per the
   charter's explicit instruction on this hunk, not as a live defect.
3. Hunk 34/35: "on the same terms a row does" momentarily reads as
   claiming full symmetry between register rows and §21.6 entries before
   the sentence's own next clause ("none first among them") narrows it.
   Resolved: the qualifying clause is in the same sentence, immediately
   correcting the reading, not a silent later contradiction.
4. Hunk 34: the "finding aid, not the whole of them" clause adds one
   more plural noun phrase ("them" = further rules) ahead of the
   sentence's final "them" ("keep them distinct from the governing
   one"). Resolved: the final "them" is grammatically bound to the
   sentence's subject ("any identifiers ..."), not to the newly
   inserted phrase, in both the old and new text.
5. Hunk 37 (slack cell): §5.2's own line "tells an operator to compact"
   looks, out of context, like a leftover use of the old "compaction"
   terminology next to the newly worded cell. Resolved: R-CNT-21's own
   text explains both are correct simultaneously (compaction = the
   specific rewrite run for reclaiming alone; "a rewrite" = the general
   class). Also outside my seven hunks' scope to sweep.
6. Hunk 36: "records" (new) vs. "makes" (old) as the verb describing
   what R-TYP-04 does to the "one case" claim. Resolved: R-TYP-04's own
   text already contains the assertion ("this rule admits no exception
   ... the one case ... arises only ..."), so both verbs are defensible
   glosses; no truth-condition change.

## 4. Checks that ran clean with no candidate at all

- NESTED_DASH: scanned every hunk's post-repair text for an em-dash pair
  nested inside a clause already set off by em-dashes. None of the seven
  hunks' changed text contains more than the pre-existing single dash
  pairs already in context (hunk 34's "— except ... —" is one pair, not
  nested; hunks 03/04/35/36/37/38 contain no em dashes in their changed
  lines at all). No NESTED_DASH findings.
- BCP-14 casing: none of the seven hunks introduce a new BCP-14 keyword
  (MUST/SHOULD/MAY/etc.) in any casing; none to check.
