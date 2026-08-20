# Cleanroom round 13 — quiz KEY transcript

## Disclosure

Files read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only
(read in five contiguous chunks covering lines 1–4128, i.e. the whole
document), plus four `grep -n` calls against that same file.

Local computation run: `python3 -c` one-liners implementing CRC-32C
(Castagnoli, reflected, init/final 0xFFFFFFFF) and the arithmetic below.
No files were read by any of those scripts. My CRC implementation was
validated against **every** CRC constant this document publishes before I
used it for an answer:

| Constant | Spec says | I computed |
|---|---|---|
| CRC-32C("123456789") §4.5 | 0xE3069283 | 0xE3069283 |
| CRC-32C(zero bytes) §4.5 | 0x00000000 | 0x00000000 |
| Appendix A trailer CRC | 0xE00938D2 | 0xE00938D2 |
| §7.4 example, 4 sentinel entries | 0x80A34955 | 0x80A34955 |
| §7.4 example, crc_of_crc_array | 0xC4EE982E | 0xC4EE982E |
| §15.4 full all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 |

Nothing else read: no ADRs, no `docs/`, no `conformance/`, no
`registry.json`, no PLAN.md / AGENTS.md / README, no git history, no web.
I did not read or list the round13 output directory. I wrote only this
transcript file into it.

---

## Q01 — extent growth on a fully-stored layer

Declared (y, x), E = (5, 5), T = (4, 4), interleaved, lin 1, codec 1,
filter 1, A = 0, S = 0, one uint16 channel `v`, fill bytes `CD AB`
(= 0xABCD). Generation 3 stores every addressed tile. Commit raises
E to (8, 8) and changes nothing else.

**Grid arithmetic (§11.2, `[R-GEO-03]`).** Before: G = (⌈5/4⌉, ⌈5/4⌉)
= (2, 2), N = 4. After: G = (⌈8/4⌉, ⌈8/4⌉) = (2, 2), N = 4.
Interleaved ⇒ addressed-tile count = N = 4 both before and after.
entry_count unchanged at 4; extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84
unchanged (`[R-CNT-17]`). P = ∏Tᵢ = 16 unchanged; Q = 2 unchanged;
decoded size = P·Q = 32 unchanged.

**(a) Permitted?** `[R-WRT-04]` step 4 prohibits a declaration change
that alters, for a stored tile, "the set of padding positions … the
decoded size, the byte offset of any sample … or the codec and filter".
Growing E does alter the padding-position set here — before the growth
G·T = 8 > E = 5 along both axes, after it G·T = 8 = E, so the layer has
no padding positions at all. But the same requirement carves the case
out explicitly:

> "and an extent MAY always **grow**, since a position that becomes real
> held that channel's fill and fill is a legal sample value."
> — §20.3, `[R-WRT-04]`

The 15 former padding positions of the edge tile carried `CD AB` by
`[R-SER-05]`; they now read as the sample value 0xABCD, "a legal sample
value". §11.1's rationale says the same from the other side: "Extents
grow; they do not shrink". **yes.**

**(b) Must the tile-index region be re-emitted?** `[R-WRT-04]` step 4:
"Every layer whose stored-tile set or index content this commit changes
has its tile-index region re-emitted in full … A layer whose record
alone changes keeps its extent slot, pointing at the existing region".
The stored-tile set is unchanged and no entry's bytes change (ordinals
do not renumber, since every Gᵢ is unchanged). §11.1's rationale is
decisive: "Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2)
unchanged touches the directory alone." **no.**

**(c) Must stored payload bytes be re-emitted?** No declaration a stored
tile depends on changed in a way that invalidates its bytes: decoded
size, sample offsets, codec and filter are all unchanged, and the
formerly-padding bytes are now legal real samples. **no.**

**Answer: `yes; no; no`.** High confidence.

---

## Q02 — interleaved byte offset of channel `c`

Dims (z, y, x), E = (10, 40, 60), T = (4, 8, 16). Channels in declared
order: `a` uint8 B=1, `b` float32 B=4, `c` int16 B=2, `d` bool B=1
(interleaved bool has element size 1, §14.2/§12.1).

In-tile position (§11.4, `[R-GEO-06]`): uᵢ = xᵢ mod Tᵢ
= (5 mod 4, 20 mod 8, 33 mod 16) = (1, 4, 1).

