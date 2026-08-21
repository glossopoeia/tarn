# Round 16 triage — implementer-consequence lens

## What I read

Only `spec/tarn.md`, plus one directory listing of the round16 scratchpad
filtered with `grep -v triage` so no `transcript-triage-*.md` name was
printed and none was opened. I read no walk transcript this round — the
findings quote themselves adequately and I preferred to check the document
directly. Sections read in full or in part: §2.1–2.5, §3.1 (via §20.3's
citation), §4.2 ([R-ENC-04]–[R-ENC-06]), §5.2, §6.1, §11.1–11.4, §14.1–14.5,
§15.1–15.3, §17.2 (codec 4 + Note), §17.3, §19.2–19.4, §20.1–20.5, §21.1,
§21.3 (L2, L44), §21.4 (all 26 rows), §21.5 (preamble + R1/R3/R4), §21.6,
§21.7, §21.8, Appendix G in full.

One mechanical check run:

```
121 rows, 275 instances   # matches §21.8's normative total
T18 = 4 instances, R4 = 12, T24 = 1, T15 = 2, T25 = 3
```

so the two reporters who claimed the cells reproduce 275 exactly were right,
and the T18/R4 defect is not arithmetic.

## Grouping

14 groups over 33 ids. Union checked by hand and by count: 7+7+3+2+2+2+3+
1+1+1+1+1+1+1 = 33.

| group | ids |
|---|---|
| s21-7-witness-account | reader-01 writer-01 verifier-02 diagrams-01 register-01 adversary-01 quiz-02 |
| wrt06-duplicate-limb | reader-04 writer-04 verifier-04 diagrams-03 register-05 adversary-05 quiz-03 |
| shrink-deaddress-tense | reader-02 register-04 adversary-02 |
| shrink-creates-padding | writer-02 quiz-01 |
| content-sniffer-actor | reader-03 diagrams-05 |
| ordinal-renumber-rationale | writer-06 adversary-04 |
| skippable-frame-instances | diagrams-04 register-03 adversary-03 |
| empty-layer-pq-overflow | verifier-01 |
| profile-omits-filter | writer-03 |
| ancillary-drop-layer-set | writer-05 |
| wrt07-refusal-citation | verifier-03 |
| verifier-should-advisories | verifier-05 |
| r3-unassigned-parenthetical | register-02 |
| compaction-figure-caption | diagrams-02 |

Two splits worth defending. **shrink-deaddress-tense vs
shrink-creates-padding** both live in §20.3 step 4's shrink paragraph but are
different defects with different repairs: the first is *all* stored tiles
leaving the addressed set while declarations change (tense conflict); the
second is a *mixed* shrink where surviving stored tiles gain padding
positions (a false premise in the permission). Repairing one does not repair
the other. **adversary-05** carries a second observation (§22.3
[R-SEC-04]'s doubled adverbial) inside a finding whose headline is the
[R-WRT-06] duplicate; it lands in wrt06-duplicate-limb and I carry the §22.3
note into that group's repair.

## Judgements, with the text behind each downgrade

### 1. s21-7-witness-account — CONFIRMED, not byte-level

§21.7, verbatim:

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

§20.3 step 4's bar has four listed effects; two of them (decoded size, codec
and filter) are witnessed by rows that have nothing to do with §14-constrained
bytes. Verified in the table at §21.4: T14 "Codec 1 (none) declared and a
non-sentinel index entry's length differs from the tile's decoded size",
reader / tile use; T3 the same under a compressing codec; T17 "Codec 3 (zstd)
and the stored bytes do not begin with the compressed-frame magic 28 B5 2F
FD"; T25 malformed stream. The counterexamples given by six of the seven
reporters all work on a layer with G·T = E (no padding position), no bool
channel (no pad bit, no boolean byte). register-01 additionally kills the
charitable re-reading ("witnessed *as a change*"): T4 does not witness a
change either, a freshly created file can carry a wrong padding byte, so that
reading leaves the bar with no witness at all.

