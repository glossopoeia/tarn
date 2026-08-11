# Cleanroom round 7 — writer walk

**Access disclosure.** spec/tarn.md only

## Walk summary

I implemented the writer on paper in four passes.

(1) Creation from §§4–8 alone. I derived the 128-byte minimal file without looking at Appendix A: front block 89 54 41 52 4E 0D 0A 1A + 8 zero bytes; directory at 16 = CRC-32C of zero bytes = 00 00 00 00 (dir_length 4); 44 bytes pad; trailer at 64. Trailer fields all determined by §6.2 except three I had to guess: file_id (any nonzero), version_minor ([R-CNT-26] is a SHOULD), and dir_offset/dir_length placement. I implemented CRC-32C from §4.5's parameters and confirmed the check vector (0xE3069283 / 0x00000000), the all-sentinel full-segment constant (0xEECB3BB2), and Appendix A's trailer CRC over bytes [0,60): I computed 0xE00938D2 → bytes D2 38 09 E0, matching the printed dump exactly. With Appendix A's stated file_id, every one of the 128 bytes I derived matched. I found no guess I could not justify from §§4–8; Appendix A is byte-correct.

(2) A one-layer file. §7.4's inline payload is fully packed and unambiguous: (1+len) name, layout, linearization u16, codec u16, filter u16, A/S/A_slab u64s, rank u8, C u16, then d dimension entries and C channel entries, then index_encoding, entry_count, crc_of_crc_array, then sub-records to the end. Index region = entry_count×20 + ⌈entry_count/2¹⁶⌉×4, cross-checked by [R-CNT-17]. I re-derived every worked example in §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §17.3 and §20.3 and all are arithmetically correct. §21.2–§21.5 sum to 125 rows, and the Instances cells sum to exactly 242, matching [R-ERR-02].

(3) Append, commit shapes, slack. §20.3's procedure is complete and deterministic given a touched-layer set. Two questions I could not close from the text: whether a commit may reuse the previous generation's directory region and append only pad+trailer (WR-02, byte-level), and whether an appender may relocate an untouched layer's index (WR-06).

(4) Torn-write recovery. §9.6 is implementable as written: probe 64-aligned offsets downward from the largest o with o+64 ≤ physical length, require magic + CRC + committed_file_length = o+64, re-verify the truncation whole, continue past failures, report the candidate and the reject count. I found no gap here.

The divergence catalogue is finding WR-11.

## Findings (11)

### WR-01 — CONTRADICTION

**Location.** §20.4 [R-WRT-08] persistence table, MU = 1 row; against §20.3 [R-WRT-04] step 4, §20.4 first paragraph [R-WRT-05], §9.2 [R-LIF-02], Appendix H

§20.4's persistence table is declared to govern every record type with the registry's fixed flags authoritative for registered types; the layer record is a registered type with MU = 1, so the MU = 1 row's obligation — 'Retain byte-identical. The updater MUST NOT modify the scope the record governs' — forbids an updater from ever modifying any layer, which contradicts §20.3's entire append procedure and §20.4's own opening sentence.

> Persistence governs every record type; only the authoritative source of the flags differs. For a type §7.3 registers, the registry's fixed flags govern rather than the stored ones (`[R-CNT-22]`)

> | MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs: an unknown critical record at layer scope blocks modification of that layer, leaving other layers editable

> | 0x0001 | layer | file (container for layer scope) | MU = 1, PE = 1 |

> In the new complete directory, an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify ... a record it modifies is new output under its writer obligations (`[R-CNF-05]`).

**Permitted readings.**

