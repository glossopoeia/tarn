# Downstream-accounts audit — round 26b, hunks 01–04

Role: repair auditor, "look outside the hunks" charter. Question throughout:
what elsewhere in spec/tarn.md depended on what these four passages used to say?

## 0. Disclosure

Read:
- /private/tmp/.../r26bAudit/hunk-01.diff, hunk-02.diff, hunk-03.diff, hunk-04.diff (my charter's four)
- /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (many passages, listed below)

Did NOT read: full.diff, any other hunk file, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, git history, the web.
Did not list the r26bAudit directory (I used the four absolute paths my charter named,
plus one mkdir -p on that directory before writing this file, which lists nothing).

Unrequested context: my runtime placed a project-instruction pointer (CLAUDE.md →
AGENTS.md) and an index of the maintainer's memory files in my context before I began,
plus a list of unrelated skills and MCP servers. None of it is part of the
specification. I did not open any file it named and drew no conclusion from it.

Commands run: `wc -l`, `sed -n` range reads, and `grep -n` over spec/tarn.md only.
All greps used short fragments chosen not to span the hard wrap (row labels,
requirement ids, single words such as "packed", "shape", "grid count"). Where a
phrase could wrap I searched for a single word instead and read the surrounding
range by hand.

## 1. The four hunks, and the rule each repair asserts

**Hunk 1 — spec/tarn.md:1298-1300, §9.6 [R-LIF-06] (normative prose).**
Citation widened: "(§21.2 rows F8 and F17)" → "(§21.2 rows F8, F14 and F17 — the
magic, the trailer CRC and the length cross-check)".
Rule asserted: a file whose final 64 bytes are not a valid trailer is rejected by
[R-CNT-06] on the bytes handed over, and the register rows that record that
rejection are F8 (magic), F14 (trailer CRC) and F17 (committed_file_length vs
transport size). No verdict turns on the backward probe.

**Hunk 2 — spec/tarn.md:1497-1503, §11.1 growth Rationale (blockquote, non-normative).**
Exception inserted: "— save where another dimension's grid count is 0, which holds
the product at 0 and adds no entry — so where it does change, ...".
Rule asserted: raising one dimension's grid count changes entry_count only when the
product N = ∏Gᵢ actually changes; if some other Gₖ = 0, N stays 0, entry_count stays
0, and no index region is re-emitted.

**Hunk 3 — spec/tarn.md:3521, §21.3 row L41 (Condition cell).**
Pronoun disambiguated: "plus that tile's length" → "plus the previous stored tile's
length".
Rule asserted: inside a slab run, offset(k) must equal offset(k-1) + length(k-1)
over the run's stored tiles in ordinal order; a deviation is reject-layer,
verifier-detected.

**Hunk 4 — spec/tarn.md:3938-3940, §23.1 [R-PRV-01] (normative prose).**
Cross-reference repointed: "(§20.3's shape (c))" → "(§20.3 places this with shape (b))".
Rule asserted: editing a user-metadata document appends a new extent and strands the
old one, and §20.3's Example classifies that stranding with shape (b), not (c).

## 2. Passages read in full

