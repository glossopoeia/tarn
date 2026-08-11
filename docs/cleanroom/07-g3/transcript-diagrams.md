# Cleanroom round 7 — diagrams walk

**Access disclosure.** spec/tarn.md only

## Walk summary

I inventoried and checked every figure, ASCII layout, byte table, layout table and worked example in the document, and completed the audit from the text alone.

Byte-exact figures, all recomputed independently (CRC-32C implemented from §4.5's stated parameters): the §4.5 check vector (CRC-32C("123456789") = 0xE3069283, stored `83 92 06 E3`; CRC of zero bytes = 0) — confirmed; Appendix A's 128-byte annotated dump — every field offset re-derived against §6.2's trailer table (magic [64,72), version_major [72,74), minor [74,76), flags [76,80), generation [80,88), dir_offset [88,96), dir_length [96,104), committed_file_length [104,112), file_id [112,120), reserved [120,124), CRC [124,128)), the directory CRC over zero bytes = 0x00000000, the 44-byte pad arithmetic, and the trailer CRC over bytes [0,60), which I computed as 0xE00938D2 = stored `D2 38 09 E0` — all correct, and consistent with §5.1's smallest-file example and Appendix B; §15.4's all-sentinel full-segment constant, which I computed over 65,536 × `FF ×16 00 ×4` as 0xEECB3BB2 — correct; §12.3's twelve-byte channel entry; §4.6's `température` NFC/NFD byte counts; §12.1's bfloat16 `80 3F` / `0x7FC0`; §17.2's zstd magic and T23's LZ4 frame magic; §15.2's 20-byte sentinel.

Arithmetic in every worked example checks out: §11.2 grids, §11.4 ordinals (s = 10, in-tile 11,452, disk 74), §14.2 strides and offsets (Q = 3/5, 18/30 bytes, [15,18)/[25,30)), §14.3's `55 01` / `55 FD` packing, §14.5's 32-byte edge tile, §15.4's segmentation (16 segments, 16,960 final entries, [19,660,800, 20,000,000), 20,000,064-byte region, 1.25 MiB), §16.2's four runs, §17.3's byte-shuffle output (reproduced byte for byte), §20.3's 644-byte index, §21.9's 256 KiB/4 MiB note.

I also mechanically recounted §21's register: 39 + 50 + 26 + 10 = 125 rows and, counting semicolon-separated instance cells per §21.1's stated rule, exactly 242 instances — matching §21.8's claim precisely.

ASCII diagram column positions were extracted programmatically. §9.2's crash figure, §20.3's shapes (a)–(c) and §20.5's compaction figure are column-exact (each ▓ run occupies exactly the columns of the structure it replaced; the F arrow sits one column past the final border, which is correct for a file length). §5.1's box figure is the exception (finding DG-06). Cross-figure agreement holds: §5.1 vs §20.3(a) (adding a layer), §9.2 row 3 vs §20.3(b), §5.1 vs §20.5 (the contiguity difference is explicitly disclaimed and cross-referenced).

Findings below are figure/table/restatement defects; none is byte-level, and I say why for each.

## Findings (9)

### DG-01 — CONTRADICTION

**Location.** §8.1 map (`[R-CNT-19]`); §4.5; §5.2 (`[R-CNT-02]`); §9.7 (`[R-LIF-08]`); §7.2 (`[R-CNT-13]`); §20.4 table

§8.1's coverage map claims to account for every field of every structure, but it has no row for a record extent belonging to any record type other than layer (tile-index region) and user metadata. A conforming file can carry an experimental-range MU = 0 record with a nonzero extent slot, whose extent bytes are a §5.2 'structure' in the live committed state covered by no checksum at all — so §8.1's map does not, in fact, state a checksum for every structure, and §9.7's coverage walk has no checksum to apply to those bytes.

> Every field of every structure is covered by exactly one checksum — excepting the equality-checked front signature block and this map's terminal checksum fields, per §4.5 — as this map states. All checksums are CRC-32C over bytes exactly as stored. `[R-CNT-19]`

> Every byte of the live committed state belongs to exactly one of: the front signature block; or a **structure** — a stored-tile extent, a record extent (the bytes any record's extent slot references, whatever the record's type, §7.2), the directory, or the trailer.

> It checks that these occupy disjoint byte ranges, that each lies within [16, F − 64), and that each verifies against the checksum covering it (§8.1).

> For a record with MU = 0, the extent slot is its only sanctioned reference to bytes outside the record sequence ... this is what lets a compactor relocate an unknown ancillary's extent without parsing it (§20).

**Permitted readings.**

1. §8.1's map is exhaustive of what this format checksums, and `[R-CNT-19]`'s universal phrasing is simply overbroad: an unknown record's extent is covered by nothing, `[R-LIF-08]`'s checksum clause is vacuous for it, and a verifier certifies the file.
2. `[R-CNT-19]` is a real requirement over every structure §5.2 names, so a live-state structure covered by no checksum is a defect the verifier cannot check, and it must report *cannot establish* under `[R-CNF-11]` rather than certify.

**Picked.** The first. §21.6 registers 'A record type this specification has not assigned, from the experimental range (≥ 0x8000, §10.2), carries MU = 0' as a defined, conforming condition, and §21's register — whose completeness is normative — carries no row for an uncovered extent. A verifier therefore has no basis to withhold certification; `[R-CNT-19]`'s scope is the structures this specification itself defines fields for.

**Rationale.** This is a table-completeness defect, not a rule conflict a file can exhibit: no file becomes conforming or nonconforming either way. It is reportable because §8.1 is presented as a total map and §9.7 leans on it ('the checksum covering it') for a claimant class that has none. §20.5's compactor relies on the same gap in the other direction — it relocates such an extent verbatim with nothing to re-verify against, while `[R-WRT-09]` tells it to 'verify each link of the chain ... and each relocated extent's checksum'.

**Byte-level?** no — Concrete file: directory carries a record type 0x8001, flags MU = 0 / PE = 1, inline_length 0, extent (X, 100) over 100 arbitrary bytes, plus one intact layer. Every reader treats it identically — ignore-record, no fetch of the extent (`[R-CNT-15]`, §21.6) — so no reader's accept/reject of any byte changes. A writer's permitted output does not change either: nothing obliges or forbids a checksum in those 100 bytes. The only divergence is a verifier's verdict, and §21.6 plus the register's normative completeness already fix it as conforming.

### DG-02 — CONTRADICTION

**Location.** §18.2 layout table (`[R-MTA-03]`) vs §21.6's table row; §10.3 (`[R-EXT-03]`); §7.1 (`[R-CNT-25]`)

§18.2's layout table gives the metadata-encoding field's valid values as '1 or 2', which makes an experimental-range value (≥ 0x80) an invalid field value and hence a nonconforming file. §21.6 registers exactly that byte as a defined, non-violating condition whose file is conforming.

> | 0 | 1 | u8 | encoding | structural | 1 or 2; see below |

> | A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's conduct, not the bytes | `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]` |

> and for the metadata-encoding space of §18.2, ignore-record under the quarantine (`[R-CNT-25]`), never a scope-level rejection. `[R-EXT-03]`

**Permitted readings.**

1. The 'Valid values' cell is normative for file conformance, as the same column is elsewhere (F13, F14, F17 are register rows for the trailer table's cells), so encoding 0x80 makes the file nonconforming and — being an invalid field value in a structural field — is a validity error at the record's containing scope.
2. The cell is shorthand for 'the values this text assigns', §18.2's following prose and `[R-CNT-25]` govern the outcome, and a file carrying 0x80 is conforming with the record ignored.

**Picked.** The second. `[R-CNT-25]` names 'an unimplemented or invalid encoding' explicitly and assigns ignore-record 'notwithstanding the owning-scope mapping of `[R-CNF-08]`'; `[R-EXT-03]` adds 'never a scope-level rejection'; §21.6 states the file is conforming. Three rules foreclose the first reading.

**Rationale.** The defect is that §18.2's table cell is the one 'Valid values' cell in the document that hard-codes an assigned-value list where the space has a conforming experimental range. §6.2's trailer table shows the careful form for exactly this case — version_minor reads 'any (see §6.3)' and flags names the lanes rather than the assigned bits — so the table pattern the document otherwise follows is available and was not used here.

**Byte-level?** no — Concrete file: a top-level user-metadata record whose one inline byte is 0x80, with a valid extent and one readable layer. Under the table-as-normative reading a reader would reject-file and return nothing; under the governing rules it ignores the record and serves the layer. That would be byte-level if both readings were permitted — but `[R-CNT-25]`'s 'invalid encoding → ignore-record, notwithstanding `[R-CNF-08]`' and `[R-EXT-03]`'s 'never a scope-level rejection' make the rejecting reader nonconforming. What is left is the verifier's verdict on the same bytes, which §21.6 fixes as conforming.

### DG-03 — CONTRADICTION

**Location.** §15.4 second worked example vs `[R-CNT-17]` (§7.4), `[R-CNT-23]` (§7.4 table), §7.4 opening paragraph, `[R-GEO-02]` (§11.1)

§15.4's example asserts that any layer with entry_count ≤ 65,536 has one segment and a 4-byte segment-CRC array. At entry_count = 0 — an explicitly valid, first-class case — the region has zero segments, a zero-byte array, extent slot (0, 0), and crc_of_crc_array = 0; there is no region to fetch and no CRC to verify.

> A layer with entry_count ≤ 65,536 has one segment and a 4-byte array: fetching the whole region and verifying one CRC is the naive reader, unchanged.

> Under index_encoding 1, extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0); a mismatch ... is a validity error at layer scope. `[R-CNT-17]`

> A layer record's extent slot addresses the layer's tile-index region (§15); a layer with zero addressed tiles has extent (0, 0).

> A dimension with extent 0 is valid: its grid count is 0, the layer has zero addressed tiles, its tile index has zero entries, and its reference array is empty. `[R-GEO-02]`

**Rationale.** ⌈0 / 2¹⁶⌉ = 0, so the formula the example illustrates yields a zero-length region, not a 4-byte array. The example's bound should be 1 ≤ entry_count ≤ 65,536. As written, a reader who takes the example as the general small-layer case would expect a 4-byte tail on a region that does not exist, and the register already treats the file the example describes as broken (L23 registers a nonzero slot with entry_count = 0, L28 a nonzero crc_of_crc_array with entry_count = 0 — both reject-layer).

**Byte-level?** no — Two candidate byte sequences: a layer record with entry_count = 0, extent slot (0,0), crc_of_crc_array = 0 (correct), versus one with entry_count = 0, a 4-byte extent and a stored array CRC. Both are decided without ambiguity: the first is conforming, the second is L23/L28 reject-layer, because `[R-CNT-17]`'s formula and `[R-CNT-23]`'s 'crc_of_crc_array ... 0 when entry_count = 0' compute a unique answer. No implementation reading the normative rules can be misled into accepting the second, so no byte a conforming reader must accept or reject changes.

### DG-04 — CONTRADICTION

**Location.** §5.1 'a file after three commits' figure caption vs §20.3 (`[R-WRT-04]` step 4) and its note; §1 third design pillar

The §5.1 figure's caption states, without qualification, that only the directory, the pad and the trailer are re-emitted per commit. §20.3 requires every layer whose stored-tile set, index content, or index placement a commit changes to have its whole tile-index region re-emitted, and §1 and §20.3's note both price that cost explicitly.

> Layer A's tiles and index have never moved: only the directory, the pad and the trailer are re-emitted per commit, and a layer the commit does not touch keeps its extent slot pointing where it always pointed (§20.3, `[R-WRT-05]`).

> Every layer whose stored-tile set, index content, or index placement this commit changes has its tile-index region re-emitted in full — entry_count entries plus the segment CRC array ...

> A long series of small edits is supported and wasteful — each costs a full tile and its layer's whole index (§20.3).

**Rationale.** The clause is true of this figure's file (no commit after creation changed a layer's stored tiles) but is written as a general property of commits, and it sits immediately above the paragraph that generalizes it further ('the structures that must change on every commit are the last ones in the file'). §20.3's shape (b) figure draws the contradicting case — the index region hatched and re-emitted whole — so the two figures of the same operation disagree at the caption level. Scoping the sentence to layer A, or to commits that touch no layer's tiles or index, resolves it.

