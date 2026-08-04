# Cleanroom Reader Walkthrough — TARN Array Model (§11–§16)

**Charter:** READER. Source of truth: `spec/tarn.md` only (working draft; §17 Codecs, §18 User Metadata, §19 Reading, §20 Writing, §21 Error Register/Limits, §22–§24 and Appendices are *[Reserved]*). The codec is treated throughout as an opaque stored-bytes → decoded-bytes transform of known output size, per charter. All citations are to that document's sections and requirement IDs.

**Independent verification performed:** I re-derived the three CRC-32C constants the spec states, using only §4.5's algorithm definition (Castagnoli 0x1EDC6F41, reflected input/output, init 0xFFFFFFFF, final XOR 0xFFFFFFFF): `"123456789"` → `0xE3069283` ✓ (§4.5 check vector); zero bytes → `0x00000000` ✓ (§4.5, and the smallest-file example §5.1); a full segment of 2¹⁶ sentinel entries (1,310,720 bytes of `FF ×16 00 ×4`) → `0xEECB3BB2` ✓ (`[R-IDX-05]`). Every worked numeric example in §11–§16 was also re-derived by hand and checks out (details in Findings/OBSERVATION).

---

## 1. The full walk: "channel values at coordinate (x₀,…,x_{d−1}) of layer named Z"

### 1.0 Container prerequisites (the platform the array model stands on)

