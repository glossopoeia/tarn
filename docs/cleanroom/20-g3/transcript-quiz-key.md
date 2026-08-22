# Round 20 — quiz KEY transcript

**Access.** Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole document, in five `sed` ranges). No other file read, no directory listing, no git,
no web, no conformance/ or docs/. Local Python only (CRC-32C + integer arithmetic),
reading no files. Scratch scripts written by me under the scratchpad.

**CRC implementation validated** before use against all five check values the document
itself states:
- CRC-32C("123456789") = 0xE3069283 ✓ (§4.5)
- CRC-32C(zero bytes) = 0x00000000 ✓ (§4.5)
- 4 sentinel entries (80 B) → 0x80A34955 ✓ (§7.4 example)
- CRC over `55 49 A3 80` → 0xC4EE982E ✓ (§7.4 example)
- 2¹⁶ sentinel entries → 0xEECB3BB2 ✓ (§15.4 / `[R-IDX-05]`)
- Appendix A trailer [0,60) → 0xE00938D2, bytes `d2 38 09 e0` ✓

---

## Q01 — inline_length and extent_length for layer `flux`

**Inline payload field widths** (§7.4 table, packed in table order, "no alignment or
padding between them"):

| field | bytes |
|---|---|
| name `flux` (u8 len + 4) | 5 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| dim `y` (1+1 + 8 + 8) | 18 |
| dim `x` (1+1 + 8 + 8) | 18 |
| chan `u` float64 (1+1 + 2 + 1+8) | 13 |
| chan `v` int16 (1+1 + 2 + 1+2) | 7 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| sub-records | 0 |
| **total** | **108** |

Cross-checked against §7.4's worked example, which decomposes its 81 bytes as
"Name and the nine scalars from layout through channel count occupy 4 + 34 bytes, the
dimension entry 18, the channel entry 12, and the trailing fixed fields 13". Here the
name is 5 and the nine scalars are the same 34 → 39; dims 36; channels 13 + 7 = 20;
trailing 13. 39+36+20+13 = **108**. Fill lengths are the types' element sizes
(§12.1: float64 = 8, int16 = 2), forced by `[R-CNT-23]`.

**Extent length.** Grid counts (§11.2, `[R-GEO-03]`): G_y = ⌈300/128⌉ = 3,
G_x = ⌈500/128⌉ = 4 → N = 12. Layout is **planar**, so the addressed-tile count is
C·N = 2·12 = **24**, and `[R-CNT-17]` makes entry_count = 24.

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 24×20 + 1×4 = 480 + 4 = **484**.

Declarations are consistent: A = 0 with S = 4 does not trip `[R-CNT-16]` (which bars
A ≠ 0 *and* S ≠ 0), and A_slab = 4096 is a power of two in 1…2⁶² as `[R-CNT-23]`
requires when S ≠ 0.

**Answer: a=108 b=484**

---

## Q02 — the segment-CRC array and crc_of_crc_array of an all-sentinel layer

Interleaved, rank 1, `t` E=300 T=128 → G = ⌈300/128⌉ = 3, N = 3. Interleaved →
addressed-tile count = N = **3** = entry_count (§11.2, `[R-CNT-17]`).

Segments (§15.4): ⌈3/2¹⁶⌉ = 1, so the segment CRC array is 4 bytes. Segment 0 covers
entries [0, min(2¹⁶, 3)) = all three, and the CRC is "over exactly those entries' bytes
as stored — the final partial segment's CRC covers only its actual bytes." So it is
CRC-32C over 60 bytes, each entry the sentinel `FF ×16 00 ×4` (§15.2, `[R-IDX-02]`).

`[R-IDX-05]`'s 0xEECB3BB2 constant is explicitly unavailable here: it licenses only a
**full** segment ("one covering exactly 2¹⁶ entries"), and "a partial segment's CRC MUST
be computed."

Computed: CRC-32C(60 sentinel bytes) = 0xD171D122 → stored little-endian (`[R-ENC-09]`)
as `22 d1 71 d1`.

crc_of_crc_array (§7.4, §8.1) = CRC-32C over the segment-CRC array as stored, i.e. over
those 4 bytes = 0x34C74AFB → `fb 4a c7 34`.

**Answer: a=22 d1 71 d1  b=fb 4a c7 34**

---

## Q03 — stored bytes of a filtered edge tile, and its entry crc

Geometry: rank 1, E = 3, T = 2 → G = 2, N = 2. Tile ordinal 1 covers x ∈ {2, 3};
x = 2 is real, x = 3 is a **padding position** (§11.3, coordinate ≥ E).

P = ∏Tᵢ = 2. Interleaved with C = 2 → sample stride Q = B_a + B_b = 1 + 2 = 3, and the
decoded size is P·Q = 6 (§14.2, `[R-SER-02]`).

Value sequence (`[R-SER-01]`, interleaved, sample-major): value k is channel (k mod C)
at in-tile ordinal k div C.
- k=0 → `a` at ordinal 0 (x=2) = 0x11 → `11`
- k=1 → `b` at ordinal 0 (x=2) = 0x2233 → `33 22` (little-endian)
- k=2 → `a` at ordinal 1 (x=3, padding) = fill 0x09 → `09`  (`[R-SER-05]`)
- k=3 → `b` at ordinal 1 (padding) = fill 0xBEEF → `ef be`  (`[R-SER-05]`)

Decoded tile image = `11 33 22 09 ef be` (6 bytes ✓).

Filter 2 = byte-shuffle (`[R-COD-10]`): stride s = Q = 3 for an interleaved tile;
L = 6, n = L/s = 2. "byte i of group j at offset i·n + j":
group0 = 11 33 22, group1 = 09 ef be →
offset0=11, offset1=09, offset2=33, offset3=ef, offset4=22, offset5=be.
Filtered image = `11 09 33 ef 22 be`.

Codec 1 = none (`[R-COD-04]`): "The stored bytes are the filtered image verbatim", and
the entry's length must equal the decoded size (6 ✓).

So the tile's complete stored bytes = **`11 09 33 ef 22 be`**.

Entry crc (§15.1, §8.1) = CRC-32C of the *stored* bytes = 0x7E07273F → stored
little-endian as `3f 27 07 7e`.

**Answer: a=11 09 33 ef 22 be  b=3f 27 07 7e**

---

## Q04 — decoded tile image of a packed planar bool plane

G_r = ⌈4/5⌉ = 1, G_c = ⌈3/3⌉ = 1 → N = 1, one channel → one addressed tile.
P = ∏Tᵢ = 5·3 = 15. Planar + bool → §14.3 packed plane, decoded size ⌈15/8⌉ = **2 bytes**.

In-tile ordinal (§11.4, permanent row-major): k = u₀·T₁ + u₁ = u₀·3 + u₁.
Real positions are u₀ ∈ 0…3, u₁ ∈ 0…2 (E = (4,3)); u₀ = 4 is entirely padding
(ordinals 12, 13, 14).

Bits (value k at bit k mod 8 of byte k div 8, LSB-first, `[R-SER-03]`):
- k = 1 ↔ coordinate (0,1) → **true** (1)
- all other real k (0, 2…11) → false (0)
- k = 12, 13, 14 padding → must carry the channel's fill = 0x01 → 1 (`[R-SER-05]`)
- P mod 8 = 7, so bit 7 of byte 1 is the single **pad bit**, which "MUST carry the
  plane's channel's fill bit" → 1 (`[R-SER-05]`, §14.3)

Bit string k=0…14: `0 1 0 0 0 0 0 0 0 0 0 0 1 1 1`

byte 0 = bit1 set = 0x02.
byte 1 = bits 4,5,6 (k=12,13,14) + pad bit 7 = 0x10|0x20|0x40|0x80 = 0xF0.

**Answer: 02 f0**

---

## Q05 — spatial tile ordinal and in-tile byte offset

G = (⌈10/3⌉, ⌈9/4⌉, ⌈5/2⌉) = (4, 3, 3).
Coordinate (8,5,3): tᵢ = xᵢ div Tᵢ = (2, 1, 1); uᵢ = xᵢ mod Tᵢ = (2, 1, 1).

Spatial tile ordinal (`[R-GEO-06]`, linearization 1): s = Σ tᵢ·∏_{j>i} Gⱼ
= 2·(3·3) + 1·(3) + 1 = 18 + 3 + 1 = **22**.

In-tile sample ordinal: u = Σ uᵢ·∏_{j>i} Tⱼ = 2·(4·2) + 1·2 + 1 = 16 + 2 + 1 = 19.

Interleaved element sizes (§12.1): a int32 = 4, b **bool = 1** (§14.2: "a bool value —
interleaved layers only … as a single byte, with element size 1 in the arithmetic
below"), c float16 = 2. Q = 4+1+2 = 7; F_c = Σ_{j<2} Bⱼ = 4+1 = 5.

§14.2: "channel c's value at in-tile ordinal u sits at byte u·Q + Fᶜ"
= 19·7 + 5 = 133 + 5 = **138**.

**Answer: a=22 b=138**

---

## Q06 — offsets inside a planar tile-index region

G_y = ⌈256/1⌉ = 256, G_x = 256 → N = 65,536. C = 2, planar → entry_count = C·N = 131,072.

Coordinate (100, 200) with T = (1,1): t = (100, 200);
s = t_y·G_x + t_x = 100·256 + 200 = 25,800.
Channel `q` is index 1 → disk ordinal = c·N + s = 65,536 + 25,800 = **91,336**
(`[R-GEO-06]`, channel-major).

(a) §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region byte
20·k" → 20 × 91,336 = **1,826,720**.

(b) Region layout (§15.1): `[entry array: entry_count × 20][segment CRC array:
⌈entry_count/2¹⁶⌉ × 4]`, "with no padding anywhere inside the region." Entry array =
131,072 × 20 = 2,621,440 bytes, so the CRC array begins at region byte 2,621,440.
Segments = ⌈131,072/65,536⌉ = 2. Entry 91,336 lies in segment ⌊91,336/65,536⌋ = 1
(§15.4: segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))), and "the s-th
u32 of the segment CRC array" is at 2,621,440 + 4·1 = **2,621,444**.

