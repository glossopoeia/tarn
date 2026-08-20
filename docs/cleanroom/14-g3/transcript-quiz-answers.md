# Cleanroom round 14 — quiz answerer transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4168 lines, in five `Read` calls, plus two `grep`/`wc` invocations against
that same file). I ran one local Python script that reads no files (arithmetic,
struct packing). I read no ADRs, no `docs/`, no `conformance/`, no
`registry.json`, no git history, no web. I did not read or list the round-14
output directory. Prior format knowledge was used only to raise suspicions;
every answer below is settled against quoted spec text.

---

## Q01 — channel entry for `w`, bfloat16, fill −2.5

§7.4's inline-payload table, channel-entry row:

> `C channel entries | name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes) | type per §12; fill length equals the type's element size (`[R-CNT-23]`)`

So the entry is: name-length u8, name bytes, type u16 LE, fill-length u8, fill bytes.

- name `w` = one ASCII byte 0x77, prefix `01`.
- bfloat16 is sample type **11** (§12.1 table), u16 LE = `0b 00`.
- element size 2 (§12.1), so fill prefix = `02`.
- §12.1 `[R-TYP-02]`: "A bfloat16 bit pattern b denotes exactly the value that
  the IEEE 754 binary32 bit pattern b × 2¹⁶ … denotes."
  binary32(−2.5) = 0xC0200000 (verified by `struct.pack('<f', -2.5)`).
  High 16 bits = 0xC020. Little-endian (§4.1 `[R-ENC-01]`) → `20 c0`.

Cross-check against §12.3's worked `temp` entry
(`04 74 65 6D 70 0C 00 04 00 00 C0 7F`): same field order, same prefixes.

**Answer: `01 77 0b 00 02 20 c0`** (7 bytes). Confidence high.

---

## Q02 — decoded tile image, planar bool, tile (1,1)

Geometry: d=2, dims `r`,`c`, E=(5,5), T=(4,4). G=(⌈5/4⌉,⌈5/4⌉)=(2,2).
P = ∏Tᵢ = 16 (§11.2).

Planar + bool → §14.3 `[R-SER-03]`: "the decoded tile image is the tile's P
values bit-packed LSB-first: value k occupies bit k mod 8 of byte k div 8 …
and the decoded size is ⌈P/8⌉ bytes." ⌈16/8⌉ = **2 bytes**. P mod 8 = 0, so
there are **no pad bits**.

Tile (1,1) covers r ∈ [4,8), c ∈ [4,8). The only coordinate inside the extents
is (4,4), whose in-tile position is (0,0), in-tile ordinal
Σ uᵢ·∏_{j>i}Tⱼ = 0·4 + 0 = **0** (§11.4 `[R-GEO-06]`). That value is false → bit 0 = 0.

The other 15 positions are padding positions (§11.3). §14.5 `[R-SER-05]`:
"at every padding position, a writer MUST encode, for each channel the position
carries, that channel's fill value — … the fill bit in a packed plane."
Fill byte 0x01 = true (§13.2) → fill bit 1.

byte 0 = bits 0..7 = values 0..7 = 0,1,1,1,1,1,1,1 → 0b11111110 = 0xFE
byte 1 = bits 0..7 = values 8..15 = all 1 → 0xFF

