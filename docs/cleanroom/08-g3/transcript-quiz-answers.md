# Round 8 — quiz answerer transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3842 lines, in four `Read` chunks plus a `wc`). I ran one Python
script that reads no files (arithmetic, struct packing, bit packing,
byte-shuffle simulation). No ADRs, no docs/, no conformance/, no
registry.json, no git history, no web, no directory listings.

---

## Q01 — two channel entries

§7.4 channel entry layout: `name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes)`,
"fill length equals the type's element size (`[R-CNT-23]`)". Fields "are packed in
table order with no alignment or padding between them" (`[R-CNT-18]`).

Channel 0 — `m`, bool, fill true:
- name: `01 6D`
- type: bool = 1 (§12.1 table) → u16 LE `01 00`
- fill: bool element size 1 (§12.1); §13.2 "`0x00` (false) or `0x01` (true)" → len `01`, byte `01`
→ `01 6D 01 00 01 01`

Channel 1 — `bt`, bfloat16, fill 1.0:
- name: `02 62 74`
- type: bfloat16 = 11 → `0B 00`
- fill: element size 2; §12.1 example "bfloat16 1.0 is `0x3F80` … stored as the bytes `80 3F`"
→ len `02`, bytes `80 3F`
→ `02 62 74 0B 00 02 80 3F`

Concatenated (14 bytes): **016d010001010262740b0002803f**

Cross-check against §12.3's worked example `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — same field order.

Confidence: high.

## Q02 — planar bool edge tile

Geometry: G = (⌈5/4⌉, ⌈5/4⌉) = (2,2), N = 4, P = ∏Tᵢ = 16 (§11.2).
Planar, C = 1 → addressed-tile count = C·N = 4.

