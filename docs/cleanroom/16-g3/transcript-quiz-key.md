# Cleanroom round 16 — quiz KEY transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole file, in four `Read` calls). I ran `wc` on that file and one `grep` against
that file only. I ran one Python script I wrote myself in the scratchpad
(`calc.py`), which reads no project files — it implements CRC-32C and does the
arithmetic. No ADRs, no `docs/`, no `conformance/`, no `registry.json`, no git
history, no web. I did not read or list the round16 output directory.

My CRC-32C implementation is validated against three constants the spec itself
states: `CRC32C("123456789") = 0xE3069283`; §7.4's worked example
(4-sentinel segment → `0x80A34955`, crc_of_crc_array → `0xC4EE982E`);
§15.4's full all-sentinel segment constant `0xEECB3BB2`; and Appendix A's
trailer CRC `0xE00938D2`. All four reproduce.

---

## Q01 — trailer bytes [60, 64)

Trailer layout (§6.2 table). Field values:

- [0,8) magic `8A 4E 52 41 54 0D 0A 1A`
- [8,10) version_major = 1
- [10,12) version_minor: `[R-CNT-26]` — "A writer SHOULD emit the lowest
  version_minor that defines every feature present in the file — for a file
  expressible under this text, 0 — and an appender the maximum of that floor
  and the prior trailer's minor". Floor 0, prior 0 → **0**.
- [12,16) flags: `[R-CNT-08]` — "a writer creating a file under this text MUST
  write flags = 0"; an updater copies forward unknown ignore-lane bits, and
  there are none (every prior trailer carried flags = 0) → **0**.
- [16,24) generation = 3
- [24,32) dir_offset = 16
- [32,40) dir_length = 4096
- [40,48) committed_file_length = 4288 (4288 mod 64 = 0 ✓; 16+4096 = 4112 ≤ 4288−64 = 4224 ✓)
- [48,56) file_id = 0x00000000DEADBEEF → `EF BE AD DE 00 00 00 00`
- [56,60) reserved = 4 zero bytes (§6.2 "Valid values: zero")

Bytes [0,60):
`8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00 03 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00 00 10 00 00 00 00 00 00 c0 10 00 00 00 00 00 00 ef be ad de 00 00 00 00 00 00 00 00`

CRC-32C = **0x24006CA2**, stored little-endian.

**Answer: `a2 6c 00 24`** — confidence high.

---

## Q02 — layer record header [4,8) and [16,24)

(a) inline_length. §7.4 payload, packed in table order, no padding
(`[R-CNT-18]`). Calibrated against §7.4's own worked example (name 4 + nine
scalars 34; dimension entry 18; channel entry 12; trailing fixed fields 13).

| Part | Bytes |
|---|---|
| name `grid` (1+4) | 5 |
| layout…channel count (9 scalars: 1+2+2+2+8+8+8+1+2) | 34 |
| dim `row` (1+3+8+8) | 20 |
| dim `col` (1+3+8+8) | 20 |
| chan `u` float64 (1+1 + 2 + 1+8) | 13 |
| chan `flag` bool (1+4 + 2 + 1+1) | 9 |
| index_encoding + entry_count + crc_of_crc_array (1+8+4) | 13 |
| sub-records | 0 |
| **total** | **114** |

114 = 0x72 → u32 LE `72 00 00 00`.