Downgrade. Nothing about a reader's or verifier's duty moves, because §21.7
neither grants nor removes any:

> The subsections after §21.5 are not part of the register and carry no
> rows: neither this completeness clause nor the instance arithmetic below
> reaches §21.6's defined non-violations, §21.7's account of what no check
> detects, or §21.9's limits.  (§21.1)

and the duty to fire T3/T14/T17/T25 comes from elsewhere and is unconditional:

> A reader MUST detect every violation the error register (§21) assigns to
> the reader as its detector, and apply the outcome class this specification
> assigns to each  ([R-CNF-04])

A reader cannot in any case tell how a file came to be, so a sentence about
which *commits* leave witnesses cannot change what it does with bytes in hand.
Implementer consequence: none on the wire; the cost is that §21.1 makes §21.7
"the account, by class, of what fails" the detectability gate, and an auditor
asking why step 4 owes no register row is given a false answer, understating
detectability — the unsafe direction for this particular section.

Repair: strike the conjunct and say the bar is unwitnessed only where the
change reaches neither a byte §14 structurally constrains nor a quantity the
tile-scope rows cross-check (decoded size against a codec-1 entry length,
stored bytes against the declared codec) — naming T3/T14/T17/T25 beside
T2/T4/T5. Only the byte-offset item (a channel reorder at unchanged total
stride) and a padding-set change on a layer that has no padding are genuinely
unwitnessed.

### 2. wrt06-duplicate-limb — CONFIRMED, editorial

§20.5 as written:

> it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it
> and call the output clean — and a record §20.4 does let it drop is no
> exception, dropping being available only where that table licenses it —
> nor re-emit it corrected (`[R-WRT-05]`).

Limbs one and three are the same proposition under the same citation. No
antecedent for "it" makes the third distinct: under [R-WRT-05] a retained
record is re-emitted byte-identically, so "corrected" re-emission is one
prohibition however the object is named. Not byte-level: a compactor's lawful
outcomes are refuse, or drop where §20.4's table licenses it, under every
reading — "A compactor may drop it whenever it rewrites the file" (§20.4,
MU = 0 / PE = 0 row) is unconditional for compactors, which resolves
reader-04's worry about the dash clause: it bars laundering, not dropping.
Repair: delete the trailing limb. adversary-05's second sighting, §22.3's
"re-verified as a whole file before being trusted (`[R-LIF-06]`) before any
use", is the same edit residue and should be fixed in the same pass.

### 3. shrink-deaddress-tense — CONFIRMED, not byte-level

The two tenses, both in step 4:

> The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so a commit does not escape this by unstoring in the same
> breath: superseding every tile of a layer and re-declaring it are one
> operation, and this bars it.

> …but where it drops a tile out of the addressed set entirely (§11.2's grid
> count falls), nothing is altered for a tile the new state stores, and the
> commit is permitted

All three reporters picked "barred", and I agree: the tense sentence states
what it is doing and why, and "A layer that stores no tile MAY be re-declared
freely" must be read in the same tense or it swallows the bar. But the shrink
paragraph's criterion is stated in the new state's tense and §11.1's Rationale
repeats it that way, so the seam is real.

Downgrade quote — the document itself says this bar has no single-file
witness:

> and a commit that supersedes every tile it would have damaged leaves the
> live state clean, so the bar is unwitnessed there for the same reason
> `[R-LIF-01]` is: it is a property of the prior generation, which §9.7 does
> not reconstruct  (§21.7, normative)

Emittable-by-another-actor, stated explicitly: the live state reading B
reaches in one commit — layer with E = 0, entry_count 0, extent slot (0, 0),
crc_of_crc_array 0, new declarations, the old payloads slack — is exactly the
live state reading A reaches in two commits, and is also a state a creator can
emit outright. So no byte sequence enters or leaves the conforming set; the
two outputs differ only in generation number and slack, neither of which any
rule constrains. Not byte-level.

