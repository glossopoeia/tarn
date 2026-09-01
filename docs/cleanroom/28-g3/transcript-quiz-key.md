# Round 28 — quiz keyer transcript

## Access / method

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4648 lines, 281,820 bytes). It was where the brief said it would be. Read it in
full via `sed -n` ranges plus `grep` for headers. No other project file was read;
no ADRs, no conformance corpus, no registry, no git history, no web.

Local computation only (Python, reading no project files): a CRC-32C
implementation in `scratchpad/crc.py`, validated against three constants the
document itself publishes before it was used for any answer:

- CRC-32C("123456789") = 0xE3069283, CRC-32C("") = 0x00000000 (§4.5 check vector)
- CRC-32C of 80 bytes = 4 sentinel entries = 0x80A34955; CRC of that 4-byte
  array = 0xC4EE982E (§7.4 worked example)
- CRC-32C of a full 2^16-entry all-sentinel segment = 0xEECB3BB2 (§15.4, `[R-IDX-05]`)
- Appendix A's minimal-file trailer CRC = 0x402F157E, stored `7E 15 2F 40`

All four reproduce exactly.

Context that arrived unrequested: see the `disclosure` field.

---

## Q01 — trailer checksum field bytes

§6.2's trailer layout table gives the fields and offsets; the CRC field at
offset 60 is "CRC-32C over trailer bytes [0, 60)". §4.5 `[R-ENC-09]` fixes
CRC-32C, "stored as a little-endian `u32`". §4.1 `[R-ENC-01]`: all multi-byte
values little-endian.

Trailer bytes [0, 60) assembled:

```
8a4e5241540d0a1a        magic (§6.2)
0100                    version_major = 1
0000                    version_minor = 0
00000000                flags = 0
4000000000000000        dir_offset = 64
6400000000000000        dir_length = 100
0001000000000000        committed_file_length = 256
bebafeca00000000        file_id = 0x00000000CAFEBABE
00 x12                  reserved, zero
```

Gates check out: F = 256 is a multiple of 64; dir_offset 64 >= 16;
dir_length 100 >= 4; 64 + 100 = 164 <= F - 64 = 192; file_id != 0.

CRC-32C over those 60 bytes = 0x9C67F80D. Stored little-endian: `0D F8 67 9C`.

**Answer: `0df8679c`**  (high confidence — same routine reproduces Appendix A)

---

## Q02 — channel entry, `w`, bfloat16, fill = binary32 0xC0000000's value

§7.4's inline-payload table: a channel entry is
"name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes)".
§12.3's worked example pins the byte order: `temp`/float32/NaN is
`04 74 65 6D 70 0C 00 04 00 00 C0 7F`.

- name: length 1, byte 0x77 -> `01 77`
- type: bfloat16 = ID 11 (§12.1 table) -> u16 LE `0b 00`
- fill: §12.1 `[R-TYP-02]` — "A bfloat16 bit pattern b denotes exactly the value
  that the IEEE 754 binary32 bit pattern b × 2^16 (b in the high 16 bits, low
  16 bits zero) denotes." b × 2^16 = 0xC0000000 => b = 0xC000 (= -2.0).
  Element size 2, so fill length prefix 2 (`[R-CNT-23]`), bytes LE `00 c0`.

**Answer: `01770b000200c0`**  (high confidence)

---

## Q03 — interleaved tile, codec 1, filter 2, stored bytes

Layer: rank 2, T = (2,3), P = 6, no padding. C = 2: `a` uint8 (B=1), `b` uint16 (B=2).
Q = sum B = 3. §14.2: interleaved decoded size = P·Q = 18; offset of channel c's
value at in-tile ordinal u is u·Q + F_c, F_a = 0, F_b = 1.

Decoded tile image (18 bytes):
`a0 00 80 | a1 01 80 | a2 02 80 | a3 03 80 | a4 04 80 | a5 05 80`
(0x8000+k little-endian is `k 80`.)

§17.1 `[R-COD-01]`: "A stored tile's bytes are produced from its decoded tile
image (§14) by two per-tile stages: the layer's filter (§17.3), then its codec".

§17.3 `[R-COD-10]`: interleaved shuffle stride s = Q = 3; n = L/s = 6;
"the filtered image places byte i of group j at offset i · n + j".

- i=0 (the `a` bytes): offsets 0..5 -> `a0 a1 a2 a3 a4 a5`
- i=1 (`b` low bytes): offsets 6..11 -> `00 01 02 03 04 05`
- i=2 (`b` high bytes): offsets 12..17 -> `80 80 80 80 80 80`

Codec 1 (`[R-COD-04]`): "The stored bytes are the filtered image verbatim."
Length 18 = decoded size, consistent with `[R-COD-04]`'s equality.

**Answer: `a0a1a2a3a4a5000102030405808080808080`**  (high confidence)

