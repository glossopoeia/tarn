# Triage pass — implementer consequence — cleanroom round 34

## Disclosure of what I read

Only `spec/tarn.md`, by targeted `sed`/`grep` ranges. I did **not** open any walk
transcript, did **not** list `/private/tmp/.../r34-round/out/`, and did not touch
`docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history
or the web. No other triage pass's notes were read or looked for. I opened no
directory listing at any point in this session.

Spec ranges read (line numbers of `spec/tarn.md`):
1–50 (§1 opening incl. the test-vector note at line 22), 95–300 (§2.1–§2.4),
594–630 (§4.7 + its Note), 633–780 (§5.1, §5.2), 781–958 (§6.1–§6.4),
998–1050 (§7.2), 1102–1215 (§7.4), 1441–1545 (§9.6, §9.7), 1638–1706 (§11.1, §11.2),
2201–2300 (§15.2, §15.3, §15.4), 2300–2410 (§16), 2634–2700 (§18.2),
3146–3411 (§20.3 whole), 3411–3480 (§20.4), 3476–3560 (§20.5),
3629–3720 (§21.1), 3719–3780 (§21.2 + head of §21.3), 3830–3868 (§21.4),
3901–4030 (§21.6, §21.7, §21.8), 4027–4126 (§21.9), 4161–4210 (§22.3),
4320–4410 (§24), 4557–4760 (Appendices E, F, G, head of H).
Plus `grep` for register rows L17/L18/L40–L49, T3/T4/T7/T11/T14, and counts of
`drop`/`preserv`/`retain`/`compactor` inside Appendix G's line range.

Nothing in the 26 findings was left unevaluated.

---

## Grouping

21 groups over 26 ids. Every id in exactly one group.

| group | ids |
|---|---|
| re-established-verb | reader-01, adversary-01, quiz-01 |
| bar-category-21-7 | reader-02, writer-02 |
| appendix-g-compactor-record-drop | writer-01 |
| both-sides-dimension-extent | writer-04, adversary-02 |
| slab-kept-no-trigger | writer-03 |
| new-state-keeps-two-senses | adversary-03 |
| structural-descriptive-actor-sets | verifier-01, adversary-04 |
| coverage-walk-tile-scope | verifier-02 |
| shape-c-empty-layer-redeclaration | diagrams-01 |
| presentation-note-vs-tables | diagrams-02 |
| metadata-encoding-valid-values-cell | diagrams-03 |
| f5-pad-in-floor-derivation | diagrams-04 |
| f27-l48-citation-scope | register-01 |
| trailer-mimic-payload-vs-slack | register-02 |
| limits-every-file-every-layer | register-03 |
| row-is-the-rule | register-04 |
| vector-per-instance-quantifier | register-05 |
| l44-omitted-from-parenthetical | adversary-05 |
| http-vocabulary-unpinned | adversary-06 |
| t7-t11-double-classification | quiz-02 |
| section-21-1-rules-unidentified | quiz-03 |

Merges I made and why:

- **reader-01 + adversary-01 + quiz-01.** One sentence, one word: the closed
  exception list's third verb "re-established" against the delegated clause's
  "kept". The three reporters pick different readings ((a) some→same,
  (2) kept-over-moved-geometry) but the defect is identical.
- **reader-02 + writer-02.** Both attack the same clause of §20.3 step 4 — its
  citation of §21.7's "no condition a file can exhibit" class — and both offer
  the same alternative (unwitnessed) on the same evidence (the superseded
  generation survives in slack, §9.6's probe reaches it).
- **writer-04 + adversary-02.** Same sentence, same headline defect: "where a
  field is on both sides — a dimension extent, …" when a dimension extent is on
  the permitted list only. adversary-02 adds a second complaint about the same
  sentence (the "reach every declaration field of §7.4" claim), which I fold in
  rather than splitting, since an id may land in only one group.

Splits I did **not** make:

- **writer-03 vs adversary-03** stay separate. Both concern the closing sentence
  of §20.3 step 4, but they are different defects with opposite directions and
  different repairs: writer-03 says the verb "kept" is stated without
  [R-SLB-04]'s trigger list (too broad); adversary-03 says the quantifier "every
  run the new state keeps" inherits the narrower of two senses of "keeps"
  used four lines apart (too narrow).
- **verifier-01 vs adversary-04** merged (same actor-set mismatch in §4.7,
  same witness class), even though verifier-01 grades it AMBIGUITY and
  adversary-04 OBSERVATION.

---

## Byte-level re-judgement, with the sentence that decides each downgrade

The test: does resolving this change which byte sequences a conforming
implementation may emit, or must accept or reject?

**Result: 0 of 21 groups byte-level.** Every reporter self-flagged no; I did not
inherit that. Each downgrade below carries the quotation that decides it. I state
the premise each rests on so it can be attacked.

### 1. re-established-verb (reader-01, adversary-01, quiz-01) — CONFIRMED, not byte-level

The verb is real and unmatched. §20.3 step 4:

> "and a slab or alignment declaration MAY be declared, changed, re-established
> or cleared as this step provides below."

against the clause below:

> "a slab declaration declared, changed or **kept** has its invariants
> re-established over every run the new state keeps, or is cleared (`[R-SLB-04]`)"

The restatements at §11.1 Rationale ("may be declared, changed, re-established or
cleared") and Appendix H carry the same verb.

Decider for the downgrade — the step's own default clause:

> "A layer that stores a tile **in the generation this commit supersedes**
> **keeps its declarations**, with these exceptions and no other"

Enumerate every transition an A or S declaration can make in one commit:
none→some ("declared"), some→other ("changed"), some→none ("cleared"),
some→same (the default "keeps its declarations"), and the exclusive A/S switch
("cleared" + "declared", the several-at-once clause permitting them together).
Every transition is licensed under every reading of "re-established". The
new-state declaration values a commit may leave behind are therefore the same
set under all three readings, so no file is emittable under one and barred under
another, and the bytes carry no record of how the commit arrived at its values.

Premise my downgrade rests on: that "keeps its declarations" is a *permission*
(the default disposition) and not merely a description, so some→same needs no
exception. If a maintainer reads the opening clause as merely descriptive, then
the closed list would have to name some→same and "re-established" is load-bearing
— but even then the reachable value set is identical, so the bytes still do not
move.

Implementer consequence: none in bytes. A writer author reading (b)
(clear-and-redeclare as a distinct operation) hunts below for a clause governing
it and finds one about runs. Cost is a wasted search, not a wrong byte.

### 2. bar-category-21-7 (reader-02, writer-02) — PARTIAL, not byte-level

The clause under attack:

> "the bar stating no condition a file can exhibit (§21.7, `[R-ERR-01]`,
> `[R-CNF-02]`)"

Both reporters argue it is instead §21.7's *unwitnessed* class, because a
physical TARN file carries the superseded generation in its slack and §9.6's
probe reaches it.

I checked the premise both reporters share and it does not hold. §5.2:

> "Every byte the live state does not claim is **slack**: … Slack has no internal
> structure this specification defines, **its content is unconstrained**, and no
> conformance requirement applies to it."

and §9.6:

> "slack is unconstrained (`[R-CNT-21]`)"

and §20.4's Rationale:

> "Adjacency is a fact about a file's history, which §9.7 does not reconstruct"

Because slack content is unconstrained, a single-commit creator may lawfully emit
a file whose slack contains a well-formed superseded trailer and directory
declaring a different layout under the same file_id. That file is byte-identical
to writer-02's witness and was produced by no violating commit. §2.3 fixes that
file conformance "is a pure predicate on bytes", so a predicate two byte-identical
files answer differently is not a condition a file exhibits. That is precisely
§21.7's second class, and §20.3's citation is defensible on a stronger ground than
either reporter allows.

What survives: the sentence cites §21.7 without saying which of that section's two
classes it means to invoke or why, and §21.7's own worked case for the class
([R-ENC-06]'s field widths) is justified by an argument that does not transfer.
§18.2 adds a second member of the class with its own reasoning ("the bar on sizing
a buffer binds a reader rather than the document, and so states no condition a file
can exhibit at all"); §20.3 supplies none.

Not byte-level under either classification, and both reporters agree. §21.7:
unwitnessed conditions require no row ("that clause requires no row for it"), and
no-condition requirements have "no condition to omit". §2.3's [R-CNF-02] names
this exact bar:

> "§20.3 step 4's bar on the fixed declarations of a layer that stores a tile are
> the cases this text states, and each is declared where it arises"

with "a file is never nonconforming by virtue of one". Verdict and register row
are the same under both readings.

### 3. appendix-g-compactor-record-drop (writer-01) — CONFIRMED, not byte-level

Verified. §20.4's MU = 0 / PE = 0 row:

> "a compactor MAY drop it whenever it rewrites the file"

§20.5:

> "the live committed state (§7.2), **less any record §20.4 lets it drop**"

Appendix G item 8:

> "A compactor's output is therefore reproducible only modulo its trailer"

I re-ran the reporter's search over Appendix G's line range (4587–4751):
`drop` 0 hits, `preserv` 0 hits, `retain` 0 hits, `compactor` 7 hits. The zeros
are real. Neither the ten items nor the closing paragraph's enumeration mentions
record retention or the PE bit. So two profile-adopting compactors given one
conforming input carrying a MU = 0 / PE = 0 record may emit directories differing
by one record — and with it dir_length, every downstream offset, the directory
CRC, committed_file_length and F. That is not "modulo its trailer".

Downgrade decider — Appendix G's own opening:

> "It adds no requirement to any actor: a writer ignoring it is fully conforming"

together with [R-CNF-01]'s exemption for "appendices identified as
non-normative". Both compactors are conforming and both outputs are conforming
files. Resolving item 8 removes no byte sequence from the emittable set and
changes no accept/reject verdict.

Premise: that the profile is genuinely optional, so a claim inside it cannot bind.
If a maintainer intended item 8's sentence to *state* a profile obligation
(retain everything), then the profile's own item set would have to say so — and it
does not, which is exactly the defect.

Implementer consequence — the sharpest in this round's set, and concretely
describable both ways. Team A builds content-addressed storage on the profile,
having read that only the trailer can move; it stores digests of compacted files.
Team B ships a compactor that drops PE = 0 records (or is forced to, since §20.5
requires dropping as "the one disposal that answers" for a detected violation, and
how much a compactor detects beyond [R-WRT-09]'s floor is per-implementation).
Swapping compactors changes every digest. Both teams are conforming; the profile's
promise is what failed.

### 4. both-sides-dimension-extent (writer-04, adversary-02) — CONFIRMED, not byte-level

Verified field by field against §7.4's table. The fixed list in §20.3 step 4 is:

> "the layout, the linearization and the index encoding, the codec and the filter,
> the rank and the dimension order, every tile extent, every channel's type and
> fill, an interleaved layer's channel list (its names aside), and the position of
> every planar channel the new state keeps"

A dimension **extent** is not there, and cannot be: the fixed list is introduced
as "Every **other** declaration is fixed", i.e. the complement of the permitted
list, which already names "an extent MAY grow, and MUST NOT shrink". The other
two named examples do sit on both lists. So the illustration is wrong about one
of its three members on the natural reading of "the two lists … both sides".

adversary-02's second half also holds: entry_count, crc_of_crc_array, the extent
slot and the sub-record sequence are §7.4 rows neither list reaches; the sentence
disposes of them in its *next* clause, so "Between them the two lists reach every
declaration field of §7.4" is true only if "declaration field" silently excludes
those four.

Downgrade decider — the permitted list itself:

> "an extent MAY grow, and MUST NOT shrink"

That states the whole of what a commit may do to a dimension extent under either
reading of "both sides", and the fixed list's membership is unchanged either way.
No commit becomes permitted or barred.

Premise: that the sentence is an illustration of two lists already stated in full,
not a rule of its own. Attack it by arguing the sentence's completeness claim is
itself normative — but even then it claims only reach, and the reach of the
operative lists is what decides commits.

### 5. slab-kept-no-trigger (writer-03) — PARTIAL, not byte-level

The asymmetry is real inside one sentence. Slab half grounded in a trigger-list
rule and stated triggerlessly; alignment half grounded in an unconditional
invariant and stated unconditionally:

> "a slab declaration declared, changed or kept has its invariants re-established
> over every run the new state keeps, or is cleared (`[R-SLB-04]`), and an aligned
> layer's stored tiles … satisfy its invariant or the declaration is cleared
> (`[R-SLB-01]`, `[R-CNF-05]`)"

against [R-SLB-04]'s five triggers.

But the claimed bite does not arise, and for a reason the reporter states only
half of. On a nonconforming input already carrying L41 or L42, the *narrow*
reading does not license a rename-only commit that leaves the defect: [R-CNF-05]
does the work directly.

> "**Conforming writer.** A writer MUST emit only conforming files. `[R-CNF-05]`"

and [R-SLB-03] is unconditional over the live state:

> "When declared, for every run: the run's stored tiles are contiguous and packed
> in ordinal order … and the first stored tile's offset satisfies
> offset mod A_slab = 0."

So no conforming updater may emit *any* commit leaving that layer slab-declared
and unpacked, rename-only included. The broad reading is redundant, not wrong;
the narrow reading is not permissive, because [R-CNF-05] closes it. Hence PARTIAL:
the grounding asymmetry is a genuine wording defect, the "unrequested
verifier-grade sweep" dilemma is not — an updater that will emit a conforming file
already owes the whole-file conformance of its output.

Premise: that L41/L42 make the file nonconforming (they are §21.3 register rows,
so yes) and that [R-CNF-05] reaches an updater (§2.3: "An updater MUST satisfy
every writer requirement for the bytes it produces" — and here the layer record
carrying the stale declaration *is* a byte it produces, since re-emission is
production for conformance purposes). If a maintainer holds that a
byte-identically re-emitted record is not "bytes it produces", the downgrade
weakens — but §20.3 step 2 says the opposite twice ("a violation latent in a
structure it carries forward unmodified travels with that structure").

### 6. new-state-keeps-two-senses (adversary-03) — CONFIRMED, not byte-level

Two senses, four lines apart, verified:

> "the position of every planar channel **the new state keeps**"  (retained-from-before;
> contrasted with the channels a shortening removes)

> "an aligned layer's stored tiles — **every one the new state keeps**, not only
> those this commit adds"  (present in the new state, added included)

The third use, "every run the new state keeps", is unqualified.

Downgrade decider — [R-SLB-03] again, unconditional:

> "When declared, for every run: the run's stored tiles are contiguous and packed
> in ordinal order"

plus [R-CNF-05]. Under the narrow reading a growth's new runs owe nothing under
§20.3, but the file the writer would emit exhibits L41 or L42 and [R-CNF-05] bars
emitting it. [R-SLB-04]'s own triggers ("the stored-tile set, the run partition")
fire on a growth in any case. So the emittable set does not move: this is exactly
the discriminator "a permissive reading that lets a writer produce a file carrying
a register-row violation moves nothing".

Implementer consequence: a writer author reading §20.3 alone under the narrow
sense skips the check on new runs, then fails verification. Wasted iteration, not
a divergent file that ships.

### 7. structural-descriptive-actor-sets (verifier-01, adversary-04) — CONFIRMED, not byte-level

Verified. §4.7:

> "A field is **structural** if its value determines anything a conforming reader
> **or verifier** does … It is **descriptive** if it determines none of those: its
> value determines nothing a conforming **reader** does"

The witness class is populated: §7.2's record-header table classes the flags field
(bits 2–15 reserved) as structural, while [R-CNT-12] says "readers MUST ignore
them" and assigns detection to a verifier (F26, L47). Same for a registered type's
stored MU/PE bits (§7.3 / F28, L49).

Downgrade decider — the very next sentence of §4.7:

> "In format major 1 `version_minor` is the only descriptive field, and every
> other field this specification defines is structural."

That assigns every actual field by name, so nobody has to run the test to classify
anything; and every layout table prints an explicit Class cell besides. The one
normative consequence of "descriptive" — "a reader MUST NOT alter decoding based
on it" — is independently required of the only disputed fields by [R-CNT-12]'s
"readers MUST ignore them". Two readings, identical reader behaviour, identical
writer output, identical verifier verdict.

Premise: that the closing sentence is exhaustive for format major 1. It says so.
The exposure is to a *future* minor that adds a verifier-only field and has to run
the test — which is a maintenance hazard, not a present one.

### 8. coverage-walk-tile-scope (verifier-02) — PARTIAL, not byte-level

The passage:

> "The walk is incomplete where a scope-level rejection ends that scope's
> enumeration … a tile's or a document's decode declined leaves the walk complete,
> that claimant being enumerated from its index entry or extent slot."

and, stipulatively, at layer scope:

> "A rejected layer's claimants are not enumerated, **whether or not the rejection
> impeded reading them**"

The reporter is right that only two tile cases are glossed and that T1–T5 and
T13–T26 are not among them. But the text does decide it, more firmly than the
reporter allows, in two places. §5.2's leading criterion is factual and
enumeration-shaped:

> "Where the walk of §9.7 does **not enumerate** every region's claimants, the
> verifier MUST report the total as partial."

and §9.7 fixes what the walk enumerates, with exactly one carve-out:

> "the stored extent of each non-sentinel tile-index entry (an entry `[R-IDX-03]`
> classifies reject-tile on a *structural* ground contributes no stored extent to
> the walk; **one whose stored bytes alone fail its crc keeps its extent**)"

A T4 or T3 or T24 tile's entry is well-formed, so its extent is enumerated, so the
walk enumerated every claimant, so the total is exact. Reading (a) — the
reporter's own pick — is the one the document states. What survives is the reading
hazard: the layer clause's express counter-factual invites *expressio unius* over
the two tile carve-outs.

Not byte-level on any reading. The disputed quantity is a line in a verifier's
report. §2.3 fixes the verdict either way ("An established violation takes
priority: a verifier that has established any violation reports *nonconforming*"),
readers owe no coverage walk at all (§5.2: "Coverage is checked by verifiers, never
by readers"), and the file is nonconforming under both readings so [R-CNF-05] bars
every conforming writer from emitting it regardless.

Implementer consequence, stated concretely because it is real even though inert
for bytes: two verifiers handed a four-tile layer whose edge tile carries non-fill
padding report 52 bytes exact vs 180 bytes partial. §22.3 makes that number
operator-facing ("the distinguishing figure comes from a walk that completes").
That is a divergence in tooling output, not in the artifact.

### 9. shape-c-empty-layer-redeclaration (diagrams-01) — CONFIRMED, not byte-level

The re-declaration sentence sits inside shape (c) between two sentences expressly
marked "not this shape", carrying no such marking itself. Reading B (a free
re-declaration is directory-only) is wrong.

Downgrade decider — §20.3 step 4, unconditional and above the figure:

> "Every layer whose stored-tile set **or index content** this commit changes has
> its tile-index region re-emitted in full — entry_count entries plus the segment
> CRC array — necessarily at a new placement (`[R-LIF-01]`)"

with [R-CNT-17]:

> "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when
> entry_count is 0) … a mismatch … is a validity error at layer scope"

I walked the case split. Where the re-declaration changes the grid count (the
reporter's (100,) T=32→16, entry_count 4→7), reading B's directory-only output
carries extent_length ≠ the formula: a layer-scope validity error, so a
nonconforming file, so [R-CNF-05] bars a conforming writer from emitting it.
Where it does not change entry_count or index content (a renamed dimension, a
changed fill on an empty layer), both readings agree the commit is directory-only
and both outputs are identical. So there is no case where reading B yields a
conforming file reading A forbids: the emittable set does not move.

The figure is a labelled *Example*, non-normative under [R-CNF-01]. §11.1's
Rationale draws the same distinction correctly for growth ("A growth that changes
no grid count … taken alone touches the directory alone"), which is the model for
the repair.

### 10. presentation-note-vs-tables (diagrams-02) — CONFIRMED, not byte-level

Both halves check out. §6.1's table columns are `| Offset | Size | Value | Class |`
— no name/Field column — while the Note's carve-out for it says only that "a Value
column replaces type and range". §7.2's table is
`| Offset | Size | Type | Field | Class |` with no range column; of its five
fields, `type (0 invalid)` and the flags cell fold a range into the Field cell and
`inline_length`, `extent_offset`, `extent_length` do not, their constraints living
in [R-CNT-12] and [R-CNT-13] below.

Downgrade decider — [R-CNF-01]:

> "All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative."

The passage is a *Note*. Which columns a table prints changes no byte and no
verdict, and every omitted name and range is stated normatively elsewhere
(§6.1's own "Writers MUST emit exactly these 16 bytes"; [R-CNT-12]/[R-CNT-13]).

### 11. metadata-encoding-valid-values-cell (diagrams-03) — PARTIAL, not byte-level

This was my closest byte-level candidate, because a validator built from the cell
alone would reject at the record's containing scope a file this specification
calls conforming — an accept/reject divergence, which is the second half of the
test. I checked whether the document leaves that open. It does not, four times
over, and the cell itself defers:

> "| 0 | 1 | u8 | encoding | structural | 1 or 2; **see below** |"

§18.2's next paragraph:

> "Field values: 0 is invalid; 1 = none and 2 = zstd are assigned; 3 through 0x7F
> are reserved; values ≥ 0x80 are the experimental range (§10). … An encoding a
> reader does not implement is therefore one this specification does not assign,
> and **is ignore-record (`[R-CNT-25]`)**."

§21.6's row:

> "A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); **the file is conforming** — §10.3's
> prohibition binds a writer's conduct, not the bytes"

So the cell states the values a conforming *writer* emits and points at the
paragraph for everything else; a reader that stops at "1 or 2" has ignored an
in-cell pointer, which is a misreading rather than an ambiguity in the text.

PARTIAL rather than CONFIRMED on the reporter's framing: the contrast with §7.4's
index_encoding cell ("any other value — including 0, reserved 2–0x7F, and the
experimental range ≥ 0x80 (§10) — is a validity error at layer scope") is not two
conventions applied to like spaces. The two value spaces genuinely differ — an
experimental *index_encoding* is a layer-scope validity error, an experimental
*document encoding* is ignore-record on a conforming file — so the cells differ
because the rules do. What remains is that the §18.2 cell carries the terse form
in a column that elsewhere carries hard conformance bounds (§6.2's "≥ 16", "≠ 0",
"zero").

Premise of the downgrade: that "; see below" is a deferral a reader is obliged to
follow. Attack it by holding that a layout table's Valid-values column must be
self-sufficient — but §4.7's Note never promises that, and §6.2's version_major
cell ("1 (0 invalid; others: §6.3)") uses the same deferring shape.

### 12. f5-pad-in-floor-derivation (diagrams-04) — CONFIRMED, not byte-level

F5's Condition cell names four components; [R-CNT-27] derives the floor from
three:

> "No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer."

and [R-CNT-05] says the pad can be absent outright:

> "a writer that ends its directory on a 64-byte boundary leaves none"

§2.3's Note derives the same floor from the same three ("the 128-byte floor it
asserts is derived from a directory of at least 4 bytes at an offset of at least
16 and a 64-aligned F"). The reporter's F = 128 / dir [16, 64) / trailer [64, 128)
witness satisfies [R-CNT-06]'s `dir_offset + dir_length ≤ F − 64` at equality with
zero pad, so the pad is genuinely not a component of the minimum.

Downgrade decider — §21.1:

> "each row *restates* its governing rule, and where a row and the rule it cites
> diverge, **the rule governs**"

The divergence is confined to F5's reason clause; condition (F < 128), outcome,
detector, tier and instances all match [R-CNT-27]. No file changes sides.

### 13. f27-l48-citation-scope (register-01) — CONFIRMED, not byte-level

Verified against the tables: F27's and L48's Governing rule cells read
`[R-MTA-05]` (R-CNF-05); F28's and L49's read `[R-CNT-22]` (R-CNF-05). The
parenthetical opens on "several such rows", names two rules, and closes "— F27
and L48", which are one rule's rows.

Downgrade: reading A (the citation attaches to the [R-MTA-05] clause) is settled
by the document's own practice at §7.1 in the identical shape, and by §21.1's
tie-break in any case:

> "where a row and the rule it cites diverge, **the rule governs**"

Every row's condition, outcome, scope and detector stay where the tables put them.
The cost the reporter names — a mislabelled corpus entry under [R-VEC-02] — is
recoverable by [R-VEC-01] ("where a vector's recorded expectation and this
specification disagree, this specification governs and the vector is corrected").

### 14. trailer-mimic-payload-vs-slack (register-02) — CONFIRMED, not byte-level

The §21.6 entry states a condition about a payload and gives a reason about slack:

> "| A payload contains a byte string that mimics a trailer | Inert: **nothing
> enumerates slack**, and a recovery tool re-verifies its output whole (§9.6) … |
> `[R-LIF-06]` |"

The governing rule is stated over a live payload:

> "a **tile payload** can deliberately contain a byte string that mimics a valid
> trailer, so recovery output MUST be re-verified as a whole file (§8) before
> being trusted"

and §22.3 keeps the two apart deliberately: "under live-state coverage a mimic **in
slack** is inert — nothing enumerates it — but a recovery tool that truncates to
one produces a different file." A live stored-tile extent is enumerated — §9.7
reaches "the stored extent of each non-sentinel tile-index entry" — so the entry's
stated reason does not cover its stated condition.

Downgrade decider — §21.1's closing sentence on this very table:

> "§21.6's entries restate their governing rules on the same terms a row does, and
> where such an entry and the rule it cites diverge, **the rule governs there too**."

[R-LIF-06]'s obligations on a recovery tool are unchanged: re-verify the output
whole, report the candidate settled on and how many were rejected. No file becomes
emittable or rejectable.

Implementer consequence: a recovery-tool author who builds from the §21.6 entry
alone might model mimics as a slack-only phenomenon — but [R-LIF-06]'s own text,
which the entry cites, says "a tile payload" in the first line of its cautions, so
the branch does get written.

### 15. limits-every-file-every-layer (register-03) — PARTIAL, not byte-level

The clause:

> "The first five rows range over declarations, which every file and every layer
> carries."

Three of the five (rank d, channels per layer C, addressed tiles per layer) are
per-layer, and §21.6 blesses a zero-layer file ("The file contains zero layers | A
conforming file"). But the distributive reading — file-level declarations by every
file, layer-level ones by every layer — is the plain one and is simply true, and
the reporter concedes it. PARTIAL because the "falsified" headline overstates a
loose universal.

Downgrade decider — the sentence immediately before it:

> "Either way a file containing no instance of a kind does not exceed that row,
> whatever its declarations would derive."

That settles the zero-layer file for all eight rows. §21.9 states minimum
guarantees, not caps, so a file with no instance cannot exceed one, and
[R-CNF-03]'s acceptance duty runs to a zero-layer file under either reading:
"Software that declines **on that ground** a file whose every quantity lies within
the table is not a conforming reader". No reader may decline it either way.

### 16. row-is-the-rule (register-04) — CONFIRMED, not byte-level

> "The **Instances** column enumerates what a conformance corpus builds for that
> row (§21.8): the row is the rule, and each instance is one file."

against, twenty lines earlier in the same subsection:

> "each row *restates* its governing rule, and where a row and the rule it cites
> diverge, **the rule governs**"

Reading (1) (corpus-building shorthand: the row is the unit a corpus is counted
against) is the one the sentence's subject supports. Downgrade decider is the
tie-break just quoted, plus [R-VEC-01]:

> "where a vector's recorded expectation and this specification disagree, this
> specification governs and the vector is corrected"

A corpus author who takes reading (2) builds a vector recording an unsupported
expectation; [R-VEC-01] makes the vector wrong, not the document. No file's
verdict moves.

### 17. vector-per-instance-quantifier (register-05) — CONFIRMED, not byte-level

§21.8:

> "has at least one conformance vector (§24) whose expected outcome is that row's
> outcome, and one vector per instance."

§24, declaring itself the inheritor of the same obligation:

> "Coverage is the corpus's own obligation, inherited from `[R-ERR-02]`: every
> register row has **at least one** vector for each instance it names"

The parallel restatement carries a quantifier the source drops. Reading (1) (the
"at least" distributing across the "and") is right, and the surrounding text
settles it: "A row without a vector is a gap in the corpus, not a licence to skip
the check" (§21.8) and "A missing vector is a gap in the corpus and never a licence
to skip the check it would have exercised" (§24) are both floors; nothing anywhere
caps a corpus.

Downgrade: both [R-ERR-02] and [R-VEC-03] bind the conformance corpus, not any
file. [R-VEC-01] makes the corpus derivative. No byte sequence enters or leaves
the emittable set.

### 18. l44-omitted-from-parenthetical (adversary-05) — REFUTED, not byte-level

The sentence:

> "but for a decoded size, a padding position or pad bit, or a boolean byte the
> register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
> outright under a changed codec or filter (T24, T25), no check any actor owes
> able to see it (§21.7)"

The reporter proposes L44 as an omitted member. It does not belong. The
sentence's subject is a check able to *see the reinterpretation* — that "the same
bytes would denote values, coordinates or padding the writer did not store". Every
enumerated row fires only because a stored tile was written under the old
declarations: T3 and T14 compare a stored length against the derived decoded size,
T4/T5/T2 read stored padding and boolean bytes, T24/T25 fail a decode of stored
bytes. L44 reads declarations alone — "Codec 4 (lz4) declared on a layer any of
whose **addressed** tiles' decoded size exceeds 0x7E000000" — and fires identically
on a file a creator wrote in one commit with those declarations and no tile stored
at all. It separates no violating commit's output from a lawful creation, so it
witnesses nothing about the change.

And the same step already sites L44 correctly, on the right ground, two paragraphs
later:

> "A permitted change holds provided the declarations and geometry it produces stay
> within every bound they are subject to: `[R-COD-07]`'s lz4 decoded-size cap (L44,
> the largest channel plane governing in a planar layer)"

with the bar's own clause anticipating the reporter's file:

> "a file such a commit leaves can be nonconforming on its own terms, as the
> paragraph below sets out."

The document decides it. Nothing to repair; at most a maintainer could write "a
stored tile's decoded size" to foreclose the literal reading.

### 19. http-vocabulary-unpinned (adversary-06) — CONFIRMED, not byte-level

Verified: Appendix F is titled "Normative references", is not marked
non-normative (so normative under [R-CNF-01]), and lists BCP 14, RFC 3720,
IEEE 754, RFC 1950/1951/1952/8878, LZ4 Block, RFC 8259, RFC 3339 and Unicode. No
HTTP specification. [R-CNT-10] imposes a MUST in HTTP terms of art:

> "A remote reader MUST handle a 200 response to a range request … and SHOULD fall
> back to a size probe plus an absolute range on transports without suffix-range
> support"

The contrast with the rest of the appendix is sharp — the lz4 block format is
pinned to a release tag, IEEE 754 to a named rounding attribute.

Downgrade: the term that actually bears on a verdict is defined in-document,
in the same rule:

> "The size a remote reader compares against committed_file_length MUST be
> transport-authoritative (a full-response content length, the complete length of
> a range response, or a size probe)"

so the F17 cross-check does not turn on an unpinned term. What is left unpinned —
"200", "range request", "suffix-range support" — governs a reader's transport
conduct, and "the file's bytes are identical whether the reader handles a 200
correctly or not". No verifier verdict turns on it, and §6.4's Note says the
request accounting is "a theory of operation, not a budget".

Implementer consequence: a reader author must supply HTTP semantics from outside
a document that promises to be "implementable from this document alone" (§1).
Real, and a maintainer decision (which RFC to cite) rather than an edit.

### 20. t7-t11-double-classification (quiz-02) — PARTIAL, not byte-level

Verified on §15.3's table. An entry with offset = 0xFFFF_FFFF_FFFF_FFFF and
length = 5 is not a sentinel (§15.2 requires both fields plus crc 0), so:

> "| offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
> reject-tile |"

and

> "| offset > 2⁶³ − 1 or length > 2⁶³ − 1 (non-sentinel) | *structural*:
> reject-tile (`[R-ENC-03]`) |"

both reach it. So §15.3's table alone double-classifies, and the register offers
T7 and T11 for the same 20 bytes. That much is right.

PARTIAL because the claim that only T11's cell decides the label is wrong: §21.1's
specialization test decides it independently, and this is exactly the relation
those two rows stand in.

> "where every file exhibiting one row's condition … necessarily exhibits
> another's, the file is recorded against the narrower row … the property decides
> any pair and **this list is not offered as closed**."

Every entry with exactly one field at S necessarily has that field above 2⁶³ − 1,
so T7 is a strict specialization of T11 and the file is recorded against T7 —
the same answer T11's own "the value being distinct from the all-ones sentinel"
clause gives. The reporter noticed the enumerated pair list omits T7/T11 but
overlooked that the list is expressly open and the property self-applying.

Not byte-level: both rows carry outcome reject-tile, detector reader, detection
point tile use, and the same structural classification, so the entry is refused
identically and contributes no claimant to the walk either way. Only a manifest
label moves, and [R-VEC-02] provides for a file that cannot isolate one row.

### 21. section-21-1-rules-unidentified (quiz-03) — CONFIRMED, not byte-level

Verified. §21.1 carries no *Note*, *Example* or *Rationale* label and is not an
appendix, so it is normative under [R-CNF-01]. It states at least three rules
(completeness is normative; the rule governs a diverging row; the specialization
test) and none carries an identifier. §2.2's own claim:

> "Normative requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`."

