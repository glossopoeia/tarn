# Cleanroom Writer Transcript — TARN Array-Model Serialization (§11–§16)

Source of truth: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full. Nothing else was consulted. Sections §17 (Codecs and Filters), §18–§24, and the Appendices are marked *[Reserved]* in the text I read; where a charter task touches them I say so explicitly. All arithmetic follows §11.2/§11.4 as written; all multi-byte values are little-endian per §4.1 `[R-ENC-01]`.

Charter tasks 1 and 2 describe **independent hypothetical states** of layer K (task 1 has tile (2, 2) carrying real data; task 2 stores only disk ordinals 0 and 5). I treat them as separate files.

---

## 1. Layer K — geometry, strides, and the (2, 2) edge tile

**Declarations.** Interleaved (layout = 1, §7.4/§14.1 `[R-SER-06]`), linearization = 1 (row-major, the only writer-legal value, §11.4 `[R-GEO-05]`). Dimensions in declared order: `y` (E₀ = 5, T₀ = 2) then `x` (E₁ = 7, T₁ = 3). Channels in declared order: `a` (uint16, element size 2, §12.1 `[R-TYP-01]`; fill field bytes `FF FF`, i.e. the LE encoding of 0xFFFF, §13.1 `[R-TYP-06]`) then `m` (bool, element size 1; fill byte `0x00` = false, the only legal encodings being 0x00/0x01, §13.2 `[R-TYP-07]`).

**Derived quantities** (§11.2 `[R-GEO-03]`, §14.2 `[R-SER-02]`):

| Quantity | Value | Derivation |
|---|---|---|
| Grid counts (G_y, G_x) | (3, 3) | ⌈5/2⌉ = 2+1 = 3; ⌈7/3⌉ = 2+1 = 3 (Eᵢ/Tᵢ plus 1 when Eᵢ mod Tᵢ ≠ 0) |
| Spatial-tile count N | 9 | ∏ Gᵢ = 3·3 |
| Addressed-tile count | 9 | interleaved ⇒ N (planar would be C·N) |
| P (sample positions per tile) | 6 | ∏ Tᵢ = 2·3 |
| Sample stride Q | 3 | Σ Bᵢ = 2 (uint16) + 1 (interleaved bool is a single byte, §14.2) |
| In-sample offsets | F_a = 0, F_m = 2 | Fᶜ = Σ Bⱼ, j < c |
| Value count V per tile | 12 | P·C = 6·2 `[R-SER-01]` |

**Every tile's decoded size: 18 bytes** (P·Q = 6·3), for all nine tiles — disk ordinals 0 through 8. Decoded size is a function of declarations alone, identical for every tile of the layer (§11.3 uniform shape `[R-GEO-04]`; §14.3 `[R-SER-07]`), edge tiles included.

**The edge tile at tile coordinates (t_y, t_x) = (2, 2).** Spatial ordinal s = t₀·G₁ + t₁ = 2·3 + 2 = **8**; interleaved, so disk ordinal is also 8 (§11.4 `[R-GEO-06]`). It covers y ∈ {4, 5} and x ∈ {6, 7, 8}. Layer extents bound real coordinates to y < 5, x < 7 (§3.1), so exactly one position is real — (y, x) = (4, 6) — and the other five are **padding positions** (coordinate ≥ Eᵢ on some axis, §11.3 `[R-GEO-04]`):

| In-tile ordinal k (= u_y·3 + u_x, row-major, §11.4) | (u_y, u_x) | (y, x) | Status |
|---|---|---|---|
| 0 | (0, 0) | (4, 6) | **real** |
| 1 | (0, 1) | (4, 7) | padding (x ≥ 7) |
| 2 | (0, 2) | (4, 8) | padding (x ≥ 7) |
| 3 | (1, 0) | (5, 6) | padding (y ≥ 5) |
| 4 | (1, 1) | (5, 7) | padding (both) |
| 5 | (1, 2) | (5, 8) | padding (both) |

