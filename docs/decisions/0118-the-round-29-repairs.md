# 0118. Round 29's nineteen checkable repairs

- Status: Accepted (resolves round 29's repairable findings)
- Date: 2026-09-02
- Covers: §2.4 `[R-CNF-12]`; §9.6 `[R-LIF-06]`; §11.1's Rationale; §16.2
  `[R-SLB-04]`; §18.2 `[R-MTA-09]`; §19.3 `[R-RDR-03]`; §20.3 step 4
  `[R-WRT-04]`; §20.5 `[R-WRT-06]`, `[R-WRT-07]`; §21.1; §21.2 row F18 and its
  preamble; §21.6; §21.7 `[R-ERR-01]`; §21.9 `[R-ERR-05]`; Appendix G item 5
- Confirm: none

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
