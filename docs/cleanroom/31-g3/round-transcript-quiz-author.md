# Round 31 — quiz author transcript

## Access and method

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,790 lines), in five contiguous chunks, whole. No `docs/`, no `conformance/`, no
`registry.json`, no git history, no web. No directory listings.

Scratch directory (mine alone):
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/quiz-author/`
One file written there: `qa_crc_checks.py` — a self-contained CRC-32C
implementation (reflected Castagnoli, init/final 0xFFFFFFFF) that reads no
files. I did not read the output directory.

Search discipline: the document is hard-wrapped, so every phrase check was run
by normalising all whitespace to single spaces over the whole file in Python and
substring-matching short fragments, never by line-oriented grep. Every phrase I
relied on was confirmed HIT; no conclusion rests on a zero.

## Calibration pass — the document's own arithmetic

Before authoring I re-derived every checksum constant and every worked numeric
example the document states, so that questions built on the same machinery
would be built on ground I had checked rather than on the document's assurance.

Verified by computation:

- §4.5 check vector: CRC-32C("123456789"), CRC-32C(zero bytes).
- §7.4's layer-record example: the segment CRC over 80 bytes of four sentinel
  entries, and the crc_of_crc_array over that 4-byte array.
- §15.4 / Appendix B: the CRC of a full 2^16-entry all-sentinel segment.
- Appendix A: the trailer CRC of the 128-byte minimal file.

Verified by hand:

- §7.4's 81-byte inline payload, field by field, and its 4+34 / 18 / 12 / 13
  decomposition.
- §11.2, §11.4 and §15.4's ordinal and region-offset examples (s = 10, in-tile
  ordinal 11,452, disk ordinal 74, region bytes [1480, 1500), entries 96–127).
- §15.4's 1,000,000-entry example: 16 segments, 64-byte array, region
  20,000,064 bytes, segment-relative byte 339,180, ranges [19,660,800,
  20,000,000) and [20,000,000, 20,000,064), 1.25 MiB per full segment.
- §14.2's three offset examples, §14.3's packed example (0x55 0x01 / 0x55 0xFD),
  §14.5's 32-byte edge tile, §17.3's shuffle permutation, §20.3's 644-byte index.
- §21.9's note: 2^32 tiles -> 256 KiB CRC array; 2^36 -> 4 MiB.
- §21.8's closed count. I counted §21.2 = 35 rows / 56 instances,
  §21.3 = 49 / 116, §21.4 = 26 / 55, §21.5 = 10 / 50, applying §21.1's own
  counting rules (a "—" cell is one instance; semicolons separate). Totals
  120 conditions / 277 instances, exactly as §21.8 states. No finding.

Everything checked. The document is arithmetically clean in every place I could
test it, which is worth recording because it means a divergence between the
answerer and the key on any of my arithmetic questions is a fact about a reader,
not about the text.

## How the slate was chosen

The brief weights the seventeen changed passages but warns that four of the last
five rounds found their survivor in untouched text. I aimed the slate as
follows.

Aimed at the changed surface (the newest text):

- §6.3 / §20.5 / §2.3 — the ignore-lane origination prohibition, stated in five
  places. Q07 forces the three writer tiers apart on the same field and asks for
  the bytes, so a reader who has collapsed compactor onto creator diverges.
- §20.3 — the widened carve-out and the two bars. Q08 puts four commits to them,
  one per limb: last-channel removal (ordinal bar), middle-channel removal
  (ordinal bar bites), interleaved channel removal (§14 bar bites), and a
  filter change that §17.3 makes the identity (the carve-out's first limb).
  Q04 exercises the commit protocol's floor.
- §18.2 — the rewritten frame rules. Q06 forces the R3/R4 routing decision the
  section states in one sentence and R4's cell restates.
- §9.7 / §5.2 — the partial-total rule and the discard-with-the-layer clause.
  Q10 is arithmetic that is wrong by exactly one layer's claimants if that
  clause is missed.
- §2.3 / §21.2 — [R-CNF-13]'s reach. Q05 is two files that differ only in which
  row they trip, one reaching and one not.
- §17.2 / §21.9 / §11.2 — the lz4 cap's quantifier over addressed tiles and
  §21.9's per-instance individuation. Q15.

Aimed at untouched text, deliberately:

- §7.4 field packing (Q01), §15.1 region layout and §11.4 ordinals (Q02),
  §6.2 trailer layout plus §4.5 (Q03), §14.2 offsets (Q11), §14.3 packing with
  §14.5 pad-bit content (Q12), §14.2's [R-SER-08] return rule (Q13), §19.1
  step 4's uniqueness-first clause (Q14), §20.4's table against §7.3 (Q09).

Coverage against the brief's floor:

- Concrete bytes at concrete offsets: Q01 (header field), Q03 (trailer CRC),
  Q07 (flags field), Q12 (packed plane).
- Reader/verifier verdicts on a specific malformed file: Q05, Q06, Q13, Q14.
- Arithmetic: Q01, Q02, Q04, Q10, Q11.
- Rules spread across more than one section: Q05, Q07, Q08, Q09, Q10, Q15.

Independence: I checked each pair for a shared failure mode. Q02 and Q11 both
compute ordinals, so Q11 was trimmed to the in-tile ordinal (permanent for every
linearization) and the in-sample offset, leaving the spatial/disk ordinal to Q02
alone. Q12 and Q13 both touch bool, so Q12 is planar packing plus pad bits and
Q13 is the interleaved byte's resolution rule; they fail for different reasons.
Q03 carries flags = 0 so that a little-endian slip cannot sink both Q03 and Q07.

## What I wrote and rejected

- **An instance-count question** ("how many instances does §21.4 enumerate?").
  Mechanical and determinate — I counted it — but it moves no bytes and the
  tedium invites arithmetic slips that would masquerade as a divergence about
  the text. Rejected.
- **A question on whether an appender must refuse to commit on an input whose
  violation it has detected.** This is finding quiz-01: the document decides it
  by naming the case, but it uses "relies on" in two incompatible senses to do
  so. Asking it would have produced a divergence that indicts the text rather
  than either answerer, which is a finding's job and not a question's. Rejected
  and filed instead.
- **A question on whether a conforming reader must accept a conforming file
  carrying an experimental MU = 1 *sub-record*.** Same reason — filed as
  quiz-02.
- **A second reach question** (major other than 1, trailer CRC failing). Folded
  into Q05 as its second file rather than asked separately, since two reach
  questions would fail together.
- **A question keyed to Appendix G's single-group identity filter (n = L/s = 1)
  against §20.3's carve-out.** I convinced myself §20.3's "the list names where
  that effect arises rather than standing on its own" makes the general test
  govern, so the answer is determinate — but the reasoning is thin enough that a
  key and an answer could honestly split on it. Rejected as a question; the
  cleaner packed-bool limb, which [R-COD-10] names in terms, is Q08's item (iv).
- **A CRC question over two full all-sentinel segments** (crc_of_crc_array over
  eight bytes). Determinate and computable, but it would have been the second
  CRC question and Q03 already covers the emission skill. Rejected.

## The slate

15 questions, as returned in the structured result. No answers are recorded
here or anywhere else; I computed several of them privately to confirm each
question has one, and none is written down.

Q01 — layer-record inline_length from the §7.4 field table, plus that value as
the u32 at record-header offset 4.
Q02 — planar geometry: entry_count, index-region extent_length, a disk ordinal,
and that entry's byte offset within the region.
Q03 — the four bytes at [F-4, F) of a fully specified 128-byte file.
Q04 — the smallest committed_file_length a commit appending one specified layer
record to the 128-byte minimal file can produce.
Q05 — two files declaring a format major this verifier does not implement; the
verdict for each.
Q06 — a user-metadata frame whose content-size field disagrees with the decoded
document: outcome class, register row, file conformance.
Q07 — trailer flags across compactor, creator and appender, as bytes.
Q08 — four commits against §20.3's two bars: how many are barred.
Q09 — four records against §20.4's table: how many may be dropped.
Q10 — a verifier's slack figure where a layer-scope rejection stops the walk.
Q11 — interleaved decoded size and the byte offset of one channel's value.
Q12 — the two bytes of a packed planar bool plane with padding positions and
pad bits.
Q13 — what a reader returns for a nonconforming interleaved bool byte, and who
detects it.
Q14 — two layer records with byte-identical empty name fields.
Q15 — codec 4 declared on a layer that addresses no tile.

## Findings

Four, all graded byte-level = false, each with the reason it is not. See the
structured result for locations and quotations. Two are recent-edit artifacts in
listed sections (§22.3, §20.4's table); two are cross-section wording mismatches
in text no hunk touched (§20.1/§20.3 step 2 against §20.3's [R-WRT-03], and
§2.3's [R-CNF-03] against §21.6's closing paragraph). None of them forks the
bytes: in each case another sentence in the document settles the behaviour, and
in the first the disputed output file would carry a register-row violation under
either reading, so [R-CNF-05] bars it either way and the emittable set does not
move.
