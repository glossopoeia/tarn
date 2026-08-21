# Maintainer's independent pass over round 17's repairs

Written before reading any auditor's return, so that the reconciliation has an
independent column. Ten hunks, commit `08b9b9d..a42d0b6`.

## Clean in this pass

**Hunk 8 (Appendix G, `file_id` fallback).** `0x0000000000000001` is
determinate: `file_id` is u64 (§6.2's trailer table, offset 48), the substituted
value is a value not a byte string, and the trigger — the digest's last eight
bytes all zero — is a test a writer can perform. `(§6.2 forbids file_id = 0)`
resolves: §6.2 spans 735–784 and states `file_id ≠ 0` at both 750 and 776. No
stale "any other fixed nonzero value" survives anywhere (`phrase.py "fixed
nonzero"` → 0 occurrences).

**Hunk 9 (Appendix G, "any *remaining* record extents").** I suspected this of
being an unexplained restrictor and it is not — it is necessary. §7.4 (line
1002): "A layer record's extent slot addresses the layer's tile-index region",
and §5.2's walk (line 1333) confirms the region "enters the walk once, as that
record's extent". A tile-index region therefore *is* a record extent. Item 3
places every layer's index region in its first clause; without "remaining", the
second clause would place them again. The order is total and each extent is
placed exactly once: layer-record extents (index regions) in clause 1,
top-level and layer-sub-record extents in clause 2, directory last.

**Hunk 6 (§21.7, T3/T14).** The assignment is correct and not swapped. T3
(3458) tests "the decoded payload's byte length"; T14 (3469) tests "a
non-sentinel index entry's length", under codec 1. Matches the repair.

**The §20.4 chain, as far as it goes.** "Superseding a stored tile's bytes
re-places that layer's index region" holds for every supersede, not just the
common case: line 607 states the rule as "a commit that changes a layer's
stored-tile set **or index content**", and a supersede changes index content
(entry offsets). Re-placement moves `extent_offset` and changes
`crc_of_crc_array`, so the layer record is modified.

**No orphan left by the deleted carve-out.** `phrase.py "MUST retain"` → 1
occurrence, the drop-only-commit rule, still valid. `"only change is a
supersede"` → 0. `"may drop"` / `"dropped"` → four restatements (3110, 3144,
3164, 3527), none of which restates the scope-change condition, so the
widening stranded nothing.

**Gates, before any edit of mine:** `tarn_check` PASS 0 findings / 7 warnings;
`tarn_build --selftest` Appendix A byte-identical; `tarn_vectors --verify`
isolation clean, 121 rows; `tarn_propagate` nothing to propagate; lineage grep
zero matches.

## Findings

**M1 — hunk 1 against hunk 2, same commit, unswept.** §11.1's Rationale (1488)
says "A layer that **stored** nothing may be re-declared **freely.**" — bare.
§20.3's example-(c) Rationale (3083), edited in the *same commit*, says
"re-declared **freely, subject to every rule its new geometry is subject to**".
One commit, one rule, two restatements, only one qualified. Both sit in `>`
blocks so neither carries force ([R-CNF-01]) and the governing normative text
is §20.3 step 4 at 2986–2988 — so not byte-level. But this is exactly the shape
`tarn_propagate` cannot see, being two passages written to disagree in the same
commit, and exactly the shape that has produced a byte-level defect in each of
the last four rounds.

**M2 — hunk 3, stranded word.** "Dropping the record, or dropping another
record in the same commit, is not itself such a change **either**". "Either"
chains onto a preceding negative — round 16's "Superseding … is **not** such a
change for either kind" — which this repair reversed into a positive ("which
**is** such a change"). The word now has no antecedent.

**M3 — hunk 3, circular citation.** "an appender never removes one **(§20.4)**"
cites the section the cell is in. The sentence that would support it, at 3125,
opens "No commit **therefore** removes a layer record" — it is derived *from*
this table. The real ground is that both registered types carry PE = 1
(`[R-CNT-22]`, §7.3), stated at 3126.

**M4 — hunk 3, three nested em-dashes.** "…the file's layer set — which a
commit changes by adding a layer and equally by modifying any layer's record —
an appender never removes one (§20.4) — or another *non-layer* top-level
record." Clause boundaries are genuinely ambiguous: the trailing "or another
non-layer top-level record" has to reach back past two dashes to attach.

**M5 — hunk 3, "layer set" stretched past its meaning.** The cell stipulates
that a commit changes "the file's **layer set** … equally by modifying any
layer's record". A set does not change when a member's contents change. The
scope being named is really "the file's layer set, or any layer record's
content". A cleanroom reader is likely to file this, and it is the wording, not
the decision, that is at fault.

**M6 — hunk 3, the widening's reach, for Rob.** Under it, a top-level
MU = 0 / PE = 0 record may be dropped by an appender in *any* commit that
modifies any layer's record — which is every commit that appends tiles,
supersedes a tile, grows an extent, renames a layer, or changes a fill. The
word "*independently*" and the scope machinery now exclude only the drop-only
commit. That may be exactly what was intended, but round 17 framed the decision
as resolving a MAY/MUST contradiction, and this consequence was not on the
table. Not a defect; a decision whose scope should be seen.

**M7 — hunk 4 against untouched §20.5, local contradiction.** §20.5 at 3160
states the general rule as "MUST NOT emit a file carrying a violation **it has
detected**" — conditioned on detection. The repair at 3190 states its
obligation unconditionally: an entry classified reject-tile on a structural
ground "**obliges the compactor to refuse**". The repair then concedes at
3196–3198 that "a compactor **need not have looked**; where it has, this is the
disposal" — which conditions on detection again. Unconditional MUST and
"need not have looked" sit in the same parenthetical, and the untouched
sentence 30 lines above takes the detection side. The citations themselves all
resolve: §20.1 (2868) does say a compactor "satisf[ies] every writer
requirement for the bytes [it] produce[s]", and `[R-WRT-01]` (2871) does limit
the travelling licence to "a structure they neither modify nor rely on".

**M8 — hunk 5, citation widened from verifier to reader.** The repair says a
decline on the size bound is what "`[R-MTA-09]` makes **that actor's**
capability", for "a **reader or verifier**". `[R-MTA-09]` says that of the
verifier only: "the bound is that **verifier's** capability … a **verifier**
MUST NOT report it as one" (2467–2469). For a reader it says something
different — an over-bound document "is ignore-record like any other it cannot
read" (2463). The carve-out's substance is right; its attribution is not.

**M9 — hunk 7, paraphrase broader than the source.** "the two capability
refusals §21.6 names, a foreign format major and an **unimplemented MU = 1
type**". §21.6 (3549–3558) names, as its second case, an **experimental-range**
record type carrying MU = 1. "Unimplemented MU = 1 type" also covers the
reserved-range case, which §21.6 expressly makes a violation (F35, F36, L24,
L25), and the registered-but-unimplemented case §20.4 (3121) treats as
reject-file. The count of two is right; the description of the second is not.

**M10 — hunk 10, citation points at the definition, not the obligation.** The
verifier checklist now reads "decoded-content obligations — padding samples,
pad bits and interleaved boolean bytes (§14.5, **§14.3**, §14.2)". §14.3
*defines* pad bits (1893); the *obligation* is §14.5 at 1957, "Every pad bit
(§14.3) MUST carry the plane's [fill]", and row T5 cites `[R-SER-05]`. The
writer checklist two paragraphs earlier (4284) cites "`[R-SER-05]`, §14.5" for
the same thing. A list of obligations should cite the obligation.

**M11 — hunk 6, "witnessed by T3 or T14" reads exhaustive.** A declaration
change that reaches *the codec* — say 1 → 2 — is most likely witnessed by T25
(a stream that fails to decode), not T3 or T14. Naming fewer witnesses than
exist is the safe direction in a section about what is *undetected*, so this is
low severity, but the sentence promises more closure than it has.

## M12 — the finding no spec-only agent could reach: round 17 reversed an
## Accepted ADR in spec text and recorded nothing

`git log 08b9b9d..HEAD -- docs/decisions/` is **empty**. Round 17 changed
`spec/tarn.md` by 32 insertions and 22 deletions, including the deletion of a
normative MUST and the widening of a normative MAY, and added no ADR.

The deleted carve-out is the subject of **ADR-0070, "A supersede-only commit
drops nothing"**, `Status: Accepted`, dated 2026-08-17, whose decision reads
"so a commit whose only change is a supersede **MUST retain** the record"
(line 39). `spec/tarn.md:3123` now reads "an appender superseding a tile **MAY
drop the record**". Nothing supersedes ADR-0070; `grep -rn "0070"
docs/decisions/*.md` finds no other ADR referencing it.

So the repository currently holds an Accepted ADR and a normative spec
sentence that decide the same question opposite ways. This breaks three
standing rules at once: AGENTS.md §2 ("Decisions are ADRs … supersede, never
rewrite"), AGENTS.md §4 ("Spec text encodes Accepted decisions only"), and the
ADR-before-or-with-the-text rule.

**Why seventeen rounds could not find this.** Every cleanroom agent reads
`spec/tarn.md` and nothing else — that is the gate's whole design. A
contradiction between the spec and the decision trail is invisible from inside
the spec. It is not a defect the instrument is pointed at, and no amount of
running it again would have surfaced it. The repair audit found it only
because the audit is allowed to look at the commit.

This also re-reads round 17's own verdict. Round 17 called its survivor "the
direct consequence of a decision taken the same day" and closed it by
maintainer decision. The decision was taken and applied; it was never
recorded. The round's finding was therefore half-dispositioned, and the
process rule that would have caught it is the one the round did not run.

## Vocabulary drift noticed in passing

§21.7 names the same triple three ways within eleven lines: "boolean bytes"
(3577), "an interleaved boolean" (3590), "a boolean byte" (3599). Appendix H
(4316) says "interleaved boolean bytes". Only the interleaved layout has
boolean *bytes*; packed planar bool has bits. Not wrong in context, but the
bare "boolean byte" at 3599 is the newest of the four and the least precise.
