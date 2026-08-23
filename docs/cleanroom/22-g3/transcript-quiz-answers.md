# Cleanroom round 22 — quiz answerer transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4394 lines, in five sequential `Read` calls, plus targeted `grep`/`sed`
re-reads of §18.2, §21.5, §21.9 against that same file).

Ran two local Python scripts I wrote myself
(`scratchpad/calc.py`, `scratchpad/calc2.py`) that read no files: a CRC-32C
implementation and the geometry/coverage arithmetic. The CRC implementation
was validated twice against the document's own published values — the
`"123456789"` check vector of §4.5 (`0xE3069283`) and Appendix A's trailer
CRC (`0xE00938D2`) — before being used for Q02.

No ADRs, no `docs/`, no `conformance/`, no `registry.json`, no git history,
no web access, no directory listings.

**Unsolicited context.** Material appeared in my context before the task
began: a project instruction file pointing at another document, and an index
of the maintainer's memory notes with several titled entries (one of whose
titles referenced a spec-section-to-corpus relationship). I did not open any
of it and did not use any of it. Nothing in it is cited below; every answer
derives from `spec/tarn.md` alone. Reporting its appearance as the brief
requires.

---

## Q01 — layer record inline payload

Field order from §7.4's table. Sizes cross-checked against §7.4's own worked
example, which itemizes "Name and the nine scalars from layout through
channel count occupy 4 + 34 bytes, the dimension entry 18, the channel entry
12, and the trailing fixed fields 13 — 81 exactly".

**(a) The two channel entries.** §7.4: "C channel entries | name (u8 len +
bytes) · type u16 (0 invalid) · fill (u8 len + bytes)", with "fill length
equals the type's element size (`[R-CNT-23]`)".

- `a`, bool. §12.1 gives bool ID 1, element size 1. §13.2: bool fill is one
  byte, `0x01` (true). → `01 61 01 00 01 01`
  (len 1, `a`=0x61, type u16 LE `01 00`, fill len `01`, fill byte `01`)
- `b`, uint16. §12.1 gives uint16 ID 7, element size 2. Fill 0x1234 LE.
  → `01 62 07 00 02 34 12`

Concatenated: `01 61 01 00 01 01 01 62 07 00 02 34 12` (13 bytes).

**(b) inline_length.**

Geometry (§11.2): G_y = ⌈4/2⌉ = 2, G_x = ⌈6/3⌉ = 2, N = 4. Planar, so the
addressed-tile count is C·N = 2·4 = 8 → entry_count = 8 (`[R-CNT-17]`).

| Region | Bytes |
|---|---|
| name (`01 6d`) | 2 |
| nine scalars: layout 1, linearization 2, codec 2, filter 2, A 8, S 8, A_slab 8, rank 1, C 2 | 34 |
| 2 dimension entries @ (2 + 8 + 8) | 36 |
| 2 channel entries (6 + 7) | 13 |
| index_encoding 1 + entry_count 8 + crc_of_crc_array 4 | 13 |
| sub-records | 0 |

Total = 2 + 34 + 36 + 13 + 13 = **98**.

---

## Q02 — last four bytes of a single-commit file

Record size: a user-metadata record's inline payload is "exactly one byte"
(§18.2, `[R-MTA-03]`), so the record is 24 + 1 = 25 bytes. The directory
region is "exactly that one record followed by the region's terminal
checksum" → dir_length = 25 + 4 = 29, dir_offset = 64, directory ends at 93.

`[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary … and the
new trailer". 93 → 128; trailer [128, 192); F = 192, a multiple of 64
(`[R-CNT-01]`). Creation path: "writing beginning at offset 16, with
generation 1".

Trailer bytes [0, 60) per §6.2's layout:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                      version_major = 1
00 00                      version_minor = 0
00 00 00 00                flags = 0
01 00 00 00 00 00 00 00    generation = 1
40 00 00 00 00 00 00 00    dir_offset = 64
1d 00 00 00 00 00 00 00    dir_length = 29
c0 00 00 00 00 00 00 00    committed_file_length = 192
18 07 f6 e5 d4 c3 b2 a1    file_id = 0xA1B2C3D4E5F60718 LE
00 00 00 00                reserved
```

CRC-32C over those 60 bytes = 0xB17DAE50, "stored as a little-endian `u32`"
(§4.5). The last four byte positions of the file are trailer bytes [60, 64),
which §6.2 assigns to the trailer CRC.

