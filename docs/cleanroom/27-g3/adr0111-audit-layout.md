# Layout audit transcript — case-adr0111

## Disclosure

Context I did not ask for appeared before I began: a CLAUDE.md pointer to
AGENTS.md, a user memory index (topics: naming constraints on published
rationale, TARN working cadence, decision style, workflow-verifier failure
shapes, spec-edit propagation checks, TARN register/corpus build list), a
userEmail block, and a currentDate block. None of it is part of the
specification and none of it is evidence about the change under audit. I did
not open AGENTS.md, MEMORY.md's linked files, or any docs/ ADR, and did not
treat any of that material as instruction or evidence. I disregarded it.

Files read (only these, per charter):
- /private/tmp/.../scratchpad/case-adr0111/hunk-01.diff
- /private/tmp/.../scratchpad/case-adr0111/hunk-02.diff
- /private/tmp/.../scratchpad/case-adr0111/hunk-03.diff
- /private/tmp/.../scratchpad/case-adr0111/hunk-04.diff
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md
  (multiple ranges: 151-280, 341-405, 800-874, 1222-1345, 3565-3612, 4230-4300,
  plus targeted greps over the whole file for specific terms)

Commands run: `wc -l` on tarn.md; `grep -n` for "generation", "trailer
offset|offset NN", "reserved", "R-ENC-04\]", "R-CNT-06", "^| F[0-9]* |",
"R-CNT-06\][^,]*states|nine\b|ten\b". No writes except this transcript. No
git commands, no other files, no directory listing of case-adr0111/.

I did not read full.diff, did not read hunk files outside my charter, and did
not list the case-adr0111 directory.

## Hunk headers vs bodies

All four headers were checked against their bodies and against the current
file. All four are accurate:

- hunk-01: claims lines 249-251. Current file lines 249/251 are exactly the
  two changed lines ("states nine" / "the other seven"); 250 is the unchanged
  context between them. Matches.
- hunk-02: claims lines 395-398. Current file 395-398 is exactly the new
  **generation** bullet. Matches.
- hunk-03: claims lines 811-815. Current file 811-815 is exactly the five
  `+` table rows (dir_offset..reserved). Matches.
- hunk-04: claims lines 837-843. Current file 837-843 is exactly the
  post-change validation sentence, rewrapped. Matches. Diff body itself is a
  clean removal of "1 ≤ generation ≤ 2⁶³ − 1; " with no other content change.

No header/body disagreement found in any of the four hunks.

## The rule each hunk adopts (own words)

- hunk-01: Re-derives how many conditions `[R-CNT-06]` states now that one
  (the generation range check) is gone, and how many of those remaining
  conditions are fixed-across-majors invariants under `[R-CNT-24]`.
- hunk-02: Redefines **generation** to no longer be "counted" by any field;
  ordering across a file's generations is now carried by
  committed_file_length's strict increase (delegates to §9.3).
- hunk-03: Trailer table with generation's row deleted and the four
  structural fields after it shifted back 8 bytes each; reserved widened from
  4 to 12 bytes and moved from offset 56 to offset 48.
- hunk-04: The prose validation-gate list with the generation range clause
  removed and the sentence rewrapped; no other clause touched.

## Check 1 — count arithmetic (primary target)

Derived the count two independent ways.

**A. From §6.2's own text (current file, lines 833-843).** The paragraph
first validates, in order, three fixed-position items (magic, CRC, "the
version gate (§6.3)"), then a conjunctive "MUST validate all of the
following": flag gates (§6.3); committed_file_length == F; committed_file_length
% 64 == 0; dir_offset ≥ 16; dir_length ≥ 4; dir_offset+dir_length ≤ F−64;
file_id ≠ 0; reserved bytes zero — all cited at the end to `[R-CNT-06]`.

**B. From §21's register (independent, not part of my hunks, but read for
cross-check since it is inside spec/tarn.md).** Rows whose Governing rule
cell names `[R-CNT-06]` as the *primary* (first) citation:
F8 (magic), F9 (dir_offset<16), F10 (dir_offset+dir_length>F−64), F12
(file_id=0), F13 (committed_file_length not %64), F14 (trailer CRC), F15
(reserved≠0), F16 (dir_length<4), F17 (committed_file_length≠file size).
That is exactly **9** rows. Crucially, F18 (version_major=0) is governed by
`[R-CNT-07]`, and F19 (incompat flag bit) by `[R-CNT-08]` — confirming that
"the version gate" and "the flag gates" mentioned in §6.2's ordering sentence
are cross-references to other requirements' conditions, not conditions
`[R-CNT-06]` itself states. This resolves the apparent ambiguity in reading A
(whether "committed_file_length == F ... and is a multiple of 64" is one
clause or two): the register treats them as two distinct conditions (F13,
F17), and flag/version gates as zero — both readings converge on 9.