**Complete decoded image (18 bytes).** Value sequence is sample-major: value k is channel (k mod 2) at in-tile ordinal k div 2 `[R-SER-01]`; sample k occupies bytes [3k, 3k+3): `a` at 3k (u16 LE), `m` at 3k+2 `[R-SER-02]`. Real sample: a = 0x0102 → bytes `02 01` `[R-ENC-01]`; m = true → `0x01` (§14.2; only 0x00/0x01 are writer-legal, `[R-SER-08]`). Every padding position MUST encode each channel's fill (§14.5 `[R-SER-05]`).

| Byte | Hex | Sample / channel | Justification |
|---|---|---|---|
| 0 | `02` | ordinal 0 (real, (4,6)), `a` low byte | LE encoding of 0x0102 `[R-ENC-01]`, `[R-SER-02]` |
| 1 | `01` | ordinal 0, `a` high byte | same |
| 2 | `01` | ordinal 0, `m` | true = 0x01, §14.2 `[R-SER-08]` |
| 3 | `FF` | ordinal 1 (padding, (4,7)), `a` low | recorded fill bytes `FF FF` `[R-SER-05]`, `[R-TYP-06]` |
| 4 | `FF` | ordinal 1, `a` high | same |
| 5 | `00` | ordinal 1, `m` | recorded fill byte 0x00 (false) `[R-SER-05]`, `[R-TYP-07]` |
| 6–8 | `FF FF 00` | ordinal 2 (padding, (4,8)) | same two rules |
| 9–11 | `FF FF 00` | ordinal 3 (padding, (5,6)) | same |
| 12–14 | `FF FF 00` | ordinal 4 (padding, (5,7)) | same |
| 15–17 | `FF FF 00` | ordinal 5 (padding, (5,8)) | same |

Full image: `02 01 01 FF FF 00 FF FF 00 FF FF 00 FF FF 00 FF FF 00`

There are **no pad bits** anywhere in this layer: pad bits exist only in packed planar bool planes when P mod 8 ≠ 0 (§14.3 `[R-SER-03]`); interleaved layers never pack. A reader never returns the padding positions `[R-GEO-04]`; a verifier MUST check their content (violation: reject-tile) `[R-SER-05]`, and any interleaved bool byte other than 0x00/0x01 is likewise verifier-detected at tile scope `[R-SER-08]`.

Note this 18-byte image is the input to the codec pipeline (§14 preamble); the **stored** bytes depend on §17, which is reserved — see Findings.

---

## 2. Layer K's tile-index region (ordinals 0 and 5 stored; all else sentinel)

entry_count = addressed-tile count = **9** (`[R-CNT-17]`, §11.2). Under index_encoding 1 (§15.1 `[R-IDX-01]`) the region is, contiguously with no internal padding:

- entry array: 9 × 20 = 180 bytes
- segment CRC array: ⌈9 / 2¹⁶⌉ × 4 = 4 bytes

**Region size = 184 bytes**, and the layer record's extent_length MUST equal 184 `[R-CNT-17]`. The region is always raw — never compressed (§7.1 `[R-CNT-25]`). Entries are in disk-ordinal order, entry k at region byte 20k `[R-IDX-01]`. Entry layout: offset u64 at +0, length u64 at +8, crc u32 at +16 (§15.1), all LE.

**Complete byte layout** (region-relative offsets; `XX XX XX XX` marks a CRC value I am told not to compute):