**Byte-level?** no — A writer misled by this caption would append a new tile payload and re-emit only the directory, pad and trailer. That file is still conforming: the layer's index still points at the superseded payload, the new payload is simply unreferenced slack (`[R-CNT-21]`), and every checksum verifies. So the misreading produces wrong content in a well-formed file — §21.7's 'incorrectness of content' class — not a divergence about which bytes any implementation must accept or reject.

### DG-05 — OBSERVATION

**Location.** §19.1 step 4 (`[R-RDR-01]`) and §19.3 (`[R-RDR-03]`) vs the Detector/Detected columns of §21.2 (F24, F25, F26) and §21.3 (L1, L11, L12, L13)

The consolidated open and layer-access algorithms enumerate the checks due at their tier, but their enumerations are not co-extensive with the register rows the same tier carries. §19.1's record walk names only `[R-CNT-12]`, `[R-CNT-15]`, `[R-CNT-14]`, `[R-CNT-13]` and `[R-ENC-12]`, yet F24/F25/F26 (`[R-CNT-25]`, `[R-MTA-03]`) are reject-file rows detected at open. §19.3's list omits `[R-ENC-03]`, `[R-ENC-06]`, `[R-CNT-25]` and `[R-MTA-03]`, yet L1, L3, L11, L12 and L13 are layer-access rows governed by them.

