# Round 9 — quiz author transcript

**No answers appear anywhere in this file.** Where I say "verified", I mean I ran
the arithmetic or the CRC locally and satisfied myself the document determines a
single value; the value is not recorded here.

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–3893 (the whole document). Ran two `grep`
invocations against that same file (`informative`). Ran two `python3` heredocs
that read no files at all — a from-scratch CRC-32C (Castagnoli, reflected,
init/final 0xFFFFFFFF) plus struct packing, used to (a) reproduce the document's
own check vector for `"123456789"` and for zero bytes, (b) reproduce Appendix A's
trailer CRC from the trailer layout, (c) confirm §15.4's all-sentinel full-segment
constant against 2^16 synthesized sentinel entries, and (d) confirm that each
candidate question that asks for a CRC has exactly one answer. No ADRs, no
`docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`/`AGENTS.md`, no git
history, no network.

Prior-knowledge policy: I used background knowledge of DEFLATE/zstd/LZ4/JSON only
to *generate* suspicions. Every question's answer is settled from this document's
text; where a question touches RFC 8878 behaviour (the Window_Descriptor floor),
the document states the fact itself in §17.2's note, so an answerer needs no
external reference.

## How I read the document

One full pass front to back, then targeted re-reads of the weighted list:
Appendix G, §21.2, Appendix H, §21.9, §21.6, §2.3, §4.7, §21.1, §9.7, §20.3, then
§2.4, §21.7, §4.6, §9.2, §15.3, §20.4, §21.3, §21.4.

Two independent checks I ran to see whether the register is internally sound
before drawing questions from it:

1. **Row counts.** §21.2 claims 38 conditions (F1–F38), §21.3 claims 50 (L1–L50),
   §21.4 claims 27 (T1–T27), §21.5 claims 10 (R1–R10); §21.8 claims 125 rows. The
   rows are all present and the sum matches.
2. **Instance counts.** §21.1 fixes the counting rule: semicolon-separated within
   a cell, a cell reading `—` is one instance, and the fields of a *single
   predicate* are not instances. I counted every cell in §21.2–§21.5 by hand under
   that rule and the total matches §21.8's stated figure exactly. I had expected
   this to be the round's cheap defect and it is not one; the arithmetic is clean.
   The only friction is *how* several cells name their instances — see finding
   quiz-03.

## The slate, and why each question earns its place

Composition targets from the charter: ≥3 concrete-byte questions (I have 7), ≥2
reader/verifier verdicts on a specific malformed file (5), ≥2 arithmetic (4), ≥2
rules stated across more than one section (nearly all). No two questions fail for
the same reason — I checked each pair for a shared single point of failure and
split the two "unassigned record type range" questions into one merged item
(Q11) rather than two that a single misreading of the MU rule would sink together.

- **Q01 — trailer bytes of a 128-byte file.** §6.2's layout + §4.5's CRC
  parameters + §5.1's minimum. Pinned every trailer field in the question so the
  only work is the layout and the checksum; a wrong polynomial, a wrong
  reflection, or big-endian storage all show up as different bytes on disk.
  Appendix A gives a worked instance with a different `file_id`, so the question
  is a recomputation, not a lookup.
- **Q02 — packed planar bool edge tile.** Four sections have to agree: §11.2's
  grid counts, §11.3's padding positions, §11.4's row-major in-tile ordinal,
  §14.3's LSB-first packing and ⌈P/8⌉ size, §14.5's rule that padding positions
  and pad bits both carry the channel's fill bit. The tile is deliberately an
  *edge* tile with P not a multiple of 8, so both the padding-position and the
  pad-bit halves of §14.5 are live at once. §14.3's own example has neither
  padding positions nor the same P, so it cannot be copied.
