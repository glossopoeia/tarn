# Round 20 — quiz answerer transcript

**Access.** I read exactly one file: `spec/tarn.md` (4369 lines, read in full, in five
chunks). No other file, no directory listing, no git, no web. All computation ran in
Python over literals I typed by hand from the questions and from the spec text; no
script read any file. Scratch files written by me:
`scratchpad/round20/calc.py`, `scratchpad/round20/geo.py`, and this transcript.

**CRC harness validation.** Before trusting any computed checksum I reproduced four
constants the spec publishes: CRC-32C("123456789") = 0xE3069283 (§4.5), CRC-32C of
zero bytes = 0x00000000 (§4.5), CRC-32C of a full 2^16-entry all-sentinel segment =
0xEECB3BB2 (§15.4 / Appendix B), and — as an end-to-end check of both the segment
and crc_of_crc_array layers — §7.4's `sst` example: 0x80A34955 over 80 bytes of four
sentinel entries and 0xC4EE982E over the resulting 4-byte array. I also reproduced
Appendix A's trailer CRC 0xE00938D2 over its 60 trailer bytes, which validates my
trailer field packing as well as the CRC.

---

## Q01 — inline_length and extent_length of a planar rank-2 layer

**(a) inline_length.** §7.4's payload table, packed in table order with no padding
("fields are packed in table order with no alignment or padding between them",
`[R-CNT-18]`):

| field | bytes |
|---|---|
| name `flux` (u8 len + 4) | 5 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| slab alignment A_slab u64 | 8 |
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

5+1+2+2+2+8+8+8+1+2 = 39; +36 dims = 75; +20 channels = 95; +13 trailing = **108**.

Cross-check against §7.4's worked example, which sums the same way: "Name and the
nine scalars from layout through channel count occupy 4 + 34 bytes, the dimension
entry 18, the channel entry 12, and the trailing fixed fields 13 — 81 exactly."
There name is 4 bytes (len 3) and the channel is float32 (fill 4), giving 12; mine is
`flux` = 5 and float64 = 13 / int16 = 7. Fill length is the element size
(`[R-CNT-23]`: "fill length equals the type's element size"): float64 = 8, int16 = 2
(§12.1 table).

Note A = 0 with S = 4 is permitted — `[R-CNT-16]` bars only A ≠ 0 *and* S ≠ 0 — and
A_slab = 4096 is a power of two in 1 … 2^62, so no constraint bites.

**(b) extent_length.** Grid counts, §11.2: G_y = ceil(300/128) = 3, G_x =
ceil(500/128) = 4, so N = 12. Planar, so the addressed-tile count is C·N = 2·12 = 24
(`[R-GEO-03]`), and entry_count = 24 (`[R-CNT-17]`). Then `[R-CNT-17]`:
"extent_length MUST equal entry_count × 20 + ceil(entry_count / 2^16) × 4" =
24×20 + 1×4 = 480 + 4 = **484**.

**Answer: `a=108 b=484`.** Confidence high.

---

## Q02 — segment-CRC array and crc_of_crc_array of an all-sentinel rank-1 layer

G = ceil(300/128) = 3; interleaved, so entry_count = N = 3 (`[R-GEO-03]`). One
segment (ceil(3/2^16) = 1), so the segment CRC array is 4 bytes (§15.1).

No tile stored ⇒ all three entries are the sentinel, `FF ×16 00 ×4` (`[R-IDX-02]`).
The segment CRC is "the CRC-32C over exactly those entries' bytes as stored — the
final partial segment's CRC covers only its actual bytes" (`[R-IDX-04]`), i.e. over
60 bytes, **not** 0xEECB3BB2: `[R-IDX-05]` licenses that constant only for a **full**
segment of exactly 2^16 sentinel entries, and "a partial segment's CRC MUST be
computed."

CRC-32C(SENT×3) = 0xD171D122 → stored little-endian `22 d1 71 d1`.
crc_of_crc_array = CRC-32C over that 4-byte array = 0x34C74AFB → stored `fb 4a c7 34`.

**Answer: `a=22 d1 71 d1 b=fb 4a c7 34`.** Confidence high.

---

## Q03 — stored tile bytes and entry crc, interleaved + byte-shuffle + codec none

Geometry: G = ceil(3/2) = 2, N = 2, P = ∏T = 2. Tile ordinal 1 covers x ∈ {2, 3};
x = 2 is real (E = 3), x = 3 is a padding position (§11.3).

Value sequence, interleaved (`[R-SER-01]`): value k = channel (k mod C) at in-tile
ordinal k div C. Q = B_a + B_b = 1 + 2 = 3; decoded size P·Q = 6 (`[R-SER-02]`).
F_a = 0, F_b = 1.

