# Repair audit — hunk-01 (§20.5 reserved-range parenthetical) and hunk-02 (§21.2 preamble)

Working transcript. Written for someone re-running the work, not as a summary.

## 0. Disclosure — what I read and ran

Read:
- `/private/tmp/.../r24audit-b/hunk-01.diff` (whole file, 34 lines)
- `/private/tmp/.../r24audit-b/hunk-02.diff` (whole file, 43 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these ranges:
  lines 134–232 (§2.3 conformance classes), 555–625 (§5.1 anatomy, `[R-CNT-01]`,
  `[R-CNT-27]`), 691–830 (§6.1–§6.4), 1370–1460 (§10.1–§10.4), 2691–2760
  (§19.1 open algorithm, §19.2 opening), 3192–3320 (§20.5 compaction, whole
  subsection), 3319–3460 (§21.1, §21.2 preamble + whole F table), 3460–3580
  (§21.3 L table, §21.4 T table, §21.5 preamble + R table), 3576–3710 (§21.6,
  §21.7, §21.8, §21.9 opening), 3775–3800 (§21.9 `[R-ERR-05]` limits prose).
- Head-line listing of every `##`/`###`/`####` heading in the spec.

Ran:
- `wc -l` on the spec.
- `grep -n` on the spec for `R-CNT-27`, `10.2|10.1`.
- Built a whitespace-normalised single-line copy of the spec at
  `.../scratchpad/flat.txt` with `tr '\n' ' ' | tr -s ' '`, because the document
  is hard-wrapped and line-oriented grep misses wrapped phrases. All phrase
  searches below were run against `flat.txt` with
  `grep -o -E '.{N}<fragment>.{N}'`. Fragments searched: `128 bytes`,
  `128-byte`, `\bF5\b`, `geometry`, `capability grounds`, `version gate`,
  `fixed across`, `R-CNT-24`.

Did NOT read: `full.diff`, hunk-03/hunk-04, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, the web. Did not list the hunk directory.

**Unrequested context that appeared before I began.** My runtime placed a
project-instruction pointer and an index of the maintainer's private memory
notes in my context (topic titles only, plus one date). None of it is part of
the specification and I drew no conclusion from it; I name its appearance here
as required and do not repeat its contents. Every conclusion below is traceable
to a spec line range or a grep output reproduced in this file.

---

# HUNK 1 — §20.5, line ~3213

## 1.1 The count, done first, from §10.2's table, before reading either side

§10.2's table (spec lines 1397–1406). Rows, verbatim first column:

| # | Space |
|---|---|
| 1 | record type (§7.3) |
| 2 | channel layout (§14.1) |
| 3 | linearization (§11.4) |
| 4 | sample type (§12.2) |
| 5 | codec (§17.2) |
| 6 | filter (§17.3) |
| 7 | index encoding (§7.4, §15.1) |
| 8 | metadata encoding (§18.2) |

**Eight tabulated spaces.** Minus record type = **seven others**.

Trap checked: §10.2's prose immediately below the table says "Two spaces carry
no experimental range: channel layout … and **the trailer's flag lanes**, which
§6.3 partitions instead." That sentence calls the flag lanes a *space*, but the
flag lanes are **not a row of the table**. The repair's wording is "the other
seven spaces §10.2 **tabulates**" — scoped to the table, not to §10.2's prose.
That scoping is correct and is the difference between 7 and 8. Noted as a
deliberate, correct choice, not an accident.

## 1.2 The rule the repair adopts

*In my own words:* for each numeric identifier space §10.2's table lists other
than the record-type space, this document contains exactly one error-register
row that makes a reserved-range value in that space a violation; the record-type
space instead has two such rows (one per containing scope). Nothing about an
implementation's behaviour changes — this is a descriptive parenthetical inside
a normative paragraph, restating rows stated elsewhere.

## 1.3 Label-to-space match, one for one

Read from §21.3 (lines 3490–3505) and §21.5 (line 3560):

- L31 — "Layer record's index_encoding is a value other than 1 — 0, reserved
  2–0x7F, or experimental ≥ 0x80" → **index encoding**
- L33 — "Layer record's linearization is a value other than 1 — 0, reserved 2–3,
  reserved 4–0x7FFF, or experimental ≥ 0x8000" → **linearization**
- L34 — "A channel entry's type is outside 1 … 13 — 0, reserved 14–19, reserved
  20–0x7FFF, or experimental ≥ 0x8000" → **sample type**
- L36 — "Layer record's layout is a value other than 1 or 2 — 0 or reserved
  3–255" → **channel layout**
- L43 — "Layer record's codec is a value other than 1 … 4 — 0, reserved
  5–0x7FFF, or experimental ≥ 0x8000" → **codec**
- L45 — "Layer record's filter is a value other than 1 or 2 — 0, reserved
  3–0x7FFF, or experimental ≥ 0x8000" → **filter**
- R1 — "A user-metadata record declares a document encoding of 0, or a
  reserved-range value (3-0x7F)" → **metadata encoding**

Seven labels, seven spaces, bijective. **Every one of the seven covers its
space's *reserved* range explicitly**, which is what the sentence claims ("values
this text still registers as reserved-range violations"). L36 has no
experimental clause, correctly, because §10.2 gives channel layout no
experimental range.

Uniqueness check (is it really *one* row per space?). I walked the full F, L, T
and R tables looking for a second value-set row per space:
- index encoding: only L31. L22 mentions `index_encoding 1` but its subject is
  extent_length, not the value set.
- linearization: only L33.
- sample type: only L34. L30 (fill length prefix vs element size) and L35 (bool
  fill byte) are not value-set rows.
- codec: only L43. L44 is codec 4's decoded-size cap, not a value-set row.
- filter: only L45.
- channel layout: only L36.
- metadata encoding: only R1. R3's clause "encoding 0 and a reserved value are
  unassigned too and R1 registers both" points back to R1, it does not add a row.
Result: **one row each. Count and enumeration both hold.**

Record type: F36 (top-level) and L25 (layer sub-record), as the sentence says.
F35 and L24 exist too but §21.1 names them explicitly as strict specializations
("F35 of F36, L24 of L25") for the MU = 1 case; in the compaction context a
MU = 1 record the compactor does not implement forces refusal under `[R-WRT-06]`
anyway, so F36/L25 are the right two to name. Not a defect.

## 1.4 The two-group arithmetic

The sentence divides §10.1's four extension vehicles into two groups:
- §10.1 (lines 1374–1382): 1 new record types, 2 new values in reserved ranges,
  3 new ignore-lane flag bits, 4 new standardized user-metadata keys.
- "the two … §21.6 makes conforming" = the carried ignore-lane bit and the
  unrecognized `tarn.` key. Verified against §21.6's table: row "An ignore-lane
  flag bit (16–31) is set | Ignored; **the file is conforming**" and row "A
  user-metadata document carries an unrecognized `tarn.`-prefixed key |
  **Conforming**". Vehicles 3 and 4. ✔
- "the other two" = vehicles 1 and 2. Every member lands in exactly one group,
  2 + 2 = 4. ✔
- Vehicle 1 (new record types) and the record-type row of §10.2's table are the
  same subject matter, so F36/L25 discharge both; the remaining seven table rows
  discharge the rest of vehicle 2. No space is double-counted and none is
  omitted.

Deliberate trap I checked and cleared: §21.6 also makes conforming "A record
type this specification has not assigned, from the **experimental** range
(≥ 0x8000) … carries MU = 0". Does that make *three* vehicles conforming? No —
the sentence's premise is "a feature **a later minor defines**", and a later
minor registers out of the *reserved* range (§10.4), never the experimental one,
which §10.3 confines to private use and bars from released software. So the
experimental §21.6 row is outside the premise and the "two/two" split stands.

## 1.5 Check 2 — citations in the repaired text

- **§10.2** — opened (lines 1389–1412). Claims made of it: that it "tabulates"
  identifier spaces, and that there are seven besides record type. Both true of
  the table. **PASS.**
- Untouched citations in the same sentence, opened anyway because the repair
  changed the sentence's arithmetic: **§10.1** (four vehicles — verified, exactly
  four numbered items, closed by "Nothing else extends this format"); **§21.6**
  (two conforming rows — verified above); **§6.3** (`[R-CNT-08]` ignore-lane bits
  conforming — verified, line 812: "a set ignore-lane bit is not a
  file-conformance violation"); **§18.3** (unrecognized `tarn.` key — the §21.6
  row cites `[R-MTA-06]`; consistent); **`[R-CNT-26]`** (line 820: "a higher minor
  than needed costs readers nothing … but **misstates the file's feature floor to
  tooling**" — §20.5 calls a lower minor's understatement "the mirror of the
  overstatement `[R-CNT-26]` names"; the verbs are *misstates* / *understates*
  over the same object, "the file's feature floor to tooling". **PASS**);
  **`[R-CNT-08]`**, **`[R-LIF-01]`**, **`[R-LIF-03]`**, **`[R-WRT-06]`** — all
  outside the changed bytes, all consistent with their sentences.