1. The table binds every record type including registered ones, so an updater may never modify a layer (no conforming append that touches a layer's tiles, index, or record exists).
2. The table binds only records the updater does not understand — the reading Appendix H states ('never modifies a scope governed by an unknown critical record') and [R-CNF-06] scopes preservation to 'records it does not understand'.
3. The table binds every type, but 'retain' is defeated by §20.4's opening dichotomy: a record the updater logically modifies is not 'retained', so the MU = 1 row only governs records the commit leaves alone.

**Picked.** Reading 2 (unknown critical records only), because Appendix H states it explicitly, [R-CNF-06] scopes preservation to records not understood, and reading 1 makes §20.3, §9.2 and §20.5 unreachable.

**Rationale.** The word 'unknown' appears only in the row's explanatory clause, not in its obligation; the sentence introducing the table expressly extends it to every type. A writer implementer following the table literally would refuse every layer-modifying commit.

**Byte-level?** no — No byte sequence changes status. Under both readings the set of conforming files is identical — file conformance is a pure predicate on bytes (§2.3 [R-CNF-02]), and a generation g+1 file with a modified layer record and re-emitted index is conforming however it was produced. No reader or verifier verdict differs; the divergence is entirely in whether an updater is permitted to offer the operation. I can name no byte sequence two implementations would accept/reject differently.

### WR-02 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §9.2 [R-LIF-02] step 3; §3.1 (definition of *directory*); §5.1 [R-CNT-01]; §6.2 [R-CNT-05]/[R-CNT-06]; §9.7 [R-LIF-08]; §21.2 register

Nothing among the file-level requirements forbids a commit from pointing its new trailer at the *previous* generation's directory region and appending only the pad and a 64-byte trailer. Whether such a file is a conforming file — and therefore whether a verifier certifies it — is not decided by the text.

> A writer performing a commit MUST, in order: ... (3) append the new complete directory — re-emitting every retained record per §20's preservation rules — followed by its CRC

> Each commit appends a *complete* directory — never a delta — so a file contains one directory per generation; unqualified, *the directory* means the live generation's.

> Writers MUST place the directory so that no structure lies between its end and the trailer.

> A verifier checking `[R-CNT-02]`'s partition walks the live state only. ... Bytes the walk does not reach are slack

**Permitted readings.**

1. Nonconforming file: §3.1's 'one directory per generation' and §5.1's 'each generation's directory' are file-level structural requirements, so a generation whose trailer reaches an earlier generation's directory violates them (even though §21 registers no row and §9.7's walk cannot see it).
2. Conforming file, nonconforming writer: [R-LIF-02] step 3 binds the actor only; file conformance is a pure predicate on bytes (§2.3 [R-CNF-02]) and every byte-testable rule — [R-CNT-01], [R-CNT-02], [R-CNT-05], [R-CNT-06], [R-CNT-13], [R-LIF-08] — is satisfied.
3. Conforming file and conforming writer: step 3's 'append the new complete directory' is read as an obligation that the live directory be complete and current, which it is; re-emitting identical bytes would be pure waste and §5.2's rationale disclaims any interest in which commit wrote which bytes.

**Picked.** Reading 2. §2.3 is explicit that conformance of a file is a predicate on bytes and does not depend on any writer, and no byte-testable requirement is broken; but step 3 is an unqualified MUST on the writer, so a conforming writer may not produce it.

**Rationale.** This matters to a writer: it is the difference between a 64-byte 'touch' commit and one that re-emits a directory that can run to megabytes at 65,536 layers (§21.9's note). §9.7 explicitly declines to reconstruct history, so a verifier walking only the live state has no basis to refuse.

**Byte-level?** yes — Concrete sequence: take Appendix A's 128-byte file verbatim and append 64 bytes — the same trailer with generation = 2, committed_file_length = 192 (C0 00 00 00 00 00 00 00), and its CRC recomputed. The result is 192 bytes; dir_offset = 16, dir_length = 4, 20 ≤ 192 − 64; the live state is front block + [16,20) + [128,192); slack is [20,128) = 108 bytes, which contains the superseded generation-1 trailer. Under reading 2 a verifier MUST certify this file; under reading 1 it MUST report nonconforming. Two conforming verifiers therefore return opposite verdicts on a named byte sequence, and a conforming writer under reading 3 may emit it while one under reading 2 may not.

### WR-03 — AMBIGUITY

**Location.** §6.3 [R-CNT-08]; §20.5 [R-WRT-06]; §20.1 [R-WRT-01]

A compactor emits a complete file in one commit at generation 1 with a fresh file_id — §20.1's definition of a *creator* — yet §6.3 obliges 'a writer creating a file under this text' to write flags = 0 while §20.5 obliges the compactor's output trailer to carry the input's unknown ignore-lane bits forward. Which governs a compactor is not stated.

> In this specification's text no flag bits are defined: a writer creating a file under this text MUST write flags = 0, but a set ignore-lane bit is not a file-conformance violation

> The output trailer copies the input's unknown ignore-lane flag bits forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the input's version_minor — a compactor cannot know which minor version defined an ignore-lane bit it does not implement, so it does not lower the floor beneath one.

> - **creator** — emits a complete file in one commit, generation 1: the minimal conforming writer.

**Permitted readings.**

1. 'Creating a file under this text' means creating a file none of whose features exceed this text; a compactor of a file carrying ignore-lane bits is not doing that, so §20.5 governs and the bits are copied.
2. 'Creating a file' is the tier test: a compactor emits generation 1 and is therefore a creator, so flags = 0 governs and §20.5's copy-forward clause conflicts with [R-CNT-08].
3. [R-CNT-08]'s clause is aimed at an appender-vs-creator distinction that §20.5 simply overrides for compaction, the later and more specific rule winning.

**Picked.** Reading 1/3 (the bits are copied forward), because §20.5 states the compactor case specifically and gives the reason, and because §2.3 already declares a set ignore-lane bit not to be a file-conformance violation, so the loss of a feature-floor signal is the only cost.

**Rationale.** A writer implementer building a compactor must decide this at the point of emitting the trailer; the two readings emit different flag words for the same input.

**Byte-level?** no — The emitted trailers differ (flags = 0 vs flags = copied bits), but both files are conforming: §6.3 and §2.3 [R-CNF-02] jointly declare a set ignore-lane bit not to be a file-conformance violation, and [R-CNT-08] obliges every reader to ignore bits 16–31 outright. No reader's or verifier's verdict on any byte sequence changes, and no byte sequence becomes acceptable or unacceptable. The divergence is a writer-conduct one only.

### WR-04 — CONTRADICTION

**Location.** §18.4 [R-MTA-07]; against §21.1 (normative completeness), §2.4 [R-CNF-07], §21.5

[R-MTA-07] expressly declares a file carrying a standardized `tarn.` key outside its listed scope to be nonconforming and verifier-detectable, but the condition has no row in §21.2–§21.5, whose completeness §21.1 declares normative; and its assigned handling — the reader ignores the key, not the record — is not one of the four reader outcomes [R-CNF-07] requires every detectable violation to carry.

> A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document. A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`)

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document

> Every detectable violation named by this specification is assigned exactly one **reader outcome**: reject-file, reject-layer, reject-tile, or ignore-record. `[R-CNF-07]`

**Rationale.** The comparable verifier-only, reader-behavior-unchanged violations are all registered — unsorted metadata members as F30/L49 and a registered type's stored flag mismatch as F31/L50 — and §21.6's closing paragraph explicitly re-homes those two from the not-a-violation table into the register on exactly this precedent. [R-MTA-07]'s violation has the identical shape and was not given the same treatment. It is also not excused by §21.7: it is detectable in a single file. §21.6 does list an unrecognized `tarn.` key as conforming, but that is [R-MTA-06]'s case (a conduct rule §2.3 names by section), a different condition.

**Byte-level?** no — §21.1 fixes the outcome: 'where a row and the rule it cites diverge, the rule governs', and here the rule states the verdict outright — the file is nonconforming and a verifier detects it. So a verifier handed a file whose layer-scope user-metadata document carries `tarn.created` (a file-only key) must report nonconforming under both the register-as-written and the rule; there is no byte sequence two implementations would classify differently. What is missing is the register row and the corresponding conformance vector ([R-ERR-02] would require one), plus an outcome class for [R-CNF-07]'s purposes — a documentation and corpus defect, not a byte one.

### WR-05 — CONTRADICTION

**Location.** §11.1 Rationale and §13.3 'Note — sparse writing'; against §20.3 [R-WRT-04] step 4 and §11.4 [R-GEO-06]

Two places state that extent growth is a metadata-only operation. It is metadata-only only when no grid count changes; any growth that increases some ⌈Eᵢ/Tᵢ⌉ changes entry_count, renumbers disk ordinals, and forces the layer's whole tile-index region to be re-emitted — the single most expensive thing a commit does.

> Empty layers serve schema-first workflows: declare layers at creation, grow extents as data arrives — extent growth is a metadata-only operation under this specification's commit model.

> Extent growth is a metadata-only operation (§11.1), so declare-then-fill workflows append tiles as data arrives, generation by generation (§9).

> entries new to this generation (added tiles, grown extents) emitted per §15, and every other entry byte-identical at its disk-ordinal position (a geometry change renumbers ordinals, `[R-GEO-06]`)

**Rationale.** Worked case: a layer with E = (1000), T = (256) has G = 4, entry_count = 4. Growing E to 2000 gives G = 8 and entry_count = 8, so the index region must be re-emitted at a new offset with four new sentinel entries, the layer record's extent slot and crc_of_crc_array change, and the old region becomes slack. For a rank-2 layer, growing the *first* dimension renumbers every existing tile's spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ, so every entry moves within the region. Only growth that leaves every Gᵢ unchanged (growth into existing edge padding) is genuinely metadata-only — and that case works precisely because [R-SER-05] already forced padding positions to hold fill. The schema-first workflow the rationale sells is exactly the one §20.3's own note warns costs 'about 20 MB of index' per touch on a 10⁶-tile layer.

**Byte-level?** no — Both offending statements sit in blocks labelled *Rationale* and *Note*, which §2.1 [R-CNF-01] makes non-normative, and the normative rules (§20.3 step 4, [R-GEO-06], [R-CNT-17]) unambiguously fix the bytes: entry_count equals the geometry-derived addressed-tile count, entries are in disk-ordinal order, and the region's length follows the formula. A writer that believed the rationale and left the index untouched would emit a file failing [R-CNT-17], which is L22/L23 — already registered and already rejected by every reader at layer access. No two conforming implementations can disagree about bytes here; the defect is that the document misstates its own cost model in the place a writer plans against.

### WR-06 — AMBIGUITY

**Location.** §20.3 [R-WRT-04] step 4; §20.4 [R-WRT-05]

It is not stated whether an appender MAY relocate the tile-index region of a layer whose stored-tile set, index content and record the commit does not otherwise change — for example to place it beside a newly written sibling.

> Every layer whose stored-tile set, index content, or index placement this commit changes has its tile-index region re-emitted in full

> A layer whose record alone changes keeps its extent slot, pointing at the existing region.

> In the new complete directory, an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify; a record it modifies is new output under its writer obligations (`[R-CNF-05]`).

**Permitted readings.**

1. Forbidden: 'index placement this commit changes' is a *description* of what triggers re-emission, not a permission to change placement at will; combined with 'keeps its extent slot' and [R-WRT-05]'s byte-identical obligation, an untouched layer's index must stay where it is.
2. Permitted: an appender may elect to treat the layer record as logically modified, which makes it 'new output under its writer obligations'; it then re-emits the index at a new offset, re-points the slot, and the old region becomes slack. [R-SLB-05]'s placement freedom and [R-WRT-07]'s explicit grant to a compactor support relocation being a normal operation.
3. Permitted only when the commit already changes that layer's record for another reason, by analogy with §20.4's MU = 0/PE = 0 drop rule ('only in a commit that independently changes the scope the record attaches to').

**Picked.** Reading 2. [R-WRT-05]'s obligation is expressly conditioned on the record being one the updater 'does not logically modify', and nothing makes relocation a prohibited modification; the cost — the old region becomes slack — is borne by the writer, which §16's [R-SLB-05] already says is the only sanction for wasteful placement.

**Rationale.** This is a live choice for an appender that wants slab locality across a multi-layer commit. Under reading 1 it must leave the layer's index where an earlier generation put it and can never restore locality short of full compaction.

**Byte-level?** no — The resulting file is conforming under either reading: the relocated region is a live record extent, disjoint, checksum-consistent, and the superseded region is slack that [R-CNT-21] leaves unconstrained and [R-LIF-08] merely counts. No register row distinguishes the two files, so no reader or verifier reaches a different verdict. Two appenders would emit different bytes for the same request, but that divergence is already licensed generally by [R-CNF-05]; what is undecided is only whether one of them is a conforming updater.

### WR-07 — AMBIGUITY

**Location.** §9.7 [R-LIF-08]; §21.2 row F36 Instances; against §7.4 (layer record extent slot addresses the tile-index region) and §21.3 row L19

§9.7's coverage walk and F36's instance list both enumerate 'record extents' and 'tile-index region(s)' as separate claimants, but for a layer record they are the same bytes — the layer record's extent slot *is* the index region. Read literally, the walk claims those bytes twice and every file with a non-empty layer fails the disjointness check.

> From the live trailer it enumerates the live directory and its records, each record's extent, and each layer's tile-index region together with that region's non-sentinel entries ... It checks that these occupy disjoint byte ranges

> | F36 | ... | stored-tile extents; tile-index regions; record extents; sub-record extents; directory region | verifier | certification |

> A layer record's extent slot addresses the layer's tile-index region (§15); a layer with zero addressed tiles has extent (0, 0).

**Permitted readings.**

1. Literal: the enumeration lists two claimants over one byte range, so the disjointness check fails on every layered file — plainly not intended and self-refuting.
2. 'Record extents' means the extents of records other than layer records (non-layer top-level records and sub-records), and 'tile-index region' names the layer record's extent under its structural name; one claimant per range.

**Picked.** Reading 2, on the evidence of §21.3's L19, whose instance list is 'stored-tile extents; tile-index region; layer sub-record extents' — it names the index region and the sub-record extents but pointedly not a separate 'layer record extent', which is the dedup made explicit.

**Rationale.** A single structure cannot overlap itself under any sensible construction of [R-CNT-13]'s 'no two extent slots and no two structures overlap' — there is one slot and one structure. But a verifier implemented straight from §9.7's sentence would build two claim records from one slot.

**Byte-level?** no — The literal reading is self-refuting: it would make Appendix A's own worked model of a layered file nonconforming and would leave [R-CNT-02]'s partition unsatisfiable for every file with entry_count > 0, which §21.6 and §24 both presuppose is a normal case. No implementer can sustain it, and L19's instance list disambiguates. So there is no byte sequence over which two conforming verifiers could actually disagree; the defect is an imprecise enumeration.

### WR-08 — OBSERVATION

**Location.** §21.7 [R-ERR-01] second paragraph; §21.1 ('§21.7 the inventory of what fails it'); §15.1 [R-IDX-01]; §6.3 [R-CNT-08]

§21.1 makes §21.7 the inventory of obligations that escape the register for want of detectability, but §21.7's list omits at least two: [R-IDX-01]'s requirement that index entries be in disk-ordinal order, and [R-CNT-08]'s updater obligation to copy unknown ignore-lane bits forward.

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document, detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

> A second set of obligations is omitted from the register because a single file exhibits no witness of their violation. Committed-prefix immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets in its own payload is opaque by construction.

> The entry for the tile with disk ordinal k (§11.4) is the k-th entry, at region byte 20·k; entry order is disk-ordinal order, so a planar layer's entries group channel-major. `[R-IDX-01]`

> An updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear them

**Rationale.** [R-IDX-01]'s ordering sits in exactly the class §21.7 already names for [R-GEO-06] and [R-SER-01]: a permuted entry array is structurally impeccable — every entry well-formed, every segment CRC correct, every stored extent in bounds and non-overlapping — and no check in §21 detects it (only a slab declaration would, incidentally, via L42). [R-CNT-08]'s copy-forward has no single-file witness at all, since a reader cannot know which bits the input carried. Elsewhere the document is scrupulous about this bookkeeping: §7.4's note explains why the nesting prohibition has no row, §16.2's note explains why [R-SLB-04] has none, and §9.5's note explains why post-commit residue has none. These two got no such note and no place in §21.7.

**Byte-level?** no — Nothing in the byte layout is at stake. [R-IDX-01] already fixes the entry at region byte 20·k unambiguously, so a conforming writer knows exactly what to emit and a conforming reader knows exactly where to look; the omission concerns only whether the document accounts for the fact that no one can catch a writer that gets it wrong. Adding both to §21.7 would change no file's status and no implementation's behavior.

### WR-09 — OBSERVATION

**Location.** §2.3 [R-CNF-03] second sentence; against §21.6's closing paragraphs

§2.3's parenthetical cross-reference does not match what §21.6 says. §2.3 attaches three qualifiers to the reader's acceptance obligation and then claims §21.6's closing paragraph 'names those two exceptions'; §21.6 in fact names an unimplemented format major and an *experimental-range* record type with MU = 1, and names neither the §21.9 resource-limit qualifier nor the broader class §2.3 states.

> A reader MUST accept every conforming file of a format major version it implements, carrying no record of a type it does not implement with MUST_UNDERSTAND = 1, and none of whose values exceeds the minimum guarantees of §21's limits table (§21.6's closing paragraph names those two exceptions)

> Two distinct cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement** ... The second is an **experimental-range record type carrying MU = 1**

**Rationale.** Three separable mismatches. (a) §2.3 lists three carve-outs — implemented major, no unimplemented MU = 1 type, within §21.9's guarantees — and calls them 'those two'. (b) §21.6's first case (unimplemented major) is one §2.3 has already handled in its own leading clause, so the sets are offset by one. (c) §2.3's second qualifier is 'a type it does not implement with MUST_UNDERSTAND = 1', which covers reserved-range types and types a later minor version registers, whereas §21.6 restricts its second case to the *experimental* range — and reserved-range MU = 1 types are registered as violations (F38, L25), which is a materially different disposition. A reader implementer reconciling the two has to work out that §2.3's list is the operative one.

**Byte-level?** no — Every underlying disposition is stated unambiguously elsewhere and none of them is in doubt: F21 fixes the unimplemented major, F38/L25 fix reserved-range MU = 1 (violation, reject), §21.6's table and closing fix experimental MU = 1 (conforming file, reader refuses), and [R-ERR-04] fixes the resource-limit refusal and its required diagnostic. The parenthetical is a finding aid that miscounts; correcting it changes no file's conformance and no reader's outcome on any byte sequence.

### WR-10 — OBSERVATION

**Location.** §7.4 layer-record layout table; §1 'How to read this document'; §4.7 [R-ENC-16]

§7.4's layout table gives Field/Type/Constraint but no byte offsets and no taxonomy class, though §1's rubric and [R-ENC-16] presuppose every field carries one; and no field anywhere in the document is classified *informative*, leaving that third class defined but uninstantiated.

> Layout tables in this document give, per field: byte offset within the structure, size, type, name, taxonomy class, and valid range.

> Every field this specification defines is classified **structural**, **semantic**, or **informative**. A field classified informative MUST NOT affect how any byte is located or decoded, and a reader MUST NOT alter decoding based on it; each informative field's definition states what a reader does when it contradicts the data it describes. `[R-ENC-16]`

**Rationale.** The omission of offsets in §7.4 is defensible and probably deliberate — the payload is variable-length, so offsets are not constants — but the class column is not, and §7.4 is the largest structure in the format. Classes are recoverable from prose for some fields (§11.4 calls linearization structural, §12 calls the sample type structural, §13.1 calls fill semantic) and are simply absent for others: layer name, A, S, A_slab, rank d, channel count C, dimension extents and tile extents, entry_count, crc_of_crc_array. Separately, [R-ENC-16] carries an obligation ('each informative field's definition states what a reader does when it contradicts the data it describes') that no field in this document discharges, because no field is informative — the closest analogues, `tarn.stats` and `tarn.axes`, are metadata keys governed by [R-MTA-08], not fields.

**Byte-level?** no — The taxonomy is a documentation device with exactly one normative consequence — [R-ENC-16]'s prohibition on informative fields affecting decoding — and that consequence has no subject in format major 1. Every §7.4 field's decoding role is fully fixed by the rules that use it, so a writer emits and a reader parses identical bytes whatever class label is attached. The only cost is to a later minor version that wants to add an informative field and finds no worked precedent.

### WR-11 — OBSERVATION

**Location.** Whole document; catalogue anchored at §2.3 [R-CNF-05], §5.2, §9.2, §16, §17, §18.2, §20.5, Appendix G

This is the requested catalogue of legitimate byte divergence, not a defect claim: every place two conforming writers given byte-identical logical input may emit different bytes, with the rule licensing each. Twenty-five licensed axes, two undecided (WR-02, WR-06), and nine places that look free but are not.

**Rationale.** LICENSED DIVERGENCE — root licence [R-CNF-05]: 'this specification does not promise canonical bytes, and two conforming writers given identical input MAY produce different conforming files.'
1. file_id — any nonzero u64 (§6.2 table); [R-LIF-03]'s cryptographic draw is a SHOULD.
2. version_minor — [R-CNT-26] is a SHOULD, and [R-CNT-07] forbids readers to gate on minors, so any u16 rides.
3. Ignore-lane flag bits 16–31 — [R-CNT-08] plus [R-CNF-02]: a set bit 'is not a file-conformance violation'.
4. Placement and order of every structure in the file — [R-SLB-05] ('any non-overlapping byte positions, in any order'), [R-LIF-02] step 2 ('in any order'), [R-WRT-02] ('placement is otherwise free').
5. dir_offset — any value ≥ 16 meeting §6.2's bounds; a consequence of 4.
6. Size of the gaps left between structures — [R-SLB-05]; the bytes become slack under §5.2.
7. Content of slack bytes — [R-CNT-03] is a SHOULD; [R-CNT-21]: 'its content is unconstrained, and no conformance requirement applies to it.'
8. Order of records within the directory — [R-CNT-14]; Appendix G item 3 confirms it 'is otherwise free to vary'.
9. Tile extents Tᵢ — §11.3's note: 'Tile extents are a writer's choice, and this specification imposes none.'
10. Channel layout, interleaved vs planar — [R-SER-09]; §14.4's note gives the byte consequence for bool.
11. Codec, 1 through 4 — [R-COD-03]; all four core.
12. Filter, 1 or 2 — [R-COD-09]; both core.
13. Encoder output within a chosen codec — Appendix G item 1: RFC 1951 and RFC 8878 'constrain what a decoder accepts, not how an encoder chooses blocks, matches, or tables'. Byte-identity across implementations is unattainable for codecs 2–4.
14. zstd Frame_Content_Size present or absent, and the declared window size anywhere ≤ decoded size — [R-COD-06]: 'The frame content-size field MAY be present.'
15. Sentinel vs stored for a tile whose every sample equals fill — §3.1/§13; Appendix G item 6 closes this only for the profile, which proves it open in the core.
16. The fill bytes recorded when the caller chooses none — [R-TYP-10] is a SHOULD ('A writer that defaults differently still emits a conforming file').
17. Whether alignment A, or slab S with A_slab, is declared and at what value — §16.1/§16.2 MAY; Appendix G item 5.
18. Commit batching: the same content as one commit or many — §9; Appendix G item 4.
19. Unicode normalization form of layer, dimension and channel names — [R-ENC-14] is a SHOULD, and [R-ENC-13] makes NFC and NFD distinct names.
20. User-metadata JSON serialization — whitespace, number formatting, and \uXXXX escaping (§18.2 makes key identity the decoded string). [R-MTA-05]: sorted members make 'one writer's output reproducible ... it does not make two writers' output identical.'
21. Metadata encoding 1 vs 2 — [R-MTA-03]; both core.
22. Presence of the optional file-scope and per-layer user-metadata records and of any standardized key — §18.1, §18.4 ('Each is OPTIONAL and advisory').
23. Dimension declaration order for column-major producers — §11.4's note; borderline, since it changes the declared array.
24. Which commit each structure lands in, and hence every absolute offset — §9.
25. A compactor's placement of everything it carries — [R-WRT-07]: 'free to place structures anywhere §5.2 admits.'
UNDECIDED: reuse of the prior generation's directory (WR-02); relocation of an untouched layer's index (WR-06).
NOT DIVERGENCE, though it looks like it: pre-trailer pad length — §6.2 says 'a longer gap is conforming, and no conforming commit produces one', so the file space is wider than the writer output space but two conforming writers still both pad to the next 64-byte boundary, and to zero bytes when the directory already ends aligned. The all-sentinel full-segment CRC is a fixed value; [R-IDX-05] licenses skipping the computation, never a different value, and 'Equality with the constant licenses nothing for readers.' Padding-position content and pad bits are pinned to fill by [R-SER-05]. Interleaved bool bytes are 0x00 or 0x01 only ([R-SER-08]). Deduplicating two identical tiles, or sharing one index region between two layers, is forbidden — [R-CNT-13]: 'Extents are owned exactly once.' Reserved record flag bits, and the MU/PE bits of registered types, are fixed ([R-CNT-12], [R-CNT-22]). Front-block bytes [8,16) and trailer bytes [56,60) are zero. Entry order is disk-ordinal order ([R-IDX-01]). A compactor may not re-compress: [R-WRT-07] keeps 'every stored tile's bytes verbatim — each index entry's crc is unchanged'.

**Byte-level?** no — By construction this catalogue contains no ambiguity: every entry is a divergence the document deliberately and explicitly licenses, so both of any two writers' outputs are conforming files and every reader and verifier reaches the same verdict on each. It is reported here because the task asked for it, not because resolving anything in it would move a byte. The two entries that would move bytes are broken out as WR-02 (byte-level) and WR-06 (not).
