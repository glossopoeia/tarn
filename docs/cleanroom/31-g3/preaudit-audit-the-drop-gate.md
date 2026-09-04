# Audit transcript — lane "the-drop-gate" (hunks 11 and 16)

## Disclosure

Read: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-11.diff`,
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-16.diff`,
and `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via sed/grep on
absolute paths; passages listed below). Wrote:
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/scratch/the-drop-gate/tarn-flat.txt`
(a whitespace-flattened copy of the spec with `> ` stripped, for wrap-proof phrase
search) and this file. No other file read or written. Did not read full.diff, other
hunks, docs/, git, conformance/, registry, or the web; did not list the case directory.

Context I did not ask for: the runtime placed a project-instructions pointer, a
memory index (four entry titles about this project's harness, gate word list,
preflight, and "repair prose vs rules"), a git-status block naming five recent
commit subjects (which name ADR numbers and round numbers), and a user email into
my context before I began. I did not open any of the files those pointed at and
drew no conclusion from them; everything below rests on the spec text and the two
hunk files.

## Hunk headers vs bodies

- hunk-11: header says lines 3135-3138, nearest heading line 3104 "20.3 The append
  procedure". `sed -n 3104p` → "#### 20.3 The append procedure"; `sed -n 3135,3138p`
  shows the "+" lines verbatim. Match.
- hunk-16: header says line 3417, nearest heading 3393 "20.4 Re-emission and
  preservation". `sed -n 3393p` → "#### 20.4 Re-emission and preservation";
  line 3417 is the new MU = 0, PE = 0 row verbatim. Match.

## Passages read in full

§2.1–§2.4 (lines 95–336), §5.2 (689–762), §6.3 (856–900), §7.2–§7.4 (973–1187),
§9.1–§9.2 and start of §9.3 (1233–1330), §9.7 (1462–1511), §10.3–§10.4 (1555–1602),
§19.1–§19.3 (2862–2983), §20 intro, §20.1, §20.2 (3062–3104), §20.3 whole
(3104–3392), §20.4 whole (3393–3451), §20.5 whole (3452–3594), §21.1 (3597–3682),
§21.5–§21.6 (3831–3919), §21.7 excerpt around [R-ERR-04] (4015–4035), §22.3
(4111–4155), §23.1 (4186–4223), Appendix H (4698–4770). Plus the heading list.

## The rule each hunk adopts (my words)

**Hunk 16 (the cell).** For a record of a type the updater does not implement whose
stored flags are MU = 0 and PE = 0, the updater has exactly two options — carry the
record forward byte-identically, or omit it from the new directory — and the choice
is unconditioned: it may omit it in any commit it makes, including a commit that
does nothing else; a compactor may omit it from any output. An updater that omits
it SHOULD report that. The old cell conditioned the appender's drop on the same
commit *independently* changing the scope the record attached to, and forbade a
drop-only commit ("MUST retain it").

**Hunk 11 (the step).** In §20.3 step 2, an appender carrying a defective structure
forward may not repair it and may not drop it, unless §20.4's table licenses the
drop — and the sentence then asserts the table's licence covers exactly one class:
"an unregistered record stored MU = 0, PE = 0 and for no other". The old text
said "MUST NOT drop the record (§20.4)" with no gloss (and, in the old cell, the
drop was conditioned).

## Check 1 — tense and quantifier

Cell: "an updater MAY drop the record in any commit" — actor: updater; set: every
commit; generation: the new directory (drop = absence from the directory step 3 of
[R-LIF-02] emits). "a compactor MAY drop it whenever it rewrites the file" — actor:
compactor; set: every compaction. "the writer that stored PE = 0" — the original
writer. No tense ambiguity: a drop is only ever expressed in the new generation.
The cell IS the normative rule (the table has no requirement ID; nothing else
states the drop licence — see sweeps).

