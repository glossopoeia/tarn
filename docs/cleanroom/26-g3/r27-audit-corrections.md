# Repair audit — working transcript

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../case-r27audit/hunk-01.diff` … `hunk-12.diff` (all twelve of my
  charter; `cat`'d in two batches). I did **not** read `full.diff`, did not list the
  directory, and did not open any other hunk file.
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, at these ranges:
  94–320 (§2 entire), 318–400 (§3.1–§3.3), 406–470 (§4.1–§4.4), 731–910 (§6 entire),
  939–1150 (§7.2–§7.4), 1504–1640 (§11 entire + §12 head), 1643–1700 (§12.1–§12.2),
  1869–1975 (§14.2–§14.4), 2033–2160 (§15 entire), 2158–2262 (§16 entire),
  2261–2470 (§17 entire), 2799–2870 (§19.2–§19.4 head), 2989–3210 (§20.3),
  3389–3520 (§21.1–§21.2), 3516–3573 (§21.3), 3573–3700 (§21.4–§21.6),
  3766–3862 (§21.8–§21.9), 3861–3900 (§22.1–§22.3 head), 4312–4455 (Appendix G).

Ran: `wc -l`, `grep -n "^#\{1,4\} "` for the heading map, `grep -n "R-CNT-17"`, and
three `python3` heredocs that whitespace-normalise the whole file and print ±170–220
characters of context around each occurrence of a literal fragment (this is how I
defeated the hard wrap; every phrase search below was run against the normalised
string, never line-oriented `grep`). Fragments searched: `dir_offset + dir_length`,
`extent_offset + extent_length`, `declaration-derived`, `designate`, `R-ENC-04`,
`sum or product`, `offsets plus lengths`, `R-CNT-27`, `128`, `R-COD-04`,
`stored tiles`, `addressed tiles`, `ranges over`, `Gᵢ · Tᵢ`, `Gᵢ·Tᵢ`, `overhang`,
`mod Tᵢ`, `G · T`, `high edge`, `§11.3`.

No other file was opened. I did not read docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, registry.json, git history, or the web.

**Unrequested context.** Material appeared in my context before the charter: a
project instruction file pointer (CLAUDE.md → AGENTS.md), an index of the
maintainer's memory notes with six titled entries, a user email, a date, and a
`gitStatus` block carrying the current branch and the subject lines of the five most
recent commits. That block names a round number and the subjects of several ADRs,
some of which describe the very repairs in my hunks. **I disregarded all of it.** No
conclusion below rests on it; every finding is derived from the hunk files and
`spec/tarn.md` alone, and I have not repeated its contents. Disclosing it here as
required.

---

## 1. The rule each repair adopts, in my words

- **H1 (§2.3, `[R-CNF-02]`).** A file declaring a foreign major is outside this
  document's conforming/nonconforming dichotomy *except* for the requirements
  `[R-CNF-13]` says reach it; failing one of those *is* a finding about its bytes.
- **H2 (§2.3, new `[R-CNF-13]` + Note).** A requirement reaches a foreign-major file
  iff the invariant its condition violates is one `[R-CNT-24]` fixes in every major.
  Readers must apply reaching requirements and reject on their own ground; verifiers
  report *nonconforming* on a reaching failure; everything else is not assessed.
- **H3 (§4.2, `[R-ENC-04]`).** The 2⁶³−1 ceiling binds only quantities the spec
  *expressly designates* (in the section that defines them) as declaration-derived
  sums/products. An expression written only inside a comparison and named nowhere is
  not designated and need not be formed.
- **H4 (§11.2, `[R-GEO-03]`).** N, P, the addressed-tile count and N·P are express
  designations under `[R-ENC-04]`; the former blanket "all geometry arithmetic" is
  dropped.
- **H5 (§11.3, `[R-GEO-04]`).** Padding exists on axis i iff Eᵢ mod Tᵢ ≠ 0 — the same
  predicate as the old Gᵢ·Tᵢ > Eᵢ, expressed without forming a product.
- **H6 (§17 preamble).** Every rule of §17 ranges over stored tiles; a sentinel tile
  satisfies them vacuously.
- **H7 (§17.2, `[R-COD-04]`).** Under codec 1 it is a *non-sentinel* entry's length
  that must equal the decoded size.
- **H8 (§17.2 Note).** `[R-ENC-04]` binds its designated quantities in an empty layer;
  `[R-COD-07]`'s cap does not.
- **H9 (§20.3 step 4).** Same narrowing, restated inside the growth permission.
- **H10 (§21.2 preamble).** Reach is decided by `[R-CNF-13]`; deriving it yields
  exactly F8, F14, F6 and both F1 instances; the preamble is a restatement and the
  rule governs.
- **H11 (§22.2, `[R-SEC-02]`).** Same narrowing, restated as a security property.
- **H12 (Appendix G item 5).** The filter changes stored bytes on any tile whose
  shuffle stride exceeds 1; at stride 1 it is the identity.

---

## 2. Group B first (it produced the sharpest result)

### 2.1 Does "stored" bound every rule in §17?

I enumerated §17's rules from the section text (lines 2261–2469):

| Rule | What it ranges over | Bounded by storedness? |
|---|---|---|
| `[R-COD-01]` pipeline | a stored tile's bytes | yes |
| `[R-COD-02]` independence | every stored tile | yes |
| **`[R-COD-03]` codec field value set** | **the layer's codec declaration** | **no — layer scope, L43, reader/layer access** |
| `[R-COD-04]` codec 1 length equality | non-sentinel entries | yes |
| `[R-COD-05]` deflate | stored bytes | yes |
| `[R-COD-06]` zstd | stored bytes / frame header | yes |
| **`[R-COD-07]` lz4 cap** | **"a layer any of whose *addressed* tiles' decoded size exceeds 0x7E000000"** | **no — expressly *addressed*** |
| `[R-COD-08]` exact decode | stored bytes | yes |
| **`[R-COD-09]` filter field value set** | **the layer's filter declaration** | **no — layer scope, L45** |
| `[R-COD-10]` byte-shuffle | a tile's filtered image | yes (mechanics) |
| **`[R-COD-11]` certification** | **a verifier's ability on a layer** | **no — layer scope** |

So the universal fails four ways. Two of them fork bytes.

**Corroborating passages the repair collides with (none of which it touched):**

1. §21.3, row L44 — *"Codec 4 (lz4) declared on a layer any of whose **addressed**
   tiles' decoded size exceeds 0x7E000000 bytes"*, detector reader, detected at layer
   access, governing `[R-COD-07]`.
2. §17.2's own Note, ~90 lines below the repair and **edited in this same batch**
   (hunk 8) — *"The cap is quantified over the layer's *addressed* tiles, so a layer
   that addresses none … satisfies it whatever its tile shape declares … The escape
   ends exactly when the layer's addressed-tile count rises above 0"*. Storedness is
   nowhere in that account.
3. §21.9, `[R-ERR-03]`'s paragraph, normative (not a blockquote) — *"*Decoded size of
   one tile* ranges over a layer's **addressed** tiles, stored or not, exactly as
   `[R-COD-07]`'s cap is: a tile's decoded size is a function of the layer's
   declarations alone (`[R-SER-07]`), so an addressed tile has one whether or not its
   index entry is the sentinel."* This is the flat negation of the repair's sentence,
   for the same rule.
4. §20.3 step 4 (hunk 9's own paragraph) — *"`[R-COD-07]`'s lz4 decoded-size cap among
   them (L44), which an empty layer escapes only because that cap is quantified over
   addressed tiles."*

**Is the §17 preamble normative?** Yes. It carries no requirement ID, but `[R-CNF-01]`
exempts only §1, Note/Example/Rationale-labelled text, and non-normative appendices.
The preamble is plain prose in §17, as is the owning-scope sentence it was appended
to. So this is a rule-versus-rule collision, not a row-versus-rule one, and §21.1's
"the rule governs" tiebreak does not resolve it.

**Byte-level construction (A-01).** Rank-1 interleaved layer, one float64 channel
(B = 8, §12.1), E₀ = 2²⁸, T₀ = 2²⁸. Then G₀ = 1, N = 1, entry_count = 1, P = 2²⁸,
Q = 8, decoded size P·Q = 2³¹ = 2,147,483,648 > 0x7E000000 = 2,113,929,216. Declare
codec 4. Store nothing: the single index entry is the sentinel (`FF ×16 00 ×4`), which
§21.6 records as a defined non-violation. Every other quantity is in domain (N·P = 2²⁸,
C·N = 1, extent slot addresses a 24-byte index region, L22's formula 1×20 + 1×4 = 24).

- Implementation A reads `[R-COD-07]` and L44: the layer's *addressed* tile has a
  decoded size over the cap → **reject-layer at layer access**, and `[R-CNF-05]` bars
  a conforming writer from emitting the file at all.
- Implementation B reads §17's new preamble: `[R-COD-07]` is a rule of this section,
  it ranges over stored tiles, no tile is stored, the rule is satisfied vacuously →
  **accepts the layer**, serves fill, and a writer under B emits the file.

Different bytes on disk, different accept/reject verdicts. Byte-level.

**Byte-level construction (A-02).** Same layer shape, any tile size, all entries
sentinel, `codec = 0x8000` (experimental) or `codec = 5` (reserved). `[R-COD-03]` and
L43 make this reject-layer at layer access, checkable from declarations alone; the
preamble makes it vacuous. Same fork, with `[R-COD-09]`/L45 the identical case for the
filter field. Note the preamble's word is *satisfies these rules vacuously*, which is
what does the damage: a value-set rule has no tile to be vacuous over, so the sentence
either says nothing about it (and the universal "Every rule in this section" is false)
or excuses it (and L43/L45 are dead for sparse layers). Both readings are defects.

**The charitable reading does not save `[R-COD-07]`.** One might read the preamble as
"wherever a rule of this section speaks of tiles, it means stored tiles". `[R-COD-07]`
*does* speak of tiles — and it says *addressed* ones. So the charitable reading
converts `[R-COD-07]`'s quantifier rather than leaving it alone. This is precisely
check 7's shape: "addressed" against "stored", one sentence carrying the analogy for a
whole section's worth of rules, sound for `[R-COD-01]`/`[R-COD-05]`/`[R-COD-08]` and
unsound for the next member.

### 2.2 Hunk 7 against its register row — passes

`[R-COD-04]` now: *"A **non-sentinel** index entry's length therefore MUST equal the
tile's decoded size"*. §21.4 row T14: *"Codec 1 (none) declared and a **non-sentinel**
index entry's length differs from the tile's decoded size"*, six instances, reader,
tile use, governing `[R-COD-04]`. Identical qualifier. The row already carried it; the
repair brings the rule into line with the row rather than the other way round.
**Verdict: correct, and the register needed no sweep.**

§3.1 confirms the qualifier is co-extensive with storedness: *"A tile is *stored in a
generation* if and only if that generation's tile-index entry for it is not the
sentinel (§15)."* So "non-sentinel entry" ≡ "stored tile" exactly, and hunk 7 and hunk
6's parenthetical cite the same fact consistently. `[R-IDX-02]` supplies the converse
(*"An addressed tile that is not stored has the **sentinel entry**"*). Both citations
in hunk 6 resolve and say what is claimed.

Residual note, not a finding: is a *structurally* defective entry (§15.3's six
structural rows — offset = S with length ≠ S, length 0, offset < 16, field over 2⁶³−1,
overflowing extent) a "stored" tile? By §3.1 yes, since it is non-sentinel, so
`[R-COD-04]` bites it in addition to §15.3. Both outcomes are reject-tile, so nothing
diverges; I looked for a conflict here and found none.

### 2.3 Appendix G item 5

The repair replaces *"changes the stored bytes of every tile it touches"* with
*"changes the stored bytes of any tile whose shuffle stride exceeds 1 — §17.3 makes it
the identity where the stride is 1, as for a packed boolean plane"*.

`[R-COD-10]` verbatim: *"The shuffle stride s is the channel's element size for a
planar tile and the sample stride Q for an interleaved tile (§14.2); for a packed
boolean plane s = 1 and the filter is the identity. … Viewing the image as n = L/s
consecutive groups of s bytes, the filtered image places byte i of group j at offset
i · n + j"*.

Every case that rule names:

- planar tile → s = Bᶜ. §12.1: bool/int8/uint8 have element size 1, so **a planar
  int8 or uint8 plane also has stride 1** and the filter is the identity there too.
  The repair's "as for a packed boolean plane" is exemplary ("as for"), so this is not
  wrong, only incomplete.
- interleaved tile → s = Q = Σ Bᵢ. **A single-channel uint8 interleaved layer has
  Q = 1**, likewise identity.
- packed boolean plane → s = 1, identity. Correctly named.
- The general "stride 1 ⇒ identity" claim is sound: at s = 1, n = L, i = 0, and byte 0
  of group j lands at 0·L + j = j.

**The falsifier is in the other direction, and the repair did not reach it.** Set
n = L/s = 1 — one group. Then i ranges over 0…s−1, j = 0 only, and byte i of group 0
lands at i·1 + 0 = i: the identity, **for every stride**. n = 1 means L = s, which is
reachable and conforming: interleaved with P = 1 (all Tᵢ = 1, legal — `[R-GEO-01]`
requires only Tᵢ ≥ 1) gives L = P·Q = Q = s; planar numeric with P = 1 gives
L = P·Bᶜ = Bᶜ = s. So a layer with all tile extents 1 and a float64 channel has
stride 8 > 1 and filter 2 produces byte-identical output to filter 1 on every tile.
The corrected claim's "any tile whose shuffle stride exceeds 1" is therefore still an
overclaim — the same defect class, narrowed but not closed. (A second falsifier, weaker
because content-dependent: any permutation is the identity on a constant-byte image.)

Appendix G is *"(non-normative)"* in its own heading and states *"It adds no
requirement to any actor"*, so nothing here moves bytes. But it is offered as the
factual warrant for pinning the filter, and the warrant as written is false for a
reachable, conforming layer shape.

---

## 3. Group A — the overflow ceiling

### 3.1 Hunk 5 is genuinely equivalent, at every value

Old: *"Where Gᵢ · Tᵢ > Eᵢ"*. New: *"Where Eᵢ mod Tᵢ ≠ 0"*. With Gᵢ = ⌈Eᵢ/Tᵢ⌉ and
Tᵢ ≥ 1 (`[R-GEO-01]`, so the modulus is defined):

- Eᵢ mod Tᵢ ≠ 0 ⇒ Gᵢ = ⌊Eᵢ/Tᵢ⌋ + 1 ⇒ Gᵢ·Tᵢ = Tᵢ⌊Eᵢ/Tᵢ⌋ + Tᵢ > Eᵢ. ✓
- Eᵢ mod Tᵢ = 0 ⇒ Gᵢ = Eᵢ/Tᵢ ⇒ Gᵢ·Tᵢ = Eᵢ, not >. ✓
- Degenerate Eᵢ = 0: 0 mod Tᵢ = 0 ⇒ no padding; old form Gᵢ = 0, 0 > 0 false. ✓
- Degenerate 0 < Eᵢ < Tᵢ: Eᵢ mod Tᵢ = Eᵢ ≠ 0 ⇒ padding; old Gᵢ = 1, Tᵢ > Eᵢ. ✓
  (§11.1 already calls this "a single padded tile along that axis".)

Equivalent everywhere. And the repair *fixes a live defect*: under the old
`[R-ENC-04]` ("any quantity this specification defines as a sum or product"), Gᵢ·Tᵢ
was such a product, and Gᵢ·Tᵢ can exceed 2⁶³−1 on a perfectly sane layer — Eᵢ = 2⁶³−1,
Tᵢ = 2⁶², gives Gᵢ = 2 and Gᵢ·Tᵢ = 2⁶³ — which the old text made a reject-layer.

**Sweep check:** normalised search for `Gᵢ · Tᵢ`, `Gᵢ·Tᵢ`, `G · T` → 0 hits each. The
old form survives nowhere. §11.2's Example ("extents (1000, 2048) … the last row of
tiles is padded") reads correctly under the new form (1000 mod 256 = 232 ≠ 0). The
`(§4.2)` citation resolves: §4.2 is "Integer types and domains" and now contains the
"no reader is obliged to form it" clause the parenthetical leans on. **Clean.**

### 3.2 Hunk 4's narrowing — what it drops, and whether that matters

Dropped: *"like all geometry arithmetic"*. Kept: N, P, addressed-tile count (N or C·N),
N·P, all now expressly designated in the section that defines them, exactly as the
repaired `[R-ENC-04]` demands of a designation.

What §11 still derives that is now undesignated: §11.4's ordinals
(s = Σᵢ tᵢ·∏_{j>i}Gⱼ, in-tile Σᵢ uᵢ·∏_{j>i}Tⱼ, disk c·N + s) and the partial products
inside them. I checked domination: with every Gᵢ ≥ 1, ∏_{j>i}Gⱼ ≤ N; s ≤ N−1;
c·N + s ≤ C·N − 1; in-tile ordinal ≤ P−1. All dominated by designated quantities.
L2's row already says this explicitly — *"C·N (which dominates the max disk ordinal
(C−1)·N + (N−1))"*. Where some Gᵢ = 0 the layer addresses no tile, so no ordinal is
ever formed. **The drop is safe for ordinals.** It is not safe for §19.3 — see 3.4.

### 3.3 What the "designation is express" clause leaves stranded

I enumerated every sum/product the document derives from file integers and asked, of
each, whether it is *expressly designated by the section that defines it*:

| Quantity | Designating text | Designated? |
|---|---|---|
| N, P, addressed count, N·P | §11.2, hunk 4 | yes |
| Q, Fᶜ, P·Q, P·Bᶜ, offsets of value k | §14.2 `[R-SER-02]`: *"These products and sums are declaration-derived quantities under `[R-ENC-04]`"* | yes |
| decoded sizes, V | §14.3 `[R-SER-07]`: *"Every decoded size, and the value count V, is a declaration-derived quantity under `[R-ENC-04]`"* | yes |
| index entry offset + length | §15.2 `[R-IDX-02]` names `[R-ENC-04]`'s sum rule; §15.3's table row *"offset + length overflows"* | yes |
| record extent_offset + extent_length | §7.2 `[R-CNT-13]`: *"or an **overflowing sum** is a validity error"* | yes (and independently grounded) |
| **dir_offset + dir_length** | §6.2's table cell *"≥ 4; dir_offset + dir_length ≤ F − 64"*; `[R-CNT-06]`'s *"dir_offset + dir_length ≤ F − 64"*; §6.4 and §19.1's fetch range | **no — written only inside comparisons and a fetch interval, named nowhere** |
| **entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4** | `[R-CNT-17]`'s *"extent_length MUST equal …"* (a comparison); §15.1's layout diagram, which sits inside a `>` block and is therefore non-normative | **no** |

Both stranded expressions are named as **instances of register rows whose governing
rule is `[R-ENC-04]`**: F3 (*"dir_offset + dir_length; non-layer top-level record
extent_offset + extent_length"*) and L2 (*"… entry_count × 20 + ⌈entry_count/2¹⁶⌉ ×
4"*). §21.1: *"each row *restates* its governing rule, and where a row and the rule it
cites diverge, **the rule governs**"* — so after the repair these two instances restate
nothing, while §21.8 still commissions a corpus vector for each
(*"one vector per instance"*).

**Not byte-level, and here is why I say so.** Take the disputed file for F3's first
instance: `dir_offset + dir_length > 2⁶³−1`. `[R-ENC-03]` caps committed_file_length at
2⁶³−1 and `[R-CNT-06]` forces committed_file_length = F, so `dir_offset + dir_length ≤
F − 64 < 2⁶³−1` is already a MUST; the file violates `[R-CNT-06]` and is caught by F10
at the same tier (reader, open). It is nonconforming under both readings, so
`[R-CNF-05]` bars it either way and the emittable set does not move. Same for L2's
index-region instance: an entry_count whose region size overflows admits no
extent_length that satisfies `[R-CNT-17]`, so L22 fires at layer access under both
readings. The defect is a register that has been left overclaiming, not a fork.

**One further wrinkle in the repaired sentence itself.** `[R-ENC-04]`'s own parenthetical
still glosses the covered class as *"(offsets plus lengths, grid counts, tile counts,
sample-position counts, ordinals)"*. `dir_offset + dir_length` is an offset plus a
length. The parenthetical says it is in; the express-designation sentence says it is
out. And the operative restrictor **"declaration-derived"** is nowhere defined in this
document — I searched: it occurs only in `[R-ENC-04]`, `[R-GEO-03]`, `[R-SER-02]`,
`[R-SER-07]`, `[R-SEC-02]` and L2, always as a used term, never as a defined one, and
§3.1's term list does not carry it. On its most natural reading ("derived from a
layer's declarations") it excludes trailer and record arithmetic a second time over.

### 3.4 The restatement that was not swept — §19.3

The repair swept four restatements: §11.2 (hunk 4), §17.2's Note (hunk 8), §20.3 step 4
(hunk 9), §22.2 (hunk 11). Searching `R-ENC-04` across the normalised document turns up
one more, and it is the only one that is itself a numbered requirement:

> §19.3, `[R-RDR-03]`: *"…the geometry floor and its arithmetic (`[R-GEO-01]`–
> `[R-GEO-03]`), the 2⁶³ − 1 ceiling on **every quantity that arithmetic derives**
> (`[R-ENC-04]`) and on the decoded sizes §14 derives from it (`[R-SER-02]`,
> `[R-SER-07]`)…"*

Repaired `[R-ENC-04]`: *"any quantity this specification **designates** a
declaration-derived sum or product"*. "Every quantity that arithmetic derives" is
strictly wider than "every quantity it designates" — that is the whole content of the
repair — and §19.3 is the layer-access checklist an implementer works from. Because
both are numbered requirements, §21.1's row-versus-rule tiebreak does not apply; there
is no tiebreak at all.

The divergence bites exactly where hunk 4 dropped "all geometry arithmetic": on
intermediates of a designated product. Construction: rank-3 interleaved layer, one
uint8 channel, T = (1, 1, 1), E = (2⁴⁰, 2⁴⁰, 0). Then G = (2⁴⁰, 2⁴⁰, 0), and every
designated quantity is tiny — N = 0, P = 1, N·P = 0, C·N = 0, Q = 1, P·Q = 1,
entry_count = 0, extent slot (0, 0), crc_of_crc_array = 0. `[R-GEO-02]` and §21.6 make
the zero extent a defined non-violation, `[R-ENC-03]` passes on every field
(2⁴⁰ ≤ 2⁶³−1). But the arithmetic of `[R-GEO-03]` that derives N passes through
G₀·G₁ = 2⁸⁰.

- Implementation A follows repaired `[R-ENC-04]`: G₀·G₁ is not a designated quantity,
  N = 0 is, N = 0 is in range → **accepts the layer**, serves no samples.
- Implementation B follows `[R-RDR-03]` as written and checks the ceiling on every
  quantity that arithmetic derives → **reject-layer at layer access**, and a writer
  reading B concludes `[R-CNF-05]` bars the file.

I record the strongest defence of the repair: one can read `[R-RDR-03]`'s clause as a
mere pointer to `[R-ENC-04]` ("the ceiling that rule imposes, over whatever it
reaches"), in which case nothing diverges; and one can argue ∏Gᵢ has one value, 0, and
the partial product is an artifact of evaluation order. Neither defence is in the text.
`[R-ENC-04]`'s excusing clause is scoped to *"an expression this specification writes
only inside a comparison"*, which does not describe a partial product of a designated
product, so the repaired rule does not settle intermediates either way — and §19.3
settles them the old way. I mark this byte-level, on the narrow ground that two
competent implementations differ on the accept/reject verdict for the file above.

**§21.3's L2 carries the same wide form** — *"A declaration-derived sum or product of a
layer exceeds 2^63 − 1"*, with no "designates". It was not swept. Because §21.1 makes
the rule govern a row, L2 is subordinate; I fold it into the F3/L2 finding rather than
counting it twice.

**Passes I confirmed in this group.** Hunks 9 and 11 restate the narrowed rule
faithfully: "every quantity it designates" and "Every declaration-derived sum and
product `[R-ENC-04]` designates" both range over the same set as "any quantity this
specification designates". Hunk 8 sits in a `>` block and is therefore non-normative,
but it changes no rule — it contrasts `[R-COD-07]`'s *addressed-tile* quantifier with
`[R-ENC-04]`'s designation quantifier, and the contrast is sound for both P·Q and P·Bᶜ,
each designated by `[R-SER-02]` and each a function of declarations alone, hence formed
in a layer that addresses nothing. I tested the analogy on each of the two quantities
separately, as check 7 demands, and both hold. §22.2's surrounding claim — *"Three
properties bound what a hostile file can make a reader spend"* — still holds under the
narrowing: the index amplifier the section's Note names is tied down by `[R-CNT-17]`
and `[R-CNT-13]`, not by `[R-ENC-04]`.

---

## 4. Group C — reach

### 4.1 Deriving the membership myself

`[R-CNT-24]` fixes, in every format major version: (i) trailer magic at F−64;
(ii) version_major and version_minor at F−56; (iii) CRC-32C at F−4 over
[F−64, F−4); (iv) the front signature block is constant; (v) the trailer is not
grown. That leaves 64 − 8 − 4 − 4 = 48 trailer bytes, [12, 60) in trailer coordinates,
free for a future major.

Row by row across §21.2's 36 conditions, asking only "is the invariant this condition
violates on that list?":

- **F1** — front-block bytes [0,8) reversed; trailer magic at F−64 reversed. Both on
  the list, (iv) and (i). **Reaches, both instances.**
- **F6** — the 16-byte front block not byte-identical. (iv). **Reaches.**
- **F8** — the 8 bytes at F−64 not the trailer magic. (i). **Reaches.**
- **F14** — u32 at trailer offset 60 ≠ CRC-32C of trailer [0,60). Offset 60 = F−4;
  [0,60) = [F−64, F−4). (iii) exactly. **Reaches.**
- F2, F9–F13, F15–F17 — every field they read (dir_offset, dir_length, generation,
  committed_file_length, file_id, reserved[56,60)) lies in the redefinable 48.
  **Do not reach.**
- F5 — asserts F ≥ 128. Not on the list; the floor is built from a ≥4-byte directory at
  offset ≥16 and a 64-aligned F, which are format major 1's. **Does not reach.**
- F3, F4, F7, F18–F36 — every one governs a structure this text defines for major 1
  (directory, records, extents, flags, layer names). **Do not reach.**

So the reaching set is {F1 (both instances), F6, F8, F14} — **exactly what the new
preamble names, and nothing else.** The exhaustive claim "and no other row" survives
falsification. The old preamble's "four rows" named the same four. **Membership: correct.**

Citation spot-checks in hunk 2's Note, all of which resolve:
- `[R-CNT-27]` — verbatim *"No conforming file is shorter than 128 bytes: the front
  signature block, a directory of at least 4 bytes at an offset of at least 16, and the
  64-byte trailer at a 64-aligned offset cannot be satisfied in fewer."* The Note's
  characterisation is faithful. ✓
- F15's Governing rule cell does cite `(R-CNT-24)`, as the Note says, and its bytes
  [56,60) are inside [12,60). ✓
- F14's CRC coordinates check out as computed above. ✓

Hunk 10's warrant phrase, compared word for word: the preamble says the four rows are
*"each asserting an invariant `[R-CNT-24]` fixes in every major"*; `[R-CNF-13]` says
*"the invariant its condition violates is one `[R-CNT-24]` fixes"*. "Assert" and
"violate" are duals over the same object, and `[R-CNF-13]`'s second sentence uses
"asserted" itself. **The analogy passes.**

### 4.2 The granularity mismatch

`[R-CNF-13]`'s subject is a **requirement**: *"A **requirement** of this specification
**reaches** a file … when, and only when, the invariant **its condition** violates …"*,
closing *"**Every other requirement** of this specification governs a structure this
text defines for format major 1 alone; it is not assessed…"*. §21.2's preamble and the
hunk-2 Note both apply the test at **row** granularity: *"Which **rows** reach…"*,
*"§21.2's F14 reaches…"*, *"F5 does not reach…"*, *"F15 does not reach…"*.

The two granularities are not interchangeable, and one requirement makes that concrete.
`[R-CNT-06]` is the governing rule of **ten** §21.2 rows: F8, F9, F10, F11, F12, F13,
F14, F15, F16, F17. Two of them reach; eight do not. `[R-CNT-06]`'s own text is a
single ordered list of conditions — *"the trailer magic; the trailer CRC; the version
gate … and then … the flag gates; committed_file_length …; dir_offset ≥ 16;
dir_length ≥ 4; … reserved bytes zero"*.

So: is `[R-CNT-06]` a reaching requirement? It is certainly not one of the "other
requirements" that govern major-1-only structure — two of its conditions assert
`[R-CNT-24]` invariants. Then *"A reader MUST apply every reaching requirement to a
file whatever major it declares"* obliges a reader to apply **all** of `[R-CNT-06]` to
a major-7 file, including dir_offset ≥ 16 and reserved-bytes-zero — which is precisely
what §21.2's preamble ("no other row") and the Note ("F15 does not reach") deny. There
is no reading on which both survive: the rule quantifies over requirements, the
restatement over rows, and `[R-CNT-06]` splits.

Not byte-level. Every foreign-major file is reject-file under both readings — on
`[R-CNT-06]`'s ground under one, on `[R-CNT-07]`'s capability ground under the other —
and no conforming writer under this text emits a foreign major at all
(version_major = 1, §6.2). What forks is a verifier's *verdict word*
(*nonconforming* versus *cannot establish*) and a reader's diagnostic, neither of which
is a byte or an accept/reject verdict.

### 4.3 "MUST apply" against `[R-CNT-04]`'s "MAY defer or omit"

`[R-CNF-13]`: *"A reader MUST apply every reaching requirement to a file whatever major
it declares … the distinct diagnostic `[R-CNT-07]` asks for is owed where **every
reaching requirement is satisfied** and the declared major is one the reader does not
implement."*

`[R-CNT-04]` is a reaching requirement (it governs F6 and F1's front-block instance).
Its text: *"A reader that would have to issue a further range request to obtain those
bytes **MAY defer or omit the check**: its open path is anchored at the trailer (§6.2),
and the two-request accounting of §6.4 does not include the front block."*

A remote reader that lawfully omits the front-block check has *not* established that
every reaching requirement is satisfied, so under `[R-CNF-13]`'s literal condition the
distinct diagnostic is not owed to it — while `[R-CNT-07]` states that SHOULD
unconditionally (*"the diagnostic for an unimplemented major SHOULD be distinct from
both 'not a TARN file' and 'corrupt'"*), and §6.4's whole accounting exists to spare
that reader the fetch. The condition `[R-CNF-13]` attaches is undecidable for exactly
the reader `[R-CNT-04]` exempts.

The old §21.2 preamble carried this qualification in terms — *"F6 with F1's front-block
instance, which `[R-CNT-04]` places before other processing for a reader that already
holds those bytes, **one that would have to fetch them being free to defer or omit the
check**"* — and the new preamble drops it. F6's Condition cell still states the
exemption, so the information is not lost from the register; what is new is the flat
"MUST apply" in `[R-CNF-13]` with no carve-out. Not byte-level, for the reason in 4.2.

### 4.4 Decidability for a row the register does not yet hold

The charter's hard question. `[R-CNT-24]`'s list is closed and short, so for a *new*
row the test is mechanical **provided its condition asserts one invariant**. It does
not always. F5 is the standing proof: its condition (F < 128) asserts a conjunction
built from a fixed ingredient (a 64-byte trailer at F−64 and a 16-byte front block, both
`[R-CNT-24]`'s) and major-1 ingredients (dir_length ≥ 4 at dir_offset ≥ 16, F ≡ 0 mod
64). `[R-CNF-13]` says "**the** invariant its condition violates", presupposing exactly
one, and gives no rule for decomposing a conjunction. The document resolves F5 — and
F14, and F15 — only in the **Note**, which is a `>` block and therefore non-normative
by `[R-CNF-01]`; and §21.2's preamble, the other place the answer appears, expressly
demotes itself (*"where this restatement and that rule diverge, the rule governs"*).
So the normative answer for a conjunctive condition has to be re-derived from a rule
that does not supply a decomposition rule.

I considered reporting this as a check-3 finding (a rule whose only statement is inside
a `>` block). I decided it is not one: the Note *explains* three determinations rather
than *making* them, and the reaching set is stated normatively in §21.2's preamble even
though that preamble is a restatement. What survives is the under-determination itself,
and it is subsumed by the granularity finding in 4.2 — both come from `[R-CNF-13]`
attaching "the invariant" to the wrong unit. I record it here and do not double-count
it as a separate finding.

I also checked the degenerate end: a 32-byte file declaring major 7. F8 and F14 cannot
be evaluated (F−64 < 0); F1 and F6 can be, and pass if the front block is right; F5
does not reach. So no reaching requirement fails and none can be checked — the file is
neither conforming nor nonconforming and a verifier owes *cannot establish*. Consistent
with `[R-CNF-11]`, which I opened: *"An established violation takes priority … and
*cannot establish* is available only to a traversal that established no violation."*
No defect, but worth the maintainer knowing the boundary is real.

### 4.5 Hunk 1

Cites `[R-CNF-13]`, which exists (hunk 2 adds it) and says what is claimed. I checked
the passage it lands in for a sentence written to be true only under the old wording.
The bullet's opening — *"File conformance is a pure predicate on bytes … It is always
conformance to a stated format major version"* — now coexists with a verifier reporting
*nonconforming* on a file whose stated major this document does not define. That is
coherent on `[R-CNF-13]`'s own reasoning (*"the invariant broken is one that major
shares"*), and §21.6's *"the file can be perfectly conforming under that major"* is
undisturbed. `[R-CNF-11]`'s *cannot establish* machinery is likewise consistent:
established violation beats inability to check, which is exactly the priority
`[R-CNF-13]` asserts. **No finding.**

---

## 5. Check-by-check summary of what passed

1. **Tense/quantifier.** Passes for hunks 4, 5, 7, 8, 9, 11 (each compared against the
   rule it restates, quoted above). Fails for hunk 6 (stored vs addressed, §17
   preamble against `[R-COD-07]`) and for hunk 2 (requirement-granular vs row-granular).
2. **Citations.** `[R-CNF-13]`, `[R-CNT-24]`, `[R-CNT-27]`, `[R-CNT-07]`, `[R-CNT-04]`,
   `[R-CNT-06]`, `[R-IDX-02]`, `[R-COD-10]`, `[R-ENC-04]`, `[R-CNF-11]`, §3.1, §4.2,
   §6.2, §6.3, §14.2, §14.3, §21.1, §21.6, §21.9 — all opened, all say what the
   repairing sentence claims. No citation defect found.
3. **Repair sits in normative text.** Hunks 1, 2 (rule half), 3, 4, 5, 6, 7, 9, 10, 11
   are in normative text. Hunk 2's Note and hunk 8 are `>` blocks — but neither is the
   sole statement of any rule (the reaching set is stated normatively in §21.2's
   preamble; `[R-ENC-04]` and `[R-COD-07]` state their own quantifiers). Hunk 12 is a
   non-normative appendix by design. **No orphaned-rule defect.**
4. **Contradiction in the same passage.** Two found, both in §17: the preamble against
   `[R-COD-07]`+L44+the section's own Note+§21.9, and the preamble against
   `[R-COD-03]`/`[R-COD-09]`+L43/L45. One found across passages: `[R-RDR-03]` against
   the narrowed `[R-ENC-04]`. One found in §2.3: "MUST apply" against
   `[R-CNT-04]`'s "MAY defer or omit".
5. **Exhaustive claims.** Audited: "Every rule in this section" (§17 — **fails**);
   "and no other row" (§21.2 — holds, derived independently in 4.1); "every quantity it
   designates" (§20.3 — holds); "Every declaration-derived sum and product" (§22.2 —
   holds); "any tile whose shuffle stride exceeds 1" (Appendix G — **fails** at n = 1);
   "36 conditions" (§21.2 — F1…F36, correct); "the two capability refusals §21.6 names"
   (§21.9, untouched — §21.6 does name exactly two, holds).
6. **What is left unconstrained.** For §4.2 the structure is "sums and products the
   document derives from file integers"; I enumerated all of them (table in 3.3) and
   two are now unclaimed by any designation while their register rows still cite
   `[R-ENC-04]`. For §17 the structure is the (codec, filter) declaration pair plus the
   stored payload; the repair's scope statement governs the payload half and mis-scopes
   the declaration half. For §11.2 the sibling quantities are §11.4's ordinals, which I
   verified are dominated by designated quantities.
7. **Analogy quantifiers, word for word.** Recorded at 2.1, 2.3, 3.4 and 4.1. The one
   that fails is hunk 6's, and it fails per-member exactly as the charter predicts:
   sound for `[R-COD-01]`, `[R-COD-05]`, `[R-COD-08]`; unsound for `[R-COD-07]`,
   `[R-COD-03]`, `[R-COD-09]`, `[R-COD-11]`.

Findings A-01 … A-07 follow in the structured result.
