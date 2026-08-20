# Cleanroom round 13 — quiz answerer transcript

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(whole document, lines 1–4128, in four Read calls). No other file in the
repository was read, listed, or grepped. No git history, no ADRs, no
conformance corpus, no registry.json, no web access. Ran two local Python
scripts I wrote myself in the scratchpad (`calc.py`, `calc2.py`) that read
no files — CRC-32C, byte-shuffle, bit-packing, and integer arithmetic only.
Wrote this transcript. Did not read or list the output directory.

**Self-validation of my tooling.** My CRC-32C reproduces all three constants
the document itself publishes: CRC-32C("123456789") = 0xE3069283 (§4.5),
CRC-32C(∅) = 0x00000000 (§4.5), Appendix A's trailer CRC 0xE00938D2, §7.4's
`sst` example (four sentinel entries → 0x80A34955; crc_of_crc_array →
0xC4EE982E), and §15.4's all-sentinel full-segment constant 0xEECB3BB2. My
byte-shuffle reproduces §17.3's worked example byte for byte. So the
arithmetic below rests on machinery the document itself pins.

---

## Q01 — extent growth (5,5)→(8,8), tiles (4,4), all four tiles stored

Geometry before: G = (⌈5/4⌉, ⌈5/4⌉) = (2,2), N = 4, interleaved →
addressed-tile count 4 (§11.2 `[R-GEO-03]`). After: G = (⌈8/4⌉, ⌈8/4⌉) =
(2,2), N = 4. **Grid counts unchanged**, so entry_count stays 4 and
extent_length stays 84.

What *does* change for stored tiles: the padding-position set. Before, tile
(0,1) has real x = 4 only, tile (1,0) real y = 4 only, tile (1,1) exactly one
real position (4,4) and 15 padding positions (§14.5's own worked example is
this very geometry). After the growth, every position of all four tiles is
real; no padding positions remain.

§20.3 step 4 `[R-WRT-04]` prohibits exactly that class of change:

> "A commit MUST NOT change a layer's declarations in a way that alters, for
> any tile that layer stores, what §14 fixes for its stored bytes or how they
> decode — the set of padding positions (§11.3) and the content `[R-SER-05]`
> fixes there, the decoded size, the byte offset of any sample within the
> decoded tile image, or the codec and filter that produced the stored bytes."

— but the same paragraph carves the case out explicitly:

> "and an extent MAY always **grow**, since a position that becomes real held
> that channel's fill and fill is a legal sample value."

The `since` clause reasons about precisely this situation: `[R-SER-05]` had
forced those padding positions to hold `CD AB`, so after the growth they are
real samples reading 0xABCD — a legal uint16. §11.1's rationale confirms the
direction of travel ("Extents grow; they do not shrink") and the cost model
("Growth that leaves every grid count ⌈Eᵢ/Tᵢ⌉ unchanged touches the
directory alone").

(a) **yes** — the growth carve-out governs; nothing else in the layer changes.

(b) **no** — `[R-WRT-04]`: "Every layer whose stored-tile set or index content
this commit changes has its tile-index region re-emitted in full … A layer
whose record alone changes keeps its extent slot, pointing at the existing
region". Stored-tile set unchanged, entry_count unchanged, every entry's
bytes unchanged → index content unchanged. §5.1's example says the same:
"a layer the commit does not touch keeps its extent slot pointing where it
always pointed". This is §20.3 example shape (c), a change confined to the
directory.

(c) **no** — the growth is permitted *because* the stored bytes stay valid;
re-emitting them is exactly what the carve-out makes unnecessary.

**Answer: `yes; no; no`**

Noted oddity: the general prohibition and the growth permission are in
textual tension (growth *does* alter the padding-position set), resolved
only by reading the `since` clause as the reason the exception is safe.
That reading is the only one that gives the exception any work to do.

---

## Q02 — interleaved byte offset of channel `c` at (5,20,33)

Tile extents T = (4,8,16). In-tile position uᵢ = xᵢ mod Tᵢ (§11.4
`[R-GEO-06]`): u = (5 mod 4, 20 mod 8, 33 mod 16) = (1, 4, 1).

In-tile sample ordinal = Σᵢ uᵢ · ∏_{j>i} Tⱼ
= 1·(8·16) + 4·16 + 1·1 = 128 + 64 + 1 = **193**.

Element sizes (§12.1): a uint8 → 1, b float32 → 4, c int16 → 2, d bool → 1
(interleaved bool is a single byte, §14.2). Sample stride Q = 1+4+2+1 = 8.
In-sample offset of channel index 2: F² = 1 + 4 = 5.

§14.2 `[R-SER-02]` table, interleaved: offset of value k = (k div C)·Q +
F_{k mod C}; §14.2's closing sentence gives the direct form: "channel c's
value at in-tile ordinal u sits at byte u · Q + Fᶜ".

193 · 8 + 5 = 1544 + 5 = **1549**. (Decoded size P·Q = 512·8 = 4096, so
1549 is in range.)

**Answer: `1549`**

---

## Q03 — planar bool tile, extents (2,2), tile extents (3,3), fill 0x01

Planar bool → packed plane (§14.3 `[R-SER-03]`). P = 3·3 = 9, decoded size
⌈9/8⌉ = 2 bytes. G = (1,1), N = 1, C = 1 → one addressed tile (§11.2).

In-tile ordinal k = u_y·3 + u_x. Real positions (inside extents (2,2)):
k ∈ {0,1,3,4}, all false → bit 0. Padding positions (y=2 or x=2):
k ∈ {2,5,6,7,8}. §14.5 `[R-SER-05]`: "at every padding position, a writer
MUST encode … the fill bit in a packed plane" → bit 1.

Pad bits: P mod 8 = 1 ≠ 0, so bit positions 1–7 of the final byte are pad
bits, and "Every pad bit MUST carry the plane's channel's fill bit" → 1.

- byte 0 = bits 0..7 = values 0..7 = 0,0,1,0,0,1,1,1 → 0b1110_0100 = **0xE4**
- byte 1 = bit 0 = value 8 = 1 (padding); bits 1–7 = pad bits = 1 → **0xFF**

Cross-check against §14.3's own example (P=10, fill true → `55 FD`, pad bits
2–7 set): same construction.