> Parse the record sequence under §7.2's framing (`[R-CNT-12]`), applying the MUST_UNDERSTAND gate for unknown top-level types (`[R-CNT-15]`), the per-type multiplicity rules (`[R-CNT-14]`), and the extent-slot validity rules for non-layer top-level records (`[R-CNT-13]`) — all decidable from the resident bytes and F — and build the layer table

> | F26 | A top-level user-metadata record's inline_length is not 1; the encoding field is a fixed structure, not a growable one | — | reader | open | `[R-MTA-03]` (R-ENC-07) |

> the slot's validity rules (`[R-CNT-13]`), the §7.4 constraint set (`[R-CNT-23]`, `[R-CNT-16]`), the exact parse, sub-record walk, and sub-record multiplicity (`[R-CNT-18]`, `[R-CNT-14]`), dimension- and channel-name rules (`[R-ENC-12]`, `[R-ENC-15]`), the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3, the per-type fill constraints (§13.2, `[R-TYP-07]`), the codec declaration bounds (`[R-COD-07]`), the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`), and the index cross-checks computable without I/O (`[R-CNT-17]`).

**Rationale.** Decidable — §19.2's tier bullets ('the directory region and its record walk'; 'the full validation of that layer's record') are the governing timing rule and are broad enough to cover the omitted rules, and §19 announces itself as a consolidation that 'introduces no new structures'. But deciding it requires cross-tabulating 125 register rows against two prose enumerations, which is why it is an OBSERVATION rather than an ambiguity. The stake is real: F24/F25/F26 are reject-file, so an implementer who reads §19.1's step 4 as exhaustive builds a reader that serves a whole file's layers before ever noticing a file-scope violation.

