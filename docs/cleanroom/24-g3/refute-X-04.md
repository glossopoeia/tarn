# Refute pass — X-04

## Read
- /private/tmp/.../r24audit/finish/finding-X-04.md
- /private/tmp/.../r24audit/hunk-02.diff
- spec/tarn.md: lines 94-145 (§2.1-§2.3, [R-CNF-01], [R-CNF-02]), 145-240 ([R-CNF-03..05], [R-CNF-11], §2.4),
  560-585 ([R-CNT-01], [R-CNT-27]), 720-760 (§6.1 tail, §6.2 trailer layout table),
  755-810 ([R-CNT-05], [R-CNT-06], §6.3 [R-CNT-07], [R-CNT-24]), 820-870 ([R-CNT-26], §6.4, [R-CNT-09], [R-CNT-10]),
  1288-1320 (§9.6 [R-LIF-06]), 2390-2410 (§17.4 [R-COD-11]), 3317-3396 (§21.1), 3390-3455 (§21.2 preamble + rows F1-F13),
  3580-3640 (§21.6), 3699-3710 (§21.8 [R-ERR-02], §21.9 head), 3969-4040 (§24 [R-VEC-01..04]).

## Greps run (exact)
- `grep -n "R-CNT-27\|R-CNT-24\|R-CNT-10\|R-CNF-02\|R-CNF-05" spec/tarn.md` -> hits incl. 575, 771, 803, 830, 864, 3400, 3405, 3408, 3422, 3785.
- `grep -n "cannot establish" spec/tarn.md` -> 194, 211, 221, 2400, 2403, 2508.
- `grep -n "^#### 21\.\|^### 21" spec/tarn.md` -> 3317, 3319, 3396, 3455, 3512, 3546, 3580, 3634, 3699, 3706.
- `grep -n "9.6\|recovery" spec/tarn.md` -> 59, 616, 766, 1216, 1250, 1288, 1295, 1305, 2950, 3298, 3599, 3859-3862, 3913.
- `grep -n "128-byte floor\|precedes\|do reach it" spec/tarn.md` -> 2431, 3404, 3409.

## Question 1 — real as text?

The repaired sentence (3403-3412):
  "Five rows are outside that reasoning and do reach it. Four have as their subject a field
   fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer
   CRC ... and F6 with F1's front-block instance ... The fifth is F5, `[R-CNT-27]`'s 128-byte
   floor, which §6.2's order does not name because it precedes that order: a file shorter than
   128 bytes has no trailer to read a magic, a CRC or a version from, so the floor is
   established before any field the gate consults exists."

F5's Instances cell (3422): "F (physical file size); committed_file_length" — two instances.

Three independent pieces of the document show the sentence's own justification cannot cover
instance 2:

(a) §6.2 trailer layout (line ~748): committed_file_length sits at trailer offset 40; version_major
    at trailer offset 8. Instance 2's subject lives *inside* the trailer the sentence says a
    too-short file "has no trailer to read a ... version from". If the trailer is absent, so is
    committed_file_length. The stated ground is self-defeating for instance 2.

(b) [R-CNT-06] (771-776): "A reader MUST validate, in order: the trailer magic; the trailer CRC;
    the version gate (§6.3) ... and then, those gates passed, MUST validate all of the following
    ... committed_file_length equals the file size ... and is a multiple of 64". The
    committed_file_length check is expressly *post*-gate. Instance 2 cannot precede the gate.

(c) Decisive, and from the sentence's own cited rule: [R-CNT-24] (803) fixes across every major
    only "the trailer magic at F − 64, version_major and version_minor at F − 56, and a CRC-32C at
    F − 4", and "A future major MAY redefine only the remaining 48 trailer bytes". Trailer offset 40
    is inside those 48 redefinable bytes. So in a file declaring another major, the eight bytes at
    trailer offset 40 are not committed_file_length at all — the field does not exist there. The
    sentence's stated criterion for the other four ("their subject is a field fixed across every
    major ([R-CNT-24])") *excludes* F5's second instance by name.

