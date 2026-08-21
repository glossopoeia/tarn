# Round 16 triage — skeptic pass

## Access disclosure

Read only `spec/tarn.md` (§2.1–2.5, §3.1, §5.2, §6.1, §9.7, §11.1–11.4, §14.2–14.5,
§15.2–15.4, §17.2–17.3, §18.2, §19.3, §20.1–20.5, §21.1–21.9, §22.3, Appendix G,
Appendix H's verifier checklist). Ran only `sed`/`grep`/`wc` over that one file.
Read **no** transcript in `round16/` — neither a walk transcript nor any
`transcript-triage-*.md`. I listed the round16 directory once (`ls`) before reading
the brief's prohibition carefully; the listing showed filenames only and I opened
none of them. Recorded here for honesty.

No git history, no docs/, no PLAN.md, no AGENTS.md, no conformance/, no registry.json,
no web.

## Grouping (33 ids → 14 groups)

| group | ids |
|---|---|
| G1 §21.7 "and nowhere else" | reader-01, writer-01, verifier-02, diagrams-01, register-01, adversary-01, quiz-02 |
| G2 [R-WRT-06] duplicated limb | reader-04, writer-04, verifier-04, diagrams-03, register-05, adversary-05, quiz-03 |
| G3 shrink + surviving-tile padding | writer-02, quiz-01 |
| G4 tense clause vs shrink-to-zero + re-declare | reader-02, register-04, adversary-02 |
| G5 T18/R4 instance asymmetry | diagrams-04, register-03, adversary-03 |
| G6 content sniffer | reader-03, diagrams-05 |
| G7 §11.1 Rationale "ordinals renumber" | writer-06, adversary-04 |
| G8 P·Q in an empty layer | verifier-01 |
| G9 Appendix G / filter | writer-03 |
| G10 §20.4 "the file's layer set" | writer-05 |
| G11 [R-WRT-07] citing [R-WRT-06] | verifier-03 |
| G12 verifier's duty toward SHOULDs | verifier-05 |
| G13 §20.5 compaction caption | diagrams-02 |
| G14 R3's "§21.6 governs" | register-02 |

G3 and G4 are deliberately kept apart. Both sit in §20.3 step 4's shrink paragraph,
but G3 is about **surviving** stored tiles gaining padding positions and G4 is about
**dropped** tiles plus a bundled declaration change. Different premises, different
repairs.

## G1 — §21.7's "and nowhere else"

Text checked (§21.7, verbatim):

> §20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally constrains —
> a padding position, a pad bit, or a boolean byte — the §21.4 rows firing there and
> nowhere else

Counterexamples verified against the rows as written:
- T14 (§21.4): "Codec 1 (none) declared and a non-sentinel index entry's length
  differs from the tile's decoded size", detector *reader*, detected *tile use*,
  governing `[R-COD-04]`, which itself says the check is "checkable from the entry
  and the layer record alone, before any payload fetch."
- T17: "Codec 3 (zstd) and the stored bytes do not begin with the compressed-frame
  magic 28 B5 2F FD", detector *reader*, *tile use*.
- T3: "The decoded payload's byte length is not exactly the tile's decoded size
  derived from the layer's declarations."
None of these requires a padding position, a pad bit or a boolean byte, and §20.3
step 4 expressly lists "the decoded size … or the codec and filter that produced the
stored bytes" among what the bar covers.

Tried to kill it three ways and failed:
1. *"Witnessed" might mean witnessed-as-a-change.* register-01 already answers this
   and the answer holds: T4 does not witness a change either (a creator can emit a
   wrong padding byte from scratch), so under that reading the sentence's own named
   rows witness nothing and the clause is vacuous.
2. *Maybe §20.3 step 4 elsewhere concedes the change is undetectable.* It says the
   opposite, in normative text: "Where a change does reach them it makes each stored
   tile it reaches nonconforming." That corroborates the finding.
3. *Maybe §21.7 is scoped to exclude these rows.* No such scoping exists; the clause
   is stated as a conjunctive necessary condition plus "nowhere else".

CONFIRMED.

**Byte-level: no.** Deciding sentences, quoted:
- §21.1: "The subsections after §21.5 are not part of the register and carry no rows:
  neither this completeness clause nor the instance arithmetic below reaches §21.6's
  defined non-violations, §21.7's account of what no check detects, or §21.9's
  limits."
- `[R-CNF-04]` (§2.3): "A reader MUST detect every violation the error register (§21)
  assigns to the reader as its detector, and apply the outcome class this
  specification assigns to each".
So §21.7 grants no exemption and creates no duty; T3/T14/T17/T24/T25 bind through
their own rows either way, and every reader rejects the same tiles before and after
the repair. Severity: register-bookkeeping — §21's account of itself.

reader-01's extra observation is correct and worth carrying into the repair: after
the codec, filter and decoded-size limbs are removed from the "unwitnessed" claim,
what is genuinely unwitnessed is the *sample byte offset* limb (e.g. a channel
reorder at unchanged total stride), plus the padding-set limb on a layer that has no
padding position.

## G2 — [R-WRT-06]'s duplicated limb

Verified verbatim at §20.5:

> it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call
> the output clean — and a record §20.4 does let it drop is no exception, dropping
> being available only where that table licenses it — nor re-emit it corrected
> (`[R-WRT-05]`).

First and third limbs are the same proposition under the same citation. Hunted for a
distinguishing antecedent for "it": the interposed aside says a droppable record "is
no exception", i.e. it is subject to the same limbs rather than opening a new one, so
no reading makes limb 3 distinct. CONFIRMED, editorial.

adversary-05's second instance is real too — §22.3 `[R-SEC-04]`: "recovery output is
re-verified as a whole file before being trusted (`[R-LIF-06]`) before any use" —
same shape, one adverbial written twice. Folded into this group's repair.

**Byte-level: no.** `[R-WRT-05]` is cited in both limbs and states the byte-identical
re-emission rule; a compactor's lawful outcomes are the same two under every reading.

## G3 — the shrink paragraph's false premise (the group I tried hardest to kill)

Text (§20.3 step 4):

> An extent MAY also **shrink**. Where the shrink leaves a stored tile addressed it is
> the case above — barred wherever it alters what §14 fixes for that tile — but where
> it drops a tile out of the addressed set entirely (§11.2's grid count falls),
> nothing is altered for a tile the new state stores, and the commit is permitted

Both counterexamples check out arithmetically. quiz-01: rank 1, E 25→15, T 10, so
G 3→2; tile 2 drops, tile 1 (stored, retained, still addressed) gains padding
positions at x = 15…19 where it holds real samples. writer-02: E=(5,5)→(5,3),
T=(4,4), G_x 2→1; the t_x=1 column drops, and surviving tiles gain a padding position
at x=3. In both, *both* clauses' antecedents hold, and the asserted premise "nothing
is altered for a tile the new state stores" is false. The defect is real: CONFIRMED.

**Byte-level: no.** Three quotations decide it, and a fourth kills the reporter's own
support for the losing reading.

1. The same sentence's first limb: "Where the shrink leaves a stored tile addressed
   it is the case above — barred wherever it alters what §14 fixes for that tile."
   In both counterexamples the shrink *does* leave stored tiles addressed, so this
   antecedent is satisfied and the consequent is "barred". Reading R1 needs the
   second limb to override the first where both fire; nothing licenses that priority,
   and it is the first limb that points at the governing MUST NOT.
2. The governing MUST NOT, three sentences earlier, is unconditional and quantified
   over every such tile: "A commit MUST NOT change a layer's declarations in a way
   that alters, for any tile that layer stores **in the generation this commit
   supersedes** … the set of padding positions (§11.3) and the content `[R-SER-05]`
   fixes there". And the step states its own test per tile: "The test is the effect
   on such a tile, and the list names where that effect arises rather than standing
   on its own."
3. §2.1 gives BCP 14 force "when, and only when, they appear in all capitals". The
   drafters used all-caps for the shrink permissions they meant as permissions ("An
   extent MAY also **shrink**"; "A layer that stores no tile MAY be re-declared
   freely") and lowercase for "the commit is permitted". A lowercase gloss resting on
   a false factual premise does not override an all-caps MUST NOT.
4. quiz-01 cites §11.1's Rationale as evidence that R1 "is the intended reading". Check
   the citation, not the sentence around it: the Rationale reads "a shrink is barred
   wherever it alters what §14 fixes for **a tile the new state still stores**". In
   quiz-01's own counterexample tile 1 *is* a tile the new state still stores, and the
   shrink alters what §14 fixes for it — so the cited Rationale bars quiz-01's
   commit rather than permitting it.

Emittable-by-another-actor check, made explicitly: the file R1 would produce is
nonconforming as a byte sequence under `[R-SER-05]` ("at every padding position, a
writer MUST encode … that channel's fill value … a verifier MUST check it, and a
violation is a validity error at tile scope") and is registered as T4. §2.3 makes file
conformance "a pure predicate on bytes", so no actor and no history can make those
bytes conforming — a creator could not emit them either. Every conforming verifier
returns the same verdict on the file under both readings, and the set of conforming
files is unchanged. What the two readings fork is one appender's *conduct* while
producing an already-nonconforming artifact, not the accept/reject boundary.

Noting for the record that writer-02's own cited closer does **not** hold: `[R-CNF-06]`
binds an updater to "every writer requirement for the bytes it produces", and the
appender does not produce tile 1's bytes — `[R-WRT-01]` deliberately gives appenders
the per-bytes obligation rather than the creator's whole-file one. The finding
survives that; it does not survive quotations 1–4.

This is the closest call in the batch. If a maintainer reads the two limbs as
per-commit alternatives rather than per-tile, it becomes byte-level. I do not, because
the first limb's antecedent is "a stored tile" and the step's own test is stated
per-tile. Repair either way: condition the permission — "…and alters nothing §14
fixes for any tile the new state still stores".

## G4 — tense clause vs shrink-to-zero plus a declaration change

Deciding sentence, quoted, and it is the sentence written for exactly this case:

> The tense is the prior generation's (§3.1 defines *stored* against a generation), so
> a commit does not escape this by unstoring in the same breath: superseding every
> tile of a layer and re-declaring it are one operation, and this bars it.

§3.1 confirms the mechanism-independence: "A tile is *stored in a generation* if and
only if that generation's tile-index entry for it is not the sentinel; unqualified
*stored* means stored in the live generation." De-addressing by shrink and
superseding by sentinel both leave the tile not stored, so both are "unstoring in the
same breath" and both are reached.

The shrink paragraph does not say the opposite. It licenses *the shrink*; it nowhere
says a declaration change may be bundled with one, and its premise clause is about
§14 effects on surviving tiles. All three reporters independently concluded "barred",
which is the answer the tense clause gives.

PARTIAL — the residual defect is real but smaller than reported: the shrink
paragraph's "a tile the new state stores" and §11.1's Rationale's "a tile the new
state still stores" both float the tense the sentence above just pinned, so the
paragraph reads as though it re-opened a question it did not. Editorial. Not
byte-level: both routes leave conforming live states and §21.7 already records that
"a commit that supersedes every tile it would have damaged leaves the live state
clean, so the bar is unwitnessed there".

## G5 — T18 vs R4

Verified both cells verbatim. T18: four instances, three of them skippable-frame
placements. R4: "a skippable frame, top-level extent; a skippable frame, layer
sub-record extent" — placement-agnostic, one per container. §18.2 carries the same
constraint over: "the frame magic; no skippable frame and no second frame; no nonzero
dictionary ID; no content-checksum flag."

Tried to distinguish them: §18.2's "exactly one RFC 8878 compressed frame occupying
the extent's bytes before its terminal CRC" is a span condition, which might make
placement immaterial for R4. But T18's condition is "the stored extent holds more
than the single compressed frame" — the same span shape. Nothing in the text makes
the two rows' checks differently shaped, so §21.1's criterion is being applied two
ways to one rule. §21.1 itself does not arbitrate: "the count is therefore mechanical
once the cell is written". CONFIRMED.

Arithmetic sanity: 36 + 49 + 26 + 10 = 121 conditions, matching §21.8's "121
conditions over 275 instances". I did not re-derive 275 by hand; two reporters did
independently and agree, and nothing in my grade turns on it.

**Byte-level: no.** §21.1: "The **Instances** column enumerates what a conformance
corpus builds for that row (§21.8)". Only corpus size moves; `[R-COD-06]` and
`[R-MTA-09]` decide every extent's verdict without reference to the column.
Register-bookkeeping, and the direction (T18→2 and 273, or R4→+4 and 279) is a
maintainer's call.

## G6 — the content sniffer

Verified: "content sniffer" occurs exactly twice (line 713, inside `[R-CNT-04]`'s
normative sentence; line 729, inside a Note). §2.3 opens "Conformance is defined for
five classes" and names file, reader, writer, updater, verifier. So a normative MUST
binds a party with no conformance class and assigns it reject-file, which §2.4 defines
as a reader outcome. CONFIRMED.

One correction to both reporters: the "phrasing discipline" they lean on — "every
requirement names the actor it binds (writer, reader, updater, verifier, or file)" —
is inside a **Note**, and §2.1 excludes "any text labeled *Note*, *Example*, or
*Rationale*" from the normative document. The discipline is a description of house
style, not a rule the sentence violates. §2.3's five classes carries the argument on
its own.

**Byte-level: no.** F6 restates the rule with the sniffer dropped: "the obligation
binds a reader holding those bytes resident, and a reader that would have to fetch
them MAY defer or omit the check (`[R-CNT-04]`); a verifier holds no such exemption
(§2.3)", detector *reader*, outcome reject-file. Appendix H's verifier checklist says
the same. Every accept/reject on the front block is decided by the resident-reader
half, which binds any party holding [0,16) — a sniffer included. Editorial.

## G7 — §11.1's Rationale on renumbering

`[R-GEO-06]`: "the **spatial tile ordinal** of (t₀, …, t_{d−1}) is s = Σᵢ tᵢ · ∏_{j>i}
Gⱼ", and the disk ordinal is "s for an interleaved layer, and **c · N + s** for a
planar layer". Growing dimension m raises G_m, which appears in the coefficient of
t_i for every i < m. So ordinals are preserved **iff m = 0** — the first-declared
dimension — and only in an interleaved layer, since planar's c·N shifts every c ≥ 1
whenever N changes. The Rationale's unqualified "disk ordinals renumber" is therefore
wrong in exactly that case. CONFIRMED.

adversary-04 states this correctly. writer-06's headline — "any dimension but the
last" — is itself wrong: growing a middle dimension m raises G_m and renumbers every
t_i with i < m. Its worked example (rank 2, growing y) is a first-dimension growth and
is right.

**Byte-level: no.** §2.1: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*". The normative
statement carries the correct qualifier — §20.3 step 4: "(a geometry change renumbers
ordinals wherever `[R-GEO-06]` moves them)". Editorial.

## G8 — P·Q in a zero-extent layer (verifier-01, self-flagged byte-level)

The reporter's case is that the only text deciding whether `[R-ENC-04]` reaches P·Q in
a layer addressing no tile is §17.2's Note, which §2.1 excludes. I searched for
normative text and found three pieces:

1. `[R-SER-07]` (§14.3, normative): "decoded size is a function of the layer's
   declarations alone — geometry, layout, and channel types — never of payload
   content, and readers allocate from those declarations, not from stored data. Every
   decoded size, and the value count V, is a declaration-derived quantity under
   `[R-ENC-04]`." A zero-extent layer has all three declarations, so it has a decoded
   size, and that decoded size is under `[R-ENC-04]`. Reading B's premise — that no
   decoded size is *defined* absent a tile — is contradicted here in terms.
2. `[R-SER-02]` (§14.2, normative): "These products and sums are declaration-derived
   quantities under `[R-ENC-04]`."
3. §20.3 step 4 (normative, not a Note): "`[R-COD-07]`'s lz4 decoded-size cap among
   them (L44), which an empty layer escapes **only because that cap is quantified over
   addressed tiles**. `[R-ENC-04]`'s 2⁶³ − 1 ceiling **on every derived product** is
   another". The "only because" plus "on every derived product" is precisely the half
   the reporter says exists nowhere but the Note.

The register corroborates by contrast within one table: L44 reads "Codec 4 (lz4)
declared on a layer any of whose **addressed tiles'** decoded size exceeds
0x7E000000", while L2 reads "A declaration-derived sum or product **of a layer**
exceeds 2^63 - 1", instancing "P·Q (which dominates V = P·C); P·Bᶜ", detector
*reader*, detected *layer access*, governing `[R-ENC-04]` (R-GEO-03, R-CNT-13,
R-SER-02, R-SER-07). If P·Q existed only where tiles exist, L2's detection point
would be tile use, as T3's and T14's are. (I do not lean on L2 alone: §21.1 makes a
row a restatement, "and where a row and the rule it cites diverge, the rule governs".
The rule, via `[R-SER-07]`, does not diverge.)

So the reporter's witness file is nonconforming and "Verifier B" is not a conforming
verifier — `[R-CNF-04]` obliges it to detect L2. No fork. PARTIAL, not byte-level:
what is genuinely true is the smaller point that §19.3's enumeration names
"`[R-ENC-06]`, `[R-ENC-03]`" and "the geometry floor and its arithmetic
(`[R-GEO-01]`–`[R-GEO-03]`)" but never `[R-ENC-04]` by identifier, so the layer-access
duty for L2's non-geometry instances reaches §19.3 only through `[R-GEO-03]`'s
"subject to `[R-ENC-04]`". A one-identifier addition closes it.

This is the second group I tried hardest to uphold. It failed on `[R-SER-07]`'s
"function of the layer's declarations alone".

## G9 — Appendix G and the filter

Confirmed mechanically: "filter" does not occur anywhere in Appendix G (lines
4088–4211).

But the finding misreads item 5. Its stated test is not "changes the stored bytes and
is not implied by content"; it is: "**No declared alignment and no slab**, or fixed
declared values — both change **placement** and neither is implied by content." The
filter changes no placement. Item 5 exists to close item 3's placement rule, which
leaves gaps open "save where alignment forces a gap".

And the profile nowhere pins the caller's encoding declarations. Item 2's own
justification says so: "this format fixes no canonical serialization of logical
content, and two files carrying the same arrays can legitimately differ in tiling,
layout, and codec." Layout, linearization, tile extents, channel order and codec value
are all "not implied by content" and all left to the caller; the filter sits with
them. Item 1 pins the codec *encoder*, not the codec value, because RFC 1951/8878
leave encoder output open — a freedom the filter does not have: `[R-COD-10]` fixes
the transform completely ("The shuffle stride s is the channel's element size for a
planar tile and the sample stride Q for an interleaved tile … the filtered image
places byte i of group j at offset i · n + j"), and "A writer that filters with any
other stride violates this rule". So for a given declared filter value the output is
determined, and the closing claim "Everything else the profile needs is already
mandatory" is true of the filter.

The finding's test proves too much: applied consistently it would oblige Appendix G to
pin layout and tiling as well. REFUTED. Not byte-level; Appendix G is headed
non-normative and "adds no requirement to any actor".

## G10 — "the file's layer set"

The discriminator is inside the one sentence: "for a layer sub-record, that layer's
record, the entry set of its index, or which of its tiles are stored; for a top-level
record, the file's layer set or another *non-layer* top-level record." The drafters
wrote "that layer's **record**" where they meant a record's content changing, and
"the file's layer **set**" where they meant membership. §20.4 also fixes that
membership only ever grows: "No commit therefore removes a layer record."

So reading (a) — a rename does not license the drop — is what the text says, which is
what the reporter concluded. PARTIAL: the phrase is worth one clarifying clause
because "layer set" is nowhere defined, but the parallel decides it. Not byte-level;
and note that even under reading (b) both outputs are conforming with no file-level
witness, so nothing about accept/reject moves — only an updater's conduct.

## G11 — [R-WRT-07]'s "`[R-WRT-06]` having obliged the compactor to refuse"

The trace through `[R-WRT-09]`'s enumeration is accurate, and §15.3 does say a
structural entry "contributes no stored extent to the *verifier* rows … and none to
`[R-LIF-08]`'s coverage walk", so "each relocated extent's checksum" really does not
reach T6.

But the citation is to `[R-WRT-06]` whole, not to its first clause, and the rule's
second clause carries it: "and MUST NOT emit a file carrying a violation it has
detected". Detection is forced by `[R-WRT-07]`'s own regeneration rule — "entry
offsets new; entry lengths, entry crcs, and **sentinel entries unchanged**" — which
cannot be performed without applying §15.3's classification ("For each entry … a
reader MUST classify as follows"), and §15.2 makes crc = 0 part of what a sentinel is,
so a T6 entry is met precisely while deciding whether to copy it or to compute it a
new offset. `[R-CNF-11]` makes the compactor a reader inheriting every reader
obligation, and T6's detector is *reader*.

So the cited rule does support the conclusion, by its second clause. PARTIAL, and the
reporter's own preferred reading (ii) is the right one; the improvement is to name
`[R-IDX-03]` in `[R-WRT-09]`'s list so the support is by the first clause too.
Editorial, not byte-level: the input carries T6 and is nonconforming either way.

## G12 — must a verifier hunt SHOULD deviations?

Reading A is closed by a two-step inside §2.3/§2.4. §2.3 defines a conforming file as
"A byte sequence satisfying every **file-level requirement** of this specification".
`[R-CNF-12]` says "Deviation from a SHOULD is not a violation for this purpose: §21's
register enumerates MUST-level conditions only, and a verifier reports a SHOULD
deviation as an advisory that does not bar certification." If a SHOULD were a
file-level requirement, a deviating file would fail §2.3's definition — which
`[R-CNF-12]` expressly denies. So SHOULDs are not among the "file-level requirements"
a verifier "additionally checks", and Reading A has no support.

REFUTED. Not byte-level on the reporter's own ground: the verdict on every file is
identical, and the reporter's `[R-CNT-03]` example shows the document closing the
cases that could have mattered. No repair needed.

## G13 — the §20.5 compaction caption

Premise confirmed. §5.2 defines a structure as "a stored-tile extent, a record extent
(the bytes any record's extent slot references, whatever the record's type, §7.2), the
directory, or the trailer", and §9.7: "A layer record's extent slot addresses that
layer's tile-index region (§7.4), so the region enters the walk once, as that
record's extent." So an index region is a record extent, both record extents in the
figure are marked ′, and the leading clause "every record extent survive[s]
byte-for-byte" is false of every record extent in the figure it captions. CONFIRMED.

**Byte-level: no.** §2.1: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*" — this is an
Example caption. `[R-WRT-07]` states the regeneration normatively and the caption's own
trailing clause repeats it ("each relocated index region is regenerated — the ′
marks"). Severity: figure.

## G14 — R3's "§21.6 governs"

The correction sits four lines above the table, in §21.5's preamble: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as violations: what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding byte's own
value set (`[R-MTA-03]`)." R1's own cell registers "a document encoding of 0, or a
reserved-range value (3-0x7F)", §21.6's entry is scoped to "an experimental-range
(≥ 0x80) document encoding", and Appendix H's verifier checklist closes with "encoding
0 and the reserved range stay violations (R1)". §21.1: "where a row and the rule it
cites diverge, the rule governs."

So the document decides it four ways and the reporter agrees ("only the parenthetical
is wrong"). PARTIAL — the parenthetical is loose and should name the experimental
range — register-bookkeeping, not byte-level.

## Byte-level tally

Zero. Reporters self-flagged two (verifier-01, quiz-01); both are downgraded above
with quotations. The two I fought hardest to uphold were G3 and G8, and I have said
where each would flip.

## Coverage

Counted by hand from the group table: 7+7+2+3+3+2+2+1+1+1+1+1+1+1 = 33. Each input id
appears in exactly one group; no id is dropped or duplicated.
