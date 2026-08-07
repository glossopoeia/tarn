# G2 — Minimal Conforming Reader: Byte-Precise Implementation Plan

**Charter:** codec 1 only, no slabs, no alignment, local files. Source read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full, and nothing else. Every constant and every worked example in the document was independently recomputed (see Observation O-9).

---

## 1. What the product is, and is not

`[R-CNF-03]` (§2.3) is unambiguous: a reader that declines a core codec, either filter, either layout, or any of the thirteen core sample types **is not a conforming reader**, "even if it reads all other conforming files correctly." The weekend artifact below is therefore a *correct partial reader*, not a conforming one. Its refusals on codecs 2–4 must be reported as capability, never as corruption — `[R-ERR-04]` states the reason ("a reader that reports 'too large' as 'corrupt' invites the deletion of intact data"), and the same logic applies to "I don't implement zstd."

Both filters *are* implemented below (byte-shuffle is 12 lines), because filter 2 composes with codec 1.

---

## 2. Structures parsed in order, with offsets and widths

All multi-byte fields little-endian (`[R-ENC-01]`). `u32le(b)` / `u64le(b)` below mean LE decode. Field widths are fixed and are never a writer choice (`[R-ENC-06]`).

### 2.1 Front signature block — file bytes [0, 16) (§6.1)

| Offset | Size | Value |
|---|---|---|
| 0 | 8 | `89 54 41 52 4E 0D 0A 1A` |
| 8 | 8 | zero |

A **local** reader MUST verify all 16 bytes by equality *before other processing*; mismatch → reject-file (`[R-CNT-04]`, row F10). The local/remote distinction is defined in §6.1 itself, not §6.4 — a local reader has no §6.4 obligations at all.

### 2.2 Trailer — file bytes [S − 64, S) (§6.2)

| Off | Size | Type | Field |
|---|---|---|---|
| 0 | 8 | bytes | magic `8A 4E 52 41 54 0D 0A 1A` |
| 8 | 2 | u16 | version_major |
| 10 | 2 | u16 | version_minor |
| 12 | 4 | u32 | flags (0–15 incompat, 16–31 ignore) |
| 16 | 8 | u64 | generation |
| 24 | 8 | u64 | dir_offset |
| 32 | 8 | u64 | dir_length |
| 40 | 8 | u64 | committed_file_length = F |
| 48 | 8 | u64 | file_id |
| 56 | 4 | bytes | reserved (zero) |
| 60 | 4 | u32 | trailer CRC |

### 2.3 Directory region — [dir_offset, dir_offset + dir_length) (§7.1)

* record sequence = `[dir_offset, dir_offset + dir_length − 4)`
* terminal CRC = `[dir_offset + dir_length − 4, dir_offset + dir_length)`
* Always raw — "no codec involvement on the open path."

### 2.4 Record — 24-byte header + `inline_length` bytes (§7.2)

| Off | Size | Type | Field |
|---|---|---|---|
| 0 | 2 | u16 | type (0 invalid) |
| 2 | 2 | u16 | flags: bit0 MU, bit1 PE, bits 2–15 reserved |
| 4 | 4 | u32 | inline_length |
| 8 | 8 | u64 | extent_offset |
| 16 | 8 | u64 | extent_length |

Record stride = `24 + inline_length`. Sequence must consume the record region exactly, no residue.

### 2.5 Layer record inline payload (§7.4) — cursor parse, no padding between fields

```
p = 0
name_len   u8   @p        ; p += 1
name       [name_len]     ; p += name_len
layout     u8   @p        ; p += 1
lineariz.  u16  @p        ; p += 2
codec      u16  @p        ; p += 2
filter     u16  @p        ; p += 2
A          u64  @p        ; p += 8
S          u64  @p        ; p += 8
A_slab     u64  @p        ; p += 8
d          u8   @p        ; p += 1
C          u16  @p        ; p += 2
repeat d:  dname_len u8, dname[..], E u64, T u64     ; 1+len+16 each
repeat C:  cname_len u8, cname[..], type u16,
           fill_len  u8,  fill[fill_len]             ; 1+len+2+1+fill_len each
index_encoding u8  @p     ; p += 1
entry_count    u64 @p     ; p += 8
crc_of_crc_arr u32 @p     ; p += 4
sub-records: §7.2 framing to the end of inline_length, no residue
```

Fixed prefix before the dimension entries is `name_len + 35` bytes; fixed suffix after the channel entries is 13 bytes.

### 2.6 Tile-index region — at the layer record's extent slot (§15.1)

```
[ entry array: entry_count × 20 ][ segment CRC array: ceil(entry_count / 65536) × 4 ]
```
No padding anywhere inside. Entry for disk ordinal *k* is at region byte `20·k`:

| Off | Size | Type | Field |
|---|---|---|---|
| 0 | 8 | u64 | offset |
| 8 | 8 | u64 | length |
| 16 | 4 | u32 | crc |

Sentinel = `FF ×16 00 ×4` (§15.2).

---

## 3. Every checksum, with the exact ranges it covers

All CRC-32C, Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored LE u32 (§4.5, `[R-ENC-09]`). Verified: CRC-32C(`"123456789"`) = 0xE3069283; CRC-32C(∅) = 0x00000000.

| Checksum | Stored at | Covers |
|---|---|---|
| Front block | — (byte equality) | — |
| Trailer | file `[F−4, F)` | file `[F−64, F−4)` |
| Directory | file `[dir_off+dir_len−4, dir_off+dir_len)` | file `[dir_off, dir_off+dir_len−4)` |
| `crc_of_crc_array` | layer record inline payload | file `[X + 20·entry_count, X + 20·entry_count + 4·nsegs)`, X = layer extent_offset |
| Segment *s* CRC | CRC-array byte `4·s` | file `[X + 20·65536·s, X + 20·min((s+1)·65536, entry_count))` |
| Stored tile | entry byte +16 | file `[entry.offset, entry.offset + entry.length)` — **stored** bytes, before decode |
| User-metadata extent | `[eo+el−4, eo+el)` | `[eo, eo+el−4)` — encoded bytes exactly as stored |

Chain of trust, strictly ordered (§8.2): trailer → directory → crc_of_crc_array → segment CRC array → index segment → index entry → stored tile.

Two constants worth hard-coding, both recomputed and confirmed: `crc_of_crc_array = 0x00000000` when `entry_count = 0` is *both* the `[R-CNT-23]` literal and the honest CRC of zero bytes — no special case is needed. The all-sentinel full-segment constant is `0xEECB3BB2` (`[R-IDX-05]`), but it may **never** be used as a match target: "verification is byte comparison of computed CRCs, never constant matching."

---

## 4. Validation, and exactly where each check happens

`[R-RDR-02]` fixes the *latest* detection point; earlier is always licensed. Register row IDs from §21.2–§21.5 in brackets.

### 4.1 Tier: OPEN (§19.1)

1. `S ≥ 128` else reject-file — `[R-CNT-27]` [F7].
2. `bytes[0,16) == constant` else reject-file — `[R-CNT-04]` [F10, F2].
3. Read `T = bytes[S−64, S)`.
4. `T[0,8) == 8A 4E 52 41 54 0D 0A 1A` else reject-file [F13].
5. `crc32c(T[0,60)) == u32le(T[60,64))` else reject-file [F19].
6. version gate: `version_major == 0` → reject-file "invalid" [F23]; `!= 1` → reject-file with a diagnostic distinct from "not a TARN file" and from "corrupt" [F24], `[R-CNT-07]`.
   *Steps 4–6 are the only ones touching fields whose positions are fixed across all majors (`[R-CNT-24]`) — hence the mandated order.*
7. version_minor: ignore, always. A reader MUST NOT reject on it.
8. `flags & 0xFFFF == 0` else reject-file [F25]; bits 16–31 ignored (`[R-CNT-08]`).
9. Domain gates before use: `dir_offset, dir_length, committed_file_length ≤ 2⁶³−1` [F3]; `generation ≤ 2⁶³−1` (§6.2 table + `[R-ENC-03]` — **no register row**, see Finding O-1).
10. `F == S` [F22] and `F mod 64 == 0` [F18].
11. `dir_offset ≥ 16` [F14]; `dir_length ≥ 4` [F21]; `dir_offset + dir_length` does not exceed 2⁶³−1 [F4] and `≤ F − 64` [F15].
12. `generation ≥ 1` [F16]; `file_id != 0` [F17]; `T[56,60)` all zero [F20].
13. Read the directory region; `crc32c(region[0, dir_length−4)) == u32le(tail4)` else reject-file [F26]. **Before any other use of the region** (`[R-CNT-11]`).
14. Walk records over `R = region[0, dir_length−4)`:
    * header containment `p+24 ≤ len(R)` and body containment `p+24+inline_length ≤ len(R)` else reject-file [F31].
    * `type == 0` → reject-file [F28].
    * **type 0x0001 (layer):** parse *only* the name here — `name_len ≥ 1` [L6], well-formed UTF-8 [L4], no U+0000–U+001F [L7], `1+name_len ≤ inline_length` [L22]; violations reject-**layer**, not the file. Insert into the file-scope namespace; a byte-identical duplicate → reject-**file** [F6] (`[R-ENC-15]`, raw-byte comparison, no normalization).
    * **type 0x0002 (user metadata), top-level:** at most one [F36]; `inline_length == 1` else reject-file (`[R-MTA-03]` — **no register row**); extent slot != (0,0) else reject-file [F27]; `extent_length ≥ 5` else reject-file (`[R-CNT-25]` — **no register row**); slot rules [F32/F33/F34]; encoding byte ∈ {1,2} else ignore-record and SHOULD report [R1].
    * **unknown type:** MU=1 → reject-file [F37]; MU=0 → ignore-record [R10]. Its extent slot is still validated here [F32/F33/F34] (§19.1 step 4 covers "non-layer top-level records").
    * Layer records' extent slots are **not** validated at open; they belong to layer access [L14–L16].

