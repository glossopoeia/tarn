# Conforming TARN Verifier — Implementation Plan (from `spec/tarn.md` only)

Scope note before anything else: a verifier **is a reader** — §4.2 says so explicitly ("A reader — including any updater or verifier, which are readers of the files they process", [R-ENC-04]) — so every reader MUST in the spec binds me, *plus* the verifier-only obligations the spec assigns by name ([R-CNT-03] nonzero padding, [R-CNT-05] gap bound, [R-CNT-13] overlap, [R-CNT-22] flag-mismatch reporting, [R-CNT-21]/[R-LIF-08] coverage). Verification never decodes tile payloads: the §3.3 Note states no Part I structure requires decoding sample payloads and that "verifiers … operate on files whose layers they cannot decode." So my verifier needs the CRC-32C function and structure parsers, not codecs.

Verdict semantics I adopt (justified under AMBIGUITY 1): the verifier emits (a) a **certification verdict** — file conformance is "a pure predicate on bytes" [R-CNF-02], so *any* violation of a MUST that constrains bytes, at any owning scope, fails certification — and (b) per-finding **reader-outcome classes** (reject-file / reject-layer / reject-tile / ignore-record, §2.4 [R-CNF-07], [R-CNF-08]) so consumers know blast radius. Per [R-CNF-04] I never repair or infer.

---

## Part 1 — Full verification procedure

**Stage 0 — self-test.** Before touching the file, confirm the CRC-32C implementation (Castagnoli 0x1EDC6F41, reflected, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored LE u32) reproduces the check vector: CRC of `"123456789"` = `0xE3069283` [R-ENC-09, §4.5]. A function that fails this "does not implement this specification's checksum."

