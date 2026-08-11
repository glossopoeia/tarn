# Cleanroom round 7 — adversary walk

**Access disclosure.** spec/tarn.md only

## Walk summary

I read spec/tarn.md end to end, then worked as an adversary: for each construction I wrote the concrete bytes and asked whether the text forecloses it or leaves it open. I also re-derived every numeric claim I could check by computation rather than by reading anything else.

Arithmetic and constants all hold. I implemented CRC-32C from §4.5's parameters and confirmed CRC("123456789") = 0xE3069283, CRC(∅) = 0x00000000, `[R-IDX-05]`'s full all-sentinel segment CRC = 0xEECB3BB2 (65,536 × `FF×16 00×4`), and Appendix A's trailer CRC over bytes [0,60) = 0xE00938D2 → `D2 38 09 E0`. Appendix A's whole hex dump is self-consistent with §6.2's field offsets. §11.2/§11.4/§14.2/§14.3/§14.5/§15.4/§17.3/§20.3's worked examples all recompute correctly (ordinals 10, 11452, 74; region bytes [1480,1500); shuffle output; 20,000,064; 644). §21.8's "125 conditions over 242 named instances" is exactly right: I counted 39+50+26+10 rows and, by §21.1's mechanical semicolon rule, 61+100+45+36 = 242 instances.

Attacks the text refuted (worth recording): a tile placed between the live directory's end and the trailer (`[R-CNT-05]`/F9); two layers sharing one index region, entry aliasing, extents inside the directory (`[R-CNT-13]`/§15.3/F36); zeroing or all-ones index regions (§15.2); version-gate-before-field-gates ordering, which cleanly separates *cannot establish* from *nonconforming* (`[R-CNT-06]`, §6.2); duplicate-name-before-name-validity (§19.1 step 4); zstd Window_Size's two derivations for sub-1 KiB tiles (§17.2 note); vacuous slab/alignment invariants; entry_count = 0 where the required crc_of_crc_array = 0 coincides with CRC(∅) = 0; extent_offset + length = F − 64 exactly; extent slots of unknown MU = 0 records (§19.1 step 4 validates them despite ignore-record); the experimental-MU = 1 record, which §21.6 and §2.3 deliberately route to *cannot establish* rather than to divergent verdicts; and 7 bits of unconstrained DEFLATE tail padding, which both verifiers must accept.

One structural discovery shaped my calibration: `[R-CNF-12]` licenses whole-file rejection of any nonconforming file, so *scope-attribution* disputes can never be byte-level — whole-file rejection is always permitted. That leaves only three byte-level channels: whether a file is conforming at all, what a reader returns from a *conforming* file, and what a writer may emit. I found two live ones, both of the first kind, and demoted several findings I would otherwise have flagged.

## Findings (12)

### RD-01 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §17.2 `[R-COD-07]`; §11.1 `[R-GEO-02]`; §14.2 `[R-SER-02]`; §14.3/§14.2 via `[R-SER-07]`; §4.2 `[R-ENC-04]`; §21.3 row L45; §21.6 ("A dimension has extent 0")

In a layer with zero addressed tiles (any dimension extent 0), `[R-COD-07]`'s lz4 cap is quantified over "any of whose addressed tiles" — an empty set — while the decoded size it bounds is a declaration-derived quantity that still has a value. The text never says whether declaration-level bounds apply to a layer that addresses no tiles, so the same bytes are conforming under one reading and reject-layer under the other.

> Writers MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes

> A dimension with extent 0 is valid: its grid count is 0, the layer has zero addressed tiles, its tile index has zero entries, and its reference array is empty. Readers MUST accept such a layer

> decoded size is a function of the layer's declarations alone — geometry, layout, and channel types — never of payload content

> and a reader MUST treat such a declaration as a validity error at layer scope, checkable from declarations alone.

**Permitted readings.**