**Answer: `50 ae 7d b1`**

---

## Q03 — zstd metadata frame with a wrong Frame_Content_Size

Everything structural passes: extent slot valid, extent CRC verifies,
inline_length 1, encoding 2 assigned, one frame, no dictionary ID, no
content-checksum flag, no trailing bytes, document content clean and sorted.
The single defect is FCS = 4,096 against a 4,000-byte decoded document.

§18.2 `[R-MTA-09]` is decisive: "The frame's content-size field, unlike the
decoded size and the window, is *not* left to the reader: it MAY be present,
and when present it MUST equal the byte length of the decoded document. **A
mismatch is a failure to decode within the meaning of R3**".

So this is R3, not R4 — R4's instance list covers the frame constraints
(magic, skippable/second frame, dictionary ID, checksum flag, trailing
bytes) and does not include the content-size field, and §18.2 routes the
mismatch to R3 by name.

R3's row (§21.5): Detector **reader**, Detected **extent use**. §21.5's
heading fixes the outcome: "Outcome: ignore-record".

(a) **R3** · (b) **ignore-record** · (c) **reader** · (d) **extent use**

---

## Q04 — 16 MiB window against an 8 MiB verifier bound

§21.9's table gives "zstd frame `Window_Size` | 8 MiB" as a minimum
guarantee. The verifier's bound is exactly that, so 16 MiB exceeds it.

§18.2 `[R-MTA-09]`: "The frame's declared `Window_Size` is unconstrained here
… a frame declaring more than the reader admits is ignore-record on that
ground — the reader's capability, not a failure to decode within the meaning
of R3, and **no violation: the file exceeds a §21.9 guarantee and so remains
conforming** while the reader MAY decline it".

(a) **conforming**. `[R-ERR-04]`: "A file exceeding any of these remains
conforming, and a reader MAY decline it".

(b) The verifier declined and established nothing. §18.2: "A **verifier**
that declines to decode a document on the bound above cannot establish that
document's conformance and MUST NOT certify the file … it fixes the file's
verdict as *cannot establish* only where the verifier established no
violation elsewhere". Whether "the bound above" reaches the *window* bound as
well as the size bound is settled by §21.5's preamble, which names both:
"except where a reader or verifier declines the decode on the size bound **or
on the frame's declared window**, which `[R-MTA-09]` makes that actor's
capability and not a fact about the file." §2.3 likewise lists "when it
declines to decode a user-metadata document (`[R-MTA-09]`)" as a
cannot-establish ground. → **cannot establish**.

(c) **ignore-record**, per the `[R-MTA-09]` sentence quoted above.

---

## Q05 — rank 40, one empty dimension, 512 MiB declared tile

**(a) Conforming.** Every declaration is in range:

- rank 40 ≤ 255, the `u8` field's hard cap (`[R-ERR-05]`, §7.4).
- Extent 0 is explicitly valid: `[R-GEO-02]` "A dimension with extent 0 is
  valid: its grid count is 0, the layer has zero addressed tiles, its tile
  index has zero entries". `[R-GEO-01]` adds "at Eᵢ = 0 the grid count is 0
  and the layer addresses no tile".
- G_0 = ⌈0 / 67,108,864⌉ = 0, so N = 0, entry_count = 0, extent slot (0,0),
  crc_of_crc_array = 0 — all consistent with `[R-CNT-17]`/`[R-CNT-23]`.
- Derived products stay far under 2⁶³ − 1 (`[R-ENC-04]`): P = 2²⁶,
  Q = 8, P·Q = 536,870,912.
- Codec 1, so `[R-COD-07]`'s lz4 cap (L44) never engages.

**(b) Only "rank d of a layer".** 40 > 32.

The trap is the 512 MiB derived tile size against the 256 MiB row. §21.9
forecloses it: "The last three rows are **per-instance**: they range over the
tiles, user-metadata documents and compressed frames a file actually
contains, and a file containing none of a kind does not exceed that row,
**whatever its declarations would derive** — a layer addressing no tile
(§11.2) has no tile whose decoded size the table can bound". This layer
addresses no tile, so it contains none. C = 1, entry_count = 0, one layer, a
tiny directory, no metadata document, no zstd frame — no other row is
reached.

---

## Q06 — planar geometry arithmetic

§11.2: G_i = ⌈E_i / T_i⌉ → G = (⌈100/10⌉, ⌈200/64⌉, ⌈300/64⌉) = (10, 4, 5).
N = ∏G_i = 200. Planar: "its **addressed-tile count** … is N for an
interleaved layer and C · N for a planar layer".

