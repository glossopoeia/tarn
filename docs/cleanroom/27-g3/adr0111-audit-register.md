# Register audit transcript — case-adr0111

## Disclosure

Before starting work, my context window already contained material I did not
request: a project CLAUDE.md pointer, an index of the user's personal memory
files (topics like "TARN working cadence", "Rob's decision style", "Spec edits
need propagation checks", "TARN register is the corpus build list"), the
user's email address, today's date, an "Auto Mode Active" operating note, and
an environment block naming the repository/branch/git status. None of this is
part of the specification and none of it is evidence about the change under
audit. I have disregarded all of it and am not treating any of it as a fact
about the document, per the brief's instruction. I have not repeated its
contents beyond the topic labels needed to name what appeared.

## What I read

- All 8 assigned hunk files verbatim:
  hunk-16.diff, hunk-17.diff, hunk-18.diff, hunk-19.diff, hunk-20.diff,
  hunk-21.diff, hunk-22.diff, hunk-25.diff
  (path: .../scratchpad/case-adr0111/<name>.diff)
- spec/tarn.md, the following regions (via Read, by line offset):
  - 94–163 (§2.1–2.3, incl. the F15/R-CNT-24 "does not reach" Note)
  - 238–294 (§2.3 reach test, §2.4 opening)
  - 340–402 (§3.1 terminology incl. "generation" definition)
  - 756–943 (§6.1–6.4, §7.1 opening) — trailer layout table, remote-open
    accounting
  - 850–935 (§6.3–6.4 in full)
  - 1200–1345 (§8.2, §9.1–9.3 incl. R-LIF-01/02/03 and their Notes)
  - 1330–1345 (§9.3 Note: "F counts bytes, not commits")
  - 1433–1477 (§9.7 Coverage verification, incl. its Note)
  - 3334–3433 (§20.5 Compaction, in full — R-WRT-06 obligations)
  - 3476–3615 (§21.1, §21.2 in full, incl. the F11-struck Note)
  - 3614–3743 (§21.3 Layer-scope, §21.4 Tile-scope, §21.5 Ignored records —
    full tables, to validate §21.8's cross-table totals)
  - 3796–3877 (§21.7 What no check detects, §21.8 Conformance vector
    coverage, §21.9 heading)
  - 4160–4199 (§24 opening through the row-label-permanence paragraph)
  - 4255–4294 (§24 worked byte-level example + table, to check for stale
    trailer offsets)
  - 4494–4510 (appendix: "One generation" / no-commit-count item)
- Targeted greps of spec/tarn.md for: `generation`, `renumber|positional|
  struck|retired|F11`, `R-VEC-01|R-VEC-02`, `R-LIF-01|R-LIF-03|R-LIF-04`,
  `R-ENC-03`, `R-CNT-24`, `R-WRT-06|R-WRT-01`, `offset 56|56 that|reserved
  bytes at|trailer reserved|56,60|48,60`, `dir_offset|dir_length|
  committed_file_length|file_id` combined with offset-looking patterns,
  `commit count|number of commits|commit number|how many commit`.

I did not read full.diff, any hunk file outside my charter, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, or git history, and did not list the
case-adr0111 directory.

## Header-vs-body check

All 8 hunk headers name a location; I checked the current file at that
location against the hunk body:

- hunk-16 → line 3562: "Outcome: reject-file. 35 conditions. Which rows..." — matches.
- hunk-17 → line 3573: F2 row — matches.
- hunk-18 → lines 3582–3585: F12/F13/F14/F15 rows — matches (F11 absent, table flows F10→F12 with no broken markdown).
- hunk-19 → lines 3608–3613: the "F11 is struck" Note — matches.
- hunk-20 → lines 3816–3822: the R-LIF-01/R-LIF-03 paragraph in §21.7 — matches.
- hunk-21 → lines 3855–3861: the "three obligations" sentence in §21.7 — matches.
- hunk-22 → line 3871: §21.8's "120 conditions over 275 instances" — matches.
- hunk-25 → lines 4182–4186: §24's row-label-permanence sentence — matches.

No header/body mismatch found in any of the 8.

## Arithmetic — recounting §21.2–§21.5 by hand

Per §21.1: a row is one condition; the Instances column is mechanical —
semicolon-separated items, an em-dash cell counts as 1.

**§21.2 (F), 35 rows (F1–F10, F12–F36; F11 struck):**
F1:2 F2:5 F3:2 F4:1 F5:2 F6:2 F7:4 F8:1 F9:1 F10:1 | subtotal 21
F12:1 F13:1 F14:1 F15:1 F16:1 F17:2 F18:1 F19:1 F20:1 | subtotal 10 (running 31)
F21:1 F22:1 F23:2 F24:1 F25:1 F26:1 F27:1 F28:2 F29:3 F30:2 | subtotal 15 (running 46)
F31:1 F32:1 F33:5 F34:1 F35:1 F36:1 | subtotal 10 (running 56)
**F total = 56 instances, 35 conditions.**

Cross-check: the old text (per hunk bodies) had F2 with 6 instances
(dir_offset; dir_length; committed_file_length; generation; extent_offset;
extent_length) and a live F11 row worth 1 instance (generation). Old F total
= 56 − 5(new F2) + 6(old F2) + 1(F11) = 58, old condition count = 36. This
matches the hunk's own "-36" / "-1" register text (hunk-16: 36→35;
hunk-22: 121→120 overall). Internally consistent.

**§21.3 (L), 49 rows** (counted from the full table, not just the hunks —
needed to validate §21.8's overall total):
L1:8 L2:9 L3:1 L4:2 L5:1 L6:1 L7:2 L8:2 L9:2 L10:1 (29)
L11:1 L12:2 L13:1 L14:3 L15:4 L16:2 L17:2 L18:3 L19:1 L20:1 (20, run 49)
L21:4 L22:4 L23:4 L24:1 L25:1 L26:1 L27:1 L28:1 L29:3 L30:2 (22, run 71)
L31:3 L32:3 L33:4 L34:4 L35:1 L36:2 L37:1 L38:1 L39:3 L40:1 (23, run 94)
L41:3 L42:1 L43:3 L44:3 L45:3 L46:2 L47:2 L48:1 L49:4 (22, run 116)
**L total = 116 instances, 49 conditions.**

**§21.4 (T), 26 rows:**
T1:1 T2:1 T3:6 T4:4 T5:1 T6:1 T7:2 T8:1 T9:1 T10:1 (19)
T11:2 T12:1 T13:2 T14:6 T15:2 T16:1 T17:1 T18:2 T19:1 T20:1 (19, run 38)
T21:3 T22:6 T23:1 T24:1 T25:3 T26:3 (17, run 55)
**T total = 55 instances, 26 conditions.**

**§21.5 (R), 10 rows:**
R1:4 R2:2 R3:2 R4:16 R5:8 R6:4 R7:6 R8:2 R9:2 R10:2 = 48
**R total = 48 instances, 10 conditions.**

**Grand total (new): 35+49+26+10 = 120 conditions; 56+116+55+48 = 275
instances.**

This matches §21.8's new stated total exactly: "120 conditions over 275
instances" (hunk-22). And old total (36+49+26+10=121; 58+116+55+48=277)
matches the hunk's own "-121"/"-277" struck text. **Validated by
reproducing an unchanged table (L, T, R) alongside the changed one (F) —
the arithmetic is internally exact in both directions.**

## Citations opened and checked

- `[R-CNT-24]` (§6.3, lines 861–868): fixes trailer magic (F−64), version
  fields (F−56), and the CRC (F−4) across every major; "a future major MAY
  redefine only the remaining 48 trailer bytes." F15's reserved field sits
  inside that 48-byte redefinable region regardless of whether it is 4
  bytes at offset 56 (old) or 12 bytes at offset 48 (new) — so the §2.3
  Note ("F15 does not reach... inside the 48 that rule lets a future major
  redefine", lines 280–282) is untouched by the reorder and remains
  correct. Confirmed by direct reading, not by inference alone.
- `[R-LIF-01]` (§9.1, line 1231) — committed-prefix immutability. Correctly
  paired with the §21.7 claim.
- `[R-LIF-03]` (§9.3, lines 1311–1320) — "Within one file_id, F strictly
  increases per commit... so it orders that file's generations and
  identifies each of them." Word-for-word matches the new §21.7 text's
  "the strict growth of `committed_file_length` across the commits of one
  file_id." Tense, quantifier ("strictly"/"strict"), and scope ("within
  one file_id"/"across the commits of one file_id") all agree.
- §9.3's own Note (lines 1337–1341): "F counts bytes, not commits... how
  many commits a file has undergone is not recoverable from the live
  trailer, and no field records it" — directly supports the new §21.7
  clause "no field of a file records how many commits that history holds."
  Same claim also appears, independently phrased, at §20.5 (lines
  3361–3364: "no field counts commits") and in the appendix (line
  4502–4503: "No field records how many commits a file has had"). Three
  independent restatements, all consistent, none contradicting the
  changed text.
- §9.7 (lines 1433–1477, esp. the closing Note "Nothing here enumerates
  prior commits") — supports "which §9.7 does not reconstruct" for both
  the R-LIF-01/03 clause and the later "prior generation" clause in
  hunk-21's paragraph.
- §20.5 (lines 3334–3433) — read in full to verify hunk-21's "three
  obligations on a compacted file's trailer" under `[R-WRT-06]`: (1) MUST
  mint a fresh file_id, (2) MUST copy forward unknown ignore-lane bits,
  (3) version_minor SHOULD take R-CNT-26's floor / the input's minor.
  These three, and only these three, are obligations *on the trailer*;
  the paragraph's other R-WRT-06 obligation (refuse to compact a file
  carrying an unimplemented MU=1 record) is not a trailer-field
  obligation and is correctly excluded from the count. "The last two"
  (referenced later in the same passage) are the ignore-lane bits and the
  version_minor floor in both the old (4-item) and new (3-item) list —
  removing "its generation" from the middle of the old list does not
  change which items are "the last two," so that internal cross-reference
  still resolves correctly.
- §2.2 (lines 116–122) — "Identifiers are stable: they are never
  renumbered or reused, a withdrawn requirement leaves its identifier
  permanently retired." This is the model hunk-19's Note and hunk-25's
  §24 paragraph both invoke by name for register row labels. The verbs
  ("never renumbered," "never reused") are lifted directly from §2.2's own
  wording — a same-terms analogy, not a paraphrase drift. §24's paragraph
  (which the Note cites as `[R-VEC-02]`) is itself in normative flowing
  text (not a blockquote), ending in a bracketed requirement tag, so the
  policy is actually established there; the §21.2 Note is a labelled,
  non-normative aside that only reports the fact and points to where the
  binding text lives — consistent with how this document elsewhere
  handles retired identifiers (e.g., the R-SER-04 retirement Note at
  lines 2053–2055, same pattern).
- `[R-VEC-02]` — confirmed its only defining occurrence is the §24
  paragraph itself (line 4198); the §21.2 Note's citation (`§24,
  [R-VEC-02]`) and hunk-25's own use of the tag point at the same place.
  No dangling or misresolved citation.
- `[R-ENC-03]` (line 455, general u64 domain rule) — F2's governing rule;
  unaffected by generation's removal since the removed field no longer
  exists to bound.

## Sweep for stale material

- `grep -n "generation"` across the whole file: every remaining hit uses
  *generation* as the §3.1 terminology concept ("one committed state of a
  file... successive generations... ordered by the strictly increasing
  committed file length their trailers carry," lines 395–398) or in
  ordinary prose about "the live/prior generation." None refers to the
  removed trailer *field*. The §3.1 definition itself already states "No
  field numbers generations" — consistent with, not contradicted by, the
  hunks under audit.
- `grep` for `renumber|positional|struck|retired|F11`: only §2.2's
  identifier-stability text, the two unrelated `[R-GEO-06]`/§20.3
  ordinal-renumbering passages (about tile ordinals, a different kind of
  renumbering, unaffected), the R-SER-04 retirement Note, hunk-19's Note,
  and hunk-25's paragraph. Nothing else asserts register-row labels are
  positional or renumber; F11 is not reused anywhere.
- `grep` for old trailer offsets/widths (`offset 56`, `[56,60)`, `4
  reserved`, etc.): only F15's own current text (`[48,60)`, 12 bytes) and
  the §24 worked example's `[112, 124) | zero | trailer reserved, 12
  bytes, zero` — which is offset 48 relative to the trailer start (112 −
  64 = 48) and matches the new layout exactly, including the raw hex dump
  at that file (12 zero bytes at 0x70–0x7B, CRC at 0x7C–0x7F). No stale
  offset anywhere.
- Trailer field table (§6.2, lines 805–816): dir_offset=16, dir_length=24,
  committed_file_length=32, file_id=40, reserved=48 (12 bytes), CRC=60.
  Matches every downstream reference I checked (F-table cells, §24
  example, R-CNT-24's "48 redefinable bytes" arithmetic: 64 − 16 = 48,
  where the 16 fixed bytes are magic(8) + version fields(4) + CRC(4)).
- No struct/layout listing elsewhere in the document restates trailer
  field order, so there is nothing else to sweep for this reorder.

## Findings considered and rejected

1. *Possible stale "R-CNT-06 states nine [conditions]" (line 249)* —
   considered whether removing generation's old F11 check should have
   changed this count. On inspection this sentence is not in my hunk set
   and, more importantly, is already consistent with the current (5
   trailer-validation clauses after the always-fixed 3, one of which
   bundles two F-rows) §6.2 text with no mention of generation — so either
   it was already correct or was corrected in a hunk outside my charter;
   either way it is not contradicted by anything in my 8 hunks. Not
   reported, since it is outside the audited change and shows no
   inconsistency with it.
2. *Whether "fresh file_id draw" truly belongs to `[R-WRT-06]`* — the
   first §20.5 paragraph asserting the fresh-file_id MUST does not carry
   its own terminal bracket tag; I initially suspected this might mean
   hunk-21 miscounts by attributing it to R-WRT-06. Tracing forward, the
   next `[R-WRT-06]` tag (line 3394) closes an unbroken block of
   obligations starting from "A compactor MUST refuse to compact when..."
   through "cannot be safely relocated," with no other requirement tag
   in between — the document's established pattern of one long paragraph
   run closed by a single tag. Corroborated independently at lines
   4530–4531 ("A compactor's output is therefore reproducible only modulo
   its trailer: `[R-WRT-06]`'s fresh file_id..."). So the attribution is
   correct; not reported.
3. *Whether "no field of a file records how many commits" is an
   unsupported new universal (check 5)* — traced to three independent,
   pre-existing normative/rationale passages stating the identical fact
   in different words (§9.3 Note, §20.5, appendix item 4). Not a bare
   assertion introduced only here; not reported.
4. *Whether the F11-note's non-normative framing leaves the row-label
   retirement rule unenforced (check 3)* — the actual binding text is
   §24's flowing paragraph ending `[R-VEC-02]`, not the blockquote Note;
   the Note is correctly only explanatory. Not reported.

## Result

No defects found across the 8 assigned hunks. The trailer reorder is
applied consistently everywhere I could check (table, worked example,
R-CNT-24's redefinable-byte arithmetic); the F11 strike is arithmetically
exact in both the row count and the instance count, cross-validated
against the unchanged L/T/R tables; the row-label permanence policy is
introduced once, in normative text, cited correctly from its one
non-normative echo, and contradicted nowhere; and the §21.7 rewrite's new
claims about `committed_file_length` and about no field counting commits
are each independently corroborated by existing normative or rationale
text elsewhere in the document.
