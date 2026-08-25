# Repair audit — four hunks, r26b

Auditor working transcript. Artifact of record.

## 0. Disclosure

Read: the four charter hunk files
(`hunk-01.diff` … `hunk-04.diff` under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/f4334f8b-602f-4a50-9c17-a97272554180/scratchpad/r26bAudit/`),
and `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.

Nothing else. No `docs/`, no ADRs, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no
`AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history, no
`full.diff`, no other hunk file. I did not list the audit directory. I ran
`wc`, `sed -n`, `grep -n`, `tr '\n' ' ' | grep -o` against `spec/tarn.md`
only.

**Unrequested context.** Before I began, my runtime placed in context a
project instruction file pointer (`CLAUDE.md` → `AGENTS.md`) and an index of
the maintainer's personal memory notes naming several TARN-specific
memory files, plus environment/date/git-status boilerplate including a list
of recent commit subject lines. I did not open any of those files, and I have
disregarded their contents as evidence. I note in particular that the git
status block named recent commit subjects; I did not use them to steer the
audit and reached every conclusion below from the specification text. This is
a disclosed exposure, not a disclosed act.

**Hunk-file header defect (not a spec defect, reported here for the record).**
The `#` comment header of `hunk-01.diff` says it "lands at spec/tarn.md line
1289, in §11.1's growth Rationale (non-normative)", and `hunk-02.diff` says it
lands "in §9.6's recovery-scan note". The two descriptions are swapped
relative to the diff bodies and to the file. Verified: line 1289 of
`spec/tarn.md` is inside §9.6 (heading `#### 9.6 Recovery scan (not a reader
behavior)` at line 1287), and line 1489 is inside §11.1's `> **Rationale.**`
block (heading `#### 11.1 Geometry and its validity floor` at line 1447). I
audited by body, not by header. Hunk 1 = §9.6, **normative prose**. Hunk 2 =
§11.1 Rationale, **non-normative blockquote**. The line numbers in the headers
are correct; only the section/nature labels are transposed.

---

## Hunk 1 — §9.6, line 1299: register-row citation for a bad trailer

### The change

```
-bytes handed over (§21.2 rows F8 and F17), and the earlier state the
+bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
+trailer CRC and the length cross-check), and the earlier state the
```

### The rule the repair asserts

Not a rule about implementations directly. It asserts a mapping: the set of
§21.2 rows that register the failure of a file whose final 64 bytes are not a
valid trailer is exactly {F8, F14, F17}, and those correspond to the magic
gate, the trailer-CRC gate, and the committed_file_length-vs-file-size gate.

### Deriving the correct list from the source, not the diff

§9.6 defines its own notion of a valid trailer candidate, one sentence
earlier (lines 1290–1293):

> "probe backward at 64-aligned offsets o for the trailer magic; on a match,
> require the trailer CRC to verify and committed_file_length = o + 64."

Three criteria: **magic**, **trailer CRC**, **committed_file_length = o + 64**.
For the file as handed over, the final 64 bytes begin at o = F − 64, so the
third criterion is committed_file_length = F.

Mapping each to §21.2 (lines 3444, 3450, 3453 read in full):

| criterion | row | row text | verdict |
|---|---|---|---|
| magic | F8 | "The 8 bytes at F-64 are not exactly the trailer magic 8A 4E 52 41 54 0D 0A 1A … `[R-CNT-06]`" | correct |
| trailer CRC | F14 | "The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes [0,60) … `[R-CNT-06]` (R-CNT-20, R-ENC-09)" | correct |
| length | F17 | "Trailer committed_file_length does not equal the transport-authoritative file size … `[R-CNT-06]` (R-LIF-04, R-CNT-10)" | correct |

The derived list is {F8, F14, F17}. The repaired citation is {F8, F14, F17}.
**Nothing missing; nothing named wrong.** The pre-repair list omitted F14, the
CRC row — that is exactly the gap closed.

### Check 2 — citations resolve

- `[R-CNT-06]` (§6.2, lines 782–790). Opened and read in full. Its gate list
  is: "the trailer magic; the trailer CRC; the version gate (§6.3) … and then
  … the flag gates (§6.3); committed_file_length equals the file size (for a
  remote reader, the size reported by its transport) and is a multiple of 64;
  dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
  1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes zero. Any failure is
  reject-file." The three the repair names are all in it, and the first two are
  the first two in mandated order. **PASS.**
- §21.2 (line 3417 onward) — is the file-scope table. **PASS.**
- Rows F8, F14, F17 — quoted above, all three exist and say what is claimed.
  **PASS.**
- §9.7 / `[R-LIF-08]` (cited in the untouched context) — §9.7 begins line 1316
  and is the coverage-verification section; consistent. **PASS.**
- `[R-CNT-06]` also cited at line 1298 in the same sentence — same rule.
  **PASS.**

### Check 1 — tense and quantifier

Quantifier: "a file whose final 64 bytes are not a valid trailer". Universal
over files, present tense, ranges over *the bytes handed over* — the sentence
says so explicitly ("on the bytes handed over"). This is the right set: the
whole point of the passage is that the probe's finding about an *earlier*
commit state is not a verdict about the artifact presented. No generation
confusion: "the earlier state the probe finds is a different artifact".
**PASS.**

### Check 3 — the repair sits in normative text

Line 1289 is plain prose, no `>` prefix, inside §9.6, whose paragraph
terminates in `[R-LIF-06]` (line 1314). Normative. The repaired clause is a
parenthetical citation inside a normative sentence, which is the right place
for it. **PASS.**

### Check 4 — contradiction in the same passage

I read §9.4 (line 1244) through §9.7's first paragraph (line 1330) entire.
The competing statement I went looking for is the §9.5 Note at lines 1274–1281:

> "**Note.** Residue past a completed commit carries no register row of its
> own. A reader meets it as a trailer that fails its gates — the magic, the
> CRC, or committed_file_length against the transport size, each of which
> §21.2 already registers …"

That Note names **the same three gates in the same order**. Before this
repair, §9.6 named two and the Note named three — the divergence. After it,
they agree. So this repair does not create a contradiction; it removes one.
`[R-LIF-05]` (line 1271, "MUST NOT scan backward") is untouched and still
consistent — §9.6 opens "never conforming readers on the default path".
**PASS.**

### Check 5 — exhaustive claims

The list is presented as closed ("rows F8, F14 and F17 — the magic, the
trailer CRC and the length cross-check"). I tried three falsifiers:

1. **A file under 64 bytes.** F5 (line 3441, "File size is below the 128-byte
   minimum … `[R-CNT-27]` (R-CNT-01, R-CNT-06)") registers it, and F8 cannot be
   evaluated because there are no bytes at F−64. *Defused:* such a file has no
   "final 64 bytes", so it does not satisfy the sentence's antecedent. Not a
   counterexample. I am not reporting this.
2. **F = 1000, valid magic, valid CRC, committed_file_length = 1000.** All
   three named criteria hold, yet the file fails `[R-CNT-06]` at F13
   (committed_file_length not a multiple of 64). This is the *converse*
   direction — the sentence claims not-valid ⇒ fails-gates, not
   fails-gates ⇒ one of these three rows. Not a counterexample.
3. **A 64-byte file that is nothing but a plausible trailer.** Fails F5 and
   F10, but again its final 64 bytes *are* valid by the three criteria.
   Converse direction again. Not a counterexample.

Within the sentence's own antecedent, the triple is exhaustive: failing "not a
valid trailer" means failing at least one of magic / CRC / length, and each
maps to exactly one named row. **PASS.**

### Check 6 — what is still unconstrained in this structure

Structure: the 64-byte trailer and the gate set §21.2 registers over it. I
enumerated every field of the trailer from the §6.2 table (lines 740–752) —
magic, version_major, version_minor, flags, generation, dir_offset,
dir_length, committed_file_length, file_id, reserved[56,60), trailer CRC — and
checked each has a row:

| field | row(s) |
|---|---|
| magic | F1, F8 |
| version_major | F18 |
| version_minor | (descriptive; `[R-CNT-07]` forbids rejecting on it) |
| flags | F19 |
| generation | F2, F11 |
| dir_offset | F9, F2 |
| dir_length | F16, F10, F2 |
| committed_file_length | F13, F17, F2, F5 |
| file_id | F12 |
| reserved [56,60) | F15 |
| trailer CRC | F14 |

No sibling quantity of this structure is left ungoverned. The repair
constrained a citation, not a quantity, so there is no "one of two quantities"
exposure here. **PASS.**

### Check 7 — argument by analogy

The repaired text contains no "exactly as / the same way / as X is / following
X" construction. The nearest thing is the appositive gloss "— the magic, the
trailer CRC and the length cross-check", which is a naming of the three rows,
not a transposition of one rule's quantifier onto another. For completeness I
compared the two governing verbs anyway:

- Repair: "a file whose final 64 bytes **are not a valid trailer** fails
  `[R-CNT-06]`'s gates **on the bytes handed over**".
- §9.5 Note: "A reader **meets it as a trailer that fails its gates** — the
  magic, the CRC, or committed_file_length against the transport size".

Both range over the file the reader is holding, present tense, no generation
shift. Same set. **PASS.**

### Hunk 1 verdict: clean. No finding.

---

## Hunk 2 — §11.1 Rationale, line 1499: an exception to the growth claim

### The change

```
-> extent_length (`[R-CNT-17]`), so the layer's whole tile-index region
+> extent_length (`[R-CNT-17]`) — save where another dimension's grid
+> count is 0, which holds the product at 0 and adds no entry — so where
+> it does change, the layer's whole tile-index region
```

### The sentence as it now stands (lines 1496–1503, verbatim)

> "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the
> directory alone; growth that raises one changes entry_count and with it
> extent_length (`[R-CNT-17]`) — save where another dimension's grid count is
> 0, which holds the product at 0 and adds no entry — so where it does change,
> the layer's whole tile-index region is re-emitted and disk ordinals renumber
> wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`) — the first growth of
> a zero-extent layer included."

### The rule the repair asserts

That raising one grid count does **not** change entry_count when some *other*
dimension's grid count is 0, because entry_count is derived from the product
N = ∏ Gᵢ, and a zero factor pins the product at 0.

### Constructing the case (the exception is real)

Rank-2 layer, E = (0, 100), T = (10, 10). §11.2 (`[R-GEO-03]`, line 1517):
Gᵢ = ⌈Eᵢ/Tᵢ⌉, so G = (0, 10); N = ∏ Gᵢ = 0. `[R-GEO-02]` (line 1466): "A
dimension with extent 0 is valid: its grid count is 0, the layer has zero
addressed tiles, its tile index has zero entries". Grow E₂ from 100 to 200:
G₂ rises 10 → 20 — a grid count is raised — and N = 0 · 20 = 0. §11.2's
addressed-tile count is "N for an interleaved layer and C · N for a planar
layer", so entry_count stays 0 either way. **The exception is real.** The
pre-repair sentence was false for this case.

### Check on scope — does the exception swallow more than intended?

entry_count = N or C·N with N = ∏ Gᵢ. Raising Gₖ from a to b (b > a) leaves the
product unchanged **iff** ∏_{i≠k} Gᵢ = 0, i.e. iff some other Gⱼ = 0. So
"another dimension's grid count is 0" is exactly the carve-out — no more, no
less. For rank 1 there is no "another dimension", and indeed N = G₁ always
changes. **No overshoot, no undershoot in the carve-out itself.** The ordinary
case (all other grid counts nonzero) still reads true.

### Check 2 — citations resolve

- `[R-CNT-17]` (line 1039–1042): "Under index_encoding 1, extent_length MUST
  equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is
  0); a mismatch, or an entry_count that does not equal the geometry-derived
  addressed-tile count, is a validity error at layer scope." Supports both
  "changes entry_count and with it extent_length" (the formula is strictly
  increasing in entry_count) and the carve-out (entry_count 0 ⇒ extent_length
  0). **PASS.**
- §11.2 for ⌈Eᵢ/Tᵢ⌉ (line 1508 heading, definition at 1517). **PASS.**
- `[R-GEO-06]` (lines 1563–1576): defines spatial and disk tile ordinals,
  s = Σᵢ tᵢ · ∏_{j>i} Gⱼ and c·N + s. Renumbering under a grid-count change is
  exactly what this formula does. **PASS.**
- §20.3 / `[R-WRT-04]` step 3 (lines 2985–2998): "Re-emit … necessarily at a
  new placement (`[R-LIF-01]`) … (a geometry change renumbers ordinals
  wherever `[R-GEO-06]` moves them). A layer whose record alone changes keeps
  its extent slot, pointing at the existing region". **PASS** — and note this
  normative text *corroborates the carve-out*: a layer whose entry_count does
  not change keeps its slot and re-emits nothing.

### Check 3 — normative placement

The repair edits a `> **Rationale.**` block, non-normative per `[R-CNF-01]`
(line 106: "All text in this document is normative except: §1 …; any text
labeled *Note*, *Example*, or *Rationale* …"). The question is whether the
*wrong* statement it corrects also lives in normative text that was left
standing. I searched for it:

```
$ grep -n "R-CNT-17" spec/tarn.md
934, 1021, 1042, 1097, 1140, 1499, 2080, 2107, 2815, 3060, 3501, 3502, 3849
```

I opened 1021 (§7.4 field table: "entry_count | u64 | equals the addressed-tile
count (§11.2, `[R-CNT-17]`)"), 1042 (`[R-CNT-17]` itself), 3501 (L21) and 3502
(L22). None of them states the loose claim; all of them derive entry_count from
geometry, which is automatically correct in the zero-product case. §20.3 step 3
(2985–2998) likewise. **So the defective claim existed only in this Rationale,
and the repair landed where it needed to.** PASS.

### Check 4 — contradiction in the same passage — FAILS

The passage is the single sentence quoted above. Its final clause was not
touched by the repair:

> "— the first growth of a zero-extent layer included."

It attaches to "the layer's whole tile-index region **is re-emitted** and disk
ordinals renumber", i.e. it asserts that even the first growth of a
zero-extent layer re-emits the whole index region.

Counter-case, built from the same machinery as above: rank-2 layer,
E = (0, 0), T = (10, 10). G = (0, 0), N = 0, entry_count = 0, extent slot
(0, 0). This is a zero-extent layer (line 2833 uses the term the same way:
"any region of a zero-extent layer"; §11.1's Rationale opens on exactly this
schema-first case). Its **first growth** raises E₁ from 0 to 50: G = (5, 0),
N = 0 still. The new carve-out fires — "another dimension's grid count is 0" —
entry_count stays 0, and by §15's own account (line 2105: "At entry_count = 0
there is no region at all — zero segments, a zero-byte CRC array, extent slot
(0, 0) and crc_of_crc_array = 0") there is no region to re-emit.

So the carve-out excludes a case the trailing clause explicitly includes, three
clauses later, in the same sentence. This is the shape check 4 exists for: a
sentence written to be true only under the old wording, left standing beside
new text that narrows it. **FINDING A-01.**

### Check 5 — exhaustive claims

Words promising completeness in or near the repaired text: "every grid count",
"one shrink can do several of these at once", "the first growth … included".

- "growth that leaves **every** grid count unchanged touches the directory
  alone" — true; entry_count is a function of the grid counts alone.
- "**the first** growth of a zero-extent layer included" — falsified above; see
  A-01.
- "which holds the product at 0 and adds **no** entry" — true; verified against
  §11.2's N = ∏ Gᵢ and the addressed-tile count definition.

### Check 6 — what the repair left unconstrained

Structure: a layer's geometry declaration and the index quantities derived from
it. Members: rank d, per-dimension Eᵢ and Tᵢ, channel count C, layout
(interleaved/planar), entry_count, extent_offset/extent_length,
crc_of_crc_array, and the derived N, P, N·P, C·N.

The repaired sentence names entry_count and extent_length. Its siblings under a
growth:

- **crc_of_crc_array** — the sentence never mentions it, but `[R-CNT-23]`
  (line 1022) pins it ("0 when entry_count = 0") and L27 registers the
  violation. Governed.
- **extent_offset** — §20.3 step 3 pins it ("necessarily at a new placement",
  or kept when the record alone changes). Governed.
- **N·P, C·N, P** — `[R-GEO-03]` + `[R-ENC-04]`, registered at L2. Governed.
- **disk ordinals** — `[R-GEO-06]`, cited. Governed.
- **the lz4 decoded-size cap under growth** — §20.3 (lines 3028–3037) handles
  it explicitly and names L44. Governed.

No unpinned sibling. **PASS** (subject to A-01/A-02, which are about the
sentence's own text, not an ungoverned neighbour).

### Check 7 — argument by analogy

The repaired text contains no "exactly as / as X is / the same way"
construction. The nearest is the causal "which holds the product at 0", whose
warrant is §11.2's definition, not another rule's quantifier. Comparing verbs
anyway:

- Repair: "growth that raises one **changes** entry_count".
- `[R-CNT-17]`: "an entry_count that **does not equal** the geometry-derived
  addressed-tile count, is a validity error".
- §11.2 / `[R-GEO-03]`: "The layer's **addressed-tile count** — the number of
  its tile-index entries (§15) — **is** N for an interleaved layer and C · N
  for a planar layer".

"changes entry_count" is a claim about the difference between two generations'
values of a quantity that §11.2 **is**-defines from geometry, and `[R-CNT-17]`
ties the stored field to. The three range over the same quantity for one
layer. The analogy, such as it is, holds for both layouts separately:
interleaved entry_count = N, planar = C·N, and both are 0 when N is 0.
**PASS.**

### New ambiguity introduced

The repair introduces the pronoun "**it**" in "so where **it** does change".
Candidate antecedents, in the order the sentence supplies them:

1. "entry_count"
2. "extent_length"
3. "the product"
4. "one" (a grid count), from "growth that raises one"

(1)–(3) co-vary exactly — `[R-CNT-17]`'s formula is strictly increasing in
entry_count and the product determines entry_count — so among them the reading
does not matter. Reading (4) does matter: under it the sentence says *every*
growth that raises a grid count re-emits the whole index region, which
**nullifies the carve-out the repair was written to add**. Reading (4) is not
the nearest antecedent, but it is made live by the trailing clause "the first
growth of a zero-extent layer included", which is true only under reading (4).
The two defects reinforce each other. **FINDING A-02.**

### Hunk 2 verdict: two findings, A-01 (contradiction) and A-02 (new ambiguity).

---

## Hunk 3 — §21.3 row L41, line 3521: pronoun in the Condition cell

### The change

```
-| L41 | Inside a slab run, a stored tile's offset ≠ the previous stored tile's offset plus that tile's length (…)
+| L41 | Inside a slab run, a stored tile's offset ≠ the previous stored tile's offset plus the previous stored tile's length (…)
```

### The rule the repair adopts

For each stored tile k after the first in a slab run,
offset(k) = offset(k−1) + length(k−1), where k−1 is the previous **stored**
tile (sentinels and structurally-reject entries skipped). A file violating
this exhibits L41; the outcome is reject-layer, detected by a verifier at
certification.

### Which antecedent makes the row satisfiable — worked out independently

Two readings of the old "that tile's length":

- **Reading P** (previous stored tile): offset(k) = offset(k−1) + len(k−1).
  This is ordinary back-to-back packing. Satisfiable for any sequence of
  lengths; determines a unique layout given the run's first offset.
- **Reading C** (the current stored tile, "a stored tile" — the demonstrative
  reaching back to the sentence's subject): offset(k) = offset(k−1) + len(k).
  A tile's placement would depend on its own length. For a run with lengths
  100 then 200 this puts tile 1 at offset 200, leaving 100 unclaimed bytes
  *inside* the run — which the same cell's own instance "gap" says is a
  violation. Worse, for lengths 200 then 100 it puts tile 1 at offset 100,
  overlapping tile 0. Reading C is not merely odd; it makes the invariant
  produce gaps and overlaps as its *conforming* output, contradicting the
  parenthetical.

So Reading P is the satisfiable one. The repair chose Reading P. **Correct.**

### Cross-check against the Instances cell

Instances: "gap; overlap; out-of-ordinal placement". Under Reading P:
offset(k) > offset(k−1)+len(k−1) is a gap; offset(k) < that is an overlap;
tiles laid down in a different order than ordinal order produce
offset(k) < offset(k−1) and so fail too — "out-of-ordinal placement". All
three instances are generated by the disambiguated predicate, and each is
distinguishable as a file, which §21.1's instance rules require. Under
Reading C the mapping from the predicate to "gap"/"overlap" is incoherent.
**The Instances cell corroborates the chosen antecedent.**

### Cross-check against the governing rule

`[R-SLB-03]`, §16.2, lines 2157–2176. Read entire. The packing clause:

> "When declared, for every run: the run's stored tiles are contiguous and
> packed in ordinal order — each stored tile's offset equals the previous
> stored tile's offset plus **its** length — and the first stored tile's
> offset satisfies offset mod A_slab = 0."

Nearest-antecedent binding gives "its" = the previous stored tile, i.e.
Reading P. The non-normative Note at line 2198 glosses it the same way: "A slab
guarantees *contiguity*: consecutive disk ordinals occupy consecutive bytes."
And the Example at 2213–2216: "run 1's stored tiles are 8, 9, 11…15, packed
with no gap where 10". So the repair matches its governing rule's intended
reading. **PASS on choice of antecedent.**

### Check 2 — citations resolve

- `[R-SLB-03]` — opened, quoted above; states the packing invariant and
  "A verifier MUST check these invariants (violation: reject-layer, §15.3)".
  Matches L41's Detector=verifier, outcome reject-layer. **PASS.**
- `(R-IDX-03)` in the row's parenthetical — §15.3's classification of index
  entries; the L41 cell's own parenthetical reads exactly the same distinction
  §16.2 draws at 2163–2170 ("entries §15.3 classifies reject-tile on a
  *structural* ground … An entry whose only defect is that its stored bytes
  fail its crc is not"). **PASS.**
- §15.3 (named in the cell) — corroborated at §15's line 2043–2051: "Six rows
  are marked *structural* … `[R-SLB-03]`'s run continuity closes over it as it
  does over a sentinel". **PASS.**

### Check 1 — tense and quantifier

L41 quantifies over "a stored tile" "inside a slab run" — existential over
tiles, in the live committed state a verifier is certifying. `[R-SLB-03]`
quantifies universally: "for every run: … each stored tile's offset equals".
A register row states the *violation* condition, so the existential-of-negation
is the correct dual of the rule's universal. Generation: both range over the
state being verified, not a superseded one. **PASS.**

### Check 3 — normative placement, and the unswept restatement — FAILS

The rule's distinctive terms, searched with the hard wrap normalised away:

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "previous stored tile[^.—]\{0,90\}"
previous stored tile's offset plus its length
previous stored tile's offset plus the previous stored tile's length (gap, overlap, or out-of-ordinal placemen
```

Exactly two statements of the packing relation exist in the document: §16.2's
(`[R-SLB-03]`, the governing rule) and L41's (the register row). The repair
disambiguated **the row**. The **rule** still says "plus **its** length".

§21.1 (lines 3355–3358) settles which one an implementer must follow:

> "each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**."

So the authority for this invariant is the sentence that still carries the
pronoun. If the demonstrative in L41 was live enough to require a repair, the
possessive in `[R-SLB-03]` — the identical construction, with the identical two
antecedents ("each stored tile" as subject, "the previous stored tile" as the
nearer possessive) — is live in the place that governs. The repair fixed the
derived text and left the source. **FINDING A-03.**

I also checked the other places `[R-SLB-03]` is named — lines 2046, 2184, 2931,
3258 — and none of them restates the packing arithmetic; they cite it. Only
§16.2 and L41 state it.

### Check 4 — contradiction in the same structure

I read the whole L41 cell and the rows around it (L39–L42), and §16.2 entire.

- L42 ("A slab run's first stored tile's offset is not a multiple of A_slab")
  is the other half of `[R-SLB-03]`; the disambiguation does not touch the
  first stored tile, which has no previous stored tile, and §16.2 confirms
  "A run with no stored tiles imposes nothing." No collision.
- The carve-out inside L41's own cell — "sentinels and entries §15.3
  classifies reject-tile on a structural ground are transparent, an entry
  failing only its stored bytes' crc is not" — survives the change: "the
  previous stored tile" already means the previous non-transparent one, and
  §16.2 says so in the same words ("Sentinel tiles are transparent to run
  continuity: they occupy no bytes and do not break packing"). No collision.
- L20 (A ≠ 0 and S ≠ 0 both declared) and `[R-SLB-05]`'s inter-run placement
  freedom (§16.2, lines 2160–2163) are unaffected. No collision.

**PASS.**

### Check 5 — exhaustive claims

§21.3's header says "49 conditions." I counted the rows: L1 … L49, contiguous,
no row added or removed by this hunk. The count is still correct. The cell's
own list "(gap, overlap, or out-of-ordinal placement…)" is closed and, as shown
above, the three exhaust the ways the equality can fail given ordinal order.
The Instances cell still reads three instances, and §21.1's instance
arithmetic ("Instances within a cell are separated by semicolons") is
unchanged by the repair — the repair added no semicolon. **PASS.**

### Check 6 — what else in this structure is unconstrained

Structure: the slab declaration and the run invariants. Every quantity it can
carry, and its governing row:

| quantity | governed by |
|---|---|
| S (run length), domain 1 … 2⁶³−1 | `[R-SLB-02]`, §7.4 table; L1 lists "slab run length S" |
| A_slab a power of two 1 … 2⁶² | L29 |
| A_slab nonzero with S = 0 | L28 |
| A and S both declared | L20 (`[R-CNT-16]`) |
| run partition (blocks, block_start + r·S, no spanning channel blocks) | `[R-SLB-02]` |
| first stored tile of a run, alignment | L42 |
| subsequent stored tiles, packing | L41 — the repaired row |
| bytes between runs | slack, `[R-SLB-05]`, §5.2 |
| overlap between a run's tiles and any other layer structure | L18 |
| stale declaration carried forward | `[R-SLB-04]`; its Note (2186–2191) says deliberately it has no row of its own, detected as L41/L42 |

No sibling quantity of this structure is unpinned. This is the check that
caught the compressed-frame-header defect, and I ran it deliberately here
because L41/L42 are a two-member set and only one was touched — L42 needs no
change: it names "A_slab" explicitly and carries no pronoun. **PASS.**

### Check 7 — argument by analogy

L41 contains no "exactly as / the same way / following X" construction. It
carries no warrant sentence. **N/A — nothing to compare.** For the record, the
two governing verbs that would be compared if one existed:

- L41: "a stored tile's offset **≠** the previous stored tile's offset plus the
  previous stored tile's length"
- `[R-SLB-03]`: "each stored tile's offset **equals** the previous stored
  tile's offset plus its length"

Same relation, dual polarity, same set (stored tiles inside one run). That
is the correct row/rule relationship; see A-03 for the residual pronoun.

### Hunk 3 verdict: the disambiguation is correct; one finding, A-03, for the unswept governing rule.

---

## Hunk 4 — §23.1, line 3939: cross-reference into §20.3's Example

### The change

```
-and strands the old one (§20.3's shape (c)), which is the case most
+and strands the old one (§20.3 places this with shape (b)), which is
+the case most
```

### The rule the repair asserts

That §20.3 assigns the case "editing a user-metadata document appends a new
extent and strands the old one" to shape **(b)**, not shape (c).

### Reading the Example's sub-parts in full

`> **Example — the three shapes a commit takes.**` runs from line 3099 to
3149. I read every sub-part:

- **(a) A new layer** (3102–3113): "Nothing existing is rewritten." Slack is
  the old directory, pad and trailer.
- **(b) Tiles added to an existing layer** (3115–3128): "That layer's index is
  re-emitted whole; a commit that supersedes stored tiles takes the same shape
  … Superseded payloads become slack too; retained ones do not move."
- **(c) A change confined to the directory** (3130–3145): "clearing a slab
  declaration, renaming a layer, or changing a channel's fill value on a layer
  with no padding position and no pad bit. Only the directory is re-emitted."
  And then, at 3141–3145, verbatim:

  > "Editing user metadata is not this shape: its document lives in an extent
  > (`[R-CNT-25]`), so a new extent is appended and the old one becomes slack,
  > **as in (b)**."

So the document explicitly refuses (c) for this case and assigns the stranding
to (b). **The new reference lands on the sub-part the document actually
assigns this case to.** The pre-repair "(c)" pointed at the sub-part that says
"is not this shape". **Correct.**

### Check 2 — citations resolve

- §20.3 — the append procedure, heading at line 2940. Contains the Example.
  **PASS.**
- "shape (b)" — exists, at line 3115, and is the label §20.3 uses at 3145.
  **PASS.**
- Other citations in the same repaired sentence, unchanged but re-checked
  because they sit inside the edited passage: §9.1 (append-only model),
  §15.2 (sentinel), §20.3 step 4 (the shrink permission — lines 3041–3060,
  which does say "a new padding position whose stored byte already holds the
  fill `[R-SER-05]` fixes is not one"), §20.4 (record drop — the MU=0/PE=0 row
  at 3184), `[R-CNT-21]` (slack), §9.6 (backward scan), `[R-PRV-01]`. All
  resolve and say what the passage claims. **PASS.**
- `[R-CNT-25]` — cited by (c) for the claim that the metadata document lives
  in an extent; F21 (line 3457) registers "A top-level user-metadata record
  (type 0x0002) carries extent slot (0, 0), placing its document inline" as a
  violation, and L10 the sub-record equivalent. So "appends a new extent" is
  normatively grounded independent of the Example. **PASS.**

### Check 1 — tense and quantifier

"editing a user-metadata document appends a new extent and strands the old
one". Present-generic over commits; "the old one" is the extent of the
generation this commit supersedes. `[R-LIF-01]` freezes committed bytes, so
the appending is forced, not merely typical. The generations are the right way
round: the new extent belongs to the new state, the stranded one to the
superseded state. **PASS.**

### Check 3 — the repair sits in normative text; and the harder question

§23.1 is normative: it is not blockquoted, it contains "Writers and the tools
built on them MUST NOT represent any commit that makes sample data unreachable
as erasure of it", and it terminates in `[R-PRV-01]` (line 3956). So a
normative sentence now cites a labelled sub-part of a **non-normative
Example** (`[R-CNF-01]`, line 106, makes anything labelled *Example*
non-normative).

I asked whether that is the right thing for a normative sentence to do, and
worked it through rather than asserting:

- The label "(b)" exists nowhere outside the Example. I checked:
  `grep -n "(a)" spec/tarn.md` returns exactly one hit, line 3102, and
  `grep -n "shape (b)"` returns exactly one, the repaired line 3939. So the
  reference resolves only into non-normative text, and would dangle if the
  Example were ever cut.
- But the reference carries **no normative weight**. The proposition
  "editing a user-metadata document appends a new extent and strands the old
  one" is asserted by §23.1 itself, and is independently forced by
  `[R-CNT-25]` (document must live in an extent; F21/L10 register the
  alternative) plus `[R-LIF-01]` (committed bytes frozen) plus `[R-WRT-05]`
  ("a record it modifies is new output under its writer obligations"). The
  parenthetical only tells the reader where the document illustrates the same
  shape. Nothing in `[R-PRV-01]`'s MUST NOT depends on the Example being
  normative.
- The alternative — deleting the reference — would lose a navigational aid
  that is accurate. The alternative of citing a normative anchor instead
  (§20.3 step 3, or `[R-CNT-25]`) would be an improvement in robustness, but
  the current text is not *wrong*.

**Conclusion: not a defect.** It is a fragile pointer, and I record the
fragility here rather than as a finding, because the sentence borrows no force
from the Example and the fact it asserts is normatively grounded elsewhere.

### Check 4 — contradiction in the same passage

I read §23.1 entire (3927–3968), both paragraphs.

- "no commit removes a layer at all" (3941) — corroborated by §20.4 line
  3189: "No commit therefore removes a layer record". No collision.
- "**Where the structure carrying the bytes leaves the live state** … **Where
  it does not** … Those two cases are exhaustive" (3942–3953) — a metadata
  extent that is superseded is squarely in the first case (the extent leaves
  the live state), so the repaired clause does not disturb the dichotomy.
- "the list of operations above is not offered as closed" (3954) — explicitly
  disclaims exhaustiveness of the enumeration the repaired clause belongs to.
  No collision.
- §20.3's (c) says "Editing user metadata is **not** this shape" — the repair
  no longer collides with that; it is what the repair fixed.

**PASS.**

### Check 5 — exhaustive claims

- "the three shapes a commit takes" (the Example's title) — does placing a
  metadata edit "with shape (b)" break the count of three? No: it is placed
  *with* an existing shape, not added as a fourth, and the Example's own
  wording ("as in (b)") does the same.
- "Those two cases are exhaustive" (3952) — untouched, and argued from a
  genuine dichotomy (bytes leave the live state, or stay in the structure that
  carried them). Not falsifiable from the document.
- "which is the case most likely to strand content a caller believes it
  deleted" — a superlative, but a judgement, not a count. Untouched by the
  repair.
- "no commit removes a layer at all" — verified against §20.4 (3189) and the
  MU=0/PE=0 table row ("A commit changes the layer set by adding a layer; an
  appender never removes one"). Holds.

**PASS.**

### Check 6 — what else in this structure is unconstrained

Structure: §23.1's enumeration of the ways a commit makes bytes unreachable.
Members named: superseding a stored tile's payload; unstoring a tile to a
sentinel; a shrink dropping tiles out of the addressed set; a shrink turning
real positions into padding; dropping a record; superseding a record's extent;
editing a user-metadata document.

Members *not* named that a commit also strands: the **superseded tile-index
region** (§20.3 step 3 re-emits it "necessarily at a new placement", stranding
the old one — this is the dominant slack source per the §20.3 Note at 3081:
"editing one sample of a 10⁶-tile layer appends about 20 MB of index"), the
**superseded directory, pad and trailer** (shape (a)'s own account), and
**inter-run slack** left by a slab relayout. None of these carry sample data
the caller believes it deleted, and the paragraph disclaims closure at line
3954 ("the list of operations above is not offered as closed"), so the omission
is licensed rather than a gap. §23.2 separately covers the index's disclosure
("a tile unstored by a later commit leaves its earlier payload in the file as
slack (§23.1)"). **PASS** — the disclaimer is what saves it, and it is
pre-existing.

### Check 7 — argument by analogy — compared word for word

The repair *is* an analogy claim, so this check bites hardest here.

- Repair's governing verb: "§20.3 **places this with** shape (b)".
- Cited text's governing verb: "a new extent is appended and the old one
  becomes slack, **as in** (b)".

"places this with" is a categorisation; "as in" is a resemblance in the
respect just named. Do they range over the same thing? The proposition §23.1
attaches the parenthetical to is precisely "appends a new extent and strands
the old one" — which is, word for word, the proposition §20.3 says holds "as
in (b)". So the two verbs range over the same claim, and the analogy is
carried for exactly one proposition, not several.

I tested whether the stronger reading — "a metadata edit *is* shape (b)" —
could mislead. Shape (b)'s defining feature is "That layer's index is
re-emitted whole", which a top-level metadata edit does not do (it touches no
layer). But §20.3 (c) states outright that a metadata edit is a directory-plus-
extent operation, and §23.1's sentence is about stranding, not about index
re-emission, so a reader following the pointer arrives at (b)'s stranding
account — which is what was promised. The analogy is sound for the one
proposition it carries. **PASS**, with the note recorded here that the
statement locating this case lives in sub-part (c), not (b), so a reader who
jumps straight to (b) finds no mention of user metadata. That is a
navigational roughness, not a false claim, and I am not reporting it.

### Secondary: relative-pronoun attachment

The repair turned a noun-phrase parenthetical "(§20.3's shape (c))" into a
full clause "(§20.3 places this with shape (b))", and the sentence continues
"…, which is the case most likely to strand content a caller believes it
deleted". "which" should bind to "editing a user-metadata document"; the
parenthetical now ends in the noun phrase "shape (b)". Parentheticals do not
conventionally supply antecedents, and the same exposure existed before the
repair (the old parenthetical also ended in "shape (c)"). **Not newly
introduced; not reported.**

### Hunk 4 verdict: clean. No finding.

---

## Byte-level analysis of each finding

The discriminating question, per the charter: is the disputed file itself
conforming, and does only one reading permit an actor to produce it?

**A-01 (hunk 2, trailing clause).** The disputed behaviour is whether a commit
that grows one zero extent of a layer with two zero extents re-emits a
tile-index region. Under both readings the normative rules force the same
bytes: `[R-CNT-17]` requires extent_length = 0 when entry_count = 0, L22
registers "a nonzero slot with entry_count = 0", `[R-CNT-23]` requires
crc_of_crc_array = 0. A writer that believed the trailing clause and tried to
emit a region would produce a file carrying an L22 violation, which
`[R-CNF-05]` bars every conforming writer from emitting under both readings.
The emittable set does not move. **Not byte-level.** It is also inside a
Rationale, which `[R-CNF-01]` makes non-normative, so it constrains nobody.

**A-02 (hunk 2, "it").** Same passage, same non-normative status, same
`[R-CNT-17]`/L22 backstop. **Not byte-level.**

**A-03 (hunk 3, §16.2's "its").** Here the disputed file *is* conforming under
one reading. Take a slab-declared layer, one run, two stored tiles at ordinals
0 and 1, lengths 100 and 200, A_slab = 1, first offset 4096·k. Reading P puts
tile 1 at first_offset + 100; Reading C puts it at first_offset + 200.
Implementation V_P (a verifier reading `[R-SLB-03]`'s "its" as the previous
tile) certifies the Reading-P file; implementation V_C rejects it at layer
scope as L41, and certifies instead a file with 100 unclaimed bytes between
the two tiles — which V_P records as L41 "gap". The two verifiers return
opposite verdicts on the same bytes, and the writers built against them emit
different offset fields in the tile-index entry for ordinal 1. **Byte-level.**
I record honestly that Reading C is the semantically degenerate one and a
careful implementer would not adopt it — but that is exactly the argument that
would have excused leaving L41 alone, and L41 was repaired. The governing rule
is where the reading has to be foreclosed.

---

## Summary of contradictions looked for and NOT found

- Hunk 1 vs `[R-LIF-05]` (readers MUST NOT scan backward): no collision;
  §9.6 opens by excluding conforming readers on the default path.
- Hunk 1 vs the §9.5 Note's three-gate list: agreement, newly achieved.
- Hunk 2's carve-out vs §20.3 step 3 ("A layer whose record alone changes keeps
  its extent slot"): agreement; step 3 corroborates the carve-out.
- Hunk 2's carve-out vs `[R-GEO-02]` (zero-extent dimension is valid): no
  collision.
- Hunk 2's carve-out vs the Rationale's earlier "A layer that stored nothing
  may be re-declared freely" and §20.3's "A layer that stores no tile … MAY be
  re-declared freely": no collision; different subject (re-declaration vs
  index re-emission).
- Hunk 3 vs L42 and vs L41's own transparency carve-out: no collision.
- Hunk 3 vs §21.3's "49 conditions" count: still 49.
- Hunk 4 vs §23.1's "Those two cases are exhaustive": no collision.
- Hunk 4 vs §20.4's "No commit therefore removes a layer record": no collision.
- Hunk 4 vs the Example's "three shapes" count: no collision.
