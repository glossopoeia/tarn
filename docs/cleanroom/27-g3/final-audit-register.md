# Register Auditor Transcript

## Disclosure of unrequested context

Before I did anything, my system context already contained: a CLAUDE.md
project-instruction pointer, the user's email, today's date, a git status
block naming the branch "main" and five recent commit subjects (mentioning
"ADR-0111", "the generation counter is removed", "a struck row label
retired", "ADR-0109 repair audit", etc.), and a long list of available
skills/tools. None of this is part of the specification and none of it is
evidence about it. I did not use any of it to form a judgment about the
change — I derived everything below from spec/tarn.md and my nine assigned
hunk files. I note, per instructions, only that it appeared, and mention it
no further.

## What I read

- `/private/tmp/.../case-final/hunk-17.diff` through `hunk-24.diff` and
  `hunk-27.diff` (the nine hunks named in my charter) — full contents, via
  the Read tool.
- `spec/tarn.md` in full-section sweeps, via `sed -n` over the following
  line ranges (all via Bash, no other files touched, directory never
  listed): 94–180 (§2.1–2.2 Conformance / requirement identifiers), 360–400
  (glossary: generation), 800–930 (§6.2–6.4 trailer layout, remote open),
  1222–1360 (§9.1–9.3 lifecycle/commit protocol/generations), 1440–1520
  (§9.7 coverage verification), 3341–3480 (§20.5 compaction), 3470–3900
  (§21.1 through §21.8 in full, including the full §21.2/§21.3/§21.4/§21.5
  register tables), 4140–4210 (§23.3 lead-in / §24 opening through the
  R-VEC-02 paragraph), 4250–4340 (Appendix A worked byte example, Appendix
  B constants table), plus targeted `grep -n` sweeps listed below.
- I did not read full.diff, any hunk outside my nine, docs/, PLAN.md,
  OPEN-QUESTIONS.md, AGENTS.md, or any git history. I ran no git commands.
  I wrote to no file in the repository; my only write is this transcript.

## Header-vs-body verification

For each of the 9 hunks I located the post-change text in the current file
with `grep -n` and compared the reported line range to the header's claim.
All 9 headers matched the body within the expected tolerance (the header
documents state it is derived from the first changed line, not the hunk's
`@@` start):

- hunk-17: claimed 3509–3516; `F1's front-block instance` found at 3512,
  `at a given instance of it` at 3509 — matches.
- hunk-18: claimed 3569; `#### 21.2 File-scope violations` at 3567,
  "35 conditions" one line below — consistent with a single-line hunk
  landing just after the heading.
- hunk-19: claimed 3580; F2 row is the second row of the table starting
  3578 — consistent.
- hunk-20: claimed 3589–3592; F12–F16 rows verified at 3589–3593 in
  current file — consistent (F11 row deleted, so F12 begins here).
- hunk-21: claimed 3615–3620; `Row label F11 is struck` found at 3615 —
  matches.
- hunk-22: claimed 3823–3829; `immutability and the strict growth` found
  at 3823 — matches.
- hunk-23: claimed 3862–3868; `the unknown ignore-lane bits` region
  located in that span — matches.
- hunk-24: claimed 3878; `Every row of §21.2 through §21.5 — 120
  conditions over 275` found at 3878 — matches.
- hunk-27: claimed 4189–4193; `a row label is never renumbered` found at
  4189 — matches.

No header/body mismatches found.

## Full-arithmetic recount of §21.8's totals (hunk-24)

§21.1 states the counting rule I must apply: instances are semicolon-
separated items in the Instances cell, and a cell reading "—" counts as
one instance (the smallest legal member — a single predicate over several
fields — is still one distinguishable file).

I counted every row's Instances cell by hand, section by section, reading
directly from the current file's tables (not the hunks — the hunks only
touch a few rows; §21.3, §21.4, §21.5 are untouched by any of my 9 hunks,
so counting them serves as the "reproduce a total believed unchanged"
validation the charter asks for before trusting the changed section).

### §21.2 (F-rows, touched by hunks 18–20) — 35 conditions (F1–F36 minus
struck F11)

