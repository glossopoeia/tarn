# Round 24 — quiz answerer working transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(read in full, in six `sed` slices). I ran one Python script I wrote myself
(`calc.py`, in this scratchpad) implementing CRC-32C and the arithmetic below;
it reads no files. No ADRs, no `docs/`, no `conformance/`, no `registry.json`,
no git, no web. Unrequested context did appear in my prompt before I began: a
project instruction file (`CLAUDE.md`) pointing at `AGENTS.md`, and an index of
the maintainer's auto-memory files with one-line descriptions. I did not open
`AGENTS.md` or any memory file, and I did not use any of that material as
evidence; every answer below is derived from `spec/tarn.md` alone.

**CRC tool validation.** My CRC-32C reproduces §4.5's check vector
(`"123456789"` → `0xE3069283`; zero bytes → `0x00000000`), Appendix A's trailer
CRC `0xE00938D2`, §7.4's worked example (4 sentinel entries → segment CRC
`0x80A34955`, crc_of_crc_array `0xC4EE982E`), and §15.4's full-all-sentinel
segment constant `0xEECB3BB2`. Four independent anchors, all matching.

---

## Q01 — bytes at 192-byte file offsets 188..191

F = 192, so the live trailer occupies [128, 192) (§6.2: final 64 bytes,
64-aligned; 192 mod 64 = 0). Offsets 188..191 = trailer bytes [60, 64) = the
trailer CRC field: "CRC-32C over trailer bytes [0, 60)" (§6.2 layout table),
stored as a little-endian u32 (`[R-ENC-09]`).

Trailer bytes [0, 60), assembled from §6.2's layout with the declared values:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                      version_major = 1
00 00                      version_minor = 0
00 00 00 00                flags = 0
03 00 00 00 00 00 00 00    generation = 3
10 00 00 00 00 00 00 00    dir_offset = 16
44 00 00 00 00 00 00 00    dir_length = 68
c0 00 00 00 00 00 00 00    committed_file_length = 192
ef be ad de 00 00 00 00    file_id = 0x00000000DEADBEEF
00 00 00 00                reserved
```

(Gate sanity: dir_offset 16 ≥ 16; dir_length 68 ≥ 4; 16 + 68 = 84 ≤ F − 64 = 128;
F multiple of 64; file_id ≠ 0 — the file is expressible.)

CRC-32C = **0xF3566CE6** → stored little-endian.

**Answer: `e6 6c 56 f3`.** Confidence: high.

---

## Q02 — crc_of_crc_array for entry_count = 3, all sentinel

§15.1: region = entry array (3 × 20 = 60 bytes) then segment CRC array
(⌈3/2¹⁶⌉ × 4 = 4 bytes). §15.4: segment 0 covers entries
[0, min(2¹⁶, 3)) = [0, 3); "the final partial segment's CRC covers only its
actual bytes." `[R-IDX-05]` licenses the `0xEECB3BB2` constant only for a
**full** segment — "a partial segment's CRC MUST be computed" — so it does not
apply here.

Sentinel entry (§15.2, `[R-IDX-02]`): `FF ×16 00 ×4`. Three of them = 60 bytes.

- segment CRC = CRC-32C(60 sentinel bytes) = **0xD171D122**, stored `22 d1 71 d1`
- crc_of_crc_array (§7.4, §8.1) = CRC-32C over that 4-byte array = **0x34C74AFB**

Note entry_count ≠ 0, so `[R-CNT-23]`'s "0 when entry_count = 0" does not fire.

**Answer: `fb 4a c7 34`.** Confidence: high.

---

## Q03 — interleaved stored bytes with byte-shuffle

Geometry: d = 1, T₀ = 4, so P = 4 (§11.2). C = 2: `a` uint8 (B = 1), `b` uint16
(B = 2). Sample stride Q = ΣBᵢ = 3 (§14.2). Decoded size = P·Q = 12.

Value sequence (§14.1, interleaved, sample-major, declared channel order):

decoded tile image = `11 34 12 | 22 78 56 | 33 bc 9a | 44 f0 de`
(each `b` value little-endian: 0x1234 → `34 12`, etc.)

Pipeline (§17.1): decoded image → **filter** → **codec**. Filter 2 byte-shuffle
(`[R-COD-10]`): stride s = Q = 3 for an interleaved tile; L = 12, n = L/s = 4;
"byte i of group j at offset i · n + j".

- i = 0 → offsets 0–3: `11 22 33 44`
- i = 1 → offsets 4–7: `34 78 bc f0`
- i = 2 → offsets 8–11: `12 56 9a de`

(Verified my transform against §17.3's own worked example: `00 00 80 3F 00 00 00
40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`. Exact match.)

Codec 1 = none: "the stored bytes are the filtered image verbatim"
(`[R-COD-04]`), and the entry length must equal the decoded size, 12. ✓

**Answer: `11 22 33 44 34 78 bc f0 12 56 9a de`.** Confidence: high.

---

## Q04 — planar bool packed plane, decoded tile image

G_y = ⌈3/3⌉ = 1, G_x = ⌈2/3⌉ = 1, N = 1; planar addressed-tile count = C·N = 1.
P = ∏Tᵢ = 9. Planar bool → §14.3 packing, decoded size ⌈9/8⌉ = 2.

In-tile ordinal (§11.4, permanent row-major) = u_y·T_x + u_x = 3·u_y + u_x.
Positions with u_x = 2 have coordinate x = 2 ≥ E_x = 2, so they are **padding
positions** (§11.3) and `[R-SER-05]` fixes their content to the channel's fill
bit — fill byte 0x01 = true.

| ordinal | (u_y,u_x) | value |
|---|---|---|
| 0 | (0,0) | true = 1 |
| 1 | (0,1) | false = 0 |
| 2 | (0,2) | padding → fill = 1 |
| 3 | (1,0) | false = 0 |
| 4 | (1,1) | true = 1 |
| 5 | (1,2) | padding → 1 |
| 6 | (2,0) | true = 1 |
| 7 | (2,1) | true = 1 |
| 8 | (2,2) | padding → 1 |

Byte 0 = bits 0–7 = 1,0,1,0,1,1,1,1 → 1+4+16+32+64+128 = 245 = **0xF5**.
Byte 1 = bit 0 = ordinal 8 = 1; P mod 8 = 1, so pad bits 1–7 each carry the
fill bit = 1 (`[R-SER-05]`: "Every pad bit MUST carry the plane's channel's fill
bit") → **0xFF**.

Filter 1 and codec 1 leave stored = decoded anyway; the question asks for the
decoded tile image.

**Answer: `f5 ff`.** Confidence: high.

---

## Q05 — compactor output trailer

flags = 0x00050000 → bits 16 and 18, both in the **ignore lane** (16–31). §6.3:
readers ignore them, "a set ignore-lane bit is not a file-conformance
violation", and "A compactor … carries the input's unknown ignore-lane bits
into its output trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`)."
`[R-WRT-06]`: "The output trailer MUST copy the input's unknown ignore-lane flag
bits forward."