- in-tile ordinal 0 (x = 2, real): a = 0x11 at byte 0; b = 0x2233 at bytes 1–2, LE = `33 22`.
- in-tile ordinal 1 (x = 3, padding): `[R-SER-05]` — "at every padding position, a
  writer MUST encode, for each channel the position carries, that channel's fill
  value". a = 0x09 at byte 3; b = 0xBEEF at bytes 4–5, LE = `ef be`.

Decoded tile image = `11 33 22 09 ef be`.

Filter 2 (byte-shuffle, `[R-COD-10]`): interleaved ⇒ stride s = Q = 3; L = 6, n = 2.
"the filtered image places byte i of group j at offset i · n + j". Groups: g0 =
`11 33 22`, g1 = `09 ef be`. Offsets 0..5 ← (i0j0, i0j1, i1j0, i1j1, i2j0, i2j1) =
`11 09 33 ef 22 be`. (I checked this rule against §17.3's own float32 example and
reproduced `00 00 00 00 00 00 80 00 40 3F 40 40` exactly.)

Codec 1: "The stored bytes are the filtered image verbatim" (`[R-COD-04]`), and the
entry length must equal the decoded size 6 — it does.

**(a)** stored bytes = `11 09 33 ef 22 be`.
**(b)** entry crc = CRC-32C of those stored bytes (§8.1: "Stored tile | the crc field
of its index entry | the tile's stored bytes" — i.e. bytes *as stored*, post-filter,
post-codec) = 0x7E07273F → stored `3f 27 07 7e`.

**Answer: `a=11 09 33 ef 22 be b=3f 27 07 7e`.** Confidence high.

---

## Q04 — decoded tile image of a packed planar bool plane

G_r = ceil(4/5) = 1, G_c = ceil(3/3) = 1, N = 1, C = 1 planar ⇒ 1 addressed tile.
P = T_r · T_c = 5·3 = 15. Planar bool ⇒ §14.3 packing: "value k occupies bit k mod 8
of byte k div 8 … and the decoded size is ceil(P/8) bytes" = 2 bytes.

In-tile ordinal (§11.4) = u_r · T_c + u_c = 3·u_r + u_c.

- true sample at (0, 1) → ordinal 1.
- all other real positions (u_r ∈ 0..3, u_c ∈ 0..2) false.
- padding positions: u_r = 4 (E_r = 4 < T_r = 5) with u_c = 0,1,2 → ordinals 12, 13, 14.
  `[R-SER-05]`: each carries the fill bit; fill byte 0x01 = true ⇒ bit 1.
- pad bits: P mod 8 = 7 ≠ 0, so bit 7 of byte 1 is a pad bit and "Every pad bit MUST
  carry the plane's channel's fill bit" (`[R-SER-05]`) ⇒ 1.

Bit vector (ordinal 0…14): 0 1 0 0 0 0 0 0 | 0 0 0 0 1 1 1, plus pad bit 7 = 1.
Byte 0 = bit1 set = 0x02. Byte 1 = bits 4,5,6 (values 12,13,14) + bit 7 (pad) =
0x70 | 0x80 = 0xF0.

**Answer: `02 f0`.** Confidence high. (Sanity: §14.3's own example, fill true, gives
`55 FD` — pad bits set — the same mechanism.)

---

## Q05 — spatial tile ordinal and in-tile byte offset

G = (ceil(10/3), ceil(9/4), ceil(5/2)) = (4, 3, 3).
Coordinate (8, 5, 3): t = (8 div 3, 5 div 4, 3 div 2) = (2, 1, 1);
u = (8 mod 3, 5 mod 4, 3 mod 2) = (2, 1, 1).

`[R-GEO-06]`: s = Σ t_i · ∏_{j>i} G_j = 2·(3·3) + 1·3 + 1 = 18 + 3 + 1 = **22**.

In-tile sample ordinal = Σ u_i · ∏_{j>i} T_j = 2·(4·2) + 1·2 + 1 = 16 + 2 + 1 = 19.

Interleaved byte offset (`[R-SER-02]`, and §14.2's closing sentence "channel c's value
at in-tile ordinal u sits at byte u · Q + F^c"): Q = 4 (int32) + 1 (bool, element size
1 in an interleaved tile) + 2 (float16) = 7; F_c for channel index 2 = 4 + 1 = 5.
Offset = 19·7 + 5 = 133 + 5 = **138**.

**Answer: `a=22 b=138`.** Confidence high.

---

## Q06 — offsets inside a planar tile-index region