---

## Q04 — one-sample bool tile, interleaved then planar

rank 1, E=1, T=1 => P = 1. One bool channel, fill byte 0x01 (true), tile stored,
value true.

Interleaved (§14.2 `[R-SER-02]`): "a bool value — interleaved layers only ... as
a single byte, 0x00 = false, 0x01 = true, with element size 1". Q = 1,
decoded size = P·Q = 1. Image = `01`.

Planar (§14.3 `[R-SER-03]`): packed LSB-first, decoded size = ceil(P/8) = 1 byte.
Value 0 occupies bit 0 = 1. "The final byte's high bits beyond the last value
(bit positions P mod 8 through 7, when P mod 8 != 0) are the tile's **pad
bits**". P mod 8 = 1, so bits 1..7 are pad bits, and §14.5 `[R-SER-05]`: "Every
pad bit (§14.3) MUST carry the plane's channel's fill bit." Fill = true = 1, so
bits 1..7 all set. Byte = 0xFF.

§14.4's Note confirms the shape of this exact case: "At P = 1 the two are the
same length and `[R-SER-05]` fixes the planar pad bits to the channel's fill, so
the images coincide exactly when that fill is false." Here fill is true, so they
differ.

**Answer: `01 ff`**  (high confidence)

---

## Q05 — version_major 3, byte-reversed front magic, resident [0,16)

The trailer is intact (correct magic, CRC verifies, fields in range). The front
signature block is wrong: bytes [0,8) are the front magic byte-reversed.

