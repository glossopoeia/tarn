# Cleanroom round 34 — quiz answerer transcript

Sole source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(read in full, in five `Read` calls). No other file in the repository was
opened, listed, or grepped. Local computation only (Python, no file reads
other than my own scratch script).

Scratch files written (mine alone, in
`/private/tmp/claude-501/.../r34-round/scratch/quiz-answerer/`):
- `qa_calc.py` — CRC-32C implementation, trailer assembly, grid/ordinal
  arithmetic, bit-packing and byte-shuffle.

CRC implementation validated two ways before use:
- §4.5 check vector: CRC-32C(`"123456789"`) = `0xE3069283`; CRC-32C(∅) = 0.
- Appendix A's trailer: rebuilding trailer bytes [0,60) with
  file_id = 0x0123456789ABCDEF reproduces the published `0x402F157E`.
  That also confirms my field offsets and little-endian packing.

---

## Q01 — channel entry, `b` / bfloat16 / fill 1.0

§7.4's channel-entry shape: `name (u8 len + bytes) · type u16 (0 invalid) ·
fill (u8 len + bytes)`, with "fill length equals the type's element size
(`[R-CNT-23]`)".

- name: length 1, byte `62` → `01 62`
- type: bfloat16 is ID 11 (§12.1 table) → u16 LE `0b 00`
- fill: element size 2 → prefix `02`. §12.1's worked example: "bfloat16 1.0
  is `0x3F80` ... stored as the bytes `80 3F`" → `80 3f`

Cross-checked against §12.3's `temp` example, which is
`04 74 65 6D 70 0C 00 04 00 00 C0 7F` — same shape.

**`01 62 0b 00 02 80 3f`** (7 bytes).

---

## Q02 — inline_length and extent_length

Field sizes in §7.4 table order:

| field | bytes |
|---|---|
| name (`ab`) | 1 + 2 = 3 |
| layout u8 … channel count u16 (nine scalars) | 1+2+2+2+8+8+8+1+2 = 34 |
| 2 dimension entries, each 1+1+8+8 | 36 |
| channel `r` uint8: 1+1 name, 2 type, 1+1 fill | 6 |
| channel `v` float64: 1+1 name, 2 type, 1+8 fill | 13 |
| index_encoding + entry_count + crc_of_crc_array | 1+8+4 = 13 |

Total = 3 + 34 + 36 + 6 + 13 + 13 = **105**. No sub-records, no residue,
so inline_length = 105. (The same accounting reproduces §7.4's worked
example exactly: 4 + 34 + 18 + 12 + 13 = 81.)

entry_count: layout 2 = planar. G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3,
N = 9; §11.2 addressed-tile count for planar = C·N = 2·9 = 18.

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 18×20 + 1×4 = 360 + 4 = **364**.

---

## Q03 — zero-extent planar layer under codec 4

G_y = ⌈0/16384⌉ = 0, so N = 0 and the addressed-tile count C·N = 0
(`[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is 0,
the layer has zero addressed tiles ... Readers MUST accept such a layer").
entry_count 0, slot (0,0), crc_of_crc_array 0 all satisfy `[R-CNT-17]`
and `[R-CNT-23]`.

The tempting rejection is `[R-COD-07]`'s lz4 cap: P = 16384² = 2²⁸ and a
planar float64 plane is P·8 = 0x80000000, above 0x7E000000. But the cap is
quantified over *addressed* tiles, and §17.2's Note is explicit: "a layer
that addresses none — any dimension extent 0 ... — satisfies it whatever
its tile shape declares, and codec 4 is conforming there." L44 restates the
same quantifier.

`[R-ENC-04]`'s ceiling *is* checked in an empty layer (same Note), but
2³¹ ≤ 2⁶³−1, as are P = 2²⁸ and N·P = 0. §21.9's 256 MiB tile row also does
not bind ("A layer addressing no tile ... has no tile whose decoded size the
table bounds"), and exceeding a §21.9 row is not a validity error anyway.

**accept.**

---

## Q04 — trailer CRC

Trailer bytes [0,60) assembled per §6.2's layout, little-endian:

```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
80 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00
```

CRC-32C over those 60 bytes = **`1c5cfd35`**. (Same bytes with Appendix A's
file_id give 0x402F157E, matching the document — my implementation and byte
layout are validated.)

Stored little-endian at [60,64) that would be `35 fd 5c 1c`; the question
asks for the numeric value.

---

## Q05 — index entry `08 … 64 … de ad be ef`

Parsed: offset = 8, length = 100, crc = 0xEFBEADDE. Not the sentinel.

§15.3: "offset < 16 (non-sentinel) | *structural*: reject-tile — the front
block is never payload". Register row **T8**: "A non-sentinel tile-index
entry has offset < 16, addressing bytes of the front signature block" —
detector reader, detected at tile use, `[R-IDX-03]`. Outcome per §21.4:
**reject-tile**. No other T-row fires (length ≠ 0 so not T10;
8+100 = 108 ≤ F−64 = 1,048,512 so not T9; not a sentinel so not T6/T7).

Coverage walk: §9.7 — "An entry `[R-IDX-03]` classifies reject-tile on a
*structural* ground does not make the walk incomplete: the walk passes over
it, and the bytes of the file it nominally addresses fall to slack".
§5.2 says the same. So the total is **not** partial on this account: **no**.

**T8; reject-tile; no.**

---

## Q06 — zstd document, FCS 100, decodes to 90

§18.2 keeps the frame's content-size constraint as the file's, restated over
the quantity a document does have: "when present it MUST equal the byte
length of the decoded document. A mismatch is one of the frame constraints
R4 registers, not a failure to decode under R3: the bytes decode, and what
is wrong is what the header said about them."

R4's own text confirms: "the content-size field breaks its constraint exactly
when it is present and does not equal the decoded document's byte length",
and its instance list includes "the content-size field declared larger than
the decoded length, layer sub-record extent". 100 > 90.

R3 explicitly yields: "where the encoding is 2 and what fails is one of the
frame constraints R4 registers, R4 is the row".

§21.5's outcome for every row is ignore-record (the `[R-CNT-25]` quarantine),
and `[R-MTA-09]` closes: "Any violation here is ignore-record".

**R4; ignore-record.**

---

## Q07 — encoding byte 0x90 (X) vs 0x40 (Y)

§10.2 metadata-encoding space: assigned 1–2, reserved 3–0x7F, experimental
≥ 0x80.

X: 0x90 ≥ 0x80, experimental. §21.6: "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the
file is conforming ... No document rule attaches at such an encoding, so a
verifier certifies, reporting the record it ignored". `[R-MTA-10]`: "A
verifier meeting such a record in an otherwise conforming file has no
requirement it is unable to check ... and at an experimental-range encoding
certification is unaffected". Verdict: **conforming**.

Y: 0x40 is in 3–0x7F, reserved. §21.5 **R1**: "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)".
§21.5 preamble: "Every row here is a violation all the same: the outcome
bounds a reader's blast radius and never makes the file conforming". §2.3:
"a verifier that has established any violation reports *nonconforming*".
The row's detector is *reader* at open, so a verifier (a reader) establishes
it. Verdict: **nonconforming**.

**X: conforming; Y: nonconforming.**

---

## Q08 — committed_file_length after a minimal commit

`[R-LIF-02]`: (1) begin at exactly F = 128; (2) nothing appended; (3) the
4-byte directory at [128, 132); (5) "append the pad to the next 64-byte
boundary ... and the new trailer".

132 → next 64-byte boundary is 192. Trailer occupies [192, 256).
New F = **256**.

Checks: 256 mod 64 = 0 (`[R-CNT-06]`); dir_offset + dir_length = 132 ≤
F − 64 = 192; the increase is 128, meeting §9.2's "strictly greater ... by
at least 128".

The answer is robust to the other reading of "4 bytes long" (record sequence
of 4 bytes plus its CRC, dir_length 8, region ending at 136): the pad still
runs to 192 and F is still 256.

---

## Q09 — disk ordinal and index byte offset

G_y = ⌈100/32⌉ = 4, G_x = ⌈200/64⌉ = 4 (200/64 = 3.125), N = 16.
Tile coords: t_y = 70 div 32 = 2, t_x = 130 div 64 = 2.
`[R-GEO-06]` linearization 1: s = Σ tᵢ·∏_{j>i} Gⱼ = 2·4 + 2 = 10.
Planar disk ordinal = c·N + s = 3·16 + 10 = **58**.
§15.1: "The entry for the tile with disk ordinal k ... is the k-th entry, at
region byte 20·k" → 20 × 58 = **1160**.

(Shape-checked against §11.4's own example: C = 4, N = 32, s = 10 →
2·32 + 10 = 74, and §15.4 puts entry 74 at bytes [1,480, 1,500) = 20·74.)

---

## Q10 — experimental top-level type 0x8000, MU = 1

(a) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 →
reject-file." → **reject-file**.

(b) §2.3 lists as a cannot-establish ground "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and
*cannot establish* "is available only to a traversal that established no
violation" — which is the stipulated case. → **cannot establish**.

(c) §21.6's closing: "an **experimental-range top-level record type carrying
MU = 1** ... `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
makes the file conforming all the same ... the file in the second carries no
violation at all." §10.3's publication ban binds conduct, not bytes. → **yes**.

---

## Q11 — packed planar bool tile

G_y = ⌈2/3⌉ = 1, G_x = ⌈3/4⌉ = 1, N = 1, C = 1 → one addressed tile.
P = ∏Tᵢ = 3·4 = 12. Planar bool → §14.3 packing, decoded size ⌈12/8⌉ = 2.

In-tile ordinal (§11.4) = u_y·T_x + u_x = 4·u_y + u_x. Inside the extents
(2,3): u_y < 2 and u_x < 3 → ordinals 0,1,2,4,5,6 are real and hold **false**.
Ordinals 3, 7, 8, 9, 10, 11 are padding positions; `[R-SER-05]` requires each
to encode the channel's fill — here **true**. P mod 8 = 4 ≠ 0, so bits 4–7 of
byte 1 are pad bits, which `[R-SER-05]` also fixes to the fill bit (true).

Byte 0 (values 0–7, LSB-first): 0,0,0,1,0,0,0,1 → 0b1000_1000 = 0x88.
Byte 1: values 8–11 all 1 (bits 0–3), pad bits 4–7 all 1 → 0xFF.

**`88 ff`**

Note the oddity worth stating: the tile's *stored* content is almost all
ones although every sample the reference array contains is false — that is
exactly `[R-SER-05]`'s fill-encoded padding.

---

## Q12 — interleaved uint8 + uint16 under byte-shuffle

P = 1·2 = 2, C = 2, Q = 1 + 2 = 3, decoded size P·Q = 6 (§14.2).
In-tile ordinals: (0,0) → 0, (0,1) → 1.
Value sequence (§14.1, sample-major): a@0, b@0, a@1, b@1.
Bytes, little-endian: `11` | `33 22` | `44` | `66 55`.

(a) **`11 33 22 44 66 55`**

Filter 2 (§17.3): interleaved stride s = Q = 3; L = 6, n = L/s = 2. Byte i
of group j moves to offset i·n + j.
Group 0 = `11 33 22`, group 1 = `44 66 55`.
offsets: 11→0, 33→2, 22→4, 44→1, 66→3, 55→5.

(b) **`11 44 33 66 22 55`**

Codec 1 (none): "The stored bytes are the filtered image verbatim"
(`[R-COD-04]`), and the stored length equals the decoded size, 6. Inverse
permutation verified in code.

---

## Q13 — what one commit may do to a layer that stored a tile

§20.3 step 4: "A layer that stores a tile **in the generation this commit
supersedes** keeps its declarations, with these exceptions and no other: its
name, and its dimension and channel names, MAY change; an extent MAY grow,
and MUST NOT shrink; a planar layer's channel list MAY be extended at its
end or shortened from its end, but not both in one commit; and a slab or
alignment declaration MAY be declared, changed, re-established or cleared as
this step provides below. A commit MAY make several of these changes at
once, an extension and a shortening of one channel list excepted."

(i) name change + extent growth — both on the permitted list, and composing
is expressly licensed. **Permitted.**

(ii) append one channel at the end *and* remove one from the end, in one
commit — the single stated exception to composition: "a commit that shortens
a planar layer's channel list appends no channel to it and one that extends
it removes none, whatever the counts, so replacing the last channel ... is
two commits or a rewrite." **Not permitted.**

(iii) clear A (512→0) and declare S = 4 with A_slab = 4096 — both are the
"declared, changed, re-established or cleared" case; composition is licensed;
`[R-CNT-16]`'s mutual exclusivity is satisfied by the new state (A = 0,
S ≠ 0); `[R-SLB-04]`'s invariants are stipulated satisfied.
**Permitted.**

(iv) change a channel's recorded fill — "Every other declaration is fixed for
as long as the layer stores a tile: ... every channel's type and fill", and
§20.3's shape (c) names "a fill value" among the changes that are "not an
appender's operation at all". **Not permitted.**

**i, iii**

---

## Q14 — two layer records with identical, invalid name fields

(a) §19.1 step 4: "Uniqueness is decided first, and over the raw name bytes
whether or not each name is itself well-formed — `[R-ENC-13]` makes name
comparison a byte comparison, which needs no valid name — so two layers whose
name fields are byte-identical are a duplicate even when neither name is
valid." `[R-ENC-15]`: "a duplicate layer name is a file-scope error
(reject-file)". Row F4. → **reject-file**.

(The U+0001 in each name is separately L6, reject-layer at open; the question
asks only about the byte-identity, which is the file-scope condition.)

(b) §19.2's tier list has exactly four entries, the first being "**at open:**
the front signature block ... and the layer-name namespace (§19.1's steps)".
§19.1 step 4 says so directly: "A duplicate layer name is a validity error at
file scope, here, at open". → **at open**.

---

## Q15 — compaction with A's extents fixed, B's moved

(a) `[R-WRT-07]`: a compactor "regenerates each tile-index region any of
whose stored extents the output relocates (entry offsets new; entry lengths,
entry crcs, and sentinel entries unchanged; segment CRCs recomputed ...)".
§20.5's figure states this case verbatim: "In this placement A's stored
extents happen not to move, so A's index is copied and only its slot
re-pointed; under a placement that moved them it would be regenerated too."
→ **B**.

(b) flags = 0x00030000 sets bits 16 and 17, both in the ignore lane (16–31,
§6.3). `[R-WRT-06]`: "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward and set no other, in place of the flags = 0
§6.3 requires of a file created under this text." §6.3 agrees: a compactor
"carries the input's unknown ignore-lane bits into its output trailer rather
than writing flags = 0, and sets no other". Nothing licenses clearing them,
and the compactor implements neither feature, so both are "unknown" bits it
copies. → **0x00030000**.

---

## Underdetermination

I found none of the fifteen underdetermined. Two came close and are worth
naming for the key's benefit:

- **Q08.** "the new complete directory it appends is 4 bytes long" admits two
  readings (region including its terminal CRC, vs. record sequence plus a
  separate CRC). Both yield F = 256, so the ambiguity does not reach the
  answer.
- **Q13 (iii).** The permitted-exception list is a closed list whose members
  compose, with exactly one stated non-composing pair. Reading the alignment
  clear and the slab declaration as two separate exercises of the same
  clause, or as one "slab or alignment declaration" change, gives the same
  result either way.