- **Q03 — byte-shuffle stride.** The entire question is whether the shuffle stride
  for an interleaved tile is the sample stride Q (§14.2) or a channel's element
  size; §17.3 states the rule and §14.2 supplies Q. A wrong stride is exactly the
  §21.7 case that produces a file every checksum certifies and whose samples are
  wrong. I chose the given decoded image so that the bool channel's bytes are
  legal 0x00/0x01, to keep §14.2's conformance question out of the way.
- **Q04 — user-metadata record header bytes.** §7.2's header layout, §7.3's *fixed*
  flags for a registered type (the trap: writing flags = 0), §18.2's one-byte
  inline payload, §4.1's byte order. Every byte is determined.
- **Q05 — index region length and crc_of_crc_array for an all-sentinel layer.**
  Combines §7.4's `[R-CNT-17]` length formula, §15.4's segment partition, §15.2's
  sentinel bytes, §15.4's all-sentinel constant, and §4.5's little-endian storage
  of a CRC. Chose entry_count so that both segments are *full* — §15.4 permits the
  constant only for full segments and requires a partial segment's CRC to be
  computed, so a reader who misses that distinction still gets this one right and
  the question stays about the chain, not about a trap I did not want here.
- **Q06 — compactor's output trailer, bytes [8, 16).** §6.2's field positions,
  §6.3's ignore-lane rule and `[R-CNT-26]`'s minor-version floor, §20.5's rule that
  a compactor carries unknown ignore-lane bits forward and takes the greater of the
  floor and the input's minor. Three plausible wrong answers (flags = 0, minor = 0,
  byte order) each change bytes on disk.
- **Q07 — Appendix G, the entry for an all-fill tile.** Appendix G item 7 (all-zero
  fill default) feeds item 6 (sentinel for every all-fill tile), which resolves
  through §15.2 to a fixed 20 bytes. Two profile items plus a constant — the
  cheapest possible demonstration that the profile's items interlock, and the exact
  place Appendix G says they do ("two writers that default fill differently
  disagree about which tiles exist").
- **Q08 — planar index arithmetic, plus one register row.** §11.2 grid counts,
  §11.4's channel-major disk ordinal c·N + s, §15.1's 20·k placement, §7.4's
  length formula, and finally §21.3's L-row for a length mismatch. Numbers chosen
  so they do not coincide with §15.4's or §11.4's worked examples.
- **Q09 — slack total, partiality, and verdict for a damaged file.** The heart of
  §9.7's newest text: an entry §15.3 classifies reject-tile on a *structural*
  ground contributes no extent to the coverage walk and does not make the walk
  incomplete, while an entry whose only defect is a failed stored-bytes CRC keeps
  its extent in the walk. Add §5.2's definition of slack, §2.3's rule that an
  established violation beats *cannot establish*, and one integer plus two words
  settles all of it. This is the question I expect to separate readers who
  implemented §9.7 from readers who skimmed it.
- **Q10 — committed_file_length after an append.** §20.3's rule that a layer whose
  stored-tile set changes has its *whole* index region re-emitted, §7.4's length
  formula, §7.1's 4-byte directory CRC, §9.2 step 5's pad to the next 64-byte
  boundary, §6.2's 64-byte trailer and F mod 64 = 0. Five places, one integer.
- **Q11 — reserved vs experimental record type, MU = 1.** Six short answers plus a
  row identifier. Tests: `[R-CNT-15]`'s MU gate; §21.6's two "conforming files a
  reader nevertheless refuses"; `[R-CNF-02]`'s conduct-versus-bytes line; §2.3's
  *cannot establish* and its priority rule; and §21.1's specialization rule (which
  of two rows a file is recorded against). Merged from two candidate questions
  precisely so that the reserved and experimental halves cross-check each other
  inside one item.
- **Q12 — duplicate, ill-formed layer names.** §19.1 step 4 decides uniqueness
  first and over raw bytes whether or not either name is well-formed; §4.6 makes
  comparison a byte comparison; `[R-ENC-15]` puts a duplicate layer name at file
  scope while an ill-formed name is layer scope. Asks for the outcome, the §19.2
  tier, and the register row.