**Stage A — preliminaries.**
1. Obtain the physical file size S from the filesystem (transport-authoritative; never from file content, cf. [R-CNT-10]'s principle).
2. Read bytes [0, 16) and compare **by byte equality** to `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes. I am a local reader, so this check is mandatory before other processing; mismatch → **reject-file** [R-CNT-04, §6.1]. A byte-swapped-looking signature is reject-file, never adapted [R-ENC-02].

**Stage B — live trailer** (final 64 bytes). Validate **in the order [R-CNT-06] fixes**:
3. Trailer magic `8A 4E 52 41 54 0D 0A 1A` → mismatch **reject-file** (or "torn", [R-LIF-05]; I MUST NOT scan backward *as my open step* — the backward probe happens later, as the §9.6/§9.7 verifier operation, after the live open verdict is recorded).
4. Trailer CRC: CRC-32C over bytes [F−64, F−60+56) i.e. trailer [0, 60), compare to field at [60, 64) → mismatch **reject-file**.
5. Version gate: version_major must be 1; 0 is invalid; any unimplemented major → **reject-file** with the distinct diagnostic ("TARN format major N…") [R-CNT-07]. version_minor never causes rejection [R-CNT-07]. (Only magic/CRC/version touch cross-major-fixed fields [R-CNT-24].)
6. Flag gates: any set bit in incompat lane (bits 0–15; bit 0 = LSB [R-ENC-08]) → **reject-file**; ignore-lane bits (16–31) are ignored, and are *not* a defect (a future minor may define them — §4.3's growth vehicles) [R-CNT-08]. Then: committed_file_length = S and F mod 64 = 0; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64 (sum checked for overflow per [R-ENC-04]); generation ≥ 1; file_id ≠ 0; reserved [56, 60) zero. Any failure → **reject-file** [R-CNT-06]. Any u64 offset/length/extent field anywhere above 2⁶³−1 → validity error at owning scope [R-ENC-03].
7. Verifier-only: pre-trailer gap g = (F − 64) − (dir_offset + dir_length) must be < 64 [R-CNT-05] and all-zero [R-CNT-03] → violation is a validity error at **file scope**.

**Stage C — live directory.**
8. Read [dir_offset, dir_offset + dir_length). Verify the final 4 bytes are the CRC-32C of the preceding dir_length − 4 bytes **before any other use** → mismatch **reject-file** [R-CNT-11]. The region is always raw — no codec on the open path [R-CNT-11], [R-CNT-25]. Note [R-ENC-05]: no allocate/seek/I/O on any integer before its covering checksum verified — this forces the trailer-CRC-before-directory-fetch and directory-CRC-before-record-parse ordering.

**Stage D — record sequence (top level).**
9. Iterate 24-byte headers + inline payloads [§7.2]. Header or inline payload extending past the sequence → **reject-file** (directory's owning scope is the file, §7.1). Type 0 → **reject-file** [R-CNT-12].
10. Flags: reserved bits 2–15 must be zero from writers; as reader I ignore them; as certifier I record a defect (see AMBIGUITY 2). MU=1 ∧ PE=0: writers MUST NOT emit; I treat the record as PE=1 and record a defect [R-CNT-12].
11. Known types (major 1): 0x0001 layer (MU=1, PE=1), 0x0002 user metadata (MU=0, PE=1) [§7.3]. Stored flags differing from the registry values: apply the type's semantics regardless, **SHOULD report** the mismatch [R-CNT-22].
12. Unknown top-level type: MU=1 → **reject-file**; MU=0 → **ignore-record** (defined condition, not a violation, §2.4) [R-CNT-15].
13. Multiplicity: second file-scope user-metadata record → **reject-file**; order carries no meaning [R-CNT-14].
14. Extent slots: (0,0) = none; otherwise both halves nonzero, extent_offset ≥ 16, extent_offset + extent_length ≤ F − 64, no overflow. Violation → error at the scope the record governs: **reject-layer** for a layer record (and sub-records), **reject-file** for other top-level records (so a malformed slot on the top-level user-metadata record is reject-file) [R-CNT-13, §7.3].

**Stage E — layer record inline payload** (owning scope: layer; every violation below → **reject-layer** unless stated) [R-CNT-23], [R-CNT-18]:
15. Parse in the §7.4 order, requiring exact fit: fixed fields, d dimension entries, C channel entries, trailing fixed fields entirely inside the inline payload; the residue must parse as zero or more complete sub-records with no residue; overrun/truncation/residue → reject-layer [R-CNT-18].
16. Field gates: name per §4.6 (well-formed UTF-8 [R-ENC-11]; non-empty, ≤255 bytes, no U+0000–U+001F [R-ENC-12]); duplicate **layer** name → **reject-file** [R-ENC-15]; layout ∈ {1, 2}; linearization = 1 exactly (0, reserved 2–3, future 4–0x7FFF, and experimental ≥ 0x8000 all → reject-layer) [R-GEO-05]; codec ≠ 0 (full valid set is §17 — Reserved; see Part 4); filter ∈ {1, 2}; A = 0 or a power of two; S; A_slab = 0 iff S = 0, else power of two; **A ≠ 0 ∧ S ≠ 0 → reject-layer** [R-CNT-16]; rank d ≥ 1; C ≥ 1 [R-GEO-01]; dimension names and channel names unique within the layer → duplicate is reject-layer [R-ENC-15]; each Tᵢ ≥ 1, Eᵢ ≥ 0 (extent 0 valid, [R-GEO-02]); fill length must equal the type's element size — parseable via its own u8 length prefix, but *validating* it needs §12 (Reserved); index_encoding = 1 (0 invalid, 2 reserved, ≥0x80 experimental — my handling: reject-layer, see AMBIGUITY 8); crc_of_crc_array = 0 when entry_count = 0 [R-CNT-23].
17. Geometry cross-checks: Gᵢ = ⌈Eᵢ/Tᵢ⌉ computed as Eᵢ/Tᵢ + (1 if Eᵢ mod Tᵢ ≠ 0) — deliberately not (Eᵢ+Tᵢ−1)/Tᵢ, per the §11.2 Note; N = ∏Gᵢ; addressed = N (interleaved) or C·N (planar); any product/sum > 2⁶³−1 → reject-layer [R-GEO-03], [R-ENC-04]. Then entry_count must equal the addressed-tile count, and extent_length must equal entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 (0 when entry_count = 0, in which case the slot must be (0,0), §7.4); mismatch → **reject-layer** [R-CNT-17].
18. Sub-records: §7.2 framing at layer scope; type 0 or framing overrun → **reject-layer**; at most one user-metadata sub-record → second is reject-layer [R-CNT-14]; nesting depth beyond two → reject-layer; unknown sub-record MU=1 → **reject-layer** (never reject-file), MU=0 → ignore-record [R-CNT-18].

**Stage F — per-layer tile index and stored tiles** (chain of trust §8.2, strictly ordered: trailer → directory → crc_of_crc_array → segment CRC array → index segment → index entry → stored tile [R-CNT-20]):
19. Fetch the index region (bounds already validated). Verify crc_of_crc_array (a directory field, already CRC-protected) against the CRC-32C of the segment-CRC array; then each segment CRC against its entries; failure of any index cross-check, the CRC array, or a segment → **reject-layer** [R-CNT-20]. The region is always raw [R-CNT-25]. *The byte placement of the CRC array inside the region, the 20-byte entry's internal layout, and the sentinel encoding are §15 — Reserved. This is a hard forward reference; see Part 4.*
20. For each non-sentinel entry: bounds/invalid-combination checks per §15's table (Reserved), then verify the entry's crc field over "the tile's stored bytes" (§8.1) → mismatch **reject-tile** [R-CNT-20]. A rejected tile must never silently read as fill [R-CNF-09] — my report marks it unreadable, not fill.

**Stage G — user-metadata records.**
21. If an extent is present: verify its final 4 bytes as CRC-32C of the preceding bytes ("the encoded bytes exactly as stored, before decoding", §8.1) → mismatch **ignore-record**, and SHOULD report the loss [R-CNT-20]. The encoding byte in the record's own payload: 1 = none, 2 = zstd; a value I do not implement → **ignore-record**, SHOULD report [R-CNT-25]; 0 is invalid — outcome unstated (AMBIGUITY 3). Document-level checks (key uniqueness etc.) are §18 — Reserved.

**Stage H — live-state overlap** (verifier-only; readers not obligated, [R-CNT-13]).
22. Collect every structure reachable from the live trailer — directory, each layer's index region, each stored-tile extent from live index entries, each user-metadata extent — whichever generation appended them. No two may overlap, and none may touch a metadata structure or the front block/trailer: intra-layer overlap → **reject-layer**; any other overlap → **reject-file** [R-CNT-13]. (Interaction with coverage's exactly-once: CONTRADICTION 1.)

**Stage I–J — generation enumeration and byte coverage** — Part 2 below.

**Stage K — report**: certification verdict; findings each tagged with requirement ID and outcome class; dead-space inventory (report-only — dead space is conforming; [R-CNT-21] routes it to compaction §20 and privacy §23).

---

## Part 2 — The byte-coverage walk (§5.2, §9.6, §9.7)

**Enumerating generations** [R-LIF-08](a), [R-LIF-06]:
1. Probe backward from F − 64 to 0 **at 64-aligned offsets only** for the trailer magic. A candidate at offset o qualifies only if its trailer CRC verifies **and** committed_file_length = o + 64.
2. Accept only the candidate set forming a **chain**: exactly one candidate per generation number from live g down to 1; committed_file_lengths strictly increasing; each = candidate offset + 64; each candidate's directory bounds inside its own committed length. A candidate outside the chain is discarded as a payload mimic (tile payloads may legitimately contain trailer look-alikes, [R-LIF-06]). A duplicate or missing generation number in the chain → coverage failure at **file scope**. (How to resolve a mimic that *collides* with a real generation number: AMBIGUITY 4 / CONTRADICTION 2 — I implement backtracking chain search anchored at the live trailer.)
3. If I cannot verify any enumerated generation's trailer, directory, or tile index, I "cannot establish coverage and MUST treat the file as nonconforming" [R-LIF-08](d) — even when the live read path is pristine.

**Attribution** [R-LIF-08](b): generation k owns byte range [F_{k−1}, F_k), with F₀ = 16; the front block [0, 16) belongs to no generation.

**Claimed set per generation k** [R-LIF-08](c): verify gen k's directory CRC, parse its records, and claim:
- the directory region itself; its pre-trailer pad [dir end, F_k − 64) — which must be < 64 bytes [R-CNT-05] and all zero [R-CNT-03]; and its trailer [F_k − 64, F_k);
- every structure referenced **transitively** from that directory — extent slots (tile-index regions, user-metadata extents, including layer sub-record extents), and tile-index entries (stored-tile extents) — **filtered to those lying within [F_{k−1}, F_k)**. The in-range filter is what makes attribution decidable (§9.7 Note): a later directory retaining an earlier generation's structures produces only out-of-range references, so retained bytes are claimed exactly once, by the generation whose commit appended them [R-CNT-02];
- declared padding of that generation: the pre-trailer pad, plus alignment gaps of aligned/slab layers — locatable only via §16, which is Reserved (Part 4).

Every byte of [F_{k−1}, F_k) must be claimed **exactly once**; the walk therefore requires parsing every generation's directory and verifying every generation's index chain (crc_of_crc_array → segment CRCs) just to *read the entries* ([R-ENC-10]), which is why (d) names exactly those three structures.

**Nonconforming (certification fails) on:**
- any byte of [16, F) claimed by no class [R-CNT-02] — e.g., slack between two tile payloads that no index entry covers;
- any byte claimed twice [R-LIF-08](c) (intra-layer case: CONTRADICTION 1 — reported reject-layer per [R-CNT-13], certification fails either way);
- any nonzero byte in any generation's declared padding [R-CNT-03] (file scope, verifier-detected);
- any pre-trailer gap ≥ 64 bytes [R-CNT-05];
- broken chain: missing/duplicate generation, non-increasing committed lengths, cfl ≠ o+64, dead directory out of its own bounds [R-LIF-08](a));
- unverifiable trailer/directory/tile index of *any* enumerated generation [R-LIF-08](d));
- physical size ≠ live committed_file_length, F not a multiple of 64 [R-CNT-06], [R-CNT-01];
- every reject-file/-layer/-tile condition from Part 1 (per my AMBIGUITY-1 reading, layer- and tile-scope violations also defeat whole-file certification, since a conforming writer could not have emitted those bytes [R-CNF-05]).

**Merely reported (file remains certifiable):**
- unknown MU=0 records, top-level or sub-record — ignore-record is "a defined condition that is not a violation" (§2.4, [R-CNT-15], [R-CNT-18]);
- set ignore-lane trailer bits — must be ignored; future minors may define them ([R-CNT-08], §4.3);
- stored MU/PE flags differing from the registry values on known types — explicit SHOULD-report [R-CNT-22];
- dead space itself — superseded structures are conforming; I inventory them for the (Reserved) §23 privacy story [R-CNT-21];
- non-NFC names — [R-ENC-14] is a SHOULD; byte-distinct lookalike names are legal and reported;
- user-metadata encoding values I don't implement — reader outcome ignore-record + SHOULD report [R-CNT-25]; certification handling flagged (AMBIGUITY 3).

---

## Part 3 — Worked trace: 3 generations, one layer, one superseded tile, one re-tag

Assumptions, stated because the writer has latitude: one interleaved layer (layout 1), rank 2, grid 2×2 → N = 4 addressed tiles, all stored in gen 1; A = 0, S = 0 (so no §16 alignment gaps exist — deliberate, since §16 is Reserved); index size = 4×20 + ⌈4/2¹⁶⌉×4 = **84 bytes** [R-CNT-17]; gen 1 carried a file-scope user-metadata record (so gen 3's "re-tag" replaces it); the order of step-2 appends within a commit is a writer choice ("in any order", [R-LIF-02]) — I show one legal order; directory, pad, trailer come last in every generation (§5.1, [R-LIF-02] steps 3–5). Gen 2 supersedes spatial tile s = 2. Each Fₖ is a multiple of 64 [R-CNT-01].

| # | Byte range (file order) | Structure | §5.2 class | Claimed by | Live status at gen 3 |
|---|---|---|---|---|---|
| 1 | [0, 16) | front signature block | front block | **no generation** (F₀ = 16, [R-LIF-08](b)) | live (constant) |
| 2 | [16, a) | tile payload s=0 | stored-tile extent | **gen 1** (via D₁ → layer record → I₁ → entry 0) | live (referenced by I₂ entry 0) |
| 3 | [a, b) | tile payload s=1 | stored-tile extent | **gen 1** (via I₁ entry 1) | live |
| 4 | [b, c) | tile payload s=2 (original) | stored-tile extent | **gen 1** (via I₁ entry 2) | **dead** since gen 2 [R-CNT-21] |
| 5 | [c, d) | tile payload s=3 | stored-tile extent | **gen 1** (via I₁ entry 3) | live |
| 6 | [d, d+84) | I₁ — gen-1 tile-index region | tile-index region | **gen 1** (via D₁ layer record's extent slot) | **dead** since gen 2 |
| 7 | [d+84, e) | M₁ — user-metadata extent (encoded doc + 4-byte CRC) | record extent | **gen 1** (via D₁ user-metadata record's extent slot) | **dead** since gen 3 |
| 8 | [e, f) | D₁ — complete directory: layer record (slot→I₁, entry_count 4, crc_of_crc_array over I₁'s CRC array) + user-metadata record (slot→M₁) + 4-byte CRC | directory | **gen 1** (self, [R-LIF-08](c)) | dead (superseded) |
| 9 | [f, F₁−64) | P₁ — pre-trailer pad, < 64 zero bytes | declared padding | **gen 1** | dead |
| 10 | [F₁−64, F₁) | R₁ — trailer: generation 1, cfl = F₁ | trailer | **gen 1** | dead, but required for the chain [R-LIF-08](a) |
| 11 | [F₁, g) | tile payload s=2′ (replacement) | stored-tile extent | **gen 2** (via D₂ → layer record → I₂ → entry 2; in-range) | live |
| 12 | [g, g+84) | I₂ — gen-2 tile-index region: entries 0,1,3 → rows 2,3,5 (out-of-range refs, no claim); entry 2 → row 11 | tile-index region | **gen 2** (via D₂ layer record's slot) | live |
| 13 | [g+84, h) | D₂ — complete directory: layer record (slot→I₂, new crc_of_crc_array) + user-metadata record re-emitted (slot→M₁, out-of-range ref) + CRC | directory | **gen 2** | dead since gen 3 |
| 14 | [h, F₂−64) | P₂ — pre-trailer pad | declared padding | **gen 2** | dead |
| 15 | [F₂−64, F₂) | R₂ — trailer: generation 2, cfl = F₂ | trailer | **gen 2** | dead, chain member |
| 16 | [F₂, i) | M₃ — new user-metadata extent | record extent | **gen 3** (via D₃ user-metadata record's slot; in-range) | live |
| 17 | [i, j) | D₃ — complete directory: layer record re-emitted (slot→I₂ — out-of-range ref, no claim) + user-metadata record (slot→M₃) + CRC | directory | **gen 3** | **live directory** |
| 18 | [j, F₃−64) | P₃ — pre-trailer pad | declared padding | **gen 3** | live |
| 19 | [F₃−64, F₃) | R₃ — live trailer: generation 3, cfl = F₃ = file size | trailer | **gen 3** | **live** |

Coverage arithmetic the verifier confirms: gen 1's range [16, F₁) is exactly rows 2–10, each claimed once from D₁'s transitive closure; gen 2's range [F₁, F₂) exactly rows 11–15 (D₂'s references to rows 2,3,5,7 are out-of-range and claim nothing); gen 3's range [F₂, F₃) exactly rows 16–19 (D₃'s references to I₂ and, through it, all four live payloads are out-of-range). No byte is claimed twice precisely because of the in-range filter; rows 4, 6, 7, 8–10, 13–15 are dead space — claimed, conforming, report-only [R-CNT-21]. Live-overlap check (Stage H) runs over rows 2, 3, 5, 11, 12, 16, 17, 19 (+front block) and finds none. Chain check: R₃(3) → R₂(2) → R₁(1), cfl strictly increasing, each = offset+64, each directory in-bounds. All three directories' CRCs, both index regions' crc_of_crc_array + segment CRCs must verify or the file is nonconforming outright [R-LIF-08](d)]. All three pads and any index-entry-to-index-region seams must be zero-free — actually there are no seams here: every inter-structure byte is inside a claimed structure or a declared pad; a nonzero byte in P₁/P₂/P₃ → nonconforming [R-CNT-03].

---

## Part 4 — What the text leaves me unable to decide while classifying every byte

The single hard blocker is **§15 [Reserved]**: I know the entry size (20 bytes) and segment-CRC granularity (one u32 per 2¹⁶ entries) only via [R-CNT-17]'s size formula, and I know an entry has "a crc field" (§8.1) and a sentinel exists (§3.1). I do **not** know: the field order inside the 20 bytes, the sentinel encoding, the invalid-combination table, where the segment-CRC array sits inside the region, or the bounds rules for entry offsets/lengths. Without these I cannot identify stored tiles, claim payload bytes, or verify segments byte-exactly — coverage is unimplementable for any layer with entry_count > 0. Secondary blockers: **§16** (alignment-gap location for A≠0/S≠0 layers — cannot locate that declared padding), **§12** (type codes, element sizes → fill-length validation), **§17** (codec value set beyond "0 invalid"), **§18** (user-metadata payload layout beyond the encoding u8; whether the document may be inline), **§21** (limits minimums — cannot separate "resource-limited reject" from nonconformance; consolidated error register), **§10** (experimental-range policy), **§20** (what "preservation rules" re-emission must look like byte-wise; whether compaction renumbers generations from 1, which [R-LIF-08](a)'s chain-to-1 requires).

---

## AMBIGUITIES

1. **What fails certification** — §2.3 [R-CNF-02] "satisfying every file-level requirement" vs §2.4's scoped outcomes. Readings: (i) any violated byte-constraining MUST (any scope) makes the file nonconforming, outcomes only describe reader blast radius; (ii) only file-scope violations defeat file conformance. I pick (i): conformance is "a pure predicate on bytes," and [R-CNF-05] means no conforming writer emits a reject-layer/-tile byte pattern; the verifier reports the scoped outcome but withholds the certificate.
2. **Writer-MUST-NOT / reader-ignore mismatches** — reserved record-flag bits nonzero, MU=1∧PE=0 ([R-CNT-12]), stored MU/PE ≠ registry ([R-CNT-22]), trailer ignore-lane bits vs "MUST write flags = 0" ([R-CNT-08]). Readings: fail certification vs report-only. I pick: report-only for ignore-lane bits (future minors may define them, §4.3) and for [R-CNT-22] mismatches (spec says SHOULD report, implying not reject); fail-certification for reserved record-flag bits and MU=1∧PE=0 (no growth vehicle can ever assign them — §4.3 lists only trailer ignore-lane bits — so they are unambiguously writer defects), consistent with my reading in (1).
3. **User-metadata encoding = 0 (invalid) or unassigned ≥ 3** — [R-CNT-25] assigns ignore-record only to "an encoding value the reader does not implement"; outcome for the explicitly invalid 0, and conformance status of ≥3 (future §18 range?), are unstated. I pick ignore-record + report for both, deferring the conformance verdict on ≥3 with a flag; reject-file for one metadata byte contradicts [R-CNT-25]'s evident intent.
4. **Chain construction under mimic collision** — [R-LIF-08](a): if a payload-embedded trailer mimic verifies (CRC, cfl = o+64) and repeats a real generation number, is that immediately "duplicate generation number → failure," or do I search for a consistent chain? I pick backtracking search anchored at the live trailer, failing only when no candidate set satisfies (a)–(c); the "discarded as a payload mimic" sentence shows mimics are not meant to defeat verification. (See CONTRADICTION 2.)
5. **Re-validating dead generations** — which bound applies to a superseded directory's extent slots: its own F_k or the live F ([R-CNT-13] says "past F − 64" without qualification)? And do dead trailers get full [R-CNT-06] semantic checks (file_id ≠ 0, reserved zero, cfl multiple of 64) beyond [R-LIF-08](a)'s list — including file_id equality across the chain, which [R-LIF-03] ("the file_id chosen at creation") implies but (a) omits? I pick: validate against the generation's own F_k (matches (a)'s "inside its own committed length" logic), and enforce file_id equality + reserved-zero on all chain trailers, since gen k was once a live state that had to satisfy [R-CNT-06].
6. **index_encoding 2 (reserved) and ≥ 0x80 (experimental)** — [R-CNT-23] rejects "reserved or unassigned" values at layer scope, but whether the experimental range counts as "unassigned" for a major-1 verifier is deferred to §10/§15 (Reserved). I pick reject-layer for everything ≠ 1, by analogy with [R-GEO-05]'s explicit rejection of the experimental linearization range and because [R-CNT-17]'s size formula exists only for encoding 1.
7. **Checksums of dead-only structures** — [R-LIF-08](d) requires verifying each generation's trailer, directory, and tile index, but is silent on superseded stored-tile payload CRCs and dead user-metadata extent CRCs. Readings: skip (coverage needs only extents, not payload contents) vs verify (whole-bytes predicate + immutability [R-LIF-01] means a mismatch is corruption). I verify and fail certification on mismatch, reporting that reader impact is nil; a verifier that skips is defensible under the letter of (d).
8. **User-metadata document placement** — whether the extent slot may be (0,0) with the document inline is undecidable (§5.2/§8.1 speak only of "user-metadata extents"; §18 Reserved). I accept (0,0) as "no extent" per [R-CNT-13] and defer document validation.

## CONTRADICTIONS

1. **Intra-layer overlap outcome**: §7.2 [R-CNT-13] — "a verifier MUST treat an intra-layer overlap as reject-layer" — vs §9.7 [R-LIF-08](c) — "Every byte of [F_{k−1}, F_k) MUST be claimed exactly once," whose failures the section frames as coverage failure at **file scope**. Two live index entries of one layer overlapping in their own generation trigger both rules with different outcomes. (Also §5.2 [R-CNT-02] condemns only bytes "claimed by **no** class," silent on double claims — a third strength.) My resolution: report reject-layer per the more specific [R-CNT-13]; certification fails either way; the spec should carve intra-layer overlaps out of exactly-once or align the outcomes.
2. **Conforming mimics can fail coverage**: §9.6 [R-LIF-06] normatively acknowledges "a tile payload can deliberately contain a byte string that mimics a valid trailer" (a conforming file), but §9.7 [R-LIF-08](a) read literally makes a duplicate generation number among qualifying candidates "a coverage-verification failure at file scope" — so a crafted-but-conforming payload could render a conforming file unverifiable, contradicting §2.3 [R-CNF-02] (conformance is a pure predicate on bytes). Resolved in practice by the backtracking reading (AMBIGUITY 4), but the text as written permits a verifier that flunks conforming files.

## OBSERVATIONS

1. The verifier's entire reader-obligation inheritance hangs on one parenthetical in §4.2 [R-ENC-04] ("including any updater or verifier"); nothing in §2.3's conformance classes says a verifier is a reader.
2. The 20-byte entry size and 4-bytes-per-2¹⁶-entries segment structure are recoverable *only* by reverse-engineering [R-CNT-17]'s arithmetic; 20 = 8+8+4 strongly suggests (offset u64, length u64, crc u32), but I refused to guess the order/sentinel (Part 4).
3. Checksum fields themselves are covered by no checksum (trailer CRC covers [0,60), not itself; likewise the directory and user-metadata trailing CRCs), contra the letter of [R-CNT-19]/§4.5 "every field … exactly one checksum"; must be read as "every protected field."
4. The scope routing that a malformed extent slot on a *top-level user-metadata record* is **reject-file** (via [R-CNT-13] "the file for other top-level records" + §7.3's scope column) — while every other user-metadata failure is ignore-record — is decidable but easy to get wrong.
5. Establishing that prior directories/trailers are simultaneously "dead space" ([R-CNT-21]) and mandatory verification targets ([R-LIF-08](a)/(d)) requires cross-reading three sections; "readers MUST NOT interpret" dead space explicitly does not bind verifiers.
6. Deciding that the empty directory's CRC is 0x00000000 relies on the non-normative §5.1 example plus the CRC definition (init⊕final XOR cancel on empty input); a normative empty-input vector would help.
7. The [R-LIF-08](c) in-range filter silently also handles *forward* references (a corrupt dead directory pointing past its own F_k claims nothing in any generation) — decidable, but only after working the traversal semantics through: the filter applies to claimed structures, not to traversal.
8. Chain-to-generation-1 ([R-LIF-08](a)) forces compaction (§20, Reserved) to renumber from 1; if §20 chooses otherwise, every compacted file fails coverage verification.
9. A gigantic live generation number is self-refuting without deep scanning: g trailers need at least 64g bytes below F, so g > (F−16)/64 fails the chain arithmetically — worth stating in §21's limits to spare verifiers a full probe.
10. [R-CNT-13]'s "neither its inline payload nor its extent contents encode offsets or lengths of other file bytes" for MU=0 records is not mechanically checkable from bytes; a verifier can only enforce its consequences (coverage/overlap), never the property itself.
