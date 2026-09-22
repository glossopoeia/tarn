# Register hunter — round 37 transcript

## Access and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,981 lines). I did not open `AGENTS.md`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`docs/`, `conformance/`, `spec/registry.json`, or any git history — no
`git log`/`git diff`/`git status` was run against the repository, and I did
not list the repository's directories. I did not read the output directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/out/`
and did not list it.

My scratch directory,
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/register/`,
was empty when I created it (`mkdir -p` reported nothing pre-existing, and
`ls -la` immediately after showed only `.` and `..`) — no prior attempt's
files were present, so there was nothing to disclose on that count. Files I
wrote there: `f_rows.txt`, `l_rows.txt`, `t_rows.txt`, `r_rows.txt` (the raw
`| id | condition | instances | detector | detected | rule |` lines of
§21.2–§21.5, extracted with `sed`/`grep` from the one permitted file);
`count_instances.py` and `instances_out.txt` (my instance-count script and
its output); `check_detector.py` (the detector/detected consistency
checker); this file, `transcript_draft.md`, which I copied to the published
transcript path.

**Context I did not ask for.** Before I began, my runtime context included
a project `CLAUDE.md` pointing at `AGENTS.md` (unread, per the access rule),
a `MEMORY.md` index of file-named notes about this project's TARN harness
history (titles only, e.g. "TARN repair prose vs rules", "TARN no lowercase
keywords", "TARN class lines are undertakings" — I did not open any of the
linked note files), and the git status/log of the repository (branch `main`,
recent commit subjects mentioning "Cleanroom round 37", "ADR-0131", and
"round 36"). None of this is part of the specification and none of it is
evidence about the specification's text. I did not open any memory note
file, and I did not treat the commit subjects (which name "ADR-0131" and a
"two flag bits" / "orthogonal" theme) as telling me where a defect is; where
my own reading independently led me to the same textual neighborhood (§7.2's
Note on the two record-flag bits), I say so below and note that my
conclusion rests on the specification's own text, checked on its own terms,
not on the memory index or commit subjects.

**Paths.** The file was exactly where the brief said:
`spec/tarn.md`, 302,375 bytes, 4,981 lines. No path discrepancy to report.

## Locating §21 and getting an accurate copy of it

`grep -n "^### " tarn.md` and `grep -n "^#### 2[01]\." tarn.md` located
§21 at lines 3733–4239 (next section, §22, at 4241) and confirmed the
subsection boundaries: 21.1 (3735), 21.2 (3834), 21.3 (3888), 21.4 (3945),
21.5 (3982), 21.6 (4016), 21.7 (4078), 21.8 (4135), 21.9 (4142). I read the
whole span with `Read` in one call (offset 3733, limit 508) so I would have
verbatim text rather than working from summaries, and re-read `#### 7.2`,
`#### 20.3`, `#### 20.4`, `#### 20.1`, `#### 18.2`, `#### 6.2`/`#### 6.3`,
`#### 4.2`–`#### 4.6`, `#### 11.3`, `#### 14.2`–`#### 14.5`, `#### 16.1`–
`#### 16.2`, `#### 19.2`, `#### 2.3`–`#### 2.5`, `### 24`, and Appendix H in
full for the rules the register cites, plus every place outside §21 that
cites a register row by label (see the sweep below).

## The counting (charter bullet: "The counting")

### Row counts per subsection

I extracted the table rows mechanically rather than trusting the prose
count, so a miscount in the stated total would show up independent of my
reading:

```
sed -n '3844,3880p' tarn.md | grep -E '^\| [FLTR][0-9]+ \|'   -> 35 lines (F)
sed -n '3893,3944p' tarn.md | grep -E '^\| L[0-9]+ \|'         -> 49 lines (L)
sed -n '3953,3980p' tarn.md | grep -E '^\| T[0-9]+ \|'         -> 26 lines (T)
sed -n '4003,4014p' tarn.md | grep -E '^\| R[0-9]+ \|'         -> 10 lines (R)
```

I then re-ran the same row-label pattern (`^\| [FLTR][0-9]+ \|`) over the
*entire* document (not just my believed line ranges) to make sure no row
existed outside the ranges I had assumed, and to check for duplicate or
reused labels:

```
grep -nE '^\| [FLTR][0-9]+ \|' tarn.md | wc -l   -> 120
```

