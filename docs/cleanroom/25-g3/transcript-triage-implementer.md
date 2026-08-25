# Round 25 triage — implementer-consequence lens

## What I read

Only `spec/tarn.md`. Sections read in full or in relevant part: §1, §2.1–§2.5,
§3.1–§3.2, §4.7, §5.1–§5.2, §6.1–§6.4, §7.1–§7.4, §9.5–§9.6, §11.1–§11.4,
§12 head, §14.1–§14.5, §16.2, §18.2 (encoding + the four document
restrictions), §19.1–§19.3, §20.3–§20.5, §21.1–§21.9, §23.1, §24, Appendix G.
I did NOT open any `transcript-*.md` — not the walks, not (obviously) the
triage notes. Every quotation below is from the spec file itself.

One mechanical check run (python, counting §21.2–§21.5 rows and
semicolon-separated Instances cells): 121 rows, 277 instances, matching
§21.8's stated "121 conditions over 277 instances" exactly as the cells are
written today. That matters for the R8 group.

## Standing premise for every downgrade in this pass

The byte-level test I applied is the one stated: does resolving the item
change which byte sequences a conforming implementation may emit, or must
accept or reject? I read that as a test about the format's *predicate on
bytes* and about reader/verifier verdicts on a single file, not about which
of two conforming outputs an updater picks for a given caller request. The
document itself draws that line, and I lean on it repeatedly:

> §2.3 `[R-CNF-02]`: "File conformance is a pure predicate on bytes: it does
> not depend on any reader, writer, or environment. ... A few obligations
> this specification places on writers govern their *conduct* rather than
> their output ... and a file is never nonconforming by virtue of one:
> conduct rules bind the actor, the predicate binds the bytes."

If a maintainer wants the gate to cover updater-conduct forks as well, groups
5 (step-4 list) and 7 (drop licence) are the two that flip. I state that
explicitly rather than burying it, because the premise — not the reasoning on
top of it — is where this pass could be wrong the way round 16 was wrong.

## Groups

### 1. F5 / `[R-CNT-27]` unordered against the version gate — reader-01, register-01, diagrams-02

Three reporters, one defect, described from §5.1, §6.2 and §21.2. Verified:
§6.2's ordered list is "the trailer magic; the trailer CRC; the version gate
(§6.3) ... and then, those gates passed ... the flag gates;
committed_file_length ...; dir_offset ≥ 16; dir_length ≥ 4; dir_offset +
dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes
zero." `[R-CNT-27]` is nowhere in it, and F5's first instance is "F (physical
file size)", which §19.1 step 1 obtains before step 2 fetches the trailer.
§21.2's preamble is normative (§2.1 exempts only §1, Note/Example/Rationale,
non-normative appendices), and it asserts a closed count of four exception
rows on a warrant — "§6.2 puts the version gate ahead of every check but the
trailer magic and the trailer CRC" — that does not reach F5. Confirmed.

Byte-level? No. The witness (F = 80, front block exact, trailer at [16,80),
version_major = 7, CRC verifying over [16,76)) is refused by every reader
either way:

> §6.3 `[R-CNT-07]`: "A reader MUST reject-file when version_major is 0
> (invalid) or is a major it does not implement".

And the verifier verdict the reporters worry about is decided outside this
paragraph:

> §2.3 `[R-CNF-02]`: "a file declaring another major is neither conforming
> nor nonconforming under it: a reader refuses such a file on capability
> grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about its
> bytes."

`[R-CNT-27]`'s own text is "No *conforming* file is shorter than 128 bytes";
a file this document declines to judge is neither conforming nor
nonconforming, so no violation is *established* against it and §2.3's
"established violation takes priority" clause never fires. Reading A is
foreclosed for a verifier. What is left is the reader's diagnostic class,
which §6.3 constrains at SHOULD level only. So: no emittable byte sequence
moves, no accept/reject moves, no MUST-level verdict moves.

