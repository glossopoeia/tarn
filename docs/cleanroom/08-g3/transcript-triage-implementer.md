# Round 8 triage — implementer-consequence lens

## What I read and ran

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (3842 lines), in six
  reads: 1–300, 300–700, 700–1099, 1099–1398, 1398–1848, 1848–2298, 2298–2698,
  2698–3038, 3038–3378, 3378–3842. Every section and every appendix.
- No transcripts from `round8/` were read. No `docs/`, `PLAN.md`, `AGENTS.md`,
  `conformance/`, `spec/registry.json`, git history, or web.
- Three mechanical checks over `spec/tarn.md` with awk/grep:
  1. Register rows whose Detector cell is `verifier`:
     F9 F28 F29 F30 F31 F36 F39 L19 L26 L41 L42 L43 L47 L48 L49 L50 T2 T4 T5 T26
     — exactly twenty, matching verifier-05's list.
  2. Row counts per table: F 39, L 50, T 26, R 10 = 125, matching §21.8's
     "125 conditions". Instance counts (semicolon-separated, `—` counted as 1):
     F 61, L 102, T 45, R 44 = 252, matching §21.8's "252 instances" and
     register-04's independent count.
  3. `preserve-verbatim` occurs exactly twice, both inside §2.4 (line 216
     definition, line 226 table row). register-06 confirmed.
  4. Layout tables carrying a `Class` column: §6.1 (644), §6.2 (687), §7.2 (851),
     §15.1 (1879), §18.2 (2313). §7.4's layer-record table (951) is
     `| Field | Type | Constraint |` — no Class column. diagrams-02 confirmed.

## Grouping

23 groups over 33 ids. Two ids from one reporter were split (adversary-04 carries
both the Appendix-H SHOULD item and the reader-checklist omission; I placed it
with the SHOULD group, its titular first item, and cross-referenced the other).

| group | ids |
|---|---|
| f36-detection-tier-misstated | reader-01, diagrams-04 |
| lif08-closing-drops-structural-qualifier | reader-02 |
| idx03-slack-gloss-additive | verifier-03 |
| enc12-missing-quarantine-carveout | reader-03 |
| lif08-walk-omits-subrecord-extents | reader-04 |
| wrt08-mu1-file-scope-vs-reject-file | writer-01 |
| wrt08-another-top-level-record-scope | writer-02, quiz-01 |
| lif02-creation-offset-16 | writer-03 |
| overlong-pretrailer-pad-unregistered | writer-04, verifier-01 |
| example-c-fill-change | verifier-02, diagrams-01 |
| layer-record-table-no-taxonomy-class | diagrams-02 |
| apph-writer-should-among-musts | diagrams-03, adversary-04, quiz-03 |
| apph-reader-drops-metadata-encoding | diagrams-06 |
| apph-verifier-checklist-incomplete | verifier-05 |
| f21-not-a-byte-defect | register-01, adversary-03 |
| l24-name-overrun-tier | register-02 |
| enc06-no-tile-scope-cause-row | register-03 |
| l2-container-axis-collapsed | register-04 |
| err05-hard-limit-inventory-short | diagrams-05, register-05 |
| preserve-verbatim-unbound | register-06 |
| cnf11-unable-to-check-unscoped | verifier-04, adversary-01 |
| cnf02-conduct-list-under-inclusive | adversary-02 |
| lif08-omits-f9-gap-check | quiz-02 |
| appg-profile-degrees-of-freedom | writer-05 |

Deliberate non-merges:
- reader-02 vs verifier-03 sit in the same two sentences but are different
  defects: reader-02 is about *which* entries lose their extent (structural vs
  crc-failing); verifier-03 is about the *arithmetic* of the slack total. Fixing
  one does not fix the other.
- quiz-02 (§9.7 does not state the F9 check) vs verifier-05 (Appendix H's verifier
  list omits it) are two places, two edits.
- writer-04/verifier-01 (over-long pad, a *detectable* obligation absent from the
  register) vs adversary-02 ([R-CNF-02]'s conduct list omits *undetectable* writer
  prohibitions). Shared root — the conduct-rule carve-out is stated by
  enumeration — but different repairs. Flagged for joint repair in both groups.

## Byte-level judgements

Two groups fork the bytes. Both live in §20.4's `[R-WRT-08]` persistence table.

### wrt08-mu1-file-scope-vs-reject-file (writer-01) — BYTE-LEVEL

The row says, for a type the updater does not implement:

> at file scope it blocks any modification of file-scope structure — adding,
> removing, or reordering top-level records — **while a commit that only changes a
> layer's own tiles, index, or record remains permitted**.

Against it:
- §7.2 `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file".
- §2.4: reject-file — "A reader MUST NOT rely on any structure in it."
- §2.3 `[R-CNF-11]`: "Verifiers and updaters are readers of the files they process
  and inherit every reader obligation."
- §20.3 step 2: "**Open.** Perform §19.1's open (`[R-RDR-01]`) — the appender is a
  reader here."
- §19.1 step 4: the record walk applies "the MUST_UNDERSTAND gate for unknown
  top-level types (`[R-CNT-15]`)".

So the appender's own mandated procedure obliges it to reject at open, and the
final clause of the MU = 1 row's file-scope half becomes wholly inoperative text.
A contradiction that renders one text entirely dead is the classic mark of a live
fork rather than a settled question — the drafters wrote an explicit contrast
("blocks X while Y remains permitted"), which is not how one writes a clause one
believes unreachable. I checked whether `[R-WRT-06]`'s separate compactor refusal
makes reading (i) redundant, as writer-01 argues: it does not, because
`[R-WRT-06]` also covers layer-scope MU = 1 sub-records, which are reject-*layer*
and so not caught by reject-file. That weakens writer-01's argument without
resolving the contradiction.

Concrete divergence: same generation-1 file, one top-level experimental-range
record with MU = 1 that neither updater implements, instruction "supersede tile 1
of layer elev". Updater A appends a new payload, a full re-emitted index region, a
directory and a trailer, and the file grows to generation 2. Updater B emits
nothing. Both resulting files are conforming files (§21.6: an experimental-range
MU = 1 record leaves the file conforming), so no verifier verdict distinguishes
them and nothing downstream corrects the fork. What is at stake is which byte
sequences a conforming updater may emit — the byte-level test as written.

### wrt08-another-top-level-record-scope (writer-02, quiz-01) — BYTE-LEVEL

> An appender may drop it only in a commit that *independently* changes the scope
> the record attaches to: for a layer sub-record, that layer's record, index, or
> stored tiles; for a top-level record, the file's layer set or **another
> top-level record**.

Reading A (a layer record is a top-level record, so a tile commit that re-points
its extent slot licenses the drop) is supported by §7.3, which scopes type 0x0001
to "file", and by the register's own vocabulary: F3, F28, F29, F31, F33, F34, F35
all say "**non-layer** top-level record" precisely when they mean to exclude layer
records, while F27 and F32 say "top-level record" unqualified and plainly include
them.

Reading B is supported only by the MU = 1 row's gloss. I checked that gloss and it
is weaker than quiz-01 claims: "adding, removing, or reordering top-level
records ... while a commit that only changes a layer's own tiles, index, or record
remains permitted" establishes that *modifying* a layer record is not
*adding/removing/reordering*, which is true whether or not a layer record is a
top-level record. It does not establish that a layer record is not one. The other
support for B is redundancy — under A, "the file's layer set" is subsumed by
"another top-level record" — but that redundancy dissolves if "another top-level
record" is read as an existing other record the commit modifies, which is itself a
natural reading.

Nothing in the document settles it. Concrete divergence: same file carrying a
top-level MU = 0 / PE = 0 ancillary of an unimplemented type, same instruction
"supersede tile 5 of layer A". Appender X emits a four-record directory carrying
the ancillary's 24-byte header and inline payload, with its extent live. Appender
Y emits a three-record directory, the ancillary's extent demoted to slack. Different
dir_length, different terminal directory CRC, different pad, different
committed_file_length. Both files conform; exactly one appender satisfies
`[R-CNF-06]`, and this text does not say which. Application state disappears on a
routine tile update under one of the two.

## Every downgrade, with the sentence that decides it

### f36-detection-tier-misstated (reader-01, diagrams-04) → register-bookkeeping

The cell is wrong: L17/L18 carry Detected = layer access, T8/T9 carry tile use.
Confirmed against the rows. Not byte-level:

> §19.2 `[R-RDR-02]`: "A reader MAY detect any violation earlier (`[R-CNF-12]`)".
> §21.1: "where a row and the rule it cites diverge, **the rule governs**."

Both readings reject the same files at the same scopes. diagrams-04's worry that a
reader might eagerly fetch every index region at open is real as a performance
matter but not a conformance one: §6.4's Note says "no request count is a
conformance property, and nothing here bounds what a reader fetches."

### lif08-closing-drops-structural-qualifier (reader-02) → editorial

Decided three times, twice within reach of the sentence:

> §9.7, same paragraph, opening: "an entry `[R-IDX-03]` classifies reject-tile on a
> *structural* ground contributes no stored extent to the walk; one whose stored
> bytes alone fail its crc keeps its extent".
> §15.3: "An entry whose only defect is that its stored bytes fail its crc is
> well-formed ... so its extent stands and it keeps its place in the *verifier*
> rows, in run continuity, and in the coverage walk."
> §16.2 `[R-SLB-03]`: "An entry whose only defect is that its stored bytes fail its
> crc is not transparent — its offset and length stand".

The third of these is the one reader-02 worried about (an L42 verdict turning on
it), and it is decided in §16.2 in exactly those words.

### idx03-slack-gloss-additive (verifier-03) → editorial

verifier-03 is right that the gloss read additively is not merely different but
impossible. §9.7 claims the front block for the walk ("The front signature block at
[0, 16) and the live trailer at [F − 64, F) are claimed by the walk as well"), so
adding a T8 entry's nominal [8,12) to the slack total double-counts claimed bytes;
a T9 entry's nominal extent runs past physical end of file; T11/T12's nominal
extents are not representable. Not byte-level: the slack total is a report figure,
§9.7's set-complement definition governs the arithmetic —

> §9.7: "Bytes the walk does not reach are slack: the verifier sums them and
> reports the total, and their content is not its concern."

— and every file exhibiting a structural entry is already nonconforming on
T6–T12. Real defect all the same; the sentence should not survive as written.

### enc12-missing-quarantine-carveout (reader-03) → editorial

Decided four times, once with an explicit override of the very mapping
`[R-ENC-12]` invokes:

> §7.1 `[R-CNT-25]`: "content violating the document's own rules (ill-formed UTF-8
> included, `[R-ENC-11]`) — is ignore-record with a SHOULD-report, **notwithstanding
> the owning-scope mapping of `[R-CNF-08]`**."
> §18.1 `[R-MTA-02]`: "the outcome of every failure to read its **document** is
> ignore-record whatever the scope".

`[R-ENC-12]`'s phrase "a validity error at the owning scope" is *defined by*
`[R-CNF-08]` (§2.4), so `[R-CNT-25]`'s "notwithstanding" clause reaches it
directly. Plus `[R-MTA-04]`'s fourth restriction folds §4.6's name rules into the
document's own rules, and R6/R10 register both cases with outcome ignore-record.
Editorial, but a worthwhile one-clause fix: `[R-ENC-11]`, one paragraph earlier,
carries exactly the carve-out `[R-ENC-12]` lacks.

### lif08-walk-omits-subrecord-extents (reader-04) → editorial

> §7.4 `[R-CNT-18]`: "Sub-records are layer-scope records".
> §7.2 `[R-CNT-13]`: "a verifier MUST treat an intra-layer overlap — including a
> stored extent overlapping its own layer's index region or **sub-record extents** —
> as reject-layer".
> L19 Instances: "stored-tile extents; tile-index region; layer sub-record extents".

The walk must reach them; "the live directory and its records" ranges over records
generally, as §9.7's own demonstration about a layer record's index region shows.

### lif02-creation-offset-16 (writer-03) → editorial (PARTIAL)

Decided in the creation section itself:

> §20.2 `[R-WRT-02]`: "each layer's stored tiles, tile-index region, and any record
> extents, in any order satisfying §5.2's coverage classes (`[R-CNT-02]`,
> `[R-CNT-03]`) and every declared layout invariant (`[R-SLB-01]`, `[R-SLB-03]`) —
> **placement is otherwise free** (`[R-SLB-05]`)".
> §16.1 `[R-SLB-01]`: "The bytes alignment leaves between structures are slack
> (§5.2), which writers SHOULD zero and no conformance requirement constrains."

The strict reading also fails a reductio on ordinary appends: step 1's "begin
writing at exactly F" would forbid an aligned layer from placing its first new tile
at the next A-multiple past F, which §16.1 expressly contemplates as slack. Both
creators' files are conforming and no reader or verifier can tell them apart, so
no single byte sequence is judged differently. The creation sentence is still worth
a clause saying placement inside step 2 is free.

### overlong-pretrailer-pad-unregistered (writer-04, verifier-01) → editorial

§6.2 settles the file and the commit in one clause:

> "`[R-CNT-05]`: this specification does not constrain their content, and bounds
> their number only through step 5 of the commit protocol, which pads to the next
> 64-byte boundary (`[R-LIF-02]`) — **a longer gap is conforming, and no conforming
> commit produces one**."

verifier-01 picked (a) and writer-04 picked the same substance; both are right.
The residue is real and narrower than either states: §21.1's completeness clause is
not falsified, because §10.3's experimental-value prohibition is likewise
detectable, likewise carries no register row, and is likewise handled in §21.6 —
the register enumerates violations that carry a reader outcome (`[R-CNF-07]`), and
a conduct-only obligation carries none. What is genuinely under-inclusive is
§2.3's *enumeration* of conduct rules, which names §10.3, §18.3 and §6.3 and not
§9.2 step 5. Same root as adversary-02.

### example-c-fill-change (verifier-02, diagrams-01) → editorial

Both reporters are right and their worked instances agree. Not byte-level:

> §2.1 `[R-CNF-01]`: "All text in this document is normative except: §1
> (Introduction); any text labeled *Note*, *Example*, or *Rationale*".
> §14.5 `[R-SER-05]`: "at every padding position, a writer MUST encode, for each
> channel the position carries, that channel's fill value ... a verifier MUST check
> it, and a violation is a validity error at tile scope."

Every conforming verifier condemns the post-(c) file at T4/T5 and every conforming
reader serves it unchanged, so no byte and no verdict is open. But of everything in
this round this is the item most likely to produce a shipped bug: an updater whose
`set_fill()` re-emits only the directory is the natural implementation, and it
silently produces files every verifier rejects tile by tile, on exactly the layers
where fill matters — the ones with ragged edges. diagrams-01's packed-bool case is
worse and correct: a plane with P mod 8 ≠ 0 has pad bits in *every* tile, so no edge
is needed for T5 to fire everywhere.

### layer-record-table-no-taxonomy-class (diagrams-02) → editorial

Confirmed mechanically: §7.4's is the one layout table without a Class column, and
the only three §7.4 fields classified anywhere are linearization (§11.4, "`u16`,
structural"), channel sample type (§12, "`u16`, structural"), and fill (§13.1, "The
fill value is semantic"). Not byte-level:

> §4.7 `[R-ENC-16]`: "A field classified **informative** MUST NOT affect how any
> byte is located or decoded, and a reader MUST NOT alter decoding based on it; each
> informative field's definition states what a reader does when it contradicts the
> data it describes."

That prohibition is the only behaviour a class carries, no §7.4 field is a
candidate for it (each has an explicit normative role in locating or decoding, and
none carries a "what a reader does when it contradicts" clause), and the
structural/semantic line carries no behaviour at all. So decoding is identical
whatever labels an implementer infers. `[R-ENC-16]` is nonetheless unmet by the
document for fifteen fields.

### apph-writer-should-among-musts (diagrams-03, adversary-04, quiz-03) → editorial

> §5.2 `[R-CNT-03]`: "no conformance requirement rides on slack content either way."
> §5.2: slack's "content is unconstrained, and no conformance requirement applies to
> it."
> Appendix H: "each entry's authority is the requirement or section cited, never
> this summary."

Three reporters, one defect, and diagrams-03's sharpest point is the internal
inconsistency: Appendix G draws the SHOULD/MUST line explicitly for this very
requirement ("gap content, which `[R-CNT-03]` only advises and this profile
requires") while Appendix H flattens it. adversary-04's second item is
diagrams-06's subject; grouped there in substance, id placed here.

### apph-reader-drops-metadata-encoding (diagrams-06) → editorial

> §18.2 `[R-MTA-03]`: "Both assigned encodings are core: a conforming reader MUST be
> able to decode encoding 2, whose decoder `[R-COD-11]` already requires of it for
> codec 3".

Encoding 1 is verbatim storage and encoding 2 is the zstd decoder codec 3 already
mandates, so no implementation satisfying the four listed capabilities can fail the
fifth. Nothing happens to an implementer; the list is short by one term of the rule
it cites.

### apph-verifier-checklist-incomplete (verifier-05) → editorial (PARTIAL)

Items (1) and (2) confirmed mechanically: the register has exactly twenty
verifier rows and Appendix H reaches seventeen of them; F9, F39 and L26 have no
line. verifier-05's F9 construction is sound — a claimant in the pre-trailer gap is
inside [16, F − 64), disjoint from every other claimant, and passes its own
checksum, so it survives all three checks §9.7 states.

Item (3) is only partly right. T3, T24 and T25 are reader rows, and Appendix H's
verifier entry opens "every reader obligation, plus the checks readers are exempt
from", which reaches them. What Appendix H does not say — and what verifier-05 is
groping toward — is that a verifier must exercise those obligations over *every*
tile, where a reader exercises them only at tile use. Not byte-level:

> Appendix H: "each entry's authority is the requirement or section cited, never
> this summary."

### f21-not-a-byte-defect (register-01, adversary-03) → register-bookkeeping

The contradiction is real and §21.6 states it in plain words. Not byte-level:

> §21.1: "where a row and the rule it cites diverge, **the rule governs**."
> §6.3 `[R-CNT-07]`: "A reader MUST reject-file when version_major is 0 (invalid) or
> is a major it does not implement" — reserving "invalid" for 0 alone.
> §2.3 `[R-CNF-11]`: *cannot establish* is available "as when the file names a format
> major version it does not implement".

Under both readings every reader rejects the file at open and no verifier
certifies it; only the label on the non-certification moves. The residue that
actually costs something is register-01's third point: `[R-VEC-02]` obliges each
vector's manifest to record "whether the file is **conforming**", and for F21's
vector the answer is relativized to a major this document does not define — §2.3's
own "every conforming file of a format major version it implements" presupposes
conforming files of majors a reader does not implement. That is a corpus-
construction gap, not a byte gap, and `[R-VEC-04]`'s "every vector built from §21's
register is nonconforming" is false for exactly this one row.

### l24-name-overrun-tier (register-02) → register-bookkeeping

Confirmed, and the register contradicts itself here rather than merely
contradicting §19: L4, L6 and L7 — the other layer-*name* rows — all carry
Detected = open, while L24's first instance (leading fixed fields, name first)
carries layer access. §19.1 step 4 and §19.2's tier list both put the name at open.
Not byte-level:

> §19.2 `[R-RDR-02]`: "A reader MAY detect any violation earlier (`[R-CNF-12]`)".

The layer is reject-layer and the file nonconforming under either tier.

### enc06-no-tile-scope-cause-row (register-03) → register-bookkeeping

Confirmed as an asymmetry. §15.1 makes the entry's owning scope the tile, and the
entry is a fixed-width structure (u64/u64/u32), so `[R-ENC-06]` names a tile-scope
condition with no cause row. Not byte-level — F5's own cell states why a cause row
changes nothing:

> F5: "the checks that fire are those values' own value and bounds gates, and this
> row records the cause rather than a procedure of its own".

Every instance is already caught at the tile by T1/T8/T9/T11/T12.

### l2-container-axis-collapsed (register-04) → register-bookkeeping

Confirmed, and I reproduced register-04's arithmetic independently: 61/102/45/44 =
252 over 125 rows, matching §21.8. L1 splits the layer-record and sub-record
containers four ways; L16 four ways; L17 and L18 two ways each; L2 collapses them
to one. Not byte-level:

> §21.8 `[R-ERR-02]`: "Every row of §21.2 through §21.5 — 125 conditions over 252
> instances — has at least one conformance vector (§24) ... and one vector per
> instance."

Both files are reject-layer under `[R-CNT-13]` and `[R-ENC-04]` whichever way the
cell reads; only the corpus loses a vector. Note the collision with register-03:
if both are repaired, §21.8 becomes 126 conditions over 254 instances (L2's split
adds one instance to §21.3, and a new T-row adds one row and at least one
instance).

### err05-hard-limit-inventory-short (diagrams-05, register-05) → editorial

One defect, several instances. `[R-ERR-03]`'s "lives here" overstates
`[R-CNF-10]`, whose actual words are:

> §2.5 `[R-CNF-10]`: "Every limit that affects which files are valid or which files a
> conforming reader accepts lives **in this specification, never only in an
> implementation**."

and `[R-ERR-05]` concedes the point in its own next clause: "They are stated where
the structures forcing them are defined". Not byte-level: §16.1 and §7.4 state the
alignment bounds directly, `[R-CNT-23]` assigns the outcome, and L40/L30 register
them; §5.1 and §6.2 state the file floor and the dir bounds, and F7/F11/F18
register them; §18.2 states the key cap and R10 registers it. register-05's
derivation catch is correct and independently checkable: `[R-MTA-04]`'s fourth
restriction subjects user-metadata keys to "at most 255 bytes", and a JSON key has
no `u8` length prefix, so `[R-ERR-05]`'s parenthetical derivation does not hold for
that instance. And 512 is a number chosen here — §16.1's own note calls it "the
legacy sector floor" — which falsifies "never a number chosen here".

### preserve-verbatim-unbound (register-06) → editorial

Confirmed mechanically: two occurrences, both in §2.4. §20.4 carries the whole
substance in prose ("Retain byte-identical" in all three rows, `[R-WRT-05]`'s "MUST
re-emit byte-identically") without binding the term. Nothing behavioural turns on
it.

### cnf11-unable-to-check-unscoped (verifier-04, adversary-01) → editorial (PARTIAL)

Same defect from two lenses: the governing clause of `[R-CNF-11]` does not scope
"unable to check", and verifier-04's reductio and adversary-01's f3.bin are two
consequences of that one gap.

adversary-01 self-flagged byte-level and built a file to prove it. I downgrade,
on a sentence *both* reporters truncated mid-way in their quotations:

> §2.3 `[R-CNF-11]`: "A verifier MUST report each requirement it was unable to check,
> naming the requirement and the ground, whichever of the three verdicts it reports;
> **that per-requirement report constrains the report and not the verdict**, as
> *unexamined* does below."

"whichever of the three verdicts it reports" contemplates *conforming* alongside a
non-empty unchecked list, and "constrains the report and not the verdict" says
outright that the list does not drive the verdict. adversary-01's V-B chain breaks
at its second link: an unchecked `[R-COD-10]` gives no ground to report *cannot
establish*, and the MUST-NOT-certify clause attaches only to a file the verifier
reports *that way*. The specific MUST-NOT-certify grounds elsewhere — §17.4
`[R-COD-11]` (cannot execute a codec or filter) and §18.2 `[R-MTA-09]` (declines a
document's decode) — are capability grounds and do not reach f3.bin, whose filter
the verifier can execute perfectly well. §21.7 `[R-ERR-01]` confirms the direction:
"A writer that emits well-formed structures carrying wrong sample values — a
mis-strided filter (`[R-COD-10]`), an undisclosed compression dictionary
(`[R-COD-06]`), or simply wrong data — produces a file that every checksum in §8
certifies."

verifier-04's reductio stands independently and is the cheaper argument: the broad
reading empties the conforming-verifier class.

### cnf02-conduct-list-under-inclusive (adversary-02) → editorial

The W1/W2 byte-identical pair is a sound construction and the enumeration is
genuinely under-inclusive. Decided by the principle sentence the enumeration
serves, plus §17.2's own classification:

> §2.3 `[R-CNF-02]`: "File conformance is a pure predicate on bytes: it does not
> depend on any reader, writer, or environment."
> §17.2 `[R-COD-06]`: "it is **a writer violation** whose consequence is wrong decoded
> content, **the same undetectable class as any other writer that emits wrong
> bytes** (§21)."

A writer that emits wrong sample values emits a conforming file; §17.2 places the
undisclosed dictionary in that same class by name, and §17.3 does the same for the
stride ("undetectable by construction (§21.7)"). So the second horn is the
document's, and the repair is to the enumeration, not to the predicate.

### lif08-omits-f9-gap-check (quiz-02) → editorial

> §6.2 `[R-CNT-05]`: "A verifier MUST treat a structure in that gap as a validity
> error at file scope, and counts the rest as slack".

Stated unambiguously, just not in §9.7 — which is the section a verifier's coverage
walk is built from, and the only place the claimant inventory the check needs
exists. Same underlying row as verifier-05's item (1); different edit.

### appg-profile-degrees-of-freedom (writer-05) → editorial (PARTIAL)

> Appendix G: "It adds no requirement to any actor: a writer ignoring it is fully
> conforming".
> §2.1 `[R-CNF-01]`: appendices identified as non-normative are not normative.

Two of writer-05's three sub-claims stand. Gap extent: item 3 fixes a sequence, not
offsets, and §16 `[R-SLB-05]` expressly permits scattering ("A writer that scatters
structures wastes space rather than violating a rule"), so two profile writers can
differ in padding and the closing paragraph names only gap *content* as what the
profile adds. Fill default: `[R-TYP-10]` is a SHOULD the profile never promotes, and
the closing paragraph cites `[R-TYP-06]` (fill is recorded) rather than `[R-TYP-10]`
(what it is) — and this one changes the reference array, not only the bytes.

The sub-record-order claim is weaker than writer-05 states. Item 3's second sentence
reads "Records are ordered by type, and within type 0x0001 by layer name", which
is not confined to top-level records and does order a layer's sub-records by type;
`[R-CNT-14]` caps user-metadata sub-records at one per layer, so the only residual
freedom is two unknown sub-records sharing a type.