In-tile sample ordinal = Σ uᵢ·∏_{j>i} Tⱼ
= 1·(8·16) + 4·(16) + 1 = 128 + 64 + 1 = **193**.

Sample stride Q = Σ Bᵢ = 1 + 4 + 2 + 1 = 8.
Channel 2's in-sample offset F² = Σ_{j<2} Bⱼ = 1 + 4 = 5.

§14.2 `[R-SER-02]`, closing form of §14.2's example: "channel c's value
at in-tile ordinal u sits at byte u · Q + Fᶜ".

193 · 8 + 5 = 1544 + 5 = **1549**.

High confidence.

---

## Q03 — planar bool packed plane, all-false interior

E = (2, 2), T = (3, 3), planar, one bool channel `m`, fill byte 0x01
(true). G = (⌈2/3⌉, ⌈2/3⌉) = (1, 1), N = 1, C = 1 ⇒ addressed tiles
= C·N = 1. P = ∏Tᵢ = 9.

Planar bool ⇒ §14.3 packed plane, decoded size ⌈9/8⌉ = 2 bytes.

In-tile ordinal u_y·3 + u_x; positions with u ≥ 2 on either axis are
padding (`[R-GEO-04]`), and `[R-SER-05]` fixes padding content to the
fill bit (true = 1):

| ordinal | (u_y,u_x) | real? | bit |
|---|---|---|---|
| 0 | (0,0) | real | 0 |
| 1 | (0,1) | real | 0 |
| 2 | (0,2) | pad | 1 |
| 3 | (1,0) | real | 0 |
| 4 | (1,1) | real | 0 |
| 5 | (1,2) | pad | 1 |
| 6 | (2,0) | pad | 1 |
| 7 | (2,1) | pad | 1 |
| 8 | (2,2) | pad | 1 |

LSB-first packing (§14.3): value k at bit k mod 8 of byte k div 8.
Byte 0 = bits 0..7 = 0,0,1,0,0,1,1,1 = 0x04+0x20+0x40+0x80 = **0xE4**.
Byte 1 bit 0 = value 8 = 1. P mod 8 = 1 ≠ 0, so bit positions 1..7 are
pad bits, and `[R-SER-05]` requires each to carry the fill bit = 1
("Every pad bit (§14.3) MUST carry the plane's channel's fill bit").
Byte 1 = **0xFF**.

**Answer: `e4 ff`.** High confidence. (Cross-check: §14.3's own example,
fill true, P = 10, gives `55 FD` — the same pad-bits-set behavior.)

---

## Q04 — interleaved tile, byte-shuffle, codec none

E = (2,2), T = (2,2) ⇒ P = 4, G = (1,1), one tile. Channels `a` uint8,
`b` uint16. Q = 3, decoded size P·Q = 12.

Decoded tile image (§14.2, sample-major, little-endian):

| ordinal | a | b (LE) | bytes |
|---|---|---|---|
| 0 | 00 | 0x0201 | 00 01 02 |
| 1 | 03 | 0x0504 | 03 04 05 |
| 2 | 06 | 0x0807 | 06 07 08 |
| 3 | 09 | 0x0B0A | 09 0A 0B |

Image = `00 01 02 03 04 05 06 07 08 09 0a 0b`.

Filter 2, byte-shuffle (`[R-COD-10]`): "The shuffle stride s is … the
sample stride Q for an interleaved tile"; s = 3, L = 12, n = L/s = 4;
"the filtered image places byte i of group j at offset i · n + j".

- i = 0 → offsets 0..3: 00, 03, 06, 09
- i = 1 → offsets 4..7: 01, 04, 07, 0a
- i = 2 → offsets 8..11: 02, 05, 08, 0b

Codec 1 (`[R-COD-04]`): "The stored bytes are the filtered image
verbatim", and length must equal decoded size (12 ✓).

**Answer: `00 03 06 09 01 04 07 0a 02 05 08 0b`.** High confidence.

---

## Q05 — trailer CRC bytes at [F−4, F)

F = 192 ⇒ trailer occupies [128, 192); trailer bytes [60, 64) = file
offsets [188, 192) = "a CRC-32C at F − 4 covering bytes [F − 64, F − 4)"
(`[R-CNT-24]`), i.e. CRC-32C over trailer bytes [0, 60), stored
little-endian (`[R-ENC-09]`).

