# Downstream-accounts audit — ADR-0106 repair set (7 hunks)

Role: repair auditor, **downstream charter** — not "are the seven corrections
right", but "what elsewhere in the document depended on what those passages
used to say".

## 0. Disclosure

Read, in full or in the passages named below:
- `/private/tmp/.../case-adr0106/hunk-01.diff` … `hunk-07.diff` (my seven, read first, all seven together)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — passages read in
  full: §2.2 tail, §2.3 (lines 120–265), §2.4, §3.1 (lines 340–375), §4.2
  (lines 425–470), §5.1 (600–640), §6.2–§6.4 (778–943), §7.1–§7.3 (896–1046),
  §7.2 record framing (943–1010), §7.4 head (1046–1090), §10.3 tail /§11.1–§11.2
  (1495–1580), §13 (1740–1850), §14.2–§14.4 (1875–1990), §15.1–§15.4
  (2030–2160), §16 (2166–2265), §17 whole (2268–2470), §17.4/§18.1–§18.2
  (2470–2560), §19 (2740–2960), §20.3 step 4 (3040–3200), §20.5 (3285–3345),
  §21 (3380–3915), Appendix G (4315–4460), Appendix H (4460–4529).
- Ran `grep`/`rg` and one python whitespace-normalising scan over
  `spec/tarn.md` only. Exact greps and output are reproduced in §1 below.

Read nothing else. Did not open `docs/`, `conformance/`, `spec/registry.json`,
`full.diff`, any other hunk file, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, git history, or the web. Did not list the case directory.

**Unrequested context.** My runtime placed material in context before I began:
a project instruction file (CLAUDE.md pointing at AGENTS.md) and an index of
the maintainer's personal memory notes naming several TARN working documents,
plus a git status block with recent commit subject lines. This material is not
part of the specification. I did not open any file it named, and I did not
follow any lead it suggested; every conclusion below is traced to a quoted line
of `spec/tarn.md` or of a hunk file. I disclose its appearance rather than its
contents. One unavoidable leak: the git status block is visible in my context
and its commit subjects name prior ADR numbers. I did not use them; where a
conclusion could look derived from them (e.g. that `[R-ENC-04]` was narrowed in
an earlier round) I re-derived it from the text of `[R-ENC-04]` itself, quoted
below.

## 1. Greps run, verbatim

Because the file is hard-wrapped, every phrase search that could wrap was run
through a whitespace-normalising python scan, not a line grep.

```
$ grep -n -i "reach" spec/tarn.md
38,144,146,229,231,237,240,253,256,260,365,664,678,720,758,989,1263,1348,1373,
1380,1394,1413,1926,2240,2760,3071,3190,3258,3265,3297,3329,3336,3421,3472,
3514,3542,3595,3607,3732,3734,3737,3742,3827,3905,3907,3977,3978,3999,4180,4279,4409
```
Only 144, 146, 229–260, 3472–3475 are the §2.3 "reach" sense; the rest are
"reachable from the trailer", "a match reaching past output", etc.

```
$ grep -n "R-CNF-13\|R-CNT-24" spec/tarn.md
144,230,233,244,249,255,261,814,847,1433,3473,3475,3496
```

```
$ grep -n "R-CNT-06" spec/tarn.md
232,806,822,1284,1345,2767,3482,3483,3484,3486,3489,3490,3491,3492,3493,3494,
3495,3496,3497,3498,3854
```

```
$ grep -n "R-ENC-04" spec/tarn.md
449,820,976,1087,1562,1896,1978,2073,2092,2392,2865,3087,3484,3527,3594,3885
```

```
$ grep -n "vacuous\|sentinel" spec/tarn.md
(no hit for "vacuous"; 40 hits for "sentinel", listed in body)
```

```
$ grep -n "identity\|stride" spec/tarn.md
1894,1915,2001,2428,2429,2431,2436,2451,2612,2632,2665,2966,3067,3249,3254,
3608,3641,3703,3725,3745,4333,4399,4400,4422
```

```
$ grep -n "diverge\|restatement\|restates\|the rule governs" spec/tarn.md
8,1497,1780,1919,2840,3410,3411,3425,3781,4228
```