All 120 matches fall inside the four line ranges above; there are no F/L/T/R
table rows anywhere else in the document. I then parsed the numeric part of
each label and checked the run for gaps and duplicates:

- F: 1–36 present except **11 missing** (35 rows) — matches the register's
  own Note: "Row label F11 is struck, and the gap it leaves in this table is
  deliberate... never renumbered, never reused." I grepped `\bF11\b` over the
  whole document and it occurs exactly once, in that Note — no stray
  reference to a live "F11" anywhere else.
- L: 1–49 present, no gaps, no duplicates (49 rows).
- T: 1–26 present, no gaps, no duplicates (26 rows).
- R: 1–10 present, no gaps, no duplicates (10 rows).

35 + 49 + 26 + 10 = **120**, matching both §21.2's/§21.3's/§21.4's/§21.5's
own per-subsection counts ("35 conditions", "49 conditions", "26
conditions", "10 conditions") and §21.8's aggregate ("120 conditions over
277 instances"). This is a clean mechanical match — I did not need to
resolve any ambiguity to get it.

### Instance counts

§21.1's own arithmetic for the Instances column is stated precisely enough
to mechanize: "Instances within a cell are separated by semicolons, and a
cell reading — is one instance; the count is therefore mechanical once the
cell is written." I wrote `count_instances.py` to parse the Instances column
(3rd pipe-delimited field) of each of the four extracted files, splitting on
`;` and treating a bare `—` as exactly one instance:

```
=== f_rows.txt: 35 rows, 56 instances ===
=== l_rows.txt: 49 rows, 116 instances ===
=== t_rows.txt: 26 rows, 55 instances ===
=== r_rows.txt: 10 rows, 50 instances ===
```

56 + 116 + 55 + 50 = **277**, exactly matching §21.8's "277 instances" and
§24's implicit claim (every instance gets at least one vector). This total
is exact, not approximately close — I checked the arithmetic twice (once by
hand-adding the four subtotals, once letting the same script sum them) and
both give 277.

Because an exact grand-total match does not rule out two compensating
per-row errors, I spot-checked individual rows against §21.1's own
enumeration rules (magnitude-direction doubling for "differs from"/"does not
equal" with no direction bound; no doubling for "exceeds"/"larger than",
which bound one direction; no doubling for a value/nonzero test like
`A ≠ 0`; layout-shape enumeration where the derived quantity's formula
differs by layout; alternative-shape enumeration where the condition text
itself lists distinct malformed classes):

- **L21** (`entry_count` vs geometry-derived count, "does not equal"):
  2 layouts (interleaved, planar) × 2 directions (larger/smaller) = 4.
  Matches the cell's 4 semicolon-separated items.
- **L22** (`extent_length` formula under index_encoding 1): 2 directions on
  the general mismatch, plus the two explicit edge alternatives the
  condition text itself calls out (`slot (0,0)` with `entry_count > 0`; a
  nonzero slot with `entry_count = 0`) = 4. Matches.
- **T3** ("not exactly the tile's decoded size"): 3 layout shapes ×
  2 directions = 6. Matches.
- **T14** (codec 1, "length differs from decoded size"): 3 layouts ×
  2 directions = 6. Matches.
- **T21** ("window size larger than the tile's decoded size" — bounded one
  direction only): 3 layout shapes, no doubling = 3. Matches (no spurious
  direction-doubling where the text itself bounds one way).
- **T22** (zstd content-size field "does not equal" decoded size):
  3 layouts × 2 directions = 6. Matches.
- **L20/L27/L28** (conjunctive value tests, e.g. "declares both A ≠ 0 and
  S ≠ 0", "S = 0 but nonzero A_slab", "entry_count = 0 but nonzero
  crc_of_crc_array"): single predicates over two fields, correctly one
  instance each (cell reads `—`).
- **L29** (`A_slab` malformed under `S ≠ 0`): three materially different
  malformed-value alternatives the condition text itself states (zero, not
  a power of two, above 2⁶²) = 3. Matches.
- **R7** (not well-formed JSON / top-level not object / leading BOM):
  3 alternatives × 2 containers (top-level, sub-record) = 6. Matches.
- **R8** (non-finite number: overflowing magnitude / bare token):
  2 alternatives × 2 containers = 4. Matches.
- **R4** (encoding-2 frame constraints): I independently derived this one
  against §18.2's own prose (see below) and got 7 distinct constraints ×
  2 containers = 14, matching the row.

I found no row where the enumeration disagreed with §21.1's stated policy.
Given the exact grand-total match plus this spot-check across rows using
every one of §21.1's stated axes (magnitude direction, layout-shape,
explicit alternatives, conjunctive-predicate collapse), I am confident the
277 figure is correct and that no individual row's instance count is
miscounted in a way that happens to cancel elsewhere.

### §21.9's own arithmetic

§21.9's Note derives two numbers from the entry_count guarantee (2³²) via
the segment-CRC array size (4 bytes per 2¹⁶-entry segment): I recomputed
both.

- At `entry_count = 2³²`: segments = 2³² / 2¹⁶ = 2¹⁶ = 65,536; array size =
  4 × 65,536 = 262,144 bytes = **256 KiB**. The Note says "still 256 KiB" —
  matches exactly.
- At `entry_count = 2³⁶`: segments = 2³⁶ / 2¹⁶ = 2²⁰ = 1,048,576; array size
  = 4 × 1,048,576 = 4,194,304 bytes = **4 MiB**. The Note says "it reaches
  4 MiB at 2³⁶" — matches exactly.

The "65,536 layers is roughly a 12.5 MiB directory... and the 16 MiB
directory row states that same budget" figure is explicitly hedged
("roughly", "assumed") and rests on an unstated average-record-size
assumption I cannot recover from the text alone; I did not find a
contradiction, but I also could not independently verify the 12.5 MiB
figure, since the assumed average record size is not given. I record this
under `confidence_empty` rather than as a finding, since the text itself
flags it as an approximation and not a claim of exactness.

## Row-versus-rule agreement (charter bullet 1)

I checked every row's governing rule against that rule's actual text where
the rule was one I had reason to read closely (either because it governs
several rows, because it sits in one of the three passages the brief names
as this cycle's changed surface, or because its scope-splitting logic
looked non-trivial). In every case below the row's condition, scope,
detector, and outcome matched the cited rule's text exactly:

- **F1/F6/F8/F14 vs R-CNT-24/R-CNT-06/R-ENC-02**: §6.2's `[R-CNT-06]`
  validates the trailer magic, trailer CRC, and version gate "in order,"
  and separately states the front block and trailer's owning scope is the
  file. §6.3's `[R-CNT-24]` fixes, across every format major, exactly three
  things: the trailer magic at F−64, the version fields' *position* (not
  value) at F−56, and the trailer CRC at F−4 over [F−64, F−4); plus the
  front signature block's constancy. §2.3's own worked Note (lines 283–294)
  explicitly derives that F14 (trailer CRC) and F1/F6/F8 (front block /
  trailer magic) *reach* every format major on this basis, while F5 (file
  size floor) and F15 (trailer reserved bytes) do *not* reach, even though
  F15's Governing-rule cell parenthetically cites `[R-CNT-24]`. I recompute
  this derivation myself in the ambiguity/observation section below,
  because the *parenthetical* citation pattern across F14/F15 struck me as
  asymmetric with which one actually reaches, though the reach analysis
  itself is stated correctly and does not move any byte.
