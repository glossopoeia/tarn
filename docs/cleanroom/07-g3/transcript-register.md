# Cleanroom round 7 — register walk

**Access disclosure.** spec/tarn.md only

## Walk summary

I read spec/tarn.md end to end, then worked §21 as an auditor.

§21.1 makes four things normative. (1) Completeness: "Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document", with detectability gated by [R-CNF-07] and §21.7 named as "the inventory of what fails it". (2) The tiebreak: each row "*restates* its governing rule, and where a row and the rule it cites diverge, **the rule governs**". (3) Scope attachment: conditions attach to the finest structure they damage; outcome follows scope, never severity; a file exhibiting a strict specialization is recorded against the narrower row. (4) The counting rule: an Instances cell is mechanical — semicolon-separated items, a "—" cell is one instance, an instance may name a field, a container, or a stated alternative, "a condition applying to two alternatives in two containers has four", a family whose shape does not change is one instance (T24's *any codec*), and "One instance is one *distinguishable* file", so fields read by a single predicate are not instances. Verifier rows record a scope, not a reader obligation.

I then traced all 125 rows (F1–F39, L1–L50, T1–T26, R1–R10) to their cited requirements. §15.3's classification table maps one-to-one onto T1/T6–T12 plus L19/F36/L41–L43, and §7.4's constraint list maps onto L28–L37/L40/L44/L46 with nothing left over. §17.2's six zstd constraints map onto T17–T22 exactly. The F-row/L-row pairs are deliberately disjointed by a "non-layer top-level" or "top-level" qualifier in every case but F31, which is the finding below.

I counted the instance cells myself: §21.2 = 61, §21.3 = 100, §21.4 = 45, §21.5 = 36, total 242, over 39+50+26+10 = 125 conditions. Both figures in §21.8 are exactly right under §21.1's mechanical rule, so the count claim survives. What does not survive is the internal consistency of some cells against §21.1's own arithmetic, and the presence of instances no file can exhibit alone.

For completeness I walked every MUST-level requirement from §2 through §24 and asked whether the register, §21.6, or §21.7 accounts for it. One named, expressly detectable violation has no row anywhere ([R-MTA-07]); §21.7's undetectable inventory omits the whole §20 updater/compactor family; and §21.6's closing "two cases" claim is contradicted by the cross-reference §2.3 points at it with. I could complete the audit from the text alone.

## Findings (12)

### RD-01 — CONTRADICTION

**Location.** §21.2 row F31; §21.3 row L50; §7.3 [R-CNT-22]; §7.2 [R-CNT-13]

F31 claims every top-level record of a registered type, which includes layer records (type 0x0001 is a top-level type), and therefore collides with L50, which claims layer records for reject-layer. F31 sits under §21.2's blanket "Outcome: reject-file", so the same file is recorded at two different scopes by two different rows.

> | F31 | A top-level record of a type §7.3 registers carries a stored MU or PE bit differing from the value the registry fixes; readers apply the type's fixed semantics regardless | flags bit 0; flags bit 1 | verifier | certification | `[R-CNT-22]` (R-CNF-05) |

> | L50 | A layer record, or a sub-record of a type §7.3 registers, carries a stored MU or PE bit differing from the value the registry fixes; readers apply the type's fixed semantics regardless | layer record flags; sub-record flags | verifier | certification | `[R-CNT-22]` (R-CNF-05) |

> a verifier MUST treat the mismatch as a validity error at the record's governing scope

> a validity error at the scope the record governs (§7.3): the layer for a layer record and for sub-records, the file for other top-level records

> Outcome: reject-file. 39 conditions.

**Picked.** Reject-layer, per L50 and [R-CNT-22]; F31 must be read as restricted to non-layer top-level records (type 0x0002).

**Rationale.** Every other F/L pair in the register carries the disambiguating qualifier that F31 lacks: F28 and F29 say "A non-layer top-level record's flags", F33–F35 say "A non-layer top-level record's extent slot", F30 says "top-level user-metadata document" against L49's "layer sub-record". F31 alone omits it. §21.1's tiebreak decides the substance — [R-CNT-22] says "the record's governing scope", and §7.2 fixes that as the layer for a layer record — so only the table is wrong. The corpus consequence is real: under F31 as written a layer record with a flipped PE bit is built as a reject-file vector and as an L50 reject-layer vector, and [R-VEC-04] requires the reject-layer one to carry an intact sibling while the reject-file one does not.

**Byte-level?** no — No byte sequence is treated differently. [R-CNT-22] already obliges every reader to "apply a known type's specified semantics regardless of its stored MU and PE bits", so reader behavior over the affected bytes is identical under both rows; only a verifier's recorded scope differs, and its verdict is nonconforming either way. §21.1's "the rule governs" resolves the scope without any implementation having to guess.

### RD-02 — OBSERVATION

**Location.** §18.4 [R-MTA-07]; §21.1 completeness clause; §21.2–§21.5 (no row); §21.6 (no row); §21.7 [R-ERR-01]

[R-MTA-07] expressly names a detectable, verifier-detected, file-nonconforming violation — a standardized `tarn.` key appearing outside the scopes §18.4's table lists — and the register carries no row for it, at any scope. §21.1 makes that omission a defect in the document.

> A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document. A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`); no reader's behavior turns on the violation, since a reader ignores the key either way.

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document, detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

**Picked.** The register is incomplete; the missing row is a verifier/certification row with two instances (top-level document, layer sub-record document) — `tarn.created` or `tarn.creator` in a layer document, or `tarn.axes`/`tarn.stats` in the file document.

**Rationale.** The condition has exactly the profile of F30/L49 and F31/L50: verifier detector, certification detection point, nonconforming file, unchanged reader behavior. §21.6's closing paragraph makes that profile an explicit precedent — "Both make the file nonconforming while leaving every reader behavior unchanged ... so both carry detector *verifier*, on the precedent `[R-CNT-12]`'s reserved-flag rows already set" — so there is no principled reason for [R-MTA-07] to be absent. It is not covered by §21.7 either: §21.7's first paragraph is about content correctness and its second about obligations with no single-file witness, and this one has a witness in one file. It is also not in §21.6, which would be wrong, since [R-MTA-07] calls the file nonconforming.

**Byte-level?** no — [R-MTA-07] itself states both halves — the writer prohibition and the reader's "MUST ignore ... rather than rejecting the document" — so no implementation needs the register to know what to emit or how to handle the bytes. The omission changes the corpus (a missing vector under [R-ERR-02]) and a verifier's report, not any accept/reject decision over bytes.

### RD-03 — CONTRADICTION

**Location.** §2.3 [R-CNF-03]; §21.6 closing paragraphs; §21.9 [R-ERR-04]

§2.3 carves two exceptions out of the reader's acceptance obligation and cites §21.6's closing paragraph as naming them, but §21.6's closing paragraph names a different pair. The exception §2.3 cares about most — a file whose values exceed §21.9's minimum guarantees — appears nowhere in §21.6, and §21.6's first case (an unimplemented version_major) is not one of §2.3's two.

> A reader MUST accept every conforming file of a format major version it implements, carrying no record of a type it does not implement with MUST_UNDERSTAND = 1, and none of whose values exceeds the minimum guarantees of §21's limits table (§21.6's closing paragraph names those two exceptions),

> Two distinct cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly conforming under that major. The second is an **experimental-range record type carrying MU = 1**

> A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose declarations exceed what it can serve, a layer or a tile.

**Picked.** §21.6's enumeration is incomplete and the §2.3 cross-reference is wrong: there are at least three conforming-file-refused cases (unimplemented major, unimplemented MU = 1 type, and a resource declination under [R-ERR-04]), and §21.6 lists two of them, only one of which §2.3 is pointing at.

**Rationale.** §2.3's "those two exceptions" are (a) a record of an unimplemented type with MU = 1 and (b) values exceeding the minimum guarantees. §21.6's two are (a′) an unimplemented major and (b′) an experimental-range type with MU = 1. Only (a) and (b′) are close, and (b′) is narrower than (a): a MU = 1 type a reader does not implement can also arrive from a later minor version's registry assignment, which is neither experimental nor reserved. The resource case is stated only in [R-ERR-04], and §21.6 — the section §2.3 sends the reader to — never mentions it, while [R-ERR-04] adds a refusal granularity ("a layer or a tile") that §2.3's whole-file framing does not anticipate.

**Byte-level?** no — [R-ERR-04] states the resource rule directly and unambiguously in §21.9, and [R-CNT-07] states the version_major rule directly in §6.3, so an implementation reaching either through its own section gets the same answer. The defect is a broken cross-reference and an under-enumerated table, not a fork in what may be accepted: no byte sequence is accepted by one reading and rejected by the other.

### RD-04 — AMBIGUITY

**Location.** §21.1 Instances paragraph; §21.2 row F33; §21.3 rows L16, L1; §21.5 row R5

§21.1 fixes the instance arithmetic as multiplicative — alternatives times containers — but several cells collapse one factor. L16 states two alternatives in two containers and lists two instances; F33 states the same two alternatives in one container and lists them both; R5 states two alternatives in two containers and lists only the containers; L1 lists two fields that each occur in two containers as two instances, not four.

> An instance names a field the condition ranges over, a container it can occur in, one of several alternatives the condition text states, or any combination of the three — a condition applying to two alternatives in two containers has four.

> | L16 | A layer record's or sub-record's extent slot has exactly one of extent_offset and extent_length zero | layer record extent slot; sub-record extent slot | reader | layer access | `[R-CNT-13]` |

> | F33 | A non-layer top-level record's extent slot has exactly one half zero (offset 0 with length != 0, or offset != 0 with length 0) | extent_offset; extent_length | reader | open | `[R-CNT-13]` |

> | R5 | A decoded user-metadata document violates the document's own content rules — a key or string value containing ill-formed UTF-8 | top-level document; layer sub-record document | reader | extent use | `[R-CNT-25]` (R-ENC-11) |

> | L1 | A u64 offset, length, extent, or count field of a layer record holds a value above 2^63 - 1 | extent_offset; extent_length (layer record and sub-record slots); dimension extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S | reader | layer access | `[R-ENC-03]` (R-CNT-13, R-CNT-23) |

**Permitted readings.**

1. The cells are authoritative and §21.1's multiplication sentence is illustrative, so L16 = 2, R5 = 2, L1 = 6, and the corpus is 242 files.
2. §21.1's multiplication is the rule and the cells are simply wrong, so L16 = 4, R5 = 4, L1 = 8, and the corpus is 248 files — contradicting §21.8's stated 242.
3. The collapsed cells are claiming the alternatives are not 'materially different shapes' and so fall under the single-instance licence granted to T24's 'any codec' — but §21.1 grants that licence only to a family 'without the condition changing shape', and F33 demonstrates the register does not consider offset-zero and length-zero to be one shape.

**Picked.** Reading 1 for the corpus as it stands, because §21.8's 242 and my own mechanical recount of every cell agree exactly, so the cells were counted, not the rule applied. But the rule as written yields 248, and F33 shows the register applying it inconsistently across scopes for one and the same condition ([R-CNT-13]'s half-zero slot).

**Rationale.** The two readings are not reconcilable by §21.1's own text: it says the count 'is therefore mechanical once the cell is written', which makes the cell authoritative for the count, and in the same breath says two alternatives in two containers has four, which makes the condition authoritative. F33 versus L16 is the clean witness — identical condition, identical governing rule, one cell enumerating alternatives and the other enumerating containers. R5 compounds it, since a key and a string value are not the same shape: an ill-formed key also engages §4.6's name rules ([R-ENC-12], registered separately as R6 and R10) while a value engages only [R-ENC-11].

**Byte-level?** no — The dispute is over how many files a conformance corpus builds for a row, not over what any of those files contains or how a reader treats it. Every affected condition already has an unambiguous outcome from its governing rule ([R-CNT-13] reject-layer, [R-CNT-25] ignore-record). No implementation reads the Instances column to decide anything about bytes; §24 makes the corpus derivative in any case — 'where a vector's recorded expectation and this specification disagree, this specification governs'.

### RD-05 — AMBIGUITY

**Location.** §21.1 opening paragraph; §21.6; §21.7 [R-ERR-01]

§21.1 is titled 'How to read the register' and governs 'The register below', but §21 contains four violation subsections, a non-violation table (§21.6), an undetectability inventory (§21.7), a coverage claim (§21.8) and a limits table (§21.9). Whether §21.1's completeness clause, row-versus-rule tiebreak and instance arithmetic reach §21.6 and §21.7 is never stated, and the two candidate scopes give different answers about §21.6's rows.

> The register below enumerates every detectable violation this specification names: each row is one malformed condition, with the outcome class its scope determines (§2.4), the actor obliged to detect it, the point by which detection is due (§19.2), and the requirement that defines it.

> but each row *restates* its governing rule, and where a row and the rule it cites diverge, **the rule governs**

> | A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a writer's conduct, not the bytes | `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]` |

**Permitted readings.**

1. 'The register' means §21.2–§21.5 only. §21.6's rows then have no stated tiebreak against their cited rules, and a §21.6 row that says more than its rules do stands on its own authority.
2. 'The register' means §21.2–§21.6, since §21.5's preamble cross-refers to §21.6 as part of the same apparatus ('§21.6 lists the ignore-record conditions that are not violations') and §21.6's rows carry the same Rule column. Then the tiebreak applies, and a §21.6 row asserting something its cited rules do not say is overridden by silence.
3. 'The register' means the whole of §21.2–§21.7, since §21.1 explicitly enrols §21.7 as 'the inventory of what fails' the detectability gate.

**Picked.** Reading 3 for completeness (§21.1 names §21.7 by role, so §21.7 is inside the apparatus) and reading 2 for the tiebreak, because §21.6's rows carry a Rule column for exactly the same purpose §21.1 describes.

**Rationale.** The choice matters for §21.6's experimental-metadata-encoding row, which is the only place in the document that says a file carrying such an encoding is conforming: [R-MTA-03] fixes only the value partition, and [R-EXT-03] fixes only the ignore-record outcome, 'never a scope-level rejection'. Under reading 2 the tiebreak would leave the conformance question unanswered by any rule. It is rescued, but only indirectly, by [R-CNF-02], which names §10.3 as a conduct rule — 'where a value is published ... and a file is never nonconforming by virtue of one' — so the row is a correct derivation rather than a free-standing requirement. The contrast with §7.2, where [R-CNT-15] states the parallel conclusion for record types in the rule text itself, shows the document knows this needs saying and says it in one space but not the other.

**Byte-level?** no — I checked whether the register is the sole statement here, because that would make it byte-level under the stated test — it would decide whether a conforming writer may emit an experimental metadata-encoding byte. It is not sole: [R-CNF-02] plus §10.3 plus [R-MTA-03] already yield 'conforming', by the same chain [R-CNT-15] spells out for record types. Both readings of §21.1's scope therefore land on the same emit/accept behavior; only the derivation path differs.

### RD-06 — OBSERVATION

**Location.** §21.2 row F5; §21.3 row L3; §4.2 [R-ENC-06]; §21.8 [R-ERR-02]; §24 [R-VEC-03]

F5 and L3 register a field written at the wrong width, with total size unchanged, as a reader-detected violation. With the size unchanged there is no byte-level witness distinguishing it from a correct structure carrying different values, so no vector can be built that exercises F5 or L3 and nothing else — yet [R-ERR-02] and [R-VEC-03] require one per instance.

> No field's width is ever a writer choice: every field's width is fixed by this specification, and a structure whose fields appear at any other width is invalid at its owning scope. `[R-ENC-06]`

> | F5 | A fixed file-scope structure places its fields at widths other than those the spec fixes, with total size unchanged | trailer (e.g. version_major/version_minor written as u32 each); top-level record header | reader | open | `[R-ENC-06]` (R-CNT-06) |

> | L3 | A field of a layer-scope structure is written at a width other than the one this specification fixes (e.g. rank d as u16) | any layer-record inline-payload field | reader | layer access | `[R-ENC-06]` (R-CNT-18) |

> Every row of §21.2 through §21.5 — 125 conditions over 242 named instances — has at least one conformance vector (§24) whose expected verdict is that row's outcome, and a row naming instances has one vector per instance.

**Picked.** F5 and L3 are rows for conditions with no isolable witness; they belong with §21.7's inventory, or the register should say what byte pattern a reader is supposed to catch.

**Rationale.** Take F5's own example. version_major = 1 written as a u32 is the bytes 01 00 00 00 at trailer offset 8, which under the fixed layout reads as version_major = 1, version_minor = 0 — a perfectly valid trailer that no reader can fault. If instead the value makes the parse fail, it fails as F20/F21/F17 and §21.1's finest-structure rule records it there. L3's example behaves the same way: rank d as u16 shifts every subsequent field by one byte, so the inline payload overruns or leaves residue, and §21.1's specialization principle records the file against L24 ('A declared region of the layer record's inline payload does not lie entirely within inline_length'). Both rows also assign detector 'reader' and a detection tier, which [R-ENC-06] never does — it states invalidity, not a detection procedure. Contrast F1, which is candid about exactly this problem: 'detectable only through that field's own value or range gate'.

**Byte-level?** no — Because a reader parses every structure at the widths this specification fixes and has no other layout available, a same-size width error produces bytes that are either fully valid or invalid under some other row's gate. There is no byte sequence two implementations could classify differently on the strength of F5 or L3; the rows describe writer intent, which is not a property of the file.

### RD-07 — OBSERVATION

**Location.** §21.4 rows T15, T16, T23; §17.2 [R-COD-05], [R-COD-07], [R-COD-06], [R-COD-08]

T15 and T23 assign detector 'reader' at 'tile use' for a wrapper or frame magic, but neither [R-COD-05] nor [R-COD-07] states any reader obligation — unlike zstd, where [R-COD-06] mandates the magic check in so many words. The only reader path the rules actually supply for these rows is [R-COD-08]'s decode-exactness rule.

> **Codec 2 — deflate.** The stored bytes are exactly one DEFLATE compressed data stream as defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952) wrapper. `[R-COD-05]`

> they MUST begin with the compressed-frame magic (0xFD2FB528, the bytes `28 B5 2F FD`), and a reader MUST treat a payload whose first four bytes are not that magic, or that contains a skippable frame anywhere or more than one frame, as a validity error at tile scope

> **Codec 4 — lz4.** The stored bytes are exactly one LZ4 block per the LZ4 Block Format Description (lz4_Block_format.md, version 1.0; Appendix F pins the exact revision), decoded with the stored length as the input size and the decoded size as the output capacity. The LZ4 frame format is not used.

> | T23 | Codec 4 (lz4) and the stored bytes are an LZ4 frame (magic 04 22 4D 18) instead of exactly one raw LZ4 block | — | reader | tile use | `[R-COD-07]` |

**Picked.** Read T15/T16/T23 as identifications of a cause, with detection flowing from [R-COD-08]; §21.1's tiebreak forces this, since the cited rules impose no magic-based check.

**Rationale.** The rows are worded carefully enough to stay faithful — 'instead of exactly one raw LZ4 block', 'carry a wrapper rather than a raw RFC 1951 DEFLATE stream' — so a reader that keys on the four magic bytes alone would be going beyond both the row and the rule. The asymmetry with zstd is what makes this worth recording: an implementer building from the register would reasonably conclude all three codecs get a magic gate, and only one of them does. T16 has a second problem: 'the stored extent holds more than one DEFLATE stream — a second stream begins after the BFINAL block' is a strict specialization of T24 ('bytes remain in the stored extent after the stream, frame, or block ends'), and §21.1's specialization list — 'F2 of F8 and of F10, F38 of F39, L25 of L26' — does not name it, nor T18 of T24.

**Byte-level?** no — I tested whether a conforming file could start a codec-4 payload with 04 22 4D 18, which is the case where a magic-gating reader would wrongly reject conforming bytes. It cannot: token 0x04 means literal length 0 and match length 8, so the next two bytes are read as a match offset of 0x4D22 = 19746 with zero bytes of output produced, which is invalid at output position 0. Every LZ4 block beginning with that magic is malformed, so the divergence is unreachable. For deflate, a byte string that is simultaneously a valid zlib stream and a valid raw RFC 1951 stream consuming the extent exactly would have to place the Adler-32 inside and outside the stream at once; and any such file is nonconforming anyway, so [R-CNF-12]'s 'a reader MAY reject it upon detecting any violation' licenses both behaviors.

### RD-08 — OBSERVATION

**Location.** §21.4 rows T13 and T25; §17.1 [R-COD-02]; §17.2 [R-COD-08]

T13's second instance and T25's third instance name the same LZ4 condition in different words, so one file satisfies both rows, and T13 has no detection procedure of its own — a stored tile that needs state outside its extent is met by a reader only as a decode failure under [R-COD-08], which is T25.

> | T13 | A stored tile is not independently decodable from its own extent and layer record — the decode needs state or side data outside the extent | deflate stream carrying a previous tile's history window; lz4 block whose match offset reaches before its own output start | reader | tile use | `[R-COD-02]` (R-COD-06, R-COD-08) |

> | T25 | The stored bytes are a malformed stream that fails to decode | deflate block type 3 / invalid Huffman table; corrupt zstd block header; lz4 match offset 0 or match reaching past produced output | reader | tile use | `[R-COD-08]` |

> Every stored tile is independently decodable from its stored bytes and its layer's record alone: neither stage carries state between tiles, references bytes outside the tile's stored extent, or requires side data — dictionaries included (§17.2). Slabs (§16) are an I/O grouping, never a compression context. `[R-COD-02]`

**Picked.** T13 is a cause row like T26, not an independent check; its instances are detected by T25's procedure, and §21.1's specialization rule should name the pair.

**Rationale.** An LZ4 match offset that 'reaches before its own output start' and one 'reaching past produced output' are the same predicate — the match source lies before byte 0 of this block's output. Both rows are reject-tile, reader, tile use, so nothing diverges in outcome; what diverges is which row a corpus vector is attributed to, and §21.1 handles that only for the three specialization pairs it names. T26 shows the document already has a vocabulary for this case — 'the check that detects it is T2's or T4's, and this row records the cause rather than a procedure of its own' — and T13 could have used it. The deflate instance is the same story: a raw stream whose back-references reach before the start of output is malformed under RFC 1951 and fails as T25.

**Byte-level?** no — Both rows carry the identical outcome, detector and detection point, and both trace to [R-COD-08]'s 'a reader MUST treat a malformed stream and either inexactness as a validity error at tile scope'. Whichever row an implementation attributes the file to, it rejects the same tile. The consequence is duplicate corpus vectors under [R-ERR-02], not a divergence in bytes.

### RD-09 — OBSERVATION

**Location.** §21.7 [R-ERR-01] second paragraph; §21.1 completeness clause; §20 [R-WRT-05]–[R-WRT-09]; §6.3 [R-CNT-08]; §23.1 [R-PRV-01]

§21.1 designates §21.7 as 'the inventory of what fails' the detectability gate, but §21.7's second paragraph enumerates five requirements and omits every §20 updater and compactor obligation, the updater's ignore-lane copy-forward duty, and [R-PRV-01] — all MUST-level, all with no single-file witness, none registered and none inventoried.

> A second set of obligations is omitted from the register because a single file exhibits no witness of their violation. Committed-prefix immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets in its own payload is opaque by construction. `[R-ERR-01]`

> In the new complete directory, an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify, whether or not it implements the record's type

> It MUST mint a fresh file_id for the output — a new draw under §9.3's randomness advice, not merely a value compared against the input's

> An updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear them

**Picked.** §21.7's second list is exemplary in fact but is enrolled by §21.1 as an inventory; either it should carry the §20 family or §21.1 should stop calling it the inventory.

**Rationale.** [R-WRT-05]'s byte-identical re-emission, [R-WRT-06]'s fresh file_id, [R-WRT-07]'s reference-array equality, [R-WRT-08]'s no-re-encode rule and [R-CNT-08]'s copy-forward duty are all two-file properties: you need the input and the output, or two generations, and §9.7 explicitly declines to reconstruct history — 'Nothing here enumerates prior commits.' They sit in exactly the same class as [R-LIF-01] and [R-LIF-03], which §21.7 does name. The document elsewhere is scrupulous about explaining why a MUST carries no row — §16.2's note on [R-SLB-04], §7.4's note on the nesting prohibition, §9.5's note on residue past a completed commit all do this work — which makes the §20 family's silent absence conspicuous rather than harmless.

**Byte-level?** no — Every requirement in question is stated in full at its own site with its actor and obligation intact, so an updater or compactor implementing §20 knows precisely what to emit. Whether §21.7 also lists it changes only whether a reader auditing §21 can conclude the inventory is exhaustive. No byte a conforming tool emits, accepts or rejects turns on it.

### RD-10 — OBSERVATION

**Location.** §21.5 row R5; §18.2 [R-MTA-04] fourth bullet

[R-MTA-04]'s fourth bullet names two distinct ways a document's UTF-8 can fail — an ill-formed byte sequence in the source, and a \uXXXX escape denoting an unpaired surrogate after escape resolution — and R5's condition and Instances cell carry only the first, so the escape case has no instance anywhere in the register.

> - **Well-formed UTF-8 throughout** (`[R-ENC-11]`) — including after escape resolution: a `\uXXXX` escape denoting an unpaired surrogate has no UTF-8 encoding and makes the document unreadable, as does an ill-formed byte sequence in the source

> | R5 | A decoded user-metadata document violates the document's own content rules — a key or string value containing ill-formed UTF-8 | top-level document; layer sub-record document | reader | extent use | `[R-CNT-25]` (R-ENC-11) |

**Picked.** R5 is narrower than the rule it restates; the unpaired-surrogate escape needs its own instances, since a document carrying it is well-formed UTF-8 in the source and well-formed JSON per RFC 8259.

**Rationale.** The escape case is a materially different shape by §21.1's own criterion, and the register applies that criterion elsewhere: T15 splits zlib from gzip, T25 splits the three codecs' malformations, R7 splits the BOM from the non-object top-level value. A vector for the escape case is a different file in a different way — the stored bytes pass every UTF-8 check and only fail after a JSON parser resolves \uD800 — so a corpus built from R5's two instances will not contain it. R7 does not rescue it either: an unpaired surrogate escape is syntactically valid JSON, so 'not well-formed JSON' does not reach it.

**Byte-level?** no — [R-MTA-04] states the consequence in the rule text — the document 'makes the document unreadable' — and §7.1's quarantine fixes unreadable as ignore-record with a SHOULD-report, so two implementations reading §18.2 handle the byte sequence identically whether or not the register enumerates it. The gap is a missing corpus vector under [R-ERR-02], not a fork in behavior.

### RD-11 — OBSERVATION

**Location.** §21.8 [R-ERR-02]; §21.1 Instances paragraph; §21.3 row L2

I recounted every Instances cell mechanically and §21.8's figures are exact — 39 + 50 + 26 + 10 = 125 conditions and 61 + 100 + 45 + 36 = 242 instances — but the word 'named' is wrong for 51 of them, and two of L2's instances are files that cannot exist on their own, contrary to §21.1's distinguishability rule.

> Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical once the cell is written. One instance is one *distinguishable* file: where a condition is a single predicate over several fields — a sum against a bound, a combination of two flag bits — the fields it reads are not instances, because no two files could differ.

> Every row of §21.2 through §21.5 — 125 conditions over 242 named instances — has at least one conformance vector (§24) whose expected verdict is that row's outcome

> | L2 | A declaration-derived sum or product of a layer exceeds 2^63 - 1 although every contributing field is in domain | extent_offset + extent_length; N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N; max disk ordinal (C−1)·N + (N−1); V = P·C; P·Q; P·Bᶜ; entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | reader | layer access | `[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07) |