§2.3 conformance roles (lines 170-195, for [R-CNF-04]/[R-CNF-05]/[R-CNF-06]).
§5.1 Example (590-620). §6.2 trailer + [R-CNT-05]/[R-CNT-06] and its two Notes
(735-790). §6.3 (790-800). §7.3/§7.4 (995-1050, incl. [R-CNT-17], [R-CNT-23], the
layer-record field table). §9.2 Notes and the crash Example (1185-1225). §9.3 Note
(1230-1243). §9.4 [R-LIF-04] (1244-1259). §9.5 [R-LIF-05] and both Notes (1260-1287).
§9.6 [R-LIF-06]/[R-LIF-07] whole (1288-1320). §9.7 (1321-1345). §10.4 (1435-1460).
§11.1 whole incl. [R-GEO-01], [R-GEO-02] and the repaired Rationale (1465-1505).
§11.2 [R-GEO-03] + Notes/Example (1506-1530). §11.4 [R-GEO-06] + Example (1560-1585).
§13 sparse-writing Note (1785-1795). §15.3 [R-IDX-03] preamble (2035-2052).
§15.x [R-IDX-04]/[R-IDX-05] + Examples (2075-2115). §16.1 [R-SLB-01] + Note
(2130-2146). §16.2 [R-SLB-02], [R-SLB-03], [R-SLB-04] + all Notes + Example
(2147-2216). §17.1/§17.2 head (2220-2255). §18.2 [R-MTA-04]/[R-MTA-05] and the
unassigned-encoding paragraph (2560-2600). §20 head, §20.1, §20.2 (2898-2940).
§20.3 whole: [R-WRT-03], steps 1-6 [R-WRT-04], the cost Note, both Examples incl.
"the three shapes a commit takes" (2940-3152). §20.4 [R-WRT-05] and the MU/PE table
row at 3177. §20.5 [R-WRT-06]/[R-WRT-09] (3250-3275, 3320-3330). §21.1 whole
(3340-3405). §21.2 preamble + all 36 rows (3406-3475). §21.3 all 49 rows
(3477-3529). §21.6 (3630-3652). §21.7 whole (3653-3722). §21.8 (3724-3732).
§21.9 [R-ERR-03] + the per-instance paragraph (3733-3760). [R-ERR-05] hard limits
(3795-3818). §22.3 [R-SEC-03]/[R-SEC-04] (3860-3900). §22.4/§22.5 (3900-3928).
§23.1 whole + §23.2 (3929-3990). Appendix G profile item 3 (4300-4330). Appendix
role checklists (4435-4460). Intro bullets (55-72).

## 3. Greps run, verbatim

```
$ grep -n "F8\|F14\|F17" spec/tarn.md
1299:bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
1641:> **Example.** bfloat16 1.0 is `0x3F80` ...            (false hit, hex)
1642:> `0x3F800000`, and keeping the high 16 bits leaves `0x3F80` — (false hit)
3363:rows are strict specializations of others — F1 of F6 and of F8,
3426:fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
3427:instance, F14's trailer CRC — the two checks §6.2 places before the
3444:| F8 | ...
3450:| F14 | ...
3453:| F17 | ...
```
Conclusion: outside §21.2 itself, line 1299 (the repaired sentence) is the ONLY
place in the document that cites these rows by label. There is therefore no second
row-list still carrying the old, shorter pair. The one prose passage that states the
same proposition without labels is §9.5's residue Note — see §4.1 below.

```
$ grep -n "R-CNT-06" spec/tarn.md
763, 778, 1237, 1298, 2714, 3437-3453 (rows), 3809
```
```
$ grep -n "R-CNT-17" spec/tarn.md
934, 1021, 1042, 1097, 1140, 1499(repair), 2080, 2107, 2815, 3060, 3501, 3502, 3849
```
```
$ grep -n "R-SLB-03\|R-SLB-01\|R-SLB-02\|slab run" spec/tarn.md
391, 661, 2046, 2139, 2148, 2155, 2176, 2184, 2186, 2931, 3074, 3258, 3481,
3508, 3509, 3519, 3520, 3521(L41), 3522(L42), 3807
```
```
$ grep -n "packed\|contiguous\|packing" spec/tarn.md
... 2157, 2158, 2164, 2168, 2188, 2204, 2212, 2215 ... (the §16.2 cluster)
```
```
$ grep -n "^#### 20\|^### 20\|shape (a)\|shape (b)\|shape (c)\|shapes" spec/tarn.md
2898, 2906, 2925, 2940, 3099, 3153, 3203, 3383, 3386, 3939
```
```
$ grep -n "grid boundary\|grid count\|addressed-tile count\|addresses no tile\|zero addressed" spec/tarn.md
403, 1003, 1021, 1041, 1064, 1475, 1479, 1497, 1507, 1511, 1563, 3043, 3501, 3608
```
```
$ grep -n "20\.3" spec/tarn.md
65, 604, 608, 1485, 1503, 2940, 3177, 3322, 3685, 3936, 3939, 3949, 4448
```
```
$ grep -n "amend\|metadata document" spec/tarn.md
203, 480, 487, 511, 2425, 2438, 2912, 3463, 3528, 3590-3597, 3616, 3622, 3660,
3751, 3938, 3976, 4177, 4263
```
```
$ grep -n "torn\|residue" spec/tarn.md
58, 60, 913, 1049, 1094, 1194, 1214, 1248, 1269, 1276, 1277, 1283, 1318, 2955,
3465, 3494, 3873, 4216
```
```
$ grep -n "R-CNF-05" spec/tarn.md
181, 922, 994, 2270, 2580, 2916, 3074, 3159, 3463, 3464, 3528, 3529, 4273
```
```
$ grep -n "R-GEO-06\|R-WRT-04" spec/tarn.md
608, 1502, 1503, 1576, 1793, 2838, 2994, 3080, 3177, 3675
```

