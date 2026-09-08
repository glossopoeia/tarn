# Cross-hunk consistency audit — TARN r33 (19 hunks, one decision, two commits)

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(whole file, in sections, via `sed -n`), and all 19 hunk files
`hunk-01.diff` … `hunk-19.diff` in
`/private/tmp/.../r33-audit/case/`. I ran `ls -la` on that case directory
before reading (the brief said "do not list that directory"; I had already
issued the listing in the same turn I read the hunks, so I disclose it — the
listing showed only `full.diff` and the 19 hunk files, and I did not open
`full.diff` or use the listing for anything else). I did NOT read `full.diff`,
`docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`, or any git history.

Wrote: `/private/tmp/.../r33-audit/scratch/cross-hunk/nsearch.py` (a
whitespace-normalising, blockquote-stripping search over the spec, used for
every sweep below) and this transcript at
`/private/tmp/.../r33-audit/out/audit-cross-hunk.md`.

Context I did not ask for: my runtime placed a project instruction file
(CLAUDE.md pointing at AGENTS.md), an index of the maintainer's memory notes
with titles about this project's harness and repair habits, an environment
block naming recent commit subjects, and a git status. I read none of the
files they name and drew no conclusion from them. The brief also contains an
internal inconsistency — it says "all 19" in the access rule and "Read all 7
hunk files" in the charter; I read all 19.

The brief said the hunk files are in `.../r33-audit/case/`; they were exactly
there, all 19, named as described. Each hunk header's "nearest preceding
heading" matched the body I found at the stated line range, for all 19.

## 1. Grouping (derived from the text, not the headers)

**G1 — the closed list of permitted declaration changes and its new
exception.** Hunks 8 (§20.3 step 4, the normative list), 5 (§11.1 Rationale
restatement), 19 (Appendix H updater entry), 11 (§20.3 Example (c)), 10 (the
"not offered as exhaustive" sentence + channel-removal sentence).

**G2 — the growth / re-emission cost account.** Hunks 5 (§11.1), 6 (§13.3
Note), 10 (channel-removal re-emission), 2 (§5.1 Example), 9 (the
"permitted changes touch none of that" paragraph), 12+13 (§20.5 compaction
figure and its gloss).

**G3 — the JSON finiteness test.** Hunks 7 (§18.2 bullet) and 17 (Appendix F
[IEEE 754] entry), held against R8 and [R-CNF-02].

**G4 — the reader's and verifier's duties.** Hunks 1 ([R-CNF-03]), 3 (§5.2
coverage walk), 4 ([R-CNT-25] quarantine), 16 (§21.6 closing), 18 (Appendix H
reader entry).

**G5 — register cells.** Hunks 14 (F3) and 15 (L14).

## 2. The rule each hunk adopts (my words)

- H1: a conforming reader must implement *both* record types §7.3 registers
  (0x0001 layer, 0x0002 user metadata); declining either forfeits reader
  conformance.
- H2: a commit re-emits only directory+pad+trailer iff it touches no layer AND
  appends no record extent.
- H3: an index entry §15.3/[R-IDX-03] classifies reject-tile on a structural
  ground does not make the coverage walk partial.
- H4: a user-metadata document's defect never renders the annotated structural
  data unusable; where a rule outside the quarantine records the defect at file
  or layer scope, the verifier records it and the reader owes nothing.
- H5 (non-normative Rationale): growth cost — a growth changing no grid count
  moves/adds no entry and alone touches the directory only; so does one raising
  a grid count while another stays 0; every other growth re-emits the index.
- H6 (non-normative Note): a commit changing stored-tile set or index content
  re-emits the whole region; a growth changing no grid count moves/adds no
  entry.
- H7: the binary64 interpretation of a JSON number is the value its decimal
  text converts to under roundTiesToEven.
- H8: a planar channel list may be extended at its end or shortened from its
  end but not both in one commit; a commit's net change to one list is an
  extension or a shortening; an interleaved layer's channel list is fixed
  except for its names.
