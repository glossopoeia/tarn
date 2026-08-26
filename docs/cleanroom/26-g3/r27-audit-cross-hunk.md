# Cross-hunk consistency audit — round 27 repairs

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (in slices via
`sed -n`, covering lines 100–300, 330–375, 395–450, 600–620, 740–850, 965–1000,
1020–1100, 1530–1600, 1860–1990, 2020–2145, 2255–2500, 2845–2870, 3055–3100,
3390–3505, 3520–3610, 3670–3700, 3770–3815, 3860–3900, 4360–4420), plus
`hunk-01.diff` … `hunk-12.diff` in the case directory. Did NOT read `full.diff`,
`docs/`, `conformance/`, `spec/registry.json`, git history, or the web. Did not
list the case directory beyond a glob for `hunk-*.diff`.

Unrequested context appeared before I began: a project instruction file pointer
and an index of the maintainer's memory notes naming prior-round topics. I did
not open any of it and drew no conclusion from it. Disclosed, not used.

## Searches run (all against spec/tarn.md)

```
grep -n "R-CNT-24\|R-CNT-27\|R-CNT-07\|R-CNT-04"     -> 145,229,236,241,252,256,258,567,615,763,811,834,843,1426,2760,2763,2808,3471,3479,3483,3484,3493,3496,3654,3676,3691,3852,4176,4507
grep -n "R-ENC-04"                                   -> 446,1555,1889,1971,2066,2085,2388,2861,3083,3481,3524,3591,3882
grep -n "dir_offset +\|extent_offset +\|declaration-derived\|designat"
                                                     -> 167,168,438,442,444,788,815,873,1554,1889,1970,2389,2766,3084,3481,3488,3507,3510,3524,3539,3881,3882
grep -n "R-COD-0[1-9]\|R-COD-1[01]"                  -> 201,1908,2279,2285,2298,2304,2308,2318,2348,2378,2398,2407,2422,2437,2462,2464,2506,2518,2529,2543,2561,2564,2858,2906,3064,3080,3565,3566,3567,3582,3589,3591,3592,3593,...,3606,3633,3661,3700,3798,3845,3879,3881
grep -n "addressed"                                  -> 348,349,353,358,1043,1061,1081,1520,1530,1551,1741,1792,2041,2061,2090,2373,2380,2384,2629,3083,3092,3108,3175,3543,3566,3648,3650,3789,3798,3800,3822,3887,3977,4014,4316
grep -n "ranges over\|range over"                    -> 2265, 3425, 3430, 3797, 3807
grep -n "R-CNT-13"                                   -> 993,2163,2485,2646,2773,2848,3480,3481,3508,3509,3510,3511,3523,3524,3537,3538,3539,3540,3568,3569
grep -n "R-CNT-17"                                   -> 974,1061,1082,1137,1180,1539,2122,2149,2864,3109
grep -n "major" (filtered)                           -> 141,160,199,228-259,457,735,811,828-842,1426,3469,3471,3677,3691,3725,3813,4290,4295
```

Hard-wrap caution honoured: every phrase searched was a short fragment that
cannot wrap (`addressed`, `designat`, `ranges over`, bare requirement ids).

## Grouping by the rule touched (not by section, not by commit)

**Group A — what a requirement ranges over across format majors.**
Hunks 1, 2, 10. Hunk 2 is the new rule (`[R-CNF-13]`); hunk 1 is §2.3's
class definition adopting it; hunk 10 is §21.2's restatement deriving a row
list from it.

**Group B — what quantity `[R-ENC-04]` ranges over.**
Hunks 3 (the narrowing itself), 4 (§11.2's designation), 5 (§11.3 rewritten to
form no product), 8 (§17.2 Note, non-normative), 9 (§20.3), 11 (§22.2).

**Group C — what a §17 rule ranges over: stored vs addressed tiles.**
Hunks 6 (section preamble), 7 (`[R-COD-04]`), and the *statements about
`[R-COD-07]`* inside hunks 8 and 9. Hunk 8 and 9 therefore sit in two groups.

**Group D — Appendix G's byte-determinism argument for the filter.**
Hunk 12 alone, warranted by §17.3 `[R-COD-10]`.

The charter's three-cycle description maps onto B (narrowed a rule's reach),
C (section preamble bounding every rule in its section), and A (a requirement
deciding when requirements apply). All three are about what a rule ranges
over, and they do not agree.

## Rule each repair adopts, in my words

- H1: a foreign-major file *can* be nonconforming after all, but only via
  reaching requirements.
- H2: a requirement reaches a foreign-major file iff the invariant its
  condition violates is one `[R-CNT-24]` fixes; the reader applies it on its
  own ground; everything else is unassessed.
- H3: `[R-ENC-04]` bites only on quantities a defining section expressly
  designates; a bare expression inside a comparison is not one, and no reader
  must form it.