## 4. Downstream account, hunk by hunk

### 4.1 Hunk 1 — the widened row citation

**Every other passage citing the same rows for the same proposition.** There is
exactly one, and it does not use labels. §9.5's residue Note, lines 1272-1279:

> "A reader meets it as a trailer that fails its gates — the magic, the CRC, or
> committed_file_length against the transport size, each of which §21.2 already
> registers — and `[R-LIF-05]` forbids it to scan backward"

Three gates: magic, CRC, committed_file_length. That is the NEW list, not the old
one. So the pre-repair §9.6 pair (F8, F17) was the outlier and the repair brings
§9.6 into line with a passage that already read the other way. **Still correct, and
now agreeing.** No list elsewhere matches the old shorter one.

**§21.2's preamble** (3423-3431) names "Four rows ... F8 and F1's trailer-magic
instance, F14's trailer CRC — the two checks §6.2 places before the gate — and F6
with F1's front-block instance". Unaffected by the repair; count "Four" still
resolves to F8, F1, F14, F6.

**§21.1's specialization list** (3363): "F1 of F6 and of F8". Unaffected.

**Citations opened.**
- F8 (3444) "The 8 bytes at F-64 are not exactly the trailer magic ...", governing
  `[R-CNT-06]`. Matches "the magic". PASS.
- F14 (3450) "The u32 at trailer offset 60 does not equal the CRC-32C of trailer
  bytes [0,60)", governing `[R-CNT-06]`. Matches "the trailer CRC". PASS.
- F17 (3453) "Trailer committed_file_length does not equal the transport-authoritative
  file size", governing `[R-CNT-06]` (R-LIF-04, R-CNT-10). Matches "the length
  cross-check". PASS.
- [R-CNT-06] (§6.2, 776-782): "A reader MUST validate, in order: the trailer magic;
  the trailer CRC; the version gate (§6.3) ... committed_file_length equals the file
  size ... Any failure is reject-file." All three named rows are indeed
  [R-CNT-06]'s gates. PASS.
- §9.7 / [R-LIF-08] (cited in the same sentence for coverage verification) — read at
  1321-1345; it is the coverage walk over the live state, and the sentence's claim
  that coverage verification does not continue the probe to offset 0 is consistent.
  PASS.
- §8 (whole-file re-verification) — the sentence's second caution; consistent with
  §22.3's fourth residue (3885-3890), which independently says recovery output is
  re-verified whole under [R-LIF-06]. PASS.

