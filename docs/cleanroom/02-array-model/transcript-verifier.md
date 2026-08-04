# TARN Verifier Certification over the Array Model (§§11–16) — Fresh-Context Trace

Source of truth: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full. Nothing else was consulted. All citations are to that document.

## 0. Standing and prerequisites

A conforming verifier is a reader that additionally checks every file-level requirement — including those ordinary readers are exempted from — and certifies conformance; it inherits every reader obligation [§2.3, R-CNF-11]. A verifier certifies only violation-free files: outcome classes (reject-file / reject-layer / reject-tile / ignore-record, §2.4, R-CNF-07) describe the *blast radius for readers*, never degrees of file conformance; for a nonconforming file no acceptance obligation exists [§2.4, R-CNF-12]. So for every check below, "outcome" means: the reader-scope classification the verifier reports; certification fails on any hit.

The array-model checks presuppose the strictly ordered chain of trust: trailer → directory → (per layer) crc_of_crc_array → segment CRC array → index segment → index entry → stored tile [§8.2, R-CNT-20]. No field may be acted on before the checksum covering it is verified [§4.5, R-ENC-10; §4.2, R-ENC-05]. I take trailer and directory verification (Part I, §§6–7) as already passed and do not re-derive them, except where §§11–16 checks hang off them.

---

## 1. The complete check list

### 1.1 Layer-declaration validity (geometry, types, fill — §§11–13, §7.4)

| # | Check | Failure outcome / scope | IDs |
|---|---|---|---|
| D1 | rank d ≥ 1; every tile extent Tᵢ ≥ 1; channel count C ≥ 1 | reject-layer | R-GEO-01 |
| D2 | Dimension extent Eᵢ = 0 is *valid* (grid count 0, zero addressed tiles, empty reference array) — acceptance obligation, not a failure | — (must accept) | R-GEO-02 |
| D3 | Every geometry product — Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, P = ∏Tᵢ, addressed count (N or C·N), decoded sizes, index-region size — ≤ 2⁶³−1; no wrapped/truncated value acted on | reject-layer | R-GEO-03, R-ENC-04 |
| D4 | linearization = 1 (0, 2–3, 4–0x7FFF reserved, ≥0x8000 experimental: all invalid here) | reject-layer | R-GEO-05 |
| D5 | layout ∈ {1 interleaved, 2 planar} | reject-layer | R-SER-06, R-CNT-23 |
| D6 | Every channel type ∈ {1..13}; no size/semantics inferred for others | reject-layer | R-TYP-01, R-TYP-03, R-CNT-23 |
| D7 | Each fill field's byte length equals its type's element size | reject-layer | R-CNT-23, R-TYP-06 |
| D8 | bool fill byte ∈ {0x00, 0x01} (numeric fills: every bit pattern valid) | reject-layer | R-TYP-07, R-TYP-05 |
| D9 | Names (layer, dimensions, channels): well-formed UTF-8, non-empty, ≤255 bytes, no U+0000–U+001F; dimension/channel names unique in layer; layer name unique in file | reject-layer, except duplicate *layer* name → reject-file | R-ENC-11, R-ENC-12, R-ENC-15 |
| D10 | index_encoding = 1 (raw-segmented); any other value including experimental range invalid | reject-layer | §7.4 table, R-CNT-23, §15.1 |
| D11 | A = 0 or a power of two with 512 ≤ A ≤ 2⁶²; S = 0 or 1 ≤ S ≤ 2⁶³−1; A_slab = 0 iff S = 0, else power of two 1 ≤ A_slab ≤ 2⁶² | reject-layer | R-SLB-01, R-CNT-23 |
| D12 | Not both A ≠ 0 and S ≠ 0 (mutually exclusive) | reject-layer | R-CNT-16 |
| D13 | crc_of_crc_array = 0 when entry_count = 0; nonzero with entry_count = 0 invalid | reject-layer | R-CNT-23 |
| D14 | No layer rejected for its layout × channel-type combination — acceptance obligation | — (must accept) | R-SER-09 |

### 1.2 Index cross-checks (§7.4)

| # | Check | Failure outcome / scope | IDs |
|---|---|---|---|
| X1 | entry_count equals the geometry-derived addressed-tile count: N (interleaved) or C·N (planar) | reject-layer | R-CNT-17, R-GEO-03, R-CNT-20 |
| X2 | Under index_encoding 1: extent_length = entry_count·20 + ⌈entry_count/2¹⁶⌉·4, and 0 when entry_count = 0 (extent slot (0,0) for a zero-tile layer) | reject-layer | R-CNT-17, §7.4 |

