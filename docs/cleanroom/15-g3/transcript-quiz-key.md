# Round 15 — quiz key transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(four `Read` calls covering lines 1–4228, the whole document). I read no ADR, no
`docs/`, no `PLAN.md`, no `conformance/`, no `spec/registry.json`, no git history, no web
resource, and I did not list any directory. I ran two local Python programs that read no
files: one CRC-32C implementation (validated against §4.5's check vector
`CRC-32C("123456789") = 0xE3069283`, `CRC-32C(<empty>) = 0x00000000`, Appendix B's
all-sentinel-segment constant `0xEECB3BB2`, and §7.4's worked example
`0x80A34955` / `0xC4EE982E`), and one arithmetic script. I wrote this transcript and two
scratch scripts under my own scratchpad, and did not read the output directory.

---

## Q01 — minimal one-layer file: committed_file_length and dir_length

Layer record inline payload, §7.4 field order, packed with no padding
("fields are packed in table order with no alignment or padding between them", `[R-CNT-18]`):

| field | bytes |
|---|---|
| name `z` (u8 len + 1) | 2 |
| layout | 1 |
| linearization (u16) | 2 |
| codec (u16) | 2 |
| filter (u16) | 2 |
| alignment A (u64) | 8 |
| slab S (u64) | 8 |
| slab alignment (u64) | 8 |
| rank d (u8) | 1 |
| channel count C (u16) | 2 |
| dimension `t`: name(1+1) + extent u64 + tile extent u64 | 18 |
| channel `v`: name(1+1) + type u16 + fill(1 len + 1 byte, uint8 element size 1) | 6 |
| index_encoding (u8) | 1 |
| entry_count (u64) | 8 |
| crc_of_crc_array (u32) | 4 |
| **total inline_length** | **73** |

Cross-check against §7.4's own worked example, which is byte-identical in structure but
with a 3-byte name and a float32 channel: 81 = 4 + 34 + 18 + 12 + 13. Mine is
2 + 34 + 18 + 6 + 13 = 73. ✔

Extent 0 on dimension `t`: G = ⌈0/1⌉ = 0, N = 0, so the addressed-tile count is 0
(`[R-GEO-02]`, `[R-GEO-03]`). Hence entry_count = 0, and §7.4: "a layer with zero
addressed tiles has extent (0, 0)"; `[R-CNT-17]`'s formula gives extent_length 0, and
`[R-CNT-23]` forces crc_of_crc_array = 0. **There is no tile-index region in this file.**

Record = 24-byte header (§7.2) + 73 = 97 bytes. Directory region = record sequence + its
terminal CRC-32C (§7.1): dir_length = 97 + 4 = **101**.

Smallest permitted dir_offset = 16 (`[R-CNT-06]`: "dir_offset ≥ 16"). Directory occupies
[16, 117).

Shortest file: `[R-CNT-06]` requires dir_offset + dir_length ≤ F − 64 and F a multiple of
64. 117 ≤ F − 64 ⇒ F ≥ 181 ⇒ F = 192. Trailer at [128, 192); pre-trailer pad [117, 128) =
11 bytes — exactly `[R-LIF-02]` step 5's pad to the next 64-byte boundary. F = 192 ≥ 128
(`[R-CNT-27]`). ✔

**(a) 192, (b) 101.**

---

## Q02 — segment CRC array and crc_of_crc_array bytes

entry_count = 3 ⇒ ⌈3/2¹⁶⌉ = 1 segment, a 4-byte segment CRC array (§15.1). Segment 0
covers entries [0, 3) — all 60 entry bytes (§15.4). Entry bytes as stored:

```
entry 0  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 00 00 00 00   (sentinel, §15.2)
entry 1  00 10 00 00 00 00 00 00  18 00 00 00 00 00 00 00  44 33 22 11
entry 2  ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff 00 00 00 00
```

CRC-32C over those 60 bytes = 0x5DAE66CD, stored little-endian (`[R-ENC-09]`) as
`cd 66 ae 5d`.

