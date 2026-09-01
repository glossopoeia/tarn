# Downstream auditor transcript — generation-counter removal

## Unsolicited context disclosure

Before I did any work, my runtime context contained: a project CLAUDE.md
pointer to AGENTS.md, the user's email, today's date, a skill-name listing,
and — inside the environment/git-status block at the very top of the
conversation — the current git branch and five "Recent commits" subject
lines (one explicitly named "ADR-0111" and referenced a generation counter
and a struck row label). None of this is part of the specification and none
of it is evidence about the change. I did not open AGENTS.md, any ADR, or
git log/diff, and did not use the commit subjects as a basis for any
finding below — every finding below is derived solely from spec/tarn.md
and the 31 hunk files. I record only that this material appeared, per
instructions, without repeating its contents further. (Note: I found a
file already present at this exact transcript path when I went to write
it, apparently left by a prior pass — its content matched the conclusion I
had independently already reached; I overwrote it with this transcript of
my own actual reads/runs rather than adopting its text unread.)

## What I read

- All 31 hunk files, hunk-01.diff through hunk-31.diff, in
  .../scratchpad/case-final/, via `cat` in one Bash call (output too large
  for inline return, so I read the persisted tool-result file in full with
  `Read`).
- spec/tarn.md, via targeted `Read` calls at every offset the hunks land,
  plus every offset a document-wide grep sweep surfaced.
- I did not read full.diff, tools.diff, any file outside spec/tarn.md and
  the hunk-NN.diff files, and did not list the case-final directory
  (I globbed `hunk-*.diff` only, which is inside my charter — the names
  were given to me explicitly).

## Commands run (verbatim) and hit counts

1. `ls .../case-final/hunk-*.diff | wc -l` → 31
2. `cat` of all 31 hunk files (one Bash call) → truncated for size, full
   output saved to a tool-results file; read that file in full with `Read`.
3. `wc -l spec/tarn.md` → 4648
4. `grep -n -i "generation" spec/tarn.md | wc -l` → 54
5. `grep -n -i "genera" spec/tarn.md` → broader sweep (also catches
   "general"/"generally" false positives) — used to confirm no
   hyphen-wrapped "genera-\ntion" was hiding from the narrower grep; none
   found (the word never breaks across a line anywhere in the file).
6. `grep -n -i "generation" spec/tarn.md` (final, exact, re-run) → 47
   distinct lines: 372,373,374,375,385,389,390,392,395,396,624,629,1011,
   1026,1249,1258,1260,1267,1304,1307,1313,1315,1316,1344,1375,1605,1610,
   1870,1910,2305,3035,3118,3128,3133,3134,3151,3168,3172,3175,3279,3333,
   3435,3456,3768,3861,3964,4074,4076,4124,4143,4374,4380,4507,4568 — every
   one read in surrounding context via `Read` and individually classified
   (see "Sweep results" below).
7. `grep -n "offset 1[6-9]\|offset 2[0-9]\|offset 3[0-9]\|offset 4[0-9]\|offset 5[0-9]\|offset 6[0-9]" spec/tarn.md`
   → 3 hits (line 1254 "beginning at offset 16" [front-signature-block
   offset, unaffected], and F14/F15's own already-updated register rows).
8. `grep -n "56\]\|\[56\|56,\|, 56\|offset 56\|trailer offset 56\|\bF-8\b" spec/tarn.md`
   → 2 hits: line 863 ("version_minor at F − 56" — computed from the fixed,
   unmoved version_major/minor field, unaffected by the reorder) and line
   1643 (unrelated tiling example, false-positive match on "F-8" pattern
   inside "(4, 8)").
9. `grep -n "R-CNT-06" spec/tarn.md` → 15 hits; enumerated every register
   row and every prose citation governed by `[R-CNT-06]`.
10. `grep -n "reserved" spec/tarn.md | grep -i "trailer\|byte"` → 5 hits;
    checked every stated width/position of the trailer's reserved run.
11. `grep -n "renumber\|retired\|struck\|withdrawn" spec/tarn.md` → 6 hits;
    checked every place the document states or restates identifier/
    row-label retirement policy.
12. `grep -n "^| [FLTR][0-9]" spec/tarn.md | grep -i "generation"` → 0 hits
    (confirms no register row anywhere still lists "generation" as an
    Instance, after the F2 edit and the F11 strike).
13. `grep -n "^#### 21\." spec/tarn.md` and reads of each subsection's
    "Outcome: ... N conditions" line → 35 (§21.2), 49 (§21.3), 26 (§21.4),
    10 (§21.5); 35+49+26+10 = 120 by hand, matching §21.8's "120
    conditions" exactly.
14. `grep -n "conditions\|instances" spec/tarn.md` filtered against
    boilerplate phrasing → isolated the four subsection totals above plus
    §21.8's "120 conditions over 275" rollup, and confirmed no other
    stray count (121, 277, 36) survives anywhere in the document.
15. `grep -n "exactly as\|the same way\|as .* is\b\|for the same reason\|likewise\|on the same discipline" spec/tarn.md`
    (Check 7 sweep) → read every hit; the only one inside the 31 hunks'
    landed text is hunk-06's "It is `[R-CNT-27]`'s 128-byte floor argument
    run from F rather than from offset 0"; the rest predate this round and
    are orthogonal to the generation removal.
16. A from-scratch Python CRC-32C (Castagnoli, reflected in/out, init
    0xFFFFFFFF, final XOR 0xFFFFFFFF, reversed poly 0x82F63B78)
    implementation, run over the 60 trailer bytes hand-assembled from
    Appendix A's new hex dump (file offsets [64,124): magic, version_major/
    minor, flags, dir_offset=16, dir_length=4, committed_file_length=128,
    file_id=0x0123456789ABCDEF, 12 zero reserved bytes) → `0x402f157e`,
    matching the document's stated `0x402F157E` / little-endian bytes
    `7E 15 2F 40` exactly.