Step: "MUST NOT drop the record save where §20.4's table licenses the drop" —
actor: appender; the licence is delegated to the table. The gloss "which it does
for an unregistered record stored MU = 0, PE = 0 and for no other" is a
restatement of the table's reach. Comparison with the rule it restates: the
table's introduction (line 3409–3411) keys the table on "a type the updater does
not implement" and on "stored flags"; the paragraph above it (3401–3408) keys the
drop licence generally on *authoritative* flags — registry for registered types,
the implemented definition for an implemented unregistered type ("the stored bits
never do"), stored bits only for an unimplemented type. The gloss uses
"unregistered" + "stored", which is neither of those keys. See A-01.

## Check 2 — citations

- Hunk 11 "§20.4's table": opened; the table exists at 3413–3417 and its third
  row licenses a drop. PASS as a pointer; but the old text cited "§20.4" (the
  section, which includes the flag-authority paragraph) and the new text narrows
  to "the table", which by its own introduction covers only unimplemented types.
  See A-01.
- Hunk 11 context "[R-LIF-01]" (unchanged text): §9.1 — committed prefix immutable.
  PASS.
- Hunk 16: the new cell cites nothing. The old cell's citations ([R-CNT-22], §7.3,
  §20.3, [R-WRT-04], §7.4) were removed with the text that needed them; none is
  needed by the new text. PASS.
- Cross-checked the cell's neighbours it must agree with: [R-CNT-12] (§7.2,
  MU = 1 with PE = 0 read as PE = 1), [R-CNT-15] (§7.2, MU rule + updater
  obligations are §20's subject), [R-CNT-22] (§7.3, stored bits authoritative only
  for types the tool does not implement), [R-WRT-05] (3395–3399), [R-WRT-08]
  (3429–3433), [R-LIF-02] (§9.2). All say what §20.4 relies on them for.

## Check 3 — normative placement

Hunk 11 lands inside numbered step 2 of §20.3 — plain prose, no Note/Example/
Rationale label. Normative. Hunk 16 lands in a Markdown table in §20.4 body, not
in any blockquote. Normative. Test applied: [R-CNF-01]'s label test, not the ">"
marker. Distinctive-term sweeps (flattened copy): "whose only effect is the drop" 1
hit (3417); "bit's own" 1 (3417); "declined preservation" 1 (3417); "for no other"
1 (3137); "licenses the drop" 1 (3136). Each hit is in normative text; no
labeled block restates the old rule.

## Check 4 — contradiction in the same passage, including untouched text

Read the whole table, the two paragraphs after it, [R-WRT-08], the Rationale, §20.5,
and step 2 of §20.3 around hunk 11.

(a) **MU = 1 row vs the new "any commit".** MU = 1 row (3415, untouched): "The
updater MUST NOT modify the scope the record governs. At layer scope an unknown
critical record blocks modification of that layer". Dropping an MU = 0 / PE = 0
*sub-record* of that layer changes the layer record's inline payload (sub-record
bytes gone, inline_length changes) — under [R-WRT-05] that record is no longer
"re-emit[ted] byte-identically", i.e. the layer is modified. New cell: "an updater
MAY drop the record in any commit, including one whose only effect is the drop".
Under the old cell this collision could not arise: the drop of a sub-record
required an *independent* change to that layer's record, which the MU = 1 row
already barred, so the precondition was never satisfiable. The new unconditional
MAY reaches it. Same shape against §20.3 step 2's own sentence (3123–3125,
untouched): "reject-layer bars a commit that modifies that layer" — a drop-only
commit on a sub-record of a rejected layer modifies that layer. At file scope both
collisions are vacuous (reject-file / top-level MU = 1 → no commit exists). See
A-02.

(b) "No commit therefore removes a layer record, or a user-metadata record at
either scope" (3419) — still follows from the paragraph + table. No conflict.

(c) [R-WRT-08] "MUST NOT modify one except by relocating its extent" — dropping is
not modifying; "Retain byte-identical, or drop it" remains the exhaustive pair.
No conflict.

(d) Rationale block: "differs ... exactly by the records modified, added, or
dropped" — consistent.

(e) §20.5: "less any record §20.4 lets it drop"; "only where §20.4's table
licenses it"; "Where the table does not license a drop the compactor MUST
refuse" — the compactor half of the cell ("MAY drop it whenever it rewrites the
file") is what these lean on; unchanged in substance. Consistent. The MU = 1 row's
"a compactor MUST refuse to compact the file" makes "whenever it rewrites" vacuous
there — consistent, not contradictory.

## Check 5 — exhaustive claims