| Region bytes | Entry | Content (hex) |
|---|---|---|
| [0, 20) | 0 — **stored**, offset 4096 (0x1000), length 40 (0x28) | `00 10 00 00 00 00 00 00` · `28 00 00 00 00 00 00 00` · `XX XX XX XX` = CRC-32C over the 40 stored bytes at file offsets [4096, 4136) (§8.1, §15.1) |
| [20, 40) | 1 — sentinel | `FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF 00 00 00 00` `[R-IDX-02]` |
| [40, 60) | 2 — sentinel | same 20 bytes |
| [60, 80) | 3 — sentinel | same 20 bytes |
| [80, 100) | 4 — sentinel | same 20 bytes |
| [100, 120) | 5 — **stored**, offset 4136 (0x1028), length 44 (0x2C) | `28 10 00 00 00 00 00 00` · `2C 00 00 00 00 00 00 00` · `XX XX XX XX` = CRC-32C over the 44 stored bytes at file offsets [4136, 4180) |
| [120, 140) | 6 — sentinel | same 20 bytes as entry 1 |
| [140, 160) | 7 — sentinel | same 20 bytes |
| [160, 180) | 8 — sentinel | same 20 bytes |
| [180, 184) | — | segment CRC array: one u32 LE |

**Coverage of each checksum** (§8.1 `[R-CNT-19]`, §15.4 `[R-IDX-04]`):

