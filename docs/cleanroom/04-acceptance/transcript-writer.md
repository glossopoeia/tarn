# TARN WRITER cleanroom — byte-exact construction of layer `q`

Source: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, read in full. No other file, no git, no web.

**Method note.** I implemented CRC-32C from §4.5's stated parameters alone (Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian) and validated it against three independent constants the spec publishes before using it: CRC-32C(`"123456789"`) = `0xE3069283` (§4.5), CRC-32C of zero bytes = `0x00000000` (§4.5), and the full all-sentinel segment constant `0xEECB3BB2` (§15.4, `[R-IDX-05]`). All three reproduce. I then also reproduced Appendix A's trailer CRC `0xE00938D2` from its own field values. Every file below was afterwards re-walked by an independently written reader implementing §19.1's open, §15.4's chain, §14's offset arithmetic, §9.7's coverage partition and §5.2's dead-space count — it reports zero unclaimed bytes in generation 1 and the dead totals stated below.

---

## 1. Generation 1 — creation

### 1.1 Declarations and everything derived from them

| Quantity | Value | Rule |
|---|---|---|
| rank *d* | 2, dims declared **y** then **x** | §7.4, §3.1 (declared order load-bearing) |
| extents E | (E_y, E_x) = (3, 4) | §11.1 |
| tile extents T | (T_y, T_x) = (2, 2) | §11.1 |
| grid counts G | G_y = ⌈3/2⌉ = 2, G_x = ⌈4/2⌉ = 2 | `[R-GEO-03]` |
| spatial tile count N | 2 × 2 = **4** | `[R-GEO-03]` |
| positions per tile P | 2 × 2 = **4** | `[R-GEO-03]` |
| channels C | 2 — `a` uint16 (type 7, B=2), `f` bool (type 1, B=1) | §12.1 |
| addressed tiles | interleaved ⇒ N = **4** ⇒ `entry_count` = 4 | `[R-GEO-03]`, `[R-CNT-17]` |
| sample stride Q | B_a + B_f = 2 + 1 = **3** | `[R-SER-02]` |
| in-sample offsets F | F_a = 0, F_f = 2 | `[R-SER-02]` |
| decoded size | P · Q = 4 × 3 = **12 bytes/tile** | `[R-SER-02]` |
| stored length | codec 1 ⇒ **must equal 12** | `[R-COD-04]` |
| index region length | 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 80 + 4 = **84** | `[R-CNT-17]`, §15.1 |
| in-tile ordinal | u_y·T_x + u_x = u_y·2 + u_x | `[R-GEO-06]` (last-declared varies fastest) |
| spatial ordinal s | t_y·G_x + t_x = t_y·2 + t_x | `[R-GEO-06]`, linearization 1 |
| disk ordinal | = s (interleaved) | `[R-GEO-06]` |

Padding (§11.3): G_y·T_y = 4 > E_y = 3, so coordinate **y = 3 is padding**; G_x·T_x = 4 = E_x, so x has none.

Sample encodings, little-endian per `[R-ENC-01]`:
- real sample = `a`=0x0102 → `02 01`, then `f`=true → `01` ⇒ **`02 01 01`**
- padding position = each channel's *fill* (`[R-SER-05]`): `a` fill `FF FF`, `f` fill byte `00` ⇒ **`FF FF 00`**

### 1.2 The four stored tiles — decoded images including padding positions

Value sequence is sample-major, channel values adjacent in declared order (`[R-SER-01]`); byte offset of channel *c* at in-tile ordinal *u* is u·Q + F_c (`[R-SER-02]`).

**s = 0** — tile (t_y,t_x) = (0,0), offset 16, CRC `0x49743679`
`02 01 01  02 01 01  02 01 01  02 01 01`

| k | (u_y,u_x) | (y,x) | kind | bytes |
|---|---|---|---|---|
| 0 | (0,0) | (0,0) | real | `02 01 01` |
| 1 | (0,1) | (0,1) | real | `02 01 01` |
| 2 | (1,0) | (1,0) | real | `02 01 01` |
| 3 | (1,1) | (1,1) | real | `02 01 01` |

**s = 1** — tile (0,1), offset 28, CRC `0x49743679` — byte-identical to s=0; covers (y 0–1, x 2–3), all real.

**s = 2** — tile (1,0), offset 40, CRC `0xFA3F5563`
`02 01 01  02 01 01  FF FF 00  FF FF 00`

| k | (u_y,u_x) | (y,x) | kind | bytes |
|---|---|---|---|---|
| 0 | (0,0) | (2,0) | real | `02 01 01` |
| 1 | (0,1) | (2,1) | real | `02 01 01` |
| 2 | (1,0) | (**3**,0) | **padding** | `FF FF 00` (fill) |
| 3 | (1,1) | (**3**,1) | **padding** | `FF FF 00` (fill) |

**s = 3** — tile (1,1), offset 52, CRC `0xFA3F5563` — byte-identical to s=2; covers (y 2–3, x 2–3), with y=3 padding.

