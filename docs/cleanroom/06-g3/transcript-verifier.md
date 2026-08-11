# Cleanroom round 6 — verifier

> *Editorial note.* In the Readings for §16.2, one word naming the tile
> before another was replaced with "the tile ahead of it", to satisfy
> this repository's vocabulary gate. The meaning is unchanged and no
> finding is affected; the substitution is recorded here rather than made
> silently, since this file is a verbatim artifact.

Protocol: ADR-0034. Access rule: `spec/tarn.md` only.

## Walk

ACCESS DISCLOSURE. I read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (all 3,475 lines). No ADRs, PLAN.md, AGENTS.md, README, conformance/, registry.json, git history, or web. I ran two scripts: one implementing CRC-32C from §4.5's parameters alone, and one counting rows/instances in §21's tables from the spec file itself. Every conclusion below cites the document.

TWO THINGS I CONFIRMED BEFORE TRUSTING ANYTHING ELSE.

(1) The checksum is reproducible from the text. Implementing CRC-32C from §4.5's stated parameters (Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) reproduces all four constants the document commits to: CRC-32C("123456789") = 0xE3069283 and CRC-32C of zero bytes = 0x00000000 (§4.5); the CRC of a full all-sentinel segment = 0xEECB3BB2 (`[R-IDX-05]`, Appendix B); and Appendix A's trailer CRC = 0xE00938D2 over its bytes [0,60). Appendix A's file is 128 bytes, dir_offset 16, dir_length 4, and its directory CRC over zero bytes is 0x00000000 as §7.1 requires. A verifier's entire chain of trust rests on this one primitive, and it is pinned tightly enough to build without guessing.

(2) The register's arithmetic is self-consistent. Parsing §21.2–§21.5 mechanically gives 39 + 50 + 26 + 10 = 125 rows and 244 instances under §21.1's counting rule (semicolon-separated, a cell reading "—" counting as one) — exactly the "125 conditions over 244 named instances" of `[R-ERR-02]`. The register is the verifier's build list, so this mattered.

──────────────────────────────────────────────
A. THE CERTIFICATION PROCEDURE, END TO END
──────────────────────────────────────────────

A verifier is a reader plus a set of checks readers are exempt from (`[R-CNF-11]`), and its verdict is a pure predicate on bytes (`[R-CNF-02]`, `[R-CNF-12]`: "a verifier certifies only violation-free files"). Unlike a reader, it cannot be lazy: §19.2's tiers fix the *latest* point a reader must detect something, but a verifier must check every scope whether or not anything would ever access it. My procedure is nine phases.

PHASE 0 — capability gate. Before touching bytes, establish that this build can execute all four codecs (§17.2), both filters (§17.3), both layouts, all thirteen sample types (§12.1), a JSON parser meeting `[R-MTA-04]`, and at least §21.9's minimum guarantees. If any layer later declares a codec or filter I cannot execute, `[R-COD-11]` forbids certification outright; the same for a user-metadata document I decline to decode (`[R-MTA-09]`). A resource refusal must be reported as a resource limit and never as a validity error (`[R-ERR-04]`), and it yields "not certified", not "nonconforming".

PHASE 1 — file frame. Obtain the transport-authoritative size F (`[R-CNT-10]`; never substitute committed_file_length). Reject below 128 bytes (`[R-CNT-27]`, F7). Compare bytes [0,16) to the front-block constant by equality (`[R-CNT-04]`, F8, F2) — I always do this regardless of transport; see the finding on `[R-CNT-04]`.

PHASE 2 — trailer. Read [F−64, F). Validate in §6.2's mandated order, which is not negotiable because only magic, version, and the terminal CRC sit at positions fixed across all majors (`[R-CNT-24]`): magic (F10), trailer CRC over [0,60) (F16), version gate (F20/F21), then the field gates — incompat lane bits 0–15 all clear (F22), committed_file_length = F and ≡ 0 mod 64 (F19/F15), dir_offset ≥ 16 (F11), dir_length ≥ 4 (F18), dir_offset + dir_length ≤ F − 64 (F12), generation ≥ 1 (F13), file_id ≠ 0 (F14), reserved [56,60) zero (F17). Ignore-lane bits 16–31 are not a violation (§21.6). Nothing past the CRC may be acted on before the CRC verifies (`[R-ENC-10]`, `[R-ENC-05]`).

PHASE 3 — directory. Fetch [dir_offset, dir_offset+dir_length), verify the terminal 4-byte CRC over the preceding dir_length−4 bytes *before any other use* (`[R-CNT-11]`, F23). Then parse the record sequence: exact framing with no residue (`[R-CNT-12]`, F32), type ≠ 0 (F27), multiplicity — at most one file-scope user-metadata record (F37) (`[R-CNT-14]`); MU gate on unknown types (F38); extent-slot validity for non-layer top-level records (F33/F34/F35) (`[R-CNT-13]`). Here the verifier adds four checks a reader never makes: reserved flag bits 2–15 clear (F29), MU=1&PE=0 absent (F28), registered types carrying exactly §7.3's fixed MU/PE bits (F31), and no reserved-range type 0x0003–0x7FFF (F39).

