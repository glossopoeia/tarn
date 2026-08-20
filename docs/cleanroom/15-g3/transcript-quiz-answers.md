# Cleanroom round 15 — quiz answerer transcript

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(entire file, lines 1–4227, in six Read calls). Ran one `rg` against that same
file to confirm where `[R-SLB-04]` is cited. Ran three Python computations that
read no files (a CRC-32C implementation validated against the spec's own three
published constants, plus geometry/offset arithmetic). Read no ADR, no
`docs/`, no `conformance/`, no `registry.json`, no git history, no web. Did not
list or read the output directory.

CRC implementation validation (§4.5 check vector, §15.4 constant, §7.4 example):

- CRC-32C(`"123456789"`) = 0xE3069283 ✓
- CRC-32C(zero bytes) = 0x00000000 ✓
- CRC-32C(2^16 sentinel entries) = 0xEECB3BB2 ✓
- §7.4's example: 4 sentinel entries → 0x80A34955; its 4-byte array → 0xC4EE982E ✓

---

## Q01 — committed_file_length and dir_length of the minimal one-layer file

**Inline payload size.** §7.4's table, in order, plus §7.4's own worked example
("Name and the nine scalars from layout through channel count occupy 4 + 34
bytes, the dimension entry 18, the channel entry 12, and the trailing fixed
fields 13 — 81 exactly"), which pins each group:

| Group | Bytes |
|---|---|
| name `z` (u8 len + 1 byte) | 2 |
| nine scalars: layout 1, linearization 2, codec 2, filter 2, A 8, S 8, A_slab 8, d 1, C 2 | 34 |
| 1 dimension entry: name 2 + extent 8 + tile extent 8 | 18 |
| 1 channel entry: name 2 + type 2 + fill (1 len + 1 byte, uint8 element size 1) | 6 |
| trailing fixed: index_encoding 1 + entry_count 8 + crc_of_crc_array 4 | 13 |
| sub-records | 0 |

inline_length = 2 + 34 + 18 + 6 + 13 = **73**.

**Consistency of the declaration.** Dimension `t` has extent 0, tile extent 1 →
G = ⌈0/1⌉ = 0 (§11.2), N = 0, interleaved so addressed-tile count = N = 0
(`[R-GEO-03]`), entry_count = 0, extent slot (0,0) and crc_of_crc_array = 0
(§7.4, `[R-CNT-17]`, `[R-CNT-23]`). No tile-index region exists (§15.4's
example: "At entry_count = 0 there is no region at all"). So the layer record is
the only structure besides the directory.

**Directory region.** Record = 24-byte header (§7.2) + 73 = 97 bytes. §7.1: the
region's "final 4 bytes are a CRC-32C over the preceding dir_length − 4 bytes;
those covered bytes are the record sequence itself". dir_length = 97 + 4 = **101**.

**Placement.** Smallest permitted dir_offset is 16 (`[R-CNT-06]`: "dir_offset ≥
16"; §5.1: "a directory of at least 4 bytes at an offset of at least 16"). So the
region is [16, 117).

**F.** `[R-CNT-06]`: dir_offset + dir_length ≤ F − 64, and committed_file_length
is a multiple of 64. 117 ≤ F − 64 → F ≥ 181 → smallest multiple of 64 is
**192**. That is also exactly what `[R-LIF-02]` step 5 produces: pad from 117 to
the next 64-byte boundary (128), then the 64-byte trailer at [128, 192). 192 ≥
the 128-byte floor of `[R-CNT-27]`.

**(a) 192  (b) 101**

---

## Q02 — segment CRC array and crc_of_crc_array bytes

§15.1: region = entry array (3 × 20 = 60 bytes) then segment CRC array
(⌈3/2¹⁶⌉ × 4 = 4 bytes). §15.4: "the s-th u32 of the segment CRC array is the
CRC-32C over exactly those entries' bytes as stored — the final partial segment's
CRC covers only its actual bytes." One partial segment covering all 3 entries, so
it is computed over all 60 bytes (§15.4 also forbids substituting 0xEECB3BB2:
that constant is only for *full* segments, and this segment is neither full nor
all-sentinel).

Entry bytes (§15.1 layout, §15.2 sentinel, `[R-ENC-01]` little-endian):

```
entry 0  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00
entry 1  00 10 00 00 00 00 00 00  18 00 00 00 00 00 00 00  44 33 22 11
entry 2  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00
```

CRC-32C over those 60 bytes = 0x5DAE66CD → stored little-endian as `cd66ae5d`.
CRC-32C over that 4-byte array = 0x884CB519 → stored little-endian as `19b54c88`
(§4.5: "stored as a little-endian `u32`"; §8.1: the segment CRC array is "itself
covered by the layer record's crc_of_crc_array").

**(a) cd66ae5d  (b) 19b54c88**

---

## Q03 — stored bytes of a planar bool tile

G_y = ⌈3/3⌉ = 1, G_x = ⌈2/3⌉ = 1, N = 1, P = 3·3 = 9. Planar bool → §14.3:
"the decoded tile image is the tile's P values bit-packed LSB-first: value k
occupies bit k mod 8 of byte k div 8 … the decoded size is ⌈P/8⌉ bytes" = 2 bytes.
Codec 1 and filter 1 → stored bytes = decoded image (§17.2 codec 1; §17.3 filter
1; and for a packed bool plane the shuffle would be the identity anyway).

In-tile ordinal = u_y·T_x + u_x = 3u_y + u_x (§11.4).

| k | (u_y,u_x) | status | bit |
|---|---|---|---|
| 0 | (0,0) | real, 0+0 even | 1 |
| 1 | (0,1) | real, odd | 0 |
| 2 | (0,2) | padding (x=2 ≥ E_x=2) → fill bit | 0 |
| 3 | (1,0) | real, odd | 0 |
| 4 | (1,1) | real, even | 1 |
| 5 | (1,2) | padding → fill | 0 |
| 6 | (2,0) | real, even | 1 |
| 7 | (2,1) | real, odd | 0 |
| 8 | (2,2) | padding → fill | 0 |

`[R-SER-05]`: "at every padding position, a writer MUST encode … the fill bit in
a packed plane. Every pad bit (§14.3) MUST carry the plane's channel's fill bit."
Fill is 0x00 = false, so all padding positions and all pad bits are 0.

Byte 0 = bits 0,4,6 set = 0x01 + 0x10 + 0x40 = 0x51. Byte 1 = bit 0 (ordinal 8) =
0, pad bits 1–7 = fill = 0 → 0x00.

**5100**

---

## Q04 — interleaved decoded size and in-tile byte offset

§14.2: interleaved decoded size = P · Q, offset of value k = (k div C)·Q + F_{k mod C}.

P = 3·5 = 15 (§11.2). Q = Σ B_i = 1 (uint8) + 8 (float64) + 2 (bfloat16) = 11
(§12.1 element sizes). Decoded size = 15 · 11 = **165**.

Channel `c` has index 2, F_c = 1 + 8 = 9. In-tile ordinal of (2,3) = 2·5 + 3 = 13
(§11.4, in-tile order row-major for every linearization). §14.2's closing example
states the direct form: "channel c's value at in-tile ordinal u sits at byte
u · Q + F^c". 13 · 11 + 9 = 143 + 9 = **152**.

**(a) 165  (b) 152**

---

## Q05 — byte offset of a planar tile's index entry

G_z = ⌈5/2⌉ = 3, G_y = ⌈9/4⌉ = 3, G_x = ⌈20/8⌉ = 3 → N = 27 (§11.2).

Tile coordinates t_i = x_i div T_i: t_z = 3 div 2 = 1, t_y = 7 div 4 = 1,
t_x = 17 div 8 = 2 (§11.4).

Spatial ordinal s = Σ t_i · ∏_{j>i} G_j = 1·(3·3) + 1·3 + 2 = 14.

Channel `r` is index 2 (declared third). Planar disk ordinal = c·N + s =
2·27 + 14 = 68 (`[R-GEO-06]`).

§15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
byte 20·k." 20 · 68 = **1360**.

---

## Q06 — extent_length and last segment's entry count

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4.
65,537 × 20 = 1,310,740. ⌈65537/65536⌉ = 2 → +8. Total **1,310,748**.

§15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))". Last
segment is s = 1: [65,536, min(131,072, 65,537)) = [65,536, 65,537) = **1** entry.

**(a) 1310748  (b) 1**

---

## Q07 — exact slack total

Layer's tile-index region length = 5 × 20 + ⌈5/2¹⁶⌉ × 4 = 104 (`[R-CNT-17]`), so
it occupies [512, 616).

Claimants of the live committed state (§5.2, §9.7 — front block and live trailer
are claimed by the walk; a record is not a claimant of its own, its header and
inline payload lying inside the directory region):

| Claimant | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile | [16, 216) | 200 |
| stored tile | [256, 356) | 100 |
| stored tile | [384, 448) | 64 |
| user-metadata record extent | [448, 488) | 40 |
| tile-index region | [512, 616) | 104 |
| directory region | [640, 736) | 96 |
| live trailer | [960, 1024) | 64 |

All disjoint; each non-front/trailer claimant lies within [16, 960) = [16, F−64).
Sum = 684. Slack = F − 684 = 1024 − 684 = **340**.

The two sentinel entries contribute no extent (§15.2, §9.7).

---

## Q08 — partial slack figure after an established layer-scope overlap

§5.2 `[R-CNT-21]`: "Where the walk of §9.7 does not enumerate every region's
claimants — whether because a scope-level rejection ends that scope's enumeration
(a rejected layer's claimants are not enumerated … and where the rejection is one
the walk itself established, L18's overlap or L40 through L42's placement among
them, **the claimants it had already enumerated are discarded with the layer**
…) … the verifier MUST report the total as partial. A partial total is F less the
bytes claimed by the claimants the walk did enumerate."

The overlap is L18 (two structures of one and the same layer), established by the
walk, at layer A's scope → all of layer A's claimants are discarded: its index
region (44) and both stored extents (100 + 100) = 244.

Claimants that survive: front 16 + directory 128 + layer B index 24 + layer B
stored extent 200 + trailer 64 = 432.

Partial total = 2048 − 432 = **1616**. (Note it is an over-count of true slack,
which is what `[R-CNT-21]` calls "an upper bound on the file's true slack, never
an under-count".)

The verifier did *not* elect to stop early, but the scope-level rejection is
independently a reason the walk did not complete, so the figure is **partial**,
and the verifier "MUST say which scope or violation stopped the walk".

**(a) 1616  (b) partial**

---

## Q09 — slab offset, and the outcome when it is wrong

N = ⌈128/32⌉ = 4; interleaved → 4 addressed tiles ✓ entry_count. P = 32, Q = 1,
decoded size 32; codec 1 requires length = 32 (`[R-COD-04]`) ✓.

Entry classification (§15.3):
- entry 0: non-sentinel, well-formed stored tile at 4096, length 32.
- entry 1: offset = S, length ≠ S → *structural*: reject-tile.
- entry 2: non-sentinel, well-formed stored tile at X, length 32.
- entry 3: offset = S, length = S, crc 0 → valid sentinel.

§16.2 `[R-SLB-02]`: interleaved → single block [0, N) = [0, 4); run 0 starts at
ordinal 0 and S = 4, so all four ordinals are one run.

`[R-SLB-03]`: "the run's stored tiles are contiguous and packed in ordinal order —
each stored tile's offset equals the previous stored tile's offset plus its
length — and the first stored tile's offset satisfies offset mod A_slab = 0.
… Sentinel tiles are transparent to run continuity … So are the entries §15.3
classifies reject-tile on a *structural* ground."

Entry 1 (structural) and entry 3 (sentinel) are transparent. First stored tile is
entry 0: 4096 mod 64 = 0 ✓. Next stored tile is entry 2, so
X = 4096 + 32 = **4128**.

(b) X = 4160 leaves a 32-byte gap inside the run. §21.3 row **L41**: "Inside a
slab run, a stored tile's offset ≠ the previous stored tile's offset plus that
tile's length (gap, overlap, or out-of-ordinal placement; sentinels and entries
§15.3 classifies reject-tile on a structural ground are transparent …)" —
Detector *verifier*, outcome **reject-layer** (§21.3 header: "Outcome:
reject-layer"; §15.3's last-but-one row: "alignment or slab invariant violated
(§16) | *verifier*: reject-layer"). Not L42: entry 0's offset *is* A_slab-aligned.

**(a) 4128  (b) reject-layer, L41**

---

## Q10 — compactor facing one tile whose bytes fail its entry crc

`[R-WRT-09]`: a compactor "MUST verify each link of the chain — the open (§19.1),
each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and
each relocated extent's checksum, **including every stored tile's entry crc** —
before emitting that structure's bytes."

`[R-WRT-06]`: "A compactor MUST refuse to compact when any check `[R-WRT-09]`
obliges fails, and MUST NOT emit a file carrying a violation it has detected: it
can neither drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
(`[R-WRT-05]`)."

That closes (i) (emitting a detected violation), (iii) (re-emitting corrected —
and `[R-WRT-07]` fixes "entry lengths, entry crcs, and sentinel entries
unchanged"), and (ii) (§20.4: "No commit therefore removes a layer record …
compaction … carries every layer of its input forward (§20.5)").

**(iv)**

---

## Q11 — compactor and a slab-declared layer

(a) `[R-WRT-06]`: "Given a conforming input the output is a conforming file. A
compactor satisfies every writer requirement for the bytes it produces." The
output layer record still declares S = 8, A_slab = 4096 (see (b)), so
`[R-SLB-03]`'s contiguity and alignment invariants bind the output's placement;
violating them is L41/L42, reject-layer. **no**

(b) `[R-WRT-07]`: "A compactor preserves content but not placement … and every
retained record per §20.4, **except that** relocation re-points extent slots,
regenerates each relocated tile-index region (entry offsets new; entry lengths,
entry crcs, and sentinel entries unchanged; segment CRCs recomputed over the
entries as re-emitted), and updates the layer-record fields covering a
regenerated region (crc_of_crc_array)." That `except` list is closed, and
`[R-WRT-05]` otherwise requires byte-identical re-emission of every retained
record. Clearing S/A_slab is not among the permitted changes.

`[R-SLB-04]`'s either/or ("re-establish the invariants … or clear the
declaration in the new generation") is scoped to a *commit* — and §9.1 makes
compaction a whole-file rewrite rather than a commit; the spec cites
`[R-SLB-04]` only at §20.3 step 4 (the appender's path), never in §20.5. So the
compactor's only route is to re-establish the invariants. **no**

**(a) no  (b) no**

---

## Q12 — directory offset under Appendix G's profile

Appendix G item 3: "The first structure begins at 16, directly after the front
signature block … each later structure begins where the previous one ended, save
where alignment forces a gap" (none: no A, no A_slab; the 64-byte trailer
alignment and pre-trailer pad come *after* the directory).

Order: "For each layer in ascending layer-name byte order: its stored tiles in
disk-ordinal order, then its tile-index region; then any record extents in
ascending record order — all of them after every layer's tiles and index region,
not interleaved with them; then the directory."

`a` (0x61) precedes `b` (0x62).

Index region sizes (`[R-CNT-17]`): layer `a`, entry_count 2 → 2×20 + 4 = 44;
layer `b`, entry_count 1 → 1×20 + 4 = 24.

| Structure | Range |
|---|---|
| `a` tile, disk ordinal 0 (30 B) | [16, 46) |
| `a` tile, disk ordinal 1 (40 B) | [46, 86) |
| `a` tile-index region (44 B) | [86, 130) |
| `b` tile (50 B) | [130, 180) |
| `b` tile-index region (24 B) | [180, 204) |
| user-metadata extent (60 B) | [204, 264) |
| directory | begins at **264** |

**264**

---

## Q13 — unimplemented experimental MU = 1 sub-record

Type 0x9000 ≥ 0x8000 → experimental range (§10.2's record-type row).

(a) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never
reject-file". §2.4's vocabulary names it **reject-layer**.

(b) §2.3: a verifier reports *cannot establish* "where some requirement is one it
is unable to check on a capability or resource ground, as when the file names a
format major version it does not implement, **when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)**". §21.6 confirms
the file is conforming ("an experimental-range record type carrying MU = 1 …
`[R-CNF-02]` makes the file conforming all the same"), so no violation is
established, and *cannot establish* "is available only to a traversal that
established no violation" — which this one is.

**(a) reject-layer  (b) cannot establish**

---

## Q14 — verdicts for encoding 0x85 vs 0x05

§18.2 `[R-MTA-03]`: "0 is invalid; 1 = none and 2 = zstd are assigned; 3 through
0x7F are reserved; values ≥ 0x80 are the experimental range".

**File A (0x85, experimental).** §21.6: "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file
is conforming — §10.3's prohibition binds a writer's conduct, not the bytes. No
document rule attaches at such an encoding, so a verifier certifies, reporting
the record it ignored." `[R-MTA-10]`: "A verifier meeting such a record in an
otherwise conforming file has no requirement it is unable to check … and
certification is unaffected." Verdict: **conforming** (with a report line naming
the scope, encoding value 0x85, and extent length 200).

**File B (0x05, reserved).** §21.5 row **R1**: "A user-metadata record declares a
document encoding of 0, or a reserved-range value (3-0x7F)". §21.5's header:
"Every row here is a violation all the same: the outcome bounds a reader's blast
radius and never makes the file conforming (`[R-CNF-12]`)", and §21.5 adds
explicitly "what `[R-MTA-10]` withdraws is the document's content rules, never
the encoding byte's own value set". An established violation forces
*nonconforming* (§2.3). Verdict: **nonconforming**.

**A = conforming, B = nonconforming**

---

## Q15 — changing filter 1 → 2 on a planar uint8 layer with stored tiles

§20.3 step 4 `[R-WRT-04]`: "A commit MUST NOT change a layer's declarations in a
way that alters, for any tile that layer stores **in the generation this commit
supersedes**, what §14 fixes for its stored bytes or how they decode — … or the
codec and filter that produced the stored bytes."

But the same step qualifies it: "The test is the effect on such a tile, and the
list names where that effect arises rather than standing on its own: **a change
that leaves every one of those tiles' stored bytes meaning exactly what they
meant — a filter whose mandated stride makes it the identity (`[R-COD-10]`)** …
— is not what this bars."

`[R-COD-10]`: "The shuffle stride s is the channel's element size for a planar
tile … Viewing the image as n = L/s consecutive groups of s bytes, the filtered
image places byte i of group j at offset i · n + j."

Layer L is planar with one uint8 channel → element size 1 → s = 1 → every group
is one byte, i is always 0, and byte 0 of group j lands at 0·n + j = j. The
filter is the identity, so each stored tile's bytes decode to exactly the image
they decoded to under filter 1.

Nothing else changes: geometry (64,64)/(16,16) gives G = (4,4), N = 16, exactly
the 16 addressed tiles, no padding positions, decoded size P = 256 unchanged;
codec unchanged; extent slot, index entries and every other record re-emitted
byte-identically (`[R-WRT-05]`).

**permitted**