Trailer bytes [0,60), built per §6.2's layout table:

```
8a 4e 52 41 54 0d 0a 1a   magic
01 00                      version_major = 1
00 00                      version_minor = 0
00 00 00 00                flags = 0
02 00 00 00 00 00 00 00    generation = 2
10 00 00 00 00 00 00 00    dir_offset = 16
64 00 00 00 00 00 00 00    dir_length = 100
c0 00 00 00 00 00 00 00    committed_file_length = 192
ef be ad de 00 00 00 00    file_id = 0x00000000DEADBEEF
00 00 00 00                reserved
```

CRC-32C = 0x98C09A8D → stored LE as `8d 9a c0 98`.

Sanity of the premise: 16 + 100 = 116 ≤ 192 − 64 = 128 ✓; 192 mod 64 = 0 ✓;
generation ≥ 1 ✓; file_id ≠ 0 ✓.

**Answer: `8d 9a c0 98`.** High confidence (implementation validated
against all six published CRC constants).

---

## Q06 — smallest F for a one-record directory

Inline payload sizes from §7.4's table (widths confirmed against §7.4's
worked example, which sums 4 + 34 + 18 + 12 + 13 = 81):

| Field | bytes |
|---|---|
| name `a` (u8 len + 1) | 2 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| slab alignment u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| 1 dimension entry: name(2) + extent(8) + tile extent(8) | 18 |
| 1 channel entry: name(2) + type(2) + fill(1 len + 1) | 6 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| **total inline_length** | **73** |