Reach (§2.3 `[R-CNF-13]`, and §21.2's opening): "Deriving it there yields F8,
F14, F6 and both of F1's instances — each asserting an invariant `[R-CNT-24]`
fixes in every major — and no other row." So the front-block condition reaches a
file declaring major 3.

F1 is the narrower row here (a signature constant stored byte-reversed;
§21.1: "F1's front-block instance of F6 ... stand in that relation"), governed by
`[R-ENC-02]`: "a reader encountering what appears to be a byte-swapped signature
(§6) MUST treat the file as invalid (reject-file), never as a foreign-endian
file to be adapted."

Residency: `[R-CNT-04]` / §19.1 step 1 — "A reader whose open leaves bytes
[0, 16) **resident** ... MUST verify the full block by byte equality before other
processing, and MUST treat any mismatch as reject-file." The stipulated reader's
open leaves them resident, so the exemption does not apply, and `[R-CNF-13]`
carries the exemption test across majors unchanged ("`[R-CNT-04]`'s residency
exemption among them").

(a) **reject-file**.

(b) `[R-CNF-13]`: the reader "MUST treat its failure as reject-file on the ground
of the requirement stating it rather than on capability grounds; the distinct
diagnostic `[R-CNT-07]` asks for is owed where every reaching condition is
satisfied and the declared major is one the reader does not implement." A
reaching condition failed, so **no**.

(c) `[R-CNF-13]`: "A verifier that establishes such a failure reports
*nonconforming*, whatever major the file declares and whether or not it
implements that major." F6's Instances cell adds "a verifier holds no such
exemption (§2.3)". So **nonconforming**.

**Answer: reject-file; no; nonconforming**  (high confidence)

---

## Q06 — encoding byte 0x03 vs 0x83

§10.2 / §18.2 `[R-MTA-03]`: metadata-encoding space — 1,2 assigned; 3–0x7F
reserved; >= 0x80 experimental.

File P, encoding 0x03 (reserved): register row R1 — "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)" —
outcome ignore-record, detector reader. §21.5's preamble: "Every row here is a
violation all the same: the outcome bounds a reader's blast radius and never
makes the file conforming (`[R-CNF-12]`)." A verifier that establishes a
violation reports nonconforming (§2.3 `[R-CNF-11]`).
-> ignore-record; nonconforming.

File Q, encoding 0x83 (experimental): §21.6 — "A user-metadata record declares an
experimental-range (>= 0x80) document encoding | Ignored (ignore-record); the
file is conforming ... No document rule attaches at such an encoding, so a
verifier certifies, reporting the record it ignored". `[R-MTA-10]` confirms:
"A verifier meeting such a record in an otherwise conforming file has no
requirement it is unable to check — the record is not among `[R-CNF-11]`'s
cannot-establish grounds, and certification is unaffected".
-> ignore-record; conforming.

(Framing is clean in both: inline_length 1, extent_length 40 >= 5, extent CRC
verifies — so no F21/F22/F23/R2.)

**Answer: ignore-record; nonconforming; ignore-record; conforming**  (high confidence)

---

## Q07 — layer sub-record type 0x9000, MU=1, PE=1, unimplemented

0x9000 >= 0x8000 = experimental range for record types (§10.2 table).

(a) §7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer,
and where the file is otherwise conforming a reader MUST NOT reject the file for
it". -> **reject-layer**.

(b) §21.6: "The qualifier is load-bearing — the same type as a layer sub-record
is reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
the top-level case is a file a reader refuses, since the prohibition on
publishing experimental values binds a writer's conduct and not the bytes."
`[R-CNF-02]` makes the emission a conduct violation, not a byte violation. The
stipulation removes every register row. -> **yes**.

(c) §2.3 `[R-CNF-11]`: a verifier reports *cannot establish* "when a record
carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and
"*cannot establish* is available only to a traversal that established no
violation" — none here. -> **cannot establish**.

**Answer: reject-layer; yes; cannot establish**  (high confidence)

---

## Q08 — sentinel offset/length with crc = 5

§15.3's table: "offset = S ∧ length = S ∧ crc != 0 | *structural*: reject-tile".

Register row: T6 — "A tile-index entry has offset and length both
0xFFFF_FFFF_FFFF_FFFF but crc != 0", detector reader, detected at tile use,
governing rule `[R-IDX-03]`, in §21.4 whose outcome is reject-tile.

(c) §13.3 `[R-TYP-09]`: "Fill is produced by exactly one condition: a sentinel
entry read from a verified index chain ... A reader MUST NOT return fill for a
tile whose entry is malformed (§15.3)". `[R-CNF-09]`: "a read of a rejected tile
MUST NOT silently return fill." -> **no**.

**Answer: T6; reject-tile; no**  (high confidence)

---

## Q09 — planar layer arithmetic

§11.2 `[R-GEO-03]`: G_i = ceil(E_i/T_i); N = prod G_i; addressed-tile count is
C·N for a planar layer.

G_y = ceil(1000/256) = 4;  G_x = ceil(300/128) = 3;  N = 12.

(1) entry_count = C·N = 5 × 12 = **60**  (`[R-CNT-17]`: entry_count "equals the
    addressed-tile count").

(2) §7.4 `[R-CNT-17]`: "Under index_encoding 1, extent_length MUST equal
    entry_count × 20 + ceil(entry_count / 2^16) × 4".
    = 60×20 + 1×4 = 1200 + 4 = **1204**.

(3) §11.4 `[R-GEO-06]`: t_y = 700 div 256 = 2; t_x = 200 div 128 = 1;
    s = sum t_i · prod_{j>i} G_j = 2·G_x + 1 = 2·3 + 1 = 7.
    Planar disk ordinal = c·N + s = 3·12 + 7 = **43**.

(4) §15.1 `[R-IDX-01]`: "The entry for the tile with disk ordinal k (§11.4) is
    the k-th entry, at region byte 20·k" -> 20 × 43 = **860**.

**Answer: 60, 1204, 43, 860**  (high confidence)

---

## Q10 — interleaved decoded size and offset

T = (2,3,4) -> P = 24. Channels: `p` bool (B=1, §14.2 gives interleaved bool
element size 1), `q` float64 (B=8), `r` uint16 (B=2). Q = 1+8+2 = 11.

(1) §14.2 `[R-SER-02]`: interleaved decoded size = P·Q = 24 × 11 = **264**.

(2) §11.4 `[R-GEO-06]`: in-tile sample ordinal of (1,2,3) =
    sum u_i · prod_{j>i} T_j = 1·(3·4) + 2·4 + 3 = 12 + 8 + 3 = 23.
    §14.2: "channel c's value at in-tile ordinal u sits at byte u · Q + F_c".
    F_r = B_p + B_q = 1 + 8 = 9.
    23 × 11 + 9 = 253 + 9 = **262**.  (262 + 2 = 264, the image's end. Checks.)

**Answer: 264, 262**  (high confidence)

---

## Q11 — smallest new committed_file_length

§9.2 `[R-LIF-02]`: "A commit's committed_file_length is strictly greater than
the prior trailer's, by at least 128". 4096 + 128 = 4224.

The Note under it derives the floor and it is achievable here: dir_offset = 4096
(step 1 begins writing at exactly F), dir_length = 4 (`[R-CNT-06]` minimum), so
dir_offset + dir_length = 4100 <= new F - 64; and `[R-CNT-06]` makes F a multiple
of 64. Smallest multiple of 64 with F - 64 >= 4100 is F = 4224
(4224 - 64 = 4160 >= 4100).

**Answer: 4224**  (high confidence)

---

## Q12 — instance count of the ignore-record table (§21.5)

§21.1's reading rule: "Instances within a cell are separated by semicolons, and
a cell reading — is one instance; the count is therefore mechanical once the
cell is written."

Mechanical count of the §21.5 Instances column:

| Row | Instances |
|---|---|
| R1 | 4 |
| R2 | 2 |
| R3 | 2 |
| R4 | 16 |
| R5 | 8 |
| R6 | 4 |
| R7 | 6 |
| R8 | 2 |
| R9 | 2 |
| R10 | 2 |
| **total** | **48** |

Cross-check on the counting rule: applying the identical mechanical rule to all
four register tables yields 35 + 49 + 26 + 10 = 120 rows and
56 + 116 + 55 + 48 = 275 instances — exactly §21.8 `[R-ERR-02]`'s
"120 conditions over 275 instances". The rule and the arithmetic are both
confirmed by the document's own figure.

**Answer: 48**  (high confidence)

---

## Q13 — compactor output flags and version_minor

Input flags 0x00030000 = ignore-lane bits 16 and 17 set; incompat lane clear.
This text "defines no flag bits" (§6.3 `[R-CNT-08]`), so both are unknown
ignore-lane bits, and §21.6 makes a set ignore-lane bit a conforming condition.

(1) §20.5 `[R-WRT-06]`: "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward, in place of the flags = 0 §6.3 requires of a file
created under this text (`[R-CNT-08]`)." §6.3 already says a compactor "carries
the input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0". A compactor implementing only this text's features sets no other
bit, and the incompat lane stays 0. -> **`00030000`**.

(2) `[R-WRT-06]`: "Where the output carries a feature a later minor defines and
this compactor does not — on a conforming input a carried ignore-lane bit (§6.3)
or an unrecognized `tarn.` key in a record it never decoded (§18.3) ... the
output's version_minor SHOULD be at least the input's". The output carries a
carried ignore-lane bit, so this branch applies, not `[R-CNT-26]`'s floor.
Input version_minor = 2. -> **2**.

**Answer: `00030000`, 2**  (high confidence)

---

## Q14 — may the appender drop each MU=0/PE=0 sub-record?

§20.4's table, MU = 0 / PE = 0 row: "Retain byte-identical, or drop it ... An
appender MUST NOT drop it except in a commit that *independently* changes the
scope the record attaches to: for a layer sub-record, that layer's record, the
entry set of its index, or which of its tiles are stored ... Superseding a
stored tile's bytes re-places that layer's index region (§20.3, `[R-WRT-04]`),
moving its extent slot (§7.4) and so modifying that layer's record, which is such
a change: an appender superseding a tile MAY drop a top-level such record, or
such a sub-record of the layer whose tile it superseded".

The stored flags govern, since the updater does not implement the type
(§20.4: "For a type the updater does not implement, the stored flags are
authoritative"), and the type is unregistered so §7.3's fixed flags do not apply.

- Layer A's sub-record: the commit supersedes a tile of layer A, which is exactly
  the change the rule names. -> **yes**.
- Layer B's sub-record: nothing about layer B changes. And "Dropping the record,
  or dropping another record in the same commit, is not itself such a change, so
  a commit whose only effect would be the drop MUST retain it." -> **no**.

**Answer: yes, no**  (high confidence)

---

## Q15 — 1372-byte pre-trailer gap

F = 2048; trailer at [1984, 2048); directory at [512, 612). Bytes [612, 1984)
hold no structure and are unclaimed — a 1372-byte pre-trailer gap.

(a) §6.2 `[R-CNT-05]`: the pre-trailer pad's number is bounded "only through step
5 of the commit protocol, which pads to the next 64-byte boundary
(`[R-LIF-02]`) — **a longer gap is conforming, and no conforming commit produces
one**." §2.3 `[R-CNF-02]` names this case expressly among the writer obligations
whose violation is not a file-conformance violation: "§6.3's flags = 0 against a
set ignore-lane bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's
pad are the cases this text states". The unclaimed bytes are slack (§5.2
`[R-CNT-21]`), whose content and quantity carry no conformance requirement, and
F7's condition ("A structure occupies bytes between the live directory's end and
the live trailer") is not exhibited. -> **yes**.

(b) The same sentence: "no conforming commit produces one." Step 5 of
`[R-LIF-02]` pads to the *next* 64-byte boundary — from 612 that is 640, giving
a trailer at [640, 704) and F = 704, not 2048. Every writer tier runs this path:
a creator and a compactor via §20.2 / §20.5's creation path, an appender via
§20.3 step 6. So no conforming writer produces this file, though the bytes are
conforming. -> **no**.

This is the conduct/predicate split §2.3 draws stated as a pair.

**Answer: yes, no**  (high confidence)

---

## Underdetermined

None of the fifteen came out underdetermined. Each turned on an express
sentence, and I looked hard for a second reading on Q05 (capability vs.
reaching-condition ground), Q07 (verdict *cannot establish* vs. *conforming*),
Q13 (`[R-WRT-06]`'s branch vs. `[R-CNT-26]`'s floor) and Q15 (a conduct rule that
is not a byte rule) — in each case the document forecloses the alternative in a
sentence written for that purpose. I record that as a fact about this document's
current state, not as a target met.