**Byte-level?** no — Concrete file: one intact layer plus a top-level user-metadata record with inline_length = 2 (F26, reject-file, Detected = open). Reader A rejects at open and returns nothing; reader B, following §19.1's step-4 list literally, opens, serves the layer's samples, and trips only at extent use — a visible difference in what bytes get served. It is not byte-level because both §19.2's first tier bullet and F26's own Detected cell put the check at open, and §19.1 is silent rather than contrary ('all decidable from the resident bytes and F' describes the listed items, it does not close the list). Reader B is therefore nonconforming under a rule already written.

### DG-06 — OBSERVATION

**Location.** §5.1 'a file after three commits' figure (the brace line under the box); §20.3 shape (a) brace label

In §5.1's box figure, all three under-braces are drawn two columns right of the cells they label: the 'tiles+index' braces close on the first ▓ column of the adjacent slack run rather than on the layer cell, and the 're-emitted' brace closes one column past the box's right border. §20.3(a)'s brace over the slack run is labelled 'was dir₁' although the run it spans is dir₁, the pad and tr₁.

> │ front │  layer A  │▓▓▓▓▓▓▓│  layer B  │▓▓▓▓▓▓▓│ dir₃ │pad │ trail₃ │

> └tiles+index┘       └tiles+index┘       └──── re-emitted ────┘

