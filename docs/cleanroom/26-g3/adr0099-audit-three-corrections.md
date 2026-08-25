# Repair audit — case-adr0099, hunks 01/02/03

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../case-adr0099/hunk-01.diff`, `hunk-02.diff`, `hunk-03.diff` (my charter's three hunk files, and only those).
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — ranges 106-112, 172-190, 545, 591-612, 1000-1100, 1440-1640, 1740-1800, 2030-2110, 2116-2250, 2300-2350, 2828-2845, 2885-3090, 3255-3275, 3339-3345, 3418-3530, 3600-3665, 3748, 4178, plus grep-driven single lines.

Ran (all against `spec/tarn.md` only):

- `grep -n "entry_count" spec/tarn.md`
- `grep -n "R-GEO-06\|R-GEO-05\|R-GEO-07" spec/tarn.md`
- `grep -n "R-WRT-04" spec/tarn.md`
- `grep -n "R-SLB-03\|R-SLB-02\|R-SLB-04\|R-SLB-01\|R-SLB-05" spec/tarn.md`
- `grep -n -i "grid boundary\|grid count\|grid counts" spec/tarn.md`
- `grep -n "zero-extent\|empty layer\|Empty layers\|addresses no tile\|addresses none" spec/tarn.md`
- `grep -n "L44" spec/tarn.md`
- `grep -n "first growth\|its length\|previous stored tile" spec/tarn.md`
- `grep -n "R-CNF-01\|R-CNF-05" spec/tarn.md`
- a Python whitespace-normalising scan of the whole file (hard-wrap-safe) for the phrases
  `tile-index region`, `re-emit`, `grows its extents`, `grow`, `entry_count`, `addressed-tile count`,
  printing +/-90 chars of context and the source line number for every hit. This is the search I
  relied on for cross-document restatements, because the document is hard-wrapped and a
  line-oriented grep for e.g. "grows its extents so that entry_count" cannot match.

Did NOT read: `full.diff`, any hunk file other than my three, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, git history,
the web. Did not list the case directory.

**Unrequested context that appeared before I began:** the runtime placed a project instruction
pointer (`CLAUDE.md` -> `AGENTS.md`) and an index of the maintainer's personal memory files in my
context, listing note titles about this project's working cadence, its register, and prior
verifier failures. I did not open any of them and I have not used anything they suggested; every
conclusion below is traced to a line of `spec/tarn.md` or to one of my three hunk files. I disclose
their appearance because the access rule requires it.

---

## 1. The three hunks as landed, verified against the current file

`sed -n '1466p;1493,1506p;1748p;1788,1796p;2146p;2156,2166p'` confirms all three "nearest preceding
heading" annotations in the hunk headers are correct:

- hunk 1 lands at 1493-1506, under `#### 11.1 Geometry and its validity floor` (line 1466). It is
  inside the `> **Rationale.**` blockquote that starts at line 1484.
- hunk 2 lands at 1788-1796, under `#### 13.3 Unstored tiles read as fill` (line 1748). It is
  inside the `> **Note — sparse writing.**` blockquote.
- hunk 3 lands at 2156-2163, under `#### 16.2 The slab declaration` (line 2146). It is in the
  **normative** paragraph carrying `[R-SLB-03]` (line 2177) — no `>` prefix.

`[R-CNF-01]` (line 106-112) reads: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative." So hunks 1 and 2 have **no normative force** and hunk 3 does.

### Rule each repair adopts, in my words

**Hunk 1.** For a commit that grows a layer's extents, the two-way split is by whether the layer
record's `entry_count` field changes. If it does not, the commit rewrites the layer record only —
no tile bytes, no index bytes. If it does, `extent_length` changes with it, so the layer's whole
tile-index region is written out again at a new place, and every stored tile's disk ordinal that
`[R-GEO-06]`'s formula moves is renumbered. A growth that pushes one grid count up while some other
grid count is still 0 is in the first bucket (the product stays 0); the growth that lifts the final
remaining zero grid count is in the second.

**Hunk 2.** A commit re-emits a layer's whole tile-index region if it changes the layer's
stored-tile set, or if it grows the layer's extents in a way that changes `entry_count`. (Growing
extents *without* changing `entry_count` no longer triggers the claim.)

**Hunk 3.** In a slab run, the packing relation is
`offset[k] = offset[k-1] + length[k-1]` over the run's stored tiles in ordinal order — the *previous*
tile's length, not the current tile's.

---

## 2. Hunk 3 first (it is the only normative one)

### 2.1 The passage in full (lines 2146-2177)

