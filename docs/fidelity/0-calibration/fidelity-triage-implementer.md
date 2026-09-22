# Triage pass — implementer-consequence lens

## Access and method

Read only the two permitted editions:
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (4981 lines)
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md (4977 lines)

No transcript-*.md files were opened (not needed: every finding's cited passage was
checked directly against both editions).

Disclosure: no material was placed in my context before I began beyond the task
text itself (the 67 findings and their quotes), which is not evidence and was
independently re-checked against the source files below.

Decisive move: I ran a full `diff -u a/tarn.md b/tarn.md` over the two complete
files (not just the cited line ranges) and confirmed there are **exactly six**
textual hunks between the editions, byte for byte:

1. §6.3 — `MUST NOT clear them, and` removed from the ignore-lane sentence.
2. §20.3 step 2 — `save where §20.4 licenses the drop` removed from the
   appender's no-drop sentence.
3. §20.3 worked Example — `644` changed to `664`.
4. §20.4 — `reaches only a type the updater does not implement` changed to
   `reaches every type, implemented or not`.
5. §20.4 — the sentence `One sub-record blocks the drop, ... (the table's
   first row).` removed.
6. §21.2 register row F19, Instances cell — `flags bits 0-15` changed to
   `flags bits 0-7`.

Every one of the 67 findings traces to one of these six hunks, or reports no
textual difference at all (confirmed by grep/diff against both files at the
cited section). This let me settle, with certainty rather than inference,
which findings describe a real cross-edition difference and which do not
(including all fourteen quiz-matrix items, none of whose cited passages fall
inside any of the six hunks).

## Groups

### G1 — ignore-lane "MUST NOT clear them" dropped (§6.3, [R-CNT-08])
Members: cmp-reader-01, cmp-writer-06, cmp-verifier-06, swab-01, adv-05

A: "An updater MUST copy forward unknown ignore-lane bits of its input file,
MUST NOT clear them, and MUST NOT set any other..."
B: "An updater MUST copy forward unknown ignore-lane bits of its input file,
MUST NOT set any other..."

Verdict: EQUIVALENT. "Copy forward X" is itself the affirmative duty to
reproduce X's bit values unchanged in the output; clearing a bit that was set
is not copying it forward, so B's remaining clause already forecloses
clearing. This is independently confirmed by the trailer flags-field table
(§6.2, line 838, byte-identical in both editions): "bits 16-31 (ignore lane)
... carried forward unchanged by every updater (appender and rewriter alike)"
— an unqualified, unchanged obligation that already binds every updater in
both editions regardless of §6.3's wording. No implementation conforming to
B's text (either clause, or the §6.2 table) could clear an ignore-lane bit
while still conforming. byte_level: false.

### G2 — appender's carve-out for §20.4-licensed drops dropped (§20.3 step 2)
Members: cmp-reader-02, cmp-writer-02, cmp-verifier-03, swab-02, swba-01, adv-01

A: "...it MUST NOT repair the defect — [R-LIF-01] freezes the committed
prefix — and MUST NOT drop the record save where §20.4 licenses the drop."
B: "...it MUST NOT repair the defect — [R-LIF-01] freezes the committed
prefix — and MUST NOT drop the record."

§20.4 (unchanged, both editions): "an appender MAY drop the record in any
commit it is otherwise free to make" for an MU=0/PE=0 record, and "A commit
MAY therefore drop a layer record" for a PE=0-registry-fixed layer.

Verdict: LOSS, BYTE-LEVEL. Implementer consequence: an appender built
strictly, procedurally, from B's step 2 (a numbered "MUST, in order" list) as
an unqualified prohibition has nothing at that point in the text to admit the
§20.4 exception, and a strict reading commits it to retaining every
carried-forward record it does not itself modify — including one §20.4
explicitly licenses it to drop. On a commit whose only requested edit is
dropping a PE=0 sub-record (or an otherwise-droppable layer), a B-only
implementation that follows step 2 literally emits a directory that still
carries that record's header, extent slot and (for a layer) its sub-records
and tile-index region; an A-only implementation drops them and reclaims the
slot. Different directory bytes for the identical input and requested edit.
(A careful B-only implementer who separately notices and resolves the tension
in favor of §20.4 would match A — but nothing in B's own step 2 text forces
that resolution, which is exactly the loss: A states the reconciliation
in-line, B does not state it anywhere.)

