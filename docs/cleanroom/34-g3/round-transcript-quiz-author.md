# Cleanroom round 34 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,838 lines), in five `Read` calls covering lines 1–4838 with no gaps. No other
file in the repository was read, listed, or searched. No git history, no web.

Local computation only, in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r34-round/scratch/quiz-author/`:

- `qa_check.py` — a CRC-32C implementation (reflected, poly 0x82F63B78, init/final
  0xFFFFFFFF) checked against §4.5's two check vectors and against Appendix A's
  trailer CRC, plus the layer-record framing and grid arithmetic used below.
- `count_inst.py` — parses §21.2–§21.5's register tables out of the spec text and
  counts rows and semicolon-separated Instances cells.

`count_inst.py` reads the spec file (the one file I am permitted to read) and
nothing else. Both scripts were written by me in that directory and nowhere else.

Context I did not ask for appeared before I began: a project instruction file
pointer and an index of the maintainer's memory notes naming this project. I
disregarded it; nothing in this slate or these findings rests on it. Its
contents are not repeated here. The spec was where the brief said it would be.

## Method

Read the document end to end once, in order, before authoring anything. Then:

1. Rebuilt the document's own worked examples independently to confirm I was
   reading its arithmetic the way it states it: §7.4's 81-byte `sst` layer-record
   payload (4 + 34 leading, 18 dimension, 12 channel, 13 trailing), §11.4's
   spatial and disk ordinals, §14.2's interleaved offsets, §17.3's byte-shuffle
   permutation, and Appendix A's trailer CRC. All reproduced. That gave me a
   calibrated basis for building fresh cases rather than restating the document's.
2. Counted §21.2–§21.5 mechanically: 120 rows (F 35 after F11's strike, L 49,
   T 26, R 10) over 277 instances, which matches §21.8's stated figures exactly.
   No question rests on that count; I ran it to look for a discrepancy and found
   none.
3. Walked the sixteen changed passages hunting for a defect, then built the slate
   so that the newest text carries the most weight while still forcing a reader
   into older sections to answer.

## Where the slate is weighted

Sections touched by at least one question, with the changed surface marked *:

- §2.3* — verifier verdicts (Q07, Q10)
- §4.1, §4.5 — endianness, CRC (Q01, Q04, Q12)
- §5.1*, §5.2* — file anatomy, slack (Q05, Q08)
- §6.2, §6.3 — trailer layout and flag lanes (Q04, Q08, Q15)
- §7.4 — layer-record framing (Q01, Q02, Q03)
- §9.2 — commit protocol (Q08)
- §9.7* — coverage walk (Q05)
- §11.2, §11.4 — grid and ordinals (Q02, Q03, Q09, Q11, Q12)
- §12.1 — element sizes, bfloat16 (Q01, Q02)
- §14.2, §14.3, §14.5 — byte layout, packed planes, padding content (Q11, Q12)
- §15.1, §15.3 — index region and entry validity (Q02, Q05, Q09)
- §17.2, §17.3 — codec 4's cap, byte-shuffle (Q03, Q12)
- §18.2* — metadata encoding and frame constraints (Q06, Q07)
- §19.1*, §19.2 — the open, detection tiers (Q14, Q05)
- §20.3* — the closed list of permitted commit changes (Q13)
- §20.5* — compaction (Q15)
- §21.1*, §21.3*, §21.4, §21.5*, §21.6* — register rows and non-violations
  (Q03, Q05, Q06, Q07, Q10)

Coverage against the charter's floors: concrete bytes at concrete offsets —
Q01, Q04, Q11, Q12 (four, floor three). Reader/verifier verdicts on a specific
malformed file — Q05, Q06, Q07, Q10, Q14 (five, floor two). Arithmetic —
Q02, Q08, Q09 (three, floor two). Rules whose statement is spread across more
than one section — Q03, Q07, Q10, Q13, Q15 (five, floor two).

No two questions fail together. The four byte-producing questions each turn on a
different mechanism (name+type+fill framing; CRC-32C over a fixed 60-byte
window; LSB-first bit packing with fill-valued pad bits; the shuffle
permutation over a sample stride). The five verdict questions turn on five
different rules (§15.3's structural rows, §18.2's R3/R4 split, §21.6's
experimental-vs-reserved line, §21.6's conforming-file-a-reader-refuses case,
§19.1 step 4's uniqueness-before-validity ordering).

## The fifteen

Recorded here as posed, without answers. I hold answers for none of them in this
file by design.

Q01 — channel entry bytes for a bfloat16 channel with fill 1.0.
Q02 — inline_length and index extent_length for a fully specified planar layer record.
Q03 — codec 4 on a layer with a zero extent whose declared plane exceeds the lz4 cap.
Q04 — the trailer CRC over a fully specified 60-byte trailer prefix.
Q05 — classifying a 20-byte index entry with offset 8, and its effect on the coverage walk.
Q06 — routing a zstd content-size mismatch in a user-metadata extent to its register row.
Q07 — verifier verdicts for metadata encoding 0x90 versus 0x40.
Q08 — the committed_file_length a minimal second commit must carry.
Q09 — planar disk ordinal and its entry's byte offset in the index region.
Q10 — reader outcome, verifier verdict, and file conformance for an experimental MU = 1 top-level record.
Q11 — the decoded tile image of a packed planar bool tile with padding positions and pad bits.
Q12 — the decoded image and the stored bytes of an interleaved tile under filter 2.
Q13 — which of four single-commit changes §20.3 step 4 permits on a layer that stored a tile.
Q14 — outcome and detection tier for two layer records with byte-identical but invalid names.
Q15 — which index region a compactor regenerates, and the output trailer's flags value.

## What I rejected, and why

- **"How many instances does §21.8 count?"** — mechanically checkable, and I did
  check it, but answering is transcription of table cells rather than applying a
  rule. Lazy by the charter's own test.
- **An index entry with offset = all-ones and length = 5.** I built this first as
  a §15.3 classification case and abandoned it: §15.2 makes such an entry
  non-sentinel, so I expected both the "exactly one of offset and length is the
  sentinel" row (T7) and the "offset or length exceeds 2⁶³ − 1" row (T11) to
  match, leaving the row label indeterminate without §21.1's specialization
  arithmetic. Re-reading T11's Condition cell closed it — "the value being
  distinct from the all-ones sentinel" excludes the case explicitly — so the
  question would have had a determinate answer after all, but only via a clause
  a reader must notice. I replaced it with the offset = 8 case (Q05), which hits
  exactly one row on its face. Reported as an OBSERVATION rather than dropped
  silently.
- **"Is a switch from alignment to slab in one commit permitted?"** as a
  standalone yes/no. Kept, but folded into Q13's four-way subset so that a single
  reading of one clause cannot carry the whole question.
- **A question turning on `[R-CNT-26]`'s version_minor floor.** `[R-CNF-12]` puts
  SHOULD deviation outside the register, so no verdict a question could ask for
  is determinate at the level this slate wants.
- **A question about the pre-trailer pad's content.** `[R-CNT-03]` is advisory and
  `[R-CNT-21]` makes slack content unconstrained, so there is no single answer.
- **"What does a verifier report for a file whose walk stopped at L18?"** — I built
  this against §5.2's new sentences on discarded claimants and it is determinate,
  but its answer is prose ("a partial total, naming the scope that stopped the
  walk"), not the short unambiguous token the charter asks for. Its content
  survives as Q05's yes/no half instead.

## Findings raised while authoring

Three, all recorded in the structured result: an ambiguity in the fourth verb of
§20.3 step 4's permitted-change list (`quiz-01`), an observation on the cost of
deciding which §21.4 row records an index entry that trips two structural rows
(`quiz-02`), and an observation that §21.1's own load-bearing rules carry no
requirement identifier for a vector to cite (`quiz-03`). None is byte-level, and
the reasoning for each is in its `byte_level_rationale`.