### 1.3 Every byte of generation 1 (F₁ = 384)

```
00000000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
00000010  02 01 01 02 01 01 02 01  01 02 01 01 02 01 01 02
00000020  01 01 02 01 01 02 01 01  02 01 01 02 01 01 FF FF
00000030  00 FF FF 00 02 01 01 02  01 01 FF FF 00 FF FF 00
00000040  10 00 00 00 00 00 00 00  0C 00 00 00 00 00 00 00
00000050  79 36 74 49 1C 00 00 00  00 00 00 00 0C 00 00 00
00000060  00 00 00 00 79 36 74 49  28 00 00 00 00 00 00 00
00000070  0C 00 00 00 00 00 00 00  63 55 3F FA 34 00 00 00
00000080  00 00 00 00 0C 00 00 00  00 00 00 00 63 55 3F FA
00000090  5B B7 3A B1 01 00 03 00  62 00 00 00 40 00 00 00
000000A0  00 00 00 00 54 00 00 00  00 00 00 00 01 71 01 01
000000B0  00 01 00 01 00 00 00 00  00 00 00 00 00 00 00 00
000000C0  00 00 00 00 00 00 00 00  00 00 00 00 00 02 02 00
000000D0  01 79 03 00 00 00 00 00  00 00 02 00 00 00 00 00
000000E0  00 00 01 78 04 00 00 00  00 00 00 00 02 00 00 00
000000F0  00 00 00 00 01 61 07 00  02 FF FF 01 66 01 00 01
00000100  00 01 04 00 00 00 00 00  00 00 69 CA 93 4A 3B B9
00000110  B0 06 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000120  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000130  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000140  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
00000150  01 00 00 00 00 00 00 00  94 00 00 00 00 00 00 00
00000160  7E 00 00 00 00 00 00 00  80 01 00 00 00 00 00 00
00000170  EF CD AB 89 67 45 23 01  00 00 00 00 76 E1 88 5E
```

**Label table.**

| Bytes | Hex | Meaning |
|---|---|---|
| [0,8) | `89 54 41 52 4E 0D 0A 1A` | front signature magic, §6.1 |
| [8,16) | zero ×8 | front signature reserved, §6.1 |
| [16,28) | `02 01 01 …` | stored tile s=0 (§14) |
| [28,40) | `02 01 01 …` | stored tile s=1 |
| [40,52) | `02 01 01 02 01 01 FF FF 00 FF FF 00` | stored tile s=2 |
| [52,64) | same | stored tile s=3 |
| **[64,148)** | | **tile-index region**, `entry_count`×20 + 1×4, §15.1 |
| [64,72) | `10 00 …` | entry 0 offset = 16 |
| [72,80) | `0C 00 …` | entry 0 length = 12 |
| [80,84) | `79 36 74 49` | entry 0 crc = 0x49743679 |
| [84,104) | `1C…`, `0C…`, `79 36 74 49` | entry 1: offset 28, length 12 |
| [104,124) | `28…`, `0C…`, `63 55 3F FA` | entry 2: offset 40, length 12, crc 0xFA3F5563 |
| [124,144) | `34…`, `0C…`, `63 55 3F FA` | entry 3: offset 52, length 12 |
| [144,148) | `5B B7 3A B1` | segment-CRC array, 1 segment: CRC-32C over region [0,80) = **0xB13AB75B** (§15.4; partial segment covers only its actual bytes) |
| **[148,274)** | | **directory region**, `dir_length` = 126, §7.1 |
| [148,150) | `01 00` | record type 0x0001 = layer |
| [150,152) | `03 00` | flags MU=1 PE=1 (§7.3 fixes these) |
| [152,156) | `62 00 00 00` | inline_length = 98 |
| [156,164) | `40 00 …` | extent_offset = 64 (the index region) |
| [164,172) | `54 00 …` | extent_length = 84 |
| [172,174) | `01 71` | layer name "q" (len 1) |
| [174,175) | `01` | layout = 1 interleaved |
| [175,177) | `01 00` | linearization = 1 row-major |
| [177,179) | `01 00` | codec = 1 none |
| [179,181) | `01 00` | filter = 1 none |
| [181,189) | zero ×8 | alignment A = 0 (none declared) |
| [189,197) | zero ×8 | slab S = 0 |
| [197,205) | zero ×8 | A_slab = 0 (forced by `[R-CNT-23]` when S = 0) |
| [205,206) | `02` | rank d = 2 |
| [206,208) | `02 00` | channel count C = 2 |
| [208,210) | `01 79` | dim 0 name "y" |
| [210,218) | `03 00 …` | E_y = 3 |
| [218,226) | `02 00 …` | T_y = 2 |
| [226,228) | `01 78` | dim 1 name "x" |
| [228,236) | `04 00 …` | E_x = 4 |
| [236,244) | `02 00 …` | T_x = 2 |
| [244,246) | `01 61` | channel 0 name "a" |
| [246,248) | `07 00` | type 7 = uint16 |
| [248,249) | `02` | fill length 2 = element size (`[R-CNT-23]`) |
| [249,251) | `FF FF` | fill for `a` |
| [251,253) | `01 66` | channel 1 name "f" |
| [253,255) | `01 00` | type 1 = bool |
| [255,256) | `01` | fill length 1 |
| [256,257) | `00` | fill for `f` = false (`[R-TYP-07]` admits only 0x00/0x01) |
| [257,258) | `01` | index_encoding = 1 raw-segmented |
| [258,266) | `04 00 …` | entry_count = 4 |
| [266,270) | `69 CA 93 4A` | crc_of_crc_array = **0x4A93CA69** (CRC-32C over [144,148)) |
| — | (none) | zero sub-records — inline payload ends exactly here (`[R-CNT-18]`) |
| [270,274) | `3B B9 B0 06` | directory CRC = **0x06B0B93B** over [148,270) |
| [274,320) | zero ×46 | pre-trailer pad, `[R-CNT-05]`/`[R-CNT-03]` (46 < 64) |
| **[320,384)** | | **trailer**, §6.2 |
| [320,328) | `8A 4E 52 41 54 0D 0A 1A` | trailer magic |
| [328,330) | `01 00` | version_major = 1 |
| [330,332) | `00 00` | version_minor = 0 (`[R-CNT-26]` floor) |
| [332,336) | `00 00 00 00` | flags = 0 (`[R-CNT-08]` MUST for a writer under this text) |
| [336,344) | `01 00 …` | generation = 1 |
| [344,352) | `94 00 …` | dir_offset = 148 |
| [352,360) | `7E 00 …` | dir_length = 126 |
| [360,368) | `80 01 …` | committed_file_length = 384 (384 mod 64 = 0) |
| [368,376) | `EF CD AB 89 67 45 23 01` | file_id = 0x0123456789ABCDEF |
| [376,380) | `00 00 00 00` | reserved, zero |
| [380,384) | `76 E1 88 5E` | trailer CRC = **0x5E88E176** over [320,380) |

