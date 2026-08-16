# Cleanroom round 9 — quiz answerer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3892 lines, in five `Read` calls). I read nothing else — no ADRs, no
`docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`/`AGENTS.md`/
`README.md`, no git history, no web. I did not list directories.

I ran local Python (two scratch scripts I wrote myself, in the scratchpad,
reading no project files) to compute CRC-32C values and to check arithmetic.
My CRC-32C implementation was validated against three constants the document
itself publishes before I used it for anything:

- CRC-32C(`"123456789"`) = `0xE3069283` ✓ (§4.5 check vector)
- CRC-32C(zero bytes) = `0x00000000` ✓ (§4.5)
- Appendix A's trailer: my computation gives `0xE00938D2`, stored `D2 38 09 E0` ✓
- CRC-32C of 2¹⁶ sentinel entries = `0xEECB3BB2` ✓ (§15.4, Appendix B)

The last one is a strong independent check: it confirms both my CRC and my
reading of the 20-byte sentinel entry layout.

---

## Q01 — final four bytes of a 128-byte, zero-layer file

The final four bytes of any file are trailer bytes [60, 64): the trailer CRC,
"CRC-32C over trailer bytes [0, 60)" (§6.2 layout table, `[R-CNT-06]`,
`[R-CNT-24]`: "a CRC-32C at F − 4 covering bytes [F − 64, F − 4)").

Trailer bytes [0, 60), all little-endian (`[R-ENC-01]`):

```
8a 4e 52 41 54 0d 0a 1a   magic (§6.2)
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
01 00 00 00 00 00 00 00   generation = 1
10 00 00 00 00 00 00 00   dir_offset = 16
04 00 00 00 00 00 00 00   dir_length = 4
80 00 00 00 00 00 00 00   committed_file_length = 128
01 00 00 00 00 00 00 00   file_id = 0x0000000000000001
00 00 00 00               reserved
```

CRC-32C over those 60 bytes = **0xEC73541B**, stored little-endian as
`1b 54 73 ec`.

This is Appendix A's file with only file_id changed (0x0123456789ABCDEF → 1),
and my code reproduces Appendix A's `D2 38 09 E0` for the original, which
validates the layout byte-for-byte.

**Answer: `1b5473ec`** (file order).

## Q02 — planar bool tile image

Planar + bool ⇒ packed plane (§14.3, `[R-SER-03]`), not §14.2's byte-per-value.
G = (⌈5/3⌉, ⌈5/3⌉) = (2, 2); tile (1,1) is a legal tile coordinate.
P = ∏Tᵢ = 3·3 = 9. Decoded size = ⌈P/8⌉ = 2 bytes.

Tile (1,1) covers y ∈ [3,6), x ∈ [3,6). In-tile uᵢ = xᵢ mod 3. In-tile ordinal
= u_y·3 + u_x (§11.4, row-major, permanent for every linearization).

| ordinal | (u_y,u_x) | (y,x)  | status  | bit |
|---|---|---|---|---|
| 0 | (0,0) | (3,3) | true    | 1 |
| 1 | (0,1) | (3,4) | false   | 0 |
| 2 | (0,2) | (3,5) | padding | 1 (fill) |
| 3 | (1,0) | (4,3) | false   | 0 |
| 4 | (1,1) | (4,4) | true    | 1 |
| 5 | (1,2) | (4,5) | padding | 1 |
| 6 | (2,0) | (5,3) | padding | 1 |
| 7 | (2,1) | (5,4) | padding | 1 |
| 8 | (2,2) | (5,5) | padding | 1 |

`[R-SER-05]`: "at every padding position, a writer MUST encode … the fill bit
in a packed plane. Every pad bit (§14.3) MUST carry the plane's channel's fill
bit." Fill byte 0x01 = true (§13.2), so every padding position and every pad
bit is 1.

Byte 0 (bits 0–7 = ordinals 0–7, LSB-first): 1,0,1,0,1,1,1,1
 = 1+4+16+32+64+128 = 245 = 0xF5.
Byte 1: bit 0 = ordinal 8 = 1; P mod 8 = 1, so bits 1–7 are pad bits = 1 ⇒ 0xFF.

**Answer: `f5 ff`**

## Q03 — byte-shuffle of an interleaved tile

