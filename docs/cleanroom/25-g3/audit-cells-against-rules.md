# Repair audit — hunk-01 (§21.3 L16 Condition cell) and hunk-02 (§21.5 R7 Condition cell)

## 0. Disclosure

Read: the two hunk files named in my charter (`hunk-01.diff`, `hunk-02.diff`), and
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (many passages, listed below).
Ran: `wc`, `sed -n`, `awk`, `grep -n`, and one `python3` heredoc that reads only
`spec/tarn.md` and counts register rows/instances. I did not open `full.diff`, other hunk
files, `docs/`, `conformance/`, `registry.json`, git history, or the web, and I did not list
the r26audit directory.

Unrequested context appeared in my context window before I began: a project instruction
file pointer (CLAUDE.md -> AGENTS.md) and an index of the maintainer's memory notes naming
things like a working cadence, a register/corpus relationship, and prior workflow failures.
I did not open any of it and drew no conclusion from it; I name it here because it appeared.

Spec passages read in full:
- §4.1 (lines 370-380) — endianness, "There is no byte-order mark"
- §4.6 (Strings and names) — the three name constraints
- §7.2 (lines 899-975) — record framing, including the whole `[R-CNT-13]` extent-slot paragraph
- §7.3 (lines 975-1000)
- §15.3 entry-state table (lines 2040-2065)
- §18.1, §18.2 (whole, incl. `[R-MTA-03]`, `[R-MTA-09]`, `[R-MTA-04]`, `[R-MTA-05]`, `[R-MTA-10]`), §18.3, §18.4
- §19.3 opening (lines 2790-2810)
- §21.1 (whole), §21.2 rows F1-F36 (skimmed; F9/F10/F30/F31/F32/F33 read in full),
  §21.3 rows L1-L23 in full plus L46/L47, §21.4 rows T1-T26, §21.5 preamble + rows R1-R10,
  §21.6 (whole), §21.8

---

## 1. HUNK 1 — §21.3 row L16, Condition cell (spec line 3493)

### 1.1 The diff

```
- | L16 | A layer record's or sub-record's nonzero extent slot has extent_offset < 16, pointing into the front signature block | ...
+ | L16 | A layer record's or sub-record's nonzero extent slot has extent_offset in 1-15, placing the extent inside the front signature block | ...
```
Instances / Detector / Detected / Governing rule are untouched:
`layer record extent slot; sub-record extent slot | reader | layer access | [R-CNT-13]`.

### 1.2 The rule the repair adopts, in my words

For a layer record or a layer sub-record whose extent slot is something other than the
no-extent slot, an `extent_offset` of 1 through 15 inclusive is a layer-scope validity
error; `extent_offset = 0` is *not* this row's business, because a zero half is already the
condition L15 registers. In implementation terms: a reader validating a layer record must
reject the layer when a slot names a start byte inside the 16-byte front signature block,
and the register assigns the offset-0 case to a different row rather than to two rows.

### 1.3 The governing rule, opened and quoted (§7.2, lines 928-953, normative body text —
verified by `awk` that none of lines 928-953 begins with ">")

> The **extent slot** (extent_offset, extent_length): (0, 0) means no
> extent. Any other combination with either half zero, an
> extent_offset < 16, an extent extending past F − 64, or an
> overflowing sum is a validity error at the scope the record governs
> (§7.3): the layer for a layer record and for sub-records, the file for
> other top-level records — a malformed slot on a layer record is
> therefore reject-layer, consistent with `[R-CNT-17]`.

Condition the rule creates: over slots that are not (0,0), four independent disjuncts each
make the slot a validity error at the record's governing scope — (a) either half zero,
(b) extent_offset < 16, (c) extent_offset + extent_length > F − 64, (d) the sum overflows.
For a layer record or a sub-record the scope is the layer, hence reject-layer.

### 1.4 Deriving the numeric range myself

Register rows that restate the four disjuncts at layer scope:
- (a) either half zero → **L15** ("has exactly one of extent_offset and extent_length zero"),
  instances `layer record extent_offset; layer record extent_length; sub-record extent_offset;
  sub-record extent_length` — 4.