F1=2, F2=5, F3=2, F4=1, F5=2, F6=2, F7=4, F8=1, F9=1, F10=1, F12=1, F13=1,
F14=1, F15=1, F16=1, F17=2, F18=1, F19=1, F20=1, F21=1, F22=1, F23=2,
F24=1, F25=1, F26=1, F27=1, F28=2, F29=3, F30=2, F31=1, F32=1, F33=5,
F34=1, F35=1, F36=1.

Running sum: 2,7,9,10,12,14,18,19,20,21,22,23,24,25,26,28,29,30,31,32,33,
35,36,37,38,39,41,44,46,47,48,53,54,55,56.

**§21.2 total = 35 conditions, 56 instances.**

### §21.3 (L-rows, untouched by any of my hunks) — 49 conditions (L1–L49)

L1=8, L2=9, L3=1, L4=2, L5=1, L6=1, L7=2, L8=2, L9=2, L10=1, L11=1, L12=2,
L13=1, L14=3, L15=4, L16=2, L17=2, L18=3, L19=1, L20=1, L21=4, L22=4,
L23=4, L24=1, L25=1, L26=1, L27=1, L28=1, L29=3, L30=2, L31=3, L32=3,
L33=4, L34=4, L35=1, L36=2, L37=1, L38=1, L39=3, L40=1, L41=3, L42=1,
L43=3, L44=3, L45=3, L46=2, L47=2, L48=1, L49=4.

Running sum lands at **116 instances** (checked twice).

**§21.3 total = 49 conditions, 116 instances.**

### §21.4 (T-rows, untouched) — 26 conditions (T1–T26)

T1=1, T2=1, T3=6, T4=4, T5=1, T6=1, T7=2, T8=1, T9=1, T10=1, T11=2, T12=1,
T13=2, T14=6, T15=2, T16=1, T17=1, T18=2, T19=1, T20=1, T21=3, T22=6,
T23=1, T24=1, T25=3, T26=3.

Running sum lands at **55 instances**.

**§21.4 total = 26 conditions, 55 instances.**

### §21.5 (R-rows, untouched) — 10 conditions (R1–R10)

R1=4, R2=2, R3=2, R4=16 (8 named alternatives × {top-level, layer
sub-record} = 16), R5=8, R6=4, R7=6, R8=2, R9=2, R10=2.

Sum: 4+2+2+16+8+4+6+2+2+2 = **48 instances**.

**§21.5 total = 10 conditions, 48 instances.**

### Grand total

Conditions: 35 + 49 + 26 + 10 = **120**.
Instances: 56 + 116 + 55 + 48 = **275**.

This is an exact match to hunk-24's new text: "120 conditions over 275
instances." I independently rebuilt this number from the live tables, not
from the hunk's own arithmetic.

### Validating against the pre-change total (121 / 277)

I do not have the old file, but I do have the two rows the diffs changed.
Deleted row F11's Instances cell was "generation" — 1 instance, and it was
1 whole condition. F2's old Instances cell (from hunk-19's `-` line)
carried an extra "generation" item versus the new cell, i.e. 6 instances
vs. today's 5. So the delta from old to new is exactly: conditions
121 → 120 (−1, the struck F11 row), instances 277 → 275 (−1 for F11's own
instance, −1 for the dropped "generation" item inside F2). That is
precisely hunk-24's stated before/after (121/277 → 120/275). The two
independent routes (direct recount of the current tables; delta arithmetic
from the diff's own before-text) agree exactly.

## §21.1's specialization clause (hunk-17) — deriving each named pair

The rule the hunk adopts: a file may exhibit two register rows' conditions
at once; where every file satisfying the narrower row's condition (at a
given *instance* of that row, since a row may enumerate several) also
necessarily satisfies the broader row's condition, the file is filed under
the narrower row only. The hunk's correction versus the pre-image is to
attach this per-*instance*, because F1 has two instances (front-block,
trailer-magic) that specialize two *different* rows, and the old text's
flat "F1 of F6 and of F8" wrongly implied either instance implied both.

I derived each of the six pairs the new sentence names, from the current
§21.2/§21.3 table text (read above), not by trusting the label:

