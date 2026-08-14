# Round 8 — quiz keyer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3842 lines, in four Read calls). I ran `wc -l` on that same file, and one
Python script that reads no files (pure arithmetic / byte packing) to check the
computations below. No ADRs, no `docs/`, no `conformance/`, no `registry.json`,
no git history, no web access, no directory listings. Prior knowledge of zstd /
LZ4 / DEFLATE and of other array formats was used only to *read* the document's
external references, never to settle a question the document itself answers.

---

## Q01 — two channel entries

§7.4 layer-record inline payload table, channel entry row:

> `C channel entries | name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes)`

and `[R-CNT-23]`: "fill length equals the type's element size".

§12.1 type table: bool = ID 1, element size 1. bfloat16 = ID 11, element size 2.
§13.2: bool fill is one byte, `0x01` = true.
§12.1's bfloat16 example: "bfloat16 1.0 is `0x3F80` … stored as the bytes `80 3F`".

Channel 0 (`m`, bool, true): `01` `6D` `01 00` `01` `01` = `016D01000101` (6 bytes)
Channel 1 (`bt`, bfloat16, 1.0): `02` `62 74` `0B 00` `02` `80 3F` = `0262740B0002803F` (8 bytes)

Concatenated, declared order: **`016D010001010262740B0002803F`** (14 bytes).

## Q02 — planar bool edge tile

Geometry: E = (5,5), T = (4,4). §11.2: Gᵢ = ⌈5/4⌉ = 2, so G = (2,2), N = 4, P = 16.
Planar, C = 1 → addressed-tile count = C·N = 4.

**(a) decoded tile image.** §14.3: planar bool plane is bit-packed LSB-first,
value k at bit k mod 8 of byte k div 8, decoded size ⌈P/8⌉ = 2 bytes.