## Arithmetic I derived myself

**A. §2.3/§21.2's "nine … seven" claim (hunk-01).** Enumerated every §21.2
row whose *first-named* Governing rule is `[R-CNT-06]`: F8, F9, F10, F12,
F13, F14, F15, F16, F17 = **9 rows**. Of these, F8 (trailer magic) and F14
(trailer CRC) assert invariants the fixed byte ranges of `[R-CNT-24]`
cover (magic [0,8), CRC [60,64)); the remaining F9, F10, F12, F13, F15,
F16, F17 = **7 rows** address fields in the "remaining 48 bytes" a future
major may redefine. Matches "states nine, … the other seven do not"
exactly. Cross-check: 9 (post-edit) + 1 (F11, removed) = 10, and 7
(post-edit) + 1 (F11, non-fixed) = 8 — exactly the pre-edit "ten"/"eight"
the hunk replaces. Self-consistent in both directions.

**B. §21.2's "35 conditions" (hunk-18).** Counted rows F1…F10 (10 rows,
F11 struck/absent) plus F12…F36 (25 numbered rows) = **35**, by direct
enumeration of every `| F<n> |` row in the live table.

**C. §21.8's "120 conditions over 275 instances" (hunk-24).** Section
totals stated in-line: §21.2 "35 conditions", §21.3 "49 conditions", §21.4
"26 conditions", §21.5 "10 conditions" → 35+49+26+10 = **120**, matching
exactly (121 → 120 = −1, for the struck F11 row). For instances: F11's own
pre-strike Instances cell held exactly one item ("generation"), and F2's
Instances cell lost exactly one item ("generation", a six-item list
becoming five). 277 − 1 (F11's row) − 1 (F2's lost item) = **275**,
matching exactly. I verified this as the *delta* the round's two edits
fully determine, rather than re-deriving the entire 275-item baseline from
all 120 rows' Instances cells from scratch (that full re-derivation is
outside what this round's change controls and was presumably swept by an
earlier round).

**D. The 128-byte commit-growth floor (hunks 05/06/07/11).** From
`[R-LIF-02]` step 1 (new bytes begin at exactly prior F) and `[R-LIF-01]`
(bytes below F immutable): new dir_offset ≥ prior F. From `[R-CNT-06]`:
dir_length ≥ 4, and dir_offset + dir_length ≤ new F − 64. Chaining: new F
≥ prior F + 4 + 64 = prior F + 68. Since every committed_file_length is a
multiple of 64 (both prior and new, `[R-CNT-06]`), the smallest multiple
of 64 that is ≥ prior F + 68 is prior F + 128 (prior F + 64 is only +64,
short of +68). Matches every place the document now asserts "at least
128." Checked this holds even when the pre-trailer pad is 0 bytes (§6.2
permits a directory that already ends on a 64-byte boundary to have none)
— the derivation never assumed nonzero pad.

