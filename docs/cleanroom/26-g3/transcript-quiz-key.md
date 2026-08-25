# Round 26 — quiz keyer transcript

Access: read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole file, in five Read calls). Local Python for CRC-32C and arithmetic;
no other file read, no git, no web.

## CRC implementation validation

Before answering, I implemented CRC-32C (reflected, poly 0x82F63B78 reversed
form, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against every
constant the document publishes:

- §4.5 check vector: CRC-32C("123456789") = 0xE3069283 ✓; CRC-32C(zero bytes)
  = 0x00000000 ✓
- §15.4: CRC-32C of 2¹⁶ sentinel entries = 0xEECB3BB2 ✓
- §7.4 example: CRC over 4 sentinel entries (80 bytes) = 0x80A34955 ✓, and
  crc_of_crc_array over `55 49 A3 80` = 0xC4EE982E ✓
- Appendix A: trailer CRC over trailer bytes [0,60) = 0xE00938D2 ✓
- §17.3 shuffle example (float32 1.0/2.0/3.0, s=4, n=3) reproduces
  `00 00 00 00 00 00 80 00 40 3F 40 40` ✓

All five reproduce, so the CRC routine, the sentinel byte layout, the trailer
field layout, and the shuffle direction are all corroborated against the
document's own worked numbers.

---

## Q01

Layer record inline payload field order and widths from §7.4's table.
Widths: name = u8 len + bytes; layout u8; linearization u16; codec u16;
filter u16; A u64; S u64; A_slab u64; rank u8; C u16; each dimension entry =
u8 len + name bytes + u64 extent + u64 tile extent; each channel entry =
u8 len + name bytes + u16 type + u8 fill len + fill bytes; index_encoding u8;
entry_count u64; crc_of_crc_array u32; then sub-records.

Offsets (name `ab`, d = 2, C = 2):

```
 0      01+2   name: len 1 byte + "ab"          -> 0..2   (3)
 3      u8     layout 2                          -> 3
 4      u16    linearization 1                   -> 4..5
 6      u16    codec 3                           -> 6..7
 8      u16    filter 2                          -> 8..9
10      u64    A = 0                             -> 10..17
18      u64    S = 4                             -> 18..25
26      u64    A_slab = 4096                     -> 26..33
34      u8     rank d = 2                        -> 34
35      u16    C = 2                             -> 35..36
37      dim `y` 1+1+8+8 = 18                     -> 37..54
55      dim `x` 1+1+8+8 = 18                     -> 55..72
73      chan `u` uint16 1+1+2+1+2 = 7            -> 73..79
80      chan `b` bool   1+1+2+1+1 = 6            -> 80..85
86      u8     index_encoding 1                  -> 86
87      u64    entry_count                       -> 87..94
95      u32    crc_of_crc_array                  -> 95..98
```

Total 99 bytes, no sub-records → **inline_length = 99**.

Cross-check against §7.4's worked example: there the name is 4 bytes and
"the nine scalars from layout through channel count occupy 4 + 34 bytes",
dimension entry 18, channel entry 12 (float32: 1+4+2+1+4), trailing fixed
fields 13 (1+8+4). Here: 3 + 34 = 37, dims 36, channels 7 + 6 = 13,
trailing 13 → 99. Same decomposition.

entry_count: §11.2 `[R-GEO-03]` — "The layer's addressed-tile count … is N
for an interleaved layer and C · N for a planar layer". G_y = ⌈10/4⌉ = 3,
G_x = ⌈9/4⌉ = 3, N = 9, C = 2, layout 2 = planar → **entry_count = 18**.

extent_length: `[R-CNT-17]` — "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4". 18·20 + 1·4 = 360 + 4 = **364**.

entry_count field begins at inline-payload offset **87**.

(A = 0 with S = 4 is fine: `[R-CNT-16]` bars only A ≠ 0 together with S ≠ 0.)

**Answer: 99, 18, 364, 87.** Confidence high.

## Q02

§6.2 layout table: magic [0,8); version_major [8,10); version_minor [10,12);
flags [12,16); generation [16,24); dir_offset [24,32); dir_length [32,40);
committed_file_length [40,48); file_id [48,56); reserved [56,60); trailer CRC
[60,64) = "CRC-32C over trailer bytes [0, 60)", stored little-endian
(`[R-ENC-09]`).

Bytes [0,60):
```
8A 4E 52 41 54 0D 0A 1A  01 00  00 00  00 00 00 00
03 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
44 00 00 00 00 00 00 00  C0 00 00 00 00 00 00 00
EF BE AD DE 00 00 00 00  00 00 00 00
```
CRC-32C = 0xF3566CE6, stored little-endian as `E6 6C 56 F3`.

**Answer: `e66c56f3`.** Confidence high.

## Q03

Interleaved, `a` uint8 (B=1), `b` int16 (B=2) → Q = ΣBᵢ = 3 (§14.2).
Decoded image is 12 bytes, and §14.2 gives decoded size P·Q, so P = 4.

Filter first, then codec (§17.1 `[R-COD-01]`): "the layer's filter (§17.3),
then its codec (§17.2)". Shuffle stride for an interleaved tile is Q = 3
(`[R-COD-10]`), n = L/s = 12/3 = 4.

Groups: (41 02 01)(07 FE FF)(07 FE FF)(07 FE FF).
Byte i of group j goes to offset i·n + j:
- i=0 → 41 07 07 07 (offsets 0–3)
- i=1 → 02 FE FE FE (offsets 4–7)
- i=2 → 01 FF FF FF (offsets 8–11)

Codec 1 (none): "The stored bytes are the filtered image verbatim"
(`[R-COD-04]`), so stored bytes = `41 07 07 07 02 FE FE FE 01 FF FF FF`.

Length field: `[R-COD-04]` — "The index entry's length therefore MUST equal
the tile's decoded size" = 12.

crc field: §15.1 — "CRC-32C of the stored tile's bytes". CRC-32C of those 12
bytes = 0x2B8A45D7, stored little-endian `D7 45 8A 2B`.

**Answer: `4107070702fefefe01ffffff`; 12; `d7458a2b`.** Confidence high.

## Q04

G_y = ⌈1000/128⌉ = 8, G_x = ⌈500/128⌉ = 4, N = 32 (§11.2).
Planar, C = 3 → entry_count = C·N = **96**.
extent_length = 96·20 + ⌈96/65536⌉·4 = 1920 + 4 = **1924** (`[R-CNT-17]`).

§11.4 `[R-GEO-06]`: tᵢ = xᵢ div Tᵢ → t_y = 400 div 128 = 3, t_x = 300 div 128
= 2. "the spatial tile ordinal … is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" = 3·G_x + 2 =
3·4 + 2 = 14. "The disk tile ordinal … is … c · N + s for a planar layer",
c = 2 for `b` (0-based, §3.1) → 2·32 + 14 = **78**.

§15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k … is at
region byte 20·k" → 20·78 = **1560**.

**Answer: 96, 1924, 78, 1560.** Confidence high.

## Q05

§9.7 `[R-LIF-08]` names the claimants: the directory, each record's extent,
each non-sentinel entry's stored extent, plus "The front signature block at
[0, 16) and the live trailer at [F − 64, F) are claimed by the walk as well".
"A record is not a claimant of its own — its header and inline payload lie
inside the directory region". The layer record's extent slot addresses the
tile-index region, so that region "enters the walk once, as that record's
extent".

Claimed: front 16 + index region [16,60) 44 + tile [64,164) 100 +
tile [200,300) 100 + directory [848,960) 112 + trailer [960,1024) 64 = 436.

(Consistency check: entry_count = 2 → extent_length = 2·20 + 4 = 44 = the
declared [16,60). ✓)

Slack = 1024 − 436 = 588. By regions: [60,64) 4 + [164,200) 36 +
[300,848) 548 = 588. The walk completes, so the total is exact, not partial
(`[R-CNT-21]`).

**Answer: 588.** Confidence high.

## Q06

(a) §7.1 `[R-CNT-25]`: "An extent of (0, 0) on a user-metadata record, or one
whose extent_length is less than 5 … is a validity error at its containing
scope." Top-level → file → **reject-file** (register F21).

(b) extent_length 4 < 5 → same sentence → **reject-file** (F22).

(c) inline byte 0x00 = encoding 0. `[R-CNT-25]`: "An encoding value of 0, or
one the reader does not implement, makes that record unreadable, with the
same outcome as a failed CRC — ignore-record." Register R1 lists encoding 0
explicitly → **ignore-record**.

(d) §18.2 `[R-MTA-03]`: "A record whose inline_length is not 1 is a validity
error at the record's containing scope." Top-level → **reject-file** (F23,
instance "inline_length ≥ 2").