```
#### 16.2 The slab declaration

A layer MAY declare a slab run length S >= 1 with slab alignment A_slab, ... [R-SLB-02]

When declared, for every run: the run's stored tiles are contiguous
and packed in ordinal order — each stored tile's offset equals the
previous stored tile's offset plus that previous tile's length — and
the first stored
tile's offset satisfies offset mod A_slab = 0. The runs themselves
are not mutually ordered or joined: between runs, placement freedom
(`[R-SLB-05]`) governs, and the bytes left between them are slack
(§5.2), which writers SHOULD zero. Sentinel tiles are transparent to run continuity: they
occupy no bytes and do not break packing. So are the entries §15.3
classifies reject-tile on a *structural* ground: they address no
usable extent, and the run's stored tiles close over them. An entry
whose only defect is that its stored bytes fail its crc is not
transparent — its offset and length stand, and the packing relation
reads them as it does any other stored tile's — so this invariant
stays decidable from the index entries alone, given the committed
file length §15.3 already requires to classify any entry. A run with no stored
tiles
imposes nothing. A verifier MUST
check these invariants (violation: reject-layer, §15.3); readers are
not obligated to, and MAY instead detect contiguity arithmetically
from any index segment. `[R-SLB-03]`
```

### 2.2 Which antecedent makes the rule satisfiable

The pre-repair text was "each stored tile's offset equals the previous stored tile's offset plus
its length". Two antecedents for "its":

- *previous tile's length*: `off[k] = off[k-1] + len[k-1]`. Offsets strictly increase (a stored
  tile has `length >= 1`: §15.3's table row "length = 0 (non-sentinel) | *structural*: reject-tile
  — absence is spelled sentinel; no codec emits zero bytes"), extents abut with no gap and no
  overlap. Satisfiable, and it is what "contiguous and packed in ordinal order" means.
- *this tile's length*: `off[k] = off[k-1] + len[k]`. This lays each tile's bytes at an offset
  determined by its own length, which for a run of three tiles of lengths 10, 20, 30 starting at
  1000 gives offsets 1000, 1020, 1050 — the first tile then occupies [1000,1010) and [1010,1020) is
  a gap, i.e. the run is *not* packed. It only coincides with packing when all lengths are equal.
  So this reading contradicts the same sentence's own "contiguous and packed".

The repair picks the first. Correct.

### 2.3 Against the register row that restates it

§21.3, line 3522:

```
| L41 | Inside a slab run, a stored tile's offset ≠ the previous stored tile's offset plus the
previous stored tile's length (gap, overlap, or out-of-ordinal placement; sentinels and entries
§15.3 classifies reject-tile on a structural ground are transparent, an entry failing only its
stored bytes' crc is not) | gap; overlap; out-of-ordinal placement | verifier | certification |
`[R-SLB-03]` (R-IDX-03) |
```

Row and rule now say the same thing word for word — "the previous stored tile's offset plus the
previous stored tile's length" against "the previous stored tile's offset plus that previous tile's
length". §21.1's precedence question (rule governs over row) does not arise: they agree. **Pass.**

### 2.4 Against the arithmetic the surrounding passage states

- `[R-SLB-02]`, line 2150-2155: "Runs partition each contiguous block of disk ordinals
  independently: for an interleaved layer the single block [0, N); for a planar layer each channel
  block [c·N, (c+1)·N) — runs never span channel blocks, and the final run of a block can cover
  fewer than S ordinals. Run r of a block starts at ordinal block_start + r·S." Ordinal arithmetic,
  untouched by the pronoun; consistent.
- §16.2's Example (lines ~2231-2240): "If ordinal 10 is a sentinel, run 1's stored tiles are 8, 9,
  11…15, packed with no gap where 10 would have been." "no gap" is only true under the
  previous-tile's-length reading. Consistent.
- §15.3 / `[R-IDX-03]`, line 2046: "`[R-SLB-03]`'s run continuity closes over it as it does over a
  sentinel" and "its extent stands and it keeps its place in the *verifier* rows, in run
  continuity, and in the coverage walk". The repaired sentence's own follow-on — "its offset and
  length stand, and the packing relation reads them as it does any other stored tile's" — now has a
  coherent referent: tile k-1's length is what places tile k. Under the discarded reading this
  sentence was nearly meaningless. **The repair makes the neighbouring sentence work.**
- §20.5 compactor, line 3259: "free to place structures anywhere §5.2 admits and every declared
  layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)". No arithmetic restated; consistent.

