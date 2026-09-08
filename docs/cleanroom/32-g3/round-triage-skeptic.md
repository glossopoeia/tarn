# Triage pass — Skeptic lens — cleanroom round 32

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in
  chunks: §1–§4.7 (lines 1–400 and 450–500), §5.1–§5.2 (629–768), §7.1–§7.4
  (948–1195), §9.1–§9.3 (1240–1340), §9.7 (1469–1523), §11.1–§11.4
  (1618–1740), §13.3–§14.1 (1903–1962), §14.5–§15.4 (2119–2240), §18.2
  (2611–2800), §19.1–§19.4 (2872–2995), §20.3–§20.5 (3114–3560), §21.1–§21.9
  (3562–3951), Appendix H (4672–4754). Plus one grep for section headers and
  one grep for `754|round`.
- **No** walk transcript. **No** other triage pass's notes. **No** directory
  listing of any kind — I opened only the one file, by name. No `docs/`,
  `PLAN.md`, `AGENTS.md`, `conformance/`, `registry.json`, git history, web.

## Method

For each finding I looked for the sentence that forecloses it, and quoted it
where I found one. Where I could not find one I say so and grade accordingly.

---

## Grouping

19 groups over 29 ids. Each id in exactly one group.

| Group | Members |
|---|---|
| note-sparse-writing-overclaims | reader-01, writer-03, verifier-02, adversary-02, quiz-01 |
| bounds-paragraph-unscoped-biconditional | reader-02, writer-01 |
| cnt17-smaller-entry-count-false | reader-03, writer-04 |
| planar-channel-list-composition | writer-02, verifier-03, adversary-01, quiz-03 |
| fixed-decl-witness-omits-t4-t5 | verifier-01, register-01 |
| anatomy-figure-omits-record-extents | diagrams-01 |
| apph-reader-accept-duty-truncated | diagrams-02 |
| apph-updater-reemit-condition-dropped | diagrams-03 |
| empty-layer-redeclare-qualifier-drift | diagrams-04 |
| compaction-figure-prime-undefined | diagrams-05 |
| l14-condition-drops-residue | diagrams-06 |
| f3-missing-in-domain-qualifier | diagrams-07 |
| s216-closing-overstates-reader-side | register-02 |
| cnt25-never-invalidates-unscoped | register-03 |
| registered-record-type-implementation-premise | adversary-03 |
| binary64-rounding-direction-unnamed | adversary-04 |
| compactor-refusal-vs-placement | adversary-05 |
| interleaved-channel-rename | quiz-02 |
| walk-incompleteness-carveout-only-in-97 | quiz-04 |

---

## Group-by-group

### 1. note-sparse-writing-overclaims (5 members) — CONFIRMED, not byte-level

Text at 1941–1949, verified verbatim:

> **Note — sparse writing.** … each commit that changes a layer's stored-tile
> set or its index content — which, among the declaration changes §20.3
> permits a layer that stores a tile, only a change to entry_count does —
> re-emits that layer's whole tile-index region

The parenthetical is false at least twice, and I checked both counterexamples
against the text rather than the reporters' accounts:

1. **Growth ∧ shortening.** §20.3 step 4 (3182–3185): "an extent MAY grow…; a
   planar layer's channel list MAY be extended at its end, or shortened from
   its end… A commit MAY make several of these changes at once." With C·N
   held constant (reader-01: C 4→2, N 8→16; quiz-01: C 4→2, N 3→6;
   adversary-02: C 3→2, N 4→6) entry_count and extent_length are unchanged
   while every disk ordinal moves, because [R-GEO-06] (1728–1731) makes the
   planar disk ordinal c·N + s. Index content changes; entry_count does not.
2. **A slab or alignment declaration.** §20.3 step 4 closing (3262–3266): "a
   slab declaration is re-established or cleared (`[R-SLB-04]`), and an
   aligned layer's stored tiles — every one the new state keeps, not only
   those this commit adds — satisfy its invariant or the declaration is
   cleared". With [R-LIF-01] freezing committed bytes, satisfying a new A
   means superseding tiles at conforming offsets: entry offsets change,
   entry_count does not.

The third, textual, point is also right: §20.3 puts entry_count on neither
list — "entry_count and crc_of_crc_array follow the commit" (3197) — so the
Note names as the sole member of a set something that is not a member.

