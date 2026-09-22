# Diff-adversary transcript — TARN fidelity round

## Access discipline

I read exactly two files, by name:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md` (4977 lines)

I did not list any other directory and did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, spec/registry.json, git history, or the web. My scratch directory is
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/diff-adversary/`,
which I created and used for every working file: `raw.diff`, `build.py`, `f19-bit10.tarn`.

**Disclosure of pre-existing context.** Before I began, my runtime context already contained a
`MEMORY.md` file (the user's cross-session memory) whose index lines gesture at this project's
known defect categories (e.g. an entry titled "TARN closed-list exceptions compose", one titled
"TARN repair prose vs rules", one titled "TARN class lines are undertakings"). That material
appeared in my context before I opened either edition; it is not evidence, I have not treated any
titled hunch there as a lead, and I am not repeating its content here. Every finding below was
independently re-derived from the two files themselves, with byte-level or verdict-level
construction, and would stand even if that memory file did not exist. I also had a project
CLAUDE.md pointer (`See AGENTS.md`) in context; I did not open AGENTS.md, per the access rule, and
did not use that pointer for anything.

## Method

Both files are hard-wrapped prose (~5000 lines each) that are extremely close in size (4981 vs
4977 lines — a 4-line difference). Rather than eyeball-compare ~10,000 lines by hand (error-prone
against hard-wrap noise), I ran a line-level `diff -u a/tarn.md b/tarn.md`, which is exact and
whitespace/reflow-sensitive at the line level. This is a legitimate "local computation that reads
no other file" over the two permitted files.

**Control on the method's completeness.** `diff -u` found exactly **6 hunks**, and the total line
delta across all hunks (-1, -1, 0, 0, -2, 0) sums to -4, exactly matching the 4981→4977 line-count
delta. That arithmetic identity is itself a control: it proves the 6 hunks are the *entire* set of
line-level differences between the files — there is no seventh change hiding in a region where line
count happened to balance out. I additionally ran two independent sanity controls to rule out
tooling failure masking real differences:
- `grep -c "CRC-32C"` → 28 in both files; `grep -c "R-CNT-08"` → 10 in both; `grep -c "R-WRT-05"` →
  7 in both. These confirm grep/diff are actually reading both files (a silent empty-read would
  show 0/0, not matching non-zero counts), and confirm no requirement ID was silently
  renumbered or duplicated elsewhere as a side effect of the edits.
- `md5` of the two files differs (`75a78592...` vs `0b49bb3c...`), consistent with 6 real hunks
  existing (i.e., diff isn't erroneously reporting "no differences" while the files actually
  differ, nor is it reporting differences that don't exist — both are gross sanity checks, not a
  substitute for the line diff, which remains the authoritative source).

I did not need to grep for suspect vocabulary ("save where", "unless", "any", "every") as a
*discovery* method, because the exhaustive line diff already surfaced every candidate location —
including exactly the quantifier flip ("only" → "every ... or not") and the exception-drop ("save
where §20.4 licenses the drop" → dropped) that such a targeted grep would have been aimed at
finding. I used those phrases only to re-locate and re-quote hunks precisely (all reported as
`grep -n` calls above), never as a discovery pass over unread material.

## The six hunks, worked to bytes/verdicts

### Hunk 1 — §6.3, [R-CNT-08], updater's "MUST NOT clear" clause

A (lines 907-909):
> An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT clear them,
> and MUST NOT set any other: no writer under this text originates an ignore-lane bit...

B (line 907-908):
> An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT set any other:
> no writer under this text originates an ignore-lane bit...

B drops "MUST NOT clear them" as a separate clause. **Construction attempted:** an updater that
sets output flags bits 16-31 to 0 while its input carried an unknown ignore-lane bit set — would A
condemn this and B permit it?

**Closed as EQUIVALENT.** The trailer's own layout table (§6.2, row for the `flags` field, offset
12) is **byte-identical in both editions** (verified: same line, same text in both files): "bits
16–31 (ignore lane) 0 from a creator, **carried forward unchanged by every updater** (appender and
rewriter alike), a set bit ignored." "Carried forward unchanged" already forbids clearing any of
those bits — an updater that clears one has not carried it forward unchanged, full stop, regardless
of whether §6.3's prose separately says "MUST NOT clear them." An implementation built from B alone
that reads §6.2's table (which every implementation must, to know the field even exists) already
inherits the no-clearing obligation. No file's accept/reject verdict and no writer's output bytes
change between an implementation of A and an implementation of B on this point. **Rejected as a
finding** — closed by §6.2's unchanged table row.

### Hunk 2 — §20.3 step 2, [R-LIF-01] / §20.4 licensed drop

A (lines 3218-3220):
> Against any other structure the appender carries forward, it MUST NOT repair the defect —
> `[R-LIF-01]` freezes the committed prefix — and **MUST NOT drop the record save where §20.4
> licenses the drop.**

B (line 3218):
> Against any other structure the appender carries forward, it MUST NOT repair the defect —
> `[R-LIF-01]` freezes the committed prefix — and **MUST NOT drop the record.**

B deletes the carve-out "save where §20.4 licenses the drop" entirely, leaving an unqualified
prohibition. **Construction:** §20.4 (unchanged in both editions, verified byte-identical at this
location) states, in its `MU = 0, PE = 0` row: "an appender MAY drop the record in any commit it is
otherwise free to make — one whose only effect is the drop included" and, in its prose: "A commit
MAY therefore drop a layer record."

Take a concrete file: a layer L with a sub-record of a registered/definition-fixed type carrying
`PE = 0` (e.g. an application record whose governing definition sets `PE = 0`), and an appender
performing a commit whose only content change is dropping that one sub-record (per the `MU=0,
PE=0` row's express licence). Ask: **does §20.3 step 2 forbid this appender's own commit?**

- Under **A**: no contradiction. Step 2's "MUST NOT drop the record" is explicitly qualified
  by "save where §20.4 licenses the drop," and §20.4's `PE=0` row is exactly such a licence. The
  appender may emit the commit that omits the record's slot from the new directory — smaller
  directory bytes, one fewer record header+inline+extent triple than an unmodified re-emission.
- Under **B**: step 2 reads as an absolute prohibition, with no cross-reference reconciling it with
  §20.4's own "MAY drop" licence two sub-sections later. A writer implemented strictly, procedurally,
  from §20.3's step list (which is exactly how a procedural "MUST, in order" list is meant to be
  read and implemented) would refuse ever to drop *any* record during an append — producing a
  directory that **retains** the PE=0 record's header, inline payload and extent slot bytes, where
  an A-faithful implementation's directory **omits** them. That is a concrete byte-for-byte
  difference in the directory region's record sequence (and, correspondingly, in which bytes fall
  to slack vs. remain claimed) for the identical logical edit request.