Tile (1,1) covers coordinates 4–7 on both axes; only (4,4) is inside the extents
(§11.3, and §14.5's worked example uses exactly this geometry: "one real
position, (4, 4), and 15 padding positions"). Its in-tile position is (0,0),
in-tile ordinal 0 (§11.4).

Value 0 = false → bit 0 of byte 0 clear. All 15 padding positions carry the
channel's fill bit (`[R-SER-05]`: "at every padding position, a writer MUST
encode … the fill bit in a packed plane"); fill byte is `0x01` = true, so the
fill bit is 1. P mod 8 = 0, so there are no pad bits.

byte 0 = `1111 1110` = 0xFE; byte 1 = `1111 1111` = 0xFF → **`FEFF`**.

**(b) length field.** Codec 1 = none: "The stored bytes are the filtered image
verbatim" (`[R-COD-04]`), filter 1 = none (`[R-COD-09]`). So length = decoded
size = **2**. (`[R-COD-04]` independently requires the entry's length to equal
the decoded size under codec 1.)

**(c) index-entry offset.** §11.4: s = Σ tᵢ·∏_{j>i}Gⱼ = 1·2 + 1 = 3; planar disk
ordinal = c·N + s = 0·4 + 3 = 3. §15.1: "The entry for the tile with disk ordinal
k … is at region byte 20·k" → 20·3 = **60**.

## Q03 — interleaved shuffle

P = 2, C = 2, B_a = 1 (uint8), B_b = 2 (uint16), Q = 3. Decoded size = P·Q = 6.

§14.1 interleaved: "value k of the sequence is channel (k mod C)'s value at
in-tile ordinal k div C". Sequence: a₀=0x11, b₀=0x2233, a₁=0x44, b₁=0x5566.
Little-endian (`[R-ENC-01]`): decoded image = `11 33 22 44 66 55`.

§17.3 byte-shuffle: stride s = Q = 3 for an interleaved tile; n = L/s = 6/3 = 2;
"the filtered image places byte i of group j at offset i · n + j".

- group 0 = `11 33 22`, group 1 = `44 66 55`
- offsets: (i=0,j=0)→0:11, (i=0,j=1)→1:44, (i=1,j=0)→2:33, (i=1,j=1)→3:66,
  (i=2,j=0)→4:22, (i=2,j=1)→5:55

Filtered = `11 44 33 66 22 55`. Codec 1 stores it verbatim → **`114433662255`**.

## Q04 — 3-D interleaved coordinate

E = (10,9,7), T = (4,5,3). G = (⌈10/4⌉, ⌈9/5⌉, ⌈7/3⌉) = (3,2,3).
Coordinate (7,6,5): t = (1,1,1), u = (3,1,2) (§11.4, tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ).

**(a)** s = t₀·(G₁·G₂) + t₁·G₂ + t₂ = 1·6 + 1·3 + 1 = 10. Interleaved ⇒ disk
ordinal = s = **10** (`[R-GEO-06]`: "The disk tile ordinal … is s for an
interleaved layer").

**(b)** in-tile ordinal u = u₀·(T₁·T₂) + u₁·T₂ + u₂ = 3·15 + 1·3 + 2 = 50.
Q = 1 + 8 + 2 = 11; F_c for channel index 2 = B_a + B_b = 9.
§14.2: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ" →
50·11 + 9 = **559**.

## Q05 — slack total

F = 1024. Claimants of the live committed state (§9.7 `[R-LIF-08]`, §5.2
`[R-CNT-02]`):

- front signature block [0, 16) — 16
- layer record's extent = the tile-index region [16, 100) — 84
  (`[R-CNT-17]` check: 4×20 + ⌈4/2¹⁶⌉×4 = 84 ✓; §9.7: "the region enters the
  walk once, as that record's extent")
- entry 0's stored tile [100, 220) — 120
- entry 1: valid sentinel — contributes no extent (§15.2, §9.7)
- entry 2's stored tile [256, 320) — 64. Its bytes fail its crc, but §15.3:
  "An entry whose only defect is that its stored bytes fail its crc is
  well-formed … its extent stands and it keeps its place in … the coverage
  walk." So it *is* claimed.
- entry 3: offset 8 < 16, non-sentinel → §15.3 *structural*: reject-tile. §15.3:
  such an entry contributes "none to `[R-LIF-08]`'s coverage walk, whose slack
  total therefore includes whatever bytes such an entry nominally addresses."
  §9.7 adds that this "does not make the walk incomplete".
- directory [832, 928) — 96
- live trailer [960, 1024) — 64

Claimed total = 16+84+120+64+96+64 = 444. Slack = 1024 − 444 = **580**
(gaps: [220,256)=36, [320,832)=512, pre-trailer pad [928,960)=32 → 36+512+32=580).

The walk completes and the verifier does not stop early, so `[R-CNT-21]`'s
partial-total clause does not apply: a full total is reported. (The verifier also
establishes T1 and T8 violations, but the question asks only for the slack count.)

## Q06 — index region arithmetic, entry_count = 2¹⁷

**(a)** `[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4
= 131072×20 + 2×4 = 2,621,440 + 8 = **2621448**.

**(b)** §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))".
100000 div 65536 = 1 → segment 1 covers entries [65536, 131072), i.e. region
bytes [65536×20, 131072×20) = **[1310720, 2621440)**.

**(c)** §15.1: the segment CRC array follows the entry array contiguously, at
region byte entry_count×20 = 2,621,440, and "the s-th u32 of the segment CRC
array" is segment s's. s = 1 → **[2621444, 2621448)**.

## Q07 — planar slab run

**(a)/(b)** `[R-GEO-06]`: planar disk ordinal = c·N + s. 19 = 1·10 + 9 →
channel index **1**, spatial ordinal **9**.

**(c)** `[R-SLB-02]`: "for a planar layer each channel block [c·N, (c+1)·N) —
runs never span channel blocks … Run r of a block starts at ordinal
block_start + r·S." Block for c = 1 is [10, 20); runs start at 10, 14, 18.
Ordinal 19 falls in the run beginning at **18** (a final run of 2 < S = 4, which
`[R-SLB-02]` expressly permits).

## Q08 — reserved-range top-level record, MU = 0

Type 0x0005 is in the reserved range 0x0003–0x7FFF (§10.2 table).

**(a)** `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 →
reject-file; MU = 0 → ignore-record." → **ignore-record**.

**(b)** Same rule: "one from the reserved range is a value this specification
has not assigned — emitting it is a violation, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing scope."
Register row F39 (detector *verifier*, outcome reject-file) covers exactly this
"whatever its MU bit". The verifier has established a violation, and §2.3: "An
established violation takes priority: a verifier that has established any
violation reports *nonconforming*." → **nonconforming**.

(F38 is the MU = 1 specialization and does not apply here.)

## Q09 — experimental-range layer sub-record, MU = 1

Type 0x8001 ≥ 0x8000 = experimental range (§10.2).

**(a)** `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer —
never reject-file". → **reject-layer**.

**(b)** §21.6: "an **experimental-range record type carrying MU = 1** (§10.2,
§10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the
file conforming all the same, since the prohibition on publishing experimental
values binds a writer's conduct and not the bytes." → **yes**, conforming.
(§21.6 also notes this case is deliberately *not* a register row.)

**(c)** §2.3: *cannot establish* is available "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)". No violation is
established anywhere else, so → **cannot establish**.

## Q10 — declined metadata decode plus L28

The smallest bound §18.2 permits: "a reader instead decodes with a bound of its
own choosing, no smaller than §21.9's user-metadata guarantee" = 16 MiB. A 20 MiB
document exceeds it, so the decline is licensed.

**(a)** The layer record declares entry_count = 0 with crc_of_crc_array =
0x00000001, which is register row L28 / `[R-CNT-23]`: "a nonzero
crc_of_crc_array with entry_count = 0 — as a validity error at layer scope."
That is an established violation. §2.3: "a verifier that has established any
violation reports *nonconforming*, however many requirements it was unable to
check." → **nonconforming**.

**(b)** `[R-MTA-09]`: "the decline is not a finding that the file is
nonconforming and a verifier MUST NOT report it as one." → **no**. (It must
still be reported as an unchecked requirement, but not as a nonconformance
finding.)

## Q11 — segment CRC failure mid-request

**(a)** `[R-IDX-04]`: "any mismatch or cross-check failure (`[R-CNT-17]`) is
reject-layer." → **reject-layer**. (Confirmed by `[R-RDR-02]`: "index-chain
failures take layer scope (`[R-IDX-04]`) although their detection point is tile
use", and by register row L39.)

**(b)** §2.4 reject-layer: "The outcome is prospective: it bars further service
from the layer, and does not retroactively invalidate content already returned
under §19.2's validation timing." §19.4 step 8: "the bar is prospective, so
values the reader has already returned under §19.2's timing stand". → **no**.

**(c)** §19.4 step 8: a layer-scope failure "bars the request's remaining
entries and all further service from the layer". → **no**.

## Q12 — commit that only changes a fill value

**(a)** `[R-LIF-02]` step 1: "begin writing at exactly F". Nothing in step 2 is
needed — §20.3's example (c) names exactly this case: "A change confined to the
directory — clearing a slab declaration, renaming a layer, changing a channel's
fill value. Only the directory is re-emitted." So the directory begins at
**4096**.

**(b)** Directory = [4096, 4396). `[R-LIF-02]` step 5: "append the pad to the
next 64-byte boundary". Next boundary above 4396 is 4416 → **20** pad bytes.

**(c)** Trailer occupies [4416, 4480); committed_file_length = **4480**
(multiple of 64 ✓, §6.2).

**(d)** Step 5: "generation one greater than the prior trailer's" → **8**.

**(e)** §20.3 step 4 / `[R-WRT-05]`: "A layer whose record alone changes keeps
its extent slot, pointing at the existing region". The fill value lives in the
layer record's inline payload, not the index, and the new fill is the same byte
length, so the record's framing is unchanged in shape. → **no**.

## Q13 — appender against minor 5 with ignore-lane bits set

**(a)** `[R-CNT-26]`: "A writer SHOULD emit the lowest version_minor that
defines every feature present in the file — for a file expressible under this
text, 0 — and an appender the maximum of that floor and the prior trailer's
minor". max(0, 5) = **5**.

**(b)** Trailer offset 12 is the u32 `flags` field (§6.2 layout table). Bits 16
and 17 are ignore-lane bits (16–31). `[R-CNT-08]`: "An updater MUST copy forward
unknown ignore-lane bits of the file it modifies and MUST NOT clear them" — this
overrides the "writer creating a file under this text MUST write flags = 0"
clause, which binds creation. flags = 0x00030000, little-endian → **`00000300`**.

**(c)** §6.3: "a set ignore-lane bit is not a file-conformance violation … files
carrying them are conforming files this text's readers ignore"; §21.6 lists both
"An ignore-lane flag bit (16–31) is set → the file is conforming" and
"version_minor is higher than this text defines → Accepted; minors never gate".
→ **yes**.

## Q14 — zstd window larger than decoded size

Window_Size = 1024 > decoded size 512. `[R-COD-06]`: writers "MUST NOT declare a
window size exceeding the tile's decoded size; a reader MUST treat either as a
validity error at tile scope, both being header-checkable."

**(a)** **reject-tile**. **(b)** register row **T21**: "Codec 3 (zstd) and the
frame declares a window size larger than the tile's decoded size" — reader
detector, tile use, `[R-COD-06]`.

Everything else stated (magic present, no dictionary ID, no content checksum, FCS
absent, exact decode to 512, exact consumption, crc matches) is conforming, so
T17–T20, T22, T24, T25 do not fire. §17.2's note that a sub-1-KiB tile is
"encodable under codec 3 only as a single-segment frame" is the same conclusion
from the other side.

## Q15 — empty layer names

**File 1.** Both name fields are the single byte `0x00`, both within
inline_length. §19.1 step 4 is decisive: "Uniqueness is decided first, and over
the raw name bytes whether or not each name is itself well-formed —
`[R-ENC-12]` makes name comparison a byte comparison, which needs no valid
name — so two layers whose name fields are byte-identical are a duplicate even
when neither name is valid." `[R-ENC-15]`: "a duplicate layer name is a
file-scope error (reject-file)". → **reject-file, F6** ("Two layer records in
the live directory carry byte-identical name fields, both obtainable within
their records' inline_length").

L6 (empty layer name → reject-layer) is also exhibited, twice, but the reader's
applied outcome is the file-scope one, decided first by §19.1's ordering; F6 is
the row the duplicate condition is recorded against.

**File 2.** Names `""` and `"a"` are byte-distinct, so no duplicate. `a` is a
valid name (non-empty, ≤255 bytes, no U+0000–U+001F). The first record's name has
length prefix 0 → `[R-ENC-12]`: "A name is: non-empty …; a reader MUST treat such
a name as a validity error at the owning scope", and §7.4 makes the layer record's
inline payload layer-scoped. → **reject-layer, L6** ("A layer record's name has
length prefix 0 (empty name)"), detected at open per the register.
