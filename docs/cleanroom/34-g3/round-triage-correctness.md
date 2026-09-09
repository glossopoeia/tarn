# Triage pass — CORRECTNESS lens — cleanroom round 34

## Disclosure of what I read

Only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, by
`sed -n`/`grep`/`awk` over line ranges. I opened **no** walk transcript, **no**
other triage pass's notes, **no** directory listing of `r34-round/out` or any
other directory. I ran `mkdir -p` on my own output directory only. I ran three
counting greps confined to Appendix G's line range (4587–4751) to check a
reporter's arithmetic.

Sections read in full or in the relevant range: §2.1, §2.2, §2.3, §4.7, §5.1,
§5.2, §6.1, §6.2 (R-CNT-05/06 area), §6.4, §7.1 (tail), §7.2, §7.3, §7.4,
§9.6, §9.7, §11.1, §11.2, §15.1–§15.4, §16–§16.2, §18.1–§18.2 (opening),
§20.3, §20.4, §20.5 (opening), §21.1–§21.9, §22.3, §24, Appendix F,
Appendix G, Appendix H (updater checklist excerpt).

My lens is **correctness**: for each finding, is the quotation accurate, is it
in context, does the cited section say what the reporter says, and is the
claimed second reading actually permitted by the words?

---

## Byte-level test applied to every group

> Does resolving this change which byte sequences a conforming implementation
> may emit, or must accept or reject?

**Nothing here survives it.** Group by group, the sentence that decides it is
quoted below. No reporter self-flagged byte-level this round, and I did not
find one they missed. The two places I probed hardest for a byte fork —
G5 (the slab half's missing trigger) and G8 (the coverage walk's completeness
test) — are recorded below with the reasoning that closed them, including the
premise each closure rests on.

---

## G1 — `re-established` vs `kept` (reader-01, adversary-01, quiz-01)

Same defect, three reporters. §20.3 step 4 line 3217:

> and a slab or alignment declaration MAY be **declared, changed,
> re-established or cleared** as this step provides below.

delegating to line 3321:

> a slab declaration **declared, changed or kept** has its invariants
> re-established over every run the new state keeps, or is cleared
> (`[R-SLB-04]`)

Verified: `grep -n "re-establish"` gives exactly five sites — 1664 (§11.1
Rationale), 2368 ([R-SLB-04]), 3217 (the member), 3321 (the delegation),
4799 (Appendix H). At 2368 and 3321 the object is *the invariants*; at 3217,
1664 and 4799 the object is *the declaration*. adversary-01's count is right.

The exception list is closed in terms — "keeps its declarations, with these
exceptions and no other". So a member that is not an exception is a
bookkeeping defect, and a delegation whose vocabulary does not match the
clause it delegates to is one too. Both are real.

