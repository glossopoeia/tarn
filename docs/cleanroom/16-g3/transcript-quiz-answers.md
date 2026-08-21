# Cleanroom round 16 — quiz answerer transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4282 lines, in five sequential `Read` calls). I ran `wc` and `grep` against that
same file only. I ran two Python scripts I wrote myself in the scratchpad
(`calc.py`, `calc2.py`) which read no files — a CRC-32C implementation plus
integer arithmetic. My CRC implementation was validated against three constants
the document itself states: CRC-32C("123456789") = 0xE3069283, the §7.4 example's
4-sentinel segment CRC 0x80A34955 and crc_of_crc_array 0xC4EE982E, and §15.4's
full all-sentinel segment constant 0xEECB3BB2 — all three reproduced exactly.
I read no ADR, no test vector, no registry.json, no other repository file, and no
git history. I did not list the output directory.

---

## Q01 — trailer bytes [60, 64)

Trailer layout §6.2. Field values:

- magic `8A 4E 52 41 54 0D 0A 1A`
- version_major = 1 (§6.2 valid values)
- version_minor: `[R-CNT-26]` — "A writer SHOULD emit the lowest version_minor that
  defines every feature present in the file — for a file expressible under this text,
  0 — and an appender the maximum of that floor and the prior trailer's minor".
  Floor 0, prior minor 0 → **0**.
- flags: `[R-CNT-08]` — "a writer creating a file under this text MUST write
  flags = 0"; an updater copies forward unknown ignore-lane bits, and every prior
  trailer carried flags = 0 → **0**.
- generation = 3 (given; `[R-LIF-02]` step 5 would also force it from a gen-2 prior)
- dir_offset = 16, dir_length = 4096, committed_file_length = 4288
  (4288 mod 64 = 0 ✓; dir_offset + dir_length = 4112 ≤ F − 64 = 4224 ✓)
- file_id = 0x00000000DEADBEEF → `ef be ad de 00 00 00 00`
- reserved [56, 60) = zero (§6.2 "Valid values: zero")

Bytes [0, 60):

```
8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
03 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00
00 10 00 00 00 00 00 00 c0 10 00 00 00 00 00 00
ef be ad de 00 00 00 00 00 00 00 00
```

CRC-32C over those 60 bytes = **0x24006CA2**, stored little-endian (`[R-ENC-09]`).

**Answer: `a2 6c 00 24`**

---

## Q02 — layer record header [4, 8) and [16, 24)

Header layout §7.2: offset 4 = inline_length (u32); offset 16 = extent_length (u64).

**(a) inline_length.** §7.4's packed payload, in table order:

| part | bytes |
|---|---|
| name `grid` (1 + 4) | 5 |
| layout, linearization, codec, filter (1+2+2+2) | 7 |
| A, S, A_slab (8·3) | 24 |
| rank d (1), C (2) | 3 |
| dim `row` (1+3+8+8) | 20 |
| dim `col` (1+3+8+8) | 20 |
| chan `u` float64 (1+1 + 2 + 1+8) | 13 |
| chan `flag` bool (1+4 + 2 + 1+1) | 9 |
| index_encoding (1), entry_count (8), crc_of_crc_array (4) | 13 |
| sub-records | 0 |