**(a)** entry_count = 3 · 200 = **600**.

**(b)** `[R-CNT-17]`: "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4" = 600·20 + 1·4 = **12,004**.

**(c)** §11.4: t_i = x_i div T_i → (55 div 10, 130 div 64, 200 div 64) =
(5, 2, 3). "the **spatial tile ordinal** … is s = Σᵢ tᵢ · ∏_{j>i} Gⱼ" =
5·(4·5) + 2·5 + 3 = 100 + 10 + 3 = 113. "The **disk tile ordinal** … is
**c · N + s** for a planar layer" = 2·200 + 113 = **513**.

**(d)** u_i = x_i mod T_i = (5, 2, 8). "The **in-tile sample ordinal** of
(u₀, …, u_{d−1}) is Σᵢ uᵢ · ∏_{j>i} Tⱼ" = 5·(64·64) + 2·64 + 8 =
20,480 + 128 + 8 = **20,616**.

---

## Q07 — packed planar bool tile with padding

G = (⌈3/3⌉, ⌈2/3⌉) = (1, 1), N = 1; planar with C = 1 → one addressed tile.
P = ∏T_i = 9. §14.3: packed plane, decoded size ⌈P/8⌉ = 2 bytes.

The tile spans x0 ∈ [0,3), x1 ∈ [0,3), but E_1 = 2, so every position with
x1 = 2 is a padding position (§11.3). `[R-SER-05]`: "at every padding
position, a writer MUST encode … the fill bit in a packed plane", and fill is
true → bit 1.

In-tile ordinal k = u₀·T₁ + u₁ = 3·x0 + x1:

| k | (x0,x1) | value |
|---|---|---|
| 0 | (0,0) | 0 |
| 1 | (0,1) | 1 |
| 2 | (0,2) pad | 1 |
| 3 | (1,0) | 1 |
| 4 | (1,1) | 0 |
| 5 | (1,2) pad | 1 |
| 6 | (2,0) | 0 |
| 7 | (2,1) | 1 |
| 8 | (2,2) pad | 1 |

§14.3: "value k occupies bit k mod 8 of byte k div 8 … LSB-first".
Byte 0 = bits set at 1,2,3,5,7 = 2+4+8+32+128 = 174 = `0xAE`.
Byte 1 = bit 0 (value 8 = true) plus pad bits: P mod 8 = 1, so bit positions
1 through 7 are pad bits, each carrying the fill bit (true) → `0xFF`.

**(a) `ae ff`**

**(b)** Codec 1, filter 1. `[R-COD-04]`: "The stored bytes are the filtered
image verbatim. The index entry's length therefore MUST equal the tile's
decoded size". → **2**

---

## Q08 — interleaved sample offset

§14.2: Q = ΣB_i = 1 + 4 + 2 = **7**; P = 2·4 = 8; decoded size 56.
Tile extents equal the extents, so the coordinate (1, 2) is also the in-tile
position. In-tile ordinal u = u₀·T₁ + u₁ = 1·4 + 2 = 6.

§14.2's closing example: "channel c's value at in-tile ordinal u sits at byte
u · Q + Fᶜ". The sample begins at channel `a`'s byte, F_a = 0.

**(a)** 6 · 7 + 0 = **42**

**(b)** In declared channel order, "each sample's channel values are adjacent,
in declared channel order" (`[R-SER-01]`), each little-endian (`[R-ENC-01]`):
- a = 0x2A (uint8) → `2a`
- b = 1.5 (float32) = 0x3FC00000 → `00 00 c0 3f`
- c = −3 (int16, two's complement) = 0xFFFD → `fd ff`

**`2a 00 00 c0 3f fd ff`**

---

## Q09 — all-ones offset/length with a nonzero crc

§15.2 fixes the sentinel as "offset and length both `0xFFFF_FFFF_FFFF_FFFF`
and crc 0". Here crc = 1, so §15.3's second row applies: "offset = S ∧
length = S ∧ crc ≠ 0 | *structural*: reject-tile".

**(a)** Register row **T6**: "A tile-index entry has offset and length both
0xFFFF_FFFF_FFFF_FFFF but crc ≠ 0".

**(b) no.** §9.7 `[R-LIF-08]`: "an entry `[R-IDX-03]` classifies reject-tile
on a *structural* ground contributes no stored extent to the walk". §15.3
agrees: such an entry "contributes … none to `[R-LIF-08]`'s coverage walk, so
any bytes it nominally addressed that no other claimant claims fall to slack".

**(c) no.** §16.2 `[R-SLB-03]`: "Sentinel tiles are transparent to run
continuity … **So are the entries §15.3 classifies reject-tile on a
*structural* ground**: they address no usable extent, and the run's stored
tiles close over them." (Contrast the crc-failing entry, which is *not*
transparent — not this case.)