The open touches the trailer and the directory only. No extent, no index, no payload.

### 4.2 Tier: LAYER ACCESS (§19.3) — no I/O; everything is decidable from the resident directory and F

* Exact parse, no overrun/truncation/residue [L22], sub-records parse cleanly [L13].
* `layout ∈ {1,2}` [L35]; `linearization == 1` [L32]; `codec ∈ 1..4` [L44]; `filter ∈ {1,2}` [L46]; `index_encoding == 1` [L30].
* `A == 0` or (power of two, 512 ≤ A ≤ 2⁶²) [L38]; `S == 0` or `1 ≤ S ≤ 2⁶³−1` [L1]; `A_slab == 0` iff `S == 0` [L27], else power of two `1 ≤ A_slab ≤ 2⁶²` [L28]; `A != 0 ∧ S != 0` → reject-layer [L19]. *A no-slab/no-alignment reader still must run all five of these.*
* `d ≥ 1`, `C ≥ 1`, every `Tᵢ ≥ 1` [L31]; `Eᵢ, Tᵢ ≤ 2⁶³−1` [L1].
* Dimension and channel names: non-empty [L8], well-formed UTF-8 [L5], no C0 [L9], unique within kind [L10].
* `type ∈ 1..13` [L33]; `fill_len ==` element size {1:1, 2:1, 3:2, 4:4, 5:8, 6:1, 7:2, 8:4, 9:8, 10:2, 11:2, 12:4, 13:8} [L29]; bool fill ∈ {0x00, 0x01} [L34].
* Geometry: `Gᵢ = Eᵢ/Tᵢ + (1 if Eᵢ mod Tᵢ else 0)` — **never** `(E+T−1)/T`, §11.2's note forbids it because the intermediate sum can leave the domain. `N = ∏Gᵢ`, `P = ∏Tᵢ`; all of `N, P, N·P, C·N, V = P·C, P·Q, P·Bᶜ, (C−1)·N+(N−1)` overflow-checked at 2⁶³−1 [L2].
* `entry_count == N` (interleaved) or `C·N` (planar) [L20].
* Extent slot: `(0,0)` iff `entry_count == 0`; else `extent_length == entry_count·20 + ceil(entry_count/65536)·4` [L21], `extent_offset ≥ 16` [L15], `extent_offset + extent_length ≤ F − 64` [L16], no half-zero [L14], no overflow [L2].
* `entry_count == 0 → crc_of_crc_array == 0` [L26].
* Sub-records: type != 0 [L12], type 0x0001 forbidden here [L25], unknown MU=1 → reject-layer [L24], unknown MU=0 → ignore-record [R10], ≤ 1 user-metadata sub-record [L18], UM sub-record extent != (0,0) [L11].
* codec 4 only: decoded size ≤ `0x7E000000` [L45].

### 4.3 Tier: TILE USE (§19.4)

See the walk in §5. Detected here: [L36], [L37] (layer scope, despite the tile-use detection point — `[R-RDR-02]` says so explicitly), [T1], [T3], [T6]–[T12], [T14].

### 4.4 Not this reader's job

Coverage partition [F8], padding zero-ness [F9], pre-trailer-gap bound [F11/F12], extent overlap [F35, L17], alignment/slab invariants [L39, L41–L43], reserved/MU-PE flag hygiene [F29, F30, L47, L48], decoded-content obligations [T2, T4, T5, T26]. All verifier-assigned; §19.2 places them outside the reader tiers entirely.

---

## 5. The full walk: "give me channel *c* at coordinate *x*" → bytes

### Step 1 — Domain (`[R-MDL-01]`, `[R-GEO-02]`)
Point request: require `0 ≤ xᵢ < Eᵢ` for every *i*. Failure is a **request** failure — "with no verdict on the file." Region request: intersect with the extents; a disjoint region, or any region of a zero-extent layer, **succeeds and returns no samples**.

### Step 2 — Ordinals (`[R-GEO-06]`)
```
tᵢ = xᵢ div Tᵢ            uᵢ = xᵢ mod Tᵢ
s  = Σᵢ tᵢ · ∏_{j>i} Gⱼ    (spatial tile ordinal, linearization 1)
u  = Σᵢ uᵢ · ∏_{j>i} Tⱼ    (in-tile ordinal — row-major for every linearization, permanently)
k  = s                     (interleaved)
k  = c·N + s               (planar, channel-major)
```

