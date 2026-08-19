# Round 12 — quiz KEY working transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3982 lines, in four `Read` calls). I read no ADRs, no docs/, no conformance/,
no registry.json, no git history, no web. I ran two Python scripts I wrote myself
(`calc.py`, `calc2.py`) in the scratchpad; they read no files. `calc.py` implements
CRC-32C from the polynomial and validates against three constants the spec itself
states: CRC-32C("123456789") = 0xE3069283, CRC-32C(zero bytes) = 0x00000000, the
all-sentinel full-segment constant 0xEECB3BB2 (§15.4), and Appendix A's trailer CRC
0xE00938D2. All four reproduced exactly, so the checksum routine is the spec's.

---

## Q01 — trailer CRC bytes

Trailer layout §6.2. Bytes [0,60) assembled little-endian:

```
8a4e5241540d0a1a 0100 0000 00000000
0700000000000000  generation = 7
1000000000000000  dir_offset = 16
0400000000000000  dir_length = 4
8000000000000000  committed_file_length = 128
a5a5a5a5a5a5a5a5  file_id
00000000          reserved
```

CRC-32C over those 60 bytes = 0xDC0DCE6D. §4.5: "stored as a little-endian `u32`",
so the file bytes at [60,64) are `6d ce 0d dc`.

**Answer: `6dce0ddc`**

Method cross-check: rebuilding Appendix A's trailer (generation 1, file_id
0x0123456789ABCDEF) with the same routine yields 0xE00938D2 → bytes `d2 38 09 e0`,
matching the appendix hex dump exactly.

## Q02 — dir_length and committed_file_length

§7.4 inline-payload field order and widths; §7.2 24-byte record header; §7.1
directory = record sequence + 4-byte CRC.

Inline payload:
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
| 2 dim entries, each (1+1 name) + 8 + 8 = 18 | 36 |
| ch `v` uint16: 1+1 name, 2 type, 1+2 fill | 7 |
| ch `m` bool: 1+1 name, 2 type, 1+1 fill | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| sub-records | 0 |
| **total** | **101** |

Fill framing confirmed by §12.3's worked example: `04 74 65 6D 70 0C 00 04 00 00 C0 7F`
= 12 bytes for a 4-byte name + u16 type + u8 fill-length + 4 fill bytes.

Record = 24 + 101 = 125. dir_length = 125 + 4 = **129**.
Directory occupies [16, 145). §9.2 step 5: "append the pad to the next 64-byte
boundary" → 192; trailer [192, 256). F = **256**, a multiple of 64 (§6.2), and
dir_offset + dir_length = 145 ≤ F − 64 = 192 ✓.

Geometry check: dim 0 extent 0 → G₀ = 0, N = 0, interleaved addressed-tile count 0,
so entry_count = 0, extent slot (0,0), crc_of_crc_array = 0 — consistent with
`[R-CNT-17]`/`[R-CNT-23]`.

**Answer: 129, 256**

## Q03 — interleaved stored tile bytes

G = (⌈2/2⌉, ⌈2/3⌉) = (1,1), N = 1. P = 2·3 = 6. C = 2, Q = 1 + 2 = 3.
Decoded size = P·Q = 18 (§14.2).

In-tile ordinal = u_y·3 + u_x (§11.4, row-major, permanent). Ordinals 2 and 5 have
x = 2 ≥ E_x = 2 → padding positions, whose content `[R-SER-05]` fixes to the
channels' recorded fills (a = 0x7F, b = 0xBEEF → `EF BE` LE).

Decoded image (sample-major, `a` then `b` LE):
`11 02 01 | 22 04 03 | 7F EF BE | 33 06 05 | 44 08 07 | 7F EF BE`

Filter 2, interleaved → stride s = Q = 3 (§17.3), n = 18/3 = 6; byte i of group j
moves to i·n + j:
`11 22 7F 33 44 7F | 02 04 EF 06 08 EF | 01 03 BE 05 07 BE`

Codec 1: "the stored bytes are the filtered image verbatim" (`[R-COD-04]`), and
length 18 = decoded size ✓.

**Answer: `11227f33447f0204ef0608ef0103be0507be`** (36 hex digits)

## Q04 — planar bool tile bytes

G = (⌈3/2⌉, ⌈7/5⌉) = (2,2). P = 2·5 = 10. Tile (1,1) covers r ∈ [2,4), c ∈ [5,10).
Real coords: r = 2 only (E_r = 3), c = 5,6 only (E_c = 7).

In-tile ordinal = u_r·5 + u_c:
- 0 → (2,5) = true; 1 → (2,6) = false; 2–4 → (2,7..9) padding; 5–9 → r = 3 padding.

`[R-SER-05]`: every padding position encodes the fill bit — fill 0x01 = true.
So values 0..9 = 1,0,1,1,1,1,1,1,1,1.

