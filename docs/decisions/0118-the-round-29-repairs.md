# 0118. Round 29's nineteen checkable repairs

- Status: Accepted (resolves round 29's repairable findings)
- Date: 2026-09-02
- Covers: §2.4 `[R-CNF-12]`; §9.6 `[R-LIF-06]`; §11.1's Rationale; §16.2
  `[R-SLB-04]`; §18.2 `[R-MTA-09]`; §19.3 `[R-RDR-03]`; §20.3 step 4
  `[R-WRT-04]`; §20.5 `[R-WRT-06]`, `[R-WRT-07]`; §21.1; §21.2 row F18 and its
  preamble; §21.6; §21.7 `[R-ERR-01]`; §21.9 `[R-ERR-05]`; Appendix G item 5.
  By the erratum: §2.3 `[R-CNF-13]`; §18.2's Note; §20.5's Example;
  §21.9 `[R-ERR-04]`; Appendix H
- Confirm: none
- Erratum: 2026-09-03 — the pre-round-30 audit changed ten of these repairs and swept four neighbours; see the Erratum section.

## Context

Round 29 returned 26 distinct defects. Five were decisions and are ADR-0117; one
was the front-matter *structural* gloss, repaired with the block's relabelling;
one was §14.2's layout qualifier, repaired with decision 2. **The nineteen here
are the remainder — each checkable against a named rule, none byte-level.** They
are recorded in one ADR because they are one round's findings and each is small;
five touch register cells, which is why an ADR is required at all (ADR-0104).

## Decision

**§21.7 and its restatement in §21.1 — the detectable clause's third quantifier.**
Three reporters found that *"separated by such a check"* admits two scopings: one
check separating the file from all others, or a possibly different check per
comparison. Only the distributive reading makes *unwitnessed* and *detectable*
exact duals, which the same paragraph asserts, and only it leaves F35 its row.
Both sites now say **some** such check, *"which need not be the same check for
every one of them."*

**§2.4 `[R-CNF-12]` — §21 inventories the verifier's duty, it does not bound it.**
*"runs to the MUST-level conditions §21 inventories"* reads as a restriction to
what §21 lists, which would make §21.7's account of unregistered obligations
incoherent. Now appositive: *"runs to MUST-level conditions, which §21
inventories"*.

**§20.3 step 4, five repairs to one numbered step.**

- The §14 bar's list named padding positions but never the pad bits §14.3 gives a
  packed planar bool plane, though `[R-SER-05]` fixes content at both and T5
  registers the pad-bit case. The list now names both.
- The same list said *"the byte offset of any **sample**"* where §14.2 defines the
  **value** offset and §3.1 separates the two. It now names the value.
- The growth permission was reading as an application of the bar's carve-out. It
  is not: the carve-out reaches a position whose stored byte already holds the
  fill it keeps, not one that ceases to be padding. Stated as an exception the
  permission supplies rather than one the carve-out does.
- The shrink sentence's *"This is precisely where…"* had no named antecedent. Now
  *"A shrink whose damage falls on a tile the new state no longer stores is
precisely where the §14 bar has no witness"*.
- (`[R-SLB-04]`, §16.2) The slab trigger named only tile-side changes, so
  introducing or changing a slab declaration escaped it, and it was tenseless. It
  now covers the declaration itself and binds a layer slab-declared **in either
  the superseded or the new generation**.

**§20.5, three repairs.** `[R-WRT-07]` regenerated *"each relocated tile-index
region"* when what forces regeneration is a stored extent moving, not the region:
now *"each tile-index region any of whose stored extents the output relocates"*.
And *"Neither obligation has a witness in the output alone (§21.7)"* was false for
the `[R-CNT-26]` branch — on an output carrying no later-minor feature the
compactor does not implement, the stored version_minor is checkable against the
floor — and its §21.7 citation pointed at the wrong one of that section's two
grounds. Both corrected; the citation is dropped rather than requalified.

**§9.6 `[R-LIF-06]`** obliged a report of *"the candidate it settled on"* in two
reachable states where the probe settles on none. The no-candidate branch is
stated.

**§21.9 `[R-ERR-05]` — a closed count replaced by its enumeration.** *"Two do
not"* disagreed with L1 about whether the 2⁶² ceilings on A and A_slab are chosen
limits or consequences of the u64 domain. They are chosen here, and are now named;
the closed count becomes *"Some do not"*, because a count stated in prose is a
defect this project has repaired more than once.

**§21.2 F18, its preamble, and §21.6 — the cross-major claim is dropped.** All
three said version_major = 0 is invalid *in every format major version*, which
`[R-CNT-24]` does not fix. What carries the row is that version_major = 0 declares
no major at all, so `[R-CNF-13]`'s premise is unmet and `[R-CNT-07]` governs. That
is what they now say.

**§21.1's *sole resolved byte*** was attributed to §14.2; the rule is §12.3's
`[R-TYP-04]`. Reattributed.

**§19.3 and §21.7 — a parse convention is not a validation.** §19.3 listed
`[R-ENC-06]`'s fixed field widths among what a reader validates, while §21.7 says
that rule states no condition a file can exhibit. §19.3 now names *"the field
widths at which §4 fixes the parse"*, and §21.7's claim that a shifted value is
*"caught by the rows for the fields that hold them"* is qualified to where those
rows reject it.

**§18.2 `[R-MTA-09]`** said *"on the bound above"* where two bounds are stated
above. Now *"either bound above"*.

**§11.1's Rationale** said a zero-extent layer's *"last"* zero grid count, which
reads as the last-declared dimension. Now *"only remaining"*.

**Appendix G item 5** claimed the shuffle *"changes the stored bytes of every tile
it touches"*, false wherever the permutation fixes the decoded image. Qualified,
with the corollary the item exists for: a fixed image is no evidence of which
filter produced it.

## Consequences

**The register does not move**: 120 conditions, 277 instances, 331 vectors. F18's
condition text changed and its instance did not; `[R-ERR-05]` and `[R-ENC-03]`
keep their rows. Appendix A byte-identical.

**Six propagation acknowledgements**, each a site sharing a rule id with a repair
without restating it — except `[R-SER-03]` → `[R-SER-05]`, where T4, T5 and
Appendix H are the sources the §14 bar's list was extended to agree with.

**These repairs are what round 30 reads.** Round 29 met the first half of G3's
criterion; the second half is whether a round reading this work returns zero. On
this cycle's evidence the next defect is usually in the last repair, and three of
this cycle's repairs were defective in ways their own audits caught — so the
nineteen here are the text that matters most, and they are audited before the
round charters.

## Precedent

- **ADR-0104**, requiring an ADR for a register change: five of these touch cells.
- **ADR-0106**, on a passage wrong twice: applied to `[R-ERR-05]`'s closed count,
  which is enumerated rather than recounted.

## Erratum, 2026-09-03 — the pre-round-30 audit

Six lanes read the nineteen repairs above together with the one sentence
`b91e499` repaired in §21.7 — twenty-one hunks over `88e4ce6..e42509b` — and
returned 21 findings, 16 distinct defects, none byte-level. Five of the sixteen
were found by two lanes independently. Eighteen edits followed. On this cycle's
record every audited repair has been found defective in a shape different from
the defect it fixed, and this audit is no exception: **of the nineteen repairs,
five came back clean with evidence, four were sound as written but left a
neighbour unswept or a sibling quantity open, and ten needed a second repair.**
Three of the ten were cut rather than reworded.

**Ten repairs needed a second repair.**

- **`[R-CNF-12]`** (§2.4). The appositive *"runs to MUST-level conditions,
  which §21 inventories"* asserts of the whole class that §21 inventories it,
  and §21.7 says an unwitnessed MUST-level condition has no row; the
  restrictive form was the defect and the appositive re-imported it from the
  other side. Two lanes found it. The clause is cut: the preceding sentence
  already states the true direction, that the register enumerates MUST-level
  conditions only.
- **§20.5's witness sentence.** *"Neither obligation has a witness in the
  output alone, save that where the output carries no later-minor feature the
  compactor does not implement, its stored version_minor is checkable against
  the floor"* keyed checkability to the compactor's implementation set, which
  the output does not carry, and a witness is what a *checker* can establish
  from what it holds. Two lanes found it, with the three cases that separate
  the two — no later-minor feature at all, one the compactor implements, one
  it does not — the sentence wrong in both directions. It was the sentence's
  second false form, and it explained nothing the register needs: both
  obligations are SHOULDs, which `[R-CNF-12]` places outside the register
  whatever their witness. Cut, on ADR-0106's rule; the paragraph ends at
  *"Otherwise version_minor follows `[R-CNT-26]`'s floor."* The account above
  — "Both corrected" — describes the previous draft.
- **§21.7 and §21.1, the third quantifier.** *"which need not be the same check
  for every one of them"* — *them* had two antecedents, the files and the
  actors. Now *"every one of those files"*, and §21.1's *"for each"* is *"for
  each such file"*.
- **§21.7 `[R-ERR-01]`.** The qualifier *"caught by the rows for the fields
  that hold them wherever the shifted value is one those rows reject"* gave
  `[R-ENC-06]` the partially-caught shape §21.7 files as *unwitnessed* for a
  mis-strided filter while insisting the rule states no condition at all. The
  aside is cut: a structure written at other widths yields *"a different file,
  conforming or not on its own terms"*, which is the whole point.
- **§20.3 step 4, the shrink sentence.** *"A shrink whose damage falls on a
  tile the new state no longer stores is precisely where the §14 bar has no
  witness"* is a biconditional about the bar, and the bar is unwitnessed
  outside shrinks too — re-typing a channel int8 to uint8 over a stored tile is
  barred, leaves a conforming file, and no obliged check separates it — while
  *a tile* admits a shrink that also damages a still-stored one, which T4
  witnesses. Now one direction, and *only*: a shrink whose damage falls only on
  tiles the new state no longer stores leaves the live state clean, so the bar
  has no witness there.
- **§20.3 step 4, the §14 bar's list.** The renamed member *"the byte offset
  of any value within the decoded tile image"* names a byte offset where §14.3
  fixes a bit position: a packed planar bool plane with T = (2, 4) and no
  padding, re-declared (4, 2), moves value (1, 0) from bit 4 to bit 1 of the
  same byte while nothing the list names changes. The governing clause reaches
  it and the sentence after the list says the list is not the test, so the bar
  was never open — but the list is what an implementer checks. Now *"the byte
  offset — or, in a packed plane, the bit position — of any value"*.
- **`[R-SLB-04]`** (§16.2). The widened trigger still omitted an occasion: a
  geometry change that renumbers disk ordinals with N, the stored-tile set, the
  run partition and the declaration all unchanged — G = (2, 4) to (4, 2) at
  T = (1, 1) moves two stored tiles from separate runs into one, where they now
  need packing. Added: *"the disk ordinal of any tile the new state stores"*.
  Not byte-level: the output exhibits L41 under both readings.
- **§19.3 `[R-RDR-03]`.** *"the field widths at which §4 fixes the parse"*
  remained a member of a list of validations while naming no check; the list's
  closing sentence gives every member a scope its failure takes, and this one
  has none. Dropped; the exact parse `[R-CNT-18]` already in the list is where
  the widths bite.
- **`[R-ERR-04]`** (§21.9). *"stated or derived quantities"* left the scope
  list *"a layer or a tile"* still without the record scope §18.2 assigns to a
  document frame's declared window, so a reader declining an oversized
  sub-record frame had the layer or the file to choose from and §18.2's
  ignore-record was neither. Two lanes found it. The list now names *"the
  record carrying a user-metadata document, as §18.2 assigns"*. The gap
  predates this ADR; the rewording exposed it.
- **Appendix G item 5.** The repair used *fix* in the mathematical sense two
  words before *"**Fixed declared tile extents**"* uses it in the profile's.
  Reworded without the word: where the permutation leaves the image unchanged,
  the stored bytes are the same under either filter and are no evidence of
  which was declared.

**Four were sound as written and left something beside them.**

- **`[R-WRT-07]`'s re-keying** was correct, and §20.5's Example two paragraphs
  below still keyed regeneration on *"a relocated tile-index region"* while
  giving the new criterion as its reason. A labelled block disagreeing with the
  rule it illustrates is a finding wherever it lands; two lanes found it. The
  Example is re-keyed to the rule.
- **`[R-LIF-06]`'s no-candidate branch** is reachable for both kinds of tool,
  and it restated *"how many it rejected"* without *rejected* being defined
  anywhere: the paragraph used *candidate* both for a magic match and for a
  match passing the trailer gate, so the count was re-verification failures
  alone or gate failures too. *Candidate* is now defined at the gate, and the
  count is candidates rejected on re-verification.
- **The F18 sweep** left three texts agreeing verbatim — and left the ground
  they agree on, that version_major = 0 declares no major at all so the reach
  question does not arise and `[R-CNT-07]` governs, stated only in §21.2's
  preamble and §21.6, text §21.1 subordinates to the rule. Read literally,
  `[R-CNF-13]`'s *"a format major other than 1"* includes 0 and F18 would not
  reach; the register's gloss is what reconciles the two rules. `[R-CNF-13]`
  now states it, and the three register passages restate it. This is the one
  edit of the eighteen that adds a sentence to a rule, and it adds what the
  document already asserted of that rule elsewhere.
- **§21.1's reattribution** of the sole resolved byte to `[R-TYP-04]` was
  correct, and Appendix H's reader checklist still made the same claim with
  the abandoned citation (§14.2). Two lanes found it. It now cites
  `[R-TYP-04]`.

Beside these, **§18.2's Note** beneath `[R-MTA-09]` still explained
`[R-ERR-04]`'s scope test in the superseded word *declarations*; it now carries
the current term and says a document's decoded size is neither stated nor
derived. And **one sentence outside this ADR's repairs is cut**: §21.7's
operational gloss, aligned by ADR-0117's decision 1, was *"ask whether a breach
can be made to leave behind a file no obliged check separates from one that
does not exhibit the condition"* — ∃f ∃g ∀k where the definition it glosses is
∀f ∃g ∀k, one quantifier weaker, so a condition with one inseparable exhibiting
file and another separated from every non-exhibiting file is unwitnessed by the
gloss and detectable by the definition. That decision closed the gloss's
comparison class and left its quantifier; the definition is already declared
the whole of the test, and the sentence now ends at *"without appeal to a
list"*.

**Five repairs came back clean with evidence**: the pad bits in the §14 bar's
list (`[R-SER-05]` fixes content at both, checked against §14.3 and §14.5);
the growth permission as an exception (the logic done from the text: a growth
alters the set of padding positions, the carve-out covers the opposite
direction, so the MAY must be an exception); `[R-ERR-05]`'s enumeration (2⁶²
derived one step below the u64 field's largest power of two, and A, A_slab
outside `[R-ENC-03]`'s domain by L1's own instance list); `[R-MTA-09]`'s
*either* (exactly two bounds above, both declined on); and §11.1's *only
remaining* (both grid cases built). The detectable/unwitnessed duality was
computed by hand in two lanes: ¬(∀f ∃g ∀k ¬sep) = ∃f ∀g ∃k sep, exactly as
§21.7 claims.

**The register does not move**: 120 conditions, 277 instances, 331 vectors,
Appendix A byte-identical, every vector isolating its defect. Three
propagation acknowledgements covering four sites, each a site that now
restates a rule the edit sourced. Ten quotation acknowledgements, each a span this ADR quoted as new
text that the audit then changed or that this erratum quotes as superseded — which is the count a repairs ADR should
expect, and the reason `tarn_adr_quotes` exists.

## Erratum, 2026-09-03 — a repair recorded and not made

The Context above says that §14.2's layout qualifier was "repaired with
decision 2". **No commit made that repair.** `0790131` did not touch §14.2 and
nothing after it did; round 29's findings recorded the reporter's one-clause
repair as the right disposition, and it was carried into this ADR's accounting
as done. Round 30's reader found the same sentence cold, built the same
construction, and two of three passes upheld it byte-level. ADR-0119 makes the
repair — in §14.2, in row L2, and in §17.2's Note — and records the check now
owed after every repairs commit: the round's repair list against the diff,
item by item.