- (b) extent_offset < 16 → **L16** (this row).
- (c) past F − 64 → **L17**.
- (d) overflow → **L2** (`layer record extent_offset + extent_length; sub-record extent_offset +
  extent_length`, governing `[R-ENC-04]`); field domain > 2^63−1 → **L1**.

Now partition the value space of the pair:
| slot | rule bites? | registered by |
|---|---|---|
| (0, 0) | no — "means no extent" | nothing (correct) |
| (0, L≠0) | yes, "either half zero"; also "extent_offset < 16" | L15 (offset instance). NOT L16 after the repair. |
| (1..15, 0) | yes, "either half zero"; also "< 16" | L15 (length instance) — **and arguably L16, see §1.7** |
| (1..15, L≠0) | yes, "< 16" | L16 |
| (≥16, 0) | yes, "either half zero" | L15 |
| (≥16, L≠0) | not on this ground | — |

Values of extent_offset: 0 is registered (by L15) exactly once; 1-15 are registered by L16;
16 and above are not registered on this ground, correctly. **No value falls out of the
register and, at the offset-0 end, none is registered twice any more.** Before the repair,
`extent_offset < 16` plus "nonzero extent slot" made a (0, L≠0) slot an instance of both L15
and L16, and §21.1's specialization clause does not name L15/L16 as such a pair:

> Some rows are strict specializations of others — F1 of F6 and of F8, F35 of F36, L24 of
> L25 — and a file exhibiting a specialization is recorded against the narrower row

So the repair's direction is right, and the low bound of 1 is the right low bound.

### 1.5 Siblings — do they agree, and where they differ, which is right?

grep output for the front-block bound family (`grep -n "< 16\|≥ 16\|less than 16\|below 16"`):

```
747:| 24 | 8 | u64 | dir_offset | structural | ≥ 16 |
775:a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset +
930:extent_offset < 16, an extent extending past F − 64, or an
2058:| offset < 16 (non-sentinel) | *structural*: reject-tile — the front block is never payload |
3442:| F9 | Trailer dir_offset is less than 16, pointing the directory into or before the front signature block | ...
3542:| T8 | A non-sentinel tile-index entry has offset < 16, addressing bytes of the front signature block | ...
4148:| Directory minimums | dir_offset ≥ 16, dir_length ≥ 4 | §6.2, §5.1 |
```

- **F31** (line 3464) is the file-scope twin and currently reads identically in both the
  changed respects: "A non-layer top-level record's nonzero extent slot has extent_offset in
  1-15, placing the extent inside the front signature block". So after the repair L16 and F31
  agree in form and bound. (F31 was not in my charter; I make no claim about when it acquired
  that wording, only that the two now match.)