**Answer: `e4 ff`**

---

## Q04 — interleaved uint8+uint16, filter 2 byte-shuffle, codec 1

Q = 1 + 2 = 3; P = 4; decoded size = P·Q = 12 (§14.2). Value at ordinal u:
`a` at u·3, `b` little-endian at u·3+1..2.

Decoded tile image: `00 01 02 03 04 05 06 07 08 09 0a 0b`
(0x0201 → `01 02`; 0x0504 → `04 05`; 0x0807 → `07 08`; 0x0B0A → `0A 0B`).

No padding positions (extents = tile extents), so §14.5 imposes nothing.

Filter first, then codec (§17.1 `[R-COD-01]`: "the layer's **filter** …,
then its **codec** … — the filtered image is the codec's input").

Byte-shuffle (§17.3 `[R-COD-10]`): stride s = Q = 3 for an interleaved tile;
L = 12, n = L/s = 4; "the filtered image places byte i of group j at offset
i · n + j".

- i=0 → offsets 0..3 = 00, 03, 06, 09
- i=1 → offsets 4..7 = 01, 04, 07, 0A
- i=2 → offsets 8..11 = 02, 05, 08, 0B

Codec 1 (none): "The stored bytes are the filtered image verbatim"
(`[R-COD-04]`), and length 12 = decoded size ✓.

(My shuffle routine reproduces §17.3's float32 example exactly:
`00 00 80 3F 00 00 00 40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`.)

**Answer: `00 03 06 09 01 04 07 0a 02 05 08 0b`**

---

## Q05 — trailer CRC at [F−4, F), F = 192

§6.2 layout / §6.3 `[R-CNT-24]`: the u32 at trailer offset 60 is CRC-32C over
trailer bytes [0, 60), and F − 4 is that field.

Trailer bytes [0,60):
```
8a 4e 52 41 54 0d 0a 1a  01 00 00 00 00 00 00 00
02 00 00 00 00 00 00 00  10 00 00 00 00 00 00 00
64 00 00 00 00 00 00 00  c0 00 00 00 00 00 00 00
ef be ad de 00 00 00 00  00 00 00 00
```
(magic; version_major 1; version_minor 0; flags 0; generation 2;
dir_offset 16; dir_length 100; committed_file_length 192;
file_id 0x00000000DEADBEEF; reserved 0.)

CRC-32C = 0x98C09A8D, stored little-endian (§4.5 `[R-ENC-09]`).

Validation of the routine: it reproduces Appendix A's 0xE00938D2 for that
file's trailer, and §4.5's `"123456789"` check vector.

**Answer: `8d 9a c0 98`**

---

## Q06 — smallest F for a one-layer-record directory at dir_offset 16

Inline payload, packed in §7.4's table order with no padding
(`[R-CNT-18]`: "fields are packed in table order with no alignment or
padding between them"):

| field | bytes |
|---|---|
| name `a` (u8 len + 1) | 2 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| A u64 | 8 |
| S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| C u16 | 2 |
| dim `x`: name 2 + extent 8 + tile extent 8 | 18 |
| chan `c`: name 2 + type 2 + fill (1 len + 1) | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| **total** | **73** |

Cross-check with §7.4's worked example (name `sst`, float32 channel): there
the payload is 81 = 4 + 34 + 18 + 12 + 13. Here name is 2 not 4 and the
channel entry 6 not 12: 2 + 34 + 18 + 6 + 13 = 73 ✓. No sub-records, so the
payload ends exactly there ("no residue").

Geometry forces the trailing fields: G_x = ⌈0/1⌉ = 0 → N = 0 → addressed-tile
count 0 (§11.2), so entry_count = 0, crc_of_crc_array = 0 (`[R-CNT-23]`), and
the extent slot is (0,0) (§7.4: "a layer with zero addressed tiles has extent
(0,0)"; `[R-CNT-17]`'s formula gives extent_length 0).

Record = 24-byte header + 73 = 97 bytes. Directory region = record sequence +
terminal CRC-32C = 97 + 4 = **101** bytes (§7.1), at [16, 117).

Trailer constraints (§6.2 `[R-CNT-06]`, `[R-CNT-01]`): dir_offset +
dir_length ≤ F − 64, and F mod 64 = 0.
16 + 101 = 117 ≤ F − 64 → F ≥ 181 → smallest multiple of 64 is **192**.

At F = 192 the trailer sits at [128, 192) and the pre-trailer pad is
[117, 128) = 11 bytes — exactly `[R-LIF-02]` step 5's pad to the next 64-byte
boundary, so a conforming commit produces this file. F = 192 ≥ 128
(`[R-CNT-27]`) ✓.

**Answer: `192`**

---

## Q07 — slab run 1 with a half-sentinel entry

Geometry: G_x = ⌈32/4⌉ = 8 = N = entry_count. S = 4, interleaved → single
block [0,8); runs [0,4) and [4,8) (§16.2 `[R-SLB-02]`: "Run r of a block
starts at ordinal block_start + r·S"). Ordinals 4–7 are run 1.

(a) Ordinal 5: offset = S (all-ones), length = 32 ≠ S. §15.3 `[R-IDX-03]`
row: "offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile". The outcome-class vocabulary is §2.4's four names; the one here
is **reject-tile** (*structural* marks the row category, not the class).

(b) Run 1's entries: 4 stored (8192, 100); 5 structural reject-tile;
6 stored (8292, 50); 7 valid sentinel. §16.2 `[R-SLB-03]`: "Sentinel tiles
are transparent to run continuity … So are the entries §15.3 classifies
reject-tile on a *structural* ground: they address no usable extent, and the
run's stored tiles close over them."

So the packing relation reads only ordinals 4 and 6:
8192 + 100 = 8292 = ordinal 6's offset ✓. (First stored tile alignment,
L42's subject, also holds: 8192 mod 4096 = 0.) No L41 violation.

**Answer: `reject-tile; no`**

---

## Q08 — metadata encoding 0x40 vs 0x90

§10.2 / §18.2 `[R-MTA-03]` partition the metadata-encoding space:
0 invalid; 1, 2 assigned; **3–0x7F reserved**; **≥ 0x80 experimental**.

File A, encoding 0x40 = 64 → reserved range. §21.5 row **R1**: "A
user-metadata record declares a document encoding of 0, or a reserved-range
value (3-0x7F)" — outcome ignore-record, but §21.5's preamble is explicit:
"Every row here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming". `[R-EXT-03]`: "a value
from a reserved range MUST NOT be emitted at all before this specification
assigns it". So a violation is established → `[R-CNF-11]`: "a verifier that
has established any violation reports *nonconforming*".

File B, encoding 0x90 = 144 → experimental range. §21.6: "A user-metadata
record declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); **the file is conforming** … No document rule attaches under
an unassigned encoding, so a verifier certifies, reporting the record it
ignored". `[R-MTA-10]` confirms: "A verifier meeting such a record in an
otherwise conforming file has no requirement it is unable to check — the
record is not among `[R-CNF-11]`'s cannot-establish grounds, and
certification is unaffected". No violation, nothing unchecked → *conforming*.

**Answer: `nonconforming; conforming`**

Framing quibble (does not change the answers): the two files cannot literally
differ in exactly one byte, since the encoding byte lies inside the directory
record sequence and both files' directory CRCs must be correct.

---

## Q09 — verifier that cannot run zstd, plus a bool fill of 0x02

Layer B's fill: §13.2 `[R-TYP-07]` — "For bool, the fill field is one byte
and its value is constrained: `0x00` (false) or `0x01` (true). Writers MUST
NOT emit any other byte; a reader MUST treat any other byte as a validity
error at layer scope." Register row **L35**, detector reader, at layer
access, reject-layer. The verifier traverses the whole file, so it reaches
and establishes it.

Layer A gives a cannot-establish ground (`[R-COD-11]`: "A verifier that
cannot execute a layer's codec or filter cannot establish that layer's
conformance and MUST NOT certify the file"), but priority is fixed:
`[R-CNF-11]` — "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements
it was unable to check, and *cannot establish* is available only to a
traversal that established no violation."

**Answer: `nonconforming`**

(The verifier must still report the zstd inability per `[R-CNF-11]`'s
per-requirement reporting duty — but "that per-requirement report constrains
the report and not the verdict".)

---

## Q10 — ranges for entry 150,000 of a 200,000-entry index

§15.1 `[R-IDX-01]`: region = [entry array: entry_count × 20] [segment CRC
array: ⌈entry_count / 2¹⁶⌉ × 4], contiguous, no padding.
§15.4 `[R-IDX-04]`: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶,
entry_count))"; a reader must verify crc_of_crc_array over the CRC array and
the segment CRC over the segment containing k.

- Segment index = 150000 div 65536 = **2** (131072 ≤ 150000 < 196608).
- Segment 2 covers entries [131072, 196608) — a full segment.
- Byte range: 131072·20 = 2,621,440 to 196608·20 = 3,932,160.
- Entry array length = 200000·20 = 4,000,000.
- Segment count = ⌈200000/65536⌉ = 4 → CRC array = 16 bytes:
  [4,000,000, 4,000,016).

Cross-check with §15.4's worked example (entry_count 1,000,000 → 16 segments,
64-byte array, region 20,000,064 bytes): same construction.

**Answer: `2621440,3932160,4000000,4000016`**

---

## Q11 — a 40 MiB metadata document against a 16 MiB reader bound

(a) §18.2 `[R-MTA-09]`: "a reader instead decodes with a bound of its own
choosing, no smaller than §21.9's user-metadata guarantee". The Note adds:
"A file whose document decodes to more than the guarantee stays conforming".
§21.9 `[R-ERR-04]`: "A file exceeding any of these remains conforming".
Every stated structural rule holds. → **yes**.

(b) `[R-ERR-04]`: a reader "MAY decline it — at the whole file, or at the
narrowest scope whose declarations exceed what it can serve, a layer or a
tile." A user-metadata document has no declared size at all (`[R-MTA-09]`:
"a document has no declared size"), so no layer's or tile's declarations
measure it, and the whole file is the only available scope. §18.2's Note
states this outright: "a reader that instead declines on resource grounds
under `[R-ERR-04]` does so at the whole file, a document having no declared
size and so no narrower scope whose declarations that rule can measure."
→ **file**.

(c) `[R-MTA-09]`: "A **verifier** that declines to decode a document on the
bound above cannot establish that document's conformance and MUST NOT certify
the file … it fixes the file's verdict as *cannot establish* only where the
verifier established no violation elsewhere." None established here.
→ **cannot establish**.

**Answer: `yes; file; cannot establish`**

Note: (b)'s crispest statement lives in a *Note*, which §2.1 makes
non-normative; the normative pair `[R-ERR-04]` + `[R-MTA-09]` yields the same
answer, since neither "layer" nor "tile" has a declaration measuring a
document.

---

## Q12 — codec 4 (lz4) cap, interleaved vs planar

P = 25000 · 10000 = 250,000,000. G = (1,1), N = 1, so tiles are addressed in
both variants (interleaved 1; planar C·N = 2) — the §17.2 Note's
zero-addressed-tile escape does not apply.

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes … in a planar layer
each channel's plane carries its own decoded size (§14.2, §14.3), and the
largest governs — and a reader MUST treat such a declaration as a validity
error at layer scope."

Cap = 0x7E000000 = 2,113,929,216.

- **Interleaved**: Q = 8 (float64) + 1 (bool as a single byte, §14.2) = 9;
  decoded size = P·Q = 2,250,000,000 > 2,113,929,216 → **error**
  (reject-layer, register row L44).
- **Planar**: channel `w` plane = P·8 = 2,000,000,000; channel `f` packed
  bool plane = ⌈P/8⌉ = 31,250,000 (§14.3). Largest = 2,000,000,000 ≤ cap →
  **permitted**.

The bool channel is the whole story: as an interleaved byte it costs
250 MB per tile; as a packed plane it costs 31.25 MB and is not the
governing plane at all.

**Answer: `error; permitted`**

---

## Q13 — dropping an MU=0/PE=0 experimental top-level record

Type 0x9000 ≥ 0x8000 → experimental range (§10.2), unimplemented, MU = 0,
PE = 0. §20.4's table, MU = 0 / PE = 0 row:

> "An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: … for a top-level record, the file's layer set
> or another *non-layer* top-level record. Superseding a stored tile's bytes
> is not such a change for either kind … so a commit whose only change is a
> supersede MUST retain the record. Dropping the record, or dropping another
> record in the same commit, is not itself such a change either, so a commit
> whose only effect would be the drop MUST retain it."

- (a) supersede one tile's bytes → named explicitly as **not** such a change →
  must retain.
- (b) add a new layer M → changes **the file's layer set** → permits the drop.
- (c) only effect is the drop → named explicitly → must retain.

**Answer: `b`**

---

## Q14 — coverage walk slack total, F = 512

Claimants of the live committed state (§9.7 `[R-LIF-08]`, §5.2 `[R-CNT-02]`):
the front block, the trailer, the directory, each record's extent, and each
non-sentinel entry's stored extent. A record is not a claimant of its own —
its header and payload lie inside the directory region.

| claimant | range | bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile 1 | [16, 48) | 32 |
| layer record extent = tile-index region | [64, 148) | 84 |
| stored tile 2 | [148, 180) | 32 |
| user-metadata record extent | [180, 220) | 40 |
| directory region | [328, 448) | 120 |
| live trailer | [448, 512) | 64 |
| **total claimed** | | **388** |

(Index cross-check: entry_count 4 → 4×20 + ⌈4/2¹⁶⌉×4 = 84 = the slot's
length, `[R-CNT-17]` ✓. Both stored entries are well-formed and their crcs
match, so both keep their extents in the walk, §15.3.)

Slack = F − claimed = 512 − 388 = **124**, i.e. the gaps [48, 64) = 16 and
[220, 328) = 108. No pre-trailer pad (the directory ends exactly at 448).

(b) `[R-CNT-21]` requires a *partial* total only "Where the walk of §9.7 does
not enumerate every region's claimants — whether because a scope-level
rejection ends that scope's enumeration … or because the verifier elected
under `[R-CNF-11]` to stop at the first violation". Neither happened; the
walk completes, and the total "tighten[s] to the exact total when the walk
completes". → **no**.

**Answer: `124; no`**

---

## Q15 — reserved-range type 0x0005 with MU = 1

Type 0x0005 ∈ 0x0003–0x7FFF, the record-type reserved range (§10.2).
Flags 0x0003 → MU = 1, PE = 1 (so `[R-CNT-12]`'s MU=1/PE=0 row and the
reserved-flag-bit row do not apply); inline_length 0 and extent (0,0) are
unconstrained for an unknown type.

Two §21.2 rows describe the condition:

- **F35** — "A top-level record has a reserved-range type value
  (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1" |
  reader | **open** | `[R-CNT-15]`
- **F36** — "A top-level record carries a type value from the reserved range
  0x0003-0x7FFF … emitting one is a violation whatever its MU bit" |
  verifier | certification | `[R-CNT-15]`

§21.1 resolves the overlap by name: "Some rows are strict specializations of
others — F1 of F6 and of F8, **F35 of F36**, L24 of L25 — and a file
exhibiting a specialization is recorded against the narrower row, whose
detector and detection point are the ones that apply."

F35 is the narrower row; its Detected cell reads *open*.

**Answer: `F35; open`**

---

## Underdetermined count

Zero questions came out underdetermined. Two carry noted textual tension —
Q01(a) (the growth carve-out against the padding-position prohibition) and
Q11(b) (the crispest statement lives in a non-normative Note, though the
normative rules yield the same answer) — but in both cases the document
admits only one implementable reading.