Coverage (`[R-CNT-02]`, §9.7): 16 + 48 + 84 + 126 + 46 + 64 = 384 = F. **Zero dead bytes.** Verified by walk.

### 1.4 Every value I had to choose

| Choice | Value used | Freedom |
|---|---|---|
| `file_id` | 0x0123456789ABCDEF | any nonzero; §9.3 SHOULD be cryptographically random |
| structure order within `[R-LIF-02]` step 2 | 4 tile payloads in disk-ordinal order, then the index region | "in any order" (`[R-LIF-02]`, `[R-SLB-05]`) |
| tile offsets | 16, 28, 40, 52 — packed, gapless | free but gapless: undeclared gaps would be dead space, a writer defect (`[R-SLB-05]`) |
| index region offset | 64 | free |
| directory offset | 148 | free; pad length is then *forced* to 46 by F mod 64 = 0 |
| pre-trailer pad | 46 zero bytes | forced once dir end is chosen (`[R-CNT-05]`) |
| directory contents | exactly one record | no user-metadata record emitted (§18.1 says MAY) |
| sub-records | none | MAY (§7.4) |
| `version_minor` | 0 | `[R-CNT-26]` SHOULD-floor |
| storing s=2 and s=3 rather than sentinels | stored | forced by the charter; both conform. Appendix G item 6 would sentinel an *all-fill* tile — these are not all-fill |

Everything else in the file is **forced** by the declarations: all four CRCs, the 12-byte decoded size, the `02 01 01` / `FF FF 00` sample bytes, the padding content, the 84-byte index length, the 20-byte entry layout, `A_slab` = 0, the record flags `03 00`, and the trailer's field values.

---

## 2. Generation 2 — grow E_y from 3 to 5, commit

New geometry: E = (5, 4), T unchanged ⇒ G_y = ⌈5/2⌉ = **3**, G_x = 2, **N = 6**, `entry_count` = 6, index region = 6×20 + 4 = **124**. P, Q and the decoded size are unchanged (12), because tile extents did not change.

**Ordinal renumbering.** s = t_y·G_x + t_x and G_x is unchanged, so tiles 0–3 keep disk ordinals 0–3 and their entries are carried **byte-identical at their disk-ordinal position** (`[R-GEO-06]`, §20.3 step 4). New tiles: (t_y,t_x) = (2,0) → s = 4 and (2,1) → s = 5. I emit both as **sentinels** — they carry no caller data, so they read as fill (`[R-TYP-08]`). This is a writer choice; storing all-fill tiles instead would also conform.

Extent growth is metadata-only (§11.1 rationale): no tile payload is re-emitted. Writing begins at **exactly F₁ = 384** (`[R-LIF-02]` step 1).

### 2.1 Appended bytes [384, 704) — 320 bytes

