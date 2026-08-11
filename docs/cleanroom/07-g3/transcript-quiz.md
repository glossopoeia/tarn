# Cleanroom round 7 — quiz, key, and adjudication

Slate authored by one agent, answered by a second, keyed by a third, each blind to the others'
output and each reading `spec/tarn.md` alone. A divergence indicts the key as readily as the answer.

## Result: 15 agree / 0 diverge / 0 underdetermined

### Q1 — AGREE

**Taker.** 10 files

**Key.** 10 files

**Adjudication.** Spec supports both. §21.1: "Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical once the cell is written." I counted R4's cell in §21.5 directly: it holds exactly ten semicolon-separated items (missing frame magic / a skippable frame / a second frame / a nonzero dictionary ID / the content-checksum flag set, each × top-level extent and layer sub-record extent). §21.8 [R-ERR-02] "a row naming instances has one vector per instance"; §24 [R-VEC-02] "Each vector is one file plus a manifest entry"; §24 [R-VEC-03] "at least one vector for each instance it names". R4's outcome is ignore-record, so [R-VEC-04]'s intact-sibling rule (reject-layer/reject-tile only) adds nothing. Minimum and required count: 10. The taker derives 10 as 5 alternatives × 2 containers and the key by direct semicolon count; §21.1 licenses both framings ("a condition applying to two alternatives in two containers has four"). Note one mis-citation by the taker: the instance-counting paragraph in §21.1 is not tagged [R-CNF-07] (that identifier lives in §2.4); the paragraph is untagged prose in §21.1. Does not affect the answer.

### Q2 — AGREE

**Taker.** reject-layer; reader; layer-access tier

**Key.** reject-layer; reader; layer-access tier

**Adjudication.** Spec supports both. 0x0400 is in the record-type reserved range 0x0003–0x7FFF (§10.2 table). Two §21.3 rows describe it: L25 (reserved-range sub-record type with MU = 1 — reader, layer access) and L26 (reserved-range sub-record type whatever the MU bit — verifier, certification); both sit in §21.3, whose outcome is reject-layer. §21.1 decides the pair verbatim: "Some rows are strict specializations of others — F2 of F8 and of F10, F38 of F39, L25 of L26 — and a file exhibiting a specialization is recorded against the narrower row, whose detector and detection point are the ones that apply." L25 therefore governs: reader, layer access. §7.4 [R-CNT-18] confirms substantively — "an unknown sub-record type with MU = 1 is reject-layer — never reject-file" — and §10.3 [R-EXT-03] routes reserved-range record types to [R-CNT-18] for layer sub-records. §19.2 [R-RDR-02] names the tier "at first access to a layer". PRESERVE_ON_EDIT = 1 is inert here ([R-CNT-12] would impute it anyway); the key says so explicitly, the taker leaves it implicit.

### Q3 — AGREE

**Taker.** cannot establish; file conforming

**Key.** cannot establish; file conforming

**Adjudication.** Spec supports both. 0x9000 ≥ 0x8000, the record-type experimental range (§10.2 table). §2.3 [R-CNF-11] lists cannot establish "when a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and "a verifier MUST NOT certify a file it reports that way." §21.6's closing text is decisive on the second half: an experimental-range record type carrying MU = 1 is one of two "conforming files a reader nevertheless refuses" — "[R-CNT-15] obliges the reader to reject, and [R-CNF-02] makes the file conforming all the same, since the prohibition on publishing experimental values binds a writer's conduct and not the bytes" — and that is also why it carries no register row. Both agents identify the no-row point correctly. The key additionally justifies PE = 1 from the byte-perfect stipulation plus [R-CNT-12]; immaterial to the verdict.

### Q4 — AGREE

**Taker.** yes; layer; resource limit

**Key.** yes; layer; resource limit