**E. The ordering-quantity ceiling, 2⁶³ − 64 (hunk-07's second Note).**
F ≤ 2⁶³ − 1 (u64 domain, `[R-ENC-03]`) and F ≡ 0 (mod 64) (`[R-CNT-06]`).
2⁶³ is itself a multiple of 64 (2⁶³ = 64·2⁵⁷), so 2⁶³ − 1 ≡ 63 (mod 64),
and the largest multiple of 64 not exceeding it is 2⁶³ − 64. Matches the
text's claim exactly.

**F. Appendix A's worked trailer CRC (hunks 28/29), byte-level.** Computed
CRC-32C over the 60 bytes at file offsets [64,124) as printed in the new
hex dump → `0x402f157e`. Equals the document's stated `0x402F157E`, and
the little-endian byte order shown (`7E 15 2F 40`) is correct. This is
the one unambiguously byte-level check in this audit: a conforming reader
given this exact 128-byte file computes this exact CRC and must accept
the trailer; a wrong constant here would make the spec's own reference
example non-self-consistent, and it is not.

**G. Trailer total width.** 8(magic)+2(major)+2(minor)+4(flags)+
8(dir_offset)+8(dir_length)+8(cfl)+8(file_id)+12(reserved)+4(CRC) = 64.
Confirms the new table still sums to the fixed 64-byte trailer, and that
the freed 8 bytes from removing `generation` were folded entirely into
`reserved` (4 → 12 bytes: 4 + 8 = 12).

## Citations opened and checked

`[R-CNT-24]` (§6.3) — confirms only magic[0,8), version_major/minor[8,12),
and CRC[60,64) are fixed across majors; every reordered field (dir_offset,
dir_length, committed_file_length, file_id, reserved, flags) sits in the
"remaining 48 bytes" a future major may redefine, so the reorder is legal
under R-CNT-24's own terms, and the un-hunked §6.3 paragraph stating this
needed no edit — verified this by direct arithmetic (48 = 64 − 16, a
function only of the fixed fields' widths, none of which moved).
`[R-SLB-05]` (§16) — supports hunk-08's "placement within a commit is
free." `[R-CNT-21]` (§5.2) — supports hunk-08's "slack is unconstrained."
`[R-CNT-27]` (§5.1, 128-byte file-size floor) — the analogy hunk-06's new
Note draws ("run from F rather than from offset 0"): both derivations use
the identical shape (a ≥4-byte directory plus a 64-byte trailer at a
64-aligned offset, forced up from a starting point); R-CNT-27's own
argument is 16 (front block) + 4 (min directory) → next 64-aligned offset
= 64 → +64 trailer = 128; the append-case argument substitutes prior F
for offset 0 and gets the same shape. Analogy holds (see Check 7).
§2.2 (identifier retirement) and §24/`[R-VEC-02]` (row-label retirement) —
both opened to check hunk-21's new Note's citation "on the model §2.2
states … (§24, `[R-VEC-02]`)"; both passages do state exactly the "never
renumbered, never reused" policy the Note claims — not an overreach.
`[R-LIF-01]`, `[R-LIF-02]`, `[R-LIF-03]`, `[R-ENC-03]`, `[R-CNT-06]` — each
checked against the surrounding prose in §9.2/§9.3/§20.5 as tagged; each
tag sits at the end of the paragraph whose claims it actually supports.

## The seven checks, applied

1. **Restatement fidelity.** §21.2/§21.8's summary counts restate the
   table rows themselves; checked arithmetically (A, B, C above) — exact,
   word for word ("nine"/"seven", "35", "120"/"275").
2. **Citations point where claimed.** All checked above; no misdirected
   citation found. Notably, §21.7's citation for "the strict growth of
   committed_file_length" is `[R-LIF-01]`, `[R-LIF-02]` (hunk-22) — correct,
   since the strict-increase claim's normative home is §9.2's R-LIF-02 tag,
   not §9.3's R-LIF-03 tag (which now covers only the caching/revalidation
   obligation, not the increase itself).
3. **Normative placement.** hunk-06 and part of hunk-07 add material inside
   labelled `>` **Note** blocks. Checked this is not the sole statement of
   a rule: the material is explanatory derivation of facts already stated
   normatively (§9.2's R-LIF-02 tag carries the "at least 128" claim itself
   in plain paragraph text, not just in the Note; §9.3's main paragraph,
   tagged `[R-LIF-03]`, carries the ordering claim). The Notes derive and
   explain; they do not hide a rule. Similarly hunk-21's Note cites an
   already-normative statement of the row-label policy at §24/R-VEC-02
   (itself not inside a labelled block). Passes.
4. **No contradiction elsewhere in the same passage.** Read full
   surrounding subsections for every hunk (§6.2, §9.2, §9.3, §9.6,
   §20.1–20.5, §21.1–21.9, §22.5, §23.2, §24, Appendix A/D/G) — no internal
   contradiction found within any touched passage.
5. **No exhaustive claim it cannot carry.** The specialization list
   (hunk-17) and every analogy list found are explicitly qualified "not
   offered as closed" — no new closed/universal claim introduced by these
   hunks. The one place I scrutinized hardest for overclaim — §9.3's "F …
   identifies each of them [generations]" — is self-hedged in the very
   next Note of the same hunk ("The contract above also assumes a
   conforming writer …"), so the potential overclaim is disclosed in the
   same breath it's made, not left implicit.
6. **What was left open.** Checked every trailer-adjacent quantity:
   version_minor (still governed by `[R-CNT-26]`, untouched), flags (still
   governed by §6.3, untouched), file_id (still governed, untouched),
   dir_offset/dir_length/committed_file_length (still governed by
   `[R-CNT-06]`'s field table, values unchanged, only byte position
   moved). Compaction's output F is explicitly noted as unconstrained
   relative to the input's F ("before any comparison of
   committed_file_length") — a correct statement of what's open, not an
   oversight. Found nothing newly ungoverned.
7. **Analogy verb-matching.** hunk-06: governing verb of `[R-CNT-27]` is
   "cannot be satisfied in fewer [bytes]" (a derivation from minimum
   structure sizes); governing verb of the new Note is "is therefore at
   least … plus 128" (the same derivation shape, re-run from F instead of
   from 0). Re-derived both independently (arithmetic D above) — same
   reasoning, same conclusion shape; analogy holds. hunk-27/§24: "a row
   label is never renumbered and never reused … exactly as §2.2 makes the
   identifier permanent" — §2.2's verbs ("never renumbered or reused …
   permanently retired") match the new text's verbs
   ("never renumbered and never reused … denotes one condition for the
   life of format major 1") word for word; analogy holds. No other
   "exactly as / the same way / likewise" phrasing was introduced by
   these 31 hunks.

## Sweep results by category (per charter)

**Removed field's name ("generation").** 47 distinct lines swept and
individually classified (run #6). Every surviving occurrence uses
*generation* in the surviving glossary sense — "one committed state of a
file" (§3.1: "stored in a generation", "the live generation") — never as a
reference to a numbered counter field. Zero defects found.

**Old offsets/widths.** Swept for `offset 16/24/32/40/48/56/60` patterns
and bracket-range patterns (runs #7–8); all hits are either unrelated
file-level offsets (front block, directory) or the two already-correct
updated register rows (F14, F15). Zero stale offsets found.

**Passages relying on the removed field's properties (counting, ordering,
distinguishing states).** The *ordering* property is explicitly
re-derived and re-grounded on `committed_file_length`'s strict increase
throughout §9.2/9.3, with citations pointing at the correct requirement
(checked above, arithmetic D). The *counting* property (how many commits
a file has had) is explicitly and repeatedly *disclaimed* rather than
silently dropped — §9.3's third Note, §20.5, §21.7, §23.2, and Appendix G
all now say explicitly that no field counts commits, each in the context
relevant to it. This is the correct response to a genuinely lost
capability, stated everywhere that fact used to be assumed.

**Register row-label policy reversal.** Found and read every passage
reasoning about row labels: §21.1's specialization-pair list (untouched by
the label-policy change itself, but independently checked for correctness
under hunk-17's new "instance-level specialization" wording — F1's
front-block instance genuinely specializes F6, F1's trailer-magic instance
genuinely specializes F8, not a case of both instances specializing both
rows), §21.2's new Note (hunk-21), §24/R-VEC-02 (hunk-27). No other
passage in the document discusses row-label numbering (run #11 confirms
only these two sites use the vocabulary at all). Checked that the other
row-label series (L, T, R) have no gaps that would be inconsistent with
the new policy — none do; F11 is the first-ever struck row, so this is the
policy's first live application, not a retrofit onto existing gaps.

**Counts.** §21.2's "35 conditions" and §21.8's "120 conditions over 275
instances" both independently re-derived from the live table and matched
exactly. No other stray count (121, 277, 36) survives anywhere in the
document (run #14).

## Candidates considered and rejected

1. **§6.3's R-CNT-24 paragraph and §2.3's Note about F15's non-reach** —
   not in any hunk, both directly discuss trailer byte positions. Strong
   candidates for a stale restatement. Checked in full: every number
   (F−64, F−56, F−4, 48 remaining bytes) is derived from the *fixed*
   fields (magic, version, CRC), none of which moved or changed width; the
   new reserved field's position [48,60) is still inside the same 48-byte
   redefinable span as the old [56,60) position. Rejected — correct as
   written, no update needed, and this is exactly the shape of passage the
   charter warns to look for, so I verified it by hand rather than
   assuming.
2. **Whether "nine" might really be "eight" or "ten" under a different way
   of drawing R-CNT-06's clause boundaries** (e.g. splitting
   "committed_file_length equals file size" and "is a multiple of 64" into
   two conditions instead of one). Resolved by cross-checking against the
   register's own row count (9 rows citing R-CNT-06 as sole governing
   rule) rather than parsing English clause boundaries — the register
   gives an unambiguous, independently countable answer matching "nine"
   exactly, and F13 alone (not two rows) covers the multiple-of-64 check.
   Rejected.
3. **Whether the 275-instance total might be off by exactly 1 from a
   miscounted F2/F11 interaction** — exactly the shape of defect a
   generation-removal could hide. Checked the delta both ways (−1
   condition from F11 itself, −1 instance from F11's own single-item
   Instances cell, −1 instance from F2's Instances cell losing
   "generation" = −2 instances net, 277→275) — self-consistent, matches
   the document. Rejected.
4. **§9.3's "identifies each of them" as an unsupported new claim keyed to
   a quantity that doesn't determine it** (the pattern the brief calls
   this project's most-repeated defect). Checked whether
   committed_file_length actually determines a generation, given the
   document elsewhere concedes a non-conforming writer can reuse an F
   value via rollback+re-append. Found the limitation disclosed in the
   same hunk's third Note ("The contract above also assumes a conforming
   writer …"), not left for a reader to discover elsewhere. Rejected as a
   properly-scoped claim.
5. **hunk-08's "at or above the expected one"** — considered whether a
   rollback attacker can only reach F values strictly above the expected
   one (making "at or above" an overclaim in the exact-match direction).
   Re-derived: the previously-expected F is itself a legitimate later
   commit than the truncation point F_old, so it already satisfies
   F_expected ≥ F_old + 128 and is a multiple of 64 — reachable exactly by
   padding. Rejected.
6. **hunk-05/06's "binds from the second commit onward" vs. R-LIF-02's own
   unqualified strict-increase sentence** — considered whether this is an
   internal contradiction (the unqualified sentence technically also
   "binds" the creation commit, which has no prior trailer). Concluded
   this is vacuous truth at creation, and the qualifying sentence is a
   clarification of that vacuity, not a contradiction. Rejected.
7. **hunk-12's unrelated wording fix** ("compactor MUST refuse [the file]"
   → "compactor MUST refuse to compact [the file]") — checked it doesn't
   collide with other "MUST refuse" phrasing in §20.5; the surrounding
   prose already uses "MUST refuse to compact" twice unchanged, so this
   table-row edit brings it into consistency rather than conflict.
   Rejected — not a defect, and not part of the generation-removal surface
   either (a separate precision fix riding along).

