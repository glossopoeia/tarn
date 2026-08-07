# TARN Acceptance Review — WRITER Charter

**Reviewer role:** fresh-context implementer of a conforming *writer* (creator + appender + compactor).
**Source of truth:** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full (3172 lines). No other file, no repository history, no external reference, no prior knowledge of the project.
**Method:** every byte below was derived from the spec text, emitted by a from-scratch builder, and then re-read by an independently written reader/verifier that re-derives geometry, re-checks every cross-check in §7.4/§15, and recomputes every checksum in §8.1's map. The CRC-32C implementation was written from §4.5's parameters alone and reproduces **both** constants the document supplies as check values: `CRC-32C("123456789") = 0xE3069283` (§4.5) and `CRC-32C` of a full all-sentinel segment `= 0xEECB3BB2` (§15.4, `[R-IDX-05]`). The second is a genuine independent confirmation of a spec constant, not a restatement of it.

---

## 1. The generation-1 file

### 1.1 What the charter fixes, and what I had to choose

The charter fixes: one interleaved layer; dims `t`(E=2,T=1) then `x`(E=3,T=2); channels `p`(uint8, fill `0x00`) and `q`(bool, fill `0x01`); codec 1; no alignment, no slab.

Everything else is a writer choice. Every choice I made, named:

| # | Choice | Value | Why the spec leaves it open |
|---|---|---|---|
| C1 | Layer name | `"L"` (1 byte, `4C`) | §4.6 constrains form only; `[R-ENC-15]` uniqueness is trivially met |
| C2 | Dimension names | `"t"`, `"x"` (`74`, `78`) | same |
| C3 | Channel names | `"p"`, `"q"` (`70`, `71`) | same |
| C4 | `filter` | 1 = none | `[R-COD-09]` permits 1 or 2 freely; charter is silent |
| C5 | `version_minor` | 0 | `[R-CNT-26]` floor for a file expressible under this text |
| C6 | `flags` | 0 | `[R-CNT-08]` — MUST be 0 for a writer under this text |
| C7 | `file_id` | `0x0F1E2D3C4B5A6978` | §6.2 requires ≠ 0; `[R-LIF-03]` SHOULDs a CSPRNG draw. Fixed here for reproducibility of this transcript |
| C8 | `generation` | 1 | forced for a creator (`[R-LIF-02]` creation path) |
| C9 | Which tiles are stored | tiles 0, 1, 2 stored; tile 3 = sentinel | §13 / `[R-IDX-02]`; Appendix G item 6 confirms this is a writer choice, not a rule |
| C10 | Sample values | see §1.3 | application data |
| C11 | Structure order | payloads (disk-ordinal order) → index region → directory | `[R-LIF-02]` step 2: "in any order"; `[R-SLB-05]` |
| C12 | `dir_offset` | 112 | free, subject to `[R-CNT-06]` and `[R-CNT-05]`; it determines the pad length (19) and F (320) |
| C13 | No sub-records, no user metadata | — | optional (`[R-CNT-14]`) |

**One placement constraint that is *not* free, and that I had to infer** (see Finding A2): because the layer declares neither alignment nor a slab, `[R-CNT-03]`'s enumeration of *declared padding* — "the alignment gaps of aligned or slab-declared layers (§16) and each generation's pre-trailer pad" — is closed. Therefore any gap I left between two structures would be a byte claimed by no coverage class, and `[R-CNT-02]` says such a file "is not a conforming file" (register row F9). **My structures are packed gaplessly from offset 16 to the directory's end; only the pre-trailer pad may be a gap.**

### 1.2 Geometry, derived

Per `[R-GEO-03]`, `[R-SER-01]`, `[R-SER-02]`:

```
d = 2, C = 2, layout = 1 (interleaved), linearization = 1 (row-major)
dim 0: t  E₀ = 2, T₀ = 1  →  G₀ = ⌈2/1⌉ = 2/1 = 2, remainder 0        (§11.2)
dim 1: x  E₁ = 3, T₁ = 2  →  G₁ = ⌈3/2⌉ = 3/2 + 1 = 1 + 1 = 2         (§11.2)
N = ∏Gᵢ = 4  (spatial-tile count)
P = ∏Tᵢ = 1 · 2 = 2  (sample positions per tile)
addressed-tile count = N = 4 (interleaved)  →  entry_count = 4  [R-CNT-17]
B_p = 1 (uint8), B_q = 1 (bool, element size 1 by §12.1)
Q = ΣBᵢ = 2 (sample stride);  F_p = 0, F_q = 1  (in-sample offsets, §14.2)
V = P · C = 4 values per tile;  decoded size = P · Q = 4 bytes        [R-SER-02]
codec 1 ⇒ every stored tile's index-entry length MUST equal 4          [R-COD-04]
index region length = 4·20 + ⌈4/2¹⁶⌉·4 = 80 + 4 = 84                   [R-CNT-17]
```

Tile↔coordinate map (`[R-GEO-06]`, s = t₀·G₁ + t₁; in-tile ordinal u = u₀·T₁ + u₁, and T₀ = 1 so u₀ ≡ 0):

| s | tile coords (t₀,t₁) | covers t | covers x | in-tile ordinal 0 | in-tile ordinal 1 |
|---|---|---|---|---|---|
| 0 | (0,0) | t=0 | x∈{0,1} | (0,0) real | (0,1) real |
| 1 | (0,1) | t=0 | x∈{2,3} | (0,2) real | **(0,3) padding** (x ≥ E₁=3, §11.3) |
| 2 | (1,0) | t=1 | x∈{0,1} | (1,0) real | (1,1) real |
| 3 | (1,1) | t=1 | x∈{2,3} | (1,2) real | **(1,3) padding** |

