# Round 26 audit — downstream-accounts charter (hunks 01 and 02)

## 0. Disclosure

Files opened: `/private/tmp/.../r26audit/hunk-01.diff`, `/private/tmp/.../r26audit/hunk-02.diff`,
and `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (many ranges, listed below).
Nothing else. I did not open `full.diff`, other hunk files, `docs/`, `conformance/`,
`spec/registry.json`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, git history,
or the web. I did not list the r26audit directory (I ran `mkdir -p` on it before writing this
file; no listing).

Unrequested context appeared before I began: a project-instruction file (CLAUDE.md pointing at
AGENTS.md) and an index of the maintainer's memory notes naming several TARN working-practice
topics. I did not open any of the files it names and drew no conclusion from it. Its contents
are not repeated here.

Commands run: `wc -l`, `grep -n` (patterns listed inline below), `sed -n` range prints,
`awk` on a line range, and one `python3` heredoc that reads only `spec/tarn.md` and counts
register rows/instances.

Spec ranges read in full: 225-272 (§2.4), 473-520 (§4.6), 553-560/618-692 (§5.1 tail, §5.2),
693-736 (§6.1), 866-1000 (§7.1-§7.3), 1000-1112 (§7.4), 1321-1372 (§9.7), 2418-2630 (§18.1-§18.4
head), 2747-2816 (§19.2-§19.3 head), 3335-3414 (§21.1), 3414-3470 (§21.2), 3471-3530 (§21.3),
3528-3600 (§21.4, §21.5), 3596-3660 (§21.6 + tail prose), 3721-3740 (§21.8, §21.9 head),
3895-3925 (§22.4), 4002-4090 (§24), 4320-4345 (Appendix G item 3), 4403-4474 (Appendix H).

---

## 1. The two repairs, and the rule each adopts

### Hunk 1 — §21.3 row L16, Condition cell (spec line 3493)

Before: `A layer record's or sub-record's nonzero extent slot has extent_offset < 16, pointing
into the front signature block`

After: `A layer record's or sub-record's nonzero extent slot has extent_offset in 1-15, placing
the extent inside the front signature block`

**Rule the repair adopts, in my words:** for a layer record or one of its sub-records, an extent
slot that is not the "no extent" slot and whose `extent_offset` is one of the fourteen values
1 through 15 is a reject-layer violation. Offset 0 is no longer named by this row; whatever
registers a slot whose offset is 0 must be some other row. An implementation that rejects a
layer whose record extent begins at byte 7 conforms; an implementation asked which row records
a layer record extent slot of (0, 200) must now look elsewhere than L16.

### Hunk 2 — §21.5 row R7, Condition cell (spec line 3591)

Before: `A decoded user-metadata document is not well-formed JSON, or its top-level value is not
an object`

After: `A decoded user-metadata document is not well-formed JSON, its top-level value is not an
object, or it carries a leading U+FEFF byte-order mark`

**Rule the repair adopts, in my words:** three independent facts about a decoded user-metadata
document each make it unreadable and each is registered by this one row — bad JSON, a non-object
top-level value, and a leading byte-order mark. The third was already enumerated in the row's
Instances cell but not stated in its Condition; the repair makes the Condition state what the
Instances cell builds. Nothing about the file's bytes changes; what changes is that the row's
condition text and its instance arithmetic now agree.

---

## 2. Register arithmetic (the "count or total" limb of my charter)

§21.8 (line 3722-3725): "Every row of §21.2 through §21.5 — **121 conditions over 277
instances** — has at least one conformance vector (§24) ... and one vector per instance."

§21.2 head: "36 conditions." §21.3 head: "49 conditions." §21.4 head: "26 conditions."
§21.5 tail: "10 conditions."

I recomputed both totals mechanically from the current file with a script that reads only
`spec/tarn.md`, splits each register table row on `|`, and counts the Instances cell as 1 when
it is `—` and otherwise as the number of semicolon-separated items (§21.1: "Instances within a
cell are separated by semicolons, and a cell reading — is one instance; the count is therefore
mechanical once the cell is written."). Exact output:

```
{'21.2': 3413, '21.3': 3470, '21.4': 3527, '21.5': 3561, '21.6': 3595}
21.2 rows 36 instances 58
21.3 rows 49 instances 116
21.4 rows 26 instances 55
21.5 rows 10 instances 48
total instances 277
```

36+49+26+10 = 121 ✓ and 58+116+55+48 = 277 ✓. **Both stated totals still hold.** Neither hunk
touched an Instances cell or added/removed a row, so this was the expected result, but it also
tells me something about hunk 2: R7's Instances cell held six items *before* the repair while
its Condition text stated only two alternatives over two containers (= four by §21.1's
arithmetic: "a condition applying to two alternatives in two containers has four"). The repair
raises the Condition to three alternatives × two containers = six, which is what the cell has
always listed and what the 277 total has always counted. So the repair moves the row *into*
agreement with a total that was already written for the post-repair reading. No count downstream
of hunk 2 needs sweeping.

Same test on hunk 1: L16's Instances cell is "layer record extent slot; sub-record extent slot"
= one alternative over two containers = 2, both before and after. "extent_offset < 16" and
"extent_offset in 1-15" are each one alternative — §21.1's direction rule ("where its own text
bounds the comparison in one direction — an *exceeds*, a *larger than* — there is one ... Nor
does a field tested only for being nonzero") gives one either way, and a membership test against
a fixed constant range is not "a comparison of two magnitudes either of which can be the
greater". So 2 stands. No count downstream of hunk 1 needs sweeping.

---

## 3. Who cites the changed rows

```
$ grep -n "L16\|L15\|L17\|\bR7\b\|R7)\|R7," spec/tarn.md
3466: | F33 | ... a claimant reaching the front signature block or the live trailer is instead
       caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier | ...