Hunk 11: "for no other" — falsified in both directions by an implemented
unregistered type whose stored bits disagree with its definition (A-01).
"unregistered" — not the document's usual term (elsewhere "a type §7.3 registers",
"this specification does not register", "unassigned"); one prior use at line 1563.
Reserved-range types are unregistered too, and the table does license their drop
when unimplemented and stored MU = 0 / PE = 0 (§21.6 row: "a reserved-range type
is read the same way"), so the word's reach there is right.

Hunk 16: "in any commit" — falsified by (a) above (A-02). "including one whose only
effect is the drop" — tested below under the commit protocol; admitted. "whenever
it rewrites the file" — holds. "The licence is the bit's own" — PE = 0 alone is
not enough (MU = 1 with PE = 0 reads as PE = 1, [R-CNT-12]); but the row label is
MU = 0, PE = 0, so "the bit" is read in that row. Holds.

## Is a drop-only commit a commit the protocol admits?

[R-LIF-02] (1245–1258): step (2) "append new stored-tile payloads and tile-index
regions for the layers it changes, and any new record extents" — "for the layers it
changes" and "any" admit zero; step (3) "append the new complete directory —
re-emitting every retained record" — "retained" already contemplates non-retained
ones; the 128-byte floor is derived from "at least a directory and a trailer"
(§20.3 step 6, 3313–3316). §20.3 step 4 (3149–3153): "Every layer whose
stored-tile set or index content this commit changes has its tile-index region
re-emitted" — conditional; a drop changes neither. So yes: the sentence that
decides it is [R-LIF-02] step 2's "any new record extents" read with step 3, and
§20.3's Example (c) (non-normative) confirms "A change confined to the directory
... Only the directory is re-emitted." §20.1's appender description ("adding
layers or records, superseding tiles, growing extents, amending metadata") does
not list dropping — but it also omits shrinks, unstores and slab clearing that
§20.3 permits, so it is descriptive, not closed. Not a finding.

## Check 6 — what the row leaves unconstrained

Structure: the MU = 0 / PE = 0 row of the §20.4 obligations table. Quantities it
touches and what fixes each:
- retention: "Retain byte-identical" — [R-WRT-05] fixes what byte-identical means
  (header, inline payload, extent slot).
- the drop: licensed unconditionally for updater and compactor — the cell itself.
- the extent: "becoming slack" — [R-CNT-21] (§5.2: everything an earlier commit
  superseded is slack; only compaction reclaims it) and §23.1 (leaves bytes
  recoverable). For a record with extent (0, 0) there is no extent; the phrase is
  vacuous and the record's header/inline payload go to slack with the superseded
  directory anyway. Not a gap.
- the report: SHOULD, consequence stated. Reaches a compactor because §20.1 puts
  compactors under [R-CNF-06] (the updater rule) and the MU = 1 row lists
  compactor duties under "Updater obligation".
- record whose stored flags disagree with the registry: the paragraph above the
  table routes registered types to the registry (both PE = 1 → no drop); the row
  is never reached. Fixed.
- record of an implemented unregistered type: the table's introduction keys the
  table on "a type the updater does not implement", and the paragraph says the
  definition supplies the flags. So the *table* does not reach it; the paragraph
  does, by "Persistence governs every record type; only the authoritative source
  of the flags differs". This is the seam hunk 11's gloss gets wrong (A-01). It is
  pre-existing that the "MU = 0, PE = 1 → Retain byte-identical" row cannot
  literally apply to implemented types (user metadata is MU = 0 / PE = 1 and
  updaters edit it), which is why the table must be read as unimplemented-only;
  the cell did not change that.
- the sibling rows: MU = 1 and MU = 0 / PE = 1 unchanged; their interaction with
  the widened MAY is A-02.

## Check 7 — analogy

Hunk 11 argues by none. Hunk 16's "The licence is the bit's own: the writer that
stored PE = 0 declined preservation across edits" is an argument from the bit's
meaning, not a cross-reference. Where is PE's meaning defined? Sweep
"PRESERVE_ON_EDIT": §7.2 field table (names the bit only), F25, L46. Sweep
"preserv" (excluding preserve-verbatim): nothing else states what PE = 0 means.
So the cell is the definition; the governing verbs ("declined preservation" /
"MAY drop") range over the same record. No mismatch. §2.4's preserve-verbatim
entry ("§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows")
ranges over the other two rows — consistent.

## Check 8 — anaphors around the insertions

Forward from hunk 11's insertion to the end of step 2 (3138–3148): "a
structure's bytes" (generic); "the bytes it produces" (its own sentence);
"travels with that structure" (own sentence); "which is as true of an index entry
... as of a record" (own sentence); "SHOULD report it" → "a violation" (own
sentence). Before/after: identical resolutions; the inserted clause introduces
no new noun any of them could grab. Backward: the inserted "which it does" → "§20.4's
table" (nearest antecedent, same sentence); "the drop" → "drop the record" (same
sentence); "the record" → pre-existing anaphor to "any other structure" (already
assumed the structure is a record; unchanged).

