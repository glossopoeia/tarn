# Round 33 — quiz author transcript

## 0. Access and method

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,805 lines), in full, in six `sed -n` chunks. No other repository file was read
or listed. No git, no web, no conformance corpus, no ADRs, no registry.json.

Local computation only, in my own scratch directory
`/private/tmp/claude-501/.../r33-round/scratch/quiz-author/`:

- `qa_instcount.py` — parses the §21.2–§21.5 register tables out of the spec text
  and counts rows and Instances-cell entries.
- `qa_crc.py` — a from-scratch CRC-32C (reflected, poly 0x82F63B78, init/xor
  0xFFFFFFFF) used only to confirm the specification's own published constants
  reproduce, so that the byte questions below are answerable at all.

Both files are mine alone; neither was written to a shared directory, and nothing
was read back from the output directory.

## 1. What I checked before authoring

I did not want to build a slate on arithmetic the document itself gets wrong, so
I first re-derived every published constant and count I could reach cheaply:

- §4.5's check vector CRC-32C("123456789") and CRC-32C(<empty>) — both reproduce.
- Appendix A's trailer CRC over trailer bytes [0,60) — reproduces.
- §15.4's all-sentinel full-segment constant — reproduces.
- §7.4's worked layer-record example: its segment CRC over the 80-byte
  four-sentinel entry array, and its crc_of_crc_array over that 4-byte array —
  both reproduce; the payload's field-by-field byte budget sums to the stated 81;
  the stated extent_length matches [R-CNT-17]'s formula.
- §15.4's 1,000,000-entry example: segment count, CRC-array offset, segment 15's
  byte range, the region length, the ~339 KB figure and the 1.25 MiB full-segment
  figure all check.
