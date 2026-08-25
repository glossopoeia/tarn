# Cleanroom round 26 — quiz author transcript

**No answers appear in this file.** Only the slate, the method, and what was rejected.

## Access

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (4,484 lines,
read whole in four `Read` calls). Ran two local Python scripts in the scratchpad:

- `count_inst.py` — reads the spec file, parses the §21.2–§21.5 register tables, counts rows
  and the semicolon-separated Instances cells. Result: 121 rows / 277 instances, which matches
  §21.8's "121 conditions over 277 instances" and the per-subsection counts (36/49/26/10).
  No finding.
- `crc.py` / `q2.py` — a CRC-32C implementation (Castagnoli, reflected, init/final 0xFFFFFFFF)
  validated against the document's own check vectors and against §7.4's and §15.4's published
  constants. All four reproduced exactly. Used only to confirm that each byte-level question has
  a determinate answer; the computed values are deliberately not recorded here.

No other file was read. No directory listing, no git, no web, no ADRs, no conformance corpus.

**Disclosed context I did not ask for.** The runtime placed a project-instruction pointer, an
index of the maintainer's memory notes, and a git status/recent-commit list in my context before
I began. The commit subjects name section numbers and describe repairs. I treated all of it as
non-evidence and did not use it to choose or aim any question or finding; two of my findings sit
in sections those subjects mention, and I reached both from the seven-passage pointer in my own
brief plus the document text. Disclosed in the structured result.

## Method

1. Read the document end to end once, cold, without the brief's pointers in view.
2. Second pass on the seven named passages (§9.6, §11.1, §13.3, §16.2, §17.2, §21.3, §23.1),
   reading each as it now stands rather than as a diff.
3. Ran the register instance census (hint 5: closed counts) — clean.
4. Censused the document's own uses of the word *last* (hint 7) — see finding quiz-02.
5. Built candidate questions, then discarded any whose answer I could not pin to a single value
   by computation or by two independent readings of the governing text.

## Coverage the slate is built to hit

- Concrete bytes at concrete offsets: Q02, Q03, Q10, Q13 (four, charter asks three).
- Reader/verifier verdicts on a specific malformed file: Q06, Q07, Q08, Q15, and Q11's third part.
- Arithmetic (sizes, counts, alignment, coverage): Q01, Q04, Q05, Q12, Q14.
- Rules whose statement is spread across sections: Q05 (§11.2+§11.4+§15.1), Q09 (§20.3+§14.5+§11.3),
  Q11 (§17.2 rule + its Note + §11.2 + §21.3 L44), Q12 (§16.2+§15.3+§21.3 L41), Q15 (§13.3+§15.3+§19.4).
- Weight on the seven changed passages: §9.6 → Q08; §11.1/§20.3 → Q09; §13.3 → Q15; §16.2 → Q12;
  §17.2 → Q11; §21.3 → Q11 and Q12.

Deliberately no two questions share a single failure mode: the two padding-content questions were
collapsed to one (Q10, packed bool, which additionally exercises pad bits), and the byte-shuffle
question (Q03) supplies its decoded image explicitly so it does not inherit Q10's reasoning.

## The slate (question stems only)

- Q01 layer-record inline payload sizing: inline_length, entry_count, extent_length, and the
  0-based offset of the entry_count field. §7.4 + §11.2 + §12.1 + §15.1.
- Q02 trailer bytes [60,64) for a fully specified trailer. §6.2 + §4.1 + §4.5.
- Q03 byte-shuffle output for a given interleaved decoded image, plus the codec-1 entry length and
  the entry's crc field as stored. §17.3 + §14.2 + §15.1 + §4.5 + `[R-COD-04]`.
- Q04 planar index arithmetic: entry_count, extent_length, disk ordinal, region byte offset.
  §11.2 + §11.4 + §15.1 + §7.4.
- Q05 verifier's slack total for a fully laid-out file. §5.2 + §9.7 + §15.1.
- Q06 four independent defects on a top-level user-metadata record → four outcome classes.
  §7.1 + §18.1 + §18.2 + §21.2/§21.5.
- Q07 experimental-range metadata encoding: verifier verdict word + reader outcome class.
  §18.2 + §21.6 + §2.3.
- Q08 §9.6 recovery probe over a torn 640-byte file: settled offset, recovered length, and what a
  conforming reader on the default path does. §9.6 + §9.5 + §6.2.
- Q09 §20.3 step 4 shrink: two variants, permitted or barred. §20.3 + §14.5 + §11.3.
- Q10 packed boolean plane with a padding position and pad bits: the decoded byte, the stored
  length under codec 1 + filter 2, and the entry crc. §14.3 + §14.5 + §13.2 + §17.3 + §15.1.
- Q11 codec 4 on a zero-extent layer, then after a growth: reject or not, entry_count, outcome.
  §17.2 + its Note + §11.2 + §21.3 L44.
- Q12 slab run packing with a sentinel and a structurally rejected entry vs. a crc-failing entry:
  two required offsets. §16.2 + §15.3 + §21.3 L41.
- Q13 segment CRC array for entry_count = 65,537, all sentinel: the 8 stored bytes and
  crc_of_crc_array. §15.4 + §15.2 + §7.4 + §4.5.
- Q14 directory sizing: dir_length and the smallest F a conforming commit produces.
  §7.2 + §7.1 + §6.2 + §9.2 step 5 + §5.2.
- Q15 planar layer, three channels at one spatial ordinal in three entry states: fill or failure
  for each. §13.3 + §15.3 + §19.4 + `[R-CNF-09]`.

## Rejected candidates, and why

- **"How many candidates did the recovery tool reject?"** — dropped as a question because the
  document does not fix whether a magic match failing the CRC or the `committed_file_length = o + 64`
  test counts as a rejected candidate. Reported instead as finding quiz-01.
- **zstd single-segment Frame_Content_Size for a sub-1-KiB tile** — §17.2's Note establishes that
  such a tile is encodable only as a single-segment frame, but the rule says the content-size field
  "MAY be present", and whether RFC 8878 forces it is external. Indeterminate from this document;
  dropped without a finding, since the underlying rule is not itself unclear.
- **Verifier verdict for a file declaring version_major = 2 with a second, ordinary field
  violation** — §6.2's ordered validation puts the version gate before the field gates, but
  `[R-RDR-02]` lets a reader detect any violation earlier and §2.3 says an established violation
  takes priority. Two defensible verdicts; dropped rather than reported, since a file declaring a
  foreign major is outside this document's predicate either way.
- **A second padding-content question (interleaved numeric edge tile)** — correct and computable,
  but it fails together with Q10 for the same reason (§14.5). Cut.
- **"Which register row does this file exercise?"** — a table lookup; excluded by the charter.
- **An extents-reshape question ((4,6) → (6,4) at tile extents (2,2), entry_count unchanged, disk
  ordinals renumbered)** — I convinced myself §20.3 step 4 permits it (nothing §14 fixes for a
  prior-generation stored tile is altered) and that the resulting file is conforming either way, so
  there is no determinate "must the index be re-emitted" answer that turns on bytes. Not asked;
  the neighbouring narrowness in §13.3's Note is reported as finding quiz-03.