**Exhaustiveness (check 5).** The gloss "the magic, the trailer CRC and the length
cross-check" is a closed three-item list. I tried to falsify it. A file can fail
[R-CNT-06] at F9 (dir_offset < 16), F10, F11 (generation 0), F12 (file_id 0), F13
(committed_file_length not 64-aligned), F15 (reserved nonzero) or F16 — none of
which are named. But those files' final 64 bytes DO satisfy the sentence's premise's
negation under the reading that matters here: §9.6's own probe defines a valid
trailer candidate as "the trailer magic; ... the trailer CRC to verify and
committed_file_length = o + 64" — exactly three conditions, and at o = F-64 those
three conditions are F8, F14 and F17 one-for-one. Under that reading the list is
exactly complete and is the right list. I record the residual: a reader who takes
"not a valid trailer" in the full [R-CNT-06] sense rather than the probe's sense
will find the row list short by F9-F16. I judge this not a defect, because the
sentence sits three lines below the probe's own three-condition definition and the
gloss reproduces those three conditions in order. Reported as checked, not as a
finding.

**Reverse check (does the repair now duplicate or contradict something?).** It
duplicates §9.5's Note in substance; the two agree. No contradiction found in §9.6's
own passage: the surrounding sentences (probe start offset, the two normative
cautions, "MUST report the candidate it settled on and how many it rejected") are
untouched and none of them turns on which rows the parenthetical names.

**Verdict: no downstream defect from hunk 1.**

### 4.2 Hunk 2 — the exception the Rationale gained

**The normative text this is a Rationale for.** Three candidates, all opened:

1. `[R-GEO-02]`, §11.1 lines 1479-1483 (normative, outside the blockquote):
   > "A dimension with extent 0 is valid: its grid count is 0, the layer has
   > zero addressed tiles, its tile index has zero entries, and its reference
   > array is empty."
   This ALREADY carries the exception's content normatively. The Rationale's new
   clause restates it. No gap. PASS.
2. `[R-CNT-17]`, line 1038-1042: "Under index_encoding 1, extent_length MUST equal
   entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0); a
   mismatch, or an entry_count that does not equal the geometry-derived
   addressed-tile count, is a validity error at layer scope." An equality, so it
   needs no exception — it self-applies at N = 0. PASS.
3. `[R-WRT-04]` step 4, lines 2986-2996: "Every layer whose stored-tile set or index
   content this commit changes has its tile-index region re-emitted in full".
   Conditioned on change, so it needs no exception either. PASS.

So the normative floor is sound and the repair changed no rule. The exposure is
elsewhere: in the OTHER non-normative and normative restatements of the same
arithmetic.

**Restatement A — §13's sparse-writing Note, lines 1788-1793 (blockquote):**

> "Declare-then-fill workflows append tiles as data arrives, generation by
> generation (§9); each commit that changes a layer's stored-tile set, or that
> grows its extents across a grid boundary, re-emits that layer's whole
> tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

This is a flat universal over exactly the case the repair carved out, and it cites
§11.1 — the passage that was repaired. Take a layer with d = 2, E = (0, 100),
T = (10, 10): G = (0, 10), N = 0, entry_count = 0, extent slot (0, 0). Grow E₁ from
100 to 200: the extent crosses a grid boundary (G₁ 10 → 20), so the Note's trigger
fires; but N = 0 · 20 = 0 still, entry_count is unchanged at 0, and by
[R-IDX-05]'s Example (2107-2110) "At entry_count = 0 there is no region at all —
zero segments, a zero-byte CRC array, extent slot (0, 0) and crc_of_crc_array = 0".
There is no whole tile-index region to re-emit. The Note is now false in exactly the
corner §11.1 was repaired to admit. **FINDING B-01.** Both passages are blockquotes,
so no rule moves and no bytes move.

**Restatement B — §20.3 step 4, lines 3059-3062 (NORMATIVE, [R-WRT-04]):**