G_y = G_x = 256 (tile extent 1 everywhere), N = 65,536. C = 2 planar ⇒ entry_count =
C·N = 131,072.

Spatial ordinal of tile (100, 200) = 100·256 + 200 = 25,800. Channel `q` is channel
index 1, so the disk ordinal is c·N + s = 65,536 + 25,800 = 91,336 (`[R-GEO-06]`).

**(a)** §15.1: "The entry for the tile with disk ordinal k is the k-th entry, at region
byte 20·k" ⇒ 20 × 91,336 = **1,826,720**.

**(b)** The entry array is entry_count × 20 = 2,621,440 bytes, immediately followed by
the segment CRC array "with no padding anywhere inside the region" (§15.1). Entry
91,336 lies in segment 91,336 div 65,536 = 1 (§15.4), and the s-th u32 of the array
starts at 2,621,440 + 1×4 = **2,621,444**.

**Answer: `a=1826720 b=2621444`.** Confidence high.

---

## Q07 — new trailer CRC and slack after a no-op commit

`[R-LIF-02]`: (1) begin writing at exactly F = 128; (2) nothing; (3) directory + CRC
= 4 bytes at [128, 132); (4) barrier; (5) "append the pad to the next 64-byte
boundary … and the new trailer, with generation one greater than the prior trailer's
and committed_file_length equal to the new end."

Pad: 132 → 192 (60 bytes). Trailer at [192, 256). New F = 256, a multiple of 64.
Fields: magic; version_major 1; version_minor 0; flags 0; generation 2; dir_offset
128; dir_length 4; committed_file_length 256; file_id 0x0123456789ABCDEF (a commit
carries the same file_id — `[R-LIF-03]`, `[R-WRT-04]` step 6); reserved zero.

Trailer bytes [0,60) =
`8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00 02 00 00 00 00 00 00 00 80 00 00 00
00 00 00 00 04 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 ef cd ab 89 67 45 23 01
00 00 00 00`

CRC-32C = 0x8740D5C5 → stored `c5 d5 40 87`.

**Slack.** §9.7 / `[R-CNT-21]`: the walk claims the front block [0,16), the live
directory [128,132), the live trailer [192,256), plus each record extent and each
non-sentinel stored extent — of which there are none. Claimed = 16 + 4 + 64 = 84.
F − 84 = 256 − 84 = **172**. Itemised: the superseded [16,128) = 112 (old dir, old
pad, old trailer) plus the new pre-trailer pad [132,192) = 60. The walk completes, so
the total is exact, not partial.

**Answer: `a=c5 d5 40 87 b=172`.** Confidence high.

---

## Q08 — trailer validation order and the version gate

§6.2: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the
version gate (§6.3)". §21.2's preamble confirms the ordering explicitly: "F8 and F1's
trailer-magic instance, F14's trailer CRC — the two checks §6.2 places before the
gate".

**(a)** Magic is correct, so the first failing check is the trailer CRC: the u32 at
trailer offset 60 does not equal CRC-32C of trailer bytes [0,60) — register row F14,
`[R-CNT-06]`.
**(b)** "Any failure is reject-file" (`[R-CNT-06]`) ⇒ **reject-file**.
**(c)** **No** — the CRC gate precedes the version gate and fails, so the reader never
reaches it.
**(d)** Second file: version_major 7 is a major this reader does not implement, so
`[R-CNT-07]` obliges **reject-file**. Is that a finding of nonconformance? **No** —
§2.3: "a file declaring another major is neither conforming nor nonconforming under
it: a reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
refusal is not a finding about its bytes." §21.6 repeats it: "In both the outcome
records a reader's capability, not a defect in the bytes."

**Answer: `a=trailer CRC mismatch (u32 at trailer offset 60 ≠ CRC-32C of trailer bytes
[0,60)) b=reject-file c=no d=reject-file, no`.** Confidence high.

---

## Q09 — experimental-range sub-record with MU = 1

