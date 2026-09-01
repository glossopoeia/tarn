# Downstream auditor transcript — case-adr0111

## Disclosure

Context I did not ask for, present before I began: a CLAUDE.md pointer to
AGENTS.md, a MEMORY.md index (file names only: "tarn-lineage-stays-private",
"tarn-working-cadence", "rob-decision-style", "workflow-verifier-failures",
"spec-edits-need-propagation-checks", "tarn-register-is-the-corpus-buildlist"),
a userEmail block, and a currentDate block. I did not open any of the files
the memory index names, did not act on anything in that context, and treated
none of it as evidence about the specification. Also present: a long tool
catalog (Artifact, Bash, ListAgents, browser tools, skills, etc.) — irrelevant
to this task, unused except Bash/Read which I used for the audit itself.

I read exactly:
- All 29 hunk files, hunk-01.diff through hunk-29.diff, in
  /private/tmp/.../scratchpad/case-adr0111/ (concatenated once into a scratch
  dump file via `cat` for my own reading convenience, then read via the Read
  tool — no other file in that directory was opened, and the directory was
  never listed).
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md,
  in many targeted reads (offsets given below) plus several `grep -n`
  passes over the whole file.

I ran: `wc -l`, `grep -n` (multiple patterns: "generation" case-insensitive,
offset/byte-range patterns, "R-CNT-06", "R-CNT-24", "R-ENC-03", "R-SLB-05",
"R-CNT-21", "renumber|row label|struck|retired", "F11\b", "counter",
"castagnoli"), and a few Python scripts (see arithmetic below) to
mechanically count register rows/instances and to compute CRC-32C by hand
against the worked example in Appendix A. No git command, no web, no file
outside the two permitted locations.

## Header-vs-body check (mechanical claim in every hunk)

Spot-checked several hunks' claimed "lands at lines N–M" against the body:
hunk-03 body shows the trailer table 6.2, hunk-27 shows the Appendix A field
table, hunk-19 shows the §21.2 struck-row note — in each case the change I
found by reading the live file at the stated location matched the hunk's
before/after text. I did not find a header/body mismatch in any of the 29
hunks. (The brief calls out that this class of error has happened before, so
I checked deliberately rather than assuming.)

## Arithmetic performed

**R-CNT-06's "nine" invariants (hunk-01).** Counted the "Governing rule"
column of §21.2 (lines 3572–3606) for rows whose primary citation is
`R-CNT-06`: F8, F9, F10, F12, F13, F14, F15, F16, F17 — nine rows. Of these,
F8 (trailer magic) and F14 (trailer CRC) are the two the document's own
§2.3 text (lines 249–251) says `[R-CNT-24]` fixes across every major; the
remaining seven do not. Matches the hunk's "nine ... the other seven" exactly.

**Row-label struck, not renumbered (hunk-16, 18, 19).** Extracted every
`| F<n> |` row label present in the live file:
F1–F10, F12–F36 = 35 rows (F11 absent). Matches the "35 conditions" the
hunk installs. F11 does not reappear as a reused label anywhere (`grep -n
"F11\b"` returns only the struck-row note itself).

**§21.8's "120 conditions over 275 instances" (hunk-22).** Wrote a small
Python script that walks every table row in §21.2–§21.5 (lines 3560–3741),
extracts the row label (`[FLTR]\d+`) and its Instances cell, and counts
instances per §21.1's stated rule ("a cell reading — is one instance; the
count is therefore mechanical once the cell is written", i.e. semicolon
count + 1, or 1 for an em-dash cell). Result, per section:
- F (§21.2): 35 conditions, 56 instances
- L (§21.3): 49 conditions, 116 instances
- T (§21.4): 26 conditions, 55 instances
- R (§21.5): 10 conditions, 48 instances
Totals: 120 conditions, 275 instances — exactly what hunk-22 installs, and
each section total also matches that section's own self-declared count
(35/49/26/10, at lines 3562, 3617, 3677, 3727). This is a full enumeration,
not a sample.

**Appendix A worked example (hunks 26–27).** Implemented CRC-32C
(Castagnoli, reflected, init/final 0xFFFFFFFF) per §4.5's definition and
verified it against the spec's own check vector: CRC32C("123456789") =
0xE3069283 — matched. Then:
- Reconstructed the OLD 60-byte trailer prefix (with the generation field)
  from the pre-image hex dump and computed its CRC: got 0xE00938D2, which
  is exactly the old table's `D2 38 09 E0` (little-endian) — confirms my
  CRC implementation against a second, independent known-good value from
  the document itself.
