# Round 35 — quiz key transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read in full, lines 1–4865, in five `Read` calls). No other file was read.

Scratch files written (in `.../r35-round/scratch/quiz-keyer/`):
`qk_calc.py`, `qk_validate.py`. Scratch dir was empty when I created it.

## Method validation before answering

`qk_validate.py` reproduced, from my own CRC-32C implementation and my own
model of the layer-record field widths, three values the document states
independently:

- Appendix A trailer CRC = **0x402F157E** (spec: 0x402F157E)
- §7.4 example, CRC over 4 sentinel entries (80 bytes) = **0x80A34955** (spec: same)
- §7.4 example, crc_of_crc_array = **0xC4EE982E** (spec: same)
- §7.4 example inline payload length computed = **81** (spec: 81)
- §15.4 all-sentinel full-segment constant = **0xEECB3BB2** (spec: same)
- §4.5 check vectors: CRC-32C("123456789") = 0xE3069283, CRC-32C(empty) = 0

All searches were run whitespace-normalised (blockquote `> ` markers stripped,
runs of whitespace collapsed) with a deliberate negative control that missed,
so no conclusion here rests on a line-oriented zero.

---

## Q01 — trailer CRC bytes at 188–191

Trailer occupies [128, 192); file offsets 188–191 are trailer bytes [60, 64),
which §6.2's layout table gives as "u32 | trailer CRC | structural |
CRC-32C over trailer bytes [0, 60)".

Trailer bytes [0,60) built from §6.2's table:
```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
00 00                     version_minor = 0
00 00 00 00               flags = 0
60 00 00 00 00 00 00 00   dir_offset = 96
04 00 00 00 00 00 00 00   dir_length = 4
c0 00 00 00 00 00 00 00   committed_file_length = 192
ef be ad de 00 00 00 00   file_id = 0x00000000DEADBEEF
00 ×12                    reserved
```
CRC-32C = 0x8CB3C8B8, stored little-endian (`[R-ENC-09]`) → **b8 c8 b3 8c**.

Consistency: dir_offset 96 ≥ 16; 96+4 = 100 ≤ F−64 = 128; F = 192 is a
multiple of 64. Conforming.

**Answer: b8 c8 b3 8c**

---

## Q02 — entry_count, extent_length, inline_length

Grid counts (§11.2): G_t = ⌈5/2⌉ = 3, G_zz = ⌈9/4⌉ = 3, N = 9.
Planar ⇒ addressed-tile count = C·N = 2·9 = **18** (`[R-GEO-03]`,
"is N for an interleaved layer and C · N for a planar layer").

`[R-CNT-17]`: extent_length = 18×20 + ⌈18/2¹⁶⌉×4 = 360 + 4 = **364**.

Inline payload, §7.4 table order, packed with no padding (`[R-CNT-18]`):
- name `flux`: 1+4 = 5
- layout 1, linearization 2, codec 2, filter 2, A 8, S 8, A_slab 8, rank 1, C 2 = 34
- dim `t`: 1+1+8+8 = 18; dim `zz`: 1+2+8+8 = 19
- chan `a` int16 (elem 2): 1+1 +2 +1+2 = 7
- chan `bb` float64 (elem 8): 1+2 +2 +1+8 = 14
- index_encoding 1 + entry_count 8 + crc_of_crc_array 4 = 13

