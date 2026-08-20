# Cleanroom round 14 — quiz key transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4168 lines, in four Read calls). I ran `wc -l` and one `grep -n` against that
same file, and two Python computations that read no files (bfloat16 bit pattern,
grid/offset/CRC-free arithmetic). I read no ADRs, no `docs/`, no `conformance/`,
no `spec/registry.json`, no git history, no prior-round transcripts, and I did
not list the output directory. No web access.

---

## Q01 — channel entry for `w`, bfloat16, fill −2.5

§7.4 channel entry layout: `C channel entries | name (u8 len + bytes) · type u16
(0 invalid) · fill (u8 len + bytes)`, with "fill length equals the type's element
size (`[R-CNT-23]`)".

- name: `w` = 0x77, one byte, prefix `01` → `01 77`
- type: bfloat16 = ID 11 (§12.1 table), u16 little-endian (`[R-ENC-01]`) → `0b 00`
- fill: element size 2 (§12.1), so prefix `02`, then the bfloat16 encoding of −2.5.

bfloat16 (`[R-TYP-02]`): "A bfloat16 bit pattern b denotes exactly the value that
the IEEE 754 binary32 bit pattern b × 2¹⁶ (b in the high 16 bits, low 16 bits
zero) denotes." binary32(−2.5) = 0xC0200000 (sign 1, biased exp 0x80, significand
0x200000). High 16 bits = 0xC020. Little-endian → `20 c0`.

Cross-check with §12.1's worked example: bfloat16 1.0 is 0x3F80 stored `80 3F` —
same construction.

Cross-check of entry shape with §12.3's example: `temp`/float32 entry is
`04 74 65 6D 70 0C 00 04 00 00 C0 7F` — name, type LE, fill prefix, fill bytes.

**Answer:** `01 77 0b 00 02 20 c0` (7 bytes).

---

## Q02 — decoded tile image of a planar bool edge tile

Rank 2, dims `r`,`c`, E = (5,5), T = (4,4). Planar, one bool channel, fill byte
0x01 (true).

§11.2: G = (⌈5/4⌉, ⌈5/4⌉) = (2,2). P = ∏Tᵢ = 16.

Layout is planar and the channel is bool → §14.3 packed boolean plane: "value k
occupies bit k mod 8 of byte k div 8 …, and the decoded size is ⌈P/8⌉ bytes."
⌈16/8⌉ = 2 bytes. P mod 8 = 0, so there are **no pad bits**.

Tile coordinates (1,1) covers coordinates 4–7 on both axes (§11.4: tᵢ = xᵢ div Tᵢ).
Extents are 5, so only (4,4) is inside the extents; its in-tile position is
(0,0) (uᵢ = xᵢ mod Tᵢ), in-tile ordinal 0·4 + 0 = 0. It holds **false** → bit 0 = 0.

The other 15 positions are padding positions (§11.3). `[R-SER-05]`: "at every
padding position, a writer MUST encode, for each channel the position carries,
that channel's fill value — … the fill bit in a packed plane." Fill = true → bits
1..15 all 1.

byte 0 = bits 0–7 = 0b1111_1110 = 0xFE; byte 1 = bits 8–15 = 0xFF.

(Structurally the §14.5 worked example — extents (5,5), tiles (4,4), tile (1,1),
one real position and 15 padding — is the same geometry.)

**Answer:** `fe ff`.

---

## Q03 — trailer bytes at offsets 24 and 40

Creation path (`[R-LIF-02]`): front block [0,16); then step 2 payloads/index
beginning at offset 16 → 700 bytes = [16, 716); step 3 directory, dir_length 180
→ dir_offset = 716, directory region [716, 896); step 5 "append the pad to the
next 64-byte boundary" — 896 mod 64 = 0, so the pad is 0 bytes (§6.2: "a writer
that ends its directory on a 64-byte boundary leaves none"); trailer [896, 960).

F = 960; 960 mod 64 = 0 ✓. dir_offset + dir_length = 896 ≤ F − 64 = 896 ✓ (§6.2).

Trailer layout (§6.2): offset 24 = dir_offset (u64), offset 40 =
committed_file_length (u64), both little-endian.

- 716 = 0x2CC → `cc 02 00 00 00 00 00 00`
- 960 = 0x3C0 → `c0 03 00 00 00 00 00 00`