> └── untouched ──┘└ was dir₁ ──┘

**Rationale.** Measured from the rendered columns: the box separators sit at columns 0, 8, 20, 28, 40, 48, 55, 60, 69, so layer A's cell is columns 9–19 and layer B's is 29–39; the braces run 9–21 and 29–41, each claiming the first slack column, and the third runs 49–70 against a box that ends at 69. The slack columns are precisely what the layer's tiles+index are not — they are superseded directories — so the drawing labels one column of each ▓ run as layer structure. §9.2's, §20.3(b)'s and §20.5's figures are column-exact by comparison (in §20.3(a) and (b) the ▓ run occupies exactly the columns of the dir│pad│tr it replaced), so this is an outlier rather than a house style. The 'was dir₁' label is corrected by the prose two lines later ('The slack is the old directory, pad and trailer'), so it misleads only a reader who reads the figure alone.

**Byte-level?** no — The figure is explicitly labelled 'Regions, not offsets' and carries no byte offsets, sizes or ordering commitments — its own caption disclaims contiguity and ordering by citing `[R-SLB-05]`. No byte sequence's validity turns on where a brace corner falls.

### DG-07 — OBSERVATION

**Location.** Appendix A, closing paragraph, vs §6.4 (`[R-CNT-09]`) and §6.1 (`[R-CNT-04]`)

Appendix A asserts that any speculative suffix window over this 128-byte file reaches offset 0 and therefore makes the front block resident. A suffix window need only start at or below dir_offset = 16 to make the second request unnecessary; a 112-byte window covering [16, 128) captures the directory, reaches offset 16, and leaves bytes [0, 16) non-resident.

> A local reader additionally verifies bytes [0, 16) by equality first, which `[R-CNT-04]` requires of any reader holding them — as a remote reader does too whenever it speculates a suffix window, since this file is 128 bytes and any such window reaches offset 0.

> A reader MAY instead speculatively fetch a suffix window in one request and use containment: if the fetched buffer contains the directory region, request 2 is unnecessary.

**Rationale.** The annotation attaches residency to the act of speculating rather than to the window's start offset, which is the opposite of the test `[R-CNT-04]` is at pains to establish ('The test is residency, not transport'). The 64 KiB window §6.4 advises does reach offset 0 on a 128-byte file, but nothing binds a speculator to that size, and the appendix's 'any such window' over-licenses the inference. Reworded as 'whenever it speculates a window that reaches offset 0', it is exact.

**Byte-level?** no — In both readings the front-block equality check is optional for a reader that does not hold [0, 16) (`[R-CNT-04]`: 'A reader that would have to issue a further range request to obtain those bytes MAY defer or omit the check'), and mandatory for one that does. F8's condition text already records the same conditionality. So the set of files any conforming reader must reject is unchanged; only the appendix's description of when the condition is triggered is wrong.

### DG-08 — OBSERVATION

**Location.** §21.2, row F5, Instances cell

F5's condition requires the total structure size to be unchanged, but its worked instance — a trailer with version_major and version_minor each written as u32 — adds four bytes to the trailer and therefore cannot be built while holding the size fixed, unless another 4-byte field (in practice the reserved bytes at [56,60)) is deleted, which is a different violation.