### Step 3 — Index chain (`[R-IDX-04]`) — once per needed entry, cacheable
```
nsegs = ceil(entry_count / 65536)
seg   = k div 65536
crcarr_range  = [X + 20·entry_count,  X + 20·entry_count + 4·nsegs)
segment_range = [X + 20·65536·seg,    X + 20·min((seg+1)·65536, entry_count))
```
Both ranges are computable from the layer record alone and MAY be fetched in parallel. Verify `crc32c(crcarr) == crc_of_crc_array` [L36], then `crc32c(segment) == u32le(crcarr[4·seg .. 4·seg+4))` [L37]. Either mismatch → **reject-layer**. Committed-prefix immutability (`[R-LIF-03]`) licenses caching both results.

### Step 4 — Entry classification (§15.3) — **order matters**
Entry at segment byte `20·(k mod 65536)`.
```
1. offset==2⁶⁴−1 && length==2⁶⁴−1 && crc==0  -> VALID SENTINEL
2. offset==2⁶⁴−1 && length==2⁶⁴−1 && crc!=0  -> reject-tile [T6]
3. exactly one of offset/length ==2⁶⁴−1      -> reject-tile [T7]
4. length == 0                               -> reject-tile [T10]
5. offset < 16                               -> reject-tile [T8]
6. offset > 2⁶³−1 || length > 2⁶³−1          -> reject-tile [T11]
7. offset+length > 2⁶³−1                     -> reject-tile [T12]
8. offset+length > F − 64                    -> reject-tile [T9]
```
Rows 1–3 **must** precede rows 6–8: `[R-IDX-02]` exempts sentinel fields from `[R-ENC-03]`/`[R-ENC-04]`. Invert this and every sparse tile in every conforming file becomes a read failure.

**Sentinel → fill, with no payload I/O** (`[R-TYP-06]`, `[R-TYP-08]`): planar returns *that entry's channel's* recorded fill bytes; interleaved returns *every carried channel's* fill, in declared channel order. Bit-exact, straight from the channel entry — never a type-derived default.

**Any reject-tile → the read reports failure.** `[R-TYP-09]` and `[R-CNF-09]`: fill is produced by exactly one condition, a valid sentinel in a verified chain. Fill is never a failure fallback.

### Step 5 — Payload
Decoded size, the three-case function:

| Case | Decoded size | Value *k*'s byte offset |
|---|---|---|
| interleaved | `P · Q`, `Q = Σ Bᵢ` | `(k div C)·Q + F_{k mod C}`, `Fᶜ = Σ_{j<c} Bʲ` |
| planar, numeric channel *c* | `P · Bᶜ` | `k · Bᶜ` |
| planar, bool channel | `ceil(P/8)` | bit `k mod 8` of byte `k div 8`, LSB-first |

Codec 1: `entry.length` must equal the decoded size — checked **before any fetch** (`[R-COD-04]`, [T14]). Then fetch `[offset, offset+length)` and verify `crc32c(stored) == entry.crc` [T1] **before decoding** (`[R-CNT-20]`).