**Answer:** (a) `cc 02 00 00 00 00 00 00`; (b) `c0 03 00 00 00 00 00 00`.

---

## Q04 — total slack bytes

`[R-LIF-08]`/`[R-CNT-02]` claimants of the live state: front block, live trailer,
directory, each record's extent, and the stored extent of each non-sentinel index
entry. "A layer record's extent slot addresses that layer's tile-index region
(§7.4), so the region enters the walk once, as that record's extent, and is not a
second claimant beside it." A record is not a claimant of its own (its header and
inline payload lie inside the directory region).

Tile-index region length under index_encoding 1 (`[R-CNT-17]`):
entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 = 6×20 + 1×4 = 124 → [1000, 1124).

| Claimant | Bytes |
|---|---|
| front signature block [0,16) | 16 |
| live trailer [4032,4096) | 64 |
| directory [3900,4000) | 100 |
| tile-index region [1000,1124) | 124 |
| stored tile [16,216) | 200 |
| stored tile [500,800) | 300 |
| user-metadata extent [2000,2500) | 500 |
| **total claimed** | **1304** |

The other four index entries are sentinels and claim nothing (§15.2, §9.7).

Slack = F − claimed = 4096 − 1304 = **2792**. The walk is complete (nothing
blocks it), so this is a full total, not a partial one (`[R-CNT-21]`).

**Answer:** 2792.

---

## Q05 — inline_length and extent_length

Inline payload fields in §7.4 table order, packed with no padding (`[R-CNT-18]`):

| Part | Bytes |
|---|---|
| name `ab` (1 + 2) | 3 |
| layout u8 + linearization u16 + codec u16 + filter u16 + A u64 + S u64 + A_slab u64 + d u8 + C u16 | 34 |
| 2 dimension entries, each 1+1 name + 8 extent + 8 tile extent = 18 | 36 |
| channel `m` bool: 1+1 name + 2 type + 1 fill-prefix + 1 fill = 6 | 6 |
| channel `v` float64: 1+1 name + 2 type + 1 fill-prefix + 8 fill = 13 | 13 |
| index_encoding u8 + entry_count u64 + crc_of_crc_array u32 | 13 |
| sub-records | 0 |
| **inline_length** | **105** |

Cross-checked against §7.4's worked example, which gives 4 + 34 (name and the
nine scalars) + 18 (dimension entry) + 12 (float32 channel entry) + 13 (trailing
fixed) = 81 — the same decomposition.

Geometry: G = (⌈10/4⌉, ⌈7/4⌉) = (3, 2), N = 6 (§11.2). Layer is **planar**, so the
addressed-tile count is C·N = 2·6 = 12 = entry_count (`[R-GEO-03]`, `[R-CNT-17]`).

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 12×20 + 1×4 = **244**.

**Answer:** (a) 105; (b) 244.

---

## Q06 — disk tile ordinal and index-entry byte offset

E = (100,60,40), T = (32,16,16), C = 4, planar, linearization 1.

G = (⌈100/32⌉, ⌈60/16⌉, ⌈40/16⌉) = (4, 4, 3); N = ∏Gᵢ = 48.

Coordinate (70,33,20): tᵢ = xᵢ div Tᵢ = (2, 2, 1).

`[R-GEO-06]`: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ = 2·(4·3) + 2·(3) + 1 = 24 + 6 + 1 = 31.

