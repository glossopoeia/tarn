# Cleanroom round 29 — findings

Protocol: ADR-0034, four phases, over the surface changed by ADR-0113, ADR-0114,
ADR-0115 and ADR-0116 and their repair cycles. Charter: [prompt.md](prompt.md).

## Verdict

**Zero byte-level ambiguities. The first half of G3's criterion is met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge** — twenty-third round running |
| Findings | **34**, from 7 reporters |
| Distinct defects | **26** by union-find |
| Self-flagged byte-level | **1** |
| Upheld by any triage pass | **1** (skeptic only — a split) |
| Surviving the refute phase, two neutral checkers and a hand-check | **0** |
| Harness | 13 agents, 13 returned, 0 dead walks, 0 dead triage |

Byte-level history: … → 2 → 1 → **0**.

**G3's second half is now live.** Round 30, reading round 29's repairs, must also
return zero. Five previous zeros — rounds 7, 9, 13, 23 and 25 — were each followed
by a round that found the next defect in the repairs that zero produced. That is
the shape this round's repairs have to survive.

## The one byte-level flag, and why it does not stand

### `planar-pq-designation` — `adversary-01`, §14.2 `[R-SER-02]`

§14.2 ends a layout-keyed table — planar → `P · Bᶜ`, interleaved → `P · Q` — with
the sentence *"These products and sums are declaration-derived quantities under
`[R-ENC-04]`."* That sentence carries no layout qualifier. The reporter asked
whether a **planar** layer therefore derives `P · Q` for the overflow ceiling, and
built a 256-byte file to force the question: rank 1, one dimension with E = 1 and
T = 2⁵⁹, two float64 channels, so P = 2⁵⁹ and Q = 16.

**The arithmetic is sound and was re-derived three times independently.**
`P · Bᶜ` = 2⁵⁹ · 8 = 2⁶², comfortably inside the domain; `P · Q` = 2⁵⁹ · 16 = 2⁶³,
exceeding 2⁶³ − 1 by exactly one. The geometry is legal — `[R-GEO-01]` requires
only d ≥ 1, Eᵢ ≥ 0, Tᵢ ≥ 1, C ≥ 1, and expressly permits a tile extent to exceed
its dimension's extent. So the fork the reporter describes would be real **if the
wide reading were live.**

It is not. `[R-ENC-04]` supplies its own test: *"A designation is express, made by
the section that defines the quantity; an expression this specification writes
only inside a comparison, and names nowhere, is not a designated quantity."*
§14.2 defines `P · Q` as **the decoded size of an interleaved tile**. A planar
layer contains no interleaved tile, so the quantity has no instance in it. The
designation is not withheld from planar layers — the quantity does not arise.

**Ten texts agree, and they were checked by hand rather than taken from an agent.**

- §14.2's table keys `P · Q` to the row headed **interleaved**, and the
  subsection's opening sentence is already an if/else over layout: *"In a planar
  tile of a numeric channel (§12.1), and in every interleaved tile…"*
- `[R-SER-07]`: *"**Whichever** of §14.2 or §14.3 defines a tile's decoded size…
  decoded size is a function of the layer's declarations alone — geometry,
  **layout**, and channel types."* The disjunction is express.
- `[R-COD-07]`: *"in a planar layer **each channel's plane carries its own decoded
  size** (§14.2, §14.3), and the largest governs."* False if a planar layer had a
  whole-tile `P · Q`.
- `[R-GEO-03]` states the same shape for the addressed-tile count — *"is N for an
  interleaved layer and C · N for a planar layer"* — which is the document's
  convention for a layout-conditioned designation.
- `[R-COD-10]`: *"the channel's element size for a planar tile and the sample
  stride Q for an interleaved tile."*
- **Five register rows** — L44, T3, T14, T21, T22 — each prefix *interleaved* to
  `P · Q` and *planar numeric* to `P · Bᶜ`.
- §21.1's own instance rule: *"Where the quantity a condition derives varies by
  layout, the layout formulas are materially different shapes and the cell
  enumerates them"*, with *"One instance is one distinguishable file"* — and a
  file declares one layout.

The wide reading requires taking §14.2's summary sentence in isolation from the
table it summarises, against all of the above. **That is the shape every byte-level
flag in this cycle has died on** — a sentence read without the structure governing
it — and it is why the charter added a fifth discriminator naming it.

### How it was settled, in order

1. **Triage split, 1 of 3.** Correctness and implementer graded it PARTIAL and not
   byte-level; the skeptic graded it CONFIRMED and byte-level.
2. **The refute phase fired on the split**, which is the round-17 trigger working
   as designed. Its refuter died twice on the driver and completed on the fallback,
   returning `DOWNGRADE_STANDS` — the **weak direction for a weaker model**, and
   the verdict that clears the gate, so it was not banked.
3. **Two neutral checkers, blind to the finding**, were asked to derive from the
   document alone the complete list of quantities designated for a planar layer,
   and only then to answer the specific question. Both returned **NO at high
   confidence**, with independently-assembled section lists. Deriving the whole
   list is what makes the single answer checkable.
4. **Hand-check.** Every text above was opened and read here.

**The finding is still worth a repair**, and the reporter's own recommendation is
the right one: close the question in one clause — *"each for the layout its row
states"* — which removes the ambiguity without changing any rule. That is the
maintainer's direction applied: minimise the impact of a possible misreading
rather than argue the reading.