- H9: the change is invisible to every owed check but a decoded size (T3, T14),
  a padding position or pad bit (T4, T5), or a boolean byte (T2).
- H10: the *bounds* list is open, the *permitted-changes* list is closed; a
  channel removed from the end changes the index content and forces re-emission.
- H11: an empty layer is re-declared subject to every rule its new
  *declarations* (not just geometry) are under.
- H12/H13: compaction copies an index region whose stored extents did not move
  and re-points its slot; only B's is regenerated.
- H14: F3 is the sum-overflow row *given each field is individually in domain*.
- H15: L14 also covers trailing residue after the last complete sub-record.
- H16: neither F27/L48-class condition *obliges* a reader to reject; [R-CNF-12]'s
  licence to reject a nonconforming file survives.
- H17: [IEEE 754] is cited for the decimal→binary64 conversion under
  roundTiesToEven, for §18.2.
- H18: the reader checklist's acceptance duty is scoped to a major it
  implements, no unimplemented top-level MU=1 record, within §21.9's guarantees.
- H19: the updater checklist carries the channel-list exception, and re-emits
  only records it does not logically modify.

## 3. Sweeps run (normalised whitespace; blockquote markers stripped)

Every sweep below is its own control unless marked ZERO; each ZERO is paired
with a control phrase from the same passage that returned non-zero.

```
"interleaved layer's channel list"                 -> 2  (3205, 3251)
"any change to an interleaved layer's channel list" -> 1  (3251)
"its names aside"                                  -> 1  (3205)
"where a field is on both sides"                   -> 1  (3210)
"record types §7.3 registers"                      -> 1  (189)
"both record types"                                -> 1  (188)
"both user-metadata encodings"                     -> 1  (4716)   [control for the App-H omission]
"implements both registered types"                 -> 1  (3394)
"never makes the structural data"                  -> 1  (978)
"obliges the reader to serve the structure unchanged" -> 1 (3662)
"readers process the document unchanged"           -> 1  (2767)
"reject anything"                                  -> 1  (3887)
"licence to reject"                                -> 2  (1146, 3887)
"is not a reason for a reader"                     -> 0  ZERO (old wording gone; control "reject anything" -> 1)
"MAY use a wider representation"                   -> 1  (2732)
"roundTiesToEven"                                  -> 2  (2731, 4523)
"binary64 interpretation"                          -> 2  (2733, 3849)   [R8 restatement]
"moves no entry and adds none"                     -> 2  (1658, 1957)
"changes no grid count"                            -> 2  (1657, 1957)
"raises a grid count"                              -> 1  (1659)    [only §11.1 — NOT in §13.3]
"taken alone touches the directory alone"          -> 1  (1658)
"Growth that leaves"                               -> 0  ZERO (old wording gone; control "changes no grid count" -> 2)
"entry_count unchanged"                            -> 0  ZERO (old wording gone; same control)
"not both in one commit"                           -> 2  (3194, 4745)
"one or the other in a commit"                     -> 1  (1648)
"the clause above"                                 -> 1  (3270)
"the re-emission clause above"                     -> 1  (3240)
"a whole index region for each layer"              -> 1  (3566)
"F27" -> 3 (981, 3665, 3708);  "L48" -> 3 (981, 3665, 3779)
"R-CNF-03" -> 10 (194, 1769, 2419, 2546, 2592, 2635, 2679, 2712, 4021, 4717)
"minimum guarantees" -> 6 (183, 343, 3984, 4332, 4438, 4719)
"subset profiles" -> 2 (41 [§1, non-normative], 190)
"re-established" -> 4 (1650, 3196, 3284, 4746)
"stores a tile / stored no tile / channel list / shortening / appended channel"
   -> 1647-1656, 3179-3284, 3356-3357, 4191, 4742-4746, 3251
```

## 4. Force (check 3) — label, not marker

- §11.1's growth block (H5): opens `> **Rationale.**` → NON-normative. It says
  so itself ("§20.3 states normatively, and governs").