**Picked.** The totals are right; two of L2's ten instances should be struck, which would make the corpus 240, and 'named' should read 'enumerated' or simply 'instances'.

**Rationale.** On the wording: 51 cells read '—' and name nothing, yet §21.1 counts each as one instance, and only counting them reaches 242 — so §21.8's arithmetic silently uses the rule its own adjective contradicts. On L2: the max disk ordinal is (C−1)·N + (N−1) = C·N − 1, so it can exceed 2⁶³ − 1 only when C·N does, and C·N is already an instance in the same cell — no file can exhibit the one without the other. Likewise V = P·C arises only in an interleaved layer, where the decoded size is P·Q with Q = ΣBᵢ ≥ C, so P·C overflows only when P·Q does, and P·Q is also in the cell. Both fall under 'no two files could differ'. The rest of L2 survives: N, P, N·P, P·Bᶜ and the index-length formula are each independently reachable.

**Byte-level?** no — Nothing here touches a file's content. [R-ENC-04] gives one outcome — 'a validity error at the owning scope' — for every quantity in the cell, so a reader that overflow-checks the products it computes behaves identically whether L2 has eight instances or ten. The consequence is two corpus files that duplicate others.

### RD-12 — OBSERVATION

**Location.** §21.9 [R-ERR-03], [R-ERR-04]; §2.5 [R-CNF-10]; §24 [R-VEC-03]

