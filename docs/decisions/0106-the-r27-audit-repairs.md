# 0106. Six defects from the round-27 audit, five of them this week's own repairs

- Status: Accepted (resolves the ADR-0102/0103/0105 audit)
- Date: 2026-08-25
- Covers: §6.2's and §7.2's declaration-derived sums; `[R-CNT-17]`'s index-region
  length; §17's preamble; §2.3's `[R-CNF-13]`; §21.2's preamble; Appendix G item 5
- Revises: repairs written by ADR-0102, ADR-0103 and ADR-0105
- Confirm: none

## Context

Three cycles were audited together — twelve hunks, eighty inserted lines, the
largest diff this instrument has been given. Three auditors returned **twenty-five
findings, eight self-flagged byte-level**. The per-auditor cap of 4 left thirteen
ungraded, so a second pass grouped those thirteen into eight distinct defects and
re-ran them alongside a refute pass on the four downgraded byte-level flags.

**Six defects were confirmed, and five of them were introduced this week.** Two
of the four refute attacks overturned their downgrades. The honest summary is
that this was the worst repair batch in the project's record.

## Decision

**§17's scope statement is deleted, not narrowed.** ADR-0103 added "Every rule in
this section ranges over **stored** tiles … and satisfies these rules vacuously",
meaning to state one property instead of three qualifiers. It was false twice
over. `[R-COD-07]`'s cap is quantified over a layer's **addressed** tiles, which
§21.9 states in normative text — "*Decoded size of one tile* ranges over a
layer's **addressed** tiles, **stored or not**, exactly as `[R-COD-07]`'s cap is"
— so the sentence contradicted the document outright, and that was graded
byte-level. And the universal is wrong under *any* tile set: `[R-COD-03]` and
`[R-COD-09]` constrain the layer record's codec and filter fields and
`[R-COD-11]` a verifier's certification, so three of §17's eleven rules range
over no tile at all. Changing *stored* to *addressed* would have left a
known-false quantifier standing, which is why the sentence goes rather than
moves. `[R-COD-04]`'s explicit "non-sentinel" qualifier, added in the same ADR,
already does the work the blanket was invented for.

**`[R-CNF-13]` re-quantifies from a requirement to a condition**, and this is the
defect that mattered most. ADR-0105 wrote reach over *requirements*. But
`[R-CNT-06]` is a single requirement stating **ten** conditions and governing ten
§21.2 rows, of which only the trailer magic and the trailer CRC assert invariants
`[R-CNT-24]` fixes; the other eight assert `dir_offset ≥ 16`, `file_id ≠ 0`,
reserved bytes zero and the rest, which `[R-CNT-24]` fixes nothing about. **A
per-requirement test therefore could not produce the row set §21.2's own preamble
claimed to derive from it** — it had to reach all ten rows or none. A refuter
built the fork explicitly, with a reader implementing majors 1 and 7, which
`[R-CNF-13]`'s own text contemplates. Reach is now per condition, as §21.1
individuates them, and the rule says why.

**§21.2's preamble stops claiming a precedence §21.1 does not grant it.** It said
"where this restatement and that rule diverge, the rule governs (§21.1)". §21.1
grants that exactly twice, to *rows* — "each row is one malformed condition" —
and to §21.6's entries. A preamble paragraph is neither.

**Appendix G item 5 stops asserting a universal at all.** ADR-0103 replaced
"changes the stored bytes of every tile it touches" with "any tile whose shuffle
stride exceeds 1", which is also false: `[R-COD-10]` puts byte *i* of group *j*
at offset *i·n + j*, so at **n = 1** the permutation is the identity at every
stride, and n = L/s = P = ∏ Tᵢ. Every layer with all tile extents 1 is a
counterexample, and `[R-GEO-01]` permits Tᵢ = 1. The item now names the property
— the filter is the identity exactly where its permutation is — rather than any
universal over tiles.

**Three stranded quantities regain their designation.** ADR-0102 narrowed
`[R-ENC-04]` to quantities the specification expressly designates, and did not
sweep the register against the new boundary. L2 enumerates nine derived
quantities and F3 a tenth; §11.2, §14.2 and §14.3 designate six of them. The
remaining sums — `dir_offset + dir_length` (§6.2), `extent_offset +
extent_length` (§7.2), and `entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`
(`[R-CNT-17]`) — were designated nowhere, so rows registered overflows the rule
no longer reached. Each is now designated where the quantity is defined.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. No cell
changes; the three designations restore reach to instances L2 and F3 already
carried, so their vectors stand.

One propagation acknowledgement, for `[R-CNT-06]`, which `[R-CNF-13]` now names
by way of explaining the per-condition quantifier.

**What this batch shows about repair, and it is not comfortable.** Two of the
five repairs reproduced the exact shape they were fixing: a false universal was
replaced by a narrower false universal in Appendix G, and three per-rule
qualifiers were replaced by a blanket in §17 that was false of more rules than
the qualifiers had covered. Both were written quickly, in text nobody re-read
around, and both passed every mechanical gate. **A repair that generalises is a
new claim about the whole passage, and it needs the same derivation a new rule
needs** — ADR-0095's lesson about counts, which turns out to apply to
quantifiers with equal force.

**On the audit's own coverage.** Twenty-five findings against a cap of four per
auditor left thirteen ungraded — more than half — and two of the six confirmed
defects came out of that starved set. A cap sized for a three-hunk diff was
carried unchanged onto a twelve-hunk one. The cap must scale with the diff, and
until it does the DROPPED log is the only thing standing between a starved audit
and a clean-looking one.

## Precedent

- ADR-0095's rule that a partition stated by a property beats a list, and its
  limit: a property is only better than a list if it is *true*, and this batch
  produced two that were not.
- §21.9's "addressed tiles, stored or not", which is the sentence that made §17's
  blanket a contradiction rather than a looseness.
- ADR-0081's repair audit, which found all six of these before a fresh-context
  round read a line of them.