Third-declared channel → 0-based channel index c = 2 (§3.1: "a channel's **index**
is its 0-based position in that order").

Planar disk tile ordinal = c·N + s = 2·48 + 31 = **127**.

§15.1: "The entry for the tile with disk ordinal k (§11.4) is the k-th entry, at
region byte 20·k" → 20 × 127 = **2540**.

**Answer:** (a) 127; (b) 2540.

---

## Q07 — decoded-image offset and its filtered position

Interleaved, T = (3,4) → P = 12. Channels `a` int16 (B=2), `b` bool (B=1 in
interleaved, §14.2), `c` float32 (B=4). Sample stride Q = ΣBᵢ = 7; F_c = ΣB_j over
j < c = 2 + 1 = 3.

In-tile coordinates (2,1) → in-tile ordinal u = Σ uᵢ·∏_{j>i}Tⱼ = 2·4 + 1 = 9
(`[R-GEO-06]`; in-tile order is row-major for every linearization).

§14.2's closing sentence: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ" → 9·7 + 3 = **66**.

Filter 2, byte-shuffle (`[R-COD-10]`): stride s = Q = 7 for an interleaved tile.
L = P·Q = 84, n = L/s = 12. "the filtered image places byte i of group j at offset
i · n + j". Decoded offset 66 → group j = 66 div 7 = 9, byte i = 66 mod 7 = 3.
Filtered offset = 3·12 + 9 = **45**. (Inverse check: j·s + i = 9·7 + 3 = 66 ✓.)

**Answer:** (a) 66; (b) 45.

---

## Q08 — verifier verdict

Finding 1 — declined user-metadata decode. Encoding 2 is *assigned*, so the
document rules attach. `[R-MTA-09]`: "A **verifier** that declines to decode a
document on the bound above cannot establish that document's conformance and MUST
NOT certify the file … the decline is not a finding that the file is nonconforming
… it fixes the file's verdict as *cannot establish* only where the verifier
established no violation elsewhere."

Finding 2 — record type 0x8123, MU = 0, PE = 0, flags **bit 5 set**. The
experimental type with MU = 0 is a defined non-violation (§21.6). But bit 5 is a
reserved flag bit. `[R-CNT-12]`: "Reserved flag bits: writers MUST emit zero;
readers MUST ignore them … a verifier MUST treat a nonzero reserved flag bit …
as a validity error at the record's governing scope." Register row F26: "Any of a
non-layer top-level record's reserved flag bits 2-15 is set | verifier |
certification | `[R-CNT-12]`", outcome reject-file. That is an **established
violation**.

`[R-CNF-11]`: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it
was unable to check, and *cannot establish* is available only to a traversal that
established no violation."

The decline is still reported per-requirement, but it does not set the verdict.

**Answer:** `nonconforming`.

---

## Q09 — reader obligation and verifier verdict

Layout: F = 1024; trailer [960,1024) valid; directory [512, 576) valid; one
stored tile at [600,700), i.e. between the directory's end and the live trailer.

(a) Reader on the open path. §19.1's open consumes trailer and directory only.
Trailer gates (`[R-CNT-06]`) all pass: dir_offset 512 ≥ 16, dir_length 64 ≥ 4,
dir_offset + dir_length = 576 ≤ F − 64 = 960, F multiple of 64, etc. The index
entry itself is well-formed under §15.3 (offset ≥ 16; offset + length = 700 ≤
F − 64 = 960), and in any case entries are a tile-use tier, not the open. The
violated rule is `[R-CNT-05]`: "A verifier MUST treat a structure in that gap as a
validity error at file scope … (readers check neither, their check being the
dir-bounds rule of `[R-CNT-06]`)." Register row F7 assigns detector *verifier*,
detected *certification*. So no reader obligation — at open or anywhere.
(`[R-CNF-12]` still *permits* a reader that detects it to reject; permitted is not
obliged.)

(b) The verifier detects F7, an established file-scope violation → verdict
`nonconforming` (`[R-CNF-11]`, `[R-CNF-12]`: "a verifier certifies only
violation-free files").

**Answer:** (a) no; (b) `nonconforming`.

---

## Q10 — two trailer variants of the minimal file

§6.2 valid values: generation "1 ≤ generation ≤ 2⁶³ − 1 (`[R-ENC-03]`)";
file_id "≠ 0". §6.2's reader validation list repeats exactly those two.

**Variant A** — generation = 0x7FFF_FFFF_FFFF_FFFF = 2⁶³ − 1: at the top of the
valid range, inclusive. file_id = 0xFFFF_FFFF_FFFF_FFFF: nonzero, and file_id is
*not* an "offset, length, extent, or count" (§4.2), so `[R-ENC-03]`'s 2⁶³ − 1
domain does not reach it — the trailer table's only constraint is "≠ 0", and F2's
instance list names dir_offset, dir_length, committed_file_length and generation
but never file_id. Every other byte is Appendix A's, and the CRC is recomputed.
→ **accept**. (§9.3's note that such a file "admits no further commit" is a
statement about writers, not readers.)

**Variant B** — generation = 0x8000_0000_0000_0000 = 2⁶³ > 2⁶³ − 1: out of domain.
`[R-CNT-06]`: "Any failure is reject-file." Register rows F2 (u64 count above
2⁶³ − 1, instance *generation*) and the trailer-gate family both carry outcome
reject-file. file_id = 1 is fine, but one failure suffices.
→ **reject**, outcome class **reject-file**.

**Answer:** A: `accept`. B: `reject` — reject-file.

---

## Q11 — the 20 bytes at disk ordinal 5 in generation 8

`[R-WRT-04]` step 4: the layer's stored-tile set changes (ordinal 2 goes from
sentinel to stored), so "Every layer whose stored-tile set or index content this
commit changes has its tile-index region re-emitted in full … with entries for
tiles this commit stores or supersedes written to their new state, entries for
tiles that become unstored written as the sentinel, entries new to this generation
… emitted per §15, and **every other entry byte-identical at its disk-ordinal
position**". Geometry does not change, so `[R-GEO-06]` moves no ordinal.

Ordinal 5 is untouched → byte-identical. Note the oddity: offset = 8 is below 16,
so this entry is a §15.3 *structural* reject-tile (register row T8) — and §20.3
step 2 is explicit that this changes nothing: "a malformed index entry an appender
meets while re-emitting a region is carried forward byte-identically at its
disk-ordinal position under step 4, not repaired to a sentinel."

Bytes (§15.1, little-endian): offset u64 8 → `08 00 00 00 00 00 00 00`;
length u64 0x40 → `40 00 00 00 00 00 00 00`; crc u32 0x11223344 → `44 33 22 11`.

**Answer:** `08 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 44 33 22 11`.

---

## Q12 — the slab-consistent value of X

Interleaved layer, so `[R-SLB-02]` gives a single block [0, N) = [0, 4) with
S = 4 → exactly one run, ordinals 0–3, starting at ordinal 0.

Which entries count as stored tiles for `[R-SLB-03]`?

- Ordinal 0: offset 5 < 16, non-sentinel → §15.3 *structural*: reject-tile (T8).
  `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile on a *structural*
  ground: they address no usable extent, and the run's stored tiles close over
  them." → **transparent**.
- Ordinal 1: offset 1536, length 700, stored bytes fail the crc. `[R-SLB-03]`: "An
  entry whose only defect is that its stored bytes fail its crc is not transparent
  — its offset and length stand, and the packing relation reads them as it does
  any other stored tile's." → **counts**, and it is the run's *first* stored tile.
- Ordinal 2: sentinel → transparent ("Sentinel tiles are transparent to run
  continuity").
- Ordinal 3: offset X, length 40, crc correct → counts.

Invariants: first stored tile's offset mod A_slab = 0 → 1536 mod 512 = 0 ✓ (this
is why ordinal 1, not ordinal 0, must be the aligned one). Packing: "each stored
tile's offset equals the previous stored tile's offset plus its length" →
X = 1536 + 700 = **2236**.

Bounds check: 2236 + 40 = 2276 ≤ F − 64 = 8128 ✓ (§15.3). Codec 3 imposes no
length relation (`[R-COD-08]`'s note).

**Answer:** 2236.

---

## Q13 — which layer's fill byte may change in a commit

`[R-WRT-04]` step 4: "A commit MUST NOT change a layer's declarations in a way
that alters, for any tile that layer stores, what §14 fixes for its stored bytes
or how they decode — the set of padding positions (§11.3) and the content
`[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within
the decoded tile image, or the codec and filter that produced the stored bytes."

Layer P: E = (8,8), T = (4,4) → G = (2,2), Gᵢ·Tᵢ = 8 = Eᵢ on both axes, so **no
padding positions** (§11.3). Interleaved uint8 → no packed plane, so no pad bits.
The fill value therefore fixes nothing inside any stored tile: only unstored tiles
read as fill, and every tile is stored. §20.3's example (c) names this case
exactly: "A change confined to the directory — clearing a slab declaration,
renaming a layer, or **changing a channel's fill value on a layer with no padding
position and no pad bit**." → permitted.

Layer Q: E = (9,8), T = (4,4) → G = (3,2); G₀·T₀ = 12 > 9, so the tiles at t₀ = 2
carry padding positions (coordinates 9, 10, 11 along dim 0). Every addressed tile
is stored, so those tiles are stored, and `[R-SER-05]` fixes their padding bytes
to the recorded fill 0x00. Changing the declaration to 0x07 alters "the content
`[R-SER-05]` fixes there" for stored tiles → barred; §20.3's example (c) again:
"A fill change on a layer carrying either is not an appender's operation at all
(step 4): it would invalidate every stored tile it reaches."

**Answer:** `P only`.

---

## Q14 — reproducible-writer emission order

Appendix G item 3: "For each layer in ascending layer-name byte order: its stored
tiles in disk-ordinal order, then its tile-index region; then any record extents
in ascending record order — all of them after every layer's tiles and index
region, not interleaved with them; then the directory. That order runs over
top-level records first, then, within each layer record, its sub-records."

Layer-name byte order: `a` (0x61) before `b` (0x62).

A layer record's extent *is* its tile-index region (§7.4), already placed by the
per-layer clause, so the "record extents" that remain are the file-scope
user-metadata record's extent (a top-level record, hence first) and layer `a`'s
user-metadata sub-record's extent (a sub-record, hence after the top-level pass;
`b` has none). No alignment and no slab, so no gaps beyond the pre-trailer pad,
and "Each structure begins where the previous one ended".

1. layer `a`'s stored tiles (disk-ordinal order)
2. layer `a`'s tile-index region
3. layer `b`'s stored tiles (disk-ordinal order)
4. layer `b`'s tile-index region
5. the file-scope user-metadata record's extent
6. layer `a`'s user-metadata sub-record's extent
7. the directory region (record sequence plus its CRC)

Seven structures, as the question expects.

---

## Q15 — the T4 conformance vector

The row: §21.4 T4, "A padding position does not encode, for each channel it
carries, that channel's recorded fill value", detector **verifier**, detected
certification, governing rule `[R-SER-05]`, outcome **reject-tile** (§21.4's
heading).

(a) `[R-VEC-04]`: the intact sibling is "another layer, **or another tile of the
same layer where that layer is one a reader is still permitted to serve**". T4's
damage is at tile scope and its detector is the verifier, so the layer is neither
rejected nor barred from service — a reader is still permitted to serve it.
Another tile of the same layer qualifies. → **yes**.

(b) `[R-VEC-04]`: "Where it is the verifier, no reader is obliged to refuse
anything (§21.1), so the pair is the scope at which a verifier confines its
finding … and **the content a reader owes from every scope, the damaged one
included**." `[R-VEC-02]` likewise requires "the decoded content a reader is to
return from every scope it can read". A reader can read the damaged tile — the
defect is in padding positions, which a reader never returns (`[R-GEO-04]`), so
its real sample positions are still owed. → **yes**.

(c) `[R-VEC-02]`: the manifest records, "for each structure the file damages, the
outcome class (§2.4), the scope, and the §21 register row it exercises together
with that row's governing requirement identifier". T4's outcome class is
**reject-tile**.

**Answer:** (a) yes; (b) yes; (c) reject-tile.

---

## Underdetermined?

None of the fifteen. The closest calls, recorded:

- **Q03's pad.** §6.2 allows a longer gap ("a longer gap is conforming, and no
  conforming commit produces one"), but the question stipulates a *conforming
  creator following the commit protocol*, and `[R-LIF-02]` step 5 pads "to the
  next 64-byte boundary" — 896 already is one, so the pad is zero and F = 960 is
  forced. Determinate.
- **Q10's file_id.** §4.2's 0…2⁶³−1 domain is scoped to "every offset, length,
  extent, and count"; file_id is none of those, §6.2 constrains it only as ≠ 0,
  and F2 does not list it. Determinate, though the reading turns on that scoping.
- **Q12's first stored tile.** Turns on ordinal 0 being *structural*-transparent
  while ordinal 1 (crc-failing only) is not — both stated explicitly in
  `[R-SLB-03]` and §15.3. Determinate.
- **Q14's item 5/6 ordering.** The profile's "top-level records first, then,
  within each layer record, its sub-records" is explicit; the only inference is
  that a layer record's own extent is not re-placed, which the per-layer clause
  already placed. Determinate.