**Adjudication.** Spec supports both. §21.9's table guarantees rank d of 32, so d = 40 is outside the minimum guarantees; §2.3 [R-CNF-03] binds a reader only to conforming files "none of whose values exceeds the minimum guarantees of §21's limits table", so the acceptance obligation does not reach this file and the reader stays conforming. §21.9 [R-ERR-04]: "A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose declarations exceed what it can serve, a layer or a tile." Rank is a layer-record inline-payload field (§7.4) whose owning scope is the layer (§11.1: "The owning scope (§2.4) of a layer's geometry and linearization fields is the layer"), so the layer is the narrowest available scope — tile is unavailable because no tile declaration carries the excess (the key states this explicitly; the taker implies it). Category is fixed by [R-ERR-04]: "a refusal on resource grounds MUST be reported as a resource limit and not as a validity error." The taker's citation of §2.5 [R-CNF-10] is apt as supporting context.

### Q5 — AGREE

**Taker.** reject-file; yes, verdict changes

**Key.** reject-file; yes, verdict changes

**Adjudication.** Spec supports both, including the second half. §6.1's table makes bytes [8, 16) "zero", so 0x01 at offset 8 breaks the constant block (register row F8's second instance, "reserved bytes [8,16)", reader, open). §6.1 [R-CNT-04] names this exact residency case: a reader whose open leaves [0, 16) resident — "a local file, a memory mapping, a speculative suffix window that reached offset 0, or any transport already holding them" — "MUST verify the full block by byte equality before other processing, and MUST treat any mismatch as reject-file." A 65,536-byte suffix window against a 20,000-byte file reaches offset 0, so the obligation binds: reject-file. On the counterfactual, [R-CNT-04] continues: "A reader that would have to issue a further range request to obtain those bytes MAY defer or omit the check", repeated at §19.1 step 1 — so the two-exact-range reader is under no obligation and completes the open. Both agents also correctly separate reader obligation from file conformance: §2.3 [R-CNF-02] makes file conformance "a pure predicate on bytes", so the file is nonconforming under either open path. Appendix A's closing paragraph makes the same residency point for the 128-byte file.

### Q6 — AGREE

**Taker.** CRC over [262080, 262140); stored bytes at [262140, 262144)

**Key.** same

**Adjudication.** Spec supports both. F = 262,144 and the trailer occupies [F − 64, F) = [262,080, 262,144) (§6.2: "The trailer occupies the final 64 bytes of the file"). §6.2's layout table puts the trailer CRC at trailer offset 60, size 4, "CRC-32C over trailer bytes [0, 60)" — absolute [262,080, 262,140) covered, stored at absolute [262,140, 262,144). Order is fixed by §6.2 [R-CNT-06]: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate (§6.3)", so the CRC must pass before the reader acts on version_major = 7 (§6.3 [R-CNT-07] rejects an unimplemented major). §6.3 [R-CNT-24] is what makes this checkable at all under an unimplemented major: "In every format major version, permanently: the final 64 bytes of a file contain the trailer magic at F − 64, version_major and version_minor at F − 56, and a CRC-32C at F − 4 covering bytes [F − 64, F − 4)". Both agents cite it. The key adds the [R-CNT-10] caution that F must be transport-authoritative rather than read from committed_file_length — correct and a genuine refinement, since committed_file_length sits in the 48 bytes a future major may redefine; the taker does not contradict it.

### Q7 — AGREE

**Taker.** reject-file at open

**Key.** reject-file at open

**Adjudication.** Spec supports both. §19.1 step 4 states it almost verbatim: "A duplicate layer name is a validity error at file scope, here, at open ([R-ENC-15], §19.2). Uniqueness is decided first, and over the raw name bytes whether or not each name is itself well-formed — [R-ENC-12] makes name comparison a byte comparison, which needs no valid name — so two layers whose name fields are byte-identical are a duplicate even when neither name is valid." §4.6 [R-ENC-15] independently assigns file scope ("a duplicate layer name is a file-scope error (reject-file)"), and §2.4 [R-CNF-08] maps file scope to reject-file. The competing condition, ill-formed UTF-8 in a layer name, is row L4 (reject-layer, reader, open, [R-ENC-11]) and is subsumed: §2.4 says of reject-file "A reader MUST NOT rely on any structure in it." Both agents reach reject-file at open. One citation nit: the byte-comparison rule is [R-ENC-13] ("Name comparison is raw bytes"); §19.1 step 4 attributes it to [R-ENC-12], and the key follows §19.1's attribution while listing [R-ENC-13] separately. That misattribution is in the spec's own prose, not in either agent's reasoning, and changes nothing — [R-ENC-12] and [R-ENC-13] are adjacent halves of §4.6's name rules.