And the sentence splits F1 by instance twice in the same breath ("F1's trailer-magic instance",
"F1's front-block instance"), so a bare "F5" reads as the whole row under the convention the
sentence itself establishes.

=> The finding is real as text. The repaired sentence is over-broad and unsupported by what it
cites for half the row it names.

## Question 2 — byte-level?

Divergent file class needed for X-04 (instance 2 fires, instance 1 does not, foreign major):
  W = physical size 4096; final 64 bytes carry the trailer magic and a correct trailer CRC;
      version_major = 7; bytes at trailer offset 40 = 64 (below the 128 floor, multiple of 64).

Constructions tried, actor by actor:

1. Reader. [R-CNT-06] orders magic, CRC, version gate; [R-CNT-07] "A reader MUST reject-file when
   version_major is ... a major it does not implement". Reject-file under BOTH readings. Under
   reading A the register outcome for F5 is also reject-file (§21.2 "Outcome: reject-file").
   Same verdict, same bytes.

2. Verifier. Tempting lever: [R-CNF-11] "An established violation takes priority: a verifier that
   has established any violation reports *nonconforming* ... and *cannot establish* is available
   only to a traversal that established no violation." So reading A (violation established) would
   give *nonconforming* and reading B *cannot establish*. But [R-CNF-02] (139-144) is categorical:
   "a file declaring another major is neither conforming nor nonconforming under it: a reader
   refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a
   finding about its bytes." §21.6's closing paragraph repeats it: "a file this document declines
   to judge is not one [a register row]". A verifier therefore cannot report *nonconforming* for W
   under either reading, and MUST NOT certify it either way. The accept/reject bit is identical;
   only the diagnostic label and the per-requirement report move, and neither is a byte of a file.
   Note also that this same tension exists for the four uncontested rows, so it is not created by
   X-04.

3. Writer / creator / appender / updater. No writer under this text emits version_major ≠ 1
   (§6.2 valid-values "1 (0 invalid; others: §6.3)"; [R-CNT-24]). W is outside the emittable set
   under both readings. The set does not move.

4. Corpus author (the auditor's own byte-level route). §21.8/[R-ERR-02] wants "one vector per
   instance"; F5 = 2 instances under both readings (X-04 does not change the arithmetic, and the
   finding concedes this). [R-VEC-04] settles the rest: "every vector built from §21's register is
   nonconforming". W is neither conforming nor nonconforming, so no §21 register vector declares a
   foreign major at all. Both F5 vectors are major-1 files under both readings. The corpus does
   not move a byte.

5. Recovery tool (§9.6, [R-LIF-06]). The probe requires "committed_file_length = o + 64", so any
   candidate the probe accepts has declared length equal to the truncated physical length — the two
   F5 instances coincide and never diverge. Whole-file re-verification of the truncated output then
   runs [R-CNT-27] on the physical instance. No divergence attributable to instance 2.

6. A reader that implements major 7. Not constructible from this document alone — this text defines
   major 1 only ([R-CNF-02]), so "two conforming implementations reading only this document" cannot
   include one.

=> Not byte-level. Every construction lands on a file this document declines to judge, which every
conforming reader rejects, no conforming writer emits, and no register vector can be.

## Verdict

The verifier's rationale ("the file at issue declares a major this text does not judge ... every
reader rejects it either way") is CORRECT about byte impact — and byte impact was never in dispute:
the auditor graded X-04 not byte-level themselves. What the rationale never touches is whether the
repaired sentence is right. It is not: [R-CNT-24], the sentence's own citation, places
committed_file_length among the 48 bytes a future major may redefine, and [R-CNT-06] places its
check after the gate. A REFUTED grade has to establish the repaired text is correct; this one
established only non-byte-levelness. DOWNGRADE_REFUTED as to the REFUTED grade; the finding stands
as a real, non-byte-level textual defect.