**Answer: a=1826720 b=2621444**

---

## Q07 — new trailer CRC and slack after one no-op commit

`[R-LIF-02]`: (1) begin at exactly F = 128; (2) nothing appended; (3) new complete
directory at [128, 132) — given; (4) barrier; (5) "append the pad to the next 64-byte
boundary … and the new trailer, with generation one greater than the prior trailer's and
committed_file_length equal to the new end".

Directory ends at 132 → pad to 192 (60 bytes) → trailer at [192, 256) → new F = 256
(multiple of 64 ✓). generation = 1 + 1 = 2. file_id unchanged (`[R-LIF-03]`: "the file_id
chosen at creation"; `[R-WRT-04]` step 6: "the same file_id"). dir_offset = 128,
dir_length = 4, version_minor 0 and flags 0 as stated, reserved zero.

Trailer bytes [0, 60):
```
8A 4E 52 41 54 0D 0A 1A   magic
01 00                     version_major 1
00 00                     version_minor 0
00 00 00 00               flags 0
02 00 00 00 00 00 00 00   generation 2
80 00 00 00 00 00 00 00   dir_offset 128
04 00 00 00 00 00 00 00   dir_length 4
00 01 00 00 00 00 00 00   committed_file_length 256
EF CD AB 89 67 45 23 01   file_id 0x0123456789ABCDEF
00 00 00 00               reserved
```
CRC-32C = 0x8740D5C5 → stored little-endian at [60, 64) as **`c5 d5 40 87`**.

**Slack.** `[R-LIF-08]`/`[R-CNT-02]`: the live committed state's claimants are the front
block [0,16) = 16 B, the live directory [128,132) = 4 B, and the live trailer
[192,256) = 64 B. Zero records → no record extents, no tile-index regions, no
stored-tile extents. Claimed = 84. "Every byte the live state does not claim is slack"
(`[R-CNT-21]`): 256 − 84 = **172**.

Sanity: [16,128) = 112 bytes (the superseded directory, pad and trailer of generation 1)
plus the new pre-trailer pad [132,192) = 60 bytes → 172 ✓. The walk completes, so the
total is exact, not partial.

**Answer: a=c5 d5 40 87  b=172**

---

## Q08 — the trailer validation order and the version gate

§6.2 `[R-CNT-06]`: "A reader MUST validate, **in order**: the trailer magic; the trailer
CRC; the version gate (§6.3) … and then, those gates passed, MUST validate all of the
following…". §21.2's preamble restates it: "§6.2 puts the version gate ahead of every
check but the trailer magic and the trailer CRC".

(a) The magic is correct, so the first failing check is the second one: the u32 at
trailer offset 60 does not equal CRC-32C over trailer bytes [0, 60) — register row F14,
`[R-CNT-06]` (R-CNT-20, R-ENC-09). That is the single condition reported.

(b) "Any failure is reject-file" (`[R-CNT-06]`); F14's outcome is reject-file (§21.2).

(c) **No.** The CRC gate precedes the version gate and its failure is terminal. Note
this is why §21.2 says F14 is one of the four rows that "do reach" a foreign-major file:
the CRC is checked before the major is consulted at all.

(d) Second file: version_major 7 in a major-1-only reader → `[R-CNT-07]`: "A reader MUST
reject-file when version_major is 0 (invalid) or is a major it does not implement" →
**reject-file**. Is that a finding of nonconformance? **No.** §2.3 `[R-CNF-02]`: "a file
declaring another major is neither conforming nor nonconforming under it: a reader
refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a
finding about its bytes." §21.6 lists it as one of two "conforming files a reader
nevertheless refuses", and it is "Neither … a register row".

**Answer: a=trailer CRC mismatch (u32 at trailer offset 60 ≠ CRC-32C over [0,60)) b=reject-file c=no d=reject-file, no**

---

## Q09 — an experimental-range MU=1 sub-record

(a) `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is **reject-layer**".

(b) Same sentence: "and where the file is otherwise conforming a reader MUST NOT reject
the file for it — on a nonconforming file `[R-CNF-12]`'s licence to reject on any
detected violation is untouched". The stipulation says everything else is well-formed and
(see (c)) conforming, so the licence does not open. **No.**

§21.6 confirms the scoping: "The qualifier is load-bearing — the same type as a layer
sub-record is reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
the top-level case is a file a reader refuses".

(c) **Conforming.** Type 0x8001 is in the experimental range (§10.2: record type ≥ 0x8000).
`[R-CNT-15]`: "a record type from the experimental range is conforming (§10.3's
prohibition binds the writer's conduct, not the bytes, `[R-CNF-02]`)". MU = 1 with PE = 1
is permitted (only MU = 1 with PE = 0 is barred, `[R-CNT-12]`). Extent slot (0,0) "means
no extent" and is valid (`[R-CNT-13]`); inline_length 0 is unconstrained for an
unassigned type, whose payload `[R-CNT-15]` leaves opaque. §2.3 anticipates exactly this
file: a conforming file may carry "a type it does not implement with
MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from the
experimental range".

**Answer: a=reject-layer b=no c=conforming**

---

## Q10 — a reserved-range top-level record with MU = 0

(a) **Nonconforming.** §21.2 F36: "A top-level record carries a type value from the
reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is
a violation whatever its MU bit." `[R-CNT-15]`: "one from the reserved range is a value
this specification has not assigned — emitting it is a violation".

(b) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
**ignore-record**. … Readers of both apply the MU rule above unchanged." §21.6 likewise:
"a *reserved*-range type is read the same way, but emitting one is a violation (F36, L25)".

(c) **verifier.** `[R-CNT-15]`: "a verifier MUST treat a reserved-range record type as a
validity error at the record's governing scope"; F36's Detector cell is *verifier*,
Detected *certification*.

**Answer: a=nonconforming b=ignore-record c=verifier**

---

## Q11 — a compactor's output trailer

(a) `[R-WRT-06]`: "The output trailer MUST copy the input's unknown ignore-lane flag bits
forward, in place of the flags = 0 §6.3 requires of a file created under this text
(`[R-CNT-08]`)." §6.3 states the same: "A compactor, though its output is a new file,
carries the input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0". Bits 16 and 18 are ignore-lane (bits 16–31) and unimplemented, so both carry;
no incompat bit is set. flags = 0x00050000, stored little-endian (`[R-ENC-01]`,
`[R-ENC-09]`) as **`00 00 05 00`**.

(b) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and **generation 1**: a
compacted file is a whole-file rewrite under a new file_id by definition". → **1**.

(c) **No.** Same rule: the fresh file_id is "a new draw under §9.3's randomness advice,
**not merely a value compared against the input's**", and "reusing the input's would
break the (file_id, range) cache contract of `[R-LIF-03]`, since relocation puts
different bytes at the same ranges." Carrying the input's own file_id is precisely what
is barred.

(Note: version_minor is not asked; §20.5 would put it at ≥ the input's 4 here, since the
output carries carried ignore-lane bits the compactor does not implement.)

**Answer: a=00 00 05 00  b=1  c=no**

---

## Q12 — two compactor inputs

**FILE A — refuse.** The entry has offset = 8 < 16, non-sentinel. §15.3's table:
"offset < 16 (non-sentinel) | *structural*: reject-tile — the front block is never
payload" (register row T8). §20.5 walks this case out explicitly:

> "Regenerating a region means classifying every entry in it: a sentinel is re-emitted
> unchanged, and every other entry is re-pointed to where its stored extent now lies. An
> entry §15.3 classifies reject-tile on a structural ground is neither — `[R-IDX-03]`
> gives it no stored extent for a re-pointing to target — so regenerating the region
> cannot proceed without meeting it, and the violation is thereafter one the compactor
> has detected. `[R-WRT-06]` then obliges refusal: the compactor can neither reproduce
> the entry nor invent a replacement, and no drop is available, a tile-index entry being
> no record §20.4's table licenses dropping."

So: **refuse**.

**FILE B — carry.** Type 0x0100 is reserved-range and unassigned → F36, a violation, but
with **Detector = verifier, Detected = certification**. The compactor is a reader, not a
verifier: §2.3 "a violation whose assigned detector is the verifier imposes no reader
obligation"; `[R-WRT-09]` fixes the compactor's verification depth as "the open (§19.1),
each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and each
relocated extent's checksum, including every stored tile's entry crc" — the reserved-range
type value is in none of them, and §19.1's record walk applies only the MU gate
(`[R-CNT-15]`), which with MU = 0 yields ignore-record, not a failure.

§20.5's refusal clause is conditioned on detection — "MUST NOT emit a file carrying a
violation **it has detected**" — and §20.5's own opening states the contrary case: "a
violation latent in a structure it carries forward verbatim travels into its output
(`[R-WRT-01]`) — its verification depth is `[R-WRT-09]`'s". §20.5's closing paragraph
draws exactly this line: `[R-WRT-09]`'s reach "bounds how far a compactor goes looking,
not what it owes on what regenerating the region has already put in front of it." Nothing
puts the type value in front of it.

So compaction is permitted and carrying the record forward is permitted → **carry**.

*Competing reading, recorded.* MU = 0 / PE = 0 does make a drop available ("A compactor
MAY drop it whenever it rewrites the file", §20.4), and a compactor that *does* notice
the reserved range must then drop or refuse. But `drop` as the question defines it —
"only if the offending record is absent from the output" — asserts an obligation the text
does not impose on a compactor that has not detected the violation, and dropping is a MAY,
never a MUST. I implement `carry`, with a SHOULD-report of the anomaly.

**Answer: A=refuse B=carry**

---

## Q13 — verdict with one violation and one undecidable requirement

(a) The reserved flag bit 5 on a top-level non-layer record is F26 (`[R-CNT-12]`:
"a verifier MUST treat a nonzero reserved flag bit … as a validity error at the record's
governing scope"), an **established** violation. §2.3 `[R-CNF-11]`: "An established
violation takes priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and *cannot establish*
is available only to a traversal that established no violation." → **nonconforming**.

(b) **Yes.** §2.3: "A verifier MUST report each requirement it was unable to check on a
capability or resource ground, naming the requirement and the ground, **whichever of the
three verdicts it reports**; that per-requirement report constrains the report and not
the verdict." The declined decode is a listed cannot-establish ground ("when it declines
a layer's or a tile's decode on resource grounds and so cannot check §14's
decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`)") — here it is
reported without changing the verdict.