### Q8 — AGREE

**Taker.** length = 2; crc over the 2 stored bytes as stored

**Key.** same

**Adjudication.** Spec supports both, and the arithmetic checks out. P = ∏Tᵢ = 3 · 3 = 9 (§11.2 [R-GEO-03]). A planar bool plane is bit-packed with "the decoded size is ⌈P/8⌉ bytes" = ⌈9/8⌉ = 2 (§14.3 [R-SER-03]). Filter 1 is none — "the filtered image is the decoded image" (§17.3 [R-COD-09]) — and codec 1 is none: "The stored bytes are the filtered image verbatim. The index entry's length therefore MUST equal the tile's decoded size" (§17.2 [R-COD-04]), "checkable from the entry and the layer record alone, before any payload fetch." So length = 2 exactly. The crc: §15.1's entry table gives "CRC-32C of the stored tile's bytes (§8.1)", §8.1's map gives "Stored tile | the crc field of its index entry | the tile's stored bytes", and §8.1 [R-CNT-19] fixes "All checksums are CRC-32C over bytes exactly as stored" — here the 2 bytes at [offset, offset + 2), which under codec 1 / filter 1 coincide with the packed decoded image. The key's extra observation is right and worth keeping: P mod 8 = 1, so the final byte carries six pad bits, and §14.5 [R-SER-05] requires each to carry the channel's fill bit — those bits are inside the checksummed 2 bytes.

### Q9 — AGREE

**Taker.** reject-tile, tile scope, reader (tile use)

**Key.** same, row T21

**Adjudication.** Spec supports both. Decoded size = P · Bᶜ = 9 · 2 = 18 for a planar uint16 plane (§11.2 [R-GEO-03], §14.2 [R-SER-02]). Every other stipulated feature is compliant with §17.2 [R-COD-06]: the magic 28 B5 2F FD is present, one frame only, no dictionary ID, no content-checksum flag, and Frame_Content_Size = 18 satisfies "when present it MUST equal the tile's decoded size." The violation is the window: [R-COD-06] — writers "MUST NOT declare a window size exceeding the tile's decoded size; a reader MUST treat either as a validity error at tile scope, both being header-checkable" — and 1024 > 18. That is register row T21 (§21.4: "Codec 3 (zstd) and the frame declares a window size larger than the tile's decoded size", reader, tile use), outcome reject-tile per §21.4's heading. Both agents identify §17.2's note as the explanation of the corner: with Single_Segment_Flag clear "the Window_Descriptor cannot express less than 1 KiB", so a sub-1-KiB tile "is therefore encodable under codec 3 only as a single-segment frame." The key correctly rules out the §21.9 8 MiB Window_Size guarantee as a red herring — that governs a conforming wide window and an [R-ERR-04] resource decline, not this violation.

### Q10 — AGREE

**Taker.** reject-layer, layer scope, layer access; quarantine does not change it

**Key.** same, row L12

**Adjudication.** Spec supports both. Inline side is clean: §18.2 [R-MTA-03] fixes inline_length at exactly 1 and encoding 1 = none is assigned. The defect is the extent slot. §7.1 [R-CNT-25]: an extent "whose extent_length is less than 5 — too short to hold both a document and the terminal CRC-32C §8.1 places in its final 4 bytes — is a validity error at its containing scope." For a sub-record that scope is the layer (§7.2 [R-CNT-13]: the scope the record governs is "the layer for a layer record and for sub-records"; §7.4 [R-CNT-18]: "Sub-records are layer-scope records"), and §2.4 [R-CNF-08] maps layer scope to reject-layer. Register row L12 records exactly this (reader, layer access, [R-CNT-25]). On the quarantine, §18.1 [R-MTA-02] is dispositive and both agents quote it: "The quarantine covers the document only: a malformed extent slot on such a record, (0, 0) included, is a validity error at the record's containing scope ([R-CNT-13], [R-CNT-25]), because that failure precedes the document." Detection tier is §19.2's "at first access to a layer" — note that the extent-use tier does not apply, because the failure is in the slot, read during §19.3's layer validation, not in the extent's contents.

