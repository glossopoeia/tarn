# Round 26 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
Local computation only (Python CRC-32C, no file reads other than my own
scratch scripts).

**CRC implementation validation.** Reflected polynomial 0x82F63B78, init
0xFFFFFFFF, final XOR 0xFFFFFFFF. Reproduces, unaided, every CRC constant
the document itself states:

- CRC-32C("123456789") = 0xE3069283 (§4.5 check vector) ✓
- CRC-32C(zero bytes) = 0x00000000 ✓
- 4 sentinel entries (80 bytes) → 0x80A34955 (§7.4 example) ✓
- crc_of_crc_array of that 4-byte array → 0xC4EE982E (§7.4 example) ✓
- Appendix A trailer bytes [0,60) → 0xE00938D2 ✓
- 2¹⁶ sentinel entries → 0xEECB3BB2 (§15.4, `[R-IDX-05]`) ✓

Six independent hits; the implementation is the document's checksum.

---

## Q01 — layer-record inline payload arithmetic

Payload field order is §7.4's table. Walking the offsets exactly as the
§7.4 worked example does (which lands on 81 for its own layer, confirming
the packing rule "fields are packed in table order with no alignment or
padding between them", `[R-CNT-18]`):

| offset | field | size |
|---|---|---|
| 0 | name `ab`: u8 len + 2 bytes | 3 |
| 3 | layout (u8) = 2 | 1 |
| 4 | linearization (u16) = 1 | 2 |
| 6 | codec (u16) = 3 | 2 |
| 8 | filter (u16) = 2 | 2 |
| 10 | alignment A (u64) = 0 | 8 |
| 18 | slab S (u64) = 4 | 8 |
| 26 | A_slab (u64) = 4096 | 8 |
| 34 | rank d (u8) = 2 | 1 |
| 35 | channel count C (u16) = 2 | 2 |
| 37 | dim `y`: name 2 + extent 8 + tile extent 8 | 18 |
| 55 | dim `x`: same | 18 |
| 73 | chan `u`: name 2 + type 2 + fill (1 + 2, uint16 elem size 2) | 7 |
| 80 | chan `b`: name 2 + type 2 + fill (1 + 1, bool elem size 1) | 6 |
| 86 | index_encoding (u8) = 1 | 1 |
| **87** | **entry_count (u64)** | 8 |
| 95 | crc_of_crc_array (u32) | 4 |
| 99 | (end — no sub-records) | |

(1) inline_length = **99**.

(4) entry_count begins at byte **87**.

(2) entry_count: layout 2 = planar. §11.2 grid counts G_y = ⌈10/4⌉ = 3,
G_x = ⌈9/4⌉ = 3, N = 9; planar addressed-tile count = C·N = 2·9 = **18**.

(3) `[R-CNT-17]`: "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4" = 18·20 + 1·4 = 360 + 4 = **364**.

Answer: 99, 18, 364, 87.

---

## Q02 — trailer CRC

§6.2 layout, all little-endian. Bytes [0,60):

```
8a4e5241540d0a1a 0100 0000 00000000
0300000000000000 1000000000000000 4400000000000000
c000000000000000 efbeadde00000000 00000000
```

CRC-32C = 0xF3566CE6, stored little-endian at [60,64) as `e6 6c 56 f3`.

Answer: **e66c56f3**.

---

## Q03 — interleaved shuffle + codec 1

Channels `a` uint8 (B=1), `b` int16 (B=2) → Q = 3. §17.3: "The shuffle
stride s is … the sample stride Q for an interleaved tile". L = 12,
n = L/s = 4.

`[R-COD-10]`: "the filtered image places byte i of group j at offset
i · n + j".

Groups: (41 02 01)(07 FE FF)(07 FE FF)(07 FE FF)
→ first bytes 41 07 07 07, second bytes 02 FE FE FE, third bytes 01 FF FF FF.

(Cross-check: applying the same code to §17.3's float32 example reproduces
its stated output `00 00 00 00 00 00 80 00 40 3F 40 40` exactly.)

Codec 1 (none): "The stored bytes are the filtered image verbatim"
(`[R-COD-04]`).

(1) **4107070702fefefe01ffffff**
(2) `[R-COD-04]`: "The index entry's length therefore MUST equal the tile's
decoded size" = **12**
(3) CRC-32C of the stored bytes = 0x2B8A45D7, stored LE = **d7458a2b**

---

## Q04 — planar geometry and entry placement

G_y = ⌈1000/128⌉ = 8, G_x = ⌈500/128⌉ = 4, N = 32.

(1) planar entry_count = C·N = 3·32 = **96**
(2) extent_length = 96·20 + ⌈96/65536⌉·4 = 1920 + 4 = **1924**
(3) t = (400 div 128, 300 div 128) = (3, 2); `[R-GEO-06]` s = Σ tᵢ·∏_{j>i} Gⱼ
= 3·4 + 2 = 14. Channel `b` has index c = 2 (declared third). Disk ordinal
= c·N + s = 2·32 + 14 = **78**
(4) §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at
region byte 20·k" = 20·78 = **1560**

---

## Q05 — slack total

§9.7 claimants of the live state: front block [0,16), the layer record's
extent = the tile-index region [16,60), each non-sentinel entry's stored
extent [64,164) and [200,300), the directory [848,960), the live trailer
[960,1024).

(entry_count = ⌈5/4⌉ = 2, extent_length = 2·20 + 4 = 44 = 60 − 16 ✓, so the
slot is self-consistent and the walk completes.)

Claimed = 16 + 44 + 100 + 100 + 112 + 64 = 436.
Slack = 1024 − 436 = **588**. (Regions: [60,64) 4, [164,200) 36,
[300,848) 548 → 588 ✓)

`[R-CNT-21]`: "a verifier that reaches a live state MUST report the total
number of slack bytes". The walk completes, so the total is exact, not
partial.

---

## Q06 — four user-metadata cases

(a) §7.1 `[R-CNT-25]`: "An extent of (0, 0) on a user-metadata record …
is a validity error at its containing scope." Top-level → file → F21
**reject-file**.

(b) extent_length 4 < 5. Same sentence: "or one whose extent_length is
less than 5 — too short to hold both a document and the terminal CRC-32C".
F22 → **reject-file**.

(c) inline_length 1, encoding byte 0x00 = encoding value 0. §7.1: "An
encoding value of 0, or one the reader does not implement, makes that
record unreadable, with the same outcome as a failed CRC — ignore-record."
R1 → **ignore-record**. (R1 is a *violation* carrying outcome
ignore-record; the question asks the outcome class.)

(d) `[R-MTA-03]`: "A record whose inline_length is not 1 is a validity
error at the record's containing scope". F23 → **reject-file**.

Answer: reject-file, reject-file, ignore-record, reject-file.

---

## Q07 — experimental metadata encoding

0x9F ≥ 0x80 → experimental range (§10.2, §18.2).

§21.6 row: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming …
No document rule attaches at such an encoding, so a verifier certifies,
reporting the record it ignored."

`[R-MTA-10]`: "A verifier meeting such a record in an otherwise conforming
file has no requirement it is unable to check — the record is not among
`[R-CNF-11]`'s cannot-establish grounds, and certification is unaffected".

(1) **conforming** (2) **ignore-record**

---

## Q08 — recovery probe

(1) `[R-LIF-06]`: "The probe begins at the largest 64-aligned offset o with
o + 64 ≤ the physical file length." 640 − 64 = 576, 64-aligned → **576**.

(2) Probing backward: 576 has no magic. 448 has magic and a verifying CRC,
but the rule additionally requires "committed_file_length = o + 64" =
512; it declares 576, so it is not a valid candidate. 256 has magic, a
verifying CRC, and cfl = 320 = 256 + 64 ✓. Whole-file re-verification of
[0,320) succeeds ("a candidate whose whole-file re-verification fails was
not a commit state, so the tool continues the probe past it"), so the tool
settles on **256**.

(3) Default read path: the 8 bytes at F − 64 = 576 are not the trailer
magic → F8, `[R-CNT-06]`. `[R-LIF-05]`: "a reader that finds no valid
trailer in the final 64 bytes MUST report the file torn or invalid and
MUST NOT scan backward." → **reject-file**.

---

## Q09 — the shrink bar

Rank 1, T = 4. Extent 8 → G = 2; extent 7 → G = ⌈7/4⌉ = 2. entry_count
unchanged, decoded size (P·Q = 4·1 = 4) unchanged, offsets unchanged,
codec/filter unchanged. What changes: tile 1 covers coordinates 4–7, and
coordinate 7 (in-tile ordinal 3) becomes a **padding position**.

§20.3 step 4: "A commit MUST NOT change a layer's declarations in a way
that alters, for any tile that layer stores in the generation this commit
supersedes, what §14 fixes for its stored bytes … the set of padding
positions (§11.3) and the content `[R-SER-05]` fixes there …" — with the
express carve-out: "a new padding position whose stored byte already holds
the fill `[R-SER-05]` fixes — is not what this bars." The shrink paragraph
repeats it: "a new padding position whose stored byte already holds the
fill `[R-SER-05]` fixes is not one, so a shrink producing only those is
permitted here exactly as it is there."

Case A: byte is 0x00 = the recorded fill → carve-out applies →
**permitted**.
Case B: byte is 0x05 ≠ fill → the new padding position's content violates
what `[R-SER-05]` fixes → **barred**.

---

## Q10 — packed bool plane

G = ⌈5/6⌉ = 1, N = 1, planar C = 1 → entry_count 1. P = ∏Tᵢ = 6.
Planar bool → §14.3 packed plane, decoded size ⌈6/8⌉ = 1 byte.

In-tile ordinals 0–5; ordinals 0–4 are coordinates 0–4 (real), ordinal 5 is
coordinate 5 ≥ extent 5 → a padding position. `[R-SER-05]`: a padding
position carries "the fill bit in a packed plane"; fill 0x01 = true → 1.
P mod 8 = 6 ≠ 0, so bits 6–7 are pad bits, which "MUST carry the plane's
channel's fill bit" = 1.

bit0..7 = 1,0,1,1,0,1,1,1 → 0x01+0x04+0x08+0x20+0x40+0x80 = 0xED.

Filter 2: §17.3 "for a packed boolean plane s = 1 and the filter is the
identity". Codec 1 → stored verbatim.

(1) **ed** (2) `[R-COD-04]` length = decoded size = **1**
(3) CRC-32C(0xED) = 0x0E65B798 → stored LE **98b7650e**

---

## Q11 — the lz4 cap and the escape closing

(1) G_y = ⌈0/65536⌉ = 0 → N = 0 → entry_count = 0, no addressed tiles.
§17.2's note on `[R-COD-07]`: "The cap is quantified over the layer's
*addressed* tiles, so a layer that addresses none — any dimension extent 0
— satisfies it whatever its tile shape declares, and codec 4 is conforming
there." Also check what *is* checked in an empty layer: P·Bᶜ = 2³² · 8 =
2³⁵ = 34,359,738,368 < 2⁶³ − 1, so `[R-ENC-04]` is satisfied. → **no**.

(2) y extent 1 → G_y = 1; G_x = ⌈1000000/65536⌉ = 16 (65536·15 = 983040 <
1000000). N = 16; planar C = 1 → entry_count = **16**.

(3) Now the layer addresses tiles, and each plane's decoded size is
P·Bᶜ = 2³⁵ = 34,359,738,368 > 0x7E000000 = 2,113,929,216. `[R-COD-07]`:
"Writers MUST NOT declare this codec for a layer any of whose addressed
tiles' decoded size exceeds 0x7E000000 bytes … a reader MUST treat such a
declaration as a validity error at layer scope" (L44). §20.3 names exactly
this case: the growth must stay "within every bound … `[R-COD-07]`'s lz4
decoded-size cap among them (L44), which an empty layer escapes only
because that cap is quantified over addressed tiles." → **reject-layer**.

---

## Q12 — slab run continuity

Interleaved → single block [0, 10). `[R-SLB-02]`: "Run r of a block starts
at ordinal block_start + r·S" → runs [0,4), [4,8), [8,10). Ordinals 4–7 are
exactly run 1.

`[R-SLB-03]`: "each stored tile's offset equals the previous stored tile's
offset plus that previous tile's length"; sentinels are transparent, and
"So are the entries §15.3 classifies reject-tile on a *structural* ground";
but "An entry whose only defect is that its stored bytes fail its crc is
not transparent — its offset and length stand, and the packing relation
reads them as it does any other stored tile's".

(1) Ordinal 6 has offset = S with length ≠ S → §15.3 row "offset = S ∧
length ≠ S … *structural*: reject-tile" → transparent. Ordinal 4 sentinel →
transparent. So ordinal 7 follows ordinal 5: 8192 + 300 = **8492**.
(First stored tile of the run is ordinal 5; 8192 mod 1024 = 0 ✓.)

(2) Ordinal 6's only defect is its crc → not transparent, its extent stands
(8492 + 100 = 8592, and 8492 = 8192 + 300 keeps the run consistent). So
ordinal 7's offset = **8592**.

---

## Q13 — 65,537 sentinel entries

(1) §15.1 region = entry array + segment CRC array; `[R-CNT-17]` gives the
length: 65537·20 + ⌈65537/65536⌉·4 = 1,310,740 + 2·4 = **1,310,748**.

(2) §15.4: segment 0 covers entries [0, 65536) — a full segment of
sentinels → 0xEECB3BB2 (`[R-IDX-05]`, and my own computation reproduces
it). Segment 1 covers entries [65536, 65537) — one sentinel entry, 20
bytes `FF ×16 00 ×4`; "the final partial segment's CRC covers only its
actual bytes" and "a partial segment's CRC MUST be computed" →
CRC-32C = 0xE5389D3D. Stored little-endian, in order:
**b23bcbee3d9d38e5**

(3) crc_of_crc_array = CRC-32C over those 8 stored bytes = 0x38502EF7,
stored little-endian as a u32 → **f72e5038**.
(Reading note: "exactly as stored in the inline payload" — I give the
stored byte order. The numeric value is 0x38502EF7.)

---

## Q14 — smallest single-commit file

(1) §7.2 framing: each record is a 24-byte header plus inline_length bytes.
Layer 24 + 84 = 108; user metadata 24 + 1 = 25; sequence 133. §7.1: "Its
final 4 bytes are a CRC-32C over the preceding dir_length − 4 bytes" →
dir_length = 133 + 4 = **137**.

(2) Minimum layout. Front block [0,16) (`[R-LIF-02]` creation path: emit
the front block, then write "beginning at offset 16"). Step 2 appends the
record extents: the 5-byte user-metadata extent, earliest at [16,21) — the
layer has entry_count 0 and slot (0,0), so it contributes no index region.
Step 3 appends the directory: [21,158). `[R-CNT-05]` forbids any structure
between the directory's end and the trailer, so nothing can be tucked after
it. Step 5 pads "to the next 64-byte boundary" → 192, then the 64-byte
trailer at [192,256).

F = **256**. It cannot be 192: that needs the directory to end by 128, but
16 + 5 + 137 = 158 bytes are unavoidable before the pad. F is a multiple of
64 (§6.2) ✓.

---

## Q15 — three planar entries at one spatial ordinal

- `r`: offset = length = S, crc = 0 → §15.3 "valid sentinel — reads as
  fill". `[R-TYP-08]`, `[R-RDR-04]` step 4: "A valid sentinel
  short-circuits steps 5 and 6 … reads as fill". → **fill**
- `g`: offset = length = S, crc ≠ 0 → §15.3 "*structural*: reject-tile"
  (T6). `[R-TYP-09]`: "A reader MUST NOT return fill for a tile whose entry
  is malformed"; `[R-CNF-09]`: "a read of a rejected tile MUST NOT silently
  return fill". → **failure**
- `b`: well-formed entry whose stored bytes fail its crc → §15.3
  "reject-tile (§8.2)" (T1). → **failure**

The layer chain verifies, so nothing escalates to layer scope, and
`[R-RDR-04]` step 8 bounds each rejected entry's failure to the positions
that entry carries.

Answer: fill, failure, failure.