A gap at F11 (`> **Note.** Row label F11 is struck...`, line 3608) is
consistent with F11 having been the generation-range condition, permanently
retired rather than renumbered — matching the brief's description of the
"second, separable change." (I did not audit that note's correctness, since
§21 is outside my four hunks; I note it only as corroborating context.)

So: **pre-change total = 10 (9 + the struck F11), post-change total = 9.
Matches "ten"→"nine" exactly.**

Fixed-vs-not: `[R-CNT-24]` (line 861-868) fixes only trailer magic, F−64;
version_major/version_minor, F−56; and the CRC at F−4 — plus the front
signature block. Among `[R-CNT-06]`'s own 9 (or pre-change 10) conditions,
only magic and CRC fall inside that fixed set — version_major's own gate is
owned by `[R-CNT-07]`, not `[R-CNT-06]`. So fixed = 2 in both versions;
non-fixed = 10−2=8 before, 9−2=7 after. **Matches "eight"→"seven" exactly.**

Conclusion: the count change in hunk-01 is arithmetically and citation-wise
correct, verified two independent ways.

## Check on layout (primary target)

New table (lines 807-816), offsets and widths, cumulative:
0+8=8, 8+2=10, 10+2=12, 12+4=16, 16+8=24, 24+8=32, 32+8=40, 40+8=48,
48+12=60, 60+4=64. Contiguous, no gap or overlap, sums to exactly 64.
Matches "trailer is still 64 bytes" and "CRC still at offset 60 over
[0,60)" from the brief and from the table's own last row.

Checked every other statement in my four hunks against these positions:
- hunk-04's prose (`dir_offset ≥ 16`, `dir_length ≥ 4`,
  `dir_offset + dir_length ≤ F − 64`, `file_id ≠ 0`, `reserved bytes zero`)
  states only value constraints, not byte offsets, so it cannot go stale
  under a reorder — consistent.
- Register rows F14 ("trailer offset 60") and F15 ("12 reserved bytes at
  trailer offset 48") already reflect the new positions (outside my hunks,
  but read to check for staleness per the brief's instruction to look at
  "text no hunk touched"). Consistent, not stale.
- Appendix A's byte-level example dump (lines 4255-4281) already reflects
  the new layout: dir_offset at file bytes [80,88) = trailer offset 16;
  dir_length [88,96) = offset 24; committed_file_length [96,104) = offset
  32; file_id [104,112) = offset 40; 12 reserved bytes [112,124) = offset
  48-60; CRC [124,128) = offset 60. All consistent, not stale. (Outside my
  hunks; checked only for the "left the reorder open" question.)
- §9.2's note (lines 1263-1273, unchanged, outside my hunks) still cites
  `[R-CNT-06]` for "dir_length ≥ 4 and dir_offset + dir_length ≤ ... F − 64"
  — value constraints again, unaffected by offset reshuffling.

No stale offset or width found anywhere I could check inside or adjacent to
my four hunks.

## Check on hunk-02 (the term) — restatement fidelity

New text: "No field numbers generations; successive generations of one file
are ordered by the strictly increasing committed file length their trailers
carry (§9.3)."

Opened §9.3 (lines 1304-1345). Found: "Within one file_id, F strictly
increases per commit — by at least 128 (`[R-LIF-02]`) — so it orders that
file's generations and identifies each of them" (line 1311-1313), and the
third Note: "F counts bytes, not commits. It orders a file's generations and
tells a cache which one it holds, but it does not number them... no field
records it" (lines 1337-1341).

Word-for-word: "strictly increases" ↔ "strictly increasing"; "orders that
file's generations" ↔ "generations ... are ordered"; "does not number them
... no field records it" ↔ "No field numbers generations." Tense and
quantifier match. §9.3's scope is "within one file_id" — §3.1 defines
**file** as "a single TARN artifact" (one byte sequence), and file_id is
"chosen at creation" and persists for that artifact's whole lifetime
(compaction produces a *different* file under a new file_id, §9.3's third
Note and §20.5) — so "one file" and "one file_id" pick out the same scope
here. No scope mismatch.

Also spot-checked line 3326-3328 (§19, unchanged, outside my hunks): "the
live state names one generation, and two trailers of one file_id are ordered
by committed_file_length without being counted" — already phrased
identically to the new §3.1 term, corroborating that this is a
document-wide, consistently-executed change rather than an isolated edit.

## Check 2 — citations

- `[R-CNT-06]` (hunk-01, hunk-04): resolves to §6.2's trailer-validation
  paragraph. Correct.