**(a)** `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer".
⇒ **reject-layer**.
**(b)** Same sentence: "and where the file is otherwise conforming a reader MUST NOT
reject the file for it". The file is otherwise well-formed, so ⇒ **no**.
**(c)** `[R-CNT-15]`: "a record type from the experimental range is conforming (§10.3's
prohibition binds the writer's conduct, not the bytes, `[R-CNF-02]`)". §21.6 makes the
sub-record case explicit: "the same type as a layer sub-record is reject-layer and
never a ground to refuse the file (`[R-CNT-18]`)". Flags MU=1/PE=1 are a legal
combination (`[R-CNT-12]` bars only MU=1 with PE=0), and an unknown type's inline
payload is opaque. ⇒ **conforming**.

**Answer: `a=reject-layer b=no c=conforming`.** Confidence high.

---

## Q10 — reserved-range top-level record with MU = 0

**(a)** `[R-CNT-15]`: "one from the reserved range is a value this specification has not
assigned — emitting it is a violation". Register row F36. ⇒ **nonconforming**.
**(b)** Same rule: "An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
ignore-record … Readers of both apply the MU rule above unchanged." ⇒ **ignore-record**.
**(c)** F36's Detector cell is *verifier*, Detected *certification*: "a verifier MUST
treat a reserved-range record type as a validity error at the record's governing
scope". ⇒ **verifier**. (F35 — the MU = 1 specialization, detector *reader* — does not
apply here, MU = 0.)

**Answer: `a=nonconforming b=ignore-record c=verifier`.** Confidence high.

---

## Q11 — compactor output trailer

**(a)** `[R-WRT-06]`: "The output trailer MUST copy the input's unknown ignore-lane flag
bits forward, in place of the flags = 0 §6.3 requires of a file created under this
text". Bits 16 and 18 are ignore-lane, so flags = 0x00050000, little-endian
**`00 00 05 00`**.
**(b)** `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and generation 1".
⇒ **1**.
**(c)** Same sentence: "a new draw under §9.3's randomness advice, not merely a value
compared against the input's … reusing the input's would break the (file_id, range)
cache contract of `[R-LIF-03]`". ⇒ **no**.

(version_minor is a red herring here; it is only a SHOULD floor and not asked.)

**Answer: `a=00 00 05 00 b=1 c=no`.** Confidence high.

---

## Q12 — two compactor inputs

**FILE A.** offset 8 is < 16 on a non-sentinel entry ⇒ §15.3's row "offset < 16
(non-sentinel) | *structural*: reject-tile". §20.5 addresses precisely this:
"An entry §15.3 classifies reject-tile on a structural ground is neither — `[R-IDX-03]`
gives it no stored extent for a re-pointing to target — so regenerating the region
cannot proceed without meeting it, and the violation is thereafter one the compactor
has detected. `[R-WRT-06]` then obliges refusal: the compactor can neither reproduce
the entry nor invent a replacement, and no drop is available, a tile-index entry being
no record §20.4's table licenses dropping." ⇒ **refuse**.

**FILE B.** Reserved-range type 0x0100, MU = 0 / PE = 0. This *is* a violation (F36),
but its assigned detector is the *verifier*, and a compactor is a reader/updater, not
a verifier: §2.3 gives updaters "every reader obligation", and `[R-RDR-02]` says "a
violation whose assigned detector is the verifier … imposes no reader obligation".
`[R-WRT-09]` fixes the compactor's verification depth — the open, each retained layer's
record and full index chain, each relocated extent's checksum — none of which tests a
record type against the reserved range. `[R-WRT-06]`'s prohibition bites on "a
violation it has detected", and §20.5 states the converse outright: "a violation
latent in a structure it carries forward verbatim travels into its output
(`[R-WRT-01]`)". §20.4's MU=0/PE=0 row permits either disposal ("Retain
byte-identical, or drop it … A compactor MAY drop it whenever it rewrites the file"),
so dropping is licensed but not required. ⇒ **carry**.

*Competing reading for B, noted honestly:* if one holds that a compactor which
implements the registered type list thereby "has detected" that 0x0100 lies in
0x0003–0x7FFF, then `[R-WRT-06]`'s "MUST NOT emit a file carrying a violation it has
detected" fires and, drop being licensed here, the answer becomes `drop`. I reject it
because the spec assigns F36's detection to the verifier and never obliges a compactor
to make it; but the text does not say in so many words that a compactor must *not*
notice. I answer `carry` and would implement `carry`.

**Answer: `A=refuse B=carry`.** Confidence: A high, B medium.

---

## Q13 — verdict with one established violation plus an undecodable layer

The established violation is a reserved flag bit on a top-level non-layer record —
F26, `[R-CNT-12]`, detector verifier, outcome reject-file. It is a violation.

**(a)** §2.3: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*, however many requirements it was unable to
check, and *cannot establish* is available only to a traversal that established no
violation." ⇒ **nonconforming**.
**(b)** §2.3: "A verifier MUST report each requirement it was unable to check on a
capability or resource ground, naming the requirement and the ground, whichever of the
three verdicts it reports". ⇒ **yes**.
**(c)** §21.9's 256 MiB decoded-tile row is a *minimum guarantee*, not a cap:
"A file exceeding any of these remains conforming, and a reader MAY decline it"
(`[R-ERR-04]`). ⇒ **no**.

**Answer: `a=nonconforming b=yes c=no`.** Confidence high.

