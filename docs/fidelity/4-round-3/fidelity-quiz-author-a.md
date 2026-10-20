# Quiz-author transcript — edition A

## Disclosure

Context that arrived unbidden, before I read anything: a project CLAUDE.md
pointer, a user auto-memory index of prior-round note titles, and a relayed
"user request" (the single word "Go") that the harness says launched this
run. None of it is part of the specification or evidence about it; I did
not open or rely on any of it, and it needed no reconciliation with this
brief.

What I read: exactly one file,
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`,
5004 lines, read in full via six sequential Read calls (offsets 0, 600,
1200, 1800, 2400, 3000, 3600, 4200, 4599, 5000 — i.e. the whole file,
start to end, including all appendices). The path matched the brief
exactly. I did not open any other copy of this specification, any ADR,
PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md,
conformance/, spec/registry.json, or git history, and I did not list any
directory other than my own scratch directory and the (unlisted,
unread) output directory path I was given to write to.

What I ran: `ls`/`mkdir` to create my own scratch directory (it did not
exist; no prior attempt's files were present), and a handful of `grep -n`
calls against the one file I read, used only to corroborate quotations
and numeric constants I had already seen in the full Read output (not as
a substitute for reading — I read the document directly, so the
hard-wrap/line-grep hazard the brief warns about did not bite me here).
Grepped fragments and their line numbers, all confirmed present:
`entry_count × 20` (lines 1162, 2222, 3915, 3935), `0x7E000000` (lines
2552, 3957, 4240, 4626), `separate namespaces` (line 583), `F36` (lines
3635, 3790, 3899, 4048, 4094), `prospective` (lines 311, 3120),
`Deriving it there yields` (line 3857), `65,536 bytes` (lines 939, 4623),
`at least 128` / `plus 128` / `prior F plus` (lines 1304, 1335, 1337,
1377, 1402, 3402).

Files I wrote: this transcript, at
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/quiz-author-a/transcript.md`.
I did not read or list the output directory
(`/private/tmp/claude-501/.../fidelity-5/out/`) beyond writing this one
file to it as instructed.

No answers are recorded anywhere in this transcript or in the structured
return — only the 15 questions, their source sections (for my own
traceability, not given to answerers), and notes on rejected candidates.

## The slate (15 questions)

Each question stands alone for the answerer: it is handed only the
question text and a document. Source-section notes below are for the
record, not part of what an answerer sees.

1. **[Part I, §7.4 constraint table + §15.1 region layout]** A layer
   declares index_encoding 1 and entry_count = 70,000. What must
   extent_length equal — as an exact u64 value, given in hexadecimal
   (upper-case, no 0x needed stated either way, just say which you used)?

2. **[Part I, §6.4 + §6.2/§9.2 commit protocol]** Per §6.4's writer
   guidance, if a writer wants to guarantee that a single 64 KiB suffix
   fetch always captures the trailer and the directory together, what is
   the maximum dir_length (in bytes) it should keep, assuming the
   worst-case pre-trailer pad the commit protocol allows?

