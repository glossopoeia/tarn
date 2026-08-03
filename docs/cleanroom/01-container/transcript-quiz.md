Below are the quiz answers, each with citations and confidence, followed by the consolidated defect list. All citations are to `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.

---

**Q1 — Smallest conforming file, byte by byte**

Size is exactly 128 bytes. Derivation: front block is 16 bytes at offset 0 (§6.1 [R-CNT-04]); dir_offset ≥ 16, dir_length ≥ 4 (§6.2 table, [R-CNT-06]); only a <64-byte zero pad may sit between directory end and trailer ([R-CNT-05]); the trailer is 64 bytes and F must be a multiple of 64 ([R-CNT-01], §6.2). Minimum content 16+4+64 = 84 → next multiple of 64 = 128. The §5.1 Example states this layout explicitly (non-normative but exactly consistent with the normative constraints).

| Offset (hex) | Bytes | Meaning | Determined? |
|---|---|---|---|
| 0x00–0x07 | `89 54 41 52 4E 0D 0A 1A` | front magic (§6.1) | yes |
| 0x08–0x0F | `00` ×8 | front reserved zero (§6.1) | yes |
| 0x10–0x13 | `00 00 00 00` | empty directory: CRC-32C of zero bytes = 0x00000000, LE (§5.1 Example; §7.1 [R-CNT-11]; §4.5 [R-ENC-09]) | yes |
| 0x14–0x3F | `00` ×44 | pre-trailer pad, must be zero ([R-CNT-03], [R-CNT-05]) | yes |
| 0x40–0x47 | `8A 4E 52 41 54 0D 0A 1A` | trailer magic (§6.2) | yes |
| 0x48–0x49 | `01 00` | version_major = 1 (§6.2, §6.3 [R-CNT-07]) | yes |
| 0x4A–0x4B | — | version_minor | **NOT determined** — any u16 ("any (see §6.3)", §6.2 table; [R-CNT-07] forbids minor-based rejection) |
| 0x4C–0x4F | `00 00 00 00` | flags = 0 ("a writer creating a file MUST write flags = 0", [R-CNT-08]; this file's one trailer is a creation trailer, §9.2) | yes (see AMBIGUITY 1) |
| 0x50–0x57 | `01 00 00 00 00 00 00 00` | generation = 1 (creation is generation 1, §9.2; a 128-byte file cannot hold a chain deeper than 1, [R-LIF-08](a)) | yes |
| 0x58–0x5F | `10 00 00 00 00 00 00 00` | dir_offset = 16 (forced by byte coverage [R-CNT-02] + §5.1 Example) | yes |
| 0x60–0x67 | `04 00 00 00 00 00 00 00` | dir_length = 4 | yes |
| 0x68–0x6F | `80 00 00 00 00 00 00 00` | committed_file_length = 128 ([R-CNT-01]) | yes |
| 0x70–0x77 | — | file_id | **NOT determined** — any u64 ≠ 0 (§6.2 table, [R-CNT-06]); SHOULD (not MUST) be cryptographically random ([R-LIF-03]) |
| 0x78–0x7B | `00 00 00 00` | trailer reserved zero (§6.2, [R-CNT-06]) | yes |
| 0x7C–0x7F | — | trailer CRC: CRC-32C over bytes [0x40, 0x7C) (§6.2, §8.1) | **functionally determined**: a fixed function of the version_minor and file_id choices, not a constant |

Undetermined bytes, exactly: 0x4A–0x4B (version_minor, any u16), 0x70–0x77 (file_id, any nonzero u64), 0x7C–0x7F (CRC — uniquely determined once the first two are chosen). Confidence: certain, except flags (inferred — AMBIGUITY 1) and the note that "smallest" is unique in size but not in bytes (OBSERVATION 1).

**Q2 — 10,000,000-byte file, dir_length = 2,000**

10,000,000 = 64 × 156,250, so F is validly a multiple of 64 ([R-CNT-01]).

- Request 1: the final 64 bytes — [9,999,936, 10,000,000) (bytes 9,999,936–9,999,999 inclusive). §6.4 [R-CNT-09].
- Request 2: [dir_offset, dir_offset + 2,000), where dir_offset is read from the validated trailer. §6.4 [R-CNT-09]. The spec does not pin dir_offset to a single value: [R-CNT-05] (pad < 64) plus §9.2 step 5 (pad to next 64-boundary) confine it to dir_offset ∈ [9,997,873, 9,997,936] — 64 admissible values. Under the maximal (pad = 0) placement, request 2 is [9,997,936, 9,999,936).
- Directory CRC: the final 4 bytes of the region — [dir_offset + 1,996, dir_offset + 2,000), covering [dir_offset, dir_offset + 1,996) (§7.1 [R-CNT-11], §8.1). Under the maximal placement: CRC at [9,999,932, 9,999,936) covering [9,997,936, 9,999,932).
- Largest conforming dir_offset: **9,997,936** (directory ends exactly at F − 64 = 9,999,936, pre-trailer pad = 0; satisfies dir_offset + dir_length ≤ F − 64 of [R-CNT-06] with equality, and [R-CNT-05]).

Confidence: certain (the interval for dir_offset is a derivation, also certain; see OBSERVATION 2 on request 2 not being a constant).

**Q3 — generation = 0**

Outcome: reject-file. [R-CNT-06] requires validating "generation ≥ 1 … Any failure is reject-file"; the §6.2 table gives generation's valid values as ≥ 1; §9.3 [R-LIF-03] requires g ≥ 1. Actors: every reader — and updaters and verifiers are "readers of the files they process" (§4.2 [R-ENC-04] parenthetical), so an updater rejects before modifying anything (cf. the same principle stated for incompat flags in [R-CNT-08]) and a verifier treats the file as nonconforming. A writer opening for append validates the trailer per §6.2, and on failure "the file is torn: the writer MUST NOT append" ([R-LIF-04]). No conforming writer emits it ([R-CNF-05]). Confidence: certain.

**Q4 — version_major = 3**

The reader validates magic, then CRC, then hits the version gate and MUST reject-file ([R-CNT-06] order; [R-CNT-07]). Its diagnostic SHOULD be distinct from both "not a TARN file" and "corrupt" — e.g. "TARN format major 3; this reader supports major 1" ([R-CNT-07], with the stated consequence of deviating). It is entitled to interpret exactly the fields whose positions are fixed across all majors ([R-CNT-24]): the trailer magic at F − 64, version_major and version_minor at F − 56, and the CRC-32C at F − 4 covering [F − 64, F − 4). Everything else — flags, generation, dir_offset, dir_length, committed_file_length, file_id, reserved — sits in the 48 bytes a future major MAY redefine ([R-CNT-24]), so a major-1 reader must not interpret them. [R-CNT-06] says explicitly that only the three ordered gates "touch fields whose positions are fixed across all majors". Confidence: certain.

**Q5 — transport size 1,048,640 vs committed_file_length 1,048,576**

Walk: (1) fetch final 64 bytes [1,048,576, 1,048,640) ([R-CNT-09]); (2) magic verifies; (3) trailer CRC verifies; (4) version gate passes (assume major 1); (5) the reader must now validate "committed_file_length equals the file size (for a remote reader, the size reported by its transport)" — 1,048,576 ≠ 1,048,640 → **reject-file** ([R-CNT-06]). The reader MUST NOT substitute the trailer's committed_file_length for the transport size ([R-CNT-10]), and MUST report the file torn or invalid and MUST NOT scan backward ([R-LIF-05] — "trailer-at-end-or-fail"). A non-normative note permits retrying the validation once on shared filesystems with attribute-cache staleness (§9.5 Note). Locating the real last committed state (plausibly a genuine trailer at [1,048,512, 1,048,576)) is the deliberate recovery operation of §9.6, performed by tools and verifiers, never by a reader on the default path ([R-LIF-06]). Confidence: certain. (See OBSERVATION 3: this end-of-file candidate would also fail §9.6's recovery criterion committed_file_length = o + 64, marking it a payload mimic.)

**Q6 — layer record (0x0001) with stored MU = 0**

Reader: applies the layer record's specified semantics unchanged — "A reader MUST apply a known type's specified semantics regardless of its stored MU and PE bits — a flipped stored bit never changes conforming behavior" ([R-CNT-22]; registry fixes layer = MU 1, PE 1, §7.3 table). Every conforming reader implements type 0x0001 ([R-CNF-03] core obligations; stored bits are authoritative only for types the consuming tool does not implement, [R-CNT-22]/[R-CNT-15]). Verifier: SHOULD report the mismatch — "unreported, a writer defect propagates silently to consumers that do not know the type" ([R-CNT-22]). No reject outcome is assigned at any scope. Note [R-CNT-12]'s forced-PE rule concerns the different combination MU = 1/PE = 0. Confidence: certain for behavior; the file's conformance classification is AMBIGUITY 3.

**Q7 — planar, extents (512, 512), tiles (256, 256), C = 3, index_encoding 1**

- G₀ = G₁ = ⌈512/256⌉ = 2; N = 4 spatial tiles ([R-GEO-03]).
- Addressed-tile count for planar = C · N = 3 · 4 = 12, and entry_count must equal it: **entry_count = 12** ([R-GEO-03]; §7.4 table; [R-CNT-17]).
- **extent_length = 12 × 20 + ⌈12 / 2¹⁶⌉ × 4 = 240 + 4 = 244 bytes** ([R-CNT-17]).
- **Segment-CRC array = 4 bytes** (one CRC-32C for one segment): the ⌈entry_count/2¹⁶⌉ × 4 term of [R-CNT-17], which §8.1's coverage map identifies as "the per-segment CRC array, itself covered by the layer record's crc_of_crc_array".

Confidence: entry_count and extent_length certain; segment-CRC array size inferred (the formula and §8.1 determine the size; §15, which owns the layout, is [Reserved] — see AMBIGUITY 4 on placement).

**Q8 — two layer records named `64 65 6D` ("dem")**

Name comparison is raw bytes, so identical byte sequences are the same name ([R-ENC-13]). Layer names are unique per file; "a duplicate layer name is a file-scope error (reject-file)" ([R-ENC-15], reaffirmed in [R-CNT-23]'s exception clause). Outcome: **reject-file**; scope: the entire file, not just the two layers. Confidence: certain.

**Q9 — dir_offset = 16, dir_length = 100**

Directory region is [16, 116). Its CRC is the final 4 bytes, **[112, 116)**, and covers the preceding dir_length − 4 = 96 bytes, **[16, 112)** — the raw record sequence (§7.1 [R-CNT-11]; §8.1 coverage map). Confidence: certain.

**Q10 — locating generation 3's directory in a generation-5 file**

First, this is not a reader behavior: only recovery tools and verifiers do it, "never conforming readers on the default path" ([R-LIF-06], [R-LIF-05]). Procedure: probe backward from the end at 64-aligned offsets o for the trailer magic; each candidate must satisfy trailer-CRC verification and committed_file_length = o + 64 (§9.6 [R-LIF-06]); continue the probe toward offset 0 and accept only the set forming a chain — exactly one candidate per generation number from 5 down to 1, committed_file_lengths strictly increasing, each equal to its candidate's offset + 64, each candidate's directory bounds inside its own committed length ([R-LIF-08](a)). Take the chain member with generation = 3; its dir_offset/dir_length locate generation 3's directory; verify that directory's CRC before any other use ([R-CNT-11], [R-ENC-10]). The hazard the text warns about: **a tile payload can deliberately contain a byte string that mimics a valid trailer** — so recovery output MUST be re-verified as a whole file before being trusted, and off-chain candidates are discarded as payload mimics ([R-LIF-06]; [R-LIF-08](a)). Confidence: certain.

**Q11 — zero-layer file**

Conforming: yes. "any number of layer records (zero is valid: an empty directory is a conforming generation)" ([R-CNT-14]); the §5.1 Example calls the 128-byte file "a valid, empty file". Minimum size: **128 bytes**, because the front block is 16 bytes, the directory is at least 4 (dir_length ≥ 4, [R-CNT-06]), the trailer is 64, and F must be a multiple of 64 ([R-CNT-01]) — 84 rounds up to 128. Confidence: certain.

**Q12 — index compression; user-metadata encoding declaration**

A tile-index region is compressed under **no circumstances**: "The directory and the tile-index region are always raw (the index so that it can be range-fetched, §15)" ([R-CNT-25]). The encoding of a user-metadata document is declared by **the user-metadata record itself, in its own payload**, as a u8 (0 invalid, 1 = none, 2 = zstd) ([R-CNT-25]); an unimplemented encoding value makes that record unreadable with outcome ignore-record, SHOULD be reported ([R-CNT-25]). Confidence: certain; the exact byte position of that u8 within the payload is §18's subject, which is [Reserved] — the-text-does-not-say (see OBSERVATION 4).

**Q13 — front-block byte 12 = 0x01**

Byte 12 lies in the front block's reserved-zero field (§6.1 table: offset 8, size 8, value zero). Local reader: MUST verify the full 16 bytes by byte equality before other processing; any mismatch → **reject-file** ([R-CNT-04]). Remote reader that never fetched the front block: proceeds normally — "a remote reader MAY defer or omit this check (its open path is anchored at the trailer, §6.2, and the two-request accounting of §6.4 does not include the front block)" ([R-CNT-04]). Are both conforming? **Both reader behaviors are conforming** — the divergence is explicitly licensed by [R-CNT-04]. The **file** is not conforming (writers MUST emit exactly those 16 bytes, [R-CNT-04]; conformance is a byte predicate, [R-CNF-02]), and nothing obliges a reader to accept a nonconforming file ([R-CNF-03] obliges acceptance of conforming files only). Confidence: certain.

**Q14 — 92 zero bytes between directory end and trailer**

The bytes are zero, so [R-CNT-03]'s content rule is satisfied; but the pre-trailer pad must be "fewer than 64 bytes" ([R-CNT-05]), and 92 ≥ 64. Reader: concludes nothing is wrong and proceeds — "readers are not obligated to check the gap bound; their check is the dir-bounds rule of [R-CNT-06]" ([R-CNT-05] parenthetical), and dir_offset + dir_length = F − 64 − 92 ≤ F − 64 passes. Verifier: **validity error at file scope** (reject-file / nonconforming) under [R-CNT-05]; equivalently the 92 bytes cannot all be claimed as declared padding, failing the exactly-once coverage of [R-CNT-02]/[R-LIF-08](c). The splitting rules: [R-CNT-05]'s explicit reader/verifier split, backed by the §5.2 Note "Coverage is checked by verifiers, never by readers" (note non-normative; the parenthetical in [R-CNT-05] is normative). Confidence: certain (see AMBIGUITY 5 on whether a reader is *permitted* to reject).

**Q15 — trailer validation ordering**

Fixed order, mandatory ([R-CNT-06]): (1) trailer magic, (2) trailer CRC, (3) version gate (§6.3). Any order after those gates pass, each before acting on the fields involved: flag gates (§6.3); committed_file_length equals the (transport-authoritative) file size and is a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; generation ≥ 1; file_id ≠ 0; reserved bytes zero. The property that makes the fixed-order three special: **they touch only fields whose positions are permanently fixed across all format majors** ([R-CNT-06]: "only these touch fields whose positions are fixed across all majors"; [R-CNT-24]: magic at F − 64, version_major/minor at F − 56, CRC at F − 4 covering [F − 64, F − 4), constant "in every format major version, permanently"). So they are the only checks that can run before the reader knows it implements the file's major; the remaining 48 trailer bytes may be redefined by a future major and are meaningless until the version gate passes. The CRC-before-magic-and-versions-use ordering also satisfies [R-ENC-10]/[R-ENC-05] for everything downstream. Confidence: certain.

---

**AMBIGUITIES**

1. (Q1, §6.2 flags row vs §6.3 [R-CNT-08] vs [R-CNF-02]) Whether nonzero ignore-lane flag bits make a major-1 file nonconforming as bytes. Reading A: the creation-writer rule "MUST write flags = 0" plus [R-CNF-05] makes flags = 0 a property of every conforming major-1 file (no conforming writer/updater chain can produce anything else). Reading B: file conformance is reader-observable bytes; readers MUST ignore the ignore lane, so files with those bits set are conforming. I pick A for the Q1 minimal file — its sole trailer is necessarily a creation trailer (generation 1, §9.2) — so I report flags as determined `00 00 00 00`; under Reading B the 16 ignore-lane bits would join the undetermined list.
2. (Q2, §6.4 [R-CNT-09]) "The exact byte range of each request": request 2's range is not a spec constant — [R-CNT-05] and §9.2 step 5 leave 64 admissible dir_offset values ([9,997,873, 9,997,936]) for F = 10,000,000, dir_length = 2,000. The range is exact only after request 1 is decoded. I answered with the general form plus the maximal-placement instance; the question's own request for "the largest dir_offset" suggests this is intended, but the phrasing permits reading it as expecting one fixed range.
3. (Q6, §7.3 [R-CNT-22] vs §2.3 [R-CNF-02]) A stored-flag mismatch on a registered type: writers MUST emit exact values, so the file violates a writer-side MUST, yet the only stated consequence is a verifier SHOULD-report, with reader behavior explicitly unchanged. Readings: (a) the file is nonconforming and the verifier's report marks it so; (b) the file remains conforming and the report is advisory. I pick (a) — [R-CNF-02] plus the §2.1 Note's pairing discipline read writer prohibitions as file-level constraints — but the absence of a "validity error" phrase (used everywhere else) leaves it open.
4. (Q7, [R-CNT-17]/§8.1 vs §15 [Reserved]) The size of the segment-CRC array (4 bytes here) is decidable from [R-CNT-17]'s formula plus §8.1's coverage row, but its placement within the tile-index region, segment boundaries' exact definition, and entry layout are all forward references into reserved §15. Unresolvable from present text; my answer needed only the size, which is safe. Readings on placement (before vs after the entries) exist; I would not pick either without §15.
5. (Q14, [R-CNT-05] vs [R-CNF-03]/[R-CNF-04]) Readers are "not obligated" to check the gap bound — but may a reader that checks anyway reject? [R-CNF-03] compels acceptance of conforming files only; this file is nonconforming, and rejecting is neither heuristic repair nor value inference ([R-CNF-04]). Reading A: a reader MAY volunteer verifier checks and reject. Reading B: reader outcomes are exhaustively assigned ([R-CNF-07] "every detectable violation named… is assigned exactly one reader outcome") and this violation's assigned detector is the verifier, so a reader should not reject. I pick A (nothing forbids it), but the outcome-assignment machinery reads as if B were intended.

**CONTRADICTIONS**

1. (§8.1 [R-CNT-19] vs its own coverage map) "Every field of every structure is covered by exactly one checksum — the equality-checked front signature block being §4.5's sole exception." Strictly read, the checksum fields themselves — trailer CRC [60, 64) (covers only [0, 60)), the directory region's final 4 bytes, and a user-metadata extent's final 4 bytes — are covered by no checksum, so the "sole exception" claim is false for them. (The segment-CRC array is fine: it is covered by crc_of_crc_array, and crc_of_crc_array by the directory CRC.) Harmless resolution available — a CRC field self-detects its own corruption via verification failure — but the text as written contradicts itself.
2. (§4.5 [R-ENC-10] vs §6.2 [R-CNT-06]) [R-ENC-10]: "A reader MUST verify the checksum covering a field before acting on that field." The trailer magic is covered by the trailer CRC, yet [R-CNT-06] mandates checking the magic *before* verifying that CRC. If equality-testing the magic is "acting on" it, the two rules conflict; resolvable by reading "acting on" as using a value to drive behavior beyond validation (consistent with [R-ENC-05]'s allocate/seek/I/O framing), and the explicit ordering in [R-CNT-06] governs. Both citations stand as a strict-reading conflict.

**OBSERVATIONS**

1. (Q1) "The smallest conforming file" is unique in size (128) but not in bytes: a 128-byte file with, e.g., a nonempty directory ending at or before offset 64 also conforms. The §5.1 Example's layout (empty directory at [16, 20), 44-byte pad) is the one I reported; the free fields (version_minor, file_id, CRC) are the same either way, but the question's definite article cost effort to justify.
2. (Q2) Deriving the 64-value dir_offset interval required combining [R-CNT-05] (pad < 64), §9.2 step 5 (pad to next boundary), and [R-CNT-06] (dir bounds) — no single rule states it.
3. (Q5) The end-of-file trailer in this scenario also fails §9.6's recovery criterion committed_file_length = o + 64 (1,048,576 ≠ 1,048,640), so even a recovery tool discards it as a payload mimic — a nice cross-check, but confirming that the reader-path rejection and tool-path discard agree took three sections ([R-CNT-06], [R-CNT-10], [R-LIF-05], [R-LIF-06]).
4. (Q12) The user-metadata encoding byte's existence, type, and value set are fully normative in [R-CNT-25] even though §18 (the record's own section) is [Reserved]; deciding that this was answerable at all (vs an unresolvable forward reference) required checking that nothing in the answer depends on §18's missing layout.
5. (Q3/Q4/Q5) The trailer table's "Valid values" column, [R-CNT-06]'s validation list, and §6.3's prose overlap almost completely; each answer required confirming they agree (they do) since a divergence would have been a contradiction.
6. (Q1) file_id's upper range: §4.2's 2⁶³ − 1 cap enumerates "offsets, lengths, and extents" only, so file_id ranges over the full nonzero u64 domain — decidable, but only by noticing the cap's enumeration is exhaustive.