1. **Front block** (local reader/sniffer only): bytes [0, 16) must equal `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes, by byte equality; mismatch → reject-file. A remote reader may defer/omit this (`[R-CNT-04]`).
2. **Trailer**: fetch the final 64 bytes. Validate **in order**: trailer magic `8A 4E 52 41 54 0D 0A 1A`; trailer CRC — CRC-32C over trailer bytes [0, 60) compared to the u32 at [60, 64); the version gate (version_major = 1, minor never gates) (`[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-24]`). Then, gates passed: incompat-lane flag bits 0–15 all implemented (none defined in this text → must be 0 to proceed; ignore-lane bits 16–31 ignored); committed_file_length = transport-authoritative file size F and F mod 64 = 0; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; generation ≥ 1; file_id ≠ 0; reserved [56, 60) zero. Any failure → reject-file (`[R-CNT-06]`, `[R-CNT-08]`, `[R-CNT-10]`).
3. **Directory**: fetch [dir_offset, dir_offset + dir_length). Verify its final 4 bytes as CRC-32C over the preceding dir_length − 4 bytes **before any other use** of the region; mismatch → reject-file (`[R-CNT-11]`). The directory is always raw — no codec on the open path (`[R-CNT-25]`).
4. **Record scan**: parse the record sequence under §7.2 framing (24-byte header: type u16, flags u16, inline_length u32, extent_offset u64, extent_length u64; then inline_length payload bytes). Header/payload overrunning the sequence, or type 0 → reject-file (`[R-CNT-12]`). Record order carries no meaning (`[R-CNT-14]`). Unknown top-level type: MU=1 → reject-file, MU=0 → ignore-record (`[R-CNT-15]`). Locate the layer record (type 0x0001) whose name equals Z by **raw byte comparison** — no normalization or case folding (`[R-ENC-13]`). Two layer records with identical name bytes → reject-file (`[R-ENC-15]`).

Per `[R-ENC-05]`/`[R-ENC-10]`, no integer from the file is used to allocate, seek, or fetch before the checksum covering it verifies: trailer fields are usable after the trailer CRC, layer-record fields after the directory CRC, index-entry fields after the segment chain (below), tile bytes after the entry crc.

### 1.1 Layer-record fields consumed (§7.4), and their validation

From Z's inline payload, packed in table order with no padding (`[R-CNT-18]`):

| Field | Consumed for | Validity on this path |
|---|---|---|
| name | matched against Z | §4.6 name rules (`[R-ENC-12]`) |
| layout u8 | value-sequence mode, addressed-tile count, disk ordinal | must be 1 (interleaved) or 2 (planar); anything else → reject-layer (`[R-SER-06]`) |
| linearization u16 | spatial-ordinal formula | must be 1 (row-major); 0, 2, 3, reserved, experimental → reject-layer (`[R-GEO-05]`) |
| codec u16 | opaque decode pipeline | 0 invalid (`[R-CNT-23]`); value set is §17's subject — *reserved* (see Findings) |
| filter u16 | opaque decode pipeline | 1 = none, 2 = byte-shuffle; 0/reserved → reject-layer (§7.4, `[R-CNT-23]`) |
| alignment A, slab S, A_slab | **not used by the read path** — offsets are explicit; alignment/slab invariants bind verifiers (`[R-SLB-01]`, `[R-SLB-03]`) | A ≠ 0 ∧ S ≠ 0 → reject-layer (`[R-CNT-16]`); nonzero non-power-of-two/out-of-range A, S, A_slab, or A_slab ≠ 0 with S = 0 → reject-layer (`[R-CNT-23]`) |
| rank d u8, channel count C u16 | loop bounds | d ≥ 1, C ≥ 1, all Tᵢ ≥ 1; else reject-layer (`[R-GEO-01]`) |
| d dimension entries (name, Eᵢ u64, Tᵢ u64) | bounds check, tiling arithmetic | names unique in layer (`[R-ENC-15]` → reject-layer); Eᵢ, Tᵢ ≤ 2⁶³ − 1 (`[R-ENC-03]`) |
| C channel entries (name, type u16, fill bytes) | element sizes B_c, fill values, tuple order | type ∈ 1..13, else reject-layer (`[R-TYP-03]`); fill length = element size, else reject-layer (`[R-CNT-23]`); bool fill ∈ {0x00, 0x01}, else reject-layer (`[R-TYP-07]`) |
| index_encoding u8 | region layout | must be 1 (raw-segmented); else reject-layer (§7.4, §15) |
| entry_count u64 | segment count, cross-checks | must equal geometry-derived addressed-tile count (below); else reject-layer (`[R-CNT-17]`) |
| crc_of_crc_array u32 | verifies segment CRC array | 0 when entry_count = 0, else nonzero mismatch handled at verify time (`[R-CNT-23]`, `[R-IDX-04]`) |
| extent slot (extent_offset, extent_length) | index-region location | (0, 0) iff zero addressed tiles; malformed slot (one half zero, offset < 16, past F − 64, overflow) → reject-layer (`[R-CNT-13]`); extent_length must equal entry_count·20 + ⌈entry_count/2¹⁶⌉·4 → else reject-layer (`[R-CNT-17]`) |

Payload must parse exactly — fixed fields, d dimension entries, C channel entries, trailing fixed fields all inside the inline payload, remainder parsing as complete sub-records with no residue; violation → reject-layer (`[R-CNT-18]`).

**Coordinate domain check:** the request is answerable only for 0 ≤ xᵢ < Eᵢ for all i (`[R-MDL-01]`); coordinates at or beyond any extent are not in the reference array (an extent-0 dimension means the layer has no samples at all, `[R-GEO-02]`).

### 1.2 Coordinate-to-tile arithmetic (§11.2, §11.4)

All in **declared dimension order**, with overflow of any sum/product beyond 2⁶³ − 1 → reject-layer (`[R-ENC-04]`, `[R-GEO-03]`):

- Grid counts: Gᵢ = Eᵢ/Tᵢ + (1 if Eᵢ mod Tᵢ ≠ 0 else 0) — the spec deliberately specifies this form, not (Eᵢ+Tᵢ−1)/Tᵢ, to avoid intermediate overflow (§11.2 Note).
- N = ∏ Gᵢ (spatial tiles), P = ∏ Tᵢ (sample positions per tile).
- Addressed-tile count = N (interleaved) or C·N (planar) (`[R-GEO-03]`); must equal entry_count (`[R-CNT-17]`).
- Tile coordinates tᵢ = xᵢ div Tᵢ; in-tile position uᵢ = xᵢ mod Tᵢ.
- In-tile sample ordinal m = Σᵢ uᵢ · ∏_{j>i} Tⱼ (row-major, permanent for every linearization) (`[R-GEO-06]`).
- Spatial tile ordinal (linearization 1): s = Σᵢ tᵢ · ∏_{j>i} Gⱼ.
- **Disk tile ordinal(s)**: interleaved → the single tile k = s; planar → one tile per channel, k_c = c·N + s, c the channel's 0-based declared index (channel-major grouping) (`[R-GEO-06]`).

### 1.3 Index entry location and the exact verification chain

Under index_encoding 1 the region at [extent_offset, extent_offset + extent_length) is contiguously: entry array (entry_count × 20 bytes) then segment CRC array (⌈entry_count/2¹⁶⌉ × 4 bytes), no padding (`[R-IDX-01]`). Entry k is the 20 bytes at region offset 20·k: offset u64, length u64, crc u32.

**Chain of trust, strictly ordered (§8.2 `[R-CNT-20]`):** trailer → directory → crc_of_crc_array → segment CRC array → index segment → index entry → stored tile. Concretely, to use entry k:

1. Trailer CRC over file bytes [F−64, F−60+56) = [F−64, F−4), compared to u32 at [F−4, F) — already done at open (fail → reject-file).
2. Directory CRC over [dir_offset, dir_offset + dir_length − 4), compared to the region's final 4 bytes — already done (fail → reject-file). This is the checksum covering every layer-record field, including extent_offset/length, entry_count, and crc_of_crc_array.
3. Layer cross-checks (`[R-CNT-17]`): extent_length = entry_count·20 + ⌈entry_count/2¹⁶⌉·4, entry_count = geometry-derived count (fail → reject-layer).
4. Fetch the **whole** segment CRC array — region bytes [entry_count·20, entry_count·20 + ⌈entry_count/2¹⁶⌉·4) — and the **whole segment containing k** — segment index σ = k div 2¹⁶, covering entries [σ·2¹⁶, min((σ+1)·2¹⁶, entry_count)), i.e. region bytes [σ·2¹⁶·20, min(…)·20). Both ranges are computable from the layer record alone and MAY be fetched in parallel, but verification is in dependency order (`[R-IDX-04]`):
   - CRC-32C over the fetched CRC array, compared to the layer record's crc_of_crc_array (fail → reject-layer);
   - CRC-32C over the fetched segment's bytes exactly as stored, compared to the σ-th u32 of the array (a final partial segment's CRC covers only its actual bytes) (fail → reject-layer).
5. Classify entry k per §15.3 (`[R-IDX-03]`), sentinel pattern first (`[R-ENC-03]`/`[R-ENC-04]` apply to non-sentinel entries only, `[R-IDX-02]`):
   - offset = 2⁶⁴−1 ∧ length = 2⁶⁴−1 ∧ crc = 0 → **valid sentinel**, reads as fill (skip to §1.5's fill path);
   - the sentinel pattern with crc ≠ 0, or exactly one of offset/length all-ones → reject-tile;
   - non-sentinel with length = 0, or offset < 16, or offset/length > 2⁶³−1, or offset + length overflowing or > F − 64 → reject-tile.
6. Fetch the stored bytes [offset, offset + length). Compute CRC-32C over exactly those bytes; compare to the entry's crc field. Mismatch → reject-tile (§8.1, `[R-CNT-20]`). Only now may the bytes be interpreted.

### 1.4 Payload decode and offset arithmetic (both layouts)

Feed the stored bytes to the opaque codec/filter pipeline named by the layer's codec and filter fields (§17, reserved). The expected **decoded size** is a function of declarations alone — never of payload content — and the reader allocates from it (`[R-SER-07]`):

| Case | Decoded size | Where the requested value lives |
|---|---|---|
| interleaved (any channel mix; bool as 1 byte) | P · Q, Q = Σ Bᵢ (sample stride) | channel c: bytes [m·Q + F_c, m·Q + F_c + B_c), F_c = Σ_{j<c} Bⱼ (`[R-SER-02]`; equivalently value k = m·C + c at (k div C)·Q + F_{k mod C}) |
| planar, numeric channel c | P · B_c | bytes [m·B_c, (m+1)·B_c) (`[R-SER-02]`) |
| planar, bool channel | ⌈P/8⌉ | bit (m mod 8) of byte (m div 8), LSB-first (bit 0 least significant, §4.4 `[R-ENC-08]`); 0 = false, 1 = true (`[R-SER-03]`) |

A decoded payload whose length is not exactly the decoded size → reject-tile (`[R-SER-07]`). Values are little-endian at the type's element size (`[R-ENC-01]`, §12.1); the value sequence is in-tile-ordinal order, sample-major with channels adjacent in declared order for interleaved (`[R-SER-01]`).

### 1.5 The returned value

Return the C-tuple in declared channel order:

- **Interleaved**: all C values come from the one tile k = s — either the decoded bytes at the offsets above, or (sentinel) every channel's fill: the tuple of recorded fill bytes in declared channel order (`[R-TYP-08]`).
- **Planar**: each channel independently — channel c from tile k_c = c·N + s if stored (its own chain steps 4–6 and decode), or channel c's recorded fill bytes if k_c is the sentinel; one sample can mix decoded and fill channels (`[R-MDL-01]`, `[R-TYP-08]`).

Every returned value is the encoded bit pattern, bit-for-bit: no NaN quieting, no canonicalization, −0.0 ≠ +0.0, fill returned exactly as recorded (`[R-MDL-02]`, `[R-TYP-04]`, `[R-TYP-06]`). A planar bool value is returned as the logical value its bit denotes (§12.1, `[R-SER-03]`).

---

## 2. Cold-read accounting: entry_count = 1,000,000, disk ordinal 999,999

Geometry of the index region (index_encoding 1, `[R-CNT-17]`, `[R-IDX-01]`, `[R-IDX-04]`):

- Entry array: 1,000,000 × 20 = 20,000,000 bytes, region [0, 20,000,000).
- Segments: ⌈1,000,000 / 65,536⌉ = 16 — segments 0–14 full (65,536 entries each, covering entries 0–983,039), segment 15 partial with 1,000,000 − 983,040 = 16,960 entries.
- Segment CRC array: 16 × 4 = 64 bytes, region [20,000,000, 20,000,064). Region total 20,000,064 bytes = required extent_length.

Target: k = 999,999 → σ = 999,999 div 65,536 = 15; segment-relative entry 999,999 − 983,040 = 16,959, at segment-relative byte 20 × 16,959 = 339,180 (region byte 19,660,800 + 339,180 = 19,999,980; the entry is region bytes [19,999,980, 20,000,000)).

**Exact index-region fetches and verifications** (file offsets are extent_offset + the region offsets given):

1. Region **[20,000,000, 20,000,064)** — the whole 64-byte segment CRC array. CRC-32C over all 64 bytes, compared to the layer record's crc_of_crc_array. (Fail → reject-layer.)
2. Region **[19,660,800, 20,000,000)** — the whole of segment 15: 16,960 × 20 = 339,200 bytes. CRC-32C over all 339,200 bytes, compared to the array's u32 index 15 (array bytes [60, 64), i.e. region [20,000,060, 20,000,064)). (Fail → reject-layer.)

The two fetches MAY be issued in parallel; verification order is array first, then segment (`[R-IDX-04]`).

**Verified index bytes for this read: 64 + 339,200 = 339,264 bytes** (the spec's own §15.4 example says "~339 KB" for exactly this case — confirmed).

**Worst case for this layer**: the target ordinal falling in a full segment (any k < 983,040): 65,536 × 20 = 1,310,720 bytes (1.25 MiB) + 64-byte array = **1,310,784 bytes** of index verified. The spec's general bound — never more than one full segment plus the CRC array, at any layer scale — holds, noting the array itself grows as ⌈entry_count/2¹⁶⌉ × 4 (here 64 bytes).

Outside the index region, the same cold read also CRC-verifies the 64-byte trailer (CRC over its first 60 bytes), the dir_length-byte directory (CRC over dir_length − 4), and the stored tile's own bytes (entry's crc over all `length` stored bytes — data-dependent, not quantifiable from entry_count).

---

## 3. Degradation walks

| Case | Outcome class | Scope / blast radius | Assigning requirement |
|---|---|---|---|
| (a) entry is the sentinel (`FF ×16 00 ×4`) | **not a violation** — the tile reads as fill (each channel it carries returns its recorded fill at every in-extent position); this is the *only* condition that produces fill | that one addressed tile; interleaved → whole fill sample, planar → exactly that entry's channel | `[R-IDX-02]`, `[R-IDX-03]` row 1, `[R-TYP-08]`, guarded by `[R-TYP-09]` |
| (b) entry's crc ≠ CRC-32C of the stored bytes | **reject-tile** | that tile only; neighbors in the same layer unaffected; reader MUST NOT return fill for it | `[R-IDX-03]` ("stored bytes fail the entry's crc"), `[R-CNT-20]`, `[R-CNF-09]`/`[R-TYP-09]` |
| (c) a segment CRC mismatches its computed value | **reject-layer** | the whole layer's data and metadata; other layers unaffected; the layer's name may still be listed | `[R-IDX-04]`, `[R-CNT-20]`, scope table §2.4 |
| (d) channel-type value 14 | **reject-layer** — 14 is reserved without semantics (pinned for a possible OFP8 E4M3, but assigned nothing); reader MUST NOT infer an element size from it | the declaring layer only — "never the file" | `[R-TYP-03]`, `[R-CNT-23]`, §12.2 + its Note, `[R-CNF-04]` |
| (e) decoded payload one byte longer than the decoded size | **reject-tile** — decoded size is declaration-derived, never content-derived | that tile only | `[R-SER-07]` |
| (f) interleaved bool value byte 0x02 | file is **nonconforming**; assigned detector is the **verifier**, for which it is a validity error at **tile scope**. An ordinary reader is not obligated to screen decoded content and is not nonconforming for missing it; a reader that does detect it MAY reject (per `[R-CNF-12]`) — no defined return value exists for the byte | tile scope when detected | `[R-SER-08]`, `[R-CNF-12]` |
| (g) linearization value 2 | **reject-layer** — 2 is reserved without semantics | the declaring layer only | `[R-GEO-05]` |

---

## 4. The fill path

**Planar mixed sample.** Layer planar, channels A and B; at spatial ordinal s, A's tile (disk ordinal idx(A)·N + s) is the sentinel and B's tile (idx(B)·N + s) is stored. One sample there returns: B's value decoded from B's stored tile (offset m·B_B, or bit m for bool, after B's tile passes its full chain), and A's value = **the recorded fill bytes of A's channel entry, bit-exact**. The mix within a single sample is explicitly defined behavior (`[R-MDL-01]`, `[R-TYP-08]`, §13.3's r/g/b example). B's storedness never influences A's result: per-channel storedness is independent in planar layers.

**NaN-payload float fill.** A float32 channel whose recorded fill is `0x7FC00001` (a NaN carrying payload bit 0; stored little-endian as `01 00 C0 7F`) returns **exactly the bit pattern 0x7FC00001** — the recorded bytes, unaltered. Fill is authoritative and bit-exact: no type-derived default, no quieting, no canonicalization (`[R-TYP-06]`, `[R-TYP-04]`, §12.3's worked example: "equally valid and round-trips bit-exactly").

**Unstored tile, interleaved layer.** The sentinel entry covers all C channels at once: every sample position of that tile inside the layer's extents reads as the **full fill sample** — each channel's recorded fill, in declared channel order (`[R-TYP-08]`; §13.3 example: fills 0xFF/0x00/0x00 → every sample reads (255, 0, 0)). Fill flows only from a sentinel read through a *verified* chain: a malformed entry, failed segment/array CRC, or failed tile CRC is a rejection, never fill (`[R-TYP-09]`, `[R-CNF-09]`).

---

## 5. Edge tiles

**Clipping.** Where Gᵢ·Tᵢ > Eᵢ, the high-edge tiles along dimension i contain padding positions — positions whose coordinate along that axis would be ≥ Eᵢ (§11.3). The decoded image covers the full logical tile shape, so the reader's clip is arithmetic on output, not on decode: a value at in-tile position (u₀,…,u_{d−1}) of tile (t₀,…,t_{d−1}) is returnable iff tᵢ·Tᵢ + uᵢ < Eᵢ for every i. In the single-coordinate walk of §1 this is the up-front domain check; in a region read it means enumerating only in-extent positions of the edge tile.

**What it must never return.** Padding positions — they are not part of the reference array (`[R-MDL-01]`), and "a reader MUST NOT return padding positions as samples" (`[R-GEO-04]`). Writers must have encoded fill there (`[R-SER-05]`), so an accidental non-clipping reader observes fill rather than garbage (§14.5 Rationale) — but returning it is still a conformance violation; the reader is also not obligated to *check* padding content (that duty is the verifier's, tile scope, `[R-SER-05]`).

**Decoded size, edge vs interior: identical.** Every tile of a layer has the same logical shape (T₀,…,T_{d−1}) (§3.1, §11.3), P = ∏ Tᵢ counts padding positions too, and decoded size is a function of declarations alone (`[R-SER-07]`): P·Q interleaved, P·B_c planar numeric, ⌈P/8⌉ planar bool — for every tile, edge or interior. Edge tiles are never truncated; §14.5's example (extents (5,5), tiles (4,4), uint16: the corner tile with one real sample is still 32 decoded bytes) confirms.

---

## 6. Verdict

**Sections 11–16 are implementable as a reader from this text alone, with the codec opaque** — the geometry, ordinal, index, verification, fill, and serialization arithmetic is fully determined, richly cross-referenced, and every worked example I re-derived is correct, including all three CRC constants. The container (Part I) supplies a complete open path. What I had to guess or could not resolve:

1. **The codec value set** — the one genuinely unresolvable forward reference. §7.4 says only "codec u16, §17 (0 invalid)"; `[R-CNT-23]` demands reject-layer for "unassigned" codec values, but the assignment set is §17's reserved subject. I cannot write that validity check, and `[R-CNF-03]`'s core-codec obligation is unknowable. (Filter is fine: §7.4 enumerates its full value set; only byte-shuffle's *semantics* are opaque.)
2. **The codec boundary contract** — I assumed the pipeline yields a byte string whose length the reader compares against the declaration-derived decoded size (`[R-SER-07]`), which works for any opaque transform; whether §17 adds obligations (e.g., declared-output-size framing, mid-decode limits) is unknowable.
3. **Verification caching** — I read "to use entry k, a reader MUST verify" (`[R-IDX-04]`) as once-per-snapshot, justified by committed-prefix immutability (§9.1, §9.3, §9.5), not once-per-use.
4. **§19 (Reading) and §21 (limits/error register) are reserved** — I reconstructed the read algorithm from §6–§8 + §15; §19 may constrain it further, and the minimum guarantees a reader must accept (`[R-CNF-10]`) are unknowable.
5. **Out-of-extents requests** — no outcome class exists for a coordinate outside the reference array; I treat it as an API-domain error, not a file outcome (defensible from `[R-MDL-01]`/`[R-MDL-02]`: the conformance target is defined only on the reference array).

## Findings

### AMBIGUITY

- **A1 — §7.4 codec field / `[R-CNT-23]` / §17 (reserved).** `[R-CNT-23]` requires reject-layer for "a reserved or unassigned … codec … value," but the codec value set lives in reserved §17, so both "every nonzero value is potentially assigned" and "no value is yet assigned" are consistent readings — the check is unwritable. **Picked:** validate only codec ≠ 0 structurally; surface any codec as "unsupported" (read fails at layer granularity) pending §17. Least destructive, and matches how §12.2 handles unknown-to-the-reader enum values (reject-layer, never reject-file). This is the charter's "unresolvable forward reference" case.
- **A2 — `[R-IDX-04]` "To use entry k, a reader MUST verify…".** Per-use re-verification vs. per-session caching of the array/segment verification is not stated. **Picked:** verify each fetched range once per open snapshot; §9.1/§9.3/§9.5 immutability makes cached verification sound, and `[R-LIF-03]` explicitly licenses (file_id, range)-keyed caching.
- **A3 — `[R-ENC-15]` duplicate-name detection scope on the read path.** "A reader MUST treat a duplicate name as a validity error" — it is unstated whether a reader serving one layer must detect duplicates *among other layers'* names, or only duplicates it encounters resolving Z. **Picked:** compare all layer names in one pass during the directory parse (the directory is fully resident and CRC-verified anyway, so cost is negligible) and reject-file on any duplicate; deep payload validation only for the target layer, per §2.4's blast-radius model.
- **A4 — `[R-SER-08]` detecting-reader behavior for interleaved bool 0x02.** The tile-scope assignment names the verifier; for an ordinary reader that happens to detect the byte, `[R-CNF-12]` says it "MAY reject" without fixing the scope, and "no defined return value" exists otherwise. **Picked:** a reader that detects it rejects at tile scope (mirroring the verifier's assignment); a reader that doesn't screen returns the byte unaltered under `[R-TYP-04]` and is conforming per `[R-SER-08]`'s explicit safe-harbor.

### CONTRADICTION

- none. (Actively hunted: §2.4's exactly-one-outcome rule vs `[R-SER-08]`'s verifier-detector construction is consistent — `[R-CNF-12]` anticipates verifier-assigned detectors; §15.3's verifier-only rows are explicitly carved out of the reader obligation; §8.1's coverage map, §8.2's chain, and `[R-IDX-04]` agree; every worked example's arithmetic agrees with its normative rule.)

### OBSERVATION

- **O1 — Reads are tile-granular in I/O, verification, and decode.** The entry's crc covers the tile's entire stored bytes and the codec is an opaque whole-payload transform, so a single-sample read costs: full stored-extent fetch + full CRC + full decode. Not a defect — inherent to §8.1's coverage design — but implementers should surface a tile-cache.
- **O2 — The §15.4 worst-case phrasing is segment-bounded only.** "Never more than one full segment (1.25 MiB) plus the CRC array" is exact, but the CRC array grows as ⌈entry_count/2¹⁶⌉·4 bytes and must be fetched and verified *whole* for any entry use; at extreme entry counts (e.g. 2⁴⁰ entries → 64 MiB array) the array dominates the verified bytes. A future limits table (§21) capping entry_count would bound this.
- **O3 — Independent verification of stated constants.** Recomputed from §4.5's definition alone: `"123456789"` → 0xE3069283 ✓; empty input → 0x00000000 ✓; 2¹⁶ sentinel entries (1,310,720 bytes) → 0xEECB3BB2 ✓. All §11–§16 worked examples re-derived and correct, including §15.4's accounting (segment-relative byte 339,180; segment 15 = region [19,660,800, 20,000,000); region total 20,000,064) and §14.3's packed-plane bytes (`55 01` / `55 FD`).
- **O4 — Serial round-trip floor.** `[R-ENC-05]`/`[R-ENC-10]` force a cold single-sample read into at least four dependent fetch stages: trailer → directory → (CRC array ∥ segment, parallel pair) → stored tile. §6.4's 64 KiB suffix speculation can merge the first two; nothing can merge the last two with the first.
- **O5 — Planar all-channel reads may touch multiple segments.** Entries for one spatial ordinal s sit at disk ordinals c·N + s, spaced N·20 region bytes apart; for N ≥ 2¹⁶ they are guaranteed to lie in different segments, each requiring its own segment verification (the one whole-array verification is shared). Follows directly from `[R-GEO-06]`/`[R-IDX-01]`/`[R-IDX-04]`; worth stating in §19 when drafted.
- **O6 — Reader-invisible layout declarations.** A conforming reader can ignore A, S, A_slab entirely beyond structural validation (`[R-SLB-01]`, `[R-SLB-03]`): offsets are always explicit. Slab declarations are purely an optimization hint (range coalescing) on the read side.
