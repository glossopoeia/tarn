# Cleanroom round 12 — quiz answerer transcript

## Disclosure

Files read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only, in full
(lines 1–3983, via the Read tool in six chunks, plus `wc`). No other file in the
repository was read, listed, or grepped. No ADRs, no `docs/`, no `conformance/`,
no `spec/registry.json`, no `PLAN.md`/`AGENTS.md`/`README.md`, no git history, no
web access.

Computation run: two self-written Python scripts in the scratchpad
(`calc.py`, `calc2.py`) reading no project files — a CRC-32C implementation
(validated against §4.5's `"123456789"` = `0xE3069283`, CRC of zero bytes = 0,
and Appendix A's trailer CRC `0xE00938D2`) plus integer arithmetic for grid
counts, ordinals, decoded sizes, byte-shuffle, and bit packing.

Prior knowledge of zstd/deflate/lz4 was used only to read the questions; every
conclusion below is anchored to a sentence in this document.

---

## Q01 — trailer bytes [60, 64)

§6.2's layout table: offset 0 magic (8), 8 version_major (u16), 10
version_minor (u16), 12 flags (u32), 16 generation (u64), 24 dir_offset (u64),
32 dir_length (u64), 40 committed_file_length (u64), 48 file_id (u64), 56
reserved (4 bytes), 60 trailer CRC (u32) = "CRC-32C over trailer bytes [0, 60)".
All multi-byte fields little-endian (`[R-ENC-01]`); CRC stored as a
little-endian u32 (`[R-ENC-09]`).

Bytes [0,60):

```
0000 8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
0010 07 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
0020 04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
0030 a5 a5 a5 a5 a5 a5 a5 a5 00 00 00 00
```

CRC-32C = `0xDC0DCE6D`; stored little-endian → `6D CE 0D DC`.

**Answer: `6dce0ddc`**  (my CRC routine reproduces Appendix A's `D2 38 09 E0`
for the minimal file, so the implementation is the one §4.5 specifies.)

## Q02 — dir_length and committed_file_length

Layer record = 24-byte header (§7.2) + inline_length bytes. §7.4's field order:

| field | bytes |
|---|---|
| name `grid` (u8 len + 4) | 5 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| A u64 | 8 |
| S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| C u16 | 2 |
| 2 dim entries, each (1+1) + 8 + 8 = 18 | 36 |
| ch0 `v` uint16: (1+1) + 2 + (1+2) | 7 |
| ch1 `m` bool: (1+1) + 2 + (1+1) | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| sub-records | 0 |
| **total inline_length** | **101** |

Record = 24 + 101 = 125. §7.1: the directory region's "final 4 bytes are a
CRC-32C over the preceding dir_length − 4 bytes; those covered bytes are the
record sequence itself". So dir_length = 125 + 4 = **129**.

Consistency: E₀ = 0 → G₀ = 0 → N = 0, so entry_count = 0 (`[R-CNT-17]`),
extent slot (0,0) and crc_of_crc_array = 0 (`[R-CNT-23]`) — as stated.

Directory occupies [16, 145). `[R-LIF-02]` step 5: "append the pad to the next
64-byte boundary … and the new trailer". 145 → 192 (47 pad bytes); trailer
[192, 256). F = **256**, a multiple of 64 (`[R-CNT-01]`), and
dir_offset + dir_length = 145 ≤ F − 64 = 192 (`[R-CNT-06]`).

*Noted tension:* `[R-CNT-05]` says "a longer gap is conforming, and no
conforming commit produces one". The question stipulates a creator emitting in
one commit, so step 5 binds and F is fixed at 256.

**Answer: 129, 256**

## Q03 — interleaved tile bytes

G_y = ⌈2/2⌉ = 1, G_x = ⌈2/3⌉ = 1, N = 1, P = 2·3 = 6 (`[R-GEO-03]`).
Q = 1 + 2 = 3; decoded size P·Q = 18 (`[R-SER-02]`).

In-tile ordinal = u_y·3 + u_x (`[R-GEO-06]`, row-major, permanent). Ordinals
2 and 5 have u_x = 2 → x = 2 ≥ E_x = 2, so they are padding positions; per
`[R-SER-05]` a writer "MUST encode, for each channel the position carries,
that channel's fill value" — a = 0x7F, b = 0xBEEF → bytes `EF BE`.

Decoded image (sample-major, declared channel order, LE):
`11 02 01 | 22 04 03 | 7f ef be | 33 06 05 | 44 08 07 | 7f ef be`

Filter 2, interleaved → stride s = Q = 3 (`[R-COD-10]`); n = 18/3 = 6; byte i
of group j goes to offset i·n + j:

`11 22 7f 33 44 7f | 02 04 ef 06 08 ef | 01 03 be 05 07 be`

Codec 1: "the stored bytes are the filtered image verbatim" (`[R-COD-04]`).

**Answer: `11227f33447f0204ef0608ef0103be0507be`**

## Q04 — packed planar bool tile

G_r = ⌈3/2⌉ = 2, G_c = ⌈7/5⌉ = 2; P = 2·5 = 10. Tile (1,1) covers r ∈ [2,4),
c ∈ [5,10). Real positions: (2,5) at in-tile ordinal 0, (2,6) at ordinal 1;
the other eight are padding (r = 3 ≥ 3, or c ≥ 7).

§14.3: "value k occupies bit k mod 8 of byte k div 8 … the decoded size is
⌈P/8⌉" = 2 bytes. Padding positions carry the fill bit and "Every pad bit MUST
carry the plane's channel's fill bit" (`[R-SER-05]`); fill = 0x01 = true = 1.

bits by ordinal 0..9 = 1,0,1,1,1,1,1,1,1,1; pad bits 10..15 = 1.
byte 0 = 0b1111_1101 = 0xFD; byte 1 = 0b1111_1111 = 0xFF.

Filter 2: "for a packed boolean plane s = 1 and the filter is the identity"
(`[R-COD-10]`). Codec 1 stores verbatim.

**Answer: `fdff`**

## Q05 — offset of layer `beta`'s tile-index region

Appendix G item 3: "For each layer in ascending layer-name byte order: its
stored tiles in disk-ordinal order, then its tile-index region; then any record
extents … all of them after every layer's tiles and index region … Each
structure begins where the previous one ended, save where alignment forces a
gap". No A, no A_slab (item 5 / the stated declarations). Creation writes
"beginning at offset 16" after the front block (`[R-LIF-02]`).

`alpha` < `beta` in byte order.

| structure | range |
|---|---|
| front block | [0, 16) |
| alpha tile 0 (100) | [16, 116) |
| alpha tile 1 (150) | [116, 266) |
| alpha index: 2·20 + ⌈2/2¹⁶⌉·4 = 44 (`[R-CNT-17]`) | [266, 310) |
| beta tile 0 (200) | [310, 510) |
| beta tile 1 (210) | [510, 720) |
| beta tile 2 (220) | [720, 940) |
| **beta index: 3·20 + 4 = 64** | **[940, 1004)** |

The 300-byte and 80-byte user-metadata extents come after every layer's tiles
and index region, so they do not shift this.

**Answer: 940**

## Q06 — slack total

§9.7 claimants: the directory, each record's extent, the stored extent of each
non-sentinel entry, plus "The front signature block at [0, 16) and the live
trailer at [F − 64, F) … claimed by the walk as well". A layer record's extent
slot addresses the index region, which "enters the walk once, as that record's
extent"; "A record is not a claimant of its own".

- front block 16
- trailer [960, 1024) 64
- directory [800, 900) 100
- index region at 700, length 2·20 + 4 = 44
- top-level UM extent [400, 460) 60
- entry 0 [100, 300) 200 — `[R-IDX-03]`: "An entry whose only defect is that
  its stored bytes fail its crc is well-formed … its extent stands and it keeps
  its place … in the coverage walk."
- entry 1 offset 8 → `offset < 16 (non-sentinel)` = *structural*: reject-tile →
  "contributes … none to `[R-LIF-08]`'s coverage walk, so any bytes it
  nominally addressed … fall to slack." Contributes 0.

Claimed = 16 + 64 + 100 + 44 + 60 + 200 = 484. Slack = 1024 − 484 = **540**.

The walk completes (the structural entry "does not make the walk incomplete";
the verifier did not elect to stop), so this is an exact total, not partial.

**Answer: 540**

## Q07 — reserved-range top-level record, MU = 0

Type 0x0005 lies in the record-type reserved range 0x0003–0x7FFF (§10.2).

(a) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file;
MU = 0 → ignore-record. … Readers of both apply the MU rule above unchanged."
Outcome class: **ignore-record**.

(b) Same rule: "one from the reserved range is a value this specification has
not assigned — emitting it is a violation, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing
scope." Register row F36 (detector verifier, certification). An established
violation → `[R-CNF-11]`: "a verifier that has established any violation
reports *nonconforming*". Verdict: **nonconforming**.

**Answer: ignore-record; nonconforming**

## Q08 — declined metadata decode plus a reserved layer flag bit

The metadata decline alone would give *cannot establish* (`[R-MTA-09]`). But
"reserved bit 5 set" on a layer record's flags is register row L47 ("Any of a
layer record's or sub-record's reserved flag bits 2-15 is set", detector
verifier, reject-layer), governed by `[R-CNT-12]`: "a verifier MUST treat a
nonzero reserved flag bit … as a validity error at the record's governing
scope."