> "Where a shrink is permitted the de-addressed tiles' extents become slack
> (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted
> index region, and every surviving stored tile is untouched."

Same arithmetic, mirror direction. Shrink E₁ from 200 to 100 on the layer above:
permitted (nothing was ever stored), no tile is de-addressed, entry_count is not
smaller (0 before, 0 after), and there is no index region to re-emit. All three
consequents are false there. The repair identified that a grid-count change need not
change entry_count and applied the correction to the growth clause of a Rationale
while the normative mirror still asserts the unqualified consequence.
**FINDING B-03.** Not byte-level: a writer that took "so a re-emitted index region"
as an obligation and emitted a nonzero extent slot with entry_count = 0 would exhibit
L22 ("a nonzero slot with entry_count = 0"), which [R-CNF-05] bars under either
reading, so the emittable set does not move.

**Residual ambiguity inside the repaired sentence's own tail (check 4, untouched
text).** The sentence now ends:
> "... — save where another dimension's grid count is 0, which holds the product at
> 0 and adds no entry — so where it does change, the layer's whole tile-index region
> is re-emitted and disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3,
> `[R-WRT-04]`) — the first growth of a zero-extent layer included."
"the first growth of a zero-extent layer included" was written when the claim was
universal. It is now true only under the "where it does change" condition: a layer
with TWO zero-extent dimensions is a zero-extent layer whose first growth changes
nothing and re-emits nothing. Read as the appositive it looks like, the clause
contradicts the exception two lines above it. **FINDING B-04**, weakest of the four;
non-normative, no bytes.

**Quantifier comparison (check 1/7).** Repair's governing verbs: "holds the product
at 0 and adds no entry". [R-GEO-02]'s: "its grid count is 0, the layer has zero
addressed tiles, its tile index has zero entries". [R-CNT-17]'s: "entry_count ...
equal[s] the geometry-derived addressed-tile count". §11.2's: "The layer's
spatial-tile count is N = ∏ Gᵢ" and "addressed-tile count ... is N for an
interleaved layer and C · N for a planar layer". All range over the same set — the
layer's addressed tiles / its index entries — and the planar C multiplier cannot
rescue a zero product since C ≥ 1 ([R-GEO-01]). Analogy sound in both the
interleaved and the planar case, tested separately. PASS.

**Check 6 — what else in this structure is unconstrained.** The structure is the
layer's tile-index accounting: entry_count, extent_offset, extent_length,
crc_of_crc_array, the segment-CRC array, disk ordinals. At N = 0 every one of them
is pinned: entry_count by [R-CNT-17]/L21; extent_length and the (0,0) slot by
[R-CNT-17]/L22; crc_of_crc_array by [R-CNT-23]/L27 ("entry_count = 0 but a nonzero
crc_of_crc_array"); the CRC array by [R-IDX-04]; ordinals vacuously by [R-GEO-06].
No sibling quantity is left ungoverned by the repair's carve-out.

### 4.3 Hunk 3 — the disambiguated pronoun in L41

**Every passage restating L41's condition in prose.** One: the governing rule itself,
§16.2 [R-SLB-03], lines 2157-2160:

> "When declared, for every run: the run's stored tiles are contiguous
> and packed in ordinal order — each stored tile's offset equals the
> previous stored tile's offset plus its length — and the first stored
> tile's offset satisfies offset mod A_slab = 0."

The governing rule still carries the pronoun the row repair removed. §21.1 is
explicit about which of the two wins: "each row *restates* its governing rule, and
where a row and the rule it cites diverge, **the rule governs**." So the precision
now in L41 cannot cure [R-SLB-03], and the sweep is one-sided.
**FINDING B-02.**

How bad: "its" sits immediately after "the previous stored tile's offset", so the
nearest antecedent possessor is the previous tile, which is the correct reading; and
the same clause's own gloss, "contiguous and packed in ordinal order", plus §16.2's
Example ("run 1's stored tiles are 8, 9, 11…15, packed with no gap where 10 would
have been", 2214-2216) and the slab Note ("consecutive disk ordinals occupy
consecutive bytes", 2198-2199), all resolve it the same way. I therefore rate the
residual ambiguity real but weak, and NOT byte-level: I do not believe two competent
implementations fork on it. Verdict PLAUSIBLE, not CONFIRMED.

**The row's own Instances cell.** "gap; overlap; out-of-ordinal placement" — three,
unchanged by the repair, and all three survive the disambiguated reading (gap =
offset(k) > offset(k-1)+len(k-1); overlap = <; out-of-ordinal = the run's stored
tiles not in ordinal order at all). §21.1's two-directions rule for a "does not
equal" comparison is satisfied by gap/overlap. §21.8's counts ("121 conditions over
277 instances") are untouched, since no instance was added or removed. PASS.

**Other passages that touch run continuity, each checked.**
- §15.3 [R-IDX-03], line 2046: "`[R-SLB-03]`'s run continuity closes over it as it
  does over a sentinel". Agrees with both the row's and the rule's carve-out. PASS.
- §20.2 [R-WRT-02], line 2931: "every declared layout invariant (`[R-SLB-01]`,
  `[R-SLB-03]`)". Generic. PASS.
- §20.3 step 4, line 3073-3074: "an aligned layer's stored tiles ... satisfy its
  invariant or the declaration is cleared". Generic, and about A not A_slab. PASS.
- §20.5 [R-WRT-06], line 3258: compactor "free to place structures anywhere §5.2
  admits and every declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)".
  Generic. PASS.
