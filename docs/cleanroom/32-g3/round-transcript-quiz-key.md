# Cleanroom round 32 — quiz keyer transcript

Source read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4754 lines), read
in full in four contiguous chunks. No other file read. Scratch scripts written to
`/private/tmp/claude-501/.../r32-round/scratch/quiz-keyer/qk_crc.py` and `qk_arith.py`.

CRC implementation self-validated against two independent in-document anchors before use:
§4.5's check vector (CRC-32C("123456789") = 0xE3069283, CRC-32C(∅) = 0x00000000) and
Appendix A's minimal-file trailer CRC (0x402F157E, stored `7E 15 2F 40`). Both reproduced exactly.

Search method: the document is hard-wrapped and blockquotes wrap with `> `, so every phrase probe
was run against a normalised copy (blockquote markers stripped, all whitespace collapsed to single
spaces) rather than line-oriented grep. Every probe below returned HIT; no conclusion here rests on
a zero.

---

## Q01 — layer-record inline payload arithmetic

§7.4's table fixes the field order. Widths, in order:

| field | bytes |
|---|---|
| name `sst` (u8 len + 3) | 4 |
| layout u8 | 1 |
| linearization u16 | 2 |
| codec u16 | 2 |
| filter u16 | 2 |
| A u64 | 8 |
| S u64 | 8 |
| A_slab u64 | 8 |
| rank d u8 | 1 |
| channel count C u16 | 2 |
| dim `y` (1+1 name, 8 extent, 8 tile extent) | 18 |
| dim `x` | 18 |
| chan `a` (1+1 name, 2 type, 1+2 fill) uint16 | 7 |
| chan `b` (1+1 name, 2 type, 1+4 fill) float32 | 9 |

4+1+2+2+2+8+8+8+1+2 = 36; +18+18 = 72; +7+9 = 88+2 = 90. **index_encoding offset = 90.**
Cross-checked against §7.4's own worked example, whose rank-1/one-channel payload places
index_encoding at 68 with the identical field widths (name 4, nine scalars 34, dim 18, chan 12).

inline_length = 90 + 1 (index_encoding) + 8 (entry_count) + 4 (crc_of_crc_array) = **103**;
no sub-records, and §7.4 requires the payload to "parse exactly … with no residue".

Geometry (§11.2): G = (⌈4/2⌉, ⌈6/3⌉) = (2, 2), N = 4. Layout 2 = planar, so the addressed-tile
count is C·N = 2·4 = **8**, which `[R-CNT-17]` obliges entry_count to equal.

`[R-CNT-17]`: extent_length = 8 × 20 + ⌈8/2¹⁶⌉ × 4 = 160 + 4 = **164**.

Answer: **90, 103, 8, 164**.

## Q02 — packed planar bool tiles, padding carries the fill bit

Planar + bool ⇒ §14.3's packed plane. G = (⌈3/2⌉, ⌈3/4⌉) = (2, 1); N = 2; P = ∏Tᵢ = 2·4 = 8;
decoded size ⌈8/8⌉ = 1 byte, and P mod 8 = 0 so there are **no pad bits** (§14.3's pad bits arise
only when P mod 8 ≠ 0). Every byte here is therefore a value byte.

In-tile ordinal (§11.4, permanent for every linearization): k = u₀·T₁ + u₁ = 4u₀ + u₁.
Bit k mod 8 of byte k div 8 (§14.3), 0 = false, 1 = true.

`[R-SER-05]`: "at every padding position, a writer MUST encode … that channel's fill value —
… the fill bit in a packed plane". Fill is 0x01 = true, so every padding position is a set bit.

Tile (0,0): x₀ = u₀ ∈ {0,1} (both < 3, real); x₁ = u₁ ∈ {0,1,2,3}, u₁ = 3 ⇒ x₁ = 3 ≥ E₁ = 3, padding.
k = 3 and k = 7 are the padding positions ⇒ bits 3 and 7 set ⇒ **0x88**.

Tile (1,0): x₀ = 2 + u₀, so u₀ = 1 ⇒ x₀ = 3, the whole u₀ = 1 half (k = 4..7) is padding; and
within u₀ = 0, k = 3 is padding (x₁ = 3). ⇒ bits 3,4,5,6,7 set ⇒ **0xF8**.

Answer: **88, F8**.

## Q03 — trailer CRC

§6.2's layout, all little-endian, bytes [0,60):

```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
10 00 00 00 00 00 00 00  44 00 00 00 00 00 00 00
c0 00 00 00 00 00 00 00  ef be ad de 00 00 00 00
00 00 00 00 00 00 00 00  00 00 00 00
```

CRC-32C = 0x092F02D6, stored little-endian as `d6 02 2f 09`.