### 1.3 The reference array (§3.2) and the decoded tile images

Chosen sample content, and the resulting reference array (`[R-MDL-01]`):

| coord (t,x) | p (uint8) | q (bool) | source |
|---|---|---|---|
| (0,0) | `0x0A` | true | tile 0 |
| (0,1) | `0x0B` | false | tile 0 |
| (0,2) | `0x0C` | true | tile 1 |
| (1,0) | `0x14` | false | tile 2 |
| (1,1) | `0x15` | true | tile 2 |
| (1,2) | `0x00` | **true** | **tile 3 is the sentinel → fill** (`[R-TYP-08]`) |

Decoded tile images. Value k of the sequence is channel (k mod C) at in-tile ordinal k div C (`[R-SER-01]`); its byte offset is (k div C)·Q + F_{k mod C} = u·2 + F_c (`[R-SER-02]`). Padding positions carry **fill**, not zero, not garbage (`[R-SER-05]`) — for `q` that is the fill *byte* `0x01`, since an interleaved bool is one byte (§14.2, §14.5).

| tile | byte 0 = p@u0 | byte 1 = q@u0 | byte 2 = p@u1 | byte 3 = q@u1 | image | CRC-32C |
|---|---|---|---|---|---|---|
| 0 (stored) | `0A` p(0,0) | `01` q(0,0)=true | `0B` p(0,1) | `00` q(0,1)=false | `0A 01 0B 00` | `0x0DF6F2FF` |
| 1 (stored) | `0C` p(0,2) | `01` q(0,2)=true | `00` **p fill (pad pos (0,3))** | `01` **q fill (pad pos (0,3))** | `0C 01 00 01` | `0x922B08AF` |
| 2 (stored) | `14` p(1,0) | `00` q(1,0)=false | `15` p(1,1) | `01` q(1,1)=true | `14 00 15 01` | `0x4AA74020` |
| 3 | — | — | — | — | **not stored** — sentinel entry `FF×16 00×4` (§15.2) | — |

Filter 1 = none, so the filtered image is the decoded image; codec 1 = none, so the stored bytes are the filtered image verbatim (`[R-COD-04]`). Stored length = 4 = decoded size for each stored tile. ✔

### 1.4 Complete file — every byte

**F = 320 bytes** (multiple of 64, `[R-CNT-01]`).

```
       0  1  2  3  4  5  6  7    8  9  A  B  C  D  E  F
0000  89 54 41 52 4E 0D 0A 1A   00 00 00 00 00 00 00 00
0010  0A 01 0B 00 0C 01 00 01   14 00 15 01 10 00 00 00
0020  00 00 00 00 04 00 00 00   00 00 00 00 FF F2 F6 0D
0030  14 00 00 00 00 00 00 00   04 00 00 00 00 00 00 00
0040  AF 08 2B 92 18 00 00 00   00 00 00 00 04 00 00 00
0050  00 00 00 00 20 40 A7 4A   FF FF FF FF FF FF FF FF
0060  FF FF FF FF FF FF FF FF   00 00 00 00 A9 AB E0 81
0070  01 00 03 00 61 00 00 00   1C 00 00 00 00 00 00 00
0080  54 00 00 00 00 00 00 00   01 4C 01 01 00 01 00 01
0090  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
00A0  00 00 00 00 00 00 00 00   00 02 02 00 01 74 02 00
00B0  00 00 00 00 00 00 01 00   00 00 00 00 00 00 01 78
00C0  03 00 00 00 00 00 00 00   02 00 00 00 00 00 00 00
00D0  01 70 06 00 01 00 01 71   01 00 01 01 01 04 00 00
00E0  00 00 00 00 00 48 4A 3D   55 54 37 2D 96 00 00 00
00F0  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
0100  8A 4E 52 41 54 0D 0A 1A   01 00 00 00 00 00 00 00
0110  01 00 00 00 00 00 00 00   70 00 00 00 00 00 00 00
0120  7D 00 00 00 00 00 00 00   40 01 00 00 00 00 00 00
0130  78 69 5A 4B 3C 2D 1E 0F   00 00 00 00 00 3B 3A 97
```

#### 1.4.1 Front signature block — [0, 16) — §6.1, `[R-CNT-04]`

| Range | Bytes | Meaning |
|---|---|---|
| [0,8) | `89 54 41 52 4E 0D 0A 1A` | `\x89` "TARN" CR LF ctrl-Z — constant, structural |
| [8,16) | `00 ×8` | reserved, zero |

Belongs to no generation (§9.7(b): F₀ = 16). Checked by byte equality only — covered by no checksum (§8.1).

#### 1.4.2 Stored-tile extents — [16, 28) — generation 1

| Range | Bytes | Tile |
|---|---|---|
| [16,20) | `0A 01 0B 00` | disk ordinal 0 |
| [20,24) | `0C 01 00 01` | disk ordinal 1 (bytes 2–3 are the fill-encoded padding position) |
| [24,28) | `14 00 15 01` | disk ordinal 2 |

Placed in disk-ordinal order at the earliest legal offset (16 — `[R-IDX-03]` forbids offset < 16). Gapless, per §1.1.

#### 1.4.3 Tile-index region — [28, 112) — 84 bytes — §15.1, `[R-IDX-01]`

Entry k at region byte 20·k (file offset 28 + 20k). Layout per entry: `u64 offset · u64 length · u32 crc`.

| Entry | File range | offset | length | crc | Bytes |
|---|---|---|---|---|---|
| 0 | [28,48) | 16 | 4 | `0x0DF6F2FF` | `10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00  FF F2 F6 0D` |
| 1 | [48,68) | 20 | 4 | `0x922B08AF` | `14 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00  AF 08 2B 92` |
| 2 | [68,88) | 24 | 4 | `0x4AA74020` | `18 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00  20 40 A7 4A` |
| 3 | [88,108) | **sentinel** | | | `FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  00 00 00 00` |

