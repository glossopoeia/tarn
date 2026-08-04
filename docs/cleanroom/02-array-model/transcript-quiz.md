# Cleanroom Implementer Quiz — TARN Spec, Gate Transcript

**Source of truth:** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full (1,623 lines). No other file, tool, or prior knowledge consulted. All section numbers and `[R-…]` identifiers below refer to that document.

## Derived geometry (used throughout)

**Layer L** — planar (layout 2, §7.4/§14.1), linearization 1; dims declared (y, x); channels declared (m, t) so m has channel index 0, t has index 1 (§3.1, §11.4).

- G_y = ⌈10/4⌉ = 10 div 4 + 1 (since 10 mod 4 = 2 ≠ 0) = **3**; G_x = ⌈13/8⌉ = 1 + 1 (13 mod 8 = 5 ≠ 0) = **2** — ceiling form per §11.2 `[R-GEO-03]`.
- N = 3 · 2 = **6** spatial tiles; P = 4 · 8 = **32** positions per tile; C = **2**.
- Planar addressed-tile count = C · N = 2 · 6 = **12** (§11.2 `[R-GEO-03]`).

**Layer K** — interleaved (layout 1), linearization 1; dims (y, x); channels (a, m), a index 0, m index 1.

- G_y = ⌈5/2⌉ = 2 + 1 = **3**; G_x = ⌈7/3⌉ = 2 + 1 = **3**; N = **9**; P = 2 · 3 = **6**; C = **2**.
- Interleaved addressed-tile count = N = **9** (§11.2 `[R-GEO-03]`).

---

## Q1 — L: addressed-tile count, index-region size, CRC-array start

**Answer.** Addressed-tile count **12**. Region total size **244 bytes**. Segment CRC array starts at region byte offset **240** (occupying [240, 244)).

**Arithmetic.** entry_count = addressed-tile count = 12 (§7.4 `[R-CNT-17]`). Under index_encoding 1 the region is [entry array: entry_count × 20][segment CRC array: ⌈entry_count/2¹⁶⌉ × 4], contiguous, no padding (§15.1 `[R-IDX-01]`); extent_length must equal entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 (`[R-CNT-17]`). 12 × 20 = 240; ⌈12/65,536⌉ = 1; 1 × 4 = 4; 240 + 4 = 244. CRC array begins immediately after the entry array, at byte 240.

**Citations.** §11.2 `[R-GEO-03]`, §7.4 `[R-CNT-17]`, §15.1 `[R-IDX-01]`. **Confidence: high.**

## Q2 — L: disk ordinal of channel t's tile at tile coords (2, 1); entry byte range

**Answer.** Disk tile ordinal **11**; index entry occupies region bytes **[220, 240)**.

**Arithmetic.** Under linearization 1, spatial ordinal s = Σ tᵢ · ∏_{j>i} Gⱼ = t_y · G_x + t_x = 2 · 2 + 1 = 5 (§11.4 `[R-GEO-06]`). Planar disk ordinal = c · N + s with c = index(t) = 1: 1 · 6 + 5 = 11 (`[R-GEO-06]`). Entry k sits at region byte 20 · k (§15.1 `[R-IDX-01]`): 20 · 11 = 220, entries are 20 bytes → [220, 240). (Consistent with Q1: entry 11 is the last, ending exactly where the CRC array begins.)

**Citations.** §11.4 `[R-GEO-06]`, §15.1 `[R-IDX-01]`. **Confidence: high.**

## Q3 — L: which tile carries t at (y, x) = (9, 12), and where in its decoded image

**Answer.** The tile at tile coordinates **(2, 1)**, disk ordinal **11**; the value occupies bytes **[48, 52)** of that tile's 128-byte decoded plane.