```
00000180  10 00 00 00 00 00 00 00  0C 00 00 00 00 00 00 00
00000190  79 36 74 49 1C 00 00 00  00 00 00 00 0C 00 00 00
000001A0  00 00 00 00 79 36 74 49  28 00 00 00 00 00 00 00
000001B0  0C 00 00 00 00 00 00 00  63 55 3F FA 34 00 00 00
000001C0  00 00 00 00 0C 00 00 00  00 00 00 00 63 55 3F FA
000001D0  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
000001E0  00 00 00 00 FF FF FF FF  FF FF FF FF FF FF FF FF
000001F0  FF FF FF FF 00 00 00 00  44 4A 1F A8 01 00 03 00
00000200  62 00 00 00 80 01 00 00  00 00 00 00 7C 00 00 00
00000210  00 00 00 00 01 71 01 01  00 01 00 01 00 00 00 00
00000220  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000230  00 00 00 00 00 02 02 00  01 79 05 00 00 00 00 00
00000240  00 00 02 00 00 00 00 00  00 00 01 78 04 00 00 00
00000250  00 00 00 00 02 00 00 00  00 00 00 00 01 61 07 00
00000260  02 FF FF 01 66 01 00 01  00 01 06 00 00 00 00 00
00000270  00 00 D7 DF 96 D8 78 CA  E4 C7 00 00 00 00 00 00
00000280  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
00000290  02 00 00 00 00 00 00 00  FC 01 00 00 00 00 00 00
000002A0  7E 00 00 00 00 00 00 00  C0 02 00 00 00 00 00 00
000002B0  EF CD AB 89 67 45 23 01  00 00 00 00 CA 24 54 C9
```

| Bytes | Hex | Meaning |
|---|---|---|
| [384,464) | entries 0–3 | **byte-identical** to gen 1's entries 0–3 (offsets 16/28/40/52, lengths 12, crcs 0x49743679 ×2, 0xFA3F5563 ×2) |
| [464,484) | `FF ×16 00 ×4` | entry 4 — sentinel (`[R-IDX-02]`), tile (2,0) unstored |
| [484,504) | `FF ×16 00 ×4` | entry 5 — sentinel, tile (2,1) unstored |
| [504,508) | `44 4A 1F A8` | segment CRC over the 120 entry bytes = **0xA81F4A44**. Partial segment (6 of 65 536), so it is *computed*, never the `0xEECB3BB2` constant (`[R-IDX-05]`) |
| [508,510) | `01 00` | layer record type |
| [510,512) | `03 00` | flags MU=1 PE=1 |
| [512,516) | `62 00 00 00` | inline_length = 98 (unchanged) |
| [516,524) | `80 01 …` | extent_offset = **384** (new index region) |
| [524,532) | `7C 00 …` | extent_length = **124** (`[R-CNT-17]`: 6×20 + 4) |
| [532,630) | inline payload | identical to gen 1's **except three fields** |
| ↳ [570,578) | `05 00 …` | **E_y = 5** (was `03`) |
| ↳ [618,626) | `06 00 …` | **entry_count = 6** (was `04`) |
| ↳ [626,630) | `D7 DF 96 D8` | **crc_of_crc_array = 0xD896DFD7** (was 0x4A93CA69) |
| [630,634) | `78 CA E4 C7` | directory CRC = **0xC7E4CA78** |
| [634,640) | zero ×6 | pre-trailer pad (`[R-CNT-05]`) |
| [640,648) | `8A 4E …` | trailer magic |
| [648,652) | `01 00 00 00` | version_major 1, version_minor 0 (`[R-CNT-26]`: max(floor 0, prior 0)) |
| [652,656) | `00 00 00 00` | flags = 0; no unknown ignore-lane bits to copy forward (`[R-CNT-08]`) |
| [656,664) | `02 00 …` | **generation = 2** (exactly one greater) |
| [664,672) | `FC 01 …` | dir_offset = 508 |
| [672,680) | `7E 00 …` | dir_length = 126 |
| [680,688) | `C0 02 …` | committed_file_length = **704** (704 mod 64 = 0) |
| [688,696) | `EF CD AB 89 67 45 23 01` | **same file_id** (`[R-LIF-03]`) |
| [696,700) | zero | reserved |
| [700,704) | `CA 24 54 C9` | trailer CRC = **0xC95424CA** |

### 2.2 Exactly what becomes dead

Dead space = every byte the live state no longer reaches (§5.2, `[R-CNT-21]`). After this commit that is the contiguous range **[64, 384) = 320 bytes**, namely:

| Range | Size | What it was |
|---|---|---|
| [64,148) | 84 | generation 1's tile-index region — **superseded** by [384,508) |
| [148,274) | 126 | generation 1's directory — superseded by [508,634) |
| [274,320) | 46 | generation 1's pre-trailer pad |
| [320,384) | 64 | generation 1's trailer |

**Nothing else becomes dead.** The front block [0,16) and all four tile payloads [16,64) remain live — reachable through the new directory's new index region, whose entries 0–3 still point at offsets 16/28/40/52. Live gen-2 state: 16 + 48 + 124 + 126 + 6 + 64 = 384 bytes; 384 live + 320 dead = 704 = F₂. Verified by walk.

### 2.3 The semantic consequence, which the growth makes unavoidable

