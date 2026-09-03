# Cleanroom round 29 — quiz keyer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read whole, via the Read tool, in four contiguous passes).

Tooling written (scratch dir `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/quiz-keyer/`):
- `crc_qk.py` — CRC-32C implementation + Q01–Q08 arithmetic.
- Two inline heredoc scripts (no files): register instance counter; wrap-safe
  phrase verifier.

**CRC implementation validated against the document's own check values before
any answer rested on it:**
- CRC-32C("123456789") = 0xE3069283 ✓ (§4.5)
- CRC-32C(zero bytes) = 0x00000000 ✓ (§4.5)
- CRC-32C of a full 2^16-sentinel segment = 0xEECB3BB2 ✓ (§15.4, Appendix B)
- §7.4 worked example: CRC over 80 sentinel bytes = 0x80A34955 ✓, and
  crc_of_crc_array over `55 49 A3 80` = 0xC4EE982E ✓

**Search discipline.** Every phrase search was run on a whitespace-normalised
copy of the file with leading `> ` blockquote markers stripped, so hard wraps
and blockquote wrapping cannot produce a false zero. A deliberate
never-present control string was included in the same batch and correctly
missed, proving the search could have succeeded.

---

## Q01 — 73,101,192

Layer record inline payload (§7.4 table, packed in table order, no padding):

| field | bytes |
|---|---|
| name `q` (u8 len + 1) | 2 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| slab alignment u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| 1 dim entry: name(1+1) + extent u64 + tile extent u64 | 18 |
| 1 chan entry: name(1+1) + type u16 + fill(1+1) | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |

Total **73**. Cross-checked against §7.4's own worked example, which decomposes
its 81-byte payload as "name and the nine scalars from layout through channel
count occupy 4 + 34 bytes, the dimension entry 18, the channel entry 12, and
the trailing fixed fields 13". My scalar block is the same 34, dim entry the
same 18, trailing the same 13; only name (2 vs 4) and channel entry (6 vs 12)
differ, as the shorter names and 1-byte fill require.

entry_count: E=0, T=1 → G = ⌈0/1⌉ = 0 (§11.2); N = ∏G = 0; interleaved →
addressed-tile count = N = 0 (`[R-GEO-03]`). So entry_count = 0, extent slot
(0, 0) and extent_length 0 (`[R-CNT-17]`), crc_of_crc_array = 0 (`[R-CNT-23]`).
No tile-index region and no stored tiles exist, so nothing but the directory
occupies the body.

dir_length: record sequence = 24-byte header (§7.2) + 73 = 97; plus the
region's terminal 4-byte CRC (§7.1) → **101**.

committed_file_length: `[R-CNT-06]` requires dir_offset ≥ 16; the smallest
permitted is 16, and nothing else needs body bytes. Directory occupies
[16, 117). `[R-LIF-02]` step 5 pads to the next 64-byte boundary (128) and
appends the 64-byte trailer → F = **192**. Independently forced by
`[R-CNT-06]`: F multiple of 64 and dir_offset + dir_length ≤ F − 64 →
117 ≤ F − 64 → F ≥ 181 → F = 192.

## Q02 — 07dc6d9a

§6.2 layout table: offset 60, size 4, "CRC-32C over trailer bytes [0, 60)",
stored little-endian (`[R-ENC-09]`).

Trailer [0,60) =
`8a4e5241540d0a1a 0100 0200 00000000 1000000000000000 0010000000000000 8010000000000000 0100fecaefbeadde 000000000000000000000000`

(4224 = 0x1080 → `80 10 00 …`; file_id 0xDEADBEEFCAFE0001 little-endian →
`01 00 FE CA EF BE AD DE`.)

CRC-32C = 0x9A6DDC07. The question asks for the bytes **in the order they
appear in the file**, i.e. the little-endian storage: `07 dc 6d 9a` →
**07dc6d9a**.

## Q03 — eeff,2

Planar + bool channel → §14.3 packed plane. P = ∏Tᵢ = 3·3 = 9; decoded size
⌈P/8⌉ = 2 bytes.

Tile (1,1) covers y∈[3,6), x∈[3,6); E=5 so y=5 and x=5 are padding. In-tile
ordinal = u_y·3 + u_x (§11.4, permanent row-major). Real ordinals are
0,1,3,4 (u_y,u_x ∈ {0,1}); ordinals 2,5,6,7,8 are padding positions.

`[R-SER-05]`: every padding position carries "the fill bit in a packed plane";
every pad bit carries "the plane's channel's fill bit". Fill = 0x01 = true = 1.
P mod 8 = 1, so byte 1 bits 1–7 are pad bits, all 1.