**(d) refuse.** §20.5: "An entry §15.3 classifies reject-tile on a structural
ground is neither — `[R-IDX-03]` gives it no stored extent for a re-pointing
to target — so regenerating the region cannot proceed without meeting it, and
the violation is thereafter one the compactor has detected. `[R-WRT-06]` then
obliges **refusal**: the compactor can neither reproduce the entry nor invent
a replacement, and no drop is available, a tile-index entry being no record
§20.4's table licenses dropping."

---

## Q10 — reserved-range sub-record type 0x0500 with MU = 0

0x0500 falls in §10.2's record-type **reserved** range 0x0003–0x7FFF.

**(a) ignore-record.** `[R-CNT-18]`: "an unknown sub-record type with MU = 1
is reject-layer … with MU = 0 it is ignore-record." `[R-CNT-15]` confirms
reserved-range types are read the same way as experimental ones: "Readers of
both apply the MU rule above unchanged", and `[R-EXT-03]` routes sub-records
to `[R-CNT-18]`.

**(b) nonconforming.** `[R-CNT-15]`: "one from the reserved range is a value
this specification has not assigned — **emitting it is a violation**, and a
verifier MUST treat a reserved-range record type as a validity error at the
record's governing scope."

**(c) L25** — "A layer record's sub-record carries a type value from the
reserved range 0x0003-0x7FFF, which this specification has not assigned;
emitting one is a violation **whatever its MU bit**". (L24 is the MU = 1
specialization and does not apply here; §21.1: "a file exhibiting a
specialization is recorded against the narrower row" — MU = 0 keeps it at
L25.)

**(d) verifier**, per L25's Detector cell.

Noted oddity, answered as written: §21.3's heading assigns L25 the outcome
reject-layer, while the reader's outcome for this sub-record is
ignore-record. §21.1 reconciles them: "For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not
an obligation on any reader: the governing rule states what a reader does."

---

## Q11 — flags = 0x00010000 on a newly created file

0x00010000 sets bit 16 → the **ignore lane** (bits 16–31), not the incompat
lane (bits 0–15).

**(a) conforming.** §6.3 `[R-CNT-08]`: "a set ignore-lane bit is not a
file-conformance violation — such bits are defined by later minor versions,
and files carrying them are conforming files this text's readers ignore."
§21.6 lists it as a defined non-violation: "An ignore-lane flag bit (16–31)
is set | Ignored; **the file is conforming**". No violation is established and
nothing is unable to be checked, so §2.3's verdict is *conforming*.

**(b) no.** F19 covers only "Any bit of the flags **incompat** lane (bits
0-15)". No other register row reaches this file.

**(c) yes.** `[R-CNT-08]`: "a writer creating a file under this text **MUST
write flags = 0**". `[R-CNF-02]` classifies it as a conduct rule: "A writer
obligation whose violation this specification expressly declares not to be a
file-conformance violation binds the actor in the same way; §6.3's flags = 0
against a set ignore-lane bit … are the cases this text states."

So: an all-caps MUST is violated, the file is conforming, and no register row
fires — which is exactly the shape §21.1's completeness clause tolerates,
since the register enumerates *file-conformance* violations only.

---

## Q12 — slack total

§9.7 names the claimants: the directory, each record's extent, the stored
extent of each non-sentinel index entry, plus "The front signature block at
[0, 16) and the live trailer at [F − 64, F) … being members of the live
committed state". A layer record's extent slot addresses its tile-index
region, which "enters the walk once, as that record's extent, and is not a
second claimant beside it"; a record itself is not a claimant, its bytes
lying inside the directory region.

Index region size: d = 1, E = 4, T = 2 → G = 2, N = 2, interleaved →
entry_count = 2. `[R-CNT-17]`: 2·20 + ⌈2/65536⌉·4 = 40 + 4 = 44. Region
[3072, 3116).