PHASE 4 — layer records, exhaustively. For each layer record, run §19.3's full validation (`[R-RDR-03]`) — every layer, not only accessed ones. Parse the inline payload strictly in table order with no padding: name; layout; linearization; codec; filter; A; S; A_slab; d; C; d dimension entries; C channel entries; index_encoding; entry_count; crc_of_crc_array; then a sub-record sequence with no residue (`[R-CNT-18]`, L24/L15). Check names (`[R-ENC-11]`/`[R-ENC-12]`/`[R-ENC-15]`, L4–L10: layer-name uniqueness is file scope, dimension/channel-name duplication is layer scope). Check every value set — layout 1|2 (L37), linearization = 1 only (L34), type 1–13 (L35), codec 1–4 (L44), filter 1|2 (L46), index_encoding = 1 (L32) — with reserved *and* experimental values all layer-scope errors per `[R-GEO-05]`/`[R-TYP-03]`/`[R-COD-03]`/`[R-COD-09]`. Check the fill field's length against the type's element size (L31) and a bool fill of exactly 0x00/0x01 (L36, `[R-TYP-07]`). Check A ≠ 0 XOR S ≠ 0 (L21), A a power of two in [512, 2⁶²] (L40), A_slab a power of two in [1, 2⁶²] and zero exactly when S = 0 (L29/L30), crc_of_crc_array = 0 exactly when entry_count = 0 (L28). Compute geometry with the ceiling division §11.2 mandates (Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0 — never (E+T−1)/T, whose intermediate can leave the domain), overflow-checking every product against 2⁶³−1 (`[R-ENC-04]`, L2), then cross-check entry_count against the addressed-tile count (N interleaved, C·N planar; L22) and extent_length against entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 (L23). Check `[R-COD-07]`'s lz4 declaration bound against the decoded tile size (L45). Add the verifier-only flag checks again at layer scope (L47, L48, L50) and reserved-range sub-record types (L26).

PHASE 5 — index chains, every layer, every segment. Fetch each layer's segment CRC array, verify crc_of_crc_array over it (L38), then verify every segment CRC over its entries as stored — the final partial segment covering only its actual bytes (L39). `[R-IDX-05]`'s all-sentinel constant 0xEECB3BB2 is a writer shortcut only: "Equality with the constant licenses nothing for readers: verification is byte comparison of computed CRCs, never constant matching." Then classify every entry per §15.3's table (T6–T12), including the sentinel test (offset=length=2⁶⁴−1 ∧ crc=0), and note that `[R-ENC-03]`/`[R-ENC-04]`'s domain rules apply to non-sentinel entries only (`[R-IDX-02]`). A reader touches one segment; a verifier touches all of them.

PHASE 6 — the coverage walk (§B below).

PHASE 7 — placement invariants (§D below).

PHASE 8 — decoded content (§E below), plus user-metadata extents: CRC (R2), encoding byte and its inline_length of exactly 1 (F26/L13, R1), zstd frame constraints carried over from `[R-COD-06]` minus the tile-size ones (R4, `[R-MTA-09]`), decode (R3), then the document rules — JSON object, no BOM (R7), finite numbers and no bare NaN/Infinity (R8), no duplicate decoded keys (R9), well-formed UTF-8 after escape resolution including unpaired-surrogate escapes (R5), keys non-empty, ≤ 255 bytes, free of U+0000–U+001F (R6/R10) — and the verifier-only member-ordering check (F30/L49).

PHASE 9 — verdict. Certify only if no row of §21.2–§21.5 fired anywhere and no scope went unexamined. Emit the slack total unconditionally (`[R-CNT-21]`). Report each finding as (row id, outcome class, scope, governing requirement id) — the tuple `[R-VEC-02]` says a manifest entry records — and keep resource refusals in a distinct channel from validity errors (`[R-ERR-04]`).

──────────────────────────────────────────────
B. THE COVERAGE WALK AND WHAT IT REPORTS
──────────────────────────────────────────────

`[R-LIF-08]` scopes it precisely: "A verifier checking `[R-CNT-02]`'s partition walks the live state only." From the live trailer I enumerate claimants:

  • the front signature block [0, 16) — a coverage class of its own, not a "structure" (§5.2);
  • the live directory [dir_offset, dir_offset + dir_length);
  • the live trailer [F−64, F);
  • every record's extent — top-level and sub-record, "whatever the record's type" (`[R-CNT-02]`), so an unknown MU=0 ancillary's extent and a user-metadata extent whose document failed its own rules are still claimants;
  • every layer's tile-index region (the layer record's extent slot);
  • every non-sentinel, well-formed index entry's extent [offset, offset+length).

Nothing else is enumerated. Prior generations' trailers, directories and pads, superseded payloads, and superseded index regions are simply not reached, and `[R-LIF-08]` makes everything the walk misses slack. That is why §5.2's Note can say the "belongs to no class" half is untestable and only disjointness remains: "The live committed state is *defined* as the front block plus what the coverage walk reaches."

What it reports:
  1. Disjointness verdict — see §C.
  2. Bounds: every enumerated claimant inside [16, F−64), the front block and trailer at their fixed positions.
  3. F9: no structure in the pre-trailer pad (`[R-CNT-05]`). Combined with disjointness this collapses to one invariant I derive rather than read: every live structure other than the directory and the trailer lies entirely within [16, dir_offset).
  4. The slack total: F minus the union of all claimed bytes. This is a MUST (`[R-CNT-21]`), and it is the number §20.3 and §20.5 both cite as the operator's signal to compact — a commit leaves a directory, a pad, a trailer, and a whole index region per touched layer behind. I compute it as a byte-set union, not by subtraction, so that an overlap cannot silently make the total look plausible.
  5. Nothing about slack *content*: "Slack has no internal structure this specification defines, its content is unconstrained, and no conformance requirement applies to it" (`[R-CNT-21]`). A trailer-mimicking byte string in slack is inert (§21.6, `[R-LIF-06]`) — I do not scan for it, and I do not scan backward for prior generations (see the §9.6/§9.7 contradiction I filed).