### Step 6 — Decode (`[R-COD-01]`: codec first, then the filter's inverse)
Codec 1 is the identity. Then:
* filter 1 → identity.
* filter 2 (byte-shuffle inverse, `[R-COD-10]`): stride `sh` = `Q` interleaved, `Bᶜ` planar numeric, `1` (identity) for a packed bool plane. With `n = L/sh`: `out[j·sh + i] = in[i·n + j]` for `0 ≤ i < sh`, `0 ≤ j < n`. Length unchanged. (Verified against §17.3's float32 example: `00 00 80 3F 00 00 00 40 00 00 40 40` ↔ `00 00 00 00 00 00 80 00 40 3F 40 40`.)

Decoded length must equal the decoded size exactly [T3] — under codec 1 this is implied by [T14], but assert it anyway; allocation comes from declarations, never from stored data (`[R-SER-07]`, `[R-SEC-02]`).

### Step 7 — Extract
Interleaved numeric: `Bᶜ` bytes at `u·Q + Fᶜ`. Interleaved bool: the single byte at `u·Q + Fᶜ`. Planar numeric: `Bᶜ` bytes at `u·Bᶜ`. Planar bool: bit `u mod 8` of byte `u div 8`.

Never return a padding position (`[R-GEO-04]`) — step 1 already excludes them, since padding positions have coordinates outside the extents. Never return a pad bit.

### Step 8 — Return
Bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`): NaN payloads preserved, −0.0 ≠ +0.0.

### Worked check, interleaved
§11.2/§11.4's layer: extents (1024, 2048), tiles (256, 256), G = (4, 8), N = 32, P = 65536. Coordinate (300, 700) → t = (1, 2), s = 10, u = 44·256 + 188 = 11,452. Entry 10 at region byte 200, segment 0. Channels `a` (uint8), `b` (uint16) → Q = 3, F_a = 0, F_b = 1, decoded size 196,608. `b` sits at byte `11452·3 + 1 = 34,357`.

### Worked check, planar
Same layer, C = 4, channel 2 → k = 2·32 + 10 = 74, entry at region bytes [1480, 1500) (§15.4's own example). If channel 2 is float64: decoded size 524,288, value at byte `11452·8 = 91,616`. If channel 2 is bool: decoded size 8192, value = bit `11452 mod 8 = 4` of byte `1431`.

---

## 6. Sections I actually needed

**In full:** §2.3–2.5, §3.1–3.2, §4.1–4.7, §6.1–6.3, §7.1–7.4, §8.1–8.2, §11.1–11.4, §12.1–12.3, §13.1–13.3, §14.1–14.5, §15.1–15.4, §17.1, §17.3, §19.1–19.4, §21.2–21.6, §21.9, Appendix A (my first test vector), Appendix B (finding aid).

**Partially:** §5.1 (`[R-CNT-27]` only), §5.2 (only to learn a reader never checks coverage), §9.1 + §9.5 (immutability licenses caching; trailer-at-end-or-fail), §16.1–16.2 (only the A/S/A_slab bounds — already in §7.4's table), §17.2 (codec 1 and `[R-COD-04]`), §18.2 (the encoding byte, for [R1] and `[R-MTA-03]`).

**Not needed:** §1, §6.4, §9.2–9.4, §9.6–9.7, §10, §18.1/18.3/18.4, §20, §22, §23, §24, Appendices C–H.

**§19.3 is the single most valuable section in the document.** Without it the layer-record validation set is scattered across thirteen sections and is not assemblable in a weekend. With it, it is a checklist.

---

## 7. Honest hours

| Work | Hours |
|---|---|
| CRC-32C table-driven + check vectors | 0.5 |
| Front block, trailer, version/flag gates, ordered validation | 2 |
| Directory CRC, record framing, top-level walk, name namespace | 2.5 |
| Layer-record parse + the §19.3 validation set (~30 checks) | 5 |
| Geometry, ordinals, overflow-checked derived quantities | 2 |
| Index region: segments, CRC array, §15.3 classification | 3 |
| Tile read: codec 1, shuffle inverse, four extraction paths | 4 |
| Outcome plumbing (4 classes, scope propagation, resource-vs-validity split) | 1.5 |
| Tests: Appendix A + hand-built vectors per §21 row | 3 |
| **Total, codec-1 reader** | **≈ 23** |
| Add deflate/zstd/lz4 bindings + zstd frame-header constraints (dict ID, checksum flag, window size, content size, exactly-one-frame) to reach `[R-CNF-03]` | +6–8 |

A real weekend, not a comfortable one. The long pole is the validation set, not the data path.

---

## 8. The three hardest things to get right

**1. Sentinel-before-domain ordering, paired with fill-vs-failure.** §15.3's table is *ordered*, and `[R-IDX-02]` exempts sentinel fields from the 2⁶³−1 domain rule. Check the domain first and every sparse tile in every conforming file becomes a read failure. Get `[R-TYP-09]`/`[R-CNF-09]` wrong in the other direction and a corrupt tile silently returns fill — the failure mode the format was built to make impossible. The two mistakes are inverses; only one of them is loud.

**2. Verify-before-act as an ordering constraint on I/O.** `[R-ENC-05]` forbids allocating, seeking, or fetching on any file-derived integer before its covering checksum verifies; §8.2's chain has seven links. The natural implementation — read entry *k*, seek, read the payload, then verify — violates it. The index is the sharpest case: *two* independent CRC verifications (`crc_of_crc_array` over the whole array, then the containing segment's CRC) must both pass before entry *k*'s twenty bytes may be interpreted at all — and the array's own length derives from `entry_count`, itself trustworthy only after the directory CRC.

**3. Overflow discipline at 2⁶³−1, over derived quantities.** Not 2⁶⁴. `[R-ENC-04]` covers *ten* named products for a single layer (L2's instance list). §11.2 explicitly forbids the `(E+T−1)/T` ceiling idiom because the intermediate sum leaves the domain. In a u64 language this wraps silently; in an i64 language it traps by accident and must still be handled deliberately at the boundary.

*Runner-up:* the bool asymmetry. Packed LSB-first at ⌈P/8⌉ bytes planar, a full byte at element size 1 interleaved, one byte of fill in the channel entry either way, and a shuffle stride of 1 in the packed case. Four extraction paths where a naive design has one.

---

## 9. Places I had to re-read, guess, or assemble

* **The decoded-size function** is assembled from §14.2's table row (labelled "planar, **numeric** channel c" — the only signal), §14.3's sentence, and §12.1's parenthetical "except that a planar bool plane is sized by packing." Three places, one function.
* **The layer-record validation set**: §19.3 lists it, but every *value* lives elsewhere (§7.4 table, §11.1, §11.2, §11.4, §12.2, §13.2, §14.1, §15.1, §16.1, §16.2, §17.2, §17.3, §4.6).
* **The byte offsets of the CRC array and segment *s*** inside the index region are the reader's own arithmetic; §15.1 gives the layout, §15.4 gives entry ranges, `[R-CNT-17]` gives the total. §15.4's `entry_count = 1,000,000` example is what confirmed mine.
* **A/S/A_slab bounds appear three times** (§7.4 table, §16.1/§16.2, Appendix B). A no-alignment reader still must implement all five checks — easy to skip on the assumption that "no alignment" means "ignore the fields."
* **The open-tier partial layer parse** (Finding O-4 below).
* **§4.5's coverage claim** required cross-checking §8.1 to confirm it is total (Finding O-5).

---

# Findings

## BYTE-LEVEL AMBIGUITY

**None.** Every candidate I raised was refuted against the text. The four I worked hardest on, and what killed each:

* *Sentinel entries vs. the 2⁶³−1 domain rule* (would flip fill ↔ read-failure on every conforming sparse file) — killed by `[R-IDX-02]`'s explicit exemption plus §15.3's row ordering plus §15.2's rationale.
* *Two layers both carrying an invalid (e.g. empty) name — reject-file or reject-layer?* — killed by `[R-CNF-12]`: for a nonconforming file no acceptance obligation exists, so the blast-radius divergence is licensed. §24's note blesses exactly this ("an implementation that instead rejects the whole nonconforming file is exercising `[R-CNF-12]`'s licence, not failing the vector").
* *`[R-COD-07]`'s lz4 cap on a planar layer with mixed channel types* — see Observation O-6; resolvable on purpose, and unreachable inside §21.9's guarantees.
* *`[R-SLB-05]`'s "writer defect" vs. `[R-CNT-21]`'s unconstrained dead space for a generation-1 inter-tile gap* — see Observation O-7; resolved by §9.7, §22.3, and §21.1's normative register completeness (no row → not a violation).

## CONTRADICTION

**C-1. §21.6's framing vs. `[R-CNT-15]` and `[R-CNF-12]`, for a reserved-range record type with MU = 0.**

* §21.6 (line 2668, and its row at line 2677): *"These are defined behaviors, not errors. A reader that treats any of them as a failure is the nonconforming party."* — with the row **"An unknown record type carries MU = 0 | Ignored, and preserved or dropped per its PE bit | `[R-CNT-15]`, `[R-WRT-08]`"**.
* `[R-CNT-15]` (§7.2, line 785): *"a record type from the experimental range is conforming … while one from the reserved range is a value this specification has not assigned — emitting it is a violation, and a verifier MUST treat a reserved-range record type as a validity error at the record's governing scope."*
* `[R-CNF-12]` (§2.4, line 203): *"For a nonconforming file no acceptance obligation exists — a reader MAY reject it upon detecting any violation, including violations whose assigned detector is the verifier."*

**Discriminator.** A file otherwise identical to Appendix A, extended with one top-level record of type `0x0003`, flags `0x0000` (MU = 0, PE = 0), `inline_length = 0`, extent `(0, 0)`. Verifier A, following §21.6 and the register (which has no row for a reserved-range type), **certifies the file conforming**. Verifier B, following `[R-CNT-15]`'s final clause, **refuses to certify: reject-file**. Symmetrically, a strict *reader* that rejects the file is, per §21.6's intro sentence, "the nonconforming party," while `[R-CNF-12]` explicitly licenses that rejection.

Two of §21.6's own rows already contradict its intro from the inside — the `[R-MTA-05]` row and the `[R-CNT-22]` row both say *"The file is nonconforming"* while sitting under the heading "Conditions that are **not** violations." So the table's real subject is "conditions that do not make a *reader* fail," and the intro's two sentences overstate it. The reserved-range case is where the overstatement becomes load-bearing, because that is the one row where the file's conformance genuinely turns on which range the value came from.

**Effect on my charter's product:** none. Both readings ignore the record on the read path. The divergence is in certification and in §21.6's characterization of a strict reader.

**What I searched to refute it:** §21.1's precedence clause ("where a row and the rule it cites diverge, the rule governs") — but it is scoped to "the register below," and §21.6 is introduced separately as a non-register table, so it does not cleanly reach; §10.3 `[R-EXT-03]` (restates the reader outcome, is silent on file conformance); §21.5's R10 (correct as written — ignore-record is an outcome class, not a conformance verdict, per §2.4); the register's §21.2 and §21.3 tables for any verifier row on reserved-range types (none exists); `[R-CNF-02]` (confirms the *experimental* range is conforming, and by contrast confirms the reserved range is not).

## OBSERVATION

**O-1. Register completeness gaps (§21.1 declares completeness normative: "a violation this specification names and the register omits is a defect in this document").** Five named violations have no register row, so §21.8's per-row corpus obligation and §24's per-row manifest requirement would never exercise them:

* `[R-MTA-03]` (§18.2, line 2006): a user-metadata record whose `inline_length` is not 1 is a validity error at the record's containing scope → reject-file top-level, reject-layer as a sub-record. **`R-MTA-03` occurs exactly once in the entire document — at its own definition.** F27/L11 cover only extent slot (0,0); F31 covers only overrun.
* `[R-CNT-25]` (§7.1, line 702): a user-metadata record whose `extent_length` is **less than 5** is a validity error at its containing scope. No row; F27 and L11 name only (0,0).
* `[R-MTA-09]` (§18.2, line 2014): metadata encoding 2 must satisfy the non-tile `[R-COD-06]` frame constraints — frame magic, no skippable/second frame, no nonzero dictionary ID, no content-checksum flag — and "any violation here is ignore-record." **`R-MTA-09` also occurs exactly once, at its definition.** §21.5's R3 covers only "stored bytes fail to decode"; a frame with the Content_Checksum_flag set *decodes fine*, so R3 does not reach it. Discriminator: a top-level UM record, encoding 2, one frame with the checksum flag set, decoding to `{"tarn.title":"x"}` — a reader calling a stock zstd decoder returns the document; a reader enforcing `[R-MTA-09]` reports ignore-record. The rule is unambiguous, so this is a corpus gap, not an ambiguity.
* Trailer `generation` above 2⁶³−1. §6.2's table cell says `1 ≤ generation ≤ 2⁶³ − 1 (`[R-ENC-03]`)`, which makes it a reader MUST; but `[R-CNT-06]`'s ordered validation list says only "generation ≥ 1", and F3's instance list (`dir_offset; dir_length; committed_file_length; …extent_offset; extent_length`) omits generation while F16 covers only generation = 0. Discriminator: Appendix A with bytes [80,88) = `00 00 00 00 00 00 00 80` and a recomputed trailer CRC.
* A reserved-range record type as a verifier-detected validity error — Finding C-1.

**O-2. Row F7 cites the wrong governing rule, and `[R-CNT-27]` is cited nowhere.** F7 ("File size is below the 128-byte minimum") gives its Governing rule as `[R-CNT-01]`, which says only that F equals the committed file length and is a multiple of 64. The 128-byte minimum is `[R-CNT-27]` (§5.1, line 485). Mechanical check: `R-CNT-27` appears exactly once in the document — at its own definition. Under §21.1's "where a row and the rule it cites diverge, **the rule governs**," a literal reading of F7 nullifies the check it names; it survives only because `[R-CNT-27]` states the MUST independently.

**O-3. Row L23 has no reader-detectable instance in format major 1.** L23 ("A layer record's sub-record itself contains records (nesting depth beyond two)") is assigned detector *reader*, detection point *layer access*. But major 1 defines exactly two record types: type 0x0001 nested as a sub-record is already L25, and type 0x0002's inline payload is fixed at one byte (`[R-MTA-03]`). For an *unknown* sub-record type a reader cannot parse the inline payload at all, so it cannot see nesting. §21.8 requires a vector per row; I cannot construct one whose expected verdict a conforming reader would reach.

**O-4. The open tier requires a partial layer-record parse that no register row models.** §19.1 step 4 obliges a reader to parse and check each layer record's *name* at open (`[R-ENC-12]`, and rows L4/L6/L7 confirm detection point "open"), while the containment of that name within `inline_length` is L22, detected at *layer access*. A minimal reader must therefore decide what to do with a layer record whose `name_len` overruns `inline_length` one tier before the tier that owns the check. The outcome is reject-layer either way — and §2.4's "A reader MAY still list the file's layers, including the rejected one's name" plus §19.2's separate "layer-name namespace" bullet confirm that name listing does **not** trigger full layer validation — but the split cost me two re-reads.

**O-5. §4.5's enumeration of interior checksum fields is short by one.** It names "each segment CRC array and each layer record's `crc_of_crc_array`" as the fields that are both comparison-verified and covered by exactly one further checksum. The tile-index **entry's `crc` field** is equally both: comparison-verified against the stored tile's bytes, and covered by its segment CRC. §8.1's map is complete (its "Stored tile" and "Tile-index region" rows together account for it), so the top-level coverage claim holds; only §4.5's prose list is incomplete. I had to walk §8.1 to convince myself the coverage claim was total.

**O-6. `[R-COD-07]`'s lz4 cap is phrased against a per-layer decoded size that a planar layer does not have.** "a layer whose **tiles'** decoded size exceeds `0x7E000000`" presupposes one value; a planar layer with mixed channel types has one per channel (`P·Bᶜ`, or `⌈P/8⌉`). Reading "any plane exceeds" → reject-layer; reading "only the offending planes" → the layer is accepted and the small-channel tiles are served. Constructible discriminator: planar, `d = 2`, `T = (16384, 16384)` so `P = 268,435,456`, `E = T` so `N = 1`, `C = 2` with channel 0 float64 (`P·8 = 2 GiB > 0x7E000000`) and channel 1 uint8 (`P·1 = 256 MiB < cap`), codec 4, `entry_count = 2`. I am **not** filing this as byte-level: the cap exists because it is the LZ4 block decoder's output capacity, which resolves the reading to "any"; L45's phrasing ("per-tile decoded size") is already the clearer form; and because the cap is ~1.97 GiB, every discriminator necessarily involves a tile far above §21.9's 256 MiB minimum guarantee, where `[R-ERR-04]` independently licenses a reader to decline — so the divergence is unreachable inside the guaranteed envelope. Suggest §17.2 adopt L45's wording.

**O-7. `[R-SLB-05]`'s "writer defect" sentence versus dead space's unconstrained status.** `[R-SLB-05]` (§16, line 1736): "a byte the live state neither claims nor accounts for as declared padding is dead space, and a commit that produces dead space it did not supersede is a writer defect (`[R-CNT-02]`, `[R-LIF-02]`)" — and `[R-CNT-02]`'s violation is "not a conforming file." Against that: `[R-CNT-21]` ("Every other byte of the file is dead space … its content is unconstrained, and no conformance requirement applies to it"), `[R-LIF-08]` ("their content is not its concern"), `[R-SEC-03]` ("countable rather than absent"), and — decisively — §21.1's normative register completeness, since no row makes a gratuitous gap a violation. Discriminator: a generation-1 file with a 100-byte unclaimed run between two stored tiles, no alignment or slab declared. Resolved toward "the verifier counts it and certifies." Worth noting that `[R-CNT-21]`'s *definitional* clause ("bytes an earlier commit wrote that the live state no longer reaches") does not literally cover a first-generation gap, so the resolution rests on the sentence's leading clause rather than on its gloss. One sentence in §16 would close it.

**O-8. §21.3 silently skips row number L40.** Rows run L1–L39, L41–L48; the stated "47 conditions" is correct. §14.4 documents the retirement of `[R-SER-04]` explicitly; the L40 gap gets no such note. Purely editorial, but a corpus author enumerating L1..L48 will stall.

**O-9. Everything numeric in the document checks out.** I recomputed, from the spec text alone: CRC-32C(`"123456789"`) = `0xE3069283` ✓; CRC-32C(zero bytes) = `0x00000000` ✓; Appendix A's trailer CRC over trailer bytes [0,60) = `0xE00938D2`, stored `D2 38 09 E0` ✓; the all-sentinel full-segment constant over 65,536 × `FF ×16 00 ×4` = `0xEECB3BB2` ✓. I re-derived by hand every worked example in §11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4, §17.3 and §20.3 — grid counts, ordinals, byte offsets, packed-bool bytes `55 01` / `55 FD`, the shuffle permutation, the 20,000,064-byte index region and its 339,180 segment-relative offset, the 644-byte re-emitted index — with no error found. §21.8's "121 conditions over 213 named instances" reproduces exactly on a manual recount (38 + 47 + 26 + 10 = 121; 69 + 81 + 43 + 20 = 213). Appendix A is a usable first test vector as printed.

**O-10. The charter's product cannot claim conformance, and must say so in its own diagnostics.** §2.3 `[R-CNF-03]` forecloses subset readers; `[R-ERR-04]` requires that a refusal on capability or resource grounds be reported as such and never as a validity error, "the two send a user to opposite remedies." A codec-1-only reader that reports "codec 3" as "corrupt file" is the exact failure mode that rule was written against.

---

# Verdict

**IMPLEMENTABLE: yes**
**BYTE-LEVEL AMBIGUITIES: 0**
**CONFIDENCE: high**

High for the reader path — the path I was chartered to build, exercised end to end for both layouts, with every constant and every worked example independently recomputed and matching. The one contradiction and the register gaps are documentation defects: they cost a corpus author and a verifier author, not a reader author. I did not exercise the verifier path (coverage partition, overlap detection, alignment/slab invariants, decoded-content obligations) or the updater/compactor path, and make no claim about them.
