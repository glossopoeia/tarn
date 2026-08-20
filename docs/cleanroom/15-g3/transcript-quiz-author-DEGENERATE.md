# Round 15 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,227 lines, read end to end in five passes). No other file was opened, no
directory listed, no git command run, no web access. Local computation only:
`python3` implementing CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF)
and integer arithmetic, in scratch files I created myself under this
scratchpad. No answers are recorded here.

## What I did before authoring

I refused to write questions off the changed-section list. Instead I built,
on paper and in Python, the artifacts the charter names:

1. **Re-derived every numeric example the document states**, to find out
   whether the text is arithmetically trustworthy before leaning on it:
   - CRC-32C check vector `"123456789"` → matches §4.5.
   - CRC-32C of zero bytes → matches §4.5 and Appendix A's empty directory.
   - §7.4's worked layer record: I reconstructed the 81-byte inline payload
     byte for byte from the field table, the §4.6 name prefix rule, §12.1's
     element sizes, and §11.2's grid arithmetic. It reproduces the document's
     hex dump exactly, including the 80-byte all-sentinel entry array's CRC
     and the 4-byte `crc_of_crc_array` over it.
   - §15.4's full all-sentinel segment constant → reproduced.
   - Appendix A's trailer CRC over trailer bytes [0,60) → reproduced.
   - §17.3's byte-shuffle example, §14.2's three offset examples, §14.3's
     packed-plane example, §14.5's padding example, §11.4's ordinal example,
     §15.4's two segment examples, §20.3's 644-byte index example, §21.9's
     "256 KiB at 2^32 / 4 MiB at 2^36" note — all checked by hand, all correct.

   Conclusion: the document's stated numbers are clean. That matters, because
   it means a divergence between answerer and key on any arithmetic question I
   ask is a divergence about *rules*, not about the document's own sums.

2. **Recounted §21's register arithmetic from scratch.** Rows: §21.2 = 36,
   §21.3 = 49, §21.4 = 26, §21.5 = 10, total 121 — matches §21.8. Instances,
   counted cell by cell under §21.1's stated criterion: §21.2 = 57,
   §21.3 = 115, §21.4 = 57, §21.5 = 44, total 273 — matches §21.8 exactly.
   I checked §21.1's two stated axes (layout formulas; magnitude direction)
   against every row that could exercise them (T3, T14, T21, T22, T4, T26,
   L21, L22, L30, L44, L37, L38, F17, F5) and found no row applying the
   criterion inconsistently. I also checked the specialization list
   (F1/F6/F8, F35/F36, L24/L25) and the F7-vs-F33 claimant asymmetry, which
   is correct: the directory region cannot sit between its own end and the
   trailer.

   So I did **not** ask an instance-counting question. It would have been a
   semicolon count, not a rule application, and the register is self-consistent.

3. **Traced the crc-failing-entry rule through all four places it lands**:
   §15.3's prose ("its extent stands and it keeps its place in the *verifier*
   rows, in run continuity, and in the coverage walk"), §16.2's slab
   transparency paragraph, §9.7's coverage walk, and L41's Instances cell.
   All four agree. This is the highest-torque new text in the document and it
   holds together; I built question 9 on it because an implementer who gets it
   backwards emits or accepts a different verdict.