**Answer: reject-file, reject-file, ignore-record, reject-file.** High.

## Q07

0x9F ≥ 0x80 → experimental range of the metadata-encoding space (§10.2,
§18.2).

§21.6 row: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming … No
document rule attaches at such an encoding, so a verifier certifies,
reporting the record it ignored."

§2.3 confirms this is not a cannot-establish ground: "A user-metadata
document under an encoding this specification does not assign is not such a
ground: no content rule attaches there, so nothing is left unchecked, and
certification is unaffected." `[R-MTA-10]` says the same and obliges the
verifier to report the record it ignored — a report constraint, not a verdict
constraint.

**Answer: conforming; ignore-record.** Confidence high.

## Q08

(1) §9.6 `[R-LIF-06]`: "The probe begins at the largest 64-aligned offset o
with o + 64 ≤ the physical file length." Physical length 640; 576 + 64 = 640
≤ 640 → **576**.

(2) The candidate at 448: CRC verifies but §9.6 requires
"committed_file_length = o + 64", and 576 ≠ 512 → not a valid candidate.
Continue backward. At 256: CRC verifies and committed_file_length = 320 =
256 + 64 ✓; and "recovery output MUST be re-verified as a whole file (§8)",
which the first 320 bytes pass. So the tool settles on the trailer at
**256**.