### G3 — worked example: 32·20+4 stated as 664 instead of 644
Members: cmp-reader-03, cmp-writer-05, cmp-verifier-04, swab-03, swba-02,
adv-02, writerb-01

A: "...the layer's full new index region (32 · 20 + 4 = 644 bytes...)"
B: "...the layer's full new index region (32 · 20 + 4 = 664 bytes...)"

32×20+4 = 644; B's figure is a plain arithmetic error. This passage sits
inside a block explicitly labeled "**Example.**", and [R-CNF-01] (identical,
unchanged, both editions, line 105-107) states: "All text in this document is
normative except: ... any text labeled *Note*, *Example*, or *Rationale*."
The general, normative sizing rule [R-CNT-17] (`entry_count × 20 +
⌈entry_count/2¹⁶⌉ × 4`) is unchanged, correct, and identical in both editions
at §7.4/§15.1 and in register row L22, and is what a conforming writer's
actual output length and a conforming reader's/verifier's L22 cross-check
apply — not the example's own stated total.

Verdict: LOSS (a worked figure A states correctly and B states incorrectly —
explicitly named in the fidelity test's LOSS definition), but NOT byte-level.
Implementer consequence: a writer or verifier built strictly from either
edition's normative text (the formula) computes 644 for this scenario
regardless of edition; nothing in a conforming implementation's decision path
consults the Example's own prose number. The only party who could be misled
into producing or expecting a 664-byte region is a human hand-deriving or
proofreading a test fixture from the illustration rather than the formula —
real, but not an implementation-level fork. byte_level: false.

### G4 — §20.4 MU=1 row's reach inverted, contradicting its own next clause
Members: cmp-reader-04, cmp-writer-03, cmp-verifier-01, swab-04, swba-03,
adv-03

A: "Its MU = 1 row reaches only a type the updater does not implement — ...
— so for an implemented type only the PE bit bites:"
B: "Its MU = 1 row reaches every type, implemented or not — ... — so for an
implemented type only the PE bit bites:"

B keeps A's concluding clause ("so for an implemented type only the PE bit
bites") verbatim while changing the premise it depends on to its opposite,
producing an internally self-contradictory sentence: if the row truly
"reaches every type, implemented or not," it does not follow that "only the
PE bit bites" for an implemented type, since the MU=1 row's own "MUST NOT
modify the scope the record governs" (and, at layer scope, its block on
dropping the layer) would also apply. A's premise and conclusion agree; B's
do not.

This is reachable, not academic: [R-CNT-12] (§7.2, unchanged, both editions)
states "Writers MUST NOT emit the combination MU = 1 with PE = 0," which
implies MU = 1 with PE = 1 is a legitimate, emittable combination. An updater
that implements an unregistered type it defines itself (the same paragraph's
own example) can therefore legitimately hold a sub-record of a type it
implements whose governing flags are MU = 1, PE = 1.

Verdict: LOSS, BYTE-LEVEL. For such a record: an A-built updater applies "for
an implemented type only the PE bit bites" cleanly (PE = 1: retain
byte-identical, extent unmodified — but the MU = 1 row's separate "blocks
modification of that layer, its drop included" does NOT apply, since the row
does not reach this implemented type). A B-built updater that takes its own
literal first clause ("reaches every type, implemented or not") would instead
apply the MU = 1 row's layer-drop block to this same record, refusing a
whole-layer drop that an A-built updater performs. Different accept/reject
verdicts and different directory bytes for the identical commit on the
identical input.

### G5 — layer-drop MU=1-sub-record exception sentence dropped
Members: cmp-reader-05, cmp-writer-01, cmp-verifier-02, swab-05, adv-06