y = 3 was padding in generation 1 and is a **real coordinate** in generation 2. Tiles s=2 and s=3 were not re-emitted, so the bytes now decoded at y=3 are the ones `[R-SER-05]` compelled the writer to put there: `FF FF 00` — i.e. exactly `a`'s fill 0xFFFF and `f`'s fill false. The reference array (§3.2) after this commit:

```
y=0..2, x=0..3 : a=0x0102 f=true      (stored, unchanged)
y=3,    x=0..3 : a=0xFFFF f=false     (former padding, now real — reads as fill)
y=4,    x=0..3 : a=0xFFFF f=false     (tiles s=4,s=5 sentinel — reads as fill)
```

The newly addressed *sentinel* rows and the newly exposed *former-padding* row read identically. That is not a coincidence: `[R-SER-05]`'s fill-encoded padding is what makes extent growth semantically seamless. A writer that violated `[R-SER-05]` (a tile-scope, verifier-only violation, register row T4) would leak arbitrary bytes into the array the moment an extent grew past them.

---

## 3. Generation 3 — store a non-fill value into a newly addressed tile

I store tile **s = 4**, tile coordinates (t_y,t_x) = (2,0), covering y ∈ {4,5}, x ∈ {0,1}. E_y = 5 ⇒ **y = 5 is padding**. Values stored at the two real positions: `a` = 0x0102, `f` = true — both non-fill.

Decoded image (12 bytes), CRC-32C = **0xFA3F5563**:

| k | (u_y,u_x) | (y,x) | kind | bytes |
|---|---|---|---|---|
| 0 | (0,0) | (4,0) | real | `02 01 01` |
| 1 | (0,1) | (4,1) | real | `02 01 01` |
| 2 | (1,0) | (**5**,0) | padding | `FF FF 00` |
| 3 | (1,1) | (**5**,1) | padding | `FF FF 00` |

The layer's stored-tile set changes, so the **whole index region is re-emitted** (§20.3 step 4) — entries 0–3 byte-identical, entry 4 re-pointed, entry 5 still sentinel. Writing begins at exactly F₂ = 704.

### 3.1 Appended bytes [704, 1088) — 384 bytes

```
000002C0  02 01 01 02 01 01 FF FF  00 FF FF 00 10 00 00 00
000002D0  00 00 00 00 0C 00 00 00  00 00 00 00 79 36 74 49
000002E0  1C 00 00 00 00 00 00 00  0C 00 00 00 00 00 00 00
000002F0  79 36 74 49 28 00 00 00  00 00 00 00 0C 00 00 00
00000300  00 00 00 00 63 55 3F FA  34 00 00 00 00 00 00 00
00000310  0C 00 00 00 00 00 00 00  63 55 3F FA C0 02 00 00
00000320  00 00 00 00 0C 00 00 00  00 00 00 00 63 55 3F FA
00000330  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF
00000340  00 00 00 00 C7 17 AC 46  01 00 03 00 62 00 00 00
00000350  CC 02 00 00 00 00 00 00  7C 00 00 00 00 00 00 00
00000360  01 71 01 01 00 01 00 01  00 00 00 00 00 00 00 00
00000370  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000380  00 02 02 00 01 79 05 00  00 00 00 00 00 00 02 00
00000390  00 00 00 00 00 00 01 78  04 00 00 00 00 00 00 00
000003A0  02 00 00 00 00 00 00 00  01 61 07 00 02 FF FF 01
000003B0  66 01 00 01 00 01 06 00  00 00 00 00 00 00 FD 3D
000003C0  3F 9C 5C 84 52 B4 00 00  00 00 00 00 00 00 00 00
000003D0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
000003E0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
000003F0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
00000400  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
00000410  03 00 00 00 00 00 00 00  48 03 00 00 00 00 00 00
00000420  7E 00 00 00 00 00 00 00  40 04 00 00 00 00 00 00
00000430  EF CD AB 89 67 45 23 01  00 00 00 00 15 7F 6A A6
```

| Bytes | Hex | Meaning |
|---|---|---|
| [704,716) | `02 01 01 02 01 01 FF FF 00 FF FF 00` | **new stored tile s=4**; length 12 = decoded size (`[R-COD-04]`) |
| [716,796) | entries 0–3 | byte-identical to both prior generations |
| [796,804) | `C0 02 …` | entry 4 offset = **704** |
| [804,812) | `0C 00 …` | entry 4 length = 12 |
| [812,816) | `63 55 3F FA` | entry 4 crc = 0xFA3F5563 |
| [816,836) | `FF ×16 00 ×4` | entry 5 — still sentinel |
| [836,840) | `C7 17 AC 46` | segment CRC = **0x46AC17C7** (recomputed) |
| [840,842) | `01 00` | layer record type |
| [842,844) | `03 00` | flags |
| [844,848) | `62 00 00 00` | inline_length = 98 |
| [848,856) | `CC 02 …` | extent_offset = **716** |
| [856,864) | `7C 00 …` | extent_length = 124 |
| [864,962) | inline payload | **identical to generation 2's except one field** |
| ↳ [958,962) | `FD 3D 3F 9C` | **crc_of_crc_array = 0x9C3F3DFD** |
| [962,966) | `5C 84 52 B4` | directory CRC = **0xB452845C** |
| [966,1024) | zero ×58 | pre-trailer pad |
| [1024,1032) | `8A 4E …` | trailer magic |
| [1032,1036) | `01 00 00 00` | major 1, minor 0 |
| [1036,1040) | `00 00 00 00` | flags = 0 |
| [1040,1048) | `03 00 …` | **generation = 3** |
| [1048,1056) | `48 03 …` | dir_offset = 840 |
| [1056,1064) | `7E 00 …` | dir_length = 126 |
| [1064,1072) | `40 04 …` | committed_file_length = **1088** |
| [1072,1080) | `EF CD AB 89 67 45 23 01` | same file_id |
| [1080,1084) | zero | reserved |
| [1084,1088) | `15 7F 6A A6` | trailer CRC = **0xA66A7F15** |