**Byte-level: no.** I enumerated the transitions myself rather than taking any
reporter's enumeration: none→some ("declared"), some→other ("changed"),
some→none ("cleared"), some→same (the default, "A layer ... **keeps its
declarations**"), and the exclusive A↔S switch ("A commit MAY make several of
these changes at once", clear + declare). Every transition is licensed under
every reading of the fourth verb, and the bytes carry only the new state's
declaration values — no field records how a commit arrived at them (§20.4
Rationale: "nothing in either says how many commits separate them"). The
sentence that decides it is §20.3's own default clause, "A layer that stores a
tile in the generation this commit supersedes **keeps its declarations**",
which covers some→same without help from the exception list.

*The premise my downgrade rests on, stated for attack:* that the new-state
declaration values are the whole of what the exception list constrains — i.e.
that no reading of "re-established" imposes an obligation on the *placement* of
stored tiles that "kept" does not. I checked this: any re-laying the word could
be read to require is separately and unconditionally required by [R-SLB-03]
("When declared, for every run: …") and [R-SLB-04], both of which bind
regardless of which verb the list uses.

Consensus CONFIRMED (the mismatch is real and verified at five sites).
Severity: register-bookkeeping/editorial. Repair is a maintainer's wording
call, not a mechanical edit — reader-01 is right to leave it stated.

## G2 — §20.3's bar and §21.7's "no condition a file can exhibit" (reader-02, writer-02)

Same defect. §20.3 step 4:

> This bar binds the commit as an actor: no file is nonconforming by virtue of
> its violation, and no register row records the violation itself, ... and the
> bar stating **no condition a file can exhibit** (§21.7, `[R-ERR-01]`,
> `[R-CNF-02]`)

writer-02 says the right class is *unwitnessed*, because the superseded
generation physically survives in slack and §9.6's probe could find it.
reader-02 says the same thing more weakly.

**I refute this, and the document decides it.** The decisive sentences are
[R-CNT-21] and [R-CNT-03]:

> Every byte the live state does not claim is **slack**: ... Slack has no
> internal structure this specification defines, **its content is
> unconstrained**, and no conformance requirement applies to it.

and [R-LIF-06] / §21.6, which record that a payload — hence any slack — may
carry a byte string that *mimics a valid trailer*. Put those together and
writer-02's witness collapses: the byte sequence he builds (generation 1's
directory and trailer sitting in the slack of a file whose live layer declares
layout 2) is a byte sequence a **single conforming commit** could also have
produced, by writing exactly those bytes into its gaps. Slack content is
unconstrained, so nothing in the bytes distinguishes "this file's history" from
"decoy bytes a creator wrote". §9.6 says so in terms: "the earlier state the
probe finds is a different artifact", and "For a verifier the probe is
diagnosis — which commit state is recoverable — **not a finding about the file
it was given**."

Therefore there is no byte predicate corresponding to "a commit changed a fixed
declaration", and [R-CNF-02]'s "File conformance is a pure predicate on bytes"
makes that exactly the "no condition a file can exhibit" case. The
classification is right.

Second correctness point: writer-02 argues §18.2's use of the class does not
transfer. It does. §18.2 uses the class on a *second* ground, not
[R-ENC-06]'s: "the bar on sizing a buffer binds a reader rather than the
document, and so states no condition a file can exhibit at all." That is
actor-bound, exactly as §20.3's bar is ("This bar binds the commit as an
actor"). So the document has already extended the class beyond the one worked
case both reporters treat as its only ground.

Consensus REFUTED. Byte-level: no (both reporters concede; [R-CNF-02] settles
the verdict either way).

## G3 — Appendix G item 8 "modulo its trailer" (writer-01)

Verified. Item 8: "A compactor's output is therefore reproducible **only modulo
its trailer**". §20.4's MU = 0 / PE = 0 row: "a compactor MAY drop it whenever
it rewrites the file." §20.5: "the live committed state (§7.2), **less any
record §20.4 lets it drop**".

I re-ran the reporter's greps over Appendix G's own line range (4587–4751):
`drop` 0, `preserv` 0, `compactor` 7 (he said 8; the discrepancy is a range
boundary, not a wrap artefact, and does not touch the zeros). The zeros are
real: no numbered item and no closing-paragraph clause pins record retention or
the PE bit. A dropped record changes dir_length, downstream offsets, the
directory CRC, committed_file_length and F — not the trailer alone.

**Byte-level: no.** [R-CNF-01]: "All text in this document is normative except:
... appendices identified as non-normative." Appendix G is so identified and
says of itself "It adds no requirement to any actor: a writer ignoring it is
fully conforming." Both compactors are conforming and both outputs are
conforming files.

Consensus CONFIRMED. Severity editorial (a non-normative claim that disagrees
with the normative text it glosses). Repair: an eleventh item pinning
retention, or narrow item 8's "only modulo its trailer".

## G4 — "where a field is on both sides" and the reach claim (writer-04, adversary-02)

Same sentence, grouped. Verified field by field against §7.4's table.