Implementer consequence, concretely: appender vendor A ships "shrink to zero,
re-declare, grow back" as the supported in-place way to change a layer's
channel types, tile extents, layout or codec; vendor B refuses and sends the
caller to a new layer or a whole-file rewrite. Same document, different
product capability. Worth closing.

Repair: scope the shrink permission in the prior generation's tense — "where
it drops a tile out of the addressed set entirely and the commit changes no
declaration this step's bar reaches" — and fix §11.1's Rationale to match, or
make the shrink an express exception and argue why de-addressing differs from
sentinel-unstoring. That choice is the maintainer's; the text currently
implies both.

### 4. shrink-creates-padding — CONFIRMED, not byte-level

Both counterexamples check out. quiz-01: E = 25, T = 10, G = 3, shrink to 15,
G falls to 2, tile 1 keeps covering x = 10…19 and x = 15…19 become padding
positions in a tile the new state stores. writer-02: E = (5,5), T = (4,4),
shrink E_x 5 → 3, G_x = ⌈3/4⌉ = 1 drops the t_x = 1 column while x = 3 becomes
a padding position in the surviving tiles. The permission's stated premise —
"nothing is altered for a tile the new state stores" — is false in both.

Downgrade. The same sentence's first arm fires and yields *barred*:

> Where the shrink leaves a stored tile addressed it is the case above —
> barred wherever it alters what §14 fixes for that tile

and the general bar three sentences earlier is per-tile and unconditional:

> A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores **in the generation this commit supersedes**,
> what §14 fixes for its stored bytes or how they decode — the set of padding
> positions (§11.3) and the content `[R-SER-05]` fixes there…

with "The test is the effect on such a tile, and the list names where that
effect arises rather than standing on its own" naming the quantifier
expressly. A shrink that leaves stored tiles addressed satisfies arm one's
antecedent, so arm one governs those tiles; arm two's flat "the commit is
permitted" rests on a premise arm one has already falsified.

And the file reading (a) produces is nonconforming under both readings: T4,
"A padding position does not encode, for each channel it carries, that
channel's recorded fill value", detector verifier, at certification. So no
verifier verdict forks and the file is not one any conforming actor may emit.
Not byte-level — but this is the finding in the batch most likely to become a
real shipped bug, because "did a grid count fall?" is a cheap test an
implementer will reach for. Repair (quiz-01's, exactly): condition the second
arm — "where it drops a tile out of the addressed set entirely **and alters
nothing §14 fixes for any tile the new state still stores**".

### 5. content-sniffer-actor — CONFIRMED, not byte-level

Verified: "content sniffer" occurs twice in the whole document — once in
[R-CNT-04]'s normative sentence, once in the Note eighteen lines later, which
§2.1 excludes. §2.3 opens "Conformance is defined for five classes" and names
file, reader, writer, updater, verifier. §2.4's reject-file is defined as a
reader outcome. So a normative MUST binds a party with no conformance status
and assigns it an outcome from another class's vocabulary.

Downgrade: every verdict on the front block is fixed by the resident-reader
half, and the register agrees, dropping the sniffer entirely —

> F6 … the obligation binds a reader holding those bytes resident, and a
> reader that would have to fetch them MAY defer or omit the check
> (`[R-CNT-04]`); a verifier holds no such exemption (§2.3)

Under the reading that a sniffer is a species of reader the conjunct is inert
(a sniffer holds [0,16) resident by construction); under the reading that it
is a sixth actor the MUST is unenforceable. Either way no byte moves. Repair
needs a decision: strike "and a content sniffer" (the resident-reader clause
already reaches any party holding the bytes, and the Note already tells
sniffers what to match), or define the sniffer in §2.3 as a tool outside the
conformance classes and give it its own outcome vocabulary — "not a TARN
file" is §6.3's diagnostic, not reject-file.

### 6. ordinal-renumber-rationale — CONFIRMED, editorial

[R-GEO-06]: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ. Growing dimension 0 raises G₀, which
appears in no coefficient (the product for i = 0 runs over j > 0, and every
later coefficient excludes G₀), so no existing ordinal moves. adversary-04
states this correctly; writer-06's headline generalises it to "any dimension
but the last", which is wrong at rank ≥ 3 — growing the middle dimension of a
rank-3 layer raises G₁, which sits in the i = 0 coefficient and does move
tiles. The defect they share is the Rationale's unhedged clause.

Downgrade: §2.1 excludes Rationale, and the normative statement of the same
operation carries the qualifier — "(a geometry change renumbers ordinals
wherever `[R-GEO-06]` moves them)" (§20.3 step 4). Entries are byte-identical
whether an appender copies or recomputes them. Repair: add the same qualifier
to §11.1's Rationale.