> | F5 | A fixed file-scope structure places its fields at widths other than those the spec fixes, with total size unchanged | trailer (e.g. version_major/version_minor written as u32 each); top-level record header | reader | open | `[R-ENC-06]` (R-CNT-06) |

> In every format major version, permanently: the final 64 bytes of a file contain the trailer magic at F − 64, version_major and version_minor at F − 56, and a CRC-32C at F − 4 covering bytes [F − 64, F − 4) ... The format-major-1 trailer has zero slack: every byte is assigned.

**Rationale.** The trailer's 64 bytes are fully assigned (8 + 2 + 2 + 4 + 8 + 8 + 8 + 8 + 8 + 4 + 4 = 64), so widening two u16 fields to u32 pushes the CRC past the trailer's end. The corpus obligation is one file per instance (`[R-ERR-02]`, `[R-VEC-03]`), so a builder must either drop a field — making the vector exercise F17 or F16 as well — or violate the row's own 'total size unchanged' premise. §24's rule for non-isolable conditions ('the entry records every row the file exercises and says which it was built for') absorbs this, but the cell's parenthetical as written names an impossible file.

**Byte-level?** no — `[R-ENC-06]` has no direct witness in the bytes — a reader sees only values, and every realization of this condition is caught by the trailer's ordinary field gates (F3, F11, F12, F16, F19). Which vector a corpus builder constructs does not change what any implementation may emit or must accept, and §21.1 already makes the governing rule, not the row, authoritative.

### DG-09 — AMBIGUITY

**Location.** §21.3, row L1 Instances cell, against §21.1's instance-enumeration rule and §21.8's total; compare L16, L17, L18

L1's instance cell folds two containers into a parenthetical ('extent_offset; extent_length (layer record and sub-record slots)'), yielding two instances for a condition that §21.1's own rule would count as four — a field ranging over two containers. L16, L17 and L18 expand the same two containers into separate instances. How many corpus files L1 requires is therefore not fixed by the register.

> | L1 | A u64 offset, length, extent, or count field of a layer record holds a value above 2^63 - 1 | extent_offset; extent_length (layer record and sub-record slots); dimension extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S | reader | layer access | `[R-ENC-03]` (R-CNT-13, R-CNT-23) |

> An instance names a field the condition ranges over, a container it can occur in, one of several alternatives the condition text states, or any combination of the three — a condition applying to two alternatives in two containers has four.

> | L17 | A layer record's or sub-record's nonzero extent slot has extent_offset < 16, pointing into the front signature block | layer record extent slot; sub-record extent slot | reader | layer access | `[R-CNT-13]` |

**Permitted readings.**

1. Count the cell mechanically as written: L1 has six instances, and the register's total is 242 — which is exactly what §21.8 states, so the cell is correct and the parenthetical is merely descriptive.
2. Apply §21.1's field × container product: extent_offset and extent_length each occur in two containers, giving eight instances for L1 and 244 in total — which contradicts §21.8's stated 242.

**Picked.** The first. §21.1 says 'the count is therefore mechanical once the cell is written', and I recounted all 125 rows: semicolon-counting the cells as written gives exactly 39 + 50 + 26 + 10 = 125 rows and 61 + 100 + 45 + 36 = 242 instances, matching §21.8 to the unit. The cell text is authoritative; the parenthetical is prose.

**Rationale.** The reading is settled by the arithmetic, but the inconsistency is worth recording because §21.1's enumeration rule and the cell-as-written rule can disagree, and only one of them is checkable against §21.8's total. Two corpus builders reading L1 alongside L17 could reasonably build six or eight files for the same row; `[R-VEC-03]` makes any shortfall 'a gap in the corpus'. Expanding L1's parenthetical the way L17 does — and updating 242 to 244 — removes the divergence.

**Byte-level?** no — This bears only on how many files a conformance corpus contains for one register row. §24 already makes the corpus derivative ('where a vector's recorded expectation and this specification disagree, this specification governs and the vector is corrected'), and every file either builder produces is an out-of-domain u64 in a layer record — reject-layer under `[R-ENC-03]` on any reading. No byte's treatment differs.