1. **F1's front-block instance ⇒ F6.** F1(front) = "signature constant
   stored byte-reversed" at front bytes [0,8). F6 = front 16-byte block
   "not byte-identical to the constant." A byte-reversed 8-byte magic
   differs from the correct constant (the magic `89 54 41 52 4E 0D 0A 1A`
   is not its own byte-reversal), so F1(front) ⇒ F6. Holds. Distinguishing
   file: any front-block corruption that is *not* an exact byte-reversal
   (e.g. a single flipped bit) satisfies F6 but not F1 — confirms F6 is
   strictly broader.
2. **F1's trailer-magic instance ⇒ F8.** Same argument at F−64: reversing
   `8A 4E 52 41 54 0D 0A 1A` yields a different 8 bytes, so F1(trailer) ⇒
   F8 (trailer magic wrong). Holds. Does *not* imply F6 (different byte
   range), and F1(front) does *not* imply F8 — confirming the hunk's
   correction (splitting the old flat claim) was necessary and is now
   accurate.
3. **F35 ⇒ F36.** F35 = reserved-range top-level type with MU=1. F36 =
   reserved-range top-level type, any MU. F35's condition set is a strict
   subset of F36's (MU=1 is one of two MU values). Holds. Distinguishing
   file: reserved-range type with MU=0 satisfies F36, not F35.
4. **L24 ⇒ L25.** Same shape as (3) at layer-sub-record scope. Holds by
   identical argument.