crc_of_crc_array = CRC-32C over the 4-byte array `cd 66 ae 5d` = 0x884CB519, stored
`19 b5 4c 88`.

Note: the all-sentinel constant `0xEECB3BB2` does not apply — it is only for a **full**
2¹⁶-entry segment, and "a partial segment's CRC MUST be computed" (`[R-IDX-05]`).

**(a) `cd66ae5d`, (b) `19b54c88`.**

---

## Q03 — planar bool tile bytes

G_y = ⌈3/3⌉ = 1, G_x = ⌈2/3⌉ = 1, N = 1, C = 1 planar ⇒ 1 addressed tile.
P = 3 × 3 = 9. Planar bool ⇒ packed plane, ⌈9/8⌉ = 2 bytes (`[R-SER-03]`).

In-tile ordinal = u_y·T_x + u_x = 3u_y + u_x (§11.4). x ≥ 2 is a padding position
(§11.3), whose content is the channel's fill bit `0` (`[R-SER-05]`).

| ordinal | (u_y,u_x) | value |
|---|---|---|
| 0 | (0,0) | true → 1 |
| 1 | (0,1) | false → 0 |
| 2 | (0,2) | pad → fill 0 |
| 3 | (1,0) | false → 0 |
| 4 | (1,1) | true → 1 |
| 5 | (1,2) | pad → 0 |
| 6 | (2,0) | true → 1 |
| 7 | (2,1) | false → 0 |
| 8 | (2,2) | pad → 0 |

Byte 0 (bit k mod 8 of byte k div 8, LSB-first): bits 0,4,6 set ⇒ 0x51.
Byte 1: ordinal 8 → bit 0 = 0; P mod 8 = 1, so bits 1–7 are pad bits carrying the fill
bit 0 (`[R-SER-05]`) ⇒ 0x00.

Codec 1 and filter 1 leave the image verbatim (`[R-COD-04]`, `[R-COD-09]`).

**`5100`.**

---

## Q04 — interleaved decoded size and channel offset

P = 3 × 5 = 15. Element sizes (§12.1): `a` uint8 = 1, `b` float64 = 8, `c` bfloat16 = 2.
Sample stride Q = 11. Decoded size = P·Q = 15 × 11 = **165** (`[R-SER-02]`).

In-tile ordinal of (2,3) = 2·5 + 3 = 13. F_c = 1 + 8 = 9.
Offset = u·Q + F_c = 13·11 + 9 = 143 + 9 = **152** (§14.2's closing example gives exactly
this form: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ").

**(a) 165, (b) 152.**

---

## Q05 — tile-index entry offset

G = (⌈5/2⌉, ⌈9/4⌉, ⌈20/8⌉) = (3, 3, 3), N = 27.
Tile coordinates: (3 div 2, 7 div 4, 17 div 8) = (1, 1, 2).
s = Σ tᵢ·∏_{j>i} Gⱼ = 1·9 + 1·3 + 2 = 14 (`[R-GEO-06]`).
Channel `r` has index 2 ⇒ disk ordinal = c·N + s = 2·27 + 14 = 68.
Entry at region byte 20·k (`[R-IDX-01]`) = 20 × 68 = **1360**.

---

## Q06 — extent_length and last segment's coverage

(a) `[R-CNT-17]`: entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 65 537 × 20 + 2 × 4 = 1 310 740 + 8 = **1 310 748**.

(b) §15.4: segment s covers [s·2¹⁶, min((s+1)·2¹⁶, entry_count)). Segment 1 covers
[65 536, 65 537) ⇒ **1** entry.

---

## Q07 — slack total for a completed walk

Claimants (§9.7, `[R-CNT-02]`):

| claimant | bytes |
|---|---|
| front signature block [0,16) | 16 |
| live directory [640,736) | 96 |
| user-metadata record extent (448,40) | 40 |
| layer's tile-index region = layer record's extent, 5×20 + 4 | 104 |
| three stored-tile extents, 200 + 100 + 64 | 364 |
| live trailer [960,1024) | 64 |
| **total** | **684** |

The tile-index region enters once, as the layer record's extent, and is not a second
claimant (§9.7). Records themselves are not claimants — their bytes lie inside the
directory region (§9.7).

Slack = F − 684 = 1024 − 684 = **340**. (Gap check: [216,256)=40, [356,384)=28,
[488,512)=24, [616,640)=24, [736,960)=224 → 340. ✔)

---

## Q08 — slack figure after a layer-scope overlap the walk established

`[R-CNT-21]`: "where the rejection is one the walk itself established, L18's overlap or
L40 through L42's placement among them, the claimants it had already enumerated are
discarded with the layer". The overlap is L18 at layer A's scope, so **all** of layer A's
claimants — its tile-index region and both stored-tile extents — are discarded.

Enumerated claimants that survive: front block 16 + directory 128 + layer B index 24 +
layer B tile 200 + trailer 64 = 432.

"A partial total is F less the bytes claimed by the claimants the walk did enumerate."
2048 − 432 = **1616**.

The verifier did not elect to stop at the first violation, but the walk still failed to
enumerate every region's claimants, so the total is reported as **partial** (and the
verifier must say which scope stopped it — layer A).

