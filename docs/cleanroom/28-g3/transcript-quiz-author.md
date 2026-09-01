# Round 28 — quiz author transcript

**No answers appear anywhere in this file.** Where I say a question "resolves",
I mean that I satisfied myself the document fixes one answer; I do not record
what it is.

## 1. Access and disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,648 lines, 281,820 bytes). It was exactly where the brief said it would be.
I read it end to end in five passes (lines 1–400, 400–849, 849–1298, 1298–1717,
1718–2147, 2148–2567, 2566–2985, 2985–3403, 3404–3803, 3803–4202, 4202–4648).

I ran `wc -l` and `ls -la` against that path, and one `grep -n` against that
file only (searching for every use of "committed file length" /
"committed_file_length", to sweep the field the format change re-pointed).
I listed no directories.

I ran local Python (no file reads) to implement CRC-32C per §4.5 and to check
this document's own stated constants and worked arithmetic. Nothing else: no
ADRs, no `docs/`, no `conformance/`, no `registry.json`, no git history, no web.

**Unrequested context.** Before I began, my runtime placed a `system-reminder`
in context containing a project instruction file (`CLAUDE.md`, which forwards to
`AGENTS.md`), the maintainer's email address, and today's date. I did not open
`AGENTS.md` or anything else it named, and nothing in it informed a single
question or finding. Disclosed here because the brief requires it; its contents
are not repeated.

## 2. Calibration pass — checking the document against itself

Before authoring I re-derived every constant and worked number I could, because
the brief said one of the four commits changed the bytes (a field removed from
the trailer, the following fields moved, the freed bytes not reclaimed, and a
quantity the removed field supplied now carried by a different field). A stale
offset or a worked example whose arithmetic no longer follows was the highest-
value thing available. Everything below **checked out**:

- **CRC-32C implementation** reproduced §4.5's check vector for `"123456789"`
  and for zero bytes, so the checks that follow are trustworthy.
- **§7.4's layer-record example.** Field-by-field byte accounting (4 + 34 + 18 +
  12 + 13 = 81) matches the hex dump's offsets exactly; the four-sentinel
  80-byte entry array's segment CRC and the crc_of_crc_array over those four
  bytes both reproduce the stated values; `[R-CNT-17]`'s extent length for
  entry_count 4 reproduces.
- **Appendix A's 128-byte minimal file.** Every annotation-table byte range
  lines up with the hex dump under the *current* trailer layout — magic 0,
  version_major 8, version_minor 10, flags 12, dir_offset 16, dir_length 24,
  committed_file_length 32, file_id 40, reserved 48 (12 bytes), CRC 60 — and
  the stated trailer CRC reproduces exactly. This is the passage I most
  expected to be stale after a field removal. It is not.
- **§15.4's all-sentinel full-segment constant** reproduces.
- **§15.4's two worked index examples** (entry_count 1,000,000 segment
  arithmetic; the C=4/N=32 planar disk ordinal and its region bytes) reproduce.
- **§17.3's byte-shuffle example** reproduces under the stated permutation.
- **§14.2's three offset examples** and **§14.3's packed-plane example**
  reproduce.
- **§9.3's ceiling note** (2⁶³ − 64 as the largest 64-multiple the value domain
  admits, and no further commit possible there) is arithmetically right — this
  was the "ceiling re-pointed at a new quantity" shape the brief warned about,
  and it survives.
- **Register totals.** I counted every row and every Instances cell under
  §21.1's stated convention: §21.2 = 35 rows / 56 instances (F11 struck),
  §21.3 = 49 / 116, §21.4 = 26 / 55, §21.5 = 10 / 48. Totals 120 rows and
  **275 instances** — exactly what §21.8 claims. The register's own arithmetic
  is internally consistent.
- **§2.3's "`[R-CNT-06]` states nine"** cross-checks against §21.2: exactly nine
  rows name `[R-CNT-06]` first (F8, F9, F10, F12–F17), of which two assert
  invariants `[R-CNT-24]` fixes. Consistent.