| Claimant | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile, disk ordinal 0 | [1024, 1124) | 100 |
| stored tile, disk ordinal 1 | [2048, 2148) | 100 |
| tile-index region (layer record extent) | [3072, 3116) | 44 |
| user-metadata record extent | [3116, 3176) | 60 |
| directory region | [3200, 3400) | 200 |
| live trailer | [4032, 4096) | 64 |

All disjoint (verified programmatically). Claimed = 584.
Slack = F − claimed = 4096 − 584 = **3512**.

The walk completes, so `[R-CNT-21]`'s partial-total rule does not engage and
the figure is exact.

---

## Q13 — bad trailer CRC ahead of a foreign major

§6.2 `[R-CNT-06]` fixes the order: "A reader MUST validate, **in order**: the
trailer magic; the trailer CRC; the version gate (§6.3) … and then, those
gates passed, MUST validate all of the following".

The magic matches. The next check is the trailer CRC, which fails. Everything
else the question names — version_major = 5 (a capability refusal, not a
finding), dir_offset = 8 (F9), generation = 0 (F11) — lies at or behind
gates the reader never reaches.

§21.2's preamble confirms the CRC precedes the version gate and reaches even
a foreign-major file: "F8 and F1's trailer-magic instance, **F14's trailer
CRC — the two checks §6.2 places before the gate**".

**(a) F14** — "The u32 at trailer offset 60 does not equal the CRC-32C of
trailer bytes [0,60)".
**(b) reject-file** — §21.2's heading, and §6.2: "Any failure is
reject-file."

(The question's stem calls the file "format major version 1" while
version_major holds 5; the answer is unaffected either way, since the CRC
check precedes the version gate.)

---

## Q14 — dropping MU = 0 / PE = 0 records

Types 0x9001 and 0x9002 are ≥ 0x8000, the experimental range; with MU = 0
§21.6 makes them conforming and the updater does not implement either, so
§20.4's stored-flag row governs: "For a type the updater does not implement,
the stored flags are authoritative".

The MU = 0, PE = 0 row: "An appender MUST NOT drop it except in a commit that
*independently* changes the scope the record attaches to: for a layer
sub-record, **that layer's** record, the entry set of its index, or which of
its tiles are stored; for a top-level record, the file's layer set, **any
layer record's content**, or another *non-layer* top-level record."

Superseding a tile of B re-places B's index region, moving B's extent slot,
and §20.4 says so explicitly: "Superseding a stored tile's bytes re-places
that layer's index region … and so modifying that layer's record, which is
such a change: an appender superseding a tile MAY drop a top-level such
record, **or such a sub-record of the layer whose tile it superseded**".

**(a) yes** — the top-level 0x9002 record qualifies via "any layer record's
content", which layer B's record satisfies.

**(b) no** — the qualifying change for a sub-record must be to *that*
layer's record, index entry set, or stored-tile set. This commit touches
layer B; layer A's record, index and stored tiles are untouched. The permission
is granted only for "such a sub-record of the layer whose tile it
superseded", which is B, not A.

---

## Q15 — planar slab runs and a packing gap

G = ⌈10/2⌉ = 5, N = 5, C = 2 → 10 addressed tiles, disk ordinals 0–9.

§16.2 `[R-SLB-02]`: "Runs partition each contiguous block of disk ordinals
independently: for an interleaved layer the single block [0, N); **for a
planar layer each channel block [c·N, (c+1)·N) — runs never span channel
blocks, and the final run of a block can cover fewer than S ordinals**. Run r
of a block starts at ordinal block_start + r·S."

Block 0 = [0, 5) with S = 3 → runs [0, 3) and [3, 5).
Block 1 = [5, 10) with S = 3 → runs [5, 8) and [8, 10).

**(a) [0, 3), [3, 5), [5, 8), [8, 10)**

**(b)** Run [0, 3) holds entries 0 (stored, 8192 + 100), 1 (sentinel —
transparent to run continuity), 2 (stored, 8300). `[R-SLB-03]`: "each stored
tile's offset equals the previous stored tile's offset plus its length".
Expected 8192 + 100 = 8292; actual 8300 — an 8-byte gap.

Alignment is fine: 8192 mod 4096 = 0, so `[R-SLB-03]`'s first-stored-tile
rule (L42) is satisfied. The exercised row is **L41** — "Inside a slab run, a
stored tile's offset ≠ the previous stored tile's offset plus that tile's
length (**gap**, overlap, or out-of-ordinal placement; sentinels … are
transparent…)" — instance *gap*, detector verifier.