(3) Default read path (§9.5 `[R-LIF-05]`): "a reader that finds no valid
trailer in the final 64 bytes MUST report the file torn or invalid and MUST
NOT scan backward." The 8 bytes at F−64 = 576 are not the magic → §6.2's
first ordered check fails → **reject-file** (F8).

**Answer: 576, 256, reject-file.** Confidence high.

## Q09

Geometry: extent 8, tile 4 → G = 2, N = 2, interleaved 1 channel →
entry_count 2. After the shrink to 7: G = ⌈7/4⌉ = 2, N = 2, entry_count
unchanged. Coordinate 7 leaves the extents, so in-tile ordinal 7 mod 4 = 3
of disk-ordinal-1's tile becomes a **padding position**.

§20.3 step 4: "A commit MUST NOT change a layer's declarations in a way that
alters, for any tile that layer stores in the generation this commit
supersedes, what §14 fixes for its stored bytes or how they decode — the set
of padding positions (§11.3) and the content `[R-SER-05]` fixes there …"
— but immediately: "a change that leaves every one of those tiles' stored
bytes meaning exactly what they meant — … or **a new padding position whose
stored byte already holds the fill `[R-SER-05]` fixes** — is not what this
bars."

And for shrinks specifically: "a shrink is permitted exactly where it alters
nothing §14 fixes for any tile the layer stores in the generation this commit
supersedes. … its carve-out included — a new padding position whose stored
byte already holds the fill `[R-SER-05]` fixes is not one, so a shrink
producing only those is permitted here exactly as it is there."
§11.1's rationale states the same.

Case A: that byte is 0x00 = the recorded fill → carve-out applies →
**permitted**.
Case B: 0x05 ≠ fill → `[R-SER-05]` would now be violated at that position,
so the change alters what §14 fixes for a prior-generation stored tile →
**barred**.

**Answer: permitted, barred.** Confidence high.

## Q10