The fixed list is: "the layout, the linearization and the index encoding, the
codec and the filter, the rank and the dimension order, every tile extent,
every channel's type and fill, an interleaved layer's channel list (its names
aside), and the position of every planar channel the new state keeps." **A
dimension extent is not in it**, and cannot be: the list opens "Every **other**
declaration is fixed", so it is the complement of the permitted list by
construction. Both reporters are right on the fact.

Reading (b) — "both sides" = the permitted and the barred — is not merely
available, it is the *better* reading, and this is where I differ from
writer-04's grading. Under (b) all three named examples work uniformly (extent:
grow permitted / shrink barred; planar list: end-extend/end-shorten permitted /
the rest barred; interleaved list: names permitted / the rest barred). Under
(a) only two of three work. And (b) has a real referent in the same step: "What
the line gives up is stated rather than carved around: **a shrink**, a fill
change, a re-type, ...". So the sentence is true under the reading that makes
all three examples uniform, and false under the one that makes two of three
work. That is not an ambiguity between two live readings; it is a sentence
whose looser reading is the wrong one.

adversary-02's second point — that entry_count, crc_of_crc_array, the extent
slot and the sub-record sequence are §7.4 rows the two lists do not reach — is
factually right but over-graded. The *same sentence* disposes of them
explicitly: "; entry_count and crc_of_crc_array follow the commit, the record's
extent slot with them (§7.2), and a layer's sub-records are §20.4's subject
whether or not the layer stores a tile." The semicolon clause is the narrowing
adversary-02 says the document nowhere makes.

**Byte-level: no.** "an extent MAY grow, and MUST NOT shrink" states the whole
of what a commit may do to a dimension extent under either reading, and the
fixed list's membership is unchanged.

Consensus PARTIAL: the illustration is loose, but the defect is narrower than
either reporter states.

## G5 — the slab half is stated over "kept" with no trigger (writer-03)

Verified. §20.3: "a slab declaration declared, changed **or kept** has its
invariants re-established over every run the new state keeps, or is cleared
(`[R-SLB-04]`)". [R-SLB-04] fires only on five named changes: "changes the
stored-tile set, the run partition, the byte placement of any run, the disk
ordinal of any tile the new state stores, or the slab declaration itself".
A rename-only commit makes none of them. So the restatement is broader than
the rule it cites. Real.

**I probed this for a byte fork and it does not open one.** The candidate fork:
if "has its invariants re-established" is read as requiring an *action*, a
rename-only commit on a slab-declared layer would have to re-lay every run —
appending payloads and re-emitting the index — or clear the declaration, and
that changes bytes. It does not, because both §20.3 and [R-SLB-04] state the
obligation as a *result over the new state*, not an operation:

> MUST either **re-establish the invariants for every such run** — or clear the
> declaration in the new generation

and [R-SLB-03] states the invariants as a standing property of the live state:
"When declared, for every run: the run's stored tiles are contiguous and packed
in ordinal order ... and the first stored tile's offset satisfies
offset mod A_slab = 0." On a conforming input those already hold and a
rename-only commit disturbs none of the four inputs to them, so the broad
reading is satisfied by doing nothing.

*The premise my downgrade rests on, stated for attack:* that "has its
invariants re-established over every run" is a state predicate on the new
generation and not an imperative to perform a re-lay. If a maintainer intended
the imperative sense, this **would** fork the bytes of a rename-only commit on
a slab layer. I record it as the single place in this round's input where a
byte fork is one word's reading away, and the repair below removes the
question.

Consensus CONFIRMED. Severity editorial. Repair: attach [R-SLB-04]'s triggers
to "kept", or ground the slab half in [R-SLB-03]+[R-CNF-05] as the alignment
half is grounded in [R-SLB-01]+[R-CNF-05].

## G6 — "the new state keeps" carries two senses (adversary-03)

**Refuted on the premise.** The reporter asserts the two uses are "mutually
exclusive". They are not: one uniform sense — *holds in the new state* —
satisfies all three uses without contradiction.

