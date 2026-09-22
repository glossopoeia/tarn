# Quiz-author transcript — cleanroom round 37

## Access discipline

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full (4,981 lines, read in nine sequential chunks via the Read tool,
offsets 1, 1000, 1700, 2299, 2907, 3126, 3575, 3733, 4182, 4480 — contiguous,
no gaps, no re-reads of already-covered ranges). Ran `wc -l` on that same
file once, to confirm its length before chunking (4,981 lines, matching the
brief's stated figure). No other file was opened. No `git log`/`git diff`,
no web search/fetch, no directory listing of the repository, no read of
`AGENTS.md`, `PLAN.md`, `docs/`, `conformance/`, or `spec/registry.json`.

Scratch directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/quiz-author/`
was created by me (did not exist before) and was empty when I began — no
prior attempt's files were present, so there is nothing to disclose on that
front. I did not end up writing any files into it: every arithmetic
computation needed to check a question's determinacy (grid counts, byte
offsets, extent_length formulas, run partitions, the byte-shuffle
permutation) was small enough to carry out by hand against the text, and I
deliberately avoided running the one computation that would have produced
an actual answer value (a CRC-32C over ~89 KB of repeating sentinel-entry
bytes for Q01) so as not to record an answer anywhere, per the charter's
prohibition. I did not read or list the sibling `out/` directory beyond
writing this one file to it.

## Contamination disclosure

Before this task's instructions were computed, my context already
contained: a project `CLAUDE.md` pointer to `AGENTS.md` (not read); a
user memory file (`MEMORY.md`) listing many prior-round TARN memory
entries by title (e.g. entries about the harness spec path, a lost
word-list file, repair-vs-diff bookkeeping, subagent model enforcement,
refute-phase triggers, permissions/carve-outs, closed-list exceptions,
and others); and a git-status block naming recent commit subjects,
including "Cleanroom round 37: charter, over 96e4ad4..6c9470e",
"The pre-round-37 audit of ADR-0131: two defects in three clauses, none
byte-level, both repaired", "ADR-0131: round 36's repairs — three
clauses, after a zero read on a weaker instrument", and "Cleanroom round
36: no byte-level flag, on Sonnet throughout — eight findings, eight
defects, the refute phase stood on the zero...". None of this was
solicited by me; it was present in the system reminders before I issued
my first tool call. I have not opened, searched, or otherwise consulted
any of the files those memory entries or commit subjects name, and I did
not use their content to decide what to look for, what to ask, or what
to expect the answers to be. The 15 questions below were authored solely
from close reading of `spec/tarn.md`'s own text. I am naming that this
material appeared, per the brief's instruction, without repeating or
relying on its substance beyond what is in this paragraph.

No path discrepancy: `spec/tarn.md` was exactly where the brief said it
would be; no alternate location had to be found.

## How the slate was built

I read the whole document once, start to finish, taking the three named
changed passages (§3.3, §20.3, §20.4) and the five described decisions
(the layer-drop/sub-record rule of §20.4; the two-flags-not-orthogonal
Note of §7.2 plus the no-embedded-offsets exception it states for the
layer record; the rewriter/creator choice of §20.1; the "fixed
declarations" bar of §20.3 step 4; and the registry/table material the
brief points at) as the sections to read hardest, then read the rest of
the document (container framing, checksums, lifecycle, geometry, sample
types, fill, serialization, tile index, slabs, codecs, filters, user
metadata, the reader/writer/updater algorithms, the error register, the
security/privacy sections, and every appendix including the fully
worked minimal-file and layer-record examples) at the same level of
attention, per the instruction not to read a clean passage as a checked
one.

I did not attempt to guess or re-derive what changed between rounds —
no diff was available to me and using outside knowledge of the round's
history (even the little that leaked into context unsolicited) to aim
the slate would be exactly the contamination the access rule exists to
prevent. Instead I weighted the slate toward the sections the brief
named as newest (§3.3, §20.3, §20.4) while spending real effort on
adjacent machinery those sections depend on (§7.2's record framing,
§7.4's layer-record layout, §11–§15's geometry/tiling/index arithmetic,
§14/§17's byte layout and codec/filter rules, §21's register) because a
correct answer to a §20.x question about what a commit or a rewrite may
do routinely turns on a definition sitten two sections away.

## Design choices and what I rejected

- Every question is self-contained: each states its own scenario (layer
  declarations, flag values, byte contents) rather than pointing back at
  a worked example already in the document, because asking about an
  example verbatim would be "quoting a table back" rather than requiring
  the answerer to apply a rule to a new case.
- I rejected several draft questions that reduced to a single register-row
  lookup with no second ingredient (e.g., "what is the sentinel entry's
  byte pattern" — pure recall of one constant; "what codec values are
  reserved" — pure recall of one range). Every question below needs at
  least two rules, or a rule plus arithmetic over invented declarations,
  or an application of a definition to a constructed edge case.
- I rejected a question built around RFC 8878's Single_Segment_Flag
  interaction with content-size presence, because settling it would have
  required importing knowledge of the external zstd spec beyond what
  `[R-COD-06]`/§18.2 state outright — the document gestures at that
  derivation in a Note but does not fully pin the case I wanted to ask
  about, so the "single determinate answer from this document alone"
  bar was not clearly met. I replaced it with a window-size-vs-decoded-
  size question (Q12) whose answer follows from `[R-COD-06]`'s stated
  text alone, independent of that RFC subtlety.
- I rejected a question asking directly "does dropping a layer strand its
  sub-records," because the answer is stated almost verbatim in §20.4's
  own paragraph — I replaced it with Q09, which forces the answerer to
  identify *which* of two co-present sub-records is the one that blocks
  a drop (only the unimplemented MU=1 one; a PE=1 user-metadata
  sub-record does not itself block a layer drop), which cannot be
  answered by quoting one sentence.
- I rejected two arithmetic drafts (a second tile-index segment-count
  question, and a second inline_length computation) as redundant with
  Q01/Q05/Q07/Q06 respectively, in favor of covering more distinct
  mechanisms (slab-run partition, byte-shuffle permutation, zstd window
  bound) once each, per the instruction not to ask two questions that
  fail together for the same reason.
- Before finalizing, I checked every question's answer for
  determinacy by working it by hand against the cited rules; none came
  up indeterminate, so I have no indeterminate-question finding to
  report. I record no candidate answers here or elsewhere, per the
  charter.

## The slate (15 questions)

See the structured result for the canonical text; summarized here for
the record, with the section(s) each draws on and why each earns its
place:

1. **Q01** (§15.1, §15.4) — partial vs. full tile-index segment CRC
   (byte-level: the stored CRC-32C value; forces recognizing that the
   all-sentinel shortcut constant applies only to a *full* 2¹⁶-entry
   segment, never a partial one).
2. **Q02** (§11.2, §11.4, §14.2) — byte offset of one channel's value
   inside a decoded interleaved tile image, for an invented 2-D layer
   and coordinate (arithmetic chaining grid math, in-tile ordinal, and
   sample-stride offset arithmetic across three sections).
3. **Q03** (§14.2, §17.2/`[R-COD-07]`, §2.4) — lz4's decoded-size cap
   tested against a planar layer's *largest* channel plane; the point is
   the outcome's scope (whole layer, not just the offending tile) and
   that other layers are unaffected.
4. **Q04** (§6.3/`[R-CNT-08]`, §21.2 F19) — an incompat-lane bit set on a
   file whose version_major this reader implements; tests that "this
   text defines no flag bits" makes *every* incompat bit unimplemented,
   independent of version_major.
5. **Q05** (§7.4, §21.3 L22/`[R-CNT-17]`) — extent_length arithmetic
   from a stated entry_count.
6. **Q06** (§16.2/`[R-SLB-02]`) — slab run partition arithmetic: how many
   ordinals the final, necessarily-shorter run covers.
7. **Q07** (§7.4) — full inline_length computation for an invented
   planar 2-channel, 2-dimension layer record, entirely by table
   arithmetic (not a lookup of the document's own worked example, which
   uses different declarations).
8. **Q08** (§20.3 step 4) — whether an appender may change only a
   channel's fill value on a layer that already stores a tile; tests
   that fill is on the *fixed*, not the *permitted*, side of that
   step's list.
9. **Q09** (§7.2's Note, §20.4's table and paragraph) — which of two
   co-present sub-records (a PE=1 user-metadata one, an unimplemented
   MU=1 one) blocks a layer drop.
10. **Q10** (§7.2's Note, §7.3/`[R-CNT-15]`, §21.2 F25) — an
    experimental-range top-level record stored MU=1/PE=0: separates
    "is the file conforming" (no — F25) from "what does an ordinary
    reader do" (reject-file regardless, unchanged by the illegal
    combination).
11. **Q11** (§14.2, §17.3/`[R-COD-10]`) — byte-shuffle applied to a
    2-channel interleaved tile's decoded image; produces an exact
    6-byte output sequence.
12. **Q12** (§17.2/`[R-COD-06]`, §21.9) — a zstd tile whose declared
    Window_Size sits inside §21.9's 8 MiB reader-guarantee floor but
    still exceeds *this tile's own* decoded size; tests that those are
    two different bounds and the tile-scope one governs.
13. **Q13** (§3.3's Note, §20.5) — whether a rewriter may *re-create* a
    layer (as opposed to carrying it forward) without decoding it; tests
    that the Note's "operate on files whose layers they cannot decode"
    licenses only the carry-forward path.
14. **Q14** (§7.2, §20.5) — whether a rewriter implementing a
    hypothetical future MU=1 registered type that carries its own file
    references may relocate what that type references during a
    compaction.
15. **Q15** (§20.1, §20.4) — classifying a tool that reads and fully
    decodes an existing file but writes flags=0 and drops the input's
    user-metadata record outright: creator, not rewriter, and therefore
    free of §20.4's preservation table.

## Findings hit while authoring

None met this charter's bar for a reportable AMBIGUITY, CONTRADICTION,
or OBSERVATION with a defensible byte-level verdict and a verbatim
quotation. I looked specifically at the mechanics the brief flagged
(the layer-drop/sub-record interaction, the two-flags-not-orthogonal
Note, the rewriter/creator choice, the §20.3 step 4 bar, and the
table/Note/Example material naming an actor by class versus by tier)
and did not find an internal inconsistency I could quote and defend
without relying on knowledge of what changed between rounds, which I do
not have and did not seek out. No question in the slate turned out
indeterminate once checked against the text, so there is no
indeterminacy finding either.