- **Q13 — hard limits versus minimum guarantees.** §21.9 states both lists in one
  section and they are easy to conflate: 32 and 4096 are floors a reader must
  accept, 255 and 65,535 are hard limits from field widths (`[R-ERR-05]`,
  Appendix B). Getting this backwards makes a reader reject a conforming file, or
  makes a writer emit an invalid one.
- **Q14 — codec 3 window on a small tile.** `[R-COD-06]` forbids a declared window
  larger than the decoded size and requires Frame_Content_Size, when present, to
  equal it; §17.2's note supplies the Window_Descriptor floor that makes the
  answer forced. Yields a yes/no, an outcome class, a T-row, and an integer.
- **Q15 — the one byte a conforming file cannot carry.** `[R-SER-08]`'s
  reader-side rule (report 0x00 as false and every other byte as true), its
  detector assignment to the verifier, Appendix H's reader checklist restating it,
  and §21.4's row split between real and padding positions (T2 vs T4). This is the
  clearest case in the document of a rule whose statement is spread across §14.2,
  §21.4 and Appendix H, and where a reader that "helpfully" rejects instead is
  still conforming while one that returns `false` is not.

## Candidates I rejected, and why

- **"How many instances does §21.3 enumerate?"** Mechanically determinate, and I
  verified the total. Rejected: fifty rows of semicolon counting is an arithmetic
  slip generator, and a divergence between answerer and key would indict nobody's
  reading of the document. A quiz item should fail for a reason.
- **A bfloat16 channel-entry byte question.** Determinate (§12.1's binary32
  identification, §7.4's channel entry, fill length = element size). Rejected as
  too close to §12.3's worked example, which gives the same shape verbatim for
  float32; and §12 is not in the weighted set.
- **"Which fields does this specification classify as informative?"** The honest
  answer is a count, and the count is a finding rather than a question — see
  quiz-02. Asking it would have made the answerer and the key argue about a gap
  in the document instead of about the document.
- **Appendix G item 2's `file_id`.** "A cryptographic hash of the file's own
  emitted bytes" names no hash function and no truncation rule, so no byte value
  is determined. Not a question; not reported as a finding either, since Appendix G
  is non-normative and explicitly says profile conformance is confirmed only by
  reproducing the file.
- **Request-count questions on §6.4.** §6.4's own note says no request count is a
  conformance property. Nothing to fork.
- **"Is a writer that pads more than to the next 64-byte boundary conforming?"**
  I traced this all the way through and it resolves — see quiz-04 — but the
  resolution rides on one clause of `[R-CNF-02]`, and an answerer could reasonably
  land elsewhere for reasons that are about that clause rather than about any
  byte. Reported as an observation instead of asked.
- **A §20.4 drop-permission question (MU = 0 / PE = 0).** Determinate, but the
  answer is a paraphrase of one table cell's prose rather than a byte, a count, or
  a verdict name, and I could not compress it to something unambiguous to compare.

## Determinacy checks I ran before freezing the slate

- Reproduced §4.5's check vector and Appendix A's trailer CRC from the §6.2 layout
  alone; my CRC agrees with the document, so every CRC-bearing question has a
  single answer the document determines.
- Confirmed §15.4's full all-sentinel segment constant by building 2^16 sentinel
  entries from §15.2's 20-byte pattern and checksumming them. It holds. Had it not,
  that would have been a byte-level defect (writers may emit the constant
  uncomputed; readers verify by comparison), so this was worth the minute.
- Checked that each question's scenario is not accidentally under-determined:
  pinned `dir_offset` in Q01 (a 128-byte file does not force it), pinned "no gaps"
  and "no alignment or slab" in Q10, pinned "does not elect to stop at the first
  violation" in Q09, pinned declaration order in Q03 and Q08, and pinned hex case
  and separators in every byte question.