Tile (1,1) covers coords 4–7 on both axes; only (4,4) is inside the extents
(§14.5's example uses exactly this geometry: "one real position, (4, 4), and
15 padding positions"). In-tile position of (4,4) is (0,0) → in-tile ordinal 0.

(a) Planar bool → §14.3 packed plane, decoded size ⌈P/8⌉ = 2 bytes, "value k
occupies bit k mod 8 of byte k div 8 … 0 = false and 1 = true". P mod 8 = 0, so
no pad bits. §14.5: every padding position carries "the fill bit in a packed
plane"; fill byte 0x01 = true → bit 1. So bit 0 = 0 (the stored false), bits
1–15 = 1.
byte0 = 0b1111_1110 = 0xFE, byte1 = 0xFF → **FEFF**

(b) The tile is stored (fill is true; the sample reads false, so a sentinel is
impossible). filter 1 = none, codec 1 = none: "The stored bytes are the filtered
image verbatim. The index entry's length therefore MUST equal the tile's decoded
size" (`[R-COD-04]`) → **2**

(c) s = t₀·G₁ + t₁ = 1·2 + 1 = 3 (`[R-GEO-06]`); planar disk ordinal = c·N + s =
0·4 + 3 = 3. §15.1: "The entry for the tile with disk ordinal k is the k-th
entry, at region byte 20·k" → **60**

Confidence: high.

## Q03 — interleaved shuffle

P = 2, C = 2, Q = 1 + 2 = 3, decoded size P·Q = 6 (`[R-SER-02]`).
Interleaved sample-major (`[R-SER-01]`): ordinal 0 → `11 33 22`, ordinal 1 → `44 66 55`
(uint16 little-endian).
Decoded image: `11 33 22 44 66 55`.

Filter 2, `[R-COD-10]`: stride s = Q = 3 for an interleaved tile; n = L/s = 2;
"the filtered image places byte i of group j at offset i · n + j".
- (i,j) = (0,0)→0:11, (1,0)→2:33, (2,0)→4:22, (0,1)→1:44, (1,1)→3:66, (2,1)→5:55

Filtered = `11 44 33 66 22 55`. Codec 1 → stored verbatim.

**114433662255**

Confidence: high.

## Q04 — 3-D interleaved offset

G = (⌈10/4⌉, ⌈9/5⌉, ⌈7/3⌉) = (3, 2, 3), N = 18.
Coordinate (7,6,5): t = (1,1,1), u = (3,1,2) (`[R-GEO-06]`).

(a) s = t₀·G₁G₂ + t₁·G₂ + t₂ = 1·6 + 1·3 + 1 = 10; interleaved → disk ordinal = s = **10**

(b) in-tile ordinal = u₀·T₁T₂ + u₁·T₂ + u₂ = 3·15 + 1·3 + 2 = 50.
Q = 1 + 8 + 2 = 11; F² (channel `c`, index 2) = B_a + B_b = 9.
Offset = u·Q + Fᶜ = 50·11 + 9 = **559**
(§14.2's closing sentence: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ".)

Confidence: high.

## Q05 — slack total

Layer cross-check: extent_length 84 = 4×20 + ⌈4/2¹⁶⌉×4 ✓ (`[R-CNT-17]`).

`[R-LIF-08]` walk claimants:
- front block [0,16) = 16
- tile-index region (the layer record's extent) [16,100) = 84
- entry 0's extent [100,220) = 120
- entry 1: valid sentinel — no extent
- entry 2: crc mismatch. §9.7 parenthetical: "one whose stored bytes alone fail its
  crc keeps its extent"; §15.3: "its extent stands and it keeps its place … in the
  coverage walk" → [256,320) = 64
- entry 3: offset 8 < 16 → *structural* reject-tile; "contributes no stored extent
  to the walk" and its nominal bytes "fall to slack"
- directory [832,928) = 96
- trailer [960,1024) = 64

Claimed = 444. Slack = 1024 − 444 = **580**
(equivalently the gaps [220,256)=36, [320,832)=512, [928,960)=32).

Walk completes: "An entry `[R-IDX-03]` classifies reject-tile does not make the
walk incomplete", and the verifier does not stop early — so this is a full, not
partial, total.

*Noted ambiguity, resolved:* §9.7's last sentence, read without the "structural"
qualifier it carries earlier in the same paragraph, would also send entry 2's 64
bytes to slack (giving 644). The parenthetical two paragraphs above and §15.3's
explicit "its extent stands … in the coverage walk" settle it at 580.

Confidence: high (medium on the drafting looseness, not on the answer).

## Q06 — segments at entry_count 131072

(a) `[R-CNT-17]`: 131072×20 + ⌈131072/65536⌉×4 = 2,621,440 + 8 = **2,621,448**

(b) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))".
100000 div 65536 = 1 → segment 1 covers entries [65536, 131072), region bytes
20·65536 = 1,310,720 to 20·131072 = 2,621,440 → **[1310720, 2621440)**

(c) §15.1: entry array then segment CRC array. Array starts at 2,621,440; "the
s-th u32 of the segment CRC array" with s = 1 → **[2621444, 2621448)**

Confidence: high.

## Q07 — planar slab run

(a) c = 19 div N = 19 div 10 = **1** (disk ordinal = c·N + s, `[R-GEO-06]`)
(b) s = 19 − 1·10 = **9**
(c) `[R-SLB-02]`: planar blocks [c·N, (c+1)·N) = [10,20); "Run r of a block starts
at ordinal block_start + r·S" with S = 4 → runs start at 10, 14, 18; 19 is in the
run starting at **18** (the final run of the block, covering 2 ordinals — "the
final run of a block can cover fewer than S ordinals").
A_slab = 512 is not used in this computation.

Confidence: high.

## Q08 — reserved-range top-level record, MU = 0

0x0005 lies in the record-type reserved range 0x0003–0x7FFF (§10.2).

(a) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file;
MU = 0 → ignore-record. … Readers of both apply the MU rule above unchanged."
→ **ignore-record**

(b) Same rule: "one from the reserved range is a value this specification has not
assigned — emitting it is a violation, and a verifier MUST treat a reserved-range
record type as a validity error at the record's governing scope." Register row F39
(detector verifier, reject-file). An established violation → `[R-CNF-11]`: "a
verifier that has established any violation reports *nonconforming*"
→ **nonconforming**

Confidence: high.

## Q09 — experimental-range layer sub-record, MU = 1

0x8001 ≥ 0x8000 → experimental range (§10.2).

(a) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never
reject-file" → **reject-layer**

(b) §21.6: "an **experimental-range record type carrying MU = 1** … `[R-CNT-15]`
obliges the reader to reject, and `[R-CNF-02]` makes the file conforming all the
same, since the prohibition on publishing experimental values binds a writer's
conduct and not the bytes." → **yes**

(c) §2.3: *cannot establish* is available "when a record carries MUST_UNDERSTAND = 1
with a type it does not implement (§21.6)", and it "is available only to a
traversal that established no violation" — which holds here.
→ **cannot establish**

Confidence: high.

## Q10 — declined metadata decode plus L28

Smallest permitted bound: `[R-MTA-09]` "a bound of its own choosing, no smaller
than §21.9's user-metadata guarantee" = 16 MiB. A 20 MiB document exceeds it.

The layer declares entry_count = 0 with crc_of_crc_array = 0x00000001 — register
row L28, `[R-CNT-23]`: "a nonzero crc_of_crc_array with entry_count = 0 — as a
validity error at layer scope", detector reader. That is an established violation.

(a) `[R-CNF-11]`: "An established violation takes priority" → **nonconforming**
(b) `[R-MTA-09]`: "the decline is not a finding that the file is nonconforming and
a verifier MUST NOT report it as one" → **no** (it is reported as an unchecked
requirement, not as nonconformance)

Confidence: high.

## Q11 — segment CRC mismatch mid-request

(a) `[R-IDX-04]`: "any mismatch or cross-check failure (`[R-CNT-17]`) is
reject-layer" → **reject-layer**

(b) §2.4 reject-layer: "The outcome is prospective: it bars further service from
the layer, and does not retroactively invalidate content already returned under
§19.2's validation timing"; `[R-RDR-04]` step 8: "the bar is prospective, so values
the reader has already returned … stand" → **no**

(c) `[R-RDR-04]` step 8: an index-chain failure "bars the request's remaining
entries and all further service from the layer" → **no**

Confidence: high.

## Q12 — fill-only commit

(a) `[R-LIF-02]` step 1: "begin writing at exactly F"; steps 2 appends nothing
here (shape (c) of §20.3's example: "A change confined to the directory —
clearing a slab declaration, renaming a layer, changing a channel's fill value.
Only the directory is re-emitted.") → **4096**

(b) Directory [4096, 4396); step 5 "append the pad to the next 64-byte boundary":
next boundary is 4416 → **20**

(c) Trailer [4416, 4480); committed_file_length = new end = **4480** (multiple of
64 ✓)

(d) "generation one greater than the prior trailer's" → **8**

(e) `[R-WRT-05]` / `[R-WRT-04]` step 4: "A layer whose record alone changes keeps
its extent slot, pointing at the existing region" → **no**

*Oddity noted:* §14.5 obliges padding positions to encode the recorded fill, so a
fill change can strand stored edge tiles in violation of `[R-SER-05]`. The
document's own worked example nonetheless classifies a fill change as
directory-only, and (e) asks only about the index region, which is not re-emitted.

Confidence: high.

## Q13 — appender against minor 5 with ignore-lane bits

(a) `[R-CNT-26]`: "A writer SHOULD emit the lowest version_minor that defines every
feature present in the file — for a file expressible under this text, 0 — and an
appender the maximum of that floor and the prior trailer's minor." max(0, 5) = **5**
(the same logic §20.5 spells out for a compactor: it "does not lower the floor
beneath" an ignore-lane bit it does not implement).

(b) Trailer offset 12 is the u32 flags field (§6.2). `[R-CNT-08]`: "An updater MUST
copy forward unknown ignore-lane bits of the file it modifies and MUST NOT clear
them" (the flags = 0 rule binds "a writer creating a file under this text").
Bits 16|17 = 0x00030000, little-endian → **00000300**

(c) §21.6: "An ignore-lane flag bit (16–31) is set | Ignored; the file is
conforming"; "version_minor is higher than this text defines | Accepted".
`[R-CNF-02]` names §6.3's flags = 0 against a set ignore-lane bit as a conduct rule
that is expressly not a file-conformance violation → **yes**

Confidence: high.

## Q14 — zstd window 1024 for a 512-byte tile

`[R-COD-06]`: writers "MUST NOT declare a window size exceeding the tile's decoded
size; a reader MUST treat either as a validity error at tile scope, both being
header-checkable." Window_Size 1024 > 512.

(a) **reject-tile**
(b) **T21** — "Codec 3 (zstd) and the frame declares a window size larger than the
tile's decoded size", detector reader, detected at tile use.

Consistent with §17.2's note: below 1 KiB decoded, "A tile … is therefore encodable
under codec 3 only as a single-segment frame" — Single_Segment_Flag is clear here,
so the file is nonconforming exactly as T21 records. Every other listed property
(magic, no dict ID, no checksum flag, absent FCS, exact decode, exact consumption,
matching entry crc) clears T17–T20, T22, T24, T25 and T1.

Confidence: high.

## Q15 — empty layer-record names

File 1 — both name fields are the byte `00`, both within inline_length. §19.1 step 4:
"Uniqueness is decided first, and over the raw name bytes whether or not each name
is itself well-formed … so two layers whose name fields are byte-identical are a
duplicate even when neither name is valid." `[R-ENC-15]`: "a duplicate layer name is
a file-scope error (reject-file)".
→ **reject-file, F6**

File 2 — the two name fields differ (`00` vs `01 61`), so no duplicate. The first
layer record's name has length prefix 0, violating `[R-ENC-12]`'s non-empty rule at
layer scope.
→ **reject-layer, L6**

Confidence: high (File 1: the F6 row explicitly requires only that both name fields
be "obtainable within their records' inline_length", which holds; the §19.1
"uniqueness is decided first" clause exists precisely for this case).
