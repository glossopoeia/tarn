# Triage pass — correctness lens — cleanroom round 32

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only.
Sections opened by line range: §2.1–§2.5, §3.1, §4.2–§4.3, §5.1, §5.2, §7.1–§7.4,
§9.2, §9.7, §10.4, §11.1–§11.4, §13.3, §14.5, §15.3–§15.4, §16.1–§16.2, §18.2,
§19.1–§19.2, §20.3, §20.4, §20.5, §21.1–§21.7, §24, Appendix F, Appendix H.
Ran: `wc -l`, `grep -n` for headings and requirement ids, and one `python3` check of
the binary64 overflow boundary arithmetic.

Did NOT read: any walk transcript, any other triage pass's notes, `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `spec/registry.json`, git history, the web. No directory
listing of the round output directory was run.

## Method

For each finding: (1) locate the quoted text in the file and check the quotation is
accurate and in context; (2) check the cited section says what the reporter says;
(3) ask whether the claimed second reading survives the surrounding words; (4) apply
the byte-level test and, where downgrading, find and quote the deciding sentence.

## Text checked (verbatim, with line context)

### §20.3 step 4 — the closed list (L3183-3207)

> A layer that stores a tile **in the generation this commit supersedes** keeps its
> declarations, with these exceptions and no other: its name, and its dimension and
> channel names, MAY change; an extent MAY grow, and MUST NOT shrink; a planar layer's
> channel list MAY be extended at its end, or shortened from its end; and a slab or
> alignment declaration MAY be declared, re-established or cleared as this step provides
> below. A commit MAY make several of these changes at once. Every other declaration is
> fixed for as long as the layer stores a tile: the layout, the linearization and the
> index encoding, the codec and the filter, the rank and the dimension order, every tile
> extent, every channel's type and fill, an interleaved layer's channel list, and the
> position of every planar channel but the last. A commit MUST NOT change one of these;
> the change is a new layer, or a whole-file rewrite under a fresh file_id.

Head-of-step test (L3160-3172):

> Every layer whose stored-tile set or index content this commit changes has its
> tile-index region re-emitted in full — entry_count entries plus the segment CRC
> array — necessarily at a new placement ... entries new to this generation (added
> tiles, grown extents, an appended channel) emitted per §15, and every other entry
> byte-identical at its disk-ordinal position (a growth renumbers ordinals wherever
> `[R-GEO-06]` moves them, and nothing else this step permits moves one).

Bounds paragraph close (L3243-3246):

> The list is not offered as exhaustive: a change is permitted exactly where the
> declarations it produces satisfy every rule they are subject to.

### §13.3 Note (L1941-1949) — quoted accurately by five reporters.

### §2.1 (L107-109)

> All text in this document is normative except: §1 (Introduction); any text labeled
> *Note*, *Example*, or *Rationale*; and appendices identified as non-normative. `[R-CNF-01]`

and (L101-104) BCP 14 keywords bind "when, and only when, they appear in all capitals".

### §21.7 (L3897-3899)

> The obligations of §14.5 and `[R-SER-08]` narrow this only where content is
> structurally constrained: padding positions, pad bits, and boolean bytes.

### §14.5 [R-SER-05] — "a verifier MUST check it, and a violation is a validity error at tile scope."
### §21.4 T4/T5 — both present, Detector *verifier*, Detected *certification*.

### §9.2 [R-LIF-02] step 2 — "append new stored-tile payloads and tile-index regions for
the layers it changes, and any new record extents (file-scope or layer-scope)".

### §3.1 — "**channel** — a named, typed per-sample value of a layer (§12). Channels are
declared in order; a channel's **index** is its 0-based position in that order".

### §19.1 [R-RDR-01] step 4 — "Parse the record sequence under §7.2's framing ... and build
the layer table: each layer record's name, parsed and checked per §4.6".

