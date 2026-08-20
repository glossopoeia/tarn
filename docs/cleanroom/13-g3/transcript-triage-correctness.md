# Round 13 triage — correctness lens — working transcript

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — §2.1–2.5,
§4.7, §5.1–5.2, §6.1–6.2, §7.2–7.4, §9.7, §10.2–10.3, §11.1–11.4, §14.2,
§15.1–15.2, §16.1–16.2, §17.3–17.4, §18.2, §19.1–19.2, §20.3, §21 entire,
§24, Appendix G, Appendix H, front matter. Ran one `python3` count over the
§21.2–§21.5 tables and three `grep`s (`renumber|positional|struck|row label`;
the §21.9 guarantee figures; section headings).

Did **not** read any `transcript-triage-*.md`. I listed the round13 directory
once (`ls`) before reading the instruction line about not listing it — the
listing showed only `build.py, calc.py, file1.py, q.py, transcript-adversary.md,
transcript-diagrams.md, transcript-quiz-answers.md, transcript-quiz-author.md,
transcript-quiz-key.md, transcript-reader.md, transcript-register.md,
transcript-verifier.md, transcript-writer.md, verify.py` — i.e. no triage file
existed at that moment and I opened none. I also opened none of the walk
transcripts; every claim below was checked against `spec/tarn.md` directly.
Did not read docs/, PLAN.md, AGENTS.md, conformance/, registry.json, git log,
or the web.

## Mechanical checks I ran myself

- §21.2–§21.5 row count and instance count, computed from the cells as
  written (semicolon split, `—` = 1): **121 rows, 264 instances**. §21.8's
  "121 conditions over 264 instances" is arithmetically correct. So every
  instance-criterion finding is about *unevenness of cell-writing*, not about
  a miscount.
- `grep -n "renumber\|positional\|is struck\|row label"` → hits only at §2.2
  (identifiers never renumbered), §11.1 (ordinals), §20.3 (ordinals), §24
  (the sentence under dispute). §21.1 carries no such statement. The three
  reporters who said so are correct.
- `grep` for each §21.9 guarantee figure (4096, 65,536, 16 MiB, 256 MiB,
  8 MiB, 2³²) → only §21.9, Appendix B (non-normative), §17.2's citation of
  the 8 MiB window and §18.2's Note on 16 MiB. register-05's factual premise
  holds.
- §14.2: `Q = Σ Bᵢ over all channels`. One uint8 channel ⇒ Q = 1 ⇒
  byte-shuffle at s = 1 is the identity (§17.3: "byte i of group j at
  i·n + j", with s = 1, n = L, i = 0 ⇒ offset j). writer-02's witness 1 is
  arithmetically sound.
- [R-GEO-06]: s = Σᵢ tᵢ·∏_{j>i} Gⱼ. The i = 0 term's product excludes G₀, so
  raising G₀ alone leaves every existing s fixed. Checked diagrams-02's
  (4,4)→(7,4) worked case: entries 0–15 keep their ordinals. Sound.
- writer-03's slab witness recomputed: G=(2,2), s = 2t_y+t_x ⇒ tiles at
  ordinals 0,1,2,3 / offsets 4096,4097,8192,8193; runs [0,2),[2,4) both
  packed and A_slab-aligned. Grow x 2→3: G=(2,3), s = 3t_y+t_x ⇒ old
  tile(1,1) moves to ordinal 4, which is the first ordinal of run [4,6);
  8193 mod 4096 = 1 ⇒ L42. Sound.

## Grouping

24 ids → 14 groups.

| group | ids |
|---|---|
| metadata-encoding-unassigned-vs-reserved | reader-01, writer-01, diagrams-03, adversary-02 |
| instance-criterion-uneven | reader-02, diagrams-01, register-03 |
| appendix-g-record-order-circular | writer-04, diagrams-04, adversary-04 |
| vec02-cites-2101-for-row-renumbering | verifier-02, diagrams-06, register-01 |
| f33-gloss-drops-third-overlap-case | register-04, adversary-03 |
| wrt04-declaration-freeze-overclaim | writer-02 |
| slb04-trigger-misses-run-repartition | writer-03 |
| partial-slack-rejected-layer-claimants | verifier-01 |
| geometry-change-renumbers-ordinals-false | diagrams-02 |
| layout-table-column-convention | diagrams-05 |
| 2107-omits-cnt18-nesting | register-02 |
| 2109-finding-aid-framing | register-05 |
| front-block-check-verifier-obligation | adversary-01 |
| rationale-bars-shrink-flatly | adversary-05 |

Grouping notes:

- writer-02 vs adversary-05 kept **separate**. They share a topic (what a
  commit may change) but not a defect. adversary-05's witness (E 5→4, T=4,
  one stored tile with no padding either side) is permitted under *both* of
  writer-02's readings, because §20.3's enumeration is already scoped "for
  any tile that layer stores" and the disappearing tile was the sentinel. So
  adversary-05 is a Rationale-vs-rule mismatch that survives however
  writer-02 is resolved, and the repairs are in different sentences.