### 2.5 Seven checks on hunk 3

1. **Tense/quantifier.** The rule is stated over the live committed state, not over a transition;
   "for every run", "each stored tile", "the first stored tile". This *is* the normative rule (not
   a restatement of one), so there is no upstream quantifier to match — I say so per the charter.
   The quantifier is unchanged by the repair: only the possessive changed. Pass.
2. **Citations.** The repaired sentence itself carries no citation. The paragraph cites
   `[R-SLB-05]` (verified, line 2117-2127: placement freedom for layers declaring neither alignment
   nor slab — correct as the governing rule *between* runs), §5.2 (slack), §15.3 (verified, lines
   2036-2070, includes the structural rows and the committed file length F). Pass.
3. **Sits in normative text.** Yes: line 2156-2163 has no `>` prefix and the paragraph ends
   `[R-SLB-03]`. Grepping the distinctive words (`previous stored tile`, hard-wrap-safe) returns
   exactly two hits: line 2159 (the rule) and line 3522 (L41). Both normative. Pass.
4. **No contradiction in the same passage.** Read the whole of §16 (2116-2245). The three
   transparency carve-outs (sentinels; structurally reject-tile entries; *not* crc-failing entries),
   "A run with no stored tiles imposes nothing", "The runs themselves are not mutually ordered or
   joined", `[R-SLB-04]`'s re-establish-or-clear, and the two Notes and Example are all consistent
   with `off[k] = off[k-1] + len[k-1]`. `[R-CNT-16]` (A and S mutually exclusive) and `[R-SLB-01]`
   (per-tile alignment) do not interact. No contradiction found.
5. **Exhaustive claims.** "for every run" — qualified by "A run with no stored tiles imposes
   nothing" and by the transparency sentences; sound. "each stored tile's offset" — the first
   stored tile has no previous, and is handled by the "and the first stored tile's offset satisfies
   offset mod A_slab = 0" clause; sound. "the first stored tile" — a run has at most one; sound.
   No count, no closed list. Pass.
6. **What else is unconstrained?** Structure = one slab run. Its members: (a) the set of stored
   tiles in [block_start + r·S, block_start + (r+1)·S) — fixed by `[R-SLB-02]` and the index; (b)
   each stored tile's offset — pinned by the repaired relation and by the A_slab clause for the
   first; (c) each stored tile's length — pinned by §15's entry and `[R-SER-07]`'s exact-size rule,
   not by §16; (d) the run's ordinal span S — pinned by `[R-CNT-23]`'s table row (1 <= S <= 2^63-1)
   and L1/L2; (e) A_slab — pinned by `[R-CNT-23]` (power of two, 1..2^62; 0 iff S=0) and rows L28,
   L29; (f) bytes between runs — deliberately unconstrained slack, `[R-SLB-05]`, §5.2; (g) bytes
   after a run's last stored tile — same. I found **no sibling quantity of this structure left
   unpinned by accident.** Notably the "sibling" that could have been missed — the *ordering*
   half of "contiguous and packed in ordinal order" — is in fact entailed by the repaired relation,
   because stored lengths are >= 1 (§15.3), so offsets strictly increase with ordinal; L41's
   "out-of-ordinal placement" instance is therefore reachable from the repaired sentence alone.
7. **Analogy.** The repaired sentence contains no "exactly as", "the same way", "as X is",
   "following", "likewise", "transposed from", "for the same reason". Nearest thing is the
   *neighbouring* (untouched) "the packing relation reads them as it does any other stored tile's";
   its two verbs are "reads ... its offset and length" against the repaired rule's "equals the
   previous stored tile's offset plus that previous tile's length" — both range over the run's
   stored tiles in ordinal order, so the comparison holds. Reported per instruction even though it
   passes.

**Hunk 3: no finding.**

---

## 3. Hunk 1 — §11.1's Rationale

### 3.1 The full Rationale as landed (lines 1484-1503)