Every bracketed identifier inside §21.1 cites a rule stated elsewhere. Neighbouring
subsections each declare one ([R-ERR-01], [R-ERR-02], [R-ERR-03]–[R-ERR-05]).
The front matter (line 22) says test vectors cite "stable identifiers like
`[R-IDX-03]`".

Downgrade: an identifier is a citation handle. [R-CNF-01] makes the text normative
without one, and [R-VEC-02] obliges a manifest to record "that **row's** governing
requirement identifier" — every row has one, so no manifest entry is blocked. No
writer output and no verdict changes if the identifiers are added or withheld.

The unindexed rules are real and the fix is a maintainer's call (allocate
[R-ERR-06] and up, or state expressly that §21.1's rules are read under
[R-ERR-02]).

---

## Summary

- 26 ids, 21 groups, every id in exactly one group, no duplicates.
- Byte-level upheld: 0. No reporter flagged one; I re-tested each independently
  against the emit / must-accept / must-reject test and quoted a decider for each
  downgrade rather than asserting one.
- The two I looked hardest at for a byte-level fork:
  **metadata-encoding-valid-values-cell** (an accept/reject fork on its face, closed
  by the cell's own "; see below" plus §18.2's ignore-record sentence and §21.6's
  row) and **appendix-g-compactor-record-drop** (a real, describable byte divergence
  between two conforming compactors, closed only by Appendix G being non-normative
  and adding no requirement). If any group in this set is going to be reopened by a
  refuter, it should be one of those two, and the second is the one with the
  concrete implementer cost.
- Strongest by my lens (implementer consequence, regardless of byte level):
  appendix-g-compactor-record-drop, then coverage-walk-tile-scope, then
  http-vocabulary-unpinned.
- Most inert: l44-omitted-from-parenthetical (refuted),
  limits-every-file-every-layer, row-is-the-rule.
- I could not check the ADR ledger (docs/ is out of scope), so every downgrade
  above is grounded in the specification text and never in "the ledger already
  asks it".