This is a live self-contradiction inside B (step 2 vs. §20.4's own licence, neither passage in B
cross-referencing the other), not present in A, where the cross-reference resolves it. **Verdict:
LOSS** (a carve-out A states and B omits, per the fidelity test's own first category), reported as
adv-01.

### Hunk 3 — §20.3, worked example arithmetic

A (line 3400):
> the layer's full new index region (32 · 20 + 4 = **644** bytes — one entry re-pointed, 31
> byte-identical)

B (line 3398):
> the layer's full new index region (32 · 20 + 4 = **664** bytes — one entry re-pointed, 31
> byte-identical)

Pure arithmetic: 32 × 20 = 640; 640 + 4 = **644**. Verified independently in `build.py`
(`entries*per_entry + seg_crc_bytes = 644`). Edition B's stated result (664) does not equal the
formula it prints; edition A's does. Both editions state the identical entry-size factor (20
bytes/entry) and entry count (32) in the same worked example, so the *normative* per-entry index
size is unaffected — this is squarely the charter's fifth construction category: "a quantity ... a
worked example ... gives differently." An implementer or conformance-vector author who builds a
test fixture by trusting B's stated total (664 bytes for this layer's index region) rather than
recomputing from the formula would construct a file whose index-region length field does not match
what a correct implementation (or a straight reading of A) computes, and a verifier checking the
worked-example byte count against a real constructed file would report a different pass/fail
outcome for a "does this match the documented worked figure" check. Reported as adv-02, kind
**LOSS** (worked figure divergence; the containing block is a non-normative *Example* under
`[R-CNF-01]`, so this does not itself create a live conformance-behavior split — flagged as such in
the finding).

