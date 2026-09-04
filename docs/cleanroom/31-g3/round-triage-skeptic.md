# Triage pass — Skeptic lens — cleanroom round 31

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in full, in
  seven sequential `sed -n` ranges covering lines 1–4790. Two of those ranges
  overflowed the tool's inline limit and were saved to files; I re-read the
  overflowed regions (3000–3300, 3300–3700) at narrower width and read the
  register tables (3698–3880) by targeted `grep` on row ids.
- Targeted greps: `tile extent` (line-filtered to >3070), `F19|F35|F36|L24|L25|L44|L22|T2|R1`
  row texts, `entries restate their governing rules`, `the rule governs there too`,
  `All text in this document is normative except`, `all other layers are unaffected`.

I read **no** walk transcript, **no** other triage pass's notes, **no** `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the
web. I ran no directory listing of `r31-round/out/` or of any other agent's path.
Every quotation below is from `spec/tarn.md`.

## Grouping

24 input ids → 20 groups. Four ids collapse into one group (the `[R-CNF-03]`
top-level-qualifier defect, reported four times by four reporters); two ids
collapse into one (the growth paragraph's single-limb gloss of the §14 bar's
carve-out). Everything else is distinct.

I deliberately did **not** merge:

- **diagrams-01 with writer-02/verifier-01.** Both concern the §14 bar's
  carve-out, but they are different defects: diagrams-01 is that the carve-out's
  *second limb* is stated over "stored byte" where a packed-plane padding
  position is a bit; writer-02/verifier-01 is that a *downstream gloss* names one
  limb where the carve-out has two. A repair to either leaves the other standing.
- **adversary-02 with writer-02/verifier-01.** adversary-02 is §11.1's *Rationale*
  omitting §20.3's express growth permission; the other is §20.3's own growth
  paragraph under-describing the carve-out. Different text, different repair.
- **register-01 with the `[R-CNF-03]` group.** register-01 is about `[R-ERR-04]`'s
  *scope enumeration* for a resource decline; the `[R-CNF-03]` group is about the
  missing `top-level` qualifier on the MU = 1 exemption. They meet in §2.3 but are
  independent sentences.

---

## Group-by-group

### 1. cnf03-top-level-qualifier — reader-01, writer-03, adversary-01, quiz-02

**Verified against the document.** §2.3 `[R-CNF-03]`, verbatim:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from the
> experimental range, since a reserved-range type carrying MU = 1 is itself a
> violation — and none of whose values exceeds the minimum guarantees of §21's
> limits table

No `top-level`. §21.6's closing paragraph, verbatim:

> The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only the
> top-level case is a file a reader refuses

I confirmed that "record" ranges over both scopes in this document: §7.4
`[R-CNT-18]` — "Sub-records are layer-scope records". So the defect is real and
all four reporters have it right. **CONFIRMED.**

**Byte-level? No.** Two independent sentences decide the accept/reject verdict on
the disputed file:

1. §7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
   where the file is otherwise conforming a reader MUST NOT reject the file for
   it". Unconditional. Withdrawing a duty is not granting a permission.
2. The residue reader-01 raises — whether a reader that must open the file owes
   service on its *other, undamaged* layers, since `[R-CNF-03]` is the only source
   of that duty — is decided by §2.4's outcome table, which reader-01 did not
   reach: "**reject-layer** | The affected layer's data and metadata are not
   usable; **all other layers are unaffected**."

**The premise my downgrade rests on**, stated so it can be attacked: that §2.4's
"all other layers are unaffected" is a statement about the *reader's obligations*
toward those layers and not merely about the blast radius of the violation. If
someone reads it as purely descriptive of scope — "unaffected" meaning only "not
themselves rejected", leaving service on them ungoverned — then reader-01's
residue survives and the group becomes a behavioural fork about which layers a
reader must serve. I do not think that reading survives §2.4's own sentence "A
reader MAY still list the file's layers, including the rejected one's name",
which presupposes the file remains in service.

**Repair:** insert `top-level` before `record` in `[R-CNF-03]`. One word.

---

### 2. tile-extent-permutation-unbarred — writer-01

**This is the group I tried hardest to kill and could not.**

Verified the arithmetic independently. Interleaved, rank 2, E = (4,4), one uint8
channel, codec 1, filter 1.

| | T = (4,1) | T = (1,4) |
|---|---|---|
| G = (⌈E₀/T₀⌉, ⌈E₁/T₁⌉) | (1, 4) | (4, 1) |
| N = ∏Gᵢ | 4 | 4 |
| P = ∏Tᵢ | 4 | 4 |
| Q = ΣBᵢ | 1 | 1 |
| decoded size P·Q | 4 | 4 |
| entry_count (interleaved = N) | 4 | 4 |
| `[R-CNT-17]` extent_length = 4·20 + ⌈4/2¹⁶⌉·4 | 84 | 84 |
| offset of value k = (k div C)·Q + F_{k mod C} | k | k |
| padding positions (Eᵢ mod Tᵢ) | 4 mod 4 = 0, 4 mod 1 = 0 → none | 4 mod 1 = 0, 4 mod 4 = 0 → none |