**Arithmetic.** (9, 12) is inside extents (9 < 10, 12 < 13; §3.1). Tile coords tᵢ = xᵢ div Tᵢ: t_y = 9 div 4 = 2, t_x = 12 div 8 = 1 (§11.4 `[R-GEO-06]`). Disk ordinal per Q2 = 11. In-tile position uᵢ = xᵢ mod Tᵢ: u_y = 1, u_x = 4; in-tile ordinal = u_y · T_x + u_x = 1 · 8 + 4 = 12 (`[R-GEO-06]`, row-major in-tile order permanent per §11.4). Planar numeric plane: offset of value k = k · Bᶜ = 12 · 4 = 48, size 4 → [48, 52); decoded size P · Bᶜ = 32 · 4 = 128 (§14.2 `[R-SER-02]`).

**Citations.** §11.4 `[R-GEO-06]`, §14.1 `[R-SER-01]`, §14.2 `[R-SER-02]`. **Confidence: high.**

## Q4 — L: complete decoded image of channel m's tile at (2, 1), all real values false

**Answer.** Four bytes: **`E0 E0 FF FF`**.

**Arithmetic.** Planar bool plane: bit-packed LSB-first, value k in bit k mod 8 of byte k div 8, decoded size ⌈P/8⌉ = ⌈32/8⌉ = 4 bytes (§14.3 `[R-SER-03]`, bit numbering §4.4 `[R-ENC-08]`). Tile (2, 1) covers y ∈ [8, 12), x ∈ [8, 16). Real positions need y < 10 and x < 13 → u_y ∈ {0, 1} and u_x ∈ {0..4}; everything else is a padding position (§11.3 `[R-GEO-04]`). Padding positions must carry the channel's fill value — the fill *bit* in a packed plane — and m's fill is 0x01 = true → bit 1 (§14.5 `[R-SER-05]`, §13.2 `[R-TYP-07]`). Real values are false → bit 0. P mod 8 = 0, so there are no §14.3 pad bits; all 32 bits are value bits.

- **Byte 0** (ordinals 0–7 = row u_y = 0): bits 0–4 real/false = 0; bits 5–7 padding (x = 13, 14, 15) = 1 → 0b1110_0000 = **0xE0**.
- **Byte 1** (ordinals 8–15 = row u_y = 1): same pattern as row 0 → **0xE0**.
- **Byte 2** (ordinals 16–23 = row u_y = 2, i.e. y = 10 ≥ 10): all padding → all 1 → **0xFF**.
- **Byte 3** (ordinals 24–31 = row u_y = 3, y = 11): all padding → **0xFF**.

**Citations.** §14.3 `[R-SER-03]`, §14.5 `[R-SER-05]`, §11.3 `[R-GEO-04]`, §4.4 `[R-ENC-08]`, §13.2 `[R-TYP-07]`. **Confidence: high.**

## Q5 — L: t's plane for the same spatial tile — decoded size; bytes at in-tile ordinal 7

**Answer.** Decoded size **128 bytes**; the four bytes at ordinal 7 (plane bytes [28, 32)) are **`00 00 00 80`** — channel t's recorded fill, bit-exact.

**Arithmetic.** Decoded size = P · Bᶜ = 32 · 4 = 128 (§14.2 `[R-SER-02]`). Ordinal 7 → u_y = 7 div 8 = 0, u_x = 7 mod 8 = 7 → x = 8 + 7 = 15 ≥ 13 → padding position (§11.3). A writer MUST encode the channel's fill bytes at every padding position (§14.5 `[R-SER-05]`), and fill is returned/stored bit-exactly (`[R-TYP-04]`, `[R-TYP-06]`) — here `00 00 00 80`, the little-endian float32 pattern 0x80000000 (−0.0), which `[R-TYP-05]` admits as a fill. Offset: 7 · 4 = 28 → [28, 32).

**Citations.** §14.2 `[R-SER-02]`, §14.5 `[R-SER-05]`, §11.3 `[R-GEO-04]`, §12.3 `[R-TYP-04]`/`[R-TYP-05]`, §13.1 `[R-TYP-06]`. **Confidence: high.**

## Q6 — L: ordinal 3 sentinel; read at (y, x) = (5, 9)

**Answer.** Channel **m returns its fill, 0x01 = true**. Channel **t returns the decoded stored value** at in-tile ordinal 9 of the tile at disk ordinal 9 — plane bytes [36, 40) — after the tile's CRC verifies. The sample legitimately mixes fill and decoded channels.