### 7. skippable-frame-instances — CONFIRMED, register bookkeeping

T18 gives four instances, splitting the skippable frame by position; R4 gives
one skippable instance per container for the same [R-COD-06] constraint that
§18.2 carries over. §21.1's criterion:

> a row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them
> (T15, T25)

[R-COD-06]'s own word is "anywhere", which is the T24-shaped family, and
T18's condition text ("holds more than the single compressed frame") does not
vary by position. My count confirms the cells as written total 121/275
exactly, so §21.8's total is consistent with the cells and the defect is the
criterion's application, not arithmetic. Not byte-level: [R-COD-06] and
[R-MTA-09] reject/ignore a skippable frame wherever it sits, under both
readings; only the corpus size moves, and §21.1 scopes Instances to "what a
conformance corpus builds for that row". Repair is a maintainer decision:
collapse T18's three positions to one (275 → 273) or expand R4 by four
(275 → 279), and update §21.8's total either way. [R-VEC-03]'s one-vector-per-
instance obligation is what makes leaving it unresolved expensive.

### 8. empty-layer-pq-overflow — PARTIAL, not byte-level

The reporter's claim is that only §17.2's Note decides whether [R-ENC-04]
reaches P·Q in a zero-extent layer. That is not so; three normative passages
decide it.

> These products and sums are declaration-derived quantities under
> `[R-ENC-04]`.  (§14.2, [R-SER-02] — the table whose rows are P·Bᶜ and P·Q)

> decoded size is a function of the layer's declarations alone — geometry,
> layout, and channel types — never of payload content … Every decoded size,
> and the value count V, is a declaration-derived quantity under
> `[R-ENC-04]`.  (§14.3, [R-SER-07])

> L2 | A declaration-derived sum or product **of a layer** exceeds 2^63 - 1
> although every contributing field is in domain | … N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ;
> N·P; C·N …; **P·Q** (which dominates V = P·C); **P·Bᶜ**; … | reader |
> layer access | `[R-ENC-04]`

L2 carries no addressed-tile quantifier, unlike L44, which states one on its
face ("any of whose addressed tiles' decoded size exceeds 0x7E000000"), and
§20.3 step 4 draws exactly that contrast in normative text: the lz4 cap
"an empty layer escapes only because that cap is quantified over addressed
tiles. `[R-ENC-04]`'s 2⁶³ − 1 ceiling on every derived product is another".
With [R-CNF-04] binding a reader to every row the register assigns it, a
verifier that certifies the 192-byte witness is not a second permitted reading
— it has missed L2. So Reading B is closed and no two conforming
implementations diverge on that file.