- "an aligned layer's stored tiles — every one the new state keeps, **not only
  those this commit adds** — satisfy its invariant". "X, not only Y" entails
  X ⊇ Y, so "keeps" here already includes added tiles. The reporter reads this
  correctly.
- "the position of every planar channel the new state keeps". Under the same
  sense this covers an appended channel too, whose position is newly assigned
  and therefore vacuously unmoved; it excludes channels a shortening removed,
  which is the contrast the clause needs. No incoherence.
- "every run the new state keeps" then means every run in the new state, which
  is what [R-SLB-03] requires unconditionally.

So the third use does not "inherit an ambiguity"; it inherits the one sense
that works everywhere. What survives is the *cosmetic* asymmetry the reporter
notices at the end: the alignment half carries an explicit appositive and the
slab half does not.

**Byte-level: no**, and on the reporter's own correct ground: [R-SLB-03] is
unconditional over the live state and [R-CNF-05] ("A writer MUST emit only
conforming files") bars a conforming writer from emitting an unpacked new run
under either reading — L41/L42 are registered rows.

Consensus PARTIAL.

## G7 — §4.7's structural/descriptive actor sets (verifier-01, adversary-04)

Same defect. Verified verbatim:

> A field is **structural** if its value determines anything a conforming
> **reader or verifier** does with the bytes it reads ... It is **descriptive**
> if it determines none of those: its value determines nothing a conforming
> **reader** does

The asymmetry is real. Both witnesses offered are not.

verifier-01's witness is "§7.2's record-header table classifies the flags
field, 'bits 2-15 reserved', as structural". I read the table. Its Field cell
is `flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved`
and the Class cell classifies **the flags field**, not the reserved bits. The
flags field is structural on the reader-only test alone: [R-CNT-15] makes an
unknown type's MU bit decide reject-file vs ignore-record. adversary-04's
witness — the stored MU and PE bits of a registered type ([R-CNT-22]) — fails
the same way: those are bits inside the flags field, and [R-ENC-16] classifies
"Every **field** this specification defines".

So no field witnesses the overlap, and the classes partition extensionally even
though the definitions overlap intensionally. What remains is a genuine
drafting asymmetry with no populated consequence, closed anyway by the next
sentence: "In format major 1 `version_minor` is the only descriptive field, and
every other field this specification defines is structural."

**Byte-level: no.** The label's one normative consequence, "a reader MUST NOT
alter decoding based on it", is separately stated for the disputed bits by
[R-CNT-12] ("readers MUST ignore them").

Consensus PARTIAL — right about the wording, wrong about the witness.

## G8 — the coverage walk's incompleteness test (verifier-02)

I pushed on this one hard, because a divergent slack total is the closest thing
in this round's input to an observable fork.

**The text decides it, and it decides it factually.** §5.2:

> The walk is incomplete **where a scope-level rejection ends that scope's
> enumeration**, where the verifier declined a layer on resource grounds
> (`[R-ERR-04]`) and so never enumerated its claimants, or where the verifier
> elected under `[R-CNF-11]` to stop at the first violation

"where a rejection **ends** that scope's enumeration" is a condition on the
ending, not a stipulation that a rejection ends it. §9.7 says the same with a
different verb: "Where the walk does not complete — a scope-level rejection
**blocks** enumeration, ...". The one stipulation in the passage is stated
expressly and only for layers: "A rejected layer's claimants are not
enumerated, **whether or not the rejection impeded reading them**." Its
presence at layer scope and absence at tile scope is the signal, and the
reporter reads it correctly.

§15.3 closes the residue the reporter says is left open: "An entry whose only
defect is that its stored bytes fail its crc is well-formed: the defect lies in
the bytes it addresses, not in the entry, so its extent stands and it **keeps
its place in the *verifier* rows, in run continuity, and in the coverage
walk**." That reason — the claimant comes from the entry, not the payload —
reaches T1, T3, T4, T14 and every codec row alike.

So reading (b) is not permitted; the reporter picked (a) and (a) is what the
text says. What is real is the narrower point in his own title: the tile gloss
names two cases and is silent on the rest, which costs a reader a
cross-section walk to reach an answer the text does determine.

**Byte-level: no.** The question arises only where a violation exists, so §2.3's
priority rule fixes the verdict at *nonconforming* either way ("An established
violation takes priority"), and the disputed quantity is a report line. No
conforming file is reachable by this question at all: the only incompleteness
causes are a rejection, a resource decline, or an elected stop.

Consensus PARTIAL.

## G9 — Example shape (c) and free re-declaration (diagrams-01)

Verified. The sentence sits between two explicitly-marked exclusions and is not
itself marked. But it marks itself differently, in its own words: "...which is
**the same step's permission**" — it cites step 4 as a permission, not shape
(c) as a shape. Reading B is available only by position, not by wording.

The reporter's substantive point is right and I checked it: an empty layer can
still *address* tiles (§7.4's own worked example — extents 100, tile extent 32,
"entry_count = 4", "With no tile stored, every index entry is the sentinel",
extent slot length 84), so a re-declaration changing the tile extent changes
entry_count and index content and trips step 4's unconditional clause: "Every
layer whose stored-tile set or index content this commit changes has its
tile-index region re-emitted in full ... necessarily at a new placement". §11.1's
Rationale draws exactly this distinction for growth and shape (c) does not.

**Byte-level: no.** [R-CNF-01] makes a labelled *Example* non-normative, and
step 4's clause is unconditional; a commit built from the figure alone would
emit an L21/L22 file that [R-CNF-05] bars every conforming writer from.

Consensus PARTIAL (right defect, weak second reading).

## G10 — §4.7's presentation Note vs §6.1 and §7.2 (diagrams-02)

Both halves verified.

(a) §6.1's table columns are `| Offset | Size | Value | Class |`. There is no
Field/name column, and the Note's carve-out only says "a Value column replaces
type and range". The fields are named elsewhere (F6's Instances cell: "magic
bytes [0,8); reserved bytes [8,16)").

(b) §7.2's table columns are `| Offset | Size | Type | Field | Class |` — no
Valid-values column at all. The Note says "§7.2 folds each field's range into
its Field cell". Of five fields, `type (0 invalid)` folds a range, `flags`
folds a bit assignment, and `inline_length`, `extent_offset`, `extent_length`
fold nothing; their constraints are in [R-CNT-12] and [R-CNT-13].

The escape "each table giving the columns its structure needs" does license
omission, but the Note's own practice is to name each omission, which is the
reporter's point and it is fair.

**Byte-level: no.** [R-CNF-01] exempts labelled *Note* text; every omitted name
and range is stated normatively elsewhere.

Consensus CONFIRMED, severity editorial.

## G11 — §18.2's `1 or 2` valid-values cell (diagrams-03)

Verified. §18.2's row reads `1 or 2; see below`, and the paragraph directly
below gives the full set, with §21.6 recording an experimental-range encoding
as a conforming file (ignore-record) and [R-EXT-03] behind it. The contrast
with §7.4's index_encoding row is real: that row spells out "any other value —
including 0, reserved 2–0x7F, and the experimental range ≥ 0x80 (§10) — is a
validity error at layer scope".

The reporter's harm claim ("a validator built from the cell alone") is softened
by the cell's own "; see below", which he reports. The near-parallel he
considers and rejects (§6.2's version_major cell) is correctly rejected.

**Byte-level: no.** The cell defers explicitly and R1 registers only encoding 0
and the reserved range as violations.

Consensus CONFIRMED, severity editorial.

## G12 — F5's reason clause names the pre-trailer pad (diagrams-04)

Verified, including the witness. [R-CNT-27] derives the floor from three
components: "the front signature block, a directory of at least 4 bytes at an
offset of at least 16, and the 64-byte trailer at a 64-aligned offset cannot be
satisfied in fewer." The pad is not one, and [R-CNT-05] says so directly: "a
writer that ends its directory on a 64-byte boundary leaves none."

The witness holds: F = 128, dir_offset = 16, dir_length = 48 gives directory
[16, 64) and trailer [64, 128) with zero pad; 16 + 48 = 64 = F − 64 satisfies
[R-CNT-06]; the 48 bytes carry a 44-byte record sequence (a 24-byte header plus
a 20-byte inline payload) and the 4-byte terminal CRC, with no residue (F29).
An experimental-range MU = 0 record with extent slot (0, 0) is conforming per
§21.6 and ignored per [R-CNT-15].

§21.1 governs: "where a row and the rule it cites diverge, **the rule
governs**", and the divergence is confined to F5's reason clause; condition,
outcome, detector, tier and instances all match.

**Byte-level: no.** Same condition, same outcome, same detector.

Consensus CONFIRMED, severity register-bookkeeping.

## G13 — §21.1's "— F27 and L48" (register-01)

Verified against the tables. F27 and L48 carry Governing rule `[R-MTA-05]`;
F28 and L49 carry `[R-CNT-22]`. So Reading B would be wrong twice, as the
reporter says.

But "undetermined" over-states. The parenthetical is semicolon-separated —
"(`[R-CNT-22]`, whose registered type keeps its fixed semantics; **and**
`[R-MTA-05]`, whose unsorted document readers process as they find it — F27 and
L48)" — so the dash-clause attaches to the second conjunct, and §7.1 uses the
identical pairing outside any ambiguity: "where a rule outside this quarantine
records a document's defect at the file or the layer (`[R-MTA-05]`, F27, L48)".
The reporter cites §7.1 himself and it settles the attachment.

What survives is the asymmetry: [R-CNT-22]'s two rows go unnamed where
[R-MTA-05]'s two are named.

**Byte-level: no.** Row conditions, outcomes, scopes and detectors are where
the tables put them; [R-VEC-01] makes a mislabelled vector wrong rather than
the document.

Consensus PARTIAL, severity register-bookkeeping.

## G14 — §21.6's trailer-mimic entry (register-02)

Verified, and the reporter is right. §21.6's Condition cell says "**A
payload** contains a byte string that mimics a trailer" and the Defined
behavior cell justifies inertness with "nothing enumerates **slack**". A live
tile payload is precisely what the walk *does* enumerate: §9.7 reaches "the
stored extent of each non-sentinel tile-index entry", and [R-CNT-02] makes a
stored-tile extent a structure of the live committed state.

§22.3 — which the entry condenses — keeps the two apart correctly: "under
live-state coverage a mimic **in slack** is inert — nothing enumerates it — but
a recovery tool that truncates to one produces a different file." And the
governing rule states the caution over a payload, not over slack: [R-LIF-06],
"a **tile payload** can deliberately contain a byte string that mimics a valid
trailer, so recovery output MUST be re-verified as a whole file".

So the entry's condition and its reason are of different classes. The right
reason for a live payload is that no reader scans backward and the walk claims
those bytes as a stored extent.

**Byte-level: no.** [R-LIF-06]'s obligations on recovery tools are unchanged
under either reading, and §21.1 already fixes that the rule governs a diverging
§21.6 entry.

Consensus CONFIRMED, severity register-bookkeeping.

## G15 — §21.9's "which every file and every layer carries" (register-03)

Verified. The first five rows are rank d of a layer, channels per layer C,
addressed tiles per layer (entry_count), layers per file, dir_length. Three are
per-layer. A zero-layer file is conforming three times over: §21.6's entry
("The file contains zero layers | A conforming file"), [R-CNT-14] ("zero is
valid: a directory carrying no layer record is a conforming generation"), and
§5.1's 128-byte Example.

Under the distributive reading the clause is true; under the universal reading
a conforming file refutes it. Either way it fails to support the contrast it is
there to draw, since a zero-layer file has no instance of the first three rows
just as a tile-less layer has none of the tile row.

The preceding sentence already covers the case: "Either way a file containing
no instance of a kind does not exceed that row, whatever its declarations would
derive."

**Byte-level: no.** [R-CNF-03]'s acceptance duty runs to a zero-layer file
under both readings; nothing to exceed.

Consensus CONFIRMED, severity editorial.

## G16 — §21.1's "the row is the rule" (register-04)

Verified both sentences, twenty lines apart in one subsection:

> ... but each row *restates* its governing rule, and where a row and the rule
> it cites diverge, **the rule governs**.

> The **Instances** column enumerates what a conformance corpus builds for that
> row (§21.8): **the row is the rule**, and each instance is one file.

The second is a mapping statement inside a corpus-building sentence — row ↦
the unit tested, instance ↦ one file — and its parallel clause ("each instance
is one file") confirms that shape. §24 [R-VEC-02] keeps the two distinct as
things a manifest records both of, and [R-VEC-01] puts the specification above
the vector. So the authority reading is ruled out three ways.

What is left is a real collision of wording in one subsection: a document that
says "the rule governs" should not say "the row is the rule" a few lines later.

**Byte-level: no.**

Consensus CONFIRMED, severity editorial.

## G17 — §21.8's "one vector per instance" (register-05)

Verified both. §21.8: "has **at least one** conformance vector (§24) whose
expected outcome is that row's outcome, and **one vector per instance**." §24
[R-VEC-03]: "every register row has **at least one** vector for each instance
it names".

The cap reading is not a live reading. "one vector per instance" in this
context is a coverage floor, and both neighbours say so: "A row without a
vector is a gap in the corpus, not a licence to skip the check" (§21.8) and "A
missing vector is a gap in the corpus and never a licence to skip the check it
would have exercised" (§24). Nothing anywhere gives a reason to cap a corpus,
and [R-VEC-03]'s own further demand (a vector at every sentinel, boundary and
hard limit) would be unsatisfiable under a cap wherever such a vector coincides
with a covered instance — which the reporter notices.

So: a real inconsistency of phrasing between two statements of one inherited
obligation, not an ambiguity.

**Byte-level: no.** Both rules bind the corpus, and [R-VEC-01] makes it
derivative.

Consensus PARTIAL.

## G18 — the decoded-size parenthetical omits L44 (adversary-05)

Verified. The sentence:

> ... but for a decoded size, a padding position or pad bit, or a boolean byte
> the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that
> fails outright under a changed codec or filter (T24, T25), no check any actor
> owes able to see it (§21.7)

L44 exists and is a decoded-size row ("Codec 4 (lz4) declared on a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes", detector reader,
layer access), and the reporter's re-tiling arithmetic is right.

But the reporter's own counter-argument is the correct one, and the document
confirms it. The sentence's subject is what a *stored tile's bytes now denote*
— "Under new ones the same bytes would denote values, coordinates or padding
the writer did not store". L44 and L2 witness an out-of-bounds *declaration*,
not a misdenoting tile. And §20.3 handles those in the very next paragraph,
citing L44 by name: "A permitted change holds provided the declarations and
geometry it produces stay within every bound they are subject to:
`[R-COD-07]`'s lz4 decoded-size cap (L44 ...); `[R-ENC-04]`'s 2⁶³ − 1
ceiling ...". So the omission is deliberate scoping, not a gap.

**Byte-level: no.** The sentence is a rationale for a bar already stated and
classified; L44 requires of a reader exactly what it requires either way.

Consensus PARTIAL.

## G19 — Appendix F pins no HTTP reference (adversary-06)

Verified. Appendix F is headed "Normative references" without a
"(non-normative)" marker — unlike Appendices A–E and G–H — so [R-CNF-01] leaves
it normative. Its entries are BCP 14, RFC 3720, IEEE 754, RFC 1950, RFC 1951,
RFC 1952, RFC 8878, LZ4 Block, RFC 8259, RFC 3339, Unicode, plus an
"Informative:" line for OCP OFP8. No HTTP specification.

[R-CNT-10] states a MUST in HTTP vocabulary: "A remote reader MUST handle a 200
response to a range request ... and SHOULD fall back to a size probe plus an
absolute range on transports without suffix-range support". §6.4 adds "a suffix
range, whose response also carries the transport-authoritative file size".

One correction to the reporter's framing: the quantity he says is left
undefined — "what counts as the transport-authoritative length" — is defined in
[R-CNT-10] itself, parenthetically: "(a full-response content length, the
complete length of a range response, or a size probe)". So the accept/reject
path (F17's cross-check) does not hang on the unpinned vocabulary. What is
genuinely unpinned is "200" and "suffix-range support".

**Byte-level: no.** The rule constrains a reader's transport conduct; the
file's bytes and every verdict are identical either way.

Consensus PARTIAL, severity editorial (or design-decision: whether to pin an
HTTP reference at all is a maintainer's call, since the substantive obligation
is restated in plain terms).

## G20 — half-sentinel entry, T7 vs T11 (quiz-02)

Verified. §15.2: "Sentinel entries are a reserved pattern, not offsets or
lengths: `[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to
the fields of **non-sentinel entries only**." An entry with offset = all-ones
and length = 5 is not a sentinel entry, so on §15.3's face two rows reach it:

> | offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*: reject-tile |
> | offset > 2⁶³ − 1 or length > 2⁶³ − 1 (non-sentinel) | *structural*: reject-tile (`[R-ENC-03]`) |

Both give the same outcome, so §15.3 costs a reader nothing. The register does
double-offer T7 and T11, and only T11's own Condition cell excludes the case —
"the value being distinct from the all-ones sentinel" — a qualification §15.3
does not carry. The reporter's inversion point is sharp and correct: §21.1 has
the row *restate* the rule and lose to it where they diverge, and here the row
carries a qualification the rule lacks.

§21.1's enumerated specialization pairs do not name T7/T11, but that list "is
not offered as closed", so this is not a violation of a closed list.

**Byte-level: no.** Both candidate rows are reject-tile, reader-detected, at
tile use, and the entry contributes no claimant to the coverage walk either
way (§15.3, §9.7).

Consensus CONFIRMED, severity register-bookkeeping.

## G21 — §21.1's rules carry no identifier (quiz-03)

Verified. §21.1 carries no *Note*/*Example*/*Rationale* label and is not in an
appendix, so [R-CNF-01] makes it normative. Every bracketed identifier in it is
a citation of a rule stated elsewhere; the subsection ends without one, while
§21.7 ends `[R-ERR-01]`, §21.8 `[R-ERR-02]`, §21.9 `[R-ERR-03]`…`[R-ERR-05]`.

The reporter under-cites his own case. §2.2's opening sentence is the one that
bites: "**Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`.**" §21.1 states at least one rule that binds an actor —
"the file is recorded against the narrower row, whose detector and detection
point are the ones that apply" — with no identifier, and §24 [R-VEC-02] obliges
a manifest to record "that row's governing requirement identifier".

Whether §21.1's completeness clause and rule-over-row tie-break are
*requirements* or *interpretive conventions about the document* is the question
a maintainer has to answer; the specialization rule is the one that most looks
like a requirement.

**Byte-level: no.** [R-CNF-01] makes the text bind whether or not it is
numbered; only a manifest entry's form changes.

Consensus CONFIRMED, severity design-decision.

---

## Coverage check

Groups: G1(3) G2(2) G3(1) G4(2) G5(1) G6(1) G7(2) G8(1) G9(1) G10(1) G11(1)
G12(1) G13(1) G14(1) G15(1) G16(1) G17(1) G18(1) G19(1) G20(1) G21(1).
Sum = 3+2+1+2+1+1+2+1+1+1+1+1+1+1+1+1+1+1+1+1+1 = 26. Input ids = 26. Each id
appears once; I listed them and struck them off one at a time against the input
list. No id dropped, none duplicated.

Byte-level upheld: 0.