Segment CRC array — [108, 112) — ⌈4/2¹⁶⌉ = 1 u32, over entries [0, min(2¹⁶,4)) = the whole 80-byte entry array (§15.4):

| Range | Bytes | Value |
|---|---|---|
| [108,112) | `A9 AB E0 81` | segment 0 CRC = `0x81E0ABA9` |

Note the partial segment's CRC is **computed** over its actual 80 bytes; `[R-IDX-05]`'s `0xEECB3BB2` shortcut applies only to a *full* 2¹⁶-entry all-sentinel segment and would be wrong here.

#### 1.4.4 Directory region — [112, 237) — 125 bytes — §7.1

**Record header — [112, 136) — §7.2**

| Off | Range | Bytes | Field |
|---|---|---|---|
| 0 | [112,114) | `01 00` | type = 0x0001 (layer) |
| 2 | [114,116) | `03 00` | flags = MU(bit0) \| PE(bit1) — fixed by §7.3's registry table, `[R-CNT-22]` |
| 4 | [116,120) | `61 00 00 00` | inline_length = 97 |
| 8 | [120,128) | `1C 00 00 00 00 00 00 00` | extent_offset = 28 → the tile-index region |
| 16 | [128,136) | `54 00 00 00 00 00 00 00` | extent_length = 84 = 4·20 + 1·4 ✔ `[R-CNT-17]` |

**Layer-record inline payload — [136, 233) — 97 bytes — §7.4**, packed in table order with no padding (`[R-CNT-18]`):

| Range | Bytes | Field |
|---|---|---|
| [136,138) | `01 4C` | name: u8 len 1, `"L"` |
| [138,139) | `01` | layout = 1 (interleaved) |
| [139,141) | `01 00` | linearization = 1 (row-major; the only legal value, `[R-GEO-05]`) |
| [141,143) | `01 00` | codec = 1 (none) |
| [143,145) | `01 00` | filter = 1 (none) |
| [145,153) | `00 ×8` | alignment A = 0 |
| [153,161) | `00 ×8` | slab S = 0 |
| [161,169) | `00 ×8` | A_slab = 0 — forced to 0 when S = 0 (`[R-CNT-23]`) |
| [169,170) | `02` | rank d = 2 |
| [170,172) | `02 00` | channel count C = 2 |
| [172,174) | `01 74` | dim 0 name `"t"` |
| [174,182) | `02 00 00 00 00 00 00 00` | E₀ = 2 |
| [182,190) | `01 00 00 00 00 00 00 00` | T₀ = 1 |
| [190,192) | `01 78` | dim 1 name `"x"` |
| [192,200) | `03 00 00 00 00 00 00 00` | E₁ = 3 |
| [200,208) | `02 00 00 00 00 00 00 00` | T₁ = 2 |
| [208,210) | `01 70` | ch 0 name `"p"` |
| [210,212) | `06 00` | type = 6 (uint8) |
| [212,214) | `01 00` | fill: u8 len 1 (= element size, `[R-CNT-23]`), fill byte `0x00` |
| [214,216) | `01 71` | ch 1 name `"q"` |
| [216,218) | `01 00` | type = 1 (bool) |
| [218,220) | `01 01` | fill: len 1, fill byte `0x01` = true (`[R-TYP-07]` admits only `00`/`01`) |
| [220,221) | `01` | index_encoding = 1 (raw-segmented) |
| [221,229) | `04 00 00 00 00 00 00 00` | entry_count = 4 = addressed-tile count ✔ |
| [229,233) | `48 4A 3D 55` | crc_of_crc_array = `0x553D4A48` = CRC-32C over the 4-byte segment-CRC array |

No sub-records: the payload ends exactly at the trailing fixed field, no residue (`[R-CNT-18]`).

**Directory CRC — [233, 237)**

| Range | Bytes | Value |
|---|---|---|
| [233,237) | `54 37 2D 96` | `0x962D3754` = CRC-32C over the preceding dir_length − 4 = 121 record bytes (§7.1) |

The encoding of the layer-record byte string is pinned exactly by §12.3's worked channel-entry example (`04 74 65 6D 70 0C 00 04 00 00 C0 7F`), which is what let me confirm the fill field's `u8 len + bytes` framing without guessing.

#### 1.4.5 Pre-trailer pad — [237, 256) — 19 bytes

`00 ×19`. Declared padding of generation 1; MUST be zero (`[R-CNT-03]`); fewer than 64 bytes (`[R-CNT-05]`). Its length is a *consequence* of C12, not an independent choice: 256 = the least 64-aligned offset ≥ 237.

#### 1.4.6 Trailer — [256, 320) — §6.2

| Off | Range | Bytes | Field |
|---|---|---|---|
| 0 | [256,264) | `8A 4E 52 41 54 0D 0A 1A` | trailer magic (`\x8A` "NRAT" CR LF ctrl-Z) |
| 8 | [264,266) | `01 00` | version_major = 1 |
| 10 | [266,268) | `00 00` | version_minor = 0 |
| 12 | [268,272) | `00 00 00 00` | flags = 0 |
| 16 | [272,280) | `01 00 00 00 00 00 00 00` | generation = 1 |
| 24 | [280,288) | `70 00 00 00 00 00 00 00` | dir_offset = 112 (≥ 16 ✔) |
| 32 | [288,296) | `7D 00 00 00 00 00 00 00` | dir_length = 125 (≥ 4 ✔; 112+125 = 237 ≤ 320−64 ✔) |
| 40 | [296,304) | `40 01 00 00 00 00 00 00` | committed_file_length = 320 = F, 320 mod 64 = 0 ✔ |
| 48 | [304,312) | `78 69 5A 4B 3C 2D 1E 0F` | file_id = `0x0F1E2D3C4B5A6978` ≠ 0 |
| 56 | [312,316) | `00 00 00 00` | reserved, zero |
| 60 | [316,320) | `00 3B 3A 97` | trailer CRC = `0x973A3B00` over [0, 60) |