Cell: "the bit's own" → the PE = 0 bit of the row label; "such a record" → the
row's record; "the loss" → the drop. Paragraph after the table: "No commit
therefore removes ..." → the paragraph + table above; unchanged. Rationale: "the
records modified, added, or dropped" — generic.

## Downstream of the licence

- §20.5 (3452–3470, 3529–3532): "less any record §20.4 lets it drop", "only where
  §20.4's table licenses it", "no drop is available, a tile-index entry being no
  record §20.4's table licenses dropping" — all still describe the cell.
- §23.1 (4193–4195): "a record's extent goes the same way whether a commit drops the
  record (§20.4) or supersedes it" — still describes it.
- §21.6 row (3876): "Ignored, and preserved or dropped per its PE bit" — the row
  presupposes an unimplemented type ("Ignored"), so "its PE bit" = stored bit,
  which matches the table's key. Now matches the cell *better* than before (the
  old cell's commit-conditioning was never in the row). Its Rule cell cites
  [R-WRT-08], which says nothing about PE or dropping — pre-existing, and the
  drop rule carries no ID to cite; not a finding of this repair.
- Appendix H updater checklist (4736–4743): "respects every record's MU and PE
  bits, the registry's fixed values governing for a registered type (§20.4,
  [R-CNT-22]); never removes a layer record, or a user-metadata record at either
  scope (§20.4)" — still describes the cell; non-normative.
- §2.4 preserve-verbatim (306) — names the other two rows; still right.
- §22.3 (4137–4140) — re-emission/no-re-encode; unaffected.

## Hunk 11's class vs the set the cell + paragraph license

Derived set (from 3401–3417): a record may be dropped iff its *authoritative*
flags are MU = 0 and PE = 0, where authoritative = registry (registered types →
never), the implemented definition (implemented unregistered type), or the stored
bits (unimplemented type; MU = 1 / PE = 0 → PE = 1).

Hunk 11's class: unregistered AND stored MU = 0 AND stored PE = 0.

- unimplemented, stored MU = 0, PE = 0: both yes. Match.
- registered type stored MU = 0, PE = 0 (F28/L49 violation): registry → no;
  "unregistered" excludes → no. Match.
- MU = 1 stored with PE = 0: [R-CNT-12] → PE = 1 → no; "stored MU = 0" excludes →
  no. Match.
- reserved-range unimplemented, stored MU = 0, PE = 0: stored bits govern → yes;
  unregistered → yes. Match (§21.6 row agrees).
- implemented unregistered type, definition PE = 1 (or MU = 1), stored MU = 0,
  PE = 0: definition governs, "the stored bits never do" → no; hunk 11 → yes.
  MISMATCH.
