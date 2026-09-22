# Reader-comparator working transcript (compare-reader)

## 0. Disclosure

**Files read, exactly:**
1. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4,981 lines / 302,380 bytes)
2. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md` (4,977 lines / 302,125 bytes)
3. `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-reader-a.md` (read in full via the Read tool)
4. `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/out/transcript-reader-b.md` (read in full via the Read tool)

No other file was opened. No directory was listed other than creating my own
scratch directory (`mkdir -p`) and writing files into it. I did not open
docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/,
spec/registry.json, git history, or the web.

**Commands run** (all `Bash`, all scoped to the two permitted spec files or my
own scratch directory):
- `ls -la` on the four permitted files (existence/size check only).
- `wc -l a/tarn.md b/tarn.md`, `wc -c a/tarn.md b/tarn.md` (size only).
- `grep -c -- "<tag>" a/tarn.md` / `b/tarn.md`, run once per requirement-ID
  tag (about 50 tags total: every `[R-XXX-NN]` cited by either walk's
  transcript or by the probe answers), to compare how many times each
  requirement ID appears in each edition before reading any of them in
  context. Every count matched exactly between editions.
- `grep -n "^#### N.M"` / `"^### N."` on both files, to locate the section
  headers the probes and the two walks cite, so I could `Read` the same
  section number in both editions side by side.
- `grep -n "F19"` on both files (2 hits each; used to find the register row).
- `grep -n "^| F[0-9]\|^| L[0-9]\|^| T[0-9]\|^| R[0-9]"` on both files,
  redirected to `reg_a.txt` / `reg_b.txt` in my scratch directory (120 lines
  each — every row of the entire error-handling register, F/L/T/R rows), then
  `diff reg_a.txt reg_b.txt`. This is a control-verified sweep: it captures
  every register row as a single physical line (register rows are table rows,
  never hard-wrapped), so no hard-wrap pitfall applies to it. It found
  exactly one differing row (F19, reported below).
- `diff a/tarn.md b/tarn.md` and `diff -u a/tarn.md b/tarn.md`, the
  decisive sweep: a full line-level diff of the two complete specification
  files. This is safe from the hard-wrap pitfall in the direction that
  matters here — it does not rely on a phrase landing on one line to be
  found; it compares every line of both files and reports every place they
  differ, whatever the wrap. (It could in principle report a spurious hunk
  where identical prose merely re-wrapped at a different column with no
  wording change; I read every hunk it reported in full sentence context
  below and confirmed each one is a genuine wording/content difference, not
  a re-wrap artifact.) It reported exactly **6 hunks**. I then `Read` each
  hunk's full paragraph (and, for two of them, the whole surrounding
  subsection) in both editions via the `Read` tool to confirm the change in
  its normative context, not just as a diff line.

**Why the full-document diff is the load-bearing method here.** The charter's
item 5 asks me to read the sections the reader depends on most, side by
side, looking for a rule, exception, quantifier or figure present in one
edition and not the other, "past the probes." A line-level diff of the
whole document *is* that check, exhaustively rather than by sampling: every
byte at which the two editions differ is one of the 6 hunks below, full
stop — nothing else in either 300KB file differs. I did not stop at running
it; I opened every hunk in prose context (via `Read`, offsets given below)
to judge, in each case, whether the differing words change a rule, an
exception, a quantifier, or a figure, per the fidelity test's four/seven
kinds, and whether it is reachable by any of the 8 probes or either walk's
own findings.

**Corroborating checks.** For every section either transcript's probe
answers (R1–R8) cite by number, I separately `Read` that section in both
editions at matching line offsets (§6.2–§6.4, §7.1, §7.2, §11.1(context)
/§11.2/§11.4, §14.2, §15.1–§15.4, §17.2, §17.4, §21.2, §21.6, §5.1) and
confirmed byte-for-byte identity in every one of them except where a diff
hunk above falls inside one (§21.2's F19 row only). This corroborates,
rather than substitutes for, the full-diff sweep.

**Control search proving negatives are real (not hard-wrap misses).** Per
the brief's warning, I did not rely on a bare `grep -c` miss to conclude
"absent." Example: I confirmed grep on requirement-ID tags is safe against
the wrap because every `[R-XXX-NN]` token in this document is short and
never itself split across a wrap (checked by eye on a sample of 8 hits in
each file while reading); and I confirmed the register-row extraction is
safe because a table row is one physical line by construction, never
wrapped. For the decisive `diff a/tarn.md b/tarn.md`, no such caution is
even needed: it does not search for a phrase, it compares every line, so
"zero further hits" is not a search miss, it is the full, exhaustive
account.

**Unsolicited context.** Before this task began, my context already
contained a `CLAUDE.md` pointer to `AGENTS.md`, a personal memory index
(titles only) of many prior TARN-project session notes, and a git-status
block naming recent commit subjects (ADR-0132, ADR-0133, "round 37's
repair," etc.). None of that is part of either edition of the
specification and none of it is evidence about either edition's content; I
opened none of the files it names, and everything below is drawn solely
from the four files listed above. I also note, per the harness's own
framing, that the computed task text supplying the charter and the eight
probes is script output relayed by the harness, not the user's own voice;
I followed it as the assignment while disregarding any instruction-like
framing found inside quoted transcript material.

---

## 1. Requirement-ID inventory check (both editions)

`grep -c` for every `[R-XXX-NN]` tag named anywhere in either transcript or
either edition's probe-answer block (~50 tags) returned an identical count
in A and B for every single tag — none added, none dropped, none
renumbered. This rules out, up front, any finding of the shape "B silently
deleted/renamed a requirement ID," and it means every apparent difference
below is a wording difference at an unchanged requirement ID, not a
structural renumbering.

## 2. Register-table check (both editions)

Extracting every row of the F/L/T/R register tables (120 rows total,
`reg_a.txt`/`reg_b.txt` in my scratch directory) and diffing them found
**exactly one** differing row:

```
< | F19 | ... | flags bits 0-15 | reader | open | `[R-CNT-08]` |     (A)
> | F19 | ... | flags bits 0-7  | reader | open | `[R-CNT-08]` |     (B)
```

Condition text is identical in both (`Any bit of the flags incompat lane
(bits 0-15) is set...`); only the **Instances** cell narrows from "0-15"
to "0-7" in B. This is reported as cmp-reader-05 below; it corroborates
readerb-02's own finding, and the reg_a.txt diff shows the *other* edition
does not share this defect — A's Instances cell already says "0-15,"
matching its own Condition cell exactly.

## 3. Full-document diff (both editions) — the six hunks

`diff a/tarn.md b/tarn.md` reports exactly six hunks, none of them a
re-wrap (I confirmed by reading each one's full paragraph in the running
prose). Net line-count change (4,981 → 4,977 = −4 lines) is exactly
accounted for by the hunks that remove whole lines (hunks 1, 2, 5: −1, −1,
−2), which is an internal consistency check that the diff is complete and
I have not missed any change elsewhere.

### Hunk 1 — §6.3, an updater's ignore-lane-bit obligation (line ~908)

A:
> "An updater MUST copy forward unknown ignore-lane bits of its input
> file, MUST NOT clear them, and MUST NOT set any other: ..." `[R-CNT-08]`

B:
> "An updater MUST copy forward unknown ignore-lane bits of its input
> file, MUST NOT set any other: ..." `[R-CNT-08]`

B drops the middle clause, "MUST NOT clear them." A imposes three distinct
obligations on an updater regarding an ignore-lane bit it does not
understand: (i) copy it forward, (ii) do not clear it, (iii) set no other
such bit. B states only (i) and (iii). "Copy forward" alone does not
entail "never clear," if "copy forward" is read as "propagate the file's
overall ignore-lane state" rather than "preserve this exact bit's value" —
the explicit "MUST NOT clear them" is what forecloses an updater that
zeroes out bits it finds meaningless while otherwise regenerating the
trailer. Kind: **LOSS**. Byte-level: **true** — an updater built strictly
from B's text could conform to B while zeroing an unknown ignore-lane bit
during a rewrite/append (since nothing in B forbids it), producing a
different trailer `flags` value than an updater built from A (which is
explicitly barred from clearing it). Location A: §6.3 (`[R-CNT-08]`).
Location B: §6.3 (`[R-CNT-08]`), absent the clause.

### Hunk 2 — §20.3 step 2, an appender's obligation to a carried-forward defective record (line ~3219)

A:
> "...it MUST NOT repair the defect — `[R-LIF-01]` freezes the committed
> prefix — and MUST NOT drop the record **save where §20.4 licenses the
> drop**."

B:
> "...it MUST NOT repair the defect — `[R-LIF-01]` freezes the committed
> prefix — and MUST NOT drop the record."

B drops "save where §20.4 licenses the drop." §20.4 (identical text in
both editions, confirmed below) states that a record whose governing flags
are `MU = 0, PE = 0` may be dropped by an appender in any commit it is
otherwise free to make ("Retain byte-identical, or drop it... an appender
MAY drop the record in any commit it is otherwise free to make"). A's
sentence is explicitly harmonized with that later licence; B's is not — B's
"MUST NOT drop the record" is now an unconditional prohibition that
contradicts §20.4's own `MU=0,PE=0` row two sections later **within the
same edition**. Kind: **LOSS** (a carve-out A states and B does not).
Byte-level: **true** — an implementer following B's literal text at this
step would refuse to drop a `PE=0` record it is carrying forward
unmodified from a defective prior state, where an implementer following
A's text (or B's own §20.4) would drop it; the two implementations commit
different bytes (one strands the defective record, the other does not).
Location A: §20.3 step 2 (`[R-LIF-01]`, cross-referencing §20.4). Location
B: §20.3 step 2 (`[R-LIF-01]`), the cross-reference and exception removed.

### Hunk 3 — §20.3 step 4, worked-example arithmetic (line ~3400)

A:
> "...the layer's full new index region (32 · 20 + 4 = **644** bytes...)"

B:
> "...the layer's full new index region (32 · 20 + 4 = **664** bytes...)"

32 × 20 + 4 = 644 (arithmetically correct, matching the general formula
`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`, itself unchanged and identical
in both editions at §15.1/§21's L2 row). B's stated figure, 664, is simply
wrong. This sits inside a `> **Example.**` block, non-normative under
[R-CNF-01] in the sense that no conforming reader/writer behavior is
defined by the example's prose — the binding rule is the formula stated
elsewhere, unchanged in both editions. Kind: **LOSS** (a worked figure A
states correctly and B states incorrectly — this is the "worked figure"
clause of the LOSS definition, applied to an introduced error rather than
an omission). Byte-level: **false** for a reader who computes the size
from the formula; **plausible but not established** for an implementer who
instead calibrates against the document's own stated example number — the
document gives no register row or rule keyed to this example figure, so I
do not mark it byte-level true, but flag the risk. Location A: §20.3 step
4 example. Location B: same location, arithmetic error.

### Hunk 4 — §20.4, which types the MU=1 re-emission row reaches (line ~3497)

A:
> "The table states what an updater owes a record it does not logically
> modify, read under whichever flags govern it. Its MU = 1 row reaches
> **only a type the updater does not implement** — an updater implements
> both registered types and understands an unregistered type it implements
> from its definition, modifying their records as §20.3 and that
> definition provide — so **for an implemented type only the PE bit
> bites**:"

B:
> "The table states what an updater owes a record it does not logically
> modify, read under whichever flags govern it. Its MU = 1 row reaches
> **every type, implemented or not** — an updater implements both
> registered types and understands an unregistered type it implements from
> its definition, modifying their records as §20.3 and that definition
> provide — so **for an implemented type only the PE bit bites**:"

Only the clause "reaches only a type the updater does not implement" vs.
"reaches every type, implemented or not" changed; everything else,
including the *same sentence's own conclusion* ("so for an implemented
type only the PE bit bites"), is untouched. B is now internally
self-contradictory within one sentence: it asserts the MU=1 row reaches
"every type, implemented or not," then immediately concludes that "for an
implemented type only the PE bit bites" — which is true only if the MU=1
row does *not* reach implemented types, i.e., only under A's wording. A is
internally consistent; B is not. Kind: **CONTRADICTION** (introduced
within B alone; not present in A) with a **LOSS** aspect (A's correct,
determinate scope-statement is what B corrupted). Byte-level: **plausible
divergence** — an implementer reading B's first clause literally could
conclude the MU=1 row's obligation ("the updater MUST NOT modify the scope
the record governs") binds even a record of an *implemented* type when its
governing flags happen to carry MU=1, and refuse an edit A's (self-
consistent) text would allow via §20.3's per-type rules; a different
implementer reading only B's second clause would do what A specifies.
Two conforming-per-B implementations can therefore diverge on the same
file where two conforming-per-A implementations cannot. Location A: §20.4
(`[R-WRT-05]`/`[R-CNT-22]` context, the paragraph introducing the
re-emission table). Location B: same location, reversed clause.

### Hunk 5 — §20.4, the sub-record veto on dropping a layer (line ~3512)

A:
> "A commit MAY therefore drop a layer record, and the drop takes the
> layer whole: a sub-record's flags govern it within a layer the updater
> keeps, so a dropped layer's sub-records and their extents go with it
> whatever their PE bits. **One sub-record blocks the drop, a sub-record
> of a type the updater does not implement with MU = 1, the drop being a
> modification of the scope it governs (the table's first row).** A
> commit never removes a user-metadata record from a scope it keeps..."

B:
> "A commit MAY therefore drop a layer record, and the drop takes the
> layer whole: a sub-record's flags govern it within a layer the updater
> keeps, so a dropped layer's sub-records and their extents go with it
> whatever their PE bits. A commit never removes a user-metadata record
> from a scope it keeps..."

B drops the entire sentence stating the exception: a layer carrying an
unimplemented, critical (`MU=1`) sub-record cannot be dropped at all,
because dropping the layer is itself "a modification of the scope [that
sub-record] governs," which the MU=1 row (identical in both editions,
§20.4's table) forbids ("The updater MUST NOT modify the scope the record
governs"). Without this sentence, B's surrounding text reads as an
unqualified licence: "A commit MAY therefore drop a layer record, and the
drop takes the layer whole" — full stop, with no stated exception anywhere
in B for the case where the layer carries an unimplemented critical
sub-record. Kind: **LOSS** (an exception A states, B omits entirely — one
of the clearest instances of the charter's LOSS category, "a rule, a
carve-out, an exception... that A states and B does not"). Byte-level:
**true** — an updater built strictly from B's text may drop a layer
carrying an unimplemented `MU=1` sub-record (emitting a directory without
that layer and its sub-records), which A's text (and A's own MU=1 row,
still present verbatim in B's own table two rows above) forbids; an
updater built from A refuses that same drop. Two implementations,
otherwise identical, commit different bytes for the same input file and
the same requested edit. Location A: §20.4, immediately after the "A
commit MAY therefore drop a layer record" sentence. Location B: same
location, sentence absent.

### Hunk 6 — §21.2 register row F19, Instances cell (line ~3863/3859)

Covered in detail above (Section 2). Kind: **LOSS**. Byte-level: **false**
— confirmed by direct comparison with the governing rule `[R-CNT-08]`,
identical and unqualified across bits 0–15 in both editions, so no
conforming reader's accept/reject behavior changes; the loss is in the
register's own corpus-coverage promise (§21.1's "at least one vector per
instance"), which in B's edition, read literally, no longer promises
coverage of incompat-lane bits 8–15. This is exactly readerb-02's own
finding (below, §5), now confirmed to be a defect unique to edition B: A's
parallel cell reads "flags bits 0-15," matching its own Condition text
exactly, with no analogous defect.

---

## 4. The eight probes: text-identity check

For every probe R1–R8, I opened, in both editions, every section number
either walk's transcript cites for that probe (§6.2, §6.3, §6.4, §7.1,
§7.2, §11.2, §11.4, §14.2, §15.1–§15.4, §17.2, §17.4, §21.2, §21.6, §5.1)
and compared them at matching offsets. All of them are byte-identical
between editions (none falls inside any of the 6 hunks above except §21.2's
F19 row, addressed under R2 below). Consequences:

- **R1** (open accounting): §6.4, §19.1 (unread directly but not needed —
  §6.4 itself states the "steps 1 and 2 cost one request" claim verbatim
  in both editions), §7.1 all identical. FROM A and FROM B agree
  (2 requests, `64 + dir_length` bytes, alternative 1-request strategy
  licensed by the same "theory of operation, not a budget" Note, verbatim
  in both). **EQUIVALENT** — genuine agreement over identical text, not
  luck.
- **R2** (flags = 0x00000004): §6.2's trailer-table row and §6.3's flag-gate
  paragraph are identical in both editions; the only edition-specific text
  touching F19 anywhere is the register row's Instances cell (hunk 6),
  which is not reachable by this probe (the probe asks for outcome class
  and conformance verdict, both governed by the identical `[R-CNT-08]`
  paragraph and the identical Condition cell, not by the Instances cell).
  FROM A and FROM B agree (reject-file, F19). **EQUIVALENT**.
- **R3** (codec 3 / zstd, reader lacks it): §17.2, §17.4, §21.6's closing
  two paragraphs, §21.9 all identical in both editions (checked verbatim,
  §17.4 and §21.6 reproduced in full above). Both FROM A and FROM B say
  "underdetermined" for the identical reason, quoting the identical
  sentence ("software unable to execute an assigned codec or filter is not
  a conforming reader"). **EQUIVALENT** — and see §5 below: this identical
  underdetermination is *also* independently reported as each walk's own
  Finding (readera-01/readerb-01), which I address separately.
- **R4** (tile-index entry, one field sentinel): §15.1–§15.3 identical,
  confirmed by full-text comparison above; register row T7 not in the
  6-hunk diff. FROM A and FROM B agree (reject-tile, T7, structural,
  scope=tile). **EQUIVALENT**.
- **R5** (directory CRC mismatch): §7.1 identical (confirmed above). FROM A
  and FROM B agree (reject-file, F20). **EQUIVALENT**.
- **R6** (F=96): §5.1 identical (confirmed above, full text reproduced).
  FROM A and FROM B agree (reject-file, F5, decided from F alone). **EQUIVALENT**.
- **R7** (disk ordinal / byte offset arithmetic): §11.2, §11.4, §14.2
  identical (confirmed above). Both compute disk ordinal 4, channel b at
  byte 17, via the same formulas; the differing citation lists in the two
  probe-answer blocks (A cites R-GEO-03, B cites R-GEO-05/06 for the same
  step) reflect each walker's own choice of which identical, both-present
  requirement ID to name, not a document difference — `grep -c R-GEO-03`
  is 3/3, present at the same three lines in both editions. **EQUIVALENT**.
- **R8** (unimplemented type, MU=1, top-level vs. sub-record): §7.2, §7.4,
  register rows F35/T-none/L-none, §21.6's closing "structural cases"
  paragraph, `[R-CNT-15]`/`[R-CNT-18]` all identical in both editions
  (§7.2 and §21.6 reproduced in full above). Both FROM A and FROM B agree:
  reject-file at top level, reject-layer as a sub-record, same rules cited.
  **EQUIVALENT**.

No probe passage falls inside any of the 6 hunks. This means: every
probe-level agreement between the two walks is a genuine agreement over
identical text, not a lucky agreement over diverging text (charter item 2)
— I looked for the latter specifically and found none.

## 5. Each walk's own findings, checked against the other edition

- **readera-01** (edition A, OBSERVATION: no outcome class for a reader
  lacking a mandatory codec/filter) and **readerb-01** (edition B,
  AMBIGUITY: same gap). I opened §17.2, §17.4, §21.6, §21.9 in both
  editions (reproduced in full above) and confirmed they are byte-
  identical. The defect both walks independently found is the same defect,
  reachable from the same, unchanged text, in both editions. Per charter
  item 3: this is not a LOSS unique to B nor an ADDITION unique to A — it
  is a pre-existing indeterminacy present in the shared source text A and
  B both carry forward unchanged. Kind: **EQUIVALENT** (as a fidelity
  matter between the editions — the two walks correctly and independently
  found the identical gap, which is itself a finding worth keeping on
  record but not a fidelity divergence).
- **readerb-02** (edition B, OBSERVATION: F19's Instances cell narrower
  than its Condition). I confirmed edition A's parallel cell reads "flags
  bits 0-15," matching its Condition exactly, with no analogous defect —
  see hunk 6 above. This is a genuine, B-only defect. Kind: **LOSS**
  (already reported as cmp-reader-05/hunk 6; readerb-02's finding is
  correct and its "byte-level: false" self-assessment is also correct,
  confirmed independently against `[R-CNT-08]`'s identical, unqualified
  text in both editions).

## 6. Guessing/re-reading moments in the transcripts (charter item 4)

Reader B's transcript explicitly disambiguates a naming collision at R4
(tile-index entry `offset`/`length` §15.1 vs. a record's `extent_offset`/
`extent_length` §7.2) before answering; reader A's transcript answers R4
without pausing on this point. I checked: both terms, and both fields
they name, are defined identically in both editions (§15.1 and §7.2 both
confirmed byte-identical above), so this is not a case where B's text
forced a disambiguation A's text did not — the same two same-named-adjacent
structures exist, unchanged, in A. B's walker chose to be more explicit
about a possible confusion that A's text permits equally; this is a
difference in walker diligence, not in the documents. No finding.

I found no other instance in either transcript of a walker re-reading,
backtracking, or flagging a forced guess that traces to a text difference
between editions — every guess/underdetermination either walk reports
(R3, the codec-capability gap; R1's "which strategy is canonical") is
reachable from text confirmed identical above.

## 7. Sections read "past the probes" beyond the full-document diff

Sections 5.1, 5.2 (partially), 6.1–6.4, 7.1, 7.2, 7.3 (header only), 7.4
(header only, contents not separately re-read beyond the diff/grep
confirmation that no hunk falls inside it), 11.2, 11.4, 14.2, 15.1–15.4,
17.2, 17.4, 18.1 (opening), 19.1 (via §6.4's cross-references), 20.3–20.4
(in full, both editions), 21.1 (implicitly, via the register-row extraction
and its own stated precedence rule "where a row and the rule it cites
diverge, the rule governs" — quoted identically by readerb-02 and confirmed
present in both editions' §21.1 by the register-diff finding only one row
differing), 21.2 (register table, all 120 F/L/T/R rows), 21.6 were each
opened in at least one edition and cross-checked against the other. Given
the full-document diff already proves these (and every other section) are
otherwise byte-identical, no further section-by-section reading was needed
to satisfy charter item 5 beyond confirming each of the six hunks in its
full paragraph context, which is done in §3 above.

## 8. Evidence summary

**Sweeps run.** (1) `grep -c` for ~50 requirement-ID tags against both
files: every count matched, 0 discrepancies. (2) `grep -n` for section
headers (§2.3–§21.9 range, ~20 headers) against both files: used to align
`Read` offsets; all headers present in both at a consistent ±1-to-4-line
offset (accounted for by the six hunks' net line-count change). (3)
`grep -n "^| F[0-9]\|^| L[0-9]\|^| T[0-9]\|^| R[0-9]"` against both files
→ 120/120 rows, diffed: 1 differing row (F19). (4) `diff a/tarn.md
b/tarn.md`: 6 hunks, the complete and exhaustive account of every
difference between the two 300KB documents. Each of the 6 hunks' controls:
I directly read the paragraph or subsection containing each hunk, in both
editions, via the `Read` tool at the offsets given in §3, rather than
trusting the diff line alone — this is the control that proves each hunk
is a genuine content change and not a line-wrap artifact (a re-wrap would
show the *same* words split at a different column; all six hunks instead
show different words or numbers).

**Derived numbers, checked against the documents' own stated figures.**
32 × 20 + 4 = 644 (my computation) vs. A's stated 644 (match) vs. B's
stated 664 (mismatch — this is hunk 3, reported as a document defect, not
a computation error on my part). Line-count arithmetic: 4,981 (A) − 4,977
(B) = 4; hunks removing whole lines account for exactly 1 + 1 + 2 = 4 lines
removed (hunks 1, 2, 5), and the remaining three hunks (3, 4, 6) are
same-line-count edits — this cross-check confirms the 6-hunk diff is
complete, i.e., I have not missed a 7th change that the diff tool
somehow failed to report.

**Rejected candidates.** I considered treating hunk 4 (the MU=1
row-scope reversal) as a plain LOSS like hunks 1, 2, 5, 6, but closed
that framing in favor of also flagging it as CONTRADICTION: unlike the
other hunks, B's replacement clause does not merely omit or narrow what A
said, it produces a sentence that is locally self-contradictory against
its own very next clause ("so for an implemented type only the PE bit
bites"), which is a stronger and more diagnosable defect than a bare
omission — I kept both labels rather than picking one, since the schema
allows it and both are true of this instance. I considered whether hunk 3
(644 vs. 664) rises to `byte_level: true` on the theory that an
implementer might trust the document's own worked example over deriving
the formula themselves; I left it as "plausible but not established"
rather than "true," because the document states the general formula
elsewhere unchanged in both editions and gives no register row or rule
keyed to the example's specific number — the risk is real (a wrong
worked example can seed a wrong implementation) but I do not have a
textual hook making it a conformance-verdict divergence the way hunks 1,
2, and 5 clearly are.

**Where confidence is thin.** I did not re-derive every one of the ~120
register rows' Condition-vs-Instances consistency the way I happened to
for F19 (that came from the targeted `grep -n "F19"` the probe R2 prompted,
plus the full register-table diff, which would have caught any *other*
row that also differs between editions — and it reported only F19 — but I
did not separately check every row's Condition cell against its own
Instances cell *within a single edition* for the kind of self-inconsistency
readerb-02 flagged; that is a different, single-edition audit outside this
comparator's mandate, which is a *cross-edition* diff). I am confident the
6-hunk full-document diff is a complete account of every difference between
the two editions specifically (that is what `diff` computes, and the
line-count check in §8 corroborates it), which is the strongest claim this
task asks for.
