# TARN Specification — Acceptance Review Transcript

**Reviewer role:** fresh-context implementer. **Universe:** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (3,171 lines), read in full, nothing else. No repository files, no git, no web, no prior knowledge used.

**Method note.** Beyond reading, I performed one class of independent work: I implemented CRC-32C exactly as `[R-ENC-09]` describes (polynomial 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and recomputed the three constants the document states, plus Appendix A's trailer. This is arithmetic over values quoted in the text, not external input. All three reproduce exactly:

| Constant | Spec says | I computed |
|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | `0xE3069283` / `83 92 06 E3` | `0xE3069283` ✓ |
| CRC-32C(zero bytes) (§4.5) | `0x00000000` | `0x00000000` ✓ |
| Appendix A trailer CRC over [0,60) | `0xE00938D2` / `D2 38 09 E0` | `0xE00938D2` ✓ |
| CRC of 2¹⁶ sentinel entries (`[R-IDX-05]`) | `0xEECB3BB2` | `0xEECB3BB2` ✓ |

I also re-derived every worked example in §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §17.3, and §20.3; all check out. And I verified §21's mechanical counts (see OBSERVATION 7).

---

## The two given layers

**Layer L** — planar (`layout = 2`, §14.1), linearization 1, rank d = 2.
Dimensions in declared order: y (E₀ = 9, T₀ = 4), x (E₁ = 5, T₁ = 4).
Channels in declared order: m (index 0, bool, element size 1, fill `00`), v (index 1, float32, element size 4, fill `00 00 80 3F`). C = 2.

Grid arithmetic (`[R-GEO-03]`, §11.2 — ceiling division stated as E/T plus 1 when E mod T ≠ 0):
- G₀ = ⌈9/4⌉ = 2 + 1 = **3**
- G₁ = ⌈5/4⌉ = 1 + 1 = **2**
- N = ∏Gᵢ = 3 · 2 = **6** spatial tiles
- P = ∏Tᵢ = 4 · 4 = **16** sample positions per tile

**Layer K** — interleaved (`layout = 1`). Channels: a (index 0, uint16, B⁰ = 2, fill `FF FF`), m (index 1, bool, B¹ = 1 for the interleaved byte, `[R-TYP-01]` element-size column and §14.2's "1 for bool"). C = 2.

---

## Q1 — The smallest conforming file

**Answer: 128 bytes. Bytes [16, 20) are the entire directory region** — a record sequence of zero bytes followed by its 4-byte terminal CRC-32C, which for zero covered bytes is `0x00000000`, stored `00 00 00 00`.

Derivation, not just citation. From `[R-CNT-06]`: F mod 64 = 0; the trailer occupies the final 64 bytes; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64. Substituting the minima: 16 + 4 = 20 ≤ F − 64 → F ≥ 84 → the next multiple of 64 is **128**. This matches §5.1's example, `[R-CNT-01]`, Appendix A, Appendix B ("Smallest conforming file | 128 bytes"), and register row F8.

Why [16, 20) is *necessarily* the directory rather than merely conventionally so: the only declared-padding classes in `[R-CNT-02]`/§5.2 are alignment gaps of aligned or slab-declared layers and each generation's pre-trailer pad. A file with no layers has no alignment gaps, so a directory placed at, say, offset 20 would leave [16, 20) claimed by no coverage class — not a conforming file (F9). Hence dir_offset = 16 and dir_length = 4 are forced. The four bytes are the region's terminal CRC (`[R-CNT-11]`, §8.1's coverage map), covering dir_length − 4 = 0 bytes.

**Citations:** §5.1 `[R-CNT-01]`, §5.2 `[R-CNT-02]`, §6.2 `[R-CNT-06]`, §7.1 `[R-CNT-11]`, §4.5 `[R-ENC-09]`, §21.2 F8/F9, Appendix A, Appendix B.
**Confidence: high.**

---

## Q2 — Trailer says committed_file_length = 128; file on disk is 192 bytes

**Answer: reject-file, and the reader MUST NOT scan backward to find the earlier trailer.**

A reader takes the transport-authoritative size (192) and reads the final 64 bytes, [128, 192) — §19.1 step 2 anchors the open at F − 64 where F is the *physical/transport* size, and `[R-CNT-10]` forbids substituting committed_file_length for the transport size. Two sub-cases, both reject-file:

- If [128, 192) parses as a trailer declaring committed_file_length = 128, the gate "committed_file_length equals the file size … and is a multiple of 64" in `[R-CNT-06]` fails → **reject-file**, register row **F23**.
- If [128, 192) is not a valid trailer (the real trailer sits at [64, 128) and 64 bytes were appended after the commit), the default read path is trailer-at-end-or-fail: `[R-LIF-05]` — "a reader that finds no valid trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT scan backward" → **reject-file**, register row **F40** ("Bytes were appended past a completed commit and never truncated").

Adjacent obligations the same bytes trigger for other actors: a writer opening for append MUST establish F by validating the final 64 bytes and, on failure, MUST NOT append (`[R-LIF-04]`); locating the earlier state is the deliberate recovery scan of §9.6 (`[R-LIF-06]`), explicitly "not a reader behavior", and its output MUST be re-verified as a whole file. Even when validation *succeeds*, `[R-LIF-04]` requires a writer whose physical file exceeds F to truncate to F or overwrite from it, so this state never survives a completed commit.

**Citations:** `[R-CNT-06]`, `[R-CNT-10]`, `[R-LIF-05]`, `[R-LIF-04]`, `[R-LIF-06]`, §19.1 step 2 `[R-RDR-01]`, F23, F40.
**Confidence: high.**

---

## Q3 — Layer L: addressed-tile count, index region size, CRC-array offset

Planar ⇒ addressed-tile count = C · N (`[R-GEO-03]`).

- **Addressed-tile count = 2 · 6 = 12.** This is also the required `entry_count` (`[R-CNT-17]`, §7.4; mismatch is L20).
- **Index region total size** under index_encoding 1 (`[R-CNT-17]`, `[R-IDX-01]`):
 entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 = 12 × 20 + ⌈12/65536⌉ × 4 = 240 + 1 × 4 = **244 bytes.**
 This is exactly the value the layer record's `extent_length` MUST carry (L21 otherwise).
- **Segment CRC array begins at region byte 240** (immediately after the entry array, "contiguously … with no padding anywhere inside the region", §15.1), occupying region bytes [240, 244) — one segment, since ⌈12/65536⌉ = 1.

**Citations:** §11.2 `[R-GEO-03]`, §7.4 `[R-CNT-17]`, §15.1 `[R-IDX-01]`, §15.4 `[R-IDX-04]`.
**Confidence: high.**

---

## Q4 — Layer L: disk ordinal of v at tile coordinates (2, 1), and its entry's byte range

Channel v is declared second, so its **channel index c = 1** (§3.1: "a channel's index is its 0-based position in that order").

Spatial tile ordinal under linearization 1 (`[R-GEO-06]`): s = Σᵢ tᵢ · ∏_{j>i} Gⱼ = t₀·G₁ + t₁ = 2 · 2 + 1 = **5**.

Disk ordinal, planar (`[R-GEO-06]`, channel-major): c · N + s = 1 · 6 + 5 = **11**.

Entry position (`[R-IDX-01]`: "The entry for the tile with disk ordinal k is the k-th entry, at region byte 20·k"): 20 × 11 = 220 → **region bytes [220, 240)**, i.e. absolute [extent_offset + 220, extent_offset + 240).

Consistency check: 11 is the last of 12 entries, and 240 is where the CRC array begins (Q3) — the entry array ends exactly there. ✓

**Citations:** §3.1 (channel index), §11.4 `[R-GEO-06]`, §15.1 `[R-IDX-01]`.
**Confidence: high.**

---

## Q5 — Layer L: the complete decoded image of m's tile at tile coordinates (2, 1)

**Answer: `01 00` (two bytes).**

m is a **bool channel in a planar layer**, so §14.3 governs: the decoded tile image is the tile's P values bit-packed LSB-first, value k at bit k mod 8 of byte k div 8, decoded size ⌈P/8⌉ = ⌈16/8⌉ = **2 bytes** (`[R-SER-03]`; §14.2's table explicitly does not apply — packing is exclusive to planar bool planes).

Which positions are real. Tile (2, 1) covers y ∈ [2·4, 3·4) = [8, 12) and x ∈ [1·4, 2·4) = [4, 8). The extents are E_y = 9, E_x = 5, so the only coordinate inside the reference array is (y, x) = (8, 4); the other 15 are **padding positions** (§11.3, `[R-GEO-04]` — coordinates ≥ Eᵢ along an axis).

In-tile ordinals (`[R-GEO-06]`, permanent row-major in-tile ordinal Σᵢ uᵢ · ∏_{j>i} Tⱼ = u₀·4 + u₁):

| k | u = (k div 4, k mod 4) | coordinate (8+u₀, 4+u₁) | status | bit |
|---|---|---|---|---|
| 0 | (0,0) | (8, 4) | **real** | 1 (given: true) |
| 1–3 | (0,1..3) | (8, 5..7) | x ≥ 5 → padding | fill bit |
| 4–7 | (1,0..3) | (9, 4..7) | y ≥ 9 → padding | fill bit |
| 8–15 | (2..3, ·) | (10..11, ·) | y ≥ 9 → padding | fill bit |

Byte-by-byte justification:

- **Byte 0 = `0x01`.** Bit 0 holds value k = 0, the sole real sample, true → 1 (§14.3: "0 = false and 1 = true"). Bits 1–7 hold k = 1…7, all padding positions, which `[R-SER-05]` requires to carry "the fill bit in a packed plane". m's recorded fill byte is `0x00` = false (`[R-TYP-07]`, §13.2), so the fill bit is 0. 0b0000_0001 = `0x01`.
- **Byte 1 = `0x00`.** Bits 0–7 hold k = 8…15, all padding positions → fill bit 0 each. There are **no pad bits** here: pad bits exist only when P mod 8 ≠ 0 (§14.3), and P = 16 ≡ 0 (mod 8), so every bit of byte 1 encodes a real value slot, all of them padding positions.

Two things this image is *not*: it is not affected by the layer's filter declaration in any case, since a packed boolean plane has shuffle stride s = 1 and byte-shuffle is the identity there (`[R-COD-10]`); and if the layer declares codec 1, `[R-COD-04]` additionally forces the index entry's `length` to equal 2.

**Citations:** §14.3 `[R-SER-03]`, §14.5 `[R-SER-05]`, §11.3 `[R-GEO-04]`, §13.2 `[R-TYP-07]`, §11.4 `[R-GEO-06]`, §4.4 `[R-ENC-08]`, `[R-COD-10]`, `[R-COD-04]`.
**Confidence: high.** (§14.5's own worked example — extents (5,5), tiles (4,4), edge tile (1,1), one real position and 15 padding — is the numeric twin of this case in the numeric-channel form.)

---

## Q6 — Layer K: sample stride, and byte offset of m at in-tile ordinal 3

**Sample stride Q = ΣBᵢ = 2 (uint16 `a`) + 1 (interleaved bool `m`) = 3 bytes** (§14.2 `[R-SER-02]`: "Q = Σ Bᵢ over all channels (the sample stride)"; bool counts as element size 1 in interleaved layouts).

**Offset of m at in-tile ordinal 3 = 11.**

Two equivalent derivations, both from `[R-SER-02]`:
- Closed form given at the end of §14.2's example — "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ": F¹ = Σ_{j<1} Bⱼ = B⁰ = 2, so 3 · 3 + 2 = **11**.
- Table form: value index k = u · C + c = 3 · 2 + 1 = 7; offset = (k div C) · Q + F_{k mod C} = (7 div 2) · 3 + F¹ = 3 · 3 + 2 = **11**.

The value occupies exactly one byte, [11, 12), and must be `0x00` or `0x01` (`[R-SER-08]`). Decoded size of the whole tile would be P · Q (§14.2), P depending on K's unstated tile extents.

**Citations:** §14.2 `[R-SER-02]`, `[R-SER-01]` (interleaved sample-major order), `[R-SER-08]`.
**Confidence: high.**

---

## Q7 — Classify two index entries

**(a) offset = length = `FF FF FF FF FF FF FF FF`, crc = 0** → the **sentinel entry**: valid, not a violation. The tile is addressed but not stored; every sample position it carries reads as the channel's fill value, bit-exactly and with no payload I/O (`[R-IDX-02]`, §15.3 row 1 "valid sentinel — reads as fill", `[R-TYP-08]`, §19.4 step 4, §21.6 row 1). It is exactly the 20 bytes `FF ×16 00 ×4` (Appendix B). Note `[R-IDX-02]` exempts these fields from `[R-ENC-03]`'s value domain and `[R-ENC-04]`'s sum rule — the all-ones pattern is a reserved pattern, not an offset.

**(b) twenty `0x00` bytes** → offset = 0, length = 0, crc = 0. This is **not** a sentinel (the sentinel is all-ones, not all-zeros), so it is a non-sentinel entry and trips two §15.3 rows independently: **length = 0 (non-sentinel) → reject-tile** (register T10 — "absence is spelled sentinel; no codec emits zero bytes") and **offset < 16 (non-sentinel) → reject-tile** (register T8 — "the front block is never payload"). Outcome: **reject-tile**. Critically, `[R-TYP-09]` forbids returning fill here: "A reader MUST NOT return fill for a tile whose entry is malformed"; a rejected tile's read reports failure (`[R-CNF-09]`). §15.2's Rationale names this case by design: a zeroed index region "parses under this rule as offset 0 / length 0 — loudly invalid — rather than as a valid all-sparse index silently returning fill".

One precision worth stating, because it changes what an implementation actually reports: entry classification happens at §19.4 **step 4**, *after* step 3's index chain. In the realistic scenario that produces (b) — a zeroed or hole-punched region — the segment CRC array is zeroed too, and CRC-32C over the zeroed entry bytes is not zero (for a single 20-byte zero entry it is `0xBCC5563E`; for the whole 244-byte region of Q3's layer, `0x139D31CD`), so `[R-IDX-04]`'s segment check fails first and the outcome the user sees is **reject-layer** (L37). The entry-level classification is reject-tile; the chain-level failure that precedes it is reject-layer.

**Citations:** §15.2 `[R-IDX-02]`, §15.3 `[R-IDX-03]` (rows for length = 0 and offset < 16), T8, T10, `[R-TYP-09]`, `[R-CNF-09]`, §19.4 `[R-RDR-04]` steps 3–4, `[R-IDX-04]`/L37, Appendix B.
**Confidence: high.**

---

## Q8 — Unsorted user-metadata object members

- **Is the file conforming? No.** `[R-MTA-05]`: "Writers MUST serialize object members in ascending order of their keys' UTF-8 bytes"; violating it makes the file nonconforming (`[R-CNF-05]`). §21.6's row states it outright: "The file is nonconforming".
- **What does a reader do? Processes the document unchanged.** `[R-MTA-05]`: "unsorted members do not make a document unreadable … readers process the document unchanged", and "Readers MUST NOT depend on member order for meaning". This is *not* an ignore-record condition — it is absent from §21.5. §21.6's preamble goes further: "A reader that treats any of them as a failure is the nonconforming party."
- **What does a verifier do? MUST report it, and MUST NOT certify the file.** `[R-MTA-05]`: "a verifier MUST report it". Certification is gated by §2.4/`[R-CNF-12]`: "a verifier certifies only violation-free files", and Appendix H's verifier checklist repeats it.

There is a gap here that a verifier implementer hits immediately: the condition has **no register row and no outcome class**. It appears only in §21.6, the table of "conditions that are not violations", while §21.1 claims the register's completeness is normative and `[R-CNF-07]` claims every detectable violation carries exactly one of the four outcomes. See CONTRADICTION 2. `[R-VEC-02]` survives this only because such a file damages no structure — the vector records `conforming: false` with no damaged-scope rows.

**Citations:** `[R-MTA-05]`, §21.6 (unsorted-members row), `[R-CNF-05]`, `[R-CNF-12]`, §2.4, Appendix H, and for the gap: §21.1, `[R-CNF-07]`.
**Confidence: high** on all three behaviors; **medium** on what a verifier *records* (undetermined — see findings).

---

## Q9 — A user-metadata document containing `1e400`

**Outcome: ignore-record, with a SHOULD-report. The whole document is dropped; nothing else is affected — and the outcome is ignore-record at *every* containing scope.**

`[R-MTA-04]`'s "Finite numbers only" restriction: "A document is unreadable if it contains a number whose binary64 interpretation is not finite — which covers a magnitude that overflows on conversion, `1e400` being the ordinary case". Unreadable ⇒ ignore-record with the report `[R-CNT-25]` asks for. Register row **R7** ("A user-metadata document contains a non-finite number, in any form"), detector: reader, detection point: **extent use** (§19.2's fourth tier).

On scope, precisely as asked: the record's *owning* scope is the file for a top-level record and the layer for a sub-record (§18.1), but the **quarantine overrides the owning-scope mapping**: "the outcome of every failure to read its document is ignore-record whatever the scope" (`[R-MTA-02]`), and `[R-CNT-25]` says this holds "notwithstanding the owning-scope mapping of `[R-CNF-08]`". So a layer's metadata document containing `1e400` does **not** reject the layer, and a file-scope one does not reject the file. "Application metadata never invalidates the structural data it annotates."

Note the granularity: it is the **document** that is dropped, not just the offending key. Contrast `[R-MTA-07]`, where a *standardized* key of the wrong shape or scope is ignored individually "rather than rejecting the document". Non-finiteness is a document-level rule under `[R-MTA-04]`.

Also note: the *file* remains nonconforming if a writer emitted it (writers SHOULD NOT emit numbers binary64 cannot represent exactly — and a non-finite one violates the document's own rules), but no reader-visible scope is rejected.

**Citations:** §18.2 `[R-MTA-04]`, §7.1 `[R-CNT-25]`, §18.1 `[R-MTA-02]`, `[R-CNF-08]`, §19.2 `[R-RDR-02]`, §21.5 R7.
**Confidence: high.**

---

## Q10 — A layer record declaring codec `0x8001`

**Outcome: reject-layer. Scope: layer. Detected at layer access.**

0x8001 ≥ 0x8000, so it is in the codec space's **experimental range** (§10.2's table, §17.2). `[R-COD-03]`: "Writers MUST NOT emit a codec value other than 1 through 4; a reader MUST treat any other value — 0, every reserved value, and the experimental range included — as a validity error at layer scope (`[R-CNT-23]`)." `[R-EXT-03]` confirms the general rule: an experimental value "treats it as its space's rules require: a validity error at the owning scope for the value sets of … §17.2".

Consequences of reject-layer (§2.4's table): the layer's data and metadata are unusable; **all other layers are unaffected**; the reader MAY still list the file's layers including this one's name. Detection is due no later than first access to the layer — §19.3 `[R-RDR-03]` lists "the value sets of … §17.2" among the checks that must precede first access, and all of them are "decidable from the resident directory and F: layer access performs no fetch". Register row **L44**.

Also relevant: a writer emitting this makes the file nonconforming (`[R-CNF-05]`, `[R-EXT-03]`: experimental values MUST NOT appear "in released software or published data", and reserved values MUST NOT be emitted at all). And `[R-COD-11]`: for a conforming reader the "cannot execute this codec" position "arises only at a reserved or experimental value, every assigned codec and filter being core".

**Citations:** §10.2 `[R-EXT-02]`, §10.3 `[R-EXT-03]`, §17.2 `[R-COD-03]`, `[R-CNT-23]`, §19.3 `[R-RDR-03]`, §2.4, L44, `[R-COD-11]`.
**Confidence: high.**

---

## Q11 — Unknown record type `0x0003` with MU = 1

0x0003 sits in the record-type space's **reserved** range 0x0003–0x7FFF (§10.2), unassigned in format major 1 (§7.3: "All other type values are unassigned").

- **At file scope (top-level record in the directory): reject-file.** `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file; MU = 0 → ignore-record." Register row **F38**, detector reader, detected at **open** (§19.1 step 4 applies "the MUST_UNDERSTAND gate for unknown top-level types").
- **As a layer sub-record: reject-layer — explicitly never reject-file.** `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never reject-file — and with MU = 0 is ignore-record." Register row **L24**, detected at **layer access**.

Two riders. (i) `[R-EXT-03]` routes reserved-range values to exactly these MU-bit outcomes, and forbids emitting a reserved value at all before assignment — so this file is nonconforming today, though the same bytes could become conforming under a later minor that registers 0x0003. (ii) For tooling rather than readers: §20.4's table makes an unknown MU = 1 record "Retain byte-identical" and blocks modification of the scope it governs, and `[R-WRT-06]` makes a compactor refuse outright (Q14). The interaction of that table with `[R-CNT-15]` at file scope is AMBIGUITY 2 below.

**Citations:** §10.2 `[R-EXT-02]`, §7.3, `[R-CNT-15]`, `[R-CNT-18]`, `[R-EXT-03]`, §19.1 `[R-RDR-01]` step 4, F38, L24.
**Confidence: high.**

---

## Q12 — entry_count = 70,000

All arithmetic from `[R-CNT-17]`, `[R-IDX-01]`, `[R-IDX-04]`. Region offsets below are relative to the layer record's `extent_offset`; absolute file offsets add it.

- **Segments:** ⌈70,000 / 2¹⁶⌉ = ⌈70,000 / 65,536⌉ = **2** (segment 0 full at 65,536 entries; segment 1 partial at 70,000 − 65,536 = 4,464 entries).
- **CRC array size:** 2 × 4 = **8 bytes**.
- **Region size:** 70,000 × 20 + 8 = 1,400,000 + 8 = **1,400,008 bytes** — and this is exactly the value `extent_length` must carry (L21 otherwise).
- Region partition: entry array **[0, 1,400,000)**, segment CRC array **[1,400,000, 1,400,008)**.

**Entry 69,999** — the last entry — lies at region byte 20 × 69,999 = 1,399,980, i.e. **[1,399,980, 1,400,000)**. Its segment index is 69,999 div 65,536 = **1**, which per §15.4 covers entries [65,536, min(131,072, 70,000)) = [65,536, 70,000).

**Exactly what must be verified before using entry 69,999** (`[R-IDX-04]`: "To use entry k, a reader MUST verify, in dependency order, crc_of_crc_array over the fetched CRC array and the segment CRC over the fetched segment containing k"; both ranges computable from the layer record alone, and they MAY be fetched in parallel):

1. **`crc_of_crc_array`** (the u32 in the layer record) over region bytes **[1,400,000, 1,400,008)** — the whole 8-byte segment CRC array as stored.
2. **Segment 1's CRC** — the second u32 of that array, at region bytes [1,400,004, 1,400,008) — over region bytes **[1,310,720, 1,400,000)**, that being 20 × 65,536 = 1,310,720 through 20 × 70,000 = 1,400,000. Length 89,280 bytes = 4,464 entries × 20. ✓ (A partial segment's CRC "covers only its actual bytes" — §15.4 — so this is 89,280 bytes, not 1,310,720, and `[R-IDX-05]`'s all-sentinel constant may not be used here: only *full* segments may take the constant, and even then "Equality with the constant licenses nothing for readers".)

Segment 0's CRC value is verified as *bytes* (it is inside the array covered by `crc_of_crc_array`), but segment 0's *entries* need not be fetched or checked — that is the whole point of segmentation.

Enclosing links of §8.2's ordered chain must already hold: trailer CRC over trailer [0, 60); directory CRC over dir_length − 4 bytes; and the layer's I/O-free cross-checks `[R-CNT-17]` (entry_count = geometry-derived addressed-tile count; extent_length = 1,400,008). Downstream, once the entry is classified non-sentinel, its own `crc` must verify over the fetched stored bytes before any decoding (§19.4 step 5, `[R-CNT-20]`).

Total pre-read verification volume: 89,288 bytes — well under §15.4's stated worst case of one full segment (1.25 MiB) plus the CRC array.

**Citations:** `[R-CNT-17]`, `[R-IDX-01]`, §15.4 `[R-IDX-04]`, `[R-IDX-05]`, §8.2 `[R-CNT-20]`, §19.4 `[R-RDR-04]` steps 3–5.
**Confidence: high.**

---

## Q13 — Rank 32 and rank 40

- **Rank 32: yes, a conforming reader must accept it.** §21.9's table gives "rank d of a layer | 32" as a **minimum guarantee**, and `[R-CNF-03]` binds: "A reader MUST accept every conforming file none of whose values exceeds the minimum guarantees of §21's limits table." `[R-ERR-03]` restates it as a floor, and `[R-ERR-04]` adds the teeth: "Software that declines a file whose every quantity lies within the table is not a conforming reader." Note the precise condition is joint — the *file's* other quantities must also be within the table (see OBSERVATION 5).
- **Rank 40: not required to accept; a reader MAY decline.** `[R-ERR-04]`: "A file exceeding any of these remains conforming, and a reader MAY decline it." Rank 40 is perfectly representable and valid — the hard cap is 255, a consequence of the `u8` rank field (`[R-ERR-05]`, §7.4, Appendix B) — so this is a capability question, not a validity question.
- **If it declines, what must it report?** `[R-ERR-04]`: "a refusal on resource grounds MUST be reported as a resource limit and not as a validity error: the two send a user to opposite remedies, and a reader that reports 'too large' as 'corrupt' invites the deletion of intact data." Appendix H's reader checklist repeats it.

What the text does **not** fix is the *scope* of that refusal — whether the reader declines the file or may decline only the oversized layer and serve the rest. See AMBIGUITY 1.

**Citations:** §21.9 `[R-ERR-03]`, `[R-ERR-04]`, `[R-ERR-05]`, §2.3 `[R-CNF-03]`, §2.5 `[R-CNF-10]`, Appendix B, Appendix H.
**Confidence: high** on the three answers; **medium** on refusal scope.

---

## Q14 — A compacted file's identity, and unknown MU = 1 records

**file_id: a new one. generation: 1.** `[R-WRT-06]`: "It MUST give the output a new file_id (§9.3's randomness advice applies) and generation 1: a compacted file is a whole-file rewrite under a new file_id by definition (`[R-LIF-01]`), and reusing the input's would break the (file_id, range) cache contract of `[R-LIF-03]`, since relocation puts different bytes at the same ranges." The id must be nonzero (`[R-CNT-06]`) and SHOULD be drawn from a cryptographically random source (§9.3, `[R-LIF-03]`). `[R-PRV-04]` confirms the intent: "Compaction mints a new one — the only defined way to break file_id linkage". Two other trailer fields ride along: unknown ignore-lane flag bits are copied forward (`[R-CNT-08]`) and version_minor follows `[R-CNT-26]`.

**Unknown record type with MU = 1: the compactor MUST refuse to compact the file.** `[R-WRT-06]`: "A compactor MUST refuse to compact a file carrying **any** record whose type it does not implement with MU = 1: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated." "Any" covers layer sub-records as well as top-level records — and it is at layer scope that the rule does real work, since a top-level unknown MU = 1 record already makes the compactor, which is a reader (`[R-CNF-11]`), reject the file under `[R-CNT-15]`. Refusal is unconditional: dropping the offending layer and compacting the remainder is not licensed.

The rule is load-bearing for `[R-WRT-07]`'s claim that "No other record payload carries a file offset: MU = 0 records by rule (§7.2), and an MU = 1 type the compactor does not implement never reaches this step."

**Citations:** §20.5 `[R-WRT-06]`, `[R-WRT-07]`, `[R-LIF-01]`, `[R-LIF-03]`, §9.3, `[R-CNT-06]`, `[R-CNT-08]`, `[R-CNT-26]`, `[R-CNF-11]`, `[R-CNT-15]`, `[R-PRV-04]`.
**Confidence: high** (small residual on "new" — see AMBIGUITY 3).

---

## Q15 — Appendix A's trailer CRC and its coverage

**Value: `0xE00938D2`, stored little-endian as the bytes `D2 38 09 E0` at file offsets [124, 128).**

**Covered bytes: trailer bytes [0, 60) — absolute file bytes [64, 124).** That is the trailer's first 60 bytes: magic, version_major, version_minor, flags, generation, dir_offset, dir_length, committed_file_length, file_id, and the 4 reserved bytes — everything except the CRC field itself.

Three independent statements of the coverage agree: §6.2's layout row ("trailer CRC | structural | CRC-32C over trailer bytes [0, 60)"); §8.1's map ("Trailer | trailer bytes [60, 64) | trailer bytes [0, 60)"); and `[R-CNT-24]`'s permanent, cross-major guarantee ("a CRC-32C at F − 4 covering bytes [F − 64, F − 4)"), which for F = 128 gives [64, 124) ✓.

I recomputed this from the appendix's own field values — `8A 4E 52 41 54 0D 0A 1A | 01 00 | 00 00 | 00 00 00 00 | 01×u64 | 16×u64 | 4×u64 | 128×u64 | 0x0123456789ABCDEF×u64 | 00 00 00 00` — and got `0xE00938D2`. Appendix A is byte-accurate.

**Citations:** §6.2 (trailer layout), §8.1 `[R-CNT-19]`, `[R-CNT-24]`, §4.5 `[R-ENC-09]`, Appendix A.
**Confidence: high** (independently verified by computation).

---

## Findings

### AMBIGUITY

**A1 — Scope of a resource refusal is undefined. §21.9 `[R-ERR-04]`, with `[R-CNF-03]` (§2.3).**
`[R-ERR-04]` says "A file exceeding any of these remains conforming, and a reader MAY decline **it**", and requires the refusal be reported as a resource limit rather than a validity error. Two readings the text permits: (a) the licensed unit of refusal is the whole file — a reader that meets one over-guarantee layer declines the file; (b) a reader may decline at the narrowest scope affected (that layer, or that tile for the 256 MiB tile guarantee) and serve everything else, since nothing forbids it and §2.4's outcome classes are explicitly about *violations*, which this is not. I picked (b) as permissible and (a) as certainly permitted, because §2.4's blast-radius vocabulary is unavailable here by its own terms and no rule requires a reader to fail a whole file for one oversized layer. The consequence is observable: two conforming readers given the same conforming file can differ on whether the other layers are served. Related: §21.9's guarantees are per-quantity, so the phrase "a conforming file whose quantities lie within these bounds" needs the joint reading (`[R-CNF-03]`'s "none of whose values exceeds") to be well defined — that part *is* determined, but only from §2.3, not from §21.9's own text. **Not byte-level** — no reading changes which bytes are produced or accepted as valid.

**A2 — May an updater commit at all to a file carrying an unknown top-level MU = 1 record? §20.4's preservation table vs. `[R-CNT-15]` (§7.2) with `[R-CNF-11]` (§2.3).**
§20.4's table row reads: "MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs: an unknown critical record at layer scope blocks modification of that layer, and **at file scope blocks file-scope modification entirely**." Reading (a): the file-scope clause licenses an appender to commit — modifying, say, one layer's tiles — while re-emitting the unknown record byte-identically and touching nothing file-scope. Reading (b): an updater is a reader of what it processes (`[R-CNF-11]`), `[R-CNT-15]` makes an unknown top-level MU = 1 record **reject-file**, and §2.4's reject-file row says "A reader MUST NOT rely on any structure in it" — so the updater must stop, emit nothing, and the §20.4 row's file-scope clause is vacuous at that scope (it does real work only for layer-scope sub-records, where reject-layer leaves other layers modifiable). **I picked (b)**: `[R-CNT-15]` is unconditional, `[R-CNF-11]` is unconditional, and `[R-WRT-06]`'s parallel rule for compactors ("MUST refuse") shows the document's intent for critical unknowns. Reading (a) would let a tool append to a file every conforming reader rejects. **Not byte-level** — both readings agree on what a conforming file may contain; they differ only on whether a tool may produce a new generation.

**A3 — "a new file_id" (§20.5 `[R-WRT-06]`) — fresh draw, or provably different?**
Reading (a): the compactor MUST ensure output file_id ≠ input file_id (implying a comparison). Reading (b): it MUST mint a fresh identifier per §9.3's randomness advice, and a 1-in-2⁶⁴ collision with the input would be unfortunate but not a violation. The rationale clause ("reusing the input's would break the (file_id, range) cache contract") argues for (a); the parenthetical "(§9.3's randomness advice applies)" argues for (b). **I picked (a)** — the stated harm is about the *value*, not the *process* — which costs one comparison. Appendix G item 2's hash-derived file_id is compatible with either. **Not byte-level** in any consequential sense: file_id is a writer-chosen value in both readings.

**Byte-level ambiguities: none.** I specifically stress-tested the layout surfaces where two readings could produce or accept different bytes, and each is closed by explicit text: field order/widths of the layer-record inline payload (§7.4's table + `[R-CNT-18]`'s exact-parse rule); the tile-index region's two-part layout, entry stride, and ordinal→byte mapping (§15.1 `[R-IDX-01]`); sentinel bytes (`[R-IDX-02]` + Appendix B); segment boundaries and partial-segment CRC coverage (§15.4); interleaved vs. planar value order and offsets (`[R-SER-01]`, `[R-SER-02]`); packed-bool bit order, decoded size, and pad-bit content (`[R-SER-03]`, `[R-SER-05]`, §4.4); padding-position content (`[R-SER-05]`); shuffle stride selection and permutation direction, both stated *and* worked (`[R-COD-10]`); every checksum's exact byte range (§8.1's map, §6.2, §7.1, §15.4); the pre-trailer pad's length (uniquely determined by `[R-LIF-02]` step 5 + F13); and codec-1's length equality (`[R-COD-04]`). Where a formula could have been read two ways, a numeric example pins it — and all nine such examples reproduce exactly.

### CONTRADICTION

**C1 — §2.3 says "four classes" and then defines five.**
§2.3's opening sentence: "Conformance is defined for four classes." The bullets that follow define five: **Conforming TARN file** `[R-CNF-02]`, **Conforming reader** `[R-CNF-03]`/`[R-CNF-04]`, **Conforming writer** `[R-CNF-05]`, **Conforming updater** `[R-CNF-06]`, **Conforming verifier** `[R-CNF-11]`. Appendix H independently enumerates five checklists ("Conforming file / reader / writer / updater / verifier"), and §21.1, §2.4, and §19.2 all treat verifier as a distinct actor with its own detection tier ("*certification*, for the rows a verifier detects, which §19.2 places outside the reader tiers entirely"). Both cannot hold: either the count is stale or one bullet is not a class. Cosmetic in effect — no behavior depends on the number — but it is a normative sentence (§2.3 is not labeled Note/Example/Rationale, so `[R-CNF-01]` makes it normative) and it is the first thing a fresh implementer reads about conformance.

**C2 — The register's normative completeness (§21.1) and `[R-CNF-07]` (§2.4) versus §21.6's three "the file is nonconforming" rows.**
`[R-CNF-07]`: "Every detectable violation named by this specification is assigned exactly one reader outcome: reject-file, reject-layer, reject-tile, or ignore-record." §21.1: "The register below enumerates every violation this specification names … a violation this specification names and the register omits is a defect in this document." §21.6 is headed "Conditions that are **not** violations … These are defined behaviors, not errors" — yet three of its rows say the opposite in their own text:
- unsorted user-metadata members → "The file is nonconforming, but the document is readable" (`[R-MTA-05]`, a writer MUST);
- an unregistered `tarn.`-prefixed key → "The file is nonconforming, but a reader ignores that key" (`[R-MTA-06]`, a writer MUST NOT) — which also contradicts §18.3's own sentence four lines earlier, "A file carrying an unrecognized `tarn.` key is **conforming**";
- a registered type's stored MU/PE bit differing from §7.3's fixed value → "The file is nonconforming, but readers apply the type's fixed semantics" (`[R-CNT-22]`).

Each is a named violation with no register row in §21.2–§21.5 and no assigned outcome class, so `[R-CNF-07]`'s "exactly one" and §21.1's completeness both fail for them. The document elsewhere shows it knows how to handle writer-only violations — F30/F31 and L47/L48 give the MU=1/PE=0 combination and reserved flag bits proper rows with a verifier detector and a scope — so the omission is inconsistent with the register's own practice, not a deliberate carve-out. Concretely, this bites a verifier implementer: §21.1 says detection points and outcomes come from the register, and there is no row to cite when reporting an unsorted document, nor any scope to attach to the report. (§18.3's internal conflict on the `tarn.` key is the sharpest of the three, since the two statements are five lines apart and flatly opposite.)

### OBSERVATION

**O1 — Fill is amendable in a "metadata-only" commit but binds stored bytes, and §20.3 doesn't warn.**
`[R-SER-05]` requires every padding position of a *stored* tile to encode "that channel's **recorded** fill value", and T4 makes a mismatch a tile-scope validity error. A channel's recorded fill lives in the layer record, which a commit may rewrite while keeping the extent slot pointing at the existing index region (§20.3 step 4: "A layer whose record alone changes keeps its extent slot"). Step 4 lists what forces re-emission — stored-tile set, index content, index placement — and a **fill change is none of those**. So amending a fill value silently makes every retained stored *edge* tile nonconforming under T4, with no reader-visible symptom (readers never return padding positions, `[R-GEO-04]`) and no rule in §20 flagging it. Related: §13.1 classifies fill as semantic — "it affects what unstored samples read as, never how any byte is located or decoded" — which is literally true (writing is neither locating nor decoding) but does not prepare a reader of §13 for §14.5's byte-level obligation; I had to hold both sections open to see the interaction. Also related: §11.1's Rationale advertises "extent growth is a metadata-only operation", which holds only while the grid counts Gᵢ = ⌈Eᵢ/Tᵢ⌉ are unchanged; once E crosses a tile boundary the addressed-tile count and every disk ordinal change, and §20.3 step 4 does say so ("a geometry change renumbers ordinals"). Suggest a sentence in §20.3 step 4 adding "a change to any channel's fill value" to the re-emission triggers.

**O2 — `[R-LIF-08]` coverage verification is decidable but disproportionately expensive, and dead-space bit-rot fails the whole file.**
§9.7(d) plus F42: "A verifier that cannot verify an enumerated generation's trailer, directory, tile index, or **any structure those claim** (stored-tile extents and record extents included) cannot establish coverage and MUST treat the file as nonconforming." So certifying a file requires verifying every checksum of every *superseded* generation — bytes no live read ever touches — and a single bit flip in dead space (a superseded tile payload) makes an otherwise perfect file uncertifiable at file scope. For an append-heavy file this is O(total bytes ever written) rather than O(live bytes), and the failure mode is one no compaction-free remedy fixes. It is decidable and the document is internally consistent about it (`[R-CNT-21]` classifies dead space; §20.5 reclaims it), but implementers sizing a verifier should know the cost is unbounded in file history, and users should know that "verify" and "read" can disagree for reasons that have nothing to do with the data they can reach.

**O3 — §9.7(a)'s "taking the file size as F_k" required a second reading.**
`[R-LIF-08]` step (a): "A candidate qualifies only if it satisfies `[R-CNT-06]`'s field validity against its own committed length F_k (taking the file size as F_k)". `[R-CNT-06]` contains "committed_file_length equals the file size", which for a superseded candidate is false against the physical size — the parenthetical is doing the work of substituting F_k for "the file size" throughout the borrowed check. Decidable, but the reuse of a rule whose text names the physical file size for candidates that are by construction not at the physical end is the one place in Part I where I had to reconstruct the intent rather than read it.

**O4 — Asymmetric statement of the user-metadata extent's document boundary.**
§18.2 pins the boundary explicitly for encoding 2 ("exactly one RFC 8878 compressed frame occupying the extent's bytes **before its terminal CRC**") but says only "Encoding 1 stores the document verbatim". The boundary for encoding 1 — document = extent bytes [0, extent_length − 4) — is forced by §8.1's map ("User-metadata extent | final 4 bytes of the extent | the preceding bytes"), so only one reading survives and this is not an ambiguity; but the asymmetry invites an implementer to include the CRC bytes in the JSON text. One clause in §18.2 would close it.

**O5 — §21.9's guarantees are per-quantity and do not compose; a corpus builder needs to know that.**
The table guarantees rank 32 *and* a 256 MiB decoded tile, but a rank-32 layer with every Tᵢ ≥ 2 has P = ∏Tᵢ ≥ 2³² sample positions, i.e. ≥ 4 GiB for even a one-byte channel — 16× above the tile guarantee. So the only rank-32 layers a reader is obliged to accept are ones with nearly all tile extents equal to 1. `[R-CNF-03]`'s "none of whose values exceeds" makes this correct as written (the conjunction is required), but the table reads like a menu of independently achievable maxima and `[R-VEC-03]` will need vectors that respect the joint constraint. Worth a sentence under the table.

**O6 — `[R-CNT-13]`'s exactly-once ownership forecloses tile deduplication.**
"within the live committed state … no two extent slots and no two structures overlap", with cross-layer overlap being reject-file. Two identical tiles — the common case of a large constant region, or the same mask reused by two layers — cannot share one stored extent; each needs its own bytes. This is a deliberate anti-aliasing property (`[R-SEC-03]` names it as removing a whole attack class), but it is a natural optimization implementers will attempt and the document never says "no" in those words. The sanctioned substitute is the sentinel plus fill (`[R-IDX-02]`, `[R-TYP-08]`) for all-fill tiles, which Appendix G item 6 makes a reproducibility requirement.

**O7 — The register's mechanical counts hold exactly; I verified them.**
§21.1 states the instance count is mechanical ("Instances within a cell are separated by semicolons, and a cell reading — is one instance"). Applying that rule: §21.2 has 43 rows (F1–F45 with F6 and F39 retired) totalling **91** instances; §21.3 has 47 rows (L1–L48 with L40 retired) totalling **81**; §21.4 has 26 rows (T1–T26) totalling **43**; §21.5 has 10 rows (R1–R10) totalling **20**. Rows: 43 + 47 + 26 + 10 = **126**; instances: 91 + 81 + 43 + 20 = **235**. Both match §21.8's "126 conditions over 235 named instances" exactly, and each section's stated row count matches its table. Combined with the four reproduced CRC constants and the nine reproduced worked examples, the document's arithmetic surface is clean — which is unusual at this size and is the main reason my confidence below is high rather than medium.

**O8 — No diagnostic guidance for the unimplemented-incompat-flag case, the exact analogue of the version_major case that gets it.**
`[R-CNT-07]` requires a distinct diagnostic for an unimplemented major ("a reader that reports an unimplemented major as corruption misleads users into discarding files that current software reads"), and §21.6 carves the case out explicitly as "a reader's capability, not a defect in the bytes". `[R-CNT-08]`'s incompat lane is the same situation one level down — a later minor may define incompat bits, and files carrying them are conforming under that minor while this text's readers reject them — but F26 lists it as a plain file-scope violation with no analogous caveat and no diagnostic advice. The same user-harm argument applies verbatim.

**O9 — The top-level record sequence lacks the explicit "no residue" clause its sub-record sequences get.**
`[R-CNT-18]` says a layer record's remaining bytes "MUST parse as zero or more complete sub-records … **with no residue**; any overrun, truncation, or residue is a validity error at layer scope." §7.2's top-level sequence has no such sentence. It is nonetheless decidable: residue of ≥ 24 bytes parses as a record header (and is then subject to the type-0 and MU gates), and residue of < 24 bytes trips F32 / `[R-CNT-12]` because the header extends past the sequence end. I had to construct that argument rather than read it; one clause in §7.2 mirroring `[R-CNT-18]` would remove the inference.

---

## Verdict

IMPLEMENTABLE: yes
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high
