# Cleanroom round 17 — quiz author transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,317 lines, in five sequential Read calls). Ran `wc -l` on that same
file. Wrote and ran two scratch Python files under my own scratchpad
(`crc.py`, plus inline `python3 -c` computations) that read no project
files. No `docs/`, no ADRs, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`/`AGENTS.md`/`README.md`, no git history, no directory listings,
no web. I did not read the round-17 output directory.

## Method

1. Read the document cold, front to back.
2. Reimplemented CRC-32C from §4.5's parameters and checked it against
   §4.5's own check vector (`"123456789"` → `0xE3069283`; empty → `0`).
   Both reproduce.
3. Re-derived every worked numeric example the document states, to find
   out which of its own constants I could lean on when building questions:
   - §7.4 layer-record example: segment CRC over four sentinel entries =
     `0x80A34955` ✔; `crc_of_crc_array` = `0xC4EE982E` ✔; inline payload
     81 bytes ✔; index extent length 84 ✔.
   - §15.4 all-sentinel full-segment constant `0xEECB3BB2` ✔ (computed
     over 65,536 × 20 bytes).
   - Appendix A trailer CRC `0xE00938D2` over trailer bytes [0,60) ✔.
   - §11.2, §11.4, §14.2, §14.3, §14.5, §15.4, §17.3, §20.3 worked
     examples all re-derived and consistent.
4. Re-derived §21.8's register arithmetic from §21.1's instance rules:
   §21.2 = 58, §21.3 = 116, §21.4 = 55, §21.5 = 44 → 273 instances over
   36+49+26+10 = 121 conditions. Matches §21.8 exactly. I had planned a
   question on this and dropped it (see "rejected", below) once it proved
   consistent and mechanical.
5. Built the slate by actually constructing files/commits and recording
   every point where I had to decide something the text left me to
   resolve. Those decision points became the findings.

## The slate, and why each earns its place

**Q01 — directory-region CRC of a one-record directory.** Concrete bytes
at a concrete offset. Requires §7.2's 24-byte header layout, §7.3's
registry-fixed flag values for type 0x0002 (a writer MUST emit MU=0/PE=1,
so `flags` is not free), §18.2's one-byte inline payload, and §4.5's CRC.
An implementation that guesses the flags word or the field order emits a
different directory.

**Q02 — layer-record `inline_length`.** Pure packing arithmetic over
§7.4's table, but it cannot be answered without §12.1's element sizes and
`[R-CNT-23]`'s rule that a fill field's length equals the type's element
size. Mixed-width channels (float64 + int16) make the two-channel term
asymmetric, so an implementer who assumes uniform channel entries is
wrong. Wrong answer ⇒ an unparseable record.

**Q03 — packed boolean plane of an edge tile.** Byte-producing.
Simultaneously exercises §11.2's ceiling division, §11.3's padding
positions, §14.3's LSB-first packing with §4.4's bit numbering, and
§14.5's rule that every padding position carries the fill bit. Two of the
sixteen bit positions are real, thirteen are padding; getting §14.5 wrong
flips thirteen bits.

**Q04 — compaction of a structurally-rejected index entry.** Combines
§11.2/§11.4 (planar disk ordinal `c·N + s`), §15.1 (20 bytes per entry, at
region byte 20·k), §15.3 (a `length = 0` non-sentinel entry is
*structural*: reject-tile), and §20.5's newly-worded rule that such an
entry is "reproduced with its offset and length exactly as they stand"
and does not oblige the compactor to refuse. Two implementations could
plausibly diverge on whether the compactor refuses, sentinelises the
entry, or copies it — and the output bytes differ in all three.

**Q05 — verifier verdict with two metadata-encoding anomalies.** One
experimental-range encoding byte (0x85) and one reserved-range one (0x05).
§21.6 makes the first a defined non-violation; §21.5's preamble and R1
make the second a violation with outcome ignore-record. §2.3's priority
rule then fixes the verdict. This is the exact distinction §21.5's
preamble was written to draw, and an implementer who folds "unassigned"
into one bucket certifies a nonconforming file.

**Q06 — verifier verdict on a resource decline.** Requires §17.2's
statement that a window wider than §21.9's 8 MiB guarantee is *conforming*
and merely licenses a decline, §21.9/`[R-ERR-04]`'s minimum-guarantee
semantics, and §2.3's enumeration of the cannot-establish grounds. The
trap is reporting *nonconforming* (the file is clean) or *conforming*
(§2.3 forbids certifying).

**Q07 — updater retain-vs-drop, two scopes at once.** §20.4's MU=0/PE=0
row licenses a drop only on an independent change to the scope the record
attaches to, and that scope differs between a layer sub-record and a
top-level record. A commit that adds a layer changes the file's layer set
but touches nothing about layer `a`. Answering with one word for both
records is the failure mode. Directory bytes differ.

**Q08 — §20.3's tense.** A commit that unstores every tile of a layer
*and* re-declares it. The permission ("a layer that stores no tile … MAY
be re-declared freely") and the bar are quantified over different
generations, and §20.3 states which one wins. Answering "permitted" lets
an appender emit a file this specification bars.

**Q09 — front-block residency over a 200 response.** §6.1's test is
residency, not transport; §6.4 requires deliberate handling of a 200; a
suffix window larger than the file reaches offset 0. Three sections, one
verdict.

**Q10 — index extent_length.** Ceiling division in three dimensions (one
of which has `E < T`), the planar addressed-tile count `C·N`, and
`[R-CNT-17]`'s `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`. A writer that
omits the segment-CRC-array term writes a slot the reader rejects.

**Q11 — lz4 decoded-size cap on a mixed planar layer.** `[R-COD-07]`'s cap
is quantified over addressed tiles and, in a planar layer, "the largest
governs" — and a packed bool plane is ⌈P/8⌉ while a float64 plane is 8P.
Also asks for the register's Detected tier, which §19.3 places at layer
access. An implementer who measures the bool plane, or who defers the
check to tile use, diverges on accept/reject.

**Q12 — slab run continuity with a crc-failing entry.** §16.2 makes
sentinels and *structurally* reject-tile entries transparent to run
continuity but explicitly makes an entry whose only defect is a failed
stored-bytes crc **not** transparent. I constructed the run so that the
two readings give opposite verdicts: read correctly the run is packed and
its first stored tile is 512-aligned; read wrongly the first stored tile
is at 2078 and A_slab fails. The answer forks on exactly that clause.

**Q13 — Appendix G total emission order.** Item 3 pins per-layer ordering
by ascending layer-name bytes, then all remaining record extents after
every layer's tiles and index region, top-level records before layer
sub-records, then the directory. Labels deliberately shuffled so the
answer is not alphabetical.

**Q14 — reject-layer is prospective.** §15.4/`[R-IDX-04]` fixes the
outcome; §19.4 step 8 and §2.4's reject-layer row fix whether already
returned values stand. Two sections, and the wrong answer makes a reader
retract data this specification says it may keep.

**Q15 — committed file length and directory slot after one commit.**
Builds on Appendix A's file plus §7.4's example layer, `[R-CNT-17]`'s
index length, §7.2's header size, §7.1's terminal CRC, and `[R-LIF-02]`
step 5's 64-byte pad. Emits two u64 fields at a fixed trailer offset.

## Coverage check against the charter

- Concrete bytes at concrete offsets: Q01, Q03, Q04(b), Q15(b) — four.
- Reader/verifier verdicts on a specific malformed file: Q05, Q06, Q11,
  Q12 (and Q08, Q14) — four to six.
- Arithmetic (sizes, counts, alignment, coverage): Q02, Q04(a), Q10,
  Q15(a) — four.
- Rules spread across more than one section: Q07 (§20.3+§20.4),
  Q09 (§6.1+§6.4+§19.1), Q14 (§2.4+§15.4+§19.4), Q11 (§17.2+§19.3+§21.3),
  Q13 (App. G + §5.2) — five.
- Changed-section weighting: §2.4 (Q14), §6.1 (Q09), §11.1 (Q10 geometry
  floor / zero-ish extents), §19.3 (Q11 tier), §20.3 (Q08, Q07), §20.4
  (Q07), §20.5 (Q04), §21.4 (Q12, Q04), §21.5 (Q05), Appendix G (Q13).
  §21.7 is not directly quizzed — it is an account of what has *no*
  witness, so a determinate byte-level question off it is hard to state
  without asking the answerer to prove a negative.

No two questions fail together for one reason: only Q01 and (indirectly)
Q15 touch CRC computation, and Q15's asked fields are not checksums.

## Questions I built and rejected

- **Register instance count.** "How many instances do §21.4's 26 rows
  carry?" (answer is a specific integer). Dropped: once I verified
  58+116+55+44 = 273 matches §21.8, the question degenerates into counting
  semicolons, and a miscount by either the answerer or the key would be a
  divergence about arithmetic stamina rather than about the document.
- **`[R-IDX-05]`'s all-sentinel constant.** Asking for `0xEECB3BB2` is a
  table lookup; asking the answerer to *compute* it costs 1.3 MB of CRC
  and proves nothing about reading.
- **Front-block check on a foreign major.** §21.2's preamble reasoning
  about which rows reach a file declaring major ≠ 1 is interesting, but a
  file 64 bytes long with a trailer magic at offset 0 puts `[R-CNT-04]`,
  `[R-CNT-27]` and §6.2's validation order into a three-way ordering I
  could not settle from the text with confidence — so it is not a fair
  question. (Noted; not filed as a finding, because I could not construct
  a case where the outcome differs: every ordering lands on reject-file.)
- **`tarn.stats` staleness.** Advisory throughout; no determinate byte or
  verdict.
- **§21.7 "what no check detects".** Every candidate resolves to "no
  verdict changes", which is exactly what makes it unquizzable.

## Findings recorded while authoring

See the structured result: `quiz-01` … `quiz-05`. None of the five is
byte-level on my own analysis, and I say so in each — the two quantifier
mismatches I found (§11.1's rationale, §20.4's licensing list) are each
decided against the loose text by an explicit clause elsewhere, which is
the same shape as the register-row-versus-rule pattern §21.1 already
resolves. I flag them anyway because both sit in changed sections and both
misstate, in prose, the very rule the surrounding repair was aimed at.

No answers are recorded anywhere in this file.
