# Quiz-author transcript — edition B

## Disclosure

**Path discrepancy.** The brief calls me the quiz author for "edition B" and
tells me my access rule is to read exactly one file, named at
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md`
— note the path segment is `editions/c`, not `editions/b`. I read exactly
that file, at exactly that path, and inferred nothing from the mismatch
between the path's own label and my assigned role. I did not open, look
for, or infer the contents of any other edition, including one that might
be at an `editions/b/tarn.md` path. I am reporting the discrepancy as
required; I did not try to resolve it myself.

**What I read.** I read the single file named above in full (4,885 lines,
296,597 bytes), via `cat -n` / `sed -n` over the file in ranges (never
using a line-oriented `grep` to search for wrapped phrases — no such
search was needed since I read the file in full sequential ranges). I ran
no command that reads any other file in the repository. I ran one local
Python script, in my own scratch directory, that reads no files — it only
does arithmetic to check my own candidate answers (grid/tile arithmetic,
disk-tile-ordinal arithmetic, a byte-shuffle-filter worked example, a
decoded-tile-size computation, and the tile-index `extent_length`
formula). That script and its output are not repeated here since the
charter says not to record my own answers; I used it only to confirm each
question I kept has a single determinate answer before including it.

**Unsolicited context.** My runtime context, before I began, included a
`CLAUDE.md` project-instructions pointer, an auto-memory index of prior
session notes about this same project (titled things like "TARN harness
spec path", "TARN repair prose vs rules", "TARN post-G3 readable-edition
process", etc.), and a git-status block naming several recent commit
subjects. None of this is part of the specification, none of it is
evidence about the specification, and I disregarded all of it in
authoring the slate below. I am naming that it appeared, per the brief,
without repeating its contents or acting on anything in it.

**Scratch directory.** My scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/quiz-author-b/`)
was empty when I started — no prior attempt's files were present. I wrote
one file there, `verify.py`, used only for the arithmetic checks
mentioned above.

I did not read or list the shared output directory
(`fidelity-2/out/`) beyond writing this one file to it.

## How I read the document

I read Part 0 and Part I (Preliminaries and Container, §1–§10) in full,
then Part II (Array Model, §11–§18) in full, then Part III (Behavior,
§19–§24) in full, then the non-normative appendices (A–H) for
orientation only (I did not draw any question's determinacy from
appendix text alone — Appendix A's worked file and Appendix G's profile
were read only as a sanity check against the normative sections they
restate).

## Slate design

The brief asks for 15 questions: ≥3 from Part I, ≥3 from Part II, ≥3 from
Part III, and ≥4 whose answer turns on a prose rule (a carve-out, an
exception, a quantifier, a keyword) rather than a table read-off. My
final slate is 4 Part I / 7 Part II / 4 Part III = 15, and 8 of the 15
turn on a prose rule rather than a bare table lookup (I erred toward more
than the floor on both axes, since several natural container/geometry
questions turn out to double as prose-rule questions once built out with
a concrete case).

I deliberately built each question around a *concrete scenario* — actual
field values, actual geometry, actual byte patterns — rather than asking
for a definition or a table cell, per the charter's warning against
"quotes a table back" questions. Several questions require doing the
document's own arithmetic (ceiling-division grid counts, the disk-tile
ordinal formula, the tile-index `extent_length` formula, the
byte-shuffle permutation, a decoded-tile-size computation) before the
rule can even be checked, which is what makes them byte-level rather
than definitional.

