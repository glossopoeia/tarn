# Round 19 — quiz answerer transcript

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(sequentially, whole, via `sed -n`/`grep`). I read no ADR, no test vector, no
manifest, no registry.json, no PLAN/AGENTS/README, no git history, no web. I ran
one local Python script (`crc.py` in this scratchpad, written by me) implementing
CRC-32C and integer arithmetic; it reads no files. I validated the CRC
implementation against three constants the specification itself states
(§4.5's `CRC-32C("123456789") = 0xE3069283`; §7.4's worked example
`0x80A34955` / `0xC4EE982E`; §15.4's `0xEECB3BB2`) — all three reproduced
exactly.

---

## Q01 — compactor output flags and minimum version_minor

**(a)** `[R-WRT-06]` (§20.5): "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward, in place of the flags = 0 §6.3 requires of a file
created under this text (`[R-CNT-08]`)." §6.3 says the same: "A compactor, though
its output is a new file, carries the input's unknown ignore-lane bits into its
output trailer rather than writing flags = 0."

Bits 18 and 20 are both in the ignore lane (bits 16–31, §6.2/§6.3), and the
compactor implements no flag bits, so both are *unknown* ignore-lane bits and both
carry forward. Output flags = 0x00140000 (bit 18 = 0x00040000, bit 20 =
0x00100000). Little-endian u32 (`[R-ENC-01]`), on disk: `00 00 14 00`.

**(b)** Two floors compete. `[R-CNT-26]` gives a floor of 0 "for a file
expressible under this text". But §20.5 raises it: "Where the output carries a
feature a later minor defines and this compactor does not — on a conforming input
a carried ignore-lane bit (§6.3) ... — the output's version_minor SHOULD be at
least the input's". The output does carry such bits, so the SHOULD applies and the
floor is the input's minor = **3**. The question asks for the smallest value that
deviates from no requirement *or recommendation*, so the SHOULD binds.

**Answer: `00 00 14 00`, 3.** Confidence high.

---

## Q02 — three compaction inputs

**(a)** offset = S (all-ones sentinel value), length = 0x40, crc = 0. §15.3's third
row: "offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S | *structural*:
reject-tile" (register row T7). `[R-WRT-07]`: "Regenerating a region means
classifying every entry in it: a sentinel is re-emitted unchanged, and every other
entry is re-pointed to where its stored extent now lies. An entry §15.3 classifies
reject-tile on a structural ground is neither ... so regenerating the region cannot
proceed without meeting it, and the violation is thereafter one the compactor has
detected. `[R-WRT-06]` then obliges refusal: the compactor can neither reproduce
the entry nor invent a replacement, and no drop is available, a tile-index entry
being no record §20.4's table licenses dropping." → **refuse**.

**(b)** type 0x8123 ≥ 0x8000 = experimental range (§10.2), MU = 0. §21.6: "A record
type this specification has not assigned, from the experimental range ... carries
MU = 0 | Ignored, and preserved or dropped per its PE bit" — the file is
conforming. §7.2: "For a record with MU = 0, the extent slot is its only sanctioned
reference to bytes outside the record sequence ... this is what lets a compactor
relocate an unknown ancillary's extent without parsing it (§20)." PE = 0, so
§20.4's table also offers "A compactor MAY drop it whenever it rewrites the file."
Either disposal is available; nothing obliges refusal. → **compact**.

**(c)** type 0x9000, MU = 1. `[R-WRT-06]`: "A compactor MUST refuse to compact a
file carrying any record whose type it does not implement with MU = 1: such a type
can define references this specification does not (§7.2), so its bytes cannot be
safely relocated." (Independently, §20.4 and `[R-CNT-15]` make an unimplemented
top-level MU = 1 record reject-file for the compactor-as-reader.) The file is
nonetheless conforming (§21.6's "conforming files a reader nevertheless refuses"),
which does not change the refusal. → **refuse**.

**Answer: refuse compact refuse.** Confidence high.

---

## Q03 — 192-byte empty file: verdict and slack

Trailer gates (`[R-CNT-06]`): magic ✓, CRC ✓, version_major 1 ✓, flags 0 ✓,
committed_file_length 192 = file size and 192 mod 64 = 0 ✓, dir_offset 16 ≥ 16 ✓,
dir_length 4 ≥ 4 ✓, 16 + 4 = 20 ≤ F − 64 = 128 ✓, generation 1 in range ✓,
file_id ≠ 0 ✓, reserved zero ✓. Directory region [16, 20) = `00 00 00 00` = CRC-32C
of zero bytes over a zero-length record sequence ✓ (§7.1, §4.5). Zero layers is a
non-violation (§21.6: "The file contains zero layers | A conforming file with an
empty directory").

The only oddity is the 108-byte gap between the directory's end (20) and the
trailer (128), where `[R-LIF-02]` step 5 would have padded only to 64. `[R-CNT-05]`
settles it: "a longer gap is conforming, and no conforming commit produces one",
and `[R-CNF-02]` names precisely this case as writer conduct rather than a
file-conformance violation: "§6.2's pre-trailer gap longer than `[R-LIF-02]` step
5's pad are the cases this text states". F7 registers only "A structure occupies
bytes between the live directory's end and the live trailer" — there is no
structure there. Verdict: **conforming**.

Slack (§9.7, `[R-CNT-21]`): the walk completes, so the total is exact, not partial.
Claimants: front block [0,16) = 16, directory [16,20) = 4, trailer [128,192) = 64 —
"The front signature block at [0, 16) and the live trailer at [F − 64, F) are
claimed by the walk as well". 192 − 16 − 4 − 64 = **108**.

**Answer: conforming, 108.** Confidence high.

---

## Q04 — crc_of_crc_array for a 3-entry all-sentinel index

d = 1, E = 70, T = 32 → G = ⌈70/32⌉ = 3 (§11.2). Interleaved, C = 1 → addressed-tile
count = N = 3, so entry_count = 3.

Index region (§15.1): 3 × 20 = 60 entry bytes, then ⌈3/2¹⁶⌉ × 4 = 4 bytes of segment
CRC array. Segment 0 covers entries [0, 3) — a *partial* segment, so `[R-IDX-05]`
forbids substituting the all-sentinel constant: "a partial segment's CRC MUST be
computed."

Sentinel = `FF ×16 00 ×4` (`[R-IDX-02]`). CRC-32C over the 60 bytes = **0xD171D122**,
stored `22 D1 71 D1`. crc_of_crc_array = CRC-32C over that 4-byte array (§7.4,
§15.4) = **0x34C74AFB**, stored little-endian.

Method validated on §7.4's own example (4 sentinels → 0x80A34955 → 0xC4EE982E):
reproduced exactly.

**Answer: `fb 4a c7 34`.** Confidence high.

---

## Q05 — 20-byte index entry for a packed-bool edge tile

Geometry: G = (⌈5/3⌉, ⌈5/3⌉) = (2, 2), N = 4, P = 3·3 = 9. Planar, C = 1, channel
index 0 → disk ordinal = c·N + s (`[R-GEO-06]`); s = t_y·G_x + t_x = 1·2 + 1 = 3, so
disk ordinal 3.

Planar bool plane → §14.3 packing: decoded size = ⌈9/8⌉ = 2 bytes, value k at bit
k mod 8 of byte k div 8, LSB-first.

Tile (1,1) covers y ∈ [3,6), x ∈ [3,6). Real positions (inside extents 5×5):
u_y, u_x ∈ {0,1}. In-tile ordinal = u_y·3 + u_x (§11.4). Real: 0, 1, 3, 4 → false → bit 0.
Padding positions (§11.3): ordinals 2, 5, 6, 7, 8 → `[R-SER-05]` fixes them to the
fill bit = 1 (fill byte 0x01 = true). P mod 8 = 1, so bits 1–7 of byte 1 are pad
bits, also the fill bit = 1 (`[R-SER-05]`: "Every pad bit (§14.3) MUST carry the
plane's channel's fill bit").

Byte 0: bits 0..7 = 0,0,1,0,0,1,1,1 → 0x04+0x20+0x40+0x80 = **0xE4**.
Byte 1: bit 0 (ordinal 8, padding) = 1; bits 1–7 pad bits = 1 → **0xFF**.
(Cross-check against §14.3's example convention: fill-true pad bits set, `55 FD`.)

Codec 1 and filter 1 → stored bytes = decoded image = `E4 FF`, and `[R-COD-04]`
requires length = decoded size = 2. crc = CRC-32C(`E4 FF`) = 0x69C99AA0.

Entry (§15.1): offset u64 = 512 = `00 02 00 00 00 00 00 00`; length u64 = 2 =
`02 00 00 00 00 00 00 00`; crc u32 = `a0 9a c9 69`.

**Answer: `00 02 00 00 00 00 00 00 02 00 00 00 00 00 00 00 a0 9a c9 69`.**
Confidence high.

---

## Q06 — layer `air`: inline_length and extent_length

Inline payload fields in §7.4's table order, packed with no padding
(`[R-CNT-18]`):

| part | bytes |
|---|---|
| name `air` (1 + 3) | 4 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| alignment A u64 | 8 |
| slab S u64 | 8 |
| slab alignment u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| 3 dimension entries (1+1 name + 8 + 8) × 3 | 54 |
| channel `u` float64: (1+1) + 2 + (1+8) | 13 |
| channel `flag` bool: (1+4) + 2 + (1+1) | 9 |
| index_encoding u8 | 1 |
| entry_count u64 | 8 |
| crc_of_crc_array u32 | 4 |
| sub-record: 24-byte header + inline_length 1 | 25 |
| **total** | **152** |

Cross-check against §7.4's worked example, which itemizes "4 + 34 bytes" for a
3-byte name plus the nine scalars: 1+2+2+2+8+8+8+1+2 = 34 ✓. Fill lengths are the
types' element sizes (`[R-CNT-23]`, §12.1): float64 = 8, bool = 1.

Extent slot: G = (⌈10/1⌉, ⌈100/50⌉, ⌈100/50⌉) = (10, 2, 2), N = 40; interleaved →
addressed-tile count = N = 40 = entry_count. `[R-CNT-17]`: extent_length =
40 × 20 + ⌈40/2¹⁶⌉ × 4 = 800 + 4 = **804**.

**Answer: 152, 804.** Confidence high.

---

## Q07 — three user-metadata encodings, verifier verdicts

**(a) 0x91** ≥ 0x80 = experimental range (§10.2, §18.2). §21.6: "A user-metadata
record declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming ... No document rule attaches at such an
encoding, so a verifier certifies, reporting the record it ignored." `[R-MTA-10]`
concurs: "A verifier meeting such a record in an otherwise conforming file has no
requirement it is unable to check ... and certification is unaffected."
→ **conforming**.

**(b) 0x05** is in the reserved range 3–0x7F. §21.5 row R1: "A user-metadata record
declares a document encoding of 0, or a reserved-range value (3-0x7F)" — a
violation, outcome ignore-record. §21.5's preamble: "Every row here is a violation
all the same: the outcome bounds a reader's blast radius and never makes the file
conforming". A verifier that has established any violation reports nonconforming
(`[R-CNF-11]`). → **nonconforming**.

**(c) 0x02**, decoded 20 MiB > the verifier's 16 MiB bound, declined. `[R-MTA-09]`:
"A **verifier** that declines to decode a document on the bound above cannot
establish that document's conformance and MUST NOT certify the file ... the decline
is not a finding that the file is nonconforming and a verifier MUST NOT report it
as one ... it fixes the file's verdict as *cannot establish* only where the
verifier established no violation elsewhere". No violation elsewhere and nothing
else unchecked. → **cannot establish**.

**Answer: conforming nonconforming cannot establish.** Confidence high.

---

## Q08 — entry_count, extent_length, segment index

G_y = G_x = ⌈100000/256⌉ = 391 (390·256 = 99840 < 100000 ≤ 391·256 = 100096).
N = 391² = 152,881. Planar, C = 3 → addressed-tile count = C·N = **458,643**
(§11.2, `[R-CNT-17]`).

extent_length = 458,643 × 20 + ⌈458,643/65,536⌉ × 4 = 9,172,860 + 7×4 =
**9,172,888** (6·65,536 = 393,216 < 458,643 ≤ 7·65,536 = 458,752).

t_y = 50,000 div 256 = 195; t_x = 60,000 div 256 = 234. s = t_y·G_x + t_x =
195·391 + 234 = 76,479 (`[R-GEO-06]`, linearization 1). Disk ordinal = c·N + s =
2·152,881 + 76,479 = 382,241. §15.4: "Segment s covers entries
[s·2¹⁶, min((s+1)·2¹⁶, entry_count))" → 382,241 div 65,536 = **5**
(5·65,536 = 327,680 ≤ 382,241 < 393,216).

**Answer: 458643, 9172888, 5.** Confidence high.

---

## Q09 — three planar channels at one coordinate

Layer record validated, whole index chain verified, so no layer-scope failure
intervenes.

- **channel 0**: well-formed non-sentinel entry, crc matches, decodes to exactly the
  decoded size — §19.4 steps 5–8 complete → **decoded**.
- **channel 1**: `FF ×16 00 ×4` = the sentinel exactly (`[R-IDX-02]`). §15.3 row 1:
  "valid sentinel — reads as fill"; `[R-TYP-08]`: in a planar layer "exactly the
  entry's channel reads as fill there" → **fill**.
- **channel 2**: offset = S, length ≠ S → §15.3's third row, *structural*:
  reject-tile (T7). `[R-CNF-09]`: "a read of a rejected tile MUST NOT silently
  return fill"; `[R-TYP-09]`: "A reader MUST NOT return fill for a tile whose entry
  is malformed (§15.3)". §19.4 step 8 bounds the failure to that entry's positions.
  → **failure**.

**Answer: decoded fill failure.** Confidence high.

---

## Q10 — zstd smallest Window_Descriptor on a 30-byte tile

Interleaved, P = 2·3 = 6, Q = 4 (float32) + 1 (bool byte, §14.2) = 5, decoded size
= P·Q = 30 — literally §14.2's own worked example ("With channels `t` (float32)
and `m` (bool) interleaved instead: Q = 5, decoded size 30").

Single_Segment_Flag clear + smallest Window_Descriptor: §17.2's Note states "without
it, the Window_Descriptor cannot express less than 1 KiB. A tile whose decoded size
is below 1 KiB — §14.2's worked examples give 18 and 30 bytes ... — is therefore
encodable under codec 3 only as a single-segment frame". So the declared window is
1 KiB > 30. `[R-COD-06]`: writers "MUST NOT declare a window size exceeding the
tile's decoded size; a reader MUST treat either as a validity error at tile scope,
both being header-checkable."

Outcome class (§2.4's four names): **reject-tile**. Register row: **T21** — "Codec 3
(zstd) and the frame declares a window size larger than the tile's decoded size".
Every other zstd row is excluded by the stipulations (magic present → not T17; one
frame → not T18; no dict ID → T19; no checksum flag → T20; decodes exactly and
consumes exactly → not T22/T24/T25; crc matches → not T1).

Note the oddity worth stating: this file is nonconforming purely because RFC 8878
cannot express a window small enough, and §21.9 lists an 8 MiB Window_Size *minimum
guarantee* that is irrelevant here — the rule violated is the per-tile ceiling, not
the reader floor.

**Answer: reject-tile, T21.** Confidence high.

---

## Q11 — decoded tile image length and bytes [5, 10)

G = (⌈5/4⌉, ⌈5/4⌉) = (2, 2). P = 4·4 = 16. Interleaved, Q = Σ Bᵢ = 1 (uint8) + 4
(float32) = 5. §14.2: decoded size = P·Q = **80**.

Tile (1,1) covers y ∈ [4,8), x ∈ [4,8); only (4,4) is inside the extents, i.e.
in-tile (0,0), ordinal 0. Ordinal 1 = in-tile (0,1) = coordinate (4,5), x = 5 ≥ E_x
= 5 → a padding position (§11.3).

§14.2's offset table: value k at (k div C)·Q + F_{k mod C}; equivalently "channel c's
value at in-tile ordinal u sits at byte u · Q + Fᶜ". Ordinal 1 occupies bytes
[1·5, 1·5+5) = [5, 10) — exactly the requested range, one whole sample.

`[R-SER-05]`: "at every padding position, a writer MUST encode, for each channel the
position carries, that channel's fill value — the recorded fill bytes for a numeric
channel, the recorded fill byte for an interleaved bool channel". So byte 5 = `a`'s
fill 0x2A (F⁰ = 0), bytes 6–9 = `b`'s fill 0xBF800000 little-endian (`[R-ENC-01]`,
F¹ = 1) = `00 00 80 bf`.

**Answer: 80, `2a 00 00 80 bf`.** Confidence high.

---

## Q12 — trailer dir_offset, dir_length, committed_file_length

Tile-index region: entry_count = 4, index_encoding 1 → extent_length =
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 (§7.4's example states 84 outright). Placed at [16, 100).

Directory begins at 100. Record sequence: one layer record = 24-byte header
(§7.2) + inline_length 81 = 105 bytes; plus the region's terminal CRC-32C, 4 bytes
(§7.1). dir_length = 105 + 4 = **109**. Directory ends at 209.

`[R-LIF-02]` step 5: "append the pad to the next 64-byte boundary". 209 → 256 (47
pad bytes). Trailer occupies [256, 320). committed_file_length = **320**, a multiple
of 64 ✓; dir_offset + dir_length = 209 ≤ F − 64 = 256 ✓; dir_offset 100 ≥ 16 ✓.

**Answer: 100, 109, 320.** Confidence high.

---

## Q13 — a shrink from (64, 64) to (64, 32)

**(a)** §20.3 step 4: "An extent MAY also **shrink**, and the bar above is the whole
of the test, **in the bar's own tense**: a shrink is permitted exactly where it
alters nothing §14 fixes for any tile the layer stores in the generation this
commit supersedes. Dropping a tile out of the addressed set (§11.2's grid count
falls) is not itself such an alteration — a tile the new state does not address
carries no §14 obligation and its extent becomes slack".

Old grid (4, 4), N = 16; new grid (⌈64/16⌉, ⌈32/16⌉) = (4, 2), N = 8. Surviving
addressed tiles are those with t_x ∈ {0, 1}. For each: tile extents unchanged, so
P = 256 and the decoded size and every in-tile byte offset are unchanged; codec and
filter unchanged; padding positions were empty before (4·16 = 64 = E_y, 4·16 = 64 =
E_x) and remain empty after (2·16 = 32 = E_x). So nothing §14 fixes for any
prior-generation stored tile is altered. Ordinal renumbering is expressly
contemplated, not barred ("a geometry change renumbers ordinals wherever
`[R-GEO-06]` moves them"), and `[R-CNT-17]` then obliges the smaller entry_count
and a re-emitted index region — which the commit does. → **yes**.

**(b)** `[R-PRV-01]` (§23.1): "A commit removes sample data two ways — superseding
it, and a shrink that de-addresses tiles (§20.3 step 4) ... Writers and the tools
built on them MUST NOT represent any commit that makes sample data unreachable as
erasure of it — a shrink reported as erasure misleads exactly as a supersede so
reported does." → **no**.

**Answer: yes no.** Confidence high.

---

## Q14 — Appendix G item 2 applied to the Appendix A file

Item 2: "its input the bytes [0, F − 64) followed by the trailer's first 60 bytes
with the `file_id` field zeroed".

Appendix A's file is 128 bytes, F = 128, F − 64 = 64. Hash input = bytes [0, 64) (64
bytes) ++ trailer bytes [0, 60) (60 bytes) = **124 bytes**. (The trailer CRC at
[60, 64) is excluded, which is what keeps the derivation non-circular.)

The eight zeroed bytes are the file_id field at trailer offset 48, size 8 (§6.2's
layout table). Measured within the hash input, the trailer's first byte sits at
input offset 64, so file_id occupies input offsets [64 + 48, 64 + 56) = **[112, 120)**.
(In the file itself those same bytes are [112, 120) too — an arithmetic coincidence
of F = 128, since the 64-byte prefix and the 64-byte trailer offset happen to
coincide; the question asks for the range within the hash input, which is what is
given.)

**Answer: 124, [112, 120).** Confidence high.

---

## Q15 — the row that witnesses a codec 3 → codec 1 re-declaration

§21.7 (`[R-ERR-01]`), "What no check detects": "§20.3 step 4's bar on a declaration
change is witnessed only where the affected tiles remain stored *and* the change
reaches a byte §14 structurally constrains ... a change that reaches the codec is
witnessed by the rows for the codec now declared, which test the stored bytes as a
stream of it (T15, T17, T23, T25), **or by T14 where the new declaration is codec
1**."

The new declaration is codec 1, so the row is T14: "Codec 1 (none) declared and a
non-sentinel index entry's length differs from the tile's decoded size"
(`[R-COD-04]`).

**Answer: T14.** Confidence high.

---

## Underdetermined questions

None of the fifteen. Each resolved to a single reading with a decisive sentence in
the document; the closest calls, and why they nonetheless resolve:

- **Q01(b)** — two floors (`[R-CNT-26]`'s 0 and §20.5's "at least the input's")
  appear to compete, but §20.5's condition ("the output carries a feature a later
  minor defines and this compactor does not") is met by the carried ignore-lane
  bits, and §20.5 says the `[R-CNT-26]` floor governs only "otherwise".
- **Q02(a)** — one might ask whether a compactor is *obliged* to regenerate that
  layer's index region at all. `[R-WRT-07]` treats regeneration as what a relocating
  compactor does, and states the consequence directly; and even a compactor that
  somehow copied the region would be barred by `[R-WRT-06]`'s "MUST NOT emit a file
  carrying a violation it has detected" once `[R-WRT-09]`'s index-chain verification
  put the region in front of it. Both roads end at refusal.
- **Q03** — the 108-byte pre-trailer gap looks like a violation until `[R-CNF-02]`
  names it as one of exactly two writer-conduct rules that are expressly not
  file-conformance violations.