Bits, value k at bit k mod 8 of byte k div 8 (§14.3):
k: 0=F, 1=T, 2=pad→1, 3=T, 4=F, 5=pad→1, 6=pad→1, 7=pad→1 → byte 0 =
2+4+8+32+64+128 = 238 = 0xEE.
k=8 = pad→1 at bit 0; bits 1–7 pad bits = 1 → byte 1 = 0xFF.

Image = **eeff**.

length: codec 1, so `[R-COD-04]` — "a non-sentinel index entry's length
therefore MUST equal the tile's decoded size" — and filter 1 is the identity.
Length = **2**.

## Q04 — 143,2860,102060

G = (⌈100/32⌉, ⌈200/64⌉, ⌈300/128⌉) = (4, 4, 3); N = 48.
t = (99 div 32, 199 div 64, 299 div 128) = (3, 3, 2).
s = Σ tᵢ·∏_{j>i} Gⱼ = 3·12 + 3·3 + 2 = **47**.
Planar disk ordinal = c·N + s, c = 2 (`c` is third declared) → 2·48 + 47 = **143**.

Entry offset in the region: "the entry for the tile with disk ordinal k is the
k-th entry, at region byte 20·k" (`[R-IDX-01]`) → 20·143 = **2860**. (Entry
array precedes the segment CRC array, §15.1, so the region's first byte is
entry 0's.)

u = (99 mod 32, 199 mod 64, 299 mod 128) = (3, 7, 43); T = (32, 64, 128).
in-tile ordinal = 3·(64·128) + 7·128 + 43 = 24576 + 896 + 43 = 25515.
Planar numeric: "offset of value k = k · Bᶜ" (§14.2 table), Bᶜ = 4 →
25515·4 = **102060**.

## Q05 — 176,4,69

Q = ΣBᵢ = 2 (int16) + 1 (bool, "element size 1 in the arithmetic below") +
8 (float64) = 11. P = 4·4 = 16.
Interleaved decoded size = P·Q = **176**.
G = (⌈10/4⌉, ⌈10/4⌉) = (3,3). t = (5 div 4, 6 div 4) = (1,1).
s = 1·3 + 1 = 4; interleaved disk ordinal = s = **4**.
u = (1, 2); in-tile ordinal = 1·4 + 2 = 6. Fᶜ for `v` (c=2) = 2 + 1 = 3.
Offset = u·Q + Fᶜ = 6·11 + 3 = **69** (§14.2's closing sentence gives exactly
this form).

## Q06 — 1310724,3a173c06

G = (⌈512/2⌉, ⌈512/2⌉) = (256,256); N = 65536; interleaved → entry_count =
65536.
extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 (`[R-CNT-17]`)
= 1310720 + 1·4 = **1310724**.

The segment CRC array is one u32. Segment 0 covers entries
[0, min(65536, 65536)) = all 65536 — a **full** segment, all sentinels — so its
CRC is the constant `[R-IDX-05]` fixes, 0xEECB3BB2, stored little-endian as
`b2 3b cb ee`. crc_of_crc_array = CRC-32C over that 4-byte array (§7.4, §8.1)
= **0x3a173c06**. (Answer form asks for the u32 value, not stored order.)

## Q07 — 56,116,55,48

Rule applied: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is
written" (§21.1).

Counted by hand and then mechanically (splitting each Instances cell on `;`).
Both agree: §21.2 = 56 over 35 rows; §21.3 = 116 over 49; §21.4 = 55 over 26;
§21.5 = 48 over 10. Sum = 275 over 120 rows, which independently reproduces
§21.8's "120 conditions over 275 instances".

## Q08 — 2,44,1

Gen 2 geometry: E = 2, T = 2 → G = 1, N = 1; planar → addressed-tile count
= C·N = 2·1 = **2** = entry_count (`[R-CNT-17]`).
extent_length = 2×20 + ⌈2/2¹⁶⌉×4 = 40 + 4 = **44**.
`q` has channel index 1; the tile covering x = 0,1 is spatial ordinal 0; disk
ordinal = c·N + s = 1·1 + 0 = 1, and entry order is disk-ordinal order
(`[R-IDX-01]`) → 0-based position **1**.

Commit legality (not asked, but checked): the shrink alters nothing §14 fixes
for either prior-generation stored tile at s = 0 — same P, same decoded size,
no new padding position (x = 0,1 stay real). The tiles at s = 1 drop out of
the addressed set, which §20.3 says "is not itself such an alteration". The
planar-ordinal bar "does not reach a shrink either". Renumbering is expressly
contemplated: "a geometry change renumbers ordinals wherever `[R-GEO-06]`
moves them".

## Q09 — R4,ignore-record