I also tried to avoid clustering: several questions above the floor
(Q8/Q9/Q10 in my working numbering, all "does this concrete layer-record
combination violate a rule, and which register row") are structurally
similar in *shape* but each hinges on a different specific constraint
(alignment/slab mutual exclusion; fill-length-vs-element-size; the
`entry_count`/extent-slot arithmetic cross-check), so a wrong answer to
one does not imply a wrong answer to another for the same reason.

## What I rejected

- **A pure CRC-32C table-lookup question** ("what is CRC-32C of the
  9-byte check vector / of zero bytes") — this is exactly the kind of
  table-quoting question the charter warns against; the answer sits in
  one place in §4.5 with no second place to combine it against.
- **A registry-table lookup** ("which codec ID is zstd") — same reason.
- **A `version_minor`-floor question for an appender.** I drafted:
  "An appender's input trailer has `version_minor = 3`; the commit adds
  no feature needing a minor above 0 — what value MUST the output
  trailer's `version_minor` carry?" On closer reading, `[R-CNT-26]`
  states the floor-and-carry rule as a **SHOULD**, not a MUST: "A writer
  SHOULD emit the lowest version_minor that defines every feature
  present in the file … and an appender the maximum of that floor and
  the prior trailer's minor." Because writer conformance is semantic
  (`[R-CNF-05]`: two conforming writers given identical input MAY
  produce different conforming files), and this specific rule is
  advisory rather than a MUST-level file-conformance requirement, a
  conforming appender is not in fact forced to emit any particular
  `version_minor` value here — so the question as drafted has no single
  answer a file's conformance turns on. I replaced it with a question
  about the ignore-lane flags carry-forward rule (`[R-CNT-08]`), which
  *is* MUST-level ("An updater MUST copy forward unknown ignore-lane
  bits of its input file, MUST NOT clear them, and MUST NOT set any
  other") and yields an exact required hex value. I record the rejected
  `version_minor` question as an AMBIGUITY finding (quizb-01) below,
  since it is a genuine soft spot in the text for anyone trying to build
  a determinate conformance question on it, even though it is not a
  defect in the specification's own logic (SHOULD is a deliberate,
  clearly-marked choice here, not an oversight).
- **A question about which commit "shape" (§20.3's (a)/(b)/(c)) a given
  edit produces.** I found this genuinely determinate but decided it
  would duplicate the reasoning tested by my rewrite-regeneration
  question (Q13 below) too closely — both turn on "does the tile-index
  region get re-emitted" — so I kept only one.
- **A question about `tarn.stats`/`tarn.axes` shape validity.** These are
  explicitly advisory/non-structural (`[R-MTA-07]`, `[R-MTA-08]`) and a
  malformed one never affects file conformance at all — it is a
  correctly *negative* case (nothing to check byte-for-byte against) and
  would not "produce, if answered wrongly, a file two implementations
  disagree about," so I dropped it as insufficiently pointed for this
  slate, not as a defect in the document.

## The slate (no answers recorded)

1. A conforming-looking TARN file has a trailer whose magic, CRC, and
   version gate all validate correctly, whose file_id, reserved bytes,
   and flags are all valid, and whose `committed_file_length` field
   equals 320, matching the transport-reported physical file size
   exactly. The same trailer's `dir_offset` field is 200 and its
   `dir_length` field is 60. Under the trailer's remaining
   field-validation rules, does this trailer pass validation? If it
   fails, name the exact register-row identifier (e.g., "F12") for the
   specific defect, and state the reader outcome (name the outcome
   class).

2. A remote reader opens a TARN file by issuing a single speculative
   suffix-range request for the file's final 500 bytes of a much larger
   file; the response does not include byte offset 0 of the file. The
   fetched trailer and directory both validate successfully by every
   rule that applies to them. Is this reader obligated, before any other
   processing, to verify the 16-byte front signature block by byte
   equality? Answer yes or no, and name the requirement identifier that
   decides the answer.

3. A TARN file's directory contains a single top-level record whose type
   field is 0x0050 and whose MUST_UNDERSTAND flag bit is set to 1
   (PRESERVE_ON_EDIT is also set to 1, so the flag combination itself is
   not separately defective). No record type 0x0050 is one this
   specification assigns. What reader outcome applies to this file (name
   the outcome class), and which register-row identifier documents this
   exact condition?

4. An appender opens an existing TARN file whose live trailer has
   `flags = 0x00010000` (bit 16 set; every other bit, including every
   bit of the incompat lane, is 0). This specification's text defines no
   meaning for bit 16. The appender's commit adds no feature that
   requires any flag bit to be set. What exact 32-bit value, in hex,
   MUST the appender's new trailer's `flags` field carry?

5. A layer is declared with rank 3, dimensions of extents (500, 0, 10)
   and tile extents (64, 8, 4) respectively, interleaved channel layout,
   and 5 channels. What value MUST this layer's `entry_count` field
   equal?

6. A layer has planar channel layout with 2 dimensions whose grid counts
   (number of tiles along each axis) are G0 = 5 and G1 = 3, and it has 4
   channels (channel indices 0 through 3). Under linearization 1
   (row-major), what is the disk tile ordinal — i.e., the zero-based
   tile-index entry number — of the tile carrying channel index 3 at
   tile coordinates (t0, t1) = (2, 1)?

7. An interleaved layer has exactly two channels declared in order:
   channel `a` of type uint16, then channel `b` of type uint8. One tile
   of this layer has exactly two sample positions, with in-tile ordinals
   0 and 1. Before any filtering, at in-tile ordinal 0 channel `a` has
   the bit pattern 0x0102 and channel `b` has the bit pattern 0xAA; at
   in-tile ordinal 1, channel `a` has 0x0304 and channel `b` has 0xBB.
   This layer declares filter 2 (byte-shuffle) and codec 1 (none). List
   the tile's stored bytes, in order, as a sequence of six uppercase hex
   byte-pairs separated by spaces.

8. A layer record declares a nonzero per-tile alignment A = 1024
   together with a nonzero slab run length S = 50 and a slab alignment
   A_slab = 4096 (itself a valid power of two in range). Is this
   combination of declarations a validity error? If so, name the
   register-row identifier and the resulting reader outcome (name the
   outcome class).

9. A layer declares a channel of sample type uint32 (a numeric type with
   a 4-byte element size). That channel's entry, as parsed from the
   layer record, gives a fill field with a length prefix of 2 (i.e.,
   only 2 bytes of fill data follow). Is this a validity error? If so,
   name the register-row identifier and the resulting reader outcome.

10. Under index_encoding 1, a layer record declares `entry_count = 12`
    but an extent slot of (0, 0). Is this combination a validity error?
    If so, name the register-row identifier and the resulting reader
    outcome.

11. During an appender's commit, one of a layer's existing tile-index
    entries is not touched by the commit (the tile it addresses is
    neither superseded nor newly stored) — call it entry E. Entry E's
    own 20 bytes are well-formed under §15.3's classification
    (non-sentinel, offset ≥ 16, both fields in the valid domain, no
    overflow, extent within bounds), but the bytes at the extent entry E
    addresses fail entry E's own crc field. When the appender re-emits
    this layer's tile-index region, what MUST it do with entry E's 20
    bytes? And separately, when a reader later requests the tile entry E
    addresses, what outcome does that read report (name the outcome
    class)?

12. A reader issues one region request against an accessed planar layer,
    covering two channels (`temp`, channel index 0, and `mask`, channel
    index 1) across several spatial tiles. Of all the tile-index entries
    the request needs, exactly one — the entry for channel `temp`'s tile
    at one particular spatial tile — fails verification of its stored
    bytes against its crc field (a structurally well-formed entry; only
    its stored bytes' checksum fails); every other needed entry, across
    both channels and every other spatial tile the request covers,
    verifies and decodes without incident. Which of the following most
    narrowly and correctly describes what the reader is barred from
    returning: (a) only `temp` channel's data at that one spatial tile;
    (b) both channels' data at that one spatial tile; (c) all of `temp`
    channel's data across every spatial tile the request covers; (d) the
    entire request, including `mask` channel and every other spatial
    tile? Answer with the single letter.

13. A rewriter is compacting a TARN file. In doing so it must regenerate
    one layer's entire tile-index region, because some of that layer's
    stored extents are being relocated. Among that layer's existing
    tile-index entries is one entry that §15.3 classifies as
    reject-tile on a *structural* ground (for example, its offset and
    length fields are inconsistent with the sentinel pattern) — meaning
    the entry addresses no usable stored extent at all. List, as a short
    ordered list, the only two dispositions available to the rewriter
    for this situation (i.e., the only two things it is permitted to
    do), per the specification's own text.

14. An interleaved layer declares two channels, both int32 (4-byte
    element size each), and tile extents (128, 128) — so P = 16,384
    sample positions per tile. This layer declares codec 3 (zstd). One
    of its stored tiles' zstd frame header declares (via a
    Window_Descriptor) a Window_Size of 1,048,576 bytes. Is this tile's
    frame a validity error under the codec's declared-window rule? If
    so, name the register-row identifier, the resulting outcome class,
    and whether the detecting actor is the reader or the verifier.

15. A layer's tile index has `entry_count = 131,072`, giving two
    segments: segment 0 (entries 0 through 65,535) and segment 1
    (entries 65,536 through 131,071) — each covering exactly 65,536
    entries. Every entry in segment 0 is the sentinel. In segment 1,
    every entry is the sentinel except for exactly one, which is a
    non-sentinel (stored-tile) entry. May the writer, for segment 1,
    emit the stored constant `0xEECB3BB2` as its segment-CRC-array value
    instead of computing the real CRC-32C over segment 1's actual entry
    bytes? Answer yes or no, and name the requirement identifier that
    decides the answer.

## Coverage check against the charter

- Part I (container, §5–§10): Q1, Q2, Q3, Q4 — 4 questions.
- Part II (array model, §11–§18): Q5, Q6, Q7, Q8, Q9, Q10, Q15 — 7
  questions.
- Part III (reading/writing/updating/register, §19–§24): Q11, Q12, Q13,
  Q14 — 4 questions.
- Prose-rule questions (carve-out, exception, quantifier, or keyword,
  not a bare table cell): Q2 (residency — a quantifier over what bytes
  are "resident"), Q4 (the ignore-lane carry-forward keyword rule), Q5
  (the "extent 0 ⇒ grid count 0" carve-out propagating through a
  product), Q8 (the "mutually exclusive" keyword between alignment and
  slab), Q11 (the "entry is well-formed; the defect is in the bytes it
  addresses" carve-out), Q13 (the "no stored extent to re-point, so only
  two dispositions" carve-out on rewriting), Q14 (the quantifier
  distinguishing "exceeds the tile's declared decoded size" — always a
  violation — from "exceeds the reader's own resource bound" — never
  one), Q15 (the conjunction "full segment" AND "all sentinel," not
  either alone) — 8 questions.

No question records my own answer anywhere in this transcript or in the
structured result.