And the coordinate map, from §11.4 `[R-GEO-06]` (tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ,
in-tile ordinal Σ uᵢ·∏_{j>i} Tⱼ, s = Σ tᵢ·∏_{j>i} Gⱼ):

- T = (4,1): byte k of tile s ↔ coordinate (k, s).
- T = (1,4): byte k of tile s ↔ coordinate (s, k).

Twelve of sixteen positions move. The array is transposed and not one stored byte,
index entry, or index-region byte changes. This is a shape-(c) directory-only
commit.

**Foreclosure attempts, all failed:**

- *Does §20 anywhere restrict tile extents?* `grep -n "tile extent" spec/tarn.md`
  filtered to lines > 3070 returns F7, F33, L1, L18, L32 (register cells) and
  Appendix G item 5 (non-normative) — and nothing else. §20 never mentions tile
  extents. The reporter's sweep is accurate; I reproduced it.
- *Does the enumerated list reach it?* The list names "the set of padding
  positions", "the pad bits", "the content `[R-SER-05]` fixes at both", "the
  decoded size", "the byte offset — or, in a packed plane, the bit position — of
  any value within the decoded tile image", "the sample type", "the codec and
  filter". Every one is unchanged, **unless** "any value" is read as
  coordinate-indexed rather than k-indexed — the value at coordinate (0,1) moves
  from tile 1 byte 0 to tile 0 byte 1. That reading is available and the reporter
  did not test it; it is an *argument* for reading (B), not a deciding sentence,
  and it depends on a construal of "value" the document nowhere fixes.
- *Does the general test sentence decide it?* "The test is the effect on such a
  tile, and the list names where that effect arises rather than standing on its
  own". This **does** refute reading (A) as the reporter phrases it ("the
  enumerated list is the test"). It does not resolve whether the general test —
  "alters … what §14 fixes for its stored bytes or how they decode" — reaches the
  permutation. §14 fixes the value sequence in terms of (spatial ordinal, in-tile
  ordinal, channel); §14.1's "value k of the sequence is channel (k mod C)'s value
  at in-tile ordinal k div C" is *formally unchanged* by the permutation. What
  changes is §11.4's ordinal→coordinate map and §11.2's grid — neither in §14.
  §14.1 does say "the tile's P positions", but §14 does not fix *which* positions
  those are.
- *Does the carve-out's rationale decide it?* "a change that leaves every one of
  those tiles' stored bytes meaning exactly what they meant … is not what this
  bars" states a **sufficient** condition for permission. Its contrapositive is
  not stated. Under the permutation the bytes do not mean what they meant, so the
  carve-out does not rescue the commit — but not-being-rescued is not being
  barred.
- *Does the sample-type paragraph reach it by parity?* "the type is what fixes the
  value a stored bit pattern denotes, so under a new one the same bytes denote
  different values." The tile extents are what fix the *coordinate* a stored byte
  denotes — the exact parallel — and §20.3 states the reasoning for types only,
  and enumerates the type. Parity of reasoning is not a normative sentence.
