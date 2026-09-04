# Cleanroom round 31 — quiz keyer transcript

Source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4790 lines), read in
full in four `Read` passes plus targeted `grep` anchors against that same file.
No other file read. Local Python only (no file reads): scratch script
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/quiz-keyer/qk_work.py`.

CRC-32C implementation self-check: `CRC32C("123456789") = 0xE3069283`, `CRC32C(b"") = 0`
(§4.5 check vector), and it reproduces Appendix A's published trailer CRC `0x402F157E`
(`7E 15 2F 40`) from the Appendix A trailer bytes. So the CRC used below is this
document's CRC.

---

## Q01 — layer record inline_length

§7.4's field order and widths (name `u8` len + bytes; layout `u8`; linearization `u16`;
codec `u16`; filter `u16`; A `u64`; S `u64`; A_slab `u64`; rank `u8`; C `u16`;
d dimension entries = name + extent `u64` + tile extent `u64`; C channel entries =
name + type `u16` + fill (`u8` len + bytes, length = the type's element size,
`[R-CNT-23]`); index_encoding `u8`; entry_count `u64`; crc_of_crc_array `u32`).

§7.4's worked example fixes the scalar block: "Name and the nine scalars from layout
through channel count occupy 4 + 34 bytes" — so layout…C = 34 bytes.

- name `grid`: 1 + 4 = 5
- nine scalars: 34
- dim `y`: 1+1+8+8 = 18; dim `x`: 18 → 36
- chan `m`, type 1 (bool, element size 1): 1+1 + 2 + 1+1 = 6
- chan `v`, type 13 (float64, element size 8): 1+1 + 2 + 1+8 = 13 → 19
- trailing: 1 + 8 + 4 = 13

5 + 34 + 36 + 19 + 13 = **107**. (Same formula on §7.4's `sst` example returns 81,
the value the document states — the arithmetic is calibrated.)

inline_length is a `u32` at header offset 4 (§7.2), little-endian (`[R-ENC-01]`):
107 = 0x6B → **`6b 00 00 00`**.

## Q02 — planar geometry, entry_count, extent_length, disk ordinal, entry offset

G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3 (§11.2). N = ∏G = 9. C = 3, layout planar.

(a) `[R-GEO-03]`: addressed-tile count is "N for an interleaved layer and C · N for a
planar layer". entry_count = 3 × 9 = **27** (`[R-CNT-17]`).

(b) `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4
= 27×20 + 1×4 = 540 + 4 = **544**.

(c) (y,x) = (7,3): t = (7 div 4, 3 div 4) = (1, 0). Under linearization 1,
s = Σ tᵢ·∏_{j>i} Gⱼ = 1·3 + 0 = 3. Channel `c` has index 2. Planar disk ordinal
= c·N + s = 2·9 + 3 = **21** (`[R-GEO-06]`).

(d) §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
byte 20·k". 20 × 21 = **420**.

## Q03 — trailer CRC bytes at [124, 128)

Trailer [0,60) assembled per §6.2's layout, little-endian:

```
8a 4e 52 41 54 0d 0a 1a  01 00  03 00  00 00 00 00
10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
80 00 00 00 00 00 00 00  08 07 f6 e5 d4 c3 b2 a1
00 00 00 00 00 00 00 00  00 00 00 00
```

CRC-32C over those 60 bytes = 0x2FAF8508, "stored as a little-endian `u32`"
(`[R-ENC-09]`) → **`08 85 af 2f`**.

## Q04 — smallest new committed_file_length

Layer record inline payload: name `L` 2 + scalars 34 + one dim entry 18 + one bool
channel entry 6 + trailing 13 = 73. Record = 24-byte header + 73 = 97 bytes.
Directory region = record sequence (97) + terminal CRC-32C (4) = 101 (§7.1).

Geometry check: E=0, T=1 → G = 0, N = 0, interleaved addressed-tile count 0, so
entry_count 0, extent slot (0,0), crc_of_crc_array 0 — all consistent (`[R-GEO-02]`,
`[R-CNT-17]`, `[R-CNT-23]`).

`[R-LIF-02]` step 1: "begin writing at exactly F"; `[R-LIF-01]` freezes [0,128). So
dir_offset ≥ 128; take 128. Directory ends at 229. `[R-CNT-06]`: dir_offset +
dir_length ≤ F − 64 → F ≥ 293; F multiple of 64 → F ≥ 320. `[R-LIF-02]`'s "at least
128" above the prior F gives only F ≥ 256, so the directory bound binds.