4. **Walked the append and compaction procedures end to end** for a concrete
   file: established F, computed the new payload/index/directory/pad/trailer
   offsets, and derived the new `committed_file_length`. That exercise is what
   produced question 7 (the zero-length pad case) and question 4 (the
   compactor's `version_minor` and flags).

5. **Built a profile-conforming file under Appendix G** — three layers, name
   byte ordering including the prefix case, contiguous placement from offset
   16 — which produced question 6, and worked item 2's `file_id` derivation
   through to the bytes on disk, which produced question 5.

## How the slate was chosen

Weighting toward the newest text without letting the section list become a
checklist:

- §5.2 (partial slack total, rejected-layer discard) → Q8
- §16.2 (crc-failing entry is not transparent to run packing) → Q9
- §20.3 step 4 (the declaration-change bar and its tense) → Q10
- §20.5 (compactor trailer fields) → Q4
- §21.5 / §21.6 boundary (reserved vs experimental metadata encoding) → Q11
- Appendix G items 2 and 3 → Q5, Q6

and the rest built from end-to-end implementation of untouched text, where
five straight rounds have found real defects: §7.4 record framing (Q1),
§14.3 packed planes with padding (Q2), §14.2 + §17.1 + §17.3 pipeline order
(Q3), §9.2 commit arithmetic (Q7), §17.2's lz4 cap against §14.2's stride
(Q14), §11.4 + §15.1 + §15.4 index addressing (Q15), §6.2/§6.3 ordered
validation and verdict selection (Q12), §19.1 step 4's uniqueness-first rule
(Q13).

Coverage against the charter's spread requirement:
- concrete bytes at concrete offsets: Q2, Q3, Q4, Q5, Q7
- reader/verifier verdicts on a specific malformed file: Q11, Q12, Q13
  (and Q10 on a writer verdict)
- arithmetic (sizes, counts, alignment, coverage): Q1, Q6, Q7, Q8, Q9, Q14, Q15
- rules whose statement is spread across sections: Q4 (§6.3+§20.5+§6.2),
  Q8 (§5.2+§9.7), Q9 (§15.3+§16.2), Q11 (§18.2+§21.5+§21.6+§2.3),
  Q13 (§19.1+§4.6+§21.2), Q14 (§11.2+§14.2+§17.2), Q15 (§11.4+§15.1+§15.4)

No two questions fail for the same reason. In particular the three verdict
questions turn on three different mechanisms: the assigned/unassigned value-set
boundary (Q11), §6.2's validation *order* plus the capability ground (Q12), and
§19.1's uniqueness-before-well-formedness rule (Q13).

## What I rejected, and why

- **An instance-count question over §21.3.** Counts as a semicolon tally, not
  a rule application; and I verified the register already sums correctly.
- **"Which register row does file X exercise?"** Too many files exercise more
  than one row (F5 and F10 both fire on `committed_file_length` = 64), and
  §24 explicitly contemplates multi-row files, so the answer is not single.
- **A question on §6.2 ordered validation with a foreign major *and* a bad
  trailer CRC.** §21.2's preamble says every row presupposes a file declaring
  major 1, while its own trailing clause admits that the magic and CRC checks
  precede the version gate. Whether F14 reaches a file whose version_major
  byte cannot be trusted is genuinely unsettled; that is a finding, not a
  question. I reduced Q12 to a *verifying* trailer CRC so the ordering is
  unambiguous.
- **A question on shrinking an extent across a grid boundary.** I could not
  determine the answer from the document — see finding quiz-01. Replaced with
  Q10, which asks the growth/supersede case §20.3 does settle expressly.
- **A question on what a compactor emits for a structurally malformed index
  entry.** Decidable but only by a long chain (§20.5 → [R-WRT-09]'s reliance
  principle → §15.3 → [R-WRT-06]); too expensive to be a fair quiz item. Filed
  as finding quiz-02 instead.
- **A question about [R-SER-08]'s returned value framed through §21.1's
  closing paragraph.** §21.1 describes that rule as obliging a reader "to serve
  the structure unchanged", which is not what [R-SER-08] says. Filed as
  finding quiz-03 rather than asked.

## The slate (question text only — no answers recorded anywhere)

Q01  Layer record inline_length and index extent_length for a described
     planar rank-2 layer with a bool and a uint16 channel.
Q02  The two decoded bytes of a packed planar bool edge tile whose only real
     position is false and whose channel fill is true.
Q03  The twelve stored bytes of an interleaved uint8+uint16 tile under
     filter 2 then codec 1.
Q04  Trailer bytes [8,16) of a compactor's output, given an input at
     version_minor 3 with two ignore-lane bits set.
Q05  The eight bytes written into file_id under Appendix G item 2, given the
     digest's last eight bytes.
Q06  The byte offset at which a named layer's tile-index region begins in a
     profile-conforming three-layer file.
Q07  The eight bytes of committed_file_length after a commit whose directory
     ends exactly on a 64-byte boundary.
Q08  The partial slack total a verifier reports when a layer is rejected by an
     intra-layer overlap the walk itself established.
Q09  The offset the last stored tile of a slab run must carry, given one
     structurally malformed entry and one crc-failing entry inside the run.
Q10  Barred or permitted: a fill change that supersedes every tile of a layer
     with padding positions; and a fill change on a layer with none.
Q11  Reader outcome and verifier verdict for a reserved-range vs an
     experimental-range user-metadata encoding byte.
Q12  The verifier verdict for a file declaring an unimplemented format major
     whose directory CRC is also wrong.
Q13  The outcome class and detection tier for two layer records with
     byte-identical but ill-formed name fields.
Q14  The largest sample stride Q for which codec 4 may be declared at tile
     extents (16384, 16384).
Q15  Disk ordinal, entry byte offset, segment index, and index extent_length
     for a channel of a planar layer.

## Findings

Three, reported in the structured result as quiz-01 through quiz-03. Summary:

- **quiz-01 (AMBIGUITY, byte-level).** §20.3 step 4 does not settle whether a
  commit may shrink an extent so that whole tiles cease to be addressed. Two
  defensible readings; one lets an appender emit the commit, the other forces a
  whole-file rewrite.
- **quiz-02 (OBSERVATION).** §20.5/[R-WRT-09] never name §15.3's entry
  classification, so what a compactor owes on a structurally malformed index
  entry — refuse, or relocate — is decidable only through a four-hop chain.
- **quiz-03 (CONTRADICTION).** §21.1 says several verifier-detected rows'
  governing rules oblige a reader "to serve the structure unchanged", and cites
  [R-SER-08]; [R-SER-08] obliges the opposite — it resolves the byte.
