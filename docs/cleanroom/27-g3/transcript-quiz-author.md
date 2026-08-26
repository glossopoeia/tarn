# Round 27 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines — the brief said 4,550; off by one, noted, no action taken). Read it
in full, in sequence, in eight chunks. Ran `grep -o 'R-[A-Z]\{3\}-[0-9]\+'` against
that file alone to census requirement prefixes, and one small `python3` script over
that same file to count register rows and instance cells. Ran local Python for
CRC-32C, ceiling division, and byte-layout arithmetic; that code reads no project
file. No ADRs, no docs/, no conformance/, no registry.json, no git, no web.
Wrote scratch files under my own scratchpad (`crc.py`, `t2.py`, `t3.py`, `t4.py`)
and this transcript. Did not read or list the output directory.

Context I did not ask for appeared before I began: a project instruction file
pointing at AGENTS.md, and an index of the maintainer's memory files with
one-line descriptions (one of which names §21 and the vector corpus). I did not
open any of it and did not let it steer a question. Disclosed in `disclosure`.

## Calibration work done before authoring

Verified my CRC-32C implementation against three constants the document states
itself, so that any byte-level question I build on it is anchored in the
document rather than in my library:

- CRC-32C("123456789") and CRC-32C(zero bytes) — §4.5's check vector.
- The 4-sentinel segment CRC and its crc_of_crc_array — §7.4's worked example.
- The full all-sentinel segment constant — §15.4 / Appendix B.
- Appendix A's trailer CRC over trailer bytes [0, 60).

All four reproduced. That gives me confidence that a trailer-CRC question and a
crc_of_crc_array question have determinate answers a careful reader can reach.

Also mechanically checked, to make sure I was not building a question on a
miscount:

- §2.2's prefix table against every prefix actually used in the document: 19
  listed, 19 used, identical sets. The list-to-table conversion carries the same
  content. No finding.
- §21.2–§21.5 row counts (36 / 49 / 26 / 10 = 121) and instance-cell counts
  (58 / 116 / 55 / 48 = 277) against §21.8's "121 conditions over 277
  instances". Exact. I had planned a question asking the answerer to derive an
  instance count from §21.1's enumeration rules; I dropped it because it is
  laborious rather than pointed, is not a byte-level question, and a
  transcription slip on either side would produce a divergence that indicts
  nothing.
- §10.2's eight identifier spaces against the sections that own them, and
  against §20.5's "one row for each of the other seven spaces" (L31, L33, L34,
  L36, L43, L45, R1). Consistent.
- §21.2's preamble claim that exactly F8, F14, F6 and both F1 instances reach a
  foreign format major, derived independently from `[R-CNT-24]`'s four fixed
  invariants. Agrees. Q10 is built on the negative side of this (F15 does not
  reach) rather than the positive, because the positive is nearly a lookup.

## The slate, and why each earns its place

Q01 trailer CRC bytes — forces §6.2's field order and widths, §4.1's endianness,
§4.5's parameters, and derivation of flags = 0 (`[R-CNT-08]`) and reserved = 0
from the fact that a creator emitted it. Three sections, one 8-hex-digit answer.

Q02 entry_count and total sample-position count — §11.2's ceiling division, the
planar C·N rule, and ∏Tᵢ. Wrong here means an index region of the wrong length.

Q03 disk ordinal and index-region byte offset — §11.4's row-major spatial
ordinal, §11.4's channel-major c·N + s, §15.1's 20·k. Deliberately a *different*
layer from Q02 so a ceiling-division slip cannot sink both.

Q04 decoded sizes and a value's byte offset — §14.2's two formulas, §14.3's
packing, §12.1's element sizes including bool = 1 for the stride. Three integers.

Q05 byte-shuffle output of an interleaved tile — §14.1's sample-major value
sequence, §14.2's little-endian encoding, §17.3's stride = Q. Twelve concrete
bytes; a reader who takes the stride to be the element size gets a different
file.

Q06 packed boolean plane with padding positions and pad bits — §11.3, §11.4's
in-tile ordinal, §14.3's LSB-first packing, §14.5's fill-encoded padding and pad
bits. Two bytes. This is the question I expect to separate careful readers.

Q07 crc_of_crc_array over a three-entry all-sentinel index — §15.2's sentinel
bytes, §15.4's partial-segment rule (the 0xEECB3BB2 constant is licensed only for
a *full* segment, which is the trap), §4.5's parameters, §8.1's chain.

