# Round 31 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read in full, lines 1–4790, via the Read tool; plus one whitespace-normalising
Python probe over the same file to confirm decisive phrases across hard wraps and
`> ` blockquote prefixes, with a deliberate negative control that missed).

Scratch files I wrote (mine alone):
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/quiz-answerer/qa_calc_r31.py`

CRC-32C implementation self-checked against §4.5's two check vectors
(`CRC32C("123456789") = 0xE3069283`, `CRC32C("") = 0x00000000`) **and**
independently against Appendix A's trailer CRC `0x402F157E` — reproduced exactly,
which validates both the polynomial parameters and my trailer field assembly.

---

## Q01 — layer record inline_length

§7.4 field order and widths. Name `grid` = 1 (u8 prefix) + 4 = 5.
The nine scalars layout→C: layout u8 1, linearization u16 2, codec u16 2,
filter u16 2, A u64 8, S u64 8, A_slab u64 8, rank u8 1, C u16 2 = **34**
(cross-checked against §7.4's worked example: "Name and the nine scalars from
layout through channel count occupy 4 + 34 bytes").

Dimension entries (name u8len+bytes · extent u64 · tile extent u64):
`y` = 1+1+8+8 = 18; `x` = 18. Total 36.

Channel entries (name u8len+bytes · type u16 · fill u8len+bytes; fill length =
the type's element size, `[R-CNT-23]`):
- `m`, type 1 = bool, element size 1 → 1+1 + 2 + (1+1) = 6
- `v`, type 13 = float64, element size 8 → 1+1 + 2 + (1+8) = 13
Total 19.

Trailing fixed fields: index_encoding u8 1 + entry_count u64 8 +
crc_of_crc_array u32 4 = 13.

5 + 34 + 36 + 19 + 13 = **107**. No sub-records, so the payload ends there.

(b) inline_length is a u32 (§4.2, §7.2) at header offset 4, little-endian
(`[R-ENC-01]`): 107 = 0x0000006B → `6b 00 00 00`.

Note: layout 2/planar, index_encoding, entry_count value etc. do not change the
payload's *length*, only its content — the question's other declarations are
inert for (a) and (b).

## Q02 — planar geometry, entry_count, extent_length, disk ordinal

G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3 (§11.2). N = ∏G = 9.
Planar addressed-tile count = C·N = 3·9 = **27** → entry_count = 27
(`[R-CNT-17]`, `[R-GEO-03]`).

extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 = 27·20 + 1·4 = **544**
(`[R-CNT-17]`).

Coordinate (7,3): t_y = 7 div 4 = 1, t_x = 3 div 4 = 0.
s = Σ tᵢ·∏_{j>i} Gⱼ = 1·3 + 0 = 3.
Channel `c` has index 2 (0-based, declared order). Disk ordinal = c·N + s
= 2·9 + 3 = **21** (`[R-GEO-06]`).

Entry byte offset in the region = 20·k = 20·21 = **420** (`[R-IDX-01]`: "The entry
for the tile with disk ordinal k is the k-th entry, at region byte 20·k").

## Q03 — trailer CRC of a 128-byte file

Assembled trailer bytes [0,60) per §6.2's table:
`8A 4E 52 41 54 0D 0A 1A | 01 00 | 03 00 | 00 00 00 00 | 10 00×8 | 04 00×8 |
80 00×8 | 08 07 F6 E5 D4 C3 B2 A1 | 00×12` — 60 bytes.

CRC-32C = 0x2FAF8508, stored little-endian at [124,128): **`08 85 af 2f`**.

Validation of method: the same code over Appendix A's trailer (identical but
version_minor 0 and file_id 0x0123456789ABCDEF) yields 0x402F157E, exactly the
value Appendix A records.

## Q04 — smallest committed_file_length after one commit

Layer record inline payload: name `L` 2 + scalars 34 + one dimension entry
(`d`) 18 + one channel entry (`c`, bool, element size 1) 6 + trailing 13 = **73**.
Record = 24-byte header + 73 = 97 bytes (§7.2).
Directory region = record sequence + terminal CRC-32C = 97 + 4 = **101** (§7.1).

`[R-LIF-02]` step 1: begin writing at exactly F = 128; `[R-LIF-01]` freezes
[0,128). So dir_offset ≥ 128; minimum 128, directory ends at 229.
`[R-CNT-06]`: dir_offset + dir_length ≤ F − 64 → F ≥ 293; F must be a multiple
of 64 → smallest F = **320** (trailer at [256,320), 27 pad bytes at [229,256)
per step 5's pad-to-next-64-boundary).

Consistency: 320 − 128 = 192 ≥ 128, satisfying `[R-LIF-02]`'s strict increase.

Geometry check on the declared layer: E=0 → G=0 → N=0 → interleaved
addressed-tile count 0, so entry_count 0, extent (0,0), crc_of_crc_array 0 all
conform (`[R-GEO-02]`, `[R-CNT-17]`, `[R-CNT-23]`).

## Q05 — verifier verdicts on two foreign-major files

§2.3: the three verdicts are *conforming*, *nonconforming*, *cannot establish*.

`[R-CNF-13]`: a condition reaches a foreign-major file only where the invariant
it violates is one `[R-CNT-24]` fixes in every major. §21.2 derives exactly
F8, F14, F6 and both F1 instances — "and no other row".

**File A.** Magic ✓, trailer CRC ✓, front block ✓ — every reaching condition
satisfied. dir_offset = 8 violates F9, which does **not** reach: "it is not
assessed against a file declaring another major, no violation of it is
established there". No violation established; version_major 3 is a major it
does not implement — an explicitly named capability ground. §2.3: "*cannot
establish* is available only to a traversal that established no violation."
→ **cannot establish**.

**File B.** The u32 at trailer offset 60 ≠ CRC-32C of [0,60): F14, which
reaches. §2.3: "A verifier that establishes such a failure reports
*nonconforming*, whatever major the file declares and whether or not it
implements that major." Note §6.2's order puts the trailer CRC *before* the
version gate. → **nonconforming**.

## Q06 — zstd user-metadata frame whose FCS is 200, document 199 bytes

§18.2 (`[R-MTA-09]`): "The frame's content-size field ... MAY be present, and
when present it MUST equal the byte length of the decoded document. A mismatch
is one of the frame constraints R4 registers, not a failure to decode under R3."
Everything else about the extent is clean (CRC ✓, single frame ✓, no dict, no
content-checksum flag, no residue), and the decoded JSON satisfies §18.2's
content rules, so no R5–R10 row applies. R3 is expressly displaced.

(a) **ignore-record** — §21.5's outcome for every row there, and `[R-CNT-25]`'s
quarantine ("notwithstanding the owning-scope mapping of `[R-CNF-08]`").
(b) **R4** (instance: "the content-size field declared larger than the decoded
length, top-level extent").
(c) **no** — §21.5: "Every row here is a violation all the same: the outcome
bounds a reader's blast radius and never makes the file conforming."

## Q07 — flags 0x00050000 (ignore-lane bits 16 and 18)

(a) Compactor: `[R-WRT-06]` / `[R-CNT-08]` — "A compactor ... carries the
input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0, and sets no other." Output flags = 0x00050000, at trailer offset 12
as a little-endian u32 → **`00 00 05 00`**.

(b) Creator, no input: "a writer creating a file under this text MUST write
flags = 0" → **`00 00 00 00`**.

(c) `[R-CNT-08]`: an updater "MUST copy forward unknown ignore-lane bits of the
file it modifies, MUST NOT clear them, and MUST NOT set any other: no writer
under this text originates an ignore-lane bit". → **no**.

## Q08 — how many of the four commits §20.3 bars

Two bars: the **§14 bar** (no change altering what §14 fixes for a tile stored
in the superseded generation) and the **planar-ordinal bar** (no planar channel
change moving a stored tile's disk ordinal).

(i) planar (a,b,c), `a` stored, remove `c`. Ordinal bar: "Appending a channel,
or removing the last, re-indexes nothing and moves no ordinal at all." §14 bar:
a planar plane's decoded size is P·Bᶜ / ⌈P/8⌉ and its shuffle stride is the
channel's element size — the channel *count* enters neither. `a`'s stored tiles
are untouched; `c`'s de-addressed tiles were never stored. **Not barred.**

(ii) planar (a,b,c), `c` stored, remove `a`. "inserting or removing one moves
every channel after the affected position. Either is such a change wherever the
layer stores a tile for a channel that moved." `c` moves from ordinals [2N,3N)
to [N,2N) and stores a tile. **Barred.**

(iii) interleaved (u uint8, v uint16), stores a tile, remove `v`. "removing one
of its channels changes Q and so is the §14 bar's subject wherever the layer
stores a tile." Q: 3 → 1, decoded size P·Q and every value offset change.
**Barred.**

(iv) planar, one bool channel, filter 1 → 2, stores a tile. §17.3: "for a packed
boolean plane s = 1 and the filter is the identity." The §14 bar's carve-out:
"a change that leaves every one of those tiles' stored bytes meaning exactly
what they meant — a filter whose mandated stride makes it the identity
(`[R-COD-10]`) ... — is not what this bars." **Not barred.**
(Appendix G item 5 confirms the identity reading.)

→ **2**.

## Q09 — how many of four records the updater may drop

§20.4's persistence table, plus "only the authoritative source of the flags
differs":
1. 0x8001 (unimplemented), MU=0/PE=0 → stored flags authoritative → "Retain
   byte-identical, or drop it ... an updater MAY drop the record in any commit
   it is otherwise free to make — one whose only effect is the drop included."
   **Droppable.**
2. 0x0002 — a type §7.3 registers, so "the registry's fixed flags govern rather
   than the stored ones ... both registered types carry PE = 1, so neither can
   be dropped." Not droppable.
3. 0x0001 — same, PE = 1. Not droppable.
4. 0x8002 (unimplemented), MU=0/PE=1 → "Retain byte-identical, extent content
   unmodified." Not droppable.

→ **1**.

## Q10 — slack after an L18 rejection of layer B

`[R-CNT-21]`: "where the rejection is one the walk itself established, L18's
overlap ... among them, the claimants it had already enumerated are discarded
with the layer" and "A partial total is F less the bytes claimed by the
claimants the walk did enumerate".

Enumerated claimants: front signature block 16 + live trailer 64 (§9.7: "The
front signature block at [0, 16) and the live trailer at [F − 64, F) are claimed
by the walk as well, being members of the live committed state") + directory 100
+ user-metadata extent 64 + layer A index 200 + layer A tiles 500 + 300 = 1244.
Layer B's index (100) and tile (1000) are discarded with the layer.

8192 − 1244 = **6948**, reported as **partial** ("a scope-level rejection ends
that scope's enumeration ... the verifier MUST report the total as partial").

(Alternative reading considered and rejected: excluding the front block and
trailer would give 7028, but §9.7 states they are claimed by the walk.)

## Q11 — interleaved decoded size and value offset

P = ∏Tᵢ = 3·4 = 12. Q = ΣBᵢ = 1 (uint8) + 8 (float64) + 2 (int16) = 11.
Decoded size (interleaved) = P·Q = **132** (`[R-SER-02]`).

Coordinate (26,13): u_y = 26 mod 3 = 2, u_x = 13 mod 4 = 1;
in-tile ordinal u = 2·4 + 1 = 9 (`[R-GEO-06]`).
Fʳ = B_p + B_q = 1 + 8 = 9.
§14.2: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ"
= 9·11 + 9 = **108**.

## Q12 — packed planar bool tile image

Planar bool → §14.3 packing. P = ∏Tᵢ = 13. Decoded size = ⌈13/8⌉ = 2 bytes.
E = 10 < T = 13, so positions with ordinals 10, 11, 12 are **padding positions**
(§11.3), and `[R-SER-05]` fixes each to the channel's fill bit — fill 0x01 = true
= bit 1. P mod 8 = 5, so bits 5–7 of byte 1 are **pad bits**, also fill = 1.

Byte 0 (values 0–7 in bits 0–7): T,F,T,T,F,F,F,T → bits 0,2,3,7 set = 0x8D.
Byte 1: bit0 = value 8 = false = 0; bit1 = value 9 = true = 1;
bits 2,3,4 = padding positions 10,11,12 = fill 1; bits 5,6,7 = pad bits = fill 1
→ 0b1111_1110 = 0xFE.

→ **`8d fe`**. (Method cross-checked against §14.3's own example, which gives
`55 fd` for P = 10 with fill true.)

## Q13 — interleaved bool byte 0x02

E = T = 2 on both axes, so no padding positions; ordinal 2 is a real position,
which puts this at T2 rather than T4.

(a) `[R-SER-08]`: "A reader that does not reject the tile and returns the value
— whether or not it detected the violation — MUST report 0x00 as false and every
other byte as true." → **true**.
(b) "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved
bool value. Any other byte makes the file nonconforming" → **no**.
(c) "its assigned detector is the verifier, for which it is a validity error at
tile scope" → **verifier** (§2.3's class name: conforming verifier).

## Q14 — two layer records with empty (length-prefix-0) name fields

Both name fields are the single byte 0x00, hence byte-identical, and both lie
within inline_length. §19.1 step 4: "Uniqueness is decided first, and over the
raw name bytes whether or not each name is itself well-formed ... so two layers
whose name fields are byte-identical are a duplicate even when neither name is
valid." That is F4 (`[R-ENC-15]`), whose outcome is file scope: "A duplicate
layer name is a validity error at file scope, here, at open."

(a) **reject-file**. (L5's reject-layer for each empty name also holds, but
uniqueness is decided first and reject-file is what the reader takes.)
(b) F4's *Detected* cell reads `open`; §21.1: "Detection points name §19.2's
reader tiers — open, layer access, tile use, extent use." → **open**.

## Q15 — zero-extent lz4 layer with a 2 GiB nominal tile

G_y = ⌈0/16384⌉ = 0, G_x = ⌈1000000/16384⌉ = 62; N = 0; interleaved
addressed-tile count = N = 0. entry_count 0, extent (0,0), crc_of_crc_array 0
all consistent (`[R-CNT-17]`, `[R-CNT-23]`).

(a) `[R-COD-07]` bars codec 4 only "for a layer any of whose **addressed** tiles'
decoded size exceeds 0x7E000000" — vacuous at zero addressed tiles; §20.3 states
the same normatively: "`[R-COD-07]`'s lz4 decoded-size cap ... which an empty
layer escapes only because that cap is quantified over addressed tiles."
`[R-ENC-04]` is *not* so quantified, but P·Q = 2²⁸ · 8 = 2³¹ = 2,147,483,648,
far below 2⁶³ − 1, so no ceiling is breached. Every other declaration is in its
value set (layout 1, lin 1, filter 1, index_encoding 1, type 13, fill length 8,
A = S = A_slab = 0, rank 2, C 1, names valid and unique). → **no**.

(b) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed** tiles,
stored or not ... A layer addressing no tile (§11.2) therefore has no tile whose
decoded size the table bounds." So the 2 GiB figure exceeds no guarantee.
rank 2 ≤ 32, C 1 ≤ 4096, entry_count 0 ≤ 2³², 1 layer ≤ 65,536,
dir_length 200 ≤ 16 MiB, no metadata document, no zstd frame. Nothing exceeds a
guarantee, the file is conforming, and its major is one the reader implements
→ `[R-CNF-03]`'s acceptance duty applies. → **yes**.