### 1.3 Segment-CRC verification chain (§15.4, §8.1–8.2)

Order is mandatory: each link verified before acting on anything it covers [R-ENC-10, R-CNT-20].

| # | Check | Covers | Failure outcome | IDs |
|---|---|---|---|---|
| C1 | crc_of_crc_array (field in the layer record, itself under the directory CRC) matches CRC-32C computed over the segment CRC array — the final ⌈entry_count/2¹⁶⌉·4 bytes of the index region | segment CRC array bytes as stored | reject-layer | R-IDX-04, §8.1 |
| C2 | Each segment-CRC array u32 s matches CRC-32C over entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)) — bytes as stored; a final partial segment's CRC covers only its actual bytes and MUST be computed (the all-sentinel constant 0xEECB3BB2 applies only to full segments, and equality with it licenses nothing — verification is comparison of *computed* CRCs) | that segment's entry bytes | reject-layer | R-IDX-04, R-IDX-05 |
| C3 | Each non-sentinel entry's crc matches CRC-32C over the stored tile's bytes [offset, offset+length) exactly as stored (encoded — codec-independent) | the stored tile extent | reject-tile | §8.1, R-CNT-20, §15.3 |

### 1.4 Entry validity — every §15.3 row (per-entry outcomes govern notwithstanding the general owning-scope mapping of R-ENC-03/R-ENC-04) [R-IDX-03]

S below denotes the sentinel value 2⁶⁴−1; F the live committed file length.

| # | Entry state | Outcome | IDs |
|---|---|---|---|
| E1 | offset = S ∧ length = S ∧ crc = 0 | **valid sentinel** — reads as fill | R-IDX-02, R-TYP-08 |
| E2 | offset = S ∧ length = S ∧ crc ≠ 0 | reject-tile | R-IDX-03 |
| E3 | exactly one of offset/length = S | reject-tile | R-IDX-03 |
| E4 | length = 0, non-sentinel (absence is spelled sentinel; no codec emits zero bytes) | reject-tile | R-IDX-03 |
| E5 | offset < 16, non-sentinel (front block is never payload) | reject-tile | R-IDX-03 |
| E6 | offset > 2⁶³−1 or length > 2⁶³−1, non-sentinel | reject-tile | R-IDX-03, R-ENC-03 |
| E7 | offset + length overflows, or offset + length > F − 64, non-sentinel | reject-tile | R-IDX-03, R-ENC-04 |
| E8 | stored bytes fail the entry's crc | reject-tile | R-IDX-03, §8.2/R-CNT-20 |
| E9 | *verifier row:* two stored extents of the same layer overlap, or a stored extent overlaps its own layer's index region or sub-record extents | reject-layer | R-IDX-03, R-CNT-13 |
| E10 | *verifier row:* a stored extent overlaps any structure outside its own layer | reject-file | R-IDX-03, R-CNT-13 |
| E11 | *verifier row:* alignment or slab invariant violated (§16) | reject-layer | R-IDX-03, R-SLB-01, R-SLB-03 |

### 1.5 Slab and alignment invariants (§16)

| # | Check | Failure outcome / scope | IDs |
|---|---|---|---|
| S1 | Neither A nor S declared → no layout promise; nothing to check | — | R-SLB-05 |
| S2 | A declared: every stored tile's offset mod A = 0 | reject-layer (verifier row E11) | R-SLB-01 |
| S3 | S declared: runs partition each disk-ordinal block ([0,N) interleaved; [c·N,(c+1)·N) per channel planar; runs never span channel blocks); within each run, stored tiles contiguous and packed in ordinal order (each offset = previous offset + previous length; sentinels transparent, they break nothing); the run's first stored tile's offset mod A_slab = 0; a run with no stored tiles imposes nothing | reject-layer (verifier row E11) | R-SLB-02, R-SLB-03 |
| S4 | The gaps A or A_slab creates are **declared padding**: zero bytes | **reject-file** (verifier check; distinct scope from S2/S3) | R-CNT-03, §5.2 |
| S5 | A commit that superseded a stored tile in, or grew, a slab-declared layer must have re-established the invariants or cleared the declaration; a stale declaration carried forward is invalid — observable only as S3 violations | reject-layer | R-SLB-04 |

### 1.6 Decoded-content obligations (§14) — require running the codec pipeline (§17)

