# Cleanroom round 10 — quiz answerer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,919 lines, in four `Read` calls plus `wc`). I read no ADR, no
`docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`. I ran no `git` command of any kind, no web search, no
web fetch, and I listed no directories.

Local computation I ran, all in my own scratchpad, reading no project file
except the one above:

- `calc.py` — a from-scratch CRC-32C (Castagnoli, reflected, init/xor
  0xFFFFFFFF) plus the arithmetic for Q01–Q05, Q09, Q14.
- `verify.py` — validation of that CRC against two constants the spec
  itself states, both reproduced exactly:
  - CRC-32C of 2^16 sentinel entries = `0xEECB3BB2` (§15.4, `[R-IDX-05]`)
  - Appendix A's trailer CRC = `0xE00938D2` over its trailer bytes [0,60)
  - plus §4.5's own check vector: CRC-32C(`"123456789"`) = `0xE3069283`,
    CRC-32C(zero bytes) = `0x00000000`
- Two short Python passes over `spec/tarn.md` itself to count the
  Instances cells of §21.2–§21.5 mechanically.

Calibration note on the Q12 method: counting semicolon-separated items per
cell, with `—` = 1, yields 36/49/26/10 rows and 53/106/45/44 instances,
totalling **121 conditions over 248 instances** — exactly the figures
§21.8 states. The counting rule is therefore confirmed against the
document's own arithmetic, not just my reading of §21.1.

---

## Q01 — final 16 bytes of a 320-byte file

F = 320, so the trailer occupies [256, 320) and offsets [304, 320) are
trailer bytes **[48, 64)**: file_id (8), reserved (4), trailer CRC (4).

§6.2's layout table:

| trailer offset | field | value | bytes (LE) |
|---|---|---|---|
| 48 | file_id | 0x00FF00FF00FF00FF | `ff 00 ff 00 ff 00 ff 00` |
| 56 | reserved | zero | `00 00 00 00` |
| 60 | trailer CRC | CRC-32C over [0,60) | computed |