**(a) 1616, (b) partial.**

---

## Q09 — slab packing offset, and the outcome/row for a gap

G = ⌈128/32⌉ = 4, N = 4, interleaved ⇒ 4 addressed tiles ✔. P = 32, Q = 1, decoded size
32 — consistent with codec 1's length equality (`[R-COD-04]`).

`[R-SLB-02]`: interleaved ⇒ a single block [0, 4); run 0 = ordinals [0, 4).
`[R-SLB-03]`: "each stored tile's offset equals the previous stored tile's offset plus its
length", and "Sentinel tiles are transparent to run continuity".

Entry 1 is a valid sentinel; entry 3 is a valid sentinel. So the run's stored tiles are
entries 0 and 2, in ordinal order. First stored tile at 4096; 4096 mod 64 = 0 ✔.
X = 4096 + 32 = **4128**.

(b) X = 4160 leaves a 32-byte gap ⇒ the packing relation fails. §15.3's row "alignment or
slab invariant violated (§16) | *verifier*: reject-layer"; §2.4 names that outcome class
**reject-layer**. The register row is **L41** ("Inside a slab run, a stored tile's offset
≠ the previous stored tile's offset plus that tile's length (gap, overlap, or
out-of-ordinal placement…)"), instance *gap*. Not L42 — the run's first stored tile is
still A_slab-aligned.

**(a) 4128, (b) reject-layer, L41.**

---

## Q10 — compactor meeting one bad tile CRC

`[R-WRT-09]`: a compactor "MUST verify each link of the chain — the open (§19.1), each
retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and each relocated
extent's checksum, **including every stored tile's entry crc** — before emitting that
structure's bytes."

`[R-WRT-06]`: "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges
fails, and MUST NOT emit a file carrying a violation it has detected: it can neither drop
the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected (`[R-WRT-05]`)."

(ii) is barred (§20.4: no commit removes a layer record; §20.5: compaction "carries every
layer of its input forward"). (iii) is barred (`[R-WRT-07]`: entry crcs unchanged;
`[R-CNF-04]`: no heuristic repair). (i) is barred by the sentence above.

**(iv).**

---

## Q11 — compactor and a slab-declared layer

(a) `[R-WRT-06]`: "Given a conforming input the output is a conforming file"; a compactor
"satisfies every writer requirement for the bytes it produces (`[R-CNF-06]`)". With S = 8
and A_slab = 4096 still declared, `[R-SLB-03]`'s contiguity and first-tile alignment
invariants bind the output. Placement freedom (`[R-SLB-05]`) is expressly the freedom of a
layer "that declares neither alignment nor a slab". ⇒ **no**.

(b) `[R-WRT-05]` requires byte-identical re-emission of header, inline payload and extent
slot for every retained record; `[R-WRT-07]` enumerates the *only* exceptions —
"relocation re-points extent slots, regenerates each relocated tile-index region …, and
updates the layer-record fields covering a regenerated region (crc_of_crc_array)". The
slab declaration is in the inline payload and is not among them; a compactor "preserves
content but not placement". ⇒ **no**.

Competing reading considered and rejected: `[R-SLB-04]` offers "re-establish … or clear
the declaration in the new generation", which if read to cover compaction would license
(b) = yes. But that rule binds a writer or updater "whose **commit** changes …", and
compaction is not a commit (`[R-LIF-01]` distinguishes the two); and the specific
enumeration in `[R-WRT-07]` governs what a compactor may alter in a retained record.

**(a) no, (b) no.**

---

## Q12 — Appendix G directory offset

Appendix G item 3: first structure at 16; then, per layer in ascending layer-name byte
order (`a` = 0x61 before `b` = 0x62), its stored tiles in disk-ordinal order, then its
tile-index region; then record extents, all after every layer's tiles and index regions;
then the directory. No declared A or A_slab ⇒ no alignment gaps before the pre-trailer
pad, and "each later structure begins where the previous one ended".

Index-region sizes by `[R-CNT-17]`: layer `a` 2×20 + 4 = 44; layer `b` 1×20 + 4 = 24.

```
a tile 0   [16,  46)   30
a tile 1   [46,  86)   40
a index    [86, 130)   44
b tile     [130,180)   50
b index    [180,204)   24
UM extent  [204,264)   60
directory  begins at 264
```

**264.**

---

## Q13 — unknown MU = 1 sub-record

Type 0x9000 ≥ 0x8000 ⇒ experimental range (§10.2).

(a) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never
reject-file". §2.4 names the class **reject-layer**.

(b) The file is conforming — §21.6: "an **experimental-range record type carrying MU = 1**
… `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file conforming
all the same". But §2.3 lists as a *cannot establish* ground "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and "*cannot establish* is
available only to a traversal that established no violation" — which is this traversal.

**(a) reject-layer, (b) cannot establish.**

---

## Q14 — encoding 0x85 versus 0x05

File A, encoding 0x85 ≥ 0x80 ⇒ experimental. §21.6: "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); **the file is
conforming** … No document rule attaches at such an encoding, so a verifier certifies,
reporting the record it ignored". `[R-MTA-10]`: "A verifier meeting such a record in an
otherwise conforming file has no requirement it is unable to check … and certification is
unaffected". ⇒ **conforming**.

File B, encoding 0x05 ⇒ reserved range 3–0x7F. §21.5 row **R1**: "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)" — and "Every row
here is a violation all the same: the outcome bounds a reader's blast radius and never
makes the file conforming". An established violation ⇒ **nonconforming** (§2.3: "a
verifier that has established any violation reports *nonconforming*").

**A = conforming, B = nonconforming.**

---

## Q15 — filter 1 → 2 on a fully-stored planar uint8 layer

§20.3 step 4 bars a declaration change that alters, for a tile stored in the superseded
generation, "the codec and **filter** that produced the stored bytes". But the same step
states the test and its carve-out: "The test is the effect on such a tile, and the list
names where that effect arises rather than standing on its own: a change that leaves every
one of those tiles' stored bytes meaning exactly what they meant — **a filter whose
mandated stride makes it the identity (`[R-COD-10]`)** … — is not what this bars."

`[R-COD-10]`: "The shuffle stride s is the channel's element size for a planar tile."
Layer L is planar with one uint8 channel ⇒ s = 1 ⇒ n = L/1 = L, and byte i of group j goes
to i·n + j with i = 0 always ⇒ offset j. The filter is the identity; every stored tile's
bytes mean exactly what they meant, decoded size (P·Bᶜ = 256·1 = 256) is unchanged, sample
offsets unchanged, padding positions unchanged (extents 64×64 with tile extents 16×16 give
G = (4,4), N = 16, no padding positions at all).

The commit is §20.3's shape (c), a change confined to the directory; L keeps its extent
slot (`[R-WRT-05]`), and the index region is not re-emitted.

**permitted.**