- *Is the operation forbidden elsewhere?* §20.4 `[R-WRT-05]` permits modifying a
  record ("a record it modifies is new output under its writer obligations
  (`[R-CNF-05]`)") and the output is conforming. §20.5 `[R-WRT-07]`'s
  reference-array-preservation MUST binds a *compactor*, not an appender. §23.1
  `[R-PRV-01]`'s operation list is expressly "not offered as closed". §11.1's
  Rationale ("Of its two bars…") confirms §20.3 has exactly two bars and this is
  not the planar-ordinal one.
- *Is the resulting file nonconforming?* No. Every register row is satisfied,
  `[R-CNT-17]` and `[R-COD-04]` hold, every checksum verifies. §21.7 makes it
  unwitnessed: no check any actor owes separates it from a file whose bytes were
  really stored under the new tiling.

**Byte-level: YES.** The discriminating question: updater U1, reading the
enumerated list, emits a commit whose appended directory carries the layer record
with its two tile-extent u64 fields swapped; U2, reading the general test with
§14.1 and §11.4 in hand, refuses and writes a new layer or a fresh-file_id
rewrite. Both files exist; only one is emittable by a conforming updater under
each reading. The emittable set of a conforming implementation moves.

**Consistency note on this test.** Several other groups here have the same shape —
a §20.3 permission question whose resolution moves what an updater may emit
(diagrams-01, writer-02/verifier-01, adversary-03, adversary-04, quiz-01). I
downgrade those and uphold this one on a single distinguishing ground: **for each
of those I found the sentence that decides the reading, and for this one I did
not.** That is the rule I applied throughout, and it is the rule to attack if this
grading is wrong.

**Repair (needs a maintainer decision, not just an edit).** Two options, and the
maintainer must pick:
(a) add a layer's declared **tile extents** to the §14 bar's enumerated list, on
the same terms as the sample type — with the parallel sentence, "the tile extents
are what fix the coordinate a stored byte denotes, so under new ones the same
bytes denote different coordinates" — barring the change wherever the layer stores
a tile in the superseded generation; or
(b) state expressly that the §14 bar does *not* reach a tile-extent change and
that such a commit is permitted, which would be a deliberate design choice to let
a directory-only commit transpose an array over unchanged bytes. (a) is plainly
what the rest of §20.3 intends. Either way the sentence must exist.

---

### 3. growth-gloss-single-limb-carveout — writer-02, verifier-01

Both reporters describe the same sentence and the same defect; verifier-01 adds
the n = 1 sub-observation. Verified verbatim in §20.3 step 4:

> The bar's carve-out does not reach a growth: it covers a position whose stored
> byte already holds the fill it keeps, not one that ceases to be padding, so this
> is an exception the permission states rather than one the carve-out supplies.

and, two paragraphs above in the same numbered step:

> a change that leaves every one of those tiles' stored bytes meaning exactly what
> they meant — a filter whose mandated stride makes it the identity
> (`[R-COD-10]`), or a new padding position whose stored byte already holds the
> fill `[R-SER-05]` fixes — is not what this bars.

Two limbs stated; one limb glossed. **CONFIRMED** — the gloss is incomplete.

**Byte-level? No.** The deciding sentence is the primary statement above, in the
same numbered requirement, naming both limbs disjunctively, preceded by "The test
is the effect on such a tile, and the list names where that effect arises rather
than standing on its own". A later sentence answering a different question ("does
the carve-out excuse a growth?") does not redefine a rule stated in full above it.
**Premise of the downgrade:** that within one numbered requirement a primary
definitional sentence governs a later sentence that glosses it in passing. If a
reader instead takes the *last* statement as controlling — a defensible drafting
convention in some documents, though not one this text adopts anywhere — then
reading (A) revives and a filter-declaration change on an all-identity layer is
barred under one reading and permitted under the other, which would move an
updater's emittable set.

verifier-01's n = 1 point checks out: `[R-COD-10]`'s map j·s + i → i·n + j is the
identity exactly when s = 1 or n = 1 (i = 1, j = 0 forces n = 1; i = 0, j = 1
forces s = 1), and Appendix G item 5 names both cases. The filter limb's own words
("a filter whose *mandated stride* makes it the identity") reach only the s = 1
case; the n = 1 case is reached by the general test alone. That is a second, real
under-description in the same carve-out, and it belongs in the repair.

**Repair:** in the growth sentence, replace "it covers a position whose stored byte
already holds the fill it keeps" with a reference to the carve-out's padding limb
("its padding limb covers…") so the sentence does not read as a definition; and
widen the filter limb from "whose mandated stride makes it the identity" to cover
the single-group case `[R-COD-10]` and Appendix G item 5 both name.

---

### 4. carveout-byte-vs-bit-packed-plane — diagrams-01

Verified all five occurrences of the byte-shaped wording (§20.3 ×3, §11.1
Rationale, §23.1) and `[R-SER-05]`'s three-case enumeration: "the recorded fill
bytes for a numeric channel, the recorded fill byte for an interleaved bool
channel, **the fill bit in a packed plane**". The mismatch is real: the bar's own
list is bit-aware, the carve-out is not. **CONFIRMED.**

Verified the witness: planar, one bool channel, d = 1, T₀ = 16, E₀ = 16 → P = 16,
G₀ = 1, N = 1, entry_count = C·N = 1, decoded size ⌈16/8⌉ = 2, P mod 8 = 0 so no
pad bits, E mod T = 0 so no padding positions. Shrink E₀ to 15: G₀ = ⌈15/16⌉ = 1
still, entry_count and extent_length unchanged, decoded size unchanged, in-tile
ordinal 15 becomes a padding position whose bit already holds the fill. No stored
byte changes.

**Byte-level? No.** Deciding sentence, two above the carve-out:

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of those
> tiles' stored bytes meaning exactly what they meant … is not what this bars.

In the witness the tile's two stored bytes *do* mean exactly what they meant —
every one of the sixteen bit positions decodes to the same value; only position
15's sample/padding status changes, which is precisely the transition the
carve-out's numeric limb expressly permits. So the general condition is satisfied
on its own byte-shaped terms, and R2 requires taking an illustration as the rule
against an express instruction not to.

**Premise of the downgrade**, stated for attack: that "meaning exactly what they
meant" is satisfied by a position whose status changes from real sample to padding
while its stored representation is unchanged. That premise is *not* free — it is
supplied by the carve-out's own numeric limb, which grants exactly that transition
for a byte. If someone reads "meaning" strictly enough that a real-sample →
padding transition changes it, then the numeric limb is the only thing that
rescues the numeric case, the general clause rescues nothing, and the packed case
has no rescue at all — which is R2 and is byte-level. I judge that reading closed
by the numeric limb's existence, but it is the crack.

**Repair:** in the three §20.3 occurrences (and, for consistency, §11.1 and
§23.1), replace "stored byte" with "stored representation", or name the three
cases as `[R-SER-05]` already does.

---

### 5. trailer-flags-valid-values-cell — diagrams-02

Verified the whole §6.2 table. Nine of ten Valid-values cells state a value
constraint; the flags cell states "bits 0–15 incompat lane; bits 16–31 ignore lane
(§6.3)" — a decomposition. **CONFIRMED**, weakly: version_minor's cell is "any
(see §6.3)", which is a value set *plus* a pointer, so the pattern the finding
relies on holds.

**Byte-level? No.** `[R-CNT-06]` normatively orders the check: a reader "MUST
validate all of the following before acting on the fields involved: **the flag
gates (§6.3)**; …". §19.1 step 2 cites `[R-CNT-08]`. So no verdict is left open by
the table's silence. Premise: that a layout table's Valid-values column is a
finding aid subordinate to the ordered-validation rule, not an independent source
of constraints. Nothing in §4.7's presentation Note contradicts that.

**Repair:** give the cell a value: "0 when created under this text; bits 0–15 clear
(§6.3)", keeping the lane decomposition after it.

---

### 6. zero-layers-entry-fused — diagrams-03

Verified §21.6's row and `[R-CNT-14]`. The row: "The file contains zero layers | A
conforming file with an empty directory". The rule: "any number of layer records
(zero is valid: an empty directory is a conforming generation); at most one
file-scope user-metadata record". A file with zero layers and one top-level
user-metadata record is conforming and its directory is not empty. **CONFIRMED.**

**Byte-level? No.** §21.1 decides which governs, in terms:

> §21.6's entries restate their governing rules on the same terms a row does, and
> where such an entry and the rule it cites diverge, **the rule governs there
> too**.

Premise: that a §21.6 entry is a restatement within the meaning of that clause.
The clause names §21.6's entries expressly, so this is not an inference.

**Repair:** cut "with an empty directory" from the Defined-behavior cell, or make
it "A conforming file; a file whose only record is a layer record's absence has an
empty directory".

---

### 7. sparse-note-index-reemission-trigger — diagrams-04

Verified §13.3's Note and §20.3 step 4. Note: "each commit that changes a layer's
stored-tile set, **or that grows its extents so that entry_count changes**,
re-emits that layer's whole tile-index region". Rule: "Every layer whose
**stored-tile set or index content** this commit changes has its tile-index region
re-emitted in full". Checked both counterexamples:

1. A shrink dropping only sentinel tiles: stored-tile set unchanged, entry_count
   falls, and §20.3 says so itself — "`[R-CNT-17]` obliges the smaller entry_count
   and so a re-emitted index region". Outside the Note's enumeration (it is a
   shrink, not a growth).