- **F30–F33 / L15–L18 vs R-CNT-13**: §7.2's extent-slot paragraph
  states the general rule (either-half-zero, offset in [1,16), extent
  reaching F−64, and overflowing sum are validity errors "at the scope the
  record governs... the layer for a layer record and for sub-records, the
  file for other top-level records") and the overlap rule ("an intra-layer
  overlap... reject-layer, any overlap across layers or touching another
  scope's structures as reject-file, and any overlap between two
  structures neither of which belongs to a layer as reject-file"). F30–F32
  (non-layer top-level: half-zero, offset 1–15, reaches F−64) and L15–L17
  (the layer/sub-record equivalents) correctly split file-scope vs
  layer-scope exactly along that line; F33 (cross-layer/cross-scope/two-
  non-layer overlap → reject-file) and L18 (intra-layer overlap →
  reject-layer) correctly split the three-way overlap rule the same way.
  F33's own text even cross-explains why a slot of (0, N) with N ≠ 0 is
  F30's/L15's "half-zero" case and not F31's/L16's "offset 1–15" case
  (offset 0 is not in [1,16)) — I checked that this is logically correct.
- **F21/F22 and L10/L11 vs R-CNT-25**: §7.1's paragraph states "An extent
  of (0, 0) on a user-metadata record, or one whose extent_length is less
  than 5... is a validity error at its containing scope," matching F21/F22
  (top-level, file scope) and L10/L11 (sub-record, layer scope) exactly,
  including that (0,0) implies extent_length = 0 < 5, so F21 ⊂ F22 and
  L10 ⊂ L11 as §21.1 claims (see the specialization check below).
- **L21/L22 vs R-CNT-17**: §7.4's table and the paragraph under it state
  the exact formula (`extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉
  × 4`) and the entry_count-vs-geometry check; L21/L22's conditions restate
  this exactly, with the right instance enumeration (checked above).
- **L44 vs R-COD-07**: §17.2 (found via the L44 citation and by reading
  §20.3 step 4's own citation of "`[R-COD-07]`'s lz4 decoded-size cap (L44,
  the largest channel plane governing in a planar layer)") gives the exact
  cap `0x7E000000` and the planar-largest-plane rule; matches L44 verbatim
  in substance, and matches §21.9's hard-limits restatement of the same
  cap.
- **T2/T4/T5 vs R-SER-08/R-SER-05/R-SER-03**: §14.2's rule (`[R-SER-08]`)
  explicitly splits "the register witnesses" into T2 (in-tile byte,
  verifier-detected) and T4 (padding-position byte, also verifier-detected)
  — the text says so directly ("the same byte at a padding position is
  T4's, the two rows together covering `[R-SER-08]`"), and I confirmed T2's
  and T4's conditions are non-overlapping and jointly exhaust the rule's
  "any other byte" cases (real position vs padding position). T5 (pad-bit
  fill, packed bool) is `[R-SER-05]`/`[R-SER-03]`'s separate subject and is
  worded to match.
- **T17–T22 vs R-COD-06**: §17.2's zstd paragraph states magic-mismatch /
  skippable-or-second-frame / nonzero-dictionary-ID / content-checksum-flag
  / window-exceeds-decoded-size / content-size-mismatch as six discrete
  MUST-governed checks; T17–T22 map onto them one-to-one, matching wording,
  scope (tile), and detector (reader, except where the rule's own text says
  "header-checkable" — all six are reader-checkable at tile use, matching).
- **R1, R3, R4 vs R-CNT-25/R-MTA-03/R-MTA-09**: I read §18.2 in full and
  derived R4's instance list independently from its "Carried over — named
  for convenience, not as a closed list" enumeration: frame magic, no
  skippable/second frame, no nonzero dictionary ID, no content-checksum
  flag, and (per the paragraph that follows) the content-size field's
  equality with the *decoded document's* byte length. That is 5 named
  carry-overs plus the content-size constraint = 6 distinct constraints,
  but the register's R4 lists the "bytes remaining after the frame" case
  separately from "a second frame," giving 7 named alternatives × 2
  containers = 14 instances — matching my recount from §18.2's prose. I
  also verified that §18.2 explicitly excludes two of `[R-COD-06]`'s
  carried-over items from the register on named, different grounds
  (undisclosed dictionary use — unwitnessed; the buffer-sizing bar — binds
  a reader, not a file state), and R4's instance list correctly omits both.
  This is a case where the document does its own "which two rules govern"
  arithmetic explicitly and I could check the row against it directly
  rather than inferring.

I found **no row whose wording, scope, detector, or outcome diverges from
its cited governing rule.**

## Cross-references to register rows (charter bullet 3)

I swept the whole document for row-label tokens (`\b(F|L|T|R)[0-9]{1,2}\b`)
outside the 3733–4240 span, using
`grep -noE '\b(F[0-9]{1,2}|L[0-9]{1,2}|T[0-9]{1,2}|R[0-9]{1,2})\b' tarn.md`
filtered to lines outside §21, which returned 40 hits across 21 distinct
locations (§2.3's Note on reach; §4.6's Note on name duplication; §5.2's
slack-total paragraph; §7.1/§7.2/§7.4's own rule text; §9.1's user-metadata
quarantine cross-reference; §14.2's DEFLATE-trailing-byte Note; §17.2's
codec paragraphs; §18.1's quarantine paragraph; §20.3's re-declaration and
step-4 paragraphs; §20.4's persistence-table lead-in; Appendix F's reference
list; and Appendix H's four checklists). For every citation I located the
row(s) named and checked that the row's actual content is what the citing
sentence claims:

- §2.3's Note: "F14 reaches... F5 does not reach... F15 does not reach
  although its Governing rule cell cites `[R-CNT-24]`" — checked against
  the actual F5/F14/F15/F18 rows and R-CNT-24's own three-item invariant
  list; all four claims verified correct (detailed above and in the
  ambiguity section).
- §4.6's Note: "a duplicate is a validity error at file or layer scope
  (`[R-ENC-15]`, F4, L9)" — F4 is the file-scope layer-name duplicate, L9
  the layer-scope dimension/channel-name duplicate; correct pairing, no
  third case left uncovered (layer names are compared file-wide, so there
  is no "layer-scope" duplicate-layer-name case to miss).
- §5.2 (the slack-total paragraph, around line 738): "the rejection is one
  the walk itself established, L18's overlap or L40 through L42's
  placement among them" — L18 (verifier-detected overlap), L40 (verifier-
  detected per-tile alignment), L41/L42 (verifier-detected slab-run gap/
  overlap/misplacement) are indeed the register's verifier-detected,
  walk-derived layer rejections; correct.
- §7.2's extent-slot and overlap paragraphs, and §7.4's payload-parsing
  paragraph: checked above under row-vs-rule agreement.
- §9.1 (line ~998): "where a rule outside this quarantine records a
  document's defect at the file or the layer (`[R-MTA-05]`, F27, L48)" —
  F27/L48 are indeed the two `[R-MTA-05]` (member-ordering) rows, correctly
  described as sitting *outside* the R-CNT-25 quarantine (they are
  verifier/certification, not reader/ignore-record); correct.
- §14.2's Note: "a whole byte after the one holding the final bit does
  trail the stream, and `[R-COD-08]` rejects it (§21.4, T24)" — T24's
  condition ("bytes remain in the stored extent after the stream, frame,
  or block ends... any codec") is exactly this; correct.
- §17.2: covered above.
- §18.1 (line ~2648): "a malformed extent slot on such a record, (0, 0)
  included, is a validity error at the record's containing scope
  (`[R-CNT-13]`, `[R-CNT-25]`)" — this is the *slot* rule (F21/F22, L10/L11
  are the framing-level rows; the quarantine (R1–R10) is only the
  *document*, once the slot has already validated) — I checked this
  distinction is upheld consistently everywhere the two are cited together,
  and it is.
- §20.3 step 4 (lines ~3305–3319): "but for a stored tile's decoded size, a
  padding position or pad bit, or a boolean byte the register witnesses
  (T3, T14, T21, T22, T4, T5, T2) and a decode that fails outright, or a
  codec's framing check that precedes it, under a changed codec or filter
  (T17, T24, T25)" — I grouped these by what each cited row actually tests:
  {T3, T14, T21, T22} are all "decoded size" mismatches (matches "a stored
  tile's decoded size"); {T4, T5} are padding-position/pad-bit content
  (matches); T2 is the in-tile boolean byte (matches "a boolean byte");
  T25 is "decode fails outright" and T17/T24 are framing checks that
  precede a decode (magic mismatch; trailing bytes) — this is a
  representative rather than exhaustive list (several other T-rows, e.g.
  T15/T16/T18/T23, explicitly delegate their own detection to T24 or T25
  and so are subsumed rather than omitted), and I did not find this
  sentence claiming exhaustiveness — it is illustrating what *is* checkable,
  not enumerating every register row that could be. I treat this as
  correctly representative, not a completeness gap, and note it under
  rejected candidates.
- §20.3's "the bar binds a layer the commit keeps and nothing else"
  paragraph (the step-4 scope sentence named in the brief as one of the
  five changed clauses) states explicitly: "no file is nonconforming by
  virtue of its violation, and no register row records the violation
  itself, the register enumerating file-conformance violations (§21.1) and
  the bar stating no condition a file can exhibit (§21.7, `[R-ERR-01]`,
  `[R-CNF-02]`)." I checked this claim on its merits (it directly asserts a
  fact about my charter's territory — the register's completeness) rather
  than taking it on faith: the bar governs what a commit may do to a
  layer's declarations *across two generations* of the same file. A single
  live state (the only thing a reader, updater, or verifier ever validates
  — see §19.1's open, which never looks at superseded generations) cannot
  distinguish "this layer kept its declarations from the prior generation
  it superseded" from "this layer was dropped and a same-named layer with
  different declarations was added in its place" (§20.4 explicitly licenses
  the latter). No rule obliges a reader or verifier to reconstruct prior
  generations to check this (§9.7's coverage walk is over the live state
  only; a historical multi-generation reconstruction is explicitly a
  "recovery tool" concern outside normal reading, per the §20.4 Rationale's
  own admission that "nothing in either [trailer] says how many commits
  separate them"). So this bar is unwitnessed by §21.7's own test, and the
  claim that no register row is needed for it is correct. I did not find
  a completeness gap here.
- §20.4's persistence-table lead-in and Appendix H's "Conforming updater"/
  "Conforming verifier" checklists: cross-checked against F1/F6/F7/F36/L25/
  R1 and found each citation accurate (detailed above under sweeps).
- Appendix F (line ~4695, ~4697): cites T15 twice in the RFC 1951/1950/1952
  reference entries; T15's condition (zlib/gzip wrapper instead of raw
  DEFLATE) is exactly what those reference entries describe; correct.

I found **no citation that resolves to the wrong row or misstates a row's
content.**

## Completeness sweep (charter bullet 2)

I grepped every occurrence of "validity error" (51 hits), "reject-file",
"reject-layer", "reject-tile", "ignore-record", and "nonconforming" across
the whole document, and read the context of every one I had not already
placed against a register row through the row-vs-rule pass above. Beyond
what is covered above, three places explicitly discuss a condition that
sounds like it should be a register row and is not, and each is expressly
justified in the text itself as *not* a file-detectable condition (i.e.
unwitnessed under §21.7's test), rather than as a silent gap:

1. **R-ENC-06** (fixed field widths): §21.7 itself works this example —
   "a structure written at any other [width] yields different values at
   [the fixed widths]... a different file, conforming or not on its own
   terms. Nothing is omitted from the register on its account, there being
   no condition to omit." I checked this reasoning and it holds: there is
   no way to "read a field at the wrong width" and detect it as such,
   because parsing is *always* at the specified width — a file's bytes
   just are whatever they are read as.
2. **Sub-record nesting depth beyond two** (§7.4): explicitly flagged by
   its own Note as having "no reader-detectable witness, and so no register
   row" in format major 1, because detecting nesting requires parsing an
   unknown type's payload as a record sequence, which no reader does except
   for the one type (layer) whose own reappearance-as-sub-record §21.3
   *does* register (L26). Checked and consistent.
3. **§20.3 step 4's re-declaration bar**: covered above; explicitly
   unwitnessed and explicitly said so in the text, and I independently
   confirmed the unwitnessed-ness rather than taking the claim at face
   value.

I also checked, in the other direction, that §21.6's "not violations" table
does not overlap with §21.2–§21.5's actual violations, row by row (14
entries), and that the two entries explicitly called out as *moved into*
the violation rows from a former §21.6-like status (unsorted user-metadata
member ordering → F27/L48; a registered type's stored MU/PE bit differing
from the registry → F28/L49) are consistent with the closing paragraph's
own accounting ("Two conditions that once sat in this table are violations
and are registered above"). I found no row in §21.2–§21.5 that duplicates
a §21.6 entry, and no §21.6 entry that contradicts the register.

I did **not** find a detectable, file-conformance-affecting condition
stated anywhere in the document that lacks a register row, nor a register
row that registers something the cited rule does not actually make a
violation.

## Outcome vocabulary (charter bullet 5)

§2.4 defines exactly five outcome values: reject-file, reject-layer,
reject-tile, ignore-record (all four are reader outcomes, used across
§21.2–§21.5's four subsection headers, one outcome per subsection, all
four reachable), and preserve-verbatim (an updater obligation, explicitly
"orthogonal to reader outcomes" and therefore correctly *absent* from the
register's own outcome column — I checked and no register row uses it).
Every row's outcome matches its subsection header outcome (I did not find
a row silently claiming a different outcome than its subsection). All five
defined values are reachable: the four reader outcomes each label a whole
subsection (35+49+26+10 rows respectively) and preserve-verbatim is used
throughout §20.4's table. No orphaned or undefined outcome token appears
anywhere in §21.

Detector values are exactly "reader" and "verifier" throughout, matching
§2.3's actor definitions. Detected-tier values are "open," "layer access,"
"tile use," "extent use" (matching §19.2's four reader tiers exactly, by
name), and "certification" (matching §19.2's "or *certification* for the
rows a verifier detects, which §19.2 places outside the reader tiers
entirely"). I wrote `check_detector.py` to verify, over all 120 rows
mechanically, that no row pairs `detector = reader` with `detected =
certification` or `detector = verifier` with any of the four reader tiers
— it found zero mismatches. (L23's split cell, "open (the name field...);
layer access (every other field...)", is a reader-only split across two
reader tiers and does not trip this check, correctly.)

## Limits cross-reference (charter bullet 6)

I compared every quantity in §21.9's minimum-guarantee table and hard-limit
paragraph against its defining section:

- **rank ≤ 255 / ≥ 1, channel count ≤ 65,535 / ≥ 1**: §7.4's table types
  rank as `u8` (≤255) and channel count as `u16` (≤65,535); L32 registers
  the floor-of-1 violations. Matches §21.9's hard-limit paragraph exactly.
- **name/key length ≤ 255 bytes**: §4.6's name rules (`[R-ENC-12]`) and
  §18.2's folding of those rules onto user-metadata keys; matches §21.9's
  hard-limit paragraph's explicit statement of the same fold.
- **lz4 decoded-tile cap `0x7E000000`**: matches L44 and §17.2's codec-4
  paragraph verbatim; also restated identically in Appendix C's registry
  snapshot (`0x7E000000`) and in §20.3 step 4's own citation.
- **offset/length/extent/count ceiling 2⁶³−1**: matches `[R-ENC-03]`/
  `[R-ENC-04]` and F2/F3/L1/L2/T11/T12 exactly.
- **alignment A (power of two, 512–2⁶²) and slab alignment A_slab (power of
  two, 1–2⁶²)**: matches §16.1/§16.2 (`[R-SLB-01]`, `[R-SLB-02]`) and
  L29/L39 exactly.
- **slab run length S, 1 ≤ S ≤ 2⁶³−1**: matches §16.2 and §7.4's table.
- **directory ≥ 4 bytes at offset ≥ 16, and 128-byte file floor**: matches
  §6.2/§5.1 and F5/F9/F16 exactly.
- **8 MiB zstd `Window_Size` guarantee**: I traced every occurrence of
  "Window_Size" and "8 MiB" in the document (7 occurrences) and confirmed
  the *same* 8 MiB figure is used consistently for (a) the tile-codec
  window advisory in `[R-COD-06]`, (b) the user-metadata document window
  advisory in §18.2, and (c) §21.9's and Appendix C's restatement of the
  guarantee. No second, conflicting number appears anywhere.
- **256 MiB decoded-tile guarantee and 16 MiB user-metadata-document
  guarantee**: both restated identically in Appendix C's registry
  snapshot; I found no other section stating either quantity differently.
  §21.9's own Note describing 256 MiB as "an order of magnitude above the
  tile sizes §11.3 describes as ordinary" is loosely worded against
  §11.3's stated "roughly 1 to 16 MiB" workable range (256 MiB is ~16×
  the top of that range, which is on the loose edge of "an order of
  magnitude" but is explicitly hedged language in a non-normative Note,
  not a hard figure); I did not treat this as a finding, since it makes no
  claim that could be wrong at the byte level and the Note is exempt under
  R-CNF-01 in any case.

I found **no limit stated in §21.9 that conflicts with the defining
section's own statement of the same limit**, in either direction.

## The strict-specialization claims in §21.1

§21.1 asserts five specific narrower/broader pairs: "F1's front-block
instance of F6 and its trailer-magic instance of F8, F35 of F36, L24 of
L25, F21 of F22 and L10 of L11." I checked each logically (does every file
exhibiting the narrower condition necessarily exhibit the broader one?):

- F1(front) ⊂ F6: a byte-reversed 16-byte constant is (for a
  non-palindromic constant, which the actual magic bytes are) not
  byte-identical to the constant — true.
- F1(trailer) ⊂ F8: symmetric argument for the trailer magic — true.
- F35 ⊂ F36: F35 additionally requires MU=1 on top of F36's "reserved-range
  type value, whatever its MU bit" — true by construction.
- L24 ⊂ L25: same relation at layer scope — true.
- F21 ⊂ F22: extent slot (0,0) means extent_length = 0, and 0 < 5, so F21
  implies F22's "extent_length is less than 5" — true.
- L10 ⊂ L11: same argument at layer scope — true.

All five hold. I also checked that in each pair the detector and detection
point match between narrower and broader row (§21.1 says the narrower row's
detector/detection-point are "the ones that apply," implying they could in
principle differ) — in all five pairs both rows are `reader`/`open` (F-pairs)
or `reader`/`layer access` (L-pairs), so there is no conflict to resolve.

## Rejected candidates

- **F14/F15's asymmetric use of the `[R-CNT-24]` parenthetical.** F14
  (trailer CRC) does *not* cite `[R-CNT-24]` in its Governing-rule
  parenthetical (it cites R-CNT-20, R-ENC-09 instead), even though §2.3's
  Note explicitly derives F14's cross-major "reach" from `[R-CNT-24]`.
  F15 (trailer reserved bytes) *does* cite `[R-CNT-24]` parenthetically,
  even though the same Note says F15 does *not* reach on that rule's
  account. I opened this as a possible row-vs-rule divergence. It closes
  on §21.1's own sentence: "any identifiers following [the governing rule]
  in parentheses are further rules the condition reads, **a finding aid and
  not the whole of them**" — the parenthetical is explicitly non-exhaustive
  and is not the mechanism §2.3 actually uses to derive reach (§2.3 does
  that "condition by condition" from the rules' substance, not from the
  register's parenthetical citations). Since the parenthetical's own
  documented job is only "a finding aid," its asymmetric use across F14/F15
  does not misstate either row's condition, scope, detector, or outcome —
  the four things the charter's row-vs-rule bullet asks me to compare — so
  I closed this without filing it. I mention it here rather than silently
  discarding it, since it is a genuine textual oddity even though it is not
  a defect under the charter's own terms.
- **§20.3 step 4's illustrative T-row list not being exhaustive.** Opened
  as a possible closed-list-presented-as-complete issue (shape #5 in the
  round's list of twelve). Closed because the sentence does not claim
  exhaustiveness — it says what *is* checkable among several categories,
  using one or two representative row labels per category, and several
  omitted T-rows (T15/T16/T18/T23) explicitly delegate their own detection
  to the rows that are cited (T24/T25), so they are subsumed rather than
  missing.
- **65,536-layers → "roughly 12.5 MiB directory" figure.** Opened as a
  possible limits cross-reference error. Closed: the text hedges it as
  "roughly," and I could not derive a contradiction because the assumed
  average per-layer-record size behind the estimate is not stated; this is
  recorded under `confidence_empty` rather than filed as a finding, since I
  have no way to show it is wrong, only that I cannot independently confirm
  the specific figure.
- **256 MiB "an order of magnitude above" §11.3's 1–16 MiB range.** Opened
  as a possible limits inconsistency. Closed: both figures are explicitly
  hedged ("roughly," "workable range in practice"), the comparison sentence
  is inside a non-normative Note, and no byte-level claim rests on the
  approximation being exact.

## What I did not find

I did not find a CONTRADICTION between any register row and the rule it
cites. I did not find an AMBIGUITY in the register's own governing text
(§21.1) that I had to resolve by picking a reading — every rule I traced
(the strict-specialization list, the instance-enumeration rules, the
quarantine/scope split, the outcome vocabulary, the detection-tier names)
matched its restatement in the register exactly, and where the document
itself flags a subtlety (F15's parenthetical-but-non-reaching citation, the
unwitnessed conditions, the two former-§21.6 entries now registered as
violations), it explains the subtlety in its own words rather than leaving
it for a reader to discover. I looked hard for a completeness gap in both
directions and found none: every "validity error"/"reject-*"/"ignore-
record" statement I traced outside §21 either matches an existing row or is
explicitly and correctly justified as unwitnessed (no condition a file can
exhibit, or not detectable by any check the specification obliges), and
every row inside §21 traces back to a rule that actually makes the
condition a violation at the stated scope with the stated outcome.

I am reporting zero findings that meet the CONTRADICTION or AMBIGUITY bar.
Given this project's own calibration history (many zero rounds, several of
them later confirmed clean by refute passes), a register-specific zero is a
plausible true result, not evidence by itself that I under-searched — but I
record it as a zero, not as "clean," and leave the refute phase to test it.