## 1.6 Check 3 — does the repair sit in normative text?

The paragraph is §20.5 body prose (spec lines 3192–3236), not a `>` block, and
closes with `` `[R-WRT-06]` ``. Grepped `flat.txt` for the distinctive strings
`reserved-range violations` and `spaces §10.2` — the only hits are this
paragraph. The rows the parenthetical names are themselves normative table rows
in §21.2/§21.3/§21.5 with governing rules `[R-CNT-15]`, `[R-CNT-23]`,
`[R-GEO-05]`, `[R-TYP-03]`, `[R-SER-06]`, `[R-COD-03]`, `[R-COD-09]`,
`[R-CNT-25]`. The repair restates; it is not the sole statement of anything, and
§21.1's "where a row and the rule it cites diverge, the rule governs" backstops
it. **PASS.**

## 1.7 Check 4 — contradiction inside §20.5 (whole subsection read, 3192–3316)

Looked for: a carve-out the new breadth collides with; a MUST the new text lets
someone violate; a sentence true only under the old count.
- "Given a conforming input the output is a conforming file" and "MUST NOT emit a
  file carrying a violation it has detected" — consistent with, indeed the point
  of, the parenthetical: a *conforming* input cannot carry a reserved-range value
  in any of the eight spaces, which is exactly why only two of the four vehicles
  are live for the `version_minor` SHOULD.