### §21.1 — "where a row and the rule it cites diverge, **the rule governs**" and, for a
verifier-detected row, "the outcome names the scope at which the damage is recorded, not
an obligation on any reader ... and `[R-MTA-05]`, whose unsorted document readers process
as they find it — F27 and L48".

### Appendix F — "**[IEEE 754]** IEEE 754-2019 — binary16, binary32, and binary64 (§12.1)."
The normative reference is scoped to §12.1's interchange formats. Nothing anywhere in the
file matches /round|nearest|ties/ in the sense of a rounding-direction attribute
(grep run; the only hits are "round trip", "grounds", "ties the vector", "round-trips").

## Grouping

- G1 `note-entry-count-not-sole-index-changer` — reader-01, writer-03, verifier-02,
  adversary-02, quiz-01. All five attack the same parenthetical in §13.3's Note.
- G2 `cnt17-smaller-entry-count-false` — reader-03, writer-04. Both attack the *normative*
  sentence in §20.3's bounds paragraph, a different sentence from G1's.
- G3 `permitted-exactly-where-biconditional` — reader-02, writer-01.
- G4 `channel-list-shorten-extend-composition` — writer-02, verifier-03, adversary-01,
  quiz-03. One construction, one passage: quiz-03's "false justification" is writer-02's
  first "thing that goes wrong", so they are not separable without splitting writer-02.
- G5 `fixed-decl-witness-enumeration-omits-t4-t5` — verifier-01, register-01.
- G6..G19 — singletons, one per remaining finding.

29 ids in, 19 groups, each id once.

## Judgements

### G1 — CONFIRMED, not byte-level

The Note's parenthetical is false twice over, and I checked both counterexamples:

(a) grow + shorten. C=4→2, N=8→16: entry_count = C·N = 32 both times; extent_length =
32·20 + ⌈32/2^16⌉·4 = 644 both times. Both changes are on the permitted side and "A commit
MAY make several of these changes at once" permits them together. [R-GEO-06] makes the disk
ordinal c·N + s, so every ordinal from 8 up is reassigned: index content changes, entry_count
does not. The Note's closed claim is false.

(b) declaring an alignment or slab on a tile-storing layer. §20.3's own close to step 4:
"an aligned layer's stored tiles — every one the new state keeps, not only those this commit
adds — satisfy its invariant or the declaration is cleared", and [R-SLB-04] the same for a
slab. [R-LIF-01] freezes committed bytes, so the writer supersedes each offending tile at a
conforming offset: every entry offset changes, entry_count untouched.

(c) A third, purely textual defect two reporters raise and I verified: entry_count is not
among "the declaration changes §20.3 permits" at all. §20.3 puts it on neither list —
"entry_count and crc_of_crc_array follow the commit, the record's extent slot with them" —
so the Note names as the sole member of a set something that is not a member of it.

Downgrade. The block opens "> **Note — sparse writing.**" and [R-CNF-01] exempts "any text
labeled *Note*" from normativity. The governing rule is keyed to the right quantity and is
unconditional: "Every layer whose stored-tile set or index content this commit changes has
its tile-index region re-emitted in full". Premise my downgrade rests on, stated so it can be
attacked: that a writer implementing §20.3 step 4 applies the head-of-step test rather than
the Note's entry_count test, because the head-of-step test is normative and the Note is not.
If a triager holds that a Note citing [R-WRT-04] as its authority can bind, this becomes
byte-level — and the cost, as reader-01 and quiz-01 both work out, is a *conforming* file
whose reference array is wrong with no owed check able to see it.

### G2 — CONFIRMED, not byte-level