| # | Check | Failure outcome / scope | IDs |
|---|---|---|---|
| V1 | Decoded payload's byte length equals the declaration-derived decoded size exactly: planar numeric P·Bᶜ; interleaved P·Q (bool bytes count 1 in Q); planar bool ⌈P/8⌉ | reject-tile | R-SER-02, R-SER-03, R-SER-07 |
| V2 | **Padding content** (verifier MUST check; readers exempt): at every padding position (§11.3), each carried channel encodes its recorded fill — fill bytes for numeric, fill byte for interleaved bool, fill *bit* in a packed plane; every pad bit of a packed plane carries the channel's fill bit | reject-tile | R-SER-05, R-GEO-04, R-TYP-06 |
| V3 | **Interleaved bool bytes** (assigned detector: the verifier): every interleaved bool value byte ∈ {0x00, 0x01} | reject-tile (validity error at tile scope; a reader that misses it is not thereby nonconforming) | R-SER-08 |
| V4 | Packed-plane decode never *fails* over content — every value-region bit pattern decodes; only V2 constrains it, on the writer side | — (must not reject on decode) | R-SER-03 |

### 1.7 Verdict

Any hit in 1.1–1.6 → the file is nonconforming; no certificate. The verifier reports each finding at its assigned scope and MAY treat the whole file as rejected [R-CNF-12]. It never returns rejected data as valid and never substitutes fill for a rejected tile [R-CNF-09, R-TYP-09].

---

## 2. Worked trace — layer L

**Declarations.** Planar (layout = 2, valid per R-SER-06); linearization = 1 (valid per R-GEO-05). Dimensions in declared order: y (E=10, T=4), x (E=13, T=8). Channels in declared order: m = channel 0 (bool, type 1, fill `01` = true — valid per R-TYP-07, length 1 = element size per R-CNT-23) and t = channel 1 (float32, type 12, fill bytes `00 00 00 80` — little-endian bit pattern 0x80000000, i.e. −0.0; any bit pattern valid per R-TYP-05, preserved bit-exactly per R-TYP-04/R-TYP-06). A = S = A_slab = 0 assumed (none declared): consistent per R-CNT-23/R-CNT-16, no §16 promises [R-SLB-05].

**Grid arithmetic [R-GEO-03].** G_y = ⌈10/4⌉ = 2 + 1 = 3; G_x = ⌈13/8⌉ = 1 + 1 = 2. N = 3·2 = 6 spatial tiles; P = 4·8 = 32 positions per tile; C = 2.

**Addressed-tile count = C·N = 12** (planar) [§11.2, R-GEO-03]. So entry_count must equal 12 [R-CNT-17].

**Index region [§15.1, R-IDX-01; R-CNT-17].** Size = 12·20 + ⌈12/2¹⁶⌉·4 = 240 + 4 = **244 bytes**, which extent_length must equal exactly. Internal layout (region-relative; absolute = extent_offset I + these):

- **[0, 240)** — entry array: entry k (disk ordinal k) at [20k, 20k+20), each 20 bytes: offset u64, length u64, crc u32 [§15.1].
- **[240, 244)** — segment CRC array: one u32 (segment 0, partial: covers entries 0–11 only), computed — the all-sentinel constant does not apply [R-IDX-05].

**Disk ordinals [R-GEO-06]:** k = c·N + s, s = t_y·G_x + t_x (x, last-declared, varies fastest):

| k | ch | s | (t_y,t_x) | y range | x range | state | edge axes | decoded size | region bytes |
|---|---|---|---|---|---|---|---|---|---|
| 0 | m | 0 | (0,0) | 0–3 | 0–7 | stored | — | 4 | [0,20) |
| 1 | m | 1 | (0,1) | 0–3 | 8–15 | stored | **x** | 4 | [20,40) |
| 2 | m | 2 | (1,0) | 4–7 | 0–7 | stored | — | 4 | [40,60) |
| 3 | m | 3 | (1,1) | 4–7 | 8–15 | **sentinel** | **x** | — | [60,80) |
| 4 | m | 4 | (2,0) | 8–11 | 0–7 | stored | **y** | 4 | [80,100) |
| 5 | m | 5 | (2,1) | 8–11 | 8–15 | stored | **y and x** | 4 | [100,120) |
| 6 | t | 0 | (0,0) | 0–3 | 0–7 | stored | — | 128 | [120,140) |
| 7 | t | 1 | (0,1) | 0–3 | 8–15 | stored | **x** | 128 | [140,160) |
| 8 | t | 2 | (1,0) | 4–7 | 0–7 | stored | — | 128 | [160,180) |
| 9 | t | 3 | (1,1) | 4–7 | 8–15 | stored | **x** | 128 | [180,200) |
| 10 | t | 4 | (2,0) | 8–11 | 0–7 | stored | **y** | 128 | [200,220) |
| 11 | t | 5 | (2,1) | 8–11 | 8–15 | stored | **y and x** | 128 | [220,240) |