`[R-CNF-11]`: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it
was unable to check, and *cannot establish* is available only to a traversal
that established no violation."

**Answer: nonconforming**

## Q09 — planar point read across three channels

- ch 0: verified, decodes → return the bit pattern unaltered (`[R-MDL-02]`,
  `[R-TYP-04]`) → **0007**
- ch 1: sentinel → `[R-TYP-08]` / `[R-RDR-04]` step 4: "every requested sample
  position of its tile reads as fill — the entry's channel's recorded fill in a
  planar layer … bit-exactly" → **1111**
- ch 2: stored bytes fail crc → reject-tile (`[R-CNT-20]`, T1); `[R-CNF-09]`:
  "a read of a rejected tile MUST NOT silently return fill", and `[R-RDR-04]`
  step 8: "MUST NOT stand fill in for a rejected tile's positions" →
  **failure**

`[R-RDR-04]` step 8 permits failing the whole request, but the question asks
what a reader that returns anything at all must produce.

**Answer: 0007; 1111; failure**

## Q10 — zstd window larger than the decoded size

P = 2·3 = 6, C = 2, Q = 1 + 2 = 3, decoded size P·Q = 18 bytes (`[R-SER-02]`).

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size; a reader MUST treat either as a validity error at tile scope,
both being header-checkable." Single_Segment_Flag clear → Window_Size comes
from the Window_Descriptor = 1024 > 18. §17.2's note confirms this is the
expected trap: "A tile whose decoded size is below 1 KiB … is therefore
encodable under codec 3 only as a single-segment frame."