Answer: **d6 02 2f 09**.

## Q04 — interleaved decoded size and in-sample offset

P = 3·4·5 = 60. Element sizes: bool 1 (interleaved bool is "a single byte … with element size 1 in
the arithmetic below", §14.2), float64 8, int16 2 ⇒ Q = ΣBᵢ = 11.
Decoded size = P·Q = **660**.

In-tile ordinal of (2,1,3) = 2·(4·5) + 1·5 + 3 = 48. F_c = ΣB_j for j < c = 1 + 8 = 9.
§14.2's closing example: "channel c's value at in-tile ordinal u sits at byte u·Q + Fᶜ".
48·11 + 9 = **537**.

Answer: **660, 537**.

## Q05 — planar disk ordinal, index offset, segment, extent_length

G = (100, 100), N = 10 000. t = (2475 div 50, 1234 div 40) = (49, 30).
s = t₀·G₁ + t₁ = 4930 (§11.4, linearization 1).
Disk ordinal = c·N + s = 7·10 000 + 4930 = **74 930**.
§15.1: "The entry for the tile with disk ordinal k … at region byte 20·k" ⇒ **1 498 600**.
§15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))" ⇒ 74 930 div 65 536 = **1**.
entry_count = C·N = 80 000; extent_length = 80 000·20 + ⌈80 000/65 536⌉·4 = 1 600 000 + 8 = **1 600 008**.

Answer: **74930, 1498600, 1, 1600008**.

## Q06 — codec-1 lengths per channel, planar

G = (⌈25/10⌉, ⌈7/10⌉) = (3, 1), N = 3, P = 100, C = 2 ⇒ entry_count = 6.
Disk ordinal k ⇒ c = k div N, s = k mod N.

- k = 1 ⇒ c = 0 = `m` (bool, planar ⇒ packed plane): decoded size ⌈100/8⌉ = 13.
  `[R-COD-04]`: under codec 1 a non-sentinel entry's length MUST equal the decoded size ⇒ **13**.
- k = 4 ⇒ c = 1 = `v` (uint8, planar numeric): P·Bᶜ = 100·1 = **100**.

extent_length = 6·20 + ⌈6/2¹⁶⌉·4 = 120 + 4 = **124**.

Answer: **13, 100, 124**.

## Q07 — slack total, walk completeness

Claimants of the live committed state (§5.2, §9.7): front block [0,16) = 16; entry 0's stored extent
[16,316) = 300; the layer record's extent, i.e. the tile-index region, [800,844) = 44; the directory
[900,960) = 60; the live trailer [960,1024) = 64. Total claimed 484; F = 1024 ⇒ slack = **540**
(the runs [316,800) = 484 and [844,900) = 56).

Entry 1 (offset = S, length = S, crc = 5) is §15.3's row "offset = S ∧ length = S ∧ crc ≠ 0 —
*structural*: reject-tile" (register row T6). §9.7 disposes of it expressly: "An entry `[R-IDX-03]`
classifies reject-tile on a *structural* ground does not make the walk incomplete: the walk passes
over it, and the bytes it nominally addresses fall to slack (§15.3)." The verifier does not elect to
stop at the first violation, and no scope-level rejection or resource decline arises, so the walk
completes and §5.2's partial-total trigger is not met. Reported as the file's **total**.

Aside (does not change the answer): the scenario's 60-byte directory cannot in fact hold a layer
record — the minimum layer-record inline payload under §7.4 is 73 bytes (name 2, nine scalars 34,
one dimension entry 18, one channel entry 6, trailing fixed fields 13) plus a 24-byte header plus
the 4-byte region CRC = 101 bytes. The arithmetic asked for is fixed by the stated region bounds
regardless.

Answer: **540, total**.

## Q08 — entry_count against geometry

G₀ = ⌈100/32⌉ = 4, N = 4. Planar with C = 3 ⇒ addressed-tile count = C·N = 12, but entry_count = 4.
`[R-CNT-17]`: "an entry_count that does not equal the geometry-derived addressed-tile count, is a
validity error at layer scope."

The companion check passes and so is not the row: extent_length 84 = 4·20 + ⌈4/2¹⁶⌉·4, exactly
`[R-CNT-17]`'s formula for entry_count = 4, so L22 is clean and only L21 fires. L21's Instances cell
even names this direction ("planar C·N, entry_count smaller").

§21.3 row **L21**; heading outcome for §21.3 is **reject-layer**; Detector **reader**; Detected
**layer access**.

Answer: **L21, reject-layer, reader, layer access**.

## Q09 — a foreign major, reach, and the verifier's verdict

