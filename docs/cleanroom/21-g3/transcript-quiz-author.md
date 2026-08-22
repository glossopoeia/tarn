# Round 21 — quiz author transcript

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (4,377 lines, five sequential reads plus `wc -l`). Ran four local
Python computations that read no project file except one `grep` and one
`python3` pass over `spec/tarn.md` itself (register instance counting).
No ADRs, no `docs/`, no `conformance/`, no `registry.json`, no git history,
no web.

Context I did not ask for appeared before I began: a project instruction
file pointer and an index of maintainer memory-file titles. I did not open
any of it and did not use it. Disclosed in the structured result.

## Instrument calibration

Before authoring I verified my CRC-32C implementation against every value
the document states, so that any byte-level question I ask is one I have
actually checked rather than asserted:

- `CRC-32C("123456789")` → matches §4.5's check vector.
- `CRC-32C(<zero bytes>)` → matches §4.5.
- CRC over 80 bytes of four sentinel entries → matches §7.4's worked example.
- `crc_of_crc_array` over those four stored bytes → matches §7.4.
- CRC over 2^16 sentinel entries → matches §15.4's constant.
- CRC over Appendix A's trailer bytes [0, 60) → matches the stored value.

Six independent agreements. The implementation is the document's.

I also mechanically counted §21.2–§21.5: 121 rows, 273 instances by the
semicolon rule of §21.1 (a cell reading `—` counting as one). §21.8's
"121 conditions over 273 instances" is exact. Not a finding; recorded so the
next author does not re-spend the effort.

## Where I spent attention

Per the brief I read §18.2 and §21.5 first, then walked the whole document
as an implementer: front block → trailer → directory → layer record →
tile index → tile serialization → codec pipeline → the writer/updater
procedures → the register. Three of the fifteen questions sit squarely on
the newest text (Q01, Q02, Q03); the other twelve are spread across the
container, the array model, the arithmetic, and the writer path.

The judgement I made about the changed surface: the two passages settle a
*capability vs. defect* boundary, and the interesting failures are not
"did you read the new clause" but "does the new clause survive contact with
[R-CNF-11]'s priority rule and [R-ERR-04]'s floor". So Q01 tests the clean
decline, Q02 tests the floor beneath a reader's own bound, and Q03 tests
what a declining verifier still owes on header-checkable constraints. They
fail for three different reasons.

## The slate, and why each earns its place

- **Q01** — three otherwise-conforming files differing only in a
  user-metadata encoding byte / declared window. Forces the answerer to
  separate: a decline on the frame window (capability), an unassigned
  experimental encoding (defined non-violation), and a reserved-range
  encoding (R1, a violation). Draws on §18.2, §21.5's preamble, §21.6,
  §2.3. Three verdict names.
- **Q02** — a reader whose own document bound sits *below* §21.9's
  guarantee. Tests the floor in [R-MTA-09] against [R-ERR-04]'s
  "declines on that ground ... is not a conforming reader". Three yes/no.
- **Q03** — a verifier that declines on the window but can still read the
  frame header. Tests whether [R-CNF-11]'s "established violation takes
  priority" beats §18.2's cannot-establish. Outcome class, verdict, yes/no.
- **Q04** — build a layer record inline payload end to end: `inline_length`,
  the extent slot's length under [R-CNT-17], and the offset at which the
  first dimension entry begins. Requires §7.4's field order, §11.2's grid
  arithmetic, §11.2's planar addressed-tile count.
- **Q05** — concrete CRC bytes for a three-entry all-sentinel index:
  the segment CRC and `crc_of_crc_array`, as stored. §15.2 + §15.4 + §4.5,
  and the trap that §15.4's `0xEECB3BB2` constant is licensed for *full*
  segments only.
- **Q06** — planar disk ordinal, region byte offset, in-tile ordinal, and
  the value's byte offset inside the decoded plane. §11.4 + §15.1 + §14.2.
- **Q07** — a packed boolean plane's two decoded bytes, pad bit included,
  plus the index entry's length under codec 1. §14.3 + §14.5 + §4.4 +
  [R-COD-04].
- **Q08** — an interleaved edge tile's twelve decoded bytes with fill-encoded
  padding positions. §11.3 + §14.2's stride arithmetic + §14.5.