Q08 lz4 cap after a growth that lifts a layer out of the empty case — §17.2's
`[R-COD-07]`, its Note on the escape, §11.2's addressed-tile count, §20.3 step 4's
growth permission, §19.2/§21.3's tier. Verdict + tier.

Q09 unassigned metadata encoding with a failing extent CRC — `[R-MTA-10]` says
what a verifier still checks under an unassigned encoding, §21.5's R2, §21.6's
carve for the experimental range. Reader outcome + verifier verdict.

Q10 foreign format major with a nonzero trailer reserved field — §2.3's reach
paragraph and its Note on F15, §6.3's `[R-CNT-24]`, §21.2's preamble,
`[R-CNF-11]`'s verdict priority. One verdict word.

Q11 slack total — §5.2's coverage classes and §9.7's walk. The traps are that
the front block and the trailer are claimed rather than slack, that the layer
record itself is inside the directory and not a separate claimant, and that a
sub-record extent is a claimant.

Q12 the MU = 0 / PE = 0 drop rule — §20.4's table read against §20.3 step 4's
statement that superseding a tile re-places the index region and so modifies that
layer's record. Two yes/no answers, one per record, and they must differ.

Q13 layer-record inline_length and the offset of index_encoding — §7.4's field
order and widths, §4.6's prefixes, §12.1's element sizes.

Q14 Appendix G item 3's first-structure offset under a declared alignment —
one integer, and it requires noticing that item 3's order puts stored tiles
first and that `[R-SLB-01]` binds stored-tile offsets.

Q15 segment arithmetic at entry_count = 200,000 — `[R-CNT-17]`'s region formula,
§15.1's layout, §15.4's segment partition. Three integers.

## Coverage against the charter

- Concrete bytes at concrete offsets: Q01, Q05, Q06, Q07 (and Q13's offset).
- Reader/verifier verdicts on a specific malformed file: Q08, Q09, Q10.
- Arithmetic (sizes, counts, alignment, coverage): Q02, Q04, Q11, Q13, Q15.
- Rules spread across more than one section: Q03, Q05, Q06, Q08, Q09, Q10, Q12.
- Weighted to the changed surface: §2.3 (Q10), §4.2 (Q02, Q13), §6.2 (Q01),
  §7.2/§7.4 (Q13), §11.2 (Q02, Q03, Q08), §11.3 (Q06), §17/§17.2 (Q08),
  §20.3 (Q08, Q12), §21.2 (Q10), Appendix G (Q14).
- No two questions fail for one reason: the two ceiling-division questions use
  different layers; the three verdict questions turn on three unrelated rules
  (a codec cap, a metadata quarantine, a cross-major reach test).

## Questions I built and rejected

1. **Instance count for §21.4 or §21.5.** Determinate (I verified the totals),
   but a counting exercise, not a byte-level one, and prone to spurious
   divergence.
2. **"Does §20.3 step 4 bar reordering two same-element-size channel
   declarations in an interleaved layer whose fills are identical?"** The named
   list ("the set of padding positions ... the decoded size, the byte offset of
   any sample within the decoded tile image, or the codec and filter") does not
   catch it — a *sample*'s byte offset never moves under reordering, only a
   channel's in-sample offset Fᶜ does. But the paragraph says the list "names
   where that effect arises rather than standing on its own", and §14.1 fixes
   which channel value k belongs to, so the general test does catch it. I judged
   the answer determinate but the reasoning chain long enough that a divergence
   would indict the key as readily as the answer. Reported nothing; see
   findings for the weaker sibling I did report.
3. **"Two layer records with byte-identical, ill-formed name fields — F4 or
   L3?"** §19.1 step 4 settles it in terms ("Uniqueness is decided first, and
   over the raw name bytes whether or not each name is itself well-formed"), so
   it is determinate, but it is close to a single-sentence lookup once that
   sentence is found. Cut for spread.
4. **A question on §18.2's Window_Size / Single_Segment_Flag interaction.**
   Determinate, but §18.2 is not on the changed list and the passage is dense
   enough that I could not state the question without half-quoting it.
5. **A question asking which §21.2 rows reach a foreign major.** The preamble
   enumerates them outright. Replaced by Q10, which asks the answerer to apply
   the test to a row the preamble does *not* list.

## Findings

Three, recorded in the structured result. None is claimed byte-level; the
strongest (quiz-01, §22.2) is an ambiguity whose literal reading is
self-defeating, which is why I graded it down rather than up.