3. **[Part I, §2.3 reach rule (`[R-CNF-13]`) + §21.2 register]** Per
   §2.3's reach rule, exactly which rows of §21.2's file-scope register
   reach (apply to) a file declaring a format major other than 1, and how
   many total instances is that (counting each row's distinct instances
   separately, e.g. F1's two)?

4. **[Part I, §9.2 commit protocol + §6.2 trailer field rules]** A file's
   live trailer currently has committed_file_length = 1,048,576. The
   writer now performs its next commit. What is the minimum legal value
   (give it in hexadecimal) that this commit's new committed_file_length
   may take?

5. **[Part II, §11.2 grid arithmetic + §11.4 linearization]** A planar
   layer declares dimensions, in order, (y, x) with extents (1000, 2049)
   and tile extents (256, 256), and 3 channels. What is the disk ordinal
   of the tile covering tile coordinates (y = 3, x = 7) for channel index
   1 (0-based)?

6. **[Part II, §14.2 byte layout + §11.4 in-tile ordinal]** An interleaved
   layer declares channels, in order, `u` (uint32), `v` (int16), `w`
   (bool), and has tile extents (4, 4). What is the byte offset, within
   one tile's decoded image, of channel `w`'s value at in-tile coordinates
   (2, 3)?

7. **[Part II, §14.3 packed boolean planes + §13.2 fill + §14.5 padding
   content]** A planar bool channel declares fill = true (the byte
   0x01). One of its addressed, fully-stored tiles has exactly P = 20
   sample positions, every one of them a real (non-edge-padding) array
   position, and every one of those 20 real values is false. What are the
   tile's three decoded bytes, in hexadecimal, in stored order?

8. **[Part II, §17.2 lz4 cap (`[R-COD-07]`)]** A planar layer has one
   uint64 channel, and every addressed tile has P = 300,000,000 sample
   positions. The layer declares codec 4 (lz4). Is this declaration
   conforming? If not, name the outcome class and the owning scope, and
   state whether a reader can detect the violation from the layer's
   declarations alone, without fetching any tile payload.

9. **[Part II, §4.6 name rules (`[R-ENC-15]`)]** A single layer declares
   a dimension named `z` and, separately, a channel also named `z`. Is
   this a conforming layer under `[R-ENC-15]`? If it is permitted, name
   the specific textual reason (in one phrase).

10. **[Part III, §15.4 segments + §11.4 disk-ordinal formula + its
    planar-all-channel-reads note]** A planar layer has spatial-tile
    count N = 100,000 and channel count C = 4. A reader requests all 4
    channels at spatial ordinal s = 50,000. Not counting the single
    shared crc_of_crc_array check, how many *distinct* index segments
    must the reader verify at minimum to serve this request?

11. **[Part III, §21.1 detector-scope note + §21.2 row F36 + `[R-CNT-15]`]**
    A directory's top-level record sequence contains a record whose type
    field is 0x1234 (inside the reserved range 0x0003–0x7FFF) with
    MUST_UNDERSTAND = 0. Must a conforming reader reject the file because
    of this record? Separately, is the file nonetheless nonconforming,
    and if so, under which §21.2 row, what outcome class, and whose
    detector (reader or verifier)?

12. **[Part III, §20.3 step 4 permitted/forbidden changes list]** A layer
    stored at least one tile in the generation a commit supersedes. The
    commit attempts to shrink one of that layer's dimension extents (and
    change nothing else). Name the only two ways this specific change may
    legitimately be accomplished, per §20.3 step 4.

13. **[Part III, §20.4 re-emission/preservation table + its governing-flags
    paragraph]** An updater implements an unregistered record type
    (0x1234, outside §7.3's registry) according to that type's own
    external definition, which fixes MU = 0, PE = 1 for it. In the file,
    this record's stored flags happen to read MU = 0, PE = 0, and the
    updater's commit does not logically modify the record. Which flags
    govern — the stored bits, or the type's own definition — and may the
    updater drop the record from its output?

14. **[Part III, §24 conformance-vector rules (`[R-VEC-04]`)]** Per
    `[R-VEC-04]`, every conformance vector whose recorded outcome is
    reject-layer must be built inside a file that also carries what
    additional element, and what must the manifest record about that
    element?

15. **[Part III, §19.4 step 8 + §2.4 outcome-class table]** During one
    region-read request against an interleaved layer, a reader has
    already returned decoded values for several tiles earlier in that
    same request, then reaches a tile whose segment CRC fails
    verification. Per `[R-RDR-04]`: (a) what happens to the values
    already returned earlier in this same request, and (b) what happens
    to this layer for any later request in the same reader's session?

## Notable rejections

- A question computing the CRC-32C of a specific byte string by hand was
  rejected: it would require executing the exact algorithm rather than
  combining document facts, and the document already supplies the one
  check vector a reader needs — testing the check vector itself would be
  "quoting a table back."
- A question about which register rows are "strict specializations" of
  others (F1's two instances of F6/F8, F35 of F36, L24 of L25, F21 of
  F22, L10 of L11) was considered, since §21.1 states the pairing
  explicitly by name. Dropped as too close to a direct table lookup
  once narrowed to a single named pair; question 3 uses the adjacent but
  more inferential reach-rule material instead, which requires applying
  a rule rather than reading off a stated list.
- A question combining the entry_count-product overflow check (L2,
  `[R-ENC-04]`) against the extent_length-formula mismatch check (L22,
  `[R-CNT-17]`) for an entry_count at the 2⁶³−1 boundary was dropped: it
  shares its load-bearing fact (the same formula as question 1) with an
  already-slated question, risking two questions failing together for
  one reason.
- A question about `tarn.stats` staleness and whether a reader may rely
  on it was considered for the user-metadata area but dropped as too
  close to a restated definition (`[R-MTA-08]`) rather than a combination
  or application.
- No question in the final slate turned out to lack a determinate
  answer; no AMBIGUITY finding is reported against this text on that
  account.

## Findings

None beyond the disclosure above. The document determined a single
answer for every question in the slate as far as I could establish by
reading it in full; no ambiguity, contradiction, or reporter error
surfaced in the passages this slate draws on.
