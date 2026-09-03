# Round 29 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4697 lines, read in full).
Local computation: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/quiz-answerer/qa_calc.py`
plus two inline `python3` heredocs (no file written) that re-read only that same spec file.

## CRC implementation validation

Before trusting any CRC number I validated my CRC-32C against every check value the
document itself publishes:

- §4.5 check vector: CRC-32C("123456789") = 0xE3069283 ✓ ; CRC-32C(zero bytes) = 0x00000000 ✓
- Appendix A trailer: CRC over trailer [0,60) = 0x402F157E, stored `7E 15 2F 40` ✓
- §7.4 worked example: CRC over 80 sentinel bytes = 0x80A34955 ✓ ; crc_of_crc_array = 0xC4EE982E ✓
- §15.4 constant: CRC of 2^16 sentinel entries = 0xEECB3BB2 ✓

All four reproduce. Numbers below rest on that implementation.

## Search-method note

The document is hard-wrapped and blockquotes wrap with `> `. Every phrase check I ran was
against a whitespace-normalised copy with `\n> ` stripped, and I ran a deliberately absent
control string (`ZZZ-not-present-control`) in the same batch, which correctly missed. No
conclusion below rests on an unvalidated zero.

---

## Q01 — 73, 101, 192

Layer record inline payload field widths, §7.4's table, packed in table order with no padding
(`[R-CNT-18]`: "fields are packed in table order with no alignment or padding between them"):

| Field | bytes |
|---|---|
| name `q` (u8 len + 1 byte) | 2 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| A u64 | 8 |
| S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| C u16 | 2 |
| 1 dimension entry: name(1+1) + extent u64 + tile extent u64 | 18 |
| 1 channel entry: name(1+1) + type u16 + fill(1 len + 1 byte) | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |

2 + 34 + 18 + 6 + 13 = **73**. Cross-checked against §7.4's worked example, which itemises
"4 + 34 bytes, the dimension entry 18, the channel entry 12, and the trailing fixed fields
13 — 81 exactly": same decomposition, name 2 instead of 4 and channel entry 6 instead of 12.

Extent 0 ⇒ grid count ⌈0/1⌉ = 0 (§11.2, `[R-GEO-03]`; §11.1 "at Eᵢ = 0 the grid count is 0
and the layer addresses no tile"). Interleaved ⇒ addressed-tile count = N = 0, so
entry_count = 0, extent slot (0,0), crc_of_crc_array = 0 (`[R-CNT-17]`, `[R-CNT-23]`).
No tile-index region and no stored tiles exist.

Directory = one record: 24-byte header (§7.2) + 73 inline + 4-byte terminal CRC (§7.1) =
**101**.

Placement: `[R-CNT-06]` fixes dir_offset ≥ 16; `[R-LIF-02]`'s creation path writes the front
block then begins at offset 16, and step 2 has nothing to append. So dir_offset = 16,
directory occupies [16, 117). Step 5 appends "the pad to the next 64-byte boundary" → 128,
then the 64-byte trailer at [128, 192). committed_file_length = **192**, a multiple of 64,
and dir_offset + dir_length = 117 ≤ F − 64 = 128 ✓.

## Q02 — 07dc6d9a

Trailer offsets [60,64) hold the trailer CRC: "CRC-32C over trailer bytes [0, 60)" (§6.2
table, `[R-CNT-06]`), "stored as a little-endian u32" (`[R-ENC-09]`).

Bytes [0,60):
`8a4e5241540d0a1a 0100 0200 00000000 1000000000000000 0010000000000000 8010000000000000 0100fecaefbeadde 000000000000000000000000`

(dir_length 4096 = 0x1000 → `00 10 00…`; F 4224 = 0x1080 → `80 10 00…`;
file_id 0xDEADBEEFCAFE0001 LE → `01 00 FE CA EF BE AD DE`.)

CRC-32C = 0x9A6DDC07 → stored little-endian, in file order: **07 dc 6d 9a**.

## Q03 — eeff, 2

Planar + bool channel ⇒ §14.3 packed plane. G = (⌈5/3⌉, ⌈5/3⌉) = (2,2); P = 3·3 = 9;
decoded size = ⌈9/8⌉ = 2 bytes.

Tile (1,1) covers y,x ∈ [3,6). Real positions need coord < 5 ⇒ u ∈ {0,1} on both axes.
In-tile ordinal = u_y·T_x + u_x = u_y·3 + u_x (`[R-GEO-06]`), so real ordinals are
0, 1, 3, 4 → false, true, true, false. Padding-position ordinals 2, 5, 6, 7, 8 must each
carry the channel's fill bit (§14.5, `[R-SER-05]`: "the fill bit in a packed plane"),
fill = 0x01 = true. P mod 8 = 1, so byte 1's bits 1–7 are pad bits and also carry the fill
bit (`[R-SER-05]`: "Every pad bit (§14.3) MUST carry the plane's channel's fill bit").

Bit k mod 8 of byte k div 8, LSB-first:
byte 0 bits 0..7 = 0,1,1,1,0,1,1,1 → 0xEE; byte 1 = all ones → 0xFF. Image = **eeff**.

Codec 1: `[R-COD-04]` — "A non-sentinel index entry's length therefore MUST equal the tile's
decoded size" — so length = **2**.

## Q04 — 143, 2860, 102060

G = (⌈100/32⌉, ⌈200/64⌉, ⌈300/128⌉) = (4, 4, 3); N = 48.
Tile coords (99 div 32, 199 div 64, 299 div 128) = (3, 3, 2).
s = 3·(4·3) + 3·3 + 2 = 47 (`[R-GEO-06]`).
Channel `c` has index 2; planar disk ordinal = c·N + s = 2·48 + 47 = **143**.
Index entry at region byte 20·k (§15.1, `[R-IDX-01]`) = 20·143 = **2860**.
In-tile position (99 mod 32, 199 mod 64, 299 mod 128) = (3, 7, 43);
in-tile ordinal = 3·(64·128) + 7·128 + 43 = 24576 + 896 + 43 = 25515.
Planar numeric offset of value k = k·Bᶜ (§14.2 table) = 25515·4 = **102060**.

## Q05 — 176, 4, 69

G = (⌈10/4⌉, ⌈10/4⌉) = (3,3); N = 9; P = 16.
Q = ΣBᵢ = 2 (int16) + 1 (bool, "element size 1 in the arithmetic below", §14.2) + 8 (float64)
= 11. Interleaved decoded size = P·Q = **176**.
Tile coords (5 div 4, 6 div 4) = (1,1); s = 1·3 + 1 = 4; interleaved disk ordinal = s = **4**.
In-tile (1,2) → ordinal 1·4 + 2 = 6. F^v = 2 + 1 = 3. Offset = u·Q + Fᶜ = 6·11 + 3 = **69**
(§14.2: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ").

## Q06 — 1310724, 3a173c06

G = 512/2 = 256 each; N = 65536; interleaved ⇒ entry_count = 65536.
`[R-CNT-17]`: extent_length = 65536×20 + ⌈65536/2¹⁶⌉×4 = 1,310,720 + 4 = **1310724**.
One segment, exactly 2¹⁶ entries, all sentinel ⇒ its CRC is §15.4's constant 0xEECB3BB2,
stored little-endian `b2 3b cb ee`. crc_of_crc_array is "CRC-32C over the index's
segment-CRC array" (§7.4) = CRC-32C(`b2 3b cb ee`) = **0x3A173C06** → `3a173c06`.
(Stored byte order would be `06 3c 17 3a`; the question asks for the u32 value.)

## Q07 — 56, 116, 55, 48

§21.1: "Instances within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written."

Mechanical count (script splits each register row's Instances cell on `;`, `—` = 1):
§21.2 = 56 over 35 rows; §21.3 = 116 over 49 rows; §21.4 = 55 over 26 rows;
§21.5 = 48 over 10 rows. Totals 120 rows / 275 instances, which matches §21.8's
"120 conditions over 275 instances" exactly — an independent check on the count.

## Q08 — 2, 44, 1

Gen 2 geometry: E = 2, T = 2 ⇒ G = 1, N = 1. Planar ⇒ entry_count = C·N = 2·1 = **2**
(`[R-GEO-03]`, `[R-CNT-17]`).
extent_length = 2×20 + ⌈2/2¹⁶⌉×4 = 40 + 4 = **44**.
The tile carrying x = 0 and x = 1 is s = 0; channel `q` has index 1; disk ordinal =
c·N + s = 1·1 + 0 = 1, and "The entry for the tile with disk ordinal k is the k-th entry"
(`[R-IDX-01]`), so the 0-based position is **1**.

Permissibility check: the shrink drops the t=1 tiles out of the addressed set, which §20.3
says "is not itself such an alteration"; the surviving tile's decoded size, offsets, types
and padding set are unchanged; the planar-ordinal bar "does not reach a shrink either".

## Q09 — R4, ignore-record

Encoding byte 0x02 = zstd. Every carried-over frame constraint is satisfied except the
content-size field: §18.2 — "The frame's content-size field … MAY be present, and when
present it MUST equal the byte length of the decoded document. A mismatch is one of the
frame constraints R4 registers, not a failure to decode under R3: the bytes decode, and
what is wrong is what the header said about them."

Declared 512 vs decoded 500 ⇒ **R4** (instance: "the content-size field declared larger than
the decoded length, top-level extent"). §21.5's outcome for every row is **ignore-record**.

## Q10 — conforming, nonconforming

File A, byte 0x9A ≥ 0x80: experimental range of the metadata-encoding space (§10.2). §21.6:
"A user-metadata record declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming … No document rule attaches at such an encoding, so
a verifier certifies, reporting the record it ignored." Verdict **conforming**.

File B, byte 0x05: reserved range 3–0x7F. §21.5 R1 registers "encoding 0, or a
reserved-range value (3-0x7F)" as a violation, and §21.5's preamble: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as violations." An
established violation forces **nonconforming** (`[R-CNF-11]`).

## Q11 — permitted, permitted, barred, permitted

N = ⌈4/2⌉ = 2; ordinals: `a` 0–1, `b` 2–3, `c` 4–5; only `b`'s two tiles stored.
Governing text (§20.3): "a commit MUST NOT change the channel declarations in a way that
alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation
this commit supersedes … Appending a channel, or removing the last, re-indexes nothing and
moves no ordinal at all … The test is the effect on a stored tile, not the shape of the edit."

- (i) append `d`: `b` stays index 1, ordinals 2–3. No §14 change (planar tile size P·Bᶜ is
  per-channel). **permitted**
- (ii) remove `c` (the last): re-indexes nothing; `b` stays index 1, ordinals 2–3.
  **permitted**
- (iii) remove `a`: `b` re-indexes to 0, ordinals 0–1 — moves stored tiles. **barred**
- (iv) exchange `a` and `c` → (`c`,`b`,`a`): `b` keeps index 1 and ordinals 2–3; only `a`
  and `c` move, and the superseded generation stored no tile for either. **permitted**
  (this is the spec's own "moves only the ordinals of channels the superseded generation
  stored no tile for alters nothing this bars").

## Q12 — permitted, barred, permitted, barred

Interleaved, N = 1, P = 4, Q = 1, decoded size 4, fill 0x00. The §14 bar (§20.3 step 4) and
its carve-out govern.

- (i) 00 01 02 00, shrink 4→3: x = 3 becomes a padding position, and its stored byte already
  holds the fill — "a new padding position whose stored byte already holds the fill
  `[R-SER-05]` fixes is not what this bars". P = ∏Tᵢ = 4 unchanged, so decoded size and every
  offset are unchanged. **permitted**
- (ii) 00 01 02 03, shrink 4→3: the new padding position holds 0x03 ≠ fill, altering what
  §14.5 fixes for a tile stored in the superseded generation. **barred**
- (iii) 00 01 02 03, shrink 4→0: grid count falls to 0, the tile leaves the addressed set —
  "a tile the new state does not address carries no §14 obligation and its extent becomes
  slack". No padding position arises. **permitted** (the "produce a new file instead" clause
  is a SHOULD, not a bar).
- (iv) retype uint8 → int8 while the layer stores a tile carrying that channel: "changing it
  is such a change wherever the layer stores a tile that carries that channel … The test is
  on the declared types and not on the values a tile happens to hold". **barred**

## Q13 — c, a, b, a, b

1. `[R-ENC-06]`: §21.7 names it explicitly — "`[R-ENC-06]`'s fixed field widths are not a
   state a file can be in … Nothing is omitted from the register on its account, there being
   no condition to omit." → **c**
2. Undisclosed zstd dictionary with Dictionary_ID 0: §17.2 "Dictionary use the header does
   not disclose is not detectable by inspection"; §21.7 lists "an undisclosed compression
   dictionary (`[R-COD-06]`)" among what no check detects. → **a**
3. Padding position not carrying the recorded fill: registered as T4 (§21.4), detector
   verifier. → **b**
4. Mis-strided filter 2 with no padding position and no bool channel: T26's own text —
   "a wrong stride with no such structural constraint is undetectable, §21.7". → **a**
5. Interleaved bool byte at a real position that is neither 0x00 nor 0x01: registered as T2
   (§21.4). → **b**

## Q14 — no violation, L44

Generation 1: G_y = ⌈0/65536⌉ = 0 ⇒ N = 0, addressed-tile count 0, so entry_count 0,
extent slot (0,0) and crc_of_crc_array 0 are all consistent (`[R-CNT-17]`, `[R-CNT-23]`,
`[R-GEO-02]`). The lz4 cap is quantified over addressed tiles — §17.2's Note: "a layer that
addresses none — any dimension extent 0 … satisfies it whatever its tile shape declares, and
codec 4 is conforming there." The designated products are still checked: P = 2³² and
P·Q = 2³⁵ = 34,359,738,368, far below 2⁶³ − 1, so no L2. ⇒ **no violation**.

Generation 2: E_y = 1 ⇒ G_y = 1, N = 1, one addressed tile of decoded size P·Q = 2³⁵ =
34,359,738,368 > 0x7E000000 = 2,113,929,216. §20.3 names this exact case: a growth is
permitted "provided the grown geometry stays within every bound the layer's own declarations
impose, `[R-COD-07]`'s lz4 decoded-size cap among them (L44)". ⇒ **L44** (instance
"interleaved P·Q").

Caveat recorded: taken hyper-literally, "changes nothing else" would leave entry_count at 0
against a geometry-derived count of 1, which would additionally exhibit L21. The question
asks for one label and the scenario is built out of the §17.2/§20.3 passages that name L44,
so L44 is the answer; L21 is the only competing reading and it depends on the hypothetical's
wording, not on any ambiguity in the specification.

## Q15 — reject-layer, cannot establish

Type 0x8123 ≥ 0x8000 is the experimental range (§10.2), so emitting it is not a
file-conformance violation (`[R-CNF-02]`, `[R-EXT-03]`, §21.6). Flags MU = 1, PE = 1 match
what a writer may emit (`[R-CNT-12]` bars only MU = 1 with PE = 0).

Reader outcome: `[R-CNT-18]` — "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader MUST NOT reject the file for it". §21.6
confirms: "the same type as a layer sub-record is reject-layer and never a ground to refuse
the file". ⇒ **reject-layer**.

Verifier verdict: §2.3 lists as a cannot-establish ground the case "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and "*cannot establish* is
available only to a traversal that established no violation" — which holds, the file being
conforming. ⇒ **cannot establish**.