Newly dead: generation 2's index region [384,508), directory [508,634), pad [634,640) and trailer [640,704) — 320 more bytes. **Total dead after generation 3: [64, 704) = 640 bytes**, against 448 live. Reference array:

```
y=0..2 : a=0x0102 f=true  ×4
y=3    : a=0xFFFF f=false ×4
y=4    : a=0x0102 f=true (x=0,1)   a=0xFFFF f=false (x=2,3 — tile s=5 still sentinel)
```

---

## 4. Every axis on which two conforming writers may legitimately differ

Grouped by what makes the freedom legitimate. `[R-CNF-05]`: "two conforming writers given identical input MAY produce different conforming files."

**A. Explicitly unconstrained values**
1. `file_id` — any nonzero u64 (§6.2, §9.3 SHOULD-randomness only).
2. Fill value when the caller does not choose one — `[R-TYP-10]` SHOULDs all-zero; a different default is conforming and changes what unwritten regions read as.
3. `version_minor` — `[R-CNT-26]` is a SHOULD; a higher minor is conforming.
4. Unicode normalization form of names — `[R-ENC-14]` is a SHOULD; NFC and NFD names are *different names* under `[R-ENC-13]`.

**B. Placement and ordering (byte positions, never content)**
5. Order of tile payloads, index regions and record extents within `[R-LIF-02]` step 2 — any order (`[R-SLB-05]`).
6. On-disk offsets of stored tiles — any non-overlapping positions, any order relative to disk ordinals, subject only to gaplessness when no alignment/slab is declared.
7. Order of records within the directory — record order carries no meaning (`[R-CNT-14]`); Appendix G item 3 must *invent* a total order to close this.
8. Where the directory starts — which then forces, but does not fix, the pre-trailer pad length (0–63 bytes).
9. Whether `dir_length` + pad + 64 fits the 65,536-byte discovery window — `[R-CNT-09]` is a SHOULD.

**C. Declarations that change bytes without changing the reference array**
10. Codec 1–4, and, for codecs 2–4, the encoder implementation, version and settings (level, strategy, thread count) — Appendix G item 1 calls this the profile's real boundary.
11. Filter 1 or 2.
12. Channel layout interleaved vs planar — a single-channel bool layer differs even in *length* (⌈P/8⌉ vs P, §14.4 note).
13. Tile extents — §11.3 imposes none ("Tiles far outside that range remain conforming").
14. Per-tile alignment A, or slab S with A_slab — mutually exclusive (`[R-CNT-16]`), each changing placement and introducing declared padding.
15. Whether the layer carries sub-records, and whether a file- or layer-scope user-metadata record exists at all.
16. User-metadata encoding (1 none / 2 zstd), and JSON number formatting and whitespace — `[R-MTA-05]` makes *one* writer reproducible and explicitly does not make two writers agree.

**D. Sparsity and storedness — same reference array, different files**
17. Whether an **all-fill tile** is stored or sentinelled — Appendix G item 6 has to pin this precisely because both conform.
18. Whether a *partially* fill tile is stored (it must be, to carry its non-fill samples) — no freedom there, but which tiles a writer chooses to populate in a given generation is free.
19. For a full all-sentinel segment, whether the CRC is computed or the `0xEECB3BB2` constant is emitted (`[R-IDX-05]`) — same bytes, but a genuine implementation choice; for a *partial* segment it MUST be computed.

**E. Commit shaping — the history, not the live array**
20. How many commits the same logical result takes (my Tasks 2 and 3 could have been one commit), which changes generation numbers and the dead-space total.
21. Whether intermediate checkpoint commits are emitted during a large write — `[R-LIF-07]` SHOULD.
22. Whether unchanged payloads are re-emitted anyway. Concretely at Task 2: a writer may re-emit tiles s=2 and s=3 (their padding set changed from two positions to none). Because padding was already fill-encoded, the *re-emitted payload bytes are identical* — so the only difference is placement, plus 24 more bytes of dead space.
23. Whether an unchanged layer's index region is re-emitted (permitted — it supersedes the old one) or its extent slot reused (§20.3).
24. Truncate-to-F-first vs overwrite-from-F-then-truncate when a physical file is longer than F (`[R-LIF-04]`) — identical committed bytes, different conduct.
25. Whether to drop an MU = 0, PE = 0 record when modifying the scope it attaches to (§20.4 table).
26. A compactor's output placement, which `[R-WRT-07]` frees entirely ("A compactor preserves content but not placement").