Trailer bytes [0, 60) assembled from the given fields:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                     version_major = 1
03 00                     version_minor = 3
00 00 01 00               flags = 0x00010000
04 00 00 00 00 00 00 00   generation = 4
10 00 00 00 00 00 00 00   dir_offset = 16
54 00 00 00 00 00 00 00   dir_length = 84
40 01 00 00 00 00 00 00   committed_file_length = 320
ff 00 ff 00 ff 00 ff 00   file_id
00 00 00 00               reserved
```

CRC-32C over those 60 bytes = **0x1F74BD23** → stored LE `23 bd 74 1f`.

Decisive: §6.2 table row — "| 60 | 4 | u32 | trailer CRC | structural |
CRC-32C over trailer bytes [0, 60) |", with §4.5's `[R-ENC-09]` fixing the
CRC parameters and little-endian storage.

**Answer:** `ff 00 ff 00 ff 00 ff 00 00 00 00 00 23 bd 74 1f`

---

## Q02 — planar bool tile, extents (3,2), tile extents (3,3), fill true

Grid: G₀ = ⌈3/3⌉ = 1, G₁ = ⌈2/3⌉ = 1 → N = 1, one tile. P = ∏Tᵢ = 9.

Planar bool → §14.3 packed plane, decoded size ⌈P/8⌉ = **2 bytes**.

In-tile ordinal (§11.4) = u₀·T₁ + u₁ = 3u₀ + u₁. Real positions need
x₁ < E₁ = 2, so u₁ = 2 is a **padding position** (§11.3) at every u₀.

| k | (u₀,u₁) | status | bit |
|---|---|---|---|
| 0 | (0,0) | real → false | 0 |
| 1 | (0,1) | real → false | 0 |
| 2 | (0,2) | padding → fill | 1 |
| 3 | (1,0) | real | 0 |
| 4 | (1,1) | real | 0 |
| 5 | (1,2) | padding → fill | 1 |
| 6 | (2,0) | real | 0 |
| 7 | (2,1) | real | 0 |
| 8 | (2,2) | padding → fill | 1 |

Byte 0 = bits 0–7 = k=0..7 → bits 2 and 5 set = 0b00100100 = **0x24**.
Byte 1 = bit 0 is k=8 = 1; bits 1–7 are **pad bits**, which `[R-SER-05]`
requires to carry the plane's channel's fill bit (true = 1) → **0xFF**.

Decisive: `[R-SER-05]` — "at every padding position, a writer MUST encode,
for each channel the position carries, that channel's fill value … Every
pad bit (§14.3) MUST carry the plane's channel's fill bit."

**Answer:** `24 ff`

Oddity worth stating: the tile is majority-1 bits even though every real
sample is false — fill = true propagates into both the padding positions
and the pad bits.

---

## Q03 — interleaved, extents (2,2), tiles (2,3), channels a:uint8, b:int16

P = 2·3 = 6, C = 2, Q = ΣBᵢ = 1 + 2 = 3.
Decoded size = P·Q = 6·3 = **18** (§14.2 table, interleaved row).

Bytes 6–8: value offsets are (k div C)·Q + F_{k mod C}. Byte 6 starts the
sample at in-tile ordinal u = 6/Q = 2; byte 6 is channel a (F₀ = 0), bytes
7–8 channel b (F₁ = 1).

In-tile ordinal 2 → u₀ = 2 div 3 = 0, u₁ = 2 mod 3 = 2 → coordinate
(0, 2). E₁ = 2, so x₁ = 2 ≥ E₁: a **padding position**. Its content is
fixed to each channel's recorded fill (`[R-SER-05]`): a = `07`,
b = `fe ff`.

Decisive: §14.2 table "| interleaved | P · Q | (k div C) · Q + F_{k mod C} |"
and `[R-SER-05]`'s "the recorded fill bytes for a numeric channel".

**Answer:** 18, then `07 fe ff`

---

## Q04 — planar, d=3, C=5, E=(7,100,250), T=(4,32,64)

G₀ = ⌈7/4⌉ = 2, G₁ = ⌈100/32⌉ = 4, G₂ = ⌈250/64⌉ = 4 → N = 2·4·4 = **32**.

1. entry_count (planar) = C·N = 5·32 = **160**  (`[R-GEO-03]`)
2. extent_length = 160×20 + ⌈160/2¹⁶⌉×4 = 3200 + 4 = **3204** (`[R-CNT-17]`)
3. tile coords tᵢ = xᵢ div Tᵢ = (5 div 4, 40 div 32, 200 div 64) = (1,1,3);
   s = Σ tᵢ·∏_{j>i}Gⱼ = 1·(4·4) + 1·4 + 3 = 23;
   disk ordinal = c·N + s = 3·32 + 23 = **119**  (`[R-GEO-06]`)
4. region byte 20·k = 20·119 = **2380**  (`[R-IDX-01]`)
5. uᵢ = xᵢ mod Tᵢ = (1, 8, 8);
   ordinal = Σ uᵢ·∏_{j>i}Tⱼ = 1·(32·64) + 8·64 + 8 = 2048 + 512 + 8 = **2568**

Decisive: `[R-GEO-06]` — "The **disk tile ordinal**, which orders
tile-index entries (§15), is s for an interleaved layer, and **c · N + s**
for a planar layer".

**Answer:** 160, 3204, 119, 2380, 2568

---

## Q05 — index_encoding 1, entry_count 3, all sentinels

1. extent_length = 3×20 + ⌈3/2¹⁶⌉×4 = 60 + 4 = **64**  (`[R-CNT-17]`)
2. One segment, covering entries [0, 3) — a **partial** segment, so
   `[R-IDX-05]`'s 0xEECB3BB2 constant does **not** apply ("a partial
   segment's CRC MUST be computed"). The 60 covered bytes are three copies
   of `FF ×16 00 ×4` (§15.2). CRC-32C = 0xD171D122 → stored LE
   **`22 d1 71 d1`**.
3. crc_of_crc_array = CRC-32C over that 4-byte array = **`34c74afb`**.

Decisive: §15.4 — "the s-th u32 of the segment CRC array is the CRC-32C
over exactly those entries' bytes as stored — the final partial segment's
CRC covers only its actual bytes."

**Answer:** 64; `22 d1 71 d1`; `34c74afb`

---

## Q06 — two verifier verdicts

**File X.** Layer B declares linearization = 2. `[R-GEO-05]`: "A reader
MUST treat any linearization value other than 1 as a validity error at
layer scope — this includes 0, all reserved values". Register row L33,
detector *reader*, detected at layer access. The verifier completes a full
traversal, so it **establishes** this violation. Layer A's un-executable
zstd is a `[R-COD-11]` *cannot establish* ground, but §2.3 settles the
collision.

Decisive: §2.3 — "An established violation takes priority: a verifier that
has established any violation reports *nonconforming*, however many
requirements it was unable to check, and *cannot establish* is available
only to a traversal that established no violation."

**File Y.** `[R-MTA-09]`: "A **verifier** that declines to decode a
document cannot establish that document's conformance and MUST NOT certify
the file … it fixes the file's verdict as *cannot establish* only where
the verifier established no violation elsewhere". Nothing else in file Y
violates anything, and the bound is at or above §21.9's 16 MiB guarantee,
so declining is legitimate.

**Answer:** nonconforming, cannot establish

---

## Q07 — two layer records with byte-identical ill-formed names

Both name fields are `03 61 c0 62` and both lie within inline_length. Two
candidate conditions collide: L3 (name bytes not well-formed UTF-8,
reject-layer) and F4 (byte-identical layer names, reject-file). §19.1 step
4 orders them explicitly.

Decisive: §19.1 step 4 — "Uniqueness is decided first, and over the raw
name bytes whether or not each name is itself well-formed — `[R-ENC-13]`
makes name comparison a byte comparison, which needs no valid name — so
two layers whose name fields are byte-identical are a duplicate even when
neither name is valid."

F4's own text confirms the row applies: "Two layer records in the live
directory carry byte-identical name fields, both obtainable within their
records' inline_length" — reader, open, `[R-ENC-15]`, outcome reject-file
(§21.2's heading: "Outcome: reject-file").

**Answer:** reject-file, F4

---

## Q08 — front-block check for three readers

`[R-CNT-04]` makes the test **residency**, not transport: "A reader whose
open leaves bytes [0, 16) **resident** — a local file, a memory mapping, a
speculative suffix window that reached offset 0, or any transport already
holding them — and a content sniffer MUST verify the full block by byte
equality before other processing … A reader that would have to issue a
further range request to obtain those bytes MAY defer or omit the check."

- **Reader 1** — memory-mapped local file: named verbatim in the resident
  list → **MUST**.
- **Reader 2** — window is [983,040, 1,048,576); it never reaches offset 0,
  so bytes [0,16) require a further range request → **MAY-OMIT**.
  (Containment gets it the directory, which is §6.4's separate concern.)
- **Reader 3** — the 40,000-byte file is shorter than the 65,536-byte
  window and the transport returned the whole file, so the front block is
  in hand: "any transport already holding them" → **MUST**. Appendix A
  states the same case: "as a remote reader does too whenever its
  speculative suffix window reaches offset 0".

Noted alternative I rejected: `[R-CNT-10]` lets a reader *abort* a 200
response, and an aborted reader arguably never holds [0,16). The scenario
stipulates the response returned the entire file, and for a suffix request
on a 40 KB file the front block is the first thing to arrive, so residency
obtains.

**Answer:** MUST, MAY-OMIT, MUST

---

## Q09 — recovery probe on a 1,000-byte file

Decisive: `[R-LIF-06]` — "The probe begins at the largest 64-aligned offset
o with o + 64 ≤ the physical file length" and, earlier, "on a match,
require the trailer CRC to verify and committed_file_length = o + 64."

Largest 64-aligned o with o + 64 ≤ 1000 → o ≤ 936 → o = 64·14 = **896**.
Required committed_file_length = 896 + 64 = **960**.

Oddity, answered as written: the physical file is 1,000 bytes but the
candidate must declare 960 — the trailing 40 bytes are exactly the residue
`[R-LIF-04]` obliges a writer to have truncated.

**Answer:** 896, 960

---

## Q10 — compactor output trailer

1. **version_minor = 5.** `[R-WRT-06]`: the output "carries the greater of
   `[R-CNT-26]`'s floor and the input's version_minor — a compactor cannot
   know which minor version defined an ignore-lane bit it does not
   implement, so it does not lower the floor beneath one." The file is
   expressible under this text, so `[R-CNT-26]`'s floor is 0; max(0, 5) = 5.
2. **generation = 1.** `[R-WRT-06]`: "It MUST mint a fresh file_id for the
   output … and generation 1".
3. **flags = `00050000`.** `[R-CNT-08]`: "A compactor, though its output is
   a new file, carries the input's unknown ignore-lane bits into its output
   trailer rather than writing flags = 0". Bits 16 and 18 are ignore-lane
   and unknown to this compactor; the incompat lane is clear.
4. **no.** `[R-WRT-06]`: "a new draw under §9.3's randomness advice, not
   merely a value compared against the input's". Reuse would also break
   `[R-LIF-03]`'s (file_id, range) cache contract.

**Answer:** 5, 1, `00050000`, no

---

## Q11 — experimental sub-record type 0x8001 with MU = 1

1. **reject-layer.** `[R-CNT-18]`: "an unknown sub-record type with MU = 1
   is reject-layer — never reject-file — and with MU = 0 is
   ignore-record."
2. **no.** `[R-WRT-06]`: "A compactor MUST refuse to compact a file
   carrying any record whose type it does not implement with MU = 1: such
   a type can define references this specification does not (§7.2), so its
   bytes cannot be safely relocated." §20.4's MU = 1 row concurs:
   "Compaction is barred on the same ground".
3. **yes.** 0x8001 is the experimental range (§10.2: record type
   experimental ≥ 0x8000), and §21.6 lists this exact case: "an
   **experimental-range record type carrying MU = 1** … `[R-CNT-15]`
   obliges the reader to reject, and `[R-CNF-02]` makes the file
   conforming all the same, since the prohibition on publishing
   experimental values binds a writer's conduct and not the bytes."
   `[R-CNF-03]` corroborates: "in a conforming file such a type is
   necessarily from the experimental range".

   Assumption stated: the sub-record's PE bit is 1. `[R-CNT-12]` forbids
   writers to emit MU = 1 with PE = 0 and L46 registers that combination
   as a verifier-detected layer-scope violation, so PE = 0 would make the
   file nonconforming on a different ground. The scenario does not state
   PE; the spec's answer to the condition it does state is unambiguous.

**Answer:** reject-layer, no, yes

---

## Q12 — instance count of §21.4

§21.1's rule: "Instances within a cell are separated by semicolons, and a
cell reading — is one instance; the count is therefore mechanical once the
cell is written."

Applied mechanically to T1–T26:

```
T1 1  T2 1  T3 6  T4 4  T5 1  T6 1  T7 2  T8 1  T9 1  T10 1
T11 2 T12 1 T13 2 T14 1 T15 2 T16 1 T17 1 T18 4 T19 1 T20 1
T21 1 T22 1 T23 1 T24 1 T25 3 T26 3
```

Sum = **45**. (T24's `any codec` is one instance by §21.1's own example:
"a row whose check ranges over a family without the condition changing
shape states that range as a single instance (T24's *any codec*)".)

Cross-check: the same method over §21.2–§21.5 gives 53 + 106 + 45 + 44 =
248 instances over 121 rows, matching §21.8 exactly ("121 conditions over
248 instances"). The method is validated by the document's own arithmetic.

**Answer:** 45

---

## Q13 — checksum chain above a tile-index entry's crc field

§4.5 classifies the entry's crc field as an **interior** checksum: "each
segment CRC array, each tile-index entry's crc field, and each layer
record's crc_of_crc_array — are both comparison-verified and covered by
exactly one further checksum, as §8.1 maps."

Walking §8.1's map upward:

1. The crc field sits inside its 20-byte entry; §8.1 row "Tile-index
   region | the per-segment CRC array … | index entries, per segment" →
   covered by **the segment CRC** for that entry's segment — the u32 in
   the tile-index region's segment CRC array.
2. That array is covered by **the layer record's `crc_of_crc_array`
   field** (same §8.1 row: "itself covered by the layer record's
   crc_of_crc_array").
3. `crc_of_crc_array` is a field of the layer record's inline payload,
   i.e. part of the directory's raw record sequence → covered by **the
   directory region's terminal CRC**, its final 4 bytes ("the preceding
   dir_length − 4 bytes (the raw record sequence)").

Stop there: §4.5 names the directory-region checksum field as terminal —
"the trailer, directory- region, and user-metadata checksum fields — which
are verified by comparison and covered by no further checksum". The
trailer CRC covers only trailer bytes [0,60), which do not include the
directory region's bytes, so the chain does not continue into it.

**Answer:** (1) the segment CRC array's u32 for that entry's segment;
(2) the layer record's `crc_of_crc_array` field; (3) the directory
region's final-4-byte CRC (terminal).

---

## Q14 — 448-byte file with a 252-byte pre-trailer gap

1. **Yes, conforming.** Gates: F = 448 = 64·7 ✓; dir_offset 128 ≥ 16 ✓;
   dir_length 4 ≥ 4 ✓; 128 + 4 = 132 ≤ F − 64 = 384 ✓; ≥ 128 bytes ✓;
   directory CRC correct over zero bytes ✓; zero records is valid
   (`[R-CNT-14]`, and §21.6 "The file contains zero layers → A conforming
   file with an empty directory"). The 252-byte gap [132, 384) holds no
   structure, so F7 does not fire.

   Decisive: `[R-CNT-05]` — "this specification does not constrain their
   content, and bounds their number only through step 5 of the commit
   protocol, which pads to the next 64-byte boundary (`[R-LIF-02]`) — **a
   longer gap is conforming, and no conforming commit produces one**."

   The oddity is deliberate and is `[R-CNF-02]`'s design: file conformance
   is a pure predicate on bytes, so a file no conforming commit would
   produce can still be conforming.

2. **364 slack bytes.** §9.7's walk claims the front block [0,16), the
   live directory [128,132), and the live trailer [384,448) — 16 + 4 + 64
   = 84 claimed bytes; zero records means no extents and no index regions.
   448 − 84 = 364. Equivalently [16,128) = 112 plus [132,384) = 252.
   The walk completes, so `[R-CNT-21]`'s partial-total clause does not
   apply and the verifier reports a full total.

**Answer:** yes, 364

---

## Q15 — trailer field domains

**File P** — file_id = 0xFFFFFFFFFFFFFFFF, generation = 0x7FFFFFFFFFFFFFFF.

`[R-ENC-03]`'s 0…2⁶³−1 domain binds "every offset, length, extent, and
count this specification defines — entry counts and slab run lengths
included". file_id is none of those: §6.2's table classes it *semantic*
with valid values "≠ 0", and register row F2's instance list is
"dir_offset; dir_length; committed_file_length; generation; non-layer
top-level record extent_offset; extent_length" — **file_id is absent from
it while generation is present**. All-ones file_id is therefore in range.
generation = 2⁶³ − 1 is exactly the stated ceiling (§6.2: "1 ≤ generation
≤ 2⁶³ − 1"), and §9.3's note confirms it is a reachable, legal state ("a
file standing at 2⁶³ − 1 admits no further commit"). → **yes**

**File Q** — file_id = 1 (fine, ≠ 0); generation = 0x8000000000000000 =
2⁶³, one above the ceiling. Violates §6.2/`[R-CNT-06]` and `[R-ENC-03]`
(register rows F2, and `[R-CNT-06]`'s gate). → **no**

Decisive: §6.2 table — "| 48 | 8 | u64 | file_id | semantic | ≠ 0 |" and
"| 16 | 8 | u64 | generation | semantic | 1 ≤ generation ≤ 2⁶³ − 1 |".

**Answer:** yes, no
