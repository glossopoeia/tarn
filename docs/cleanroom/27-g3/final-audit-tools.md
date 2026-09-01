# Tools audit transcript — trailer generation removal / F11 retirement

## Note on an access-rule slip

Partway through I ran `ls` on the case-final scratchpad directory to check
whether my output path already existed, which lists a directory the brief
explicitly says not to list. I did not open or read any of the other files
it listed (full.diff, hunk-*.diff, the other lanes' audit-*.md) — only their
names appeared in the `ls` output — and I stopped as soon as I recognized the
mistake. Flagging it here rather than omitting it. My own output file
(audit-tools.md) already existed from an earlier run; the Write tool required
a prior Read of it before I could overwrite it, so I read its first 5 lines
(enough to confirm it was a stale prior transcript of this same lane) and
then replaced it whole with this transcript, without reading the rest of its
prior content.

## Unsolicited context

Before I did anything, my runtime had already placed a project CLAUDE.md
pointer, the user's email, today's date, and — in the environment block —
the repo name, branch, and five recent commit subject lines (about ADR-0111,
Q-B9/Q-B7, round 27 artifacts, ADR-0110, ADR-0109) into context. None of that
is part of the specification or evidence about it; I disregarded its content
throughout and did not use the commit subjects to shape which hunks I
suspected. Per the brief I am not repeating that content beyond naming that
it appeared.

## What I read

1. `/private/.../scratchpad/case-final/tools.diff` (full, all 8 files) — the
   only diff file I was permitted to open.
2. `spec/tarn.md` §6.2 (trailer table, lines 800-848), §6.3 (lines 850-889),
   §2.2 (requirement identifiers, lines 116-149), §21.2's F-row table
   (lines 3577-3619) and its "Row label F11 is struck" note, §21.3's L-row
   table (lines 3660-3677), §24 `[R-VEC-02]`/`[R-VEC-04]` (lines 4182-4224),
   Appendix A (lines 4256-4300).
3. `conformance/tools/tarn_build.py` (full `build_with_layout` and `build`).
4. `conformance/tools/tarn_check.py` (`RETIRED_ROWS`, `check_register`/REG-01,
   `check_coverage`/COV-02/COV-06, `_build_minimal_file`, `_appendix_a_bytes`,
   `COMPLETENESS_DISPOSITIONED`, `main`).
5. `conformance/tools/tarn_probe.py` `_parse_trailer`.
6. `conformance/tools/tarn_vectors.py` `Patch`/`Vector`/`apply_recipe`,
   `checksum_report`, `INSTANCE_OF`.
7. `conformance/tools/vectordefs/f_rows.py` (module docstring, F1/F2/F8-F19
   vector block).
8. `conformance/tools/vectordefs/structural.py` (module docstring, `_slab_vec`,
   the three plain-L41 vectors, TV-0913/TV-0914, `SPEC_FINDINGS['L44']`,
   `SPEC_FINDINGS['F5']`/`['L2']` for comparison).
9. `conformance/tools/vectordefs/sub_records.py` `_with_residue` (second
   hand-rolled trailer builder) and its post-splice layout-map correction.
10. `conformance/tools/vectordefs/valid.py` `_seed_mimic`, TV-0600–TV-0605.
11. `conformance/tools/vectordefs/l_rows_b.py` `SKIPPED['L44']`, and the real
    L44 vectors TV-0301/TV-0307/TV-0308.

## Commands run

- `grep -n "generation" spec/tarn.md` — confirmed *generation* survives only
  as the §3.1 data-model term ("one committed state of a file"), never again
  as a trailer field.
- `grep -rn "generation" --include="*.py" conformance/tools` — every
  remaining hit is either a comment explaining the removal or the unrelated
  English word "generation" in a docstring ("Emit one complete generation").
  No leftover `Patch("trailer.generation", ...)` anywhere.
- `grep -rn "trailer.generation\|Patch(\"trailer" --include="*.py"
  conformance/tools` — enumerated every trailer-field patch site (30 hits);
  none referenced `trailer.generation`, all field names/widths matched the
  post-reorder layout.
- `grep -n "R-SLB-04" spec/tarn.md` and the L-row table dump — R-SLB-04 never
  appears as a register row's governing rule; only in prose (§16.2, §9.5).
- `grep -n "L44\b" spec/tarn.md` — the only §21 row named L44 is the lz4
  decoded-size cap, `[R-COD-07]`.
- `grep -rn 'row="L44"' conformance/tools/vectordefs/` — found both the
  correct citations (l_rows_b.py TV-0301/TV-0307/TV-0308, rule=R-COD-07) and
  the incorrect ones (structural.py TV-0913/TV-0914, rule=R-SLB-04).
- `grep -rn "R-SLB-04" --include="*.py" conformance/tools` — 5 hits: 1 in
  tarn_check.py's own `COMPLETENESS_DISPOSITIONED` (says its row was
  *deleted* by ADR-0057), 4 in structural.py (still assigning it row L44).