- writer-01 folds two extra seams into one finding (Appendix H's line; F27/L48
  missing the "assigned encoding" qualifier). Both are the same seam as its
  headline, so the id stays in the encoding group and the repair names them.
- writer-04 folds Appendix G item 2's all-zero-digest substitute into its item-3
  finding; same group, named in the repair.

## Judgements, with the text that decides each

### 1. metadata-encoding-unassigned-vs-reserved — CONFIRMED, not byte-level

Checked: §10.2's table gives metadata encoding assigned 1,2 / reserved
3–0x7F / experimental ≥0x80, and "Value 0 is invalid in every space above".
§21.5's preamble is quoted accurately by all four reporters. R1 exists and
reads as quoted. §21.6's only metadata-encoding row is scoped
"experimental-range (≥ 0x80)". So the preamble's "except at an unassigned
encoding … and §21.6 records the defined non-violation" promises a §21.6
entry that does not exist for 0 or 3–0x7F. The defect is real, and the word
the preamble wants is *experimental*.

Downgrade quotations (four, independently sufficient):

1. §21.5, the sentence immediately after the one complained of: "Every row
   here is a violation all the same: the outcome bounds a reader's blast
   radius and never makes the file conforming (`[R-CNF-12]`); §21.6 lists the
   ignore-record conditions that are not violations." R1 is a row here.
2. §18.2 [R-MTA-10]: file conformance "is decided by the structural checks
   that precede the document alone: the record's framing and extent slot
   (`[R-CNT-13]`), **the encoding byte's own value set (`[R-MTA-03]`)**, and
   the extent's terminal CRC (`[R-CNT-20]`)" — the value-set check survives
   expressly, and the certification clause is guarded "in an otherwise
   conforming file".
3. §10.3 [R-EXT-03]: "a value from a reserved range MUST NOT be emitted at
   all before this specification assigns it".
4. §21.1: "where a row and the rule it cites diverge, the rule governs" —
   R1's cited rules are [R-CNT-25] (R-MTA-03, R-EXT-03), all three of which
   support R1.

Reading (a) — "unassigned covers reserved, so encoding 5 certifies" — is not
merely outvoted; it is self-refuting, because it relies on §21.6 recording a
non-violation that §21.6 demonstrably does not record. Appendix H's echo sits
in text that disclaims itself: "each entry's authority is the requirement or
section cited, never this summary." No reader behaviour changes either way
(ignore-record under R1 and under §21.6 alike), and no writer may emit the
byte under either reading. Not byte-level.

Repair: §21.5 preamble, "unassigned" → "experimental"; Appendix H's verifier
line likewise; optionally add "under an assigned encoding" to F27 and L48,
which R3 and R4 already carry and which [R-MTA-10] supplies globally.

### 2. instance-criterion-uneven — CONFIRMED, not byte-level