#### 1.4.7 Byte-coverage proof (§5.2, `[R-CNT-02]`)

`[0,16)` front · `[16,20)`,`[20,24)`,`[24,28)` stored-tile extents (gen 1) · `[28,112)` tile-index region (gen 1) · `[112,237)` directory (gen 1) · `[237,256)` declared padding (gen 1) · `[256,320)` trailer (gen 1). Every byte claimed exactly once; no overlaps. `dir_length + pad + 64 = 208 ≤ 65,536`, satisfying `[R-CNT-09]`'s SHOULD.

---

## 2. Generation 2 — superseding one tile

The commit supersedes disk ordinal 2 with new content p(1,0)=`0x2A`, q(1,0)=true, p(1,1)=`0x2B`, q(1,1)=true → decoded image `2A 01 2B 01`, CRC `0x57338675`.

Procedure per `[R-WRT-04]` / `[R-LIF-02]`: establish F = 320 by validating the tail trailer (step 1); open (step 2); validate the layer record and the index chain the commit reuses (step 3, `[R-WRT-03]`); write at exactly F (step 4) — the new payload, then the layer's **full** re-emitted index region (entry_count entries + segment CRC array), with unchanged entries "byte-identical at [their] disk-ordinal position"; re-emit the complete directory (step 5); barrier, pad, trailer, barrier (step 6).

**Appended bytes — [320, 640), F₂ = 640**

```
       0  1  2  3  4  5  6  7    8  9  A  B  C  D  E  F
0140  2A 01 2B 01 10 00 00 00   00 00 00 00 04 00 00 00
0150  00 00 00 00 FF F2 F6 0D   14 00 00 00 00 00 00 00
0160  04 00 00 00 00 00 00 00   AF 08 2B 92 40 01 00 00
0170  00 00 00 00 04 00 00 00   00 00 00 00 75 86 33 57
0180  FF FF FF FF FF FF FF FF   FF FF FF FF FF FF FF FF
0190  00 00 00 00 0F F5 E1 5B   01 00 03 00 61 00 00 00
01A0  44 01 00 00 00 00 00 00   54 00 00 00 00 00 00 00
01B0  01 4C 01 01 00 01 00 01   00 00 00 00 00 00 00 00
01C0  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
01D0  00 02 02 00 01 74 02 00   00 00 00 00 00 00 01 00
01E0  00 00 00 00 00 00 01 78   03 00 00 00 00 00 00 00
01F0  02 00 00 00 00 00 00 00   01 70 06 00 01 00 01 71
0200  01 00 01 01 01 04 00 00   00 00 00 00 00 EB E1 49
0210  E1 D3 78 A8 EC 00 00 00   00 00 00 00 00 00 00 00
0220  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
0230  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
0240  8A 4E 52 41 54 0D 0A 1A   01 00 00 00 00 00 00 00
0250  02 00 00 00 00 00 00 00   98 01 00 00 00 00 00 00
0260  7D 00 00 00 00 00 00 00   80 02 00 00 00 00 00 00
0270  78 69 5A 4B 3C 2D 1E 0F   00 00 00 00 DE 13 98 4C
```

| Range | Content | Notes |
|---|---|---|
| [320,324) | `2A 01 2B 01` | new stored-tile extent for disk ordinal 2 |
| [324,404) | entry array | entry 0 `offset=16 len=4 crc=0x0DF6F2FF` — **byte-identical to gen 1**; entry 1 `offset=20 len=4 crc=0x922B08AF` — byte-identical; entry 2 `offset=320 len=4 crc=0x57338675` — **re-pointed**; entry 3 `FF×16 00×4` — byte-identical sentinel |
| [404,408) | `0F F5 E1 5B` | segment 0 CRC = `0x5BE1F50F` (recomputed) |
| [408,533) | directory | one layer record, byte-identical to gen 1's **except** extent_offset `44 01 …` = 324 (at [416,424)) and crc_of_crc_array `EB E1 49 E1` = `0xE149E1EB` (at [525,529)); directory CRC `D3 78 A8 EC` = `0xECA878D3` at [529,533) |
| [533,576) | `00 ×43` | generation 2's pre-trailer pad |
| [576,640) | trailer | generation = **2**, dir_offset = 408 (`98 01 …`), dir_length = 125, committed_file_length = 640 (`80 02 …`), **same file_id** `0x0F1E2D3C4B5A6978`, flags 0, version 1.0, trailer CRC `DE 13 98 4C` = `0x4C9813DE` |

Entries 0 and 1 still point into generation 1's byte range. That is required, not merely permitted: `[R-WRT-04]` demands "every other entry byte-identical at its disk-ordinal position", and §9.7's note licenses cross-generation reference explicitly ("a generation's directory may reference structures appended by earlier commits … those bytes are claimed by the generation that appended them").

### 2.1 What becomes dead space

Dead space = structures of prior generations no longer reachable from the live trailer (`[R-CNT-21]`):