2. Removal of a planar channel with no stored tiles: §20.3 permits it ("a commit
   that moves only the ordinals of channels the superseded generation stored no
   tile for alters nothing this bars"), entry_count falls C·N → (C−1)·N. Outside
   the Note's enumeration.

**CONFIRMED.**

**Byte-level? No.** §2.1 `[R-CNF-01]`: "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*".
The block is labelled "**Note — sparse writing**". Premise: that the label governs
even where the Note states an obligation in indicative mood. `[R-CNF-01]` admits no
exception for that.

**Repair:** "each commit that changes a layer's stored-tile set or its index
content (§20.3, `[R-WRT-04]`)".

---

### 8. three-shapes-drop-only-commit — diagrams-05 — **PARTIAL**

This is the one finding I think is materially misdescribed.

Shape (c) is defined as "**A change confined to the directory** … Only the
directory is re-emitted." A drop-only commit of a PE = 0 record re-emits only the
directory and appends nothing else. It therefore satisfies (c)'s defining
sentence. The reporter rules it out of (c) via (c)'s exclusion clause:

> Editing user metadata is not this shape: its document lives in an extent
> (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack, as in
> (b).

But that clause excludes *editing*, and its stated reason is that editing **appends
a new extent**. A drop appends none, so the reason does not reach it and the
exclusion does not fire. The taxonomy is not incomplete; shape (c) covers the
case. What the reporter has actually found is that **(c)'s drawn diagram** does not
show the hatched run where the dropped extent was — the reporter says as much
("Its diagram would be (c)'s two boxes plus a hatched run"). That is a figure
defect, not a missing shape.

**Byte-level? No**, and not close: the block is labelled "**Example** — the three
shapes a commit takes", non-normative under `[R-CNF-01]`; §20.4 states the licence
("an updater MAY drop the record in any commit it is otherwise free to make — one
whose only effect is the drop included") and `[R-CNT-21]` makes the extent slack.

**Repair:** add the hatched run to shape (c)'s "after" line for the case where a
dropped record owned an extent, or name the drop in (c)'s enumeration alongside
clearing a slab declaration and renaming a layer.

---

### 9. appendix-h-flags-omission — diagrams-06

Verified Appendix H's five entries word for word. The writer entry lists seven
MUSTs and one advisory; the updater entry lists five obligations. Neither carries
`[R-CNT-08]`'s flags rules. The verifier entry does not carry them either — but it
would not, since `[R-CNF-02]` declares them not file-conformance violations. The
reporter's point that the updater entry's inherited "everything a writer does for
the bytes it produces" cannot supply the rule is right: §6.3 exempts an updater
and a compactor from the creator's flags = 0. **CONFIRMED.**

**Byte-level? No.** Appendix H is headed "(non-normative)" and disclaims in terms:
"each entry's authority is the requirement or section cited, **never this
summary**". §6.3 `[R-CNT-08]` states the obligation plainly. Premise: that a
silence in a self-disclaiming summary is not a competing reading of the rule it
summarises. I searched for any sentence making Appendix H authoritative for
anything and found none.

**Repair:** add to the writer entry "writes flags = 0 (`[R-CNT-08]`, §6.3)" and to
the updater entry "copies forward unknown ignore-lane flag bits, clearing none and
setting no other (`[R-CNT-08]`, §6.3)".

---

### 10. err04-decline-scope-enumeration — register-01

Verified `[R-ERR-04]`, `[R-COD-06]`, `[R-CNF-11]`. The tension is real:
`[R-ERR-04]` grants a decline "at the whole file, or at **the narrowest scope**
whose stated or derived quantities exceed what it can serve", while `[R-COD-06]`
says a wide window "permits a conforming reader to decline **the tile or the
layer**" and `[R-CNF-11]` names "when it declines **a layer's or a tile's** decode
on resource grounds". **CONFIRMED** as a wording defect in `[R-ERR-04]`.

**Byte-level? No**, and three sentences decide it against the exhaustive reading:

1. `[R-COD-06]` and `[R-CNF-11]` are both normative and both expressly grant the
   layer-scope decline. An enumeration in one rule does not repeal a grant in
   another.
2. §2.3 `[R-CNF-03]`: "A reader MUST accept every conforming file … **and none of
   whose values exceeds the minimum guarantees of §21's limits table**." Once a
   quantity exceeds a guarantee, the acceptance duty does not run to that file at
   all, so no scope of decline is barred.
3. §21.9's own prohibition is directed only at within-guarantee files: "Software
   that declines **on that ground** a file whose every quantity lies within the
   table is not a conforming reader".

Premise: that the Window_Size of a frame in a tile payload is a "value" of the
file within the meaning of `[R-CNF-03]`'s exceeds-clause. §21.9's per-instance
paragraph individuates that row over "the … compressed frames a file actually
contains", which makes it a §21 limits-table quantity, so I take the premise as
supplied. If it were not, argument 2 fails and only 1 and 3 remain — still enough.

**Repair:** "at the whole file, or at any scope down to the narrowest whose stated
or derived quantities exceed what it can serve: a layer, a tile, or the record
carrying a user-metadata document".

---

### 11. hard-limit-lz4-quantifier-dropped — register-02

Verified. §21.9's hard-limit clause: "a layer declaring codec 4 at decoded tile
size at most `0x7E000000` (`[R-COD-07]`)". `[R-COD-07]`: "for a layer any of whose
**addressed** tiles' decoded size exceeds 0x7E000000 bytes … in a planar layer
each channel's plane carries its own decoded size … and the largest governs". L44
carries both qualifiers. **CONFIRMED.**

**Byte-level? No.** §21.9 disclaims the restatement twice, in the same paragraph
and in the sentence introducing the list:

> The hard limits it restates are a finding aid rather than an inventory — each is
> **normative where the structure forcing it is defined**.

> They are **stated where the structures forcing them are defined**

Premise: that a restatement carrying an express, unconditional subordination
clause cannot be read as an independent norm. That is the strongest form of the
register-row-versus-rule pattern §21.1 states generally, here made explicit in
§21.9's own text.

**Repair:** "a layer declaring codec 4 at a decoded tile size of at most
`0x7E000000` over its addressed tiles (`[R-COD-07]`)".

---

### 12. experimental-entry-undercited — register-03

Verified. The §21.6 entry's Condition is scope-neutral, its Defined-behavior cell
names L25 (a sub-record row), and its Rule cell cites `[R-CNT-15]` and
`[R-WRT-08]`. `[R-CNT-15]`'s stated scope is file scope; the sub-record outcome is
`[R-CNT-18]`'s. §10.3 `[R-EXT-03]` keeps them apart expressly: "for record types,
the MU-bit outcome of `[R-CNT-15]` at file scope and `[R-CNT-18]` for layer
sub-records". **CONFIRMED** as under-citation.

**Byte-level? No.** §21.1's entry-divergence clause governs ("where such an entry
and the rule it cites diverge, the rule governs there too"), and the two rules
assign the *same* outcome to the case the entry describes — `[R-CNT-18]`: "with
MU = 0 it is ignore-record". So there is nothing for a divergence to move.
Premise: that both rules do assign ignore-record at MU = 0. I read `[R-CNT-18]`
directly to check this rather than taking the reporter's word.

**Repair:** add `[R-CNT-18]` to the Rule cell.

---

### 13. geo-rationale-omits-growth-permission — adversary-02

Verified §11.1's Rationale in full. It does state the general test correctly ("a
shrink is barred wherever it alters what §14 fixes for such a tile … and permitted
wherever it does not") and then gives three instances of "does not". It then turns
to growth only through entry_count and index re-emission, never stating §20.3's
express permission. So the omission is real. **CONFIRMED**, though weaker than the
reporter's framing: the three items are grammatically attached to "a shrink" and
presented as instances, not as an exhaustive test, and the block's later sentences
("Growth that leaves entry_count unchanged touches the directory alone") presuppose
growth is available.

**Byte-level? No.** Two sentences decide it. `[R-CNF-01]`: text "labeled … *Rationale*"
is non-normative, and the block is so labelled. And the block's own deference,
which the reporter quotes and I verified: "§20.3 states normatively, and governs,
what a commit may do to a layer that already stored tiles". Premise: that a
non-normative block's incompleteness cannot create a permitted reading of a
normative rule. That is `[R-CNF-01]`'s whole function.

**Repair:** add to the Rationale, after the shrink carve-outs, one clause: "and an
extent may grow, by the express exception §20.3 states rather than by the
carve-out".

---

### 14. renumbering-parenthetical-geometry-only — adversary-03

Verified §20.3 step 4's clause and the paragraph two below. **CONFIRMED**: the
parenthetical "(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves
them)" names one occasion, and the later paragraph reinforces it — "the
re-emission rule above, whose only stated occasion for a renumbering is a geometry
change" — after §20.3 licenses channel-declaration changes that renumber.

**Byte-level? No**, and reading (b) is not merely disfavoured but unsatisfiable.
The operative words are "every other entry byte-identical **at its disk-ordinal
position**" — the position under the new declarations. §20.3 expressly licenses the
commit that makes (b) impossible: "**Removing a planar channel de-addresses its N
tiles**" and "a commit that moves only the ordinals of channels the superseded
generation stored no tile for alters nothing this bars". `[R-CNT-17]` then forces
the new extent_length. Under (b) a licensed commit would have no emittable index
region at all. Premise: that a reading which makes an expressly licensed operation
unperformable is not a permitted reading. I checked the reporter's worked case
(planar C = 3, N = 2, remove `b`: 6 entries → 4, extent_length 4·20 + 4 = 84) and
it is right.

**Repair:** "(a geometry change, or a permitted channel-declaration change,
renumbers ordinals wherever `[R-GEO-06]` moves them)", and correspondingly widen
"whose only stated occasion for a renumbering is a geometry change" two paragraphs
below — that sentence is the one that makes the parenthetical read as closed.

---

### 15. such-a-tile-antecedent — adversary-04

Verified. The sentence is "As there, de-addressing rescues nothing: a commit that
also alters what §14 fixes for such a tile is barred", and the clause immediately
before it says the de-addressed tiles "carry no §14 obligation afterwards".
**CONFIRMED** that the antecedent is not supplied locally.

**Byte-level? No.** "As there" points at the shrink paragraph, which states the
same proposition with the antecedent spelled out:

> Dropping a tile out of the addressed set is not itself such an alteration … —
> but neither does it rescue a commit that **damages a prior-generation stored
> tile**.

So "such a tile" = a tile the layer stores in the generation this commit
supersedes, and reading (b) is refuted by the clause it directly contradicts.
Premise: that "As there" imports the earlier paragraph's formulation. The phrase
does no other work in the sentence.

**Repair:** replace "such a tile" with "a tile the layer stores in the generation
this commit supersedes".

---

### 16. ser08-returned-byte — adversary-05 — **PARTIAL**

The reporter's core claim is that `[R-SER-08]` "fixes the logical value a reader
reports … but not the byte it returns", decidable only by assembling three
passages. I checked and the document says it in one, which the reporter treats as
corroboration rather than as the answer. §19.4 step 8, verbatim:

> Return the requested values' bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`)
> — for every byte a conforming file can carry, the whole of this step
> (`[R-SER-08]` **fixes what a reader returns** for the one byte a conforming file
> cannot).

"Fixes what a reader returns" — not what it reports. With §14.2's table (0x00 =
false, 0x01 = true) and `[R-TYP-04]`'s "Wherever this specification treats two
sample or fill values as the same value, it means their encoded bytes are
identical", the returned byte is 0x01. Appendix H says the same ("the sole
resolved byte … being a nonconforming interleaved boolean it chooses to return
rather than reject"). **PARTIAL**: the residue is real — `[R-SER-08]`'s own
sentence says "MUST report 0x00 as false and every other byte as true", and
"report" is the wrong verb for a rule that fixes a return value — but the
divergence the reporter posits between two conforming readers is foreclosed.