python whitespace-normalised scan, key phrases and hit counts:
```
"requirements that reach"      1   (line 144, §2.3 [R-CNF-02])
"reaching requirement"         1   (line 146, §2.3 [R-CNF-02])
"reaching condition"           2   (lines 237, 240, §2.3 [R-CNF-13])
"format major other than 1"    2   (line 229 [R-CNF-13]; line 3472 §21.2)
"every rule in this section"   0   (confirms hunk 5's sentence is gone and
                                    nothing else states it)
"the identity"                 3   (2431 [R-COD-10]; 3067 §20.3 [R-WRT-04];
                                    4399 Appendix G item 5)
"declaration-derived"          9   (449 [R-ENC-04]; 820 [R-CNT-06]; 976
                                    [R-CNT-13]; 1087 [R-CNT-17]; 1562
                                    [R-GEO-03]; 1896 [R-SER-02]; 1978
                                    [R-SER-07]; 3527 L2; 3885 [R-SEC-02])
```

## 2. The rule each repair adopts (my words)

1. **Hunk 1 — [R-CNF-13], §2.3.** Reach is a property of a *condition* (one
   malformed state, individuated as §21.1 individuates rows), never of a
   requirement. A condition reaches a foreign-major file iff the invariant it
   violates is one [R-CNT-24] fixes in every major. A requirement may therefore
   be half-reaching: [R-CNT-06] states ten conditions, two of which reach.
2. **Hunk 2 — [R-CNT-06], §6.2.** `dir_offset + dir_length` is an expressly
   designated declaration-derived quantity, so a reader must form it in exact
   arithmetic and reject-file if its mathematical value exceeds 2⁶³−1.
3. **Hunk 3 — [R-CNT-13], §7.2.** Same, for `extent_offset + extent_length` on
   every record's extent slot (top-level, layer, sub-record).
4. **Hunk 4 — [R-CNT-17], §7.4.** Same, for
   `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`.
5. **Hunk 5 — §17 preamble.** Deletes the claim that every §17 rule ranges over
   *stored* tiles. Each §17 rule now carries its own quantifier; nothing global
   restricts the section to stored tiles.
6. **Hunk 6 — §21.2 preamble.** Reach is derived row by row (condition by
   condition), yielding exactly F8, F14, F6 and F1's two instances. Deletes the
   clause subordinating this paragraph to [R-CNF-13] on divergence.
7. **Hunk 7 — Appendix G item 5.** Byte-shuffle is the identity exactly where
   its permutation is: stride s = 1, or group count n = L/s = 1. Elsewhere it
   changes stored bytes.

## 3. Deletion 1 — §17's stored-tile preamble. Who depended on it?

Deleted: "Every rule in this section ranges over **stored** tiles — a tile
whose index entry is the sentinel is not stored (§3.1, `[R-IDX-02]`), carries
no payload under any codec, and satisfies these rules vacuously."

I walked every rule in §17 and asked what its quantifier is now that nothing
global restricts it:

| rule | quantifier in its own words | bites an unstored tile? |
|---|---|---|
| [R-COD-01] | "A **stored tile's** bytes are produced from…" | no |
| [R-COD-02] | "Every **stored tile** is independently decodable" | no |
| [R-COD-03] | layer's codec field value set | n/a |
| [R-COD-04] | "A **non-sentinel** index entry's length … MUST equal" | no — already explicit |
| [R-COD-05] | "The **stored bytes** are exactly one DEFLATE stream" | no |
| [R-COD-06] | "The **stored bytes** are exactly one … frame"; "Writers MUST NOT compress a tile using a dictionary" | no — presupposes a frame |
| [R-COD-07] | "a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000" | yes, by design |
| [R-COD-08] | "the **stored bytes** MUST decode to exactly the decoded size" | no |
| [R-COD-09] | layer's filter field value set | n/a |
| [R-COD-10] | "A writer that filters with any other stride violates this rule" | no — a writer does not filter an unstored tile |
| [R-COD-11] | verifier capability | n/a |

So the deletion creates no new violation and strands no §17 rule. It also
removes a standing conflict: [R-COD-07] expressly ranges over **addressed**
tiles, which the deleted sentence contradicted head-on.

Two things the deleted sentence also asserted, and where they still live:
- "a tile whose index entry is the sentinel is not stored" — §3.1 states the
  biconditional normatively: "A tile is *stored in a generation* if and only if
  that generation's tile-index entry for it is not the sentinel (§15)."
  §13.3 [R-TYP-08] and §21.6's first row restate it. Not stranded.
- "carries no payload under any codec … satisfies these rules vacuously" —
  §19.4 step 4 carries the operative form: "A valid sentinel short-circuits
  steps 5 and 6 for that entry … with no payload I/O". Not stranded.