**Arithmetic.** t_y = 5 div 4 = 1, t_x = 9 div 8 = 1 → s = 1 · 2 + 1 = 3 (`[R-GEO-06]`). Channel m (c = 0): disk ordinal 0 · 6 + 3 = **3** → the sentinel entry → reads as fill at every position it carries (§15.2 `[R-IDX-02]`, §13.3 `[R-TYP-08]`), and fill is taken bit-exactly from the channel entry (`[R-TYP-06]`): 0x01 = true (§13.2 `[R-TYP-07]`). Channel t (c = 1): disk ordinal 1 · 6 + 3 = **9** → stored and valid (given) → the reader verifies the chain (crc_of_crc_array → segment CRC → entry → stored bytes, §8.2 `[R-CNT-20]`, §15.4 `[R-IDX-04]`) and returns the decoded value: u = (1, 1), ordinal 1 · 8 + 1 = 9, bytes 9 · 4 = 36 → [36, 40) (`[R-SER-02]`). Mixing is explicitly defined for planar layers (§3.2 `[R-MDL-01]`, §13.3 `[R-TYP-08]`). Fill for m is licensed only because the sentinel was read from a verified chain (`[R-TYP-09]`).

**Citations.** §11.4 `[R-GEO-06]`, §15.2 `[R-IDX-02]`, §13.2–13.3 `[R-TYP-07]`/`[R-TYP-08]`/`[R-TYP-09]`, §13.1 `[R-TYP-06]`, §14.2 `[R-SER-02]`, §8.2 `[R-CNT-20]`, §15.4 `[R-IDX-04]`, §3.2 `[R-MDL-01]`. **Confidence: high.**

## Q7 — Entry: offset = length = all-FF, crc = 01 00 00 00

**Answer.** **reject-tile**; scope is exactly that one addressed tile.

**Reasoning.** The sentinel requires offset = S ∧ length = S ∧ **crc = 0** (§15.2 `[R-IDX-02]`). Here crc = 1 ≠ 0, matching §15.3's second row: "offset = S ∧ length = S ∧ crc ≠ 0 → reject-tile" (`[R-IDX-03]`). Per §2.4's outcome table, only that tile's data is unusable; neighbors and the layer are unaffected (`[R-CNF-07]`/`[R-CNF-08]`). The reader MUST NOT return fill for it — a malformed entry never reads as fill (`[R-TYP-09]`, `[R-CNF-09]`). (This is the erased-flash failure mode §15.2's rationale names: all-0xFF regions are invalid because a sentinel's crc is 0.)

**Citations.** §15.2 `[R-IDX-02]`, §15.3 `[R-IDX-03]`, §2.4 `[R-CNF-07]`–`[R-CNF-09]`, §13.3 `[R-TYP-09]`. **Confidence: high.**

## Q8 — Entry: twenty 0x00 bytes

**Answer.** **reject-tile**; scope is that one tile. It violates two rows of `[R-IDX-03]`'s classification, and emitting it violates writer conformance.

**Reasoning.** Offset = 0, length = 0, crc = 0. Offset ≠ S, so it is not a sentinel (§15.2 `[R-IDX-02]`) — sentinel classification requires the all-ones pattern. As a non-sentinel entry it trips, in §15.3 `[R-IDX-03]`:

1. "length = 0 (non-sentinel) → reject-tile — absence is spelled sentinel; no codec emits zero bytes";
2. "offset < 16 (non-sentinel) → reject-tile — the front block is never payload" (0 < 16).