- **F9** (dir_offset) and **T8** (tile-index entry) keep "< 16", i.e. they include 0.
  Is that a disagreement? No — it is principled, and I checked why:
  - dir_offset has no zero-sentinel and no companion "half zero" row; §6.2's table (line 747)
    states its domain as `≥ 16`, so 0 must be inside F9.
  - A tile-index entry's absence sentinel is all-ones (T6/T7), not zero, and length = 0 has its
    own row (T10). §15.3's outcome table (line 2058) states the bound as `offset < 16
    (non-sentinel)`. So offset 0 with a nonzero length genuinely claims byte 0 and must be
    inside T8.
  Only *record extent slots* use 0 as the "no extent" sentinel and carry a separate half-zero
  row (F30/L15), which is exactly why F31/L16 start at 1 and F9/T8 start at 0. The family is
  consistent once the reason is stated.
- **L15** and **L17** use the same "A layer record's or sub-record's ..." subject as L16, so the
  form matches its immediate neighbours.

### 1.6 Condition cell against Instances cell

Condition after repair states one predicate over two containers ("A layer record's or
sub-record's"). Instances: `layer record extent slot; sub-record extent slot` — two, one per
container, identical to L17's cell. §21.1: "An instance names a field the condition ranges
over, a container it can occur in, one of several alternatives the condition text states".
The predicate has no alternatives and the range 1-15 is a value range over one field, not a
set of alternatives (§21.1's "a field tested only for being nonzero — an *A ≠ 0* ... is a
value test and not a comparison of two quantities at all" is the nearest analogue). Two
instances is right, and the repair did not change the count. Every instance the cell lists is
a case the condition admits; every container the condition names is instanced. **Match.**

Mechanical cross-check that neither hunk disturbed the register arithmetic (python3 over
spec/tarn.md only):

```
21.2 rows 36 instances 58
21.3 rows 49 instances 116
21.4 rows 26 instances 55
21.5 rows 10 instances 48
TOTAL rows 121 instances 277
```
Stated counts: §21.2 "36 conditions" (3416), §21.3 "49 conditions" (3474), §21.4 "26
conditions" (3531), §21.5 "10 conditions" (3581), §21.8 "121 conditions over 277 instances".
All four subsection counts and both §21.8 totals reconcile exactly. Row-level: L15=4, L16=2,
L17=2, F30=2, F31=1, F32=1, T8=1, R7=6.

### 1.7 Check 6 — what the repair left open in this structure

Structure governed: **the extent slot**, a two-field group (extent_offset u64,
extent_length u64) occurring on a layer record and on each sub-record. Every quantity it
carries and the rule that fixes it:

| quantity | fixed by |
|---|---|
| extent_offset domain (≤ 2^63−1) | L1 (`[R-ENC-03]`) |
| extent_length domain (≤ 2^63−1) | L1 |
| offset+length sum domain | L2 (`[R-ENC-04]`) |
| both halves zero | defined as "no extent" — no rule bites |
| exactly one half zero | L15 |
| offset lower bound | **L16 (this repair)** |
| offset+length upper bound (F − 64) | L17 |
| overlap with another structure | L18 (intra-layer), F33 (cross-scope) |
| length ≥ 5 for a user-metadata sub-record | L11 |
| length = the index formula under index_encoding 1 | L22 |

Nothing in the slot is left ungoverned, so the "one quantity pinned, its sibling free" shape
does not appear here. But one thing *is* left open, and it is the mirror image of the defect
just repaired:

The subject is "a **nonzero extent slot**". That phrase occurs exactly twice in the document
(`grep -n "nonzero extent slot"` → 3464 (F31), 3493 (L16)) and is nowhere defined. The
register's own idiom fixes it: **L22**, four rows below, writes

> including slot (0,0) with entry_count > 0, or **a nonzero slot** with entry_count = 0

where "a nonzero slot" plainly means "a slot other than (0,0)", not "a slot with both halves
nonzero". `[R-CNT-13]` itself uses the same contrast ("(0, 0) means no extent. Any other
combination ..."). Read that way, L16 admits `(5, 0)`: it is a slot other than (0,0), and its
extent_offset is in 1-15. That slot is *also* L15's ("exactly one of extent_offset and
extent_length zero", instance "layer record extent_length"). So the repair removed the
double registration at the offset-0 end and left the identical double registration at the
length-0 end. §21.1 gives no rule for which row such a file is recorded against, because
neither row is a strict specialization of the other and the pair is not in §21.1's list.

Honest counterweights, which is why I report this at low severity: (i) the row's trailing
gloss ("placing the extent inside the front signature block") arguably excludes a zero-length
slot, since a zero-length slot places no extent anywhere — but the gloss is a consequence
clause, not the predicate, and it is the very clause I fault in A-01; (ii) §15.3's entry-state
table (lines 2054-2064) shows the document tolerating overlapping structural predicates
elsewhere (`length = 0 (non-sentinel)` and `offset < 16 (non-sentinel)` both catch an entry
`(5, 0)`) — though that is an outcome table, not the corpus register with its one-file-per-
instance arithmetic. The clean fix is one phrase: "a slot with both halves nonzero", or
"an extent slot with extent_length ≠ 0 has extent_offset in 1-15". → **finding A-02**.

### 1.8 Check 5 — exhaustive/complete claims in the repaired text

Words promising completeness in the new cell: "in 1-15" (a closed range — falsified above? no:
derived correct), "placing the extent inside the front signature block" (a claim about where
the extent lies — see below), "A layer record's or sub-record's" (a closed list of two
containers — §7.4 gives layer records and their sub-records; §21.3 is layer scope; correct).

The gloss does not survive falsification. The repair replaced "**pointing into** the front
signature block" with "**placing the extent inside** the front signature block". A slot
`(15, 84)` — the canonical shape a corpus builder would use for L16's "layer record extent
slot" instance, since a 4-entry index region is 84 bytes (§7.4's arithmetic at line 1098) —
has its extent occupying [15, 99), which is not *inside* a 16-byte block. The extent begins
in the block; it is not placed in it. The rest of the family says exactly that and does not
overreach: F9 "**pointing** the directory **into or before** the front signature block"; T8
"**addressing bytes of** the front signature block"; §15.3 "the front block is never payload".
The pre-repair wording "pointing into" was true of every case the row registers; the new
wording is true only when extent_offset + extent_length ≤ 16. F31 carries the same wording, so
the sweep, if made, is two cells. → **finding A-01**.

### 1.9 Check 4 — contradictions in the passage, including untouched text

I looked specifically for a carve-out the narrowing now collides with.

- **F33** (line 3466) is the one carve-out that names L16 by label:
  > a claimant reaching the front signature block or the live trailer is instead caught by the
  > bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier
  Does narrowing L16 to 1-15 leave a front-block claimant that F33 hands to L16 and L16 no
  longer catches? The candidate is a layer slot `(0, L≠0)`. It does not survive as a claimant:
  `[R-CNT-13]` makes offset 0 the *no-extent* sentinel, so `(0, L)` is a broken slot rather
  than a claim on bytes [0, L). Nothing in F33's list is orphaned by the repair; if anything
  the repair is what makes F33's pairing (bounds rows, not half-zero rows) accurate. **No
  contradiction.**
- **L15** immediately above: complementary, not contradictory, except for the `(1..15, 0)`
  overlap recorded as A-02.
- **L17** immediately below: upper bound, disjoint from the lower bound. Uses the same subject
  and the same two instances. **Consistent.**
- **L18 / L46 / L47** cite `[R-CNT-13]` for other clauses (overlap, flags). Untouched by the
  bound. **Consistent.**
- §19.3's layer-access obligation ("the slot's validity rules (`[R-CNT-13]`)") and §18.1's
  "a malformed extent slot on such a record, (0, 0) included, is a validity error at the
  record's containing scope (`[R-CNT-13]`, `[R-CNT-25]`)" — both unaffected by moving the
  bound from 0 to 1, because the offset-0 case remains a validity error under L15/`[R-CNT-13]`.
  **No MUST elsewhere in the passage is now violable.**

### 1.10 Check 3 — does the repair sit in normative text?

The rule's distinctive words, grepped for short non-wrapping fragments:
`grep -n "signature block"` → 335, 454, 560, 621, 624, 693, 778, 799, 1116, 1125, 1183, 1341,
2705, 2755, 2925, 3434, 3439, 3442, 3464, 3466, 3493, 3542, 4144, 4331, 4456.
`grep -n "extent slot"` → 603, 622, 928, 935, 944, 1002, 1098, 1335, 2103, 2432, 2593, 2742,
2795, 2993, 3107, 3123, 3153, 3174, 3258, 3305, 3454, 3463, 3464, 3487, 3492, 3493, 3494.

The normative statement of the bound is §7.2 line 930 (`[R-CNT-13]`), plain body text — I
verified with `awk` that lines 928-953 carry no ">" prefix. The repaired cell is a register
row, which §21.1 declares a restatement of that rule ("where a row and the rule it cites
diverge, **the rule governs**"). Neither the old nor the new text sits in a blockquote, and
the normative statement was not the thing edited — correctly, since the rule's "< 16" is right
for the rule (it ranges over *all* non-(0,0) combinations, where the offset-0 case is a
validity error twice over) and only the register needs the partition. **Passes.**

### 1.11 Check 1 — tense and quantifier

Repair: "**A** layer record's or sub-record's nonzero extent slot **has** extent_offset in
1-15". Rule: "**Any other combination** with ... an extent_offset < 16 ... **is** a validity
error". Both present-tense predicates on the file's stored bytes; neither is generation-scoped
(the generation-scoped half of `[R-CNT-13]` is the *overlap* clause, "within the live committed
state", which L18/F33 restate, not L16). Indefinite singular "a slot" against "any
combination" — same set, existential over slots. The repair narrows the *value* range but not
the *set quantified over*, and the excluded value is carried by L15's restatement of the
adjacent disjunct. **Match.**

### 1.12 Check 2 — citations

- `[R-CNT-13]` (Governing rule cell): opened at §7.2 lines 928-953. It states the extent-slot
  validity disjuncts including `extent_offset < 16`, and assigns the scope: "the layer for a
  layer record and for sub-records". Both the row's condition and its reject-layer placement in
  §21.3 are what the rule says. **PASS.**
- Detector/Detected cells ("reader | layer access"): §19.3 lines 2792-2797 make full validation
  of the layer record — "extent slot and inline payload both: the slot's validity rules
  (`[R-CNT-13]`)" — precede a reader's first access to a layer. **PASS** (unchanged by the repair).
- No section number appears in the repaired text. "front signature block" is defined at line
  335 / §6.1 as "the constant 16 bytes at offset 0", which is what makes 16 the boundary.
  **PASS.**

### 1.13 Check 7 — analogy

The repaired cell argues by no analogy: no "exactly as", "the same way", "as X is",
"following X", "likewise", "transposed from" appears in it. The only pointer at another rule
is the Governing rule cell, handled under checks 1 and 2. Verb comparison recorded there:
row "**has** extent_offset in 1-15" against rule "**is** a validity error" over "any other
combination **with** ... an extent_offset < 16". Same subject set (non-(0,0) slots), narrower
value bound, with the excluded value registered by the neighbouring row. **Nothing for
check 7 to fail on.**

---

## 2. HUNK 2 — §21.5 row R7, Condition cell (spec line 3591)

### 2.1 The diff

```
- | R7 | A decoded user-metadata document is not well-formed JSON, or its top-level value is not an object | not well-formed JSON, top-level document; ...; leading U+FEFF, top-level document; leading U+FEFF, layer sub-record document | ...
+ | R7 | A decoded user-metadata document is not well-formed JSON, its top-level value is not an object, or it carries a leading U+FEFF byte-order mark | (instances unchanged) | reader | extent use | [R-MTA-04] (R-CNT-25) |
```

### 2.2 The rule the repair adopts, in my words

A user-metadata document's decoded bytes must (i) parse as an RFC 8259 JSON text, (ii) have an
object as the top-level value, and (iii) not begin with U+FEFF. Any of the three failing makes
the record ignore-record. In implementation terms: a reader that strips or tolerates a leading
BOM before parsing — which RFC 8259 permits a parser to do — is wrong here; it must treat the
BOM as making the document unreadable, and the register now says so in the cell an implementer
reads as the statement of the condition, instead of only in the corpus column.

### 2.3 The governing rule, opened (§18.2, lines 2537-2571, normative body text — verified by
`awk` that lines 2537-2571 carry no ">" prefix; the nearest blockquote ends at line 2535)

> The decoded document is a JSON text as defined by RFC 8259, encoded
> in UTF-8. Four restrictions apply, and a document violating any of
> them is unreadable — ignore-record, with the report `[R-CNT-25]`
> asks for:
>
> - **A JSON object, unmarked.** The top-level value is an object,
>   and the encoding carries no byte-order mark: a leading U+FEFF
>   makes the document unreadable.
> ... (three further bullets) ...
>
> `[R-MTA-04]`

Condition the rule creates: three independent grounds of unreadability live in R7's territory
— failing RFC 8259 well-formedness (from the lead sentence), a non-object top-level value, and
a leading U+FEFF (both from restriction 1). The repaired cell expresses exactly those three:
no wider (it adds nothing the bullet does not say — e.g. it does not reach trailing BOMs,
interior U+FEFF, or `﻿` escapes, none of which the rule bars), no narrower (all three
grounds present). **Exact.**

### 2.4 Condition cell against Instances cell

§21.1: "a condition applying to two alternatives in two containers has four". R7 states
**three** alternatives over **two** containers (top-level document, layer sub-record document)
= six. The Instances cell lists exactly six, in the order the condition now states them:

```
not well-formed JSON, top-level document; not well-formed JSON, layer sub-record document;
top-level value not an object, top-level document; top-level value not an object, layer sub-record document;
leading U+FEFF, top-level document; leading U+FEFF, layer sub-record document
```

This *is* the defect the repair fixes: before it, the cell instanced an alternative the
condition text did not state, so the row's corpus built two files for a condition the row did
not register. Every instance is now a case the condition admits and every alternative is
instanced, in both directions. **Match.**

Direction check — should the repair instead have deleted the two U+FEFF instances? No, and the
arithmetic proves it: §21.8 states "121 conditions over 277 instances", and my mechanical count
over §21.2-§21.5 returns exactly 121 / 277 with R7 at 6. Removing the two instances would have
left §21.8 stating 277 against an actual 275. The additive repair is the one the rest of the
document already expects, and it is also the one `[R-MTA-04]` requires, since the BOM ground is
normative there regardless of what the register does.

### 2.5 Check 6 — what the repair left open in this structure

Structure governed: **the enumeration of decoded-document rules in §18.2** (the lead sentence
plus four bullets), whose members §21.5 must register one-for-one. Every member, and the row
that fixes it:

| §18.2 member | register row |
|---|---|
| "a JSON text as defined by RFC 8259" | R7 limb 1 |
| "encoded in UTF-8" | R5 (ill-formed source bytes in a key or string value) |
| restriction 1a: top-level value is an object | R7 limb 2 |
| restriction 1b: no leading U+FEFF | **R7 limb 3 (this repair)** |
| restriction 2: finite numbers, incl. bare `NaN`/`Infinity`/`-Infinity` | R8 |
| restriction 3: no duplicate keys, identity over decoded strings | R9 |
| restriction 4a: well-formed UTF-8 after escape resolution (unpaired surrogate) | R5 |
| restriction 4b: keys satisfy §4.6 — non-empty | R6 |
| restriction 4c: keys ≤ 255 bytes | R10 |
| restriction 4d: keys free of U+0000–U+001F | R6 |
| `[R-MTA-05]` member ordering (not an unreadability ground) | F27 / L48, verifier |
| `[R-ENC-13]` raw-byte key comparison | a definition, no violation to register |

I opened §4.6 to confirm the "§4.6's name rules" parenthetical is complete: §4.6 states
exactly three name constraints — "non-empty; at most 255 bytes of UTF-8 ...; free of code
points in the range U+0000 through U+001F" — matching the bullet's gloss, and all three are
registered (R6, R6, R10). Restriction 1 has exactly two limbs and after the repair both are in
R7. **No member of this structure is left unconstrained; the "one quantity pinned, its sibling
free" shape does not appear.** The mirror of A-02 — a second unregistered limb hiding beside
the repaired one — is what I was hunting here, and there is none.

### 2.6 Check 5 — exhaustive claims

The new limb adds no completeness word: no "every", "never", "always", "only", "the two", no
count, no closed list. "a leading U+FEFF byte-order mark" is a singular existential over one
code point at one position, and it is exactly the rule's own words ("a leading U+FEFF"). The
row does not claim to enumerate the document rules, so it carries no completeness burden
beyond §21.1's register-wide one, which §2.5's table shows is met. **Nothing to falsify.**

### 2.7 Check 4 — contradictions in the passage, including untouched text

- **R3** (line 3588): "A user-metadata document's stored bytes fail to decode under its
  declared assigned encoding". Could a BOM-led document be R3's rather than R7's, making the
  two rows collide? No: R4's own text fixes R3's sense — "unlike R3, a constraint of this row
  is broken by what the frame declares rather than by whether the bytes decode" — so R3 is the
  encoding-level decode (verbatim/zstd), which a BOM does not disturb. The BOM is a JSON-text
  fact, R7's. **No collision.**
- **Redundancy with R7's own limb 1**: a leading U+FEFF already makes the text fall outside
  RFC 8259's `JSON-text = ws value ws` grammar, so limb 3 is arguably a special case of limb 1.
  This is deliberate, not a contradiction: §18.2 spells the BOM out precisely because RFC 8259
  §8.1 lets a parser ignore one, so a reader that only asks "did my parser accept it?"
  establishes nothing. Within a single row, overlapping limbs cost nothing — the six instances
  are six distinguishable files (§21.1's test), and no *other* row is competing for the case.
  I therefore do not raise here what I raise for L16 in A-02: there the overlap is *between*
  two rows, which §21.1's specialization clause has to arbitrate and cannot.
- **§21.5 preamble** (lines 3564-3580): "every way its document can be unreadable takes this
  outcome, whatever the containing scope — as a violation in the rows below, except at an
  experimental-range encoding ... and except where a reader or verifier declines the decode on
  the size bound or on the frame's declared window". The BOM ground is neither exception; it
  is a violation with ignore-record outcome, which is what R7's row carries. **Consistent.**
- **§21.6** (whole table read): no entry declares a BOM, or anything about document content,
  a non-violation. The two entries touching user metadata are the experimental-range encoding
  and the unrecognized `tarn.` key / misplaced standardized key — neither is a carve-out the
  new limb collides with. **No "is not such a case" sentence bites.**
- **§4.1 line 376**, "There is no byte-order mark and no big-endian variant": this is about
  multi-byte numeric fields under `[R-ENC-02]`, a different subject from a UTF-8 BOM in a JSON
  text. Not a contradiction; not a restatement that needed sweeping either.

### 2.8 Check 3 — does the repair sit in normative text?

`grep -n "FEFF\|byte-order mark\|BOM"` returns exactly three hits: 376 (§4.1, endianness),
**2543 (§18.2, restriction 1)**, 3591 (the repaired R7 row). `awk` over lines 2525-2560 shows
line 2526-2535 are a ">" Note and lines 2537-2569 are plain body text, with `[R-MTA-04]`
closing the enumeration at line 2571. So the BOM rule's normative home is body text, it says
what R7 now says, and the repair did not put the rule in a blockquote or edit a blockquote
while leaving a normative statement standing. **Passes.** And there is no fourth site — no
unswept restatement of the BOM rule anywhere in the document.

### 2.9 Check 1 — tense and quantifier

Repair: "**A** decoded user-metadata document ... **carries** a leading U+FEFF byte-order
mark". Rule: "the encoding **carries** no byte-order mark: **a leading U+FEFF** makes the
document unreadable". Same verb, same article, same position qualifier. Generation: neither
speaks of generations; a user-metadata document is read out of a live record's extent, and the
row's Detected cell ("extent use") is §19.2's tier for exactly that. Set ranged over: the rule
is a restriction on "the decoded document", the row's subject is "a decoded user-metadata
document" — the same object, and the row's two containers (file-scope record, layer sub-record)
are §18.1's two: "A file MAY carry one user-metadata document at file scope, and each layer MAY
carry one of its own". The rule attaches to the *decoded* bytes (post-decompression), and the
row says "decoded"; the BOM is therefore tested after encoding-2 decompression, not on the
extent's stored bytes. **Match on tense, verb, and quantifier.**

One thing I checked and let go: the rule says "the **encoding** carries no byte-order mark"
while the row says the **document** carries it. The rule's own gloss in the same sentence ("a
leading U+FEFF makes the document unreadable") speaks of the document, and U+FEFF is a code
point rather than an octet, so both halves of the rule already mean the decoded text. No
divergence to report.

### 2.10 Check 2 — citations

- `[R-MTA-04]` (Governing rule cell): opened at §18.2 lines 2537-2571. It carries the RFC 8259
  well-formedness requirement, the top-level-object requirement, and the BOM prohibition —
  all three of R7's limbs, and its outcome ("unreadable — ignore-record") is §21.5's outcome.
  **PASS.**
- `(R-CNT-25)` (parenthetical): §18.1 lines 2427-2433 and §7.1 line 888 establish the
  quarantine — "the outcome of every failure to read its **document** is ignore-record whatever
  the scope, because the document is **quarantined** (`[R-CNT-25]`)". That is what puts an R7
  failure in §21.5 rather than at the containing scope, and it is cited without brackets as
  §21.1 prescribes for a rule the condition reads rather than the one that governs it.
  **PASS.**
- No section number appears in the repaired text. RFC 8259 is referenced only through
  "well-formed JSON", which the reference list at line 4256 ties to §18.2. **PASS.**

### 2.11 Check 7 — analogy

The repaired cell contains no "exactly as", "the same way", "as X is", "following X",
"likewise", "for the same reason", "transposed from". It justifies itself by nothing but its
Governing rule cell. (Its neighbours R3 and R4 do argue by analogy — R4's "the tile rule of
`[R-COD-06]` transposed to the quantity a document does have" — but neither is in this repair
and I make no claim about them.) Verb comparison against the warrant, recorded as check 7 asks:
row "**carries** a leading U+FEFF byte-order mark" against rule "the encoding **carries** no
byte-order mark". Identical verb, identical set (the decoded document's leading position).
**Passes.**

### 2.12 Overshoot / undershoot / new ambiguity for hunk 2

- Overshoot: none. The limb added is one of the two the bullet states; it did not widen R7 to
  cover, say, an interior U+FEFF or a `﻿` escape, neither of which §18.2 bars.
- Undershoot: none. Both limbs of restriction 1 are now in the cell.
- New ambiguity: the pronoun in "or **it** carries a leading U+FEFF" has "its top-level value"
  as its nearest antecedent and "a decoded user-metadata document" as its subject antecedent.
  I considered raising this and decided not to: the Instances cell reads "leading U+FEFF,
  top-level document" / "... layer sub-record document", which fixes the referent as the
  document, and no implementation could act on the other reading (a JSON value has no leading
  BOM). Recording the consideration rather than the finding, so the decision is auditable.

---

## 3. Verdict

Hunk 2 (R7): clean on all seven checks. The repair fixes a genuine condition/instances
mismatch, in the right direction, with the arithmetic in §21.8 confirming that direction; its
citations resolve; its normative home is body text and there is no second site to sweep; and
the structure it governs — §18.2's enumeration — is fully registered with nothing left open.

Hunk 1 (L16): the substance of the repair is right. The bound 1-15 is what the register needs,
it is derivable from `[R-CNT-13]` plus L15, it matches F31, and the F9/T8 divergence is
principled rather than an inconsistency. Two residues:

- **A-01** — the repair also swapped "pointing into" for "placing the extent inside", a gloss
  that is false for every extent that begins in 1-15 and runs past byte 16, which is most of
  them, including the corpus instance the row calls for.
- **A-02** — the repair removed the L15/L16 double registration at the offset-0 end and left
  the identical one at the length-0 end, because "nonzero extent slot" is undefined and the
  register's own use of "nonzero slot" (L22) means "other than (0,0)".

Neither is byte-level: under every reading of both cells the disputed file violates
`[R-CNT-13]`, so `[R-CNF-05]` bars a conforming writer from emitting it and every conforming
reader rejects the layer at layer access. What moves is which register row a file is recorded
against and what the corpus builds — not bytes on disk and not an accept/reject verdict.