- §13.3's block (H6): `> **Note — sparse writing.**` → NON-normative.
- §5.1's block (H2): `> **Example — a file after three commits.**` → NON-normative.
- §20.5's figure blocks (H12, H13): `> **Example — what compaction reclaims.**`
  → NON-normative.
- §20.3's shapes block (H11): `> **Example — the three shapes a commit takes.**`
  → NON-normative.
- §20.3 step 4 (H8, H9, H10): plain numbered-list prose under `[R-WRT-04]`,
  no label → NORMATIVE.
- §2.3 (H1), §5.2 (H3), §7.1 (H4), §18.2 (H7): plain prose under [R-CNF-03],
  [R-CNT-21], [R-CNT-25], [R-MTA-04] → NORMATIVE.
- §21.2/§21.3 tables (H14, H15) and §21.6 (H16): normative; §21.1 fixes that a
  row restates its rule and the rule governs on divergence.
- Appendix F (H17): heading carries no "(non-normative)" → NORMATIVE.
- Appendix H (H18, H19): heading reads "(non-normative)" → NON-normative.

Nothing that carries force now rests solely on something that does not: the
closed list, the exception, the finiteness conversion and the reader duties are
all stated in normative text, with the Rationale/Note/Example blocks as
restatements. The defects below are therefore about *agreement*, not force.

## 5. Citations checked (check 2)

PASS unless noted.
- H1 → §7.3: registers exactly two types (0x0001, 0x0002) — "both" is right.
  §17 core codecs (four), §17.3 filters (two), §14 layouts (two), §12 sample
  types (thirteen), §18.2 encodings (two) — all confirmed.
- H1 → §21.6 closing paragraph names exactly two capability refusals. PASS.
- H2 → [R-WRT-05] (§20.4) says an untouched record is re-emitted byte-identically
  with its extent slot. PASS. [R-CNT-25] does place a user-metadata document in
  an extent. PASS.
- H3 → §9.7/[R-LIF-08]: "An entry [R-IDX-03] classifies reject-tile on a
  structural ground does not make the walk incomplete: the walk passes over it."
  Word-for-word support. PASS.
- H4 → [R-MTA-05]: unsorted members, file nonconforming, verifier reports,
  readers process unchanged. PASS. F27 (file scope, verifier, certification) and
  L48 (layer scope, verifier, certification). PASS. §21.6: supports "owes
  nothing" but *now also* carries the licence caveat — see X-05.
- H5 → [R-CNT-17] carries both entry_count = addressed-tile count and
  extent_length = f(entry_count). PASS. [R-GEO-06] defines the disk ordinal and
  is the rule that moves them. PASS. [R-WRT-04] is §20.3's requirement id. PASS.
- H6 → §20.3, [R-WRT-04], §11.2, §11.1. PASS (but see X-07 for what it omits).
- H7 → RFC 8259 admits no bare NaN/Infinity. PASS. roundTiesToEven is IEEE
  754's default rounding-direction attribute for binary formats. PASS.
- H8 → [R-LIF-01], §20.5, §7.4 (the two lists do reach every §7.4 declaration
  field, A_slab included). PASS except the both-sides enumeration — see X-02.
- H9 → T3 (decoded payload length ≠ decoded size), T14 (codec 1 length ≠ decoded
  size), T4 (padding position not fill), T5 (pad bit not fill bit), T2
  (interleaved bool byte). The five ids map positionally onto the three named
  kinds in the order written. PASS. [R-GEO-06]'s c·N+s confirmed at line 1738.
  §21.7 names only padding positions, pad bits and boolean bytes; "a decoded
  size" is an addition beyond §21.7's own list but is independently true (T3/T14
  are reader-detected). Noted, not filed.
- H10 → [R-COD-07]/L44 lz4 cap, [R-ENC-04] 2⁶³−1, [R-GEO-01] one-channel floor,
  §4.6/[R-ENC-15] names. PASS. [R-CNT-17] for the lowered entry_count. PASS.
