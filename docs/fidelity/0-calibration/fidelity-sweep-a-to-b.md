# Sweep A→B — working transcript (completeness sweeper)

## Access
Read only:
- edition A: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (4981 lines)
- edition B: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md (4977 lines)

No other file was opened. No directory was listed for browsing purposes (only my own
scratch/out directories were created, per the ACCESS RULE's instruction to do so).

## Disclosure: material that appeared in context before I began

The harness's own framing text, shown to me before I opened either file, stated that a
mechanical checker had already compared "the requirement-ID paragraphs, the register
rows, the §3.1 terms, the tables and the fenced blocks." I did not verify that claim and
I am not relying on it as evidence — I re-derived my own findings independently from the
files themselves. Where a finding I report happens to fall inside one of those
mechanically-checked categories (a register row, a requirement-ID paragraph), I say so
explicitly and report it anyway, because I found it directly in the files, not by taking
the claim on faith.

No other material about the content of these two files was placed in my context before I
opened them.

## Method

Both files are hard-wrapped prose (~72–79 cols) with blockquoted Note/Example/Rationale
blocks (`> ` prefix). A raw line-by-line diff is useless here: any edit anywhere reflows
the paragraph's wrap points and produces a wall of spurious line-diffs having nothing to
do with content.

So, working only from the two files' own bytes:

1. I wrote a normalizer (`normalize.py`, logic inlined into a `python3 -c` heredoc, not
   saved standalone — the working commands are preserved below) that:
   - strips the `>` blockquote prefix per line but tracks whether a paragraph is
     blockquoted or not,
   - joins wrapped continuation lines of one paragraph into a single line (so wrapping
     differences between editions can never register as a "difference"),
   - keeps headings, table rows, fenced-code lines, and list-item starts as their own
     un-merged lines (so a table row is compared row-for-row, not swallowed into
     surrounding prose).
   - Output: `a_norm.txt` (1523 lines) and `b_norm.txt` (1523 lines) in my scratch
     directory.
2. `diff -u a_norm.txt b_norm.txt` over the normalized files. This is a full, exhaustive,
   whitespace-immune comparison of every paragraph, table row, heading, and labelled
   block in both editions — not a sample.
3. Control/validity checks on the method itself, before trusting its silence anywhere:
   - Section headings: `grep '^#'` on both normalized files, `diff`'d — **identical**,
     131 headings each, byte-for-byte, same order.
   - Labelled-block inventory: counted `> **Note`, `> **Example`, `> **Rationale` — 61 /
     20 / 13 in **both** editions.
   - Labelled-block *sequence*, not just count: extracted the ordered list of 94 block
     openers (Note/Example/Rationale, in document order) from each normalized file and
     `diff`'d them — **identical sequence**. This rules out a normative sentence having
     been moved into a Note (or vice versa) anywhere in the document while leaving its
     wording unchanged (a pure re-labelling would not otherwise show up in a content
     diff).
   - Balance check: the raw diff has exactly 6 removed lines and 6 added lines (paired
     1-for-1 replacements) — no bare insertion or deletion anywhere, i.e. no paragraph,
     table row, or block was wholesale added or dropped; every one of the 1523 aligned
     units in A has a corresponding unit in B.
   - Word counts: 49142 (A) vs 49095 (B), a difference of 47 words — consistent with
     exactly the small set of edits found below and nothing broader.
   - Control searches proving grep/the file reads actually reach the whole document
     (not just the part shown to me in my first reads): `CRC-32C` → 28/28;
     `linearization` (§11 area, untouched) → 15/15; `compaction` (§20/23 area) → 8/8.
     All equal, confirming both files are fully legible to my tools end to end and that
     "no diff found" in the untouched 99.6% of the document is a real zero, not a search
     failure.

Given this, the six hunks below are, to the resolution this method can see, **the
complete set of content differences between the two editions**. I additionally read the
first ~1550 lines of both files directly, side by side (§1 through §9.7), before running
the normalizer, as a manual spot-check; that manual read agrees with the automated diff
over that range (it found the same §6.3 difference, swab-01, and nothing else).

### Sections not read line-by-line by eye

I read §1–§9.7 (lines 1–~1550 of A) directly. The remainder (§10–Appendices, roughly
lines 1550–4981) I did not read prose-by-prose by eye; I rely on the normalized full-text
diff plus the structural control checks above for that range. That diff is exhaustive
over every paragraph, table row and labelled block in that range, so I am not aware of
any gap in coverage, but I flag the distinction between "read by eye" and "covered by an
exhaustive mechanical comparison of my own construction" per the disclosure instruction.

## Findings located

### swab-01 — §6.3, `[R-CNT-08]` — ignore-lane bit preservation
A: "An updater MUST copy forward unknown ignore-lane bits of its input file, MUST
NOT clear them, and MUST NOT set any other: ..."
B: "An updater MUST copy forward unknown ignore-lane bits of its input file, MUST
NOT set any other: ..."
B drops the clause "MUST NOT clear them, and". Analysis: "copy forward X" is itself
an affirmative obligation to reproduce X's bits exactly; clearing a bit that was 1
in the input is not copying it forward, so the deleted clause is logically already
entailed by the sentence's own opening clause. No behavioral daylight between the
two editions here. Classified EQUIVALENT (a stylistic de-duplication, not a
substantive narrowing) — reported because it is the kind of thing the charter asks
me to check even where I conclude "no loss."

### swab-02 — §20.3 step 2 (appender algorithm) — drop-on-carry-forward
A (line 3219-3220): "...it MUST NOT repair the defect — `[R-LIF-01]` freezes the
committed prefix — and MUST NOT drop the record save where §20.4 licenses the drop."
B (line 3218): "...it MUST NOT repair the defect — `[R-LIF-01]` freezes the
committed prefix — and MUST NOT drop the record."
B drops "save where §20.4 licenses the drop." This sentence carries no R-ID of its
own (it is numbered-list prose inside the `[R-WRT-03]`-governed appender algorithm,
not itself ID-tagged), so it is squarely inside my remit, not the mechanical
checker's. §20.4 (unchanged in both editions, confirmed identical by the diff) goes
on to state that an updater "MAY drop" an MU=0/PE=0 record "in any commit it is
otherwise free to make." Read literally and alone, B's step-2 sentence is an
unqualified "MUST NOT drop the record," which conflicts with §20.4's later,
unqualified permission for the same actor over the same class of record. A resolves
this by cross-referencing the exception at the point of the rule; B does not. LOSS
(the rule is stated more widely in B, with the narrowing exception removed) with a
resulting apparent internal contradiction against §20.4.

### swab-03 — §20.3, worked Example — index-region byte count
A (line 3400): "...the layer's full new index region (32 · 20 + 4 = 644 bytes —
one entry re-pointed, 31 byte-identical)..."
B (line 3398): "...the layer's full new index region (32 · 20 + 4 = 664 bytes —
one entry re-pointed, 31 byte-identical)..."
32 × 20 + 4 = 644, not 664 — B's own stated arithmetic (unchanged from A: "32 · 20 +
4") computes to 644; the "664" is an arithmetic error introduced in B, and also
contradicts `[R-CNT-17]`'s formula (entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4), which
is worded identically in both editions and yields 644 for entry_count = 32.
CONTRADICTION (B's own worked figure disagrees with B's own normative formula, and
with A's correct figure). This sits inside a `>` **Example** block, non-normative
under `[R-CNF-01]`, so it does not itself change what a conforming implementation
does — flagged as byte_level: false — but it is exactly the kind of worked-figure
error the charter asks me to surface, and a test-vector author trusting the
worked example would get 644 wrong.

### swab-04 — §20.4 — scope of the MU=1 table row
A (line 3497-3498): "Its MU = 1 row reaches only a type the updater does not
implement — an updater implements both registered types and understands an
unregistered type it implements from its definition..."
B (line 3495-3496): "Its MU = 1 row reaches every type, implemented or not — an
updater implements both registered types and understands an unregistered type it
implements from its definition..."
Both editions' sentence ends identically: "...so for an implemented type only the
PE bit bites" — which only makes sense on A's premise (the MU=1 row does *not*
reach implemented types, so only PE governs them). B's premise ("reaches every
type, implemented or not") directly contradicts its own sentence's conclusion.
CONTRADICTION — both against A, and internally within B's own sentence. This is
prose with no R-ID of its own (it is exposition ahead of the `[R-CNT-22]`-governed
table, not itself tagged), so squarely in my remit.