**F. Not freedoms, though they look like them**
Dimension *declaration order* changes which axis is which (§11.4's note on column-major ecosystems) — that is a different reference array, not a different encoding of the same one. And `linearization` (only 1), `index_encoding` (only 1), `flags` (must be 0), `A_slab` when S = 0 (must be 0), and both record-header flag bits on registered types are fixed, not chosen.

---

## Findings

### BYTE-LEVEL AMBIGUITY

**None.** Every byte of all three generations above is either forced by the declarations or falls under a freedom the specification names explicitly. I actively tried to break the following and failed:

- *In-tile and tile ordinals for d = 2.* §11.4's Σᵢ uᵢ·∏_{j>i}Tⱼ and Σᵢ tᵢ·∏_{j>i}Gⱼ, the prose gloss "the last-declared dimension varies fastest", and §11.4's worked example (300,700)→ordinal 11,452, tile s=10 all agree. Reproduced numerically.
- *Interleaved value order and the bool element size.* `[R-SER-01]`'s "value k … channel (k mod C) at in-tile ordinal k div C" and `[R-SER-02]`'s offset table (k div C)·Q + F_{k mod C} are algebraically the same map; "1 for bool" is stated twice (§12.1, §14.2). §14.2's `t`(float32)+`m`(bool) example pins Q = 5 for a mixed case. Reproduced.
- *Padding content in a mixed interleaved tile.* `[R-SER-05]` names each case separately ("the recorded fill bytes for a numeric channel, the recorded fill byte for an interleaved bool channel"). No gap.
- *Ordinal renumbering on extent growth.* §20.3's "every other entry byte-identical at its disk-ordinal position" could be read as "leave the entry where it sits", but the parenthetical "(a geometry change renumbers ordinals, `[R-GEO-06]`)" plus `[R-IDX-01]`'s structural mapping (entry k *is* the tile with disk ordinal k) forecloses it. Searched: `grep -n "renumber\|disk-ordinal position"` — two hits, both in §20.3 step 4, both resolving it.
- *Whether growth obliges re-emitting tiles whose padding set changed.* Searched every occurrence of "grow"/"growth" (12 hits). §11.1's rationale calls extent growth "a metadata-only operation"; §20.3 step 4 obliges re-emission of the *index*, and of payloads only for "tiles this commit stores or supersedes"; `[R-SLB-04]` handles slab declarations under growth and nothing else does. Determined: no payload obligation.
- *Pre-trailer pad length.* `[R-CNT-05]` (< 64, none when already aligned) plus F mod 64 = 0 makes it exactly (−dir_end) mod 64. No latitude.
- *Index region length and the partial segment CRC.* `[R-CNT-17]`'s formula, §15.1's layout and §15.4's "the final partial segment's CRC covers only its actual bytes" agree; `[R-IDX-05]` explicitly forbids substituting the all-sentinel constant for a partial segment.

### CONTRADICTION

**§2.3 states a class count that contradicts its own enumeration.** §2.3 opens: "Conformance is defined for four classes." It then defines **five**: Conforming TARN file `[R-CNF-02]`, Conforming reader `[R-CNF-03]`/`[R-CNF-04]`, Conforming writer `[R-CNF-05]`, Conforming updater `[R-CNF-06]`, Conforming verifier `[R-CNF-11]`. Five is the correct number, corroborated twice elsewhere: §2.1's note lists the actors as "writer, reader, updater, verifier, or file", and Appendix H gives conformance checklists for all five. §2.3 is normative text (not excluded by `[R-CNF-01]`), so the sentence is a false normative statement. Harmless to bytes; a one-word fix.

### OBSERVATION

**O1 — Register row F7 cites the wrong rule, and `[R-CNT-27]` is absent from the error register entirely.** §21.2's row F7 ("File size is below the 128-byte minimum") gives its governing rule as `[R-CNT-01]` (§5.1's anatomy/`F` mod 64 rule). The 128-byte floor is `[R-CNT-27]`, defined in the very next paragraph of §5.1. `grep -n "R-CNT-27"` returns exactly one hit in the whole document — its definition at line 485. §21.1 says "where a row and the rule it cites diverge, **the rule governs**", and the cited rule does not establish the floor. Not byte-level: `[R-CNT-27]` states the reader obligation independently, and a sub-128-byte file fails §6.2's gates anyway (dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length ≤ F−64 and F mod 64 = 0 jointly force F ≥ 128). But §21.1 makes register completeness normative, and `[R-ERR-02]`/`[R-VEC-03]` build the conformance corpus from row citations.