(Pattern matches §14.3's worked example, where fill true set the unused bits.)

**Answer: `fe ff`.** Confidence high.

---

## Q03 — trailer bytes at offsets 24 and 40

Layout:
- front block [0, 16)
- payloads + index [16, 716)  (700 bytes)
- directory region [716, 896)  (dir_length 180) → **dir_offset = 716**
- pre-trailer pad: `[R-LIF-02]` step 5 "append the pad to the next 64-byte
  boundary". 896 mod 64 = 0. §6.2: "a writer that ends its directory on a
  64-byte boundary leaves none." → pad = **0 bytes**.
- trailer [896, 960) → **F = committed_file_length = 960**, 960 mod 64 = 0 ✓
- gate check: dir_offset + dir_length = 896 ≤ F − 64 = 896 ✓

§6.2's trailer table: offset 24 = dir_offset (u64), offset 40 =
committed_file_length (u64). Little-endian.

716 = 0x00000000000002CC → `cc 02 00 00 00 00 00 00`
960 = 0x00000000000003C0 → `c0 03 00 00 00 00 00 00`

**Answer: (a) `cc 02 00 00 00 00 00 00`; (b) `c0 03 00 00 00 00 00 00`.**
Confidence high.

---

## Q04 — total slack bytes

§9.7 `[R-LIF-08]` names the claimants: the directory, each record's extent,
the stored extent of each non-sentinel index entry, plus the front block
[0,16) and the live trailer [F−64, F). "A layer record's extent slot addresses
that layer's tile-index region (§7.4), so the region enters the walk once, as
that record's extent." "Bytes the walk does not reach are slack."

Index-region length from `[R-CNT-17]`: entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 6×20 + 1×4 = **124**, so [1000, 1124).

| Claimant | bytes |
|---|---|
| front block [0,16) | 16 |
| live trailer [4032,4096) | 64 |
| directory [3900,4000) | 100 |
| tile-index region [1000,1124) | 124 |
| stored tile [16,216) | 200 |
| stored tile [500,800) | 300 |
| user-metadata extent [2000,2500) | 500 |
| **total claimed** | **1304** |

Slack = F − claimed = 4096 − 1304 = **2792**. The walk is complete (nothing
else is reachable, no rejection), so the total is exact, not partial
(`[R-CNT-21]`).

**Answer: 2792.** Confidence high.

---

## Q05 — inline_length and extent_length

Packing per §7.4 ("fields are packed in table order with no alignment or
padding between them", `[R-CNT-18]`):

| Part | bytes |
|---|---|
| name `ab` (1 prefix + 2) | 3 |
| layout u8 + linearization u16 + codec u16 + filter u16 + A u64 + S u64 + A_slab u64 + rank u8 + C u16 | 34 |
| dim `y` (1+1+8+8) | 18 |
| dim `x` (1+1+8+8) | 18 |
| channel `m` bool (1+1 name, 2 type, 1 fill-prefix, 1 fill) | 6 |
| channel `v` float64 (1+1, 2, 1, 8) | 13 |
| index_encoding u8 + entry_count u64 + crc_of_crc_array u32 | 13 |
| sub-records | 0 |
| **total** | **105** |

The 34 figure is confirmed by §7.4's worked example: "the nine scalars from
layout through channel count occupy 4 + 34 bytes".

(b) Planar ⇒ addressed-tile count = C·N (§11.2 `[R-GEO-03]`).
G = (⌈10/4⌉, ⌈7/4⌉) = (3, 2), N = 6, C = 2 → entry_count = 12.
`[R-CNT-17]`: extent_length = 12×20 + ⌈12/2¹⁶⌉×4 = 240 + 4 = **244**.

**Answer: (a) 105; (b) 244.** Confidence high.

---

## Q06 — disk tile ordinal and index byte offset

G = (⌈100/32⌉, ⌈60/16⌉, ⌈40/16⌉) = (4, 4, 3); N = ∏Gᵢ = 48.

Coordinate (70, 33, 20) → tᵢ = xᵢ div Tᵢ = (2, 2, 1).

§11.4 `[R-GEO-06]`: "the **spatial tile ordinal** of (t₀, …, t_{d−1}) is
s = Σᵢ tᵢ · ∏_{j>i} Gⱼ"
= 2·(4·3) + 2·(3) + 1 = 24 + 6 + 1 = 31.

Planar, third-declared channel ⇒ channel index c = 2 (0-based, §3.1).
"The **disk tile ordinal** … is s for an interleaved layer, and **c · N + s**
for a planar layer" = 2·48 + 31 = **127**.

§15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k … is the k-th
entry, at region byte 20·k" = 20 × 127 = **2540**.

**Answer: (a) 127; (b) 2540.** Confidence high.

---

## Q07 — decoded offset and filtered offset

Interleaved; T=(3,4) ⇒ P = 12. Element sizes: a int16 = 2, b bool = 1
(§14.2: "a bool value … as a single byte … with element size 1 in the
arithmetic below"), c float32 = 4. Q = ΣBᵢ = 7. Decoded size P·Q = 84.

In-tile coords (2,1) → in-tile ordinal u = 2·T₁ + 1 = 2·4 + 1 = 9.
F_c for c = B_a + B_b = 3.
§14.2's closing example: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ" = 9·7 + 3 = **66**.

Filter 2, interleaved ⇒ shuffle stride s = Q = 7 (§17.3 `[R-COD-10]`).
L = 84, n = L/s = 12. Decoded offset 66 lies in group j = 66 div 7 = 9 at
byte i = 66 mod 7 = 3. "the filtered image places byte i of group j at offset
i · n + j" = 3·12 + 9 = **45**.

**Answer: (a) 66; (b) 45.** Confidence high.

---

## Q08 — verifier verdict

Finding 1 — the metadata decline. §18.2 `[R-MTA-09]`: "A **verifier** that
declines to decode a document on the bound above cannot establish that
document's conformance and MUST NOT certify the file … the decline is not a
finding that the file is nonconforming … it fixes the file's verdict as
*cannot establish* only where the verifier established no violation
elsewhere". Its bound of 16 MiB is legitimate (≥ §21.9's 16 MiB guarantee).

Finding 2 — the flags bit. Type 0x8123 is experimental-range; with MU = 0 that
is §21.6's defined non-violation. But §7.2 `[R-CNT-12]`: flags "bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved … a verifier MUST
treat a nonzero reserved flag bit … as a validity error at the record's
governing scope." Bit 5 ∈ 2–15. That is §21.2 row **F26** ("Any of a
non-layer top-level record's reserved flag bits 2-15 is set", verifier,
certification, reject-file) — an **established violation**.

§2.3 `[R-CNF-11]`: "An established violation takes priority: a verifier that
has established any violation reports *nonconforming*, however many
requirements it was unable to check, and *cannot establish* is available only
to a traversal that established no violation."

**Answer: `nonconforming`.** Confidence high.

---

## Q09 — reader obligation and verifier verdict

(a) The open path is §19.1 steps 1–4: trailer gates, directory CRC, record
walk. Every §6.2 gate passes (dir_offset 512 ≥ 16; dir_length 64 ≥ 4;
512+64 = 576 ≤ F−64 = 960; F = 1024 = physical size, multiple of 64). §6.2
`[R-CNT-05]` on the pre-trailer gap: "A verifier MUST treat a structure in
that gap as a validity error at file scope, and counts the rest as slack;
… (**readers check neither**, their check being the dir-bounds rule of
`[R-CNT-06]`)." The stray tile at [600,700) also satisfies every §15.3
per-entry rule (offset ≥ 16; offset+length = 700 ≤ F−64 = 960), and its
checksum verifies — so it is not even a tile-use failure. The reader is
therefore not obliged to reject; `[R-CNF-12]` merely *permits* it to.

(b) The condition is §21.2 row **F7** — "A structure occupies bytes between
the live directory's end and the live trailer | verifier | certification |
`[R-CNT-05]`". The verifier establishes it, so per `[R-CNF-11]` the verdict
is *nonconforming*.

**Answer: (a) no; (b) `nonconforming`.** Confidence high.

---

## Q10 — two trailer variants of the minimal file

§6.2's table and `[R-CNT-06]`'s ordered gate list: "1 ≤ generation ≤ 2⁶³ − 1;
file_id ≠ 0".

**Variant A.** generation = 0x7FFFFFFFFFFFFFFF = 2⁶³ − 1 — exactly the top of
the domain, valid. file_id = 0xFFFFFFFFFFFFFFFF — the only stated constraint
is ≠ 0. file_id is not an offset, length, extent, or count, so `[R-ENC-03]`'s
2⁶³ − 1 ceiling does not reach it; §21.2's F2 instance list ("dir_offset;
dir_length; committed_file_length; generation; … extent_offset;
extent_length") omits file_id, and §23.2 calls it "a stable 64-bit
identifier". Appendix G item 2 derives it from "its low eight digest bytes
read little-endian", which presumes the full 64-bit range. → **accept**.
(§9.3's note that a file at generation 2⁶³ − 1 "admits no further commit"
constrains a future *writer*, not this reader.)

**Variant B.** generation = 0x8000000000000000 = 2⁶³, above the domain →
fails `[R-CNT-06]`'s gate (§21.2 F11's neighbourhood; `[R-ENC-03]` F2).
"Any failure is reject-file." → **reject, reject-file**.

**Answer: A = accept; B = reject reject-file.** Confidence high.

---

## Q11 — the 20 bytes at disk ordinal 5 in generation 8

The commit changes the stored-tile set, so `[R-WRT-04]` step 4 applies:
"Every layer whose stored-tile set or index content this commit changes has
its tile-index region re-emitted in full … and **every other entry
byte-identical at its disk-ordinal position**". Geometry does not change, so
`[R-GEO-06]` moves no ordinal.

Ordinal 5's entry has offset 8, which is < 16 and therefore *structurally*
reject-tile under §15.3 (row "offset < 16 (non-sentinel)"). The appender must
**not** repair it — `[R-WRT-04]` step 2: "a malformed index entry an appender
meets while re-emitting a region is carried forward byte-identically at its
disk-ordinal position under step 4, **not repaired to a sentinel**."

So the bytes are the §15.1 entry layout, little-endian: offset u64 = 8,
length u64 = 0x40, crc u32 = 0x11223344.

**Answer: `08 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 44 33 22 11`.**
Confidence high. (Noting the oddity: the entry the appender must reproduce is
itself invalid.)

---

## Q12 — the slab-satisfying value of X

Interleaved ⇒ one block [0, N) = [0, 4); S = 4 ⇒ a single run covering ordinals
0–3 (§16.2 `[R-SLB-02]`).

- Ordinal 0: offset 5 < 16 → §15.3 *structural* reject-tile. `[R-SLB-03]`:
  "So are the entries §15.3 classifies reject-tile on a *structural* ground:
  they address no usable extent, and the run's stored tiles close over them."
  → transparent.
- Ordinal 1: offset 1536, length 700; only its stored bytes fail the crc.
  `[R-SLB-03]`: "An entry whose only defect is that its stored bytes fail its
  crc is **not** transparent — its offset and length stand, and the packing
  relation reads them as it does any other stored tile's." So ordinal 1 is the
  run's **first stored tile**: 1536 mod A_slab(512) = 0 ✓.
- Ordinal 2: sentinel — "Sentinel tiles are transparent to run continuity".
- Ordinal 3: "each stored tile's offset equals the previous stored tile's
  offset plus its length" → X = 1536 + 700 = **2236**.

Bounds sanity: 2236 ≥ 16, 2236 + 40 = 2276 ≤ F − 64 = 8128 ✓. Only the run's
*first* stored tile carries the A_slab constraint, so X need not be
512-aligned (2236 mod 512 = 188).

**Answer: 2236.** Confidence high.

---

## Q13 — which layer's fill byte may be changed

`[R-WRT-04]` step 4: "A commit MUST NOT change a layer's declarations in a way
that alters, for any tile that layer stores, what §14 fixes for its stored
bytes or how they decode — **the set of padding positions (§11.3) and the
content `[R-SER-05]` fixes there**, the decoded size, …"

- **Layer P**: E=(8,8), T=(4,4) → G=(2,2); G·T = 8 = E on both axes, so
  Gᵢ·Tᵢ > Eᵢ nowhere: **no padding positions**. Interleaved uint8, so no
  packed plane and no pad bits either. The fill byte reaches nothing about any
  stored tile. §20.3's example (c) names precisely this case: "A change
  confined to the directory — clearing a slab declaration, renaming a layer,
  or **changing a channel's fill value on a layer with no padding position and
  no pad bit**." → permitted.
- **Layer Q**: E=(9,8), T=(4,4) → G=(3,2); 3·4 = 12 > 9, so the tiles at
  t₀ = 2 carry padding positions at coordinates 9, 10, 11 along dim 0. Every
  addressed tile is stored, so those tiles are stored, and `[R-SER-05]` fixes
  their padding bytes to the *recorded* fill. Changing 0x00 → 0x07 makes each
  such stored tile nonconforming. §20.3 again: "A fill change on a layer
  carrying either is not an appender's operation at all (step 4)." → barred.

**Answer: `P only`.** Confidence high.

---

## Q14 — the reproducible-writer emission order

Appendix G item 3: "**A total emission order, contiguously.** For each layer in
ascending layer-name byte order: its stored tiles in disk-ordinal order, then
its tile-index region; then any record extents in ascending record order — all
of them after every layer's tiles and index region, not interleaved with them;
then the directory. That order runs over top-level records first, then, within
each layer record, its sub-records."

Layer-name order: `a` (0x61) before `b` (0x62). Each layer record's own extent
*is* its tile-index region, already placed in the per-layer pass; the
remaining record extents are the two user-metadata documents. Record order:
top-level first (the file-scope user-metadata record), then, within each layer
record, its sub-records (layer `a`'s user-metadata sub-record; `b` has none).

1. layer `a`'s stored tiles (disk-ordinal order)
2. layer `a`'s tile-index region
3. layer `b`'s stored tiles (disk-ordinal order)
4. layer `b`'s tile-index region
5. the file-scope user-metadata record's extent
6. layer `a`'s user-metadata sub-record's extent
7. the directory region (record sequence + its CRC)

No alignment or slab is declared, so no gaps intrude (item 3: "Each structure
begins where the previous one ended, save where alignment forces a gap").

**Answer: the seven items above, in that order.** Confidence high; the one
soft spot is whether the file-scope extent precedes the layer sub-record
extent — the sentence "runs over top-level records first, then, within each
layer record, its sub-records" settles it.

---

## Q15 — the T4 conformance vector

The row is §21.4 **T4**: "A padding position does not encode, for each channel
it carries, that channel's recorded fill value | … | verifier | certification |
`[R-SER-05]`", outcome reject-tile (§21.4's heading).

(a) `[R-VEC-04]`: "Every vector whose recorded outcome is reject-layer or
reject-tile is built inside a file that also carries an **intact sibling** —
another layer, **or another tile of the same layer where that layer is one a
reader is still permitted to serve**". T4's damage is confined to tile scope
and its detector is the verifier, so the layer is fully serviceable by a
reader. → **yes**.

(b) `[R-VEC-04]` continues: "Where it is the **verifier**, no reader is obliged
to refuse anything (§21.1), so the pair is the scope at which a verifier
confines its finding … and **the content a reader owes from every scope, the
damaged one included**." §21.1 reinforces it: for verifier rows "the outcome
names the scope at which the damage is recorded, not an obligation on any
reader". And a reader never returns padding positions anyway (`[R-GEO-04]`),
so the damaged tile's real samples are content a reader still owes. → **yes**.

(c) `[R-VEC-02]`: the manifest records "for each structure the file damages,
the **outcome class** (§2.4), the scope, and the §21 register row it exercises
together with that row's governing requirement identifier". T4's outcome class
is **reject-tile**.

**Answer: (a) yes; (b) yes; (c) reject-tile.** Confidence high for (a) and
(c); medium-high for (b) — the phrase "the damaged one included" is explicit,
so I take it as determined.

---

## Underdetermined questions

None of the fifteen. I looked hardest at Q03 (whether a directory already
ending on a 64-byte boundary takes a 0-byte or a 64-byte pad — §6.2 settles it
explicitly), Q10-A (whether file_id inherits `[R-ENC-03]`'s 2⁶³ − 1 ceiling —
three independent places show it does not), and Q14's item-5/6 ordering. Each
resolved on quoted text.