The file declares version_major = 3. `[R-CNF-13]` assesses only conditions that *reach* a file
declaring another major, and §21.2 states the derivation outright: "Deriving it there yields F8,
F14, F6 and both of F1's instances … and no other row." All four are satisfied here — the magic
at F−64 is exact, the CRC at F−4 verifies over [F−64, F−4), the front block is byte-identical to
the constant, and nothing is byte-reversed.

The two defects present are the nonzero reserved bytes at trailer offset 48 (F15) and dir_length = 2
at trailer offset 24 (F16). Neither reaches: §2.3's Note says of the first, "F15 does not reach
although its Governing rule cell cites `[R-CNT-24]`: the trailer bytes it requires be zero are
inside the 48 that rule lets a future major redefine"; offset 24 lies in the same redefinable 48,
and "dir_length ≥ 4" is a format-major-1 invariant, not one `[R-CNT-24]` fixes. "Every other
condition … is not assessed against a file declaring another major … and no §21 row restating it
records such a file." ⇒ **0** rows.

Reader's refusal: `[R-CNT-07]` — "A reader MUST reject-file when version_major is 0 (invalid) or is
a major it does not implement." (§2.3 names the same rule for the capability refusal.)

Verifier: it established no violation, and §2.3 makes an unimplemented major a paradigm
cannot-establish ground — "as when the file names a format major version it does not implement" —
with *cannot establish* "available only to a traversal that established no violation".
Verdict: **cannot establish**.

Answer: **0, [R-CNT-07], cannot establish**.

## Q10 — encoding-2 frame content size against the decoded document

§18.2 replaces `[R-COD-06]`'s tile-sized rule with one over the document: "The frame's content-size
field … MAY be present, and when present it MUST equal the byte length of the decoded document. A
mismatch is one of the frame constraints R4 registers, not a failure to decode under R3: the bytes
decode, and what is wrong is what the header said about them."

Declared 4096, decoded document 4097 bytes ⇒ R4. R4's own cell restates it: "the content-size field
breaks its constraint exactly when it is present and does not equal the decoded document's byte
length", with the instance "the content-size field declared smaller than the decoded length".
Everything else — magic, single frame, no dictionary ID, no content-checksum flag, no trailing
bytes, extent CRC, document content and sorting — is clean, so no other row fires.

§21.5's outcome is **ignore-record**; R4's Detected cell is **extent use**; §21.5's preamble is
explicit that "Every row here is a violation all the same", and §2.4 has a verifier certify "only
violation-free files", so certification is barred ⇒ **no**.

Answer: **R4, ignore-record, extent use, no**.

## Q11 — a nonconforming interleaved boolean byte the reader returns

The position lies inside the extents, so it is a real (non-padding) position — T2's subject, not
T4's ("the same byte at a padding position is T4's").

`[R-SER-08]`: "A reader that does not reject the tile and returns the value — whether or not it
detected the violation — MUST return 0x00 as false and every other byte as true — the value,
encoded 0x00 or 0x01 as above, and not the stored byte." 0x7F ⇒ true ⇒ returned as **01**.

Row **T2**; its Detector cell is **verifier** ("its assigned detector is the verifier, for which it
is a validity error at tile scope"). The file is **not** conforming: "Writers MUST NOT emit any byte
other than 0x00 or 0x01 as an interleaved bool value. Any other byte makes the file nonconforming."

Answer: **01, T2, verifier, no**.

## Q12 — §20.3 step 4's closed permission list

Permitted, verbatim: "its name, and its dimension and channel names, MAY change; an extent MAY grow,
and MUST NOT shrink; a planar layer's channel list MAY be extended at its end, or shortened from its
end; and a slab or alignment declaration MAY be declared, re-established or cleared … A commit MAY
make several of these changes at once."

Fixed, verbatim: "the layout, the linearization and the index encoding, the codec and the filter,
the rank and the dimension order, every tile extent, every channel's type and fill, an interleaved
layer's channel list, and the position of every planar channel but the last."

(a) grow E₀ 100→200 — a grown extent ⇒ **yes**.
(b) shrink E₁ 50→40 — "MUST NOT shrink"; "a shrink … [is a] rewrite" ⇒ **no**.
(c) filter 2→1 — the filter is on the fixed list ⇒ **no**.
(d) clear the slab declaration (S 8→0 with A_slab 4096→0, as `[R-CNT-23]` requires) together with a
    name change — both permitted, and several at once are permitted ⇒ **yes**.
(e) remove `g` from (r,g,b) — not a shortening *from the end*; it moves `b`, whose position is fixed
    ("the position of every planar channel but the last"), and "a planar channel inserted or removed
    anywhere but the end of the list are rewrites" ⇒ **no**.
(f) append `a` at the end and grow E₀ in the same commit — both permitted, several at once ⇒ **yes**.

Answer: **yes, no, no, yes, no, yes**.

## Q13 — a grow-and-shorten commit

Superseded generation: G₀ = ⌈21/10⌉ = 3, N = 3, C = 4, planar ⇒ entry_count = **12**.
New generation: G₀ = ⌈60/10⌉ = 6, N = 6, C = 2 ⇒ entry_count = **12** (unchanged by coincidence).
Both changes are on §20.3's permitted side (a grown extent; a planar channel list shortened from its
end), so the commit is available at all.

