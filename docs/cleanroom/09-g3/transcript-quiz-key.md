# Round 9 — quiz key transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3892 lines, in five sequential `Read` calls plus one `wc`). I read no ADR, no
`docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`/`AGENTS.md`/`README`,
no git history, no web. I ran one local Python script I wrote myself
(`scratchpad/round9/calc.py`) that reads no files: it implements CRC-32C
(reflected poly 0x82F63B78, init/final 0xFFFFFFFF) and computes the Q01 trailer CRC
and the Q05 crc_of_crc_array. The implementation is validated against three
constants the document itself states: CRC-32C("123456789") = 0xE3069283 (§4.5),
CRC-32C of zero bytes = 0x00000000 (§4.5), Appendix A's trailer CRC 0xE00938D2 for
its 60 trailer bytes, and the all-sentinel full-segment constant 0xEECB3BB2 (§15.4,
recomputed from 65,536 sentinel entries). All four reproduce exactly.

---

## Q01 — final four bytes of a 128-byte zero-layer file

The final four bytes are the trailer CRC field at trailer offset [60, 64):
"CRC-32C over trailer bytes [0, 60)" (§6.2 layout table, `[R-CNT-06]`).

Trailer bytes [0, 60) assembled from §6.2's layout table with the stated fields:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
01 00 00 00 00 00 00 00   generation = 1
10 00 00 00 00 00 00 00   dir_offset = 16
04 00 00 00 00 00 00 00   dir_length = 4
80 00 00 00 00 00 00 00   committed_file_length = 128
01 00 00 00 00 00 00 00   file_id = 1
00 00 00 00               reserved
```

CRC-32C = **0xEC73541B**. Stored "as a little-endian `u32`" (`[R-ENC-09]`), so the
bytes in file order are `1b 54 73 ec`.

Sanity: substituting Appendix A's file_id 0x0123456789ABCDEF into the identical
60 bytes yields 0xE00938D2, exactly the value Appendix A records — the only
difference between that file and this one is the file_id field.

**Answer: `1b5473ec`.** (The CRC *value* is 0xec73541b; the question asked for
file order.)

---

## Q02 — decoded tile image, planar bool, tile (1,1)

Planar + bool ⇒ §14.3 packed plane, not §14.2 bytes: "In a planar tile of a bool
channel the decoded tile image is the tile's P values bit-packed LSB-first: value k
occupies bit k mod 8 of byte k div 8 (§4.4), with 0 = false and 1 = true, and the
decoded size is ⌈P/8⌉ bytes." `[R-SER-03]`

Geometry: T = (3,3), P = ∏Tᵢ = 9 (§11.2). ⌈9/8⌉ = 2 bytes.
Grid: Gᵢ = ⌈5/3⌉ = 2 each, so tile coords (1,1) exists.
Tile (1,1) covers y ∈ [3,6), x ∈ [3,6). Extents are 5, so y,x = 5 is padding.

In-tile ordinal = Σᵢ uᵢ·∏_{j>i}Tⱼ = u_y·3 + u_x (`[R-GEO-06]`), u = (y−3, x−3):

| ord | (y,x) | status | value |
|---|---|---|---|
| 0 | (3,3) | real | true = 1 |
| 1 | (3,4) | real | false = 0 |
| 2 | (3,5) | padding | fill = 1 |
| 3 | (4,3) | real | false = 0 |
| 4 | (4,4) | real | true = 1 |
| 5 | (4,5) | padding | fill = 1 |
| 6 | (5,3) | padding | fill = 1 |
| 7 | (5,4) | padding | fill = 1 |
| 8 | (5,5) | padding | fill = 1 |

Padding content is fixed: "at every padding position, a writer MUST encode, for each
channel the position carries, that channel's fill value — … the fill bit in a packed
plane. Every pad bit (§14.3) MUST carry the plane's channel's fill bit."
`[R-SER-05]`. Fill byte 0x01 ⇒ fill bit 1.

Byte 0 = bits 0–7 = ords 0–7 = 1,0,1,0,1,1,1,1
 = 0x01+0x04+0x10+0x20+0x40+0x80 = **0xF5**.
Byte 1 = bit 0 = ord 8 = 1; bits 1–7 are pad bits (P mod 8 = 1), each the fill bit 1
 ⇒ 0xFF. (Cf. §14.3's worked example: P = 10, fill true ⇒ `55 FD`.)

**Answer: `f5 ff`.**

---

## Q03 — filtered image, interleaved, filter 2

"The shuffle stride s is the channel's element size for a planar tile and the sample
stride Q for an interleaved tile (§14.2)… Viewing the image as n = L/s consecutive
groups of s bytes, the filtered image places byte i of group j at offset i·n + j"
`[R-COD-10]`.

Q = ΣBᵢ = 4 (float32) + 1 (bool) = 5 (`[R-SER-02]`). L = P·Q = 2·5 = 10. s = 5,
n = L/s = 2. Groups: g0 = `00 01 02 03 01`, g1 = `10 11 12 13 00`.

offset i·2 + j: 0←g0[0], 1←g1[0], 2←g0[1], 3←g1[1], 4←g0[2], 5←g1[2],
6←g0[3], 7←g1[3], 8←g0[4], 9←g1[4].

Verified my transform against §17.3's own example (three float32, s=4, n=3):
`00 00 80 3F 00 00 00 40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`,
which reproduces the document's example byte for byte.

**Answer: `00 10 01 11 02 12 03 13 01 00`.**

---

## Q04 — top-level user-metadata record header + inline payload

§7.2 header layout; §7.3 fixes the flags for registered types
("writers MUST emit exactly the flag values fixed in the table above", `[R-CNT-22]`):
type 0x0002 = user metadata, MU = 0, PE = 1. Bit 0 = MU, bit 1 = PE (`[R-ENC-08]`)
⇒ flags = 0x0002. Reserved bits 2–15 zero.

inline_length: "A user-metadata record's inline payload is exactly one byte"
(`[R-MTA-03]`) ⇒ 1. Payload = encoding = 2 (zstd).
extent_offset = 4096 = 0x1000; extent_length = 1200 = 0x4B0. All little-endian.

```
02 00                     type 0x0002
02 00                     flags = 0x0002 (MU=0, PE=1)
01 00 00 00               inline_length = 1
00 10 00 00 00 00 00 00   extent_offset = 4096
b0 04 00 00 00 00 00 00   extent_length = 1200
02                        encoding = 2 (zstd)
```
24 + 1 = 25 bytes.

**Answer: `02 00 02 00 01 00 00 00 00 10 00 00 00 00 00 00 b0 04 00 00 00 00 00 00 02`.**

---

## Q05 — index region length and crc_of_crc_array for 131072 all-unstored entries

(a) "Under index_encoding 1, extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4" `[R-CNT-17]`.
131072 × 20 = 2,621,440; ⌈131072/65536⌉ = 2, × 4 = 8. Total **2,621,448**.

(b) 131072 = 2 × 2¹⁶ exactly, so both segments are *full* segments of 65,536
sentinels. "The CRC-32C of a segment consisting of 2¹⁶ sentinel entries is
`0xEECB3BB2`" `[R-IDX-05]` — I recomputed this from `FF ×16 00 ×4` repeated 65,536
times and got 0xEECB3BB2, confirming both the constant and my CRC engine.

The segment CRC array is two u32s, each stored little-endian: `b2 3b cb ee b2 3b cb ee`.
crc_of_crc_array is "CRC-32C over the index's segment-CRC array" (§7.4) — i.e. over
those 8 bytes as stored (`[R-CNT-19]`: "All checksums are CRC-32C over bytes exactly
as stored"). Result: **0xd7926b78** (stored in the layer record as `78 6b 92 d7`).

**Answer: (a) 2621448; (b) d7926b78.**

---

## Q06 — compactor output trailer bytes [8, 16)

[8,10) version_major = 1 ⇒ `01 00`.

[10,12) version_minor: "The output trailer … carries the greater of `[R-CNT-26]`'s
floor and the input's version_minor — a compactor cannot know which minor version
defined an ignore-lane bit it does not implement, so it does not lower the floor
beneath one." `[R-WRT-06]`. Floor for a file expressible under this text = 0
(`[R-CNT-26]`); input minor = 3; max = 3 ⇒ `03 00`.

[12,16) flags: "A compactor, though its output is a new file, carries the input's
unknown ignore-lane bits into its output trailer rather than writing flags = 0
(§20.5, `[R-WRT-06]`)" `[R-CNT-08]`. 0x00050000 = bits 16 and 18, both in the ignore
lane (bits 16–31), both unimplemented ⇒ carried forward ⇒ `00 00 05 00`.

Nuance noted, not marked underdetermined: `[R-CNT-26]` is a SHOULD and §21 registers
no row for a "wrong" version_minor, so a compactor that wrote a higher minor would
still emit a conforming file (§2.4: "Deviation from a SHOULD is not a violation").
But the document directs exactly one value, and that is what the question asks for.

**Answer: `01 00 03 00 00 00 05 00`.**

---

## Q07 — reproducible-writer profile, all-zero uint32 tile, index entry

Appendix G item 7: "**The all-zero fill default.** Where a caller chooses no fill,
the writer records all-zero bytes — `[R-TYP-10]`'s SHOULD, taken as a requirement
here." ⇒ fill = 0x00000000.

Appendix G item 6: "**The sentinel for every all-fill tile**, so that a tile whose
samples all equal fill is never stored". Every sample position of this tile, padding
included, is 0x00000000 = fill ⇒ the tile is unstored ⇒ sentinel entry.

§15.2: "offset and length both `0xFFFF_FFFF_FFFF_FFFF` and crc 0 — the 20 bytes
`FF ×16 00 ×4`." `[R-IDX-02]`.

**Answer: `ffffffffffffffffffffffffffffffff00000000`** (32 `f` + 8 `0` = 40 digits).

---

## Q08 — planar C=3 geometry, index arithmetic, and the mismatch row

Gᵢ = ⌈Eᵢ/Tᵢ⌉: G_y = ⌈1000/256⌉ = 4, G_x = ⌈2048/256⌉ = 8; N = ∏Gᵢ = 32 (`[R-GEO-03]`).
(This is §11.2's own worked example: "With extents (1000, 2048) instead,
G_y = ⌈1000/256⌉ = 4 still".)

(a) "its **addressed-tile count** … is N for an interleaved layer and C · N for a
planar layer" `[R-GEO-03]`; entry_count "equals the addressed-tile count" (§7.4).
3 × 32 = **96**.

(b) 96 × 20 + ⌈96/65536⌉ × 4 = 1920 + 4 = **1924** (`[R-CNT-17]`).

(c) t_y = 700 div 256 = 2; t_x = 300 div 256 = 1.
s = Σ tᵢ·∏_{j>i}Gⱼ = 2·8 + 1 = 17. Disk ordinal = c·N + s = 2·32 + 17 = 81
(`[R-GEO-06]`). "The entry for the tile with disk ordinal k … is the k-th entry, at
region byte 20·k" `[R-IDX-01]` ⇒ 20 × 81 = **1620**.

(d) Region = "[ entry array: entry_count × 20 bytes ] [ segment CRC array … ]
with no padding anywhere inside the region" (§15.1) ⇒ array starts at 96 × 20 =
**1920**.

(e) extent_length 1920 ≠ 1924 ⇒ L23: "Under index_encoding 1, extent_length ≠
entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4". §21.3 heading: "Outcome: reject-layer".

**Answer: 96; 1924; 1620; 1920; L23, reject-layer.**

---

## Q09 — verifier's slack total, partiality, verdict

Entry classification (§15.3, `[R-IDX-03]`):
- entry 0: offset 16, length 100, crc matches ⇒ valid stored tile, extent [16, 116).
- entry 1: offset 300, length 200, stored bytes fail crc ⇒ reject-tile, but "the
  entry itself is well-formed; its extent stands". §9.7: "one whose stored bytes
  alone fail its crc keeps its extent". Extent [300, 500) is claimed.
- entry 2: offset = S, length = 40 ≠ S ⇒ row "offset = S ∧ length ≠ S, or
  offset ≠ S ∧ length = S | *structural*: reject-tile". §9.7: "an entry
  `[R-IDX-03]` classifies reject-tile on a *structural* ground contributes no stored
  extent to the walk".

(a) Claimants (§9.7: front block, trailer, directory, records' extents, non-sentinel
index entries; "A layer record's extent slot addresses that layer's tile-index
region (§7.4), so the region enters the walk once"):

| region | bytes |
|---|---|
| front block [0,16) | 16 |
| tile 0 extent [16,116) | 100 |
| tile-index region [128,192) | 64 |
| tile 1 extent [300,500) | 200 |
| directory [700,900) | 200 |
| trailer [960,1024) | 64 |
| **total claimed** | **644** |

All disjoint; all non-front/non-trailer claimants lie in [16, F−64) = [16, 960).
Slack = 1024 − 644 = **380**.

(b) The walk completes: the verifier "does not elect to stop at the first violation",
no scope-level rejection blocks enumeration (both defects are tile-scope), and §9.7
says explicitly "An entry `[R-IDX-03]` classifies reject-tile on a *structural*
ground does not make the walk incomplete: the walk passes over it". ⇒ **complete**.

(c) Two established violations — T1 (stored bytes fail the entry crc) and T7 (exactly
one of offset/length set to the sentinel). §2.3: "An established violation takes
priority: a verifier that has established any violation reports *nonconforming*".
⇒ **nonconforming**.

**Answer: 380; complete; nonconforming.**

---

## Q10 — new committed_file_length after an appending commit

Commit order (`[R-LIF-02]`): (1) begin at exactly F = 4096; (2) new payloads and
tile-index regions; (3) directory + CRC; (4) barrier; (5) "append the pad to the next
64-byte boundary … and the new trailer".

- new stored tile payload: 100,000 ⇒ [4096, 104096)
- re-emitted index region: "entry_count entries plus the segment CRC array"
  (`[R-WRT-04]`) = 32 × 20 + ⌈32/65536⌉ × 4 = 644 ⇒ [104096, 104740)
  (§20.3's own example: "32 · 20 + 4 = 644 bytes — one entry re-pointed, 31
  byte-identical")
- directory: record sequence 700 + terminal CRC 4 = 704 ⇒ [104740, 105444)
- pad to next 64-boundary: 105444 = 64·1647 + 36 ⇒ pad 28 ⇒ ends 105472
- trailer 64 ⇒ [105472, 105536)

committed_file_length = 105536; 105536 = 64 × 1649, so F mod 64 = 0 as §6.2 requires.
(Step 2's internal order is free — "in any order satisfying §5.2's coverage classes" —
and does not change the total.)

**Answer: 105536.**

---

## Q11 — reserved-range vs experimental-range MU=1 record

0x0500 ∈ 0x0003–0x7FFF = the **reserved** range; 0x8123 ≥ 0x8000 = the
**experimental** range (§10.2 table).

(a),(b) "An unknown record type at file scope: MU = 1 → reject-file" `[R-CNT-15]`.
Applies to both, unchanged: "Readers of both apply the MU rule above unchanged."
⇒ **reject-file** for P and for Q.

(c) P: "one from the reserved range is a value this specification has not assigned —
emitting it is a violation" `[R-CNT-15]`; §21.6 confirms "a *reserved*-range type,
whose emission `[R-CNT-15]` does make a violation (F37, F38, L25, L26)". ⇒ **no**.

(d) Q: §21.6, "Two structural cases are **conforming files a reader nevertheless
refuses**… The second is an **experimental-range record type carrying MU = 1**
(§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the
file conforming all the same". ⇒ **yes**.

(e) P: the verifier is a reader and detects F37 at open — the reserved-range check is
a value-range test needing no implementation of the type — so it *establishes* a
violation. §2.3: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it was
unable to check, and *cannot establish* is available only to a traversal that
established no violation." ⇒ **nonconforming**.

(f) Q: no violation anywhere ("both files satisfy every other requirement"), and
§2.3 names this exact situation for the third verdict: "*cannot establish* — the last
where some requirement is one it is unable to check on a capability or resource
ground, as when … a record carries MUST_UNDERSTAND = 1 with a type it does not
implement (§21.6)". ⇒ **cannot establish**.

(g) §21.1: "Some rows are strict specializations of others — … F37 of F38 … — and a
file exhibiting a specialization is recorded against the narrower row". P's record is
reserved-range *with MU = 1* ⇒ **F37**.

---

## Q12 — two layer records with byte-identical ill-formed names

(a) §19.1 step 4: "Uniqueness is decided first, and over the raw name bytes whether
or not each name is itself well-formed — `[R-ENC-12]` makes name comparison a byte
comparison, which needs no valid name — so two layers whose name fields are
byte-identical are a duplicate even when neither name is valid." `[R-ENC-15]`: "a
duplicate layer name is a file-scope error (reject-file)". ⇒ **reject-file**.
(The ill-formed UTF-8 also raises L4 at layer scope, but the file-scope outcome is
what a reader applies to the file.)

(b) §19.2's four tiers are: at open; at first access to a layer; at use of a tile; at
use of a record's extent. The layer-name namespace is listed under "**at open:** …
and the layer-name namespace (§19.1's steps)". F6's *Detected* cell is likewise
"open". ⇒ **open**.

(c) F6: "Two layer records in the live directory carry byte-identical name fields,
both obtainable within their records' inline_length (comparison is raw bytes, no
normalization)" — matching the stipulation that each name lies inside its record's
inline_length. ⇒ **F6**.

---

## Q13 — rank 40, C 5000

(a) §21.9 states **minimum guarantees, not caps**: "A file exceeding any of these
remains conforming, and a reader MAY decline it" `[R-ERR-04]`. rank 40 > 32 and
C 5000 > 4096 exceed the guarantees but violate no hard limit (rank ≤ 255,
C ≤ 65,535, `[R-ERR-05]`). ⇒ **yes**.

(b) `[R-ERR-04]`: the reader MAY decline, "Either way, a refusal on resource grounds
MUST be reported as a resource limit and not as a validity error". `[R-CNF-03]`'s
acceptance duty runs only to a conforming file "none of whose values exceeds the
minimum guarantees of §21's limits table". ⇒ **yes**.

(c) `[R-ERR-05]`: "rank at most 255 and channel count at most 65,535 (§7.4's `u8` and
`u16` fields)"; Appendix B: "Rank d, channel count C | at most 255 and 65,535".
⇒ **255**.

---

## Q14 — zstd frame with a Window_Descriptor for a 900-byte tile

(a) `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size". §17.2's note: "with Single_Segment_Flag set there is no
Window_Descriptor and Window_Size is the frame content size … without it, the
Window_Descriptor cannot express less than 1 KiB. A tile whose decoded size is below
1 KiB … is therefore encodable under codec 3 only as a single-segment frame."
900 < 1024 ⇒ any Window_Descriptor declares ≥ 1 KiB > 900. ⇒ **no**.