(The overflow/bounds rows are not violated: 0 + 0 neither overflows nor exceeds F − 64; the >2⁶³−1 row doesn't apply.) Both rows yield the same outcome, reject-tile. The reader MUST NOT return fill for it (`[R-TYP-09]`, `[R-CNF-09]`). On the writer side, a file containing this entry is nonconforming — absence must be spelled as the sentinel (`[R-IDX-02]`, `[R-CNF-05]`). §15.2's rationale confirms this is the designed behavior for a zeroed index region: loudly invalid, never silently all-sparse.

**Citations.** §15.2 `[R-IDX-02]`, §15.3 `[R-IDX-03]`, §13.3 `[R-TYP-09]`, §2.4 `[R-CNF-09]`, §2.3 `[R-CNF-05]`. **Confidence: high.**

## Q9 — K: sample stride, decoded size of every tile, offset of m at in-tile ordinal 4

**Answer.** Sample stride **Q = 3**; every tile's decoded size is **18 bytes**; channel m's value at in-tile ordinal 4 sits at byte offset **14** (byte [14, 15)).

**Arithmetic.** Q = Σ Bᵢ = B_a + B_m = 2 (uint16) + 1 (interleaved bool is a single byte with element size 1 in the arithmetic) = 3 (§14.2 `[R-SER-02]`, §12.1 `[R-TYP-01]`). Decoded size = P · Q = 6 · 3 = 18 — identical for all 9 tiles, because decoded size is a function of declarations alone and every tile has the same logical shape (§14.2 `[R-SER-02]`, §14.3 `[R-SER-07]`, §11.3). m's in-sample offset F_m = Σ Bⱼ over j < 1 = B_a = 2. Offset via `[R-SER-02]`'s formula with sequence index k = 4 · C + 1 = 9: (9 div 2) · 3 + F_{9 mod 2} = 4 · 3 + 2 = **14**.

**Citations.** §14.2 `[R-SER-02]`, §14.3 `[R-SER-07]`, §12.1 `[R-TYP-01]`, §14.1 `[R-SER-01]`. **Confidence: high.**

## Q10 — K: stored tile decodes with 0x02 at a bool byte position

**Answer.**

**(a)** No. Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value; "any other byte makes the file nonconforming" (§14.2 `[R-SER-08]`, §2.3 `[R-CNF-05]`).

**(b)** Nothing. An ordinary reader "is not obligated to screen decoded content, and a reader that does not detect the violation is not thereby nonconforming" (`[R-SER-08]`). The byte belongs to a nonconforming file, for which no acceptance obligation and no defined return value exist; a reader that *does* detect it MAY reject upon detection (§2.4 `[R-CNF-12]`).

**(c)** The verifier is the violation's assigned detector: it MUST treat the byte as a validity error at tile scope (reject-tile) (`[R-SER-08]`), and since a verifier certifies only violation-free files, certification of the file fails (§2.4 `[R-CNF-12]`, §2.3 `[R-CNF-11]`).

**Citations.** §14.2 `[R-SER-08]`, §2.3 `[R-CNF-05]`/`[R-CNF-11]`, §2.4 `[R-CNF-12]`. **Confidence: high.**

## Q11 — entry_count 70,000: segments, CRC array size, region size, verified ranges for entry 69,999

**Answer.** **2 segments**; CRC array **8 bytes**; region total **1,400,008 bytes**. Before using entry 69,999, the reader must CRC-verify, within the region: the **segment CRC array, region bytes [1,400,000, 1,400,008)** (against the layer record's crc_of_crc_array), and **segment 1, region bytes [1,310,720, 1,400,000)** (against the array's second u32) — in that dependency order (fetchable in parallel). Segment 0's bytes [0, 1,310,720) need **not** be verified. Upstream, the chain of trust also requires the trailer CRC (file bytes [F−64, F−4) covering [F−64, F−4)… i.e. trailer bytes [0, 60)) and the directory CRC (final 4 bytes of the region over the preceding dir_length − 4) to have been verified first, since crc_of_crc_array lives in the directory.

**Arithmetic.** Segments: segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, 70,000)) (§15.4 `[R-IDX-04]`). 70,000 = 65,536 + 4,464 → segment 0 = [0, 65,536), segment 1 = [65,536, 70,000), so ⌈70,000/65,536⌉ = 2 segments; array = 2 × 4 = 8 bytes (§15.1). Region = 70,000 × 20 + 8 = 1,400,000 + 8 = 1,400,008 (`[R-CNT-17]`). Entry 69,999 ≥ 65,536 → segment 1. Segment 1's bytes: [65,536 × 20, 70,000 × 20) = [1,310,720, 1,400,000) — 4,464 × 20 = 89,280 bytes. The final partial segment's CRC covers only its actual bytes (`[R-IDX-04]`).