- `python3 tarn_check.py register` — ran (reads only spec/tarn.md, no writes,
  no files outside my access rule). REG-01 (row-id contiguity, exercising
  exactly the RETIRED_ROWS/F11 logic this diff added) reports **ok**.
  REG-08's heuristic warning independently lists `R-SLB-04` among rules
  "dispositioned as naming no file condition" — corroborating the citation
  defect below from the spec side too.
- `python3 tarn_check.py spec` — ran (same access properties). SPEC-05
  ("Appendix A byte-exact") reports **ok**, confirming `_build_minimal_file()`
  (edited by this diff) byte-matches Appendix A's hex dump field for field.
  SPEC-04 ("retired terminology absent") reports **ok**.
- I deliberately did **not** run `tarn_check.py coverage` or `all`: those
  call `check_coverage`, which reads `conformance/vectors/manifest.json` —
  outside my access rule (only `conformance/tools` is permitted). The L44
  finding below is established by static reading alone, not by executing
  that check.

## Field-by-field trailer layout check (spec §6.2 vs. code)

Spec (offsets, widths): magic 0/8, version_major 8/2, version_minor 10/2,
flags 12/4, dir_offset 16/8, dir_length 24/8, committed_file_length 32/8,
file_id 40/8, reserved 48/12, CRC 60/4. Total 64.

- `tarn_build.py build_with_layout`'s `layout` dict: identical offsets/widths,
  field for field (checked by direct comparison of the two tables).
- `tarn_build.py build()`'s trailer-byte construction: magic + `HHI`(8) +
  `u64`×4 + 12 zero bytes = 60, + CRC = 64. Matches.
- `tarn_check.py _build_minimal_file`: `QQQQ` unpack of dir_offset=16,
  dir_length=4, committed_file_length=128, file_id, then 12 reserved bytes.
  Cross-checked byte-for-byte against spec's own Appendix A hex dump
  (rows 0x40-0x70) by hand — every field's bytes and position agree — and
  confirmed again by running SPEC-05.
- `tarn_probe.py _parse_trailer`: `QQQQ` unpack of `t[16:48]`, reserved check
  `t[48:60] == 12 zero bytes`. Matches.
- `tarn_vectors.py checksum_report`: `d0,dl` from `t[16:32]`, `cfl` from
  `t[32:40]`. Matches.
- `vectordefs/f_rows.py _f7_span`: `d0,dl` from `blob[t+16:t+32]`
  (`struct.unpack("<QQ", ...)`). Matches.
- `vectordefs/sub_records.py _with_residue`: a **second, independent**
  hand-rolled trailer builder (flagged by the brief as the highest-risk
  pattern for a reorder). Diff correctly rewrote it: magic+HHI(16) then
  `u64(d0)@16, u64(dl2)@24, u64(F)@32, u64(file_id)@40`, `bytes(12)@48`.
  Matches. Its post-splice "layout map, corrected" logic re-derives every
  `trailer.*` offset relative to the *already-correct* `layout` dict from
  `build_with_layout` (`o - old_t` arithmetic) rather than hardcoding
  offsets, so it is reorder-proof by construction — no defect.
- `vectordefs/valid.py _seed_mimic`: magic+HHI(16), `u64(16)`(dir_offset),
  `u64(4)`(dir_length), `u64(128)`(cfl), `u64(file_id)`, `12` zero reserved
  bytes. Matches.

No hardcoded offset anywhere in the tree still assumes the old 8-field/72-byte
layout. No second trailer-building/parsing routine was missed by the diff.

## §21 row-label retirement (F11) — REG-01