- **§20.5's "one row for each of the other seven spaces §10.2 tabulates"**: the
  seven named rows map one-to-one onto §10.2's non-record-type spaces.
- **§14.4's P = 1 claim** (the two layouts' images coincide exactly when the
  bool fill is false) is right, and I turned it into a question.

I found no arithmetic defect. That is a real result for a document whose bytes
were changed four commits ago, and it is why my findings list is short rather
than padded.

## 3. The slate — what each question is for

Fifteen questions. Every one has a single determinate answer I reached from the
document, and every one requires combining at least two places.

**Concrete bytes at concrete offsets (4).**

- **Q01 — trailer checksum.** A described trailer; produce the four stored CRC
  bytes. This is the direct probe of the changed structure: an implementer who
  still has file_id or the reserved run at the old offsets produces a different
  checksum, and the two files differ on disk. Requires §6.2's layout, §4.1's
  endianness and §4.5's CRC parameters. Deliberately uses values unlike
  Appendix A's so it cannot be answered by copying.
- **Q02 — bfloat16 channel entry.** Assemble a complete channel entry. Requires
  §7.4's channel-entry framing, §12.1's type ID *and* element size, `[R-TYP-02]`
  applied to a binary32 pattern rather than copied from §12.1's worked example,
  and `[R-CNT-23]`'s fill-length rule.
- **Q03 — filtered stored bytes.** Requires §14.1's interleaved value order,
  §14.2's byte layout and little-endianness, §17.3's stride rule (which for an
  interleaved tile is the sample stride, not an element size), and codec 1's
  identity. Wrong stride here is the exact failure `[R-COD-10]` describes.
- **Q04 — one bool sample, both layouts.** The degenerate-case probe (shape 8):
  P = 1, one channel, fill true. Requires §14.2's interleaved bool byte, §14.3's
  packing and pad-bit definition, and `[R-SER-05]`'s fill-bit rule for pad bits.
  Two implementations that skip the pad-bit rule emit a different byte.

**Reader / verifier verdicts on a specific malformed file (4).**

- **Q05 — a reaching condition under a foreign major.** Byte-reversed front
  block, version_major 3. Forces the answerer through `[R-CNF-13]`'s reach test,
  §21.2's derivation of which rows reach, `[R-CNT-04]`'s residency test, and the
  rule that a reaching failure is rejected on its own requirement's ground and
  reported *nonconforming* by a verifier that does not implement the major.
- **Q06 — reserved vs experimental metadata encoding.** One byte apart. The
  reader outcome is the same for both; the *file's* conformance and the
  verifier's verdict are not. Requires §18.2, §10.2's partition, §21.5's R1
  preamble, §21.6's row, and `[R-MTA-10]`.
- **Q07 — experimental MU = 1 as a layer sub-record.** §21.6 calls the
  top-level/sub-record qualifier load-bearing. Requires `[R-CNT-18]`,
  `[R-CNF-02]`, and §2.3's cannot-establish grounds — three sections, three
  different answers.
- **Q08 — sentinel pattern with a nonzero crc.** Requires §15.2's sentinel
  definition, §15.3's classification table, §21.4's row labelling, and
  `[R-TYP-09]`/`[R-CNF-09]`'s bar on standing fill in for a rejected tile. A
  reader that returns fill here silently corrupts a caller's data.

**Arithmetic (4).**

- **Q09 — planar geometry to index bytes.** Grid counts, addressed-tile count
  for a planar layer, `[R-CNT-17]`'s extent-length formula including its
  segment-array term, `[R-GEO-06]`'s channel-major disk ordinal, and §15.1's
  20·k placement. Four integers, four distinct places in the document.
- **Q10 — interleaved decoded size and a value's offset.** Sample stride over a
  mixed bool/float64/uint16 channel set (bool element size 1 in the arithmetic),
  the permanent row-major in-tile ordinal, and §14.2's in-sample offset.