**Citations.** §15.1 `[R-IDX-01]`, §15.4 `[R-IDX-04]`, §7.4 `[R-CNT-17]`, §8.1 `[R-CNT-19]`, §8.2 `[R-CNT-20]`, §4.5 `[R-ENC-10]`. **Confidence: high.**

## Q12 — All-sentinel layer: constant 0xEECB3BB2 without computing?

**Answer.** **entry_count 65,536: yes.** The layer has exactly one segment covering [0, 65,536) — exactly 2¹⁶ entries, i.e. a *full* segment — and all its entries are sentinels, so the writer MAY emit `0xEECB3BB2` without computing it (§15.4 `[R-IDX-05]`; the constant is defined as the CRC-32C of a segment consisting of 2¹⁶ sentinel entries).

**entry_count 65,537: only for segment 0.** There are ⌈65,537/65,536⌉ = 2 segments: segment 0 = [0, 65,536) is full and all-sentinel → constant permitted; segment 1 = [65,536, 65,537) covers 1 entry and is a **final partial segment**, whose "CRC MUST be computed" (`[R-IDX-05]`) — here the CRC-32C of the 20 bytes `FF ×16 00 ×4`, which the spec does not tabulate, so the writer computes it. In both cases crc_of_crc_array over the (4- or 8-byte) array is still required by §7.4, and the constant licenses nothing for readers, whose verification is always byte comparison of computed CRCs (`[R-IDX-05]`).

**Citations.** §15.4 `[R-IDX-04]`/`[R-IDX-05]`, §15.2 `[R-IDX-02]`, §7.4. **Confidence: high** for 65,537; **high** for 65,536, modulo the "full" wording ambiguity filed below.

## Q13 — Reading L's entire extent: samples per channel; padding-return circumstance

**Answer.** **130 samples per channel** (10 × 13 = 130; two channels → 260 values total). The circumstance under which a conforming reader may return the value at a padding position: **none — there is no such circumstance.**

**Reasoning.** The reference array has exactly the layer's extents; padding positions have coordinates outside the extents and "are not part of the reference array" (§3.2 `[R-MDL-01]`). A conforming reader returns exactly the corresponding portion of the reference array (`[R-MDL-02]`), and "a reader MUST NOT return padding positions as samples" (§11.3 `[R-GEO-04]`); §14.5 repeats that a conforming reader never returns padding content (`[R-SER-05]`). §14.5's *Rationale* — that a non-clipping reader would observe fill, a defined value — is non-normative (`[R-CNF-01]`) and grants no license.

**Citations.** §3.2 `[R-MDL-01]`/`[R-MDL-02]`, §11.3 `[R-GEO-04]`, §14.5 `[R-SER-05]`, §2.1 `[R-CNF-01]`. **Confidence: high.**

## Q14 — Interleaved, N = 6, S = 4, A_slab = 1: run partition and offset constraint

**Answer.** One block [0, 6) (interleaved); runs partition it as **run 0 = ordinals [0, 4), run 1 = ordinals [4, 6)** — run r starts at ordinal r · S, and the final run covers fewer than S (§16.2 `[R-SLB-02]`). With ordinal 1 the sentinel and tiles 0, 2, 3 stored (lengths 100, 200, 300), all three are in run 0. The exact constraint (`[R-SLB-03]`):

- **offset₂ = offset₀ + 100** and **offset₃ = offset₂ + 200 = offset₀ + 300** — each stored tile's offset equals the previous *stored* tile's offset plus its length; the sentinel at ordinal 1 occupies no bytes and is transparent to packing.
- offset₀ mod A_slab = offset₀ mod 1 = 0 — **vacuously satisfied for every offset**, so with A_slab = 1 the slab is contiguity-only (§16.2 note). offset₀ itself is otherwise constrained only by general entry validity (offset ≥ 16, offset + length ≤ F − 64, §15.3 `[R-IDX-03]`), not by the slab.
- Run 1 (ordinals 4–5, both unstored here) imposes nothing (`[R-SLB-03]`).

