# Cross-hunk audit transcript — trailer `generation` removal (29 hunks)

## Disclosure

Unrequested context appeared in my context window before I began: a project
instruction file, an index of the maintainer's persistent notes, and an
environment block naming the repository, branch and git status. I did not treat
any of it as evidence and I do not repeat its contents. I did not read
`full.diff`, `tools.diff`, `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`CLAUDE.md`, git history, or the web, and I did not list the case directory.

### What I read
- `/private/tmp/.../case-adr0111/hunk-01.diff` … `hunk-29.diff` (all 29, by
  explicit `cat` of named paths).
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, by
  targeted `sed`/`grep`: §2.2 (116–150), §2.3 (245–285), §3.1 (390–402),
  §4.2/[R-ENC-03]–[R-ENC-05] (445–475), §4.5 CRC definition (502–510),
  §5.1 (620–645), §6.2 (800–860), §6.3 (858–890), §6.4 (893–935),
  §9.1–9.7 (1228–1440), §19.1 (2816–2870), §20.1–20.5 (3025–3477),
  §21.1 (3478–3560), §21.2 (3560–3613), §21.5 (3708–3741), §21.7 (3796–3868),
  §21.8 (3869–3875), §22.5 (4058–4073), §23.1–23.2 (4074–4147),
  §24 (4160–4210), Appendix A (4249–4300), Appendix B (4300–4335),
  Appendix D (4358–4380), Appendix G (4423–4470, 4499–4570).

### What I ran
- `wc -l` on the hunk files; `cat` on each named hunk file.
- `grep -n` for: `generation`, `committed_file_length|committed file length`,
  `file_id`, `R-CNT-24`, `R-ENC-03|R-ENC-04`, `R-SLB-05|R-CNT-21`,
  `offset 56|offset 48|[56|[48|F − 56`, `CRC-32C`, `[0-9]+ conditions`,
  `121|277|275`.
- A Python row/instance counter over §21.2–§21.5 (semicolon-separated
  Instances cells, a `—` cell counting 1, per §21.1's mechanical rule).
- A Python CRC-32C (poly 0x82F63B78 reflected, init 0xFFFFFFFF, final XOR
  0xFFFFFFFF), validated against §4.5's check vector, then run over the old and
  new Appendix A trailers.

## Header verification (mechanical headers vs. bodies)

I checked every hunk header's line range and named preceding heading against
the current file. `sed -n '151p;341p;800p;1234p;1304p;1391p;3025p;3044p;3059p;
3275p;3334p;3560p;3614p;3796p;3869p;4058p;4112p;4160p;4249p;4358p;4423p'`
returned exactly the headings the hunk headers name. I hand-counted the hex-dump
and table blocks in Appendix A: 4261–4263 are precisely the three changed dump
rows and 4276–4281 precisely the six changed table rows. **No header/body
mismatch found in any of the 29 hunks.**

## Grouping by rule

- **Trailer layout** ([R-CNT-06], [R-CNT-24]): h03 (table), h04 (reader gate
  list), h17 (F2), h18 (F11 struck, F15), h26/h27 (Appendix A).
- **Ordering quantity** ([R-LIF-02], [R-LIF-03]): h02 (glossary), h05, h06,
  h07, h11, h12, h20, h23.
- **Rollback / out-of-band state** ([R-LIF-06], [R-SEC-07], [R-PRV-03]):
  h08, h23, h24, h29.
- **Compaction** ([R-WRT-06], [R-WRT-07]): h09, h10, h13, h14, h15, h21.
- **Register bookkeeping** ([R-ERR-01], [R-ERR-02], [R-VEC-02]): h16, h19,
  h21, h22, h25.
- **Rationale** : h28.

## Arithmetic

**h01 — [R-CNT-06] "states nine … the other seven".** Deriving the conditions
[R-CNT-06] itself states (excluding §6.3's version and flag gates, which it
only invokes): magic; trailer CRC; cfl = file size; cfl multiple of 64;
dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; file_id ≠ 0;
reserved zero = **9**. The register rows governed by [R-CNT-06] are F8, F14,
F17, F13, F9, F16, F10, F12, F15 = **9**. Magic and CRC reach across majors;
9 − 2 = **7**. Both numbers check.

**h16 — §21.2 "35 conditions".** Row labels present: F1–F10, F12–F36 = 35. ✓

**h22 — §21.8 "120 conditions over 275 instances".** Machine count:
§21.2 35/56, §21.3 49/116, §21.4 26/55, §21.5 10/48 → **120 / 275**. ✓
Per-section stated counts (35, 49, 26, 10) sum to 120. ✓ The instance delta of
2 is F11's single instance plus `generation` dropped from F2's cell. ✓

**h21 — §20.5's "three obligations".** §20.5's trailer obligations are: MUST
mint a fresh file_id; output trailer MUST copy unknown ignore-lane bits
forward; version_minor SHOULD be at least the input's. Exactly **three**. ✓
"For the last two" still names flags and minor. ✓

**h03/h18/h27 — widths and offsets.** 8+2+2+4+8+8+8+8+12+4 = 64. ✓ Reserved
[48,60) is 12 bytes. ✓ [R-CNT-24]'s fixed bytes are [0,8), [8,12), [60,64) = 16,
leaving 48 redefinable = [12,60); reserved [48,60) ⊂ [12,60), so §2.3's untouched
Note ("inside the 48 that rule lets a future major redefine") still holds, and
[R-CNT-24]'s "zero slack: every byte is assigned" still holds. ✓
Appendix A file offsets: trailer base 64, so trailer 16→[80,88), 24→[88,96),
32→[96,104), 40→[104,112), 48→[112,124), 60→[124,128). ✓

**h26/h27 — Appendix A CRC.** My CRC-32C reproduces §4.5's check vector
(`"123456789"` → 0xE3069283, stored `83 92 06 E3`). Over the OLD 60-byte trailer
it returns 0xE00938D2 (`D2 38 09 E0`) — the value the deleted line carried,
confirming the model. Over the NEW 60-byte trailer (magic; 01 00; 00 00;
00000000; dir_offset 16; dir_length 4; cfl 128; file_id EF CD AB 89 67 45 23 01;
12 zero bytes) it returns **0x402F157E**, stored little-endian `7E 15 2F 40` —
exactly the changed bytes at 0x7C. ✓ The hex dump rows and the byte table agree
with each other and with the §6.2 table.

**h06 — the 128-byte floor derivation.** F−64 ≥ priorF + 4 ⟹ F ≥ priorF + 68;
F and priorF multiples of 64 ⟹ F ≥ priorF + 128. ✓ [R-CNT-27]'s own argument:
F−64 ≥ 20 ⟹ F ≥ 84 ⟹ F ≥ 128. Same shape, same constant. The analogy holds.

## Citations opened

- §2.2 (h19, h25): "Identifiers are stable: they are never renumbered or reused,
  a withdrawn requirement leaves its identifier permanently retired." Both
  hunks' analogies to it are verb-for-verb accurate.
- §24 [R-VEC-02] (h19's target): the paragraph h25 rewrites does end with
  `[R-VEC-02]`, so h19's "(§24, `[R-VEC-02]`)" resolves. ✓
- [R-ENC-03] (h07): "All file offsets … are `u64` … valid range … 0 to 2⁶³ − 1."
  Supports "F ≤ 2⁶³ − 1". ✓ (but see X-05).
- [R-SLB-05] (h08): placement freedom, line 2242. ✓ [R-CNT-21] (h08): slack,
  line 722. ✓
- [R-CNT-27] (h06): §5.1 line 636–640, 128-byte floor. ✓
- §20.2 [R-WRT-02] (h13): "A creator MUST follow `[R-LIF-02]`'s creation path".
  h13's "as §20.2 obliges a creator" matches verb for verb (MUST follow). ✓
- §9.2 step 1 (h06): "(1) begin writing at exactly F (§9.4)". ✓
- [R-CNT-24] (h18's F15 parenthetical, §2.3's Note): checked above. ✓
- Appendix G item 2's file_id hash is defined over "the trailer's first 60 bytes
  with the `file_id` field zeroed" — position-independent, so the reorder leaves
  no stale offset there. ✓ Appendix B lists no trailer field offsets and no
  generation constant. ✓
- §19.1 step 2 defers to §6.2's order; no field list to restate. ✓
- Full `grep -n "generation"` sweep: every surviving occurrence is *generation
  as a committed state*, never as a field. No stale reference.

## Findings considered and REJECTED

1. **§21.7 cites ([R-LIF-01], [R-LIF-03]) for the strict growth, not
   [R-LIF-02].** [R-LIF-03] does state "Within one file_id, F strictly
   increases per commit", so the citation resolves; and the old text cited the
   same pair for the generation sequence. Not a new defect.
2. **h06's Note calls the strict increase "not an extra obligation on the
   writer" while §21.7 lists it among "obligations".** "Extra" carries the
   qualification; a derived obligation is still an obligation. Wording tension
   only.
3. **§20.5 paragraph 1 carries no trailing requirement identifier, yet §21.7
   attributes its file_id MUST to [R-WRT-06].** Pre-existing; the identifier
   plausibly closes a two-paragraph requirement. Not introduced here.
4. **The F11-retirement policy's §21 statement is a labelled Note (h19) and
   therefore non-normative.** It is not *only* there: h25 states it in §24's
   normative [R-VEC-02] text. Check 3 passes.
5. **h25 scopes label permanence to "the life of format major 1" while §2.2
   scopes identifier permanence unqualifiedly.** §21's conditions are
   major-1 conditions anyway ([R-CNF-13], §2.3); the asymmetry is harmless.
   Reported as a passing analogy comparison, not a finding.
6. **Nothing was left unpinned by the removal.** I enumerated every trailer
   quantity and found each still fixed: file_id on a commit by [R-LIF-03]
   ("the file_id chosen at creation") and §20.3 step 6; version_minor by
   [R-CNT-26]; flags by [R-CNT-08]; dir_offset/dir_length/cfl/reserved by
   [R-CNT-06]; F's floor by [R-CNT-27]/F5 and its multiple-of-64 by F13 — so
   deleting F11 (generation ≥ 1) left no hole, because committed_file_length
   already carries its own floor row and alignment row.
7. **h07's "identifies each of them" and the cache rule's "same F / higher F /
   lower F" trichotomy.** Sound for one file under a conforming writer; the
   file_id-collision hole is reported separately as X-02 rather than twice.

## Findings kept

X-01 §9.6's "signed (file_id, committed_file_length) pair" is defeated by the
      attack the same passage just described.
X-02 §9.3's new first Note infers same-prefix identity from a (file_id, F)
      match, contradicting the same requirement's own reused-file_id warning.
X-03 §20.5's "indistinguishable by their trailers alone" is refuted in terms by
      §23.2 and Appendix G item 4, both changed in this same edit.
X-04 §20.3 step 6 restates [R-LIF-02]'s "at least 128" as "necessarily above",
      and its supporting enumeration names a pad that may be zero-length.
X-05 §9.3's ceiling Note names an F (2⁶³ − 1) no conforming file can carry.
X-06 §23.2's "no longer states" is a diff artifact with no referent in the
      published text.
