# Round 35 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4864 lines), read in full via `sed -n` ranges.
Scratch files written (mine alone, in `.../r35-round/scratch/quiz-answerer/`): `qa_calc_r35.py`, `qa_verify_r35.py`.
Scratch directory was **empty** when I created it.

## Toolchain validation before use

`qa_verify_r35.py` reproduces every worked constant the document publishes, which is my evidence that
my CRC-32C, my layer-record length model, my sentinel model and my channel-entry model are the document's:

- CRC-32C("123456789") = 0xE3069283, CRC-32C(zero bytes) = 0x00000000 (§4.5 check vector) — match
- Appendix A trailer CRC = 0x402F157E — match
- §7.4 example: 80-byte 4-sentinel array CRC = 0x80A34955; crc_of_crc_array = 0xC4EE982E — both match
- §15.4 full all-sentinel segment CRC = 0xEECB3BB2 — match
- §7.4 example inline payload length = 81 — match
- §12.3 `temp` channel entry = `04 74 65 6d 70 0c 00 04 00 00 c0 7f` — match
- §14.3 packed-plane example (P=10, alternating, fill true → `55 FD`) — my packer reproduces it

## Search discipline

The document is hard-wrapped and blockquotes wrap with `> `. Line-oriented `grep` returned **0** for
"two swapped included" and "last eight bytes"; a whitespace-normalized search (with `> ` stripped)
found both. No conclusion below rests on a raw-grep zero.

---

## Q01 — trailer CRC bytes at 188..191

F = 192, trailer at [128, 192). File offsets 188..191 = trailer offsets 60..63 = the trailer CRC
(§6.2 layout table: "60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60)").

Trailer bytes [0,60) assembled little-endian (`[R-ENC-01]`):
`8a 4e 52 41 54 0d 0a 1a | 01 00 | 00 00 | 00 00 00 00 | 60 00.. (96) | 04 00.. (4) | c0 00.. (192) | ef be ad de 00 00 00 00 | 00 ×12`

CRC-32C = 0x8CB3C8B8, stored little-endian → **b8 c8 b3 8c**

## Q02 — entry_count, extent_length, inline_length

G = (⌈5/2⌉, ⌈9/4⌉) = (3, 3), N = 9 (§11.2). Planar ⇒ addressed-tile count = C·N = 2·9 = **18**
("its **addressed-tile count** … is N for an interleaved layer and C · N for a planar layer", `[R-GEO-03]`).

`[R-CNT-17]`: extent_length = 18 × 20 + ⌈18/2¹⁶⌉ × 4 = 360 + 4 = **364**.

