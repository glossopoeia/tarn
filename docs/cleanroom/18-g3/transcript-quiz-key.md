# Round 18 — quiz keyer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,339 lines, via the Read tool in six chunks). I ran `grep` against that
same file only (four patterns, to confirm exact wording of four sentences I was
about to quote). I wrote and ran three Python scripts under my own scratchpad
(`calc.py`, `calc2.py`, `calc3.py`) that read no files — they contain a CRC-32C
implementation and arithmetic only. I did not read `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the output
directory. I did not list any directory. I did not use web search or fetch.

Prior knowledge of other array/image formats was used only to generate
suspicions (e.g. "is the byte-shuffle direction the one I expect?"); every such
suspicion was settled against this document's own text and worked examples.

**CRC implementation validation.** Before answering any CRC question I checked
my CRC-32C against all four constants this document publishes:

| Source | Spec value | Mine |
|---|---|---|
| §4.5 check vector, `"123456789"` | `0xE3069283` | `0xE3069283` |
| §4.5, zero bytes | `0x00000000` | `0x00000000` |
| §7.4 example, 4 sentinel entries (80 bytes) | `0x80A34955` | `0x80A34955` |
| §7.4 example, crc_of_crc_array | `0xC4EE982E` | `0xC4EE982E` |
| §15.4 / App. B, 2^16 sentinel entries | `0xEECB3BB2` | `0xEECB3BB2` |
| App. A, trailer CRC of the 128-byte minimal file | `0xE00938D2` | `0xE00938D2` |

All six reproduce. Likewise I validated my byte-shuffle direction against
§17.3's own example (three float32 → `00 00 00 00 00 00 80 00 40 3F 40 40`)
before using it in Q04.

---

## Q01 — the 64-byte trailer

Layout from §6.2's table. Field by field:

| Off | Bytes | Field |
|---|---|---|
| 0 | `8a4e5241540d0a1a` | trailer magic (§6.2, App. B) |
| 8 | `0100` | version_major = 1 |
| 10 | `0000` | version_minor = 0 |
| 12 | `00000400` | flags = 2^18 = 0x00040000, little-endian |
| 16 | `0200000000000000` | generation = 2 |
| 24 | `1000000000000000` | dir_offset = 16 |
| 32 | `0400000000000000` | dir_length = 4 |
| 40 | `c000000000000000` | committed_file_length = 192 |
| 48 | `efcdab8967452301` | file_id = 0x0123456789ABCDEF |
| 56 | `00000000` | reserved — §6.2's table gives valid values as "zero", the only permitted value |
| 60 | `275094a8` | CRC-32C over [0,60) = 0xA8945027 |

Decisive: §6.2's table row `| 56 | 4 | bytes | reserved | structural | zero |`
and `| 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |`.

Bit numbering: §4.4 `[R-ENC-08]` — bit 0 is the LSB — so "exactly bit 18 set"
is the value 0x00040000. Bit 18 lies in the ignore lane (bits 16–31, §6.3), so
this is a conforming file even though a writer under this text would emit
flags = 0; §2.3 `[R-CNF-02]` names exactly this as a conduct rule that binds
the actor and not the bytes. Byte order little-endian throughout (`[R-ENC-01]`).

Computed trailer CRC = **0xA8945027**, stored `27 50 94 a8`.

**Answer (128 hex chars):**
`8a4e5241540d0a1a0100000000000400020000000000000010000000000000000400000000000000c000000000000000efcdab896745230100000000275094a8`

Confidence: high.

---

## Q02 — three-entry all-sentinel index region

entry_count = 3, index_encoding 1, no tile stored → all three entries are the
sentinel (§15.2 `[R-IDX-02]`: "offset and length both `0xFFFF_FFFF_FFFF_FFFF`
and crc 0 — the 20 bytes `FF ×16 00 ×4`").

(a) §15.1: region = `[entry array: entry_count × 20][segment CRC array:
⌈entry_count / 2¹⁶⌉ × 4]`, "with no padding anywhere inside the region".
3 × 20 = 60; ⌈3/65536⌉ = 1, ×4 = 4. **64 bytes.** This agrees with
`[R-CNT-17]`'s extent_length formula: 3 × 20 + 1 × 4 = 64.

(b) §15.4 `[R-IDX-04]`: segment 0 covers entries [0, min(65536, 3)) = [0,3),
and "the s-th u32 of the segment CRC array is the CRC-32C over exactly those
entries' bytes as stored — the final partial segment's CRC covers only its
actual bytes." So the CRC is over 60 bytes, not 65536 entries' worth.

**Trap checked and rejected:** `[R-IDX-05]`'s constant 0xEECB3BB2 is for a
**full** segment only — "one covering exactly 2¹⁶ entries, final or not — whose
entries are all sentinels… a partial segment's CRC MUST be computed." Three
entries is partial, so the constant does not apply.

CRC-32C of `(FF×16 00×4) × 3` = **0xD171D122**, stored `22 D1 71 D1`.

(c) §7.4 / §8.1: crc_of_crc_array is "CRC-32C over the index's segment-CRC
array". That array is the 4 bytes `22 D1 71 D1`. CRC-32C of those =
**0x34C74AFB**.

**Answer: 64; d171d122; 34c74afb.** Confidence: high.

---

## Q03 — planar bool edge tile

Geometry (§11.2 `[R-GEO-03]`): E = (5,5), T = (4,4) → G = (⌈5/4⌉, ⌈5/4⌉) =
(2,2), N = 4. Planar, C = 1 → addressed tiles = C·N = 4. P = ∏Tᵢ = 16.

Tile coordinates (1,1) covers coordinates 4–7 on both axes. Only (4,4) lies
inside the extents — this is precisely §14.5's worked example geometry ("the
edge tile at tile coordinates (1, 1) covers coordinates 4–7 along both axes —
one real position, (4, 4), and 15 padding positions"). In-tile position (0,0),
in-tile ordinal 0 (§11.4 `[R-GEO-06]`).

Planar + bool → §14.3 `[R-SER-03]`: "the decoded tile image is the tile's P
values bit-packed LSB-first: value k occupies bit k mod 8 of byte k div 8…
and the decoded size is ⌈P/8⌉ bytes" = ⌈16/8⌉ = 2 bytes.

- Ordinal 0 = false → bit 0 of byte 0 = 0.
- Ordinals 1–15 are padding positions. §14.5 `[R-SER-05]`: "at every padding
  position, a writer MUST encode, for each channel the position carries, that
  channel's fill value — … the fill bit in a packed plane." Fill byte is 0x01 =
  true (§13.2 `[R-TYP-07]`), so the fill bit is 1.
- P mod 8 = 0, so there are **no pad bits** (§14.3: pad bits arise only "when
  P mod 8 ≠ 0").

byte 0 = bits (0,1,1,1,1,1,1,1) = 0xFE; byte 1 = bits all 1 = 0xFF.

Filter 1 = none and codec 1 = none, so the stored bytes are the decoded image
verbatim (§17.3 `[R-COD-09]`, §17.2 `[R-COD-04]`). Length 2 = decoded size,
consistent with `[R-COD-04]`.

**Answer: `FE FF`.** Confidence: high.

---

## Q04 — interleaved tile under byte-shuffle

C = 2 (a: uint8, B=1; b: uint16, B=2). Q = ΣBᵢ = 3 (§14.2 `[R-SER-02]`).
P = ∏Tᵢ = 2·3 = 6. Decoded size = P·Q = 18. (This is §14.2's own worked
example: "tile extents (2, 3), P = 6, channels `a` (uint8) and `b` (uint16):
Q = 3, decoded size 18.")

Offsets: §14.2 gives offset of value k = (k div C)·Q + F_{k mod C}, with
F_a = 0, F_b = 1; equivalently "channel c's value at in-tile ordinal u sits at
byte u · Q + Fᶜ". So sample u occupies [3u, 3u+3): a at 3u, b (little-endian)
at 3u+1..3u+2.

Decoded image (18 bytes):
`01 22 11 | 02 44 33 | 03 66 55 | 04 88 77 | 05 AA 99 | 06 CC BB`

Filter 2 = byte-shuffle. §17.3 `[R-COD-10]`: "The shuffle stride s is … the
sample stride Q for an interleaved tile"; s = 3, L = 18, n = L/s = 6. "the
filtered image places byte i of group j at offset i · n + j". Direction
validated against §17.3's float32 example.

- i=0 (offsets 0–5): `01 02 03 04 05 06`
- i=1 (offsets 6–11): `22 44 66 88 AA CC`
- i=2 (offsets 12–17): `11 33 55 77 99 BB`

Codec 1 (none) → stored bytes are the filtered image verbatim (§17.1
`[R-COD-01]`: filter then codec).

**Answer: `01 02 03 04 05 06 22 44 66 88 AA CC 11 33 55 77 99 BB`.**
Confidence: high.

---

## Q05 — a 65,537-entry index

(a) `[R-CNT-17]`: "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4". 65537 × 20 = 1,310,740. ⌈65537/65536⌉ = 2, ×4 = 8.
**1,310,748.**

(b) §15.1's region layout puts the entry array first, then the segment CRC
array. The array begins at region byte 65537 × 20 = 1,310,740. §15.4: "the
s-th u32 of the segment CRC array" — segment 1 is the second u32, at
1,310,740 + 4 = **1,310,744.**

(c) §15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))".
s = 1 → [65536, min(131072, 65537)) = [65536, 65537) → **1 entry.**

**Answer: 1310748; 1310744; 1.** Confidence: high.

---

## Q06 — a one-layer file, generation 1

The layer record's inline payload is §7.4's 81-byte example: entry_count = 4,
extent slot length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 ("`[R-CNT-17]`'s arithmetic — an
extent slot of length 4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84").

- Tile-index region: [16, 100) — 84 bytes beginning at 16, as stipulated.
- Directory region begins immediately after → dir_offset = **100**.
- Directory contents (§7.1, §7.2): record sequence + terminal 4-byte CRC.
  The sequence is one record: 24-byte header + inline_length 81 = 105 bytes.
  dir_length = 105 + 4 = **109**. Directory occupies [100, 209).
- `[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary … and the
  new trailer". 209 → next 64-boundary is 256 (pad 47 bytes). Trailer occupies
  [256, 320). committed_file_length = **320**.

Cross-checks against `[R-CNT-06]`: F mod 64 = 0 ✓; dir_offset ≥ 16 ✓;
dir_length ≥ 4 ✓; dir_offset + dir_length = 209 ≤ F − 64 = 256 ✓; and no
structure sits between the directory's end and the trailer (`[R-CNT-05]`) ✓.
The creation path of `[R-LIF-02]` writes the front block then begins at 16,
which the stipulated index placement satisfies exactly.

**Answer: 100; 109; 320.** Confidence: high.

---

## Q07 — Appendix G emission order

Appendix G item 3 fixes a total order: "For each layer in ascending layer-name
byte order: its stored tiles in disk-ordinal order, then its tile-index region;
then any remaining record extents in ascending record order — all of them after
every layer's tiles and index region, not interleaved with them; then the
directory." And: "The first structure begins at 16 … each later structure
begins where the previous one ended, save where alignment forces a gap".

No declared alignment or slab (item 5's first branch), so no gaps until the
pre-trailer pad.

Layer order: `alpha` < `beta` by raw bytes (0x61 < 0x62).

**alpha.** rank 1, E₀ = 4, T₀ = 4 → G₀ = 1, N = 1; interleaved → entry_count =
1. P = 4, Q = 1 (one uint8 channel), decoded size = P·Q = 4; codec 1 forces
stored length = decoded size = 4 (`[R-COD-04]`). Tile values 01 02 03 04 ≠ fill
0x00, so item 6's all-fill-sentinel rule does not apply — it is stored, as
stipulated.
- stored tile: [16, 20)
- tile-index region: 1 × 20 + ⌈1/2¹⁶⌉ × 4 = 24 bytes → [20, 44)

**beta.** E₀ = 0 → G₀ = ⌈0/4⌉ = 0, N = 0, entry_count = 0 (`[R-GEO-02]`: "its
grid count is 0, the layer has zero addressed tiles, its tile index has zero
entries"). §7.4: "a layer with zero addressed tiles has extent (0, 0)", and
§15.4's example: "At entry_count = 0 there is no region at all". So beta
contributes **zero bytes** — no stored tiles, no index region.

**Remaining record extents.** The one top-level user-metadata record's extent,
40 bytes → begins at **44**, occupying [44, 84).

**Directory** begins at **84**.

**Answer: 44; 84.** Confidence: high.

---

## Q08 — slab run continuity

Interleaved → §16.2 `[R-SLB-02]` gives the single block [0, N) = [0, 8);
runs start at block_start + r·S, so run 0 = ordinals [0, 4). That is the run
in question.

`[R-SLB-03]`: "the run's stored tiles are contiguous and packed in ordinal
order — each stored tile's offset equals the previous stored tile's offset plus
its length — and the first stored tile's offset satisfies offset mod
A_slab = 0." Entry 0 at 4096: 4096 mod 1024 = 0 ✓ in both cases.

Ordinal 1 is the sentinel: "Sentinel tiles are transparent to run continuity:
they occupy no bytes and do not break packing."

**Case (a).** Entry 2 is a well-formed stored entry whose *stored bytes* fail
its crc. `[R-SLB-03]` is explicit: "An entry whose only defect is that its
stored bytes fail its crc is not transparent — its offset and length stand, and
the packing relation reads them as it does any other stored tile's." §15.3
agrees: such an entry "is well-formed: the defect lies in the bytes it
addresses, not in the entry, so its extent stands and it keeps its place in the
*verifier* rows, in run continuity, and in the coverage walk."
So the previous stored tile for ordinal 3 is ordinal 2: 4296 + 300 = **4596**.
(Consistency check on entry 2 itself: 4096 + 200 = 4296 ✓.)

**Case (b).** Entry 2 has offset 0, length 50 — non-sentinel with offset < 16,
which §15.3's table classifies "*structural*: reject-tile — the front block is
never payload". `[R-SLB-03]`: "So are the entries §15.3 classifies reject-tile
on a *structural* ground: they address no usable extent, and the run's stored
tiles close over them." Entry 2 is therefore transparent, and the previous
stored tile for ordinal 3 is ordinal 0: 4096 + 200 = **4296**.

**Answer: 4596; 4296.** Confidence: high.

---

## Q09 — trailer CRC fails on a foreign-major file

§6.2 `[R-CNT-06]` fixes the order: "A reader MUST validate, in order: the
trailer magic; the trailer CRC; the version gate (§6.3)". The magic passes; the
CRC fails; the reader never reaches the version gate.

§21.2's preamble confirms this is one of the four rows that reach a
foreign-major file: "Four rows are outside that reasoning and do reach it,
because their subject is a field fixed across every major (`[R-CNT-24]`): F8
and F1's trailer-magic instance, F14's trailer CRC — the two checks §6.2 places
before the gate — and F6 with F1's front-block instance".

The front block matches (F6/F1 clean); the magic matches (F8/F1 clean). The
declared major 5 is *not* a register row — §21.6: "version_major naming a major
this reader does not implement… Neither is a register row: the register
enumerates file-conformance violations (§21.1), and a file this document
declines to judge is not one." So the single row is **F14**.

§21.2's heading: "Outcome: reject-file." Outcome class = **reject-file**.

**Answer: F14; reject-file.** Confidence: high.

---

## Q10 — reserved vs experimental metadata encoding

**File A, encoding 0x03 = 3.** §18.2 `[R-MTA-03]`: "3 through 0x7F are
reserved". §21.5 row R1: "A user-metadata record declares a document encoding
of 0, or a reserved-range value (3-0x7F)" — a registered violation. §21.5's
preamble: "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming (`[R-CNF-12]`)."
Also `[R-MTA-10]`: "encoding 0 and the reserved range stay violations (R1)";
"what `[R-MTA-10]` withdraws is the document's content rules, never the encoding
byte's own value set". A verifier that establishes a violation reports
**nonconforming** (§2.3 `[R-CNF-11]`).

**File B, encoding 0x85 = 133 ≥ 0x80.** Experimental range. §21.6: "A
user-metadata record declares an experimental-range (≥ 0x80) document encoding
| Ignored (ignore-record); the file is conforming — §10.3's prohibition binds a
writer's conduct, not the bytes. No document rule attaches at such an encoding,
so a verifier certifies, reporting the record it ignored". `[R-MTA-10]`
enumerates exactly the checks that decide conformance here — framing and extent
slot, the encoding byte's value set, and the terminal CRC — and all pass
(inline_length 1, extent 40 ≥ 5, CRC correct). Verdict **conforming**.

Note the ignore-record outcome is identical for both files; the *verdicts*
differ. That asymmetry is the point of the question.

**Answer: nonconforming; conforming.** Confidence: high.

---

## Q11 — an established violation outranks a decline

The type-0x0005 top-level record: 0x0005 lies in §10.2's reserved range
0x0003–0x7FFF. MU = 0, so F35 (which requires MU = 1) does not fire, but F36
does: "A top-level record carries a type value from the reserved range
0x0003-0x7FFF, which this specification has not assigned; emitting one is a
violation whatever its MU bit" — detector *verifier*, detected at
certification. A conforming verifier checks every file-level requirement
(§2.3), so it establishes this.

The 40 MiB document is a separate matter and is *not* a violation: §18.2's note
— "A file whose document decodes to more than the guarantee stays conforming" —
and `[R-MTA-09]`: "the bound is that verifier's capability and not a limit on
validity (`[R-CNF-10]`), so the decline is not a finding that the file is
nonconforming and a verifier MUST NOT report it as one." It would fix the
verdict at *cannot establish* "only where the verifier established no violation
elsewhere".

§2.3 resolves the collision: "An established violation takes priority: a
verifier that has established any violation reports *nonconforming*, however
many requirements it was unable to check, and *cannot establish* is available
only to a traversal that established no violation."

**Answer: nonconforming.** Confidence: high.

---

## Q12 — what the appender may omit

All three records are governed by §20.4's table.

**(iii) type 0x0002, user metadata.** Registered by §7.3 with PE = 1. §20.4:
"For a type §7.3 registers, the registry's fixed flags govern rather than the
stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so neither can
be dropped", and "No commit therefore removes a layer record, or a
user-metadata record at either scope." **Must retain.**

**(i) top-level 0x9001, MU = 0 / PE = 0, unimplemented.** The MU = 0, PE = 0
row permits a drop only "in a commit that *independently* changes the scope the
record attaches to: … for a top-level record, the file's layer set, any layer
record's content, or another *non-layer* top-level record." The same row then
states this exact case: "Superseding a stored tile's bytes re-places that
layer's index region (§20.3, `[R-WRT-04]`), moving its extent slot (§7.4) and
so modifying that layer's record, which is such a change: an appender
superseding a tile MAY drop a top-level such record". **May omit.**

**(ii) sub-record 0x9002 of layer B, MU = 0 / PE = 0, unimplemented.** For a
layer sub-record the qualifying change is "that layer's record, the entry set
of its index, or which of its tiles are stored" — all of layer **B**, which
this commit leaves untouched. The table's own gloss names the permitted case as
"such a sub-record of the layer whose tile it superseded" — layer A, not B.
**Must retain.**

**Answer: (i).** Confidence: high.

---

## Q13 — compactor meeting a structurally malformed entry

The entry has offset = S (2⁶⁴ − 1) and length = 0x64 ≠ S. §15.3's table:
"offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile" (register row T7).

The compactor relocates the region, so it regenerates it. §20.5:

> "Regenerating a region means classifying every entry in it: a sentinel is
> re-emitted unchanged, and every other entry is re-pointed to where its stored
> extent now lies. An entry §15.3 classifies reject-tile on a structural ground
> is neither — `[R-IDX-03]` gives it no stored extent for a re-pointing to
> target — so regenerating the region cannot proceed without meeting it, and
> the violation is thereafter one the compactor has detected. `[R-WRT-06]` then
> obliges refusal: the compactor can neither reproduce the entry nor invent a
> replacement, and no drop is available, a tile-index entry being no record
> §20.4's table licenses dropping."

That sentence eliminates (a) ("neither reproduce the entry"), (b) ("nor invent
a replacement" — and §20.5's regeneration list says only sentinels are
re-emitted unchanged), and (c) ("no drop is available"; §20.4 also bars
removing a layer record, and §20.5 says compaction "carries every layer of its
input forward").

**Answer: d.** Confidence: high.

---

## Q14 — the compacted trailer

(a) Bits 18 and 20 both lie in the ignore lane (bits 16–31, §6.3). The
compactor implements no flag bits, so both are unknown ignore-lane bits.
§6.3 `[R-CNT-08]`: "A compactor, though its output is a new file, carries the
input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0". §20.5 `[R-WRT-06]`: "The output trailer copies the input's unknown
ignore-lane flag bits forward (`[R-CNT-08]`)". Value = 2¹⁸ + 2²⁰ = 262,144 +
1,048,576 = 1,310,720 = **0x00140000**.

(b) `[R-WRT-06]`: "It MUST mint a fresh file_id for the output … and generation
1". **1.**

(c) `[R-WRT-06]`: the output trailer "carries the greater of `[R-CNT-26]`'s
floor and the input's version_minor — a compactor cannot know which minor
version defined an ignore-lane bit it does not implement, so it does not lower
the floor beneath one." The input's minor is 7; `[R-CNT-26]`'s floor for
content expressible under this text is 0. max(0, 7) = **7.**

**Answer: 00140000; 1; 7.** Confidence: high.

---

## Q15 — a filter change with no witness

Geometry: E = (16,16), T = (8,8) → G = (2,2), N = 4; planar with C = 1 →
addressed tiles = 4. P = 64. Decoded size (planar numeric, §14.2) = P·Bᶜ =
64 × 4 = 256 bytes.

**Is the commit legal?** No. §20.3 step 4: "A commit MUST NOT change a layer's
declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes for its stored bytes or how
they decode — … the byte offset of any sample within the decoded tile image, or
the codec and filter that produced the stored bytes." The exemption ("a filter
whose mandated stride makes it the identity") does not apply: for a planar
float32 plane `[R-COD-10]` mandates s = element size = 4, n = 256/4 = 64, which
is not the identity. So generation 10 is nonconforming.

**But does the file exhibit a register row?** Walking §21.2–§21.5:

- F rows: trailer, directory, records all unchanged and valid.
- L rows: every declaration is in its value set (filter 1 valid, L45 clean);
  entry_count = C·N = 4 (L21 clean); extent_length = 4 × 20 + 4 = 84 (L22
  clean); no alignment or slab (L20, L28, L29, L39–L42 clean).
- T14 (codec 1, entry length ≠ decoded size): byte-shuffle preserves length, so
  each stored length is still 256 = decoded size. Clean.
- T3 (decoded payload length ≠ decoded size): codec 1, so decoded length =
  stored length = 256. Clean.
- T1: bytes and crcs carried forward unchanged. Clean.
- T4 / T5 (padding content, pad bits): G·T = 2 × 8 = 16 = E on both axes, so
  the layer has **no padding positions**; float32, so no pad bits. Clean.
- T2 (interleaved bool byte): not applicable — planar, float32.
- T26: predicated on filter 2 being applied at a wrong stride *and* the result
  breaking padding content or bool bytes; neither holds.

§21.7 `[R-ERR-01]` states this outcome directly: "§20.3 step 4's bar on a
declaration change is witnessed only where the affected tiles remain stored
*and* the change reaches a byte §14 structurally constrains — a padding
position, a pad bit, or a boolean byte — where §21.4's content rows fire; a
change that reaches the decoded size instead is witnessed by T3 or T14 …; a
change that reaches the codec is witnessed by the rows for the codec now
declared … or by T14 where the new declaration is codec 1". Here the change
reaches the *filter* only; it touches no structurally constrained byte, no
length, and no codec. There is no witness.

So the file is nonconforming and yet exhibits no register row — the register's
completeness clause (§21.1) runs to *detectable* violations only. Every sample
the file now returns is wrong (the stored bytes are shuffled but decoded as
unshuffled), and §21.7's opening sentence is exactly this case: "this format
detects *corruption of structure*, not *incorrectness of content*."

**Answer: none.** Confidence: high. The oddity is worth stating rather than
softening: the honest answer is "none", not "no violation".
