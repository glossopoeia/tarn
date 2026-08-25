# Round 24 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,445 lines, in five `Read` calls). No other file in the repository was
opened, listed, grepped, or fetched. No git history, no web.

Local computation only, over data I typed into scratch scripts myself:

- `round24/calc.py` — a CRC-32C implementation (Castagnoli, reflected,
  init/final 0xFFFFFFFF) plus the arithmetic for the byte-level items.
- `round24/count.py` — this one *does* read the spec file (the single
  permitted file) to extract the Instances column of §21.2–§21.5 and sum it.

CRC implementation was validated against four constants the document itself
states before I used it for anything: CRC-32C("123456789") = 0xE3069283 (§4.5),
CRC-32C of zero bytes = 0x00000000 (§4.5), the full all-sentinel segment
constant 0xEECB3BB2 (§15.4), and §7.4's worked example (segment CRC 0x80A34955
over four sentinel entries, crc_of_crc_array 0xC4EE982E), plus Appendix A's
trailer CRC 0xE00938D2. All five reproduced exactly. That is the ground my
byte answers stand on.

Context I did not ask for appeared before I began: a project instruction file
and an index of the maintainer's memory notes naming prior rounds and a working
cadence. I did not open any file it named and did not use its contents to pick
or settle anything. Disclosed in the structured result.

## How I read the document

One cold pass front to back, then targeted re-reads of §20.5, §21.2, §21.5,
§21.7 (the four passages the brief flags as newest), then §18.2, §16.2, §15.3,
§14.3/§14.5, §17.2/§17.3, §20.3 step 4, §21.9.

Two mechanical audits, because the brief warned that recent attention is not
correctness:

1. **Row counts.** §21.2 says 36 conditions (F1–F36 ✓), §21.3 says 49
   (L1–L49 ✓), §21.4 says 26 (T1–T26 ✓), §21.5 says 10 (R1–R10 ✓);
   §21.8 says 121 conditions ✓.
2. **Instance counts.** §21.1 makes the count mechanical: semicolon-separated
   items within a cell, a `—` cell being one instance. Extracted column 3 of
   every row and summed: F 58, L 116, T 55, R 48 → **277**, exactly the figure
   §21.8 states. No arithmetic defect there. I had drafted a quiz question on
   this and dropped it once it checked out — a question whose only content is
   "add up a column" earns its place only if the column is wrong.

## The slate, and why each item is on it

Coverage targets from the charter, and where they land:

- concrete bytes at concrete offsets: Q01, Q02, Q03, Q04, Q05
- reader/verifier verdicts on a specific malformed file: Q06, Q07, Q08, Q09, Q14
- arithmetic (sizes, counts, alignment, coverage): Q10, Q11, Q12, Q13
- rules spread across more than one section: Q02, Q03, Q04, Q09, Q11, Q12, Q13,
  Q14, Q15
- weighted to the four newest passages: Q05 and Q08 (§20.5), Q06 (§21.2),
  Q07 and Q09 (§21.5 + §21.6/§18.2), Q15 (§21.7 + §20.3), Q13 (§21.9's
  per-instance paragraph)

Item by item:

- **Q01 — trailer CRC.** The test is assembling §6.2's 60 bytes in the right
  order and widths, not the CRC itself. Appendix A gives the generation-1
  answer, so I moved every field off Appendix A's values.
- **Q02 — crc_of_crc_array over a three-entry all-sentinel index.** Forces the
  §15.1 region layout, §15.2's sentinel bytes, §15.4's *partial* segment rule
  ("the final partial segment's CRC covers only its actual bytes" — the
  0xEECB3BB2 constant must NOT be used), and §7.4's field. Four sections, one
  4-byte answer.
- **Q03 — byte-shuffle at interleaved stride.** §17.3's stride rule is stated
  per-layout and the interleaved case (s = Q, not the element size) is the one
  an implementer gets wrong. Codec 1 makes the filtered image the stored bytes,
  so the answer is bytes on disk.
- **Q04 — packed bool plane with padding positions and pad bits.** §14.3's
  LSB-first packing, §14.5's two distinct obligations (padding positions carry
  the fill *bit*; pad bits carry it too), §11.3's padding-position definition,
  §4.4's bit numbering. The §14.3 example is `55 01`/`55 FD`; mine is a
  different geometry so the example cannot be copied.
- **Q05 — a compacted file's trailer.** §20.5 against §6.3: ignore-lane bits
  carried forward rather than zeroed, generation 1, version_minor floor at the
  input's. Answer is 4 bytes plus two integers.