Verified every cell cited. T3 = 6, T14 = 6 (longer/shorter × three layouts);
T22 = 3 and T21 = 3 (layouts only); L21 = 1 (`—`); L22 = 3 with the plain
inequality unsplit; L30 = 1; L44 = 3. The rows are structurally alike and
counted three ways. My own count of the tables reproduces 121/264 exactly, so
§21.8's total is right about the cells as written and wrong about nothing.

Downgrade quotation: §21.1 — "Instances within a cell are separated by
semicolons, and a cell reading — is one instance; **the count is therefore
mechanical once the cell is written**." The criterion locates the discretion
in the cell, not in the count; and §24 [R-VEC-01] makes the corpus
derivative: "where a vector's recorded expectation and this specification
disagree, this specification governs". Nothing a reader does with any file
turns on how many vectors exercise T14 versus T22; T14/T22/L21/L22 reject the
same tiles and layers under any counting, via [R-COD-04], [R-COD-06] and
[R-CNT-17]. Not byte-level; this is register bookkeeping with a corpus-size
consequence.

Note for the maintainer: this is the third round in which the same asymmetry
has been reported, and the earlier repair (T3/T14) moved the inconsistency
rather than removing it. Whatever is decided, §21.8's stated total and
[R-VEC-03]'s obligation move with it.

### 3. appendix-g-record-order-circular — CONFIRMED, not byte-level

Verified §7.2's header layout: type(0,2) flags(2,2) inline_length(4,4)
extent_offset(8,8) extent_length(16,8). So a lexicographic comparison over
"encoded bytes" reaches extent_offset once type, flags and inline_length tie,
and item 3 fixes extent placement by "ascending record order" — the very
order being defined. Two fixed points, both self-consistent, as all three
reporters describe. [R-CNT-14] caps 0x0002 at one per scope; L26 keeps 0x0001
out of sub-record sequences and item 3 already patches 0x0001 by layer name.
So the general clause is exercised only by unassigned types, which
[R-CNF-02] and §21.6 make conforming as bytes for the experimental range.
The alternative "payload-only" reading leaves the same case tied. Claim
"A total emission order" is false as written.

Downgrade quotation: Appendix G's own opening — "It adds no requirement to
any actor: **a writer ignoring it is fully conforming**" — and the appendix
heading "(non-normative)", with §2.1: "All text in this document is normative
except … appendices identified as non-normative." Both fixed points are
conforming files. Not byte-level.

Repair needs a maintainer decision, not an edit: choose a placement-independent
tie-break for same-type records (e.g. compare the header with the extent slot
masked out, then inline payload, then extent_length, then declare a residual
tie an input the profile does not admit). Item 2's "with any other fixed
nonzero value substituted" has the same shape and wants the same treatment
(name the substitute).

### 4. vec02-cites-2101-for-row-renumbering — CONFIRMED, not byte-level

Grep confirms §21.1 says nothing about positional labels, striking a row, or
renumbering; the proposition exists only in §24. §21.1's actual content is the
completeness clause, the row-versus-rule precedence rule, the specialization
list, the Instances criterion and the Detected vocabulary. diagrams-06's list
of ~15 label-citing cross-references checks out on inspection (§9.6's "F8 and
F17", §17.2's "(§21.4, T24)", §21.1's own specialization list, F33's bounds
list, T2/T13/T15/T16/T23/T26's "the check that detects it is …", §21.6's
"(F18, [R-CNT-07])" and "(F35, F36, L24, L25)", Appendix H's "([R-CNT-05],
F7)" and "([R-CNT-15], F36, L25)").

Downgrade quotation: [R-VEC-02]'s own obligation is "the §21 register row it
exercises **together with** that row's governing requirement identifier", and
§2.2 "Identifiers are stable: they are never renumbered or reused". The
manifest records the pair under either label policy, so no corpus and no
implementation diverges. Not byte-level.

Repair: drop "(§21.1)", or state the labelling policy in §21.1. The latter is
a maintainer decision because ~15 in-document citations depend on labels being
stable, which is in tension with §24's assertion that they renumber.