- implemented unregistered type, definition MU = 0, PE = 0, stored PE = 1:
  definition → yes (via "Persistence governs every record type; only the
  authoritative source of the flags differs"); hunk 11 → "for no other" → no.
  MISMATCH.

## Sweeps run (flattened copy unless noted; controls shown)

- `grep -o -i -F "independently changes"` → 0. Control on the same file:
  `"scope the record governs"` → 2. Line-grep `independently` → 3 hits, none about
  records (2306, 2393, 3816). Old conditioning is swept.
- `"only effect would be the drop"` → 0 (old cell text gone); control
  `"whose only effect is the drop"` → 1.
- `"scope the record attaches"` → 0 (old cell text gone); control
  `"Persistence governs every record type"` → 1.
- `"record save where §20.4"`: line-grep 0, flat 1 — proves the line-grep misses
  wrapped phrases and the flat copy sees them.
- `"for no other"` → 1; `"licenses the drop"` → 1; `"declined preservation"` → 1;
  `"bit's own"` → 1; `"in any commit"` → 1; `"stored MU = 0, PE = 0"` → 1;
  `"MUST NOT drop"` → 1; `"the stored bits never do"` → 1;
  `"confers understanding"` → 1; `"never silently deletable"` → 1;
  `"preserved or dropped per its PE bit"` → 1; `"less any record"` → 1;
  `"amending metadata"` → 1; `"commit that modifies that layer"` → 1;
  `"such a change"` → 3 (all in §20.3 step 4, about declarations; none about
  records); `"does not implement"` → 17.
- Line-greps on the spec: `-i drop` (18 hits, all listed above, none conditions a
  record drop on another change); `-i unregistered` (1563, 3137);
  `-i licen` (12 hits; only 3136, 3417, 3466, 3469, 3532 concern the drop);
  `PRESERVE_ON_EDIT` (981, 3718, 3789); `-i preserv` (listed above);
  `-i remov` filtered to record/layer/commit (1633, 3272, 3419, 3421, 4188, 4199,
  4740); `-i amend` (3076); `-i authoritative` (904, 934, 1068, 1862, 2866, 3401,
  3410, 3710); `-i 'per its PE bit|PE = 0|PE = 1|MU = 0|MU = 1'` (listed above);
  requirement-ID grep for R-CNT-12/15/18/22, R-WRT-04/05/06/08, R-LIF-01,
  R-CNF-01/05.

## Derived numbers

The charter names no figure to recompute. Counted: table rows = 3 (3415–3417);
licensed classes under the paragraph + table = 2 (unimplemented stored
MU = 0/PE = 0; implemented-unregistered definition MU = 0/PE = 0) vs hunk 11's
1 class; §21.6 capability refusals named = 2 (foreign major, unimplemented MU = 1),
matching [R-ERR-04]'s "the two". Hunk line positions verified: 3135–3138, 3417.

## Rejected candidates

1. "§20.1's appender list omits dropping records" — dropped: the list also omits
   shrinks and unstores that §20.3 permits, so it is descriptive, not closed.
2. "The SHOULD-report does not reach a compactor" — dropped: §20.1 puts compactors
   under [R-CNF-06] and the MU = 1 row lists compactor duties under "Updater
   obligation", so "updater" includes it; and the sentence is unchanged from the
   old cell.
3. "'its extent becoming slack' is wrong for a (0, 0) record" — dropped: vacuous,
   not false; header/inline payload fall to slack with the superseded directory.
4. "A drop-only commit is not a commit [R-LIF-02] admits" — dropped: step 2's
   "any new record extents" and "for the layers it changes" admit zero; the
   128-byte floor is derived from directory + trailer alone.
5. "§21.6 row's [R-WRT-08] citation does not cover 'dropped per its PE bit'" —
   noted but dropped as a finding of these hunks: pre-existing, the row's text
   matches the cell better now than before, and the drop rule has no ID to cite.
6. "'unregistered' is a new term" — folded into A-01 rather than filed alone: the
   term is intelligible (§10.3 uses it), and the defect is the key it chooses,
   not the word.
7. "The compactor's 'whenever it rewrites' collides with the MU = 1 row's refusal"
   — dropped: refusal means no rewrite, so the MAY is vacuous there, not
   contradicted.
8. "The old cell's citations were needed and are gone" — dropped: each cited a
   clause of the deleted reasoning; nothing in the new cell needs them.

## Findings

### A-01 — Hunk 11's "for no other" fixes the licensed class by *stored* bits and by registration; §20.4 fixes it by *authoritative* bits and by implementation

Location: §20.3 step 2, lines 3135–3137. Quotation: "MUST NOT drop the record save
where §20.4's table licenses the drop, which it does for an unregistered record
stored MU = 0, PE = 0 and for no other."

Contradicting text: §20.4 lines 3406–3411: "For a type the updater implements that
this specification does not register, the definition it implements the type from
supplies the flags, and the stored bits never do ([R-CNT-22], §10.3). For a type
the updater does not implement, the stored flags are authoritative".

The two disagree for an implemented experimental-range type whose stored bits
differ from its definition, in both directions (table above). The old text cited
"§20.4" — the section, which includes the paragraph; the repair narrowed the
citation to "the table" and then asserted the table's reach with the wrong key.
Check types: OVERCLAIM ("for no other"), LOCAL_CONTRADICTION with the paragraph,
and a CITATION narrowing. Byte-level: yes, in a narrow corner — experimental type
T, updater implements T, T's definition says PE = 1, a record of T stored
MU = 0 / PE = 0 (conforming file: experimental values are conforming, and no
register row checks an unassigned type's flags). Updater A, following step 2's
gloss, emits a directory without the record; updater B, following §20.4's
paragraph, must retain it. Both outputs are conforming files; the emittable set
differs. Mitigation that keeps it narrow: §20's preamble says each step "cites the
rule whose outcome governs it", and the clause itself defers to §20.4 — but the
gloss is the only place a reader of step 2 is told the class, and it is wrong.

Repair: either cut the gloss — "MUST NOT drop the record save where §20.4
licenses the drop." — or key it correctly: "which it does for a record whose
authoritative flags under §20.4 — the stored bits, for a type the appender does
not implement — are MU = 0, PE = 0, and for no other." Cutting is the safer of
the two given that the paragraph is the authority.

### A-02 — The cell's unconditional "in any commit, including one whose only effect is the drop" collides with the MU = 1 row's layer block and with step 2's reject-layer bar

Location: §20.4 table, line 3417. Quotation: "an updater MAY drop the record in
any commit, including one whose only effect is the drop".

Contradicting text (untouched): §20.4 line 3415, MU = 1 row: "The updater MUST NOT
modify the scope the record governs. At layer scope an unknown critical record
blocks modification of that layer, leaving other layers editable ([R-CNT-18])."
And §20.3 step 2, lines 3123–3125: "reject-layer bars a commit that modifies that
layer."

A layer L carrying an unimplemented MU = 1 sub-record X and an unimplemented
MU = 0 / PE = 0 sub-record Y: dropping Y re-emits L's record with a different
inline payload, which [R-WRT-05] counts as modifying L. The MU = 1 row forbids
that; the new cell says "any commit, including one whose only effect is the
drop". Under the old cell the drop of a sub-record was conditioned on an
independent change to L's record, which the MU = 1 row already barred, so the
two rows could not meet; the widened licence meets it. Same for a sub-record of a
layer the open rejected. At file scope both bars are vacuous (no commit exists).
Check type: LOCAL_CONTRADICTION / OVERCLAIM ("any"). Byte-level: yes — updater A
reads "any commit" and emits a conforming directory with L lacking Y; updater B
reads the MU = 1 row's MUST NOT as governing and retains Y. Both outputs are
conforming files. A reader applying the BCP 14 convention that a MAY yields to a
MUST NOT would side with B, which is why this is filed as a contradiction the
text should not leave to convention rather than as a certain fork.

Repair: "so an updater MAY drop the record in any commit it is otherwise free to
make — a commit whose only effect is the drop included — and a compactor MAY drop
it whenever it rewrites the file." (The "otherwise free to make" clause picks up
the MU = 1 row's layer block and step 2's scope bars without restating them.)

## Per-check verdicts

1 TENSE/QUANTIFIER: cell passes; step's quantifier mismatches its source → A-01.
2 CITATIONS: all resolve; the narrowing from §20.4 to "§20.4's table" is part of
  A-01.
3 NORMATIVE PLACEMENT: both land in unlabeled normative text; pass.
4 LOCAL CONTRADICTION: A-02 (cell vs MU = 1 row / step 2 reject-layer bar); A-01
  (step vs §20.4 paragraph).
5 OVERCLAIM: "for no other" (A-01); "any commit" (A-02).
6 UNCONSTRAINED SIBLING: every quantity the row touches is fixed by some rule;
  the implemented-type seam is pre-existing and is what A-01 trips on.
7 ANALOGY: none in hunk 11; the cell's PE-meaning argument is the definition
  itself; pass.
8 ANAPHOR: no back-reference re-resolves; pass.
Restatements swept: the old conditioning survives nowhere (sweeps at 0 with
controls). §20.5, §23.1, §21.6, §2.4, Appendix H still describe the cell.