| Range | Size | Structure | Status |
|---|---|---|---|
| [16,20) | 4 | tile 0 payload (gen 1) | **live** — still referenced by gen 2's entry 0 |
| [20,24) | 4 | tile 1 payload (gen 1) | **live** |
| [24,28) | 4 | tile 2 payload (gen 1) | **dead** — superseded |
| [28,112) | 84 | gen-1 tile-index region | **dead** — replaced wholesale |
| [112,237) | 125 | gen-1 directory | **dead** |
| [237,256) | 19 | gen-1 pre-trailer pad | **unreachable** (see Finding O1: `[R-CNT-21]` says "structures", and §5.2 classifies padding as a *separate* class from structures, so prior padding is not literally "dead space" by that wording) |
| [256,320) | 64 | gen-1 trailer | **dead** — a trailer *is* enumerated as a structure in §5.2 |

Total unreachable: **296 bytes** of a 640-byte file. Reclaimable only by compaction (§20.5), and a privacy consideration (`[R-PRV-01]`: a writer "MUST NOT represent a commit that supersedes data as erasure of it").

---

## 3. Compaction

Input: the 640-byte generation-2 file. Output per §20.5.

**Output file_id: `0x778899AABBCCDDEE`** — a *new* value; `[R-WRT-06]` requires it ("reusing the input's would break the (file_id, range) cache contract of `[R-LIF-03]`, since relocation puts different bytes at the same ranges"), and §9.3's CSPRNG advice applies. **Output generation: 1** — `[R-WRT-06]` fixes it: "a compacted file is a whole-file rewrite under a new file_id by definition". Output version_minor 0 and flags 0 (no unknown ignore-lane bits in the input to copy forward).

**Output — 320 bytes, F = 320**

```
       0  1  2  3  4  5  6  7    8  9  A  B  C  D  E  F
0000  89 54 41 52 4E 0D 0A 1A   00 00 00 00 00 00 00 00
0010  0A 01 0B 00 0C 01 00 01   2A 01 2B 01 10 00 00 00
0020  00 00 00 00 04 00 00 00   00 00 00 00 FF F2 F6 0D
0030  14 00 00 00 00 00 00 00   04 00 00 00 00 00 00 00
0040  AF 08 2B 92 18 00 00 00   00 00 00 00 04 00 00 00
0050  00 00 00 00 75 86 33 57   FF FF FF FF FF FF FF FF
0060  FF FF FF FF FF FF FF FF   00 00 00 00 25 98 80 E2
0070  01 00 03 00 61 00 00 00   1C 00 00 00 00 00 00 00
0080  54 00 00 00 00 00 00 00   01 4C 01 01 00 01 00 01
0090  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
00A0  00 00 00 00 00 00 00 00   00 02 02 00 01 74 02 00
00B0  00 00 00 00 00 00 01 00   00 00 00 00 00 00 01 78
00C0  03 00 00 00 00 00 00 00   02 00 00 00 00 00 00 00
00D0  01 70 06 00 01 00 01 71   01 00 01 01 01 04 00 00
00E0  00 00 00 00 00 1F D2 39   03 AF 09 35 37 00 00 00
00F0  00 00 00 00 00 00 00 00   00 00 00 00 00 00 00 00
0100  8A 4E 52 41 54 0D 0A 1A   01 00 00 00 00 00 00 00
0110  01 00 00 00 00 00 00 00   70 00 00 00 00 00 00 00
0120  7D 00 00 00 00 00 00 00   40 01 00 00 00 00 00 00
0130  EE DD CC BB AA 99 88 77   00 00 00 00 F5 19 E6 39
```

### 3.1 Preserved verbatim vs. regenerated

`[R-WRT-07]` is unusually precise here, and I did not have to infer anything:

| Item | Status | Value in the output |
|---|---|---|
| Every stored tile's **bytes** | **verbatim** | `0A 01 0B 00`, `0C 01 00 01`, `2A 01 2B 01` — byte-for-byte from the input's live generation |
| Every index entry's **crc** | **unchanged** | `0x0DF6F2FF`, `0x922B08AF`, `0x57338675` |
| Every index entry's **length** | **unchanged** | 4, 4, 4 |
| **Sentinel** entries | **unchanged** | `FF×16 00×4` at disk ordinal 3 |
| The layer record: name, layout, linearization, codec, filter, A, S, A_slab, d, C, all dimension entries, all channel entries (types and fills), index_encoding, entry_count, and the record header's type/flags/inline_length | **re-emitted byte-identically** (§20.4, `[R-WRT-05]`) | bytes [136,229) and [112,120) are identical to the input's |
| Index **entry offsets** | **new** | 16, 20, 24 (were 16, 20, 320) |
| **Segment CRCs** | **recomputed** over the entries as re-emitted | `0xE2809825` (was `0x5BE1F50F`) |
| Layer record **extent slot** | **re-pointed** | extent_offset 28 (was 324); extent_length 84 unchanged |
| Layer record **crc_of_crc_array** | **updated** | `0x0339D21F` (was `0xE149E1EB`) |
| **Directory CRC** | recomputed | `0x373509AF` |
| **file_id**, **generation**, **trailer CRC** | new / reset / recomputed | `0x778899AABBCCDDEE`, 1, `0x39E619F5` |
| Dead space | **not carried** | 296 bytes gone |

The output's reference array equals the input live generation's bit for bit (`[R-WRT-07]`, `[R-MDL-02]`) — verified by my independent reader: same six coordinates, same p/q values, same fill at (1,2).

Because a compactor "preserves content, never placement", it may place structures anywhere; I chose the same gapless layout as generation 1, so the compacted file differs from the *original generation-1 file* in exactly 31 bytes: the three changed bytes of tile 2's payload (24–26), entry 2's crc (84–87), the segment CRC (108–111), crc_of_crc_array (229–232), the directory CRC (233–236), the file_id (304–311), and the trailer CRC (316–319).