Inline payload (§7.4 packed order, no padding):
name 1+4 = 5; nine scalars layout..C = 1+2+2+2+8+8+8+1+2 = 34; dim entries (1+1+8+8)+(1+2+8+8) = 18+19 = 37;
channel entries (1+1+2+1+2)+(1+2+2+1+8) = 7+14 = 21; trailing 1+8+4 = 13. Total = **110**. No sub-records.
(Model checked against §7.4's 81-byte worked example.)

**18, 364, 110**

## Q03 — interleaved decoded size and offset

P = 3·4·5 = 60. Q = Σ Bᵢ = 1 (uint8) + 4 (float32) + 1 (bool, "element size 1 in the arithmetic below", `[R-SER-02]`) = 6.
Decoded size = P·Q = **360**.

In-tile ordinal (§11.4) = Σ uᵢ·∏_{j>i}Tⱼ = 2·(4·5) + 1·5 + 3 = 48.
Offset = u·Q + F_q, F_q = 1 (only `p` precedes) → 48·6 + 1 = **289**.

**360, 289**

## Q04 — packed planar bool tile image

Planar bool ⇒ §14.3 packing. P = 3·5 = 15, decoded size ⌈15/8⌉ = 2.
Tile (0,0) covers y 0–2, x 0–4, all inside extents (6, 10): no padding positions.
Even ordinals true: byte 0 bits 0,2,4,6 = 0x55; byte 1 holds values 8–14 at bits 0–6, evens 8,10,12,14 → bits 0,2,4,6 = 0x55.
P mod 8 = 7 ≠ 0, so bit 7 is a pad bit; `[R-SER-05]`: "Every pad bit (§14.3) MUST carry the plane's channel's fill bit."
Fill 0x01 = true ⇒ bit 7 set ⇒ 0xD5.

**55 d5**

## Q05 — planar disk ordinal, entry offset, segment

G = (200, 200), N = 40000. t = (1543 div 10, 210 div 10) = (154, 21).
s = 154·200 + 21 = 30821 (`[R-GEO-06]`). `c2` has channel index 2, disk ordinal = c·N + s = 80000 + 30821 = **110821**.
Entry at region byte 20·k = **2216420** (§15.1: "The entry for the tile with disk ordinal k … is at region byte 20·k").
Segment = ⌊110821/2¹⁶⌋ = **1** (§15.4).

**110821, 2216420, 1**

## Q06 — channel entry bytes

§7.4 channel entry = name (u8 len + bytes) · type u16 · fill (u8 len + bytes).
bfloat16 = type 11 (§12.1 table) → `0b 00`. Element size 2 ⇒ fill length prefix 02.
bfloat16 1.0 = 0x3F80 (§12.1 Example), little-endian `80 3f`.

**02 68 69 0b 00 02 80 3f**

## Q07 — experimental-range metadata encoding

Encoding byte 0xB7 = 183 ≥ 0x80 ⇒ experimental range (§10.2, §18.2).
§21.6 row: "A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming … so a verifier certifies, reporting the record it ignored".
Registry flags for type 0x0002 are MU=0/PE=1 (matched, so no F28); inline_length 1 ✓; extent 200 ≥ 5, not (0,0) ✓; extent CRC verifies ✓.

**conforming, ignore-record**

## Q08 — foreign major with a nonzero reserved trailer byte

`[R-CNF-13]` / §21.2: "Deriving it there yields F8, F14, F6 and both of F1's instances … and no other row."
F8 (magic) ✓ satisfied, F14 (trailer CRC) ✓, F6/F1 (front block constant) ✓.
§2.3 Note: "F15 does not reach although its Governing rule cell cites `[R-CNT-24]`: the trailer bytes it
requires be zero are inside the 48 that rule lets a future major redefine." So the 0x01 reserved byte
establishes nothing here.

No violation established; the file names a major the verifier does not implement — §2.3's first named
cannot-establish ground. Refusal ground for the reader: `[R-CNT-07]` (§6.3).

**cannot establish, R-CNT-07**

## Q09 — permitted commit changes to a tile-storing layer

§20.3 step 4 exception list: names (layer, dimension, channel) MAY change; a dimension extent MAY grow
and MUST NOT shrink; a planar channel list MAY be extended at its end **or** shortened from its end,
not both in one commit; a slab or alignment declaration MAY be declared, changed or cleared.

- A names — permitted ("A commit MAY make several of these changes at once")
- B extent growth — permitted
- C append + remove in one commit — barred ("a commit that shortens … appends no channel to it and one that extends it removes none")
- D clear slab, declare A=4096 — permitted (declaration "declared, changed or cleared"); `[R-CNT-16]` satisfied since S=0
- E filter 1→2 — fixed declaration, barred
- F extent shrink — barred
- G swap two channel names — permitted ("a commit MAY change several names at once, two swapped included")
- H fill change — fixed ("every channel's type and fill"), barred
- I shorten planar channel list by two at the end — permitted

**ABDGI**

## Q10 — encoding-2 frame content-size mismatch

§18.2: the content-size field "MAY be present, and when present it MUST equal the byte length of the
decoded document. A mismatch is one of the frame constraints R4 registers, not a failure to decode under R3".
Declared 4096 vs decoded 4000 ⇒ R4, instance "content-size field declared larger than the decoded length,
top-level extent". §21.5 outcome header: ignore-record. R4's Detected cell: extent use.

**R4, ignore-record, extent use**

## Q11 — zero-length non-sentinel entry inside a slab run

Ordinal 2: offset 5000, length 0, crc ≠ 0, non-sentinel. §15.3 row "length = 0 (non-sentinel) | *structural*:
reject-tile". Register row **T10** ("A non-sentinel tile-index entry has length = 0"), §21.4 outcome reject-tile.

Run 0 = ordinals [0,4) (S=4, interleaved block [0,N)). Ordinal 1 is a sentinel (transparent); ordinal 2 is
structural reject-tile — `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile on a *structural*
ground … the run's stored tiles close over them." Stored tiles are 0 and 3: 1024 + 100 = 1124 ✓ packed;
1024 mod 512 = 0 ✓ aligned. No violation.

**T10, reject-tile, no**

## Q12 — growth that leaves a zero grid count

Old G = (⌈100/32⌉, ⌈0/16⌉) = (4, 0), N = 0. New G = (7, 0), N = 0. Interleaved ⇒ entry_count = N = 0 both ways.
§11.1: "so does one that raises a grid count while another stays 0, the product holding at 0 and the index
empty either way" — touches the directory alone. §20.3 step 4: "A layer the new state leaves addressing no
tile has no region to re-emit and the slot (0, 0)."

**no, 0, 0**

## Q13 — derived file_id

Appendix G item 2: "the identifier the digest's **last eight bytes in output order** — the eight a named
hash emits last, read little-endian".
Last eight in output order: `1a 2b 3c 4d 5e 6f 70 81`. Read little-endian → 0x81706F5E4D3C2B1A.

**81706f5e4d3c2b1a**

## Q14 — lz4 cap on a huge planar layer

G = (1,1,1), N = 1, P = 2048·2048·512 = 2,147,483,648 = 2³¹.
Planar numeric plane for `d` (float64, Bᶜ=8): P·8 = 2³⁴ = **17179869184**.
Packed bool plane for `m`: ⌈P/8⌉ = 268,435,456. Largest = 17,179,869,184.
0x7E000000 = 2,113,929,216 < 17,179,869,184 ⇒ `[R-COD-07]` cap broken. Row **L44** ("Codec 4 (lz4) declared
on a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes — in a planar layer the
largest channel plane governs"), §21.3 outcome reject-layer.

**17179869184, L44, reject-layer**

## Q15 — reserved-range top-level record type with MU = 0

0x0400 lies in the record-type reserved range 0x0003–0x7FFF (§10.2).
`[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file; MU = 0 → ignore-record."
Register row **F36** ("A top-level record carries a type value from the reserved range 0x0003-0x7FFF …
emitting one is a violation whatever its MU bit"); F35 is the MU = 1 specialization and does not apply.
§21.6: a reserved-range type "is read the same way, but emitting one is a violation (F36, L25)" ⇒ the
file is nonconforming.

**ignore-record, F36, no**