Edge tiles are those where Gᵢ·Tᵢ > Eᵢ intersects the tile: x-padding exists at t_x = 1 (x = 13,14,15 ≥ E_x = 13); y-padding at t_y = 2 (y = 10,11 ≥ E_y = 10) [§11.3, R-GEO-04].

**Sentinel entries: exactly one — disk ordinal 3 (channel m, spatial ordinal 3), region bytes [60, 80)**, which must be the 20 bytes `FF ×16 00 ×4` [R-IDX-02]. It is an *unstored edge tile*: it reads as fill (m = true) at every real position of its tile [R-TYP-08], carries no stored bytes, and so has no padding-content check; padding positions are never returned regardless [R-GEO-04].

Decoded sizes: m planes ⌈32/8⌉ = 4 bytes each [R-SER-03]; t planes 32·4 = 128 bytes each [R-SER-02]. All products comfortably within 2⁶³−1 [R-ENC-04].

**Every check I run on layer L**, with CRC coverage (I = the layer record's extent_offset; F = live committed length):

1. *Prerequisite chain:* trailer CRC at [F−4, F) over [F−64, F−4); directory CRC (final 4 bytes of the directory region) over the preceding dir_length−4 bytes, which include this layer record and its crc_of_crc_array field [§8.1, R-CNT-20].
2. Declaration checks D1–D14: all pass as computed above (rank 2, tile extents 4 and 8, C = 2, types 1 and 12 core, fill lengths 1 and 4, bool fill 0x01, layout 2, linearization 1, index_encoding 1, names m/t and y/x unique, layer name unique file-wide). The codec field cannot be validated from the drafted text — see Findings.
3. X1: entry_count = 12 = C·N — else reject-layer [R-CNT-17]. X2: extent_length = 244 — else reject-layer [R-CNT-17].
4. C1: CRC-32C over file bytes [I+240, I+244) (the segment CRC array) = crc_of_crc_array — else reject-layer [R-IDX-04].
5. C2: CRC-32C over file bytes [I, I+240) (entries 0–11 as stored) = the u32 at [I+240, I+244) — else reject-layer [R-IDX-04]; computed, never matched against 0xEECB3BB2 [R-IDX-05].
6. E1–E7 over all 12 entries: entry 3 exactly `FF ×16 00 ×4`; the 11 non-sentinel entries each with length ≠ 0, offset ≥ 16, offset and length ≤ 2⁶³−1, non-overflowing offset+length ≤ F−64 — failures reject-tile [R-IDX-03].
7. C3/E8: for each of the 11 stored tiles, CRC-32C over file bytes [offset_k, offset_k+length_k) = entry k's crc — else reject-tile. These cover *encoded* bytes as stored, so they run without any codec knowledge [§8.1].
8. E9/E10: the 11 stored extents pairwise disjoint, disjoint from the index region [I, I+244) and from any sub-record extents of L (reject-layer); disjoint from every structure outside L (reject-file) [R-CNT-13, R-IDX-03].
9. E11/S1: no alignment or slab declared — vacuous [R-SLB-05]; A_slab = 0 with S = 0 confirmed [R-CNT-23].
10. V1: each stored m tile decodes to exactly 4 bytes; each t tile to exactly 128 — else reject-tile [R-SER-07]. (Requires §17's pipeline — see Findings.)
11. V2 padding content [R-SER-05], reject-tile on violation, on the seven stored edge tiles (k = 1, 4, 5, 7, 9, 10, 11); in-tile ordinal = u_y·8 + u_x [R-GEO-06]:
    - k=1 (m, x-edge): bits at ordinals {5,6,7, 13,14,15, 21,22,23, 29,30,31} = fill bit 1.
    - k=4 (m, y-edge): bits at ordinals 16–31 = 1, i.e. decoded bytes 2 and 3 = `FF FF`.
    - k=5 (m, corner): see §3 below.
    - k=7, 9 (t, x-edge): 12 padding values at ordinals {5,6,7,13,14,15,21,22,23,29,30,31}, each occupying decoded bytes [4·ord, 4·ord+4) = `00 00 00 80`.
    - k=10 (t, y-edge): ordinals 16–31, decoded bytes [64, 128) = sixteen copies of `00 00 00 80`.
    - k=11 (t, corner): ordinals {5,6,7,13,14,15} ∪ {16..31} = 22 values, each `00 00 00 80`.
    - No pad bits exist anywhere: P mod 8 = 0 [§14.3].
12. V3: not applicable — no interleaved bool channel (planar layer) [R-SER-08].

---

## 3. The edge tile of channel m at tile coordinates (2, 1)

That is spatial ordinal s = 2·2 + 1 = 5, disk ordinal 5, stored per the trace. It covers y ∈ [8,12), x ∈ [8,16); real positions are y ∈ {8,9} (E_y = 10) and x ∈ {8..12} (E_x = 13): 10 real positions, 22 padding positions [§11.3]. Decoded image: packed bool plane, ⌈32/8⌉ = 4 bytes, value k at bit k mod 8 of byte k div 8, LSB-first [R-SER-03, §4.4]; in-tile ordinal u_y·8 + u_x [R-GEO-06]. Real ordinals: u_y ∈ {0,1} × u_x ∈ {0..4} → {0–4, 8–12}. Padding ordinals: {5–7, 13–15, 16–31}. P mod 8 = 0, so the tile has no pad bits — all 32 bits are value bits.

With every real m value false (bit 0) and the recorded fill true (padding bits must be the fill bit 1 [R-SER-05]):

- byte 0 (ordinals 0–7): bits 0–4 = 0, bits 5–7 = 1 → **0xE0**
- byte 1 (ordinals 8–15): bits 0–4 = 0, bits 5–7 = 1 → **0xE0**
- byte 2 (ordinals 16–23): all padding → **0xFF**
- byte 3 (ordinals 24–31): all padding → **0xFF**

**The decoded image must be `E0 E0 FF FF`.** Precisely: conformance fixes only the 22 padding bits (bits 5–7 of bytes 0–1 and all of bytes 2–3) [R-SER-05]; the 10 real bits are fixed by the stated data, not by conformance — a 1 in a real bit is a different reference array [R-MDL-01], not a violation, and a verifier cannot flag it.

**If a padding bit is wrong:** it is a validity error at tile scope — I record reject-tile for disk ordinal 5 [R-SER-05], the file is nonconforming, and certification fails [R-CNF-12]; I MAY escalate to rejecting the whole file [R-CNF-12]. I MUST NOT report that tile's data as valid [R-CNF-09] and MUST NOT substitute fill for it — rejection is never satisfied by returning fill [R-TYP-09]. No heuristic repair [R-CNF-04]. I continue scanning to report remaining findings; the certificate is already forfeit.

---

## 4. What a verifier cannot establish from §§11–16 as drafted

1. **Anything requiring decode.** §17 (Codecs and Filters) is reserved. The codec u16's value set is §17's subject (§7.4: "codec | u16 | §17 (0 invalid)"), so the drafted text assigns *no* valid codec value at all; and without the pipeline, the decoded tile image is unobtainable. Consequently checks V1 [R-SER-07], V2 [R-SER-05], and V3 [R-SER-08] — including item 11 of my trace and the `E0 E0 FF FF` verdict of §3 — are unexecutable forward references. Filter *values* (1 = none, 2 = byte-shuffle) are given in §7.4, but byte-shuffle's semantics are §17's.
2. **Limits.** §21's limits table is reserved: the verifier cannot decide whether a file stays within the minimum guarantees readers must honor [R-CNF-10, R-CNF-03], nor consult the consolidated error register [R-CNF-04].
3. **User-metadata content.** §18 reserved: a layer's user-metadata sub-record can be framed [R-CNT-18], its extent CRC checked [§8.1], its encoding byte read [R-CNT-25] — but document validity and key uniqueness are undecidable.
4. **Registry semantics.** §10 reserved (experimental ranges referenced by §11.4, §12.2, §15.1/§7.4). Harmless for format major 1: every unassigned value already rejects at layer scope [R-GEO-05, R-TYP-03, R-CNT-23].
5. **Behavioral conformance.** File conformance is a pure predicate on bytes [R-CNF-02]; reader/writer/updater conformance (e.g. R-MDL-02, R-TYP-08, R-GEO-04's "never return padding") is not certifiable from a file.
6. **Undecidable in principle, by the text's own admission:** whether a recorded fill was deliberate or a default (§13.1 Note); whether a slab declaration was freshly re-established or merely never disturbed — [R-SLB-04] is observable only through [R-SLB-01]/[R-SLB-03] invariants, and a "stale" declaration whose invariants hold is indistinguishable from a deliberate one (and conforming); real sample values versus author intent (a wrong real bit in §3 is invisible); tampering (checksums do not authenticate, §4.5 Note); axis orientation (§11.4 Note — deferred to §18).

---

## Findings

**AMBIGUITY**

1. **§15.3 [R-IDX-03] verifier rows E9/E10 vs rows E4–E7 — do malformed entries define "stored extents"?** The table does not order its rows, so an entry that is reject-tile-invalid (e.g. offset+length > F−64) either (a) still contributes an extent to the overlap checks, or (b) is excluded, only entries passing rows E1–E8 participating. I picked (b): §3.1 ties storedness to the entry, but overlap arithmetic on an extent already outside the file is meaningless, and §9.7(c)'s coverage claims can only be built from well-formed references. Either reading forfeits certification; the choice affects only which scope (tile vs layer/file) gets reported.
2. **§7.4 codec field with §17 reserved.** [R-CNT-23] makes "a reserved or unassigned … codec … value" a layer-scope validity error, and the value set is §17's subject; with §17 undrafted, the strict reading is that *every* codec value is unassigned and no layer can pass. I rejected the strict reading as an artifact of draft state and treated the check as unexecutable-pending-§17 — but either way no certificate can issue today, because check 1.6 is blocked (see also Observation 1).

**CONTRADICTION**

1. **§4.5 [R-ENC-10 context] vs §8.1 [R-CNT-19].** §4.5 states checksum fields are "verified by comparison, covered by no further checksum"; §8.1's coverage map states the per-segment CRC array is "itself covered by the layer record's crc_of_crc_array", and crc_of_crc_array (a checksum field) lies inside the directory bytes covered by the directory CRC. Both universals cannot hold: segment CRCs and crc_of_crc_array are checksum fields covered by a further checksum. Additionally §8.1 calls the front signature block the "sole exception" while its own table leaves the trailer CRC, directory CRC, and user-metadata-extent CRC fields covered by nothing — conflicting with §4.5's two-exception list. The table itself is unambiguous and is what I implemented (checks C1–C3); the prose quantifiers need reconciling.

**OBSERVATION**

1. **All decoded-content verification hangs on reserved §17.** Checks [R-SER-05], [R-SER-07], [R-SER-08] — the verifier-MUST half of §14 — cannot run without the codec pipeline; every CRC in the chain (§8.1) covers bytes *as stored*, so integrity verification is fully executable today while content verification is fully blocked. Worth stating in §17 or §14 which conformance class a verifier facing an unimplemented-but-assigned codec falls into (§9.7(d) answers the analogous question for unverifiable structures; §14 does not).
2. **Three distinct "padding" mechanisms with three failure scopes.** Padding *positions* (§11.3, content per R-SER-05: reject-tile), pad *bits* of packed planes (§14.3, also R-SER-05: reject-tile), and declared padding *between structures* (§5.2, R-CNT-03: reject-file — including §16's alignment gaps, while the §16 placement invariants themselves are reject-layer per R-SLB-01/R-SLB-03). Implementers should not merge these; in the trace, tile m(2,1) has 22 padding-position bits and zero pad bits.
3. **Notation collisions.** S = sentinel value (§15.3) vs S = slab run length (§7.4, §16.2); F = committed file length (§6.2, §15.3) vs Fᶜ = in-sample channel byte offset (§14.2). Locally disambiguated, but a hazard for exactly this kind of cross-section procedure.
4. **Verification cost is edge-proportional and whole-index.** [R-SER-05] obliges decoding every stored edge tile (decode cost on the layer's whole edge surface even when integrity already passed), and E9/E10 overlap checks require whole-directory extent knowledge (§7.2's own note) — both deliberately verifier-only; correct, but disproportionately expensive relative to every other check, which is streamable per entry.
5. **Declared padding is checksum-uncovered.** No checksum in §8.1's map covers padding bytes; their only guard is the verifier's zero test [R-CNT-03]. Corruption confined to padding is invisible to ordinary readers by design — worth a line in reserved §22.
6. **[R-SLB-04] adds no independently observable check.** A stale slab declaration is detectable only as [R-SLB-01]/[R-SLB-03] invariant failures; a verifier can cite R-SLB-04 in a report but can never distinguish "stale but coincidentally intact" from "re-established", and need not.