1. Reading 1 (vacuous quantifier): `[R-COD-07]` and L45 bind only over addressed tiles; a layer with zero addressed tiles satisfies them vacuously whatever T and the channel types are, and §21.6's "A dimension has extent 0 → A valid, empty layer" confirms the layer is conforming. Likewise no decoded size, V, P·Q or P·Bᶜ is ever formed, so `[R-ENC-04]` never fires on them.
2. Reading 2 (declaration-level bound): the decoded size exists as soon as the declarations do — `[R-SER-07]` calls it "a function of the layer's declarations alone", `[R-SER-02]` and `[R-SER-07]` call these products "declaration-derived quantities under `[R-ENC-04]`", and `[R-COD-07]` says its check is "checkable from declarations alone" and §19.3 places it at layer access, which "performs no fetch". Under this reading the layer is reject-layer and the file nonconforming.
3. Reading 3 (split): the lz4 cap is vacuous (its quantifier is explicitly over addressed tiles) while `[R-ENC-04]`'s overflow rule is unconditional (its subject is any "quantity this specification defines as a sum or product"). This mixed reading is textually the best supported and is itself evidence that the two rules were not aligned.

**Picked.** Reading 2 for the file's verdict — reject-layer, nonconforming — because §19.3 lists `[R-COD-07]` among the checks performed at layer access from declarations alone with no reference to whether any tile exists, and because Reading 1 lets a writer declare an arbitrarily oversized tile geometry and dodge every declaration bound merely by setting one extent to 0. But I hold it weakly: `[R-COD-07]`'s and L45's wording is unambiguously a quantifier over addressed tiles, and nothing in §11.1, §19.3 or §21.6 says a bound survives an empty quantification.

**Rationale.** This is the cleanest certify-versus-reject construction I could build, because §21.6 affirmatively declares the empty layer valid while §17.2's bound is phrased over a set that is empty in exactly that case. `[R-CNF-12]` cannot rescue it the way it rescues scope-attribution disputes: the dispute is not about how widely to reject a nonconforming file, it is about whether the file is conforming at all, and a verifier's certificate turns on it.