Encoding byte 0x02 = zstd. The frame satisfies magic, single-frame, zero
Dictionary_ID, no content checksum, no trailing bytes. What is wrong is
Frame_Content_Size = 512 against a decoded document of 500 bytes. §18.2: "The
frame's content-size field … MAY be present, and when present it MUST equal
the byte length of the decoded document. A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3: the bytes decode,
and what is wrong is what the header said about them."

R4's own cell confirms the individuation: "the content-size field breaks its
constraint exactly when it is present and does not equal the decoded
document's byte length", instance "the content-size field declared larger than
the decoded length, top-level extent".

Outcome: §21.5's heading — "Outcome: ignore-record" — and `[R-MTA-09]`'s
closing "Any violation here is ignore-record". → **ignore-record**.

## Q10 — conforming,nonconforming

File A, encoding byte 0x9A = 154 ≥ 0x80 → experimental range (§10.2, §18.2).
§21.6: "A user-metadata record declares an experimental-range (≥ 0x80)
document encoding | Ignored (ignore-record); the file is conforming … No
document rule attaches at such an encoding, so a verifier certifies, reporting
the record it ignored". `[R-MTA-10]`: such a verifier "has no requirement it
is unable to check — the record is not among `[R-CNF-11]`'s cannot-establish
grounds, and certification is unaffected". → **conforming**.

File B, encoding byte 0x05 → reserved range 3–0x7F. §21.5's preamble:
"Encoding 0 and a reserved-range value are unassigned too, and R1 registers
both as violations: what `[R-MTA-10]` withdraws is the document's content
rules, never the encoding byte's own value set". R1 is a violation with
outcome ignore-record; §2.3: "a verifier that has established any violation
reports *nonconforming*". → **nonconforming**.

The ignore-record outcome bounds the reader's blast radius and does not make
the file conforming (§21.5: "Every row here is a violation all the same").

## Q11 — permitted,permitted,barred,permitted

Gen 1: N = 2; channels a=0, b=1, c=2; ordinals a→0,1; b→2,3; c→4,5. Stored:
ordinals 2 and 3 only.

Governing text (§20.3, the bar beside the §14 bar): "For a **planar** layer, a
commit MUST NOT change the channel declarations in a way that alters the disk
ordinal `[R-GEO-06]` assigns any tile the layer stores in the generation this
commit supersedes."

(i) append `d` after `c`: "Appending a channel, or removing the last,
re-indexes nothing and moves no ordinal at all". b stays at 2,3. Nothing §14
fixes for b's tiles changes (planar planes are per channel). → permitted.

(ii) remove `c` (the last): same sentence, "or removing the last". b stays at
2,3. → permitted.

(iii) remove `a` (the first): "inserting or removing one moves every channel
after the affected position." b becomes index 0, its stored tiles move to
ordinals 0,1. The layer stores tiles for b in the superseded generation. →
barred.

(iv) exchange `a` and `c` → order c,b,a: b keeps index 1, so ordinals 2,3 are
unchanged; a and c move but the superseded generation stored no tile for
either. "**The test is the effect on a stored tile, not the shape of the
edit**: a commit that moves only the ordinals of channels the superseded
generation stored no tile for alters nothing this bars." → permitted.

## Q12 — permitted,barred,permitted,barred

Gen 1: interleaved, C = 1 uint8, T = 4, E = 4 → G = 1, N = 1, P = 4, Q = 1,
decoded size 4. The one addressed tile is stored.

(i) image `00 01 02 00`, E → 3: G = ⌈3/4⌉ = 1, tile still addressed; x = 3
becomes a padding position, and `[R-SER-05]` fixes its content to the fill
0x00 — which the stored byte already holds. §20.3 carve-out: "a new padding
position whose stored byte already holds the fill `[R-SER-05]` fixes is not
one, so a shrink producing only those is permitted here exactly as it is
there." Decoded size unchanged (P = ∏Tᵢ). → permitted.

(ii) image `00 01 02 03`, E → 3: the new padding position holds 0x03 ≠ fill,
so the commit alters "the content `[R-SER-05]` fixes there" for a tile the
superseded generation stores. → barred.

