# Round 34 — quiz keyer transcript

Source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4838 lines,
292,892 bytes), read in full in five `Read` calls. No other file was read.
Scratch files written (mine alone, in
`/private/tmp/claude-501/.../r34-round/scratch/quiz-keyer/`): `qk_calc.py` (CRC-32C),
`qk_geom.py` (geometry / packing / shuffle).

CRC implementation validated before use against both §4.5 check vectors
(CRC-32C("123456789") = 0xE3069283; CRC-32C(zero bytes) = 0x00000000) **and** against
Appendix A's trailer, which reproduced 0x402F157E exactly.

---

## Q01 — channel entry for `b` : bfloat16, fill 1.0

§7.4's channel-entry shape: `name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes)`,
"fill length equals the type's element size (`[R-CNT-23]`)".

- name: length 1, byte 0x62 → `01 62`
- type: bfloat16 is ID 11 (§12.1 table) → u16 little-endian (`[R-ENC-01]`) → `0b 00`
- fill: element size 2 → prefix `02`; §12.1's worked example: "bfloat16 1.0 is `0x3F80` …
  stored as the bytes `80 3F`" → `80 3f`

Cross-check against §12.3's `temp` example, which is byte-for-byte the same shape
(`04 74 65 6D 70 0C 00 04 00 00 C0 7F`).

**Answer: `01 62 0b 00 02 80 3f`** (7 bytes).

---

## Q02 — inline_length and extent_length

§7.4: "fields are packed in table order with no alignment or padding between them".

| part | bytes |
|---|---|
| name `ab` (1 + 2) | 3 |
| layout 1 + linearization 2 + codec 2 + filter 2 + A 8 + S 8 + A_slab 8 + d 1 + C 2 | 34 |
| 2 dimension entries, each (1+1) + 8 + 8 = 18 | 36 |
| channel `r` uint8: (1+1) + 2 + (1+1) = 6 | 6 |
| channel `v` float64: (1+1) + 2 + (1+8) = 13 | 13 |
| index_encoding 1 + entry_count 8 + crc_of_crc_array 4 | 13 |

Total = 3 + 34 + 36 + 19 + 13 = **105**. (The 34 is confirmed by §7.4's worked example:
"the nine scalars from layout through channel count occupy 4 + 34 bytes".)
No sub-records, no residue, so inline_length = 105.

entry_count: G_y = ⌈10/4⌉ = 3, G_x = ⌈10/4⌉ = 3, N = 9 (§11.2). Planar ⇒ addressed-tile
count = C·N = 2·9 = 18 (`[R-GEO-03]`).

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4
= 18 × 20 + 1 × 4 = 360 + 4 = **364**.

**Answer: (a) 105, (b) 364.**

---

## Q03 — zero-extent planar layer under codec 4

G_y = ⌈0/16384⌉ = 0, G_x = ⌈100/16384⌉ = 1 ⇒ N = 0 ⇒ addressed-tile count C·N = 0.
Consistent with entry_count 0, extent slot (0,0), crc_of_crc_array 0
(`[R-CNT-17]`, `[R-CNT-23]`; L22 and L27 are both clear).

`[R-GEO-02]`: "A dimension with extent 0 is valid: its grid count is 0, the layer has zero
addressed tiles… Readers MUST accept such a layer."

The trap is the lz4 cap. P = 16384 × 16384 = 2²⁸; the planar float64 plane's decoded size
is P·Bᶜ = 2³¹ = 2,147,483,648, which **exceeds** `[R-COD-07]`'s 0x7E000000 = 2,113,929,216.
But the cap is quantified over *addressed* tiles, and §17.2's Note is explicit:
"a layer that addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
whatever its tile shape declares, and codec 4 is conforming there." L44 reads the same way.

`[R-ENC-04]` does bind unconditionally ("carries no such quantifier"), so P·Bᶜ = 2³¹ is
formed and checked — comfortably under 2⁶³ − 1. N·P = 0.