**Byte-level? No** on the reporter's own ground as well: §14.2's first sentence
makes the byte a writer violation, T2 registers it, so `[R-CNF-05]` bars every
conforming writer from emitting the file under both readings.

The reporter's aside is also right and worth carrying: §19.4 and §21.1 both say
"the one byte" where 254 byte values qualify; §12.3's "the one case" is the
accurate form.

**Repair:** change `[R-SER-08]`'s "MUST report 0x00 as false and every other byte
as true" to "MUST return 0x00 as false and every other byte as true", and fix "the
one byte" to "the one case" in §19.4 step 8 and §21.1.

---

### 17. relies-on-two-senses — quiz-01

Verified both sentences. `[R-WRT-03]`: "the trailer and the full directory always
— **re-emission (§20.4) relies on every directory byte**". Step 2: "a violation
latent in a structure it **neither modifies nor relies on** travels with that
structure … — which is as true of an index entry copied to its disk-ordinal
position as of **a record re-emitted byte-identically**". The shelter is invoked on
a class the neighbouring rule's own definition of reliance excludes from it.
**CONFIRMED** as a terminology defect.

**Byte-level? No.** Step 2 states the case in terms and supplies its own ground
before it reaches `[R-WRT-01]`: "**Reproducing a structure's bytes unchanged is not
authoring them**: an appender satisfies its writer obligations for the bytes it
produces". And the contrast with §20.5 is deliberate and express — a compactor
"MUST refuse to compact when any check `[R-WRT-09]` obliges fails, and **MUST NOT
emit a file carrying a violation it has detected**", a clause §20.3 conspicuously
does not carry for an appender. Premise: that the appender/compactor asymmetry is
intended rather than an omission. §20.3 step 2 makes it explicit by adding "An
appender that carries a violation forward SHOULD report it", which presupposes it
may carry one forward and commit.