What survives, and why this is PARTIAL rather than REFUTED: §19.3's
enumeration of what full layer-record validation covers cites "the geometry
floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`)" — which reaches N, P,
N·P and C·N through [R-GEO-03]'s own [R-ENC-04] sentence — but never cites
[R-ENC-04], [R-SER-02] or [R-SER-07], and P·Q and P·Bᶜ appear in no other
item of that list. An implementer building the layer-access check list from
§19.3 alone omits the two products L2 registers at layer access. Repair:
name [R-ENC-04] (with [R-SER-02], [R-SER-07]) in §19.3's enumeration. Cheap,
and it removes the only reason anyone reached for the Note.

### 9. profile-omits-filter — CONFIRMED, not byte-level

Verified by scan of lines 4088–4211: the word "filter" does not occur in
Appendix G. Item 5 pins alignment and slab because "both change placement and
neither is implied by content"; the filter changes the stored bytes of every
tile — a stronger case than placement — and is not implied by content. §17.3
assigns 1 and 2 and prefers neither ("both are **core**"). So two writers both
claiming the profile emit different stored tiles, different entry crcs,
different layer records, different directory and trailer CRCs for identical
input — precisely the divergence the profile exists to close, and the closing
paragraph's "Everything else the profile needs is already mandatory" is false
of it.

Not byte-level: the appendix is headed non-normative, says outright "It adds
no requirement to any actor: a writer ignoring it is fully conforming", and
[R-COD-09] permits both filter values, so the conforming-file set does not
move. But the implementer consequence is real and is the profile's whole
purpose. Repair (maintainer's choice of value): add an item pinning the
filter — "Filter 1 (none), or a fixed declared filter value" — and add it to
the closing paragraph's list of what the items add.

### 10. ancillary-drop-layer-set — CONFIRMED, not byte-level

§20.4, MU = 0 / PE = 0:

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record,
> the entry set of its index, or which of its tiles are stored; for a
> top-level record, the file's layer set or another *non-layer* top-level
> record.

The sub-record list names "that layer's record" as a trigger; the top-level
list names "the file's layer set". Whether a commit that modifies a layer
record without adding or removing a layer changes "the file's layer set" is
not stated. It is not idle: layer names are the file's namespace keys (F4,
[R-ENC-15] — two byte-identical layer names is a violation), so a *rename*
can be argued to change the set of layers the file has, while an extent
growth plainly cannot. The row closes the neighbouring bootstrap cases
expressly ("Superseding a stored tile's bytes is not such a change for either
kind"; "a commit whose only effect would be the drop MUST retain it") and
leaves this one open.

Two implementations, concretely: appender A reads the phrase as covering any
layer-record change and drops an application's top-level user-metadata record
during a rename-only commit; appender B retains it. The directories differ,
the application's state is gone in A's file, and — the row says so —
"An updater that drops such a record SHOULD report the loss; unreported,
application state disappears with no diagnostic".

Emittable-by-another-actor, explicitly: A's output is a file without that
record, which the same table lets a compactor produce from the same input
whenever it rewrites ("A compactor may drop it whenever it rewrites the
file"), and which a creator may emit outright. Both outputs are conforming and
no file-level witness distinguishes them, so the conforming-file set does not
move and no verifier verdict forks. Not byte-level — but of the non-byte-level
findings this is the one that silently destroys user data, and it should be
closed. Repair (maintainer decision): say expressly whether "the file's layer
set" means which layers exist keyed by name — so a rename changes it and an
extent growth does not — or which layers exist irrespective of any declaration
including the name; and state whether *adding* a non-layer top-level record
counts as changing "another non-layer top-level record".

### 11. wrt07-refusal-citation — PARTIAL, not byte-level

The trace through [R-WRT-09]'s list is accurate as far as it goes: the open
touches trailer and directory only, §19.3's index cross-check is entry_count
and extent_length, [R-IDX-04] is the CRC chain and passes over a T6 entry
whose 20 bytes are as stored. But the finding's conclusion — that the cited
rule does not support [R-WRT-07]'s parenthetical — does not survive checking
the citation itself. [R-WRT-07] cites [R-WRT-06], not [R-WRT-09], and
[R-WRT-06]'s second clause is "MUST NOT emit a file carrying a violation it
has detected". A compactor is a reader of every structure it processes (§20.1,
[R-CNF-11]) and [R-IDX-03] opens "For each entry … a reader MUST classify as
follows"; [R-WRT-09] also obliges it to verify "every stored tile's entry
crc", which cannot be done without classifying entries to find which are
stored. So the compactor detects the T6 entry as a matter of obligation, not
of luck, and [R-WRT-06] as cited obliges the refusal. Not byte-level either
way — both routes end in refusal and the input carries T6 regardless. Repair
is optional tidiness: name [R-IDX-03] in [R-WRT-09]'s enumeration, which
makes the path one word long instead of three steps.

### 12. verifier-should-advisories — PARTIAL, not byte-level

Reading A (a verifier MUST seek and report every SHOULD deviation) is not
supported. §2.3's "checks every file-level requirement" is glossed by the rule
that governs certification:

> Deviation from a SHOULD is not a violation for this purpose: §21's register
> enumerates MUST-level conditions only, and a verifier reports a SHOULD
> deviation as an advisory that does not bar certification.  ([R-CNF-12])

Certification never forks, and no writer's output changes; the register, which
§21.1 makes the verifier's normative inventory, excludes SHOULDs by
construction. What is genuinely open is narrower than the finding states: the
document never says whether a verifier owes advisories it did not happen to
observe. Consequence is real but confined to report contents — a pipeline
gating on "zero advisories" gets different answers from two conforming
verifiers on the same file, both reporting *conforming*. Repair: one sentence
in [R-CNF-12] saying a verifier reports the SHOULD deviations it observes and
is not obliged to seek them (or the converse, if the maintainer wants NFC
checking to be mandatory — that is the item with real cost).

### 13. r3-unassigned-parenthetical — PARTIAL, not byte-level

R3's parenthetical does point every unassigned encoding at §21.6, and §21.6's
only user-metadata-encoding entry is expressly limited to the experimental
range (≥ 0x80), so the pointer is loose for encoding 0 and 3–0x7F. But the
certification hole the finding frames does not open: §21.6 has no entry those
values match, and the preamble four lines above the table says so —

> Encoding 0 and a reserved-range value are unassigned too, and R1 registers
> both as violations: what `[R-MTA-10]` withdraws is the document's content
> rules, never the encoding byte's own value set (`[R-MTA-03]`).

with R1 registering exactly those four instances (reader, at open / layer
access) and Appendix H repeating it. Not byte-level. Repair: narrow the
parenthetical — "under an experimental-range encoding this specification
defines no decoding and §21.6 governs; encoding 0 and the reserved range are
R1's".

### 14. compaction-figure-caption — CONFIRMED, figure

§5.2 defines a structure as including "a record extent (the bytes any record's
extent slot references, whatever the record's type, §7.2)", and a layer
record's extent slot addresses that layer's tile-index region. The figure's
only record extents are "A: index" and "B: index", and both carry the ′ mark.
So the caption's leading clause — "Every stored tile's bytes and every record
extent survive byte-for-byte" — is false of every record extent in the figure
it captions, and is corrected only after the semicolon.

Not byte-level: §2.1 excludes Examples and [R-WRT-07] states the regeneration
normatively and in detail (entry offsets new, lengths/crcs/sentinels
unchanged, segment CRCs recomputed). The exposure is to an implementer who
reads the figure instead of the rule and copies each index region verbatim to
a new offset — whose output then verifies structurally (copied CRCs match
copied bytes) while every entry points at the input's tile placements. That is
a bad failure mode for a documentation defect, which is why it is worth
fixing promptly even at figure severity. Repair: qualify the leading clause —
"Every stored tile's bytes survive byte-for-byte and the reference arrays are
identical; extent slots are re-pointed, retained record extents are copied
unchanged, and each relocated index region is regenerated".

## Coverage

33 input ids, 14 groups, each id in exactly one group, verified by count and
by listing. No id was dropped and none was evaluated only partially. I did not
read any triage transcript.