One correction to the finding as filed: it states that L2's instance cell pairs
each formula "with its layout". L2 lists both without naming layouts; the keying
comes from §14.2's table and the five rows above. The support is real, stated a
little more strongly than L2 carries.

## Harness integrity

**The cleanest of any round in this project.**

- **13 agents started, 13 returned.** Zero dead walks, zero dead triage. One
  refuter died twice on the driver and completed on the fallback; it is the only
  agent that needed a retry, and its lane is recorded above rather than banked.
- **Every walk's transcript matches its structured return exactly**, by
  independent id-scrape: reader 5, writer 7, verifier 4, diagrams 4, register 6,
  adversary 5 — each equal to its own `transcript_finding_count`.
- **All three triage passes CLEAN on mechanical coverage** — 34 of 34 ids each, by
  set difference against the reporters' ids, and each pass's `all_input_ids_seen`
  independently complete and exact.
- **Union-find gives 26** against pass counts of 27, 26 and 28. The passes did
  *not* agree on a count, and the one that matched the merge by number
  (implementer, 26) is not the one whose partition the merge follows. Agreeing on
  a count is not agreeing on a partition, and this round shows it directly.
- **No pass ran a directory listing.** The round-27 relocation holds.

### The control-search rule earned its place on first use

The charter added a rule this cycle: a blockquote wrap inserts `> `, so a
line-oriented search misses phrases inside a labelled block, and **a zero must be
proved with a positive control**. The quiz author's first normalised search
returned zero — and it did not act on it. It ran the control, found the control
also returned zero, diagnosed its own normalisation as not stripping the
blockquote marker, fixed it, and re-ran. One of its three findings rests on the
post-fix search only.

The rule was written into the charter that morning because the project's own
phrase tool had exactly that defect. An agent that had never seen the tool
reproduced the failure and caught it by the stated method.

### Disclosures

All spec-reading agents disclosed injected context. The quiz author additionally
disclosed two **path** mismatches, unprompted and correctly: the project
instruction file placed in its context sits under `GitHub/tarn`, not
`GitHub/tarn-first-draft`, and its harness-assigned scratchpad is keyed to the
former while the brief's paths are keyed to the latter. It used the brief's paths
for everything and did not investigate. **This is the eighth round in which the
injected-context channel has been disclosed and no mechanical check in this
project can see any of it** — and the first in which the stale directory's name
reached an agent through the runtime rather than through a charter.

## Disposition

**Zero findings are left without a disposition.** None is byte-level.

### To the maintainer — these are decisions, not repairs

Per the standing direction that prose is not expected to converge and that a
passage too difficult to disambiguate goes to human disposition rather than a
further rewording.

| Defect | Why it is a decision |
|---|---|
| §21.7's *exactly where* biconditional against the rows the register carries (4 reporters) | Three options, and the passes name it as a choice that must be made rather than left: weaken the biconditional to the one direction §21.1 states, or change what the register carries. It moves register semantics. |
| R8's Instances cell: 2 or 4 instances | Deciding it either way moves §21.8's total from 275 to 277. A register count, so ADR-0104 applies. |
| `[R-CNF-01]`'s closed exception list vs the front-matter block's self-labelling | The repair proposed is a change to the normativity rule itself. |
| `[R-LIF-02]`'s durability barriers and where conduct rules are declared | A classification question about the document's own scheme. |
| Appendix G's profile: whether tiling and layout are closed or are inputs | A scope decision about what the profile promises. |

### Repairable, each checkable against a named rule

`detectable`'s quantifier scoping (3 reporters) · `[R-CNF-12]`'s duty scope ·
Appendix G item 5's shuffle universal (2) · §21.1's *sole resolved byte*
misattribution (2) · the §14 bar's growth carve-out · §20.5's witness claim on the
`[R-CNT-26]` floor · the shrink sentence's unnamed antecedent · §20.5's §21.7
citation · `[R-WRT-07]`'s regeneration trigger · `[R-ERR-04]`'s *declarations* ·
`[R-LIF-06]`'s missing no-candidate branch · `[R-SLB-04]`'s trigger limb · the §14
bar's list omitting pad bits · the front-matter *structural* gloss · §19.3's
`[R-ENC-06]` item · `[R-ERR-05]`'s *Two do not* count · F18's cross-major claim ·
§14.2's layout qualifier · the §14 bar's *sample* vs *value* offset ·
`[R-MTA-09]`'s *the bound above* · §11.1's *last* zero grid count.

Five touch register cells and so need an ADR under ADR-0104.

## What the round says about the surface it read

The charter told the round that heavy recent attention predicts defects rather
than correctness, and asked it to put §21.7's new test to requirements itself.

It did, and the test held: **no reporter found a requirement the test fails to
decide.** What they found instead was concentrated at the test's *edges* — the
biconditional's direction, the quantifier scoping of *detectable*, and how
`[R-CNF-12]` and §19.3 reach the same ground from outside. Four reporters
converged on the first and three on the second, which is the widest convergence
this round produced.

That is a different result from the four repair audits that preceded it. Those
found the section's prose wrong about itself; this round found the section's rule
sound and its boundary with three neighbouring rules underspecified. The cut
ADR-0116 made is part of why: there is no longer an illustration to be stale.