- The `>` Example block and the closing `>` Note carry no count and no space
  list; nothing there was written to be true only under "each identifier space".
- No sentence anywhere in §20.5 repeats the count. Nothing to sweep.
**No contradiction found.**

## 1.8 Check 5 — exhaustive claims in the repaired text

Words promising completeness: "each of the **other seven** spaces", the closed
parenthetical list of seven labels, and "**one** row for each".
- "seven" — falsification attempt: count §10.2's table rows = 8; minus record
  type = 7. Cannot falsify.
- the closed list — falsification attempt: find a space with no listed row, or a
  listed row belonging to no space, or two labels for one space. All three
  attempts fail (§1.3 above).
- "one row" — falsification attempt: find a second reserved-range row for any of
  the seven. Fails (§1.3 uniqueness walk).
**All exhaustive claims carry.**

## 1.9 Check 6 — what is left unconstrained in this structure?

Structure the repair governs: §10.2's partition of every numeric identifier
space into assigned / reserved / experimental, and the register rows policing
each. Full member list and its policing rule:

| Space | value 0 | reserved range | experimental range |
|---|---|---|---|
| record type | F24 / L13 | F35, F36 / L24, L25 | §21.6 (MU=0 conforming); §21.6 closing (top-level MU=1 refused, file still conforming) |
| channel layout | L36 | L36 | n/a — no experimental range |
| linearization | L33 | L33 | L33 |
| sample type | L34 | L34 | L34 |
| codec | L43 | L43 | L43 |
| filter | L45 | L45 | L45 |
| index encoding | L31 | L31 | L31 |
| metadata encoding | R1 | R1 | §21.6 (`[R-MTA-10]`, conforming) |