§14.3 packed LSB-first, decoded size ⌈10/8⌉ = 2:
byte 0 = bits 0..7 = 1,0,1,1,1,1,1,1 = 0xFD; byte 1 = bits 0,1 = 1,1, and pad bits
2–7 "MUST carry the plane's channel's fill bit" = 1 → 0xFF.

§17.3: "for a packed boolean plane s = 1 and the filter is the identity". Codec 1 →
stored verbatim.

**Answer: `fdff`**

## Q05 — offset of beta's tile-index region

Appendix G item 3: "For each layer in ascending layer-name byte order: its stored
tiles in disk-ordinal order, then its tile-index region; then any record extents in
ascending record order — all of them after every layer's tiles and index region…
then the directory." Item 5: no declared alignment/slab, so "Each structure begins
where the previous one ended". `[R-LIF-02]` creation path: writing begins at 16.

`alpha` < `beta` bytewise. Index-region size = entry_count×20 + ⌈entry_count/2¹⁶⌉×4.

| structure | bytes | range |
|---|---|---|
| front block | 16 | [0,16) |
| alpha tiles 100+150 | 250 | [16,266) |
| alpha index 2·20+4 | 44 | [266,310) |
| beta tiles 200+210+220 | 630 | [310,940) |
| beta index 3·20+4 | 64 | [940,1004) |

The two user-metadata extents (300 and 80 bytes) are emitted after every layer's
tiles and index, so they do not shift beta's index.

**Answer: 940**

## Q06 — slack total

§9.7 claimants: front block, live trailer, directory, each record's extent, and each
non-sentinel entry's stored extent. §9.7 / `[R-IDX-03]`: an entry classified
reject-tile on a *structural* ground "contributes no stored extent to the walk";
an entry whose only defect is a failing stored-bytes crc "keeps its extent" and
"does not make the walk incomplete".

- entry 0 (offset 100, length 200): only defect is the crc → extent [100,300) claimed.
- entry 1 (offset 8): offset < 16, structural reject-tile → contributes nothing;
  [8,58) falls to slack.
- index region length = 2·20 + ⌈2/2¹⁶⌉·4 = 44 → [700,744).

Claimants: [0,16) 16 + [100,300) 200 + [400,460) 60 + [700,744) 44 + [800,900) 100
+ [960,1024) 64 = 484 bytes, pairwise disjoint. Slack = 1024 − 484 = **540**
(a complete, non-partial total).

**Answer: 540**

## Q07 — type 0x0005, MU = 0

Type 0x0005 lies in the record-type reserved range 0x0003–0x7FFF (§10.2).

(a) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file;
MU = 0 → ignore-record." → **ignore-record**.

(b) Same rule: "one from the reserved range is a value this specification has not
assigned — emitting it is a violation, and a verifier MUST treat a reserved-range
record type as a validity error at the record's governing scope." Register row F36
(detector *verifier*, certification). An established violation → `[R-CNF-11]`: "a
verifier that has established any violation reports *nonconforming*."

**Answer: ignore-record; nonconforming**

## Q08 — declined document + reserved layer flag bit

The 16 MiB decline is `[R-MTA-09]`: "not a finding that the file is nonconforming…
it fixes the file's verdict as *cannot establish* only where the verifier established
no violation elsewhere."

Reserved bit 5 of a layer record's flags: §7.2 "bits 2–15 reserved… writers MUST
emit zero… a verifier MUST treat a nonzero reserved flag bit… as a validity error at
the record's governing scope" — register row L47, verifier, reject-layer. That is an
established violation.

`[R-CNF-11]`: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it was
unable to check."

**Answer: nonconforming**

## Q09 — three planar channels

- ch 0: valid non-sentinel, crc matches, decodes → returns 0x0007 unaltered
  (`[R-MDL-02]`, `[R-TYP-04]`).
- ch 1: sentinel → `[R-TYP-08]`/`[R-RDR-04]` step 4: reads as that entry's channel's
  recorded fill, bit-exactly → 0x1111.
- ch 2: stored bytes fail crc → reject-tile (§8.2, row T1). `[R-CNF-09]`: "a read of a
  rejected tile MUST NOT silently return fill"; `[R-TYP-09]` repeats it. `[R-RDR-04]`
  step 8 lets a reader return the validating entries with a per-entry report, "but MUST
  NOT stand fill in for a rejected tile's positions."

**Answer: 0007; 1111; failure**

## Q10 — zstd window size

P = 2·3 = 6, Q = 1 + 2 = 3, decoded size = 18 bytes. Single_Segment_Flag clear, so
the Window_Descriptor governs and Window_Size = 1024 > 18.

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's decoded
size; a reader MUST treat either as a validity error at tile scope, both being
header-checkable." §17.2's own note anticipates this: a sub-1 KiB tile "is therefore
encodable under codec 3 only as a single-segment frame". Register row T21: detector
reader, Detected = tile use.