Interleaved, channels t(float32, B=4) then m(bool, B=1) ⇒ Q = ΣBᵢ = 5 (§14.2).
P = 2 ⇒ decoded size P·Q = 10 ✓ matches the 10 given bytes.

`[R-COD-10]`: "The shuffle stride s is … the sample stride Q for an interleaved
tile"; s = 5, L = 10, n = L/s = 2. "the filtered image places byte i of group j
at offset i · n + j".

Groups: g0 = `00 01 02 03 01`, g1 = `10 11 12 13 00`.

| out offset | i·n+j | source |
|---|---|---|
| 0 | i0 j0 | 00 |
| 1 | i0 j1 | 10 |
| 2 | i1 j0 | 01 |
| 3 | i1 j1 | 11 |
| 4 | i2 j0 | 02 |
| 5 | i2 j1 | 12 |
| 6 | i3 j0 | 03 |
| 7 | i3 j1 | 13 |
| 8 | i4 j0 | 01 |
| 9 | i4 j1 | 00 |

The writer's pipeline is filter then codec (§17.1, `[R-COD-01]`: "the filtered
image is the codec's input"), so this is exactly what is handed to the codec.

**Answer: `00 10 01 11 02 12 03 13 01 00`**

## Q04 — top-level user-metadata record, header + inline payload