### swab-05 — §20.4 — sub-record block on layer drop
A (lines 3509-3514): "A commit MAY therefore drop a layer record, and the drop
takes the layer whole: ... One sub-record blocks the drop, a sub-record of a type
the updater does not implement with MU = 1, the drop being a modification of the
scope it governs (the table's first row). A commit never removes a user-metadata
record from a scope it keeps: ..."
B (lines 3507-3511): "A commit MAY therefore drop a layer record, and the drop
takes the layer whole: ... A commit never removes a user-metadata record from a
scope it keeps: ..."
B omits the sentence "One sub-record blocks the drop... (the table's first row)"
entirely. However, the table's MU=1 row itself — unchanged, present verbatim in
both editions, immediately above this paragraph — already states: "At layer scope
an unknown critical record blocks modification of that layer, its drop included,
leaving other layers editable." That is the identical substantive constraint, and
the deleted sentence in A explicitly cross-references it ("the table's first row")
rather than adding new content. An implementation built from either edition, read
as a whole, has the same obligation. Classified EQUIVALENT (redundant restatement
of an already-stated table row) rather than LOSS, on a byte-level reading of "the
whole of B" — flagged because it's a closer call than swab-01: B's preceding clause
("MAY therefore drop a layer record, and the drop takes the layer whole") is left,
locally, without its immediate qualifier, which is a readability/emphasis
regression even though the rule survives elsewhere in the same edition.

### swab-06 — §21.2, register row F19 — incompat-lane bit range
A (line 3863): "| F19 | Any bit of the flags incompat lane (bits 0-15) is set;
this text defines no flag bits, so every such bit is unimplemented | flags bits
0-15 | reader | open | `[R-CNT-08]` |"
B (line 3859): same row, except the Field-checked cell reads "flags bits 0-7"
instead of "flags bits 0-15".
This is a register row, one of the categories the harness says a mechanical
checker already compared — I report it anyway because I found it directly, via the
same exhaustive normalized diff as everything else above, and it is severe: §6.2's
trailer layout table (byte-identical in both editions, confirmed by the diff)
fixes the incompat lane as bits 0–15, and §6.3's flag-gate prose (also unchanged)
requires a reader to reject-file "on any set bit it does not implement in the
incompat lane (bits 0–15)." B's F19 row narrows the field actually checked to bits
0-7, silently exempting bits 8-15 of the incompat lane from the very check the row
is describing. LOSS (the row states, more narrowly than A and than B's own §6.2/6.3
text, the range of bits F19 covers) — and squarely byte-level: a reader built to
F19's row alone in B would accept files with an unimplemented bit set anywhere in
8-15, which A's row (and both editions' own §6.2/6.3 prose) requires to be
reject-file.

## Sections confirmed equivalent (no diff located, by the exhaustive method above)

§1, §2 (2.1–2.5), §3 (3.1–3.3), §4 (4.1–4.7), §5 (5.1–5.2), §6.1, §6.2, §6.4, §7
(7.1–7.4) apart from none, §8 (8.1–8.2), §9.1–9.7, and — per the normalized-diff
balance check (6 removed / 6 added lines total, matching exactly the six hunks
above) — every section from §10 onward as well, excepting the six locations named.
I did not additionally enumerate every §10–§24 item by eye against the charter's
"list every rule/carve-out/quantifier" instruction one at a time; I relied on the
exhaustive whitespace-normalized diff (proven exhaustive by the header/label/balance
controls above) standing in for that manual enumeration over that range.