At F = 320: trailer [256, 320), pre-trailer pad [229, 256) — exactly step 5's "pad to
the next 64-byte boundary". **320**.

## Q05 — verifier verdicts on a major-3 file

The verifier implements major 1 only. `[R-CNF-13]` and §21.2: the rows that reach a
file declaring another major are exactly "F8, F14, F6 and both of F1's instances …
and no other row."

File A: F1, F6, F8, F14 are all satisfied (constant front block, exact magic, matching
CRC). dir_offset = 8 would be F9, which does **not** reach — so no violation is
established. §2.3 makes *cannot establish* the verdict "where some requirement is one
it is unable to check on a capability … ground, as when the file names a format major
version it does not implement", and it "is available only to a traversal that
established no violation." → **cannot establish**.

File B: F14 reaches. `[R-CNF-13]`: "A verifier that establishes such a failure reports
*nonconforming*, whatever major the file declares and whether or not it implements
that major." → **nonconforming**.

## Q06 — zstd metadata frame with a wrong Frame_Content_Size

§18.2: "The frame's content-size field … MAY be present, and when present it MUST
equal the byte length of the decoded document. A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3." Declared 200, decoded 199
→ R4, instance "the content-size field declared larger than the decoded length,
top-level extent."

(a) §21.5's outcome for every row there is **ignore-record**. (b) **R4**.
(c) §21.5: "Every row here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming (`[R-CNF-12]`)." → **no**.

## Q07 — ignore-lane flag bits

0x00050000 = bits 16 and 18, both in the ignore lane (16–31); no incompat bit.

(a) `[R-CNT-08]`: "A compactor, though its output is a new file, carries the input's
unknown ignore-lane bits into its output trailer rather than writing flags = 0, and
sets no other." Output flags = 0x00050000, `u32` LE at trailer offset 12 →
**`00 00 05 00`**.

(b) `[R-CNT-08]`: "a writer creating a file under this text MUST write flags = 0" →
**`00 00 00 00`**.

(c) `[R-CNT-08]`: an updater "MUST copy forward … MUST NOT clear them, and MUST NOT set
any other: no writer under this text originates an ignore-lane bit" → **no**.

## Q08 — how many of four commits §20.3 bars

Two bars: the **§14 bar** (no change altering what §14 fixes for a tile stored in the
superseded generation) and the **planar-ordinal bar**.

(i) Planar (a,b,c), only `a` stored, remove `c` (last). §20.3: "Appending a channel, or
removing the last, re-indexes nothing and moves no ordinal at all." `a` keeps index 0,
its plane's decoded size P·Bᵃ, type, codec and filter all unchanged. **Not barred.**

(ii) Planar (a,b,c), only `c` stored, remove `a` (first). "inserting or removing one
moves every channel after the affected position… Either is such a change wherever the
layer stores a tile for a channel that moved." `c` moved and is stored. **Barred.**

(iii) Interleaved (u uint8, v uint16), a tile stored, remove `v`. §20.3: "removing one
of its channels changes Q and so is the §14 bar's subject wherever the layer stores a
tile." Q 3 → 1, decoded size P·Q changes. **Barred.**

(iv) Planar, one bool channel, a tile stored, filter 1 → 2. §17.3: "for a packed
boolean plane s = 1 and the filter is the identity." §20.3's carve-out: "a filter whose
mandated stride makes it the identity (`[R-COD-10]`) … is not what this bars."
**Not barred.**

Count = **2**.

## Q09 — records an updater may drop

§20.4's table, with the authority-of-flags rule above it.

1. 0x8001 (experimental, unimplemented) → stored flags authoritative; MU=0, PE=0 →
   "Retain byte-identical, or drop it… an updater MAY drop the record in any commit it
   is otherwise free to make — one whose only effect is the drop included." Droppable.
2. 0x0002 → registered; "the registry's fixed flags govern rather than the stored ones…
   both registered types carry PE = 1, so neither can be dropped." Also: "No commit
   therefore removes a layer record, or a user-metadata record at either scope." Not.
3. 0x0001 → registered, PE = 1. Not.
4. 0x8002 (unimplemented), MU=0/PE=1 → "Retain byte-identical, extent content
   unmodified." Not.

**1**.

## Q10 — slack after an L18 rejection of layer B

§9.7 claims the front block and the live trailer as walk members. `[R-CNT-21]`: "where
the rejection is one the walk itself established, L18's overlap … among them, the
claimants it had already enumerated are discarded with the layer", and "A partial total
is F less the bytes claimed by the claimants the walk did enumerate."