§21.9's minimum guarantees are stated per quantity with no composition rule, so read literally a file combining them — 65,536 layers each declaring 2³² addressed tiles — has every quantity within bounds and a conforming reader MUST accept it, though its index regions alone run to several petabytes.

> The table below states **minimum guarantees**, not caps: a conforming reader MUST accept any conforming file whose quantities lie within these bounds, and a writer MAY rely on that. `[R-ERR-03]`

> | addressed tiles per layer (entry_count) | 2³² |

> | layers per file | 65,536 |

> Software that declines a file whose every quantity lies within the table is not a conforming reader (`[R-CNF-03]`) — the guarantees are the floor, not a suggestion.

**Permitted readings.**

1. Each row binds independently, so any file all of whose quantities are individually within bounds must be accepted, however they combine.
2. The rows bind one at a time against an otherwise ordinary file, and a reader may decline a combination under [R-ERR-04] without forfeiting conformance.

**Picked.** Reading 1, because that is what 'any conforming file whose quantities lie within these bounds' says and [R-ERR-04]'s only stated escape is for a file 'exceeding any of these' — which a combined file does not do.

**Rationale.** Under reading 1 a conforming reader is obliged to accept a file whose tile indexes total roughly 5.6 PB (2³² entries × 20 bytes × 65,536 layers), and any implementation that declines it 'is not a conforming reader'. §21.9's own note prices the rows in isolation — '2³² addressed tiles is the point where the segment-CRC array a reader fetches whole before using any entry (§15.4) is still 256 KiB; 65,536 layers is roughly a 12.5 MiB directory' — which shows the intent was reading 2, but no text states it. §24 concedes the tile-count bound alone is already unbuildable — 'its index region alone running to tens of gigabytes of incompressible entries' — without addressing what happens when the bounds are combined.

**Byte-level?** no — This does determine which files a conforming reader must accept, which is the right shape for a byte-level finding, so I checked whether the disagreement is exercisable. It is not: no such byte sequence can be produced or served, and §24 already declines to build a vector even at the single-row bound. The two readings can never be distinguished by any file two implementations could both be handed, and [R-ERR-04] in either reading requires a refusal to be 'reported as a resource limit and not as a validity error', so no reader mislabels intact bytes as corrupt.
