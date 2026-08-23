# Cleanroom round 22 — quiz author transcript

**No answers appear in this file.** I am the author only. Where I say a
question "is determinate", that is a claim about the document, not a record of
the value.

## Access and disclosure

Read: `spec/tarn.md` only, in five sequential passes covering lines 1–4394.
No `docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`, no
`AGENTS.md`, no git history, no web.

Ran: `wc -l` on that one file; three local Python scripts I authored in my
scratchpad (`crc.py`, `t.py`) implementing CRC-32C from §4.5's stated
parameters and packing trailer bytes from §6.2's stated layout. These read no
project files. Wrote: `crc.py`, `t.py`, and this transcript.

Unrequested context appeared in my context window before I began: a project
instruction file, an index of maintainer notes, and a task list naming prior
rounds. I did not read any of the files those pointed at, and nothing in them
informed any question or finding below. I name their appearance without
repeating their contents.

## Calibration work before authoring

I re-derived every constant the document asserts about itself that a quiz
could rest on, so that a divergence between answerer and key can never be the
document's own arithmetic:

- `CRC-32C("123456789")` and `CRC-32C(<empty>)` — §4.5's check vector: reproduce.
- §7.4's worked layer record: the 80-byte all-sentinel entry array's CRC, and
  the crc_of_crc_array over the resulting 4-byte array: both reproduce.
- §15.4's constant for a full segment of 2^16 sentinel entries: reproduces.
- Appendix A's trailer CRC over trailer bytes [0, 60): reproduces, which
  confirms my field-offset reading of §6.2's table.
- §17.3's byte-shuffle example (s = 4, n = 3): reproduces by hand.
- §7.4's inline_length of 81 and extent slot length of 84: reproduce.
- §15.4's 1,000,000-entry example (16 segments, region 20,000,064 bytes,
  segment 15 at [19,660,800, 20,000,000), entry at segment-relative 339,180):
  reproduces.
- §21.8's "121 conditions over 273 instances": I counted every Instances cell
  of §21.2–§21.5 by hand. 58 + 116 + 55 + 44 = 273, and 36 + 49 + 26 + 10 =
  121. Both totals are correct as the cells currently read. This mattered
  because one of my findings is about a cell that I believe is now
  *under*-enumerated; the totals being otherwise exact is what makes that
  claim sharp rather than noise.

## Where I looked

Charter directed me at §18.2 and §21.9 first. I read both closely, then walked
the document end to end building a file: front block → trailer → directory →
layer record → geometry → tile index → slab → codec pipeline → decoded tile
image → metadata extent → the register rows each step can trip. I then built
two degenerate-but-legal files on purpose: (1) a layer that addresses tiles but
stores none, and (2) a layer with rank 40 and one zero extent. Both were
productive.

## The slate, and why each question earns its place

Distribution against the charter's floors:

- Concrete bytes at concrete offsets: Q01, Q02, Q07, Q08 (four; floor three).
- Reader/verifier verdicts on a specific malformed file: Q03, Q09, Q10, Q13,
  Q15 (five; floor two).
- Arithmetic (sizes, counts, alignment, coverage): Q05, Q06, Q12, Q15 (four;
  floor two).
- Rules spread across more than one section: Q03 (§18.2+§21.5+§19.2),
  Q04 (§18.2+§2.3+§21.5+§21.9), Q05 (§21.9+§11.2+§14.2+§21.6),
  Q09 (§15.3+§9.7+§16.2+§20.5), Q10 (§7.4+§10.2/§10.3+§21.3+§21.6),
  Q14 (§20.3+§20.4+§7.3), Q11 (§2.3+§6.3+§21.1/§21.6) (seven; floor two).
- Newest text: Q03 and Q04 sit on §18.2's content-size and window paragraphs;
  Q05 sits on §21.9's per-instance/declaration split. Three of fifteen.

Independence check — no two questions fail for the same reason:

- Q01 and Q08 both encode little-endian multi-byte fields, but Q01's failure
  mode is length-prefix/element-size framing in a *declaration*, Q08's is
  in-sample offset arithmetic (Q, F_c) inside a *decoded image*. Disjoint rules.
- Q07 and Q08 both concern decoded tile images, but Q07's failure mode is
  LSB-first bit packing plus pad-bit content, Q08's is byte stride. I
  deliberately gave Q08 a layer with no padding positions so that "padding
  carries fill" is load-bearing in exactly one question.
- Q03 and Q04 are both §18.2 metadata questions, but Q03 turns on
  violation-versus-not (a content-size mismatch is a violation, row R3), and
  Q04 on capability-versus-defect (a wide window is not a violation, and the
  verdict is not *nonconforming*). A reader who confuses those two axes fails
  one and passes the other; a reader who has them right passes both. They do
  not collapse.
- Q05 and Q11 both test "conforming file a reader may nonetheless refuse", but
  Q05's mechanism is §21.9's guarantees and Q11's is §6.3's conduct-versus-bytes
  split. Different rules, different failure.
- Q06 and Q12 are both arithmetic, but Q06 is ordinal/index arithmetic inside a
  layer and Q12 is whole-file coverage accounting. No shared step.

Per-question notes:

**Q01** — channel entries plus inline_length. Requires §4.6's `u8` length
prefixes, §12.1's element-size column, §13.2's constraint that a bool fill is
exactly `0x00` or `0x01`, §4.1's little-endian rule, and §7.4's field order
including the three `u64`s that are zero. The inline_length half forces a full
walk of §7.4's table rather than a spot lookup. Getting it wrong emits a layer
record whose framing another implementation cannot parse.

**Q02** — the trailer CRC of a file described by its layout rather than by its
field values. The answerer must derive dir_length from §7.2's 24-byte header
plus `[R-MTA-03]`'s inline_length of 1 plus §7.1's terminal CRC, then derive F
from `[R-LIF-02]` step 5's pad-to-64 and §6.2's F mod 64 = 0, then lay out
§6.2's table and compute CRC-32C per §4.5. I picked values that differ from
Appendix A in generation, dir_offset, dir_length, F and file_id so the answer
cannot be copied out of the appendix. I verified the derived layout is
conforming (dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
F a multiple of 64; extent within [16, F − 64); no structure between the
directory's end and the trailer, per `[R-CNT-05]`).

**Q03** — §18.2's new content-size sentence. The document expressly routes a
Frame_Content_Size mismatch to R3 and not to R4, and R4's Instances cell
enumerates exactly the six frame constraints that do *not* include content
size, which confirms the routing. The question also asks for detector and
detection tier, which are in §21.5's row and §19.2's list, not in §18.2.

**Q04** — §18.2's Window_Size paragraph crossed with §2.3's verdict rules and
§21.9's guarantee. Three separate traps: (i) the file's status, (ii) the
verifier's verdict, which is *not* nonconforming, (iii) the reader's outcome
class, which is ignore-record and not a scope rejection.

**Q05** — §21.9's new per-instance paragraph, tested on a file that trips one
declaration row and would trip one per-instance row if that row ranged over
declarations. I deliberately used a layer that addresses *no* tile, because
that is the case §21.9's own clarifying clause settles; the case it does not
settle is the subject of finding quiz-01 and is kept out of the slate.

**Q06** — index arithmetic end to end: §11.2's ceiling division, §11.4's
spatial and disk ordinals for a planar layer, §11.4's permanent in-tile
row-major ordinal, and `[R-CNT-17]`'s extent_length formula including the
segment-CRC array term. Four integers, all mechanical.

**Q07** — §14.3's packed plane crossed with §14.5's padding content and §11.3's
definition of a padding position, plus `[R-COD-04]`'s length equality under
codec 1. The layer's tile extent exceeds one dimension's extent, so the tile
carries both padding positions *and* pad bits — the two mechanisms §14.3's Note
insists are distinct.

**Q08** — §14.2's interleaved offset arithmetic with a mixed-width channel set,
and §12.1 element sizes, and §4.1. No padding anywhere in this layer, by
design.

**Q09** — §15.3's structural rows crossed with §9.7's coverage walk and
§16.2's run continuity and §20.5's compactor-regeneration paragraph. This is
the "one malformed entry, four consequences in four sections" question.

**Q10** — a reserved-range sub-record with MU = 0. Tests that a reader's
outcome (ignore-record) and the register row's outcome (reject-layer, detector
verifier) are different facts about the same record, which §21.1's closing
paragraph states and which is the single most inviting place to over-read a
register row.

