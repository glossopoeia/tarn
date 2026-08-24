# Audit transcript — hunks 3 and 4

Auditor scope: hunk-03.diff (§21.5 rows R6 and R8) and hunk-04.diff (§21.7,
the account of what no check detects).

## 0. Disclosure

Files read: `/private/tmp/.../r24audit/hunk-03.diff`,
`/private/tmp/.../r24audit/hunk-04.diff`, and
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (passages listed
below). Nothing else. I did not open `full.diff`, other hunk files, `docs/`,
`conformance/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`spec/registry.json`, git history, or the web. I did not list the r24audit
directory.

Commands run (all against spec/tarn.md only):

```
wc -l spec/tarn.md
grep -n "^#### 21\.\|^### 21\|^## 21\|^#### 20\.\|^### 20" spec/tarn.md
sed -n '3317,3400p'   (§21.1 in full)
sed -n '3546,3580p'   (§21.5 in full, post-repair)
grep -n "R-MTA-04\|R-ENC-12\|R-ENC-11\|R-CNT-25\|R-MTA-03\|R-MTA-10\|R-MTA-09" spec/tarn.md
sed -n '2530,2605p'   ([R-MTA-04], [R-MTA-05], [R-MTA-10])
sed -n '860,900p'     ([R-CNT-25])
sed -n '465,500p'     (§4.6, [R-ENC-11], [R-ENC-12], [R-ENC-13])
sed -n '3634,3712p'   (§21.7 post-repair, §21.8, head of §21.9)
sed -n '2934,3060p'   (§20.3 append procedure, step 4 and the shrink paragraph)
grep -n "^#### 17\.\|^### 17\|^#### 14\.\|^### 14" spec/tarn.md
sed -n '2212,2260p' ; sed -n '2357,2400p'   (§17.1/§17.2 head, §17.3)
sed -n '3512,3546p'   (§21.4, all 26 tile rows)
sed -n '3192,3316p'   (§20.5 compaction, [R-WRT-06], [R-WRT-07], [R-WRT-09])
sed -n '735,830p'     (§6.2 trailer layout, §6.3 gates)
sed -n '196,235p'     ([R-CNF-11], [R-CNF-07])
grep -n "R-CNF-11\|R-CNF-07\|R-CNF-05" spec/tarn.md
grep -n "witness\|unwitnessed" spec/tarn.md
grep -n "Neither obligation" / "no witness at all" / "four obligations" /
        "\*sometimes\*" / "exactly as a" spec/tarn.md