──────────────────────────────────────────────
C. EXTENT OVERLAP DETECTION
──────────────────────────────────────────────

`[R-CNT-13]` is the rule: "Extents are owned exactly once — within the live committed state... no two extent slots and no two structures overlap." Readers are explicitly excused ("readers are not obligated to detect overlap, which requires whole-directory knowledge"), which makes this the flagship verifier check.

Implementation: build one interval list of every claimant from §B, each tagged with an owner — (layer i) or (file). Sort by start offset and sweep; any adjacent pair whose ranges intersect is a violation. Classification, per `[R-CNT-13]` and §15.3's last three rows:
  • both intervals owned by the same layer → reject-layer (L19). This covers two stored extents of one layer, a stored extent inside its own layer's index region, and a stored extent inside one of its own sub-record extents.
  • any other pair — across two layers, or a layer structure against the directory, a file-scope record extent, the trailer, or the front block → reject-file (F36).
One exclusion is normative and easy to get wrong: `[R-IDX-03]` says "an entry these rows classify reject-tile contributes no stored extent to the *verifier* rows, which bind over well-formed entries' extents only." So an entry with offset 12, or length 0, or offset+length past F−64, is reported as its own reject-tile row and then dropped from the interval list — it never becomes an overlap finding.

Consequences worth stating: deduplication is banned outright. Two layers whose index entries point at one identical payload, or two entries within one layer that do, are overlaps — the format has no shared-extent mechanism. And §22.3 names the reason: overlap-freedom "removes aliasing — two index entries pointing at one payload, or a payload overlapping a structure that governs it — as a class."

Cost: this is a sort over every stored extent in the file. See the OBSERVATION on verifier cost.

──────────────────────────────────────────────
D. ALIGNMENT AND SLAB INVARIANTS
──────────────────────────────────────────────

Mutual exclusion first: A ≠ 0 with S ≠ 0 is layer-scope invalid (`[R-CNT-16]`, L21), and A_slab must be 0 exactly when S = 0 (`[R-CNT-23]`, L29). A layer declaring neither makes no placement promise at all (`[R-SLB-05]`): "a streaming writer places tiles in acquisition order at no cost to conformance."

Per-tile alignment (`[R-SLB-01]`, L41). With A declared: for every non-sentinel entry, offset mod A = 0. Readers are exempt because "offsets are always explicit, so alignment is reader-invisible." Vacuous for a layer with no stored tiles.

Slabs (`[R-SLB-02]`, `[R-SLB-03]`, L42/L43). Partition disk ordinals into blocks — one block [0, N) interleaved, one block [c·N, (c+1)·N) per channel planar, "runs never span channel blocks". Run r of a block covers ordinals [block_start + r·S, min(block_start + (r+1)·S, block_end)), so the final run of a block may be short. Then per run, over its stored (non-sentinel) entries in ascending disk-ordinal order:
  • first stored tile: offset mod A_slab = 0 (L43). With A_slab = 1 this is vacuous, which is the "contiguity-only" declaration §16.2's note describes for remote range coalescing.
  • each subsequent stored tile: offset = previous stored tile's offset + previous stored tile's length (L42) — gap, overlap, or descending placement all fail. Sentinels are skipped entirely: "Sentinel tiles are transparent to run continuity: they occupy no bytes and do not break packing." §16.2's worked example confirms the reading (ordinals 8, 9, 11…15 packed with no gap where 10 would be).
  • a run with no stored tiles imposes nothing.
Runs are not ordered relative to each other and bytes between them are slack, so I never check inter-run placement. `[R-SLB-04]` (a stale slab declaration carried across a commit) needs no separate code: the document says its detection "*is* `[R-SLB-03]`'s" — every file exhibiting it exhibits an unpacked run or a misaligned first tile.

──────────────────────────────────────────────
E. DECODED-CONTENT OBLIGATIONS
──────────────────────────────────────────────

This is the phase that forces a verifier to decode the entire dataset, and §17.4 makes it non-optional: "The decoded-content obligations of §14 (`[R-SER-05]`, `[R-SER-08]`) require decoding."