- §21.2/§21.3/§21.4/§21.5 row counts: 35 / 49 / 26 / 10 = 120, matching §21.8;
  Instances cells sum to 277, matching §21.8. (F11 is struck, as §21.2's note says.)
- §21.2's reach derivation (F8, F14, F6, both F1 instances, and no other row)
  against [R-CNT-24]'s fixed trailer fields — holds; F13, F17, F15, F19, F12, F2
  all sit in the 48 redefinable bytes or in format-major-1-derived floors.
- §21.9's Note arithmetic (2^32 tiles → 256 KiB CRC array; 2^36 → 4 MiB) — holds.
- §14.4's P = 1 claim about planar-vs-interleaved single-channel bool — holds.

So the document's arithmetic surface is in good order, and the questions below can
rest on it.

## 2. How I chose the slate

The brief asks for 15 questions weighted toward §2.3, §5.1, §5.2, §7.1, §11.1,
§13.3, §18.2, §20.3, §20.5, §21.1, §21.2, §21.3, §21.6, Appendix F, Appendix H.
I aimed each question at a rule the answerer cannot satisfy by copying a table
cell, and at a place where a wrong reading changes bytes or a verdict.

Coverage of the required spread:

- **Concrete bytes at concrete offsets (≥3):** Q02 (a trailer CRC the answerer
  must assemble 60 bytes to compute), Q03 (a packed planar bool tile image, where
  padding positions and pad bits are two different mechanisms in one byte), Q10
  (crc_of_crc_array over the stored segment-CRC array), Q15 (the fill bytes a
  reader returns, little-endian), Q01 (a region byte offset).
- **Reader/verifier verdicts on a specific malformed file (≥2):** Q04, Q05, Q06,
  Q09, Q11, Q14.
- **Arithmetic (≥2):** Q01, Q08, Q10, Q15.
- **Statement spread over more than one section (≥2):** Q04 (§2.3 + §6.2/§6.3 +
  §21.2's reach derivation + §2.3's F15 note), Q07 (§20.3 step 4 + §11.1 +
  Appendix H), Q09 (§21.1's specialization rule + §21.2), Q11 (§5.2 + §9.7 + §2.3
  + §18.2), Q13 (§2.3 + §21.9 + §21.6), Q14 (§20.5 + §15.3 + §20.4 + [R-WRT-09]).

No two questions fail for the same reason. The three "does the closed list of
§20.3 compose?" style probes (Q07) are separated from the "does a bound reach an
empty layer?" probe (Q08) and from the compaction probe (Q14); the three CRC
questions (Q02, Q10, and Q03's byte assembly) turn on different structures.

## 3. Candidates I considered and rejected

- **"How many instances does §21.8 count, and does the register agree?"** —
  rejected. I verified it (277) so it has a determinate answer, but it is a
  mechanical census, not a byte-level question, and a divergence would indict a
  counting slip rather than a reading.
- **"Which verdict does a verifier report for an experimental-range MU = 1 layer
  sub-record of a type it does not implement?"** — rejected as insufficiently
  determinate for a cold answerer. §2.3's cannot-establish list is unqualified as
  to scope ("when a record carries MUST_UNDERSTAND = 1 with a type it does not
  implement"), while §21.6's closing paragraph treats only the *top-level* case as
  a conforming file a reader refuses. The two are reconcilable — they answer
  different questions (certification versus refusal) — but the reconciliation is
  the kind of thing an independent key could plausibly get the other way, and a
  divergence there would indict the key as readily as the answer. Not a good quiz
  question; noted here instead.
- **A boundary question on binary64 overflow at 1.7976931348623158e308** —
  rejected as needlessly cruel; the underflow/overflow contrast in Q12 tests the
  same rule (§18.2's "not finite" is about overflow, not about underflow to zero)
  without hanging on a 17th significant digit.
- **"Must a compactor refuse when it copies rather than regenerates an index
  region carrying a structurally invalid entry?"** — rejected as a question,
  because the answer turns on a placement choice §20.5 leaves free. I pinned the
  placement in Q14 so the question is determinate, and filed the free-choice
  observation as finding `quiz-03`.
- **"Can a commit remove two trailing planar channels at once?"** — rejected as a
  question for the same reason it became finding `quiz-01`: §20.3's fixed-side
  clause and its permitted-side clause pull in opposite directions and are
  reconciled only by a sentence several paragraphs later. Asking it would test
  whether the answerer found that sentence, not what the format does.
- **"What is the smallest conforming file?"** — rejected: Appendix A hands it over.
- **"Which of the eight §10.2 spaces has no experimental range?"** — rejected:
  one table cell.

## 4. The slate

Fifteen questions, each written to stand alone. Answers are recorded nowhere —
not here, not in the question text, not in my scratch files beyond the constant
checks in §1 above, which are the document's own published values.

1. **Q01** — planar entry_count, [R-CNT-17] extent_length, and the region byte
   offset of one entry, from geometry alone. §11.2 + §11.4 + §7.4 + §15.1.
2. **Q02** — the four stored trailer-CRC bytes of a fully specified 192-byte file.
   §6.2 + §4.5 + §4.1.
3. **Q03** — the two-byte decoded image of a packed planar bool edge tile where
   padding positions and pad bits both appear. §11.2 + §11.3 + §14.3 + §14.5 + §4.4.
4. **Q04** — the verifier verdict on a file declaring format major 2 with nonzero
   trailer reserved bytes. §2.3 [R-CNF-13] and its F15/F5 note + §21.2's reach
   derivation + §6.2's ordered validation.
5. **Q05** — the verifier verdict on a file carrying one experimental-range and
   one reserved-range user-metadata encoding. §18.2 [R-MTA-10] + §21.5 R1 + §21.6.
6. **Q06** — outcome class, claimant contribution, and walk completeness for a
   length-0 non-sentinel index entry. §15.3 + §9.7 + §5.2.
7. **Q07** — three composition questions about §20.3 step 4's closed list and its
   one exception. §20.3 + §11.1 + Appendix H.
8. **Q08** — [R-COD-07]'s lz4 cap against a layer with a zero extent versus one
   without. §17.2 + its Note + §11.2 + §14.2.
9. **Q09** — which row a reserved-range MU = 1 top-level record is recorded
   against, with its detector and detection point. §21.1 + §21.2.
10. **Q10** — segment count and crc_of_crc_array for a 65,536-entry all-sentinel
    index. §15.1 + §15.4 + §7.4 + §4.5.
11. **Q11** — whether a declined tile decode and a declined document decode make a
    verifier's slack total partial, and what verdict follows. §5.2 + §9.7 + §2.3
    + §18.2 [R-MTA-09].
12. **Q12** — overflow versus underflow under §18.2's finite-numbers restriction.
    §18.2 + Appendix F's IEEE 754 entry + §21.5 R8.
13. **Q13** — a layer exceeding §21.9's channel guarantee: file conformance,
    permitted decline, and the limit on that permission. §2.3 + §21.9 + §21.6.
14. **Q14** — whether a compactor must refuse a file with a structurally invalid
    index entry when its placement relocates that layer's stored extents, and
    whether dropping the entry is available. §20.5 + §15.3 + §20.4 + [R-WRT-09].
15. **Q15** — a planar sentinel read: disk ordinal and the exact returned fill
    bytes. §11.2 + §11.4 + §13.1 + §13.3 + §4.1.

## 5. Findings raised while authoring

Three, all recorded in the structured result as `quiz-01` … `quiz-03`. None is
byte-level; each says why in its own rationale. Summary:

- `quiz-01` (OBSERVATION) — §20.3 step 4's fixed-side clause "the position of
  every planar channel but the last" reads, alone, as permitting only one trailing
  channel to be removed, while the permitted side and the "what the line gives up"
  list both admit a run at the end. Decided by the "the permitted side states the
  whole of what a commit MAY do to it" sentence, several sentences on.
- `quiz-02` (CONTRADICTION) — §15.3 says the bytes a structurally-rejected entry
  nominally addressed fall to slack only where *no other claimant claims them*;
  §9.7 and §5.2 both restate the same disposal without that qualifier.
- `quiz-03` (OBSERVATION) — §20.5's refusal obligation for a structurally invalid
  index entry is reached only through region *regeneration*, which is triggered by
  a placement choice the compactor is free to make.

## 6. Disclosure

Read: `spec/tarn.md`, and nothing else. Ran: `qa_instcount.py` and `qa_crc.py`,
both written by me into my own scratch directory, both reading only that one file
or no file at all. Unsolicited context did appear in my runtime before I began
(project instruction files and an index of maintainer memory notes naming this
project's process); I disregarded it and did not act on any of it. The spec was
where the brief said it would be.