Register row T21: detector reader, Detected = tile use.

**Answer: reject-tile; tile use**

## Q11 — codec 4 declared-size bound

G = (⌈2/2⌉, ⌈12500/12500⌉, ⌈10000/10000⌉) = (1,1,1), N = 1.
P = 2 · 12500 · 10000 = 250,000,000.

Planar plane decoded sizes (§14.2 / §14.3):
- `v` float64: P · 8 = 2,000,000,000
- `m` bool, packed: ⌈P/8⌉ = 31,250,000

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes … in a planar layer each
channel's plane carries its own decoded size, and the largest governs."

0x7E000000 = 2,113,929,216. Governing size = 2,000,000,000 ≤ 2,113,929,216 →
no violation. (No `[R-ENC-04]` overflow either: N·P and P·Bᶜ are far below
2⁶³ − 1.)

**Answer: no, 2000000000**

## Q12 — dropping an unimplemented MU = 0 / PE = 0 record

§20.4's table, MU = 0 / PE = 0 row: "An appender may drop it only in a commit
that *independently* changes the scope the record attaches to: … for a
top-level record, the file's layer set or another *non-layer* top-level record.
Superseding a stored tile's bytes is not such a change for either kind … so a
commit whose only change is a supersede MUST retain the record."

(a) Replacing one tile's stored bytes with the stored-tile set unchanged is
exactly a supersede → **no**.
(b) Adding layer B changes the file's layer set → **yes**.