Extra check none of the three ran, recorded because it bears on the repair:
for a *major-1* file, F5 is never isolable. committed_file_length must equal
F and be a multiple of 64, so in 64 ≤ F < 128 the only candidate is F = 64,
which fails F10 (dir_offset ≥ 16 and dir_length ≥ 4 give a sum > F − 64 = 0);
any non-multiple of 64 fails F13 or F17 first. `[R-VEC-02]` already
anticipates non-isolable conditions, so this is not a new defect, but a
maintainer recounting rows should know F5's vector is a multi-row entry.

Implementer consequence, concretely: the cheap `if (F < 128) fail "corrupt"`
at the top of open is the obvious placement, and it turns a well-formed
future-major file into "your file is corrupt" — the exact harm `[R-CNT-07]`
names ("misleads users into discarding files that current software reads").
Cost is a diagnostic, not a byte.

### 2. "geometry" under-describes the excused set — quiz-01

Same paragraph as group 1, different defect: the excusing predicate ("whose
subject is that file's *geometry*") and the exception predicate ("their
subject is a field fixed across every major") are not complements, so rows
like F12 (file_id = 0), F15 (reserved bytes), F19 (incompat bit), F20
(directory CRC), F24 (type 0), F27, F34 are neither excused nor excepted.
Kept separate from group 1 because repairing the word "geometry" leaves
`[R-CNT-27]`'s ordering gap standing, and repairing the ordering leaves the
word standing. Not byte-level, and for the same quoted reason as group 1 —
§2.3 puts the whole file outside the judgement, so no row can be recorded
against it whatever "geometry" means.

### 3. §23.1 cites shape (c) for an operation §20.3 assigns to (b) — reader-02

Verified both sides. §20.3 shape (c): "Editing user metadata is not this
shape: its document lives in an extent (`[R-CNT-25]`), so a new extent is
appended and the old one becomes slack, as in (b)." §23.1: "editing a
user-metadata document appends a new extent and strands the old one (§20.3's
shape (c))". Flat contradiction of label; the mechanics agree. Not
byte-level — §20.3 decides the classification outright in the quoted
sentence. Implementer consequence: a deployment reading §23.1 to learn which
operations strand data is pointed at the one figure that strands nothing.
Editorial, one-word repair.

### 4. §20.3 step 2's "MUST NOT drop the record" — reader-03

Verified step 2: "Against any other structure the appender carries forward,
it MUST NOT repair the defect — `[R-LIF-01]` freezes the committed prefix —
and MUST NOT drop the record (§20.4)." The clause's own premise is
"structures the appender **carries forward**", which excludes a dropped
record by construction, and the bare "(§20.4)" is this document's citation
form for a governing rule stated elsewhere. §20.4's MU = 0 / PE = 0 row
licenses the drop under stated conditions. The reporter's hesitation is fair
(§20.5 states the compactor's version of the same question explicitly and in
the opposite direction), but the text supports the restatement reading. Not
byte-level: both outputs are conforming files, and the fork is whether one
updater run was conforming conduct. Editorial: write "and MUST NOT drop the
record except as §20.4's table licenses".

### 5. §20.3 step 4's list is short of its own test — writer-01, adversary-01

Grouped: both reporters attack the same sentence and the same structural
defect — the enumerated list after the dash is not co-extensive with the
governing test — from the test's two limbs. writer-01 attacks limb 1 ("what
§14 fixes for its stored bytes"): the list names "the set of padding
positions (§11.3) and the content `[R-SER-05]` fixes there", and §14.3 is
emphatic that "Pad bits are not padding positions (§11.3)", so pad bits and
`[R-SER-08]`'s interleaved boolean bytes are outside the list's words.
adversary-01 attacks limb 2 ("or how they decode"): a channel's declared
sample type, the channels' declared order, and the dimension order are all
things §14 decodes by and none is in the list.

Both are right that the list is short, and the document says so itself: "The
test is the effect on such a tile, and the list names where that effect
arises rather than standing on its own". §21.7's witness account, however,
is written against the list, and it too omits the type case.

Byte-level? No, and here is the premise, stated so it can be attacked. Two
sub-cases:

(a) Affected tiles remain stored and the change reaches §14-constrained
content (writer-01's planar-bool fill change). The output is nonconforming
under *both* readings — T5/T2 fire on `[R-SER-05]`/`[R-SER-08]` — and
`[R-CNF-05]` ("A writer MUST emit only conforming files") catches the
list-reading writer regardless. Nothing about the emittable set moves.

(b) The change reaches only the decode mapping (adversary-01's
float32 → int32 with fill bytes untouched and E a multiple of T). The output
is a conforming file under both readings — `[R-TYP-05]` makes every bit
pattern of a numeric type valid — and §21.7 records the gap in terms:
"§20.3 step 4's bar on a declaration change is witnessed only where the
affected tiles remain stored, and then only for part of what it bars." No
verifier can diverge, because there is nothing in the bytes to diverge about.

So the fork is in updater conduct, not in the predicate on bytes. I want to
be blunt that this is nonetheless the highest-cost group in the batch on my
lens: an appender built from the list — and the list is the only operational
form the bar takes — will accept "re-declare channel `a` from float32 to
int32" as a directory-only edit, re-emit the directory, and hand the caller a
file in which every stored sample now denotes a different number, with no
check anywhere in this document able to report it. Two teams do go down
different roads here. If the gate is meant to cover updater-conduct forks,
this is the group that flips.

### 6. §11.1's growth Rationale is false for two or more zero extents — writer-02

Verified the counterexample: `[R-GEO-02]` places no limit on how many
dimensions carry extent 0. With E = (0, 0), T = (4, 4), growing E₀ to 4 gives
G = (1, 0), N = 1·0 = 0, entry_count 0, extent_length 0 — a grid count rose
and entry_count did not change, contradicting "growth that raises one changes
entry_count and with it extent_length (`[R-CNT-17]`)", and its trailing
clause "the first growth of a zero-extent layer included" is wrong in the same
case. Non-normative (§2.1: "any text labeled *Note*, *Example*, or
*Rationale*") and every byte is independently fixed by `[R-CNT-17]`,
`[R-CNT-23]` and L22. Editorial.

### 7. Does adding a top-level record license dropping an MU=0/PE=0 record? — writer-03

Verified the row. The licence list for a top-level record is "the file's
layer set, any layer record's content, or another *non-layer* top-level
record". The first item is a *set* and the next sentence glosses addition
into it ("A commit changes the layer set by adding a layer"); the third names
a *record*, and adding a new one changes no existing one. The row forecloses
the lead phrase being read loosely ("a commit whose only effect would be the
drop MUST retain it") and expressly excludes one same-commit record operation
("Dropping the record, or dropping another record in the same commit, is not
itself such a change") without saying anything about adding one. Genuinely
underdetermined; the purposive reading and the literal reading part company.

Not byte-level: both resulting directories are conforming files (§21.6 makes
an unassigned-type MU = 0 record conforming whether present or absent), and
the same bytes are emittable by a creator and by a compactor ("A compactor
MAY drop it whenever it rewrites the file"). Implementer consequence is real
and visible to a caller: one appender sheds the ancillary the caller wanted
gone, the other retains it, and one of the two is a nonconforming updater
under `[R-CNF-06]`. Needs a maintainer decision, not a wording fix.

### 8. Appendix G leaves tiling and channel layout open — writer-04

Verified the asymmetry. Item 5 pins declared alignment, declared slab and the
filter on the argument that each "change[s] placement"/"changes the stored
bytes of every tile it touches" and none "is implied by content". Tile
extents and channel layout are writer choices in exactly that sense —
§11.3's Note: "Tile extents are a writer's choice, and this specification
imposes none"; §14.4's Note: "A single-channel bool layer does not — ⌈P/8⌉
packed bytes planar versus P bytes interleaved — and both forms are valid" —
and item 2's own rationale names them beside the codec it pins: "two files
carrying the same arrays can legitimately differ in tiling, layout, and
codec." Not byte-level: "It adds no requirement to any actor: a writer
ignoring it is fully conforming", and Appendix G is identified non-normative.
Consequence is confined to profile adopters: two of them, given the same
arrays and the same stated options, emit different files and get non-matching
content-addressed digests with no item to point at. Honest counter a
maintainer may prefer: tiling and layout may be considered part of the
caller's schema rather than the writer's freedom — but so is the codec, and
item 1 pins that. Design decision, one clause in item 5 either way.

### 9. Shape (c)'s Example quantifies over the layer, not the channel — diagrams-01

Verified the mechanism. §3.1: a tile in "a planar layer, one cell of the grid
for one channel"; §14.5 fixes padding content "for each channel the position
carries". So in a planar layer, changing channel b's fill cannot alter
anything §14 fixes for a stored tile of channel f. Step 4's bar quantifies
over "any tile that layer stores", so the commit is permitted; the Example
says "A fill change on a layer that **stores** a tile carrying either is not
an appender's operation at all (step 4)", which bars it. The Example is
correct for interleaved layers and over-general for planar ones. §2.1 decides
which governs ("All text in this document is normative except: ... any text
labeled *Note*, *Example*, or *Rationale*"). Not byte-level — both the
directory-only commit and the over-cautious new-layer/new-file rewrite are
conforming. Cost: a whole-layer duplication an implementer does not owe.

### 10. R8 enumerates containers and not its stated alternatives — diagrams-03, adversary-02

Same defect, two reporters, both disclosing prior exposure to the row label.
The counting argument stands on its own and I re-ran it: 121 rows, 277
instances as the cells read today, matching §21.8. §21.1's discipline is that
an instance names "one of several alternatives the condition text states" and
that members giving "materially different shapes" are enumerated. R8's
condition text states two ("a magnitude whose binary64 interpretation
overflows (`1e400`) and the bare tokens `NaN`, `Infinity` and `-Infinity`
alike") and its cell holds only the two containers, while R1/R5/R6/R7 all
carry their alternatives into their cells. §18.2's bullet distinguishes the
two by mechanism — the bare tokens are what "RFC 8259 does not admit and some
parsers accept regardless" — so a vector for one exercises the finiteness
conversion and a vector for the other exercises token acceptance.

Not byte-level: `[R-VEC-01]` makes the corpus derivative ("where a vector's
recorded expectation and this specification disagree, this specification
governs"), and §21.8 says "A row without a vector is a gap in the corpus, not
a licence to skip the check", so every reader's obligation is identical under
both readings. What moves is §21.8's normative instance total (277 → 279 at
four instances) and two corpus files.

One thing neither reporter weighed, and a maintainer should: a bare `NaN`
also exhibits R7's "not well-formed JSON" instance, and §21.1's specialization
list ("F1 of F6 and of F8, F35 of F36, L24 of L25") does not include R8 of R7.
If the bare tokens are enumerated as an R8 instance, the specialization
question wants an answer at the same time; `[R-VEC-02]`'s non-isolable clause
covers the vector either way.

### 11. §4.7's Note about §7.2 folding ranges into Field cells — diagrams-04

Verified §7.2's table: columns Offset | Size | Type | Field | Class, five
fields, and only `type (0 invalid)` and the flags cell carry a range;
`inline_length`, `extent_offset`, `extent_length` carry none. The Note is
non-normative (§2.1) and the ranges are stated normatively two paragraphs
below and in `[R-ENC-03]`, `[R-CNT-12]`, `[R-CNT-13]`. The reporter's stated
consequence ("shipping a parser that does not enforce F30, F31, F32, L15,
L16, L17") overstates it — the very next paragraph of §7.2 states the extent
slot rules in full — and the reporter says as much. Editorial.

### 12. §20.3's shrink sentence over-generalizes — diagrams-05

Verified with rank 1, T = 4, E 12 → 10: G = ⌈12/4⌉ = ⌈10/4⌉ = 3, no tile
de-addressed, entry_count unchanged, so "the de-addressed tiles' extents
become slack ..., `[R-CNT-17]` obliges the smaller entry_count and so a
re-emitted index region" asserts three things of every permitted shrink, two
of which hold only where a grid count falls. This one *is* normative text
(§20.3 body, not a Note), unlike the parallel §11.1 Rationale of group 6, so
the sentence is a normative over-statement rather than a stray gloss. What
decides it is step 4's own earlier rule:

> "Every layer whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full"

— index content unchanged here, so no re-emission is owed and the "obliges"
is wrong for this case. Not byte-level: re-emitting an unchanged index region
at a new placement is conforming and not re-emitting it is conforming, and
L21 checks entry_count against the geometry either way. Cost: an appender
that re-emits a 20 MB index region it did not owe, or worse, refuses a
permitted shrink because it reads "obliges the smaller entry_count" as a
precondition.

### 13. §9.6 cites F8 and F17 where §9.5 gives three grounds — register-02

Verified both. §9.5's Note: "the magic, the CRC, or committed_file_length
against the transport size, each of which §21.2 already registers" = F8, F14,
F17. §9.6: "(§21.2 rows F8 and F17)". F14 is omitted and is the reachable
case §9.6 itself raises two sentences later (a payload byte string mimicking
a trailer). All three rows share detector, detection point and outcome, so
nothing behavioural turns on it. Editorial/bookkeeping.

### 14. §21.9's "Two do not" provenance count — register-03

Verified against the paragraph's own list. The four categories are "a field's
width, an external format, or the value domain, and the rest from arithmetic
over structures a generation cannot omit". A and A_slab are u64 (§7.4), so no
field width forces power-of-two form; no external format does; `[R-ENC-03]`
bounds magnitude and says nothing about form; and it is not arithmetic over
an unomittable structure. So power-of-two-ness is chosen here, twice, and
"Two do not" is short by one or two. For A_slab it is the only substantive
constraint — its floor of 1 is 2⁰ and its ceiling is the largest power of two
in the domain. Not byte-level: §16.1, §16.2 and §7.4's table independently
require the form, so L39/L29 are unchanged. Cost falls on a reader working
out which numbers a future major could move.

### 15. `[R-CNF-03]`'s acceptance duty lacks a *top-level* qualifier — adversary-03

Verified. §2.3's clause reads "carrying no record of a type it does not
implement with MUST_UNDERSTAND = 1" with no scope qualifier, and §7.4 makes
sub-records records. Two passages foreclose the literal reading:

> `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
> where the file is otherwise conforming a reader MUST NOT reject the file
> for it"

> §21.6: "The qualifier is load-bearing — the same type as a layer sub-record
> is reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so
> only the top-level case is a file a reader refuses."

A specific MUST NOT beats the omission of a qualifier in a definition, and
the file in the construction is "otherwise conforming" (§21.6 makes an
experimental-range MU = 1 sub-record conforming), so the MUST NOT bites. Not
byte-level — no conforming reader may actually refuse. But note what the
divergence would look like if it were open: reader X opens the file, lists
both layers, serves A and rejects B; reader Y refuses the whole file. That is
an accept/reject fork, and the only thing standing between the document and
it is `[R-CNT-18]`'s clause. Adding "top-level" to §2.3 is a one-word repair
worth making for exactly that reason.

### 16. L41's "that tile's length" — quiz-02

Verified. Reading B (the current tile's length) makes the condition
offset(k) ≠ offset(prev) + length(k), which no run of two differently sized
stored tiles satisfies and which would register almost every conforming
slab-declared layer. The rule decides it:

> `[R-SLB-03]`: "the run's stored tiles are contiguous and packed in ordinal
> order — each stored tile's offset equals the previous stored tile's offset
> plus its length"

plus §16.2's Example ("run 1's stored tiles are 8, 9, 11…15, packed with no
gap where 10 would have been") and §21.1's "where a row and the rule it cites
diverge, **the rule governs**". Not byte-level. But the consequence if a
verifier author works from the row alone is severe — mass false rejections —
and the repair is three words ("plus that previous tile's length"), so this
is the cheapest high-value edit in the batch.

### 17. §20.5 names F36 and L25 where the MU = 1 case is F35 and L24 — quiz-03

Verified against §21.1 ("F35 of F36, L24 of L25 ... a file exhibiting a
specialization is recorded against the narrower row") and §21.6's complete
four-row statement. The citation is right for the MU = 0 half and incomplete
for the other. Nothing behavioural: the file is nonconforming either way and
the reader's outcome is fixed by `[R-CNT-15]`/`[R-CNT-18]`. I re-checked the
seven-space enumeration beside it (L31, L33, L34, L36, L43, L45, R1) and did
not find a problem with it. Bookkeeping.

## Coverage

21 input ids, 17 groups, each id in exactly one group, counted:
3 + 1 + 1 + 1 + 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 21.

Byte-level survivors: 0.