---

## Q14 — a zero-extent lz4 layer, then grown by one

**(a)** E_t = 0 ⇒ G_t = 0 ⇒ N = 0, addressed-tile count 0 (`[R-GEO-02]`, `[R-GEO-03]`).
§17.2's note on `[R-COD-07]`: "The cap is quantified over the layer's *addressed*
tiles, so a layer that addresses none — any dimension extent 0 — satisfies it whatever
its tile shape declares, and codec 4 is conforming there." The overflow rule still
applies without the quantifier: P = 16384·16384 = 2^28, Q = 8, P·Q = 2^31 — far below
2^63 − 1, so `[R-ENC-04]` is satisfied. entry_count 0 ⇒ extent slot (0,0) and
crc_of_crc_array 0, both consistent. ⇒ **conforming**.

**(b)** entry_count = the addressed-tile count = **0** (`[R-CNT-17]`, `[R-GEO-02]`:
"its grid count is 0, the layer has zero addressed tiles, its tile index has zero
entries").

**(c)** E_t = 1 ⇒ G_t = 1, G_x = ceil(1000/16384) = 1, N = 1: one addressed tile.
Decoded size, interleaved = P·Q = 268,435,456 × 8 = 2,147,483,648 bytes. The lz4 cap
0x7E000000 = 2,113,929,216. 2,147,483,648 > 2,113,929,216 by 33,554,432 bytes. So the
layer now declares codec 4 on a layer an addressed tile of which exceeds the cap —
`[R-COD-07]`, register row L44. §20.3 step 4 anticipates exactly this: growth is
permitted only "provided the grown geometry stays within every bound the layer's own
declarations impose, `[R-COD-07]`'s lz4 decoded-size cap among them (L44), which an
empty layer escapes only because that cap is quantified over addressed tiles."
⇒ **nonconforming**.

**(d)** `[R-COD-07]`: "a reader MUST treat such a declaration as a validity error at
layer scope, checkable from declarations alone" ⇒ **reject-layer**.

**Answer: `a=conforming b=0 c=nonconforming d=reject-layer`.** Confidence high.

---

## Q15 — four conformance verdicts

**(i) unsorted members in a nested object.** `[R-MTA-05]`: "Writers MUST serialize
object members, at every nesting depth, in ascending order of their keys' UTF-8
bytes… unsorted members do not make a document unreadable: the file is nonconforming,
a verifier MUST report it, and readers process the document unchanged." Register row
F27. ⇒ **nonconforming**.

**(ii) `tarn.created` at layer scope.** §18.4's table scopes `tarn.created` to *file*
only. §21.6: "A standardized key (§18.4) appears outside its listed scope, or carries
a value whose shape its row does not give | Conforming: placement and value shape are
writer guidance". `[R-MTA-07]`: "Neither placement nor value shape bears on validity:
the file stays conforming". ⇒ **conforming**.

**(iii) flags = 0x80000000.** Bit 31 is in the ignore lane (bits 16–31). `[R-CNT-08]`:
"a set ignore-lane bit is not a file-conformance violation — such bits are defined by
later minor versions, and files carrying them are conforming files this text's readers
ignore." `[R-CNF-02]` names this as one of the conduct rules whose violation is
expressly not a file-conformance violation. §21.6 lists it as a defined non-violation.
⇒ **conforming**.

**(iv) user-metadata record with encoding byte 0x05.** 5 lies in the reserved range
3–0x7F (§18.2, §10.2). §21.5 row R1 covers "a document encoding of 0, or a
reserved-range value (3-0x7F)", and §21.5's preamble is explicit: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as violations: what
`[R-MTA-10]` withdraws is the document's content rules, never the encoding byte's own
value set (`[R-MTA-03]`)." Note the contrast with the *experimental* range ≥ 0x80,
which §21.6 records as conforming — 0x05 is not that. The outcome is ignore-record,
but §21.5 adds "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming". ⇒ **nonconforming**.

**Answer: `i=nonconforming ii=conforming iii=conforming iv=nonconforming`.**
Confidence high.

---

## Underdetermination summary

Fourteen of fifteen questions are, in my reading, determined by the text. The one I
flag is **Q12 FILE B**, where the text determines that the compactor need not refuse
and that dropping is licensed, but leaves open whether a compactor that can trivially
observe a reserved-range type value "has detected" the violation within
`[R-WRT-06]`'s meaning — which is what separates `carry` from `drop`. I answer
`carry`, on the ground that F36's assigned detector is the verifier and `[R-WRT-09]`
does not oblige the check, and §20.5 expressly contemplates a latent violation
travelling into the output.
