# Round 19 — quiz author transcript

**No answers appear in this file.** It records the slate, how it was chosen,
what was rejected, and the checks run while authoring.

## Disclosure

Read: `spec/tarn.md` only, in full (4,364 lines), in four Read calls.
Ran: `wc`, `grep`, `sed`, `awk` against that one file; and Python that
implemented CRC-32C from the parameters in §4.5 and did arithmetic. The
Python scripts I wrote myself into the scratchpad and read back; they read
no project file. No ADR, no `docs/`, no `conformance/`, no `registry.json`,
no git history, no web. Did not read or list the round-19 output directory.

## Instrument checks run before authoring

Before trusting my own arithmetic I reproduced, from the document alone,
every constant the document states, so that a divergence between the
answerer and the key cannot be blamed on my CRC:

- §4.5 check vector: CRC-32C("123456789") and CRC-32C of zero bytes — both
  reproduced.
- §7.4's worked layer record: the segment CRC over its 80 sentinel bytes and
  the crc_of_crc_array over that 4-byte array — both reproduced.
- §15.4's all-sentinel full-segment constant — reproduced.
- Appendix A's trailer CRC over trailer bytes [0, 60) — reproduced.
- §11.2, §11.4, §14.2, §14.3, §14.5, §15.4, §16.2, §17.3, §20.3 worked
  examples: every number checked by hand. All consistent.
- §21.8's "121 conditions over 273 instances": counted mechanically off the
  register tables (rows: F 36, L 49, T 26, R 10; instances: 58 / 116 / 55 /
  44). Both totals hold. This was a candidate finding and is not one.

The point of that pass was to make sure that when a question has one answer,
the document is what determines it.

## How the slate was chosen

The charter asked for questions that (a) have one determinate answer, (b)
need two or more places in the document, (c) fork bytes or verdicts when got
wrong, and (d) are short to compare. I built candidates by actually
constructing files — a minimal one, the §7.4 example carried through to a
committed trailer, a packed-bool edge tile, a planar three-channel read —
and then turned each place I had to look something up twice into a question.

Weighting: five of fifteen sit on the four sections named as newest (§20.5
×2, §23.1, Appendix G, §21.7). The other ten are spread over the container,
the array model, the reader path and the register, because the brief's own
history says the survivors keep turning up in text nobody edited.

Case conventions are written into each question text (lowercase hex,
space-separated, stored order) so a case or separator difference cannot
masquerade as a divergence. Every answer is an integer, a hex byte string, a
verdict word, an outcome-class name, or a register row label.

### Slate (subject → what it forces the answerer to combine)

1. Compacted trailer's flags bytes and version_minor floor — §20.5's
   carry-forward MUST against §6.3's flags = 0 MUST, plus §6.2's field
   widths and the conditional the SHOULD hangs on.
2. Three compaction inputs, refuse or compact — §20.5's regeneration
   paragraph, §15.3's structural rows, §20.4's MU/PE table, §21.6.
3. A file with a 108-byte pre-trailer gap — §6.2, §2.3's conduct-rule
   carve-out, §5.2/§9.7's slack total.
4. crc_of_crc_array for a three-entry all-sentinel index — §11.2 grid,
   §15.4 segmentation, §15.2 sentinel bytes, §4.5. Baited with §15.4's
   full-segment constant, which does not apply to a partial segment.
5. The 20 bytes of a packed planar bool edge tile's index entry — §11.2,
   §11.4, §14.3, §14.5, §13.2, §17.2 codec 1, §15.1.
6. A layer record's inline_length and its index extent_length — §7.4's
   field table, §12.1 element sizes, §7.2 sub-record framing, §11.2,
   [R-CNT-17].
7. Three verifier verdicts on user-metadata encodings — §18.2, §21.5 R1,
   §21.6, §2.3's verdict priority, §21.9's guarantee.
8. Planar geometry: entry_count, extent_length, segment index — §11.2,
   §11.4's disk ordinal, §7.4's formula, §15.4.
9. A planar three-channel read across a stored, a sentinel and a
   structurally malformed entry — §15.3, §13.3, §19.4 step 8, [R-CNF-09].
10. A zstd frame whose window exceeds a 30-byte tile — §14.2 arithmetic,
    §17.2's window rule and its note, §21.4.
11. An interleaved edge tile's decoded size and five padding bytes —
    §14.2, §14.5, §13.1, §4.1.
12. Building the §7.4 example file to a trailer — §7.4, §7.2, §7.1, §9.2
    step 5, §6.2, §5.1.
13. A shrink that de-addresses whole tiles, and what may be called erasure —
    §20.3 step 4, §11.2, §23.1.
14. Appendix G item 2 applied to Appendix A's file — the hash input's
    length and the zeroed window's offsets within it.
15. §21.7's witness for a codec 3 → codec 1 declaration change.

## Rejected candidates, and why

- **"How many instances does §21.4 enumerate?"** — determinate (55), but a
  divergence would come from miscounting semicolons, not from misreading the
  document. Noise, not signal.
- **file_id = 0xFFFF_FFFF_FFFF_FFFF with generation = 2⁶³ − 1** — a clean
  question (is the file conforming; may an appender commit) resting on
  §4.2's "offset, length, extent, and count" not reaching file_id. Cut only
  for room; it would have been the sixteenth.
- **"May a compactor re-encode a stored tile's payload?"** — I wanted this
  as a question and could not use it: the document does not determine the
  answer. It is finding quiz-01 instead.
- **"May a tool call a dropped ancillary record's extent erasure?"** —
  same reason; finding quiz-02.
- **Anything asking which §21 row a codec 1 → codec 3 change witnesses** —
  §21.7 names a set (T15, T17, T23, T25) without resolving which member
  fires for a given new codec. Reversed the direction so the answer is
  single-valued.
- **Appendix G item 3's total emission order applied to a two-layer file** —
  the ordering key is well defined, but the answer is a paragraph, not a
  token. Failed the checkability test.

## Findings hit while authoring

Four, reported in the structured result: quiz-01 (byte-level — nothing
MUST-level preserves a compactor's stored-tile bytes), quiz-02 (§23.1's
enumeration is wider than the requirement it introduces), quiz-03 (§21.7
accounts for a SHOULD as witnessless when [R-CNF-12] already excludes it),
quiz-04 (§20.5's reserved-range row citation is a partial list).