§21.9's 256 MiB decoded-tile row likewise: "A layer addressing no tile (§11.2) therefore has
no tile whose decoded size the table bounds."

**Answer: accept.**

---

## Q04 — trailer CRC

Trailer bytes [0,60) assembled per §6.2's layout:

```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
80 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00  00 00 00 00
```

CRC-32C over those 60 bytes (§4.5, `[R-ENC-09]`; row F14) = **0x1c5cfd35**, stored
little-endian as `35 fd 5c 1c`.

Validation of the routine: the identical trailer with Appendix A's file_id
0x0123456789ABCDEF reproduces Appendix A's published 0x402F157E.

**Answer: `1c5cfd35`.**

---

## Q05 — index entry with offset 8

offset = 8, length = 100, crc = 0xEFBEADDE. Non-sentinel (neither field is 2⁶⁴−1).
§15.3's row "offset < 16 (non-sentinel) | *structural*: reject-tile — the front block is
never payload". Register row **T8**: "A non-sentinel tile-index entry has offset < 16,
addressing bytes of the front signature block". No other row fires: offset + length = 108
≤ F − 64 = 1,048,512; length ≠ 0; both fields ≤ 2⁶³ − 1.

Outcome class: **reject-tile** (§21.4).

Coverage walk: §9.7 — "An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
does not make the walk incomplete: the walk passes over it, and the bytes of the file it
nominally addresses fall to slack where no other claimant claims them (§15.3)."
`[R-CNT-21]` says the same. So **no**.

**Answer: T8; reject-tile; no.**

---

## Q06 — Frame_Content_Size 100, document 90 bytes

§18.2 (`[R-MTA-09]`): "The frame's content-size field, unlike the decoded size and the
window, is *not* left to the reader: it MAY be present, and when present it MUST equal the
byte length of the decoded document. A mismatch is one of the frame constraints R4
registers, not a failure to decode under R3: the bytes decode, and what is wrong is what
the header said about them."

R4's instance list names it: "the content-size field declared larger than the decoded
length, layer sub-record extent". Outcome for every §21.5 row is ignore-record, "whatever
the containing scope" (`[R-CNT-25]`'s quarantine).

**Answer: R4; ignore-record.**

---

## Q07 — encoding byte 0x90 vs 0x40

§10.2 / §18.2 partition the metadata-encoding space: 1–2 assigned, 3–0x7F reserved,
≥ 0x80 experimental.

X (0x90, experimental): §21.6 — "A user-metadata record declares an experimental-range
(≥ 0x80) document encoding | Ignored (ignore-record); the file is conforming … so a verifier
certifies, reporting the record it ignored". `[R-MTA-10]` confirms the verifier "has no
requirement it is unable to check". Verdict **conforming**.

Y (0x40 = 64, reserved range): R1 — "A user-metadata record declares a document encoding of
0, or a reserved-range value (3-0x7F)" — is a violation. §2.3: "a verifier that has
established any violation reports *nonconforming*". Verdict **nonconforming**.

**Answer: X = conforming; Y = nonconforming.**

---

## Q08 — committed_file_length after one commit