```
> **Rationale.** Empty layers serve schema-first workflows: declare
> layers at creation, grow extents as data arrives. §20.3 states
> normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: a
> shrink is barred wherever it alters what §14 fixes for such a
> tile — whether or not the new state still stores it — and permitted
> wherever it does not: a tile dropped out of the addressed set
> carries no §14 obligation and its extent becomes slack, a tile the
> superseded generation did not store carries none either, and a new
> padding position whose stored byte already holds the fill alters
> nothing. One shrink can do several of these at once. A layer that stored nothing may be re-declared
> freely. Growth
> that leaves **entry_count** unchanged touches the directory alone —
> a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another
> stays 0 among them, the product holding at 0. Growth that changes
> entry_count changes extent_length with it (`[R-CNT-17]`), so the
> layer's whole tile-index region is re-emitted and disk ordinals
> renumber wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`) —
> the growth that raises a zero-extent layer's **last** zero grid
> count included.
```

### 3.2 Deriving the partition for myself

Definitions used (all §11.2, `[R-GEO-03]`, line 1507-1515):
G_i = ceil(E_i / T_i); N = prod G_i; **addressed-tile count** = N interleaved, C·N planar, and it
is "the number of its tile-index entries (§15)".
§7.4's table (line 1021): `entry_count | u64 | equals the addressed-tile count (§11.2, [R-CNT-17])`.
So under any conforming file, `entry_count` = N or C·N.

"Growth" = extents E_i only increase (§20.3 line 3029: "an extent MAY **grow**"). G_i is
non-decreasing in E_i, so under growth each G_i is non-decreasing and N is non-decreasing. C is not
an extent, so growth leaves C fixed.

- If `entry_count` is unchanged, N is unchanged (C fixed, C >= 1). If N_after > 0 then every
  G_i_after > 0; with G_i_before <= G_i_after and equal products, every G_i is unchanged. If
  N_after = 0 then N_before = 0 and some G_j = 0 both before and after, while other G_i may have
  risen.
- So branch 1 is exactly the union of two cases: **(a)** every grid count unchanged (growth inside
  existing tiles), **(b)** the product is pinned at 0 by a still-zero grid count.
- Branch 2 is everything else, i.e. N strictly increases.

Consequence check, branch 1(a): grid counts unchanged means the index has the same entries, at the
same disk ordinals (`[R-GEO-06]`: s = sum t_i · prod_{j>i} G_j depends only on the G_j; planar
c·N + s depends only on N). Stored tile bytes are untouched — the only thing that changes about
them is that some padding positions become real, which §20.3 licenses explicitly ("a position that
becomes real held that channel's fill and fill is a legal sample value"), and which changes no
byte. §20.3 step 4: "A layer whose record alone changes keeps its extent slot, pointing at the
existing region". So: directory alone. **Holds.**

Consequence check, branch 1(b): entry_count = 0 both generations, so extent slot (0,0) and
crc_of_crc_array = 0 (§7.4, `[R-CNT-23]`; §15.4's Note line 2105: "At entry_count = 0 there is no
region at all"). There is nothing but the layer record to touch. **Holds.**

I could construct **no case falling in neither branch** (the partition is by a single scalar's
equality, hence exhaustive) and **no case in a branch whose consequence fails** — I tried slab
declarations (`[R-SLB-04]` triggers on stored-tile set / run partition / byte placement changes;
branch 1 changes none of them, since N is unchanged so the block [0,N) and [c·N,(c+1)·N) partitions
are unchanged), per-tile alignment (`[R-SLB-01]`, unchanged offsets), and `[R-COD-07]`'s lz4 cap
(quantified over addressed tiles; in 1(a) P = prod T_i is unchanged, in 1(b) there are still no
addressed tiles).

Consequence check, branch 2: `[R-CNT-17]` gives extent_length = f(entry_count) with
f(n) = 20n + ceil(n/2^16)·4, and f(n+1) - f(n) >= 20 > 0, so f is strictly increasing and
entry_count changing forces extent_length to change. §20.3 step 4 then obliges re-emission
("Every layer whose stored-tile set or index content this commit changes has its tile-index region
re-emitted in full — entry_count entries plus the segment CRC array — necessarily at a new
placement"), and "(a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)" is
verbatim the same claim as the Rationale's second half. **Holds.**

### 3.3 The trailing case

"the growth that raises a zero-extent layer's **last** zero grid count included."

Needed: name a growth that is in branch 2 and might be doubted. For a layer with at least one zero
extent, N = 0 and entry_count = 0. Any growth that leaves at least one G_i at 0 keeps entry_count
at 0 (branch 1(b)). entry_count therefore leaves 0 **exactly** when the final zero grid count is
lifted. So the case named is in branch 2, and — read as "the last remaining one" — it is the *only*
growth of such a layer that is in branch 2. The word "included" makes an inclusion claim, not an
exhaustiveness claim, so no overclaim there.

But "last" has a second available reading in this document. §11.4 uses "last" positionally: "1 =
row-major — the **last-declared** dimension varies fastest". Under the positional reading, "a
zero-extent layer's last zero grid count" is the highest-indexed dimension whose grid count is 0.
For a rank-3 layer with E = (0, 100, 0), T = (4, 4, 4): the positionally-last zero grid count is
G_2. Raising E_2 to 100 gives G = (0, 25, 25), N = 0, entry_count still 0 — **branch 1, not branch
2, so the sentence is false under that reading.** The intended reading ("the last remaining") is
recoverable, but the superseded text's "the first growth of a zero-extent layer" was temporal, and
replacing "first" with "last" in a document that also uses "last" for declared order is exactly the
kind of swap that reads as verified. → **finding A-02.**

### 3.4 The em-dash appositive in branch 1

"Growth that leaves **entry_count** unchanged touches the directory alone — a growth raising one
grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among them, the product holding at 0."

The appositive is a bare verbless noun phrase with no exemplification marker ("for instance", "as
when", "e.g."). Read as an example it is correct — it names case (b) of my derivation. Read as a
specification of the branch (which is the ordinary force of a dash-appositive restating the
preceding subject) it says branch 1 *is* the zero-product case, and thereby excludes case (a),
growth inside existing tiles with every grid count unchanged. Case (a) is the common case and the
superseded text stated it as the branch's headline ("growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉
(§11.2) unchanged touches the directory alone"); after the repair it appears nowhere in §11.1.
"among them" also has no plural antecedent in the sentence — "them" must reach implicitly to the
layer's grid counts, which are not mentioned as a set. → **finding A-03** (non-normative, low
severity; the normative statement of case (a) survives at §20.3 step 4, "A layer whose record alone
changes keeps its extent slot").

### 3.5 Restatements elsewhere — the sweep

Hard-wrap-safe scan for `grow`, `grows its extents`, `entry_count`, `tile-index region`, `re-emit`,
`grid count`. Every restatement of the "what does a growth touch" rule:

- line 605-610 (§5/§6 Example, non-normative): "A commit that changes a layer's stored-tile set or
  index **content** re-emits that layer's whole tile-index region as well, at a new placement
  (§20.3, `[R-WRT-04]`)." Keys on the normative condition, not on grid counts. Correct, needed no
  sweep.
- line 2988-2995 (§20.3 step 4, normative, `[R-WRT-04]`): the governing statement, quoted above.
  Keys on "stored-tile set or index content". Correct.
- line 3061-3062 (§20.3, normative): "`[R-CNT-17]` obliges the smaller entry_count and so a
  re-emitted index region" — the shrink direction, already keyed on entry_count. Consistent with
  the repair.
- line 3084-3085 (§20.4 Note): "any change to a layer's stored-tile set re-emits that layer's whole
  tile-index region". Narrower but true.
- line 3033-3034 (§20.3, normative): "`[R-COD-07]`'s lz4 decoded-size cap among them (L44), which
  an empty layer escapes only because that cap is quantified over addressed tiles." True, and makes
  no durability claim.
- **line 2336-2343 (§17.2 Note, non-normative) — NOT swept:**

```
> **Note.** The cap is quantified over the layer's *addressed* tiles,
> so a layer that addresses none — any dimension extent 0
> (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape
> declares, and codec 4 is conforming there. The escape is not
> durable: a later commit that grows an extent addresses tiles, and
> the same declarations are then measured against the cap.
```

  "a later commit that grows **an** extent addresses tiles" is the very proposition hunk 1 just
  refined at §11.1 and hunk 2 refined at §13.3, and it is stated here in the pre-repair, imprecise
  form. Its own escape condition is "**any** dimension extent 0", so it covers layers with two or
  more zero extents; for those, growing *an* extent addresses no tile at all (N = prod G_i holds at
  0), the layer still has zero addressed tiles, and `[R-COD-07]`'s cap is still escaped. The escape
  ends only when the last zero grid count is lifted — which is precisely the phrase hunk 1
  inserted twelve sections earlier. → **finding A-01.**

### 3.6 Seven checks on hunk 1

1. **Tense/quantifier.** The repair speaks about a *transition*: "Growth that leaves entry_count
   unchanged", "Growth that changes entry_count". Both generations are implicated, which is what
   the subject requires, and both are conforming states, so `[R-CNT-17]` binds in each — which is
   what makes the extent_length inference go through. The set ranged over is "growths of one
   layer's extents", matching §20.3's "an extent MAY **grow**". The repair is **not** the normative
   rule; the normative rule it describes is §20.3 step 4 (`[R-WRT-04]`), quoted at 3.2, whose
   quantifier is "**Every** layer whose stored-tile set or index content this commit changes". The
   repair's branch-2 antecedent ("Growth that changes entry_count") is a strict subset of that
   ("index content changes"), so the repair claims less than the rule licenses — sound direction.
   Pass.
2. **Citations.** `[R-CNT-17]`: opened at line 1038-1042 — "Under index_encoding 1, extent_length
   MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0); a mismatch,
   or an entry_count that does not equal the geometry-derived addressed-tile count, is a validity
   error at layer scope." Supports "changes entry_count changes extent_length with it", given
   strict monotonicity and given that index_encoding 1 is the only legal value (§7.4 table row:
   "any other value ... is a validity error at layer scope"). **Pass.**
   §11.2: opened at 1507-1515; defines ⌈Eᵢ / Tᵢ⌉ as the grid count and N = prod G_i. **Pass.**
   `[R-GEO-06]`: opened at 1563-1576; the ordinal formulas depend on the G_j and on N, so
   "renumber wherever `[R-GEO-06]` moves them" is exactly right (a rank-1 growth, for instance,
   moves none). **Pass.**
   §20.3: opened at 2940-3081; step 4 carries the re-emission rule. **Pass.**
   `[R-WRT-04]`: the identifier terminating §20.3's numbered procedure at line 3081, so it does
   govern steps 1-6 including step 4. **Pass.**
3. **Sits in normative text.** It does not — it is inside a `> **Rationale.**` block, which
   `[R-CNF-01]` strips of force. That is acceptable here **only because** the rule it describes is
   independently normative at §20.3 step 4 and that normative text does *not* say the old thing:
   §20.3 never keyed on grid counts, it keys on "stored-tile set or index content", which is
   correct under both the old and new wordings. Checked by hard-wrap-safe scan for `grid count`
   (8 hits, lines 403, 1064, 1475, 1479, 1497, 1507, 1563, 3044) — none of them is a normative
   re-emission trigger. So the repair did not fail to land; there is no stale normative twin.
   Pass, with the residual noted in A-01 (a stale non-normative twin does exist).
4. **No contradiction in the same passage.** Read the whole Rationale (1484-1503) and both rules of
   §11.1 (`[R-GEO-01]` 1470-1477, `[R-GEO-02]` 1479-1482). The earlier half of the Rationale is
   about shrinks and carries three carve-outs ("a tile dropped out of the addressed set carries no
   §14 obligation", "a tile the superseded generation did not store carries none either", "a new
   padding position whose stored byte already holds the fill alters nothing") plus "A layer that
   stored nothing may be re-declared freely". None of them collides with the growth sentences: the
   growth branches make no claim about what is *permitted*, only about what is *touched*, so
   there is no widened licence to collide with a narrowing carve-out and no MAY that lets an actor
   violate a MUST. `[R-GEO-02]`'s "its grid count is 0, the layer has zero addressed tiles, its
   tile index has zero entries" is what branch 1(b) relies on and agrees with it. No contradiction
   found in the passage.
   (The one thing the passage now lacks is a positive statement of case (a) — an omission, not a
   contradiction; that is A-03.)
5. **Exhaustive claims.** "touches the directory **alone**" — falsification attempted in 3.2
   against slabs, per-tile alignment, the lz4 cap, `[R-ENC-04]`'s products, and padding-position
   changes; survives. "unchanged"/"changes" — a genuine two-way partition on a scalar, exhaustive
   by construction. "the product holding at 0" — correct: prod G_i = 0 iff some G_i = 0, and
   entry_count = C·N with C >= 1, so entry_count = 0 iff N = 0. "the **last** zero grid count" —
   see A-02. "included" — an inclusion claim; verified true. No count and no closed list appears.
6. **What else in this structure is unconstrained?** Structure = the layer record's geometry-derived
   quantities that a commit's growth can move (§7.4's table, lines 1006-1023). Enumerating every
   member: `name` (no), `layout` (not by growth), `linearization` (fixed at 1), `codec`/`filter`
   (not by growth), `A` / `S` / `A_slab` (not by growth, but `[R-SLB-04]` reacts to a run-partition
   change, which a branch-2 growth causes via N), `rank d` (no), `C` (no), the d dimension entries
   — **E_i moves, T_i does not** — the C channel entries (no), `index_encoding` (fixed at 1),
   `entry_count` (**named by the repair**), `crc_of_crc_array` (**moves in branch 2 and the repair
   does not name it**), and the extent slot's `extent_offset` (**moves in branch 2 — re-emission is
   "necessarily at a new placement" — and the repair names only extent_length**).
   Assessment: `crc_of_crc_array` and `extent_offset` are both pinned normatively elsewhere —
   §7.4's table and `[R-CNT-23]` for the former, §20.3 step 4's "necessarily at a new placement
   (`[R-LIF-01]`)" and §20.5's "updates the layer-record fields covering a regenerated region
   (crc_of_crc_array)" for both — so nothing is left *unconstrained*; the Rationale is merely not
   exhaustive, which a Rationale need not be, and it does not claim to be (branch 2 says "so the
   layer's whole tile-index region is re-emitted", not "so only extent_length changes"). I record
   the enumeration rather than a finding.
   One genuine gap in coverage, recorded and judged non-defective: a re-declaration of an
   unstored layer that changes T_i or C (permitted by the immediately preceding sentence, "A layer
   that stored nothing may be re-declared freely") moves entry_count without any *growth*, so it
   falls outside both branches. The branches are explicitly scoped to "Growth", so this is silence,
   not error, and §20.3 step 4's "index content" trigger governs it normatively.
7. **Analogy.** The repair uses no "exactly as / the same way / as X is / likewise / transposed
   from / for the same reason". Its one warrant-by-pointing is the parenthetical `[R-CNT-17]`
   behind "changes extent_length with it". Verbs side by side:
   - repair: "Growth that **changes** entry_count **changes** extent_length with it" — ranges over
     an ordered pair of generations of one layer.
   - `[R-CNT-17]`: "extent_length **MUST equal** entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4" —
     ranges over a single state of one layer.
   Different sets (transition vs. state), but the repair does not import the cited rule's
   quantifier; it derives a transition fact from the cited rule holding in each of the two states,
   which `[R-CNF-05]` ("A writer MUST emit only conforming files") guarantees. The derivation needs
   f strictly increasing, which it is. The analogy carries **one** claim, not several, so there is
   no member-by-member test to run. **Pass**, and reported per instruction.

---

## 4. Hunk 2 — §13.3's "sparse writing" Note

### 4.1 Are the old and new conditions the same condition?

Old: "grows its extents **across a grid boundary**" = some G_i increases.
New: "grows its extents **so that entry_count changes**" = N (hence C·N) increases.

Not the same. Some G_i can increase while N stays 0 — a rank-2 layer at E = (0, 0), T = (4, 4)
growing to E = (1000, 0) has G going (0,0) -> (250,0), so a grid boundary is crossed and
entry_count stays 0. The new condition is **strictly narrower**, and the difference is exactly
the case hunk 1's em-dash names. Conversely, entry_count cannot change under growth without some
G_i changing (N = prod G_i), so the new condition is a proper subset of the old.

### 4.2 Which condition does the normative text use?

§20.3 step 4, `[R-WRT-04]`, line 2988: "Every layer whose stored-tile set **or index content** this
commit changes has its tile-index region re-emitted in full". Neither "grid boundary" nor
"entry_count" — but the two map cleanly:

- growth with entry_count changing => the region gains entries => index content changes => the
  normative rule obliges re-emission. The new Note **agrees** with the normative text.
- growth across a grid boundary with N pinned at 0 => entry_count 0 before and after => "At
  entry_count = 0 there is no region at all — zero segments, a zero-byte CRC array, extent slot
  (0, 0) and crc_of_crc_array = 0" (§15.4's Note, line 2105) => no index content and nothing to
  re-emit. The **old** Note demanded re-emission of a region that does not exist; the new one does
  not. The repair fixes a real over-claim.

### 4.3 Seven checks on hunk 2

1. **Tense/quantifier.** "each commit that changes a layer's stored-tile set, or that grows its
   extents so that entry_count changes" — universal over commits, per-layer, and it speaks about
   the transition (correctly: "changes", "grows"). The normative rule it restates is §20.3 step 4,
   quoted above, quantified "**Every** layer whose stored-tile set or index content this commit
   changes". Repair's antecedent ⊂ rule's antecedent; consequent identical ("re-emits that layer's
   whole tile-index region" vs "has its tile-index region re-emitted in full"). The repair is a
   restatement, not the rule. Pass.
2. **Citations.** §11.1 — opened (1466-1503). The only §11.1 text supporting the claim is the
   Rationale of hunk 1, i.e. non-normative; `[R-GEO-01]` and `[R-GEO-02]` say nothing about
   re-emission. The citation therefore points at a companion Note rather than at authority. This
   is *unchanged by the repair* (the pre-repair line carried the same "(§11.1, §20.3,
   `[R-WRT-04]`)"), both endpoints are non-normative anyway, and §20.3/`[R-WRT-04]` in the same
   parenthesis do carry the rule — so I record it as a weak citation, not a defect introduced
   here. §20.3 — opened, correct. `[R-WRT-04]` — opened at line 3081, terminates §20.3's procedure,
   correct. `[R-IDX-05]` (adjacent, untouched) — line 2095 area, the all-sentinel segment CRC
   constant; correct. **All resolve.**
3. **Sits in normative text.** No — `> **Note — sparse writing.**`, non-normative under
   `[R-CNF-01]`. Acceptable for the same reason as hunk 1: §20.3 step 4 states it normatively and
   states it in a form that neither the old nor the new Note contradicts. Checked that no normative
   sentence anywhere still uses the discarded "across a grid boundary" trigger — hard-wrap-safe
   scan for `grid boundary` returns **zero** hits in the whole document, so the discarded phrasing
   is fully retired. Pass.
4. **No contradiction in the same passage.** Read §13.3 entire (1748-1796): `[R-TYP-08]`,
   `[R-TYP-09]`, the fill Example, the Rationale, the padding Note, and this Note. `[R-TYP-09]`'s
   "Fill is produced by exactly one condition" and the padding Note's carve-out are about read
   semantics and do not touch re-emission. No sentence in §13.3 was written to be true only under
   "across a grid boundary". No contradiction found.
5. **Exhaustive claims.** "each commit that ... re-emits" — universal; falsification attempted by
   looking for a commit satisfying the antecedent that need not re-emit: none, since both disjuncts
   entail §20.3's "stored-tile set or index content" trigger. No "only", "never", "always", no
   count, no closed list. The Note does **not** claim its two disjuncts are the only triggers, and
   that matters, because they are not: a free re-declaration of an unstored layer changing T_i, C,
   or layout also moves entry_count and forces a new region, and neither disjunct names it. Since
   the sentence is phrased as an implication rather than a biconditional, this is not an overclaim
   — and it is not a regression either, the old wording having the same gap. Pass.
6. **What else is unconstrained?** Structure = the commit's effect on one layer's tile-index
   region. Members: the entry array (entry_count × 20 bytes), the segment CRC array
   (⌈entry_count/2¹⁶⌉ × 4 bytes) — both named collectively by "whole tile-index region", and §20.3
   step 4 spells them out — the extent slot (offset and length: §20.3 "necessarily at a new
   placement"), and the layer record's crc_of_crc_array (§20.5's parenthetical; §7.4's table). The
   Note names the region as a whole, so it does not pin one member and leave a sibling loose. No
   finding.
7. **Analogy.** No "exactly as / the same way / likewise / following / for the same reason". The
   parenthetical "(§11.1, §20.3, `[R-WRT-04]`)" is a citation, not an analogy; the verb comparison
   is nevertheless: repair "**re-emits** that layer's whole tile-index region" against §20.3's
   "has its tile-index region **re-emitted** in full". Same verb, same object, same set (one layer
   per commit). Pass; reported per instruction.

**Hunk 2: no finding.** It is a correct narrowing that brings the Note into agreement with §20.3
and with hunk 1.

---

## 5. Contradictions and restatements I looked for and did not find

- No normative sentence anywhere keys re-emission on grid counts or on "grid boundary" (0 hits).
- No second copy of the slab packing relation beyond L41, which agrees with the repair.
- §21.1's rule-over-row precedence never has to be invoked for L41.
- §21.6's "A dimension has extent 0 | A valid, empty layer: zero addressed tiles, an empty index,
  reads returning no samples | `[R-GEO-02]`" agrees with hunk 1's branch 1(b).
- §19.3's read algorithm (2828-2845) treats a zero-extent layer as returning no samples; consistent.
- §20.5's compactor text (3259-3275) is consistent with the disambiguated packing relation.
- §21.9's `entry_count 2³²` limit row and §21.3's L1/L2/L21/L22/L27 rows are all consistent with
  entry_count = addressed-tile count.

## 6. Findings

**A-01 — §17.2's Note still carries the pre-repair form of the rule hunk 1 just refined.**
(unswept restatement; byte-level.)

**A-02 — "the growth that raises a zero-extent layer's *last* zero grid count" is false under the
declared-order reading of "last".** (new ambiguity; not byte-level.)

**A-03 — the em-dash appositive in branch 1 is unmarked as an example, and the case the superseded
text made the branch's headline is now stated nowhere in §11.1.** (new ambiguity / partial
undershoot; not byte-level.)

Full text of each is in the structured result.