**O2 — `[R-CNT-25]`'s "extent_length less than 5" condition has no register row, and its outcome is not the one the R-rows carry.** §7.1 makes a user-metadata record "whose extent_length is less than 5 … a validity error at its containing scope" — reject-file top-level, reject-layer as a sub-record. Scanning every register row naming user metadata (F27, F36, L11, L18, R1–R9): F27/L11 cover only extent slot **(0, 0)**; F32 covers one-half-zero; F33 covers offset 1–15; nothing covers `extent_length` ∈ {1,2,3,4} with a valid offset. `grep -n "less than 5"` returns one hit, §7.1. A near-miss discriminator: a top-level type-0x0002 record with extent (offset 200, length 4) whose four bytes are `00 00 00 00` — the terminal CRC over zero preceding bytes is `0x00000000` and matches, the zero-byte document then fails R6 → ignore-record, so a register-driven implementation opens the file while a §7.1-driven one rejects it. I am **not** reporting this as byte-level: §7.1's sentence is explicit, normative, and §21.1 itself says rows merely restate rules, so a careful reader resolves it. It is a completeness defect by §21.1's own standard.

**O3 — Two conditions the specification itself calls file-nonconforming sit in §21.6, "Conditions that are not violations", outside the enumerated register.** §21.6's row for unsorted user-metadata members reads "The file is nonconforming … a verifier reports it" and cites `[R-MTA-05]`, which says "a verifier **MUST** report it". §21.6's row for a registered type's stored MU/PE mismatch cites `[R-CNT-22]`, which says the mismatch "makes the file nonconforming (`[R-CNF-05]`)" and a verifier "SHOULD report" it. Both are violations §21.1 says the register enumerates completely, and §21.8 scopes corpus coverage to "Every row of §21.2 through §21.5" — so neither gets a conformance vector, including the one with a verifier **MUST**. §21.6 is doing double duty: "no reader failure" and "not a violation" are not the same predicate, and these two rows are the first but not the second.

**O4 — The layer register skips L40 with no note.** §21.3 runs L1–L48 omitting L40; the stated count (47) and my mechanical count (47) agree, so nothing is missing — but the gap is unexplained, unlike `[R-SER-04]`, whose withdrawal §14.4 records explicitly. Register row IDs are not requirement identifiers, so §2.2's retirement rule does not reach them; a one-line note would prevent a reader from hunting for a lost row.

**O5 — The seamlessness of extent growth is a real guarantee that no requirement states.** This is the sharpest thing my Task 2 surfaced. Because `[R-SER-05]` forces every padding position to encode fill, a coordinate that crosses from padding into the extents during a metadata-only growth reads as **exactly the fill value** — indistinguishable from a never-stored tile. So "grow the extent, write nothing" yields a uniform fill frontier whether the newly addressed region falls inside an already-stored edge tile or in brand-new sentinel tiles. My generation 2 demonstrates both cases side by side (y=3 from stored tiles s=2/s=3; y=4 from sentinels s=4/s=5) and they are identical. §14.5's rationale gestures at this ("a reader that forgets to clip observes fill") but frames it as a debugging nicety; §11.1's rationale promotes extent growth without mentioning what the newly exposed positions read as. One sentence in §11.1 or §20.3 would convert a derivation into a stated property — and would make clear that `[R-SER-05]`, a verifier-only tile-scope obligation (row T4), is what a *reader* silently depends on the moment an extent grows.

**O6 — `[R-SLB-05]`'s "dead space it did not supersede" leans entirely on §5.2 for its meaning.** A commit's dead space includes the previous generation's pre-trailer pad and trailer, which are not "superseded" in the natural sense of having their content replaced in place. §5.2 settles it by enumerating "every prior generation's directory, padding, and trailer" as dead space, so the intended reading — *newly created unreachable gaps* are the defect — is recoverable. It cost me a re-read; a reader who meets `[R-SLB-05]` before §5.2 may pause too.

**O7 — Positive control, reported because it is evidence about the document.** Everything checkable that I checked, reproduced exactly: the §4.5 check vector, the §15.4 all-sentinel constant `0xEECB3BB2` (computed over 1,310,720 bytes), Appendix A's trailer CRC `0xE00938D2` rebuilt from its own field table, and eleven worked numeric examples — §11.2's grids, §11.4's ordinals 10/11,452/74, §12.1's bfloat16 `0x3F80`, §12.3's 12-byte channel entry, §14.2's three stride cases, §14.3's `55 01`/`55 FD` packed plane, §14.5's 32-byte edge tile, §15.4's 20,000,064-byte index and 1.25 MiB segment, §16.2's four slab runs, §17.3's shuffle `00 00 00 00 00 00 80 00 40 3F 40 40`, §20.3's 644-byte index. §21.8's "121 conditions over 213 named instances" is exactly right by mechanical count under §21.1's stated counting rule (F 38, L 47, T 26, R 10 = 121; instances 213), as are §21.2/§21.3/§21.4's per-section counts and §21.9's note arithmetic (2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB).

## Verdict

IMPLEMENTABLE: yes
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high