A, immediately after "...so a dropped layer's sub-records and their extents
go with it whatever their PE bits.": "One sub-record blocks the drop, a
sub-record of a type the updater does not implement with MU = 1, the drop
being a modification of the scope it governs (the table's first row). A
commit never removes a user-metadata record from a scope it keeps..."
B: "...so a dropped layer's sub-records and their extents go with it whatever
their PE bits. A commit never removes a user-metadata record from a scope it
keeps..."

I checked "the table's first row" the deleted sentence cites: the MU = 1 row
of the updater-obligation table, three paragraphs above, unchanged and
present verbatim in both editions: "At layer scope an unknown critical
record blocks modification of that layer, its drop included, leaving other
layers editable ([R-CNT-18])."

Verdict: EQUIVALENT. The deleted sentence is a restatement/cross-reference of
a rule the table row states in full, on its own, in both editions —
including "its drop included." A whole-document reading of B still forbids
dropping a layer that carries an unimplemented, MU=1 sub-record; the deleted
sentence added no obligation the table row did not already carry. This is a
closer call than G1 (the deleted sentence sat right after an unqualified-
looking "MAY drop... takes the layer whole," which reads more permissively in
isolation), but the governing rule survives, unweakened, three paragraphs
earlier in B's own text. byte_level: false — no implementation correctly
reading the whole of either edition's §20.4 diverges here.

### G6 — register row F19's Instances cell narrows bits 0-15 to bits 0-7
Members: cmp-reader-06, cmp-writer-04, cmp-verifier-05, swab-06, adv-04,
readerb-02

A, row F19: "Any bit of the flags incompat lane (bits 0-15) is set..." |
Instances: "flags bits 0-15" | ... | `[R-CNT-08]`
B, same row, same Condition text: Instances: "flags bits 0-7" | ...

Both editions' Condition cell for F19, and §6.2's trailer flags-field table
(line 838), and [R-CNT-08]'s own governing text (§6.3) are byte-identical and
unqualified over the full incompat lane (bits 0-15). §21.1 ("How to read the
register," byte-identical in both editions) states explicitly what the
Instances column is for: "The Instances column enumerates what a conformance
corpus builds for that row (§21.8): the row is the unit a vector is
attributed to ([R-VEC-02]), and each instance is one distinguishable file,
covered by at least one vector ([R-VEC-03])." That is a corpus-construction
column, not the row's statement of the check itself; the check is the
Condition cell plus the governing rule, both unqualified in B as in A.

adv-04 constructs a concrete file (bit 10 set) and argues a verifier "built
from B's narrowed register alone" would certify it — but that presupposes an
implementer derives runtime accept/reject logic from the Instances/Field
column rather than from the Condition cell and [R-CNT-08], which is not what
§21.1 says that column is for, and not what either edition's normative flow
(§6.2/§6.3, followed at open, before F19 is ever consulted as a register
cross-reference) requires. A verifier that implements F19's Condition text
and [R-CNT-08] as written — the only normative path — rejects that file under
both editions.

Verdict: LOSS, not byte-level. The defect is real and unique to B (confirmed:
A's own Instances cell says bits 0-15, matching its Condition cell; only B's
disagrees with its own Condition cell), and it degrades the register's
internal self-consistency and its stated conformance-corpus coverage promise
(a corpus built strictly to this cell's letter, per [R-VEC-02]/[R-VEC-03],
would ship without an explicit vector for e.g. bit 12) — but it does not
change any conforming reader's or verifier's accept/reject decision on any
actual file, because that decision is governed by the unchanged Condition
cell and the unchanged, unqualified [R-CNT-08], both of which state the full
bits 0-15 range in B exactly as in A. byte_level: false.

### G7 — verifier-walk quiz confirmations V1-V6 (no divergence)
Members: cmp-verifier-07, cmp-verifier-08, cmp-verifier-09, cmp-verifier-10,
cmp-verifier-11, cmp-verifier-12

Each of these re-checks a quiz item (§2.3 verdict vocabulary; §10.2/F35/F36;
§5.x slack arithmetic; §17.4 codec certification; §20.3 step 4/§9.7 history
independence; §7.2 [R-CNT-12]/F25/L46) and reports the cited passages
byte-identical between editions. My full-file diff confirms none of these six
citation sets falls within any of the six real hunks.

Verdict: EQUIVALENT (in fact, no divergence exists to grade — these are
confirmations, and I concur with each). byte_level: false.

### G8 — writera-01: same-commit drop-and-recreate zero-copy ambiguity
Members: writera-01, cmp-writer-07

The escape-hatch sentence writera-01 hinges on ("a commit MAY drop the layer
(§20.4) and add a new one under its name and other declarations, the new
layer being new whatever bytes its entries address, the dropped layer's
former extents included...") is byte-identical in both editions (confirmed:
§20.3 step 4 region, lines ~3291-3298 in A / ~3289-3296 in B, `diff` shows no
hunk there). The ambiguity writera-01 raises (whether new index entries may
legitimately re-point, unwritten, at the same commit's own just-vacated
extents) is real, but it is a property of both editions equally, not
something one states and the other omits.

Verdict: EQUIVALENT — this is not a cross-edition difference at all; the
identical indeterminacy is present, and resolves (or fails to resolve) the
same way, whichever edition an implementer builds from. byte_level: false
for the cross-edition question (an implementation built from A alone and one
built from B alone face the identical open question and could only diverge
from each other's sibling implementation, not systematically by edition).

### G9 — writera-02: cross-layer slab-recheck ambiguity
Members: writera-02, cmp-writer-08

[R-WRT-03] and the §11.1 Rationale note writera-02 relies on are confirmed
byte-identical in both editions (checked the [R-WRT-03] text and its citing
context). Same conclusion as G8.

Verdict: EQUIVALENT. byte_level: false.

### G10 — no outcome class for a reader lacking a mandatory codec/filter
Members: readera-01, readerb-01

Both walks raise the same gap from the same governing text: [R-CNF-03]'s
unconditional "conforming reader implements every core codec/filter," and
[R-COD-11]'s "software unable to execute an assigned codec or filter is not a
conforming reader" — confirmed byte-identical at every citation in both
editions (§17.4/[R-COD-11], §21.6, §21.9/[R-ERR-04]).

Verdict: EQUIVALENT — the same design gap, worded identically, in both
editions; not something one edition decided and the other left open.
byte_level: false for the cross-edition question (whatever an implementer of
degraded-capability software does here, it faces the identical text in A and
B).

### G11 — verifier-A's own design observations (§2.3 cannot-certify gap; §21.1 open subsumption list)
Members: cmp-verifier-13, verifiera-01, verifiera-02

cmp-verifier-13 confirms, and I independently confirm, that §2.3/[R-CNF-11]
(the cannot-establish trigger for an MU=1 experimental-range record) and
§21.1's "the property decides any pair and this list is not offered as
closed" are byte-identical in both editions.

Verdict: EQUIVALENT. Both are genuine properties of the specification's
design, present identically in both editions. byte_level: false.

### G12 — verifier-B's own design observations (coverage-walk triggers; fixed-declaration-bar undetectability)
Members: cmp-verifier-14, verifierb-01, verifierb-02

Same treatment: §5.2/§9.7's partial-total trigger list and §20.3 step 4/§9.7's
history-independence note are byte-identical in both editions (confirmed).

Verdict: EQUIVALENT. byte_level: false.

### G13 — quiz-matrix answer divergences: no underlying edition difference
Members: quiza-quiza-06, quiza-quiza-09, quiza-quiza-13, quizb-quizb-01,
quizb-quizb-02, quizb-quizb-03, quizb-quizb-05, quizb-quizb-06,
quizb-quizb-07, quizb-quizb-08, quizb-quizb-09, quizb-quizb-10,
quizb-quizb-12, quizb-quizb-15

For each of these fourteen items I located the passage(s) the two takers cite
in both editions. None falls inside any of the six real hunks (independently
confirmed by the full-file diff described above), and for the several I
checked byte-for-byte in full (quiza-06's §20.3 step-4 fixed-declaration
paragraph; quiza-09's and quizb-03's [R-CNT-17]/L22 formula; quiza-13's
[R-WRT-06] "two disposals" paragraph; quizb-01's [R-COD-07]/L44 rows;
quizb-08's §5.2/§9.7 walk-completeness paragraph and [R-ERR-04] citations;
quizb-10's §20.3 step-4 channel-list rules; quizb-12's version-gate ordering)
the cited text is byte-identical, word for word, between editions.

Where the two takers' stated answers differ (e.g. quiza-06's "new layer" vs
"new layer or rewrite"; quizb-08's "partial" vs "complete" slack total), the
divergence therefore cannot be attributed to anything edition B changed or
omitted — it is a disagreement between two readings of the *same* text,
which the charter's own rule assigns to REPORTER_ERROR ("a taker that
misread a text which decides the question is REPORTER_ERROR"). I did not
attempt to adjudicate which taker's answer is correct for each of the
fourteen (that is a separate question from fidelity between editions), only
that neither editions' text is responsible for the disagreement.

Verdict: REPORTER_ERROR for all fourteen. byte_level: false (by construction:
identical source text cannot make a B-only implementation diverge from an
A-only one).

## Coverage check

67 input ids listed. Groups G1-G13 have 5+6+7+6+5+6+6+2+2+2+3+3+14 = 67
member ids, each input id appears in exactly one group (verified by listing
every id above against the master list in the task).