**Byte-level?** yes — Concrete file: one layer record, name `z`, layout 1 (interleaved), linearization 1, codec 4 (lz4), filter 1, A = 0, S = 0, A_slab = 0, d = 1, C = 1; dimension entry name `x`, extent E₀ = 0, tile extent T₀ = 2,113,929,217; channel entry name `v`, type 6 (uint8), fill `00`; index_encoding 1, entry_count 0, crc_of_crc_array 0, extent slot (0, 0), no sub-records. Every other check passes exactly: G₀ = ⌈0/T₀⌉ = 0, N = 0, addressed-tile count 0, so `[R-CNT-17]`'s extent_length = 0 × 20 + 0 × 4 = 0 matches slot (0,0); P = 2,113,929,217 and P·Q = 2,113,929,217 are both inside 2⁶³ − 1, so no `[R-ENC-04]` row fires. The tile decoded size is exactly 0x7E000000 + 1. Verifier A reads `[R-COD-07]`/L45 literally — no addressed tiles, so no tile's decoded size exceeds the bound, and §21.6 affirms the empty layer is valid — and certifies. Verifier B reads the bound as a declaration-level bound (`[R-SER-07]`: "decoded size is a function of the layer's declarations alone", and `[R-COD-07]`'s own "checkable from declarations alone") and reports reject-layer, hence nonconforming. Same bytes, certify versus reject. The same construction with T₀ = 2⁶² and four float64 channels (Q = 32) puts P·Q = 2⁶⁷ past 2⁶³ − 1 and forks `[R-ENC-04]`/L2 the same way — a second, independent instance of the same vacuity.

### RD-02 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §18.2 `[R-MTA-09]`; §17.2 `[R-COD-08]`; §7.1 `[R-CNT-25]`; §21.5 rows R3 and R4

For a user-metadata document under encoding 2, `[R-MTA-09]` requires "exactly one RFC 8878 compressed frame occupying the extent's bytes before its terminal CRC", then enumerates the carried-over `[R-COD-06]` constraints — and that enumeration omits occupancy. `[R-COD-08]`'s exact-consumption rule is written for tiles and is not carried over. Whether trailing bytes after the frame make the file nonconforming, and whether a reader must ignore the record or return the document, is left open.

> Encoding 2 stores it as exactly one RFC 8878 compressed frame occupying the extent's bytes before its terminal CRC, under the frame constraints of `[R-COD-06]` that do not reference a tile: the frame magic; no skippable frame and no second frame; no nonzero dictionary ID; no content-checksum flag.

> The constraints §17.2 states against a tile's declared decoded size do not apply, because a document has no declared size

> For every codec: the stored bytes MUST decode to exactly the decoded size — no more, no fewer — and the decode MUST consume the stored bytes exactly, with no trailing bytes past the stream, frame, or block

> R4 | A user-metadata document stored under encoding 2 breaks one of the frame constraints §18.2 carries over from `[R-COD-06]`

**Permitted readings.**

1. Reading 1 (occupancy is normative): the prose "occupying the extent's bytes before its terminal CRC" states a requirement; trailing bytes make the file nonconforming, and `[R-MTA-09]`'s catch-all "Any violation here is ignore-record" gives the reader outcome. Under this reading §21.5 is missing a row, which §21.1 makes a defect in the document.
2. Reading 2 (the enumeration is the requirement): `[R-MTA-09]` names precisely which `[R-COD-06]` constraints carry over — "the frame magic; no skippable frame and no second frame; no nonzero dictionary ID; no content-checksum flag" — and deliberately drops the tile-specific ones (declared decoded size, window size, content size). `[R-COD-08]`'s no-trailing-bytes rule is a tile rule under §17.2's "For every codec", which §18.2 does not invoke. The file is conforming and the document is returned.
3. Reading 3 (undecidable-by-decoder): occupancy is normative but the spec assigns its detection to no actor, so a reader that does not detect it returns the document and a reader that does takes ignore-record — both conforming, with divergent returned metadata.

**Picked.** Reading 1 for the verdict — the participle "occupying the extent's bytes" is doing normative work and reads as a requirement, not scenery, and the parallel tile rule `[R-COD-08]` closes exactly this hole for tiles for exactly this reason. But Reading 2 is genuinely available, because `[R-MTA-09]` goes to the trouble of listing which constraints carry over and which do not, and occupancy appears in neither list.

**Rationale.** §17.2 treats "no trailing bytes past the frame" as important enough to state separately from every other zstd constraint, and to give it its own register row (T24). §18.2 carries over the other constraints by name and leaves this one to a participial phrase, then §21.5's R4 enumerates instances that do not include it. That is the signature of a rule that was transcribed rather than re-derived.

**Byte-level?** yes — Concrete extent for a top-level user-metadata record, inline payload = `02` (encoding 2): [one valid zstd frame compressing the two ASCII bytes `{}`][the two bytes `00 00`][4-byte CRC-32C over everything preceding it in the extent]. Every enumerated constraint holds: the frame magic `28 B5 2F FD` is present, there is no skippable frame, there is no second frame, Dictionary_ID is 0, the Content_Checksum_flag is clear. The extent CRC verifies. Verifier A reads "occupying the extent's bytes before its terminal CRC" as normative and reports nonconforming. Verifier B checks the four enumerated constraints, finds none broken, decodes `{}` — a valid object, no duplicate keys, sorted trivially — and certifies. Same bytes, certify versus reject. The reader side forks too: a streaming decoder that stops at end-of-frame returns the document; a whole-buffer decoder that requires its input to be exactly one frame errors and takes ignore-record. §21.5 has no row to settle it — R3 is "stored bytes fail to decode" (they do not, for decoder A) and R4's ten instances are exactly the four enumerated frame constraints, none of which is occupancy. `[R-CNF-12]` does not neutralize this the way it neutralizes scope disputes, because the disagreement is over whether the file is conforming in the first place.

### RD-03 — CONTRADICTION

**Location.** §18.4 `[R-MTA-07]` against §21.1 (register completeness), §2.4 `[R-CNF-07]`, and §24 `[R-VEC-02]`

`[R-MTA-07]` names a detectable file-level violation — a standardized `tarn.` key appearing outside the scopes §18.4's table lists — and expressly assigns its detection to a verifier. No row of §21.2–§21.5 registers it, and no outcome class is assigned to it, contradicting §21.1's normative completeness claim and `[R-CNF-07]`'s requirement that every detectable violation carry exactly one reader outcome.

> A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document. A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`)

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document

> Every detectable violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record. `[R-CNF-07]`

> A vector whose expectation cannot be stated in those terms is testing something this specification has not defined, which makes it a finding against this document rather than a vector.

**Rationale.** This is the only detectable, verifier-assigned, expressly-named violation in the document that I could find with neither a register row nor an outcome class. §21.6's neighbouring row covers the *unrecognized* `tarn.` key (conforming); the *recognized but out-of-scope* key is a different condition and falls through both tables. `[R-MTA-07]`'s companion clause — a value "whose shape does not match its row" — is worse off still: §18.4 says a reader ignores it but never says whether the file is nonconforming.

**Byte-level?** no — No byte sequence is treated differently by two verifiers that both follow the rules. `[R-MTA-07]` is explicit that the file is nonconforming and that a verifier detects it, and §21.1 characterises an omitted row as "a defect in this document" rather than as a licence to certify — so the rule still governs and both verifiers refuse to certify a file carrying `tarn.created` in a layer's document. The reader side is settled independently: a reader ignores the key either way. What is genuinely undecidable is bookkeeping, not bytes — which outcome class the violation carries, and which §21 row a conformance vector for it would name, since `[R-VEC-02]` requires a vector to record "the outcome class (§2.4), the scope, and the §21 register row it exercises" and this condition has none of the three.

### RD-04 — AMBIGUITY

**Location.** §2.3 `[R-CNF-11]`; §18.2 `[R-MTA-09]`; §21.9 `[R-ERR-04]`

A verifier reports one of three verdicts, but the text gives no priority rule for a file that simultaneously exhibits an established violation and a requirement the verifier is unable to check. Two conforming verifiers with the same capabilities can report *nonconforming* and *cannot establish* for the same file.

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or *cannot establish* — the last where some requirement is one it is unable to check

> *Cannot establish* is not a finding that the file is nonconforming, and a verifier MUST NOT certify a file it reports that way.

> the bound is that verifier's capability and not a limit on validity (`[R-CNF-10]`), so it MUST report that it cannot establish the file's conformance rather than that the file is nonconforming

> A verifier MAY stop at the first violation it finds; one that does MUST report each scope it did not examine as *unexamined*, which is not a finding that the scope is clean.

**Permitted readings.**

1. Reading 1: an established violation dominates — the file is nonconforming as a matter of fact, and cannot-establish is reserved for files where nothing definite was found.
2. Reading 2: cannot-establish dominates — `[R-MTA-09]` says the declining verifier "MUST report that it cannot establish the file's conformance rather than that the file is nonconforming", which reads as an obligation on that verifier's whole-file report.
3. Reading 3: the verdict follows whichever condition the verifier reaches first, since `[R-CNF-11]` lets it "stop at the first violation it finds" and mark the rest unexamined — making the verdict a function of traversal order the spec never fixes.

**Picked.** Reading 1. `[R-CNF-11]` defines cannot-establish as the verdict "where some requirement is one it is unable to check", which is a statement about ignorance; where a violation has actually been established the file's nonconformance is a fact about the bytes, and §2.3's own gloss that cannot-establish "is not a finding that the file is nonconforming" implies it is the verdict for the absence of such a finding, not a veto over one.

**Rationale.** The three-verdict design is otherwise carefully built — including the deliberate routing of the unimplemented-major and experimental-MU=1 cases to cannot-establish so that verifiers cannot disagree. The one case it does not cover is the conjunction, and §21.9's resource-decline path plus `[R-MTA-09]`'s bound make the conjunction easy to construct.

**Byte-level?** no — Neither verdict certifies the file, so no byte sequence changes its accept/reject status. Construct a file whose top-level user-metadata document decodes to 20 MiB — above §21.9's 16 MiB guarantee, so `[R-MTA-09]` licenses a verifier with a 16 MiB bound to decline it and requires it to "report that it cannot establish the file's conformance rather than that the file is nonconforming" — and which also carries a layer record with codec = 0, an established L44 violation. Verifier A stops at the metadata and reports cannot-establish; verifier B examines the layer and reports nonconforming; verifier C reports both, which the three-verdict rule does not permit. The difference is consequential for an operator (fix the file versus get a better verifier) but not for bytes: no verifier certifies, and `[R-CNF-12]` already frees readers on a file that is in fact nonconforming.

### RD-05 — CONTRADICTION

**Location.** §8.1 `[R-CNT-19]` and its coverage map against §5.2 `[R-CNT-02]`, §9.7 `[R-LIF-08]`, §7.2 `[R-CNT-15]`, §20.4 `[R-WRT-08]`

`[R-CNT-19]` asserts that every field of every structure is covered by exactly one checksum, with two named exceptions, "as this map states". §5.2 makes a record extent a structure "whatever the record's type", but §8.1's map has rows only for the two registered types' extents. An unknown or experimental record type's extent is a live-committed-state structure covered by no checksum at all.

> Every field of every structure is covered by exactly one checksum — excepting the equality-checked front signature block and this map's terminal checksum fields, per §4.5 — as this map states. All checksums are CRC-32C over bytes exactly as stored. `[R-CNT-19]`

> a **structure** — a stored-tile extent, a record extent (the bytes any record's extent slot references, whatever the record's type, §7.2), the directory, or the trailer

> It checks that these occupy disjoint byte ranges, that each lies within [16, F − 64), and that each verifies against the checksum covering it (§8.1).

> Byte coverage (`[R-CNT-02]`) partitions the *live* state exactly: every byte a reader can reach belongs to one named structure.

**Rationale.** The map is complete for the two registered types (layer → tile-index region, user metadata → its extent), so the gap only opens for extension records — which §10 and §20 nonetheless treat as fully first-class and relocatable. The fix is either a map row obliging a terminal CRC on any record extent, or an explicit sentence saying an unregistered type's extent is unchecksummed and naming that in §21.7 and §22.3.

**Byte-level?** no — The over-literal reading — that such a file violates `[R-CNT-19]` and is nonconforming — is refuted by too much text for a conforming verifier to sustain: §5.2 defines a record extent as "the bytes any record's extent slot references, whatever the record's type"; §7.2 says the extent slot is an MU = 0 record's sanctioned reference to outside bytes precisely so a compactor can relocate it unparsed; §20.4 and §20.5 both describe relocating an unknown record's extent; and §21.6 lists an experimental-range MU = 0 record as conforming. So both verifiers certify, and no byte sequence's status changes. What does change is an integrity claim the document makes elsewhere: `[R-LIF-08]` requires the coverage walk to check that each claimed range "verifies against the checksum covering it", and for these ranges that check is vacuous, so corruption inside them is undetectable by reader and verifier alike — a third residue that §22.3's "Two residues are stated rather than defended" and §21.7's inventory of what no check detects both omit.

### RD-06 — AMBIGUITY

**Location.** §20.4 `[R-WRT-08]` (the stored-flags table, MU = 1 row) against §7.3 `[R-CNT-22]`, §2.3 `[R-CNF-06]`, §20.3 `[R-WRT-04]` step 4

`[R-WRT-08]` states that for a registered type the registry's fixed flags govern rather than the stored ones, then applies a table whose MU = 1 row says "Retain byte-identical. The updater MUST NOT modify the scope the record governs." The layer record's registry-fixed flags are MU = 1, PE = 1, so read literally the table forbids an updater from ever modifying any layer.

> Persistence governs every record type; only the authoritative source of the flags differs. For a type §7.3 registers, the registry's fixed flags govern rather than the stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so neither can be dropped.

> | MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs: an unknown critical record at layer scope blocks modification of that layer, leaving other layers editable

> An updater MUST satisfy every writer requirement for the bytes it produces, and additionally MUST honor the preservation obligations of Part I for records it does not understand. `[R-CNF-06]`

> Every layer whose stored-tile set, index content, or index placement this commit changes has its tile-index region re-emitted in full

**Permitted readings.**

1. Reading 1 (literal, governing flags): the table is keyed on the governing flags, which for a layer record are the registry's MU = 1 — so an updater must retain every layer record byte-identical and must not modify the scope it governs, i.e. no layer may ever be edited. This contradicts §20.3 outright.
2. Reading 2 (scoped by the cell's gloss and `[R-CNF-06]`): the MU = 1 row states preservation obligations for records the updater does not understand; a type it implements it may modify, subject to `[R-CNF-05]`. This is the intended reading.

**Picked.** Reading 2, on `[R-CNF-06]`'s "MUST honor the preservation obligations of Part I for records it does not understand" and on the MU = 1 cell's own qualifier "an unknown critical record". The defect is that the sentence introducing the table explicitly redirects registered types into it via their fixed flags, which sends the layer record — the one record every appender modifies — into a row whose first sentence forbids exactly that.

**Rationale.** Worth reporting because the table's column header reads "Stored flags" while the paragraph above it says stored flags are *not* authoritative for registered types — the two halves of the same requirement disagree about what keys the table, and the key they jointly select is the one that breaks §20.3.

**Byte-level?** no — No byte sequence's validity changes. The two readings differ only in whether a given updater is a conforming updater, and any file the permissive updater emits is conforming under both readings — §20.3 step 4 spells out re-emitting a modified layer's index in full, and `[R-WRT-05]` presupposes records that are "logically modif[ied]". The restrictive reading produces an updater that refuses to act, not one that emits divergent bytes. `[R-CNF-06]` also settles it: preservation obligations bind "for records it does not understand", and the MU = 1 cell's own gloss says "an unknown critical record at layer scope blocks modification of that layer".

### RD-07 — AMBIGUITY

**Location.** §19.1 step 4 `[R-RDR-01]` against §7.4 `[R-CNT-18]`; §4.6 `[R-ENC-15]`; §21.3 rows L4/L6/L7 and L24

§19.1 fixes that layer-name uniqueness "is decided first", over raw bytes, "whether or not each name is itself well-formed". It does not say whether the name field's *framing* — its length prefix fitting inside the layer record's inline payload — is checked before or after uniqueness. A crafted file gets reject-file under one order and reject-layer under the other.

> Uniqueness is decided first, and over the raw name bytes whether or not each name is itself well-formed — `[R-ENC-12]` makes name comparison a byte comparison, which needs no valid name — so two layers whose name fields are byte-identical are a duplicate even when neither name is valid.

> the fixed fields, the d dimension entries, the C channel entries, and the trailing fixed fields MUST lie entirely within the inline payload

> L24 | A declared region of the layer record's inline payload does not lie entirely within inline_length (overrun or truncation) | leading fixed fields (name … C)

**Permitted readings.**

1. Reading 1 (framing first): a name field that overruns inline_length is not a name field at all; `[R-CNT-18]` puts the leading fixed fields, name included, inside the inline payload, and L24 names "leading fixed fields (name … C)" as an instance. Outcome: L24, reject-layer for Y only.
2. Reading 2 (uniqueness first, literally): §19.1's "Uniqueness is decided first" is unqualified, and the comparison is over "the raw name bytes", which a reader obtains from the length prefix. Outcome: F6, reject-file.
3. Reading 3 (uniqueness first over whatever bytes are in bounds): compare `alp` against `alpha`, find no duplicate, then report L24. Outcome: reject-layer, but by a comparison over a truncated string the document never defines.

**Picked.** Reading 1. `[R-CNT-18]` states the bound as a hard parse requirement and L24 lists the name among the fields it covers, and §19.1's "first" is plainly aimed at the *validity* rules of §4.6 — the sentence's own justification is "`[R-ENC-12]` makes name comparison a byte comparison, which needs no valid name", which is about well-formedness, not about framing.

**Rationale.** The document fixed the uniqueness-versus-validity order deliberately and carefully; it did not fix uniqueness versus framing, and framing is the one that can make a name field's bytes come from outside the record. Reading 2 lets an attacker choose between reject-file and reject-layer for a victim's file by placing two bytes in an unrelated record header, which is exactly the kind of cross-structure leverage §7.2's no-embedded-offsets rule exists to prevent.

**Byte-level?** no — The file is nonconforming under both orders, and `[R-CNF-12]` expressly permits a reader to reject a nonconforming file entire upon detecting any violation, so the reader that rejects the whole file is conforming regardless of which order is right; §24's note says the same thing about vectors. Both verifiers also agree the file is nonconforming. Concrete construction, for the record: layer record X with name length prefix 5 and bytes `alpha`; layer record Y later in the same sequence with inline_length = 3 and name length prefix 5 followed by only the three bytes `alp`, positioned so that the next 24 bytes — Y's successor's record header — begin with the type-field bytes `68 61` ("ha"). A reader that compares the declared five name bytes before bounds-checking reads `alpha` and reports a duplicate at file scope (F6, reject-file); a reader that applies `[R-CNT-18]`'s "MUST lie entirely within the inline payload" first reports L24 at layer scope and serves layer X. Different scopes, same bytes — but not different accept/reject obligations.

### RD-08 — OBSERVATION

**Location.** §6.2 `[R-CNT-05]` against §9.2 `[R-LIF-02]` step 5; §2.3 `[R-CNF-02]` and `[R-CNF-05]`

`[R-CNT-05]` says the pre-trailer pad's length is bounded "only through step 5 of the commit protocol" and in the same sentence that "a longer gap is conforming, and no conforming commit produces one". Step 5 is a MUST binding a writer and its effect is visible in the emitted bytes, yet §2.3's list of writer obligations that govern conduct rather than output does not include it — so a writer emitting a 128-byte pre-trailer pad emits a conforming file while violating a MUST.

> this specification does not constrain their content, and bounds their number only through step 5 of the commit protocol, which pads to the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming, and no conforming commit produces one.

> (5) append the pad to the next 64-byte boundary — zeroed by advice, `[R-CNT-03]` — and the new trailer

> A few obligations this specification places on writers govern their *conduct* rather than their output — where a value is published, or which registry version a writer targets (§10.3, §18.3) — and a file is never nonconforming by virtue of one

> A writer MUST emit only conforming files. `[R-CNF-05]`

**Rationale.** §2.3 is otherwise scrupulous about naming every conduct-only writer obligation, including the one-off §6.3 flags = 0 case, precisely so that the file predicate stays clean. `[R-LIF-02]` step 5 is a fourth such obligation and is not on the list, which leaves `[R-CNF-05]` ("a writer MUST emit only conforming files") and `[R-LIF-02]` disagreeing about what makes a writer conforming. Cheap to fix by adding step 5's pad length to §2.3's enumeration.

**Byte-level?** no — Both verifiers certify. File conformance is "a pure predicate on bytes" (`[R-CNF-02]`), `[R-CNT-05]` states outright that a longer gap is conforming, §21.2 registers only a *structure* in the gap (F9) and not an over-long gap, and §21.1's register completeness is normative for MUST-level detectable conditions — three independent signals that the bytes are fine. What is left open is only whether the *writer* is a conforming writer, which no byte sequence records.

### RD-09 — OBSERVATION

**Location.** §21.7 `[R-ERR-01]` second paragraph against §21.1; §20.4 `[R-WRT-05]`/`[R-WRT-08]`; §20.5 `[R-WRT-06]`; §9.2 `[R-LIF-02]`

§21.1 calls §21.7 "the inventory of what fails" the detectability gate, and §21.7's second paragraph presents a closed three-item list of obligations omitted from the register because a single file exhibits no witness. At least six further single-file-undetectable obligations are absent from that inventory.

> A second set of obligations is omitted from the register because a single file exhibits no witness of their violation. Committed-prefix immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets in its own payload is opaque by construction.

> detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

> an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify

> It MUST mint a fresh file_id for the output — a new draw under §9.3's randomness advice, not merely a value compared against the input's

**Rationale.** Missing from the inventory: `[R-WRT-05]`'s byte-identical re-emission; `[R-WRT-08]`'s condition on dropping an MU = 0/PE = 0 record only in a commit that independently changes the record's scope; `[R-WRT-06]`'s fresh-file_id and generation-1 obligations for a compactor; `[R-WRT-07]`'s reference-array equality across a compaction; `[R-LIF-02]`'s two storage barriers and its step ordering; and `[R-CNT-08]`'s obligation on an updater to copy unknown ignore-lane bits forward. Each is a MUST, each is verifier-relevant in principle, and each has exactly the property §21.7 was written to record. The document already demonstrates the discipline elsewhere — `[R-SLB-04]` and §7.4's nesting prohibition each carry an explicit note saying why they have no register row — so the gap here reads as an oversight rather than a policy.

**Byte-level?** no — Nothing turns on it. Each omitted obligation is undetectable in a single file under every reading, so no verifier can reject on it and no writer's byte choices change. The defect is a completeness claim the document makes about itself and does not meet.

### RD-10 — OBSERVATION

**Location.** §17.2 `[R-COD-05]` and `[R-COD-08]`; §21.7 `[R-ERR-01]`; §22.3 `[R-SEC-04]`; §23.2 `[R-PRV-03]`

A raw RFC 1951 DEFLATE stream ends on a bit boundary. The residual high bits of the stream's final byte are inside a live, checksummed structure, are consumed by no decoder, and are constrained by no rule in this document — up to seven bits of free content per codec-2 tile, invisible to every check.

> **Codec 2 — deflate.** The stored bytes are exactly one DEFLATE compressed data stream as defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952) wrapper.

> the decode MUST consume the stored bytes exactly, with no trailing bytes past the stream, frame, or block

> Slack is covered by no checksum (§8.1) and constrained by no rule: corruption confined to it is invisible to reader and verifier alike

> Two residues are stated rather than defended.

**Rationale.** §22.3 names exactly two unconstrained residues — slack, and trailer-mimicking payloads — and §21.7 states plainly what no check detects. These bits are a third: unlike slack they sit inside a structure the coverage walk claims and a checksum covers, so the intuition that "every byte a reader can reach belongs to one named structure" with fully constrained content does not hold. Worth a sentence in §21.7 or §17.2 for the same reason §14.5 pins padding content: it is a deterministic-output and disclosure surface, not a decoding hazard.

**Byte-level?** no — Two implementations cannot disagree about any byte. `[R-COD-08]`'s exact-consumption rule speaks of "trailing bytes", and no whole byte trails a stream whose final block ends within the last byte, so both verifiers accept and both decoders produce the same decoded tile image. Two files differing only in those bits are both conforming with identical reference arrays — writer freedom `[R-CNF-05]` already grants ("two conforming writers given identical input MAY produce different conforming files"), and Appendix G closes it by pinning the encoder. A whole extra byte after the byte holding the final bit does trail, and is T24.

### RD-11 — OBSERVATION

**Location.** §6.2 (generation valid values); §9.2 `[R-LIF-02]` step 5; §9.3 `[R-LIF-03]`; §4.2 `[R-ENC-03]`

The generation counter is capped at 2⁶³ − 1 by the universal value domain and must increase by exactly 1 per commit. A file at generation 2⁶³ − 1 therefore admits no further commit, and the document nowhere states this terminal condition or what a writer should do at it.

> | 16 | 8 | u64 | generation | semantic | 1 ≤ generation ≤ 2⁶³ − 1 (`[R-ENC-03]`) |

> and the new trailer, with generation one greater than the prior trailer's and committed_file_length equal to the new end

> Each commit's trailer carries generation g ≥ 1, increasing by exactly 1 per commit

> a compacted file is a whole-file rewrite under a new file_id by definition (`[R-LIF-01]`), and generation 1

**Rationale.** Not a defect in behavior, only in coverage: §9.4 and §20.3 both tell a writer how to fail safely when the trailer will not validate, and neither covers the one failure a correct writer can walk into by doing everything right for long enough. One sentence in §9.3 pointing at compaction would close it.

**Byte-level?** no — Fully decided, just unstated. A trailer carrying generation 2⁶³ would fail `[R-CNT-06]`'s "1 ≤ generation ≤ 2⁶³ − 1" gate at open in every reader (F3, F13's neighbourhood), so no implementation could disagree about the bytes. The only conforming path from a saturated file is compaction, which resets to generation 1 under a fresh file_id — but §20.5 presents compaction as a slack-reclamation operation and never as the counter's escape hatch.

### RD-12 — OBSERVATION

**Location.** §24 `[R-VEC-04]`

`[R-VEC-04]` requires every reject-layer or reject-tile vector to carry an "intact sibling — another layer, or another tile of the same layer". For a reject-layer vector the second disjunct cannot serve the stated purpose, since every tile of the rejected layer is unusable.

> Every vector whose recorded outcome is reject-layer or reject-tile is built inside a file that also carries an **intact sibling** — another layer, or another tile of the same layer — whose decoded content the manifest records

> Without the sibling a vector cannot distinguish a reader that scopes its refusal from one that rejects the file entire

**Rationale.** The disjunction should be distributed: another layer for reject-layer vectors, another tile of the same layer (or another layer) for reject-tile vectors. As written, roughly fifty §21.3 rows can be built with a sibling that proves nothing.

**Byte-level?** no — This constrains how the conformance corpus is built, not what any implementation emits or accepts. No file's verdict changes; a corpus builder that takes the disjunction literally produces a reject-layer vector with no usable sibling and so cannot distinguish a scope-respecting reader from one exercising `[R-CNF-12]`'s whole-file licence — which is the exact failure `[R-VEC-04]` was written to prevent.