Disk ordinal of channel c1 at spatial ordinal 0 in the new generation: c·N + s = 1·6 + 0 = **6**.

Re-emission: `[R-WRT-04]` step 4 — "Every layer whose stored-tile set or index content this commit
changes has its tile-index region re-emitted in full … entries new to this generation (added tiles,
grown extents, an appended channel) emitted per §15, and every other entry byte-identical at its
disk-ordinal position (a growth renumbers ordinals wherever `[R-GEO-06]` moves them …)". Here both
change: the c2/c3 tiles leave the addressed set, three new spatial tiles per surviving channel enter
it as sentinels, and every ordinal renumbers because N goes 3 → 6 ⇒ **yes**.

Noted tension, resolved against the parenthetical: §13.3's non-normative Note says index content
changes "among the declaration changes §20.3 permits a layer that stores a tile, only a change to
entry_count does". That parenthetical is inaccurate for this shape — entry_count is unchanged while
every entry's identity changes — and §2.1 makes a Note non-normative while `[R-WRT-04]`'s own text
names grown extents and ordinal renumbering as re-emission triggers.

Answer: **12, 12, 6, yes**.

## Q14 — lz4 on a layer that addresses no tile

G = (⌈0/16384⌉, ⌈1000/16384⌉) = (0, 1) ⇒ N = 0; interleaved ⇒ addressed-tile count 0, matching
entry_count = 0, extent slot (0,0) and crc_of_crc_array = 0 as `[R-CNT-17]`/`[R-CNT-23]` require.
`[R-GEO-02]` makes a zero extent valid. P = 16384² = 268 435 456, Q = 8, P·Q = 2 147 483 648 = 2³¹,
well inside `[R-ENC-04]`'s 2⁶³ − 1 ceiling, which §17.2's Note says *is* checked in an empty layer.

(1) `[R-COD-07]`'s cap is quantified over addressed tiles, and its Note says so: "a layer that
addresses none … satisfies it whatever its tile shape declares, and codec 4 is conforming there."
⇒ **yes**, conforming.

(2) L44's condition is exactly that cap ("Codec 4 (lz4) declared on a layer any of whose addressed
tiles' decoded size exceeds 0x7E000000 bytes"), and there is no addressed tile ⇒ **no**.

(3) §21.9: "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or not …
A layer addressing no tile (§11.2) therefore has no tile whose decoded size the table bounds …
a file containing no instance of a kind does not exceed that row, whatever its declarations would
derive." So this file's every quantity lies within the table, and `[R-ERR-04]`: "Software that
declines **on that ground** a file whose every quantity lies within the table is not a conforming
reader" ⇒ **no**.

Answer: **yes, no, no**.

## Q15 — compaction

**Scenario A.** Entry 3 (offset = S, length = 40) is §15.3's row "offset = S ∧ length ≠ S … —
*structural*: reject-tile" (T7). §20.5: "An entry §15.3 classifies reject-tile on a structural
ground is neither — `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so
regenerating the region cannot proceed without meeting it, and the violation is thereafter one the
compactor has detected. `[R-WRT-06]` then obliges refusal: the compactor can neither reproduce the
entry nor invent a replacement, and no drop is available, a tile-index entry being no record
§20.4's table licenses dropping." One word: **refuse**.

**Scenario B.** `[R-WRT-07]`: it "regenerates each tile-index region any of whose stored extents the
output relocates (entry offsets new; entry lengths, entry crcs, and sentinel entries unchanged;
segment CRCs recomputed over the entries as re-emitted), and updates the layer-record fields
covering a regenerated region (crc_of_crc_array)."

- (i) entry crc — "each index entry's crc is unchanged" ⇒ identical.
- (ii) entry offset — "entry offsets new" ⇒ changed.
- (iii) entry length — "entry lengths … unchanged" ⇒ identical.
- (iv) the sentinel's 20 bytes — "a sentinel is re-emitted unchanged" ⇒ identical.
- (v) entry_count — the layer's geometry is untouched, and crc_of_crc_array is the only layer-record
  field the rule updates ⇒ identical (5).
- (vi) crc_of_crc_array — expressly updated over recomputed segment CRCs taken over entries whose
  offsets moved ⇒ not carried through identically.

Answer: **refuse; i, iii, iv, v**.