### 5. f33-gloss-drops-third-overlap-case — CONFIRMED, not byte-level

[R-CNT-13] names three cases verbatim: intra-layer → reject-layer; "any
overlap across layers or touching another scope's structures" → reject-file;
"any overlap between two structures neither of which belongs to a layer" →
reject-file. F33's em-dash gloss carries the first two of the reject-file
pair and drops the third. F33's head clause ("two structures that do not
belong to the same layer") does cover it, and F33's Instances cell already
lists "record extents" and "directory region", a pair reachable only in the
dropped case. So the row is internally inconsistent, not wrong.

Downgrade quotation: §21.1 — "each row *restates* its governing rule, and
where a row and the rule it cites diverge, **the rule governs**." Both
readings give reject-file, so no verdict forks. Not byte-level.

Repair: extend F33's gloss with "or two structures neither of which belongs
to a layer".

### 6. wrt04-declaration-freeze-overclaim — CONFIRMED, not byte-level (closest call in this batch)

All three witnesses check out against the text. (1) §17.3 [R-COD-10] makes the
interleaved shuffle stride Q, §14.2 makes Q = ΣBᵢ = 1 for a single uint8
channel, and the shuffle at s = 1 is the identity; so filter 1→2 on such a
layer changes an enumerated property and alters nothing about any stored
tile. (2) A shrink whose new padding positions already hold fill changes "the
set of padding positions" while leaving every stored tile conforming.
(3) §20.3 itself says two sentences later "an extent MAY always **grow**",
and a growth alters the padding-position set of every stored edge tile — so
the enumeration already carries a stated exception. Therefore the sentence
"Every such change makes each stored tile it reaches nonconforming" is false
as a universal, and the enumeration cannot be read as an absolute list.

Downgrade quotations: §2.3 [R-CNF-02] — "**File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or
environment**" — and §9.7's Note, "Nothing here enumerates prior commits. A
verifier certifies what a reader can reach and counts what it cannot, which
is decidable from the live trailer in one pass and does not depend on
reconstructing the file's history". The file that the permissive updater
commits is conforming under either reading — a creator could emit it from
scratch — and nothing in the finished bytes records that a commit, rather
than a fresh emission, produced it. So no verifier verdict, no reader
accept/reject and no creator's emission set forks; what forks is one
updater's permission to reach a legal file by a commit. That is an actor
property of the kind [R-CNF-02] separates from the byte predicate.

I record this as the group closest to the byte-level line, because the fork
is in what a *conforming updater may emit next*, and a reader of the test's
words could stop there. It does not cross, because the emitted byte sequence
is the same sequence under both readings and is conforming under both.

Repair (maintainer decision): either restate the enumeration as elaboration
of the preamble's effect test — "in a way that alters … — that is, the set of
padding positions, …" — and delete or qualify "Every such change makes each
stored tile it reaches nonconforming"; or keep the enumeration literal, name
the growth exception as an exception to it, and add the residual case to
§21.7's account of obligations with no single-file witness.

### 7. slb04-trigger-misses-run-repartition — CONFIRMED, not byte-level

Recomputed the witness above; it holds. [R-SLB-02] partitions runs
positionally ("Run r of a block starts at ordinal block_start + r·S"), so a
growth that changes G and N re-partitions runs without moving a byte, and
[R-SLB-04]'s trigger ("changes the stored-tile set or the byte placement of
any run") does not plainly name that case.

Downgrade quotations: [R-SLB-03] binds without a trigger — "**When declared,
for every run:** the run's stored tiles are contiguous and packed … and the
first stored tile's offset satisfies offset mod A_slab = 0" — and §2.3
[R-CNF-05], "A writer MUST emit only conforming files", which [R-CNF-06]
extends to updaters. An updater that keeps the declaration emits a file L42
registers as a violation under either reading of [R-SLB-04]; one that clears
it emits a conforming file under either. Not byte-level.