G = ⌈5/6⌉ = 1, N = 1, planar C = 1 → entry_count = 1. P = ∏Tᵢ = 6.

Planar bool → §14.3 `[R-SER-03]`: bit-packed LSB-first, "value k occupies bit
k mod 8 of byte k div 8", decoded size ⌈P/8⌉ = 1 byte.

Bits:
- k=0 true → bit0 = 1
- k=1 false → bit1 = 0
- k=2 true → bit2 = 1
- k=3 true → bit3 = 1
- k=4 false → bit4 = 0
- k=5 is a padding position (coordinate 5 ≥ E = 5, §11.3). `[R-SER-05]`:
  "at every padding position, a writer MUST encode … the fill bit in a packed
  plane." Fill 0x01 = true → bit5 = 1.
- P mod 8 = 6 ≠ 0, so bits 6–7 are pad bits; `[R-SER-05]`: "Every pad bit
  (§14.3) MUST carry the plane's channel's fill bit" → bits 6,7 = 1,1.

Byte = 0b11101101 = 0xED.

Filter 2: `[R-COD-10]` — "for a packed boolean plane s = 1 and the filter is
the identity." Codec 1 → stored bytes = `ED`.

Length: `[R-COD-04]` → equals decoded size = 1.
crc: CRC-32C(0xED) = 0x0E65B798, stored little-endian `98 B7 65 0E`.

**Answer: `ed`; 1; `98b7650e`.** Confidence high.

## Q11

(1) G_y = ⌈0/65536⌉ = 0 → N = 0 → the layer addresses no tile
(`[R-GEO-02]`, §11.2). `[R-COD-07]` bars codec 4 "for a layer **any of whose
addressed tiles'** decoded size exceeds 0x7E000000" — vacuously satisfied.
The §17.2 Note states this outright: "a layer that addresses none … satisfies
it whatever its tile shape declares, and codec 4 is conforming there."
Also checked `[R-ENC-04]`, which the same Note says does apply in an empty
layer: P = 65536² = 2³², P·Bᶜ = 2³⁵ — both under 2⁶³ − 1. → **no**.

(2) y extent 0 → 1: G_y = 1, G_x = ⌈1000000/65536⌉ = 16, N = 16, C = 1 →
entry_count = C·N = **16**.