- **Q06 — foreign major with a bad trailer CRC.** §21.2's opening paragraph is
  new text and says explicitly that F14 is one of four rows that *do* reach a
  file declaring another major, because §6.2 puts the trailer CRC before the
  version gate. The trap is §2.3's "neither conforming nor nonconforming",
  which pulls toward *cannot establish*; §2.3's own "an established violation
  takes priority" decides it.
- **Q07 — experimental metadata encoding.** §21.5's exception clause, §21.6's
  row, and [R-MTA-10]. The trap is treating an encoding the reader cannot
  decode as a cannot-establish ground; §18.2 and §2.3 both say it is not.
- **Q08 — compactor meets a structurally invalid index entry.** §20.5's newest
  paragraph. Enumerated answer choices so a phrasing difference cannot look
  like a divergence.
- **Q09 — Frame_Content_Size mismatch on a metadata document.** §18.2 routes
  this to R4 and not R3 in so many words ("A mismatch is one of the frame
  constraints R4 registers, not a failure to decode under R3"), and R4's own
  Instances cell enumerates both directions. Pure R3-vs-R4 discrimination.
- **Q10 — entry_count and extent_length.** §11.2's ceiling division, the
  planar C·N addressed count, [R-CNT-17]'s formula with its ⌈n/2¹⁶⌉ term. C
  chosen so the segment term is 2, not 1.
- **Q11 — disk ordinal, region offset, segment, in-tile ordinal.** [R-GEO-06]'s
  four definitions applied at once, then §15.1's 20·k and §15.4's segment
  partition. Channel index chosen so the entry falls in segment 1.
- **Q12 — slab packing across a structurally invalid entry.** §16.2's packing
  relation plus §15.3's transparency rule for entries classified reject-tile on
  a *structural* ground (as against one failing only its stored bytes' crc,
  which is not transparent). Answer is one offset.
- **Q13 — a legal degenerate file.** Zero-extent dimension, tile extent 2³⁰,
  codec 4, decoded size 2³² — far past `[R-COD-07]`'s 0x7E000000 cap, and
  nonetheless conforming because the cap is quantified over *addressed* tiles
  and this layer addresses none. §17.2's Note and §20.3 step 4 both say so;
  §21.9's per-instance paragraph says the same for the 256 MiB row. This is the
  "file nobody would write on purpose" item.
- **Q14 — zstd Window_Descriptor on an 18-byte tile.** §17.2's Note explains
  that a sub-1-KiB tile is encodable only as a single-segment frame; clearing
  the flag therefore forces a declared window above the decoded size, which is
  T21. Needs §14.2's arithmetic to know the decoded size is 18.
- **Q15 — shrink that damages a prior-generation tile, then unstores it.**
  §20.3 step 4's quantifier is the *superseded* generation's, so the commit is
  barred; §21.7 says that is precisely where the bar has no witness. Two short
  answers, and the second is "none", which a reader trusting the register to be
  exhaustive over MUSTs will get wrong.

## Rejected candidates, and why

- **"Sum §21.5's Instances column."** Determinate, but it checked out at 48
  (and 277 overall), so the question only measures patience.
- **"Which register row does a stored tile overlapping the directory
  exhibit?"** F33 versus L18 is a genuine distinction but the answer is
  readable off one cell of one table; it fails the two-places test.
- **"A commit changes a layer's filter from 1 to 2 on an interleaved
  single-uint8-channel layer — barred or permitted?"** (Permitted: Q = 1 makes
  the mandated shuffle the identity, which §20.3 expressly carves out.) Strong
  question, cut only for space; it overlaps Q15's section pair.
- **"Front-block mismatch: which of a mapped reader, a two-request remote
  reader, and a verifier must detect it?"** Cut for space; §21.2's F6 cell and
  Appendix H settle it, and Q06 already exercises §21.2's new paragraph.
- **"Trailer CRC on a foreign-major file with a bad dir_offset → cannot
  establish."** Cut deliberately: it would have failed together with Q06 for
  the same reason (§6.2's validation order), which the charter forbids.
- **Anything turning on a SHOULD alone.** [R-CNF-12] puts SHOULD deviation
  outside the register, so no verdict question can rest on one. Q05's third
  part asks what §20.5 says the output SHOULD carry, which is a question about
  the text and not about the emittable set.

## Findings raised while authoring

Four, all reported in the structured result: §20.5's regeneration trigger
naming the wrong predicate (AMBIGUITY), §21.7 omitting [R-LIF-02] from its
account of unwitnessed obligations (OBSERVATION), §21.2's use of "geometry"
for the file's own byte layout (AMBIGUITY), and §21.7's treatment of
[R-GEO-06] covering only the tile-image half of that rule (OBSERVATION).
None graded byte-level; the rationale for each is in the finding.

No answers are recorded in this transcript or in the question text.