- H4: §11.2's four products are such designated quantities.
- H5: §11.3's padding trigger is `Eᵢ mod Tᵢ ≠ 0`, so no `Gᵢ·Tᵢ` product exists.
- H6: every §17 rule ranges over stored tiles; a sentinel tile satisfies them
  vacuously.
- H7: `[R-COD-04]`'s length equality binds non-sentinel entries only.
- H8/H9/H11: restate `[R-ENC-04]` with the new "designates" quantifier.
- H10: §21.2's reaching-row list is derived from `[R-CNF-13]`.
- H12: pinning the filter matters only where the shuffle stride exceeds 1.

## Group A findings

`[R-CNF-13]` (line 226–246) quantifies over **requirements**: "A *requirement*
of this specification **reaches** … when, and only when, the invariant *its
condition* violates …", "A reader MUST apply every reaching *requirement*",
"Every other *requirement* … governs a structure this text defines for format
major 1 alone".

§21.2's repaired preamble (line 3468) and `[R-CNF-13]`'s own Note quantify over
**rows/conditions**: "Which *rows* reach …", "F14 reaches …", "F5 does not
reach …", "F15 does not reach …".

`[R-CNT-06]` is the Governing rule of F8, F9, F10, F11, F12, F13, F14, F15,
F16 and F17. §21.2 says F8 and F14 reach and the others do not. No
requirement-level answer for `[R-CNT-06]` produces that split. → finding X-01.

`[R-CNT-07]` (line 828) states an unconditional SHOULD for the distinct
diagnostic; `[R-CNF-13]` says it "is owed" only where every reaching
requirement is satisfied. Unswept, and "owed" ≠ SHOULD. → X-08.

`[R-CNT-04]` (line 754) lets a non-resident reader "defer or omit" the front-
block check; F6's row still repeats that; hunk 10 deleted the preamble sentence
that carried it while `[R-CNF-13]` states an unqualified MUST. → X-09.

§21.6 (line 3674) untouched: "Two structural cases are **conforming files** a
reader nevertheless refuses. The first is **version_major naming a major this
reader does not implement** … In both the outcome records a reader's capability,
not a defect in the bytes". After H1/H2/H10 that is false whenever a reaching
requirement fails. → X-07.

§21.1 (line 3405) grants rule-over-restatement precedence to register *rows*
and to §21.6's *entries*; hunk 10 cites it for a §21.2 preamble paragraph. → X-11.

Enumeration check on hunk 10: `[R-CNT-24]` fixes trailer magic at F−64,
version_major/minor at F−56, CRC-32C at F−4 over [F−64,F−4), and the front
block. Rows asserting exactly those: F1 (both instances), F6, F8, F14. F15 is
at trailer offsets 56–59, inside the redefinable 48 (offsets 12–59) — correctly
excluded. F17 (committed_file_length, offset 40) redefinable — excluded. F5's
128-byte floor: 16 + 4 = 20, +64 = 84, next 64-multiple = 128 ✓, derived from
major-1 structures — correctly excluded. F18 outside the premise ✓. The list
is right *at row granularity*; that is precisely the problem.

## Group B findings

Express designations found (grep `declaration-derived`):
- line 1554 §11.2 `[R-GEO-03]` — N, P, C·N, N·P (hunk 4)
- line 1889 §14.2 `[R-SER-02]` — P·Bᶜ, P·Q, Q, Fᶜ
- line 1970 §14.3 `[R-SER-07]` — every decoded size, V

Quantities `[R-ENC-04]` is cited as governing but which no section designates:
- `dir_offset + dir_length` (F3 instance) — written only as `≤ F − 64` at
  lines 788 and 815, and as a fetch interval at 873/2766.
- `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` (L2 instance) — written only
  inside `[R-CNT-17]`'s "MUST equal" (line 1079).
- layer-record and sub-record `extent_offset + extent_length` (L2, F3) —
  `[R-CNT-13]` says "an overflowing sum" but never designates the quantity.
- non-sentinel entry `offset + length` (T12) — §15.3 table row only.
- max disk ordinal `(C−1)·N + (N−1)` — named only inside L2's parenthesis.
- `Gᵢ` itself — hunk 4 replaced "These products, like all geometry arithmetic"
  with "These products", and `Gᵢ = ⌈Eᵢ/Tᵢ⌉` is a ceiling division, not a
  product. `[R-ENC-04]`'s own category list names "grid counts".
→ X-04.

Hunk 3's closing clause "no reader is obliged to form it" collides with four
untouched MUSTs that oblige exactly that: `[R-CNT-06]` (line 815),
`[R-CNT-13]` (line 969), `[R-CNT-17]` (line 1079), §15.3's table (line 2103).
→ X-05.