**Repair:** rest step 2 on its own ground and drop the appeal to `[R-WRT-01]`'s
"neither modifies nor relies on" clause — the first half of the sentence
("Reproducing a structure's bytes unchanged is not authoring them") already
supplies it — or distinguish the two senses of "relies on" where `[R-WRT-03]`
defines the verification-depth one.

---

### 18. preservation-table-stored-flags-heading — quiz-03

Verified §20.4. The three flag sources are stated; the table's column heading is
"Stored flags" and its introducing clause is "For a type the updater does not
implement, the stored flags are authoritative … and carry these obligations".
**CONFIRMED** that the heading and the introduction scope the table to one of the
three cases.

**Byte-level? No.** The lead sentence decides it and is normative:

> **Persistence governs every record type; only the authoritative source of the
> flags differs.**

"Governs every record type" is not an implication — it is the statement that the
table's obligations apply universally with the flag values varying by source.
Premise: that "persistence" in that sentence names the table's obligations
(retain / retain-with-extent / drop) rather than some looser notion. The paragraph
introduces nothing else by that name and the table is what follows it.

The reporter's further ground also holds: the class the ambiguity would reach — an
unregistered type an updater implements from an outside definition — is one this
specification does not define, so no §21 row and no register-recorded condition
turns on the difference.