3492: | L15 | ...
3493: | L16 | ...
3494: | L17 | ...
3591: | R7  | ...
```

So exactly one passage outside §21.3 cites L16: **F33** (§21.2, line 3466). **Nothing anywhere
cites R7.** That narrows hunk 2's citation surface to zero and makes F33 the one place hunk 1
can have broken by label.

---

## 4. The underlying rule for hunk 1 — [R-CNT-13], §7.2 line 928

Verbatim (hard wrap normalised):

> The **extent slot** (extent_offset, extent_length): (0, 0) means no extent. Any other
> combination with either half zero, an extent_offset < 16, an extent extending past F − 64, or
> an overflowing sum is a validity error at the scope the record governs (§7.3): the layer for a
> layer record and for sub-records, the file for other top-level records ...

Four disjuncts, over the set "any combination other than (0,0)":

| disjunct | register row (layer tier) | register row (file tier) |
|---|---|---|
| either half zero | L15 | F30 |
| extent_offset < 16 | L16 | F31 |
| extent extending past F − 64 | L17 | F32 |
| overflowing sum | L2 (sum instance) | F3 |

**Check 2, citation verdict:** L16 cites `[R-CNT-13]`. [R-CNT-13] does contain a lower-bound
rule on `extent_offset` and does place its outcome at layer scope for a layer record and its
sub-records. **PASS** — the citation resolves and says what the row needs it to say.

**Check 1, quantifier comparison against the rule the row restates:**

- rule's governing words: "*Any other combination* with ... an *extent_offset < 16* ... is a
  validity error"
- row's governing words: "A layer record's or sub-record's *nonzero extent slot* has
  *extent_offset in 1-15*"

The rule's disjunct is strictly wider than the repaired row: `< 16` includes 0, `1-15` does not.
That is not by itself a defect — §21.1 says "each row *restates* its governing rule, and where a
row and the rule it cites diverge, **the rule governs**", and §21.1 also makes register
*completeness* normative. Completeness survives, because the slot values the row shed are picked
up by L15:

- (0, N), N>0 → L15 ("exactly one of extent_offset and extent_length zero") ✓
- (M, 0), M>0 → L15 ✓
- (M, N), 1≤M≤15, N>0 → L16 ✓

Union of L15 and L16 = union of the rule's first two disjuncts, exactly. **No gap.** No tense
question arises: neither the row nor [R-CNT-13] is quantified over a superseded generation;
[R-CNT-13]'s overlap clause is the only part that says "within the live committed state" and it
is L18/F33's subject, not L16's.

---

## 5. The underlying rule for hunk 2 — [R-MTA-04], §18.2 lines 2537-2571

Verbatim, the head sentence and the first bullet:

> The decoded document is a JSON text as defined by RFC 8259, encoded in UTF-8. Four
> restrictions apply, and a document violating any of them is unreadable — ignore-record, with
> the report `[R-CNT-25]` asks for:
>
> - **A JSON object, unmarked.** The top-level value is an object, and the encoding carries no
>   byte-order mark: a leading U+FEFF makes the document unreadable.

`[R-MTA-04]` is tagged at line 2571, after the fourth bullet, so it governs the head sentence and
all four bullets.

**Check 3, normative placement.** I checked whether the BOM rule lives only in a `>` block:

```
$ awk 'NR>=2537 && NR<=2572 {print substr($0,1,3)}' spec/tarn.md | grep ">"
(no output)
```

No line in that span begins with `>`. The BOM rule is a plain bullet in normative prose under
`[R-MTA-04]`. And:

```
$ grep -n "FEFF\|byte-order mark\|BOM" spec/tarn.md
376:  little-endian. `[R-ENC-01]` There is no byte-order mark and no big-endian
2543:  and the encoding carries no byte-order mark: a leading U+FEFF
3591: | R7 | ... or it carries a leading U+FEFF byte-order mark | ...
```

Line 376 is `[R-ENC-01]` on integer byte order — a different sense of "byte-order mark",
unrelated to the document, and not a restatement that needs sweeping. So the BOM rule has
exactly one normative home (§18.2) and one register row (R7), and the repair put the row in
agreement with the home. **PASS.** The repair did not edit a `>` block, and no `>` block anywhere
states the BOM rule in the old terms.

**Check 1, quantifier comparison.**

- rule's governing words: "*the encoding carries no byte-order mark: a leading U+FEFF makes the
  document unreadable*"
- row's governing words: "*A decoded user-metadata document ... carries a leading U+FEFF
  byte-order mark*"

Both range over one decoded document, both fix on a *leading* U+FEFF (not U+FEFF anywhere), both
are stated over the *decoded* document — which matters under encoding 2, where the BOM would sit
in the zstd frame's output, and §18.2's bullets sit under "The decoded document is ...". Same
set, same generation. **PASS.**

**Check 2, citations.** R7's Governing rule cell is `[R-MTA-04]` (R-CNT-25).
- `[R-MTA-04]` (§18.2, lines 2537-2571) — opened; it states the JSON-text requirement, the
  top-level-object requirement and the BOM requirement. **PASS.**
- `[R-CNT-25]` (§7.1, lines 878-898) — opened; "each way a user-metadata record's document can be
  unreadable once its framing has been read — a failed extent CRC, an unimplemented or invalid
  encoding, a decode failure, or content violating the document's own rules ... — is
  ignore-record with a SHOULD-report". A leading BOM is "content violating the document's own
  rules", so the ignore-record outcome the row carries is warranted. **PASS.** Note this
  enumeration is by *kind*, not by individual restriction, so adding the BOM to R7 does not
  falsify it and it needed no sweep.
- §21.5's preamble (line 3565-3575): "every way its document can be unreadable takes this
  outcome, whatever the containing scope — as a violation in the rows below, except at an
  experimental-range encoding ... and except where a reader or verifier declines the decode on
  the size bound or on the frame's declared window". A BOM is neither exception. **PASS.**

---

## 6. Reverse check for hunk 2 — does the widened R7 now overlap another row?

Rows in the same table that could register a leading BOM:

- **R3** ("stored bytes fail to decode under its declared assigned encoding") — decoding here is
  the *encoding* layer (verbatim, or the zstd frame), not JSON parsing. `EF BB BF` decodes fine
  under encoding 1 and inside a well-formed frame under encoding 2. **No overlap.**
- **R4** (encoding-2 frame constraints) — about what the frame header declares. **No overlap.**
- **R5** ("a key or string value whose UTF-8 is ill-formed in the source bytes, or that resolves
  a `\uXXXX` escape denoting an unpaired surrogate") — `EF BB BF` is well-formed UTF-8, and a
  leading BOM is not inside a key or a string value. **No overlap.**
- **R6, R9, R10** — key-level. **No overlap.**
- **R8** — numbers. **No overlap.**
- §21.6's entries — I read the whole table (lines 3601-3620). The two user-metadata entries are
  the unrecognized `tarn.` key and the mis-scoped standardized key; there is no entry declaring
  a BOM tolerable, so the repair does not contradict a defined non-violation. **No overlap.**

The one arguable internal redundancy is *within* R7 itself: RFC 8259's grammar does not admit a
leading BOM, so "not well-formed JSON" arguably already subsumes "leading U+FEFF". I do not
treat that as a defect — §18.2 states the BOM separately precisely because RFC 8259 §8.1 lets a
parser ignore a BOM rather than erroring, so a row that leaves it implicit would let a
BOM-tolerant parser conclude nothing is wrong. Two instances in the same row are also not a
bookkeeping error the way two *rows* would be, and §21.1's "one instance is one *distinguishable*
file" is satisfied: a BOM-prefixed valid object and a syntactically broken document are different
files.

**Check 4, contradiction in the same passage, hunk 2.** I read §21.5's whole preamble and all ten
rows. There is no carve-out sentence about the BOM, no MAY that the new breadth collides with,
and no sentence written to be true only under the old two-alternative wording. The preamble's two
carve-outs (experimental encoding; a reader/verifier declining on a size or window bound) both
sit upstream of the decoded document and are untouched. **PASS.**

**Check 5, exhaustive claims, hunk 2.** The repaired cell contains no "every", "always", "only",
"the two X", closed list or count. It is an open three-way disjunction joined by "or". §18.2's
neighbouring count — "**Four** restrictions apply" — is a completeness claim I did try to
falsify: restriction 1 (object, unmarked) → R7; restriction 2 (finite numbers) → R8;
restriction 3 (no duplicate keys) → R9; restriction 4 (well-formed UTF-8 throughout, plus §4.6's
key rules) → R5, R6, R10. All four are registered, and the repair puts restriction 1's second
half onto a row for the first time. The count of four is unaffected. **PASS.**

**Check 6, what R7 leaves unconstrained, hunk 2.** The structure R7 governs is the decoded
document's top-level framing. Its members: (a) whether a BOM precedes the value; (b) whether the
byte sequence is a well-formed JSON text; (c) what type the top-level value has; (d) whether
anything follows the JSON text; (e) the encoding of the whole (UTF-8). (a), (b), (c) are now all
in R7. (d) falls to "not well-formed JSON" — RFC 8259 defines a JSON text as one value with
optional surrounding whitespace, so trailing garbage is not well-formed. (e) is R5 via
`[R-ENC-11]`. I found no sibling quantity of this structure that the repair pins for one member
and leaves loose for another. **PASS.**

**Check 7, analogy, hunk 2.** The repaired cell contains no "exactly as", "the same way", "as X
is", "following X", "likewise", "transposed from", or "for the same reason". There is no warrant
citation to compare verbs against. (For contrast, R4's cell and §18.2 both carry such analogies —
"the tile rule of `[R-COD-06]` transposed to the quantity a document does have" — but they are
not in this hunk and not reached by it.) **Nothing to compare; no finding.**

**Conclusion on hunk 2: no findings.** All seven checks run, all pass, and both the outside-facing
limbs (who cites R7 — nobody; what count depends on R7 — §21.8's 277, still correct) come back
clean.

---

## 7. Reverse check for hunk 1 — does the changed L16 cell now overlap another row?

This is where I found something.

`grep -n "nonzero extent slot\|nonzero slot"` returns exactly three hits:

```
3464: | F31 | A non-layer top-level record's **nonzero extent slot** has extent_offset in 1-15,
        placing the extent inside the front signature block | extent_offset | reader | open |