### Q11 — AGREE

**Taker.** 2,120

**Key.** 2,120

**Adjudication.** Spec supports both; I recomputed independently and got 2,120. G = (⌈1024/256⌉, ⌈2048/256⌉) = (4, 8), N = ∏Gᵢ = 32 (§11.2 [R-GEO-03] — and §11.2's worked example uses this exact layer). Tile coordinates tᵢ = xᵢ div Tᵢ = (300 div 256, 700 div 256) = (1, 2) (§11.4 [R-GEO-06]). Under linearization 1, s = Σᵢ tᵢ · ∏_{j>i} Gⱼ = 1·8 + 2 = 10 — §11.4's worked example gives s = 10 for (300, 700) explicitly. Planar disk ordinal = c · N + s = 3 · 32 + 10 = 106 ("c · N + s for a planar layer … channel-major grouping"). §15.1 [R-IDX-01]: "The entry for the tile with disk ordinal k (§11.4) is the k-th entry, at region byte 20·k" → 20 · 106 = 2,120, entry occupying [2,120, 2,140). Both agents' chains are identical; the key states the closing interval, the taker the start offset the question asked for.

### Q12 — AGREE

**Taker.** FF 00 00 for tile A; no sample values for tile B

**Key.** same

**Adjudication.** Spec supports both. Tile A: §19.4 [R-RDR-04] step 4 — "A valid sentinel short-circuits steps 5 and 6 for that entry: every requested sample position of its tile reads as fill — the entry's channel's recorded fill in a planar layer; each carried channel's, in declared order, in an interleaved layer — bit-exactly and with no payload I/O ([R-TYP-06], [R-TYP-08])" — so 0xFF, 0x00, 0x00 in declared order r, g, b. §13.3's worked example is this exact layer and gives the tuple (255, 0, 0). Tile B: a stored tile failing its entry's crc is reject-tile (§15.3's table row "stored bytes fail the entry's crc", §8.2 [R-CNT-20]), and fill is barred as a fallback by §2.4 [R-CNF-09] ("a read of a rejected tile MUST NOT silently return fill") and §13.3 [R-TYP-09] ("Fill is produced by exactly one condition: a sentinel entry read from a verified index chain"). §19.4 step 8 gives the permitted latitude: "the reader MAY return the validating entries' values together with a per-entry report of the failed ones, or fail the request as a whole, but MUST NOT stand fill in for a rejected tile's positions." Both agents state both halves correctly; the key spells out the consequence that failing the request whole also withholds tile A's values, which is implied by step 8 and not contradicted by the taker.

### Q13 — AGREE

**Taker.** F = 192; 51 bytes of pad

**Key.** F = 192; 51 bytes of pad

**Adjudication.** Spec supports both; arithmetic verified. The directory region is dir_length bytes at dir_offset (§7.1), so it occupies [16, 77) — dir_length includes the terminal 4-byte CRC ("Its final 4 bytes are a CRC-32C over the preceding dir_length − 4 bytes"). §9.2 [R-LIF-02] step 5: "append the pad to the next 64-byte boundary … and the new trailer, with generation one greater than the prior trailer's and committed_file_length equal to the new end" — next multiple of 64 at or above 77 is 128, so pad = 128 − 77 = 51 bytes, trailer at [128, 192), F = 192. Every §6.2 gate holds: F mod 64 = 0 ([R-CNT-01]), dir_offset = 16 ≥ 16, dir_length = 61 ≥ 4, dir_offset + dir_length = 77 ≤ F − 64 = 128 ([R-CNT-06]). The key adds the point that makes 51 determined rather than a floor, quoting §6.2 [R-CNT-05]: the spec "bounds their number only through step 5 of the commit protocol, which pads to the next 64-byte boundary ([R-LIF-02]) — a longer gap is conforming, and no conforming commit produces one." The question stipulates the protocol is followed exactly, so 51 is the answer; the taker reaches it by the same route without naming the caveat.

### Q14 — AGREE

**Taker.** conforming (verifier certifies)

**Key.** conforming (verifier certifies)

**Adjudication.** Spec supports both on the asked question. §17.3 [R-COD-10]: "A writer that filters with any other stride violates this rule; where the resulting decoded image breaks a stated content obligation (§14.5's padding, [R-SER-08]'s bool bytes) a verifier detects it as a validity error at tile scope, and otherwise the consequence is wrong sample content — undetectable by construction (§21.7)." Both escape hatches are closed by the stipulations: every extent an exact multiple of its tile extent means Gᵢ·Tᵢ = Eᵢ, so §11.3 [R-GEO-04] yields no padding positions and §14.5 [R-SER-05] has no witness; no bool channel closes [R-SER-08] and row T2. A stride-4 shuffle is still a length-preserving permutation, and the reader's stride-5 inverse is too, so §14.3 [R-SER-07]'s exact decoded-size check passes and §8's chain verifies over what the writer wrote. §21.7 [R-ERR-01] names this case in terms: "a mis-strided filter ([R-COD-10]) … produces a file that every checksum in §8 certifies." The verifier can execute codec and filter, so [R-COD-11]'s cannot establish is unavailable. Verdict: conforming. One substantive divergence in the agents' *notes*, which the question did not ask about but which is worth resolving: the taker asserts "The file is in fact nonconforming (a writer MUST was violated)"; the key leaves the framing open. The spec decides against the taker. §2.3 [R-CNF-02] makes file conformance "a pure predicate on bytes", and a mis-strided store is byte-identical to the correctly-strided store of a different intended image — there is no byte sequence that is nonconforming by virtue of stride, so the predicate is satisfied. §2.4 [R-CNF-12] closes it from the other side: "a verifier certifies only violation-free files", so a spec that both obliges certification here and calls the file nonconforming would contradict itself. The file is conforming; §21.7 groups the mis-strided filter with "simply wrong data", which is uncontroversially conforming. Not a spec defect — determined by [R-CNF-02] plus [R-CNF-12], though only by inference, which is why the key's hedge is reasonable and the taker's flat assertion is the error.

### Q15 — AGREE

**Taker.** version_minor 3; generation 1; bit 20 only

**Key.** version_minor 3; generation 1; bit 20 only

**Adjudication.** Spec supports both on all three. §20.5 [R-WRT-06] fixes generation and minor: a compactor emits "a fresh file_id for the output … and generation 1: a compacted file is a whole-file rewrite under a new file_id by definition ([R-LIF-01])", and "The output trailer copies the input's unknown ignore-lane flag bits forward ([R-CNT-08]) and carries the greater of [R-CNT-26]'s floor and the input's version_minor — a compactor cannot know which minor version defined an ignore-lane bit it does not implement, so it does not lower the floor beneath one." §6.3 [R-CNT-26] sets the floor at "the lowest version_minor that defines every feature present in the file — for a file expressible under this text, 0"; the live state is stipulated to use no undefined feature, so floor = 0 and max(0, 3) = 3. Flags: bit 20 is in the ignore lane (bits 16–31, §6.2 table), and §6.3 [R-CNT-08] is categorical — "An updater MUST copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear them" — while no incompat-lane bit (0–15) can be set, since "an updater encountering an unknown incompat-lane bit is a reader first, and therefore rejects the file before modifying anything", and this text defines no bits in either lane. So flags = 0x00100000 exactly. Both agents also correctly note that file_id must be a fresh draw, not X, and that generation resets rather than continuing from 7 — §20.5's figure shows precisely file_id X / generation 7 in, file_id Y / generation 1 out.