Total = 5+7+24+3+40+22+13 = **114** = 0x72. (Cross-check against §7.4's worked
example: "Name and the nine scalars from layout through channel count occupy
4 + 34 bytes" — my 5 + 34 for the 4-byte name `grid`.)

Fill lengths are forced by `[R-CNT-23]`: "fill length equals the type's element
size" — float64 = 8, bool = 1 (§12.1 table).

**(b) extent_length.** Geometry: G = (⌈2048/64⌉, ⌈4096/64⌉) = (32, 64), N = 2048
(`[R-GEO-03]`). Layout is **planar**, so the addressed-tile count is C·N =
2·2048 = **4096**, which `[R-CNT-17]` requires entry_count to equal.
`[R-CNT-17]`: "extent_length MUST equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4".
= 4096·20 + ⌈4096/65536⌉·4 = 81920 + 4 = **81924** = 0x00014004.

**Answer: (a) `72 00 00 00`; (b) `04 40 01 00 00 00 00 00`**

---

## Q03 — decoded tile image and index-entry length

G = (⌈3/3⌉, ⌈4/5⌉) = (1, 1), N = 1, C = 1 planar → 1 addressed tile.
P = ∏Tᵢ = 3·5 = 15.

Planar + bool → §14.3 packed plane: "value k occupies bit k mod 8 of byte k div 8
… and the decoded size is ⌈P/8⌉ bytes" = ⌈15/8⌉ = **2 bytes**.

In-tile ordinal (§11.4, permanent row-major): u = u_i·5 + u_j.

| k | (i,j) | status | value |
|---|---|---|---|
|0|(0,0)|real|true (0 even)|
|1|(0,1)|real|false|
|2|(0,2)|real|true|
|3|(0,3)|real|false|
|4|(0,4)|padding (j ≥ 4)|fill = true|
|5|(1,0)|real|false|
|6|(1,1)|real|true|
|7|(1,2)|real|false|
|8|(1,3)|real|true|
|9|(1,4)|padding|fill = true|
|10|(2,0)|real|true|
|11|(2,1)|real|false|
|12|(2,2)|real|true|
|13|(2,3)|real|false|
|14|(2,4)|padding|fill = true|

Padding content is fixed by `[R-SER-05]`: "at every padding position, a writer MUST
encode … the fill bit in a packed plane". Bit 7 of byte 1 (k = 15) is a **pad bit**
(P mod 8 = 7 ≠ 0), and `[R-SER-05]` — "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit" — makes it 1.

Byte 0 = bits(1,0,1,0,1,0,1,0) = 0x55. Byte 1 = bits(1,1,1,0,1,0,1,**1**) = 0xD7.

(b) Codec 1: `[R-COD-04]` — "The index entry's length therefore MUST equal the
tile's decoded size" = **2**.

**Answer: (a) `55 d7`; (b) 2**

---

## Q04 — segment CRC array and crc_of_crc_array of an all-sentinel index

G = ⌈30/12⌉ = 3, interleaved → entry_count = 3 (`[R-GEO-03]`, `[R-CNT-17]`).
One segment (⌈3/2¹⁶⌉ = 1), a 4-byte CRC array (§15.1).

All three entries are sentinels: `FF ×16 00 ×4` each (`[R-IDX-02]`), 60 bytes.
This is a **partial** segment, so §15.4's constant is unavailable: `[R-IDX-05]` —
"writers … MAY emit this constant for any **full** segment … a partial segment's
CRC MUST be computed."

CRC-32C over the 60 sentinel bytes = 0xD171D122 → stored `22 d1 71 d1`.
crc_of_crc_array = CRC-32C over those 4 bytes = 0x34C74AFB → `fb 4a c7 34`.

**Answer: (a) `22 d1 71 d1`; (b) `fb 4a c7 34`**

---

## Q05 — interleaved decoded size, disk ordinal, in-tile byte offset

Q = ΣBᵢ = 1(bool) + 8(float64) + 2(int16) + 1(bool) + 4(float32) = 16 (§14.2;
"a bool value … as a single byte … with element size 1 in the arithmetic below").
P = 3·4·5 = 60.

(a) Decoded size (interleaved) = P·Q = 60·16 = **960**.

(b) G = (10, 10, 10). Tile coords tᵢ = xᵢ div Tᵢ = (17 div 3, 9 div 4, 23 div 5) =
(5, 2, 4). `[R-GEO-06]`: s = Σ tᵢ·∏_{j>i} Gⱼ = 5·100 + 2·10 + 4 = **524**.
Interleaved → disk ordinal = s = **524**.

(c) uᵢ = (17 mod 3, 9 mod 4, 23 mod 5) = (2, 1, 3). In-tile ordinal =
Σ uᵢ·∏_{j>i} Tⱼ = 2·20 + 1·5 + 3 = 48. Channel c is index 2, so
F_c = B_a + B_b = 1 + 8 = 9. §14.2's closing form: "channel c's value at in-tile
ordinal u sits at byte u · Q + Fᶜ" = 48·16 + 9 = **777**.

**Answer: (a) 960; (b) 524; (c) 777**

---

## Q06 — planar ordinal, entry offset, segment-CRC offset, extent_length

G = (⌈1000/100⌉, ⌈3000/250⌉) = (10, 12), N = 120.
(750, 1600) → t = (7, 6) → s = 7·12 + 6 = 90.

(a) Planar disk ordinal = c·N + s (`[R-GEO-06]`) = 550·120 + 90 = **66090**.

(b) §15.1: "The entry for the tile with disk ordinal k … is the k-th entry, at
region byte 20·k" = 20·66090 = **1,321,800**.

(c) entry_count = C·N = 700·120 = 84,000. Entry array occupies
84,000·20 = 1,680,000 bytes, then the segment CRC array (§15.1). Entry 66090 lies
in segment 66090 div 65536 = 1 (§15.4). Its u32 is the 1-indexed second entry of
the array: 1,680,000 + 1·4 = **1,680,004**.

(d) `[R-CNT-17]`: 84,000·20 + ⌈84,000/65,536⌉·4 = 1,680,000 + 2·4 = **1,680,008**.

**Answer: (a) 66090; (b) 1321800; (c) 1680004; (d) 1680008**

---

## Q07 — four proposed appends against a stored layer

Baseline: G = ⌈18/10⌉ = 2, N = 2, P = 10, Q = 2, decoded size 20. Tile 0 covers
x = 0..9 (all real); tile 1 covers x = 10..19, with x = 18, 19 padding positions
holding fill 00 00 (`[R-SER-05]`). Both tiles stored in generation g.

Governing text, §20.3 step 4 (`[R-WRT-04]`): "A commit MUST NOT change a layer's
declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how
they decode — the set of padding positions (§11.3) and the content `[R-SER-05]`
fixes there, the decoded size, the byte offset of any sample within the decoded
tile image, or the codec and filter that produced the stored bytes."

**(i) 18 → 20.** G stays 2; decoded size, offsets, codec, filter unchanged. Tile 1's
two padding positions become real, and their stored bytes are the fill 00 00.
§20.3 addresses exactly this: "an extent MAY **grow**, since a position that
becomes real held that channel's fill and fill is a legal sample value — provided
the grown geometry stays within every bound the layer's own declarations impose".
The grown geometry violates no bound (codec 1; P·Q = 20). → **PERMITTED**.

**(ii) 18 → 10.** G falls to 1; tile 1 leaves the addressed set. Tile 0 is
unchanged in every respect §14 fixes. §20.3: "where it drops a tile out of the
addressed set entirely (§11.2's grid count falls), nothing is altered for a tile
the new state stores, and the commit is permitted: the de-addressed tiles' extents
become slack … Discarding data is the caller's operation and this specification
does not bar it." The neighbouring "SHOULD instead produce a new file" is a SHOULD,
and `[R-CNF-12]` — "Deviation from a SHOULD is not a violation" → **PERMITTED**.

**(iii) 18 → 16.** G = ⌈16/10⌉ = 2, so tile 1 stays addressed and stored, but
x = 16, 17 become *new padding positions*. The question stipulates no stored sample
inside the old extents equals 0x0000, so those bytes are **not** fill, and
`[R-SER-05]` would now be violated for a stored tile. §20.3's escape hatch — "a new
padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is
not what this bars" — is closed by that stipulation. The change alters "the set of
padding positions … and the content `[R-SER-05]` fixes there" for a tile stored in
the superseded generation → **BARRED**.

**(iv) codec 1 → 2.** Directly named: "the codec and filter that produced the
stored bytes". Both tiles are stored in generation g → **BARRED**.

**Answer: PERMITTED, PERMITTED, BARRED, BARRED**

---

## Q08 — eight tiles' service verdicts, and L41/L42

Geometry: G = ⌈80/10⌉ = 8, interleaved, entry_count = 8. F = 8192, F − 64 = 8128.
Slab S = 4, A_slab = 1024. `[R-SLB-02]`: interleaved → one block [0, 8); runs are
[0, 4) and [4, 8).

Classification per §15.3's table (`[R-IDX-03]`):

| k | entry | classification | verdict |
|---|---|---|---|
|0|1024 / 100, crc ok|well-formed, crc ok, decodes|SERVE-DECODED|
|1|S / S / crc 0|"valid sentinel — reads as fill" (`[R-IDX-02]`, `[R-TYP-08]`)|SERVE-FILL|
|2|1124 / 200, crc mismatch|"stored bytes fail the entry's crc → reject-tile … the entry itself is well-formed; its extent stands"; `[R-CNF-09]` bars fill|REFUSE|
|3|1324 / 50, crc ok|valid|SERVE-DECODED|
|4|S / 500|"offset = S ∧ length ≠ S … *structural*: reject-tile"|REFUSE|
|5|2048 / 300, crc ok|valid|SERVE-DECODED|
|6|2348 / 0|"length = 0 (non-sentinel) … *structural*: reject-tile"|REFUSE|
|7|2348 / 150, crc ok|valid (2498 ≤ 8128)|SERVE-DECODED|

`[R-TYP-09]`: "A reader MUST NOT return fill for a tile whose entry is malformed
(§15.3) … or whose stored bytes failed their checksum" — so 2, 4, 6 are REFUSE and
not SERVE-FILL.

**Slab invariants.** `[R-SLB-03]`: sentinels and structurally-reject-tile entries
are transparent; "An entry whose only defect is that its stored bytes fail its crc
is not transparent — its offset and length stand".

Run 0 (ordinals 0–3): stored/participating = 0 (1024, 100), 2 (1124, 200), 3
(1324, 50); ordinal 1 transparent.
- first stored offset 1024 mod 1024 = 0 ✓ (no L42)
- 1024 + 100 = 1124 ✓ ; 1124 + 200 = 1324 ✓ (no L41)

Run 1 (ordinals 4–7): 4 transparent (structural), 6 transparent (structural);
participating = 5 (2048, 300), 7 (2348, 150).
- first stored offset 2048 mod 1024 = 0 ✓ (no L42)
- 2048 + 300 = 2348 ✓ (no L41)

**Answer: (a) SERVE-DECODED, SERVE-FILL, REFUSE, SERVE-DECODED, REFUSE,
SERVE-DECODED, REFUSE, SERVE-DECODED; (b) L41 NO, L42 NO**

---

## Q09 — reserved-range type 0x0400 with MU = 1

Type 0x0400 = 1024 lies in the record-type **reserved** range 0x0003–0x7FFF
(§10.2's table). flags 0x0003 = bits 0 and 1 → MU = 1, PE = 1.

Two rows describe reserved-range types: F35 (MU = 1 specifically) and F36 (any MU
bit). §21.1 resolves the pair: "Some rows are strict specializations of others —
F1 of F6 and of F8, **F35 of F36**, L24 of L25 — and a file exhibiting a
specialization is recorded against the **narrower row**, whose detector and
detection point are the ones that apply."

F35's row: `| F35 | … | — | reader | open | [R-CNT-15] |`

Reader outcome: `[R-CNT-15]` — "An unknown record type at file scope: MU = 1 →
reject-file". Type 0x0400 is unassigned, so this is the applicable outcome class.

**Answer: (a) F35; (b) reader; (c) open; (d) reject-file**

---

## Q10 — two verdicts

**File X.** Two features beyond baseline conformance.

1. Top-level user-metadata record at encoding 0x85 (experimental, ≥ 0x80).
   §21.6 records this as a defined non-violation, and `[R-MTA-10]`: "A verifier
   meeting such a record in an otherwise conforming file **has no requirement it
   is unable to check** — the record is not among `[R-CNF-11]`'s cannot-establish
   grounds, and certification is unaffected". So this alone would leave X
   certifiable (with a report line).
2. Layer sub-record at encoding **2** (assigned), decoding to 40 MiB, declined on
   a 16 MiB bound. `[R-MTA-09]`: "A **verifier** that declines to decode a document
   on the bound above cannot establish that document's conformance and MUST NOT
   certify the file … it fixes the file's verdict as *cannot establish* only where
   the verifier established no violation elsewhere."

X is conforming in every respect, so no violation is established → **cannot
establish**.

**File Y.** Adds a set reserved flag bit 5 on a layer record. That is L47 — "Any of
a layer record's or sub-record's reserved flag bits 2-15 is set", detector
verifier, at certification — an established violation. `[R-CNF-11]`: "An
established violation takes priority: a verifier that has established any violation
reports *nonconforming*, however many requirements it was unable to check."
(The mutation would also break the directory CRC → F20; either way a violation is
established.) → **nonconforming**.

**Answer: cannot establish; nonconforming**

---

## Q11 — slack total and verdict

Claimants of the live state (§9.7, `[R-LIF-08]`; the front block and live trailer
are "claimed by the walk as well"):

| claimant | bytes |
|---|---|
| front signature block | 16 |
| directory region | 200 |
| live trailer | 64 |
| layer A tile-index region | 84 |
| layer A's 4 stored tiles | 400 |
| layer B tile-index region | 84 (discarded) |
| layer B's 2 stored tiles | 600 (discarded) |

Layer B exhibits **L42** — "A slab run's first stored tile's offset is not a
multiple of A_slab" — reject-layer, established by the walk itself.

`[R-CNT-21]`: "a rejected layer's claimants are not enumerated … and where the
rejection is one the walk itself established, L18's overlap or **L40 through L42's
placement** among them, the claimants it had already enumerated are **discarded**
with the layer … A partial total is F less the bytes claimed by the claimants the
walk did enumerate — an upper bound on the file's true slack".

Enumerated claim = 16 + 200 + 64 + 84 + 400 = 764.
Reported slack = 4096 − 764 = **3332**. (The file's true slack is 2648; 3332 is the
upper bound this specification obliges, reported as partial and naming layer B.)

Verdict: a violation was established → **nonconforming** (`[R-CNF-11]`).

**Answer: (a) 3332; (b) nonconforming**

---

## Q12 — compacted output's trailer

`[R-WRT-06]`: "It MUST mint a fresh file_id for the output — a new draw under
§9.3's randomness advice, not merely a value compared against the input's — and
generation 1 … The output trailer copies the input's unknown ignore-lane flag bits
forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the
input's version_minor".

- (a) generation = **1**.
- (b) floor = 0 (file uses only features this text defines, `[R-CNT-26]`);
  input minor = 4; greater = **4**.
- (c) flags 0x00050000 = bits 16 and 18, both in the ignore lane (16–31), both
  unimplemented by this compactor → carried forward verbatim = **00050000**.
- (d) A fresh *draw* is required, not merely a different value; and reuse "would
  break the (file_id, range) cache contract of `[R-LIF-03]`" → **NO**.

**Answer: (a) 1; (b) 4; (c) 00050000; (d) NO**

---

## Q13 — Appendix G emission order

Appendix G item 3: "For each layer in **ascending layer-name byte order**: its
stored tiles in disk-ordinal order, then its tile-index region; then any record
extents in ascending record order — **all of them after every layer's tiles and
index region**, not interleaved with them; then the directory." And: "The first
structure begins at 16 … each later structure begins where the previous one ended,
save where alignment forces a gap — … or §6.2's 64-byte trailer alignment, the
pre-trailer pad included".

Layer names are the single bytes `a` (0x61) and `b` (0x62), so layer **a** sorts
first. §6.2 / `[R-LIF-02]` step 5 put the pad then the trailer last.

**Answer: Ta Ia Tb Ib M D P R**

---

## Q14 — two lz4 layers with a zero extent

Both layers have E₀ = 0, so G₀ = ⌈0/T₀⌉ = 0, N = 0, entry_count = 0: no addressed
tiles (`[R-GEO-02]`). §17.2's note: "The cap is quantified over the layer's
*addressed* tiles, so a layer that addresses none — any dimension extent 0 … —
satisfies it whatever its tile shape declares, and codec 4 is conforming there.
… `[R-ENC-04]`'s overflow rule carries no such quantifier — it binds any sum or
product a file yields — so P·Q and P·Bᶜ are checked in an empty layer even though
this cap is not."

**Layer M.** P = ∏Tᵢ = 2³² · 2³¹ = 2⁶³ = 9,223,372,036,854,775,808, which exceeds
2⁶³ − 1. `[R-GEO-03]`/`[R-ENC-04]`: "a reader MUST treat a product exceeding
2⁶³ − 1 as a validity error at layer scope". Register row L2 names `P = ∏Tᵢ` as an
instance. (P·Q = 2⁶⁶ likewise.) → **REJECT-LAYER**.

**Layer N.** P = 2³² ; P·Q = P·B = 2³² · 8 = 2³⁵ = 34,359,738,368 ≤ 2⁶³ − 1;
N·P = 0; C·N = 0; entry_count formula = 0. Every derived product is in domain. The
lz4 cap (0x7E000000) is exceeded by the hypothetical tile size but is quantified
over addressed tiles, of which there are none → L44 does not fire. Nothing else is
defective → **CONFORMING**.

**Answer: REJECT-LAYER; CONFORMING**

---

## Q15 — five conditions, register rows

**(a) MU = 0 unassigned-type record encoding an offset in its own inline payload.**
`[R-CNT-13]` prohibits it, but §21.7 (`[R-ERR-01]`) places it among the obligations
omitted from the register: "`[R-CNT-13]`'s prohibition on an MU = 0 record encoding
file offsets in its own payload is **opaque by construction**". A file exhibiting
the condition with an experimental-range type is conforming (§21.6). → **NONE**

**(b) Interleaved bool value byte 0x02 at a position inside the extents.**
"inside the layer's extents" = a real, non-padding position (§3.2, `[R-GEO-04]`).
T2: "In an interleaved tile, a bool channel's single value byte at a real
(non-padding) sample position is neither 0x00 nor 0x01" — verifier, certification,
`[R-SER-08]`. → **T2**

**(c) Layer record flags reserved bit 7 set.**
L47: "Any of a layer record's or sub-record's reserved flag bits 2-15 is set" —
verifier, certification, `[R-CNT-12]`. → **L47**

**(d) Linearization 1 declared, ordinals assigned first-dimension-fastest; planar,
all numeric, no padding position.** §21.7: "the ordinal mappings of `[R-GEO-06]`
and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it
carries, **except where §14 constrains a byte's content** — a padding position, a
pad bit, or an interleaved boolean — and a mis-ordered image is then witnessed by
T2, T4 or T5". Here there is no padding position, no packed bool plane (hence no
pad bits) and no interleaved boolean, so no witness exists. → **NONE**

**(e) entry_count written as a 4-byte field.** §21.7: "`[R-ENC-06]`'s fixed field
widths are not a state a file can be in, since the parse is always at the widths
this specification fixes and a structure written at any other yields different
values at them, **caught by the rows for the fields that hold them**." So the
answer is not NONE — the register does carry rows such a file exercises — but the
document names no single row.

Working the minimal construction: the trailing fixed fields need 1 + 8 + 4 = 13
bytes; the writer emitted 1 + 4 + 4 = 9, so inline_length is 4 short. The parse
consumes index_encoding (1 byte), then reads 8 bytes as entry_count (the writer's
4 entry_count bytes plus its 4 crc bytes), leaving 0 bytes for crc_of_crc_array →
`[R-CNT-18]`'s "the trailing fixed fields MUST lie entirely within the inline
payload" fails, which is **L23**, instance "trailing fixed fields (index_encoding,
entry_count, crc_of_crc_array)". That overrun is guaranteed regardless of content.

Competing readings I record honestly:
- **L1** may fire *as well*, since the 8 bytes read as entry_count are
  `<4 entry_count bytes><4 crc bytes>` and will exceed 2⁶³ − 1 whenever the crc's
  top byte has bit 7 set — content-dependent, so not the determinate row.
- **NONE**, if one reads §21.7's mention of `[R-ENC-06]` as putting the condition
  wholly outside the register; but that reading contradicts the same sentence's
  rider.
- **L14** ("trailing residue") or **L21/L22**, if the writer instead padded
  inline_length to the correct length — a variant the question does not state.

I would implement **L23**.

**Answer: NONE; T2; L47; NONE; L23** (item (e) underdetermined as above)