sed -n '3455,3512p' | grep -n "codec\|filter"   (L43, L45)
sed -n '2462,2480p'   (§18.2's own "carry no witness" sentence)
sed -n '1321,1340p'   (§9.7)
sed -n '3222,3234p' ; sed -n '3653,3698p'   (exact quotes)
```

Unrequested context that appeared before I began: a project instruction file
pointer (CLAUDE.md → AGENTS.md) and an index of the maintainer's memory files
with one-line descriptions, plus a git status/recent-commit listing. I did not
open any of them and I have not used their contents; I name their appearance
here as required. I note that I did not read AGENTS.md itself. Two memory-index
lines and the commit subjects would, if acted on, have pointed at areas of the
document; every conclusion below is reached from the spec text quoted inline,
and I have cited the spec line for each.

Hard-wrap discipline: every grep I relied on used a short fragment that cannot
wrap ("Neither obligation", "no witness at all", "four obligations",
"witness", "codec", "filter", bare requirement IDs). Where I needed a phrase
that spans lines I read the passage with `sed` instead of grepping for it.

---

# HUNK 3 — §21.5, rows R6 and R8 (spec line 3574 and 3576)

## The rule each edit adopts, in my words

**R6's Governing-rule edit.** Before: `[R-CNT-25]` (R-ENC-12). After:
`[R-MTA-04]` (R-CNT-25, R-ENC-12). What it makes true of an implementation:
nothing about bytes. It relocates the answer to "which requirement *defines*
the condition that a user-metadata key is empty or carries U+0000–U+001F" from
the quarantine rule to the decoded-document rule, demoting the quarantine to a
rule the condition merely reads.

**R8's Condition edit.** Before: "A user-metadata document contains a
non-finite number, in any form". After: the same, plus (a) a restatement of
the two forms [R-MTA-04] names, and (b) an argument that those two forms are
one instance and therefore that the Instances cell stays at two (one per
container). What it makes true: for a corpus builder, that R8 gets exactly two
vector files and neither need carry a bare `NaN`/`Infinity`/`-Infinity` token.

## §21.1's definition of a Governing rule cell (spec 3320–3329), quoted

> "enumerates every detectable file-conformance violation this specification
> names: each row is one malformed condition, with the outcome class its scope
> determines (§2.4) — except where a rule assigns one expressly, as
> `[R-CNT-25]`'s quarantine does for every §21.5 row, whatever the containing
> scope — the actor obliged to detect it (`[R-CNF-04]`, `[R-CNF-11]`), the
> point by which detection is due (§19.2), and **the requirement that defines
> it. A Governing rule cell names that requirement first; any identifiers
> following it in parentheses are the further rules the condition reads**"

So the cell holds the *defining* requirement, and §21.1 in the same breath
separates that from the *outcome-assigning* rule, which for every §21.5 row is
[R-CNT-25]. On that reading the pre-repair R6 named the outcome-assigner where
the definer belongs, and the repair is in the right direction.

### Does [R-MTA-04] actually define R6's condition? (check 2)

[R-MTA-04], fourth bullet (spec 2559–2566):

> "**Well-formed UTF-8 throughout** (`[R-ENC-11]`) — including after escape
> resolution: … — and every key satisfying §4.6's name rules — non-empty, at
> most 255 bytes, free of U+0000 through U+001F."

Yes. Empty key and U+0000–U+001F in a key are literally there. Verdict:
**passes**. [R-ENC-12] (spec 486–495) is the underlying §4.6 rule and is
correctly parenthesised; it also carries the quarantine carve-out ("except for
a key inside a user-metadata document, where `[R-CNT-25]`'s quarantine governs
and the outcome is ignore-record"), so [R-CNT-25] in parentheses is
defensible. Verdict on both parentheticals: **passes**.

One point in the repair's favour that I checked and want on the record:
[R-MTA-10] (spec 2582–2600) withdraws "the decoded-document restrictions
above" under an unassigned encoding. R6's condition presupposes a *decoded*
document, so anchoring it in [R-MTA-04] rather than [R-ENC-12] gets the
encoding-scoping right for free. The repair is not merely a relabelling.

### Do the other rows from the same source rule agree? (charter bullet 1)

Mapping §21.5's document rows onto [R-MTA-04]'s four bullets:

| bullet | subject | row | Governing cell |
|---|---|---|---|
| 1 | object, unmarked | R7 | `[R-MTA-04]` (R-CNT-25) |
| 2 | finite numbers only | R8 | `[R-MTA-04]` (R-CNT-25) |
| 3 | no duplicate keys | R9 | `[R-MTA-04]` (R-CNT-25) |
| 4 | UTF-8 well-formedness / surrogates | **R5** | **`[R-CNT-25]` (R-MTA-04, R-ENC-11)** |
| 4 | key non-empty / U+0000–U+001F | R6 | `[R-MTA-04]` (R-CNT-25, R-ENC-12) — *the repair* |
| 4 | key ≤ 255 bytes | R10 | `[R-MTA-04]` (R-ENC-12) |

All four bullets are covered by rows and no bullet is orphaned (check 6 on the
[R-MTA-04] structure: bullet 1 → R7, bullet 2 → R8, bullet 3 → R9, bullet 4 →
R5+R6+R10; [R-MTA-05]'s ordering obligation is carried by F27/L48, which §21.1
names at 3390–3392). Nothing in that structure is left unconstrained by the
repair.

But R5 and the repaired R6 are now exact mirror images: the same three rules,
first two swapped. `[R-CNT-25]` (R-MTA-04, R-ENC-11) against `[R-MTA-04]`
(R-CNT-25, R-ENC-12). They are drawn from the *same bullet* of the *same*
requirement. Pre-repair, R5+R6 agreed with each other and disagreed with R10;
post-repair, R6+R10 agree and R5 is alone. The repair swept one of the two
rows that needed sweeping. Recorded as **B-02**.

Counter-argument I weighed and did not find sufficient: [R-CNT-25] (spec
889–893) itself enumerates "content violating the document's own rules
(ill-formed UTF-8 included, `[R-ENC-11]`)", and R5's condition text begins
"violates the document's own content rules", so R5's cell tracks [R-CNT-25]'s
own words. That is why I record B-02 as PLAUSIBLE rather than CONFIRMED: it is
a maintainer's choice which of the two rows to align, not a demonstrable error
in R6. But the two rows cannot both be right about which requirement *defines*
a decoded-document content violation, and the repair created the split.

### R8: is the instance argument sound, and on which sentence of §21.1?

The repaired cell says the overflow form and the bare-token form are

> "the two being one instance because a document carrying a bare token is not
> well-formed JSON either, so no file exhibits this row's predicate alone
> through one (§21.1, R7)"

§21.1's instance rules (spec 3352–3379). The relevant sentences, quoted:

1. "An instance names a field the condition ranges over, a container it can
   occur in, **one of several alternatives the condition text states**, or any
   combination of the three — a condition applying to two alternatives in two
   containers has four."
2. "a row whose check ranges over a family without the condition changing
   shape states that range as a single instance (T24's *any codec*), and one
   whose members give the condition materially different shapes enumerates
   them (T15, T25)."
3. "One instance is one *distinguishable* file: where a condition is a single
   predicate over several fields — a sum against a bound, a combination of two
   flag bits — the fields it reads are not instances, **because no two files
   could differ**."

Sentence 1 is the one the edit trips. Before the repair the cell read "in any
form" and sat squarely in sentence 2's family clause: one range, one shape,
one instance per container. The repair **states the alternatives in the
condition text**, which by sentence 1 makes them instances — "a condition
applying to two alternatives in two containers has four" — and then argues its
way back out.

The ground it argues on is not in §21.1. Word-for-word (check 7's comparison,
applied to a warrant that is a citation rather than a rule):

- repair's governing verb: "**no file exhibits this row's predicate alone**
  through one"
- §21.1's governing verb: "**no two files could differ**"

Those range over different sets. §21.1 quantifies over pairs of files drawn
from *this row's own* alternatives and asks whether they could differ; the
repair quantifies over *other rows* and asks whether this row fires in
isolation. Nothing in §21.1 makes co-firing with another row a reason to
collapse an instance. §21.1's only machinery for row overlap is the
specialization sentence — "Some rows are strict specializations of others — F1
of F6 and of F8, F35 of F36, L24 of L25 — and a file exhibiting a
specialization is recorded against the narrower row" — which decides *which
row records a file*, not how many instances a cell has, and which in any case
does not list R8/R7 (correctly: neither is a strict specialization of the
other, since R8 also covers `1e400`, which is well-formed JSON, and R7 covers
non-numeric malformations).

Falsification attempt on the argument's factual claim: is a bare `NaN` really
not well-formed JSON? [R-MTA-04] bullet 2 (spec 2545–2552) says the bare
tokens are ones "which RFC 8259 does not admit and some parsers accept
regardless". So yes, R7 fires too. The factual premise is true; it is the
inference from it that §21.1 does not license.

The register's own practice contradicts the inference, twice, and once inside
the very row the repair cites:

- **R7** enumerates "leading U+FEFF, top-level document; leading U+FEFF, layer
  sub-record document" as instances, although a BOM-prefixed text is *also*
  not well-formed JSON and therefore also fires R7's first alternative. By the
  repair's principle those two instances would collapse.
- **R5** enumerates "ill-formed source bytes in a key/string value" as
  instances, although a document whose source bytes are ill-formed UTF-8 is
  also not a well-formed JSON text and so also trips R7.

So the register enumerates an alternative even when another row (or another
alternative of the same row) fires on the same file. The repair adopts the
opposite principle for R8 alone.

**Does the added reasoning change what the row's condition *is*, or only
explain it?** (charter bullet 3.) Two answers, and they differ:

- As a *predicate*, no. "in any form" already covered both forms, and the two
  forms the repair names are exactly the two [R-MTA-04] bullet 2 names, so the
  restatement is faithful (see the exhaustiveness check below). Nothing a
  reader must accept or reject changes.
- As *corpus input*, yes. §21.1 says "the count is therefore mechanical once
  the cell is written" and §21.8 says "one vector per instance". The cell now
  names an exemplar for one form (`1e400`) and an argument for building
  nothing for the other. The consequence is that **no vector in the corpus
  carries a bare `NaN`, `Infinity` or `-Infinity`** — the failure mode
  [R-MTA-04] singles out as the one "some parsers accept regardless", i.e. the
  one most likely to be an implementation bug. Recorded as **B-01**.

### R8, check 5 — exhaustive claims in the repaired text

- "**in any form**" (pre-existing) — kept, and now glossed. Fine.
- "**the two** being one instance" — a count. Is the form-set really two?
  [R-MTA-04]: "a number whose binary64 interpretation is not finite — which
  covers a magnitude that overflows on conversion, `1e400` being the ordinary
  case — or any of the bare tokens". A JSON number's binary64 interpretation
  can be non-finite only by overflow (there is no JSON literal that converts
  to a NaN), so numeric form ∪ token form is exhaustive. "The two" **holds**.
- "**no file** exhibits this row's predicate alone through one" — tested
  above; the factual claim holds (R7 always co-fires), the inference does not.
- "a magnitude whose **binary64** interpretation overflows" — matches
  [R-MTA-04]'s "A reader interprets every JSON number as an IEEE 754 binary64
  value and MAY use a wider representation … a number whose *binary64*
  interpretation is not finite". The repair correctly keeps binary64 as the
  governing width despite the wider-representation licence. **Passes.**

### R8/R6, check 1 — tense and quantifier

Neither cell has a generation-sensitive quantifier: both range over "a
user-metadata document" / "a key of a decoded user-metadata document", present
tense, over the file as it stands. [R-MTA-04] is quantified the same way ("A
document is unreadable if it contains a number whose …"; "every key satisfying
§4.6's name rules"). No mismatch. **Passes.**

### R8/R6, check 3 — normative placement

Both edits are table cells in §21.5. No line in §21.5 begins with ">"; I read
the whole subsection (3546–3578). The register is normative text
([R-ERR-02] at 3702, [R-CNF-01]'s blockquote rule not engaged). **Passes.**
Neither edit is stranded in a Note or Rationale, and neither leaves a
normative statement elsewhere saying the old thing: R6's old cell content is
gone from the file (grep for `[R-CNT-25]` (R-ENC-12) returns nothing).

### R8/R6, check 4 — contradiction inside the passage

I read §21.5's whole preamble (3548–3565) and all ten rows. The preamble's
carve-outs are about experimental encodings ([R-MTA-10]) and declined decodes
([R-MTA-09]); neither collides with a key rule or a number rule. §21.5's
header count "10 conditions." is unchanged and still correct. The Instances
cells were not touched, so §21.8's "121 conditions over 277 instances" is
arithmetically undisturbed by the edit as written — but if B-01 is resolved by
enumerating, both R8 cells grow to four and §21.8's 277 becomes 279. That
consequence belongs with B-01's repair.

---

# HUNK 4 — §21.7, spec lines 3666–3692

## The rule the repair asserts, in my words

For §20.3 step 4's bar, the repair asserts a partition of the barred effects
into witnessed and unwitnessed: §14-constrained bytes → always witnessed;
decoded size → always witnessed; codec → sometimes witnessed, never assured;
filter and length-preserving sample-offset moves → never witnessed. And it
raises §20.5's unwitnessed trailer obligations from two to four. Nothing here
licenses or bars a byte; it is the document's account of which register rows
can fire, and §21.1 (3333–3335) treats §21.7 as "the account, by class, of
what fails" the detectability gate, so getting it wrong makes the register's
normative completeness claim unaudited in that class.

## Enumerating what §20.3 step 4 bars (charter bullet 1)

The bar, verbatim (spec 2996–3004):

> "A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores **in the generation this commit supersedes**,
> what §14 fixes for its stored bytes or how they decode — the set of padding
> positions (§11.3) and the content `[R-SER-05]` fixes there, the decoded
> size, the byte offset of any sample within the decoded tile image, or the
> codec and filter that produced the stored bytes."

Items, with the side the repair puts each on:

| # | barred effect | side | clause |
|---|---|---|---|
| 1 | the set of padding positions | witnessed | "A change reaching a byte §14 structurally constrains … fires §21.4's content rows" |
| 2 | the content [R-SER-05] fixes there | witnessed | same clause |
| 3 | the decoded size | witnessed | "witnessed by T3 or T14" |
| 4 | the byte offset of any sample | **unwitnessed** | "has no witness at all" |
| 5 | the codec | sometimes | "*sometimes* witnessed … but neither is assured" |
| 6 | the filter | **unwitnessed** | "has no witness at all" |

Plus the chapeau's wider reach ("what §14 fixes … or how they decode"), which
the first clause covers via "a padding position, a pad bit, or a boolean
byte", matching §14.3's pad bits and [R-SER-08]'s interleaved boolean.

Every item lands on exactly one side, and none is missing. That is the defect
this passage exists to prevent, and on the enumeration test the repair
**passes** — it is a real improvement over the pre-repair text, which listed
padding/size/codec and left the filter and the sample-offset item on neither
side, and which also said "witnessed only where … *and* the change reaches a
byte §14 structurally constrains" and then immediately witnessed two other
things, contradicting its own "only". The new "and then only for part of what
it bars" fixes that.

## Where the *sometimes* is stated, and where it is missing (charter bullet 2)

- Clause 1 (§14-constrained byte) carries no qualification and needs none.
  Checked: §20.3 carves out the harmless case itself — "a change that leaves
  every one of those tiles' stored bytes meaning exactly what they meant — a
  filter whose mandated stride makes it the identity (`[R-COD-10]`), or a new
  padding position whose stored byte already holds the fill `[R-SER-05]` fixes
  — is not what this bars." So any change that *is* barred leaves the
  constrained byte holding content [R-SER-05]/[R-SER-08] does not fix, and T4,
  T5 or T2 fires. Unqualified is correct.
- Clause 2 (decoded size) carries none and needs none. If the declared decoded
  size changes and the tile stays stored: under codecs 2–4 the decoded payload
  length no longer equals the derived size → T3; under codec 1 the entry
  length no longer equals it → T14. Assured either way. Correct.
- Clause 3 (codec) carries "*sometimes*" and "neither is assured", with a
  correct existence argument ("a writer can choose stored bytes that satisfy
  the old declaration and the new one alike"). Correct.
- Clause 4 (filter, sample offset) carries **no** qualification and asserts the
  strongest possible claim, "has no witness at all". This is the clause that
  needs one most. See below.

## Falsifying "no witness at all" (charter bullet 3) — finding B-03

The sentence (spec 3678–3682):

> "A change reaching the filter, or moving a sample's byte offset within the
> decoded image without changing that image's length, has no witness at all —
> both filter values are length-preserving (§17.3), and the content rows test
> only the bytes §14 constrains."

Three independent falsifications, each a register row.

**(a) T2 / T4 / T5, via the filter.** Filter 1 = none and filter 2 =
byte-shuffle are length-preserving, but they are *permutations*: §17.3 says
"the filtered image places byte i of group j at offset i · n + j … the inverse
restores byte i · n + j to offset j · s + i". Changing the declaration from 1
to 2 (or 2 to 1) while the stored bytes stay put means the reader reconstructs
a *permuted* decoded image. The permutation moves arbitrary bytes into the
positions §14 constrains. Concrete file: an interleaved layer with channels
c0 = uint8 numeric and c1 = bool, Q = 2, tiles stored under filter 1, codec 1;
generation 2 re-declares filter = 2 and keeps every tile stored. The inverse
shuffle now places c0 sample bytes at the bool channel's offsets. T2 —
"In an interleaved tile, a bool channel's single value byte at a real
(non-padding) sample position is neither 0x00 nor 0x01" — fires on any such
byte outside {0x00, 0x01}. Witness exists. The same construction with padding
present fires T4, and with a packed planar bool plane, T5.

The repair's own stated reason does not survive this: "the content rows test
only the bytes §14 constrains" is true and beside the point, because a filter
change is precisely a change that puts wrong bytes *at* the constrained
positions.

**(b) §21.7's own preceding clause, six lines earlier, untouched by the
repair** (spec 3656–3661):

> "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries, **except where §14
> constrains a byte's content** — a padding position, a pad bit, or an
> interleaved boolean — **and a mis-ordered image is then witnessed by T2, T4
> or T5, exactly as a mis-strided filter is**"

This says, in the same paragraph, that (i) a mis-ordered image *is* witnessed
where §14 constrains a byte's content, and (ii) a mis-strided filter *is*
witnessed. The repaired clause says a change reaching the filter, or one
moving a sample's byte offset, has no witness at all. A declaration change
that moves a sample's byte offset produces exactly a mis-ordered image; a
filter declaration change produces exactly the mis-permuted image the
mis-strided-filter case describes. Both halves of the new clause contradict
the sentence they were appended to. This is the check-7 hit the charter
predicted: the passage argues by analogy at 3660 ("exactly as a mis-strided
filter is"), and the repair's new sentence is the analogy's negation.

Verb-for-verb, since check 7 asks for it:
- 3660: "a mis-ordered image **is then witnessed by** T2, T4 or T5"
- 3678: "A change reaching the filter … **has no witness at all**"
Same set (declaration changes producing a wrongly-ordered decoded image over
tiles that remain stored), opposite predicates.

**(c) T26 states the complement explicitly.** §21.4's T26: "Filter 2 applied
at a stride other than the mandated one, **where the resulting image breaks
§14.5's padding content or `[R-SER-08]`'s bool bytes** (a wrong stride with no
such structural constraint is undetectable, §21.7)". T26 partitions the filter
case exactly the way the repair should have: witnessed where a structural
constraint is present, undetectable otherwise. The repair collapsed T26's
partition into its second half.

**(d) L45, for the invalid-value sub-case.** §21.3's L45: "Layer record's
filter is a value other than 1 or 2 — 0, reserved 3–0x7FFF, or experimental
≥ 0x8000 … `[R-COD-09]` (R-CNT-23)". A commit that changes the filter
declaration to 3 alters "the filter that produced the stored bytes" and is
barred by step 4; it is also witnessed, by L45, at layer access. The repair's
justification, "both filter values are length-preserving", silently restricts
the subject to changes *between the two assigned values* while the subject
sentence says "a change reaching the filter". (L43 is the codec analogue; the
codec clause survives it only because "sometimes … neither is assured" is not
falsified by an additional witness.)

Both halves of clause 4 therefore need the qualification clause 3 already
received. The correct statement is that a filter change, and a
length-preserving offset move, are unwitnessed **where the affected tiles
carry no padding position, pad bit or interleaved boolean byte, and the new
declaration is itself a value [R-COD-09] admits** — which is T26's parenthesis
generalised, and which is what the sound half of the repair's reasoning
actually establishes.

Recorded as **B-03**.

## Check 5 on the rest of the repaired text

- "**both** filter values are length-preserving (§17.3)" — §17.3 assigns 1 and
  2 only ("values 3 through 0x7FFF are reserved … values ≥ 0x8000 are the
  experimental range"), filter 1 is the identity and byte-shuffle says "Length
  is unchanged". The count **passes** as a statement about assigned values;
  its use to carry an unrestricted subject is the B-03 problem.
- "**no witness at all**" — falsified, B-03.
- "(T15, T17, T23, T25)" — pre-existing, and now inside a hedged sentence.
  Checked anyway: T15 (codec 2 wrapper), T17 (codec 3 magic), T23 (codec 4
  frame-not-block), T25 (malformed stream) all test stored bytes as a stream of
  the declared codec. The list is not exhaustive of such rows (T16, T18–T22 and
  T24 also do), but it is not presented as closed and the "sometimes" hedge
  removes any weight from its closure. Not reported.
- "§20.5's **four** obligations" — verified below; the count is right.
- "its **fresh** `file_id` draw" — [R-WRT-06]: "It MUST mint a fresh file_id
  for the output — a new draw under §9.3's randomness advice, not merely a
  value compared against the input's". **Passes.**

## Check 6 on hunk 4 — the structure, and every quantity in it

Two structures are governed here.

**Structure A: the set of layer declarations step 4's bar reaches.** Members
listed in the table above; all six covered, no sibling left unaccounted. I
also checked the neighbours a witness account could miss: a change to a
channel's **recorded fill** falls under item 2 and is witnessed by T4 (padding
must "encode, for each channel it carries, that channel's recorded fill
value" — a changed declaration makes the stored fill bytes wrong); a change to
a channel's **dtype at equal element width** alters no item of the list and,
per step 4's "The test is the effect on such a tile, and the list names where
that effect arises rather than standing on its own", is not barred, so §21.7
owes it nothing.

**Structure B: the output trailer of a compaction.** §6.2's layout table gives
eleven fields: trailer magic, version_major, version_minor, flags, generation,
dir_offset, dir_length, committed_file_length, file_id, reserved, trailer CRC.
Which does §20.5/[R-WRT-06] constrain beyond what a general rule already
constrains?

| field | §20.5 obligation | witnessed? |
|---|---|---|
| file_id | "MUST mint a fresh file_id … a new draw" | no |
| generation | "and generation 1" | no |
| flags | "MUST copy the input's unknown ignore-lane flag bits forward" | no |
| version_minor | "SHOULD be at least the input's" | no |
| magic, version_major, dir_offset, dir_length, committed_file_length, reserved, CRC | none beyond [R-CNT-06]/[R-CNT-24]/[R-CNT-08] | witnessed by the file-scope rows |

Four, exactly the four the repair names, and it names them in [R-WRT-06]'s own
order. This is the check-6 shape the charter warns about — one quantity pinned
and its siblings left loose — and here the repair got it right: it went from
two to the full four and no fifth exists. **Passes**, and I want that on the
record as work done rather than a claim.

## The unswept restatement — finding B-04

§20.5, inside [R-WRT-06]'s normative paragraph (spec 3231):

> "Otherwise version_minor follows `[R-CNT-26]`'s floor. **Neither obligation
> has a witness in the output alone (§21.7).**"

"Neither" ranges over the two obligations that immediately precede it — the
ignore-lane carry-forward and the version_minor floor. That is the sentence
§21.7's *pre-repair* "two obligations" restated, and it points at §21.7 by
name. §21.7 now says four. The two statements are in direct numeric conflict,
and a reader who follows §20.5's own cross-reference lands on the
contradiction immediately. The file_id and generation obligations are stated
seven lines earlier in the same paragraph (3210–3216) with no witness claim at
all, so §20.5 currently implies, by omission and by "Neither", that those two
*do* have a witness in the output alone — which is false, and which §21.7 now
says is false.

This is the project's named signature: a rule changed in one place and left
standing in another, in the very passage the repaired text cites. The repair
should have swept §20.5 to "None of the four obligations has a witness in the
output alone (§21.7)" — or, more conservatively, moved the sentence to follow
the file_id/generation sentence and widened it there.

Recorded as **B-04**.

## Check 2 on hunk 4 — every citation, opened

| citation | claim made | verdict |
|---|---|---|
| §14 ("structurally constrains — a padding position, a pad bit, or a boolean byte") | §14 fixes content at those three | **passes** — §14.5 padding, §14.3 pad bits, [R-SER-08] bool bytes |
| §21.4's content rows | rows exist for those three | **passes** — T4, T5, T2 |
| T3 "the decoded payload's own [length]" | T3 tests decoded payload length | **passes** — "The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations" |
| T14 "the entry's declared length" and "where the new declaration is codec 1" | T14 is codec-1-conditioned and tests the entry length | **passes** — "Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size" |
| T15, T17, T23, T25 | rows for the codec now declared, testing stored bytes as a stream | **passes** (non-exhaustive, see above) |
| §17.3 | both filter values length-preserving | **passes** as to length; does **not** support "no witness at all" — the same section's permutation formula is what defeats that claim |
| [R-WRT-06] | carries all four trailer obligations | **passes** |
| §20.5 | the obligations live there | **passes** |
| [R-LIF-01] | "a property of the prior generation" | **passes** — §9.1 committed-prefix immutability |
| §9.7 | "does not reconstruct" prior generations | **passes** — "A verifier checking `[R-CNT-02]`'s partition walks the live state only" |
| [R-ENC-06] | fixed field widths | untouched context; not re-verified beyond the sentence's internal logic |
| [R-ERR-01] | terminates the passage | **passes** — present at 3698 |
| §20.3 step 4 | the bar is there | **passes** — spec 2996–3004 |

## Check 3 on hunk 4 — normative placement

I read 3634–3698 in full. No line in §21.7 begins with ">"; the whole
subsection is running normative prose closed by `[R-ERR-01]`. The repair did
not land in a Note or Rationale, and there is no competing normative statement
elsewhere still saying the old thing — except §20.5's "Neither", which is
finding B-04 and which is itself normative prose inside [R-WRT-06], not a
blockquote. **Passes** as to placement; the B-04 conflict is between two
normative sentences, which is why it matters.

## Check 1 on hunk 4 — tense and quantifier

The bar's quantifier is "for any tile that layer stores **in the generation
this commit supersedes**", and §20.3 hammers the tense twice ("The tense is
the prior generation's (§3.1 defines *stored* against a generation)"; "the
quantifier is the superseded generation's"). The repair's opening restates it
as "witnessed only where the affected tiles **remain stored**" — present
tense, the *new* state. That is not a restatement of the bar's quantifier and
must not be read as one; but it is not trying to be. It is a statement about
which files carry a witness, and a witness necessarily lives in the file as
emitted, i.e. the new generation. The following sentence "And a commit that
supersedes every tile it would have damaged leaves the live state clean" makes
the two-tense structure explicit, and §20.3's shrink paragraph confirms it
from the other side: "§21.7 records the consequence — that this is precisely
where the bar has no witness, the live state being clean". The tenses agree.
**Passes.**

One looseness I checked and decided not to report: the repair lists
"generation" among the things "the output carr[ies] no record of its input's".
The generation obligation is absolute (generation 1), not relative to the
input, so the operative reason for *that* member is the trailing clause "nor
any record that it is a compaction output at all", not the input-comparison
clause. The sentence as a whole is true because that trailing clause is
present, so there is no defect — only a list member whose warrant is the
second half of the sentence rather than the first.

## Check 4 on hunk 4 — contradictions in the passage, including untouched text

I read the entire subsection and both neighbours (§20.3 step 4 and its shrink
paragraph, §20.5's [R-WRT-06]).

- Collision found at 3660 vs 3678 — B-03, above. This is precisely the
  charter's warning: the sentence written to be true under the old wording is
  the *untouched* one, and the new breadth collides with it.
- Collision found at 3231 vs 3686 — B-04, above.
- Checked and clean: §21.7's first paragraph ("None of these is a requirement
  a verifier is *unable to check* within the meaning of `[R-CNF-11]`") does
  not collide with the second paragraph's new members; [R-CNF-11] (spec
  196–223) makes *cannot establish* available only on "a capability or
  resource ground", and absence of a witness is neither.
- Checked and clean: §20.3's "§21.7 records the consequence — that this is
  precisely where the bar has no witness, the live state being clean"
  (spec 3045–3047) still matches §21.7's supersede clause.
- Checked and clean: §18.2's own "Two of those carry no witness a file
  exhibits, and R4 registers neither" (spec 2471) is about [R-COD-06]'s frame
  constraints on a user-metadata document, a different subject; the repair
  does not touch it and does not contradict it.
- Checked and clean: §21.8's "121 conditions over 277 instances" is untouched
  by hunk 4 (§21.7 carries no rows, and §21.1 says so: "neither this
  completeness clause nor the instance arithmetic below reaches … §21.7's
  account").

## Overshoot / undershoot

- Hunk 4 **overshoots** in clause 4: the defect required putting the filter
  and the sample-offset item on a side; the repair put them on the absolute
  side rather than the qualified one, when the qualified side was available and
  is what T26 already says. B-03.
- Hunk 4 **undershoots** in not sweeping §20.5. B-04.
- Hunk 3's R6 edit neither overshoots nor undershoots on its own terms; it
  undershoots only in leaving R5. B-02.
- Hunk 3's R8 edit **overshoots**: the reported problem was presumably that
  "in any form" left the forms unstated; naming them was enough, and the
  appended instance argument is the part that goes wrong. B-01.

## Byte-level test, per finding

The discriminating question is whether the disputed file is itself conforming.

- **B-01** — the disputed files are `{"a":1e400}` and `{"a":NaN}` in a
  user-metadata extent. Both carry register-row violations (R8, and R7 as
  well for the token) under *both* readings, so [R-CNF-05] bars every
  conforming writer from emitting either under both, and every reader
  quarantines both. Only the corpus's vector count moves. **Not byte-level.**
- **B-02** — §21.1's tiebreak ("where a row and the rule it cites diverge, the
  rule governs") and §21.5's header both fix the outcome independently of the
  cell. Both cells cite the same three rules. **Not byte-level.**
- **B-03** — the disputed file (changed filter declaration, tiles retained,
  a bool byte now 0x7F) is nonconforming under both readings, because T2 is a
  register row with a verifier detector and §21.7 licenses no check-skipping;
  §21.7's own first paragraph forecloses treating these as [R-CNF-11]
  cannot-establish grounds. Two verifiers reading the two readings still
  reject the same bytes. **Not byte-level** — but it is the most serious
  finding here, because §21.1 makes the register's completeness normative and
  §21.7 is the document's only account of the excluded class; a false entry
  there is a claim that a barred condition is undetectable when a row detects
  it, which is the class of error §21.1's completeness clause exists to catch.
- **B-04** — a count in prose about witnesses. No byte, no verdict.
  **Not byte-level.**

## Summary of the seven checks

| check | hunk 3 | hunk 4 |
|---|---|---|
| 1 tense/quantifier | passes | passes |
| 2 citations | R6 passes; R8's "(§21.1, R7)" — R7 passes, §21.1 **fails** (B-01) | all pass except §17.3 used beyond what it supports (B-03) |
| 3 normative placement | passes | passes |
| 4 same-passage contradiction | passes within §21.5; R5 asymmetry (B-02) | **fails** twice (B-03 at 3660, B-04 at 3231) |
| 5 exhaustive claims | "the two" passes; "no file … alone" premise passes, inference fails | "both filter values" passes as to length; "no witness at all" **fails**; "four obligations" passes |
| 6 what is left unconstrained | [R-MTA-04]'s four bullets all carried by rows — passes | all six barred effects sided, all eleven trailer fields checked — passes |
| 7 analogy quantifiers | "no file exhibits … alone" vs §21.1's "no two files could differ" — **fails** | "is then witnessed by T2, T4 or T5, exactly as a mis-strided filter is" vs "has no witness at all" — **fails** |