**Repair:** relabel the column "Governing flags", and change the introducing clause
to "…and the table's obligations follow the governing flags, whatever their
source".

---

### 19. sec04-doubled-reverification-trigger — quiz-04

Verified verbatim in §22.3:

> which is why recovery output is re-verified as a whole file before being trusted
> (`[R-LIF-06]`) **before any use**.

The trailing phrase attaches to nothing and duplicates the trigger. And the same
obligation is stated a third time three clauses later ("which is why its output is
re-verified whole"). §22.3 carries no *Note*/*Example*/*Rationale* label, so this
is a defect in normative text. **CONFIRMED.**

**Byte-level? No.** `[R-LIF-06]` states the obligation once and cleanly: "recovery
output MUST be re-verified as a whole file (§8) before being trusted". §22.3 is a
restatement of it — the residues paragraph is expressly a discussion ("Four
residues are stated rather than defended") — and under either reading the same
whole-file re-verification is owed. Premise: that the obligation's content is
fixed by `[R-LIF-06]` and §22.3 adds none. I checked `[R-LIF-06]` directly for a
second trigger and found none.

**Repair:** delete "before any use", and collapse the second restatement ("which is
why its output is re-verified whole") into the first.

---

### 20. partial-total-causes-omit-resource-decline — verifier-02

Verified all four statements of the obligation:

- §5.2 `[R-CNT-21]`: head condition "Where the walk of §9.7 does not enumerate
  every region's claimants", then "whether because a scope-level rejection … or
  because the verifier elected under `[R-CNF-11]` to stop at the first violation".
- §9.7 `[R-LIF-08]`: "Where the walk does not complete — a scope-level rejection
  blocks enumeration, or the verifier stops at the first violation (`[R-CNF-11]`)
  — the sum is reported as partial".
- §21.6's slack row and Appendix H: the general condition alone, no causes.

And verified the third cause exists: §21.9's `entry_count` guarantee is 2³², a
layer declaring 2⁴⁰ is conforming, `[R-ERR-04]` lets a reader decline a layer, §2.3
makes a verifier a reader, and a verifier that declines the layer cannot read its
tile-index region and so cannot enumerate its stored extents. §21.9 insists such a
refusal "MUST be reported as a resource limit and **not as a validity error**", so
it is neither of the two enumerated causes. **CONFIRMED.**

**Byte-level? No**, and I make the downgrade on a sentence the reporter reached
only obliquely. §5.2, in `[R-CNT-21]` itself:

> It is not the file's slack total but a bound on it, **tightening to the exact
> total when the walk completes**.

An unmarked total therefore *claims* a completed walk. A verifier whose walk did
not complete and reports an unmarked total contradicts that sentence directly, so
reading (b) is closed by the requirement's own text and not only by its parallels.
Note that the two general restatements the reporter leans on — §21.6's slack row
and Appendix H — are both subordinate summaries (§21.1's entry-divergence clause
for the first, "(non-normative)" for the second), so they could not have carried
the downgrade alone.

**Premise of the downgrade**, for attack: that reporting a total *without* the word
"partial" is an assertion that the walk completed, rather than a neutral omission.
If a verifier's report format is such that "partial" is a positive marker whose
absence asserts nothing, the sentence above does not bite and reading (b) revives
— but even then the divergence is confined to one word in a report, and §2.4
places the slack total outside every reader obligation ("Coverage is checked by
verifiers, never by readers"), so no byte and no accept/reject verdict moves
either way.

**Repair:** in both §5.2 and §9.7, replace the two-cause enumeration with a
non-exhaustive one — "whether because a scope-level rejection ends that scope's
enumeration, because the verifier declined a scope on resource grounds
(`[R-ERR-04]`), or because the verifier elected under `[R-CNF-11]` to stop at the
first violation" — or make the clauses expressly illustrative.

---

## Coverage

24 input ids, 20 groups, each id in exactly one group. Counted twice by hand:
group 1 has 4 members, group 3 has 2, the other eighteen have 1 each —
4 + 2 + 18 = 24.

## Byte-level count

**1** — writer-01 (tile-extent permutation). No reporter's byte-level flag was
upheld except writer-01's own, and no finding the reporters graded below
byte-level was raised to it.

## What I tried hardest to kill and failed

writer-01, by six distinct routes (the §20-wide grep for `tile extent`; the
enumerated list item by item; the "list does not stand on its own" sentence; the
carve-out's contrapositive; the sample-type paragraph's parallel reasoning; and
§20.4/§20.5/§23.1/§11.1 for a prohibition elsewhere). Every route failed. The
absence of a deciding sentence is the finding.

Second-hardest: diagrams-01, which I expected to fall to the carve-out's
byte-shaped wording and which is instead saved by the general test's own words
being satisfied on the witness. I have stated the crack in that downgrade above.