**Q11** — a set ignore-lane bit. Tests §2.3's conduct-versus-bytes carve-out,
§6.3's naming of that exact case, §21.6's entry, and §21.1's normative
completeness clause (no row exists for it). Verdict must be *conforming*.

**Q12** — a slack total. Tests that §9.7's walk claims the front block and the
live trailer, that a record is not a claimant of its own header and inline
payload, and that a layer's tile-index region enters once as the layer record's
extent rather than twice. I placed every structure before the directory so that
`[R-CNT-05]`'s no-structure-after-the-directory rule is satisfied — an earlier
draft of this question put the metadata extent after the directory, which would
have made the file reject-file at file scope and destroyed the question.

**Q13** — §6.2's ordered validation. The file trips three gates; only the
earliest is established. §21.2's preamble independently confirms which two
checks precede the version gate.

**Q14** — §20.4's MU = 0 / PE = 0 drop licence, which turns on whether the
commit *independently* changes the scope the record attaches to. Superseding a
tile re-places that layer's index region and so modifies that layer's record —
a top-level record's licence — but a sub-record of a *different* layer gets no
licence from it. Two yes/no answers with opposite values, so a coin flip cannot
score.

**Q15** — §16.2's run partition for a planar layer (runs never span channel
blocks) plus the packing invariant with a sentinel in the middle of a run, plus
the register row it lands on.

## What I rejected, and why

- **Asking for the CRC-32C of a full all-sentinel segment.** §15.4 and
  Appendix B both print the constant. Pure lookup.
- **Asking for §7.4's worked example's inline_length.** Printed in the
  document.
- **Asking whether an experimental-range top-level record type with MU = 1 is
  conforming.** §21.6's "Two structural cases" paragraph states the whole
  answer in one place, including the top-level/sub-record qualifier. Lookup.
- **Asking for §21.8's instance total.** I counted it and it is correct, so the
  question would test transcription stamina, not the document.
- **A question on whether an unsorted metadata document is readable.**
  `[R-MTA-05]` states it outright in one sentence.
- **A question on the smallest conforming file.** Appendix A is the answer.
- **A question about a SHOULD.** `[R-CNF-12]` places SHOULD deviation outside
  the register; the answer would be "advisory" for every such question, which
  is a shape, not a test.
- **A question on the addressed-but-unstored tile against §21.9's 256 MiB
  row.** This is the case I believe the document does not decide (finding
  quiz-01). A question with no determinate answer indicts the key rather than
  the answerer, so it goes in the findings list instead of the slate — which is
  what the charter asks for.
- **A question on which of §18.2's two reader bounds "the bound above"
  refers to.** Same reason, weaker: it is resolvable from §21.5's preamble and
  §2.3's list, but only by a reader who thinks to go there, so it would
  manufacture a divergence about diligence rather than about the format.
  Reported as finding quiz-02.
- **A question requiring the answerer to enumerate R3's instances.** That is
  finding quiz-03's subject; asking it would be asking the answerer to ratify
  my own finding.

## Findings raised while authoring

Three, listed in the structured result: one AMBIGUITY I grade byte-level
(§21.9's per-instance quantifier over tiles, on a file that addresses tiles but
stores none), one OBSERVATION (§18.2's singular "the bound above" after two
bounds), one CONTRADICTION I grade not byte-level (§21.5's R3 Instances cell
against §21.1's stated magnitude axis, after §18.2 routed the content-size
mismatch into R3).