(The "nine scalars from layout through channel count" = 34 bytes, matching
§7.4's example exactly.)

Geometry: one dimension, E = 0, T = 1 ⇒ G = ⌈0/1⌉ = 0, N = 0, interleaved
⇒ addressed-tile count 0 ⇒ entry_count = 0 (`[R-CNT-17]`), and
crc_of_crc_array = 0 forced (`[R-CNT-23]`). §7.4: "a layer with zero
addressed tiles has extent (0, 0)" — so the record claims **no** extent
bytes anywhere in the file. No tile-index region, no stored tiles.

Record = 24-byte header + 73 = 97 bytes.
Directory region = 97 + 4 (terminal CRC-32C, §7.1) = dir_length **101**.
dir_offset = 16 ⇒ region [16, 117).

Constraints (`[R-CNT-06]`): dir_offset + dir_length ≤ F − 64 and F ≡ 0
(mod 64). 117 ≤ F − 64 ⇒ F ≥ 181 ⇒ smallest multiple of 64 is **192**.

At F = 192: trailer [128, 192), pre-trailer pad [117, 128) = 11 bytes of
slack — permitted, and exactly what `[R-LIF-02]` step 5 produces ("pads
to the next 64-byte boundary"). ≥ 128-byte floor ✓ (`[R-CNT-27]`).

**Answer: 192.** High confidence.

*Aside on the question's wording:* it says "All four names are single
ASCII bytes", but a rank-1, one-channel layer record carries exactly
three names (layer, dimension, channel). The miscount does not affect the
arithmetic — every name present is one byte plus its one-byte prefix.

---

## Q07 — slab run with a half-sentinel entry

rank 1, E = 32, T = 4 ⇒ G = 8, N = 8, interleaved ⇒ 8 addressed tiles,
disk ordinals 0–7. S = 4 ⇒ `[R-SLB-02]`: for an interleaved layer the
single block [0, 8) partitions into run 0 = [0,4) and run 1 = [4,8).
Ordinals 4–7 are exactly run 1.

**(a) Ordinal 5**: offset = 0xFFFF_FFFF_FFFF_FFFF = S, length = 32 ≠ S.
§15.3's third row: "offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S |
*structural*: reject-tile". Register row T7. The outcome-class spelling
§2.4 fixes is **reject-tile**. (Note the entry's crc = 0 is irrelevant
here; the offset/length disagreement decides it.)

**(b) Packing violation in run 1?** `[R-SLB-03]`: "each stored tile's
offset equals the previous stored tile's offset plus its length …
Sentinel tiles are transparent to run continuity … So are the entries
§15.3 classifies reject-tile on a *structural* ground: they address no
usable extent, and the run's stored tiles close over them."

- ordinal 4: stored, offset 8192, length 100
- ordinal 5: structural reject-tile ⇒ **transparent**
- ordinal 6: stored, offset 8292, length 50
- ordinal 7: valid sentinel ⇒ **transparent**

Packing check over the run's stored tiles only: 8192 + 100 = 8292 = the
next stored tile's offset ✓. First stored tile 8192 mod A_slab(4096) = 0 ✓
(not asked, but no L42 either). No gap, no overlap, no out-of-ordinal
placement ⇒ no L41. **no.**

**Answer: `reject-tile; no`.** High confidence.

---

## Q08 — reserved vs experimental metadata encoding

§18.2 `[R-MTA-03]` / §10.2's table: metadata encoding u8 — 0 invalid,
1 and 2 assigned, **3–0x7F reserved**, **≥ 0x80 experimental**.

- File A: 0x40 = 64 ⇒ **reserved** range.
- File B: 0x90 = 144 ⇒ **experimental** range.

File A hits register row **R1** (§21.5): "A user-metadata record declares
a document encoding of 0, or a reserved-range value (3-0x7F)" — outcome
ignore-record, detector reader. §21.5's preamble: "Every row here is a
violation all the same: the outcome bounds a reader's blast radius and
never makes the file conforming (`[R-CNF-12]`)". `[R-EXT-03]` likewise:
"a value from a reserved range MUST NOT be emitted at all before this
specification assigns it". A verifier traversing to completion
establishes that violation ⇒ **nonconforming**.

File B falls under §21.6's defined non-violation:

> "A user-metadata record declares an experimental-range (≥ 0x80)
> document encoding | Ignored (ignore-record); the file is conforming —
> §10.3's prohibition binds a writer's conduct, not the bytes. No
> document rule attaches under an unassigned encoding, so a verifier
> certifies, reporting the record it ignored"

`[R-MTA-10]` confirms there is no cannot-establish ground: "A verifier
meeting such a record in an otherwise conforming file has no requirement
it is unable to check". Both A and B are otherwise fully conforming
(layer record conforming; extent slot well formed; extent_length 64 ≥ 5;
inline_length 1; terminal CRC verifies over the preceding 60 bytes).
⇒ **conforming**.

**Answer: `nonconforming; conforming`.** High confidence.

*Aside:* the premise "differ in exactly one byte" cannot literally hold —
the directory region's terminal CRC-32C covers the record sequence
(§7.1), so the two files necessarily differ in five bytes. The
framing device does not affect either verdict.

---

## Q09 — established violation vs. unexecutable codec

Layer A: codec 3 (zstd), stored tiles; verifier cannot execute zstd ⇒
`[R-COD-11]`: "A verifier that cannot execute a layer's codec or filter
cannot establish that layer's conformance and MUST NOT certify the
file." That is a cannot-establish *ground*, not a finding.

Layer B: bool channel with one-byte fill 0x02. `[R-TYP-07]`: "For bool,
the fill field is one byte and its value is constrained: `0x00` (false)
or `0x01` (true). Writers MUST NOT emit any other byte; a reader MUST
treat any other byte as a validity error at layer scope." Register row
**L35**, detector reader, detected at layer access, reject-layer. The
verifier traverses the whole file, so it reaches and establishes it.

`[R-CNF-11]` settles the ordering:

> "An established violation takes priority: a verifier that has
> established any violation reports *nonconforming*, however many
> requirements it was unable to check, and *cannot establish* is
> available only to a traversal that established no violation."

**Answer: `nonconforming`.** High confidence. (The verifier must still
report, per `[R-CNF-11]`, the requirements it could not check on layer A;
that constrains the report, not the verdict. A side note: software that
cannot execute a core codec is strictly not a conforming reader under
`[R-CNF-03]`, yet §2.3 and `[R-COD-11]` both explicitly contemplate this
verifier — the tension does not change the verdict either way.)

---

## Q10 — two ranges to fetch before using entry 150,000

index_encoding 1, entry_count = 200,000; region layout §15.1:
`[entry array: 200000 × 20 = 4,000,000 bytes][segment CRC array:
⌈200000/2¹⁶⌉ × 4 bytes]`.

Segments (§15.4): segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶,
entry_count)). 150,000 div 65,536 = 2, so entry 150,000 is in **segment
2**, covering entries [131,072, 196,608) — a full segment, since
196,608 < 200,000.

