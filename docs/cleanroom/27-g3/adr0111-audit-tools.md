# Tools auditor transcript — ADR-0111 (generation removal / F11 retirement)

## Disclosure

Before starting substantive work, unrequested context appeared in my system
prompt: a CLAUDE.md pointer (AGENTS.md), a user memory index file naming
several TARN-project memory notes (by title only — I did not open any of
them), the user's email, and today's date. None of this is part of the
specification or evidence about the change under audit; I disregarded all of
it and am naming only its presence here, not its contents, per my brief.

I also received a system reminder recommending Bash-first tool use
generally. My charter for this task fixes the access rule (spec/tarn.md,
conformance/tools/**, and tools.diff only, no writes to the repo) and takes
precedence; I used Read/Bash(grep/cat, read-only) only against files inside
that allow-list.

## What I read

- `/private/tmp/.../scratchpad/case-adr0111/tools.diff` (full, via Read) —
  9 hunks across tarn_build.py, tarn_check.py, tarn_probe.py, tarn_vectors.py,
  vectordefs/f_rows.py, vectordefs/structural.py, vectordefs/sub_records.py,
  vectordefs/valid.py.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`:
  §6.2 (Trailer, lines 800-849), §6.3 (850-905), §2.2 (116-150),
  §21.1 (3478-3558), §21.2 table + F11 retirement Note (3560-3613),
  §24 / R-VEC-02 (4160-4214), R-ENC-03 / §4.2 (443-455), R-SLB-03/04
  (2270-2307), Appendix A hex dump + byte table (4245-4287).
  Also grepped the whole file for "generation" (line 372-4561, all hits)
  and for "F11\b", "R-VEC-02", section headings.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/conformance/tools/`:
  read tarn_build.py (full trailer-building sections), tarn_check.py
  (Spec class/parser lines 148-260, check_register/REG-01..08 lines
  291-479, COV-01/02/04/06 lines 760-815, _build_minimal_file/
  _appendix_a_bytes lines 635-667), tarn_probe.py (_parse_trailer and
  probe() lines 175-294), tarn_vectors.py (Patch/Vector/apply_recipe
  150-220, checksum_report 235-275, INSTANCE_OF dict 431-725, manifest()
  727-770), vectordefs/f_rows.py (VECTORS preamble and F1/F2 block
  205-343, SPEC_FINDINGS-adjacent code), vectordefs/structural.py
  (_trailer helper 130-150, _slab_vec 204-233, call sites, SPEC_FINDINGS
  L44 entry 655-685), vectordefs/sub_records.py (_with_residue, ~170-180),
  vectordefs/valid.py (_seed_mimic, TV-0604/TV-0605), vectordefs/l_rows_b.py
  (SKIPPED dict, L44 entry, 599-640), vectordefs/t_rows.py (line 372
  context), conformance/tools/propagation-acks.txt (grepped for
  "generation"/"file_id"/"R-CNT-27"; read the R-LIF-01, R-CNT-27,
  R-CNF-13 lines this diff's story touches).
- Ran read-only greps across `conformance/tools/**` for: `TRAILER_MAGIC`,
  `generation`, `committed_file_length`, `file_id`, `"trailer.generation"`,
  `"trailer.reserved"`, `MAX63`, `INSTANCE_OF`, `56:60`/`t + 56`,
  `t + 24`/`t + 40`/`t + 48` (looking for any second hand-rolled trailer
  builder/parser or leftover old-layout offset the diff might have missed).

No writes were made anywhere. No files outside the allow-list were opened,
and I did not list the scratchpad directory or open full.diff.

## Header-vs-body check

Each hunk's file/line header matched its body's actual target (verified by
re-reading the current file at the stated location for tarn_build.py,
tarn_check.py, tarn_probe.py, tarn_vectors.py, and each vectordefs/*.py
file touched). No mismatch found.

## Per-hunk rule statement and checks

**Hunk 1 (tarn_build.py, build_with_layout + build):** Drops the
`generation` parameter and the `trailer.generation` layout entry; shifts
`dir_offset`→t+16, `dir_length`→t+24, `committed_file_length`→t+32,
`file_id`→t+40, `reserved`→(t+48, 12); rewrites the directory-span unpack
to read from t+16 instead of t+24; the trailer-assembly byte string drops
`u64(generation)` and widens the reserved pad from 4 to 12 zero bytes.

- Byte-for-byte against §6.2's table (lines 805-816): dir_offset 16/8,
  dir_length 24/8, committed_file_length 32/8, file_id 40/8, reserved
  48/12, CRC 60/4 — exact match, both fields and offsets.
- Cross-checked against Appendix A's hex dump and byte table (4256-4281):
  I manually decoded the dump row by row (front block, empty directory,
  44-byte pad, trailer fields) and it reproduces the same layout with the
  same concrete file_id and CRC value the spec prints (0x402F157E) — this
  is an independent confirmation from a different part of the document
  that was not itself part of the diff.
- No second trailer-building/parsing site was missed: grepped
  `TRAILER_MAGIC` and hardcoded offsets 24/40/48/56 across the whole
  `conformance/tools` tree; every hit is either inside this diff's own
  files at the new correct offsets, or unrelated prose.

**Hunk 2 (tarn_check.py, RETIRED_ROWS + REG-01):** Adds
`RETIRED_ROWS = {"F11"}` and rewrites REG-01 from "row ids must be exactly
1..N contiguous" to "row ids must be exactly 1..N+retired contiguous,
excluding retired labels, and a retired label must never reappear."

- Restates §21's own rule: I opened §21.2's Note (3608-3612) — "A row
  label is retired on the model §2.2 states for a withdrawn requirement
  identifier — never renumbered, never reused" — and R-VEC-02 (4182-4185)
  — "a row label is never renumbered and never reused, so it denotes one
  condition for the life of format major 1, exactly as §2.2 makes the
  identifier permanent." The code comment's citation "(ADR-0111; §24
  [R-VEC-02])" resolves to exactly this text, in §24 (heading at 4160).
  Tense/quantifier/scope match: both text and comment use "never" /
  "permanently" with no exception.
- §2.2 itself (116-122) confirms the model being borrowed from: "a
  withdrawn requirement leaves its identifier permanently retired."
  Analogy check (Check 7): spec's governing verb for identifiers is
  "leaves ... permanently retired" / "never renumbered or reused"; for
  row labels it is (R-VEC-02) "never renumbered and never reused" —
  same verbs, same force, ranging over the same kind of set (a label
  namespace). The analogy holds exactly, not just approximately.
- Arithmetic check: F-rows in the table = 35 (counted directly,
  3560-3607), matching §21.2's stated "35 conditions" (line 3562) and
  matching REG-01's derivation: got = 35 ids (F1-F10, F12-F36), retired =
  {F11}, want = range(1, 35+1+1) minus {F11} = F1..F36 minus F11 = 35
  ids = got. Passes by construction on real data.
- No contradiction found elsewhere in §21.1 or §21.2 for this policy.

**Hunk 3 (tarn_check.py, _build_minimal_file):** Rewrites the hand-built
minimal 128-byte trailer to 4 QQQQ fields (no generation) + 12 reserved
bytes.

- I manually summed the byte budget: front 16 + directory-CRC 4 + pad 44 +
  trailer body 60 (8 magic + 8 header + 32 for four u64 fields + 12
  reserved) + 4 CRC = 128. Matches the 128-byte floor the function's own
  docstring and Appendix A both assert.
- Compared field-by-field against Appendix A's printed hex dump — dir_offset
  16, dir_length 4, committed_file_length 128, file_id
  0x0123456789ABCDEF, 12 zero reserved bytes, CRC 0x402F157E — identical.

**Hunk 4 (tarn_probe.py, _parse_trailer):** Drops the generation unpack
and its `gen < 1` gate; unpacks `do, dl, cfl, fid` from t[16:48]; checks
reserved at t[48:60] against 12 zero bytes.

- Matches R-CNT-06's ordered gate list (833-843): magic, CRC, version,
  then flags/committed_file_length=size/committed_file_length%64/
  dir_offset≥16/dir_length≥4/dir_offset+dir_length≤F-64/file_id≠0/reserved
  zero. No generation gate exists in the current spec text (confirmed by
  a full-file grep of "generation" — every remaining hit is either the
  glossary's *generation* concept definition at §3.1, prose about
  generations-as-commits, or references inside vectordefs comments I
  separately checked below; none is a trailer field requirement).
- Downstream callers (`probe()`, all four transport modes) check
  `info["F"] != size` using the dict's new key set (`dir_offset, dir_length,
  F, file_id` — no `generation` key referenced anywhere after this hunk).

**Hunk 5 (tarn_vectors.py, checksum_report + INSTANCE_OF):** Shifts the
directory-span/committed_file_length unpack to t+16/t+32; drops the
`'TV-0930': 'generation'` INSTANCE_OF entry; adds a comment marking
`'TV-0104': 'generation'` as pre-existing/orphaned and leaves it; drops
`'TV-0123': 'generation'`; widens `TV-0126`'s description from "[56,60)"
to "[48,60)".

- checksum_report's gate arithmetic (d0≥16, dl≥4, d0+dl≤t, cfl==F,
  cfl%64==0) is unchanged in substance, only the byte offsets it reads
  from moved to match the new layout — verified against §6.2 directly.
- TV-0104: grepped the entire tools tree for `TV-0104\b`; it appears
  nowhere as an actual `Vector(...)` definition. INSTANCE_OF is only ever
  read via `INSTANCE_OF.get(v.id, ...)` keyed off vectors that actually
  exist (`tarn_vectors.py:747`), so an orphaned key is dead data, not a
  behavioral defect — nothing iterates INSTANCE_OF's keys expecting a
  vector to back each one. I could not verify the comment's historical
  claim ("predates ADR-0111") against git history, which is outside my
  access rule; but whether or not that specific claim is exactly right,
  the entry is inert either way and out of scope for this diff (it is
  untouched code, not part of what changed).
- TV-0126's offset text: confirmed reserved now sits at [48,60) (12
  bytes) per §6.2 — matches.

**Hunk 6 (vectordefs/f_rows.py):** Directory-span unpack moved to
t+16/t+32 in `_f7_span`; the byte-reversal seed-choice comment's tail
(about a byte-reversed *generation*) is replaced by a parenthetical
noting ADR-0111 removed that field and that the retained first half of
the note never depended on it; TV-0930 and TV-0123 (`Vector(...)` objects)
are deleted and replaced by an explanatory comment; TV-0126's patch value
widened from a 4-byte `\x01\x00\x00\x00` to 12 bytes
`\x01 + \x00*11`.

- I independently re-derived the retained comment's arithmetic to check
  the parenthetical's claim that it "never depended on" generation: 320
  (the `meta` seed's F) as 8 little-endian bytes is
  `40 01 00 00 00 00 00 00`; byte-reversed and read back as
  little-endian gives `0x4001000000000000` — exactly the value the
  (unchanged) comment states, and this is committed_file_length
  arithmetic, not generation arithmetic (128 reversed → bit 63, which is
  the *other* half of the same sentence and is about avoiding an
  incidental F2 hit from a small committed_file_length, again not
  generation). The diff's added parenthetical is correct: the retained
  reasoning was always about committed_file_length/seed-size choice, and
  only the sentence removed ("generation's only gates are ≥ 1 ... 128 is
  the smallest such value") was actually about the removed field.
- F2's register row (3573) instances cell reads "dir_offset; dir_length;
  committed_file_length; non-layer top-level record extent_offset;
  extent_length" — five instances, no "generation" — matching the five
  surviving F2 vectors (TV-0107/108/109/110/111) exactly, and consistent
  with TV-0930's deletion.
- TV-0126's new 12-byte patch value matches trailer.reserved's new
  (t+48, 12) layout entry; grepped for any other `"trailer.reserved"`
  patch site — none exists.

**Hunk 7 (vectordefs/structural.py):** `_trailer` helper drops the
`generation` parameter and widens reserved to 12 bytes; `_slab_vec` drops
the `generation=` kwarg (which used to append a
`Patch("trailer.generation", ...)`) in favor of a boolean `l44=` flag that
only sets `scope["co_violates"]`; TV-0913/TV-0914 titles and call sites
updated from "generation 2 carries..." to "a later commit carries...", and
`SPEC_FINDINGS['L44']` rewritten to explain that the generation counter
was the last in-file evidence of succession and that nothing the row
actually turns on depended on it.

- Checked R-SLB-03 (2272-2292) and R-SLB-04 (2294-2300) directly: R-SLB-04
  is "detected as the invariant failures of R-SLB-03 are: by a verifier,"
  and a Note (2302-2307) states "every file exhibiting one exhibits a run
  whose tiles are unpacked or whose first stored tile is misaligned" —
  this is exactly the premise SPEC_FINDINGS['L44'] relies on ("every L44
  file is an L41 or L42 file"), and it is untouched by ADR-0111, so the
  finding's central claim still holds after the edit.
  R-LIF-08 (1400, 1474) confines a verifier to the live state — matches
  the finding's citation.
- `_trailer`'s only call site (`_F15_APPEND = bytes(8) + _trailer(16, 4,
  200)`) passes only positional dir_offset/dir_length/cfl, no stale
  `generation=` kwarg.
- `_slab_vec`'s only other call sites (TV-0912, TV-0932, TV-0933) don't
  pass `l44`, defaulting to False — no leftover `generation=` argument
  anywhere in the file (grepped `_slab_vec(` for all 5 call sites).
- Width check: `_trailer`'s body is magic(8)+header(8)+3×u64(24)+
  file_id(8)+reserved(12) = 60, +4 CRC = 64 — unchanged total trailer
  size, consistent with §6.2's "trailer occupies the final 64 bytes."

**Hunk 8 (vectordefs/sub_records.py, `_with_residue`):** Trailer literal
drops `u64(1)` (generation) and widens the reserved tail from `bytes(4)`
to `bytes(12)`.

- Byte accounting: magic(8)+header(8)+u64(d0)+u64(dl2)+u64(F)+
  u64(file_id)(32)+reserved(12) = 60, +4 CRC = 64. Consistent.

**Hunk 9 (vectordefs/valid.py, `_seed_mimic` + TV-0604/TV-0605):** The
mimic-trailer literal drops `u64(7)` (a "plausible generation") and widens
reserved from 4 to 12 zero bytes; its docstring is reworded to drop
"a plausible generation" from the list of fields the mimic trailer
imitates; TV-0604 and TV-0605 drop their `trailer.generation` patches and
reword their titles to describe only the file_id ceiling/floor.

- §21.6 / R-LIF-06 (referenced in the docstring) — the docstring's claim
  ("nothing enumerates slack and no reader scans for trailers, so the
  lookalike is inert") is not itself touched by this hunk and was not
  re-derived by me since it does not depend on which fields the mimic
  trailer contains, only on the fact that it sits in slack.
- TV-0604's reworded claim — "file_id 0xFFFFFFFFFFFFFFFF, its ceiling as
  a u64 with no upper domain limit of its own [R-CNT-06]" — checked
  against §6.2's table: file_id's Valid values cell is only "≠ 0" (814),
  no upper bound, so "no upper domain limit of its own" is accurate; the
  ceiling is only the plain u64 ceiling (2^64-1), which is what the vector
  patches. R-CNT-06 (843) is the right citation (it's the rule enumerating
  file_id's own gate, "file_id ≠ 0").
- TV-0605's reworded claim — "file_id 1, its floor: the smallest value
  [R-CNT-06] permits" — 1 is indeed the smallest value satisfying "≠ 0."
  Correct.

## Other checks run across the whole tools tree (not tied to one hunk)

- Full-tree grep for `generation` turned up only: (a) already-reviewed
  comments in structural.py/f_rows.py explaining the removal; (b)
  l_rows_b.py's SKIPPED dict entry for "L44" and PARTIAL-adjacent prose,
  which use "generation" in the spec's *conceptual* sense (a committed
  state) and are not about the trailer field; (c) t_rows.py's "placement,
  not generation" which uses "generation" as a verb (crafting a byte
  stream), unrelated; (d) propagation-acks.txt's two lines about
  ADR-0111 (R-LIF-01→R-LIF-02, R-LIF-01→R-CNT-27), which are the record
  of the spec-side sweep, not part of tools.diff and not something I was
  asked to audit. None of (b)-(d) is touched by tools.diff, and none
  contains a functional (non-comment) reference to a `generation` field
  in code.
- I noticed `l_rows_b.py`'s `SKIPPED["L44"]` entry ("The condition ranges
  over a sequence of generations ... may have no single-file witness at
  all") sits alongside `structural.py` actually building TV-0913/TV-0914
  for row L44 with a `SPEC_FINDINGS['L44']` entry describing them as
  real, if imperfect, vectors. On its face these two files disagree
  about whether L44 has any witness at all. I traced whether this is
  something tools.diff introduced or broke: `SKIPPED` is not consumed by
  any checker (grepped `SKIPPED` across every .py file in the tree; the
  only other hit is a passing mention in a `tarn_propagate.py` docstring,
  not a read of the dict), so nothing enforces agreement between the two
  files, and `l_rows_b.py` is not one of the 8 files this diff touches at
  all. TV-0913/TV-0914 already existed as vectors before this diff (the
  diff only edits their title strings and the `l44=` plumbing, it does
  not add them), so this apparent disagreement predates ADR-0111 and is
  not something the reordering/removal broke. I am treating this as
  outside my charter ("does this specific change break what was already
  there") rather than reporting it as a finding, since the change did not
  touch it and did not make it any more or less true.
- Grepped for any hardcoded old-layout offsets (`t + 24`, `t + 40`,
  `t + 48`, `[56:60]`, `t + 56`) outside what the diff already updated —
  none found; every remaining `t + 24`/`t + 40`/`t + 48` hit is a
  *new*-layout offset already covered above.
- Checked REG-04 (subsection row-count check) and REG-05/REG-08
  (completeness heuristics) are unaffected in substance by this diff
  (none of their code was touched, and the F-row count they validate
  against, 35, is unchanged by relabeling F11 as retired rather than
  renumbering).
- Confirmed no vector cites the retired label "F11" anywhere (grepped for
  `row="F11"` conceptually via review of f_rows.py — TV-0123, the only
  vector that ever cited F11, is exactly the one this diff deletes), so
  COV-02 ("cited rows exist" — checks vectors against `spec.rows`, which
  the parser builds only from actual table rows and therefore never
  contains "F11") stays consistent.

## Findings considered and rejected

- *TV-0104 orphan INSTANCE_OF entry* — considered as a possible
  stale-reference finding, rejected: unused dead data (see above), not
  behavior-affecting, and the diff's own comment already flags it as
  out-of-scope/pre-existing rather than silently leaving it.
- *l_rows_b.py SKIPPED["L44"] vs. structural.py's built L44 vectors* —
  considered, rejected: pre-existing (not touched by tools.diff), not
  consumed by any checker, and not something this specific change could
  have broken since it never read or wrote that dict.
- *Whether checker code needs a cross-generation "committed_file_length
  strictly increases" check* — considered, rejected: no existing or
  removed code in `conformance/tools` ever validated an ordering
  invariant across multiple files/generations (the tools operate on one
  file at a time); this is purely a spec-prose claim outside the tools'
  reach, so there is no tool-side gap to report.

## Result

No byte-level or logic defects found in tools.diff. The trailer layout in
tarn_build.py's layout map and in every hand-rolled trailer-building/
parsing site (tarn_check.py, tarn_probe.py, tarn_vectors.py, and all four
touched vectordefs/*.py files) agrees field-for-field and byte-for-byte
with §6.2's table and with Appendix A's worked example. RETIRED_ROWS/
REG-01's policy change is a correct, word-for-word-matching implementation
of R-VEC-02's stated rule, itself modeled explicitly on §2.2. No stale
offsets, no orphaned functional (non-comment) references to the removed
`generation` field, and no policy the checker still enforces that the
specification change reversed.