Violations are verifier-detected, reject-layer (`[R-SLB-03]`, §15.3).

**Citations.** §16.2 `[R-SLB-02]`/`[R-SLB-03]`, §15.3 `[R-IDX-03]`. **Confidence: high.**

## Q15 — Single-channel bool layer, P = 10: decoded sizes; byte-identical?

**Answer.** Planar: **⌈10/8⌉ = 2 bytes** (bit-packed LSB-first, §14.3 `[R-SER-03]`). Interleaved: **10 bytes** — each bool value a single byte 0x00/0x01, Q = 1, decoded size P · Q = 10 · 1 = 10 (§14.2 `[R-SER-02]`). The two decoded images are **not byte-identical** — different lengths (2 ≠ 10) and different encodings (packed bits vs. whole bytes). The §14.4 note states this exact contrast explicitly (single-channel *numeric* layers are byte-identical across layouts; bool layers are not), and both forms are valid (`[R-SER-09]`).

**Citations.** §14.2 `[R-SER-02]`, §14.3 `[R-SER-03]`, §14.4 `[R-SER-09]` and its note. **Confidence: high.**

---

## Findings

### AMBIGUITY

1. **§15.4 `[R-IDX-05]` — "full" segment is not explicitly defined.** The license reads "writers … MAY emit this constant for any **full** segment whose entries are all sentinels" and separately "a final partial segment's CRC MUST be computed." Readings permitted: (a) *full* = a segment covering exactly 2¹⁶ entries, final or not; (b) *full* = any non-final segment (all of which cover 2¹⁶ entries by construction). The readings diverge only for a final segment covering exactly 2¹⁶ entries — precisely Q12's entry_count = 65,536 case. I picked (a): the immediately preceding sentence defines the constant as "the CRC-32C of a segment consisting of 2¹⁶ sentinel entries," which such a final segment is, and "full"/"partial" read most naturally as entry-count qualities, not position qualities; under (b) the license would arbitrarily forbid a mathematically correct shortcut. A one-word clarification ("a segment covering exactly 2¹⁶ entries") would remove the fork.

### CONTRADICTION

None found in the sections exercised by this quiz (§§2–9, 11–16).

### OBSERVATION

1. **§15.3 `[R-IDX-03]`, length = 0 row — unresolvable forward reference in the justification.** The clause "no codec emits zero bytes" depends on §17's codec boundary contract, which is *[Reserved]*. The normative outcome (reject-tile) is fully decidable without it, but an implementer cannot yet confirm from the text that every codec's encoded output is guaranteed nonempty. Reportable as a forward reference per the charter; not a defect in the rule itself.
2. **Quiz answers are codec-invariant despite §17 being reserved.** The quiz omitted L's and K's codec/filter fields, but every question concerns decoded tile images, geometry, and the tile index; §14 defines the decoded image as the pipeline's *output*, §15's region is always raw (§7.1 `[R-CNT-25]`), so no answer above depends on §17. Useful reassurance for staging cleanroom implementations before Batch 7.
3. **Padding positions vs. pad bits (Q4).** §14.3's "pad bits" exist only when P mod 8 ≠ 0 and are distinct from §11.3's "padding positions"; a plane can have many padding positions and zero pad bits (L's P = 32). Both get the fill bit under `[R-SER-05]`, so the distinction is content-invisible in packed planes, but the near-identical terminology invites implementer confusion; a terminology cross-note in §14.3 would help.
4. **Q6's premise "stored and valid" was interpreted to include the verified chain.** Returning fill for the sentinel at ordinal 3 is licensed only by a sentinel read from a verified index chain (`[R-TYP-09]`, `[R-IDX-04]`, `[R-CNT-20]`); the answer assumes the trailer, directory, crc_of_crc_array, and segment CRC all verify. Not a spec defect — noted so the archived answer isn't quoted without that predicate.
5. **§14.2's interleaved offset formula is sequence-indexed.** The table gives offsets per value-sequence index k; the per-(channel, sample-ordinal) form u · Q + F_c used in practice (Q9) is an algebraic consequence (set k = u · C + c). A worked identity in §14.2 would spare each implementer the derivation.