**Verification depth** (`[R-WRT-09]`): the compactor relies on everything it copies, so before emitting any structure's bytes it must verify the open (§19.1), the layer record (§19.3), the full index chain — crc_of_crc_array *and* every segment CRC (`[R-IDX-04]`) — and every stored tile's entry crc. My builder did all of these.

---

## 4. Catalogue of legitimate writer divergence

`[R-CNF-05]`: "two conforming writers given identical input MAY produce different conforming files." Exhaustively, the axes are:

### 4.1 Container-level

1. **`file_id`** — any nonzero u64 (§6.2); `[R-LIF-03]` only SHOULDs a cryptographically random draw. Appendix G item 2 offers a deterministic hash alternative.
2. **`version_minor` above the floor** — `[R-CNT-26]` is a SHOULD; a higher minor yields a conforming file that "misstates the file's feature floor".
3. **Placement and interleaving order of a generation's structures** — stored-tile extents, tile-index regions, record extents, in any order (`[R-LIF-02]` step 2, `[R-SLB-05]`), *subject to* gaplessness (`[R-CNT-02]`/`[R-CNT-03]`), non-overlap (`[R-CNT-13]`), offset ≥ 16, and the directory being last before the pad (`[R-CNT-05]`).
4. **`dir_offset`** — hence the pre-trailer pad length (0–63) and F. Nothing forces a minimal pad.
5. **How many commits produce a given logical state** — one commit or many; `[R-LIF-07]` SHOULDs mid-stream checkpoint commits for very large writes. Generation count, per-generation sizes, and the resulting dead space are all writer-visible (`[R-PRV-03]`).
6. **Whether the file was created fresh or by append** — an appended file carries dead space, a compacted or freshly created one does not; both denote the same reference arrays.
7. **Record order within the directory** — `[R-CNT-14]`: "Record semantics MUST NOT depend on record order."
8. **Presence of optional records** — a file-scope user-metadata record, and per layer a user-metadata sub-record, are both optional.
9. **Whether the `[R-IDX-05]` all-sentinel constant is emitted or computed** — a freedom of *computation* only; the bytes are identical either way.

### 4.2 Layer declarations

10. **Layer, dimension, and channel names**, including Unicode normalization form (`[R-ENC-14]` is a SHOULD; byte-distinct names are distinct names, `[R-ENC-13]`).
11. **Dimension declaration order** — load-bearing but a writer's choice; §11.4's note describes column-major ecosystems declaring reversed order for zero-copy.
12. **Tile extents Tᵢ** — "Tile extents are a writer's choice, and this specification imposes none" (§11.3 note); the 1–16 MiB range is guidance only.
13. **Layout: interleaved vs planar** — both legal for any channel-type mix (`[R-SER-09]`). Byte-identical only for a single-channel *numeric* layer; a single-channel *bool* layer differs (⌈P/8⌉ vs P bytes, §14.4 note).
14. **Codec 1–4**, and *within* a chosen compressing codec, the encoder implementation, version, level, strategy, and thread count — RFC 1951/8878/LZ4 constrain decoders, not encoder choices (Appendix G item 1).
15. **Filter 1 or 2** — free, and orthogonal to codec.
16. **Alignment vs slab vs neither** — A = 0 or a power of two in [512, 2⁶²]; or S ≥ 1 with A_slab a power of two in [1, 2⁶²]; never both (`[R-CNT-16]`). This changes both offsets and the amount of declared padding. (Note: S = 1 with a small A_slab is a legal route to sub-512 per-tile alignment, since every run of one tile must start at an A_slab boundary — `[R-SLB-03]`.)
17. **Fill values** — `[R-TYP-10]` only SHOULDs all-zero when the caller does not choose; any bit pattern is valid for numeric types (`[R-TYP-05]`), `00`/`01` for bool (`[R-TYP-07]`).
18. **Which addressed tiles are stored vs. sentinel** — including *storing* a tile whose samples all equal fill; Appendix G item 6 has to *add* the all-fill-⇒-sentinel rule precisely because the core format leaves it free.
19. **Placement of runs relative to each other in a slab-declared layer**, and the gap sizes an alignment declaration leaves (`[R-SLB-03]`, `[R-SLB-01]`).

### 4.3 User metadata

20. **Presence, content, and encoding** (1 = none vs 2 = zstd), and the zstd encoder's settings.
21. **JSON serialization details** — whitespace, number formatting, string-escape choices. `[R-MTA-05]` fixes *member order* only and says so explicitly: "it does not make two writers' output identical … JSON number formatting varies by runtime."
22. **Application key namespace** — reverse-DNS prefixing is a SHOULD (`[R-MTA-06]`).

### 4.4 Updater / compactor

23. **A compactor's placement** of relocated structures, and its new `file_id`.
24. **Whether an updater drops a retained MU = 0, PE = 0 record** in a commit that modifies the scope the record attaches to (§20.4; SHOULD report the loss).

### 4.5 Explicitly *not* axes (closed by the format)

Byte order (`[R-ENC-01]`); every field width (`[R-ENC-06]`); in-tile sample order (row-major "for every linearization value, permanently", §11.4); index-entry order and the 20-byte entry (`[R-IDX-01]`); segment size 2¹⁶ (§15.4); the sentinel encoding (`[R-IDX-02]`); trailer size, offsets, and the front block (`[R-CNT-24]`, §6.1); record framing (§7.2); the fill field's length (`[R-CNT-23]`); **padding-position content** (fill, `[R-SER-05]`); **pad-bit content** (fill bit, `[R-SER-05]`); interleaved bool bytes (`[R-SER-08]`); declared-padding content (zero, `[R-CNT-03]`); JSON member order (`[R-MTA-05]`); on append, every unchanged index entry's bytes (`[R-WRT-04]`); on compaction, every stored tile's bytes, entry length, entry crc, and sentinel entry (`[R-WRT-07]`); and every retained record's bytes (`[R-WRT-05]`).