(c) **No.** §21.9's 256 MiB decoded-tile figure is a **minimum guarantee**, not a cap:
"The table below states minimum guarantees, not caps" and "A file exceeding any of these
remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest
scope whose declarations exceed what it can serve" (`[R-ERR-03]`, `[R-ERR-04]`).

**Answer: a=nonconforming b=yes c=no**

---

## Q14 — a zero-extent lz4 layer, then grown

(a) **Conforming.** G_t = ⌈0/16384⌉ = 0, G_x = ⌈1000/16384⌉ = 1 → N = 0. `[R-GEO-02]`:
"A dimension with extent 0 is valid: its grid count is 0, the layer has zero addressed
tiles". `[R-COD-07]`'s cap "Writers MUST NOT declare this codec for a layer **any of
whose addressed tiles'** decoded size exceeds 0x7E000000" is vacuous, and §17.2's Note
says so outright: "The cap is quantified over the layer's *addressed* tiles, so a layer
that addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it whatever
its tile shape declares, and codec 4 is conforming there."

The Note's companion check does apply: "`[R-ENC-04]`'s overflow rule carries no such
quantifier … so P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."
P = 16384·16384 = 268,435,456; Q = 8; P·Q = 2,147,483,648 = 2³¹, far under 2⁶³ − 1. Fine.