(3) Now the layer addresses tiles whose decoded size (planar numeric) is
P·Bᶜ = 2³² · 8 = 34,359,738,368 > 0x7E000000 = 2,113,929,216. `[R-COD-07]`:
"a reader MUST treat such a declaration as a validity error at layer scope,
checkable from declarations alone" — register row L44 → **reject-layer**.
(§20.3 step 4 independently bars the writer from making this growth: it names
"`[R-COD-07]`'s lz4 decoded-size cap among them (L44)". The question asks
what the specification assigns for the layer, which is L44's outcome.)

**Answer: no; 16; reject-layer.** Confidence high.

## Q12

Interleaved → single block [0, 10) (§16.2 `[R-SLB-02]`); "Run r of a block
starts at ordinal block_start + r·S" → runs [0,4), [4,8), [8,10). Ordinals
4–7 are run 1.

Ordinal 4 is the sentinel: "Sentinel tiles are transparent to run
continuity" (`[R-SLB-03]`). Ordinal 5 is therefore the run's **first stored
tile**: 8192 mod 1024 = 0 ✓.

`[R-SLB-03]`: "each stored tile's offset equals the previous stored tile's
offset plus that previous tile's length".

Case (1): ordinal 6 has offset = S (all-ones) and length ≠ S. §15.3 row
"offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile". `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile
on a *structural* ground: they address no usable extent, and the run's stored
tiles close over them." So ordinal 7 follows ordinal 5:
8192 + 300 = **8492**.

Case (2): ordinal 6 is well-formed and fails only its stored bytes' crc.
`[R-SLB-03]`: "An entry whose only defect is that its stored bytes fail its
crc is not transparent — its offset and length stand, and the packing
relation reads them as it does any other stored tile's." (§15.3 agrees: "its
extent stands and it keeps its place in the *verifier* rows, in run
continuity".) Its own offset checks out (8192 + 300 = 8492), so ordinal 7 =
8492 + 100 = **8592**.

**Answer: 8492, 8592.** Confidence high.

## Q13

(1) §15.1 / `[R-CNT-17]`: entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 =
65537·20 + 2·4 = 1,310,740 + 8 = **1,310,748**.

(2) §15.4 `[R-IDX-04]`: "Segment s covers entries [s·2¹⁶,
min((s+1)·2¹⁶, entry_count))". Segment 0 = entries [0, 65536): full, all
sentinels → CRC 0xEECB3BB2 (§15.4's published constant; my computation
reproduces it). Segment 1 = entry [65536, 65537): one entry, and "the final
partial segment's CRC covers only its actual bytes" — a partial segment's CRC
MUST be computed (`[R-IDX-05]`). CRC-32C of the 20 bytes `FF ×16 00 ×4` =
0xE5389D3D.

Each is stored as a little-endian u32 (`[R-ENC-09]`), so the array as stored
is `B2 3B CB EE 3D 9D 38 E5`.

(3) crc_of_crc_array = CRC-32C over that 8-byte array = 0x38502EF7, stored
little-endian `F7 2E 50 38`.

**Answer: 1310748; `b23bcbee3d9d38e5`; `f72e5038`.** Confidence high.

## Q14

(1) §7.2: each record is a 24-byte header + inline_length bytes.
Layer record: 24 + 84 = 108. User-metadata record: 24 + 1 = 25.
§7.1: "The directory region is dir_length bytes at dir_offset. Its final 4
bytes are a CRC-32C over the preceding dir_length − 4 bytes; those covered
bytes are the record sequence itself." → dir_length = 108 + 25 + 4 = **137**.

(2) Structures in the live state: front block 16 bytes at [0,16) (§6.1); the
user-metadata extent, 5 bytes, which must lie at extent_offset ≥ 16 and end
at or before F − 64 (`[R-CNT-13]`); the directory, 137 bytes; the trailer, 64
bytes ending at F. The layer has entry_count 0 and extent (0,0), so there is
no tile-index region (§15.4's example: "At entry_count = 0 there is no region
at all").

`[R-CNT-05]` bars any structure between the directory's end and the trailer,
so the extent precedes the directory. Minimum bytes before the trailer =
16 + 5 + 137 = 158, i.e. F − 64 ≥ 158 → F ≥ 222; and §6.2 requires F to be a
multiple of 64 → F = **256**.

Consistent with `[R-LIF-02]` step 5, "append the pad to the next 64-byte
boundary": directory ends at 158, pad [158,192) = 34 bytes, trailer
[192,256).

**Answer: 137, 256.** Confidence high.

## Q15

- `r`: offset = length = S, crc = 0 → §15.3 first row, "valid sentinel —
  reads as fill". §19.4 step 4: "A valid sentinel short-circuits steps 5 and 6
  … every requested sample position of its tile reads as fill — the entry's
  channel's recorded fill in a planar layer" → **fill**.
- `g`: offset = length = S but crc ≠ 0 → §15.3 row "*structural*:
  reject-tile" (register T6). `[R-TYP-09]`: "A reader MUST NOT return fill for
  a tile whose entry is malformed (§15.3)"; `[R-CNF-09]`: "a read of a
  rejected tile MUST NOT silently return fill" → **failure**.
- `b`: well-formed entry whose stored bytes fail its crc → §15.3 row "stored
  bytes fail the entry's crc | reject-tile (§8.2)" (T1) → **failure**.

Planar storedness is per channel (§3.2), and §19.4 step 8 bounds each
rejected entry's failure to the positions that entry carries, so `r` still
returns fill.

**Answer: fill, failure, failure.** Confidence high.

---

## Underdetermined questions

None. Every question resolved to a single reading anchored in a normative
sentence; where a Note was the clearest statement (Q11's codec-4 escape) the
governing normative rule (`[R-COD-07]`, quantified over *addressed* tiles)
yields the same answer independently.