- Entry 0's crc covers the tile's stored (post-codec) bytes, file offsets [4096, 4136). Entry 5's crc covers [4136, 4180). Sentinel crcs are the constant 0.
- Segment 0 — the only segment, covering entries [0, min(2¹⁶, 9)) = [0, 9) — has its u32 at region [180, 184), computed over region bytes **[0, 180)** exactly as stored (a final partial segment's CRC covers only its actual bytes).
- The layer record's crc_of_crc_array (§7.4) covers the segment CRC array itself: region bytes **[180, 184)**.

**Constant a writer may use.** `0xEECB3BB2` is the CRC-32C of a segment of exactly 2¹⁶ sentinel entries; a writer MAY emit it, uncomputed, **only for a full segment whose entries are all sentinels**; a final partial segment's CRC MUST be computed `[R-IDX-05]`. Here the single segment is partial (9 entries) *and* contains two non-sentinel entries — either alone disqualifies the constant — so the segment CRC MUST be computed. (Consequence: any layer with entry_count < 65,536 can never use the constant.)

The entry fields as given are individually valid under §15.3: offsets ≥ 16, lengths ≠ 0, within 2⁶³−1, and (assuming F large enough) offset + length ≤ F − 64 `[R-IDX-03]`.

---

## 3. Planar bool plane, P = 32, fill = true, 22 padding positions

Decoded tile image (§14.3 `[R-SER-03]`): the P = 32 values bit-packed LSB-first — value k at bit k mod 8 of byte k div 8 (§4.4 `[R-ENC-08]`), 0 = false, 1 = true — decoded size ⌈32/8⌉ = **4 bytes**.

**Padding positions.** The 22 positions whose coordinates fall outside the layer's extents (§11.3 `[R-GEO-04]`) are serialized like any other position, and the writer MUST encode at each one the plane's channel's **fill bit** (§14.5 `[R-SER-05]`: "the fill bit in a packed plane"). Fill is true (fill byte 0x01, §13.2 `[R-TYP-07]`), so each of the 22 padding positions' bits is **1**, at the bit slot its in-tile ordinal dictates. The 10 real positions carry their actual sample bits. Which of the 32 ordinals are padding is determined purely by geometry (which coordinates exceed which extent), not by anything in §14.

**Pad bits.** Pad bits exist **only when P mod 8 ≠ 0** — they are the final byte's bit positions P mod 8 through 7 (§14.3). Here P mod 8 = 0, so **this tile has no pad bits**: all 32 bits of all 4 bytes are value bits. When pad bits do exist (e.g. P = 30 would leave bits 6–7 of byte 3), every pad bit MUST carry the plane's channel's fill bit `[R-SER-05]` — with fill true they would all be 1, matching §14.3's worked example (`55 FD`).

Padding-position and pad-bit content bind the **writer**; a reader's decode never fails over packed-plane content `[R-SER-03]`, a reader never returns padding positions `[R-GEO-04]`, and the verifier checks the content (violation: reject-tile) `[R-SER-05]`.

---

## 4. Byte-for-byte agreement vs. legitimate divergence (§11–§16)

Given identical declarations and identical logical content (the same reference array, §3.2 `[R-MDL-01]`/`[R-MDL-02]`), writer conformance is explicitly semantic: "two conforming writers given identical input MAY produce different conforming files" (§2.3, `[R-CNF-05]` note). What §11–§16 pin down byte-for-byte, and where they license divergence:

**MUST agree byte-for-byte:**

1. **Every stored tile's decoded image**, in full — value order `[R-SER-01]`, byte layout and offsets `[R-SER-02]`, packed-plane bit assignment `[R-SER-03]`, padding-position and pad-bit content `[R-SER-05]`, permanent row-major in-tile ordinal (§11.4 `[R-GEO-06]`), little-endian encoding `[R-ENC-01]`, bit-pattern preservation `[R-TYP-04]`. For layer K: any tile both writers store has the identical 18-byte image; §1's edge-tile image is the unique conforming image for that content.
2. **Bool encodings**: 0x00/0x01 interleaved `[R-SER-08]`, 0/1 bits packed `[R-SER-03]`.
3. **Sentinel entries**: exactly `FF ×16 00 ×4` `[R-IDX-02]`.
4. **Index structure**: entry order = disk-ordinal order and entry position 20k `[R-IDX-01]`; region size = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 `[R-CNT-17]`; segment partition and what each CRC covers `[R-IDX-04]`.
5. **Geometry-derived counts**: grid counts, N, P, addressed-tile count, hence the entry_count value `[R-GEO-03]`, `[R-CNT-17]`.
6. **Fill fields** byte-exact per declaration `[R-TYP-06]`, `[R-TYP-07]`.
7. **All declared padding bytes are zero** wherever gaps exist `[R-CNT-03]`, `[R-SLB-01]`, `[R-SLB-03]`.

**MAY legitimately diverge (catalog of axes):**

- **D1 — Stored-tile placement and order.** With no alignment/slab declaration, "stored tiles MAY occupy any non-overlapping byte positions, in any order" (§16 `[R-SLB-05]`). This cascades: entry offset fields differ → entry bytes differ → segment CRCs differ → crc_of_crc_array differs. Placement freedom alone makes whole-index byte agreement essentially accidental.
- **D2 — Declaring alignment or slab at all, and the values.** "A layer MAY declare alignment A" (§16.1 `[R-SLB-01]`, any power of two ≥ 512); "A layer MAY declare a slab run length S ≥ 1 with slab alignment A_slab" (§16.2 `[R-SLB-02]`); mutually exclusive `[R-CNT-16]`.
- **D3 — Which aligned slot.** `[R-SLB-01]` constrains only offset mod A = 0, not which multiple of A; gap sizes vary between conforming writers.
- **D4 — Run placement under a slab.** `[R-SLB-03]` binds within-run contiguity/packing and each run's first stored tile's alignment; the absolute A_slab-aligned start of each run is unpinned (see Findings, AMBIGUITY 1, on inter-run adjacency).
- **D5 — Storedness of all-fill tiles.** A sentinel tile and a stored tile whose every value equals fill denote the same reference array (§3.1, §13.3 `[R-TYP-08]`, `[R-MDL-01]`); nothing in §11–§16 mandates minimal storage, and §13's sparse-writing note frames sentinel emission as a writer technique, not an obligation. Two writers may therefore disagree on which entries are sentinels while encoding identical logical content.
- **D6 — Codec/filter selection and encoded payload bytes.** The layer record carries codec and filter fields (§7.4), and the stored bytes are the codec pipeline's output (§14 preamble, §17). §17 is reserved: nothing in the text I read fixes any codec value's semantics or determinism, so even two writers declaring the same codec cannot be shown to agree on stored bytes — and entry length and crc fields inherit that divergence. (Reportable forward reference; see Findings.)
- **D7 — Layout choice for a single-channel numeric layer** (not K): interleaved and planar produce byte-identical tile images and identical disk ordinals; only the layout byte differs (§14.4 note). A single-channel *bool* layer diverges in image bytes too — both valid (same note).
- **D8 — Position of the index region among the generation's appended structures.** §15 pins the region's internal bytes but not where it sits; §9.2 step 2 permits appending payloads and index regions "in any order" (Part I, cited for completeness).
- **Non-axis, for completeness:** computing a full all-sentinel segment's CRC vs. writing the constant `0xEECB3BB2` produces the same bytes `[R-IDX-05]` — an implementation shortcut, not a divergence.

---

## 5. Slab honesty: K with S = 3, A_slab = 4096

Declaration validity first: S = 3 requires A = 0 (per-tile alignment and slab are mutually exclusive, `[R-CNT-16]`), and A_slab = 4096 is a power of two in [1, 2⁶²] (§7.4, §16.2 `[R-SLB-02]`).

**Run structure.** Interleaved ⇒ one contiguous block of disk ordinals [0, 9); runs partition it as [0, 3), [3, 6), [6, 9) — run r starts at ordinal 3r; here N = 9 = 3·3 so all runs are full (the final run *may* be shorter, not here) `[R-SLB-02]`. Runs never span channel blocks — vacuous for interleaved.

**Binding invariants on tile placement** (`[R-SLB-03]`, verified per §15.3's "alignment or slab invariant violated → *verifier*: reject-layer"):

1. Within each run, stored tiles are contiguous and packed in ordinal order: each stored tile's offset = previous stored tile's offset + its length.
2. Sentinels are transparent: they occupy no bytes and do not break packing.
3. Each run's **first stored tile** has offset mod 4096 = 0.
4. A run with no stored tiles imposes nothing.
5. Gaps A_slab creates are declared padding — zero bytes (`[R-SLB-03]`, §5.2, `[R-CNT-03]`).
6. General placement law still applies: no overlaps within the live committed state `[R-CNT-13]`.

Applied to task 2's storedness ({0, 5} stored): run 0's first (only) stored tile is ordinal 0 → its offset must be ≡ 0 mod 4096 (4096 qualifies); run 1's first (only) stored tile is ordinal 5 → its offset must be ≡ 0 mod 4096 — **task 2's placement at 4136 would violate this** (4136 mod 4096 = 40); run 2 is empty → nothing binds. So the task-2 file and the S = 3 declaration are mutually exclusive: under the declaration, tile 5 goes at, e.g., 8192, with the [4136, 8192) gap zero declared padding.

**An updater that supersedes one stored tile** of this layer MUST, per `[R-SLB-04]`, either **re-establish the invariants for every affected run** or **clear the declaration in the new generation**; carrying the stale declaration forward is a validity error at layer scope. Mechanics under the append-only commit model (§9.1 `[R-LIF-01]`, §9.2 — committed bytes are immutable, so the replacement payload is appended, never overwritten in place):

- If the affected run's only stored tile is the superseded one (e.g. ordinal 5 in run 1): append the new payload at any 4096-aligned offset — contiguity is trivial for a single stored tile — and the run's invariants hold again.
- If the run has other stored tiles: their old offsets are immutable and the replacement lands elsewhere (typically with a different length), so packing against the old neighbors cannot survive. The updater must re-append **all** of that run's stored tiles as a fresh contiguous, ordinal-packed, 4096-aligned sequence (the old extents become superseded dead space, §5.2 `[R-CNT-21]`), or
- Clear the declaration: emit the new generation's layer record with S = 0 — and then A_slab MUST be 0 (§7.4, `[R-CNT-23]`).

Either way the commit appends a new complete tile-index region for the layer (with entry 5 pointing at the new extent and its new length/CRC) and a new complete directory, per §9.2 — and the updater is a reader of the file first (§2.3 `[R-CNF-06]`, `[R-CNF-11]`). The same `[R-SLB-04]` obligation triggers on extent growth of a slab-declared layer.

---

## Findings

### AMBIGUITY

1. **§16.2 `[R-SLB-03]` — inter-run placement.** The enumerated invariants bind only *within* a run (contiguity, ordinal packing, first-stored-tile alignment); nothing in the requirement sentence orders run r+1 after run r or bounds the distance between runs. But the clause "the gaps A_slab creates between runs are declared padding" presupposes runs laid consecutively with only sub-A_slab alignment slack between them — an arbitrary inter-run gap is not a gap "A_slab creates", yet under `[R-CNT-02]`/`[R-CNT-03]` it would have to be zero declared padding of some class. Readings: (i) only the enumerated per-run invariants bind, runs may sit at any aligned offsets in any order; (ii) runs must additionally be consecutive in run order. I implemented the writer to emit reading (ii) — consecutive runs, each start rounded up to the next A_slab boundary — because that layout conforms under both readings; I verified task 5's placement conclusions using only reading (i)'s invariants, which both readings share. A verifier author must know which reading governs.
2. **§16.2 `[R-SLB-04]` — scope of "every affected run".** "Affected" is undefined. Readings: (a) the run(s) whose stored-tile set or byte layout the commit changes (minimally the superseded tile's run); (b) every run of the layer. I picked (a): `[R-SLB-03]` states "a run with no stored tiles imposes nothing" and the invariants are per-run, so a commit that leaves a run's entries and extents untouched cannot invalidate it. Under reading (b) an updater would have to re-verify (though not re-place) all runs, which is a verifier's job per §15.3.

### CONTRADICTION

none — I specifically cross-checked §14.2's stride table against `[R-SER-01]`'s value order, §15.1's region formula against `[R-CNT-17]`, §14.5's fill-byte padding against §13.1/§13.2's fill encoding and `[R-SER-08]`'s 0x00/0x01 domain, and §16's declared-padding language against §5.2/`[R-CNT-03]`; all consistent.

### OBSERVATION

1. **Unresolvable forward reference to §17 (reserved).** A writer cannot get from the decoded tile image (§14) to stored bytes: the codec and filter field *values'* semantics (§7.4 says only "codec u16, §17, 0 invalid") are undefined in the present text — there is not even an identifiable "no compression" codec value. Tasks 1–2 were answerable only because the charter supplies stored lengths (40, 44) as givens; the entry crc fields, which cover stored bytes (§8.1), are likewise uncomputable from this text. Everything up to and including the decoded image, and everything about the index's structure, is complete without §17.
2. **The sentinel-segment constant is dead weight for small layers.** `0xEECB3BB2` is licensed only for a *full* (exactly 2¹⁶-entry) all-sentinel segment `[R-IDX-05]`; any layer with entry_count < 65,536 has a single partial segment and must always compute — layer K (entry_count 9) can never use it.
3. **Certifying §14 requires codec implementation.** `[R-SER-05]` and `[R-SER-08]` assign padding/bool-content checks to the verifier at tile scope, which requires decoding payloads; §3.3's decode-free-verifier note is scoped to Part I only. Verifier implementers should plan the codec dependency.
4. **Stored length vs decoded size are unrelated in §11–§16.** Lengths 40/44 against decoded size 18 are legal: `[R-SER-07]`'s exact-size check applies to the *decoded* payload, and §15.3 bounds stored lengths only against the file. Nothing in these sections forbids expansion under the (reserved) codec pipeline.
5. **Decoded images are fully deterministic; index bytes are not.** For layer K every byte of every stored tile's decoded image is pinned by declarations plus the reference array (`[R-SER-01/02/05]`, `[R-TYP-04]`) — the content-addressing property §14.5's rationale claims — but placement freedom `[R-SLB-05]` means two writers' index entry bytes, segment CRCs, and crc_of_crc_array values will differ in practice; only sentinel entries and the region's structure are byte-pinned.