5. **F21 ⇒ F22.** F21 = top-level user-metadata record, extent slot
   (0,0). F22 = top-level user-metadata record, extent_length < 5. Slot
   (0,0) means extent_length = 0, which is < 5, so F21 ⇒ F22. Holds.
   Distinguishing file: extent_offset = 100 (nonzero), extent_length = 3
   satisfies F22 (length < 5) but not F21 (slot isn't (0,0)) — confirms F22
   strictly broader, and confirms this case is not instead caught by the
   half-zero row F30 (neither field is zero here, so F30/F21 do not
   apply, only F22).
6. **L10 ⇒ L11.** Same shape as (5) for a layer sub-record's user-metadata
   extent. Holds by identical argument.

All six hold. The list is explicitly non-closed ("not offered as closed"),
so I did not need to find a seventh to prove completeness — only that the
six actually asserted are true, which they are.

## §21.7's rewording (hunks 22–23) — citation check

Changed clause: "Committed-prefix immutability and the strict growth of
`committed_file_length` across the commits of one file_id (`[R-LIF-01]`,
`[R-LIF-02]`)... and no field of a file records how many commits that
history holds."

I opened each cited rule at its home section:

- `[R-LIF-01]` — §9.1: "Bytes in [0, F)... are immutable... every
  conforming mutation of a file is either a commit... or a whole-file
  rewrite... `[R-LIF-01]`." This *states* committed-prefix immutability.
  Correct citation.
- `[R-LIF-02]` — §9.2, end of the six-step commit protocol paragraph: "A
  commit's committed_file_length is strictly greater than the prior
  trailer's, by at least 128, so the committed file length orders a
  file's generations (§9.3). `[R-LIF-02]`." This *states* the strict
  growth. Correct citation, and correct choice over the old citation.
- The pre-image cited `[R-LIF-03]` instead. I opened `[R-LIF-03]` at §9.3:
  "Within one file_id, F strictly increases per commit — by at least 128
  (`[R-LIF-02]`)... `[R-LIF-03]`." §9.3's own text cites R-LIF-02 as the
  source of the strict-increase fact and uses it downstream for cache
  revalidation — i.e. R-LIF-03 *consumes* the property, it does not
  *state* it. The hunk's citation swap (R-LIF-03 → R-LIF-02) is therefore
  the correct fix the charter warned to check for, not a new defect.
- "no field of a file records how many commits that history holds" is
  verbatim consistent with §9.3's own Note: "F counts bytes, not commits.
  ... how many commits a file has undergone is not recoverable from the
  live trailer, and no field records it," and with §9.7's closing Note:
  "Nothing here enumerates prior commits." Both checked and both agree.

Changed clause (hunk-23): "§20.5's three obligations on a compacted
file's trailer (`[R-WRT-06]`) — its fresh `file_id` draw, the unknown
ignore-lane bits it MUST carry forward, and the floor its version_minor
SHOULD take." I read §20.5 in full (lines 3341–3436). It states exactly
three trailer obligations on a compactor once the generation-field
obligation is gone: (1) mint a fresh file_id, (2) copy forward unknown
ignore-lane bits, (3) version_minor floor (SHOULD at least the input's,
else `[R-CNT-26]`'s floor). No fourth obligation (no "generation" write)
appears anywhere in §20.5 — confirmed by grepping the whole file for
"generation" (below) and finding no compaction-trailer obligation
referencing it. "Three" is correct.

The "(`[R-WRT-06]`)" citation for all three, including the file_id draw,
predates this hunk (present unchanged in both the `-` and `+` text) — I
checked it anyway per Check 2. §20.5's own text puts the R-WRT-06 bracket
only at the end of the ignore-lane/version_minor/MU=1-refusal paragraph,
not at the end of the file_id paragraph, which looked at first like a
mismatch; but three other untouched passages in the document (lines 4148,
4463, 4537-4538) independently call the fresh-file_id draw "R-WRT-06's,"
so R-WRT-06 evidently is the umbrella identifier for the whole §20.5
compactor-trailer paragraph pair. This citation was not touched by the
audited hunk and is not a defect it introduced — recorded as a considered
and rejected candidate below.

"For the last two there is a second [reason]" — checked that this still
correctly refers to (ignore-lane bits, version_minor) after "generation"
was deleted from the middle of the enumerated list: it did before the
edit too (the pre-image's four items were file_id, generation, ignore-lane,
version_minor; "last two" already meant ignore-lane/version_minor, not
generation/version_minor). Deleting the middle item does not disturb this
referent. No stale reference.

## F11 retirement (hunk-20, hunk-21) vs. §2.2's model, and vs. §24 (hunk-27)

- §2.2 (current file, lines 116–121): requirement identifiers "are never
  renumbered or reused, a withdrawn requirement leaves its identifier
  permanently retired." This governs `[R-XXX-NN]` identifiers specifically,
  a different namespace from §21's row labels (F#/L#/T#/R#).
- The hunk-21 Note explicitly borrows this "on the model" — i.e. as a
  deliberate analogy, not a claim that §2.2 already governs row labels.
  Governing verbs compared side by side: §2.2 "are never renumbered or
  reused... retired permanently" vs. the Note "is retired... never
  renumbered, never reused" — same three verbs, consciously reused, over
  a different noun. This is a legitimate documentation-precedent analogy,
  not a logical leap presented as entailment.
- Because this text sits inside a `> **Note.**` block, it is
  non-normative under the document's own rule (§2.1: normative except
  Note/Example/Rationale). I checked whether the substantive claim — "row
  labels never renumber" — therefore has no force anywhere: it does not
  rest solely on the Note. Hunk-27 independently restates the same
  substance in plain (non-blockquoted) §24 prose: "a row label is never
  renumbered and never reused, so it denotes one condition for the life of
  format major 1, exactly as §2.2 makes the identifier permanent" — this
  is normative text, inside the paragraph ending `[R-VEC-02]`, which I
  confirmed by reading lines 4167–4200 directly (no `>` prefix). So the
  claim has normative force via §24 independent of the Note. I record the
  Note's non-normative placement as a considered-and-rejected candidate
  below, since a row-label-permanence fact has no byte-level or
  reader/writer-facing consequence either way (it governs how the
  register/vector corpus are built, not what bytes a conforming file may
  contain), so even a hypothetical implementer "ignoring" it changes
  nothing checkable.
- Swept for stale renumbering claims: `grep -n
  "renumber\|positional\|struck\|retired\|retire"` over the whole file
  (10 hits, shown below) — the only "renumber" hits outside my hunks are
  about requirement-identifier numbering (R-ENC-100, unrelated) and about
  *tile ordinals* renumbering under a geometry change (§20.3/`[R-GEO-06]`,
  lines 1619 and 3120 — a completely different kind of "renumbering," tile
  addressing order, not register-row labeling). No leftover claim that
  register row labels are positional/renumber.
- Swept for reuse or dangling reference to the struck label: `grep -n
  "\bF11\b"` — one hit only, the retirement Note itself. F11 is not
  reused and nothing else cross-references it as a live row.

## Trailer layout cross-check (hunks 19–20 vs. §6.2 and Appendix A)

I read §6.2's trailer field table directly (lines 800–816) to check the
byte offsets and widths the register rows restate:

| Offset | Size | Field |
|---|---|---|
| 0 | 8 | trailer magic |
| 8 | 2 | version_major |
| 10 | 2 | version_minor |
| 12 | 4 | flags |
| 16 | 8 | dir_offset |
| 24 | 8 | dir_length |
| 32 | 8 | committed_file_length |
| 40 | 8 | file_id |
| 48 | 12 | reserved |
| 60 | 4 | trailer CRC |

This matches F15's new text exactly ("12 reserved bytes at trailer offset
48," instance cell "trailer reserved [48,60)"), and F14's unchanged text
("CRC-32C of trailer bytes [0,60)" — 60 = trailer-relative offset of the
CRC field, consistent). No generation field remains in this table, and no
`generation` field appears anywhere the trailer's byte layout is restated
(grep below).

As further due diligence (outside my nine hunks, but the same defect
class the charter told me to hunt: "a stale offset or width anywhere the
old layout was restated"), I read Appendix A's worked byte-level example
(lines 4257–4278) and its byte table. It is fully consistent with the new
layout: dir_offset at [80,88), dir_length [88,96), committed_file_length
[96,104), file_id [104,112), 12 zero reserved bytes [112,124), trailer CRC
[124,128) — matching offset 48 (12 bytes reserved) relative to the
trailer's start at absolute 64. I also checked the raw hex dump against
this table (row `0060`: `80 00 00 00 00 00 00 00 EF CD AB 89 67 45 23 01`
= committed_file_length 128 then file_id in little-endian; row `0070`:
twelve zero bytes then the 4-byte CRC `7E 15 2F 40`) — internally
consistent with the table. I did not independently recompute the CRC-32C
value itself (out of scope of my nine hunks and not something a text
audit can verify without running the algorithm); noted under
confidence_empty.

## Sweeps run (verbatim, with hit counts)

- `grep -n "generation" spec/tarn.md` → 45 hits, all checked; every one is
  the general "committed state of a file" concept (glossary, §9, §20,
  Appendix, examples) — none is a residual reference to the removed
  trailer *field*, and none states a check against it.
- `grep -n "floor of 1\|generation counter\|generation.*floor\|floor.*generation" spec/tarn.md` → 0 hits.
- `grep -n "offset 56\|\[56,60)\|bytes 56\|56 through\|byte 56\|trailer offset 16\|offset 16.*dir_offset\|F − 16\|F-16\b" spec/tarn.md` → 0 hits (no stale pre-reorder offsets survive).
- `grep -n "offset 8\b\|offset 24\b\|offset 32\b\|offset 40\b\|offset 48\b\|F − 8\|F − 24\|F − 32\|F − 40\|F − 48" spec/tarn.md` → 1 hit (F15's own new text, offset 48 — expected, not stale).
- `grep -n "committed_file_length" spec/tarn.md` → 19 hits, all read; none contradicts the new offset/ordering claim.
- `grep -n "F1.*F36\|F1–F36\|F1-F36\|through F36\|F12.*F36" spec/tarn.md` → 0 hits (no range statement papers over the F11 gap).
- `grep -n "\bF11\b" spec/tarn.md` → 1 hit (the retirement Note only).
- `grep -n "renumber\|positional\|struck\|retired\|retire" spec/tarn.md` → 10 hits, all read and classified above.
- `grep -n "R-GEO-06\]\`\|R-SER-01\]\`" spec/tarn.md` → 6 hits; both identifiers exist and concern ordinal mappings, consistent with their citation in §21.7 (untouched by my hunks, spot-checked for contradiction only).
- `grep -n "R-WRT-06\|R-WRT-07\|R-WRT-01\b" spec/tarn.md` → 18 hits, read in full to resolve the file_id/R-WRT-06 citation question above.
- `grep -n "^#### 21\." spec/tarn.md` → 9 hits, used to bound each subsection for the recount.
- `grep -n "^#### 2\.2\|^### 2\." spec/tarn.md` and read of §2.1–2.3 in full, to check the requirement-identifier retirement model the hunk-21 Note borrows from.

## Candidates considered and rejected

1. **R-WRT-06 governing the fresh-`file_id` draw.** At first read, §20.5's
   file_id paragraph carries no trailing bracket, while `[R-WRT-06]` sits
   only at the end of the following paragraph (ignore-lane/version_minor/
   MU=1-refusal) — looked like the "(`[R-WRT-06]`)" citation in hunk-23's
   text might be wrong for the file_id item specifically. Rejected because
   (a) the citation was not changed by this hunk (present unedited in both
   old and new text) so it is not a defect this round introduced, and (b)
   three other untouched passages (lines 4148, 4463, 4537–4538) call the
   file_id draw "R-WRT-06's fresh draw," so R-WRT-06 is evidently the
   umbrella identifier for the whole two-paragraph compactor-trailer
   passage, not just the second paragraph.
2. **The F11-retirement Note being non-normative.** The Note sits inside a
   `> **Note.**` block, which is non-normative by the document's own §2.1
   rule, and the charter specifically warns that a rule stated only in
   such a block "carries no force." Rejected as a live defect because the
   same substantive claim ("row labels never renumber/reuse") is
   independently restated in plain, non-blockquoted, normative prose in
   §24 (hunk-27, ending `[R-VEC-02]`), and because the claim itself has no
   byte-level or actor-facing consequence (it governs how the register and
   the conformance-vector corpus are maintained, not what bytes a
   conforming file may contain) — so even taken alone, an implementer
   "ignoring" it changes nothing checkable. Recorded rather than silently
   dropped because it is exactly the pattern (§21.1's own text: "keyword-
   free clause is not thereby inert") the charter told me to be alert to.
3. **§21.1's "F21 of F22" pair possibly colliding with F30 (half-zero).**
   Considered whether the extent slot (0,0) case might actually belong to
   F30 (exactly-one-zero) rather than F21/F22 (both zero), which would
   undermine the specialization claim. Rejected on rereading F30's own
   text ("exactly one half zero (offset 0 with length != 0, or offset !=
   0 with length 0)") — slot (0,0) has *both* halves zero, so F30 does not
   apply to it at all; F21/F22 and F30 partition disjoint cases correctly,
   consistent with F33's cross-reference note about the half-zero rows.
4. **The Appendix A worked example being stale.** Given the charter's
   explicit warning about stale restated offsets, I treated the worked
   byte example as a prime suspect even though it's outside my nine hunks.
   Rejected as a finding after checking it byte-by-byte against §6.2's
   table (above) — it is fully updated to the new 12-byte-reserved-at-
   offset-48 layout, not stale.

## What I could not check

- I could not verify the Appendix A example's stated CRC-32C value
  (`0x402F157E`) by actually running CRC-32C over the listed trailer
  bytes — that is outside a text audit's reach without executing the
  algorithm, and the appendix is outside my nine assigned hunks in any
  case. If that appendix was touched by one of the three commits under
  audit, a byte-executing check of it is a gap in my coverage.
- I did not re-derive §21.3/§21.4/§21.5's *condition* counts (49/26/10)
  from first principles against the rules those rows restate — I took the
  row count (number of table rows) as the count, per §21.1's plain
  reading ("35 conditions" for §21.2 matches counting its rows), and this
  is uncontroversial arithmetic, not a judgment call. I did not re-audit
  every individual L/T/R row's own correctness against its governing
  rule — that is outside my charter's nine hunks, which do not touch
  §21.3/§21.4/§21.5 rows at all; I only used those sections' rows to
  reproduce the (unchanged) part of §21.8's total as a validation step.
- I did not have the pre-change file text, only the diff hunks' `-`
  lines; where I asserted something about "the old text," it is limited
  to what the hunks themselves show.