I then checked the one passage that argues *from* §17's quantifier — §21.9,
line 3795: "*Decoded size of one tile* ranges over a layer's **addressed**
tiles, stored or not, exactly as `[R-COD-07]`'s cap is". Under the old preamble
this analogy leaned on a rule the preamble contradicted; with the preamble gone
it stands cleanly. The deletion helps this passage rather than hurting it.

Every `§17` cross-reference (lines 167, 941, 1057, 1058, 1075, 1451, 1452,
1474, 1847, 2277, 2278, 2288, 2580, 2861, 2909, 3749, 4219, 4220, 4239, 4240,
4305–4307, 4397) was opened. None cites the deleted sentence or relies on §17
being stored-tile-scoped. **No finding.**

## 4. Deletion 2 — §21.2's "the rule governs" clause. Who depended on it?

Deleted: "where this restatement and that rule diverge, the rule governs
(§21.1)."

§21.1 supplies precedence for two things and only two: "each row *restates* its
governing rule, and where a row and the rule it cites diverge, **the rule
governs**", and "§21.6's entries restate their governing rules on the same
terms a row does, and where such an entry and the rule it cites diverge, the
rule governs there too." Neither covers a §21.x **preamble paragraph**. So
after the deletion, §21.2's derived list stands as an unsubordinated normative
claim beside [R-CNF-13].

That is only a defect if they can diverge. I derived the reaching set myself
from [R-CNT-24]'s five fixed invariants — (1) trailer magic at F−64, (2)
version_major/version_minor at F−56, (3) CRC-32C at F−4 over [F−64, F−4), (4)
the front signature block is constant, (5) the trailer is the final 64 bytes
and may not grow — and tested all 36 §21.2 rows:

- F1 instance 1 (front block [0,8) reversed) → violates (4) → reaches.
- F1 instance 2 (trailer magic reversed) → violates (1) → reaches.
- F6 (front block ≠ constant) → (4) → reaches.
- F8 (trailer magic wrong) → (1) → reaches.
- F14 (trailer CRC wrong) → (3) → reaches.
- F13 (committed_file_length not a multiple of 64): [R-CNT-24] fixes the
  trailer's *position relative to F*, not F's 64-alignment; §2.3's Note assigns
  the 64-aligned F to major 1 ([R-CNT-27]) → does not reach.
- F5 (< 128 bytes): 128 is derived from a ≥4-byte directory at offset ≥16 and a
  64-aligned F — all major 1's → does not reach. No row asserts invariant (5)
  standing alone, so nothing is missed there.
- F15 (trailer reserved [56,60) nonzero): inside the 48 bytes (5) lets a future
  major redefine → does not reach.
- F17, F19, F2, F3, F9, F10, F11, F12, F16, F20–F36: all assert major-1
  structures or major-1 field semantics → do not reach.
- F18 (version_major = 0): excluded as outside the premise, and §21.6 confirms
  "version_major = 0, permanently invalid in every format major version".

Derived set = {F1 (both instances), F6, F8, F14} = exactly what §21.2 states.
No divergence today. The deleted clause was a safety net, not load-bearing.
**No finding**, though I record the fragility: §21.2's paragraph is now a
normative closed list ("and no other row") with no stated subordination.

## 5. Re-quantification — reach moved from requirements to conditions

Every passage that applies, restates, or derives a list from [R-CNF-13]:

(a) **§21.2 preamble** — swept by hunk 6. Verified in §4 above.
(b) **§2.3's Note after [R-CNF-13]** — already condition-shaped: "The test is
    the invariant a condition violates". Its three worked rows (F14 reaches,
    F5 does not, F15 does not) are consistent with the per-condition rule and
    with my derivation. Non-normative but correct.
(c) **§2.3 bullet 1, [R-CNF-02], lines 143–147** — **NOT SWEPT.** See B-01.
(d) **§2.3 bullet 5, [R-CNF-11], lines 196–213** — reporting obligation still
    quantified over requirements. See B-02.