Every value in every space is reached by some rule. The sibling quantity I went
looking for — a space whose reserved range is policed but whose value 0 or
experimental range is not — does not exist here; each of the seven rows is
written as "a value other than X — 0, reserved …, experimental …", covering the
whole domain in one row. **Nothing left unconstrained.**

## 1.10 Check 7 — analogy

The changed bytes contain no analogy connective ("exactly as", "the same way",
"as X is", "following", "likewise", "the model is", "transposed from", "for the
same reason"). Grepped `flat.txt` around the paragraph for each; the only one in
the sentence is "**the mirror of** the overstatement `[R-CNT-26]` names", which
is untouched context. Compared anyway, verb for verb:
- repair-side governing verb: a lower minor "**understates** the file's feature
  floor to tooling"
- `[R-CNT-26]`'s governing verb: a higher minor "**misstates** the file's feature
  floor to tooling"
Same object, same range (one file's version_minor against the features present
in it), opposite direction — which is what "mirror" asserts. **Analogy holds.**

## 1.11 Hunk 1 verdict

No finding. The "-" side was wrong: "one row for each identifier space §10.2
tabulates" quantifies over all eight tabulated spaces while listing seven labels,
so the quantifier and the list disagreed by one. The "+" side fixes exactly that
and nothing more. Count verified independently before reading either side.

---

# HUNK 2 — §21.2 preamble, line ~3391

## 2.1 The rule the repair adopts

*In my own words:* of §21.2's 36 file-scope rows, exactly four can be recorded
against a file whose trailer declares a format major other than 1 — F1, F6, F8,
F14 — and the ground is that each of their subjects is a field `[R-CNT-24]`
fixes in every format major version. F18 is set aside as outside the premise.
`[R-CNT-27]`'s 128-byte floor (F5) is **no longer** among the rows that reach
such a file; it now falls under the opening premise's "rows whose subject is that
file's *geometry* do not reach it".

## 2.2 What the removed text asserted

Two separable claims:
1. **Classification:** F5 reaches a file declaring a foreign major.
2. **Ground:** "§6.2's order does not name [the floor] because it precedes that
   order: a file shorter than 128 bytes has no trailer to read a magic, a CRC or
   a version from, so the floor is established before any field the gate consults
   exists."

Claim 2's gloss is **false on the document's own text**. §6.2 (line 736): "The
trailer occupies the final 64 bytes of the file." A file of 64 ≤ F < 128 has a
final 64 bytes and therefore has a magic, a CRC and a `version_major` to read.
Only F < 64 lacks a trailer, and such a file declares no major at all, so it is
outside the premise anyway. So the "-" side carried a false rationale — a real
defect, and removing it is right.

Claim 1 does **not** depend on claim 2's gloss, and that is where I spent the
rest of the time.

## 2.3 Check 5 first — is "Four" exhaustive and correct?

`[R-CNT-24]` (lines 799–806), verbatim scope: "In every format major version,
permanently: the final 64 bytes of a file contain the trailer magic at F − 64,
version_major and version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
[F − 64, F − 4); and the front signature block (§6.1) is constant."

Fields fixed across every major, and the rows whose subject is one:
- trailer magic → **F8**, and **F1**'s trailer-magic instance
- trailer CRC → **F14**
- front signature block → **F6**, and **F1**'s front-block instance
- version_major → **F18**

Rows: F1, F6, F8, F14, F18. F18 is handled by name in the next sentence
("version_major = 0 declares no major at all"), leaving **four**. The count is
right and the enumeration is exhaustive: I checked every other F row's subject
against `[R-CNT-24]` and none qualifies. In particular **F15** (trailer reserved
bytes [56,60)) sits inside the "remaining 48 trailer bytes" a future major MAY
redefine, so it correctly is not among the four — even though its Governing rule
cell cites (R-CNT-24). And **F5**'s subjects are `F` (physical file size) and
`committed_file_length` (trailer offset 40, also inside the redefinable 48), so
under this ground F5 is correctly excluded.

**So the repair's new "because" clause is a sound, exhaustive ground, and it does
exclude F5.** The count 36 in the same preamble is unchanged and still right
(F1…F36).

## 2.4 Check 1 / the ordering test the charter names — and where it breaks

The paragraph's *first* ground (untouched by the repair) is an ordering claim:

> "§6.2 puts the version gate ahead of every check but the trailer magic and the
> trailer CRC, so such a file is refused on capability grounds first."

Find the rule that fixes the ordering and check MUST vs MAY:

- `[R-CNT-06]` (line 776): "A reader **MUST** validate, **in order**: the trailer
  magic; the trailer CRC; the version gate (§6.3) — only these touch fields whose
  positions are fixed across all majors (`[R-CNT-24]`) — and then, those gates
  passed, MUST validate all of the following before acting on the fields
  involved: the flag gates …". A MUST. But its ordering ranges over **the checks
  §6.2 itself states** — the trailer field gates. It does not range over "every
  check" in the document.

- `[R-CNT-27]` (line 571–575): "No conforming file is shorter than 128 bytes …
  A reader **MUST** treat a shorter file as a validity error at file scope."
  Unconditional MUST, **no ordering clause at all**, and §6.2 never names it.

- §19.1 (lines 2693–2712), the ordered open: "A conforming reader opens a file by
  these steps, **in order**: 1. **End of file.** Obtain the
  transport-authoritative file size F (`[R-CNT-10]`) … 2. **Trailer.** Fetch bytes
  [F − 64, F) and validate them in §6.2's fixed order — magic, trailer CRC,
  **version gate** …". **F is in hand at step 1; the version gate is not reached
  until step 2.**

So `[R-CNT-27]`'s input exists one whole step before the gate's input, its MUST
is unconditional, and no rule in the document places the floor check after the
gate. A conforming reader that evaluates the floor as soon as F exists — the
obvious implementation of §19.1 step 1 — rejects a 96-byte file bearing
`version_major = 5` on the floor, not on capability grounds. **That is exactly
what the deleted sentence's *conclusion* said, and §19.1 supports it even though
the deleted sentence's *gloss* did not.**

The paragraph therefore now carries two grounds that answer F5 in opposite
directions: the fixed-field ground (§2.3 above) excludes it; the ordering ground
plus §19.1 includes it. The repair silently picked one and deleted the sentence
that had recorded the other, without touching the ordering premise. → **A-01**.

## 2.5 Check 4 — contradiction inside the same paragraph, untouched text included

Read the whole §21.2 preamble plus all 36 rows (lines 3396–3450).

> "§6.2 puts the version gate ahead of **every check** but the trailer magic and
> the trailer CRC"

against, three clauses later in the same paragraph:

> "F6 with F1's front-block instance, **which `[R-CNT-04]` places before other
> processing**"

The front-block check is a check other than the trailer magic and the trailer
CRC, and it precedes not merely the gate but the magic itself (§19.1 step 1,
before step 2). The paragraph falsifies its own "every check" within four lines.
Independently, `[R-CNT-27]`'s floor is a second check §6.2's order does not name.
This sentence is untouched context — but the repair removed the paragraph's only
other acknowledgement that checks exist outside §6.2's order, and now rests F5's
exclusion on this premise, so the overclaim is load-bearing in a way it was not
a day ago. → **A-02**.

## 2.6 Check 2 — citations in and around the repaired sentence

- **`[R-CNT-24]`** — opened (lines 799–806). Claim: F8/F1-trailer, F14, F6/F1-front
  have "as their subject a field fixed across every major". Verified field by
  field in §2.3 above. **PASS.**
- **`[R-CNT-04]`** — opened (§6.1, lines 714–724). Claim: it "places [the
  front-block check] before other processing". What it actually says: "A reader
  whose open leaves bytes [0, 16) **resident** … MUST verify the full block by
  byte equality before other processing … A reader that would have to issue a
  further range request to obtain those bytes **MAY defer or omit the check**."
  The placement is a MUST **only for a resident reader**, with an express MAY
  exemption otherwise. The preamble restates it unqualified. F6's own row carries
  the qualifier ("a reader that would have to fetch them MAY defer or omit the
  check (`[R-CNT-04]`); a verifier holds no such exemption (§2.3)"), as does F1's
  row and §19.1 step 1. **FAIL on precision** (the conclusion "F6 does reach it"
  survives, because a verifier holds no exemption and the front block is constant
  in every major — but the cited rule does not say what the sentence says it
  says). → **A-03**.
- **`[R-CNF-02]` / §2.3** — opened (lines 137–156): "a file declaring another
  major is neither conforming nor nonconforming under it: a reader refuses such a
  file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a
  finding about its bytes." Supports the premise sentence. **PASS.**
- **§6.2** — opened; supports the magic-then-CRC-then-gate claim for the two
  named checks. **PASS** as to those two, **overclaimed** as to "every check"
  (A-02).
- **§21.6** — opened for the F18 sentence: closing paragraph, "version_major = 0,
  permanently invalid in every format major version (F18, `[R-CNT-07]`)". **PASS.**
- **`[R-CNT-27]`** — opened (line 571). Cited only in the *removed* text; nothing
  in the "+" text cites it. Its absence is the substance of A-01.

## 2.7 Check 3 — does the repair sit in normative text?

The §21.2 preamble is body prose, not a `>` block. It is however *explanatory*:
it assigns no MUST and creates no requirement. The rules it reasons about
(`[R-CNT-06]`, `[R-CNT-04]`, `[R-CNT-07]`, `[R-CNT-27]`, `[R-CNF-02]`) all live
in normative prose elsewhere, and §21.1 makes the rule govern over the register.
So neither the "-" nor the "+" text ever had force of its own; both are
navigational. This is why none of the three findings below is byte-level.
Grepped `flat.txt` for `capability grounds`, `fixed across`, `128-byte`,
`\bF5\b`, `128 bytes` — outputs reproduced below — to confirm no `>` block
restates the removed classification and no other passage carries it.

```
$ grep -o -E '.{120}\bF5\b.{160}' flat.txt
ne_length (comparison is raw bytes, no normalization) | layer record name | reader | open | `[R-ENC-15]` (R-ENC-13) | | F5 | File size is below the 128-byte minimum, so the front block, directory, pre-trailer pad and trailer cannot all fit | F (physical file size); committed_file_l
```
One hit only — F5's own row. **Nothing else in the document refers to what was
removed.** The "Also report / restatement elsewhere" item is therefore clean:
there is nothing to sweep.

```
$ grep -o -E '.{140}128 bytes.{140}' flat.txt      # 5 hits
  §5.1 [R-CNT-27] itself; §5.1's Example; §21.9 [R-ERR-05]'s limits list;
  Appendix A's minimal file; Appendix B's constants table.
```
None of the five mentions the version gate or a foreign major. No restatement of
the removed claim survives anywhere.

## 2.8 Check 6 — what does this paragraph leave unconstrained?

Structure governed: the partition of §21.2's 36 rows by whether each reaches a
file declaring a foreign major. Members and their disposition after the repair:

- named as reaching: F1, F6, F8, F14 (ground: `[R-CNT-24]`-fixed field)
- named as outside the premise: F18
- claimed not to reach, by the "geometry" clause: **unenumerated**

I walked all 36 rows against the word *geometry*. The paragraph's coined sense
must be "the file's byte layout" (every other use of *geometry* in the document
— §11.1, §10.4, L21, L32, §14.2, §23.2 — is *layer* geometry; I grepped the term
and reproduced the hits). Under that coined sense the clause plausibly covers
F2, F3, F5, F7, F9–F17, F20, F29–F33. It plainly does not cover **F4**
(duplicate layer names), **F19** (incompat-lane flag bits), **F21–F28**
(user-metadata record framing, record flags, sort order, MU/PE bits), **F34**
(two user-metadata records), **F35/F36** (reserved-range record types). Those
eleven-odd rows sit in no group at all.

This under-inclusiveness is pre-existing and unchanged by the repair, and the
paragraph does not claim to be a total partition, so I do **not** raise it as a
finding on its own. I record it because it is the reason A-01 matters: F5's home
is now decided only by which of two grounds a reader applies, and the paragraph's
taxonomy is too loose to settle it by structure.

The sibling-quantity shape the charter warns about (one quantity pinned, its
neighbour unpinned) does appear in a mild form here: F5's row has **two**
instances — "F (physical file size)" and "committed_file_length" — and they are
reached at different points of §19.1 (F at step 1, `committed_file_length` at
step 2 after the gate, per `[R-CNT-06]`'s "those gates passed, MUST validate …
committed_file_length equals the file size"). The removed sentence and the
current text both treat F5 as a single undifferentiated row. If F5 reaches a
foreign-major file at all, it reaches it only through the **F** instance; the
`committed_file_length` instance is unambiguously behind the gate. Neither side
of the diff says so. Folded into A-01's repair rather than raised separately.

## 2.9 Check 7 — analogy

The repaired text contains no analogy connective. I grepped the paragraph for
"exactly as", "the same way", "as X is", "following", "likewise", "the model
is", "transposed", "for the same reason" — none present. The nearest thing is
"F18 is **not an exception but a case outside the premise**", which is a
contrast, not a warrant borrowed from another rule; its cited rule (§21.6,
"version_major = 0 … permanently invalid in every format major version") uses
the governing verb *is permanently invalid in every*, and the paragraph's verb is
*declares no major at all*. Same range (the single field `version_major`, value
0, over all majors). **No analogy defect.** Reported as passing, per the charter.

## 2.10 What the repair got right, stated plainly

- The count went from five to four and four is correct under the ground the
  repair adopts.
- The false gloss ("a file shorter than 128 bytes has no trailer to read a magic,
  a CRC or a version from") is gone, and it was false.
- Turning "Four have as their subject a field fixed across every major" into
  "**because** their subject is a field fixed across every major" upgrades a
  description into a criterion, and the criterion is exhaustive over
  `[R-CNT-24]`'s fixed fields (§2.3 above). That is a genuine improvement.
- No restatement elsewhere in the document needed sweeping (§2.7 greps).

## 2.11 Findings raised

- **A-01** OVERSHOT — the revert removed F5's classification along with its false
  rationale, and §19.1's ordered open supports the classification it removed.
- **A-02** OVERCLAIM — "every check but the trailer magic and the trailer CRC" is
  falsified by the same paragraph and by `[R-CNT-27]`; now load-bearing.
- **A-03** CITATION — `[R-CNT-04]` is restated without its residency condition
  and its MAY-defer/omit exemption.

## 2.12 Byte-level analysis, both hunks

Disputed file for A-01/A-02: 96 bytes, trailer at [32, 96) with correct trailer
magic and correct trailer CRC, `version_major = 5`.
- Is it conforming? **Neither** — §2.3/`[R-CNF-02]` declines to judge a file
  declaring another major.
- Reader verdict under both readings: **reject-file**. One says "unimplemented
  major", the other says "file below the 128-byte floor". Same accept/reject bit.
- Writer: no conforming writer under this text emits it under either reading —
  `[R-CNF-05]` plus `[R-CNT-07]`'s major 1 and `[R-CNT-27]`'s floor. The emittable
  set does not move.
- Therefore **not byte-level**.
- What *does* fork is a **verifier's verdict label**: `[R-CNF-11]` gives
  *cannot establish* "as when the file names a format major version it does not
  implement", and also says "An established violation takes priority: a verifier
  that has established any violation reports *nonconforming*". Verifier V1, which
  evaluates `[R-CNT-27]` at §19.1 step 1, establishes F5 and reports
  *nonconforming*; verifier V2, which reaches the gate first, reports
  *cannot establish*. Same bytes, same accept/reject, different certificate. I
  name it because it is a real interoperability difference, and I decline to call
  it byte-level because the charter's discriminating test says not to.

A-03 is not byte-level either: the residency exemption is already stated
correctly in `[R-CNT-04]`, §19.1 step 1, §19.2's "at open" bullet and F6's and
F1's own row text, and §21.1 makes the rule govern over the register, so no
reader can be led to a different accept/reject by the preamble's shorthand.

Hunk 1 produced no findings, so no byte-level question arises there.