**Why not byte-level.** The block opens `> **Note — sparse writing.**` and
[R-CNF-01] (107) says "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". The rule
it glosses is unconditional and keyed to the right quantity, at the head of
the very step it cites (3162–3164): "Every layer whose stored-tile set or
index content this commit changes has its tile-index region re-emitted in
full — entry_count entries plus the segment CRC array — necessarily at a new
placement". A writer following the requirement rather than the gloss diverges
from no other writer. **Premise of the downgrade, stated so it can be
attacked:** that [R-CNF-01]'s exemption for *Note*-labelled text is complete —
i.e. that a Note citing `[R-WRT-04]` as its authority still binds nothing.
All five reporters reached the same conclusion independently.

Repair: delete the parenthetical, or replace it with §11.1's Rationale's
correct and narrower claim ("Growth that leaves **entry_count** unchanged
touches the directory alone", 1649).

### 2. bounds-paragraph-unscoped-biconditional (2) — CONFIRMED, not byte-level

Text at 3247–3249: "The list is not offered as exhaustive: a change is
permitted exactly where the declarations it produces satisfy every rule they
are subject to."

The looseness is real: the paragraph opens "A permitted change holds provided
…" (3240) but the closing sentence says "a change", and "exactly where" is a
biconditional. Under the unscoped reading a re-type or a fill change on a
tile-storing layer becomes an appender's operation.

**The sentence that forecloses it** — and this is the one I went looking for
and found — is three sentences earlier in the same paragraph block (3230–3238):

> What the line gives up is stated rather than carved around: a shrink, a fill
> change, a re-type, a re-tiling, a transposition of the dimensions, a change
> of rank, layout, linearization, index encoding, codec or filter, any change
> to an interleaved layer's channel list, and a planar channel inserted or
> removed anywhere but the end of the list are rewrites **even where a
> particular file would survive them in place, because deciding which files
> would is the edge this list exists to remove**.

That names the exact changes the unscoped reading would license and says they
are rewrites *regardless of whether the produced declarations are legal* —
which is precisely the unscoped criterion. Reinforced by 3180 ("with these
exceptions and no other"), 3191 ("A commit MUST NOT change one of these"),
§2.1's casing rule (99–103) under which a lowercase "is permitted" cannot
bound an all-capitals MUST NOT, and shape (c) at 3331–3334 ("A change to any
fixed declaration of a layer that **stored** a tile … — a fill value, a type,
a tile extent — is not an appender's operation at all (step 4)").

**Premise:** that "The list" takes its nearest antecedent (the four bounds at
3242–3247) and not the permission list two paragraphs up. Someone attacking
this would argue the biconditional supplies a *sufficient* condition that
displaces the list; the answer is that a non-capitalised sufficient condition
cannot displace a capitalised prohibition inside the same requirement.

Repair: "a **permitted** change is permitted exactly where…", or name the
list: "The list of bounds is not offered as exhaustive".

### 3. cnt17-smaller-entry-count-false (2) — CONFIRMED, not byte-level

Text at 3250–3252: "A channel removed from the end leaves its stored tiles'
extents as slack (§5.2), and `[R-CNT-17]` obliges the smaller entry_count and
so a re-emitted index region".

Normative text, and false where the same commit also grows an extent — which
the same step expressly permits three sentences earlier. In reader-03's
construction entry_count is unchanged at 32 and extent_length unchanged at
644, so [R-CNT-17] obliges nothing. The re-emission is still owed, by the
head-of-step test, not by this route.

**Not byte-level**, and here is the deciding text: [R-CNT-17] itself (3121–3126)
states the obligation without the word "smaller" — "an entry_count that does
not equal the geometry-derived addressed-tile count, is a validity error at
layer scope" — and §7.4's table row says entry_count "equals the
addressed-tile count (§11.2, `[R-CNT-17]`)". A writer that computes
entry_count by re-deriving C·N is right; one that decrements emits L21/L22,
which [R-CNF-05] bars. And the re-emission the sentence's consequent asserts
is owed anyway under 3162–3164. **Premise:** that a mis-stated *mechanism* in
normative prose licenses nothing where the obligation it mis-attributes is
stated unconditionally two paragraphs above.

Repair: "…and `[R-CNT-17]` obliges an entry_count re-derived from the new
declarations, and the ordinal renumbering re-emits the index region".

### 4. planar-channel-list-composition (4) — CONFIRMED, **BYTE-LEVEL**

This is the group I tried hardest to kill and could not.

The question: may one commit both shorten a planar channel list from its end
and extend it at its end, so that the net C is unchanged and the channel at
index C−1 carries a different name, type and fill?

**Reading A (permitted).** 3182–3185: "a planar layer's channel list MAY be
extended at its end, or shortened from its end… A commit MAY make several of
these changes at once." 3193–3196: "where a field is on both sides — a
dimension extent, **a planar layer's channel list** — the permitted side
states the whole of what a commit MAY do to it." §7.4's channel field is a
single row ("C channel entries | name … type … fill"), so on this reading the
tie-break hands names, types and fills of a planar layer's channels wholly to
the permitted side, and the composition is two of "these changes" at once.

**Reading B (forbidden).** The fixed list (3186–3191) includes "every
channel's type and fill" with no planar/interleaved qualifier, while carefully
qualifying its neighbours ("an interleaved layer's channel list", "the
position of every planar channel **but the last**"). If the tie-break
displaced the fixed side's channel items for planar layers, "every channel's
type and fill" would do no work at all for planar layers and would be
redundant for interleaved ones, which "an interleaved layer's channel list"
already covers. And the permitted side's "its dimension and **channel names**
MAY change" presupposes that a channel has identity across generations by its
position (§3.1: "a channel's index is its 0-based position in that order") —
otherwise a rename is indistinguishable from a removal plus an addition.
Under that ontology the composition changes the type declared at index C−1,
which "A commit MUST NOT change one of these" forbids.

**Sentences I looked for and did not find.** Either of these would settle it,
and neither is in the document:

- a sentence saying that the two channel-list alternatives may not be
  composed in one commit — i.e. that the net effect on the list must be an
  extension or a shortening;
- a sentence fixing the type and fill declared at **every planar channel
  position that exists in both generations**, which is the quantifier the
  question turns on.

I also checked and rejected four candidate closers:

1. The tense sentence (3199–3203) closes only the empty-then-redeclare route.
2. [R-GEO-01]'s floor of one channel bites only at net C = 0.
3. The principle paragraph's "an appended planar channel adds tiles at
   ordinals after every existing one" (3224–3226) is *falsified* by the
   composition rather than forbidding it — the appended channel's ordinals
   are exactly the removed channel's. quiz-03, writer-02, verifier-03 and
   adversary-01 all found this independently; it is a false premise inside
   the justification of a permission, which is the reverse of a closer.
4. The re-emission clause **does** settle the *entry disposition*, against
   writer-02: 3167–3169 puts "entries new to this generation (added tiles,
   grown extents, **an appended channel**) emitted per §15" ahead of the
   residual "every other entry byte-identical at its disk-ordinal position".
   An appended channel's entries fall in the named class, not the catch-all.
   So writer-02's category-3/category-4 fork is refuted; his construction's
   *harm* is not reachable that way.

I also found a partial mitigation the reporters did not raise: [R-LIF-02]
step 2 (1252–1255) says a commit "**append**[s] new stored-tile payloads",
and §20.3 step 4 repeats "writing begins at exactly F; new stored tiles and
record extents follow". So an appended channel's newly stored tiles must lie
at ≥ F, which bars adversary-01's construction of pointing the new channel's
entry at the superseded channel's bytes — and bars his two-commit
"counterweight" as well. That removes the *silent reinterpretation* harm but
does **not** remove the fork.

**Why byte-level, notwithstanding verifier-03's and quiz-02's argument.**
Their argument is that the disputed output X is a conforming file a *creator*
could emit byte-for-byte (slack content is unconstrained, [R-CNT-03]; a
pre-trailer gap longer than the pad is a conduct rule per §2.3), so the set
of conforming files does not move and no verifier verdict moves. I accept
all of that. What still moves is the set of byte sequences a conforming
*updater* may emit from a given input: under A it appends a small commit
(payloads for the new channel if any, an 84-byte index region, a directory, a
pad, a 64-byte trailer); under B it MUST instead emit a whole-file rewrite
under a fresh file_id, which shares essentially no bytes and specifically not
file_id. §20.3 step 4 is the requirement that governs exactly that pair, and
it is not among the writer-conduct rules §2.3 declares ("§6.3's flags rules …
and §6.2's pre-trailer gap … are the cases this text states"). A rule that
binds an updater's output and is not declared conduct binds bytes.

Repair (a maintainer decision, not an edit I can choose): either add to the
permitted side that a commit combining the two alternatives on one channel
list is a rewrite, or qualify the fixed side's "every channel's type and
fill" to say what it means at a position occupied by a different channel in
the two generations. Whichever is chosen, the principle paragraph's "adds
tiles at ordinals after every existing one" must be corrected too.

### 5. fixed-decl-witness-omits-t4-t5 (2) — CONFIRMED, not byte-level

3215–3219: "…but for a decoded size or a boolean byte the register witnesses
(T3, T14, T2), no check any actor owes able to see it (§21.7)."

§21.7, the section the sentence cites, states three classes, not two
(3897–3899): "The obligations of §14.5 and `[R-SER-08]` narrow this only
where content is structurally constrained: **padding positions, pad bits, and
boolean bytes**." T4 (3772) and T5 (3773) register exactly the two the
sentence drops, with detector *verifier*, and [R-SER-05] (2127–2130) states
the duty unconditionally: "a verifier MUST check it". Both worked witnesses
(a fill change over an edge tile's padding; a packed-bool plane's pad bits)
check out against §14.5 and §11.3.

**Not byte-level.** The sentence grants no permission and states no condition
a file can exhibit; it is an assertion about detectability inside a
justification. T4/T5 stand on [R-SER-05] and §21.1's "where a row and the rule
it cites diverge, the rule governs" (3582–3583). **Premise:** that a false
assertion about the *state of the checks* cannot change any check, because
the checks are stated elsewhere unconditionally.

Repair: "(T3, T14, T2, T4, T5)", or drop the enumeration and cite §21.7's
three-item narrowing.

### 6. anatomy-figure-omits-record-extents (diagrams-01) — CONFIRMED, not byte-level

§5.1 Example, 676–679: "so a commit that touches no layer re-emits the
directory, the pad and the trailer alone." [R-LIF-02] step 2 (1253–1255)
governs: "append new stored-tile payloads and tile-index regions for the
layers it changes, **and any new record extents (file-scope or
layer-scope)**". [R-CNT-25] (958–961) forces a user-metadata document into an
extent, and §20.3's own figure says so at 3338–3341: "Editing user metadata is
not this shape: its document lives in an extent (`[R-CNT-25]`), so a new
extent is appended". §5.1 is wrong as written; the two figures contradict.

Both are *Example* blocks, non-normative under [R-CNF-01], and [R-LIF-02] is
unambiguous. Repair: "a commit that touches no layer and adds no record
extent".

### 7. apph-reader-accept-duty-truncated (diagrams-02) — CONFIRMED, not byte-level

Appendix H reader entry: "accepts every conforming file within §21.9's
minimum guarantees". [R-CNF-03] (178–188) carries three qualifiers, of which
the checklist keeps one; §21.6 (3866–3878) names the file the checklist would
mis-grade: "an **experimental-range top-level record type carrying MU = 1**
… `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file
conforming all the same."

Appendix H is headed "(non-normative)" and subordinates itself: "each entry's
authority is the requirement or section cited, never this summary". The same
appendix's *updater* entry states the rejection correctly. Repair: restore
"of a format major version it implements, carrying no top-level record of a
type it does not implement with MU = 1".

### 8. apph-updater-reemit-condition-dropped (diagrams-03) — CONFIRMED, not byte-level

Appendix H: "re-emits every retained record byte-identically (§20.4)".
[R-WRT-05] (3354–3358): "every record it retains **and does not logically
modify** … a record it modifies is new output under its writer obligations".
The checklist contradicts its own preceding clause, which permits an updater
to change a layer's names and grow an extent — logical modifications of a
retained record. Non-normative; the cited rule states both conditions.
Repair: add "and does not logically modify".

### 9. empty-layer-redeclare-qualifier-drift (diagrams-04) — CONFIRMED, not byte-level

Three statements of one permission with three qualifiers:
step 4 (3204–3207) "subject to every rule its new **declarations** are
subject to"; shape (c) (3336–3338) "subject to every rule its new
**geometry** is subject to, which is the same step's permission"; §11.1's
Rationale (1646–1648) "may be re-declared freely" with no qualifier. The
document does use *geometry* narrowly (§11.1's heading; §19.3's list treats
"the geometry floor and its arithmetic" as one item among a dozen), so the
figure's substitution is a narrowing while asserting identity.

Both restatements are in labelled blocks. [R-CNT-23], [R-TYP-07], [R-COD-07]
and the §19.3 value sets bind a layer record in any generation independently
of §20.3, so a file written on the narrow reading carries a register row and
[R-CNF-05] bars it under both readings. Repair: "declarations" in both
places.

### 10. compaction-figure-prime-undefined (diagrams-05) — CONFIRMED, not byte-level

The figure draws A's tiles immediately after `front` in both rows, so A's
stored extents do not relocate — yet it marks `A: index′`. The caption
("extent slots are re-pointed and each index region any of whose stored
extents moved is regenerated — the ′ marks") does not say which of the two
the mark denotes. A's index region *does* move, so under a "re-pointed"
reading the mark is right and under a "regenerated" reading it is wrong.

Not byte-level: where nothing moved, a regenerated region is byte-identical to
a copied one — same offsets, lengths and crcs, "segment CRCs recomputed over
the entries as re-emitted" (3486–3489). The refuse-versus-emit consequence
diagrams-05 gestures at is group 17's subject and is decided there. Repair:
say what ′ marks.

### 11. l14-condition-drops-residue (diagrams-06) — CONFIRMED, not byte-level

L14's Condition cell names truncation and overrun; its Instances cell names
three ("sub-record header; sub-record inline_length; trailing residue"), and
[R-CNT-18] (3132–3134) names three: "any overrun, truncation, or residue".
The file-scope twin F29 states all three. §21.1's "where a row and the rule it
cites diverge, the rule governs" decides the verdict; what is damaged is
[R-VEC-03]'s per-instance corpus, since the third instance's condition is not
described in its own row. Instance count is unaffected (the cell is
unchanged). Repair: add ", or bytes remain after the last complete
sub-record" to the Condition cell.

### 12. f3-missing-in-domain-qualifier (diagrams-07) — CONFIRMED, not byte-level

F3 lacks the "although every contributing field is in domain" qualifier its
siblings L2 and T12 carry, so it is entailed by F2 for the same field; and
its "so the sum wraps" is not in [R-ENC-04], which states the condition as
"whose mathematical value would exceed 2⁶³ − 1" and mentions wrapping only in
the separate prohibition "MUST NOT act on a wrapped or truncated value".
§21.1 decides the verdict twice over (rule governs; and the specialization
rule records the file against the narrower row). Repair: add the qualifier,
drop "so the sum wraps".

### 13. s216-closing-overstates-reader-side (register-02) — PARTIAL, not byte-level

§21.6 (3862–3864): "neither is a reason for a reader to reject anything."
[R-CNF-12] (3323–3326): "For a nonconforming file no acceptance obligation
exists — a reader MAY reject it upon detecting any violation, **including
violations whose assigned detector is the verifier**."

The reading that would remove that licence is foreclosed twice. §21.6's
opening rule is scoped to "**These** are defined behaviors" — the table's
entries — and the closing paragraph says these two conditions were moved *out*
of that table. And §2.1 binds BCP 14 keywords "when, and only when, they
appear in all capitals": a lowercase "is a reason" cannot bound an
all-capitals MAY. So the sentence is true on its own subject (no rule *here*
supplies a rejection ground) and over-states in isolation. [R-CNT-18] models
the careful wording: "on a nonconforming file `[R-CNF-12]`'s licence to reject
on any detected violation is untouched". **Premise:** that "reason" in a
sentence about what belongs in a defined-non-violations table names a rule
stated there, not the general licence stated in §2.4. Repair: adopt
[R-CNT-18]'s clause.

### 14. cnt25-never-invalidates-unscoped (register-03) — PARTIAL, not byte-level

§7.1 (974): "Application metadata never invalidates the structural data it
annotates." [R-MTA-05] (2779–2782) says of unsorted members: "the file is
nonconforming, a verifier MUST report it, and readers process the document
unchanged."

The reading that would fork a verifier's verdict is foreclosed by §21.1
(3636–3642), which names these exact rows:

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, **not an obligation on any reader**: the governing
> rule states what a reader does, and for several such rows it obliges the
> reader to serve the structure unchanged (`[R-CNT-22]` …; and `[R-MTA-05]`,
> whose unsorted document readers process as they find it — **F27 and L48**).

So "invalidates the structural data it annotates" is true in the sense of
usability, which is the sentence's subject, and false only under a reading
that equates it with file conformance — which [R-MTA-05] and §21.6's closing
paragraph both decide expressly. **Premise:** that "invalidates the structural
data" names usability of the annotated structure, not the file's conformance
predicate. Repair: a scope word, or a pointer to [R-MTA-05].

### 15. registered-record-type-implementation-premise (adversary-03) — REFUTED

The claim is that nothing requires a conforming reader or updater to
implement the registered record types, so [R-CNF-03]'s relief clause reaches
type 0x0001 and the em-dash gloss is false.

**The sentence that forecloses it** is §19.1 step 4, inside [R-RDR-01]
(2872–2874, 2895–2903): "A conforming reader opens a file **by these steps, in
order**: … 4. **Record walk.** Parse the record sequence under §7.2's framing
…, and **build the layer table: each layer record's name, parsed and checked
per §4.6**." A reader that does not implement type 0x0001 cannot perform an
open, so it is not a conforming reader at all; and §2.3 makes updaters and
verifiers readers of what they process. The same step obliges the top-level
user-metadata framing rules, and [R-CNF-03] separately obliges "every
user-metadata encoding §18.2 assigns", which [R-MTA-03] makes both assigned
encodings core. So a conforming reader implements both registered types, the
relief clause never reaches 0x0001, the gloss holds, and §20.4's "an updater
implements both registered types" is derived rather than assumed. The second
limb (an updater dropping a layer record) additionally requires an L49 input.

No repair needed; making the premise explicit in [R-CNF-03] would be a
courtesy, not a correction.

### 16. binary64-rounding-direction-unnamed (adversary-04) — PARTIAL, not byte-level

Self-flagged byte-level. I spent the second-most effort here.

[R-MTA-04] (2720–2726): "A reader interprets every JSON number as an **IEEE
754 binary64 value** and MAY use a wider representation. A document is
unreadable if it contains a number whose binary64 interpretation is not
finite — which covers a magnitude that overflows on conversion".

The arithmetic is right: 2¹⁰²⁴ − 2⁹⁷⁰ is the midpoint, ties-to-even carries it
to 2¹⁰²⁴ and overflows; roundTowardZero yields DBL_MAX. The window is half an
ULP wide.

**Two sentences close it.** First, §2.3 [R-CNF-02] (156–158): "**File
conformance is a pure predicate on bytes: it does not depend on any reader,
writer, or environment.**" That forecloses reading (b) outright — a finiteness
test taken under whatever attribute the reader's conversion happens to run
with would make conformance depend on the reader's environment, which this
sentence forbids. So the test is under one fixed attribute. Second, the rule
names the standard, and Appendix F carries it as a normative reference
("**[IEEE 754]** IEEE 754-2019"): IEEE 754-2019 makes roundTiesToEven the
default rounding-direction attribute for results in binary formats, so a
conversion "as an IEEE 754 binary64 value" with no attribute stated is under
the default. A parser that clamps on overflow is not performing the IEEE
conversion at all.

**Premise of this downgrade, stated for attack:** that §18.2's invocation of
"an IEEE 754 binary64 value" imports IEEE 754-2019's *default* rounding
attribute, notwithstanding that Appendix F's parenthetical scopes the
reference to §12.1. A triager who holds the reference scoped to §12.1, and
holds §2.3's purity clause to establish only that the document *intends*
determinacy without supplying it, gets byte-level. That is a live objection
and I flag it rather than bury it. Repair is one clause: "…as an IEEE 754
binary64 value under roundTiesToEven".

### 17. compactor-refusal-vs-placement (adversary-05) — REFUTED as stated

The claim is that whether a compactor must refuse a structurally malformed
index entry turns on a free placement choice, because [R-WRT-07] keys
regeneration to relocation.

**The sentences that foreclose it**, both in §20.5 and one of them two lines
above the compound list the finding calls restrictive:

- [R-WRT-09] (3553–3559): "it relies structurally on **every structure it
  copies**, so it MUST verify **each link of the chain** — the open (§19.1),
  each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`),
  and each relocated extent's checksum, **including every stored tile's entry
  crc** — before emitting that structure's bytes." "every stored tile's" is a
  universal, not a restriction to relocated tiles; a restrictive reading would
  have had to say "the entry crc of every relocated stored tile".
- §20.5's own gloss (3499–3502): "That `[R-WRT-09]`'s checks reach the index
  chain **and each stored tile's entry crc** rather than an entry's own value
  domain bounds how far a compactor goes looking" — the entry crc is named
  again, unqualified by relocation.

Verifying a stored tile's entry crc requires using the entry, which under
§15.3 means classifying it, so the malformed entry is met under every
placement and [R-WRT-06]'s refusal is owed either way. The reporter reaches
the same conclusion. Repair, if any: reorder the compound list so "including
every stored tile's entry crc" does not sit inside the relocated-extent
clause.

### 18. interleaved-channel-rename (quiz-02) — REFUTED

May a commit rename a channel of an interleaved layer that stores tiles?

**The sentence that forecloses it** is the structure of the two lists
themselves (3179–3191). The permitted list is stated as exceptions — "keeps
its declarations, **with these exceptions and no other**: its name, and its
dimension and **channel names**, MAY change" — unqualified by layout. The
fixed list is then expressly the residue: "**Every other** declaration is
fixed for as long as the layer stores a tile: … an interleaved layer's channel
list …". Because the fixed list quantifies over what is *other than* the
exceptions, "an interleaved layer's channel list" cannot re-capture channel
names, which are an express exception. Reading A is the only one available.
Confirmed independently by the fixed list stating "every channel's type and
fill" as a separate item (redundant if "channel list" already reached every
per-channel field) and by the principle paragraph's "a name enters no map".

No repair needed. Note this same "Every other" argument does *not* dissolve
group 4, because there the disputed operation is not itself an express
exception on its face: it is a composition of two, and whether the
composition is an exception is the open question.

### 19. walk-incompleteness-carveout-only-in-97 (quiz-04) — PARTIAL, not byte-level

§5.2 (713–721) lists three incompleteness grounds, the first being "a
scope-level rejection ends that scope's enumeration". §9.7's closing sentence
(3511–3514 region, at 1511–1514) supplies the carve-out: "An entry
`[R-IDX-03]` classifies reject-tile on a *structural* ground does not make the
walk incomplete: the walk passes over it, and the bytes it nominally addresses
fall to slack (§15.3)."

The reading is decided, and §5.2's own wording is already conditional: it says
the walk is incomplete "**where** a scope-level rejection ends that scope's
enumeration", and §9.7 says of a structural reject-tile that the walk passes
over it — so no enumeration is ended and §5.2's condition is not met. That
makes the finding weaker than reported: §5.2 is not falsified, only thin.
[R-IDX-03] itself (2204–2210) says the same: such an entry "contributes … none
to `[R-LIF-08]`'s coverage walk". **Premise:** that §5.2's "where … ends that
scope's enumeration" is a test rather than a label, so a rejection that ends
no enumeration is outside it. Repair, optional: a cross-reference at §5.2.

---

## Which groups I tried hardest to kill and failed

1. **planar-channel-list-composition (group 4).** Six candidate closers tried;
   four refuted the reporters' *mechanism* without touching the *permission*,
   and the two that bear on the permission ("every channel's type and fill"
   vs the both-sides tie-break) point in opposite directions. Upheld
   byte-level.
2. **binary64-rounding (group 16).** Killed, but on an imported default from a
   normatively referenced standard plus a purity clause, not on a sentence in
   §18.2. The single most likely place for a refuter to land.
3. **s216 / cnt25 (groups 13, 14).** Killed on §21.1's verifier-row paragraph
   and §2.1's casing rule respectively; both survive as over-statements.