---

## Findings

### AMBIGUITY

**A1 — §9.2 `[R-LIF-02]` step 5 vs §6.2 `[R-CNT-05]`: "the next 64-byte boundary" when the directory already ends on one.**
`[R-LIF-02]` step 5 says "append the zero pad to the next 64-byte boundary and the new trailer." Readings the text permits in isolation: (i) *next* = the least 64-aligned offset ≥ the directory's end, so a directory ending at a multiple of 64 gets a zero-length pad; (ii) *next* = strictly greater, so such a directory gets a full 64-byte pad. **I picked (i)**, because `[R-CNT-05]` says only "fewer than 64 bytes" may lie between the directory's end and the trailer, and register row F13 makes "64 bytes or more" a file-scope violation. **Byte-level: NO** — reading (ii) is refuted by `[R-CNT-05]`/F13, so the spec accepts only one byte string. It cost me a re-read; a one-word fix ("to the least 64-aligned offset at or after the directory's end") would remove it.

**A2 — §16 `[R-SLB-05]` vs §5.2 `[R-CNT-02]`/`[R-CNT-03]`: may an unaligned, non-slab layer leave gaps between its structures?**
`[R-SLB-05]` says a layer declaring neither alignment nor a slab has stored tiles that "MAY occupy any non-overlapping byte positions, in any order … at no cost to conformance." Readings: (i) freedom of *ordering and relative position*, but the set of structures must still tile the generation's byte range with no unclaimed bytes; (ii) absolute placement freedom, gaps included. **I picked (i)** — `[R-CNT-02]` states "A file containing bytes claimed by no class is not a conforming file", `[R-CNT-03]`'s definition of declared padding is closed to exactly two kinds ("the alignment gaps of aligned or slab-declared layers (§16) and each generation's pre-trailer pad"), register row F10's Instances column repeats that closed list, and §16.1/§16.2 bother to declare *their* gaps as padding precisely because otherwise those gaps would be unclaimed. **Byte-level: NO** — reading (ii) is refuted. But this is the single highest-risk inference in the document for a writer implementer: nothing in §16 warns that "any byte positions" excludes leaving a hole, and a writer that pads tiles to, say, 64 bytes without declaring alignment produces a file that verifies as nonconforming under F9 with no reader ever noticing.

**A3 — §20.5 `[R-WRT-06]` + §6.3 `[R-CNT-26]`: which `version_minor` does a *compactor* write?**
`[R-CNT-26]` gives two rules — the *floor* ("the lowest version_minor that defines every feature present in the file") for a writer, and *max(floor, prior trailer's minor)* for "an appender". A compactor is neither: it produces a new file (new file_id, generation 1) yet `[R-WRT-06]` obliges it to copy the input's unknown ignore-lane flag bits forward, and it cannot know which minor version defines a bit it does not implement — so it cannot compute the floor. Readings: (i) emit the floor as this text computes it (0), knowingly understating; (ii) carry the input's minor forward, possibly overstating. **I picked (i)** for my compaction, which is byte-identical either way here because the input's minor is 0. **Byte-level: NO** — `[R-CNT-26]` is a SHOULD, so both outputs are conforming files, which makes this a writer-freedom axis (catalogued at §4.1 item 2) rather than a case where the spec mandates two different byte strings. It would become byte-level if `[R-CNT-26]` were tightened to a MUST.

**A4 — §20.5 `[R-WRT-07]`: "A compactor preserves content, never placement."**
Read once, the clause can be parsed as a prohibition ("placement must not be preserved") rather than as a disclaimer ("placement is not among the things preserved"). Readings: (i) the compactor is free to place structures anywhere, including at the same offsets they occupied in some earlier generation; (ii) the compactor must relocate. **I picked (i)**: reading (ii) has no operational content (no register row, no verifier check, and for a single-layer file "must differ" is unstateable), and `[R-SLB-05]`'s placement freedom applies to a compactor as a writer. My compacted output does in fact place tiles 0 and 1 at offsets 16 and 20 — the same offsets they held in generation 1 — which reading (ii) would forbid. **Byte-level: NO**, but only because reading (ii) is unenforceable; the sentence would be safer as "preserves content, but makes no placement promise."

**BYTE-LEVEL ambiguities: none.** Every byte of all three artifacts above was forced once my named choices (C1–C13) were made. The field order, widths, framing, value sequence, offset arithmetic, padding-position content, pad-bit rule, sentinel encoding, checksum extents, and every cross-check are pinned without inference, and §12.3's channel-entry example independently confirms the one framing (`u8 len + bytes` fill) I would otherwise have had to derive.

### CONTRADICTION

**C1 — §18.3 `[R-MTA-06]` vs §21.6's register row on unrecognized `tarn.` keys.**

- §18.3, `[R-MTA-06]`: "A file carrying an unrecognized `tarn.` key is **conforming** — later minor versions register keys, exactly as they define ignore-lane flag bits (§6.3), and this text's readers skip both harmlessly."
- §21.6, table row: "A user-metadata document carries a `tarn.`-prefixed key this specification does not define | **The file is nonconforming**, but a reader ignores that key and reads the rest of the document | `[R-MTA-06]`".

They cannot both hold of the same file: file conformance is "a pure predicate on bytes" (`[R-CNF-02]`), so a given byte sequence is conforming or it is not. The row even cites the requirement it contradicts. The break is sharper because §18.3 draws an explicit analogy to ignore-lane flag bits, and §21.6's *adjacent* row for that analogue gets it the other way ("An ignore-lane flag bit (16–31) is set | Ignored; **the file is conforming**"). Consequences for me as a writer: none byte-level (I emit no `tarn.` keys), but a verifier implementer cannot decide what verdict to certify, and neither a reader nor a verifier implementing this text can distinguish "a key registered by a later minor" (conforming per §18.3) from "a key registered by no version" (a writer violation per §18.3's own MUST NOT) — the two are byte-identical. A resolution is available if §21.1's precedence sentence ("where a row and the rule it cites diverge, the rule governs") is taken to cover §21.6 as well as §21.2–§21.5, which §21.1 does not say — its surrounding prose describes only the violation tables' six-column format. Under that resolution `[R-MTA-06]` governs and the file is conforming.