**Answer: reject-tile; tile use**

## Q11 — lz4 declared-size bound

G = (1,1,1), N = 1. P = 2 · 12500 · 10000 = 250,000,000.
Planar: `v` float64 plane = P·8 = 2,000,000,000 bytes; `m` bool plane packed =
⌈P/8⌉ = 31,250,000 bytes (§14.3).

`[R-COD-07]`: "in a planar layer each channel's plane carries its own decoded size…
and the largest governs" against 0x7E000000 = 2,113,929,216.
2,000,000,000 ≤ 2,113,929,216 → no violation. No overflow anywhere (N·P, P·Bᶜ, C·N
all far below 2⁶³−1).

**Answer: no, 2000000000**

## Q12 — dropping an MU=0/PE=0 experimental record

0x9100 ≥ 0x8000 → experimental range (§10.2); §21.6 makes such a record with MU = 0
a conforming, ignorable record. §20.4's MU = 0 / PE = 0 row governs:
"An appender may drop it only in a commit that *independently* changes the scope the
record attaches to: … for a top-level record, the file's layer set or another
*non-layer* top-level record. Superseding a stored tile's bytes is not such a change
for either kind … so a commit whose only change is a supersede MUST retain the record."

(a) replacing one tile's stored bytes = a supersede → MUST retain → **no**.
(b) adding layer B changes the file's layer set → **yes**.

**Answer: no; yes**

## Q13 — ignore-lane bit 20

Bit 20 ∈ 16–31 = ignore lane (§6.2 table, §6.3).

(a) `[R-CNT-08]`: "a set ignore-lane bit is not a file-conformance violation… files
carrying them are conforming files this text's readers ignore." `[R-CNF-02]` names
this writer obligation as one whose violation is expressly not a file-conformance
violation. §21.6 row: "An ignore-lane flag bit (16–31) is set | Ignored; the file is
conforming". → **yes**.
(b) "MUST ignore all bits in the ignore lane" → **ignore**.
(c) No violation established, nothing unable to check → **conforming**.

**Answer: yes; ignore; conforming**

## Q14 — planar ordinals and index offsets

G = (⌈4/1⌉, ⌈4096/64⌉, ⌈4096/64⌉) = (4, 64, 64); N = 16,384.
Tile coords (2, 130 div 64, 1000 div 64) = (2, 2, 15).
s = 2·(64·64) + 2·64 + 15 = 8192 + 128 + 15 = 8335 (§11.4).
Planar disk ordinal = c·N + s = 4·16384 + 8335 = 65,536 + 8,335 = **73,871**.

(b) §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
byte 20·k" → 20 · 73,871 = **1,477,420**.

(c) §15.4: segment s covers [s·2¹⁶, …) → 73,871 div 65,536 = **1**.

(d) entry_count = C·N = 5 · 16,384 = 81,920. Entry array = 81,920 · 20 = 1,638,400
bytes; the segment CRC array follows contiguously with no padding (§15.1), and has
⌈81,920/65,536⌉ = 2 u32s. Segment 1's u32 is at 1,638,400 + 4·1 = **1,638,404**.

**Answer: 73871, 1477420, 1, 1638404**

## Q15 — fill change re-emission

G = (⌈5/4⌉, ⌈5/4⌉) = (2,2); s = t_y·2 + t_x.

| tile | ordinal | padding positions |
|---|---|---|
| (0,0) | 0 | 0 |
| (0,1) | 1 | 12 |
| (1,0) | 2 | 12 |
| (1,1) | 3 | 15 |

§20.3's shape-(c) example is decisive: "A change confined to the directory —
clearing a slab declaration, renaming a layer, or changing a channel's fill value on
a layer with no padding position and no pad bit… A fill change on a layer carrying
either additionally requires re-emitting the affected stored tiles, whose content
`[R-SER-05]` fixes — which makes it shape (b)."

`[R-SER-05]` requires every padding position to encode the recorded fill; with the
fill now 0xABCD, tiles 1, 2 and 3 carry `00 00` where `CD AB` is required, so their
bytes must be re-emitted. Tile 0 has no padding position and no pad bit (interleaved,
so §14.3 packing is not in play), so its stored bytes stay valid and are not
re-emitted — the layer's whole index region is re-emitted regardless (`[R-WRT-04]`),
but that is not tile bytes.

**Answer: 1, 2, 3**

---

No question in this slate came out underdetermined. Each turned on an explicit rule
or an explicit worked example in the document; where two readings were available
(Q06's treatment of a structurally-malformed entry, Q15's re-emission obligation,
Q08's precedence of an established violation over a decline), the document names the
tie-break in its own text.