- Reconstructed the NEW 60-byte trailer prefix (generation removed,
  fields shifted, reserved widened to 12 bytes) from the hunk's hex dump
  and computed its CRC: got 0x402F157E — exactly the new table's
  `7E 15 2F 40` (little-endian) and exactly the value the changed prose
  row states. The byte-range table in the same hunk ([80,88) dir_offset,
  [88,96) dir_length, [96,104) committed_file_length, [104,112) file_id,
  [112,124) reserved 12 bytes, [124,128) CRC) was checked field-by-field
  against the hex dump and against the §6.2 trailer-offset table (offsets
  relative to trailer start + trailer start at file offset 64) — all
  arithmetic ties out, including the field-width sum (8+2+2+4+8+8+8+8+12+4
  = 64).

## Whole-document sweep for "generation"

`grep -n -i generation` over the whole file returned every occurrence
(listed and individually read in context where not already inside a hunk):
lines 372–396 (term definitions, hunk-covered), 624, 629, 1011, 1026, 1249,
1258, 1260, 1267, 1304–1338 (§9.3, hunk-covered), 1369, 1598, 1603, 1863,
1903, 2298, 3028 (hunk-covered), 3111, 3121, 3126–3168, 3272, 3326
(hunk-covered), 3428, 3449 (hunk-covered/consistent), 3761, 3854
(hunk-covered), 3957, 4067–4069 (hunk-covered), 4117, 4136, 4367–4373
(hunk-covered), 4500 (hunk-covered), 4561. Every occurrence not already
inside a hunk's changed text uses "generation" in the surviving sense —
"one committed state of a file" as a concept — never as a reference to a
numbered/counted field. None of the un-hunked occurrences assign it an
ordering, counting, or bounding role that the removed field used to supply;
each such role (ordering: §9.3; bounding: §9.3's third note; counting: §21.7,
§23.2, §20.5, Appendix G item 4) is now stated explicitly in terms of
`committed_file_length`, in text the hunks themselves supply. I read each of
these in context (not just the grep line) before classifying it; none were
sampled away.

## Whole-document sweep for stale trailer offsets/widths

`grep -n -E "\[(16|24|32|40|48|56|60|64),|offset (16|24|32|40|48|56)\b"`
over the whole file. Every hit checked in context:
- Lines 644–645 (Appendix A smallest-file example): directory/slack/trailer
  file-level offsets, unrelated to trailer-internal field layout — correct,
  untouched, doesn't need to be.
- Line 1194 (§8.1 coverage map): trailer CRC at [60,64) over [0,60) —
  correct both before and after, since magic/version/flags/CRC positions
  are untouched by the reorder.
- Line 1254 (§9.2): "writing beginning at offset 16" is the *file* offset
  right after the 16-byte front signature block, not a trailer-field
  offset — unrelated, correct.
- Lines 1452, 1456 (§9.7 walk bounds [16, F−64)): directory region bounds,
  unrelated to trailer internals — correct.
- Line 2327 (§16.2 slab example ordinal ranges [16,24), [24,32)): tile
  ordinals, unrelated — correct.
- Line 3585 (F15, hunk-covered): "12 reserved bytes at trailer offset 48"
  — matches the new table exactly.
- Lines 4270, 4272, 4284, 4290 (Appendix A): directory-region byte range
  and trailer-magic byte range at the *file* level — unaffected by the
  trailer-internal reorder, correct.
No stale offset or width describing the old trailer layout survives
anywhere outside the hunks.

## Row-label policy sweep

`grep -n -i "renumber|row label|struck|retired"` — every hit read in
context. §2.2 (line 116–122) states the identifier-permanence model the new
row-label note (hunk-19, §21.2) and the new §24 note (hunk-25) both invoke
by analogy. Line 2054's "permanently retired" is about a withdrawn
*requirement identifier* (`[R-SER-04]`), pre-existing and unrelated to this
change. No leftover statement of the old "row labels are positional and
renumber" policy survives anywhere (the only place that used to say it,
§24, is one of the 29 hunks and now says the opposite, consistently with
§21.2's new note).

## Citation and cross-reference checks (the seven-check pass)

Ran the seven checks against each of the 29 hunks. Most pass cleanly;
detail on the ones worth recording:

- **Hunk-01**: restates `[R-CNT-24]`'s reach test; verified against §2.3's
  full paragraph (lines 244–262) and against the register (§21.2) — ties
  out exactly (arithmetic above).