(b) `[R-CNT-17]`/§7.4: entry_count "equals the addressed-tile count". Interleaved →
N = 0. **entry_count = 0** (and consequently extent slot (0,0) and crc_of_crc_array = 0,
`[R-CNT-23]`).

(c) **Nonconforming.** With E_t = 1, G_t = 1 → N = 1: one addressed tile, decoded size
P·Q = 2,147,483,648 > 0x7E000000 = 2,113,929,216. §17.2's Note: "The escape is not
durable: a later commit that grows an extent addresses tiles, and the same declarations
are then measured against the cap." §20.3 step 4 names this exact case: an extent may
grow "provided the grown geometry stays within every bound the layer's own declarations
impose, `[R-COD-07]`'s lz4 decoded-size cap among them (**L44**), which an empty layer
escapes only because that cap is quantified over addressed tiles."

(d) `[R-COD-07]`: "a reader MUST treat such a declaration as a validity error at layer
scope, checkable from declarations alone"; L44's outcome is reject-layer, detected at
layer access. → **reject-layer**.

(Consistency note: the stipulated appender is not a conforming one, since `[R-CNF-05]`
requires it to emit only conforming files. That does not change what FILE B *is* —
conformance is a pure predicate on bytes, `[R-CNF-02]`.)

**Answer: a=conforming b=0 c=nonconforming d=reject-layer**