### OBSERVATION

**O1 — Prior generations' declared padding is neither live nor, literally, "dead space."** `[R-CNT-02]`'s three coverage classes are the front block, *a structure* (an enumerated list that includes the trailer but not padding), and *declared padding*. `[R-CNT-21]` then defines dead space as "**structures** of prior generations no longer reachable from the live trailer." A superseded generation's pre-trailer pad — 19 bytes at [237,256) in my file — is therefore unreachable but falls outside the defined term. No byte-level consequence (compaction drops it either way, and the output's own pad is mandated), but §23.1's privacy argument and §20.5's "dead space is never carried" both read as if the term covered it. Suggest `[R-CNT-21]` say "structures and declared padding".

**O2 — §5.2 names the tile-index region twice in one class list.** The structure class reads "stored-tile extent, tile-index region, record extent (bytes referenced by a record's extent slot, §7.2 — in format major 1, tile-index regions and user-metadata extents), directory, or trailer". A tile-index region is simultaneously the second alternative and an instance of the third. Since both are sub-kinds of the same class, "exactly one of" is not actually violated, but the sentence takes two readings to settle. Suggest dropping the standalone "tile-index region" alternative, since the parenthetical already covers it.

**O3 — The error register has unexplained row-number gaps: F6, F39, L40.** I counted the register mechanically: 43 file rows (numbered 1–45), 47 layer rows (1–48), 26 tile rows, 10 ignore rows = **126 rows over 235 named instances**, which matches §21.2's "43 conditions", §21.3's "47", §21.4's "26", and §21.8's "126 conditions over 235 named instances" exactly. So the counts are sound. But §2.2's retirement discipline is stated for `[R-…]` identifiers only, and §14.4 announces `[R-SER-04]`'s withdrawal in prose — nothing announces the three register gaps. Since §21.1 declares the register's "completeness is normative" and `[R-ERR-02]`/`[R-VEC-03]` make corpus coverage row-indexed, an implementer auditing the corpus cannot tell whether F6/F39/L40 were withdrawn or lost in editing. A one-line note ("rows F6, F39, and L40 are withdrawn and permanently retired") would close it.

**O4 — §21.5 row R10 sits in a table §21.1 calls an enumeration of violations, while §21.6 lists the identical condition as not a violation.** "An unknown record type carries MU = 0" appears as register row R10 (outcome ignore-record) and again in §21.6 ("defined behaviors, not errors"). §21.1's blanket "each row is one malformed condition" is therefore false of R10. This is *resolved* elsewhere — §2.4 says "The same vocabulary is used for defined conditions that are not violations", and `[R-VEC-02]` says outright that "a conforming file can carry a record a reader ignores (§21.5, §21.6)" — so no implementer is left guessing, but §21.1's characterizing sentence needs the same hedge. (I checked R1–R9: those are genuine violations, so the anomaly is confined to R10.)

**O5 — Disproportionately expensive, but decidable: the whole-file overlap and coverage checks.** `[R-CNT-13]`'s "extents are owned exactly once" and `[R-LIF-08]`'s generation attribution require, respectively, whole-directory knowledge and a full backward 64-aligned magic scan with chain selection over all generations. For my 640-byte two-generation file this is trivial; at 65,536 layers × 2³² entries (the §21.9 guarantees) an overlap check is a sort over ~2⁴⁸ extents. The spec is right to bind these to verifiers only and to exempt readers explicitly, and it says so — this is a note for implementers budgeting a verifier, not a defect.

**O6 — A back door worth knowing about, and possibly worth a note in §16.** `[R-CNT-16]` makes per-tile alignment and slabs mutually exclusive, and `[R-SLB-01]` floors alignment at 512. But a layer declaring S = 1 with A_slab = 64 gets every run reduced to a single tile, and `[R-SLB-03]` requires "the first stored tile's offset satisfies offset mod A_slab = 0" — i.e. *every* stored tile is 64-aligned. So sub-512 per-tile alignment is expressible after all, via the slab machinery. This is consistent (nothing is violated) and is arguably the intended answer to a writer that needs 8- or 64-byte alignment, since Finding A2 means such a writer otherwise cannot leave gaps at all. Stating it in §16.2's note would save an implementer the derivation.

**O7 — The 128-byte minimum file size is asserted only in non-normative text.** §5.1's "Example", Appendix B, and Appendix A all give 128, and register row F8 makes a shorter file reject-file citing `[R-CNT-01]` — but `[R-CNT-01]` itself only says F equals committed_file_length and is a multiple of 64. The number is derivable from `[R-CNT-06]`'s gates (dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64 ⇒ F ≥ 84; F ≡ 0 mod 64 ⇒ F ≥ 128), so nothing is missing — but F8's Condition column states the bound as though it were a stated rule, and a reader implementing from F8 alone would look for one.

---

## Verdict

IMPLEMENTABLE: yes
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high