§7.2 header, §7.3 registry row (type 0x0002 = user metadata, **MU = 0, PE = 1**,
and `[R-CNT-22]`: "writers MUST emit exactly the flag values fixed in the table
above"). Reserved flag bits 2–15 zero (`[R-CNT-12]`). flags = bit 1 only =
0x0002. `[R-MTA-03]`: "A user-metadata record's inline payload is exactly one
byte" ⇒ inline_length = 1; encoding 2 = zstd.

```
02 00                     type   = 0x0002
02 00                     flags  = PE=1, MU=0
01 00 00 00               inline_length = 1
00 10 00 00 00 00 00 00   extent_offset = 4096
b0 04 00 00 00 00 00 00   extent_length = 1200
02                        inline payload: encoding = 2 (zstd)
```

25 bytes. (extent_length 1200 ≥ 5, `[R-CNT-25]`; slot not (0,0).)

## Q05 — all-sentinel index of 131072 entries

(a) `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
 = 131072·20 + 2·4 = 2,621,440 + 8 = **2,621,448**.

(b) 131072 = 2·2¹⁶, so two **full** segments, both all-sentinel. §15.4: "The
CRC-32C of a segment consisting of 2¹⁶ sentinel entries is `0xEECB3BB2`" — I
recomputed it from `FF ×16 00 ×4` × 65536 and got 0xEECB3BB2 ✓. The segment CRC
array is those two u32s stored little-endian: `b2 3b cb ee b2 3b cb ee`.
crc_of_crc_array is "CRC-32C over the index's segment-CRC array" (§7.4, §8.1)
= **0xD7926B78** (stored bytes `78 6b 92 d7`).

The question asks for the *value*, so: `d7926b78`.

## Q06 — compactor output trailer bytes [8, 16)

Those 8 bytes are version_major (2), version_minor (2), flags (4).

- version_major = 1 → `01 00`.
- version_minor: `[R-WRT-06]` — the output "carries the greater of
  `[R-CNT-26]`'s floor and the input's version_minor — a compactor cannot know
  which minor version defined an ignore-lane bit it does not implement, so it
  does not lower the floor beneath one." Floor for a file expressible under
  this text = 0 (`[R-CNT-26]`); input minor = 3; max = 3 → `03 00`.
- flags: `[R-CNT-08]` — "A compactor, though its output is a new file, carries
  the input's unknown ignore-lane bits into its output trailer rather than
  writing flags = 0 (§20.5, `[R-WRT-06]`)." 0x00050000 = bits 16 and 18, both
  ignore lane, both unimplemented ⇒ carried verbatim → `00 00 05 00`.

**Answer: `01 00 03 00 00 00 05 00`**

(Note: `[R-CNT-26]` is itself a SHOULD, but `[R-WRT-06]` states the compactor's
minor rule declaratively inside a normative requirement, so 3 is what the
document says the output carries.)

## Q07 — reproducible-writer profile, all-zero tile

Appendix G item 7: "Where a caller chooses no fill, the writer records all-zero
bytes — `[R-TYP-10]`'s SHOULD, taken as a requirement here." uint32 fill =
`00 00 00 00`.

Appendix G item 6: "**The sentinel for every all-fill tile**, so that a tile
whose samples all equal fill is never stored." Every sample position the tile
carries, padding included, is 0x00000000 = fill ⇒ the tile is not stored ⇒ its
entry is the sentinel.

§15.2 / `[R-IDX-02]`: "offset and length both `0xFFFF_FFFF_FFFF_FFFF` and crc 0
— the 20 bytes `FF ×16 00 ×4`."

**Answer: `ffffffffffffffffffffffffffffffff00000000`** (32 f's + 8 zeros = 40 digits)

## Q08 — planar geometry arithmetic

G_y = ⌈1000/256⌉ = 4 (§11.2's own worked example gives exactly this), G_x =
⌈2048/256⌉ = 8, N = 32, C = 3.

(a) `[R-GEO-03]`: addressed-tile count = C·N for a planar layer = 3·32 = **96**.
(b) `[R-CNT-17]`: 96·20 + ⌈96/65536⌉·4 = 1920 + 4 = **1924**.
(c) t = (700 div 256, 300 div 256) = (2, 1); s = Σ tᵢ·∏_{j>i} Gⱼ = 2·8 + 1 = 17;
    disk ordinal = c·N + s = 2·32 + 17 = 81 (`[R-GEO-06]`); §15.1: "The entry
    for the tile with disk ordinal k … at region byte 20·k" = 20·81 = **1620**.
(d) §15.1's region layout: entry array (entry_count × 20) then the segment CRC
    array, "with no padding anywhere inside the region" ⇒ **1920**.
(e) 1920 ≠ 1924 ⇒ `[R-CNT-17]` mismatch ⇒ §21.3 row **L23**, outcome
    **reject-layer**. (Note 1920 is exactly (d) — the natural error of omitting
    the CRC array, which is what L23 registers.)

## Q09 — verifier walk, slack total, verdict

Index region check: entry_count 3 ⇒ 3·20 + 4 = 64 bytes; [128,192) is 64 ✓, so
no L23/L22 layer-scope rejection.

Entry classification (§15.3, `[R-IDX-03]`):
- entry 0: well-formed, crc matches — extent [16, 116) claimed.
- entry 1: "stored bytes fail the entry's crc | reject-tile (§8.2) — the entry
  itself is well-formed; its extent stands." So [300, 500) is claimed, and it
  "keeps its place in … the coverage walk."
- entry 2: offset = S, length ≠ S ⇒ "*structural*: reject-tile". §9.7: "An
  entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not
  make the walk incomplete: the walk passes over it, and the bytes it nominally
  addresses fall to slack." It contributes no extent.

Claimants (§9.7): front block [0,16)=16; entry0 [16,116)=100; index region
[128,192)=64 (entered once, as the layer record's extent); entry1
[300,500)=200; directory [700,900)=200; trailer [960,1024)=64.
Total claimed = 644.

(a) Slack = 1024 − 644 = **380**. (Gaps: [116,128)=12, [192,300)=108,
[500,700)=200, [900,960)=60 → 12+108+200+60 = 380 ✓.)

(b) The verifier did not elect to stop early, and neither entry defect makes the
walk incomplete (quotes above). So the walk completes ⇒ the total is
**complete**, not partial (`[R-CNT-21]`).

(c) Two established violations (T1 for entry 1, T7 for entry 2). `[R-CNF-11]`:
"An established violation takes priority: a verifier that has established any
violation reports *nonconforming*, however many requirements it was unable to
check." Verdict: **nonconforming**.

## Q10 — appended committed_file_length

`[R-LIF-02]` order: (1) begin at exactly F = 4096; (2) payloads + re-emitted
tile-index regions; (3) complete directory + its CRC; (5) pad to next 64-byte
boundary, then the 64-byte trailer.

- new stored tile: [4096, 104096) — 100000 bytes
- re-emitted index region (`[R-WRT-04]`: "re-emitted in full — entry_count
  entries plus the segment CRC array"): 32·20 + 1·4 = 644 → [104096, 104740)
  (matches §20.3's worked example, "32 · 20 + 4 = 644 bytes")
- directory: record sequence 700 + terminal CRC 4 = 704 → [104740, 105444)
- pad: 105444 mod 64 = 36 ⇒ 28 bytes of pad → 105472
- trailer: 64 bytes → [105472, 105536)

105536 mod 64 = 0 ✓ (§6.2). **Answer: 105536**

## Q11 — reserved-range vs experimental-range MU = 1 record

0x0500 ∈ reserved range 0x0003–0x7FFF; 0x8123 ∈ experimental ≥ 0x8000 (§10.2).

(a),(b) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 →
reject-file." Applies to both. **reject-file / reject-file**.

(c) `[R-CNT-15]`: "one from the reserved range is a value this specification has
not assigned — emitting it is a violation, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing
scope." P is **not** conforming.

(d) §21.6: "an **experimental-range record type carrying MU = 1** … `[R-CNT-15]`
obliges the reader to reject, and `[R-CNF-02]` makes the file conforming all the
same." Q **is** conforming.

(e) P: the violation is established ⇒ **nonconforming** (`[R-CNF-11]`, priority
clause) — the verifier must additionally report the requirement it could not
check.

(f) Q: no violation; §2.3 names this case explicitly — cannot establish "when a
record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)"
⇒ **cannot establish**.

(g) F37 vs F38: §21.1 — "Some rows are strict specializations of others … F37 of
F38 … and a file exhibiting a specialization is recorded against the narrower
row." P's record is reserved-range **with MU = 1** ⇒ **F37**.

## Q12 — duplicate, ill-formed layer names

(a) §19.1 step 4: "Uniqueness is decided first, and over the raw name bytes
whether or not each name is itself well-formed … so two layers whose name fields
are byte-identical are a duplicate even when neither name is valid." `[R-ENC-15]`
makes a duplicate layer name a file-scope error ⇒ **reject-file**. (L4's
ill-formed-UTF-8 reject-layer is also present, but the outcome applied to the
file is the file-scope one, decided first.)

(b) §19.2's four tiers are open / first access to a layer / use of a tile / use
of a record's extent. §19.2 lists "the layer-name namespace (§19.1's steps)"
under **at open**; §19.1 step 4 says "here, at open". ⇒ **open**.

(c) **F6** — "Two layer records in the live directory carry byte-identical name
fields, both obtainable within their records' inline_length (comparison is raw
bytes, no normalization)", which the question's premise satisfies.

## Q13 — rank 40, C 5000

§21.9 states **minimum guarantees, not caps**: rank 32, C 4096. `[R-ERR-04]`: "A
file exceeding any of these remains conforming, and a reader MAY decline it …
a refusal on resource grounds MUST be reported as a resource limit and not as a
validity error."

(a) **yes** — conforming (hard limits are rank ≤ 255, C ≤ 65,535; 40 and 5000
are inside them).
(b) **yes** — `[R-CNF-03]`'s acceptance duty runs only to a file "none of whose
values exceeds the minimum guarantees"; this file exceeds two of them, so
declining with a resource-limit report is licensed.
(c) `[R-ERR-05]`: "rank at most 255 and channel count at most 65,535 (§7.4's
`u8` and `u16` fields)" ⇒ **255**.

## Q14 — zstd window on a 900-byte tile

(a) `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's
decoded size". §17.2's note: "without it [Single_Segment_Flag], the
Window_Descriptor cannot express less than 1 KiB. A tile whose decoded size is
below 1 KiB … is therefore encodable under codec 3 only as a single-segment
frame." 900 < 1024 ⇒ **no**.
(b) `[R-COD-06]`: "a reader MUST treat either as a validity error at tile scope"
⇒ **reject-tile**.
(c) **T21** — "Codec 3 (zstd) and the frame declares a window size larger than
the tile's decoded size."
(d) `[R-COD-06]`: "when present it MUST equal the tile's decoded size" ⇒ **900**.

## Q15 — interleaved bool byte 0x02

(a) `[R-SER-08]`: "A reader that neither detects the violation nor rejects the
tile, and returns the value, MUST report 0x00 as false and every other byte as
true." ⇒ **true**.
(b) `[R-SER-08]`: "A reader is not obligated to screen decoded content, and a
reader that does not detect the violation is not thereby nonconforming." ⇒
**yes** (given it reports true, per (a)).
(c) `[R-SER-08]`: "its assigned detector is the verifier" ⇒ **verifier**.
(d) The position lies inside the layer's extents ⇒ a real, non-padding position
⇒ **T2** ("In an interleaved tile, a bool channel's single value byte at a real
(non-padding) sample position is neither 0x00 nor 0x01; the same byte at a
padding position is T4's").