F = 128. `[R-LIF-02]` step 1: begin at exactly F. Step 2 appends nothing. Step 3 appends the
4-byte directory at [128, 132) — a 4-byte directory being the whole region including its
terminal CRC (§3.1, §7.1, and Appendix A's "an empty directory — zero records, so 4 bytes
holding the CRC-32C of zero bytes"). Step 5 pads to the next 64-byte boundary: 132 → 192
(60 pad bytes), then the 64-byte trailer at [192, 256).

New F = **256**. Checks: 256 mod 64 = 0 (`[R-CNT-06]`); dir_offset + dir_length = 132 ≤
F − 64 = 192; increase = 128, matching §9.2's "strictly greater … by at least 128".

(Robust to the alternative reading in which the 4 bytes are the record sequence and the CRC
adds 4 more: end 136 still pads to 192 and F is still 256.)

**Answer: 256.**

---

## Q09 — disk ordinal and entry offset

G_y = ⌈100/32⌉ = 4, G_x = ⌈200/64⌉ = 4, N = 16 (§11.2).
Tile coordinates t_i = x_i div T_i: t_y = 70 div 32 = 2, t_x = 130 div 64 = 2 (`[R-GEO-06]`).
Spatial ordinal s = Σ t_i · ∏_{j>i} G_j = 2·4 + 2 = 10.
Planar disk ordinal = c·N + s = 3·16 + 10 = **58**.
§15.1: "The entry for the tile with disk ordinal k … is the k-th entry, at region byte 20·k"
→ 20 × 58 = **1160**.

**Answer: (a) 58, (b) 1160.**

---

## Q10 — experimental top-level type 0x8000 with MU = 1

(a) `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file." → **reject-file**.

(b) §2.3 lists as a cannot-establish ground "when a record carries MUST_UNDERSTAND = 1 with
a type it does not implement (§21.6)". The verifier established no violation, and
"*cannot establish* is available only to a traversal that established no violation".
→ **cannot establish**.

(c) §21.6's closing paragraph: the second of the two "conforming files a reader nevertheless
refuses" is "an **experimental-range top-level record type carrying MU = 1** … `[R-CNT-15]`
obliges the reader to reject, and `[R-CNF-02]` makes the file conforming all the same."
PE = 1, so `[R-CNT-12]`'s MU=1/PE=0 bar is not tripped. → **yes**.

**Answer: reject-file; cannot establish; yes.**

---

## Q11 — packed planar bool tile image

G = (⌈2/3⌉, ⌈3/4⌉) = (1, 1), N = 1, one channel planar ⇒ one addressed tile.
P = T_y·T_x = 3·4 = 12; §14.3 decoded size = ⌈12/8⌉ = 2 bytes.

In-tile ordinal = u_y·4 + u_x (§11.4, row-major, permanently). Tile coordinates are (0,0),
so coordinate = in-tile position. Real positions are u_y < 2 and u_x < 3; every other
position is a padding position (§11.3), and `[R-SER-05]` fixes each to the channel's fill —
here fill 0x01 = true, i.e. bit 1. Pad bits (P mod 8 = 4, so bits 4–7 of byte 1) likewise
carry the fill bit.

| ord | (u_y,u_x) | kind | bit |
|---|---|---|---|
|0|(0,0)|real|0|
|1|(0,1)|real|0|
|2|(0,2)|real|0|
|3|(0,3)|pad|1|
|4|(1,0)|real|0|
|5|(1,1)|real|0|
|6|(1,2)|real|0|
|7|(1,3)|pad|1|
|8|(2,0)|pad|1|
|9|(2,1)|pad|1|
|10|(2,2)|pad|1|
|11|(2,3)|pad|1|

Byte 0 = bits 0–7 = 0,0,0,1,0,0,0,1 LSB-first = 0x08 | 0x80 = 0x88.
Byte 1 = bits 0–3 = 1,1,1,1 (0x0F) plus pad bits 4–7 all 1 (0xF0) = 0xFF.

**Answer: `88 ff`.**

---

## Q12 — interleaved uint8+uint16, byte-shuffle

P = 1·2 = 2, C = 2, Q = 1 + 2 = 3, decoded size P·Q = 6 (§14.2). Extents equal tile extents,
so no padding positions.

Value sequence (§14.1, interleaved, sample-major): value k is channel (k mod C) at in-tile
ordinal k div C.
k=0 → a@0 = 0x11; k=1 → b@0 = 0x2233 → `33 22` (LE); k=2 → a@1 = 0x44;
k=3 → b@1 = 0x5566 → `66 55`.

(a) decoded tile image = `11 33 22 44 66 55`.

Byte-shuffle (`[R-COD-10]`): stride s = Q = 3 for an interleaved tile; L = 6, n = L/s = 2.
Groups: j=0 = `11 33 22`, j=1 = `44 66 55`. Byte i of group j goes to offset i·n + j:

| src (j,i) | value | dest offset |
|---|---|---|
|(0,0)|11|0|
|(0,1)|33|2|
|(0,2)|22|4|
|(1,0)|44|1|
|(1,1)|66|3|
|(1,2)|55|5|

Filtered = `11 44 33 66 22 55`. Codec 1 (`[R-COD-04]`): "The stored bytes are the filtered
image verbatim."

**Answer: (a) `11 33 22 44 66 55`; (b) `11 44 33 66 22 55`.**

---

## Q13 — which single-commit changes §20.3 step 4 permits

Permitted list (§20.3 step 4): "its name, and its dimension and channel names, MAY change;
an extent MAY grow, and MUST NOT shrink; a planar layer's channel list MAY be extended at
its end or shortened from its end, but not both in one commit; and a slab or alignment
declaration MAY be declared, changed, re-established or cleared… A commit MAY make several
of these changes at once, an extension and a shortening of one channel list excepted".

Fixed list: "the layout, the linearization and the index encoding, the codec and the filter,
the rank and the dimension order, every tile extent, **every channel's type and fill**, an
interleaved layer's channel list (its names aside), and the position of every planar channel
the new state keeps."

- (i) name change + extent growth — both permitted, and combinable. **Permitted.**
- (ii) planar channel list extended *and* shortened in one commit — expressly excepted:
  "a commit that shortens a planar layer's channel list appends no channel to it and one
  that extends it removes none, whatever the counts". **Not permitted.**
- (iii) clear A, declare S with A_slab — both fall under "a slab or alignment declaration
  MAY be declared, changed, re-established or cleared", and several at once are allowed.
  New state A = 0, S = 4 satisfies `[R-CNT-16]`'s mutual exclusivity; invariants are
  stipulated re-established (`[R-SLB-04]`). **Permitted.**
- (iv) fill change — "every channel's type and fill" is on the fixed side; §20.3's closing
  list names "a fill change" among the rewrites. **Not permitted.**

**Answer: i, iii.**

---

## Q14 — two byte-identical, ill-formed layer names

§19.1 step 4: "A duplicate layer name is a validity error at file scope, here, at open
(`[R-ENC-15]`, §19.2)… Uniqueness is decided first, and over the raw name bytes whether or
not each name is itself well-formed — `[R-ENC-13]` makes name comparison a byte comparison,
which needs no valid name — so two layers whose name fields are byte-identical are a
duplicate even when neither name is valid." `[R-ENC-15]`: "a duplicate layer name is a
file-scope error (reject-file)". Row F4.

(The U+0001 separately makes each name a layer-scope error, L6 — but the question asks what
follows from byte-identity, which is the file-scope duplicate, decided first.)

§19.2's tier list is: **at open**; at first access to a layer; at use of a tile; at use of
a record's extent. F4's *Detected* cell also reads "open".

**Answer: reject-file; at open.**

---

## Q15 — compaction with flags 0x00030000

(a) `[R-WRT-07]`: the compactor "regenerates each tile-index region any of whose stored
extents the output relocates (entry offsets new; entry lengths, entry crcs, and sentinel
entries unchanged; segment CRCs recomputed…)". §20.5's figure says it outright: "In this
placement A's stored extents happen not to move, so A's index is copied and only its slot
re-pointed; under a placement that moved them it would be regenerated too." A's stored
extents do not move ⇒ A copied; B's all move ⇒ B regenerated. → **B**.

(b) flags = 0x00030000 sets bits 16 and 17 — both in the ignore lane (bits 16–31), both
unknown to this compactor. `[R-WRT-06]`: "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward and set no other, in place of the flags = 0 §6.3 requires of a
file created under this text". `[R-CNT-08]` says the same. → **0x00030000**.

**Answer: B; 0x00030000.**