**Answer: no; yes**

## Q13 — an ignore-lane flag bit set

Bit 20 ∈ bits 16–31 = ignore lane (§6.2 table, `[R-CNT-08]`).

(a) `[R-CNT-08]`: "a set ignore-lane bit is not a file-conformance violation —
such bits are defined by later minor versions, and files carrying them are
conforming files this text's readers ignore." Reinforced by `[R-CNF-02]` and
by §21.6's row "An ignore-lane flag bit (16–31) is set | Ignored; the file is
conforming". → **yes**
(b) "MUST ignore all bits in the ignore lane (bits 16–31)" → **ignore**
(c) No violation established, and no requirement left unchecked on a capability
or resource ground → **conforming**. (`[R-CNT-26]`'s version_minor floor is a
SHOULD; `[R-CNF-12]`: "a verifier reports a SHOULD deviation as an advisory
that does not bar certification.")

**Answer: yes; ignore; conforming**

## Q14 — planar ordinals and index offsets

G = (⌈4/1⌉, ⌈4096/64⌉, ⌈4096/64⌉) = (4, 64, 64); N = 4·64·64 = 16,384.
entry_count = C·N = 5 · 16,384 = 81,920 (`[R-GEO-03]`).

Tile coords: t_z = 2/1 = 2, t_y = 130 div 64 = 2, t_x = 1000 div 64 = 15.
s = Σ tᵢ·∏_{j>i} Gⱼ = 2·(64·64) + 2·64 + 15 = 8192 + 128 + 15 = 8335.
Disk ordinal = c·N + s = 4·16,384 + 8335 = 65,536 + 8335 = **73,871**.

(b) `[R-IDX-01]`: "The entry for the tile with disk ordinal k is the k-th
entry, at region byte 20·k" → 20 · 73,871 = **1,477,420**.

(c) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))" →
73,871 div 65,536 = **1**.

(d) §15.1's region layout: entry array (entry_count × 20) then the segment CRC
array (⌈entry_count/2¹⁶⌉ × 4), "with no padding anywhere inside the region".
Entry array = 81,920 · 20 = 1,638,400; 2 segments; segment 1's u32 at
1,638,400 + 1·4 = **1,638,404**.

**Answer: 73871, 1477420, 1, 1638404**

## Q15 — tiles re-emitted on a fill change

G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2), N = 4; spatial ordinals s = t_y·2 + t_x.

| tile coords | s | covered y,x | padding positions |
|---|---|---|---|
| (0,0) | 0 | 0–3, 0–3 | 0 |
| (0,1) | 1 | 0–3, 4–7 | 12 |
| (1,0) | 2 | 4–7, 0–3 | 12 |
| (1,1) | 3 | 4–7, 4–7 | 15 |

`[R-SER-05]`: "at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value". Changing the recorded
fill from 0x0000 to 0xABCD changes the required padding bytes of every tile
carrying a padding position. §20.3's shape (c) states this directly: "changing
a channel's fill value on a layer with no padding position and no pad bit. Only
the directory is re-emitted. A fill change on a layer carrying either
additionally requires re-emitting the affected stored tiles, whose content
`[R-SER-05]` fixes."

Tile 0 carries no padding position (and, being interleaved uint16, no pad
bits), so its bytes are unchanged. Tiles 1, 2, 3 must be re-emitted (appended
at new offsets, `[R-LIF-01]`).

**Answer: 1, 2, 3**