- **Hunk-02, 07**: term definition and §9.3 rewrite are mutually
  consistent word-for-word ("No field numbers generations; ... ordered by
  the strictly increasing committed file length" / "Within one file_id, F
  strictly increases per commit ... so it orders that file's generations
  and identifies each of them").
- **Hunk-05, 06**: the "+128" floor argument was independently re-derived
  by hand (dir_offset ≥ prior F from `[R-LIF-01]` immutability; dir_length
  ≥ 4 and dir_offset+dir_length ≤ new F − 64 from `[R-CNT-06]`; new F ≥
  prior F + 68; both F values multiples of 64 forces the jump to ≥ prior F
  + 128) and matches the added Note exactly. Check 7 (analogy): the Note's
  closing sentence — "It is `[R-CNT-27]`'s 128-byte floor argument run
  from F rather than from offset 0" — was checked against R-CNT-27's own
  text (lines 636–640: front block + dir(≥16,≥4) + 64-byte aligned trailer
  ⇒ 128-byte minimum). Same governing shape (an offset floor, a ≥4 length,
  a 64-byte-aligned trailer, "cannot be satisfied in fewer"), just anchored
  at F instead of 0 — the analogy holds.
- **Hunk-07's** bound note ("F is a u64 offset under `[R-ENC-03]`") is
  imprecise wording — committed_file_length is a *length*, not an offset —
  but F2's own row text already classifies committed_file_length as one of
  the "u64 offset, length, or count" fields R-ENC-03 bounds, so the
  citation itself is correct even though the appositive noun is loose.
  Not filed as a finding: it doesn't misdirect a reader to the wrong rule,
  and doesn't change any byte-level obligation.
- **Hunk-13/14/15 (compaction)**: re-read §20.5 in full (lines 3334–3418)
  and confirmed the reduction from "four obligations" to "three" is
  accurate — the trailer obligations under `[R-WRT-06]` are exactly three
  (fresh file_id draw; ignore-lane bits copied forward; version_minor
  floor). Cross-checked against §21.7's parallel restatement (hunk-21,
  "§20.5's three obligations ... its fresh `file_id` draw, the unknown
  ignore-lane bits it MUST carry forward, and the floor its version_minor
  SHOULD take") — same three, worded consistently.
- **Hunk-20 (§21.7)** — see Finding Y-01 below: a citation that was
  accurate against the old text ("the generation sequence
  (`[R-LIF-01]`, `[R-LIF-03]`)") was carried forward unchanged onto new
  text ("the strict growth of `committed_file_length` ... (`[R-LIF-01]`,
  `[R-LIF-03]`)") whose growth claim is actually stated, as a MUST-adjacent
  derived consequence, in §9.2 under `[R-LIF-02]`, not in §9.3's
  `[R-LIF-03]` paragraph (which only *cites* `[R-LIF-02]` inline for that
  fact before building its own, distinct caching argument on top of it).

## Findings considered and rejected

- *F2's "u64 offset" framing of `committed_file_length`* (above) — rejected,
  imprecise noun choice only, correct rule cited.
- *§21.7's added clause "no field of a file records how many commits that
  history holds"* — checked against §20.5's "no field counts commits",
  §23.2's "no field carries a count", and Appendix G item 4's "No field
  records how many commits a file has had" — all four are the same claim,
  worded consistently, none contradicts another. Not a finding.
- *Appendix G item 2's hash formula* ("the trailer's first 60 bytes with
  the `file_id` field zeroed") — not touched by any hunk, and I checked
  whether it silently depended on the old generation field. It doesn't:
  the formula is stated abstractly (first 60 bytes, file_id zeroed) and
  never hardcodes which fields make up those 60 bytes, so it survives the
  reorder without needing an edit. Considered and rejected as a finding.
- *§6.3's `[R-CNT-24]` paragraph* (trailer magic at F−64, version fields at
  F−56, CRC at F−4 over [F−64,F−4), front block constant, "zero slack ...
  every byte is assigned") — not touched by any hunk. Verified it remains
  true: none of the positions or claims it makes depend on the field order
  inside the 48 bytes between flags and the CRC, which is exactly the
  region the reorder rearranged. Considered and rejected as a finding.
- *§9.6's rollback-forgery paragraph* ("a party that truncates ... can
  bring the file back to any committed file length at or above the
  expected one") — checked this doesn't secretly assume the +128 minimum
  growth rule constrains a forger; it doesn't need to, since a forger
  fabricates bytes directly rather than running the writer protocol.
  Considered and rejected as a finding.
- *Row-label permanence scoped "for the life of format major 1"*
  (§24, hunk-25) — new qualifier not in the old text. Checked whether
  anything else claims register-row permanence across major versions;
  found nothing that contradicts a major-1-scoped register. Considered
  and rejected as a finding.

## Findings reported

One finding, Y-01, filed below — a citation-drift defect (check 2), not
byte-level, moderate-to-high confidence.