"A channel removed from the end leaves its stored tiles' extents as slack (§5.2), and
`[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region". Under G1's
construction (a) the entry_count is not smaller — it is equal — so [R-CNT-17] obliges
nothing there. This is normative text stating a false arithmetic consequence in a case the
same numbered step expressly permits. It licenses nothing: the obligation it mis-attributes
is stated unconditionally two paragraphs above, and [R-CNT-17] itself states the obligation
without the word "smaller" ("an entry_count that does not equal the geometry-derived
addressed-tile count ... is a validity error at layer scope"). writer-04's companion point —
that "leaves its stored tiles' extents as slack" also fails under G4's composition — is
correct and belongs with the same repair.

### G3 — PARTIAL, not byte-level

The sentence is loosely quantified: the paragraph opens "A permitted change holds provided
..." and the sentence then says "a change is permitted exactly where ...", a biconditional
over changes at large. Real defect. But reading (B) is not permitted by the words, for two
reasons neither reporter put first. First, "The list is not offered as exhaustive" follows a
colon-list of exactly four bounds; reading "the list" as the permitted list makes the sentence
contradict its own paragraph. Second and decisive:

> A commit MUST NOT change one of these; the change is a new layer, or a whole-file
> rewrite under a fresh file_id (`[R-LIF-01]`, §20.5).

§2.1 binds BCP 14 keywords "when, and only when, they appear in all capitals". A lowercase
"a change is permitted" cannot lift an all-capitals MUST NOT stated one paragraph above,
alongside "with these exceptions and no other". Premise: that a reader reads the paragraph
in the order it is written. Repair is one word — "a permitted change is permitted exactly
where ..." — or naming the list.

### G4 — CONFIRMED, **BYTE-LEVEL**

Checked every closing route the reporters name, and one they do not.

The fixed side freezes "the position of every planar channel but the last" — affirmatively
leaving the last position unfrozen; that carve-out does nothing unless the last position's
occupant may change. The reconciliation sentence hands the channel list wholly to the
permitted side: "where a field is on both sides — a dimension extent, a planar layer's
channel list — the permitted side states the whole of what a commit MAY do to it". And
"A commit MAY make several of these changes at once" must reach *within* a bullet, because
[R-CNT-16] makes per-tile alignment and a slab mutually exclusive (§16.2: "mutually exclusive
with per-tile alignment, `[R-CNT-16]`"), so switching between them requires both a clear and
a declare, and both live in the fourth bullet.

Does "every channel's type and fill" close it? Only under a positional individuation of
channels. §3.1 individuates a channel as "a named, typed per-sample value of a layer" whose
*index* is a positional attribute — so on the composite commit no surviving channel's type
changed: one channel left, another arrived.

Does the tense sentence close it? It closes only the empty-then-redeclare route: "unstoring
or superseding every tile of a layer and re-declaring it is one operation, and it is a
rewrite". It supplies a net-effect *principle* and does not extend it to the channel list.

The sentence I looked for and did not find: any words making the two channel-list
alternatives exclusive within one commit — a "net effect", an "exactly one of", or the tense
sentence's principle carried over to a shorten-and-extend. There is none.

Two corrections to the reporters. (i) writer-02's category-3-versus-category-4 fork is
**refuted**: the re-emission clause's parenthetical names "an appended channel" among
"entries new to this generation", so the appended channel's entries are emitted per §15 and
do not fall to the catch-all "every other entry byte-identical at its disk-ordinal position".
quiz-03 has this right. (ii) quiz-03 is right that the principle paragraph's justification —
"an appended planar channel adds tiles at ordinals after every existing one, a disk ordinal
being c · N + s" — is simply false for the composite, since N is unchanged and the appended
channel takes the removed channel's ordinals [(C−1)N, CN).

Byte-level. Given one input file and one caller request, updater P (composition permitted)
appends a commit; updater Q (composition forbidden) must instead perform a whole-file rewrite
under a fresh file_id. Both outputs are conforming files. **The premise I am resting on, and
the one a refuter should attack**: that the byte-level test — "which byte sequences a
conforming implementation may emit" — is quantified per input over the conforming *updater*
class, not only over the set of conforming files. verifier-03 and quiz-02 both take the
contrary premise (a creator can emit P's output either way, so the set of conforming files
does not move) and downgrade on it. I do not, because §20.3 step 4 is a rule about what an
updater may emit from a given input, its harm is stated in exactly those terms ("Under new
ones the same bytes would denote values, coordinates or padding the writer did not store"),
and a rule whose two readings differ on whether an actor may append 44 bytes or must rewrite
the file has moved the bytes for that actor. A false negative here ships an ambiguous
specification; a false positive costs one re-read.

### G5 — CONFIRMED, not byte-level

§20.3: "but for a decoded size or a boolean byte the register witnesses (T3, T14, T2), no
check any actor owes able to see it (§21.7)". §21.7 — the section that sentence cites —
states three classes, not two: "padding positions, pad bits, and boolean bytes". T4 and T5
are registered, Detector *verifier*, and [R-SER-05] states the duty unconditionally ("a
verifier MUST check it"). A fill change on a layer with padding positions is caught by T4
cold; a packed planar bool plane's pad bits by T5. The enumeration is incomplete and
disagrees with the section it cites.

Downgrade quote: [R-SER-05] — "a verifier MUST check it, and a violation is a validity error
at tile scope" — and §21.1 — "where a row and the rule it cites diverge, **the rule
governs**". The complained-of clause grants no permission and states no condition a file can
exhibit; it is an assertion about detectability. Both readings reject the same files. Premise:
that T4 and T5 stand on [R-SER-05] and §21.4 independently of §20.3's account of them.

### G6 — CONFIRMED, not byte-level
§5.1's Example: "a commit that touches no layer re-emits the directory, the pad and the
trailer alone." [R-CNT-25]: "Each user-metadata record carries its document in its extent —
never inline". [R-LIF-02] step 2: a commit appends "any new record extents (file-scope or
layer-scope)". §20.3's shape (c) says so directly: "Editing user metadata is not this shape:
its document lives in an extent (`[R-CNT-25]`), so a new extent is appended and the old one
becomes slack, as in (b)." §5.1 is wrong as written. Both passages are labelled *Example*,
non-normative under [R-CNF-01]; [R-LIF-02] governs and is unambiguous.

### G7 — CONFIRMED, not byte-level
Appendix H's reader entry keeps one of [R-CNF-03]'s three qualifiers. §21.6's closing
paragraph names a conforming file a conforming reader must refuse ("an experimental-range
top-level record type carrying MU = 1 ... `[R-CNT-15]` obliges the reader to reject, and
`[R-CNF-02]` makes the file conforming all the same"). The appendix is headed
"(non-normative)" and says "each entry's authority is the requirement or section cited,
never this summary".

### G8 — CONFIRMED, not byte-level
[R-WRT-05] has two conditions — "every record it retains **and does not logically modify**"
— and §20.4's table preamble keeps them apart ("The table states what an updater owes a
record it does not logically modify"). Appendix H's "re-emits every retained record
byte-identically" drops the second, contradicting the clause five lines above it in the same
entry, which permits an updater to change a layer's names and grow an extent. It also loses
[R-WRT-05]'s second half, that a modified record is new output under writer obligations.

### G9 — CONFIRMED, not byte-level
Step 4: "subject to every rule its new **declarations** are subject to". Shape (c): "subject
to every rule its new **geometry** is subject to, which is the same step's permission".
§11.1's Rationale: no qualifier at all. This document uses *geometry* narrowly — §11.1 is
headed "Geometry and its validity floor"; §10.4 lists "sample types, geometry, channel sets
and layout, codecs, filters, linearization, fill, and index location or encoding" as distinct
things. Three statements, three qualifiers, one of them step 4's.

### G10 — PARTIAL, not byte-level, figure
The prime is genuinely undefined between the caption's two conjuncts ("extent slots are
re-pointed **and** each index region any of whose stored extents moved is regenerated — the ′
marks"). But the claim that `A: index′` is *wrong* is not established: the figure draws A's
tiles as one box, and a compactor "is free to place structures anywhere §5.2 admits", so
nothing in the drawing says A's individual stored extents did not move within that box, and
"Regions, not offsets" disclaims the offsets that would settle it. Real defect: the mark
carries no legend. Repair: give the ′ a one-clause legend.

### G11 — CONFIRMED, register-bookkeeping
[R-CNT-18] names three: "any overrun, truncation, or residue". L14's Instances keep three
("sub-record header; sub-record inline_length; trailing residue"); its Condition keeps two.
F29 states all three at file scope. §21.1's instance arithmetic is mechanical from the cell,
so the count is unaffected; the corpus builder for the third instance must go to the rule.

### G12 — CONFIRMED, register-bookkeeping
L2 and T12 carry "although every contributing field is in domain" / "although each field
alone is in domain"; F3 does not. Without it F3 is entailed by F2 on dir_offset, and §21.1's
specialization rule then records the file against F2 — which the row does not say where its
siblings do. "so the sum wraps" adds a condition [R-ENC-04] does not state; [R-ENC-04] is an
"exceed 2⁶³ − 1" test and separately bars acting on "a wrapped or truncated value".

### G13 — CONFIRMED, not byte-level
§21.6: "What belongs here is the reader's side of them, and it is unchanged: neither is a
reason for a reader to reject anything." Against [R-CNF-12]: "For a nonconforming file no
acceptance obligation exists — a reader MAY reject it upon detecting any violation, including
violations whose assigned detector is the verifier." The reader's side is precisely what the
reclassification changed: the licence now attaches. The document makes the qualification
elsewhere, in [R-CNT-18]: "where the file is otherwise conforming a reader MUST NOT reject
the file for it — on a nonconforming file `[R-CNF-12]`'s licence to reject on any detected
violation is untouched". Downgrade: an all-capitals MAY is not bounded by a lowercase "is a
reason" (§2.1), and the file is nonconforming under both readings ([R-MTA-05]: "the file is
nonconforming, a verifier MUST report it").

### G14 — CONFIRMED, not byte-level
"Application metadata never invalidates the structural data it annotates" carries no scope
word, while [R-MTA-05] says "the file is nonconforming, a verifier MUST report it" and F27 /
L48 record the damage at file and layer scope. Downgrade quote, from §21.1: "For a row whose
Detector is *verifier*, the outcome names the scope at which the damage is recorded, not an
obligation on any reader ... and `[R-MTA-05]`, whose unsorted document readers process as
they find it — F27 and L48." That decides the sentence toward the reader-facing sense. The
defect is the missing scope word, not an open verdict.

### G15 — PARTIAL, not byte-level
The reporter's premise — "nothing requires a conforming reader or updater to implement the
registered record types" — is refuted by [R-RDR-01] step 4, which obliges every conforming
reader to "Parse the record sequence under §7.2's framing ... and build the layer table: each
layer record's name, parsed and checked per §4.6", and to apply "the framing rules a top-level
user-metadata record carries". A reader that does not implement 0x0001 or 0x0002 cannot
complete the open. What survives is narrower and real: [R-CNF-03]'s no-subset enumeration
does not list the registered record types, so its em-dash gloss and §20.4's "an updater
implements both registered types" rest on a requirement stated in another section rather than
in the sentence that needs it.

### G16 — CONFIRMED, **BYTE-LEVEL**
§18.2 [R-MTA-04]: "A reader interprets every JSON number as an IEEE 754 binary64 value ... A
document is unreadable if it contains a number whose binary64 interpretation is not finite —
which covers a magnitude that overflows on conversion". Whether a magnitude overflows on
conversion is rounding-attribute dependent at the boundary, and the document names no
attribute. I verified the arithmetic: DBL_MAX = 2^1024 − 2^971, the midpoint to 2^1024 is
2^1024 − 2^970 (a 309-digit integer), Python's float() of its decimal expansion returns inf.
Under roundTiesToEven that literal overflows and the document is unreadable (R8, Detector
*reader*); under roundTowardZero the rounded result with unbounded exponent is DBL_MAX
exactly, so no overflow is signalled and the interpretation is finite.

The sentence I looked for and did not find: any words naming a rounding-direction attribute,
or saying "correctly rounded to nearest, ties to even", for decimal-to-binary64 conversion.
`grep -i "round|nearest|ties"` over the whole file returns only "round trip", "grounds" and
"ties the vector". The nearest thing to a decider is IEEE 754-2019's own default attribute —
but Appendix F scopes the normative reference as "**[IEEE 754]** IEEE 754-2019 — binary16,
binary32, and binary64 (**§12.1**)", to the interchange formats, not to §18.2's conversion.
I cannot quote a sentence that decides it, so I do not downgrade it.

Consequence: one file, two verifiers. R8's Detector is *reader*, its outcome ignore-record,
and §21.5 says "Every row here is a violation all the same". So verifier A reports
*nonconforming* and verifier B certifies, and [R-CNF-05] bars a conforming writer from
emitting that literal under A's reading and not under B's. The window is half an ULP wide at
the top of the binary64 range, which is small; it is not empty, and [R-VEC-03] asks the corpus
for a vector at every boundary value.

Repair (a maintainer's choice, not an edit I can make alone): name the attribute —
"correctly rounded under roundTiesToEven" — or restate the test as the one that is
attribute-independent, e.g. "a magnitude greater than or equal to 2^1024".

### G17 — PARTIAL, not byte-level
The phenomenon is real and accurately described: [R-WRT-07] keys regeneration to relocation,
placement is free ("it is free to place structures anywhere §5.2 admits"), and §20.5 itself
concedes the bound — "That `[R-WRT-09]`'s checks reach the index chain and each stored tile's
entry crc rather than an entry's own value domain bounds how far a compactor goes looking".
So whether a compactor meets a structurally malformed entry turns on a free packing choice.
But the reporter's own closure fails: §15.3 says a structural entry "contributes no stored
extent ... and none to `[R-LIF-08]`'s coverage walk", so there is no stored tile there and
[R-WRT-09]'s "every stored tile's entry crc" — universal reading and all — does not reach it.
The real defect is that §20.5's refusal trigger is placement-contingent and the document does
not say so. Not byte-level: it needs a nonconforming input, and [R-WRT-01] already provides
that "a violation latent in a structure it carries forward verbatim travels into its output".

### G18 — REFUTED
Reading B is not available. The permitted side lists "its name, and its dimension and channel
names, MAY change", unqualified by layout, as one of the exceptions. The fixed side is
introduced as "**Every other** declaration is fixed" — other than the exceptions just listed.
Channel names are on the exceptions list, so they are not among "every other declaration",
and "an interleaved layer's channel list" cannot reach them. Three further supports the
reporter found are sound: "every channel's type and fill" would be redundant if "channel
list" covered every per-channel field; "the position of every planar channel but the last"
shows "channel list" is being used for membership and position; and the tie-break enumerates
the both-sides fields ("a dimension extent, a planar layer's channel list") without naming
channel names. No repair needed.

### G19 — PARTIAL, not byte-level
Accurate that §5.2's enumeration of incompleteness grounds carries no structural-entry
carve-out. Inaccurate that "only §9.7's closing sentence settles it": §15.3 settles it too —
a structural entry "contributes no stored extent to the *verifier* rows ... and none to
`[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that no other claimant
claims fall to slack" — and §5.2's own clause is conditional, "where a scope-level rejection
**ends that scope's enumeration**", which does not fire for an entry §9.7 says "the walk
passes over". Repair is a cross-reference at §5.2, not a rule change.

## Counts

29 input ids, 19 groups, union of member_ids = the input list exactly, no duplicates.
Byte-level upheld: 2 (G4, G16). Byte-level flagged by reporters: 4 (writer-01, writer-02,
adversary-01, adversary-04) — of which writer-02 and adversary-01 fall in G4 (upheld),
adversary-04 is G16 (upheld), and writer-01 is G3 (downgraded, with the deciding MUST NOT
quoted).