Segment 2's byte range from region byte 0: [131072·20, 196608·20)
= **[2,621,440, 3,932,160)**.

Segment count = ⌈200000/65536⌉ = 4 ⇒ CRC array is 16 bytes, placed
immediately after the entry array: **[4,000,000, 4,000,016)**.

Cross-check with `[R-CNT-17]`: extent_length = 200000×20 + 4×4 =
4,000,016 = the array's end ✓.

`[R-IDX-04]`: "To use entry k, a reader MUST verify, in dependency order,
crc_of_crc_array over the fetched CRC array and the segment CRC over the
fetched segment containing k (both ranges are computable from the layer
record alone and MAY be fetched in parallel)".

**Answer: `2621440,3932160,4000000,4000016`.** High confidence.

---

## Q11 — a 40 MiB metadata document against a 16 MiB bound

**(a)** §21.9's table states *minimum guarantees, not caps*
(`[R-ERR-03]`), and §18.2's note is explicit: "A file whose document
decodes to more than the guarantee stays conforming, and it falls outside
`[R-CNF-03]`'s acceptance duty". Every structural check passes. **yes.**

**(b)** §18.2's note again: "a reader that instead declines on resource
grounds under `[R-ERR-04]` does so at the whole file, a document having
no declared size and so no narrower scope whose declarations that rule
can measure." **file.**

**(c)** `[R-MTA-09]`: "A **verifier** that declines to decode a document
on the bound above cannot establish that document's conformance and MUST
NOT certify the file … it fixes the file's verdict as *cannot establish*
only where the verifier established no violation elsewhere". No violation
established anywhere ⇒ **cannot establish**.

**Answer: `yes; file; cannot establish`.** High confidence.

---

## Q12 — codec 4 (lz4) decoded-size cap, both layouts

E = (25000, 10000), T = (25000, 10000) ⇒ G = (1, 1), N = 1, P = 25000 ×
10000 = 250,000,000. Channels `w` float64 (B = 8) and `f` bool.