- **Q11 — the smallest next committed file length.** Directly on the quantity
  that now orders generations: §9.2's at-least-128 growth plus §6.2's
  64-multiple rule. A writer that emits a smaller value produces a file
  `[R-CNT-06]`/`[R-LIF-02]` reject.
- **Q12 — instance total of §21.5.** Applies §21.1's counting convention (a
  cell reading `—` is one instance; semicolons separate) to a table, and is
  cross-checkable against §21.8's 275. Chosen over the same question about
  §21.4 because the shorter table keeps the comparison clean.

**Rules whose statement is spread across sections (3).**

- **Q13 — a compacted file's trailer.** §6.3's flags = 0 requirement against
  §20.5's copy-forward obligation, plus §20.5's version_minor floor, which
  applies only because a carried ignore-lane bit is a feature the compactor does
  not implement.
- **Q14 — dropping a droppable sub-record.** §20.4's MU = 0 / PE = 0 row turns
  on whether the commit *independently* changes the scope the record attaches
  to; §20.3 step 4 supplies the fact that superseding a tile re-places that
  layer's index region and so modifies that layer's record. Two layers, two
  different answers, one commit.
- **Q15 — an over-long pre-trailer gap.** §6.2 says such a gap is conforming and
  no conforming commit produces one; §2.3 names it as a conduct rule; §9.2 step 5
  and §20.2/§20.5 close the creator and compactor paths. Tests the
  file-predicate / actor-obligation distinction the brief flags as the dominant
  cause of mis-grading.

## 4. Candidates I rejected, and why

- **"How many conditions does the register hold in total?"** — §21.8 states 120
  outright. A lookup.
- **"What is the CRC of a full all-sentinel segment?"** — §15.4 and Appendix B
  both print the constant.
- **"Which trailer field numbers a file's generations?"** — the answer is
  "none", which is stated in §3.1, §9.3, §20.4 and §23.2. Four places saying it
  makes it a lookup, not a synthesis, and a one-word negative answer invites a
  divergence over phrasing rather than over substance.
- **A second "reach" question** using a failing trailer CRC under a foreign
  major. Dropped: it fails together with Q05 for the same reason
  (`[R-CNF-13]`'s reach test), which the brief forbids.
- **Rebuilding §7.4's 81-byte layer-record example with different values.**
  Attractive, but so close to the printed example that a careful answerer
  transcribes rather than derives; Q02 and Q09 get at the same framing rules
  without the transcription path.
- **Anything turning on a SHOULD's content** — `[R-CNT-03]`'s zeroing,
  `[R-CNT-09]`'s 64 KiB window, `[R-TYP-10]`'s zero fill. `[R-CNF-12]` puts
  SHOULD deviation outside the register, so the emittable set cannot move and
  the question would not be byte-level. Q13 asks for a SHOULD *floor value*,
  which is a number the document fixes, not a dispute about what a SHOULD
  requires.
- **Appendix G items.** Non-normative by its own heading and by `[R-CNF-01]`;
  a divergence there could not fork a conforming file.
- **A question about which §21.2 rows name `[R-CNT-06]` first.** Good, but it
  tests table-scanning stamina more than rule-combination, and Q12 already
  covers the "closed count derived from a stated convention" shape.

## 5. Findings

Two, both graded OBSERVATION. Neither forks the bytes; I say so explicitly in
each rather than reaching for byte-level, per the brief's third and fourth
discriminators. I did not find a byte-level defect, and I decline to promote a
cosmetic one to fill a quota.

1. `quiz-01` — §20.4's preservation table states normative updater obligations
   but carries no requirement identifier of its own, and §21.6 cites
   `[R-WRT-08]` for a permission that rule's sentence does not state.
2. `quiz-02` — §21.6's zero-layers entry, and `[R-CNT-14]`'s parenthesis behind
   it, gloss "zero layer records" as "an empty directory", which does not
   follow: a file with no layer records may still carry a top-level
   user-metadata record.

Details, quotations and locations are in the structured result.