(a) Trailer offsets [12, 16) = the flags field (§6.2 table) = 0x00050000
little-endian = `00 00 05 00`.

(b) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and
generation 1: a compacted file is a whole-file rewrite under a new file_id by
definition." → **1**.

(c) §20.5: "Where the output carries a feature a later minor defines and this
compactor does not — on a conforming input a carried ignore-lane bit (§6.3) …
— the output's version_minor SHOULD be at least the input's." Input's minor is
4, so the floor is **4** (not `[R-CNT-26]`'s 0, which governs only "Otherwise").

**Answer: `00 00 05 00`; 1; 4.** Confidence: high.

---

## Q06 — verifier, major 2 + bad trailer CRC

§6.2 fixes the order: "the trailer magic; the trailer CRC; the version gate
(§6.3)". The CRC check precedes the version gate. §21.2's preamble is explicit
that this row reaches a foreign-major file: "Four rows are outside that
reasoning and do reach it, because their subject is a field fixed across every
major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, **F14's trailer CRC**
— the two checks §6.2 places before the gate."

F14 is therefore established as a violation. §2.3: "An established violation
takes priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and *cannot
establish* is available only to a traversal that established no violation."

Competing reading considered: §2.3's "a file declaring another major is neither
conforming nor nonconforming under it" would push toward *cannot establish*.
§21.2 resolves it expressly against that reading for this exact field, so it is
not underdetermined.

**Answer: nonconforming.** Confidence: high.

---

## Q07 — experimental-range metadata encoding

Encoding byte 0x9A = 154 ≥ 0x80 → the experimental range (§10.2, §18.2).
Framing is clean: type 0x0002 with MU = 0 / PE = 1 matches §7.3's registry-fixed
flags (so no F28); inline_length = 1 (so no F23); extent nonzero, wholly within
[16, F−64), extent_length 40 ≥ 5 (so no F21/F22/F30–F32); terminal CRC verifies
(so no R2). Encoding is neither 0 nor reserved 3–0x7F, so R1 does not fire.

(a) §21.6: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | **Ignored (ignore-record)**; the file is conforming".

(b) Same row: "No document rule attaches at such an encoding, so a verifier
certifies, reporting the record it ignored." `[R-MTA-10]`: "A verifier meeting
such a record in an otherwise conforming file has no requirement it is unable to
check … and certification is unaffected." Since nothing else departs from the
spec, the verdict is **conforming**.

**Answer: ignore-record; conforming.** Confidence: high.

---

## Q08 — compactor meets offset=S, length=S, crc≠0

§15.3's second row: "offset = S ∧ length = S ∧ crc ≠ 0 | *structural*:
reject-tile". crc = 0x00000007 ≠ 0, so this is not a valid sentinel; it is a
structural reject-tile (register row T6).

§20.5, on regenerating a relocated index region: "An entry §15.3 classifies
reject-tile on a **structural** ground is neither — `[R-IDX-03]` gives it no
stored extent for a re-pointing to target — so regenerating the region cannot
proceed without meeting it, and the violation is thereafter one the compactor
has detected. **`[R-WRT-06]` then obliges refusal**: the compactor can neither
reproduce the entry nor invent a replacement, and no drop is available, a
tile-index entry being no record §20.4's table licenses dropping."

**Answer: refuse to compact.** Confidence: high.

---

## Q09 — Frame_Content_Size 200 vs 199-byte document

Encoding byte 0x02 = zstd (assigned). §18.2: "The frame's content-size field,
unlike the decoded size and the window, is *not* left to the reader: it MAY be
present, and when present it MUST equal the byte length of the decoded document.
**A mismatch is one of the frame constraints R4 registers, not a failure to
decode under R3**: the bytes decode, and what is wrong is what the header said
about them."

R4's instance list contains exactly this case: "the content-size field declared
larger than the decoded length, layer sub-record extent." 200 > 199. ✓

Everything else is clean: magic present, no dict ID, no content checksum, no
second/skippable frame, no trailing bytes, terminal CRC verifies, content rules
satisfied — so R3, R5–R10 do not fire.

Outcome: §18.2's closing sentence — "Any violation here is ignore-record, never
the tile-scope outcome §17.2 assigns" — and §21.5's outcome heading.

**Answer: R4; ignore-record.** Confidence: high.

---

## Q10 — planar entry_count and extent_length

G_y = ⌈5000/100⌉ = 50. G_x = ⌈4000/64⌉: 4000/64 = 62.5, and 62·64 = 3968 < 4000,
so G_x = 63. N = 50 × 63 = 3150 (§11.2).

Planar addressed-tile count = C·N = 25 × 3150 = **78,750** = entry_count
(`[R-CNT-17]`: entry_count "equals the addressed-tile count").

`[R-CNT-17]`, index_encoding 1: extent_length = entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4 = 78,750 × 20 + ⌈78,750/65,536⌉ × 4
= 1,575,000 + 2 × 4 = **1,575,008**.

**Answer: 78750; 1575008.** Confidence: high.

---

## Q11 — planar ordinals for (1000, 3000), channel 17

G_y = 4096/64 = 64, G_x = 64, N = 4096.

- t_y = 1000 div 64 = 15; u_y = 1000 mod 64 = 40
- t_x = 3000 div 64 = 46; u_x = 3000 mod 64 = 56
- (a) s = Σ tᵢ·∏_{j>i} Gⱼ = 15·64 + 46 = 1006; planar disk ordinal
  = c·N + s = 17·4096 + 1006 = 69,632 + 1006 = **70,638** (`[R-GEO-06]`)
- (b) "The entry for the tile with disk ordinal k is the k-th entry, at region
  byte 20·k" (`[R-IDX-01]`) → 20 × 70,638 = **1,412,760**
- (c) "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))"
  (`[R-IDX-04]`); 65,536 ≤ 70,638 < 131,072 → segment **1**
- (d) in-tile ordinal = Σ uᵢ·∏_{j>i} Tⱼ = 40·64 + 56 = 2560 + 56 = **2616**

**Answer: 70638; 1412760; 1; 2616.** Confidence: high.

---

## Q12 — slab packing offset X

S = 4 over the single interleaved block [0, 8) → run 0 = ordinals [0, 4), run 1
= [4, 8) (`[R-SLB-02]`: "Run r of a block starts at ordinal block_start + r·S").
Entry 3 lies in run 0 alongside entries 0, 1, 2.

Transparency (`[R-SLB-03]`): "Sentinel tiles are transparent to run continuity…
So are the entries §15.3 classifies reject-tile on a **structural** ground: they
address no usable extent, and the run's stored tiles close over them."

- entry 1: valid sentinel → transparent
- entry 2: offset 0, length 500, non-sentinel → §15.3 row "offset < 16
  (non-sentinel) | *structural*: reject-tile" (row T8) → transparent

So run 0's stored tiles, in ordinal order, are entry 0 then entry 3.

- first stored tile's offset 8192 mod A_slab 4096 = 0 ✓
- packing: "each stored tile's offset equals the previous stored tile's offset
  plus its length" → X = 8192 + 300 = **8492**

**Answer: 8492.** Confidence: high.

---

## Q13 — empty layer declaring lz4 with a huge tile

E₀ = 0 → G₀ = ⌈0/2³⁰⌉ = 0 → N = 0, addressed-tile count 0 (`[R-GEO-02]`:
"A dimension with extent 0 is valid"). entry_count = 0 ✓ (`[R-CNT-17]`);
extent slot (0, 0) ✓ (§7.4: "a layer with zero addressed tiles has extent
(0, 0)"; L22's formula gives 0); crc_of_crc_array = 0 ✓ (`[R-CNT-23]`);
A = 0 with A_slab = 0 ✓; S = 0 so `[R-CNT-16]` is satisfied; rank 1 ≥ 1,
C = 1 ≥ 1, T₀ = 2³⁰ ≥ 1 (`[R-GEO-01]`); fill length 4 = uint32 element size
(`[R-CNT-23]`); names `z`, `t`, `v` valid; layout 1, linearization 1, filter 1,
index_encoding 1 all assigned.

The one suspicious item is codec 4 with P·Q = 2³⁰ · 4 = 4,294,967,296, far above
`[R-COD-07]`'s 0x7E000000 = 2,113,929,216. But the cap is quantified over
**addressed** tiles, and this layer addresses none. §17.2's Note is explicit:
"The cap is quantified over the layer's *addressed* tiles, so a layer that
addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
whatever its tile shape declares, and **codec 4 is conforming there**." L44's row
text carries the same quantifier.

The same Note flags the arithmetic that *is* checked: "`[R-ENC-04]`'s overflow
rule carries no such quantifier … so P·Q and P·Bᶜ are checked in an empty layer."
P·Q = 2³² ≪ 2⁶³ − 1, so L2 does not fire either. N·P = 0, C·N = 0, index
formula = 0.

**Answer: no.** Confidence: high.

---

## Q14 — zstd frame with a Window_Descriptor on an 18-byte tile

Interleaved, C = 1 uint16, P = 3·3 = 9, Q = 2 → decoded size = P·Q = 18 bytes
(§14.2).

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size; a reader MUST treat either as a validity error at tile scope, both
being header-checkable."

Single_Segment_Flag is clear, so Window_Size comes from the Window_Descriptor.
§17.2's Note: "without it, the Window_Descriptor cannot express less than 1 KiB.
A tile whose decoded size is below 1 KiB — §14.2's worked examples give 18 and 30
bytes — is therefore encodable under codec 3 only as a single-segment frame."
So the declared window is ≥ 1024 > 18: the window-size constraint is broken, and
it is the *only* one broken (magic present, no dict ID, no checksum flag, single
frame, no trailing bytes, decodes to exactly the image, so T17–T20, T22, T24,
T25, T3 all clear).

§21.4 row **T21**: "Codec 3 (zstd) and the frame declares a window size larger
than the tile's decoded size | interleaved P·Q; …".

**Answer: T21.** Confidence: high.

---

## Q15 — shrink that repads a prior-generation stored tile

Geometry: G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3 → N = 9 = entry_count. After the
shrink G_x = ⌈9/4⌉ = 3 — unchanged, as stipulated.

Tile (0, 2) covers y ∈ [0, 4) and x ∈ [8, 12). Under E_x = 10 its real x
positions are 8 and 9; under E_x = 9 only 8. So x = 9 (four sample positions,
y = 0..3, all real in y) converts from real position to **padding position**,
changing "the set of padding positions (§11.3) and the content `[R-SER-05]`
fixes there" for a tile L stored in generation 1.

§20.3 step 4: "A commit MUST NOT change a layer's declarations in a way that
alters, for any tile that layer stores **in the generation this commit
supersedes**, what §14 fixes for its stored bytes or how they decode — the set
of padding positions …". And on shrinks specifically: "Unstoring that tile in the
same commit does not rescue it either, and for the same reason: the quantifier is
the superseded generation's, so **a shrink that turns real positions into padding
of a tile stored there is barred whether or not the new state still stores it**."

(a) → **barred**.

(b) The generation-2 live state is clean: nine sentinel entries, entry_count
matching the (unchanged) grid, a valid index region and crc_of_crc_array, no
stored tile to violate anything. §20.3 says so directly — "§21.7 records the
consequence — that this is precisely where the bar has no witness, the live state
being clean" — and §21.7 confirms: "§20.3 step 4's bar on a declaration change is
witnessed only where the affected tiles remain stored … a commit that supersedes
every tile it would have damaged leaves the live state clean, so the bar is
unwitnessed there." No register row.

**Answer: barred; none.** Confidence: high.
