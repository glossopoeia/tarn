# TARN Specification — Acceptance Round, Gate G2 (Minimal Reader)

**Reviewer role:** fresh-context implementer, no prior knowledge of this project.
**Source consulted:** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — and nothing else.
**Scope of the artifact:** a minimal conforming-shaped reader. Codec 1 (`none`) only, no slab invariants, no alignment invariants, local files. Both channel layouts, all thirteen sample types, both filters, sentinel/fill semantics, the full open + layer-access + tile-read chain.
**One external action:** I computed four CRC values over byte strings transcribed out of the spec, to check the document against itself. No other file was opened. Results are in §7 below — all four reproduce exactly.

---

## 1. The implementation plan, byte-precise

Every structure below is given as I would code it: offsets are relative to the structure, widths are fixed, all multi-byte fields are little-endian (`[R-ENC-01]`). Nothing in the plan is inferred; each line carries the citation that fixes it.

### 1.0 Ground rules I hardcode before writing any parser

| Rule | Citation |
|---|---|
| Everything little-endian; no BOM, no big-endian variant | §4.1 `[R-ENC-01]`, `[R-ENC-02]` |
| Every offset/length/extent/count has domain `0 … 2⁶³−1`; a larger value is a validity error at the owning scope | §4.2 `[R-ENC-03]` |
| Every sum/product derived from file integers is overflow-checked against `2⁶³−1` **before use**; never act on a wrapped value | §4.2 `[R-ENC-04]` |
| Never allocate/seek/fetch on an integer before the checksum covering it verifies | §4.2 `[R-ENC-05]`, §4.5 `[R-ENC-10]` |
| CRC-32C: poly `0x1EDC6F41`, reflected in/out, init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`, stored LE `u32` | §4.5 `[R-ENC-09]` |
| Names: `u8` length prefix, 1–255 bytes, well-formed UTF-8, no U+0000–U+001F, compared as **raw bytes** with no normalization | §4.6 `[R-ENC-11]`–`[R-ENC-13]` |
| Four reader outcomes: reject-file / reject-layer / reject-tile / ignore-record; never return fill for a rejected tile | §2.4 `[R-CNF-07]`, `[R-CNF-09]` |
| Sample values are bit patterns; decoding must not alter them | §3.2 `[R-MDL-02]`, §12.3 `[R-TYP-04]` |

That last rule is the one that makes this a weekend job rather than a week: **the reader never interprets a sample.** The thirteen sample types collapse, on the read path, into a thirteen-entry element-size table (§12.1). No IEEE 754 arithmetic, no two's-complement handling, no NaN logic — `[R-TYP-04]` forbids touching the bytes at all.

Element sizes (§12.1): `1 bool→1, 2 int8→1, 3 int16→2, 4 int32→4, 5 int64→8, 6 uint8→1, 7 uint16→2, 8 uint32→4, 9 uint64→8, 10 float16→2, 11 bfloat16→2, 12 float32→4, 13 float64→8`.

### 1.1 Front signature block — file `[0, 16)` — §6.1 `[R-CNT-04]`

| Offset | Size | Value |
|---|---|---|
| 0 | 8 | `89 54 41 52 4E 0D 0A 1A` |
| 8 | 8 | eight zero bytes |

A local reader verifies the **full 16 bytes by byte equality before other processing**; mismatch → reject-file (register F11). This is the first thing my `open()` does (§19.1 step 1).

### 1.2 Trailer — file `[F−64, F)` — §6.2

| Off | Size | Type | Field |
|---|---|---|---|
| 0 | 8 | bytes | magic `8A 4E 52 41 54 0D 0A 1A` |
| 8 | 2 | u16 | version_major |
| 10 | 2 | u16 | version_minor |
| 12 | 4 | u32 | flags |
| 16 | 8 | u64 | generation |
| 24 | 8 | u64 | dir_offset |
| 32 | 8 | u64 | dir_length |
| 40 | 8 | u64 | committed_file_length |
| 48 | 8 | u64 | file_id |
| 56 | 4 | bytes | reserved |
| 60 | 4 | u32 | trailer CRC |

**Validation, in the order `[R-CNT-06]` mandates** (the order is normative, not stylistic):

1. Magic equality (F14). Permitted before the CRC because "comparing a field against a constant for validation is not acting on it" (`[R-ENC-10]`).
2. `CRC32C(trailer[0,60)) == LE_u32(trailer[60,64))` (F20). **This is the only checksum standing between me and every other field.**
3. Version gate (§6.3 `[R-CNT-07]`): `version_major == 0` → reject-file (F24); `version_major != 1` → reject-file with a *distinct* diagnostic (F25) — the spec is explicit that "unimplemented major" must not be reported as corruption. `version_minor` **never** gates.
4. Only now, the remaining gates, all before acting on any of them:
   - flags bits 0–15 (incompat lane): any set → reject-file (F26). Bits 16–31: ignore, unconditionally.
   - `committed_file_length == ` physical size (F23) **and** `≡ 0 (mod 64)` (F19). Bind `F := committed_file_length`.
   - `dir_offset ≥ 16` (F15); `dir_offset, dir_length ≤ 2⁶³−1` (F3); `dir_length ≥ 4` (F22).
   - checked `dir_offset + dir_length`: no overflow past `2⁶³−1` (F4), and `≤ F − 64` (F16).
   - `generation ≥ 1` (F17); `file_id != 0` (F18); `reserved[56,60)` all zero (F21).

`F ≥ 128` falls out of these gates rather than being stated as a rule — see Observation O-6.

### 1.3 Directory region — file `[dir_offset, dir_offset + dir_length)` — §7.1 `[R-CNT-11]`

- Final 4 bytes = LE `u32` CRC-32C over the **preceding `dir_length − 4` bytes**, which *are* the record sequence. Verify **before any other use of the region**; mismatch → reject-file (F27).
- Record sequence length `RS = dir_length − 4`. The directory is always raw — no codec on the open path.
- Degenerate case: `dir_length == 4` ⇒ `RS == 0` ⇒ CRC over zero bytes `== 0x00000000`. This is Appendix A's empty file, and it is a conforming file with zero layers (§21.6).

### 1.4 Record framing — §7.2 `[R-CNT-12]`

Header is 24 bytes, followed by `inline_length` bytes of inline payload:

| Off | Size | Type | Field |
|---|---|---|---|
| 0 | 2 | u16 | type (0 invalid) |
| 2 | 2 | u16 | flags — bit 0 = MUST_UNDERSTAND, bit 1 = PRESERVE_ON_EDIT, bits 2–15 reserved |
| 4 | 4 | u32 | inline_length |
| 8 | 8 | u64 | extent_offset |
| 16 | 8 | u64 | extent_length |

Walk with cursor `p = 0` while `p < RS`:

```
require p + 24 <= RS                    else reject-file (F32)
read header
require p + 24 + inline_length <= RS    else reject-file (F32)
payload = seq[p+24 .. p+24+inline_length)
require type != 0                       else reject-file (F29)
dispatch on type
p += 24 + inline_length
```

Termination requires `p == RS` exactly; a 1–23 byte tail fails the first `require`.

**Dispatch at open** (§19.1 step 4 fixes exactly which checks belong here):

- **`0x0001` layer.** Parse the **name only**: `L = payload[0]`, name bytes `payload[1 .. 1+L)`. Check §4.6: `L ≥ 1` (L6), well-formed UTF-8 (L4), no byte `0x00–0x1F` (L7) — each reject-**layer**. Record the layer. **Do not** validate the layer record's extent slot here: §19.1 step 4 scopes the `[R-CNT-13]` slot checks to *non-layer* top-level records, and the register confirms it (F33–F35 say "non-layer"; L14–L16 are the layer-record counterparts, detected at layer access).
- **`0x0002` user metadata (top-level).** At most one in the sequence — a second is reject-file (F37). Extent slot `(0,0)` → reject-file (F28), because that failure *precedes* the document and so falls outside the quarantine (§18.1 `[R-MTA-02]`). `inline_length` must be 1 → otherwise reject-file (§18.2 `[R-MTA-03]`; **this rule has no register row** — Observation O-1). Slot validity per `[R-CNT-13]` (F33/F34/F35). I do **not** read the document: a minimal reader that never surfaces metadata incurs no extent obligation (`[R-RDR-02]`, "at use of a record's extent"). That keeps JSON, zstd, and §18.2's four content rules entirely out of the weekend.
- **Anything else.** Unknown type. MU bit set → reject-file (F38). Otherwise ignore-record (R10), still applying the slot rules (F33–F35).

For the two *known* types, the stored MU/PE bits are irrelevant: `[R-CNT-22]` says a reader applies a known type's fixed semantics regardless of stored flags. Reserved flag bits (F31/L48) and the MU=1/PE=0 combination (F30/L47) are **verifier** conditions — not my code.

**After the walk:** duplicate layer names, compared as raw bytes → reject-file (F7, `[R-ENC-15]`).

That completes "the open" (`[R-RDR-01]`): trailer + directory, nothing else — no extent, no index, no payload.

### 1.5 Layer access — §19.3 `[R-RDR-03]` — no I/O, decidable from resident bytes and `F`

Parse the inline payload with a strict cursor; **any** overrun, truncation, or residue → reject-layer (L22, `[R-CNT-18]`). Field order is §7.4's table order, packed with no alignment or padding:

| # | Field | Width | Validation (register row) |
|---|---|---|---|
| 1 | name | u8 len + bytes | done at open (L4/L6/L7) |
| 2 | layout | u8 | ∈ {1,2} (L35) |
| 3 | linearization | u16 | == 1 (L32) |
| 4 | codec | u16 | ∈ 1…4 (L44) |
| 5 | filter | u16 | ∈ {1,2} (L46) |
| 6 | alignment A | u64 | 0, or power of two `512 ≤ A ≤ 2⁶²` (L38) |
| 7 | slab S | u64 | 0, or `1 ≤ S ≤ 2⁶³−1` (L1) |
| 8 | A_slab | u64 | 0 iff S == 0 (L27); else power of two `1 ≤ A_slab ≤ 2⁶²` (L28) |
| — | — | — | `A != 0 && S != 0` → reject-layer (L19, `[R-CNT-16]`) |
| 9 | rank d | u8 | ≥ 1 (L31) |
| 10 | channel count C | u16 | ≥ 1 (L31) |
| 11 | d × dimension entry | u8 len + name, u64 Eᵢ, u64 Tᵢ | name rules (L5/L8/L9), unique (L10), `Tᵢ ≥ 1` (L31), domains (L1) |
| 12 | C × channel entry | u8 len + name, u16 type, u8 len + fill | name rules, unique (L10); type ∈ 1…13 (L33); `fill_len == elem_size(type)` (L29); bool fill ∈ {`0x00`,`0x01`} (L34) |
| 13 | index_encoding | u8 | == 1 (L30) |
| 14 | entry_count | u64 | ≤ 2⁶³−1 (L1) |
| 15 | crc_of_crc_array | u32 | == 0 when entry_count == 0 (L26) |
| 16 | sub-records | records to end of payload | framing, no residue (L13); type ≠ 0 (L12); `0x0001` here → reject-layer (L25); ≤1 user-metadata sub-record (L18) with slot ≠ (0,0) (L11) and slot validity (L14/L15/L16); unknown + MU=1 → reject-layer (L24); unknown + MU=0 → ignore (R10) |

§12.3 pins a channel entry byte-exactly, which I used as my parser fixture: name `temp`, float32, fill NaN `0x7FC00000` is `04 74 65 6D 70 0C 00 04 00 00 C0 7F`. That single worked example resolved every question I had about channel-entry framing.

**Geometry, all products checked against `2⁶³−1` (L2, `[R-ENC-04]`):**

- `Gᵢ = Eᵢ / Tᵢ + (1 if Eᵢ mod Tᵢ != 0 else 0)` — §11.2 `[R-GEO-03]` states this form deliberately and its Note warns off `(Eᵢ + Tᵢ − 1)/Tᵢ`, whose intermediate sum can leave the declared domain. I use the stated form verbatim.
- `N = ∏ Gᵢ` (0 if any `Eᵢ = 0`), `P = ∏ Tᵢ` (≥ 1 always, since every `Tᵢ ≥ 1`).
- addressed-tile count `= N` (interleaved) or `C·N` (planar); must equal `entry_count` (L20, `[R-CNT-17]`).
- Interleaved: sample stride `Q = Σ Bᵢ`; channel in-sample offset `F_c = Σ_{j<c} Bⱼ`.
- Decoded size: interleaved `P·Q`; planar numeric `P·B_c`; planar bool `⌈P/8⌉` (§14.2 `[R-SER-02]`, §14.3 `[R-SER-03]`).
- Index region length `= entry_count·20 + ⌈entry_count/2¹⁶⌉·4`, must equal `extent_length` (L21, `[R-CNT-17]`); `entry_count == 0` ⟺ slot `(0,0)`.
- Layer extent slot bounds when `entry_count > 0`: `offset ≥ 16` (L15), fields in domain (L1), checked `offset+length` (L2) `≤ F − 64` (L16).
- Codec 4 declaration bound `decoded_size ≤ 0x7E000000` (L45) — three lines, so I implement it even though codec 4 is out of scope.

Two things I want to record here because they cost me a search: **the alignment and slab *declarations* are reader-validated even though their *invariants* are verifier-only** (L27/L28/L38 are `detector = reader`; L39/L41/L42/L43 are `detector = verifier`). And `codec ∈ {2,3,4}` must be reported by my reader as a *capability* refusal, not a validity error — `[R-ERR-04]` is explicit that the two send users to opposite remedies. A codec-1-only reader is not a conforming reader (`[R-CNF-03]`, `[R-COD-11]`), and I say so in the diagnostic.

### 1.6 Tile index — §15

Region base `R = ` layer record's `extent_offset`. Layout (§15.1 `[R-IDX-01]`), contiguous, no padding anywhere:

```
[ R + 0                     .. R + 20·entry_count )         entry array
[ R + 20·entry_count        .. + 4·⌈entry_count/2¹⁶⌉ )      segment CRC array
```

Entry `k` at `R + 20k`: `u64 offset @0`, `u64 length @8`, `u32 crc @16`.

**Verification chain before any entry is used** (§15.4 `[R-IDX-04]`, §8.2 `[R-CNT-20]`):

1. Read the whole CRC array; `CRC32C(array bytes) == crc_of_crc_array` else reject-layer (L36).
2. `seg = k div 2¹⁶`; segment covers entries `[seg·2¹⁶, min((seg+1)·2¹⁶, entry_count))`; read `[R + 20·segStart, R + 20·segEnd)`; `CRC32C(those bytes) == LE_u32(array + 4·seg)` else reject-layer (L37). The final partial segment's CRC covers only its actual bytes.
3. `[R-IDX-05]`'s constant `0xEECB3BB2` (CRC of a *full* all-sentinel segment) is a **writer** shortcut only: "Equality with the constant licenses nothing for readers." I never pattern-match it.

Both ranges are computable from the layer record alone, and `[R-IDX-04]`'s Note licenses caching a verified range under committed-prefix immutability (`[R-LIF-03]`). My reader caches per `(file_id, generation, range)`.

### 1.7 Entry classification — §15.3 `[R-IDX-03]`, with `S = 0xFFFF_FFFF_FFFF_FFFF`

| Test | Outcome |
|---|---|
| `offset==S && length==S && crc==0` | **valid sentinel** — reads as fill |
| `offset==S && length==S && crc!=0` | reject-tile (T6) |
| exactly one of offset/length `== S` | reject-tile (T7) |
| `length == 0` | reject-tile (T10) |
| `offset < 16` | reject-tile (T8) |
| `offset > 2⁶³−1 \|\| length > 2⁶³−1` | reject-tile (T11) |
| `offset + length` overflows `2⁶³−1` | reject-tile (T12) |
| `offset + length > F − 64` | reject-tile (T9) |
| codec 1 and `length != decoded_size` | reject-tile (T14, `[R-COD-04]`) — **checkable before any payload fetch** |

Order matters: `[R-IDX-02]` exempts sentinel entries from the domain (`[R-ENC-03]`) and sum (`[R-ENC-04]`) rules, so the sentinel test must run first or every sentinel trips T11/T12. §15.2's Rationale says a reader that forgets the sentinel test "still fails safely" — true, but it fails *wrongly* (reject-tile instead of fill), so I test first.

### 1.8 Payload, decode, extract

- Read `[offset, offset+length)`; `CRC32C(those exact bytes) == entry.crc` else reject-tile (T1). §8.1: the entry crc covers "the tile's stored bytes", i.e. the extent verbatim — post-filter, post-codec.
- Codec 1: identity ("the stored bytes are the filtered image verbatim").
- Filter inverse (§17.1 `[R-COD-01]` fixes the order: writer does filter→codec, reader does codec→filter⁻¹):
  - filter 1 → identity.
  - filter 2 (byte-shuffle, `[R-COD-10]`): stride `s = Q` interleaved, `= B_c` planar numeric, `= 1` (identity) for a packed bool plane. `n = L/s`; inverse maps input byte `i·n + j` → output `j·s + i`. Length unchanged. I validated my implementation against §17.3's worked example: `00 00 80 3F 00 00 00 40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`. It reproduces.
- Decoded length must be exactly the declared decoded size (T3, `[R-SER-07]`) — under codec 1 this is already guaranteed by T14.
- **Extract** (§14.2/§14.3), given in-tile ordinal `u` and channel `c`:
  - interleaved → bytes `[u·Q + F_c, +B_c)`; a bool is the single byte there.
  - planar numeric → bytes `[u·B_c, +B_c)`.
  - planar bool → bit `u mod 8` of byte `u div 8`, LSB-first (§4.4 `[R-ENC-08]`).
- **Return** the bytes unaltered (`[R-MDL-02]`, `[R-TYP-04]`).
- **Sentinel path**: return the channel's recorded fill bytes bit-exactly (`[R-TYP-06]`); for an interleaved sentinel, every carried channel's fill in declared order (`[R-TYP-08]`). Never as a fallback for a rejected tile (`[R-TYP-09]`, `[R-CNF-09]`).

### 1.9 What I deliberately do *not* implement, and why that is legal

Verifier-only rows, per the register's `Detector` column: byte coverage and generation attribution (F9, F41–F45, §9.7); extent overlap (F36, L17); declared-padding zero content (F10); pre-trailer gap bound (F12, F13); alignment/slab invariants (L39, L41–L43); decoded-content obligations — padding-position fill (T4), pad bits (T5), interleaved bool bytes (T2), mis-strided filter (T26). §5.2's Note states it directly: "Coverage is checked by verifiers, never by readers."

---

## 2. The full walk: "value of channel C at coordinate X"

Shared setup for both walks — a layer declared `(y, x)`, `E = (1000, 2048)`, `T = (256, 256)`, linearization 1, codec 1. From §11.2: `G_y = 1000/256 = 3` remainder `232 ≠ 0` → `4`; `G_x = 2048/256 = 8` remainder `0` → `8`. So `N = 32`, `P = 65,536`. Requested coordinate `(y, x) = (300, 700)`.

Common ordinal arithmetic (§11.4 `[R-GEO-06]`):
- tile coords `t = (300 div 256, 700 div 256) = (1, 2)`
- in-tile position `u = (300 mod 256, 700 mod 256) = (44, 188)`
- in-tile ordinal `= 44·256 + 188 = 11,452` (row-major for **every** linearization, permanently)
- spatial ordinal `s = t₀·G₁ + t₁ = 1·8 + 2 = 10`

### Walk A — interleaved (layout 1)

Channels: `a` uint8 fill `0x00`, `b` uint16 fill `0xABCD`. `C = 2`, `Q = 1 + 2 = 3`, `F_a = 0`, `F_b = 1`. Decoded size `= P·Q = 196,608`. Addressed tiles `= N = 32` → `entry_count = 32`; index region `= 32·20 + ⌈32/65536⌉·4 = 644` bytes.

1. **Open** (§19.1): front block equality → trailer at `[F−64, F)` in §6.2's order → directory CRC → record walk → layer table. Two structures touched, nothing else.
2. **Layer access** (§19.3): parse and validate the full inline payload as in §1.5. `entry_count == 32 == N` ✓ (L20); `extent_length == 644` ✓ (L21). No fetch.
3. **Domain** (§19.4 step 1): `0 ≤ 300 < 1000` ✓, `0 ≤ 700 < 2048` ✓. (Outside → the *request* fails, with no verdict on the file — `[R-MDL-01]`, §21.6.)
4. **Ordinals** (step 2): disk ordinal `= s = 10` (interleaved).
5. **Index chain** (step 3): `nseg = ⌈32/65536⌉ = 1`. CRC array at region `[640, 644)`; verify against `crc_of_crc_array` (L36). Segment 0 covers entries `[0, 32)` = region `[0, 640)`; verify against the array's u32 at offset 0 (L37).
6. **Entry** (step 4): region `[200, 220)` (`20·10`). Classify per §15.3. If sentinel → return `b`'s fill bytes `CD AB` with zero payload I/O, done. Otherwise codec 1 requires `length == 196,608` (T14) before I fetch anything.
7. **Payload** (step 5): read `[offset, offset+196,608)`; CRC-32C must equal `entry.crc` (T1).
8. **Decode** (step 6): identity (codec 1), then filter⁻¹.
9. **Extract** (step 7): `b` at in-tile ordinal 11,452 sits at byte `11,452·3 + 1 = 34,357`; take `[34,357, 34,359)`. (Cross-check against §14.2's closing sentence: "channel c's value at in-tile ordinal u sits at byte `u·Q + F_c`" — matches, and `34,359 ≤ 196,608` ✓.)
10. **Return** (step 8): those two bytes verbatim, LE `uint16`. If the caller asked for the whole sample, `a` is the single byte at 34,356.

### Walk B — planar (layout 2)

Same geometry. `C = 4`: `c0 r` uint8, `c1 g` uint8, `c2 mask` bool fill `0x01`, `c3 t` float32 fill `0x7FC00000`. Addressed tiles `= C·N = 128 = entry_count`; index region `= 128·20 + 4 = 2,564` bytes. Note each channel now has its **own** decoded size — planar tiles are sized per channel by type alone (§14.4 `[R-SER-09]`).

Steps 1–3 identical. From step 4 on, per requested channel:

- **`mask` (c = 2, bool).** Disk ordinal `= c·N + s = 2·32 + 10 = 74`; entry at region `[1,480, 1,500)` — which is exactly §15.4's second worked example, so I could check my arithmetic against the document. Decoded size `= ⌈65,536/8⌉ = 8,192`; codec 1 ⇒ `entry.length == 8,192` (T14). Filter 2 would be the identity here (`s = 1`). Value at ordinal 11,452 = **bit `11,452 mod 8 = 4` of byte `11,452 div 8 = 1,431`** (§14.3), LSB-first, `0 = false / 1 = true`.
- **`t` (c = 3, float32).** Disk ordinal `= 3·32 + 10 = 106`; entry at region `[2,120, 2,140)`. Decoded size `= 65,536·4 = 262,144`. Value at bytes `[11,452·4, +4) = [45,808, 45,812)` — returned as a 4-byte bit pattern, never interpreted.
- Both entries live in segment 0 (`entry_count = 128 < 2¹⁶`), so one segment CRC and one 4-byte array cover both. §19.4's Note on planar all-channel reads spells out the general case: entries for one spatial ordinal are `N·20` region bytes apart, and for `N ≥ 2¹⁶` they are guaranteed to fall in different segments, each needing its own verification while the array verification is shared.
- **Mixed sample.** If `mask`'s entry is the sentinel and `t`'s is stored, the sample at `(300,700)` reads `mask = true` (its recorded fill `0x01`) and `t` decoded — §3.2's explicitly-defined mixed case, and §13.3's worked `r/g/b` example is the same shape.

Both walks close cleanly. I did not have to invent a single offset.

---

## 3. Which sections I needed

**Did §19 alone suffice? No — and it does not claim to.** §19's own preamble says "It introduces no new structures; each step cites the requirement whose outcome governs its failure." It is a *spine*: it fixes the order of operations and the detection tiers, and every step of it resolves into Part I or Part II for the actual bytes. That is the right design, and §1 anticipates it exactly ("Part I alone yields a container reader… returning sample values needs Part II as well").

**Load-bearing for this artifact:**

| Section | What I could not have written without it |
|---|---|
| §2.3, §2.4 | conformance classes; the four outcomes; "validity error at the owning scope" |
| §4.1–§4.6 | endianness, `2⁶³−1` domain, overflow rule, CRC-32C parameters + check vector, name rules |
| §5.1 | file anatomy; the 128-byte example |
| §6.1, §6.2, §6.3 | front block bytes; trailer layout; **the mandated validation order**; version/flag gates |
| §7.1–§7.4 | directory region + CRC; 24-byte record header; extent-slot rules; **the layer record's complete field order** |
| §8.1, §8.2 | the coverage map and the strictly ordered chain of trust |
| §9.5 | trailer-at-end-or-fail; never scan backward |
| §11.1–§11.4 | rank/extents/tile extents; ceiling-division form; padding positions; **all ordinal formulas** |
| §12.1–§12.3 | the thirteen types and their element sizes; values-are-bit-patterns; the byte-exact channel-entry example |
| §13.1–§13.3 | fill is authoritative and bit-exact; bool fill constraint; unstored ⇒ fill; fill-never-for-rejected |
| §14.1–§14.5 | value sequence, decoded size, offset arithmetic, packed bool planes, padding content |
| §15.1–§15.4 | index region layout, entry layout, sentinel, the 11-row validity table, segment/CRC-array arithmetic |
| §17.1–§17.3 | pipeline order; codec 1's length equality; byte-shuffle stride and inverse |
| §19.1–§19.4 | the four-step open, detection tiers, the layer-access checklist, the eight-step tile read |
| §21.2–§21.5 | used as my **test checklist**, not as normative source (§21.1: where a row and its rule diverge, the rule governs) |
| §21.9 | minimum guarantees, and the reporting rule that separates "too large" from "corrupt" |
| App. A | the only end-to-end byte example in the document |
| App. B | the finding aid I kept open the whole time |

**Not needed:** §9.1–§9.4, §9.6–§9.7 (writer/verifier), §10, §16 (the reader-checked A/A_slab ranges are already in §7.4's table), §18, §20, §22, §23, §24, Appendices C–H.

**Hard to locate:** two things. (a) That the reader validates alignment/slab *declarations* while the *invariants* are verifier-only — that only assembled from §7.4's table + `[R-CNT-23]` + register rows L27/L28/L38, with §16 giving no signpost. (b) `[R-MTA-03]`'s "inline_length must be 1" rule, which lives only in §18.2 and appears in neither §19 nor §21 — an implementer who reads the two consolidating sections will simply not implement it.

**Missing:** nothing that blocked me. Everything byte-level resolved.

---

## 4. Honest work estimate

**18–24 focused hours** for a competent engineer — a real weekend, with the caveat that ~4 of those hours go into building a *writer* you did not want, because there is no end-to-end fixture in the document (Observation O-2).

| Component | Hours | Notes |
|---|---|---|
| CRC-32C + self-test against §4.5's vector | 0.5 | trivial; the check vector makes it a non-issue |
| Front block + trailer parse and ordered validation | 1.0 | the order is normative, so a naive parser needs restructuring |
| Directory CRC + record walk framing | 1.5 | |
| Layer-record inline payload parse | 2.5 | the fiddliest parsing in the format: 8 fixed fields, `d` variable dim entries, `C` variable channel entries, 3 trailing fixed fields, then a sub-record sequence with zero residue |
| Layer validation (§19.3's checklist) | 3.5 | ~20 obligations, each resolving into a different section |
| Checked arithmetic helpers | 1.0 | `[R-ENC-04]` touches ten distinct expressions (L2's instance list) |
| Index region: segment math, two CRC layers, §15.3's 11-row classifier | 2.5 | |
| Ordinal arithmetic | 1.5 | |
| Payload fetch, entry CRC, codec 1, filter inverse | 1.5 | |
| Extraction incl. packed-bool bit addressing | 2.0 | |
| Fill/sentinel paths for both layouts | 1.0 | |
| Outcome-class plumbing through the API | 2.0 | four scopes, and "never return fill for a rejected tile" is an API-shape constraint, not a branch |
| Fixture construction + debugging | 4.0 | you must write a minimal writer first |

**The three hardest things to get right:**

1. **Validation-tier discipline.** Roughly ninety reader-detected conditions, each with a mandated *latest* detection point, spread across §19.2's tiers, §19.3's checklist, §19.4's steps, and the register's `Detected` column. Getting it wrong is *silent* nonconformance: you still return the right bytes for good files, and you return bytes you should have refused for bad ones. `[R-RDR-02]`'s "MAY detect earlier" is the escape hatch — the safe implementation strategy is to be as eager as the tier boundaries allow, since divergence is only ever licensed toward earlier rejection.
2. **Overflow discipline.** `[R-ENC-04]` is not a footnote: L2 names ten distinct derived quantities (`N`, `P`, `N·P`, `C·N`, max disk ordinal, `V = P·C`, `P·Q`, `P·B_c`, `offset+length`, the index-region formula). In any language with wrapping `u64` you will get eight of ten right and ship two. The spec even pre-empts the classic bug — §11.2's Note forbidding `(E+T−1)/T` — which is the single most useful sentence in Part II for an implementer.
3. **The (layout × type) matrix in serialization.** Three decoded-size formulas and three value-offset rules, selected by layout and by whether the channel is bool, plus a filter stride that changes with the same selector, plus the pad-bits-vs-padding-positions distinction (§14.3's Note exists precisely because these get conflated). §14.4's Note is the tell: a single-channel *bool* layer is **not** byte-identical across layouts, while a single-channel numeric one is.

---

## 5. Where I re-read, guessed, or reconstructed

Recorded honestly, including the ones I resolved:

1. **Which checks fire at open vs at layer access.** Resolved only by cross-referencing §19.1 step 4, §19.2's tiers, §19.3, and the register's `Detected` column — three places. The asymmetry that a *layer record's* name is checked at open (L4/L6/L7) while *dimension and channel* names are checked at layer access (L5/L8/L9) is stated **only** in the register, never in §4.6 or §7.4.
2. **Layer-record extent slots at open.** I initially applied `[R-CNT-13]` to every top-level record at open. §19.1 step 4's phrase "for non-layer top-level records" is the whole rule, and the register's F33–F35 ("non-layer") vs L14–L16 split confirms it. Two reads.
3. **`entry_count = 0` handling.** Reconstructed from five scattered statements: §7.4's table (extent `(0,0)`), `[R-CNT-17]` ("and 0 when entry_count is 0"), `[R-CNT-23]` (crc must be 0), L21, L26. All consistent — and pleasingly, `⌈0/2¹⁶⌉ = 0` makes `CRC32C(∅) = 0` agree with the mandated zero — but it is assembled, not stated in one place.
4. **Alignment/slab declaration validation for a reader that implements neither.** Reconstructed from `[R-CNT-23]` plus L27/L28/L38's `detector = reader`. §16 never says it.
5. **A layer record too short to hold its name.** The register puts L22 at `layer access`, but §19.1 step 4 obliges the open to parse the name — so the truncation must be caught earlier. `[R-RDR-02]` licenses it ("A reader MAY detect any violation earlier"), so no conflict, but I had to reason it out.
6. **Whether index-entry `offset` is file-absolute.** The word "absolute" never appears. Settled by §15.3's bounds rows (`offset < 16` invalid; `offset + length > F − 64` invalid) — decisive, but by inference.
7. **A user-metadata extent shorter than 4 bytes.** Reconstructed; see Ambiguity A-1.
8. **How a reader detects L23 (sub-record nesting).** I could not construct a case. See Observation O-4.
9. **`F ≥ 128`.** Derived, not stated normatively. See Observation O-6.

---

## 6. Self-consistency checks I ran against the document

Because G3 is about bytes, I checked the document's own numbers by computing them from the definitions it gives:

| Claim | Where | Computed | Result |
|---|---|---|---|
| `CRC32C("123456789") = 0xE3069283`, LE `83 92 06 E3` | §4.5 | `0xE3069283` | ✅ |
| `CRC32C(∅) = 0x00000000` | §4.5 | `0x00000000` | ✅ |
| CRC of a full all-sentinel segment `= 0xEECB3BB2` | §15.4 `[R-IDX-05]` | `0xEECB3BB2` over 1,310,720 bytes | ✅ |
| Appendix A trailer CRC `= 0xE00938D2`, bytes `D2 38 09 E0` | App. A | `0xE00938D2` over the 60 transcribed bytes | ✅ |
| `entry_count = 1,000,000` → 16 segments, region 20,000,064 B, entry 999,999 at segment-relative byte 339,180, segment 15 at `[19,660,800, 20,000,000)`, array at `[20,000,000, 20,000,064)` | §15.4 example | all reproduce | ✅ |
| §11.4 example: `s = 10`, in-tile ordinal `11,452`, planar disk ordinal `74`, entry at `[1,480, 1,500)` | §11.4, §15.4 | reproduce | ✅ |
| §14.2 example: `Q = 3`, size 18, sample 5 at `[15,18)`; float32+bool `Q = 5`, size 30, `[25,30)` | §14.2 | reproduce | ✅ |
| §14.3 example: alternating bools, `P = 10` → `55 01` (fill false) / `55 FD` (fill true) | §14.3 | reproduce | ✅ |
| §17.3 example: shuffle of `1.0, 2.0, 3.0` float32 | §17.3 | reproduces | ✅ |
| §14.5 example: 5×5 extents, 4×4 tiles, corner tile = 1 real + 15 padding positions, 32 bytes | §14.5 | reproduces | ✅ |
| §21.8's "126 conditions over 235 named instances" | §21.2–§21.5 | 43+47+26+10 = **126**; instances 91+81+43+20 = **235** | ✅ exact |

The instance count matching to the unit is what makes the register omissions in Observation O-1 conspicuous rather than plausibly-deliberate: the counting discipline is clearly real.

---

## 7. Findings

### AMBIGUITY

**A-1. User-metadata extent shorter than its terminal CRC.** §7.1 `[R-CNT-25]` / §8.1's map / §18.1 `[R-MTA-02]` / §18.2 `[R-MTA-09]`.
§8.1 says the user-metadata extent's checksum is "final 4 bytes of the extent" over "the preceding bytes". Nothing bounds `extent_length ≥ 4`. For `extent_length ∈ {1,2,3}` there is no well-defined "final 4 bytes".
*Readings the text permits:* (a) the extent is structurally malformed and the failure "precedes the document" (§18.1's own phrase), so it is a validity error at the containing scope — reject-file top-level, reject-layer as a sub-record; (b) it is one of the "*every* way a user-metadata record's document can be unreadable" cases that `[R-CNT-25]` sweeps into ignore-record.
*Picked:* (b). `[R-CNT-13]` enumerates *exhaustively* what makes an extent slot malformed — "either half zero, an extent_offset < 16, an extent extending past F − 64, or an overflowing sum" — and "too short" is not on that list, so the slot is well-formed and the failure lies inside the document's container, squarely under the quarantine.
*Not byte-level.* The file is nonconforming under either reading (a conforming writer's extent always holds document + CRC), and `[R-CNF-12]` plus §24's Note explicitly license a reader to reject a nonconforming file more broadly than the register's row. No conforming file's acceptance and no returned byte turns on it.

**A-2. May a conforming reader decline metadata encoding 2 (zstd) while being obliged to implement codec 3 (zstd)?** §2.3 `[R-CNF-03]` vs §18.2 `[R-MTA-03]` / §7.1 `[R-CNT-25]`.
`[R-CNF-03]` enumerates what a conforming reader must handle: core codecs, core filters, both layouts, core sample types. Metadata encodings are a *separate* identifier space (§10.2) and are not enumerated. `[R-CNT-25]` and `[R-MTA-03]` both provide for an encoding "the reader does not implement" → ignore-record.
*Readings:* (a) a conforming reader that has a zstd decoder for codec 3 must also use it for metadata encoding 2; (b) the two are independent, and declining encoding 2 is licensed.
*Picked:* (b), on the enumeration in `[R-CNF-03]` — but it is an odd result (the same decoder, present and refused), and a one-clause pointer in `[R-CNF-03]` would close it.
*Not byte-level:* metadata can never affect how a byte is located, decoded, or returned (`[R-MTA-02]`, `[R-SEC-06]`).

**A-3. Detection tier for a layer record too truncated to hold its name.** §19.1 step 4 vs register row L22 (`Detected: layer access`).
The open is obliged to parse each layer record's name (§19.1 step 4, `[R-ENC-12]`, and the duplicate-name check at file scope depends on it), so a payload too short to contain the name must fail *at open* — while L22, the row that governs inline-payload overrun, is filed at layer access.
*Picked:* detect at open. `[R-RDR-02]` explicitly licenses earlier detection ("A reader MAY detect any violation earlier"), so this is a presentation wrinkle, not a conflict.
*Not byte-level.*

### BYTE-LEVEL AMBIGUITY

**None.** Every question that could change an emitted byte, a returned byte, or the acceptance of a *conforming* file resolved to a single reading: field order and widths (§6.2, §7.2, §7.4 with `[R-CNT-18]`'s "packed in table order with no alignment or padding"), endianness (`[R-ENC-01]`), CRC parameters and storage (`[R-ENC-09]`), CRC byte ranges (§8.1's map), the index region's two-array layout and segment boundaries (§15.1, §15.4), the sentinel's exact 20 bytes (§15.2), all three decoded-size formulas and all three value-offset rules (§14.2, §14.3), pad-bit and padding-position content (§14.5), the filter stride and its inverse (`[R-COD-10]`), and codec 1's length equality (`[R-COD-04]`). Where a formula could be read two ways, a worked numeric example is adjacent and pins it — §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §17.3, and Appendix A between them nail every non-obvious encoding, exactly as §4.7's Note promises. I re-derived ten of those examples and all ten reproduce.

The one candidate that *would* have counted — Contradiction C-1's disagreement about whether a file is conforming — is disqualified because §21.1 supplies an explicit, deterministic tie-break ("where a row and the rule it cites diverge, **the rule governs**"). The reading is *determined*, not ambiguous. I flag the reasoning so a gate reviewer can disagree with the criterion rather than guess at it.

### CONTRADICTION

**C-1. Is a file carrying an unregistered `tarn.` key conforming?**
- §18.3 `[R-MTA-06]`: "A file carrying an unrecognized `tarn.` key is **conforming** — later minor versions register keys, exactly as they define ignore-lane flag bits (§6.3), and this text's readers skip both harmlessly."
- §21.6, row citing `[R-MTA-06]`: "A user-metadata document carries a `tarn.`-prefixed key this specification does not define | **The file is nonconforming**, but a reader ignores that key and reads the rest of the document."

These cannot both hold: one and the same byte sequence is conforming and nonconforming. The consequence is real, not cosmetic — a verifier "certifies only violation-free files" (`[R-CNF-12]`), so the two readings give opposite certification verdicts on a file §18.3 calls conforming. §21.1's precedence clause resolves it in favour of §18.3 (conforming). Note the internal evidence for that resolution: §6.3 `[R-CNT-08]` handles the exactly-parallel case (writer MUST write `flags = 0`, yet a set ignore-lane bit "is not a file-conformance violation") the same way §18.3 does, and §21.6 lists *that* case correctly as conforming. The `tarn.` row is the outlier. **Fix the §21.6 row, not §18.3.**

**C-2. §21.6's own heading versus three of its rows.** §21.6 is titled "Conditions that are **not** violations" and opens "These are defined behaviors, **not errors**. A reader that treats any of them as a failure is the nonconforming party." Three of its rows then say "The file is nonconforming" — the `[R-MTA-05]` unsorted-members row, the `[R-MTA-06]` row of C-1, and the `[R-CNT-22]` stored-flag-mismatch row. A nonconforming file is by definition one where a requirement is violated (§2.3, `[R-CNF-02]`), so those three are violations sitting in a table that declares them not to be. The distinction the section is reaching for — *no reader outcome*, versus *no violation* — is real and worth making explicitly, because §21.2–§21.5's completeness is normative and these three rows are the reason three named violations have no register row (O-1).

**C-3. A fifth outcome that §2.4 forbids.** §2.4 `[R-CNF-07]`: "Every detectable violation named by this specification is assigned **exactly one** reader outcome: reject-file, reject-layer, reject-tile, or ignore-record." §18.4 `[R-MTA-07]` names a detectable violation — "A writer MUST NOT emit a standardized key outside the scopes its row lists" — and assigns the reader "MUST **ignore that key** … rather than rejecting the document." Ignoring a key is not ignoring a record; the record is still processed and the rest of the document returned. `[R-MTA-08]` does the same for a stale `tarn.stats`. Benign in effect (metadata cannot affect decoding), but `[R-CNF-07]`'s universal quantifier is false as written. Either name "ignore-key" in §2.4 or scope `[R-CNF-07]` to structural violations.

### OBSERVATION

**O-1. Register completeness — a §21.1-defined defect.** §21.1 states that "a violation this specification names and the register omits is a defect in this document." At least three named violations are omitted from §21.2–§21.5:
- **`[R-MTA-03]`**: "A record whose inline_length is not 1 is a validity error at the record's containing scope." Reader-detected, scope-level outcome (reject-file top-level / reject-layer as sub-record), and **absent from the register entirely**. This is the finding with the sharpest G2 consequence: §19 and §21 are the document's two consolidating sections, and an implementer who works from them will not implement this check. F28 (the `(0,0)` extent, the sibling rule from the very same paragraph) *is* registered, which makes the omission look like an oversight rather than a decision.
- **`[R-MTA-05]`** (unsorted metadata members) and **`[R-CNT-22]`** (stored MU/PE mismatch on a registered type): both explicitly make a file nonconforming and both carry verifier reporting duties (MUST and SHOULD respectively), yet appear only in §21.6 — see C-2. Contrast F30/F31/L47/L48, which *are* registered and are likewise writer-side-only, verifier-detected conditions. The treatment is inconsistent.
- Minor: an *unimplemented* metadata encoding is a defined behavior (`[R-CNT-25]`) that appears in neither §21.5 nor §21.6, although §21.6 does list the parallel "unimplemented version_major" case.

**O-2. There is no end-to-end annotated file containing a layer.** Appendix A annotates the 128-byte *empty* file, and it is excellent — I used it as my first fixture and its CRC verifies. But every other byte-level example is a fragment: a channel entry (§12.3), offset arithmetic (§14.2), a packed plane (§14.3), a padded edge tile (§14.5), index region arithmetic (§15.4), a shuffle (§17.3). Nothing shows a **complete file with one layer, one stored tile, one sentinel, an index region, and every CRC**. The consequence for G2 is concrete and costly: a first implementer must write a minimal *writer* before they can test their reader, which is roughly four of the twenty hours below. §24 promises a conformance corpus, but §24 also says the corpus is derivative and correctable — the document should stand alone, and an ~400-byte annotated hexdump (1 layer, 2 channels, `2×2` grid with one stored tile and three sentinels, codec 1, filter 1) would be the single highest-value addition to this specification.

**O-3. Index-entry offsets are never called "file-absolute."** §15.1's table says only "see §15.3", and §15.3 pins it by bounds (`offset < 16` invalid; `offset + length > F − 64` invalid). Decidable, but region-relative is a plausible first-draft misreading that costs an afternoon. One word in the table's Valid-values cell removes it.

**O-4. Register row L23 assigns a reader a check with no reachable instance in major 1.** L23 — "A layer record's sub-record itself contains records (nesting depth beyond two)" — is `Detector: reader`, `Detected: layer access`. But a reader parses a sub-record's inline payload only for types it knows, and the only known sub-record type is `0x0002`, whose payload is exactly one byte (§18.2). Unknown sub-record payloads are opaque by construction. I could not build a case where a conforming reader would ever detect L23. It is harmless, but an implementer will spend real time asking "how?" Either reassign it to the verifier or add a note that it binds prospectively, against future record types whose payloads are defined as record sequences. The same "detectable only via downstream failure" caveat that F1 carries in its Condition text would help L3 and F5 too.

**O-5. Reader-checked *declarations* versus verifier-checked *invariants* for §16.** §16.1/§16.2 read as verifier material end to end, but a reader must still validate `A`, `S`, and `A_slab`'s declared values (L27/L28/L38, `detector = reader`) and the mutual exclusion `[R-CNT-16]` (L19). One sentence at the top of §16 — "the declared values are reader-validated (§7.4, `[R-CNT-23]`); the placement invariants below bind verifiers" — would save the search.

**O-6. The 128-byte floor exists only in non-normative text plus a register row.** Register row F8 asserts "the 128-byte minimum" and cites `[R-CNT-01]`, which does not state it; §5.1's "smallest conforming file is 128 bytes" is inside an **Example** block (non-normative by `[R-CNF-01]`), and Appendix B is a non-normative finding aid. It *is* derivable from normative gates — `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64` ⇒ `F ≥ 84`; `F ≡ 0 (mod 64)` ⇒ `F ≥ 128` — so nothing is missing in substance. Worth a parenthetical in `[R-CNT-01]` so implementers know F8 is a derived consequence, not an independent constant to hardcode.

**O-7. §19.3 is the densest paragraph in the document.** One sentence-list carries roughly twenty distinct obligations, each resolving into a different section (§11.4, §12.2, §13.2, §14.1, §15.1, §17.2, §17.3, plus five `[R-…]` identifiers). It is *complete* — I built my layer-validation function directly from it and the register agreed with it row for row — but it is the paragraph I re-read most, and a table (obligation → rule → register rows) would turn it into something an implementer can check off.

**O-8. Advertise the bit-pattern simplification.** `[R-MDL-02]` + `[R-TYP-04]` mean a reader needs *no* numeric semantics at all: the thirteen "core sample types" that `[R-CNF-03]` makes non-negotiable reduce, for a reader, to a thirteen-entry element-size table. This is a large simplification that materially lowers the apparent cost of "all thirteen types, no subsets", and §12.1 never says it out loud. A sentence there would defuse the most likely objection to `[R-CNF-03]`.

**O-9. Scope honesty about this artifact.** The reader I planned is *not* a conforming reader: `[R-CNF-03]` and `[R-COD-11]` are unambiguous that declining codecs 2–4 disqualifies it. Adding them is a second chunk of comparable size — not the codecs themselves (all three are library calls) but §17.2's frame-level constraints, which are register rows T15–T25: raw-DEFLATE-not-wrapped, exactly-one-stream, zstd frame magic / no skippable frames / no second frame / zero dictionary ID / no content-checksum flag / window ≤ decoded size / content-size equality, LZ4 block-not-frame, and exact input consumption. §17.2's Note is right that "whole-buffer decoders that tolerate concatenated or skippable frames do not by themselves enforce the exactly-one-frame rule" — that is header-parsing work on top of the library, and the spec is commendably explicit about it. The document is *not* at fault here; I flag it only so the G2 verdict is not read as "a conforming reader is a weekend."

---

## Verdict

IMPLEMENTABLE: yes
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high