Enumerated: front block 16 + directory 100 + user-metadata extent 64 + layer A index
200 + layer A tiles 500 + 300 + trailer 64 = 1244. Layer B contributes nothing.

8192 − 1244 = **6948**, reported as **partial**.

## Q11 — interleaved decoded size and value offset

P = ∏T = 3·4 = 12. Q = ΣB = 1 (uint8) + 8 (float64) + 2 (int16) = 11.
(a) §14.2, interleaved decoded size P·Q = **132**.
(b) (26,13): u_y = 26 mod 3 = 2, u_x = 13 mod 4 = 1; in-tile ordinal u = 2·4 + 1 = 9.
§14.2's closing note: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ".
Fʳ = 1 + 8 = 9. 9·11 + 9 = **108**.

## Q12 — packed planar bool tile image

G = ⌈10/13⌉ = 1, P = ∏T = 13. §14.3: decoded size ⌈13/8⌉ = 2 bytes, LSB-first,
value k at bit k mod 8 of byte k div 8.

Ordinals 10–12 are padding positions (coordinate ≥ E = 10, §11.3); `[R-SER-05]`
requires the fill bit there. P mod 8 = 5, so bits 5–7 of byte 1 are pad bits, which
`[R-SER-05]` likewise fixes to the fill bit. Fill = 0x01 = true → bit 1.

Byte 0 (values 0–7 = T,F,T,T,F,F,F,T) = 1+4+8+128 = 0x8D.
Byte 1: bit0 = v8 = false; bit1 = v9 = true (2); bits 2–4 = padding = 1 (4+8+16);
bits 5–7 = pad bits = 1 (32+64+128) → 254 = 0xFE.

**`8d fe`**.

## Q13 — a nonconforming interleaved bool byte

P = 4, Q = 4 + 1 = 5, decoded size 20. Ordinal 2 → in-tile coords (1,0), inside extents
(2,2), so a real position, not padding (T2, not T4). `m`'s byte at 2·5 + 4 = 14.

(a) `[R-SER-08]`: "A reader that does not reject the tile and returns the value …
MUST report 0x00 as false and every other byte as true." → **true**.
(b) `[R-SER-08]`: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an
interleaved bool value. Any other byte makes the file nonconforming." → **no**.
(c) "its assigned detector is the verifier"; §21.4's T2 Detector cell is *verifier*
→ **conforming verifier**.

## Q14 — two layer records with empty name fields

Both name fields are the single byte 0x00, hence byte-identical, and both lie within
inline_length. §19.1 step 4: "two layers whose name fields are byte-identical are a
duplicate even when neither name is valid", and "Uniqueness is decided first".
F4 is reader-detected at open with outcome reject-file (`[R-ENC-15]`); L5's empty-name
reject-layer is the narrower condition but uniqueness is decided first and reject-file
governs the file.

(a) **reject-file**. (b) §19.2's tier list, as §21.1 names them — "open, layer access,
tile use, extent use" — → **open**.

## Q15 — an empty layer declaring lz4 with a 2 GiB derived tile size

G_y = ⌈0/16384⌉ = 0, G_x = ⌈1000000/16384⌉ = 62, N = 0. entry_count 0, extent (0,0),
crc_of_crc_array 0 — all consistent. P = 16384² = 268,435,456; Q = 8; P·Q =
2,147,483,648 = 0x80000000.

(a) `[R-COD-07]`'s Note: "The cap is quantified over the layer's *addressed* tiles, so
a layer that addresses none — any dimension extent 0 — satisfies it whatever its tile
shape declares, and codec 4 is conforming there." `[R-ENC-04]` is checked in an empty
layer, but P·Q = 2.1×10⁹ ≪ 2⁶³ − 1, and N, N·P and the index-length expression are 0.
Every value set and the geometry floor pass. → **no**.

(b) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed** tiles… A
layer addressing no tile therefore has no tile whose decoded size the table bounds…
a file containing no instance of a kind does not exceed that row, whatever its
declarations would derive." rank 2 ≤ 32, C 1 ≤ 4096, entry_count 0 ≤ 2³², 1 layer ≤
65,536, dir_length 200 ≤ 16 MiB, no metadata document, no zstd frame. The file is
conforming and no value exceeds a guarantee, so `[R-CNF-03]`'s acceptance duty runs.
→ **yes**.