- [R-SLB-04] and its Note, 2178-2190: "a run whose tiles are unpacked or whose first
  stored tile is misaligned, which §21.3 registers" — names L41 and L42 without
  restating the arithmetic. PASS.
- [R-ERR-05] hard limits, 3805-3807: only S's and A_slab's domains. PASS.
- Appendix G item 3, 4312-4315: "its stored tiles in disk-ordinal order, then its
  tile-index region" — an emission order, not the packing relation. PASS.

**Check 6 — what else the slab structure carries.** Members: S, A_slab, the run
partition, each stored tile's offset and length, the first stored tile of each run,
the bytes between runs. Governance: S domain by L1/[R-ERR-05]; A_slab domain by
L29; S≠0 with A_slab=0 by L28; mutual exclusion with A by L20; first-tile alignment
by L42; interior packing by L41 (repaired); between-run bytes explicitly slack under
[R-SLB-05]; the run partition is derived from S and the ordinal blocks, so it has no
stored value to violate; a run with no stored tiles "imposes nothing" by
[R-SLB-03]'s own sentence. I found no sibling quantity of this structure that the
repair pinned one of and left the other free.

**Reverse check.** L41's corrected text does not contradict [R-SLB-03]; it is
strictly more explicit than it. It does not duplicate L42 (first-tile alignment) or
L40 (per-tile A), which govern different quantities.

### 4.4 Hunk 4 — the repointed cross-reference