3493: | L16 | A layer record's or sub-record's **nonzero extent slot** has extent_offset in 1-15,
        placing the extent inside the front signature block | ... |
3499: | L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 —
        including slot (0,0) with entry_count > 0, or **a nonzero slot** with entry_count = 0 | ... |
```

The term "nonzero extent slot" is nowhere defined. Two readings are open:

- **(i) "not the (0,0) slot".** This is how the document uses the phrase elsewhere: L22, in the
  *same table*, sets "slot (0,0)" against "a nonzero slot" as complements. §7.4 reinforces the
  binary — "a layer with zero addressed tiles has extent (0, 0)" — and [R-CNT-13] opens with
  "(0, 0) means no extent. **Any other combination** ...", i.e. the document's one named partition
  of the slot space is {(0,0)} versus everything else.
- **(ii) "both halves nonzero".** Supported only by the row's own trailing gloss, "placing the
  extent inside the front signature block": a slot of length 0 places no extent anywhere.

Under reading (i) the repaired L16 registers a slot of `(extent_offset = 5, extent_length = 0)`:
it is not (0,0), so it is a nonzero extent slot, and 5 is in 1-15. **L15 already registers that
same file** — "A layer record's or sub-record's extent slot has exactly one of extent_offset and
extent_length zero". Two rows, one file, one defect. The mirror pair in §21.2 shows it even more
plainly, because F30 spells the case out where L15 leaves it implicit: F30 reads "A non-layer
top-level record's extent slot has exactly one half zero (**offset 0 with length != 0, or offset
!= 0 with length 0**)" and F31 reads "nonzero extent slot has extent_offset in 1-15".

Under reading (ii) there is no overlap — but then the old text ("nonzero extent slot has
extent_offset < 16") had no overlap with L15 either, since a both-halves-nonzero slot cannot have
offset 0, and `< 16` on such a slot means exactly 1-15. That is, under reading (ii) the repair is
a no-op: old and new denote the identical set. **A repair is only a repair under reading (i)** —
under (i) the old cell reached (0, N) and collided with L15's "offset 0 with length != 0" half,
and the new cell drops that. So the repair adopts reading (i) by its own logic, and under reading
(i) it removed one half of the collision and left the other half — (M, 0) for M in 1-15 —
standing. That is my B-01: **undershot**.

The clean fix is one word: "an extent slot with both halves nonzero", or "a slot whose
extent_length is nonzero and whose extent_offset is in 1-15". The same edit is owed to F31, which
carries the identical wording.

Other rows I tested against the new L16 for overlap and cleared:
- **L17** (`extent_offset + extent_length > F - 64`) — disjoint from offsets 1-15 for any file
  with F ≥ 128 ([R-CNT-27]'s minimum) unless the extent is enormous, in which case the file
  exhibits two independent defects, not one defect registered twice. Cleared.
- **L10/L11** (user-metadata sub-record: slot (0,0); extent_length < 5) — a sub-record at (5, 3)
  trips L11 and L16, but those are two distinct facts about the slot (too short; misplaced), not
  one fact registered twice. Cleared.
- **L1/L2** (domain and sum overflow) — disjoint from 1-15. Cleared.
- **L18** (intra-layer overlap) — verifier-tier, about two structures of one layer, not about
  the front block. Cleared.
- **T8** ("A non-sentinel tile-index entry has offset < 16") — a *different* structure (index
  entry, not extent slot) at a different tier, and its `< 16` is correct there because an index
  entry has no "no entry" reading of offset 0 (the sentinel is all-ones, §15.2, and length 0 is
  T10's row). So T8 is not a restatement of L16 that the repair should have swept; it is the same
  bound over a structure whose zero case is genuinely a violation of that bound. Cleared — I
  checked §15.3's restatement table too (line 2058: "| offset < 16 (non-sentinel) | *structural*:
  reject-tile — the front block is never payload |"), which is consistent with T8 and untouched
  by this repair.
- **F31** — same condition at the file tier for non-layer top-level records. The three subjects
  (layer record, sub-record, non-layer top-level record) exhaust the record space, so L16 and F31
  together leave no record kind unregistered and do not overlap each other. Cleared as a pair,
  though both carry the B-01 wording problem.

---

## 8. Check 4 for hunk 1 — the whole passage, including text the repair did not touch

I read §21.3's head prose (lines 3471-3475) and all 49 rows, and §21.1 in full. Looking for a
carve-out the new breadth collides with, a MUST the new MAY lets someone violate, or a sentence
true only under the old wording:

- §21.1's specialization list — "Some rows are strict specializations of others — F1 of F6 and of
  F8, F35 of F36, L24 of L25 — and a file exhibiting a specialization is recorded against the
  narrower row" — does **not** name L15/L16 or F30/F31. So the document has a mechanism for
  deliberate row overlap and did not apply it here, which is evidence the L15/L16 overlap of B-01
  is unintended rather than sanctioned. (I considered whether the maintainer might simply add
  L16 to this list instead of rewording. That would work, but it would be recording a
  length-0 slot against L16 — "placing the extent inside the front signature block" — which is
  the wrong description of the file. The wording fix is the better repair.)
- §21.3's head prose is two sentences about the reject-layer outcome and the condition count.
  Nothing turns on L16's breadth.
- No carve-out, no exception sentence, no "is not such a case" anywhere in §21.3.

**One sentence outside §21.3 is written against the old wording**, and it is the F33 cell —
finding B-02, next section.

---

## 9. F33 (§21.2, line 3466) — the sentence hunk 1 did not sweep

Verbatim, the clause that matters:

> ... a claimant reaching the front signature block or the live trailer is instead caught by the
> bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier

The four pairs are the four claimant tiers, each with a lower-bound row and an upper-bound row:

| tier | lower bound (front block) | its text | covers offset 0? |
|---|---|---|---|
| directory | F9 | "dir_offset is **less than 16**" | yes |
| non-layer top-level record extent | F31 | "extent_offset **in 1-15**" | **no** |
| layer record / sub-record extent | **L16** | "extent_offset **in 1-15**" (was "**< 16**") | **no** (was yes) |
| stored-tile extent | T8 | "offset **< 16**" | yes |

The clause's antecedent is "a claimant reaching the front signature block". §5.2 defines a
claimant: "Every byte of the live committed state belongs to exactly one of: the front signature
block; or a **structure** — a stored-tile extent, **a record extent (the bytes any record's
extent slot references, whatever the record's type, §7.2)**, the directory, or the trailer."
A slot of (0, N) with N > 0 references bytes [0, N) — byte 0 among them — so it is a claimant
reaching the front signature block and the antecedent holds. §9.7 states the corresponding
normative walk check: "It checks that these occupy disjoint byte ranges, that **each lies within
[16, F − 64)**". A (0, N) extent fails that check.

Before hunk 1, under reading (i), L16 was the row that caught it and F33's consequent was true
for the layer tier. After hunk 1 it is caught by **L15** — "exactly one of extent_offset and
extent_length zero" — which F33's list does not name. So the sentence now sends a reader (or a
corpus builder following §24's "the §21 register row it exercises") to a row that does not apply.
The same is true of F31/F30 at the file tier, so hunk 1 did not create this shape so much as
extend it from one tier to two; I report it as an unswept restatement rather than as a fresh
contradiction, but it is the passage hunk 1 falsified for the layer tier and it is in no hunk.

I looked hard for reasons this does not bite, and record them honestly:

- **Does the walk ever reach a (0, N) layer extent?** §5.2 says "a rejected layer's claimants are
  not enumerated", and L15 is reader-detected at layer access, so in practice the layer is
  rejected before certification and F33 never fires on it. At the file tier F30 is reject-file at
  open, likewise. So the practical consequence is nil for a reader.
- **Is the file's verdict in doubt?** No. Under every reading the file is nonconforming (L15 or
  F30), the outcome is the same (reject-layer / reject-file), the detector is the same (reader),
  and the detection point is the same (layer access / open).

What is actually wrong is therefore the cross-reference and the vector-attribution it drives, not
any accept/reject verdict. Two repairs are available: add "F30, L15" to F33's list, or say
"caught by the bounds and slot-shape rows of §21.2 and §21.3 rather than by this row". I prefer
naming the rows, since F33 already names rows.

I also weighed, and did **not** file, a related wording point: the repair replaced "pointing
into the front signature block" with "placing the extent inside the front signature block".
"Inside" reads as containment, and an extent at offset 15 with length 100 is not inside the
16-byte block — it merely starts there; "pointing into" and F33's own "reaching" were the more
accurate verbs. I leave it unfiled because the numeric predicate "extent_offset in 1-15" governs
and the gloss is explanatory, and because the new wording is verbatim-identical to F31's, so the
document is at least internally consistent about it. It is noted here so the maintainer can see
it was considered.

---

## 10. Remaining checks for hunk 1

**Check 3, normative placement.** Lines 3487-3495 all begin with `|` (verified with
`sed -n '3487,3495p' | cut -c1-3`), so the repair sits in a register table row, not a `>` block.
The rule it restates lives in §7.2 normative prose at line 928. I grepped the distinctive terms
of the rule across the whole document — "front signature", "front block", "extent slot",
"extent_offset < 16", "less than 16", "in 1-15" — and every hit is in normative prose, a register
row, an appendix marked non-normative (B, G, H), or a `>` Example/Note that restates nothing
contrary. The one restatement in normative prose that still says the *old* thing is
[R-CNT-13]'s own "an extent_offset < 16" at line 930 — and that is correct as it stands, because
the rule is the union of L15 and L16 and §21.1 makes the rule govern anyway. It is not a failed
sweep. **PASS.**

**Check 5, exhaustive claims, hunk 1.** The repaired cell's completeness-flavoured words are the
closed range "1-15" and the definite article in "**the** front signature block". I tried to
falsify both. §6.1: "Bytes [0, 16) of every file, constant in every format major version" — one
block, sixteen bytes, so 1-15 is exactly the set of nonzero offsets inside it and "the front
signature block" names a unique structure. §3.1 line 335 agrees: "**front signature block** — the
constant 16 bytes at offset 0 (§6)". Appendix B lines 4108-4109 give [0,8) and [8,16). No
geometry or version rule moves the boundary — §6.3's version gates do not resize it, and
`[R-CNT-24]` fixes it "across every major". **PASS**, with the caveat that the closed range
excludes 0 and that exclusion is what B-01 and B-02 are about.

**Check 6, what hunk 1 leaves unconstrained.** The structure is the extent slot: two u64 fields
and their derived sum. Every quantity and combination:
- `extent_offset` domain (> 2^63−1): **L1**, instances "layer record extent_offset; sub-record
  extent_offset" ✓
- `extent_length` domain: **L1** ✓
- sum overflow: **L2**, instances "layer record extent_offset + extent_length; sub-record
  extent_offset + extent_length" ✓
- exactly one half zero: **L15** ✓
- both zero: legal, "means no extent" ([R-CNT-13]); for a user-metadata sub-record it is
  **L10** ✓
- offset below the front block's end: **L16** (the repaired row) ✓ for 1-15, **L15** for 0
- upper bound against the trailer: **L17** ✓
- length below the CRC floor on a user-metadata sub-record: **L11** ✓
- length against the index formula on a layer record: **L22** ✓
- overlap with another structure of the same layer: **L18**; with another scope's: **F33** ✓
- alignment of the extent: **L39-L42** for tiles; nothing constrains a *record extent's*
  alignment, and nothing should — §16 alignment is per-tile and per-slab by construction
  (§16.1, §16.2), and Appendix G item 3 confirms record extents are placed freely.
No sibling quantity of this structure is left governed by nothing. The repair pinned the one
quantity in play and did not strand a neighbour. **PASS** — this is the check that caught the
compressed-frame-header defect, and I ran it field by field rather than by reading the sentence.

**Check 7, analogy, hunk 1.** The repaired cell contains no "exactly as", "the same way", "as X
is", "following X", "likewise", "transposed from", "for the same reason". Its only justificatory
clause is the gloss "placing the extent inside the front signature block", which points at a
*structure* (§6.1) rather than at a *rule* whose quantifier could be compared. The nearest thing
to an analogy is the verbatim parallelism with F31, so I compared those two anyway, word for
word:

- F31: "A **non-layer top-level record's** nonzero extent slot **has** extent_offset in 1-15"
- L16: "A **layer record's or sub-record's** nonzero extent slot **has** extent_offset in 1-15"

Same governing verb ("has"), same predicate, complementary and jointly exhaustive subject sets
(every record is a layer record, a sub-record, or a non-layer top-level record). The outcome and
detection point differ correctly per §7.2's scope assignment (file/open vs layer/layer access).
**PASS** — the parallelism is sound for both members. It does, however, mean the B-01 wording
problem is shared by F31, which is why B-01's repair names both rows.

---

## 11. Verdict

Hunk 2: clean on all seven checks and on both outside limbs (no citing passage, no dependent
count). Hunk 1: the repair is directionally right, completeness survives, citations resolve,
counts hold, and no sibling quantity is stranded — but it is half-done (B-01) and it left one
cross-reference pointing at a row that no longer covers the case it was written for (B-02).
Neither finding moves the emittable byte set: the disputed files are nonconforming under every
reading, so `[R-CNF-05]`/`[R-CNT-13]` bar a conforming writer from emitting them either way, and
readers take the same outcome at the same tier either way. Both are register bookkeeping, which
is what §21.1 makes normative about itself.