Unswept restatement in normative text: `[R-RDR-03]` line 2860 still reads
"the 2⁶³ − 1 ceiling on **every quantity that arithmetic derives**
(`[R-ENC-04]`)". Hunks 9 and 11 swept §20.3 and §22.2; §19.3 was missed. → X-06.

Hunk 5 verified: `Gᵢ·Tᵢ > Eᵢ` ⟺ `Eᵢ mod Tᵢ ≠ 0`. With `Gᵢ = ⌈Eᵢ/Tᵢ⌉`, if
`Eᵢ mod Tᵢ = 0` then `Gᵢ·Tᵢ = Eᵢ`; otherwise `Gᵢ·Tᵢ > Eᵢ`. At `Eᵢ = 0`,
`Gᵢ = 0`, both sides false. Equivalent, and consistent with §11.2's own
"equal to Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0". Cite `(§4.2)` resolves: §4.2 hosts
`[R-ENC-04]`. PASS.

Hunk 8 verified: P·Q and P·Bᶜ are designated at line 1889, and P = ∏Tᵢ is a
function of tile-extent declarations alone, so both exist in a layer with a
zero extent. The Note's claim survives. PASS.

## Group C findings

Hunk 6 (line 2265, normative): "Every rule in this section ranges over
**stored** tiles".

Against it, all untouched or same-round:
- `[R-COD-07]` line 2373: "for a layer any of whose **addressed** tiles'
  decoded size exceeds 0x7E000000 bytes"
- L44 line 3566: "any of whose addressed tiles' decoded size exceeds"
- §21.9 line 3798: "ranges over a layer's **addressed** tiles, stored or not,
  exactly as `[R-COD-07]`'s cap is"
- hunk 8's Note line 2380: "The cap is quantified over the layer's *addressed*
  tiles"
- hunk 9 line 3082 (normative): "which an empty layer escapes only because
  that cap is quantified over addressed tiles"
→ X-02.

Hunk 6's "Every rule in this section" also swallows `[R-COD-03]` (codec field
value), `[R-COD-09]` (filter field value) and `[R-COD-11]` (certification),
none of which ranges over a tile at all; and its warrant ("carries no payload
under any codec") does not reach `[R-COD-04]`, whose subject is an index
entry's *length field*, which a sentinel entry does carry. That hunk 7 had to
patch `[R-COD-04]` separately is direct evidence the blanket does not hold.
Note also that the preamble's own preceding sentence says "The owning scope of
a layer's codec and filter declarations is the layer" — declarations, not
tiles. → X-03.

Hunk 6 vs hunk 7 property check: §3.1 line 349 makes them coextensive —
"A tile is *stored in a generation* if and only if that generation's tile-index
entry for it is not the sentinel". So "stored" and "non-sentinel" bound
`[R-COD-04]` the same way. PASS — the two repairs agree here.

Hunk 6 citations: §3.1 ✓ (definition above), `[R-IDX-02]` ✓ (line 2061,
"An addressed tile that is not stored has the **sentinel entry**"), §2.4 ✓
(owning-scope mapping).

## Group D findings

Hunk 12 warrant, verbs side by side:
- repair: "changes the stored bytes of any tile whose shuffle **stride
  exceeds** 1"
- §17.3 `[R-COD-10]`: "for a packed boolean plane **s = 1 and the filter is
  the identity**"; "Viewing the image as **n = L/s** consecutive groups of s
  bytes, the filtered image places byte i of group j at offset **i · n + j**"

The generalization from the packed-bool clause to "where the stride is 1" is
sound (at s = 1, i = 0 and the offset is j). But the formula is also the
identity at **n = 1**, i.e. L = s, whatever s is. §14.2 gives L = P·Q with
s = Q interleaved and L = P·Bᶜ with s = Bᶜ planar-numeric, so n = P in both:
**any layer whose tile extents are all 1 has P = 1 and a shuffle that is the
identity at every stride.** The repair's "any tile whose shuffle stride
exceeds 1" is falsified there. → X-10.

## Byte-level reasoning

X-02 moves the emittable set: a fully-sparse codec-4 layer whose declarations
put the decoded size above 0x7E000000 is barred under "addressed" and licensed
under "stored", and L44 cannot bar it independently because §21.1 makes the
rule govern over the row.

X-01 forks verifier verdicts and the `[R-CNT-07]` diagnostic on identical
bytes without moving the emittable set (no conforming writer emits a
foreign-major file at all).

X-04, X-05, X-06 do not move bytes: `[R-CNT-06]`, `[R-CNT-13]`, `[R-CNT-17]`
and §15.3 all state their comparisons in exact arithmetic and independently
pin every disputed verdict. What hunk 3 removed is the express bar on *acting
on a wrapped value*, which changes which implementations are conforming
readers, not which byte sequences are conforming files.

X-07 through X-11 are classification, diagnostic and citation defects.

X-10 sits in a non-normative appendix.