Repair: broaden [R-SLB-04]'s trigger to name the run partition —
"whose commit changes the stored-tile set, the run partition, or the byte
placement of any run".

### 8. partial-slack-rejected-layer-claimants — PARTIAL, not byte-level

The grammatical observation is right: "a rejected layer's claimants are not
enumerated, whether or not the rejection impeded reading them" is declarative,
and the trailing clause does real work only if the non-enumeration is fixed
rather than permitted. §9.7 says the same declaratively ("a scope-level
rejection blocks enumeration"). So reading (a) is the plain one and reading
(b) strains.

But the consequence the reporter draws — two conforming verifiers printing
different numbers with "no way to adjudicate" — is expressly anticipated and
licensed. §5.2's Note: "**A partial total (`[R-CNT-21]`) reports what one
verifier's incomplete walk left unclaimed, which is a fact about that run and
not about the file's live state.**" And [R-CNT-21] itself: "It is not the
file's slack total but a bound on it, tightening to the exact total when the
walk completes." A partial total is run-relative by construction; two runs
differing is the defined behaviour, not a defect. Hence PARTIAL: the defect
is the aside's grammar, not an unadjudicable divergence. Not byte-level — no
verdict and no byte moves, and for a conforming file the walk completes and
both readings give the same number.

Repair: recast the aside as the constraint it is — "…because a scope-level
rejection ends that scope's enumeration, a rejected layer's claimants being
left unenumerated whether or not the rejection impeded reading them…" — or,
if the permissive reading is intended, say so explicitly.

### 9. geometry-change-renumbers-ordinals-false — CONFIRMED, not byte-level

Arithmetic verified above; the gloss is false for interleaved growth of the
first-declared dimension and for every rank-1 layer, and true for planar
layers whenever N changes and for interleaved growth of any non-first axis.
Both sites carry it (§11.1 Rationale, §20.3 step 4's parenthetical).

Downgrade quotation: the obligation the parenthetical annotates is "every
other entry **byte-identical at its disk-ordinal position** (a geometry
change renumbers ordinals, `[R-GEO-06]`)", and [R-GEO-06] is the document's
only ordinal formula: "the **spatial tile ordinal** … is s = Σᵢ tᵢ · ∏_{j>i}
Gⱼ." A writer computes the position from the formula; the parenthetical
offers no alternative procedure, so two writers emit identical index regions.
Not byte-level; the damage is to a reader's mental model, and §11.1's site is
Rationale, non-normative under §2.1.

Repair: "a geometry change **may** renumber ordinals" in both places, or state
the condition (planar with N changed; interleaved with a non-first grid count
changed).

### 10. layout-table-column-convention — CONFIRMED, not byte-level

Audited all six tables. §6.2 trailer, §15.1 index entry and §18.2 metadata
payload deliver all six columns. §6.1 delivers Offset/Size/Value/Class (four,
Value standing in for type, name and range). §7.2 delivers
Offset/Size/Type/Field/Class (five, ranges folded into the Field cells).
§7.4 delivers Field/Type/Constraint (three, where the stated carve-out would
leave four). The reporter's count is exact.

Downgrade quotation: the passage is a Note, and §2.1 [R-CNF-01] — "All text
in this document is normative except … any text labeled *Note*, *Example*, or
*Rationale*". The front matter already hedges: "layout tables whose columns
suit the structure". Every field's offset, width, type and range remains
recoverable. Not byte-level.

Repair: soften §4.7's Note to the front matter's phrasing, or name §6.1 and
§7.2 as further carve-outs beside §7.4's.

### 11. 2107-omits-cnt18-nesting — CONFIRMED, not byte-level

§21.7's second paragraph lists six rules ([R-LIF-01], [R-LIF-03], [R-GEO-06],
[R-SER-01], [R-CNT-13]'s no-embedded-offsets clause, [R-ENC-06]) — the
reporter says "five", a harmless miscount that does not affect the point.
[R-CNT-18]'s nesting prohibition is in none of them, and its account lives
only in §7.4's Note, on a different ground: "in format major 1 it has no
reader-detectable witness, and so no register row."

Downgrade quotation: §21.1 hedges — "§21.7 the account, **by class**, of what
fails it" — and §21.7 introduces its list as "**A second set** of obligations
is omitted", not as an exhaustive one. Nothing about any file changes. Not
byte-level.

Repair: add the undetectable-by-parse class to §21.7 (one clause naming
[R-CNT-18]'s nesting prohibition and pointing at §7.4's Note).

### 12. 2109-finding-aid-framing — CONFIRMED, not byte-level

Grep confirms none of the eight guarantee figures is stated anywhere else
normatively, so "each limit is normative where the structure forcing it is
defined" has no application to the table. The clause is a true description of
the *hard* limits, which the closing paragraph restates in its own words
("They are stated where the structures forcing them are defined").

Downgrade quotation: the same paragraph carries the MUST — "The table below
states **minimum guarantees**, not caps: a conforming reader MUST accept any
conforming file whose quantities lie within these bounds" — reinforced later
by "Software that declines a file whose every quantity lies within the table
is not a conforming reader (`[R-CNF-03]`)", and by §2.5's "the table is
§21.9". Reaching reading (a)'s conclusion requires stopping mid-paragraph.
Not byte-level.

Repair: scope the clause — "and is a finding aid rather than an inventory for
the hard limits below, each of which is normative where the structure forcing
it is defined."

### 13. front-block-check-verifier-obligation — CONFIRMED, not byte-level

Verified all the restatement sites ([R-CNT-04], F1, F6, §19.1 step 1, §19.2's
first bullet, §9.7's claimant sentence) and Appendix H's verifier checklist,
which does omit the front block from "the checks readers are exempt from".
§8.1 states no checksum over [0,16) — §4.5 excepts it — so the reporter is
right that it is the one structure no checksum protects.

Downgrade quotation: §2.3 — "**Conforming verifier.** A reader that
additionally checks every file-level requirement — **including those ordinary
readers are exempted from** — and certifies conformance" — with [R-CNF-11]
restricting *cannot establish* to "a capability or resource ground". A
16-byte range request is neither. Appendix H disclaims itself: "each entry's
authority is the requirement or section cited, never this summary." Not
byte-level; the finding is that a non-normative checklist is incomplete.

Repair: add the front signature block to Appendix H's verifier list.

### 14. rationale-bars-shrink-flatly — CONFIRMED, not byte-level

Witness checked: d=1, E=5, T=4 ⇒ G=2, tile 0 stored with no padding, tile 1
the sentinel; shrinking E to 4 gives G=1 and leaves stored tile 0's decoded
size, sample offsets, padding set (empty both sides) and codec untouched, so
§20.3's prohibition — scoped "for any tile that layer stores" — does not
reach it, while §11.1's Rationale says flatly "Extents grow; they do not
shrink". The converse case (E 8→5, T=4) shows why the rule is written as it
is.

Downgrade quotation: §2.1 [R-CNF-01] — "All text in this document is
normative except … any text labeled *Note*, *Example*, or ***Rationale***" —
so §20.3's rule governs and the Rationale is a gloss; and §2.3 [R-CNF-02],
"File conformance is a pure predicate on bytes", with §9.7's Note that
nothing enumerates prior commits, so no verdict on any file turns on which
sentence an updater followed. Not byte-level.

Repair: §11.1's Rationale — "Extents grow; a shrink is barred wherever it
alters what §14 fixes for a stored tile (§20.3)".

## Byte-level tally

0 of 14 groups byte-level. Every downgrade above carries a quotation from the
text that decides it. The group I would re-read first if only one could be
re-read is #6 (wrt04-declaration-freeze-overclaim), because its fork is in an
updater's permission to emit a next generation, and because its normative
sentence contains a claim I could falsify three ways.

## Coverage

24 input ids; 14 groups; each id in exactly one group; union counted twice by
hand: 4+3+3+3+2+1+1+1+1+1+1+1+1+1 = 24.