(iii) image `00 01 02 03`, E → 0: G = ⌈0/4⌉ = 0, N = 0, the layer addresses no
tile (§11.2, `[R-GEO-02]`). §20.3: "Dropping a tile out of the addressed set
(§11.2's grid count falls) is not itself such an alteration — a tile the new
state does not address carries no §14 obligation and its extent becomes
slack". §11.1's rationale says the same. Nothing §14 fixes is altered. →
permitted. (The consequential entry_count → 0, slot (0,0),
crc_of_crc_array → 0 are obligations, not bars.)

(iv) sample type 6 → 2, extent unchanged: §20.3 — "A channel's declared
**sample type** is such a declaration, and changing it is such a change
wherever the layer stores a tile that carries that channel… **The test is on
the declared types and not on the values a tile happens to hold**". The layer
stores that tile. → barred.

## Q13 — c,a,b,a,b

1. `[R-ENC-06]`: §21.7 names it explicitly — "`[R-ENC-06]`'s fixed field
   widths are not a state a file can be in … Nothing is omitted from the
   register on its account, there being no condition to omit." → **c**.
2. Undisclosed zstd dictionary with Dictionary_ID zero: `[R-COD-06]` —
   "Dictionary use the header does not disclose is not detectable by
   inspection"; §18.2 calls it "an unwitnessed condition, exactly as
   `[R-COD-06]` has it for a tile (§21.7)". No register row. → **a**.
3. Padding position not holding the recorded fill: registered as T4 (§21.4),
   detector verifier, governing `[R-SER-05]`. → **b**.
4. Mis-strided filter 2 where the layer has no padding position and no bool
   channel: T26 covers only the case "where the resulting image breaks §14.5's
   padding content or `[R-SER-08]`'s bool bytes (a wrong stride with no such
   structural constraint is undetectable, §21.7)". Length is unchanged by the
   permutation, so no other obliged check separates it. → **a**.
5. Interleaved bool byte other than 0x00/0x01 at a real position: registered as
   T2 (§21.4), governing `[R-SER-08]`. → **b**.

## Q14 — no violation,L44

**(1) Generation 1.** G_y = ⌈0/65536⌉ = 0, G_x = ⌈4096/65536⌉ = 1, N = 0;
interleaved addressed-tile count = 0, so entry_count = 0, slot (0,0),
extent_length 0 and crc_of_crc_array 0 all satisfy `[R-CNT-17]`/`[R-CNT-23]`.
A zero extent is expressly valid (`[R-GEO-02]`), a tile extent may exceed its
dimension's extent (`[R-GEO-01]`), and codec 4 escapes its cap: "The cap is
quantified over the layer's *addressed* tiles, so a layer that addresses none —
any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile
shape declares, and codec 4 is conforming there."
`[R-ENC-04]`'s designated quantities are still formed and are all in domain:
P = 2³² , P·Q = 2³⁵, N = 0, N·P = 0, C·N = 0. → **no violation**.

**(2) Generation 2.** y: 0 → 1 makes G_y = 1, N = 1, so the layer now
addresses one tile of decoded size P·Q = 2³² · 8 = 2³⁵ = 34,359,738,368 bytes,
far above 0x7E000000 = 2,113,929,216. The same note continues: "The escape
ends exactly when the layer's addressed-tile count rises above 0 … and the
same declarations are then measured against the cap." §20.3 names the row for
exactly this transition: an extent may grow "provided the grown geometry stays
within every bound the layer's own declarations impose, `[R-COD-07]`'s lz4
decoded-size cap among them (L44), which an empty layer escapes only because
that cap is quantified over addressed tiles." → **L44**.

*Caveat recorded.* Read with maximum literalness, "changes nothing else"
leaves entry_count at 0 while the geometry-derived addressed-tile count is
now 1, which additionally exhibits **L21** (extent_length 0 stays consistent
with entry_count 0, so L22 does not fire). I answer L44 because it is the row
the specification itself names for this exact growth, and because on the
reading where the commit performs the index re-emission `[R-CNT-17]` obliges,
L44 is the *only* row exhibited. A reader who takes "changes nothing else"
to freeze entry_count would answer that the layer exhibits L21 as well.

## Q15 — reject-layer,cannot establish

Type 0x8123 ≥ 0x8000 → experimental range (§10.2). Emitting one is a
conduct violation only, not a bytes violation (`[R-CNF-02]`, §21.6), and the
question stipulates the file is conforming.

(1) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer, and
where the file is otherwise conforming a reader MUST NOT reject the file for
it". §21.6 reinforces: "the same type as a layer sub-record is reject-layer and
never a ground to refuse the file (`[R-CNT-18]`)". → **reject-layer**.

(2) §2.3 lists among the *cannot establish* grounds: "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)". The verifier
establishes no violation anywhere (the file is conforming), and *cannot
establish* "is available only to a traversal that established no violation".
→ **cannot establish**. (It must also report the requirement it could not
check and the ground.)

---

## Underdetermination summary

No question was scored `underdetermined`. Q14 carries a recorded caveat about
its own premise ("changes nothing else") rather than about the document; the
document itself is unambiguous that the grown layer exhibits L44.