(e) **Appendix H, "Conforming verifier"** — restates (d): "reports each
    requirement it was unable to check on a capability or resource ground".
    Non-normative by its own opening ("each entry's authority is the
    requirement or section cited, never this summary"), so it inherits (d)
    rather than adding a defect.
(f) **§6.3 [R-CNT-07]** — states the distinct diagnostic as a SHOULD,
    unconditionally; [R-CNF-13] narrows *when it is owed*. Same shape before
    and after the repair. Not a new defect.
(g) **§21.6's "Two structural cases are conforming files a reader nevertheless
    refuses"** — no reach language; "the file can be perfectly conforming under
    that major" is consistent.

### (c) in full — the finding

Line 143–147, inside the `[R-CNF-02]` bullet, normative (not in a `>` block):

> "This document defines format major 1, and a file declaring another major is
> neither conforming nor nonconforming under it save as to the **requirements
> that reach it** (`[R-CNF-13]`): a reader refuses such a file on capability
> grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about its
> bytes, while the failure of a **reaching requirement** is."

Against the repaired [R-CNF-13], lines 228–232:

> "A **condition** this specification names — one malformed state, as §21.1
> individuates them, **and not the requirement that defines it** — **reaches** a
> file … Reach is per condition because a single requirement can state several:
> `[R-CNT-06]` states ten, of which the trailer magic and the trailer CRC assert
> invariants `[R-CNT-24]` fixes and the other eight do not."

The cited rule now expressly denies that requirements reach. [R-CNF-02] cites
it for a notion of requirement-level reach that it defines out of existence,
four paragraphs later in the same subsection. Two readings, both broken:

- *any-condition-reaches ⇒ the requirement reaches.* Then [R-CNT-06] reaches,
  and by [R-CNF-02] a foreign-major file's failure of **any** of its ten
  conditions is "a finding about its bytes". F15 (trailer reserved bytes
  nonzero) then makes a major-7 file nonconforming — contradicting §2.3's own
  Note ("F15 does not reach … the trailer bytes it requires be zero are inside
  the 48 that rule lets a future major redefine") and §21.2's normative list
  ("F8, F14, F6 and both of F1's instances … and no other row").
- *all-conditions-reach ⇒ the requirement reaches.* Then [R-CNT-06] does not
  reach, and F8 and F14 are not findings about a foreign-major file's bytes —
  contradicting [R-CNF-13] and §21.2 in the other direction.

I checked whether any third reading rescues it. [R-CNF-02] gives no rule for
projecting condition-level reach onto requirements, and no other passage does
either (the whitespace-normalised scan finds exactly one occurrence each of
"requirements that reach" and "reaching requirement", both here).

### Byte-level for B-01

The discriminating case is a reader that **implements major 7** — [R-CNF-13]
addresses such a reader expressly ("whatever major the file declares and
whether or not it implements that major"). Take a major-7 file that is valid
under major 7 and carries data in trailer bytes [56,60), which [R-CNT-24]
expressly lets a future major redefine.

- Reader R1, following [R-CNF-02]'s requirement-level reach on the any-condition
  reading: [R-CNT-06] reaches, so all ten of its conditions apply; F15 fires;
  R1 rejects the file, and its verifier reports *nonconforming*.
- Reader R2, following [R-CNF-13]: only F8 and F14 of [R-CNT-06]'s ten apply;
  both pass; R2 accepts the file.

Same bytes, opposite accept/reject verdicts. That is byte-level. (The set of
files a conforming **writer** may emit does not move — writers under this text
emit major 1 — and I do not claim it does.)

## 6. Designation — three quantities pinned under a narrowed [R-ENC-04]

[R-ENC-04], line 439–449, as it now stands:

> "A reader … MUST treat any quantity this specification **designates** a
> declaration-derived sum or product of integers obtained from a file … whose
> mathematical value would exceed 2⁶³ − 1 as a validity error at the owning
> scope … **A designation is express, made by the section that defines the
> quantity; an expression this specification writes only inside a comparison,
> and names nowhere, is not a designated quantity and no reader is obliged to
> form it.**"

The exposure this creates: any §21 row whose **Governing rule** is [R-ENC-04]
has no governing content for an instance whose quantity is not expressly
designated. I enumerated every such instance.

**F3** (governing [R-ENC-04]), 2 instances:
- `dir_offset + dir_length` → designated by hunk 2 in [R-CNT-06]. ✔
- non-layer top-level record `extent_offset + extent_length` → designated by
  hunk 3 in [R-CNT-13], whose sentence governs every record's slot. ✔

**L2** (governing [R-ENC-04]), 9 instances:
- layer record `extent_offset + extent_length` → hunk 3. ✔
- sub-record `extent_offset + extent_length` → hunk 3 ("the layer for a layer
  record and for sub-records"). ✔
- `N = ∏⌈Eᵢ/Tᵢ⌉`, `P = ∏Tᵢ`, `N·P`, `C·N` → [R-GEO-03]: "These products are
  declaration-derived quantities under `[R-ENC-04]`". ✔
- `P·Q`, `P·Bᶜ` → [R-SER-02]: "These products and sums are declaration-derived
  quantities under `[R-ENC-04]`". ✔
- `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` → hunk 4. ✔

**T12** — governing rule is `[R-IDX-03]`, not [R-ENC-04]; §15.3's table row
states the obligation directly ("offset + length overflows … *structural*:
reject-tile"), and [R-IDX-02] additionally scopes "[R-ENC-04]'s sum rule … to
the fields of non-sentinel entries only". Doubly covered; needs no designation.

Other declaration-derived quantities the document forms, none of them a row's
[R-ENC-04] instance, all checked for an independent overflow path:
- `dir_offset + dir_length − 4` (F29's boundary) — dominated by the sum hunk 2
  designates. ✔
- `extent_offset + 20·k` and `extent_offset + entry_count × 20` (the index
  fetch addresses, §15.4) — dominated by the extent sum hunk 3 designates and
  the region size hunk 4 designates. Hunk 3 is what makes these safe. ✔
- `s·2¹⁶` / `min((s+1)·2¹⁶, entry_count)` (L38's segment range) — bounded by
  entry_count, itself bounded by the designated region size. ✔
- `block_start + r·S` (§16.2) — r ≤ ⌈N/S⌉−1 so r·S ≤ N−1; block_start ≤ C·N,
  designated. ✔
- `⌈P/8⌉` (§14.3 plane size) — [R-SER-07]: "Every decoded size, and the value
  count V, is a declaration-derived quantity under `[R-ENC-04]`". ✔ (It is not
  a separate L2 instance, correctly: no file can fail it without failing P.)
- `Q = Σ Bᵢ`, `Fᶜ = Σ Bⱼ`, value offsets — [R-SER-02]. ✔
- `(C−1)·N + (N−1)` — L2 records it as dominated by C·N. ✔
- decoded-document size, zstd Window_Size (§18.2) — content-derived, not
  declaration-derived; [R-ENC-04] does not reach them and no row claims it.

I also checked §22.2's summary, line 3884: "Every declaration-derived sum and
product `[R-ENC-04]` designates is overflow-checked before use." Open-ended, so
it neither over- nor under-claims after the three additions. And §19.3
[R-RDR-03] already lists "the 2⁶³ − 1 ceiling on every quantity that arithmetic
derives (`[R-ENC-04]`) … and the index cross-checks computable without I/O
(`[R-CNT-17]`)", so hunks 3 and 4 land inside checks §19.3 already schedules at
layer access — matching L2's *Detected: layer access* cell. Hunk 2 lands in the
trailer gates §19.1 step 2 already schedules at open — matching F3's *open*.
Scopes match too: [R-ENC-04] says "at the owning scope"; §7.2 says "the scope
the record governs … the layer for a layer record and for sub-records, the file
for other top-level records", which is exactly F3 file / L2 layer.

**No undesignated registered quantity found.** The designation gap is closed.
No finding on hunks 2, 3, 4.

## 7. Property replacing a universal — the filter identity

Hunk 7 replaced "§17.3 makes it the identity where the stride is 1" with "The
filter is the identity **exactly** where its permutation is — where the stride
is 1 … and equally where the decoded image is a single group, n = L/s being 1".

I verified the mathematics against [R-COD-10]'s own words: "the filtered image
places byte i of group j at offset i · n + j … the inverse restores byte
i · n + j to offset j · s + i." Identity ⟺ i·n + j = j·s + i for all i<s, j<n.
s = 1 ⇒ i = 0 ⇒ offset j. ✔ n = 1 ⇒ j = 0 ⇒ offset i. ✔ s>1 ∧ n>1: take
i=0, j=1 → 1 vs s ≠ 1. ✘ So "exactly" is correct.

Reachability of n = 1: n = L/s = P in both non-bool layouts (interleaved
L = P·Q, s = Q; planar numeric L = P·Bᶜ, s = Bᶜ). n = 1 ⟺ P = ∏Tᵢ = 1 ⟺ every
tile extent is 1, which [R-GEO-01] permits ("a tile extent Tᵢ ≥ 1"). So the new
case is a real, declarable configuration, not a degenerate one.

Every other passage stating the same property (three "the identity" hits total):

1. §17.3 [R-COD-10], line 2431: "for a packed boolean plane s = 1 and the
   filter is the identity." A single example of the s=1 case, not a closed
   claim. Agrees.
2. **§20.3 step 4, [R-WRT-04], lines 3066–3070 — normative, unchanged, and now
   the odd one out.** See B-03.
3. Appendix G item 5 — the repair itself.

I also checked §21.7's filter paragraph (lines 3742–3752): "A change reaching
the filter … where it breaks neither there is no witness. Neither change is
caught by a length: both filter values are length-preserving (§17.3)." Under
the n = 1 case nothing in the image changes at all, so "no witness" holds a
fortiori. Agrees. And T26's three instances ("planar numeric: channel element
size; interleaved: sample stride Q; packed planar bool: identity s = 1") are
about a *wrong* stride, not about the identity; unaffected.

### (2) in full — the finding

§20.3 step 4 states the bar and then its carve-out:

> "A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores **in the generation this commit supersedes**, what
> §14 fixes for its stored bytes or how they decode — … or the codec and filter
> that produced the stored bytes. … The test is the effect on such a tile, and
> the list names where that effect arises rather than standing on its own: a
> change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — **a filter whose mandated stride makes it the identity**
> (`[R-COD-10]`), or a new padding position whose stored byte already holds the
> fill `[R-SER-05]` fixes — is not what this bars."

and the following paragraph closes over it:

> "What counts as such an alteration is the bar above and nothing else, **its
> carve-out included** …"

"a filter whose mandated stride makes it the identity" is precisely the
stride-only universal hunk 7 abandoned. It covers every s = 1 case (packed
bool, a uint8/int8 planar channel, a 1-byte interleaved sample) and no n = 1
case. Where P = 1 the mandated stride is *not* 1 — it is Q, or Bᶜ — yet the
filter is the identity, so flipping filter 1↔2 in a commit leaves every
superseded-generation stored tile's bytes meaning exactly what they meant.

Two readings of §20.3 result:
- **general-test reading**: the em-dash pair are illustrations of "leaves …
  meaning exactly what they meant", so the n = 1 flip is permitted;
- **closed-carve-out reading**, backed by "its carve-out included": the two
  named cases are the whole of what is excused, so the n = 1 flip is barred
  and "makes each stored tile it reaches nonconforming".

### Byte-level for B-03

Layer: rank 1, T₀ = 1 (so P = 1), interleaved, two uint8 channels (Q = 2),
codec 1, filter 1, some tiles stored. A caller asks an updater to re-declare
filter = 2.
- Updater U1 (general-test reading) commits shape (c): re-emits only the
  directory with filter = 2, generation+1, tiles and index untouched. It emits
  file F′, and holds F′ conforming.
- Updater U2 (closed-carve-out reading) refuses the commit and must instead
  perform a whole-file rewrite under a fresh `file_id` (§20.3: "Such a change
  is a new layer, or a whole-file rewrite under a fresh file_id"), producing a
  different byte sequence; and it holds F′ nonconforming.

So the two readings disagree both about which bytes a conforming updater may
put on disk and about whether F′ is a conforming file. Byte-level. I record
honestly that no verifier can *detect* the difference — §21.7: "A change
reaching the filter … where it breaks neither there is no witness" — but
[R-CNF-05] ("A writer MUST emit only conforming files") binds the actor
regardless of detectability, which is exactly the class §20.3 sits in.

## 8. Checks 1–7, per hunk, including the ones that passed

**Check 1 (tense/quantifier).**
- H1: quantifier moved from requirement to condition; it *is* the normative
  rule, and §21.1's "each row is one malformed condition" supplies the
  individuation it invokes. Its restatement in [R-CNF-02] does not match →
  B-01.
- H2/H3/H4: each adds a designation, quantified over the single named
  expression; matches [R-ENC-04]'s "any quantity this specification
  **designates**". No tense issue (all are declaration-time quantities).
- H5: removes a quantifier; per-rule quantifiers checked one by one in §3.
- H6: "condition by condition" matches [R-CNF-13]. The residual instance-level
  phrase "both of F1's instances" is not a quantifier error — F1 is one
  condition and both its instances exhibit it.
- H7: "exactly where its permutation is" is a biconditional; verified.
  §20.3's stride-only restatement does not match → B-03.

**Check 2 (citations).** All opened; results in `citations_checked`.

**Check 3 (repair sits in normative text).**
- H1 lands in [R-CNF-13], plain prose. H2 [R-CNT-06], H3 [R-CNT-13], H4
  [R-CNT-17], H6 §21.2 preamble — all plain prose, none inside a `>` block.
- H5 deletes plain prose; nothing pushed into a Note.
- **H7 lands in Appendix G, which its own heading marks non-normative** and
  which states "It adds no requirement to any actor". That is acceptable for a
  profile rationale — but it means the corrected identity property now exists
  *only* in non-normative text while the normative restatement in §20.3
  [R-WRT-04] still carries the old stride-only form. That is the classic
  signature, and it is B-03.

**Check 4 (contradiction in the same passage, including untouched text).**
- H1's passage: read §2.3 end to end. The `[R-CNF-02]` bullet collides (B-01);
  the `[R-CNF-11]` bullet's per-requirement reporting is left ill-fitting
  (B-02); the Note agrees. I also examined whether [R-CNF-13]'s unqualified "A
  reader MUST apply every reaching condition" collides with F6/[R-CNT-04]'s
  "a reader that would have to fetch them MAY defer or omit the check". It does
  not: the exemption is on residency grounds, not major grounds, it travels
  inside the condition F6 states, and Appendix H confirms the split ("which
  `[R-CNT-04]` lets a reader not holding it resident defer or omit and §2.3
  does not"). Not reported.
- H2's passage (§6.2 [R-CNT-06] whole): the ordered gates, [R-CNT-05]'s
  pre-trailer-pad rule and the mimic Note carry nothing the designation
  collides with. Clean.
- H3's passage (§7.2 whole): the extent-slot paragraph continues into the
  MU = 0 no-offsets rule and the ownership rule; no collision. Clean.
- H4's passage (§7.4's constraint block): [R-CNT-16]'s A/S exclusivity sits
  immediately before and is untouched; L22's "including slot (0,0) with
  entry_count > 0" matches "(and 0 when entry_count is 0)". Clean.
- H5's passage (§17 preamble + §17.1): §17.1's rules are stored-tile-quantified
  in their own words. Clean.
- H6's passage (§21.2 preamble + F1…F36): derived list re-derived
  independently in §4; F18's carve-out sentence survives and agrees with
  §21.6. Clean.
- H7's passage (Appendix G item 5 + items 4 and 6 either side, and the closing
  inventory paragraph): item 6 pins the sentinel for all-fill tiles; the
  closing paragraph omits the filter from its inventory but disclaims
  exhaustiveness ("Read the numbered items as the list; this paragraph names
  what they are for, not how many there are"). No collision inside the
  appendix.

**Check 5 (exhaustive claims).**
- H1: "states ten" — counted the §21.2 rows whose Governing rule is
  [R-CNT-06]: F8, F9, F10, F11, F12, F13, F14, F15, F16, F17 = **ten** ✔;
  "the other eight" = the ten minus F8 and F14 = **eight** ✔.
- H6: "and no other row" — re-derived independently in §4; holds ✔.
- H7: "**exactly** where its permutation is" ✔ (proved). "**every** tile it
  touches" ✘ — falsifiable, see B-04.
- H2/H3/H4: no completeness words.
- H5: removes an "Every rule in this section" claim.

**Check 6 (what the repair leaves unconstrained in the same structure).**
- H2's structure is the 64-byte trailer. Its quantities: magic, version_major,
  version_minor, flags, generation, dir_offset, dir_length,
  committed_file_length, file_id, reserved[56,60), CRC. Every one is gated by
  [R-CNT-06]/[R-CNT-07]/[R-CNT-08], and the only derived quantity the trailer
  yields is `dir_offset + dir_length`, now designated. Nothing left open.
- H3's structure is the 24-byte record header. Quantities: type, flags,
  inline_length, extent_offset, extent_length. type → [R-CNT-12]/[R-CNT-15];
  flags → [R-CNT-12]/[R-CNT-22]; inline_length → [R-CNT-12] (F29/L14) and
  [R-MTA-03]; the slot halves → [R-CNT-13] (F30/F31/F32, L15/L16/L17) with the
  sum now designated. `inline_length` is a u32 and cannot overflow the u64
  ceiling; there is no second derived sum in this header. Nothing left open.
- H4's structure is the tile-index region: entry array + segment CRC array.
  Quantities: entry_count (L1 domain, L21 cross-check), extent_length (L22,
  now designated), crc_of_crc_array (L27, L37), per-entry offset/length/crc
  (T6–T12, T1), segment CRC (L38), index_encoding (L31). The region's two
  sub-quantities — `entry_count × 20` (the CRC array's start) and
  `⌈entry_count/2¹⁶⌉ × 4` (its length) — are both dominated by the designated
  whole. Nothing left open. **This is the check that caught the compressed-frame
  neighbour last time, and I found no unpinned sibling here.**
- H1's structure is the set of conditions; H6's is §21.2's row set; H5's is
  §17's rule set; H7's is the filter declaration. Covered above.

**Check 7 (analogy — verb against verb).** Analogy markers in the repaired
text: "exactly as", "the same way", "as X is", "likewise", "for the same
reason".
- H1: "The test is the invariant asserted, not the bytes read" — not an
  analogy, a distinction. No warrant-rule to compare.
- H2/H3/H4: "that sum being a declaration-derived quantity **under**
  [R-ENC-04]" — a subsumption, not an analogy. Compared verbs anyway:
  [R-ENC-04]'s governing verb is "**designates** a declaration-derived sum or
  product of integers **obtained from a file**"; the three repairs' verb is
  "**being** a declaration-derived quantity". Same object, same set (a sum of
  two fields obtained from the file). The designation is express and made by
  the defining section, as [R-ENC-04] requires. Passes, all three.
- H6: "Deriving it there yields …" — points at [R-CNF-13] as the derivation's
  source, and [R-CNF-13]'s verb is "**violates** … an invariant [R-CNT-24]
  **fixes** in every format major version"; §21.2's gloss is "each **asserting**
  an invariant [R-CNT-24] fixes in every major". "asserting an invariant" vs
  "the invariant it violates" — the row states the condition, the condition
  violates the invariant the row's check asserts; the two range over the same
  set of five reaching instances, which I confirmed by re-deriving both sides
  independently (§4). Passes.
- H7: "**as for** a packed boolean plane" — an example, not a warrant, and
  correct ([R-COD-10]: "for a packed boolean plane s = 1 and the filter is the
  identity"). The one real warrant is "(`[R-COD-10]`)" attached to "n = L/s
  being 1"; [R-COD-10]'s verb is "**Viewing** the image as n = L/s consecutive
  groups of s bytes, the filtered image **places** byte i of group j at offset
  i · n + j", and the repair's verb is "the decoded image **is** a single
  group, n = L/s being 1". Same quantity, same definition of n. Passes.
- H5: deletes an analogy-free sentence.

I applied check 7's "test it against each member separately" rule to the one
sentence in this set that carries a warrant for several items — H6's "Deriving
it there yields F8, F14, F6 and both of F1's instances" — and tested each of
the five instances against [R-CNT-24] one at a time (§4). All five hold
individually.

## 9. Findings

- **B-01** §2.3 [R-CNF-02] still says "the requirements that reach it" /
  "a reaching requirement" — unswept restatement of the re-quantified rule,
  contradicting [R-CNF-13] in the same subsection. Byte-level.
- **B-02** §2.3 [R-CNF-11]'s "each requirement it was unable to check" has no
  determinate answer for a half-reaching requirement. Report-level only.
- **B-03** §20.3 step 4's carve-out still states the identity property in the
  stride-only form hunk 7 abandoned; the corrected property lives only in
  non-normative Appendix G. Byte-level.
- **B-04** Appendix G item 5's "changes the stored bytes of **every** tile it
  touches" is falsifiable. Non-normative, not byte-level.

## 10. Things I looked for and did not find

- No passage anywhere cites or leans on §17's deleted stored-tile preamble
  (§3, above). The sentinel↔unstored biconditional survives in §3.1, §13.3 and
  §21.6.
- No divergence between §21.2's derived list and [R-CNF-13] that the deleted
  precedence clause would have had to resolve (§4).
- No registered declaration-derived quantity left undesignated (§6). The three
  designations exactly cover F3's two instances and L2's remaining ones; they
  neither overshoot (no new row is implied) nor undershoot.
- No row count or instance count disturbed: §21.2 36, §21.3 49, §21.4 26,
  §21.5 10, total 121 = §21.8's "121 conditions", all recounted by hand.
- No contradiction introduced in §6.2, §7.2, §7.4 or §17 by the four
  landings there (check 4, above).