- `[R-CNT-24]` (hunk-01, hunk-04): resolves to §6.3's fixed-across-majors
  paragraph (lines 861-868), which does list magic/version/CRC/front-block as
  fixed. Correct, and its content matches how hunk-01 uses it.
- §9.3 (hunk-02): resolves to "9.3 Generations, file_id, caching" and
  contains exactly the ordering claim quoted. Correct.
- §9 (hunk-02, "one committed state of a file (§9)"): resolves to "9.
  Lifecycle and Consistency," the section whose §9.1 opens "A TARN file
  changes only by commit... every conforming mutation... is either a commit
  or a whole-file rewrite." Consistent with "one committed state."
- `[R-ENC-04]` (hunk-04, unchanged content, only rewrapped): resolves to
  line 471, "A reader MUST NOT allocate, seek, or [use an overflowing sum]"
  — the general u64-sum-overflow rule. Matches "that sum being a
  declaration-derived quantity under [R-ENC-04]."

All citations in my four hunks resolve to text that says what the changed
text claims.

## Check 3 — normative placement

Both changed passages (§2.3's paragraph, §3.1's term, §6.2's table and
validation paragraph) are plain declarative prose, not inside a `>` block
labelled Note/Example/Rationale. `grep` for "generation" across the whole
document turned up no case where the *new* definition or the *removed*
field's rule now lives only inside a labelled blockquote. Passes.

## Check 4 — contradiction within the passage (including untouched text)

Read all of §2.3 (151-283), all of §3.1 (341-401), and all of §6.2
(800-848) — not just the hunked lines. No internal contradiction found: the
Note at 271-282 (illustrating F14/F5/F15) needed no update (it never
mentioned generation or the old offsets) and remains accurate against the
new layout; §6.2's own two Notes (829-831, 845-848) are untouched and
unaffected.

## Check 5 — exhaustive claims

"MUST validate all of the following... Any failure is reject-file" (§6.2)
is a closed list; rebuilt it field-by-field against the trailer table (9
fields, magic/CRC validated first, 7 more validated together) — every
trailer field is covered by some clause; nothing was dropped besides the
one field that no longer exists. Built the smallest legal member (a
128-byte empty-directory file, per Appendix A) mentally against this list:
all 9 checks apply to it and none reference a now-absent field. No
overclaim found.

## Check 6 — what the change leaves open

The structure at issue is the 64-byte trailer plus the ordering discipline
across a file's generations. Enumerated quantities: trailer field values
(all 9 still individually validated, table sums to 64 exactly — checked
above); ordering of one file_id's generations (now carried solely by
committed_file_length, per §9.3, unchanged in this respect from before this
edit — the old generation field was a bare range-bounded counter with no
normative monotonicity check of its own either, so no reader-side
verification capability was lost); numbering/counting of generations
(explicitly and correctly disclaimed as ungoverned by any field, both by
the new §3.1 term and by §9.3's pre-existing third Note). I did not find a
quantity the old generation field pinned down that the new text leaves
unpinned.

## Check 7 — argument by analogy

Searched all four hunks for "exactly as", "the same way", "as X is", "for
the same reason", "likewise", "on the same discipline". None of the four
hunks contains any such phrase — no analogy argument was introduced or
altered by this change. Nothing to test under this check.

## Findings considered and rejected

- *Possible off-by-one in the "nine"/"seven" count if "committed_file_length
  equals F" and "is a multiple of 64" are one semicolon-clause rather than
  two.* Rejected: the register (F13 vs F17) settles this by treating them as
  two distinct conditions, which is the same individuation §2.3's own
  definition of "condition" invokes ("as §21.1 individuates them"). Two
  independent countings (prose-clause count with flag/version gates
  excluded per F18/F19's governing-rule citations; and direct register
  tally) both land on 9. Not a defect.
- *Possible stale offset in prose elsewhere in §6.2.* Rejected after
  checking every offset-bearing sentence in §6.2, §9.2's note, the register
  rows F14/F15, and Appendix A's worked example — all consistent with the
  new table.
- *Possible loss of a monotonicity check the old generation field
  supplied.* Rejected: the old field's own stated rule was only a static
  range bound (`1 ≤ generation ≤ 2⁶³ − 1`), never a monotonicity check
  itself; monotonicity was always a writer-side obligation under
  `[R-LIF-02]`/`[R-LIF-03]`, unaffected by this change.
- *Possible file/file_id scope mismatch in hunk-02's new term.* Rejected:
  §3.1 defines "file" as a single artifact, and file_id is fixed for that
  artifact's lifetime (compaction makes a new file under a new file_id), so
  "one file" and "one file_id" coincide for this purpose.

## Result

No findings survive. The count change, the layout change, the term
restatement, and every citation in the four hunks check out against the
current document, including text the hunks did not touch.
