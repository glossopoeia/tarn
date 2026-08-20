# Round 14 triage — correctness lens — working transcript

## Access disclosure

Read: `spec/tarn.md` only (sections 2.1–2.5, 3.1, 4.7, 5.1, 5.2, 6.1–6.3, 7.2,
7.3, 9.1–9.7, 10.3, 10.4, 11.1, 11.3, 14.3–14.5, 15.3, 15.4, 16.2, 17.2, 18.1,
19.1, 19.2, 20.3, 20.4, 20.5, 21.1–21.9, 24, Appendix G, Appendix H).
Ran one python count over the four register tables (below).

**Accidental access:** I ran `ls .../round14/ | head -1` to confirm the output
directory existed. It printed one filename, `build.py`. No
`transcript-triage-*.md` filename was displayed and none was opened. I did not
otherwise enumerate that directory, and I opened no walk transcript either.

Read nothing from `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, or the web. (I did see, in the harness task
list, the title of a completed round-13 task: "Fix §21.1 instance-criterion
asymmetry (T3/T14, F33/F7)". That is context, not evidence; every judgement
below is against the document text.)

## Mechanical check of the register

```
rows      F 36  L 49  T 26  R 10   = 121
instances F 56  L 111 T 57  R 44   = 268
```
(semicolon-split; a cell reading `—` counted as 1). §21.8 states "121
conditions over 268 instances". So the reporters' shared premise — the stated
total is faithful to the cells as written — is verified. Any defect is in a
cell or in the criterion, not in the addition.

I then extracted every row whose Condition carries `differs from`,
`does not equal`, `≠`, `is not exactly`, or `other than`. That is the check no
reporter ran, and it changes the shape of the finding (see group 1).

---

## Group 1 — the direction axis (7 findings)

Members: reader-01, writer-01, verifier-01, diagrams-02, register-01,
adversary-01, quiz-01.

All seven report the same defect: §21.1's second instance axis —

> "Where the condition compares two quantities and either can be the greater —
> a *differs from* or *does not equal* — the two directions are likewise
> enumerated; where its own text bounds the comparison in one direction — an
> *exceeds*, a *larger than* — there is one."

— is applied at T3/T14/T22 (6 = 3 layouts × 2 directions each) and at
L41 (gap; overlap; out-of-ordinal) but not at F17, L21, L22, L30.

Verified against the text, row by row:

- F17 `does not equal the transport-authoritative file size (physical file not
  truncated or extended to it)` — cell `committed_file_length`, 1 instance.
  Both directions are separately registered violations; §9.5's Note confirms
  the "extended" direction is real and lands on F17: *"Residue past a completed
  commit carries no register row of its own. A reader meets it as a trailer
  that fails its gates — the magic, the CRC, or committed_file_length against
  the transport size, each of which §21.2 already registers."*
- L21 `does not equal the geometry-derived addressed-tile count` — cell has the
  two layout formulas and no directions. Under either reading of how the two
  axes relate, this cell is short: it applies the layout axis alone. This is
  the row that refutes the "the direction axis only refines rows the layout
  axis split" escape.
- L30 `differs from the element size` — cell `—`, 1 instance, and the same
  phrase at T14 yields "length longer; length shorter".
- L22 first member `extent_length against the formula` — a bare ≠. (diagrams-02
  excludes L22 on the ground that its other two members are the two directions
  at the extremes; that is defensible — slot (0,0) with entry_count > 0 is the
  short extreme, a nonzero slot with entry_count = 0 the long one.)

So the reported defect is real as described. **CONFIRMED.**

### What no reporter caught

The criterion's trigger phrases sweep in rows nobody listed. Running the
trigger over all 121 rows:

```
F14  1  The u32 at trailer offset 60 does not equal the CRC-32C of [0,60)
F20  1  The final 4 bytes of the directory region do not equal the CRC-32C …
L37  1  crc_of_crc_array ≠ CRC-32C over the segment-CRC array …
L38  1  A segment CRC ≠ CRC-32C over that segment's entry bytes …
T6   1  … offset and length both 0xFFFF… but crc ≠ 0
R2   2  A user-metadata extent's final 4 bytes do not equal the CRC-32C …
```

Each uses "does not equal" or "≠" and each enumerates one direction's worth.
A stored CRC and a computed CRC are two quantities of which either *can* be the
numerically greater, so a literal application of the criterion demands two
instances for each of these too. Nobody suggests that; nobody should.

That matters for the repair. The criterion is wrong in **both** directions:
under-applied at F17/L21/L22/L30, where direction is a real property of the
comparison, and over-broad at the six CRC/equality rows, where it is not. The
fix is therefore not "add five instances and restate 268 as 273". It is to
narrow the axis to *magnitude* comparisons — a length, a size, a count against
a derived quantity — and then apply it to the four rows where it bites. The
reporters' totals (272 / 273 / 274) are three different numbers for the same
claim, which is itself evidence the cells are not mechanically determined by
the criterion as written. writer-01 and quiz-01 arrive at 274 from +1 (F17)
+2 (L21) +1 (L22) +1 (L30) = +5; that is 273. Their arithmetic is off by one.

### Byte-level: no

Downgrade quotations:

§21.1: *"The **Instances** column enumerates what a conformance corpus builds
for that row (§21.8)"* — the column's only job is to size the corpus.

§24 `[R-VEC-01]`: *"The corpus is **derivative**: a conforming implementation
is one that satisfies this specification's requirements, and where a vector's
recorded expectation and this specification disagree, this specification
governs and the vector is corrected. Passing the corpus is evidence of
conformance, never its definition."*

And both directions of all four conditions are already violations under the
same governing rule at the same scope — `[R-CNT-06]` (F17), `[R-CNT-17]`
(L21/L22), `[R-CNT-23]` (L30). No file changes status. Severity:
register-bookkeeping.

---

## Group 2 — §20.3 Example (c) over-forbids (reader-02, diagrams-01)

Both describe the same collision. Step 4 (normative):

> "A commit MUST NOT change a layer's declarations in a way that alters, **for
> any tile that layer stores**, what §14 fixes for its stored bytes or how they
> decode … A layer that stores no tile MAY be re-declared freely."

Example (c):

> "A fill change on a layer carrying either is not an appender's operation at
> all (step 4): it would invalidate every stored tile it reaches."

"Carrying a padding position" is geometric — §11.3: *"Where Gᵢ · Tᵢ > Eᵢ, the
tiles at the high edge of dimension i contain **padding positions**"* — and so
is carrying a pad bit (§14.3: only when P mod 8 ≠ 0). Neither depends on which
tiles are stored. The two separating files both check out: extents (5,5), tile
extents (4,4) — §14.5's own worked example gives that edge tile 15 padding
positions — with either no tile stored or only interior (0,0) stored. Step 4
permits the fill change; (c) says it is not an appender's operation. The
example's own justification is conditional ("every stored tile it reaches")
and reaches none. **CONFIRMED.**

Byte-level: no. §2.1 `[R-CNF-01]`: *"All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*;
and appendices identified as non-normative."* The colliding text sits under
"**Example** — the three shapes a commit takes". Severity: figure — the defect
is in the prose of the three-shapes example block.

Repair: "A fill change that reaches a padding position or pad bit of a tile the
layer **stores** is not an appender's operation at all (step 4)."

---

## Group 3 — Appendix G item 2, "low eight digest bytes" (writer-02, diagrams-03)

The strongest evidence here is the pair itself: two reporters read the same
sentence and resolved it **oppositely** — writer-02 takes the trailing eight
(digest as big-endian numeral), diagrams-03 the leading eight (digest as array,
"low" = lowest-indexed), each with a coherent argument, each noting that "read
little-endian" tells you how to assemble the chosen eight and not which eight.
Item 2 pins everything else: the input range, the zeroed field, the named
function at a named version, the all-zero fallback. It does not pin this.
**CONFIRMED.**

Byte-level: no. Appendix G's own preamble: *"It adds no requirement to any
actor: a writer ignoring it is fully conforming."* And §6.2's valid-values
column for file_id is `≠ 0`; both candidates are nonzero, so both files are
conforming and no reader treats them differently. Severity: editorial —
"trailing eight" or "leading eight" is a one-word fix, in the item whose whole
purpose is to remove this freedom.

---

## Group 4 — slack total with no live trailer (writer-03) — PARTIAL

writer-03 says `[R-CNT-21]`'s MUST cannot be discharged at F8/F14/F17 because F
is defined only by the live trailer. The observation about F is right (§5.1:
*"The file size of a conforming file equals the live trailer's committed file
length F"*; §6.2's table gives committed_file_length as `= F`). But the
obligation is not unconditional in the way claimed. §5.2 opens:

> "Coverage is a property of the **live committed state** — the front signature
> block, and every structure reachable from the live trailer through the live
> directory's records, extent slots, and tile-index entries…"

and slack is *defined* as "Every byte the live state does not claim". §9.7:
*"A verifier checking `[R-CNT-02]`'s partition walks the live state only. From
the live trailer it reads the live directory…"* With no live trailer there is
no live committed state, hence no slack, hence nothing the MUST demands. The
reporter's own reading (b) is the one the document supports.

Two of the reporter's supporting claims do not survive:
- Appendix H does **not** repeat the obligation without the precondition. It
  reads: *"the live-state coverage partition and the slack total (§9.7) —
  reported as partial … where its walk did not complete"*. "live-state" is the
  precondition.
- The F17 case is not a hole: there the trailer is valid, F is known, and the
  walk over the live committed state is defined; the file is rejected at open
  on other grounds.

So: PARTIAL. The residue is real but narrow — `[R-CNT-21]`'s sentence carries
no explicit precondition of its own, and a literal implementer could invent an
F. Repair: one clause ("where the file has a live committed state") or a
pointer back to §5.2's opening. Byte-level: no; the verdict is *nonconforming*
under §2.3's *"An established violation takes priority"* either way, and only a
report field moves.

---

## Group 5 — `[R-WRT-07]`'s two-case enumeration (writer-04)

> "No other record payload carries a file offset: MU = 0 records by rule
> (§7.2), and an MU = 1 type the compactor does not implement never reaches
> this step (`[R-WRT-06]`)."

Checked both cited rules. §7.2 `[R-CNT-13]`: *"For a record with MU = 0, the
extent slot is its only sanctioned reference to bytes outside the record
sequence"* — binds MU = 0 only, and expressly contemplates the other case:
*"Records with MU = 1 carry further references only where this specification or
registry review (§10) defines them."* §20.5 `[R-WRT-06]`: *"A compactor MUST
refuse to compact a file carrying any record whose type it does not implement
with MU = 1."* The uncovered third case is an MU = 1 type the compactor **does**
implement and this document does not assign. **CONFIRMED** — the enumeration is
a completed argument where a conditional on this text's type set was meant.

One correction/extension to the reporter: it says the gap opens only for a
later minor version. §10.3 and §2.3 also admit an *experimental*-range MU = 1
record in a conforming file (§2.3: *"in a conforming file such a type is
necessarily from the experimental range"*), and a compactor may privately
implement it. So the case is reachable under this text — but still not
byte-level, because this specification defines no content rule for such a
payload, so the compactor's output remains a conforming TARN file whichever
way it handles the offsets. Severity: editorial. Repair is the reporter's own
clause.

---

## Group 6 — Appendix G item 3, the first structure's offset (writer-05)

Verified §5.2's definition excludes the front block from "structure": *"Every
byte of the live committed state belongs to exactly one of: the front signature
block; **or** a **structure** — a stored-tile extent, a record extent …, the
directory, or the trailer."* Item 3's rule is "Each structure begins where the
previous one ended", and its zeroing requirement covers only gaps "where
alignment forces a gap"; a leading gap is neither. §9.2's *"writing beginning at
offset 16"* fixes where the writer starts writing, not where the first
structure starts — zero bytes written into a leading gap satisfy it. So the
first structure's offset is free, and the recap claims item 3 closes "gap
*extent*, which placement freedom (`[R-SLB-05]`) leaves open". **CONFIRMED.**

Byte-level: no — same quotation as group 3 (*"a writer ignoring it is fully
conforming"*), and §5.2 makes the leading gap slack, so both placements are
conforming. Severity: editorial; "the first structure begins at offset 16"
closes it.

---

## Group 7 — the slack total when the walk itself finds the defect (verifier-02)

The circularity is real. `[R-CNT-21]`:

> "Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration (**a rejected
> layer's claimants are not enumerated, whether or not the rejection impeded
> reading them**) …"

L18/L40/L41/L42/L48 are verifier rows whose detection *is* the walk: the
verifier must have enumerated the layer's claimants to find the defect. The
parenthetical's "whether or not the rejection impeded reading them" was
plainly written to defeat exactly the objection that they were readable, which
is what makes reading B available. Against it, §9.7 phrases the trigger as
*"a scope-level rejection **blocks** enumeration"*, and §21.1 says of verifier
rows that *"the outcome names the scope at which the damage is recorded, not an
obligation on any reader"* — both of which point at reading A (walk completed,
total exact). The two sentences are in tension and the document does not
adjudicate; the MUST-reported number differs (27 exact vs 75 partial on the
reporter's separating file). **CONFIRMED**, and I record that the text leans A
while the reporter picked B.

The reporter's refutation of behaviour (i) — summing claimant lengths rather
than unioning them — checks out: with the overlap present, sum = 233, union =
229, F = 256, so F − sum = 23 under-counts the true 27, and `[R-CNT-21]` says
*"never an under-count"*.

Byte-level: no. Every route runs through an already-established violation;
§2.3: *"An established violation takes priority: a verifier that has
established any violation reports *nonconforming*."* Severity:
design-decision — the maintainer has to choose what "a rejected layer's
claimants are not enumerated" means when the rejection is the walk's own
finding, and say so in `[R-CNT-21]`.

Note: verifier-02 also raises, as "a smaller sibling", the no-F case that is
writer-03's entire finding. I have put verifier-02 in this group because the
walk-paradox is its headline and its separating file, and writer-03 in its own
group, since the two need different repairs. The overlap is disclosed.

(One citation slip in verifier-02: it cites `[R-ENC-05]` for the bar on acting
on a field whose CRC failed; writer-03 cites `[R-ENC-10]` for the same. The
document's rule is `[R-ENC-05]` — §4.5, *"covering it has been verified"* —
with `[R-ENC-10]` about stated field order. Immaterial to either finding.)

---

## Group 8 — foreign-major files and the register (verifier-03) — PARTIAL

§2.3 does decide it, categorically: *"a file declaring another major is neither
conforming nor nonconforming under it: a reader refuses such a file on
capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
about its bytes."* The reporter agrees. Its actual claim is that **nothing
points at §2.3** from the register, so an implementer lands on the wrong
reading.

That claim is false. §21.6's closing paragraphs address this exact case by
name:

> "Two structural cases are **conforming files a reader nevertheless refuses**.
> The first is **version_major naming a major this reader does not implement**:
> the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly
> conforming under that major. … Neither is a register row: the register
> enumerates file-conformance violations (§21.1), and a file this document
> declines to judge is not one."

That is inside §21, one subsection past the tables, and it states precisely
that the register does not reach such a file. So the signpost the reporter says
is missing exists. **PARTIAL**: the underlying question is decided and
signposted; the only residue is that F5/F9/F10/F13/F16 carry no local pointer.
Byte-level: no — the reader rejects under `[R-CNT-07]` either way, and only a
verifier's verdict *label* is at issue. Severity: editorial, optional.

---

## Group 9 — Appendix G recap omits item 10 (diagrams-04)

Mapping verified: the recap's entries are items 3 (gap content, gap extent,
record/sub-record order), 7, 6, 4, 5, 8, 2, and 1+9. Item 10 (NFC names) is
absent. **CONFIRMED** as a factual omission.

The harm claim is weaker than stated, because the paragraph guards itself:
*"Read the numbered items as the list; this paragraph names what they are for,
not how many there are."* "How many there are" disclaims completeness of the
enumeration, which is exactly the property the reporter tests. Byte-level: no
(non-normative appendix; item 10 itself is present and complete). Severity:
editorial, optional — a clause "and name normalization, which `[R-ENC-14]`
states as a SHOULD" would close it.

---

## Group 10 — §21.1's "outcome follows from scope" vs §21.5 (register-02)

§21.1 says it twice — *"the outcome class its scope determines (§2.4)"* and
*"the outcome follows from that scope, never from the severity of the
corruption"* — with no carve-out. §2.4 `[R-CNF-08]`'s map has three outputs:
*"file → reject-file, layer → reject-layer, tile → reject-tile."* All ten §21.5
rows carry ignore-record, and §18.1 states outright that scope does not decide
there: *"The owning scope of a user-metadata record is the file when the record
is top-level and the layer when it is a sub-record — but the outcome of every
failure to read its **document** is ignore-record whatever the scope, because
the document is **quarantined**."* So §21.1's general statement is contradicted
by a twelfth of the register it introduces. **CONFIRMED.**

The rows are right and §21.1 is the defective text — which is also what
§21.1's own escape clause produces (*"where a row and the rule it cites
diverge, the rule governs"*, sending the reader to `[R-CNT-25]`/`[R-MTA-02]`).
Byte-level: no. §2.4 `[R-CNF-12]`: *"For a nonconforming file no acceptance
obligation exists — a reader MAY reject it upon detecting any violation."*
Every R1–R10 file is nonconforming, so both behaviours are conforming. I
checked the one place a conforming file could fork — an experimental-range
metadata encoding — and it is §21.6's row, which states ignore-record on its
own terms, and §21.1 expressly withholds itself from §21.6 (*"The subsections
after §21.5 are not part of the register and carry no rows"*). Severity:
editorial; add the quarantine exception to §21.1's sentence.

---

## Group 11 — the Governing rule cell's parenthesized identifiers (register-03)

Grepped the whole document for any statement of the convention: `parenthes`
matches nothing outside the register cells themselves; the only "Governing
rule" hits are the four table headers. §4.7's Note describes layout-table
columns and does not reach the register. So the reporter's central claim — the
convention is nowhere stated — is **CONFIRMED**. The supporting facts check
out: F1 is `` `[R-ENC-02]` (R-CNT-04, R-CNT-06) ``, L2 carries four
parentheticals, and L26's parenthetical is `(§7.3 registry table)`, a section
reference that cannot co-govern.

The intended reading is nonetheless recoverable: §2.2 fixes the identifier form
as `[R-<PREFIX>-<NN>]`, so a bare `R-CNT-04` is not an identifier of the
defined form; §21.1's prose and §24's `[R-VEC-02]` (*"that row's governing
requirement identifier"*) are singular. Byte-level: no — it is a manifest and
navigation question; I spot-checked multi-citation cells (F1, F5, F13, F14,
F16, L2, L21, L22, L30, L44, R1–R10) and found no cell where bracketed and
parenthesized rules would answer differently about a file. Severity: editorial;
one sentence in §21.1 stating the convention.

---

## Group 12 — §21.1's verifier-row escape omits `[R-MTA-05]` (register-04)

Verified: §21.1 says *"for several such rows it obliges the reader to serve the
structure unchanged (`[R-SER-08]`, `[R-CNT-22]`)"*, and F27/L48 are governed by
`[R-MTA-05]`, whose text is *"readers process the document unchanged"* — the
same class, not named. §21.6's closing paragraph confirms the pairing the
reporter points at: *"a user-metadata document whose object members are
unsorted (`[R-MTA-05]`), and a registered record type whose stored MU or PE bit
differs from §7.3's registry (`[R-CNT-22]`)"* — one of that pair reached §21.1's
parenthetical and the other did not. **CONFIRMED.**

Reading (b) — the parenthetical as a closed list making F27/L48 binding on
readers — is not really available, and I record three guards the reporter did
not: F27 and L48 each say in their own Condition cell *"the document stays
readable and readers process it unchanged"*; §21.6's closing paragraph says
*"neither is a reason for a reader to reject anything"*; and `[R-MTA-05]`
itself governs under §21.1's own escape clause. Byte-level: no. Severity:
editorial; add `[R-MTA-05]` to the parenthetical.

---

## Group 13 — "an extent MAY always grow" vs the lz4 cap (adversary-02)

Arithmetic verified: extent 0 → 1 with tile extent 2³¹ and one uint8 channel
gives P·Q = 2³¹ = 2,147,483,648 > 0x7E000000 = 2,113,929,216, so the grown
layer trips L44/`[R-COD-07]`. §17.2's cap is quantified over *addressed* tiles,
so the empty layer escapes it; the growth ends the escape. §20.3 states the
permission flatly: *"and an extent MAY always **grow**, since a position that
becomes real held that channel's fill and fill is a legal sample value."*
The only cross-reference is §17.2's Note — *"The escape is not durable: a later
commit that grows an extent addresses tiles, and the same declarations are then
measured against the cap"* — which §2.1 makes non-normative. **CONFIRMED** as
an observation; the text is decidable, since `[R-COD-07]`'s reader clause is
unconditional and `[R-CNF-05]` binds the writer to conforming output, so the
MAY is an exception to the prohibition it follows and not a global licence.

Byte-level: no — the grown file is nonconforming under both readings, so no
conforming implementation's emit set or accept/reject set moves. Severity:
editorial; qualify the MAY, or cite `[R-COD-07]` beside it.

---

## Group 14 — the tense of "any tile that layer stores" (quiz-02) — PARTIAL, and
## the only byte-level flag in the input

This is the finding I spent the most time on, since it is the one self-flagged
byte-level and the gate is asymmetric.

The reporter's claim: §20.3 step 4's *"for any tile that layer stores"* does not
fix whether the prior or the new generation's stored set is meant, and the only
text naming a tense is §11.1's **Rationale** (*"a tile the layer already
stores"*), which §2.1 makes non-normative. Separating case: one commit that both
changes declarations and unstores every tile.

Two things decide it against the reporter.

**(1) "stored" is a defined term with a tense.** §3.1:

> "**addressed tile / stored tile** — every tile of a layer is *addressed*. A
> tile is *stored in a generation* if and only if that generation's tile-index
> entry for it is not the sentinel (§15); **unqualified *stored* means stored in
> the live generation.**"

Throughout §20.3 the live generation is the pre-commit one: step 1 establishes
F from *"the trailer at the physical end of the file"*, step 4 begins *"writing
begins at exactly F"*, and §9.2 makes the new trailer the last thing appended.
Step 4 also draws the contrast itself — *"entries for tiles that **become
unstored** written as the sentinel"* — which presupposes that those tiles are,
as the rule speaks, stored. So the reporter's "the only text in the document
that names a tense" is a Rationale is simply false; §3.1 is normative and names
it.

**(2) The separating case comes out the same under either tense anyway.** Step 4
states its own operative test twice:

> "**The test is the effect on a stored tile**, and the list names where that
> effect arises rather than standing on its own … Where a change does reach them
> **it makes each stored tile it reaches nonconforming**…"

A commit that unstores every tile of the layer makes no stored tile
nonconforming: the superseded payloads are slack, and §5.2 says of slack that
*"its content is unconstrained, and no conformance requirement applies to it"*.
So there is no tile the change "reaches" in the sense the rule defines, whichever
generation's stored set one reads into "stores". Both readings permit the
commit, and the byte fork the reporter constructs between U1 and U2 does not
arise.

A third, smaller correction: even if the commit were barred, the cost is not the
whole-file rewrite under a fresh file_id that the reporter asserts. Unstoring
every tile with no declaration change is unconstrained by step 4, and the
resulting layer then *"stores no tile"* and *"MAY be re-declared freely"*. Two
commits, not a rewrite.

**PARTIAL.** Something is genuinely thin — §20.3 never spells the tense out, and
the reader who wants it stated finds it only by chaining §3.1 into step 4 — but
the reported defect (an undetermined tense forking the emittable byte set) is not
what the text has. Byte-level: **no**, on the quotations above. Severity:
design-decision only in the weak sense that the maintainer may want to add the
qualifier "in the generation this commit supersedes"; I file it editorial.

---

## Group 15 — "decidable from index bytes alone" (quiz-03)

Verified. §16.2 closes with *"so this invariant stays decidable from index bytes
alone"*, and classifying an entry as reject-tile *on a structural ground*
requires §15.3, which opens *"For each entry, **with F the committed file
length** and S denoting the sentinel value 2⁶⁴ − 1, a reader MUST classify as
follows"* — and one of the six structural rows is *"offset + length overflows, or
offset + length > F − 64 (non-sentinel)"*. F is a trailer field, not an index
byte. **CONFIRMED**; the claim that actually holds is that the invariant needs no
stored-tile payload, which is the claim that matters (the alternative would make
slab checking fetch every tile).

Byte-level: no. §19.1 step 2 puts the validated trailer in every reader's and
verifier's hands before any index region is fetched, so no conforming actor is
ever in the position the sentence describes and every implementation classifies
identically. Severity: editorial; "from the index and the trailer" or "without
fetching any stored tile".

---

## Coverage

23 input ids, 15 groups, each id in exactly one group:

1. direction-axis — reader-01, writer-01, verifier-01, diagrams-02, register-01, adversary-01, quiz-01  (7)
2. example-c — reader-02, diagrams-01  (2)
3. digest-bytes — writer-02, diagrams-03  (2)
4. slack-no-live-trailer — writer-03  (1)
5. compactor-enumeration — writer-04  (1)
6. first-structure-offset — writer-05  (1)
7. slack-walk-paradox — verifier-02  (1)
8. foreign-major — verifier-03  (1)
9. recap-item-10 — diagrams-04  (1)
10. outcome-vs-scope — register-02  (1)
11. parenthetical-convention — register-03  (1)
12. mta-05-omitted — register-04  (1)
13. extent-grow-lz4 — adversary-02  (1)
14. stores-tense — quiz-02  (1)
15. index-bytes-alone — quiz-03  (1)

7+2+2+1+1+1+1+1+1+1+1+1+1+1+1 = 23. Counted twice, by hand and by the list
above.

Byte-level upheld: **0**. I am uneasy reporting zero, and I record which call
was closest: quiz-02, downgraded on §3.1's definition of "stored" plus step 4's
own twice-stated test. If a second pass upholds it, the two quotations above are
the ones to argue against, not the reporter's framing.