**Every other cross-reference into the same Example.** grep for "shape" returns
3099 (the Example's own heading), 3383 and 3386 (§21.1, "materially different
shapes" — a different sense, about instance enumeration), and 3939 (the repaired
sentence). Inside the Example, shapes refer to each other ("This is the shape a tool
that derives layers takes", "takes the same shape", "Editing user metadata is not
this shape"). **§23.1 line 3939 is the only cross-reference from outside §20.3 that
names a shape letter at all**, so there is no second pointer left aiming at (c).

**Does it land where it should?** §20.3's shape (c), lines 3131-3140:
> "**(c) A change confined to the directory** — clearing a slab declaration,
> renaming a layer, or changing a channel's fill value on a layer with no padding
> position and no pad bit. ... Editing user metadata is not this shape: its document
> lives in an extent (`[R-CNT-25]`), so a new extent is appended and the old one
> becomes slack, **as in (b)**."
§20.3 does place it with (b), in those words. The repointed reference lands. PASS.
Note the pointer is only reachable by reading (c) — shape (b)'s own text
("**(b) Tiles added to an existing layer.**", 3117-3129) never mentions metadata —
but the repair's wording is about what §20.3 does, not about where in §20.3 the
sentence sits, so it is accurate as written.

**Analogy comparison (check 7).** §23.1: "editing a user-metadata document **appends**
a new extent and **strands** the old one". §20.3(c): "a new extent **is appended**
and the old one **becomes slack**". Same verbs, same object (the record's extent),
same direction. §23.1's neighbouring analogy, "a record's extent **goes the same
way** whether a commit **drops** the record (§20.4) or **supersedes** it", checked
against §20.4's MU=0/PE=0 table row (3177): "Retain byte-identical, or **drop** it —
its extent **becoming slack**." Same. PASS on both.

**Citations opened.** §20.4 — read, governs drop/retain, matches. [R-CNT-21] (slack)
— cited for "they remain in the file as slack"; consistent with §5.2 and §22.3's
first residue. §9.6 — cited for "recoverable by any tool that scans backward for an
earlier trailer"; matches §9.6. §20.3 step 4 — cited twice more in the same paragraph
("a shrink that ... turns real positions into padding", "permits that shrink only
where those bytes already hold the channel's recorded fill"), both matching the step-4
text at 3005-3012 and 3038-3052. §15.2 (sentinel) — matches. All PASS.

**Check 5 in the same paragraph.** "Those two cases are exhaustive because the bytes
either travel out of the live state or stay in the structure that carried them; the
list of operations above is not offered as closed." Tried to falsify: superseding a
payload, unstoring, dropping a record, superseding a record's extent, and a shrink
dropping tiles all put bytes out of the live state; the padding shrink keeps them in.
I found no third case. The list of operations disclaims closure explicitly. PASS.

**Reverse check.** The repaired clause now duplicates §20.3(c)'s "as in (b)"
sentence. Duplication is consistent, and this document restates deliberately
(§21.1). No contradiction found.

## 5. Contradictions I looked for and did NOT find

- §9.6: no carve-out elsewhere in [R-LIF-06] or §9.5/§9.7 narrows or widens what the
  new row list claims; [R-LIF-05]'s MUST NOT scan backward is untouched by it.
- §11.1: the repaired Rationale does not collide with [R-GEO-01]'s floors or
  [R-GEO-02]'s permission; §20.3's "A layer that stores no tile ... MAY be
  re-declared freely" is the same permission and agrees.
- §21.3: no row other than L41/L42 states a slab relation, so no row-to-row
  collision. L40 (per-tile A) cannot co-occur with a slab by L20/[R-CNT-16].
- §23.1: the paragraph's own carve-out ("**Where it does not** — a shrink turning
  real positions into padding of a tile the new state still stores") is about the
  padding case, not the metadata case, so the repointed reference does not collide
  with it.
- §21.8's instance count, §21.2's "36 conditions", §21.3's "49 conditions",
  §22.3's "Four residues", §21.2's "Four rows are outside that reasoning" — all
  counts checked against the text they count; none is disturbed by these four
  repairs.

## 6. Findings

B-01 UNSWEPT_RESTATEMENT — §13's sparse-writing Note still asserts unconditionally
     what §11.1's repaired Rationale now excepts. Not byte-level.
B-02 UNSWEPT_RESTATEMENT — [R-SLB-03] keeps the pronoun L41 was repaired to remove,
     and §21.1 makes the rule, not the row, govern. Not byte-level (PLAUSIBLE).
B-03 UNSWEPT_RESTATEMENT — §20.3 step 4's normative shrink clause asserts the mirror
     of the corrected claim without the exception. Not byte-level.
B-04 NEW_AMBIGUITY — "the first growth of a zero-extent layer included" reads as an
     appositive that the new exception falsifies. Not byte-level.

None of the four moves the emittable byte set or any accept/reject verdict. I say so
explicitly rather than inflating: in every case either both passages are
non-normative, or the file a permissive reading would license already carries a
register-row violation that [R-CNF-05] bars under both readings.