(b) extent_length. Planar, so addressed-tile count = C·N (`[R-GEO-03]`).
G = (⌈2048/64⌉, ⌈4096/64⌉) = (32, 64); N = 2048; C = 2 → entry_count = 4096.
`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 4096×20 + 1×4 = 81920 + 4 = **81924** = 0x00014004 →
u64 LE `04 40 01 00 00 00 00 00`.

(A = 4096 with S = 0 is legal — `[R-CNT-16]` only bars A ≠ 0 *and* S ≠ 0;
alignment binds stored-tile offsets, not the index region.)

**Answer: (a) `72 00 00 00`; (b) `04 40 01 00 00 00 00 00`** — high.

---

## Q03 — packed planar bool tile

G = (⌈3/3⌉, ⌈4/5⌉) = (1,1), N = 1, P = 3·5 = 15. Planar bool → §14.3 packed
plane, decoded size ⌈15/8⌉ = 2.

In-tile ordinal k = u_i·T_j + u_j = 5·u_i + u_j (§11.4, permanent row-major).
Real coordinates i∈[0,3), j∈[0,4); u_j = 4 is a padding position (§11.3), whose
content is the channel's fill bit (`[R-SER-05]`) = 1.

| k | (i,j) | value |
|---|---|---|
|0|(0,0)|1| |1|(0,1)|0| |2|(0,2)|1| |3|(0,3)|0| |4|pad|1|
|5|(1,0)|0| |6|(1,1)|1| |7|(1,2)|0| |8|(1,3)|1| |9|pad|1|
|10|(2,0)|1| |11|(2,1)|0| |12|(2,2)|1| |13|(2,3)|0| |14|pad|1|

Byte 0 = bits 0–7 = k0..k7 = 1,0,1,0,1,0,1,0 → 1+4+16+64 = 0x55.
Byte 1 = bits 0–6 = k8..k14 = 1,1,1,0,1,0,1; bit 7 is the sole pad bit
(P mod 8 = 7), carrying the fill bit 1 (`[R-SER-05]`) →
1+2+4+16+64+128 = 215 = 0xD7.

(b) Codec 1 → `[R-COD-04]`: "The index entry's length therefore MUST equal the
tile's decoded size" = 2.

**Answer: (a) `55 d7`; (b) 2** — high.

---

## Q04 — segment CRC array and crc_of_crc_array, all sentinel

G = ⌈30/12⌉ = 3; interleaved → entry_count = 3. Segment CRC array is
⌈3/2¹⁶⌉ × 4 = 4 bytes, one segment covering entries [0,3).

The segment is **partial**, so `[R-IDX-05]`'s 0xEECB3BB2 constant does not
apply: "a partial segment's CRC MUST be computed."

CRC-32C over 60 bytes = 3 × (`FF`×16 `00`×4) = **0xD171D122** → `22 d1 71 d1`.
CRC-32C over those 4 bytes = **0x34C74AFB** → `fb 4a c7 34`.

**Answer: (a) `22 d1 71 d1`; (b) `fb 4a c7 34`** — high.

---

## Q05 — interleaved rank-3 tile

Q = ΣB = 1(bool a) + 8(float64 b) + 2(int16 c) + 1(bool d) + 4(float32 e) = 16.
P = 3·4·5 = 60.

(a) decoded size = P·Q = 60·16 = **960** (§14.2, interleaved row).

(b) G = (10,10,10). t = (17 div 3, 9 div 4, 23 div 5) = (5,2,4).
s = Σ tᵢ·∏_{j>i}Gⱼ = 5·100 + 2·10 + 4 = **524**. Interleaved → disk ordinal = s.

(c) u = (17 mod 3, 9 mod 4, 23 mod 5) = (2,1,3);
in-tile ordinal = 2·(4·5) + 1·5 + 3 = 48.
Channel c has index 2; F_c = 1+8 = 9.
Offset = u·Q + F_c = 48·16 + 9 = **777** (§14.2's closing example gives exactly
this form).

**Answer: (a) 960; (b) 524; (c) 777** — high.

---

## Q06 — planar index arithmetic

G = (⌈1000/100⌉, ⌈3000/250⌉) = (10, 12); N = 120; C = 700;
entry_count = C·N = 84000.

t = (750 div 100, 1600 div 250) = (7, 6); s = 7·12 + 6 = 90.

(a) disk ordinal = c·N + s = 550·120 + 90 = **66090** (`[R-GEO-06]`).
(b) entry at region byte 20·k = 20·66090 = **1,321,800** (`[R-IDX-01]`).
(c) entry array is 84000·20 = 1,680,000 bytes; segment CRC array follows
contiguously. Segments = ⌈84000/2¹⁶⌉ = 2. Entry 66090 lies in segment
66090 div 65536 = 1. Its CRC is the 1-indexed-from-0 u32:
1,680,000 + 1·4 = **1,680,004**.
(d) extent_length = 1,680,000 + 2·4 = **1,680,008** (`[R-CNT-17]`).

**Answer: (a) 66090; (b) 1321800; (c) 1680004; (d) 1680008** — high.

---

## Q07 — four proposed appends

Governing text: §20.3 step 4 (`[R-WRT-04]`): "A commit MUST NOT change a
layer's declarations in a way that alters, for any tile that layer stores **in
the generation this commit supersedes**, what §14 fixes for its stored bytes or
how they decode — the set of padding positions (§11.3) and the content
`[R-SER-05]` fixes there, the decoded size, the byte offset of any sample
within the decoded tile image, or the codec and filter that produced the stored
bytes."

Geometry at g: E = 18, T = 10, G = 2. Tile 0 covers x 0–9 (all real); tile 1
covers x 10–19, real 10–17, padding 18–19 holding fill 0x0000. Both stored.

**(i) 18 → 20.** G stays 2; entry_count and extent_length unchanged; decoded
size unchanged. Positions 18,19 stop being padding and become real samples
whose stored bytes are the fill. §20.3 permits this in terms: "an extent MAY
**grow**, since a position that becomes real held that channel's fill and fill
is a legal sample value — provided the grown geometry stays within every bound
the layer's own declarations impose". Every bound holds (codec 1 length =
decoded size 20 unchanged; no lz4 cap; no overflow). → **PERMITTED**.

**(ii) 18 → 10.** G falls 2 → 1; tile 1 drops out of the addressed set. §20.3:
"where it drops a tile out of the addressed set entirely (§11.2's grid count
falls), nothing is altered for a tile the new state stores, and the commit is
permitted". Tile 0's padding set (empty), decoded size (20), offsets, codec,
filter all unchanged. `[R-CNT-17]` obliges entry_count 1 and a re-emitted index
region; tile 1's extent becomes slack. The "SHOULD instead produce a new file"
sentence is a SHOULD, not a violation (`[R-CNF-12]`). → **PERMITTED**.

**(iii) 18 → 16.** G stays 2, so tile 1 remains addressed **and stored**.
Padding along that tile becomes x 16–19 instead of 18–19. The new padding
positions 16 and 17 must, by `[R-SER-05]`, encode the fill — and the question
states no stored sample inside the extents equals 0x0000, so those stored bytes
do *not* already hold the fill. §20.3's escape clause ("a new padding position
whose stored byte already holds the fill `[R-SER-05]` fixes — is not what this
bars") therefore does not apply; the change alters "the content `[R-SER-05]`
fixes there" for a tile the prior generation stores. → **BARRED**.

**(iv) codec 1 → 2.** Directly named: "the codec and filter that produced the
stored bytes". Both tiles are stored in g and their bytes were produced under
codec 1. → **BARRED**.

**Answer: PERMITTED, PERMITTED, BARRED, BARRED** — high.

---

## Q08 — eight entries, deflate, slab S=4 / A_slab=1024

G = ⌈80/10⌉ = 8; interleaved → entry_count = 8; decoded size = P·Q = 10·1 = 10.
F − 64 = 8128.

Classification per §15.3 (`[R-IDX-03]`):

| ord | entry | class | verdict |
|---|---|---|---|
|0|1024/100, crc ok|well-formed, decodes|SERVE-DECODED|
|1|S/S/crc 0|valid sentinel — reads as fill (`[R-TYP-08]`)|SERVE-FILL|
|2|1124/200, crc mismatch|"stored bytes fail the entry's crc → reject-tile"; `[R-CNF-09]`/`[R-TYP-09]` forbid fill|REFUSE|
|3|1324/50, crc ok|well-formed|SERVE-DECODED|
|4|offset = S, length ≠ S|*structural* reject-tile (row 3 of §15.3)|REFUSE|
|5|2048/300, crc ok|well-formed|SERVE-DECODED|
|6|2348/0|length = 0 non-sentinel → *structural* reject-tile|REFUSE|
|7|2348/150, crc ok|well-formed|SERVE-DECODED|

**Slab check.** Interleaved → single block [0,8); runs of S = 4:
run 0 = ordinals 0–3, run 1 = ordinals 4–7 (`[R-SLB-02]`).

`[R-SLB-03]`: sentinels are transparent; entries §15.3 classifies reject-tile
on a *structural* ground are transparent; "An entry whose only defect is that
its stored bytes fail its crc is **not** transparent — its offset and length
stand, and the packing relation reads them as it does any other stored tile's".

- Run 0 stored tiles in ordinal order: 0 (1024,100), **2 (1124,200)**, 3 (1324,50).
  First offset 1024; 1024 mod 1024 = 0 ✓ (no L42).
  Packing: 1024+100 = 1124 ✓; 1124+200 = 1324 ✓ (no L41).
- Run 1 stored tiles: entries 4 and 6 are structurally transparent → 5 (2048,300),
  7 (2348,150). First offset 2048; 2048 mod 1024 = 0 ✓ (no L42).
  Packing: 2048+300 = 2348 ✓ (no L41).

**Answer: (a) SERVE-DECODED, SERVE-FILL, REFUSE, SERVE-DECODED, REFUSE,
SERVE-DECODED, REFUSE, SERVE-DECODED; (b) L41 NO, L42 NO** — high.

---

## Q09 — reserved-range top-level type with MU = 1

type 0x0400 ∈ 0x0003–0x7FFF = the **reserved** range (§10.2 table).
flags 0x0003 = MU 1, PE 1 — reserved bits 2–15 clear, so no L47/F26; MU=1/PE=1
so no F25; and the type is unassigned so §7.3's fixed-flag row (F28) does not
reach it. inline_length 0 and slot (0,0) are both legal.

Two rows could match: F35 (reserved-range type with MU = 1; reader/open) and
F36 (reserved-range type whatever its MU bit; verifier/certification). §21.1
resolves it: "Some rows are strict specializations of others — F1 of F6 and of
F8, **F35 of F36**, L24 of L25 — and a file exhibiting a specialization is
recorded against the narrower row, whose detector and detection point are the
ones that apply."

Reader outcome: `[R-CNT-15]` — "An unknown record type at file scope: MU = 1 →
reject-file".

**Answer: (a) F35; (b) reader; (c) open; (d) reject-file** — high.

---

## Q10 — two verdicts

**File X.** Conforming in every respect.
- Top-level user-metadata at encoding 0x85 (experimental, ≥ 0x80): §21.6 —
  "Ignored (ignore-record); the file is conforming… No document rule attaches
  at such an encoding, so a verifier certifies, reporting the record it
  ignored." `[R-MTA-10]`: "A verifier meeting such a record in an otherwise
  conforming file has no requirement it is unable to check — the record is not
  among `[R-CNF-11]`'s cannot-establish grounds". Not a bar, not a ground.
- Layer sub-record at encoding 2, would decode to 40 MiB, verifier's bound is
  16 MiB: `[R-MTA-09]` — "A **verifier** that declines to decode a document on
  the bound above cannot establish that document's conformance and MUST NOT
  certify the file… it fixes the file's verdict as *cannot establish* only
  where the verifier established no violation elsewhere". No violation
  elsewhere. → **cannot establish**.

**File Y.** Adds a set reserved bit 5 in a layer record's flags → row L47
("Any of a layer record's or sub-record's reserved flag bits 2-15 is set",
detector verifier, `[R-CNT-12]`), an established violation. §2.3: "An
established violation takes priority: a verifier that has established any
violation reports *nonconforming*, however many requirements it was unable to
check". → **nonconforming**.

**Answer: cannot establish; nonconforming** — high.

---

## Q11 — partial slack total

Claimants (`[R-CNT-02]`, §9.7 `[R-LIF-08]`), F = 4096:

| claimant | bytes |
|---|---|
| front signature block [0,16) | 16 |
| live directory region | 200 |
| live trailer [4032,4096) | 64 |
| layer A tile-index region | 84 |
| layer A stored tiles 4 × 100 | 400 |
| *layer B tile-index region* | *84* |
| *layer B stored tiles 2 × 300* | *600* |

Layer B exhibits L42 ("A slab run's first stored tile's offset is not a
multiple of A_slab", verifier, reject-layer). `[R-CNT-21]`: "a rejected layer's
claimants are not enumerated… and where the rejection is one the walk itself
established, L18's overlap or **L40 through L42's placement** among them, the
claimants it had already enumerated are **discarded with the layer**… the
verifier MUST report the total as partial. A partial total is F less the bytes
claimed by the claimants the walk did enumerate."

Enumerated = 16 + 200 + 64 + 84 + 400 = 764.
Partial total = 4096 − 764 = **3332**. (True slack would be 2648; a partial
total is an upper bound, never an under-count — consistent.)

Verdict: an established violation ⇒ **nonconforming** (§2.3).

**Answer: (a) 3332; (b) nonconforming** — high.

---

## Q12 — compacted output's trailer

`[R-WRT-06]`: "It MUST mint a fresh file_id for the output — a new draw under
§9.3's randomness advice, not merely a value compared against the input's —
and generation 1… The output trailer copies the input's unknown ignore-lane
flag bits forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s
floor and the input's version_minor."

flags 0x00050000 = bits 16 and 18, both in the ignore lane (16–31) — no
incompat bit, so the compactor is not obliged to refuse; the two set bits are
carried forward unchanged.

(a) generation = **1**.
(b) `[R-CNT-26]`'s floor for a file expressible under this text = 0; input's
minor = 4; greater = **4**.
(c) **00050000**.
(d) Reusing the input's file_id is exactly what `[R-WRT-06]` forbids
("reusing the input's would break the (file_id, range) cache contract of
`[R-LIF-03]`, since relocation puts different bytes at the same ranges") →
**NO**.

— high.

---

## Q13 — Appendix G emission order

Item 3: "For each layer in ascending layer-name byte order: its stored tiles in
disk-ordinal order, then its tile-index region; then any record extents in
ascending record order — all of them after every layer's tiles and index
region, not interleaved with them; then the directory." And: "each later
structure begins where the previous one ended, save where alignment forces a
gap — a declared A or A_slab, or §6.2's 64-byte trailer alignment, the
pre-trailer pad included".

Names `a` (0x61) < `b` (0x62), so layer a precedes layer b.

**Answer: Ta Ia Tb Ib M D P R** — high.

---

## Q14 — two lz4 layers with a zero extent

Both layers: E_p = 0 → G_p = ⌈0/T_p⌉ = 0 → N = 0 → zero addressed tiles,
entry_count = 0, extent slot (0,0), crc_of_crc_array = 0 (`[R-GEO-02]`,
`[R-CNT-17]`, `[R-CNT-23]`). `[R-COD-07]`'s lz4 0x7E000000 cap is quantified
over *addressed* tiles; §17.2's Note is explicit: "a layer that addresses none
— any dimension extent 0 — satisfies it whatever its tile shape declares, and
codec 4 is conforming there. … `[R-ENC-04]`'s overflow rule carries no such
quantifier — it binds any sum or product a file yields — **so P·Q and P·Bᶜ are
checked in an empty layer even though this cap is not**."

**Layer M.** P = ∏Tᵢ = 2³² · 2³¹ = 2⁶³ = 9,223,372,036,854,775,808, which
exceeds 2⁶³ − 1 by exactly one. `[R-ENC-04]` / row L2 lists `P = ∏Tᵢ` as an
instance: a validity error at layer scope. → **REJECT-LAYER**.

**Layer N.** P = 2¹⁶ · 2¹⁶ = 2³² = 4,294,967,296. Q = 8. P·Q = 2³⁵ =
34,359,738,368 ≪ 2⁶³ − 1. N = 0, so N·P = 0, C·N = 0, the index formula = 0.
Every Tᵢ ≥ 1 and in domain. Decoded size 32 GiB blows past both the lz4 cap and
§21.9's 256 MiB guarantee, but the cap is unquantified here and §21.9 states
minimum guarantees, not caps (`[R-ERR-03]`). → **CONFORMING**.

**Answer: REJECT-LAYER; CONFORMING** — high.

---

## Q15 — five conditions → register rows

**(a)** MU = 0 unassigned top-level record encoding a file offset in its own
inline payload. `[R-CNT-13]` prohibits it; §21.7 `[R-ERR-01]` omits it from the
register: "`[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets
in its own payload is **opaque by construction**." → **NONE**.

**(b)** Interleaved bool value byte 0x02 at a position inside the extents =
a real (non-padding) position → **T2** (verifier, `[R-SER-08]`; the padding
counterpart would be T4).

**(c)** Layer record flags reserved bit 7 set → **L47** ("Any of a layer
record's or sub-record's reserved flag bits 2-15 is set").

**(d)** Mis-assigned spatial ordinals under linearization 1, planar, all
numeric channels, no padding position — hence no pad bits either (pad bits
exist only in packed bool planes, §14.3) and no interleaved boolean. §21.7:
"the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
structurally valid tile whatever values it carries, **except** where §14
constrains a byte's content — a padding position, a pad bit, or an interleaved
boolean — and a mis-ordered image is then witnessed by T2, T4 or T5". None of
the three exceptions is present → no witness. → **NONE**.

**(e)** entry_count written 4 bytes wide. §21.7: "`[R-ENC-06]`'s fixed field
widths are not a state a file can be in, since the parse is always at the
widths this specification fixes and a structure written at any other yields
different values at them, **caught by the rows for the fields that hold
them**." So the register does carry rows such a file exercises — NONE is wrong.
For the otherwise-conforming layer record described (no sub-records mentioned),
the payload is 4 bytes short of what the parse requires: after index_encoding
the parse takes 8 bytes for entry_count (consuming the 4 written plus the 4
crc_of_crc_array bytes) and then has 0 bytes left for crc_of_crc_array →
truncation of the trailing fixed fields → **L23** ("A declared region of the
layer record's inline payload does not lie entirely within inline_length",
instance "trailing fixed fields (index_encoding, entry_count,
crc_of_crc_array)").

*Caveat, recorded honestly:* the condition as stated does not by itself pin one
row — a layer record that also carried sub-records would parse a garbage
entry_count from the shifted bytes and exercise L21/L22 (or L1) instead, with
residue in the sub-record walk. The question's "single row" plus "otherwise
conforming" framing is what selects the no-sub-record construction, and only
that construction yields exactly one row. L23 is what I would implement.

**Answer: NONE, T2, L47, NONE, L23** — (e) medium, rest high.