(b) "a reader MUST treat either as a validity error at tile scope" ⇒ **reject-tile**.

(c) T21: "Codec 3 (zstd) and the frame declares a window size larger than the tile's
decoded size". ⇒ **T21**.

(d) "The frame content-size field MAY be present; when present it MUST equal the
tile's decoded size" ⇒ **900**.

---

## Q15 — an interleaved bool byte of 0x02

(a) `[R-SER-08]`: "A reader that neither detects the violation nor rejects the tile,
and returns the value, MUST report 0x00 as false and every other byte as true."
0x02 ≠ 0x00 ⇒ **true**.

(b) Same rule: "A reader is not obligated to screen decoded content, and a reader
that does not detect the violation is not thereby nonconforming". ⇒ **yes**.

(c) "Any other byte makes the file nonconforming: its assigned detector is the
verifier, for which it is a validity error at tile scope." ⇒ **verifier**.

(d) The sample position lies inside the layer's extents, i.e. a real (non-padding)
position ⇒ T2: "In an interleaved tile, a bool channel's single value byte at a real
(non-padding) sample position is neither 0x00 nor 0x01; the same byte at a padding
position is T4's". ⇒ **T2**.

---

## Underdetermined count

Zero questions came out underdetermined on this slate. The two places where I looked
hardest and still found the text decisive:

1. **Q06's version_minor.** `[R-CNT-26]` is a SHOULD and §21 registers no row for a
   misstated minor, so a compactor writing something other than 3 would still emit a
   *conforming file*. But `[R-WRT-06]` states declaratively what the output "carries",
   which is what the question asks, and it resolves to 3.
2. **Q09's slack total.** The wording "live committed state consists of" could be
   misread as excluding the stored-tile extents. §5.2 defines the live state to
   include "every structure reachable from the live trailer through the live
   directory's records, extent slots, and tile-index entries", so entry 0's and
   entry 1's extents are claimants; entry 2's are not, by §9.7's explicit parenthetical.
