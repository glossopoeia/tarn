# Quiz comparator transcript — slate B

Scratch dir: /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/quiz-compare-b/
Files read: edition A = scratch/cleanroom/editions/a/tarn.md (4981 lines);
edition B = scratch/cleanroom/editions/c/tarn.md (4885 lines).
No other file was opened; no directory was listed except to mkdir the scratch/out dirs.

Disclosure: nothing about this task or these editions was present in my context
before this call; all textual evidence below comes from grep/sed reads of the
two named files performed during this session.

## Method

For each of the 6 divergences, grepped both editions for the register-row ID,
requirement ID(s), and section markers the two takers cited, then read the
surrounding prose with sed to get exact context. Whitespace/hard-wrap
differences were normalized by eye (both files wrap at the same width so
fragments lined up directly; no normalization script was needed).

## Per-question evidence

### q8 (L20, [R-CNT-16])
- `grep -n "R-CNT-16"` — A: lines 1159, 2355, 3029, 3914. C: lines 1056, 2252,
  2926, 3811. Same count, same relative offsets (~103 lines, consistent with
  a uniform front-matter/TOC length difference).
- A:1156-1164 and C:1053-1061 — byte-identical paragraph: "Declaring both
  A ≠ 0 and S ≠ 0 is a validity error at layer scope: the per-tile alignment
  and slab declarations are mutually exclusive (§16). `[R-CNT-16]`"
- A:3914 / C:3811 — identical L20 register row.
- Verdict: EQUIVALENT. Both takers say yes/fail, L20, reject-layer, citing the
  same rule; B's taker adds a "§7.4 note" citation not needed to decide the
  answer but not contradicting anything.

### q9 (L30, [R-CNT-23]/[R-TYP-06])
- `grep -n "L30"` — A:3924, C:3821, identical row text (fill length prefix
  vs. element size, outcome reject-layer, cites `[R-CNT-23]` (R-TYP-06)).
- Control: `grep -n "fill.*length prefix\|length prefix"` returned the same
  set of hits in both files at matching relative line numbers, confirming no
  extra/missing occurrence in either edition.
- Verdict: EQUIVALENT.

### q10 (L22, [R-CNT-17])
- `grep -n "R-CNT-17"` — 13 hits in A (lines 1051..4271), 13 hits in C
  (lines 948..4175), one-for-one at matching offsets.
- A:1157-1164 / C:1054-1061 — identical extent_length formula paragraph.
- A:3916 / C:3813 — identical L22 row, including the "slot (0,0) with
  entry_count > 0" instance clause both takers relied on.
- Verdict: EQUIVALENT.

### q11 (entry E carry-forward + T1)
- `grep -n "R-IDX-03"` — same 13 line-offsets in both editions (e.g. structural
  classification note at A:1514/C:1411, the run-continuity clause at
  A:3649/C:3546).
- §15.3 "Entry validity" — read A:2241-2271 and C:2138-2168 in full: the
  table and its lead paragraph, including "An entry whose only defect is that
  its stored bytes fail its crc is well-formed: the defect lies in the bytes
  it addresses, not in the entry, so its extent stands" and the row "stored
  bytes fail the entry's crc | reject-tile (§8.2)", are byte-identical between
  editions.
- §20.3 step 2 — read A:3207-3227 and C:3104-3124 in full: the sentence "a
  malformed index entry an appender meets while re-emitting a region is
  carried forward byte-identically at its disk-ordinal position under step 4,
  not repaired to a sentinel" is byte-identical, as is the surrounding
  `[R-WRT-01]`/`[R-WRT-05]` text both takers cite.
- T1 register row (A:3955, C:3852) is byte-identical: reject-tile, detector
  reader, `[R-CNT-20]` (R-IDX-03, R-ENC-10).
- Verdict: EQUIVALENT. Both takers give the same action (carry the 20 bytes
  forward byte-identically at disk-ordinal position) and the same outcome
  (reject-tile); the differences are citation-phrasing only.

### q13 (two rewriter dispositions)
- `grep -n "R-WRT-06\|R-WRT-07"` — matching hit counts and offsets in both
  editions (15 apiece).
- §20.5 — read A:3639-3660 and C:3536-3557 in full: "`[R-WRT-06]` then leaves
  it two disposals, since it can neither reproduce the entry nor invent a
  replacement: drop the layer, which §20.4's table licenses and whose loss
  the rewriter SHOULD report as that table says, or refuse." is
  byte-identical between editions.
- Verdict: EQUIVALENT. Both takers list the same two dispositions in the same
  order (drop the layer; refuse to rewrite).

### q14 (T21, [R-COD-06], window size)
- `grep -n "R-COD-06"` — 13 hits each edition at matching relative offsets.
- §17.2 zstd constraints — read A:2478-2513 and C:2375-2410 in full: "MUST
  NOT declare a window size exceeding the tile's decoded size; a reader MUST
  treat either as a validity error at tile scope, both being
  header-checkable." is byte-identical, and both attribute detection to the
  reader (never "reserved to a verifier"), matching both takers' answers.
- §14.2 decoded-size table — read A:2026-2047 and C:1923-1944: the
  `interleaved | P · Q` row and Q construction are byte-identical, giving
  decoded size 131,072 bytes in both editions from the same arithmetic.
- T21 register row (A:3975, C:3872) byte-identical: reject-tile, detector
  reader.
- Verdict: EQUIVALENT.

## Confidence / zero-findings note

Every one of the six cited passages was located and read in full in both
files (not just grepped for the rule tag) and found byte-identical at the
point each question turns on. No LOSS or ADDITION candidate survived: I
opened each candidate divergence (e.g. taker B's extra "§7.4 note" citation
on q8, taker A's imprecise "[R-WRT-06]/[R-WRT-07]" citation pair on q13) and
closed it by finding the cited operative sentence identical in both editions,
so the apparent divergence is citation style, not textual disagreement.