`[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of
whose addressed tiles' decoded size exceeds 0x7E000000 bytes … in a
planar layer each channel's plane carries its own decoded size (§14.2,
§14.3), and the largest governs — and a reader MUST treat such a
declaration as a validity error at layer scope, checkable from
declarations alone."

Cap = 0x7E000000 = 2,113,929,216.

**Interleaved.** Bool is a single byte in an interleaved tile (§14.2), so
Q = 8 + 1 = 9. Decoded size = P·Q = 2,250,000,000 > 2,113,929,216 ⇒
**error** (register row L44, instance "interleaved P·Q", reader, layer
access, reject-layer).

**Planar.** Two planes, each its own decoded size (§14.2 / §14.3):
- `w`: P·B = 250,000,000 × 8 = 2,000,000,000 ≤ cap ✓
- `f`: packed bool plane, ⌈P/8⌉ = 31,250,000 ≤ cap ✓

Largest = 2,000,000,000, under the cap ⇒ **permitted**.

Overflow check (`[R-ENC-04]`): every product here is far below 2⁶³ − 1 ✓.

**Answer: `error; permitted`.** High confidence. Note the deliberate
oddity the numbers were chosen to produce: the same geometry and the same
channels are legal under codec 4 planar and illegal interleaved, because
one packed bit-plane versus one interleaved byte per sample moves the
largest decoded size across the cap.

---

## Q13 — which commit may drop the MU = 0 / PE = 0 record

Type 0x9000 ≥ 0x8000 ⇒ experimental range, unassigned; the updater does
not implement it, so §20.4's "For a type the updater does not implement,
the stored flags are authoritative" applies, giving the MU = 0, PE = 0
row:

> "Retain byte-identical, or drop it — its extent becoming slack. An
> appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: … for a top-level record, the file's
> layer set or another *non-layer* top-level record. Superseding a stored
> tile's bytes is not such a change for either kind — it re-places that
> layer's index region … without altering the scope any record attaches
> to — so a commit whose only change is a supersede MUST retain the
> record. Dropping the record, or dropping another record in the same
> commit, is not itself such a change either, so a commit whose only
> effect would be the drop MUST retain it."

- **(a)** supersedes one tile's stored bytes, nothing else — named
  verbatim as *not* such a change ⇒ must retain.
- **(b)** adds a new layer M — changes "the file's layer set" ⇒ **may
  drop**.
- **(c)** the drop is the commit's only effect — named verbatim as *not*
  such a change ⇒ must retain.

**Answer: `b`.** High confidence.

---

## Q14 — coverage walk slack total

F = 512. Claimants of the live committed state (§5.2 `[R-CNT-02]`, walked
per §9.7 `[R-LIF-08]`):

| Claimant | Range | Bytes |
|---|---|---|
| front signature block | [0, 16) | 16 |
| stored tile (entry 1) | [16, 48) | 32 |
| layer record's extent = tile-index region | [64, 148) | 84 |
| stored tile (entry 2) | [148, 180) | 32 |
| user-metadata record extent | [180, 220) | 40 |
| directory region | [328, 448) | 120 |
| live trailer | [448, 512) | 64 |
| **total claimed** | | **388** |

Notes on what is *not* a separate claimant: "A record is not a claimant
of its own — its header and inline payload lie inside the directory
region"; "A layer record's extent slot addresses that layer's tile-index
region (§7.4), so the region enters the walk once, as that record's
extent, and is not a second claimant beside it"; and the front block and
live trailer "are claimed by the walk as well, being members of the live
committed state" (§9.7).

Consistency: index extent_length 84 = 4×20 + ⌈4/2¹⁶⌉×4 ✓ (`[R-CNT-17]`);
two sentinels contribute no extent (`[R-IDX-02]`). All seven ranges are
pairwise disjoint and each of the five interior ones lies in [16, 448) ⊂
[16, F − 64) ✓.

**(a)** Slack = 512 − 388 = **124** bytes, lying in [48, 64) = 16 bytes
and [220, 328) = 108 bytes. 16 + 108 = 124 ✓.

**(b)** `[R-CNT-21]` makes a total partial only "Where the walk of §9.7
does not enumerate every region's claimants — whether because a
scope-level rejection ends that scope's enumeration … or because the
verifier elected under `[R-CNF-11]` to stop at the first violation". The
question stipulates the walk completes with neither. **no** — the total
"tighten[s] to the exact total when the walk completes".

**Answer: `124; no`.** High confidence.

---

## Q15 — reserved-range top-level type with MU = 1

Type 0x0005 lies in the record-type reserved range 0x0003–0x7FFF
(§10.2). flags 0x0003 ⇒ MU = 1, PE = 1; reserved bits 2–15 are zero
(so no F26), and the MU = 1 / PE = 0 combination is not present (so no
F25). inline_length 0 and extent slot (0, 0) are each unremarkable for an
unknown type ((0, 0) "means no extent", `[R-CNT-13]`).

Two rows describe the condition — which is what the question says:

- **F35**: "A top-level record has a reserved-range type value
  (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1" —
  detector reader, detected **open**.
- **F36**: "A top-level record carries a type value from the reserved
  range 0x0003-0x7FFF … emitting one is a violation whatever its MU bit"
  — detector verifier, detected certification.

§21.1 resolves the pair explicitly:

> "Some rows are strict specializations of others — F1 of F6 and of F8,
> **F35 of F36**, L24 of L25 — and a file exhibiting a specialization is
> recorded against the narrower row, whose detector and detection point
> are the ones that apply."

So the file is recorded against **F35**, whose Detected cell reads
**open**.

**Answer: `F35; open`.** High confidence.

---

## Underdetermination review

I looked for genuine ambiguity in each item and found none that changes
an answer. The nearest calls, recorded for the record:

- **Q01(a)** — `[R-WRT-04]`'s prohibition on altering "the set of padding
  positions" and its "an extent MAY always grow" clause are in tension on
  their faces. The clause is a stated exception inside the same
  requirement, and §11.1's rationale ("Extents grow; they do not shrink")
  reads the same way, so the resolution is not in doubt.
- **Q08** — the "exactly one byte" premise is unsatisfiable (directory
  CRC). Answered on the encoding-byte value sets, which is what the
  question turns on.
- **Q06** — "four names" miscounts a three-name record; the byte
  arithmetic is unaffected.
- **Q09** — a verifier that cannot execute zstd is arguably not a
  conforming reader (`[R-CNF-03]`), yet §2.3 and `[R-COD-11]` both name
  that situation; the verdict is `nonconforming` under either reading,
  since an established violation dominates.