5+34+18+19+7+14+13 = **110**. (Same model yields 81 for §7.4's own example.)

**Answer: 18, 364, 110**

---

## Q03 — interleaved decoded size and q's byte offset

P = 3·4·5 = 60 (§11.2). Q = Σ Bᵢ = 1 (uint8) + 4 (float32) + 1 (bool, "with
element size 1 in the arithmetic below", §14.2) = 6.
Interleaved decoded size = P·Q = **360** (§14.2 table).

In-tile ordinal of (2,1,3) = Σ uᵢ·∏_{j>i}Tⱼ = 2·20 + 1·5 + 3 = 48 (`[R-GEO-06]`).
§14.2's closing example: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ". F_q = B_p = 1. 48·6 + 1 = **289**.

**Answer: 360, 289**

---

## Q04 — packed planar bool tile image

Tile (0,0) covers y∈[0,3), x∈[0,5); extents are 6 and 10, so every position is
real — no padding positions. P = 3·5 = 15; planar bool ⇒ packed, decoded size
⌈15/8⌉ = 2 (`[R-SER-03]`).

Value k at bit k mod 8 of byte k div 8, LSB-first, 1 = true.
Even ordinals true: byte 0 bits 0,2,4,6 → 0x55; byte 1 bits 0,2,4,6 (values
8,10,12,14) → 0x55. P mod 8 = 7 ≠ 0, so bit 7 of byte 1 is a pad bit, and
`[R-SER-05]` fixes it to the channel's fill bit — fill is 0x01 (true) — so
bit 7 is set: 0x55 | 0x80 = 0xD5.

**Answer: 55 d5**

---

## Q05 — disk ordinal, region byte offset, segment index

G = (200, 200), N = 40,000. (y,x) = (1543,210) ⇒ t = (154, 21).
s = 154·200 + 21 = 30,821 (`[R-GEO-06]`, linearization 1).
Planar, c = 2 ⇒ disk ordinal = c·N + s = 80,000 + 30,821 = **110,821**.

`[R-IDX-01]`: "the k-th entry, at region byte 20·k" ⇒ 20·110,821 = **2,216,420**.

`[R-IDX-04]`: "Segment s covers entries [s·2¹⁶, …)". 110,821 div 65,536 = **1**.
(entry_count = 3·40,000 = 120,000, so segment 1 exists and is partial.)

**Answer: 110821, 2216420, 1**

---

## Q06 — channel entry bytes

§7.4: channel entry = name (u8 len + bytes) · type u16 · fill (u8 len + bytes),
fill length = element size (`[R-CNT-23]`).
bfloat16 is type 11 (§12.1 table) ⇒ `0b 00`. §12.1's example: "bfloat16 1.0 is
`0x3F80` … stored as the bytes `80 3F`". Element size 2 ⇒ fill prefix `02`.

**Answer: 02 68 69 0b 00 02 80 3f**

---

## Q07 — experimental metadata encoding

0xB7 = 183 ≥ 0x80 ⇒ experimental range (§10.2, §18.2).
§21.6 row: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming … No
document rule attaches at such an encoding, so a verifier certifies, reporting
the record it ignored".
`[R-MTA-10]`: "A verifier meeting such a record in an otherwise conforming file
has no requirement it is unable to check — the record is not among
`[R-CNF-11]`'s cannot-establish grounds".
Flags MU=0/PE=1 match §7.3's registry; inline_length 1 satisfies `[R-MTA-03]`;
extent 200 ≥ 5 and not (0,0) satisfies `[R-CNT-25]`. No violation anywhere.

**Answer: conforming, ignore-record**

---

## Q08 — foreign major with a nonzero reserved trailer byte

§21.2: "Deriving it there yields F8, F14, F6 and both of F1's instances … and
no other row." Magic, trailer CRC and front block are all correct, so every
reaching condition is satisfied.
§2.3's Note: "F15 does not reach although its Governing rule cell cites
`[R-CNT-24]`: the trailer bytes it requires be zero are inside the 48 that rule
lets a future major redefine." So the 0x01 at trailer offset 59 establishes
nothing.
`[R-CNF-13]`: "no violation of it is established there".
§2.3: *cannot establish* is "where some requirement is one it is unable to
check on a capability … ground, as when the file names a format major version
it does not implement", and it "is available only to a traversal that
established no violation" — which this is.

Reader's ground: `[R-CNT-07]`, "A reader MUST reject-file when version_major is
0 (invalid) or is a major it does not implement".

**Answer: cannot establish, R-CNT-07**

---

## Q09 — permitted commit changes to a tile-storing planar layer

§20.3 step 4: "A layer that stores a tile **in the generation this commit
supersedes** keeps its declarations, with these exceptions and no other: its
name, and its dimension and channel names, MAY change; a dimension extent MAY
grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at its
end or shortened from its end, but not both in one commit; and a slab or
alignment declaration MAY be declared, changed or cleared…"
"A commit MAY make several of these changes at once, an extension and a
shortening of one channel list excepted."
Fixed side: "the layout, the linearization and the index encoding, the codec
and the filter, the rank and the dimension order, every tile extent, every
channel's type and fill…"

- A — names. Permitted (all three name kinds, several at once).
- B — extent 100→250, tile extents unchanged. Permitted (grow).
- C — append one and remove one. **Not** permitted: "not both in one commit";
  "replacing the last channel … is two commits or a rewrite".
- D — clear slab, declare A = 4096. Permitted: "a slab or alignment declaration
  MAY be declared, changed or cleared"; `[R-CNT-16]`'s exclusivity holds
  (A ≠ 0, S = 0).
- E — filter 1→2. **Not** permitted: filter is on the fixed list.
- F — shrink 80→40. **Not** permitted: "MUST NOT shrink".
- G — swap two channel names. Permitted: "a commit MAY change several names at
  once, two swapped included, the dimension order and the channel order being
  positional and fixed".
- H — change a fill value. **Not** permitted: "every channel's type and fill".
- I — remove the last two channels. Permitted: "shortened from its end"; no
  count limit is stated (the stipulation covers `[R-GEO-01]`'s one-channel floor).

**Answer: ABDGI**

---

## Q10 — content-size field ≠ decoded length

§18.2: "The frame's content-size field … MAY be present, and when present it
MUST equal the byte length of the decoded document. A mismatch is one of the
frame constraints R4 registers, not a failure to decode under R3: the bytes
decode, and what is wrong is what the header said about them."
Declared 4096 vs decoded 4000 ⇒ mismatch (declared larger).
R4's row lists exactly that instance; its Detector is *reader* and its Detected
cell reads *extent use*. §21.5's outcome heading: "Outcome: ignore-record".

**Answer: R4, ignore-record, extent use**

---

## Q11 — zero-length non-sentinel entry inside a slab run

Ordinal 2: offset 5000, length 0, neither field the sentinel ⇒ §15.3 row
"length = 0 (non-sentinel) | *structural*: reject-tile". §21.4's row for it is
**T10**, "A non-sentinel tile-index entry has length = 0", outcome
**reject-tile**.

Run 0 = ordinals [0, 4) (S = 4, interleaved block [0, N)). `[R-SLB-03]`:
sentinels are transparent, and "So are the entries §15.3 classifies reject-tile
on a *structural* ground: they address no usable extent, and the run's stored
tiles close over them." Ordinals 1 and 2 are therefore transparent, leaving
stored tiles 0 and 3: 1024 + 100 = 1124 ✓ packed; 1024 mod 512 = 0 ✓ aligned.
No violation.

**Answer: T10, reject-tile, no**

---

## Q12 — growing an extent while another stays 0

Before: G_a = ⌈100/32⌉ = 4, G_b = ⌈0/16⌉ = 0, N = 0, interleaved ⇒
entry_count = 0, slot (0,0).
After: G_a = ⌈200/32⌉ = 7, G_b = 0, N = 0, entry_count = 0.

§11.1: "A growth that changes no grid count … moves no entry and adds none, and
taken alone touches the directory alone; so does one that raises a grid count
while another stays 0, the product holding at 0 and the index empty either way."
§20.3 step 4 re-emits only a layer "whose stored-tile set or index content this
commit changes" — neither changes here — and "A layer the new state leaves
addressing no tile has no region to re-emit and the slot (0, 0)."

**Answer: no, 0, 0**

---

## Q13 — file_id from a hash under Appendix G

Appendix G item 2: "the identifier the digest's **last eight bytes in output
order** — the eight a named hash emits last, read little-endian".
Last eight bytes in output order: `1a 2b 3c 4d 5e 6f 70 81`.
Read little-endian: 0x81706F5E4D3C2B1A. Not all zero, so the
0x0000000000000001 substitution does not apply.

**Answer: 81706f5e4d3c2b1a**

---

## Q14 — lz4 cap on a huge planar layer

P = 2048·2048·512 = 2,147,483,648.
Channel `d` (float64) plane: P·8 = **17,179,869,184**.
Channel `m` (bool) planar ⇒ packed: ⌈P/8⌉ = 268,435,456.
Largest addressed-tile decoded size = 17,179,869,184.
Cap 0x7E000000 = 2,113,929,216, exceeded.
§21.3 row **L44**: "Codec 4 (lz4) declared on a layer any of whose addressed
tiles' decoded size exceeds 0x7E000000 bytes — in a planar layer the largest
channel plane governs". §21.3 heading: "Outcome: reject-layer".
No `[R-ENC-04]` ceiling is breached (2³⁴ ≪ 2⁶³−1), so L2 is not exhibited.

**Answer: 17179869184, L44, reject-layer**

---

## Q15 — reserved-range top-level record type with MU = 0

0x0400 lies in 0x0003–0x7FFF, the record-type reserved range (§10.2).
`[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file;
MU = 0 → ignore-record… Readers of both apply the MU rule above unchanged." ⇒
**ignore-record**.
Same rule: "one from the reserved range is a value this specification has not
assigned — emitting it is a violation, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing scope."
§21.2 row **F36** (F35 requires MU = 1, so it does not apply here). A file
exhibiting a §21.2 row is not conforming (§21.1, `[R-CNF-12]`).

**Answer: ignore-record, F36, no**