---

## Q15 — four file-conformance judgments

**(i) nonconforming.** `[R-MTA-05]`: "Writers MUST serialize object members, **at every
nesting depth**, in ascending order of their keys' UTF-8 bytes. … unsorted members do not
make a document unreadable: **the file is nonconforming**, a verifier MUST report it, and
readers process the document unchanged." Register row F27 (detector verifier, outcome
reject-file). §21.6's closing text confirms it was moved *out* of the non-violation table.

**(ii) conforming.** §18.4's table scopes `tarn.created` to **file** only, so a
layer-scope occurrence is out of scope. `[R-MTA-07]`: "A reader MUST ignore a standardized
key found outside its listed scope … rather than rejecting the document. **Neither
placement nor value shape bears on validity: the file stays conforming**." §21.6 lists it:
"A standardized key (§18.4) appears outside its listed scope … | Conforming".

**(iii) conforming.** 0x80000000 is bit 31 → the **ignore lane** (bits 16–31). §6.3
`[R-CNT-08]`: "a set ignore-lane bit is **not a file-conformance violation** — such bits
are defined by later minor versions, and files carrying them are conforming files this
text's readers ignore." §2.3 names it as a conduct-only writer obligation. §21.6: "An
ignore-lane flag bit (16–31) is set | Ignored; the file is conforming".

**(iv) nonconforming.** The inline payload byte is the encoding field (§18.2). 0x05 falls
in **3 through 0x7F = reserved**, not the experimental range (≥ 0x80). §21.5 R1: "A
user-metadata record declares a document encoding of 0, or a reserved-range value
(3-0x7F)" — a registered violation, outcome ignore-record. §21.5's preamble: "Encoding 0
and a reserved-range value are unassigned too, and R1 registers both as violations: what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding byte's own
value set (`[R-MTA-03]`)." Only ≥ 0x80 would have been the §21.6 non-violation. A valid
extent slot and verifying CRC do not save it — R1's outcome bounds a reader's blast
radius and "never makes the file conforming (`[R-CNF-12]`)".

**Answer: i=nonconforming ii=conforming iii=conforming iv=nonconforming**

---

## Underdetermination summary

No question was scored underdetermined. The one I came closest to flagging is **Q12 B**,
where the text's obligation turns on whether the compactor "has detected" a
verifier-assigned violation; both readings are recorded above, and I implement `carry`
because §20.5 conditions its refusal/drop machinery on detection and `[R-WRT-09]` does not
reach the record-type value set. It is the finding most worth comparing against the blind
answerer.