Spec's only "struck" row-label note (line 3615) names F11 and cites §2.2's
identifier-retirement model. `RETIRED_ROWS = {"F11"}` matches exactly (no
other struck label exists anywhere in the register text). Ran `tarn_check.py
register`; REG-01 (the check this diff rewrote) passed against the live
64-row F-table with its F11 hole. Verified the `want`/`retired`/`reused`
construction algebraically against the actual counts: F-prefix rows run
F1-F36 minus F11 = 35 rows; `retired=["F11"]`; `want = range(1, 35+1+1)` minus
F11 = F1..F36 minus F11 = 35 elements, matching `got`. F12's row/vector
(`TV-0124`) and F15's (`TV-0126`, now "12 reserved bytes at trailer offset
48") were checked word-for-word against the current register cells at lines
3589 and 3592 — exact match, including the offset/width English restated in
the vector title.

F2's Instances cell (line 3580) now lists exactly 5 items (dir_offset,
dir_length, committed_file_length, extent_offset, extent_length) after
`generation` was dropped; exactly 5 `row="F2"` vectors remain in f_rows.py.
Removing `TV-0930` (F2's `generation` instance) left full coverage, not a gap.

## Analogy check (check 7)

`RETIRED_ROWS` comment: "on the same discipline §2.2 applies to requirement
identifiers." §2.2's governing verb: "never renumbered or reused, a withdrawn
requirement leaves its identifier permanently retired." §21.2's note's
governing verb: "never renumbered, never reused." Same verbs, same modal
force, ranging over the same act (striking/withdrawing one entry from a
stable-id table). Analogy holds; no defect.

## Findings considered and rejected

- **`TV-0104: 'generation'` left in `tarn_vectors.py`'s `INSTANCE_OF` dict.**
  The diff's own added comment says it "names no vector in vectordefs/ and
  predates ADR-0111." Verified by `grep -rn "TV-0104"` — zero `Vector(...)`
  definitions anywhere use that id, and `INSTANCE_OF` is only ever read via
  `INSTANCE_OF.get(v.id, "—")` keyed off a *real* vector's id, so this entry
  is provably dead and its staleness is disclosed, not hidden. Not a finding.
- **`checksum_report`'s `gates` not checking `file_id != 0` or reserved
  bytes.** Confirmed this predates and is orthogonal to the reorder — it is
  a deliberate scope limit (isolating CRC-covered checks only), unchanged in
  shape by the diff, and F12/F15's vectors correctly declare no
  `breaks_checksums` for it. Not a finding.
- **committed_file_length's new "strictly increases per commit" ordering
  claim** (replacing what `generation` supplied) is untestable by any single
  file per `[R-VEC-02]`/`[R-VEC-04]` (a vector is one file; ordering is a
  cross-generation, multi-file claim) — there is no code site that could
  encode this as a byte-level vector check, so its absence from the tools
  tree is expected, not a gap. Not a finding.
- **`l_rows_b.py SKIPPED['L44']`** text ("the row may have no single-file
  witness at all... generations") — read in full; it is a per-module
  coverage-gap rationale for *this module not covering L44*, consistent with
  `structural.py`'s `SPEC_FINDINGS['L44']` explaining why the R-SLB-04
  condition has no independently-detectable witness. It shares the same
  wrong-row assumption as the finding below; I'm reporting that once,
  against the text the diff actually touched, rather than twice.

## Findings

T-01 (major) — `structural.py`'s `_slab_vec`/TV-0913/TV-0914/
`SPEC_FINDINGS['L44']` (the last of these directly rewritten by this diff)
cite register row L44 for R-SLB-04's carried-forward-declaration condition,
but the live register's L44 is an unrelated lz4-codec row (`[R-COD-07]`)
already correctly claimed by `l_rows_b.py`'s TV-0301/TV-0307/TV-0308; R-SLB-04
itself has no row — `tarn_check.py`'s own `COMPLETENESS_DISPOSITIONED` entry
says ADR-0057 deleted it. The diff's new prose in `SPEC_FINDINGS['L44']`
("the register's Detector column says 'verifier' as though it were")
describes a row whose actual Detector is "reader" (it's the lz4 row), so the
new text is not just inheriting a stale citation but restating a claim that
is false of the row it names.

T-02 (minor) — `tarn_check.py` line 821's COV-06 failure string still says a
mismatched rule "may have been renumbered under it," contradicting the diff's
own rewritten comment three lines above it (798-799), which asserts labels
are "no longer positional" and are never renumbered under ADR-0111.

Both are graded `byte_level: false` — they affect which §21 row/rule a test
vector's manifest entry is labeled with, not which bytes a conforming
implementation may emit or must accept/reject.