Per stored tile, given its disk ordinal k:
  1. Recover geometry. Planar: c = k div N, s = k mod N (`[R-GEO-06]`'s c·N + s, channel-major). Interleaved: s = k, all C channels. Decompose s into tile coordinates by row-major over the grid counts G (`[R-GEO-06]`: s = Σ tᵢ·∏_{j>i} Gⱼ).
  2. Fetch [offset, offset+length), verify the entry crc *before decoding* (`[R-CNT-20]`, T1).
  3. Decode: codec first, then the filter's inverse (§17.1). Enforce the per-codec rules — codec 1's length = decoded size (T14, checkable with no fetch at all); raw RFC 1951 with no wrapper and exactly one stream (T15/T16); zstd magic 28 B5 2F FD, exactly one non-skippable frame, no dictionary ID, no content-checksum flag, window size ≤ decoded size, Frame_Content_Size = decoded size when present and never an allocation source (T17–T22); lz4 raw block, not the frame format (T23). Then `[R-COD-08]`'s universal rule: decode to exactly the decoded size, consuming the stored bytes exactly (T3, T24, T25). The decoded size comes from declarations only (`[R-SER-07]`) — never from a payload field, which is the decompression-bomb defense of `[R-SEC-02]`.
  4. Invert the filter at the mandated stride: element size for a planar numeric plane, sample stride Q for an interleaved tile, identity for a packed bool plane (`[R-COD-10]`).
  5. Padding positions (`[R-SER-05]`, T4). Enumerate in-tile positions u; u is a padding position iff for some axis i, tᵢ·Tᵢ + uᵢ ≥ Eᵢ. At each such position, every channel the position carries must encode that channel's *recorded* fill bytes:
       – interleaved: bytes [u·Q + Fᶜ, u·Q + Fᶜ + Bᶜ) equal channel c's fill field, for every c (bool channels: the single recorded fill byte);
       – planar numeric: bytes [u·Bᶜ, (u+1)·Bᶜ) equal the fill field;
       – planar bool: bit u mod 8 of byte u div 8 equals the fill bit (0x00→0, 0x01→1, per `[R-TYP-07]`).
     §14.5's example is the acceptance test: extents (5,5), tiles (4,4), the (1,1) edge tile is 32 bytes of one uint16 channel with fill 0xABCD — value 0 real, values 1–15 each `CD AB`.
  6. Packed pad bits (`[R-SER-05]` second sentence, T5). Distinct from padding positions, and §14.3's Note is explicit that a plane can have many padding positions and no pad bits. When P mod 8 ≠ 0, bit positions P mod 8 through 7 of the final byte of a planar bool plane must each carry the channel's fill bit. §14.3's example pins it: P = 10, alternating values, fill false → `55 01`; fill true → `55 FD`. Note these bits are outside the value region, so `[R-SER-03]`'s "every bit pattern of the value region decodes" does not license them — decoding never fails on them, but certification does.
  7. Interleaved bool bytes (`[R-SER-08]`, T2). Every interleaved bool value byte is 0x00 or 0x01. This is the one place the document defines what a *reader* returns for a nonconforming byte (0x00 false, anything else true) precisely so that two readers cannot diverge — but the byte is still a tile-scope violation whose detector is the verifier.
  8. Mis-strided filter (T26) is not a separate check; see my finding.

Sentinel tiles are skipped entirely — they occupy no bytes and carry no content obligations — and a rejected tile is never satisfied by returning fill (`[R-CNF-09]`, `[R-TYP-09]`).

──────────────────────────────────────────────
F. WHAT A VERIFIER CHECKS THAT A READER DOES NOT
──────────────────────────────────────────────

Twenty register rows carry detector *verifier*, plus two unconditional reporting duties. For each, what a failing file looks like:

1. F9 — structure in the pre-trailer pad (`[R-CNT-05]`). File: a layer's tile-index region emitted at dir_offset + dir_length, with the trailer 64-aligned beyond it. Every reader gate passes — dir bounds hold, the index extent is ≤ F−64, all CRCs verify — and the file reads perfectly. Reject-file at certification.

2. F36 — cross-scope overlap (`[R-CNT-13]`). File: layer B's stored tile placed at an offset inside layer A's tile-index region. Both tiles read, both CRCs verify, both layers list. Reject-file.

3. L19 — intra-layer overlap. File: a writer that "deduplicated" two identical tiles by pointing two entries of one layer at the same (offset, length, crc). Both reads return correct data. Reject-layer.

4. F28 / L47 — MU=1 with PE=0 (`[R-CNT-12]`). File: a top-level ancillary record with flags = 0x0001. A reader treats it as PE=1 and behaves identically; only a verifier notices.

5. F29 / L48 — reserved flag bits 2–15 set. File: a layer record with flags = 0x0007 instead of 0x0003. Readers must ignore reserved bits.

6. F31 / L50 — a registered type's stored MU/PE bits differing from §7.3 (`[R-CNT-22]`). File: a layer record with flags = 0x0000, or a user-metadata record with PE = 0. "A reader MUST apply a known type's specified semantics regardless of its stored MU and PE bits — a flipped stored bit never changes conforming behavior."

7. F39 / L26 — a reserved-range record type 0x0003–0x7FFF (`[R-CNT-15]`). File: a top-level record of type 0x0005 with MU = 0. Every reader ignores it silently and reads the rest. (With MU = 1 the reader rejects the file anyway — that is F38, a reader row.)

8. L41 — alignment invariant (`[R-SLB-01]`). File: layer declares A = 4096, one stored tile sits at offset 4104. Readers use the explicit offset and never look.

9. L42 — slab packing (`[R-SLB-03]`). File: S = 8, A_slab = 4096, run 0's stored tiles at (1000, len 100) then (1200) — a 100-byte hole. Readers coalesce from explicit offsets; the hole is just slack to them.

10. L43 — slab first-tile alignment. File: run 1's first stored tile at offset 8200 with A_slab = 4096.

11. T2 — interleaved bool byte 0x02 at a real position (`[R-SER-08]`). The tile's crc covers the wrong byte and verifies; a reader that does not screen content returns "true" and remains conforming.

12. T4 — padding position not carrying fill (`[R-SER-05]`). File: §14.5's edge tile with padding values zeroed while the channel's fill is 0xABCD. Nothing structural differs; a reader never returns padding positions (`[R-GEO-04]`) and so never sees them.

13. T5 — pad bits (`[R-SER-05]`). File: planar bool plane, P = 10, fill true, final byte 0x01 instead of 0xFD.

14. T26 — mis-strided byte-shuffle, observable only through 12 or 11.

15. F30 / L49 — unsorted user-metadata members (`[R-MTA-05]`). File: a document serialized as {"b":1,"a":2}. The document is readable and readers "process the document unchanged"; the file is nonconforming and "a verifier MUST report it".

16. `[R-CNT-21]` — the slack total. Not pass/fail: a MUST-report number, and the only signal an operator has that a file wants compaction.

17. `[R-CNT-02]` / `[R-LIF-08]` — the live-state partition itself, which "Coverage is checked by verifiers, never by readers" states outright.

Beyond the register, three structural differences: a verifier runs *every* reader check over *every* layer and *every* tile rather than at §19.2's access tiers; it must decode every stored tile and every metadata document, and may not certify what it cannot decode (`[R-COD-11]`, `[R-MTA-09]`); and it inherits `[R-CNF-12]`'s asymmetry — a reader may reject a nonconforming file at any point, but a verifier must reach a verdict on the whole file.

──────────────────────────────────────────────
G. WHERE I HAD TO GUESS
──────────────────────────────────────────────

Seventeen findings follow in the structured list. The four that would change my verifier's verdict on real files, in order of consequence: whether §21.5's ignore-record rows bar certification (a corrupt metadata CRC either does or does not cost a file its certificate); whether an experimental metadata encoding is a violation or conduct-bound like an experimental record type; whether `[R-MTA-05]`'s sorting is recursive; and whether `[R-MTA-07]`'s out-of-scope standardized key — a named MUST NOT with no register row — is checkable at all. The §9.6/§9.7 contradiction about generation enumeration is the one place where two normative sentences prescribe opposite procedures for the same obligation.

## Findings

### CONTRADICTION — §9.6 `[R-LIF-06]` vs §9.7 `[R-LIF-08]` (and its Note)

Byte-level: True

§9.6 tells verifiers to enumerate generations for coverage verification; §9.7 forbids it. `[R-LIF-06]`: "Recovery tools and verifiers — never conforming readers on the default path — locate commit states as follows: probe backward at 64-aligned offsets o for the trailer magic... Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0." `[R-LIF-08]`: "A verifier checking `[R-CNT-02]`'s partition walks the live state only," reinforced by its Note: "Nothing here enumerates prior commits." The two sentences describe opposite procedures for the same obligation (§5.2 coverage), and they can produce different verdicts: under §9.6's reading a verifier that reconstructs prior generations would see superseded structures as claimants and could report overlaps that §9.7 classifies as slack. I implemented `[R-LIF-08]` (live-state walk, no backward probe) and treat §9.6's sentence as vestigial, because §9.7 is the section that owns coverage verification and its rule is stated as an exclusive ("only").

### CONTRADICTION — §18.4 `[R-MTA-07]` vs §21.1 (register completeness) and §21.2–§21.6

Byte-level: True

`[R-MTA-07]` states a writer prohibition: "A writer MUST NOT emit a standardized key outside the scopes its row lists." A file carrying `tarn.created` on a layer, or `tarn.axes` at file scope, therefore fails `[R-CNF-05]` and is nonconforming — but no row of §21.2–§21.5 registers it, and §21.6 registers only the *unrecognized* `tarn.` key as a non-violation. §21.1 says: "Its completeness is normative — a violation this specification names and the register omits is a defect in this document." So either the register is incomplete or `[R-MTA-07]`'s scope clause is not a file-level requirement. This is squarely a verifier's problem: it is the only actor that would fail a file for it, it has no row, no outcome class, and no scope assignment (file or layer?). I implemented it as a reported warning that does not bar certification, since the register — which a verifier is built from — omits it, but I flag the choice as unsupported.

### CONTRADICTION — §21.2 row F36 instance list vs `[R-CNT-06]`, `[R-CNT-13]`, `[R-IDX-03]`, and `[R-ERR-02]`/`[R-VEC-03]`

Byte-level: False

F36's Instances cell names seven claimants including "trailer" and "front signature block", and `[R-ERR-02]` requires "a row naming instances has one vector per instance" while `[R-VEC-03]` repeats "every register row has at least one vector for each instance it names." But no conforming-shaped file can exhibit either instance as an *overlap*: every possible claimant is already floored at 16 and ceilinged at F−64 by a reader-detected rule — dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64 (`[R-CNT-06]`, rows F11/F12), extent_offset ≥ 16 and extent_offset + extent_length ≤ F − 64 (`[R-CNT-13]`, rows F34/F35/L17/L18), and for tile entries "offset < 16 (non-sentinel) → reject-tile" and "offset + length > F − 64 (non-sentinel) → reject-tile" (`[R-IDX-03]`, rows T8/T9). `[R-IDX-03]` then removes those entries from the verifier rows outright: "an entry these rows classify reject-tile contributes no stored extent to the *verifier* rows." So a byte of the front block or the trailer can never be double-claimed by a well-formed claimant, and the two instances name conditions no file can exhibit — the same defect class §5.2's Note describes as "a row no file could exhibit". My verifier implements the other five instances and never emits the two.

### AMBIGUITY — §21.5 (all rows R1–R10), read against §21.1, `[R-CNF-12]`, and `[R-CNT-25]`

Byte-level: True

Whether an ignore-record condition bars certification is the single largest fork in a verifier's verdict logic, and the document does not settle it. §21.1 calls every row of the register a violation ("The register below enumerates every violation this specification names"), and `[R-CNF-12]` says "a verifier certifies only violation-free files" — so a corrupt user-metadata CRC or a duplicate JSON key would make the file uncertifiable. Against that, `[R-CNT-25]` says "Application metadata never invalidates the structural data it annotates," §21.5's own heading gives the outcome as ignore-record, and §21.6 exists precisely to hold conditions that are "not violations" — which R1–R10 are not placed in.

**Readings.** (a) Every §21.5 row is a file-conformance violation: the quarantine bounds only the *reader's* blast radius, and certification fails. (b) Ignore-record conditions are defined behaviors like §21.6's, so a file with a broken metadata document is still conforming and certifiable. (c) Split: rows describing corruption (R2, R3) fail certification while rows describing content the writer chose (R7–R10) do not. I picked (a) — §21.1's completeness sentence and `[R-CNF-12]`'s "violation-free" are the only normative statements that speak to certification, and both point one way — and I report the failing row with its ignore-record reader outcome alongside the certification failure so a consumer can tell the two apart.

### AMBIGUITY — §21.5 row R1 ("experimental ≥ 0x80" instances) vs §21.6 ¶ on conforming-files-a-reader-refuses, `[R-CNF-02]`, `[R-EXT-03]`

Byte-level: True

§21.6 states the principle explicitly for record types: an experimental-range value leaves the file conforming because "the prohibition on publishing experimental values binds a writer's conduct and not the bytes," "which is why neither is a register row, while a *reserved*-range type... is." R1 nonetheless registers experimental metadata encodings (≥ 0x80) as violation instances, next to reserved ones. The other enum spaces are unambiguous the other way — `[R-GEO-05]`, `[R-TYP-03]`, `[R-COD-03]`, `[R-COD-09]` each say "the experimental range included" is a validity error — so the format is deliberately non-uniform and the metadata-encoding space is the one case left unstated. `[R-EXT-03]` fixes only the reader outcome there ("ignore-record under the quarantine... never a scope-level rejection"), not file conformance.

**Readings.** (a) Experimental metadata encoding is a violation (R1 as written): certification fails. (b) It is conduct-bound like an experimental record type: the file is conforming, the reader ignores the record, certification succeeds. I picked (a), because the register row is the more specific text and §21.1 makes its enumeration normative — but I note that (b) follows from the stated principle, and a corpus vector for R1's experimental instances would settle it.

### AMBIGUITY — §5.2 `[R-CNT-21]` and §9.7 `[R-LIF-08]`

Byte-level: False

`[R-CNT-21]` makes the slack total an unconditional verifier output — "a verifier MUST report the total number of slack bytes, since that number is what tells an operator to compact" — but the total is defined by subtraction from a walk that a nonconforming file can prevent from completing. If a layer's crc_of_crc_array fails, its entries cannot be acted on at all (`[R-ENC-05]`: no reader "MUST NOT allocate, seek, or issue I/O based on any integer obtained from a file before the checksum covering it has been verified"), so that layer's stored-tile bytes are neither claimable nor demonstrably slack. Overlapping claims break the subtraction arithmetic outright.

**Readings.** (a) Report the total only for files whose walk completes, and report "undetermined" otherwise. (b) Report a total computed with unverifiable regions treated as slack (over-reports slack, which pushes an operator to compact a file that may be damaged). (c) Report a total treating them as claimed (under-reports). I picked (a) with a partial figure and an explicit list of unwalkable regions, and I compute the total as a byte-set union rather than by subtraction so that an overlap does not silently double-count.

### AMBIGUITY — §18.2 `[R-MTA-05]` vs §21.2 row F30 and §21.3 row L49

Byte-level: True

`[R-MTA-05]` binds "object members" without qualification — on its face every object in the document, at any nesting depth. Rows F30 and L49 both phrase the condition as "a top-level user-metadata document's object members are not in ascending order," which reads as the document's outermost object only. §18.2's fourth bullet settles the *key* form ("`[R-MTA-05]`'s sort order is likewise over decoded keys' UTF-8 bytes") but not the recursion.

**Readings.** (a) All objects recursively, including objects nested inside `tarn.axes` array elements and `tarn.stats` values. (b) The outermost object only, per the register rows' wording. I picked (a): §21.1 says "where a row and the rule it cites diverge, the rule governs," and (a) is also the only reading under which `[R-MTA-05]`'s stated purpose — "This makes one writer's output reproducible for identical content" — is achieved. A writer that sorts only the top level under reading (b) would fail my verifier.

### AMBIGUITY — §21.4 row T26 and §17.3 `[R-COD-10]`

Byte-level: False

T26 is a register row with detector *verifier* and three named instances, but `[R-COD-10]` gives it no detection procedure of its own: "where the resulting decoded image breaks a stated content obligation (§14.5's padding, `[R-SER-08]`'s bool bytes) a verifier detects it as a validity error at tile scope, and otherwise the consequence is wrong sample content — undetectable by construction (§21.7)." A verifier that inverts the filter at the mandated stride and finds a padding position not carrying fill has observed exactly the evidence of T4; nothing in the decoded image distinguishes "writer used the wrong stride" from "writer wrote the wrong padding bytes." T26 therefore has no independent implementation, yet `[R-ERR-02]` demands a vector per instance whose "expected verdict is that row's outcome".

**Readings.** (a) T26 is a cause label, not a check: report T4/T2 and optionally name a wrong stride as a candidate cause. (b) T26 is a distinct check: re-invert the image at each plausible wrong stride and report T26 when one of those inversions yields conforming padding. I picked (a) — (b) is a heuristic repair-by-inference of the kind `[R-CNF-04]` forbids readers, and a verifier inherits every reader obligation (`[R-CNF-11]`) — so my verifier emits T4/T2 and never T26.

### AMBIGUITY — §2.3 `[R-CNF-11]`, §2.4 `[R-CNF-12]`, against `[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-TYP-10]`, `[R-LIF-07]`, `[R-ENC-14]`

Byte-level: True

A verifier "checks every file-level requirement... and certifies conformance," and certifies "only violation-free files." The document contains file-level SHOULDs whose deviation leaves observable bytes: unzeroed gaps (`[R-CNT-03]`), a discovery window over 65,536 bytes (`[R-CNT-09]`), a version_minor above the feature floor (`[R-CNT-26]`), a non-zero default fill (`[R-TYP-10]`), non-NFC names (`[R-ENC-14]`). None has a register row. §2.1's note says "every SHOULD states the consequence of deviation," and in each case the stated consequence is practical, not conformance — but the document never says a SHOULD deviation is not a "violation" for `[R-CNF-12]`'s purposes.

**Readings.** (a) SHOULD deviations never bar certification; a verifier reports them as advisories. (b) They bar certification, since `[R-CNF-11]` says "every file-level requirement." I picked (a): the register is the enumeration a verifier is built from, §21.1 makes its completeness normative, and no SHOULD appears in it. My verifier emits them in a separate advisory channel that never affects the certificate.

### AMBIGUITY — §6.1 `[R-CNT-04]` vs §2.3 `[R-CNF-11]` and §21.2 row F8

Byte-level: True

`[R-CNT-04]` splits the front-block obligation by transport: a local reader "MUST verify the full block by byte equality before other processing," while "A remote reader, one whose transport charges a round trip per range (§6.4), MAY defer or omit this check." F8 lists the condition with detector *reader*. A verifier operating over a remote transport is literally a remote reader, so read narrowly it may omit the one check that distinguishes a TARN file from a coincidence.

**Readings.** (a) A verifier always fetches and compares [0,16) regardless of transport, because `[R-CNF-11]` requires it to check every file-level requirement including ones readers are exempt from, and `[R-CNT-04]` is exactly such an exemption. (b) A remote verifier inherits the exemption and certifies without ever reading byte 0. I picked (a). Under (b) a file with a corrupted front block could be certified, which contradicts `[R-CNF-12]`'s violation-free requirement.

### AMBIGUITY — §17.4 `[R-COD-11]` — the phrase "the rule of §9.7(d)"

Byte-level: False

`[R-COD-11]` justifies its rule by reference: "A verifier that cannot execute a layer's codec or filter cannot establish the layer's conformance and MUST NOT certify the file — the rule of §9.7(d) applied to content." §9.7 has no lettered clauses; it is a single paragraph plus a note, and no (a)/(b)/(c)/(d) enumeration appears anywhere in §9. `[R-MTA-09]` leans on the same rule ("exactly as `[R-COD-11]` requires"), so the dangling reference propagates.

**Readings.** (a) The intended referent is `[R-LIF-08]`'s principle that a verifier certifies only what it can actually walk and check. (b) It refers to a since-removed enumerated clause. Either way the operative rule of `[R-COD-11]` is self-contained — MUST NOT certify — so I implemented it directly and ignored the citation; nothing in my verifier depends on resolving it.

### AMBIGUITY — §14.2 `[R-SER-08]` vs §21.4 row T2

Byte-level: False

`[R-SER-08]` binds every interleaved bool value: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value." T2 narrows the registered condition to "a real (non-padding) sample position." At a padding position the byte is additionally governed by `[R-SER-05]` (must be the recorded fill byte, itself constrained to 0x00/0x01 by `[R-TYP-07]`), so the two rules overlap there.

**Readings.** (a) T2 covers real positions and T4 covers padding positions; a bad bool byte at a padding position is reported as T4. (b) `[R-SER-08]` covers both and a padding position with byte 0x02 is both T2 and T4. Both readings give the identical outcome (validity error at tile scope) and identical certification verdict, so the choice is cosmetic. I picked (a) for reporting, per the register's own instance wording, and check every interleaved bool byte in the tile either way.

### AMBIGUITY — §15.3 `[R-IDX-03]` ("bind over well-formed entries' extents only") vs §5.2 `[R-CNT-02]` and §9.7 `[R-LIF-08]`

Byte-level: False

`[R-IDX-03]` excludes reject-tile entries from the *verifier rows* (overlap, alignment, slab): "an entry these rows classify reject-tile contributes no stored extent to the *verifier* rows." It says nothing about the coverage partition. §9.7 has the walk enumerate "each layer's tile-index region together with that region's non-sentinel entries" — a malformed non-sentinel entry is a non-sentinel entry.

**Readings.** (a) A reject-tile entry's extent is excluded from coverage as well, so its bytes fall to slack and inflate the slack total. (b) It is a claimant for coverage but not for the verifier rows, which is incoherent for an entry with offset 12 or length beyond F−64 (the range is not a legal range at all). I picked (a) — an entry whose fields fail their own domain checks cannot name bytes — and I report such entries' nominal ranges separately so the slack figure is not read as a clean bill.

### AMBIGUITY — §16.2 `[R-SLB-03]`

Byte-level: True

The packing invariant reads: "each stored tile's offset equals the previous stored tile's offset plus its length." The antecedent of "its" is grammatically the previous stored tile but could be parsed as the current tile's.

**Readings.** (a) offset[k] = offset[prev] + length[prev] — the previous tile's length, which is the only reading under which the tiles are contiguous and non-overlapping. (b) offset[k] = offset[prev] + length[k], which is arithmetic nonsense for a forward-packed run (it would place tile k before the tile ahead of it whenever lengths differ). I picked (a); (b) is unimplementable as a packing rule. The example in §16.2 ("If ordinal 10 is a sentinel, run 1's stored tiles are 8, 9, 11…15, packed with no gap where 10 would have been") is consistent with (a) and does not by itself disambiguate the lengths.

### AMBIGUITY — §2.3 `[R-CNF-11]`, §5.2 `[R-CNT-21]`, §18.2 `[R-MTA-05]`

Byte-level: False

Two verifier outputs are mandated by name — the slack total (`[R-CNT-21]`) and unsorted metadata members (`[R-MTA-05]`: "the file is nonconforming, a verifier MUST report it") — but nothing states whether a verifier must enumerate *all* violations or may stop at the first. The difference is large in practice: a first-failure verifier is useless for corpus work, and a full-enumeration verifier must decide what to do downstream of a failed link in §8.2's ordered chain (a failed crc_of_crc_array forbids acting on any entry of that layer, per `[R-ENC-05]`).

**Readings.** (a) Certification is a predicate and enumeration is implementation technique. (b) Full enumeration is implied by "checks every file-level requirement." I picked (a) for the certificate and (b) for the report: my verifier enumerates every independently decidable violation, marks scopes it could not reach as unexamined rather than clean, and never acts on integers from a region whose covering checksum failed.

### OBSERVATION — §7.2 `[R-CNT-13]`, §9.7 `[R-LIF-08]`, §14.5 `[R-SER-05]`, §21.9 `[R-ERR-03]`

Byte-level: False

Certification is Θ(every stored byte) in time and Θ(stored-tile count) in working memory, while a reader's per-tile cost is O(1) plus one segment. Two obligations drive it: overlap detection needs an interval union over every stored-tile extent of every layer plus every record extent and index region, and the decoded-content obligations (`[R-SER-05]`, `[R-SER-08]`) require decoding *every* stored tile of every layer and inverting its filter — checking padding positions and pad bits is not samplable, since one wrong padding byte in one edge tile is a violation. §21.9's minimum guarantees bound only what a *reader* must accept (2³² addressed tiles per layer, 65,536 layers, 256 MiB decoded tiles); nothing anywhere bounds a verifier, so a file that a conforming reader must accept can present a verifier with 2⁴⁸ extents to sort and petabytes to decompress. §24 concedes the shape of the problem for the corpus — `[R-VEC-03]`: "the tile-count guarantee is not [constructible], its index region alone running to tens of gigabytes of incompressible entries" — without drawing the parallel conclusion for the verifier. Decidable, but disproportionately expensive, and the spec offers no license to sample: `[R-COD-11]` says a verifier that cannot do the work "MUST NOT certify the file."

### OBSERVATION — §9.7 `[R-LIF-08]` vs §5.2 `[R-CNT-02]` and §6.2 `[R-CNT-05]`

Byte-level: False

Two facts a verifier needs for the coverage walk are derivable but never stated, and each cost me a pass over the document. First, §9.7 says the walk checks "that each lies within [16, F − 64)", yet §5.2's partition classes and F36's instance list both name the trailer and the front signature block as members of the partition — and the trailer at [F−64, F) fails that bound by construction. The bound evidently applies only to the items §9.7 enumerates (records, extents, index regions, entries), with the front block and trailer joining the disjointness set at fixed positions; nothing says so. Second, `[R-CNT-05]`'s prohibition on structures between the directory's end and the trailer, combined with the no-overlap rule, collapses to a single crisp invariant that the document never writes down: every live structure other than the directory and the trailer lies entirely within [16, dir_offset). That one line is the whole of the F9 check and most of the placement half of the walk; deriving it rather than reading it is the kind of expense worth naming.


## Verdict
The document is implementable as a verifier from the text alone, and I built the whole procedure — nine phases, all 20 verifier-detected register rows, the coverage walk, overlap sweep, alignment/slab invariants, and the decode-everything content pass — without consulting anything else. Its strongest properties for this role are exactly the ones a verifier lives on: the checksum is pinned tightly enough that my from-scratch CRC-32C reproduced all four published constants including Appendix A's trailer CRC and the all-sentinel segment value; §21's register is arithmetically self-consistent (125 rows, 244 instances, matching `[R-ERR-02]`); the reader/verifier detection split is stated per row rather than left to inference; and `[R-IDX-03]`'s exclusion of reject-tile entries from the verifier rows resolves what would otherwise be the nastiest ordering problem in overlap detection. The decoded-content obligations — padding positions, packed pad bits, interleaved bool bytes — are specified to the bit, with worked examples that function as acceptance tests.

The gaps are concentrated in one place: the boundary between a *reader outcome* and a *certification verdict*. The document is meticulous about the former and near-silent about the latter, and a verifier is the only actor that needs the latter. Whether an ignore-record condition bars certification (§21.5 vs `[R-CNT-25]`), whether experimental values are conduct-bound or byte-bound in the metadata-encoding space alone, whether a SHOULD deviation is a "violation" for `[R-CNF-12]`, and what the mandatory slack total means on a file whose walk cannot complete — four decisions that determine my verifier's answer on real files, none of them written down. Two harder defects sit beside them: §9.6 and §9.7 prescribe opposite procedures for coverage-related generation enumeration, and `[R-MTA-07]` states a writer MUST NOT with no register row, which §21.1's own normative completeness clause classifies as a defect in the document. F36's "trailer" and "front signature block" instances name overlaps that the reader-detected bounds rules make unexhibitable, so `[R-ERR-02]`'s one-vector-per-instance obligation cannot be met for them — the same class of defect §5.2's Note records as already found and deleted once.

None of this is fatal, and none of it required me to invent structure. Fixing the four verdict-boundary ambiguities is a matter of adding one paragraph to §21.1 saying which register sections bar certification, and the two contradictions are single-sentence repairs.