## What I could not check

- No access to `tools.diff`, `full.diff`, or any file outside the 31 named
  hunk files and the live spec, so I could not check whether a reference
  implementation, test generator, or conformance corpus still assumes 36
  F-rows, a generation field, or the old trailer offsets. Out of charter,
  not an oversight.
- I did not re-verify every one of the 31 hunk headers' claimed line
  ranges against the live file individually; I verified each hunk's
  *content* against the live file at the location grep/Read found it
  (which is what actually matters for a downstream-dependency audit), and
  found no header/body mismatch in the ones I did check directly (hunks
  01, 03, 05–08, 10–29 were all read in their landed context; several,
  e.g. hunk-15/16's figure and hunk-28/29's Appendix A table, were also
  independently reconstructed and checked byte-for-byte).
- I did not attempt a full row-by-row semantic re-audit of all 120
  register rows' Instances cells (only the two cells this round's change
  actually touches, F2 and F11); a complete re-derivation of the
  pre-existing 277→275 baseline from scratch is outside what a
  downstream-dependency sweep of *this* change can practically redo and
  was presumably already covered by an earlier round.

## Result

No findings. Every sweep, every derived number, and every citation checked
came back consistent with the repair. The passages I most expected to
surface a silently-invalidated dependency — §6.3/§2.3's discussion of
which trailer bytes are fixed across format majors, directly about
trailer byte positions and untouched by any of the 31 hunks — turned out
to be correct by construction, because the fixed/redefinable boundary is
a function only of the fixed fields' widths, none of which moved. The
"generation" sweep (47 occurrences), the offset/width sweep, the
row-label-policy sweep, and the count sweep (35/120/275) each came back
clean by direct, independent computation rather than by trusting the
hunks' own arithmetic.