- **Q09** — a foreign major with a second defect behind the version gate.
  §6.2's ordered validation + §2.3's cannot-establish + §21.2's preamble
  about which four rows reach such a file.
- **Q10** — experimental vs reserved sub-record type at MU = 1: file
  conformance and whether the reader may refuse the file. §7.4's
  [R-CNT-18], §10.2/§10.3, §21.6's closing paragraphs, [R-CNF-12].
  This is the question I most expect to split an answerer from a key.
- **Q11** — a compactor meeting a structurally malformed index entry it must
  regenerate. §15.3 + §20.5.
- **Q12** — a partial slack total's arithmetic, its label, and the verdict.
  §5.2's [R-CNT-21] + §9.7 + §2.3.
- **Q13** — a shrink that turns a real position into a padding position:
  barred or permitted, turning on the byte already stored there. §11.2 +
  §14.5 + §20.3 step 4's exception clause.
- **Q14** — a zstd tile below 1 KiB: max declarable window, and whether the
  frame must be single-segment. §14.2 + §17.2 + its note.
- **Q15** — a non-resident front block with nonzero reserved bytes: reader
  obligation, file conformance, verifier verdict, governing rule. §6.1 +
  §19.1 step 1 + §19.2 + §21.2.

## Coverage against the charter

- Concrete bytes at concrete offsets: Q05, Q07, Q08 (and Q04's offsets).
- Reader/verifier verdicts on a specific malformed file: Q03, Q09, Q10,
  Q12, Q15.
- Arithmetic: Q04, Q06, Q12, Q13, Q14.
- Rules spread across more than one section: Q02, Q10, Q11, Q13, Q15.
- No two questions fail for the same reason. The two padding questions
  (Q07, Q08) use disjoint machinery — bit packing with pad bits versus
  sample-stride interleaving with padding positions — and a reader who gets
  one right can still get the other wrong.

## Questions I drafted and rejected

1. *"What outcome class does a conforming reader apply to a user-metadata
   record whose decoded document exceeds the reader's own bound?"* —
   **indeterminate.** [R-MTA-09] says ignore-record; [R-ERR-04] permits
   declining the whole file, and §18.2's Note treats both as available.
   Reported as `quiz-03`. I removed this clause from Q02 rather than let it
   masquerade as a divergence.

2. *"Name the §21.5 row this condition exercises."* — replaced by asking for
   the governing requirement identifier. §24 ([R-VEC-02]) says row labels
   are positional and renumber; the identifier is the stable half. Asking
   for a label would have been a question about the document's typesetting.

3. *"Is the writer that left a 156-byte pre-trailer gap conforming?"* —
   dropped. The file is conforming ([R-CNF-02] names this exact case as a
   conduct rule), but "is the writer conforming" is a question about an
   actor across a whole session, not a byte or a verdict, and the answer
   form would have been an essay. I kept nothing from it.

4. *"Which of two zstd Window_Size derivations does a reader implement?"* —
   dropped as a non-question: §17.2's note establishes that no conforming
   file turns on it. Asking would have tested reading comprehension of a
   note rather than the format.

5. A trailer-CRC-from-scratch question (mutate Appendix A's `file_id` and
   `generation`, emit the new 4 CRC bytes). Dropped for redundancy with
   Q05 — both would have failed together on a wrong CRC-32C
   parameterization, which the charter forbids. Q05 keeps the CRC work but
   pins it to the sentinel/segment machinery, so a wrong answer there is
   diagnostic of §15.4 rather than of §4.5 alone.

6. *"May an appender repair a malformed index entry it re-emits?"* —
   the answer is stated flatly in §20.3 step 2 ("carried forward
   byte-identically ... not repaired to a sentinel"). Single-cell lookup;
   dropped in favour of Q11, which needs the same fact plus §20.5's
   regeneration classification and §15.3's structural-ground row.

## Note on answer forms

Every hex answer states its case in the question text (Q05 lowercase;
Q07 and Q08 uppercase), so a case difference cannot be scored as a
divergence. Every verdict question names the three verdict words verbatim.
Every integer answer is a plain integer with no units embedded.

No answers are recorded here or in the question text.