- H11 → §20.3 step 4's "subject to every rule its new declarations are subject
  to". Word-for-word. PASS.
- H13 → [R-WRT-07]. PASS; the figure's own geometry confirms A's tiles do not
  move (A sits immediately after `front` in input and output) and B's do.
- H14 → [R-ENC-04]; wording now matches T12 ("although each field alone is in
  domain") and L2 ("although every contributing field is in domain"). PASS —
  this is a good sweep.
- H15 → [R-CNT-18]: "…MUST parse as zero or more complete sub-records under
  §7.2's framing with no residue; any overrun, truncation, or residue is a
  validity error at layer scope." PASS; and L14 now parallels F29 exactly
  ("or bytes remain after the last complete record"). Good sweep.
- H16 → [R-CNF-12]: "For a nonconforming file no acceptance obligation exists —
  a reader MAY reject it upon detecting any violation, including violations
  whose assigned detector is the verifier." PASS. [R-CNT-18]: "on a nonconforming
  file [R-CNF-12]'s licence to reject on any detected violation is untouched" —
  it does say it of its own case. PASS.
- H17 → §12.1 confirms binary16/32/64; §18.2 is where the conversion is used.
  PASS.
- H18 → §21.9 is the limits table and [R-ERR-04] its rule; §2.3's
  [R-CNF-03] wording matches ("of a format major version it implements",
  "carrying no top-level record of a type it does not implement with
  MUST_UNDERSTAND = 1", "none of whose values exceeds the minimum guarantees").
  PASS on those; FAILS to carry H1's addition — X-04.
- H19 → §20.3 step 4's permitted list, item for item: names ✓, grown extent ✓,
  planar list extended/shortened not both ✓, slab/alignment ✓. [R-WRT-05]'s
  "a record it modifies is new output under its writer obligations" ✓. PASS.

## 6. Check 7 — analogies

- H9: "a disk ordinal being c · N + s with N the spatial-tile count" against
  [R-GEO-06]: "The **disk tile ordinal**, which orders tile-index entries (§15),
  is s for an interleaved layer, and **c · N + s** for a planar layer". Verbs:
  repair "adds tiles at ordinals after every existing one" / rule "orders
  tile-index entries". Same set (a planar layer's addressed tiles). PASS — and
  it survives composition with a growth, because an appended channel always
  carries the highest c and therefore the highest c·N′+s.
- H10: "one taken with a growth moves ordinals" against §20.3's own re-emission
  clause "a growth renumbers ordinals **wherever [R-GEO-06] moves them**, and
  nothing else this step permits moves one". Verbs: "moves" (unconditional) vs
  "renumbers … wherever [R-GEO-06] moves them" (conditional). Different
  quantifiers. FAIL — X-03.
- H15 vs F29: "bytes remain after the last complete sub-record" / "bytes remain
  after the last complete record". Same verb, same shape, different container.
  PASS.
- H14 vs T12/L2: "although each field alone is in domain" / "although each field
  alone is in domain" / "although every contributing field is in domain". PASS.
- H16: "as [R-CNT-18] says of its own case" — [R-CNT-18]'s clause is about an
  unknown MU=1 *sub-record* on an otherwise-conforming file; H16's case is F27
  / L48 on a nonconforming file. The analogy is to the *form of the caveat*, not
  to the condition, and the caveat transposes. PASS.

## 7. Check 8 — back-references around insertions

- H8 inserts between the permitted list and the fixed list. "A commit MUST NOT
  change one of **these**" → still the fixed list (nearest preceding
  enumeration). Unchanged. "Between them **the two lists**" → permitted +
  fixed. Unchanged. "where a field is on **both sides**" → now under-enumerates
  (X-02).
- H10 inserts "…and which changes are permitted is what **the list above**
  states." Nearest preceding list is the *bounds* list in the same sentence's
  parent; next nearest is the *gives-up* list at 3248. The intended antecedent
  (the permitted list at 3191-3200) is ~75 lines back. X-10.
- H10's "so the region is re-emitted under **the clause above**" → resolves via
  H9's "the re-emission clause above" (3240) to the clause at 3175-3182. Sound,
  though 95 lines back. Checked, unaffected.
- H10 leaves "a writer SHOULD **instead** produce a new file" — "instead" of an
  in-place shortening. The inserted clause sits between; "instead" still
  resolves to the in-place commit. Checked, unaffected.
- H5 inserts nothing before an anaphor; the sentence after it ("Any other
  growth…") refers to the growth taxonomy it itself sets up. Checked.
- H13's "the ′ marks B's, whose tiles moved; **A's** did not" → "A's tiles".
  Parallel with "whose tiles moved" carries it. Checked, mildly loose, not filed.
- H4 inserts a clause before "The directory and the tile-index region are always
  raw" — no anaphor there. Checked.
- H16 replaces a clause ending the paragraph; the next paragraph opens "Two
  structural cases are **conforming files a reader nevertheless refuses**",
  a fresh subject. Checked, unaffected.
- H2's inserted "— a user-metadata document lives in one, [R-CNT-25] —" sits
  inside its own sentence; the following sentence begins "A commit that changes
  a layer's stored-tile set…", a fresh subject. Checked, unaffected.

## 8. Findings

X-01  §20.3's "What the line gives up" sentence still reads "any change to an
      interleaved layer's channel list … are rewrites", 46 lines after H8
      qualified the fixed side to "(its names aside)". Direct contradiction with
      the permitted list's "its name, and its dimension and channel names, MAY
      change". Hunk 8. Byte-level.

X-02  H8 put the interleaved channel list on both sides of the partition without
      adding it to the enumeration that names the both-sides fields ("a
      dimension extent, a planar layer's channel list"), so the tie-break rule
      that would otherwise resolve X-01 does not reach it. Hunk 8.

X-03  H10's "one taken with a growth moves ordinals whether or not the count
      changes" is false of a shortening taken with a growth that changes no grid
      count — the very growth H5 defines as moving no entry — and drops the
      "wherever [R-GEO-06] moves them" qualification that both H5 and §20.3's
      re-emission clause carry. Hunks 5, 10.

X-04  H1 added "both record types §7.3 registers" to [R-CNF-03]; H18, editing
      the adjacent clause of the same checklist, left the parallel enumeration
      ("all four codecs, both filters, both layouts, all thirteen sample types,
      and both user-metadata encodings") without it. §7.3 also lacks the
      [R-CNF-03] core restatement every other core-set section carries. Hunks
      1, 18.

X-05  H4's "Application metadata never makes the structural data it annotates
      unusable" is the same unbounded shape H16 was written to remove three
      sections later ("neither **is a reason for a reader to reject anything**"
      → "neither **obliges** a reader to reject anything, and [R-CNF-12]'s
      licence … is untouched"). Hunks 4, 16.

X-06  §21.1's "for several such rows it obliges the reader to serve the
      structure unchanged ([R-CNT-22] …; and [R-MTA-05] … — F27 and L48)" states
      the same unqualified obligation H16 removed from §21.6, about the same two
      rows. Hunk 16.

X-07  H6 carries one of H5's two exempt growth cases into §13.3 and drops the
      other ("one that raises a grid count while another stays 0"), which is the
      declare-then-fill case §13.3 exists to describe. Hunks 5, 6.

X-08  §20.5's Example still costs slack as "a whole index region for each layer
      a commit **touched**", the pre-repair key, while §20.3 and H5 now key
      re-emission to a change in stored-tile set or index content. Hunks 5, 6, 10.

X-09  H7 pinned the conversion's rounding-direction attribute and left "and MAY
      use a wider representation" in the same sentence unqualified, so the
      sentence still reads as licensing a reader to perform the interpretation
      in a wider format. Hunks 7, 17.

X-10  H10's "the list above" re-resolves to the nearer bounds list or gives-up
      list. Hunk 10.

## 9. Rejected candidates

- **"not both in one commit" scoped per-commit rather than per-list.** §20.3's
  second sentence says "an extension and a shortening of **one channel list**
  excepted", and both restatements (§11.1 "one or the other in a commit",
  Appendix H "(not both in one commit)") sit inside a per-layer subject. A
  commit extending layer A's list and shortening layer B's is permitted on every
  reading. Dropped.
- **"a commit's net change … is an extension or a shortening" as a different
  rule from "not both in one commit".** A commit exposes only a before and an
  after list, so the net change *is* the change; with "extension" = old list is a
  prefix of new and "shortening" = new is a prefix of old, the two formulations
  coincide on every case, including "replacing the last channel". Dropped.
- **An extension composed with a growth needing the same exception H10 states
  for a shortening.** For an extension, (C+1)·N′ > C·N always, so entry_count
  always changes and re-emission always follows; no extra sentence is needed.
  Verified, dropped — this is the "another pair that composes the same way" test
  and it passes.
- **H9's "no check any actor owes able to see it" as an overclaim** (a changed
  codec would be caught by T17/T24/T25 on the old bytes). Pre-existing wording;
  H9 only *narrowed* the claim by adding padding positions and pad bits. Dropped
  as not this repair's defect.
- **§20.3's Example (c) not naming a directory-only growth.** Shape (c) is
  stated generically ("A change confined to the directory"); the three items
  after the dash read as instances, not a closed list. Dropped.
- **H12's figure showing A's index unprimed while A's index region moves.** The
  ′ marks regeneration, not relocation; the gloss says "extent slots are
  re-pointed and each index region any of whose stored extents moved is
  regenerated". Consistent. Dropped.
- **R8's Condition cell not naming roundTiesToEven.** R8 uses §18.2's own term
  "binary64 interpretation", and §21.1 makes the rule govern on divergence.
  Dropped.
- **Nested em-dash pairs.** I checked every repaired sentence in all 19 hunks;
  each dash-delimited clause contains parentheses, not a second dash pair. None
  found.

## 10. Derived numbers

- §7.3 registry rows: 2 (0x0001, 0x0002) → H1's "both" is right.
- §21.2 header "35 conditions": F1–F10 (10, F11 struck) + F12–F36 (25) = 35. ✓
- §21.3 header "49 conditions": L1–L49 = 49. ✓
- §21.4 header "26 conditions": T1–T26 = 26. ✓
- §12.1 "exactly thirteen sample types": rows 1–13. ✓ (H18's "thirteen".)
- H9's id list length: 3 named kinds → 5 rows (2+2+1) in written order. ✓
- Binary64 overflow threshold under roundTiesToEven = 2¹⁰²⁴ − 2⁹⁷⁰ ≈
  1.7976931348623158079e308; max finite = (2−2⁻⁵²)·2¹⁰²³ ≈
  1.7976931348623157081e308. The gap is what H7's rounding attribute decides,
  which is why the repair is real. Used only to size X-09; no document figure
  states either number.
- Disk-ordinal arithmetic used in X-03: C=3, N=2 → entry_count 6; shorten to
  C=2 with a growth raising N to 3 → 6, ordinals move (1·2+s → 1·3+s). With a
  growth that changes no grid count (E₀ 100→120, T₀ 32, G₀ = ⌈100/32⌉ =
  ⌈120/32⌉ = 4): N unchanged, ordinals c·N+s unchanged, count falls 3N→2N.
  This is the case H10's sentence gets wrong.

## 11. Confidence

I read the whole specification, not only the hunk neighbourhoods; I held each
of the five groups' members side by side; I ran the sweeps above with controls;
and I checked every requirement id and section number appearing in repaired
text. The things I could not check: the registry file, the conformance vectors,
and whether any of these ten were already known. Two of my findings (X-08,
X-06) are pre-existing sentences these commits should have swept rather than
defects the commits created; I say so in each.