### Hunk 4 — §20.4, MU=1 row's reach ("only" → "every ... or not")

A (lines 3497-3498):
> The table states what an updater owes a record it does not logically modify, read under
> whichever flags govern it. **Its MU = 1 row reaches only a type the updater does not implement**
> — an updater implements both registered types and understands an unregistered type it implements
> from its definition, modifying their records as §20.3 and that definition provide — so for an
> implemented type only the PE bit bites:

B (lines 3495-3496):
> The table states what an updater owes a record it does not logically modify, read under
> whichever flags govern it. **Its MU = 1 row reaches every type, implemented or not** — an updater
> implements both registered types and understands an unregistered type it implements from its
> definition, modifying their records as §20.3 and that definition provide — so for an implemented
> type only the PE bit bites:

This is a direct quantifier reversal on the very next clause of the same sentence: B asserts "MU=1
reaches every type, implemented or not" and then, unmodified, still concludes "so for an implemented
type only the PE bit bites." Those two clauses are inconsistent with each other in B: if the MU=1
row truly reached implemented types too, PE would not be the *only* thing that bites for them — MU=1
would also impose "retain byte-identical, MUST NOT modify the scope." A's version has no such
inconsistency: the premise ("only... does not implement") directly supports the conclusion ("so for
an implemented type only PE bites").

**Concrete construction:** an updater implements an unregistered type `T` from its own definition
(§10.3 vehicle for implemented-but-unregistered types — governed, per this same paragraph, by "the
definition it implements the type from," which can in principle set `MU=1` on its own sub-records,
since nothing elsewhere in the read text restricts a type's own definition to `MU=0`). The updater
wants to modify one of `T`'s sub-records inside a layer it otherwise edits freely, and that
sub-record's governing flags happen to be `MU=1, PE=0`.
- Under **A**: since the updater implements `T`, the MU=1 row does not reach it ("reaches only a
  type the updater does not implement"); modification proceeds under §20.3 and `T`'s own
  definition. The commit is allowed; the appender emits new bytes for that sub-record's extent.
- Under **B**, read at its own stated premise ("reaches every type, implemented or not"): the MU=1
  row's obligation ("Retain byte-identical... MUST NOT modify the scope the record governs... its
  drop included") applies regardless of implementation status, so the same edit is now barred, and
  a B-faithful updater must refuse the commit (or must drop the entire layer instead of editing
  it, per the table's file/layer split) — a different accept/reject verdict on the identical
  requested edit, and different output bytes (no modified sub-record extent is ever written) than
  A's implementation would produce for the same input and the same requested edit.

This is a genuine, load-bearing quantifier flip, not closed by any other unchanged passage I could
find (the table's own MU=1 cell text is unchanged in both editions, but its cell language, "an
unknown critical record," is a description under the row's *heading* rather than an independent
restatement of who the row reaches — it does not resolve which premise sentence governs). Reported
as adv-03, kind **LOSS** (per the fidelity test's own wording: "states more narrowly or more
widely").

### Hunk 5 — §20.4, layer-drop paragraph's "one sub-record blocks the drop" sentence

A (lines 3512-3514):
> A commit MAY therefore drop a layer record, and the drop takes the layer whole: a sub-record's
> flags govern it within a layer the updater keeps, so a dropped layer's sub-records and their
> extents go with it whatever their PE bits. **One sub-record blocks the drop, a sub-record of a
> type the updater does not implement with MU = 1, the drop being a modification of the scope it
> governs (the table's first row).** A commit never removes a user-metadata record from a scope it
> keeps...

B (line 3510): the bolded sentence above is **absent**; B reads "...whatever their PE bits. A
commit never removes a user-metadata record from a scope it keeps..."

**Construction attempted:** a layer with an MU=1, unimplemented-type sub-record; does dropping the
whole layer (which the surrounding paragraph otherwise licenses "whatever their PE bits") remain
barred under B once this sentence is gone?

**Closed as EQUIVALENT.** The table itself — unchanged, byte-identical in both editions, three
paragraphs earlier in the same subsection — already states, in its `MU = 1` row: "At layer scope
an unknown critical record blocks modification of that layer, **its drop included**, leaving other
layers editable." The deleted sentence in A was a restatement of that same table cell, phrased for
this specific "commit MAY drop a layer" paragraph. Its removal from B does not remove the governing
rule, which the table still states in full; an implementer of B is bound by the table regardless of
whether this specific paragraph restates it. No byte or verdict difference survives. **Rejected as
a finding** — closed by §20.4's unchanged table row for `MU = 1`, same cell quoted for Hunk 1 also
covers the "drop" phrase relevant here.

### Hunk 6 — §21.2, register row F19, Instances column

A (line 3863):
> | F19 | Any bit of the flags incompat lane (bits 0-15) is set; this text defines no flag bits, so
> every such bit is unimplemented | **flags bits 0-15** | reader | open | `[R-CNT-08]` |

B (line 3859):
> | F19 | Any bit of the flags incompat lane (bits 0-15) is set; this text defines no flag bits, so
> every such bit is unimplemented | **flags bits 0-7** | reader | open | `[R-CNT-08]` |

The **Condition** cell (prose statement of the rule) is byte-identical in both editions and still
says "bits 0-15." Only the **Instances** cell — the column §21.1 uses to enumerate which concrete
bit/byte positions the row's condition covers, the same column test-vector authors are told (§1,
Reading this document / requirement-ID note) to build fixtures against — narrows to "bits 0-7" in
B. This is exactly the charter's named target: "the register's own governing rule for a row that
disagrees with prose." In B, the register row now **disagrees with its own Condition cell in the
same row**, not just with the ambient §6.3 prose (also unchanged, still "incompat lane (bits
0–15)" in both editions, confirmed at the same line number in both files).

**Byte-level construction — carried all the way to an actual file.** I built a minimal 128-byte
conforming-shaped file (`build.py`, script and output saved at
`.../scratch/diff-adversary/f19-bit10.tarn`, verified with a CRC-32C implementation whose check
vectors reproduce the spec's own stated check vector exactly: `CRC32C("123456789") = 0xE3069283`,
`CRC32C(b"") = 0x00000000`):

- front block: `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes (bytes [0,16))
- directory: 4 bytes, zero records, CRC-32C of zero bytes = `00000000` (bytes [16,20))
- slack: 44 zero bytes (bytes [20,64))
- trailer (bytes [64,128)): magic `8A 4E 52 41 54 0D 0A 1A`; version_major=1; version_minor=0;
  **flags = 0x00000400 (bit 10 set)**; dir_offset=16; dir_length=4; committed_file_length=128;
  file_id=1; reserved=0×12; trailer CRC computed over bytes [0,60) = `0xB4969025` (little-endian
  bytes `B4 96 90 25`)

Full 128-byte hex: `895441524e0d0a1a0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00008a4e5241540d0a1a01000000000400001000000000000000040000000000000080000000000000000100000000000000000000000000000000000000
b4969025` (assembled from the three regions above; also written to `f19-bit10.tarn`).

This file passes every other §6.2 gate (dir_offset ≥ 16 ✓; dir_length ≥ 4 ✓; dir_offset+dir_length
= 20 ≤ F−64 = 64 ✓; committed_file_length = 128 = F, multiple of 64 ✓; file_id ≠ 0 ✓; reserved
zero ✓; directory CRC correct ✓; version_major = 1, implemented ✓) and fails **only** on flags bit
10, an incompat-lane bit (bits 0-15), which this text defines nothing for, so §6.3 requires
reject-file.

- A reader/verifier built from **edition A** (Instances cell: "flags bits 0-15") is told, by the
  register alone, to test bit 10 — correctly rejects this file: **verdict nonconforming
  (reject-file)**, matching §6.3's prose in both editions.
- A reader/verifier built from **edition B**'s register alone (Instances cell: "flags bits 0-7"),
  if it treats the register's Instances column as the authoritative enumeration of what to check —
  which is exactly the role §1's own text assigns the register/requirement-ID scheme relative to
  prose ("test vectors cite those identifiers rather than prose positions") — checks only bits 0-7,
  finds none set, and never flags this file under F19. Nothing else in the F19 row catches bit 10.
  Such an implementation **certifies this file as conforming**, a different verdict on the same
  concrete file than the one an A-faithful (or prose-faithful) implementation reaches.

Reported as adv-04, kind **LOSS** (register states the condition's instances more narrowly than
edition A / than the unchanged prose in the very same row).

## Rejected candidates (worked to closure, no surviving difference)

1. **Hunk 1** ("MUST NOT clear them," §6.3) — closed by §6.2's unchanged trailer-flags table cell:
   "carried forward unchanged by every updater," identical in both editions, already forbids
   clearing.
2. **Hunk 5** ("one sub-record blocks the drop," §20.4) — closed by §20.4's unchanged MU=1 table
   cell: "At layer scope an unknown critical record blocks modification of that layer, its drop
   included," identical in both editions, already states the same rule.
3. I also attempted a seventh construction not tied to any diff hunk: hunting for a coverage-
   partition or outcome-class divergence (§5.2 / §2.4) by re-reading those sections in both editions
   side by side (already captured in full during my initial reads, offsets 296-337 and 698-781 in
   both files) — byte-identical in both editions at every line; no candidate found. Given the
   exhaustive line-diff already proved these regions are untouched (they fall outside all 6 hunks),
   this was a redundant check, not a new discovery method, and it closed with nothing.

## Evidence summary

- **Sweeps run:** one exhaustive `diff -u` over the complete two files (6 hunks, confirmed complete
  by the line-count-delta identity, -4 = -1-1+0+0-2+0); four `grep -c` control searches for
  known-present strings (CRC-32C: 28/28; R-CNT-08: 10/10; R-WRT-05: 7/7 — all non-zero and matched,
  ruling out a silent empty read); one `md5` comparison (files differ, consistent with the 6 hunks
  found). No keyword-guessing grep sweep over unread material was needed or run, since the
  exhaustive diff already located every difference; the few `grep -n` calls I made after the diff
  were only to re-locate/re-quote already-found hunks precisely.
- **Derived numbers:** 32 × 20 + 4 computed independently in Python = 644, matching edition A's
  stated figure and contradicting edition B's stated 664. CRC-32C implementation validated against
  the specification's own two check vectors before being trusted for the constructed file's trailer
  CRC (`0xE3069283` for `"123456789"`, `0x00000000` for empty input — both reproduced exactly).
- **Confidence in emptiness:** the "nothing else differs" conclusion rests on the diff's
  completeness proof (line-delta identity across all hunks), not on a sampling argument — I am not
  claiming to have read every line closely enough to eyeball-catch a change; I am relying on an
  exact tool (`diff -u`) whose output is provably exhaustive for this pair of files.
